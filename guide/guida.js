/* OrtoCasa Help — pagine-guida: crea i pulsanti dei negozi (usa negozi.js). */
(function(){
  var blocchi = document.querySelectorAll(".dove");
  blocchi.forEach(function(box){
    var voce = { q: box.dataset.q, agrieuro: box.dataset.agrieuro || "" };
    ORDINE_NEGOZI.forEach(function(n, i){
      var a = document.createElement("a");
      a.href = linkCategoria(n, voce);
      a.target = "_blank";
      a.rel = "sponsored noopener";
      if (i === 0) a.className = "primo";
      a.appendChild(document.createTextNode(AFFILIATI[n].nome));
      var s = document.createElement("span");
      s.textContent = AFFILIATI[n].nota;
      a.appendChild(s);
      box.appendChild(a);
    });
  });
  /* Barra in basso: il pulsante principale porta dritto ad AgriEuro */
  var primo = document.querySelector(".dove");
  var barra = document.getElementById("barra-agrieuro");
  if (primo && barra) {
    barra.href = linkCategoria("agrieuro", { q: primo.dataset.q, agrieuro: primo.dataset.agrieuro || "" });
    barra.target = "_blank";
    barra.rel = "sponsored noopener";
  }
})();
