"""Test di strumenti/social.py senza rete: le chiamate a Meta sono simulate.

Uso:  python3 tests/test_social.py
"""
import datetime
import json
import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "strumenti"))
import social

OGGI = datetime.date(2026, 10, 28)
ENV = {"META_PAGE_ID": "111", "META_PAGE_TOKEN": "tok", "META_IG_ID": "222"}


def post(pid="p1", data="2026-10-28", **extra):
    base = {"id": pid, "data": data, "testo": "Consiglio di stagione", "link": "https://ortocasahelp.netlify.app/guide/motozappa/",
            "foto": "https://images.unsplash.com/photo-1?fm=jpg", "canali": ["facebook", "instagram", "storia"]}
    base.update(extra)
    return base


class FintoMeta:
    """Registra le chiamate HTTP e risponde come le Graph API."""

    def __init__(self, stati=("FINISHED",), errore_su=None):
        self.chiamate, self.stati, self.errore_su = [], list(stati), errore_su

    def post(self, url, campi):
        self.chiamate.append(("POST", url, campi))
        if self.errore_su and self.errore_su in url:
            raise social.ErroreAPI("HTTP 400: finto errore")
        if url.endswith("/feed"):
            return {"id": "111_9"}
        if url.endswith("/media"):
            return {"id": "c1"}
        return {"id": "m1"}

    def get(self, url, campi):
        self.chiamate.append(("GET", url, campi))
        return {"status_code": self.stati.pop(0) if self.stati else "FINISHED"}


def esegui(coda, stato=None, env=ENV, finto=None, pubblica=True):
    finto = finto or FintoMeta()
    with tempfile.TemporaryDirectory() as d:
        cart = pathlib.Path(d)
        if pubblica is not None:
            (cart / "config.json").write_text(json.dumps({"pubblica": pubblica}), encoding="utf-8")
        (cart / "coda.json").write_text(json.dumps(coda), encoding="utf-8")
        if stato is not None:
            (cart / "stato.json").write_text(json.dumps(stato), encoding="utf-8")
        fabbrica = lambda *a: social.Meta(*a, post=finto.post, get=finto.get, attendi=lambda s: None)
        codice = social.esegui(cart, OGGI, env, meta_factory=fabbrica)
        return codice, json.loads((cart / "stato.json").read_text()), (cart / "esito.md").read_text(), finto


class TestValida(unittest.TestCase):
    def test_post_buono(self):
        self.assertEqual(social.valida(post()), [])

    def test_campi_mancanti(self):
        self.assertIn("manca 'testo'", social.valida(post(testo="")))

    def test_link_esterno_senza_adv(self):
        p = post(link="https://www.agrieuro.com/motozappe-c-22.html")
        self.assertTrue(any("#ADV" in x for x in social.valida(p)))
        p["testo"] = "#ADV link affiliato. Motozappe"
        self.assertEqual(social.valida(p), [])

    def test_data_e_canali_sbagliati(self):
        probl = social.valida(post(data="28/10/2026", canali=["tiktok"]))
        self.assertTrue(any("data" in x for x in probl) and any("canali" in x for x in probl))

    def test_testo_troppo_lungo_e_http(self):
        probl = social.valida(post(testo="a" * 2001, foto="http://x"))
        self.assertEqual(len(probl), 2)


