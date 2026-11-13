# W2-A · The overlay system — senior review (w2-a-review)

One pass, design + UX + taste together, under V5.5 (implement → review once → fix → ship). Reviewer label
w2-a-review; nothing built. 11 October 2026, branch `v54-w2-a` at `4743c88` (code as of `d544ff5`; only the notes
changed since). Lane: dev server 8883 from this worktree on `ile_v5_l3` (`ILE_REFERENCE_DATE=2026-10-03`,
`DB_CONN_MAX_AGE=0`, `--noreload`, `ILE_DESIGN_PREVIEW=1` for the board), sessions minted with `Client.force_login`
by a scratch script (person, company, staff; no password used, typed or stored); one headless Chromium at a time on the
reviewer's profile; every series behind the benchmark lock; no run ended on a crash. Evidence:
`C:/tmp/ile_v5_council/evidence/v54/w2-a/review/` (E/ below).

## Verdict — SHIP_AFTER_FIXES

No P0. The system is one system: one sheet, one module, native elements. On the desktop it is at the bar: the row menu,
the rail's word and the dialogs (seen on the board, since no product page draws one yet) are calm, fast and exact. The
drawer does everything the brief asks, in both directions.
**One major blocks shipping: on a phone the two menus become sheets with no scrim and no name, and the tap that
dismisses them reaches the page.** Four minors.

## Major

### M1 — A menu shown as a phone sheet lets the dismissing tap through, and does not say what it acts on

**Where:** at ≤ 40rem, the account popover (every console page) and the row menu («Mes documents»); fr and ar, 390 and
360.

**What happens:** both menus become bottom sheets with no scrim, no head and no «Fermer». The page above stays bright
and live, so the natural gesture to dismiss the sheet (a tap above it) also acts on whatever it lands on:
- With the row menu open on «Mes documents», a tap on the search field closed the menu **and** focused the field
  (fr and ar). On a phone the keyboard rises.
- A tap on the «Manquant» filter closed the menu **and** navigated to `?état=missing` (fr and ar; E/passthrough.json).

