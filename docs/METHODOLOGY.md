# Metodología

## 1. Separación de capas

IberoLab debe mantener separadas cuatro capas para evitar confundir operaciones distintas:

1. **Entrada ortográfica:** texto moderno tal como lo introduce el usuario.
2. **Normalización fonética:** representación aproximada de los sonidos relevantes.
3. **Adaptación paleohispánica:** aplicación de las restricciones del signario elegido.
4. **Renderizado:** selección y dibujo de los signos correspondientes.

La salida final deberá permitir inspeccionar las capas intermedias.

Cuando la lectura técnica se convierta en audio, se añadirá una quinta capa independiente:

5. **Recreación acústica:** síntesis moderna y versionada de los valores convencionales de los tokens, sin atribuir al resultado prosodia ni pronunciación histórica.

La recreación acústica admite dos orígenes, que deben conservar etiquetas distintas:

- **forma ibérica atestiguada:** la secuencia escrita procede del corpus documentado, pero su sonorización es experimental;
- **entrada española moderna:** la secuencia procede de la adaptación del demostrador y no constituye vocabulario ibérico ni traducción.

## 2. Clasificación de resultados

Cada resultado deberá identificarse como una de estas categorías:

- **Transliteración:** conversión entre sistemas de escritura sin cambiar la lengua.
- **Representación fonética experimental:** adaptación de sonidos modernos a un signario antiguo.
- **Reconstrucción hipotética:** propuesta sustentada en una hipótesis explícita.
- **Recreación artística:** salida visual sin pretensión filológica.

La interfaz no utilizará la palabra «traducción» para una operación que pertenezca a otra categoría.

## 3. Estrategia corpus-first

La validación no comienza con nombres personales ni topónimos modernos. Antes de aceptar entradas libres, IberoLab reconstruye formas ya atestiguadas en publicaciones epigráficas o numismáticas.

Cada forma del corpus conserva por separado:

- lectura o transliteración publicada;
- segmentación grafemática;
- contexto de aparición;
- fuente verificable;
- confianza de lectura;
- estado de interpretación semántica.

Una lectura contrastada no implica necesariamente una traducción segura. El significado se modela como una dimensión independiente de la lectura.

La reconstrucción técnica del corpus inicial es condición necesaria, pero no suficiente, para publicar adaptación de entradas modernas. También se requieren una especificación fonética explícita, pruebas multidispositivo actuales y revisión externa suficiente de la base gráfica.

## 4. Inventario de signos

Cada signo o variante deberá incluir, como mínimo:

- identificador estable;
- sistema de escritura;
- familia o serie;
- valor o valores propuestos;
- forma SVG o referencia gráfica;
- dirección de escritura compatible;
- procedencia o contexto documental;
- cronología cuando esté disponible;
- fuente bibliográfica;
- licencia o procedencia del recurso gráfico;
- nivel de evidencia;
- observaciones y variantes relacionadas.

El primer inventario gráfico se limita a los signos exigidos por el corpus contrastado. No se completa artificialmente el signario con figuras sin procedencia.

Cuando la transcripción y el nombre paleográfico no coincidan, se registrarán como campos distintos. El caso `m1` / `m` / `ń` constituye el modelo actual: variante paleográfica, transcripción histórica y transcripción adoptada no son conceptos intercambiables.

## 5. Reutilización del prototipo HTML

Del prototipo HTML anterior pueden conservarse:

- el funcionamiento autónomo sin dependencias gráficas remotas durante la navegación;
- el renderizado por recursos SVG controlados;
- la salida por tokens;
- la lectura técnica;
- la adaptación a pantallas móviles.

Sus trazados SVG no se reutilizan como datos paleográficos porque no estaban asociados a una fuente, un alógrafo, una cronología ni una licencia verificable.

## 6. Motor de similitud

La reconstrucción del corpus inicial permite comenzar la **especificación formal** del motor, pero no autoriza todavía a publicar un conversor. La especificación deberá definir de manera versionada:

