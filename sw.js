// Service worker minimal: syarat tombol "Install app" di Chrome.
// Halaman selalu diambil dari jaringan; kalau offline, pakai salinan beranda/galeri yang tersimpan.
const CACHE = 'jia-v2';
// Cloudflare Pages menyajikan /gallery.html sebagai /gallery.
const OFFLINE = ['/', '/gallery'];
self.addEventListener('install', e => {
  // Tiap halaman disimpan sendiri-sendiri: satu yang gagal tidak membatalkan pemasangan.
  e.waitUntil(caches.open(CACHE)
    .then(c => Promise.all(OFFLINE.map(u => c.add(u).catch(() => {}))))
    .then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  if (e.request.mode !== 'navigate') return;
  const path = new URL(e.request.url).pathname.replace(/\.html$/, '').replace(/\/index$/, '/');
  e.respondWith(fetch(e.request).catch(async () =>
    (await caches.match(path)) || (await caches.match('/'))));
});
