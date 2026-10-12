/**
 * The overlay system — one module for every overlay of the product (docs/design-v5/V5_4_EXECUTION_PLAN.md §1.14; the
 * primitive contract docs/design-v5/QA/v54/w2-a/CONTRACT.md; W2-A): the modal and the alert dialog, the drawer, the
 * bottom sheet, the popover / menu and the tooltip, on native elements, drawn by static/css/v5/overlays.css.
 *
 * NATIVE ELEMENTS, AND THE INP RULE (plan §1.14). A modal kind is a <dialog>. showModal() makes the whole page inert,
 * and inertness is a style flag every element inherits: on the heaviest pages (the Arabic «Mes documents», the
 * phase-3 home on a phone) the cold open re-styled the whole document — 860 and 1 024 elements, ≈ 105 ms of style at
 * CPU × 4, p90 200 / 168 ms — against 184 / 234 and p90 80 / 72 ms trapped (docs/design-v5/QA/v54/w2-a/NOTES.md,
 * «INP»). So, as the plan's rule says, a modal kind opens with show() — a
 * dialog all the same, `aria-modal="true"`, close requests (`closedby`) — over ONE shared scrim, with the trap in
 * script: Tab and Shift+Tab wrap inside the panel and a focus that lands outside it is brought back; Esc, the focus
 * return and the scroll lock as for any modal. An engine prunes nothing for `aria-modal` alone, so while a trapped
 * panel is open the rest of the page is `aria-hidden` (never `inert`, which re-styles every element).
 * `data-overlay-modal="native"` keeps showModal() where a page is light.
 * A menu is a `popover` with a `popovertarget` trigger: light dismiss and Esc are the platform's. This module adds
 * what the platform does not give, and nothing else:
 *   · the state at t = 0 — open, aria-expanded, the focus — in the task of the input; nothing waits for a motion;
 *   · the focus moved in (CONTRACT §4) and given back to the opener, or to its successor (`data-overlay-return`),
 *     brought into the panel's own view when it lands low in a long list (the page behind never scrolls);
 *     Tab and Shift+Tab wrap inside a modal panel, and a focus sent outside a trapped one comes back; a body that
 *     scrolls and holds nothing to focus is a stop of its own;
 *   · the dismissals the platform lacks — the scrim (only when the pointer went down AND came up on it; never for an
 *     alert; never with unsaved input), «Fermer» (`data-overlay-close`), a link in a drawer, a choice in a menu, the
 *     focus leaving a menu (S-7), the grip of a sheet, Back (`data-overlay-history`), Esc for every dialog the
 *     platform does not close itself (a trapped modal, a drawer beside the list);
 *   · a menu shown as a phone sheet stands over the same scrim, which takes the whole press that dismisses it — the
 *     page is never reached — without a trap or a scroll lock: it stays a menu;
 *   · the alert's Esc is its safe answer (`data-overlay-safe`);
 *   · the scroll lock with the scrollbar's gutter kept (`html[data-overlay-lock]`), so nothing moves sideways;
 *   · a menu's side chosen before it opens (so its 4 px drop goes away from the trigger), its anchor bound, and —
 *     without anchor positioning — its place computed, with the same flip and clamp;
 *   · the leaving panel made `inert` for the length of its exit (B2);
 *   · the tooltip's Esc and press (`data-tip-off`), and the one shared top-layer tip for `data-tip="layer"` — its
 *     words the control's name or `data-tip-label`, its place beside the control or beyond the ancestor
 *     `data-tip-beyond` names (followed when a scroll moves the control), and a cancelable `overlay:tip` by which the
 *     page may refuse it (the rail's word);
 *   · the disclosure menus that are still a `<details data-dropdown>` (the rail's language): one open at a time,
 *     `aria-expanded` on the summary, Esc, a press outside and the focus leaving put one away — and an open one
 *     takes the Esc before the panel it stands in (the language's list goes before the drawer, DL54-69).
 * The motion is CSS: transitions both ways, tier 0 from the keyboard (html[data-input], static/js/head.js, or
 * `instant`), one 80 ms opacity under reduced motion. No style attribute is written: CSSOM properties only (left, top,
 * translate, the anchor names, --overlay-drag, a trapped panel's and the scrim's z-index), which the CSP allows. Strings are the templates', never this file's.
 * THE RARER PARTS — the grip of a sheet, Back, the placement without anchor positioning, a dialog's scrolling body
 * made a stop, a native modal's backdrop press — are no console page's: they live in static/js/src/overlay/extras.js,
 * imported on demand (at idle where a page draws one; at once for the placement), so the console's pages do not fetch
 * them (plan §2.6's module budget; A11Y_PERF M4).
 *
 * API (CONTRACT §6): open(panel, {opener, focus, instant, history}) · close(panel, {reason, focus, instant}) ·
 * toggle(panel, options) · isOpen(panel) · initOverlays(root). Events on the panel, bubbling: `overlay:open`,
 * `overlay:close` — detail {reason, opener}. The module wires the document when it is imported.
 */

const ROOT = document.documentElement;
const PHONE = window.matchMedia("(max-width: 40rem)");
const POINTER = window.matchMedia("(hover: hover) and (pointer: fine)");
const KINDS = new Set(["dialog", "alert", "drawer", "sheet", "popover"]);
const TABBABLE = [
  "a[href]",
  "area[href]",
  "button:not([disabled])",
  "input:not([disabled]):not([type='hidden'])",
  "select:not([disabled])",
  "textarea:not([disabled])",
  "summary",
  "iframe",
  "[contenteditable='true']",
  "[tabindex]:not([tabindex='-1'])",
].join(",");
/** The closes after which the focus goes back to the opener — when it is still inside the panel or nowhere. */
const RETURNS = new Set(["esc", "close", "choice", "grip", "back", "scrim", "light", "api"]);
/** A disclosure menu: a native <details> that opens a list over the page (the rail's language). */
const DISCLOSURE = "details[data-dropdown]";
/** The current entry of a list, whatever its token (page, true, step, location). */
const CURRENT = "[aria-current]:not([aria-current='false'])";
const ANCHORED = typeof CSS !== "undefined" && CSS.supports("position-area", "self-block-end span-self-inline-start");
const GAP = 4; // between a menu and its trigger (= --s-1 in the sheet)
const EDGE = 8; // the least distance between a placed surface and the viewport's edge

