/**
 * The rail's stored preference, applied BEFORE the first frame.
 *
 * A classic, blocking script — its own file, because the CSP allows no inline script — loaded at
 * the top of the console's body (templates/portal/base_portal.html), before the rail is parsed.
 * console.js applies the same preference again once it runs; applied only there, after the first
 * frame, the workspace moved by 184 px for a person who had opened the rail below 90rem (CLS up
 * to 1.19, measured by the gate C review). No imports, no exports: this file must stay a script.
 */
(function () {
  try {
    var state = window.localStorage.getItem("ile.rail");
    if (state === "open" || state === "closed") document.body.setAttribute("data-rail", state);
  } catch (error) {
    /* storage refused: the stylesheet's default for the width stands */
  }
})();
