# Historial de cambios

Todos los cambios relevantes del proyecto se documentarán en este archivo.

El formato se inspira en Keep a Changelog y el proyecto utilizará versionado semántico cuando exista una primera versión funcional.

## [Unreleased]

### Added

- Alcance científico y terminología inicial.
- Guía de contribución.
- Hoja de ruta por fases.
- Metodología de normalización, adaptación y renderizado.
- Política inicial de datos y procedencia.
- Plantillas estructuradas para sugerencias y errores.
- Corpus inicial de once formas ibéricas contrastadas en estudios epigráficos o numismáticos.
- Inventario mínimo de diecinueve tokens de transcripción derivado exclusivamente del corpus.
- Esquema JSON y validador reproducible para lecturas, segmentaciones, fuentes y estados semánticos.
- Auditoría del prototipo HTML anterior: se conserva la arquitectura autónoma, pero se descartan sus glifos experimentales como evidencia paleográfica.
- Mapeo gráfico provisional de dieciocho tokens mediante SVG normalizados de referencia del signario ibérico nororiental dual.
- Página HTML preparada en `docs/index.html` para mostrar las once formas contrastadas con lectura técnica y fallback visible.
- Validador del renderizador para impedir tokens ausentes, referencias SVG inválidas y páginas sin salvaguardas contra salidas vacías.
- Auditoría documental interna de las once formas, con una entrada verificable por forma y fuentes persistentes.
- Validador específico de cobertura de la auditoría documental.
- Flujo de GitHub Actions que ejecuta las validaciones del corpus, las fuentes y el renderizador en cada pull request y cambio de `main`.
- Fuente documental, evidencia, nota de transcripción y enlace persistente visibles para cada forma en la web pública.
- Navegación anterior/siguiente, indicador de posición y enlaces profundos mediante el identificador de cada forma.

### Changed

- La hoja de ruta adopta una estrategia corpus-first: formas atestiguadas, SVG verificados y solo después motor de similitud para entradas modernas.
- Las pruebas iniciales dejan de utilizar nombres personales o topónimos modernos.
- El prototipo anterior aporta su arquitectura de interfaz y renderizado por tokens, pero no sus trazados gráficos experimentales.
- La web distingue ahora entre lectura documentada, interpretación contextual y representación gráfica normalizada.
- La forma `ildiŕda` explica expresamente que el uso de `di/da` es una normalización dual y no un facsímil de la secuencia epigráfica `ti/ta` documentada para un ejemplar.
- GitHub Pages queda registrado como despliegue pre-alpha, no como beta validada.

### Verified

- Publicación correcta desde `main` y `/docs` mediante GitHub Pages.
- Renderizado visible y no vacío de `ildiŕda` en Safari iOS.
- Lectura, segmentación, contexto, interpretación y buzón de sugerencias accesibles en iPhone.

### Known limitations

- El token `ń` de `taŕśabań` permanece sin signo gráfico asignado hasta verificar la convención de transcripción y la forma exacta en la publicación correspondiente.
- Las figuras actuales son formas normalizadas de referencia y no facsímiles de los alógrafos originales de cada inscripción.
- La carga de SVG continúa siendo remota y deberá sustituirse por recursos locales verificados antes de la beta.
- Quedan pendientes las pruebas manuales de las otras diez formas en Safari iOS y las pruebas en navegadores de escritorio.
- La revisión documental realizada es interna; el corpus necesita revisión externa especializada antes de declararse estable.

### Security

- Se evita publicar como traductor literal una herramienta que solo realice representación fonética o recreación experimental.
- Se impide incorporar grafías sin fuente, procedencia o licencia verificable a la base científica.
- Los tokens no resueltos permanecen visibles y etiquetados; no se reemplazan silenciosamente por signos inventados.
- La similitud fonética futura no podrá utilizarse para inferir significado ibérico.
