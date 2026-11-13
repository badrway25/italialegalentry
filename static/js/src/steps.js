/**
 * THE STEPS OF A FORM (V5.15 W3, lane B; DECISIONS §5.12) — fetched by fieldcheck.js where a `form[data-steps]` is
 * (the company's need, the «Recueil des besoins», the sign-up). 21st.dev «Wizard Steps» 23576, ported to the page:
 * no React, no motion library — its state model (the current step, the furthest reached, the direction of travel),
 * its rail (square tiles that scale from 0.92 to 1, connectors that fill), the position said once, politely, its
 * panel (22 px in the direction of travel, 280 ms, cut under reduced motion and from the keyboard) and its focus rule
 * (after a move, the step's own legend).
 * What ILE changes: a done step keeps its NUMBER on a lit tile — never a tick (O14: a tick would read as a verdict);
 * the steps are the form's fieldsets, all in the page (templates/components/form_steps.html), so without this
 * module the form is the same form, every step shown; the server stays the judge — a step is checked through
 * fieldcheck.js's own check (the server's words) before the next one, and a form that came back with errors opens
 * on the first step that holds one; the address keeps the step (`?etape=`).
 * Round 1 (V5.15 W3): the address never opens a step past the first one whose required fields are empty (a reload
 * or a deep link to `?etape=envoi` opens where the form really stands — the values are never kept by the script:
 * no personal datum in the browser's storage); the side rail's steps not yet reached leave the Tab order; the head
 * rail is a picture (aria-hidden: the live line and the legend speak); a word still in its French source carries
 * its language (`data-msg-<name>-lang`); the panel's light is drawn on each arrival. The review is its own module
 * (steps-review.js), fetched when the last step is first reached.
 * CSP: no inline style, no string evaluated; every word is the page's (the form's `data-msg-*`).
 */

import { play, reducedMotion } from "./motion.js";

const EASE = "cubic-bezier(0.23, 1, 0.32, 1)";
const root = document.documentElement;
// (F1) the one gate (motion.js: the person's setting and html.rm), and at once from the keyboard
const still = () => reducedMotion() || root.getAttribute("data-input") === "key";

function el(tag, cls, text) {
  const node = document.createElement(tag);
  if (cls) node.className = cls;
  if (text !== undefined) node.textContent = text;
  return node;
}

