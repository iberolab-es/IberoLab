#!/usr/bin/env python3
"""Validate the public landing, history, methodology and audio safeguards."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import sys
ROOT=Path(__file__).resolve().parents[1]
INDEX=ROOT/"docs"/"index.html";HISTORY=ROOT/"docs"/"historia.html";METHODOLOGY=ROOT/"docs"/"metodologia.html";ACADEMIA=ROOT/"docs"/"academia.html";CONVERTER=ROOT/"docs"/"convertir.html";CONVERTER_UI=ROOT/"docs"/"converter-ui.js";CORPUS_RENDERER=ROOT/"docs"/"corpus-renderer.js";CORPUS_VOICE=ROOT/"docs"/"corpus-voice.js";VOICE=ROOT/"docs"/"iberian-voice.js";STYLE=ROOT/"docs"/"public-site.css";MARK=ROOT/"docs"/"assets"/"brand"/"iberolab-mark.svg"
def require(text,markers,label):
    missing=[m for m in markers if m not in text]
    if missing: raise ValueError(f"{label} lacks markers: {missing}")

class PageReferences(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links = []
        self.ids = set()
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if "id" in values:
            if values["id"] in self.ids:
                raise ValueError(f"duplicate HTML id: {values['id']}")
            self.ids.add(values["id"])
        key = "href" if tag in ("a", "link") else "src"
        if tag in ("a", "link", "script", "img") and values.get(key):
            self.links.append(values[key])

def validate_editorial_references():
    docs = ROOT / "docs"
    count = 0
    pages = ("index.html", "historia.html", "metodologia.html", "academia.html", "convertir.html", "privacidad.html", "corpus.html")
    for name in pages:
        text = (docs / name).read_text(encoding="utf-8")
        if any(phrase in text for phrase in ("contexto, segmentación", "fuente, segmentación")):
            raise ValueError(f"{name}: ambiguous claim of existing linguistic segmentation")
        if "Proyecto abierto sobre lengua ibérica" in text or "Lengua ibérica · Patrimonio · Tecnología" in text:
            raise ValueError(f"obsolete public scope in {name}")
        require(text, ('href="#contenido"', 'id="contenido"', 'href="public-site.css"'), name)
        for href in PageReferences(text).links:
            url = urlsplit(href)
            if url.scheme or url.netloc:
                continue
            target = docs / unquote(url.path or name)
            if target.is_dir():
                target = target / "index.html"
            if not target.is_file():
                raise ValueError(f"{name}: missing local target {href}")
            if url.fragment and target.suffix == ".html":
                ids = PageReferences(target.read_text(encoding="utf-8")).ids
                if url.fragment not in ids:
                    # Corpus identifiers are generated dynamically from the documented dataset.
                    import json
                    corpus_ids = {f["id"] for f in json.loads((ROOT / "data/corpus/attested-forms.v1.json").read_text())["forms"]}
                    if target.name != "index.html" or url.fragment not in corpus_ids:
                        raise ValueError(f"{name}: missing anchor {href}")
            count += 1
    return count
def main():
    files=(INDEX,HISTORY,METHODOLOGY,ACADEMIA,CONVERTER,CONVERTER_UI,CORPUS_RENDERER,CORPUS_VOICE,VOICE,STYLE,MARK)
    missing=[str(p.relative_to(ROOT)) for p in files if not p.is_file()]
    if missing: raise ValueError(f"missing public files: {missing}")
    index=INDEX.read_text(encoding="utf-8");history=HISTORY.read_text(encoding="utf-8");method=METHODOLOGY.read_text(encoding="utf-8");academia=ACADEMIA.read_text(encoding="utf-8");converter=CONVERTER.read_text(encoding="utf-8");converter_ui=CONVERTER_UI.read_text(encoding="utf-8");corpus_renderer=CORPUS_RENDERER.read_text(encoding="utf-8");corpus_voice=CORPUS_VOICE.read_text(encoding="utf-8");voice=VOICE.read_text(encoding="utf-8");combined_converter=converter+"\n"+converter_ui+"\n"+voice;combined_corpus=index+"\n"+corpus_renderer+"\n"+corpus_voice+"\n"+voice;style=STYLE.read_text(encoding="utf-8");mark=MARK.read_text(encoding="utf-8")
    require(index,("Descubre la escritura ibérica","Conversor experimental de escritura","No ofrece una traducción a la lengua ibérica","Probar conversor",'id="corpus"','href="historia.html"','href="metodologia.html"','href="academia.html"',"Un monograma-glifo contemporáneo","No es un signo ibérico antiguo","Dos puertas de entrada",'href="convertir.html?q=tierra"','dual-28-ti.svg','dual-02-e.svg','dual-34-r2.svg','dual-01-a.svg'),"home")
    require(history,("La escritura se entiende mejor cuando conocemos su mundo","Leer signos no significa traducir la lengua","Dual y no dual","Monedas e inscripciones",'href="./#corpus"','href="academia.html"'),"history")
    require(method,("No traduce el español a la lengua ibérica","Dos orígenes, dos modos de recreación","Forma atestiguada","Entrada moderna","Voz fluida moderna","Síntesis técnica","No es una reconstrucción de cómo hablaban los íberos","iberolab-sign-reading-voice-v3","iberolab-sign-reading-voice-v1","No es un signo ibérico arqueológico","Trazabilidad técnica",'href="./#corpus"','href="privacidad.html"'),"methodology")
    require(academia,("Información para universidades y especialistas",'href="./#corpus"','href="historia.html"','href="metodologia.html"','href="academia.html" aria-current="page"','href="convertir.html"'),"academic page")
    require((ROOT / "docs/corpus.html").read_text(encoding="utf-8"), ("Corpus documentado en el navegador", "0 segmentaciones lingüísticas incorporadas"), "academic corpus")
    require(combined_converter,("Escuchar entrada en español","Escuchar aproximación sonora","Fluida moderna · voz natural","Técnica · síntesis reproducible","No reconstruye cómo hablaban los íberos","iberolab-sign-reading-voice-v3","iberolab-sign-reading-voice-v1","Forma ibérica atestiguada","Entrada española moderna","sin afirmar parentesco",'href="historia.html"','href="metodologia.html"','href="academia.html"','src="iberian-voice.js"','src="converter-ui.js"','data-example="hogar"','data-example="tierra"','data-example="mundo"','data-example="olivo"','data-example="mar"',"cualquier nombre, sentimiento", "palabra o frase breve"),"converter")
    require(combined_corpus,("Escuchar forma atestiguada","Forma atestiguada · voz fluida","Forma atestiguada · síntesis técnica","La secuencia escrita está documentada; su sonido no","iberolab-sign-reading-voice-v3","VOICE_SCRIPT_PATH","nasal prolongada"),"attested corpus audio")
    require(style,(".public-nav",".home-hero",".logo-story",".video-grid"),"stylesheet")
    require(mark,("Marca contemporánea geométrica","fusiona trazos inspirados","no representa ni reproduce un signo antiguo auténtico","<circle"),"brand mark")
    if "dual-29-te.svg" in index: raise ValueError("mislabeled te/to graphic reference remains in home sample")
    if "Escuchar en ibero" in combined_converter or "pronunciación auténtica ibérica" in combined_converter or "acento ibérico histórico" in combined_converter: raise ValueError("authentic Iberian pronunciation claim detected")
    for forbidden in ("Escuchar lectura aproximada","approximateButton","experimentalReadingText"):
        if forbidden in combined_converter: raise ValueError(f"obsolete approximate-audio marker remains: {forbidden}")
    count = validate_editorial_references()
    print(f"PUBLIC SITE VALIDATION OK: landing, history, methodology, academic links, contemporary mark and bounded experimental audio present; {count} local references verified.");return 0
if __name__=="__main__":
    try: raise SystemExit(main())
    except (OSError,ValueError) as exc:
        print(f"PUBLIC SITE VALIDATION FAILED: {exc}",file=sys.stderr);raise SystemExit(1)
