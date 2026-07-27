# Revisión del prototipo HTML anterior

## Elementos reutilizables

El prototipo autónomo anterior demostró decisiones técnicas útiles:

- un único HTML sin dependencias;
- SVG inline para evitar fuentes ausentes en iOS;
- salida de lectura técnica;
- interfaz adaptable a móvil;
- renderizado por tokens.

Estas decisiones pueden reutilizarse en la futura beta.

## Elementos que no deben reutilizarse como datos científicos

Los trazados SVG del prototipo fueron creados como aproximaciones visuales y no incluían:

- referencia paleográfica individual;
- identificación de alógrafo;
- inscripción o ceca de procedencia;
- cronología;
- dirección original;
- licencia o autoría gráfica verificable.

Por ello, no se incorporan a la base de signos ni se consideran grafías ibéricas contrastadas.

## Decisión

Se conservará la **arquitectura de renderizado**, pero se reemplazará completamente la **base gráfica**. Cada nuevo SVG deberá vincularse a un registro del inventario y a una fuente documental.
