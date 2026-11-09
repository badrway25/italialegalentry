/**
 * «Il portico» — the public navigation (docs/design-v5/V5_4_EXECUTION_PLAN.md §1.11, §1.12; W2-C1).
 *
 * Moved out of static/js/main.js (initNavigation) and bundled into shell.js, the one public entry (plan §2.3).
 * No dependency but the one motion gate (motion.js: `reducedMotion()` — the setting or the preview's flag — and
 * `nextFrame()`; plan §1.5 names the architrave among the sequences that pass through it, and
 * tests/frontend/test_script_motion_gate.py holds that no other module asks the media query or a frame itself),
 * no inline code (CSP script-src 'self'), no text: every string stays in the server's HTML.
 * Every state it sets is also expressible in the markup (aria-expanded, aria-current, classes), so a page is
 * correct before this file runs, and usable without it (chrome.css: panels on hover and focus-within, the
 * menu in the flow of the header below 80rem).
 *
 *   initHeaderState  the letterhead's scrolled state: one IntersectionObserver on a 24 px sentinel, no scroll
 *                    listener (64 → 56 px; the glass only then).
 *   initPortico      the bar and its door panels, the mechanics kept from N-A (NAVIGATION.md §4.4–§4.8):
 *                    - pointer intent on fine pointers only: open after 120 ms, switch after 80 ms, close after a
 *                      250 ms grace (--panel-hover-intent, --panel-grace); a click pins what a hover opened;
 *                    - the safe triangle for doors 2–4: while the pointer travels from the open door toward its
 *                      panel, crossing a neighbour does not switch the panel (§1.12 change 1);
 *                    - the scrim only for a click, a tap or the keyboard, from the letterhead's foot down;
 *                    - the keyboard model: ← → between items (they follow the eye in RTL; an open panel follows),
 *                      ↓ into the panel, ↑ back to the door, Home / End, Esc closes and returns the focus, Tab in
 *                      document order, focus leaving the navigation closes the panel (WCAG 1.4.13);
 *                    - «l'architrave», the one indicator: translateX + scaleX, the nearest item under the
 *                      pointer, no travel on its first placement, from the keyboard or under reduced motion;
 *                    - the layout the panels need and CSS cannot know: the entries' column starts at the first
 *                      door (--portico-lead, N2); since review round 1 (v515-a-improve1) each door has its own
 *                      height and a door change morphs the card from the old one's (--portico-from);
 *                    - the photographs (a frame of the menu's own, lane C's `menu_only`): nothing before `load`; at
 *                      idle after it, from 80rem, without Save-Data, fetched once (N8); a panel opened before that
 *                      fetches its own.
 *                    The panel's open state, scrim, Esc, light dismissal and focus return are still this module's own
 *                    (W2-C1's adapter): the overlay system's contract (docs/design-v5/QA/v54/w2-a/CONTRACT.md) has no
 *                    primitive for a disclosure region yet — the portico family (surfaces PC03) is asked of W2-A
 *                    (docs/design-v5/QA/v54/w2-c2/NOTES.md, «For W2-A»); until the switch, any `overlay:open` of the
 *                    system puts the panel away.
 *   V5.15 (DECISIONS §15 lane A): every item is in the bar from 64rem (one row); «le piano», a soft plate, glides under
 *                    the pointer from item to item (`glide`, transform and width, the snappy spring; never from the
 *                    keyboard, never on a touch screen); a panel that replaces another takes its content from the side the
 *                    pointer travelled (`data-from` start | end on the nav, 21st «Directional Menu» 36476's idea).
 *   initSheet        the sheet below 64rem (80rem before V5.15) (W2-C2, plan §1.12 item 8): the overlay system's modal drawer — «Menu»
 *                    opens it, overlay.js holds the trap, the scrim, Esc, «Fermer», a link and the focus back on
 *                    «Menu» (CONTRACT §2–§4); its doors unfold in place with no script (an exclusive <details name>,
 *                    main.js's accordion where the name is not supported). Here only what the system cannot know:
 *                    a window widened past 80rem — where the bar carries everything — puts the sheet away.
 *   initTarga        «la targa»'s key alone is named by the overlay system's top-layer tooltip (`data-tip="layer"`:
 *                    the wait, the keyboard's focus, Esc and a press are overlay.js's); from 100rem the plate says its
 *                    name, so its tip is refused (the system's cancelable `overlay:tip`). The signed-in seat's account
 *                    menu is the system's popover (components/account_menu.html): nothing of it is this module's.
 *   The lock-up's key (V5.29 «layout & brand refinement» §3) is the stylesheet's alone since CLOSING (V5.29 09:41
 *                    item 1, «CSS-only where possible»): static/css/v5/chrome.css §1 — the turn at the brand's reveal and
 *                    on its hover or focus, one at a time, never under reduced motion. Nothing of it is this module's.
 */

