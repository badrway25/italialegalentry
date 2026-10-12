/**
 * Direction A · "Rete luminosa" — motion and shell behaviour.
 *
 * One import, from the project's Motion bundle. Every animation is wrapped in withMotion():
 * the first argument runs when motion is welcome, the second settles the identical final state
 * when the person asked for reduced motion. CSS only hides initial states under `.motion-ok`,
 * so without JS, or with reduced motion, every page is complete and static.
 *
 * Curves: entry cubic-bezier(.25,1,.5,1); durations from {120, 180, 240, 320} ms, plus the
 * immersive hero draw (1200 ms) and two ambient loops (24 s packet, 3.2 s hub ring) that only
 * exist inside the hero chapter.
 */
import { animate, scroll, inView, stagger, withMotion } from "/static/js/dist/motion.js";

const root = document.documentElement;
const EASE = [0.25, 1, 0.5, 1];
const reduced = typeof matchMedia === "function" && matchMedia("(prefers-reduced-motion: reduce)").matches;
root.classList.add(reduced ? "motion-reduced" : "motion-ok");

/* ---------- public header: compact on scroll, reading progress, drawer, panels ---------- */
function header() {
  const h = document.querySelector("[data-header]");
  if (!h) return;
  let frame = 0;
  const update = () => { h.classList.toggle("is-scrolled", window.scrollY > 8); frame = 0; };
  addEventListener("scroll", () => { if (!frame) frame = requestAnimationFrame(update); }, { passive: true });
  update();

  const bar = h.querySelector("[data-progress]");
  if (bar) {
    withMotion(
      () => scroll(animate(bar, { transform: ["scaleX(0)", "scaleX(1)"] }, { ease: "linear" })),
      () => { bar.hidden = true; },
    );
  }

  const toggle = document.querySelector("[data-nav-toggle]");
  const nav = document.querySelector("[data-nav]");
  if (toggle && nav) {
    const setOpen = (open) => {
      nav.classList.toggle("is-open", open);
      toggle.setAttribute("aria-expanded", String(open));
      document.body.style.overflow = open ? "hidden" : "";
    };
    toggle.addEventListener("click", () => setOpen(!nav.classList.contains("is-open")));
    addEventListener("keydown", (e) => { if (e.key === "Escape" && nav.classList.contains("is-open")) { setOpen(false); toggle.focus(); } });
    matchMedia("(min-width: 1280px)").addEventListener("change", (e) => { if (e.matches) setOpen(false); });
  }

  const items = [...document.querySelectorAll("[data-nav-item]")];
  const closeAll = (except) => items.forEach((it) => {
    if (it === except) return;
    it.classList.remove("is-open");
    it.querySelector("[data-nav-panel-toggle]")?.setAttribute("aria-expanded", "false");
  });
  items.forEach((it) => {
    const btn = it.querySelector("[data-nav-panel-toggle]");
    btn?.addEventListener("click", () => {
      const open = !it.classList.contains("is-open");
      closeAll(it);
      it.classList.toggle("is-open", open);
      btn.setAttribute("aria-expanded", String(open));
    });
    it.addEventListener("keydown", (e) => { if (e.key === "Escape" && it.classList.contains("is-open")) { closeAll(); btn?.focus(); } });
  });
  document.addEventListener("click", (e) => { if (!e.target.closest("[data-nav-item]")) closeAll(); });
}

/* ---------- reveals: inView, one entry curve, stagger 50 ms ---------- */
function reveals() {
  const singles = [...document.querySelectorAll("[data-reveal]")];
  const groups = [...document.querySelectorAll("[data-reveal-children]")];
  const lines = [...document.querySelectorAll(".line")];
  withMotion(() => {
    singles.forEach((el) => inView(el, () => {
      animate(el, { opacity: [0, 1], transform: ["translateY(14px)", "translateY(0px)"] }, { duration: 0.32, ease: EASE });
    }, { margin: "0px 0px -8% 0px" }));
    groups.forEach((el) => inView(el, () => {
      animate([...el.children], { opacity: [0, 1], transform: ["translateY(14px)", "translateY(0px)"] }, { duration: 0.32, delay: stagger(0.05), ease: EASE });
    }, { margin: "0px 0px -8% 0px" }));
    if (lines.length) {
      animate(lines.map((l) => l.firstElementChild), { transform: ["translateY(110%)", "translateY(0%)"] }, { duration: 0.28, delay: stagger(0.05), ease: EASE });
    }
  }, () => {
    singles.forEach((el) => el.classList.add("is-settled"));
    groups.forEach((el) => el.classList.add("is-settled"));
    lines.forEach((el) => el.classList.add("is-settled"));
  });
}

