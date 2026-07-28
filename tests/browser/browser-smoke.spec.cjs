const { test, expect } = require('@playwright/test');

const FORMS = [
  { id: 'ib-ne-ildirda-001', form: 'ildiŕda', cards: 5, pending: 0 },
  { id: 'ib-ne-erder-001', form: 'erder', cards: 4, pending: 0 },
  { id: 'ib-ne-undikesken-001', form: 'undikesken', cards: 7, pending: 0 },
  { id: 'ib-ne-ars-001', form: 'ars', cards: 3, pending: 0 },
  { id: 'ib-ne-ekiar-001', form: 'ekiar', cards: 4, pending: 0 },
  { id: 'ib-ne-egiar-001', form: 'egiar', cards: 4, pending: 0 },
  { id: 'ib-ne-likine-001', form: 'likine', cards: 5, pending: 0 },
  { id: 'ib-ne-tarsaban-001', form: 'taŕśabań', cards: 6, pending: 0 },
  { id: 'ib-ne-baisetas-001', form: 'baisetaś', cards: 6, pending: 0 },
  { id: 'ib-ne-seltar-001', form: 'seltar', cards: 5, pending: 0 },
  { id: 'ib-ne-ebanen-001', form: 'ebanen', cards: 5, pending: 0 }
];

const MVP_CASES = [
  { input: 'amor', reading: 'a · m · o · r', cards: 4, status: 'direct' },
  { input: 'familia', reading: 'ba · m · i · l · i · a', cards: 6, status: 'approximate' },
  { input: 'te quiero', reading: 'te / ki · e · r · o', cards: 5, status: 'direct' },
  { input: 'hogar', reading: 'o · ga · r', cards: 3, status: 'direct' },
  { input: 'amistad', reading: 'a · m · i · s · ta · da', cards: 6, status: 'approximate' }
];

async function imagesAreLoaded(page, selector) {
  return page.locator(selector).evaluateAll(images =>
    images.every(image => image.complete && image.naturalWidth > 0 && image.naturalHeight > 0)
  );
}

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
      expect(await imagesAreLoaded(page, '#glyphOutput img')).toBe(true);
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
  expect(report.version).toBe('1.2.0');
  expect(report.asset_mode).toBe('local_repository');
  expect(report.result).toBe('pass');
  expect(report.metrics).toMatchObject({
    forms_evaluated: 11,
    forms_total: 11,
    svg_loaded: 19,
    svg_total: 19,
    failed_svg_tokens: [],
    empty_outputs: 0,
    pending_tokens: [],
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

test.describe('presencia pública y académica', () => {
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
      await expect(page.locator('.site-nav').getByRole('link', { name: 'Universidades', exact: true })).toBeVisible();
      await expect(page.locator('link[rel="canonical"]')).toHaveCount(1);
      await expect(page.locator('meta[property="og:image"]')).toHaveCount(1);
    }
  });
});

test.describe('demostrador MVP de entradas breves', () => {
  for (const target of MVP_CASES) {
    test(`${target.input} produce una adaptación visible y explicada`, async ({ page }) => {
      await page.goto('/convertir.html', { waitUntil: 'load' });
      await expect(page.locator('html')).toHaveAttribute('data-mvp-converter-ready', 'true');

      await page.locator('#sourceInput').fill(target.input);
      await page.getByRole('button', { name: 'Adaptar a signos ibéricos' }).click();

      await expect(page.locator('html')).toHaveAttribute('data-mvp-result', 'success');
      await expect(page.locator('html')).toHaveAttribute('data-mvp-status', target.status);
      await expect(page.locator('#technicalReading')).toHaveText(target.reading);
      await expect(page.locator('#glyphOutput .sign-card')).toHaveCount(target.cards);
      await expect(page.locator('#glyphOutput .sign-card.failed')).toHaveCount(0);
      await expect(page.locator('#glyphOutput img')).toHaveCount(target.cards);
      expect(await imagesAreLoaded(page, '#glyphOutput img')).toBe(true);
      await expect(page.getByText('No es traducción')).toBeVisible();
    });
  }

  test('familia declara la aproximación de f mediante la serie labial', async ({ page }) => {
    await page.goto('/convertir.html', { waitUntil: 'load' });
    await page.locator('#sourceInput').fill('familia');
    await page.getByRole('button', { name: 'Adaptar a signos ibéricos' }).click();
    await expect(page.locator('#noticeList')).toContainText('f no tiene equivalente directo');
    await expect(page.locator('#statusBadge')).toHaveText('Adaptación con aproximaciones');
  });

  test('amistad declara la vocal de apoyo de la oclusiva final', async ({ page }) => {
    await page.goto('/convertir.html', { waitUntil: 'load' });
    await page.locator('#sourceInput').fill('amistad');
    await page.getByRole('button', { name: 'Adaptar a signos ibéricos' }).click();
    await expect(page.locator('#noticeList')).toContainText('vocal de apoyo');
    await expect(page.locator('#technicalReading')).toHaveText('a · m · i · s · ta · da');
  });

  test('una URL compartida restaura la entrada y su resultado', async ({ page }) => {
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

  test('el historial local conserva, reutiliza y borra entradas recientes', async ({ page }) => {
    await page.goto('/convertir.html', { waitUntil: 'load' });
    await page.locator('#sourceInput').fill('hogar');
    await page.getByRole('button', { name: 'Adaptar a signos ibéricos' }).click();
    await page.locator('#sourceInput').fill('familia');
    await page.getByRole('button', { name: 'Adaptar a signos ibéricos' }).click();

    await page.reload({ waitUntil: 'load' });
    await expect(page.locator('#historySection')).toBeVisible();
    await expect(page.locator('#historyList .history-item')).toHaveText(['familia', 'hogar']);

    await page.locator('#historyList').getByRole('button', { name: 'hogar', exact: true }).click();
    await expect(page.locator('#sourceInput')).toHaveValue('hogar');
    await expect(page.locator('#technicalReading')).toHaveText('o · ga · r');

    await page.getByRole('button', { name: 'Borrar historial' }).click();
    await expect(page.locator('#historySection')).toBeHidden();
    expect(await page.evaluate(() => localStorage.getItem('iberolab:mvp:recent:v1'))).toBeNull();
  });

  test('una entrada no admitida se bloquea sin signos parciales', async ({ page }) => {
    await page.goto('/convertir.html', { waitUntil: 'load' });
    await page.locator('#sourceInput').fill('123');
    await page.getByRole('button', { name: 'Adaptar a signos ibéricos' }).click();
    await expect(page.locator('html')).toHaveAttribute('data-mvp-result', 'blocked');
    await expect(page.locator('#glyphOutput .sign-card')).toHaveCount(0);
    await expect(page.locator('#technicalReading')).toHaveText('—');
    await expect(page.locator('#statusBadge')).toHaveText('No se ha generado una salida');
  });
});
