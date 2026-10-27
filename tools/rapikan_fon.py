"""Ganti fon monospace di templates/ dengan Space Grotesk (nol polos).

Aturan global §Fon Angka: angka tidak boleh bernol bertitik/bergaris.
Fon mono (JetBrains Mono, Fira Code, DM Mono, monospace bawaan, dll.) semuanya
bernol bertitik/bergaris, jadi diganti. Space Grotesk dipilih karena tetap berasa
"teknis"; nol polosnya diuji raster 27 Okt 2026 (piksel gelap di tengah nol = 0,
JetBrains Mono sebagai kontrol = 504).

Pakai:  python tools/rapikan_fon.py          (tulis)
        python tools/rapikan_fon.py --coba   (hanya laporan)
"""
import re
import sys
from pathlib import Path

PENGGANTI = "'Space Grotesk'"
LINK_FAMILY = "family=Space+Grotesk:wght@400;500;600;700"
NAMA_MONO = [
    "JetBrains Mono", "Fira Code", "IBM Plex Mono", "Roboto Mono", "Source Code Pro",
    "Space Mono", "DM Mono", "Geist Mono", "Ubuntu Mono", "Courier New", "SFMono-Regular",
    "SF Mono", "Menlo", "Consolas", "Monaco", "Liberation Mono",
    "Courier Prime", "Share Tech Mono", "Martian Mono", "Berkeley Mono",
]
GENERIK = ["ui-monospace", "monospace"]
KODE_INHERIT = "<style>/* fon angka: nol polos */code,kbd,pre,samp{font-family:inherit}</style>\n"


def ganti_link(teks):
    """Buang famili mono dari URL Google Fonts, tambah Space Grotesk."""
    def satu(m):
        url = m.group(0)
        for nama in NAMA_MONO:
            url = re.sub(r"family=" + re.escape(nama.replace(" ", "+")) + r"(:[^&\"']*)?&?", "", url)
        url = url.replace("css2?&", "css2?").replace("&&", "&").rstrip("&")
        if "Space+Grotesk" not in url:
            url = url.replace("css2?", "css2?" + LINK_FAMILY + "&", 1)
        if url.endswith("css2?") or "family=" not in url:
            url = "https://fonts.googleapis.com/css2?" + LINK_FAMILY + "&display=swap"
        return url
    return re.sub(r"https://fonts\.googleapis\.com/css2\?[^\"']*", satu, teks)


def ganti_nama(teks):
    for nama in NAMA_MONO:
        teks = re.sub(r"(['\"]?)" + re.escape(nama) + r"\1", PENGGANTI, teks)
    for g in GENERIK:
        # hanya sebagai nilai CSS (sesudah koma/titik dua/spasi, sebelum ; , } kutip atau spasi)
        teks = re.sub(r"(?<=[,:\s'\"])" + re.escape(g) + r"(?=\s*[;,}\"'\n)])", "sans-serif", teks)
    # rapikan urutan ganda: 'Space Grotesk', 'Space Grotesk' → satu
    teks = re.sub(r"'Space Grotesk'(\s*,\s*'Space Grotesk')+", PENGGANTI, teks)
    teks = re.sub(r"sans-serif(\s*,\s*sans-serif)+", "sans-serif", teks)
    return teks


def main():
    coba = "--coba" in sys.argv
    pola = re.compile("|".join(re.escape(n) for n in NAMA_MONO + GENERIK), re.I)
    berubah = 0
    for f in sorted(Path("templates").glob("*/*.html")):
        asli = f.read_text(encoding="utf-8")
        if not pola.search(asli):
            continue
        baru = ganti_nama(ganti_link(asli))
        if "Space Grotesk" in baru and "Space+Grotesk" not in baru:
            link = f'<link href="https://fonts.googleapis.com/css2?{LINK_FAMILY}&display=swap" rel="stylesheet">\n'
            baru = baru.replace("</head>", link + "</head>", 1)
        if "code,kbd,pre,samp{font-family:inherit}" not in baru:
            baru = baru.replace("</head>", KODE_INHERIT + "</head>", 1)
        sisa = pola.findall(baru)
        print(f"{f}: sisa mono {len(sisa)} {sorted(set(sisa))[:4]}")
        if baru != asli:
            berubah += 1
            if not coba:
                f.write_text(baru, encoding="utf-8")
    print("berkas berubah:", berubah, "(coba)" if coba else "")


if __name__ == "__main__":
    main()
