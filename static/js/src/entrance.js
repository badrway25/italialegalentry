/**
 * The entrance «Il varco» — the stage answers the person (docs/design-v5/V5_4_EXECUTION_PLAN.md §1.13 «Le vie
 * convergono al varco»; W2-B). Loaded by templates/allauth/layouts/entrance.html on every entrance page — login,
 * signup, password reset, e-mail verification, MFA — and silent where the page has no such field.
 *
 * WHAT IT DOES. It reads where the person is and what the form holds, and writes the answer as classes on the
 * stage (`[data-varco-stage]`); apps/accounts/static/accounts/entrance.css draws every state and every way to it:
 *
 *     is-ways    the e-mail field has the focus, or holds a valid address      the four ways are lit
 *     is-held    the address is valid (the field's own validity)               the threshold holds the light
 *     is-frame   a password (or a one-time code) has the focus, or is typed    the light stands on the frame
 *
 * A state is a function of the form, never a memory: clearing the address or leaving the form gives back the
 * state that matches what is left. While an address is being typed its validity is read at the person's pause
 * (--motion-wait, a threshold): «a@b» is valid and «a@b.» is not, and a light that followed every keystroke would
 * flicker. Below 64rem the stage is a band with the door alone, and the frame answers for all three (the sheet
 * says so with --varco-band; no breakpoint is written here).
 *
 * THE WAY TO A STATE. A state asked by a pointer's focus arrives with ONE PASS of light (`is-passing-ways`,
 * `is-passing-frame`: the sheet's keyframes, on the duration tokens); every other change is the sheet's opacity
 * transition; from the keyboard the sheet zeroes it (html[data-input="key"], tier 0) and no pass is asked; under
 * reduced motion the tokens are 0 ms and no pass is asked. A page that loads with something to show — the address
 * kept after a refused sign-in — shows it as a still (`is-still`), with no way to it.
 *
 * THE ARRIVAL, once. When the person arrives at the entrance from outside it, on a page at rest with no field
 * focused, the four lights travel into the threshold one after the other (`is-arriving`), after the door has been
 * painted; any focus, input or submit cuts it to the rest. Never on a refused sign-in's page, never on a page
 * reached from another entrance page (the person is already at the threshold), never from history, never on the
 * band, never under reduced motion.
 *
 * WHAT IT DOES NOT DO. The key's turn on the sign-in's submit is the loader's engage: the form names the stage in
 * data-loader-host and static/js/src/shell.js hands it to static/js/src/loader.js. Nothing here animates: no
 * element.animate(), no frame loop, no style written — classes only (CSP: style-src 'self'); the one question about
 * motion goes through motion.js's gate, and the one wait on motion through its settled(), which has a timeout.
 */
import { afterPaint, durationToken, reducedMotion, settled } from "./motion.js";

const STATES = ["ways", "held", "frame"];
const REST = { ways: false, held: false, frame: false };

const found = document.querySelector("[data-varco-stage]");
if (found) entrance(found);

