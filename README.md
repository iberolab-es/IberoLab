# IberoLab

<p align="center"><img src="docs/assets/brand/iberolab-mark.svg" alt="Símbolo de IberoLab" width="112"></p>

**Proyecto abierto y experimental para representar fonéticamente nombres, palabras y frases breves mediante escrituras paleohispánicas.**

> Estado: **pre-alpha con demostrador MVP**. La web pública reconstruye un corpus inicial contrastado y ofrece una adaptación gráfica experimental para entradas modernas breves, pero todavía no ofrece un conversor formal validado ni traducciones a la lengua ibérica.

## Qué es

IberoLab separa tres capas que no deben confundirse:

1. **Corpus documental:** lecturas, segmentaciones y contextos de formas ibéricas ya atestiguadas.
2. **Demostrador práctico:** adaptación fonética experimental de nombres, palabras y frases españolas breves mediante reglas deterministas y advertencias visibles.
3. **Motor formal futuro:** arquitectura versionada para perfiles, reglas, costes, alternativas y confianza, todavía desactivada.

La intención práctica es modesta: que una persona pueda escribir algo como `hogar`, `tierra`, `mundo`, `olivo` o `mar` y obtener una representación gráfica razonada, sin fingir una traducción que el conocimiento actual no permite. También puede introducir nombres, sentimientos o frases breves de su elección.

## Qué no es

IberoLab **no ofrece traducciones literales a la lengua ibérica**. La lengua ibérica no está descifrada hasta un grado que permita traducir de forma completa y consensuada textos modernos.

El demostrador MVP produce una **adaptación fonética experimental**. No atribuye significado ibérico a la salida, no reconstruye vocabulario antiguo y no presenta los signos normalizados como facsímiles de una inscripción concreta.

## Estado verificable actual

### Corpus atestiguado

- once formas documentadas en bibliografía epigráfica o numismática;
- diecinueve tokens derivados exclusivamente de ese corpus;
- diecinueve SVG locales con procedencia, licencia, tamaño y SHA-256 registrados;
- resolución explícita de `ń` mediante la variante paleográfica `m1`, conservando `m` como transcripción histórica;
- cero tokens gráficos pendientes en el corpus inicial;
- renderizador, navegación, lectura técnica, fuentes y enlaces profundos;
- recreación sonora opcional de las lecturas atestiguadas, separada de la evidencia escrita y rotulada como experimento moderno;
- regresión automática sobre Chromium, Firefox y WebKit.

### Demostrador MVP

- biblioteca gráfica independiente con los 38 signos normalizados de la serie nororiental dual;
- entradas limitadas a 48 caracteres y 6 palabras;
- pruebas contractuales para salidas directas, aproximaciones y frases de varias palabras;
- representación directa de vocales y continuantes;
- uso de silabogramas para las oclusivas;
- advertencias obligatorias para vocales de apoyo y sonidos modernos sin equivalente directo;
- bloqueo explícito ante símbolos no admitidos;
- prohibición de salidas vacías y sustituciones silenciosas;
- audio opcional para comparar la entrada española mediante la voz del navegador;
- voz fluida moderna mediante una ortografía puente y la voz disponible en el dispositivo, con preferencia por el euskera explicada como ajuste articulatorio y no como parentesco;
- síntesis técnica local y determinista preservada mediante `iberolab-sign-reading-voice-v1`;
- perfil vigente `iberolab-sign-reading-voice-v3`, que distingue formas atestiguadas de adaptaciones españolas modernas y amplía la cobertura sonora al token corpus `ń`;
- perfil fluido anterior `iberolab-sign-reading-voice-v2` preservado;
- separación explícita entre valores convencionales, hipótesis acústicas y decisiones de síntesis sin valor histórico.

### Motor formal

- contrato machine-readable en estado `specification_only`;
- perfiles de pronunciación, reglas lingüísticas, pesos y confianza calibrada sin aprobar;
- estados `success` y `blocked` definidos de forma mutuamente excluyente;
- conversión formal pública desactivada.

## Acceso público

- Demostrador de entradas breves: <https://iberolab-es.github.io/IberoLab/convertir.html>
- Corpus y renderizador documentado: <https://iberolab-es.github.io/IberoLab/>
- Información para universidades y especialistas: <https://iberolab-es.github.io/IberoLab/academia.html>
- Diagnóstico de corpus y SVG: <https://iberolab-es.github.io/IberoLab/test.html>
- Diagnóstico de enlaces profundos: <https://iberolab-es.github.io/IberoLab/deep-link-test.html>

