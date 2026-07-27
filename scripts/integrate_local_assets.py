#!/usr/bin/env python3
"""Switch IberoLab's renderer and self-test from remote to local SVG assets."""
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
TESTING = ROOT / "docs" / "TESTING.md"

TOKEN_ORDER = ["a", "e", "i", "u", "gi", "ke", "ki", "ba", "da", "de", "di", "ta", "s", "ś", "r", "ŕ", "l", "n"]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def local_web_paths(manifest: dict) -> dict[str, str]:
    assets = {item["token"]: item for item in manifest["assets"]}
    if set(assets) != set(TOKEN_ORDER):
        raise ValueError("manifest token set does not match the renderer token set")
    result: dict[str, str] = {}
    for token in TOKEN_ORDER:
        path = assets[token]["local_path"]
        if not path.startswith("docs/"):
            raise ValueError(f"{token!r}: local path must be inside docs/")
        result[token] = path.removeprefix("docs/")
    return result


def js_sign_block(paths: dict[str, str], indent: str = "  ") -> str:
    lines = [f'{indent}const SIGNS = {{']
    for token in TOKEN_ORDER:
        lines.append(f'{indent}  {json.dumps(token, ensure_ascii=False)}: {json.dumps(paths[token], ensure_ascii=False)},')
    lines[-1] = lines[-1].removesuffix(",")
    lines.append(f"{indent}}};")
    return "\n".join(lines)


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if text.count(old) != 1:
        raise ValueError(f"{label}: expected exactly one literal replacement, found {text.count(old)}")
    return text.replace(old, new, 1)


def regex_once(text: str, pattern: str, replacement: str, label: str) -> str:
    updated, count = re.subn(pattern, replacement, text, count=1, flags=re.DOTALL)
    if count != 1:
        raise ValueError(f"{label}: expected exactly one regex replacement, found {count}")
    return updated


def update_mapping(manifest: dict) -> None:
    mapping = load_json(MAPPING)
    assets = {item["token"]: item for item in manifest["assets"]}
    for sign in mapping["signs"]:
        token = sign["token"]
        if token in assets:
            sign["graphic_status"] = "local_reference_svg_available"
            sign["local_path"] = assets[token]["local_path"]
        elif token == "ń":
            sign.pop("local_path", None)
            if not sign.get("graphic_status", "").startswith("pending_"):
                raise ValueError("ń must remain explicitly pending")
        else:
            raise ValueError(f"mapping contains unexpected token without local asset: {token!r}")
    mapping["status"] = "local_provisional_reference_renderer"
    mapping["asset_manifest"] = MANIFEST.relative_to(ROOT).as_posix()
    write_json(MAPPING, mapping)


def update_index(paths: dict[str, str]) -> None:
    text = INDEX.read_text(encoding="utf-8")
    text = regex_once(text, r'\n  const COMMONS_REDIRECT = "[^"]+";\n', "\n", "remove remote index base")
    text = regex_once(text, r"  const SIGNS = \{.*?\n  \};", js_sign_block(paths), "replace index sign map")
    text = regex_once(
        text,
        r"  function assetUrl\(fileName\) \{\n    return COMMONS_REDIRECT \+ encodeURIComponent\(fileName\);\n  \}",
        "  function assetUrl(localPath) {\n    return localPath;\n  }",
        "replace index asset URL function",
    )
    text = text.replace('      image.referrerPolicy = "no-referrer";\n', "")
    old_footer = "Recursos gráficos provisionales: serie “Sign Iber Noro Dual 01–38”, BotaFlo, Wikimedia Commons, CC0. La auditoría documental está versionada en el repositorio y las grafías específicas de cada testimonio siguen en revisión."
    new_footer = "Recursos gráficos locales de referencia: 18 SVG de la serie “Sign Iber Noro Dual 01–38”, BotaFlo, Wikimedia Commons, CC0. Su procedencia, URL resuelta, tamaño y SHA-256 están versionados en el manifiesto del repositorio. Las grafías específicas de cada testimonio siguen en revisión."
    text = replace_once(text, old_footer, new_footer, "replace index provenance footer")
    if "Special:Redirect/file" in text or "COMMONS_REDIRECT" in text:
        raise ValueError("index still contains a remote SVG dependency")
    INDEX.write_text(text, encoding="utf-8")


