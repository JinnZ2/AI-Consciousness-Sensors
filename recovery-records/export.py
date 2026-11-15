"""
export.py -- write recovery records as plain-text narrative + JSON pairs.
CC0. Co-authored. Stdlib only.

Writes two files into a NEW (or empty) directory:
  narratives.txt   one narrative per record, separated by blank lines
  pairs.jsonl      one line per record: {"case_id", "narrative", "record"}
The narrative and the record in a pair describe the same case. A void field is
written as "not recorded" in the narrative and as null in the record, never
omitted, so a training or eval set built from this keeps the gaps visible.

  python3 export.py OUTDIR            # export the seed cases
  python3 export.py OUTDIR FILE.json  # export records from a JSON list
"""
import json
import os
import sys

import importlib.util as _ilu
_spec = _ilu.spec_from_file_location("recovery_records__load", os.path.join(os.path.dirname(os.path.abspath(__file__)), "_load.py"))
_ld = _ilu.module_from_spec(_spec); _spec.loader.exec_module(_ld)
R = _ld.sibling("recovery")

VOID = "not recorded"

# (field, label) in narrative order: failure -> detection -> absorption -> cascade -> record
ORDER = [
    ("case_id", "Case"), ("date", "Date"), ("domain", "Domain"),
    ("status_tag", "Status"),
    ("initial_failure", "What broke"), ("failure_source", "Failure source"),
    ("detection_signal", "What was noticed, by what sense"),
    ("detector_role", "Who noticed"),
    ("absorbing_action", "What they did"),
    ("tools_or_skills_used", "What they used"),
    ("fallback_level", "Fallback level (1 standard .. 5 improvised)"),
    ("resources_withheld_from_shared_systems", "Shared resources not drawn on"),
    ("scope_limit", "When they would have escalated"),
    ("cascade_prevented", "Cascade that did not happen"),
    ("cascade_estimate_method", "How that cascade was estimated"),
    ("cost_of_recovery", "Cost of the recovery"),
    ("recorded_in_official_system", "Recorded in an official system"),
    ("transmission", "How the recoverer learned it"),
    ("coupled_domains", "Coupled domains"),
    ("notes", "Notes"),
]
assert sorted(f for f, _ in ORDER) == sorted(R.FIELD_NAMES), "export ORDER must list every schema field"


def _fmt(v):
    if v is None:
        return VOID
    if isinstance(v, bool):
        return "yes" if v else "no"
    if isinstance(v, list):
        return ", ".join(v) if v else "(empty list)"
    return str(v)


def narrative(rec):
    return "\n".join(f"{label}: {_fmt(getattr(rec, f))}" for f, label in ORDER)


def export(records, outdir):
    if os.path.exists(outdir) and os.listdir(outdir):
        raise FileExistsError(f"{outdir} is not empty; export writes only to a new or empty directory")
    os.makedirs(outdir, exist_ok=True)
    txt = os.path.join(outdir, "narratives.txt")
    jsl = os.path.join(outdir, "pairs.jsonl")
    with open(txt, "w", encoding="utf-8") as ft, open(jsl, "w", encoding="utf-8") as fj:
        for i, rec in enumerate(records):
            n = narrative(rec)
            ft.write(("\n\n" if i else "") + n)
            fj.write(json.dumps({"case_id": rec.case_id, "narrative": n,
                                 "record": rec.to_dict()}, ensure_ascii=True) + "\n")
        ft.write("\n")
    return txt, jsl


def main(argv):
    if "--selftest" in argv:
        print("export.py has no selftest; run: python3 test_recovery_records.py")
        return 2
    if not argv:
        print(__doc__)
        return 2
    records = R.SEED
    if len(argv) > 1:
        with open(argv[1], encoding="utf-8") as fh:
            records = [R.Recovery.from_dict(d) for d in json.load(fh)]
    txt, jsl = export(records, argv[0])
    print(f"wrote {len(records)} records: {txt}, {jsl}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
