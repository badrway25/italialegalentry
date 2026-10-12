/**
 * The home hero, design V4 (docs/design-v4/CREATIVE_DIRECTION.md §3.1, §4): the legend rows light
 * their route, the current along the routes pauses off screen, the photograph drifts with the
 * scroll and the stage settles as the chapter leaves.
 *
 * Everything the person needs is complete on the first frame — door, key, steps, routes, exits,
 * legend, title — and NOTHING that has been painted is taken away again. This module is deferred:
 * it runs after the first paint (≈ 3 s later on slow 4G), so an entrance animated from here starts
 * from a state other than the painted one and hides what the person has already seen. Two did:
 * the title's line reveal (gate A round 3, defect 7) and the stage's choreography — arch trace,
 * routes drawn, nodes and exits faded in, steps and key settling (round 4, defect 11: routes,
 * nodes and exit words hidden for 1.6 s on slow 4G). Both are gone: a deviation from CD §3.1 and
 * §4 for the CD to sign (docs/design-v4/README.md §4.8). What moves is the current, from the first
 * frame (CSS), and the scroll-linked pair, whose state at scroll 0 IS the painted state.
 *
 * Function of each animation, per DESIGN_SYSTEM_V4.md §7.1:
 *   current along routes   ambient       CSS, 28s, paused off screen (hero.css reads .is-offscreen)
 *   legend → route         hover         120ms in / 120ms out (hero.css); here only the state
 *   photograph on scroll   scroll-linked 18px over the hero, WAAPI + ScrollTimeline
 *   stage on scroll        scroll-linked scale .96, opacity .6 as the hero leaves
 *
 * The routes are re-anchored to the real position of their legend row (§4.2: «callouts anchored
 * by construction»): the row's node disc is where the route starts. The path in the markup is the
 * no-JavaScript drawing; this file replaces it with one measured at every width.
 */
import { animate, scroll, withMotion } from "./motion.js";

const COMPACT = window.matchMedia("(max-width: 63.999rem)");
// The exits are drawn from 80rem (hero.css); below it a route ends where the drawing ends — it
// dissolves into the navy at the arch's edge instead of running to an exit that is not there
// (round-4 review, defect 13b).
const WIDE = window.matchMedia("(min-width: 80rem)");

/* The stage geometry (viewBox 640×520, the same numbers as pages.services): the inner arch's
   solid navy spans x 365–531 and its lower part, under the key, is where the four routes braid
   through; the exits, when the eyebrow names them, sit at x 624. */
const STAGE = { width: 640, height: 520, braidStart: 365, braidEnd: 531, braidY: 372, braidGap: 6, riseStart: 496, riseEnd: 520, exitX: 624 };
const EXIT_Y = { 1: 200, 2: 300, 3: 400 };
const COMPACT_VIEWBOX = "264 64 368 456"; // the arch alone, with a margin of 24

/**
 * One route: from its origin, a curve into the braid, then the braid — where the stroke dissolves
 * into the navy — or, with named exits, a curve out to the exit. `i` is the route's rank (0–3),
 * which sets its lane in the braid.
 */
function routePath(x0, y0, i, exitY, withExits) {
  // The braid: the lane a route enters the arch on is not the one it leaves on — the four cross
  // in the middle of the navy (lane i → lane 3 − i), which is what makes them a braid rather
  // than four stripes (review, correction 4). The same numbers as pages.services._route_path.
  const yIn = STAGE.braidY + i * STAGE.braidGap;
  const yOut = STAGE.braidY + (3 - i) * STAGE.braidGap;
  const c1 = Math.round(x0 + (STAGE.braidStart - x0) * 0.55);
  const start = `M${x0} ${y0} C${c1} ${y0}, ${STAGE.braidStart - 40} ${yIn}, ${STAGE.braidStart} ${yIn}`;
  if (!withExits) {
    const mid = Math.round((STAGE.braidStart + STAGE.braidEnd) / 2);
    return `${start} C${mid} ${yIn}, ${mid} ${yOut}, ${STAGE.braidEnd} ${yOut}`;
  }
  // With named exits every crossing stays in the navy: the braid ends at x 496, the route climbs
  // (or drops) to its exit's height between x 496 and 520 — inside the arch, right of the key —
  // and leaves the arch level, straight to its node; the exit words sit above their node and are
  // never struck through (rounds 3 and 4, defects 8 and 13a). The same numbers as the server.
  const { riseStart, riseEnd } = STAGE;
  const braidMid = Math.round((STAGE.braidStart + riseStart) / 2);
  const riseMid = (riseStart + riseEnd) / 2;
  return `${start} C${braidMid} ${yIn}, ${braidMid} ${yOut}, ${riseStart} ${yOut}`
    + ` C${riseMid} ${yOut}, ${riseMid} ${exitY}, ${riseEnd} ${exitY} H${STAGE.exitX}`;
}

