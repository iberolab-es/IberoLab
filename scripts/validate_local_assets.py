#!/usr/bin/env python3
"""Validate local SVG assets, provenance metadata and public local-only usage."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "signs" / "reference-standard-dual.assets.v1.json"
MAPPING = ROOT / "data" / "signs" / "reference-standard-dual.v1.json"
INDEX = ROOT / "docs" / "index.html"
SELF_TEST = ROOT / "docs" / "test.html"
ASSET_DIR = ROOT / "docs" / "assets" / "signs" / "northeastern-dual"
EXPECTED_TOKENS = {"a", "e", "i", "u", "gi", "ke", "ki", "ba", "da", "de", "di", "ta", "s", "ś", "r", "ŕ", "l", "n"}
FORBIDDEN_MARKERS = (b"<script", b"javascript:", b"onload=", b"onerror=", b"<foreignobject")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate() -> tuple[int, int]:
    manifest = load_json(MANIFEST)
    mapping = load_json(MAPPING)
    assets = manifest.get("assets", [])
    if manifest.get("asset_count") != 18 or len(assets) != 18:
        raise ValueError("manifest must declare exactly 18 assets")
    if manifest.get("licence") != "CC0-1.0" or manifest.get("author") != "BotaFlo":
        raise ValueError("manifest author or licence is not the expected reference source")

    by_token = {item.get("token"): item for item in assets}
    if set(by_token) != EXPECTED_TOKENS:
        raise ValueError(f"manifest token mismatch: {sorted(set(by_token) ^ EXPECTED_TOKENS)}")

    declared_paths: set[Path] = set()
    for token, item in by_token.items():
        relative = item.get("local_path")
        if not isinstance(relative, str) or not relative.startswith("docs/assets/signs/northeastern-dual/"):
            raise ValueError(f"{token!r}: invalid local path")
        path = ROOT / relative
        declared_paths.add(path.resolve())
        if not path.is_file():
            raise ValueError(f"{token!r}: local SVG is missing: {relative}")
        data = path.read_bytes()
        if len(data) != item.get("bytes"):
            raise ValueError(f"{token!r}: byte count mismatch")
        digest = hashlib.sha256(data).hexdigest()
        if digest != item.get("sha256"):
            raise ValueError(f"{token!r}: SHA-256 mismatch")
        if item.get("media_type") != "image/svg+xml":
            raise ValueError(f"{token!r}: unexpected media type")
        lowered = data.lower()
        for marker in FORBIDDEN_MARKERS:
            if marker in lowered:
                raise ValueError(f"{token!r}: forbidden active SVG marker {marker!r}")
        try:
            root_element = ElementTree.fromstring(data)
        except ElementTree.ParseError as exc:
            raise ValueError(f"{token!r}: malformed SVG XML") from exc
        if not root_element.tag.lower().endswith("svg"):
            raise ValueError(f"{token!r}: root element is not SVG")

    disk_paths = {path.resolve() for path in ASSET_DIR.glob("*.svg")}
    if disk_paths != declared_paths:
        extras = sorted(str(path.relative_to(ROOT)) for path in disk_paths - declared_paths)
        missing = sorted(str(path.relative_to(ROOT)) for path in declared_paths - disk_paths)
        raise ValueError(f"asset directory differs from manifest; extras={extras}, missing={missing}")

    signs = {item["token"]: item for item in mapping["signs"]}
    for token in EXPECTED_TOKENS:
        sign = signs.get(token)
        if not sign or sign.get("graphic_status") != "local_reference_svg_available":
            raise ValueError(f"{token!r}: mapping is not marked as a local SVG")
        if sign.get("local_path") != by_token[token]["local_path"]:
            raise ValueError(f"{token!r}: mapping path differs from manifest")
    pending = signs.get("ń")
    if not pending or not pending.get("graphic_status", "").startswith("pending_") or pending.get("local_path"):
        raise ValueError("ń must remain pending and must not have a local graphic")

    index = INDEX.read_text(encoding="utf-8")
    self_test = SELF_TEST.read_text(encoding="utf-8")
    for label, html in (("index", index), ("self-test", self_test)):
        if "Special:Redirect/file" in html or "COMMONS_REDIRECT" in html or "const COMMONS" in html:
            raise ValueError(f"{label} still depends on remote SVG delivery")
        for item in assets:
            web_path = item["local_path"].removeprefix("docs/")
            if web_path not in html:
                raise ValueError(f"{label} does not declare local path {web_path}")
    if 'asset_mode: "local_repository"' not in self_test:
        raise ValueError("self-test does not report local_repository asset mode")

    unresolved = manifest.get("unresolved", [])
    if len(unresolved) != 1 or unresolved[0].get("token") != "ń":
        raise ValueError("manifest must retain ń as the only unresolved graphic token")
    return len(assets), len(disk_paths)


if __name__ == "__main__":
    try:
        declared, stored = validate()
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"LOCAL ASSET VALIDATION FAILED: {exc}", file=sys.stderr)
        raise SystemExit(1)
    print(
        "LOCAL ASSET VALIDATION OK: "
        f"{declared} manifest assets; {stored} stored SVGs; hashes, provenance and local-only delivery verified; ń remains pending."
    )
