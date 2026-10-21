"""Genera le pagine-guida statiche di OrtoCasa Help e la sitemap.

Uso:  python3 strumenti/genera_guide.py
Modifica i testi in GUIDE qui sotto e rilancia: rigenera guide/<slug>/index.html e sitemap.xml.
"""
import html
import json
import pathlib

RADICE = pathlib.Path(__file__).resolve().parent.parent
SITO = "https://ortocasahelp.netlify.app"
AGGIORNATA = "2026-10-21"

GUIDE = [
    {
        "slug": "motozappa",
        "titolo": "Come scegliere la motozappa per l'orto di casa",
        "titolo_breve": "Motozappa",
        "descrizione": "Elettrica, a batteria o a scoppio? Come scegliere la motozappa giusta per il tuo orto, cosa guardare nella scheda e gli errori da evitare.",
        "attacco": "Dipende da tre cose: quanta terra lavori, com'è il terreno e quanta fatica vuoi fare tu. Il resto viene dopo.",
        "foto": "photo-1613036582025-ba1d4ccb3226",
        "alt": "Terreno scuro appena lavorato",
        "q": "motozappa",
        "agrieuro": "https://www.agrieuro.com/motozappe-c-22.html",
        "azione": "Vedi le motozappe",
        "in_breve": [
            "Orto piccolo con terra già lavorata: elettrica o a batteria.",
            "Orto medio e terreno normale: a scoppio, leggera o media.",
            "Terreno duro, prato da rompere o superfici grandi: pesante, con marce e retromarcia.",
        ],
        "sezioni": [
            ("Quale tipo ti serve", "voci", [
                ("Elettrica a filo", "Leggera e senza manutenzione del motore. Il cavo però limita: va bene per aiuole e orti vicino a casa."),
                ("A batteria", "Come l'elettrica, ma senza cavo. Controlla che l'autonomia basti per tutto l'orto, o prendi una seconda batteria."),
                ("A scoppio leggera", "Si sposta facilmente e si carica in auto. Ideale per rifinire e per terreni già lavorati."),
                ("A scoppio media o pesante", "Più peso e più potenza, con marce e retromarcia. Serve su terreni compatti e superfici grandi, ma è più faticosa da girare."),
            ]),
            ("Cosa guardare nella scheda", "punti", [
                "Larghezza di lavoro: più è larga, meno passate fai, ma tra le file strette diventa scomoda.",
                "Profondità di lavoro: per l'orto di casa non serve andare molto a fondo.",
                "Retromarcia: sulle pesanti è quasi indispensabile per uscire dagli angoli.",
                "Manico regolabile e ripiegabile: per la tua altezza e per il trasporto.",
                "Assistenza e ricambi: meglio una marca che ha un centro vicino a casa.",
            ]),
            ("Errori da evitare", "punti", [
                "Lavorare la terra bagnata: fai zolle, la compatti e te la porti dietro tutto l'anno.",
                "Prendere la più potente per sicurezza: in un orto piccolo è solo più pesante da manovrare.",
                "Passare troppe volte: sbricioli troppo la terra, e alla prima pioggia fa la crosta.",
            ]),
        ],
    },
    {
        "slug": "robot-tagliaerba",
        "titolo": "Come scegliere il robot tagliaerba",
        "titolo_breve": "Robot tagliaerba",
        "descrizione": "Con filo o senza filo, superficie, pendenza e passaggi stretti: come scegliere il robot tagliaerba giusto per il tuo prato.",
        "attacco": "Il robot giusto si sceglie guardando il prato, non la scheda: superficie, pendenza, ostacoli e passaggi stretti.",
        "foto": "photo-1741326757602-186060c5d5b5",
        "alt": "Robot tagliaerba al lavoro su un prato",
        "q": "robot tagliaerba",
        "agrieuro": "https://www.agrieuro.com/robot-tagliaerba-c-59.html",
        "azione": "Vedi i robot",
        "in_breve": [
            "Superficie massima dichiarata più grande del tuo prato, non uguale.",
            "Pendenza massima adatta al tuo terreno, se il prato non è in piano.",
            "Con filo perimetrale costa meno, senza filo si installa più in fretta.",
        ],
        "sezioni": [
            ("Con filo o senza filo", "voci", [
                ("Con filo perimetrale", "Un filo lungo il bordo del prato gli dice dove fermarsi. È affidabile ed economico, ma l'installazione richiede un pomeriggio."),
                ("Senza filo", "Si orienta con il segnale satellitare o con le telecamere, e le zone si disegnano dall'app. Sotto alberi fitti o vicino a muri alti può perdere precisione."),
            ]),
            ("Cosa guardare nella scheda", "punti", [
                "Superficie massima e ore di lavoro al giorno.",
                "Pendenza massima, in percentuale.",
                "Gestione di più zone e dei passaggi stretti tra una zona e l'altra.",
                "Altezza di taglio regolabile.",
                "Antifurto con PIN e allarme, e controllo dall'app.",
                "Rumore, se hai i vicini vicini.",
            ]),
            ("Errori da evitare", "punti", [
                "Prenderlo al limite della superficie: lavora tutto il giorno e si consuma prima.",
                "Farlo lavorare di notte: è il momento in cui girano ricci e piccoli animali.",
                "Non preparare il prato: buche, sassi e radici affioranti vanno sistemati prima.",
            ]),
        ],
        "nota": "Il robot taglia poco e spesso. L'erba tagliata resta sul prato, si decompone e torna al terreno: niente sacchi da svuotare.",
    },
    {
        "slug": "irrigazione-a-goccia",
        "titolo": "Irrigazione a goccia per l'orto: cosa serve e come montarla",
        "titolo_breve": "Irrigazione a goccia",
        "descrizione": "I pezzi che servono per l'irrigazione a goccia dell'orto, in che ordine montarli e gli errori che fanno intasare l'impianto.",
        "attacco": "Acqua alla radice, foglie asciutte, meno spreco. Si monta in un pomeriggio e dura anni.",
        "foto": "photo-1748432171507-c1d62fe2e859",
        "alt": "Aiuola con impianto di irrigazione a goccia",
        "q": "kit irrigazione a goccia",
        "agrieuro": "https://www.agrieuro.com/irrigazione-g-14.html",
        "azione": "Vedi l'irrigazione",
        "in_breve": [
            "Ala gocciolante lungo le file, gocciolatori singoli per vasi e piante isolate.",
            "Sempre filtro e riduttore di pressione subito dopo il rubinetto.",
            "Un programmatore, e l'orto si bagna anche quando non ci sei.",
        ],
        "sezioni": [
            ("I pezzi, nell'ordine dell'acqua", "sequenza", [
                ("Programmatore", "Al rubinetto: decide quando e per quanto bagnare."),
                ("Filtro", "Ferma sabbia e impurità che altrimenti intasano i gocciolatori."),
                ("Riduttore di pressione", "L'acqua di casa ha troppa pressione per i tubi della goccia."),
                ("Tubo di linea", "Porta l'acqua fino all'orto."),
                ("Ala gocciolante o gocciolatori", "L'ala lungo le file di ortaggi, i gocciolatori singoli per vasi e piante isolate."),
                ("Tappi di fine linea", "Chiudono ogni fila. Si aprono per sciacquare l'impianto."),
            ]),
            ("Cosa guardare nella scheda", "punti", [
                "Distanza tra i gocciolatori: più fitta per gli ortaggi in fila, più larga per le piante distanziate.",
                "Gocciolatori autocompensanti, se l'orto non è in piano o le file sono lunghe.",
                "Diametri e raccordi compatibili tra loro: meglio un kit o un'unica marca.",
            ]),
            ("Errori da evitare", "punti", [
                "Montare l'impianto senza filtro: i gocciolatori si intasano in poche settimane.",
                "Bagnare poco tutti i giorni: meglio meno volte e più a lungo, così le radici scendono in profondità.",
                "Lasciarlo pieno d'acqua d'inverno: svuotalo prima del gelo.",
            ]),
        ],
        "nota": "Copri l'ala gocciolante con la pacciamatura: l'acqua evapora meno e le erbacce crescono meno.",
    },
]