function setup(form, api) {
  if (form.dataset.stepsReady) return;
  const steps = [...form.querySelectorAll(".form-step")];
  if (steps.length < 2) return;
  form.dataset.stepsReady = "1";
  const key = (name) => `msg${name[0].toUpperCase()}${name.slice(1)}`;
  const msg = (name) => form.dataset[key(name)] || "";
  /** a node that says one of the form's words, in that word's language */
  const word = (tag, cls, name) => {
    const node = el(tag, cls, msg(name));
    const lang = form.dataset[`${key(name)}Lang`];
    if (lang) node.lang = lang;
    return node;
  };
  const total = steps.length;
  const labels = steps.map((step) => step.dataset.stepLabel || "");
  const actions = form.querySelector(":scope > .form__actions");
  const reviewSeat = form.hasAttribute("data-steps-review-on") ? steps[total - 1].querySelector("[data-steps-review]") : null;
  const side = form.closest(".formwork")?.querySelector("[data-steps-rail]");
  const sideItems = side ? [...side.querySelectorAll("[data-rail-step]")] : [];
  const glyph = (name, cls) => api.glyph(name, cls) || document.createTextNode("");
  const rtl = getComputedStyle(form).direction === "rtl";
  const count = (i) => msg("position").replace("%(n)s", String(i + 1)).replace("%(total)s", String(total));

  // ---- where to start: the first step the server sent back with an error; else the address — but never past the
  //      first step whose required fields are still empty (a reload, a deep link); else the first
  const asked = Math.max(0, steps.findIndex((step) => step.dataset.step === new URLSearchParams(location.search).get("etape")));
  const errored = steps.findIndex((step) => step.hasAttribute("data-step-errors"));
  let at = 0;
  if (errored >= 0) at = errored;
  else while (at < asked && !api.validate(steps[at], true)) at += 1;
  let furthest = errored >= 0 ? total - 1 : at;

  // ---- the head rail (where the side is not shown; a picture — the live line and the legend speak)
  const live = el("p", "visually-hidden");
  live.setAttribute("aria-live", "polite");
  const head = el("div", "steps-head");
  head.setAttribute("aria-hidden", "true");
  const list = el("ol", "steps-head__list");
  head.append(list);
  form.prepend(head);
  steps[0].before(live);

  // ---- the navigation: «Précédent» and «Continuer»; on the last step «Précédent» joins the form's own actions
  const nav = el("div", "steps-nav");
  const back = el("button", "btn btn--ghost btn--lg steps-nav__back");
  back.type = "button";
  back.append(glyph("arrow-start", "icon icon--flip-rtl"), word("span", "", "back"));
  const next = el("button", "btn btn--primary btn--lg steps-nav__next");
  next.type = "button";
  next.append(word("span", "", "next"), glyph("arrow", "icon icon--flip-rtl"));
  nav.append(back, next);
  steps[total - 1].after(nav);

  /** the two rails: the head's tiles (a pointer may go back on them) and the side's links (reached ones only) */
  function drawRails() {
    list.replaceChildren(...steps.map((step, i) => {
      const li = el("li", "steps-head__item");
      li.dataset.state = i < at ? "done" : i === at ? "current" : "todo";
      const tile = el("span", "steps-head__tile", String(i + 1));
      if (i <= furthest && i !== at) {
        tile.dataset.go = String(i);
        tile.classList.add("is-reachable");
      }
      li.append(tile);
      if (i < total - 1) li.append(el("span", "steps-head__bar"));
      return li;
    }));
    sideItems.forEach((item, i) => {
      item.dataset.state = i < at ? "done" : i === at ? "current" : "todo";
      const link = item.querySelector("a");
      if (!link) return;
      if (i === at) link.setAttribute("aria-current", "step"); else link.removeAttribute("aria-current");
      if (i > furthest) {
        link.setAttribute("aria-disabled", "true");
        link.tabIndex = -1;
      } else {
        link.removeAttribute("aria-disabled");
        link.removeAttribute("tabindex");
      }
    });
  }
  list.addEventListener("click", (event) => {
    const tile = event.target.closest("[data-go]");
    if (tile) goTo(Number(tile.dataset.go), { check: Number(tile.dataset.go) > at });
  });

  function paint() {
    steps.forEach((step, i) => { step.hidden = i !== at; });
    const last = at === total - 1;
    form.toggleAttribute("data-steps-last", last);
    back.hidden = at === 0;
    next.hidden = last;
    if (last && actions) actions.prepend(back); else nav.prepend(back);
    nav.hidden = last;
    drawRails();
    if (last && reviewSeat) {
      import("./steps-review.js").then((m) => m.drawReview(reviewSeat, steps.slice(0, -1), labels, { msg, word, glyph, goTo }));
    }
    const label = el("span", "", labels[at]);
    if (steps[at].dataset.stepLang) label.lang = steps[at].dataset.stepLang;
    live.replaceChildren(word("span", "", "position"), document.createTextNode(" — "), label);
    live.firstChild.textContent = count(at);
    const address = new URL(location.href);
    address.searchParams.set("etape", steps[at].dataset.step);
    history.replaceState(history.state, "", address);
  }

  function slide(step, direction) {
    if (still()) return;
    const shift = 22 * direction * (rtl ? -1 : 1);
    play(step, [{ opacity: 0, transform: `translateX(${shift}px)` }, { opacity: 1, transform: "none" }], { duration: 280, easing: EASE });
    // the panel's light is drawn again from the reading edge (v5/_formwork.css, `.is-arriving`)
    form.classList.remove("is-arriving");
    void form.offsetWidth;
    form.classList.add("is-arriving");
  }

  function arrive(step) {
    const legend = step.querySelector(".form-step__legend");
    if (legend) {
      legend.tabIndex = -1;
      legend.focus({ preventScroll: true });
    }
    const top = form.getBoundingClientRect().top;
    if (top < 0 || top > innerHeight * 0.6) form.scrollIntoView({ block: "start", behavior: still() ? "auto" : "smooth" });
  }

  function goTo(i, { check = true, focus = true } = {}) {
    if (i === at || i < 0 || i >= total) return;
    if (check && i > at) {
      for (let k = at; k < i; k += 1) {
        const bad = api.validate(steps[k]);
        if (bad) {
          if (k !== at) { at = k; paint(); }
          bad.focus();
          return;
        }
      }
    }
    const direction = i > at ? 1 : -1;
    at = i;
    furthest = Math.max(furthest, i);
    paint();
    slide(steps[at], direction);
    if (focus) arrive(steps[at]);
  }

  back.addEventListener("click", () => goTo(at - 1, { check: false }));
  next.addEventListener("click", () => goTo(at + 1));
  for (const [i, item] of sideItems.entries()) {
    item.querySelector("a")?.addEventListener("click", (event) => {
      event.preventDefault();
      if (i <= furthest) goTo(i, { check: i > at });
    });
  }
  // Enter in a field of a step that is not the last moves on, never sends (capture: before the single-submit guard)
  form.addEventListener("submit", (event) => {
    if (at < total - 1) {
      event.preventDefault();
      event.stopImmediatePropagation();
      goTo(at + 1);
    }
  }, true);
  // the error summary's links open the step that holds the field
  form.querySelector(".form-errors")?.addEventListener("click", (event) => {
    const link = event.target.closest("a[href^='#']");
    const target = link && document.getElementById(decodeURIComponent(link.hash.slice(1)));
    const owner = target?.closest(".form-step");
    if (!owner) return;
    event.preventDefault();
    goTo(steps.indexOf(owner), { check: false, focus: false });
    target.focus();
  });

  paint();
}

/** Every `[data-steps]` form under `scope`; `api.validate(step, quiet)` checks a step's fields and returns the first
 *  control in error, or null (`quiet`: without painting), and `api.glyph(name, class)` draws a symbol of the chrome
 *  sprite (fieldcheck.js). */
export function initSteps(scope, api) {
  for (const form of scope.querySelectorAll("form[data-steps]")) setup(form, api);
}
