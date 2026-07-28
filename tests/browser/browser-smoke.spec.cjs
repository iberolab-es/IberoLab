const { test, expect } = require('@playwright/test');

const FORMS = [
  { id: 'ib-ne-ildirda-001', form: 'ildiŕda', cards: 5, pending: 0 },
  { id: 'ib-ne-erder-001', form: 'erder', cards: 4, pending: 0 },
  { id: 'ib-ne-undikesken-001', form: 'undikesken', cards: 7, pending: 0 },
  { id: 'ib-ne-ars-001', form: 'ars', cards: 3, pending: 0 },
  { id: 'ib-ne-ekiar-001', form: 'ekiar', cards: 4, pending: 0 },
  { id: 'ib-ne-egiar-001', form: 'egiar', cards: 4, pending: 0 },
  { id: 'ib-ne-likine-001', form: 'likine', cards: 5, pending: 0 },
  { id: 'ib-ne-tarsaban-001', form: 'taŕśabań', cards: 6, pending: 1 },
  { id: 'ib-ne-baisetas-001', form: 'baisetaś', cards: 6, pending: 0 },
  { id: 'ib-ne-seltar-001', form: 'seltar', cards: 5, pending: 0 },
  { id: 'ib-ne-ebanen-001', form: 'ebanen', cards: 5, pending: 0 }
];

test.describe('renderizador local por enlaces profundos', () => {
  for (const target of FORMS) {
    test(`${target.form} selecciona y carga su salida`, async ({ page }) => {
      await page.goto(`/#${target.id}`, { waitUntil: 'load' });

      await expect(page.locator('html')).toHaveAttribute('data-renderer-ready', 'true');
      await expect(page.locator('#formSelect')).toHaveValue(target.id);
      await expect(page.locator('#readingText')).toHaveText(target.form);
      await expect(page.locator('#glyphOutput .sign-card')).toHaveCount(target.cards);
      await expect(page.locator('#glyphOutput .sign-card.failed')).toHaveCount(0);
      await expect(page.locator('#glyphOutput .sign-card.pending')).toHaveCount(target.pending);
      await expect(page.locator('#glyphOutput img')).toHaveCount(target.cards - target.pending);

      const imagesLoaded = await page.locator('#glyphOutput img').evaluateAll(images =>
        images.every(image => image.complete && image.naturalWidth > 0 && image.naturalHeight > 0)
      );
      expect(imagesLoaded).toBe(true);
      expect(new URL(page.url()).hash).toBe(`#${target.id}`);
    });
  }
});

test('el diagnóstico gráfico supera las once formas con SVG locales', async ({ page }) => {
  await page.goto('/test.html', { waitUntil: 'load' });
  await page.getByRole('button', { name: 'Comprobar las 11 formas' }).click();
  await expect(page.locator('html')).toHaveAttribute('data-self-test', 'pass', { timeout: 20_000 });

  const report = JSON.parse(await page.locator('#report').inputValue());
  expect(report.application).toBe('IberoLab browser self-test');
  expect(report.version).toBe('1.1.0');
  expect(report.asset_mode).toBe('local_repository');
  expect(report.result).toBe('pass');
  expect(report.metrics).toMatchObject({
    forms_evaluated: 11,
    forms_total: 11,
    svg_loaded: 18,
    svg_total: 18,
    failed_svg_tokens: [],
    empty_outputs: 0,
    pending_tokens: ['ń'],
    unexpected_pending: [],
    missing_expected_pending: []
  });
});

test('el diagnóstico de enlaces profundos supera los once identificadores', async ({ page }) => {
  test.setTimeout(60_000);
  await page.goto('/deep-link-test.html', { waitUntil: 'load' });
  await page.getByRole('button', { name: 'Comprobar los 11 enlaces' }).click();
  await expect(page.locator('html')).toHaveAttribute('data-deep-link-test', 'pass', { timeout: 45_000 });

  const report = JSON.parse(await page.locator('#report').inputValue());
  expect(report.application).toBe('IberoLab deep-link self-test');
  expect(report.version).toBe('1.0.0');
  expect(report.asset_mode).toBe('local_repository');
  expect(report.result).toBe('pass');
  expect(report.metrics).toEqual({
    links_evaluated: 11,
    links_total: 11,
    links_passed: 11,
    links_failed: 0,
    empty_outputs: 0
  });
  expect(report.links).toHaveLength(11);
  expect(report.links.every(item => item.passed && item.renderer_ready && item.rendered_children > 0)).toBe(true);
});
