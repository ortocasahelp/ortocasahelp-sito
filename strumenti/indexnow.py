"""Segnala a Bing e agli altri motori IndexNow le pagine del sito (nessun account necessario).

Uso:  python3 strumenti/indexnow.py https://ortocasahelp.netlify.app [report.md]
Legge le pagine da sitemap.xml e la chiave dal file <chiave>.txt nella radice del sito.
La chiave non è un segreto: IndexNow la vuole pubblica, per dimostrare che il sito è nostro.
"""
import json
import pathlib
import re
import sys
import urllib.error
import urllib.request

RADICE = pathlib.Path(__file__).resolve().parent.parent
BASE = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "https://ortocasahelp.netlify.app"
REPORT = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else None

chiavi = [p for p in RADICE.glob("*.txt") if re.fullmatch(r"[0-9a-f]{32}\.txt", p.name)]
if len(chiavi) != 1:
    sys.exit(f"Serve esattamente un file chiave IndexNow nella radice, trovati {len(chiavi)}")
chiave = chiavi[0].stem
urls = re.findall(r"<loc>([^<]+)</loc>", (RADICE / "sitemap.xml").read_text(encoding="utf-8"))
urls = [u.replace("https://ortocasahelp.netlify.app", BASE) for u in urls]
corpo = json.dumps({"host": BASE.split("//", 1)[1], "key": chiave, "keyLocation": f"{BASE}/{chiave}.txt", "urlList": urls}).encode()
req = urllib.request.Request("https://api.indexnow.org/indexnow", data=corpo, method="POST",
                             headers={"Content-Type": "application/json; charset=utf-8"})
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        stato = r.status
except urllib.error.HTTPError as e:
    stato = e.code
except Exception as e:
    stato = f"errore di rete: {e}"
# 200 e 202 = ricevuto; 422 = URL non corrispondenti alla chiave; 403 = chiave non trovata online
ok = stato in (200, 202)
riga = f"IndexNow: {len(urls)} pagine segnalate, risposta {stato} ({'OK' if ok else 'da controllare'})"
print(riga)
if REPORT:
    with REPORT.open("a", encoding="utf-8") as f:
        f.write(f"\n{riga}\n")
sys.exit(0 if ok else 1)
