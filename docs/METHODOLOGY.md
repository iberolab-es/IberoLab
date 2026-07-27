# Metodología

## 1. Separación de capas

IberoLab debe mantener separadas cuatro capas para evitar confundir operaciones distintas:

1. **Entrada ortográfica:** texto moderno tal como lo introduce el usuario.
2. **Normalización fonética:** representación aproximada de los sonidos relevantes.
3. **Adaptación paleohispánica:** aplicación de las restricciones del signario elegido.
4. **Renderizado:** selección y dibujo de los signos correspondientes.

La salida final deberá permitir inspeccionar las capas intermedias.

## 2. Clasificación de resultados

Cada resultado deberá identificarse como una de estas categorías:

- **Transliteración:** conversión entre sistemas de escritura sin cambiar la lengua.
- **Representación fonética experimental:** adaptación de sonidos modernos a un signario antiguo.
- **Reconstrucción hipotética:** propuesta sustentada en una hipótesis explícita.
- **Recreación artística:** salida visual sin pretensión filológica.

La interfaz no utilizará la palabra «traducción» para una operación que pertenezca a otra categoría.

## 3. Estrategia corpus-first

La validación no comenzará con nombres personales ni topónimos modernos. Antes de aceptar entradas libres, IberoLab deberá reconstruir formas ya atestiguadas en publicaciones epigráficas o numismáticas.

Cada forma del corpus deberá conservar por separado:

- lectura o transliteración publicada;
- segmentación grafemática;
- contexto de aparición;
- fuente verificable;
- confianza de lectura;
- estado de interpretación semántica.

Una lectura contrastada no implica necesariamente una traducción segura. El significado se modelará como una dimensión independiente de la lectura.

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

El primer inventario gráfico se limitará a los signos exigidos por el corpus contrastado. No se completará artificialmente el signario con figuras sin procedencia.

## 5. Reutilización del prototipo HTML

Del prototipo HTML anterior pueden conservarse:

- el funcionamiento autónomo sin dependencias externas;
- el renderizado SVG inline;
- la salida por tokens;
- la lectura técnica;
- la adaptación a pantallas móviles.

Sus trazados SVG no se reutilizarán como datos paleográficos porque no estaban asociados a una fuente, un alógrafo, una cronología ni una licencia verificable.

## 6. Motor de similitud

El motor para entradas modernas solo se desarrollará después de reconstruir el corpus contrastado. No buscará una supuesta traducción, sino una adaptación explicable mediante:

1. normalización fonética de la entrada;
2. segmentación según las clases representables por el signario;
3. comparación con secuencias y patrones atestiguados;
4. penalización de sustituciones sin equivalente directo;
5. generación de alternativas cuando exista ambigüedad;
6. explicación y nivel de confianza de cada resultado.

La similitud no autoriza a atribuir significado ibérico a una palabra moderna.

## 7. Ambigüedad

Cuando una secuencia moderna admita varias adaptaciones plausibles, el motor no deberá ocultarlo. Podrá:

- mostrar varias alternativas;
- explicar la regla aplicada;
- asignar un nivel de confianza;
- permitir al usuario escoger una variante.

## 8. Validación mínima

Antes de publicar una versión se comprobarán:

- reconstrucción no vacía de todas las formas del corpus contrastado;
- correspondencia entre tokens internos y SVG verificados;
- comportamiento consistente en iOS Safari y navegadores de escritorio;
- accesibilidad mediante texto alternativo o lectura técnica;
- ausencia de dependencias externas que impidan mostrar los signos;
- documentación de todas las sustituciones fonéticas;
- imposibilidad de confundir lectura, interpretación y adaptación moderna.

## 9. Reproducibilidad

Toda modificación del motor, del corpus o de la base de signos deberá quedar versionada. Un mismo texto, configuración y versión del motor deben producir el mismo resultado.
