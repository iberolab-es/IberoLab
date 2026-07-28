#!/usr/bin/env python3
"""Validate the practical short-input converter without third-party dependencies."""
from __future__ import annotations

import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MVP_MANIFEST = ROOT / "data" / "signs" / "mvp-standard-signary.assets.v1.json"
SEED_MANIFEST = ROOT / "data" / "signs" / "reference-standard-dual.assets.v1.json"
CONTRACT = ROOT / "data" / "engine" / "mvp-short-converter.v1.json"
PAGE = ROOT / "docs" / "convertir.html"
SCRIPT = ROOT / "docs" / "mvp-converter.js"

EXPECTED_TOKENS = [
    "a", "e", "i", "o", "u",
    "ga", "ge", "gi", "go", "gu",
    "ka", "ke", "ki", "ko", "ku",
    "ba", "be", "bi", "bo", "bu",
    "da", "de", "di", "do", "du",
    "ta", "te", "ti", "to", "tu",
    "s", "ś", "r", "ŕ", "l", "m", "n", "ḿ",
]
EXPECTED_EXAMPLES = {
    "amor": [["a", "m", "o", "r"]],
    "familia": [["ba", "m", "i", "l", "i", "a"]],
    "te quiero": [["te"], ["ki", "e", "r", "o"]],
}
UNSAFE_PATTERNS = (
    rb"<script\b",
    rb"\son[a-z]+\s*=",
    rb"javascript\s*:",
    rb"<foreignobject\b",
)


def fail(message: str) -> None:
    raise ValueError(message)


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def validate_assets() -> tuple[int, int]:
    manifest = load_json(MVP_MANIFEST)
    seed = load_json(SEED_MANIFEST)

    if manifest.get("schema_version") != "1.0.0":
        fail("MVP signary manifest must use version 1.0.0")
    if manifest.get("status") != "mvp_graphic_reference":
        fail("MVP signary manifest has an unexpected status")
    if manifest.get("asset_count") != 38:
        fail("MVP signary manifest must contain 38 assets")
    if manifest.get("tokens") != EXPECTED_TOKENS:
        fail("MVP signary token order differs from the standard 38-sign layer")

    assets = manifest.get("assets", [])
    if len(assets) != 38:
        fail("MVP signary assets array must contain 38 entries")
    if [item.get("token") for item in assets] != EXPECTED_TOKENS:
        fail("MVP signary asset tokens are incomplete, duplicated or out of order")
    if [item.get("number") for item in assets] != list(range(1, 39)):
        fail("MVP signary asset numbers must run consecutively from 1 to 38")

    for item in assets:
        token = item["token"]
        relative = item.get("local_path", "")
        if not relative.startswith("docs/assets/signs/northeastern-dual/"):
            fail(f"{token}: invalid local asset path")
        path = ROOT / relative
        if not path.is_file():
            fail(f"{token}: local SVG is missing")
        data = path.read_bytes()
        if hashlib.sha256(data).hexdigest() != item.get("sha256"):
            fail(f"{token}: SHA-256 differs from the MVP manifest")
        if len(data) != item.get("bytes"):
            fail(f"{token}: byte count differs from the MVP manifest")
        if item.get("licence") != "CC0-1.0" or item.get("author") != "BotaFlo":
            fail(f"{token}: expected CC0 attribution metadata is missing")
        if item.get("graphic_scope") != "normalized_standard_reference_not_attestation_facsimile":
            fail(f"{token}: normalized-reference boundary is missing")
        ET.fromstring(data)
        lowered = data.lower()
        for pattern in UNSAFE_PATTERNS:
            if re.search(pattern, lowered, flags=re.IGNORECASE):
                fail(f"{token}: unsafe active SVG content detected")

    if seed.get("asset_count") != 19 or len(seed.get("assets", [])) != 19:
        fail("the attested seed manifest must remain at 19 controlled assets")
    if seed.get("unresolved") != []:
        fail("the attested seed manifest must retain zero unresolved graphic tokens")
    boundary = manifest.get("scientific_boundary", {})
    if boundary.get("attested_seed_manifest_unchanged") != "data/signs/reference-standard-dual.assets.v1.json":
        fail("MVP manifest must explicitly preserve the seed manifest boundary")
    if boundary.get("does_not_claim_translation") is not True:
        fail("MVP manifest must prohibit translation claims")

    return len(assets), len(seed.get("assets", []))


