#!/usr/bin/env python3
"""
Construye una propuesta ejecutiva: Markdown editable -> HTML con marca del proyecto -> PDF.

El Markdown es la fuente. Este script no inventa contenido: sólo lo viste, usando los
tokens de marca de `config.json` (ver config.example.json en esta misma skill).

    python3 build_html_pdf.py --fuente propuesta.md --config config.json --out-dir salida/
    python3 build_html_pdf.py --fuente propuesta.md --config config.json --out-dir salida/ --no-pdf

Convención del Markdown fuente (documentada en references/proposal-outline.md):
  - Puede empezar con un bloque de título/meta libre; el cuerpo real arranca en el
    primer encabezado "## N. Título" (numerado). Todo lo anterior a ese encabezado
    se recorta: la portada generada lo reemplaza.
  - Un anexo opcional es cualquier "## Anexo X · ..." — se puede extraer como
    documento independiente (con su propia portada) vía `output.anexos` en config.json.

Generalizado a partir del script real usado en TRUTH/Telmex
(docs/sales/telmex/build_propuesta.py, speechlytics) — misma calidad, marca parametrizada.
"""

from __future__ import annotations

import argparse
import base64
import json
import re
import subprocess
import sys
from pathlib import Path

import markdown

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium-browser",
    "/usr/bin/chromium",
]


def chrome_binary() -> str | None:
    for c in CHROME_CANDIDATES:
        if Path(c).exists():
            return c
    return None