import { nextFrame, reducedMotion } from "./motion.js";
import { close as closeOverlay } from "./overlay.js";

const DESKTOP = window.matchMedia("(min-width: 80rem)");
const BAR = window.matchMedia("(min-width: 64rem)");
const FINE = window.matchMedia("(hover: hover) and (pointer: fine)");
const OPEN_MS = 120; /* --panel-hover-intent */
const SWITCH_MS = 80; /* a neighbour while a panel is open */
const CLOSE_MS = 250; /* --panel-grace */
const AIM_MS = 160; /* the pointer heads for the open panel: hold the switch this long, then look again */

const rtl = () => document.documentElement.dir === "rtl";
const shown = (el) => Boolean(el && el.getClientRects().length);

/* ---------------------------------------------------------------------------------- the letterhead */
function initHeaderState(header) {
  const sentinel = document.createElement("div");
  sentinel.setAttribute("aria-hidden", "true");
  sentinel.className = "header-sentinel";
  // A 24 px strip at the very top of the page, before the institutional bar: the bar is «scrolled» once the
  // strip has left the viewport entirely (direction V4 §3.2). The panel's geometry follows (nav.js layout()).
  document.body.prepend(sentinel);
  let first = true;
  new IntersectionObserver(([entry]) => {
    header.classList.toggle("is-scrolled", !entry.isIntersecting);
    if (!first) header.dispatchEvent(new CustomEvent("portico:layout"));
    first = false;
  }).observe(sentinel);
}

