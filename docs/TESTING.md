# Pruebas de navegador

IberoLab mantiene una matriz versionada de pruebas en `data/tests/browser-matrix.v1.json` y dos páginas públicas de diagnóstico:

- carga de SVG y reconstrucción del corpus: `https://iberolab-es.github.io/IberoLab/test.html`;
- selección mediante enlaces profundos: `https://iberolab-es.github.io/IberoLab/deep-link-test.html`.

## Diagnóstico del corpus y los SVG

La página `test.html` comprueba:

- que están declaradas las once formas del corpus;
- que los diecinueve SVG de referencia pueden cargarse en el navegador actual;
- que ninguna forma queda sin salida visible;
- que `ń` se renderiza mediante la variante paleográfica m1 documentada y no queda pendiente;
- que puede generarse un informe reproducible con navegador, fecha y resultados;
- que la ejecución corresponde al modo `local_repository`.

## Diagnóstico de enlaces profundos

La página `deep-link-test.html` abre secuencialmente las once URL con fragmento `#id` dentro de un marco del mismo origen y comprueba para cada una:

- que el renderizador termina su inicialización;
- que el fragmento solicitado permanece en la URL;
- que el selector interno adopta el identificador esperado;
- que la lectura visible coincide con la forma asociada;
- que el contenedor de signos no queda vacío;
- que puede copiarse un informe JSON independiente y reproducible.

La prueba utiliza un único marco técnico oculto y procesa las formas de manera secuencial para limitar el consumo de memoria en dispositivos móviles.

## Regresión automática entre motores

El flujo `Browser smoke tests` ejecuta Playwright sobre un servidor HTTP local y prueba la implementación en tres motores:

- Chromium;
- Firefox;
- WebKit.

Para cada motor comprueba las once formas mediante sus identificadores, la selección y lectura visible, el número esperado de tarjetas, la ausencia de tarjetas fallidas y la carga real de cada imagen local. Después ejecuta íntegramente `test.html` y `deep-link-test.html` y exige que ambos informes terminen en `pass`.

La suite utiliza Playwright `1.62.0` fijado, un único trabajador en CI, permisos de solo lectura y conserva trazas y capturas únicamente cuando existe un fallo. Su configuración se encuentra en:

- `.github/workflows/browser-smoke.yml`;
- `playwright.config.cjs`;
- `tests/browser/browser-smoke.spec.cjs`.

Esta cobertura detecta regresiones en Chromium, Firefox y WebKit, pero no equivale a una prueba manual de Google Chrome, Microsoft Edge, Mozilla Firefox instalado en un ordenador o Safari/iOS. Tampoco constituye una comparación visual píxel a píxel.

## Qué no comprueban estas pruebas

- la exactitud paleográfica del alógrafo seleccionado;
- la fidelidad del recurso gráfico a una inscripción concreta;
- la validez semántica de una interpretación;
- la futura adaptación de palabras modernas;
- la apariencia exacta píxel a píxel, que requerirá regresión visual separada.

## Procedimiento manual completo

1. Abrir `test.html` en el dispositivo y navegador que se desea revisar.
2. Pulsar **Comprobar las 11 formas**.
3. Confirmar que el informe indica `version: 1.2.0`, `asset_mode: local_repository` y `result: pass`.
4. Revisar visualmente las once filas y copiar el informe.
5. Abrir `deep-link-test.html` en el mismo navegador.
6. Pulsar **Comprobar los 11 enlaces**.
7. Confirmar que aparecen 11 enlaces correctos, 0 fallidos y 0 salidas vacías.
8. Copiar el segundo informe.
9. Adjuntar ambos JSON a la issue #6, indicando cualquier anomalía visual que las comprobaciones automáticas no detecten.

## Resultados históricos registrados

### Safari en iPhone — implementación remota

El 27 de julio de 2026 se registró una ejecución completa proporcionada por la persona propietaria del repositorio:

- 11 de 11 formas evaluadas;
- 18 de 18 SVG cargados;
- 0 recursos gráficos fallidos;
- 0 salidas vacías;
- `ń` conservado como único token explícitamente pendiente en `taŕśabań`;
- diseño responsive y contenido legible en las capturas aportadas.

El informe íntegro se conserva en `data/tests/reports/2026-07-27-safari-ios-iphone.json`. La versión y el token de sistema operativo se registran exactamente como los declara el `user_agent`; no se reinterpretan como identificación inequívoca de la versión instalada.

Esta evidencia corresponde a la implementación anterior con carga gráfica remota. Se conserva como `partial_pass` y no verifica el despliegue local actual ni los enlaces profundos.

### Chrome, Brave y Edge en iPhone con «sitio de escritorio» — implementación remota

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

Estas ejecuciones se clasifican como pruebas de **iOS en modo de presentación de escritorio**, no como pruebas de navegador de ordenador. Sus cadenas `user_agent` declaran `AppleWebKit/605.1.15`; por ello no sustituyen las pruebas pendientes de Chrome, Firefox y Edge ejecutados realmente en escritorio. También deberán repetirse sobre `asset_mode: local_repository`.

## Privacidad

Las dos páginas públicas se ejecutan localmente en el navegador. No envían los resultados a ningún servidor de IberoLab. Los informes solo salen del dispositivo cuando la persona los copia y los aporta voluntariamente.

Los informes incluyen metadatos técnicos del navegador facilitados voluntariamente para reproducibilidad, pero no incorporan dirección IP, identificadores de cuenta ni datos personales declarados por la aplicación.

## Estados de la matriz

- `pending`: no probado.
- `partial_pass`: existe una comprobación limitada, histórica o incompleta.
- `pass`: prueba completa registrada sobre la implementación actual y sin incidencias conocidas.
- `fail`: incidencia reproducible pendiente de corrección.

## Criterio de avance

La fase de navegadores no se considera completa hasta registrar pruebas satisfactorias de los dos diagnósticos en Safari iOS y en Chrome, Firefox y Edge ejecutados realmente en un ordenador. Las pruebas automatizadas entre motores y las aplicaciones iOS con «sitio de escritorio» amplían la cobertura, pero no sustituyen esos entornos manuales.

Superar los diagnósticos técnicos no sustituye la revisión paleográfica externa. El motor para entradas modernas continúa bloqueado hasta completar la revisión mínima de la base gráfica y la verificación multidispositivo de la implementación local.
