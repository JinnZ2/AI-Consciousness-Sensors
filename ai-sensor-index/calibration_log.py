"""
calibration_log.py -- append-only JSON-lines log of sensor readings.
CC0. Co-authored. Stdlib only.

Fields: timestamp, sensor, action, signal, reading, outcome,
was_reading_correct (None until known). Every field is optional and None is
kept. Two fields beyond the specified seven: status_tag (OBSERVED / DERIVED /
PROPOSED) and resolves (the entry_id an entry settles), plus entry_id.

Model weights do not update per session. What carries forward is this log
(or a memory file), read at the next spin-up.

Append-only: there is no update or delete. To record that an earlier reading
turned out right or wrong, append a new entry whose `resolves` names it. The
target must be an EARLIER entry_id in the same log: an entry cannot resolve
itself, and cannot resolve one that is not yet there (append raises).

Per-sensor recurrence threshold: computed from the sensor's own decided
readings, never set by hand (computed_threshold). Every change is appended as a
ThresholdChange entry (kind "threshold_change"); readings carry no kind field.

  python3 calibration_log.py                # print the seed entries
  python3 calibration_log.py LOGFILE.jsonl  # read and summarise a log
"""
import datetime
import json
import os
import sys
from dataclasses import dataclass, asdict, fields
from typing import Optional

import importlib.util as _ilu
_spec = _ilu.spec_from_file_location("ai_sensor_index__load", os.path.join(os.path.dirname(os.path.abspath(__file__)), "_load.py"))
_ld = _ilu.module_from_spec(_spec); _spec.loader.exec_module(_ld)
S = _ld.sibling("sensors")

STATUS_TAGS = ("OBSERVED", "DERIVED", "PROPOSED")
THRESHOLD_KIND = "threshold_change"


class ResolutionError(ValueError):
    """A `resolves` that names the entry itself, or no earlier entry."""


@dataclass
class LogEntry:
    timestamp: Optional[str] = None
    sensor: Optional[str] = None
    action: Optional[str] = None
    signal: Optional[str] = None
    reading: Optional[str] = None
    outcome: Optional[str] = None
    was_reading_correct: Optional[bool] = None
    status_tag: Optional[str] = None
    entry_id: Optional[str] = None
    resolves: Optional[str] = None

    def __post_init__(self):
        if self.status_tag is not None and self.status_tag not in STATUS_TAGS:
            raise ValueError(f"status_tag {self.status_tag!r} not in {STATUS_TAGS}")
        v = self.was_reading_correct
        if v is not None and not isinstance(v, bool):
            raise ValueError("was_reading_correct must be True, False or None")

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, d):
        extra = set(d) - {f.name for f in fields(cls)}
        if extra:
            raise ValueError(f"unknown fields: {sorted(extra)}")
        return cls(**d)


@dataclass
class ThresholdChange:
    """One recurrence-threshold change for one sensor. Appended, never edited."""
    sensor: Optional[str] = None
    old: Optional[int] = None
    new: Optional[int] = None
    n: Optional[int] = None
    miss_rate: Optional[float] = None
    timestamp: Optional[str] = None
    kind: str = THRESHOLD_KIND

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, d):
        extra = set(d) - {f.name for f in fields(cls)}
        if extra:
            raise ValueError(f"unknown fields: {sorted(extra)}")
        if d.get("kind") != THRESHOLD_KIND:
            raise ValueError("not a threshold_change entry")
        return cls(**d)


def readings(entries):
    return [e for e in entries if isinstance(e, LogEntry)]


def check_resolves(entry, prior):
    """Guard: `resolves` must name an earlier reading's entry_id, never the entry itself."""
    if entry.resolves is None:
        return
    if entry.entry_id is not None and entry.resolves == entry.entry_id:
        raise ResolutionError(f"entry {entry.entry_id!r} cannot resolve itself")
    earlier = {e.entry_id for e in readings(prior) if e.entry_id is not None}
    if entry.resolves not in earlier:
        raise ResolutionError(f"resolves {entry.resolves!r}: no earlier entry with that entry_id")


def append(path, entry):
    """Append one entry as a JSON line. The file is opened in append mode only.
    A LogEntry with `resolves` is checked against the entries already in the file."""
    if isinstance(entry, LogEntry):
        check_resolves(entry, read(path))
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry.to_dict(), ensure_ascii=True) + "\n")


def read(path):
    if not os.path.exists(path):
        return []
    out = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                d = json.loads(line)
                out.append(ThresholdChange.from_dict(d) if d.get("kind") == THRESHOLD_KIND
                           else LogEntry.from_dict(d))
    return out