const records = new WeakMap();
const wired = new WeakSet();
const sizes = new WeakMap();
const opened = []; // every open panel, the topmost last
let locks = 0;
let scrim = null; // the one scrim of the trapped modals and the menu sheets (overlays.css: .overlay-scrim)
let zBase = 0; // --z-modal, read once at idle with the scrim: no style read between an opening's writes
let anchors = 0;
let documentWired = false;
let extras = null; // the rarer parts (overlay/extras.js), once loaded
let extrasLoading = null;

/* ---- small helpers ----------------------------------------------------------------------------------------- */
const panelOf = (target) => (typeof target === "string" ? document.getElementById(target) : target);
const kindOf = (panel) =>
  panel && panel.nodeType === 1 && KINDS.has(panel.getAttribute("data-overlay")) ? panel.getAttribute("data-overlay") : null;
const fromKeyboard = () => ROOT.getAttribute("data-input") === "key";
const popoverOpen = (element) => {
  try {
    return element.matches(":popover-open");
  } catch {
    return false;
  }
};
const visible = (element) => element.getClientRects().length > 0 && getComputedStyle(element).visibility !== "hidden";
const recordOf = (panel) => {
  let record = records.get(panel);
  if (!record) {
    record = { open: false, opener: null, reason: null, focus: undefined, modal: false, pushed: false, anchor: "" };
    records.set(panel, record);
  }
  return record;
};
const millis = (panel, name, fallback) => {
  const raw = getComputedStyle(panel).getPropertyValue(name).trim();
  const value = parseFloat(raw);
  if (!raw || Number.isNaN(value)) return fallback;
  return raw.endsWith("ms") ? value : value * 1000;
};
const openersOf = (panel) => {
  if (!panel.id) return [];
  const id = CSS.escape(panel.id);
  // a button names its panel in data-overlay-open; a link opener (the no-script path) in its href
  return [
    ...document.querySelectorAll(
      `[data-overlay-open="${id}"], a[data-overlay-open=""][href="#${id}"], [popovertarget="${id}"]`,
    ),
  ];
};

/** Is the panel open — a dialog's [open], a popover's :popover-open? */
export function isOpen(target) {
  const panel = panelOf(target);
  if (!kindOf(panel)) return false;
  return panel.hasAttribute("popover") ? popoverOpen(panel) : Boolean(panel.open);
}

function tabbables(panel) {
  return [...panel.querySelectorAll(TABBABLE)].filter((element) => !element.closest("[inert]") && visible(element));
}

function titleOf(panel) {
  const id = panel.getAttribute("aria-labelledby");
  const title = (id && document.getElementById(id)) || panel.querySelector(".overlay__title");
  return title && panel.contains(title) ? title : null;
}

/** CONTRACT §4: where the focus goes when the panel opens. */
function focusTarget(panel, requested) {
  if (requested === false) return null;
  if (requested && requested.nodeType === 1) return requested;
  if (typeof requested === "string") return panel.querySelector(requested);
  const kind = kindOf(panel);
  const pick = (selector) => [...panel.querySelectorAll(selector)].find(visible) || null;
  const firstIn = (selector) => {
    const part = panel.querySelector(selector);
    return part ? tabbables(part)[0] || null : null;
  };
  if (kind === "popover") return pick("[data-overlay-focus]") || pick(CURRENT) || tabbables(panel)[0] || panel;
  const besideTheList = kind === "drawer" && panel.getAttribute("data-overlay-modal") === "none" && !PHONE.matches;
  return (
    pick("[data-overlay-focus]") ||
    (kind === "alert" ? pick("[data-overlay-safe]") : null) ||
    (besideTheList ? titleOf(panel) : null) ||
    pick(CURRENT) ||
    firstIn(".overlay__body") ||
    firstIn(".overlay__foot") ||
    titleOf(panel) ||
    panel.querySelector("[data-overlay-close]") ||
    panel
  );
}

function focus(element) {
  if (!element) return;
  if (!element.matches(TABBABLE) && !element.hasAttribute("tabindex")) element.setAttribute("tabindex", "-1");
  // the page behind never scrolls for a focus of this module (preventScroll); inside an open panel — fixed, over a
  // locked page, so nothing but its own list can move — the target is brought into the panel's view: the current
  // entry low in the drawer's list, the far end of the trap's wrap (A11Y_PERF M1, WCAG 2.4.7)
  element.focus({ preventScroll: true });
  const panel = element.closest("[data-overlay]");
  if (panel && panel !== element && isOpen(panel)) element.scrollIntoView({ block: "nearest", inline: "nearest" });
}

function setExpanded(panel, open) {
  openersOf(panel).forEach((opener) => opener.setAttribute("aria-expanded", open ? "true" : "false"));
}

/* ---- the scroll lock: the page behind a modal does not scroll, and keeps its scrollbar's gutter --------------- */
function lock(scrollbar) {
  locks += 1;
  if (locks > 1) return;
  ROOT.setAttribute("data-overlay-lock", scrollbar ? "gutter" : "");
}

/** Does the page show a scrollbar? Read BEFORE an opening writes anything, so the read costs no style recalculation. */
const hasScrollbar = () => window.innerWidth - ROOT.clientWidth > 0;

function unlock() {
  if (locks === 0) return;
  locks -= 1;
  if (locks === 0) ROOT.removeAttribute("data-overlay-lock");
}

/* ---- a menu's side, anchor and place --------------------------------------------------------------------------- */
const asSheet = (panel) => PHONE.matches && panel.getAttribute("data-overlay-phone") !== "none";

