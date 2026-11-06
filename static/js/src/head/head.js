/* Executed synchronously in <head>. External file (not inline) because the CSP is script-src 'self'
   without nonces; a classic script, no module, nothing to import.
   THIS IS THE SOURCE: base.html loads static/js/head.js, its minified build (`npm run build:js`,
   scripts/build_frontend.mjs — review v512-a-fix-w1: the render-blocking script stays under 1 KB gzip).

   1. JavaScript is available: html.no-js becomes html.js (progressive enhancement).
   2. The input modality (V5.4 plan §1.5, R-07 «the keyboard never animates»): html[data-input] says what
      the last input was — "key" after a navigation key (Tab, the arrows, Home, End, Page Up / Down,
      Enter, Space, Escape, the context-menu keys, Ctrl / Cmd K), "pointer" after a press or a mouse
      movement; absent until the first. A change asked from the keyboard is tier 0, there in the next
      frame: each family writes its one rule, html[data-input="key"] <its selector> { transition-duration: 0ms; }.
      Typing text changes nothing. The attribute is written only when the modality changes.
   3. The loader «Lume» across a navigation (V5.12 §4; the Director's DECISIONS §1 T1, T2) — here because only a
      blocking script of <head> hears the new page's `pagereveal`, which comes before its first frame:
      · the cross-document View Transition (static/css/v5/motion.css: the root cross-fades, the mark travels) is
        SKIPPED from the keyboard (html[data-input="key"]: tier 0), on the preview hub's chrome and under the
        preview's flag html.rm; the setting itself turns it off in the sheet;
      · a language switch (/fr/… → /ar/…) cross-fades the page only: the mark never travels, so it never mirrors
        (DL54-08) — html.vt-lang takes its name away on both pages, the leaving one in `pageswap`, the arriving
        one in `pagereveal`, until the transition is over;
      · V5.15 — «LUME», THE CENTRAL VEIL (§8–§14; DECISIONS §15 lane A): a page left by a pointer's navigation
        (html.lume-go, static/js/src/lume/threshold.js) hands on «go» and the click's time through sessionStorage;
        this page reads it once, within 15 s, and sets html.lume-in and --lume-t BEFORE its first paint, so the veil
        it draws (components/lume_veil.html, static/css/v5/lume.css) continues the clock the reader SAW: the leaving
        page hands on the time of the LAST FRAME IT PAINTED (threshold.js counts them; `pagehide` passes it on — the
        time to pagehide is not what was shown), and the arrival starts there. threshold.js hands it on as a phase:
        at most 150 ms before a wait (≥ 250 ms of the key's turn play on the arriving page's visible frames; the
        leaving key only crawls past 150 ms — v515-a review round 2, M-1), 480 ms once a wait has begun (the leaving
        page completed the turn: the arrival continues from the turned key and the lit room, never a second turn —
        finishing round F1, M-1); 480 is the clamp here. Under the veil the View Transition is a 140 ms dissolve of the root alone (html.lume-in,
        static/css/v5/motion.css): the held old frame dissolves into the veiled new page; the mark never travels
        then. A console page left for a console page hands on «pane»: the arrival draws the platform's lighter veil
        over the work pane, the rail kept lit (html.lume-pane). The first page of a session plays the resolve alone
        (html.lume-first from 460 ms: ≤ 240 ms; its head is never held — the LCP).
        W1's «slow» hand-off and the mark's arrival light left with the band's line. Storage refused: no veil
        arrives, none is handed on, nothing breaks. */
