#!/usr/bin/env python3
"""Insert the MVP call-to-action into the existing attested-corpus page."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "index.html"
MARKER = "data-mvp-callout"

text = PAGE.read_text(encoding="utf-8")
if MARKER in text:
    print("MVP callout already present")
    raise SystemExit(0)

old_lead = (
    '<p class="lead">Primero reconstruimos lecturas documentadas y explicamos su evidencia. '
    'El motor para palabras modernas permanecerá bloqueado hasta consolidar este corpus y sus signos.</p>'
)
new_lead = (
    '<p class="lead">Esta página conserva el corpus documentado y su evidencia. '
    'Para nombres, palabras y frases modernas breves existe un demostrador separado, '
    'siempre etiquetado como adaptación fonética experimental.</p>'
)
if old_lead not in text:
    raise RuntimeError("Expected corpus lead paragraph was not found")
text = text.replace(old_lead, new_lead, 1)

css = """
    .mvp-callout {
      margin: 20px 0;
      border: 1px solid color-mix(in srgb, var(--accent) 65%, var(--line));
      background: linear-gradient(135deg, rgba(53,167,255,.14), rgba(25,98,196,.08));
      border-radius: 20px;
      padding: 18px;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 14px;
    }
    .mvp-callout strong { display: block; font-size: 1.05rem; }
    .mvp-callout span { display: block; margin-top: 5px; color: var(--muted); line-height: 1.5; }
    .mvp-callout a {
      display: inline-flex;
      align-items: center;
      min-height: 44px;
      padding: 0 16px;
      border-radius: 13px;
      background: linear-gradient(135deg, var(--accent), var(--accent-2));
      color: white;
      text-decoration: none;
      font-weight: 850;
    }
"""
text = text.replace("  </style>", css + "  </style>", 1)

header_end = "  </header>"
callout = """

  <section class="mvp-callout" data-mvp-callout aria-label="Demostrador para palabras modernas">
    <div>
      <strong>¿Quieres representar un nombre o una frase breve?</strong>
      <span>Prueba el demostrador con ejemplos como amor, familia o te quiero. Las aproximaciones se explican y nunca se presentan como traducción.</span>
    </div>
    <a href="convertir.html">Abrir demostrador MVP</a>
  </section>"""
if header_end not in text:
    raise RuntimeError("Header closing tag was not found")
text = text.replace(header_end, header_end + callout, 1)

PAGE.write_text(text, encoding="utf-8")
print("Inserted the MVP callout into docs/index.html")
