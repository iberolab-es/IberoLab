#!/usr/bin/env python3
"""Validate coverage and public safeguards of the modular reference renderer."""
from __future__ import annotations
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];CORPUS=ROOT/"data"/"corpus"/"attested-forms.v1.json";MAPPING=ROOT/"data"/"signs"/"reference-standard-dual.v1.json";HTML=ROOT/"docs"/"index.html";SCRIPT=ROOT/"docs"/"corpus-renderer.js";LOCAL_STATUSES={"local_reference_svg_available","local_attested_variant_svg_available"}
def main():
    corpus=json.loads(CORPUS.read_text(encoding="utf-8"));mapping=json.loads(MAPPING.read_text(encoding="utf-8"));signs={i["token"]:i for i in mapping["signs"]};used={t for f in corpus["forms"] for t in f["grapheme_sequence"]}
    missing=sorted(used-signs.keys());extras=sorted(signs.keys()-used)
    if missing: raise ValueError(f"Tokens absent from renderer mapping: {missing}")
    if extras: raise ValueError(f"Renderer mapping contains unused tokens: {extras}")
    available=0;unresolved=[]
    for token in sorted(used):
        item=signs[token];status=item.get("graphic_status")
        if status in LOCAL_STATUSES:
            local_path=item.get("local_path")
            if not isinstance(local_path,str) or not local_path.endswith(".svg") or not local_path.startswith("docs/assets/signs/northeastern-dual/") or not (ROOT/local_path).is_file(): raise ValueError(f"{token!r}: invalid local SVG path")
            available+=1
        elif status and status.startswith("pending_"): unresolved.append(token)
        else: raise ValueError(f"{token!r}: unknown graphic status {status!r}")
    nasal=signs["ń"]
    expected={"graphic_status":"local_attested_variant_svg_available","paleographic_variant":"m1","traditional_transcription":"m","project_transcription":"ń","phonological_scope":"marked_nasal_not_labial","graphic_scope":"normalized_m1_variant_reference_not_facsimile","evidence":"https://doi.org/10.36707/palaeohispanica.v25i1.703"}
    for key,value in expected.items():
        if nasal.get(key)!=value: raise ValueError(f"ń mapping lacks documented {key}={value!r}")
    html=HTML.read_text(encoding="utf-8");script=SCRIPT.read_text(encoding="utf-8");combined=html+"\n"+script
    required=("renderForm","glyph-fallback","DOMContentLoaded","sourceLink","evidenceText","transcriptionNote","previousButton","nextButton","hashchange","rendererReady","No es una traducción al idioma ibérico","Referencia normalizada","variant-m1-nasal.svg","variante m1","transcripción tradicional era m","no un facsímil",'src="corpus-renderer.js"')
    absent=[m for m in required if m not in combined]
    if absent: raise ValueError(f"renderer lacks safeguards: {absent}")
    if "Special:Redirect/file" in combined or "COMMONS_REDIRECT" in combined or "upload.wikimedia.org" in combined: raise ValueError("remote SVG dependency detected")
    absent_forms=[i["id"] for i in corpus["forms"] if i["id"] not in script]
    if absent_forms: raise ValueError(f"renderer script lacks corpus entries: {absent_forms}")
    if unresolved: raise ValueError(f"seed corpus has unresolved tokens: {unresolved}")
    if available!=len(used) or available!=19: raise ValueError(f"expected nineteen available SVG mappings, got {available}")
    print(f"RENDERER VALIDATION OK: {len(corpus['forms'])} forms; {available} local SVG mappings; modular renderer and scientific safeguards present.");return 0
if __name__=="__main__":
    try: raise SystemExit(main())
    except (OSError,json.JSONDecodeError,KeyError,ValueError) as exc:
        print(f"RENDERER VALIDATION FAILED: {exc}",file=sys.stderr);raise SystemExit(1)
