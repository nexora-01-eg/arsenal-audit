"""READ-ONLY audio character probe: first-30s acoustic features + durations.
Usage: python probe_audio_char.py  (writes audio_char.jsonl)
"""
import json
import os

import numpy as np

AUDIT = r"F:\Arsenal_audit\audit_20260919_01"
ARSENAL = r"F:\Arsenal"


def features(path, limit_s=30.0):
    import av
    try:
        c = av.open(path)
    except Exception as e:
        return {"ok": False, "error": f"open: {e}"}
    try:
        astream = next((s for s in c.streams if s.type == "audio"), None)
        if astream is None:
            return {"ok": False, "error": "no audio stream"}
        res = av.AudioResampler(format="s16", layout="mono", rate=8000)
        blocks = []
        total = 0.0
        for frame in c.decode(astream):
            for rf in res.resample(frame) or []:
                a = np.frombuffer(bytes(rf.planes[0]), dtype=np.int16).astype(np.float32) / 32768.0
                blocks.append(a)
                total += len(a) / 8000.0
                if total >= limit_s:
                    break
            if total >= limit_s:
                break
        if not blocks:
            return {"ok": False, "error": "no samples"}
        x = np.concatenate(blocks)
        rms = float(np.sqrt((x ** 2).mean()))
        zc = float(((x[1:] >= 0) != (x[:-1] >= 0)).mean())
        win = x[: 8000 * 10]
        spec = np.abs(np.fft.rfft(win * np.hanning(len(win))))
        freqs = np.fft.rfftfreq(len(win), 1 / 8000.0)
        centroid = float((spec * freqs).sum() / max(spec.sum(), 1e-9))
        # energy dynamics: RMS over 0.5s windows, coefficient of variation
        w = 4000
        nw = max(len(x) // w, 1)
        env = np.array([np.sqrt((x[i * w:(i + 1) * w] ** 2).mean())
                        for i in range(nw)])
        dyn = float(env.std() / max(env.mean(), 1e-9))
        peak = float(np.abs(x).max())
        return {"ok": True, "seconds_analyzed": round(total, 1),
                "rms": round(rms, 4), "peak": round(peak, 3),
                "zcr": round(zc, 4), "centroid_hz": round(centroid, 1),
                "dynamics": round(dyn, 3)}
    finally:
        c.close()


def main():
    recs = [json.loads(l) for l in open(os.path.join(AUDIT, "audio_meta.jsonl"),
                                       encoding="utf-8")]
    music = [r for r in recs if r["path"].startswith("04_Music")]
    others = [r for r in recs if not r["path"].startswith("04_Music")]
    import random
    random.seed(7)
    targets = others + random.sample(music, min(60, len(music)))
    out = open(os.path.join(AUDIT, "audio_char.jsonl"), "w", encoding="utf-8")
    for i, r in enumerate(targets):
        m = features(os.path.join(ARSENAL, r["path"]))
        m.update({"path": r["path"], "duration": r.get("duration")})
        out.write(json.dumps(m, ensure_ascii=False) + "\n")
        if (i + 1) % 50 == 0:
            print(f"{i + 1}/{len(targets)}", flush=True)
    out.close()
    print("DONE", len(targets))

if __name__ == "__main__":
    main()