/** Before it opens: below its trigger unless it does not fit there and there is more room above (MS §6). */
function chooseSide(panel, trigger) {
  panel.style.removeProperty("left");
  panel.style.removeProperty("top");
  if (!trigger || asSheet(panel)) {
    panel.removeAttribute("data-overlay-side");
    return;
  }
  const box = trigger.getBoundingClientRect();
  const height = (sizes.get(panel) || { height: 0 }).height;
  const below = window.innerHeight - box.bottom - GAP - EDGE;
  const above = box.top - GAP - EDGE;
  panel.toggleAttribute("data-overlay-side", height > below && above > below);
  if (panel.hasAttribute("data-overlay-side")) panel.setAttribute("data-overlay-side", "above");
  if (ANCHORED) {
    const record = recordOf(panel);
    if (!record.anchor) {
      anchors += 1;
      record.anchor = `--overlay-anchor-${anchors}`;
    }
    trigger.style.setProperty("anchor-name", record.anchor);
    panel.style.setProperty("position-anchor", record.anchor);
  }
}

/** Without anchor positioning (overlay/extras.js): a menu placed beside its trigger and followed — only while open. */
function placeByScript(panel, on = true) {
  if (ANCHORED) return;
  withExtras((parts) => {
    if (on && isOpen(panel)) {
      parts.place(panel, recordOf(panel).opener);
      parts.follow(panel, true);
    } else {
      parts.follow(panel, false);
    }
  });
}

/** The menus' sizes, read once at idle on inert clones, so the side is known before the first opening. */
function measure(root) {
  const panels = [...root.querySelectorAll("[data-overlay='popover']")].filter((panel) => !sizes.has(panel));
  if (!panels.length) return;
  const box = document.createElement("div");
  box.className = "overlay-measure";
  box.setAttribute("aria-hidden", "true");
  box.inert = true;
  const clones = panels.map((panel) => {
    const clone = panel.cloneNode(true);
    [clone, ...clone.querySelectorAll("[id]")].forEach((node) => node.removeAttribute("id"));
    clone.removeAttribute("popover");
    clone.setAttribute("data-overlay-measure", "");
    box.append(clone);
    return clone;
  });
  document.body.append(box);
  panels.forEach((panel, index) => sizes.set(panel, { width: clones[index].offsetWidth, height: clones[index].offsetHeight }));
  box.remove();
}

function whenIdle(task) {
  if (typeof window.requestIdleCallback === "function") window.requestIdleCallback(task, { timeout: 1500 });
  else window.setTimeout(task, 250);
}

/* ---- the rarer parts (overlay/extras.js): loaded once, on demand; what they need is handed over ---------------- */
function loadExtras() {
  if (!extrasLoading) {
    extrasLoading = import("./overlay/extras.js").then((module) => {
      extras = module.install({
        close,
        recordOf,
        opened,
        asSheet,
        popoverOpen,
        kindOf,
        tabbables,
        topTrapped: () => trapped().pop(),
        scrim: () => scrim,
        GAP,
        EDGE,
        ROOT,
      });
      return extras;
    });
  }
  return extrasLoading;
}

/** Run a task with the rarer parts — at once when they are here, else as soon as they arrive. */
function withExtras(task) {
  if (extras) task(extras);
  else loadExtras().then(task, () => {});
}

/** Back: one history entry for an open panel (a swap replaces it) — only while the panel is still open. */
function remember(panel, record, history) {
  withExtras((parts) => isOpen(panel) && parts.remember(panel, record, history));
}

/* ---- open --------------------------------------------------------------------------------------------------- */
/**
 * Open a panel (an element, or its id). `opener` is where the focus goes back (default: the focused element);
 * `focus` overrides the target of CONTRACT §4 (an element, a selector, or false); `instant` is tier 0 (default: the
 * last input was a key); `history` pushes an entry that Back takes away (`{url, replace}` for a content swap). An open
 * panel is not opened again: its opener is updated and a swap replaces its history entry — the slide never replays.
 */
export function open(target, options = {}) {
  const panel = panelOf(target);
  const kind = kindOf(panel);
  if (!kind || !panel.isConnected) return false;
  wirePanel(panel);
  const record = recordOf(panel);
  const history = options.history ?? (panel.hasAttribute("data-overlay-history") ? true : undefined);
  if (isOpen(panel)) {
    if (options.opener) record.opener = options.opener;
    if (history && record.pushed) remember(panel, record, typeof history === "object" ? history : { replace: true });
    return true;
  }
  const scrollbar = kind !== "popover" && locks === 0 ? hasScrollbar() : false; // the one read, before any write
  const active = document.activeElement;
  record.opener = options.opener || (active && active !== document.body && !panel.contains(active) ? active : null);
  record.reason = null;
  record.focus = undefined;
  record.opening = true;
  panel.toggleAttribute("data-instant", Boolean(options.instant ?? fromKeyboard()));
  window.clearTimeout(record.inertTimer);
  panel.inert = false;
  panel.removeAttribute("data-overlay-dirty");
  try {
    if (kind === "popover") {
      chooseSide(panel, record.opener);
      panel.showPopover({ source: record.opener || undefined });
      placeByScript(panel);
      sizes.set(panel, { width: panel.offsetWidth, height: panel.offsetHeight });
    } else {
      const beside = kind === "drawer" && panel.getAttribute("data-overlay-modal") === "none";
      const modal = !beside || PHONE.matches;
      panel.toggleAttribute("data-overlay-mode", beside && modal);
      if (beside && modal) panel.setAttribute("data-overlay-mode", "sheet");
      // close requests (Esc, a phone's Back gesture) reach a dialog that is not opened by showModal()
      if (!panel.hasAttribute("closedby")) panel.setAttribute("closedby", "closerequest");
      if (modal) {
        lock(scrollbar);
        record.modal = true;
        record.native = panel.getAttribute("data-overlay-modal") === "native";
        if (record.native) {
          panel.showModal();
        } else {
          panel.setAttribute("aria-modal", "true");
          panel.show();
        }
      } else {
        panel.show();
      }
    }
  } catch {
    if (record.modal) unlock();
    record.modal = false;
    record.opening = false;
    return false;
  }
  record.opening = false;
  adopt(panel);
  syncScrim();
  focus(focusTarget(panel, options.focus));
  syncHidden(); // once the focus is in: it never stands in a hidden subtree
  // a body that scrolls with nothing to focus is a stop of its own (overlay/extras.js; the focus has laid it out)
  if (kind !== "popover" && panel.querySelector(".overlay__body")) withExtras((parts) => parts.reachable(panel));
  if (history) remember(panel, record, history);
  panel.dispatchEvent(new CustomEvent("overlay:open", { bubbles: true, detail: { reason: options.reason || "api", opener: record.opener } }));
  return true;
}

