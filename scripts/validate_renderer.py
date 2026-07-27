#!/usr/bin/env python3
"""Validate coverage and public safeguards of the provisional renderer."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "data" / "corpus" / "attested-forms.v1.json"
MAPPING = ROOT / "data" / "signs" / "reference-standard-dual.v1.json"
HTML = ROOT / "docs" / "index.html"


def main() -> int:
    corpus = json.loads(CORPUS.read_text(encoding="utf-8"))
    mapping = json.loads(MAPPING.read_text(encoding="utf-8"))
    signs = {item["token"]: item for item in mapping["signs"]}
    used = {token for form in corpus["forms"] for token in form["grapheme_sequence"]}

    missing = sorted(used - signs.keys())
    if missing:
        raise ValueError(f"Tokens absent from renderer mapping: {missing}")

    available = 0
    unresolved: list[str] = []
    for token in sorted(used):
        item = signs[token]
        status = item.get("graphic_status")
        if status == "local_reference_svg_available":
            local_path = item.get("local_path")
            if not isinstance(local_path, str) or not local_path.endswith(".svg"):
                raise ValueError(f"{token!r}: invalid local SVG path")
            if not local_path.startswith("docs/assets/signs/northeastern-dual/"):
                raise ValueError(f"{token!r}: local SVG path is outside the controlled asset directory")
            if not (ROOT / local_path).is_file():
                raise ValueError(f"{token!r}: local SVG does not exist")
            available += 1
        elif status and status.startswith("pending_"):
            unresolved.append(token)
        else:
            raise ValueError(f"{token!r}: unknown graphic status {status!r}")

    html = HTML.read_text(encoding="utf-8")
    required_markers = [
        "renderForm",
        "glyph-fallback",
        "DOMContentLoaded",
        "sourceLink",
        "evidenceText",
        "transcriptionNote",
        "previousButton",
        "nextButton",
        "hashchange",
        "rendererReady",
        "No es una traducción al idioma ibérico",
        "Referencia normalizada",
        "Recursos gráficos locales de referencia",
    ]
    absent = [marker for marker in required_markers if marker not in html]
    if absent:
        raise ValueError(f"HTML lacks required safeguards: {absent}")

    if "Special:Redirect/file" in html or "COMMONS_REDIRECT" in html:
        raise ValueError("public renderer still contains a remote SVG dependency")

    absent_forms = [item["id"] for item in corpus["forms"] if item["id"] not in html]
    if absent_forms:
        raise ValueError(f"HTML lacks corpus entries: {absent_forms}")

    if unresolved != ["ń"]:
        raise ValueError(f"expected only explicit unresolved token ń, got {unresolved}")

    print(
        "RENDERER VALIDATION OK: "
        f"{len(corpus['forms'])} forms; {available} local SVG mappings; "
        f"{len(unresolved)} explicit unresolved token(s): "
        f"{', '.join(unresolved) or 'none'}; evidence, navigation and local-only delivery safeguards present."
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, json.JSONDecodeError, KeyError, ValueError) as exc:
        print(f"RENDERER VALIDATION FAILED: {exc}", file=sys.stderr)
        raise SystemExit(1)
