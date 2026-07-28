(() => {
  "use strict";

  const MAX_CHARACTERS = 48;
  const MAX_WORDS = 6;

  const SIGN_PATHS = Object.freeze({
    a: "assets/signs/northeastern-dual/dual-01-a.svg",
    e: "assets/signs/northeastern-dual/dual-02-e.svg",
    i: "assets/signs/northeastern-dual/dual-03-i.svg",
    o: "assets/signs/northeastern-dual/dual-04-o.svg",
    u: "assets/signs/northeastern-dual/dual-05-u.svg",
    ga: "assets/signs/northeastern-dual/dual-06-ga.svg",
    ge: "assets/signs/northeastern-dual/dual-07-ge.svg",
    gi: "assets/signs/northeastern-dual/dual-08-gi.svg",
    go: "assets/signs/northeastern-dual/dual-09-go.svg",
    gu: "assets/signs/northeastern-dual/dual-10-gu.svg",
    ka: "assets/signs/northeastern-dual/dual-11-ka.svg",
    ke: "assets/signs/northeastern-dual/dual-12-ke.svg",
    ki: "assets/signs/northeastern-dual/dual-13-ki.svg",
    ko: "assets/signs/northeastern-dual/dual-14-ko.svg",
    ku: "assets/signs/northeastern-dual/dual-15-ku.svg",
    ba: "assets/signs/northeastern-dual/dual-16-ba.svg",
    be: "assets/signs/northeastern-dual/dual-17-be.svg",
    bi: "assets/signs/northeastern-dual/dual-18-bi.svg",
    bo: "assets/signs/northeastern-dual/dual-19-bo.svg",
    bu: "assets/signs/northeastern-dual/dual-20-bu.svg",
    da: "assets/signs/northeastern-dual/dual-21-da.svg",
    de: "assets/signs/northeastern-dual/dual-22-de.svg",
    di: "assets/signs/northeastern-dual/dual-23-di.svg",
    do: "assets/signs/northeastern-dual/dual-24-do.svg",
    du: "assets/signs/northeastern-dual/dual-25-du.svg",
    ta: "assets/signs/northeastern-dual/dual-26-ta.svg",
    te: "assets/signs/northeastern-dual/dual-27-te.svg",
    ti: "assets/signs/northeastern-dual/dual-28-ti.svg",
    to: "assets/signs/northeastern-dual/dual-29-to.svg",
    tu: "assets/signs/northeastern-dual/dual-30-tu.svg",
    s: "assets/signs/northeastern-dual/dual-31-s.svg",
    ś: "assets/signs/northeastern-dual/dual-32-s2.svg",
    r: "assets/signs/northeastern-dual/dual-33-r.svg",
    ŕ: "assets/signs/northeastern-dual/dual-34-r2.svg",
    l: "assets/signs/northeastern-dual/dual-35-l.svg",
    m: "assets/signs/northeastern-dual/dual-36-m.svg",
    n: "assets/signs/northeastern-dual/dual-37-n.svg",
    ḿ: "assets/signs/northeastern-dual/dual-38-m2.svg"
  });

  const VOWELS = new Set(["a", "e", "i", "o", "u"]);
  const STOP_SERIES = Object.freeze({
    b: { a: "ba", e: "be", i: "bi", o: "bo", u: "bu" },
    p: { a: "ba", e: "be", i: "bi", o: "bo", u: "bu" },
    d: { a: "da", e: "de", i: "di", o: "do", u: "du" },
    t: { a: "ta", e: "te", i: "ti", o: "to", u: "tu" },
    g: { a: "ga", e: "ge", i: "gi", o: "go", u: "gu" },
    k: { a: "ka", e: "ke", i: "ki", o: "ko", u: "ku" }
  });

  const ACCENT_MAP = Object.freeze({
    á: "a", à: "a", ä: "a", â: "a",
    é: "e", è: "e", ë: "e", ê: "e",
    í: "i", ì: "i", ï: "i", î: "i",
    ó: "o", ò: "o", ö: "o", ô: "o",
    ú: "u", ù: "u", û: "u"
  });

  function addNotice(notices, code, message, severity = "warning") {
    if (!notices.some(item => item.code === code && item.message === message)) {
      notices.push({ code, message, severity });
    }
  }

  function blocked(original, code, message) {
    return {
      executionStatus: "blocked",
      classification: "experimental_phonetic_adaptation",
      translationClaim: false,
      original,
      normalized: "",
      words: [],
      notices: [{ code, message, severity: "blocking" }],
      operations: [],
      status: "blocked"
    };
  }

  function normalizeInput(rawInput) {
    const original = String(rawInput ?? "").trim();
    if (!original) {
      return { error: blocked(original, "empty_input", "Escribe un nombre, una palabra o una frase breve.") };
    }
    if (Array.from(original).length > MAX_CHARACTERS) {
      return {
        error: blocked(
          original,
          "input_too_long",
          `El demostrador admite un máximo de ${MAX_CHARACTERS} caracteres.`
        )
      };
    }
    if (/\d/u.test(original)) {
      return { error: blocked(original, "digits_not_supported", "Los números todavía no están admitidos en este MVP.") };
    }
    if (/[^A-Za-zÁÉÍÓÚÜÑáéíóúüñÀÈÌÒÙàèìòùÄËÏÖäëïöÂÊÎÔÛâêîôû\s'’\-.,;:!?¿¡()]/u.test(original)) {
      return {
        error: blocked(
          original,
          "unsupported_symbol",
          "La entrada contiene un símbolo que el demostrador todavía no sabe interpretar de forma segura."
        )
      };
    }

    const operations = [];
    let text = original.toLocaleLowerCase("es-ES").normalize("NFC");
    let accentsRemoved = false;
    text = Array.from(text).map(character => {
      if (ACCENT_MAP[character]) {
        accentsRemoved = true;
        return ACCENT_MAP[character];
      }
      return character;
    }).join("");
    if (accentsRemoved) {
      operations.push({ code: "accent_marks_normalized", message: "Se retiraron tildes después de conservar la identidad de las vocales." });
    }

    const beforePunctuation = text;
    text = text.replace(/[.,;:!?¿¡()'’\-]+/gu, " ").replace(/\s+/gu, " ").trim();
    if (text !== beforePunctuation.trim()) {
      operations.push({ code: "punctuation_as_boundary", message: "La puntuación se trató como separación entre palabras." });
    }
    if (!text) {
      return { error: blocked(original, "empty_after_normalization", "La entrada no contiene letras adaptables.") };
    }

    const words = text.split(" ").filter(Boolean);
    if (words.length > MAX_WORDS) {
      return {
        error: blocked(
          original,
          "too_many_words",
          `El demostrador admite un máximo de ${MAX_WORDS} palabras.`
        )
      };
    }
    return { original, normalized: text, words, operations };
  }

  function scanWord(word, notices, operations) {
    const units = [];
    for (let index = 0; index < word.length;) {
      const character = word[index];
      const next = word[index + 1] || "";
      const afterNext = word[index + 2] || "";
      const pair = character + next;

      if (pair === "rr") {
        units.push({ type: "trill", source: "rr" });
        index += 2;
        continue;
      }
      if (pair === "ll") {
        units.push({ type: "palatal", source: "ll" });
        index += 2;
        continue;
      }
      if (pair === "ch") {
        units.push({ type: "affricate", source: "ch" });
        index += 2;
        continue;
      }
      if (character === "q" && next === "u" && /[ei]/u.test(afterNext)) {
        units.push({ type: "k", source: "qu" });
        operations.push({ code: "silent_u_after_q", message: `En «${word}», qu ante e/i se normalizó como /k/.` });
        index += 2;
        continue;
      }
      if (character === "g" && next === "u" && /[ei]/u.test(afterNext)) {
        units.push({ type: "g", source: "gu" });
        operations.push({ code: "silent_u_after_g", message: `En «${word}», la u muda de gu ante e/i no se pronuncia.` });
        index += 2;
        continue;
      }
      if (character === "g" && next === "ü" && /[ei]/u.test(afterNext)) {
        units.push({ type: "g", source: "g" }, { type: "w", source: "ü" });
        addNotice(notices, "diaeresis_to_u_glide", `En «${word}», ü se conserva mediante una aproximación vocálica u.`, "warning");
        index += 2;
        continue;
      }

      if (VOWELS.has(character)) {
        units.push({ type: "vowel", value: character, source: character });
      } else if (character === "ü") {
        units.push({ type: "w", source: character });
        addNotice(notices, "diaeresis_to_u_glide", `En «${word}», ü se conserva mediante una aproximación vocálica u.`, "warning");
      } else if (["b", "p", "d", "t", "k", "m", "n", "l", "s"].includes(character)) {
        units.push({ type: character, source: character });
      } else if (character === "v") {
        units.push({ type: "b", source: character });
        operations.push({ code: "v_to_b_pronunciation", message: `En «${word}», v se interpreta con la pronunciación española /b/.` });
      } else if (character === "c") {
        units.push({ type: /[ei]/u.test(next) ? "theta" : "k", source: character });
      } else if (character === "z") {
        units.push({ type: "theta", source: character });
      } else if (character === "g") {
        units.push({ type: /[ei]/u.test(next) ? "velar_fricative" : "g", source: character });
      } else if (character === "j") {
        units.push({ type: "velar_fricative", source: character });
      } else if (character === "f") {
        units.push({ type: "f", source: character });
      } else if (character === "x") {
        units.push({ type: "k", source: character }, { type: "s", source: character });
        addNotice(notices, "x_to_ks", `En «${word}», x se descompone de forma aproximada en k + s.`, "information");
      } else if (character === "ñ") {
        units.push({ type: "palatal_nasal", source: character });
      } else if (character === "y") {
        if (word.length === 1 || index === word.length - 1) {
          units.push({ type: "vowel", value: "i", source: character });
          operations.push({ code: "word_final_y_to_i", message: `En «${word}», y se interpreta como vocal i.` });
        } else {
          units.push({ type: "palatal", source: character });
        }
      } else if (character === "r") {
        const previous = word[index - 1] || "";
        units.push({ type: index === 0 || /[nls]/u.test(previous) ? "trill" : "tap", source: character });
      } else if (character === "w") {
        units.push({ type: "w", source: character });
      } else if (character === "h") {
        addNotice(notices, "silent_h_removed", `En «${word}», h no genera signo porque es muda en la pronunciación española de referencia.`, "information");
      } else if (character === "q") {
        units.push({ type: "k", source: character });
        addNotice(notices, "isolated_q_to_k", `En «${word}», q fuera de qu se aproxima mediante k.`, "warning");
      } else {
        return { error: `No se ha podido interpretar «${character}» dentro de «${word}».` };
      }
      index += 1;
    }
    return { units };
  }

  function nextVowel(units, startIndex) {
    for (let index = startIndex; index < units.length; index += 1) {
      if (units[index].type === "vowel") return units[index].value;
    }
    return null;
  }

  function appendStop(tokens, units, index, stopType, notices, word, warningCode = null) {
    const immediate = units[index + 1];
    const immediateVowel = immediate?.type === "vowel" ? immediate.value : null;
    const supportVowel = immediateVowel || nextVowel(units, index + 1) || "a";
    const seriesType = stopType === "p" ? "p" : stopType;
    tokens.push(STOP_SERIES[seriesType][supportVowel]);

    if (warningCode === "f_to_labial_stop") {
      addNotice(notices, warningCode, `En «${word}», f no tiene equivalente directo y se aproxima mediante la serie labial b/p.`, "warning");
    } else if (stopType === "p") {
      addNotice(notices, "p_to_shared_labial_series", `En «${word}», p usa la serie labial compartida y pierde el contraste gráfico con b.`, "warning");
    } else if (warningCode === "velar_fricative_to_k") {
      addNotice(notices, warningCode, `En «${word}», j o g suave se aproxima mediante la serie velar k.`, "warning");
    }

    if (immediateVowel) {
      return 1;
    }
    if (nextVowel(units, index + 1)) {
      addNotice(
        notices,
        "cluster_support_vowel",
        `En «${word}», una oclusiva dentro de un grupo consonántico usa ${supportVowel} como vocal de apoyo; la vocal original se conserva después.`,
        "warning"
      );
    } else {
      addNotice(
        notices,
        "final_support_vowel",
        `En «${word}», una oclusiva sin vocal posterior usa a como vocal de apoyo.`,
        "warning"
      );
    }
    return 0;
  }

  function adaptWord(word, units, notices) {
    const tokens = [];
    for (let index = 0; index < units.length; index += 1) {
      const unit = units[index];
      if (unit.type === "vowel") {
        tokens.push(unit.value);
      } else if (["m", "n", "l", "s"].includes(unit.type)) {
        tokens.push(unit.type);
      } else if (unit.type === "tap") {
        tokens.push("r");
      } else if (unit.type === "trill") {
        tokens.push("ŕ");
        addNotice(
          notices,
          "r_series_project_convention",
          "El demostrador usa r para la vibrante simple y ŕ para la múltiple como convención gráfica del proyecto, no como identidad fonética histórica demostrada.",
          "information"
        );
      } else if (["b", "p", "d", "t", "g", "k"].includes(unit.type)) {
        index += appendStop(tokens, units, index, unit.type, notices, word);
      } else if (unit.type === "f") {
        index += appendStop(tokens, units, index, "b", notices, word, "f_to_labial_stop");
      } else if (unit.type === "velar_fricative") {
        index += appendStop(tokens, units, index, "k", notices, word, "velar_fricative_to_k");
      } else if (unit.type === "theta") {
        tokens.push("s");
        addNotice(notices, "theta_to_sibilant", `En «${word}», el sonido de z o c ante e/i se aproxima mediante la sibilante s.`, "warning");
      } else if (unit.type === "palatal") {
        tokens.push("i");
        addNotice(notices, "palatal_to_i", `En «${word}», y o ll consonántica se aproxima mediante i.`, "warning");
      } else if (unit.type === "palatal_nasal") {
        tokens.push("n", "i");
        addNotice(notices, "palatal_nasal_to_ni", `En «${word}», ñ se aproxima mediante la secuencia n + i.`, "warning");
      } else if (unit.type === "affricate") {
        tokens.push("ś");
        addNotice(notices, "ch_to_marked_sibilant", `En «${word}», ch se aproxima mediante la sibilante marcada ś.`, "warning");
      } else if (unit.type === "w") {
        tokens.push("u");
        addNotice(notices, "w_to_u", `En «${word}», la semiconsonante w/ü se aproxima mediante u.`, "warning");
      }
    }
    return tokens;
  }

  function convert(rawInput) {
    const normalized = normalizeInput(rawInput);
    if (normalized.error) return normalized.error;

    const notices = [];
    const operations = [...normalized.operations];
    const adaptedWords = [];

    for (const word of normalized.words) {
      const scanned = scanWord(word, notices, operations);
      if (scanned.error) {
        return blocked(normalized.original, "uninterpretable_letter", scanned.error);
      }
      const tokens = adaptWord(word, scanned.units, notices);
      if (!tokens.length) {
        return blocked(normalized.original, "empty_word_output", `«${word}» no ha producido ningún signo; no se ofrecerá una salida vacía.`);
      }
      if (tokens.some(token => !SIGN_PATHS[token])) {
        return blocked(normalized.original, "missing_graphic_token", `La adaptación de «${word}» requiere un signo gráfico no disponible.`);
      }
      adaptedWords.push({ source: word, tokens });
    }

    const approximate = notices.some(item => item.severity === "warning");
    return {
      executionStatus: "success",
      classification: "experimental_phonetic_adaptation",
      translationClaim: false,
      original: normalized.original,
      normalized: normalized.normalized,
      words: adaptedWords,
      notices,
      operations,
      status: approximate ? "approximate" : "direct",
      pronunciationLabel: normalized.normalized,
      technicalReading: adaptedWords.map(item => item.tokens.join(" · ")).join(" / ")
    };
  }

  window.IberoMvp = Object.freeze({
    MAX_CHARACTERS,
    MAX_WORDS,
    SIGN_PATHS,
    convert
  });
})();