const hero = document.querySelector("[data-hero]");
if (hero) {
  /* 2. The stage (1, the title's reveal, is gone: see the head of this file). */
  const stage = hero.querySelector("[data-stage]");
  const doorway = hero.querySelector("[data-doorway]");
  const legend = hero.querySelector("[data-legend]");
  const routes = [...hero.querySelectorAll("[data-doorway-routes] .route")];

  /* 2a. Anchoring: each route starts at its legend row's node disc, measured in stage units.
         Below 64rem the legend is a plain list and the stage is the door alone (viewBox narrowed
         to the arch), so there is nothing to anchor. */
  const layoutRoutes = () => {
    if (!doorway || !stage || !legend) return;
    if (COMPACT.matches) {
      doorway.setAttribute("viewBox", COMPACT_VIEWBOX);
      stage.classList.add("is-compact");
      return;
    }
    doorway.setAttribute("viewBox", `0 0 ${STAGE.width} ${STAGE.height}`);
    stage.classList.remove("is-compact");
    const box = doorway.getBoundingClientRect();
    if (!box.width) return;
    const scale = STAGE.width / box.width;
    const withExits = doorway.classList.contains("doorway--exits") && WIDE.matches;
    routes.forEach((route, i) => {
      const row = legend.querySelector(`[data-legend-row="${route.dataset.route}"] [data-legend-node]`);
      if (!row) return;
      const disc = row.getBoundingClientRect();
      const x0 = Math.round((disc.left + disc.width / 2 - box.left) * scale);
      const y0 = Math.round((disc.top + disc.height / 2 - box.top) * scale);
      const exitY = EXIT_Y[route.dataset.exit] || EXIT_Y[2];
      const d = routePath(x0, y0, i, exitY, withExits);
      route.querySelectorAll("[data-route-casing], [data-route-line], [data-route-current]").forEach((p) => p.setAttribute("d", d));
      route.querySelectorAll("[data-route-node], [data-route-ring]").forEach((c) => {
        c.setAttribute("cx", String(x0));
        c.setAttribute("cy", String(y0));
      });
    });
  };
  layoutRoutes();
  if (stage && "ResizeObserver" in window) new ResizeObserver(layoutRoutes).observe(stage);
  COMPACT.addEventListener("change", layoutRoutes);
  WIDE.addEventListener("change", layoutRoutes);
  // The legend's rows settle once the interface font has arrived; the anchors follow it.
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(layoutRoutes);

  /* 2b. The scroll-linked pair — nothing on load (see the head of this file). Through WAAPI +
         ScrollTimeline: a `transform` string, not Motion's `y` shorthand, which would fall back
         to a JavaScript scroll callback. At scroll 0 each is at the painted state: the photograph
         at the scale(1.06) hero.css gives it (it started 6px lower: a jump on attach), the stage
         untouched until the hero's end nears 80 % of the viewport. */
  const photo = doorway ? doorway.querySelector("[data-doorway-photo]") : null;
  withMotion(
    () => {
      if (photo) {
        scroll(
          animate(photo, { transform: ["translateY(0) scale(1.06)", "translateY(-18px) scale(1.06)"] }, { ease: "linear" }),
          { target: hero, offset: ["start start", "end start"] },
        );
      }
      if (stage) {
        scroll(
          animate(stage, { transform: ["scale(1)", "scale(0.96)"], opacity: [1, 0.6] }, { ease: "linear" }),
          { target: hero, offset: ["end 80%", "end start"] },
        );
      }
    },
    null,
  );

  /* 2c. Off screen or hidden tab: the current stops (hero.css reads .is-offscreen). */
  new IntersectionObserver(([entry]) => hero.classList.toggle("is-offscreen", !entry.isIntersecting), {
    threshold: 0.05,
  }).observe(hero);
  document.addEventListener("visibilitychange", () => {
    hero.classList.toggle("is-offscreen", document.visibilityState === "hidden");
  });

  /* 2d. The legend lights its route (§4.3). The stage carries `data-route`; the route, the row
         and — when the entrances section is on the page — the related panel carry `is-active` /
         `is-related`. Keyboard: focus does the same as hover; touch: the tap navigates. */
  if (legend && doorway) {
    const related = (actor) => document.querySelector(`.register--entrances [data-route="${actor}"]`);
    // The caption: a reserved slot at the head of the panel, so the gloss never changes a row's
    // height (the routes are anchored to the rows). The row keeps the same text for assistive
    // technology, visually hidden.
    const caption = legend.querySelector("[data-legend-caption]");
    const light = (actor) => {
      doorway.setAttribute("data-route", actor);
      routes.forEach((r) => r.classList.toggle("is-active", r.dataset.route === actor));
      let gloss = "";
      let glossLang = "";
      legend.querySelectorAll("[data-legend-row]").forEach((row) => {
        const on = row.dataset.legendRow === actor;
        row.classList.toggle("is-active", on);
        if (on) {
          gloss = (row.querySelector(".doorway-legend__gloss") || {}).textContent || "";
          // A gloss in a fallback language carries it (services.entrances, text_lang): so does the
          // caption that shows it, for its face and its direction.
          glossLang = (row.querySelector(".doorway-legend__gloss [lang]") || {}).lang || "";
        }
      });
      if (caption) {
        caption.textContent = gloss.trim();
        if (glossLang) caption.setAttribute("lang", glossLang);
        else caption.removeAttribute("lang");
        caption.classList.toggle("is-on", Boolean(gloss.trim()));
      }
      document.querySelectorAll(".register--entrances .is-related").forEach((el) => el.classList.remove("is-related"));
      const panel = related(actor);
      if (panel) panel.classList.add("is-related");
    };
    const dim = () => {
      doorway.removeAttribute("data-route");
      routes.forEach((r) => r.classList.remove("is-active"));
      legend.querySelectorAll("[data-legend-row].is-active").forEach((row) => row.classList.remove("is-active"));
      if (caption) caption.classList.remove("is-on");
      document.querySelectorAll(".register--entrances .is-related").forEach((el) => el.classList.remove("is-related"));
    };
    legend.querySelectorAll("[data-legend-row]").forEach((row) => {
      const actor = row.dataset.legendRow;
      row.addEventListener("pointerenter", (event) => { if (event.pointerType !== "touch") light(actor); });
      row.addEventListener("pointerleave", dim);
      row.addEventListener("focus", () => light(actor));
      row.addEventListener("blur", dim);
    });
  }
}

/* 3. THE ROUTE BETWEEN TWO SHORES — the pilot sequence (function: orientation).
      The line draws with the scroll, not with a timer: the reader advances along the route as they
      advance down the page. ScrollTimeline through Motion's scroll(), so it runs off the main
      thread; with reduced motion the line is simply drawn. The stations settle through the shared
      [data-reveal] pass in shell.js. */
const voyage = document.querySelector("[data-voyage]");
if (voyage) {
  const line = voyage.querySelector(".voyage__line");
  if (line) {
    withMotion(
      () => scroll(animate(line, { strokeDashoffset: [1, 0] }, { ease: "linear" }), {
        target: voyage,
        offset: ["start 85%", "end 70%"],
      }),
      null,
    );
  }
}
