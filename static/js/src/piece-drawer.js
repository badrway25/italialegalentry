/**
 * The preview drawer — one piece of the register, unfolded beside it (design V5, W3-C; V5.4 plan §1.14 «Preview
 * drawer», §3.5 item 5; DOCUMENT_WORKSPACE.md §12): templates/documents/partials/piece_drawer.html on the overlay
 * system (static/js/src/overlay.js — the drawer family, non-modal beside the list on desktop, a modal sheet on a phone;
 * docs/design-v5/QA/v54/w2-a/CONTRACT.md). Imported by console.js where the register draws the drawer.
 *
 *   open      a plain press on a row's title (the row is the link), on a row's act, or on the strip's act; a modified
 *             press (a new tab, a new window) and a middle one keep the link's own way — and without this module the
 *             same links lead to the piece's page
 *   head      at 0 ms, from the row: the file's reference, the title in its own language, the row's line — the state's
 *             chip, the actor, the date — copied as words and attributes into the template's slots (nothing waits for
 *             the network, and nothing is inserted in the press's task: an insertion re-evaluates the console's
 *             document-wide :has() rules — ≈ 80 ms at CPU × 4 on «Mes pièces», measured)
 *   body      the piece's page fetched and its <article> taken whole: nothing for the first 400 ms, then the busy key
 *             turns in the head (L2's markup); on a piece's first arrival its parts are seated by L3 (loader.js `seat`),
 *             a refresh swaps in place; the Dépôt inside is wired with the drawer as the host of its live regions and
 *             the drawer's own refresh — after a filing the piece is read again in place AND the register behind it
 *             (its strip, its row, its files), the drawer's opener moved to the fresh row
 *   history   the first opening pushes the piece's URL (a reload lands on the full page); Back, Esc and «Fermer» close
 *             it (overlay.js) and the register's URL — its `?état=` — comes back; a swap replaces the entry
 *             (replaceState); a Forward onto a closed drawer's entry loads that piece's page. While the drawer owns
 *             its entry the register's keeps no scroll to restore (`history.scrollRestoration`, manual): going back
 *             to it would put the page where it stood at the first opening (REVIEW M1) — the page stays where the
 *             person is, and the mode comes back once the register's entry is theirs again
 *   beside    while the drawer is non-modal the workspace makes room for it (`data-drawer-beside`): the register lays
 *             itself out by the width it is given (its container query) — five columns, or cards — and the row the
 *             person pressed stays where it stood under the pointer, on opening as on closing (REVIEW M2)
 *   marked    the register says which piece the drawer shows: its row's title `aria-current`, the row in the selected
 *             state (`data-drawer-open`: the hover's surface and a 2 px rule, _workspace.css §10); the strip's next
 *             piece too when it is that piece, its act stepped down to a secondary — moved on a swap, cleared on
 *             closing (REVIEW M2, m2)
 *   focus     the title on opening (a non-modal drawer, CONTRACT §4) and, on closing, the title of the row of the piece
 *             shown — after a swap too: the native dialog, shown once, hands the focus back to the row focused at its
 *             show(), and overlay.js gives it back only from inside the panel (REVIEW M1); a swap from the list
 *             leaves the focus where the person is; a row's act or the strip's act sends it to the Dépôt's field once
 *             the piece has arrived
 * No word here: every word is the page's. CSP: nothing evaluated, no inline style — classes and attributes only.
 */
import { initDepots } from "./depot.js";
import { afterPaint } from "./motion.js";
import { initOverlays, isOpen, open } from "./overlay.js";

/** What opens a piece in the drawer: a row's title, a row's act, the strip's act — inside the register only. */
const OPENERS = ".doc-row__link, .doc-row__act a, .reg__next-act a";
/** The eye forgives this long a wait (--motion-wait): the key shows only after it. */
const WAIT = 400;
/** L3 of «Lume» (loader.js `seat`) — never imported statically: shell.js loads the loader on demand (W1-D). Asked for
 *  when a piece is opened, it arrives long before the piece's page; a fragment that arrives first simply stands — a seat
 *  begun after its rows were painted would hide them and raise them again. */
