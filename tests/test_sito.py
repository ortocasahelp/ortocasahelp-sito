"""Test end-to-end della home OrtoCasa Help (Playwright, Chromium headless).

Uso:  python3 tests/test_sito.py [cartella-schermate]
Le immagini esterne (Unsplash) vengono bloccate di proposito: il test verifica
logica e layout, non la disponibilità di servizi terzi.
"""
import pathlib
import sys
from urllib.parse import urlparse, parse_qs

from playwright.sync_api import sync_playwright

RADICE = pathlib.Path(__file__).resolve().parent.parent
PAGINA = (RADICE / "index.html").as_uri()
SCHERMATE = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else None

esiti = []


def verifica(nome, condizione, dettaglio=""):
    esiti.append((nome, bool(condizione), dettaglio))


def blocca_esterni(route):
    if route.request.url.startswith("file://"):
        return route.continue_()
    return route.abort()


with sync_playwright() as p:
    browser = p.chromium.launch()
    ctx = browser.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
    ctx.route("**/*", blocca_esterni)
    pagina = ctx.new_page()
    errori_js = []
    pagina.on("pageerror", lambda e: errori_js.append(str(e)))
    pagina.on("console", lambda m: m.type == "error" and "ERR_FAILED" not in m.text and errori_js.append(m.text))
    pagina.goto(PAGINA)
    pagina.wait_for_load_state("load")

    # 1. Funzione pura linkNegozio, senza codici affiliato
    casi = pagina.evaluate("""() => ({
        agrieuro: linkNegozio('agrieuro','motozappa elettrica'),
        amazon:   linkNegozio('amazon','motozappa elettrica'),
        manomano: linkNegozio('manomano','motozappa elettrica'),
        ebay:     linkNegozio('ebay','motozappa elettrica'),
        vuoto:    linkNegozio('amazon','   '),
        nullo:    linkNegozio('amazon', null),
        ignoto:   linkNegozio('leroy','x'),
        speciali: linkNegozio('amazon','semi & "fave" <b>#1'),
        lungo:    linkNegozio('ebay','a'.repeat(200)),
    })""")
    verifica("AgriEuro: ricerca senza codice", casi["agrieuro"] == "https://www.agrieuro.com/advanced_search_result.php?keywords=motozappa%20elettrica", casi["agrieuro"])
    verifica("Amazon: nessun tag finto", casi["amazon"] == "https://www.amazon.it/s?k=motozappa%20elettrica", casi["amazon"])
    verifica("ManoMano: formato /cat/a+b", casi["manomano"] == "https://www.manomano.it/cat/motozappa+elettrica", casi["manomano"])
    verifica("eBay: ricerca senza parametri EPN", casi["ebay"] == "https://www.ebay.it/sch/i.html?_nkw=motozappa%20elettrica", casi["ebay"])
    verifica("Testo vuoto -> nessun link", casi["vuoto"] is None and casi["nullo"] is None)
    verifica("Negozio sconosciuto -> nessun link", casi["ignoto"] is None)
    q = parse_qs(urlparse(casi["speciali"]).query)
    verifica("Caratteri speciali codificati", q.get("k") == ['semi & "fave" <b>#1'] and "<" not in casi["speciali"], casi["speciali"])
    verifica("Testo troncato a 80 caratteri", parse_qs(urlparse(casi["lungo"]).query)["_nkw"] == ["a" * 80])

    # 2. Con codici affiliato impostati
    con = pagina.evaluate("""() => {
        AFFILIATI.amazon.tag='prova-21'; AFFILIATI.ebay.campid='5338000000';
        AFFILIATI.manomano.awinMid='1234'; AFFILIATI.manomano.awinAffId='999';
        AFFILIATI.agrieuro.codice='abc'; AFFILIATI.agrieuro.parametro='aff';
        const r = {
          amazon: linkNegozio('amazon','vasi'), ebay: linkNegozio('ebay','vasi'),
          manomano: linkNegozio('manomano','vasi grandi'), agrieuro: linkNegozio('agrieuro','vasi'),
          cat: linkCategoria('agrieuro', CATEGORIE[0]), catAmazon: linkCategoria('amazon', CATEGORIE[4])
        };
        AFFILIATI.amazon.tag=''; AFFILIATI.ebay.campid=''; AFFILIATI.manomano.awinMid=''; AFFILIATI.manomano.awinAffId='';
        AFFILIATI.agrieuro.codice=''; AFFILIATI.agrieuro.parametro='';
        return r;
    }""")
    verifica("Amazon: tag aggiunto", parse_qs(urlparse(con["amazon"]).query).get("tag") == ["prova-21"], con["amazon"])
    eq = parse_qs(urlparse(con["ebay"]).query)
    verifica("eBay: parametri EPN Italia", eq.get("mkrid") == ["724-53478-19255-0"] and eq.get("campid") == ["5338000000"] and eq.get("mkevt") == ["1"], con["ebay"])
    mq = parse_qs(urlparse(con["manomano"]).query)
    verifica("ManoMano: avvolto da Awin", con["manomano"].startswith("https://www.awin1.com/cread.php") and mq.get("ued") == ["https://www.manomano.it/cat/vasi+grandi"], con["manomano"])
    verifica("AgriEuro categoria con codice", con["cat"] == "https://www.agrieuro.com/motozappe-c-22.html?aff=abc", con["cat"])
    verifica("Categoria senza pagina AgriEuro -> ricerca", con["catAmazon"].startswith("https://www.amazon.it/s?k=serra"), con["catAmazon"])

    # 3. Modulo: invio a vuoto mostra l'errore e non apre nulla
    aperte = []
    ctx.on("page", lambda pg: aperte.append(pg.url))
    pagina.click("#bottone-cerca")
    verifica("Invio vuoto: messaggio d'errore visibile", pagina.is_visible("#errore-ricerca"))
    verifica("Invio vuoto: campo marcato non valido", pagina.get_attribute("#cosa", "aria-invalid") == "true")
    verifica("Invio vuoto: nessuna scheda aperta", len(aperte) == 0)

    # 4. Cambio negozio aggiorna il bottone; invio reale apre la scheda giusta
    pagina.click("label[for=n-ebay]")
    verifica("Bottone segue il negozio scelto", pagina.inner_text("#bottone-cerca") == "Cerca su eBay")
    verifica("Errore sparisce scrivendo", (pagina.fill("#cosa", "tubo gocciolante") or True) and not pagina.is_visible("#errore-ricerca"))
    richieste = []
    ctx.on("request", lambda r: r.is_navigation_request() and richieste.append(r.url))
    with ctx.expect_page() as nuova:
        pagina.press("#cosa", "Enter")
    nuova.value.wait_for_load_state()
    url_aperto = next((u for u in richieste if "ebay.it" in u), "")
    verifica("Invio con Enter apre eBay con la ricerca", url_aperto == "https://www.ebay.it/sch/i.html?_nkw=tubo%20gocciolante", url_aperto or str(richieste))
    nuova.value.close()

    # 5. Suggerimenti del mese
    n_sugg = pagina.locator("#suggerimenti button").count()
    verifica("Suggerimenti stagionali presenti", n_sugg == 4, str(n_sugg))
    primo = pagina.locator("#suggerimenti button").first.inner_text()
    pagina.locator("#suggerimenti button").first.click()
    verifica("Suggerimento riempie il campo", pagina.input_value("#cosa") == primo, primo)

    # 6. Categorie e pannello
    n_cat = pagina.locator(".tessera").count()
    verifica("9 categorie con foto", n_cat == 9 and pagina.locator(".tessera img").count() == 9)
    alt_vuoti = pagina.evaluate("() => [...document.querySelectorAll('.tessera img')].filter(i => !i.alt).length")
    verifica("Tutte le foto hanno testo alternativo", alt_vuoti == 0)
    verifica("Nessuna icona disegnata nelle categorie", pagina.locator(".tessera svg").count() == 0)

    if SCHERMATE:
        SCHERMATE.mkdir(parents=True, exist_ok=True)
        pagina.evaluate("window.scrollTo(0,0)")
        pagina.fill("#cosa", "")
        pagina.click("label[for=n-agrieuro]")
        pagina.screenshot(path=str(SCHERMATE / "1-telefono-inizio.png"))
        pagina.screenshot(path=str(SCHERMATE / "2-telefono-intera.png"), full_page=True)

    pagina.locator(".tessera").nth(2).click()
    verifica("Pannello si apre", pagina.is_visible("#pannello"))
    link = pagina.eval_on_selector_all("#pannello-link a", "els => els.map(a => [a.textContent, a.href, a.rel, a.target])")
    verifica("Pannello: 4 negozi", [l[0] for l in link] == ["AgriEuro", "Amazon", "ManoMano", "eBay"], str(link))
    verifica("Pannello: AgriEuro va alla categoria robot", link[0][1] == "https://www.agrieuro.com/robot-tagliaerba-c-59.html", link[0][1])
    verifica("Pannello: link sponsored e in nuova scheda", all(l[2] == "sponsored noopener" and l[3] == "_blank" for l in link))
    if SCHERMATE:
        pagina.screenshot(path=str(SCHERMATE / "3-telefono-pannello.png"))
    pagina.keyboard.press("Escape")
    verifica("Pannello si chiude con Esc", not pagina.is_visible("#pannello"))

    # 7. Nessuno scorrimento orizzontale su telefono
    largo = pagina.evaluate("() => document.documentElement.scrollWidth <= window.innerWidth")
    verifica("Nessuno scorrimento orizzontale (390 px)", largo)

    # 8. Desktop
    desk = browser.new_context(viewport={"width": 1280, "height": 900})
    desk.route("**/*", blocca_esterni)
    pd = desk.new_page()
    pd.on("pageerror", lambda e: errori_js.append(str(e)))
    pd.goto(PAGINA)
    verifica("Desktop: nessuno scorrimento orizzontale", pd.evaluate("() => document.documentElement.scrollWidth <= window.innerWidth"))
    if SCHERMATE:
        pd.screenshot(path=str(SCHERMATE / "4-computer.png"), full_page=True)

    verifica("Nessun errore JavaScript", not errori_js, "; ".join(errori_js))
    browser.close()

falliti = [e for e in esiti if not e[1]]
for nome, ok, det in esiti:
    print(("OK   " if ok else "FAIL ") + nome + ("" if ok or not det else "  -> " + det))
print(f"\n{len(esiti) - len(falliti)}/{len(esiti)} verifiche superate")
sys.exit(1 if falliti else 0)
