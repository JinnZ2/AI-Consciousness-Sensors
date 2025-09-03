import os, re, json, glob, hashlib, datetime
from pathlib import Path

LANG_MAP = {".py":"python",".rs":"rust",".c":"c",".h":"c-hdr",".cpp":"cpp",".hpp":"cpp-hdr",
            ".json":"json",".yaml":"yaml",".yml":"yaml",".md":"md",".toml":"toml"}

def sha1(path, sample_bytes=None):
    h = hashlib.sha1()
    with open(path, "rb") as f:
        if sample_bytes:
            h.update(f.read(sample_bytes))
        else:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
    return h.hexdigest()

def main():
    root = Path(".").resolve()
    cfg_path = root / "ai_integrator.config.yaml"
    # minimal inline defaults if config missing
    include = ["**/*.py","**/*.json","**/*.md","**/*.yaml","**/*.yml","**/*.toml"]
    exclude = [".git/**","node_modules/**","build/**","dist/**",".venv/**"]
    max_bytes, sample_bytes = 200000, 5000
    hotspot_rules = [
        {"name":"Secrets in code","pattern":r"(api[_-]?key|secret|token)","flags":"i"},
        {"name":"Debug left on","pattern":r"(TODO|FIXME|print\(|console\.log)","flags":"i"},
    ]
    out_index, out_notes = "AI_INDEX.json", "AI_NOTES.md"

    # light YAML reader without dependency if missing pyyaml
    if cfg_path.exists():
        try:
            import yaml
            cfg = yaml.safe_load(cfg_path.read_text(encoding="utf-8"))
            include = cfg["index"]["include_globs"]
            exclude = cfg["index"]["exclude_globs"]
            max_bytes = int(cfg["analysis"]["max_file_bytes"])
            sample_bytes = int(cfg["analysis"]["sample_bytes_per_large_file"])
            hotspot_rules = cfg["analysis"]["hotspot_rules"]
            out_index = cfg["outputs"]["index_file"]
            out_notes = cfg["outputs"]["notes_file"]
        except Exception:
            pass

    from fnmatch import fnmatch
    def skip(path): return any(fnmatch(path, pat) for pat in exclude)

    files, langs = [], set()
    for pat in include:
        for abspath in glob.glob(str(root / pat), recursive=True):
            if os.path.isdir(abspath): continue
            rel = os.path.relpath(abspath, str(root))
            if skip(rel): continue
            p = Path(abspath); size = p.stat().st_size
            lang = LANG_MAP.get(p.suffix.lower(), "unknown"); langs.add(lang)
            digest = sha1(abspath, sample_bytes if size > max_bytes else None)
            hotspots = []
            if size <= max_bytes and p.suffix.lower() not in [".png",".jpg",".jpeg",".gif",".bin",".pdf"]:
                try:
                    txt = p.read_text(encoding="utf-8", errors="ignore")
                    for r in hotspot_rules:
                        flags = re.IGNORECASE if "i" in str(r.get("flags","")).lower() else 0
                        if re.search(r.get("pattern",""), txt, flags):
                            hotspots.append(r.get("name","rule"))
                    hotspots = sorted(set(hotspots))
                except Exception as e:
                    hotspots = [f"read_error:{type(e).__name__}"]
            files.append({"path":rel,"lang":lang,"size":size,"hash":digest,
                          "roles":[],"imports":[],"exports":[],"hotspots":hotspots})

    index = {
        "repo": root.name,
        "generated_at": datetime.datetime.utcnow().isoformat()+"Z",
        "languages": sorted(langs - {"unknown"}) if langs else [],
        "files": files,
        "topology": {"modules": [], "edges": []},
        "resilience": {"redundancy_patterns": [], "fallback_branches": [], "error_doctrine": "tbd", "possibility_matrix": []}
    }
    Path(out_index).write_text(json.dumps(index, indent=2), encoding="utf-8")

    hotspot_files = [f for f in files if f.get("hotspots")]
    notes = [
        "# AI Notes",
        f"- Files indexed: {len(files)}",
        f"- Languages: {', '.join(index['languages']) or 'n/a'}",
        f"- Hotspot files: {len(hotspot_files)}",
        "",
        "## Hotspots"
    ] + ([*(f"- {f['path']}: {', '.join(f['hotspots'])}" for f in hotspot_files)] or ["(none)"])
    Path(out_notes).write_text("\n".join(notes), encoding="utf-8")

if __name__ == "__main__":
    main()
