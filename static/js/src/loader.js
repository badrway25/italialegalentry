/**
 * The loader «Lume» — one state machine for three tiers (V5.4 plan §1.9; DL54-07, DL54-08, DL54-09; W1-D).
 *
 *   rest ── engage(host) ──▶ engaged   the key turns once and HOLDS (L1, the login's stage on submit)
 *        ── release(host) ─▶ open      the lit doorway, the key in ink, back to rest (an in-page host)
 *        ── rest(control) ─▶ rest      every class and ARIA state removed
 *
 * Nothing loops. A long wait is a still picture and the words carry it: the host's word at 1 s, its sentence
 * at 10 s with the «Réessayer» control that lets the person submit again. L1 is a singleton: one host engaged
 * at a time, and never on an OUTCOME_BEARING action (the situation's recalculation, the pre-assessment, an
 * eligibility, a scan's verification: a lit doorway near a legal answer would promise one — RTD-M6, DL54-09),
 * which keep L2 and L3.
 *
 * What this module does NOT draw. Every beat is a CSS animation on transform / opacity (v5/loader.css, and
 * the console's generated _loader-light.css): here only classes and ARIA change, timers schedule the state
 * changes, and the one wait on motion goes through motion.js's settled(), which has a timeout. The console's
 * ENTRANCE RELEASE never passes here either: the page that follows a successful sign-in is served with
 * `[data-lume="release"]` on the rail's mark (accounts.signals → templates/partials/portal_chrome.html) and the
 * animation starts at the first paint, with or without script, once per session.
 *
 * How it is reached. shell.js sets the busy face of a submitted form's control in the submit's own task — the
 * class is what draws the key, so the face is in the click's frame — and imports this module on that first
 * submit, never before (plan §2.3: the loader loads through shell.js). `submitted()` then takes the rest: the
 * ARIA state, and the engage of the host the form names in `data-loader-host` (W2-B's login: the stage's
 * mark), with `data-loader-action` against the list above. L3 — `seat()` — is for the containers whose content
 * arrives asynchronously; no server-rendered region ever seats (DS 2026 §12).
 *
 * NO WAIT IS FOR EVER (the review-once of V5.5, 9 October 2026). The busy face is for an answer that replaces
 * the page, and a page that is replaced takes its state with it. When the page stays, something ends the wait:
 *   · what is known beforehand never waits — a form `data-loader="none"` (its answer is a file), a form that
 *     opens elsewhere or closes a dialog, a control that is not a `.btn`: shell.js's part;
 *   · the submit was answered in the page — a listener that runs after shell.js's hook cancelled it (a
 *     validation, a confirmation): at rest in the next task. A script that answers in the page ITSELF cancels
 *     the submit on the form, before the hook, and calls `busy()` and `settle()`;
 *   · the page came back from the back/forward cache (`pageshow`): at rest;
 *   · the answer was not a page, or nothing came — a download nobody declared, a 204, a navigation the person
 *     stopped, a link that died. No event tells a script any of these, so the wait is a LEASE of SLOW_AFTER,
 *     the moment «Réessayer» is offered: where a host offers it the person decides, and anywhere else the form
 *     comes back to rest by itself and can be submitted again. A form that carries files is given, on top, the
 *     time they need at UPLOAD_FLOOR: a slow upload keeps its key.
 * A busy control is known by its ARIA state, not by its face: `aria-busy` is on every control that waits and
 * never outlives the wait; the class `is-busy` — the key — only where the key has a place (shell.js: a
 * link-styled or icon-only button has no padding to hold it). `aria-disabled` is set only where the second
 * submit is really refused — main.js's guard on `form[data-single-submit]`; elsewhere it would announce a
 * refusal that does not exist.
 */
import { durationToken, settled } from "./motion.js";

/** A busy face that has shown stays at least this long, so a quick answer never flickers (gate 0's floor). */
export const MIN_SHOWN = 480;
/** The word of a long wait. */
export const WORD_AFTER = 1000;
/** The sentence of a very long wait, and «Réessayer» — and the lease of a busy face that no page replaces. */
export const SLOW_AFTER = 10000;
/** Bytes per second (128 kbit/s, under an EDGE uplink): the time a form's files are given on top of the lease. */
export const UPLOAD_FLOOR = 16 * 1024;
/** The actions on which L1 never plays (plan §1.9 item 2): they keep L2 and L3. */
export const OUTCOME_BEARING = new Set(["recalculate-situation", "pre-assessment", "eligibility", "scan-verification"]);

