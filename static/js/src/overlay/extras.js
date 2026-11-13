/**
 * The overlay system's rarer parts — what no console page draws, so no console page fetches it (the module budget of
 * docs/design-v5/V5_4_EXECUTION_PLAN.md §2.6; docs/design-v5/QA/v54/w2-a/A11Y_PERF.md M4). static/js/src/overlay.js
 * imports this file on demand — at idle where a page draws one of these parts, at once for the placement:
 *   · the grip of a sheet (`data-overlay-grip`): dragged down it follows the finger; let go past a third, or fast, the
 *     sheet leaves; short of that it springs back. Never the only way out: «Fermer» is always there (WCAG 2.5.7);
 *   · Back (`data-overlay-history`, `open(panel, {history})`): the opening pushes one history entry, Back closes the
 *     panel, and a content swap in an open panel replaces the entry (overlay.js takes the entry back when the panel
 *     closes another way);
 *   · the place of a menu where the engine has no anchor positioning: on the trigger's inline end, below unless the
 *     side chosen before the opening says above, flipped and clamped as `position-try-fallbacks` would, and followed
 *     on scroll and resize;
 *   · a dialog's body that scrolls and holds nothing to focus made a stop of its own (WCAG 2.1.1: Chromium and Firefox
 *     make such a scroller focusable themselves, Safari does not — A11Y_PERF m1, an alert's body at 400 % zoom), read
 *     at the opening and on a resize; the trap counts it;
 *   · the press on a native modal's ::backdrop (`data-overlay-modal="native"`, showModal()): it closes the dialog
 *     only when it went down AND came up outside the panel — never an alert, never unsaved input.
 * It imports nothing: overlay.js hands over what the parts need (`install(core)`) — the frame wait of motion.js's gate
 * among them (`core.nextFrame`: no module asks for a frame itself, W1-D). CSSOM writes only (left, top, translate,
 * --overlay-drag), which the CSP allows; strings are the templates', never this file's.
 */

let core = null;

/** Called once by overlay.js with its core: returns the parts. */
export function install(api) {
  core = api;
  // Back: a panel whose history entry is gone closes
  window.addEventListener("popstate", (event) => {
    [...core.opened].forEach((panel) => {
      const record = core.recordOf(panel);
      if (record.pushed && !(event.state && event.state.ileOverlay === panel.id)) {
        record.pushed = false;
        core.close(panel, { reason: "back" });
      }
    });
  });
  // a resize (a zoom) may make a body scroll, or stop: its stop follows — once a frame, the frame asked of the gate
  // (under reduced motion it answers at once: a resize is already one a frame)
  let resizing = false;
  window.addEventListener(
    "resize",
    () => {
      if (resizing) return;
      resizing = true;
      core.nextFrame().then(() => {
        resizing = false;
        core.opened.forEach(reachable);
      });
    },
    { passive: true },
  );
  return { wireGrip, remember, place, follow, reachable, wireBackdrop };
}

/* ---- a body that scrolls and holds nothing to focus is a stop of its own ----------------------------------------- */
const stops = new WeakSet();

function reachable(panel) {
  if (core.kindOf(panel) === "popover") return;
  panel.querySelectorAll(".overlay__body").forEach((body) => {
    if (body.closest("[data-overlay]") !== panel) return;
    const scrolls = body.scrollHeight > body.clientHeight + 1;
    if (scrolls && !body.hasAttribute("tabindex") && !core.tabbables(body).length) {
      body.tabIndex = 0;
      stops.add(body);
    } else if (!scrolls && stops.has(body) && document.activeElement !== body) {
      body.removeAttribute("tabindex");
      stops.delete(body);
    }
  });
}

/* ---- a native modal's ::backdrop: a press that went down AND came up outside the panel's box ---------------------- */
const backdrops = new WeakSet();

function wireBackdrop(panel, record) {
  if (backdrops.has(panel)) return;
  backdrops.add(panel);
  const outside = (event) => {
    const box = panel.getBoundingClientRect();
    return event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom;
  };
  panel.addEventListener("pointerdown", (event) => {
    record.downOnScrim = event.target === panel && outside(event);
  });
  panel.addEventListener("click", (event) => {
    const down = record.downOnScrim;
    record.downOnScrim = false;
    if (!down || event.target !== panel || !outside(event) || !record.modal) return;
    if (core.kindOf(panel) === "alert" || panel.hasAttribute("data-overlay-dirty")) return;
    core.close(panel, { reason: "scrim" });
  });
}

