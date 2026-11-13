# W2-D — accessibility + performance check (one pass)

Italy Legal Entry™ · V5.4 under V5.5 (delivery mode) · role `w2-d-a11y-perf`: built nothing, changed nothing in the family's
code · 9 October 2026, 20:10–21:40 · branch `v54-w2-d` at `a649654`, tree clean before and after · lane 5 (8785, `ile_v5_l5`).
Subject: the hero in the real home and the home around it (`/fr/`, `/ar/`; `/it/`, `/en/` for names), the Phase 3 page the
lane serves and the interim page (gate G3 closed — what the site shows today), plus the other pages its sheets reach.

**Verdict: SHIP_AFTER_FIXES.** No P0. No WCAG 2.2 AA failure found. No performance regression against the W1-0 «before»
set: LCP 464–628 ms earlier, the longest load task 124–154 ms where it was 710–938 ms, CLS ≤ 0.038, nothing loops.
Left: one decision to record at the merge (F1), small corrections, most of one line (F3, F5, F6, F8, F9, F10), and a defect that
is **not this family's** but stops every measurement on 8782 and any deployment (F2).

## 1. Findings

| # | Severity | Finding (measured) | Fix |
|---|---|---|---|
| F1 | major | **The home's CSS is over plan §2.6's page-type ceiling.** 57 180 B gzip on the wire in three render-blocking sheets (`main.css` 43 249 · `pages.css` 4 000 · `hero.css` 9 931) against 39 114 B in two at `v54/base` and 46 753 B on design-v5 today: 9 874 B over the ceiling (baseline + 8 KB = 47 306 B; «a family over its ceiling does not merge»). Each sheet is inside its own budget (`main.css` 42.2 KB ≤ 45; `hero.css` 9.7 KB ≤ 14, F4) and the legacy rules went first, so the excess is the hero's sheet, which §1.17 makes a page entry without amending §2.6. Effect measured: none to the worse (`hero.css` is in at 635 ms, `main.css` — the last blocking sheet — at 1 079 ms; LCP 1 600 ms against 2 064) | No code. The merge step records the home's ceiling in DL54 on this measurement (`main.css`'s ceiling + `pages.css` + `hero.css`'s F4): §2.6 item 5 lets the CD raise a ceiling by 2 KB only. `test_css_budget.py` (plan §2.7) does not exist: nothing pins any ceiling today |
| F2 | major — **not this family's** (W1-D, the steward) | **`collectstatic` fails under the production storage** on design-v5 (`8246a7f`) and on this branch: `SuspiciousFileOperation` from `apps/portal/static/portal/console.css:15`, `@import url("../../../../static/css/v5/_loader-light.css")` (W1-D, `fa07163`) — the raw entry is collected and the manifest storage follows the import out of `STATIC_ROOT`. 8782 has not been rebuilt since 5 October, so nobody met it: no family can be measured there, and a deployment stops at this command | Keep the import out of what is collected (a build-only entry outside `static/` that imports the light sheet and the console sheet), then a test that runs `collectstatic` with `CompressedManifestStaticFilesStorage` into a temporary root. For this check the raw entry was left out of the lane's own twin (`--ignore "portal?console.css"`): the home does not load it |
| F3 | minor | **A press in the hero is 4–5 × dearer than on the V4 page, inside the 200 ms budget.** Event Timing at CPU × 4: a press during the movement 136–152 ms median (max 200), Tab into the hero 56–120 (max 168), a tap on a settled tile 128–200, the replay 48–144; the before set's proxy was 32. Each state change recalculates the hero's `:has()` rules (the long task of a hover's start: 86–140 ms, 44–74 of them style), and `pointerdown` reads the geometry in the handler | `hero.js`: in the `pointerdown` handler defer `flow()` through `nextFrame()` (the hover already runs before the press), so the handler writes classes only. Re-measure the tile tap |
| F4 | minor | **CD condition C-5's layer clause (≤ 2.5 MB at 1 ×) is not met on the desktop.** LayerTree (it answers in this headless shell): at rest 0 hero layers; while the discovery plays 73 drawing layers, ≈ 10.9 MB of backing (layer bounds × 4 bytes) at 1440 × 900 (17.0 MB at 1920 × 1080, 3.5 MB at 390 × 844 @1 ×), ≈ 8.4 MB during a hover's flow; all released at the settle. No dropped frame, no long task traced to it | None needed to ship. If wanted: the three niche-sized boxes are 5.4 MB of it (`.he-door-box` 2.3, `.he-niche` 1.6, `.he-niche__halo` 1.5): clip the halo to the arch's box, as the CD wrote |
| F5 | minor | **The eight pathway rows show no sign of being links at rest on a screen that hovers**: ink titles, no underline, the arrow at opacity 0 until hover or focus — the same drawing as the trust chapter's four rows, which are not links. No criterion fails (name, role, focus and target are right; forced colours draw them in `LinkText`) | `pages.css`: under `(hover: hover)` rest the arrow at .6, as the hero's own arrows rest, and 1 under the hand |
| F6 | minor | **Text-only 200 %** (brief A9, CD C-4; WCAG 1.4.4 is met by zoom): the hero holds (0 px past a tile, no overlap), but the phone page scrolls sideways — 66 px at 390, 96 px at 360 — on the register's calls (`.entry__cta` keeps `white-space: nowrap`); on the Arabic page the promoter's name overlaps its neighbours (a 32 px line under a 40 px size: the base sheet's Arabic metric) | `pages.css`: `.home-entrances .entry__cta { white-space: normal; flex-wrap: wrap; }`. The Arabic line height is W1-A's |
| F7 | minor | **On phones the replay button takes focus after the four tiles and stands above them** (DOM: origins, then niche; phone composition: band, then tiles). Brief E5 («Tab = visual order») holds at every other stop and size; meaning and operation are kept (2.4.3 is not failed) | Accept and say it in `docs/ACCESSIBILITY.md` §3, or try `reading-flow` on the phone grid later |
| F8 | minor | **A touch screen in the desktop layout never draws the four calls** (≥ 64 rem with `hover: none`: an iPad lying down): they wait for a hover, and the register that carries them is not drawn there. The links keep name, sentence and arrow | `hero.css`: `@media (hover: none) and (min-width: 64rem) { .he-origin__call { opacity: 1; } }` |
| F9 | minor | **The hero's rows are final only when the whole hero is parsed.** Under profile A + CPU × 4 the page paints while the document is still arriving: in 5 of 76 loads an early frame drew the hero before its rows were final — the path 40 px higher where it was measured, the height of the stations' row (`--labels-h`): three times the path alone (≤ 0.0003), once with the statement (0.023, Arabic desktop; CLS that load 0.038 with the navigation's), once on a phone (0.070, flagged by the browser as following the viewport's set-up and so outside CLS) | `hero.css`, Phase 3 variant only: give the stations' row its height before the list arrives, `[labels] minmax(var(--labels-h), auto)` |
| F10 | minor | **The brand name in the `h1` carries the locked text's language.** `<span class="he__name" … lang="fr">ITALY LEGAL ENTRY™</span>` on the Italian, English and Arabic pages (unmarked on the French one), while the header's lock-up marks the same name `lang="en"`: on `/en/` a French voice is asked to read an English name. Proper names are outside 3.1.2; a wrong mark is still worse than none | `_hero.html`: the name's span takes `lang="en"`, as the lock-up does, instead of `d.title.lang` |

Looked at and left: «Connexion» on the night row takes the paper ring (the button rule reads the legacy `--focus-ring-color`:
W1-C's retarget) — as drawn it is a paper halo and a teal ring, 3.1–3.7 : 1 outside, clearly seen; the replay's ring lies on
the open door's band along one side on a phone lying down (2.3 : 1 there, 6.3–7.6 elsewhere).

## 2. Accessibility — what was run and what it read

Dev shape, lane 5. Phase 3 page unless said; the interim page (gate closed in the server process only, no database write)
repeated structure, keyboard, contrast, reflow, spacing, targets and reduced motion with the same results.

| Check | Cells | Result |
|---|---|---|
| Names, roles, outline (CDP tree; axe-core 4.13.0, WCAG 2.0–2.2 A / AA) | fr, ar × 1440 × 900, 390 × 844; it, en for the tree | **0 axe violations** (8 runs with the interim page). One `h1` (the name, hidden, + the promise); levels 1 · 2 · 3, none skipped; list «Séquence du projet pilote» (6); `nav` «Les quatre accès de l'écosystème»: four links named by their word, described by sentence + call; `button` «Rejouer l'animation de la porte», named in four languages. 0 duplicate id, 0 broken ARIA reference, 0 `title`; door and plates out of the tree (`aria-hidden`, `alt=""`). Arabic: 60 French runs carry `lang="fr"`, 0 unmarked |
| Keyboard, both ways (real Tab presses) | 11 cells: fr, ar at 1440 × 900, 1366 × 768, 1024 × 768; fr 1920 × 1080; fr, ar 390 × 844; fr 360 × 800, 844 × 390 | 562 stops, the same list reversed; **0 without `:focus-visible`; 0 covered** (15-point hit test per stop); the highest a focused stop comes to rest is y = 72–98 px, clear of a sticky bar that ends at 57 px (2.4.11). Order = visual order except F7. Enter and Space replay the sequence (36 animations, 29 on a phone), focus stays; Escape or any key inside the hero lands the still in the same check; a key outside the hero does not stop it |
| Focus ring on pixels (shot with and without its outline) | the 280 stops of `main` | Whole on every side (≥ 0.98; one two-line link whose ring follows its lines — looked at). CD M1 closed: no ring cut at 1366 × 768 or 1024 × 768. Ring against its outside, p5: hero 4.1–5.9, replay 6.3–7.6, paper 3.7, brand chapter 3.5, plate 4.1, night link 9.9 |
| Contrast on pixels (the programme's p5 glyph method) | 9 cells + 3 interim; rest, hover, focus, press | **0 run under 4.5 : 1** (3 : 1 from 24 px); **every hero run under 16 px ≥ 7 : 1** (brief E1): calls 9.4 under the hand and the keyboard, 8.3 pressed (M2 closed); stations 9.2 on the wall, 14.0 on the night; «ENTRÉE EN ITALIE» 10.2–10.4; sentences 10.3; secondary 7.5–7.7; CTA label 15.2 · 7.5 · 10.2. Chapters: ink 13.6–16.2; `--text-2` 6.46 (4.5–5.5 as drawn on the 13 px labels at DPR 1: subpixel fringes; lowest 4.52); links 5.7; the brand button's label 5.29. Marks ≥ 3 : 1 (path 6.4, gold run 10.1, treads 4.9–10.4, rail 7.8, spine 6.3) |
| Reduced motion, first load of a session | fr, ar 1440; fr 1024; fr, ar 390; fr 844 × 390 | **A real still**: 0 `animate()` calls, 0 running animations in 83 samples over 5 s, `he is-ajar`, no replay button; 0.6 s against 5.6 s: 0 px; against the settled hero of a page that moves: 0 px in four cells, 56–67 px of ≈ 1 M in two (the arch's hairline). Hand and keyboard: the state in the next frame, nothing runs. Nothing in `main` declares a transition or an animation longer than 0 |
| Forced colours, light and dark | fr, ar 1440; fr 1024; fr, ar 390 | Nothing plays; text is `CanvasText` or `LinkText` on `Canvas` (14–21 : 1), 0 pair under 4.5; every stop keeps a whole `Highlight` ring; calls shown; four stems; steps in `CanvasText`; the stage present (C-3, E7). Captures looked at |
| No script | fr 1440, 390; ar 390 | The whole page, the door closed as drawn (ajar under reduced motion, by CSS) |
| Reflow 320 px (320 × 568; 320 × 256 @4 = 400 % of 1280 × 1024) | fr, ar | No sideways scroll, 0 text over text, 0 text cut, every tile holds its word, the arrow off the word (B1 closed) |
| Zoom 200 %; WCAG 1.4.12 spacing | 5 windows; 11 cells from 320 to 1440, fr + ar | Clean: no scroll, no overlap, nothing cut; tiles grow with their words |
| Targets (hit-tested outwards from each centre) | 10 cells | **None under 24 px** in the hero and the chapters (a pathway's 22 px title link answers on its whole row); **under a finger none under 44 px**: primary 52, secondary 44 (landscape too: m3 closed), tiles 158 × 64 to 173 × 72, replay 44 × 46–72, chapter links 44 (their `::after`); gaps ≥ 8 px |
| Other pages the sheets reach (login, anti-fraud, «Le projet», a door page, the pilot, the forum; two in Arabic) | 1440, 390 | 200; 0 overflow, 0 clipped text, 0 shift, 0 axe violation but the login's known `target-size` (in the before set too); the entrance's door is drawn |

## 3. Performance — against `w1-0/before/MANIFEST.json`

The before set's protocol and analysis, imported read-only (`tools/analyse.py`, `an_pfr.py`, `capture.py`): profile A
(150 ms RTT, 1.6 / 0.75 Mbps), CPU × 4, cold loads, n = 9 per cell interleaved, HeadlessChrome 153. Served by **the lane's own
compressed twin on 8785** — the plan's 8782 shape (DEBUG off, `CompressedManifestStaticFilesStorage`, hashed URLs, gzip on
the wire; settings outside the repository) on the lane's port and database; 8782 itself untouched. The machine was busier
than in the before set's windows (26 % / 37 % before / during a load, against 15 % / 26 %): a bias against the after set.

| Cell (median of 9) | LCP before → after (range) | Δ | FCP | Longest load task | Total blocking time | CLS | LCP element |
|---|---|---|---|---|---|---|---|
| fr · 1440 × 900 | 2 064 → **1 600** (1 364–1 756) | −464 | 2 064 → 1 196 | 710 → 129 | 293 → 319 | 0.002 → 0.016 | door `.webp` 400 → door `.avif` 576 (9 / 9) |
| fr · 412 × 823 @1.75 | 2 100 → **1 600** (1 452–1 812) | −500 | 2 100 → 1 216 | 746 → 124 | 261 → 173 | 0 → 0 | `p.hero__body` → door `.avif` 400 (9 / 9) |
| ar · 1440 × 900 | 2 356 → **1 728** (1 656–1 796) | −628 | 2 356 → 1 376 | 938 → 154 | 536 → 375 | 0.019 → 0.018 (max 0.038) | door → door (9 / 9) |
| ar · 412 × 823 @1.75 | 2 328 → **1 716** (1 668–1 928) | −612 | 2 328 → 1 368 | 914 → 154 | 509 → 274 | 0.003 → 0 | text → door (9 / 9) |

- **LCP element.** The door's image in 56 of 56 traced loads, requested once (the preload is reused). On phones it replaces the text
  the V4 page had: the image lands 350–385 ms after first paint and still 500–610 ms before the old LCP. The brief's F1 and the CD's C-5 (median ≤ 2.2 s, the door every time) are met.
- **Long tasks.** The 710–938 ms first-render task is gone: the page now paints its header first, and the load is 6–8 tasks of
  56–190 ms (their sum 420–760 ms against 1 200–1 960 ms); total blocking time is lower in three cells and 26 ms higher in the fourth,
  on the busier machine. None introduced beyond the before set's own.
- **CLS.** ≤ 0.038 in every load. The hero adds nothing but F9; the 0.013–0.023 at 1440 is the main navigation's box growing
  while the header is parsed (22 of 28 desktop loads) — W2-C1's, §4.

| On the wire, fr (bytes) | before | after | Budget |
|---|---|---|---|
| CSS, render-blocking | 39 114 in 2 | **57 180 in 3** (+18 066) | F1 |
| JavaScript | 36 892 in 8 | 44 318 in 7 (+7 426) | ≤ 45 KB a public page: 43.3 KB, 1.7 KB left; the hero's chunk 6 982 B ≤ 7 KB |
| CSS + JS requests before `load` | 10 | 10 | ≤ before: met |
| Fonts (ar) | 304 340 in 6 (535 436 in 14) | 20 956 in 2 (53 184 in 3) | ≤ 25 KB (≤ 56): met |
| Images, 1440 | 45 324 in 5 | 175 122 in 12 — the door 47 115, four plates 11 718, **the navigation's four photographs 109 096** | door row ≤ 110 kB: 58.8; §4 |
| Images, 412 | 45 324 in 5 | 48 022 in 7 (the door 33 418) | F4's ≤ 45 kB: 41.1 |
| Document (gzip) | 10 306 | 14 001 (933 elements against 725) | — |

**The hero's life** (same twin, profile A, CPU × 4, n = 5 per cell, no input before the settle):

| Window | fr 1440 | fr 412 | ar 1440 | ar 412 | Bar |
|---|---|---|---|---|---|
| The discovery — main thread, ms per second | 61.4 (52–79) | 52.0 (43–83) | 57.8 (54–76) | 44.4 (42–53) | C-5: ≤ 60 |
| — tasks over 50 ms (longest) | 2 (67) | 0 (48) | 1 (55) | 0 (43) | none «serious» |
| — length | 3 561 ms | 2 784 ms | 3 562 ms | 2 774 ms | ≤ 5 s; once a session |
| At rest, 3 s | 0 frames, 0 timers, 0 rAF, 0 animations, 0 `will-change` | same | same | same | nothing loops |
| The hand's flow (2.4 s window) | 218 ms/s, 2 tasks (92) | 125, 1 (86) | 216, 2 (93) | 104, 1 (68) | F3 |
| The replay | 104 ms/s, 2 tasks (70) | 92, 0 | 95, 2 (70) | 96, 1 (60) | — |
| Layout shifts from the settle on | 0 | 0 | 0 | 0 | ≤ 0.05 |

The discovery stands at C-5's 60 ms/s on the desktop, on a machine 30–44 % busy during those loads; under it on phones.

## 4. Seen, not this family's

- **F2**, above: `collectstatic` (W1-D's file; the steward's before the next 8782 window).
- **W2-C1 — the navigation's four photographs are requested before `load`** in 18 of 18 desktop loads in production shape
  (17–35 ms before it, 109 KB), where plan §1.12 says «nothing before `load`». They start 675–1 043 ms after the LCP, so the
  door is not delayed. The implementer's reading (NOTES §8.4) is confirmed.
- **W2-C1 — the main navigation shifts while the header is parsed** (0.013–0.023 per load at 1440; the French desktop's CLS
  goes from 0.002 to 0.016), and its phone drawer opens in 104–120 ms at CPU × 4 (max 192) where the V4 one took 48–56.
- **W1-C — a `.btn`'s focus ring ignores the night context** (`--focus-ring-color`, not `--focus-ring`).
- The footer's sixteen links are 24 px tall under a finger (the chrome's).

## 5. Method, limits, not done

- Own headless Chromium (the repository venv's Playwright 1.63), own profiles under `.profiles/w2-d-a11y-perf/` (removed after
  each run; none left), one browser at a time, no pytest. 251 browser starts waited on the benchmark lock: never present; never
  created by this role. No run crashed. Never 8780, 8782, 9222 or 9223. The senior reviewer worked beside this check on 8885.
- Servers on 8785, each stopped after its series: the dev server (accessibility), the compressed twin (performance), the dev
  server with gate G3 closed in the process (the interim page). This role wrote nothing to the lane's database (anonymous page loads; the gate was closed in the
  process, not in the flag's row) and nothing to the worktree but this report (the twin's `STATIC_ROOT` was a scratch folder,
  removed).
- **The timing figures are a lane's screen for regressions, not the Performance Lead's PASS on 8782** (plan §2.6): same shape
  and protocol, but another port and database, no lock held, a busier machine. HTTP/1.1 only.
- Not done: a screen reader with a person (E9), a real phone, WebKit and Firefox, the hero's parity check of §1.17 (pixels and
  clock against the re-held prototype). The Forum's banner is not on the page at the lane's date (its gate closed on
  2 October). The contrast figures at DPR 1 carry headless Chromium's subpixel fringes; at DPR 2 they equal the tokens'.

## 6. Evidence and tools

`C:/tmp/ile_v5_council/evidence/v54/w2-d/a11y-perf/` — `s1_structure.json` … `s7_others.json` (one per check),
`interim/` (the same with the gate closed), `perf/twin-P/` and `perf/twin-D/` (`runs.jsonl`, one trace kept per cell),
`perf/summary-*.json`, `perf/layers.json`, `perf/shifts.json`, `bytes_by_tree.json`, `shots/`, `look/` (the captures looked
at), `logs/`, `README.md`. Tools, outside every repository: `C:/tmp/ile_v5_council/.work/w2-d/w2-d-a11y-perf/` (`rig.py`,
`s1_structure.py` … `s7_others.py`, `perf_trace.py`, `perf_compare.py`, `perf_layers.py`, `perf_shifts.py`, `look.py`,
`twin/settings_8785_twin.py`, the start and stop scripts).