## Convenciones del MVP

El demostrador utiliza una pronunciación española cuidada como **convención operativa del proyecto**, no como pronunciación universal de España. Las decisiones discutibles se explican en pantalla.

Entre otras:

- `b` y `p` comparten la serie labial ibérica y la pérdida del contraste se advierte;
- `r` y `ŕ` se emplean como convención gráfica para la vibrante simple y múltiple, sin afirmar identidad fonética histórica;
- `f`, `ñ`, `ch`, `y/ll`, la fricativa de `j` y el sonido de `z/c` requieren aproximaciones visibles;
- una oclusiva dentro de un grupo consonántico puede necesitar una vocal de apoyo declarada.

## Principios

- Rigor terminológico y transparencia sobre los límites del conocimiento.
- Separación entre corpus atestiguado, demostración práctica y motor formal.
- Trazabilidad de cada signo, variante, transcripción y recurso gráfico.
- Ausencia de traducciones, significados o pronunciaciones antiguas inventadas.
- Toda recreación sonora se identifica como experimento moderno y nunca como pronunciación auténtica o reconstrucción histórica.
- Ausencia de sustituciones silenciosas.
- Funcionamiento local en el navegador sin depender de SVG remotos.
- Pruebas reproducibles antes de etiquetar una versión estable.

## Estructura actual

```text
.github/     Plantillas, gobernanza y GitHub Actions de solo lectura

data/        Corpus, inventarios, manifiestos, contratos y esquemas

docs/        Web pública, demostrador, diagnósticos y metodología

scripts/     Validadores y utilidades reproducibles

tests/       Regresión automatizada de navegador
```

La especificación estructural del motor ya existe, pero no contiene reglas lingüísticas formalmente aprobadas. El demostrador MVP es una capa deliberadamente menor y auditable. Los futuros módulos de adaptación fonética formal seguirán las puertas de [PHONETIC_ENGINE_SPEC.md](docs/PHONETIC_ENGINE_SPEC.md); las dimensiones españolas se documentan en [SPANISH_PRONUNCIATION_PROFILES.md](docs/SPANISH_PRONUNCIATION_PROFILES.md).

## Validación local

```bash
python scripts/validate_corpus.py
python scripts/validate_source_audit.py
python scripts/validate_local_assets.py
python scripts/validate_renderer.py
python scripts/validate_browser_matrix.py
python scripts/validate_project_state.py
python scripts/validate_engine_spec.py
python scripts/validate_engine_schema_registry.py
python scripts/validate_pronunciation_profiles.py
python scripts/validate_mvp_converter.py
python scripts/validate_experimental_voice.py
python scripts/validate_public_presence.py
```

La regresión de navegador se ejecuta con Playwright según `playwright.config.cjs` y `.github/workflows/browser-smoke.yml`.

## Participar

Las sugerencias y errores se gestionan mediante [GitHub Issues](https://github.com/iberolab-es/IberoLab/issues/new/choose). Antes de contribuir, consulta [CONTRIBUTING.md](CONTRIBUTING.md), la [metodología](docs/METHODOLOGY.md), la [especificación del motor](docs/PHONETIC_ENGINE_SPEC.md), los [perfiles de pronunciación](docs/SPANISH_PRONUNCIATION_PROFILES.md), la [procedencia de los recursos](docs/ASSET_PROVENANCE.md) y el [plan de difusión](OUTREACH.md).

## Hoja de ruta

Consulta [ROADMAP.md](ROADMAP.md). El seguimiento detallado se concentra actualmente en:

- [fase 1 y base paleográfica](https://github.com/iberolab-es/IberoLab/issues/2);
- [pruebas multidispositivo](https://github.com/iberolab-es/IberoLab/issues/6);
- [demostrador MVP y especificación del motor moderno](https://github.com/iberolab-es/IberoLab/issues/3).

## Licencia

Código y documentación publicados bajo [Apache License 2.0](LICENSE), salvo que un recurso concreto indique otra licencia. Los recursos gráficos de terceros conservan su propia atribución y licencia en los manifiestos y en `NOTICE`.

---

### English summary

IberoLab is an open experimental project for representing short modern Spanish names, words and phrases with normalized ancient Iberian signs. A public MVP demonstrator uses deterministic, explained conventions and a separate 38-sign graphic layer. It is not a translation into the undeciphered Iberian language. The attested research corpus remains separate, and the formal phonetic engine, pronunciation profiles, calibrated confidence and reviewed rule system remain disabled.
