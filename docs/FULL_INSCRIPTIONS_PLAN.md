# Ampliación a inscripciones completas — propuesta, 26/10/2026

No añade registros al catálogo ni acredita segmentaciones. El catálogo actual sigue conteniendo once formas aisladas. La prioridad es una edición pequeña con capas de evidencia separadas, no ampliar automáticamente el conversor.

## Primera selección documental

| Prioridad | Objeto y edición | Evidencia disponible | Condición para incorporarlo |
| --- | --- | --- | --- |
| 1 | Mosaico de La Caridad, Caminreal; MLH E.7.1 = K.5.3; Simón Cornago 2015, pp. 96–102 | Texto breve con interpunciones; análisis publicado del nombre y sufijos, con discusión de sus funciones | Conservar los separadores gráficos separados del análisis lingüístico; confirmar derechos de la edición |
| 1 | Escifo de Mas Castellar, fragmentos MC-30426-5 + MC-30453-12; Ferrer i Jané et al. 2025, pp. 185–187, tabla 1 p. 191 | Lectura completa propuesta al reunir dos fragmentos; nombre + ar como propuesta publicada | Registrar signos parcialmente conservados y alternativas; no confundir este vaso con el fragmentario de 2014 |
| 2 | Estela de Sinarcas; Quixal Santos, Ferrer i Jané e Iranzo Viana 2024, tabla 1 p. 169 | Propuesta de estructura y alternativas de interpretación; no segmentación consensuada | Revisar la edición íntegra, lagunas y lecturas con especialista antes de transcribirla en el catálogo |

Caminreal permite empezar por una lectura breve; Mas Castellar prueba la gestión de reconstrucciones. Sinarcas debe esperar a un procedimiento sólido para alternativas. «Texto completo» describe el alcance de la edición, no garantiza conservación íntegra ni lectura cierta.

## Modelo de ficha propuesto

| Capa | Campos mínimos y reglas |
| --- | --- |
| Identificación | ID interno estable; identificadores externos con autoridad, fuente y fecha de comprobación; inventarios de cada fragmento |
| Objeto | Lugar, contexto de hallazgo, soporte, conservación; intervalo de datación y fundamento bibliográfico; distinguir contexto y fecha de ejecución |
| Escritura | Sistema nororiental; subtipo dual/no dual/desconocido solo si consta en la fuente; lengua separada |
| Original | Fotografías/dibujos únicamente con derechos propios verificados; nunca sustituirlos por signos SVG normalizados |
| Edición | Transliteración por líneas, convenciones de la edición, lagunas, restituciones y signos dudosos; autor, año, páginas/figuras y URL |
| División gráfica | Separadores atestiguados en el objeto y saltos de línea; sin atribuirles automáticamente función léxica |
| Segmentación | Lista independiente de análisis publicados, unidades y correspondencia con el texto; autoría, localizador, estado propuesto/discutido y revisión especializada |
| Interpretación | Hipótesis semánticas atribuidas por separado; traducción solo si la fuente y su grado de incertidumbre se explicitan |
| Variantes y certeza | Ediciones alternativas conservadas; certeza por lectura/análisis, sin porcentajes inventados ni herencia automática de la certeza del nombre |
| Derechos y revisión | Licencia por recurso y titular, atribución, modificaciones, fecha de consulta, permisos, revisión e historial; null explicado para datos ausentes |

La interfaz será HTML estático por ficha, índice desde corpus.html y búsqueda opcional. Un módulo de inscripciones independiente de `attested-forms` evitará convertir tokens del renderizador en análisis lingüístico. No se integrarán segmentaciones generadas por IA.

## Reutilización: decisión por material

* Mas Castellar: la ficha editorial declara CC BY-SA 4.0. El texto cubierto puede reutilizarse cumpliendo atribución, enlace a licencia, indicación de cambios y compartir igual. Revisar créditos de cada figura antes de copiarla; mantener la licencia de contenido separada de la del código.
* Caminreal: el apartado de licencia de la ficha consultada no declara una licencia concreta. No se autoriza desde esta auditoría copiar la edición ni sus imágenes; conservar enlaces y obtener aclaración o permiso antes de reproducir material protegido.
* Sinarcas: el editor indexa CC BY-NC-SA 4.0; falta verificar el alcance en el PDF completo y créditos de imágenes. No importar por ahora.
* Hesperia: la consulta directa no se pudo completar en esta sesión. Identificadores, ediciones y licencia de cada recurso quedan pendientes. El acceso público no implica permiso de extracción o redistribución de la base.

La antigüedad del texto no elimina los posibles derechos de ediciones modernas, imágenes y bases de datos. La LPI contempla protecciones diferenciadas (arts. 10, 32, 41, 129 y 133); la cita no constituye una licencia general para republicar un corpus.

## Entregas y dependencias

1. Registrar fuentes, convenciones y derechos → aprobar esquema sin datos de ejemplo ficticios.
2. Preparar una ficha de Caminreal o Mas Castellar → revisión especializada documentada y derechos resueltos.
3. Incorporar una segunda ficha → validar diferencias entre división gráfica, restauración y segmentación atribuida.
4. Añadir alternativas de Sinarcas → revisión de todas las lecturas, nunca resolver controversias automáticamente.

Controles: localizador por afirmación, compatibilidad de licencias, correspondencia de unidades con edición, conservación de variantes, generador reproducible, enlaces estables, consulta sin JavaScript, teclado, móvil/escritorio y regresión del corpus existente. Cada incorporación requiere una revisión propia antes de producción.

## Referencias verificadas y límites

* Simón Cornago, I. (2015), Palaeohispanica 15, 87–127. [Artículo y condiciones](https://ifc-ojs.es/index.php/palaeohispanica/en/article/view/39). DOI: 10.36707/palaeohispanica.v0i15.39. La fecha de carga OJS no sustituye el año del volumen.
* Ferrer i Jané, J. et al. (2025), Palaeohispanica 25, 175–202. [Artículo y licencia](https://ifc-ojs.es/index.php/palaeohispanica/en/article/view/703). DOI: 10.36707/palaeohispanica.v25i1.703.
* Quixal Santos, D.; Ferrer i Jané, J.; Iranzo Viana, P. (2024), Archivo de Prehistoria Levantina 35, 157–184. [Editor](https://mupreva.org/web_mupreva_dedalo/publicaciones/1626/es). Solo se ha podido contrastar contenido indexado; no se presenta como cotejo íntegro del PDF.
* [Hesperia](https://hesperia.ucm.es/); [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.es); [LPI, texto consolidado](https://www.boe.es/buscar/act.php?id=BOE-A-1996-8930).
