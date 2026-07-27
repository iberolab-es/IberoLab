# Procedencia de los recursos gráficos

## Alcance

IberoLab incluye 18 SVG normalizados de referencia del signario ibérico nororiental dual. Se utilizan para reconstruir visualmente las segmentaciones del corpus inicial; no son facsímiles de los alógrafos concretos conservados en cada moneda, cerámica, mosaico o estela.

## Fuente y licencia

- Colección: Wikimedia Commons, categoría `Iberian letters`.
- Serie: `Sign Iber Noro Dual 01–38`.
- Autor de los archivos utilizados: BotaFlo.
- Fecha declarada por la fuente: 2022.
- Licencia: CC0 1.0 Universal.
- Base académica indicada por la propia fuente: signario dual nororiental según Ferrer y Jané (2005).

La atribución se conserva como trazabilidad del proyecto aunque CC0 no la exija jurídicamente.

## Inventario verificable

El archivo `data/signs/reference-standard-dual.assets.v1.json` registra individualmente para cada recurso:

- token de transcripción;
- identificador estable de IberoLab;
- nombre y página del archivo de origen;
- URL de redirección y URL final resuelta durante la descarga;
- ruta local pública;
- tamaño en bytes;
- hash SHA-256;
- tipo de medio;
- autoría y licencia.

Los archivos se sirven desde `docs/assets/signs/northeastern-dual/`. La web pública y el autodiagnóstico no dependen de Wikimedia para mostrar los signos.

## Reproducción y actualización

En una rama de revisión:

```bash
python scripts/vendor_reference_svgs.py
python scripts/integrate_local_assets.py
python scripts/validate_local_assets.py
python scripts/validate_renderer.py
python scripts/validate_browser_matrix.py
```

Una actualización solo debe aceptarse si:

1. se conservan 18 recursos válidos y el manifiesto coincide con sus hashes;
2. no aparecen elementos activos peligrosos en los SVG;
3. el renderizador y la prueba pública emplean exclusivamente rutas locales;
4. la procedencia y la licencia permanecen documentadas;
5. las pruebas automáticas y manuales se repiten.

## Token pendiente

`ń`, utilizado en la transcripción `taŕśabań`, permanece sin recurso gráfico asignado. No se sustituirá por `n`, `m` o `ḿ` hasta verificar de forma específica el signo y la convención de transcripción en la publicación citada de 2025.

## Límite científico

La disponibilidad local y la integridad criptográfica de un SVG prueban la reproducibilidad técnica del recurso, no su adecuación paleográfica a una inscripción concreta. La selección de alógrafos documentados continúa siendo una fase posterior y requiere revisión especializada.
