/* ITALY LEGAL ENTRY™ — Direction B · architectural depth
   One module for both prototype pages. Every animation goes through withMotion(): the
   first argument animates, the second settles the same final state without motion.
   Only transform and opacity move; SVG strokes move by dashoffset (composited). */
import { animate, scroll, inView, stagger, withMotion } from "/static/js/dist/motion.js";

const EASE_IN = [0.25, 1, 0.5, 1];   // entry — easeOutQuart
const EASE_OUT = [0.7, 0, 0.3, 1];   // exit
const D = { fast: 0.12, base: 0.18, reveal: 0.24, plate: 0.32, trace: 0.96 }; // trace: immersive only

const root = document.documentElement;
const $ = (sel, scope = document) => scope.querySelector(sel);
const $$ = (sel, scope = document) => Array.from(scope.querySelectorAll(sel));

function settle(nodes) {
  for (const n of nodes) n.classList.add("is-settled");
}
function after(controls, cb, fallbackMs = 600) {
  if (controls && controls.finished && typeof controls.finished.then === "function") {
    controls.finished.then(cb, cb);
  } else if (controls && typeof controls.then === "function") {
    controls.then(cb, cb);
  } else {
    setTimeout(cb, fallbackMs);
  }
}

/* ---------- 1. Public header: floating plane + reading hairline ---------- */
function header() {
  const h = $("[data-header]");
  if (!h) return;
  let queued = false;
  const update = () => {
    queued = false;
    if (window.scrollY > 8) h.setAttribute("data-floating", "");
    else h.removeAttribute("data-floating");
  };
  addEventListener("scroll", () => {
    if (!queued) { queued = true; requestAnimationFrame(update); }
  }, { passive: true });
  update();

  const bar = $("[data-progress]", h);
  if (bar) {
    withMotion(
      () => scroll((p) => bar.style.setProperty("--p", p.toFixed(4))),
      () => bar.style.setProperty("--p", "0"),
    );
  }
}

/* ---------- 2. Mobile drawer: a threshold that opens ---------- */
function drawer() {
  const h = $("[data-header]");
  const btn = $("[data-nav-toggle]");
  const panel = $("[data-nav-drawer]");
  if (!h || !btn || !panel) return;

  // The header sits under the utility bar until the page scrolls: the drawer starts where the
  // header actually ends, not at a fixed height.
  const place = () => panel.style.setProperty("--drawer-top", Math.max(0, h.getBoundingClientRect().bottom) + "px");
  addEventListener("resize", () => { if (!panel.hidden) place(); });

  const setOpen = (open) => {
    btn.setAttribute("aria-expanded", String(open));
    h.toggleAttribute("data-open", open);
    root.classList.toggle("drawer-open", open);
    if (open) {
      place();
      panel.hidden = false;
      withMotion(
        () => animate(panel, { opacity: [0, 1], y: [-8, 0] }, { duration: D.reveal, ease: EASE_IN }),
        null,
      );
      const first = $("a, button", panel);
      if (first) first.focus({ preventScroll: true });
    } else {
      const hide = () => { panel.hidden = true; };
      const ctrl = withMotion(
        () => animate(panel, { opacity: [1, 0], y: [0, -8] }, { duration: D.base, ease: EASE_OUT }),
        hide,
      );
      if (ctrl) after(ctrl, hide, 200);
    }
  };

  btn.addEventListener("click", () => setOpen(btn.getAttribute("aria-expanded") !== "true"));
  panel.addEventListener("keydown", (e) => {
    if (e.key === "Escape") { setOpen(false); btn.focus(); }
  });
  btn.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && btn.getAttribute("aria-expanded") === "true") setOpen(false);
  });
  const mq = matchMedia("(min-width: 1101px)");
  mq.addEventListener("change", () => { if (mq.matches && !panel.hidden) setOpen(false); });
}

/* ---------- 3. Hero: the title reveals, the doorway builds itself ---------- */
/* Sequence (immersive chapter, the one place a trace may exceed 320 ms):
   plane into register → arch outlines traced → threshold lit (photograph) → inner arch rises →
   key rises out of the steps under its glow → the three steps build outward → caption.
   Every step is a class; CSS transitions on transform/opacity/dashoffset do the work, so the
   sequence is cheap, interruptible, and identical in its final state to the reduced-motion page. */
