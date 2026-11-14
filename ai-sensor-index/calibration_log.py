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
turned out right or wrong, append a new entry whose `resolves` names it.

  python3 calibration_log.py                # print the seed entries
  python3 calibration_log.py LOGFILE.jsonl  # read and summarise a log
"""
import json
import os
import sys
from dataclasses import dataclass, asdict, fields
from typing import Optional

STATUS_TAGS = ("OBSERVED", "DERIVED", "PROPOSED")


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


def append(path, entry):
    """Append one entry as a JSON line. The file is opened in append mode only."""
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry.to_dict(), ensure_ascii=True) + "\n")


def read(path):
    if not os.path.exists(path):
        return []
    out = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                out.append(LogEntry.from_dict(json.loads(line)))
    return out


def resolved_state(entries):
    """entry_id -> latest known was_reading_correct, following `resolves`."""
    state = {}
    for e in entries:
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
        print(f"{len(entries)} entries, {len(st)} ids, {known} with a known outcome")
        return 0
    for e in SEED:
        print(json.dumps(e.to_dict(), ensure_ascii=True))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
