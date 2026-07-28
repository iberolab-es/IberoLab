#!/usr/bin/env python3
"""Synchronize IberoLab's local SVG manifest with public renderer files.

This command is idempotent for the current nineteen-token seed corpus. It does
not choose new signs; it only propagates the already reviewed manifest and the
documented m1 → ń resolution.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "signs" / "reference-standard-dual.assets.v1.json"
MAPPING = ROOT / "data" / "signs" / "reference-standard-dual.v1.json"
INDEX = ROOT / "docs" / "index.html"
SELF_TEST = ROOT / "docs" / "test.html"
MATRIX = ROOT / "data" / "tests" / "browser-matrix.v1.json"
TOKEN_ORDER = ["a", "e", "i", "u", "gi", "ke", "ki", "ba", "da", "de", "di", "ta", "s", "ś", "r", "ŕ", "l", "n", "ń"]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def local_web_paths(manifest: dict) -> dict[str, str]:
    assets = {item["token"]: item for item in manifest["assets"]}
    if set(assets) != set(TOKEN_ORDER):
        raise ValueError("manifest token set does not match the nineteen-token renderer set")
    result: dict[str, str] = {}
    for token in TOKEN_ORDER:
        path = assets[token]["local_path"]
        if not isinstance(path, str) or not path.startswith("docs/") or not path.endswith(".svg"):
            raise ValueError(f"{token!r}: invalid public local path")
        if not (ROOT / path).is_file():
            raise ValueError(f"{token!r}: local asset does not exist")
        result[token] = path.removeprefix("docs/")
    return result


def js_sign_block(paths: dict[str, str], indent: str = "  ") -> str:
    lines = [f"{indent}const SIGNS = {{"]
    for token in TOKEN_ORDER:
        lines.append(f"{indent}  {json.dumps(token, ensure_ascii=False)}: {json.dumps(paths[token], ensure_ascii=False)},")
    lines[-1] = lines[-1].removesuffix(",")
    lines.append(f"{indent}}};")
    return "\n".join(lines)


def replace_sign_block(path: Path, paths: dict[str, str]) -> None:
    text = path.read_text(encoding="utf-8")
    updated, count = re.subn(r"  const SIGNS = \{.*?\n  \};", js_sign_block(paths), text, count=1, flags=re.DOTALL)
    if count != 1:
        raise ValueError(f"{path.relative_to(ROOT)}: expected one SIGNS block, found {count}")
    if "Special:Redirect/file" in updated or "COMMONS_REDIRECT" in updated or "const COMMONS" in updated:
        raise ValueError(f"{path.relative_to(ROOT)} still contains a remote SVG dependency")
    path.write_text(updated, encoding="utf-8")


def update_mapping(manifest: dict) -> None:
    mapping = load_json(MAPPING)
    assets = {item["token"]: item for item in manifest["assets"]}
    for sign in mapping["signs"]:
        token = sign["token"]
        asset = assets.get(token)
        if not asset:
            raise ValueError(f"mapping contains token without local asset: {token!r}")
        sign["local_path"] = asset["local_path"]
        if token == "ń":
            sign.update(
                {
                    "reference_id": asset["reference_id"],
                    "file_name": asset["source_file_name"],
                    "graphic_status": "local_attested_variant_svg_available",
                    "paleographic_variant": asset["paleographic_variant"],
                    "traditional_transcription": asset["traditional_transcription"],
                    "project_transcription": asset["project_transcription"],
                    "phonological_scope": asset["phonological_scope"],
                    "graphic_scope": asset["graphic_scope"],
                    "evidence": asset["scholarly_evidence"],
                }
            )
        else:
            sign["graphic_status"] = "local_reference_svg_available"
    mapping["status"] = "local_reference_renderer_complete_for_seed_corpus"
    mapping["asset_manifest"] = MANIFEST.relative_to(ROOT).as_posix()
    write_json(MAPPING, mapping)


def update_matrix() -> None:
    matrix = load_json(MATRIX)
    matrix["schema_version"] = "1.3.0"
    matrix["updated_on"] = "2026-07-28"
    matrix["expected"]["mapped_svg_tokens"] = 19
    matrix["expected"]["explicit_pending_tokens"] = []
    matrix["expected"]["asset_mode"] = "local_repository"
    matrix["expected"]["resolved_transcriptions"] = {
        "ń": {"paleographic_variant": "m1", "traditional_transcription": "m", "current_transcription": "ń"}
    }
    write_json(MATRIX, matrix)


def main() -> int:
    manifest = load_json(MANIFEST)
    if manifest.get("asset_count") != 19 or manifest.get("unresolved") != []:
        raise ValueError("local asset manifest must contain nineteen resolved SVGs")
    paths = local_web_paths(manifest)
    update_mapping(manifest)
    replace_sign_block(INDEX, paths)
    replace_sign_block(SELF_TEST, paths)
    update_matrix()
    print("LOCAL ASSET INTEGRATION OK: nineteen resolved SVGs synchronized with renderer, self-test, mapping and matrix.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"LOCAL ASSET INTEGRATION FAILED: {exc}", file=sys.stderr)
        raise SystemExit(1)
