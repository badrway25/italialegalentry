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
 *   transition   pattern «wizard»: the leaving question fades 120 ms, the arriving one comes in
 *                200 ms from 16 px in the reading direction; nothing under reduced motion
 *   stepper      the current node moves; a node fills when its question gets an answer
 *   hash         #q-<name> opens that question (the Stepper's links work without the script)
 *
 * Motion, the reduced-motion question and the frame wait come from motion.js: the one gate
 * (V5.4 plan §1.5, W1-D) — the setting, or the preview's html.rm flag. Nothing moves at load (V5.4
 * plan §1.5, W3-D): the first question is shown as it is, and the submit takes its role (secondary
 * while stepping) without its colour transition.
 */

import { afterPaint, animate, nextFrame, reducedMotion } from "./motion.js";

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
  const show = (target, travel, focus) => {
    if (target < 0 || target >= steps.length || target === index) return;
    const first = index < 0;
    const leaving = index >= 0 ? steps[index] : null;
    index = target;
    const arriving = steps[index];
    const last = index === steps.length - 1;
    const animated = Boolean(travel) && !reducedMotion();
    // The arriving question is drawn invisible until the leaving one has gone (pattern «wizard»:
    // 120 ms out, then 200 ms in — never two panels at once).
    if (animated) arriving.style.opacity = "0";
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
    if (animated) {
      if (leaving) leaving.hidden = false;
      const leave = leaving ? animate(leaving, { opacity: [1, 0] }, { duration: 0.12, easing: "ease-in" }) : null;
      // Motion commits the final values as inline styles: each animation is cancelled once it has
      // finished (the natural state IS the final state), so no `style` attribute survives the swap.
      const clear = (controls, element) => {
        // A frame later: Motion commits its final values right after `finished` resolves.
        nextFrame().then(() => {
          if (controls && typeof controls.cancel === "function") controls.cancel();
          ["opacity", "transform", "translate"].forEach((property) => element.style.removeProperty(property));
          if (!element.getAttribute("style")) element.removeAttribute("style");
        });
      };
      const enter = () => {
        if (leaving) {
          leaving.hidden = true;
          clear(leave, leaving);
        }
        arriving.style.removeProperty("opacity");
        const arrive = animate(arriving, { opacity: [0, 1], x: [16 * travel * direction(), 0] }, { duration: 0.2, easing: "ease-out" });
        arrive.finished.then(() => clear(arrive, arriving));
      };
      if (leave) leave.finished.then(enter);
      else enter();
    }
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
