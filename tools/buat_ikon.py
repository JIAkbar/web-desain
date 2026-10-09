"""Logo konsep D (J dari petak grid 3x4) -> favicon.svg, PNG ikon, dan potongan SVG navbar.

Sumber tunggal: daftar CELLS di bawah (sama dengan konsep D di artifact Arah Desain JIA).
Jalankan dari root repo: python tools/buat_ikon.py
"""
from PIL import Image, ImageDraw

# (kolom, baris, penuh?) — petak penuh membentuk huruf J, sisanya petak samar.
CELLS = [(2, 0, 1), (2, 1, 1), (2, 2, 1), (2, 3, 1), (1, 3, 1), (0, 3, 1), (0, 2, 1),
         (0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0), (1, 2, 0)]
# Geometri konsep D dalam viewBox 64: x = 8 + c*16 (lebar 14), y = 6 + r*13 (tinggi 11).
X0, DX, W, Y0, DY, H = 8, 16, 14, 6, 13, 11
INK, FAINT, PAPER = (11, 11, 11), (217, 217, 214), (255, 255, 255)


def rects_svg(fill_full='currentColor', faint_attr='opacity=".15"'):
    out = []
    for c, r, full in CELLS:
        a = f'fill="{fill_full}"' if full else f'fill="{fill_full}" {faint_attr}'
        out.append(f'<rect x="{X0 + c * DX}" y="{Y0 + r * DY}" width="{W}" height="{H}" {a}/>')
    return ''.join(out)


def favicon_svg():
    # Hitam di tab terang, putih di tab gelap.
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
            '<style>rect{fill:#0b0b0b}@media (prefers-color-scheme:dark){rect{fill:#f2f2ee}}</style>'
            + ''.join(f'<rect x="{X0 + c * DX}" y="{Y0 + r * DY}" width="{W}" height="{H}"'
                      + ('' if full else ' opacity=".18"') + '/>' for c, r, full in CELLS)
            + '</svg>\n')


def png(size, content=0.82, bg=PAPER):
    """content = bagian sisi kanvas yang diisi logo (viewBox 64 dipetakan ke situ)."""
    ss = 8  # gambar besar lalu diperkecil supaya tepi halus
    S = size * ss
    im = Image.new('RGB', (S, S), bg)
    d = ImageDraw.Draw(im)
    k = S * content / 64
    off = (S - 64 * k) / 2
    for c, r, full in CELLS:
        x, y = off + (X0 + c * DX) * k, off + (Y0 + r * DY) * k
        d.rectangle([x, y, x + W * k - 1, y + H * k - 1], fill=INK if full else FAINT)
    return im.resize((size, size), Image.LANCZOS)


if __name__ == '__main__':
    open('favicon.svg', 'w', encoding='utf-8', newline='\n').write(favicon_svg())
    png(32, content=1.0).save('favicon-32.png', optimize=True)
    png(180).save('ikon-180.png', optimize=True)
    png(192).save('ikon-192.png', optimize=True)
    png(512).save('ikon-512.png', optimize=True)
    # Maskable: isi wajib di 80% tengah, jadi logo diperkecil.
    png(512, content=0.6).save('ikon-512-maskable.png', optimize=True)
    print(rects_svg())
