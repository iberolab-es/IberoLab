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
    "a", "e", "i", "o", "u", "ga", "ge", "gi", "go", "gu",
    "ka", "ke", "ki", "ko", "ku", "ba", "be", "bi", "bo", "bu",
    "da", "de", "di", "do", "du", "ta", "te", "ti", "to", "tu",
    "s", "ś", "r", "ŕ", "l", "m", "n", "ḿ",
]
EXPECTED_EXAMPLES = {
    "amor": [["a", "m", "o", "r"]],
    "familia": [["ba", "m", "i", "l", "i", "a"]],
    "te quiero": [["te"], ["ki", "e", "r", "o"]],
}
UNSAFE = (rb"<script\b", rb"\son[a-z]+\s*=", rb"javascript\s*:", rb"<foreignobject\b")


def fail(message: str) -> None:
    raise ValueError(message)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_assets() -> tuple[int, int]:
    manifest = load_json(MVP_MANIFEST)
    seed = load_json(SEED_MANIFEST)
    assets = manifest.get("assets", [])

    if manifest.get("schema_version") != "1.0.0" or manifest.get("status") != "mvp_graphic_reference":
        fail("MVP signary manifest version or status is invalid")
    if manifest.get("asset_count") != 38 or len(assets) != 38:
        fail("MVP signary manifest must contain 38 assets")
    if manifest.get("tokens") != EXPECTED_TOKENS:
        fail("MVP signary token order differs from the standard 38-sign layer")
    if [item.get("token") for item in assets] != EXPECTED_TOKENS:
        fail("MVP signary asset tokens are incomplete or out of order")
    if [item.get("number") for item in assets] != list(range(1, 39)):
        fail("MVP asset numbers must run consecutively from 1 to 38")

    for item in assets:
        token = item["token"]
        relative = item.get("local_path", "")
        if not relative.startswith("docs/assets/signs/northeastern-dual/"):
            fail(f"{token}: invalid local asset path")
        path = ROOT / relative
        if not path.is_file():
            fail(f"{token}: local SVG is missing")
        data = path.read_bytes()
        if hashlib.sha256(data).hexdigest() != item.get("sha256") or len(data) != item.get("bytes"):
            fail(f"{token}: stored file differs from manifest")
        if item.get("licence") != "CC0-1.0" or item.get("author") != "BotaFlo":
            fail(f"{token}: source metadata is incomplete")
        if item.get("graphic_scope") != "normalized_standard_reference_not_attestation_facsimile":
            fail(f"{token}: normalized-reference boundary is missing")
        ET.fromstring(data)
        lowered = data.lower()
        if any(re.search(pattern, lowered, flags=re.IGNORECASE) for pattern in UNSAFE):
            fail(f"{token}: unsafe active SVG content detected")

    if seed.get("asset_count") != 19 or len(seed.get("assets", [])) != 19:
        fail("the attested seed manifest must remain at 19 assets")
    if seed.get("unresolved") != []:
        fail("the attested seed manifest must retain zero unresolved graphic tokens")
    boundary = manifest.get("scientific_boundary", {})
    if boundary.get("attested_seed_manifest_unchanged") != "data/signs/reference-standard-dual.assets.v1.json":
        fail("MVP manifest must preserve the seed-manifest boundary")
    if boundary.get("does_not_claim_translation") is not True:
        fail("MVP manifest must prohibit translation claims")
    return len(assets), len(seed.get("assets", []))


def validate_contract() -> int:
    contract = load_json(CONTRACT)
    if contract.get("status") != "public_preview_mvp":
        fail("MVP contract must use public_preview_mvp status")
    if contract.get("classification") != "experimental_phonetic_adaptation":
        fail("MVP classification is invalid")
    if contract.get("translation_claim") is not False or contract.get("formal_engine_enabled") is not False:
        fail("translation and the formal engine must remain disabled")

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
            fail(f"MVP policy must enforce {key}")
    if policy.get("unknown_symbol_policy") != "block":
        fail("unknown symbols must block")

    examples = contract.get("acceptance_examples", [])
    by_input = {item.get("input"): item for item in examples}
    if set(by_input) != set(EXPECTED_EXAMPLES):
        fail("acceptance examples must be amor, familia and te quiero")
    for source, expected in EXPECTED_EXAMPLES.items():
        if by_input[source].get("expected_words") != expected:
            fail(f"{source}: expected token sequence differs from the contract")
    if by_input["familia"].get("required_warning_code") != "f_to_labial_stop":
        fail("familia must retain the explicit f warning")
    return len(examples)


def validate_web_files() -> tuple[int, int]:
    page = PAGE.read_text(encoding="utf-8")
    script = SCRIPT.read_text(encoding="utf-8")
    page_markers = (
        "Adaptación fonética experimental",
        "No es una traducción al idioma ibérico",
        "Escuchar entrada en español",
        "Compartir resultado",
        'id="actionStatus"',
        'wordLabel.className = "word-label"',
        'searchParams.set("q", trimmed)',
        "navigator.share",
        "Los signos son formas normalizadas de referencia",
        'src="mvp-converter.js"',
        'data-example="amor"',
        'data-example="familia"',
        'data-example="te quiero"',
        'data-example="amistad"',
        'data-example="hogar"',
        'dataset.mvpConverterReady = "true"',
    )
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
    for marker in page_markers:
        if marker not in page:
            fail(f"converter page lacks required marker {marker!r}")
    for marker in script_markers:
        if marker not in script:
            fail(f"converter script lacks safeguard {marker!r}")

    for item in load_json(MVP_MANIFEST)["assets"]:
        browser_path = item["local_path"].removeprefix("docs/")
        if browser_path not in script:
            fail(f"converter script does not map token {item['token']!r}")
    if "upload.wikimedia.org" in page or "upload.wikimedia.org" in script:
        fail("public converter must not depend on remote SVG delivery")
    return len(page_markers), len(script_markers)


def validate() -> tuple[int, int, int, int, int]:
    asset_count, seed_count = validate_assets()
    example_count = validate_contract()
    page_markers, script_markers = validate_web_files()
    return asset_count, seed_count, example_count, page_markers, script_markers


if __name__ == "__main__":
    try:
        assets, seed_assets, examples, page_markers, script_markers = validate()
    except (OSError, json.JSONDecodeError, ET.ParseError, KeyError, TypeError, ValueError) as exc:
        print(f"MVP CONVERTER VALIDATION FAILED: {exc}", file=sys.stderr)
        raise SystemExit(1)
    print(
        "MVP CONVERTER VALIDATION OK: "
        f"{assets} normalized SVGs; seed corpus remains {seed_assets}; "
        f"{examples} contract examples; {page_markers} page markers; {script_markers} script safeguards."
    )
