#!/usr/bin/env python3
"""Validate the public landing, history, methodology and audio safeguards."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
INDEX=ROOT/"docs"/"index.html";HISTORY=ROOT/"docs"/"historia.html";METHODOLOGY=ROOT/"docs"/"metodologia.html";ACADEMIA=ROOT/"docs"/"academia.html";CONVERTER=ROOT/"docs"/"convertir.html";CONVERTER_UI=ROOT/"docs"/"converter-ui.js";CORPUS_RENDERER=ROOT/"docs"/"corpus-renderer.js";CORPUS_VOICE=ROOT/"docs"/"corpus-voice.js";VOICE=ROOT/"docs"/"iberian-voice.js";STYLE=ROOT/"docs"/"public-site.css";MARK=ROOT/"docs"/"assets"/"brand"/"iberolab-mark.svg"
def require(text,markers,label):
    missing=[m for m in markers if m not in text]
    if missing: raise ValueError(f"{label} lacks markers: {missing}")
def main():
    files=(INDEX,HISTORY,METHODOLOGY,ACADEMIA,CONVERTER,CONVERTER_UI,CORPUS_RENDERER,CORPUS_VOICE,VOICE,STYLE,MARK)
    missing=[str(p.relative_to(ROOT)) for p in files if not p.is_file()]
    if missing: raise ValueError(f"missing public files: {missing}")
    index=INDEX.read_text(encoding="utf-8");history=HISTORY.read_text(encoding="utf-8");method=METHODOLOGY.read_text(encoding="utf-8");academia=ACADEMIA.read_text(encoding="utf-8");converter=CONVERTER.read_text(encoding="utf-8");converter_ui=CONVERTER_UI.read_text(encoding="utf-8");corpus_renderer=CORPUS_RENDERER.read_text(encoding="utf-8");corpus_voice=CORPUS_VOICE.read_text(encoding="utf-8");voice=VOICE.read_text(encoding="utf-8");combined_converter=converter+"\n"+converter_ui+"\n"+voice;combined_corpus=index+"\n"+corpus_renderer+"\n"+corpus_voice+"\n"+voice;style=STYLE.read_text(encoding="utf-8");mark=MARK.read_text(encoding="utf-8")
    require(index,("Lengua ibérica · Patrimonio · Tecnología","Adaptación fonética · MVP","No ofrece una traducción a la lengua ibérica","Probar conversor",'id="corpus"','href="historia.html"','href="metodologia.html"','href="academia.html"',"Un monograma-glifo contemporáneo","No es un signo ibérico antiguo","Para la comunidad académica",'href="convertir.html?q=tierra"','dual-28-ti.svg','dual-02-e.svg','dual-34-r2.svg','dual-01-a.svg'),"home")
    require(history,("Comprender el mundo ibérico antes de intentar representarlo","Leer signos no significa traducir la lengua","Una sección preparada para crecer con YouTube","Monedas e inscripciones",'href="./#corpus"','href="academia.html"'),"history")
    require(method,("No traduce el español a la lengua ibérica","Dos orígenes, dos modos de recreación","Forma atestiguada","Entrada moderna","Voz fluida moderna","Síntesis técnica","No es una reconstrucción de cómo hablaban los íberos","iberolab-sign-reading-voice-v3","iberolab-sign-reading-voice-v1","No es un signo ibérico arqueológico","Trazabilidad técnica",'href="./#corpus"','href="privacidad.html"'),"methodology")
    require(academia,("Información para universidades y especialistas",'href="./#corpus"','href="historia.html"','href="metodologia.html"','href="academia.html" aria-current="page"','href="convertir.html"'),"academic page")
    if 'href="corpus.html"' in history or 'href="corpus.html"' in method: raise ValueError("provisional corpus.html link remains in public pages")
    require(combined_converter,("Escuchar entrada en español","Escuchar aproximación sonora","Fluida moderna · voz natural","Técnica · síntesis reproducible","No reconstruye cómo hablaban los íberos","iberolab-sign-reading-voice-v3","iberolab-sign-reading-voice-v1","Forma ibérica atestiguada","Entrada española moderna","sin afirmar parentesco",'href="historia.html"','href="metodologia.html"','href="academia.html"','src="iberian-voice.js"','src="converter-ui.js"','data-example="hogar"','data-example="tierra"','data-example="mundo"','data-example="olivo"','data-example="mar"',"cualquier nombre, sentimiento", "palabra o frase breve"),"converter")
    require(combined_corpus,("Escuchar forma atestiguada","Forma atestiguada · voz fluida","Forma atestiguada · síntesis técnica","La secuencia escrita está documentada; su sonido no","iberolab-sign-reading-voice-v3","VOICE_SCRIPT_PATH","nasal prolongada"),"attested corpus audio")
    require(style,(".public-nav",".home-hero",".logo-story",".video-grid"),"stylesheet")
    require(mark,("Marca contemporánea geométrica","fusiona trazos inspirados","no representa ni reproduce un signo antiguo auténtico","<circle"),"brand mark")
    if "dual-29-te.svg" in index: raise ValueError("mislabeled te/to graphic reference remains in home sample")
    if "Escuchar en ibero" in combined_converter or "pronunciación auténtica ibérica" in combined_converter or "acento ibérico histórico" in combined_converter: raise ValueError("authentic Iberian pronunciation claim detected")
    for forbidden in ("Escuchar lectura aproximada","approximateButton","experimentalReadingText"):
        if forbidden in combined_converter: raise ValueError(f"obsolete approximate-audio marker remains: {forbidden}")
    print("PUBLIC SITE VALIDATION OK: landing, history, methodology, academic links, contemporary mark and bounded experimental audio present.");return 0
if __name__=="__main__":
    try: raise SystemExit(main())
    except (OSError,ValueError) as exc:
        print(f"PUBLIC SITE VALIDATION FAILED: {exc}",file=sys.stderr);raise SystemExit(1)
