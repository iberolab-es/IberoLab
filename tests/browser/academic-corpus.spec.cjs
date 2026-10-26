const { test, expect } = require('@playwright/test');
const fs = require('node:fs');
const path = require('node:path');
const seed = JSON.parse(fs.readFileSync(path.join(__dirname, '../../data/corpus/attested-forms.v1.json'), 'utf8'));

for (const width of [360, 720, 1440]) {
  test(`el enlace directo deja la ficha visible bajo la navegación a ${width}px`, async ({ page }) => {
    await page.setViewportSize({ width, height: 900 });
    await page.goto('/corpus.html');
    await page.locator('.catalogue-index a[href="#ib-ne-ebanen-001"]').click();
    const card = await page.locator('#ib-ne-ebanen-001').boundingBox();
    const nav = await page.locator('.public-nav').boundingBox();
    expect(card.y).toBeGreaterThanOrEqual(Math.max(0, nav.y + nav.height));
    await expect(page.locator('#ib-ne-ebanen-001 h2')).toBeInViewport();
  });
}

for (const width of [360, 1440]) {
  test(`el investigador llega al corpus desde la portada a ${width}px`, async ({ page }, testInfo) => {
    await page.setViewportSize({ width, height: 900 });
    await page.goto('/');
    const entry = page.locator('.home-hero').getByRole('link', { name: 'Consultar corpus documentado', exact: true });
    await expect(entry).toBeVisible();
    await entry.click();
    await expect(page).toHaveURL(/\/corpus\.html$/);
    await expect(page.getByRole('heading', { name: 'Corpus documentado en el navegador.' })).toBeVisible();
    await expect(page.locator('.catalogue-card')).toHaveCount(11);
    await expect(page.locator('.catalogue-scope')).toContainText('0 ediciones de inscripciones completas');
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);
    if (testInfo.project.name === 'chromium') {
      await page.screenshot({ path: testInfo.outputPath(`corpus-${width}.png`), fullPage: true });
    }
    await page.goto('/academia.html');
    const academicEntry = page.locator('header .actions a').first();
    await expect(academicEntry).toHaveAttribute('href', 'corpus.html');
    await academicEntry.click();
    await expect(page.locator('#catalogueStatus')).toHaveText('11 de 11 fichas disponibles.');
    await page.locator('#interpretationFilter').selectOption('disputed');
    await expect(page.locator('.catalogue-card:visible')).toHaveCount(1);
    await expect(page.locator('.catalogue-card:visible h2')).toHaveText('ebanen');
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);
    if (testInfo.project.name === 'chromium') {
      await page.screenshot({ path: testInfo.outputPath(`interpretacion-discutida-${width}.png`), fullPage: true });
    }
  });
}

test('todas las fichas conservan lectura, tokens, certeza y bibliografía del conjunto de datos', async ({ page }) => {
  await page.goto('/corpus.html');
  for (const form of seed.forms) {
    const card = page.locator(`#${form.id}`);
    await expect(card.locator('h2')).toHaveText(form.form);
    await expect(card.locator('.catalogue-reading')).toHaveText(form.form);
    await expect(card.locator('.grapheme-sequence')).toHaveText(form.grapheme_sequence.join(' · '));
    await expect(card.locator('.linguistic-status')).toHaveAttribute('data-status', 'not_catalogued');
    await expect(card.locator('.reading-confidence')).toContainText('sin escala calibrada');
    expect(await card.locator('.catalogue-sources a').evaluateAll(links => links.map(link => link.href))).toEqual(form.sources.map(source => source.url));
    await expect(card.locator('.catalogue-actions a').first()).toHaveAttribute('href', `./#${form.id}`);
  }
});

test('búsqueda y filtros no confunden hipótesis con lectura ni crean resultados', async ({ page }) => {
  await page.goto('/corpus.html');
  const search = page.locator('#catalogueSearch');
  await search.fill('seltar');
  await expect(page.locator('.catalogue-card:visible h2')).toHaveText('seltar');
  await page.locator('#interpretationFilter').selectOption('disputed');
  await expect(page.locator('#catalogueEmpty')).toBeVisible();
  await expect(page.locator('#catalogueStatus')).toHaveText('0 de 11 fichas disponibles.');
  await page.getByRole('button', { name: 'Restablecer' }).click();
  await page.locator('#interpretationFilter').selectOption('supported_hypothesis');
  await expect(page.locator('.catalogue-card:visible h2')).toHaveText('erder');
  // An index link must reveal a record hidden by the current filters.
  await page.getByRole('navigation', { name: 'Índice de las once formas' }).getByRole('link', { name: 'taŕśabań', exact: true }).click();
  await expect(page.locator('#ib-ne-tarsaban-001')).toBeVisible();
  await expect(page.locator('#catalogueSearch')).toHaveValue('');
  await expect(page.locator('#interpretationFilter')).toHaveValue('all');
  await search.fill('palabra-inexistente');
  await expect(page.locator('.catalogue-card:visible')).toHaveCount(0);
});

test('los enlaces directos abren las once fichas y su fuente sin pasar por GitHub', async ({ page }) => {
  for (const form of seed.forms) {
    await page.goto(`/corpus.html#${form.id}`);
    await expect(page.locator(`#${form.id}`)).toBeInViewport();
    await expect(page.locator(`#${form.id} .catalogue-sources a`).first()).toHaveAttribute('href', form.sources[0].url);
  }
});

test('las once fichas y las referencias se leen sin JavaScript', async ({ browser, baseURL }) => {
  const context = await browser.newContext({ javaScriptEnabled: false, baseURL });
  const page = await context.newPage();
  try {
    await page.goto('/corpus.html#ib-ne-ebanen-001');
    await expect(page.locator('.catalogue-card')).toHaveCount(11);
    await expect(page.locator('#ib-ne-ebanen-001')).toBeInViewport();
    await expect(page.locator('#ib-ne-ebanen-001 .semantic-label')).toHaveText('Interpretación discutida');
    await expect(page.locator('#catalogueTools')).toBeHidden();
    // Playwright omits NOSCRIPT roots from its text matcher; assert the rendered paragraph.
    await expect(page.locator('noscript p')).toBeVisible();
    await expect(page.locator('noscript p')).toContainText('las once fichas y sus referencias siguen disponibles');
  } finally {
    await context.close();
  }
});

test('la búsqueda y las notas pueden manejarse con teclado', async ({ page }) => {
  await page.goto('/corpus.html');
  await page.keyboard.press('Tab');
  await expect(page.getByRole('link', { name: 'Saltar al contenido' })).toBeFocused();
  await page.keyboard.press('Enter');
  await expect(page.locator('#contenido')).toBeFocused();
  const search = page.locator('#catalogueSearch');
  await search.focus();
  await page.keyboard.type('ebanen');
  await search.press('Enter');
  await expect(page.locator('.catalogue-card:visible')).toHaveCount(1);
  const summary = page.locator('#ib-ne-ebanen-001 summary');
  await summary.focus();
  await summary.press('Enter');
  await expect(page.locator('#ib-ne-ebanen-001 details')).toHaveAttribute('open', '');
});
