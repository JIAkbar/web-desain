"""Tambal luber horizontal template di HP (≤640 px).

Temuan audit 27 Okt 2026 (tools/audit_template.js, 390 px): 24 template luber.
Penyebab dan tambalan:
- hiasan/marquee/laci menu yang memang dimaksudkan terpotong → html, body overflow-x: clip
- tabel lebar → tabel bisa digulir sendiri
- tombol CTA navbar mendorong tombol menu keluar layar → CTA disembunyikan di HP
  (tetap ada di menu/hero), grid dua kolom tanpa breakpoint → satu kolom
Blok ditandai PENANDA sehingga skrip aman dijalankan ulang.
"""
import re
from pathlib import Path

PENANDA = "/* rapikan-hp */"
UMUM = "html,body{overflow-x:clip}table{display:block;max-width:100%;overflow-x:auto}"
KHUSUS = {
    "04-bisnis": ".tentang-inner{grid-template-columns:minmax(0,1fr)!important}.tentang-metrics{grid-template-columns:repeat(2,minmax(0,1fr))!important}", "12-blog": ".newsletter-section{margin-inline:0!important;max-width:100%}", "18-musik": "", "29-projectmgmt": "", "30-bizanalytics": "",
    "31-hrtech": "", "45-trading": ".analitik-wrap{grid-template-columns:minmax(0,1fr)!important}", "47-wealth": ".btn-cta{display:none}", "48-aiwriting": ".nav-actions .btn-primary{display:none}", "61-invoice": "",
    "70-jobboard": ".nav-actions .btn-primary{display:none}", "74-elearning": ".nav-actions .btn-primary{display:none}", "77-telemedicine": ".consult-grid{grid-template-columns:minmax(0,1fr)!important}", "82-mentalhealth": ".nav-actions .btn-primary{display:none}",
    "84-defi": "", "86-apidevpro": "",
    "02-pendidikan": ".nav-cta .btn-cta-outline,.nav-cta .btn-cta-fill{display:none}",
    "05-komunitas": ".btn-donate{display:none}",
    "25-travel": ".nav-right .btn-book{display:none}",
    "17-properti": ".btn-agen{display:none}",
    "19-hukum": ".btn-konsultasi{display:none}",
    "34-marketplace": ".nav-icon-btn:not(#cartNavBtn){display:none}",
    "35-rumahsakit": ".fas-grid{grid-template-columns:1fr}",
    "41-portaldesa": "[style*=\"grid-template-columns:1fr 1fr\"]{grid-template-columns:1fr!important}",
    "51-libracademia": ".btn-nav-primary{display:none}",
    "64-trackbase": ".nav-right .btn-ghost{display:none}.hero-inner,.cf-inner{grid-template-columns:minmax(0,1fr)!important}",
    "106-sparklehome": "nav .btn-primary,header .btn-primary{display:none}",
}


def main():
    for slug, css in KHUSUS.items():
        f = next(Path("templates", slug).glob("*.html"))
        teks = f.read_text(encoding="utf-8")
        # blok lama diganti supaya isi KHUSUS terbaru selalu terpakai
        teks = re.sub(r"<style>" + re.escape(PENANDA) + r".*?</style>\n", "", teks)
        blok = f"<style>{PENANDA}@media (max-width:640px){{{UMUM}{css}}}</style>\n"
        f.write_text(teks.replace("</head>", blok + "</head>", 1), encoding="utf-8")
        print("ditambal", f)


if __name__ == "__main__":
    main()
