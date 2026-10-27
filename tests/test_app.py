"""Test dell'app installabile (manifest, icone, service worker, lettura senza rete).

Uso:  python3 tests/test_app.py
Avvia un piccolo server su localhost (il service worker funziona solo su https o localhost).
"""
import functools
import http.server
import json
import pathlib
import socketserver
import struct
import sys
import threading

from playwright.sync_api import sync_playwright

RADICE = pathlib.Path(__file__).resolve().parent.parent
esiti = []


def verifica(nome, ok, dettaglio=""):
    esiti.append((nome, bool(ok), dettaglio))


def dimensioni_png(p):
    with open(p, "rb") as f:
        testa = f.read(24)
    return struct.unpack(">II", testa[16:24])


# 1. Manifest e icone
man = json.loads((RADICE / "manifest.webmanifest").read_text(encoding="utf-8"))
verifica("Manifest: nome, avvio e modalità app", man["name"] == "OrtoCasa Help" and man["start_url"].startswith("/") and man["display"] == "standalone")
for ic in man["icons"]:
    f = RADICE / ic["src"].lstrip("/")
    lato = int(ic["sizes"].split("x")[0])
    verifica(f"Icona {ic['src']} esiste e misura {ic['sizes']}", f.exists() and dimensioni_png(f) == (lato, lato))
verifica("Icona maskable presente", any(i.get("purpose") == "maskable" for i in man["icons"]))
verifica("Icona Apple 180x180", dimensioni_png(RADICE / "icone/apple-touch-icon.png") == (180, 180))
pagine = [RADICE / "index.html", RADICE / "privacy/index.html", RADICE / "chi-siamo/index.html", *sorted((RADICE / "guide").glob("**/index.html"))]
senza = [str(p.relative_to(RADICE)) for p in pagine if 'rel="manifest"' not in p.read_text(encoding="utf-8") or "/app.js" not in p.read_text(encoding="utf-8")]
verifica("Ogni pagina collega manifest e app.js", not senza, str(senza))

# 2. Service worker vero su localhost
class Silenzioso(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


Gestore = functools.partial(Silenzioso, directory=str(RADICE))
with socketserver.TCPServer(("localhost", 0), Gestore) as srv:
    porta = srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = f"http://localhost:{porta}"
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": 390, "height": 844}, is_mobile=True)
        ctx.route("https://**/*", lambda r: r.abort())  # niente rete esterna (foto, negozi)
        pg = ctx.new_page()
        errori = []
        pg.on("pageerror", lambda e: errori.append(str(e)))
        pg.goto(base + "/")
        pronto = pg.evaluate("() => navigator.serviceWorker.ready.then(r => !!r.active)")
        verifica("Service worker attivo", pronto)
        pg.reload()
        verifica("La pagina è controllata dal service worker", pg.evaluate("() => !!navigator.serviceWorker.controller"))
        pg.goto(base + "/guide/microgreens/")
        ctx.set_offline(True)
        pg.reload()
        verifica("Senza rete: la guida visitata si apre", "Microgreens" in pg.title(), pg.title())
        pg.goto(base + "/guide/motozappa/")
        verifica("Senza rete: una pagina mai vista mostra la home salvata", "OrtoCasa Help" in pg.title(), pg.title())
        ctx.set_offline(False)
        verifica("Nessun errore JavaScript", not errori, "; ".join(errori))
        browser.close()
    srv.shutdown()

falliti = [e for e in esiti if not e[1]]
for nome, ok, det in esiti:
    print(("OK   " if ok else "FAIL ") + nome + ("" if ok or not det else "  -> " + det))
print(f"\n{len(esiti) - len(falliti)}/{len(esiti)} verifiche superate")
sys.exit(1 if falliti else 0)
