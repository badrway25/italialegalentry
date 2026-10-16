/**
 * The console shell (docs/design-v5/V5_4_EXECUTION_PLAN.md §1.18 D06, §3.5 item 3; W3-A): the rail that
 * folds and remembers it, the word of a glyph that stands alone, its keyboard model, and the mobile drawer.
 *
 * No animation library here: what moves is the rail's width (a CSS transition on a token, on the
 * person's own act) and the overlays (the overlay system's transitions, static/css/v5/overlays.css). The
 * current page is drawn by CSS on `aria-current` («il lume»); a page is a full navigation, so there is
 * nothing for it to travel between. Nothing moves at load.
 *
 * The overlays of every console page — the drawer, the account popover, the row menu, the disclosures, the
 * tooltips — are the overlay system's (static/js/src/overlay.js, V5.4 plan §1.14; W2-A), imported here: it
 * wires the page's hooks when it loads, and this module adds only what is the shell's own.
 *
 *   rail state      `data-rail` on <body>, "open" or "closed". static/js/rail-pref.js writes it before
 *                   the first frame — the choice stored in localStorage under `ile.rail`, else open
 *                   from 80rem and compact below; this module keeps the control's `aria-expanded` in
 *                   step, stores the choice on every press (try/catch: private windows, blocked
 *                   storage — the console must work without it) and follows the width while no choice
 *                   is stored. Without script the stylesheet keeps the rail open.
 *   rail words      a glyph without its word (the compact rail's entries, the foot's controls) shows it
 *                   beside itself on hover and on keyboard focus: the overlay system's one top-layer
 *                   tip, the rail saying which controls and when (`overlay:tip`)
 *   rail keyboard   ArrowUp/ArrowDown move between entries, Home/End to the first/last
 *   drawer          a modal drawer of the overlay system. «Menu» — once, in the bottom bar — is a link
 *                   to it (`data-overlay-open`; without script the system's stylesheet shows the drawer
 *                   it points at); the system makes it the button of a modal: the role, Enter and
 *                   Space, aria-expanded and aria-haspopup, the trap, Esc and the scrim, the focus on
 *                   the page one is on and back to «Menu» on close. Here: a window widened past 64rem
 *                   puts it away.
 *
 * The one frame wait (the rail's width transitions only once the first frame is painted) goes
 * through motion.js's gate, like every frame wait of the project (V5.4 plan §1.5, W1-D).
 */
import { afterPaint } from "./motion.js";
import { close, isOpen } from "./overlay.js";

const KEY = "ile.rail";
const WIDE = window.matchMedia("(min-width: 80rem)");

