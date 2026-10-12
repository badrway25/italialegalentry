/**
 * Italy Legal Entry™ — progressive enhancement (ES module, no framework, no external libs).
 *
 * Every behaviour here enhances markup that already works without JavaScript:
 *  - (the public navigation moved to static/js/src/nav.js, bundled into shell.js: design V5 «Il portico»,
 *    V5.4 plan §1.12 and §2.2's slice of this file, W2-C1)
 *  - details-based dropdowns: Escape / outside click — a fallback for the pages that do not load the overlay
 *    system yet (static/js/src/overlay.js owns every dropdown, dialog, drawer, popover and tooltip of a page
 *    that does: V5.4 plan §1.14, W2-A)
 *  - accordion (exclusive mode, a link opens its row), tabs (roving tabindex, one indicator), stepper
 *    (client-side panels)
 *  - reveal-on-scroll (never hides content when JS is off; honours prefers-reduced-motion)
 *  - optional count-up counters
 *
 * Conventions: behaviours are attached through data-* attributes; no inline handlers
 * (CSP: script-src 'self'); all text stays in the HTML (translatable server-side).
 */

const REDUCED_MOTION = window.matchMedia("(prefers-reduced-motion: reduce)");

const qs = (sel, root = document) => root.querySelector(sel);
const qsa = (sel, root = document) => Array.from(root.querySelectorAll(sel));

/* ------------------------------------------------------------------------ */
/* Form error summary: after a server-side validation round-trip the page    */
/* reloads at the top; move focus to the summary so keyboard and screen-     */
/* reader users land on the errors (WCAG 3.3.1 / 4.1.3).                     */
/* ------------------------------------------------------------------------ */
function initFormErrorFocus() {
  const summary = document.getElementById("form-errors");
  if (!summary) return;
  summary.focus({ preventScroll: true });
  summary.scrollIntoView({ block: "center", behavior: REDUCED_MOTION.matches ? "auto" : "smooth" });
}

/* ------------------------------------------------------------------------ */
/* 2. Details-based dropdowns — a FALLBACK (W2-A): the overlay system        */
/*    (static/js/src/overlay.js) owns the dropdowns of every page that loads */
/*    it — the console's — and marks each `data-dropdown="overlay"`, which   */
/*    this function then leaves alone. It serves the pages that do not load  */
/*    it yet: the letterhead's account menu, until W2-C2 moves it onto the   */
/*    popover and shell.js imports overlay.js — and this function goes.      */
/* ------------------------------------------------------------------------ */
function initDropdowns() {
  const dropdowns = qsa("details[data-dropdown]");
  if (!dropdowns.length) return;
  // overlay.js loads after this module (document order): who owns a dropdown is read at the event, not here
  const mine = (details) => details.getAttribute("data-dropdown") !== "overlay";

  dropdowns.forEach((details) => {
    const summary = qs("summary", details);
    details.addEventListener("toggle", () => {
      if (!mine(details)) return;
      if (details.open) {
        dropdowns.forEach((d) => d !== details && mine(d) && d.removeAttribute("open"));
        summary?.setAttribute("aria-expanded", "true");
      } else {
        summary?.setAttribute("aria-expanded", "false");
      }
    });
    summary?.setAttribute("aria-expanded", details.open ? "true" : "false");
    details.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && details.open && mine(details)) {
        event.preventDefault();
        // close this dropdown and stop: Escape dismisses the list, not a menu it may sit in
        event.stopPropagation();
        details.removeAttribute("open");
        summary?.focus();
      }
    });
    details.addEventListener("focusout", (event) => {
      if (mine(details) && !details.contains(event.relatedTarget)) details.removeAttribute("open");
    });
  });

  document.addEventListener("click", (event) => {
    dropdowns.forEach((d) => {
      if (d.open && mine(d) && !d.contains(event.target)) d.removeAttribute("open");
    });
  });
}

