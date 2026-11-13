/**
 * C · «il racconto» — the sticky story (design V5.22, SECTION_SYSTEM_V2 §2 C; lane S). A split chunk loaded by rise.js
 * for [data-sec-js~="racconto"]. The step in the middle band of the viewport is the active one: it writes `data-step`
 * on the figure (whose layers draw or light per state, v5/_sec-racconto.css) and `data-active` on itself (its text at
 * --text-1, the others at --text-2). Scrolling only — nothing to operate, the reading order unchanged. Under reduced
 * motion and html.rm nothing is written: the figure stands in its final drawing, every step at full ink.
 */
import { reducedMotion } from "../motion.js";

export default function initRacconto() {
  if (reducedMotion()) return;
  document.querySelectorAll("[data-sec-js~='racconto']").forEach((root) => {
    const figure = root.querySelector(".racconto__figura");
    const steps = [...root.querySelectorAll(".racconto__passo")];
    if (!figure || !steps.length) return;
    root.dataset.live = "";
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          figure.dataset.step = entry.target.dataset.step;
          steps.forEach((step) => step.toggleAttribute("data-active", step === entry.target));
        });
      },
      { rootMargin: "-45% 0px -45% 0px" },
    );
    steps.forEach((step) => observer.observe(step));
    addEventListener("pagehide", () => observer.disconnect(), { once: true });
  });
}