/* 1. The rail — the <nav>, not the <body> that carries the state under the same attribute. */
const rail = document.querySelector("nav[data-rail]");
const toggle = document.querySelector("[data-rail-toggle]");
if (rail && toggle) {
  const read = () => {
    try {
      return localStorage.getItem(KEY);
    } catch {
      return null;
    }
  };
  const write = (state) => {
    try {
      localStorage.setItem(KEY, state);
    } catch {
      /* storage refused: the choice lasts for the page, which is still correct */
    }
  };
  const apply = (state, persist) => {
    document.body.dataset.rail = state;
    toggle.setAttribute("aria-expanded", state === "open" ? "true" : "false");
    if (persist) write(state);
  };
  const stored = read();
  if (stored === "open" || stored === "closed") apply(stored, false);
  else apply(WIDE.matches ? "open" : "closed", false);
  // The width transitions only after the first frame (`is-ready`, v5/_shell.css §6): never at load.
  afterPaint().then(() => document.body.classList.add("is-ready"));

  toggle.addEventListener("click", () => {
    apply(document.body.dataset.rail === "open" ? "closed" : "open", true);
  });

  // No stored preference: follow the width, as rail-pref.js decided it at load.
  WIDE.addEventListener("change", (event) => {
    if (read() === null) apply(event.matches ? "open" : "closed", false);
  });

  /* The current page stays in view: on a short screen the list scrolls under the pinned foot, and a
     page near its end would otherwise be marked out of sight. Placed at once — a scroll offset, not
     a movement. */
  const scroller = rail.querySelector("[data-rail-scroll]");
  const current = scroller ? scroller.querySelector("[aria-current='page']") : null;
  if (scroller && current && scroller.scrollHeight > scroller.clientHeight) {
    const view = scroller.getBoundingClientRect();
    const row = current.getBoundingClientRect();
    if (row.bottom > view.bottom) scroller.scrollTop += row.bottom - view.bottom + 8;
    else if (row.top < view.top) scroller.scrollTop -= view.top - row.top + 8;
  }

  /* The word of a glyph that stands alone — the overlay system's one top-layer tip (W2-A; plan §1.14, O11),
     which the list's scroll edge cannot clip: beside the control, beyond the rail's own edge — never over the
     rail, so the pointer may rest on the word (WCAG 1.4.13) without it lying over the foot's next control, and
     in Arabic on the rail's left, the inline end there —, after the tooltip's 400 ms under the pointer and at
     once under the keyboard's focus; Esc (wherever the focus is), a press, the pointer or the focus leaving put
     it away. The rail says which controls have a word (`data-rail-tip`, the word in `data-label`) and when:
     `data-rail-tip="always"` — a control that never shows its word (sign-out, the rail's own control) —,
     otherwise only while the rail is compact or the word is cut (a long name, a long audience): open, the
     word is beside the glyph, and the rail refuses the tip. */
  const clipped = (item) =>
    [...item.querySelectorAll(".rail__who-name, .rail__who-role, .rail__space")].some(
      (word) => word.scrollWidth > word.clientWidth,
    );
  rail.querySelectorAll("[data-rail-tip]").forEach((item) => {
    item.setAttribute("data-tip", "layer");
    item.setAttribute("data-tip-side", "inline-end");
    item.setAttribute("data-tip-beyond", "nav[data-rail]");
    item.setAttribute("data-tip-label", item.dataset.label || "");
  });
  rail.addEventListener("overlay:tip", (event) => {
    const item = event.target.closest("[data-rail-tip]");
    if (item && item.dataset.railTip !== "always" && document.body.dataset.rail !== "closed" && !clipped(item)) {
      event.preventDefault();
    }
  });
}

/* The keyboard model — ArrowUp/ArrowDown, Home, End — on every rail: the fixed one and the
   drawer's copy (gate B review, correction 10: the arrows were inert in the drawer). */
document.querySelectorAll(".rail").forEach((element) => {
  const entries = [...element.querySelectorAll("[data-rail-item]")];
  if (!entries.length) return;
  element.addEventListener("keydown", (event) => {
    const index = entries.indexOf(document.activeElement);
    if (index < 0) return;
    let next = null;
    if (event.key === "ArrowDown") next = entries[(index + 1) % entries.length];
    else if (event.key === "ArrowUp") next = entries[(index - 1 + entries.length) % entries.length];
    else if (event.key === "Home") next = entries[0];
    else if (event.key === "End") next = entries[entries.length - 1];
    if (next) {
      event.preventDefault();
      next.focus();
    }
  });
});

/* 2. The register's search (design V4 §3.5.3): filters the rows shown by their title, in the
      page, as the person types; the state filter stays in the URL. Nothing is sent anywhere. A register read
      again by the preview drawer (`documents:refreshed`) has its search wired again. */
const bindSearch = (root) => root.querySelectorAll("[data-doc-search]").forEach((input) => {
  if (input.dataset.docSearchReady !== undefined) return;
  input.dataset.docSearchReady = "";
  const list = document.getElementById(input.dataset.docSearch);
  const none = document.querySelector(`[data-doc-search-empty="${input.dataset.docSearch}"]`);
  if (!list) return;
  const status = document.querySelector(`[data-doc-search-status="${input.dataset.docSearch}"]`);
  const count = status ? status.querySelector("[data-doc-search-count]") : null;
  const rows = [...list.querySelectorAll(".doc-row")];
  // «Mes pièces» V5 (W3-C): the rows stand in three groups; a group whose rows are all filtered out goes with them.
  const groups = [...list.querySelectorAll(".doc-group")];
  const fold = (text) => text.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase();
  let announce = 0;
  input.addEventListener("input", () => {
    const needle = fold(input.value.trim());
    let shown = 0;
    rows.forEach((row) => {
      const title = row.querySelector(".doc-row__title");
      const hit = !needle || fold(title ? title.textContent : "").includes(needle);
      row.hidden = !hit;
      if (hit) shown += 1;
    });
    groups.forEach((group) => {
      group.hidden = !group.querySelector(".doc-row:not([hidden])");
    });
    if (none) none.hidden = shown > 0;
    // The screen reader hears the count once the typing pauses (gate C review, correction 8).
    if (count && status) {
      window.clearTimeout(announce);
      announce = window.setTimeout(() => {
        count.textContent = needle ? `${status.dataset.docSearchLabel} ${shown} / ${rows.length}` : "";
      }, 400);
    }
  });
});
bindSearch(document);
document.addEventListener("documents:refreshed", (event) => bindSearch(event.target));

