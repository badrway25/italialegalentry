# W2-A shipped — 12 October 2026

**The overlay system — dialog, drawer, popover, tooltip, sheet: one native system.** Tag **`v54/w2-a`** (design-v5
`cd8674c`, the status commit, as for the earlier families); merge commit `078254b`. The owner's preview on
http://127.0.0.1:8780 serves it: v5-live checked out at the tag, 8780 restarted at 01:48 and verified. Steward's merge,
label `w2-a-merge`, under `DESIGN_V5_MERGE_LOCK` from 00:39:10 (the earlier attempt of 11 October, 20:41–20:48, stopped
at the shared-CSS gate: `NOTES.md` «Steward»). Reviewed once and fixed (V5.5): `REVIEW.md` and `A11Y_PERF.md` are both
SHIP_AFTER_FIXES with no P0; the fix pass (`NOTES.md`, «Review fixes») closed the review's major, the check's four majors
and its minor and two of the review's minors (the other two are Wave 4's, below); the budget fix (`NOTES.md`, «Budget
fix»; DL54-94) then brought every page type under its ceiling. No reviewer has read the fix pass or the budget fix again.

## What shipped

- **One system on native elements** (plan §1.14, O1–O11; `CONTRACT.md`): one shared sheet, `static/css/v5/overlays.css`
  in `main.css`; one module, `static/js/src/overlay.js`, imported by `console.js` (the rarer parts,
  `static/js/src/overlay/extras.js`, fetched on demand); five components,
  `templates/components/{dialog,drawer,popover,tooltip,sheet}.html`, each with a link opener that works without script
  (`:target`) and «Fermer» always there. The modal kinds open with `show()`, `aria-modal` and the one scrim, with the
  trap in script (the INP rule of §1.14 fired: `showModal()` re-styled the whole page at every opening; it stays an
  opt-in); the page behind a trapped panel takes neither a press nor the focus and leaves the accessibility tree while
  the panel is open; state and focus at t = 0, the focus back to the opener; transitions both ways on §1.14's clocks,
  mirrored by one `--dir`; reduced motion one 80 ms opacity, forced colours drawn, nothing moving at rest.
