#!/usr/bin/env python3
"""Validate the public landing, history, methodology and approximate-reading safeguards."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
INDEX=ROOT/"docs"/"index.html";HISTORY=ROOT/"docs"/"historia.html";METHODOLOGY=ROOT/"docs"/"metodologia.html";CONVERTER=ROOT/"docs"/"convertir.html";CONVERTER_UI=ROOT/"docs"/"converter-ui.js";STYLE=ROOT/"docs"/"public-site.css";MARK=ROOT/"docs"/"assets"/"brand"/"iberolab-mark.svg"
def require(text,markers,label):
    missing=[m for m in markers if m not in text]
    if missing: raise ValueError(f"{label} lacks markers: {missing}")
def main():
    files=(INDEX,HISTORY,METHODOLOGY,CONVERTER,CONVERTER_UI,STYLE,MARK)
    missing=[str(p.relative_to(ROOT)) for p in files if not p.is_file()]
    if missing: raise ValueError(f"missing public files: {missing}")
    index=INDEX.read_text(encoding="utf-8");history=HISTORY.read_text(encoding="utf-8");method=METHODOLOGY.read_text(encoding="utf-8");converter=CONVERTER.read_text(encoding="utf-8");converter_ui=CONVERTER_UI.read_text(encoding="utf-8");combined_converter=converter+"\n"+converter_ui;style=STYLE.read_text(encoding="utf-8");mark=MARK.read_text(encoding="utf-8")
    require(index,("Lengua ibérica · Patrimonio · Tecnología","Probar conversor",'id="corpus"','href="historia.html"','href="metodologia.html"','href="academia.html"',"Un signo-raíz contemporáneo","No es un signo ibérico antiguo","Para la comunidad académica"),"home")
    require(history,("Comprender el mundo ibérico antes de intentar representarlo","Leer signos no significa traducir el idioma","Una sección preparada para crecer con YouTube","Monedas e inscripciones",'href="academia.html"'),"history")
    require(method,("No traduce el español al idioma ibérico","Dos audios con alcances distintos","Lectura aproximada","No es un signo ibérico arqueológico","Trazabilidad técnica",'href="privacidad.html"'),"methodology")
    require(combined_converter,("Escuchar lectura aproximada","experimentalReadingText","recurso didáctico y no una reconstrucción histórica",'href="historia.html"','href="metodologia.html"','href="academia.html"','src="converter-ui.js"'),"converter")
    require(style,(".public-nav",".home-hero",".logo-story",".video-grid"),"stylesheet")
    require(mark,("Marca contemporánea geométrica","no representa un signo antiguo auténtico","<circle"),"brand mark")
    if "Escuchar en ibero" in combined_converter: raise ValueError("authentic Iberian pronunciation claim detected")
    print("PUBLIC SITE VALIDATION OK: landing, history, methodology, academic links, contemporary mark and approximate-reading safeguards present.");return 0
if __name__=="__main__":
    try: raise SystemExit(main())
    except (OSError,ValueError) as exc:
        print(f"PUBLIC SITE VALIDATION FAILED: {exc}",file=sys.stderr);raise SystemExit(1)
