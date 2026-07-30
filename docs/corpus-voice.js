(() => {
  "use strict";

  const VOICE_SCRIPT_PATH = "iberian-voice.js";
  let voicePromise = null;
  let modeSelect = null;
  let playButton = null;
  let status = null;
  let activePlayback = null;
  let requestGeneration = 0;

  function loadVoiceEngine() {
    if (window.IberoVoice) return Promise.resolve(window.IberoVoice);
    if (voicePromise) return voicePromise;
    voicePromise = new Promise((resolve, reject) => {
      const script = document.createElement("script");
      script.src = VOICE_SCRIPT_PATH;
      script.async = true;
      script.addEventListener("load", () => {
        if (window.IberoVoice) resolve(window.IberoVoice);
        else reject(new Error("El motor sonoro no se ha inicializado."));
      }, { once: true });
      script.addEventListener("error", () => {
        reject(new Error("No se ha podido cargar el motor sonoro."));
      }, { once: true });
      document.head.append(script);
    });
    return voicePromise;
  }

  function selectedMode() {
    return modeSelect?.value || "fluid";
  }

  function currentForm() {
    const source = document.getElementById("readingText")?.textContent.trim() || "";
    const technicalReading = document.getElementById("tokenText")?.textContent.trim() || "";
    const tokens = technicalReading
      .split("·")
      .map(token => token.trim())
      .filter(Boolean);
    return { source, tokens };
  }

  function resetButton() {
    if (!playButton) return;
    playButton.textContent = "Escuchar forma atestiguada";
    playButton.setAttribute("aria-pressed", "false");
    playButton.disabled = !window.IberoVoice?.isModeSupported(selectedMode());
    document.documentElement.dataset.attestedVoiceState = "idle";
  }

  function stopPlayback({ announce = false } = {}) {
    requestGeneration += 1;
    if (activePlayback) {
      activePlayback.stop();
      activePlayback = null;
    } else {
      window.IberoVoice?.stop();
    }
    resetButton();
    if (announce && status) status.textContent = "Recreación detenida.";
  }

  async function playCurrentForm() {
    if (activePlayback) {
      stopPlayback({ announce: true });
      return;
    }

    const form = currentForm();
    const mode = selectedMode();
    const request = ++requestGeneration;
    if (!form.source || !form.tokens.length) {
      status.textContent = "No hay una lectura atestiguada disponible.";
      return;
    }

    playButton.disabled = true;
    status.textContent = mode === "fluid"
      ? "Preparando la voz fluida del dispositivo…"
      : "Preparando la síntesis técnica local…";

    try {
      const engine = await loadVoiceEngine();
      if (request !== requestGeneration) return;
      if (!engine.isModeSupported(mode)) {
        throw new Error("El modo sonoro no está disponible.");
      }
      const playback = await engine.play(
        [{ source: form.source, tokens: form.tokens }],
        { mode, sourceClass: engine.SOURCE_ATTESTED }
      );
      const latestForm = currentForm();
      if (
        request !== requestGeneration ||
        latestForm.source !== form.source ||
        latestForm.tokens.join("·") !== form.tokens.join("·") ||
        selectedMode() !== mode
      ) {
        playback.stop();
        return;
      }

      activePlayback = playback;
      playButton.disabled = false;
      playButton.textContent = "Detener recreación";
      playButton.setAttribute("aria-pressed", "true");
      document.documentElement.dataset.attestedVoiceState = "playing";
      status.textContent = playback.mode === "fluid"
        ? `Forma atestiguada · voz fluida (${playback.rendered.paletteLabel}): ${playback.rendered.spokenText}.`
        : `Forma atestiguada · síntesis técnica: ${playback.rendered.reading}.`;

      playback.ended.then(() => {
        if (activePlayback !== playback) return;
        activePlayback = null;
        resetButton();
        status.textContent = "Recreación sonora finalizada.";
      });
    } catch {
      if (request !== requestGeneration) return;
      activePlayback = null;
      resetButton();
      status.textContent = "No se ha podido reproducir esta recreación en el navegador.";
    }
  }

  function mountControls() {
    const tokenText = document.getElementById("tokenText");
    const technical = tokenText?.closest(".technical");
    if (!technical) return;

    const section = document.createElement("section");
    section.className = "technical";
    section.setAttribute("aria-label", "Recreación sonora de la forma ibérica atestiguada");
    section.innerHTML = `
      <div class="controls">
        <div>
          <label for="attestedVoiceMode">Recreación sonora de esta lectura</label>
          <select id="attestedVoiceMode">
            <option value="fluid" selected>Fluida moderna · voz natural</option>
            <option value="technical">Técnica · síntesis reproducible</option>
          </select>
        </div>
        <button id="attestedVoiceButton" class="secondary" type="button" aria-pressed="false">
          Escuchar forma atestiguada
        </button>
      </div>
      <div class="transcription-note">
        La secuencia escrita está documentada; su sonido no. Esta función vocaliza valores convencionales mediante el perfil <code>iberolab-sign-reading-voice-v3</code>, no una pronunciación histórica. Para <code>ń</code>, la voz fluida usa <code>n</code> y la técnica una nasal prolongada como convención de baja confianza.
      </div>
      <div id="attestedVoiceStatus" class="position" role="status" aria-live="polite"></div>
    `;
    technical.insertAdjacentElement("afterend", section);
    modeSelect = section.querySelector("#attestedVoiceMode");
    playButton = section.querySelector("#attestedVoiceButton");
    status = section.querySelector("#attestedVoiceStatus");
    playButton.disabled = true;

    playButton.addEventListener("click", playCurrentForm);
    modeSelect.addEventListener("change", () => {
      stopPlayback();
      status.textContent = "";
      resetButton();
    });
    for (const controlId of [
      "formSelect",
      "renderButton",
      "previousButton",
      "nextButton"
    ]) {
      document.getElementById(controlId)?.addEventListener("click", () => stopPlayback());
    }
    document.getElementById("formSelect")?.addEventListener("change", () => stopPlayback());
    window.addEventListener("hashchange", () => stopPlayback());
    window.addEventListener("pagehide", () => stopPlayback());

    loadVoiceEngine()
      .then(engine => {
        document.documentElement.dataset.attestedVoiceProfile = engine.PROFILE_ID;
        resetButton();
      })
      .catch(() => {
        playButton.disabled = true;
        status.textContent = "El motor sonoro no está disponible en este navegador.";
      });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", mountControls, { once: true });
  } else {
    mountControls();
  }
})();
