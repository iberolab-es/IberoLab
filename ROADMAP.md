# Hoja de ruta de IberoLab

## Fase 0 — Fundación del proyecto

- [x] Crear repositorio público.
- [x] Establecer alcance y límites científicos.
- [x] Adoptar Apache License 2.0.
- [x] Configurar plantillas de issues y gobernanza.
- [x] Definir criterios de aceptación de datos.

## Fase 1A — Corpus contrastado y segmentación

- [x] Crear un corpus inicial de formas presentes en estudios epigráficos o numismáticos.
- [x] Registrar para cada forma la lectura, segmentación, contexto, fuente y nivel de confianza.
- [x] Separar la seguridad de lectura del estado de interpretación semántica.
- [x] Derivar un inventario mínimo de tokens únicamente a partir del corpus.
- [x] Añadir validación automática de integridad y reproducibilidad.
- [ ] Someter el corpus inicial a revisión documental antes de declararlo estable.

## Fase 1B — Inventario paleográfico y SVG verificados

- [x] Crear un mapeo gráfico provisional con formas normalizadas de referencia para 18 de los 19 tokens del corpus.
- [x] Mantener `ń` como token explícitamente pendiente, sin sustituirlo por `n`, `m` o `ḿ`.
- [x] Añadir un validador que comprueba cobertura, archivos SVG y salvaguardas contra salidas vacías.
- [ ] Diseñar el esquema definitivo para signos, alógrafos y variantes.
- [ ] Registrar forma, valor, variante, procedencia, cronología, dirección y referencia de cada alógrafo.
- [ ] Sustituir progresivamente las formas normalizadas por SVG propios derivados de formas documentadas o recursos con licencia compatible.
- [ ] Reconstruir gráficamente las once formas del corpus sin tokens pendientes.
- [ ] Crear pruebas de integridad y regresión visual de la base.
- [ ] Ampliar después, sin mezclar sistemas, a ibérico meridional, greco-ibérico y celtibérico.

## Fase 2 — Motor de similitud y adaptación fonética

- [ ] Definir una representación fonética normalizada para entradas modernas.
- [ ] Comparar secuencias modernas con patrones silábicos y grafemáticos documentados.
- [ ] Segmentar en vocales, continuantes y grupos oclusiva-vocal.
- [ ] Tratar explícitamente sonidos sin equivalente directo.
- [ ] Generar alternativas cuando exista ambigüedad.
- [ ] Etiquetar la confianza y explicar cada decisión.
- [ ] Evitar presentar la adaptación como traducción al idioma ibérico.

## Fase 3 — Renderizador

- [x] Reutilizar del prototipo HTML anterior la arquitectura autónoma y el renderizado por tokens, no sus glifos experimentales.
- [x] Crear una página de referencia con salida inicial visible, lectura técnica y fallback por token.
- [x] Preparar `docs/index.html` para una futura publicación desde `/docs` mediante GitHub Pages.
- [ ] Integrar SVG locales verificados para eliminar la dependencia de carga remota.
- [ ] Verificar compatibilidad real con Safari iOS, Chrome, Firefox y Edge.
- [ ] Escritura de izquierda a derecha y derecha a izquierda cuando corresponda.
- [ ] Copia, descarga y exportación accesible.
- [ ] Pruebas visuales automatizadas.

## Fase 4 — Beta web

- [ ] Interfaz pública clara y responsive.
- [ ] Reconstrucción verificable del corpus contrastado.
- [ ] Adaptación experimental de entradas modernas mediante el motor de similitud.
- [ ] Explicación de qué hace y qué no hace la herramienta.
- [ ] Enlace directo al buzón de sugerencias de GitHub.
- [ ] Publicación gratuita mediante GitHub Pages.

## Fase 5 — Ampliación

- [ ] Comparación entre varios sistemas de escritura.
- [ ] API o paquete reutilizable.
- [ ] Exportación de resultados y metadatos.
- [ ] Revisión externa por especialistas.
- [ ] Versiones educativas y docentes.

## Criterio de publicación

No se etiquetará una versión como beta pública hasta que el renderizador reconstruya de forma visible y reproducible las formas contrastadas en móvil y escritorio, y cada transformación moderna pueda explicarse paso a paso.
