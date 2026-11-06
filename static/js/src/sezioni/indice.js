/**
 * L · «l'indice» — tabs and master–detail, and the exclusive disclosure of a phone (design V5.22, SECTION_SYSTEM_V2 §2 L;
 * lane S). A split chunk loaded by rise.js for [data-sec-js~="indice"]: without it the index is a list of anchors and
 * every panel is shown — complete in reading order.
 *
 * ≥ 64 rem: the ARIA tabs pattern — a vertical tablist (roving tabindex; Arrows, Home, End; activation follows the
 * focus), the panels stacked in one grid cell so a selection never moves the page (CLS 0); the first item, or the one
 * the address names (#id: the FAQ's permalinks), is selected; `data-hash` keeps the address in step. The list's items
 * step out of the tree while it is a tablist (role="none": the tabs are the tablist's own children, as ARIA requires —
 * axe's aria-required-children and aria-required-parent) and step back in when it is a list again. Below 64 rem: each
 * panel's own heading becomes its disclosure button, all closed at first, one open at a time; the button exists only
 * then — a tab's panel heading is a heading, never a dormant button. The keyboard's change is instant
 * (v5/_sec-indice.css: html[data-input="key"] never animates); the stage crosses in only once the reader has chosen
 * (`data-moved`), never at load. No scroll listener; one media listener.
 */
import { reducedMotion } from "../motion.js";

const WIDE = "(min-width: 64rem)";

function setup(root) {
  const tabs = [...root.querySelectorAll(".indice__voce")];
  const panels = tabs.map((tab) => root.querySelector(tab.hash));
  if (!tabs.length || panels.includes(null)) return;
  const list = root.querySelector(".indice__lista");
  const media = matchMedia(WIDE);
  const hashed = root.hasAttribute("data-hash");
  const named = () => panels.findIndex((panel) => "#" + panel.id === location.hash);
  let current = Math.max(0, named());

  const heads = panels.map((panel) => panel.querySelector(".indice__titolo"));
  const buttons = panels.map((panel, i) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "indice__apri";
    button.setAttribute("aria-controls", panel.id + "-corpo");
    panel.querySelector(".indice__corpo").id = panel.id + "-corpo";
    button.addEventListener("click", () => open(i, button.getAttribute("aria-expanded") !== "true"));
    return button;
  });

  // the heading's words move into its button for a phone's disclosure, and back out for the tabs
  function wrap(on) {
    heads.forEach((head, i) => {
      const button = buttons[i];
      if (on === button.isConnected) return;
      if (on) {
        button.append(...head.childNodes);
        head.append(button);
      } else {
        head.append(...button.childNodes);
        button.remove();
      }
    });
  }

  function select(i, focus) {
    current = i;
    tabs.forEach((tab, k) => {
      const on = k === i;
      tab.setAttribute("aria-selected", String(on));
      tab.tabIndex = on ? 0 : -1;
      panels[k].toggleAttribute("data-on", on);
    });
    if (!focus) return;
    root.dataset.moved = "";
    tabs[i].focus();
    if (hashed) history.replaceState(null, "", "#" + panels[i].id);
  }

  function open(i, on) {
    buttons.forEach((button, k) => {
      const show = on && k === i;
      button.setAttribute("aria-expanded", String(show));
      panels[k].toggleAttribute("data-on", show);
    });
  }

  function mode() {
    const wide = media.matches;
    root.dataset.mode = wide ? "tabs" : "disclosure";
    list.setAttribute("role", wide ? "tablist" : "list");
    if (wide) list.setAttribute("aria-orientation", "vertical");
    else list.removeAttribute("aria-orientation");
    wrap(!wide);
    tabs.forEach((tab, i) => {
      if (wide) {
        tab.parentElement.setAttribute("role", "none");
        tab.setAttribute("role", "tab");
        tab.setAttribute("aria-controls", panels[i].id);
        panels[i].setAttribute("role", "tabpanel");
        panels[i].setAttribute("aria-labelledby", tab.id);
      } else {
        tab.parentElement.removeAttribute("role");
        ["role", "aria-controls", "aria-selected", "tabindex"].forEach((name) => tab.removeAttribute(name));
        panels[i].removeAttribute("role");
        panels[i].setAttribute("aria-labelledby", panels[i].id + "-title");
      }
    });
    if (wide) select(current);
    else open(hashed ? named() : -1, true); // a phone opens the answer its address names, the others folded
  }

  list.addEventListener("click", (event) => {
    const i = tabs.indexOf(event.target.closest(".indice__voce"));
    if (i < 0 || !media.matches) return;
    event.preventDefault();
    select(i, true);
  });
  list.addEventListener("keydown", (event) => {
    const i = tabs.indexOf(event.target.closest(".indice__voce"));
    if (i < 0 || !media.matches) return;
    const last = tabs.length - 1;
    const step = { ArrowDown: 1, ArrowRight: 1, ArrowUp: -1, ArrowLeft: -1 }[event.key];
    const rtl = getComputedStyle(root).direction === "rtl" && /Left|Right/.test(event.key) ? -1 : 1;
    const next = step ? (i + step * rtl + tabs.length) % tabs.length : event.key === "Home" ? 0 : event.key === "End" ? last : -1;
    if (next < 0) return;
    event.preventDefault();
    select(next, true);
  });
  media.addEventListener("change", mode);
  // a same-document permalink (a link to another question, the address bar) selects or opens its answer; on a phone
  // its heading comes under the letterhead (an answer above it may have folded) — at once from the keyboard and under
  // reduced motion
  if (hashed)
    addEventListener("hashchange", () => {
      const i = named();
      if (i < 0) return;
      if (media.matches) return select(i);
      current = i;
      open(i, true);
      const calm = reducedMotion() || document.documentElement.dataset.input === "key";
      heads[i].scrollIntoView({ block: "start", behavior: calm ? "instant" : "smooth" });
    });
  mode();
}

export default function initIndice() {
  document.querySelectorAll("[data-sec-js~='indice']").forEach(setup);
}
