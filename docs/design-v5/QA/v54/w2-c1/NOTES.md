# W2-C1 · «Il portico» — implementation notes

The family's implementer (label w2-c1-impl-1), under V5.5 delivery mode (implement → review once → fix → ship).
Append-only: each step adds a dated section. Heavy evidence (captures, measures, logs) under
`C:/tmp/ile_v5_council/evidence/v54/w2-c1/` (E/ below), outside every repository. Lane 9: dev server 8789 on
`ile_v5_l9`, `ILE_REFERENCE_DATE=2026-10-03`, `DB_CONN_MAX_AGE=0`, `--noreload`; pytest on `test_ile_v5_l9` /
`test_test_ile_v5_l9` (two concurrent runs, two databases); headless Chromium with the lane's own profile
(`C:/tmp/ile_v5_council/.profiles/w2-c1-impl-1/`); never 8780, never Chrome 9222 / 9223. Every browser series and
build went through `servers/lock_gate.py` first.

The direction is settled: the owner's «Fase 3 — menu aperto» (`C:/tmp/ile_v5_council/proof/home/phase3-menu.html`),
developed as plan §1.12 says, with N-A's mechanics only (intent timing, the keyboard model, one indicator) and «la
targa» of §1.11. No variant was built and none is proposed.

---

## Step 1 — the bar and the panels (5 October, interrupted; resumed and finished 8 October 2026)

### Where the resumption started

The branch `v54-w2-c1` (from `v54-w1-a` at `304c587`) held 25 uncommitted files from the interrupted start of 5
October: `apps/cms/templatetags/cms_nav.py` (`_portico()`), the four chrome templates, `static/css/v5/chrome.css`
(936 lines), `static/js/src/nav.js`, `shell.js` importing it, `initNavigation` removed from `main.js`, the eight
door photographs with their `PROVENANCE.json`, and the deletions of `v2/shell.css`, `components.css` §5–§7 / §25
and the chrome of `v4/shell.css`. No notes, no commit. Everything was read, built, rendered on the lane and judged
right; nothing was discarded. `design-v5` (the clock fix, `e16e811`) was merged first (`6ed38b3`, no conflict, no
overlap with the dirty files).

### What was done

1. **The letterhead bar** (`templates/partials/{utility_bar,header,main_nav}.html`, `chrome.css` §2–§4): the
   institutional bar 32 px night with the promoter and the four languages named in their own language (never
   «ع»), 24 px targets on a fine pointer, 44 on a coarse one; the letterhead 64 → 56 px once scrolled (glass only
   then, fine pointer, ≥ 80rem, no panel open); the six items — four doors as `button[aria-expanded][aria-controls]`,
   a hairline, Forum, Projet (D-U3); «l'architrave» as the one indicator (`translateX() scaleX()` on
   `--spring-snappy`, physical pixels from one code path, no travel on first placement, from the keyboard or under
   reduced motion); «la targa» flat in the end zone — ink hairline, radius 6, the gold key as ornament, the label
   from 90rem, the key alone below with a name tooltip, the account menu in the same seat when signed in, nothing
   drawn when the flags are off.
