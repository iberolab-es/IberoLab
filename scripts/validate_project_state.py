#!/usr/bin/env python3
"""Validate consistency between IberoLab's current data and current-state docs.

Historical reports and changelog entries may legitimately describe older
18-asset states. This validator targets only datasets and documents that claim
to describe the present architecture and roadmap.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "signs" / "reference-standard-dual.assets.v1.json"
MAPPING = ROOT / "data" / "signs" / "reference-standard-dual.v1.json"
INVENTORY = ROOT / "data" / "signs" / "minimum-inventory.v1.json"
MATRIX = ROOT / "data" / "tests" / "browser-matrix.v1.json"
SELF_TEST = ROOT / "docs" / "test.html"
README = ROOT / "README.md"
ROADMAP = ROOT / "ROADMAP.md"
METHODOLOGY = ROOT / "docs" / "METHODOLOGY.md"
CORPUS_DOC = ROOT / "docs" / "ATTESTED_CORPUS.md"

CURRENT_DOCS = {
    "README": README,
    "ROADMAP": ROADMAP,
    "METHODOLOGY": METHODOLOGY,
    "ATTESTED_CORPUS": CORPUS_DOC,
}

STALE_CURRENT_STATE_PHRASES = (
    "18 de los 19 tokens",
    "dieciocho SVG de referencia dentro del repositorio",
    "Resolver paleográficamente `ń` o mantenerlo formalmente pendiente",
    "`ń` como token explícitamente pendiente",
    "`ń` permanece sin signo gráfico asignado",
    '"graphic_status":"pending_verified_svg"',
    '"allograph_status":"not_selected"',
)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def require_markers(label: str, text: str, markers: tuple[str, ...]) -> None:
    missing = [marker for marker in markers if marker not in text]
    if missing:
        raise ValueError(f"{label} lacks current-state markers: {missing}")


def validate() -> tuple[int, int, int, int]:
    manifest = load_json(MANIFEST)
    mapping = load_json(MAPPING)
    inventory = load_json(INVENTORY)
    matrix = load_json(MATRIX)

    assets = manifest.get("assets", [])
    if manifest.get("asset_count") != 19 or len(assets) != 19:
        raise ValueError("current manifest must contain nineteen assets")
    if manifest.get("unresolved") != []:
        raise ValueError("current manifest must have no unresolved graphic tokens")
    asset_tokens = {item.get("token") for item in assets}
    if len(asset_tokens) != 19 or "ń" not in asset_tokens:
        raise ValueError("current manifest token set must contain nineteen unique tokens including ń")

    signs = {item.get("token"): item for item in mapping.get("signs", [])}
    inventory_signs = {item.get("transliteration"): item for item in inventory.get("signs", [])}
    if set(signs) != asset_tokens or set(inventory_signs) != asset_tokens:
        raise ValueError("inventory, mapping and manifest token sets differ")
    if inventory.get("schema_version") != "1.1.0":
        raise ValueError("minimum inventory must use schema 1.1.0")
    if inventory.get("status") != "transcription_inventory_with_graphic_references":
        raise ValueError("minimum inventory status is obsolete")
    if len(inventory_signs) != 19:
        raise ValueError("minimum inventory must contain nineteen unique token entries")

    for token in asset_tokens:
        inventory_item = inventory_signs[token]
        mapping_item = signs[token]
        asset_item = next(item for item in assets if item.get("token") == token)
        if inventory_item.get("graphic_reference_id") != mapping_item.get("reference_id"):
            raise ValueError(f"{token!r}: inventory and mapping reference IDs differ")
        if inventory_item.get("graphic_reference_id") != asset_item.get("reference_id"):
            raise ValueError(f"{token!r}: inventory and manifest reference IDs differ")
        if inventory_item.get("local_path") != mapping_item.get("local_path"):
            raise ValueError(f"{token!r}: inventory and mapping paths differ")
        if inventory_item.get("local_path") != asset_item.get("local_path"):
            raise ValueError(f"{token!r}: inventory and manifest paths differ")
        if inventory_item.get("graphic_status") != mapping_item.get("graphic_status"):
            raise ValueError(f"{token!r}: inventory and mapping graphic statuses differ")
        if str(inventory_item.get("graphic_status", "")).startswith("pending_"):
            raise ValueError(f"{token!r}: inventory retains a pending graphic status")

    nasal = signs["ń"]
    nasal_inventory = inventory_signs["ń"]
    expected_nasal = {
        "graphic_status": "local_attested_variant_svg_available",
        "paleographic_variant": "m1",
        "traditional_transcription": "m",
        "project_transcription": "ń",
    }
    for key, value in expected_nasal.items():
        if nasal.get(key) != value or nasal_inventory.get(key) != value:
            raise ValueError(f"current ń data has invalid {key}")

    expected = matrix.get("expected", {})
    if matrix.get("schema_version") != "1.3.0":
        raise ValueError("current browser matrix must use schema 1.3.0")
    if expected.get("mapped_svg_tokens") != 19 or expected.get("explicit_pending_tokens") != []:
        raise ValueError("current browser matrix must expect nineteen SVGs and no pending tokens")

    self_test = SELF_TEST.read_text(encoding="utf-8")
    require_markers(
        "self-test",
        self_test,
        (
            'version: "1.2.0"',
            'asset_mode: "local_repository"',
            'const EXPECTED_PENDING = new Set([]);',
            "0/19",
            "variant-m1-nasal.svg",
            "ń resuelto mediante la variante m1 documentada",
        ),
    )

    current_texts = {label: path.read_text(encoding="utf-8") for label, path in CURRENT_DOCS.items()}
    for label, text in current_texts.items():
        stale = [phrase for phrase in STALE_CURRENT_STATE_PHRASES if phrase in text]
        if stale:
            raise ValueError(f"{label} contains stale current-state phrases: {stale}")

    require_markers(
        "README",
        current_texts["README"],
        (
            "diecinueve SVG locales",
            "cero tokens gráficos pendientes",
            "variante paleográfica `m1`",
            "regresión automática sobre Chromium, Firefox y WebKit",
            "todavía no ofrece un conversor",
        ),
    )
    require_markers(
        "ROADMAP",
        current_texts["ROADMAP"],
        (
            "Integrar los 19 SVG",
            "Reconstruir las once formas sin salidas vacías ni tokens gráficos pendientes",
            "Especificación permitida antes de implementar",
            "Implementación bloqueada",
            "pruebas manuales actuales del renderizador",
        ),
    )
    require_markers(
        "METHODOLOGY",
        current_texts["METHODOLOGY"],
        (
            "El caso `m1` / `m` / `ń`",
            "especificación formal",
            "La implementación pública permanecerá bloqueada",
            "no sustituyen las pruebas manuales",
        ),
    )
    require_markers(
        "ATTESTED_CORPUS",
        current_texts["ATTESTED_CORPUS"],
        (
            "diecinueve tokens",
            "diecinueve recursos SVG locales",
            "variante paleográfica `m1`",
            "no son facsímiles",
        ),
    )

    return len(assets), len(signs), len(inventory_signs), len(CURRENT_DOCS)


if __name__ == "__main__":
    try:
        asset_count, mapping_count, inventory_count, document_count = validate()
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"PROJECT STATE VALIDATION FAILED: {exc}", file=sys.stderr)
        raise SystemExit(1)
    print(
        "PROJECT STATE VALIDATION OK: "
        f"{asset_count} manifest assets; {mapping_count} mapped tokens; {inventory_count} inventory entries; "
        f"{document_count} current-state documents aligned with the m1/m/ń resolution and phase gates."
    )
