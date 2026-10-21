# OrtoCasa Help — sito

Sito statico di ricerca rapida per orto e giardino: l'utente scrive cosa cerca e viene portato ai risultati di AgriEuro, Amazon, ManoMano o eBay tramite link di affiliazione.

## File

| File | Cosa contiene |
|---|---|
| `index.html` | Pagina completa: stile, contenuti e script. In cima allo script c'è la **configurazione** (codici affiliato, suggerimenti del mese, categorie). |
| `fonts.css` | Font Sora e Comfortaa incorporati (licenza SIL OFL 1.1, da @fontsource 5.3.0). Nessuna chiamata a Google Fonts. |
| `tests/test_sito.py` | Test automatici end-to-end (Playwright). |
| `CHANGELOG.md` | Storico delle versioni. |

## Inserire i codici affiliato

Nel blocco `AFFILIATI` in `index.html`:

- **Amazon**: `tag` (es. `ortocasa-21`)
- **eBay Partner Network**: `campid` (ID campagna; i parametri Italia `mkrid=724-53478-19255-0` sono già impostati)
- **ManoMano via Awin**: `awinMid` (ID inserzionista ManoMano su Awin) e `awinAffId` (il proprio ID publisher)
- **AgriEuro**: `codice` e `parametro`, da confermare con il formato fornito dopo l'approvazione. Anche l'indirizzo di ricerca libera AgriEuro (`advanced_search_result.php?keywords=`) è da confermare; le pagine categoria AgriEuro usate sono state verificate.

Con un campo vuoto il link funziona comunque, senza tracciamento.

## Provare in locale

Basta aprire `index.html` nel browser. Test automatici:

```
pip install playwright && python -m playwright install chromium
python3 tests/test_sito.py cartella-schermate   # la cartella è facoltativa
```

## Pubblicazione

Netlify pubblica in automatico il ramo `main` del repository `ortocasahelp/ortocasahelp-sito`. Ogni pull request genera un'anteprima Netlify separata: si controlla lì prima di unire su `main`.

**Rollback**: da Netlify → Deploys → scegliere il deploy precedente → "Publish deploy", oppure annullare la pull request su GitHub (Revert).

## Foto

Tutte da Unsplash, licenza Unsplash (uso commerciale gratuito), verificate una per una il 21/10/2026. Autori citati nel piè di pagina.
