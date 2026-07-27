# Renderizador provisional de formas contrastadas

## Objetivo

Este renderizador permite comprobar que las lecturas del corpus se convierten en una secuencia visual no vacía antes de construir el motor para palabras modernas.

No reproduce el ductus exacto de cada inscripción. Utiliza formas de referencia del signario ibérico nororiental dual para verificar la cadena técnica:

`forma atestiguada → segmentación publicada → token → signo visible`

## Recursos gráficos

La primera prueba visual utiliza la serie **Sign Iber Noro Dual 01–38**, publicada por BotaFlo en Wikimedia Commons bajo CC0 y descrita como un signario ibérico nororiental dual basado en Ferrer & Jané.

Las imágenes se cargan mediante la redirección estable de Wikimedia Commons. La interfaz mantiene siempre un recuadro textual visible si una imagen no se carga, de modo que nunca vuelva a producir una salida completamente vacía.

## Limitación `ń`

La transcripción reciente `taŕśabań` contiene `ń`. El corpus conserva la lectura publicada, pero el renderizador no le asigna provisionalmente el signo `n`, `m` o `ḿ` sin revisar la forma exacta en la publicación de 2025. La interfaz muestra un bloque de “signo pendiente de verificación” en lugar de ocultarlo o inventarlo.

## Reutilización del HTML anterior

Se han recuperado sus decisiones técnicas útiles:

- un solo documento HTML;
- JavaScript inline;
- renderizado por tokens;
- salida visible desde la carga inicial;
- lectura técnica;
- diseño responsive.

No se reutilizan sus antiguos trazados SVG experimentales.

## Estado

Este componente es una **prueba de referencia**, no la beta pública definitiva. La siguiente revisión deberá vincular cada forma a los alógrafos concretos de su inscripción o, cuando no sea viable, declarar expresamente que se muestra una forma tipográfica normalizada.
