const { test, expect } = require('@playwright/test');

test('la portada presenta la identidad pública y enlaza las tres áreas principales', async ({ page }) => {
  await page.goto('/', { waitUntil: 'load' });
  await expect(page.getByRole('heading', { name: 'IberoLab' })).toBeVisible();
  await expect(page.getByText('Lengua ibérica · Patrimonio · Tecnología')).toBeVisible();
  await expect(page.getByText('No es un signo ibérico antiguo.')).toBeVisible();
  await expect(page.locator('#corpus')).toBeVisible();
  await expect(page.getByRole('link', { name: 'Probar conversor' }).first()).toHaveAttribute('href', 'convertir.html');
  await expect(page.getByRole('link', { name: 'Explorar corpus' })).toHaveAttribute('href', 'corpus.html');
  await expect(page.getByRole('link', { name: 'Aprender historia' })).toHaveAttribute('href', 'historia.html');
});

test('un enlace histórico de la raíz conserva el identificador al abrir el corpus', async ({ page }) => {
  await page.goto('/#ib-ne-ildirda-001', { waitUntil: 'load' });
  await expect(page).toHaveURL(/corpus\.html#ib-ne-ildirda-001$/);
  await expect(page.locator('html')).toHaveAttribute('data-renderer-ready', 'true');
  await expect(page.locator('#readingText')).toHaveText('ildiŕda');
});

test('historia distingue lectura y traducción y anuncia la futura integración audiovisual', async ({ page }) => {
  await page.goto('/historia.html', { waitUntil: 'load' });
  await expect(page.getByRole('heading', { name: 'Comprender el mundo ibérico antes de intentar representarlo.' })).toBeVisible();
  await expect(page.getByText('Leer signos no significa traducir el idioma.')).toBeVisible();
  await expect(page.getByText('Una sección preparada para crecer con YouTube.')).toBeVisible();
});

test('metodología identifica el emblema como contemporáneo y explica los dos audios', async ({ page }) => {
  await page.goto('/metodologia.html', { waitUntil: 'load' });
  await expect(page.getByText('No es un signo ibérico arqueológico.')).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Dos audios con alcances distintos.' })).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Lectura aproximada' })).toBeVisible();
});

test('la lectura aproximada vocaliza la secuencia generada con una voz moderna', async ({ page }) => {
  await page.addInitScript(() => {
    window.__iberoSpoken = null;
    class StubUtterance {
      constructor(text) { this.text = text; this.lang = ''; this.rate = 1; }
    }
    Object.defineProperty(window, 'SpeechSynthesisUtterance', { configurable: true, value: StubUtterance });
    Object.defineProperty(window, 'speechSynthesis', {
      configurable: true,
      value: {
        cancel() {},
        speak(utterance) {
          window.__iberoSpoken = { text: utterance.text, lang: utterance.lang, rate: utterance.rate };
        }
      }
    });
  });
  await page.goto('/convertir.html', { waitUntil: 'load' });
  await page.locator('#sourceInput').fill('familia');
  await page.getByRole('button', { name: 'Adaptar a signos ibéricos' }).click();
  await page.getByRole('button', { name: 'Escuchar lectura aproximada' }).click();
  expect(await page.evaluate(() => window.__iberoSpoken)).toEqual({ text: 'bamilia', lang: 'es-ES', rate: 0.78 });
  await expect(page.getByText(/recurso didáctico y no una reconstrucción histórica/)).toBeVisible();
});
