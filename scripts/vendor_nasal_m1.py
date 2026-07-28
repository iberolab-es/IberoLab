#!/usr/bin/env python3
"""Vendor the m1 sign used for the scholarly transcription ń.

The 2025 Mas Castellar publication identifies the sign in taŕśabańar as
paleographic variant m1. It notes that the traditional transcription was m and
adopts ń for Iberian because the sign behaves as a marked, non-labial nasal.
This script vendors a CC0 normalized m1 reference SVG and records that
transcription history without presenting the resource as an inscription
facsimile.
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "signs" / "reference-standard-dual.assets.v1.json"
LOCAL_PATH = ROOT / "docs" / "assets" / "signs" / "northeastern-dual" / "variant-m1-nasal.svg"
FILE_NAME = "NE Iberian m1.svg"
SOURCE_REDIRECT = "https://commons.wikimedia.org/wiki/Special:Redirect/file/" + quote(FILE_NAME)
SOURCE_PAGE = "https://commons.wikimedia.org/wiki/File:NE_Iberian_m1.svg"
USER_AGENT = "IberoLab/1.0 (+https://github.com/iberolab-es/IberoLab; contact: iberolab.es@gmail.com)"
MAX_BYTES = 1_000_000
FORBIDDEN_MARKERS = (b"<script", b"javascript:", b"onload=", b"onerror=", b"<foreignobject")


def fetch() -> tuple[bytes, str, str | None]:
    last_error: Exception | None = None
    for attempt in range(1, 5):
        request = Request(
            SOURCE_REDIRECT,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "image/svg+xml,*/*;q=0.8",
                "Accept-Encoding": "identity",
            },
        )
        try:
            with urlopen(request, timeout=60) as response:
                data = response.read(MAX_BYTES + 1)
                if len(data) > MAX_BYTES:
                    raise ValueError("m1 SVG exceeds the maximum accepted size")
                return data, response.geturl(), response.headers.get_content_type()
        except (HTTPError, URLError) as exc:
            last_error = exc
            if attempt == 4:
                raise
            delay = 60 if isinstance(exc, HTTPError) and exc.code == 429 else 10 * attempt
            print(f"retry {attempt}/4 after {delay}s: {exc}", file=sys.stderr, flush=True)
            time.sleep(delay)
    raise RuntimeError(f"could not download m1 SVG: {last_error}")


def validate_svg(data: bytes) -> None:
    if not data:
        raise ValueError("m1 SVG response is empty")
    lowered = data.lower()
    for marker in FORBIDDEN_MARKERS:
        if marker in lowered:
            raise ValueError(f"m1 SVG contains forbidden marker {marker!r}")
    try:
        root = ElementTree.fromstring(data)
    except ElementTree.ParseError as exc:
        raise ValueError("m1 SVG is malformed XML") from exc
    if not root.tag.lower().endswith("svg"):
        raise ValueError("m1 resource root element is not SVG")


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assets = manifest.get("assets", [])
    if any(item.get("token") == "ń" for item in assets):
        raise ValueError("manifest already contains an asset for ń")

    data, resolved_url, media_type = fetch()
    validate_svg(data)
    if media_type != "image/svg+xml":
        raise ValueError(f"unexpected media type for m1 SVG: {media_type!r}")

    LOCAL_PATH.parent.mkdir(parents=True, exist_ok=True)
    LOCAL_PATH.write_bytes(data)
    digest = hashlib.sha256(data).hexdigest()
    record = {
        "token": "ń",
        "reference_id": "variant-m1-nasal",
        "source_file_name": FILE_NAME,
        "source_file_page": SOURCE_PAGE,
        "source_redirect_url": SOURCE_REDIRECT,
        "resolved_download_url": resolved_url,
        "local_path": LOCAL_PATH.relative_to(ROOT).as_posix(),
        "sha256": digest,
        "bytes": len(data),
        "media_type": media_type,
        "author": "Vriullop",
        "licence": "CC0-1.0",
        "licence_url": "https://creativecommons.org/publicdomain/zero/1.0/",
        "paleographic_variant": "m1",
        "traditional_transcription": "m",
        "project_transcription": "ń",
        "phonological_scope": "marked_nasal_not_labial",
        "graphic_scope": "normalized_m1_variant_reference_not_facsimile",
        "scholarly_evidence": "https://doi.org/10.36707/palaeohispanica.v25i1.703"
    }
    assets.append(record)
    manifest["schema_version"] = "1.1.0"
    manifest["asset_count"] = len(assets)
    manifest["assets"] = assets
    manifest["source_sets"] = [
        {
            "name": "Sign Iber Noro Dual 01–38",
            "author": "BotaFlo",
            "licence": "CC0-1.0",
            "scope": "normalized signary references"
        },
        {
            "name": "NE Iberian m1.svg",
            "author": "Vriullop",
            "licence": "CC0-1.0",
            "scope": "normalized paleographic variant m1 used for token ń"
        }
    ]
    manifest["unresolved"] = []
    manifest["resolved_tokens"] = [
        {
            "token": "ń",
            "resolved_as": "m1",
            "traditional_transcription": "m",
            "current_transcription": "ń",
            "evidence": "https://doi.org/10.36707/palaeohispanica.v25i1.703",
            "resolved_on": "2026-07-28"
        }
    ]
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"NASAL ASSET VENDORED: {LOCAL_PATH.relative_to(ROOT)}; "
        f"{len(data)} bytes; sha256={digest}"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError, HTTPError, URLError) as exc:
        print(f"NASAL ASSET VENDORING FAILED: {exc}", file=sys.stderr)
        raise SystemExit(1)
