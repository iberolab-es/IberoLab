# Corpus inicial de formas ibéricas atestiguadas

## Decisión de diseño

IberoLab no empieza probando nombres personales o topónimos modernos. El primer renderizador se valida con secuencias que ya aparecen en estudios epigráficos o numismáticos.

La secuencia de trabajo es:

1. registrar una lectura académica con su fuente;
2. segmentarla en signos de la escritura utilizada;
3. vincular cada token a un recurso gráfico controlado;
4. comprobar que la forma completa se reconstruye sin vacíos;
5. mantener separadas lectura, variante paleográfica, interpretación y representación normalizada;
6. solo entonces especificar una adaptación por similitud para entradas modernas.

## Qué valida este corpus

El corpus inicial valida **lecturas y segmentaciones**, no traducciones completas. Distingue:

- nombres propios identificados;
- leyendas monetales y topónimos;
- términos con interpretación contextual;
- hipótesis semánticas;
- secuencias cuyo significado continúa discutido.

Una forma reconstruida gráficamente no implica que la web reproduzca el alógrafo exacto de cada objeto arqueológico.

## Formas iniciales

| Forma | Tipo | Estado semántico | Uso en IberoLab |
|---|---|---|---|
| `ildiŕda` | leyenda monetal toponímica | referente identificado | prueba de vocal, lateral, dental dual y vibrante |
| `erder` | marca de valor | hipótesis apoyada: 1/2 | prueba de dental y secuencia cerrada |
| `undikesken` | leyenda monetal/étnica | referente identificado | prueba repetida de `ke` |
| `ars` | leyenda de ceca | referente identificado | prueba alfabética breve |
| `ekiar` | término formular | autoría/producción contextual | prueba de `ki` |
| `egiar` | variante formular | variante documentada | contraste `ki`/`gi` |
| `likine` | antropónimo | nombre identificado | prueba de secuencia mixta |
| `taŕśabań` | antropónimo | nombre y propietario identificados | prueba de `ŕ`, `ś` y de la variante paleográfica `m1` transcrita `ń` |
| `baisetaś` | antropónimo funerario | nombre identificado | prueba de `ba`, `ta` y `ś` |
| `seltar` | término funerario | interpretación contextual: tumba/monumento | prueba de secuencia funeraria |
| `ebanen` | término formular funerario | significado discutido | prueba sin forzar traducción |

## Inventario mínimo actual

Las once formas requieren **diecinueve tokens** de transcripción. Cada uno se vincula a uno de los **diecinueve recursos SVG locales** registrados en:

- `data/signs/minimum-inventory.v1.json`;
- `data/signs/reference-standard-dual.v1.json`;
- `data/signs/reference-standard-dual.assets.v1.json`.

El inventario mínimo ya no contiene estados gráficos pendientes. Sin embargo, dieciocho recursos siguen siendo formas normalizadas de signario y **no son facsímiles** de todos los testimonios donde aparecen.

El token `ń` se documenta de forma especial:

- variante paleográfica: `m1`;
- transcripción tradicional: `m`;
- transcripción adoptada por IberoLab: `ń`;
- alcance gráfico: referencia normalizada m1, no facsímil del escifo.

Esta separación evita identificar silenciosamente `ń` con `n`, `m` o `ḿ`.

## Regla crítica

Que una forma tenga una lectura estable no implica que su significado esté completamente resuelto. El sistema debe poder mostrar:

- **lectura segura / significado incierto**;
- **lectura segura / interpretación contextual**;
- **lectura e interpretación firmemente identificadas**.

Del mismo modo, que exista un SVG controlado no implica que se haya seleccionado el alógrafo exacto de cada inscripción.

## Fuentes de referencia

La bibliografía completa y las URL persistentes se almacenan dentro de `data/corpus/attested-forms.v1.json`. El corpus se apoya inicialmente en:

- Ferrer i Jané y Giral Royo, sobre `ildiŕda` y `erder`;
- Moncunill y Francès, sobre `ekiar/egiar`;
- Simón Cornago, revisión de la inscripción musiva de Caminreal;
- Ferrer i Jané et al., sobre `taŕśabań` y la variante `m1`;
- Quixal, Ferrer i Jané e Iranzo, revisión de la estela de Sinarcas;
- Moncunill, metodología para nombres comunes ibéricos.

## Próxima etapa

La cobertura técnica del corpus inicial está completa. Las siguientes tareas son:

1. registrar alógrafos específicos y su procedencia cuando la evidencia lo permita;
2. repetir los diagnósticos actuales en móvil y navegadores de ordenador reales;
3. obtener revisión externa especializada;
4. definir formalmente el modelo fonético futuro sin publicar todavía un conversor.

No se incorporan como evidencia los 37 trazados del prototipo HTML anterior, porque no estaban vinculados a variantes paleográficas documentadas.
