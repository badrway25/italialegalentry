/**
 * «The rise» — the public pages' section and row reveals in TIME, not in scroll (V5.15 §6; DECISIONS §15 lane A;
 * v515-a review round 2, M-3). Loaded by templates/base.html on the public pages only (the console's base empties the
 * block): a page-only module, nothing in the shared bundle.
 *
 * Why not `animation-timeline: view()` any more: a scroll-linked rise moves only while the page moves — it finished
 * off-screen, and the filmed home scroll showed the same frame at 140 and 640 ms. Here a block below the fold is held
 * 18 px low and transparent until it enters (IntersectionObserver), then it RISES over 420 ms by itself, the blocks
 * that enter together 40 ms apart, once.
 *
 * WHAT RISES: a chapter's head, statement and prose; the rows of the lists the pages draw (the registers, the trust
 * statements, the pathways, the Forum's programme, the FAQ's questions, the glossary's entries, the living topics, the
 * pages' link lists) and the children of lane C's `[data-motion="rise"]` blocks. A pathway row and a programme row also
 * DRAW their rule in gold as they rise (the home's route, the Forum's timeline: v5/_reveal.css).
 *
 * NEVER HIDDEN: anything in view (or above it) when the page is drawn — a reader never waits for what they are looking
 * at, and the LCP is never held; anything inside the page head or the home's hero (their own sequence); everything
 * under reduced motion, under the preview's html.rm, from the keyboard (R-07: the keyboard never animates — a focus
 * inside a held block shows it at once), without IntersectionObserver, without script, in print.
 *
 * V5.22 — THE SECTION RUNTIME (SECTION_SYSTEM_V2 §2.0, lane S). The rise above stays for the rows of plain lists and the
 * pages not recomposed yet (S-close removes it); a V2 section ([data-sec]) is signed by its pattern's own verbs
 * (v5/_reveal.css «Motion Density V2»). The contract:
 *   - at load, a [data-sec] section that starts below 92 % of the viewport gets data-sec-state="wait"; once a quarter of
 *     it shows (or a quarter of the viewport, for a section taller than four viewports) it gets "in", once; a section
 *     in view at load is never held — it is drawn at rest;
 *   - reduced motion, html.rm, the keyboard, no IntersectionObserver, no script: no state is ever written, and the
 *     section stands as its designed still; a focus, a find (hashchange) or a print shows a held section at once;
 *   - the interactive modules of the library (static/js/src/sezioni/, split chunks, never entries) load through
 *     import() only when a [data-sec-js~="<name>"] asks for them — whatever the motion setting: a tab is a tab;
 *   - no scroll listener; every observer is disconnected once its sections are released.
 */
import { reducedMotion } from "./motion.js";

const root = document.documentElement;

const GROUPS = [
  ".registro:not(.spazi)",
  ".register",
  ".home-trust__list",
  ".pathway-list",
  ".forum-programme",
  ".page-links",
  ".accordion",
  ".glossary__list",
  "[data-motion='rise']",
].join(",");
const SINGLES = "main :is(.chapter__head, .chapter__statement, .chapter__prose, .home-section__more)";
const OWN_SEQUENCE = ".page-header, .ingresso, .he, [data-stagger], dialog, [hidden]";
/** The blocks of one batch, 40 ms apart; the ninth and later share the eighth's delay. */
const MAX_STEP = 8;

const calm = () =>
  root.classList.contains("rm") ||
  root.dataset.input === "key" ||
  !("IntersectionObserver" in window) ||
  reducedMotion();

const order = (a, b) => (a.target.compareDocumentPosition(b.target) & Node.DOCUMENT_POSITION_FOLLOWING ? -1 : 1);

function show(element) {
  element.dataset.rise = "in";
}

export function initRise() {
  if (calm()) return;
  const items = new Set();
  document.querySelectorAll(GROUPS).forEach((group) => {
    for (const child of group.children) items.add(child);
  });
  document.querySelectorAll(SINGLES).forEach((element) => items.add(element));
  const fold = window.innerHeight * 0.92;
  // read every place first, then write: one layout, one style pass
  const held = [...items].filter((element) => {
    if (element.closest(OWN_SEQUENCE)) return false;
    const box = element.getBoundingClientRect();
    return box.height > 0 && box.top >= fold;
  });
  if (!held.length) return;
  held.forEach((element) => {
    element.dataset.rise = "";
  });
  const observer = new IntersectionObserver(
    (entries) => {
      let step = 0;
      entries
        .filter((entry) => entry.isIntersecting)
        .sort(order)
        .forEach((entry) => {
          entry.target.style.setProperty("--rise-k", String(Math.min(step++, MAX_STEP - 1)));
          show(entry.target);
          observer.unobserve(entry.target);
        });
    },
    { rootMargin: "0px 0px -8% 0px" },
  );
  held.forEach((element) => observer.observe(element));
  // the keyboard, a find, a jump: whatever is reached is there at once
  document.addEventListener("focusin", (event) => {
    const block = event.target instanceof Element && event.target.closest("[data-rise='']");
    if (block) show(block);
  });
  window.addEventListener("hashchange", () => held.forEach(show), { once: true });
}

const MODULES = {
  indice: () => import("./sezioni/indice.js"),
  mappa: () => import("./sezioni/mappa.js"),
  flow: () => import("./sezioni/flow.js"),
  spia: () => import("./sezioni/spia.js"),
  racconto: () => import("./sezioni/racconto.js"),
};

export function loadModules() {
  const names = new Set();
  document.querySelectorAll("[data-sec-js]").forEach((el) =>
    el.dataset.secJs.split(/\s+/).forEach((name) => MODULES[name] && names.add(name)),
  );
  names.forEach((name) =>
    MODULES[name]()
      .then((module) => module.default())
      .catch(() => {}),
  );
}

const STEPS = [0, 0.05, 0.1, 0.15, 0.2, 0.25];

export function initSections() {
  if (calm()) return;
  const fold = window.innerHeight * 0.92;
  const held = [...document.querySelectorAll("[data-sec]")].filter((section) => {
    const box = section.getBoundingClientRect();
    return box.height > 0 && box.top >= fold;
  });
  if (!held.length) return;
  held.forEach((section) => {
    section.dataset.secState = "wait";
  });
  let left = held.length;
  const release = (section) => {
    if (section.dataset.secState !== "wait") return;
    section.dataset.secState = "in";
    observer.unobserve(section);
    if (!--left) observer.disconnect();
  };
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        const tall = entry.boundingClientRect.height > window.innerHeight * 4;
        if (entry.isIntersecting && (entry.intersectionRatio >= 0.25 || (tall && entry.intersectionRect.height >= window.innerHeight * 0.25))) {
          release(entry.target);
        }
      });
    },
    { threshold: STEPS },
  );
  held.forEach((section) => observer.observe(section));
  const all = () => held.forEach(release);
  document.addEventListener("focusin", (event) => {
    const section = event.target instanceof Element && event.target.closest("[data-sec-state='wait']");
    if (section) release(section);
  });
  window.addEventListener("hashchange", all, { once: true });
  window.addEventListener("beforeprint", all, { once: true });
}

initRise();
initSections();
loadModules();
