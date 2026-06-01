const APP_SHELL_CACHE = "toolspaedeia-shell-v4";
const PRIVATE_CONTENT_CACHE = "toolspaedeia-private-content-v3";

const SHELL_URLS = [
    "/",
    "/courses/purchased-courses/",
    "/courses/published-courses/"
];

self.addEventListener("install", (event) => {
    event.waitUntil(
        caches.open(APP_SHELL_CACHE).then((cache) => cache.addAll(SHELL_URLS))
    );
    self.skipWaiting();
});

self.addEventListener("activate", (event) => {
    event.waitUntil(
        caches.keys().then((keys) =>
            Promise.all(
                keys
                    .filter((key) => ![APP_SHELL_CACHE, PRIVATE_CONTENT_CACHE].includes(key))
                    .map((key) => caches.delete(key))
            )
        )
    );
    self.clients.claim();
});

self.addEventListener("message", (event) => {
    const data = event.data || {};

    if (data.type === "CLEAR_PRIVATE_CACHE") {
        event.waitUntil(caches.delete(PRIVATE_CONTENT_CACHE));
        return;
    }

    if (data.type !== "WARM_PURCHASED_CONTENT") {
        return;
    }

    const urls = Array.isArray(data.urls) ? data.urls : [];
    if (!urls.length) {
        return;
    }

    event.waitUntil(
        caches.open(PRIVATE_CONTENT_CACHE).then(async (cache) => {
            for (const url of urls) {
                try {
                    const response = await fetch(url, {
                        credentials: "include",
                        cache: "no-cache"
                    });

                    if (response.ok) {
                        await cache.put(new URL(url, self.location.origin).pathname, response.clone());
                    }
                } catch (_error) {
                }
            }
        })
    );
});

function isSensitiveMutationPath(pathname) {
    return pathname.includes("/enrollment-dialog/")
        || pathname.includes("/stripe/webhook/")
        || pathname.includes("/mark-complete/")
        || pathname.includes("/attempt/")
        || pathname.includes("/logout/");
}

function isShellPage(pathname) {
    return SHELL_URLS.includes(pathname);
}

function isCourseOrModulePage(pathname) {
    const coursePattern = /^\/courses\/\d+\/$/;
    const modulePattern = /^\/courses\/\d+\/modules\/\d+\/$/;
    return coursePattern.test(pathname) || modulePattern.test(pathname);
}

self.addEventListener("fetch", (event) => {
    const request = event.request;

    if (request.method !== "GET") {
        return;
    }

    const url = new URL(request.url);

    if (isSensitiveMutationPath(url.pathname)) {
        return;
    }

    if (url.pathname.startsWith("/static/") || url.pathname.startsWith("/media/")) {
        event.respondWith(
            caches.match(request).then((cachedResponse) => {
                if (cachedResponse) {
                    return cachedResponse;
                }

                return fetch(request).then((networkResponse) => {
                    if (networkResponse.ok) {
                        const responseToCache = networkResponse.clone();
                        caches.open(APP_SHELL_CACHE).then((cache) => cache.put(request, responseToCache));
                    }
                    return networkResponse;
                });
            })
        );
        return;
    }

    if (isShellPage(url.pathname)) {
        event.respondWith(
            fetch(request)
                .then((networkResponse) => {
                    if (networkResponse.ok) {
                        const responseToCache = networkResponse.clone();
                        caches.open(APP_SHELL_CACHE).then((cache) => cache.put(url.pathname, responseToCache));
                    }
                    return networkResponse;
                })
                .catch(async () => {
                    const cache = await caches.open(APP_SHELL_CACHE);
                    const cachedResponse = await cache.match(url.pathname, { ignoreVary: true });
                    if (cachedResponse) {
                        return cachedResponse;
                    }

                    return new Response(
                        "<h1>Offline</h1><p>Page is not cached yet. Open it once while online.</p>",
                        {
                            headers: { "Content-Type": "text/html; charset=utf-8" },
                            status: 503,
                        }
                    );
                })
        );
        return;
    }

    if (isCourseOrModulePage(url.pathname)) {
        event.respondWith(
            fetch(request)
                .then((networkResponse) => {
                    if (networkResponse.ok) {
                        const responseToCache = networkResponse.clone();
                        caches
                            .open(PRIVATE_CONTENT_CACHE)
                            .then((cache) => cache.put(url.pathname, responseToCache));
                    }
                    return networkResponse;
                })
                .catch(async () => {
                    const cache = await caches.open(PRIVATE_CONTENT_CACHE);
                    const cachedResponse = await cache.match(url.pathname, { ignoreVary: true });
                    if (cachedResponse) {
                        return cachedResponse;
                    }

                    return new Response(
                        "<h1>Offline</h1><p>This page is not available offline yet. Open it once while online.</p>",
                        {
                            headers: { "Content-Type": "text/html; charset=utf-8" },
                            status: 503,
                        }
                    );
                })
        );
    }
});
