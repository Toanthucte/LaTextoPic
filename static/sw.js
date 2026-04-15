// LƯU Ý QUAN TRỌNG: Khi Push code lên GitHub cho PWA, NGAY LẬP TỨC phải CẬP NHẬT phiên bản CACHE_NAME này!
const CACHE_NAME = 'latextopic-v1.0.1'

// Các file cần lưu cache (offline)
const urlsToCache = ['./', 'manifest.json', 'icon.png']

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('Opened cache')
      return cache.addAll(urlsToCache)
    }),
  )
  // Ép Service Worker mới hoạt động ngay (skip waiting)
  self.skipWaiting()
})

self.addEventListener('activate', (event) => {
  const cacheWhitelist = [CACHE_NAME]
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheWhitelist.indexOf(cacheName) === -1) {
            // Xoá cache cũ không hợp lệ
            return caches.delete(cacheName)
          }
        }),
      )
    }),
  )
  self.clients.claim()
})

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      // TÌm thấy trong cache thì trả về
      if (response) {
        return response
      }
      return fetch(event.request)
    }),
  )
})
