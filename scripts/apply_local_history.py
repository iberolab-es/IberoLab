#!/usr/bin/env python3
"""Add a small private on-device history to the public MVP converter."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace(path: str, old: str, new: str, expected: int = 1) -> None:
    target = ROOT / path
    text = target.read_text(encoding="utf-8")
    count = text.count(old)
    if count != expected:
        raise RuntimeError(f"{path}: expected {expected} occurrence(s), found {count}: {old!r}")
    target.write_text(text.replace(old, new), encoding="utf-8")


# Styles for a compact, mobile-first recent-results section.
replace(
    "docs/convertir.html",
    '    .counter { margin-top: 8px; color: var(--muted); font-size: .85rem; }',
    '    .counter { margin-top: 8px; color: var(--muted); font-size: .85rem; }\n'
    '    .history { margin-top: 18px; padding-top: 16px; border-top: 1px solid var(--line); }\n'
    '    .history[hidden] { display: none; }\n'
    '    .history-head { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 10px; }\n'
    '    .history-head h2 { margin: 0; font-size: 1rem; }\n'
    '    .history-list { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px; }\n'
    '    button.history-item { min-height: 38px; padding: 0 13px; background: rgba(89,211,155,.1); color: var(--ok); }\n'
    '    button.history-clear { min-height: 36px; padding: 0 12px; background: transparent; color: var(--muted); }\n'
    '    .history-note { margin: 9px 0 0; color: var(--muted); font-size: .82rem; line-height: 1.45; }',
)

# Public section, hidden until the device has stored a successful adaptation.
replace(
    "docs/convertir.html",
    '    <p class="counter">Ejemplos orientativos. Puedes escribir cualquier nombre, palabra o frase breve.</p>\n\n    <section id="resultSection"',
    '    <p class="counter">Ejemplos orientativos. Puedes escribir cualquier nombre, palabra o frase breve.</p>\n\n'
    '    <section id="historySection" class="history" aria-labelledby="historyTitle" hidden>\n'
    '      <div class="history-head">\n'
    '        <h2 id="historyTitle">Recientes en este dispositivo</h2>\n'
    '        <button id="clearHistoryButton" class="history-clear" type="button">Borrar historial</button>\n'
    '      </div>\n'
    '      <div id="historyList" class="history-list"></div>\n'
    '      <p class="history-note">Se guardan como máximo cinco entradas y solo en este navegador. IberoLab no recibe este historial.</p>\n'
    '    </section>\n\n'
    '    <section id="resultSection"',
)

# Runtime references and constants.
replace(
    "docs/convertir.html",
    '  const actionStatus = document.getElementById("actionStatus");\n  let currentResult = null;',
    '  const actionStatus = document.getElementById("actionStatus");\n'
    '  const historySection = document.getElementById("historySection");\n'
    '  const historyList = document.getElementById("historyList");\n'
    '  const clearHistoryButton = document.getElementById("clearHistoryButton");\n'
    '  const HISTORY_KEY = "iberolab:mvp:recent:v1";\n'
    '  const HISTORY_LIMIT = 5;\n'
    '  let currentResult = null;',
)

# History helpers are deliberately local-only and failure tolerant.
replace(
    "docs/convertir.html",
    '  function createSignCard(token) {',
    '  function readHistory() {\n'
    '    try {\n'
    '      const parsed = JSON.parse(window.localStorage.getItem(HISTORY_KEY) || "[]");\n'
    '      if (!Array.isArray(parsed)) return [];\n'
    '      return parsed.filter(item => typeof item === "string" && item.trim()).slice(0, HISTORY_LIMIT);\n'
    '    } catch {\n'
    '      return [];\n'
    '    }\n'
    '  }\n\n'
    '  function writeHistory(entries) {\n'
    '    try {\n'
    '      if (entries.length) window.localStorage.setItem(HISTORY_KEY, JSON.stringify(entries));\n'
    '      else window.localStorage.removeItem(HISTORY_KEY);\n'
    '      return true;\n'
    '    } catch {\n'
    '      return false;\n'
    '    }\n'
    '  }\n\n'
    '  function renderHistory() {\n'
    '    const entries = readHistory();\n'
    '    historyList.replaceChildren();\n'
    '    historySection.hidden = entries.length === 0;\n'
    '    for (const value of entries) {\n'
    '      const button = document.createElement("button");\n'
    '      button.className = "history-item";\n'
    '      button.type = "button";\n'
    '      button.dataset.historyValue = value;\n'
    '      button.textContent = value;\n'
    '      button.addEventListener("click", () => {\n'
    '        input.value = value;\n'
    '        updateCounter();\n'
    '        convert();\n'
    '        input.focus();\n'
    '      });\n'
    '      historyList.append(button);\n'
    '    }\n'
    '  }\n\n'
    '  function rememberResult(result) {\n'
    '    if (result.executionStatus !== "success") return;\n'
    '    const value = result.original.trim();\n'
    '    if (!value) return;\n'
    '    const key = value.toLocaleLowerCase("es-ES");\n'
    '    const entries = [value, ...readHistory().filter(item => item.toLocaleLowerCase("es-ES") !== key)].slice(0, HISTORY_LIMIT);\n'
    '    if (writeHistory(entries)) renderHistory();\n'
    '  }\n\n'
    '  function createSignCard(token) {',
)

# Remember only explicit successful conversions; merely opening a shared URL stays passive.
replace(
    "docs/convertir.html",
    '  function convert({ updateUrl = true } = {}) {\n'
    '    renderResult(window.IberoMvp.convert(input.value));\n'
    '    if (updateUrl) {',
    '  function convert({ updateUrl = true, remember = true } = {}) {\n'
    '    const result = window.IberoMvp.convert(input.value);\n'
    '    renderResult(result);\n'
    '    if (remember) rememberResult(result);\n'
    '    if (updateUrl) {',
)
replace(
    "docs/convertir.html",
    '    convert({ updateUrl: false });',
    '    convert({ updateUrl: false, remember: false });',
)

# Clear control and initial rendering.
replace(
    "docs/convertir.html",
    '  speakButton.addEventListener("click", () => {',
    '  clearHistoryButton.addEventListener("click", () => {\n'
    '    if (writeHistory([])) {\n'
    '      renderHistory();\n'
    '      actionStatus.textContent = "Historial local borrado.";\n'
    '      setTimeout(() => { actionStatus.textContent = ""; }, 1600);\n'
    '    } else {\n'
    '      actionStatus.textContent = "El navegador no ha permitido borrar el historial local.";\n'
    '    }\n'
    '  });\n\n'
    '  speakButton.addEventListener("click", () => {',
)
replace(
    "docs/convertir.html",
    '  window.addEventListener("popstate", loadFromUrl);\n  loadFromUrl();',
    '  window.addEventListener("popstate", loadFromUrl);\n  renderHistory();\n  loadFromUrl();',
)

# Static validation markers.
validator = ROOT / "scripts" / "validate_mvp_converter.py"
text = validator.read_text(encoding="utf-8")
anchor = '        "Compartir resultado",\n'
if anchor not in text:
    raise RuntimeError("validator history anchor not found")
text = text.replace(
    anchor,
    anchor + '        "Recientes en este dispositivo",\n        "IberoLab no recibe este historial",\n        \'id="historySection"\',\n        \'HISTORY_KEY = "iberolab:mvp:recent:v1"\',\n        "HISTORY_LIMIT = 5",\n        "window.localStorage",\n',
    1,
)
validator.write_text(text, encoding="utf-8")

# Browser regression for persistence, ordering, reuse and deletion.
tests = ROOT / "tests" / "browser" / "browser-smoke.spec.cjs"
text = tests.read_text(encoding="utf-8")
anchor = "  test('una entrada no admitida se bloquea sin signos parciales', async ({ page }) => {"
if anchor not in text:
    raise RuntimeError("browser history insertion anchor not found")
history_test = '''  test('el historial local conserva, reutiliza y borra entradas recientes', async ({ page }) => {
    await page.goto('/convertir.html', { waitUntil: 'load' });
    await page.locator('#sourceInput').fill('hogar');
    await page.getByRole('button', { name: 'Adaptar a signos ibéricos' }).click();
    await page.locator('#sourceInput').fill('familia');
    await page.getByRole('button', { name: 'Adaptar a signos ibéricos' }).click();

    await page.reload({ waitUntil: 'load' });
    await expect(page.locator('#historySection')).toBeVisible();
    await expect(page.locator('#historyList .history-item')).toHaveText(['familia', 'hogar']);

    await page.getByRole('button', { name: 'hogar', exact: true }).click();
    await expect(page.locator('#sourceInput')).toHaveValue('hogar');
    await expect(page.locator('#technicalReading')).toHaveText('o · ga · r');

    await page.getByRole('button', { name: 'Borrar historial' }).click();
    await expect(page.locator('#historySection')).toBeHidden();
    expect(await page.evaluate(() => localStorage.getItem('iberolab:mvp:recent:v1'))).toBeNull();
  });

'''
text = text.replace(anchor, history_test + anchor, 1)
tests.write_text(text, encoding="utf-8")

# Changelog entry.
changelog = ROOT / "CHANGELOG.md"
text = changelog.read_text(encoding="utf-8")
marker = "## "
index = text.find(marker)
entry = "## Unreleased — historial local privado\n\n- El demostrador recuerda como máximo cinco adaptaciones exitosas en el navegador.\n- Las entradas recientes pueden reutilizarse con un toque y borrarse por completo.\n- No se guarda el historial en IberoLab ni se envía a ningún servidor del proyecto.\n- La regresión comprueba persistencia, orden, reutilización y borrado.\n\n"
text = entry + text if index < 0 else text[:index] + entry + text[index:]
changelog.write_text(text, encoding="utf-8")

print("Private local recent-results history applied.")
