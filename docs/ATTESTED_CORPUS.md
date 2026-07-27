# Corpus inicial de formas ibéricas atestiguadas

## Decisión de diseño

IberoLab no empezará probando nombres personales o topónimos modernos. El primer renderizador se validará con secuencias que ya aparecen en estudios epigráficos o numismáticos.

La secuencia de trabajo será:

1. registrar una lectura académica con su fuente;
2. segmentarla en signos de la escritura utilizada;
3. seleccionar o dibujar variantes gráficas documentadas;
4. comprobar que la forma completa se reconstruye sin vacíos;
5. solo entonces estudiar una adaptación por similitud para entradas modernas.

## Qué valida este corpus

El corpus inicial valida **lecturas y segmentaciones**, no traducciones completas. Distingue:

- nombres propios identificados;
- leyendas monetales y topónimos;
- términos con interpretación contextual;
- hipótesis semánticas;
- secuencias cuyo significado continúa discutido.

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
| `taŕśabań` | antropónimo | nombre y propietario identificados | prueba de signos especiales `ŕ`, `ś`, `ń` |
| `baisetaś` | antropónimo funerario | nombre identificado | prueba de `ba`, `ta` y `ś` |
| `seltar` | término funerario | interpretación contextual: tumba/monumento | prueba de secuencia funeraria |
| `ebanen` | término formular funerario | significado discutido | prueba sin forzar traducción |

## Regla crítica

Que una forma tenga una lectura estable no implica que su significado esté completamente resuelto. El motor debe poder mostrar:

- **lectura segura / significado incierto**;
- **lectura segura / interpretación contextual**;
- **lectura e interpretación firmemente identificadas**.

## Fuentes de referencia

La bibliografía completa y las URL persistentes se almacenan dentro de `data/corpus/attested-forms.v1.json`. El corpus se apoya inicialmente en:

- Ferrer i Jané y Giral Royo, sobre `ildiŕda` y `erder`;
- Moncunill y Francès, sobre `ekiar/egiar`;
- Simón Cornago, revisión de la inscripción musiva de Caminreal;
- Ferrer i Jané et al., sobre `taŕśabań`;
- Quixal, Ferrer i Jané e Iranzo, revisión de la estela de Sinarcas;
- Moncunill, metodología para nombres comunes ibéricos.

## Próxima etapa

El inventario gráfico se limitará a los signos necesarios para reconstruir estas once formas. No se incorporarán todavía las 37 figuras SVG del prototipo HTML anterior: sus trazados no estaban vinculados a variantes paleográficas documentadas.
