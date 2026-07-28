#!/usr/bin/env python3
"""Validate the specification-only European Spanish pronunciation registry."""
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
README = ROOT / "README.md"
ROADMAP = ROOT / "ROADMAP.md"

EXPECTED_DIMENSIONS = {
    "sibilant_system": {"distinction", "seseo", "ceceo"},
    "palatal_lateral_system": {"yeismo", "y_ll_distinction"},
    "vowel_sequence_interpretation": {
        "lexically_fixed_diphthong",
        "lexically_fixed_hiatus",
        "profile_conditioned",
        "ambiguity_branch",
    },
    "stress_assignment_source": {
        "orthography_and_reviewed_lexicon",
        "user_supplied_pronunciation",
        "ambiguity_branch",
    },
}

EXPECTED_PENDING = {
    "coda_s_realization",
    "intervocalic_d_reduction",
    "velar_fricative_realization",
    "word_final_n_realization",
    "rhotic_coda_and_cluster_realization",
    "loanword_and_proper_name_pronunciation",
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


def validate_profile_schema(schema: dict) -> None:
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        fail("profile schema must use JSON Schema draft 2020-12")
    if schema.get("title") != "IberoLab Spanish pronunciation profile":
        fail("profile schema title is unexpected")

    expected_required = {
        "schema_version",
        "profile_id",
        "profile_version",
        "status",
        "language_tag",
        "geographic_scope",
        "register_scope",
        "label",
        "declared_dimensions",
        "lexical_exception_policy",
        "unknown_word_policy",
        "source_set",
        "review",
    }
    if set(schema.get("required", [])) != expected_required:
        fail("profile schema required fields differ from the contract")

    properties = schema.get("properties", {})
    if properties.get("language_tag", {}).get("const") != "es-ES":
        fail("profile schema must target es-ES")
    statuses = set(properties.get("status", {}).get("enum", []))
    if not {"draft", "preview", "under_review", "approved", "deprecated"}.issubset(statuses):
        fail("profile schema lacks required lifecycle states")
    unknown_policy = set(properties.get("unknown_word_policy", {}).get("enum", []))
    if unknown_policy != {
        "block",
        "require_user_pronunciation",
        "ambiguity_branch_without_ranking",
    }:
        fail("unknown-word policy must not permit silent guessing")

    approval_rules = schema.get("allOf", [])
    if not approval_rules:
        fail("profile schema must contain a top-level approval condition")
    serialized = json.dumps(approval_rules, ensure_ascii=False)
    for marker in ('"approved"', '"internal_review"', '"external_review"', '"approval_date"'):
        if marker not in serialized:
            fail(f"profile approval condition lacks {marker}")


def validate_registry(registry: dict) -> tuple[int, int, int]:
    if registry.get("schema_version") != "1.0.0":
        fail("pronunciation registry must use version 1.0.0")
    if registry.get("registry_id") != "iberolab-spanish-pronunciation-dimensions":
        fail("pronunciation registry id is unexpected")
    if registry.get("status") != "specification_only":
        fail("pronunciation registry must remain specification_only")
    if registry.get("language_tag") != "es-ES":
        fail("pronunciation registry must target es-ES")
    if registry.get("public_profile_selection_enabled") is not False:
        fail("public pronunciation-profile selection must remain disabled")
    if registry.get("default_profile_id") is not None:
        fail("no default pronunciation profile may be selected yet")
    if registry.get("approved_profiles") != []:
        fail("no pronunciation profile is approved yet")
    if registry.get("profile_schema") != "data/schema/pronunciation-profile.schema.json":
        fail("pronunciation registry points to an unexpected schema")

    policy = registry.get("policy", {})
    for key in (
        "no_silent_default",
        "variation_must_be_declared",
        "orthography_is_not_pronunciation",
        "reference_description_is_not_universal_profile",
        "profile_version_required_before_implementation",
    ):
        if policy.get(key) is not True:
            fail(f"pronunciation policy must enforce {key}")
    if policy.get("unknown_word_guessing_enabled") is not False:
        fail("unknown-word guessing must remain disabled")

    dimensions = registry.get("documented_dimensions", [])
    by_id = {item.get("dimension_id"): item for item in dimensions}
    if set(by_id) != set(EXPECTED_DIMENSIONS) or len(dimensions) != len(EXPECTED_DIMENSIONS):
        fail("documented pronunciation dimensions are incomplete or duplicated")

    source_count = 0
    for dimension_id, expected_options in EXPECTED_DIMENSIONS.items():
        item = by_id[dimension_id]
        if item.get("default_option") is not None:
            fail(f"{dimension_id}: a silent default is forbidden")
        option_ids = {option.get("option_id") for option in item.get("options", [])}
        if option_ids != expected_options:
            fail(f"{dimension_id}: option set differs from the registry contract")
        if len(item.get("description", "")) < 20:
            fail(f"{dimension_id}: substantive description is required")
        sources = item.get("sources", [])
        if not sources:
            fail(f"{dimension_id}: at least one source is required")
        for index, source in enumerate(sources):
            validate_https(source.get("url", ""), f"{dimension_id}.sources[{index}]")
            if source.get("source_type") not in {
                "academy_reference",
                "peer_reviewed_phonetic_description",
            }:
                fail(f"{dimension_id}: source type is not allowed")
            if len(source.get("scope", "")) < 10:
                fail(f"{dimension_id}: source scope is required")
        source_count += len(sources)

    references = registry.get("reference_descriptions", [])
    if len(references) != 1:
        fail("exactly one reference-only phonetic description is required")
    reference = references[0]
    if reference.get("reference_id") != "formal_castilian_jipa_2003":
        fail("reference-only phonetic description is unexpected")
    if reference.get("status") != "reference_only_not_approved_profile":
        fail("reference description must not be treated as an approved profile")
    validate_https(reference.get("url", ""), "reference_descriptions[0]")

    pending = registry.get("pending_dimensions", [])
    pending_ids = {item.get("dimension_id") for item in pending}
    if pending_ids != EXPECTED_PENDING or len(pending) != len(EXPECTED_PENDING):
        fail("pending pronunciation dimensions are incomplete or duplicated")
    if any(len(item.get("reason", "")) < 20 for item in pending):
        fail("every pending dimension requires a substantive reason")

    gates = registry.get("approval_gates", {})
    required_closed = {
        "internal_phonetic_review",
        "external_phonetic_review",
        "dimension_sources_reviewed",
        "default_profile_approved",
        "public_profile_selection_may_be_enabled",
    }
    if gates.get("profile_schema_validated") is not True:
        fail("profile schema gate must be validated")
    if any(gates.get(key) is not False for key in required_closed):
        fail("review and publication gates must remain closed")

    return len(dimensions), source_count, len(pending)


def validate_engine_contract(contract: dict) -> None:
    if contract.get("input_profile_status") != "pending_approval":
        fail("engine input profile status must remain pending_approval")
    if contract.get("supported_input_profiles") != []:
        fail("engine must not advertise a supported profile yet")
    gates = contract.get("implementation_gates", {})
    if gates.get("approved_spanish_pronunciation_profile") is not False:
        fail("Spanish pronunciation profile gate must remain closed")
    if gates.get("public_engine_may_be_enabled") is not False:
        fail("public engine gate must remain closed")


def validate_documents() -> None:
    specification = SPEC_DOC.read_text(encoding="utf-8").casefold()
    for marker in (
        "perfiles aprobados: ninguno",
        "perfil por defecto: ninguno",
        "no existe un «español de españa» implícito",
        "no existe opción por defecto",
        "la adivinación automática está desactivada",
        "motor fonético: no implementado",
    ):
        if marker.casefold() not in specification:
            fail(f"pronunciation documentation lacks marker {marker!r}")

    readme = README.read_text(encoding="utf-8").casefold()
    if "no contiene reglas lingüísticas aprobadas ni habilita un conversor" not in readme:
        fail("README must continue to state that no converter is enabled")

    roadmap = ROADMAP.read_text(encoding="utf-8").casefold()
    if "definir perfiles de pronunciación de español europeo" not in roadmap:
        fail("ROADMAP must retain the pronunciation-profile task")


def validate() -> tuple[int, int, int]:
    validate_profile_schema(load_json(PROFILE_SCHEMA))
    dimension_count, source_count, pending_count = validate_registry(load_json(REGISTRY))
    validate_engine_contract(load_json(ENGINE_CONTRACT))
    validate_documents()
    return dimension_count, source_count, pending_count


if __name__ == "__main__":
    try:
        dimensions, sources, pending = validate()
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"PRONUNCIATION PROFILE VALIDATION FAILED: {exc}", file=sys.stderr)
        raise SystemExit(1)

    print(
        "PRONUNCIATION PROFILE VALIDATION OK: "
        f"{dimensions} documented dimensions; {sources} scoped source records; "
        f"{pending} dimensions explicitly pending; no default or approved profile; public selection disabled."
    )
