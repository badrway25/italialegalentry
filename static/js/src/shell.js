/**
 * Shell behaviour shared by every page: the header that changes state once the page has scrolled
 * (and knows when it floats over a dark chapter), the navigation's sliding indicator, and the
 * section reveals ("documents placed on the table").
 *
 * The navigation itself — drawer, mega-menu, focus management — stays in static/js/main.js, which
 * predates this file and is tested. This file adds what design V4 needs on top of it and nothing
 * that duplicates it.
 *
 * Function of each animation, per docs/design-v4/DESIGN_SYSTEM_V4.md §7.1:
 *   header.is-scrolled     nav (6)      — the page has moved; the letterhead becomes the glass bar
 *   header.is-over-dark    nav (6)      — the bar floats over a dark chapter: 92 % glass, not 85 %
 *   .main-nav__indicator   nav (6)      — ONE bar that travels between items, SPRING_SNAPPY;
 *                                         reduced motion: it jumps
 *   [data-reveal]          panel enter  — sections arrive as sheets laid on a table, 320ms,
 *                                         --ease-enter, from 12px below, siblings staggered 40ms;
 *                                         reduced motion shows them complete, immediately
 */
import { animate, inView, stagger, withMotion, reducedMotion, SPRING_SNAPPY } from "./motion.js";

const EASE_ENTER = [0.25, 1, 0.5, 1];
const DESKTOP = window.matchMedia("(min-width: 80rem)");

/* 1. Header: a sentinel above it, observed; no scroll listener, no layout read. */
const header = document.querySelector(".site-header");
if (header) {
  const sentinel = document.createElement("div");
  sentinel.setAttribute("aria-hidden", "true");
  sentinel.className = "header-sentinel";
  // The bar changes state once the page has moved 24 px (direction §3.2): the sentinel is a
  // 24 px strip at the very top of the page (v4/shell.css) — before the institutional bar, not
  // between it and the header, or the threshold would be measured from the bar's foot — and the
  // bar is «scrolled» from the moment the strip has left the viewport entirely.
  document.body.prepend(sentinel);
  new IntersectionObserver(
    ([entry]) => header.classList.toggle("is-scrolled", !entry.isIntersecting),
    { threshold: 0 },
  ).observe(sentinel);

  /* 1b. Over a dark chapter the glass is denser. The root is shrunk to the band the header
        occupies: a chapter intersecting that band is a chapter under the bar. Rebuilt on
        resize because rootMargin takes pixels. */
  const chapters = [...document.querySelectorAll(".chapter--dark")];
  if (chapters.length) {
    let observer = null;
    const under = new Set();
    const watch = () => {
      if (observer) observer.disconnect();
      under.clear();
      const band = header.getBoundingClientRect().height || 64;
      observer = new IntersectionObserver(
        (entries) => {
          for (const entry of entries) {
            if (entry.isIntersecting) under.add(entry.target);
            else under.delete(entry.target);
          }
          header.classList.toggle("is-over-dark", under.size > 0);
        },
        { rootMargin: `0px 0px -${Math.max(0, window.innerHeight - band)}px 0px` },
      );
      chapters.forEach((chapter) => observer.observe(chapter));
    };
    watch();
    let resizeTimer = 0;
    window.addEventListener("resize", () => {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(watch, 150);
    });
  }
}

/* 2. The navigation's indicator: one 2px bar under the list, moved to the item under the pointer
      or the focus, and back to the current item. Positioned from the list's reading edge, so the
      same measure works in both directions; SPRING_SNAPPY through Motion, a jump under reduced
      motion. Only at desktop widths, where the list is a row. */