function entrance(stage) {
  const page = stage.closest(".varco") || document;
  const sheet = page.querySelector(".varco__sheet") || page;
  // the references are kept: the show / hide control turns a password field into a text field and back
  const email = sheet.querySelector('input[type="email"]');
  const secrets = [...sheet.querySelectorAll('input[type="password"], input[autocomplete="one-time-code"]')];
  const fields = [email, ...secrets].filter(Boolean);
  let shown = REST;
  const passes = { ways: 0, frame: 0 }; // per light: a pass that ends after a newer one of its kind leaves the class alone
  let pause = 0; // the timer of a typing pause in the e-mail field
  let arrival = "waiting"; // waiting → playing → over

  const band = () => getComputedStyle(stage).getPropertyValue("--varco-band").trim() === "1";
  const valid = (input) => input.value.trim() !== "" && input.validity.valid;
  const any = (state) => STATES.some((name) => state[name]);
  /** A password's show / hide control is the password's own: the focus on it is the focus on the field. */
  const serves = (active, input) =>
    active === input ||
    (active instanceof Element && active.hasAttribute("data-password-toggle") && active.getAttribute("aria-controls") === input.id);
  /** Does the focus on this element ask for a state by itself — a field, or a password's own control? */
  const asks = (element) => element === email || secrets.some((input) => serves(element, input));

  /** The state that matches the form, with `active` as the focused element. */
  function read(active) {
    const held = Boolean(email) && valid(email);
    const ways = Boolean(email) && (active === email || held);
    const frame = secrets.some((input) => serves(active, input) || input.value !== "");
    return band() ? { ways: false, held: false, frame: ways || frame } : { ways, held, frame };
  }

  /** A class is written only when it changes: a keystroke that changes nothing touches nothing. */
  function mark(cls, on) {
    if (stage.classList.contains(cls) !== on) stage.classList.toggle(cls, on);
  }

  /** The arrival ends as soon as the person acts — and never starts after that. */
  function cut() {
    arrival = "over";
    mark("is-arriving", false);
  }

  /** One pass of light toward a state a pointer's focus has just asked for; the class leaves with the motion. */
  function pass(name) {
    const mine = (passes[name] += 1);
    const cls = `is-passing-${name}`;
    mark(cls, true);
    const longest = durationToken("--motion-slow", 0) + durationToken("--motion-fast", 0);
    settled(stage, { subtree: true, timeout: longest + 200 }).then(() => {
      if (mine === passes[name]) mark(cls, false);
    });
  }

  /** Write the state. `focused` is the field the person has just focused, when that is what asked for it. */
  function show(next, focused = null) {
    const travel = focused !== null && !reducedMotion() && document.documentElement.dataset.input === "pointer";
    for (const name of STATES) {
      mark(`is-${name}`, next[name]);
      if (!next[name]) mark(`is-passing-${name}`, false);
    }
    if (travel && next.ways && !shown.ways && focused === email) pass("ways");
    if (travel && next.frame && !shown.frame) pass("frame");
    shown = next;
  }

  /** A state shown without a way to it: the page loaded with it. */
  function still(state) {
    mark("is-still", true);
    show(state);
    afterPaint().then(() => mark("is-still", false));
  }

  if (fields.length) {
    // focusin and focusout name the element that takes the focus, so a move between two fields is one state — and
    // the state an element asks for is written when it takes the focus, with its pass, not when the other loses it
    document.addEventListener("focusin", (event) => {
      cut();
      show(read(event.target), asks(event.target) ? event.target : null);
    });
    document.addEventListener("focusout", (event) => {
      clearTimeout(pause);
      if (!asks(event.relatedTarget)) show(read(event.relatedTarget));
    });
    for (const field of fields) {
      field.addEventListener("input", () => {
        cut();
        clearTimeout(pause);
        // a cleared address, or a password, answers at once; an address being typed, at the person's pause
        if (field !== email || email.value === "") show(read(document.activeElement));
        else pause = setTimeout(() => show(read(document.activeElement)), durationToken("--motion-wait", 400));
      });
      field.addEventListener("change", () => {
        cut();
        clearTimeout(pause);
        show(read(document.activeElement));
      });
    }
    window.addEventListener("resize", () => show(read(document.activeElement)), { passive: true });
  } else {
    document.addEventListener("focusin", cut);
  }
  page.addEventListener("submit", cut);
  // a page restored from history comes back with its fields filled: their state as a still, no way to it
  window.addEventListener("pageshow", (event) => {
    if (event.persisted) still(read(document.activeElement));
  });

  const first = read(document.activeElement);
  if (any(first)) still(first);

  /** Does the person come from another entrance page — «/<language>/<the same first segment>/…» of this site? */
  function fromInside() {
    try {
      const from = new URL(document.referrer);
      const family = (path) => path.split("/").filter(Boolean)[1] || "";
      return from.origin === location.origin && family(from.pathname) !== "" && family(from.pathname) === family(location.pathname);
    } catch {
      return false; // no referrer: the person arrives from outside
    }
  }

  function fromHistory() {
    const [navigation] = performance.getEntriesByType("navigation");
    return Boolean(navigation) && navigation.type === "back_forward";
  }

  /** Resolves once the door has been painted: its photograph decoded and a largest-contentful-paint entry
   *  reported — the arrival never starts before the page's largest paint. Where the browser reports no such
   *  entry, the page's load stands for it. */
  function doorPainted() {
    const photo = stage.querySelector(".door-stage__photo img");
    const decoded = photo && typeof photo.decode === "function" ? photo.decode().catch(() => {}) : Promise.resolve();
    const types = typeof PerformanceObserver === "function" ? PerformanceObserver.supportedEntryTypes || [] : [];
    const painted = types.includes("largest-contentful-paint")
      ? new Promise((resolve) => {
          const observer = new PerformanceObserver((list) => {
            if (!list.getEntries().length) return;
            observer.disconnect();
            resolve();
          });
          observer.observe({ type: "largest-contentful-paint", buffered: true });
        })
      : new Promise((resolve) => {
          if (document.readyState === "complete") resolve();
          else window.addEventListener("load", () => resolve(), { once: true });
        });
    return Promise.all([decoded, painted]);
  }

  function arrive() {
    if (arrival !== "waiting" || document.visibilityState !== "visible") return;
    if (reducedMotion() || band() || fields.includes(document.activeElement)) {
      arrival = "over";
      return;
    }
    arrival = "playing";
    mark("is-arriving", true);
    const whole = durationToken("--motion-route-light", 0) + 3 * durationToken("--motion-route-stagger", 0);
    settled(stage, { subtree: true, timeout: whole + 200 }).then(() => {
      if (arrival === "playing") cut();
    });
  }

  if (any(first) || document.getElementById("form-errors") || fromInside() || fromHistory()) {
    arrival = "over";
  } else {
    doorPainted()
      .then(afterPaint)
      .then(() => {
        if (document.visibilityState === "visible") arrive();
        else document.addEventListener("visibilitychange", arrive, { once: true });
      });
  }
}