/** The bookkeeping of an open panel, wherever the opening came from (this module, a native trigger, another script). */
function adopt(panel) {
  const record = recordOf(panel);
  if (record.open) return;
  record.open = true;
  if (!panel.hasAttribute("popover") && !record.modal && panel.matches(":modal")) {
    // a dialog another script opened with showModal(): a native modal, its ::backdrop press included
    record.modal = true;
    record.native = true;
    lock(hasScrollbar());
    withExtras((parts) => parts.wireBackdrop(panel, record));
  }
  if (!opened.includes(panel)) opened.push(panel);
  setExpanded(panel, true);
}

/* ---- close ---------------------------------------------------------------------------------------------------- */
/**
 * Close a panel. `reason` is said in `overlay:close` (default "api"); `focus` is where the focus goes instead of the
 * opener (false: it stays); `instant` is tier 0 (default: the last input was a key).
 */
export function close(target, options = {}) {
  const panel = panelOf(target);
  if (!kindOf(panel) || !isOpen(panel)) return false;
  const record = recordOf(panel);
  record.reason = options.reason || "api";
  record.focus = options.focus;
  panel.toggleAttribute("data-instant", Boolean(options.instant ?? fromKeyboard()));
  if (panel.hasAttribute("popover")) panel.hidePopover(); // beforetoggle settles it, in this task
  else panel.close();
  settle(panel);
  return true;
}

/** Toggle a panel; true when it is now open. */
export function toggle(target, options = {}) {
  return isOpen(target) ? !close(target, options) : open(target, options);
}

/** What every close does once, whoever started it (this module, Esc, a light dismiss, a form method="dialog"). */
function settle(panel) {
  const record = recordOf(panel);
  if (!record.open) return;
  record.open = false;
  const reason = record.reason || (panel.hasAttribute("popover") ? "light" : "close");
  record.reason = null;
  const index = opened.indexOf(panel);
  if (index >= 0) opened.splice(index, 1);
  if (record.modal) unlock();
  record.modal = false;
  record.native = false;
  panel.removeAttribute("aria-modal");
  panel.style.removeProperty("z-index");
  syncScrim();
  syncHidden(); // before the focus comes back to the page
  if (panel.hasAttribute("popover")) placeByScript(panel, false);
  setExpanded(panel, false);
  panel.removeAttribute("data-overlay-dirty");
  panel.removeAttribute("data-overlay-dragging");
  panel.style.removeProperty("translate");
  panel.style.removeProperty("--overlay-drag");
  // B2: the leaving panel takes no click and no Tab for the length of its exit
  panel.inert = true;
  window.clearTimeout(record.inertTimer);
  record.inertTimer = window.setTimeout(() => {
    if (!isOpen(panel)) panel.inert = false;
  }, millis(panel, "--overlay-out", 200) + 80);
  // the focus goes back where the person was — only from inside the panel, or from nowhere
  const active = document.activeElement;
  const within = !active || active === document.body || panel.contains(active);
  if (record.focus !== false && RETURNS.has(reason) && within) {
    let target = record.focus && record.focus.nodeType === 1 ? record.focus : record.opener;
    if (!target || !target.isConnected || target.closest("[inert]")) {
      const id = (record.opener && record.opener.getAttribute && record.opener.getAttribute("data-overlay-return")) ||
        panel.getAttribute("data-overlay-return");
      target = (id && document.getElementById(id)) || document.getElementById("main-content");
    }
    focus(target);
  }
  record.focus = undefined;
  if (record.pushed && reason !== "back") {
    record.pushed = false;
    if (window.history.state && window.history.state.ileOverlay === panel.id) window.history.back();
  }
  panel.dispatchEvent(new CustomEvent("overlay:close", { bubbles: true, detail: { reason, opener: record.opener } }));
}

/* ---- Esc: an alert's is its safe answer ------------------------------------------------------------------------ */
function escapePanel(panel) {
  const safe = kindOf(panel) === "alert" ? panel.querySelector("[data-overlay-safe]") : null;
  if (safe && !safe.hasAttribute("data-overlay-close")) safe.click();
  else close(panel, { reason: "esc" });
}

/* ---- the scrim: one element under the topmost trapped panel — or under a menu shown as a phone sheet —, on that
        panel's clocks ------------------------------------------------------------------------------------------- */
const trapped = () => opened.filter((panel) => recordOf(panel).modal && !recordOf(panel).native);

/** What the scrim stands under: the topmost trapped panel, or a menu shown as a sheet opened above it. */
function scrimTop() {
  for (let index = opened.length - 1; index >= 0; index -= 1) {
    const panel = opened[index];
    const record = recordOf(panel);
    if ((record.modal && !record.native) || (kindOf(panel) === "popover" && asSheet(panel))) return panel;
  }
  return null;
}

function syncScrim() {
  const stack = trapped();
  const top = scrimTop();
  if (!top) {
    if (scrim) {
      scrim.toggleAttribute("data-instant", fromKeyboard());
      scrim.removeAttribute("data-open");
      scrim.style.removeProperty("--overlay-drag");
    }
    return;
  }
  makeScrim();
  // stacked trapped panels: each above the one before, the scrim right under the topmost — or, under a menu sheet
  // (in the top layer, above them all), over every trapped panel
  const base = zBase || 50;
  stack.forEach((panel, index) => panel.style.setProperty("z-index", String(base + 2 * index)));
  const under = stack.includes(top) ? stack.indexOf(top) : stack.length;
  scrim.style.setProperty("z-index", String(base + 2 * under - 1));
  // the scrim moves on the clocks of what the panel is now: a menu or a dialog on a phone, a drawer opened as a
  // sheet, leave as sheets
  const kind = kindOf(top);
  const asSheetNow = kind === "popover" || top.getAttribute("data-overlay-mode") === "sheet" || (PHONE.matches && /^(dialog|alert)$/.test(kind));
  scrim.setAttribute("data-kind", asSheetNow ? "sheet" : kind);
  scrim.toggleAttribute("data-instant", top.hasAttribute("data-instant"));
  scrim.setAttribute("data-open", "");
}

