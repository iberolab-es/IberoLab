(function attachIberoVoice(root, factory) {
  "use strict";
  const api = factory(root);
  if (typeof module === "object" && module.exports) module.exports = api;
  root.IberoVoice = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function createIberoVoice(root) {
  "use strict";

  const VERSION = "0.2.0";
  const PROFILE_ID = "iberolab-sign-reading-voice-v2";
  const TECHNICAL_PROFILE_ID = "iberolab-sign-reading-voice-v1";
  const FLUID_PROFILE_ID = "iberolab-fluid-device-voice-v1";
  const MODE_FLUID = "fluid";
  const MODE_TECHNICAL = "technical";
  const PLAYBACK_SESSION_TYPE = "playback";
  const SAMPLE_RATE = 24000;
  const EDGE_SILENCE_SECONDS = 0.06;
  const TOKEN_GAP_SECONDS = 0.032;
  const WORD_GAP_SECONDS = 0.18;
  const BASE_PITCH_HZ = 122;

  const VOWEL_FORMANTS = Object.freeze({
    a: [[730, 170, 1], [1090, 230, 0.82], [2440, 320, 0.48]],
    e: [[530, 150, 1], [1840, 260, 0.88], [2480, 340, 0.42]],
    i: [[280, 130, 1], [2290, 250, 0.92], [3010, 350, 0.4]],
    o: [[570, 160, 1], [840, 210, 0.82], [2410, 330, 0.43]],
    u: [[300, 135, 1], [870, 220, 0.78], [2240, 330, 0.4]]
  });

  const STOP_TOKENS = Object.freeze({
    ba: ["b", "a"], be: ["b", "e"], bi: ["b", "i"], bo: ["b", "o"], bu: ["b", "u"],
    da: ["d", "a"], de: ["d", "e"], di: ["d", "i"], do: ["d", "o"], du: ["d", "u"],
    ta: ["t", "a"], te: ["t", "e"], ti: ["t", "i"], to: ["t", "o"], tu: ["t", "u"],
    ga: ["g", "a"], ge: ["g", "e"], gi: ["g", "i"], go: ["g", "o"], gu: ["g", "u"],
    ka: ["k", "a"], ke: ["k", "e"], ki: ["k", "i"], ko: ["k", "o"], ku: ["k", "u"]
  });

  const CONTINUANT_TOKENS = new Set(["s", "ś", "r", "ŕ", "l", "m", "n", "ḿ"]);
  const FLUID_LANGUAGE_PREFERENCES = Object.freeze(["eu-ES", "eu", "ca-ES", "ca", "es-ES", "es"]);
  const FLUID_PALETTES = Object.freeze({
    eu: Object.freeze({
      id: "modern-basque-orthographic-bridge",
      label: "paleta moderna en euskera",
      tokenText: Object.freeze({
        s: "z",
        "ś": "s",
        r: "r",
        "ŕ": "rr",
        l: "l",
        m: "m",
        n: "n",
        "ḿ": "um"
      })
    }),
    ca: Object.freeze({
      id: "modern-mediterranean-orthographic-bridge",
      label: "paleta mediterránea moderna",
      tokenText: Object.freeze({
        s: "s",
        "ś": "x",
        r: "r",
        "ŕ": "rr",
        l: "l",
        m: "m",
        n: "n",
        "ḿ": "um"
      })
    }),
    es: Object.freeze({
      id: "modern-peninsular-orthographic-bridge",
      label: "paleta peninsular moderna",
      tokenText: Object.freeze({
        s: "s",
        "ś": "sh",
        r: "r",
        "ŕ": "rr",
        l: "l",
        m: "m",
        n: "n",
        "ḿ": "um"
      })
    })
  });
  const VALID_TOKENS = new Set([
    ...Object.keys(VOWEL_FORMANTS),
    ...Object.keys(STOP_TOKENS),
    ...CONTINUANT_TOKENS
  ]);

  let audioContext = null;
  let activePlayback = null;

  function fail(message) {
    throw new TypeError(message);
  }

  function normalizeWords(words) {
    if (!Array.isArray(words) || words.length === 0) {
      fail("La recreación necesita al menos una palabra adaptada.");
    }
    return words.map((word, wordIndex) => {
      const tokens = Array.isArray(word) ? word : word && word.tokens;
      if (!Array.isArray(tokens) || tokens.length === 0) {
        fail(`La palabra ${wordIndex + 1} no contiene tokens sonoros.`);
      }
      const normalizedTokens = tokens.map(token => String(token));
      const unsupported = normalizedTokens.find(token => !VALID_TOKENS.has(token));
      if (unsupported) {
        fail(`El perfil sonoro ${PROFILE_ID} no admite el token «${unsupported}».`);
      }
      return {
        source: !Array.isArray(word) && typeof word.source === "string" ? word.source : "",
        tokens: normalizedTokens
      };
    });
  }

  function tokenKind(token) {
    if (VOWEL_FORMANTS[token]) return "vowel";
    if (STOP_TOKENS[token]) return "stop_syllabogram";
    if (token === "s" || token === "ś") return "sibilant";
    if (token === "r" || token === "ŕ") return "rhotic";
    if (token === "m" || token === "n" || token === "ḿ") return "nasal";
    return "lateral";
  }

  function tokenDuration(token) {
    if (VOWEL_FORMANTS[token]) return 0.19;
    if (STOP_TOKENS[token]) return 0.245;
    if (token === "s" || token === "ś") return 0.15;
    if (token === "r") return 0.082;
    if (token === "ŕ") return 0.155;
    if (token === "ḿ") return 0.165;
    return 0.13;
  }

  function buildPlan(words) {
    const normalizedWords = normalizeWords(words);
    const items = [];
    let cursor = EDGE_SILENCE_SECONDS;

    normalizedWords.forEach((word, wordIndex) => {
      if (wordIndex > 0) cursor += WORD_GAP_SECONDS;
      word.tokens.forEach((token, tokenIndex) => {
        const duration = tokenDuration(token);
        items.push({
          token,
          kind: tokenKind(token),
          wordIndex,
          tokenIndex,
          startSeconds: cursor,
          durationSeconds: duration
        });
        cursor += duration;
        if (tokenIndex < word.tokens.length - 1) cursor += TOKEN_GAP_SECONDS;
      });
    });

    const reading = normalizedWords
      .map(word => word.tokens.join(" · "))
      .join(" / ");

    return {
      profileId: TECHNICAL_PROFILE_ID,
      version: VERSION,
      words: normalizedWords,
      reading,
      items,
      durationSeconds: cursor + EDGE_SILENCE_SECONDS
    };
  }

  function languageFamily(language) {
    const normalized = String(language || "").toLocaleLowerCase("en");
    if (normalized.startsWith("eu")) return "eu";
    if (normalized.startsWith("ca")) return "ca";
    return "es";
  }

  function availableVoices() {
    if (!root.speechSynthesis || typeof root.speechSynthesis.getVoices !== "function") return [];
    try {
      const voices = root.speechSynthesis.getVoices();
      return Array.isArray(voices) ? voices : Array.from(voices || []);
    } catch {
      return [];
    }
  }

  function selectFluidVoice() {
    const voices = availableVoices();
    for (const preferredLanguage of FLUID_LANGUAGE_PREFERENCES) {
      const exact = voices.find(voice =>
        String(voice.lang || "").toLocaleLowerCase("en") ===
        preferredLanguage.toLocaleLowerCase("en")
      );
      if (exact) {
        return {
          voice: exact,
          language: exact.lang || preferredLanguage,
          palette: FLUID_PALETTES[languageFamily(exact.lang || preferredLanguage)],
          requestedLanguage: preferredLanguage
        };
      }
      if (!preferredLanguage.includes("-")) {
        const family = voices.find(voice =>
          languageFamily(voice.lang) === preferredLanguage.toLocaleLowerCase("en")
        );
        if (family) {
          return {
            voice: family,
            language: family.lang || preferredLanguage,
            palette: FLUID_PALETTES[languageFamily(family.lang || preferredLanguage)],
            requestedLanguage: preferredLanguage
          };
        }
      }
    }

    return {
      voice: null,
      language: "eu-ES",
      palette: FLUID_PALETTES.eu,
      requestedLanguage: "eu-ES"
    };
  }

  function stopTokenText(token, paletteFamily) {
    const [consonant, vowel] = STOP_TOKENS[token];
    if (paletteFamily === "eu") return `${consonant}${vowel}`;
    if (consonant === "g" && (vowel === "e" || vowel === "i")) return `gu${vowel}`;
    return `${consonant}${vowel}`;
  }

  function fluidTokenText(token, palette) {
    if (VOWEL_FORMANTS[token]) return token;
    if (STOP_TOKENS[token]) {
      const paletteFamily = palette === FLUID_PALETTES.eu
        ? "eu"
        : palette === FLUID_PALETTES.ca
          ? "ca"
          : "es";
      return stopTokenText(token, paletteFamily);
    }
    return palette.tokenText[token];
  }

  function buildFluidPlan(words, voiceSelection = selectFluidVoice()) {
    const normalizedWords = normalizeWords(words);
    const palette = voiceSelection.palette || FLUID_PALETTES.eu;
    const spokenWords = normalizedWords.map(word => {
      const spoken = word.tokens.map(token => fluidTokenText(token, palette)).join("");
      return /[aeiou]/i.test(spoken) ? spoken : `${spoken}e`;
    });
    const reading = normalizedWords
      .map(word => word.tokens.join(" · "))
      .join(" / ");

    return {
      profileId: FLUID_PROFILE_ID,
      version: VERSION,
      mode: MODE_FLUID,
      reading,
      words: normalizedWords,
      spokenWords,
      spokenText: spokenWords.join(", "),
      language: voiceSelection.language || "eu-ES",
      requestedLanguage: voiceSelection.requestedLanguage || "eu-ES",
      paletteId: palette.id,
      paletteLabel: palette.label,
      voice: voiceSelection.voice || null,
      voiceName: voiceSelection.voice?.name || "",
      deterministic: false,
      historicalRelationshipClaim: false
    };
  }

  function hashString(value) {
    let hash = 2166136261;
    for (const character of value) {
      hash ^= character.codePointAt(0);
      hash = Math.imul(hash, 16777619);
    }
    return hash >>> 0;
  }

  function makeRandom(seed) {
    let state = seed || 0x6d2b79f5;
    return function random() {
      state |= 0;
      state = state + 0x6d2b79f5 | 0;
      let value = Math.imul(state ^ state >>> 15, 1 | state);
      value = value + Math.imul(value ^ value >>> 7, 61 | value) ^ value;
      return ((value ^ value >>> 14) >>> 0) / 4294967296;
    };
  }

  function envelope(time, duration, attack = 0.014, release = 0.026) {
    const onset = Math.min(1, time / attack);
    const offset = Math.min(1, Math.max(0, duration - time) / release);
    return Math.max(0, Math.min(onset, offset));
  }

  function createHarmonicProfile(formants, pitch) {
    const harmonicCount = Math.max(12, Math.min(48, Math.floor(5600 / pitch)));
    const amplitudes = [];
    let energy = 0;

    for (let harmonic = 1; harmonic <= harmonicCount; harmonic += 1) {
      const frequency = harmonic * pitch;
      let resonance = 0.018;
      for (const [centre, bandwidth, weight] of formants) {
        const distance = (frequency - centre) / bandwidth;
        resonance += weight * Math.exp(-0.5 * distance * distance);
      }
      const amplitude = resonance / Math.pow(harmonic, 0.72);
      amplitudes.push(amplitude);
      energy += amplitude * amplitude;
    }

    const normalizer = Math.sqrt(energy) || 1;
    return amplitudes.map(value => value / normalizer);
  }

  function addVoicedSegment(
    samples,
    startSeconds,
    durationSeconds,
    formants,
    pitch,
    random,
    gain,
    options = {}
  ) {
    const start = Math.round(startSeconds * SAMPLE_RATE);
    const length = Math.max(1, Math.round(durationSeconds * SAMPLE_RATE));
    const targetProfile = createHarmonicProfile(formants, pitch);
    const onsetFormants = options.onsetFormants || formants;
    const onsetProfile = createHarmonicProfile(onsetFormants, pitch);
    let phase = (random() * Math.PI * 2);

    for (let offset = 0; offset < length && start + offset < samples.length; offset += 1) {
      const time = offset / SAMPLE_RATE;
      const progress = time / durationSeconds;
      const localPitch = pitch * (1 - 0.018 * progress + 0.004 * Math.sin(2 * Math.PI * 4.3 * time));
      phase += 2 * Math.PI * localPitch / SAMPLE_RATE;
      const transition = Math.min(1, time / 0.045);
      let value = 0;

      for (let harmonic = 1; harmonic <= targetProfile.length; harmonic += 1) {
        const onset = onsetProfile[harmonic - 1] || 0;
        const target = targetProfile[harmonic - 1];
        const amplitude = onset + (target - onset) * transition;
        value += amplitude * Math.sin(harmonic * phase + harmonic * 0.11);
      }

      const modulation = typeof options.modulation === "function"
        ? options.modulation(time, durationSeconds)
        : 1;
      const breath = (random() * 2 - 1) * 0.012;
      samples[start + offset] += (value + breath) *
        envelope(time, durationSeconds, options.attack, options.release) *
        modulation *
        gain;
    }
  }

  function addBandNoise(samples, startSeconds, durationSeconds, centreHz, bandwidthHz, random, gain) {
    const start = Math.round(startSeconds * SAMPLE_RATE);
    const length = Math.max(1, Math.round(durationSeconds * SAMPLE_RATE));
    const temporary = new Float32Array(length);
    const radius = Math.exp(-Math.PI * bandwidthHz / SAMPLE_RATE);
    const coefficient = 2 * radius * Math.cos(2 * Math.PI * centreHz / SAMPLE_RATE);
    const radiusSquared = radius * radius;
    let previous = 0;
    let beforePrevious = 0;
    let peak = 0;

    for (let index = 0; index < length; index += 1) {
      const white = random() * 2 - 1;
      const current = (1 - radius) * white + coefficient * previous - radiusSquared * beforePrevious;
      temporary[index] = current;
      beforePrevious = previous;
      previous = current;
      peak = Math.max(peak, Math.abs(current));
    }

    const scale = peak > 0 ? gain / peak : 0;
    for (let index = 0; index < length && start + index < samples.length; index += 1) {
      const time = index / SAMPLE_RATE;
      samples[start + index] += temporary[index] *
        scale *
        envelope(time, durationSeconds, 0.008, 0.018);
    }
  }

  function renderVowel(samples, item, vowel, pitch, random, gain = 0.55, onsetF2 = null) {
    const target = VOWEL_FORMANTS[vowel];
    const onset = onsetF2
      ? [target[0], [onsetF2, target[1][1], target[1][2]], target[2]]
      : target;
    addVoicedSegment(
      samples,
      item.startSeconds,
      item.durationSeconds,
      target,
      pitch,
      random,
      gain,
      { onsetFormants: onset }
    );
  }

  function renderStop(samples, item, consonant, vowel, pitch, random) {
    const voiced = consonant === "b" || consonant === "d" || consonant === "g";
    const closure = voiced ? 0.052 : 0.06;
    const burst = voiced ? 0.019 : 0.026;
    const burstStart = item.startSeconds + closure;
    const vowelStart = burstStart + burst;
    const vowelDuration = Math.max(0.12, item.durationSeconds - closure - burst);
    const place = consonant === "b"
      ? { centre: 900, bandwidth: 800, onsetF2: 700 }
      : consonant === "d" || consonant === "t"
        ? { centre: 3600, bandwidth: 1500, onsetF2: 1750 }
        : { centre: 1900, bandwidth: 1000, onsetF2: 1350 };

    if (voiced) {
      addVoicedSegment(
        samples,
        item.startSeconds,
        closure,
        [[220, 150, 1], [900, 280, 0.35], [2100, 400, 0.18]],
        pitch * 0.84,
        random,
        0.13,
        { attack: 0.008, release: 0.01 }
      );
    }
    addBandNoise(
      samples,
      burstStart,
      burst,
      place.centre,
      place.bandwidth,
      random,
      voiced ? 0.25 : 0.38
    );
    renderVowel(
      samples,
      {
        startSeconds: vowelStart,
        durationSeconds: vowelDuration
      },
      vowel,
      pitch,
      random,
      0.56,
      place.onsetF2
    );
  }

  function renderSibilant(samples, item, token, random) {
    if (token === "s") {
      addBandNoise(samples, item.startSeconds, item.durationSeconds, 6600, 2100, random, 0.48);
    } else {
      addBandNoise(samples, item.startSeconds, item.durationSeconds, 4300, 1450, random, 0.5);
    }
  }

  function renderRhotic(samples, item, token, pitch, random) {
    const formants = [[460, 200, 0.72], [1450, 300, 0.55], [2500, 380, 0.32]];
    if (token === "r") {
      addVoicedSegment(samples, item.startSeconds, item.durationSeconds, formants, pitch, random, 0.34, {
        attack: 0.006,
        release: 0.01,
        modulation(time, duration) {
          const contact = Math.abs(time - duration * 0.48) < 0.009;
          return contact ? 0.08 : 0.82;
        }
      });
      return;
    }
    addVoicedSegment(samples, item.startSeconds, item.durationSeconds, formants, pitch, random, 0.38, {
      attack: 0.008,
      release: 0.014,
      modulation(time) {
        const opening = 0.5 + 0.5 * Math.sin(2 * Math.PI * 23 * time - Math.PI / 2);
        return 0.08 + 0.92 * opening * opening;
      }
    });
  }

  function renderNasal(samples, item, token, pitch, random) {
    const formants = token === "n"
      ? [[280, 170, 1], [1650, 340, 0.32], [2600, 430, 0.2]]
      : token === "ḿ"
        ? [[270, 180, 1], [1050, 360, 0.38], [2050, 450, 0.22]]
        : [[250, 160, 1], [1050, 330, 0.34], [2150, 430, 0.2]];
    addVoicedSegment(samples, item.startSeconds, item.durationSeconds, formants, pitch * 0.96, random, 0.34, {
      attack: 0.012,
      release: 0.02,
      modulation: token === "ḿ"
        ? time => 0.82 + 0.1 * Math.sin(2 * Math.PI * 5 * time)
        : undefined
    });
  }

  function renderLateral(samples, item, pitch, random) {
    addVoicedSegment(
      samples,
      item.startSeconds,
      item.durationSeconds,
      [[360, 180, 0.9], [1250, 300, 0.56], [2700, 420, 0.25]],
      pitch,
      random,
      0.36,
      { attack: 0.01, release: 0.018 }
    );
  }

  function normalizeSamples(samples) {
    let previousInput = 0;
    let previousOutput = 0;
    let peak = 0;
    for (let index = 0; index < samples.length; index += 1) {
      const current = samples[index] - previousInput + 0.995 * previousOutput;
      previousInput = samples[index];
      previousOutput = current;
      samples[index] = current;
      peak = Math.max(peak, Math.abs(current));
    }
    const scale = peak > 0 ? Math.min(1.8, 0.92 / peak) : 0;
    for (let index = 0; index < samples.length; index += 1) samples[index] *= scale;
    return peak * scale;
  }

  function synthesize(words) {
    const plan = buildPlan(words);
    const samples = new Float32Array(Math.ceil(plan.durationSeconds * SAMPLE_RATE));
    const random = makeRandom(hashString(`${TECHNICAL_PROFILE_ID}|${plan.reading}`));

    for (const item of plan.items) {
      const phraseProgress = item.startSeconds / plan.durationSeconds;
      const pitch = BASE_PITCH_HZ - 13 * phraseProgress + 2 * Math.sin(item.wordIndex * 0.9);
      if (item.kind === "vowel") {
        renderVowel(samples, item, item.token, pitch, random);
      } else if (item.kind === "stop_syllabogram") {
        const [consonant, vowel] = STOP_TOKENS[item.token];
        renderStop(samples, item, consonant, vowel, pitch, random);
      } else if (item.kind === "sibilant") {
        renderSibilant(samples, item, item.token, random);
      } else if (item.kind === "rhotic") {
        renderRhotic(samples, item, item.token, pitch, random);
      } else if (item.kind === "nasal") {
        renderNasal(samples, item, item.token, pitch, random);
      } else {
        renderLateral(samples, item, pitch, random);
      }
    }

    const peak = normalizeSamples(samples);
    return {
      profileId: TECHNICAL_PROFILE_ID,
      version: VERSION,
      mode: MODE_TECHNICAL,
      sampleRate: SAMPLE_RATE,
      samples,
      reading: plan.reading,
      words: plan.words,
      items: plan.items,
      durationSeconds: samples.length / SAMPLE_RATE,
      peak
    };
  }

  function fingerprint(rendered) {
    if (!rendered || !(rendered.samples instanceof Float32Array)) {
      fail("La huella necesita una síntesis válida.");
    }
    let hash = 2166136261;
    for (const sample of rendered.samples) {
      const quantized = Math.max(-32768, Math.min(32767, Math.round(sample * 32767)));
      hash ^= quantized & 0xffff;
      hash = Math.imul(hash, 16777619);
    }
    return (hash >>> 0).toString(16).padStart(8, "0");
  }

  function isPlaybackSupported() {
    return isModeSupported(MODE_FLUID) || isModeSupported(MODE_TECHNICAL);
  }

  function isModeSupported(mode) {
    if (mode === MODE_FLUID) {
      return Boolean(
        root.speechSynthesis &&
        typeof root.speechSynthesis.speak === "function" &&
        typeof root.speechSynthesis.cancel === "function" &&
        root.SpeechSynthesisUtterance
      );
    }
    if (mode === MODE_TECHNICAL) {
      return Boolean(root.AudioContext || root.webkitAudioContext);
    }
    return false;
  }

  function requestPlaybackAudioSession() {
    const session = root.navigator && root.navigator.audioSession;
    if (!session) return () => {};

    let previousType;
    try {
      previousType = session.type;
      session.type = PLAYBACK_SESSION_TYPE;
    } catch {
      return () => {};
    }

    let released = false;
    return function releasePlaybackAudioSession() {
      if (released) return;
      released = true;
      try {
        if (session.type === PLAYBACK_SESSION_TYPE) {
          session.type = previousType || "auto";
        }
      } catch {
        // The browser owns the audio session and may revoke access at any time.
      }
    };
  }

  function stop() {
    if (!activePlayback) return;
    const playback = activePlayback;
    activePlayback = null;
    playback.stopInternal();
  }

  async function playTechnical(words) {
    const AudioContextConstructor = root.AudioContext || root.webkitAudioContext;
    if (!AudioContextConstructor) {
      throw new Error("Este navegador no ofrece Web Audio para reproducir la recreación.");
    }

    stop();
    const releaseAudioSession = requestPlaybackAudioSession();
    let playback = null;

    try {
      if (!audioContext || audioContext.state === "closed") {
        audioContext = new AudioContextConstructor();
      }
      const resumePromise = audioContext.state !== "running" &&
        typeof audioContext.resume === "function"
        ? audioContext.resume()
        : null;
      const rendered = synthesize(words);
      if (resumePromise) await resumePromise;

      const buffer = audioContext.createBuffer(1, rendered.samples.length, rendered.sampleRate);
      buffer.copyToChannel(rendered.samples, 0);
      const source = audioContext.createBufferSource();
      source.buffer = buffer;
      source.connect(audioContext.destination);

      let resolveEnded;
      let finished = false;
      const ended = new Promise(resolve => {
        resolveEnded = resolve;
      });
      playback = {
        mode: MODE_TECHNICAL,
        source,
        rendered,
        ended,
        finish() {
          if (finished) return;
          finished = true;
          if (activePlayback === playback) activePlayback = null;
          releaseAudioSession();
          resolveEnded(rendered);
        },
        stop() {
          if (activePlayback === playback) stop();
        },
        stopInternal() {
          try {
            source.stop();
          } catch {
            // A source that has already ended cannot be stopped a second time.
          } finally {
            playback.finish();
          }
        }
      };
      source.addEventListener("ended", playback.finish, { once: true });
      activePlayback = playback;
      source.start();
      return playback;
    } catch (error) {
      if (activePlayback === playback) activePlayback = null;
      releaseAudioSession();
      throw error;
    }
  }

  async function playFluid(words) {
    if (!isModeSupported(MODE_FLUID)) {
      throw new Error("Este navegador no ofrece una voz de sistema para la recreación fluida.");
    }

    stop();
    root.speechSynthesis.cancel();
    const releaseAudioSession = requestPlaybackAudioSession();
    const rendered = buildFluidPlan(words);
    const utterance = new root.SpeechSynthesisUtterance(rendered.spokenText);
    utterance.lang = rendered.language;
    utterance.rate = 0.78;
    utterance.pitch = 0.94;
    utterance.volume = 1;
    if (rendered.voice) utterance.voice = rendered.voice;

    let resolveEnded;
    let finished = false;
    const ended = new Promise(resolve => {
      resolveEnded = resolve;
    });
    const playback = {
      mode: MODE_FLUID,
      utterance,
      rendered,
      ended,
      finish() {
        if (finished) return;
        finished = true;
        if (activePlayback === playback) activePlayback = null;
        releaseAudioSession();
        resolveEnded(rendered);
      },
      stop() {
        if (activePlayback === playback) stop();
      },
      stopInternal() {
        try {
          root.speechSynthesis.cancel();
        } finally {
          playback.finish();
        }
      }
    };

    utterance.addEventListener("end", playback.finish, { once: true });
    utterance.addEventListener("error", playback.finish, { once: true });
    activePlayback = playback;
    try {
      root.speechSynthesis.speak(utterance);
      return playback;
    } catch (error) {
      if (activePlayback === playback) activePlayback = null;
      releaseAudioSession();
      throw error;
    }
  }

  async function play(words, options = {}) {
    const requestedMode = options.mode || MODE_FLUID;
    if (requestedMode === MODE_FLUID) {
      if (isModeSupported(MODE_FLUID)) return playFluid(words);
      if (isModeSupported(MODE_TECHNICAL)) return playTechnical(words);
    }
    if (requestedMode === MODE_TECHNICAL) return playTechnical(words);
    throw new Error(`Modo sonoro no disponible: ${requestedMode}.`);
  }

  return Object.freeze({
    VERSION,
    PROFILE_ID,
    TECHNICAL_PROFILE_ID,
    FLUID_PROFILE_ID,
    MODE_FLUID,
    MODE_TECHNICAL,
    SAMPLE_RATE,
    VALID_TOKENS: Object.freeze(Array.from(VALID_TOKENS)),
    buildPlan,
    buildFluidPlan,
    synthesize,
    fingerprint,
    isPlaybackSupported,
    isModeSupported,
    selectFluidVoice,
    play,
    playFluid,
    playTechnical,
    stop
  });
});