/* 2b. The preview drawer and the filter's sheet (design V5, W3-C; plan §1.14; DOCUMENT_WORKSPACE.md §12, §13), on
      the overlay system: the sheet is overlay.js's own (a link to it, data-overlay-open); the drawer's module —
      the row unfolded beside the register, a sheet on a phone — is imported where the register draws it. */
if (document.querySelector("[data-piece-drawer]")) {
  import("./piece-drawer.js").then(({ initPieceDrawer }) => initPieceDrawer());
}

/* 2d. The Dépôt (design V5, W3-C; DOCUMENT_WORKSPACE.md §11): where a page draws one — a piece's page, the upload
      page — its module is imported, never before; without it the Dépôt is the browser's own form. */
if (document.querySelector("[data-depot-form]")) {
  import("./depot.js").then(({ initDepots }) => initDepots(document));
}

/* 2e. The deletion of a loose file asks first (design V5, W3-C; REVIEW m4): a row's «Supprimer» opens the overlay
      system's alert dialog (its `data-overlay-open`; without script it posts its form at once). Here only what the
      dialog needs of the row that asked: the file's name in the question, and its «Supprimer» pointed at that row's
      form — a submit of that form, the same POST. */
const deletion = document.querySelector("[data-doc-delete-go]");
if (deletion) {
  deletion.closest("[data-overlay]").addEventListener("overlay:open", (event) => {
    const form = event.detail && event.detail.opener ? event.detail.opener.form : null;
    if (!form || !form.id) return;
    const name = event.currentTarget.querySelector("[data-doc-delete-name]");
    if (name) name.textContent = form.dataset.docDelete || "";
    deletion.setAttribute("form", form.id);
  });
}

/* 2c. The context bar (design V4 §3.6.1): the case file's header, once scrolled past, becomes a
      compact glass bar under the console bar — title, chip, action. Shown by a class; the bar is
      in the markup, hidden to assistive technology (its facts are the header's). */
const ctx = document.querySelector("[data-ctx]");
const ctxBar = document.querySelector("[data-ctx-bar]");
if (ctx && ctxBar && "IntersectionObserver" in window) {
  new IntersectionObserver(
    ([entry]) => {
      const on = !entry.isIntersecting && entry.boundingClientRect.top < 0;
      ctxBar.classList.toggle("is-on", on);
      // The sticky heads below (the tables) sit under the bar while it is on.
      document.body.classList.toggle("has-ctx-bar", on);
    },
    { threshold: 0 },
  ).observe(ctx);
}

/* 3. The drawer — a modal drawer of the overlay system (data-overlay="drawer", from the reading edge). «Menu»
      and the drawer's close control are links (`#console-drawer`, `#main-content`): without script they still
      lead somewhere, and they say what they are. With the system they are buttons — the role comes with the
      behaviour — Space presses them as Enter does, nothing is added to the address, and the focus goes to the
      page one is on (the system's «current entry») and back to «Menu».
      The drawer — and the top bar's account popover — belong to the widths that draw the top and bottom bars: a
      window widened past 64rem puts them away, and a focus that was in one goes to the rail, which stands at the
      reading edge again (neither «Menu» nor the bar's account is drawn there). */
const phoneOnly = [document.querySelector("[data-console-drawer]"), document.getElementById("console-account")].filter(Boolean);
if (phoneOnly.length) {
  window.matchMedia("(min-width: 64rem)").addEventListener("change", (event) => {
    if (!event.matches) return;
    const rail = document.getElementById("console-rail") || undefined;
    phoneOnly.forEach((panel) => isOpen(panel) && close(panel, { focus: rail }));
  });
}