/** The scrim exists before it is needed — made at idle by initOverlays: an insertion under the body in the tap
    re-evaluates every :has() rule of the page (≈ 700 elements restyled on «Mes documents», NOTES «INP»). */
function makeScrim() {
  if (!zBase) zBase = parseInt(getComputedStyle(ROOT).getPropertyValue("--z-modal"), 10) || 50;
  if (scrim) return;
  scrim = document.createElement("div");
  scrim.className = "overlay-scrim";
  scrim.setAttribute("aria-hidden", "true");
  // A press on the scrim is the panel's it stands under, the WHOLE press — pointerdown to click: a menu sheet is
  // light-dismissed by the platform on the way up, before the click, so the scrim stays in the press's way until
  // that click (`data-held`) and the page is never reached (REVIEW M1: no field behind focused, no link followed).
  // Down and up on it, it closes a menu (light) or the topmost trapped panel — never an alert, never unsaved input.
  let pressed = null;
  let held = 0;
  const release = () => {
    window.clearTimeout(held);
    scrim.removeAttribute("data-held");
  };
  scrim.addEventListener("pointerdown", (event) => {
    pressed = event.target === scrim ? scrimTop() : null;
    if (!pressed) return;
    scrim.setAttribute("data-held", "");
    window.clearTimeout(held);
    held = window.setTimeout(release, 1000); // a press that never clicks (a long press) lets go of the page
  });
  // a press on a dim layer does not move the focus: the close gives it back where CONTRACT §4 says
  scrim.addEventListener("mousedown", (event) => event.preventDefault());
  scrim.addEventListener("pointercancel", release);
  scrim.addEventListener("click", (event) => {
    const panel = pressed;
    pressed = null;
    release();
    if (!panel || event.target !== scrim || !isOpen(panel)) return;
    if (kindOf(panel) === "popover") close(panel, { reason: "light" });
    else if (recordOf(panel).modal && kindOf(panel) !== "alert" && !panel.hasAttribute("data-overlay-dirty")) {
      close(panel, { reason: "scrim" });
    }
  });
  document.body.append(scrim);
}

/* ---- the page behind a trapped panel leaves the accessibility tree ------------------------------------------------ */
// showModal() takes the page out by its inertness; the trap (the INP rule) has none, and an engine prunes nothing for
// aria-modal alone (Chromium kept the banner, the bars, main and the footer: A11Y_PERF M2). So while a trapped panel
// is open, every element beside its way up to the body is aria-hidden — never inert: no rule selects aria-hidden, so
// nothing is re-styled and the INP rule's gain is kept. Written once the focus is in, taken back before it comes
// out: the focus never stands in a hidden subtree. An element hidden by its own markup is left as it is.
let hidden = new Set();
const SILENT = new Set(["SCRIPT", "STYLE", "TEMPLATE", "LINK", "META", "NOSCRIPT"]);

function syncHidden() {
  const stack = trapped();
  const top = stack[stack.length - 1];
  const next = new Set();
  if (top) {
    // the topmost trapped panel, and whatever opened above it, keep their way up to the body
    const way = new Set();
    opened.slice(opened.indexOf(top)).forEach((panel) => {
      for (let node = panel; node && node !== document.body; node = node.parentElement) way.add(node);
    });
    way.forEach((node) => {
      [...(node.parentElement ? node.parentElement.children : [])].forEach((sibling) => {
        if (way.has(sibling) || SILENT.has(sibling.tagName)) return;
        if (hidden.has(sibling) || !sibling.hasAttribute("aria-hidden")) next.add(sibling);
      });
    });
  }
  hidden.forEach((element) => next.has(element) || element.removeAttribute("aria-hidden"));
  next.forEach((element) => hidden.has(element) || element.setAttribute("aria-hidden", "true"));
  hidden = next;
}

