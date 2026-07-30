# Recreación sonora experimental

## Alcance

La voz de IberoLab **no reconstruye cómo hablaban los íberos**. Vocaliza la secuencia de valores convencionales que ya aparece en la lectura técnica del conversor.

Por ejemplo, si la adaptación gráfica produce `ka · s · a`, el sistema recibe esos tres tokens. No traduce la palabra a la lengua ibérica ni le atribuye una pronunciación histórica.

La clasificación correcta es **aproximación sonora experimental**, **recreación sonora experimental**, **voz fluida moderna** o **lectura sintética de los signos**. No debe denominarse «audio en ibérico», «pronunciación auténtica», «acento ibérico» ni «reconstrucción histórica».

## Dos modos complementarios

El perfil público `iberolab-sign-reading-voice-v2` conserva dos renderizadores:

### Voz fluida moderna

Es el modo predeterminado. Une los valores de los signos en palabras completas y pide al sistema de voz del navegador o dispositivo una articulación natural. Así evita las pausas independientes, reinicios de fase y ataques uniformes que hacían que la primera versión sonara mecánica.

El sistema prefiere una voz moderna en euskera (`eu-ES`) cuando está disponible. Si no lo está, busca una voz catalana y después una voz española. La voz, el timbre y algunos detalles prosódicos pueden variar entre dispositivos; este modo no es determinista.

### Síntesis técnica reproducible

Conserva el perfil `iberolab-sign-reading-voice-v1`: genera una señal mono a 24 kHz mediante formantes, explosiones de oclusivas, ruido filtrado y realizaciones diferenciadas de róticas y sibilantes. Es más mecánica, pero resulta útil como referencia de laboratorio porque la misma secuencia mantiene el mismo plan y la misma semilla dentro de una versión.

## Por qué se usa una paleta euskérica moderna

No se usa el euskera porque se considere demostrado que el ibérico fuera su antepasado o sonara como él. Moncunill y Velaza subrayan que la hipotética relación del ibérico con cualquier lengua antigua o moderna sigue siendo incierta.

La elección es estrictamente instrumental:

- la mayoría de variedades modernas del euskera emplean cinco vocales `a`, `e`, `i`, `o`, `u`;
- su ortografía permite una oposición práctica entre vibrante simple y múltiple mediante `r/rr`;
- ofrece grafías distintas para sibilantes laminales y apicales, útiles para hacer audible la hipótesis de trabajo aplicada a `s/ś`;
- el sistema de voz está disponible en plataformas modernas como una voz humana completa, no como fonemas aislados.

En el puente principal, IberoLab representa convencionalmente `s → z`, `ś → s`, `r → r` y `ŕ → rr`. La correspondencia facilita la articulación, pero **no constituye evidencia de parentesco, continuidad ni identidad fonética histórica**.

Tampoco se adopta un «acento celta» o árabe. El celtibérico era otra lengua paleohispánica, de filiación indoeuropea, y el árabe pertenece a un horizonte peninsular posterior al final de la documentación ibérica. Usarlos como modelo conferiría al audio una asociación histórica que las fuentes no justifican.

## Base lingüística

Los dos modos comparten las mismas convenciones de entrada:

- cinco vocales convencionales `a`, `e`, `i`, `o`, `u`;
- tres series de oclusivas: labial, dental y velar;
- contraste gráfico en las series dentales y velares del sistema dual;
- valores convencionales para `l`, `m` y `n`;
- existencia de dos signos róticos y dos sibilantes, aunque su oposición fonética exacta no sea segura.

Las incertidumbres permanecen visibles:

- `s` y `ś` se diferencian mediante una hipótesis laminal frente a apical;
- `r` y `ŕ` se realizan como vibrante simple y múltiple siguiendo una convención propia de IberoLab;
- `ḿ` recibe una vocalización auxiliar únicamente para poder oír el signo;
- la oposición de las oclusivas dentales y velares se realiza como sonora frente a sorda, aunque se ha planteado también una diferencia fortis/lenis;
- no se infiere un sistema ibérico de acento, ritmo o entonación.

## Reproducción, privacidad y compatibilidad

IberoLab no envía las palabras ni el audio a sus propios servidores.

- En el modo fluido, la página solicita la voz instalada o administrada por el navegador o el sistema operativo. La disponibilidad, descarga de activos de voz y tratamiento interno dependen de la plataforma.
- En el modo técnico, todas las muestras se calculan mediante JavaScript en el propio navegador.

En WebKit compatible, ambos modos solicitan una sesión `playback` antes de reproducir para evitar que el modo silencio del iPhone deje el audio mudo ([WebKit, incidencia 237322](https://bugs.webkit.org/show_bug.cgi?id=237322)). La sesión anterior se restaura al terminar o detener la recreación.

## Fuentes de referencia

- Noemí Moncunill Martí y Javier Velaza Frías, «Iberian», *Palaeohispanica* 20 (2020), pp. 591–629. DOI: [10.36707/palaeohispanica.v0i20.370](https://doi.org/10.36707/palaeohispanica.v0i20.370).
- Oliver Simkin, «The Iberian sibilants revisited», *Palaeohispanica* 17 (2017), pp. 207–233. [Texto completo](https://ifc.dpz.es/recursos/publicaciones/36/49/13simkin.pdf).
- Ander Egurtzegi, «Phonetics and Phonology» (2013), en *Towards a History of the Basque Language*. [Texto completo](https://www.phonetik.uni-muenchen.de/personen/assoziierte_wissenschaftler/egurtzegi_ander/2013_protobasque_phonology.pdf).
- Iván Igartua, «Bringing phonological oddities to the fore: The Basque sibilants», *ASJU* 57 (2023), pp. 495–513. DOI: [10.1387/asju.25965](https://doi.org/10.1387/asju.25965).

Las configuraciones legibles por máquina se conservan en:

- [`data/engine/experimental-voice-profile.v2.json`](../data/engine/experimental-voice-profile.v2.json), perfil híbrido vigente;
- [`data/engine/experimental-voice-profile.v1.json`](../data/engine/experimental-voice-profile.v1.json), síntesis técnica preservada.
