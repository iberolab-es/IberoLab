#!/usr/bin/env python3
"""Validate IberoLab's versioned browser matrix and public self-test page."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "data" / "tests" / "browser-matrix.v1.json"
TEST_PAGE = ROOT / "docs" / "test.html"
REQUIRED_BROWSERS = {"Safari", "Chrome", "Firefox", "Edge"}
REQUIRED_DESKTOP_BROWSERS = {"Chrome", "Firefox", "Edge"}
ALLOWED_STATUS = {"pending", "partial_pass", "pass", "fail"}
EXPECTED_FORMS = {
    "ildiŕda", "erder", "undikesken", "ars", "ekiar", "egiar",
    "likine", "taŕśabań", "baisetaś", "seltar", "ebanen",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_pass_report(environment: dict, context: str, expected: dict) -> None:
    report_name = environment.get("report_file")
    if not isinstance(report_name, str) or not report_name:
        raise ValueError(f"{context}: pass status requires report_file")

    report_path = ROOT / report_name
    if not report_path.is_file():
        raise ValueError(f"{context}: report file does not exist: {report_name}")

    report = load_json(report_path)
    metrics = report.get("metrics", {})
    if report.get("result") != "pass":
        raise ValueError(f"{context}: linked report result is not pass")
    if report.get("application") != "IberoLab browser self-test":
        raise ValueError(f"{context}: unexpected report application")
    if metrics.get("forms_evaluated") != expected["forms_total"]:
        raise ValueError(f"{context}: report does not evaluate all forms")
    if metrics.get("forms_total") != expected["forms_total"]:
        raise ValueError(f"{context}: report forms_total mismatch")
    if metrics.get("svg_loaded") != expected["mapped_svg_tokens"]:
        raise ValueError(f"{context}: report SVG count mismatch")
    if metrics.get("svg_total") != expected["mapped_svg_tokens"]:
        raise ValueError(f"{context}: report svg_total mismatch")
    if metrics.get("empty_outputs") != expected["empty_outputs"]:
        raise ValueError(f"{context}: report contains empty outputs")
    if metrics.get("failed_svg_tokens") != []:
        raise ValueError(f"{context}: report contains failed SVG tokens")
    if metrics.get("pending_tokens") != expected["explicit_pending_tokens"]:
        raise ValueError(f"{context}: report pending token mismatch")
    if metrics.get("unexpected_pending") != []:
        raise ValueError(f"{context}: report contains unexpected pending tokens")
    if metrics.get("missing_expected_pending") != []:
        raise ValueError(f"{context}: report misses expected pending tokens")

    engine_token = environment.get("engine_token_from_user_agent")
    user_agent = report.get("user_agent", "")
    if engine_token and engine_token not in user_agent:
        raise ValueError(f"{context}: report user_agent lacks declared engine token")

    forms = report.get("forms", [])
    names = {item.get("form") for item in forms}
    if names != EXPECTED_FORMS:
        raise ValueError(f"{context}: report form set mismatch")

    for item in forms:
        if item.get("failedTokens"):
            raise ValueError(f"{context}: {item.get('form')!r} contains failed tokens")
        visible_count = item.get("visibleCount")
        tokens = item.get("tokens")
        if not isinstance(tokens, list) or visible_count != len(tokens):
            raise ValueError(f"{context}: {item.get('form')!r} visible token count mismatch")
        expected_pending = ["ń"] if item.get("form") == "taŕśabań" else []
        if item.get("pending") != expected_pending:
            raise ValueError(f"{context}: {item.get('form')!r} pending state mismatch")


def validate() -> tuple[int, int, int, int]:
    matrix = load_json(MATRIX)
    expected = matrix.get("expected", {})
    environments = matrix.get("environments", [])

    if expected.get("forms_total") != 11:
        raise ValueError("browser matrix must expect eleven forms")
    if expected.get("mapped_svg_tokens") != 18:
        raise ValueError("browser matrix must expect eighteen mapped SVG tokens")
    if expected.get("empty_outputs") != 0:
        raise ValueError("browser matrix must require zero empty outputs")
    if expected.get("explicit_pending_tokens") != ["ń"]:
        raise ValueError("browser matrix must preserve only ń as explicit pending token")

    if not isinstance(environments, list) or not environments:
        raise ValueError("browser environments must be non-empty")

    browsers = set()
    desktop_browsers = set()
    ids = set()
    passed = 0
    desktop_passed = 0
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
            validate_pass_report(environment, context, expected)
            passed += 1
            if platform == "desktop" and device_class == "desktop":
                desktop_passed += 1

        if environment.get("presentation_mode") == "request_desktop_site" and platform == "desktop":
            raise ValueError(f"{context}: request_desktop_site must not be classified as desktop platform")

    missing_browsers = REQUIRED_BROWSERS - browsers
    if missing_browsers:
        raise ValueError(f"browser matrix lacks: {sorted(missing_browsers)}")

    missing_desktop_targets = REQUIRED_DESKTOP_BROWSERS - desktop_browsers
    if missing_desktop_targets:
        raise ValueError(
            f"browser matrix lacks explicit desktop targets: {sorted(missing_desktop_targets)}"
        )

    html = TEST_PAGE.read_text(encoding="utf-8")
    markers = [
        "Comprobar las 11 formas",
        "EXPECTED_PENDING",
        "empty_outputs",
        "failed_svg_tokens",
        "navigator.userAgent",
        "navigator.clipboard",
        "dataset.selfTest",
        "No valida la exactitud paleográfica",
    ]
    missing_markers = [marker for marker in markers if marker not in html]
    if missing_markers:
        raise ValueError(f"self-test page lacks safeguards: {missing_markers}")

    for form in EXPECTED_FORMS:
        if form not in html:
            raise ValueError(f"self-test page lacks form {form!r}")

    return len(environments), len(REQUIRED_BROWSERS), passed, desktop_passed


if __name__ == "__main__":
    try:
        environment_count, browser_count, passed_count, desktop_passed_count = validate()
    except (OSError, json.JSONDecodeError, KeyError, ValueError) as exc:
        print(f"BROWSER MATRIX VALIDATION FAILED: {exc}", file=sys.stderr)
        raise SystemExit(1)

    print(
        "BROWSER MATRIX VALIDATION OK: "
        f"{environment_count} environments; {browser_count} required browsers; "
        f"{passed_count} complete pass report(s), of which {desktop_passed_count} "
        "are true desktop environments; public self-test covers eleven forms and "
        "preserves ń as pending."
    )
