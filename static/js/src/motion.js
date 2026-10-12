/**
 * Motion — the one gate every moving thing passes through, and the helpers it needs
 * (docs/design-v5/V5_4_EXECUTION_PLAN.md §1.5 «Reduced motion, built as a state», W1-D).
 *
 * THE GATE. `reducedMotion()` is the only place a script asks whether it may move: the person's
 * setting, `prefers-reduced-motion: reduce`, read live (it can change while the page is open), or the
 * preview's flag `html.rm`, whose twin in static/css/v5/tokens.css zeroes the same duration tokens as
 * the media block (tests/frontend/test_rm_flag_parity.py). No other module reads the media query, and
 * no module calls `element.animate()` or `requestAnimationFrame` itself: they call `play()`,
 * `nextFrame()`, `afterPaint()` and `tween()`, which ask the gate first
 * (tests/frontend/test_script_motion_gate.py).
 *
 * THE STATE IS SET AT t = 0. A caller writes the final state first and animates towards it, so under
 * reduced motion nothing has to happen: `play()` creates no animation, `nextFrame()` and `afterPaint()`
 * resolve at once, `tween()` lands on its end. And nothing waits on `transitionend` or `animationend`:
 * a 0 s transition never fires its event, so a script waiting on one would hang exactly under reduced
 * motion. `settled()` waits on the animations really running, and gives up after a timeout.
 *
 * Motion (motion.dev) stays re-exported for the modules that still use it (shell.js, home.js) until
 * their families remove it; the dependency leaves in W4-B (plan §1.5 «Engine»: no new use).
 */
export { animate, scroll, inView, stagger, spring, hover, press } from "motion";
import { spring } from "motion";

const QUERY = "(prefers-reduced-motion: reduce)";
const media = typeof matchMedia === "function" ? matchMedia(QUERY) : null;

/** THE gate: true when the person asked for reduced motion, or the preview's flag html.rm is set. */
export function reducedMotion() {
  return Boolean(media && media.matches) || document.documentElement.classList.contains("rm");
}

/** Calls `callback(reducedMotion())` whenever the setting changes; returns the unsubscribe. */
export function onReducedMotionChange(callback) {
  if (!media) return () => {};
  const handler = () => callback(reducedMotion());
  media.addEventListener("change", handler);
  return () => media.removeEventListener("change", handler);
}

/**
 * Run `fn` only when motion is welcome; otherwise apply `settle` (usually: set the final state).
 * Keeps the reduced-motion branch next to the animation it replaces, where a reviewer can see that the
 * final state is the same in both.
 */
export function withMotion(fn, settle) {
  if (reducedMotion()) {
    if (settle) settle();
    return null;
  }
  return fn();
}

/**
 * The Web Animations API through the gate: `element.animate(keyframes, options)`, or null under reduced
 * motion — the caller has already written the final state, so there is nothing to play. Durations come
 * from `durationToken()`, curves from `easingToken()`; `fill: "none"` unless the element is leaving.
 */
export function play(element, keyframes, options) {
  if (reducedMotion() || !element || typeof element.animate !== "function") return null;
  return element.animate(keyframes, options);
}

/** Resolves after the next frame; at once under reduced motion, where nothing waits to be painted. */
export function nextFrame() {
  if (reducedMotion()) return Promise.resolve();
  return new Promise((resolve) => requestAnimationFrame(() => resolve()));
}

/** Resolves once the current state has been painted (two frames); at once under reduced motion. */
export function afterPaint() {
  if (reducedMotion()) return Promise.resolve();
  return new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(() => resolve())));
}

/**
 * A frame clock through the gate: `step(progress)` from 0 to 1 over `duration` ms; under reduced motion a
 * single `step(1)`. Returns the function that stops it.
 */
export function tween(duration, step) {
  if (reducedMotion() || !(duration > 0)) {
    step(1);
    return () => {};
  }
  let id = 0;
  const start = performance.now();
  const frame = (now) => {
    const progress = Math.min(1, Math.max(0, (now - start) / duration));
    step(progress);
    if (progress < 1) id = requestAnimationFrame(frame);
  };
  id = requestAnimationFrame(frame);
  return () => cancelAnimationFrame(id);
}

/**
 * Resolves when the animations running on `element` — CSS transitions and animations included, its
 * descendants' too with `subtree` — have finished or been cancelled, or after `timeout` ms, whichever
 * comes first. Never hangs: a 0 s transition creates nothing to wait for, an endless one is cut short.
 */
export function settled(element, { timeout = 1000, subtree = false } = {}) {
  const running = element && typeof element.getAnimations === "function" ? element.getAnimations({ subtree }) : [];
  if (!running.length) return Promise.resolve();
  return new Promise((resolve) => {
    const timer = setTimeout(resolve, timeout);
    Promise.allSettled(running.map((animation) => animation.finished)).then(() => {
      clearTimeout(timer);
      resolve();
    });
  });
}

/** A duration token in ms as the cascade gives it now: 0 under reduced motion, where the tokens are zeroed. */
export function durationToken(name, fallback = 0, element = document.documentElement) {
  const raw = getComputedStyle(element).getPropertyValue(name).trim();
  const value = parseFloat(raw);
  if (!raw || Number.isNaN(value)) return fallback;
  return raw.endsWith("ms") ? value : raw.endsWith("s") ? value * 1000 : value;
}

/** A curve token for WAAPI's `easing`: a curve is never typed in a script. */
export function easingToken(name, fallback = "linear", element = document.documentElement) {
  return getComputedStyle(element).getPropertyValue(name).trim() || fallback;
}

/**
 * The two springs of design V4 (docs/design-v4/DESIGN_SYSTEM_V4.md §7), ready to spread into an
 * `animate()` options object. SOFT stops just short of a bounce (ζ ≈ 0.93): layout, heights,
 * reorders. SNAPPY is exactly critical (ζ = 1): indicators, thumbs, anything that follows a
 * pointer or a selection. Nothing in the project springs with a damping below 25 — that is the
 * wobble the owner called «too much». Their CSS twins are the --spring-* tokens.
 */
export const SPRING_SOFT = { type: spring, stiffness: 260, damping: 30 };
export const SPRING_SNAPPY = { type: spring, stiffness: 400, damping: 40 };
