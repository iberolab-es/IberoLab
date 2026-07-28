#!/usr/bin/env python3
"""Fetch the missing normalized 38-sign Northeastern Iberian SVG references.

The practical MVP graphic layer remains separate from the 19-token attested
seed corpus. Existing seed assets are reused without new network requests; one
Commons API query resolves only the missing standard files.
"""
from __future__ import annotations

import hashlib
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "docs" / "assets" / "signs" / "northeastern-dual"
MANIFEST_PATH = ROOT / "data" / "signs" / "mvp-standard-signary.assets.v1.json"
SEED_MANIFEST_PATH = ROOT / "data" / "signs" / "reference-standard-dual.assets.v1.json"

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
USER_AGENT = "IberoLab/1.0 (https://github.com/iberolab-es/IberoLab)"


def source_file_name(number: int, label: str) -> str:
    return f"Sign Iber Noro Dual {number:02d} {label}.svg"


def validate_svg(data: bytes, source_file: str) -> None:
    if not data.lstrip().startswith((b"<?xml", b"<svg")):
        raise RuntimeError(f"{source_file}: content is not recognizable SVG/XML")
    ET.fromstring(data)
    lowered = data.lower()
    for pattern in UNSAFE_PATTERNS:
        if re.search(pattern, lowered, flags=re.IGNORECASE):
            raise RuntimeError(f"{source_file}: unsafe active SVG content detected")


def fetch_bytes(opener: urllib.request.OpenerDirector, url: str) -> tuple[bytes, str]:
    delays = (0, 2, 5, 10)
    last_error: Exception | None = None
    for delay in delays:
        if delay:
            time.sleep(delay)
        try:
            with opener.open(url, timeout=45) as response:
                return response.read(), response.geturl()
        except urllib.error.HTTPError as exc:
            last_error = exc
            if exc.code not in {429, 502, 503, 504}:
                raise
    assert last_error is not None
    raise last_error


def resolve_missing_urls(
    opener: urllib.request.OpenerDirector,
    missing_rows: list[tuple[int, str, str, str]],
) -> dict[str, dict[str, str]]:
    titles = [f"File:{source_file_name(number, label)}" for number, _, label, _ in missing_rows]
    query = urllib.parse.urlencode(
        {
            "action": "query",
            "format": "json",
            "formatversion": "2",
            "prop": "imageinfo",
            "iiprop": "url",
            "titles": "|".join(titles),
        }
    )
    payload, _ = fetch_bytes(opener, "https://commons.wikimedia.org/w/api.php?" + query)
    document = json.loads(payload.decode("utf-8"))
    resolved: dict[str, dict[str, str]] = {}
    for page in document.get("query", {}).get("pages", []):
        title = page.get("title", "")
        info = page.get("imageinfo", [])
        if page.get("missing") is True or not info:
            raise RuntimeError(f"Commons did not resolve {title!r}")
        resolved[title.removeprefix("File:")] = {
            "url": info[0]["url"],
            "description_url": info[0].get("descriptionurl", ""),
        }
    expected = {title.removeprefix("File:") for title in titles}
    if set(resolved) != expected:
        raise RuntimeError(f"Commons API resolution mismatch: {sorted(expected - set(resolved))}")
    return resolved


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)

    seed = json.loads(SEED_MANIFEST_PATH.read_text(encoding="utf-8"))
    seed_by_source = {
        item["source_file_name"]: item
        for item in seed.get("assets", [])
        if item.get("source_file_name", "").startswith("Sign Iber Noro Dual ")
    }

    missing_rows = [row for row in ROWS if not (OUTPUT_DIR / row[3]).is_file()]
    print(f"Reusing {len(ROWS) - len(missing_rows)} existing standard SVGs; fetching {len(missing_rows)} missing SVGs.")

    opener = urllib.request.build_opener()
    opener.addheaders = [("User-Agent", USER_AGENT)]
    resolved_missing = resolve_missing_urls(opener, missing_rows) if missing_rows else {}
    assets: list[dict] = []

    for number, token, label, local_name in ROWS:
        source_file = source_file_name(number, label)
        local_path = OUTPUT_DIR / local_name
        existing_metadata = seed_by_source.get(source_file)

        if local_path.is_file():
            data = local_path.read_bytes()
            if existing_metadata:
                source_page = existing_metadata["source_file_page"]
                redirect_url = existing_metadata["source_redirect_url"]
                resolved_url = existing_metadata["resolved_download_url"]
            else:
                source_page = (
                    "https://commons.wikimedia.org/wiki/File:"
                    + urllib.parse.quote(source_file.replace(" ", "_"))
                )
                redirect_url = (
                    "https://commons.wikimedia.org/wiki/Special:Redirect/file/"
                    + urllib.parse.quote(source_file)
                )
                resolved_url = resolved_missing.get(source_file, {}).get("url", "")
        else:
            metadata = resolved_missing[source_file]
            print(f"Downloading {number:02d}/38: {source_file}")
            data, resolved_url = fetch_bytes(opener, metadata["url"])
            source_page = metadata["description_url"] or (
                "https://commons.wikimedia.org/wiki/File:"
                + urllib.parse.quote(source_file.replace(" ", "_"))
            )
            redirect_url = (
                "https://commons.wikimedia.org/wiki/Special:Redirect/file/"
                + urllib.parse.quote(source_file)
            )
            if len(data) < 200:
                raise RuntimeError(f"{source_file}: downloaded file is unexpectedly small")
            local_path.write_bytes(data)
            time.sleep(0.35)

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
