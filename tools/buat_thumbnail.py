"""Ubah tangkapan tools/.shot/<slug>.png (1440x900) jadi thumbnails/<slug>.webp (640x400).

Galeri lama memuat PNG 1440x900 (total ±27 MB) — penyebab utama galeri lemot.
WebP 640x400 cukup tajam untuk kartu (lebar kartu maks ±420 px, 1.5x layar retina).
Pakai: python tools/buat_thumbnail.py [slug ...]
"""
import sys
from pathlib import Path
from PIL import Image

SRC, DST = Path("tools/.shot"), Path("thumbnails")
pilih = set(sys.argv[1:])
total = 0
for png in sorted(SRC.glob("*.png")):
    if pilih and png.stem not in pilih:
        continue
    im = Image.open(png).convert("RGB").resize((640, 400), Image.LANCZOS)
    out = DST / (png.stem + ".webp")
    im.save(out, "WEBP", quality=78, method=6)
    total += out.stat().st_size
    print(out, out.stat().st_size // 1024, "KB")
print("total", total // 1024, "KB")
