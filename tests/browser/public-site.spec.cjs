const { test, expect } = require('@playwright/test');

test('la portada presenta la identidad pública sin ocultar el corpus', async ({ page }) => {
  await page.goto('/', { waitUntil: 'load' });
  await expect(page.getByRole('heading', { name: 'IberoLab' })).toBeVisible();
  await expect(page.getByText('Lengua ibérica · Patrimonio · Tecnología')).toBeVisible();
  await expect(page.getByText('No es un signo ibérico antiguo.')).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Un monograma-glifo contemporáneo.' })).toBeVisible();
  await expect(page.locator('#corpus')).toBeVisible();
  await expect(page.locator('html')).toHaveAttribute('data-renderer-ready', 'true');
  await expect(page.getByRole('link', { name: 'Aprender historia' })).toHaveAttribute('href', 'historia.html');
  await expect(page.getByRole('link', { name: 'Información para universidades' })).toHaveAttribute('href', 'academia.html');
  await expect(page.getByRole('link', { name: 'Abrir «tierra»' })).toHaveAttribute('href', 'convertir.html?q=tierra');
});

test('la muestra de tierra alinea cada rótulo con su SVG correcto', async ({ page }) => {
  await page.goto('/', { waitUntil: 'load' });
  const cards = page.locator('.sample-reading .sample-sign');
  await expect(cards.locator('span')).toHaveText(['ti', 'e', 'ŕ', 'a']);
  await expect(cards.locator('img')).toHaveCount(4);
  expect(await cards.locator('img').evaluateAll(images =>
    images.map(image => new URL(image.src).pathname.split('/').pop())
  )).toEqual(['dual-28-ti.svg', 'dual-02-e.svg', 'dual-34-r2.svg', 'dual-01-a.svg']);
  expect(await cards.locator('img').evaluateAll(images =>
    images.every(image => image.complete && image.naturalWidth > 0 && image.naturalHeight > 0)
  )).toBe(true);
});

test('el conversor propone vocabulario general y permite sentimientos libres', async ({ page }) => {
  await page.goto('/convertir.html', { waitUntil: 'load' });
  await expect(page.locator('#sourceInput')).toHaveValue('hogar');
  await expect(page.locator('.examples .example')).toHaveText(['hogar', 'tierra', 'mundo', 'olivo', 'mar']);
  await expect(page.getByText('Puedes escribir cualquier nombre, sentimiento, palabra o frase breve.')).toBeVisible();
});

test('la portada móvil separa el monograma de la lectura documentada', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/', { waitUntil: 'load' });
  const mark = await page.locator('.hero-mark').boundingBox();
  const tablet = await page.locator('.hero-tablet').boundingBox();
  expect(mark).not.toBeNull();
  expect(tablet).not.toBeNull();
  expect(mark.y + mark.height).toBeLessThanOrEqual(tablet.y);
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= document.documentElement.clientWidth)).toBe(true);
});

test('la página académica ofrece acceso directo a Historia', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/academia.html', { waitUntil: 'load' });
  await expect(page.getByRole('link', { name: 'Historia', exact: true })).toBeVisible();
  await expect(page.getByRole('link', { name: 'Universidades', exact: true })).toHaveAttribute('aria-current', 'page');
});

test('historia mantiene la distinción entre lectura y traducción y prepara YouTube', async ({ page }) => {
  await page.goto('/historia.html', { waitUntil: 'load' });
  await expect(page.getByRole('heading', { name: 'Comprender el mundo ibérico antes de intentar representarlo.' })).toBeVisible();
  await expect(page.getByText('Leer signos no significa traducir la lengua.')).toBeVisible();
  await expect(page.getByText('Una sección preparada para crecer con YouTube.')).toBeVisible();
});

