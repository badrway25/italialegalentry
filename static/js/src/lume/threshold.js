/**
 * «La soglia» — the threshold of a navigation, T2 of the loader «Lume» (V5.12 §4; the Director's DECISIONS §1 T2).
 *
 * A same-origin navigation that has not committed within --motion-wait (400 ms) says so, in the letterhead's band
 * (the console's bar on a console page) and nowhere else:
 *   1. the light line — 2 px under the band's rule, drawn from the inline-start edge (right to left in Arabic) to
 *      85 % over --motion-draw, then HELD: it never loops and never pretends to finish;
 *   2. the mark — the letterhead's lock-up mark, the rail's tile on a console page — plays L1's engage: the key turns
 *      once and holds;
 *   3. the word — at 1 s, «Chargement…» in the band's `role="status"` line, said once.
 * (V5.15: what shows is the central veil — components/lume_veil.html, static/css/v5/lume.css — on html.lume-go and
 * html.is-departing, and its one status line; the band's line and word of W1 are gone.) This module only decides WHEN.
 *
 * WHAT IS A NAVIGATION HERE. A primary click on a same-origin `a[href]` that leaves this document, and a form's
 * submit, that nothing has cancelled once the event's dispatch is over (an overlay's opener, a door of the portico,
 * a script answering in the page all cancel theirs). Never: a new tab or window (`target`, a modifier, the middle
 * button), a download (`download`, or `data-loader="none"` on the link, the form or an ancestor: the answer is a
 * file and no event would end the wait), a same-page anchor (the skip link included), a dialog's form, an OUTCOME_BEARING form (a legal answer keeps the
 * button's busy key only: no lit doorway near it, DL54-09), the preview hub's chrome (`dp-page`), an error page
 * (its door stays still).
 *
 * NO FAKE WAIT, NO FAKE END. Nothing shows before --motion-wait; nothing is held after the page is replaced; there
 * is no minimum display time. What ends a wait that no page ends: the return from the back/forward cache
 * (`pageshow`), the Navigation API's `navigateerror` where it exists (a stopped navigation), and otherwise a LEASE of
 * SLOW_AFTER — the loader's own (static/js/src/loader.js), after which the band is quiet again.
 *
 * V5.15 (DECISIONS §15 lane A) — THE CENTRAL VEIL. A pointer's navigation now begins the brand's transition at once
 * (`go()`: html.lume-go, components/lume_veil.html, static/css/v5/lume.css): the page dims, the doorway comes, the key
 * turns — and the next page, reading the click's time in head.js, continues the same 700 ms clock through the light and
 * the resolve. Nothing waits for it: the click's own navigation is never delayed, the veil takes no pointer and no
 * key, and Esc stops a pending navigation (`window.stop()`) and puts the veil away. The keyboard's navigation gets no
 * veil (tier 0) until its wait passes --motion-wait, which then shows the still. The band's line and word of W1 are
 * gone: the veil's sill and its one status line, under the stage, carry the wait.
 *
 * The threshold is the same picture under reduced motion and from the keyboard — the still: the line at its 85 %,
 * the key turned, the room lit — shown with one 80 ms fade (reduced motion) or at once (the keyboard). This module
 * does not ask the setting: it changes no duration.
 */
import { durationToken, nextFrame, reducedMotion } from "../motion.js";

/** The word of a long wait, counted from the click — the loader's WORD_AFTER. */
export const WORD_AFTER = 1000;
/** The arrival's clock after a wait (lume.css): the turn done, the key back in place, the room lighting, the sill near
 *  its 85 % — where the leaving page's held picture stands (finishing round F1, M-1). head.js clamps to it. */
export const TURNED_AT = 480;
/** The lease of a departure that no page ends — the loader's SLOW_AFTER. */
export const SLOW_AFTER = 10000;
/** The actions on which no lit doorway plays (V5.4 plan §1.9 item 2; DL54-09): they keep L2, the button's key. The
 *  twin of loader.js's list — that module is imported on the first submit only, so this one cannot read it there;
 *  tests/frontend/test_loader_rules.py holds the two lists equal. */
export const OUTCOME_BEARING = new Set(["recalculate-situation", "pre-assessment", "eligibility", "scan-verification"]);

const root = document.documentElement;
let timers = [];

const words = () => document.querySelectorAll("[data-lume-word]");

/** Back to rest: no veil, no turning key, no word. */
export function quiet() {
  timers.forEach(clearTimeout);
  timers = [];
  root.classList.remove("is-departing", "lume-go", "lume-pane");
  words().forEach((line) => {
    line.textContent = "";
  });
}

/** A navigation has started: after --motion-wait without a new page the band says so, at 1 s the word. */
export function depart() {
  quiet();
  const wait = durationToken("--motion-wait", 400);
  timers = [
    setTimeout(() => root.classList.add("is-departing"), wait),
    setTimeout(() => {
      // one line per page (the letterhead's, or the console bar's): the word is said once
      words().forEach((line) => {
        line.textContent = line.dataset.lumeWord || "";
      });
    }, Math.max(WORD_AFTER, wait)),
    setTimeout(quiet, SLOW_AFTER),
  ];
}

/** The veil begins: the page dims, the doorway comes, the key turns (pointer navigations; never from the keyboard).
 *  The click's time is left on <html> for head.js's `pagehide`, which hands it to the next page. */
