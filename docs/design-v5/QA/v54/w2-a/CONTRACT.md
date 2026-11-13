# W2-A · The overlay system — the primitive contract

One page, written before the code (V5.4 plan §3.4 item 1, «publishes first»). W2-C2 (the phone sheet, the targa
popover), W3-C (the preview drawer, the filter sheet) and W2-A's own propagation (the console drawer, the account
popover, the row menu) build on it. Decisions: plan §1.14 (O1–O11), §1.5 (MS-O2, MS-O4, MS-O5, MS-O6), DS V5 §10.6.
If the code and this page disagree, the code is wrong.

**Files.** `static/js/src/overlay.js` (behaviour; bundle `static/js/dist/overlay.js`) and its rarer parts
`static/js/src/overlay/extras.js` (imported on demand: §6) · `static/css/v5/overlays.css` (in `main.css`, after
`v5/tabs.css`: what every page may draw) and its page-only part `static/css/v5/_overlay-panels.css` (entry
`apps/core/static/core/overlay-panels.css`, built to `css/dist/core/overlay-panels.css`: §1, «Shared and page-only»)
· `templates/components/{dialog,drawer,popover,tooltip,sheet}.html`.
**Native elements:** a `<dialog>` for every modal kind, `popover` + `popovertarget` for menus, the control's own
`::after` for the tooltip. Script adds what the platform does not give; nothing waits for a motion. **The INP rule
fired** (plan §1.14; `NOTES.md` «INP»): `showModal()` makes the whole page inert and restyles every element, so a modal
kind opens with `show()` + `aria-modal="true"` + `closedby="closerequest"` over ONE shared scrim, with the trap in
script, and the rest of the page `aria-hidden` while it is open (an engine prunes nothing for `aria-modal` alone; never
`inert`, which re-styles every element); `data-overlay-modal="native"` keeps `showModal()` where a page is light.

## 1 · Families, elements, anatomy

