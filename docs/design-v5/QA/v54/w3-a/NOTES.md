# W3-A · the console shell «Tre livelli» — implementation notes

The area's implementer (label w3-a-impl-1), under V5.5 delivery mode (implement → review once → fix → ship).
Append-only: each step adds a dated section. Heavy evidence (captures, measures, logs) under
`C:/tmp/ile_v5_council/evidence/v54/w3-a/` (E/ below), outside every repository. Lane 6: dev server 8786 on
`ile_v5_l6` (`ILE_REFERENCE_DATE=2026-10-03`, `DB_CONN_MAX_AGE=0`, `--noreload`), pytest on `test_ile_v5_l6`, one
pytest and one browser at a time; headless Chromium with the lane's own profile
(`C:/tmp/ile_v5_council/.profiles/w3-a-impl-1/`); signed-in pages through sessions minted with
`Client.force_login` by a scratch script — no password used, typed or stored; never 8780, never Chrome 9222 / 9223.
Every browser series and build went through `servers/lock_gate.py` first. No run reported here ended on a crash.

The direction is settled — plan §1.18 D06, P-A «Tre livelli»; the gate-0 comp
`C:/tmp/ile_v5_council/proof/shell-dashboard/`. No variant was built and none is proposed. The decisions met during
the build are DL54-39 … DL54-46.

---

## Step 1 — the rail and the frame on desktop (9 October 2026)

Branch `v54-w3-a` from design-v5 `13ce8c4` (W1-D's tag `v54/w1-d` is in the base: the loader's release hook on the
rail's mark is kept as it landed — `{% entrance_release as lume_release %}`, the two seats, the `_loader-light.css`
import first in `console.css`; `test_loader_w1_d.py` and `test_reduced_motion_w1_d.py` pass unchanged).

### What was done

1. **One builder for every rail** (`apps/portal/services.py`: `shell_navigation(user, space, active)`,
   `shell_space`, `_bottom_keys`; DL54-39). Two spaces — «Espace réservé», «Espace entreprise» — decided by the
   route; every producer asks the builder (the portal's views, `academy`, `helpdesk`, `selection`, `companies`). A
   role's registers come first under «Mon rôle» (the dispatch desk of an operator or an administrator joined
   them); the account's other space is drawn at the rail's head; four entries at most reach the bottom bar.
   «Communications d’identité» is a page of «Échanges» for the account somebody has asked (DL54-44).
2. **The rail in three levels** (`templates/partials/portal_chrome.html`, `templates/portal/partials/rail_nav.html`,
   `apps/portal/static/portal/v5/_shell.css` §2): the space as the line under the name (DL54-40); the section as a
   word on the text axis, or a rule where the word would repeat; the page as glyph + word on ONE text axis (64 px)
   and ONE glyph column (32 px) that does not move when the rail folds. «Il lume» — the current page's glyph on a
   lit paper disc — once per rail copy, no edge bar (DL54-43).
3. **The foot, pinned** (DL54-42): the account (the audience's glyph, the name, who it is → the profile), sign-out,
   the rail's control, the language by its own name (the four open above the control), «Site public». One row in
   the four languages; under the user's own text spacing the row wraps rather than overlap.
4. **Compact and open, the choice kept** (`static/js/rail-pref.js`, `static/js/src/console.js`; DL54-41): open from
   80rem, compact (64 px, glyphs alone) below; `ile.rail` in `localStorage`, written on `<body>` before the first
   frame; without script the rail is open and its control is not offered. One density step: rows of 40 px under
   760 px of height with a fine pointer. The word of a lone glyph stands beyond the rail's edge (DL54-43).
5. **The page frame** (`templates/portal/base_portal.html`, `_shell.css` §3–§4; DL54-45): the context bar is the
   level of the page (the breadcrumb); one start edge, a column of 1320 px, 32 / 32 px of rhythm; one page header by
   the frame's own rules whatever markup a family still carries; a console button on the control's corner; the
   footer as one line; two native skip links (the content; the rail from 64rem, «Menu» below).
6. **`console.css` is the console's import list** (`_loader-light.css`, then `v5/_shell.css`): each family adds the
   import of its own partial. The partial is at the manifest's path, `apps/portal/static/portal/v5/_shell.css`
   (plan §2.3) — the step's brief names `static/css/v5/_shell.css`, which no entry of the console could import
   without putting console CSS in a public directory.
7. **Legacy out** (DL54-46): the four blocks of `portal.css` that the shell supersedes.

Below 64rem the phone chrome is V4's, carried into `_shell.css` §5 on V5 tokens (the top bar, the bottom bar, the
drawer with the whole rail): it is **step 2**. Two things of it were done now because they were defects: the second
skip link («Menu», three keys instead of 21 to 41) and the account trigger's width at 320 px.

### Measures (final code; lane 8786; E/)

