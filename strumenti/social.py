"""Pubblica i post di OrtoCasa Help su Pagina Facebook e Instagram, senza computer acceso.

Gira su GitHub Actions (workflow "Social"), martedì e sabato. Legge la coda dei post da una cartella
dati (il ramo "social" del repository), pubblica il primo post pronto con le API ufficiali di Meta
e annota l'esito in stato.json ed esito.md nella stessa cartella.

Uso:  python3 strumenti/social.py <cartella-dati> [AAAA-MM-GG]

Variabili d'ambiente (segreti di GitHub, mai nel codice):
  META_PAGE_ID     ID della Pagina Facebook OrtoCasa Help
  META_PAGE_TOKEN  token di accesso della Pagina (permessi pages_manage_posts, instagram_content_publish)
  META_IG_ID       ID dell'account Instagram professionale collegato alla Pagina
  META_GRAPH_VERSION  facoltativa, versione delle Graph API (predefinita v23.0)
Se mancano, nessun post viene pubblicato: l'esito lo dice e il post resta in coda.

Formato di coda.json: lista di post, ognuno così:
  {"id": "2026-10-28-pacciamatura", "data": "2026-10-28", "testo": "...", "link": "https://ortocasahelp.netlify.app/guide/...",
   "foto": "https://images.unsplash.com/photo-...&fm=jpg", "canali": ["facebook", "instagram", "storia"]}
"""
import datetime
import json
import pathlib
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import zoneinfo

SITO = "https://ortocasahelp.netlify.app"
CANALI = ("facebook", "instagram", "storia")
ETICHETTA_ADV = "#ADV"
LUNGHEZZA_MAX_TESTO = 2000  # Instagram accetta didascalie fino a 2200 caratteri
TENTATIVI_STATO = 10
ATTESA_STATO_S = 3


class ErroreAPI(Exception):
    pass


def http_post(url, campi, timeout=30):
    """POST form-urlencoded; restituisce il JSON della risposta o solleva ErroreAPI."""
    dati = urllib.parse.urlencode(campi).encode()
    req = urllib.request.Request(url, data=dati, method="POST")
    return _esegui(req, timeout)


def http_get(url, campi, timeout=30):
    req = urllib.request.Request(url + "?" + urllib.parse.urlencode(campi), method="GET")
    return _esegui(req, timeout)


def _esegui(req, timeout):
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        corpo = e.read().decode(errors="replace")[:500]
        raise ErroreAPI(f"HTTP {e.code}: {corpo}") from e
    except (urllib.error.URLError, TimeoutError) as e:
        raise ErroreAPI(f"rete: {e}") from e


def valida(post):
    """Restituisce l'elenco dei problemi del post (vuoto se è pubblicabile)."""
    problemi = []
    for campo in ("id", "data", "testo", "link", "foto", "canali"):
        if not post.get(campo):
            problemi.append(f"manca '{campo}'")
    if problemi:
        return problemi
    try:
        datetime.date.fromisoformat(post["data"])
    except ValueError:
        problemi.append("data non valida (serve AAAA-MM-GG)")
    if len(post["testo"]) > LUNGHEZZA_MAX_TESTO:
        problemi.append(f"testo oltre {LUNGHEZZA_MAX_TESTO} caratteri")
    if not post["link"].startswith("https://"):
        problemi.append("link non https")
    elif not post["link"].startswith(SITO + "/") and ETICHETTA_ADV not in post["testo"]:
        problemi.append(f"link esterno (affiliato?) senza {ETICHETTA_ADV} nel testo")
    if not post["foto"].startswith("https://"):
        problemi.append("foto non https")
    sconosciuti = [c for c in post["canali"] if c not in CANALI]
    if sconosciuti:
        problemi.append(f"canali sconosciuti: {sconosciuti}")
    return problemi


