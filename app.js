/* OrtoCasa Help — registra il service worker (sito installabile come app). Solo su https. */
if ("serviceWorker" in navigator && (location.protocol === "https:" || location.hostname === "localhost")) {
  window.addEventListener("load", function () {
    navigator.serviceWorker.register("/sw.js").catch(function (err) { console.warn("Service worker non registrato:", err); });
  });
}
