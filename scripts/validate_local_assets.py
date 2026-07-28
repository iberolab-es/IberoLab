#!/usr/bin/env python3
"""Validate local SVG assets, provenance metadata and modular public local-only usage."""
from __future__ import annotations
import hashlib,json,sys
from pathlib import Path
from xml.etree import ElementTree
ROOT=Path(__file__).resolve().parents[1];MANIFEST=ROOT/"data"/"signs"/"reference-standard-dual.assets.v1.json";MVP_MANIFEST=ROOT/"data"/"signs"/"mvp-standard-signary.assets.v1.json";MAPPING=ROOT/"data"/"signs"/"reference-standard-dual.v1.json";INDEX=ROOT/"docs"/"index.html";RENDERER=ROOT/"docs"/"corpus-renderer.js";SELF_TEST=ROOT/"docs"/"test.html";ASSET_DIR=ROOT/"docs"/"assets"/"signs"/"northeastern-dual"
EXPECTED_TOKENS={"a","e","i","u","gi","ke","ki","ba","da","de","di","ta","s","ś","r","ŕ","l","n","ń"};LOCAL_STATUSES={"local_reference_svg_available","local_attested_variant_svg_available"};FORBIDDEN_MARKERS=(b"<script",b"javascript:",b"onload=",b"onerror=",b"<foreignobject")
def load_json(path): return json.loads(path.read_text(encoding="utf-8"))
def validate_svg_file(path,item,label):
    if not path.is_file(): raise ValueError(f"{label}: local SVG is missing: {path.relative_to(ROOT)}")
    data=path.read_bytes()
    if len(data)!=item.get("bytes") or hashlib.sha256(data).hexdigest()!=item.get("sha256"): raise ValueError(f"{label}: stored SVG differs from manifest")
    if item.get("media_type")!="image/svg+xml" or item.get("licence")!="CC0-1.0": raise ValueError(f"{label}: media type or licence is invalid")
    lowered=data.lower()
    for marker in FORBIDDEN_MARKERS:
        if marker in lowered: raise ValueError(f"{label}: forbidden active SVG marker {marker!r}")
    try: root_element=ElementTree.fromstring(data)
    except ElementTree.ParseError as exc: raise ValueError(f"{label}: malformed SVG XML") from exc
    if not root_element.tag.lower().endswith("svg"): raise ValueError(f"{label}: root element is not SVG")
