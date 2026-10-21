const { test, expect } = require('@playwright/test');
const { execFileSync } = require('node:child_process');

test('el contexto conduce a ejemplos verificables y conserva sus fuentes', async ({ page }) => {
  await page.goto('/historia.html');
  await page.getByRole('link', { name: 'Dual y no dual', exact: true }).click();
  await expect(page.locator('#dual')).toBeInViewport();
  const details = page.locator('#dual details');
  await details.locator('summary').focus();
  await page.keyboard.press('Enter');
  await expect(details).toHaveAttribute('open', '');
  await expect(details).toContainText('fortis/lenis');
  for (const id of ['ref-mv', 'ref-ferrer']) {
    await expect(page.locator(`#${id} a`)).toHaveAttribute('href', /\.pdf$/);
  }
  await page.getByRole('link', { name: 'mundo → m · u · n · do', exact: true }).click();
  await expect(page.locator('#sourceInput')).toHaveValue('mundo');
  await expect(page.locator('#technicalReading')).toHaveText('m · u · n · do');
  const procedure = page.locator('#como-funciona');
  await procedure.locator('summary').focus();
  await page.keyboard.press('Enter');
  await expect(procedure).toHaveAttribute('open', '');
  await page.locator('#sourceInput').fill('familia');
  await page.locator('#converterForm button').click();
  await expect(page.locator('#technicalReading')).toHaveText('ba · m · i · l · i · a');
  await expect(page.locator('#noticeList')).toContainText('f no tiene equivalente directo');
});

test('la portada permite saltar con teclado y destaca el conversor', async ({ page }) => {
  await page.goto('/');
  await page.keyboard.press('Tab');
  await expect(page.getByRole('link', { name: 'Saltar al contenido' })).toBeFocused();
  await page.keyboard.press('Enter');
  await expect(page.locator('#contenido')).toBeFocused();
  await expect(page.locator('.home-hero')).toContainText('No reconstruye su pronunciación');
  const order = await page.locator('main > section').evaluateAll(sections => sections.slice(0, 2).map(s => s.textContent));
  expect(order[0]).toContain('Conversor experimental de escritura');
  expect(order[1]).toContain('La escritura se entiende mejor');
  await page.locator('.home-hero').getByRole('link', { name: 'Probar conversor', exact: true }).click();
  await expect(page.locator('#sourceInput')).toBeEditable();
});

for (const width of [360, 1440]) {
  test(`navegación, signos y capturas a ${width}px`, async ({ page }, testInfo) => {
    await page.setViewportSize({ width, height: 900 });
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    for (const [slug, path] of [['inicio', '/'], ['contexto', '/historia.html'], ['conversor', '/convertir.html'], ['metodologia', '/metodologia.html'], ['academia', '/academia.html']]) {
      await page.goto(path, { waitUntil: 'networkidle' });
      await expect(page.locator('h1')).toHaveCount(1);
      expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);
      await expect(page.locator('nav').getByRole('link', { name: 'Documentación académica', exact: true }).first()).toBeVisible();
      expect(await page.locator('img').evaluateAll(images => images.every(img => img.complete && img.naturalWidth > 0))).toBe(true);
      expect(errors).toEqual([]);
      if (testInfo.project.name === 'chromium') await page.screenshot({ path: testInfo.outputPath(`${slug}-${width}-despues.png`), fullPage: true });
    }
    if (testInfo.project.name === 'chromium' && process.env.REVIEW_BASE_SHA) {
      const base = process.env.REVIEW_BASE_SHA;
      if (!/^[a-f0-9]{40}$/.test(base)) throw new Error('Invalid baseline SHA');
      const original = execFileSync('git', ['show', `${base}:docs/index.html`], { encoding: 'utf8' });
      const css = execFileSync('git', ['show', `${base}:docs/public-site.css`], { encoding: 'utf8' });
      await page.route('**/public-site.css', route => route.fulfill({ contentType: 'text/css', body: css }));
      await page.route('**/?baseline-review', route => route.fulfill({ contentType: 'text/html', body: original }));
      await page.goto('/?baseline-review', { waitUntil: 'networkidle' });
      await page.screenshot({ path: testInfo.outputPath(`inicio-${width}-antes.png`), fullPage: true });
    }
  });
}