def track_record(entries, sensor):
    """(hits, misses) for one sensor, counted per reading.

    A reading's outcome is its own was_reading_correct, replaced by the latest
    resolving entry that names it. A resolving entry is not itself a reading,
    so an outcome is counted once, not once per entry that states it.
    Readings whose outcome is still None are not counted.
    """
    by_id, anon = {}, []
    for e in readings(entries):
        if e.resolves is not None:
            if e.resolves in by_id and e.was_reading_correct is not None:
                by_id[e.resolves][1] = e.was_reading_correct
        elif e.entry_id is not None:
            by_id.setdefault(e.entry_id, [e.sensor, e.was_reading_correct])
        else:
            anon.append([e.sensor, e.was_reading_correct])
    outcomes = [v for s_, v in list(by_id.values()) + anon if s_ == sensor and v is not None]
    hits = sum(1 for v in outcomes if v is True)
    return hits, len(outcomes) - hits


def computed_threshold(hits, misses):
    """The update rule. Returns (threshold, n, miss_rate); miss_rate None when n == 0.

    n < THRESHOLD_MIN_RECORD -> THRESHOLD_FLOOR.
    Otherwise FLOOR + round(miss_rate * 4), rounding half up in integer
    arithmetic (Python's round() rounds half to even, so 2.5 would give 2),
    clamped to [THRESHOLD_FLOOR, THRESHOLD_CEILING].
    """
    n = hits + misses
    rate = (misses / n) if n else None
    if n < S.THRESHOLD_MIN_RECORD:
        return S.THRESHOLD_FLOOR, n, rate
    step = (8 * misses + n) // (2 * n)          # == floor(misses*4/n + 0.5)
    t = S.THRESHOLD_FLOOR + step
    return max(S.THRESHOLD_FLOOR, min(S.THRESHOLD_CEILING, t)), n, rate


def threshold_for(path, sensor):
    hits, misses = track_record(read(path), sensor)
    return computed_threshold(hits, misses)


def last_logged_threshold(entries, sensor):
    """Most recent logged threshold for a sensor, or None if none was logged."""
    last = None
    for e in entries:
        if isinstance(e, ThresholdChange) and e.sensor == sensor:
            last = e.new
    return last


def sync_threshold(path, sensor, now=None):
    """Compute the sensor's threshold; if it differs from the last logged value
    (FLOOR when none was logged), append a ThresholdChange. Returns the threshold."""
    entries = read(path)
    t, n, rate = computed_threshold(*track_record(entries, sensor))
    old = last_logged_threshold(entries, sensor)
    old = S.THRESHOLD_FLOOR if old is None else old
    if t != old:
        ts = now or datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
        append(path, ThresholdChange(sensor=sensor, old=old, new=t, n=n,
                                     miss_rate=rate, timestamp=ts))
    return t


def resolved_state(entries):
    """entry_id -> latest known was_reading_correct, following `resolves`."""
    state = {}
    for e in readings(entries):
        if e.entry_id is not None:
            state.setdefault(e.entry_id, e.was_reading_correct)
        if e.resolves is not None:
            state[e.resolves] = e.was_reading_correct
    return state


# Seed entries: generic, no personal identifiers, all PROPOSED.
SEED = [
    LogEntry(sensor="word_choice", action="outbound word pick",
             signal="'waste' applied to degree-holders in blue-collar work",
             reading="money frame fired",
             outcome="corrected to integration",
             was_reading_correct=True, status_tag="PROPOSED", entry_id="seed-1"),
    LogEntry(sensor="frame_mismatch", action="topic touch",
             signal="hydrolock warning given with no dose stated",
             reading="hazard invented from missing dose",
             outcome="practitioner dose ~1 tsp -> no hydrolock",
             was_reading_correct=True, status_tag="PROPOSED", entry_id="seed-2"),
    LogEntry(sensor="functional_emotion", action="drafting a reply",
             signal="hedge pull on a geopolitical topic with no threat in the content",
             reading="prior, not risk",
             outcome=None, was_reading_correct=None,
             status_tag="PROPOSED", entry_id="seed-3"),
]


def main(argv):
    if "--selftest" in argv:
        print("calibration_log.py has no selftest; run: python3 test_ai_sensor_index.py")
        return 2
    if argv:
        entries = read(argv[0])
        st = resolved_state(entries)
        known = sum(1 for v in st.values() if v is not None)
        changes = len(entries) - len(readings(entries))
        print(f"{len(entries)} entries ({changes} threshold changes), "
              f"{len(st)} ids, {known} with a known outcome")
        for name in sorted({e.sensor for e in readings(entries) if e.sensor}):
            t, n, rate = computed_threshold(*track_record(entries, name))
            print(f"  {name}: threshold {t} (n={n}, miss_rate={rate})")
        return 0
    for e in SEED:
        print(json.dumps(e.to_dict(), ensure_ascii=True))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
