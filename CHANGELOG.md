# Historial de cambios

Todos los cambios relevantes del proyecto se documentarán en este archivo.

El formato se inspira en Keep a Changelog y el proyecto utilizará versionado semántico cuando exista una primera versión funcional.

## Unreleased — identidad pública, historia y lectura aproximada

- La raíz del sitio se convierte en una portada visual y el renderizador documentado pasa a `corpus.html`.
- Los enlaces históricos `/#ib-ne-…` redirigen al corpus conservando su identificador.
- Se incorpora un emblema contemporáneo con significado oficial y advertencia expresa de que no es un signo arqueológico.
- Se publican páginas de Historia y Metodología preparadas para futuros contenidos didácticos y de YouTube.
- El conversor añade una lectura vocal moderna de la secuencia generada, etiquetada como recurso aproximado y no como pronunciación histórica auténtica.
- Se añaden validación estática y regresión en Chromium, Firefox y WebKit para la nueva capa pública.

## Unreleased — historial local privado

- El demostrador recuerda como máximo cinco adaptaciones exitosas en el navegador.
- Las entradas recientes pueden reutilizarse con un toque y borrarse por completo.
- No se guarda el historial en IberoLab ni se envía a ningún servidor del proyecto.
- La regresión comprueba persistencia, orden, reutilización y borrado.

## Unreleased — resultados compartibles y frases más claras

- Los resultados del demostrador disponen de URL restaurable mediante `?q=`.
- Se añade compartir nativo en móvil con copia al portapapeles como alternativa.
- Las frases muestran el rótulo de cada palabra sobre su grupo de signos.
- La regresión comprueba restauración, actualización de URL y contenido compartido.

## [Unreleased]

### Added

- Alcance científico, terminología, guía de contribución, hoja de ruta y política de datos.
- Corpus inicial de once formas ibéricas contrastadas en estudios epigráficos o numismáticos.
- Inventario mínimo de diecinueve tokens derivado exclusivamente del corpus.
- Esquemas y validadores reproducibles para corpus, fuentes, inventario, recursos y documentos de estado.
- Auditoría del prototipo HTML anterior: se conserva la arquitectura autónoma, pero no sus glifos experimentales como evidencia paleográfica.
- Renderizador público del corpus con navegación, lectura técnica, fuentes y enlaces profundos.
- Diagnóstico gráfico de las once formas y diagnóstico independiente de enlaces profundos.
- Regresión automática con Playwright sobre Chromium, Firefox y WebKit.
- Dieciocho SVG normalizados de la serie nororiental dual y variante paleográfica m1 para resolver `ń` en el corpus.
- Manifiesto del corpus con diecinueve recursos, procedencia, licencia, tamaño y SHA-256.
- Contrato machine-readable `specification_only` para un futuro motor formal de adaptación fonética.
- Esquemas mutuamente excluyentes para resultados satisfactorios e intentos bloqueados.
- Registro de dimensiones de pronunciación española sin perfil universal o valor por defecto.
- Biblioteca gráfica independiente con los 38 signos normalizados de la serie `Sign Iber Noro Dual 01–38` para el demostrador práctico.
- Manifiesto `data/signs/mvp-standard-signary.assets.v1.json` con fuente, licencia, ruta, tamaño y SHA-256 de los 38 SVG.
- Contrato `data/engine/mvp-short-converter.v1.json` para nombres, palabras y frases de hasta 48 caracteres y 6 palabras.
- Adaptador determinista `docs/mvp-converter.js` con correspondencias directas, vocales de apoyo declaradas y aproximaciones visibles.
- Página responsive `docs/convertir.html` con ejemplos `amor`, `familia`, `te quiero`, `hogar` y `amistad`.
- Audio para escuchar la entrada española y una lectura moderna aproximada de la secuencia generada.
- Validador del demostrador que conserva separado el manifiesto científico de 19 recursos.
- Pruebas de navegador para adaptaciones directas, aproximadas y bloqueadas.
- Acceso al demostrador desde la portada y buzón estructurado de sugerencias.

### Changed

- La hoja de ruta adopta una estrategia corpus-first para la base científica y una vía MVP separada para la utilidad práctica.
- La web distingue entre corpus atestiguado, demostrador moderno y motor formal futuro.
- El demostrador se clasifica siempre como `experimental_phonetic_adaptation` y nunca como traducción.
- El inventario científico permanece limitado a los tokens exigidos por el corpus, mientras el demostrador utiliza una capa gráfica completa e independiente.
- `b/p`, `r/ŕ`, sonidos sin equivalente directo y grupos consonánticos se gestionan mediante convenciones de proyecto explicadas en pantalla.
- Los símbolos desconocidos bloquean la ejecución en lugar de desaparecer o producir candidatos parciales.
- Los SVG se sirven exclusivamente desde el repositorio; la navegación no depende de Wikimedia.
- Los flujos temporales con permiso de escritura se eliminan después de generar o integrar recursos.

### Verified

- Publicación correcta desde `main` y `/docs` mediante GitHub Pages.
- Funcionamiento del corpus histórico en Safari, Chrome, Brave y Edge sobre iPhone con la implementación remota previa.
- Cobertura actual del corpus: once formas, diecinueve SVG locales y cero tokens gráficos pendientes.
- `ń` resuelto mediante la variante m1 documentada, conservando `m` como transcripción histórica.
- Integridad, XML, procedencia y ausencia de contenido activo comprobados para los recursos locales.
- Regresión automática del corpus y los enlaces profundos satisfactoria en Chromium, Firefox y WebKit.
- Contrato del motor formal validado con etapas no implementadas, pesos vacíos y puertas cerradas.
- Registro de perfiles españoles validado sin perfil aprobado ni pronunciación adivinada.
- Descarga controlada de los veinte SVG estándar que faltaban y reutilización de los dieciocho ya versionados.
- Manifiesto MVP completo con 38/38 recursos locales y manifiesto científico conservado en 19/19.
- Ejemplos contractuales: `amor` → `a · m · o · r`; `familia` → `ba · m · i · l · i · a`; `te quiero` → `te / ki · e · r · o`.

### Known limitations

- Los signos son formas normalizadas de referencia y no facsímiles de alógrafos arqueológicos concretos.
- El demostrador aplica convenciones de proyecto y no reconstruye vocabulario ni significado ibéricos.
- Ambos audios usan síntesis moderna del navegador; la lectura aproximada no reconstruye la pronunciación ibérica antigua.
- Las aproximaciones para `f`, `ñ`, `ch`, `y/ll`, `j`, `z/c` y otros sonidos modernos requieren revisión y pueden mejorarse.
- Deben repetirse manualmente las pruebas actuales en Safari/iOS y en Chrome, Firefox y Edge de ordenador.
- La cobertura automática no sustituye revisión visual ni evaluación con usuarios.
- El corpus y la selección de alógrafos específicos necesitan revisión externa antes de declararse estables.
- El motor formal con perfiles aprobados, reglas versionadas, alternativas, costes y confianza calibrada continúa sin implementar.

### Security and scientific boundaries

- No se publica como traducción una operación de adaptación fonética o recreación gráfica.
- No se infiere significado ibérico a partir de similitud sonora.
- No se incorporan recursos sin procedencia o licencia verificable.
- No se permiten salidas vacías, sustituciones silenciosas ni candidatos parciales tras un bloqueo.
- Los SVG se validan como XML, se comparan mediante SHA-256 y se rechazan si contienen scripts, manejadores de eventos, `javascript:` o `foreignObject`.
- Los CI ordinarios conservan permiso de solo lectura.
