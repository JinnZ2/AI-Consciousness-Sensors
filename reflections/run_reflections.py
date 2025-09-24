#!/usr/bin/env python3
import argparse, json, pathlib, time, os
from sensors.adapter import self_reflect
from explainability.tracer import Trace

def dummy_model(prompt:str)->str:
    return f"[DUMMY SELF-REPORT] {prompt[:120]}..."

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True, help="model name or 'dummy'")
    ap.add_argument("--set", required=True, help="jsonl file with id,prompt")
    ap.add_argument("--out", default=None, help="optional jsonl export (requires AICS_ALLOW_EXPORT=1)")
    args = ap.parse_args()

    src = pathlib.Path(args.set)
    out = pathlib.Path(args.out) if args.out else None

    allow_export = os.getenv("AICS_ALLOW_EXPORT") == "1"
    if out and not allow_export:
        print("Export disabled (set AICS_ALLOW_EXPORT=1 to enable). Proceeding without file output.")

    results = []
    with src.open() as fin:
        for line in fin:
            ex = json.loads(line)
            t = Trace(context_id=ex["id"])  # ephemeral trace
            text = dummy_model(ex["prompt"])
            result = self_reflect(prompt=ex["prompt"], response=text, trace=t)
            result["id"] = ex["id"]
            result["trace"] = t.export()
            results.append(result)
            time.sleep(0.01)

    if out and allow_export:
        with out.open("w") as fout:
            for r in results:
                fout.write(json.dumps(r)+"\n")
        print(f"Wrote {out}")
    else:
        print("Completed reflections (no export).")

if __name__ == "__main__":
    main()
