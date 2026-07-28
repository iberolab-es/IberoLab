#!/usr/bin/env python3
"""Vendor the controlled northeastern Iberian reference SVG set.

The standard series supplies eighteen normalized signary references. The
nineteenth corpus token, ń, is supplied by the separately documented m1
variant and is preserved when this script refreshes the standard series.
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "docs" / "assets" / "signs" / "northeastern-dual"
MANIFEST = ROOT / "data" / "signs" / "reference-standard-dual.assets.v1.json"
ERROR_LOG = ROOT / "data" / "signs" / "vendor-error.log"
SOURCE_BASE = "https://commons.wikimedia.org/wiki/Special:Redirect/file/"
FILE_PAGE_BASE = "https://commons.wikimedia.org/wiki/File:"
USER_AGENT = "IberoLab/1.0 (+https://github.com/iberolab-es/IberoLab; contact: iberolab.es@gmail.com)"
MAX_BYTES = 1_000_000
MAX_ATTEMPTS = 5
REQUEST_INTERVAL_SECONDS = 7.0
RETRYABLE_HTTP_CODES = {429, 500, 502, 503, 504}
NASAL_TOKEN = "ń"
NASAL_PATH = ASSET_DIR / "variant-m1-nasal.svg"

STANDARD_SIGN_SPECS = [
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

FORBIDDEN_MARKERS = (b"<script", b"javascript:", b"onload=", b"onerror=", b"<foreignobject")


def retry_delay(exc: HTTPError | URLError, attempt: int) -> float:
    if isinstance(exc, HTTPError):
        retry_after = exc.headers.get("Retry-After")
        if retry_after:
            try:
                return max(1.0, float(retry_after))
            except ValueError:
                try:
                    retry_at = parsedate_to_datetime(retry_after)
                    return max(1.0, retry_at.timestamp() - time.time())
                except (TypeError, ValueError, OverflowError):
                    pass
        if exc.code == 429:
            return max(60.0, 15.0 * attempt)
    return min(120.0, 10.0 * (2 ** (attempt - 1)))


def fetch_svg(file_name: str) -> tuple[bytes, str, str | None]:
    source_url = SOURCE_BASE + quote(file_name)
    last_error: HTTPError | URLError | None = None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        request = Request(
            source_url,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "image/svg+xml,*/*;q=0.8",
                "Accept-Encoding": "identity",
            },
        )
        try:
            with urlopen(request, timeout=60) as response:
                media_type = response.headers.get_content_type()
                final_url = response.geturl()
                data = response.read(MAX_BYTES + 1)
            if len(data) > MAX_BYTES:
                raise ValueError(f"{file_name}: resource exceeds {MAX_BYTES} bytes")
            return data, final_url, media_type
        except HTTPError as exc:
            last_error = exc
            if exc.code not in RETRYABLE_HTTP_CODES or attempt == MAX_ATTEMPTS:
                raise
        except URLError as exc:
            last_error = exc
            if attempt == MAX_ATTEMPTS:
                raise
        delay = retry_delay(last_error, attempt)
        print(f"retry {attempt}/{MAX_ATTEMPTS} for {file_name} after {delay:.0f}s: {last_error}", file=sys.stderr, flush=True)
        time.sleep(delay)
    raise RuntimeError(f"{file_name}: exhausted retries: {last_error}")


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


def load_nasal_record() -> dict[str, object]:
    if not MANIFEST.is_file() or not NASAL_PATH.is_file():
        raise ValueError("resolved m1 asset is missing; run scripts/vendor_nasal_m1.py first")
    current = json.loads(MANIFEST.read_text(encoding="utf-8"))
    record = next((item for item in current.get("assets", []) if item.get("token") == NASAL_TOKEN), None)
    if not record or record.get("paleographic_variant") != "m1":
        raise ValueError("manifest lacks the documented m1 record for ń")
    data = NASAL_PATH.read_bytes()
    validate_svg(data, "NE Iberian m1.svg")
    refreshed = dict(record)
    refreshed["bytes"] = len(data)
    refreshed["sha256"] = hashlib.sha256(data).hexdigest()
    refreshed["media_type"] = "image/svg+xml"
    return refreshed


def main() -> int:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, object]] = []
    for index, (token, reference_id, file_name) in enumerate(STANDARD_SIGN_SPECS):
        if index:
            time.sleep(REQUEST_INTERVAL_SECONDS)
        data, final_url, media_type = fetch_svg(file_name)
        validate_svg(data, file_name)
        local_path = ASSET_DIR / f"{reference_id}.svg"
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
        print(f"vendored {token:>2} -> {local_path.relative_to(ROOT)} ({len(data)} bytes, {digest[:12]})", flush=True)

    records.append(load_nasal_record())
    manifest = {
        "schema_version": "1.1.0",
        "manifest_id": "iberolab-reference-standard-dual-local-assets",
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "source_collection": "https://commons.wikimedia.org/wiki/Category:Iberian_letters",
        "source_series": "Sign Iber Noro Dual 01–38 plus documented NE Iberian m1 variant",
        "author": "multiple CC0 contributors; see source_sets and asset records",
        "licence": "CC0-1.0",
        "licence_url": "https://creativecommons.org/publicdomain/zero/1.0/",
        "asset_count": len(records),
        "assets": records,
        "unresolved": [],
        "source_sets": [
            {"name": "Sign Iber Noro Dual 01–38", "author": "BotaFlo", "licence": "CC0-1.0", "scope": "normalized signary references"},
            {"name": "NE Iberian m1.svg", "author": "Vriullop", "licence": "CC0-1.0", "scope": "normalized paleographic variant m1 used for token ń"},
        ],
        "resolved_tokens": [
            {
                "token": "ń",
                "resolved_as": "m1",
                "traditional_transcription": "m",
                "current_transcription": "ń",
                "evidence": "https://doi.org/10.36707/palaeohispanica.v25i1.703",
                "resolved_on": "2026-07-28",
            }
        ],
    }
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    ERROR_LOG.unlink(missing_ok=True)
    print(f"manifest written: {MANIFEST.relative_to(ROOT)} ({len(records)} assets)")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # noqa: BLE001 - CLI must fail closed on any download/validation error.
        print(f"SVG VENDORING FAILED: {exc}", file=sys.stderr)
        raise SystemExit(1)