/* ---- the panel's own listeners ------------------------------------------------------------------------------------ */
function wirePanel(panel) {
  if (wired.has(panel)) return;
  wired.add(panel);
  const kind = kindOf(panel);
  const record = recordOf(panel);

  if (panel.hasAttribute("popover")) {
    panel.addEventListener("beforetoggle", (event) => {
      if (event.newState === "open") {
        window.clearTimeout(record.inertTimer);
        panel.inert = false;
        if (!record.opening) {
          // opened by its trigger without this module's click (or by another script): the same preparation
          const trigger = openersOf(panel)[0] || null;
          record.opener = record.opener && record.opener.isConnected ? record.opener : trigger;
          chooseSide(panel, record.opener);
        }
      } else {
        settle(panel);
      }
    });
    panel.addEventListener("toggle", (event) => {
      if (event.newState !== "open" || !popoverOpen(panel)) return;
      if (!record.open) {
        adopt(panel);
        syncScrim();
        placeByScript(panel);
        if (!panel.contains(document.activeElement)) focus(focusTarget(panel));
      }
    });
  } else {
    // Esc on a modal dialog: the platform's `cancel`, taken here so that the close is this module's — and an
    // alert's Esc is its safe answer
    panel.addEventListener("cancel", (event) => {
      event.preventDefault();
      escapePanel(panel);
    });
    panel.addEventListener("close", () => settle(panel));
    // a dialog opened by another script (dialog toggle events, where they exist)
    panel.addEventListener("toggle", (event) => {
      if (event.newState === "open" && panel.open) adopt(panel);
    });
    // a native modal's ::backdrop is the dialog's own box: its press (overlay/extras.js), wired at idle
    if (panel.getAttribute("data-overlay-modal") === "native") whenIdle(() => withExtras((parts) => parts.wireBackdrop(panel, record)));
    // unsaved input keeps the scrim and the grip from dismissing it
    panel.addEventListener("input", () => panel.setAttribute("data-overlay-dirty", ""));
    // the grip (overlay/extras.js), wired at idle: a drag needs an open sheet, so a person's act — «Fermer» is there
    if (kind === "sheet" || panel.querySelector("[data-overlay-grip]")) {
      whenIdle(() => withExtras((parts) => parts.wireGrip(panel, record)));
    }
  }

  panel.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && panel.hasAttribute("popover")) {
      record.reason = "esc"; // the platform closes it; settle() says why
      return;
    }
    if (event.key === "Tab" && record.modal) {
      // the trap: Tab and Shift+Tab wrap inside the panel (the focusin guard brings back a focus sent outside)
      const list = tabbables(panel);
      if (!list.length) {
        event.preventDefault();
        return;
      }
      const first = list[0];
      const last = list[list.length - 1];
      const active = document.activeElement;
      if (event.shiftKey && (active === first || !panel.contains(active) || active === panel)) {
        event.preventDefault();
        focus(last);
      } else if (!event.shiftKey && (active === last || !panel.contains(active))) {
        event.preventDefault();
        focus(first);
      }
      return;
    }
    if (kind === "popover" && ["ArrowDown", "ArrowUp", "Home", "End"].includes(event.key)) {
      const list = tabbables(panel);
      if (!list.length) return;
      const at = list.indexOf(document.activeElement);
      let next = 0;
      if (event.key === "ArrowDown") next = (at + 1) % list.length;
      else if (event.key === "ArrowUp") next = at <= 0 ? list.length - 1 : at - 1;
      else if (event.key === "End") next = list.length - 1;
      event.preventDefault();
      focus(list[next]);
    }
  });

  if (kind === "popover") {
    // S-7: a menu closes when the focus leaves it — for an element outside both the menu and its trigger
    panel.addEventListener("focusout", (event) => {
      const next = event.relatedTarget;
      if (!record.open || !next || panel.contains(next) || (record.opener && record.opener.contains(next))) return;
      close(panel, { reason: "focus", focus: false });
    });
    // a choice closes the menu (a link leaves the page, a button acts); the focus goes back to the trigger
    panel.addEventListener("click", (event) => {
      const choice = event.target.closest("a[href], button, [role='menuitem']");
      if (!choice || !panel.contains(choice) || choice.hasAttribute("data-overlay-keep")) return;
      if (choice.matches("[aria-haspopup], [popovertarget]")) return;
      close(panel, { reason: "choice" });
    });
  } else if (kind === "drawer" || kind === "sheet") {
    // a link in a drawer or a sheet takes the person elsewhere: the panel goes, the link does the rest
    panel.addEventListener("click", (event) => {
      const link = event.target.closest("a[href]");
      if (!link || !panel.contains(link) || link.hasAttribute("data-overlay-close") || link.hasAttribute("data-overlay-keep")) return;
      if (link.target && link.target !== "_self") return;
      close(panel, { reason: "link", focus: false });
    });
  }
}

/* ---- the tooltip: Esc and a press put it away; the top-layer tip for a control inside a clipping ancestor ------- */
let tip = null;
let tipFor = null;
let tipTimer = 0;
let hideTimer = 0;
let warmUntil = 0;

function tipElement() {
  if (tip) return tip;
  tip = document.createElement("div");
  tip.className = "tooltip";
  tip.setAttribute("popover", "manual");
  tip.setAttribute("aria-hidden", "true");
  tip.addEventListener("pointerenter", () => window.clearTimeout(hideTimer));
  tip.addEventListener("pointerleave", (event) => {
    if (!tipFor || !tipFor.contains(event.relatedTarget)) hideTip();
  });
  document.body.append(tip);
  return tip;
}

function placeTip(control) {
  const box = control.getBoundingClientRect();
  const width = tip.offsetWidth;
  const height = tip.offsetHeight;
  const viewWidth = ROOT.clientWidth;
  const viewHeight = ROOT.clientHeight;
  const side = control.getAttribute("data-tip-side") || "block-start";
  const rtl = getComputedStyle(control).direction === "rtl";
  let left;
  let top;
  if (side === "inline-end" || side === "inline-start") {
    // beside the control, beyond the edge it names: in Arabic the inline end is on the left — and beyond the edge
    // of the ancestor `data-tip-beyond` names, if any (the rail's: never over the rail's next control)
    const toRight = (side === "inline-end") !== rtl;
    const beyond = control.getAttribute("data-tip-beyond");
    const edge = (beyond && control.closest(beyond)) || control;
    const outer = edge.getBoundingClientRect();
    const right = Math.max(box.right, outer.right);
    const leftEdge = Math.min(box.left, outer.left);
    left = toRight ? right + 6 : leftEdge - 6 - width;
    if (left < EDGE || left + width > viewWidth - EDGE) left = toRight ? leftEdge - 6 - width : right + 6;
    top = box.top + box.height / 2 - height / 2;
  } else {
    left = box.left + box.width / 2 - width / 2;
    top = side === "block-end" ? box.bottom + 6 : box.top - 6 - height;
    if (top < EDGE || top + height > viewHeight - EDGE) top = side === "block-end" ? box.top - 6 - height : box.bottom + 6;
  }
  tip.style.left = `${Math.round(Math.min(Math.max(left, EDGE), Math.max(EDGE, viewWidth - width - EDGE)))}px`;
  tip.style.top = `${Math.round(Math.min(Math.max(top, EDGE), Math.max(EDGE, viewHeight - height - EDGE)))}px`;
}

/** Is the control's middle on screen and its own — no scroller's edge, no bar over it? */
function inView(control) {
  const box = control.getBoundingClientRect();
  const hit = document.elementFromPoint(box.left + box.width / 2, box.top + box.height / 2);
  return Boolean(hit && control.contains(hit));
}

/** A control whose overlay is open names nothing: its panel is there (a popover's trigger, a dialog's opener). */
function panelOpenFor(control) {
  const id = control.getAttribute("popovertarget") || control.getAttribute("aria-controls");
  const panel = id ? document.getElementById(id) : null;
  return Boolean(panel && kindOf(panel) && isOpen(panel));
}