| Family | Element and class | Opened by | ≤ 40rem (640 px) |
|---|---|---|---|
| Modal dialog | `<dialog class="overlay overlay--dialog" data-overlay="dialog">` | `open()` → `show()` + the scrim + the trap | bottom sheet |
| Alert dialog | the same + `overlay--alert`, `role="alertdialog"`, `data-overlay="alert"` | idem | bottom sheet |
| Drawer | `<dialog class="overlay overlay--drawer" data-overlay="drawer" data-overlay-edge="end\|start">` | modal: as the dialog; `data-overlay-modal="none"`: `show()` alone (the preview drawer, beside the list) | modal: full width · non-modal: a modal sheet |
| Bottom sheet | `<dialog class="overlay overlay--sheet" data-overlay="sheet">` | as the dialog | — |
| Popover / menu | `<div class="overlay overlay--popover" data-overlay="popover" popover>` + a `popovertarget` trigger | the trigger (native, or `open()` → `showPopover()`) | bottom sheet over the one scrim, headed by its name — still a menu (§2); `data-overlay-phone="none"` keeps it anchored |
| Tooltip | one shared top-layer `.tooltip` (`popover="manual"`) for `data-tip="layer"`, its text the `aria-label` or `data-tip-label`, beside its control or beyond the ancestor `data-tip-beyond` names (the rail's word, «⋮» of a row) · page-only: the control's own `::after`, text = its `aria-label` (`data-tip`), no script — never on a submit button, whose `::after` is the loader's busy key | hover (after the wait) and keyboard focus; a page may refuse it (`overlay:tip`) | none |

Anatomy of a panel with a head (dialog, alert, drawer, sheet):
`.overlay__grip` (sheet only, decorative) · `.overlay__head` [`.overlay__glyph` — a 40 px disc for a consequence ·
`.overlay__title` (`id` = the panel's `aria-labelledby`) · `.overlay__close` «Fermer», 44 × 44 at the inline end,
**always present**] · `.overlay__body` (scrolls, `overscroll-behavior: contain`) · `.overlay__foot` (pinned; the primary
at the inline end; a destructive action last, the garnet outline). A popover holds
`.overlay__body`, its rows `.overlay__item` (36 px, 44 under a coarse pointer) and `.overlay__sep` — and, when it is
named (`label`), `.overlay__caption` above them: its name in the small secondary ink, `aria-hidden` (the group's name
already says it), drawn only as a phone sheet, where the menu stands far from the trigger that names it.
Surface `--surface-raised`, a 1 px `--line-rhythm` edge, no lit arris. Shadow: popover `--shadow-3`, the others
`--shadow-4`. Radii: tooltip 4 · popover 8 · dialog, drawer and sheet 12 — a sheet's top corners, a drawer's free
edge only.

**Shared and page-only** (the owner's V5.8 CSS budget, 11 October 2026: the shared ceilings are hard; DL54-94).
`v5/overlays.css`, in `main.css`, holds what every page may draw: the panel and its motion both ways, the one scrim,
the drawer (the console's), the popover / menu — a bottom sheet on a phone, with its head line — and the top-layer
tooltip, the scroll lock, the account trigger. What no product page draws today is **page-only**, in
`v5/_overlay-panels.css`: the dialog and the alert dialog, the bottom sheet and its grip, the head / body / foot
anatomy of `dialog.html`, `sheet.html` and `drawer.html` (a drawer beside the list opens as a sheet on a phone), a
native modal's `::backdrop` and the control's own CSS tooltip with its warm group. **THE RULE: a page that draws a
dialog, an alert dialog, a bottom sheet, a drawer of `components/drawer.html`, a native modal or a CSS tooltip links
the page-only sheet in its `extra_head`** — `<link rel="stylesheet" href="{% static 'css/dist/core/overlay-panels.css' %}">`
— after `main.css`; that sheet says reduced motion, forced colours, paper and the keyboard's tier 0 again for its
families, after their rules. Today: the overlay board and the design showcase. Next: W3-E's staff consequence
dialogs, W3-F2's danger confirmation, W3-C's preview drawer and filter sheet, W2-C2's phone sheet if it is the sheet
family. A console page links nothing more: its drawer has its own head. `test_overlays.py` refuses a template that
draws a page-only part without the link.

## 2 · Scrim

ONE element, `.overlay-scrim` (made at idle by `overlay.js`), under the topmost trapped panel — `--scrim-modal`,
**opacity only, never a blur**, on that panel's clocks (§5); a `showModal()` panel (the native opt-in) uses its own
`::backdrop`, drawn the same way, reading its custom properties from its dialog (B3). **A menu shown as a sheet at
≤ 40rem stands over it too**, on the sheet's clocks — and stays a menu: no trap, no scroll lock, no `aria-hidden`
(§3, §4). Far from its trigger, a sheet over a live page let the tap that dismissed it act on whatever lay under it (a
field focused, a link followed — the W2-A review's M1). An anchored menu draws none. **The scrim holds the whole
press**, pointerdown to click (`data-held`): a menu sheet is light-dismissed on the way up, and the scrim is still under
the finger when the click comes, so the page behind is never reached; the press moves no focus. It closes a menu
(`light`), or a trapped panel only when the pointer went down **and** came up on it, never for an alert dialog, and
never while the panel holds unsaved input.

## 3 · Dismissal

| | Esc | Scrim / outside | «Fermer» | Also |
|---|---|---|---|---|
| dialog | ✓ | ✓ (§2) | ✓ | a `<form method="dialog">` button |
| alert | = the safe answer (`[data-overlay-safe]`) | never | ✓ | — |
| drawer, modal | ✓ | ✓ (§2) | ✓ | a link inside it |
| drawer, non-modal | ✓ | — | ✓ | Back, with `data-overlay-history` |
| sheet | ✓ | ✓ (§2) | ✓ | the grip, dragged down (never the only way out) |
| popover / menu | ✓ | light dismiss — as a phone sheet the press lands on the scrim and goes no further (§2) | — | the focus leaving it (S-7); choosing an item |
| tooltip | ✓ (wherever the focus is) | leaving, blur | — | a press on its control |

Back on phones: Android's back gesture is a close request — it closes a modal dialog and a popover natively. With
`data-overlay-history` (or `open(panel, {history})`) the opening pushes one history entry: Back closes the panel,
and closing it another way takes the entry back; a content swap in an open panel replaces the entry.

## 4 · Focus

- **In**, in the task of the input (state at t = 0): `[data-overlay-focus]` → an alert's `[data-overlay-safe]` → the
  current entry (`[aria-current="page"]`) → the first control of the body, then of the foot → the title
  (`tabindex="-1"`). A non-modal drawer takes its title. A popover takes its first item. A focus the module moves never
  scrolls the page (`preventScroll`); inside an open panel it is brought into the panel's own view
  (`scrollIntoView`, `nearest`) — the current entry low in a long list, the far end of the trap's wrap (WCAG 2.4.7).
- **Back**, on every close that started inside the panel (Esc, «Fermer», a choice, the grip, Back): to the opener —
  or, if the opener has left the page, to `data-overlay-return="<id>"`, else `#main-content`. A light dismiss or the
  focus leaving does not move the focus: the person already moved it.
- **The trap** (modal kinds): the page behind takes no press (the scrim) and no focus — Tab and Shift+Tab wrap inside
  the panel, a focus sent outside is brought back —, `aria-modal="true"`, and every element beside the panel's way up to
  the body is `aria-hidden` while it is open (Chromium prunes nothing for `aria-modal` alone: A11Y_PERF M2), written
  once the focus is in and taken back before it comes out — never `inert`, and no rule of the project selects
  `aria-hidden`, so nothing is re-styled; an element hidden by its own markup is left as it is. The native opt-in has
  the platform's inertness instead. A dialog's body that scrolls and holds nothing to focus is a stop of its own
  (`tabindex="0"` while it overflows, at the opening and on a resize; WCAG 2.1.1 — Chromium and Firefox do it
  themselves, Safari does not), which the trap counts.
- **Openers**: `aria-expanded` follows the panel; a dialog opener has `aria-haspopup="dialog"`; a link opener
  (`href="#id"`, the no-script path) is given `role="button"` and answers Space.
- **The leaving panel** takes no click and no Tab (`inert` from the close, B2). **Scroll lock** while a modal is
  open: `html[data-overlay-lock]` — `overflow: hidden`, plus `scrollbar-gutter: stable` when the page had a
  scrollbar (`="gutter"`): no layout shift.

## 5 · Motion — tokens only, transitions both ways (retarget, O1)

| | In | Out |
|---|---|---|
| tooltip | after `--tooltip-delay` (400), `--motion-fast` (120) opacity `--ease-enter`; a warm group (`data-tip-group`): neighbours 0 + 0 ms, cools after 400 | 0 ms |
| popover | `--motion-standard` (200) `--ease-enter`: opacity + a 4 px drop away from its trigger | `--motion-fast` (120) `--ease-enter` |
| dialog, alert | scrim `--motion-standard`; panel scale .96 → 1 + opacity, `--motion-emphasized` (320) `--ease-enter` | `--motion-fast` (120) `--ease-enter`, scrim with it |
| drawer | «Slide»: `translate: calc(100% · edge · --dir) 0`, `--motion-emphasized` (320) `--ease-enter`; the scrim with the panel | `--motion-standard` (200) `--ease-layout` |
| sheet | from the bottom, `--spring-sheet-duration` (550) `--spring-sheet`; a 48 px bleed; safe areas | `--motion-standard` (200) `--ease-layout` |

`@starting-style` for the way in; `allow-discrete` on `display` and `overlay` for the way out; nothing that shapes a
panel sits under `[open]` / `:popover-open` (B1). **From the keyboard: 0 ms** (`html[data-input="key"]`, and
`[data-instant]` for a scripted `instant` open). **Reduced motion: one `--motion-reduced` (80 ms) opacity, no
transform at any frame** (MS-O4). RTL: drawers mirror (`--dir`), sheets do not, menus align on the trigger's inline
end. Forced colours: the panel and the tip keep a `CanvasText` edge; the focus ring is `Highlight`.

## 6 · The JS API (`static/js/src/overlay.js`, an ES module)

```js
import { open, close, toggle, isOpen, initOverlays } from "./overlay.js";

open(panel, { opener, focus, instant, history })  // panel: element or id → true when open
close(panel, { reason, focus, instant })          // → true when it was open; reason defaults to "api"
toggle(panel, options)                            // → true when now open
isOpen(panel)
initOverlays(root = document)                     // wires every hook below inside root; idempotent
```

- `opener` (default: the focused element) is where the focus returns; `focus` overrides the target of §4 (an
  element, a selector, or `false`); `instant: true` = tier 0; `history: true | { url, replace }`.
- **Events** on the panel, bubbling: `overlay:open`, `overlay:close` — `detail: { reason, opener }`; `reason` ∈
  `esc · scrim · close · link · choice · light · focus · back · grip · api`. On a tooltip's control, bubbling and
  cancelable: `overlay:tip`, just before the top-layer tip shows — `preventDefault()` refuses it (the rail's word
  while the word is beside its glyph).
- **Hooks** (data-* only; classes are for styling): `data-overlay="<family>"` · `data-overlay-open="<id>"` ·
  `data-overlay-close` · `data-overlay-focus` · `data-overlay-safe` · `data-overlay-grip` · `data-overlay-edge` ·
  `data-overlay-modal="none" | "native"` · `data-overlay-phone="none"` · `data-overlay-keep` (a link or button inside a
  panel that does not close it: a content swap) · `data-overlay-history` · `data-overlay-return` · `data-tip`
  (`="layer"`) · `data-tip-side` · `data-tip-group` · `data-tip-label` (the layer tip's words where the control's name
  is its own content) · `data-tip-beyond` (a selector: the layer tip stands beyond that ancestor's edge — the rail's) ·
  `details[data-dropdown]` (a disclosure menu that is still a `<details>`: one open at a time, `aria-expanded` on its
  summary, Esc, a press outside and the focus leaving close it; an open one takes the Esc before the panel it stands
  in). **State written by script**: `[data-instant]`, `[data-overlay-side="above"]`, `[data-overlay-dragging]`,
  `--overlay-drag`, `[data-tip-off]`, `inert`, `html[data-overlay-lock]`, `data-dropdown="overlay"` (a disclosure the
  module owns: `main.js`'s fallback leaves it alone), `aria-hidden` on the page behind a trapped panel, `[data-held]` on
  the scrim for the length of a press, `tabindex="0"` on a body that scrolls with nothing to focus.
- **The layer tip follows a scroll** that moves its control — the focus's own scroll of the compact rail's list among
  them — while the control keeps the keyboard's focus or the pointer and stands in view; otherwise it goes.
- **The rarer parts**, `overlay/extras.js`, are no console page's: the grip of a sheet, Back (the history entry), the
  placement without anchor positioning, a dialog's scrolling body made a stop, a native modal's backdrop press. The
  module imports them on demand — at idle where a page draws one (`data-overlay-history`, `data-overlay-grip`,
  `data-overlay-modal="native"`, a dialog's `.overlay__body`), at once for the placement where the engine has no anchor
  positioning — and hands over what they need; a console page never fetches them.
- Who loads it: `console.js` imports it (every console page: the drawer, the account popover — its trigger named
  «‹short name› — Mon compte», the words it shows first (WCAG 2.5.3) then what it opens —, the row menu, the rail's
  disclosures and word); the design showcase loads it; W2-C2 adds it to `shell.js` (public pages) — until then
  `main.js` keeps a fallback for the letterhead's `<details>` account menu. Without the script: a `href="#id"` opener
  shows its panel in place (`:target`), at once, and «Fermer» is a link back; a popover still opens, light-dismisses
  and closes on Esc (native); a tooltip still shows on hover and focus.

## 7 · Budgets

**CSS** (gzip −9 as the stewards weigh it, `gzip.compress(data, 9)`, the bundles rebuilt from a clean dist; DL54-94):
the shared payload is under every page type's ceiling — an interior page (`main.css`) 42 152 B of 42 540, the login
47 013 of 47 392, the home 56 803 of 57 191, the console page types (`main` + `console` + `portal`) 50 893 of
50 927, «Mes pièces» 52 065 of 52 099, the company's dashboard 51 766 of 51 800. `css/dist/core/overlay-panels.css`
2 071 B, fetched only by the pages that link it (§1). What brought the merged tree (`main.css` 44 022 B, the console
page types 52 840 B) there: the page-only part (§1), the shared sheet written once per declaration (the popover and
the dialog leave on the panel's own clocks, the tip's box written once, no redundant backdrop), dead rules deleted
from the shared bundles (`NOTES.md` «Budget fix», each one proved by a grep of every tree) and the console drawer's
declarations that the system's drawer already gives.
**Script**: the core chunk every console page loads 6 466 B (plan §2.6's module budget: 4 KB), `overlay/extras.js`'s
chunk 1 600 B on demand, `dist/console.js` 1 505 B. The dialog's and the sheet's own code in the core is at most
≈ 300 B gzip (measured by stubbing it out) and is synchronous behaviour — the alert's safe answer, the guard of
unsaved input against the scrim, the drawer beside the list opened as a sheet on a phone — that a lazy chunk would
lose for an interaction made before it arrives; it stays in the core and the figure is recorded (DL54-94). The rest of
the core is what a console page uses: the drawer's trap, scrim and focus, the menus' side, anchor and measure, the
layer tip, the disclosures.
**Interaction**: no long task on open — the INP rule, measured (CPU × 4, 412 px, touch, n = 9, cold): the trapped
open p90 80 ms on the Arabic «Mes documents» once W3-A's `html:has(.console-drawer[open])` left with the console
drawer, 72 ms on the phase-3 home (`showModal()`: 200 / 168 ms); 184 / 234 elements restyled against 860 / 1 024.
Never a `:has()` over the whole document that a focus or an `[open]` re-evaluates (W2-C1's `html:has(:focus-visible)`
is now `html[data-input="key"]`). CLS 0; 0 px movement of inner rows during an exit; 0 CSP violations (CSSOM writes
only: `left`, `top`, `translate`, the anchor names, `--overlay-drag`, a trapped panel's and the scrim's `z-index`).
