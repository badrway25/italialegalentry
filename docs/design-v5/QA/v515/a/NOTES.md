# V5.15 · lane A · W3 — Navbar Premium, Global Lume Loader, Motion language (label v515-a-build)

28 October 2026 · branch `v515-a` from design-v5 `ece1eeb` · worktree `C:/tmp/ile_wt/v515-a` · lane server 8783 (dev
settings, `ILE_DESIGN_PREVIEW=1`, `ILE_REFERENCE_DATE=2026-10-03`, database lane l3) · binding: the owner's V5.15
(`directives/V5_15_PREMIUM_VISUAL_REMEDIATION_CREATIVE_OVERRIDE.md`), DECISIONS §15 (lane A), §16 (carry-over), §10.0,
§12–§14; V5.12–V5.14. Decision log: **DL54-170** (the steward renumbers if needed).

## 0. Carry-over first (DECISIONS §16) — done, one root cause

The three browser regressions had ONE root: lane A's own W2 dead-rule cut in `static/css/base.css` removed `.list-reset`
**and the rule's body**, leaving `ul[role="list"], ol[role="list"]` glued to `hr`'s rule — every `role="list"` list drew
a hairline and 32 px above and below. That made the letterhead 129 px tall (the glossary's letter index stuck at 57 px
under a 122 px header), the console's bottom bar 101 px, and the language list in the institutional bar 89 px tall.
Restored (`list-style: none; padding-inline-start: 0; margin: 0`), commit `e27539f`. The pre-existing
`test_arabic_mirrors_the_chrome_and_never_the_mark` read `.console-bar__tile img`, which W1 replaced by the mark in
layers: the test now reads the layered mark (green plane first, `direction: ltr`, no transform on any layer) — the
never-mirrored guard kept. `test_console_phone_browser_w3_a.py` 29 passed; the glossary test 2 passed.
**Every lane benefits from this fix** (it affects every `role="list"` list on every page): please rebase on it.

## 1. What the owner sees, where (VISIBLE IN PREVIEW: Navbar Premium · Global Lume Loader · Motion System · 21st Components)