class Meta:
    def __init__(self, page_id, token, ig_id, versione="v23.0", post=http_post, get=http_get, attendi=time.sleep):
        self.page_id, self.token, self.ig_id = page_id, token, ig_id
        self.base = f"https://graph.facebook.com/{versione}"
        self.post, self.get, self.attendi = post, get, attendi

    def facebook(self, p):
        r = self.post(f"{self.base}/{self.page_id}/feed", {"message": p["testo"], "link": p["link"], "access_token": self.token})
        return r["id"]

    def _instagram(self, campi):
        contenitore = self.post(f"{self.base}/{self.ig_id}/media", {**campi, "access_token": self.token})["id"]
        for _ in range(TENTATIVI_STATO):
            stato = self.get(f"{self.base}/{contenitore}", {"fields": "status_code", "access_token": self.token}).get("status_code")
            if stato == "FINISHED":
                break
            if stato in ("ERROR", "EXPIRED"):
                raise ErroreAPI(f"Instagram: contenitore {contenitore} in stato {stato}")
            self.attendi(ATTESA_STATO_S)
        else:
            raise ErroreAPI(f"Instagram: contenitore {contenitore} non pronto dopo {TENTATIVI_STATO} controlli")
        return self.post(f"{self.base}/{self.ig_id}/media_publish", {"creation_id": contenitore, "access_token": self.token})["id"]

    def instagram(self, p):
        # Su Instagram i link nella didascalia non sono cliccabili: si rimanda al link in bio.
        didascalia = p["testo"] + "\n\nLa guida completa: link in bio."
        return self._instagram({"image_url": p["foto"], "caption": didascalia})

    def storia(self, p):
        return self._instagram({"image_url": p["foto"], "media_type": "STORIES"})


def scegli(coda, stato, oggi):
    """Primo post valido, con data <= oggi, che ha ancora canali da pubblicare."""
    for p in coda:
        if valida(p) or datetime.date.fromisoformat(p["data"]) > oggi:
            continue
        fatti = stato.get(p["id"], {})
        if any(c not in fatti for c in p["canali"]):
            return p
    return None


def esegui(cartella, oggi, env, meta_factory=Meta):
    cartella = pathlib.Path(cartella)
    coda = json.loads((cartella / "coda.json").read_text(encoding="utf-8")) if (cartella / "coda.json").exists() else []
    file_stato = cartella / "stato.json"
    stato = json.loads(file_stato.read_text(encoding="utf-8")) if file_stato.exists() else {}
    righe = [f"# Social: esito del {oggi.isoformat()}", ""]
    invalidi = [(p.get("id", "?"), valida(p)) for p in coda if valida(p)]
    for pid, probl in invalidi:
        righe.append(f"- Post {pid} scartato: {', '.join(probl)}")
    errore = False
    post = scegli(coda, stato, oggi)
    if post is None:
        righe.append("- Nessun post pronto in coda.")
    elif not (env.get("META_PAGE_TOKEN") and env.get("META_PAGE_ID")):
        righe.append(f"- Post {post['id']} pronto ma non pubblicato: mancano i segreti META_PAGE_ID/META_PAGE_TOKEN.")
    else:
        meta = meta_factory(env["META_PAGE_ID"], env["META_PAGE_TOKEN"], env.get("META_IG_ID", ""),
                            env.get("META_GRAPH_VERSION") or "v23.0")
        fatti = stato.setdefault(post["id"], {})
        for canale in post["canali"]:
            if canale in fatti:
                continue
            if canale in ("instagram", "storia") and not env.get("META_IG_ID"):
                righe.append(f"- {post['id']} / {canale}: saltato, manca META_IG_ID.")
                continue
            try:
                fatti[canale] = {"id": getattr(meta, canale)(post), "quando": oggi.isoformat()}
                righe.append(f"- {post['id']} / {canale}: pubblicato (id {fatti[canale]['id']}).")
            except (ErroreAPI, KeyError) as e:
                errore = True
                righe.append(f"- {post['id']} / {canale}: ERRORE {e}")
        if not fatti:
            del stato[post["id"]]
    file_stato.write_text(json.dumps(stato, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    in_coda = sum(1 for p in coda if not valida(p) and any(c not in stato.get(p["id"], {}) for c in p["canali"]))
    righe.append(f"- Post ancora da pubblicare in coda: {in_coda}.")
    (cartella / "esito.md").write_text("\n".join(righe) + "\n", encoding="utf-8")
    print("\n".join(righe))
    return 1 if errore or invalidi else 0


if __name__ == "__main__":
    import os
    if len(sys.argv) < 2:
        sys.exit("Uso: python3 strumenti/social.py <cartella-dati> [AAAA-MM-GG]")
    giorno = datetime.date.fromisoformat(sys.argv[2]) if len(sys.argv) > 2 else datetime.datetime.now(zoneinfo.ZoneInfo("Europe/Rome")).date()
    sys.exit(esegui(sys.argv[1], giorno, os.environ))