/* ---------- hero: the doorway is complete from the first frame; the network converges on it ----------
   The owner's composition (photo, navy inner arch, gold key, three steps) is never withheld.
   What is choreographed on top of it: the arch stroke traced (the legal frame), a one-time
   glow on the key (the regular procedure), then the pathways drawing toward the door and the
   actors arriving. Reduced motion: everything complete and still. */
function hero() {
  const net = document.querySelector("[data-net]");
  const door = document.querySelector("[data-door]");
  if (!net || !door) return;
  const outline = [...door.querySelectorAll(".door__outline")];
  const glow = door.querySelector(".door__glow");
  const route = net.querySelector(".net__route");
  const edges = [...net.querySelectorAll(".net__edge")];
  const nodes = [...net.querySelectorAll(".net__node")];
  const labels = [...net.querySelectorAll(".net__label, .net__territory")];

  withMotion(async () => {
    // 1 · the doorway is already complete (photo, inner arch, key, steps at opacity 1 from the
    //     first frame); only its stroke is traced on top and the key glows once
    animate(outline, { strokeDashoffset: [1, 0] }, { duration: 0.9, delay: stagger(0.15, { startDelay: 0.1 }), ease: EASE });
    animate(glow, { opacity: [0.55, 1] }, { duration: 0.6, delay: 0.5, ease: EASE });
    // 2 · the network converges on it
    await animate(route, { strokeDashoffset: [1, 0] }, { duration: 1.2, delay: 0.5, ease: EASE }).finished;
    door.classList.add("is-open");
    animate(edges, { strokeDashoffset: [1, 0] }, { duration: 0.6, delay: stagger(0.035), ease: EASE });
    animate(nodes, { opacity: [0, 1], transform: ["scale(0.5)", "scale(1)"] }, { duration: 0.32, delay: stagger(0.04), ease: EASE });
    await animate(labels, { opacity: [0, 1] }, { duration: 0.24, delay: stagger(0.04, { startDelay: 0.25 }), ease: EASE }).finished;
    net.classList.add("is-drawn", "is-live");
    door.classList.add("is-live");
  }, () => { net.classList.add("is-drawn"); door.classList.add("is-open"); });

  // depth: three speeds — copy 1×, scene 0.9×, photograph inside the arch slower still
  const hero = net.closest(".hero");
  const scene = net.parentElement;
  const img = door.querySelector(".door__img");
  if (hero && scene && matchMedia("(min-width: 1024px)").matches) {
    withMotion(() => {
      scroll(animate(scene, { transform: ["translateY(0px)", "translateY(-40px)"] }, { ease: "linear" }), { target: hero, offset: ["start start", "end start"] });
      scroll(animate(img, { transform: ["translateY(0px)", "translateY(-22px)"] }, { ease: "linear" }), { target: hero, offset: ["start start", "end start"] });
    });
  }
}

/* ---------- process: scroll-linked path, stations light as the line reaches them ---------- */
function process() {
  const sec = document.querySelector("[data-proc]");
  if (!sec) return;
  const path = sec.querySelector(".proc__path");
  const spine = sec.querySelector(".proc__spine-fill");
  const stations = [...sec.querySelectorAll(".proc__station")];
  const dots = [...sec.querySelectorAll(".proc__dot")];
  const light = (p) => {
    const n = Math.min(stations.length, Math.floor(p * stations.length + 0.45));
    stations.forEach((s, i) => s.classList.toggle("is-lit", i < n));
    dots.forEach((d, i) => d.classList.toggle("is-lit", i < n));
  };
  const offset = ["start 0.85", "end 0.75"];
  withMotion(() => {
    scroll(animate(path, { strokeDashoffset: [1, 0] }, { ease: "linear" }), { target: sec, offset });
    if (spine) scroll(animate(spine, { transform: ["scaleY(0)", "scaleY(1)"] }, { ease: "linear" }), { target: sec, offset });
    scroll((progress) => light(progress), { target: sec, offset });
  }, () => { sec.classList.add("is-complete"); light(1); });
}

/* ---------- platform shell: collapsible rail ---------- */
function shell() {
  const app = document.querySelector("[data-app]");
  const btn = document.querySelector("[data-rail-toggle]");
  if (!app || !btn) return;
  btn.addEventListener("click", () => {
    const collapsed = app.classList.toggle("is-collapsed");
    btn.setAttribute("aria-expanded", String(!collapsed));
    btn.setAttribute("aria-label", collapsed ? "Développer la navigation" : "Réduire la navigation");
  });
  addEventListener("keydown", (e) => { if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "b") { e.preventDefault(); btn.click(); } });
}

header();
reveals();
hero();
process();
shell();
