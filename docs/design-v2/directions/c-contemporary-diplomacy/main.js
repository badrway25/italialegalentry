/**
 * DIRECTION C — Euro-Mediterranean / Contemporary Diplomacy · prototype behaviour.
 *
 * Every animation is declared with its function, its trigger, its duration and its reduced-motion
 * state (via withMotion: the settle branch is always the same final state). Only transform, opacity
 * and stroke-dashoffset are animated. Loops are ≥ 20 s, pausable, and pause offscreen / hidden tab.
 */
import { animate, scroll, inView, stagger, withMotion } from "/static/js/dist/motion.js";

const EASE_OUT = [0.25, 1, 0.5, 1];
const D = { fast: 0.12, base: 0.18, slow: 0.24, reveal: 0.32, draw: 0.9, tide: 28 };

const root = document.documentElement;
root.classList.add("js");

/* 0. Prototype-only: `?dir=rtl` mirrors the page to review the Arabic composition. */
const params = new URLSearchParams(location.search);
if (params.get("dir") === "rtl") { root.dir = "rtl"; root.lang = "ar"; }

/* 1. Header: hairline + translucent midnight once the page has scrolled (function: orientation). */
const header = document.querySelector(".site-header");
if (header) {
  const sentinel = document.createElement("div");
  sentinel.setAttribute("aria-hidden", "true");
  sentinel.className = "header-sentinel";
  header.before(sentinel);
  new IntersectionObserver(([e]) => header.classList.toggle("is-scrolled", !e.isIntersecting), { rootMargin: "-1px 0px 0px 0px" }).observe(sentinel);
}

/* 2. Mobile navigation drawer (no animation on repeated keyboard use beyond the panel itself). */
const toggle = document.querySelector("[data-nav-toggle]");
const drawer = document.querySelector("[data-nav-drawer]");
if (toggle && drawer) {
  const setOpen = (open) => {
    toggle.setAttribute("aria-expanded", String(open));
    drawer.classList.toggle("is-open", open);
    if (open) drawer.querySelector("a")?.focus({ preventScroll: true });
  };
  toggle.addEventListener("click", () => setOpen(toggle.getAttribute("aria-expanded") !== "true"));
  document.addEventListener("keydown", (e) => { if (e.key === "Escape" && drawer.classList.contains("is-open")) { setOpen(false); toggle.focus(); } });
  drawer.addEventListener("click", (e) => { if (e.target.closest("a")) setOpen(false); });
}

/* 3. Section reveal — "documents placed on the table" (function: hierarchy / causality).
      Trigger: enters viewport at 88 %. 320 ms, easeOutQuart, from 10 px above at 101.2 % — a sheet laid down. Siblings stagger 60 ms. */
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
    inView(els[0], () => {
      const pending = els.filter((el) => !el.classList.contains("is-in"));
      pending.forEach((el) => el.classList.add("is-in"));
      animate(pending, { opacity: [0, 1], y: [-10, 0], scale: [1.012, 1] }, { duration: D.reveal, ease: EASE_OUT, delay: stagger(0.06) });
    }, { margin: "0px 0px -12% 0px" });
    // A late element in a long group (below the first one's viewport) gets its own trigger.
    els.slice(1).forEach((el) => inView(el, () => {
      if (el.classList.contains("is-in")) return;
      el.classList.add("is-in");
      animate(el, { opacity: [0, 1], y: [-10, 0], scale: [1.012, 1] }, { duration: D.reveal, ease: EASE_OUT });
    }, { margin: "0px 0px -8% 0px" }));
  }
}, settleAll);

