#!/usr/bin/env python3
"""Apply the public identity, history navigation and approximate-reading audio iteration."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace(path: str, old: str, new: str, expected: int = 1) -> None:
    target = ROOT / path
    text = target.read_text(encoding="utf-8")
    count = text.count(old)
    if count != expected:
        raise RuntimeError(f"{path}: expected {expected} occurrence(s), found {count}: {old!r}")
    target.write_text(text.replace(old, new), encoding="utf-8")


# Public home: preserve the corpus renderer while turning the root into a real landing page.
replace(
    "docs/index.html",
    '<meta name="description" content="Corpus inicial de formas ibéricas documentadas y representación gráfica normalizada de referencia.">',
    '<meta name="description" content="IberoLab: corpus documentado, adaptación gráfica experimental y divulgación sobre lengua ibérica.">',
)
replace("docs/index.html", "<title>IberoLab — Corpus ibérico contrastado</title>", "<title>IberoLab — Lengua ibérica, patrimonio y tecnología</title>")
replace("docs/index.html", "  <style>", '  <link rel="stylesheet" href="public-site.css">\n  <style>', 1)
replace(
    "docs/index.html",
    "<body>\n<main>",
    '''<body>
<nav class="site-nav" aria-label="Navegación principal">
  <div class="site-nav-inner">
    <a class="brand-link" href="./"><img src="assets/brand/iberolab-emblem.svg" alt=""><span class="brand-word">Ibero<span>Lab</span></span></a>
    <div class="site-links">
      <a href="#corpus">Corpus</a>
      <a href="historia.html">Historia</a>
      <a href="metodologia.html">Metodología</a>
      <a class="nav-cta" href="convertir.html">Probar conversor</a>
    </div>
  </div>
</nav>
<main class="home-main">''',
)
replace(
    "docs/index.html",
    '''  <header>
    <div class="eyebrow">IberoLab · pre-alpha</div>
    <h1>Formas ibéricas contrastadas</h1>
    <p class="lead">Esta página conserva el corpus documentado y su evidencia. Para nombres, palabras y frases modernas breves existe un demostrador separado, siempre etiquetado como adaptación fonética experimental.</p>
  </header>''',
    '''  <header id="inicio" class="home-hero">
    <div>
      <div class="hero-kicker">Lengua ibérica · Patrimonio · Tecnología</div>
      <h1 class="hero-title">Ibero<span>Lab</span></h1>
      <div class="hero-tagline">Explorar, representar y divulgar con límites explícitos.</div>
      <p class="hero-copy">IberoLab combina un corpus atestiguado, signos normalizados y herramientas abiertas para acercar la escritura ibérica al público. El proyecto distingue siempre entre evidencia histórica y adaptación experimental moderna.</p>
      <div class="cta-row">
        <a class="cta-link gold" href="convertir.html">Probar conversor</a>
        <a class="cta-link outline" href="#corpus">Explorar corpus</a>
        <a class="cta-link outline" href="historia.html">Aprender historia</a>
      </div>
    </div>
    <div class="hero-visual" aria-label="Identidad visual y signos de referencia">
      <img class="hero-emblem" src="assets/brand/iberolab-emblem.svg" alt="Emblema contemporáneo de IberoLab">
      <div class="hero-tablet">
        <div class="tablet-label">Lectura documentada · ildiŕda</div>
        <div class="tablet-signs" aria-hidden="true">
          <img src="assets/signs/northeastern-dual/dual-03-i.svg" alt="">
          <img src="assets/signs/northeastern-dual/dual-35-l.svg" alt="">
          <img src="assets/signs/northeastern-dual/dual-23-di.svg" alt="">
          <img src="assets/signs/northeastern-dual/dual-34-r2.svg" alt="">
          <img src="assets/signs/northeastern-dual/dual-21-da.svg" alt="">
        </div>
      </div>
    </div>
  </header>

  <section class="section-block" aria-labelledby="pillarsTitle">
    <div class="section-kicker">Qué es IberoLab</div>
    <h2 id="pillarsTitle" class="section-title">Un proyecto abierto para acercar la escritura ibérica.</h2>
    <p class="section-lead">La utilidad práctica no debe borrar la incertidumbre histórica. Por eso el corpus, el conversor y la divulgación mantienen alcances diferenciados y verificables.</p>
    <div class="feature-grid">
      <article class="feature-card"><div class="feature-icon">01</div><h3>Basado en evidencia</h3><p>Formas documentadas con contexto, segmentación y fuente.</p></article>
      <article class="feature-card"><div class="feature-icon">02</div><h3>Rigor y transparencia</h3><p>Las aproximaciones se explican y los límites permanecen visibles.</p></article>
      <article class="feature-card"><div class="feature-icon">03</div><h3>Tecnología abierta</h3><p>Código, datos, recursos y validaciones publicados en GitHub.</p></article>
      <article class="feature-card"><div class="feature-icon">04</div><h3>Para todos</h3><p>Una experiencia visual y didáctica sin fingir certezas.</p></article>
    </div>
  </section>''',
)
replace(
    "docs/index.html",
    '<section class="panel" aria-labelledby="rendererTitle">',
    '<section id="corpus" class="panel" aria-labelledby="rendererTitle">',
)
replace(
    "docs/index.html",
    "  </section>\n\n  <footer>",
    '''  </section>

  <section class="section-block gold-edge" aria-labelledby="historyHomeTitle">
    <div class="split-grid">
      <div>
        <div class="section-kicker">Historia y contexto</div>
        <h2 id="historyHomeTitle" class="section-title">La escritura se entiende mejor cuando conocemos su mundo.</h2>
        <p class="section-lead">La nueva sección didáctica explica quiénes fueron los íberos, qué testimonios conservamos, qué podemos leer y por qué todavía no podemos traducir plenamente su lengua.</p>
        <div class="cta-row"><a class="cta-link gold" href="historia.html">Explorar historia</a><a class="cta-link outline" href="metodologia.html">Conocer metodología</a></div>
      </div>
      <div class="video-card"><span>Próxima línea editorial</span><h3>Historia enlazada con YouTube</h3><p>Vídeos, textos, fuentes y materiales complementarios convivirán en una misma sección didáctica.</p></div>
    </div>
  </section>

  <section class="section-block" aria-labelledby="logoTitle">
    <div class="logo-story">
      <img src="assets/brand/iberolab-emblem.svg" alt="Emblema contemporáneo de IberoLab">
      <div>
        <div class="section-kicker">Identidad del proyecto</div>
        <h2 id="logoTitle" class="section-title">Un signo-raíz contemporáneo.</h2>
        <p class="section-lead">El eje central representa memoria y continuidad; las ramas, transmisión y expansión del conocimiento; el círculo, preservación y unidad; el punto lateral, fuente y testimonio humano.</p>
        <p class="logo-disclaimer"><strong>No es un signo ibérico antiguo.</strong> Es un emblema moderno creado para identificar IberoLab.</p>
      </div>
    </div>
  </section>

  <section class="section-block gold-edge" aria-labelledby="communityTitle">
    <div class="section-kicker">Proyecto abierto</div>
    <h2 id="communityTitle" class="section-title">Para la comunidad académica y para cualquier persona curiosa.</h2>
    <p class="section-lead">Especialistas en lingüística, epigrafía, arqueología, filología y tecnologías del lenguaje pueden revisar el proyecto. Quien se acerca por primera vez también encontrará una entrada sencilla y honesta.</p>
    <div class="cta-row"><a class="cta-link gold" href="https://github.com/iberolab-es/IberoLab">Participar en GitHub</a><a class="cta-link outline" href="https://github.com/iberolab-es/IberoLab/issues/new/choose">Enviar aportación</a></div>
  </section>

  <footer>''',
    1,
)

# Converter navigation and a clearly labelled modern vocalisation of the generated token sequence.
replace("docs/convertir.html", "  <style>", '  <link rel="stylesheet" href="public-site.css">\n  <style>', 1)
replace(
    "docs/convertir.html",
    "<body>\n<main>",
    '''<body>
<nav class="site-nav" aria-label="Navegación principal">
  <div class="site-nav-inner">
    <a class="brand-link" href="./"><img src="assets/brand/iberolab-emblem.svg" alt=""><span class="brand-word">Ibero<span>Lab</span></span></a>
    <div class="site-links"><a href="./#corpus">Corpus</a><a href="historia.html">Historia</a><a href="metodologia.html">Metodología</a><a class="nav-cta" href="convertir.html" aria-current="page">Conversor</a></div>
  </div>
</nav>
<main>''',
)
replace(
    "docs/convertir.html",
    '        <button id="speakButton" class="secondary" type="button">Escuchar entrada en español</button>\n        <button id="copyButton" class="secondary" type="button">Copiar lectura técnica</button>',
    '        <button id="speakButton" class="secondary" type="button">Escuchar entrada en español</button>\n        <button id="approximateButton" class="secondary" type="button">Escuchar lectura aproximada</button>\n        <button id="copyButton" class="secondary" type="button">Copiar lectura técnica</button>',
)
replace(
    "docs/convertir.html",
    '<strong>Sobre la pronunciación:</strong> el audio reproduce la entrada española mediante la voz disponible en tu navegador. No intenta reconstruir cómo habría pronunciado esta secuencia una persona ibérica de la Antigüedad.',
    '<strong>Sobre la pronunciación:</strong> «Escuchar entrada» reproduce el español original. «Escuchar lectura aproximada» vocaliza con una voz española moderna la secuencia de signos generada; es un recurso didáctico y no una reconstrucción histórica de la pronunciación ibérica.',
)
replace(
    "docs/convertir.html",
    '¿Has detectado una adaptación mejorable? <a href="https://github.com/iberolab-es/IberoLab/issues/new/choose" target="_blank" rel="noopener noreferrer">Enviar una sugerencia</a>.',
    '¿Has detectado una adaptación mejorable? <a href="https://github.com/iberolab-es/IberoLab/issues/new/choose" target="_blank" rel="noopener noreferrer">Enviar una sugerencia</a>. <a href="historia.html">Historia y contexto</a>.',
)
replace(
    "docs/convertir.html",
    '  const speakButton = document.getElementById("speakButton");\n  const copyButton = document.getElementById("copyButton");',
    '  const speakButton = document.getElementById("speakButton");\n  const approximateButton = document.getElementById("approximateButton");\n  const copyButton = document.getElementById("copyButton");',
)
replace(
    "docs/convertir.html",
    '      speakButton.disabled = true;\n      copyButton.disabled = true;',
    '      speakButton.disabled = true;\n      approximateButton.disabled = true;\n      copyButton.disabled = true;',
)
replace(
    "docs/convertir.html",
    '    speakButton.disabled = !("speechSynthesis" in window);\n    copyButton.disabled = false;',
    '    speakButton.disabled = !("speechSynthesis" in window);\n    approximateButton.disabled = !("speechSynthesis" in window);\n    copyButton.disabled = false;',
)
replace(
    "docs/convertir.html",
    '''  speakButton.addEventListener("click", () => {
    if (!currentResult || currentResult.executionStatus !== "success" || !("speechSynthesis" in window)) return;
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(currentResult.original);
    utterance.lang = "es-ES";
    utterance.rate = 0.9;
    window.speechSynthesis.speak(utterance);
  });''',
    '''  speakButton.addEventListener("click", () => {
    if (!currentResult || currentResult.executionStatus !== "success" || !("speechSynthesis" in window)) return;
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(currentResult.original);
    utterance.lang = "es-ES";
    utterance.rate = 0.9;
    window.speechSynthesis.speak(utterance);
  });

  function experimentalReadingText(result) {
    const modernLabels = { "ŕ": "r", "ś": "s", "ń": "n" };
    return result.words
      .map(word => word.tokens.map(token => modernLabels[token] || token).join(""))
      .join(" ");
  }

  approximateButton.addEventListener("click", () => {
    if (!currentResult || currentResult.executionStatus !== "success" || !("speechSynthesis" in window)) return;
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(experimentalReadingText(currentResult));
    utterance.lang = "es-ES";
    utterance.rate = 0.78;
    window.speechSynthesis.speak(utterance);
    actionStatus.textContent = "Reproduciendo una lectura moderna aproximada de los signos.";
    setTimeout(() => { actionStatus.textContent = ""; }, 2200);
  });''',
)

# Static validation markers for the converter.
validator = ROOT / "scripts" / "validate_mvp_converter.py"
text = validator.read_text(encoding="utf-8")
anchor = '        "Escuchar entrada en español",\n'
if anchor not in text:
    raise RuntimeError("converter validator anchor not found")
text = text.replace(anchor, anchor + '        "Escuchar lectura aproximada",\n        "experimentalReadingText",\n        "recurso didáctico y no una reconstrucción histórica",\n', 1)
validator.write_text(text, encoding="utf-8")

# Public-site validator in the standard read-only CI.
replace(
    ".github/workflows/validate.yml",
    '      - name: Validate practical short-input MVP converter\n        run: python scripts/validate_mvp_converter.py',
    '      - name: Validate practical short-input MVP converter\n        run: python scripts/validate_mvp_converter.py\n\n      - name: Validate public identity, history and methodology\n        run: python scripts/validate_public_site.py',
)

# Browser regression for the public layer and the approximate-reading button.
tests = ROOT / "tests" / "browser" / "browser-smoke.spec.cjs"
text = tests.read_text(encoding="utf-8")
anchor = "test.describe('renderizador local por enlaces profundos', () => {"
if anchor not in text:
    raise RuntimeError("browser public-page insertion anchor not found")
public_tests = '''test('la portada pública enlaza conversor, historia y corpus sin ocultar los límites', async ({ page }) => {
  await page.goto('/', { waitUntil: 'load' });
  await expect(page.getByRole('heading', { name: 'IberoLab' })).toBeVisible();
  await expect(page.getByText('Lengua ibérica · Patrimonio · Tecnología')).toBeVisible();
  await expect(page.getByText('No es un signo ibérico antiguo')).toBeVisible();
  await expect(page.locator('#corpus')).toBeVisible();
  await expect(page.getByRole('link', { name: 'Aprender historia' })).toHaveAttribute('href', 'historia.html');
});

test('la página de historia mantiene la distinción entre lectura y traducción', async ({ page }) => {
  await page.goto('/historia.html', { waitUntil: 'load' });
  await expect(page.getByRole('heading', { name: /Historia y contexto del mundo ibérico/ })).toBeVisible();
  await expect(page.getByText('Leer signos no significa traducir el idioma.')).toBeVisible();
  await expect(page.getByText('Una sección preparada para crecer con YouTube.')).toBeVisible();
});

'''
text = text.replace(anchor, public_tests + anchor, 1)
audio_anchor = "  test('una entrada no admitida se bloquea sin signos parciales', async ({ page }) => {"
if audio_anchor not in text:
    raise RuntimeError("browser audio insertion anchor not found")
audio_test = '''  test('la lectura aproximada vocaliza la secuencia generada y no la etiqueta como ibero auténtico', async ({ page }) => {
    await page.addInitScript(() => {
      window.__iberoSpoken = null;
      class StubUtterance { constructor(text) { this.text = text; } }
      Object.defineProperty(window, 'SpeechSynthesisUtterance', { configurable: true, value: StubUtterance });
      Object.defineProperty(window, 'speechSynthesis', {
        configurable: true,
        value: { cancel() {}, speak(utterance) { window.__iberoSpoken = { text: utterance.text, lang: utterance.lang, rate: utterance.rate }; } }
      });
    });
    await page.goto('/convertir.html', { waitUntil: 'load' });
    await page.locator('#sourceInput').fill('familia');
    await page.getByRole('button', { name: 'Adaptar a signos ibéricos' }).click();
    await page.getByRole('button', { name: 'Escuchar lectura aproximada' }).click();
    const spoken = await page.evaluate(() => window.__iberoSpoken);
    expect(spoken).toEqual({ text: 'bamilia', lang: 'es-ES', rate: 0.78 });
    await expect(page.getByText(/recurso didáctico y no una reconstrucción histórica/)).toBeVisible();
  });

'''
text = text.replace(audio_anchor, audio_test + audio_anchor, 1)
tests.write_text(text, encoding="utf-8")

# Changelog.
changelog = ROOT / "CHANGELOG.md"
text = changelog.read_text(encoding="utf-8")
entry = '''## Unreleased — identidad pública, historia y audio aproximado

- La raíz del sitio se convierte en una portada visual sin retirar el corpus documentado.
- Se incorpora un emblema contemporáneo con significado y advertencia de que no es un signo arqueológico.
- Se publican páginas de Historia y Metodología preparadas para futuros contenidos de YouTube.
- El conversor añade una lectura vocal aproximada de la secuencia generada, etiquetada como recurso didáctico moderno.
- Se añaden validación estática y regresión de navegador para la nueva capa pública.

'''
marker = "## "
index = text.find(marker)
text = entry + text if index < 0 else text[:index] + entry + text[index:]
changelog.write_text(text, encoding="utf-8")

# Align the history heading with its navigation and validation label.
replace(
    "docs/historia.html",
    "<h1>Comprender el mundo ibérico antes de intentar representarlo.</h1>",
    "<h1>Historia y contexto del mundo ibérico.</h1>",
)

print("Public identity, history pages and approximate-reading audio applied.")
