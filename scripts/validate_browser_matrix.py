#!/usr/bin/env python3
"""Validate IberoLab's browser matrix and public diagnostic pages."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "data" / "tests" / "browser-matrix.v1.json"
TEST_PAGE = ROOT / "docs" / "test.html"
DEEP_LINK_PAGE = ROOT / "docs" / "deep-link-test.html"
REQUIRED_BROWSERS = {"Safari", "Chrome", "Firefox", "Edge"}
REQUIRED_DESKTOP_BROWSERS = {"Chrome", "Firefox", "Edge"}
ALLOWED_STATUS = {"pending", "partial_pass", "pass", "fail"}
CURRENT_ASSET_MODE = "local_repository"
HISTORICAL_REMOTE_EXPECTED = {
    "forms_total": 11,
    "mapped_svg_tokens": 18,
    "empty_outputs": 0,
    "explicit_pending_tokens": ["ń"],
}
EXPECTED_LINKS = {
    "ib-ne-ildirda-001": "ildiŕda",
    "ib-ne-erder-001": "erder",
    "ib-ne-undikesken-001": "undikesken",
    "ib-ne-ars-001": "ars",
    "ib-ne-ekiar-001": "ekiar",
    "ib-ne-egiar-001": "egiar",
    "ib-ne-likine-001": "likine",
    "ib-ne-tarsaban-001": "taŕśabań",
    "ib-ne-baisetas-001": "baisetaś",
    "ib-ne-seltar-001": "seltar",
    "ib-ne-ebanen-001": "ebanen",
}
EXPECTED_FORMS = set(EXPECTED_LINKS.values())


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_report_core(environment: dict, context: str, expected: dict, pending_by_form: dict[str, list[str]]) -> dict:
    report_name = environment.get("report_file")
    if not isinstance(report_name, str) or not report_name:
        raise ValueError(f"{context}: tested status requires report_file")
    report_path = ROOT / report_name
    if not report_path.is_file():
        raise ValueError(f"{context}: report file does not exist: {report_name}")

    report = load_json(report_path)
    metrics = report.get("metrics", {})
    if report.get("result") != "pass" or report.get("application") != "IberoLab browser self-test":
        raise ValueError(f"{context}: linked report is not a passing IberoLab browser self-test")
    for key in ("forms_evaluated", "forms_total"):
        if metrics.get(key) != expected["forms_total"]:
            raise ValueError(f"{context}: report {key} mismatch")
    for key in ("svg_loaded", "svg_total"):
        if metrics.get(key) != expected["mapped_svg_tokens"]:
            raise ValueError(f"{context}: report {key} mismatch")
    if metrics.get("empty_outputs") != expected["empty_outputs"]:
        raise ValueError(f"{context}: report contains empty outputs")
    if metrics.get("failed_svg_tokens") != []:
        raise ValueError(f"{context}: report contains failed SVG tokens")
    if metrics.get("pending_tokens") != expected["explicit_pending_tokens"]:
        raise ValueError(f"{context}: report pending token mismatch")
    if metrics.get("unexpected_pending") != [] or metrics.get("missing_expected_pending") != []:
        raise ValueError(f"{context}: report pending-token bookkeeping is inconsistent")

    engine_token = environment.get("engine_token_from_user_agent")
    user_agent = report.get("user_agent", "")
    if engine_token and engine_token not in user_agent:
        raise ValueError(f"{context}: report user_agent lacks declared engine token")

    forms = report.get("forms", [])
    if {item.get("form") for item in forms} != EXPECTED_FORMS:
        raise ValueError(f"{context}: report form set mismatch")
    for item in forms:
        if item.get("failedTokens"):
            raise ValueError(f"{context}: {item.get('form')!r} contains failed tokens")
        tokens = item.get("tokens")
        if not isinstance(tokens, list) or item.get("visibleCount") != len(tokens):
            raise ValueError(f"{context}: {item.get('form')!r} visible token count mismatch")
        if item.get("pending") != pending_by_form.get(item.get("form"), []):
            raise ValueError(f"{context}: {item.get('form')!r} pending state mismatch")
    return report


def validate_svg_self_test() -> None:
    html = TEST_PAGE.read_text(encoding="utf-8")
    markers = [
        "Comprobar las 11 formas", "EXPECTED_PENDING", "empty_outputs", "failed_svg_tokens",
        "navigator.userAgent", "navigator.clipboard", "dataset.selfTest",
        "No valida la exactitud paleográfica", 'asset_mode: "local_repository"',
        'version: "1.2.0"', "variant-m1-nasal.svg", "variante paleográfica m1",
    ]
    missing = [marker for marker in markers if marker not in html]
    if missing:
        raise ValueError(f"self-test page lacks safeguards: {missing}")
    if "Special:Redirect/file" in html or "const COMMONS" in html:
        raise ValueError("self-test still contains a remote SVG dependency")
    if 'const EXPECTED_PENDING = new Set([]);' not in html:
        raise ValueError("self-test must expect no pending graphic tokens")
    for form in EXPECTED_FORMS:
        if form not in html:
            raise ValueError(f"self-test page lacks form {form!r}")


def validate_deep_link_self_test() -> None:
    html = DEEP_LINK_PAGE.read_text(encoding="utf-8")
    markers = [
        "Comprobar los 11 enlaces", "IberoLab deep-link self-test", 'asset_mode: "local_repository"',
        "dataset.deepLinkTest", "rendererReady", "formSelect", "readingText", "glyphOutput",
        "links_evaluated", "links_failed", "deep-link-state-mismatch", "iframe",
        "contentDocument", "contentWindow", "No valida la exactitud paleográfica",
    ]
    missing = [marker for marker in markers if marker not in html]
    if missing:
        raise ValueError(f"deep-link self-test lacks safeguards: {missing}")
    for identifier, form in EXPECTED_LINKS.items():
        if identifier not in html or form not in html:
            raise ValueError(f"deep-link self-test lacks {identifier!r} or {form!r}")
    if html.count("{id:") != len(EXPECTED_LINKS):
        raise ValueError("deep-link self-test target count does not match eleven")


def validate() -> tuple[int, int, int, int, int]:
    matrix = load_json(MATRIX)
    expected = matrix.get("expected", {})
    environments = matrix.get("environments", [])
    if matrix.get("schema_version") != "1.3.0":
        raise ValueError("browser matrix must use schema 1.3.0")
    if expected.get("forms_total") != 11 or expected.get("mapped_svg_tokens") != 19:
        raise ValueError("browser matrix must expect eleven forms and nineteen SVG tokens")
    if expected.get("empty_outputs") != 0 or expected.get("explicit_pending_tokens") != []:
        raise ValueError("browser matrix must require zero empty outputs and no pending graphic tokens")
    if expected.get("asset_mode") != CURRENT_ASSET_MODE:
        raise ValueError("browser matrix must target local_repository asset mode")
    resolved = expected.get("resolved_transcriptions", {}).get("ń", {})
    if resolved != {"paleographic_variant": "m1", "traditional_transcription": "m", "current_transcription": "ń"}:
        raise ValueError("browser matrix must document the m1/m/ń resolution")
    if not isinstance(environments, list) or not environments:
        raise ValueError("browser environments must be non-empty")

    browsers: set[str] = set()
    desktop_browsers: set[str] = set()
    ids: set[str] = set()
    passed = desktop_passed = historical_partial = 0
    for index, environment in enumerate(environments):
        context = f"environments[{index}]"
        environment_id = environment.get("id")
        if not environment_id or environment_id in ids:
            raise ValueError(f"{context}: missing or duplicate id")
        ids.add(environment_id)
        browser = environment.get("browser")
        platform = environment.get("platform")
        device_class = environment.get("device_class")
        browsers.add(browser)
        if platform == "desktop" and device_class == "desktop":
            desktop_browsers.add(browser)
        status = environment.get("status")
        if status not in ALLOWED_STATUS:
            raise ValueError(f"{context}: invalid status")

        if status == "pass":
            report = validate_report_core(environment, context, expected, {})
            if report.get("asset_mode") != CURRENT_ASSET_MODE or report.get("version") != "1.2.0":
                raise ValueError(f"{context}: current pass report is not the resolved local implementation")
            passed += 1
            if platform == "desktop" and device_class == "desktop":
                desktop_passed += 1

        if status == "partial_pass" and environment.get("report_file"):
            tested_mode = environment.get("tested_asset_mode")
            if tested_mode == "remote_reference":
                report = validate_report_core(
                    environment,
                    context,
                    HISTORICAL_REMOTE_EXPECTED,
                    {"taŕśabań": ["ń"]},
                )
                if report.get("asset_mode") not in (None, "remote_reference"):
                    raise ValueError(f"{context}: historical report has inconsistent asset mode")
                if environment.get("current_asset_mode") != CURRENT_ASSET_MODE:
                    raise ValueError(f"{context}: historical entry lacks current asset mode")
                if environment.get("current_implementation_verified") is not False:
                    raise ValueError(f"{context}: historical entry must remain unverified for current assets")
                historical_partial += 1

        if environment.get("presentation_mode") == "request_desktop_site" and platform == "desktop":
            raise ValueError(f"{context}: request_desktop_site must not be desktop platform")

    if REQUIRED_BROWSERS - browsers:
        raise ValueError(f"browser matrix lacks: {sorted(REQUIRED_BROWSERS - browsers)}")
    if REQUIRED_DESKTOP_BROWSERS - desktop_browsers:
        raise ValueError(f"browser matrix lacks desktop targets: {sorted(REQUIRED_DESKTOP_BROWSERS - desktop_browsers)}")

    validate_svg_self_test()
    validate_deep_link_self_test()
    return len(environments), len(REQUIRED_BROWSERS), passed, desktop_passed, historical_partial


if __name__ == "__main__":
    try:
        environment_count, browser_count, passed_count, desktop_passed_count, historical_count = validate()
    except (OSError, json.JSONDecodeError, KeyError, ValueError) as exc:
        print(f"BROWSER MATRIX VALIDATION FAILED: {exc}", file=sys.stderr)
        raise SystemExit(1)
    print(
        "BROWSER MATRIX VALIDATION OK: "
        f"{environment_count} environments; {browser_count} required browsers; "
        f"{passed_count} current 19-asset pass report(s), of which {desktop_passed_count} are desktop; "
        f"{historical_count} historical 18-asset partial pass report(s); both public diagnostics validated."
    )