class TestEsegui(unittest.TestCase):
    def test_pubblica_tutti_i_canali(self):
        codice, stato, esito, f = esegui([post()])
        self.assertEqual(codice, 0)
        self.assertEqual(set(stato["p1"]), {"facebook", "instagram", "storia"})
        feed = next(c for c in f.chiamate if c[1].endswith("/111/feed"))[2]
        self.assertEqual(feed["link"], "https://ortocasahelp.netlify.app/guide/motozappa/")
        storie = [c for c in f.chiamate if c[1].endswith("/media") and c[2].get("media_type") == "STORIES"]
        self.assertEqual(len(storie), 1)
        didascalia = next(c for c in f.chiamate if c[1].endswith("/media") and "caption" in c[2])[2]["caption"]
        self.assertIn("link in bio", didascalia)
        self.assertIn("ancora da pubblicare in coda: 0", esito)

    def test_post_futuro_non_pubblicato(self):
        codice, stato, esito, f = esegui([post(data="2026-11-01")])
        self.assertEqual((codice, stato, f.chiamate), (0, {}, []))
        self.assertIn("Nessun post pronto", esito)

    def test_un_post_per_esecuzione_in_ordine(self):
        _, stato, _, _ = esegui([post("a"), post("b")])
        self.assertEqual(list(stato), ["a"])
        _, stato, _, _ = esegui([post("a"), post("b")], stato=stato)
        self.assertEqual(list(stato), ["a", "b"])

    def test_senza_segreti_nessuna_chiamata(self):
        codice, stato, esito, f = esegui([post()], env={})
        self.assertEqual((codice, stato, f.chiamate), (0, {}, []))
        self.assertIn("mancano i segreti", esito)

    def test_senza_instagram_solo_facebook(self):
        env = {k: v for k, v in ENV.items() if k != "META_IG_ID"}
        _, stato, esito, _ = esegui([post()], env=env)
        self.assertEqual(list(stato["p1"]), ["facebook"])
        self.assertIn("manca META_IG_ID", esito)

    def test_errore_api_segnalato_e_riprovato_dopo(self):
        codice, stato, esito, _ = esegui([post()], finto=FintoMeta(errore_su="/media"))
        self.assertEqual(codice, 1)
        self.assertEqual(list(stato["p1"]), ["facebook"])
        self.assertIn("ERRORE", esito)
        # al giro dopo riprova solo i canali mancanti, senza ripubblicare su Facebook
        codice, stato, _, f = esegui([post()], stato=stato)
        self.assertEqual(codice, 0)
        self.assertFalse(any(c[1].endswith("/feed") for c in f.chiamate))
        self.assertEqual(set(stato["p1"]), {"facebook", "instagram", "storia"})

    def test_contenitore_instagram_in_errore(self):
        codice, stato, esito, _ = esegui([post(canali=["instagram"])], finto=FintoMeta(stati=["IN_PROGRESS", "ERROR"]))
        self.assertEqual((codice, stato), (1, {}))
        self.assertIn("ERROR", esito)

    def test_contenitore_mai_pronto(self):
        codice, _, esito, _ = esegui([post(canali=["storia"])], finto=FintoMeta(stati=["IN_PROGRESS"] * 20))
        self.assertEqual(codice, 1)
        self.assertIn("non pronto", esito)

    def test_post_invalido_segnalato(self):
        codice, stato, esito, _ = esegui([post("x", testo=""), post("y")])
        self.assertEqual(codice, 1)
        self.assertIn("Post x scartato", esito)
        self.assertIn("y", stato)

    def test_in_pausa_nessuna_chiamata(self):
        for valore in (False, None):
            codice, stato, esito, f = esegui([post()], pubblica=valore)
            self.assertEqual((codice, stato, f.chiamate), (0, {}, []))
            self.assertIn("In pausa", esito)

    def test_coda_assente(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(social.esegui(d, OGGI, ENV), 0)
            self.assertIn("Nessun post pronto", (pathlib.Path(d) / "esito.md").read_text())


class TestCodaReale(unittest.TestCase):
    """La coda pronta nel repository (social/coda.json) deve essere tutta valida."""

    def test_coda_del_repository(self):
        f = pathlib.Path(__file__).resolve().parent.parent / "social" / "coda.json"
        if not f.exists():
            self.skipTest("nessuna coda nel ramo corrente")
        coda = json.loads(f.read_text(encoding="utf-8"))
        self.assertTrue(coda)
        for p in coda:
            self.assertEqual(social.valida(p), [], p.get("id"))
        self.assertEqual(len({p["id"] for p in coda}), len(coda), "id duplicati")


if __name__ == "__main__":
    unittest.main(verbosity=1)
