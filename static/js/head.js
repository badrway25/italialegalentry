/* Executed synchronously in <head>. External file (not inline) because the CSP is script-src 'self'
   without nonces; a classic script, no module, nothing to import.

   1. JavaScript is available: html.no-js becomes html.js (progressive enhancement).
   2. The input modality (V5.4 plan §1.5, R-07 «the keyboard never animates»): html[data-input] says what
      the last input was — "key" after a navigation key (Tab, the arrows, Home, End, Page Up / Down,
      Enter, Space, Escape, the context-menu keys, Ctrl / Cmd K), "pointer" after a press or a mouse
      movement; absent until the first. A change asked from the keyboard is tier 0, there in the next
      frame: each family writes its one rule, html[data-input="key"] <its selector> { transition-duration: 0ms; }.
      Typing text changes nothing. The attribute is written only when the modality changes. */
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
