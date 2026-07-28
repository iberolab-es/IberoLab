#!/usr/bin/env python3
"""Reapply public presence after restoring conflicting files from current main."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace(path: str, old: str, new: str, expected: int = 1) -> None:
    target = ROOT / path
    text = target.read_text(encoding="utf-8")
    count = text.count(old)
    if count != expected:
        raise RuntimeError(f"{path}: expected {expected} occurrence(s), found {count}: {old!r}")
    target.write_text(text.replace(old, new), encoding="utf-8")


META_CONVERTER = '''  <meta name="description" content="Adaptación fonética experimental de nombres, palabras y frases breves mediante signos ibéricos normalizados.">
  <link rel="canonical" href="https://iberolab-es.github.io/IberoLab/convertir.html">
  <link rel="icon" href="assets/brand/iberolab-mark.svg" type="image/svg+xml">
  <link rel="manifest" href="site.webmanifest">
  <meta name="theme-color" content="#10253a">
  <meta property="og:type" content="website">
  <meta property="og:title" content="IberoLab · Adaptación fonética experimental">
  <meta property="og:description" content="Escribe un nombre, una palabra o una frase breve y visualízala mediante signos ibéricos normalizados.">
  <meta property="og:url" content="https://iberolab-es.github.io/IberoLab/convertir.html">
  <meta property="og:image" content="https://iberolab-es.github.io/IberoLab/assets/brand/iberolab-social-card.png">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="https://iberolab-es.github.io/IberoLab/assets/brand/iberolab-social-card.png">
  <title>IberoLab — Conversor breve experimental</title>'''
replace(
    "docs/convertir.html",
    '  <meta name="description" content="Adaptación fonética experimental de nombres, palabras y frases breves mediante signos ibéricos normalizados.">\n  <title>IberoLab — Conversor breve experimental</title>',
    META_CONVERTER,
)

TOPBAR_CSS = '''    .site-topbar { display: flex; align-items: center; justify-content: space-between; gap: 18px; flex-wrap: wrap; margin-bottom: 26px; }
    .site-brand { display: inline-flex; align-items: center; gap: 11px; color: var(--text); text-decoration: none; font-size: 1.1rem; font-weight: 900; }
    .site-brand img { width: 46px; height: 46px; }
    .site-nav { display: flex; flex-wrap: wrap; gap: 12px; }
    .site-nav a { color: var(--muted); text-decoration: none; font-weight: 750; }
    .site-nav a:hover { color: var(--text); }
'''
replace(
    "docs/convertir.html",
    "    .topline { display: flex; justify-content: space-between; align-items: center; gap: 16px; }",
    TOPBAR_CSS + "    .topline { display: flex; justify-content: space-between; align-items: center; gap: 16px; }",
)

TOPBAR = '''  <div class="site-topbar">
    <a class="site-brand" href="./"><img src="assets/brand/iberolab-mark.svg" alt="Símbolo de IberoLab"><span>IberoLab</span></a>
    <nav class="site-nav" aria-label="Navegación principal">
      <a href="convertir.html">Demostrador</a>
      <a href="./">Corpus</a>
      <a href="academia.html">Universidades</a>
      <a href="https://github.com/iberolab-es/IberoLab">GitHub</a>
    </nav>
  </div>
'''
replace("docs/convertir.html", "<main>\n  <header>", "<main>\n" + TOPBAR + "  <header>")
replace(
    "docs/convertir.html",
    '    Capa gráfica MVP: 38 SVG normalizados de la serie “Sign Iber Noro Dual 01–38”, con procedencia, licencia CC0, tamaño y SHA-256 versionados en un manifiesto independiente del corpus científico. ¿Has detectado una adaptación mejorable? <a href="https://github.com/iberolab-es/IberoLab/issues/new/choose" target="_blank" rel="noopener noreferrer">Enviar una sugerencia</a>.',
    '    Capa gráfica MVP: 38 SVG normalizados de la serie “Sign Iber Noro Dual 01–38”, con procedencia, licencia CC0, tamaño y SHA-256 versionados en un manifiesto independiente del corpus científico. ¿Has detectado una adaptación mejorable? <a href="https://github.com/iberolab-es/IberoLab/issues/new/choose" target="_blank" rel="noopener noreferrer">Enviar una sugerencia</a>.<br><br>\n    <a href="academia.html">Información académica</a> · <a href="privacidad.html">Privacidad</a>.',
)

# Add academic/public browser checks to current main tests, preserving history tests.
tests = ROOT / "tests" / "browser" / "browser-smoke.spec.cjs"
text = tests.read_text(encoding="utf-8")
anchor = "test.describe('demostrador MVP de entradas breves', () => {"
if anchor not in text:
    raise RuntimeError("browser test anchor not found")
public_tests = '''test.describe('presencia pública y académica', () => {
  test('la página académica publica límites y vías de revisión', async ({ page }) => {
    await page.goto('/academia.html', { waitUntil: 'load' });
    await expect(page.getByRole('heading', { name: /Un proyecto pequeño/ })).toBeVisible();
    await expect(page.getByText('IberoLab no traduce al idioma ibérico')).toBeVisible();
    await expect(page.getByRole('link', { name: 'Enviar una aportación' })).toBeVisible();
    await expect(page.getByText('English summary')).toBeVisible();
  });

  test('corpus y demostrador exponen identidad y metadatos sociales', async ({ page }) => {
    for (const path of ['/', '/convertir.html']) {
      await page.goto(path, { waitUntil: 'load' });
      await expect(page.locator('.site-brand img')).toHaveCount(1);
      await expect(page.getByRole('link', { name: 'Universidades' })).toBeVisible();
      await expect(page.locator('link[rel="canonical"]')).toHaveCount(1);
      await expect(page.locator('meta[property="og:image"]')).toHaveCount(1);
    }
  });
});

'''
text = text.replace(anchor, public_tests + anchor, 1)
tests.write_text(text, encoding="utf-8")

# Insert public changelog after the existing local-history entry from main.
changelog = ROOT / "CHANGELOG.md"
text = changelog.read_text(encoding="utf-8")
anchor = "## Unreleased — resultados compartibles y frases más claras"
entry = '''## Unreleased — identidad y presencia académica

- Se incorpora una identidad visual propia y explícitamente contemporánea.
- Se publica una página bilingüe para universidades y especialistas.
- Se añaden citación, privacidad, sitemap, robots, manifiesto web y metadatos sociales.
- Corpus y demostrador comparten cabecera, navegación y acceso a revisión académica.

'''
if anchor not in text:
    raise RuntimeError("changelog anchor not found")
text = text.replace(anchor, entry + anchor, 1)
changelog.write_text(text, encoding="utf-8")

print("Public presence reconciled with current main history feature.")
