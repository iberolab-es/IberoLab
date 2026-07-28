#!/usr/bin/env python3
"""Add shareable MVP result URLs and clearer word grouping."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace(path: str, old: str, new: str, expected: int = 1) -> None:
    target = ROOT / path
    text = target.read_text(encoding="utf-8")
    count = text.count(old)
    if count != expected:
        raise RuntimeError(f"{path}: expected {expected} occurrence(s), found {count}: {old!r}")
    target.write_text(text.replace(old, new), encoding="utf-8")


# Styling: identify words and provide a compact action status line.
replace(
    "docs/convertir.html",
    '    .word-group { display: flex; flex-wrap: wrap; gap: 9px; align-items: center; padding: 4px 0; }',
    '    .word-group { display: grid; gap: 7px; align-items: start; padding: 4px 0; }\n'
    '    .word-label { color: var(--accent); font-size: .76rem; font-weight: 850; letter-spacing: .04em; }\n'
    '    .word-signs { display: flex; flex-wrap: wrap; gap: 9px; align-items: center; }',
)
replace(
    "docs/convertir.html",
    '    .actions { display: flex; flex-wrap: wrap; gap: 9px; margin-top: 14px; }',
    '    .actions { display: flex; flex-wrap: wrap; gap: 9px; margin-top: 14px; }\n'
    '    .action-status { min-height: 1.35em; margin-top: 8px; color: var(--muted); font-size: .85rem; }',
)

# Interface: add share action and accessible feedback.
replace(
    "docs/convertir.html",
    '        <button id="copyButton" class="secondary" type="button">Copiar lectura técnica</button>\n      </div>',
    '        <button id="copyButton" class="secondary" type="button">Copiar lectura técnica</button>\n'
    '        <button id="shareButton" class="secondary" type="button">Compartir resultado</button>\n'
    '      </div>\n'
    '      <div id="actionStatus" class="action-status" role="status" aria-live="polite"></div>',
)

# Runtime references.
replace(
    "docs/convertir.html",
    '  const copyButton = document.getElementById("copyButton");\n  let currentResult = null;',
    '  const copyButton = document.getElementById("copyButton");\n'
    '  const shareButton = document.getElementById("shareButton");\n'
    '  const actionStatus = document.getElementById("actionStatus");\n'
    '  let currentResult = null;',
)

# Word groups display their original word above the glyph sequence.
replace(
    "docs/convertir.html",
    '      const group = document.createElement("div");\n'
    '      group.className = "word-group";\n'
    '      group.dataset.sourceWord = word.source;\n'
    '      group.append(...word.tokens.map(createSignCard));\n'
    '      output.append(group);',
    '      const group = document.createElement("div");\n'
    '      group.className = "word-group";\n'
    '      group.dataset.sourceWord = word.source;\n'
    '      const wordLabel = document.createElement("div");\n'
    '      wordLabel.className = "word-label";\n'
    '      wordLabel.textContent = word.source;\n'
    '      const signs = document.createElement("div");\n'
    '      signs.className = "word-signs";\n'
    '      signs.append(...word.tokens.map(createSignCard));\n'
    '      group.append(wordLabel, signs);\n'
    '      output.append(group);',
)

# Disable and enable share consistently.
replace(
    "docs/convertir.html",
    '      copyButton.disabled = true;\n      renderNotices(result);',
    '      copyButton.disabled = true;\n      shareButton.disabled = true;\n      actionStatus.textContent = "";\n      renderNotices(result);',
)
replace(
    "docs/convertir.html",
    '    copyButton.disabled = false;\n    renderNotices(result);',
    '    copyButton.disabled = false;\n    shareButton.disabled = false;\n    actionStatus.textContent = "";\n    renderNotices(result);',
)

# Shareable query parameters and browser navigation.
replace(
    "docs/convertir.html",
    '  function convert() {\n    renderResult(window.IberoMvp.convert(input.value));\n  }',
    '  function resultUrl(value = input.value) {\n'
    '    const url = new URL(window.location.href);\n'
    '    const trimmed = value.trim();\n'
    '    if (trimmed) url.searchParams.set("q", trimmed);\n'
    '    else url.searchParams.delete("q");\n'
    '    return url;\n'
    '  }\n\n'
    '  function convert({ updateUrl = true } = {}) {\n'
    '    renderResult(window.IberoMvp.convert(input.value));\n'
    '    if (updateUrl) {\n'
    '      const url = resultUrl();\n'
    '      window.history.replaceState(null, "", `${url.pathname}${url.search}${url.hash}`);\n'
    '    }\n'
    '  }\n\n'
    '  function loadFromUrl() {\n'
    '    const sharedInput = new URL(window.location.href).searchParams.get("q");\n'
    '    if (sharedInput !== null) input.value = sharedInput;\n'
    '    updateCounter();\n'
    '    convert({ updateUrl: false });\n'
    '  }',
)

# Sharing uses the native sheet on supported devices and clipboard as fallback.
replace(
    "docs/convertir.html",
    '  copyButton.addEventListener("click", async () => {\n'
    '    if (!currentResult || currentResult.executionStatus !== "success") return;\n'
    '    try {\n'
    '      await navigator.clipboard.writeText(currentResult.technicalReading);\n'
    '      copyButton.textContent = "Lectura copiada";\n'
    '      setTimeout(() => { copyButton.textContent = "Copiar lectura técnica"; }, 1600);\n'
    '    } catch {\n'
    '      copyButton.textContent = "No se pudo copiar";\n'
    '    }\n'
    '  });\n\n'
    '  updateCounter();\n'
    '  convert();',
    '  copyButton.addEventListener("click", async () => {\n'
    '    if (!currentResult || currentResult.executionStatus !== "success") return;\n'
    '    try {\n'
    '      await navigator.clipboard.writeText(currentResult.technicalReading);\n'
    '      copyButton.textContent = "Lectura copiada";\n'
    '      actionStatus.textContent = "La lectura técnica se ha copiado.";\n'
    '      setTimeout(() => { copyButton.textContent = "Copiar lectura técnica"; actionStatus.textContent = ""; }, 1600);\n'
    '    } catch {\n'
    '      copyButton.textContent = "No se pudo copiar";\n'
    '      actionStatus.textContent = "El navegador no ha permitido copiar la lectura.";\n'
    '    }\n'
    '  });\n\n'
    '  shareButton.addEventListener("click", async () => {\n'
    '    if (!currentResult || currentResult.executionStatus !== "success") return;\n'
    '    const url = resultUrl(currentResult.original).toString();\n'
    '    const text = `IberoLab — ${currentResult.original}\\n${currentResult.technicalReading}\\nAdaptación fonética experimental; no es una traducción.`;\n'
    '    try {\n'
    '      if (typeof navigator.share === "function") {\n'
    '        await navigator.share({ title: "IberoLab", text, url });\n'
    '        actionStatus.textContent = "Resultado compartido.";\n'
    '      } else {\n'
    '        await navigator.clipboard.writeText(`${text}\\n${url}`);\n'
    '        actionStatus.textContent = "Enlace y lectura copiados para compartir.";\n'
    '      }\n'
    '      setTimeout(() => { actionStatus.textContent = ""; }, 2200);\n'
    '    } catch (error) {\n'
    '      if (error?.name !== "AbortError") actionStatus.textContent = "No se pudo compartir el resultado.";\n'
    '    }\n'
    '  });\n\n'
    '  window.addEventListener("popstate", loadFromUrl);\n'
    '  loadFromUrl();',
)

# Static validation markers.
validator = ROOT / "scripts" / "validate_mvp_converter.py"
text = validator.read_text(encoding="utf-8")
anchor = '        "Escuchar entrada en español",\n'
if anchor not in text:
    raise RuntimeError("validator page marker anchor not found")
text = text.replace(
    anchor,
    anchor + '        "Compartir resultado",\n        \'id="actionStatus"\',\n        \'class="word-label"\',\n        \'searchParams.set("q", trimmed)\',\n        "navigator.share",\n',
    1,
)
validator.write_text(text, encoding="utf-8")

# Browser regression: shared URL restore, word labels and native share payload.
tests = ROOT / "tests" / "browser" / "browser-smoke.spec.cjs"
text = tests.read_text(encoding="utf-8")
anchor = "  test('una entrada no admitida se bloquea sin signos parciales', async ({ page }) => {"
if anchor not in text:
    raise RuntimeError("browser test insertion anchor not found")
new_tests = '''  test('una URL compartida restaura la entrada y su resultado', async ({ page }) => {
    await page.goto('/convertir.html?q=te%20quiero', { waitUntil: 'load' });
    await expect(page.locator('#sourceInput')).toHaveValue('te quiero');
    await expect(page.locator('#technicalReading')).toHaveText('te / ki · e · r · o');
    await expect(page.locator('.word-label')).toHaveText(['te', 'quiero']);
  });

  test('al adaptar se actualiza la URL compartible', async ({ page }) => {
    await page.goto('/convertir.html', { waitUntil: 'load' });
    await page.locator('#sourceInput').fill('amistad');
    await page.getByRole('button', { name: 'Adaptar a signos ibéricos' }).click();
    expect(new URL(page.url()).searchParams.get('q')).toBe('amistad');
  });

  test('compartir usa la hoja nativa con lectura y enlace restaurable', async ({ page }) => {
    await page.addInitScript(() => {
      window.__iberoShared = null;
      Object.defineProperty(navigator, 'share', {
        configurable: true,
        value: async payload => { window.__iberoShared = payload; }
      });
    });
    await page.goto('/convertir.html', { waitUntil: 'load' });
    await page.locator('#sourceInput').fill('amor');
    await page.getByRole('button', { name: 'Adaptar a signos ibéricos' }).click();
    await page.getByRole('button', { name: 'Compartir resultado' }).click();
    const payload = await page.evaluate(() => window.__iberoShared);
    expect(payload.text).toContain('a · m · o · r');
    expect(new URL(payload.url).searchParams.get('q')).toBe('amor');
  });

'''
text = text.replace(anchor, new_tests + anchor, 1)
tests.write_text(text, encoding="utf-8")

# Changelog entry.
changelog = ROOT / "CHANGELOG.md"
text = changelog.read_text(encoding="utf-8")
marker = "## "
index = text.find(marker)
entry = "## Unreleased — resultados compartibles y frases más claras\n\n- Los resultados del demostrador disponen de URL restaurable mediante `?q=`.\n- Se añade compartir nativo en móvil con copia al portapapeles como alternativa.\n- Las frases muestran el rótulo de cada palabra sobre su grupo de signos.\n- La regresión comprueba restauración, actualización de URL y contenido compartido.\n\n"
if index < 0:
    text = entry + text
else:
    text = text[:index] + entry + text[index:]
changelog.write_text(text, encoding="utf-8")

print("Shareable MVP result links and word grouping applied.")
