#!/usr/bin/env python3
"""Validate the mutually exclusive success and blocked engine envelopes."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "engine" / "schema-registry.v1.json"
SUCCESS_SCHEMA = ROOT / "data" / "schema" / "adaptation-result.schema.json"
BLOCKED_SCHEMA = ROOT / "data" / "schema" / "adaptation-blocked.schema.json"
SPEC_DOC = ROOT / "docs" / "PHONETIC_ENGINE_SPEC.md"
REQUIRED_VERSIONS = {
    "engine",
    "rule_set",
    "cost_model",
    "confidence_model",
    "corpus",
    "minimum_inventory",
    "graphic_mapping",
    "asset_manifest",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def fail(message: str) -> None:
    raise ValueError(message)


def validate_version_object(schema: dict, label: str) -> None:
    versions = schema.get("properties", {}).get("source_versions", {})
    if set(versions.get("required", [])) != REQUIRED_VERSIONS:
        fail(f"{label} must require every version-bound dependency")


def validate() -> tuple[int, int, int]:
    registry = load_json(REGISTRY)
    success = load_json(SUCCESS_SCHEMA)
    blocked = load_json(BLOCKED_SCHEMA)

    if registry.get("schema_version") != "1.0.0":
        fail("engine schema registry must use version 1.0.0")
    if registry.get("registry_id") != "iberolab-phonetic-engine-schema-registry":
        fail("engine schema registry has an unexpected id")
    if registry.get("contract") != "data/engine/phonetic-engine-contract.v1.json":
        fail("engine schema registry points to an unexpected contract")
    if registry.get("public_conversion_enabled") is not False:
        fail("engine schema registry must keep public conversion disabled")
    if registry.get("selection_rule") != "Exactly one execution-state schema must apply to a serialized engine response.":
        fail("engine schema registry lacks the exclusivity rule")

    states = registry.get("execution_states", [])
    if len(states) != 2 or {item.get("status") for item in states} != {"success", "blocked"}:
        fail("engine schema registry must contain exactly success and blocked states")
    by_status = {item["status"]: item for item in states}
    expected = {
        "success": {
            "schema": "data/schema/adaptation-result.schema.json",
            "candidate_policy": "one_or_more_candidates_required",
            "semantic_claims_policy": "must_be_empty",
        },
        "blocked": {
            "schema": "data/schema/adaptation-blocked.schema.json",
            "candidate_policy": "no_candidates_allowed",
            "semantic_claims_policy": "must_be_empty",
        },
    }
    for status, fields in expected.items():
        for key, value in fields.items():
            if by_status[status].get(key) != value:
                fail(f"{status} registry entry has invalid {key}")
        if not (ROOT / by_status[status]["schema"]).is_file():
            fail(f"{status} schema file does not exist")

    if success.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        fail("success schema must use JSON Schema draft 2020-12")
    success_properties = success.get("properties", {})
    if success_properties.get("classification", {}).get("const") != "experimental_phonetic_adaptation":
        fail("success schema has an invalid classification")
    if success_properties.get("translation_claim", {}).get("const") is not False:
        fail("success schema must prohibit translation claims")
    if success_properties.get("semantic_claims", {}).get("maxItems") != 0:
        fail("success schema must prohibit semantic claims")
    if success_properties.get("candidates", {}).get("minItems") != 1:
        fail("success schema must require at least one candidate")
    validate_version_object(success, "success schema")

    if blocked.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        fail("blocked schema must use JSON Schema draft 2020-12")
    blocked_properties = blocked.get("properties", {})
    if blocked_properties.get("execution_status", {}).get("const") != "blocked":
        fail("blocked schema must identify execution_status=blocked")
    if blocked_properties.get("classification", {}).get("const") != "experimental_phonetic_adaptation":
        fail("blocked schema has an invalid classification")
    if blocked_properties.get("translation_claim", {}).get("const") is not False:
        fail("blocked schema must prohibit translation claims")
    if blocked_properties.get("semantic_claims", {}).get("maxItems") != 0:
        fail("blocked schema must prohibit semantic claims")
    if blocked_properties.get("candidates", {}).get("maxItems") != 0:
        fail("blocked schema must prohibit candidates")
    if blocked_properties.get("blocking_reasons", {}).get("minItems") != 1:
        fail("blocked schema must require at least one blocking reason")
    validate_version_object(blocked, "blocked schema")

    success_required = set(success.get("required", []))
    blocked_required = set(blocked.get("required", []))
    for common in ("classification", "translation_claim", "contract_version", "source_versions", "input", "warnings", "candidates", "semantic_claims"):
        if common not in success_required or common not in blocked_required:
            fail(f"both execution schemas must require {common}")
    if "blocking_reasons" in success_required:
        fail("success schema must not require blocking reasons")
    if "blocking_reasons" not in blocked_required:
        fail("blocked schema must require blocking reasons")

    specification = SPEC_DOC.read_text(encoding="utf-8")
    specification_casefold = specification.casefold()
    for marker in (
        "un intento bloqueado",
        "no puede presentar candidatos parciales",
        "data/schema/adaptation-blocked.schema.json",
        "data/engine/schema-registry.v1.json",
    ):
        if marker.casefold() not in specification_casefold:
            fail(f"engine specification lacks blocked-state marker {marker!r}")

    return len(states), len(success_required), len(blocked_required)


if __name__ == "__main__":
    try:
        state_count, success_required_count, blocked_required_count = validate()
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"ENGINE SCHEMA REGISTRY VALIDATION FAILED: {exc}", file=sys.stderr)
        raise SystemExit(1)
    print(
        "ENGINE SCHEMA REGISTRY VALIDATION OK: "
        f"{state_count} exclusive execution states; {success_required_count} required success fields; "
        f"{blocked_required_count} required blocked fields; blocked attempts cannot expose candidates or semantic claims."
    )
