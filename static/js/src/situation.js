/**
 * «Ma situation» as a guided form (docs/design-v4/CREATIVE_DIRECTION.md §3.7): one question at a
 * time, the Stepper as the map, «Précédent» · «Continuer» in the foot.
 *
 * Progressive enhancement only. The form is ONE form saved in ONE post; this script hides the
 * questions that are not the current one (the `hidden` attribute — hidden fields are still
 * submitted), it never removes, reorders or validates anything. Without it the questions follow
 * each other and the submit is there; with it the submit is there too, on every step, because a
 * person may want to save after one answer.
 *
 *   transition   pattern «wizard»: the leaving question fades 120 ms (--motion-fast), then the arriving
 *                one comes in 200 ms (--motion-standard) from 16 px in the reading direction, both on
 *                --ease-enter (a small surface leaves on the enter curve, MS-O2); nothing under reduced motion,
 *                nothing when the keyboard asks (tier 0, R-07: Enter or Space on «Continuer», «Précédent» or a
 *                Stepper link — head.js writes html[data-input="key"] on the keydown, before the click)
 *   interrupted  a change asked while another is in flight lands that one first (its animations cancelled, no
 *                inline opacity left) and plays its own arrival only; the earlier change's late steps see that
 *                their turn has passed and do nothing, so one question is always drawn and keeps the focus
 *   stepper      the current node moves; a node fills when its question gets an answer
 *   hash         #q-<name> opens that question (the Stepper's links work without the script)
 *
 * The motion is the Web Animations API through motion.js's play(), and the reduced-motion question, the
 * frame wait and the wait on the leaving fade (settled(), with its timeout) are motion.js's too: the one
 * gate (V5.4 plan §1.5, W1-D) — the setting, or the preview's html.rm flag. No library (W4-B: the Motion
 * library's animate() left; same clock, same distance, same order — the curve is now the token's, where
 * Motion had applied its own default ease-out). Nothing moves at load (V5.4 plan §1.5, W3-D): the first
 * question is shown as it is, and the submit takes its role (secondary while stepping) without its colour
 * transition.
 */

import { afterPaint, durationToken, easingToken, play, reducedMotion, settled } from "./motion.js";

