#!/usr/bin/env python3
"""Validate IberoLab's attested seed corpus without third-party dependencies."""

from __future__ import annotations

import json
import sys
import unicodedata
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CORPUS_PATH = ROOT / "data" / "corpus" / "attested-forms.v1.json"
SIGNS_PATH = ROOT / "data" / "signs" / "minimum-inventory.v1.json"

ALLOWED_READING = {"low", "medium", "high", "very_high"}
ALLOWED_SEMANTIC = {
    "uninterpreted",
    "disputed",
    "supported_hypothesis",
    "contextually_supported",
    "identified_name",
    "identified_referent",
}
FORBIDDEN_KEYS = {"translation", "literal_translation", "modern_equivalent"}


def fail(message: str) -> None:
    raise ValueError(message)


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def validate_https(url: str, context: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.netloc:
        fail(f"{context}: source URL must be an absolute HTTPS URL: {url!r}")


def validate() -> tuple[int, int]:
    corpus = load_json(CORPUS_PATH)
    inventory = load_json(SIGNS_PATH)

    forms = corpus.get("forms")
    if not isinstance(forms, list) or not forms:
        fail("Corpus must contain a non-empty forms array.")

    inventory_tokens = {
        item["transliteration"] for item in inventory.get("signs", [])
    }
    if not inventory_tokens:
        fail("Minimum sign inventory is empty.")

    ids: set[str] = set()
    normalized_forms: set[str] = set()
    used_tokens: set[str] = set()

    for index, item in enumerate(forms):
        context = f"forms[{index}]"
        forbidden = FORBIDDEN_KEYS.intersection(item)
        if forbidden:
            fail(f"{context}: forbidden unqualified translation keys: {sorted(forbidden)}")

        entry_id = item.get("id")
        form = item.get("form")
        tokens = item.get("grapheme_sequence")
        sources = item.get("sources")

        if not isinstance(entry_id, str) or not entry_id:
            fail(f"{context}: missing id.")
        if entry_id in ids:
            fail(f"{context}: duplicate id {entry_id!r}.")
        ids.add(entry_id)

        if not isinstance(form, str) or not form.strip():
            fail(f"{context}: missing form.")
        normalized = unicodedata.normalize("NFC", form)
        if form != normalized:
            fail(f"{context}: form must use Unicode NFC normalization.")
        if normalized in normalized_forms:
            fail(f"{context}: duplicate form {form!r}.")
        normalized_forms.add(normalized)

        if item.get("reading_confidence") not in ALLOWED_READING:
            fail(f"{context}: invalid reading_confidence.")
        if item.get("semantic_status") not in ALLOWED_SEMANTIC:
            fail(f"{context}: invalid semantic_status.")

        if not isinstance(tokens, list) or not tokens:
            fail(f"{context}: grapheme_sequence must be non-empty.")
        joined = "".join(tokens)
        if joined != form:
            fail(
                f"{context}: token sequence {tokens!r} joins to {joined!r}, "
                f"not to form {form!r}."
            )
        unknown = set(tokens) - inventory_tokens
        if unknown:
            fail(f"{context}: tokens absent from minimum inventory: {sorted(unknown)}")
        used_tokens.update(tokens)

        if not isinstance(sources, list) or not sources:
            fail(f"{context}: at least one source is required.")
        for source_index, source in enumerate(sources):
            source_context = f"{context}.sources[{source_index}]"
            if not source.get("citation"):
                fail(f"{source_context}: citation is required.")
            validate_https(source.get("url", ""), source_context)
            doi = source.get("doi")
            if doi and not source["url"].endswith(doi):
                fail(f"{source_context}: DOI URL does not match doi field.")

    unused = inventory_tokens - used_tokens
    if unused:
        fail(f"Minimum inventory contains tokens not used by the corpus: {sorted(unused)}")

    return len(forms), len(inventory_tokens)


if __name__ == "__main__":
    try:
        form_count, sign_count = validate()
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"VALIDATION FAILED: {exc}", file=sys.stderr)
        raise SystemExit(1)

    print(
        f"VALIDATION OK: {form_count} attested forms; "
        f"{sign_count} minimum transcription tokens."
    )
