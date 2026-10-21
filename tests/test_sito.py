"""Test end-to-end della home OrtoCasa Help (Playwright, Chromium headless).

Uso:  python3 tests/test_sito.py [cartella-schermate] [cartella-foto-locali]
      SITO_URL=https://... python3 tests/test_sito.py [cartella-schermate]
      (con SITO_URL prova il sito pubblicato, con le foto vere; i negozi restano bloccati)
Senza la seconda cartella le immagini esterne (Unsplash) vengono bloccate:
il test verifica logica e layout, non la disponibilità di servizi terzi.
Con la seconda cartella, le foto vengono servite da file locali <id>.jpg
(solo per schermate realistiche).
"""
import os
import pathlib
import re
import sys
from urllib.parse import urlparse, parse_qs

from playwright.sync_api import sync_playwright

RADICE = pathlib.Path(__file__).resolve().parent.parent
SITO_URL = os.environ.get("SITO_URL", "").rstrip("/")
PAGINA = SITO_URL + "/" if SITO_URL else (RADICE / "index.html").as_uri()
CONSENTITI = (SITO_URL + "/", "https://images.unsplash.com/") if SITO_URL else ()
SCHERMATE = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else None
FOTO_LOCALI = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else None

esiti = []


def verifica(nome, condizione, dettaglio=""):
    esiti.append((nome, bool(condizione), dettaglio))


def instrada(route):
    url = route.request.url
    if url.startswith("file://") or url.startswith(CONSENTITI or ("\0",)):
        return route.continue_()
    m = re.match(r"https://images\.unsplash\.com/(photo-[0-9a-f-]+)", url)
    if FOTO_LOCALI and m and (FOTO_LOCALI / (m.group(1) + ".jpg")).exists():
        return route.fulfill(path=str(FOTO_LOCALI / (m.group(1) + ".jpg")), content_type="image/jpeg")
    return route.abort()


def carica_foto(pg):
    """Scorre la pagina per far partire le foto caricate in ritardo, poi torna in cima."""
    if SITO_URL:
        altezza = pg.evaluate("document.body.scrollHeight")
        for y in range(0, altezza, 500):
            pg.evaluate(f"window.scrollTo(0, {y})")
            pg.wait_for_timeout(150)
        pg.wait_for_load_state("networkidle")
        pg.wait_for_function("() => [...document.images].every(i => i.complete)", timeout=20000)
    pg.evaluate("window.scrollTo(0, 0)")
    pg.wait_for_timeout(400)


