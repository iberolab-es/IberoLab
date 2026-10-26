# Consulta académica del corpus — propuesta de desarrollo

Base auditada el 26/10/2026: `c14bafb84d646c8d4f05a8b511d859106c416e80`. La rama nueva no modifica el despliegue ni se integra sin autorización.

## Diagnóstico verificable

El conjunto `data/corpus/attested-forms.v1.json` contiene once formas aisladas, no once ediciones de inscripciones completas. Sus `grapheme_sequence` son descomposiciones técnicas para el renderizador, no segmentaciones en palabras o morfemas. No existen campos para esas segmentaciones, sus localizadores o una revisión especializada por análisis. Los identificadores son internos y no identificadores de objetos en Hesperia o inventarios arqueológicos.

| Material | Entradas | Alcance |
| --- | --- | --- |
| ildiŕda, erder, undikesken, ars | 4 | Formas en estudio numismático; ejemplares no individualizados en el conjunto |
| ekiar, egiar | 2 | Formas de fórmula discutidas en bibliografía; no ediciones completas |
| likine | 1 | Forma onomástica del mosaico de Caminreal; no transcripción del mosaico completo |
| taŕśabań | 1 | Nombre aislado en el estudio de Mas Castellar; no edición de los dos escifos |
| baisetaś, seltar, ebanen | 3 | Formas de la estela de Sinarcas; no edición integral ni análisis sintáctico resuelto |

La revisión bibliográfica anterior registra presencia de las formas y contexto. No es una validación externa integral ni acredita toda interpretación. `erder` mantiene hipótesis interpretativa; `ebanen`, interpretación discutida; `baisetaś`, nombre identificado con papel sintáctico discutido. La certeza de lectura y el estado interpretativo permanecen separados.

## Acceso y funcionamiento

`corpus.html` muestra todas las fichas directamente, sin GitHub, cuentas ni instalaciones. La portada ofrece un enlace en su navegación y otro en las llamadas principales; `academia.html` prioriza la consulta del corpus. El conversor se conserva en el recorrido divulgativo. El visor anterior y sus enlaces profundos siguen funcionando.

Las fichas contienen identificador interno, transcripción adoptada, tokens grafemáticos, contexto/procedencia de la referencia, soporte o ámbito, límites de identificación de objeto, bibliografía, notas y certeza de lectura diferenciada de interpretación. Ninguna afirma una segmentación lingüística incorporada. No se han añadido lecturas ni traducciones.

Las once fichas existen en el HTML estático incluso sin JavaScript. El script local solo aporta búsqueda tolerante a diacríticos y filtro de interpretación. No realiza segmentación, análisis ni consultas remotas. Los enlaces de índice revelan fichas aunque estuvieran ocultas por un filtro. Los fragmentos internos son estables.

## Datos y generación

El conjunto original permanece intacto. `data/corpus/academic-catalog.v1.json` contiene anotaciones en español tomadas del contexto ya presente en el visor y límites de segmentación explícitos. No sustituye los identificadores internos por códigos arqueológicos inventados.

`scripts/render_academic_catalog.py` genera el HTML a partir del conjunto original y las anotaciones. `scripts/validate_academic_catalog.py` exige cobertura exacta, cero ediciones completas y cero segmentaciones lingüísticas en esta versión y comprueba que el HTML no esté desincronizado. Las cinco pruebas negativas rechazan duplicados, omisiones, códigos de objeto inventados y segmentaciones no documentadas.

## Ampliación gradual pendiente

1. Seleccionar una inscripción cuya edición y condiciones de reutilización puedan comprobarse.
2. Registrar por separado objeto, procedencia, transcripción y tipo de división: separadores visibles en el original, segmentación editorial o hipótesis morfológica.
3. Asociar cada análisis con publicación, página/figura, autoría y estado: documentado, hipotético, discutido o no segmentado.
4. Mantener alternativas y restauraciones explícitas; nunca rellenar huecos con IA.
5. Obtener revisión especializada registrada y ejecutar pruebas antes de publicar la ficha ampliada.

La necesidad de textos ibéricos segmentados sigue abierta. Esta entrega mejora el acceso y la trazabilidad del material real; no afirma satisfacerla con once formas aisladas. Las referencias y fuentes son las ya conservadas en el conjunto original; no se importan textos de bibliotecas, Hesperia ni imágenes sin revisar derechos.

## Validación prevista para el PR

Catorce validadores y cinco pruebas negativas; matriz de navegador con recorrido desde portada y documentación académica, once fichas y referencias, búsqueda/filtros, enlaces profundos, ausencia de JavaScript, teclado y anchos 360/1440. Las capturas se conservan como artefactos de CI. Las pruebas de software no sustituyen revisión filológica ni auditoría integral de accesibilidad.

Las comunicaciones privadas de evaluación y la matriz que distingue sus autores se conservan fuera del repositorio público. No se atribuye aval institucional ni revisión formal de datos.

## Auditoría posterior del PR #41

Se aclara que `likine` y `taŕśabań` son bases onomásticas extraídas por análisis bibliográfico, no transcripciones íntegras de sus grupos inscritos. Las notas identifican páginas y distinguen los vasos de Mas Castellar. El rótulo general «Forma de referencia adoptada» evita atribuir al objeto el recorte de una forma. Se corrige el margen de anclas en tabletas y se añade prueba a 360, 720 y 1440 píxeles.

La propuesta de fichas completas, candidatos, atribuciones, derechos pendientes y dependencias se desarrolla en [FULL_INSCRIPTIONS_PLAN.md](FULL_INSCRIPTIONS_PLAN.md). No incorpora ninguna inscripción ni segmentación nueva.
