/**
 * The one place this project imports Motion from.
 *
 * Every page-level bundle takes `animate`, `scroll`, `inView`, `stagger` and `spring` from here
 * rather than from "motion" directly, so docs/design-v2/FRONTEND_DEPENDENCIES.md can say what
 * is actually in play and the budget stays honest: adding an import here is adding weight to
 * every bundle that uses this module, and it shows up in one diff.
 *
 * `reducedMotion()` is exported beside them because it is the first thing every animation has to
 * ask. It reads the media query live rather than once: a person can switch the preference while
 * the page is open, and an animation that started before the switch should not be the reason
 * they have to reload.
 */
export { animate, scroll, inView, stagger, spring, hover, press } from "motion";
import { spring } from "motion";

const QUERY = "(prefers-reduced-motion: reduce)";

export function reducedMotion() {
  return typeof matchMedia === "function" && matchMedia(QUERY).matches;
}

/**
 * Run `fn` only when motion is welcome; otherwise apply `settle` (usually: set the final state).
 * Keeps the reduced-motion branch next to the animation it replaces, where a reviewer can see
 * that the final state is the same in both.
 */
export function withMotion(fn, settle) {
  if (reducedMotion()) {
    if (settle) settle();
    return null;
  }
  return fn();
}

/**
 * The two springs of design V4 (docs/design-v4/DESIGN_SYSTEM_V4.md §7), ready to spread into an
 * `animate()` options object. SOFT stops just short of a bounce (ζ ≈ 0.93): layout, heights,
 * reorders. SNAPPY is exactly critical (ζ = 1): indicators, thumbs, anything that follows a
 * pointer or a selection. Nothing in the project springs with a damping below 25 — that is the
 * wobble the owner called «too much».
 */
export const SPRING_SOFT = { type: spring, stiffness: 260, damping: 30 };
export const SPRING_SNAPPY = { type: spring, stiffness: 400, damping: 40 };
