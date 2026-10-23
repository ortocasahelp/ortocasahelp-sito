# Changelog

## 4.6.0 — 26/10/2026

- Visibilità su Google: nuova pagina indice `/guide/` con tutte le guide (foto, titolo, riassunto, dati strutturati CollectionPage + ItemList), generata da `strumenti/genera_guide.py`.
- Nuova pagina `/chi-siamo/`: chi scrive, come nascono le guide, come si mantiene il sito (affiliazioni dichiarate), contatto. Dati strutturati AboutPage.
- Guide: briciole con link all'indice e dati strutturati BreadcrumbList insieme ad Article; data di aggiornamento 26/10/2026; comprende anche la guida serra da giardino (4.4.8).
- Home: dati strutturati WebSite + Organization (con il profilo Pinterest), pulsante "Tutte le guide" (prima la home collegava solo 3 guide su 5).
- Piè di pagina di home, guide, indice, chi siamo e privacy: link a Tutte le guide, Chi siamo, Privacy.
- Social senza computer: feed RSS `feed.xml` delle guide (per la pubblicazione automatica dei pin su Pinterest, con `<link rel="alternate">` nelle pagine) e workflow `Social` che pubblica su Pagina Facebook, Instagram e storie con le API ufficiali di Meta, leggendo la coda dal ramo `social`. Script `strumenti/social.py` con 16 test (`tests/test_social.py`).
- Sitemap con `/guide/` e `/chi-siamo/`; test: 111 verifiche (indice, chi siamo, dati strutturati, ogni indirizzo della sitemap ha la sua pagina); la verifica online controlla anche le due pagine nuove.

## 4.4.8 — 26/10/2026

- Nuova guida: serra da giardino (`/guide/serra-da-giardino/`), con la foto della serra già usata in home. Nessuna pagina categoria AgriEuro sicura: il pulsante AgriEuro apre la ricerca "serra da giardino". Aggiunta a sitemap, test e verifica online.

## 4.4.7 — 23/10/2026

- eBay Partner Network attivo: i link eBay di home e guide portano il codice della campagna OrtoCasaHelp (campid `5339228940`, parametri EPN Italia). Test aggiornati: i casi "senza codici" azzerano il campid solo durante la prova.

## 4.4.6 — 22/10/2026

- Nuova guida: biotrituratore (`/guide/biotrituratore/`), con pagina categoria AgriEuro verificata e foto di legno triturato (Declan Chidlow, Unsplash). Aggiunta a sitemap, test e verifica online; crediti aggiornati.

## 4.4.5 — 22/10/2026

- Motozappe: nuova foto con una motozappa vera (Iftekhar Sourav, Unsplash) al posto della foto di sola terra, in home e nella guida. Crediti aggiornati.

## 4.4.4 — 22/10/2026

- Pinterest: meta tag `p:domain_verify` nella home per verificare il sito sull'account aziendale OrtoCasa Help (da non rimuovere).

## 4.4.3 — 22/10/2026

- Google Search Console: file di verifica della proprietà `google323c386588effe2f.html` nella radice (da non rimuovere: serve a restare verificati). Controllato dai test locali e dalla verifica online.

## 4.4.2 — 21/10/2026

- Verifica online: attende che Netlify abbia pubblicato tutte le pagine controllate (guide, sitemap, script), non solo la home. Prima una modifica che non toccava `index.html` veniva controllata a pubblicazione non finita e dava falsi errori (successo con la 4.4.1).

## 4.4.1 — 21/10/2026

- Nuova guida: decespugliatore (`/guide/decespugliatore/`), con pagina categoria AgriEuro verificata. Aggiunta a sitemap, test e verifica online.

## 4.4.0 — 21/10/2026

- Pagina Privacy e cookie (`/privacy/`): titolare Stefano Ciceri, dati di navigazione Netlify, foto Unsplash, nessun cookie proprio, diritti GDPR. Collegata dal piè di pagina di home e guide e inserita nella sitemap.

## 4.3.2 — 21/10/2026

- Nuovo indirizzo del sito: https://ortocasahelp.netlify.app (prima lustrous-concha-651962.netlify.app). Aggiornati canonical, sitemap, robots, guide, IndexNow e controlli.

## 4.3.1 — 21/10/2026

- IndexNow: a ogni pubblicazione le pagine della sitemap vengono segnalate in automatico a Bing e agli altri motori aderenti, senza bisogno di account (`strumenti/indexnow.py`, chiave pubblica nella radice).

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
