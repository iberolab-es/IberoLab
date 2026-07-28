#!/usr/bin/env python3
"""Replace provisional corpus.html links with the real corpus anchor."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

for relative in ("docs/historia.html", "docs/metodologia.html"):
    path = ROOT / relative
    text = path.read_text(encoding="utf-8")
    count = text.count('href="corpus.html"')
    if count == 0:
        raise RuntimeError(f"{relative}: no provisional corpus link found")
    path.write_text(text.replace('href="corpus.html"', 'href="./#corpus"'), encoding="utf-8")

validator = ROOT / "scripts" / "validate_public_site.py"
text = validator.read_text(encoding="utf-8")
old = '    require(history,("Comprender el mundo ibérico antes de intentar representarlo","Leer signos no significa traducir el idioma","Una sección preparada para crecer con YouTube","Monedas e inscripciones",\'href="academia.html"\'),"history")\n    require(method,("No traduce el español al idioma ibérico","Dos audios con alcances distintos","Lectura aproximada","No es un signo ibérico arqueológico","Trazabilidad técnica",\'href="privacidad.html"\'),"methodology")'
new = '    require(history,("Comprender el mundo ibérico antes de intentar representarlo","Leer signos no significa traducir el idioma","Una sección preparada para crecer con YouTube","Monedas e inscripciones",\'href="./#corpus"\',\'href="academia.html"\'),"history")\n    require(method,("No traduce el español al idioma ibérico","Dos audios con alcances distintos","Lectura aproximada","No es un signo ibérico arqueológico","Trazabilidad técnica",\'href="./#corpus"\',\'href="privacidad.html"\'),"methodology")\n    if \'href="corpus.html"\' in history or \'href="corpus.html"\' in method: raise ValueError("provisional corpus.html link remains in public pages")'
if old not in text:
    raise RuntimeError("public-site validator anchor not found")
validator.write_text(text.replace(old, new, 1), encoding="utf-8")
print("Public corpus links corrected.")