/* ------------------------------------------------------------------------ */
/* 3. Accordion — native <details>: exclusive mode for browsers without      */
/*    <details name>, and a link to a row opens it                           */
/* ------------------------------------------------------------------------ */
function initAccordions() {
  qsa('[data-accordion="single"]').forEach((group) => {
    const panels = qsa("details", group);
    panels.forEach((panel) => {
      panel.addEventListener("toggle", () => {
        if (!panel.open) return;
        panels.forEach((other) => {
          if (other !== panel && other.open) other.removeAttribute("open");
        });
      });
    });
  });
  // A link to a row (/faq/#key, «Lien direct vers cette question») lands on the answer, not on a closed question.
  const openTarget = () => {
    let target = null;
    try {
      target = location.hash.length > 1 ? document.getElementById(decodeURIComponent(location.hash.slice(1))) : null;
    } catch (_) {
      /* a malformed fragment names nothing */
    }
    if (target && target.matches("details.accordion__item")) target.open = true;
  };
  openTarget();
  window.addEventListener("hashchange", openTarget);
}

/* ------------------------------------------------------------------------ */
/* 4. Tabs — WAI-ARIA tabs: roving tabindex, automatic activation, the one   */
/*    indicator of static/css/v5/tabs.css; stacked sections without JS       */
/* ------------------------------------------------------------------------ */
function initTabs() {
  qsa("[data-tabs]").forEach((widget) => {
    const list = qs("[role=tablist]", widget);
    const tabs = qsa("[role=tab]", widget);
    const panels = tabs.map((tab) => document.getElementById(tab.getAttribute("aria-controls")));
    if (!list || !tabs.length || panels.some((panel) => !panel)) return;
    let current = -1;

    // The indicator (design V5, V5.4 plan §1.5 MS-O3): where the selected label is inside the list, in physical
    // pixels from the list's top left corner — the same measure in both directions — written as custom
    // properties; tabs.css moves a 1 px box there with transform alone. Nothing is animated from here: a
    // pointer's choice sets .is-travelling and the sheet's transition does the rest (0 ms under reduced motion).
    const place = () => {
      const tab = tabs[current];
      const box = list.getBoundingClientRect();
      const r = tab ? tab.getBoundingClientRect() : null;
      if (!r || !r.width) return; // not rendered (a hidden ancestor): the next measure will find it
      const pad = parseFloat(getComputedStyle(tab).paddingInlineStart) || 0;
      const x = r.left - box.left + pad;
      const before = parseFloat(widget.style.getPropertyValue("--tabs-x"));
      widget.style.setProperty("--tabs-dir", Number.isFinite(before) && x < before ? "-1" : "1");
      widget.style.setProperty("--tabs-x", `${x.toFixed(2)}px`);
      widget.style.setProperty("--tabs-y", `${(r.bottom - box.top - 1).toFixed(2)}px`);
      widget.style.setProperty("--tabs-w", Math.max(1, r.width - 2 * pad).toFixed(2));
      widget.classList.add("is-ready");
    };

    // `travel` is true for a pointer's choice only: from the keyboard, at load, from a link and on a resize the
    // change is static (tier 0). The class is set before anything is measured, so the arriving panel is first
    // rendered with its transition.
    const select = (index, { focus = false, travel = false } = {}) => {
      widget.classList.toggle("is-travelling", travel && index !== current);
      if (index !== current) {
        current = index;
        tabs.forEach((tab, i) => {
          const selected = i === index;
          tab.setAttribute("aria-selected", selected ? "true" : "false");
          tab.tabIndex = selected ? 0 : -1;
          panels[i].hidden = !selected;
        });
        place();
      }
      if (focus) tabs[index].focus();
    };

    tabs.forEach((tab, index) => {
      // event.detail is the click count: 0 when Enter or Space made the click
      tab.addEventListener("click", (event) => select(index, { travel: event.detail > 0 }));
      tab.addEventListener("keydown", (event) => {
        if (event.altKey || event.ctrlKey || event.metaKey) return; // Alt + arrow is the browser's «back»
        const rtl = getComputedStyle(list).direction === "rtl";
        let target = null;
        if (event.key === "ArrowRight") target = index + (rtl ? -1 : 1);
        else if (event.key === "ArrowLeft") target = index + (rtl ? 1 : -1);
        else if (event.key === "Home") target = 0;
        else if (event.key === "End") target = tabs.length - 1;
        if (target === null) return;
        event.preventDefault();
        select((target + tabs.length) % tabs.length, { focus: true });
      });
    });

    const fromHash = () => panels.findIndex((panel) => location.hash === `#${panel.id}`);
    const marked = tabs.findIndex((tab) => tab.getAttribute("aria-selected") === "true");
    select(fromHash() >= 0 ? fromHash() : Math.max(0, marked));
    window.addEventListener("hashchange", () => {
      if (fromHash() >= 0) select(fromHash());
    });
    // The labels move when the face arrives, the list wraps or the page is resized: measure again, in place.
    if ("ResizeObserver" in window) {
      const observer = new ResizeObserver(() => {
        widget.classList.remove("is-travelling");
        place();
      });
      [list, ...tabs].forEach((el) => observer.observe(el));
    }
  });
}