const form = document.querySelector("[data-wizard]");
if (form) {
  const steps = [...form.querySelectorAll("[data-wizard-step]")];
  const marks = [...document.querySelectorAll("[data-wizard-mark]")];
  const prev = form.querySelector("[data-wizard-prev]");
  const next = form.querySelector("[data-wizard-next]");
  const position = form.querySelector("[data-wizard-position]");
  const direction = () => (document.documentElement.dir === "rtl" ? -1 : 1);
  let index = -1;

  const answered = (step) =>
    [...step.querySelectorAll("input, select, textarea")].some((control) => {
      if (control.type === "radio" || control.type === "checkbox") return control.checked && control.value !== "";
      return control.value.trim() !== "";
    });

  const submit = form.querySelector("[data-wizard-submit]");
  // The change in flight: its turn (each change takes the next) and its animations — the leaving fade, then the
  // arrival. Between the press and the arrival the arriving question carries an inline opacity of 0.
  let generation = 0;
  let flight = [];
  const plain = (step) => {
    step.style.removeProperty("opacity");
    if (!step.getAttribute("style")) step.removeAttribute("style");
  };
  // Lands the change in flight, if there is one: its animations cancelled, no question left at an inline opacity.
  const land = () => {
    const moving = steps.some((step) => step.style.opacity !== "") || flight.some((a) => a.playState === "running");
    flight.forEach((animation) => animation.cancel());
    flight = [];
    steps.forEach(plain);
    return moving;
  };

  const show = (target, travel, focus) => {
    if (target < 0 || target >= steps.length || target === index) return;
    const turn = ++generation;
    const interrupted = land();
    const first = index < 0;
    const leaving = index >= 0 ? steps[index] : null;
    index = target;
    const arriving = steps[index];
    const last = index === steps.length - 1;
    // Tier 0 (plan §1.5, R-07): a change the keyboard asks for is there at once, as under reduced motion.
    const animated = Boolean(travel) && !reducedMotion() && document.documentElement.getAttribute("data-input") !== "key";
    // The whole pattern — 120 ms out, then 200 ms in, never two panels at once — unless a change was interrupted:
    // its leaving question is gone at once and the new one plays its arrival only.
    const sequence = animated && Boolean(leaving) && !interrupted;
    // The arriving question is drawn invisible until the leaving one has gone.
    if (sequence) arriving.style.opacity = "0";
    steps.forEach((step, k) => {
      step.hidden = k !== index;
    });
    marks.forEach((mark, k) => {
      mark.classList.toggle("wstep__item--current", k === index);
      if (k === index) mark.setAttribute("aria-current", "step");
      else mark.removeAttribute("aria-current");
    });
    prev.hidden = index === 0;
    next.hidden = last;
    // One PRIMARY per screen: «Continuer» while stepping, the submit on the last question.
    if (submit) {
      // At load the submit takes its role with no transition: the colour change is applied in one style pass
      // under `transition: none`, which leaves once that state has been painted.
      if (first) submit.style.transition = "none";
      submit.classList.toggle("btn--primary", last);
      submit.classList.toggle("btn--secondary", !last);
      if (first) {
        void getComputedStyle(submit).backgroundColor;
        afterPaint().then(() => {
          submit.style.removeProperty("transition");
          if (!submit.getAttribute("style")) submit.removeAttribute("style");
        });
      }
    }
    if (position) position.textContent = `${index + 1} / ${steps.length}`;
    // The URL follows the question (the Stepper's links are anchors), without a history entry.
    if (travel && window.history.replaceState) window.history.replaceState(null, "", `#${arriving.id}`);
    if (focus) arriving.focus({ preventScroll: false });
    if (!animated) return;
    const ease = easingToken("--ease-enter");
    // Each late step first asks whether its turn is still the current one: a later change has landed this one.
    const arrive = () => {
      if (turn !== generation) return;
      const shift = `translateX(${16 * travel * direction()}px)`;
      const arrival = play(arriving, { opacity: [0, 1], transform: [shift, "translateX(0)"] }, { duration: durationToken("--motion-standard", 200), easing: ease });
      flight = arrival ? [arrival] : [];
      plain(arriving);
    };
    if (!sequence) {
      arrive();
      return;
    }
    leaving.hidden = false;
    const fast = durationToken("--motion-fast", 120);
    // The leaving fade holds its last frame (`fill: forwards`) until its question is hidden, then lets go:
    // the natural state IS the final state, so no `style` attribute survives the swap.
    const leave = play(leaving, { opacity: [1, 0] }, { duration: fast, easing: ease, fill: "forwards" });
    flight = leave ? [leave] : [];
    settled(leaving, { timeout: fast + 100 }).then(() => {
      if (turn !== generation) return;
      leaving.hidden = true;
      if (leave) leave.cancel();
      arrive();
    });
  };

  prev.addEventListener("click", () => show(index - 1, -1, true));
  next.addEventListener("click", () => show(index + 1, 1, true));
  document.querySelectorAll("[data-wizard-go]").forEach((link) => {
    link.addEventListener("click", (event) => {
      event.preventDefault();
      const target = Number(link.dataset.wizardGo) - 1;
      show(target, Math.sign(target - index) || 1, true);
    });
  });

  // A node fills as soon as its question has an answer — the same rule as the profile's count.
  steps.forEach((step, k) => {
    step.addEventListener("input", () => marks[k]?.classList.toggle("wstep__item--done", answered(step)));
    step.addEventListener("change", () => marks[k]?.classList.toggle("wstep__item--done", answered(step)));
  });

  // Errors after a post: open the first question that carries one; otherwise the hash, or the first.
  const erred = steps.findIndex((step) => step.querySelector(".form-field__errors"));
  const fromHash = () => steps.findIndex((step) => `#${step.id}` === window.location.hash);
  form.classList.add("wiz--guided");
  const hashed = fromHash();
  show(erred >= 0 ? erred : hashed >= 0 ? hashed : 0, 0, false);
  window.addEventListener("hashchange", () => {
    const target = fromHash();
    if (target >= 0) show(target, Math.sign(target - index) || 1, true);
  });
}
