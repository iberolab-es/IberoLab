# Recreación sonora experimental

## Alcance

El sintetizador de IberoLab **no reconstruye cómo hablaban los íberos**. Vocaliza la secuencia de valores convencionales que ya aparece en la lectura técnica del conversor y la convierte en una señal sonora reproducible.

Por ejemplo, si la adaptación gráfica produce `m · u · n · do`, el sintetizador recibe exactamente esos cuatro tokens. No recibe de nuevo la palabra española original y no utiliza la voz `es-ES` del dispositivo.

La clasificación correcta es **aproximación sonora experimental**, **recreación sonora experimental** o **lectura sintética de los signos**. No debe denominarse «audio en ibérico», «pronunciación auténtica» ni «reconstrucción histórica».

## Base lingüística

El perfil `iberolab-sign-reading-voice-v1` parte de los aspectos que cuentan con mayor consenso relativo:

- cinco vocales convencionales `a`, `e`, `i`, `o`, `u`;
- tres series de oclusivas: labial, dental y velar;
- contraste gráfico en las series dentales y velares del sistema dual;
- valores convencionales para `l`, `m` y `n`;
- existencia de dos signos róticos y dos sibilantes, aunque su oposición fonética exacta no sea segura.

Las incertidumbres permanecen visibles:

- `s` y `ś` se diferencian acústicamente mediante una hipótesis laminal frente a apical/retraída;
- `r` y `ŕ` se realizan como vibrante simple y múltiple siguiendo una convención propia de IberoLab, no una identificación histórica demostrada;
- `ḿ` recibe un color nasal silábico únicamente para poder oír el signo;
- la oposición de las oclusivas dentales y velares se realiza como sonora frente a sorda, aunque se ha planteado también una diferencia fortis/lenis.

## Decisiones de síntesis

El audio se genera íntegramente en el navegador con un sintetizador de formantes determinista:

- señal mono a 24 kHz;
- timbres vocálicos creados mediante resonancias formánticas;
- cierres y explosiones diferenciados para las oclusivas;
- ruido filtrado para las dos sibilantes;
- interrupciones distintas para las dos róticas;
- duración aproximadamente uniforme por token;
- pausas breves entre signos y mayores entre palabras.

El tono, el ritmo, las duraciones, las frecuencias formánticas y la ligera caída melódica son decisiones modernas de interfaz. No existe evidencia suficiente para atribuirlos a la prosodia ibérica.

La síntesis no requiere red, cuenta, clave de API ni archivos de voz externos. Para la misma secuencia de tokens y la misma versión utiliza siempre el mismo plan y la misma semilla. Dentro de un mismo motor JavaScript genera las mismas muestras; no se promete identidad binaria absoluta entre navegadores distintos, cuyas funciones matemáticas pueden introducir diferencias numéricas mínimas.

## Fuentes de referencia

- Noemí Moncunill Martí y Javier Velaza Frías, «Iberian», *Palaeohispanica* 20 (2020), pp. 591–629. DOI: [10.36707/palaeohispanica.v0i20.370](https://doi.org/10.36707/palaeohispanica.v0i20.370).
- Oliver Simkin, «The Iberian sibilants revisited», *Palaeohispanica* 17 (2017), pp. 207–233. [Texto completo](https://ifc.dpz.es/recursos/publicaciones/36/49/13simkin.pdf).

La configuración machine-readable se conserva en [`data/engine/experimental-voice-profile.v1.json`](../data/engine/experimental-voice-profile.v1.json).
