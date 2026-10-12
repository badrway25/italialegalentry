/**
 * Italy Legal Entry™ — progressive enhancement (ES module, no framework, no external libs).
 *
 * Every behaviour here enhances markup that already works without JavaScript:
 *  - navigation drawer + accessible mega-menu (keyboard, Escape, aria-expanded)
 *  - details-based dropdowns (language switcher, account menu): Escape / outside click
 *  - accordion (exclusive mode), tabs (roving tabindex), stepper (client-side panels)
 *  - reveal-on-scroll (never hides content when JS is off; honours prefers-reduced-motion)
 *  - native <dialog> open/close with focus restore
 *  - optional count-up counters
 *
 * Conventions: behaviours are attached through data-* attributes; no inline handlers
 * (CSP: script-src 'self'); all text stays in the HTML (translatable server-side).
 */

const REDUCED_MOTION = window.matchMedia("(prefers-reduced-motion: reduce)");
// Navigation breakpoint — keep in sync with components.css §navigation (80rem).
const DESKTOP = window.matchMedia("(min-width: 80rem)");
const FOCUSABLE = 'a[href], button:not([disabled]), input:not([disabled]):not([type="hidden"]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])';

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
/* 1. Navigation: drawer (mobile) + mega-menu (desktop)                      */
/* ------------------------------------------------------------------------ */
function initNavigation() {
  const toggle = qs("[data-nav-toggle]");
  const drawer = qs("[data-nav-drawer]");
  const overlay = qs("[data-nav-overlay]");
  const items = qsa("[data-nav-item]");

  const closeAllPanels = (except = null) => {
    items.forEach((item) => {
      if (item === except) return;
      item.dataset.open = "false";
      const btn = qs("[data-nav-panel-toggle]", item);
      if (btn) btn.setAttribute("aria-expanded", "false");
    });
  };

  const openPanel = (item) => {
    closeAllPanels(item);
    item.dataset.open = "true";
    const btn = qs("[data-nav-panel-toggle]", item);
    if (btn) btn.setAttribute("aria-expanded", "true");
  };

  items.forEach((item) => {
    const btn = qs("[data-nav-panel-toggle]", item);
    if (!btn) return;
    btn.setAttribute("aria-expanded", "false");
    btn.addEventListener("click", () => {
      const isOpen = item.dataset.open === "true";
      if (isOpen) {
        closeAllPanels();
      } else {
        item.navOpener = btn;
        openPanel(item);
        const first = qs(FOCUSABLE, qs("[data-nav-panel]", item));
        if (first && DESKTOP.matches) first.focus();
      }
    });
    item.addEventListener("keydown", (event) => {
      // Inside an open panel the arrows keep working (gate A review, correction 7): Down/Up walk
      // the panel's links (Up from the first returns to the toggle), Left/Right leave for the
      // neighbouring section, as they do on the bar.
      // Only for a key pressed IN the panel: the bar's own ArrowDown bubbles here too, after it has
      // focused the panel's first link, and used to be handled twice — the first link was skipped
      // (gate A, round 4, defect 15).
      const panel = qs("[data-nav-panel]", item);
      if (item.dataset.open === "true" && panel && panel.contains(event.target)) {
        const links = qsa(FOCUSABLE, panel).filter((el) => el.offsetParent !== null);
        const at = links.indexOf(document.activeElement);
        const isRtl = document.documentElement.dir === "rtl";
        const step = event.key === (isRtl ? "ArrowLeft" : "ArrowRight") ? 1 : event.key === (isRtl ? "ArrowRight" : "ArrowLeft") ? -1 : 0;
        if (event.key === "ArrowDown" && at >= 0) {
          event.preventDefault();
          links[(at + 1) % links.length].focus();
          return;
        }
        if (event.key === "ArrowUp" && at >= 0) {
          event.preventDefault();
          // Up from the first link returns to the stop that opened the panel: the section's link
          // (ArrowDown on it) or its chevron (a click or Enter on it).
          (at === 0 ? item.navOpener || qs("[data-nav-link]", item) || btn : links[at - 1]).focus();
          return;
        }
        if (step && DESKTOP.matches) {
          event.preventDefault();
          // The same stops as the bar's arrows (below), sections without a panel included.
          const index = sections.findIndex((section) => section.li === item);
          const target = sections[(index + step + sections.length) % sections.length];
          closeAllPanels();
          (target.link || target.btn).focus();
          return;
        }
      }
      if (event.key === "Escape" && item.dataset.open === "true") {
        event.preventDefault();
        // Escape closes the INNERMOST open thing, and only that one. Without stopping the event
        // here it also reaches the drawer's handler on `document`, so one key press closed both
        // the section panel and the whole menu around it.
        event.stopPropagation();
        closeAllPanels();
        (item.navOpener || btn).focus();
      }
    });
    // Desktop: close when focus leaves the item
    item.addEventListener("focusout", (event) => {
      if (!DESKTOP.matches) return;
      if (!item.contains(event.relatedTarget)) closeAllPanels();
    });
  });

  // Arrow keys on the bar (desktop menubar behaviour). Every stop of a section — its link and its
  // chevron — answers them (the chevron was a dead end: → did nothing, ↓ scrolled the page; gate A,
  // round 4, defect 15): ←/→ go to the neighbouring section, ↓ opens the panel and enters it, and
  // no arrow scrolls the page while the focus is on the bar. Sections without a panel are stops too.
  const sections = qsa(".main-nav__list > .main-nav__item").map((li) => ({
    li,
    link: qs(":scope > [data-nav-link]", li),
    btn: qs(":scope > [data-nav-panel-toggle]", li),
  })).filter((section) => section.link || section.btn);
  sections.forEach((section, index) => {
    [section.link, section.btn].filter(Boolean).forEach((stop) => {
      stop.addEventListener("keydown", (event) => {
        if (!DESKTOP.matches) return;
        const isRtl = document.documentElement.dir === "rtl";
        const next = isRtl ? "ArrowLeft" : "ArrowRight";
        const prev = isRtl ? "ArrowRight" : "ArrowLeft";
        if (event.key === next || event.key === prev) {
          event.preventDefault();
          const step = event.key === next ? 1 : -1;
          const target = sections[(index + step + sections.length) % sections.length];
          (target.link || target.btn).focus();
        } else if (event.key === "ArrowDown" || event.key === "ArrowUp") {
          event.preventDefault();
          if (event.key !== "ArrowDown" || !section.btn) return;
          section.li.navOpener = stop;
          openPanel(section.li);
          const first = qsa(FOCUSABLE, qs("[data-nav-panel]", section.li)).find((el) => el.offsetParent !== null);
          if (first) first.focus();
        }
      });
    });
  });

  if (!toggle || !drawer) return;

  const header = qs("#site-header");
  // The drawer and its scrim are position:fixed: both start under the header's REAL bottom edge,
  // which moves with the utility bar (visible or scrolled away) and the scrolled header. The
  // property is set on the header so that both of its children inherit it (gate A, round 3: a
  // z-index inside the sticky header cannot put the scrim under the header's own content) — and
  // measured again whenever the viewport or the header changes while the drawer is open: rotating
  // a phone left the drawer over the lock-up, or a 41px band of page uncovered (round 4, 12).
  const placeDrawer = () => {
    if (!header) return;
    const bottom = Math.max(0, Math.round(header.getBoundingClientRect().bottom));
    header.style.setProperty("--nav-drawer-top", `${bottom}px`);
  };
  const isOpen = () => document.body.dataset.navOpen === "true";
  window.addEventListener("resize", () => { if (isOpen()) placeDrawer(); });
  if (header && "ResizeObserver" in window) new ResizeObserver(() => { if (isOpen()) placeDrawer(); }).observe(header);
  const setDrawer = (open) => {
    if (open) placeDrawer();
    document.body.dataset.navOpen = open ? "true" : "false";
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    if (open) {
      const first = qs(FOCUSABLE, drawer);
      if (first) first.focus();
    }
  };

  toggle.setAttribute("aria-expanded", "false");
  toggle.addEventListener("click", () => setDrawer(document.body.dataset.navOpen !== "true"));
  if (overlay) overlay.addEventListener("click", () => setDrawer(false));

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && document.body.dataset.navOpen === "true") {
      setDrawer(false);
      toggle.focus();
    }
  });

  // Keep focus inside the drawer while open on mobile (simple loop trap)
  drawer.addEventListener("keydown", (event) => {
    if (event.key !== "Tab" || DESKTOP.matches || document.body.dataset.navOpen !== "true") return;
    const focusables = qsa(FOCUSABLE, drawer).filter((el) => el.offsetParent !== null);
    if (!focusables.length) return;
    const first = focusables[0];
    const last = focusables[focusables.length - 1];
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      toggle.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      toggle.focus();
    }
  });

  DESKTOP.addEventListener("change", () => {
    setDrawer(false);
    closeAllPanels();
  });
}

