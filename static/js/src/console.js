/**
 * The console shell (docs/design-v4/CREATIVE_DIRECTION.md §3.9): the rail that collapses and
 * remembers it, its keyboard model, and the mobile drawer.
 *
 * No animation library here: what moves is the rail's width (a CSS transition on a token) and
 * the drawer (a CSS animation on `[open]`). The active entry's indicator is drawn by CSS on
 * `aria-current`; a page is a full navigation, so there is nothing for it to travel between.
 *
 *   rail collapse   persisted in localStorage under `ile.rail` (try/catch: private windows,
 *                   blocked storage — the console must work without it); default: open from
 *                   90rem, collapsed below, as the stylesheet says without the attribute
 *   rail keyboard   ArrowUp/ArrowDown move between entries, Home/End to the first/last
 *   drawer          a native <dialog>: showModal() traps focus and Esc closes; the two «Menu»
 *                   buttons (top bar, bottom bar) carry aria-expanded
 */

const KEY = "ile.rail";
const WIDE = window.matchMedia("(min-width: 90rem)");

/* 1. The rail. */
const rail = document.querySelector("[data-rail]");
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
  // The width transitions only after the first frame (console.css `is-ready`): never at load.
  window.requestAnimationFrame(() => window.requestAnimationFrame(() => document.body.classList.add("is-ready")));

  toggle.addEventListener("click", () => {
    apply(document.body.dataset.rail === "open" ? "closed" : "open", true);
  });

  // No stored preference: follow the width, as the stylesheet would without the attribute.
  WIDE.addEventListener("change", (event) => {
    if (read() === null) apply(event.matches ? "open" : "closed", false);
  });

  const items = [...rail.querySelectorAll("[data-rail-item]")];

  /* The tooltip of the collapsed rail: one fixed element beside the entry under the pointer or
     the focus (the rail's scroll area would clip a pseudo-element). Only while collapsed: open,
     the label is beside the glyph. */
  const tip = document.createElement("span");
  tip.className = "rail__tip";
  tip.setAttribute("aria-hidden", "true");
  document.body.append(tip);
  /* Physical sides on purpose: in RTL the rail is on the right and the tip goes on the item's
     LEFT — which is inline-END there, the opposite of what a logical property spelt for LTR does
     (gate B review, correction 2: the tip sat at x 78 with the item at x 1374). */
  const showTip = (item) => {
    if (document.body.dataset.rail !== "closed") return;
    const box = item.getBoundingClientRect();
    const rtl = document.documentElement.dir === "rtl";
    tip.textContent = item.dataset.label || "";
    tip.style.top = `${Math.round(box.top + box.height / 2)}px`;
    tip.style.transform = "translateY(-50%)";
    if (rtl) {
      tip.style.left = "auto";
      tip.style.right = `${Math.round(window.innerWidth - box.left + 12)}px`;
    } else {
      tip.style.right = "auto";
      tip.style.left = `${Math.round(box.right + 12)}px`;
    }
    tip.classList.add("is-on");
  };
  let tipTimer = 0;
  const hideTip = () => {
    window.clearTimeout(tipTimer);
    tip.classList.remove("is-on");
  };
  items.forEach((item) => {
    // The pointer waits the tooltip's 400 ms (DS §7.1); the keyboard focus does not wait.
    item.addEventListener("pointerenter", () => {
      window.clearTimeout(tipTimer);
      tipTimer = window.setTimeout(() => showTip(item), 400);
    });
    item.addEventListener("pointerleave", hideTip);
    item.addEventListener("focus", () => showTip(item));
    item.addEventListener("blur", hideTip);
  });
  toggle.addEventListener("click", hideTip);
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
      page, as the person types; the state filter stays in the URL. Nothing is sent anywhere. */
document.querySelectorAll("[data-doc-search]").forEach((input) => {
  const list = document.getElementById(input.dataset.docSearch);
  const none = document.querySelector(`[data-doc-search-empty="${input.dataset.docSearch}"]`);
  if (!list) return;
  const status = document.querySelector(`[data-doc-search-status="${input.dataset.docSearch}"]`);
  const count = status ? status.querySelector("[data-doc-search-count]") : null;
  const rows = [...list.querySelectorAll(".doc-row")];
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

/* 2b. The row menu (design V4 §3.5.4): a native popover with `margin: 0` lands at the viewport's
      origin unless it is placed. Placed when it opens, beside its button, on the reading edge of
      the row (CSSOM only — no style attribute); above the button when the viewport ends first. */
document.querySelectorAll(".doc-menu[popover]").forEach((menu) => {
  const button = document.querySelector(`[popovertarget="${menu.id}"]`);
  if (!button) return;
  menu.addEventListener("toggle", (event) => {
    if (event.newState !== "open") return;
    const box = button.getBoundingClientRect();
    const rtl = document.documentElement.dir === "rtl";
    const below = box.bottom + 4;
    const top = below + menu.offsetHeight > window.innerHeight ? Math.max(8, box.top - 4 - menu.offsetHeight) : below;
    menu.style.top = `${Math.round(top)}px`;
    menu.style.bottom = "auto";
    if (rtl) {
      menu.style.left = `${Math.round(box.left)}px`;
      menu.style.right = "auto";
    } else {
      menu.style.right = `${Math.round(window.innerWidth - box.right)}px`;
      menu.style.left = "auto";
    }
  });
});

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

/* 3. The drawer. */
const drawer = document.querySelector("[data-console-drawer]");
if (drawer && typeof drawer.showModal === "function") {
  const openers = [...document.querySelectorAll("[data-console-menu]")];
  const setExpanded = (open) => openers.forEach((button) => button.setAttribute("aria-expanded", open ? "true" : "false"));
  let lastOpener = null;
  openers.forEach((button) => {
    button.addEventListener("click", () => {
      lastOpener = button;
      drawer.showModal();
      setExpanded(true);
      const current = drawer.querySelector("[aria-current='page']") || drawer.querySelector("[data-rail-item]");
      if (current) current.focus();
    });
  });
  drawer.querySelectorAll("[data-console-close]").forEach((button) => button.addEventListener("click", () => drawer.close()));
  // A click on the backdrop lands on the dialog element itself, not on its content.
  drawer.addEventListener("click", (event) => {
    if (event.target === drawer) drawer.close();
  });
  drawer.addEventListener("close", () => {
    setExpanded(false);
    if (lastOpener) lastOpener.focus();
  });
}