/* ------------------------------------------------------------------------ */
/* 5. Stepper — client-side panels (all panels visible without JS)           */
/* ------------------------------------------------------------------------ */
function initSteppers() {
  qsa("[data-stepper]").forEach((widget) => {
    const steps = qsa("[data-step]", widget);
    const markers = qsa("[data-step-marker]", widget);
    if (steps.length < 2) return;
    let current = Math.max(0, steps.findIndex((s) => s.hasAttribute("data-step-current")));

    const show = (index) => {
      current = Math.min(Math.max(index, 0), steps.length - 1);
      steps.forEach((step, i) => {
        step.hidden = i !== current;
      });
      markers.forEach((marker, i) => {
        marker.classList.toggle("stepper__item--current", i === current);
        marker.classList.toggle("stepper__item--done", i < current);
        if (i === current) marker.setAttribute("aria-current", "step");
        else marker.removeAttribute("aria-current");
      });
      const heading = qs("h2, h3, [data-step-focus]", steps[current]);
      if (heading) {
        heading.tabIndex = -1;
        heading.focus({ preventScroll: false });
      }
    };

    widget.addEventListener("click", (event) => {
      const next = event.target.closest("[data-step-next]");
      const prev = event.target.closest("[data-step-prev]");
      if (next) {
        event.preventDefault();
        show(current + 1);
      } else if (prev) {
        event.preventDefault();
        show(current - 1);
      }
    });
    steps.forEach((step, i) => {
      step.hidden = i !== current;
    });
  });
}

/* ------------------------------------------------------------------------ */
/* 6. Reveal on scroll — additive only; reduced motion => visible at once     */
/* ------------------------------------------------------------------------ */
function initReveal() {
  const targets = qsa(".reveal");
  if (!targets.length) return;
  const showAll = () => targets.forEach((el) => el.classList.add("is-visible"));
  if (REDUCED_MOTION.matches || !("IntersectionObserver" in window)) {
    showAll();
    return;
  }
  qsa(".reveal--stagger").forEach((group) => {
    Array.from(group.children).forEach((child, i) => child.style.setProperty("--reveal-index", String(Math.min(i, 8))));
  });
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { rootMargin: "0px 0px -8% 0px", threshold: 0.08 }
  );
  targets.forEach((el) => observer.observe(el));
  // Safety net: anything still hidden after 2.5 s becomes visible (e.g. print, zoom).
  setTimeout(showAll, 2500);
  REDUCED_MOTION.addEventListener("change", () => REDUCED_MOTION.matches && showAll());
}

