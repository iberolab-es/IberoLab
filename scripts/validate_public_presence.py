#!/usr/bin/env python3
"""Validate IberoLab public identity, academic presentation and discoverability."""
from __future__ import annotations

import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

REQUIRED_FILES = (
    ROOT / "CITATION.cff",
    ROOT / "OUTREACH.md",
    DOCS / "academia.html",
    DOCS / "privacidad.html",
    DOCS / "robots.txt",
    DOCS / "sitemap.xml",
    DOCS / "site.webmanifest",
    DOCS / "assets" / "brand" / "iberolab-mark.svg",
    DOCS / "assets" / "brand" / "iberolab-mark-512.png",
    DOCS / "assets" / "brand" / "iberolab-social-card.svg",
    DOCS / "assets" / "brand" / "iberolab-social-card.png",
)


def fail(message: str) -> None:
    raise ValueError(message)


def require(text: str, markers: tuple[str, ...], label: str) -> None:
    for marker in markers:
        if marker not in text:
            fail(f"{label} lacks required marker {marker!r}")


def validate() -> tuple[int, int]:
    for path in REQUIRED_FILES:
        if not path.is_file() or path.stat().st_size == 0:
            fail(f"required public file is missing or empty: {path.relative_to(ROOT)}")

    mark_svg = DOCS / "assets" / "brand" / "iberolab-mark.svg"
    social_svg = DOCS / "assets" / "brand" / "iberolab-social-card.svg"
    for path in (mark_svg, social_svg):
        root = ET.parse(path).getroot()
        if not root.tag.endswith("svg"):
            fail(f"{path.name} is not an SVG root")
        lowered = path.read_text(encoding="utf-8").lower()
        if "<script" in lowered or "javascript:" in lowered or "foreignobject" in lowered:
            fail(f"active SVG content detected in {path.name}")

    for path in (
        DOCS / "assets" / "brand" / "iberolab-mark-512.png",
        DOCS / "assets" / "brand" / "iberolab-social-card.png",
    ):
        if path.read_bytes()[:8] != b"\x89PNG\r\n\x1a\n":
            fail(f"{path.name} is not a valid PNG signature")

    page_markers = (
        'rel="canonical"',
        'href="assets/brand/iberolab-mark.svg"',
        'rel="manifest"',
        'href="site.webmanifest"',
        'property="og:image"',
        'name="twitter:card"',
        'content="summary_large_image"',
        'class="site-brand"',
        'href="academia.html"',
    )
    for name in ("index.html", "convertir.html"):
        text = (DOCS / name).read_text(encoding="utf-8")
        require(text, page_markers, name)
        if any(marker in text.lower() for marker in ("google-analytics", "gtag(", "plausible", "matomo", "facebook pixel")):
            fail(f"tracking marker detected in {name}")

    academia = (DOCS / "academia.html").read_text(encoding="utf-8")
    require(
        academia,
        (
            "Información para universidades y especialistas",
            "IberoLab no traduce al idioma ibérico",
            "English summary",
            "Hesperia",
            "Palaeohispanica",
            "Enviar una aportación",
            "no está afiliado",
            "marca contemporánea",
        ),
        "academia.html",
    )

    privacy = (DOCS / "privacidad.html").read_text(encoding="utf-8")
    require(privacy, ("no incorpora analítica", "no se envían a un servidor", "?q="), "privacidad.html")

    manifest = json.loads((DOCS / "site.webmanifest").read_text(encoding="utf-8"))
    if manifest.get("name") != "IberoLab" or manifest.get("start_url") != "./":
        fail("web manifest identity or start URL is invalid")
    icon_types = {item.get("type") for item in manifest.get("icons", [])}
    if {"image/svg+xml", "image/png"} - icon_types:
        fail("web manifest must expose SVG and PNG icons")

    sitemap = (DOCS / "sitemap.xml").read_text(encoding="utf-8")
    for url in ("/IberoLab/</loc>", "/IberoLab/convertir.html", "/IberoLab/academia.html", "/IberoLab/privacidad.html"):
        if url not in sitemap:
            fail(f"sitemap lacks {url}")

    citation = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    require(citation, ("cff-version: 1.2.0", "IberoLab contributors", "license: Apache-2.0"), "CITATION.cff")

    active_public = "\n".join(
        (ROOT / path).read_text(encoding="utf-8")
        for path in ("README.md", "docs/index.html", "docs/convertir.html", "docs/academia.html")
    )
    for personal_example in ("Lara", "Cris"):
        if personal_example in active_public:
            fail(f"personal example remains in active public content: {personal_example}")

    outreach = (ROOT / "OUTREACH.md").read_text(encoding="utf-8")
    require(outreach, ("Valoración de X", "No traduce", "Hesperia", "Palaeohispanica"), "OUTREACH.md")
    return len(REQUIRED_FILES), 3


if __name__ == "__main__":
    try:
        files, pages = validate()
    except (OSError, ValueError, json.JSONDecodeError, ET.ParseError) as exc:
        print(f"PUBLIC PRESENCE VALIDATION FAILED: {exc}", file=sys.stderr)
        raise SystemExit(1)
    print(f"PUBLIC PRESENCE VALIDATION OK: {files} public assets/files; {pages} public pages checked.")
