/* OrtoCasa Help — service worker: rende il sito installabile e leggibile anche senza rete.
   Pagine: prima la rete (sempre aggiornate), se manca la rete l'ultima copia salvata.
   CSS, JS, font e icone: copia salvata subito, aggiornata in sottofondo.
   Le richieste verso altri siti (foto Unsplash, negozi) non passano di qui. */
var VERSIONE = "ortocasa-v1";
var DI_BASE = ["/", "/guide/", "/fonts.css", "/guide/guida.css", "/negozi.js", "/guide/guida.js", "/app.js", "/icone/icona-192.png"];

self.addEventListener("install", function (e) {
  e.waitUntil(caches.open(VERSIONE).then(function (c) { return c.addAll(DI_BASE); }).then(function () { return self.skipWaiting(); }));
});

self.addEventListener("activate", function (e) {
  e.waitUntil(caches.keys().then(function (nomi) {
    return Promise.all(nomi.filter(function (n) { return n !== VERSIONE; }).map(function (n) { return caches.delete(n); }));
  }).then(function () { return self.clients.claim(); }));
});

self.addEventListener("fetch", function (e) {
  var req = e.request;
  if (req.method !== "GET" || new URL(req.url).origin !== self.location.origin) return;
  if (req.mode === "navigate") {
    e.respondWith(fetch(req).then(function (r) {
      var copia = r.clone();
      caches.open(VERSIONE).then(function (c) { c.put(req, copia); });
      return r;
    }).catch(function () {
      return caches.match(req).then(function (r) { return r || caches.match("/"); });
    }));
    return;
  }
  e.respondWith(caches.match(req).then(function (salvata) {
    var rete = fetch(req).then(function (r) {
      if (r.ok) { var copia = r.clone(); caches.open(VERSIONE).then(function (c) { c.put(req, copia); }); }
      return r;
    });
    return salvata || rete;
  }));
});
