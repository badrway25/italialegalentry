/**
 * The home's one entry (design V5.4, plan §2.3 «JavaScript»; W2-D): it imports the hero's module and carries the
 * dismissible institutional notice — moved verbatim from apps/pages/static/pages/js/home.js, which is deleted (one
 * request fewer). Bundled by esbuild into static/js/dist/home.js and loaded by templates/pages/home.html as a module:
 * deferred, never inline.
 *
 * The V4 hero's choreography (the route anchoring, the scroll-linked photograph and stage, the legend's hover state)
 * left with the V4 hero: the V5 hero is hero.js, and its hand states are CSS (hero.css). The pilot route's line, drawn
 * with the scroll, left with the route (W2-D step 3): the Morocco → Italy model is said once, by the hero's path, and
 * the chapters under the hero do not move.
 */
import "./hero.js";

/* THE DISMISSIBLE NOTICE — progressive enhancement only (the page is complete without it).
      `[data-dismissible="<id>"]` wrappers hold a hidden `[data-dismiss]` button. With JS the button
      appears; activating it hides the notice and remembers the choice for the current tab in
      sessionStorage — no cookie, no identifier, nothing sent to the server. Focus moves to the main
      landmark so keyboard users are never left on a removed control. */
const PREFIX = "ile.dismissed.";

function storage() {
  try {
    const probe = `${PREFIX}probe`;
    window.sessionStorage.setItem(probe, "1");
    window.sessionStorage.removeItem(probe);
    return window.sessionStorage;
  } catch (error) {
    return null; // storage blocked: the notice is simply dismissed for this page view
  }
}

function initDismissible(wrapper, store) {
  const key = PREFIX + wrapper.dataset.dismissible;
  const button = wrapper.querySelector("[data-dismiss]");
  if (!button) return;
  if (store && store.getItem(key) === "1") {
    wrapper.hidden = true;
    return;
  }
  button.hidden = false;
  button.addEventListener("click", () => {
    wrapper.hidden = true;
    if (store) store.setItem(key, "1");
    const main = document.getElementById("main-content");
    if (main) main.focus({ preventScroll: true });
  });
}

const store = storage();
document.querySelectorAll("[data-dismissible]").forEach((wrapper) => initDismissible(wrapper, store));

/* V5.31 · THE HOME'S TABS (owner's FINAL HOMEPAGE REBUILD, 10 Nov 2026; lane B) — the orientation's four moments and the
      pathway explorer: `[data-tabs]` holds `[data-tab]` anchors and their `[data-panel]`s. Without script the anchors
      jump to panels that all stand in order; with it, the ARIA tabs pattern — roving tabindex, the arrows (mirrored on
      a right-to-left page), Home and End, activation following the focus — the panels stacked in one cell (CLS 0) and
      the first selected (or the one the address names). `data-moved` is set once the reader has chosen, so the stage
      crosses in only then; the keyboard's change is instant (html[data-input="key"], v5/_home-b.css). */
const WIDE = matchMedia("(min-width: 64rem)");

function initTabs(root) {
  const tabs = [...root.querySelectorAll("[data-tab]")];
  const panels = tabs.map((tab) => root.querySelector(tab.hash));
  if (!tabs.length || panels.includes(null)) return;
  const list = tabs[0].closest("ul");
  list.setAttribute("role", "tablist");
  const orient = () => list.setAttribute("aria-orientation", WIDE.matches ? "vertical" : "horizontal");
  orient();
  WIDE.addEventListener("change", orient);
  tabs.forEach((tab, i) => {
    tab.parentElement.setAttribute("role", "none");
    tab.setAttribute("role", "tab");
    tab.setAttribute("aria-controls", panels[i].id);
    panels[i].setAttribute("role", "tabpanel");
    panels[i].setAttribute("aria-labelledby", tab.id);
  });
  const select = (i, moved) => {
    tabs.forEach((tab, k) => {
      tab.setAttribute("aria-selected", String(k === i));
      tab.tabIndex = k === i ? 0 : -1;
      panels[k].toggleAttribute("data-on", k === i);
    });
    if (!moved) return;
    root.dataset.moved = "";
    tabs[i].focus({ preventScroll: true });
    tabs[i].scrollIntoView({ block: "nearest", inline: "nearest" });
  };
  list.addEventListener("click", (event) => {
    const i = tabs.indexOf(event.target.closest("[data-tab]"));
    if (i < 0) return;
    event.preventDefault();
    select(i, true);
  });
  list.addEventListener("keydown", (event) => {
    const i = tabs.indexOf(event.target.closest("[data-tab]"));
    const step = { ArrowDown: 1, ArrowRight: 1, ArrowUp: -1, ArrowLeft: -1 }[event.key];
    if (i < 0 || !(step || event.key === "Home" || event.key === "End")) return;
    const flip = /Left|Right/.test(event.key) && getComputedStyle(root).direction === "rtl" ? -1 : 1;
    const n = tabs.length;
    event.preventDefault();
    select(step ? (i + step * flip + n) % n : event.key === "Home" ? 0 : n - 1, true);
  });
  select(Math.max(0, panels.findIndex((panel) => "#" + panel.id === location.hash)));
  root.dataset.ready = "";
}

document.querySelectorAll("[data-tabs]").forEach(initTabs);

/* the frauds' detail (owner §22): the body's two middle sentences behind «Lire le détail»; the text itself is never cut */
const apri = document.querySelector("[data-allerta-apri]");
if (apri && apri.previousElementSibling.querySelector(".ls-4")) {
  apri.hidden = false;
  apri.addEventListener("click", () => apri.setAttribute("aria-expanded", String(apri.getAttribute("aria-expanded") !== "true")));
}

/* the phones' doors (owner's precision pass, 11 Nov 2026): each tile's sentence behind its own button, one open at a time —
      the sentence is drawn by hero.css from the button's aria-expanded; without script the button stays hidden */
const more = [...document.querySelectorAll("[data-origin-more]")];
more.forEach((button) => {
  button.hidden = false;
  button.addEventListener("click", () =>
    more.forEach((other) => other.setAttribute("aria-expanded", String(other === button && button.getAttribute("aria-expanded") !== "true"))));
});