LOGO = ('<svg viewBox="0 0 56 56" fill="none" aria-hidden="true"><circle cx="28" cy="33" r="18" stroke="#F07F1A" stroke-width="9"/>'
        '<g transform="translate(28,18)"><path d="M0 3 L0 -3" stroke="#C9E86A" stroke-width="2.6" stroke-linecap="round"/>'
        '<path d="M0 -2 C-1.5 -9 -7 -13 -12.5 -12.5 C-11.5 -6 -5.5 -2 0 -2 Z" fill="#C9E86A"/>'
        '<path d="M0 -2 C1.5 -9 7 -13 12.5 -12.5 C11.5 -6 5.5 -2 0 -2 Z" fill="#C9E86A"/></g></svg>')


def e(t):
    return html.escape(t, quote=True)


def foto(fid, w):
    return f"https://images.unsplash.com/{fid}?auto=format&fit=crop&w={w}&q=70"


def blocco_negozi(g, classe=""):
    return (f'<div class="dove {classe}" data-q="{e(g["q"])}" data-agrieuro="{e(g.get("agrieuro", ""))}" '
            f'data-titolo="{e(g["titolo_breve"])}"></div>')


def sezione(titolo, tipo, voci):
    out = [f'<section class="parte"><h2>{e(titolo)}</h2>']
    if tipo == "voci":
        out.append('<dl class="voci">' + "".join(f"<div><dt>{e(a)}</dt><dd>{e(b)}</dd></div>" for a, b in voci) + "</dl>")
    elif tipo == "sequenza":
        out.append('<ol class="sequenza">' + "".join(f"<li><b>{e(a)}</b><span>{e(b)}</span></li>" for a, b in voci) + "</ol>")
    else:
        out.append('<ul class="punti">' + "".join(f"<li>{e(v)}</li>" for v in voci) + "</ul>")
    out.append("</section>")
    return "".join(out)


