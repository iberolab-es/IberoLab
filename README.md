# IberoLab

**Proyecto abierto y experimental para estudiar la representación fonética de lenguas modernas mediante escrituras paleohispánicas.**

> Estado: **pre-alpha / fase de fundamentación**. La web pública reconstruye un corpus inicial contrastado, pero todavía no ofrece un conversor de palabras modernas ni un traductor al idioma ibérico.

## Qué es

IberoLab separa dos líneas de trabajo que no deben confundirse:

1. **Base documental y gráfica:** lectura, segmentación, contexto y representación controlada de formas ya atestiguadas.
2. **Adaptación moderna futura:** representación fonética experimental de entradas actuales mediante reglas explicables y versionadas.

El proyecto distingue siempre entre lectura, interpretación semántica, adaptación fonética y renderizado gráfico.

## Qué no es

IberoLab **no traduce literalmente al idioma ibérico**. La lengua ibérica no está descifrada hasta un grado que permita traducir de forma completa y consensuada textos modernos. Cualquier salida futura deberá identificarse con precisión como:

- transliteración;
- representación fonética experimental;
- reconstrucción hipotética;
- recreación artística.

## Estado verificable actual

La pre-alpha dispone de:

- once formas documentadas en bibliografía epigráfica o numismática;
- diecinueve tokens de transcripción derivados exclusivamente de ese corpus;
- diecinueve SVG locales con procedencia, licencia, tamaño y SHA-256 registrados;
- resolución explícita de `ń` mediante la variante paleográfica `m1`, conservando `m` como transcripción histórica;
- cero tokens gráficos pendientes en el corpus inicial;
- renderizador público con navegación, lectura técnica, fuentes y enlaces profundos;
- diagnóstico público de carga del corpus y los SVG;
- diagnóstico público de los once enlaces profundos;
- validaciones automáticas del corpus, las fuentes, los recursos gráficos y la matriz de navegadores;
- regresión automática sobre Chromium, Firefox y WebKit.

Continúan pendientes las pruebas manuales de la implementación actual en Safari/iOS y en navegadores de ordenador, la selección progresiva de alógrafos específicos y la revisión externa especializada.

## Acceso público

- Corpus y renderizador: <https://iberolab-es.github.io/IberoLab/>
- Diagnóstico de corpus y SVG: <https://iberolab-es.github.io/IberoLab/test.html>
- Diagnóstico de enlaces profundos: <https://iberolab-es.github.io/IberoLab/deep-link-test.html>

## Principios

- Rigor terminológico y transparencia sobre los límites del conocimiento.
- Separación entre datos documentados, hipótesis y decisiones de diseño.
- Trazabilidad de cada signo, variante, transcripción y recurso gráfico.
- Compatibilidad con móvil y escritorio sin depender de recursos gráficos remotos durante la navegación.
- Pruebas reproducibles antes de publicar una versión estable.
- Ausencia de sustituciones silenciosas cuando una equivalencia sea incierta.

## Estructura actual

```text
.github/     Plantillas, gobernanza y GitHub Actions
data/        Corpus, inventarios, auditorías, manifiestos e informes

docs/        Web pública, diagnósticos y documentación metodológica
scripts/     Validadores, migraciones y utilidades reproducibles
tests/       Pruebas automatizadas de navegador
```

Los futuros módulos de adaptación fonética no se incorporarán hasta que exista una especificación formal aprobada y claramente separada de la base documental.

## Validación local

Las comprobaciones documentales y gráficas utilizan Python sin dependencias de ejecución externas:

```bash
python scripts/validate_corpus.py
python scripts/validate_source_audit.py
python scripts/validate_local_assets.py
python scripts/validate_renderer.py
python scripts/validate_browser_matrix.py
```

La regresión de navegador se ejecuta con Playwright según `playwright.config.cjs` y `.github/workflows/browser-smoke.yml`.

## Participar

Las sugerencias y errores se gestionan mediante [GitHub Issues](https://github.com/iberolab-es/IberoLab/issues/new/choose). Antes de contribuir, consulta [CONTRIBUTING.md](CONTRIBUTING.md), la [metodología](docs/METHODOLOGY.md) y la [procedencia de los recursos](docs/ASSET_PROVENANCE.md).

## Hoja de ruta

Consulta [ROADMAP.md](ROADMAP.md). El seguimiento detallado se concentra actualmente en:

- [fase 1 y base paleográfica](https://github.com/iberolab-es/IberoLab/issues/2);
- [pruebas multidispositivo](https://github.com/iberolab-es/IberoLab/issues/6);
- [especificación futura del motor moderno](https://github.com/iberolab-es/IberoLab/issues/3).

## Licencia

Código y documentación publicados bajo [Apache License 2.0](LICENSE), salvo que un recurso concreto indique otra licencia. Los recursos gráficos de terceros conservan su propia atribución y licencia en el manifiesto y en `NOTICE`.

---

### English summary

IberoLab is an open experimental project for phonetic representation of modern languages using ancient Iberian and other Palaeohispanic scripts. Its current pre-alpha reconstructs a documented seed corpus with nineteen controlled local SVG resources. It does **not** claim to translate modern text into the undeciphered Iberian language, and the modern-input engine has not yet been implemented.