| What | Result |
|---|---|
| The rail's keys by URL (29 page types, ten accounts; E/nav/) | before: 4–5 different key sets per account, 5 bottom entries for a company and the administrator, one label twice and two entries current on the help desk's pages · after: **2 key sets per account (its two spaces)**, ≤ 4 bottom entries, no label twice, never two current |
| A person's open rail at **1366 × 657** (E/sizes3/, the browser test) | whole in fr, it, en and ar: ten pages, three section words, head and foot in 657 px — nothing of the list (518 px) waits under a fold; rows 40 px; the foot's five controls in view, each at least 36 px high |
| The same rail at 1280 × 800 · 1920 × 1080 · compact at 1024 × 768 | whole, fr and ar (rows 44 px) |
| Longer rails (a role's registers: 11–13 entries; a company in «Espace réservé»: 10 + the way to its space) | the foot stays pinned and in view at every size; the list scrolls — by 11 px (a company, ar, 1280 × 800), 69 px (a professional, ar, 1366 × 657), 198 px (the administrator's 13 entries, 1366 × 657) — and the last page is reached; the current page is kept in view |
| 120 captures: ten page types of six accounts × fr / ar × 1920, 1366 × 657 (open, compact), 1280 (open, compact), 1024 (E/sizes3/) | 120 × 200; 0 horizontal overflow; the current page marked once per rail copy on each; 0 console or CSP messages |
| Smoke: 48 page rows (37 templates, eight accounts) × fr / ar × 1440 and 390 (E/s3-*/) | 45 × 200 + the three expected (403 terms required, 405 POST-only, 503 forum closed); 0 overflow; one h1 except `companies/profile_form.html` (two — the page's own, W3-E); 0 CSP messages |
| Animations at load, inside the shell | **0** (the pages' own draw patterns — `rail-draw`, `strip-fill` — are W3-B's and W3-D's) |
| Layout shift with a stored choice against the width | CLS < 0.01 (the browser test) |
| Corners per screen (1440, 48 rows) | 45 rows ≤ 3 (12 drew four and one five before the fold); left: the documents pages' search field (6 px, W3-C), the wizard on «Ma situation» (12 and 6, W3-F1) |
| Shadows in the shell at rest | none; the language menu takes the menus' level while open |
| The foot's last row | fr 24 px to spare · **it 15** · en 33 · ar 29 (before: 0 · −8 · 1 · 0) |
| WCAG 1.4.12, the four spacings (E/a11y/) | no control over another, none outside the rail, the foot in view; «Site public» goes under the row; the account's name is cut with an ellipsis and said whole by its word |
| WCAG 1.4.10 at 320 px (E/a11y/) | 0 horizontal overflow on three accounts (8 px before, with an e-mail address as the name); phone chrome 57 + 56 = 113 px |
| Forced colours · reduced motion | the row keeps an outline, the disc the system's highlight, the rail its edges · the rail has its new width in the same frame (0 ms) |
| CSS | `dist/portal/console.css` 13 807 → 22 461 B (2 936 → 4 235 gzip); `dist/portal/portal.css` 12 311 → 10 243 (2 687 → 2 263); the console page type 49 556 → **50 431 B gzip**, 571 over the Wave-1 ceiling of 49 860 (DL54-46) |
| JS | `dist/console.js` 4 279 → 5 111 B (1 676 → 1 938 gzip); `rail-pref.js` 847 → 1 064 B. `static/js/*.js` 17.3 → 17.5 KB: DS 2026 §16's figure is the steward's to regenerate (within the test's 10 %) |

### Tests

Targeted only (V5.5) — not the full suite. One pytest at a time on `test_ile_v5_l6`; no run ended on a crash.

- **Non-browser, one run** (31 min): `tests/test_phase_console.py tests/test_check_ownership.py apps/portal
  apps/companies apps/academy apps/helpdesk apps/selection apps/forum apps/documents apps/cases apps/orientation
  tests/security tests/frontend tests/i18n` — **2 879 passed**, 3 skipped, 2 xfailed, **6 failed**: the six cases of
  `test_state_chips_carry_a_register` on the preview's own templates (`templates/dev/designpreview/`), which fail on
  design-v5 already (W1-B's and W1-D's notes) and which this branch does not touch.
- **Browser** (Chromium): `tests/frontend/test_console_shell_browser_w3_a.py` **26 passed**; `apps/portal/tests/
  test_browser.py tests/frontend/test_browser_w1_b.py tests/frontend/test_loader_w1_d.py tests/frontend/
  test_reduced_motion_w1_d.py tests/i18n/test_rtl_browser.py tests/frontend/test_design_preview.py apps/ecosystem/
  tests/test_browser.py` **100 passed**.
- **New:** `tests/frontend/test_console_shell_w3_a.py` (27: the builder, every producer, the markup, the sheets, the
  identity panel) and `tests/frontend/test_console_shell_browser_w3_a.py` (26, see DS 2026 §11.6).
- **One regression of the build, found by the targeted run and fixed:** `apps/portal/tests/test_browser.py::
  test_secondary_pages_have_no_horizontal_overflow_at_390` (fr, ar) — a title that hugs its words was as wide as a
  100-character word; it is bounded by the frame.
- `ruff check` is clean on every Python file the branch touches. `ruff check .` reports six findings on the base,
  in `apps/accounts/apps.py` and `scripts/gen_loader_light.py` (W1-D's) — the steward's.
- `test_css_bundle_is_current` and `test_frontend_bundle_is_current` pass on the committed `dist/`.

### Paths outside the area's slice (`scripts/check_ownership.py w3-a 13ce8c4`: 7, each in DL54-46)

`apps/academy/views.py`, `apps/helpdesk/views.py`, `apps/selection/services.py`, `apps/companies/views.py` (no owner:
each module's rail producer asks the builder; `selection.services.has_disclosures`); `apps/core/icons.py` and
`tests/frontend/test_icons.py` (W1-B: two keys of the rail in the registry, and the stand-in account of its walk);
`apps/portal/static/portal/portal.css` (W3-B's «bridge part» is untouched: the four deleted blocks are the shell's
own legacy). The `dist/` files are generated — the steward rebuilds them from clean after the merge.

### What is left

**Step 2 — the phone chrome (this area).**
- The top bar and the bottom bar are V4's on V5 tokens: two-line and hyphenated labels in the bottom bar at
  320–390 px («Communica-tions», «Mes docu-ments»); W1-A's two patches for them in `static/css/v5/base.css` (lines
  28–47) leave when the bar is redrawn.
- A French title or name in the Arabic top bar is cut at its start (the ellipsis shows the end of the string).
- The company space's bottom bar for a project reader without a company holds one entry and «Menu» — the current
  page («Analyse territoriale») is not in it (`companies.services.navigation`'s `bottom` set).
- The drawer keeps V4's segmented language track; it moves to the overlay system with W2-A.
- The phone action bar (D06: «actions sit at the band's end or in the phone action bar»).

**Waiting for something else.**
- The **notification centre** (the gate's popover / sheet, `v5/_notifications.css`) and the console's **account
  popover**: the overlay system (W2-A) is not shipped. Nothing was started.
- **The labelled compact rail** (80 px, a 12/16 label under each glyph) and **«Changer d'espace»** as a label: new
  copy, B1 (DL54-41, DL54-44). Between 64rem and 80rem the default rail is glyphs alone.
- **«Aller à…»** (D06: staff only): there is no such control in the product yet; not built.
- The Forum permanent's own five rows on its pages (gate closed, 503 on the lane); its governance templates were
  not rendered on the lane.

**Seen on the way — other areas'.**
- W3-C: the documents pages draw four corners (the search field's 6 px).
- W3-F1: «Ma situation» draws five (the wizard's panel 12, its field 6).
- W3-E: `templates/companies/profile_form.html` renders two `h1`; on that page an account without a company has no
  entry to mark («Mon entreprise» appears once the company exists). Eyebrows above a title often repeat the level the
  breadcrumb already gives.
- The case page's height differs by 68 px between two loads of the same page (its content; not the shell).

**For the steward and the checks.**
- `docs/ACCESSIBILITY.md` does not name the console's rail yet — its keyboard model (§3) and the rows of 1.4.12 and
  1.4.13 are W2-C1's and W1-A's slices: the facts are in DS 2026 §11.6 and in the table above.
- The rail's control draws one glyph (`panel-left-close`) in both states; its state is said by `aria-expanded`. A
  twin for the compact state would be the icon family's.
- Without script, below 64rem, «Menu» opens nothing (a `<dialog>` needs script) and only the bottom bar's four entries
  are within reach — V4's behaviour, unchanged; to be settled with the phone redraw.

**Not measured.** LCP and long tasks on the compressed twin (8782): the shell adds no animation at load, no image and
no font; +262 B gzip of script and +875 B gzip of CSS for the page type. WebKit and Firefox were not run. axe was not
run (no copy on the machine, and no package may be added): the keyboard walk, the focus rings, forced colours,
reduced motion, the targets, 1.4.10, 1.4.12 and 1.4.13 were checked by the probes above.

### Commits (branch `v54-w3-a`)

- `98923cd` one builder for every rail of the console — `shell_navigation(user, space, active)`
- `1aad882` the console shell «Tre livelli» — the rail in three levels, its pinned foot, the page frame (desktop)
- `acb0e14` the rail holds whole at 1366 × 657 in Arabic too; a title hugs its words and never exceeds the frame
- `0ec37f8` the shell's tests — the builder, every producer, the markup, the sheets; and the browser half
- `6ce74f6` the foot holds in four languages; a lone glyph's word stands beyond the rail's edge; three corners a screen
- `e8de5a7` «Communications d’identité» keeps a place under one builder
- `19adfe3` `portal.css` loses the legacy rules the console shell supersedes
- `b09189c` tests — the identity panel, the tip's contract, the four languages, the audiences, 320 px
- `c4077b9` docs — DS 2026 §11.6, the console's rows of §2.1 and §16; DL54-39 … DL54-46
- then this file.

design-v5 is one commit ahead of the branch's base (`8246a7f`, the steward's W1-D note): no file in common.

---

## Step 2 — phones and tablets: the rail laid flat (9–10 October 2026)

The area's implementer, label w3-a-impl-2. Same lane (8786 on `ile_v5_l6`, pytest on `test_ile_v5_l6`), headless
Chromium with its own profile (`C:/tmp/ile_v5_council/.profiles/w3-a-impl-2/`), sessions minted with
`Client.force_login` — no password used, typed or stored — and revoked at the end; never 8780, never Chrome 9222 /
9223. One browser and one pytest at a time; every browser series and build after `servers/lock_gate.py`. No run
reported here ended on a crash. Scratch: `C:/tmp/ile_v5_council/.work/w3-a/w3-a-impl-2/`; evidence: `E/step2/`.
Phones and tablets are **emulated** (Chromium, `is_mobile` + touch): no real iOS or Android device was used.

The decisions met during the build are DL54-47 … DL54-52. No variant was built and none is proposed.

### What was done

1. **Below 64rem the rail is laid flat, in the same night** (`_shell.css` §5; `portal_chrome.html`; DL54-47).
   - **The top bar is the rail's head:** the mark on its paper tile (32 px drawn, 44 to the finger, the way to the
     space's first page; W1-D's release seat is unchanged), the level of the page as its title, the account — V4's
     menu until the overlay system brings the popover: its glyph alone on a phone, the name beside it from 48rem.
     48 px on a phone, 56 in the band. **No «≡»**: «Menu» stands once.
   - **The bottom bar is the rail's pages:** four entries at most and «Menu» at the reading end; «il lume» is the
     rail's lit paper disc — no bar at the edge, no tinted glyph. In the band from 48rem the glyph on its disc stands
     beside its word (the rail's row) in a bar of 56 px.
   - **The drawer holds the whole rail and the rail's own foot** — who the account is (→ the profile), sign-out as a
     row with its word, the language by its own name (the four open above it), «Site public» — instead of V4's
     segmented «IT FR EN ع» track. Today's mechanism: a native `<dialog>` opened with `showModal()`. The page behind
     the scrim does not scroll; a long name (an e-mail address) goes on a second line, never under an ellipsis.
2. **The bar's words are the live labels, whole** (DL54-49): none shortened, none new. A label stands on one line or
   on its two runs — the builder splits it (`_bar_lines`), the bar never breaks inside a word and never clips. A bar
   whose words do not hold on one line of a phone draws them on two runs at once (`_bar_stacks`); an entry's air
   gives way before a word does; **three entries where four do not hold** (`_bottom_yield`: below 22.5rem for every
   bar, below 30rem for a bar that carries a role's register).
3. **The company space's bar** is capped and completed by the shell: a project reader without a company has
   «Analyse territoriale» and «Communications» on the bar (one entry and «Menu» before, the current page missing).
4. **One «Menu», a link that script turns into a button** (DL54-50): three keys to reach it; Enter and Space; the
   focus on the page one is on; Esc puts the language's list away, then the drawer; the focus returns; a press on
   the scrim closes; a window widened past 64rem closes. The role of a button comes with the script that makes it
   one: **without script** it stays a link, the stylesheet shows the drawer it points at (`:target`) and the close
   control leads back to the page — V4's «Menu» opened nothing without script.
5. **A page's phone action bar** (O63, DL54-51) takes the four entries' place and «Menu» keeps the same end: the case
   file, 48 + 61 = 109 px. **The questionnaire's foot** on «Ma situation» holds five controls: below 64rem it is part
   of its page and its controls wrap (177 px of chrome → 114).
6. **Safe areas** on the logical sides (`viewport-fit=cover` is in `base.html`): the top bar, the bottom bar, the
   drawer, the page frame. **Short or very narrow viewports** (under 30rem of height, under 22.5rem of width): the
   top bar leaves with the page, the drawer's foot is not pinned. **Paper**: no rail, no bar, no drawer in print,
   and the room the page keeps for them given back at once.
7. **W1-A's two patches for V4's bar are retired** from `static/css/v5/base.css` (their own comments ask for it).

### Measures (final code; lane 8786; E/step2/)

| What | Before (V4's phone chrome on V5 tokens, same lane) | After |
|---|---|---|
| Chrome that stays on screen, 360–430 px | 113 px (57 + 56) | **114 px** in fr / it / en (48 + 66), **103 px** in ar (48 + 55) — 120 at most; a bar whose words hold on one line, 100 px |
| …on the case file · on «Ma situation» | 174 px · 177 px | **109 px** · **114 px** (103 in ar) |
| …in the band, 768 and 1023 px | not measured | 112 px (56 + 56); 117 on the case file |
| …at 320 px · on a phone on its side (844 × 390) | 113 px | 66 px at most (55 in ar; 72 for a professional, whose Arabic words take two runs) · 56 px: the top bar leaves with the page |
| …with a notch and a home indicator (47 and 34 px, emulated through CDP) | — | the bars grow by the device's insets and by nothing else: 114 + 81 px upright, 56 + 21 on its side |
| The bar's labels | 52 drawings (ten accounts, fr / ar, 390 and 320): 204 of 240 overflowed their box or were clipped by the bar; up to four lines; broken inside words («Communica-tions», «Désigna-tion des…») | 312 drawings (ten accounts × fr / it / en / ar × 320, 360, 375, 390, 412, 430): of 1 320 labels («Menu» among them) **898 on one line, 422 on two, none on three**, none outside its seat, none cut |
| Between the words of two entries | words touching («documents Communications») | **7.7 px at least**; 8.5 from 480 to 767 px (144 more drawings) |
| Entries on the bar | 1 to 4 (a reader without a company: 1) | 2 to 4; three at most at 320, and below 30rem with a role's register |
| A seat on the bar | 64 × 56 px at least, the labels clipped | **51 × 52 px at least**; the top bar's tile and account 44 × 44 (the tile was 32 × 32) |
| «Menu» | twice (the top bar's «≡», the bottom bar); nothing without script | **once**; three keys; the drawer without script too |
| The drawer's controls under a finger | — | 20 for a person (two in the head, ten pages, eight in the foot — the four languages among them): each at least 44 × 44 |
| Horizontal overflow | 9 px on one drawing (a person's dashboard at 320, fr) | 0 from the shell on 312 + 144 + 52 drawings. 11 drawings overflow by a page's own content: a person's dashboard whose pre-assessment panel holds a link that does not wrap (W3-B's — the same 9 px at 320 in fr; 6–33 px in it up to 375; 26–60 px in en at every width), the company dashboard's «needs» panel head at 320 in it (4 px) |
| Forced colours · reduced motion | — | the two bars take an edge of 1 px (116 px), the current entry an outline and the system's highlight · the drawer is in place at once (0 ms for 320) |
| Animations at load, inside the chrome | 0 | 0 |
| Console and CSP messages on every drawing above | — | 0 |
| CSS | `dist/portal/console.css` 22 461 B (4 235 gzip) | 29 207 B (5 167 gzip); the console page type **51 305 B gzip**, +874 for the step, 1 445 over the Wave-1 ceiling of 49 860 (DL54-52) |
| JS | `dist/console.js` 5 111 B (1 938 gzip) | 5 416 B (2 037 gzip) |

Looked at, not only measured: `E/step2/final-look/sheet-{fr,it,en,ar}.png` (six accounts at 360 and 390 in each
language), `final-states/sheet-{pages,band,safe}.png` and its captures (the drawer, the language's list, the
account's menu, the case file, the band at 768 / 1023, a phone on its side, the safe areas, forced colours, 320 px),
`final-focus/sheet-fr.png` (the rings), `dbg-nojs-drawer.png`, `dbg-drawer-long-name-320.png`; the state before:
`before/sheet-bars.png`. The folders `a1`–`a3`, `m1`–`m11`, `st1`–`st3`, `look1`–`look2`, `focus1` and `wide1` are the
build's iterations, kept for the record. The `final-*` series were taken on the code as committed, less the print
block's last correction (print only); `final-smoke/sheet-{1440,390}.png` — the dashboard, «Mes demandes» and the
company space, fr and ar — on the committed code itself.

**Below 320 px** (not a gate; probed at 240 px in en and 200 px in ar on a professional's bar, `dbg-bar-scroll-*.png`):
the row is wider than the screen and scrolls sideways inside the bar; the page itself does not overflow. A «Menu»
wholly out of view is brought in by the focus; one partly in view stays where it is until the row is scrolled
(Chromium's own rule for a focus).

### Tests

Targeted only (V5.5). One pytest at a time on `test_ile_v5_l6`; no run ended on a crash.

- **Non-browser, on the step's final tree** (20 min): `tests/frontend tests/test_phase_console.py tests/i18n
  apps/portal` — **1 816 passed**, 2 xfailed, **6 failed**: the six cases of `test_state_chips_carry_a_register` on
  the preview's own templates (`templates/dev/designpreview/`), which fail on design-v5 already (step 1; W1-B's and
  W1-D's notes) and which this branch does not touch. After the last corrections the ten files that read what
  changed — the shell's static tests, `test_design_docs.py`, the two bundle tests, the token and RTL guards,
  `tests/test_phase_console.py` — were run again, the last time on the committed tree: **735 passed**.
- **Non-browser, the wider run** (32 min; started after the step's last Python change, `b26f353`):
  `tests/test_phase_console.py tests/test_check_ownership.py apps/portal apps/companies apps/academy apps/helpdesk
  apps/selection apps/forum apps/documents apps/cases apps/orientation tests/security tests/frontend tests/i18n` —
  2 902 passed, 3 skipped, 2 xfailed, 8 failed: the same six, and two of `test_console_shell_w3_a.py` that read a
  template being edited while the run was on (both pass in the run above). `tests/security apps/companies
  tests/test_check_ownership.py` were run once more on the final tree: **263 passed** — the authorisation audit, the
  object permissions and the privilege-escalation tests are untouched and green.
- **Browser** (Chromium, on the final tree): `tests/frontend/test_console_phone_browser_w3_a.py` (29) and
  `tests/frontend/test_console_shell_browser_w3_a.py` (26) — **55 passed**; `apps/portal/tests/test_browser.py
  tests/frontend/test_browser_w1_b.py tests/frontend/test_loader_w1_d.py tests/frontend/test_reduced_motion_w1_d.py
  tests/i18n/test_rtl_browser.py tests/frontend/test_design_preview.py apps/ecosystem/tests/test_browser.py` —
  **402 passed** (the seven files whole: their non-browser tests ran with them).
- **New:** `tests/frontend/test_console_phone_browser_w3_a.py` (29, see DS 2026 §11.6) and 26 more in
  `tests/frontend/test_console_shell_w3_a.py` (53 with step 1's 27).
- **Found by the targeted runs and fixed:**
  - W1-B's `test_the_rail_the_bottom_bar_and_the_drawer_draw_the_registrys_symbols`: «Menu» is a link now — one
    filter in its file (DL54-52).
  - `test_documented_file_weights_are_roughly_true`: the weight of `v5/base.css` in DS 2026 was 20 % off with
    the two retired patches — `scripts/regen_design_inventory.py --write` (DL54-52).
  - On paper at a desk width the room kept for the rail glided away over 200 ms — the rail's one transition, seen
    under print emulation (67 px left at once, 0 after). Chromium's own print path starts no transition (the PDF's
    text starts at 32 px upright and on its side, before and after: `E/step2/print-*.pdf`), but nothing says every
    engine does: the print block silences the transition and stands after it.
  - One failure of the drawer test in three full runs of its file (none in five runs alone), on a loaded machine.
    The first run's log was cut and the failure's own message with it, so the cause is read from the test, not
    proven: it reads `aria-expanded` the moment the dialog loses `open`, and console.js folds it in the dialog's
    `close` event, a task later. Its waits now go through `_drawer_put_away` — a race of the test, not of the
    product; the file's run since is green.
- `ruff check` and `ruff format --check` are clean on the Python the step wrote (`apps/portal/services.py`, the three
  `*_w3_a.py` test files). `test_css_bundle_is_current` and `test_frontend_bundle_is_current` pass on the committed
  `dist/`; `scripts/regen_design_inventory.py` finds the inventory current.

### Paths outside the area's slice (step 2: two, each in DL54-52)

`static/css/v5/base.css` (W1-A: its two patches for V4's bar deleted, as their comments ask) and
`tests/frontend/test_browser_w1_b.py` (W1-B: one filter — «Menu» is a link now). In DS 2026: the console shell's prose
(§11.6, the row of `console.css` in §2.1), the sentences elsewhere that say where the language control and the
drawer's script live (§10, §11.3, §16), the sentence of §2's row 22 that named the retired patches, and two figures
rewritten by `scripts/regen_design_inventory.py --write` (the weight of `v5/base.css`, 20 % off after the deletion;
§16's total). The `dist/` files are generated — the steward rebuilds them from clean after the merge.
`scripts/check_ownership.py w3-a 13ce8c4`: 10 inside, 4 slice, 14 generated, 9 outside — step 1's seven (DL54-46)
and these two.

### What is left

**Waiting for copy (B1).**
- **Short labels for the bar** («Accueil · Dossier · Pièces · Messages»): the day they are signed every role's bar
  is one line and the rules of DL54-49 (two runs, three entries on a phone for a role's register) have nothing left
  to do. Until then a professional, an operator and an authorised actor have three entries and «Menu» below 30rem
  («Mes documents» is in the drawer).

**Waiting for the overlay system (W2-A).**
- The **drawer** moves onto it (focus trap, scrim and sheet are the system's); the **account popover** replaces V4's
  menu in the top bar (its links are 36 px high under a finger: W2-A's); the **notification centre** (the bell).
- Without script the drawer is not modal (no scrim, the page behind stays live): it is a way through, not the drawer.

**The weight.**
- The console page type's CSS stands 1 445 B gzip over the Wave-1 ceiling of 49 860 B gzip (571 after step 1). No
  sheet outside the shell's still styles the console's chrome, so the bust rule's first remedy has nothing left to
  delete; the rule's next step — the Performance Lead's measure of the first render on 8782, then the CD's one raise
  of at most 2 KB — was not taken by this step (DL54-52).

**Other families'.**
- W3-B: the person dashboard overflows horizontally on a phone when the pre-assessment panel is drawn — the panel
  head's link does not wrap: 9 px at 320 in French (before this step too), 6–33 px in Italian up to 375, 26–60 px in
  English from 320 to 430. With a page wider than the screen a phone widens its layout viewport, and the fixed bar
  with it.
- W3-E / W3-B: the company dashboard's «needs» panel head overflows by 4 px at 320 in Italian.
- W3-E (the case file): its phone action bar is the shell's contract now (`data-console-action`, or its own
  `data-file-action-bar`, read as it is): the day the hook is renamed `test_console_shell_w3_a.py` says so.
- W3-F1 (the questionnaire): its foot is part of the page below 64rem (DL54-51) — its ONE act («Continuer») is a
  candidate for the action bar when the wizard is redrawn; the stepper's eighth node wraps at 360.
- W2-A: `account-menu__link` 222 × 36 under a coarse pointer (already in W1-A's and W1-B's notes).
- W1-B: `tests/frontend/test_browser_w1_b.py` has two lines over 120 characters that `ruff format --check` reports on
  the base already; this step added one filter and left them.

**For the steward and the checks.**
- DL54-47 … DL54-52 may collide with another family's numbers on its own branch (W1-C's reach DL54-45): renumber at
  the merge, as for W1-D.
- `docs/ACCESSIBILITY.md` still does not name the console's phone chrome (W2-C1's and W1-A's slices): the facts are in
  DS 2026 §11.6 — 2.4.11 (scroll-padding under the two bars), 2.5.8 (44 px), 1.4.10 (the top bar leaves a narrow or
  short viewport), 1.3.4 (both orientations), 2.1.1 («Menu» with Enter and Space).
- The ownership manifest: the two paths above, with step 1's seven.

**Not measured.** Real devices (iOS Safari's toolbar, Android's gesture bar: the safe areas were emulated through
CDP); WebKit and Firefox; axe (no copy on the machine, and no package may be added) — the keyboard walk, the rings,
forced colours, reduced motion, the targets and the focus under the bars were checked by the probes and the browser
tests above; LCP and long tasks on the compressed twin (8782): the step adds no image, no font, no request and no
animation at load, +874 B gzip of CSS and +99 B gzip of script for the page type.

### Commits (branch `v54-w3-a`, after step 1's)

- `b26f353` the bottom bar's builder — the company space's bar capped and completed, the entry that leaves a row too
  short, a label's two runs
- `51d8a9b` the console shell below 64rem — «the rail laid flat»: the top bar, the bottom bar, the drawer
- `eee013e` tests — the bar's words for every role in four languages, «Menu» in three keys, the drawer, the band,
  Arabic, the states
- `581b2a5` the phone chrome's last facts — nothing of it on paper, the page still under an open drawer, a long name
  on two lines, a row that scrolls inside the bar
- `f738436` «Menu» says what it is — a link in the markup, a button by the script that makes it one
- `0722ce1` tests — paper, the page under an open drawer, a long name, the role given by script, the bar's scroll;
  W1-B's walk reads the bar's entries
- `37a5345` docs — DS 2026 §11.6 «Sotto 64rem: la rail distesa»; DL54-47 … DL54-52
- then this section.

design-v5 is still one commit ahead of the branch's base (`8246a7f`, the steward's W1-D note): no file in common.

---

## Review fixes (11 October 2026)

The area's implementer, label w3-a-fix: one fix pass after the senior review (`REVIEW.md`, SHIP_AFTER_FIXES) and
the accessibility and performance check (`A11Y_PERF.md`, SHIP_AFTER_FIXES). Same lane — the dev server on 8786 from
this worktree on `ile_v5_l6` (`ILE_REFERENCE_DATE=2026-10-03`, `DB_CONN_MAX_AGE=0`, `--noreload`), pytest on
`test_ile_v5_l6` —, headless Chromium with its own profile (`C:/tmp/ile_v5_council/.profiles/w3-a-fix/`), sessions
minted with `Client.force_login` (no password used, typed or stored) and revoked at the end; never 8780, 8782, 9222
or 9223. One browser and one pytest at a time, each browser series and build after `servers/lock_gate.py`; no run
ended on a crash. Scratch: `C:/tmp/ile_v5_council/.work/w3-a/w3-a-fix/`; evidence: `E/fix/` (`fix1` … `fix5`,
`smoke`, `smoke-final`). The decisions met are DL54-53. No variant was built and none is proposed.

### What each finding became

| Finding | What was done | Where |
|---|---|---|
| REVIEW **M1** (major) — a staff member's home is a person's dashboard | **Fixed.** «Espace réservé» starts where its rail does: for an account that holds a role's register the space's `url` — the rail's mark, the phone's tile, the drawer's mark, the way back from «Espace entreprise» — is the first entry of «Mon rôle»; for every other account, the dashboard, which stays one key away under «Parcours». One rule for the rail and its start (`_role_surfaces`), no query added | `apps/portal/services.py` (`shell_space`, `_person_space_start`, `_role_surfaces`) |
| REVIEW **m1** — a scrolling rail cut dead under the foot | **Fixed.** The `background-attachment: local` pair: a band of the night's sheet (24 px) fixed to the list's end, covered by the rail's own night that travels with the list's end — at the list's end, or when nothing scrolls, the band is gone. CSS only, no motion; the drawer's list has it too. The two images are tokens (`--rail-scroll-edge`, `--rail-scroll-cover`, tokens.css «console chrome»): an app sheet draws no gradient (`test_design_docs.py`, DL54-53 item 3) | `_shell.css` §2, `static/css/v5/tokens.css` |
| REVIEW **m2** — the French name above an Arabic title off the reading edge | **Fixed.** The frame's `inline-size: fit-content` rule extended to the ContextHeader's line above its title, bounded by the frame | `_shell.css` §4 |
| REVIEW **m3** — the identity carriers disagree on the empty dashboards | **Fixed, the shell's part.** A space's first page ends its trail on itself — «Espace réservé › Tableau de bord», «Espace entreprise › Tableau de bord» —, the space's name drawn as a word, never a link to the page one is on; the phone's top bar says the page. The h1 «ESPACE RÉSERVÉ» is W3-B's locked copy | `apps/portal/views.py`, `apps/companies/views.py` |
| REVIEW **m4** — the notification centre, the account popover, «Aller à…», the labelled compact rail | **Not this merge** (the review's own call): W2-A's overlay system; no «Aller à…» control in the product; B1's copy | — |
| REVIEW **m5** — the page type's weight | **Not code.** Below, with A11Y m3 | — |
| REVIEW **m6** — one glyph for both states of the rail's control; French two-line bar labels | **Handed over.** The twin is the icon family's (W1-B): `panel-left-open` is not in the sprite, and mirroring `panel-left-close` would draw a panel on the right — direction mirrors, meaning does not (`apps/core/icons.py` FLIP_RTL). The short bar labels are B1's | — |
| A11Y **M1** (major) — the footer's legal links 20 px tall | **Fixed.** `inline-flex`, 24 px at least; 44 × 44 under a coarse pointer | `_shell.css` §4, §6 |
| A11Y **m1** — the account menu's rows 36 px under a finger | **Fixed.** 44 px under a coarse pointer, in the phone's top bar (V4's menu, until W2-A's popover) | `_shell.css` §6 |
| A11Y **m2** — the skip links' ring on the paper where the rail is compact | **Fixed.** The ring is drawn inside the navy box (`outline-offset: calc(-2 * var(--focus-ring-width))`) | `_shell.css` §4 |
| A11Y **m3** — the dashboard page type over its §2.6 ceiling | **To record at the merge** — figures below and in DL54-53 | — |
| A11Y **m4** — the account's name cut under text spacing | **Fixed where it is drawn**: in the band (48–64rem) the name beside the glyph goes on a second line instead of an ellipsis. At 390 and 320 the probe's «clipped» name is its visually hidden box — below 48rem the glyph stands alone and the name is the trigger's word for a reader, with or without the spacing (the check's own `clip` and `spacing_clip` rows are identical) | `_shell.css` §5, the band |

### Measures (final code; lane 8786; E/fix/)

| What | Before | After |
|---|---|---|
| Where the mark leads (the rail's, the phone's tile, the drawer's) | the dashboard, for every account | qa-admin (a superuser) → «Processus assignés», demo-operateur → «Désignation des professionnels», demo-professionnel → «Demandes qui me sont confiées», demo-acteur-autorise → «Processus assignés»; a person, a person without a file, a company → the dashboard. On all 48 smoke loads the mark is the rail's first page (one exception, below: the company space of a project reader) |
| The mark pressed (1366 × 657), the tile pressed (390) | «ESPACE RÉSERVÉ», «Commencer le questionnaire» | the register: its entry lit, its title the h1, its act on the row («Enregistrer le mandat») |
| The dashboards' trail | «Accueil › Espace réservé» · «Accueil › Espace entreprise» | «Accueil › Espace réservé › Tableau de bord» · «… › Espace entreprise › Tableau de bord», in fr and ar; the phone's top bar «Tableau de bord» / «لوحة المتابعة»; every other page keeps the space as a link |
| The list's end, 3 px above it in the list's padding | the rail's night (11, 26, 51) | (22, 47, 78) while the list scrolls — the administrator at 1366 × 657 open and compact, fr and ar; a professional in ar —; (11, 26, 51) once the list is at its end, and on a list that does not scroll (a person at 1366 × 657 and 1440 × 900); no image under forced colours |
| The ContextHeader's name line in Arabic, off the title's edge | 130 px at 1366; mid-line at 360 | **0 px** at 1366 and 360; French unchanged on the start edge |
| The footer's legal links | 20 px tall («تنبيه» 26.5 × 20) | **24 px** with a fine pointer; **44 × 44 at least** under a coarse one. The footer: 69 → 73 px at 1440, 97 → 121 at 390, 125 → 173 at 320 in fr (its links on two rows), 97 → 121 at 320 in ar |
| The account menu's rows under a finger (390, 320; fr, ar) | 222 × 36 | **222 × 44** |
| The skip links' ring | 2 px beyond the box (1.68 : 1 over the paper where the rail is compact) | **inside the box** (−4 px), at 1100 and 1366 × 657 compact, 1440, 390, fr and ar |
| The band's account name under WCAG 1.4.12 (820 px; 1000 px) | cut by an ellipsis where it does not fit | «qa-admin@example.test» on two lines (42 px in the 44 px trigger), the bar still 56 px, nothing cut, fr and ar |
| Smoke: 12 page types (six accounts) × fr / ar × 1440 / 390, and the home | — | 50 × 200; 0 horizontal overflow, 0 console errors, 0 CSP messages, one h1 each; the phone chrome unchanged (114 / 103 / 109 on the case file / 100) |
| CSS, gzip −9 | the console page type 51 305 B | **51 458 B (+153**: `dist/portal/console.css` 5 167 → 5 292, `dist/main.css` +28); JS unchanged |

**The weight (REVIEW m5, A11Y m3).** On the family's base the page type stands 1 598 B over the Wave-1 ceiling of
49 860 B; on today's design-v5 the check's 50 479 B becomes about 50 632 (+772, 1.5 %). The fix adds no image, font,
request or animation. At the merge, the steward records a ceiling in the decision log (DL54-44's route, under V5.5's
performance rule, citing the check's A/B) or takes about 0.8 KB of legacy console rules out first; the Performance
Lead's first-render measure on 8782 belongs to the integration checkpoint.

### Tests

Targeted only (V5.5). One pytest at a time on `test_ile_v5_l6`; no run ended on a crash.

- **Non-browser** (7 min 24 s, on the final code): `tests/frontend/test_console_shell_w3_a.py`,
  `test_icons.py`, `test_css_bundle_is_current.py`, `test_frontend_bundle_is_current.py`, `test_design_docs.py`,
  `test_v5_tokens.py`, `test_css_tokens_exist.py`, `tests/test_phase_console.py`, `apps/portal`, `apps/companies` —
  **1 007 passed**. After the docs commit: `test_design_docs.py`, `test_v5_tokens.py`, `test_console_shell_w3_a.py`,
  `tests/test_check_ownership.py` — **670 passed**.
- **Browser** (Chromium, on the final code): `tests/frontend/test_console_shell_browser_w3_a.py` and
  `test_console_phone_browser_w3_a.py` — **64 passed** (9 new); `apps/portal/tests/test_browser.py`,
  `tests/frontend/test_browser_w1_b.py`, `tests/frontend/test_loader_w1_d.py`, `tests/i18n/test_rtl_browser.py`
  (`-m browser`) — **57 passed**.
- **New:** in `test_console_shell_w3_a.py` — where a space starts for eleven kinds of account (and no query once
  the roles are read), the three rendered marks, the dashboards' trails, the sheet's fixes; in
  `test_console_shell_browser_w3_a.py` — the band at the list's end and nowhere else (open and compact, fr and ar,
  measured on pixels), the mark's landing, the footer's and the menu's targets under a fine and a coarse pointer, the
  ring inside the skip link, the Arabic context line on the title's edge, the band's name under text spacing.
- **Found by the targeted run and fixed:** `test_design_docs.py::test_conforming_app_stylesheets_use_only_design_tokens`
  — the scroll edge's two `linear-gradient()` written in `_shell.css`: an app sheet draws no gradient. They became
  the two tokens (DL54-53 item 3); the shell's own test asserts again that `_shell.css` draws none.
- `ruff check` and `ruff format --check` clean on the five Python files the pass wrote; `npm run build` from this
  worktree (no install); `test_css_bundle_is_current` and `test_frontend_bundle_is_current` pass on the committed
  `dist/`.

### Paths outside the slice

`scripts/check_ownership.py w3-a 13ce8c4`: 12 inside, 4 slice, 14 generated, **11 outside** — step 1's seven
(DL54-46), step 2's two (DL54-52) and this pass's two (DL54-53): `apps/portal/views.py` (no owner: `_render` and the
dashboard's crumb) and `static/css/v5/tokens.css` (W1-A: two tokens in the «console chrome» group, beside
`--rail-bg`, so that the file does not conflict with W2-D's block appended at its end on design-v5). The merge step
writes them into the manifest.

### What is left, and whose

- **W2-A**: the notification centre, the console's account popover (its rows are 44 under a finger already), the
  drawer onto the overlay system. **B1**: the labelled 80 px compact rail, «Changer d'espace», the bar's short
  labels. **No control yet**: «Aller à…» for staff.
- **W1-B**: the rail control's twin glyph for the compact state (`panel-left-open`).
- **W3-B**: a home of staff's own (the shell sends them to their first register meanwhile) and the empty
  dashboards' h1 against its locked copy.
- **The accounts module** (L-09): the sign-in lands operators and administrators on the person dashboard —
  `accounts.adapters.get_login_redirect_url` has no row for them —, while the mark now takes them to the dispatch
  desk. The account menu's «Espace réservé» and every producer's breadcrumb root still lead to the dashboard.
- **W3-E / the companies module**: in «Espace entreprise» the mark — and the switch from «Espace réservé» — lead to
  the company dashboard even for a project reader without a company (the QA administrator), whose rail does not
  list it (`companies.services.navigation` hides the dashboard from a project reader).
- **Other modules' trails**: the selection workspace's last crumb says «Sélection autorisée» where its entry and its
  h1 say «Processus assignés»; the Academy's pages have no «Espace réservé» level («Accueil › Academy»).
- **The steward**: DL54-53 is renumbered at the merge; the weight's ceiling; the eleven paths in the manifest.

**Not measured.** Real devices, WebKit and Firefox; LCP and long tasks on the compressed twin (8782) — the pass adds
153 B gzip of CSS and nothing else that loads.

### Commits (branch `v54-w3-a`)

- `9c5e563` a space starts where its rail does — a role account's mark leads to its first register (review M1)
- `55ba453` a space's first page ends its trail on itself — «Espace réservé › Tableau de bord» (review m3)
- `7daf9d8` the sheet — the list's scroll edge, the context line in Arabic, the footer's and the menu's targets, the
  skip ring, the band's name
- `26baf74` tests — where a space starts, a first page's trail, the scroll edge, the footer's targets, the skip ring,
  Arabic's context line, the band's name
- `98c2aa0` docs — DS 2026 §11.6 «Dopo la revisione»; DL54-53
- then this section.

---

## Merge step — the steward's note on numbering (11 October 2026; label w3-a-merge)

W2-D's and W1-C's entries reached design-v5 first as DL54-39 … DL54-57, so at the family's merge its fifteen entries
became **DL54-58 … DL54-72** — the same order, add 19: DL54-39 → 58 (one builder), 40 → 59, 41 → 60, 42 → 61,
43 → 62, 44 → 63, 45 → 64 (the page frame), 46 → 65, 47 → 66 (the rail laid flat), 48 → 67, 49 → 68, 50 → 69,
51 → 70, 52 → 71 (step 2's paths and weight), 53 → 72 (the fix pass) — content unchanged but for their
cross-references and their two «Numbering» paragraphs. The steward's own record of the merge is **DL54-73**.

How to read the numbers written before the merge:
- **This file** and **`REVIEW.md`**: every DL54-39 … DL54-53 is the family's own — read it with 19 added — but
  two: «DL54-44's route» in «Review fixes» (*The weight*) is design-v5's DL54-44, the steward's record of the w2-d
  merge, and «W1-C's reach DL54-45» in step 2's «What is left» speaks of W1-C's numbers.
- **`A11Y_PERF.md`**: «DL54-45» (M1, the one-line footer) is the family's — DL54-64; the three «DL54-44» (the raw
  console entry that `collectstatic` refuses, «as DL54-44 did for the home», the Performance Lead's PASS) are
  design-v5's DL54-44, unchanged.
- The citations in code and in DS 2026 follow the new numbers: `_shell.css` (DL54-67), `portal_chrome.html` and
  the two test files (DL54-66 … DL54-71, DL54-71), DS 2026 §11.6 (DL54-60, DL54-66 … DL54-71, DL54-72).

What shipped, the tag and what is left: `SHIPPED.md`, beside this file (on design-v5).
