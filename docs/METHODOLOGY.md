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

## 3. Inventario de signos

Cada signo o variante deberá incluir, como mínimo:

- identificador estable;
- sistema de escritura;
- familia o serie;
- valor o valores propuestos;
- forma SVG o referencia gráfica;
- dirección de escritura compatible;
- procedencia o contexto documental;
- fuente bibliográfica;
- nivel de evidencia;
- observaciones y variantes relacionadas.

## 4. Ambigüedad

Cuando una secuencia moderna admita varias adaptaciones plausibles, el motor no deberá ocultarlo. Podrá:

- mostrar varias alternativas;
- explicar la regla aplicada;
- asignar un nivel de confianza;
- permitir al usuario escoger una variante.

## 5. Validación mínima

Antes de publicar una versión se comprobarán:

- resultados no vacíos para el corpus de prueba;
- correspondencia entre tokens internos y SVG renderizados;
- comportamiento consistente en iOS Safari y navegadores de escritorio;
- accesibilidad mediante texto alternativo o lectura técnica;
- ausencia de dependencias externas que impidan mostrar los signos;
- documentación de todas las sustituciones fonéticas.

## 6. Reproducibilidad

Toda modificación del motor o de la base de signos deberá quedar versionada. Un mismo texto, configuración y versión del motor deben producir el mismo resultado.