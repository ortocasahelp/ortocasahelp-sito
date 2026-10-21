"""Verifica del sito pubblicato e dei collegamenti esterni (solo libreria standard).

Uso:  python3 tests/verifica_online.py https://ortocasahelp.netlify.app [report.md]

Controlli:
  1. La home online è identica a index.html del repository (attende fino a 10 minuti
     che Netlify finisca la pubblicazione).
  2. fonts.css è online.
  3. Ogni foto Unsplash usata dal sito risponde con un'immagine.
  4. Le pagine categoria AgriEuro esistono.
  5. Le ricerche sui 4 negozi rispondono (avviso, non errore: i negozi a volte bloccano i robot).
Esce con codice 1 se un controllo bloccante fallisce.
"""
import pathlib
import re
import sys
import time
import urllib.error
import urllib.request

RADICE = pathlib.Path(__file__).resolve().parent.parent
BASE = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "https://ortocasahelp.netlify.app"
REPORT = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else None
ATTESA_MAX_S = 600
UA = "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Mobile Safari/537.36 OrtoCasaHelp-controlli"

righe = []
bloccanti_falliti = 0


def scarica(url, metodo="GET", timeout=25):
    req = urllib.request.Request(url, method=metodo, headers={"User-Agent": UA, "Accept-Language": "it-IT,it;q=0.9"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.headers.get("Content-Type", ""), r.read() if metodo == "GET" else b"", r.geturl()
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get("Content-Type", "") if e.headers else "", b"", url
    except Exception as e:  # rete, timeout, DNS
        return 0, "", str(e).encode(), url


def esito(nome, ok, dettaglio="", bloccante=True):
    global bloccanti_falliti
    simbolo = "OK" if ok else ("ERRORE" if bloccante else "AVVISO")
    if not ok and bloccante:
        bloccanti_falliti += 1
    righe.append((simbolo, nome, dettaglio))
    print(f"{simbolo:7} {nome}" + (f"  -> {dettaglio}" if dettaglio else ""), flush=True)


# 1. Home identica al repository
locale = (RADICE / "index.html").read_bytes()
inizio = time.time()
while True:
    stato, _, corpo, _ = scarica(BASE + "/")
    if stato == 200 and corpo == locale:
        esito("Home online aggiornata all'ultima versione", True, f"dopo {int(time.time() - inizio)} s")
        break
    if time.time() - inizio > ATTESA_MAX_S:
        motivo = f"HTTP {stato}" if stato != 200 else "contenuto diverso da index.html del repository"
        esito("Home online aggiornata all'ultima versione", False, motivo)
        break
    time.sleep(20)

# 2. Font
stato, tipo, corpo, _ = scarica(BASE + "/fonts.css")
esito("fonts.css online", stato == 200 and b"@font-face" in corpo, f"HTTP {stato}")

# 2b. Guide, sitemap e robots
chiave_indexnow = [p.name for p in RADICE.glob("*.txt") if re.fullmatch(r"[0-9a-f]{32}\.txt", p.name)]
for percorso in chiave_indexnow + ["privacy/", "guide/motozappa/", "guide/robot-tagliaerba/", "guide/irrigazione-a-goccia/", "guide/guida.css", "guide/guida.js", "negozi.js", "sitemap.xml", "robots.txt"]:
    stato, _, corpo, _ = scarica(f"{BASE}/{percorso}")
    locale_file = RADICE / (percorso + "index.html" if percorso.endswith("/") else percorso)
    identico = locale_file.exists() and corpo == locale_file.read_bytes()
    esito(f"Online: {percorso}", stato == 200 and identico, f"HTTP {stato}" + ("" if identico else ", diverso dal repository"))

# 3. Foto
testo = locale.decode("utf-8")
testo_guide = "".join(p.read_text(encoding="utf-8") for p in (RADICE / "guide").glob("*/index.html"))
foto = sorted(set(re.findall(r'"(photo-[0-9]+-[0-9a-f]+)"', testo) + re.findall(r'/(photo-[0-9]+-[0-9a-f]+)\?', testo_guide)))
for f in foto:
    stato, tipo, _, _ = scarica(f"https://images.unsplash.com/{f}?auto=format&fit=crop&w=200&q=50")
    esito(f"Foto {f}", stato == 200 and tipo.startswith("image/"), f"HTTP {stato} {tipo}")

# 4. Pagine categoria AgriEuro
for url in sorted(set(re.findall(r'"(https://www\.agrieuro\.com/[a-z0-9-]+-[cg]-\d+\.html)"', testo))):
    stato, _, _, finale = scarica(url)
    esito(f"AgriEuro categoria {url.rsplit('/', 1)[1]}", stato == 200, f"HTTP {stato}" + (f", rimanda a {finale}" if finale != url else ""))

# 5. Ricerche nei negozi (avvisi)
ricerche = {
    "AgriEuro": "https://www.agrieuro.com/search/motozappa",
    "AgriEuro (due parole)": "https://www.agrieuro.com/search/motozappa%20elettrica",
    "Amazon": "https://www.amazon.it/s?k=motozappa",
    "ManoMano": "https://www.manomano.it/cat/motozappa",
    "eBay": "https://www.ebay.it/sch/i.html?_nkw=motozappa",
}
for nome, url in ricerche.items():
    stato, _, corpo, finale = scarica(url)
    trovato = b"motozapp" in corpo.lower()
    dettaglio = f"HTTP {stato}, parola cercata {'presente' if trovato else 'assente'} nella pagina"
    if finale != url:
        dettaglio += f", rimanda a {finale}"
    esito(f"Ricerca {nome}", stato == 200 and trovato, dettaglio, bloccante=False)

totale_ok = sum(1 for r in righe if r[0] == "OK")
sintesi = f"{totale_ok}/{len(righe)} controlli OK, {bloccanti_falliti} errori bloccanti"
print("\n" + sintesi)

if REPORT:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    md = [f"# Verifica online — {time.strftime('%d/%m/%Y %H:%M UTC', time.gmtime())}", "", f"Sito: {BASE}", "", f"**{sintesi}**", "",
          "| Esito | Controllo | Dettaglio |", "|---|---|---|"]
    md += [f"| {a} | {b} | {c} |" for a, b, c in righe]
    REPORT.write_text("\n".join(md) + "\n", encoding="utf-8")

sys.exit(1 if bloccanti_falliti else 0)