/* ------------------------------------------------------------------------ */
/* 2. Details-based dropdowns (language switcher, account menu)              */
/* ------------------------------------------------------------------------ */
function initDropdowns() {
  const dropdowns = qsa("details[data-dropdown]");
  if (!dropdowns.length) return;

  const closeOthers = (current) => {
    dropdowns.forEach((d) => {
      if (d !== current) d.removeAttribute("open");
    });
  };

  dropdowns.forEach((details) => {
    const summary = qs("summary", details);
    details.addEventListener("toggle", () => {
      if (details.open) {
        closeOthers(details);
        summary?.setAttribute("aria-expanded", "true");
      } else {
        summary?.setAttribute("aria-expanded", "false");
      }
    });
    summary?.setAttribute("aria-expanded", details.open ? "true" : "false");
    details.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && details.open) {
        event.preventDefault();
        // Same rule as the navigation panels: close this dropdown and stop. The language switcher
        // now lives inside the drawer on a phone (design V2 §8.2), and without this line Escape
        // dismissed the language list AND the menu it was sitting in.
        event.stopPropagation();
        details.removeAttribute("open");
        summary?.focus();
      }
    });
    details.addEventListener("focusout", (event) => {
      if (!details.contains(event.relatedTarget)) details.removeAttribute("open");
    });
  });

  document.addEventListener("click", (event) => {
    dropdowns.forEach((d) => {
      if (d.open && !d.contains(event.target)) d.removeAttribute("open");
    });
  });
}