/* ---- history: Back closes a panel that asked for it ------------------------------------------------------------ */
function remember(panel, record, history) {
  const url = typeof history === "object" && history.url ? history.url : window.location.href;
  const state = { ...(window.history.state || {}), ileOverlay: panel.id };
  if (record.pushed || (typeof history === "object" && history.replace)) {
    window.history.replaceState(state, "", url);
  } else {
    window.history.pushState(state, "", url);
    record.pushed = true;
  }
}

/* ---- the grip of a sheet: dragged down, it follows the finger; let go past a third or fast, the sheet leaves ----- */
function wireGrip(panel, record) {
  let start = null;
  // the scrim follows the drag only while it stands under this sheet
  const scrimOf = () => (core.topTrapped() === panel ? core.scrim() : null);
  const reset = () => {
    panel.removeAttribute("data-overlay-dragging");
    panel.style.removeProperty("translate");
    panel.style.removeProperty("--overlay-drag");
    const scrim = core.scrim();
    if (scrim) {
      scrim.style.removeProperty("--overlay-drag");
      scrim.removeAttribute("data-overlay-dragging");
    }
  };
  panel.addEventListener("pointerdown", (event) => {
    const grip = event.target.closest("[data-overlay-grip]");
    if (!grip || !panel.contains(grip) || event.button !== 0 || !record.open) return;
    start = { y: event.clientY, last: event.clientY, lastTime: event.timeStamp, speed: 0, id: event.pointerId };
    grip.setPointerCapture(event.pointerId);
    panel.setAttribute("data-overlay-dragging", "");
    const scrim = scrimOf();
    if (scrim) scrim.setAttribute("data-overlay-dragging", "");
  });
  panel.addEventListener("pointermove", (event) => {
    if (!start || event.pointerId !== start.id) return;
    const delta = Math.max(0, event.clientY - start.y);
    const elapsed = event.timeStamp - start.lastTime;
    if (elapsed > 0) start.speed = (event.clientY - start.last) / elapsed;
    start.last = event.clientY;
    start.lastTime = event.timeStamp;
    panel.style.translate = `0 ${Math.round(delta)}px`;
    const drag = Math.min(1, delta / Math.max(1, panel.offsetHeight)).toFixed(3);
    panel.style.setProperty("--overlay-drag", drag);
    const scrim = scrimOf();
    if (scrim) scrim.style.setProperty("--overlay-drag", drag);
  });
  const release = (event) => {
    if (!start || event.pointerId !== start.id) return;
    const delta = Math.max(0, event.clientY - start.y);
    const fast = start.speed > 0.6 && delta > 24;
    const far = delta > panel.offsetHeight / 3;
    start = null;
    reset();
    if (event.type === "pointerup" && (far || fast) && !panel.hasAttribute("data-overlay-dirty")) {
      core.close(panel, { reason: "grip" });
    }
  };
  panel.addEventListener("pointerup", release);
  panel.addEventListener("pointercancel", release);
}

/* ---- without anchor positioning: the menu's place, computed — on the trigger's inline end, flipped and clamped -- */
function place(panel, trigger) {
  if (!trigger || core.asSheet(panel) || !core.popoverOpen(panel)) return;
  const { GAP, EDGE, ROOT } = core;
  const box = trigger.getBoundingClientRect();
  const width = panel.offsetWidth;
  const height = panel.offsetHeight;
  const viewWidth = ROOT.clientWidth;
  const viewHeight = ROOT.clientHeight;
  const rtl = getComputedStyle(panel).direction === "rtl";
  let left = rtl ? box.left : box.right - width;
  if (left < EDGE || left + width > viewWidth - EDGE) left = rtl ? box.right - width : box.left; // the other side
  left = Math.min(Math.max(left, EDGE), Math.max(EDGE, viewWidth - width - EDGE));
  let top = panel.getAttribute("data-overlay-side") === "above" ? box.top - GAP - height : box.bottom + GAP;
  top = Math.min(Math.max(top, EDGE), Math.max(EDGE, viewHeight - height - EDGE));
  panel.style.left = `${Math.round(left)}px`;
  panel.style.top = `${Math.round(top)}px`;
}

/** A placed menu follows its trigger while it is open. */
function follow(panel, on) {
  const record = core.recordOf(panel);
  if (on && !record.follower) {
    record.follower = () => place(panel, record.opener);
    window.addEventListener("scroll", record.follower, { capture: true, passive: true });
    window.addEventListener("resize", record.follower, { passive: true });
  } else if (!on && record.follower) {
    window.removeEventListener("scroll", record.follower, { capture: true });
    window.removeEventListener("resize", record.follower);
    record.follower = null;
  }
}
