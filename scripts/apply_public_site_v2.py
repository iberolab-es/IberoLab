#!/usr/bin/env python3
"""Integrate the public landing, history navigation and approximate-reading audio over current main."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace(path: str, old: str, new: str, expected: int = 1) -> None:
    target = ROOT / path
    text = target.read_text(encoding="utf-8")
    count = text.count(old)
    if count != expected:
        raise RuntimeError(f"{path}: expected {expected}, found {count}: {old!r}")
    target.write_text(text.replace(old, new), encoding="utf-8")


# Home metadata and shared public styles.
replace("docs/index.html", '<meta name="description" content="Corpus inicial de formas ibéricas documentadas y representación gráfica normalizada de referencia.">', '<meta name="description" content="IberoLab: corpus documentado, adaptación gráfica experimental y divulgación sobre lengua ibérica.">')
replace("docs/index.html", '<meta property="og:title" content="IberoLab · Corpus ibérico documentado">', '<meta property="og:title" content="IberoLab · Lengua ibérica, patrimonio y tecnología">')
replace("docs/index.html", '<title>IberoLab — Corpus ibérico contrastado</title>\n  <style>', '<title>IberoLab — Lengua ibérica, patrimonio y tecnología</title>\n  <link rel="stylesheet" href="public-site.css">\n  <style>')
replace(
    "docs/index.html",
    '''    <nav class="site-nav" aria-label="Navegación principal">
      <a href="convertir.html">Demostrador</a>
      <a href="./">Corpus</a>
      <a href="academia.html">Universidades</a>
      <a href="https://github.com/iberolab-es/IberoLab">GitHub</a>
    </nav>''',
    '''    <nav class="site-nav" aria-label="Navegación principal">
      <a href="#corpus">Corpus</a>
      <a href="historia.html">Historia</a>
      <a href="metodologia.html">Metodología</a>
      <a href="academia.html">Universidades</a>
      <a href="convertir.html">Conversor</a>
      <a href="https://github.com/iberolab-es/IberoLab">GitHub</a>
    </nav>''',
)
replace(
    "docs/index.html",
    '''  <header>
    <div class="eyebrow">IberoLab · pre-alpha</div>
    <h1>Formas ibéricas contrastadas</h1>
    <p class="lead">Esta página conserva el corpus documentado y su evidencia. Para nombres, palabras y frases modernas breves existe un demostrador separado, siempre etiquetado como adaptación fonética experimental.</p>
  </header>''',
    '''  <header class="home-hero">
    <div>
      <div class="hero-kicker">Lengua ibérica · Patrimonio · Tecnología</div>
      <h1 class="hero-title">Ibero<span>Lab</span></h1>
      <div class="hero-tagline">Explorar, representar y divulgar con límites explícitos.</div>
      <p class="hero-copy">IberoLab combina un corpus atestiguado, signos normalizados y herramientas abiertas para acercar la escritura ibérica al público. El proyecto distingue siempre entre evidencia histórica y adaptación experimental moderna.</p>
      <div class="cta-row"><a class="cta-link gold" href="convertir.html">Probar conversor</a><a class="cta-link outline" href="#corpus">Explorar corpus</a><a class="cta-link outline" href="historia.html">Aprender historia</a></div>
    </div>
    <div class="hero-visual">
      <img class="hero-mark" src="assets/brand/iberolab-mark.svg" alt="Símbolo contemporáneo de IberoLab">
      <div class="hero-tablet"><div class="tablet-label">Lectura documentada · ildiŕda</div><div class="tablet-signs" aria-hidden="true"><img src="assets/signs/northeastern-dual/dual-03-i.svg" alt=""><img src="assets/signs/northeastern-dual/dual-35-l.svg" alt=""><img src="assets/signs/northeastern-dual/dual-23-di.svg" alt=""><img src="assets/signs/northeastern-dual/dual-34-r2.svg" alt=""><img src="assets/signs/northeastern-dual/dual-21-da.svg" alt=""></div></div>
    </div>
  </header>

  <section class="section-block" aria-labelledby="pillarsTitle">
    <div class="section-kicker">Qué es IberoLab</div><h2 id="pillarsTitle" class="section-title">Un proyecto abierto para acercar la escritura ibérica.</h2><p class="section-lead">La utilidad práctica no debe borrar la incertidumbre histórica. Corpus, conversor y divulgación mantienen alcances diferenciados y verificables.</p>
    <div class="feature-grid"><article class="feature-card"><div class="feature-icon">01</div><h3>Basado en evidencia</h3><p>Formas documentadas con contexto, segmentación y fuente.</p></article><article class="feature-card"><div class="feature-icon">02</div><h3>Rigor y transparencia</h3><p>Las aproximaciones se explican y los límites permanecen visibles.</p></article><article class="feature-card"><div class="feature-icon">03</div><h3>Tecnología abierta</h3><p>Código, datos, citación y validaciones publicados.</p></article><article class="feature-card"><div class="feature-icon">04</div><h3>Para todos</h3><p>Una experiencia visual y didáctica sin fingir certezas.</p></article></div>
  </section>''',
)
replace("docs/index.html", '<section class="panel" aria-labelledby="rendererTitle">', '<section id="corpus" class="panel" aria-labelledby="rendererTitle">')
replace(
    "docs/index.html",
    '  </section>\n\n  <footer>',
    '''  </section>

  <section class="section-block gold-edge"><div class="split-grid"><div><div class="section-kicker">Historia y contexto</div><h2 class="section-title">La escritura se entiende mejor cuando conocemos su mundo.</h2><p class="section-lead">La sección didáctica explica quiénes fueron los íberos, qué testimonios conservamos, qué podemos leer y por qué todavía no podemos traducir plenamente su lengua.</p><div class="cta-row"><a class="cta-link gold" href="historia.html">Explorar historia</a><a class="cta-link outline" href="metodologia.html">Conocer metodología</a></div></div><div class="video-card"><span>Próxima línea editorial</span><h3>Historia enlazada con YouTube</h3><p>Vídeos, textos, fuentes y materiales complementarios convivirán en una misma sección didáctica.</p></div></div></section>

  <section class="section-block"><div class="logo-story"><img src="assets/brand/iberolab-mark.svg" alt="Símbolo contemporáneo de IberoLab"><div><div class="section-kicker">Identidad del proyecto</div><h2 class="section-title">Un signo-raíz contemporáneo.</h2><p class="section-lead">El eje central representa memoria y continuidad; las ramas, transmisión y expansión del conocimiento; el círculo, preservación y unidad; los puntos laterales, fuentes y testimonios humanos.</p><p class="logo-disclaimer"><strong>No es un signo ibérico antiguo.</strong> Es una marca contemporánea inspirada en la lógica visual paleohispánica.</p></div></div></section>

  <section class="section-block gold-edge"><div class="section-kicker">Proyecto abierto</div><h2 class="section-title">Para la comunidad académica y para cualquier persona curiosa.</h2><p class="section-lead">La página académica, la citación, la privacidad, los datos y el código permanecen abiertos a revisión.</p><div class="cta-row"><a class="cta-link gold" href="academia.html">Información para universidades</a><a class="cta-link outline" href="https://github.com/iberolab-es/IberoLab">Participar en GitHub</a><a class="cta-link outline" href="privacidad.html">Privacidad</a></div></section>

  <footer>''',
    1,
)

# Converter navigation, shared styling and approximate audio.
replace("docs/convertir.html", '<title>IberoLab — Conversor breve experimental</title>\n  <style>', '<title>IberoLab — Conversor breve experimental</title>\n  <link rel="stylesheet" href="public-site.css">\n  <style>')
replace(
    "docs/convertir.html",
    '''    <nav class="site-nav" aria-label="Navegación principal">
      <a href="convertir.html">Demostrador</a>
      <a href="./">Corpus</a>
      <a href="academia.html">Universidades</a>
      <a href="https://github.com/iberolab-es/IberoLab">GitHub</a>
    </nav>''',
    '''    <nav class="site-nav" aria-label="Navegación principal">
      <a href="convertir.html">Conversor</a>
      <a href="./#corpus">Corpus</a>
      <a href="historia.html">Historia</a>
      <a href="metodologia.html">Metodología</a>
      <a href="academia.html">Universidades</a>
      <a href="https://github.com/iberolab-es/IberoLab">GitHub</a>
    </nav>''',
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
    '  const speakButton = document.getElementById("speakButton");\n  const copyButton = document.getElementById("copyButton");',
    '  const speakButton = document.getElementById("speakButton");\n  const approximateButton = document.getElementById("approximateButton");\n  const copyButton = document.getElementById("copyButton");',
)
replace("docs/convertir.html", '      speakButton.disabled = true;\n      copyButton.disabled = true;', '      speakButton.disabled = true;\n      approximateButton.disabled = true;\n      copyButton.disabled = true;')
replace("docs/convertir.html", '    speakButton.disabled = !("speechSynthesis" in window);\n    copyButton.disabled = false;', '    speakButton.disabled = !("speechSynthesis" in window);\n    approximateButton.disabled = !("speechSynthesis" in window);\n    copyButton.disabled = false;')
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
    return result.words.map(word => word.tokens.map(token => modernLabels[token] || token).join("")).join(" ");
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

# Validator marker additions.
validator = ROOT / "scripts" / "validate_mvp_converter.py"
text = validator.read_text(encoding="utf-8")
anchor = '        "Escuchar entrada en español",\n'
if anchor not in text:
    raise RuntimeError("MVP validator anchor missing")
text = text.replace(anchor, anchor + '        "Escuchar lectura aproximada",\n        "experimentalReadingText",\n        "recurso didáctico y no una reconstrucción histórica",\n', 1)
validator.write_text(text, encoding="utf-8")

# CI keeps both the existing academic-presence validation and the new public-site validation.
replace(
    ".github/workflows/validate.yml",
    '      - name: Validate public identity and academic presence\n        run: python scripts/validate_public_presence.py',
    '      - name: Validate public identity and academic presence\n        run: python scripts/validate_public_presence.py\n\n      - name: Validate public landing, history and approximate audio\n        run: python scripts/validate_public_site.py',
)

# Changelog: insert a focused section without removing the concurrent identity work.
changelog = ROOT / "CHANGELOG.md"
text = changelog.read_text(encoding="utf-8")
marker = "## Unreleased — historial local privado"
entry = '''## Unreleased — portada, historia y lectura aproximada

- La raíz incorpora una presentación visual inspirada en el diseño aprobado sin retirar el corpus ni romper sus enlaces profundos.
- Se publican páginas de Historia y Metodología enlazadas con la presencia académica existente.
- El símbolo oficial recibe una explicación pública y se identifica como marca contemporánea, no como signo arqueológico.
- El conversor añade una lectura vocal moderna de la secuencia generada, etiquetada como aproximación didáctica.
- La regresión automática comprueba portada, historia, metodología y audio en Chromium, Firefox y WebKit.

'''
if marker not in text:
    raise RuntimeError("CHANGELOG insertion marker missing")
changelog.write_text(text.replace(marker, entry + marker, 1), encoding="utf-8")

print("Public site v2 applied over current main identity infrastructure.")
