#!/usr/bin/env python3
"""Apply the documented m1 → ń resolution across IberoLab.

This migration is intentionally explicit: m1 is the paleographic variant,
traditional m is retained as transcription history, and ń remains the project's
scholarly transcription. The SVG is a normalized reference, not a facsimile.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAPPING = ROOT / "data" / "signs" / "reference-standard-dual.v1.json"
MANIFEST = ROOT / "data" / "signs" / "reference-standard-dual.assets.v1.json"
AUDIT = ROOT / "data" / "audits" / "source-review.v1.json"
MATRIX = ROOT / "data" / "tests" / "browser-matrix.v1.json"
INDEX = ROOT / "docs" / "index.html"
SELF_TEST = ROOT / "docs" / "test.html"
PLAYWRIGHT = ROOT / "tests" / "browser" / "browser-smoke.spec.cjs"
ROADMAP = ROOT / "ROADMAP.md"
TESTING = ROOT / "docs" / "TESTING.md"
CHANGELOG = ROOT / "CHANGELOG.md"
NOTICE = ROOT / "NOTICE"
PROVENANCE = ROOT / "docs" / "ASSET_PROVENANCE.md"

LOCAL_REPO_PATH = "docs/assets/signs/northeastern-dual/variant-m1-nasal.svg"
LOCAL_WEB_PATH = "assets/signs/northeastern-dual/variant-m1-nasal.svg"
EVIDENCE = "https://doi.org/10.36707/palaeohispanica.v25i1.703"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise ValueError(f"{label}: expected one occurrence, found {count}")
    return text.replace(old, new, 1)


def update_mapping() -> None:
    mapping = read_json(MAPPING)
    signs = {item["token"]: item for item in mapping["signs"]}
    sign = signs.get("ń")
    if not sign:
        raise ValueError("mapping lacks token ń")
    sign.clear()
    sign.update(
        {
            "token": "ń",
            "reference_id": "variant-m1-nasal",
            "file_name": "NE Iberian m1.svg",
            "graphic_status": "local_attested_variant_svg_available",
            "local_path": LOCAL_REPO_PATH,
            "paleographic_variant": "m1",
            "traditional_transcription": "m",
            "project_transcription": "ń",
            "phonological_scope": "marked_nasal_not_labial",
            "graphic_scope": "normalized_m1_variant_reference_not_facsimile",
            "evidence": EVIDENCE,
            "note": "The 2025 publication identifies the sign as m1. Its traditional transcription m is retained as history; IberoLab follows the publication's ń transcription. The SVG is a normalized m1 reference, not a facsimile of the vessel."
        }
    )
    mapping["status"] = "local_reference_renderer_complete_for_seed_corpus"
    mapping["purpose"] = (
        "Provide visible, reproducible reference rendering for all tokens in the attested seed corpus, "
        "using normalized signary shapes and the documented m1 variant for ń."
    )
    mapping["scientific_scope"]["represents"] = (
        "Normalized reference sign shapes associated with conventional transliteration values; for ń, "
        "the documented paleographic variant m1 with explicit transcription history."
    )
    mapping["asset_manifest"] = MANIFEST.relative_to(ROOT).as_posix()
    mapping["resolved_tokens"] = [
        {
            "token": "ń",
            "paleographic_variant": "m1",
            "traditional_transcription": "m",
            "current_transcription": "ń",
            "evidence": EVIDENCE
        }
    ]
    write_json(MAPPING, mapping)


def update_audit() -> None:
    audit = read_json(AUDIT)
    entry = next(item for item in audit["entries"] if item["form_id"] == "ib-ne-tarsaban-001")
    entry["findings"] = [
        "The 2025 publication gives the complete sequence taŕśabańar and isolates the owner's name taŕśabań.",
        "The publication identifies the relevant sign as paleographic variant m1; it records traditional transcription m and adopts ń for Iberian as a marked, non-labial nasal.",
        "IberoLab uses a normalized CC0 m1 SVG and does not present it as a facsimile of either skyphos."
    ]
    entry["pending_tokens"] = []
    entry["resolved_graphic_tokens"] = [
        {
            "token": "ń",
            "variant": "m1",
            "traditional_transcription": "m",
            "current_transcription": "ń",
            "graphic_scope": "normalized_variant_reference_not_facsimile"
        }
    ]
    write_json(AUDIT, audit)


def update_matrix() -> None:
    matrix = read_json(MATRIX)
    matrix["schema_version"] = "1.3.0"
    matrix["updated_on"] = "2026-07-28"
    matrix["expected"]["mapped_svg_tokens"] = 19
    matrix["expected"]["explicit_pending_tokens"] = []
    matrix["expected"]["resolved_transcriptions"] = {
        "ń": {
            "paleographic_variant": "m1",
            "traditional_transcription": "m",
            "current_transcription": "ń"
        }
    }
    write_json(MATRIX, matrix)


def update_index() -> None:
    text = INDEX.read_text(encoding="utf-8")
    text = replace_once(
        text,
        '    "l": "assets/signs/northeastern-dual/dual-35-l.svg",\n    "n": "assets/signs/northeastern-dual/dual-37-n.svg"',
        '    "l": "assets/signs/northeastern-dual/dual-35-l.svg",\n    "n": "assets/signs/northeastern-dual/dual-37-n.svg",\n    "ń": "assets/signs/northeastern-dual/variant-m1-nasal.svg"',
        "index sign map"
    )
    text = replace_once(
        text,
        '      note:"La lectura ń está documentada, pero su signo gráfico no se asignará a n, m o ḿ sin una verificación paleográfica específica.",',
        '      note:"La publicación identifica el signo como la variante paleográfica m1. Su transcripción tradicional era m; IberoLab adopta ń siguiendo el estudio, que la caracteriza como nasal marcada no labial. El SVG es una referencia normalizada m1, no un facsímil.",',
        "index tarsaban note"
    )
    text = replace_once(
        text,
        'Recursos gráficos locales de referencia: 18 SVG de la serie “Sign Iber Noro Dual 01–38”, BotaFlo, Wikimedia Commons, CC0. Su procedencia, URL resuelta, tamaño y SHA-256 están versionados en el manifiesto del repositorio. Las grafías específicas de cada testimonio siguen en revisión.',
        'Recursos gráficos locales de referencia: 19 SVG CC0 con procedencia, URL resuelta, tamaño y SHA-256 versionados. Dieciocho pertenecen a la serie normalizada “Sign Iber Noro Dual 01–38” de BotaFlo; para ń se usa la variante normalizada m1 de Vriullop, identificada por la publicación de 2025. Ningún recurso se presenta como facsímil del testimonio.',
        "index footer"
    )
    INDEX.write_text(text, encoding="utf-8")


def update_self_test() -> None:
    text = SELF_TEST.read_text(encoding="utf-8")
    text = replace_once(
        text,
        '    "l": "assets/signs/northeastern-dual/dual-35-l.svg",\n    "n": "assets/signs/northeastern-dual/dual-37-n.svg"',
        '    "l": "assets/signs/northeastern-dual/dual-35-l.svg",\n    "n": "assets/signs/northeastern-dual/dual-37-n.svg",\n    "ń": "assets/signs/northeastern-dual/variant-m1-nasal.svg"',
        "self-test sign map"
    )
    text = replace_once(text, 'const EXPECTED_PENDING = new Set(["ń"]);', 'const EXPECTED_PENDING = new Set([]);', "self-test pending set")
    text = replace_once(
        text,
        'Esta página prueba, en el navegador actual, que las once formas están declaradas, que sus signos normalizados pueden cargarse y que el único token deliberadamente pendiente es <code>ń</code>.',
        'Esta página prueba, en el navegador actual, que las once formas están declaradas, que sus diecinueve signos de referencia pueden cargarse y que la transcripción <code>ń</code> utiliza la variante paleográfica m1 documentada.',
        "self-test lead"
    )
    text = replace_once(
        text,
        '<div class="metric"><strong id="signsMetric">0/18</strong><span>SVG cargados</span></div>',
        '<div class="metric"><strong id="signsMetric">0/19</strong><span>SVG cargados</span></div>',
        "self-test metric"
    )
    text = replace_once(
        text,
        '? "Prueba técnica superada: 11 formas evaluadas, 18 SVG locales cargados, ninguna salida vacía y ń permanece explícitamente pendiente."',
        '? "Prueba técnica superada: 11 formas evaluadas, 19 SVG locales cargados, ninguna salida vacía y ń resuelto mediante la variante m1 documentada."',
        "self-test success text"
    )
    text = replace_once(text, 'version: "1.1.0",', 'version: "1.2.0",', "self-test version")
    SELF_TEST.write_text(text, encoding="utf-8")


def update_playwright() -> None:
    text = PLAYWRIGHT.read_text(encoding="utf-8")
    text = replace_once(
        text,
        "{ id: 'ib-ne-tarsaban-001', form: 'taŕśabań', cards: 6, pending: 1 },",
        "{ id: 'ib-ne-tarsaban-001', form: 'taŕśabań', cards: 6, pending: 0 },",
        "playwright tarsaban pending"
    )
    text = replace_once(text, "expect(report.version).toBe('1.1.0');", "expect(report.version).toBe('1.2.0');", "playwright report version")
    text = replace_once(text, "svg_loaded: 18,\n    svg_total: 18,", "svg_loaded: 19,\n    svg_total: 19,", "playwright SVG totals")
    text = replace_once(text, "pending_tokens: ['ń'],", "pending_tokens: [],", "playwright pending tokens")
    PLAYWRIGHT.write_text(text, encoding="utf-8")


def update_docs() -> None:
    roadmap = ROADMAP.read_text(encoding="utf-8")
    roadmap = replace_once(
        roadmap,
        "- [x] Crear un mapeo gráfico provisional con formas normalizadas de referencia para 18 de los 19 tokens del corpus.\n- [x] Mantener `ń` como token explícitamente pendiente, sin sustituirlo por `n`, `m` o `ḿ`.",
        "- [x] Crear un mapeo gráfico provisional con formas normalizadas de referencia para los 19 tokens del corpus.\n- [x] Resolver `ń` como transcripción de la variante paleográfica m1, conservando `m` como transcripción histórica y sin confundirla con `n` o `ḿ`.",
        "roadmap token coverage"
    )
    ROADMAP.write_text(roadmap, encoding="utf-8")

    testing = TESTING.read_text(encoding="utf-8")
    testing = testing.replace("dieciocho SVG normalizados", "diecinueve SVG de referencia")
    testing = testing.replace("que `ń` sigue siendo el único token deliberadamente pendiente;", "que `ń` se renderiza mediante la variante paleográfica m1 documentada y no queda pendiente;")
    testing = testing.replace("`version: 1.1.0`", "`version: 1.2.0`")
    TESTING.write_text(testing, encoding="utf-8")

    changelog = CHANGELOG.read_text(encoding="utf-8")
    marker = "- Regresión automática con Playwright sobre Chromium, Firefox y WebKit para las once formas y las dos páginas de diagnóstico."
    addition = marker + "\n- Variante paleográfica m1 normalizada, trazable y licenciada para resolver la transcripción ń del corpus."
    changelog = replace_once(changelog, marker, addition, "changelog added item")
    changelog = changelog.replace("- `ń` permanece visible como único token deliberadamente pendiente en `taŕśabań`.", "- `ń` queda resuelto mediante la variante paleográfica m1 documentada; se conserva `m` como transcripción histórica y el recurso no se presenta como facsímil.")
    changelog = changelog.replace("- El token `ń` de `taŕśabań` permanece sin signo gráfico asignado hasta verificar la convención de transcripción y la forma exacta en la publicación correspondiente.\n", "")
    CHANGELOG.write_text(changelog, encoding="utf-8")

    notice = NOTICE.read_text(encoding="utf-8")
    if "NE Iberian m1.svg" not in notice:
        notice += (
            "\n\nThe normalized m1 variant used for the transcription ń is derived from "
            "‘NE Iberian m1.svg’ by Vriullop, Wikimedia Commons, dedicated under CC0 1.0. "
            "Its paleographic assignment and transcription history are documented from "
            "Ferrer i Jané et al. (2025), DOI 10.36707/palaeohispanica.v25i1.703.\n"
        )
    NOTICE.write_text(notice, encoding="utf-8")

    provenance = PROVENANCE.read_text(encoding="utf-8")
    if "## Variante nasal m1" not in provenance:
        provenance += (
            "\n\n## Variante nasal m1\n\n"
            "El token `ń` utiliza `docs/assets/signs/northeastern-dual/variant-m1-nasal.svg`, "
            "procedente de `NE Iberian m1.svg`, obra de Vriullop publicada en Wikimedia Commons bajo CC0 1.0. "
            "La publicación de 2025 sobre `taŕśabańar` identifica el signo como variante `m1`: conserva `m` como "
            "transcripción tradicional y adopta `ń` para el comportamiento ibérico de nasal marcada no labial. "
            "IberoLab registra estas tres capas por separado y usa el SVG únicamente como referencia normalizada, no como facsímil.\n\n"
            f"Evidencia paleográfica: {EVIDENCE}.\n"
        )
    PROVENANCE.write_text(provenance, encoding="utf-8")


def main() -> int:
    manifest = read_json(MANIFEST)
    assets = {item.get("token"): item for item in manifest.get("assets", [])}
    if manifest.get("asset_count") != 19 or "ń" not in assets:
        raise ValueError("the generated 19-asset manifest with ń is required before migration")
    if assets["ń"].get("paleographic_variant") != "m1":
        raise ValueError("the ń asset is not documented as m1")
    update_mapping()
    update_audit()
    update_matrix()
    update_index()
    update_self_test()
    update_playwright()
    update_docs()
    print("NASAL RESOLUTION APPLIED: m1, traditional m and current ń are now explicitly separated.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, json.JSONDecodeError, KeyError, StopIteration, TypeError, ValueError) as exc:
        print(f"NASAL RESOLUTION FAILED: {exc}", file=sys.stderr)
        raise SystemExit(1)
