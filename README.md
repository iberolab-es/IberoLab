# IberoLab

**Motor abierto y experimental para representar fonéticamente lenguas modernas mediante escrituras paleohispánicas.**

> Estado: **pre-alpha / fase de fundamentación**. El proyecto todavía no ofrece un traductor público validado.

## Qué es

IberoLab investiga cómo transformar texto moderno —inicialmente español— en una **representación fonética experimental** adaptada a signarios ibéricos y otras escrituras paleohispánicas.

El proyecto separa tres operaciones distintas:

1. normalización fonética del texto de entrada;
2. adaptación a las restricciones del sistema de escritura seleccionado;
3. renderizado de signos mediante recursos propios y verificables.

## Qué no es

IberoLab **no traduce literalmente al idioma ibérico**. La lengua ibérica no está descifrada hasta un grado que permita una traducción completa y consensuada de textos modernos. Cualquier salida pública deberá identificar con claridad si es:

- transliteración;
- representación fonética experimental;
- reconstrucción hipotética;
- recreación artística.

## Principios

- Rigor terminológico y transparencia sobre los límites del conocimiento.
- Separación entre datos documentados, hipótesis y decisiones de diseño.
- Trazabilidad de cada signo, variante y valor fonético utilizado.
- Compatibilidad con móvil y escritorio sin depender de fuentes externas no controladas.
- Pruebas reproducibles antes de publicar una versión estable.

## Objetivos iniciales

- Construir un inventario versionado de signos y variantes.
- Desarrollar un motor fonético modular para español.
- Crear un renderizador SVG fiable.
- Publicar una beta web gratuita mediante GitHub Pages.
- Abrir un canal estructurado para errores, propuestas y aportaciones documentales.

## Estructura prevista

```text
.github/     Plantillas, automatización y gobernanza
database/    Inventario de signos y metadatos
docs/        Metodología, alcance y referencias
engine/      Normalización y adaptación fonética
tests/       Casos de prueba y validación
web/         Aplicación estática y renderizador
```

## Participar

Las sugerencias y errores se gestionan mediante [GitHub Issues](https://github.com/iberolab-es/IberoLab/issues/new/choose). Antes de contribuir, consulta [CONTRIBUTING.md](CONTRIBUTING.md).

## Hoja de ruta

Consulta [ROADMAP.md](ROADMAP.md).

## Licencia

Código y documentación publicados bajo [Apache License 2.0](LICENSE), salvo que un recurso concreto indique otra licencia.

---

### English summary

IberoLab is an open experimental project for phonetic representation of modern languages using ancient Iberian and other Palaeohispanic scripts. It does **not** claim to translate modern text into the undeciphered Iberian language.