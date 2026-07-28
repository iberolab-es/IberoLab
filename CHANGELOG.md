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
- Esquema JSON específico para el inventario mínimo sincronizado con el mapeo gráfico y el manifiesto de recursos.
- Auditoría del prototipo HTML anterior: se conserva la arquitectura autónoma, pero se descartan sus glifos experimentales como evidencia paleográfica.
- Mapeo gráfico inicial de dieciocho tokens mediante SVG normalizados del signario ibérico nororiental dual, ampliado después con la variante m1 documentada.
- Página HTML preparada en `docs/index.html` para mostrar las once formas contrastadas con lectura técnica y fallback visible.
- Validador del renderizador para impedir tokens ausentes, referencias SVG inválidas y páginas sin salvaguardas contra salidas vacías.
- Auditoría documental interna de las once formas, con una entrada verificable por forma y fuentes persistentes.
- Validador específico de cobertura de la auditoría documental.
- Flujo de GitHub Actions que ejecuta las validaciones del corpus, las fuentes y el renderizador en cada pull request y cambio de `main`.
- Fuente documental, evidencia, nota de transcripción y enlace persistente visibles para cada forma en la web pública.
- Navegación anterior/siguiente, indicador de posición y enlaces profundos mediante el identificador de cada forma.
- Página pública de autodiagnóstico para comprobar las once formas, la carga de los signos y la ausencia de salidas vacías.
- Página pública independiente que abre secuencialmente los once enlaces profundos y verifica el hash, la selección, la lectura y la salida gráfica efectiva.
- Regresión automática con Playwright sobre Chromium, Firefox y WebKit para las once formas y las dos páginas de diagnóstico.
- Variante paleográfica m1 normalizada, trazable y licenciada para resolver la transcripción ń del corpus.
- Matriz versionada de pruebas en Safari, Chrome, Brave, Firefox y Edge, separando los entornos móviles de los navegadores ejecutados realmente en ordenador.
- Diecinueve SVG de referencia almacenados dentro del repositorio bajo rutas estables.
- Manifiesto individual de los recursos gráficos con origen, URL resuelta, autoría, licencia, tamaño y hash SHA-256.
- Validador de integridad de los SVG locales, su procedencia, sus hashes y la ausencia de elementos activos inseguros.
- Validación transversal que contrasta manifiesto, mapeo, inventario mínimo, matriz, autodiagnóstico y documentos de estado.
- Documentación específica de procedencia y procedimiento reproducible de actualización de los recursos gráficos.
- Contrato machine-readable `specification_only` para el futuro motor de adaptación fonética.
- Esquema JSON de resultados que exige versiones, capas, candidatos, operaciones, costes, explicaciones y ausencia de afirmaciones semánticas.
- Esquema JSON independiente para intentos bloqueados, que exige razones explícitas y prohíbe candidatos parciales.
- Registro machine-readable que declara como mutuamente excluyentes los estados `success` y `blocked`.
- Especificación normativa de las etapas, invariantes, ambigüedad, errores, costes, confianza y puertas de implementación.
- Validador que impide activar conversión pública, perfiles, reglas, pesos o confianza calibrada antes de su aprobación.
- Validador que comprueba la exclusión entre resultados válidos e intentos bloqueados y prohíbe afirmaciones semánticas en ambos estados.

### Changed

