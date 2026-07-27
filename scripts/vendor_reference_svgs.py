#!/usr/bin/env python3
"""Vendor the provisional CC0 northeastern-dual reference SVGs.

The script downloads the exact Wikimedia Commons SVG files declared by
IberoLab, rejects unsafe or malformed SVG input, stores each resource under a
stable repository path and writes a machine-readable provenance manifest.
"""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "docs" / "assets" / "signs" / "northeastern-dual"
MANIFEST = ROOT / "data" / "signs" / "reference-standard-dual.assets.v1.json"
SOURCE_BASE = "https://commons.wikimedia.org/wiki/Special:Redirect/file/"
FILE_PAGE_BASE = "https://commons.wikimedia.org/wiki/File:"
USER_AGENT = "IberoLab/1.0 (+https://github.com/iberolab-es/IberoLab)"
MAX_BYTES = 1_000_000

SIGN_SPECS = [
    ("a", "dual-01-a", "Sign Iber Noro Dual 01 A.svg"),
    ("e", "dual-02-e", "Sign Iber Noro Dual 02 E.svg"),
    ("i", "dual-03-i", "Sign Iber Noro Dual 03 I.svg"),
    ("u", "dual-05-u", "Sign Iber Noro Dual 05 U.svg"),
    ("gi", "dual-08-gi", "Sign Iber Noro Dual 08 GI.svg"),
    ("ke", "dual-12-ke", "Sign Iber Noro Dual 12 KE.svg"),
    ("ki", "dual-13-ki", "Sign Iber Noro Dual 13 KI.svg"),
    ("ba", "dual-16-ba", "Sign Iber Noro Dual 16 BA.svg"),
    ("da", "dual-21-da", "Sign Iber Noro Dual 21 DA.svg"),
    ("de", "dual-22-de", "Sign Iber Noro Dual 22 DE.svg"),
    ("di", "dual-23-di", "Sign Iber Noro Dual 23 DI.svg"),
    ("ta", "dual-26-ta", "Sign Iber Noro Dual 26 TA.svg"),
    ("s", "dual-31-s", "Sign Iber Noro Dual 31 S.svg"),
    ("ś", "dual-32-s2", "Sign Iber Noro Dual 32 Ś.svg"),
    ("r", "dual-33-r", "Sign Iber Noro Dual 33 R.svg"),
    ("ŕ", "dual-34-r2", "Sign Iber Noro Dual 34 Ŕ.svg"),
    ("l", "dual-35-l", "Sign Iber Noro Dual 35 L.svg"),
    ("n", "dual-37-n", "Sign Iber Noro Dual 37 N.svg"),
]

FORBIDDEN_MARKERS = (
    b"<script",
    b"javascript:",
    b"onload=",
    b"onerror=",
    b"<foreignobject",
)


def fetch_svg(file_name: str) -> tuple[bytes, str, str | None]:
    source_url = SOURCE_BASE + quote(file_name)
    request = Request(source_url, headers={"User-Agent": USER_AGENT, "Accept": "image/svg+xml,*/*;q=0.8"})
    with urlopen(request, timeout=45) as response:
        media_type = response.headers.get_content_type()
        final_url = response.geturl()
        data = response.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise ValueError(f"{file_name}: resource exceeds {MAX_BYTES} bytes")
    return data, final_url, media_type


def validate_svg(data: bytes, file_name: str) -> None:
    if not data:
        raise ValueError(f"{file_name}: empty response")
    lowered = data.lower()
    for marker in FORBIDDEN_MARKERS:
        if marker in lowered:
            raise ValueError(f"{file_name}: forbidden SVG marker {marker!r}")
    try:
        root = ElementTree.fromstring(data)
    except ElementTree.ParseError as exc:
        raise ValueError(f"{file_name}: malformed XML: {exc}") from exc
    if not root.tag.lower().endswith("svg"):
        raise ValueError(f"{file_name}: root element is not SVG")


def main() -> int:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, object]] = []

    for token, reference_id, file_name in SIGN_SPECS:
        data, final_url, media_type = fetch_svg(file_name)
        validate_svg(data, file_name)
        local_name = f"{reference_id}.svg"
        local_path = ASSET_DIR / local_name
        local_path.write_bytes(data)
        digest = hashlib.sha256(data).hexdigest()
        records.append(
            {
                "token": token,
                "reference_id": reference_id,
                "source_file_name": file_name,
                "source_file_page": FILE_PAGE_BASE + quote(file_name.replace(" ", "_")),
                "source_redirect_url": SOURCE_BASE + quote(file_name),
                "resolved_download_url": final_url,
                "local_path": local_path.relative_to(ROOT).as_posix(),
                "sha256": digest,
                "bytes": len(data),
                "media_type": media_type,
                "author": "BotaFlo",
                "licence": "CC0-1.0",
                "licence_url": "https://creativecommons.org/publicdomain/zero/1.0/",
            }
        )
        print(f"vendored {token:>2} -> {local_path.relative_to(ROOT)} ({len(data)} bytes, {digest[:12]})")

    manifest = {
        "schema_version": "1.0.0",
        "manifest_id": "iberolab-reference-standard-dual-local-assets",
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "source_collection": "https://commons.wikimedia.org/wiki/Category:Iberian_letters",
        "source_series": "Sign Iber Noro Dual 01–38",
        "author": "BotaFlo",
        "licence": "CC0-1.0",
        "licence_url": "https://creativecommons.org/publicdomain/zero/1.0/",
        "asset_count": len(records),
        "assets": records,
        "unresolved": [
            {
                "token": "ń",
                "status": "pending_nasal_sign_verification",
                "reason": "No graphic is assigned until the exact sign and transcription convention are verified against the cited 2025 publication.",
            }
        ],
    }
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"manifest written: {MANIFEST.relative_to(ROOT)} ({len(records)} assets)")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # noqa: BLE001 - CLI must fail closed on any download/validation error.
        print(f"SVG VENDORING FAILED: {exc}", file=sys.stderr)
        raise SystemExit(1)