(function () {
  var root = document.documentElement;
  root.classList.replace("no-js", "js");
  var KEYS = {
    Tab: 1, ArrowUp: 1, ArrowDown: 1, ArrowLeft: 1, ArrowRight: 1, Home: 1, End: 1, PageUp: 1, PageDown: 1,
    Enter: 1, " ": 1, Escape: 1, ContextMenu: 1, F10: 1
  };
  function set(kind) {
    if (root.getAttribute("data-input") !== kind) root.setAttribute("data-input", kind);
  }
  window.addEventListener("keydown", function (event) {
    var shortcut = (event.ctrlKey || event.metaKey) && (event.key === "k" || event.key === "K");
    if (KEYS[event.key] === 1 || shortcut) set("key");
  }, true);
  window.addEventListener("pointerdown", function () { set("pointer"); }, true);
  window.addEventListener("pointermove", function (event) {
    if (event.pointerType === "mouse") set("pointer");
  }, { capture: true, passive: true });
})();
(function () {
  var root = document.documentElement;
  var KEY = "ile.lume";
  var langOf = function (url) { var m = /^\/(fr|it|en|ar)(\/|$)/.exec(url.pathname); return m ? m[1] : ""; };
  var hub = function () { return Boolean(document.body && document.body.classList.contains("dp-page")); };
  var handed = "";
  try {
    // a journey seen before in this session (V5.12 §5; DECISIONS §2 M5): the journey's light — the public passage's
    // («la linea») and the console's («Mon parcours») — advances on its FIRST view in a session only. The key holds two
    // fixed surface tokens at most, «passage» and «journey», never a path (a path can carry a case file's reference;
    // the published technical-storage information says the values hold no identifier). html.is-seen-passage /
    // html.is-seen-journey, set before the first paint, say that surface was shown before; the sheets then draw it as
    // its own still (v5/_reveal.css, portal/v5/_journey-rail.css). A surface's token is written once the page that
    // carries it is parsed. Storage refused: the light plays each time.
    var SURFACES = { passage: ".linea__step--current, .linea__step--done", journey: ".journey:not(.journey--descriptive)" };
    var seen = (sessionStorage.getItem("ile.seen") || "").split(" ").filter(function (token) { return SURFACES.hasOwnProperty(token); });
    seen.forEach(function (token) { root.classList.add("is-seen-" + token); });
    document.addEventListener("DOMContentLoaded", function () {
      var shown = Object.keys(SURFACES).filter(function (token) { return seen.indexOf(token) >= 0 || document.querySelector(SURFACES[token]); });
      try { sessionStorage.setItem("ile.seen", shown.join(" ")); } catch (error) { /* the light plays each time */ }
    });
    handed = sessionStorage.getItem(KEY) || "";
    if (handed) sessionStorage.removeItem(KEY);
  } catch (error) { handed = ""; }
  var parts = handed.split("|");
  var age = Date.now() - Number(parts[1]);
  if (/\bgo\b/.test(parts[0]) && age < 15000) {
    root.classList.add("lume-in");
    if (parts[3] === "pane") root.classList.add("lume-pane");
    root.style.setProperty("--lume-t", Math.min(480, age, parts[2] | 0) + "ms");
  } else if (/\blang\b/.test(parts[0]) && age < 5000) root.classList.add("vt-lang");
  try {
    if (!handed && !sessionStorage.getItem("ile.lume1")) root.classList.add("lume-first"); // from 460 ms: lume.css
    sessionStorage.setItem("ile.lume1", "1");
  } catch (error) { /* no first veil without storage: it would play on every page */ }
  var done = function () { root.classList.remove("vt-lang"); };
  window.addEventListener("pagereveal", function (event) {
    var transition = event.viewTransition;
    if (!transition) { done(); return; }
    if (root.classList.contains("rm") || hub()) transition.skipTransition();
    transition.finished.then(done, done);
  });
  window.addEventListener("pageswap", function (event) {
    var transition = event.viewTransition;
    if (!transition) return;
    if (root.getAttribute("data-input") === "key" || root.classList.contains("rm") || hub()) {
      transition.skipTransition();
      return;
    }
    var entry = event.activation && event.activation.entry;
    if (entry && entry.url && langOf(new URL(entry.url)) !== langOf(location)) root.classList.add("vt-lang");
  });
  window.addEventListener("pagehide", function () {
    var mark = root.classList.contains("lume-go") ? "go" : root.classList.contains("vt-lang") ? "lang" : "";
    if (!mark) return;
    var at = (mark === "go" && Number(root.getAttribute("data-lume-at"))) || Date.now();
    var shown = root.getAttribute("data-lume-painted");
    // a console page left for a console page: html.lume-pane, set by threshold.js's go() on a console page
    var pane = mark === "go" && root.classList.contains("lume-pane") ? "|pane" : "";
    try { sessionStorage.setItem(KEY, mark + "|" + at + "|" + (shown === null ? Date.now() - at : shown) + pane); } catch (error) { /* nothing handed on */ }
  });
  window.addEventListener("pageshow", function (event) {
    if (event.persisted) root.classList.remove("vt-lang", "lume-in", "lume-first", "lume-go", "lume-pane", "is-departing");
  });
})();
