#!/usr/bin/env python3
"""Finalize public metadata, documentation and validation wiring."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def replace(path: str, old: str, new: str, expected: int = 1) -> None:
    target = ROOT / path
    text = target.read_text(encoding="utf-8")
    count = text.count(old)
    if count != expected:
        raise RuntimeError(f"{path}: expected {expected} occurrence(s), found {count}: {old!r}")
    target.write_text(text.replace(old, new), encoding="utf-8")


# Use PNG for reliable social previews while preserving SVG for the on-page mark.
for path in ("docs/index.html", "docs/convertir.html", "docs/academia.html"):
    target = ROOT / path
    text = target.read_text(encoding="utf-8")
    text = text.replace("assets/brand/iberolab-social-card.svg", "assets/brand/iberolab-social-card.png")
    icon = '  <link rel="icon" href="assets/brand/iberolab-mark.svg" type="image/svg+xml">'
    if 'rel="apple-touch-icon"' not in text:
        if icon not in text:
            raise RuntimeError(f"{path}: icon marker missing")
        text = text.replace(icon, icon + '\n  <link rel="apple-touch-icon" href="assets/brand/iberolab-mark-512.png">', 1)
    card = '  <meta name="twitter:card" content="summary_large_image">'
    if 'name="twitter:image"' not in text:
        if card not in text:
            raise RuntimeError(f"{path}: twitter card marker missing")
        text = text.replace(card, card + '\n  <meta name="twitter:image" content="https://iberolab-es.github.io/IberoLab/assets/brand/iberolab-social-card.png">', 1)
    target.write_text(text, encoding="utf-8")

# Manifest includes scalable and installable PNG icons.
manifest_path = ROOT / "docs" / "site.webmanifest"
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
manifest["icons"] = [
    {
        "src": "assets/brand/iberolab-mark.svg",
        "sizes": "any",
        "type": "image/svg+xml",
        "purpose": "any maskable",
    },
    {
        "src": "assets/brand/iberolab-mark-512.png",
        "sizes": "512x512",
        "type": "image/png",
        "purpose": "any maskable",
    },
]
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# Repository presentation and removal of the remaining personal-name example.
replace(
    "README.md",
    "# IberoLab\n\n**Proyecto abierto y experimental",
    '# IberoLab\n\n<p align="center"><img src="docs/assets/brand/iberolab-mark.svg" alt="Símbolo de IberoLab" width="112"></p>\n\n**Proyecto abierto y experimental',
)
replace(
    "README.md",
    "algo como `Lara`, `amor`, `familia` o `te quiero`",
    "algo como `amor`, `familia`, `hogar` o `te quiero`",
)
replace(
    "README.md",
    "- Corpus y renderizador documentado: <https://iberolab-es.github.io/IberoLab/>\n",
    "- Corpus y renderizador documentado: <https://iberolab-es.github.io/IberoLab/>\n- Información para universidades y especialistas: <https://iberolab-es.github.io/IberoLab/academia.html>\n",
)

# Add public presence to the ordinary read-only CI.
replace(
    ".github/workflows/validate.yml",
    "      - name: Validate practical short-input MVP converter\n        run: python scripts/validate_mvp_converter.py",
    "      - name: Validate practical short-input MVP converter\n        run: python scripts/validate_mvp_converter.py\n\n      - name: Validate public identity and academic presence\n        run: python scripts/validate_public_presence.py",
)

# Ensure personal examples cannot reappear in active public files.
validator = ROOT / "scripts" / "validate_public_presence.py"
text = validator.read_text(encoding="utf-8")
anchor = '    outreach = (ROOT / "OUTREACH.md").read_text(encoding="utf-8")\n'
if anchor not in text:
    raise RuntimeError("public validator anchor missing")
insert = '''    active_public = "\\n".join(
        (ROOT / path).read_text(encoding="utf-8")
        for path in ("README.md", "docs/index.html", "docs/convertir.html", "docs/academia.html")
    )
    for personal_example in ("Lara", "Cris"):
        if personal_example in active_public:
            fail(f"personal example remains in active public content: {personal_example}")

'''
text = text.replace(anchor, insert + anchor, 1)
validator.write_text(text, encoding="utf-8")

print("Public presence finalized.")
