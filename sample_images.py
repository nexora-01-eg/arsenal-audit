"""READ-ONLY image stats + contact sheets for MH 01-images.
Header-only PIL stats for all; deterministic every-150th montage (12/sheet).
"""
import json
import os
from PIL import Image, ImageDraw

ARSENAL = r"F:\Arsenal"
AUDIT = r"F:\Arsenal_audit\audit_20260919_01"
IMG = os.path.join(AUDIT, "images")
os.makedirs(IMG, exist_ok=True)
IMG_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp", ".tiff"}

recs = [json.loads(l) for l in open(os.path.join(AUDIT, "inventory.jsonl"),
                                   encoding="utf-8")]
mh = sorted([r for r in recs
             if r["path"].startswith("MH -") and r["ext"] in IMG_EXTS],
            key=lambda r: r["path"])
print("mh images:", len(mh))
stats, fails = [], 0
for r in mh:
    p = os.path.join(ARSENAL, r["path"])
    try:
        with Image.open(p) as im:
            im.load()
            stats.append({"path": r["path"], "size": r["size"],
                          "format": im.format, "mode": im.mode,
                          "width": im.width, "height": im.height,
                          "alpha": int(im.mode in ("RGBA", "LA", "PA"))})
    except Exception as e:
        fails += 1
json.dump(stats, open(os.path.join(AUDIT, "image_stats.json"), "w",
                      encoding="utf-8"))
print("stats ok:", len(stats), "fail:", fails)

sample = [stats[i] for i in range(0, len(stats), 150)][:24]
print("montage sample:", len(sample))
TH = 220
for g in range(0, len(sample), 12):
    items = sample[g:g + 12]
    cols = 4
    rows = (len(items) + cols - 1) // cols
    cw, ch = 340, TH + 30
    canvas = Image.new("RGB", (cols * cw, rows * ch), (18, 18, 18))
    d = ImageDraw.Draw(canvas)
    for i, it in enumerate(items):
        cx, cy = (i % cols) * cw, (i // cols) * ch
        d.text((cx + 6, cy + 4), f"{it['width']}x{it['height']} {it['path'].split(chr(92))[-1][:44]}",
               fill=(255, 220, 90))
        try:
            im = Image.open(os.path.join(ARSENAL, it["path"])).convert("RGB")
            im.thumbnail((320, TH))
            c2 = Image.new("RGB", (320, TH), (18, 18, 18))
            c2.paste(im, ((320 - im.width) // 2, (TH - im.height) // 2))
            canvas.paste(c2, (cx + 10, cy + 26))
        except Exception as e:
            d.text((cx + 10, cy + 100), "UNREADABLE", fill=(255, 80, 80))
    canvas.save(os.path.join(IMG, f"img_{g // 12:02d}.jpg"), quality=85)
    print("sheet img_%02d" % (g // 12))