const navList = document.querySelector(".main-nav__list");
if (navList && header) {
  const links = [...navList.querySelectorAll(".main-nav__link")];
  const current = () => links.find((link) => link.hasAttribute("aria-current")) || null;
  // The bar is a child of the HEADER, not of the list: the list must stay unpositioned so the
  // mega-menu, absolutely positioned inside it, takes the header as its containing block and
  // spans the full width. The bar therefore sits on the header's own bottom edge.
  const indicator = document.createElement("span");
  indicator.className = "main-nav__indicator";
  indicator.setAttribute("aria-hidden", "true");
  header.append(indicator);
  let shown = null;

  const moveTo = (link, immediate = false) => {
    if (!DESKTOP.matches || !link) {
      indicator.classList.remove("is-on");
      shown = null;
      return;
    }
    const rtl = document.documentElement.dir === "rtl";
    const list = header.getBoundingClientRect();
    const box = link.getBoundingClientRect();
    const offset = rtl ? list.right - box.right : box.left - list.left;
    const x = rtl ? -offset : offset;
    const first = !indicator.classList.contains("is-on");
    indicator.classList.add("is-on");
    if (immediate || first || reducedMotion()) {
      indicator.style.transform = `translateX(${x}px)`;
      indicator.style.width = `${box.width}px`;
    } else {
      animate(indicator, { x, width: box.width }, SPRING_SNAPPY);
    }
    shown = link;
  };

  const settle = () => moveTo(current(), true);
  links.forEach((link) => {
    link.addEventListener("pointerenter", () => moveTo(link));
    link.addEventListener("focus", () => moveTo(link));
  });
  navList.addEventListener("pointerleave", () => moveTo(current()));
  navList.addEventListener("focusout", (event) => {
    if (!navList.contains(event.relatedTarget)) moveTo(current());
  });
  settle();
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(settle);
  DESKTOP.addEventListener("change", settle);
  let resizeTimer = 0;
  window.addEventListener("resize", () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => moveTo(shown || current(), true), 150);
  });
}

/* 3. Password fields show and hide themselves (design V4 §3.3): a labelled control beside the
      field swaps the input's type; its label says what pressing it will do, aria-pressed says
      the state. Nothing is submitted, nothing is stored. */
document.querySelectorAll("[data-password-toggle]").forEach((button) => {
  const input = document.getElementById(button.getAttribute("aria-controls"));
  if (!input) return;
  button.addEventListener("click", () => {
    const shown = input.type === "text";
    input.type = shown ? "password" : "text";
    button.setAttribute("aria-pressed", shown ? "false" : "true");
    button.textContent = shown ? button.dataset.labelShow : button.dataset.labelHide;
    input.focus({ preventScroll: true });
  });
});

/* 4. A submitted form's primary button is busy until the answer arrives (DS §7.1 pattern 13):
      the meter, drawn by v4/buttons.css on `.is-busy`, replaces the disabled greying main.js
      applies to the same button; `aria-busy` tells assistive technology why nothing happens. */
document.querySelectorAll("form[data-single-submit]").forEach((form) => {
  form.addEventListener("submit", () => {
    form.querySelectorAll('button[type="submit"]').forEach((button) => {
      button.classList.add("is-busy");
      button.setAttribute("aria-busy", "true");
    });
  });
});

/* 5. Reveals. Grouped by parent so siblings stagger; a late sibling below the first one's
      viewport gets its own trigger, or it would arrive early and unseen. */
const reveals = [...document.querySelectorAll("[data-reveal]")];
const settleAll = () => reveals.forEach((el) => el.classList.add("is-in"));

withMotion(() => {
  const groups = new Map();
  for (const el of reveals) {
    const key = el.parentElement;
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(el);
  }
  for (const [, els] of groups) {
    inView(
      els[0],
      () => {
        const pending = els.filter((el) => !el.classList.contains("is-in"));
        pending.forEach((el) => el.classList.add("is-in"));
        animate(
          pending,
          { opacity: [0, 1], transform: ["translateY(12px)", "translateY(0)"] },
          { duration: 0.32, ease: EASE_ENTER, delay: stagger(0.04) },
        );
      },
      { margin: "0px 0px -12% 0px" },
    );
    els.slice(1).forEach((el) =>
      inView(
        el,
        () => {
          if (el.classList.contains("is-in")) return;
          el.classList.add("is-in");
          animate(
            el,
            { opacity: [0, 1], transform: ["translateY(12px)", "translateY(0)"] },
            { duration: 0.32, ease: EASE_ENTER },
          );
        },
        { margin: "0px 0px -8% 0px" },
      ),
    );
  }
}, settleAll);
