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

## Fase 2 — Adaptación de entradas modernas

### Fase 2A — Demostrador MVP práctico

Objetivo limitado: nombres, palabras y frases breves con representación gráfica, reglas deterministas y aproximaciones visibles.

- [x] Mantener separado el corpus científico de la capa gráfica práctica.
- [x] Integrar una biblioteca independiente con los 38 signos normalizados de la serie nororiental dual.
- [x] Registrar para los 38 SVG fuente, licencia, ruta, tamaño y SHA-256.
- [x] Limitar la entrada a 48 caracteres y 6 palabras.
- [x] Representar vocales y continuantes mediante signos alfabéticos.
- [x] Representar oclusivas mediante silabogramas y declarar cualquier vocal de apoyo.
- [x] Definir aproximaciones visibles para sonidos modernos sin equivalente directo.
- [x] Bloquear símbolos no admitidos y prohibir salidas vacías.
- [x] Añadir ejemplos contractuales para `amor`, `familia` y `te quiero`.
- [x] Crear una interfaz responsive separada del corpus atestiguado.
- [x] Añadir audio opcional exclusivamente para la entrada española.
- [x] Añadir una voz fluida moderna y una síntesis técnica reproducible, con perfiles versionados, hipótesis visibles y prohibición expresa de presentarlas como pronunciación histórica o prueba de parentesco.
- [x] Añadir regresión automática para resultados directos, aproximados y bloqueados.
- [ ] Repetir manualmente las pruebas del demostrador en Safari/iOS, Chrome, Firefox y Edge.
- [ ] Revisar con usuarios reales si las explicaciones son comprensibles y suficientemente breves.

El demostrador se etiqueta siempre como **adaptación fonética experimental**. No es una traducción, no atribuye significado ibérico y no activa el motor formal.

### Especificación permitida antes de implementar el motor formal

- [x] Definir un contrato versionado para capas, etapas, candidatos, operaciones, costes, confianza, explicaciones y dependencias.
- [x] Separar formalmente información lingüística, decisiones de adaptación y resolución gráfica.
- [x] Definir el esquema machine-readable de un resultado de adaptación experimental sin afirmaciones semánticas.
- [x] Mantener perfiles, reglas, pesos, confianza calibrada y conversión formal explícitamente desactivados en el contrato inicial.
- [x] Definir el esquema de perfiles de pronunciación de español europeo y un registro inicial de dimensiones sin perfil por defecto.
- [ ] Aprobar uno o más perfiles españoles después de revisión interna, revisión externa y delimitación geográfica y de registro.
- [ ] Aprobar una representación fonética interna y su inventario de rasgos para entradas españolas.
- [ ] Construir un inventario explícito de sonidos modernos sin equivalente directo.
- [ ] Definir el esquema formal de reglas y sus niveles de evidencia.
- [ ] Documentar pesos, empates y calibración solo después de disponer de reglas y evaluación suficientes.

### Implementación bloqueada del motor formal

- [ ] Normalizar ortografía y pronunciación mediante perfiles formalmente aprobados.
- [ ] Comparar secuencias modernas con patrones silábicos y grafemáticos documentados.
- [ ] Generar alternativas ordenadas cuando exista ambigüedad.
- [ ] Calcular costes y confianza calibrada de forma reproducible.
- [ ] Versionar conjuntos formales de reglas y modelos de evaluación.

La implementación formal continúa bloqueada por las pruebas manuales actuales del renderizador, el modelo mínimo de alógrafos, la revisión externa, el perfil fonético y la evaluación. Estos bloqueos no impiden mantener un demostrador MVP pequeño, explícito y sin pretensión de referencia lingüística universal.

## Fase 3 — Renderizador

- [x] Reutilizar del prototipo HTML anterior la arquitectura autónoma y el renderizado por tokens, no sus glifos experimentales.
- [x] Crear una página de referencia con salida inicial visible, lectura técnica y fallback por token.
- [x] Preparar `docs/index.html` para publicación desde `/docs` mediante GitHub Pages.
- [x] Añadir navegación por las once formas, enlaces profundos y fuente documental visible.
- [x] Revisar técnicamente las once formas en Safari, Chrome, Brave y Edge sobre iPhone en la implementación remota previa.
- [x] Integrar 19 SVG locales controlados y adaptar el autodiagnóstico para identificarlos como `local_repository`.
- [x] Añadir una prueba pública de los once enlaces profundos.
- [x] Ejecutar regresión automática en Chromium, Firefox y WebKit.
- [x] Añadir una página independiente para el demostrador de entradas breves.
- [ ] Repetir ambos diagnósticos del corpus en Safari, Chrome, Brave y Edge sobre iPhone después del despliegue local de 19 SVG.
- [ ] Verificar el corpus y el demostrador en Google Chrome, Mozilla Firefox y Microsoft Edge ejecutados realmente en ordenador.
- [ ] Escritura de izquierda a derecha y derecha a izquierda cuando corresponda.
- [ ] Descarga o exportación gráfica accesible.
- [ ] Regresión visual automatizada cuando se estabilice la selección de alógrafos.

## Fase 4 — Publicación web

- [x] Publicar una versión pre-alpha gratuita mediante GitHub Pages.
- [x] Disponer de una interfaz pública responsive con salida inicial visible.
- [x] Explicar públicamente qué hace y qué no hace la herramienta.
- [x] Enlazar el buzón estructurado de sugerencias de GitHub.
- [x] Incorporar un demostrador experimental para entradas modernas breves.
- [ ] Confirmar manualmente el funcionamiento del corpus y del demostrador en móvil y escritorio.
- [ ] Mejorar las reglas del MVP solo cuando el cambio pueda explicarse y probarse.
- [ ] Superar la revisión paleográfica y multidispositivo necesaria antes de etiquetar una beta.

## Fase 5 — Ampliación opcional

- [ ] Exportación de resultados y metadatos.
- [ ] Comparación entre varios sistemas de escritura.
- [ ] API o paquete reutilizable.
- [ ] Versiones educativas y docentes.
- [ ] Revisión externa por especialistas cuando el alcance del proyecto la justifique.

## Criterio de publicación

La pre-alpha puede ofrecer un demostrador breve siempre que identifique la salida como adaptación fonética experimental, explique las aproximaciones, no produzca vacíos silenciosos y mantenga separado el corpus atestiguado. Una futura beta formal exigirá mayor revisión paleográfica, pruebas multidispositivo y reglas lingüísticas versionadas.
