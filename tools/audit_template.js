// Audit + tangkapan thumbnail semua template di galeri.
// Pakai: node tools/audit_template.js [http://localhost:5177] [--shot] [slug ...]
//   --shot  simpan tangkapan 1440x900 ke tools/.shot/<slug>.png (diubah ke webp oleh buat_thumbnail.py)
// Laporan per template: galat konsol/halaman, luber horizontal di HP 390 px, elemen bertulisan berfon mono.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const base = (args.find(a => a.startsWith('http')) || 'http://localhost:5177').replace(/\/$/, '');
const shot = args.includes('--shot');
const only = args.filter(a => !a.startsWith('http') && !a.startsWith('--'));
const src = fs.readFileSync(path.join(__dirname, '..', 'gallery.html'), 'utf8');
const rows = [...src.matchAll(/slug:"([^"]+)".*?path:"([^"]+)"/g)].map(m => ({ slug: m[1], path: m[2] }))
  .filter(r => !only.length || only.includes(r.slug));
const outDir = path.join(__dirname, '.shot');
if (shot) fs.mkdirSync(outDir, { recursive: true });

const MONO = /mono|consolas|courier|menlo|monaco/i;

(async () => {
  const browser = await chromium.launch({ args: ['--enable-unsafe-swiftshader', '--use-angle=swiftshader'] });
  const hasil = [];
  for (const r of rows) {
    const rep = { slug: r.slug, err: [], overflow: 0, mono: 0 };
    for (const vp of [{ width: 390, height: 844 }, { width: 1440, height: 900 }]) {
      const ctx = await browser.newContext({ viewport: vp, reducedMotion: 'no-preference' });
      const page = await ctx.newPage();
      page.on('pageerror', e => rep.err.push('page: ' + e.message.slice(0, 120)));
      page.on('console', m => { if (m.type() === 'error') rep.err.push('console: ' + m.text().slice(0, 120)); });
      try {
        await page.goto(`${base}/${r.path}`, { waitUntil: 'load', timeout: 30000 });
        await page.waitForTimeout(vp.width === 390 ? 600 : 1800);
        if (vp.width === 390) {
          rep.overflow = await page.evaluate(() => document.documentElement.scrollWidth - innerWidth);
          rep.mono = await page.evaluate(re => {
            const rx = new RegExp(re, 'i'); let n = 0;
            for (const el of document.querySelectorAll('body *')) {
              if (!el.childNodes.length || ![...el.childNodes].some(c => c.nodeType === 3 && c.textContent.trim())) continue;
              const ff = getComputedStyle(el).fontFamily.split(',')[0];
              if (rx.test(ff)) n++;
            }
            return n;
          }, MONO.source);
        } else if (shot) {
          await page.screenshot({ path: path.join(outDir, r.slug + '.png') });
        }
      } catch (e) { rep.err.push('goto: ' + e.message.slice(0, 120)); }
      await ctx.close();
    }
    rep.err = [...new Set(rep.err)];
    hasil.push(rep);
    const bad = rep.err.length || rep.overflow > 0 || rep.mono;
    console.log(`${bad ? 'X' : 'ok'} ${r.slug} luber=${rep.overflow} mono=${rep.mono} galat=${rep.err.length}${rep.err.length ? ' ' + rep.err[0] : ''}`);
  }
  fs.writeFileSync(path.join(__dirname, '.audit.json'), JSON.stringify(hasil, null, 1));
  const n = k => hasil.filter(k).length;
  console.log(`\nTOTAL ${hasil.length} · luber ${n(h => h.overflow > 0)} · mono ${n(h => h.mono)} · galat ${n(h => h.err.length)}`);
  await browser.close();
})();