function showTip(control, instant) {
  // the words: the control's name, or `data-tip-label` where the name is the control's own content (a word the
  // control draws, or cuts, beside its glyph)
  const label = control.getAttribute("data-tip-label") || control.getAttribute("aria-label");
  if (!label || PHONE.matches || control.hasAttribute("data-tip-off") || panelOpenFor(control)) return;
  // the page may refuse a tip: a cancelable `overlay:tip` on the control (the rail's, while its word is beside the glyph)
  if (!control.dispatchEvent(new CustomEvent("overlay:tip", { bubbles: true, cancelable: true }))) return;
  window.clearTimeout(tipTimer);
  window.clearTimeout(hideTimer);
  tipElement();
  tip.textContent = label;
  tip.toggleAttribute("data-instant", Boolean(instant));
  if (!popoverOpen(tip)) tip.showPopover();
  placeTip(control);
  tipFor = control;
}

function hideTip() {
  window.clearTimeout(tipTimer);
  window.clearTimeout(hideTimer);
  if (tip && popoverOpen(tip)) {
    tip.hidePopover();
    warmUntil = performance.now() + millis(ROOT, "--tooltip-delay", 400);
  }
  tipFor = null;
}

/** Esc puts every visible tooltip away until the pointer leaves its control or the focus does. */
function dismissTips() {
  if (tip && popoverOpen(tip)) {
    if (tipFor) tipFor.setAttribute("data-tip-off", "");
    hideTip();
  }
  document.querySelectorAll("[data-tip]:not([data-tip='layer']):is(:hover, :focus-visible)").forEach((control) => {
    control.setAttribute("data-tip-off", "");
  });
}

/* ---- the disclosure menus: a <details data-dropdown> opens and closes natively; the system adds the rest ------ */
const summaryOf = (details) => details.querySelector(":scope > summary");
const ownedDisclosures = () => [...document.querySelectorAll(`${DISCLOSURE}[open]`)].filter((details) => wired.has(details));

function wireDisclosure(details) {
  if (wired.has(details)) return;
  wired.add(details);
  // the page's main.js keeps a fallback for the pages that do not load this module yet: it steps aside for this one
  details.setAttribute("data-dropdown", "overlay");
  const summary = summaryOf(details);
  if (summary) summary.setAttribute("aria-expanded", details.open ? "true" : "false");
  details.addEventListener("toggle", () => {
    if (summary) summary.setAttribute("aria-expanded", details.open ? "true" : "false");
    // one open at a time
    if (details.open) ownedDisclosures().forEach((other) => other !== details && (other.open = false));
  });
  // the focus leaving it puts it away (S-7)
  details.addEventListener("focusout", (event) => {
    if (details.open && !details.contains(event.relatedTarget)) details.open = false;
  });
}

