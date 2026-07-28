# Procedencia de los recursos gráficos

## Dos capas independientes

IberoLab mantiene deliberadamente dos inventarios gráficos:

1. **Corpus atestiguado:** 19 recursos necesarios para reconstruir las once formas documentadas del corpus inicial.
2. **Demostrador MVP:** los 38 signos normalizados de la serie nororiental dual, utilizados para adaptar gráficamente entradas españolas breves.

La ampliación práctica no modifica qué tokens están exigidos por el corpus ni convierte la serie normalizada en evidencia de alógrafos concretos.

## Fuente y licencia de la serie normalizada

- Colección: Wikimedia Commons, categoría `Iberian letters`.
- Serie: `Sign Iber Noro Dual 01–38`.
- Autor: BotaFlo.
- Fecha declarada por la fuente: 2022.
- Licencia: CC0 1.0 Universal.
- Base académica indicada por la fuente: signario dual nororiental según Ferrer i Jané (2005).

La atribución se conserva como trazabilidad aunque CC0 no la exija jurídicamente.

## Manifiesto del corpus atestiguado

`data/signs/reference-standard-dual.assets.v1.json` registra 18 archivos de la serie normalizada y la variante nasal m1 utilizada para `ń`.

Para cada recurso conserva:

- token de transcripción;
- identificador estable;
- nombre y página del archivo de origen;
- URL de redirección y URL final resuelta;
- ruta local pública;
- tamaño en bytes;
- hash SHA-256;
- tipo de medio;
- autoría y licencia.

Este manifiesto continúa limitado a 19 recursos porque se deriva del corpus inicial y no del conjunto completo del signario.

## Manifiesto del demostrador MVP

`data/signs/mvp-standard-signary.assets.v1.json` registra los 38 archivos de la serie `Sign Iber Noro Dual 01–38`.

- reutiliza los 18 archivos estándar que ya estaban versionados;
- añade los 20 archivos estándar que faltaban;
- conserva fuente, licencia, tamaño y SHA-256 de cada uno;
- etiqueta todos los trazados como referencias normalizadas y no como facsímiles;
- declara expresamente que no modifica el manifiesto del corpus atestiguado.

Los archivos de ambas capas se sirven desde `docs/assets/signs/northeastern-dual/`. La navegación pública no depende de Wikimedia para mostrar los signos.

## Variante nasal m1

El token `ń` del corpus utiliza `docs/assets/signs/northeastern-dual/variant-m1-nasal.svg`, procedente de `NE Iberian m1.svg`, obra de Vriullop publicada en Wikimedia Commons bajo CC0 1.0.

La publicación de 2025 sobre `taŕśabańar` identifica el signo como variante `m1`: conserva `m` como transcripción tradicional y adopta `ń` para el comportamiento ibérico de nasal marcada no labial. IberoLab registra por separado:

- variante paleográfica: `m1`;
- transcripción histórica: `m`;
- transcripción adoptada por el proyecto: `ń`.

El recurso es una referencia normalizada, no un facsímil del recipiente. Evidencia paleográfica: https://doi.org/10.36707/palaeohispanica.v25i1.703.

## Reproducción y actualización

Para comprobar el estado actual:

```bash
python scripts/validate_local_assets.py
python scripts/validate_renderer.py
python scripts/validate_browser_matrix.py
python scripts/validate_mvp_converter.py
```

El generador `scripts/fetch_mvp_signary.py` solo debe ejecutarse en una rama de revisión con acceso de red. El flujo temporal que incorporó los archivos fue eliminado antes de fusionar; los CI ordinarios mantienen permiso de solo lectura.

Una actualización solo debe aceptarse cuando:

1. cada manifiesto conserva su alcance y número de recursos;
2. las rutas, tamaños y hashes coinciden;
3. los SVG son XML válido y no contienen contenido activo peligroso;
4. el renderizador y el demostrador utilizan exclusivamente rutas locales;
5. la procedencia y la licencia permanecen documentadas;
6. las pruebas automáticas y manuales se repiten.

## Límite científico

La disponibilidad local y la integridad criptográfica prueban la reproducibilidad técnica de un recurso, no su adecuación paleográfica a una inscripción concreta. El demostrador combina formas normalizadas mediante reglas de proyecto para representar sonidos modernos; no reconstruye palabras ibéricas ni selecciona automáticamente el alógrafo arqueológico de un testimonio.
