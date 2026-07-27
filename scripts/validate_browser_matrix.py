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
ALLOWED_STATUS = {"pending", "partial_pass", "pass", "fail"}


def validate() -> tuple[int, int]:
    matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
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
    ids = set()
    for index, environment in enumerate(environments):
        context = f"environments[{index}]"
        environment_id = environment.get("id")
        if not environment_id or environment_id in ids:
            raise ValueError(f"{context}: missing or duplicate id")
        ids.add(environment_id)

        browser = environment.get("browser")
        browsers.add(browser)
        if environment.get("status") not in ALLOWED_STATUS:
            raise ValueError(f"{context}: invalid status")

    missing_browsers = REQUIRED_BROWSERS - browsers
    if missing_browsers:
        raise ValueError(f"browser matrix lacks: {sorted(missing_browsers)}")

    html = TEST_PAGE.read_text(encoding="utf-8")
    markers = [
        "Comprobar las 11 formas",
        "EXPECTED_PENDING",
        "empty_outputs",
        "failed_svg_tokens",
        "navigator.userAgent",
        "navigator.clipboard",
        "data-self-test",
        "No valida la exactitud paleográfica",
    ]
    missing_markers = [marker for marker in markers if marker not in html]
    if missing_markers:
        raise ValueError(f"self-test page lacks safeguards: {missing_markers}")

    for form in [
        "ildiŕda", "erder", "undikesken", "ars", "ekiar", "egiar",
        "likine", "taŕśabań", "baisetaś", "seltar", "ebanen",
    ]:
        if form not in html:
            raise ValueError(f"self-test page lacks form {form!r}")

    return len(environments), len(REQUIRED_BROWSERS)


if __name__ == "__main__":
    try:
        environment_count, browser_count = validate()
    except (OSError, json.JSONDecodeError, KeyError, ValueError) as exc:
        print(f"BROWSER MATRIX VALIDATION FAILED: {exc}", file=sys.stderr)
        raise SystemExit(1)

    print(
        "BROWSER MATRIX VALIDATION OK: "
        f"{environment_count} environments; {browser_count} required browsers; "
        "public self-test covers eleven forms and preserves ń as pending."
    )