/* ---- the document's listeners: delegated, once ------------------------------------------------------------------ */
function wireDocument() {
  if (documentWired) return;
  documentWired = true;

  document.addEventListener("click", (event) => {
    if (!(event.target instanceof Element)) return;
    // a press outside an open disclosure menu puts it away
    ownedDisclosures().forEach((details) => !details.contains(event.target) && (details.open = false));
    // an opener: a link to its panel (the no-script path) or a button
    const opener = event.target.closest("[data-overlay-open]");
    if (opener) {
      const id = opener.getAttribute("data-overlay-open") || (opener.getAttribute("href") || "").replace(/^#/, "");
      const panel = id ? document.getElementById(id) : null;
      if (kindOf(panel)) {
        event.preventDefault();
        if (kindOf(panel) === "popover") toggle(panel, { opener });
        else open(panel, { opener });
        return;
      }
    }
    // a menu's native trigger: opened here, in this task, with its side, its anchor and its focus
    const trigger = event.target.closest("[popovertarget]");
    if (trigger) {
      const panel = document.getElementById(trigger.getAttribute("popovertarget"));
      if (kindOf(panel) === "popover") {
        event.preventDefault();
        const action = trigger.getAttribute("popovertargetaction") || "toggle";
        const closingPress = recordOf(panel).closingPress === trigger;
        recordOf(panel).closingPress = null;
        if (isOpen(panel)) {
          if (action !== "show") close(panel, { reason: "close" });
        } else if (action !== "hide" && !closingPress) {
          open(panel, { opener: trigger });
        }
        return;
      }
    }
    // «Fermer» — and every [data-overlay-close] inside a panel
    const closer = event.target.closest("[data-overlay-close]");
    if (closer) {
      const panel = closer.closest("[data-overlay]");
      if (kindOf(panel) && isOpen(panel)) {
        event.preventDefault();
        close(panel, { reason: "close" });
      }
    }
  });

  // a press on the trigger of an open menu: the light dismiss closes it on the way down, so its click must not
  // open it again (where the platform does not count the trigger as part of the menu)
  document.addEventListener(
    "pointerdown",
    (event) => {
      if (!(event.target instanceof Element)) return;
      const trigger = event.target.closest("[popovertarget]");
      const panel = trigger ? document.getElementById(trigger.getAttribute("popovertarget")) : null;
      if (kindOf(panel) === "popover") recordOf(panel).closingPress = isOpen(panel) ? trigger : null;
      // a press on a control puts its tooltip away until the pointer leaves it
      const tipped = event.target.closest("[data-tip]");
      if (tipped) {
        tipped.setAttribute("data-tip-off", "");
        if (tipped === tipFor) hideTip();
      }
    },
    true,
  );

  // Space presses a link that plays a button (an opener, «Fermer»)
  document.addEventListener("keydown", (event) => {
    if (event.key === " " && event.target instanceof HTMLAnchorElement && event.target.matches("[data-overlay-open], [data-overlay-close]")) {
      event.preventDefault();
      event.target.click();
    }
  });

  // Esc: every visible tooltip goes (WCAG 1.4.13: without moving the pointer or the focus) — the key is not taken from
  // anybody else; an open disclosure menu that holds the focus goes next, and alone — its summary takes the focus, and
  // the panel it stands in stays (the key's default is prevented: no close request reaches the dialog); else a
  // non-modal drawer closes, the platform having no Esc for it
  document.addEventListener(
    "keydown",
    (event) => {
      if (event.key !== "Escape") return;
      dismissTips();
      const disclosure = event.target instanceof Element ? event.target.closest(`${DISCLOSURE}[open]`) : null;
      if (disclosure && wired.has(disclosure) && !event.defaultPrevented) {
        event.preventDefault();
        disclosure.open = false;
        focus(summaryOf(disclosure));
        return;
      }
      const top = opened[opened.length - 1];
      if (top && !top.hasAttribute("popover") && !top.matches(":modal") && !event.defaultPrevented) {
        event.preventDefault(); // the close request is this module's: an alert answers safe
        escapePanel(top);
      }
    },
    true,
  );

  // the top-layer tooltip, under a fine pointer: the wait, then the fade; a warm neighbour at once
  document.addEventListener("pointerover", (event) => {
    if (event.pointerType !== "mouse" || !POINTER.matches || !(event.target instanceof Element)) return;
    const control = event.target.closest("[data-tip='layer']");
    if (!control || control === tipFor) {
      if (control) window.clearTimeout(hideTimer);
      return;
    }
    window.clearTimeout(tipTimer);
    window.clearTimeout(hideTimer);
    if (performance.now() < warmUntil || (tip && popoverOpen(tip))) showTip(control, true);
    else tipTimer = window.setTimeout(() => showTip(control, false), millis(ROOT, "--tooltip-delay", 400));
  });
  document.addEventListener("pointerout", (event) => {
    if (!(event.target instanceof Element)) return;
    const control = event.target.closest("[data-tip]");
    if (!control || control.contains(event.relatedTarget)) return;
    control.removeAttribute("data-tip-off");
    if (control.getAttribute("data-tip") !== "layer") return;
    window.clearTimeout(tipTimer);
    if (control === tipFor && !(tip && tip.contains(event.relatedTarget))) {
      hideTimer = window.setTimeout(hideTip, 120); // the way across to the tip (WCAG 1.4.13: hoverable)
    }
  });
  document.addEventListener("focusin", (event) => {
    const panel = trapped().pop();
    if (panel && opened[opened.length - 1] === panel && event.target instanceof Element && !panel.contains(event.target)) {
      focus(tabbables(panel)[0] || titleOf(panel) || panel);
      return;
    }
    const control = event.target instanceof Element ? event.target.closest("[data-tip='layer']") : null;
    if (control && control === event.target && control.matches(":focus-visible")) showTip(control, true);
  });
  document.addEventListener("focusout", (event) => {
    if (!(event.target instanceof Element)) return;
    const control = event.target.closest("[data-tip]");
    if (!control) return;
    if (!control.matches(":hover")) control.removeAttribute("data-tip-off"); // a press's «off» lasts while the pointer stays
    if (control === tipFor) hideTip();
  });
  // a scroll moves the control under its tip — the focus's own scroll of the compact rail's list among them
  // (A11Y_PERF M3): the tip follows while its control keeps the keyboard's focus or the pointer and stands in view;
  // otherwise it goes
  window.addEventListener(
    "scroll",
    () => {
      if (!tipFor) return;
      if (tipFor.matches(":focus-visible, :hover") && inView(tipFor)) placeTip(tipFor);
      else hideTip();
    },
    { capture: true, passive: true },
  );

  // a window resized past the phone width while a menu is open puts its place in order, and its scrim
  PHONE.addEventListener("change", () => {
    opened.forEach((panel) => {
      if (panel.getAttribute("data-overlay") !== "popover") return;
      if (asSheet(panel)) {
        panel.removeAttribute("data-overlay-side");
        panel.style.removeProperty("left");
        panel.style.removeProperty("top");
      } else {
        placeByScript(panel);
      }
    });
    syncScrim();
  });
}

/* ---- the openers --------------------------------------------------------------------------------------------- */
function wireOpener(opener) {
  if (wired.has(opener)) return;
  const id = opener.getAttribute("data-overlay-open") || (opener.getAttribute("href") || "").replace(/^#/, "");
  const panel = id ? document.getElementById(id) : null;
  const kind = kindOf(panel);
  if (!kind) return;
  wired.add(opener);
  if (opener instanceof HTMLAnchorElement) opener.setAttribute("role", "button");
  opener.setAttribute("aria-controls", id);
  opener.setAttribute("aria-expanded", isOpen(panel) ? "true" : "false");
  if (kind !== "popover") opener.setAttribute("aria-haspopup", "dialog");
}

/**
 * Wire every overlay hook inside `root` (default: the document). Idempotent: call it again after inserting markup.
 */
export function initOverlays(root = document) {
  wireDocument();
  const scope = root.querySelectorAll ? root : document;
  if (root.nodeType === 1 && kindOf(root)) wirePanel(root);
  scope.querySelectorAll("[data-overlay]").forEach((panel) => {
    if (kindOf(panel)) wirePanel(panel);
  });
  scope.querySelectorAll("[data-overlay-open]").forEach(wireOpener);
  scope.querySelectorAll("[data-overlay-close]").forEach((closer) => {
    if (closer instanceof HTMLAnchorElement) closer.setAttribute("role", "button");
  });
  scope.querySelectorAll("[popovertarget]").forEach((trigger) => {
    const panel = document.getElementById(trigger.getAttribute("popovertarget"));
    if (kindOf(panel) === "popover" && !trigger.hasAttribute("aria-expanded")) trigger.setAttribute("aria-expanded", "false");
  });
  scope.querySelectorAll(DISCLOSURE).forEach(wireDisclosure);
  // without anchor positioning a menu is placed by the rarer parts: here before the first opening
  if (!ANCHORED && scope.querySelector("[data-overlay='popover']")) loadExtras();
  whenIdle(() => {
    measure(root.querySelectorAll ? root : document);
    if (document.querySelector("dialog[data-overlay], [data-overlay='popover']:not([data-overlay-phone='none'])")) makeScrim();
    if (scope.querySelector("[data-overlay-history], [data-overlay-grip], [data-overlay-modal='native'], dialog[data-overlay] .overlay__body")) loadExtras();
  });
}

initOverlays();
