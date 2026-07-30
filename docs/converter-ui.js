(() => {
  "use strict";

  const form = document.getElementById("converterForm");
  const input = document.getElementById("sourceInput");
  const counter = document.getElementById("characterCounter");
  const output = document.getElementById("glyphOutput");
  const normalizedText = document.getElementById("normalizedText");
  const technicalReading = document.getElementById("technicalReading");
  const statusBadge = document.getElementById("statusBadge");
  const noticeList = document.getElementById("noticeList");
  const speakButton = document.getElementById("speakButton");
  const recreationMode = document.getElementById("recreationMode");
  const voiceModeDescription = document.getElementById("voiceModeDescription");
  const recreationButton = document.getElementById("recreationButton");
  const copyButton = document.getElementById("copyButton");
  const shareButton = document.getElementById("shareButton");
  const actionStatus = document.getElementById("actionStatus");
  const historySection = document.getElementById("historySection");
  const historyList = document.getElementById("historyList");
  const clearHistoryButton = document.getElementById("clearHistoryButton");

  const HISTORY_KEY = "iberolab:mvp:recent:v1";
  const HISTORY_LIMIT = 5;
  const RECREATION_LABEL = "Escuchar aproximación sonora";
  const VOICE_MODE_COPY = Object.freeze({
    fluid: "<strong>Fluida moderna:</strong> articula la lectura como palabras completas con una voz actual del dispositivo. Prefiere una voz moderna en euskera por su ajuste fonético, sin afirmar parentesco con la lengua ibérica.",
    technical: "<strong>Técnica reproducible:</strong> genera la señal de 24 kHz signo a signo mediante el sintetizador de formantes de IberoLab. Es más mecánica, pero permite comparar exactamente el mismo experimento."
  });
  let currentResult = null;
  let activeRecreation = null;

  function updateCounter() {
    counter.textContent = `${Array.from(input.value).length}/${window.IberoMvp.MAX_CHARACTERS} caracteres · máximo ${window.IberoMvp.MAX_WORDS} palabras`;
  }

  function readHistory() {
    try {
      const parsed = JSON.parse(localStorage.getItem(HISTORY_KEY) || "[]");
      return Array.isArray(parsed)
        ? parsed.filter(item => typeof item === "string" && item.trim()).slice(0, HISTORY_LIMIT)
        : [];
    } catch {
      return [];
    }
  }

  function writeHistory(entries) {
    try {
      if (entries.length) localStorage.setItem(HISTORY_KEY, JSON.stringify(entries));
      else localStorage.removeItem(HISTORY_KEY);
      return true;
    } catch {
      return false;
    }
  }

  function renderHistory() {
    const entries = readHistory();
    historyList.replaceChildren();
    historySection.hidden = entries.length === 0;
    for (const value of entries) {
      const button = document.createElement("button");
      button.className = "history-item";
      button.type = "button";
      button.dataset.historyValue = value;
      button.textContent = value;
      button.addEventListener("click", () => {
        input.value = value;
        updateCounter();
        convert();
        input.focus();
      });
      historyList.append(button);
    }
  }

  function rememberResult(result) {
    if (result.executionStatus !== "success") return;
    const value = result.original.trim();
    if (!value) return;
    const key = value.toLocaleLowerCase("es-ES");
    const entries = [
      value,
      ...readHistory().filter(item => item.toLocaleLowerCase("es-ES") !== key)
    ].slice(0, HISTORY_LIMIT);
    if (writeHistory(entries)) renderHistory();
  }

  function createSignCard(token) {
    const card = document.createElement("div");
    card.className = "sign-card";
    card.setAttribute("role", "img");
    card.setAttribute("aria-label", `Signo ibérico normalizado de referencia para ${token}`);
    const image = document.createElement("img");
    image.src = window.IberoMvp.SIGN_PATHS[token];
    image.alt = `Signo ibérico normalizado para ${token}`;
    image.loading = "eager";
    const fallback = document.createElement("div");
    fallback.className = "glyph-fallback";
    fallback.textContent = `${token}\nimagen no cargada`;
    image.addEventListener("error", () => card.classList.add("failed"), { once: true });
    const label = document.createElement("div");
    label.className = "sign-token";
    label.textContent = token;
    card.append(image, fallback, label);
    return card;
  }

  function renderNotices(result) {
    noticeList.replaceChildren();
    const combined = [
      ...result.operations.map(item => ({ ...item, severity: "information" })),
      ...result.notices
    ];
    if (!combined.length) {
      const item = document.createElement("div");
      item.className = "empty-explanation";
      item.textContent = "La entrada se ha representado con correspondencias directas dentro de las convenciones del MVP.";
      noticeList.append(item);
      return;
    }
    for (const notice of combined) {
      const item = document.createElement("div");
      item.className = `notice-item ${notice.severity}`;
      item.textContent = notice.message;
      noticeList.append(item);
    }
  }

  function resetRecreationButton() {
    recreationButton.textContent = RECREATION_LABEL;
    recreationButton.setAttribute("aria-pressed", "false");
  }

  function selectedVoiceMode() {
    return recreationMode?.value === "technical" ? "technical" : "fluid";
  }

  function refreshVoiceMode() {
    let mode = selectedVoiceMode();
    if (
      window.IberoVoice &&
      !window.IberoVoice.isModeSupported(mode) &&
      window.IberoVoice.isModeSupported("technical")
    ) {
      recreationMode.value = "technical";
      mode = "technical";
    }
    if (voiceModeDescription) voiceModeDescription.innerHTML = VOICE_MODE_COPY[mode];
    if (!recreationButton || !currentResult || currentResult.executionStatus !== "success") return;
    recreationButton.disabled = !window.IberoVoice?.isModeSupported(mode);
  }

  function stopRecreation({ announce = false } = {}) {
    if (activeRecreation) {
      activeRecreation.stop();
      activeRecreation = null;
      if (announce) actionStatus.textContent = "Recreación detenida.";
    } else if (window.IberoVoice) {
      window.IberoVoice.stop();
    }
    resetRecreationButton();
  }

  function renderResult(result) {
    stopRecreation();
    currentResult = result;
    output.replaceChildren();
    document.documentElement.dataset.mvpResult = result.executionStatus;
    document.documentElement.dataset.mvpStatus = result.status;

    if (result.executionStatus === "blocked") {
      const message = document.createElement("div");
      message.className = "blocked-message";
      message.textContent = result.notices[0].message;
      output.append(message);
      normalizedText.textContent = "Entrada bloqueada";
      technicalReading.textContent = "—";
      statusBadge.className = "badge blocked";
      statusBadge.textContent = "No se ha generado una salida";
      speakButton.disabled = true;
      recreationButton.disabled = true;
      copyButton.disabled = true;
      shareButton.disabled = true;
      actionStatus.textContent = "";
      renderNotices(result);
      return;
    }

    result.words.forEach((word, index) => {
      if (index > 0) {
        const separator = document.createElement("span");
        separator.className = "word-separator";
        separator.setAttribute("aria-hidden", "true");
        separator.textContent = "·";
        output.append(separator);
      }
      const group = document.createElement("div");
      group.className = "word-group";
      group.dataset.sourceWord = word.source;
      const wordLabel = document.createElement("div");
      wordLabel.className = "word-label";
      wordLabel.textContent = word.source;
      const signs = document.createElement("div");
      signs.className = "word-signs";
      signs.append(...word.tokens.map(createSignCard));
      group.append(wordLabel, signs);
      output.append(group);
    });

    normalizedText.textContent = result.normalized;
    technicalReading.textContent = result.technicalReading;
    statusBadge.className = `badge ${result.status}`;
    statusBadge.textContent = result.status === "direct"
      ? "Adaptación directa"
      : "Adaptación con aproximaciones";
    speakButton.disabled = !("speechSynthesis" in window);
    recreationButton.disabled = !window.IberoVoice?.isModeSupported(selectedVoiceMode());
    copyButton.disabled = false;
    shareButton.disabled = false;
    actionStatus.textContent = "";
    renderNotices(result);
  }

  function resultUrl(value = input.value) {
    const url = new URL(location.href);
    const trimmed = value.trim();
    if (trimmed) url.searchParams.set("q", trimmed);
    else url.searchParams.delete("q");
    return url;
  }

  function convert({ updateUrl = true, remember = true } = {}) {
    const result = window.IberoMvp.convert(input.value);
    renderResult(result);
    if (remember) rememberResult(result);
    if (updateUrl) {
      const url = resultUrl();
      history.replaceState(null, "", `${url.pathname}${url.search}${url.hash}`);
    }
  }

  function loadFromUrl() {
    const sharedInput = new URL(location.href).searchParams.get("q");
    if (sharedInput !== null) input.value = sharedInput;
    updateCounter();
    convert({ updateUrl: false, remember: false });
  }

  form.addEventListener("submit", event => {
    event.preventDefault();
    convert();
  });
  input.addEventListener("input", updateCounter);
  for (const button of document.querySelectorAll("[data-example]")) {
    button.addEventListener("click", () => {
      input.value = button.dataset.example;
      updateCounter();
      convert();
      input.focus();
    });
  }

  clearHistoryButton.addEventListener("click", () => {
    if (writeHistory([])) {
      renderHistory();
      actionStatus.textContent = "Historial local borrado.";
      setTimeout(() => {
        actionStatus.textContent = "";
      }, 1600);
    } else {
      actionStatus.textContent = "El navegador no ha permitido borrar el historial local.";
    }
  });

  recreationMode.addEventListener("change", () => {
    stopRecreation();
    refreshVoiceMode();
    actionStatus.textContent = "";
  });

  speakButton.addEventListener("click", () => {
    if (
      !currentResult ||
      currentResult.executionStatus !== "success" ||
      !("speechSynthesis" in window)
    ) return;
    stopRecreation();
    speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(currentResult.original);
    utterance.lang = "es-ES";
    utterance.rate = 0.9;
    speechSynthesis.speak(utterance);
  });

  recreationButton.addEventListener("click", async () => {
    if (activeRecreation) {
      stopRecreation({ announce: true });
      return;
    }
    if (
      !currentResult ||
      currentResult.executionStatus !== "success" ||
      !window.IberoVoice?.isModeSupported(selectedVoiceMode())
    ) {
      actionStatus.textContent = "Este navegador no permite iniciar la recreación sonora.";
      return;
    }

    const resultAtStart = currentResult;
    const modeAtStart = selectedVoiceMode();
    if (modeAtStart === "technical" && "speechSynthesis" in window) {
      speechSynthesis.cancel();
    }
    recreationButton.disabled = true;
    actionStatus.textContent = modeAtStart === "fluid"
      ? "Preparando la voz fluida del dispositivo…"
      : "Preparando la síntesis técnica local…";

    try {
      const playback = await window.IberoVoice.play(resultAtStart.words, {
        mode: modeAtStart,
        sourceClass: window.IberoVoice.SOURCE_MODERN
      });
      if (currentResult !== resultAtStart || selectedVoiceMode() !== modeAtStart) {
        playback.stop();
        return;
      }
      activeRecreation = playback;
      recreationButton.disabled = false;
      recreationButton.textContent = "Detener aproximación";
      recreationButton.setAttribute("aria-pressed", "true");
      actionStatus.textContent = playback.mode === "fluid"
        ? `Voz fluida (${playback.rendered.paletteLabel}): ${playback.rendered.spokenText}.`
        : `Síntesis técnica: ${playback.rendered.reading}.`;
      playback.ended.then(() => {
        if (activeRecreation !== playback) return;
        activeRecreation = null;
        resetRecreationButton();
        actionStatus.textContent = "Recreación sonora finalizada.";
        setTimeout(() => {
          if (!activeRecreation && actionStatus.textContent === "Recreación sonora finalizada.") {
            actionStatus.textContent = "";
          }
        }, 1800);
      });
    } catch {
      activeRecreation = null;
      recreationButton.disabled = false;
      resetRecreationButton();
      actionStatus.textContent = "No se ha podido reproducir la recreación en este navegador.";
    }
  });

  copyButton.addEventListener("click", async () => {
    if (!currentResult || currentResult.executionStatus !== "success") return;
    try {
      await navigator.clipboard.writeText(currentResult.technicalReading);
      copyButton.textContent = "Lectura copiada";
      actionStatus.textContent = "La lectura técnica se ha copiado.";
      setTimeout(() => {
        copyButton.textContent = "Copiar lectura técnica";
        actionStatus.textContent = "";
      }, 1600);
    } catch {
      copyButton.textContent = "No se pudo copiar";
      actionStatus.textContent = "El navegador no ha permitido copiar la lectura.";
    }
  });

  shareButton.addEventListener("click", async () => {
    if (!currentResult || currentResult.executionStatus !== "success") return;
    const url = resultUrl(currentResult.original).toString();
    const text = `IberoLab — ${currentResult.original}\n${currentResult.technicalReading}\nAdaptación fonética experimental; no es una traducción.`;
    try {
      if (typeof navigator.share === "function") {
        await navigator.share({ title: "IberoLab", text, url });
        actionStatus.textContent = "Resultado compartido.";
      } else {
        await navigator.clipboard.writeText(`${text}\n${url}`);
        actionStatus.textContent = "Enlace y lectura copiados para compartir.";
      }
      setTimeout(() => {
        actionStatus.textContent = "";
      }, 2200);
    } catch (error) {
      if (error?.name !== "AbortError") {
        actionStatus.textContent = "No se pudo compartir el resultado.";
      }
    }
  });

  addEventListener("popstate", loadFromUrl);
  addEventListener("pagehide", () => stopRecreation());
  renderHistory();
  refreshVoiceMode();
  loadFromUrl();
  document.documentElement.dataset.mvpConverterReady = "true";
  document.documentElement.dataset.experimentalVoiceProfile = window.IberoVoice?.PROFILE_ID || "unavailable";
})();
