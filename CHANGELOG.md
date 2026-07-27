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
- Página pública de autodiagnóstico para comprobar las once formas, la carga de los signos y la ausencia de salidas vacías.
- Matriz versionada de pruebas en Safari, Chrome, Brave, Firefox y Edge, separando los entornos móviles de los navegadores ejecutados realmente en ordenador.
- Dieciocho SVG de referencia almacenados dentro del repositorio bajo rutas estables.
- Manifiesto individual de los recursos gráficos con origen, URL resuelta, autoría, licencia, tamaño y hash SHA-256.
- Validador de integridad de los SVG locales, su procedencia, sus hashes y la ausencia de elementos activos inseguros.
- Documentación específica de procedencia y procedimiento reproducible de actualización de los recursos gráficos.

### Changed

- La hoja de ruta adopta una estrategia corpus-first: formas atestiguadas, SVG verificados y solo después motor de similitud para entradas modernas.
- Las pruebas iniciales dejan de utilizar nombres personales o topónimos modernos.
- El prototipo anterior aporta su arquitectura de interfaz y renderizado por tokens, pero no sus trazados gráficos experimentales.
- La web distingue ahora entre lectura documentada, interpretación contextual y representación gráfica normalizada.
- La forma `ildiŕda` explica expresamente que el uso de `di/da` es una normalización dual y no un facsímil de la secuencia epigráfica `ti/ta` documentada para un ejemplar.
- GitHub Pages queda registrado como despliegue pre-alpha, no como beta validada.
- El renderizador público y el autodiagnóstico cargan los signos exclusivamente desde el propio repositorio y ya no dependen de Wikimedia durante la navegación.
- El autodiagnóstico pasa a la versión `1.1.0` e identifica explícitamente `asset_mode: local_repository` en sus informes.
- Las pruebas móviles realizadas sobre la implementación remota se conservan como evidencia histórica, pero pasan a estado parcial hasta repetirse con los SVG locales desplegados.
- El flujo ordinario de GitHub Actions valida ahora también la existencia, el hash, el XML y la trazabilidad de los dieciocho SVG locales.

### Verified

- Publicación correcta desde `main` y `/docs` mediante GitHub Pages.
- Funcionamiento técnico de las once formas en Safari, Chrome, Brave y Edge sobre iPhone en la implementación remota previa: 11/11 formas, 18/18 SVG y cero salidas vacías.
- `ń` permanece visible como único token deliberadamente pendiente en `taŕśabań`.
- Descarga reproducible de los dieciocho SVG CC0, generación del manifiesto y migración local superadas en GitHub Actions.
- Validaciones del corpus, auditoría documental, integridad gráfica, renderizador y matriz de navegadores superadas en la rama de integración local.

### Known limitations

- El token `ń` de `taŕśabań` permanece sin signo gráfico asignado hasta verificar la convención de transcripción y la forma exacta en la publicación correspondiente.
- Las figuras actuales son formas normalizadas de referencia y no facsímiles de los alógrafos originales de cada inscripción.
- Deben repetirse las pruebas móviles después del despliegue de los SVG locales.
- Continúan pendientes Chrome, Firefox y Edge ejecutados realmente en ordenador y la comprobación manual de los enlaces profundos.
- La revisión documental realizada es interna; el corpus necesita revisión externa especializada antes de declararse estable.
- La regresión visual automatizada y la selección de alógrafos específicos de cada testimonio siguen pendientes.

### Security

- Se evita publicar como traductor literal una herramienta que solo realice representación fonética o recreación experimental.
- Se impide incorporar grafías sin fuente, procedencia o licencia verificable a la base científica.
- Los tokens no resueltos permanecen visibles y etiquetados; no se reemplazan silenciosamente por signos inventados.
- La similitud fonética futura no podrá utilizarse para inferir significado ibérico.
- Los SVG se validan como XML, se comparan mediante SHA-256 y se rechazan si contienen marcadores activos como scripts, manejadores de eventos o `foreignObject`.
- El flujo temporal con permiso de escritura utilizado para generar los recursos se elimina antes de fusionar la integración; el CI ordinario conserva únicamente permiso de lectura.
