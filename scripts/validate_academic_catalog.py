#!/usr/bin/env python3
"""Check source alignment, honest scope and reproducible static academic pages."""
import json
from pathlib import Path
import sys
from render_academic_catalog import render

ROOT = Path(__file__).resolve().parents[1]


def validate_data(seed, catalog):
    if catalog.get("schema_version") != "1.0.0" or catalog.get("entry_unit") != "attested_form":
        raise ValueError("catalogue must describe the current attested-form seed")
    if catalog.get("base_corpus") != "data/corpus/attested-forms.v1.json":
        raise ValueError("catalogue provenance must point to the documented seed")
    for key in ("complete_inscription_editions", "linguistic_segmentations"):
        if type(catalog.get(key)) is not int or catalog[key] != 0:
            raise ValueError(f"{key}: this release has no reviewed complete editions or linguistic segmentations")
    entries = catalog.get("entries", [])
    ids = [item["form_id"] for item in entries]
    if len(ids) != len(set(ids)) or set(ids) != {f["id"] for f in seed["forms"]}:
        raise ValueError("catalogue entries must cover the seed exactly once")
    expected_statuses = {"not_catalogued", "documented", "hypothesis", "disputed", "unsegmented"}
    if set(catalog.get("segmentation_policy", {})) != expected_statuses:
        raise ValueError("segmentation levels must be distinguished explicitly")
    for item in entries:
        for field in ("context", "interpretation", "transcription_note"):
            if not isinstance(item.get(field), str) or not item[field].strip():
                raise ValueError(f"{item['form_id']}: missing {field}")
        provenance = item.get("provenance", {})
        if provenance.get("object_identifier") is not None:
            raise ValueError("no object identifiers are documented in the initial seed; do not invent them")
        if any(not provenance.get(key) for key in ("context", "support", "note")):
            raise ValueError("context, support and provenance limits must be visible")
        segmentation = item.get("linguistic_segmentation", {})
        if segmentation != {"status": "not_catalogued", "segments": [], "source_locator": None, "specialist_review": None}:
            raise ValueError("new linguistic segmentation requires a documented source and specialist review workflow")
    return len(entries)


def validate():
    seed = json.loads((ROOT / "data/corpus/attested-forms.v1.json").read_text())
    catalog = json.loads((ROOT / "data/corpus/academic-catalog.v1.json").read_text())
    count = validate_data(seed, catalog)
    actual = (ROOT / "docs/corpus.html").read_text(encoding="utf-8")
    if actual != render():
        raise ValueError("docs/corpus.html is stale: run scripts/render_academic_catalog.py")
    if actual.count('class="catalogue-card"') != count:
        raise ValueError("static catalogue must contain every entry without JavaScript")
    for form in seed["forms"]:
        if f'id="{form["id"]}"' not in actual:
            raise ValueError(f"missing direct link for {form['id']}")
        for source in form["sources"]:
            if source["url"] not in actual:
                raise ValueError("catalogue must expose every inherited bibliography link")
    for name in ("index.html", "academia.html", "historia.html", "metodologia.html", "convertir.html"):
        if 'href="corpus.html"' not in (ROOT / "docs" / name).read_text():
            raise ValueError(f"{name}: missing direct academic route")
    print(f"ACADEMIC CATALOGUE OK: {count} static source-traceable forms; no invented object identifiers, complete editions or linguistic segmentations; HTML synchronized.")


if __name__ == "__main__":
    try:
        validate()
    except (ValueError, KeyError, OSError) as error:
        print(f"ACADEMIC CATALOGUE FAILED: {error}", file=sys.stderr)
        sys.exit(1)