const shownAt = new WeakMap(); // control → performance.now() when its busy face appeared
const timers = new WeakMap(); // host → { word, slow }
const forms = new WeakMap(); // host → the form whose submit engaged it
const leases = new Map(); // form → the timer that ends its wait when no page comes
const retries = new WeakSet(); // the «Réessayer» controls already listened to: one listener each, for good
let engaged = null; // L1 is a singleton

const wait = (ms) => new Promise((resolve) => setTimeout(resolve, Math.max(0, ms)));
const waits = (control) => control.getAttribute("aria-busy") === "true"; // the state; the class is only its face
const statusOf = (host) => (host.parentElement ? host.parentElement.querySelector("[data-loader-status]") : null);
const retryOf = (host) => (host.parentElement ? host.parentElement.querySelector("[data-loader-retry]") : null);

/* ---- L2 — the busy key ------------------------------------------------------------------------------------ */

/** The control is busy: the key (v5/loader.css) turns once and holds; `aria-busy` says why nothing happens.
 *  `aria-disabled` — never `disabled`, so the focus stays where the person left it — only where the second
 *  submit is really refused (`refuses`: main.js's guard on form[data-single-submit]). `face: false` for a
 *  control that cannot hold the key (a link-styled button): it waits, and keeps its own face. */
export function busy(control, { refuses = false, face = true } = {}) {
  if (!control) return null;
  if (face) control.classList.add("is-busy");
  control.setAttribute("aria-busy", "true");
  if (refuses) control.setAttribute("aria-disabled", "true");
  if (!shownAt.has(control)) shownAt.set(control, performance.now());
  return control;
}

/** The answer came, in the page: the key lights (dim → lit), then the control is at rest. Never shorter than
 *  MIN_SHOWN once the face has shown. */
export async function settle(control, { lit = true } = {}) {
  if (!control) return;
  const since = performance.now() - (shownAt.get(control) ?? performance.now());
  if (since < MIN_SHOWN) await wait(MIN_SHOWN - since);
  if (lit) {
    control.classList.add("is-lit");
    await settled(control, { subtree: true, timeout: durationToken("--motion-fast", 0) + 50 });
  }
  rest(control);
}

/** Back to rest: nothing busy, nothing lit, nothing disabled. */
export function rest(control) {
  if (!control) return;
  control.classList.remove("is-busy", "is-lit");
  control.removeAttribute("aria-busy");
  control.removeAttribute("aria-disabled");
  shownAt.delete(control);
}

/* ---- L1 — the engage, the words, the release of an in-page host ---------------------------------------------- */

/** The wait begins on an L1 host (templates/components/loader.html): the key turns once and holds. Refused —
 *  false — when a host is already engaged (a singleton) or the action is outcome-bearing: the form's control keeps
 *  its L2 key, which is the right loader there. */
export function engage(host, { action = "", form = null } = {}) {
  if (!host || engaged || OUTCOME_BEARING.has(action)) return false;
  engaged = host;
  if (form) forms.set(host, form);
  host.classList.remove("is-open", "is-worded", "is-slow");
  host.classList.add("is-engaged");
  clearTimers(host);
  timers.set(host, {
    word: setTimeout(() => word(host), WORD_AFTER),
    slow: setTimeout(() => slow(host), SLOW_AFTER),
  });
  return true;
}

/** One second: the word shows and is announced (the status line is `role="status"`). */
export function word(host) {
  if (engaged !== host) return;
  host.classList.add("is-worded");
  say(host, "loaderWord");
}

/** Ten seconds: the sentence, and «Réessayer» — pressing it puts the form and its host at rest, so the person
 *  can submit again. */
export function slow(host) {
  if (engaged !== host) return;
  host.classList.add("is-slow");
  say(host, "loaderSlow");
  const retry = retryOf(host);
  if (!retry) return;
  retry.hidden = false;
  if (retries.has(retry)) return;
  retries.add(retry);
  retry.addEventListener("click", () => retryFrom(host));
}

/** The answer is here (an in-page host): the release plays, then the host is at rest. */
export async function release(host) {
  if (!host) return;
  clearTimers(host);
  host.classList.add("is-open");
  await settled(host, { subtree: true, timeout: durationToken("--motion-door", 0) + 100 });
  quiet(host);
}