export function go() {
  root.classList.remove("lume-in", "lume-first");
  const at = Date.now();
  root.dataset.lumeAt = String(at);
  // the platform is a working tool: between two console pages the veil covers the work pane only (lume.css); the
  // class is handed on by head.js's `pagehide` («pane») so the arrival draws the same
  root.classList.toggle("lume-pane", document.body.classList.contains("console"));
  root.classList.add("lume-go");
  // the last frame this page drew of the veil, for head.js's `pagehide` (review round 2, M-1: the time to pagehide is
  // not what the reader saw — a held frame is not a painted one). Through the gate's frame clock; under reduced motion
  // the still is drawn and nothing is counted (the arrival shows the still). It is handed on as a PHASE of the clock
  // (finishing round F1, M-1): before a wait, the time painted, at most 150 ms — the leaving key only crawls past it, so
  // the turn plays on the arrival; once a wait has begun (is-departing) this page completes the turn itself, and the
  // arrival continues from TURNED_AT — the key turned, the room lit — never turning it a second time, never putting the
  // light out (the round-3 review filmed 18° → 360° on the leaving page, then 14° → 360° again on the arrival)
  if (reducedMotion()) return;
  root.dataset.lumePainted = "0";
  const painted = () => {
    if (!root.classList.contains("lume-go")) return;
    const shown = root.classList.contains("is-departing") ? TURNED_AT : Math.min(150, Date.now() - at);
    root.dataset.lumePainted = String(shown);
    nextFrame().then(painted);
  };
  nextFrame().then(painted);
}

/** Is this page one where no threshold ever shows? */
const still = () => document.body.matches(".dp-page, .page-error");

const optedOut = (element) => Boolean(element.closest('[data-loader="none"]'));

/** Does this click leave the document for a page of this site, in this window? */
export function leaves(event) {
  if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return false;
  const link = event.target instanceof Element ? event.target.closest("a[href]") : null;
  if (!link || link.hasAttribute("download") || optedOut(link)) return false;
  if (!["", "_self"].includes(link.getAttribute("target") || "")) return false;
  let url;
  try {
    url = new URL(link.href, location.href);
  } catch {
    return false;
  }
  if (url.origin !== location.origin) return false;
  const here = url.pathname === location.pathname && url.search === location.search;
  return !(here && url.hash); // a same-page anchor moves the reading point, it loads nothing
}

/** Does this submit replace the page, on the threshold's terms? `staysOnPage` is shell.js's own reading.
 *  The sign-in's form (`data-loader-host`, the door's stage) is one of them since V5.18 (§4, P12): login → platform
 *  is the central veil's, like every other page change — its engage is handed to the veil, so the door's key does not
 *  turn a second time beside it (shell.js passes the answer of `after()` on to loader.js's `submitted()`). */
export function submits(form, staysOnPage) {
  if (staysOnPage || optedOut(form)) return false;
  return !OUTCOME_BEARING.has(form.dataset.loaderAction || "");
}

/** Armed once the event's dispatch is over: a listener that cancels it later answers in the page. True when the
 *  threshold takes the navigation (never on a page where no threshold shows). */
export function after(event) {
  if (still()) return false;
  setTimeout(() => {
    if (event.defaultPrevented) return;
    depart(); // first: it begins with `quiet()`, which would put a veil already drawn away
    if (root.dataset.input !== "key") go();
  }, 0);
  return true;
}

let wired = false;

/** shell.js, on every page — base.html loads it under console.js too: the click side here; the submit side is
 *  shell.js's own hook (one listener for a form), which calls `submits()` and `after()`. */
export function initThreshold() {
  if (wired) return;
  wired = true;
  // the veil laid out and its stage rasterised once the page is idle (lume.css, html.lume-warm): the click's first
  // frame then only changes opacities (review round 2, M-1: the stage's first raster was a 95–120 ms long frame)
  // A hidden tab keeps no warm layer (finishing round F1): the veil's two layers leave while the page is not shown and
  // come back when it is (a phone holds no full-viewport layer for a tab in the background)
  let warmed = false;
  const warm = () => {
    warmed = true;
    root.classList.toggle("lume-warm", !document.hidden);
  };
  if ("requestIdleCallback" in window) requestIdleCallback(warm, { timeout: 1500 });
  else setTimeout(warm, 600);
  document.addEventListener("visibilitychange", () => {
    if (warmed) warm();
  });
  document.addEventListener(
    "click",
    (event) => {
      if (leaves(event)) after(event);
    },
    true,
  );
  window.addEventListener("pageshow", (event) => {
    if (event.persisted) quiet();
  });
  // Esc always works: a pending navigation is stopped, and the veil goes with it
  document.addEventListener("keydown", (event) => {
    if (event.key !== "Escape" || !root.matches(".lume-go, .is-departing")) return;
    window.stop();
    quiet();
  });
  // the arrival's classes leave once its clock is over, so the next departure starts clean
  if (root.matches(".lume-in, .lume-first")) setTimeout(() => root.classList.remove("lume-in", "lume-first", "lume-pane"), 900);
  if (window.navigation && typeof window.navigation.addEventListener === "function") {
    window.navigation.addEventListener("navigateerror", quiet);
  }
}
