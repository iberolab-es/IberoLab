#!/usr/bin/env python3
"""Validate one-to-one scholarly source review coverage for the seed corpus."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "data" / "corpus" / "attested-forms.v1.json"
AUDIT = ROOT / "data" / "audits" / "source-review.v1.json"
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ALLOWED_READING = {"reading_verified"}
ALLOWED_CONTEXT = {"context_verified"}
ALLOWED_RENDERING = {"normalized_reference_only"}


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def fail(message: str) -> None:
    raise ValueError(message)


def validate_https(url: str, context: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.netloc:
        fail(f"{context}: expected absolute HTTPS URL, got {url!r}")


def validate() -> tuple[int, int]:
    corpus = load(CORPUS)
    audit = load(AUDIT)

    reviewed_on = audit.get("reviewed_on", "")
    if not DATE_RE.fullmatch(reviewed_on):
        fail("reviewed_on must use YYYY-MM-DD format")

    forms = corpus.get("forms", [])
    entries = audit.get("entries", [])
    if not forms or not entries:
        fail("corpus and audit must both be non-empty")

    corpus_by_id = {item["id"]: item for item in forms}
    if len(corpus_by_id) != len(forms):
        fail("corpus contains duplicate form ids")

    audit_by_id: dict[str, dict] = {}
    for index, entry in enumerate(entries):
        context = f"entries[{index}]"
        form_id = entry.get("form_id")
        if not isinstance(form_id, str) or not form_id:
            fail(f"{context}: form_id is required")
        if form_id in audit_by_id:
            fail(f"{context}: duplicate audit entry {form_id!r}")
        audit_by_id[form_id] = entry

        if entry.get("reading_status") not in ALLOWED_READING:
            fail(f"{context}: invalid reading_status")
        if entry.get("context_status") not in ALLOWED_CONTEXT:
            fail(f"{context}: invalid context_status")
        if entry.get("rendering_status") not in ALLOWED_RENDERING:
            fail(f"{context}: rendering must remain explicitly normalized")

        findings = entry.get("findings")
        if not isinstance(findings, list) or not findings or not all(
            isinstance(item, str) and item.strip() for item in findings
        ):
            fail(f"{context}: at least one non-empty finding is required")

        urls = entry.get("source_urls")
        if not isinstance(urls, list) or not urls:
            fail(f"{context}: source_urls must be non-empty")
        for url_index, url in enumerate(urls):
            validate_https(url, f"{context}.source_urls[{url_index}]")

        pending = entry.get("pending_tokens", [])
        if not isinstance(pending, list):
            fail(f"{context}: pending_tokens must be an array")

    missing = sorted(corpus_by_id.keys() - audit_by_id.keys())
    extra = sorted(audit_by_id.keys() - corpus_by_id.keys())
    if missing or extra:
        fail(f"audit coverage mismatch; missing={missing}, extra={extra}")

    unresolved: set[str] = set()
    for form_id, entry in audit_by_id.items():
        tokens = set(corpus_by_id[form_id]["grapheme_sequence"])
        pending = set(entry.get("pending_tokens", []))
        unknown = pending - tokens
        if unknown:
            fail(f"{form_id}: pending tokens not present in form: {sorted(unknown)}")
        unresolved.update(pending)

    if unresolved != {"ń"}:
        fail(f"expected only the explicitly unresolved token ń, got {sorted(unresolved)}")

    return len(forms), len(entries)


if __name__ == "__main__":
    try:
        form_count, audit_count = validate()
    except (OSError, json.JSONDecodeError, KeyError, ValueError) as exc:
        print(f"SOURCE AUDIT VALIDATION FAILED: {exc}", file=sys.stderr)
        raise SystemExit(1)

    print(
        "SOURCE AUDIT VALIDATION OK: "
        f"{form_count} corpus forms; {audit_count} reviewed entries; "
        "one explicit unresolved graphic token (ń)."
    )
