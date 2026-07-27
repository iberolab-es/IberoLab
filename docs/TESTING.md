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

## Privacidad

La prueba se ejecuta localmente en el navegador. No envía los resultados a ningún servidor de IberoLab. El informe solo sale del dispositivo cuando la persona lo copia y lo aporta voluntariamente.

## Estados de la matriz

- `pending`: no probado.
- `partial_pass`: existe una comprobación limitada, pero falta revisar todo el corpus o todos los criterios.
- `pass`: prueba completa registrada y sin incidencias conocidas.
- `fail`: incidencia reproducible pendiente de corrección.

## Criterio de avance

La fase de navegadores no se considera completa hasta registrar pruebas satisfactorias en Safari iOS, Chrome, Firefox y Edge de escritorio. Superar el diagnóstico técnico no sustituye la revisión paleográfica externa.
