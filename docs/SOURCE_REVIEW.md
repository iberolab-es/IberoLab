# Revisión documental del corpus inicial

Fecha de revisión: **28 de julio de 2026**.

## Alcance

Esta revisión comprueba que las once formas del corpus inicial aparecen en publicaciones académicas o repositorios institucionales citados. No valida todavía el alógrafo exacto de cada inscripción ni convierte el renderizador normalizado en un facsímil.

La evidencia se mantiene en tres capas independientes:

1. **Lectura atestiguada:** la secuencia aparece en la fuente.
2. **Contexto e interpretación:** se registra si la propuesta es un nombre, una fórmula, un referente conocido o una hipótesis semántica.
3. **Representación gráfica:** la web usa por ahora formas normalizadas de referencia del signario nororiental dual.

La matriz legible por máquina está en `data/audits/source-review.v1.json` y se valida automáticamente con `scripts/validate_source_audit.py`.

## Resultado por grupos

### Numismática: `ildiŕda`, `erder`, `undikesken`, `ars`

Fuente principal: Ferrer i Jané y Giral Royo, *A propósito de un semis de ildiŕda con leyenda erder*, DOI `10.36707/palaeohispanica.v0i7.277`.

- `ildiŕda` está verificada como lectura empleada por el estudio. El artículo también ofrece para un ejemplar la secuencia puntuada `i.l.ti.ŕ.ta`; la salida `i · l · di · ŕ · da` de IberoLab es una normalización dual, no una reproducción del epígrafe.
- `erder` está verificada. Su interpretación como marca de valor de un medio es una hipótesis apoyada por el contexto monetal, no una traducción léxica absoluta.
- `undikesken` se conserva según la forma usada por el estudio; otras convenciones bibliográficas pueden mostrar variantes como `untikesken`.
- `ars` se registra como el comparador de ceca usado en el estudio, sin afirmar que la secuencia aislada reproduzca la leyenda completa de todos los ejemplares mencionados.

### Fórmulas de autoría: `ekiar`, `egiar`

Fuente principal: Moncunill Martí y Francès, *Un nuevo cálato inscrito de Ca n'Oliver*, identificador persistente `https://hdl.handle.net/2445/217431`.

La publicación caracteriza explícitamente la fórmula mediante `ekiar/egiar`. La función general está contextualizada, pero el análisis gramatical preciso no se presenta como cerrado.

### Caminreal: `likine`

Fuente principal: Simón Cornago, *Treinta años de investigaciones sobre la inscripción musiva de Caminreal*, DOI `10.36707/palaeohispanica.v0i15.39`.

`likine` está verificado como elemento antroponímico central de la inscripción. IberoLab muestra la forma aislada y no pretende reconstruir el mosaico completo.

### Mas Castellar: `taŕśabań`

Fuente principal: Ferrer i Jané et al., *La casa de Taŕśabań*, DOI `10.36707/palaeohispanica.v25i1.703`.

La publicación da la secuencia completa `taŕśabańar` y aísla el antropónimo `taŕśabań`. La lectura está verificada. El token final `ń` permanece sin SVG asignado porque la serie gráfica genérica utilizada por la web no permite identificarlo con seguridad como `n`, `m` o `ḿ`.

### Estela de Sinarcas: `baisetaś`, `seltar`, `ebanen`

Fuente principal: Quixal Santos, Ferrer i Jané e Iranzo Viana, *Nuevas miradas a la estela de Sinarcas desde una perspectiva histórica, cultural y territorial*, Archivo de Prehistoria Levantina 35 (2024), repositorio institucional de la Universitat de València.

- `baisetaś` está verificado como antropónimo; su papel concreto dentro de las alternativas sintácticas del epitafio continúa discutido.
- `seltar` aparece en contexto funerario y se interpreta de forma contextual como tumba o monumento funerario. No se ofrece como equivalencia válida para cualquier contexto.
- `ebanen` está verificado como secuencia, pero su análisis compite entre una posible marca de filiación y una posible forma verbal. IberoLab no le asigna traducción.

## Límites pendientes

- Seleccionar alógrafos específicos para cada testimonio.
- Resolver paleográficamente el token `ń` de `taŕśabań`.
- Integrar SVG locales para eliminar la dependencia de Wikimedia Commons.
- Completar pruebas manuales de las once formas en Safari iOS y en navegadores de escritorio.
- Obtener revisión externa de una persona especialista antes de declarar estable el corpus.

## Regla para el futuro motor

El análisis de similitud para palabras modernas solo podrá usar patrones procedentes de entradas revisadas y deberá mantener separadas:

- la pronunciación moderna de entrada;
- la adaptación fonética;
- la secuencia paleohispánica propuesta;
- el grado de confianza;
- la evidencia documental disponible.

La similitud sonora nunca se utilizará para inferir significado ibérico.
