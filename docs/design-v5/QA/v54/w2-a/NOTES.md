# W2-A · the overlay system — implementation notes

The area's implementer (label w2-a-impl-1), under V5.5 delivery mode (implement → review once → fix → ship).
Append-only: each step adds a dated section. Heavy evidence (captures, traces, measures) under
`C:/tmp/ile_v5_council/evidence/v54/w2-a/` (E/ below), outside every repository. Lane 3: dev server 8783 on
`ile_v5_l3` (`ILE_REFERENCE_DATE=2026-10-03`, `DB_CONN_MAX_AGE=0`, `--noreload`, `ILE_DESIGN_PREVIEW=1` with
`ILE_DESIGN_PREVIEW_PORT=8783` for the board's route), pytest on `test_ile_v5_l3`, one pytest and one browser at a
time; headless Chromium (the lane's profile under `C:/tmp/ile_v5_council/.profiles/w2-a-impl-1/` for the looks);
signed-in pages through a session minted with `Client.force_login` by a scratch script — no password used, typed or
stored; never 8780, never Chrome 9222 / 9223. Every browser series and build went through
`C:/tmp/ile_v5_council/servers/lock_gate.py` first. No run reported here ended on a crash.

The direction is settled — plan §1.14 (O1–O11), §3.4 item 1; the decisions met during the build are DL54-74 …
DL54-76. No variant was built and none is proposed.

---

## Step 1 — the primitives (11 October 2026)

Branch `v54-w2-a` from design-v5 `1c001e6` (the w3-a merge and its steward notes).

### What was done

1. **The contract first** (`CONTRACT.md`, one page, committed before any code `da8bbd1`; brought in line with the
   trap mode at the end of the step): families, anatomy, scrim, dismissal, focus, motion tokens, the JS API, the
   hooks, the budgets. W2-C2 (the phone sheet, the targa popover) and W3-C (the preview drawer, the filter sheet)
   build on it.
2. **`static/css/v5/overlays.css`** (in `main.css` after `v5/tabs.css`): one anatomy (paper, hairline, head with the
   40 px glyph disc and «Fermer» 44 px, a body that scrolls, a pinned foot; rows 36 / 44 coarse); corners 4 · 8 · 12;
   shadow 3 / 4; the scrim opacity only; transitions both ways (`@starting-style`, `allow-discrete` on display and
   overlay), nothing that shapes a panel under `[open]`; the clocks of §1.14 per family (dialog .96 → 1 320 / 120,
   drawer «Slide» 320 / 200 on `--ease-layout`, sheet on `--spring-sheet` 550 / 200 with a 48 px bleed and the safe
   area, menu 4 px drop 200 / 120); one `--dir`; ≤ 40rem the dialog and the menu become sheets (a menu stays a menu:
   no scrim), a modal drawer full width, a drawer beside the list a modal sheet; the CSS tooltip (`attr(aria-label)`,
   400 ms wait, the warm group by `@property --tip-warm`, the 6 px bridge, 0 ms out) and the top-layer `.tooltip`; the
   scroll lock keeping the gutter; reduced motion one `--motion-reduced` opacity and no transform; forced colours;
   paper; tier 0 from the keyboard, last. `components.css` §21 (the V2 dialog) deleted.
3. **`static/js/src/overlay.js`** (bundle `dist/overlay.js`, 18.5 KB min, 6.0 KB gzip): `open`, `close`, `toggle`,
   `isOpen`, `initOverlays`; `overlay:open` / `overlay:close`. State and focus at t = 0; focus back to the opener or
   its successor; the dismissals of the contract; the alert's safe answer; history (Back); the menu's side chosen
   before it opens (sizes read at idle on inert clones), its anchor bound, script placement without anchor
   positioning; the leaving panel inert; the tooltip's Esc and press and the shared top-layer tip; the grip; and,
   after the INP measure, **the trap mode** (below). CSSOM writes only; nothing waits on a transition; no animation.
4. **The five components** `templates/components/{dialog,drawer,popover,tooltip,sheet}.html`: the contract's markup,
   a link opener that works without script (`:target`), «Fermer» always there, `body_template` / `actions_template`
   for a template-side caller.
5. **The board** `/__design-v5/specimens/overlays/` (`templates/dev/designpreview/specimens/overlays.html`, its dev
   sheet, one row of the preview's index): every family open in French and Arabic with live strings.
6. **The INP rule** (§1.14) measured and applied — see «INP» below: the modal kinds open with `show()`, `aria-modal`,
   `closedby` and one scrim, the trap in script; `data-overlay-modal="native"` keeps `showModal()`; and W2-C1's
   `html:has(:focus-visible)` is now `html[data-input="key"]` (one rule of `chrome.css`).
7. **`main.js`'s `initDialogs`** also closes, with the overlay system's «Fermer», a dialog it opened on a page that
   does not load `overlay.js` yet (the design showcase).
8. **DS 2026**: §2's row of `v5/overlays.css`, §7.2's 40rem, §10's five components, §12, §16; the figures the change
   moved regenerated (`scripts/regen_design_inventory.py --write`); §1.4's blurred V2 backdrop retired.

### What looking showed, and what was fixed (all before the tests were green)

- The board's French column rendered in Italian (the specimen view renders under `it`): each French cell has its
  own `{% language "fr" %}`.
- In the board's Arabic cell a menu aligned on its trigger's right edge: `position-area` reads the viewport's
  direction (the root's, Italian there) → `self-block-end span-self-inline-start`, the panel's own direction.
- A trigger's tooltip stayed over its open menu, and its Esc closed the tip instead of the menu → a control whose panel
  is open names nothing; Esc puts tips away and takes the key from nobody.
- The full-width phone drawer kept a hairline on the screen's edge → `border-inline: 0` there.
- The browser tests found three more: a link opener (`data-overlay-open` with no value) never got
  `aria-expanded="true"`; the tip's «off» rule lost the specificity contest to the hover rule; the head covered half
  of the sheet's grip.

### INP — the rule fired, and what the traces found

Lane 8783, Chromium 153 headless, 412 × 823 @1.75, touch, CPU × 4, cold (a fresh context per load), the panel
injected and the real `dist/overlay.js` imported; elements re-styled read from traces (deterministic), latencies from
Event Timing (INP's definition). E/inp/ (`inp_final.json`, `trace_real.json`, `steps.json`, `variants.json`).

| Cold open | Arabic «Mes documents» | phase-3 home, fr |
|---|---|---|
| `showModal()` — elements re-styled · style | 860 · 103 ms | 1 024 · 109 ms |
| trapped open — elements · style | 184 · 38 ms (876 while W3-A's `:has` rule stays) | 234 · 36 ms |
| `showModal()` INP median / p90 (n = 9) | 128 / 200 ms | 152 / 168 ms |
| trapped INP median / p90 (n = 9) | 64 / 80 ms (W3-A's rule removed); 160 / 240 ms with it | 64 / 72 ms |
| trapped close p90 | 80 ms | 56 ms |

- `showModal()` makes the whole page inert, a style flag every element inherits: the whole document is re-styled in
  the tap. Plan §1.14's rule item 3 → `show()` + the shared scrim + the script trap + `aria-modal` + Esc + the return.
- **`html:has(:focus-visible)` re-styled the whole document on every focus change** — every press of a link or a
  button, on every page (3 758 → 181 elements for the same opening once it was removed; style 213 → 34 ms). Replaced
  by `html[data-input="key"]`, the same behaviour (DL54-75).
- **W3-A's `html:has(.console-drawer[open])`** re-styles ≈ 700 elements at every `[open]` on a console page (a dialog,
  a `<details>`): it leaves when the console drawer moves onto the system (step 2).
- Inserting the scrim in the tap re-evaluated the page's `:has()` rules (≈ 720 elements): it is made at idle.
- The first press of a page also re-styles what the families' tier-0 rules name (`html[data-input]` changing from
  absent to «pointer»): once per page and per modality change, not per opening — left as is.
- The machine was shared and busy (23–74 % CPU across the runs): latencies moved from run to run; the element counts
  did not. One harness bug was caught and fixed before any conclusion: the first variant run called `new Function`
  in the page, which the CSP refuses — those taps opened nothing; every result above is from runs that check the
  panel opened.

### Measures

- `dist/main.css` gzip 42 386 → 44 661 B at the branch's base (+2 275: `v5/overlays.css` +3.1 KB, §21 −0.9 KB); the
  46 080 B ceiling holds (1 419 B left) — design-v5 has since merged W2-B, and the merge step measures the sum. Step 2 deletes `components.css` §8, `v4/workspace.css`'s row popover and `v4/shell.css`'s
  account menu.
- `dist/overlay.js` 18.5 KB min / 6.0 KB gzip, loaded only where a page imports it. Adding the entry moved esbuild's
  runtime helpers into a chunk of their own (`chunk-*.js`, 0.7 KB), fetched beside the others at the same depth.
- CLS: the trapped page does not move (the gutter kept where a scrollbar was; tested); 0 CSP violation, 0 console
  error on the board and on the smoke pages.

### Tests

- `tests/frontend/test_overlays.py` — 27 contract checks on the sources (the cascade, the anatomy's tokens, the
  motion, the trap's pins, the components in fr and ar, the guard against a document-wide `:has()` on the focus or an
  opening).
- `tests/frontend/test_overlays_browser_w2_a.py` — 24 browser checks on the board (Esc and the return for five
  families, the trap and the focus brought back, the still page, the scrim's three cases, Back, the menu's every way
  out, O1–O4, the tooltip and the top-layer tip, «Fermer» 44 px, the grip, the phone, the API; the native opt-in).
  The Firefox / WebKit smoke (O10) is collected only where their binaries are installed — not on this machine, never
  downloaded; its code path was run once on Chromium (`ILE_OVERLAY_SMOKE_ENGINES=chromium`, passed).
- `tests/i18n/test_rtl_browser_overlays.py` — 5 checks on an Arabic document of the real components (the drawers
  mirror and arrive from their edge, the sheet does not, the menu on the inline end, the tips, the dialog's head).
- Targeted runs, all green: the overlay tests (27 + 24 + 5); `tests/frontend/test_layout.py`, `apps/portal`,
  `apps/documents`, `tests/security`, `tests/test_phase_console.py`, the W3-A static shell tests, `test_design_docs.py`,
  the two bundle-currency tests (645 passed); `apps/portal/tests/test_browser.py` + `tests/i18n/test_rtl_browser.py`
  (31 passed); `tests/frontend/test_browser_w2_c1.py` (12, the navbar's keyboard scroll after the `chrome.css` rule);
  the tokens, motion-gate, RTL-static, custom-property, icon, preview and showcase suites (1 110 passed, 1 xfail
  as before).
- Smoke, looked at: the home, the dashboard and «Mes documents», fr and ar, 1440 and 390 (E/smoke/): unchanged, no
  overflow, nothing of the system on a page that does not draw it.

### What is left — step 2 (propagation) and others

1. **The console drawer onto the system** (`portal_chrome.html`'s drawer element, `console.js`'s drawer code — the
   slice): open/close through `overlay.js`; delete W3-A's `html:has(.console-drawer[open])` and its keyframes
   (`_shell.css`, W3-A's file: a justified path, with the shell's tests `test_console_shell_w3_a.py` and the two
   browser files updated); the INP then measures as the table's «W3-A's rule removed» row.
2. **The account popover** (`account_menu.html` → `popover.html` with its rows; the console bar's account) and the
   **row menu** (`document_row.html`'s popover → the system's popover); delete `components.css` §8,
   `v4/workspace.css`'s row popover, `v4/shell.css`'s account menu (the file); `initDropdowns` stays for the rail's
   language `<details>` until it is not one.
3. **The rail's word** (`console.js`'s `.rail__tip`, W3-A's) onto the system's top-layer tip — O11 in the product.
4. `initDialogs` retires once every page with a dialog loads `overlay.js` (W2-C2 adds it to `shell.js`).
5. The pre-merge sync with design-v5 (W2-B shipped after this branch was cut, `0c4cc46`): DS 2026's figures and
   `main.css`'s imports are the likely meeting points; the bundles are rebuilt from clean by the steward.
6. The «Définition» popover stays parked (plan §1.14, owner B).
7. Honest limits: the motion was judged on captures and sampled frames, not watched at speed; the Firefox / WebKit
   smoke did not run here; a trapped panel must sit at the body's level (no transformed or z-indexed ancestor).

---

## Step 2 — the propagation (11 October 2026)

The area's implementer (label w2-a-impl-2), V5.5 delivery mode. Checkpoint tag `v54/w2-a-pre-propagation` (`7921323`,
plan §2.2: «before any propagation step inside a family») before the first change. Lane 3 as in step 1 (8783 on
`ile_v5_l3`, `ILE_REFERENCE_DATE=2026-10-03`, `DB_CONN_MAX_AGE=0`, `--noreload`, `ILE_DESIGN_PREVIEW=1`); pytest on
`test_ile_v5_l3`; one browser and one pytest at a time; the lane server stopped during every pytest browser run;
sessions minted with `Client.force_login` for four personas — person (`qa-person`, the account with the most pieces),
company (`qa-company`), staff (`qa-admin`), operator (`demo-operateur`) — under the preview's cookie name
(`ile_v5_sessionid`): no password used, typed or stored. Every browser series and build went through
`C:/tmp/ile_v5_council/servers/lock_gate.py` first; no run reported here ended on a crash. Evidence under
`C:/tmp/ile_v5_council/evidence/v54/w2-a/step2/` (E2/ below). Decisions: DL54-77; paths outside the slice: DL54-78.

### What was done, in plan §1.14's order

1. **The console drawer** (`e5fa845`) — W3-A's `<dialog>` is a modal drawer of the system: `overlay overlay--drawer`,
   `data-overlay="drawer"`, `data-overlay-edge="start"`; «Menu» its link opener (`data-overlay-open`), the close control
   the system's «Fermer» (`data-overlay-close`), both still links without script. `console.js` imports `overlay.js`; its
   §3 is one listener (a window widened past 64rem puts the drawer and the bar's account away, the focus to the rail).
   The trap with `aria-modal`, the one scrim on the drawer's clocks, Esc, the focus on the page one is on and back on
   «Menu», «Slide» in 320 ms / out 200 ms from the reading edge (mirrored by `--dir`), at once from the keyboard, one
   80 ms opacity under reduced motion — all the system's. W3-A's measures and night stay the drawer's (320 px / 88vw
   over the system's full-width phone rule, the safe areas, `--drawer-radius`, `--shadow-4-dark`), written on the panel
   and never under `[open]` (B1). **Deleted**: `html:has(.console-drawer[open])` (≈ 700 elements re-styled at every
   `[open]` of a console page — DL54-75 item 3), the drawer's `::backdrop`, its two keyframes.
2. **Popovers and menus** (`5183091`) — `account_menu.html` has two faces, one set of rows: `popover=True` (the
   console's top bar, `menu_id="console-account"`) is a real `<button popovertarget>` and `components/popover.html`, a
   group named «Mon compte», a sheet that stays a menu at ≤ 40rem; the default stays V4's `<details>` for the letterhead
   (W2-C2's). The row menu of `document_row.html` is the system's popover named by the piece's title; «⋮» a real
   button named by the top-layer tooltip. **Deleted** (the deletion map's W2-A rows): `components.css` §8 (the account
   menu — 17 numbered sections left), `v4/workspace.css`'s row popover, `console.js`'s placement of the row menu; what
   V4's details face still needs of §8 went into `v4/shell.css`'s last block, which leaves with that face. The trigger's
   base serves both faces from `v5/overlays.css` §9.
3. **Modal and alertdialog** (`17ab68e`) — no product page draws one besides the drawer (the staff consequence dialogs
   are W3-E's, plan §3.5 item 7's gate); `initDialogs` left `main.js` with its last caller, the design showcase, whose
   two dialogs now open through the system (`data-overlay-open`, the demo's buttons `data-overlay-close`, `overlay.js`
   loaded by the showcase). The disclosures that are still a `<details data-dropdown>` (the rail's language) are
   `overlay.js`'s (`ed3db83`): one open at a time, `aria-expanded`, Esc, a press outside, the focus leaving — and an open
   one takes the Esc before the panel it stands in (DL54-69's order). `main.js`'s `initDropdowns` is a fallback that
   steps aside for every disclosure the system marks `data-dropdown="overlay"`, read at the event (overlay.js loads after
   main.js): it serves the letterhead's account menu until W2-C2. Without script a panel appears and leaves at once.
4. **The tooltip group** (`ba64bf9`) — the rail's word (W3-A's `.rail__tip`) is the system's one top-layer tip, O11 in
   the product: `data-tip-label` (the words), `data-tip-beyond` (beyond the rail's edge, never over the foot's next
   control; on the left in Arabic), a cancelable `overlay:tip` (the rail refuses the tip while a word is beside its
   glyph). A control names nothing while the overlay it opens is open (the rail's own control keeps its word). The tip
   shows on the keyboard's focus, as every tip of the system. **Deleted**: `.rail__tip`, its CSS and its forced-colours
   rule, sixty lines of timers. «⋮» of every register row carries the same tip.
5. **The notification centre is not built** — handed over (below): its content must be an asynchronous fragment
   (plan §3.5 item 3) and no view returns one.
6. Contract (`CONTRACT.md` §6: `overlay:tip`, `data-tip-label`, `data-tip-beyond`, `details[data-dropdown]`, who loads
   the module), DS 2026 prose and figures, ACCESSIBILITY.md's rows, DL54-77 / DL54-78 (`eb6e02c`); the bundles rebuilt
   from a clean dist (`d544ff5`).

### What looking showed (the captures were looked at, not only measured)

- The smoke's first pass found nothing wrong: the drawer, the account popover and the row menu opened with every
  behaviour of the contract on the first run (E2/smoke/). The looks in both directions (E2/look/: the drawer of the
  person, the company and the staff account at 390 in fr / ar; the account popover as a sheet at 390 and hanging from
  its trigger at 820 — its inline end on the trigger's, the left one in Arabic; the row menu 4 px under «⋮» at 1440, its
  tooltip; the compact rail's word beyond the rail; sign-out's word at 1366 × 657 in Arabic, beyond the rail's left edge)
  read as the system draws them.
- W3-A's no-script test found the one behaviour the move changed: following the close link, the drawer stayed on
  screen for the system's 200 ms way out → the no-script path is instant (`html.no-js .overlay { transition: none }`).
- W3-A's word test found the second: a programmatic focus after a pointer's press brought W3-A's tip; the system shows a
  tip on the keyboard's focus (`:focus-visible`) — the test now reaches the compact rail's page by its arrows.

### Measures

- **INP, the real overlays** (E2/inp/inp_console.json; Arabic «Mes documents» signed in, 412 × 823 @1.75, touch, CPU × 4,
  cold — a fresh browser per load —, n = 9 per cell; Event Timing, INP's definition; the machine at 70 % CPU, 2.6 GB
  free): the drawer opens p90 **168 ms** (median 136) and closes p90 128 ms (median 120); the account popover 88 / 48 ms;
  the row menu 104 / 40 ms; 0 interaction over 200 ms, every one checked open / closed. The drawer's close spends 63–90 ms
  in its handler (the leaving panel made `inert`, then a style read in `settle()`): inside the rule, left as is.
- **Weight** (gzip -9 of the bundles rebuilt from clean): `dist/main.css` 44 652 → **44 466 B** (−186, components.css §8,
  the row popover); `dist/portal/console.css` 5 292 → **5 061 B** (−231: W3-A's drawer rules, `:has()`, keyframes,
  `.rail__tip`); `dist/portal/portal.css` 2 263 unchanged; `dist/console.js` 2 053 → 1 505 B, and console pages now load
  the overlay chunk (`chunks/chunk-CJ6MQ2P4.js`, 6 472 B, shared with `dist/overlay.js` 142 B). The three sheets every
  console page loads weigh 51 790 B — 49 941 B at the branch's base measured the same way (DL54-73 item 3 recorded
  50 007 B at the w3-a merge) —: +1 849 B, step 1's `v5/overlays.css` (+2 266 B in `main.css`) less this step's
  deletions (−417 B). For the merge step, which DL54-73 item 3 sends back to the log.
- **Re-probe** (E2/probe/report-*.json, 306 page views): every console page type of each persona's own rail — the
  person's ten (`/espace-reserve/`, ma-situation, mon-parcours, dossiers, mes-demandes, mes-documents, mes-echeances,
  communications, guichet, formation), the company's (and «Espace entreprise»: its dashboard, mes-besoins,
  mon-entreprise), the staff's and the operator's registers (selection, guichet/confiees, guichet/designation …) —, in
  fr and ar, at 1440 × 900, 1366 × 657 and 390 × 844 (touch): 0 console error, 0 CSP violation, 0 horizontal overflow, 0
  legacy overlay left (`.rail__tip`, `.doc-menu`, a `details.account-menu` in the console); at 390 on every page the
  drawer opened with `aria-modal`, the focus on the page one is on, closed on Esc with the focus back on «Menu» and the
  lock gone, and the account popover opened as a sheet with the focus on its first row and closed on Esc back to its
  trigger; at 1440 on «Mes documents» the row menu opened 4 px under «⋮» on its inline end (fr: right edges equal; ar:
  left edges equal) and Esc gave the focus back.

### Tests

- New: `tests/frontend/test_overlays.py` +7 (34 in all; the `:has()` guard now reads the console's entry too);
  `tests/frontend/test_overlays_console_w2_a.py` (7, rendered); `tests/frontend/test_overlays_console_browser_w2_a.py`
  (7, browser — the drawer's trap and way out, the account popover in the band fr / ar and as a phone sheet, the row
  menu fr / ar with its tooltip, O11).
- Updated for the mechanism, every behaviour kept: W3-A's `test_console_shell_w3_a.py` (`:modal` → the trap,
  keyframes → none, V4's list → the popover, the drawer's hooks), `test_console_phone_browser_w3_a.py` (`aria-modal`,
  the «Slide» transition and its direction instead of a keyframe's name, the popover's box),
  `test_console_shell_browser_w3_a.py` (the popover's rows; the system's tip for the rail's word, reached by the
  keyboard); `test_static_assets.py` (main.js keeps no `showModal`).
- **Targeted runs, on the final tree (`d544ff5`), all green, 0 skip, 0 crash**:
  - without a browser, one run (16 min): `tests/frontend/test_overlays.py`, `test_overlays_console_w2_a.py`,
    `tests/frontend/test_layout.py`, `apps/portal`, `test_console_shell_w3_a.py`, `test_console_shell_stylesheets.py`,
    `tests/test_phase_console.py`, `apps/documents`, `tests/security`, `test_css_bundle_is_current.py`,
    `test_frontend_bundle_is_current.py`, `test_design_docs.py`, `test_static_assets.py` — **698 passed** (8 browser
    tests deselected, run below);
  - in the browser, one batch at a time, the lane server stopped: `apps/portal/tests/test_browser.py` +
    `tests/i18n/test_rtl_browser.py` + `tests/i18n/test_rtl_browser_overlays.py` — **36 passed**;
    `test_console_shell_browser_w3_a.py` + `test_console_phone_browser_w3_a.py` — **64 passed**;
    `test_overlays_browser_w2_a.py` + `test_overlays_console_browser_w2_a.py` — **31 passed**; and, since the trigger's
    base in `overlays.css` §9 serves the letterhead's details face too, `test_browser_w2_c1.py` + `test_browser_w1_b.py`
    — **16 passed** (the letterhead looked at as well: E2/look/letterhead-*.png, fr / ar, 1600, 1280, 390 — the seat, the
    list under its trigger, Esc through `main.js`'s fallback).
  - `ruff check` and `ruff format --check` clean on every Python file the step touched.

### Handed to

- **W2-C2 — the public account popover.** `templates/partials/header.html` includes `components/account_menu.html`
  twice (the targa's seat and the drawer's head): add `popover=True` with two `menu_id`s, `overlay.js` to `shell.js`,
  then delete `main.js`'s `initDropdowns` fallback, the details face of `account_menu.html` and `v4/shell.css` (the file;
  its header says so). `chrome.css`'s `.targa-seat .account-menu__summary` rules already draw the button (the trigger's
  base in `overlays.css` §9 resets it). The letterhead's name is still cut by an ellipsis (DS 2026 §10: «da correggere»).
- **The notification centre** (plan §3.5 item 3's gate; W3-A handed it to W2-A, DL54-73 item 4). The data exists — the
  person's inbox is `portal.Message` (`notifications.Notification` attaches to a message), the unread count is
  `portal.services.unread_count`, drawn in «Communications (n)» —, but the gate asks the centre's content as an
  asynchronous fragment and no view returns one: a new view and URL (the latest communications as rows, authorised by
  `portal.policies`, with L3's `seat()` on arrival) is backend work the brief says not to invent. The primitives are
  ready: a popover from a bell in the top bar (a sheet on phones), its body fetched on `overlay:open`, `data-overlay-keep`
  for a row that swaps. Whose: the portal's owner for the endpoint (W3-E or a steward assignment), then the shell's
  trigger (`portal_chrome.html`, W3-A's file) and `apps/portal/static/portal/v5/_notifications.css` (W3-A's slice).
- **W3-E** — the staff consequence dialogs on the modal (plan §3.5 item 7): `components/dialog.html` with `kind="alert"`.
- **W1-P** — the preview index's frame viewer (`dp-viewer`, `static/js/dev/designpreview.js`) is a dev tool of its own,
  not a product overlay: not moved.

### What is left, and honest limits

- The Firefox / WebKit smoke (O10) did not run here: no binaries on this machine, none downloaded (as in step 1).
- The console's three sheets stand 1 849 B over the branch base (above; 1 783 B over DL54-73's recorded 50 007 B): step 1's
  sheet, measured and accepted in step 1 under V5.5; this step only removes weight. The merge step says it in the log.
- Console pages now load the overlay chunk (6.5 KB gzip of script) — the plan's «console.js imports overlay.js».
- Motion judged on captures and sampled boxes (the drawer's way out caught at 320 px wide with its 12 px corners, then
  hidden), not watched at speed.
- A trapped panel must sit at the body's level (step 1's limit): the console drawer does.

### Copy packet for the owner

No new product string. Every word drawn is a live string of the catalogue or live data: «Mon compte» (the popover's
name), «Ouvrir le menu de la pièce» (now «⋮»'s `aria-label` and its tooltip — the same msgid as before, which was a
visually hidden span), the account's four rows, the rail's own labels as its words, the piece's title as its menu's
name. The design showcase (DEBUG only, never in production) had two sentences of its developer French rewritten to say
what its dialogs now are; they are not product copy.

### For the merge

- `scripts/check_ownership.py w2-a design-v5 --working-tree`: 15 inside, 9 slice, 19 generated, **13 outside** — each
  named in DL54-76 (step 1: `static/css/dev/overlay-board.css`, `templates/dev/designpreview/specimens/overlays.html`,
  `apps/designpreview/live.py`, `static/css/v5/chrome.css`) and DL54-78 (step 2: `apps/portal/static/portal/v5/_shell.css`,
  `tests/frontend/test_console_shell_w3_a.py`, `test_console_shell_browser_w3_a.py`, `test_console_phone_browser_w3_a.py`,
  `static/css/v4/shell.css`, `templates/dev/showcase.html`, `apps/core/dev.py`, `tests/frontend/test_static_assets.py`,
  `docs/ACCESSIBILITY.md`); the merge step writes them into the manifest.
- **Numbering**: design-v5 already holds DL54-74 … DL54-76 (W2-B's two entries and the steward's record of the w2-b
  merge): this branch's DL54-74 … DL54-78 are renumbered at the merge, as W3-A's were (DL54-73 item 1).
- The pre-merge sync with design-v5 meets `docs/design/DESIGN_SYSTEM_2026.md` (W2-B's prose) and `static/css/components.css`
  (W2-B's four lines of §27); the bundles are rebuilt from clean by the steward.

---

## Review fixes — the fix pass (11 October 2026)

The area's implementer for the fix pass (label w2-a-fix), V5.5 delivery mode: one pass on the senior review
(`REVIEW.md`: M1, m1–m4) and the accessibility + performance check (`A11Y_PERF.md`: M1–M4, m1). Lane 3 as before (8783
on `ile_v5_l3`, `ILE_REFERENCE_DATE=2026-10-03`, `DB_CONN_MAX_AGE=0`, `--noreload`, `ILE_DESIGN_PREVIEW=1`); pytest on
`test_ile_v5_l3`; one browser and one pytest at a time, the lane server stopped during every pytest browser run;
sessions minted with `Client.force_login` for `qa-person`, `qa-doc-person` and `qa-admin` — no password used, typed or
stored —, revoked at the end; headless Chromium on the profile `.profiles/w2-a-fix/`; every build and browser series
behind `lock_gate.py`; no run reported here ended on a crash. Evidence under
`C:/tmp/ile_v5_council/evidence/v54/w2-a/fix/` (E3/ below); scripts under `.work/w2-a/w2-a-fix/`. Decisions: DL54-79
(the log is append-only: it supersedes DL54-74 item 3 and amends DL54-75, rather than editing them).

### What was fixed

| Item | Fix | Seen working (E3/) |
|---|---|---|
| REVIEW M1 (major) — a menu sheet let the dismissing tap through, and did not say what it acts on | At ≤ 40rem a popover shown as a sheet stands over the shared `.overlay-scrim` (opacity only, the sheet's clocks; no trap, no scroll lock, no `aria-hidden`: it stays a menu). The scrim holds the whole press, pointerdown to click (`data-held`, let go on the click, a cancel, or after 1 s): the platform light-dismisses the menu on the way up, and the click that follows still lands on the scrim. The press moves no focus (mousedown's default prevented); the close gives it back as CONTRACT §4 says. The sheet is headed by its group name — `components/popover.html` draws `label` as `.overlay__caption` (`aria-hidden`, `--text-2`, `--u-small`, on the rows' inline edge), seen only as a phone sheet. | `smoke-passthrough-name.json`, 390 × 844 touch, fr and ar: a tap on the search field above the row menu's sheet → menu closed, field **not** focused (the focus back on «⋮»); a tap on «Manquant» → not followed (the URL unchanged); the account sheet's dismissing tap on a filter link → not followed; Esc → closed, focus on «⋮», scrim gone. Head lines «Extrait de casier judiciaire», «Mon compte» / «حسابي» (`rowmenu-sheet-*.png`, `account-sheet-*.png`: looked at — the page dimmed behind, the name on the inline start, the rows unchanged) |
| A11Y M1 (major) — the focus landed off-screen in the drawer | `focus()` keeps `preventScroll` for the page and then, inside an open panel, `scrollIntoView({block: "nearest", inline: "nearest"})`. | `smoke-m1focus-m2tree.json`: «Academy» whole (seen 1.0) in `qa-admin`'s drawer at 390 × 844, 844 × 390 and in Arabic at 390 × 844, and `qa-doc-person`'s in Arabic at 320 × 568 — by tap and by key; Shift+Tab across the wrap at 844 × 390 lands on «Site public», whole; `scrollY` / `scrollX` 0 in every cell (`m1-*.png`) |
| A11Y M2 (major) — the page behind the trapped drawer stayed in the tree | While a trapped panel is open, every element beside its way up to the body is `aria-hidden="true"` — written after the focus goes in, taken back before it comes out; an element hidden by its own markup left alone; never `inert`. `test_overlays.py` now guards that no rule of the project selects `aria-hidden`. | Chromium's AX tree with the drawer open: 107 nodes, the landmarks the dialog and its «Menu» alone (fr and ar; 178 / 185 before opening) — as `showModal()`'s; closed, the tree whole again, only the scrim hidden (its own), the focus on «Menu» |
| A11Y M3 (major) — the rail's word vanished when a focus scrolled the compact rail | The capture scroll listener re-places the layer tip (`placeTip`) while its control still matches `:focus-visible` or `:hover` and its middle is its own on screen (`elementFromPoint`); otherwise it hides it. | `smoke-m3words-m1zoom.json`: real Tab presses, rail compact: `qa-admin` at 1366 × 657, 13 of 13 list items' words in fr and in ar (the list 588 px in 425); `qa-doc-person` at 1100 × 600, 10 of 10 |
| A11Y M4 (major) — bytes over §2.6 | The grip of a sheet, Back (the history entry and its `popstate`), the placement without anchor positioning (and its follower), a dialog's scrolling body made a stop (m1) and a native modal's backdrop press move to `static/js/src/overlay/extras.js`, imported on demand: at idle where a page draws one (`data-overlay-history`, `data-overlay-grip`, `data-overlay-modal="native"`, a dialog's `.overlay__body`), at once where the engine has no anchor positioning. It imports nothing: `overlay.js` hands it what the parts need (`install(core)`). esbuild's helpers stay in their shared chunk (the steward's build). | No console page fetches the new chunk (none draws those hooks; Chromium anchors). Weights below. |
| A11Y m1 (minor) — a 24 px scroll region with nothing focusable at 400 % | `reachable()` (in the extras): `tabindex="0"` on a dialog's `.overlay__body` while it overflows and holds nothing tabbable (what Chromium and Firefox do and Safari does not), at the opening and on a resize; removed when it stops overflowing (unless focused); the trap's list counts it; its ring drawn inside its box. | The board at 320 × 256 @4: the alert's body 304 px in 24, `tabindex="0"`, the Tab walk «Confirmer…» → «Fermer» → the body → «Annuler» (`m1zoom-alert.png`) |
| REVIEW m3 (minor) — the account trigger named by the short name alone | The console bar's trigger is `aria-label="‹short name› — Mon compte"`: the words it shows first (WCAG 2.5.3), then what it opens; two live strings. | AX names «qa-person — Mon compte», «qa-person — حسابي» at 390 |
| REVIEW m4 (minor) — two stale leftovers | `components.css`'s reduced-motion block no longer names V2's `.dialog[open]`; the header of `v5/overlays.css` says the trap (`show()`, `aria-modal`, the one scrim, `aria-hidden`), with `showModal()` the native opt-in. | `test_the_v2_dialog_of_components_css_left_with_its_template` |
| REVIEW m1 (minor) — the drawer's cold open on the INP edge | **Not changed**, as the review asked: Wave 4's measure on a quiet machine and a real mid-range Android decides; if its p90 still exceeds 200 ms, plan §1.14's INP item 1 (the closed drawer laid out at idle). The fixes add no style or layout to the open: `aria-hidden` costs 0–1 style recalculation (≤ 0.7 ms, A11Y_PERF's probe) and `scrollIntoView` reads the layout the focus has just made. | — |
| REVIEW m2 (minor) — O10 not run | **Not run**, as the review asked: Wave 4's cross-engine pass (no WebKit or Firefox binary on this machine, none downloaded), before W2-C2 ships the public phone sheet on the same module. | — |

Also: the board's two account popovers are named «Mon compte» (their phone sheet shows the head line); the row menus of
the board stay unnamed (a dev board).

### Measures

- **Script** (gzip −9 without a name, the bundles rebuilt from a clean `static/js/dist`): the core chunk every console
  page loads **6 491 B** (6 472 B before: the five fixes went in and the rarer parts came out); the on-demand chunk
  **1 600 B** (`chunks/extras-*.js`), fetched by no console page; `dist/console.js` 1 505 B and `dist/overlay.js`
  143 B unchanged. Still over §2.6's 4 KB module budget: the merge step records the budget (DL54-79 item 5).
- **CSS** (gzip −9, no name, rebuilt from a clean `static/css/dist`): `dist/main.css` 44 466 → **44 523 B** (+57: the
  head line, the held scrim, the scrolling body's ring); `dist/portal/console.css` 5 061 B and `portal.css` 2 263 B
  unchanged. The three sheets every console page loads: 51 847 B — 1 906 B over the branch base's 49 941 B (A11Y_PERF
  M4: +1 849 B), 1 840 B over DL54-73's recorded 50 007 B — the merge step's to record (DL54-79 item 5).
- DS 2026's one figure the change moved, regenerated: `v5/overlays.css` 29.7 → 31.6 KB (its comments).

### Tests

- **New and updated** — the console's eight new or changed browser checks were run once against the code before the
  fix (the previous `static/js` restored in the worktree, then put back): all eight failed with the reported defects
  (the field focused, the menu sheet without scrim, «Academy» at seen < 1, the skip links unhidden, the words of «Mes
  échéances» and «Communications» missing, fr and ar), and pass on the fix. (The board's 400 % check was not run so:
  before the fix the body carried no `tabindex` at all.)
  - `tests/frontend/test_overlays_console_browser_w2_a.py` (7 → 14): `test_a_menu_sheet_takes_the_whole_press_that_dismisses_it`
    (fr, ar: the search field, the filter link); `test_on_a_phone_the_account_popover_is_a_sheet_that_stays_a_menu`
    (the scrim, the head line, no trap, no lock, Esc); `test_the_drawer_brings_the_focused_entry_into_its_view`
    (390 × 844, 844 × 390; tap and key; Shift+Tab's wrap); `test_the_page_behind_the_drawer_leaves_the_accessibility_tree`;
    `test_the_compact_rails_word_follows_the_keyboard_down_a_list_that_scrolls` (fr, ar).
  - `tests/frontend/test_overlays_browser_w2_a.py` (+1): `test_at_400_percent_a_scrolling_body_with_nothing_to_focus_is_a_stop`;
    the phone test's menu sheet over the scrim, the account popover's head line.
  - `tests/frontend/test_overlays.py` (34 → 37): the head line and the held scrim; the rarer parts behind the dynamic
    import and nowhere in a console page's markup; `aria-hidden` after the focus goes in and before it comes out, no
    rule selecting it, the focus's scroll inside an open panel only, the tip's scroll; the extras CSSOM-only too.
  - `tests/frontend/test_overlays_console_w2_a.py` (the trigger's name and the head line, fr / ar);
    `tests/frontend/test_console_shell_w3_a.py` (its trigger pin allows the name: DL54-78's path).
- **Targeted runs on the final tree, all green, 0 skip, 0 crash:**
  - without a browser, one run (17 min 21 s, the machine shared): `tests/frontend/test_overlays.py`,
    `test_overlays_console_w2_a.py`, `test_console_shell_w3_a.py`, `test_console_shell_stylesheets.py`,
    `test_design_docs.py`, `test_layout.py`, `test_static_assets.py`, the two bundle-currency tests,
    `test_components_w1_c.py`, `test_chips_cards_w1_c.py`, `test_icons.py`, `test_loader_w1_d.py`, `test_v4_tokens.py`,
    `test_v5_tokens.py`, `tests/i18n/test_rtl_static.py`, `tests/test_check_ownership.py`,
    `tests/test_regen_design_inventory.py`, `tests/test_phase_console.py`, `apps/portal`, `apps/documents`,
    `tests/security` — **1 408 passed** (30 browser tests deselected, run below);
  - in the browser, one batch at a time, the lane server stopped: `test_overlays_console_browser_w2_a.py` — **14
    passed**; `test_overlays_browser_w2_a.py` + `tests/i18n/test_rtl_browser_overlays.py` — **30 passed** (the grip,
    Back and the native backdrop through the on-demand chunk); W3-A's `test_console_shell_browser_w3_a.py` +
    `test_console_phone_browser_w3_a.py` — **64 passed** (the drawer and the rail with the new `aria-hidden`, focus
    and tip); `apps/portal/tests/test_browser.py` + `tests/i18n/test_rtl_browser.py` + `test_browser_w2_c1.py` +
    `test_browser_w1_b.py` — **47 passed** (the console in both directions; the letterhead, whose details face shares
    `main.css`).
- `ruff check` and `ruff format --check` clean on every Python file the pass touched.

### For the merge

- `scripts/check_ownership.py w2-a design-v5 --working-tree`: 17 inside, 9 slice, 20 generated, **14 outside** — step 2's
  thirteen (DL54-76, DL54-78) and `static/js/src/overlay/extras.js` (DL54-79 item 8). `static/css/components.css`
  counts as «slice» (w2-a's §8 and §21): the one selector deleted, V2's `.dialog[open]`, stood in the universal
  reduced-motion block, which is W1-D's slice — §21's leftover, deleted at the review's request (DL54-79 item 8).
- **Numbering**: DL54-79 joins this branch's DL54-74 … DL54-78 in the renumbering at the merge.
- **Copy packet**: no new string. The head lines are the groups' existing names (the piece's title, «Mon compte»);
  the trigger's name joins two live strings with the em dash the console's tiles already use.
- Handed on, unchanged by this pass: REVIEW m1 (the INP edge) and m2 (O10) to Wave 4; the A11Y observation on the CSS
  tip's forced-colours bridge (cosmetic, not counted) is not changed.

---

## Steward — the merge stopped at the shared-CSS gate (11 October 2026, 20:41–20:48)

The steward (label w2-a-merge), under `DESIGN_V5_MERGE_LOCK` from 20:41:28, released at the end. **Nothing was
merged**: design-v5 stays at `d40f209`, v5-live at `0a8299d` (`v54/w3-b`), 8780 was not restarted, no `v54/w2-a`
tag. This branch is as the fix pass left it (`23cbfb1`), plus this section. Evidence:
`C:/tmp/ile_v5_council/evidence/v54/w2-a/merge/budget_gate.log`; scripts: `.work/w2-a/w2-a-merge/`.

**What was done.** The pre-merge sync (`git merge --no-commit design-v5`, 77 commits: W2-B's login, the static
pipeline, W3-B's dashboards). The CSS sources merged clean (`components.css` and `v4/workspace.css` auto-merged). The
conflicts were the decision log (numbering below), DS 2026 (five hunks, both areas kept, by
`.work/w2-a/w2-a-merge/resolve_ds.py`) and three bundles. `static/css/dist` and `static/js/dist` were deleted and
rebuilt (`npm run build`), then weighed. The gate failed, so the sync was undone (`git reset --hard 23cbfb1`; the
worktree had been clean before it).

**The gate** (the owner's V5.8 and the orchestrator's reading of it, the V5_5 addendum of 11 Oct 19:40: «the shared
bundles' ceilings … are hard — no merge raises them … a merge that grows it is sent back, not recorded as a new
ceiling»; plan §2.6 items 3 and 5; DL54-87 item 3: the once-only raise is spent). gzip as the stewards measure it,
`gzip.compress(data, 9)` (it reproduces DL54-73's 50 007 B and DL54-87's 50 927 B; this notes file's figures are GNU
`gzip -9 -n`, 54–66 B lighter on `main.css`):

| Page type | design-v5 `d40f209` | merged (rebuilt) | change | ceiling | over by |
|---|---|---|---|---|---|
| console page types (`main` + `console` + `portal`) | 50 927 | 52 840 | +1 913 | 50 927 (DL54-87) | **1 913** |
| «Mes pièces» (+ `documents.css`) | 52 099 | 54 012 | +1 913 | 52 099 | 1 913 |
| the company's dashboard (+ `companies.css`) | 51 800 | 53 713 | +1 913 | 51 800 | 1 913 |
| an interior page (`main.css`) | 41 880 | 44 022 | +2 142 | 42 540 (42 461, DL54-73, + 79, DL54-76) | 1 482 |
| the home (+ `hero.css`, `pages.css`) | 56 531 | 58 673 | +2 142 | 57 191 (DL54-87) | 1 482 |
| the login (+ `entrance.css`) | 46 741 | 48 883 | +2 142 | 47 392 (DL54-76) | 1 491 |

`dist/main.css` +2 142 B (`v5/overlays.css` less the deletions); `dist/portal/console.css` −229 B. `main.css` stays
2 058 B under its 45 KB cap (46 080 B), but every page type is over its own ceiling. **DL54-79 item 5's request —
«the merge step records … the page types' ceilings» — cannot be met: V5.8 forbids exactly that.**

**Where the bytes are.** `v5/overlays.css` costs about 2 650 B of the merged `main.css` (marginal, node zlib -9):
§1 the clocks 43 · §2 the panel 461 · §3 open / closed 312 · §4 the families 577 · §5 ≤ 40rem 129 · §6 the tooltip 467 ·
§7 the lock 33 · §8 no script / reduced motion / forced colours / touch / paper / keyboard 272 · §9 the account
trigger 59. Product pages draw three parts of the system: the drawer (`portal_chrome.html`, every console page), the
popover (the console's account and «Mes pièces»' row menu, as a sheet at ≤ 40rem) and the layer tip (`data-tip="layer"`,
the rail's words). **No product page draws** the dialog / alertdialog family, the bottom-sheet family and its grip, or
a native modal's `::backdrop`: only the board and the design showcase do.

**What the merge needs, on the merged tree** (V5.8: the family moves its rules into page-only sheets or deletes what
they replace; quality is not cut):
- **Console page types: ≤ 50 927 B, which leaves 0 B of headroom today.** Whatever of the system a console page loads
  must be paid for by deletions on console pages: moving overlay rules from `main.css` into `console.css` does not change
  the console total.
- **Every other page type: at most about +650 B over design-v5's `main.css`** (interior and home +660, login +651).
- The levers V5.8 names: a page-only sheet (a `css/dist` entry of its own, built by `scripts/build_css.mjs`) for what
  no shared page draws — the dialog / alert and sheet families, the grip and the native backdrop —
  linked only by the templates that draw them; the console's own parts (the drawer) out of `main.css`, which helps the
  public page types only; and deletions of legacy rules that console pages still load, to offset the drawer, popover
  and tip. Moving the undrawn families out is unlikely to clear 1.9 KB on its own (§4 is 577 B in all). If it cannot fit
  without cutting quality, the orchestrator decides: the steward may not record a raise.

**Not a V5.8 ceiling, recorded for the merge step.** Script: the overlay core chunk every console page loads is 6 466 B
gzip (plan §2.6: the overlay module ≤ 4 KB), and the runtime-helper chunk is 394 B on every page; `dist/console.js`
2 038 → 1 505 B.

**Numbering, for the next merge.** Today design-v5 holds DL54-74 … DL54-87, so this branch's DL54-74 … DL54-79 would
become DL54-88 … DL54-93 (add 14). The steward renumbers at the merge that lands, because another family's merge may
move them again. The ownership check: the 14 paths outside the slice that DL54-76, DL54-78 and DL54-79 declare,
unchanged.

---

## Budget fix — the shared-CSS budget (11–12 October 2026)

The area's implementer for the fix pass (label w2-a-fix), resumed after the steward's stop at the shared-CSS gate,
under the owner's V5.8 (the shared ceilings are hard; a surface's own CSS goes into page-only sheets; reuse and delete
first; no quality cut). **Resumed after an interruption**: the cut pass (same label, 20:56–22:40) had committed the
merge and the budget work (`b6eae23` … `2314017`) and left one uncommitted edit — the Arabic RTL document of
`tests/i18n/test_rtl_browser_overlays.py` linking the page-only sheet, the fix of the three checks that failed once the
panels left `main.css` — kept and committed (`1dc7648`); nothing was discarded. Every figure and claim of the cut pass
below was re-measured or re-read on the final tree before it was written here. This pass's commits: `1dc7648`,
`9c8571d` (design-v5 merged again), `59fe32a` (the components' headers and the guard), `c0d6037` (W1-D's loader test,
§5), `6fad77c` (DL54-94's figures) and this section. Lane 3 as before (8783 on `ile_v5_l3`,
`ILE_REFERENCE_DATE=2026-10-03`, `DB_CONN_MAX_AGE=0`, `--noreload`, `ILE_DESIGN_PREVIEW=1`); pytest on `test_ile_v5_l3`;
one browser and one pytest at a time, the lane server stopped during every pytest run; sessions minted with
`Client.force_login` for `qa-person`, `qa-doc-person` and `qa-admin` — no password used, typed or stored —, revoked at
the end (with the three the cut pass had left); headless Chromium on `.profiles/w2-a-fix-final/`; every build and
browser series behind `lock_gate.py` (the lock was never present); no run reported here ended on a crash. Evidence:
`C:/tmp/ile_v5_council/evidence/v54/w2-a/budget/` (E4/); scripts: `.work/w2-a/w2-a-fix/budget/` (the cut pass) and
`.work/w2-a/w2-a-fix/budget-final/` (this pass). Decision: DL54-94.

### 1 · design-v5 merged into the branch first (`b6eae23`, `9c8571d`)

`git merge design-v5` — 77 commits (W2-B's login, the static pipeline, W3-B's dashboards). Conflicts: the decision log,
DS 2026 (five hunks, resolved as the steward's `resolve_ds.py` does: both areas kept) and three bundles (deleted and
rebuilt from a clean dist with `npm run build`, never by hand). Merged and rebuilt, the weights are the steward's to the
byte (`main.css` 44 022 B, `console.css` 6 843 B, the console page types 52 840 B — `budget_gate.log`). design-v5 then
moved by two commits (`2e513c7`, `1c03e3b`: the confidential-material guard reads the depositant's identifiers from a
private table; the current-site finding stated without a recipe — docs, `.env.example`, a middleware docstring, two
test files), merged without conflict (`9c8571d`); nothing built or drawn changed. `static/css/dist` and
`static/js/dist` deleted and rebuilt from clean on `9c8571d`: byte-identical to the committed bundles.

**The decision log keeps design-v5's numbers; W2-A's entries follow them.** How to read the numbers written before
the merge — in this file, `REVIEW.md`, `A11Y_PERF.md` and `CONTRACT.md` alike:

| Written | Read | The entry |
|---|---|---|
| DL54-74 | **DL54-88** | the overlay system as built |
| DL54-75 | **DL54-89** | the INP rule fired; `html[data-input="key"]` |
| DL54-76 | **DL54-90** | step 1's paths outside the slice |
| DL54-77 | **DL54-91** | step 2: every overlay of a console page on the system |
| DL54-78 | **DL54-92** | step 2's paths outside the slice |
| DL54-79 | **DL54-93** | the fix pass |

Except where a W2-A text names design-v5's own: `A11Y_PERF.md`'s «design-v5's recorded figures (DL54-73, DL54-76)» and
«as DL54-44, -73 and -76 did», and the fix pass's «as DL54-44, DL54-73 and DL54-76 did» (DL54-93 item 5, which the
merge's renumbering had moved and the cut pass put back): that DL54-76 is design-v5's, the steward's record of the
w2-b merge. Every DL54-73 and lower is design-v5's. The steward's section above already writes design-v5's numbers
(DL54-76 the w2-b merge, DL54-87 the w3-b merge). The three citations outside the log (`ACCESSIBILITY.md`, DS 2026,
`v5/chrome.css`) read the new numbers. This pass's entry is DL54-94.

### 2 · Before → after, per page type

gzip as the stewards weigh it (`gzip.compress(data, 9)`, the steward's own `weigh_pages.py`), the bundles rebuilt from a
clean dist on the final tree:

| Page type | design-v5 `1c03e3b` | merged (`b6eae23`) | after (`9c8571d`) | ceiling | under by |
|---|---|---|---|---|---|
| an interior page (`main.css`) | 41 880 | 44 022 | **42 152** | 42 540 | 388 |
| the login (+ `entrance.css`) | 46 741 | 48 883 | **47 013** | 47 392 | 379 |
| the home (+ `hero.css`, `pages.css`) | 56 531 | 58 673 | **56 803** | 57 191 | 388 |
| console page types (`main` + `console` + `portal`) | 50 927 | 52 840 | **50 893** | 50 927 | 34 |
| «Mes pièces» (+ `documents.css`) | 52 099 | 54 012 | **52 065** | 52 099 | 34 |
| the company's dashboard (+ `companies.css`) | 51 800 | 53 713 | **51 766** | 51 800 | 34 |

(design-v5 `1c03e3b` weighs as `d40f209`, where the steward measured: its two new commits change no sheet.) Sheets:
`main.css` 44 022 → **42 152 B** (−1 870), `portal/console.css` 6 843 → **6 809 B** (−34), `portal/portal.css`
1 975 → **1 932 B** (−43); `dist/main.css` stays far under its 46 080 B cap. Against design-v5 itself: the console page
types −34 B, every public page type +272 B (inside the interior's, the login's and the home's ceilings). New, fetched only
where it is linked: `core/overlay-panels.css` **2 071 B**. **No page type is over its ceiling; nothing is recorded as a
new ceiling.**

### 3 · The means, in the order the brief gives them, and their bytes

Measured step by step, each step's bundles built from a clean dist (`a743c68` extracted to a scratch tree and built
there), `gzip.compress(data, 9)`:

| Step | `main.css` | `console.css` | `portal.css` | console page types |
|---|---|---|---|---|
| merged (`b6eae23`) | 44 022 | 6 843 | 1 975 | 52 840 |
| + the dead rules deleted (`a743c68`) | 43 258 (**−764**) | 6 843 | 1 932 (**−43**) | 52 033 (−807) |
| + the page-only part and the trims (`9ea3cdb`) | 42 152 (**−1 106**) | 6 809 (**−34**) | 1 932 | 50 893 (−1 140) |

1. **A page-only sheet for what no product page draws** (`9ea3cdb`) — the dialog and the alert dialog, the bottom sheet
   and its grip, the head / body / foot anatomy of `dialog.html`, `sheet.html` and `drawer.html` (with a drawer beside
   the list's phone sheet), a native modal's `::backdrop`, and the control's own CSS tooltip with its warm group (no
   product page draws it either: the product's words are the top-layer tip, which stays shared). The partial
   `static/css/v5/_overlay-panels.css`; its entry `apps/core/static/core/overlay-panels.css` (an app sheet, so
   `scripts/build_css.mjs` builds it as it is; `core` is the app of the cross-cutting interface and had no static
   directory), its import written in the collected tree (`../css/v5/_overlay-panels.css`, DS 2026 §2); built to
   `css/dist/core/overlay-panels.css` (2 071 B); linked by the overlay board and the design showcase only. The partial
   comes after `main.css`, so it says reduced motion, forced colours, paper and tier 0 again after its families.
   **The rule is in CONTRACT §1**: a page that draws a dialog, an alert dialog, a bottom sheet, a drawer of
   `components/drawer.html`, a native modal or a CSS tooltip links that sheet; `test_overlays.py` refuses a template
   that draws one without the link. This pass wrote the rule into the headers of `dialog.html`, `sheet.html`,
   `drawer.html` and `tooltip.html` (where a family adopting one reads first; `tooltip.html` still named `overlays.css`
   for the `::after` tip), and the guard now also sees `components/tooltip.html` included without `layer=True` (the CSS
   face of the component). **Worth**: put back into today's `main.css` where `overlays.css` ends, the partial would
   weigh **+1 117 B** — the panels +708, the CSS tip +409 —, an upper bound, since the partial restates reduced motion,
   forced colours, paper and tier 0 for its families.
2. **`v5/overlays.css` trimmed without changing what is drawn** (`9ea3cdb`; 31.6 → 22.3 KB of source with item 1):
   the popover and the dialog leave on the panel's own clocks instead of a copy of them; `--overlay-scrim-in` and
   `--overlay-drag` live where they are read (the native backdrop, a sheet's grip); the phone popover's two rules are
   one, without the declarations its panel already has; the top-layer tip's box is one rule; `.tooltip::backdrop`
   leaves (the platform's popover backdrop is transparent and takes no press); tier 0 is one list. **Worth**: inside one
   bundle, the trims pay for the restatements the split needs — the final sources with the partial imported back into
   `main.css` right after `overlays.css` weigh 43 269 B, against the untrimmed system's 43 258 B (`a743c68`). So the
   −1 106 B of `9ea3cdb` is the page-only part leaving, and the trims are what keeps the split from costing the shared
   sheet any byte. The same rule for the console's drawer (`_shell.css`, DL54-92's path): its place, flex column, box
   and start corners are the system drawer's, not written twice; its measures, night and the `display` that outweighs
   `.console-drawer { display: none }` stay — `console.css` **−34 B**.
3. **Dead rules deleted from the shared bundles** (`a743c68`) — `main.css` **−764 B**, `portal.css` **−43 B**. The
   criterion, the brief's: a selector is dead only if it names at least one class, id or attribute outside `:not()`
   and none of its classes, ids or attribute names appears in any template, Python, JS, JSON or SVG file of design-v5,
   of this branch and of `v54-w3-c`, `v54-w3-d`, `v54-w3-f1`, `v54-w3-f2` (tracked and untracked files) — nor in the
   installed Django forms and allauth packages, whose templates render on the product's pages —, nor as a prefix or a
   suffix a template, Python or JS builds a class from (`x--{{ v }}`, `f"x--{v}"`, `` `x--${v}` ``, `"x--" + v`); a rule
   goes when every selector of its list is dead (`cssdead.py`, a CSS parser and a token index of every file of the six
   trees and the two packages). **The proof** (`prove_dead.py`): each name grepped literally,
   `git -C <tree> grep --untracked -c -w -F -e <name> -- '*.html' '*.txt' '*.xml' '*.py' '*.js' '*.mjs' '*.cjs' '*.json' '*.svg'`
   per tree and `git grep --no-index` per package, the built prefixes and suffixes from a fresh index. **Re-run by this
   pass at 23:28 on the trees as they stand** (design-v5 `1c03e3b`, v54-w2-a `9c8571d`, v54-w3-c `4268d7f`, v54-w3-d
   `b9907ab`, v54-w3-f1 `25a3322` with its 41 uncommitted or untracked files, v54-w3-f2 `0e81923`; design-v5, v54-w3-c,
   v54-w3-d and v54-w3-f2 had moved since the cut pass's run at 21:50): 77 selectors, **0 hits for every name but
   `t-entry` and `t-ui`**, whose hits (9 lines per tree, in `apps/core/dev.py`, `test_chips_cards_w1_c.py`,
   `test_design_docs.py`, `test_v5_tokens.py`) are all the custom properties `--t-entry`, `--t-entry-lh`,
   `--t-entry-size`, `--t-ui`, `--t-ui-size` (`-w` counts `-` as a word boundary) — never the class (a second search
   for the names not preceded by `--`: 0 lines in every tree); no built prefix or suffix reaches any name.
   E4/`dead_rules_proof_final.json` (and the cut pass's `dead_rules_proof.json`, the same result). 77 selectors, 65
   whole rules and 12 out of a list, 59 names:

   | Sheet | Selectors | The names, absent from every tree |
   |---|---|---|
   | `static/css/components.css` (§12, W2-E's row) | 9 | `entrance__cta`, `entrance__illustration`, `entrance__num`, `entrance__text`, `entrance__title` |
   | `static/css/_legacy-tokens.css` | 7 | `text-display`, `text-h1`, `text-h2`, `text-h3`, `text-label`, `text-lead`, `text-legal` |
   | `static/css/base.css` | 8 | `lang-switcher`, `no-print`, `t-entry`, `t-muted`, `t-numeral`, `t-plate--caps`, `t-ui` |
   | `static/css/layout.css` | 31 | `cluster--between`, `cluster--end`, `col-4` … `col-9`, `col-start-2` … `col-start-4`, `container--flush`, `container--read`, `container--spread`, `hide-desktop`, `mb-0`, `mt-0`, `mt-8`, `mx-auto`, `section--a`, `section--b`, `section--c`, `section--header--center`, `split--even`, `zones--no-margin`, `zones--no-rail`, `zones__content`, `zones__margin`, `zones__rail` |
   | `static/css/register.css` | 15 | `plate--verso`, `plate__caption`, `plate__caption-credit`, `plate__caption-date`, `plate__caption-place`, `plate__figure`, `plate__statement`, `ref-marker`, `t-muted` |
   | `static/css/v5/base.css` (W1-A) | 4 | `on-image`, `t-entry` |
   | `static/css/v5/field.css` (W1-C) | 1 | `form__intro` |
   | `apps/portal/static/portal/portal.css` (W3-A) | 2 | `portal__aside` |

   Left on purpose: `.section--inverse` and `.container--narrow` in `layout.css`, dead too, which `v54-w3-f1` deletes in
   its own branch — deleting them here would only make its merge conflict —; and `.section--d`, the one consumer of
   `--rank-d-block`, which DS 2026 §3 documents as used (`test_reserve_labels_match_the_design_system_stylesheets` says
   so). No dead rule in `console.css`'s partials, `v4/workspace.css`, `v4/wizard.css` or `v4/hero.css`: every name there
   still appears somewhere.
4. **The script** (not a V5.8 ceiling; the brief: move the dialog and sheet code into a lazy chunk if no behaviour is
   lost, otherwise record the figure). **Recorded**: the core chunk every console page loads is **6 466 B** gzip
   (`chunks/chunk-4PT2QVVC.js`; plan §2.6's module budget: 4 KB), the rarer parts 1 600 B on demand
   (`chunks/extras-*.js`, fetched by no console page), `dist/console.js` 1 505 B (design-v5: 2 038 B) — `static/js/dist`
   unchanged by the budget fix. Stubbing every dialog- and sheet-only path out of the core (`budget/jsx/stub.js`,
   re-measured by this pass: 6 366 → 6 071 B, esbuild alone) saves ≈ 295 B — still 2 KB over the budget — and those
   paths are synchronous behaviour of the opening and of the press: the alert's Esc as its safe answer and its focus, the
   guard of unsaved input and of an alert against the scrim, a drawer beside the list opened as a sheet on a phone (and
   its title's focus beside the list), the native opt-in, a dialog another script opened with `showModal()`. A lazy chunk
   would lose them for an interaction made before it arrives, or make the opening wait for a fetch (the contract's state
   at t = 0, the INP rule); the rare parts that can wait already moved (A11Y_PERF M4). The rest of the core is what a
   console page uses: the drawer's trap, scrim and focus, the menus' side, anchor and measure, the layer tip, the
   disclosures. (The other large chunk a console page loads, 26.6 KB gzip, is the motion library behind `motion.js`'s
   `afterPaint` — design-v5's own, W1-D's, unchanged here.)

### 4 · What looking showed (nothing drawn changed)

- **The product's pages, computed** (the cut pass's `cmp_styles.py`, E4/`cmp_styles.json`, re-read by this pass): the
  computed style of every element and of every `::before` / `::after` that draws, with the fix's bundles and then with
  the merged bundles of `b6eae23` swapped in place on the same DOM in the same state — the drawer open (390, fr and ar),
  the account popover as a sheet (390) and anchored (820, ar), the row menu anchored (1440, fr and ar) and as a sheet
  (390), the compact rail's word (1100), «Mes pièces» at rest, the home (1440 fr, 390 ar), «Note legali», the FAQ, the
  glossary (ar), the login, the profile with the letterhead's account menu open (1600); the same state in all 16 cases,
  the rows' boxes equal to the pixel. Equal, but for: custom properties no rule of these pages reads (`--tip-warm`,
  registered by the page-only sheet now; `--overlay-drag`, `--overlay-scrim-in`); a menu body's `flex-grow`,
  `min-height` and `overscroll-behavior` — the body is `overflow: visible` inside a popover that scrolls itself
  (`overflow-y: auto`, `overscroll-behavior: contain`), so nothing moves or scrolls differently —; and **«⋮»'s invisible
  touch ring** (W3-C's `.doc-row__more::after`, `inset: -2px` under a coarse pointer, `v4/workspace.css`), which the
  CSS tip's rules used to hide by accident — on every phone (`@media (max-width: 40rem) { [data-tip]::after { display:
  none } }`) and, elsewhere, while its menu was open (`[data-tip][aria-expanded="true"]::after`). Those rules are
  page-only now, so the ring gives «⋮» the 48 px target W3-C's Gate C review wrote (nothing is painted; under a phone
  sheet the scrim covers it). The home's and the login's other differences are their own animations caught at two
  moments: the same elements differ in a control run that swaps in identical bundles (E4/`control/`).
- **The board, computed** (`cmp_board.py`, E4/`cmp_board.json`): `main.css` + the page-only sheet against the merged
  single `main.css`, every element, in eleven states — at rest, the alert (fr), the dialog with a field (ar), both
  drawers, the sheet, the alert and the sheet and the drawer beside the list as phone sheets, the account menu, the CSS
  tip on keyboard focus: **0 differences**. The cascade's new order (the partial after the whole of `main.css`) changes
  nothing the board draws.
- **The smoke on the lane, on the final tree** (`budget-final/smoke_final.py`, E4/`smoke-final/smoke.json` and 18
  captures, looked at): the drawer at 390 in fr and ar — from the reading edge, `aria-modal`, the focus on the page one is
  on, the scrim, Esc → closed with the focus on «Menu» and the lock gone; the account popover at 390 a sheet over the
  scrim headed «Mon compte» / «حسابي», rows 44 px, Esc back to the trigger, and at 820 hanging from its trigger, inline
  ends equal (fr right, ar left); the row menu at 1440 4 px under «⋮», inline ends equal, fr and ar, and at 390 a sheet
  headed by the piece's title over the scrim; «⋮»'s word on hover (fr, ar); the compact rail's words on Tab, every item,
  fr and ar (`qa-admin`, 1100 × 700); the board's alert and sheet at 1440 and 390 with the page-only sheet loaded,
  «Fermer» 44 × 44, 12 px corners, the shadow, the focus on «Annuler» / the current language, the Arabic sheet's head
  from the right. **0 console error, 0 CSP violation, 0 horizontal overflow.** (At 64rem and wider the console's account
  is the rail's own, so its popover has no 1440 case.)

### 5 · Tests

- **The run found one red test of this area's making** — W1-D's
  `tests/frontend/test_loader_rules.py::test_the_release_s_seat_is_the_rail_mark_and_the_bar_mark_with_the_img_for_every_other_page`
  split `portal_chrome.html` on `<dialog class="console-drawer"`, which W2-A's step 2 (`e5fa845`) had made
  `<dialog class="console-drawer overlay overlay--drawer"`: an `IndexError` on every tree since then, which no earlier
  W2-A run met (none included the file). The anchor reads the first class now; the assertion — the drawer keeps its
  `<img>`, no release in it — is unchanged and holds (`c0d6037`; a justified path, DL54-94 item 9).
- **Without a browser, one run on the final tree** (`9c8571d`, 17 min 40 s, the machine shared with two other lanes'
  runs): `tests/frontend/` `test_overlays.py`, `test_overlays_console_w2_a.py`, `test_layout.py`,
  `test_console_shell_w3_a.py`, `test_console_shell_stylesheets.py`, `test_css_bundle_is_current.py`,
  `test_frontend_bundle_is_current.py`, `test_design_docs.py`, `test_static_pipeline.py`, `test_static_assets.py`,
  `test_components_w1_c.py`, `test_chips_cards_w1_c.py`, `test_css_tokens_exist.py`, `test_dashboard_w3_b.py`,
  `test_design_preview.py`, `test_entrance_w2_b.py`, `test_icons.py`, `test_legacy_token_shim.py`,
  `test_loader_rules.py`, `test_loader_w1_d.py`, `test_v4_tokens.py`, `test_v5_tokens.py` (every test file that reads a
  sheet the pass touched); `tests/i18n/test_rtl_static.py`; `tests/test_check_ownership.py`,
  `tests/test_regen_design_inventory.py`, `tests/test_phase_console.py`; `apps/portal`, `apps/documents`,
  `apps/academy/tests/test_views.py`; `tests/security` — **1 892 passed, 1 failed (the loader test above), 1 skipped,
  1 xfailed**, 67 browser tests deselected (run below). The skip is the security commit's own design:
  `test_the_depositants_private_identifiers_are_checked` runs only where `ILE_CONFIDENTIAL_SENTINELS` names the private
  table, which this worktree's `.env` does not (as on CI; the table was not touched). The xfail is the legacy token
  shim's debt, as before.
- **After this pass's fixes** (the components' headers, the guard, the loader anchor, DL54-94): `test_overlays.py`,
  `test_overlays_console_w2_a.py`, `test_loader_rules.py`, `test_design_docs.py`, `test_design_preview.py` —
  **397 passed**.
- **In the browser, one batch at a time, the lane server stopped, on the final tree** (`budget-final/run_tests.sh`):
  `test_overlays_console_browser_w2_a.py` — **14 passed**; `test_overlays_browser_w2_a.py` +
  `tests/i18n/test_rtl_browser_overlays.py` — **30 passed** (the board through the page-only sheet, the grip, Back and the
  native backdrop through the on-demand chunk, the Arabic document); W3-A's `test_console_shell_browser_w3_a.py` +
  `test_console_phone_browser_w3_a.py` — **64 passed**; `apps/portal/tests/test_browser.py` +
  `tests/i18n/test_rtl_browser.py` + `test_browser_w2_c1.py` + `test_browser_w1_b.py` — **46 passed, 1 failed**:
  W2-C1's `test_the_photographs_follow_the_loading_policy`, at 1440 (re-run three times: failed, passed, passed);
  `test_dashboard_browser_w3_b.py` — **27 passed**. No run crashed.
- **That failure is design-v5's, not this branch's — measured, not assumed** (E4/`photos_vs_load.json`,
  `photos_ab.json`, `photos_who.json`; lane 8783, the public home at 1440, a fresh context per load): on the page's own
  clock the four letterhead photographs start before `loadEventStart` in 5 of 12 loads (by 0.3–0.6 ms), which is what
  the test's `before == []` catches. Interleaved A/B, the same home with design-v5's own `css/dist` and `js/dist` routed
  in: **9 of 14 loads early with design-v5's bundles, 6 of 14 with this branch's**. And what starts them is not
  `nav.js`'s warm-up: a trap on `HTMLImageElement.loading` shows each photograph's `startTime` 1.6–26.3 ms *before*
  `nav.js` sets `loading="eager"`, in 10 of 10 loads — Chromium's lazy loader starts them by itself at that width.
  `nav.js` (W2-C1) is the same file as design-v5's; the home's markup and bundles were byte-identical when the cut
  pass's run of the same batch passed 47 of 47 at 22:29. Handed to W2-C1 (§7).
- `ruff check` clean on the three Python files the pass touched; `ruff format --check` clean on `test_overlays.py` and
  `test_rtl_browser_overlays.py`. `test_loader_rules.py` is reported unformatted by `ruff format` on design-v5 already
  (W1-D's file; CI runs `ruff check` only): not reformatted here, the two changed lines comply.

### 6 · For the merge

- `scripts/check_ownership.py w2-a design-v5`: **17 inside, 9 slice, 23 generated, 24 outside** — the fourteen of
  DL54-90, DL54-92 and DL54-93 and ten new, each named in DL54-94 item 9: `static/css/v5/_overlay-panels.css` and
  `apps/core/static/core/overlay-panels.css` (the system's page-only partial and its entry: the slice names
  `v5/overlays.css`), the dead rules' sheets `static/css/_legacy-tokens.css`, `static/css/base.css`,
  `static/css/layout.css`, `static/css/register.css`, `static/css/v5/base.css` (W1-A), `static/css/v5/field.css`
  (W1-C), `apps/portal/static/portal/portal.css` (W3-A), and `tests/frontend/test_loader_rules.py` (W1-D's, its anchor
  on the drawer's tag — §5). `static/css/components.css` counts as «slice»: its §12
  leftovers are W2-E's row of the deletion map, deleted here as dead (DL54-94 item 9 says so for the steward's diff
  check). Generated: `static/css/dist/core/overlay-panels.css`. The merge step writes them into the manifest.
- **Numbering**: W2-A's entries are DL54-88 … DL54-94 on top of today's design-v5; if another family's merge lands
  first, the steward moves them again.
- **The shared payload, for the gate**: before (design-v5 `1c03e3b` = `d40f209`) → after (this branch, rebuilt from
  clean): every page type at or under its ceiling — §2's table, reproduced by the steward's `weigh_pages.py`. The
  console page types keep 34 B of room; the public page types 388 / 379 / 388 B.
- The in-flight trees (`v54-w3-c`, `v54-w3-d`, `v54-w3-f1`, `v54-w3-f2`) still carry W3-A's console drawer in
  `portal_chrome.html`; their merges meet W2-A's version (step 2), as the steward already knows from the w2-a slice.

### 7 · Handed to, and left

- **Every family that adopts a dialog, an alert dialog, a bottom sheet, `components/drawer.html`, a native modal or the
  CSS face of `components/tooltip.html` links the page-only sheet** (CONTRACT §1; the components' headers say it):
  **W3-E** (the staff consequence dialogs — `components/dialog.html` with `kind="alert"`), **W3-F2** (the danger
  confirmation, if it becomes a dialog), **W3-C** (the preview drawer beside the list and its phone sheet, the filter
  sheet), **W2-C2** (its phone sheet, if it is the sheet family). None of the four in-flight trees draws one today (a
  grep of their templates). `test_overlays.py::test_the_panels_are_page_only_and_linked_by_the_pages_that_draw_them`
  fails for a template that draws one without the link.
- **W2-C1 — the letterhead's photographs start before `load` at 1440, and its test flakes on it** (§5, measured on
  design-v5's own bundles too). Plan §1.12 item 4 says «nothing before `load`; the four at idle after it, from 80rem».
  On the page's clock Chromium's lazy loader starts the four `loading="lazy"` photographs of the closed door panels by
  itself, before `nav.js`'s `warmAll` asks for them, and in some loads just before `load` —
  `test_browser_w2_c1.py::test_the_photographs_follow_the_loading_policy` then fails at 1440 (2 of its 4 runs
  here). W2-C1's to decide: what keeps the closed panels' photographs out of the lazy loader's reach until
  `warmAll` (`templates/partials/main_nav.html`, `static/js/src/nav.js`, `static/css/v5/chrome.css`), or the test's
  bound. Not changed here: not W2-A's slice, and not W2-A's doing.
- **W3-F1** — `layout.css`'s `.section--inverse` and the `.container--narrow` aliases are left for its own merge, which
  deletes them.
- **W3-C**, for its information only — «⋮»'s touch ring (`v4/workspace.css`, its rule) now applies on phones as written
  (§4); nothing to do.
- **The module's 4 KB** (plan §2.6): the core stays 6 466 B; what would cut it is no move but a rewrite of what the
  console uses (§3 item 4). Recorded here and in DL54-94 item 7 for the orchestrator.
- Unchanged by this pass and still owed: REVIEW m1 (the drawer's cold open on the INP edge) and m2 (O10, the WebKit and
  Firefox smoke) — Wave 4.