/* ------------------------------------------------------------------------ */
/* 7. Dialogs — the overlay system's (static/js/src/overlay.js, W2-A): the   */
/*    `initDialogs` of design V1 left this file with its last caller.        */
/* ------------------------------------------------------------------------ */

/* ------------------------------------------------------------------------ */
/* 8. Counters — count up once visible (optional; static value without JS)    */
/* ------------------------------------------------------------------------ */
function initCounters() {
  const counters = qsa("[data-counter]");
  if (!counters.length) return;
  const run = (el) => {
    const target = Number(el.dataset.counter);
    if (!Number.isFinite(target) || REDUCED_MOTION.matches) {
      el.textContent = el.dataset.counterFormat ? formatNumber(target) : String(target);
      return;
    }
    const duration = 900;
    const start = performance.now();
    const step = (now) => {
      const t = Math.min(1, (now - start) / duration);
      const eased = 1 - Math.pow(1 - t, 3);
      el.textContent = formatNumber(Math.round(target * eased));
      if (t < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  };
  const formatNumber = (n) => new Intl.NumberFormat(document.documentElement.lang || "fr").format(n);
  if (!("IntersectionObserver" in window)) {
    counters.forEach(run);
    return;
  }
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        run(entry.target);
        observer.unobserve(entry.target);
      }
    });
  });
  counters.forEach((el) => observer.observe(el));
}

/* ------------------------------------------------------------------------ */
/* 9. Misc: "back" links, current-year, forms double-submit guard           */
/* ------------------------------------------------------------------------ */
function initMisc() {
  qsa("[data-history-back]").forEach((el) => {
    el.addEventListener("click", (event) => {
      if (history.length > 1) {
        event.preventDefault();
        history.back();
      }
    });
  });
  // The double-submit guard (design V5, V5.4 plan §1.9, W1-D): the first submit goes through and the form
  // is marked `data-submitted`; a second one — Enter again, a second click — is refused until the answer
  // replaces the page. The button is `aria-disabled`, never `disabled`: the focus stays where the person left
  // it, and the busy key v5/loader.css draws on `.is-busy` (set by shell.js in the same task) turns on it.
  // loader.js lifts the mark when the wait ends without a new page — «Réessayer», the lease of 10 s, a submit
  // answered in the page; a page back from the cache is at rest again.
  qsa("form[data-single-submit]").forEach((form) => {
    form.addEventListener("submit", (event) => {
      if (form.hasAttribute("data-submitted")) {
        event.preventDefault();
        return;
      }
      form.setAttribute("data-submitted", "");
      qsa('button[type="submit"]', form).forEach((btn) => btn.setAttribute("aria-disabled", "true"));
    });
  });
  window.addEventListener("pageshow", (event) => {
    if (!event.persisted) return;
    qsa("form[data-single-submit][data-submitted]").forEach((form) => {
      form.removeAttribute("data-submitted");
      qsa('button[type="submit"]', form).forEach((btn) => btn.removeAttribute("aria-disabled"));
    });
  });
  // Section navigation: mark the link of the section currently in view
  const sectionNav = qs("[data-section-nav]");
  if (sectionNav && "IntersectionObserver" in window) {
    const links = qsa("a[href^='#']", sectionNav);
    const sections = links.map((a) => document.getElementById(a.getAttribute("href").slice(1))).filter(Boolean);
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          links.forEach((a) => {
            if (a.getAttribute("href") === `#${entry.target.id}`) a.setAttribute("aria-current", "true");
            else a.removeAttribute("aria-current");
          });
        });
      },
      { rootMargin: "-40% 0px -55% 0px" }
    );
    sections.forEach((s) => observer.observe(s));
  }
}

/* ------------------------------------------------------------------------ */
function init() {
  initFormErrorFocus();
  initDropdowns();
  initAccordions();
  initTabs();
  initSteppers();
  initReveal();
  initCounters();
  initMisc();
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", init, { once: true });
} else {
  init();
}

export { init };
