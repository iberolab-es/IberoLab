#!/usr/bin/env python3
"""Validate the attested corpus and its synchronized minimum token inventory."""

from __future__ import annotations

import json
import sys
import unicodedata
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CORPUS_PATH = ROOT / "data" / "corpus" / "attested-forms.v1.json"
INVENTORY_PATH = ROOT / "data" / "signs" / "minimum-inventory.v1.json"
INVENTORY_SCHEMA_PATH = ROOT / "data" / "schema" / "minimum-inventory.schema.json"
MAPPING_PATH = ROOT / "data" / "signs" / "reference-standard-dual.v1.json"
MANIFEST_PATH = ROOT / "data" / "signs" / "reference-standard-dual.assets.v1.json"

ALLOWED_READING = {"low", "medium", "high", "very_high"}
ALLOWED_SEMANTIC = {
    "uninterpreted",
    "disputed",
    "supported_hypothesis",
    "contextually_supported",
    "identified_name",
    "identified_referent",
}
ALLOWED_CLASSES = {
    "vowel",
    "continuant",
    "labial_syllabogram",
    "dental_syllabogram",
    "velar_syllabogram",
}
ALLOWED_GRAPHIC_STATUS = {
    "local_reference_svg_available",
    "local_attested_variant_svg_available",
}
FORBIDDEN_KEYS = {"translation", "literal_translation", "modern_equivalent"}
EXPECTED_NASAL = {
    "graphic_status": "local_attested_variant_svg_available",
    "allograph_status": "documented_variant_m1_normalized_reference",
    "evidence_level": "transcription_and_variant_attested_graphic_reference_controlled",
    "paleographic_variant": "m1",
    "traditional_transcription": "m",
    "project_transcription": "ń",
    "evidence": "https://doi.org/10.36707/palaeohispanica.v25i1.703",
}


