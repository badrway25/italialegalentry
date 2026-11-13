/**
 * The rail's state, written BEFORE the first frame.
 *
 * A classic, blocking script — its own file, because the CSP allows no inline script — loaded at
 * the top of the console's body (templates/portal/base_portal.html), before the rail is parsed. It
 * writes `data-rail` on <body>: the person's stored choice (`ile.rail`: "open" or "closed"), else
 * open from 80rem and compact below. console.js reads the same state once it runs; decided only
 * there, after the first frame, the workspace moved by 184 px (CLS up to 1.19, measured by the
 * gate C review). Without this script the stylesheet keeps the rail open (v5/_shell.css §1).
 * No imports, no exports: this file must stay a script.
 */
(function () {
  var state = null;
  try {
    state = window.localStorage.getItem("ile.rail");
  } catch (error) {
    /* storage refused: the width decides */
  }
  if (state !== "open" && state !== "closed") {
    state = window.matchMedia("(min-width: 80rem)").matches ? "open" : "closed";
  }
  document.body.setAttribute("data-rail", state);
})();
