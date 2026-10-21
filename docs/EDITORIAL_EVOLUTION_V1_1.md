# Evolución divulgativa v1.1 — propuesta de desarrollo

Estado: propuesta revisable, pendiente de autorización para producción. No cambia corpus, signos, reglas del conversor ni perfil sonoro v3. No implica validación científica integral ni respaldo institucional.

## Auditoría y línea base

Base: `db1ee9a2991136a456ca0ad26c45c4f6078bd076`, recuperada de `main` el 21/10/2026, sin modificaciones locales previas. Trece validadores correctos antes de intervenir.

Sitio estático en `docs/`, HTML/CSS/JavaScript sin framework, servidor de aplicación ni empaquetador. GitHub Pages publica `docs/` con `.nojekyll`. Actions ejecuta validadores Python y Playwright 1.62.0 con Chromium, Firefox y WebKit. Las dependencias de pruebas no son dependencias de producción.

`mvp-converter.js` aplica reglas deterministas al español; `converter-ui.js` controla entrada, avisos e historial; `corpus-renderer.js` representa las once formas; `corpus-voice.js` e `iberian-voice.js` conservan la procedencia de las secuencias. Web Speech proporciona la voz fluida y Web Audio la técnica. `data/` contiene contratos, corpus y manifiestos. Los SVG son locales: 19 recursos del corpus, 38 del demostrador y 39 tokens sonoros con `ń`.

| Lugar | Antes | Después |
| --- | --- | --- |
| Cabecera, metadatos y tarjeta social | Lengua ibérica, patrimonio y tecnología | Descubre la escritura ibérica; alcance nororiental visible |
| Portada | Conversor tras presentación genérica | Conversor inmediatamente después de cabecera, contexto a continuación |
| Historia | Tarjetas generales sin citas junto a los hechos | Recorrido con localizadores bibliográficos y ampliación opcional |
| Conversor | Signario impreciso en primera explicación | Nororiental de referencia dual, procedimiento, ejemplos y límites |
| Página académica | Público y validez poco delimitados | Documentación para examen especializado; sin utilidad científica acreditada |
| Móvil | Navegación secundaria oculta por CSS | Enlaces disponibles en varias filas, foco y salto al contenido |
| Citación | Enlace local a archivo ausente de `docs/` | Enlace al archivo real del repositorio |

## Diseño y prioridades

P0: objetivo reconocible, conversor destacado y límites en primera pantalla. P1: contexto documentado, ejemplos reproducibles, navegación accesible y acceso especializado. P2: propuesta modular para otros sistemas sin activarlos.

«Conversor experimental de escritura» describe la interacción; «adaptación gráfico-fonética del español moderno» precisa la operación. No es una transliteración reversible, traducción ni transcripción arqueológica. Se conserva «adaptación fonética experimental» como clasificación técnica del resultado.

Los 38 signos son una selección operativa, no un inventario exhaustivo ni un estándar universal. Corpus, normalización gráfica y audio conservan sus límites y convenciones anteriores.

## Fuentes

- Moncunill Martí y Velaza Frías (2020), *Iberian*, Palaeohispanica 20, 591–629: §§1.1–1.2, 1.4–1.5 y 2.1. [PDF](https://ifc.dpz.es/recursos/publicaciones/38/77/17moncunillvelaza.pdf).
- Ferrer i Jané (2020), *Las escrituras epicóricas de la Península Ibérica*, Palaeohispanica 20, 969–1016: §1.1 y §2.1.1. [PDF](https://ifc.dpz.es/recursos/publicaciones/38/77/27ferrer.pdf).
- [Hesperia](https://hesperia.ucm.es/) se enlaza como recurso institucional; no se importan registros ni se inventan identificadores. Su disponibilidad no se usa como evidencia de un hecho.

Se citan páginas y apartados. La ficha editorial de Ferrer y su PDF muestran DOI distintos; aquí se conserva el enlace al texto examinado sin dar la discrepancia por resuelta.

## Validación y límites

Se repiten los trece validadores y la regresión funcional. Las nuevas pruebas examinan divulgación, teclado, navegación móvil y desbordamientos; la matriz conserva corpus, adaptación y voz. CI guarda capturas de las cinco páginas principales y comparación de portada contra la base del PR. El resultado definitivo será el de los controles del PR.

No cambian reglas, corpus, manifiestos, SVG de signos ni audio. Se verifica por diff contra la base, además de las pruebas de ejemplos. La regresión técnica no acredita exactitud paleográfica, accesibilidad completa ni pronunciación histórica. Las pruebas de audio con dobles controlan comportamiento, no la audición humana.

La publicación desde `main` no debe alterarse por abrir esta propuesta. Integración y despliegue requieren autorización del responsable del proyecto. Ampliación futura: [RESEARCH_SCOPE.md](RESEARCH_SCOPE.md).