test('metodología identifica el símbolo y separa los dos alcances sonoros', async ({ page }) => {
  await page.goto('/metodologia.html', { waitUntil: 'load' });
  await expect(page.getByText('No es un signo ibérico arqueológico.')).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Una fusión gráfica, no un signo antiguo.' })).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Dos funciones sonoras, dos alcances.' })).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Recreación experimental' })).toBeVisible();
  await expect(page.getByText('No es una reconstrucción de cómo hablaban los íberos.')).toBeVisible();
});

test('la voz experimental sintetiza los tokens de forma local y determinista', async ({ page }) => {
  await page.goto('/convertir.html', { waitUntil: 'load' });
  const summary = await page.evaluate(() => {
    const result = window.IberoMvp.convert('mundo');
    const first = window.IberoVoice.synthesize(result.words);
    const second = window.IberoVoice.synthesize(result.words);
    const plainS = window.IberoVoice.synthesize([{ tokens: ['s'] }]);
    const markedS = window.IberoVoice.synthesize([{ tokens: ['ś'] }]);
    const rms = Math.sqrt(
      first.samples.reduce((sum, value) => sum + value * value, 0) / first.samples.length
    );
    return {
      profileId: first.profileId,
      sampleRate: first.sampleRate,
      reading: first.reading,
      durationSeconds: first.durationSeconds,
      peak: first.peak,
      rms,
      deterministic:
        window.IberoVoice.fingerprint(first) === window.IberoVoice.fingerprint(second),
      distinctSibilants:
        window.IberoVoice.fingerprint(plainS) !== window.IberoVoice.fingerprint(markedS),
      itemCount: first.items.length
    };
  });
  expect(summary.profileId).toBe('iberolab-sign-reading-voice-v1');
  expect(summary.sampleRate).toBe(24000);
  expect(summary.reading).toBe('m · u · n · do');
  expect(summary.durationSeconds).toBeGreaterThan(0.7);
  expect(summary.durationSeconds).toBeLessThan(1.2);
  expect(summary.peak).toBeGreaterThan(0.7);
  expect(summary.rms).toBeGreaterThan(0.03);
  expect(summary.deterministic).toBe(true);
  expect(summary.distinctSibilants).toBe(true);
  expect(summary.itemCount).toBe(4);
});

test('la interfaz compara español moderno y recreación de signos sin confundirlos', async ({ page }) => {
  await page.addInitScript(() => {
    window.__iberoSpoken = null;
    class StubUtterance { constructor(text) { this.text = text; this.lang = ''; this.rate = 1; } }
    Object.defineProperty(window, 'SpeechSynthesisUtterance', { configurable: true, value: StubUtterance });
    Object.defineProperty(window, 'speechSynthesis', { configurable: true, value: { cancel() {}, speak(utterance) { window.__iberoSpoken = { text: utterance.text, lang: utterance.lang, rate: utterance.rate }; } } });
  });
  await page.goto('/convertir.html', { waitUntil: 'load' });
  await page.locator('#sourceInput').fill('mundo mundo');
  await page.getByRole('button', { name: 'Adaptar a signos ibéricos' }).click();
  await page.getByRole('button', { name: 'Escuchar entrada en español' }).click();
  expect(await page.evaluate(() => window.__iberoSpoken)).toEqual({ text: 'mundo mundo', lang: 'es-ES', rate: 0.9 });

  const recreation = page.getByRole('button', { name: 'Escuchar aproximación sonora' });
  await expect(recreation).toBeEnabled();
  await recreation.click();
  await expect(page.getByRole('button', { name: 'Detener aproximación' })).toHaveAttribute('aria-pressed', 'true');
  await expect(page.locator('#actionStatus')).toHaveText('Reproduciendo: m · u · n · do / m · u · n · do.');
  await page.getByRole('button', { name: 'Detener aproximación' }).click();
  await expect(recreation).toHaveAttribute('aria-pressed', 'false');
  await expect(page.locator('#actionStatus')).toHaveText('Recreación detenida.');

  await expect(page.getByRole('button', { name: 'Escuchar lectura aproximada' })).toHaveCount(0);
  await expect(page.getByText(/No reconstruye cómo hablaban los íberos/)).toBeVisible();
});