1. representación fonética interna de la entrada;
2. inventario de rasgos relevantes;
3. segmentación según las clases representables por el signario;
4. reglas y costes de sustitución, inserción, pérdida o aproximación;
5. comparación con secuencias y patrones atestiguados;
6. generación de alternativas cuando exista ambigüedad;
7. cálculo determinista de confianza;
8. explicación legible de cada transformación.

La implementación pública permanecerá bloqueada hasta completar las pruebas manuales actuales del renderizador, fijar el modelo mínimo de alógrafos y obtener revisión externa suficiente.

La similitud no autoriza a atribuir significado ibérico a una palabra moderna.

## 7. Ambigüedad

Cuando una secuencia moderna admita varias adaptaciones plausibles, el motor no deberá ocultarlo. Podrá:

- mostrar varias alternativas;
- explicar la regla aplicada;
- asignar un nivel de confianza;
- permitir al usuario escoger una variante.

Una elección del usuario no convierte una hipótesis en lectura documentada.

## 7.1. Recreación sonora

La recreación sonora recibe como entrada una secuencia inspeccionable de tokens: una lectura atestiguada del corpus o la secuencia ya adaptada por el demostrador, nunca una traducción inferida. Debe funcionar sin transmitir la entrada a IberoLab y declarar por separado:

- valores convencionales con consenso relativo;
- hipótesis fonéticas discutibles;
- convenciones propias del proyecto;
- decisiones puramente acústicas, como timbre, tono, duración, pausas y contorno melódico.

El perfil vigente ofrece una voz fluida moderna, dependiente de la voz instalada en el dispositivo, y conserva un modo técnico determinista. Si se utiliza la fonética o la ortografía de una lengua moderna como paleta articulatoria, debe explicarse que no supone parentesco, descendencia ni continuidad histórica.

La variante `m1`, transcrita por el proyecto como `ń`, se conserva como token propio. La voz fluida la aproxima mediante `n` y la síntesis técnica mediante una nasal prolongada; son decisiones audibles de baja confianza y no valores históricos establecidos.

La interfaz utilizará «recreación sonora experimental», «voz fluida moderna» o «lectura sintética de los signos». No utilizará «pronunciación auténtica», «audio en ibérico», «acento ibérico histórico» ni formulaciones equivalentes. La configuración se documenta en [`EXPERIMENTAL_VOICE.md`](EXPERIMENTAL_VOICE.md), `data/engine/experimental-voice-profile.v3.json` y los perfiles preservados `data/engine/experimental-voice-profile.v2.json` y `data/engine/experimental-voice-profile.v1.json`.

## 8. Validación mínima

Antes de publicar una versión con entradas modernas se comprobarán:

- reconstrucción no vacía de todas las formas del corpus contrastado;
- correspondencia entre tokens internos y SVG verificados;
- comportamiento consistente en Safari/iOS y navegadores de escritorio reales;
- accesibilidad mediante texto alternativo o lectura técnica;
- ausencia de dependencias externas que impidan mostrar los signos;
- documentación de todas las sustituciones fonéticas;
- imposibilidad de confundir lectura, interpretación y adaptación moderna;
- determinismo del resultado para una misma versión y configuración;
- alternativas visibles cuando dos soluciones tengan costes comparables;
- revisión externa de la base documental y gráfica utilizada.

Las pruebas automatizadas en Chromium, Firefox y WebKit son regresión técnica, no sustituyen las pruebas manuales de navegadores de marca ni la revisión paleográfica.

## 9. Reproducibilidad

Toda modificación del motor, del corpus o de la base de signos deberá quedar versionada. Un mismo texto, configuración y versión del motor deben producir el mismo resultado.

Las reglas, pesos y tablas de correspondencia no podrán cambiar silenciosamente. Cada resultado futuro deberá incluir, como mínimo, la versión del corpus, la versión del inventario gráfico, la versión de las reglas y las opciones aplicadas.
