"""READ-ONLY forensic inventory walker for F:\Arsenal.
Writes inventory.jsonl + summary.json into the audit dir. Never writes
into the arsenal. Run: python inventory.py
"""
import json
import os
from collections import Counter
from datetime import datetime, timezone

ARSENAL = r"F:\Arsenal"
OUTDIR = r"F:\Arsenal_audit\audit_20260919_01"

def walk():
    n_dirs = 0
    recs = []
    for root, dirs, files in os.walk(ARSENAL):
        n_dirs += 1
        for fn in files:
            p = os.path.join(root, fn)
            try:
                st = os.stat(p, follow_symlinks=False)
            except OSError as e:
                recs.append({"path": os.path.relpath(p, ARSENAL), "error": str(e)})
                continue
            _, ext = os.path.splitext(fn)
            recs.append({
                "path": os.path.relpath(p, ARSENAL),
                "name": fn,
                "ext": ext.lower(),
                "size": st.st_size,
                "mtime": datetime.fromtimestamp(
                    st.st_mtime, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "top": os.path.relpath(p, ARSENAL).split(os.sep)[0],
            })
    return recs, n_dirs

def main():
    os.makedirs(OUTDIR, exist_ok=True)
    recs, n_dirs = walk()
    with open(os.path.join(OUTDIR, "inventory.jsonl"), "w", encoding="utf-8") as f:
        for r in recs:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    ext_c = Counter(r.get("ext", "") for r in recs if "error" not in r)
    top_c = Counter(r.get("top", "") for r in recs if "error" not in r)
    top_bytes = Counter()
    for r in recs:
        if "error" not in r:
            top_bytes[r["top"]] += r["size"]
    errs = [r for r in recs if "error" in r]
    summary = {
        "arsenal": ARSENAL,
        "scanned_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "total_files": len(recs),
        "total_dirs": n_dirs,
        "total_bytes": sum(r.get("size", 0) for r in recs),
        "unreadable": len(errs),
        "by_topdir": {k: {"files": top_c[k], "bytes": top_bytes[k]} for k in top_c},
        "by_ext_top60": dict(ext_c.most_common(60)),
        "n_extensions": len(ext_c),
    }
    with open(os.path.join(OUTDIR, "summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=1)
    print("files:", len(recs), "dirs:", n_dirs,
          "GB:", round(summary["total_bytes"] / 1e9, 2))
    print("errors:", len(errs))

if __name__ == "__main__":
    main()
