#!/usr/bin/env python3
"""Validate coverage of the provisional reference renderer."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "data" / "corpus" / "attested-forms.v1.json"
MAPPING = ROOT / "data" / "signs" / "reference-standard-dual.v1.json"


def main() -> int:
    corpus = json.loads(CORPUS.read_text(encoding="utf-8"))
    mapping = json.loads(MAPPING.read_text(encoding="utf-8"))
    signs = {item["token"]: item for item in mapping["signs"]}
    used = {token for form in corpus["forms"] for token in form["grapheme_sequence"]}
    missing = sorted(used - signs.keys())
    if missing:
        raise ValueError(f"Tokens absent from renderer mapping: {missing}")

    available = 0
    unresolved = []
    for token in sorted(used):
        item = signs[token]
        status = item.get("graphic_status")
        if status == "reference_svg_available":
            name = item.get("file_name")
            if not name or not name.endswith(".svg"):
                raise ValueError(f"{token!r}: invalid SVG filename")
            available += 1
        elif status and status.startswith("pending_"):
            unresolved.append(token)
        else:
            raise ValueError(f"{token!r}: unknown graphic status {status!r}")

    html = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    required_markers = ["renderForm", "glyph-fallback", "DOMContentLoaded"]
    absent_markers = [marker for marker in required_markers if marker not in html]
    if absent_markers:
        raise ValueError(f"HTML lacks required safeguards: {absent_markers}")

    print(
        "RENDERER VALIDATION OK: "
        f"{len(corpus['forms'])} forms; {available} SVG mappings; "
        f"{len(unresolved)} explicit unresolved token(s): {', '.join(unresolved) or 'none'}."
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, json.JSONDecodeError, KeyError, ValueError) as exc:
        print(f"RENDERER VALIDATION FAILED: {exc}", file=sys.stderr)
        raise SystemExit(1)