- La hoja de ruta adopta una estrategia corpus-first: formas atestiguadas, SVG verificados y solo después motor de similitud para entradas modernas.
- Las pruebas iniciales dejan de utilizar nombres personales o topónimos modernos.
- El prototipo anterior aporta su arquitectura de interfaz y renderizado por tokens, pero no sus trazados gráficos experimentales.
- La web distingue ahora entre lectura documentada, interpretación contextual y representación gráfica normalizada.
- La forma `ildiŕda` explica expresamente que el uso de `di/da` es una normalización dual y no un facsímil de la secuencia epigráfica `ti/ta` documentada para un ejemplar.
- GitHub Pages queda registrado como despliegue pre-alpha, no como beta validada.
- El renderizador público y el autodiagnóstico cargan los signos exclusivamente desde el propio repositorio y ya no dependen de Wikimedia durante la navegación.
- El autodiagnóstico pasa a la versión `1.2.0`, identifica `asset_mode: local_repository`, espera 19 SVG y no admite tokens gráficos pendientes.
- Las pruebas móviles realizadas sobre la implementación remota se conservan como evidencia histórica, pero pasan a estado parcial hasta repetirse con los SVG locales actuales.
- El flujo ordinario de GitHub Actions valida la existencia, el hash, el XML y la trazabilidad de los diecinueve SVG locales.
- El inventario mínimo pasa de ser una lista de transcripciones con gráficos pendientes a un dataset enlazado token por token con el mapeo y el manifiesto actuales.
- La documentación de pruebas separa el diagnóstico gráfico del diagnóstico de enlaces profundos para conservar informes reproducibles y responsabilidades técnicas distintas.
- Los cambios en `docs/`, la configuración de Playwright o la suite de navegador activan una comprobación automática en tres motores con permisos de solo lectura.
- La fase 2 separa el contrato estructural ya aprobado de perfiles, reglas, pesos, calibración e implementación todavía pendientes.
- Cualquier resultado futuro deberá clasificarse como adaptación fonética experimental, conservar todas las versiones y mantener vacía la colección de afirmaciones semánticas.
- Un intento bloqueado deja de poder representarse como resultado degradado: debe usar su propio esquema, mantener vacíos los candidatos y explicar las razones del bloqueo.

### Verified

- Publicación correcta desde `main` y `/docs` mediante GitHub Pages.
- Funcionamiento técnico de las once formas en Safari, Chrome, Brave y Edge sobre iPhone en la implementación remota previa: 11/11 formas, 18/18 SVG y cero salidas vacías.
- `ń` queda resuelto mediante la variante paleográfica m1 documentada; se conserva `m` como transcripción histórica y el recurso no se presenta como facsímil.
- Descarga reproducible de los dieciocho SVG iniciales y del recurso m1, generación del manifiesto y migración local superadas en GitHub Actions.
- Validaciones del corpus, inventario mínimo, auditoría documental, integridad gráfica, renderizador, matriz y estado transversal superadas.
- Ejecución automática completa satisfactoria en Chromium, Firefox y WebKit: once enlaces, diecinueve SVG locales y ambos diagnósticos sin fallos.
- Contrato del motor validado con ocho etapas no implementadas, ocho tipos estructurales de operación, pesos vacíos y todas las puertas de implementación cerradas.
- Registro de estados validado con un esquema de éxito que exige candidatos y otro de bloqueo que los prohíbe.

### Known limitations

- Las figuras actuales son formas normalizadas de referencia y no facsímiles de los alógrafos originales de cada inscripción.
- Deben repetirse las pruebas móviles después del despliegue de los SVG locales actuales.
- Continúan pendientes Google Chrome, Mozilla Firefox y Microsoft Edge ejecutados manualmente en ordenador y la ejecución registrada del diagnóstico de enlaces profundos en esos entornos.
- La cobertura automática de Chromium, Firefox y WebKit no sustituye navegadores de marca, Safari/iOS ni una regresión visual píxel a píxel.
- La revisión documental realizada es interna; el corpus necesita revisión externa especializada antes de declararse estable.
- La selección de alógrafos específicos de cada testimonio sigue pendiente.
- El motor para entradas modernas todavía no está implementado.
- No existen todavía perfiles de pronunciación, inventario fonético aprobado, reglas de adaptación, pesos, calibración ni candidatos lingüísticos válidos.

### Security

- Se evita publicar como traductor literal una herramienta que solo realice representación fonética o recreación experimental.
- Se impide incorporar grafías sin fuente, procedencia o licencia verificable a la base científica.
- Cualquier token no resuelto futuro deberá permanecer visible y etiquetado; no podrá reemplazarse silenciosamente por un signo inventado.
- La similitud fonética futura no podrá utilizarse para inferir significado ibérico.
- Los SVG se validan como XML, se comparan mediante SHA-256 y se rechazan si contienen marcadores activos como scripts, manejadores de eventos o `foreignObject`.
- Los flujos temporales con permiso de escritura se eliminan antes de fusionar; los CI ordinarios conservan únicamente permiso de lectura.
- La regresión de navegador utiliza dependencias y navegadores fijados por la versión de Playwright y conserva evidencias solo cuando una prueba falla.
- El contrato del motor prohíbe salida pública mientras cualquier puerta permanezca cerrada y exige trazabilidad completa de cada operación futura.
- Los bloqueos del motor no pueden filtrar candidatos incompletos ni utilizar una confianza baja como sustituto de una condición de error.