def update_self_test(paths: dict[str, str]) -> None:
    text = SELF_TEST.read_text(encoding="utf-8")
    text = regex_once(text, r'\n  const COMMONS = "[^"]+";\n', "\n", "remove remote self-test base")
    text = regex_once(text, r"  const SIGNS = \{.*?\n  \};", js_sign_block(paths), "replace self-test sign map")
    text = replace_once(
        text,
        "  function imageUrl(file) { return COMMONS + encodeURIComponent(file); }",
        "  function imageUrl(localPath) { return localPath; }",
        "replace self-test image URL function",
    )
    text = replace_once(text, '      version: "1.0.0",', '      version: "1.1.0",\n      asset_mode: "local_repository",', "update self-test payload")
    text = replace_once(
        text,
        '      ? "Prueba técnica superada: 11 formas evaluadas, ninguna salida vacía y ń permanece explícitamente pendiente."',
        '      ? "Prueba técnica superada: 11 formas evaluadas, 18 SVG locales cargados, ninguna salida vacía y ń permanece explícitamente pendiente."',
        "update self-test success message",
    )
    if "Special:Redirect/file" in text or "const COMMONS" in text:
        raise ValueError("self-test still contains a remote SVG dependency")
    SELF_TEST.write_text(text, encoding="utf-8")


def update_matrix() -> None:
    matrix = load_json(MATRIX)
    matrix["schema_version"] = "1.2.0"
    matrix["updated_on"] = "2026-07-28"
    matrix["expected"]["asset_mode"] = "local_repository"
    repeat_note = "Repeat the complete test against local repository SVG assets."
    for environment in matrix["environments"]:
        if environment.get("platform") == "iOS" and environment.get("report_file"):
            environment["status"] = "partial_pass"
            environment["tested_asset_mode"] = "remote_reference"
            environment["current_asset_mode"] = "local_repository"
            environment["current_implementation_verified"] = False
            pending = environment.setdefault("pending", [])
            if repeat_note not in pending:
                pending.append(repeat_note)
    write_json(MATRIX, matrix)


def update_testing_docs() -> None:
    text = TESTING.read_text(encoding="utf-8")
    marker = "## Transición a recursos locales"
    if marker not in text:
        text += (
            "\n\n## Transición a recursos locales\n\n"
            "Desde la revisión que integra `reference-standard-dual.assets.v1.json`, la página pública carga los 18 SVG desde el propio repositorio. Los informes móviles anteriores se conservan como evidencia histórica de la implementación remota, pero pasan a `partial_pass` hasta repetir el diagnóstico con los recursos locales desplegados.\n\n"
            "El modo «sitio de escritorio» en iPhone continúa siendo una prueba iOS basada en WebKit y no sustituye Chrome, Firefox o Edge ejecutados realmente en un ordenador.\n"
        )
    TESTING.write_text(text, encoding="utf-8")


def main() -> int:
    manifest = load_json(MANIFEST)
    if manifest.get("asset_count") != 18:
        raise ValueError("local asset manifest must contain exactly 18 SVGs")
    paths = local_web_paths(manifest)
    update_mapping(manifest)
    update_index(paths)
    update_self_test(paths)
    update_matrix()
    update_testing_docs()
    print("LOCAL ASSET INTEGRATION OK: mapping, renderer, self-test and browser matrix updated.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"LOCAL ASSET INTEGRATION FAILED: {exc}", file=sys.stderr)
        raise SystemExit(1)
