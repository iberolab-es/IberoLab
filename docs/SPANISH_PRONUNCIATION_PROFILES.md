# Perfiles de pronunciación para español europeo

## 1. Estado

Este documento especifica cómo deberá declararse una pronunciación española antes de que IberoLab pueda normalizar fonéticamente una entrada moderna.

Estado actual:

- registro: `data/engine/spanish-pronunciation-dimensions.v1.json`;
- esquema de perfil: `data/schema/pronunciation-profile.schema.json`;
- estado: `specification_only`;
- perfiles aprobados: ninguno;
- perfil por defecto: ninguno;
- selección pública de perfil: desactivada;
- motor fonético: no implementado.

La existencia del esquema no autoriza a generar pronunciaciones ni adaptaciones.

## 2. Por qué no existe un «español de España» implícito

La etiqueta `es-ES` delimita una lengua y un ámbito territorial, pero no determina por sí sola una pronunciación única. Entre hablantes españoles existen diferencias fonológicas, fonéticas, geográficas, sociales y de registro.

IberoLab no deberá:

- identificar automáticamente una pronunciación por la ubicación del usuario;
- presentar una variedad castellana concreta como neutral para toda España;
- considerar el seseo o el yeísmo errores;
- convertir la ortografía en pronunciación sin registrar excepciones y ambigüedades;
- mezclar estilo formal, habla coloquial y procesos de habla conectada dentro de un mismo perfil sin declararlo.

## 3. Fuentes y alcance

La primera versión utiliza dos tipos de fuente:

1. **referencias académicas panhispánicas**, para reconocer variación y separar ortografía de pronunciación;
2. **descripciones fonéticas revisadas por pares**, para disponer de modelos técnicos concretos sin convertirlos en perfiles universales.

La descripción de Martínez-Celdrán, Fernández-Planas y Carrera-Sabaté de 2003 se registra como referencia de una variedad castellana formal. No se adopta como perfil por defecto de España.

## 4. Dimensiones documentadas

### 4.1 Sistema de sibilantes

Debe declararse explícitamente una de estas opciones cuando se apruebe un perfil:

- `distinction`: contraste entre /s/ y la sibilante interdental asociada a z y c ante e/i;
- `seseo`: una categoría /s/ para ambas series ortográficas;
- `ceceo`: una categoría interdental para ambas series, con delimitación geográfica y sociolingüística específica.

No existe opción por defecto. El seseo es una pronunciación plenamente válida en las zonas donde está asentado; el ceceo requiere un perfil explícitamente acotado y una revisión sociolingüística cuidadosa.

### 4.2 Sistema palatal y yeísmo

Debe distinguirse entre:

- `yeismo`: y consonántica y ll comparten categoría fonológica, sin fijar todavía una única realización alofónica;
- `y_ll_distinction`: se conserva el contraste con la lateral palatal.

No existe opción por defecto. El predominio territorial del yeísmo no autoriza a borrar silenciosamente el contraste en un perfil que pretenda representar a hablantes que lo conservan.

### 4.3 Secuencias vocálicas

La silabificación real de dos vocales contiguas no siempre puede deducirse únicamente de la clasificación ortográfica. Por eso esta dimensión se resolverá a nivel léxico o de unidad concreta mediante:

- diptongo fijado por entrada revisada;
- hiato fijado por entrada revisada;
- regla de perfil aprobada y limitada a un entorno;
- bifurcación sin ranking cuando la evidencia no permita elegir.

No se establecerá una preferencia global diptongo/hiato.

### 4.4 Fuente del acento léxico

La posición del acento deberá proceder de:

- ortografía y léxico revisado;
- pronunciación proporcionada por el usuario cuando la entrada sea excepcional;
- bifurcación explícita cuando no exista resolución suficiente.

Los nombres propios, extranjerismos, siglas, abreviaturas y formas no normalizadas no podrán recibir una pronunciación inventada para evitar un bloqueo.

## 5. Dimensiones aún no normalizadas

Permanecen pendientes, entre otras:

- realización de /s/ en coda;
- reducción o pérdida de /d/ intervocálica;
- realización de la fricativa velar;
- realización de /n/ final;
- róticas en coda y grupos consonánticos;
- préstamos y nombres propios;
- profundidad del habla conectada.

Estas dimensiones no se incorporarán con listas intuitivas. Cada una requerirá fuentes primarias o descripciones fonéticas revisadas, ámbito geográfico, registro, nivel de habla y relación con el inventario interno.

## 6. Estructura de un futuro perfil

Un perfil aprobado deberá incluir:

- identificador y versión;
- etiqueta `es-ES`;
- ámbito geográfico incluido;
- afirmaciones geográficas excluidas;
- registro y velocidad;
- profundidad de habla conectada;
- decisiones explícitas para cada dimensión aplicable;
- política de excepciones léxicas;
- política para palabras desconocidas;
- fuentes;
- revisión interna y externa;
- fecha de aprobación.

Un perfil no podrá aprobarse si se limita a etiquetas vagas como «neutro», «peninsular» o «estándar» sin definir sus rasgos.

## 7. Palabras desconocidas

La política futura deberá elegir entre:

- bloquear la entrada;
- exigir pronunciación del usuario;
- conservar alternativas sin ranking.

La adivinación automática está desactivada. El objetivo es evitar que una regla ortográfica aparente produzca una cadena fonética convincente pero falsa.

## 8. Relación con el contrato del motor

El contrato general mantiene:

- `input_profile_status: pending_approval`;
- `supported_input_profiles: []`;
- puerta `approved_spanish_pronunciation_profile: false`.

Antes de implementar, cualquier resultado deberá quedar ligado a un perfil aprobado y versionado. Este documento no modifica todavía los esquemas de resultados porque no existe ninguna referencia de perfil válida que pueda serializarse.

## 9. Revisión y aprobación

Para aprobar un primer perfil se exigirá:

1. revisión interna de coherencia;
2. revisión externa fonética;
3. fuentes para cada dimensión;
4. delimitación geográfica y de registro;
5. inventario fonético compatible;
6. léxico de excepciones o política de bloqueo;
7. casos de prueba positivos, ambiguos y bloqueados;
8. ausencia de un perfil por defecto no justificado.

## 10. Siguiente trabajo permitido

La siguiente especificación segura es el inventario de unidades fonéticas y rasgos. Deberá poder representar las opciones del registro sin seleccionar todavía reglas de adaptación paleohispánica.