def validate_contract() -> int:
    contract = load_json(CONTRACT)
    if contract.get("status") != "public_preview_mvp":
        fail("MVP converter contract must use public_preview_mvp status")
    if contract.get("classification") != "experimental_phonetic_adaptation":
        fail("MVP converter classification is invalid")
    if contract.get("translation_claim") is not False:
        fail("MVP converter must prohibit translation claims")
    if contract.get("formal_engine_enabled") is not False:
        fail("the formal engine must remain disabled")

    scope = contract.get("scope", {})
    if scope.get("maximum_characters") != 48 or scope.get("maximum_words") != 6:
        fail("MVP input limits must remain 48 characters and 6 words")
    policy = contract.get("adaptation_policy", {})
    for key in (
        "cluster_support_vowels_must_be_reported",
        "unsupported_sound_substitutions_must_be_reported",
        "silent_character_removal_must_be_reported",
        "empty_output_forbidden",
    ):
        if policy.get(key) is not True:
            fail(f"MVP adaptation policy must enforce {key}")
    if policy.get("unknown_symbol_policy") != "block":
        fail("unknown symbols must block instead of disappearing")

    examples = contract.get("acceptance_examples", [])
    by_input = {item.get("input"): item for item in examples}
    if set(by_input) != set(EXPECTED_EXAMPLES):
        fail("MVP acceptance examples must be exactly amor, familia and te quiero")
    for source, expected in EXPECTED_EXAMPLES.items():
        if by_input[source].get("expected_words") != expected:
            fail(f"{source}: expected token sequence differs from the MVP contract")
    if by_input["familia"].get("required_warning_code") != "f_to_labial_stop":
        fail("familia must retain the explicit f approximation warning")
    return len(examples)


def validate_web_files() -> tuple[int, int]:
    page = PAGE.read_text(encoding="utf-8")
    script = SCRIPT.read_text(encoding="utf-8")

    page_markers = (
        "Adaptación fonética experimental",
        "No es una traducción al idioma ibérico",
        "Escuchar entrada en español",
        "Signos normalizados de referencia",
        'src="mvp-converter.js"',
        'data-example="amor"',
        'data-example="familia"',
        'data-example="te quiero"',
        'dataset.mvpConverterReady = "true"',
    )
    for marker in page_markers:
        if marker not in page:
            fail(f"converter page lacks required marker {marker!r}")

    script_markers = (
        "experimental_phonetic_adaptation",
        "translationClaim: false",
        "cluster_support_vowel",
        "f_to_labial_stop",
        "theta_to_sibilant",
        "palatal_nasal_to_ni",
        "empty_word_output",
        "window.IberoMvp",
    )
    for marker in script_markers:
        if marker not in script:
            fail(f"converter script lacks required safeguard {marker!r}")

    manifest = load_json(MVP_MANIFEST)
    for item in manifest["assets"]:
        browser_path = item["local_path"].removeprefix("docs/")
        if browser_path not in script:
            fail(f"converter script does not map token {item['token']!r} to its local SVG")

    if "upload.wikimedia.org" in page or "upload.wikimedia.org" in script:
        fail("public converter must not depend on remote SVG delivery")
    return len(page_markers), len(script_markers)


def validate() -> tuple[int, int, int, int, int]:
    asset_count, seed_count = validate_assets()
    example_count = validate_contract()
    page_marker_count, script_marker_count = validate_web_files()
    return asset_count, seed_count, example_count, page_marker_count, script_marker_count


if __name__ == "__main__":
    try:
        assets, seed_assets, examples, page_markers, script_markers = validate()
    except (OSError, json.JSONDecodeError, ET.ParseError, KeyError, TypeError, ValueError) as exc:
        print(f"MVP CONVERTER VALIDATION FAILED: {exc}", file=sys.stderr)
        raise SystemExit(1)

    print(
        "MVP CONVERTER VALIDATION OK: "
        f"{assets} normalized SVGs; seed corpus remains {seed_assets}; "
        f"{examples} acceptance examples; {page_markers} page markers; "
        f"{script_markers} script safeguards."
    )