def validate():
    manifest=load_json(MANIFEST);mapping=load_json(MAPPING);assets=manifest.get("assets",[])
    if manifest.get("schema_version")!="1.1.0" or manifest.get("asset_count")!=19 or len(assets)!=19 or manifest.get("licence")!="CC0-1.0": raise ValueError("attested seed manifest metadata is invalid")
    source_sets=manifest.get("source_sets",[])
    if {i.get("name") for i in source_sets}!={"Sign Iber Noro Dual 01–38","NE Iberian m1.svg"} or any(i.get("licence")!="CC0-1.0" for i in source_sets): raise ValueError("manifest source sets are invalid")
    by_token={i.get("token"):i for i in assets}
    if set(by_token)!=EXPECTED_TOKENS: raise ValueError(f"manifest token mismatch: {sorted(set(by_token)^EXPECTED_TOKENS)}")
    seed_paths=set()
    for token,item in by_token.items():
        relative=item.get("local_path")
        if not isinstance(relative,str) or not relative.startswith("docs/assets/signs/northeastern-dual/"): raise ValueError(f"{token!r}: invalid local path")
        path=ROOT/relative;seed_paths.add(path.resolve());validate_svg_file(path,item,token)
    nasal_asset=by_token["ń"]
    expected_nasal={"reference_id":"variant-m1-nasal","source_file_name":"NE Iberian m1.svg","author":"Vriullop","paleographic_variant":"m1","traditional_transcription":"m","project_transcription":"ń","phonological_scope":"marked_nasal_not_labial","graphic_scope":"normalized_m1_variant_reference_not_facsimile","scholarly_evidence":"https://doi.org/10.36707/palaeohispanica.v25i1.703"}
    for key,value in expected_nasal.items():
        if nasal_asset.get(key)!=value: raise ValueError(f"ń asset has invalid {key}")
    mvp=load_json(MVP_MANIFEST);mvp_assets=mvp.get("assets",[])
    if mvp.get("status")!="mvp_graphic_reference" or mvp.get("asset_count")!=38 or len(mvp_assets)!=38: raise ValueError("MVP manifest must declare 38 assets")
    mvp_paths=set()
    for item in mvp_assets:
        relative=item.get("local_path")
        if not isinstance(relative,str) or not relative.startswith("docs/assets/signs/northeastern-dual/"): raise ValueError(f"MVP token {item.get('token')!r}: invalid local path")
        path=ROOT/relative;mvp_paths.add(path.resolve());validate_svg_file(path,item,f"MVP {item.get('token')!r}")
    if len(mvp_paths)!=38: raise ValueError("MVP manifest paths must identify 38 unique SVGs")
    disk_paths={p.resolve() for p in ASSET_DIR.glob("*.svg")};declared_union=seed_paths|mvp_paths
    if disk_paths!=declared_union:
        extras=sorted(str(p.relative_to(ROOT)) for p in disk_paths-declared_union);missing=sorted(str(p.relative_to(ROOT)) for p in declared_union-disk_paths);raise ValueError(f"asset directory differs from manifests; extras={extras}, missing={missing}")
    signs={i["token"]:i for i in mapping["signs"]}
    if set(signs)!=EXPECTED_TOKENS: raise ValueError("mapping token set must equal corpus tokens")
    for token in EXPECTED_TOKENS:
        sign=signs.get(token)
        if not sign or sign.get("graphic_status") not in LOCAL_STATUSES or sign.get("local_path")!=by_token[token]["local_path"]: raise ValueError(f"{token!r}: mapping differs from accepted manifest")
    nasal_sign=signs["ń"]
    for key in ("paleographic_variant","traditional_transcription","project_transcription","phonological_scope","graphic_scope","evidence"):
        expected_key="scholarly_evidence" if key=="evidence" else key
        if nasal_sign.get(key)!=nasal_asset.get(expected_key): raise ValueError(f"ń mapping differs for {key}")
    public_renderer=INDEX.read_text(encoding="utf-8")+"\n"+RENDERER.read_text(encoding="utf-8");self_test=SELF_TEST.read_text(encoding="utf-8")
    for label,text in (("public renderer",public_renderer),("self-test",self_test)):
        if any(marker in text for marker in ("Special:Redirect/file","COMMONS_REDIRECT","const COMMONS")): raise ValueError(f"{label} still depends on remote SVG delivery")
        for item in assets:
            web_path=item["local_path"].removeprefix("docs/")
            if web_path not in text: raise ValueError(f"{label} does not declare local path {web_path}")
    if 'asset_mode: "local_repository"' not in self_test or 'version: "1.2.0"' not in self_test: raise ValueError("self-test metadata is outdated")
    if manifest.get("unresolved")!=[]: raise ValueError("manifest must not retain unresolved tokens")
    resolved=manifest.get("resolved_tokens",[])
    if len(resolved)!=1 or resolved[0].get("token")!="ń" or resolved[0].get("resolved_as")!="m1": raise ValueError("manifest must record m1 resolution of ń")
    return len(assets),len(mvp_assets),len(disk_paths)
if __name__=="__main__":
    try: seed_declared,mvp_declared,stored=validate()
    except (OSError,json.JSONDecodeError,KeyError,TypeError,ValueError) as exc:
        print(f"LOCAL ASSET VALIDATION FAILED: {exc}",file=sys.stderr);raise SystemExit(1)
    print(f"LOCAL ASSET VALIDATION OK: {seed_declared} seed assets; {mvp_declared} MVP assets; {stored} stored SVGs; modular local-only delivery verified.")
