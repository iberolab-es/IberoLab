#!/usr/bin/env python3
"""Validate the minimal, specification-only pronunciation profile registry."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "engine" / "spanish-pronunciation-dimensions.v1.json"
PROFILE_SCHEMA = ROOT / "data" / "schema" / "pronunciation-profile.schema.json"
ENGINE_CONTRACT = ROOT / "data" / "engine" / "phonetic-engine-contract.v1.json"
SPEC_DOC = ROOT / "docs" / "SPANISH_PRONUNCIATION_PROFILES.md"

EXPECTED_DIMENSIONS = {
    "sibilant_system",
    "palatal_lateral_system",
    "vowel_sequence_interpretation",
    "stress_assignment_source",
}


def fail(message: str) -> None:
    raise ValueError(message)


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def validate_https(url: str, context: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.netloc:
        fail(f"{context}: expected an absolute HTTPS URL")


def validate() -> tuple[int, int, int]:
    registry = load_json(REGISTRY)
    schema = load_json(PROFILE_SCHEMA)
    contract = load_json(ENGINE_CONTRACT)

    if registry.get("schema_version") != "1.0.0":
        fail("registry version must be 1.0.0")
    if registry.get("status") != "specification_only":
        fail("registry must remain specification_only")
    if registry.get("language_tag") != "es-ES":
        fail("registry must target es-ES")
    if registry.get("public_profile_selection_enabled") is not False:
        fail("public profile selection must remain disabled")
    if registry.get("default_profile_id") is not None:
        fail("no silent default profile is allowed")
    if registry.get("approved_profiles") != []:
        fail("no profile is approved in this specification-only phase")

    policy = registry.get("policy", {})
    if policy.get("no_silent_default") is not True:
        fail("the registry must prohibit silent defaults")
    if policy.get("variation_must_be_declared") is not True:
        fail("pronunciation variation must be declared")
    if policy.get("unknown_word_guessing_enabled") is not False:
        fail("unknown-word pronunciation guessing must remain disabled")

    dimensions = registry.get("documented_dimensions", [])
    dimension_ids = {item.get("dimension_id") for item in dimensions}
    if dimension_ids != EXPECTED_DIMENSIONS or len(dimensions) != len(EXPECTED_DIMENSIONS):
        fail("the four MVP pronunciation dimensions are incomplete or duplicated")

    source_count = 0
    for item in dimensions:
        dimension_id = item.get("dimension_id", "unknown")
        if item.get("default_option") is not None:
            fail(f"{dimension_id}: default_option must remain null")
        options = item.get("options", [])
        if not options:
            fail(f"{dimension_id}: at least one explicit option is required")
        option_ids = [option.get("option_id") for option in options]
        if None in option_ids or len(option_ids) != len(set(option_ids)):
            fail(f"{dimension_id}: option identifiers must be present and unique")
        sources = item.get("sources", [])
        if not sources:
            fail(f"{dimension_id}: at least one source is required")
        for index, source in enumerate(sources):
            validate_https(source.get("url", ""), f"{dimension_id}.sources[{index}]")
        source_count += len(sources)

    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        fail("profile schema must use JSON Schema draft 2020-12")
    if schema.get("title") != "IberoLab Spanish pronunciation profile":
        fail("profile schema title is unexpected")
    properties = schema.get("properties", {})
    if properties.get("language_tag", {}).get("const") != "es-ES":
        fail("profile schema must target es-ES")
    unknown_policy = set(properties.get("unknown_word_policy", {}).get("enum", []))
    if unknown_policy != {
        "block",
        "require_user_pronunciation",
        "ambiguity_branch_without_ranking",
    }:
        fail("profile schema must not allow silent pronunciation guessing")
    if not schema.get("allOf"):
        fail("profile schema must define explicit approval conditions")

    if contract.get("public_conversion_enabled") is not False:
        fail("public conversion must remain disabled")
    if contract.get("input_profile_status") != "pending_approval":
        fail("engine pronunciation profile status must remain pending_approval")
    if contract.get("supported_input_profiles") != []:
        fail("the engine must not advertise supported profiles yet")

    documentation = SPEC_DOC.read_text(encoding="utf-8").casefold()
    for marker in (
        "perfiles aprobados: ninguno",
        "perfil por defecto: ninguno",
        "la adivinación automática está desactivada",
        "motor fonético: no implementado",
    ):
        if marker.casefold() not in documentation:
            fail(f"pronunciation documentation lacks marker {marker!r}")

    pending_count = len(registry.get("pending_dimensions", []))
    return len(dimensions), source_count, pending_count


if __name__ == "__main__":
    try:
        dimensions, sources, pending = validate()
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"PRONUNCIATION PROFILE VALIDATION FAILED: {exc}", file=sys.stderr)
        raise SystemExit(1)

    print(
        "PRONUNCIATION PROFILE VALIDATION OK: "
        f"{dimensions} documented dimensions; {sources} source records; "
        f"{pending} dimensions left for later refinement; no default profile and no public converter."
    )