- **The console drawer** (below 64rem, «Menu», on every console page): W3-A's `<dialog>` is a modal drawer of the
  system — «Slide» in 320 ms and out in 200 ms from the reading edge over the one scrim, the trap, Esc / the scrim /
  «Fermer», the focus on the page one is on (brought into the panel's view) and back on «Menu», the page behind still.
  Its cold open p90 went from 504 to 144 ms on the area's measure (`A11Y_PERF.md`).
- **The account popover** (the console's top bar): a real `<button popovertarget>` named «‹short name› — Mon compte»,
  rows 44 px under a finger; at ≤ 40rem a bottom sheet over the one scrim, headed «Mon compte» / «حسابي», that stays a
  menu, and the tap that dismisses it reaches nothing (the review's M1). The letterhead keeps V4's details face until
  W2-C2 moves it onto the same popover.
- **The row menu of «Mes documents»**: «⋮» is a real button named by the layer tip; its menu is the system's popover,
  named by the piece's title, 4 px under the button on its inline end (fr and ar), with the arrows between the rows; at
  ≤ 40rem a sheet headed by the piece's title.
- **The rail's word** (O11 in the product): the compact rail's glyphs, sign-out and the words the open rail had to cut
  show the system's one top-layer tip beyond the rail's edge — 400 ms under the pointer, at once under the keyboard's
  focus, away on Esc, re-placed while a focus scrolls the rail. W3-A's `.rail__tip` and its timers left.
- **The dialog, the alert dialog, the bottom sheet and the drawer beside a list** are ready for the families that adopt
  them, in a **page-only sheet**, `css/dist/core/overlay-panels.css` (2 071 B gzip), linked only by the pages that draw
  one (CONTRACT §1; `test_overlays.py` refuses a template that draws one without the link). No product page draws one
  today; the overlay board and the design showcase do.
- **What left the cascade**: `components.css` §8 (the account menu) and §21 (the V2 dialog and its blurred backdrop),
  the row popover of `v4/workspace.css`, the drawer, the row menu's placement and the rail tip of `console.js`,
  `initDialogs` of `main.js` (its `initDropdowns` stays as the letterhead's fallback), and 77 dead selectors in eight
  shared sheets, each proved by a grep of six trees (DL54-94 item 4).

## The merge

- **The pre-merge sync.** design-v5 stood at `1c03e3b`, the commit the budget fix had already merged into the branch
  (`9c8571d`): `git merge design-v5` found the branch up to date. No conflict to resolve.
- **Numbering.** Nothing to move: W2-A's seven entries are **DL54-88 … DL54-94**, as the budget fix numbered them after
  design-v5's DL54-87 (the notes' «Budget fix» §1 says how to read the numbers written before it). The steward's
  record of the merge is **DL54-95** (`baa88cc`).
- **Ownership.** `scripts/check_ownership.py w2-a 1c03e3b` listed the 24 paths outside the slice that the family
  declares (DL54-90, DL54-92, DL54-93, DL54-94 item 9); each was read in the diff and written under w2-a with its
  reason (`5418565`): the system's new files whole (the page-only partial and its entry, `overlay/extras.js`, the board
  and its sheet), the rest as slices — `live.py`'s board row, the showcase and its demo, W3-A's `_shell.css` and its
  three test files (retargeted, their intents kept), W1-D's loader test (one anchor), `test_static_assets.py`,
  `v4/shell.css`, `v5/chrome.css`, `ACCESSIBILITY.md`, and the dead rules of seven sheets. Five slices named as written
  (`portal_chrome.html`, `console.js`, `components.css`, `main.css`, DS 2026). After it: 22 inside, 28 slice,
  23 generated, and the manifest itself, the one steward-only path (before: 24 outside). `--validate`: coherent,
  25 families, 538 entries.
- **Bundles.** On the branch, `static/css/dist` and `static/js/dist` deleted and rebuilt (`npm run build`): byte for
  byte the family's committed bundles. On design-v5 after the merge, rebuilt again from clean (`361b03d`): every CSS
  bundle byte for byte the branch's; the JS the branch's code byte for byte with three chunk names following this
  worktree's `node_modules` path (as at the w3-b merge). `scripts/regen_design_inventory.py` found one stale figure —
  DS 2026 §2's `layout.css`, written by hand as 7.5 KB, 7 784 B after the deletions — written as 7.6 KB on the branch
  before the tests (`1c6e39b`); current on design-v5 after the merge (nothing written). The capture report is
  unchanged: `capture.py` captures the home, the privacy page, the login and the 404, which draw nothing of the system
  (DL54-95 item 6).
- **Bytes — the owner's V5.8 gate** (gzip −9, before → after; DL54-95 item 3):

  | Page type | design-v5 before | after | ceiling |
  |---|---|---|---|
  | console page types (`main` + `console` + `portal`) | 50 927 | **50 893** (−34) | 50 927 |
  | «Mes pièces» (+ `documents.css`) | 52 099 | **52 065** (−34) | 52 099 |
  | the company's dashboard (+ `companies.css`) | 51 800 | **51 766** (−34) | 51 800 |
  | an interior page (`main.css`) | 41 880 | **42 152** (+272) | 42 540 |
  | the login (+ `entrance.css`) | 46 741 | **47 013** (+272) | 47 392 |
  | the home (+ `hero.css`, `pages.css`) | 56 531 | **56 803** (+272) | 57 191 |

  No page type over its ceiling; none raised, none recorded anew, none lowered. The console's shared CSS — the owner's
  named concern — is 34 B lighter. New, fetched only where it is linked: `core/overlay-panels.css` 2 071 B.
  `dist/main.css` stands 3 928 B under its 45 KB cap. JS: the overlay core chunk every console page loads is 6 466 B
  (plan §2.6: the overlay module ≤ 4 KB — recorded, not met: DL54-94 item 7, DL54-95 item 5), `dist/console.js` 2 038
  → 1 505 B; every page gains the runtime helpers' 394 B chunk while the motion library's chunk is 253 B lighter.
- **Lint and migrations.** `ruff check .`: all checks passed; `makemigrations --check --dry-run`: no changes.
- **Tests** (lane `test_ile_v5_l3`, one pytest and one browser at a time, every run behind the benchmark lock; V5.5:
  targeted, not the full suite). On the branch with the steward's commits, non-browser — `test_overlays.py`,
  `test_overlays_console_w2_a.py`, `test_layout.py` (the whole file, the account menu's slice included),
  `test_console_shell_w3_a.py`, `test_console_shell_stylesheets.py`, `tests/test_phase_console.py`, `apps/portal`,
  `apps/documents`, `tests/security`, `test_css_bundle_is_current`, `test_frontend_bundle_is_current`,
  `test_design_docs`, `test_static_pipeline`, `test_loader_rules`, `test_static_assets`, `test_design_preview`,
  `tests/test_check_ownership.py`, `tests/test_regen_design_inventory.py`: **1 077 passed**, 1 skipped (the sentinel
  test: the branch worktree's `.env` names no private table), 0 failed (14 min 11 s). Browser (headless Chromium):
  `test_overlays_console_browser_w2_a.py` **14 passed**; `test_overlays_browser_w2_a.py` +
  `tests/i18n/test_rtl_browser_overlays.py` **30 passed**; W3-A's `test_console_shell_browser_w3_a.py` +
  `test_console_phone_browser_w3_a.py` **64 passed** on the full re-run — the first run had 63 passed and 1 failed
  (`test_menu_is_reached_in_three_keys_and_opens_a_drawer_that_holds_the_whole_rail`: a press on the scrim right after
  a quick close and reopen did not close the drawer within 30 s, eight minutes into the batch on a machine shared with
  two other lanes' test runs; the test alone passed 3 of 3, then the whole batch 64 of 64; no run crashed);
  `apps/portal/tests/test_browser.py` + `tests/i18n/test_rtl_browser.py` **31 passed** — 139 browser tests passed on
  the clean runs. On design-v5 after the merge and the rebuild: the two bundle tests, `test_design_docs`,
  `test_static_pipeline`, the ownership and inventory tests, `test_overlays.py`, `test_console_shell_w3_a.py` and
  `tests/security` — **332 passed**, 0 skipped (the sentinel test ran: design-v5's `.env` names the private table)
  (5 min 33 s); `test_overlays_console_browser_w2_a.py` on the renamed chunks — **14 passed**. Logs:
  `C:/tmp/ile_v5_council/evidence/v54/w2-a/merge/`.
- `live_status.json`: the family row w2-a — state v5, its review as the decision, the tag; no surface key (see «Not
  done»). `CHANGELOG_V54.md`: the entry first.

## On http://127.0.0.1:8780 (all 200, no traceback, after the restart)

- http://127.0.0.1:8780/fr/ · http://127.0.0.1:8780/ar/ · http://127.0.0.1:8780/__design-v5/ — the strip names
  `v54/w2-a`; the index lists the family as passed, with its review
  (http://127.0.0.1:8780/__design-v5/decisioni/w2-a/REVIEW.md), and links the overlay board.
- **The overlay board** — http://127.0.0.1:8780/__design-v5/specimens/overlays/ : every family of the system open in
  French and Arabic with live strings — the dialog and the alert dialog, both drawers, the bottom sheet, the menus, the
  tooltips; a window under 640 px shows them as phone sheets (the strip's phone frame holds the site's pages, never the
  preview's own).
- **The console** — `/__design-v5/` → «Personas» → «Entrer» (no password; the preview's sessions are read-only):
  - «Personne avec dossier» (qa-doc-person): http://127.0.0.1:8780/fr/espace-reserve/mes-documents/ and
    http://127.0.0.1:8780/ar/espace-reserve/mes-documents/ — «⋮» on each row opens the row menu under its button (in
    the phone frame, a sheet headed by the piece's title over the scrim); fold the rail and pass over or Tab through
    its glyphs for their words.
  - Any persona's console page — e.g. http://127.0.0.1:8780/fr/espace-reserve/ («Personne, conditions non acceptées»,
    qa-person) or http://127.0.0.1:8780/fr/espace-reserve/entreprise/ («Entreprise — Cantiere Adriatico», qa-company)
    — in the strip's phone frame, or a window under 1024 px: «Menu» opens the drawer; the account's glyph in the top
    bar opens the account popover (a sheet under 640 px). **Reduced motion** and **forced colours**: the system's
    settings.

Checked after the restart, by request only (no browser on the owner's server;
`C:/tmp/ile_v5_council/evidence/v54/w2-a/merge/verify_8780.log`): `/fr/`, `/ar/`, `/it/`, `/en/`, the login,
`/__design-v5/`, the index, the review and the board answer 200, the strip names `v54/w2-a`, the board carries the five
families and links the page-only sheet and the module; `main.css`, the page-only sheet, `console.js` and the three
chunks it imports answer 200. Through the preview's own persona switch («Sortir» after each): qa-doc-person's dashboard
in fr, ar, it and en and «Mes documents» in fr and ar, qa-person's dashboard and qa-company's company dashboard in fr
and ar — each 200 with the system's drawer (`overlay--drawer`, «Menu» its opener) and the account popover in the markup,
«Mes documents» with three rows whose «⋮» opens a system popover; no V4 row menu, no rail tip of W3-A's; no traceback
in the server's log (`.work/servers/srv8780.log`).

## Not done

- **The V5.8 reading, for the orchestrator** (DL54-95 item 3). The gate was passed on the page types' ceilings as the
  log records them (plan §2.6 item 3), the reading of the first stop and the target the budget fix met. The
  orchestrator's note on V5.8 writes the shared ceilings as «`main.css` as it stands at `v54/w3-b`»: read as that
  sheet's weight there (41 880 B), this merge is 272 B over it on every public page type, which draws nothing of the
  system today. The lever, if that reading is meant: the console-only parts of `v5/overlays.css` (the drawer, the
  popover, the layer tip) into `console.css` — the console page types unchanged, the public page types lighter — until
  W2-C2 brings the popover to the letterhead.
- **The overlay module's 4 KB** (plan §2.6): the core chunk is 6 466 B; what would cut it is a rewrite of what the
  console uses, not a move (DL54-94 item 7). Recorded for the orchestrator.
- **Wave 4**: REVIEW m1 (the drawer's cold open on the INP edge, to be measured on a quiet machine and a real mid-range
  Android) and m2 (O10, the WebKit and Firefox smoke — no binary on this machine), before W2-C2 ships the public phone
  sheet on the same module. The first browser run's failure (the scrim press after a quick close and reopen, under
  load) did not reproduce; its cause is not established — noted for the same pass.
- **No surface key in `live_status.json`.** The system is drawn inside other families' pages (the console's chrome,
  «Mes documents»); no census id is an overlay page, so the pages keep the state their own families give them — as for
  W1-C's components and W3-A's shell. The family row and the board say what shipped.
- **Handed to other families** (`NOTES.md` «Budget fix» §7, «Handed to»): **every family that adopts a dialog, an alert
  dialog, a bottom sheet, `components/drawer.html`, a native modal or the CSS face of `components/tooltip.html` links
  the page-only sheet** — W3-E (the staff consequence dialogs), W3-F2 (a danger confirmation as a dialog), W3-C (the
  preview drawer beside the list and its phone sheet, the filter sheet), W2-C2 (its phone sheet, if it is the sheet
  family); W2-C2 — the letterhead's account menu onto the popover (`shell.js` importing `overlay.js`), after which
  `main.js`'s `initDropdowns` and `v4/shell.css`'s details face go; the notification centre (a popover, a sheet on
  phones) waits for a view that returns its asynchronous fragment (plan §3.5 item 3); W2-C1 — the letterhead's
  photographs that Chromium's lazy loader starts before `load` at 1440, and the flaky
  `test_browser_w2_c1.py::test_the_photographs_follow_the_loading_policy` (measured on design-v5's own bundles too; not
  run at this merge); W3-F1 — `layout.css`'s `.section--inverse` and `.container--narrow`, dead, left for its own merge.
  The in-flight trees (`v54-w3-c`, `v54-w3-d`, `v54-w3-f1`, `v54-w3-f2`) still carry W3-A's console drawer in
  `portal_chrome.html`: their merges meet W2-A's version.
- **Not checked at the merge:** no browser on 8780 (by rule) — the console pages were checked there by request only;
  Safari, Firefox, a real phone and a screen reader were never run; the Performance Lead's measure on the compressed
  twin 8782 was not made for this merge.
- **The full suite** was not run (V5.5: the integration checkpoint runs it).
