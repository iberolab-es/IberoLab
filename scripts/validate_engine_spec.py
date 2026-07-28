#!/usr/bin/env python3
"""Validate the specification-only contract for IberoLab's future engine."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data" / "engine" / "phonetic-engine-contract.v1.json"
RESULT_SCHEMA = ROOT / "data" / "schema" / "adaptation-result.schema.json"
SPEC_DOC = ROOT / "docs" / "PHONETIC_ENGINE_SPEC.md"
README = ROOT / "README.md"
ROADMAP = ROOT / "ROADMAP.md"

EXPECTED_PIPELINE = [
    "input_validation",
    "orthographic_normalization",
    "phonetic_normalization",
    "constraint_projection",
    "candidate_generation",
    "candidate_scoring",
    "explanation_generation",
    "graphic_resolution",
]
EXPECTED_LAYERS = [
    "raw_input",
    "normalized_orthography",
    "phonetic_units",
    "adaptation_operations",
    "ranked_candidates",
    "graphic_output",
]
EXPECTED_OPERATIONS = {
    "exact_match",
    "feature_substitution",
    "segment_insertion",
    "segment_deletion",
    "vowel_attachment",
    "syllable_restructuring",
    "ambiguity_branch",
    "allograph_selection",
}
EXPECTED_UNRESOLVED = {
    "spanish_pronunciation_profiles",
    "phonetic_notation_and_features",
    "semisyllabic_constraint_model",
    "rule_evidence_levels",
    "cost_weights",
    "allograph_profiles",
    "confidence_calibration",
}
EXPECTED_DEPENDENCIES = {
    "corpus": "data/corpus/attested-forms.v1.json",
    "minimum_inventory": "data/signs/minimum-inventory.v1.json",
    "graphic_mapping": "data/signs/reference-standard-dual.v1.json",
    "asset_manifest": "data/signs/reference-standard-dual.assets.v1.json",
}
REQUIRED_RESULT_VERSIONS = {
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


def require_markers(label: str, text: str, markers: tuple[str, ...]) -> None:
    missing = [marker for marker in markers if marker not in text]
    if missing:
        fail(f"{label} lacks required specification markers: {missing}")


def validate_contract(contract: dict) -> tuple[int, int, int]:
    if contract.get("schema_version") != "1.0.0":
        fail("engine contract must use schema_version 1.0.0")
    if contract.get("contract_id") != "iberolab-phonetic-adaptation-contract":
        fail("engine contract has an unexpected id")
    if contract.get("status") != "specification_only":
        fail("engine contract must remain specification_only")
    if contract.get("public_conversion_enabled") is not False:
        fail("public conversion must remain disabled")
    if contract.get("target_operation") != "experimental_phonetic_adaptation":
        fail("target operation must be experimental_phonetic_adaptation")
    if contract.get("result_schema") != "data/schema/adaptation-result.schema.json":
        fail("engine contract points to an unexpected result schema")

    exclusions = set(contract.get("exclusions", []))
    required_exclusions = {
        "translation_into_iberian_language",
        "semantic_inference_from_sound_similarity",
        "unqualified_single_answer",
        "silent_token_substitution",
        "unversioned_rule_changes",
        "automatic_allograph_claims",
    }
    if not required_exclusions.issubset(exclusions):
        fail(f"engine contract lacks exclusions: {sorted(required_exclusions - exclusions)}")

    dependencies = contract.get("dependencies", {})
    if dependencies.get("version_binding_required") is not True:
        fail("engine contract must require version binding")
    for key, path in EXPECTED_DEPENDENCIES.items():
        if dependencies.get(key) != path:
            fail(f"engine dependency {key} must be {path!r}")
        if not (ROOT / path).is_file():
            fail(f"engine dependency does not exist: {path}")

    if contract.get("input_profile_status") != "pending_approval":
        fail("input profile status must remain pending_approval")
    if contract.get("supported_input_profiles") != []:
        fail("no input pronunciation profile may be advertised yet")

    pipeline = contract.get("pipeline", [])
    if [item.get("id") for item in pipeline] != EXPECTED_PIPELINE:
        fail("engine pipeline order or identifiers differ from the approved structural contract")
    if [item.get("order") for item in pipeline] != list(range(1, len(EXPECTED_PIPELINE) + 1)):
        fail("engine pipeline order values must be consecutive from 1")
    if any(item.get("implementation_status") != "not_implemented" for item in pipeline):
        fail("every engine stage must remain not_implemented")
    if any(not isinstance(item.get("responsibility"), str) or len(item["responsibility"]) < 20 for item in pipeline):
        fail("every engine stage requires a substantive responsibility")

    layers = contract.get("layers", [])
    if [item.get("id") for item in layers] != EXPECTED_LAYERS:
        fail("engine layer identifiers or order differ from the structural contract")

    operations = contract.get("operation_types", [])
    operation_ids = {item.get("id") for item in operations}
    if operation_ids != EXPECTED_OPERATIONS or len(operations) != len(EXPECTED_OPERATIONS):
        fail("engine operation type set is incomplete or duplicated")
    if any(item.get("definition_status") != "structural_only" for item in operations):
        fail("operation types must remain structural_only until rules are approved")

    cost_model = contract.get("cost_model", {})
    if cost_model.get("status") != "uncalibrated" or cost_model.get("domain") != "non_negative_real":
        fail("cost model must remain uncalibrated and non-negative")
    if cost_model.get("weights") != {}:
        fail("cost weights must remain empty until documented and approved")
    tie_policy = cost_model.get("tie_policy", {})
    if tie_policy.get("preserve_exact_ties") is not True or tie_policy.get("near_tie_threshold") is not None:
        fail("exact ties must be preserved and near-tie threshold must remain undefined")

    confidence = contract.get("confidence_model", {})
    if confidence.get("status") != "uncalibrated":
        fail("confidence model must remain uncalibrated")
    if confidence.get("numeric_percentage_prohibited") is not True:
        fail("numeric confidence percentages must remain prohibited")
    if confidence.get("allowed_current_band") != "not_calibrated":
        fail("current confidence band must remain not_calibrated")

    candidate_policy = contract.get("candidate_policy", {})
    for key in ("single_output_not_guaranteed", "preserve_exact_ties", "preserve_profile_ambiguity", "silent_empty_output_forbidden"):
        if candidate_policy.get(key) is not True:
            fail(f"candidate policy must enforce {key}")
    if candidate_policy.get("maximum_candidates") is not None:
        fail("maximum candidate count must remain undefined")

    invariants = contract.get("invariants", [])
    if not isinstance(invariants, list) or len(invariants) < 10 or len(set(invariants)) != len(invariants):
        fail("engine contract requires at least ten unique invariants")
    invariant_text = " ".join(invariants)
    for marker in ("No phonetic or graphic similarity", "No unrepresentable source unit", "Rendering cannot alter"):
        if marker not in invariant_text:
            fail(f"engine invariants lack marker {marker!r}")

    gates = contract.get("implementation_gates", {})
    if not gates or any(value is not False for value in gates.values()):
        fail("every implementation and publication gate must remain false")
    if gates.get("public_engine_may_be_enabled") is not False:
        fail("public engine gate must remain false")

    unresolved = contract.get("unresolved_decisions", [])
    unresolved_ids = {item.get("id") for item in unresolved}
    if unresolved_ids != EXPECTED_UNRESOLVED or len(unresolved) != len(EXPECTED_UNRESOLVED):
        fail("unresolved decision set differs from the approved contract")
    if any(not item.get("blocking_for_implementation") and not item.get("blocking_for_publication") for item in unresolved):
        fail("every unresolved decision must block implementation or publication")

    return len(pipeline), len(operations), len(invariants)


def validate_result_schema(schema: dict) -> tuple[int, int]:
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        fail("adaptation result schema must use JSON Schema draft 2020-12")
    if schema.get("title") != "IberoLab experimental phonetic adaptation result":
        fail("adaptation result schema has an unexpected title")
    properties = schema.get("properties", {})
    if properties.get("classification", {}).get("const") != "experimental_phonetic_adaptation":
        fail("result schema must classify outputs as experimental phonetic adaptation")
    if properties.get("translation_claim", {}).get("const") is not False:
        fail("result schema must prohibit translation claims")
    if properties.get("semantic_claims", {}).get("maxItems") != 0:
        fail("result schema must prohibit semantic claims")

    source_versions = properties.get("source_versions", {})
    if set(source_versions.get("required", [])) != REQUIRED_RESULT_VERSIONS:
        fail("result schema must require every version-bound dependency")

    required_top = {
        "schema_version",
        "classification",
        "translation_claim",
        "contract_version",
        "source_versions",
        "input",
        "layers",
        "candidates",
        "warnings",
        "semantic_claims",
    }
    if set(schema.get("required", [])) != required_top:
        fail("result schema top-level required fields differ from the contract")

    definitions = schema.get("$defs", {})
    required_definitions = {"phonetic_unit", "cost_component", "adaptation_operation", "confidence", "explanation_step", "candidate"}
    if set(definitions) != required_definitions:
        fail("result schema definition set is incomplete or contains unreviewed definitions")

    candidate_required = set(definitions["candidate"].get("required", []))
    for field in ("token_sequence", "graphic_reference_ids", "operations", "total_cost", "confidence", "explanation_steps"):
        if field not in candidate_required:
            fail(f"candidate result schema must require {field}")
    if definitions["candidate"]["properties"]["total_cost"].get("minimum") != 0:
        fail("candidate total cost must be non-negative")

    confidence = definitions["confidence"]
    if "not_calibrated" not in confidence["properties"]["status"].get("enum", []):
        fail("confidence schema must support not_calibrated")

    operation_types = set(definitions["adaptation_operation"]["properties"]["operation_type"].get("enum", []))
    if operation_types != EXPECTED_OPERATIONS:
        fail("result schema operation types differ from the engine contract")

    return len(definitions), len(required_top)


def validate_documents() -> None:
    specification = SPEC_DOC.read_text(encoding="utf-8")
    require_markers(
        "PHONETIC_ENGINE_SPEC",
        specification,
        (
            "No implementa reglas español→ibérico",
            "conversión pública: desactivada",
            "Los pesos permanecen vacíos",
            "La confianza actual es `not_calibrated`",
            "No se impondrá una variedad regional marcada",
            "Una decisión de ingeniería nunca podrá etiquetarse como hecho ibérico documentado",
            "La implementación seguirá desactivada",
        ),
    )
    readme = README.read_text(encoding="utf-8")
    require_markers("README", readme, ("todavía no ofrece un conversor", "futuros módulos de adaptación fonética"))
    roadmap = ROADMAP.read_text(encoding="utf-8")
    require_markers("ROADMAP", roadmap, ("Especificación permitida antes de implementar", "Implementación bloqueada"))


def validate() -> tuple[int, int, int, int, int]:
    contract = load_json(CONTRACT)
    schema = load_json(RESULT_SCHEMA)
    pipeline_count, operation_count, invariant_count = validate_contract(contract)
    definition_count, required_count = validate_result_schema(schema)
    validate_documents()
    return pipeline_count, operation_count, invariant_count, definition_count, required_count


if __name__ == "__main__":
    try:
        pipeline_count, operation_count, invariant_count, definition_count, required_count = validate()
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"ENGINE SPEC VALIDATION FAILED: {exc}", file=sys.stderr)
        raise SystemExit(1)
    print(
        "ENGINE SPEC VALIDATION OK: "
        f"{pipeline_count} specification-only stages; {operation_count} structural operation types; "
        f"{invariant_count} invariants; {definition_count} result definitions; {required_count} required result fields; "
        "public conversion, profiles, weights and calibrated confidence remain disabled."
    )