/* ---------------------------------------------------------------------------------- «il portico» */
function initPortico(header) {
  const nav = header.querySelector("[data-portico]");
  if (!nav) return;
  const inner = header.querySelector(".site-header__inner");
  const tops = [...nav.querySelectorAll(":scope > .main-nav__list > .main-nav__item > .main-nav__link")];
  const doors = tops.filter((top) => top.hasAttribute("data-portico-door"));
  if (!doors.length) return;
  const architrave = nav.querySelector("[data-portico-architrave]");
  const plate = nav.querySelector("[data-portico-plate]");
  const scrim = header.querySelector("[data-portico-scrim]");
  const panelOf = (door) => document.getElementById(door.getAttribute("aria-controls"));
  const doorOf = (panel) => doors.find((door) => panelOf(door) === panel) || null;
  const photoDoors = doors.filter((door) => panelOf(door)?.classList.contains("portico--door"));
  const openDoor = () => doors.find((door) => door.getAttribute("aria-expanded") === "true") || null;
  const current = () => tops.find((top) => top.hasAttribute("aria-current")) || null;
  const visibleTops = () => tops.filter(shown);
  const links = (panel) => [...panel.querySelectorAll("a[href]")].filter(shown);
  let mode = null; /* how the open panel was opened: pointer · click · key */
  let timer = 0;
  let classTimer = 0;
  let firstPointerOpen = true;
  let hovered = null; /* the door whose item is under the pointer */
  let samples = []; /* the pointer's last positions, for the safe triangle */
  let warmed = false;

  /* ---- l'architrave: physical pixels from the inner box's left edge, transform only ---- */
  function place(target, jump) {
    if (!architrave) return;
    if (!target || !BAR.matches || !shown(target)) {
      architrave.classList.remove("is-on");
      return;
    }
    const box = inner.getBoundingClientRect();
    const r = target.getBoundingClientRect();
    const pad = parseFloat(getComputedStyle(target).paddingInlineStart) || 0;
    const first = !architrave.classList.contains("is-on");
    architrave.classList.toggle("is-jump", Boolean(jump) || first || reducedMotion());
    architrave.style.transform = `translateX(${(r.left - box.left + pad).toFixed(2)}px) scaleX(${Math.max(1, r.width - 2 * pad).toFixed(2)})`;
    architrave.classList.add("is-on");
  }
  const rest = (jump) => place(openDoor() || current(), jump);

  /* ---- le piano: the soft plate under the pointer (physical pixels, as the architrave) ---- */
  function glide(target) {
    if (!plate) return;
    if (!target || !BAR.matches || !FINE.matches || !shown(target)) {
      plate.classList.remove("is-on");
      return;
    }
    const box = inner.getBoundingClientRect();
    const r = target.getBoundingClientRect();
    const first = !plate.classList.contains("is-on");
    plate.classList.toggle("is-jump", first || reducedMotion());
    plate.style.inlineSize = `${r.width.toFixed(2)}px`;
    plate.style.transform = `translateX(${(r.left - box.left).toFixed(2)}px)`;
    plate.classList.add("is-on");
  }

  /* ---- the geometry CSS cannot know: where the first door's words start (the plain panel's lede column) ----
     One rect, re-read on every change, the scrolled letterhead included (the lock-up may move the bar). Review round 1
     (v515-a-improve1): the doors no longer share one height — each panel has its own, and a door change morphs the
     card from the old door's height (`--portico-from`, written in `open()`, chrome.css §5) — so nothing opens the
     panels out of sight any more. */
  function lead() {
    const box = inner.getBoundingClientRect();
    const style = getComputedStyle(inner);
    const first = doors.find(shown);
    if (first) {
      const r = first.getBoundingClientRect();
      const pad = parseFloat(getComputedStyle(first).paddingInlineStart) || 0;
      const value = rtl()
        ? box.right - (parseFloat(style.paddingInlineEnd) || 0) - (r.right - pad)
        : r.left + pad - (box.left + (parseFloat(style.paddingInlineStart) || 0));
      if (value > 120) nav.style.setProperty("--portico-lead", `${Math.round(value)}px`);
    }
  }
  function layout() {
    if (!BAR.matches) return;
    lead();
    rest(true);
  }

  /* ---- the scrim: from the letterhead's real foot, so the institutional bar is never dimmed ---- */
  function showScrim(on) {
    if (!scrim) return;
    if (on) header.style.setProperty("--portico-scrim-top", `${Math.max(0, Math.round(header.getBoundingClientRect().bottom))}px`);
    scrim.hidden = !on;
  }

  /* ---- the photographs: a panel's own photograph is asked for when it opens, all of them at idle ---- */
  function warm(panel) {
    const img = panel?.querySelector("[data-portico-photo]");
    if (img && img.loading !== "eager") img.loading = "eager";
  }
  function warmAll() {
    if (warmed || !DESKTOP.matches || (navigator.connection && navigator.connection.saveData)) return;
    warmed = true;
    photoDoors.forEach((door) => warm(panelOf(door)));
  }
  nav.querySelectorAll("[data-portico-photo]").forEach((img) => {
    const done = () => img.classList.add("is-loaded");
    if (img.complete && img.naturalWidth) done();
    else img.addEventListener("load", done, { once: true });
  });

  function flag(name, ms) {
    nav.classList.add(name);
    clearTimeout(classTimer);
    classTimer = setTimeout(() => nav.classList.remove("is-switching", "is-first"), ms);
  }

  /* ---- open / close ---- */
  function open(door, how) {
    clearTimeout(timer);
    const was = openDoor();
    if (was === door) {
      if (how !== "pointer" && mode === "pointer") {
        mode = how;
        showScrim(true);
      }
      return;
    }
    const instant = how === "key" || reducedMotion();
    nav.classList.toggle("is-instant", instant);
    nav.classList.remove("is-switching", "is-first");
    if (was) {
      const forward = doors.indexOf(door) > doors.indexOf(was);
      nav.dataset.from = forward ? "end" : "start";
      // the card morphs from the old door's height to the new one's (chrome.css §5 / _portico.css); the old door's
      // plate is a drawing, not a photograph: nothing to cross-fade, it leaves with its panel
      panelOf(door).style.setProperty("--portico-from", `${Math.round(panelOf(was).getBoundingClientRect().height)}px`);
      was.setAttribute("aria-expanded", "false");
      if (!instant) flag("is-switching", 260);
    } else if (how === "pointer" && firstPointerOpen && !instant) {
      flag("is-first", 420);
    }
    if (how === "pointer") firstPointerOpen = false;
    warm(panelOf(door));
    door.setAttribute("aria-expanded", "true");
    mode = how === "pointer" && mode && mode !== "pointer" ? mode : how;
    header.classList.add("has-portico");
    showScrim(mode !== "pointer");
    place(door, instant || Boolean(was && how === "key"));
  }
  function close(focusBack) {
    clearTimeout(timer);
    const was = openDoor();
    if (!was) return;
    nav.classList.toggle("is-instant", mode === "key" || reducedMotion());
    was.setAttribute("aria-expanded", "false");
    mode = null;
    header.classList.remove("has-portico");
    showScrim(false);
    if (focusBack) was.focus();
    rest(false);
  }

  /* ---- the safe triangle: is the pointer heading for the open panel? ----
     The apex is the previous sample, the base the panel's top edge: a pointer moving down into that fan is
     on its way to the panel, whatever door it crosses on the way (doors 2–4 sit away from their entries). */
  function aiming() {
    const door = openDoor();
    const now = performance.now();
    const point = samples[samples.length - 1];
    if (!door || !point || now - point.t > AIM_MS) return false; /* a pointer that has stopped aims at nothing */
    const apex = samples.find((sample) => now - sample.t <= 120) || samples[0];
    const r = panelOf(door).getBoundingClientRect();
    const dy = point.y - apex.y;
    if (dy <= 0) return false;
    if (point.y >= r.top) return point.y < r.bottom;
    const x = apex.x + ((point.x - apex.x) * (r.top - apex.y)) / dy;
    return x >= r.left - 8 && x <= r.right + 8;
  }
  function intend(door) {
    clearTimeout(timer);
    const was = openDoor();
    if (was === door) return;
    if (was && mode === "pointer" && aiming()) {
      timer = setTimeout(() => {
        if (hovered === door) intend(door);
      }, AIM_MS);
      return;
    }
    timer = setTimeout(() => open(door, "pointer"), was ? SWITCH_MS : OPEN_MS);
  }

  /* ---- the pointer: intent, never a bare hover; a click pins what the hover opened ---- */
  doors.forEach((door) => {
    const item = door.closest("li");
    item.addEventListener("pointerenter", (event) => {
      if (event.pointerType !== "mouse" || !FINE.matches || !BAR.matches) return;
      hovered = door;
      intend(door);
    });
    item.addEventListener("pointerleave", (event) => {
      if (event.pointerType !== "mouse") return;
      if (hovered === door) hovered = null;
      clearTimeout(timer);
      if (mode === "pointer") timer = setTimeout(() => close(false), CLOSE_MS);
    });
    door.addEventListener("click", (event) => {
      const key = event.detail === 0; /* Enter / Space */
      if (openDoor() === door) {
        if (mode === "pointer" && !key) {
          mode = "click";
          showScrim(true);
          return;
        }
        close(false);
      } else {
        open(door, key ? "key" : "click");
      }
    });
  });
  header.addEventListener(
    "pointermove",
    (event) => {
      if (event.pointerType !== "mouse") return;
      const point = { x: event.clientX, y: event.clientY };
      // Between two items the indicator follows the nearest one (no dead zone), while no panel is open.
      if (!openDoor() && FINE.matches && nav.contains(event.target)) {
        let best = null;
        let distance = Infinity;
        for (const top of visibleTops()) {
          const r = top.getBoundingClientRect();
          const d = Math.abs(point.x - (r.left + r.width / 2));
          if (d < distance) {
            distance = d;
            best = top;
          }
        }
        place(best, false);
      }
      if (FINE.matches && nav.contains(event.target)) glide(event.target.closest(".main-nav__link"));
      samples.push({ ...point, t: performance.now() });
      if (samples.length > 8) samples = samples.slice(-8);
    },
    { passive: true },
  );
  nav.addEventListener("pointerleave", () => {
    glide(null);
    if (!openDoor()) rest(false);
  });
  if (scrim) scrim.addEventListener("click", () => close(false));

  /* ---- the keyboard (NAVIGATION §4.8; APG «disclosure navigation») ---- */
  const step = (list, from, by) => list[(list.indexOf(from) + by + list.length) % list.length];
  const eye = (key) => ((key === "ArrowRight") !== rtl() ? 1 : -1); /* → is «next» in LTR, «previous» in RTL */
  nav.addEventListener("keydown", (event) => {
    const target = event.target;
    const panel = target.closest("[data-portico-panel]");
    const top = panel ? null : target.closest(".main-nav__link");
    if (event.key === "Escape" && openDoor()) {
      event.preventDefault();
      event.stopPropagation();
      close(true);
      return;
    }
    if (top) {
      const list = visibleTops();
      if (event.key === "ArrowRight" || event.key === "ArrowLeft") {
        event.preventDefault();
        const next = step(list, top, eye(event.key));
        next.focus();
        if (openDoor()) {
          if (doors.includes(next)) open(next, "key");
          else close(false);
        }
        place(next, true);
      } else if (event.key === "ArrowDown" && doors.includes(top)) {
        event.preventDefault();
        if (openDoor() !== top) open(top, "key");
        links(panelOf(top))[0]?.focus();
      } else if (event.key === "ArrowUp" && doors.includes(top)) {
        event.preventDefault(); /* nothing above the bar: the page does not scroll either */
      } else if (event.key === "Home" || event.key === "End") {
        event.preventDefault();
        const to = event.key === "Home" ? list[0] : list[list.length - 1];
        to.focus();
        if (openDoor()) {
          /* as the arrows: an open panel follows the focus to a door, and leaves with it otherwise */
          if (doors.includes(to)) open(to, "key");
          else close(false);
        }
        place(to, true);
      }
      return;
    }
    if (panel) {
      const own = links(panel);
      const owner = doorOf(panel);
      const at = own.indexOf(target);
      if (event.key === "ArrowDown" || event.key === "ArrowUp") {
        event.preventDefault();
        if (event.key === "ArrowUp" && at <= 0) owner.focus();
        else own[Math.min(own.length - 1, Math.max(0, at + (event.key === "ArrowDown" ? 1 : -1)))].focus();
      } else if (event.key === "Home" || event.key === "End") {
        event.preventDefault();
        (event.key === "Home" ? own[0] : own[own.length - 1]).focus();
      } else if (event.key === "ArrowRight" || event.key === "ArrowLeft") {
        event.preventDefault();
        const next = step(visibleTops(), owner, eye(event.key));
        next.focus();
        if (doors.includes(next)) open(next, "key");
        else close(false);
        place(next, true);
      }
    }
  });
  nav.addEventListener("focusin", (event) => {
    const top = event.target.closest(".main-nav__link");
    if (top && !openDoor()) place(top, true);
  });
  // WCAG 1.4.13 + APG: focus that leaves the navigation closes the panel.
  nav.addEventListener("focusout", (event) => {
    if (event.relatedTarget && !nav.contains(event.relatedTarget)) {
      if (openDoor()) close(false);
      else rest(true);
    }
  });
  // Esc wherever the focus is (a panel opened by the pointer while the focus is in the page).
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && openDoor() && !nav.contains(document.activeElement)) close(false);
  });
  // A panel of the overlay system opening — the sheet, the account popover — puts the door's panel away: in Safari and
  // on an iPad a press does not focus the button pressed, so a door pinned by a press has no focus to lose and the
  // focusout above never comes; the opening moves the focus into its own panel (W2-C2 REVIEW m2).
  document.addEventListener("overlay:open", () => close(false));

  /* ---- widths, fonts, the scrolled letterhead ---- */
  let asked = 0; // the layout requests so far: only the last one of a frame measures (layout() takes no
  // argument: the «forced» flag it was once handed was read by nothing — CLOSING, V5.29 09:41 item 1, dead code out)
  const relayout = () => {
    const mine = ++asked;
    nextFrame().then(() => {
      if (mine === asked) layout();
    });
  };
  BAR.addEventListener("change", () => {
    close(false);
    relayout();
  });
  DESKTOP.addEventListener("change", relayout);
  addEventListener("resize", relayout, { passive: true }); /* the lead and the architrave */
  header.addEventListener("portico:layout", relayout); /* the 64 ↔ 56 switch: the lead and the architrave */
  (document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve()).then(relayout);
  const idle = () => (window.requestIdleCallback ? requestIdleCallback(warmAll, { timeout: 4000 }) : setTimeout(warmAll, 2000));
  if (document.readyState === "complete") idle();
  else addEventListener("load", idle, { once: true });
  relayout();
}

/* ---------------------------------------------------------------------------------- «la targa» */
function initTarga(header) {
  const targa = header.querySelector(".site-header__end > .targa[data-tip]");
  if (!targa) return;
  const labelled = window.matchMedia("(min-width: 90rem)"); /* chrome.css §6: the plate's word from 90rem (V5.15) */
  targa.addEventListener("overlay:tip", (event) => {
    if (labelled.matches) event.preventDefault();
  });
}

/* ---------------------------------------------------------------------------------- the sheet (< 64rem) */
function initSheet(header) {
  const sheet = document.getElementById("nav-sheet");
  if (!sheet) return;
  // past 64rem the sheet is not drawn and «Menu» neither (every item is in the bar): the sheet goes at once, and a focus
  // that was in it lands on the letterhead's lock-up (overlay.js moves it only from inside the sheet)
  BAR.addEventListener("change", () => {
    if (BAR.matches) closeOverlay(sheet, { reason: "api", instant: true, focus: header.querySelector(".brand") });
  });
}

export function initNavigation() {
  const header = document.querySelector(".site-header");
  if (!header) return;
  initHeaderState(header);
  initPortico(header);
  initTarga(header);
  initSheet(header);
}