function retryFrom(host) {
  const form = forms.get(host);
  if (form) {
    // «Réessayer» is about to hide while it holds the focus: the focus goes first to the control the person is
    // invited to press again — the one that was busy — never to <body>.
    const controls = [...form.elements];
    const submit = controls.find(waits) || controls.find((control) => control.type === "submit");
    if (submit) submit.focus();
    over(form);
  }
  quiet(host);
}

function quiet(host) {
  clearTimers(host);
  host.classList.remove("is-engaged", "is-open", "is-worded", "is-slow");
  const status = statusOf(host);
  if (status) status.textContent = "";
  const retry = retryOf(host);
  if (retry) retry.hidden = true;
  if (engaged === host) engaged = null;
}

/* ---- the wait that no page ends ----------------------------------------------------------------------------- */

/** The form can be submitted again: its busy controls are at rest and main.js's double-submit guard is lifted
 *  (the mark on the form, and the `aria-disabled` it put on every submit button of a guarded form). */
function free(form) {
  const guarded = form.hasAttribute("data-single-submit");
  form.removeAttribute("data-submitted");
  for (const control of form.elements) {
    if (waits(control)) rest(control);
    else if (guarded && control.type === "submit") control.removeAttribute("aria-disabled");
  }
}

/** The wait of this form is over and no page came: its lease ends, its host is quiet, it is free again. */
function over(form) {
  clearTimeout(leases.get(form));
  leases.delete(form);
  if (engaged && forms.get(engaged) === form) quiet(engaged);
  free(form);
}

/** A wait is a lease, not a state: SLOW_AFTER, plus the time the form's files need at UPLOAD_FLOOR. At its end
 *  the form is free again — unless its host is offering «Réessayer», which leaves the choice to the person: the
 *  lease then stays on the books until the retry, the answer or a return from the cache ends the wait. */
function lease(form) {
  clearTimeout(leases.get(form));
  let bytes = 0;
  for (const input of form.querySelectorAll('input[type="file"]')) for (const file of input.files) bytes += file.size;
  const expire = () => {
    if (engaged && forms.get(engaged) === form && retryOf(engaged)) return;
    over(form);
  };
  leases.set(form, setTimeout(expire, SLOW_AFTER + (bytes / UPLOAD_FLOOR) * 1000));
}

function clearTimers(host) {
  const pending = timers.get(host);
  if (!pending) return;
  clearTimeout(pending.word);
  clearTimeout(pending.slow);
  timers.delete(host);
}

function say(host, key) {
  const status = statusOf(host);
  if (status && status.dataset[key]) status.textContent = status.dataset[key];
}

/* ---- L3 — the seat ------------------------------------------------------------------------------------------ */

/** A fragment container's content has just arrived: on its FIRST arrival its rows rise 4 px, one after the
 *  other (v5/loader.css); a refresh swaps in place. Resolves once the rows have settled. */
export async function seat(container) {
  if (!container || container.hasAttribute("data-seated")) return;
  container.setAttribute("data-seated", "");
  container.classList.add("is-seating");
  const longest = durationToken("--motion-standard", 0) + 7 * durationToken("--motion-stagger", 0);
  await settled(container, { subtree: true, timeout: longest + 100 });
  container.classList.remove("is-seating");
}

/* ---- the hooks ---------------------------------------------------------------------------------------------- */

/** shell.js, on a form's submit (it has already set `aria-busy`, and the class where the key has a place): the
 *  rest of the ARIA state, the engage of the host the form names, and the lease of the wait. `event` is the submit
 *  itself: a listener that runs after shell.js's may still cancel it — the answer is then given in the page — so
 *  it is read once its dispatch is over. */
export function submitted(form, control, event) {
  if (control) {
    busy(control, { refuses: form.hasAttribute("data-single-submit"), face: control.classList.contains("is-busy") });
  }
  const host = form.dataset.loaderHost ? document.getElementById(form.dataset.loaderHost) : null;
  if (host) engage(host, { action: form.dataset.loaderAction || "", form });
  lease(form);
  if (event) {
    setTimeout(() => {
      if (event.defaultPrevented) over(form);
    }, 0);
  }
}

// A page restored from the back/forward cache comes back as it was left: waiting. It is at rest.
window.addEventListener("pageshow", (event) => {
  if (!event.persisted) return;
  [...leases.keys()].forEach(over);
  if (engaged) quiet(engaged);
});
