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
 *                      door (--portico-lead, N2), one height for the four door panels (--portico-h, LA-7 — measured
 *                      when the width, the bar or the fonts change, not on the scrolled switch), the short panels
 *                      marked (.portico--short) so that their list closes with a hairline;
 *   initTarga        the key-alone plate's name tooltip hides on Esc while the pointer or the focus stays (1.4.13).
 *                    - the photographs: nothing before `load`; at idle after it, from 80rem, without Save-Data,
 *                      fetched once (N8); a panel opened before that fetches its own; the old one cross-fades.
 *   initDrawer       today's drawer below 80rem (main.js's, kept until W2-C2 moves it onto the overlay system):
 *                    «Menu», the scrim and the drawer from the letterhead's real foot, Esc, the focus loop,
 *                    the sections unfolding in place.
 */

import { nextFrame, reducedMotion } from "./motion.js";

const DESKTOP = window.matchMedia("(min-width: 80rem)");
const BAR = window.matchMedia("(min-width: 64rem)");
const FINE = window.matchMedia("(hover: hover) and (pointer: fine)");
const OPEN_MS = 120; /* --panel-hover-intent */
const SWITCH_MS = 80; /* a neighbour while a panel is open */
const CLOSE_MS = 250; /* --panel-grace */
const AIM_MS = 160; /* the pointer heads for the open panel: hold the switch this long, then look again */
const FOCUSABLE =
  'a[href], button:not([disabled]), input:not([disabled]):not([type="hidden"]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])';

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

  /* ---- the geometry CSS cannot know: where the first door's words start, one height for the doors ----
     Two costs, kept apart (the family's a11y/perf check, finding 2): the lead is one rect and is re-read on every
     change, the scrolled letterhead included (the lock-up may move the bar); the one height opens the four door
     panels out of sight and is measured only when the inner's width, the bar or the fonts change — never on the
     64 ↔ 56 switch, where it was a long task on every wheel crossing. */
  let measuredAt = -1; /* the inner width the one height was measured at */
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
    return box;
  }
  function heights() {
    // One height for the door panels: each is measured at its natural height, out of sight, in one frame.
    nav.classList.add("is-measuring");
    nav.style.setProperty("--portico-h", "auto");
    const natural = photoDoors.map((door) => [panelOf(door), panelOf(door).offsetHeight]);
    nav.classList.remove("is-measuring");
    const height = Math.max(0, ...natural.map(([, h]) => h));
    if (height) nav.style.setProperty("--portico-h", `${Math.ceil(height)}px`);
    // A door whose own content ends well above the shared height (LA-7's 24 px) closes its list with a hairline.
    for (const [panel, h] of natural) panel.classList.toggle("portico--short", height - h > 24);
  }
  function layout(force) {
    if (!BAR.matches) return;
    const width = Math.round(lead().width);
    if (force || width !== measuredAt) {
      measuredAt = width;
      heights();
    }
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
      const leaving = panelOf(was);
      if (!instant && DESKTOP.matches && leaving.classList.contains("portico--door")) {
        leaving.classList.add("is-leaving");
        setTimeout(() => leaving.classList.remove("is-leaving"), 220);
      }
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
      samples.push({ ...point, t: performance.now() });
      if (samples.length > 8) samples = samples.slice(-8);
    },
    { passive: true },
  );
  nav.addEventListener("pointerleave", () => {
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

  /* ---- widths, fonts, the scrolled letterhead ---- */
  let asked = 0; // the layout requests so far: only the last one of a frame measures
  let forced = false;
  const relayout = (force) => {
    forced = forced || force === true;
    const mine = ++asked;
    nextFrame().then(() => {
      if (mine !== asked) return;
      const full = forced;
      forced = false;
      layout(full);
    });
  };
  BAR.addEventListener("change", () => {
    close(false);
    relayout(true);
  });
  DESKTOP.addEventListener("change", () => relayout(true));
  addEventListener("resize", () => relayout(false), { passive: true }); /* the heights again only if the width moved */
  header.addEventListener("portico:layout", () => relayout(false)); /* the 64 ↔ 56 switch: the lead and the architrave */
  (document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve()).then(() => relayout(true));
  const idle = () => (window.requestIdleCallback ? requestIdleCallback(warmAll, { timeout: 4000 }) : setTimeout(warmAll, 2000));
  if (document.readyState === "complete") idle();
  else addEventListener("load", idle, { once: true });
  nav.classList.add("is-enhanced");
  relayout(true);
}

/* ---------------------------------------------------------------------------------- «la targa» */
function initTarga(header) {
  // Below the label threshold the key alone carries a name tooltip on hover and on focus; Esc hides it while the
  // pointer or the focus stays (WCAG 1.4.13: dismissible), until either leaves. The tip is chrome.css §6's.
  const targa = header.querySelector(".site-header__end > .targa");
  if (!targa) return;
  const back = () => targa.classList.remove("tip-off");
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && targa.matches(":hover, :focus-visible")) targa.classList.add("tip-off");
  });
  targa.addEventListener("pointerleave", back);
  targa.addEventListener("blur", back);
}

