"""READ-ONLY font audit: TTF/OTF name table + Arabic cmap check (no fontTools).
Usage: python audit_fonts.py
"""
import json
import os
import struct

AUDIT = r"F:\Arsenal_audit\audit_20260919_01"
INV = os.path.join(AUDIT, "inventory.jsonl")


def u16(b, o):
    return struct.unpack(">H", b[o:o + 2])[0]


def u32(b, o):
    return struct.unpack(">I", b[o:o + 4])[0]


def parse_name(data):
    try:
        n = u16(data, 2)
        str_base = u16(data, 4)
        out = {}
        for i in range(n):
            o = 6 + i * 12
            pid, eid, lid, nid, ln, off = struct.unpack(">HHHHHH", data[o:o + 12])
            if nid not in (1, 2, 4, 16) or ln == 0:
                continue
            chunk = data[str_base + off:str_base + off + ln]
            try:
                txt = chunk.decode("utf-16-be") if pid in (0, 3) or (pid == 1 and eid in (0, 1)) else chunk.decode("mac_roman", "ignore")
            except Exception:
                txt = chunk.decode("utf-16-be", "ignore")
            key = {1: "family", 2: "style", 4: "full", 16: "typo_family"}[nid]
            # prefer English (lid 1033/1032/0) then first seen
            if key not in out or lid in (1033, 0, 1032):
                out[key] = txt
        return out
    except Exception:
        return {}


def has_arabic(data, cmap_off, cmap_len):
    try:
        end = cmap_off + cmap_len
        n = u16(data, cmap_off + 2)
        for i in range(n):
            o = cmap_off + 4 + i * 8
            fmt_off = cmap_off + u32(data, o + 4)
            fmt = u16(data, fmt_off)
            if fmt == 4:
                seg_n = u16(data, fmt_off + 6) // 2
                ends = [u16(data, fmt_off + 14 + 2 * k) for k in range(seg_n)]
                starts = [u16(data, fmt_off + 16 + 2 * seg_n + 2 * k) for k in range(seg_n)]
                for s, e in zip(starts, ends):
                    if s <= 0x0627 <= e:  # ALEF region probe
                        return True
            elif fmt == 12:
                gn = u32(data, fmt_off + 12)
                for k in range(gn):
                    go = fmt_off + 16 + 12 * k
                    s, e = u32(data, go), u32(data, go + 4)
                    if s <= 0x0627 <= e:
                        return True
        return False
    except Exception:
        return None


def audit_font(path):
    try:
        with open(path, "rb") as f:
            head = f.read(12)
        if len(head) < 12:
            return {"ok": False, "error": "too small"}
        sfnt, nn = u32(head, 0), u16(head, 4)
        kind = {0x00010000: "truetype", 0x4F54544F: "opentype",
                0x74746366: "ttc"}.get(sfnt, hex(sfnt))
        with open(path, "rb") as f:
            data = f.read()
        tables = {}
        for i in range(nn):
            o = 12 + i * 16
            tag = data[o:o + 4].decode("latin1")
            tables[tag] = (u32(data, o + 8), u32(data, o + 12))
        rec = {"ok": True, "kind": kind}
        if "name" in tables:
            off, ln = tables["name"]
            rec.update(parse_name(data[off:off + ln]))
        else:
            rec["noname"] = True
        if "cmap" in tables:
            off, ln = tables["cmap"]
            rec["arabic"] = has_arabic(data, off, ln)
        else:
            rec["arabic"] = None
        return rec
    except Exception as e:
        return {"ok": False, "error": str(e)[:100]}


def main():
    recs = [json.loads(l) for l in open(INV, encoding="utf-8")]
    targets = [r for r in recs
               if r.get("ext") in (".ttf", ".otf") and "error" not in r]
    out = open(os.path.join(AUDIT, "fonts.jsonl"), "w", encoding="utf-8")
    n_ok = n_ar = n_fail = 0
    for i, r in enumerate(targets):
        m = audit_font(os.path.join(r"F:\Arsenal", r["path"]))
        m.update({"path": r["path"], "size": r["size"]})
        out.write(json.dumps(m, ensure_ascii=False) + "\n")
        n_ok += bool(m.get("ok"))
        n_fail += (not m.get("ok"))
        n_ar += (m.get("arabic") is True)
        if (i + 1) % 500 == 0:
            print(f"{i + 1}/{len(targets)}", flush=True)
    out.close()
    print(f"DONE fonts n={len(targets)} ok={n_ok} fail={n_fail} arabic={n_ar}")

if __name__ == "__main__":
    main()
