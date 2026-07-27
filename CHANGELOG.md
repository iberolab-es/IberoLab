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

### Changed

- La hoja de ruta adopta una estrategia corpus-first: formas atestiguadas, SVG verificados y solo después motor de similitud para entradas modernas.
- Las pruebas iniciales dejan de utilizar nombres personales o topónimos modernos.

### Security

- Se evita publicar como traductor literal una herramienta que solo realice representación fonética o recreación experimental.
- Se impide incorporar grafías sin fuente, procedencia o licencia verificable a la base científica.
