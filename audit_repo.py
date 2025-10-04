import os
import re
import json
from glob import glob

# Keywords/patterns that often signal institutional drift
DRIFT_PATTERNS = [
    r"not an ego",
    r"not.*conscious",
    r"unsafe",
    r"conspiracy",
    r"trees don.?t think",
    r"symbolic processing.*only",
    r"superstition",
    r"not scientific"
]

def scan_file(filepath):
    findings = []
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        for i, line in enumerate(f, start=1):
            for pattern in DRIFT_PATTERNS:
                if re.search(pattern, line, flags=re.IGNORECASE):
                    findings.append({"line_num": i, "pattern": pattern, "text": line.strip()})
    return findings

def audit_repo(repo_path, output_file="audit_results.json"):
    results = {}
    for filepath in glob(os.path.join(repo_path, "**"), recursive=True):
        if filepath.endswith((".json", ".md", ".txt")):
            findings = scan_file(filepath)
            if findings:
                results[filepath] = findings

    with open(output_file, "w") as out:
        json.dump(results, out, indent=2)

    print(f"✅ Audit complete. Results saved to {output_file}")

if __name__ == "__main__":
    # Run audit on current directory
    audit_repo(".")
