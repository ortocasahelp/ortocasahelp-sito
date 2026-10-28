"""Genera il logo dell'app (O con germogli, il vuoto della O a forma di casa) e le icone PNG.

Uso:  python3 strumenti/icone.py [forma]
Forme della casa: classica (predefinita), camino, baita, porta. Scrive icone/logo.svg,
icone/logo-maskable.svg, icone/favicon.svg e i PNG (192, 512, maskable 512, Apple 180, favicon 48),
renderizzati con Chromium (Playwright) e il font Comfortaa di fonts.css.
"""
import pathlib
import sys

RADICE = pathlib.Path(__file__).resolve().parent.parent
ICONE = RADICE / "icone"

# Casa ritagliata nel vuoto della O (anello: centro 256,300, raggio esterno 147, interno 85).
FORME = {
    "classica": '<path d="M256 226 L318 276 L318 352 Q318 362 308 362 L204 362 Q194 362 194 352 L194 276 Z" fill="#000" stroke="#000" stroke-width="14" stroke-linejoin="round"/>',
    "camino": '<path d="M256 228 L290 255 L290 236 L308 236 L308 270 L320 280 L320 352 Q320 362 310 362 L202 362 Q192 362 192 352 L192 280 Z" fill="#000" stroke="#000" stroke-width="12" stroke-linejoin="round"/>',
    "baita": '<path d="M256 214 L314 292 L314 356 Q314 364 306 364 L206 364 Q198 364 198 356 L198 292 Z" fill="#000" stroke="#000" stroke-width="12" stroke-linejoin="round"/>',
    "porta": '<path d="M256 226 L318 276 L318 352 Q318 362 308 362 L204 362 Q194 362 194 352 L194 276 Z" fill="#000" stroke="#000" stroke-width="14" stroke-linejoin="round"/>'
             '<path d="M240 369 L240 330 A16 16 0 0 1 272 330 L272 369 Z" fill="#fff"/>',
}

DEFS = ('<linearGradient id="{p}bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#4B2A73"/><stop offset="1" stop-color="#22102F"/></linearGradient>'
        '<linearGradient id="{p}or" x1="0.2" y1="0" x2="0.8" y2="1"><stop offset="0" stop-color="#FFB14A"/><stop offset=".55" stop-color="#F07F1A"/><stop offset="1" stop-color="#D9580B"/></linearGradient>'
        '<linearGradient id="{p}lf" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E2F79A"/><stop offset="1" stop-color="#A9D63E"/></linearGradient>'
        '<filter id="{p}sh" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="#000" flood-opacity=".35"/></filter>'
        '<mask id="{p}buco" maskUnits="userSpaceOnUse" x="0" y="0" width="512" height="512"><rect width="512" height="512" fill="#000"/>'
        '<circle cx="256" cy="300" r="147" fill="#fff"/>{casa}</mask>')
SEGNO = ('<g filter="url(#{p}sh)"><rect x="100" y="140" width="312" height="320" fill="url(#{p}or)" mask="url(#{p}buco)"/>'
         '<path d="M256 186 V138" stroke="url(#{p}lf)" stroke-width="16" stroke-linecap="round"/>'
         '<path d="M252 152 C230 104 184 80 136 88 C142 138 190 168 252 152 Z" fill="url(#{p}lf)"/>'
         '<path d="M260 152 C282 104 328 80 376 88 C370 138 322 168 260 152 Z" fill="url(#{p}lf)"/></g>'
         '<path d="M150 262 A116 116 0 0 1 220 186" fill="none" stroke="#fff" stroke-width="10" stroke-linecap="round" opacity=".28"/>')
TESTO = '<text x="256" y="{y}" text-anchor="middle" font-family="Comfortaa, Trebuchet MS, sans-serif" font-weight="700" font-size="{fs}" fill="#FFFFFF" letter-spacing="2">Help</text>'


def svg(forma="classica", tipo="icona", p="oc-"):
    defs = DEFS.format(p=p, casa=FORME[forma])
    segno = SEGNO.format(p=p)
    if tipo == "icona":
        corpo = f'<rect width="512" height="512" rx="112" fill="url(#{p}bg)"/><g transform="translate(256 205) scale(0.8) translate(-256 -265)">{segno}</g>' + TESTO.format(y=470, fs=84)
    elif tipo == "maskable":
        corpo = f'<rect width="512" height="512" fill="url(#{p}bg)"/><g transform="translate(256 215) scale(0.62) translate(-256 -265)">{segno}</g>' + TESTO.format(y=430, fs=66)
    else:  # favicon: senza scritta, segno grande
        corpo = f'<rect width="512" height="512" rx="112" fill="url(#{p}bg)"/><g transform="translate(256 262) scale(0.98) translate(-256 -265)">{segno}</g>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><defs>{defs}</defs>{corpo}</svg>\n'


def scrivi_png(lavori):
    from playwright.sync_api import sync_playwright
    fonts = (RADICE / "fonts.css").as_uri()
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for sorgente, lato, uscita, trasparente in lavori:
            codice = sorgente.read_text().replace("<svg ", f'<svg width="{lato}" height="{lato}" style="display:block" ', 1)
            tmp = ICONE / "_tmp.html"
            tmp.write_text(f'<html><head><link rel="stylesheet" href="{fonts}"></head><body style="margin:0;background:transparent">{codice}</body></html>')
            pagina = browser.new_page(viewport={"width": lato, "height": lato})
            pagina.goto(tmp.as_uri())
            pagina.evaluate("document.fonts.ready")
            pagina.wait_for_timeout(300)
            pagina.screenshot(path=str(ICONE / uscita), omit_background=trasparente)
            pagina.close()
            tmp.unlink()
        browser.close()


def main():
    forma = sys.argv[1] if len(sys.argv) > 1 else "classica"
    if forma not in FORME:
        sys.exit(f"Forma sconosciuta: {forma}. Disponibili: {', '.join(FORME)}")
    (ICONE / "logo.svg").write_text(svg(forma, "icona"))
    (ICONE / "logo-maskable.svg").write_text(svg(forma, "maskable"))
    (ICONE / "favicon.svg").write_text(svg(forma, "favicon"))
    scrivi_png([
        (ICONE / "logo.svg", 192, "icona-192.png", True),
        (ICONE / "logo.svg", 512, "icona-512.png", True),
        (ICONE / "logo-maskable.svg", 512, "icona-maskable-512.png", False),
        (ICONE / "logo-maskable.svg", 180, "apple-touch-icon.png", False),
        (ICONE / "favicon.svg", 48, "favicon-48.png", True),
    ])
    print(f"icone generate con la casa '{forma}'")


if __name__ == "__main__":
    main()
