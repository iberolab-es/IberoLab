# Especificación formal del futuro motor fonético

## 1. Estado y alcance

Este documento define el **contrato estructural** de un futuro motor de adaptación fonética. No implementa reglas español→ibérico, no activa entradas modernas en la web pública y no autoriza el uso de la palabra «traducción».

Estado normativo actual:

- contrato: `data/engine/phonetic-engine-contract.v1.json`;
- esquema de salida: `data/schema/adaptation-result.schema.json`;
- estado: `specification_only`;
- conversión pública: desactivada;
- pesos, perfiles de pronunciación y confianza: no aprobados.

La operación futura se clasificará siempre como **representación fonética experimental**.

## 2. Objetivos

El motor deberá:

1. conservar la entrada original;
2. separar normalización ortográfica, análisis fonético, adaptación paleohispánica y renderizado;
3. utilizar únicamente reglas versionadas;
4. producir una o varias alternativas cuando exista ambigüedad;
5. asignar costes no negativos mediante componentes inspeccionables;
6. explicar cada transformación;
7. vincular todos los tokens y recursos gráficos a versiones concretas;
8. impedir inferencias semánticas a partir de semejanza sonora;
9. impedir salidas vacías o sustituciones silenciosas;
10. ser determinista para la misma entrada, perfil, configuración y conjunto de versiones.

## 3. No objetivos

El contrato no pretende:

- traducir español al idioma ibérico;
- reconstruir vocabulario ibérico no documentado;
- atribuir significado a una secuencia por parecido fonético;
- elegir automáticamente un alógrafo arqueológico exacto;
- ocultar diferencias dialectales del español;
- ofrecer porcentajes de confianza antes de una calibración verificable;
- aprender pesos automáticamente a partir del corpus inicial de once formas.

## 4. Capas obligatorias

### 4.1 Entrada original

Debe conservarse sin alteraciones y acompañada de:

- etiqueta de lengua;
- perfil de pronunciación declarado;
- opciones de normalización;
- versión del contrato.

Ninguna corrección ortográfica podrá aplicarse de forma silenciosa.

### 4.2 Normalización ortográfica

Debe generar:

- texto normalizado;
- lista ordenada de operaciones;
- relación entre cada fragmento normalizado y su posición en la entrada original;
- advertencias sobre ambigüedades o caracteres no admitidos.

Esta capa no contiene todavía fonemas ni signos ibéricos.

### 4.3 Normalización fonética

Debe representar una secuencia ordenada de unidades. Cada unidad incluirá como mínimo:

- índice estable dentro de la secuencia;
- símbolo fonético o identificador de haz de rasgos;
- rasgos relevantes;
- intervalo de origen en el texto;
- certeza del análisis;
- pertenencia silábica;
- información de acento cuando corresponda.

La notación normativa exacta y el inventario de rasgos continúan pendientes de aprobación.

### 4.4 Restricciones del sistema de escritura

La adaptación debe declarar:

- sistema seleccionado;
- perfil de signario;
- inventario de tokens permitido;
- restricciones activas;
- reglas descriptivas sustentadas documentalmente;
- decisiones de ingeniería que no sean afirmaciones paleográficas.

Las dos últimas categorías deberán almacenarse por separado.

### 4.5 Operaciones de adaptación

Cada operación incluirá:

- identificador;
- tipo;
- unidades fonéticas de origen;
- tokens de destino;
- regla aplicada;
- componentes de coste;
- base de evidencia;
- explicación legible.

Tipos estructurales iniciales:

- coincidencia exacta aprobada;
- sustitución de rasgos;
- inserción de segmento;
- eliminación de segmento;
- asociación vocálica;
- reestructuración silábica;
- bifurcación por ambigüedad;
- selección de alógrafo.

Estos nombres definen el contrato, no autorizan todavía ninguna regla concreta.

### 4.6 Candidatos

El motor no garantiza una única salida. Cada candidato deberá conservar:

- secuencia de tokens;
- referencias gráficas;
- operaciones aplicadas;
- coste total;
- confianza;
- explicación paso a paso;
- estado de renderizado.

Los empates exactos no podrán eliminarse arbitrariamente. El umbral para soluciones casi empatadas continúa pendiente.

### 4.7 Renderizado

El renderizado es la última capa y no puede modificar la secuencia lingüística.

Cada token deberá:

- existir en el inventario mínimo versionado;
- enlazar con el mapeo gráfico de la misma versión;
- resolver a un recurso del manifiesto declarado;
- producir un error visible si falta el recurso;
- conservar la distinción entre referencia normalizada y alógrafo específico.

## 5. Modelo de costes

### 5.1 Dominio

Los costes serán números reales no negativos.

### 5.2 Agregación provisional

La agregación inicial prevista es aditiva, pero no se considera aprobada hasta validar:

- independencia o interacción de componentes;
- escala de cada categoría;
- tratamiento de reparaciones múltiples;
- umbral de casi empate;
- estabilidad frente a cambios pequeños de entrada.

### 5.3 Coste cero

Solo una coincidencia exacta sustentada por una regla aprobada podrá tener coste de adaptación cero. La selección gráfica se tratará en una capa separada.

### 5.4 Categorías estructurales

El esquema admite componentes para:

- coincidencia exacta;
- sustitución de rasgos;
- inserción;
- eliminación;
- asociación vocálica;
- reestructuración silábica;
- ausencia en el inventario;
- ambigüedad de perfil;
- elección de alógrafo.

Los pesos permanecen vacíos y no deberán inventarse para producir una demostración visual.

## 6. Confianza

La confianza actual es `not_calibrated`.

Hasta disponer de perfiles aprobados, reglas revisadas, pesos documentados, un conjunto de evaluación suficiente y revisión externa:

- no se mostrarán porcentajes;
- no se utilizarán bandas alta/media/baja;
- el esquema exigirá `numeric_score: null`;
- la explicación deberá indicar que la confianza no está calibrada.

La confianza futura no podrá derivarse únicamente del coste del mejor candidato. Deberá considerar al menos:

- cobertura de reglas;
- calidad de la evidencia;
- ambigüedad fonética de entrada;
- distancia respecto a alternativas;
- número y gravedad de aproximaciones;
- estabilidad frente a perfiles razonables.

## 7. Versionado obligatorio

Cada resultado deberá registrar versiones de:

- motor;
- conjunto de reglas;
- modelo de costes;
- modelo de confianza;
- corpus;
- inventario mínimo;
- mapeo gráfico;
- manifiesto de recursos.

Un cambio en cualquiera de estas dependencias deberá permitir distinguir los resultados antiguos de los nuevos.

## 8. Reproducibilidad

Para una misma combinación de:

- entrada original;
- perfil de pronunciación;
- opciones;
- versiones;
- reglas y pesos;

el motor deberá producir los mismos candidatos, costes, orden y explicaciones.

Cualquier desempate deberá utilizar una regla explícita y versionada; nunca el orden accidental de un diccionario, una respuesta de red o un generador aleatorio sin semilla registrada.

## 9. Gestión de ambigüedad

El motor deberá bifurcar candidatos cuando:

- el perfil de pronunciación permita análisis distintos;
- dos reglas incompatibles tengan evidencia comparable;
- dos secuencias tengan el mismo coste;
- la elección de vocal de apoyo no esté determinada;
- una restricción dependa de una decisión aún no aprobada.

La interfaz futura deberá explicar por qué existen varias alternativas.

## 10. Errores y bloqueos

Constituyen condiciones de bloqueo:

- entrada sin perfil aprobado;
- unidad fonética no representable sin regla de aproximación;
- regla sin identificador o versión;
- token fuera del inventario;
- recurso gráfico ausente;
- coste negativo;
- candidato sin explicación;
- intento de producir una afirmación semántica;
- salida vacía generada por eliminaciones silenciosas.

Un bloqueo debe devolverse como estado explícito, no como cadena vacía ni como sustitución inventada.

## 11. Perfil de español pendiente

Antes de implementar la normalización fonética deberá aprobarse un documento independiente que resuelva, como mínimo:

- variedad o variedades de español europeo admitidas;
- tratamiento de distinción y seseo;
- yeísmo y posibles contrastes;
- realización de /s/ en coda;
- grupos consonánticos;
- diptongos, hiatos y semivocales;
- acento léxico;
- préstamos, abreviaturas, números y nombres propios;
- relación entre ortografía y pronunciación excepcional;
- opciones que el usuario puede declarar y valores por defecto.

No se impondrá una variedad regional marcada bajo una etiqueta genérica de español.

## 12. Evidencia de reglas

Cada futura regla deberá distinguir:

1. **evidencia del corpus:** patrón presente en los datos atestiguados;
2. **evidencia bibliográfica:** análisis o restricción descritos en una fuente;
3. **decisión de ingeniería:** aproximación necesaria para entradas modernas;
4. **preferencia de interfaz:** orden o presentación sin valor lingüístico.

Una decisión de ingeniería nunca podrá etiquetarse como hecho ibérico documentado.

## 13. Puertas antes de implementar

La implementación seguirá desactivada hasta completar:

- informes manuales actuales en Safari/iOS;
- informes manuales en Chrome, Firefox y Edge de ordenador;
- modelo mínimo de alógrafos;
- revisión externa documental y gráfica;
- perfil de pronunciación aprobado;
- inventario fonético interno aprobado;
- conjunto inicial de reglas revisado;
- pesos y política de empates documentados;
- plan de evaluación y confianza.

## 14. Siguiente trabajo permitido

Sin activar un conversor, pueden desarrollarse de forma segura:

1. esquema de perfiles de pronunciación;
2. inventario de unidades fonéticas y rasgos;
3. esquema de reglas y niveles de evidencia;
4. catálogo de restricciones del signario;
5. casos de prueba contractuales sin salida lingüística inventada;
6. validador de coherencia entre reglas, inventario y resultados.

## 15. Criterio de aceptación de esta especificación

Esta primera especificación se considera estructuralmente válida cuando:

- el contrato machine-readable permanece en `specification_only`;
- `public_conversion_enabled` es `false`;
- no existen perfiles admitidos ni pesos inventados;
- el esquema de resultados prohíbe afirmaciones semánticas;
- cada candidato exige operaciones, costes, versiones y explicaciones;
- el CI comprueba estas condiciones;
- la documentación pública continúa indicando que no existe un conversor validado.
