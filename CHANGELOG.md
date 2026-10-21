# Changelog

## 4.3.0 — 21/10/2026

- Tre pagine-guida per Google: motozappa, robot tagliaerba, irrigazione a goccia, con barra fissa "Vedi su AgriEuro" e link ai 4 negozi.
- Guide generate da `strumenti/genera_guide.py` (testi in un unico punto), che scrive anche `sitemap.xml` e `robots.txt`.
- Negozi e link affiliati spostati in `negozi.js`, condiviso da home e guide.
- Home: link "Leggi la guida" nei consigli, meta tag per la condivisione (Open Graph) e indirizzo canonico.
- Test: 68 verifiche; la verifica online controlla anche guide, sitemap e robots.

## 4.2.1 — 21/10/2026

- Corretta la ricerca AgriEuro: il vecchio indirizzo dava errore 404 (trovato dalla verifica online). Ora usa `/search/<parole>`.
- Riquadro Decespugliatori: inquadratura della foto spostata sul soggetto.

## 4.2.0 — 21/10/2026

- Controlli automatici su GitHub Actions: test a ogni modifica, verifica del sito online dopo ogni pubblicazione e ogni mattina, schermate con le foto vere salvate nel ramo `controlli`.
- Nuovo `tests/verifica_online.py`; `tests/test_sito.py` può provare il sito pubblicato (`SITO_URL`).

## 4.1.0 — 21/10/2026 (prima pubblicazione della nuova grafica)

- Telefono: la ricerca resta fissa in alto scorrendo, il logo scorre via e lascia più spazio.
- Tocchi immediati: niente ritardo né riquadro grigio al tocco, effetto di pressione su reparti, lavori del mese e negozi.
- Pannello negozi più rapido ad aprirsi e chiudibile trascinandolo verso il basso.
- Tutti i pulsanti alti almeno 48 px; effetti al passaggio del mouse solo su computer.
- Test: 43 verifiche, incluse altezza dei pulsanti e trascinamento del pannello.

## 4.0.0 — 21/10/2026

- Nuova palette "melanzana e zucca": viola melanzana per testata e blocchi, arancio del logo per le azioni, verde lattuga per i dettagli. Lo stile bianco e nero della 3.0.0 è stato scartato.
- Font Bricolage Grotesque (variabile, con dimensione ottica) al posto di Archivo.
- Apertura del mese su fondo viola con bollino del mese e lavori collegati scorrevoli.
- Reparti a mosaico di foto grandi; consigli in schede bianche; negozi in un blocco viola.
- Contenuti, link e calendario invariati rispetto alla 3.0.0.

## 3.0.0 — 21/10/2026

- Nuovo stile negozio: fondo bianco, nero e arancio del logo, niente più verde di fondo.
- Titoli in Archivo stretto (stile volantino), cartellini gialli tipo vivaio su reparti e mese.
- Ricerca sempre in alto: mentre scrivi compare il menu con i 4 negozi; Invio cerca su AgriEuro.
- In apertura il lavoro del mese, con calendario dell'orto completo per i 12 mesi e 3 lavori collegati.
- Nuove sezioni: "Prima di comprare" (consigli pratici) e "Dove cerchiamo" (a cosa serve ogni negozio).
- Nuove foto Unsplash verificate: aglio (Colin Watts), fagioli (Maddi Bazzocco), carriola (Annie Spratt).
- Test aggiornati: 39 verifiche, incluso il controllo dei 12 mesi.

## 2.0.0 — 21/10/2026

- Nuova grafica in stile app: fondo verde bosco, foto reali (Unsplash) al posto delle icone disegnate.
- Ricerca rapida verso AgriEuro, Amazon, ManoMano ed eBay, con scelta del negozio.
- Suggerimenti di ricerca che cambiano ogni mese.
- Categorie a foto con pannello di scelta del negozio; per AgriEuro si apre direttamente la pagina categoria quando esiste.
- Codici affiliato vuoti di default: niente più segnaposto tipo `TUO_TAG_AMAZON` finiti nei link.
- Rimossi prezzi, stelle e numeri di recensioni inventati e il pulsante "chat con l'esperto" non ancora funzionante.
- Rimosso Leroy Merlin (non tra i programmi scelti).
- Font incorporati nel sito, senza chiamate a Google Fonts.
- File principale rinominato `index.html` (minuscolo): con `Index.html` Netlify non trovava la pagina iniziale.
- Logo adattato al fondo scuro (scritta chiara, cotiledoni verde più luminoso); forma invariata.
- Aggiunti test automatici, README e questo changelog.

## 1.0.0 — 20/10/2026

- Prima pubblicazione (`Index.html`, grafica chiara).
