#!/usr/bin/env python3
"""Validate the public identity, history, methodology and routing layer."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "docs" / "index.html"
CORPUS = ROOT / "docs" / "corpus.html"
HISTORY = ROOT / "docs" / "historia.html"
METHODOLOGY = ROOT / "docs" / "metodologia.html"
CONVERTER = ROOT / "docs" / "convertir.html"
STYLE = ROOT / "docs" / "public-site.css"
LOGO = ROOT / "docs" / "assets" / "brand" / "iberolab-emblem.svg"


def require(text: str, markers: tuple[str, ...], label: str) -> None:
    missing = [marker for marker in markers if marker not in text]
    if missing:
        raise ValueError(f"{label} lacks required markers: {missing}")


def main() -> int:
    files = (INDEX, CORPUS, HISTORY, METHODOLOGY, CONVERTER, STYLE, LOGO)
    missing_files = [str(path.relative_to(ROOT)) for path in files if not path.is_file()]
    if missing_files:
        raise ValueError(f"public site files missing: {missing_files}")

    index = INDEX.read_text(encoding="utf-8")
    corpus = CORPUS.read_text(encoding="utf-8")
    history = HISTORY.read_text(encoding="utf-8")
    methodology = METHODOLOGY.read_text(encoding="utf-8")
    converter = CONVERTER.read_text(encoding="utf-8")
    style = STYLE.read_text(encoding="utf-8")
    logo = LOGO.read_text(encoding="utf-8")

    require(index, (
        "Lengua ibérica · Patrimonio · Tecnología",
        "Probar conversor",
        'id="corpus"',
        'href="corpus.html"',
        'href="historia.html"',
        'href="metodologia.html"',
        "Un signo-raíz contemporáneo",
        "No es un signo ibérico antiguo",
        "Para la comunidad académica",
        "location.replace(`corpus.html${location.search}${location.hash}`)",
    ), "home")
    require(corpus, (
        "Formas ibéricas contrastadas",
        "No es una traducción al idioma ibérico",
        "renderForm",
        "rendererReady",
        "variant-m1-nasal.svg",
    ), "corpus page")
    require(history, (
        "Comprender el mundo ibérico antes de intentar representarlo",
        "Leer signos no significa traducir el idioma",
        "Una sección preparada para crecer con YouTube",
        "Monedas e inscripciones",
    ), "history page")
    require(methodology, (
        "No traduce el español al idioma ibérico",
        "Lectura aproximada",
        "No es un signo ibérico arqueológico",
        "Trazabilidad técnica",
    ), "methodology page")
    require(converter, (
        "Escuchar lectura aproximada",
        "recurso didáctico y no una reconstrucción histórica",
        "experimentalReadingText",
        'href="historia.html"',
        'href="corpus.html"',
    ), "converter")
    require(style, (".site-nav", ".home-hero", ".logo-story", ".video-grid"), "public stylesheet")
    require(logo, ("Emblema contemporáneo de IberoLab", "raíz, escritura, memoria", "<circle"), "brand emblem")

    if "Escuchar en ibero" in converter:
        raise ValueError("converter must not claim an authentic Iberian pronunciation")
    if "signo ibérico histórico" in index.lower():
        raise ValueError("home must not present the contemporary emblem as an ancient sign")

    public_pages = {
        "home": index,
        "corpus": corpus,
        "history": history,
        "methodology": methodology,
        "converter": converter,
    }
    remote_asset_markers = ('<img src="http', '<script src="http', '<link rel="stylesheet" href="http')
    for label, text in public_pages.items():
        found = [marker for marker in remote_asset_markers if marker in text.lower()]
        if found:
            raise ValueError(f"{label} contains uncontrolled remote presentation assets: {found}")

    lowered_logo = logo.lower()
    unsafe_logo_markers = ("<script", "javascript:", "<foreignobject", "onload=")
    unsafe = [marker for marker in unsafe_logo_markers if marker in lowered_logo]
    if unsafe:
        raise ValueError(f"brand emblem contains active SVG content: {unsafe}")

    print(
        "PUBLIC SITE VALIDATION OK: home, legacy corpus routing, local presentation assets, "
        "history, methodology, contemporary emblem and approximate-reading safeguards present."
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError) as exc:
        print(f"PUBLIC SITE VALIDATION FAILED: {exc}", file=sys.stderr)
        raise SystemExit(1)
