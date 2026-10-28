// Buat og-image.png (1200x630) dari rupa landing: judul hero + adegan 3D isometrik asli.
// Pakai (server lokal menyajikan root repo):  node tools/buat_og.js [http://localhost:5177]
// 1. Tangkap kanvas hero 3D landing (latar transparan) dalam tema terang.
// 2. Susun kartu OG dengan token & fon landing, lalu simpan ke og-image.png.
const { chromium } = require('playwright');
const path = require('path');

const base = (process.argv[2] || 'http://localhost:5177').replace(/\/$/, '');
const root = path.join(__dirname, '..');

(async () => {
  const browser = await chromium.launch({ args: ['--enable-unsafe-swiftshader', '--use-angle=swiftshader'] });

  // 1. adegan 3D — reducedMotion supaya balok sudah berdiri penuh & diam
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2, reducedMotion: 'reduce' });
  await ctx.addInitScript(() => { localStorage.setItem('pf_theme', 'light'); localStorage.setItem('pf_lang', 'id'); });
  const page = await ctx.newPage();
  await page.goto(base + '/index.html', { waitUntil: 'networkidle' });
  await page.waitForSelector('#heroStage.ready');
  await page.waitForTimeout(1500);
  await page.addStyleTag({ content: '.stage-tag{display:none!important}html,body{background:transparent!important}' });
  const scene = (await page.locator('#heroStage').screenshot({ omitBackground: true })).toString('base64');
  await ctx.close();

  // 2. kartu OG
  const og = await browser.newPage({ viewport: { width: 1200, height: 630 } });
  await og.setContent(`<!doctype html><html><head>
<link href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@800;900&family=Archivo:wght@500;600&display=block" rel="stylesheet">
<style>
  *{margin:0;padding:0;box-sizing:border-box}
  body{width:1200px;height:630px;background:#f4f3ef;color:#111;font-family:'Archivo',sans-serif;position:relative;overflow:hidden;font-variant-numeric:tabular-nums}
  .grid{position:absolute;inset:0;background-image:linear-gradient(#e6e3dc 1px,transparent 1px),linear-gradient(90deg,#e6e3dc 1px,transparent 1px);background-size:40px 40px;opacity:.55}
  .top{position:absolute;left:64px;top:52px;display:flex;align-items:center;gap:12px;font-family:'Big Shoulders Display';font-weight:900;font-size:34px}
  .avail{position:absolute;right:64px;top:56px;display:flex;align-items:center;gap:10px;padding:8px 16px 8px 12px;border:1.5px solid #bdb9ae;border-radius:999px;background:#fff;font-size:18px;font-weight:500;color:#2b2b29}
  .avail i{width:10px;height:10px;border-radius:50%;background:#16a34a}
  h1{position:absolute;left:64px;top:132px;font-family:'Big Shoulders Display';font-weight:900;text-transform:uppercase;font-size:112px;line-height:.9;letter-spacing:-.005em}
  h1 span{display:block} h1 .o{color:#ff5b1f}
  .sub{position:absolute;left:64px;bottom:56px;display:flex;align-items:center;gap:14px;font-size:24px;font-weight:600;color:#2b2b29}
  .sub b{width:12px;height:12px;background:#ff5b1f;border-radius:2px}
  .scene{position:absolute;left:650px;top:96px;width:500px;height:auto}
  .url{position:absolute;right:64px;bottom:58px;font-size:20px;font-weight:600;color:#5f5e59}
</style></head><body>
  <div class="grid"></div>
  <img class="scene" src="data:image/png;base64,${scene}">
  <div class="top"><svg viewBox="0 0 64 64" width="34" height="34"><g fill="#111"><rect x="40" y="6" width="14" height="11"/><rect x="40" y="19" width="14" height="11"/><rect x="40" y="32" width="14" height="11"/><rect x="40" y="45" width="14" height="11"/><rect x="24" y="45" width="14" height="11"/><rect x="8" y="45" width="14" height="11"/><rect x="8" y="32" width="14" height="11"/></g><g fill="#111" opacity=".15"><rect x="8" y="6" width="14" height="11"/><rect x="24" y="6" width="14" height="11"/><rect x="24" y="19" width="14" height="11"/><rect x="8" y="19" width="14" height="11"/><rect x="24" y="32" width="14" height="11"/></g></svg>JIA</div>
  <div class="avail"><i></i>Malang, ID</div>
  <h1><span>Aplikasi web</span><span>yang dipakai</span><span class="o">sungguhan.</span></h1>
  <div class="sub"><b></b>Web Developer · aplikasi web, UI/UX, web 3D</div>
  <div class="url">jiaporto.pages.dev</div>
</body></html>`, { waitUntil: 'networkidle' });
  await og.evaluate(() => document.fonts.ready);
  await og.screenshot({ path: path.join(root, 'og-image.png') });
  await browser.close();
  console.log('og-image.png ditulis');
})();