/* ------------------------------------------------------------------------ */
/* 3. Accordion — exclusive mode for browsers without <details name>         */
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
}

/* ------------------------------------------------------------------------ */
/* 4. Tabs — WAI-ARIA tabs with roving tabindex; stacked sections without JS */
/* ------------------------------------------------------------------------ */
function initTabs() {
  qsa("[data-tabs]").forEach((widget) => {
    const tabs = qsa("[role=tab]", widget);
    const panels = qsa("[role=tabpanel]", widget);
    if (!tabs.length || tabs.length !== panels.length) return;

    const activate = (index, focus = true) => {
      tabs.forEach((tab, i) => {
        const selected = i === index;
        tab.setAttribute("aria-selected", selected ? "true" : "false");
        tab.tabIndex = selected ? 0 : -1;
        panels[i].hidden = !selected;
        if (selected && focus) tab.focus();
      });
      try {
        if (widget.dataset.tabsRemember) localStorage.setItem(`tabs:${widget.dataset.tabsRemember}`, String(index));
      } catch (_) {
        /* storage unavailable */
      }
    };

    tabs.forEach((tab, index) => {
      tab.addEventListener("click", () => activate(index, false));
      tab.addEventListener("keydown", (event) => {
        const isRtl = document.documentElement.dir === "rtl";
        const next = isRtl ? "ArrowLeft" : "ArrowRight";
        const prev = isRtl ? "ArrowRight" : "ArrowLeft";
        let target = null;
        if (event.key === next) target = (index + 1) % tabs.length;
        else if (event.key === prev) target = (index - 1 + tabs.length) % tabs.length;
        else if (event.key === "Home") target = 0;
        else if (event.key === "End") target = tabs.length - 1;
        if (target !== null) {
          event.preventDefault();
          activate(target);
        }
      });
    });

    let initial = tabs.findIndex((t) => t.getAttribute("aria-selected") === "true");
    if (location.hash) {
      const byHash = panels.findIndex((p) => `#${p.id}` === location.hash);
      if (byHash >= 0) initial = byHash;
    }
    activate(initial >= 0 ? initial : 0, false);
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
/* 7. Dialog — native <dialog>; the platform traps focus and handles Escape  */
/* ------------------------------------------------------------------------ */
function initDialogs() {
  let opener = null;
  document.addEventListener("click", (event) => {
    const openBtn = event.target.closest("[data-dialog-open]");
    if (openBtn) {
      const id = openBtn.dataset.dialogOpen || (openBtn.getAttribute("href") || "").replace(/^#/, "");
      const dialog = id && document.getElementById(id);
      if (dialog && typeof dialog.showModal === "function") {
        event.preventDefault();
        opener = openBtn;
        dialog.showModal();
        const first = qs("[data-dialog-focus]", dialog) || qs(FOCUSABLE, dialog);
        if (first) first.focus();
      }
      return;
    }
    const closeBtn = event.target.closest("[data-dialog-close]");
    if (closeBtn) {
      const dialog = closeBtn.closest("dialog");
      if (dialog) {
        event.preventDefault();
        dialog.close();
      }
    }
  });
  qsa("dialog").forEach((dialog) => {
    dialog.addEventListener("close", () => {
      if (opener && document.contains(opener)) opener.focus();
      opener = null;
    });
    // Click on the backdrop closes (only when the click target is the dialog itself)
    dialog.addEventListener("click", (event) => {
      if (event.target === dialog && dialog.dataset.dialogLight !== undefined) dialog.close();
    });
  });
}

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
  qsa("form[data-single-submit]").forEach((form) => {
    form.addEventListener("submit", () => {
      qsa('button[type="submit"]', form).forEach((btn) => {
        btn.setAttribute("aria-disabled", "true");
        btn.disabled = true;
      });
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
  initNavigation();
  initDropdowns();
  initAccordions();
  initTabs();
  initSteppers();
  initReveal();
  initDialogs();
  initCounters();
  initMisc();
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", init, { once: true });
} else {
  init();
}

export { init };