def cargar_config(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def css_desde_config(cfg: dict) -> str:
    c = cfg["colors"]
    f = cfg["fonts"]
    len_meta = max(len(cfg.get("cover", {}).get("meta", [])), 1)
    return f"""
:root {{
  --bg: {c['bg']};
  --surface: {c['surface']};
  --surface-2: {c['surface_2']};
  --pale-primary: {c.get('pale_primary', c['surface'])};
  --pale-info: {c.get('pale_info', c['surface'])};
  --pale-accent: {c.get('pale_accent', c['surface'])};
  --border: {c['border']};
  --hairline: {c['hairline']};

  --text: {c['text']};
  --text-paper: {c['text_paper']};
  --text-dim: {c['text_dim']};
  --muted: {c['muted']};

  --accent: {c['accent']};   /* hallazgo, taxonomia. nunca accion primaria */
  --primary: {c['primary']}; /* color de marca principal */
  --info: {c['info']};       /* dato y metrica */
  --dark: {c['dark']};       /* seguridad y privacidad, bloques de codigo */

  --font-display: '{f['display']}', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-body: '{f['body']}', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', sans-serif;
  --font-mono: '{f['mono']}', 'SF Mono', Menlo, monospace;
}}

* {{ margin: 0; padding: 0; box-sizing: border-box; }}

html {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}

body {{
  background: var(--bg);
  color: var(--text);
  font-family: var(--font-body);
  font-size: 10.2pt;
  line-height: 1.62;
  font-weight: 400;
  -webkit-font-smoothing: antialiased;
}}

.page {{
  max-width: 190mm;
  margin: 0 auto;
  padding: 14mm 0 20mm;
}}

/* ---------- portada ---------- */

.cover {{
  break-after: page;
  page-break-after: always;
  min-height: 245mm;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 8mm 0 10mm;
}}

.cover-mark {{
  font-family: var(--font-display);
  font-weight: 700;
  font-size: 15pt;
  letter-spacing: 0.26em;
  color: var(--primary);
}}

.cover-mark span {{ color: var(--accent); }}

.cover-rule {{
  height: 3px;
  width: 64px;
  background: var(--accent);
  margin: 6mm 0 0;
}}

.cover-kicker {{
  font-family: var(--font-mono);
  font-size: 8pt;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--text-dim);
  margin-bottom: 5mm;
}}

.cover-title {{
  font-family: var(--font-display);
  font-size: 34pt;
  line-height: 1.06;
  font-weight: 500;
  color: var(--text-paper);
  letter-spacing: -0.02em;
  max-width: 150mm;
}}

.cover-title strong {{ font-weight: 700; color: var(--primary); }}

.cover-sub {{
  font-size: 12pt;
  color: var(--text-dim);
  margin-top: 6mm;
  max-width: 130mm;
  line-height: 1.5;
}}

.cover-meta {{
  border-top: 1px solid var(--hairline);
  padding-top: 5mm;
  display: grid;
  grid-template-columns: repeat({len_meta}, 1fr);
  gap: 6mm;
}}

.cover-meta div {{ font-size: 8.4pt; }}

.cover-meta dt {{
  font-family: var(--font-mono);
  font-size: 7pt;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--muted);
  margin-bottom: 1.4mm;
}}

.cover-meta dd {{ color: var(--text-paper); font-weight: 500; }}

.cover-firma {{
  border-top: 1px solid var(--hairline);
  padding-top: 5mm;
  margin-top: 6mm;
  display: flex;
  align-items: center;
  gap: 7mm;
}}

.cover-logo {{ height: 7.5mm; width: auto; }}

.cover-firma p {{
  margin: 0;
  font-size: 8pt;
  color: var(--text-dim);
  line-height: 1.5;
}}

.cover-firma strong {{ color: var(--text-paper); font-weight: 600; }}

/* ---------- indice ---------- */

.toc {{
  break-after: page;
  page-break-after: always;
  padding-top: 4mm;
}}

.toc h2 {{
  break-before: auto;
  page-break-before: auto;
  margin-top: 0;
}}

.toc ol {{ list-style: none; margin: 6mm 0 0; }}

.toc li {{
  padding: 2.6mm 0;
  border-bottom: 1px solid var(--border);
  font-size: 10.4pt;
  color: var(--text-paper);
  display: flex;
  gap: 6mm;
  align-items: baseline;
}}

.toc .toc-n {{
  font-family: var(--font-mono);
  font-size: 8.4pt;
  color: var(--accent);
  min-width: 8mm;
  font-weight: 500;
}}

.toc .toc-anexo {{
  color: var(--text-dim);
  padding-left: 14mm;
  font-size: 9.6pt;
}}

/* ---------- jerarquia ---------- */

h1 {{
  font-family: var(--font-display);
  font-size: 20pt;
  font-weight: 600;
  color: var(--primary);
  letter-spacing: -0.015em;
  margin: 0 0 4mm;
}}

h2 {{
  font-family: var(--font-display);
  font-size: 15pt;
  font-weight: 600;
  color: var(--text-paper);
  letter-spacing: -0.012em;
  margin: 12mm 0 4mm;
  padding-top: 4mm;
  border-top: 2px solid var(--primary);
  break-after: avoid;
  page-break-after: avoid;
  break-inside: avoid;
}}

h2:first-of-type {{ margin-top: 0; }}

h3 {{
  font-family: var(--font-display);
  font-size: 11.4pt;
  font-weight: 600;
  color: var(--primary);
  margin: 7mm 0 2.5mm;
  break-after: avoid;
  page-break-after: avoid;
}}

h4 {{
  font-family: var(--font-body);
  font-size: 10pt;
  font-weight: 600;
  color: var(--text-paper);
  margin: 5mm 0 2mm;
  break-after: avoid;
}}

p {{ margin: 0 0 3.2mm; }}

strong {{ font-weight: 600; color: var(--text-paper); }}

a {{ color: var(--info); text-decoration: none; }}

ul, ol {{ margin: 0 0 3.6mm 5mm; }}
li {{ margin-bottom: 1.6mm; }}
li::marker {{ color: var(--accent); }}

hr {{
  border: 0;
  border-top: 1px solid var(--hairline);
  margin: 7mm 0;
}}

/* ---------- tablas ---------- */

table {{
  width: 100%;
  border-collapse: collapse;
  margin: 4mm 0 6mm;
  font-size: 8.8pt;
  break-inside: avoid;
  page-break-inside: avoid;
}}

thead {{ background: var(--primary); }}

th {{
  color: #ffffff;
  font-family: var(--font-body);
  font-weight: 600;
  font-size: 8pt;
  letter-spacing: 0.02em;
  text-align: left;
  padding: 2.4mm 2.6mm;
  vertical-align: bottom;
}}

td {{
  padding: 2.2mm 2.6mm;
  border-bottom: 1px solid var(--border);
  vertical-align: top;
  line-height: 1.45;
}}

tbody tr:nth-child(even) {{ background: var(--surface); }}

th[align="right"], td[align="right"] {{ text-align: right; }}
th[align="center"], td[align="center"] {{ text-align: center; }}

td strong {{ color: var(--primary); }}

td[align="right"] {{ font-family: var(--font-mono); font-size: 8.4pt; }}

/* ---------- citas y bloques ---------- */

blockquote {{
  background: var(--pale-primary);
  border-left: 3px solid var(--primary);
  padding: 4mm 5mm;
  margin: 4mm 0 5mm;
  font-size: 9.4pt;
  break-inside: avoid;
  page-break-inside: avoid;
}}

blockquote p {{ margin-bottom: 2.4mm; }}
blockquote p:last-child {{ margin-bottom: 0; }}
blockquote strong {{ color: var(--primary); }}

pre {{
  background: var(--dark);
  color: #e8eef5;
  padding: 4mm 5mm;
  border-radius: 2px;
  font-family: var(--font-mono);
  font-size: 8.4pt;
  line-height: 1.6;
  overflow-x: auto;
  margin: 4mm 0 5mm;
  break-inside: avoid;
  page-break-inside: avoid;
}}

code {{
  font-family: var(--font-mono);
  font-size: 0.92em;
  background: var(--surface-2);
  padding: 0.4mm 1.2mm;
  border-radius: 2px;
}}

pre code {{ background: none; padding: 0; color: inherit; font-size: 1em; }}

em {{ color: var(--text-dim); }}

/* ---------- impresion ---------- */

@page {{
  size: A4;
  margin: 14mm 12mm 14mm 12mm;
}}

@media print {{
  .page {{ max-width: none; padding: 0; }}
  h2 {{ break-before: page; page-break-before: always; }}
  h2:first-of-type {{ break-before: auto; page-break-before: auto; }}
  .cover {{ min-height: 250mm; }}
}}
"""


PLANTILLA = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{titulo}</title>
<link rel="preconnect" href="https://fonts.googleapis.com" crossorigin />
<link rel="stylesheet" href="{google_fonts_url}" />
<style>{css}</style>
</head>
<body>
<div class="page">
{portada}
{cuerpo}
</div>
</body>
</html>
"""

PORTADA = """<section class="cover">
  <div>
    <div class="cover-mark">{brand_name}<span>{brand_suffix}</span></div>
    <div class="cover-rule"></div>
  </div>
  <div>
    <div class="cover-kicker">{kicker}</div>
    <h1 class="cover-title">{title_html}</h1>
    <p class="cover-sub">{subtitle}</p>
  </div>
  <dl class="cover-meta">
{meta_html}
  </dl>
  <div class="cover-firma">
    {logo_html}
    <p>{tagline_html}</p>
  </div>
</section>
"""


def data_uri(path: Path) -> str:
    """Empotra un binario en el HTML. El PDF sale autocontenido, sin rutas locales."""
    tipo = {".png": "image/png", ".svg": "image/svg+xml", ".jpg": "image/jpeg", ".jpeg": "image/jpeg"}[path.suffix.lower()]
    return f"data:{tipo};base64,{base64.b64encode(path.read_bytes()).decode()}"


def meta_html_de(meta: list[list[str]]) -> str:
    filas = []
    for rotulo, valor in meta:
        filas.append(f"    <div><dt>{rotulo}</dt><dd>{valor}</dd></div>")
    return "\n".join(filas)


def portada_html(cfg: dict, kicker: str, title_html: str, subtitle: str, root: Path) -> str:
    brand = cfg["brand"]
    logo_path = root / brand["logo_path"] if brand.get("logo_path") else None
    logo_html = f'<img class="cover-logo" src="{data_uri(logo_path)}" alt="{brand["name"]}" />' if logo_path and logo_path.exists() else ""
    return PORTADA.format(
        brand_name=brand["name"],
        brand_suffix=brand.get("name_accent_suffix", ""),
        kicker=kicker,
        title_html=title_html,
        subtitle=subtitle,
        meta_html=meta_html_de(cfg["cover"]["meta"] if "meta" in cfg["cover"] else []),
        logo_html=logo_html,
        tagline_html=brand.get("tagline_html", brand.get("tagline", "")),
    )


def primer_encabezado_numerado(md: str) -> int:
    """Índice donde empieza el cuerpo real: el primer '## N. Título'. -1 si no hay."""
    m = re.search(r"^## \d+\.\s", md, flags=re.MULTILINE)
    return m.start() if m else -1


def recortar_encabezado(md: str) -> str:
    """Quita el bloque de titulo/metadatos libre del Markdown: eso lo reemplaza la portada."""
    i = primer_encabezado_numerado(md)
    return md if i == -1 else md[i:]


def extraer_seccion(md: str, heading_prefix: str) -> str:
    """Recorta desde `heading_prefix` (p.ej. '## Anexo A') hasta el siguiente '## ' o EOF."""
    m = re.search(r"^" + re.escape(heading_prefix), md, flags=re.MULTILINE)
    if not m:
        raise ValueError(f"No se encontró la sección que empieza con {heading_prefix!r}")
    resto = md[m.end():]
    sig = re.search(r"^## ", resto, flags=re.MULTILINE)
    cuerpo = resto[: sig.start()] if sig else resto
    return (md[m.start():m.start() + (m.end() - m.start())] + cuerpo).rstrip().removesuffix("---").rstrip() + "\n"


def tabla_de_contenido(md: str) -> str:
    """Indice a partir de los H2 del Markdown. Sin folios: Chrome no numera paginas."""
    titulos = re.findall(r"^## (.+)$", md, flags=re.MULTILINE)
    filas = []
    for t in titulos:
        t = t.strip()
        m = re.match(r"^(\d+)\.\s+(.*)$", t)
        if m:
            filas.append(f'<li><span class="toc-n">{m.group(1)}</span>{m.group(2)}</li>')
        else:
            filas.append(f'<li class="toc-anexo">{t}</li>')
    return (
        '<section class="toc">\n'
        "  <h2>Contenido</h2>\n"
        "  <ol>\n    " + "\n    ".join(filas) + "\n  </ol>\n</section>\n"
    )


def alinear_numeros(html: str) -> str:
    """python-markdown emite style="text-align: right"; lo pasamos a atributo align."""
    html = re.sub(r'\s*style="text-align:\s*right;?"', ' align="right"', html)
    html = re.sub(r'\s*style="text-align:\s*center;?"', ' align="center"', html)
    html = re.sub(r'\s*style="text-align:\s*left;?"', "", html)
    return html


def render_md(md_texto: str) -> str:
    html = markdown.markdown(md_texto, extensions=["tables", "fenced_code", "sane_lists", "attr_list"])
    return alinear_numeros(html)


def construir_documento(cfg: dict, root: Path, cuerpo_md: str, titulo: str, kicker: str, title_html: str, subtitle: str, con_toc: bool) -> str:
    cuerpo = render_md(cuerpo_md)
    css = css_desde_config(cfg)
    portada = portada_html(cfg, kicker, title_html, subtitle, root)
    if con_toc:
        portada += tabla_de_contenido(cuerpo_md)
    return PLANTILLA.format(
        titulo=titulo,
        google_fonts_url=cfg["fonts"]["google_fonts_url"],
        css=css,
        portada=portada,
        cuerpo=cuerpo,
    )


def a_pdf(html_path: Path, pdf_path: Path) -> bool:
    chrome = chrome_binary()
    if not chrome:
        print("  ! Chrome no encontrado en ninguna ruta conocida; se omite el PDF", file=sys.stderr)
        return False
    cmd = [
        chrome,
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        "--virtual-time-budget=12000",
        f"--print-to-pdf={pdf_path}",
        html_path.as_uri(),
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    if res.returncode != 0 or not pdf_path.exists():
        print(res.stderr[-1500:], file=sys.stderr)
        return False
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--fuente", type=Path, required=True, help="Markdown fuente de la propuesta")
    ap.add_argument("--config", type=Path, required=True, help="config.json con marca/colores/portada")
    ap.add_argument("--out-dir", type=Path, required=True, help="carpeta de salida")
    ap.add_argument("--no-pdf", action="store_true", help="sólo genera el HTML")
    args = ap.parse_args()
    args.fuente = args.fuente.resolve()
    args.config = args.config.resolve()
    args.out_dir = args.out_dir.resolve()

    if not args.fuente.exists():
        print(f"No existe {args.fuente}", file=sys.stderr)
        return 1
    cfg = cargar_config(args.config)
    root = args.config.parent
    args.out_dir.mkdir(parents=True, exist_ok=True)

    md_texto = args.fuente.read_text(encoding="utf-8")
    salida = cfg["output"]

    documentos = [{
        "base_name": salida["base_name"],
        "html_title": salida["html_title"],
        "cuerpo_md": recortar_encabezado(md_texto),
        "kicker": cfg["cover"]["kicker"],
        "title_html": cfg["cover"]["title_html"],
        "subtitle": cfg["cover"]["subtitle"],
        "con_toc": True,
    }]
    for anexo in salida.get("anexos", []):
        documentos.append({
            "base_name": anexo["base_name"],
            "html_title": anexo["html_title"],
            "cuerpo_md": extraer_seccion(md_texto, anexo["heading_prefix"]),
            "kicker": anexo["cover_kicker"],
            "title_html": anexo["cover_title_html"],
            "subtitle": anexo["cover_subtitle"],
            "con_toc": False,
        })

    fallo = False
    for doc in documentos:
        html_path = args.out_dir / f"{doc['base_name']}.html"
        pdf_path = args.out_dir / f"{doc['base_name']}.pdf"
        html = construir_documento(cfg, root, doc["cuerpo_md"], doc["html_title"], doc["kicker"], doc["title_html"], doc["subtitle"], doc["con_toc"])
        html_path.write_text(html, encoding="utf-8")
        print(f"  HTML  {html_path.name}  ({html_path.stat().st_size / 1024:.0f} KB)")
        if args.no_pdf:
            continue
        if a_pdf(html_path, pdf_path):
            print(f"  PDF   {pdf_path.name}  ({pdf_path.stat().st_size / 1024:.0f} KB)")
        else:
            print(f"  ! no se genero {pdf_path.name}", file=sys.stderr)
            fallo = True
    return 1 if fallo else 0


if __name__ == "__main__":
    raise SystemExit(main())
