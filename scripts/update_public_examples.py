#!/usr/bin/env python3
"""Replace personal MVP examples with neutral, project-oriented examples."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace(path: str, old: str, new: str, expected: int = 1) -> None:
    target = ROOT / path
    text = target.read_text(encoding="utf-8")
    count = text.count(old)
    if count != expected:
        raise RuntimeError(f"{path}: expected {expected} occurrence(s) of {old!r}, found {count}")
    target.write_text(text.replace(old, new), encoding="utf-8")


# Public page: neutral examples and a clearer invitation.
replace("docs/convertir.html", 'placeholder="Ej.: Lara, familia, te quiero"', 'placeholder="Ej.: amor, familia, te quiero"')
replace(
    "docs/convertir.html",
    '      <button class="example" type="button" data-example="Lara">Lara</button>\n'
    '      <button class="example" type="button" data-example="Cris">Cris</button>',
    '      <button class="example" type="button" data-example="amistad">amistad</button>\n'
    '      <button class="example" type="button" data-example="hogar">hogar</button>',
)
replace(
    "docs/convertir.html",
    '    </div>\n\n    <section id="resultSection"',
    '    </div>\n    <p class="counter">Ejemplos orientativos. Puedes escribir cualquier nombre, palabra o frase breve.</p>\n\n    <section id="resultSection"',
)

# Browser regression: replace the personal cluster case with two neutral product cases.
replace(
    "tests/browser/browser-smoke.spec.cjs",
    "  { input: 'Cris', reading: 'ki · r · i · s', cards: 4, status: 'approximate' }",
    "  { input: 'hogar', reading: 'o · ga · r', cards: 3, status: 'direct' },\n"
    "  { input: 'amistad', reading: 'a · m · i · s · ta · da', cards: 6, status: 'approximate' }",
)
replace(
    "tests/browser/browser-smoke.spec.cjs",
    "  test('Cris conserva el grupo consonántico mediante una vocal de apoyo declarada', async ({ page }) => {\n"
    "    await page.goto('/convertir.html', { waitUntil: 'load' });\n"
    "    await page.locator('#sourceInput').fill('Cris');\n"
    "    await page.getByRole('button', { name: 'Adaptar a signos ibéricos' }).click();\n"
    "    await expect(page.locator('#noticeList')).toContainText('vocal de apoyo');\n"
    "    await expect(page.locator('#technicalReading')).toHaveText('ki · r · i · s');\n"
    "  });",
    "  test('amistad declara la vocal de apoyo de la oclusiva final', async ({ page }) => {\n"
    "    await page.goto('/convertir.html', { waitUntil: 'load' });\n"
    "    await page.locator('#sourceInput').fill('amistad');\n"
    "    await page.getByRole('button', { name: 'Adaptar a signos ibéricos' }).click();\n"
    "    await expect(page.locator('#noticeList')).toContainText('vocal de apoyo');\n"
    "    await expect(page.locator('#technicalReading')).toHaveText('a · m · i · s · ta · da');\n"
    "  });",
)

# Static validator: require the neutral public examples.
validator = ROOT / "scripts/validate_mvp_converter.py"
text = validator.read_text(encoding="utf-8")
anchor = '        \'data-example="te quiero"\',\n'
if anchor not in text:
    raise RuntimeError("validate_mvp_converter.py: example marker anchor not found")
text = text.replace(anchor, anchor + '        \'data-example="amistad"\',\n        \'data-example="hogar"\',\n', 1)
validator.write_text(text, encoding="utf-8")

# Changelog: current product wording should use neutral examples.
changelog = ROOT / "CHANGELOG.md"
changelog_text = changelog.read_text(encoding="utf-8")
changelog_text = changelog_text.replace("`Cris`", "`amistad`").replace("`Lara`", "`hogar`")
changelog.write_text(changelog_text, encoding="utf-8")

# Verify there are no personal examples left in current product assets.
checked = [
    "docs/convertir.html",
    "tests/browser/browser-smoke.spec.cjs",
    "scripts/validate_mvp_converter.py",
    "CHANGELOG.md",
]
for relative in checked:
    current = (ROOT / relative).read_text(encoding="utf-8")
    for forbidden in ("Lara", "Cris"):
        if forbidden in current:
            raise RuntimeError(f"{relative}: personal example remains")

print("Updated public MVP examples to amor, familia, te quiero, amistad and hogar.")