| Where | What |
|---|---|
| **Every page, public and platform — click any link** | **«Lume», the central loader.** The page dims under a night veil with a light blur; at the centre a lit paper doorway stands in the portico's three gold arches with the ILE mark at its foot; **the key turns once on its shaft, coming forward as it turns** (0 → 360°, 1 → 1.6 → 1); the light passes — the room behind the door lights, warm light spills over the floor, the sill draws in gold —; the stage opens towards the reader and the veil lifts off the new page. **≈ 700 ms in all on a fast local server**: the leaving page draws the first part, the arriving page continues the same clock (it is told the click's time before its first paint), so the owner sees it on 8780 without any throttling. Nothing waits for it: the browser loads the next page from the click. |
| A slow page (DevTools «Slow 4G») | The veil stays, key turned, the sill held at 85 % (never a fake end), and at 1 s **«Chargement…»** under the stage (said once; ar «جارٍ التحميل…»). **Esc** stops the pending navigation and the veil goes. Back / forward always work. |
| Keyboard navigation | No veil for a fast page (the keyboard never animates, R-07); after 400 ms the still. |
| Reduced motion (OS setting) | The branded still: the lit doorway, the key at rest, the sill at 85 %, by one 80 ms fade; the arrival holds it 240 ms. No rotation, no scale, no parallax. |
| First page of a visit | The whole clock once (the doorway, the turn, the light, the resolve). |
| **The letterhead, every desktop width** | **One row**: [ITALY LEGAL ENTRY™] [Personnes · Entreprises · Institutions · Universités & Formation │ Forum Vénétie–Maroc · Projet] [FR ▾ · Espace réservé]. No institutional bar above it any more. From 1440 px «Espace réservé» is the row's primary action, filled in night with the gold key. A soft plate glides under the pointer from item to item; the architrave marks the open / current item; once the page moves the bar turns to glass with a soft shadow. Measured one row, no overflow, in fr · it · en · ar at 1024, 1280, 1366, 1440, 1512, 1600 and 1920, signed out and in (`shots/row-*.png`; the browser guards); 1024 compresses (the mark alone, 14 px words), compact (lock-up 32/17, no chevrons) at every width above. |
| The language switch | «FR ▾» opens a popover with the four names in their own language, the current one checked (the overlay system's popover: Esc, a press outside, the arrows, the focus back). |
| **The mega panel** (hover / click a door, ≥ 1024) | A floating card under the bar (radius 16, hairline, deep shadow) that scales in; switching doors, the content slides in **from the side the pointer travelled**; the door's photograph opens with a mask and settles; on **Personnes** a glass «QUESTIONNAIRE D’ORIENTATION — Commencer l’orientation →» plate on the photograph (the highlighted destination). Projet stays a plain panel (V5.15 §2: not an image in every menu). |
| **Phone (< 1024)** | «Menu» opens a **full-height sheet** revealed as a light from the button's corner (mirrored in Arabic); its rows come in one after the other; the doors in 20 px on night discs; a door unfolds with its photograph (masked in), its gloss and entries; the foot on night with the access and the promoter. |
| Public page heads (every `.page-header` / `.ingresso`) | The eyebrow, the title, the lede and the aside **rise in sequence** at load (70 ms apart, 520 ms; after the veil lifts when one arrives). |
| Sections, as they scroll in | A chapter's heading and lead rise into place (`view()`); any block lane C marks `data-motion="rise"` rises its children one after the other. |
| Cards (`.card--link`, `[data-spotlight]`) | Lift 3 px with their shadow under the hand, the photograph settles 1.03, a soft gold light follows the pointer. |
| `[data-parallax]` figures, `[data-timeline]` / the case file's history | A 6 % drift against the scroll (from 48rem); the timeline's line draws as it is read. |
| **The platform** (dashboard, organisation dashboard) | The same veil on every rail click (`shots/cs-console.png`); the dashboard's blocks rise into place, main column first then the side; rows, tasks and the organisation's references lean 2 px under the hand. |

Captures (headless and HEADED Chromium 1234 on 8783): `C:/tmp/ile_v5_council/.work/v515-a/shots/` — `cast-sheet-fr.png`
(a real click, frames from the click: veil → turn → light → new page), `cs-ar.png` (Arabic phone: the sheet, the door
with its photograph, the veil, the arrival, the head rising), `cs-rm.png` (reduced motion: the still),
`cs-console.png` (the platform), `panel-*.png`, `sheet-*.png`, `row-*.png`, `veil-*.png`.

**Self-review at the V5.15 bar** (headed, 1440 and 390, fr and ar, reduced motion): letterhead 4/5 (one calm row, a
plate and glass that feel engineered; Arabic mirrored correctly); mega panel 4/5; phone sheet 4/5; veil 4.5/5 (a real
brand moment, not a spinner, and it is fast); motion language 4/5 on the pages that already carry the classes — it
grows with lane C's new headers and sections (the contracts below).

## 2. What changed (files)

* **Loader** — `templates/components/lume_veil.html` (new), included once by `templates/base.html` after the skip link;
  `static/css/v5/lume.css` (new, imported last by `static/css/main.css`); `static/js/src/lume/threshold.js` (`go()`,
  the veil drawn AFTER `depart()`'s own `quiet()`, Esc → `window.stop()`, the arrival's classes cleared at 900 ms);
  `static/js/src/head/head.js` → `static/js/head.js` (the «go» hand-off with the click's time, `--lume-t` clamped to
  400 ms, `lume-first` once per session through `ile.lume1`, the View Transition skipped under the veil on both sides;
  W1's «slow» arrival light removed). Removed: W1's band line, the band's word and turning key, the console bar's line
  and word, the tiles' and the letterhead mark's arrival light (`static/css/v5/motion.css`,
  `apps/portal/static/portal/v5/_motion.css`, `templates/partials/header.html`, `templates/partials/portal_chrome.html`).
  The View Transition stays for the navigations the veil does not take (the sign-in's door into the console, back /
  forward).
* **Navbar** — `templates/partials/header.html` (rewritten: one row, the language switch popover, the access, the primary
  action), `templates/base.html` (no institutional bar; the veil), `templates/partials/main_nav.html` (the plate, the
  highlighted destination, the field no longer hidden as a whole since it holds a link, the sheet's door photograph),
  `static/css/v5/chrome.css` (§2 the language switch replaces the institutional bar; §3 glass from 64rem + shadow; §4 all
  items from 64rem, the bands, the plate; §5 the floating panel, the direction, the photo's mask, the feature plate;
  §6 the end zone; §7 «Menu» below 64rem, the sheet's stagger / photograph / light reveal), `static/css/v5/motion.css`
  (the lock-sig compact band to 100rem), `static/js/src/nav.js` (`glide` — the plate; `data-from`; the sheet closes past
  64rem; «la targa» labelled from 90rem).
* **Motion language** — `static/css/v5/_reveal.css` (M15, M16, M19–M22; page-only `core/reveal.css`),
  `apps/portal/static/portal/v5/_motion.css` (the platform's rise and lean), `static/js/src/shell.js` (the spotlight's one
  passive listener).
* **Carry-over** — `static/css/base.css` (the list reset), `tests/frontend/test_console_phone_browser_w3_a.py`.
* Docs — `docs/design-v5/DECISION_LOG_V54.md` DL54-170; `docs/design-v5/COMPONENT_PROVENANCE.md` five V5.15 rows and the
  rejected-families note.

## 3. Decisions taken inside the brief (Creative Director, lane A)

* **One clock across two pages, not a fake wait.** The envelope is real time the browser is already spending (the click,
  the request, the first paint) plus a ≈ 400 ms resolve on the arriving page that never blocks input (the veil has
  `pointer-events: none`, the page under it is live). This is V5.15 §11's «very short controlled transition envelope».
* **A night veil and a paper doorway.** The verbatim mark keeps its colours only on paper (its navy steps disappear on
  night), so the doorway itself is the lit paper — the mark stands in a lit door in the dark: the brand's own image,
  no new mark variant (BRAND_ASSETS §1: «variante per fondo scuro solo se necessaria» — none was).
* **The key's turn is a 3D turn on its shaft** (the brand's rule: 0 → 360°, never held mirrored) made visible by a
  forward bump (1 → 1.6 → 1) at the centre — it reads as a turn at 390 px.
* **The View Transition steps aside** whenever the veil is drawn: two page changes drawn over each other read as a glitch.
* **No institutional bar.** V5.15 §1 forbids a stacked row; the promoter is named in the sheet's foot, the footer and the
  console foot.
* **The primary action is the access.** Measured: the content column stops at 1 360 px; the six French items (817 px with
  chevrons), the full lock-up (303), the language (55), the labelled access (140) and «Commencer l’orientation» (228)
  need 1 615 — two rows (the browser guard caught it at 1600). So the letterhead is compact at every width (1 195 px at
  1600), the access «Espace réservé» is the row's primary action (filled in night from 90rem), and the orientation
  questionnaire is the Personnes panel's highlighted destination (and the home's first action).
* **DECISIONS §2 rule 1 amended** for the page head (its sequence ≤ 520 ms after the first paint or after the veil) and a
  section's heading (at rest whenever already in view) — V5.15 §6 asks for staggered typography and section reveals.

## 4. Budgets (measured; Python `gzip -9`, as the tests read them)

| Asset | design-v5 `ece1eeb` | v515-a | Limit |
|---|---|---|---|
| `static/css/dist/main.css` | 31 279 B | **33 565 B** | **exception: 31 414 → 33 600** (the veil is global brand infrastructure on every page; paid in part by W1's band line, word and arrival light and the institutional bar, which left) |
| `static/js/head.js` (render-blocking) | 978 B | **1 196 B** | **exception: 1 000 → 1 250** (the veil's hand-off must run before the first paint) |
| `static/js/dist/shell.js` | 4 390 B | 4 683 B | ≤ 4 700 |
| `static/css/dist/core/reveal.css` (public pages) | 1 342 B | 1 894 B | page-only ≤ 6 KB |
| `static/css/dist/portal/console.css` | 8 134 B | 8 021 B | console only (falls: the bar's line left) |

No animation library, no new npm package, no React, no video. CLS: the veil and the plate are fixed / absolute
(no layout); the sheet's reveal is a clip-path; the head's rise is transform + opacity. LCP: the arriving page paints under
the veil from its first frame (the veil's ground is translucent; nothing in the page is held back).

## 5. Contracts for other lanes (no file of theirs changed)

* **Lane C** — `data-stagger` on any new page head (its children rise in sequence: eyebrow, title, lede, aside); the
  existing `.page-header` / `.ingresso` parts already do. `data-motion="rise"` on a block whose children should rise as
  it enters. `data-parallax` on a figure (its `img` drifts). `data-timeline` on a timeline whose `::before` is the line.
  `data-spotlight` on any card-like surface that is not `.card--link`. Mega-menu photographs: the four door frames
  (`static/img/portico/`) are lane C's; better frames per door are welcome — the panel takes any 4:5 crop. «Projet» has no
  icon in the phone's sheet (`cms_nav._DOOR_ICONS` is lane C's file): a glyph for it (e.g. `ile-arch`) would complete the
  sheet's column.
* **Lane B** — a `globe` / `languages` Lucide glyph in the sprite would let the language switch carry a globe beside «FR» (today the code
  alone, which reads well); not blocking.
* **Lane D** — the platform's motion keys on `.db-main`, `.db-side`, `.db-list__row`, `.db-task`, `.reg-row__link`,
  `.org-refs__link` (no template change needed). Keep those classes, or tell lane A when they change.
* **Steward** — DL54-170 may need renumbering; the base.css list-reset fix is in this branch's first commit.

## 6. New translatable strings

**None.** Every word drawn is an existing msgid: «Chargement…», «Choisir la langue», «Commencer l’orientation»,
«Questionnaire d’orientation», «Menu», «Fermer», «Espace réservé».

## 7. Tests (lane l3: `TEST_DATABASE_URL=…/test_ile_v5_l3`)

* **New**: `tests/frontend/test_lume_v515_a.py` — 12 tests, 14 cases (8 static / client: the veil included once after the skip
  link, nothing focusable, one status line on public and console pages, the shared clock, never a click taken, the
  still under reduced motion and html.rm, never on the hub / an error page / forced colours, the threshold's order and
  Esc, head.js's hand-off and its measured ceiling, the one-row letterhead with the language popover and the highlighted
  destination, main.css's measured exception; 4 browser tests, 6 cases: a pointer navigation draws the veil and Esc puts it away (fr
  1440, ar 390), the keyboard and reduced motion see the still, an arrival continues the clock and is gone after it, one
  row at 1024 / 1280 / 1440 in fr and ar and the sheet below 64rem).
* **Updated, stale by the change, no guard weakened** (each asserts the new rule as precisely as the old one):
  `test_lume_v512_a.py` (the band's line → its absence and the veil's sill; the band's word → the veil's one line; the
  hand-off «go» / «lang»; the console takes the veil; the View Transition steps aside under the veil), `test_loader_rules.py`
  (the veil in the L1 allow-list; `--motion-draw` left the loader's sheets), `test_motion_v512_a_w2.py` (main.css at the
  exception; `rise-in` admitted only on the page head and a section's heading), `test_layout.py`, `test_ui_translations.py`
  (no institutional bar; the language popover), `test_nav_sheet_w2_c2.py` (the plate's word from 90rem, the compact band,
  the tap highlight), `test_overlays_console_w2_a.py` (three popovers: the account ×2 and the language),
  `test_design_docs.py` («Menu» and the drawer below BAR), `test_browser_w2_c1.py` (the label from 90rem; one row
  1280–1920 holds), `test_browser_w2_c2.py` (no «Menu» from 64rem — the side sheet measured at 768; the end zone on the
  edge with the flag off; six items at 1024 with ≥ 24 px spare, fine and coarse, with a 17 px scrollbar, signed out and
  in; a door's one photograph at the phone's size, none while the sheet is closed — N8 amended by V5.15, DL54-170),
  `test_motion_browser_w4_b.py` (the fold measured once the dashboard's rise has settled), `test_console_phone_browser_w3_a.py`
  (carry-over: the layered tile).
* **Runs**:
  * non-browser, the 72 files that read the chrome, the loader, the motion, the docs and the bundles: **2 189 passed**
    on the first run with 38 failures, all fixed (rerun of every failing file: **908 + 804 + 716 passed**); left: **14
    failures pre-existing on design-v5** (`e580b41`, the same 14 on the same database: `test_cms_nav` portico panel,
    `test_nav_sheet_w2_c2` signed-in seat, `test_mobile_rtl_w4_a` the 500's semicolon, `test_service_pages_w3_f2` ×11 —
    the account frames, the profile's and the situation's personal fields, the 400/500 without the database);
  * browser (one Chromium, under the machine's lock): `test_lume_v515_a`, `test_lume_v512_a`, `test_motion_v512_a_w2`,
    `test_browser_w2_c1`, `test_browser_w2_c2`, `test_loader_w1_d`, `test_reduced_motion_w1_d`,
    `test_content_pages_browser_w3_f2`, `test_browser`, `test_rtl_browser`, `test_overlays_browser_w2_a`,
    `test_motion_browser_w4_b`, `test_console_phone_browser_w3_a`: **all pass** after the fixes (77 + 131 + 24 + 10 + 8
    + 2 passed across the runs) except **`test_rtl_browser::test_every_arabic_public_page_fits_the_viewport` ×2:
    54 Arabic routes answer 200, the test wants ≥ 55** — the three closed by lane C's gates (forum-virtuel, actualités,
    partenaires) answer 404; not this lane's (DECISIONS §14 asked the W2 steward to move those suites to the hidden state).
  * Found and fixed by the guards on the way: a two-row letterhead at 1600 with the orientation action in the row (§3),
    the Arabic face fetched on a Latin page by the language popover's codes (now in the Latin face).

## 8. Requests

See §5 (contracts for lanes B, C, D; the steward). Plus, for the **steward**: the base.css list-reset fix (`e27539f`)
repairs every `role="list"` list on every page — please merge lane A first, as the merge order says.

## Round 1 improvements (label v515-a-improve1, 29 October 2026)

Rebased on design-v5 `7f2a02d` first: DL54-169 is the v517-p3 merge's, so this lane's decision is **DL54-170** (the
log's row and section, these notes, DESIGN_SYSTEM_2026 and the test comments renumbered; commit `0651bf4`).
Reviewed in HEADED Chromium 1234 on 8783 (database `ile_v5`, the four doors), fr · it · en · ar, 768 → 1440, 390;
captures `C:/tmp/ile_v5_council/.work/v515-a/shots/i1-*` (probes `improve1.py`, `measure_row.py`, `console_pane.py`,
`lcp.py`, outside the repository).

| Review finding | What changed | Measured |
|---|---|---|
| **Word at the viewport's top** (major) | `--lume-w` on `:root` (the word is the veil's sibling); 24 px under the stage | word top 704 / stage bottom 680 at 1440; 633 / 609 at 390 (ar) |
| **Fast navigation: a frozen click, then a cut** (major) | the leaving page hands on what it PAINTED (`pagehide`: `go|click|shown|pane`); the arrival continues from it (≥ 100 ms, ≤ 440 ms; from the click's age when back within 150 ms); under the veil the View Transition is kept as a **140 ms dissolve of the root alone** (`html.lume-in::view-transition-old(root)`, no mark travels): the held old frame dissolves into the veiled page | a real click at 1440 fr: `pagereveal` with a VT, `--lume-t` 196 ms, the key visibly turning across ≈ 190 ms of frames; 390 ar: `--lume-t` 150, the whole turn on visible frames |
| **The key pulses at 390** (major) | stage `min(24rem, 80vw, 52vh)` (312 px at 390, was 257); the key lifts 1 → 1.45 and HOLDS while it turns (90 → 400 ms: 310 ms of turn), a specular light sweeps its face (masked to the key), its shadow swings with it, then it settles; the leaving page plays the same keyframes | `i1-turn-ar-390-strip.png`: edge-on at 200 ms, its back at 260–330, settled and lit at 420–520 |
| **Mega panel: one height, a white void** (major) | each door its own height, the card MORPHS between doors (`interpolate-size`, `--portico-from`); three zones: the lede (the door's name, gloss, «Voir l’espace»), the entries on two columns of hairline rows — a short door's two entries become two **tiles** (title, line, the way forward at the foot, a lift under the hand) — and **«la lunetta»**: the door's night plate (the portico's arches in gold, the door's glyph lit, its highlighted destination; the whole plate is the link: the questionnaire for Personnes, the door's space for the others) | Personnes 371 px, the three others 272 (were all ≈ 550); `i1-panel-fr-1440-d*.png`, `i1-panel-ar-1440-d*.png` |
| **Photographs repeat the home's tiles** (major) | the panel and the sheet draw a photograph only from a frame of the menu's own (`item.photo.menu_only`); none until lane C's frames exist (request below) | 0 portico frame fetched at any width |
| **Motion language: 0 hooks** (major) | keyed to the classes the pages draw: the rows of `.register`, `.registro` (not lane C's `.spazi`), `.home-trust__list`, `.forum-programme`, `.page-links` rise in sequence as the list enters (`view()`); the home's entrance rows and the pages' link rows lean 4 px with a plate and the pointer's light; the door plate `.porta` and any `.card--link` / `[data-spotlight]` take the light; lane C's `.bande-foto__frame` drifts (M22); lane C's photo.html already carries `data-reveal="mask"` / `data-grade` (M2, M3) | Projet, Contact, Réseau, Forum and the home now carry the rise and the light |
| **LCP on a first visit** (major) | `lume-first` plays the resolve alone (from 460 ms, ≤ 240 ms) and the head is never held (`--rise-wait: 0`); on an arrival the head waits at most `360 − t` ms | see «LCP» below |
| **The end zone changes form** (major) | the access is a filled night control at EVERY width (a 40 px night square with the gold key below 90rem, labelled from 90rem); language, access and «Menu» share one 40 px height (44 under a finger); the language is a 40 px square (its code) below 90rem | 768: 40 · 40 · 40; 1024–1366: 40 · 40; 1440: 40 · 40 |
| **The wordmark dropped at 1024–1279** (major) | root cause: the compact bands were written BEFORE the generic 64rem rule, which overrode their 14 px wordmark and 8 px items; now in cascade order. The wordmark returns from **70rem** (was 72); 64–70rem the mark alone, the items given its room | at 1024 the French row lacks 84 px for the full lock-up (measured, `measure_row.py`); one row everywhere in fr · it · en · ar, 768–1440 |
| **The sheet's raw search form** (major) | one field: the glyph inside at the start, a night icon submit inside at the end (named «Rechercher»), the label read and not drawn | `i1-sheet-strip.png` |
| Projet without a glyph | `ile-arch` (the sprite's own) in its slot | idem |
| The focus ring square (minor) | the plate's radius, 2 px outside a 32 px plate | `i1-panel-fr-1440-focus.png` |
| The feature plate grey at 1024 (minor) | the plate is solid night at every width (no glass over white) | `i1-panel-fr-1024-d0.png` |
| The console's veil heavy (minor) | between two console pages the veil covers the work pane only (the rail lit, a 15rem doorway, no blur, a lighter ground); entering a space keeps the full veil | `i1-console-pane-250.png`: `inset-inline-start` 248 px = the rail |
| The dead utility bar (minor) | `templates/partials/utility_bar.html` and its two `base.css` rules removed | |
| The spotlight as a background (minor) | the light is a `::before` layer; the lift's transition list keeps the card's own border transition | |
| The sheet's reveal too quick (minor) | the light 300 ms, the rows 40 ms apart from 90 ms, the search and the primary last | |
| Tests (minor) | the word under the stage and inside the viewport; the arrival's first frame `0 < ground < 1` at `--lume-t` 100 ms | |
| DL54-169 taken (minor) | renumbered DL54-170, with a round-1 paragraph | |

**Not changed, on purpose.** The blur (minor): not traced at 4× CPU this round; left at 8 px on the public veil (the
pane variant has none). The Arabic chrome's French glosses: locked copy without a reviewed translation — lane D (Q3).

### LCP (indicative: 8783, dev server, 390 × 844 mobile, 4× CPU, ≈ 1.6 Mbps / 150 ms RTT, 3 samples, median)

| Page | first visit (lume-first) | seen | review round 1 (one sample) |
|---|---|---|---|
| `/fr/faq/` | **2 048 ms** | 2 044 ms | 2 716 / 1 992 ms |
| `/fr/parcours/` | 1 944 ms | 1 848 ms | — |

The first visit no longer pays for the veil: under 2.5 s, within 4 ms of a seen page on the FAQ. (8782, the compressed
twin, serves another build and is the Performance Lead's: not switched by this lane.)

### Budgets (Python `gzip -9`)

| Asset | before round 1 | after | Limit |
|---|---|---|---|
| `static/css/dist/main.css` | 33 565 | **33 152** | ≤ 33 600 (the recorded exception; it fell) |
| `static/css/dist/core/portico.css` (new; `media="(min-width: 64rem)"`, public pages) | — | 2 663 B | page-only ≤ 6 KB (test: ≤ 3 000) |
| `static/js/head.js` | 1 196 | **1 244** | ≤ 1 250 |
| `static/js/dist/shell.js` | 4 683 | ≈ 4 570 | ≤ 4 700 (the panel's measuring code left) |
| `static/css/dist/core/reveal.css` | 1 894 | ≈ 2 190 | page-only ≤ 6 KB |

The desktop's mega panel left main.css: a phone never blocks its first paint on it (a stylesheet whose `media` does not
match is fetched at the lowest priority); a desktop fetches one more small sheet in parallel.

### Requests

* **Lane C** — four mega-menu-ONLY frames (4:5, 640 and 960 webp, licensed with provenance; one per door — persons,
  companies, institutions, universities — none that a page shows), and `_photo()` in `cms_nav.py` returning
  `"menu_only": True` with them. The panel then lays the frame under the plate's light (`_portico.css`) and the sheet
  shows it in the unfolded door; restore the two loading-policy assertions then (`test_browser_w2_c1`
  `test_the_photographs_follow_the_loading_policy`: (1440, 900, 4); `test_browser_w2_c2`
  `test_no_photograph_on_a_phone_nor_with_save_data`: one frame at the phone's size).
* **Lane D (Q3)** — the Arabic (and Italian / English) chrome shows the Personnes and Universités doors' glosses in
  French (`lang="fr" dir="ltr"`): reviewed translations, or a decision that the gloss is not drawn on those pages.
* **Steward** — `core/portico.css` is a new collected sheet linked from `base.html` (public pages only; the console's
  base empties the block). No new msgid: «Rechercher», «Voir l’espace» and the door labels already exist.

### Tests (lane l3, `test_ile_v5_l3`)

* **Updated, no guard weakened** (each asserts the new rule as precisely as the old one): `test_lume_v515_a.py` (the
  key's clock, its lift held through the turn, the glint and the shadow; `--lume-w` on the root; the hand-off from what
  was painted, ≥ 100 / ≤ 440 ms; the dissolve under the veil and no mark travelling; the first visit from 460 ms; the
  pane class; the lunetta's two destinations and `menu_only`; `core/portico.css` linked from 64rem and ≤ 3 000 B;
  NEW browser assertions: the word stands under the stage and inside the viewport, the arrival's first frame has
  `0 < ground < 1` at `--lume-t` 100 ms; the sill's hold waited for, not timed), `test_lume_v512_a.py` (the console's
  turn is `lume-key-clock`; under a pointer's veil a short dissolve where a View Transition is allowed, none under
  reduced motion or from the keyboard), `test_motion_v512_a_w2.py` (the public block's two sheets; a list's rows admitted
  to `rise-in`, bounded to the five lists), `test_browser_w2_c1.py` / `test_browser_w2_c2.py` (no portico frame fetched
  until lane C's menu-only frames — the assertions to restore are named in the docstrings; the key alone a 40 px
  square), `test_design_docs.py`'s sources (DESIGN_SYSTEM_2026 §2 weights, §12 keyframes; ACCESSIBILITY's citations).
* **Runs**: non-browser, the 15 files that read the chrome, the loader, the motion and the docs: **365 passed**, then
  the 10 red re-run green (84 + 6 passed) except the two **pre-existing on design-v5** (`test_cms_nav` portico's
  «Actualités», `test_nav_sheet_w2_c2` signed-in seat). Browser (one Chromium, under the lock): `test_lume_v515_a`,
  `test_lume_v512_a`, `test_browser_w2_c1`, `test_browser_w2_c2`, `test_motion_v512_a_w2`, `test_overlays_browser_w2_a`
  (77: 72 passed, the 5 red fixed and re-run green), `test_loader_w1_d`, `test_reduced_motion_w1_d`,
  `test_console_phone_browser_w3_a`, `test_motion_browser_w4_b`, `test_nav_sheet_w2_c2` (**89 passed**, the one red the
  pre-existing signed-in seat).
* Lane server 8783 stopped at the end; the Chromium lock released.

## Round 2 improvements (label v515-a-improve2, 29 October 2026)

Reviewed in HEADED Chromium 1234 on 8783 (database `ile_v5`), fr · ar, 1440 · 1024 · 390; captures
`C:/tmp/ile_v5_council/.work/v515-a/shots/r2-*` (probes `veilprobe.py`, `trace.py`, `cast.py`, `panels.py`,
`riseclock.py`, `rail.py`, `lcp.py`, outside the repository).

### M-1 — the click's dead frame and the hand-off (Lume)

**Traced, not guessed.** A Chrome trace across a real click (headed, 1440) and a bisection of the veil's layers:

| What was on the click's first frame | Cost on this machine (GPU process) |
|---|---|
| the stage's first raster — above all the halo's 96 px and 48 px **blurred box-shadows** | 95–120 ms (`DoEndRasterCHROMIUM`); halo hidden → ≈ 10 ms |
| the full-viewport **backdrop blur** | 45–70 ms of compositing on that frame and on every frame of the turn |
| the animated `drop-shadow` filter, the glint's `background-position` | a repaint of the key on every frame |
| the main thread (click, style, layout) | ≤ 17 ms — not the cause |

What changed (`static/css/v5/lume.css`, `static/js/src/lume/threshold.js`, `static/js/src/head/head.js`):

* the halo's glow is **pre-drawn** (two radial-gradient layers behind the paper), the key's shadow a **pre-drawn
  layer** (`.sig__turn::before`, the key's own mask in navy), the glint a still light — all three by **opacity only**;
* the **backdrop blur is gone** (a denser night instead; V5.15 §12 asks for «subtle blur» — measured, it was the price of
  every frame of the turn on this machine, and the reviewer had the same machine);
* the veil is **pre-warmed** once the page is idle (`html.lume-warm`, `requestIdleCallback`): laid out, its ground and
  stage rasterised as their own layers at an imperceptible 0.002 opacity (`pointer-events: none` as ever), so the
  click's first frame only changes opacities;
* the leaving page **counts the frames it painted** (`data-lume-painted`, through motion.js's `nextFrame()`) and
  `pagehide` hands on the LAST PAINTED one; the arrival starts at `min(150, age, painted)` ms — **≥ 250 ms of the turn
  play on the arriving page**; past 150 ms the leaving page's key only crawls (`lume-key-leave`, ≤ 40°) so the hand-off
  never jumps back more than a few degrees under the 140 ms dissolve; a real wait (400 ms, `is-departing`) completes the
  turn and holds it (`lume-key-finish`, no-preference only).

Measured (in-page rAF log from the click, headed, `/fr/faq/` → a bar link; 3 runs each):

| | before | after |
|---|---|---|
| 1440, 1× CPU — longest leaving-page frame | 133–208 ms | **29–41 ms** |
| 390, 1× CPU | — | **27–33 ms** |
| 1440, 4× CPU | 217 ms | **≈ 45 ms** |
| `--lume-t` handed on (real click) | 265 / 290 ms | **125–150 ms** |
| turn frames visible on the arrival (filmed, 1440) | 4–5 | **≈ 11** (`r2-cast-1440.png`, 439 → 625 ms) |

Note on the film: CDP's screencast itself lags ≈ 100 ms behind the page on this machine (its own frames before the
click arrive 10–40 ms apart, irregularly), so the first veil frame shows later in the film than in the page's rAF log.

### M-2 — the mega panel

* every entry carries its destination's **glyph on a tinted disc** (`templates/partials/_portico_glyph.html`, the
  registry's meanings: `signpost`, `award`, `presentation`, `sprout`, `circle-help`, `book-a`, `briefcase-business`,
  `factory`, `send`, `handshake`);
* a long door (Personnes): **one 64 px row rhythm** — glyph, title, at most one line; a title alone sits on the same
  centre line;
* **the legal notice is never clamped**: the door's own space's line («Italy Legal Entry ne délivre pas de visas…») is
  drawn whole in the panel's foot (`portico__notice`, beside the anti-fraud link) and stays the entry's description
  (`aria-describedby`);
* a short door (Entreprises, Institutions, Universités): **two door cards as tall as the lede** — the glyph and the way
  forward at the top, the title and its line at the foot; the lede at the body's size (it was the panel's tallest
  column);
* the lunetta of a short door no longer repeats the door's name (eyebrow only); the card's one row fills it through a
  morph (`grid-template-rows: minmax(0, 1fr)` — no strip at 120 ms, `r2-panel-fr-1440-switch120.png`); the pale rule
  under the lunetta removed.

### M-3 — the motion language, in time

* `static/js/src/rise.js` (new page-only entry, **873 B gzip**, linked in base.html's `reveal_sheet` block — the console
  empties it): a block **below the fold** is held 18 px low and transparent, and **rises over 420 ms as it enters**
  (IntersectionObserver, 40 ms apart for the blocks that enter together, once). Keyed to: chapters' heads, statements
  and prose; the registers; the home's trust statements and **pathways (each row's rule draws in gold — the home's
  route)**; **the Forum's programme (its timeline rule draws)**; **the FAQ's questions**; **the glossary's entries**;
  the living topics (`.registro`); the pages' link lists; `[data-motion="rise"]`.
* Never hidden: what is in view at load (no LCP held), the page head and the hero (their own sequence), reduced motion,
  html.rm, the keyboard (a focus inside a held block shows it), no IntersectionObserver, no script, print.
* The `view()` rises (finished off-screen) are removed. Measured after a 0.7-viewport scroll (`riseclock.py`): the FAQ
  at 390 — 7 blocks rising between 93 and 589 ms; the home at 390 (ar) — 3 blocks, 134 → 584 ms: the frames at 140 and
  640 ms differ.
* The door plate's light (`.porta`): 30 % gold, screened.
* `/vivre-en-italie/` on this database has no topic rows (nothing to key); `/projet/` carries none of the keyed lists.
  The Forum's programme is empty in `ile_v5`: its rule draw is checked in CSS only.

### Minors

* the language switch below 90rem: «Menu»'s 40 px hairline plate (`r2-panel-fr-1024-d0.png`);
* the sheet's search: placeholder «Rechercher» (existing msgid), the long name stays its label;
* the console's rail under the veil: no View Transition name on the rail's plate or the mark (`:is(.lume-go, .lume-in)`
  — they left a hole where they stood): the root's 140 ms dissolve alone (`rail.py`: 2 animations, both on the root);
* the real-click test: `test_a_real_click_hands_on_what_was_painted_and_leaves_the_turn_to_the_arrival` (fr 1440, ar
  390) — `--lume-t` ≤ 150 ms after a real click.

### Budgets (Python `gzip -9`)

| Asset | after round 1 | after round 2 | Limit |
|---|---|---|---|
| `static/css/dist/main.css` | 33 152 | **33 267** | ≤ 33 600 (the recorded exception) |
| `static/js/head.js` | 1 244 | **1 247** | ≤ 1 250 |
| `static/js/dist/shell.js` | ≈ 4 570 | 4 638 | ≤ 4 700 |
| `static/js/dist/rise.js` (new, public pages) | — | 873 | page-only |
| `static/css/dist/core/portico.css` | 2 663 | 2 985 | ≤ 3 000 |
| `static/css/dist/core/reveal.css` | ≈ 2 190 | 2 227 | page-only ≤ 6 KB |

### LCP (indicative: 8783, dev server, 390 × 844 mobile, 4× CPU, ≈ 1.6 Mbps / 150 ms RTT, **5 samples**, median)

| Page | first visit | seen | at the round-1 commit (same probe) |
|---|---|---|---|
| `/fr/faq/` | **1 996 ms** | 1 988 ms | 2 048 ms (3 samples) |
| `/fr/` | 2 644 ms | 2 624 ms | **2 604 ms** (seen) — unchanged by this round; with `rise.js` blocked 2 616 ms |

The FAQ's 2 532 ms in the review was a single sample: five give 1 996 ms. The home's 2.6 s on this throttled dev
server is the same before and after this round (the wordmark and the hero's frames; not this lane's to move here) —
the Performance Lead's 8782 (compressed, minified) is the measure of record before merge.

### Requests

* **Lane C** — unchanged from round 1 (the four menu-only frames). New: the Forum's programme rule draw and the living
  topics' rise are keyed and ready; they show as soon as `ile_v5` carries programme rows and topics.
* **Lane D (Q3)** — unchanged: the French glosses in the Arabic panel and the French body copy on the Arabic
  orientation page need reviewed translations (or a decision not to draw the gloss there).
* **Steward** — `static/js/dist/rise.js` is a new entry (public pages; the console's base empties the block). One new
  partial, `templates/partials/_portico_glyph.html`. No new msgid («Rechercher» exists).

### Tests (lane l3, `test_ile_v5_l3`)

* **New**: `test_lume_v515_a.py::test_a_real_click_hands_on_what_was_painted_and_leaves_the_turn_to_the_arrival` (fr
  1440, ar 390: a real click from the pre-warmed home; `--lume-t` ≤ 150 ms).
* **Updated, no guard weakened**: `test_lume_v515_a.py` (the turn compositor-only — no filter, no drop-shadow, no
  animated background-position; the shadow layer and `lume-shade`; the leaving key's crawl and the wait's finish, under
  no-preference only; the pre-warm; no backdrop blur; no blurred halo shadow; the painted-frame count through
  `nextFrame()`; the hand-off `min(150, age, painted)`; Esc and the arrival's end read the veil at rest — hidden, or
  pre-warmed at ≤ 0.01 opacity; the arrival from a 40 ms paint starts at 40 ms), `test_lume_v512_a.py` (a wait's turn
  is `lume-key-finish`), `test_motion_v512_a_w2.py` (the public block links `rise.js`), `DESIGN_SYSTEM_2026` (§12
  `lume-key-leave`, `lume-key-finish`, `lume-shade`; lume.css 21.6 KB).
* **Runs**: the 16 files that read the chrome, the loader, the motion, the docs and the bundles: **780 passed, 18
  failed** on the first run — 2 pre-existing on design-v5 (`test_cms_nav` portico's «Actualités», `test_nav_sheet_w2_c2`
  signed-in seat), the rest this round's stale assertions and two real bugs the guards caught (the wait's finish played
  under reduced motion; the frame counter went through `requestAnimationFrame` instead of the gate): fixed. Re-run of the
  failing files with the browser suites (`test_motion_browser_w4_b`, `test_browser_w2_c1`, `test_browser_w2_c2`):
  **152 passed**, 4 red fixed (the counter placed before `lume-go` under reduced motion; `wait_for_function` given a
  string under the CSP; the real-click test moved to the home, which the test database publishes) and re-run:
  `test_lume_v515_a`, `test_lume_v512_a`, `test_frontend_bundle_is_current`, `test_script_motion_gate`,
  `test_loader_rules`, `test_reduced_motion_w1_d`, `test_loader_w1_d` — **94 passed**.
* Lane server 8783 stopped at the end; the Chromium lock released.

## Finishing round F1 (label v515f-a-improve1, 29 October 2026)

After the third quality review (`C:/tmp/ile_v5_council/evidence/v515/a/QA_ROUND3.md`: Mega menu 3.5, Global Lume Loader
3.5; Navbar, Phone sheet, Motion language and Platform motion 4). design-v5 `7f2a02d` was already in the branch (the
merge was a no-op). Checked in HEADED Chromium 1234 on 8783 (database `ile_v5`): fr · ar · en at 1440, it at 1280, fr ·
ar at 1024, fr · ar at 390, ar at 375, reduced motion at 1440 and 390. Captures:
`C:/tmp/ile_v5_council/evidence/v515/a/f1-*.png`; probes and logs: `C:/tmp/ile_v5_council/.work/v515f-a-f1/`.

### M-1 — the slow path (Lume)

* **The hand-off is a phase of the clock** (`threshold.js` `go()`): before a wait, the time painted, at most 150 ms (the
  fast path of round 2, unchanged); once a wait has begun (`is-departing`), `TURNED_AT` = 480 ms — that page turned the
  key itself and lit the room half, so the arrival continues from the turned key, back in place, the room lighting and
  the sill near its 85 %. `head.js` clamps to 480 (its 150 clamp moved to the leaving page, which knows the phase).
* `lume-key-finish` 360 → 260 ms (the window in which an arrival can meet a half-finished turn is shorter).
* **The arrival's turn runs ≤ 120 ms behind its clock** (`lume.css`: the turn, its shadow and its glint,
  `animation-delay: calc(min(120ms, 480ms - var(--lume-t)) - var(--lume-t))`): the arriving page's long first frame
  (80–110 ms, round 3) lands on the resting key; from a wait's 480 ms there is no offset.
* Filmed (`f1-cast-*.png`, rAF logs in `.work/v515f-a-f1`):
  * **slow, fr 1440, 1.5 s latency**: the leaving page turns the key once and holds it, the word at 1 s; the arrival
    reads `--lume-t` 480 ms and its key is at identity on every frame — **no second turn, the room never goes dark**;
  * **fast, fr 1440**: `--lume-t` 150 ms; the arrival's key at rest on its first two frames (386, 401 ms), then 8°,
    22°, 65°, 122°, … 360° by 770 ms — the front half of the turn now visible;
  * **ar 390**: `--lume-t` 116 ms; the key at rest, then 2°, 3°, 6°, 14°, 25°, 38°, 51°, 107°, 130°… — ≈ 10 frames of turn;
  * **reduced motion, slow**: the still (no rotation), the arrival from 480 ms holds it and fades.
* The pre-warmed veil leaves a hidden tab (`visibilitychange`: `lume-warm` only while the page is shown).

### M-2 — the mega panel (Personnes, short doors, Institutions, Projet, the notice)

* **No ellipsis anywhere**: a long door's rows are ≥ 76 px, their line WHOLE (`text-wrap: pretty`); the two columns share
  each grid row, so a pair stands level; the glyph and the title hang from the row's top. Below 80rem a long door shows
  its titles alone (64 px rows). Probed: 0 clipped lines on every door at fr/ar/en 1440, it 1280, fr/ar 1024.
* **The brand is one isolated, unbroken LTR run** (`brand_bdi` filter: `<bdi dir="ltr">Italy Legal Entry™</bdi>`,
  `white-space: nowrap`): the ar 375 sheet's FAQ line no longer splits «Italy | Legal Entry™» across two lines.
* **Short doors (Entreprises, Institutions, Universités): destination rows**, one above the other — glyph on a 44 px
  disc, the title and its whole line, the way forward on a night disc at the end; 96–132 px each, sized to what they say
  (round 3: 280 × 220 cards with ≈ 120 px of empty gradient). Institutions' line is whole: «… chaque demande est lue par
  l'équipe du projet.» (no clamp).
* **Entreprises' lines**: the two sentences the companies' page sets beside the same links (existing msgids: «Signalez
  les besoins professionnels de votre entreprise.», «Présentation du projet et de la séquence proposée.»); a line shows
  only where the catalogue translates it (the first is French in it/en/ar → the title alone there). No request needed.
* **Projet**: every entry its glyph (the project the brand's arch; AGAMI the project team's mark and Réseau the
  authorised actor's, both through the registry's ACTOR map — a literal `badge-dot` is refused by the icon guard; the
  news `newspaper`; Contact `message-square-text`) and **AGAMI its line** «Le promoteur du projet» (its page's first
  chapter head, translated in it/en/ar).
* **The legal notice in every language**: the Personnes door's own-space line is `item.notice`, drawn in the foot of the
  panel AND of the sheet's door on every page — the locked French with `lang="fr" dir="ltr"` until the prescribed text
  exists in the page's language (as the door's gloss already does); never drawn twice.

### Minors

* **One current item**: on `/fr/forum/` only the Forum item carries `aria-current` (`_one_current`: a page that is a
  top-level item is current there only; the Institutions door and its Forum entry are not marked).
* **The sheet's entries carry the panel's glyphs** (20 px on a 32 px tinted disc; chrome.css).
* **The warm veil on a hidden tab**: removed while hidden (above). Scroll at 390/4×: not re-measured in this round —
  the layer is now absent whenever the tab is in the background; the desktop measure of round 3 stands (neutral).
* **LCP** (8783, 390 × 844, 4× CPU, ≈ 1.6 Mbps / 150 ms RTT, 5 samples, median; the machine shared with three lanes'
  browser runs): `/fr/` first 2 452 ms, seen 2 512 ms; `/fr/faq/` first 2 216 ms, seen 2 164 ms. `rise.js` now
  `fetchpriority="low"` (out of the LCP image's way). **Request to the Performance Lead**: the 5-sample measure on 8782
  after the merge (8782 serves design-v5, not this branch).
* **The richer motion vocabulary** (`[data-reveal=mask]`, `[data-timeline]`, `.card--link`, `[data-spotlight]`,
  `.bande-foto__frame`) is still dormant: **hook contract for lane C** — `data-reveal="mask"` on a photograph's
  `<figure>` or `<picture>` (its mask opens as it enters), `data-timeline` on a list whose rows are stations (its line
  draws down as it is read), `.card--link` on a whole-card link, `data-spotlight` on a surface that follows the pointer;
  nothing else is needed — `v5/_reveal.css` already keys them. The photo mask and the timeline first.
* `/vivre-en-italie/`: still 0 topics on `ile_v5` — re-check once lane C's living page has content.
* Q3 carry-over (lanes C/D): the Personnes gloss is French in en/it/ar, the Arabic FAQ questions and the Forum title are
  French — unchanged, not lane A's.
* The lume shadow layer's offset is straight down (`translate: 0 1.5%`): the RTL guard (`test_rtl_static`) caught round
  2's horizontal 1 % with no twin; the brand never mirrors, so the shadow now needs none.

### Budgets (Python `gzip -9`)

| Asset | round 2 | F1 | Limit |
|---|---|---|---|
| `static/css/dist/main.css` | 33 267 | **33 448** | ≤ 33 600 |
| `static/js/head.js` | 1 247 | **1 248** | ≤ 1 250 |
| `static/js/dist/shell.js` | 4 638 | **4 690** | ≤ 4 700 |
| `static/css/dist/core/portico.css` | 2 985 | **2 993** | ≤ 3 000 |

### Requests

* **Lane C** — the hook contract above (photo mask, timeline); the four menu-only frames (unchanged).
* **Lane D (Q3)** — unchanged: reviewed translations of the French glosses / body copy on the Arabic pages, or a
  decision not to draw the gloss there; the prescribed Personnes notice in it/en/ar (it shows in French until then).
* **Performance Lead** — the 5-sample LCP on 8782 after the merge.
* **Steward** — no new file; no new msgid (every line added is an existing, translated catalogue string).

### Tests (lane l3, `test_ile_v5_l3`)

* **New**: `test_lume_v515_a.py::test_a_slow_navigation_s_arrival_never_turns_the_key_a_second_time` (browser, fr 1440,
  1.5 s latency: `--lume-t` ≥ 400 ms, the arrival's first-frame key turned or at identity);
  `test_cms_nav.py::test_portico_notice_stands_in_every_language_and_one_item_is_current` (the notice in it/en/ar, said
  `lang="fr"` while untranslated, never twice; `brand_bdi` isolates and escapes; on the Forum only the Forum is current).
* **Updated, no guard weakened**: `test_lume_v515_a.py` (the hand-off as a phase — ≤ 150 before a wait, `TURNED_AT`
  480 after; head.js's clamp 480; the arrival's turn offset; `lume-key-finish` 260 ms; the warm veil off a hidden tab),
  `test_cms_nav.py` (the Personnes own-space line is the notice, not a second line; Entreprises' two lines; AGAMI's
  line), `test_nav_sheet_w2_c2.py` (the Forum's glyph on its row AND on the Institutions door's Forum entry: two
  handshakes, both asserted in place), `test_browser_w2_c2.py` (the sheet's door panel: one decorative glyph per entry,
  nothing else drawn), `test_motion_v512_a_w2.py` (`rise.js` `fetchpriority="low"`).
* **Runs**: 12 files (lume v515/v512, the W2-C1/C2 browser suites, nav sheet, cms nav, icons, motion v512 W2, RTL
  static, design docs, the two bundle checks): **278 passed, 3 failed** → the sheet glyph assertion updated (2 passed on
  re-run with the new slow-path test); the other two are **pre-existing on design-v5** (checked on the stashed tree):
  `test_cms_nav::test_portico_gives_every_door_its_panel_from_live_content` (Projet's «Actualités» absent on the test
  database — every F1 assertion before it passes) and `test_nav_sheet_w2_c2::test_signed_in_…account_popover`. A
  wider non-browser run (motion, reduced motion, loader, tokens, layout, mobile RTL, i18n): 878 passed, 2 failed —
  `test_rtl_static` (round 2's shadow offset, fixed here: 142 passed on re-run) and
  `test_mobile_rtl_w4_a::test_the_500_keeps_its_semicolon_with_its_words` (pre-existing, unchanged by this lane).
* Lane server 8783 stopped at the end; the Chromium lock released (held 09:05–09:20 and 09:21–09:38).
