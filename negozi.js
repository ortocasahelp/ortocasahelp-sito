/* OrtoCasa Help — negozi e link affiliati, condiviso da home e guide.
   CONFIGURAZIONE: unico punto da modificare quando arrivano i codici affiliato. */

var AFFILIATI = {
  agrieuro: { nome: "AgriEuro", nota: "Specialista orto e giardino", codice: "", parametro: "" },
  amazon:   { nome: "Amazon",   nota: "Consegna veloce",             tag: "" },
  manomano: { nome: "ManoMano", nota: "Fai da te e giardino",        awinMid: "17962", awinAffId: "3130993" },
  ebay:     { nome: "eBay",     nota: "Usato e ricambi",             campid: "5339228940" }
};
var ORDINE_NEGOZI = ["agrieuro", "amazon", "manomano", "ebay"];

/* Pagine categoria AgriEuro verificate dai controlli automatici. */
var AE = {
  motozappe:"https://www.agrieuro.com/motozappe-c-22.html", irrigazione:"https://www.agrieuro.com/irrigazione-g-14.html",
  robot:"https://www.agrieuro.com/robot-tagliaerba-c-59.html", decespugliatori:"https://www.agrieuro.com/decespugliatori-c-3.html"
};

/* ---------- Costruzione dei link (funzioni pure, testate) ---------- */
function pulisci(testo){
  return String(testo == null ? "" : testo).replace(/\s+/g, " ").trim().slice(0, 80);
}
function linkNegozio(negozio, testo){
  var q = pulisci(testo);
  if (!q) return null;
  var e = encodeURIComponent(q);
  var url;
  switch (negozio) {
    case "agrieuro":
      // Formato verificato sulle pagine di ricerca indicizzate di AgriEuro (es. /search/zappa).
      url = "https://www.agrieuro.com/search/" + e;
      if (AFFILIATI.agrieuro.codice && AFFILIATI.agrieuro.parametro)
        url += "?" + AFFILIATI.agrieuro.parametro + "=" + encodeURIComponent(AFFILIATI.agrieuro.codice);
      return url;
    case "amazon":
      url = "https://www.amazon.it/s?k=" + e;
      if (AFFILIATI.amazon.tag) url += "&tag=" + encodeURIComponent(AFFILIATI.amazon.tag);
      return url;
    case "manomano":
      url = "https://www.manomano.it/cat/" + q.split(" ").map(encodeURIComponent).join("+");
      if (AFFILIATI.manomano.awinMid && AFFILIATI.manomano.awinAffId)
        url = "https://www.awin1.com/cread.php?awinmid=" + encodeURIComponent(AFFILIATI.manomano.awinMid) +
              "&awinaffid=" + encodeURIComponent(AFFILIATI.manomano.awinAffId) + "&ued=" + encodeURIComponent(url);
      return url;
    case "ebay":
      url = "https://www.ebay.it/sch/i.html?_nkw=" + e;
      if (AFFILIATI.ebay.campid)
        url += "&mkevt=1&mkcid=1&mkrid=724-53478-19255-0&campid=" + encodeURIComponent(AFFILIATI.ebay.campid) + "&toolid=10001";
      return url;
    default:
      return null;
  }
}
function linkCategoria(negozio, cat){
  if (negozio === "agrieuro" && cat.agrieuro) {
    var u = cat.agrieuro;
    if (AFFILIATI.agrieuro.codice && AFFILIATI.agrieuro.parametro)
      u += "?" + AFFILIATI.agrieuro.parametro + "=" + encodeURIComponent(AFFILIATI.agrieuro.codice);
    return u;
  }
  return linkNegozio(negozio, cat.q);
}
