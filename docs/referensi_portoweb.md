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

## Polaris web components (Shopify) — pilot antrean #23

- **URL:** `https://cdn.shopify.com/shopifycloud/polaris-2.0.js` (dipin ke 2.0; `polaris-2.js` ikut berubah). Dicek 26 Okt 2026 oleh sesi AI Skill: 200, 919.721 byte, `text/javascript`.
- **Dokumentasi:** https://shopify.dev/docs/api/app-home/web-components — 50 komponen dalam 7 kelompok (Actions 6, Feedback 5, Forms 17, Layout 10, Media 4, Overlay 2, Tipografi 6).
- **Akses & batas:** bebas, tanpa kunci. Dokumentasi resmi meminta `app-bridge.js` + meta `shopify-api-key`. Uji 26 Okt 2026 (sesi ini): tanpa keduanya komponen tetap tergambar dan konsol kosong.
- **Atribut:** paket tipe `@shopify/polaris-types@2.0.0` (`npm pack`, `dist/custom-elements.json` + `dist/polaris.d.ts`), diekstrak di folder sementara, tidak disalin ke repo. Komponen tambahan di paket itu yang bukan bagian dari 50: `s-press-button`, `s-scroll-box` (tidak dipakai).
- **Lisensi:** TIDAK disebut di dokumentasi web components; `package.json` paket tipe juga tanpa ruas `license`. Katalog AI Skill mencatat "boleh disalin: tidak tahu". Halaman hanya memuat skrip dari CDN Shopify, tidak menyalin kodenya. **Keputusan Johan diperlukan sebelum push/tayang**; sampai itu halaman bertanda `noindex` dan tidak dipush.
- **Berkas lokal:** TIDAK di repo ini. Landing pilot dipindah ke `AI Skill/04 - Referensi/Referensi Design Systems/landing/polaris/` (keputusan Johan 26 Okt 2026: "AI Skill, lokal saja"); `design-systems/` dibuang dari riwayat cabang 28 Okt 2026 (antrean #25). Bukti tangkapan versi 1 tetap di `docs/bukti-23/`.
- **Fon:** komponen memakai `ShopifyInter` (nol polos); halaman memakai Fraunces (Google Fonts) untuk judul dan Inter/Segoe UI untuk isi.

| Tersedia (inventaris) | Diambil? | Alasan / bukti | Keputusan |
|---|---|---|---|
| 50 komponen web components | ✅ semua | dihitung skrip di halaman: 50/50 terdaftar dan terpakai | Johan, "kerjakan #23" (26 Okt 2026) |
| `app-bridge.js` + meta `shopify-api-key` | ❌ | tidak dibutuhkan untuk menggambar di halaman lepas (uji 26 Okt 2026) | sesi ini, dengan bukti uji; bisa dibalik Johan |
| Paket React lama `Shopify/polaris` (MIT, diarsipkan) | ❌ | cadangan, tidak dibutuhkan karena web components jalan | sesi ini |

## Pustaka CDN landing & galeri 3D — antrean #28, #30, #31 (27–28 Okt 2026)

Semua dimuat live dari CDN dengan versi dikunci; tidak ada kode pustaka yang disalin ke repo. Dicek `curl` = 200 saat dibangun.

| Pustaka | Versi | Lisensi | URL | Dipakai di |
|---|---|---|---|---|
| three.js (+ addons `examples/jsm`) | 0.170.0 | MIT | `https://cdn.jsdelivr.net/npm/three@0.170.0/` | `index.html`, template 126–131 |
| Material Web (`@material/web`) | 2.2.0 | Apache-2.0 | `https://cdn.jsdelivr.net/npm/@material/web@2.2.0/all.js/+esm` | 126-orbita |
| Bootstrap | 5.3.3 | MIT | `https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/` | 127-sonara |
| IBM Carbon web components | 2.60.0 | Apache-2.0 | `https://1.www.s81c.com/common/carbon/web-components/version/v2.60.0/` (token tema white/g100 disalin ke halaman karena berkas tema IBM hanya ada di jalur `latest`) | 128-lintas |
| Tailwind CSS browser | 4.1.13 | MIT | `https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4.1.13` (token gaya shadcn/ui ditulis sendiri) | 129-nalar |
| Shoelace | 2.20.1 | MIT | `https://cdn.jsdelivr.net/npm/@shoelace-style/shoelace@2.20.1/cdn/` | 130-ruang |
| Fluent UI web components | 3.1.3 (+ `@fluentui/tokens` 1.0.0-alpha.24) | MIT | `https://cdn.jsdelivr.net/npm/@fluentui/web-components@3.1.3/dist/web-components-all.min.js` | 131-rapatin |
| GitHub Primer CSS | 21.5.1 | MIT | `https://cdn.jsdelivr.net/npm/@primer/css@21.5.1/dist/primer.min.css` | 132-kodekita |
| Adobe Spectrum Web Components (bundle) | 1.12.4 | Apache-2.0 | `https://esm.sh/@spectrum-web-components/bundle@1.12.4` | 133-kanvas |
| Ionic (`@ionic/core`) | 8.8.19 | MIT | `https://cdn.jsdelivr.net/npm/@ionic/core@8.8.19/` | 134-jalanin |
| PatternFly | 6.6.1 | MIT | `https://cdn.jsdelivr.net/npm/@patternfly/patternfly@6.6.1/patternfly.min.css` (6.7.0 baru 13 hari, sengaja tidak dipakai) | 135-awannusa |
| daisyUI (+ Tailwind browser 4.1.11) | 5.0.43 | MIT | `https://cdn.jsdelivr.net/npm/daisyui@5.0.43/` | 136-kopiloka |
| Bulma | 1.0.4 | MIT | `https://cdn.jsdelivr.net/npm/bulma@1.0.4/css/bulma.min.css` | 137-sekolahku |
| GSAP + ScrollTrigger | 3.12.5 | lisensi standar GreenSock (gratis untuk situs) | `https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/` | 130-ruang, 131-rapatin |
| Google Fonts tambahan | — | OFL | Space Grotesk (pengganti fon mono di 48 template), Roboto, Manrope, IBM Plex Sans, Geist, dan fon isi landing 3D | template |

Fon angka: semua fon di atas bernol polos; Space Grotesk diuji raster 27 Okt 2026 (piksel gelap di tengah nol = 0, JetBrains Mono sebagai kontrol = 504).

## Keputusan "tidak diambil" / ganti sumber / jahit

Tidak berlaku — belum pernah ada penggantian sumber, jahitan data, atau ruas yang sengaja dilewatkan di proyek ini. Proyek murni template statis, tidak ada angka/data sensitif yang berasal dari sumber luar.

## Riwayat

- 2026-10-28 — tambah 6 pustaka design system untuk landing 3D 132–137 (#31).

- 2026-10-28 — tambah pustaka CDN landing baru (#28) dan 6 landing 3D × design system (#30); fon mono template diganti Space Grotesk (#29).

- 2026-10-28 — landing Polaris keluar dari repo, pindah ke AI Skill (#25).
- 2026-10-26 — tambah sumber Polaris web components (pilot #23); lisensi belum diputuskan Johan.
- 2026-08-23 — dibuat (perintah lintas-sesi dari sesi "AI Skill", instruksi Johan 2026-08-23); sumber: 1 (Google Fonts); halaman dipetakan: 0 (tidak ada halaman berbasis data luar); yang belum diputuskan: 0.