function hero() {
  const el = $("[data-hero]");
  if (!el) return;
  const lines = $$(".title__line > span", el);
  const reveals = $$("[data-reveal]", el);
  const portal = $("[data-portal]", el);

  const finish = () => {
    settle(lines.map((s) => s.parentElement));
    settle(reveals);
    if (portal) portal.classList.add("is-planed", "is-traced", "is-lit", "is-open", "is-keyed", "is-stepped", "is-built");
    el.classList.add("is-settled");
  };

  withMotion(() => {
    animate(lines, { transform: ["translateY(105%)", "translateY(0%)"] },
      { duration: D.plate, delay: stagger(0.07), ease: EASE_IN });
    animate(reveals, { opacity: [0, 1], y: [12, 0] },
      { duration: D.reveal, delay: stagger(0.06, { startDelay: 0.16 }), ease: EASE_IN });
    if (portal) {
      const step = (cls, ms) => setTimeout(() => portal.classList.add(cls), ms);
      step("is-planed", 120);
      step("is-traced", 260);
      step("is-lit", 980);
      step("is-open", 1180);
      step("is-keyed", 1420);
      step("is-stepped", 1560);
      setTimeout(finish, 2000);
    } else {
      setTimeout(finish, 900);
    }
    return null;
  }, finish);

  // Scroll-linked, extremely controlled: the photograph and the key drift a few pixels against
  // the arch while the hero leaves the viewport (pathway → advancement). Wide layout only.
  if (portal && matchMedia("(min-width: 1025px)").matches) {
    const img = $(".arch__img", portal);
    const key = $(".arch__key", portal);
    withMotion(() => {
      if (img) scroll(animate(img, { y: [0, 26] }, { ease: "linear" }), { target: el, offset: ["start start", "end start"] });
      if (key) scroll(animate(key, { y: [0, -14] }, { ease: "linear" }), { target: el, offset: ["start start", "end start"] });
    }, null);
  }
}

/* ---------- 4. Generic reveal groups (threshold band, section heads, CTA) ---------- */
function revealGroups() {
  const groups = $$("[data-reveal-group]");
  for (const g of groups) {
    const items = $$("[data-reveal]", g);
    if (!items.length) continue;
    withMotion(() => {
      inView(g, () => {
        const ctrl = animate(items, { opacity: [0, 1], y: [16, 0] },
          { duration: D.reveal, delay: stagger(0.06), ease: EASE_IN });
        after(ctrl, () => settle(items));
      }, { amount: 0.2 });
    }, () => settle(items));
  }
}

/* ---------- 5. The four thresholds ---------- */
function thresholds() {
  const list = $("[data-seuils]");
  if (!list) return;
  const items = $$(".seuil", list);
  withMotion(() => {
    inView(list, () => {
      const ctrl = animate(items, { opacity: [0, 1], y: [24, 0] },
        { duration: D.plate, delay: stagger(0.07), ease: EASE_IN });
      after(ctrl, () => settle(items));
    }, { amount: 0.15 });
  }, () => settle(items));
}

/* ---------- 6. Process chamber: pinned section, chapters light the floors ---------- */
function process() {
  const section = $("[data-process]");
  if (!section) return;
  const chapters = $$(".chapter", section);
  const route = $(".drawing--process .route", section);

  // Chapter → active floor. inView (IntersectionObserver) — scroll stays 1:1, nothing is pinned by JS.
  for (const ch of chapters) {
    inView(ch, () => {
      section.dataset.active = ch.dataset.stage;
      for (const c of chapters) {
        const on = c === ch;
        c.classList.toggle("is-active", on);
        if (on) c.setAttribute("aria-current", "step"); else c.removeAttribute("aria-current");
      }
    }, { amount: 0.4, margin: "-12% 0px -38% 0px" });
  }

  // Route trace is scroll-linked (ScrollTimeline via Motion scroll()), only on the wide layout
  // where the drawing is actually pinned beside the chapters.
  const wide = matchMedia("(min-width: 1024px)");
  if (route && wide.matches) {
    const list = $("[data-chapters]", section);
    withMotion(() => {
      scroll(animate(route, { strokeDashoffset: [1, 0] }, { ease: "linear" }),
        { target: list, offset: ["start 62%", "end 62%"] });
    }, () => route.classList.add("is-drawn"));
  } else if (route) {
    route.classList.add("is-drawn");
  }
}

/* ---------- 7. Platform: plates into register, rail marker ---------- */
function platform() {
  const groups = $$("[data-plates]");
  if (!groups.length) return;
  for (const g of groups) {
    const plates = $$("[data-plate]", g);
    withMotion(() => {
      const ctrl = animate(plates, { opacity: [0, 1], y: [8, 0] },
        { duration: D.reveal, delay: stagger(0.04), ease: EASE_IN });
      after(ctrl, () => settle(plates));
    }, () => settle(plates));
  }
  const rail = $("[data-rail]");
  if (rail) {
    withMotion(() => setTimeout(() => rail.classList.add("is-marked"), 240),
      () => rail.classList.add("is-marked"));
  }
}

/* ---------- 8. Dropdowns built on <details> ---------- */
function dropdowns() {
  const all = $$("details[data-dropdown]");
  for (const d of all) {
    d.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && d.open) { d.open = false; const s = $("summary", d); if (s) s.focus(); }
    });
    d.addEventListener("focusout", (e) => {
      if (d.open && !d.contains(e.relatedTarget)) d.open = false;
    });
  }
  document.addEventListener("click", (e) => {
    for (const d of all) if (d.open && !d.contains(e.target)) d.open = false;
  });
}

/* ---------- boot ---------- */
try {
  header();
  drawer();
  hero();
  revealGroups();
  thresholds();
  process();
  platform();
  dropdowns();
} catch (err) {
  // Whatever failed, the page must never stay half-hidden.
  root.classList.add("motion-failed");
  console.error(err);
}
// Belt and braces: nothing waits on an animation forever.
setTimeout(() => {
  settle($$("[data-reveal], [data-plate], .seuil, .title__line"));
  root.classList.add("motion-done");
}, 4000);
