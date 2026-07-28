# Hoja de ruta de IberoLab

## Fase 0 — Fundación del proyecto

- [x] Crear repositorio público.
- [x] Establecer alcance y límites científicos.
- [x] Adoptar Apache License 2.0.
- [x] Configurar plantillas de issues y gobernanza.
- [x] Definir criterios de aceptación de datos.
- [x] Añadir validación automática en GitHub Actions para cada cambio propuesto.

## Fase 1A — Corpus contrastado y segmentación

- [x] Crear un corpus inicial de formas presentes en estudios epigráficos o numismáticos.
- [x] Registrar para cada forma la lectura, segmentación, contexto, fuente y nivel de confianza.
- [x] Separar la seguridad de lectura del estado de interpretación semántica.
- [x] Derivar un inventario mínimo de tokens únicamente a partir del corpus.
- [x] Añadir validación automática de integridad y reproducibilidad.
- [x] Completar una revisión documental interna, forma por forma, con fuentes persistentes.
- [ ] Obtener revisión externa de una persona especialista antes de declarar estable el corpus.

## Fase 1B — Inventario paleográfico y SVG verificados

### Base gráfica del corpus inicial

- [x] Crear un mapeo gráfico de referencia para los 19 tokens del corpus.
- [x] Integrar los 19 SVG dentro del repositorio y eliminar su dependencia remota durante la navegación.
- [x] Resolver `ń` como transcripción actual de la variante paleográfica `m1`, conservando `m` como transcripción histórica y sin confundirla con `n` o `ḿ`.
- [x] Registrar para cada SVG la fuente, autoría, licencia, ruta local, tamaño y hash SHA-256.
- [x] Añadir pruebas automáticas de existencia, integridad criptográfica, XML válido y ausencia de marcadores activos inseguros.
- [x] Reconstruir las once formas sin salidas vacías ni tokens gráficos pendientes.
- [x] Ejecutar regresión automática sobre Chromium, Firefox y WebKit.

### Base paleográfica ampliada

- [ ] Diseñar el esquema definitivo para signos, alógrafos y variantes.
- [ ] Registrar forma, valor, variante, procedencia, cronología, dirección y referencia de cada alógrafo.
- [ ] Sustituir progresivamente las formas normalizadas por SVG propios derivados de testimonios documentados o por recursos compatibles seleccionados específicamente.
- [ ] Obtener revisión externa especializada de la selección gráfica y de la separación entre lectura, variante y valor.
- [ ] Crear pruebas automatizadas de regresión visual cuando exista una base visual estable.
- [ ] Ampliar después, sin mezclar sistemas, a ibérico meridional, greco-ibérico y celtibérico.

## Fase 2 — Motor de similitud y adaptación fonética

### Especificación permitida antes de implementar

- [x] Definir un contrato versionado para capas, etapas, candidatos, operaciones, costes, confianza, explicaciones y dependencias.
- [x] Separar formalmente información lingüística, decisiones de adaptación y resolución gráfica.
- [x] Definir el esquema machine-readable de un resultado de adaptación experimental sin afirmaciones semánticas.
- [x] Mantener perfiles, reglas, pesos, confianza calibrada y conversión pública explícitamente desactivados en el contrato inicial.
- [ ] Aprobar una representación fonética interna y su inventario de rasgos para entradas españolas.
- [ ] Definir perfiles de pronunciación de español europeo sin imponer silenciosamente una variedad regional.
- [ ] Construir un inventario explícito de sonidos modernos sin equivalente directo.
- [ ] Definir el esquema de reglas y sus niveles de evidencia.
- [ ] Preparar casos de prueba contractuales sin inventar salidas lingüísticas.
- [ ] Documentar pesos, empates y calibración solo después de disponer de reglas y evaluación suficientes.

### Implementación bloqueada

- [ ] Normalizar ortografía y pronunciación de entradas modernas.
- [ ] Segmentar en vocales, continuantes y grupos oclusiva-vocal compatibles con el sistema seleccionado.
- [ ] Comparar secuencias modernas con patrones silábicos y grafemáticos documentados.
- [ ] Generar alternativas cuando exista ambigüedad.
- [ ] Calcular costes y confianza de forma determinista y reproducible.
- [ ] Explicar cada sustitución, pérdida o aproximación.
- [ ] Evitar presentar la adaptación como traducción al idioma ibérico.

La especificación estructural está versionada en `data/engine/phonetic-engine-contract.v1.json` y `docs/PHONETIC_ENGINE_SPEC.md`. La implementación y su exposición pública continúan bloqueadas hasta completar las pruebas manuales actuales del renderizador, fijar el modelo mínimo de alógrafos, aprobar el perfil fonético y someter la base inicial a revisión externa.

## Fase 3 — Renderizador

- [x] Reutilizar del prototipo HTML anterior la arquitectura autónoma y el renderizado por tokens, no sus glifos experimentales.
- [x] Crear una página de referencia con salida inicial visible, lectura técnica y fallback por token.
- [x] Preparar `docs/index.html` para publicación desde `/docs` mediante GitHub Pages.
- [x] Añadir navegación por las once formas, enlaces profundos y fuente documental visible.
- [x] Revisar técnicamente las once formas en Safari, Chrome, Brave y Edge sobre iPhone en la implementación remota previa.
- [x] Integrar 19 SVG locales controlados y adaptar el autodiagnóstico para identificarlos como `local_repository`.
- [x] Añadir una prueba pública de los once enlaces profundos.
- [x] Ejecutar regresión automática en Chromium, Firefox y WebKit.
- [ ] Repetir ambos diagnósticos en Safari, Chrome, Brave y Edge sobre iPhone después del despliegue local de 19 SVG.
- [ ] Verificar ambos diagnósticos en Google Chrome, Mozilla Firefox y Microsoft Edge ejecutados realmente en ordenador.
- [ ] Escritura de izquierda a derecha y derecha a izquierda cuando corresponda.
- [ ] Copia, descarga y exportación accesible.
- [ ] Regresión visual automatizada cuando se estabilice la selección de alógrafos.

## Fase 4 — Beta web

- [x] Publicar una versión pre-alpha gratuita mediante GitHub Pages.
- [x] Disponer de una interfaz pública responsive con salida inicial visible.
- [x] Explicar públicamente qué hace y qué no hace la herramienta.
- [x] Enlazar el buzón estructurado de sugerencias de GitHub.
- [ ] Confirmar mediante pruebas manuales que todo el corpus se reconstruye con los recursos locales actuales en móvil y escritorio.
- [ ] Incorporar una adaptación experimental de entradas modernas solo después de aprobar la especificación, las reglas y sus pruebas.
- [ ] Superar la revisión paleográfica, las pruebas multidispositivo y la revisión externa necesarias para etiquetar una beta.

## Fase 5 — Ampliación

- [ ] Comparación entre varios sistemas de escritura.
- [ ] API o paquete reutilizable.
- [ ] Exportación de resultados y metadatos.
- [ ] Revisión externa por especialistas.
- [ ] Versiones educativas y docentes.

## Criterio de publicación

La pre-alpha puede mostrar formas contrastadas y limitaciones explícitas. No se etiquetará una versión como beta hasta que el renderizador reconstruya de forma visible y reproducible el corpus mediante recursos controlados en móvil y escritorio, la base gráfica haya recibido revisión externa suficiente y cada transformación moderna pueda explicarse paso a paso.
