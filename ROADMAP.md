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

- [ ] Diseñar el esquema de datos para signos, alógrafos y variantes.
- [ ] Comenzar por el signario ibérico nororiental necesario para el corpus contrastado.
- [ ] Registrar forma, valor, variante, procedencia, cronología, dirección y referencia.
- [ ] Incorporar SVG propios derivados de formas documentadas o recursos con licencia compatible.
- [ ] Reconstruir gráficamente las formas del corpus sin signos vacíos.
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

- [ ] Reutilizar del prototipo HTML anterior la arquitectura autónoma y el renderizado por tokens, no sus glifos experimentales.
- [ ] Renderizado SVG independiente de fuentes del sistema.
- [ ] Compatibilidad con Safari iOS, Chrome, Firefox y Edge.
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