**Why it is below the bar:** the row menu's sheet sits at the foot of the screen, far from its «⋮», and nothing
visible says which piece it is for. The piece's title is only the popover's `aria-label` (E/phone/*-rowmenu.png). A
transient menu shown as a sheet with no scrim is a hybrid that native action sheets and the products we measure
against do not ship. It is also not what the system's own sheet is: plan §1.14 / DS V5 §10.6 say «≤ 640 px: bottom
sheet», and the system's bottom sheet (PR10) has the scrim and the head. DL54-74 item 3 rejected a scrim because a
popover's `::backdrop` does not take the press. It did not weigh the system's own `.overlay-scrim`, which is a real
element and does take it.

**Fix (one direction):**
- At ≤ 40rem a popover shown as a sheet draws the shared `.overlay-scrim` under it: opacity only, on the sheet's
  clocks, no trap and no scroll lock.
- The scrim takes the whole press. Pointerdown → click closes the menu (reason `light`, focus as today), and the press
  goes no further: the page is never reached.
- The sheet gets one head line with the menu's name: its existing `aria-label` (the piece's title, «Mon compte») in the
  head's small secondary ink, above the rows. These are live strings and data; no new copy.
- It stays a menu: Esc, the focus leaving, a choice. Anchored menus on wider screens are unchanged.
- Update CONTRACT §2 / §3 and DL54-74 item 3. In `test_overlays_console_browser_w2_a.py`, prove the two taps above (the
  field, the filter link) reach nothing.

## Minor

**m1 — The drawer's cold open sits on the INP budget's edge.**
- Measured: Arabic «Mes documents», 412 × 823 @1.75, touch, CPU × 4, cold (a fresh browser per sample), n = 18 over
  two runs, on a shared machine (two other lanes running browser suites; ≈ 38 % CPU, 1.1–1.9 GB free). The drawer
  opens at median 168 ms and p90 215–232 ms (by percentile method; range 120–272), so above the 200 ms target on this
  machine. Every open holds a long task of 93–194 ms. It closes at p90 112–144 ms.
- For comparison: the account popover opens at p90 120 ms and the row menu at 128 ms (E/inp*.json). The implementer
  measured the drawer at p90 168 ms (n = 9).
- Not a regression: it is better than W3-A's merged drawer, 160 / 240 ms with `html:has(.console-drawer[open])`.
- Where the time goes (three cold traces, E/trace.json): the tap's click handler takes 85–143 ms. Inside it, the
  module's synchronous reads force the drawer's first style pass (176 elements, 37–57 ms) and its first layout
  (182 objects, 30–66 ms): focusing the current entry and checking visibility both need the just-shown panel laid out.
  Paint then takes about 53–65 ms.
- That is the cost the plan's INP item 1 («each dialog laid out in advance, at idle») exists to remove, and it is not
  applied to the drawer. The closed drawer is `display: none`, so every open lays out the rail's whole copy in the tap.
- No change asked to ship. Wave 4's measure on a quiet machine and a real mid-range Android decides. If p90 still
  exceeds 200 ms there, item 1 is the lever.

**m2 — O10 (the WebKit / Firefox smoke) did not run** (no binaries on this machine, none downloaded).
- I ran the one path Chromium never takes: placement without anchor positioning. `CSS.supports('position-area')` was
  stubbed false before `overlay.js` loaded and the `@supports` block was neutralised. `placeByScript` then puts the row
  menu and the account popover exactly where anchor positioning does: inline end on inline end in fr and ar, 4 px
  away, the flip above, following the scroll (E/fallback.json).
- Still owed: open, close, Esc, focus return and the trap on Safari and Firefox, above all iOS Safari's scroll lock
  under the trapped drawer. This belongs to Wave 4's cross-engine pass, before W2-C2 ships the public phone sheet on
  the same module.

**m3 — The console bar's account trigger is named only by the person's short name** («qa-person»).
- Below 48rem it shows only a glyph. A screen-reader user hears a name, not what the button opens. «Mon compte» is
  read only once the popover is open (its group label) or from the landmark.
- Fix: name the button «‹short name› — Mon compte»: the visible text first (WCAG 2.5.3), from two live strings.
- Same as V4's summary; not a regression.

**m4 — Stale leftovers.**
- `static/css/components.css`'s reduced-motion block still names `.dialog[open]`, V2's dialog, deleted with §21.
- The header of `static/css/v5/overlays.css` still says a modal kind opens with `showModal()`, with the platform's
  inertness and Esc. The INP rule changed that (`show()` + the trap; its §3 comment is right).
- Delete the first; correct the second.

## What holds — measured on the real pages

| Check | Result |
|---|---|
| Drawer — 390 / 360, person · company · staff, fr · ar | `aria-modal`; focus on the current page's entry; Tab ×40 (×45 in the scroll check) and Shift+Tab ×12 never leave it; a scripted focus outside comes back; the point outside the panel is the scrim (the page takes no press); Esc, the scrim and a close request (`requestClose()`, as Android's Back sends it) close it with focus back on «Menu», a link closes it and navigates; scroll kept at 400 px in every path; the drawer's language list takes Esc first and the drawer stays (DL54-69) |
| Motion | «Slide» from the reading edge (−100 % fr, +100 % ar) in ≈ 320 ms, out in ≈ 200 ms; O1 retarget continuous both ways (closed at −29 %, reversed from there; reopened at −81 %, continued from there); keyboard opens at rest on the first frame; reduced motion opacity only, 80 ms, `translate: none` on every frame; the popover's 4 px drop + opacity in ≈ 200 ms |
| Row menu — 1440 · 1366 × 657, person · staff, fr · ar | 4 px from «⋮», inline ends equal (0 px, fr right · ar left), flips above near the foot; focus on the first row; arrows, End; Esc and «⋮» again give focus back; another «⋮» switches menus; Tab out closes (S-7); content unmoved; the tooltip after the wait, gone on Esc |
| Account popover | sheet at ≤ 40rem with 44 px rows (see M1); in the band (820 touch, 1000 mouse) hangs from its trigger with inline ends equal, fr · ar |
| O11 — the rail's word | compact rail (1200 × 700; 1366 × 657 folded), fr · ar: whole, 6 px beyond the rail's edge (right in fr, left in ar), never over the next control; hoverable; gone on Esc; at once on keyboard focus; the warm group shows a neighbour at once; sign-out's word too |
| Targets · forced colours · RTL | every phone target ≥ 44 px (Menu 70 × 66, «Fermer» 44, rows 44, trigger 44); a `CanvasText` edge on the drawer, the sheets and the menu; drawers mirror, sheets do not, menus on the inline end |
| Modal family (board, the real components and module) | the alert focuses «Annuler», refuses the scrim, Esc = the safe answer; the dialog with a field focuses the field; focus back on the opener; sheets at 390, mirrored head and foot in Arabic |
| Health | 0 console error and 0 CSP violation in every run; 0 horizontal overflow on the 82 page views at 1440 (every page of the three personas' rails and their two public links, fr · ar) |

**W3-A's shell — no regression found:**
- The drawer, the rail's toggle and arrows (the drawer's too: correction 10), widening past 64rem (closes the drawer;
  focus to the rail), the no-script path (`:target` shows the drawer; its close link leads back) and the rail's word
  all behave.
- The drawer gained an exit and a retarget, and lost W3-A's `:has()` cost.
- One deliberate change: the word shows on keyboard focus (`:focus-visible`), not after a pointer's press.
- Tests on this tree: `test_overlays.py` + `test_overlays_console_w2_a.py` + `test_console_shell_w3_a.py`, 99 passed;
  W3-A's two browser suites + `test_overlays_console_browser_w2_a.py`, 71 passed (12 min 56 s, no crash). Both runs
  used `test_ile_v5_l3`, one pytest at a time, with the lane server stopped.

**Old code left:** nothing on a console page.
- The rail's language stays a `<details data-dropdown>`, now owned by `overlay.js`.
- The letterhead's V4 account menu (public pages, and `/compte/profil/`, which renders in the public shell) is W2-C2's
  by plan, served by `main.js`'s fallback.
- No `data-dialog-*` hook, `confirm()` or other modal code remains.

## Method

Scripts outside every repository, in `C:/tmp/ile_v5_council/.work/w2-a/w2-a-review/`: `explore.py`, `phone.py`,
`scrolljump.py`, `passthrough.py`, `desktop.py`, `extra.py`, `inp.py`, `trace.py`, `board.py`, `fallback.py`. Each
writes its JSON and captures under E/.
