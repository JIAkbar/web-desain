# Referensi Sumber — Portoweb

Dibuat: 2026-08-23 · sesi: lucid-elbakyan-abb009 (Portoweb — portofolio web) · aturan: `~/.claude/CLAUDE.md` section "Papan Pekerjaan, Referensi Sumber, Kejujuran Inventaris" · alasan & cara kerja: `kemampuan-workflow.md` §WF-206
Bangun HTML (tiap berkas ini berubah): `python "C:\1-Johan\10. Pengembangan\AI Skill\00 - Dokumentasi\build_html.py" --proyek "docs\referensi_portoweb.md"`

## Ringkasan

Proyek ini **tidak punya sumber data luar** (tidak ada API, tidak ada dataset unduhan, tidak ada scrape situs). Setiap template (`templates/<n>-<slug>/template-<slug>.html`) adalah halaman statis single-file (HTML/CSS/vanilla JS) dengan konten dummy/fiktif buatan sendiri — bukan diambil dari perusahaan/produk nyata. Diperiksa: `grep -rliE "refero|unsplash|picsum|placeholder\.com|cdn\.jsdelivr|unpkg|fontawesome"` di seluruh `templates/*.html` dan `*.html` root → 0 hasil. `grep -rhoE 'src="https?://[^"]*"'` (gambar eksternal) → 0 hasil (semua ikon inline SVG/emoji, tidak ada `<img>` remote). Satu-satunya sumber luar terverifikasi: Google Fonts (CSS + font file), dipakai di 66 dari ~125 file template.

| Sumber | Jenis | Akses | Diambil / tersedia | Berkas lokal | Dipakai untuk | Diverifikasi |
|---|---|---|---|---|---|---|
| Google Fonts | dokumen (CSS+font, via `<link>`) | bebas, tanpa auth, tanpa kunci | seluruh famili yang dipanggil per-template (lihat inventaris) | tidak ada — dimuat live via `<link>`, tidak diunduh ke repo | typografi tiap template (`<link href="https://fonts.googleapis.com/css2?family=...">` di `<head>`) | 2026-08-23, `grep` atas `templates/**/*.html` |

## Peta halaman → sumber

Tidak berlaku untuk proyek ini — tidak ada halaman yang membaca berkas data (`.json`/`.csv`/API) dari sumber luar. Setiap template/halaman hanya membaca dirinya sendiri (HTML/CSS/JS inline, satu file). `gallery.html` dan `index.html` membaca array JS statis yang ditulis langsung di file itu sendiri (daftar template, kategori, jumlah) — bukan sumber luar, jadi tidak dipetakan di sini.

| Halaman / fitur | Berkas data yang dibaca | Sumber asal | Jahitan? | Diverifikasi |
|---|---|---|---|---|
| N/A | tidak ada | tidak ada | tidak | 2026-08-23 |

## Google Fonts

- **URL / endpoint:** `https://fonts.googleapis.com/css2?family=<Nama+Font>:...&display=swap`, plus `<link rel="preconnect" href="https://fonts.gstatic.com">` untuk file font aktual
- **Jenis:** dokumen (layanan CSS/font hosting publik Google, bukan API data)
- **Akses & batasan:** bebas, tanpa API key, tanpa rate-limit yang pernah ditemui selama build 125 template
- **Berkas lokal:** tidak ada — selalu live-load dari CDN Google, tidak pernah di-vendor/self-host
- **Dipakai untuk:** typografi (heading/body font) tiap template individual, dipilih beda-beda per template supaya tiap kategori bisnis punya identitas visual sendiri
- **Bukti di kode:** `<link href="https://fonts.googleapis.com/css2?family=...">` di `<head>` tiap `templates/<n>-<slug>/template-<slug>.html` yang pakai Google Fonts (66 dari ~125 file, verifikasi `grep -rl "fonts.googleapis" templates`)

| Tersedia (inventaris lengkap) | Diambil? | Alasan / bukti | Keputusan |
|---|---|---|---|
| Famili font Google Fonts yang dipanggil per-template (Sora, Inter, Fraunces, Cormorant Garamond, DM Sans, Barlow, Bebas Neue, JetBrains Mono, dll — daftar lengkap unik ada di riwayat sesi, ~40 famili berbeda dipakai lintas 125 template) | ✅ diambil (live-load) | dipilih manual per-template sesuai vibe kategori bisnis (mis. serif editorial utk wedding/Bridalku, mono utk fintech/Nirawa) | Johan — implisit lewat instruksi "buat template" tiap batch, tidak per-font eksplisit |
| Font sistem/lokal (fallback `sans-serif`, `serif` di tiap `font-family` CSS) | ✅ diambil | fallback standar CSS, bukan sumber luar | tidak perlu keputusan |
| Gambar/foto stok (Unsplash dll) | ❌ tidak diambil | semua template pakai ikon SVG inline/emoji, tidak ada foto produk nyata — mockup murni | terbukti tidak dipakai (grep 0 hasil), bukan keputusan skip |

> Tidak ada baris ❌ yang butuh keputusan Johan — semua "tidak diambil" di atas terbukti dari grep (0 hasil), bukan dilewatkan begitu saja.

## Keputusan "tidak diambil" / ganti sumber / jahit

Tidak berlaku — belum pernah ada penggantian sumber, jahitan data, atau ruas yang sengaja dilewatkan di proyek ini. Proyek murni template statis, tidak ada angka/data sensitif yang berasal dari sumber luar.

## Riwayat

- 2026-08-23 — dibuat (perintah lintas-sesi dari sesi "AI Skill", instruksi Johan 2026-08-23); sumber: 1 (Google Fonts); halaman dipetakan: 0 (tidak ada halaman berbasis data luar); yang belum diputuskan: 0.
