/**
 * The notices — the session's messages, wired (V5.12 §5; the Director's DECISIONS §2 M9, §3 «Notifications»: 21st.dev
 * Toast 24297, its behaviour only — no React, no library). Imported by shell.js only when a page carries one
 * (`[data-notices]`, templates/base.html); without it the messages simply stay where the page drew them.
 *
 *   enter     v5/notice.css: from --reveal-shift away, over --motion-standard (CSS, at the first paint: nothing here)
 *   «Fermer»  every notice can be closed: the control is shown here (hidden without script, where it could do nothing);
 *             the focus, when it was inside, goes to the main content, never to <body>
 *   leave     a success (`data-notice-auto`, in the toast region at the viewport's foot: its going never moves the page)
 *             leaves by itself after AUTO_AFTER — the clock PAUSES while the pointer is over it, while the focus is in
 *             it, and while the page is hidden, and starts again with what was left. An error, a warning, an
 *             information never leave by themselves (WCAG 2.2.1: nothing the person must read is timed away).
 *   out       `is-leaving` (--motion-fast, opacity and --reveal-shift), then the notice is removed; under reduced
 *             motion the tokens are 0 ms and it is removed at once.
 * No word here: «Fermer» is the template's. CSP: classes and attributes only.
 */
import { durationToken } from "./motion.js";

/** A success's stay (DECISIONS §2 M9). */
export const AUTO_AFTER = 6000;

function leave(notice) {
  if (notice.classList.contains("is-leaving")) return;
  const region = notice.parentElement;
  if (notice.contains(document.activeElement)) {
    const main = document.getElementById("main-content");
    if (main) main.focus({ preventScroll: true });
  }
  notice.classList.add("is-leaving");
  window.setTimeout(() => {
    notice.remove();
    if (region && !region.querySelector(".alert")) region.hidden = true;
  }, durationToken("--motion-fast", 0) + 40);
}

/** The clock of a success: AUTO_AFTER in all, paused on hover, on focus and while the page is hidden. */
function clock(notice) {
  let left = AUTO_AFTER;
  let started = 0;
  let timer = 0;
  const holds = new Set();
  const run = () => {
    if (timer || holds.size) return;
    started = performance.now();
    timer = window.setTimeout(() => leave(notice), left);
  };
  const hold = (why) => {
    holds.add(why);
    if (!timer) return;
    window.clearTimeout(timer);
    timer = 0;
    left = Math.max(0, left - (performance.now() - started));
  };
  const free = (why) => {
    holds.delete(why);
    run();
  };
  notice.addEventListener("pointerenter", () => hold("pointer"));
  notice.addEventListener("pointerleave", () => free("pointer"));
  notice.addEventListener("focusin", () => hold("focus"));
  notice.addEventListener("focusout", (event) => {
    if (!notice.contains(event.relatedTarget)) free("focus");
  });
  const visibility = () => (document.hidden ? hold("hidden") : free("hidden"));
  document.addEventListener("visibilitychange", visibility);
  if (document.hidden) holds.add("hidden");
  run();
}

export function initNotices(root = document) {
  root.querySelectorAll("[data-notices] .alert:not([data-notice-wired])").forEach((notice) => {
    notice.setAttribute("data-notice-wired", "");
    const close = notice.querySelector("[data-notice-close]");
    if (close) {
      close.hidden = false;
      close.addEventListener("click", () => leave(notice));
    }
    if (notice.hasAttribute("data-notice-auto")) clock(notice);
  });
}

initNotices();
