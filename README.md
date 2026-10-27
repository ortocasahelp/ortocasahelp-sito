# OrtoCasa Help — sito

Sito online: **[OrtoCasa Help](https://ortocasahelp.netlify.app/)** · Guide: [motozappa](https://ortocasahelp.netlify.app/guide/motozappa/), [robot tagliaerba](https://ortocasahelp.netlify.app/guide/robot-tagliaerba/), [irrigazione a goccia](https://ortocasahelp.netlify.app/guide/irrigazione-a-goccia/), [decespugliatore](https://ortocasahelp.netlify.app/guide/decespugliatore/), [biotrituratore](https://ortocasahelp.netlify.app/guide/biotrituratore/), [serra da giardino](https://ortocasahelp.netlify.app/guide/serra-da-giardino/)

Sito statico di ricerca rapida per orto e giardino: l'utente scrive cosa cerca e viene portato ai risultati di AgriEuro, Amazon, ManoMano o eBay tramite link di affiliazione.

## File

| File | Cosa contiene |
|---|---|
| `index.html` | Pagina completa: stile, contenuti e script. In cima allo script c'è la **configurazione**: codici affiliato (`AFFILIATI`), foto (`F`), calendario dell'orto (`MESI`, un lavoro principale + 3 lavori per mese) e reparti (`REPARTI`). |
| `negozi.js` | Codici affiliato (`AFFILIATI`) e costruzione dei link ai negozi, condiviso da home e guide. **Qui si inseriscono i codici.** |
| `guide/` | Pagine-guida (`guide/<nome>/index.html`), stile `guida.css`, pulsanti `guida.js`. Non modificarle a mano: si rigenerano. |
| `strumenti/genera_guide.py` | Testi delle guide; rilanciarlo rigenera guide, `sitemap.xml` e `robots.txt`. |
| `fonts.css` | Font Bricolage Grotesque (variabile) e Comfortaa incorporati (licenza SIL OFL 1.1, da @fontsource 5.3.0). Nessuna chiamata a Google Fonts. |
| `tests/test_sito.py` | Test automatici end-to-end (Playwright); con `SITO_URL` prova il sito pubblicato. |
| `tests/verifica_online.py` | Verifica del sito pubblicato, delle foto e dei link ai negozi (solo libreria standard). |
| `.github/workflows/controlli.yml` | Controlli automatici su GitHub. |
| `CHANGELOG.md` | Storico delle versioni. |

## Inserire i codici affiliato

Nel blocco `AFFILIATI` in `negozi.js`:

- **Amazon**: `tag` (es. `ortocasa-21`)
- **eBay Partner Network**: `campid` (ID campagna; i parametri Italia `mkrid=724-53478-19255-0` sono già impostati)
- **ManoMano via Awin**: `awinMid` (ID inserzionista ManoMano su Awin) e `awinAffId` (il proprio ID publisher)
- **AgriEuro**: `codice` e `parametro`, da confermare con il formato fornito dopo l'approvazione. La ricerca AgriEuro usa `agrieuro.com/search/<parole>`; le pagine categoria AgriEuro sono verificate dai controlli automatici.

Con un campo vuoto il link funziona comunque, senza tracciamento.

## Provare in locale

Basta aprire `index.html` nel browser. Test automatici:

```
pip install playwright && python -m playwright install chromium
python3 tests/test_sito.py cartella-schermate   # la cartella è facoltativa
```

## Controlli automatici (GitHub Actions)

File: `.github/workflows/controlli.yml`.

- **Test della pagina**: a ogni proposta di modifica (pull request) e a ogni pubblicazione. Una proposta si unisce a `main` solo se i test passano.
- **Verifica del sito online**: dopo ogni pubblicazione su `main`, ogni mattina alle 05:17 UTC e a richiesta (Actions → Controlli → Run workflow). Controlla con `tests/verifica_online.py` che la home online sia identica a `index.html`, che font, foto e pagine AgriEuro rispondano e che le ricerche nei negozi funzionino (queste ultime come avvisi). Poi ripete i test sul sito vero e scatta le schermate con le foto.
- **IndexNow**: dopo ogni pubblicazione verificata, `strumenti/indexnow.py` segnala le pagine della sitemap a Bing e agli altri motori aderenti. La chiave è il file `<32 caratteri>.txt` nella radice (pubblica per definizione).
- Gli esiti (`esito.txt`, `verifica-online.md`, `test-online.txt`, `schermate/*.png`) vengono salvati nel ramo **`controlli`**, sovrascritto a ogni esecuzione.

## Social automatici (senza computer acceso)

- **Pinterest**: il sito pubblica `feed.xml` (RSS delle guide, generato da `strumenti/genera_guide.py`). Nelle impostazioni dell'account aziendale Pinterest → *Pubblicazione automatica / RSS* si aggiunge una volta `https://ortocasahelp.netlify.app/feed.xml`: da lì Pinterest crea da solo un pin per ogni guida nuova (fino a 200 al giorno, dentro 24-48 ore).
- **Facebook e Instagram**: workflow `.github/workflows/social.yml`, martedì e sabato. Pubblica con le API ufficiali di Meta il primo post pronto della coda `coda.json` nel ramo `social` (un post per giro: Pagina Facebook, Instagram e storia) e scrive `stato.json` ed `esito.md` nello stesso ramo.
  - Segreti del repository da impostare una volta: `META_PAGE_ID`, `META_PAGE_TOKEN` (token di Pagina senza scadenza, permessi `pages_manage_posts`, `instagram_basic`, `instagram_content_publish`), `META_IG_ID`. Senza segreti non pubblica niente e lo scrive nell'esito.
  - Interruttore: `config.json` nel ramo `social`. Con `{"pubblica": false}` (o senza file) non pubblica niente e i post restano in coda; si mette `true` quando si decide di rendere visibili i social.
  - Regole controllate dallo script: testo, link e foto obbligatori; link fuori dal sito solo con `#ADV`; massimo 2000 caratteri.
  - Test: `python3 tests/test_social.py` (le chiamate a Meta sono simulate).
- I gruppi Facebook non si possono automatizzare: Meta ha tolto le API dei gruppi nell'aprile 2024.

## App installabile

- `manifest.webmanifest`, icone in `icone/` (sorgente del logo: `icone/logo.svg`), service worker `sw.js` registrato da `app.js`. Dal telefono: menu del browser → "Aggiungi a schermata Home".
- Il service worker non salva le richieste verso altri siti (foto, negozi). Se si cambia la lista dei file di base in `sw.js`, aumentare `VERSIONE`.
- Test: `python3 tests/test_app.py`.

## Pubblicazione

Netlify pubblica in automatico il ramo `main` del repository `ortocasahelp/ortocasahelp-sito`. Ogni pull request genera un'anteprima Netlify separata: si controlla lì prima di unire su `main`.

**Rollback**: da Netlify → Deploys → scegliere il deploy precedente → "Publish deploy", oppure annullare la pull request su GitHub (Revert).

## Foto

Tutte da Unsplash, licenza Unsplash (uso commerciale gratuito), verificate una per una il 21/10/2026. Autori citati nel piè di pagina.
