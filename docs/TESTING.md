# Pruebas de navegador

IberoLab mantiene una matriz versionada de pruebas en `data/tests/browser-matrix.v1.json` y una página pública de autodiagnóstico en:

`https://iberolab-es.github.io/IberoLab/test.html`

## Qué comprueba el autodiagnóstico

- que están declaradas las once formas del corpus;
- que los dieciocho SVG normalizados pueden cargarse en el navegador actual;
- que ninguna forma queda sin salida visible;
- que `ń` sigue siendo el único token deliberadamente pendiente;
- que puede generarse un informe reproducible con navegador, fecha y resultados.

## Qué no comprueba

- la exactitud paleográfica del alógrafo seleccionado;
- la fidelidad del recurso gráfico a una inscripción concreta;
- la validez semántica de una interpretación;
- la futura adaptación de palabras modernas.

## Procedimiento manual

1. Abrir `test.html` en el dispositivo y navegador que se desea revisar.
2. Pulsar **Comprobar las 11 formas**.
3. Confirmar que el resultado global indica prueba superada.
4. Revisar visualmente las once filas.
5. Pulsar **Copiar informe**.
6. Adjuntar el JSON a la issue #6, indicando cualquier anomalía visual que la prueba automática no detecte.

## Resultados registrados

### Safari en iPhone — prueba completa satisfactoria

El 27 de julio de 2026 se registró una ejecución completa proporcionada por la persona propietaria del repositorio:

- 11 de 11 formas evaluadas;
- 18 de 18 SVG cargados;
- 0 recursos gráficos fallidos;
- 0 salidas vacías;
- `ń` conservado como único token explícitamente pendiente en `taŕśabań`;
- diseño responsive y contenido legible en las capturas aportadas.

El informe íntegro se conserva en `data/tests/reports/2026-07-27-safari-ios-iphone.json`. La versión y el token de sistema operativo se registran exactamente como los declara el `user_agent`; no se reinterpretan como identificación inequívoca de la versión instalada.

Esta prueba no cubre todavía los enlaces profundos por identificador y deberá repetirse cuando los SVG remotos sean sustituidos por recursos locales.

### Chrome, Brave y Edge en iPhone con «sitio de escritorio»

El mismo día se registraron tres ejecuciones completas adicionales desde Chrome, Brave y Edge en iPhone solicitando la presentación de escritorio. Las tres obtuvieron:

- 11 de 11 formas evaluadas;
- 18 de 18 SVG cargados;
- 0 recursos fallidos;
- 0 salidas vacías;
- `ń` como único token pendiente esperado.

Los informes se conservan en:

- `data/tests/reports/2026-07-27-chrome-ios-desktop-mode.json`;
- `data/tests/reports/2026-07-27-brave-ios-desktop-mode.json`;
- `data/tests/reports/2026-07-27-edge-ios-desktop-mode.json`.

Estas ejecuciones se clasifican como pruebas de **iOS en modo de presentación de escritorio**, no como pruebas de navegador de ordenador. Sus cadenas `user_agent` declaran `AppleWebKit/605.1.15`; por ello no sustituyen las pruebas pendientes de Chrome, Firefox y Edge ejecutados realmente en escritorio.

## Privacidad

La prueba se ejecuta localmente en el navegador. No envía los resultados a ningún servidor de IberoLab. El informe solo sale del dispositivo cuando la persona lo copia y lo aporta voluntariamente.

El informe versionado incluye metadatos técnicos del navegador facilitados voluntariamente para reproducibilidad, pero no incorpora dirección IP, identificadores de cuenta ni datos personales declarados por la aplicación.

## Estados de la matriz

- `pending`: no probado.
- `partial_pass`: existe una comprobación limitada, pero falta revisar todo el corpus o todos los criterios.
- `pass`: prueba completa registrada y sin incidencias conocidas.
- `fail`: incidencia reproducible pendiente de corrección.

## Criterio de avance

La fase de navegadores no se considera completa hasta registrar pruebas satisfactorias en Safari iOS y en Chrome, Firefox y Edge ejecutados realmente en un ordenador. Las pruebas de aplicaciones iOS con «sitio de escritorio» amplían la cobertura móvil, pero no cubren los motores ni el entorno de escritorio. Superar el diagnóstico técnico no sustituye la revisión paleográfica externa.
