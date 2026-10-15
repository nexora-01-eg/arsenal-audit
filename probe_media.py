"""READ-ONLY media probers. Usage: python probe_media.py video|audio
PyAV header reads only (no full decode). Output to audit dir.
"""
import json
import os
import sys

AUDIT = r"F:\Arsenal_audit\audit_20260919_01"
INV = os.path.join(AUDIT, "inventory.jsonl")
VIDEO_EXTS = {".mp4", ".mov", ".mkv", ".avi", ".webm", ".m4v", ".mpg",
              ".mpeg", ".3gp", ".flv", ".wmv", ".m2ts"}
AUDIO_EXTS = {".mp3", ".wav", ".ogg", ".oga", ".flac", ".m4a", ".aac",
              ".opus", ".wma", ".aiff", ".aif", ".mid", ".midi"}


def probe_one(path):
    import av
    try:
        c = av.open(path)
    except Exception as e:
        return {"ok": False, "error": f"open: {e}"}
    try:
        info = {"ok": True, "format": c.format.name if c.format else "",
                "duration": round(c.duration / 1e6, 3) if c.duration else None,
                "bitrate": c.bit_rate, "streams": []}
        for s in c.streams:
            d = {"type": s.type,
                 "codec": s.codec_context.name if s.codec_context else ""}
            if s.type == "video":
                d.update({"width": s.width, "height": s.height,
                          "fps": round(float(s.average_rate), 3)
                          if s.average_rate else None,
                          "frames": s.frames,
                          "pix_fmt": s.format.name if s.format else ""})
            if s.type == "audio":
                cc = s.codec_context
                d.update({"sample_rate": cc.sample_rate if cc else None,
                          "channels": cc.channels if cc else None,
                          "layout": str(cc.layout).split(":")[0] if cc and cc.layout else ""})
            info["streams"].append(d)
        return info
    finally:
        c.close()


def main():
    which = sys.argv[1]
    exts = VIDEO_EXTS if which == "video" else AUDIO_EXTS
    recs = [json.loads(l) for l in
            open(INV, encoding="utf-8") if '"error"' not in l]
    targets = [r for r in recs if r["ext"] in exts]
    out_path = os.path.join(AUDIT, f"{which}_meta.jsonl")
    ok = fail = 0
    with open(out_path, "w", encoding="utf-8") as f:
        for i, r in enumerate(targets):
            p = os.path.join(r"F:\Arsenal", r["path"])
            m = probe_one(p)
            m.update({"path": r["path"], "size": r["size"]})
            f.write(json.dumps(m, ensure_ascii=False) + "\n")
            ok += m.get("ok", False)
            fail += (not m.get("ok", False))
            if (i + 1) % 100 == 0:
                print(f"{i + 1}/{len(targets)} ok={ok} fail={fail}", flush=True)
    print(f"DONE {which}: n={len(targets)} ok={ok} fail={fail}")

if __name__ == "__main__":
    main()