with sync_playwright() as p:
    browser = p.chromium.launch()
    ctx = browser.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
    ctx.route("**/*", instrada)
    pagina = ctx.new_page()
    errori_js = []
    pagina.on("pageerror", lambda e: errori_js.append(str(e)))
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
    verifica("AgriEuro: ricerca senza codice", casi["agrieuro"] == "https://www.agrieuro.com/search/motozappa%20elettrica", casi["agrieuro"])
    verifica("Amazon: nessun tag finto", casi["amazon"] == "https://www.amazon.it/s?k=motozappa%20elettrica", casi["amazon"])
    mm = casi["manomano"]
    mm_dest = parse_qs(urlparse(mm).query).get("ued", [""])[0] if mm.startswith("https://www.awin1.com/") else mm
    verifica("ManoMano: formato /cat/a+b", mm_dest == "https://www.manomano.it/cat/motozappa+elettrica", mm)
    verifica("ManoMano: codici Awin reali (ManoMano IT 17962, publisher 3130993)",
             parse_qs(urlparse(mm).query).get("awinmid") == ["17962"] and parse_qs(urlparse(mm).query).get("awinaffid") == ["3130993"], mm)
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
          manomano: linkNegozio('manomano','vasi grandi'),
          cat: linkCategoria('agrieuro', REPARTI[0]), catAmazon: linkCategoria('amazon', REPARTI[4])
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
    verifica("Reparto senza pagina AgriEuro -> ricerca", con["catAmazon"].startswith("https://www.amazon.it/s?k=serra"), con["catAmazon"])

    # 3. Calendario: 12 mesi completi, ogni mese con 3 lavori e foto
    cal = pagina.evaluate("""() => Object.keys(MESI).map(k => {
        const m = MESI[k];
        return [k, !!(m.nome && m.titolo && m.consiglio && m.azione && m.q && m.foto && m.alt), m.altri.length, m.altri.every(a => a.length === 3 && a.every(x => x))];
    })""")
    verifica("Calendario: 12 mesi", [c[0] for c in cal] == [str(i) for i in range(1, 13)])
    verifica("Calendario: campi completi", all(c[1] and c[2] == 3 and c[3] for c in cal), str([c for c in cal if not (c[1] and c[2] == 3 and c[3])]))
    verifica("Mese corrente mostrato", pagina.inner_text("#mese-titolo") == pagina.evaluate("MESI[meseCorrente()].titolo"))
    foto_usate = pagina.evaluate("() => [...new Set([...Object.values(MESI).map(m=>m.foto), ...REPARTI.map(r=>r.foto)])]")
    foto_ok = pagina.evaluate("() => Object.values(F)")
    verifica("Solo foto verificate", all(f in foto_ok for f in foto_usate), str(foto_usate))

    # 4. Ricerca nella testata
    verifica("Menu negozi nascosto a campo vuoto", not pagina.is_visible("#scelte"))
    pagina.fill("#cosa", "tubo gocciolante")
    bott = pagina.locator("#scelte button")
    verifica("Menu con 4 negozi mentre scrivi", bott.count() == 4 and pagina.is_visible("#scelte"))
    verifica("Primo negozio AgriEuro", "AgriEuro" in bott.first.inner_text())
    richieste = []
    ctx.on("request", lambda r: r.is_navigation_request() and richieste.append(r.url))
    with ctx.expect_page() as nuova:
        bott.nth(3).click()
    nuova.value.wait_for_load_state()
    verifica("Tocco su eBay apre la ricerca giusta", "https://www.ebay.it/sch/i.html?_nkw=tubo%20gocciolante" in richieste, str(richieste))
    nuova.value.close()
    richieste.clear()
    with ctx.expect_page() as nuova:
        pagina.press("#cosa", "Enter")
    nuova.value.wait_for_load_state()
    verifica("Invio apre AgriEuro", any(u.startswith("https://www.agrieuro.com/search/tubo") for u in richieste), str(richieste))
    nuova.value.close()
    pagina.fill("#cosa", "   ")
    verifica("Solo spazi: menu chiuso", not pagina.is_visible("#scelte"))
    aperte = []
    ctx.on("page", lambda pg: aperte.append(pg.url))
    pagina.press("#cosa", "Enter")
    pagina.wait_for_timeout(300)
    verifica("Solo spazi + Invio: non apre nulla", len(aperte) == 0)
    pagina.fill("#cosa", "")
    pagina.locator("body").click(position={"x": 5, "y": 400})

    # 5. Lavori del mese e pannello
    verifica("3 lavori del mese", pagina.locator("#altri button").count() == 3)
    if SCHERMATE:
        SCHERMATE.mkdir(parents=True, exist_ok=True)
        carica_foto(pagina)
        pagina.screenshot(path=str(SCHERMATE / "1-telefono-inizio.png"))
        pagina.screenshot(path=str(SCHERMATE / "2-telefono-intera.png"), full_page=True)
    pagina.click("#mese-azione")
    verifica("Bottone del mese apre il pannello", pagina.is_visible("#pannello"))
    link = pagina.eval_on_selector_all("#pannello-link a", "els => els.map(a => [a.firstChild.textContent, a.href, a.rel, a.target])")
    verifica("Pannello: 4 negozi in ordine", [l[0] for l in link] == ["AgriEuro", "Amazon", "ManoMano", "eBay"], str(link))
    verifica("Pannello: link sponsored in nuova scheda", all(l[2] == "sponsored noopener" and l[3] == "_blank" for l in link))
    verifica("Pannello: query del mese", pagina.evaluate("encodeURIComponent(MESI[meseCorrente()].q)") in link[1][1], link[1][1])
    if SCHERMATE:
        pagina.screenshot(path=str(SCHERMATE / "3-telefono-pannello.png"))
    pagina.keyboard.press("Escape")
    verifica("Pannello si chiude con Esc", not pagina.is_visible("#pannello"))
    pagina.click("#mese-azione")
    pagina.evaluate("""() => { const c = document.querySelector('.pannello-corpo'); const r = c.getBoundingClientRect();
        const t = (y) => new Touch({identifier: 1, target: c, clientX: r.left + 40, clientY: y});
        c.dispatchEvent(new TouchEvent('touchstart', {touches: [t(r.top + 20)], bubbles: true}));
        c.dispatchEvent(new TouchEvent('touchmove', {touches: [t(r.top + 160)], bubbles: true}));
        c.dispatchEvent(new TouchEvent('touchend', {touches: [], bubbles: true})); }""")
    verifica("Pannello si chiude trascinandolo giù", not pagina.is_visible("#pannello"))
    pagina.click("#mese-azione")
    pagina.evaluate("""() => { const c = document.querySelector('.pannello-corpo'); const r = c.getBoundingClientRect();
        const t = (y) => new Touch({identifier: 1, target: c, clientX: r.left + 40, clientY: y});
        c.dispatchEvent(new TouchEvent('touchstart', {touches: [t(r.top + 20)], bubbles: true}));
        c.dispatchEvent(new TouchEvent('touchmove', {touches: [t(r.top + 50)], bubbles: true}));
        c.dispatchEvent(new TouchEvent('touchend', {touches: [], bubbles: true})); }""")
    verifica("Piccolo trascinamento non chiude", pagina.is_visible("#pannello"))
    pagina.keyboard.press("Escape")

    # 6. Reparti e consigli
    verifica("9 reparti con foto", pagina.locator(".reparto").count() == 9 and pagina.locator(".reparto img").count() == 9)
    verifica("Tutte le foto hanno testo alternativo", pagina.evaluate("() => [...document.querySelectorAll('main img')].every(i => i.alt)"))
    verifica("Nessuna icona disegnata nei reparti", pagina.locator(".reparto svg").count() == 0)
    pagina.locator(".reparto").nth(2).click()
    href0 = pagina.get_attribute("#pannello-link a >> nth=0", "href")
    verifica("Reparto robot: AgriEuro va alla categoria", href0 == "https://www.agrieuro.com/robot-tagliaerba-c-59.html", href0)
    pagina.keyboard.press("Escape")
    pagina.locator(".consigli button").first.click()
    verifica("Consiglio motozappa apre il pannello giusto", pagina.inner_text("#pannello-titolo") == "Motozappe")
    pagina.keyboard.press("Escape")

    # 7. Layout
    verifica("Nessuno scorrimento orizzontale (390 px)", pagina.evaluate("() => document.documentElement.scrollWidth <= window.innerWidth"))
    verifica("Ricerca resta visibile in alto scorrendo", pagina.evaluate("() => { window.scrollTo(0, 1500); const r = document.querySelector('#cosa').getBoundingClientRect(); return r.top >= 0 && r.top < 20; }"))
    verifica("Elementi toccabili alti almeno 44 px", pagina.evaluate("() => [...document.querySelectorAll('main button, .chiudi')].filter(b => b.offsetParent).every(b => b.getBoundingClientRect().height >= 44)"),
             pagina.evaluate("() => [...document.querySelectorAll('main button')].filter(b => b.offsetParent && b.getBoundingClientRect().height < 44).map(b => b.textContent.trim()).join(', ')"))
    verifica("Tocco senza ritardo (touch-action)", pagina.evaluate("() => getComputedStyle(document.querySelector('.reparto')).touchAction === 'manipulation'"))

    desk = browser.new_context(viewport={"width": 1280, "height": 900})
    desk.route("**/*", instrada)
    pd = desk.new_page()
    pd.on("pageerror", lambda e: errori_js.append(str(e)))
    pd.goto(PAGINA)
    verifica("Desktop: nessuno scorrimento orizzontale", pd.evaluate("() => document.documentElement.scrollWidth <= window.innerWidth"))
    if SCHERMATE:
        carica_foto(pd)
        pd.screenshot(path=str(SCHERMATE / "4-computer.png"), full_page=True)

    # 8. Pagine-guida
    GUIDE = {"motozappa": "https://www.agrieuro.com/motozappe-c-22.html",
             "robot-tagliaerba": "https://www.agrieuro.com/robot-tagliaerba-c-59.html",
             "irrigazione-a-goccia": "https://www.agrieuro.com/irrigazione-g-14.html",
             "decespugliatore": "https://www.agrieuro.com/decespugliatori-c-3.html"}
    pg = ctx.new_page()
    pg.on("pageerror", lambda e: errori_js.append(str(e)))
    for slug, cat in GUIDE.items():
        url_g = f"{SITO_URL}/guide/{slug}/" if SITO_URL else (RADICE / "guide" / slug / "index.html").as_uri()
        pg.goto(url_g)
        pg.wait_for_load_state("load")
        link = pg.eval_on_selector_all(".dove a", "els => els.map(a => [a.firstChild.textContent, a.href, a.rel, a.target])")
        verifica(f"Guida {slug}: 4 negozi in ordine", [l[0] for l in link] == ["AgriEuro", "Amazon", "ManoMano", "eBay"], str(link))
        verifica(f"Guida {slug}: AgriEuro alla categoria", link and link[0][1] == cat, link[0][1] if link else "")
        verifica(f"Guida {slug}: link sponsored", all(l[2] == "sponsored noopener" and l[3] == "_blank" for l in link))
        verifica(f"Guida {slug}: barra in basso verso AgriEuro", pg.get_attribute("#barra-agrieuro", "href") == cat)
        verifica(f"Guida {slug}: titolo e descrizione", pg.title().endswith("| OrtoCasa Help") and len(pg.get_attribute('meta[name=description]', 'content') or '') > 60)
        verifica(f"Guida {slug}: nessuno scorrimento orizzontale", pg.evaluate("() => document.documentElement.scrollWidth <= window.innerWidth"))
        verifica(f"Guida {slug}: link toccabili alti almeno 44 px", pg.evaluate("() => [...document.querySelectorAll('.dove a, .altre a, .barra-acquisto a')].every(a => a.getBoundingClientRect().height >= 44)"))
        verifica(f"Guida {slug}: link alle altre guide funzionano", pg.evaluate("() => [...document.querySelectorAll('.altre a')].length") == len(GUIDE) - 1)
        if SCHERMATE and slug == "motozappa":
            carica_foto(pg)
            pg.screenshot(path=str(SCHERMATE / "5-guida-telefono.png"), full_page=True)
    pg.close()
    verifica("Home: 3 link alle guide", pagina.locator(".consigli a.guida").count() == 3)
    verifica("Home: link alla privacy", pagina.locator('footer a[href="privacy/"]').count() == 1)
    pp = ctx.new_page()
    pp.on("pageerror", lambda e: errori_js.append(str(e)))
    pp.goto(f"{SITO_URL}/privacy/" if SITO_URL else (RADICE / "privacy" / "index.html").as_uri())
    verifica("Privacy: titolare e contatto presenti", "Stefano Ciceri" in pp.inner_text("main") and "stefano.ciceri@gmail.com" in pp.inner_text("main"))
    verifica("Privacy: nessuno scorrimento orizzontale", pp.evaluate("() => document.documentElement.scrollWidth <= window.innerWidth"))
    pp.close()

    file_google = sorted(RADICE.glob("google*.html"))
    verifica("Search Console: file di verifica Google presente e corretto",
             len(file_google) == 1 and file_google[0].read_text() == f"google-site-verification: {file_google[0].name}")

    verifica("Nessun errore JavaScript", not errori_js, "; ".join(errori_js))
    browser.close()

falliti = [e for e in esiti if not e[1]]
for nome, ok, det in esiti:
    print(("OK   " if ok else "FAIL ") + nome + ("" if ok or not det else "  -> " + det))
print(f"\n{len(esiti) - len(falliti)}/{len(esiti)} verifiche superate")
sys.exit(1 if falliti else 0)
