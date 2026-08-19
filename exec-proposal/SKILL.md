---
name: exec-proposal
description: Build an enterprise-grade executive sales/service proposal from a single Markdown source, exported to branded HTML+PDF and Word — matching the real pipeline that won the TRUTH → HITSS/Telmex deal (docs/sales/telmex in speechlytics). Markdown stays the single source of truth; a project-specific config.json (colors, fonts, logo, cover copy) brands the output without touching the scripts. Use when the user wants a client-facing proposal, SOW, or executive one-pager as a polished PDF/Word pair, says "propuesta ejecutiva", "propuesta para [cliente]", "cotización formal", "SOW en Word y PDF", or references the Telmex/TRUTH proposal as the bar to match. Triggers on "/exec-proposal", "haz una propuesta como la de Telmex/TRUTH", "propuesta ejecutiva en Word y PDF".
---

# Exec Proposal

Turns a Markdown proposal into a branded, print-quality **HTML + PDF** pair and a **Word (.docx)** the client can actually edit — same visual bar as the TRUTH/HITSS/Telmex proposal (cover page, auto table of contents, styled tables, optional standalone appendices), but with the brand tokens (colors, fonts, logo, cover copy) pulled from a per-project `config.json` instead of hardcoded, so it works for any client/project without touching the scripts.

You are producing files, not a chat draft. The Markdown is the only thing you write by hand — the two build scripts (`scripts/build_html_pdf.py`, `scripts/build_docx.py`) do the rest, deterministically, from that Markdown plus `config.json`.

## Where this came from

Reverse-engineered from a real, already-proven pipeline: `docs/sales/telmex/build_propuesta.py` and `build_propuesta_docx.py` in the `speechlytics` repo, which generated the actual proposal that went out to HITSS for the Telmex Zona Oriente deal. Nothing here is invented — the CSS, the OOXML table styling, the cover-page layout, the appendix-splitting logic are all lifted from that working code and parametrized. If you ever need to sanity-check a change against the original, that folder is the reference (Markdown source `propuesta-zona-oriente.md`, its rendered HTML/PDF/DOCX outputs, and a `NOTA-INTERNA-propuesta.md` with the internal reasoning behind it).

## Workflow

1. **Find the project's brand.** Before asking the user for colors, check whether the project already has one: a `DESIGN.md`, a design-system HTML reference, brand color tokens in CSS (`--primary`, `--brand-*`), or an existing logo asset. Reuse those values in `config.json` rather than inventing new ones — the proposal should look like it came from the same company as the product. Only ask the user directly if nothing exists (brand name, primary/accent colors, logo file, fonts if they care).

2. **Write the Markdown.** This is the actual content work — read `references/proposal-outline.md` for the proven 10-section-plus-appendices shape (résumé ejecutivo, alcance, operación, SLAs, modelo económico, evolución, requerimientos, consideraciones, confidencialidad, vigencia) and adapt it to the real deal; don't force sections that don't apply. Follow the structural convention documented there: free-text header block, then the body starting at the first `## N. Título`, then optional `## Anexo X · ...` sections. Never invent numbers, SLAs, or commitments — pull real figures from what the user gives you, and flag anything you're unsure of rather than guessing a number that ends up in a contract.

3. **Fill `config.json`** from `examples/config.example.json` (the actual TRUTH values — copy the shape, replace the values). Fields that matter most:
   - `brand.name`, `brand.tagline`, `brand.logo_path` (relative to the config file's own directory).
   - `colors.primary` / `colors.accent` — everything else derives visual weight from just these two; don't over-specify a full palette unless the project already has one.
   - `cover.title_html` / `cover.title_bold_docx` — the HTML version can use inline tags (`<strong>`) and HTML entities (`&iacute;`) for accented characters; the DOCX version needs the plain-text substring that should render bold, since Word building has no HTML parser.
   - `output.anexos` — one entry per `## Anexo X` section that should also ship as its own standalone branded document (leave `[]` if none).

4. **Build.**
   ```bash
   python3 scripts/build_html_pdf.py --fuente propuesta.md --config config.json --out-dir salida/
   python3 scripts/build_docx.py     --fuente propuesta.md --config config.json --out-dir salida/
   ```
   Both need `markdown` and `python-docx` installed (`pip install markdown python-docx` if missing — check first, they're commonly already present). PDF export shells out to headless Chrome (`--headless=new --print-to-pdf`); if Chrome isn't found at a known path, the HTML/DOCX still generate, just skip the PDF and say so.

5. **Verify before delivering.** Actually open the HTML (or render it — screenshot via whatever browser tooling is available) and check: cover page reads right, the TOC lists every section, tables aren't cut off, no leftover `{placeholder}` text, no `&nbsp;`-mangled accents. Open the DOCX with `python-docx` and sanity-check paragraph/table counts are non-zero. Never hand off a proposal you haven't looked at — this is a client-facing legal-adjacent document, not a draft.

6. **Deliver.** `SendUserFile` the HTML, PDF, and DOCX (and any standalone appendix PDFs). Mention plainly that Word is the editable copy for the client's redlines and PDF/HTML are the polished send-as-is versions.

## Design notes

- **Markdown is the only editable source.** Never hand-edit the generated HTML or DOCX for a content change — edit the Markdown and rebuild. The scripts are deterministic; a hand-edit that isn't reflected in the Markdown gets silently lost on the next rebuild.
- **The DOCX converter is hand-rolled, not pandoc.** It needed control pandoc doesn't give without a reference-doc template of its own: a branded cover page, per-row table shading, a colored-folio table of contents, `keep-with-next` on headings. If a Markdown construct isn't supported (nested lists, footnotes, images inline in body text), it's a real gap in `scripts/build_docx.py`'s `bloques()` tokenizer — extend it rather than routing around it with hand-edited output.
- **Print CSS, not screen CSS.** `build_html_pdf.py`'s stylesheet is tuned for A4 + headless Chrome's print engine (`@page`, `break-before/after`, `mm` units) — it will look slightly different in a normal browser tab (fine for review) versus the actual PDF (what matters). Always check the PDF, not just the HTML preview, before delivering.
- **Self-contained output.** The logo is embedded as a base64 data URI in the HTML/PDF specifically so the PDF has zero local file dependencies once generated — keep that if you touch `data_uri()`.
- Named `exec-proposal`, not `proposal` or `telmex-proposal` — checked the catalog for collisions before installing.

## Notes

- Two output formats from one source is the entire point — never let the Markdown, the HTML/PDF, and the DOCX drift into three separately-maintained versions of the same proposal.
- Scale: designed for a single proposal document (a handful of appendices at most), not a multi-file proposal suite. For that, generate multiple Markdown sources and run the pipeline once per document.