def fail(message: str) -> None:
    raise ValueError(message)


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def validate_https(url: str, context: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.netloc:
        fail(f"{context}: source URL must be an absolute HTTPS URL: {url!r}")


def validate_inventory_schema_file() -> None:
    schema = load_json(INVENTORY_SCHEMA_PATH)
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        fail("minimum inventory schema must use JSON Schema draft 2020-12")
    if schema.get("title") != "IberoLab minimum transcription and graphic inventory":
        fail("minimum inventory schema has an unexpected title")
    signs = schema.get("properties", {}).get("signs", {})
    if signs.get("minItems") != 19 or signs.get("maxItems") != 19:
        fail("minimum inventory schema must require exactly nineteen signs")


def validate_inventory(inventory: dict, mapping: dict, manifest: dict) -> set[str]:
    if inventory.get("schema_version") != "1.1.0":
        fail("minimum inventory must use schema_version 1.1.0")
    if inventory.get("status") != "transcription_inventory_with_graphic_references":
        fail("minimum inventory has an obsolete status")
    expected_links = {
        "derived_from": "data/corpus/attested-forms.v1.json",
        "graphic_mapping": "data/signs/reference-standard-dual.v1.json",
        "asset_manifest": "data/signs/reference-standard-dual.assets.v1.json",
    }
    for key, value in expected_links.items():
        if inventory.get(key) != value:
            fail(f"minimum inventory {key} must be {value!r}")

    policy = inventory.get("policy", {})
    for key in ("description", "svg_policy", "allograph_policy", "legacy_html"):
        if not isinstance(policy.get(key), str) or len(policy[key].strip()) < 20:
            fail(f"minimum inventory policy lacks a substantive {key}")

    entries = inventory.get("signs")
    if not isinstance(entries, list) or len(entries) != 19:
        fail("minimum inventory must contain exactly nineteen sign entries")

    mapping_by_token = {item.get("token"): item for item in mapping.get("signs", [])}
    manifest_by_token = {item.get("token"): item for item in manifest.get("assets", [])}
    ids: set[str] = set()
    tokens: set[str] = set()

    for index, item in enumerate(entries):
        context = f"inventory.signs[{index}]"
        identifier = item.get("id")
        token = item.get("transliteration")
        if not isinstance(identifier, str) or not identifier.startswith("ib-ne-sign-"):
            fail(f"{context}: invalid id")
        if identifier in ids:
            fail(f"{context}: duplicate id {identifier!r}")
        ids.add(identifier)
        if not isinstance(token, str) or not token:
            fail(f"{context}: transliteration is required")
        if token in tokens:
            fail(f"{context}: duplicate transliteration {token!r}")
        tokens.add(token)

        if item.get("class") not in ALLOWED_CLASSES:
            fail(f"{context}: invalid token class")
        if item.get("script") != "Northeastern Iberian":
            fail(f"{context}: unexpected script")
        if item.get("corpus_required") is not True:
            fail(f"{context}: every minimum token must be corpus_required")
        if item.get("graphic_status") not in ALLOWED_GRAPHIC_STATUS:
            fail(f"{context}: graphic status is not a controlled local status")
        if not isinstance(item.get("notes"), str) or len(item["notes"].strip()) < 20:
            fail(f"{context}: substantive notes are required")

        mapped = mapping_by_token.get(token)
        asset = manifest_by_token.get(token)
        if not mapped or not asset:
            fail(f"{context}: token is absent from mapping or manifest")
        for field, mapped_field in (
            ("graphic_reference_id", "reference_id"),
            ("local_path", "local_path"),
            ("graphic_status", "graphic_status"),
        ):
            if item.get(field) != mapped.get(mapped_field):
                fail(f"{context}: {field} differs from graphic mapping")
        if item.get("graphic_reference_id") != asset.get("reference_id"):
            fail(f"{context}: graphic_reference_id differs from asset manifest")
        if item.get("local_path") != asset.get("local_path"):
            fail(f"{context}: local_path differs from asset manifest")
        if not (ROOT / item["local_path"]).is_file():
            fail(f"{context}: local SVG does not exist")

        if token == "ń":
            for key, value in EXPECTED_NASAL.items():
                if item.get(key) != value:
                    fail(f"{context}: ń has invalid {key}: {item.get(key)!r}")
            if item.get("graphic_reference_id") != "variant-m1-nasal":
                fail(f"{context}: ń must use variant-m1-nasal")
        else:
            if item.get("allograph_status") != "normalized_reference_only":
                fail(f"{context}: standard token must remain normalized_reference_only")
            if item.get("evidence_level") != "transcription_attested_graphic_reference_controlled":
                fail(f"{context}: standard token has an unexpected evidence level")
            forbidden_variant_fields = {
                "paleographic_variant",
                "traditional_transcription",
                "project_transcription",
                "evidence",
            }.intersection(item)
            if forbidden_variant_fields:
                fail(f"{context}: standard token contains variant-only fields {sorted(forbidden_variant_fields)}")

    if tokens != set(mapping_by_token) or tokens != set(manifest_by_token):
        fail("minimum inventory, graphic mapping and asset manifest token sets differ")
    if manifest.get("asset_count") != len(entries) or manifest.get("unresolved") != []:
        fail("asset manifest must contain nineteen resolved entries")
    return tokens


def validate() -> tuple[int, int, int]:
    corpus = load_json(CORPUS_PATH)
    inventory = load_json(INVENTORY_PATH)
    mapping = load_json(MAPPING_PATH)
    manifest = load_json(MANIFEST_PATH)
    validate_inventory_schema_file()
    inventory_tokens = validate_inventory(inventory, mapping, manifest)

    forms = corpus.get("forms")
    if not isinstance(forms, list) or not forms:
        fail("Corpus must contain a non-empty forms array.")

    ids: set[str] = set()
    normalized_forms: set[str] = set()
    used_tokens: set[str] = set()

    for index, item in enumerate(forms):
        context = f"forms[{index}]"
        forbidden = FORBIDDEN_KEYS.intersection(item)
        if forbidden:
            fail(f"{context}: forbidden unqualified translation keys: {sorted(forbidden)}")

        entry_id = item.get("id")
        form = item.get("form")
        tokens = item.get("grapheme_sequence")
        sources = item.get("sources")

        if not isinstance(entry_id, str) or not entry_id:
            fail(f"{context}: missing id.")
        if entry_id in ids:
            fail(f"{context}: duplicate id {entry_id!r}.")
        ids.add(entry_id)

        if not isinstance(form, str) or not form.strip():
            fail(f"{context}: missing form.")
        normalized = unicodedata.normalize("NFC", form)
        if form != normalized:
            fail(f"{context}: form must use Unicode NFC normalization.")
        if normalized in normalized_forms:
            fail(f"{context}: duplicate form {form!r}.")
        normalized_forms.add(normalized)

        if item.get("reading_confidence") not in ALLOWED_READING:
            fail(f"{context}: invalid reading_confidence.")
        if item.get("semantic_status") not in ALLOWED_SEMANTIC:
            fail(f"{context}: invalid semantic_status.")

        if not isinstance(tokens, list) or not tokens:
            fail(f"{context}: grapheme_sequence must be non-empty.")
        joined = "".join(tokens)
        if joined != form:
            fail(f"{context}: token sequence {tokens!r} joins to {joined!r}, not to form {form!r}.")
        unknown = set(tokens) - inventory_tokens
        if unknown:
            fail(f"{context}: tokens absent from minimum inventory: {sorted(unknown)}")
        used_tokens.update(tokens)

        if not isinstance(sources, list) or not sources:
            fail(f"{context}: at least one source is required.")
        for source_index, source in enumerate(sources):
            source_context = f"{context}.sources[{source_index}]"
            if not source.get("citation"):
                fail(f"{source_context}: citation is required.")
            validate_https(source.get("url", ""), source_context)
            doi = source.get("doi")
            if doi and not source["url"].endswith(doi):
                fail(f"{source_context}: DOI URL does not match doi field.")

    unused = inventory_tokens - used_tokens
    if unused:
        fail(f"Minimum inventory contains tokens not used by the corpus: {sorted(unused)}")

    return len(forms), len(inventory_tokens), len(mapping.get("signs", []))


if __name__ == "__main__":
    try:
        form_count, token_count, graphic_count = validate()
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"VALIDATION FAILED: {exc}", file=sys.stderr)
        raise SystemExit(1)
    print(
        f"VALIDATION OK: {form_count} attested forms; {token_count} minimum transcription tokens; "
        f"{graphic_count} synchronized graphic mappings; no inventory token remains pending."
    )