/* ---------------------------------------------------------------------------------- the drawer (< 80rem) */
function initDrawer(header) {
  const toggle = header.querySelector("[data-nav-toggle]");
  const drawer = header.querySelector("[data-nav-drawer]");
  const overlay = header.querySelector("[data-nav-overlay]");
  if (!toggle || !drawer) return;
  const items = [...drawer.querySelectorAll("[data-nav-item]")];

  // The sections unfold in place: one open at a time, Esc closes the innermost.
  const closeItems = (except = null) =>
    items.forEach((item) => {
      if (item === except) return;
      item.dataset.open = "false";
      item.querySelector("[data-nav-panel-toggle]")?.setAttribute("aria-expanded", "false");
    });
  items.forEach((item) => {
    const button = item.querySelector("[data-nav-panel-toggle]");
    if (!button) return;
    button.setAttribute("aria-expanded", "false");
    button.addEventListener("click", () => {
      const opening = item.dataset.open !== "true";
      closeItems(item);
      item.dataset.open = opening ? "true" : "false";
      button.setAttribute("aria-expanded", opening ? "true" : "false");
    });
    item.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && item.dataset.open === "true") {
        event.preventDefault();
        event.stopPropagation(); /* Esc closes the innermost open thing, and only that one */
        closeItems();
        button.focus();
      }
    });
  });

  // The drawer and its scrim start at the letterhead's REAL foot, which moves with the institutional bar and
  // the scrolled state: written on the header, so that both inherit it (G-23), and measured again whenever the
  // viewport or the header changes while the drawer is open (rotation, round 4 defect 12).
  const placeDrawer = () => {
    const bottom = Math.max(0, Math.round(header.getBoundingClientRect().bottom));
    header.style.setProperty("--nav-drawer-top", `${bottom}px`);
  };
  const isOpen = () => document.body.dataset.navOpen === "true";
  addEventListener("resize", () => isOpen() && placeDrawer(), { passive: true });
  if ("ResizeObserver" in window) new ResizeObserver(() => isOpen() && placeDrawer()).observe(header);
  const setDrawer = (open) => {
    if (open) placeDrawer();
    document.body.dataset.navOpen = open ? "true" : "false";
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    if (open) drawer.querySelector(FOCUSABLE)?.focus();
  };
  toggle.setAttribute("aria-expanded", "false");
  toggle.addEventListener("click", () => setDrawer(!isOpen()));
  overlay?.addEventListener("click", () => setDrawer(false));
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && isOpen()) {
      setDrawer(false);
      toggle.focus();
    }
  });
  // The focus stays inside the open drawer: Tab from the last stop and Shift+Tab from the first return to «Menu».
  drawer.addEventListener("keydown", (event) => {
    if (event.key !== "Tab" || DESKTOP.matches || !isOpen()) return;
    const stops = [...drawer.querySelectorAll(FOCUSABLE)].filter(shown);
    if (!stops.length) return;
    if (event.shiftKey && document.activeElement === stops[0]) {
      event.preventDefault();
      toggle.focus();
    } else if (!event.shiftKey && document.activeElement === stops[stops.length - 1]) {
      event.preventDefault();
      toggle.focus();
    }
  });
  DESKTOP.addEventListener("change", () => {
    setDrawer(false);
    closeItems();
  });
}

export function initNavigation() {
  const header = document.querySelector(".site-header");
  if (!header) return;
  initHeaderState(header);
  initPortico(header);
  initTarga(header);
  initDrawer(header);
}
