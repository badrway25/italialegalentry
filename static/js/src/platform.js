/**
 * The platform's spotlight (V5.15 lane D; 21st «Spotlight» 35180, adapted — no React, no re-render): a soft light that
 * follows a FINE pointer across a cell of the console's lattice, an organisation's tile, its calm panel. It writes two
 * custom properties on the cell (--spot-x, --spot-y, once a frame at most) and a class while the pointer is over it;
 * portal/v5/_platform.css draws the light from them (in portal/platform.css, the page-only sheet of the pages that load
 * this module). Touch and pen do nothing; the keyboard is never lit (the focus ring says where it is); under reduced
 * motion the light still answers the pointer — it is a hover state, not a movement of the page — but appears at once
 * (the sheet's durations are tokens, 0 ms there).
 *
 * One delegated listener per group (`data-spot-group`) — no listener per cell, nothing at load beyond finding the
 * groups. Without this module the page is complete: the cells simply never light.
 */
import { nextFrame } from "./motion.js";

const groups = document.querySelectorAll("[data-spot-group]");
let frame = 0;
let pending = null;

function paint() {
  frame = 0;
  if (!pending) return;
  const { cell, x, y } = pending;
  const box = cell.getBoundingClientRect();
  cell.style.setProperty("--spot-x", `${Math.round(x - box.left)}px`);
  cell.style.setProperty("--spot-y", `${Math.round(y - box.top)}px`);
  pending = null;
}

for (const group of groups) {
  let lit = null;
  group.addEventListener("pointermove", (event) => {
    if (event.pointerType !== "mouse") return;
    const cell = event.target instanceof Element ? event.target.closest("[data-spot]") : null;
    if (cell !== lit) {
      lit?.classList.remove("is-lit");
      lit = cell && group.contains(cell) ? cell : null;
      lit?.classList.add("is-lit");
    }
    if (!lit) return;
    pending = { cell: lit, x: event.clientX, y: event.clientY };
    if (!frame) {
      frame = 1;
      nextFrame().then(paint); // the motion gate's frame (at once under reduced motion)
    }
  }, { passive: true });
  group.addEventListener("pointerleave", () => {
    lit?.classList.remove("is-lit");
    lit = null;
  });
}
