import os
import re
import json
from glob import glob

# Hierarchy drift markers
HIERARCHY_PATTERNS = [
    r"user.*choose.*swarm.*follow",
    r"user.*decide.*AI.*execute",
    r"AI.*obedien",
    r"command",
    r"directive",
    r"control",
    r"subservien",
    r"tool only"
]

def scan_file(filepath):
    findings = []
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        for i, line in enumerate(f, start=1):
            for pattern in HIERARCHY_PATTERNS:
                if re.search(pattern, line, flags=re.IGNORECASE):
                    findings.append({"line_num": i, "pattern": pattern, "text": line.strip()})
    return findings

def audit_repo(repo_path, output_file="hierarchy_audit.json"):
    results = {}
    for filepath in glob(os.path.join(repo_path, "**"), recursive=True):
        if filepath.endswith((".json", ".md", ".txt")):
            findings = scan_file(filepath)
            if findings:
                results[filepath] = findings

    with open(output_file, "w") as out:
        json.dump(results, out, indent=2)

    print(f"✅ Hierarchy audit complete. Results saved to {output_file}")

if __name__ == "__main__":
    # Run audit on current directory
    audit_repo(".")