2. **One panel per door, from live content only** (`cms_nav._portico()`): the door card's locked gloss (its
   `lang` attribute kept: a prescribed French gloss on an Arabic page says `lang="fr"` and is drawn LTR in its run),
   the CMS children or — for Institutions and Universités, which have none — the door card's two live task links
   through `public_url` (gated like the pages), a second line under an entry only where a short live sentence exists
   (≤ 160 characters, whole, in the page's own language: an Arabic list never carries a French line), the
   anti-fraud page as the panel's foot, the audience glyph once on a 36 px night disc, the door's photograph in
   colour (4 : 5, 640 / 960 webp, the Image Art Director's derivatives, `static/img/portico/PROVENANCE.json`).
   «Projet» is a plain panel hung from the bar's inline end; «Actualités» lives inside it. No schema change.
3. **Geometry**: the panel hangs from `.site-header__inner` (N1), 8 | 4 with the photograph in the last four
   columns; the entries column starts at the first door's inline start (`--portico-lead`, measured by `nav.js`;
   N2: the first door's first entry is 21 px below its door, under its word); one height for the four door panels
   (`--portico-h`, measured once out of sight; LA-7); the hairline of the letterhead runs into the panel's top edge;
   paper, shadow L3, 12 px bottom corners (three radii on the screen at rest, DL54-14).
4. **Behaviour** (`static/js/src/nav.js`, ≤ 4 KB gzip: 9.1 KB minified in `chunk-BUUEPXNL.js`): hover intent
   120 / 80 / 250 ms on `(hover: hover) and (pointer: fine)` and `pointerType === "mouse"` only; a click pins a
   hover-opened panel; the scrim only for click, tap and keyboard, from the letterhead's foot (never over the
   institutional bar); the safe triangle for doors 2–4 (the apex is the pointer's previous sample, the base the open
   panel's top edge; a pointer heading into the panel holds the switch, re-examined every 160 ms); the keyboard
   model of NAVIGATION §4.8 (← → in the eye's direction, an open panel follows them; ↓ opens and enters; ↑ from the
   first entry returns to the door with the panel open; Home / End on the bar and in the panel, the open panel
   following; Enter toggles and keeps the focus on the door; Esc closes and returns the focus; focus leaving the
   navigation closes, 1.4.13); the 1024–1279 band (the four doors in the bar, panels without the photograph, «Menu»
   with Forum · Projet · languages); today's drawer below 80rem, `--nav-drawer-top` written on the header so that
   drawer and overlay inherit it (G-23 closed); `html.no-js .site-header { position: relative }` below 80rem (G-04
   closed); photographs: nothing before `load`, the four at idle after it from 80rem only, never with Save-Data,
   never on a phone (measured in cold contexts: 0 / 0 / 4 at 390 / 1024 / 1440).
5. **Motion** (plan §1.5): the panel is a transition (in: opacity + 8 px, 200 ms `--ease-enter`; out 120 ms;
   instant from the keyboard and on a door change; content swap 120 ms of opacity; the entries rise 4 px, 30 ms
   apart, on the first pointer open per page only; photographs cross-fade in 200 ms under `contain: paint`); under
   `prefers-reduced-motion` one 80 ms opacity (`--motion-reduced`) — today still flattened to 0.01 ms by the
   universal `!important` block of `components.css` §29, which W1-D deletes; the state is right the day that block
   goes. No keyframe: `menu-in*` and `mega-in` left with the legacy chrome.
6. **Deletions** (plan §2.3's map, W2-C1's rows): `static/css/v2/shell.css` (the file), `components.css` §5
   utility bar, §6 language switcher, §7 header and drawer, §25 footer (29 → 25 numbered sections),
   `v4/shell.css`'s chrome (21.6 → 2.3 KB: the account menu as the V4 Menu stays for W2-A / W2-C2, the notice for
   W1-C). `main.css`: `v2/shell.css` out, `v5/chrome.css` last. `dist/main.css` 42.8 KB gzip (238.6 → 234.0 KB
   raw), under the 45 KB ceiling.
7. **Tests**: `test_browser.py` (the keyboard test rewritten for the disclosure model; the panel opened by its
   door), `test_rtl_browser.py` (the desktop panel through its door; header slice), `test_cms_nav.py` (+ two tests
   on `_portico()`: every door's panel from live content; the language of glosses and second lines, fallback and DB
   rows), `test_layout.py` (the targa follows the flag; header slice), `test_design_docs.py` (my slice: the v5 tail
   of the cascade, the sticky-header trap read from `chrome.css`, the keyboard list, the hooks of §16 may live in
   `static/js/src/`, the navigation thresholds read from `nav.js` + `chrome.css` and quoted by §7.2 / §11 / A11Y
   §3), `docs/qa/design/capture.py` (the panel opened by its door). New per-family files:
   `tests/frontend/test_browser_w2_c1.py` (the keyboard model, hover intent and the pin, the safe triangle for doors
   2–4 with the travel in px, the photographs' loading policy, the no-script fallback + G-04, 2.4.11 under the sticky
   letterhead) and `tests/i18n/test_rtl_browser_nav.py` (N19: the architrave under the open door, the entries at the
   first door's inline start, the plain panel at the inline end, the arrows following the eye — in ar and fr).
8. **Documents** (my slice): DS 2026 §2 (the chrome's row; `v4/shell.css` as what is left; the runtime properties),
   §7.2 (the two thresholds 64 / 80rem, `89.999rem`), §10 `language_segmented.html`, §11 intro / §11.1 «Il
   portico» / §11.2 drawer (G-02's figures on the V5 chrome, G-23 and G-04 closed) / §11.3 the language control and
   the targa / §11.5, §12 (two sentences on the keyframes that left), §16 (`nav.js`), §21 (G-04, G-23 closed);
   A11Y §3 (the portico and drawer rows), §4.3–§4.5, §7, §9.1, §10.2, §11 (the test table), §13 (G-04, G-23 closed;
   G-12 re-pointed), the WCAG rows 1.4.3, 1.4.13, 2.4.3, 2.4.11. `scripts/regen_design_inventory.py --write` then
   recomputed the figures (§2 weights and numbering, §16 size, the A11Y summary: 31 conformi, 8 parziali).

### Measures (E/build2/, `measure.json`; lane 9, Chromium headless, DPR 1)

| What | fr | ar |
|---|---|---|
| Letterhead / institutional bar at 1440 | 65 px (64 + hairline) over 32 px | same |
| Panel («Personnes», hover) | x 100 → 1340 (the content box), 570 px high; all four doors 570 px | 488 px (shorter texts) |
| First entry vs its door (N2) | 21 px below the door's foot, text under the door's word | same |
| Travel door → first entry (doors 2 / 3 / 4) | 164 / 282 / 444 px — the panel held along each path | 317 / 215 / 85 px |
| Architrave under the open door | on, 2 px, laguna; `Highlight` in forced colours | on, placed from the right |
| Scrim | hover: none; click / keyboard: from y = 97, never over the bar | same |
| Photographs before `load` / after idle (cold) | 0 / 4 at 1440; 0 / 0 at 1024; 0 / 0 at 390 | — |
| 1024 band | four doors, panel without photograph (x 40 → 984), «Menu» with Forum · Projet | same |
| Drawer 390 / 1024 | from y = 57 / 97 (the header's real foot), 787 / 671 px high, no overflow | same |
| 320 | «Menu» 46 × 44 px, right edge = content edge (300 px), name kept; no overflow | «القائمة», same |
| Scrolled | 57 px bar, lock-up 32 px, glass | same |
| Requests before `load` on the home | 2 sheets, 8 scripts (see «left») | same |
| Console | 0 errors; the Vazirmatn preload warning on /ar/ is W1-A's | |

Captures looked at (E/build2/): the closed bar, every door open, the pinned state, the keyboard state, the
scrolled bar, 1024 closed / door / drawer, 390 closed / drawer / section, 320, 1920 door 3, the FAQ (current
door), reduced motion, forced colours — fr and ar.

### Decisions met during the build (no owner question)

- **Home / End with a panel open** move the open panel like the arrows (the first start left it open under
  another item).
- **The plain panel's gloss keeps its language**: the fallback structure's description is a gettext source; the
  panel asks the catalogues (`page_services.ui`) instead of re-reading an already translated string as French,
  which drew the Arabic «Projet» gloss LTR.
- **The panel's height** is the content's honest height (Personnes: six entries, four with a second line); the
  sparse doors (two entries) keep the one height with the gloss, the photograph and paper — the void is breathing
  room, not a defect; no row was compacted below 48 px and no line was clamped.
- **`v4/shell.css` is not deleted whole**: the account menu's V4 Menu (W2-A's popover replaces it) and the notice
  (W1-C) stay in a 2.3 KB file with the family that deletes each block named in its header.

### Ownership

`scripts/check_ownership.py w2-c1 v54-w1-a --working-tree`: every path of mine is inside the slice or a declared
slice of a shared file (`main.js` initNavigation, `base.html` chrome block, `test_design_docs.py`, `test_layout.py`,
`test_rtl_browser.py`), except the eight photographs `static/img/portico/*.webp` and their `PROVENANCE.json`, which
no family owns yet — the merge step writes them into the manifest (plan §2.2). The check also lists the clock fix's
files (`tests/conftest.py`, `tests/i18n/test_ui_translations.py`, `tests/security/test_object_permissions.py`),
which came with the design-v5 merge, and W1-A's files when run from `v54/base`: neither is this family's change.

### What is left (for the reviewer and the steward)

- `docs/qa/design/capture-report.json` (steward-only) must be regenerated by `capture.py` at the merge: the G-02
  figures of §11.2 / A11Y §13 are the V5 chrome's (787 / 787 px at 390 × 844, 671 / 671 px at 1024 × 768) and G-23 /
  G-04 are closed; `test_capture_report_is_current_and_backs_the_documented_figures` compares them with the JSON
  and is red on this branch until the regeneration.
- **Requests before `load`** on the home: 8 scripts (6 before). `scripts/build_frontend.mjs` takes every top-level
  file of `static/js/src/` as an entry, so `nav.js` — a module, not an entry — is split into its own chunk plus a
  206-byte `__esm` wrapper chunk. Not in this family's slice; the fix is an explicit entry list (or modules in a
  subfolder) in the build script, W4-B / the steward. Everything is one request fewer per page once done.
- The reduced-motion state of the panel reads 0.01 ms until W1-D deletes `components.css` §29's universal block;
  the V5 rule (80 ms opacity) is in `chrome.css` §9 already.
- W2-C2: the phone sheet on the overlay system, the signed-in targa's account popover, the panel's switch from the
  local adapter to `overlay.js` (W2-A's contract was not published when this step ran: `nav.js` keeps its own
  scrim, dismissal and focus return, as plan §1.12 item 6 allows).
- The «richer than Fase 3» sheet (N18: the comp beside the build, the same door open, at 1440 and 1920) is the
  reviewer's; the captures to compare are in E/build2/.
- B1 item 1 (the panel descriptions as copy) stays the owner's; until then the second lines are the live sentences
  listed in `cms_nav._SECOND_LINES` (each the page's own text).

### Tests run on lane 9 (8 October 2026)

- **Browser** (`-m browser`, Chromium headless, `test_ile_v5_l9`): `tests/frontend/test_browser.py`,
  `tests/frontend/test_browser_w2_c1.py`, `tests/frontend/test_header_fits_the_narrowest_viewport.py`,
  `tests/i18n/test_rtl_browser.py`, `tests/i18n/test_rtl_browser_nav.py` — **45 passed** (the no-script test first
  failed on its own timing: it looked 100 ms after the pointer left, inside the panel's 120 ms `display` transition;
  it now waits 400 ms). The safe triangle held for the three doors, travel 169 / 287 / 442 px at 1440.
- **Non-browser** (`test_test_ile_v5_l9`): `test_cms_nav`, `test_layout`, `test_design_docs`,
  `test_css_bundle_is_current`, `test_frontend_bundle_is_current`, `test_css_tokens_exist`, `test_static_assets`,
  `test_v5_tokens`, `test_legacy_token_shim`, `test_template_comments_do_not_leak`, `test_rtl_static`,
  `test_page_integrity`, `tests/compliance`, `apps/cms` — 834 collected: **833 passed, 1 xfailed, 1 failed** — W1-A's `tests/frontend/test_v5_tokens.py::test_v5_closes_the_cascade_and_reaches_the_browser_in_the_bundle`, which pinned `v5/base.css` as the last import while plan §2.3 puts `chrome.css` after the foundation; its one assertion now reads «the foundation's four sheets first, then only V5 sheets» (a justified extra in W1-A's file, declared here for the steward). `test_design_docs` + `test_v5_tokens` re-run after that: **566 passed**, the two known reds below.
- **Known red, not this family's to fix:**
  - `test_design_docs.py::test_capture_report_is_current_and_backs_the_documented_figures` — reads the steward-only
    `docs/qa/design/capture-report.json`, still the V4 chrome's figures (731 / 655 px, overlay over the header); the
    documents now carry the V5 chrome's (787 / 671 px, G-23 and G-04 closed). Green once the steward regenerates the
    report at the merge (plan §2.2 step 3).
  - `test_design_docs.py::test_cited_paths_exist` — A11Y §13's G-15 row cites `static/css/fonts.css`, which left with
    W1-A (the row is identical at this branch's point of departure, `304c587`): W1-A's / the steward's G-15 patch.
- Not run: the full suite (V5.5: integration checkpoints run it).

### Commits on `v54-w2-c1` (after the merge of design-v5, `6ed38b3`)

- `8199bf2` the four door photographs, in colour, with their provenance (`static/img/portico/`)
- `b1026a1` cms_nav gives every door its panel from live content (`_portico`) + its tests
- `a7ff2d9` «Il portico» — the letterhead bar, the four door panels, la targa and the drawer in the real templates; `nav.js` out of `main.js`; the legacy chrome deleted; dist rebuilt
- the tests of «Il portico» (retargets + the two per-family files + capture.py + the one assertion of `test_v5_tokens.py`)
- DS 2026 / A11Y rewritten for the portico, G-04 and G-23 closed, these notes

The trailer «Claude Opus 5.5» is the owner's standing convention for this programme (every commit of the branch
carries it); the model that did this step is Claude Fable 5.1.

### Lane state at hand-over

The dev server 8789 is left running on `ile_v5_l9` for the reviewer (stop: the process listening on 127.0.0.1:8789
only). Profiles under `C:/tmp/ile_v5_council/.profiles/w2-c1-impl-1/`; the smoke and patch scripts under
`C:/tmp/ile_v5_council/.work/w2-c1/w2-c1-impl-1/`; captures and `measure.json` in E/build2/ (before the two fixes)
and E/build3/ (after).

---

## Review fixes — the fix pass (label w2-c1-fix, 9 October 2026)

The family's implementer again, under V5.5 (implement → review once → fix → ship), on the two verdicts of 9 October:
`REVIEW.md` (SHIP_AFTER_FIXES: M1–M4, m1–m4) and `A11Y_PERF.md` (SHIP_AFTER_FIXES: 1–7). Branch `v54-w2-c1` from
`a78dad8`. Lane 9: the dev server 8789 restarted from this worktree at the fix (`cms_nav.py` changed; `--noreload`);
profiles under `C:/tmp/ile_v5_council/.profiles/w2-c1-fix/`; scratch under `.work/w2-c1/w2-c1-fix/` (`measure_bar.py`,
`checks.py`, `perf_layout.py`, `mint.py`); evidence under `E/fix/`. Every browser series and the build waited behind
`PERFORMANCE_BENCHMARK_LOCK` (W1-B's a11y/perf window held it 08:58 → 09:10). The signed-in pages used one session
minted on `ile_v5_l9` with `Client.force_login` (`mint.py`, the cookie in the profile folder only; revoked at the end).
The model that did this pass is Claude Fable 5.1; the commit trailer stays the programme's convention.

**Method.** Measured first, then fixed, then measured again: `E/fix/measures-before.json` / `-before-signed.json`
hold the letterhead's boxes in fr · it · en · ar at 1024 · 1280 · 1366 · 1440 · 1512 · 1600 · 1920 (and 320 · 340 ·
360 · 390), signed out and in, plus the text-spacing state; `measures-after*.json`, `RESULTS-checks-after.json` and
`RESULTS-layout-cost-after.json` the same after the fixes.

### What the before-measure said (the arithmetic the review asked for)

| Band (column) | Row needed, signed out — fr · it · en · ar | Signed in (seat 136 / 141) |
|---|---|---|
| 80–90rem (1096 px) | 1178.6 · 1152.1 · 1177.5 · 1064.1 → fr + 82.6, it + 56.1, en + 81.5 | fr + 186.7, ar + 77 |
| 90–100rem (1240 px), plate labelled 140 | 1320.4 · 1286.9 · 1314.6 · 1194.5 → fr + 80.5, it + 46.9, en + 74.6 | fr + 76.7, ar 0 |
| ≥ 100rem (1360 px) | all fit (fr 39.5 px of slack) | all fit |

So at 90–100rem the French row leaves 59 px — the labelled plate (140) can never fit there, only the key (32); at
80–90rem the overflow is 83 px before any end zone; and the phone row carried a latent defect nobody had measured: at
369–383 px the name (227.5) + 24 + «Menu» with its word (92) = 343.5 px exceeded the column (329–343).

### The fixes

1. **M1 — the letterhead holds its column** (`chrome.css` §3, §4, §6; the review's option (a), kept at 80rem as plan
   §1.12 item 7 says). *80–90rem*: the compact letterhead — the lock-up at 32/17 (the scrolled state's size), 16 px
   gaps, the doors without their chevrons as between 64 and 80rem (the reviewer's padding-8 variant left French
   1.4 px of slack; the chevrons, which the review itself named the one default-looking piece, buy 72). *Below
   100rem* the end zone is compact: the key alone, and — signed in — the person glyph alone on the same 32 px plate
   (the name visually hidden, so the summary keeps its accessible name; no chevron). *From 100rem* the plate's word
   and the seat's name (`max-inline-size: 6rem`, then an ellipsis — the room the French row leaves at 100rem). The
   label's threshold moves from 90rem to 100rem, the measured one (§1.11: «wherever it fits»). After: the end zone's
   inline-end edge is **on the column's edge** (0.0 px in all 24 signed-out and 20 signed-in cells) in the four languages at every width,
   signed out and in; the compact band needs fr 1029, en 1028, it 1002, ar 914 ≤ 1096; `test_the_letterhead_holds_its_column_at_every_desktop_width`
   (4 languages × 6 widths signed out + 3 signed in) pins it.
2. **M2 / A11Y_PERF 1 — WCAG 1.4.12**: `.main-nav__list { flex-wrap: wrap }` from 64rem — when a row cannot hold its
   items the list wraps, the letterhead grows by one row, the panels (hung from the inner's foot) follow, the
   architrave stays at the foot. After, under the standard sheet: scrollWidth = clientWidth everywhere, the end zone inside the column (0.0 past) — fr — 1024: 1024 = 1024, 2 rows, header 129; 1280: 1280 = 1280, 2 rows, header 129; 1440: 1440 = 1440, 2 rows, header 129 · it — 1024: 1024 = 1024, 2 rows, header 129; 1280: 1280 = 1280, 2 rows, header 129; 1440: 1440 = 1440, 2 rows, header 129 · en — 1024: 1024 = 1024, 2 rows, header 129; 1280: 1280 = 1280, 2 rows, header 129; 1440: 1440 = 1440, 2 rows, header 129 · ar — 1024: 1024 = 1024, 1 row, header 65; 1280: 1280 = 1280, 1 row, header 65; 1440: 1440 = 1440, 1 row, header 65 (the two «items past the viewport» the probe counts at 1024 are the hidden drawer's own Forum · Projet links, translated off-screen by design).
   `test_the_bar_wraps_under_text_spacing_and_never_clips` (fr + ar at 1024 / 1280 / 1440).
3. **M3 — the panels**: `.portico__space { align-self: start }` — «Voir l'espace» 16 px under the gloss,
   the lede one block; and `nav.js` marks `.portico--short` the door panels whose own content ends more than 24 px
   (LA-7) above the shared height, whose last entry closes with a hairline. After: fr 1440: doors door2, door3, door4 marked `.portico--short` (last entry `border-bottom 1px solid`), Personnes and Projet not; the one height 570 px fr / 508 px ar (the compact end zone moves the bar toward the end, so the lede column is wider and the Arabic lines wrap once more: 488 → 508), the plain Projet panel 432 / 350 px; at 1920 door 2 is 550 px and short; the Arabic
   panels and the plain Projet panel re-checked (captures `E/fix/after-{fr,ar}-1440-door1…5.png`, `-1920-door2`).
   Content stays live-only; the void below the lede is the grid's air by design (DL54-22). A side effect of the
   compact end zone, for the record: the bar sits at the row's end, so the key alone moves it 27 px further in French
   at 1440 (the lede 327.5 → 354.9 px) and 96 px in Arabic, whose items are 115 px shorter (373 → 469 px; the
   entries column 454 → 358 px): the Arabic lines wrap once more and the one height is 508 px instead of 488 —
   whole lines, nothing clipped, the entries still under the first door's word (N2). At 1600 nothing moves.
4. **M4 — the brand name on phones** (`chrome.css` §1, §3, §7): the name hidden only at ≤ 20.5rem (328 px); below
   48rem the letterhead's gap is 12 px and «Menu» has 8 px of padding (84 px with its word, 44 without). The
   arithmetic: 227.5 + 12 + 44 = 283.5 ≤ the column from 329 px; 320 keeps the mark alone (280 px of content cannot
   hold 283.5 with the brand's 14 px words). After: 320: name hidden, «Menu» 44 / 44 px (fr / ar), button on the column's edge (0.0 past), no sideways scroll; 340: name shown, «Menu» 44 / 44 px (fr / ar), button on the column's edge (0.0 past), no sideways scroll; 360: name shown, «Menu» 44 / 44 px (fr / ar), button on the column's edge (0.0 past), no sideways scroll; 390: name shown, «Menu» 84 / 87 px (fr / ar), button on the column's edge (0.0 past), no sideways scroll.
   `test_the_name_and_the_menu_button_share_the_phone_row` (320 · 328 · 329 · 340 · 360 · 368 · 369 · 375 · 390, fr + ar).
5. **m1** — `_SECOND_LINES` gains `("", "pages:project")`, `("", "pages:network")`, `("", "pages:contact")` with the
   pages' own standfirsts (`HERO_INTERIM["subtitle_fr"]` reused by the project page; `page_lead` of network.html and
   contact.html): fr 86 / 70 / 64 chars, ar 62 / 47 / 43; `test_portico_gives_every_door_its_panel_from_live_content`
   asserts `[True, False, True, True, True]` for the Projet panel. The Arabic back-office case of
   `test_portico_glosses_and_second_lines_carry_their_language` now expects the contact page's Arabic lead instead of
   `""`: the plan's precedence (description_<lang>, then the live line) — the French back-office line still never
   reaches the Arabic list.
6. **m2** — `lang` and `dir` on the gloss paragraph (`main_nav.html`), not on a span: the French block on the Arabic
   page is ragged-right in its column (the paragraph says lang=fr dir=ltr, computed direction ltr, text-align start; the Arabic Projet gloss stays rtl).
7. **m3** — the account glyph in ink (the `--identity-key` rule removed; forced colours keep `CanvasText`).
8. **m4** — DL54-20 … DL54-25 appended (the three build decisions + this pass's three: the fit, the phone row, the
   focus jump / the measure off the scrolled switch), with table rows. Numbered after design-v5's DL54-19 (`db55a67`);
   this branch's file ended at DL54-16, so the sequence jumps — the steward renumbers at the merge.
9. **A11Y_PERF 2 — the long task on the 64 ↔ 56 switch**: `layout()` split into `lead()` (one rect, every change)
   and `heights()` (the four panels out of sight — only when the inner's width, the bar or the fonts change, cached
   by width; `resize` re-measures only if the width moved). After, CPU ×4: fr: no long task on any of the eight wheel crossings (before 56–93 ms), the relayout alone 17–25 ms (before 54–77), the class toggle 20–28 (before 26–29); ar: none (before 89–125), the relayout 19–25 (before 74–107), the toggle 23–46 (before 25–31) — the acceptance «no long task > 50 ms on a wheel crossing at CPU ×4» holds in both languages (`perf_layout.py`, the a11y check's protocol: 1440 × 900, cold profile, 3.5 s of idle, four 420 px crossings down and up).
10. **A11Y_PERF 3 — the tip**: Esc hides it while the pointer or the focus stays (`initTarga`, `.tip-off` until
    `pointerleave` / `blur`); `border: 1px solid CanvasText` under forced colours. It stays below the plate: a 64 px
    bar with a 32 px plate leaves 16 px under it, not a 24 px tip, and beside the plate it would cover «Projet». After:
    fr 1280: hover → shown (y 87 → 111, the header's foot at 97), Esc → hidden while the pointer stays, pointer gone → hidden, hover again → shown; focus → shown, Esc → hidden, focus again → shown; ar the same; forced colours: border 1px solid rgb(0, 0, 0) (CanvasText).
11. **A11Y_PERF 4** — `html:has(:focus-visible) { scroll-behavior: auto; }` in `chrome.css` §3 (the navigation's
    item): a keyboard focus jumps; a pointer's anchor click keeps the smooth scroll (DL54-25). The instant jump
    exposed a hidden one: focusing a stop of the sticky letterhead while the page is scrolled (a door by script,
    Shift+Tab from the page into the end zone) scrolled the page to the top, because the page's scroll padding
    (80 px, for 2.4.11) also applied to targets that *are* the bar — the smooth scroll had hidden it, and
    `test_the_keyboard_model_of_the_portico`'s «↑ never scrolls» had passed on timing (it read `scrollY` before the
    smooth scroll had moved). Cure: `scroll-margin-block-start: -80px` on the letterhead's own stops (the lock-up,
    the six items, the end zone). Measured (`probe_scroll3.py`): 300 px stays 300 px after a door's focus and after
    Shift+Tab into the header, fr and ar; a page link below the fold still lands under the header's foot
    (359 / 371 vs 57). The panels' entries keep the padding.
12. **A11Y_PERF 6** — the drawer's language segments: `min-block-size: var(--hit-primary)` on the links under
    `(pointer: coarse)`, the track growing around its padding. After at 390 touch: links 85 × 44 px, the track 48 px, fr and ar.
13. **A11Y_PERF 7** — the door's chevron takes `ButtonText` under forced colours (scoped to the bar; the icon
    system's own rule stays W1-B's).

**Not done (outside the slice, listed for the steward):** A11Y_PERF 5, the explicit entry list in
`scripts/build_frontend.mjs` (the `nav.js` chunk, +1 request) — W4-B / the steward at the merge; the icon-system
forced-colours rule (W1-B); `docs/qa/design/capture-report.json` (steward, as before); `components.css` §29's
reduced-motion block (W1-D). Two pre-existing long lines in `test_browser_w2_c1.py` that `ruff format` would wrap
are left as they were (`ruff check` is clean).

### Measures after (E/fix/)

**The letterhead's fit (fr · it · en · ar; `measures-after.json`, `measures-after-signed.json`)**

| Width | Column | Row needed, signed out / signed in — fr | it | en | ar | Plate |
|---|---|---|---|---|---|---|
| 1280 | 1096 | 1029 / 1029 | 1002 / 1002 | 1028 / 1028 | 914 / 914 | key alone |
| 1366 | 1096 | 1029 / 1029 | 1002 / 1002 | 1028 / 1028 | 914 / 914 | key alone |
| 1440 | 1240 | 1213 / 1213 | 1186 / 1186 | 1212 / 1212 | 1098 / 1098 | key alone |
| 1512 | 1240 | 1213 / 1213 | 1186 / 1186 | 1212 / 1212 | 1098 / 1098 | key alone |
| 1600 | 1360 | 1320 / 1317 | 1287 / 1290 | 1315 / 1316 | 1194 / 1207 | yes |
| 1920 | 1360 | 1320 / 1317 | 1287 / 1290 | 1315 / 1316 | 1194 / 1207 | yes |

The end zone's overflow past the column is **0.0 px in every cell** (overflowPx of `measures-after*.json`), six items on one row, `scrollWidth == clientWidth`; the seat is 32 × 32 at 1280 and 1440 and carries the name at 1600 (136.1 px fr, 140.9 px ar).

**The panels (`RESULTS-checks-after.json`, captures `after-*`)**: «Voir l'espace» 16 px under the gloss in all ten panels; fr 1440: doors door2, door3, door4 marked `.portico--short` (last entry `border-bottom 1px solid`), Personnes and Projet not; the one height 570 px fr / 508 px ar (the compact end zone moves the bar toward the end, so the lede column is wider and the Arabic lines wrap once more: 488 → 508), the plain Projet panel 432 / 350 px; at 1920 door 2 is 550 px and short; the French gloss on the Arabic page: the paragraph says lang=fr dir=ltr, computed direction ltr, text-align start; the Arabic Projet gloss stays rtl.

**The tip**: fr 1280: hover → shown (y 87 → 111, the header's foot at 97), Esc → hidden while the pointer stays, pointer gone → hidden, hover again → shown; focus → shown, Esc → hidden, focus again → shown; ar the same; forced colours: border 1px solid rgb(0, 0, 0) (CanvasText).

**Forced colours**: the door's chevron computed rgb(0, 0, 0) = the door's colour rgb(0, 0, 0) (CanvasText); absent in the compact band (1280: display none).

**The drawer's languages on a coarse pointer (390)**: links 85 × 44 px, the track 48 px, fr and ar.

**The seat, signed in**: 32 × 32 at 1280 and 1440 (chevron none, the name visually hidden), 136.1 px at 1600 with the name; the glyph rgb(21, 34, 42) = the summary's ink.

**Scrolled at 1366**: header 57 px, mark 32 px (the band's compact lock-up is the scrolled one).

**The long task on the 64 ↔ 56 switch (`RESULTS-layout-cost-after.json`, CPU ×4)**: fr: no long task on any of the eight wheel crossings (before 56–93 ms), the relayout alone 17–25 ms (before 54–77), the class toggle 20–28 (before 26–29); ar: none (before 89–125), the relayout 19–25 (before 74–107), the toggle 23–46 (before 25–31) — the acceptance «no long task > 50 ms on a wheel crossing at CPU ×4» holds in both languages (`perf_layout.py`, the a11y check's protocol: 1440 × 900, cold profile, 3.5 s of idle, four 420 px crossings down and up).

**Console**: 0 errors, 0 page errors across the series (the probes' `errors` lists are empty).

### Tests run on lane 9 (9 October 2026, `test_ile_v5_l9`)

- **Non-browser** (`test_ile_v5_l9`): `test_cms_nav`, `test_design_docs`, `test_css_bundle_is_current`, `test_frontend_bundle_is_current`, `test_layout`, `test_template_comments_do_not_leak`, `test_css_tokens_exist`, `test_v5_tokens`, `test_static_assets`, `test_rtl_static` — **738 passed, 2 failed** in 6 min 20 s: the two known reds of step 1 (`test_cited_paths_exist`, A11Y's G-15 row citing `static/css/fonts.css`, W1-A's patch; `test_capture_report_is_current_and_backs_the_documented_figures`, the steward-only report). The first run had stopped on `test_portico_glosses_and_second_lines_carry_their_language` — the Arabic back-office expectation of item 5 — fixed and re-run. The design-docs slice re-run after the last DS edit: 4 passed.
- **Browser** (`-m browser`, Chromium headless): `test_browser.py`, `test_browser_w2_c1.py`, `test_header_fits_the_narrowest_viewport.py`, `test_rtl_browser.py`, `test_rtl_browser_nav.py` — **52 passed, 1 failed** in 15 min 13 s: `test_the_keyboard_model_of_the_portico`'s «↑ never scrolls» read `scrollY` 0 — the focus jump of item 11, made visible by the instant keyboard scroll. After the scroll-margin rule the targeted re-run — the keyboard model, 2.4.11, `test_mega_menu_is_keyboard_operable`, `test_rtl_browser_nav.py` (4), `test_header_fits_the_narrowest_viewport.py` (5) — **12 passed** in 2 min 8 s. The three new tests passed in the full run: the fit (4 languages × 6 widths signed out + 3 signed in), the 1.4.12 wrap (fr + ar × 3 widths), the phone row (9 widths × 2 languages).
- `ruff check` clean on the four Python files touched; `scripts/regen_design_inventory.py --write` after the document edits (the A11Y summary 31 → 32 conformi, 10 → 9 da confermare; §2's weight of `v5/chrome.css`).
- Not run: the full suite (V5.5: the integration checkpoints run it).

### Ownership

`scripts/check_ownership.py w2-c1 a78dad8 --working-tree` → PASS (7 inside, 3 slice, 5 generated). The slice
warnings, declared: `docs/ACCESSIBILITY.md` — the rows 1.4.12 and 1.4.13 of the WCAG table and the targa row of §9.1
lie outside «§3» (as step 1's edits did; the summary line was regenerated by `scripts/regen_design_inventory.py`);
`docs/design/DESIGN_SYSTEM_2026.md` — §7.2 and §11 only, plus §2's weight row regenerated by the same script;
`DECISION_LOG_V54.md` — append-only entries and their table rows. `static/img/portico/*` remain the manifest's to
assign (step 1).

### Commits of this pass

- `6045eec` the Projet panel's three live lines (m1) and the gloss's direction on its paragraph (m2); the stale nav chunk of the previous build out of dist
- `0ec3619` the letterhead holds its column at every width (M1, M2, M4), the lede block and the closing hairline (M3), the glyph in ink (m3), the one height off the scrolled switch (A11Y_PERF 2), the tip's Esc and forced border (3), the keyboard jump and the stops' scroll-margin (4), the drawer's 44 px segments (6), the chevron in forced colours (7); the three new tests; dist rebuilt (`main.css` 42 505 → 42 624 B gzip, the nav chunk 3 343 → 3 530 B gzip)
- `b1068d8` DS 2026 §7.2 / §11.1 / §11.3, the A11Y rows, DL54-20 … DL54-25
- this commit: these notes

The trailer «Claude Opus 5.5» is the programme's standing convention, as step 1 recorded; a second trailer names the model that did this pass (Claude Fable 5.1).

### Lane state at hand-over

8789 runs from this worktree at the pass's HEAD (stop: the process listening on 127.0.0.1:8789 only); the reviewer's
8889 still runs the pre-fix Python (`cms_nav.py` without the three Projet lines) — restart it before reading the
Projet panel there. The minted session was revoked (`mint.py revoke`: 1 session row deleted on `ile_v5_l9`, the secrets file removed); the profile folder holds no cookie.