let loaderModule = null;
let loaderAsked = null;
const askLoader = () => (loaderAsked ||= import("./loader.js").then((module) => (loaderModule = module)));
const seat = (container) => {
  if (loaderModule) loaderModule.seat(container); // its first steps are synchronous: before the rows' first paint
};

async function readArticle(url, signal) {
  const response = await fetch(url, { credentials: "same-origin", headers: { Accept: "text/html" }, signal });
  if (!response.ok) throw new Error(String(response.status));
  const doc = new DOMParser().parseFromString(await response.text(), "text/html");
  return doc;
}

export function initPieceDrawer() {
  const drawer = document.querySelector("[data-piece-drawer]");
  if (!drawer || drawer.dataset.pieceDrawerReady !== undefined) return;
  drawer.dataset.pieceDrawerReady = "";
  const title = drawer.querySelector("[data-drawer-title]");
  const ref = drawer.querySelector("[data-drawer-ref]");
  const slots = {
    chip: drawer.querySelector("[data-drawer-state] .chip"),
    blocked: drawer.querySelector("[data-drawer-blocked]"),
    actor: drawer.querySelector("[data-drawer-actor]"),
    actorName: drawer.querySelector("[data-drawer-actor-name]"),
    due: drawer.querySelector("[data-drawer-due]"),
  };
  const body = drawer.querySelector("[data-drawer-body]");
  const workspace = document.querySelector(".console__workspace");
  let registerUrl = null; // the register's URL when the drawer first opened — its ?état= included
  let current = null; // the piece shown
  let controller = null; // the reading in flight
  let busyTimer = 0;

  const absolute = (href) => new URL(href, window.location.href).href;
  const rowOf = (link) => {
    const row = link.closest(".doc-row");
    if (row) return row;
    const href = absolute(link.getAttribute("href") || "");
    return [...document.querySelectorAll(".doc-register .doc-row")].find((candidate) => {
      const title = candidate.querySelector(".doc-row__link");
      return title && absolute(title.getAttribute("href")) === href;
    }) || null;
  };

  /** The head, at 0 ms, from the row the person pressed — words and attributes only, into the slots the template
   *  draws: no element is inserted in the press's task (an insertion re-evaluates the page's :has() rules). */
  const hrefOf = (svg) => (svg && svg.querySelector("use") ? svg.querySelector("use").getAttribute("href") : null);
  /** A slot's words through its own text node (the template gives each one): a text node's data is no insertion. */
  const setText = (element, text) => {
    const node = element.firstChild;
    if (node && node.nodeType === Node.TEXT_NODE && element.childNodes.length === 1) {
      if (node.data !== text) node.data = text;
    } else {
      element.textContent = text;
    }
  };
  const setHref = (svg, href) => {
    const use = svg && svg.querySelector("use");
    if (use && href) use.setAttribute("href", href);
  };
  function fillHead(row, link) {
    // the strip's act whose row a state filter keeps out of the list: the strip names the piece and its date
    const next = row ? null : link.closest(".reg__next");
    const titleLink = row ? row.querySelector(".doc-row__link") : (next && next.querySelector(".reg__next-title")) || link;
    setText(title, titleLink.textContent.trim());
    // a title in another language than the page's keeps its own, isolated in the line (the block keeps the page's)
    const language = titleLink.matches("[lang]") ? titleLink : titleLink.querySelector("[lang]") || titleLink;
    ["lang", "dir"].forEach((name) => {
      const value = language.getAttribute(name);
      if (value) title.setAttribute(name, value);
      else title.removeAttribute(name);
    });
    const caseRef = ((row && row.closest(".ws-case")) || document).querySelector(".ws-case__ref > span");
    setText(ref, caseRef ? caseRef.textContent.trim() : "");
    const chip = row && row.querySelector(".doc-row__state .chip");
    if (slots.chip) slots.chip.closest("[data-drawer-state]").hidden = !chip;
    if (chip && slots.chip) {
      slots.chip.setAttribute("data-register", chip.getAttribute("data-register") || "");
      setHref(slots.chip.querySelector("svg"), hrefOf(chip.querySelector("svg")));
      setText(slots.chip.querySelector(".chip__w"), chip.querySelector(".chip__w").textContent.trim());
    }
    if (slots.blocked) slots.blocked.hidden = !(row && row.querySelector(".doc-row__blocked"));
    const actor = row && row.querySelector(".doc-row__resp");
    slots.actor.hidden = !actor;
    if (actor) {
      setHref(slots.actor.querySelector(".glyph svg"), hrefOf(actor.querySelector(".glyph svg")));
      const name = actor.querySelector(".doc-row__actor");
      setText(slots.actorName, name ? name.textContent.replace(/\s+/g, " ").trim() : "");
    }
    const date = (row && row.querySelector(".doc-row__due .doc-due")) || (next && next.querySelector(".reg__next-due .doc-due"));
    slots.due.hidden = !(date && date.querySelector("time"));
    if (date && date.querySelector("time")) {
      const due = slots.due.querySelector(".doc-due");
      due.className = `${date.className} doc-due--inline`;
      setHref(due.querySelector(".doc-due__mark svg"), hrefOf(date.querySelector(".doc-due__mark svg")));
      const time = due.querySelector("time");
      time.setAttribute("datetime", date.querySelector("time").getAttribute("datetime") || "");
      setText(time, date.querySelector("time").textContent);
      const word = date.querySelector(".doc-due__word");
      const slot = due.querySelector(".doc-due__word");
      setText(slot, word ? word.textContent : " ");
      slot.hidden = !word; // no word, no separator
    }
  }

  /** The register says which piece the drawer shows (REVIEW M2): the row's title is the current one, the row holds
   *  the selected state; where the strip names that piece, its next piece too, and its act steps down to a secondary —
   *  the drawer holds the act now (REVIEW m2). Attributes and a class only: nothing is inserted. */
  function mark(url) {
    document.querySelectorAll(".doc-register [data-drawer-open]").forEach((element) => element.removeAttribute("data-drawer-open"));
    document.querySelectorAll(".doc-register .doc-row__link[aria-current]").forEach((link) => link.removeAttribute("aria-current"));
    document.querySelectorAll(".doc-register [data-drawer-stepped]").forEach((act) => {
      act.classList.replace("btn--secondary", "btn--primary");
      act.removeAttribute("data-drawer-stepped");
    });
    if (!url) return;
    document.querySelectorAll(".doc-register .doc-row__link").forEach((link) => {
      if (absolute(link.getAttribute("href")) !== url) return;
      link.setAttribute("aria-current", "true");
      link.closest(".doc-row").setAttribute("data-drawer-open", "");
    });
    document.querySelectorAll(".doc-register .reg__next-act a").forEach((act) => {
      if (absolute(act.getAttribute("href")) !== url) return;
      act.closest(".reg__next").setAttribute("data-drawer-open", "");
      if (act.classList.replace("btn--primary", "btn--secondary")) act.setAttribute("data-drawer-stepped", "");
    });
  }

  /** On closing, the focus in the register stands in view — the page is never moved for it otherwise. */
  function reveal() {
    const active = document.activeElement;
    if (!active || active === document.body || !active.closest(".doc-register")) return;
    const style = getComputedStyle(document.documentElement);
    const top = parseFloat(style.scrollPaddingTop) || 0;
    const bottom = window.innerHeight - (parseFloat(style.scrollPaddingBottom) || 0);
    const box = active.getBoundingClientRect();
    if (box.top < top || box.bottom > bottom) active.scrollIntoView({ block: "nearest", behavior: "instant" });
  }

  /** The workspace makes room for a drawer beside the list — once the drawer's first frame is painted: the register's
   *  re-layout (its container query: five columns, or cards) stays out of the press's frame (plan §1.14 O7, INP). It
   *  reads the drawer as it is by then, so a quick close or reopen settles on the last state. `element` is what the
   *  person's eye and pointer are on — what was pressed on opening or, on closing, where the focus is (the title of
   *  the row of the piece shown): it stands where it stood once the register has laid itself out again (REVIEW M2:
   *  the card that slid under the pointer read as the piece open). Then the marks follow the drawer, and on closing
   *  the focus is brought into view. */
  let besideQueued = false;
  let place = null;
  function beside(element) {
    if (element) place = element;
    if (besideQueued) return;
    besideQueued = true;
    afterPaint().then(() => {
      besideQueued = false;
      const open = isOpen(drawer);
      const on = open && drawer.getAttribute("data-overlay-mode") !== "sheet";
      const keep = place && place.isConnected ? place : null;
      place = null;
      if (workspace && workspace.hasAttribute("data-drawer-beside") !== on) {
        const before = keep ? keep.getBoundingClientRect().top : 0;
        workspace.toggleAttribute("data-drawer-beside", on);
        const shift = keep ? Math.round(keep.getBoundingClientRect().top - before) : 0;
        if (shift) window.scrollBy({ top: shift, behavior: "instant" });
      }
      mark(open ? current : null);
      if (!open) reveal();
    });
  }

  /* The register's history entry keeps no scroll of its own while the drawer owns the next one (REVIEW M1): Back, Esc
     and «Fermer» go back to it, and the browser would put the page back where it stood at the first opening — the
     top, after a swap far down the list. Held before the first push (the register's entry is the current one then,
     and the drawer's entry inherits it), given back once the register's entry is the current one again. */
  let restoration = null;
  const holdScroll = () => {
    if (restoration !== null || !("scrollRestoration" in window.history)) return;
    restoration = window.history.scrollRestoration;
    window.history.scrollRestoration = "manual";
  };
  const releaseScroll = () => {
    if (restoration === null || isOpen(drawer)) return;
    window.history.scrollRestoration = restoration;
    restoration = null;
  };
  /** After a close: when overlay.js has asked for the register's entry (history.back()) and the drawer's is still
   *  the current one, the mode comes back once that traversal has landed, after its frame. */
  const settleScroll = () => {
    if (restoration === null) return;
    if (window.history.state && window.history.state.ileOverlay === drawer.id) {
      window.addEventListener("popstate", () => afterPaint().then(releaseScroll), { once: true });
    } else {
      afterPaint().then(releaseScroll);
    }
  };

  /* Was the focus inside the drawer when it closed? Read on `overlay:close`, by which time the native close has
     already handed the focus back to the row focused at the dialog's show(): that focusout comes with the drawer
     shut, and is not the person leaving it. */
  let focusInside = false;
  drawer.addEventListener("focusin", () => {
    focusInside = true;
  });
  drawer.addEventListener("focusout", (event) => {
    if (drawer.open && !drawer.contains(event.relatedTarget)) focusInside = false;
  });

  function busy(on) {
    window.clearTimeout(busyTimer);
    if (on) {
      body.setAttribute("aria-busy", "true");
      busyTimer = window.setTimeout(() => drawer.classList.add("is-busy"), WAIT);
    } else {
      body.removeAttribute("aria-busy");
      drawer.classList.remove("is-busy");
    }
  }

  /** The piece read (again): its article in the body — seated on a piece's first arrival, swapped in place after. */
  async function load(url, { first = false, toDepot = false } = {}) {
    if (controller) controller.abort();
    controller = new AbortController();
    const { signal } = controller;
    if (first) body.replaceChildren();
    busy(true);
    try {
      const doc = await readArticle(url, signal);
      const article = doc.querySelector("article.doc-piece");
      if (!article) throw new Error("no piece");
      const node = document.importNode(article, true);
      if (first) node.setAttribute("data-seat", "");
      body.replaceChildren(node);
      if (first) body.scrollTop = 0;
      initDepots(node, { live: drawer, refresh });
      initOverlays(node);
      if (first) seat(node);
      if (toDepot) {
        const field = node.querySelector('[data-depot] input[type="file"]');
        if (field) field.focus({ preventScroll: false });
      }
      return node;
    } catch (error) {
      if (error && error.name === "AbortError") return null;
      // the piece could not be read here: its own page is the way
      window.location.assign(url);
      return null;
    } finally {
      if (!signal.aborted) busy(false);
    }
  }

  /** After an answer that changed the piece (the Dépôt's filing): the piece in place, then the register behind it. */
  async function refresh() {
    if (!current) return null;
    const node = await load(current);
    await refreshRegister();
    return node;
  }

  async function refreshRegister() {
    if (!registerUrl) return;
    try {
      const doc = await readArticle(registerUrl);
      const fresh = doc.querySelector(".doc-page");
      const page = document.querySelector(".doc-page");
      if (!fresh || !page) return;
      const node = document.importNode(fresh, true);
      page.replaceWith(node);
      initOverlays(node); // the filter's sheet of the fresh page
      node.dispatchEvent(new CustomEvent("documents:refreshed", { bubbles: true })); // console.js: the search
      const link = [...node.querySelectorAll(".doc-row__link")].find((candidate) => absolute(candidate.getAttribute("href")) === current);
      if (link && isOpen(drawer)) {
        open(drawer, { opener: link }); // the focus goes back to the fresh row on closing
        fillHead(link.closest(".doc-row"), link); // the head repeats the row as it is now
      }
      if (isOpen(drawer)) mark(current); // the fresh register says which piece is open, its strip's act stepped down
    } catch {
      /* the register stays as it was until the next page */
    }
  }

  function openPiece(link, { toDepot = false } = {}) {
    askLoader();
    const url = absolute(link.getAttribute("href"));
    const row = rowOf(link);
    const opener = (row && row.querySelector(".doc-row__link")) || link;
    fillHead(row, link);
    const swap = isOpen(drawer);
    if (swap && current === url) return; // the piece is already there
    if (!swap) {
      registerUrl = window.location.href;
      holdScroll(); // before the drawer's entry is pushed
    }
    const first = current !== url;
    if (!open(drawer, { opener, history: swap ? { url, replace: true } : { url } })) {
      releaseScroll();
      window.location.assign(url);
      return;
    }
    current = url;
    beside(link); // what was pressed stays under the pointer: the row's title, the row's act, the strip's act
    load(url, { first, toDepot });
  }

  /** The opener a plain press would hand to the drawer, or null (a modified press keeps the link's own way). */
  const openerOf = (event) => {
    if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return null;
    const link = event.target instanceof Element ? event.target.closest(OPENERS) : null;
    if (!link || !link.closest(".doc-register") || !link.getAttribute("href")) return null;
    const url = new URL(link.getAttribute("href"), window.location.href);
    return url.origin === window.location.origin && url.pathname.startsWith("/documents/requirements/") ? link : null;
  };

  document.addEventListener("click", (event) => {
    if (event.defaultPrevented) return;
    const link = openerOf(event);
    if (!link) return;
    event.preventDefault();
    openPiece(link, { toDepot: !link.classList.contains("doc-row__link") });
  });

  drawer.addEventListener("overlay:close", (event) => {
    const { reason, opener } = event.detail || {};
    const inside = focusInside;
    focusInside = false;
    if (controller) controller.abort();
    busy(false);
    current = null;
    registerUrl = null;
    // the focus goes back to the title of the row of the piece shown (overlay.js's opener, which a swap moves) — not
    // to the row of the first opening, where the native dialog has just put it; only when it was inside the drawer
    // or nowhere, and never for a link that leaves the page (REVIEW M1)
    const active = document.activeElement;
    const nowhere = !active || active === document.body;
    if (reason !== "link" && (inside || nowhere) && opener && opener.isConnected && !opener.closest("[inert]")) {
      if (active !== opener) opener.focus({ preventScroll: true });
    }
    const focused = document.activeElement;
    beside((focused && focused.closest(".doc-register") ? focused : null) || (opener && opener.isConnected ? opener : null));
    settleScroll();
  });

  // a Forward onto the entry of a drawer that is closed: the piece's own page (the URL already says which)
  window.addEventListener("popstate", (event) => {
    if (event.state && event.state.ileOverlay === drawer.id && !isOpen(drawer)) window.location.reload();
  });
}