def pagina(g, altre):
    url = f"{SITO}/guide/{g['slug']}/"
    dati = {
        "@context": "https://schema.org", "@type": "Article", "headline": g["titolo"], "description": g["descrizione"],
        "image": foto(g["foto"], 1200), "dateModified": AGGIORNATA, "inLanguage": "it-IT", "mainEntityOfPage": url,
        "author": {"@type": "Organization", "name": "OrtoCasa Help"}, "publisher": {"@type": "Organization", "name": "OrtoCasa Help"},
    }
    corpo = "".join(sezione(*s) for s in g["sezioni"])
    nota = f'<p class="nota">{e(g["nota"])}</p>' if g.get("nota") else ""
    link_altre = "".join(f'<li><a href="../{a["slug"]}/">{e(a["titolo_breve"])}</a></li>' for a in altre)
    return f"""<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>{e(g["titolo"])} | OrtoCasa Help</title>
<meta name="description" content="{e(g["descrizione"])}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:title" content="{e(g["titolo"])}">
<meta property="og:description" content="{e(g["descrizione"])}">
<meta property="og:image" content="{foto(g["foto"], 1200)}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="it_IT">
<meta name="theme-color" content="#2D1846">
<link rel="preconnect" href="https://images.unsplash.com">
<link rel="stylesheet" href="../../fonts.css">
<link rel="stylesheet" href="../guida.css">
<script type="application/ld+json">{json.dumps(dati, ensure_ascii=False)}</script>
</head>
<body>
<header class="testata"><div class="contenitore">
  <a href="../../" class="logo" aria-label="OrtoCasa Help, torna alla home">{LOGO}<span class="marchio"><span class="o">O</span>rtoCasa Help</span></a>
</div></header>
<main>
  <article>
    <div class="apertura"><div class="contenitore">
      <p class="briciole"><a href="../../">Home</a> / Guide</p>
      <h1>{e(g["titolo"])}</h1>
      <p class="attacco">{e(g["attacco"])}</p>
      <img class="foto" src="{foto(g["foto"], 900)}" srcset="{foto(g["foto"], 600)} 600w, {foto(g["foto"], 900)} 900w, {foto(g["foto"], 1400)} 1400w" sizes="(min-width: 800px) 720px, 100vw" alt="{e(g["alt"])}" fetchpriority="high">
    </div></div>
    <div class="contenitore testo">
      <section class="in-breve"><h2>In breve</h2><ul>{"".join(f"<li>{e(v)}</li>" for v in g["in_breve"])}</ul></section>
      {corpo}
      {nota}
      <section class="parte" id="dove"><h2>Dove comprarla</h2><p class="sotto">Si apre la pagina del negozio, con i suoi prezzi, spedizioni e garanzie.</p>{blocco_negozi(g)}</section>
      <section class="parte altre"><h2>Altre guide</h2><ul>{link_altre}</ul></section>
      <p class="firma">Guida di OrtoCasa Help, a cura di un perito agrario. Aggiornata il {AGGIORNATA[8:10]}/{AGGIORNATA[5:7]}/{AGGIORNATA[:4]}.</p>
    </div>
  </article>
</main>
<div class="barra-acquisto"><a class="primario" id="barra-agrieuro" href="#dove">Vedi su AgriEuro</a><a class="secondario" href="#dove">Altri negozi</a></div>
<footer><div class="contenitore">
  <p>OrtoCasa Help partecipa a programmi di affiliazione: se acquisti dopo aver cliccato un nostro link, il negozio ci riconosce una commissione, senza costi aggiuntivi per te. In qualità di Affiliato Amazon, OrtoCasa Help riceve un guadagno dagli acquisti idonei.</p>
  <p>Foto da <a href="https://unsplash.com/?utm_source=ortocasahelp&amp;utm_medium=referral" rel="noopener" target="_blank">Unsplash</a>. © 2026 OrtoCasa Help</p>
</div></footer>
<script src="../../negozi.js"></script>
<script src="../guida.js"></script>
</body>
</html>
"""


def main():
    for g in GUIDE:
        altre = [a for a in GUIDE if a["slug"] != g["slug"]]
        dest = RADICE / "guide" / g["slug"] / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(pagina(g, altre), encoding="utf-8")
        print("scritta", dest.relative_to(RADICE))
    urls = [f"{SITO}/"] + [f"{SITO}/guide/{g['slug']}/" for g in GUIDE]
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sitemap += [f"  <url><loc>{u}</loc><lastmod>{AGGIORNATA}</lastmod></url>" for u in urls]
    sitemap.append("</urlset>")
    (RADICE / "sitemap.xml").write_text("\n".join(sitemap) + "\n", encoding="utf-8")
    (RADICE / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITO}/sitemap.xml\n", encoding="utf-8")
    print("scritte sitemap.xml e robots.txt")


if __name__ == "__main__":
    main()
