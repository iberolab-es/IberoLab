#!/usr/bin/env python3
"""Fetch the missing normalized 38-sign Northeastern Iberian SVG references.

This script builds a manifest for the practical short-input MVP. It deliberately
keeps that graphic layer separate from the 19-token attested seed corpus.
"""
from __future__ import annotations

import hashlib
import json
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "docs" / "assets" / "signs" / "northeastern-dual"
MANIFEST_PATH = ROOT / "data" / "signs" / "mvp-standard-signary.assets.v1.json"

ROWS = [
    (1, "a", "A", "dual-01-a.svg"),
    (2, "e", "E", "dual-02-e.svg"),
    (3, "i", "I", "dual-03-i.svg"),
    (4, "o", "O", "dual-04-o.svg"),
    (5, "u", "U", "dual-05-u.svg"),
    (6, "ga", "GA", "dual-06-ga.svg"),
    (7, "ge", "GE", "dual-07-ge.svg"),
    (8, "gi", "GI", "dual-08-gi.svg"),
    (9, "go", "GO", "dual-09-go.svg"),
    (10, "gu", "GU", "dual-10-gu.svg"),
    (11, "ka", "KA", "dual-11-ka.svg"),
    (12, "ke", "KE", "dual-12-ke.svg"),
    (13, "ki", "KI", "dual-13-ki.svg"),
    (14, "ko", "KO", "dual-14-ko.svg"),
    (15, "ku", "KU", "dual-15-ku.svg"),
    (16, "ba", "BA", "dual-16-ba.svg"),
    (17, "be", "BE", "dual-17-be.svg"),
    (18, "bi", "BI", "dual-18-bi.svg"),
    (19, "bo", "BO", "dual-19-bo.svg"),
    (20, "bu", "BU", "dual-20-bu.svg"),
    (21, "da", "DA", "dual-21-da.svg"),
    (22, "de", "DE", "dual-22-de.svg"),
    (23, "di", "DI", "dual-23-di.svg"),
    (24, "do", "DO", "dual-24-do.svg"),
    (25, "du", "DU", "dual-25-du.svg"),
    (26, "ta", "TA", "dual-26-ta.svg"),
    (27, "te", "TE", "dual-27-te.svg"),
    (28, "ti", "TI", "dual-28-ti.svg"),
    (29, "to", "TO", "dual-29-to.svg"),
    (30, "tu", "TU", "dual-30-tu.svg"),
    (31, "s", "S", "dual-31-s.svg"),
    (32, "ś", "Ś", "dual-32-s2.svg"),
    (33, "r", "R", "dual-33-r.svg"),
    (34, "ŕ", "Ŕ", "dual-34-r2.svg"),
    (35, "l", "L", "dual-35-l.svg"),
    (36, "m", "M", "dual-36-m.svg"),
    (37, "n", "N", "dual-37-n.svg"),
    (38, "ḿ", "Ḿ", "dual-38-m2.svg"),
]

UNSAFE_PATTERNS = (
    rb"<script\b",
    rb"\son[a-z]+\s*=",
    rb"javascript\s*:",
    rb"<foreignobject\b",
)


def validate_svg(data: bytes, source_file: str) -> None:
    if not data.lstrip().startswith((b"<?xml", b"<svg")):
        raise RuntimeError(f"{source_file}: content is not recognizable SVG/XML")
    ET.fromstring(data)
    lowered = data.lower()
    for pattern in UNSAFE_PATTERNS:
        if re.search(pattern, lowered, flags=re.IGNORECASE):
            raise RuntimeError(f"{source_file}: unsafe active SVG content detected")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)

    opener = urllib.request.build_opener()
    opener.addheaders = [("User-Agent", "IberoLab/1.0 signary asset fetcher")]
    assets: list[dict] = []

    for number, token, source_label, local_name in ROWS:
        source_file = f"Sign Iber Noro Dual {number:02d} {source_label}.svg"
        source_page = (
            "https://commons.wikimedia.org/wiki/File:"
            + urllib.parse.quote(source_file.replace(" ", "_"))
        )
        redirect_url = (
            "https://commons.wikimedia.org/wiki/Special:Redirect/file/"
            + urllib.parse.quote(source_file)
        )
        local_path = OUTPUT_DIR / local_name

        if local_path.exists():
            data = local_path.read_bytes()
            with opener.open(redirect_url, timeout=30) as response:
                resolved_url = response.geturl()
                response.read(1)
        else:
            with opener.open(redirect_url, timeout=30) as response:
                data = response.read()
                resolved_url = response.geturl()
            if len(data) < 200:
                raise RuntimeError(f"{source_file}: downloaded file is unexpectedly small")
            local_path.write_bytes(data)

        validate_svg(data, source_file)
        assets.append(
            {
                "number": number,
                "token": token,
                "reference_id": f"dual-{number:02d}-{local_name[8:-4]}",
                "source_file_name": source_file,
                "source_file_page": source_page,
                "source_redirect_url": redirect_url,
                "resolved_download_url": resolved_url,
                "local_path": local_path.relative_to(ROOT).as_posix(),
                "sha256": hashlib.sha256(data).hexdigest(),
                "bytes": len(data),
                "media_type": "image/svg+xml",
                "author": "BotaFlo",
                "licence": "CC0-1.0",
                "licence_url": "https://creativecommons.org/publicdomain/zero/1.0/",
                "graphic_scope": "normalized_standard_reference_not_attestation_facsimile",
            }
        )

    manifest = {
        "schema_version": "1.0.0",
        "manifest_id": "iberolab-mvp-standard-signary-assets",
        "status": "mvp_graphic_reference",
        "purpose": (
            "Complete normalized 38-sign reference layer for short modern-input "
            "adaptations. It is separate from the attested seed corpus manifest."
        ),
        "source_collection": "https://commons.wikimedia.org/wiki/Category:Iberian_letters",
        "source_series": "Sign Iber Noro Dual 01–38",
        "author": "BotaFlo",
        "licence": "CC0-1.0",
        "asset_count": len(assets),
        "tokens": [token for _, token, _, _ in ROWS],
        "assets": assets,
        "scientific_boundary": {
            "attested_seed_manifest_unchanged": "data/signs/reference-standard-dual.assets.v1.json",
            "does_not_claim_translation": True,
            "does_not_select_attestation_specific_allographs": True,
        },
    }
    MANIFEST_PATH.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Prepared {len(assets)} standard SVG references at {MANIFEST_PATH}")


if __name__ == "__main__":
    main()
