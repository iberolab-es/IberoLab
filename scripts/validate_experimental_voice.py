#!/usr/bin/env python3
"""Validate the experimental sign-reading voice profile and public safeguards."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "data" / "engine" / "experimental-voice-profile.v3.json"
PREVIOUS_FLUID_PROFILE = ROOT / "data" / "engine" / "experimental-voice-profile.v2.json"
TECHNICAL_PROFILE = ROOT / "data" / "engine" / "experimental-voice-profile.v1.json"
MVP_CONTRACT = ROOT / "data" / "engine" / "mvp-short-converter.v1.json"
SIGNARY = ROOT / "data" / "signs" / "mvp-standard-signary.assets.v1.json"
CORPUS_INVENTORY = ROOT / "data" / "signs" / "minimum-inventory.v1.json"
ENGINE = ROOT / "docs" / "iberian-voice.js"
CORPUS_RENDERER = ROOT / "docs" / "corpus-renderer.js"
CORPUS_VOICE = ROOT / "docs" / "corpus-voice.js"
PUBLIC_DOC = ROOT / "docs" / "EXPERIMENTAL_VOICE.md"
CONVERTER = ROOT / "docs" / "convertir.html"
CONVERTER_UI = ROOT / "docs" / "converter-ui.js"
METHODOLOGY = ROOT / "docs" / "metodologia.html"
PRIVACY = ROOT / "docs" / "privacidad.html"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def require_markers(label: str, text: str, markers: tuple[str, ...]) -> None:
    missing = [marker for marker in markers if marker not in text]
    if missing:
        raise ValueError(f"{label} lacks markers: {missing}")


def validate() -> tuple[int, int]:
    required_files = (
        PROFILE,
        PREVIOUS_FLUID_PROFILE,
        TECHNICAL_PROFILE,
        MVP_CONTRACT,
        SIGNARY,
        CORPUS_INVENTORY,
        ENGINE,
        CORPUS_RENDERER,
        CORPUS_VOICE,
        PUBLIC_DOC,
        CONVERTER,
        CONVERTER_UI,
        METHODOLOGY,
        PRIVACY,
    )
    missing_files = [str(path.relative_to(ROOT)) for path in required_files if not path.is_file()]
    if missing_files:
        raise ValueError(f"missing experimental voice files: {missing_files}")

    profile = load_json(PROFILE)
    previous_fluid_profile = load_json(PREVIOUS_FLUID_PROFILE)
    technical_profile = load_json(TECHNICAL_PROFILE)
    contract = load_json(MVP_CONTRACT)
    signary = load_json(SIGNARY)
    corpus_inventory = load_json(CORPUS_INVENTORY)

    if profile.get("schema_version") != "3.0.0":
        raise ValueError("voice profile schema version must be 3.0.0")
    if profile.get("profile_id") != "iberolab-sign-reading-voice-v3":
        raise ValueError("voice profile ID differs")
    if profile.get("status") != "public_experimental_recreation":
        raise ValueError("voice profile status is invalid")
    if profile.get("classification") != "source_aware_modern_reading_of_conventional_sign_values":
        raise ValueError("voice profile classification is invalid")
    if profile.get("historical_pronunciation_reconstruction") is not False:
        raise ValueError("historical pronunciation reconstruction must remain false")
    if profile.get("translation_claim") is not False:
        raise ValueError("translation claim must remain false")
    if previous_fluid_profile.get("profile_id") != "iberolab-sign-reading-voice-v2":
        raise ValueError("preserved v2 profile ID differs")
    if technical_profile.get("profile_id") != "iberolab-sign-reading-voice-v1":
        raise ValueError("preserved technical profile ID differs")
    if technical_profile.get("historical_pronunciation_reconstruction") is not False:
        raise ValueError("preserved technical profile must remain non-historical")

    if profile.get("default_mode") != "fluid":
        raise ValueError("fluid voice must remain the public default")

    source_classes = profile.get("source_classes", {})
    if set(source_classes) != {"attested_iberian_form", "modern_spanish_adaptation"}:
        raise ValueError("voice profile must declare exactly two source classes")
    if source_classes["attested_iberian_form"].get("required_public_label") != "forma ibérica atestiguada":
        raise ValueError("attested source class lacks its required public label")
    if source_classes["modern_spanish_adaptation"].get("required_public_label") != "adaptación fonética experimental":
        raise ValueError("modern source class lacks its required public label")

    modes = profile.get("modes", {})
    fluid_mode = modes.get("fluid", {})
    technical_mode = modes.get("technical", {})
    required_fluid_values = {
        "renderer_id": "iberolab-fluid-device-voice-v1",
        "type": "system_speech_synthesis_with_orthographic_bridge",
        "input": "conventional_sign_tokens",
        "preferred_language_tag": "eu-ES",
        "deterministic": False,
        "iberolab_network_required": False,
        "same_voice_across_devices_guaranteed": False,
    }
    for key, value in required_fluid_values.items():
        if fluid_mode.get(key) != value:
            raise ValueError(f"fluid voice mode has invalid {key}")

    modern_palette = fluid_mode.get("modern_palette", {})
    if modern_palette.get("historical_relationship_claim") is not False:
        raise ValueError("modern palette must not claim a historical relationship")
    if modern_palette.get("descent_claim") is not False:
        raise ValueError("modern palette must not claim descent")
    required_mappings = {"s": "z", "ś": "s", "r": "r", "ŕ": "rr", "ń": "n", "ḿ": "um"}
    if modern_palette.get("token_mappings") != required_mappings:
        raise ValueError("modern Basque bridge mappings differ")

    required_technical_values = {
        "renderer_id": "iberolab-sign-reading-voice-v1",
        "type": "deterministic_client_side_formant_synthesizer",
        "sample_rate_hz": 24000,
        "network_required": False,
        "external_voice_required": False,
        "input": "conventional_sign_tokens",
        "same_input_same_plan": True,
        "same_input_same_samples_within_runtime_version": True,
        "cross_engine_bit_identity_guaranteed": False,
    }
    for key, value in required_technical_values.items():
        if technical_mode.get(key) != value:
            raise ValueError(f"technical voice mode has invalid {key}")

    token_groups = []
    for item in profile.get("evidence_based_conventions", []):
        token_groups.extend(item.get("tokens", []))
    for item in profile.get("explicit_hypotheses", []):
        token_groups.extend(item.get("tokens", []))
    expected_tokens = set(signary.get("tokens", []))
    corpus_tokens = {
        item.get("transliteration")
        for item in corpus_inventory.get("signs", [])
        if item.get("transliteration")
    }
    expected_tokens.update(corpus_tokens)
    if len(token_groups) != len(set(token_groups)):
        raise ValueError("voice profile repeats one or more sign tokens")
    if set(token_groups) != expected_tokens or len(token_groups) != 39:
        raise ValueError("voice profile must cover exactly the 39 public corpus/MVP tokens")

    hypothesis_by_id = {
        item.get("id"): item for item in profile.get("explicit_hypotheses", [])
    }
    if hypothesis_by_id.get("two_sibilants", {}).get("confidence") != "low_hypothesis":
        raise ValueError("sibilant contrast must remain labelled as a low-confidence hypothesis")
    if hypothesis_by_id.get("two_rhotics", {}).get("confidence") != "project_convention":
        raise ValueError("rhotic contrast must remain labelled as a project convention")
    if hypothesis_by_id.get("m1_nasal", {}).get("confidence") != "low_project_convention":
        raise ValueError("m1/ń audio must remain a low-confidence project convention")

    source_urls = {item.get("url") for item in profile.get("sources", [])}
    required_sources = {
        "https://ifc.dpz.es/recursos/publicaciones/38/77/17moncunillvelaza.pdf",
        "https://ifc.dpz.es/recursos/publicaciones/36/49/13simkin.pdf",
        "https://www.phonetik.uni-muenchen.de/personen/assoziierte_wissenschaftler/egurtzegi_ander/2013_protobasque_phonology.pdf",
        "https://doi.org/10.1387/asju.25965",
        "https://ifc.dpz.es/recursos/publicaciones/35/02/01ferreretal.pdf",
        "https://ifc.dpz.es/recursos/publicaciones/41/87/08ferrer.pdf",
    }
    if not required_sources.issubset(source_urls):
        raise ValueError("voice profile lacks one or more scholarly sources")

    audio_policy = contract.get("input_convention", {}).get("audio_policy", "")
    require_markers(
        "MVP audio policy",
        audio_policy,
        (
            "adapted sign tokens",
            "modern fluid device voice",
            "technical local synthesizer",
            "reconstructed Iberian pronunciation",
        ),
    )

    script = ENGINE.read_text(encoding="utf-8")
    corpus_renderer = CORPUS_RENDERER.read_text(encoding="utf-8")
    corpus_voice = CORPUS_VOICE.read_text(encoding="utf-8")
    require_markers(
        "voice engine",
        script,
        (
            'PROFILE_ID = "iberolab-sign-reading-voice-v3"',
            'TECHNICAL_PROFILE_ID = "iberolab-sign-reading-voice-v1"',
            'FLUID_PROFILE_ID = "iberolab-fluid-device-voice-v1"',
            'MODE_FLUID = "fluid"',
            'MODE_TECHNICAL = "technical"',
            'SOURCE_ATTESTED = "attested_iberian_form"',
            'SOURCE_MODERN = "modern_spanish_adaptation"',
            "normalizeSourceClass",
            "SAMPLE_RATE = 24000",
            "hashString",
            "makeRandom",
            "buildPlan",
            "synthesize",
            "fingerprint",
            "AudioContext",
            "webkitAudioContext",
            'PLAYBACK_SESSION_TYPE = "playback"',
            "root.navigator.audioSession",
            "renderSibilant",
            "renderRhotic",
            "buildFluidPlan",
            "selectFluidVoice",
            "SpeechSynthesisUtterance",
            "speechSynthesis",
            "root.AudioContext",
            '"ń": "n"',
        ),
    )
    for forbidden in ("fetch(", "XMLHttpRequest", "WebSocket"):
        if forbidden in script:
            raise ValueError(f"experimental voice engine must not depend on {forbidden}")

    public_doc = PUBLIC_DOC.read_text(encoding="utf-8")
    require_markers(
        "voice methodology",
        public_doc,
        (
            "no reconstruye cómo hablaban los íberos",
            "recreación sonora experimental",
            "Voz fluida moderna",
            "paleta euskérica moderna",
            "no constituye evidencia de parentesco",
            "Síntesis técnica reproducible",
            "formas ibéricas atestiguadas",
            "adaptaciones modernas",
            "`ń`",
            "`s` y `ś`",
            "`r` y `ŕ`",
            "10.36707/palaeohispanica.v0i20.370",
        ),
    )

    converter = CONVERTER.read_text(encoding="utf-8")
    converter_ui = CONVERTER_UI.read_text(encoding="utf-8")
    methodology = METHODOLOGY.read_text(encoding="utf-8")
    privacy = PRIVACY.read_text(encoding="utf-8")
    require_markers(
        "public converter",
        converter + "\n" + converter_ui,
        (
            'id="recreationButton"',
            'id="recreationMode"',
            "Fluida moderna · voz natural",
            "Técnica · síntesis reproducible",
            "Escuchar aproximación sonora",
            "No reconstruye cómo hablaban los íberos",
            'src="iberian-voice.js"',
            "iberolab-sign-reading-voice-v3",
            "sin afirmar parentesco",
            "sourceClass: window.IberoVoice.SOURCE_MODERN",
        ),
    )
    require_markers(
        "attested corpus voice",
        corpus_voice,
        (
            "Escuchar forma atestiguada",
            "Forma atestiguada · voz fluida",
            "Forma atestiguada · síntesis técnica",
            "iberolab-sign-reading-voice-v3",
            "La secuencia escrita está documentada; su sonido no",
            "VOICE_SCRIPT_PATH",
            "sourceClass: engine.SOURCE_ATTESTED",
            "ń",
            "nasal prolongada",
        ),
    )
    require_markers(
        "attested corpus voice loader",
        corpus_renderer,
        ('script.src = "corpus-voice.js"',),
    )
    require_markers(
        "public methodology",
        methodology,
        (
            "Dos orígenes, dos modos de recreación",
            "Voz fluida moderna",
            "Síntesis técnica",
            "No es una reconstrucción de cómo hablaban los íberos",
            "iberolab-sign-reading-voice-v3",
            "Forma atestiguada",
            "Entrada moderna",
        ),
    )
    require_markers(
        "privacy page",
        privacy,
        (
            "Audio en el dispositivo",
            "no envía a sus servidores el texto ni el audio",
            "modo técnico calcula íntegramente sus muestras",
            "formas atestiguadas",
        ),
    )

    return len(token_groups), len(source_urls)


if __name__ == "__main__":
    try:
        token_count, source_count = validate()
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"EXPERIMENTAL VOICE VALIDATION FAILED: {exc}", file=sys.stderr)
        raise SystemExit(1)
    print(
        "EXPERIMENTAL VOICE VALIDATION OK: "
        f"{token_count} tokens; {source_count} sources; fluid device voice plus deterministic technical synthesis; "
        "two source classes; historical-pronunciation claim disabled."
    )