/* 4. HERO — title reveal line by line, territory draws, tide ambient (pausable). */
const heroTitle = document.querySelector("[data-hero-title]");
const territory = document.querySelector("[data-territory]");
if (heroTitle) {
  const lines = heroTitle.querySelectorAll(".line > span");
  withMotion(() => {
    heroTitle.classList.add("is-in");
    animate(lines, { y: ["110%", "0%"] }, { duration: 0.6, ease: EASE_OUT, delay: stagger(0.08, { startDelay: 0.1 }) });
  }, () => heroTitle.classList.add("is-in"));
}
if (territory) {
  const route = territory.querySelector(".terr__route");
  const stations = territory.querySelectorAll(".terr__station");
  const layers = territory.querySelectorAll("[data-tide]");
  const tideButton = document.querySelector("[data-tide-toggle]");
  const tideLabel = document.querySelector("[data-tide-label]");
  let tides = [];
  let userPaused = false;
  let visible = true;

  const syncTide = () => {
    const shouldPlay = visible && !userPaused && document.visibilityState !== "hidden";
    tides.forEach((c) => (shouldPlay ? c.play() : c.pause()));
  };

  withMotion(() => {
    // Territorial lines draw and settle (function: orientation — the two shores and the route).
    territory.dataset.drawn = "true";
    if (route) animate(route, { strokeDashoffset: [1, 0] }, { duration: D.draw, ease: EASE_OUT, delay: 0.35 });
    animate(stations, { opacity: [0, 1], scale: [0.4, 1] }, { duration: D.slow, ease: EASE_OUT, delay: stagger(0.12, { startDelay: 0.5 }) });
    stations.forEach((s) => s.classList.add("is-in"));
    // Tide: three contour layers drift at their own depth. 28 s, linear alternate, transform only.
    tides = [...layers].map((layer, i) => animate(layer, { x: [0, (i % 2 ? 1 : -1) * (12 - i * 3)], y: [0, -(6 - i * 1.5)] }, { duration: D.tide + i * 6, ease: "linear", repeat: Infinity, repeatType: "reverse" }));
    new IntersectionObserver(([e]) => { visible = e.isIntersecting; syncTide(); }, { threshold: 0.05 }).observe(territory);
    document.addEventListener("visibilitychange", syncTide);
    if (tideButton) {
      tideButton.addEventListener("click", () => {
        userPaused = !userPaused;
        tideButton.setAttribute("aria-pressed", String(userPaused));
        if (tideLabel) tideLabel.textContent = userPaused ? "Reprendre le mouvement" : "Suspendre le mouvement";
        syncTide();
      });
    }
  }, () => {
    territory.dataset.drawn = "true";
    territory.classList.add("is-static");
    if (tideButton) tideButton.dataset.static = "true"; // nothing moves: the control has no job
  });
}

/* 4b. THE DOORWAY — pathway → connection → advancement. The arch traces itself (900 ms), the three
      steps are laid down from the widest, the key (visible from first paint) settles and then breathes
      (6 s, transform + opacity on a pre-rendered glow layer — no filter loops). Scroll: the photograph
      moves 18 px over the whole hero, nothing else. Reduced motion: complete and still. */
const doorway = document.querySelector("[data-doorway]");
if (doorway) {
  const trace = doorway.querySelector(".doorway__trace path");
  const steps = doorway.querySelectorAll(".doorway__steps span");
  const key = doorway.querySelector("[data-doorway-key]");
  const glow = doorway.querySelector("[data-doorway-glow]");
  const photo = doorway.querySelector("[data-doorway-photo]");
  const hero = document.querySelector(".hero");
  withMotion(() => {
    doorway.classList.add("is-in");
    if (trace) animate(trace, { strokeDashoffset: [1, 0] }, { duration: D.draw, ease: EASE_OUT, delay: 0.15 });
    animate(steps, { scaleX: [0, 1] }, { duration: D.reveal, ease: EASE_OUT, delay: stagger(0.1, { startDelay: 0.55, from: "last" }) });
    // The inner arch and the key are visible from first paint (never opacity 0): the key only settles by 8 px, then breathes.
    if (key) {
      animate(key, { y: [8, 0] }, { duration: 0.5, ease: EASE_OUT, delay: 0.9 }).then(() => {
        animate(key, { y: [0, -6] }, { duration: 6, ease: "easeInOut", repeat: Infinity, repeatType: "reverse" });
      });
    }
    if (glow) animate(glow, { opacity: [0.45, 0.9], scale: [0.96, 1.04] }, { duration: 6, ease: "easeInOut", repeat: Infinity, repeatType: "reverse", delay: 1.2 });
    if (photo && hero) scroll(animate(photo, { y: [6, -12], scale: [1.06, 1.06] }, { ease: "linear" }), { target: hero, offset: ["start start", "end start"] });
  }, () => doorway.classList.add("is-in"));
}

/* 5. PROCESS — the route draws with the scroll (ScrollTimeline via Motion scroll()), stations settle. */
const routeSvg = document.querySelector("[data-route-svg]");
const routeMap = document.querySelector("[data-route-map]");
if (routeSvg && routeMap) {
  const line = routeSvg.querySelector(".route-line");
  withMotion(() => {
    routeSvg.dataset.drawn = "true";
    if (line) scroll(animate(line, { strokeDashoffset: [1, 0] }, { ease: "linear" }), { target: routeMap, offset: ["start 85%", "end 70%"] });
  }, () => { routeSvg.dataset.drawn = "true"; });
}

/* 6. PLATFORM — the current-step marker settles once (function: state), rows are revealed by §3. */
const marker = document.querySelector("[data-rail-marker]");
if (marker) {
  withMotion(() => {
    animate(marker, { scale: [0.5, 1], opacity: [0, 1] }, { duration: D.slow, ease: EASE_OUT, delay: 0.3 });
  }, null);
}
