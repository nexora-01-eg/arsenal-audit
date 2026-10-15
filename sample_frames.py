"""READ-ONLY frame sampler + contact-sheet builder.
Usage: python sample_frames.py
Samples every 10th MH video (deterministic), 3 frames each, montages of 8.
"""
import json
import os
from PIL import Image, ImageDraw

ARSENAL = r"F:\Arsenal"
AUDIT = r"F:\Arsenal_audit\audit_20260919_01"
FRM = os.path.join(AUDIT, "frames")
os.makedirs(FRM, exist_ok=True)

v = [json.loads(l) for l in open(os.path.join(AUDIT, "video_meta.jsonl"),
                                 encoding="utf-8")]
mh = sorted([x for x in v if x.get("ok") and x["path"].startswith("MH -")],
            key=lambda x: x["path"])
sample = [mh[i] for i in range(0, len(mh), 10)]
print("sampling", len(sample), "of", len(mh))

import av

def grab(path, fracs):
    c = av.open(path)
    try:
        vs = next(s for s in c.streams if s.type == "video")
        dur = (c.duration or 0) / 1e6
        outs = []
        for f in fracs:
            t = max(0.1, dur * f)
            c.seek(int(t * 1e6))
            for frame in c.decode(vs):
                if frame.time >= t - 0.5:
                    outs.append(frame.to_image())
                    break
        return outs
    finally:
        c.close()

index = []
for n, x in enumerate(sample):
    p = os.path.join(ARSENAL, x["path"])
    try:
        imgs = grab(p, (0.25, 0.5, 0.75))
    except Exception as e:
        print("FAIL", x["path"], str(e)[:80])
        continue
    thumbs = []
    for k, im in enumerate(imgs):
        im.thumbnail((320, 320))
        fp = os.path.join(FRM, f"vid{n:02d}_{k}.jpg")
        im.save(fp, quality=82)
        thumbs.append(fp)
    index.append({"n": n, "path": x["path"],
                  "duration": x.get("duration"), "frames": thumbs})
json.dump(index, open(os.path.join(AUDIT, "frame_index.json"), "w",
                      encoding="utf-8"), ensure_ascii=False, indent=1)

TH = 200
def sheet(items, name):
    cols, rows = 4, 2
    cw, ch = 320 * 3 + 30, TH + 44
    canvas = Image.new("RGB", (cols * cw, rows * ch), (18, 18, 18))
    d = ImageDraw.Draw(canvas)
    for i, it in enumerate(items):
        cx, cy = (i % cols) * cw, (i // cols) * ch
        d.text((cx + 6, cy + 4), f"[{it['n']}] {it['path'].split(chr(92))[-1][:52]}",
               fill=(255, 220, 90))
        for k, fp in enumerate(it["frames"]):
            im = Image.open(fp)
            w, h = im.size
            im = im.resize((320, TH))
            canvas.paste(im, (cx + k * 320 + 10, cy + 28))
    canvas.save(os.path.join(FRM, name), quality=85)
    print("sheet", name)

for g in range(0, len(index), 8):
    sheet(index[g:g + 8], f"sheet_{g // 8:02d}.jpg")
print("indexed:", len(index))
