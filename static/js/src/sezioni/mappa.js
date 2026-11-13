/**
 * H · «la mappa» — the interactive actor map (design V5.22, SECTION_SYSTEM_V2 §2 H; lane S). A split chunk loaded by
 * rise.js for [data-sec-js~="mappa"]: without it the nodes are anchors to their entries and every entry is listed —
 * `:target` shows one.
 *
 * The nodes become a tablist (the hub first: Escape and the hub return to it; the list's items step out of the tree,
 * role="none", so the tabs are the tablist's own children), roving tabindex, the Arrows rotate the
 * selection around the ring, Home and End; activation follows the focus. A fine pointer's hover previews a node, a
 * click or Enter commits it. The panels stack in one grid cell (no selection moves the page); the selected node's spoke
 * and its two neighbours' links draw, the highlight glides around the ring (`--sel`, v5/_sec-mappa.css), the panel
 * crosses in from its node's side. No scroll listener; no observer.
 */
import { reducedMotion } from "../motion.js";

function setup(root) {
  const tabs = [...root.querySelectorAll(".mappa__tasto")];
  const panels = tabs.map((tab) => root.querySelector(tab.hash));
  if (tabs.length < 2 || panels.includes(null)) return;
  const list = root.querySelector(".mappa__nodi");
  const spokes = [...root.querySelectorAll(".mappa__raggio")];
  const fine = matchMedia("(hover: hover) and (pointer: fine)");
  let committed = 0;

  const ring = root.querySelector(".mappa__anello");
  if (ring.getBoundingClientRect().width < 300) return; // a phone's narrow ring: the list is the map (v5/_sec-mappa.css)
  ring.style.setProperty("--n", String(tabs.length - 1));
  tabs.slice(1).forEach((tab, i) => tab.parentElement.style.setProperty("--i", String(i)));
  spokes.forEach((spoke, i) => spoke.style.setProperty("--i", String(i)));
  list.setAttribute("role", "tablist");
  if (root.dataset.label) list.setAttribute("aria-label", root.dataset.label);
  tabs.forEach((tab, i) => {
    tab.parentElement.setAttribute("role", "none");
    tab.setAttribute("role", "tab");
    tab.setAttribute("aria-controls", panels[i].id);
    panels[i].setAttribute("role", "tabpanel");
    panels[i].setAttribute("aria-labelledby", tab.id);
  });

  function show(i) {
    root.style.setProperty("--sel", String(tabs[i].dataset.i || 0));
    root.dataset.sel = tabs[i].dataset.node || "hub";
    tabs.forEach((tab, k) => {
      tab.setAttribute("aria-selected", String(k === i));
      tab.tabIndex = k === i ? 0 : -1;
      panels[k].toggleAttribute("data-on", k === i);
    });
    spokes.forEach((spoke, k) => spoke.toggleAttribute("data-on", k === i - 1));
  }

  function commit(i, focus) {
    committed = i;
    show(i);
    if (!focus) return;
    root.dataset.moved = "";
    tabs[i].focus();
    // a phone's entry stands under the ring, below the first screen: the chosen one comes into view (at once from the
    // keyboard and under reduced motion)
    const box = panels[i].getBoundingClientRect();
    if (box.top < 0 || box.bottom > innerHeight) {
      const calm = reducedMotion() || document.documentElement.dataset.input === "key";
      panels[i].scrollIntoView({ block: "nearest", behavior: calm ? "instant" : "smooth" });
    }
  }

  root.addEventListener("click", (event) => {
    const tab = event.target.closest(".mappa__tasto");
    if (!tab) return;
    event.preventDefault();
    commit(tabs.indexOf(tab), true);
  });
  root.addEventListener("keydown", (event) => {
    const i = tabs.indexOf(event.target.closest(".mappa__tasto"));
    if (i < 0) return;
    const n = tabs.length;
    const rtl = getComputedStyle(root).direction === "rtl" ? -1 : 1;
    const step = { ArrowRight: rtl, ArrowDown: 1, ArrowLeft: -rtl, ArrowUp: -1 }[event.key];
    const next = step ? (i + step + n) % n : event.key === "Home" ? 0 : event.key === "End" ? n - 1 : event.key === "Escape" ? 0 : -1;
    if (next < 0) return;
    event.preventDefault();
    commit(next, true);
  });
  list.addEventListener("pointerover", (event) => {
    const tab = event.target.closest(".mappa__tasto");
    if (!fine.matches || !tab) return;
    root.dataset.moved = "";
    show(tabs.indexOf(tab));
  });
  list.addEventListener("pointerleave", () => fine.matches && show(committed));
  commit(Math.max(0, panels.findIndex((panel) => "#" + panel.id === location.hash)));
}

export default function initMappa() {
  document.querySelectorAll("[data-sec-js~='mappa']").forEach(setup);
}
