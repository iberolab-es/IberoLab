# Alcance de investigación

## Propuesta modular v1.1 — todavía no implementada

Solo está disponible el nororiental actual. La clasificación de partida se contrasta con Ferrer i Jané (2020), *Las escrituras epicóricas de la Península Ibérica*, introducción y apartados de cada sistema: [PDF](https://ifc.dpz.es/recursos/publicaciones/38/77/27ferrer.pdf). Las prioridades siguientes son decisiones técnicas de proyecto, sujetas a revisión.

| Prioridad | Candidato | Riesgo que resolver | Dependencias |
| --- | --- | --- | --- |
| P0 | Registro de sistemas y variantes | El mapa actual está fijado en código | Contrato, migración compatible y pruebas de aislamiento |
| P1 | Nororiental no dual | Heredar distinciones del dual que no corresponden | Inventario propio, pérdidas explícitas y revisión especializada |
| P2 | Greco-ibérico | Forzar agrupación silábica en un módulo alfabético | Repertorio documentado, licencia y reglas independientes |
| P3 | Celtibérico | Confundir signos similares con identidad de lengua | Corpus separado, definir utilidad y revisión por especialista |
| P4 | Ibérico suroriental | Copiar valores nororientales donde hay incertidumbre | Valores revisados por signo, alternativas y bloqueo de lo no resuelto |
| P5 | Sudoeste y otros | Presentar como resuelto un sistema discutido | Empezar por visor documental; evaluar aparte entradas libres |

Cada módulo propuesto tendrá `script_id`, `variant_id`, versión, dirección, inventario, clases de signos, reglas, convenciones, fuentes, licencia, estado de revisión e incertidumbres. Los signos se identificarán por sistema: una etiqueta latina no será una equivalencia global.

El renderizador consumirá identificadores y recursos locales; la adaptación se seleccionará por módulo y podrá bloquear operaciones no documentadas. El audio necesitará perfil propio y tokens del sistema elegido, conservando la procedencia de cada secuencia. El corpus no se generará desde el conversor moderno.

Codificación: mantener identificadores estables, texto accesible y SVG trazables. Antes de exportar Unicode, comprobar cobertura real de la versión vigente, fuentes disponibles y pérdidas. No se afirma aquí que exista una codificación completa; no se usarán semejanzas visuales ni puntos privados como equivalencias históricas.

Puertas de activación, en orden: fuentes primarias y repertorio revisado; derechos de cada activo; reglas y casos bloqueados propios; revisión especializada del módulo; regresión y prototipo aislado; autorización para publicar. La disponibilidad pública de una imagen no permite asumir su reutilización. No se estima un plazo sin conocer inventario y disponibilidad de especialistas. Ninguna observación editorial sustituye esas puertas.

## Sistemas inicialmente contemplados

IberoLab deberá tratar cada sistema de escritura como un conjunto independiente de datos y reglas. El alcance previsto incluye:

- ibérico nororiental;
- ibérico meridional;
- greco-ibérico;
- celtibérico.

La incorporación de otros sistemas requerirá una propuesta específica y documentación separada.

## Datos aceptables

Podrán incorporarse:

- repertorios de signos y variantes;
- valores fonéticos o silábicos propuestos;
- convenciones de transliteración;
- dirección y disposición de escritura;
- procedencia epigráfica;
- referencias bibliográficas y catálogos;
- imágenes o SVG con licencia compatible;
- hipótesis académicas claramente atribuidas.

## Datos que no deben mezclarse

- signos de sistemas distintos presentados como equivalentes sin justificación;
- grafías modernas inventadas etiquetadas como históricas;
- traducciones semánticas no demostrables;
- reconstrucciones propias presentadas como consenso;
- recursos gráficos sin procedencia o licencia conocida.

## Modelo de procedencia

Cada dato lingüístico o gráfico deberá registrar:

- autor o entidad de la fuente;
- título o catálogo;
- fecha o edición cuando sea conocida;
- localizador estable;
- licencia o condición de uso;
- fecha de incorporación al proyecto;
- responsable de la revisión;
- nivel de evidencia.

## Política de incertidumbre

La incertidumbre forma parte del dato. No se resolverá de manera silenciosa. Las variantes y lecturas discutidas deberán conservarse como alternativas relacionables y no como una única respuesta definitiva.
