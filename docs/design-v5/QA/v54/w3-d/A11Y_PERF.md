# W3-D · The journey «La soglia» — accessibility + performance check (one pass)

Label `w3-d-a11y-perf`, 11–12 October 2026 — the family's one accessibility/performance check (V5.5: implement → review
once → fix → ship). Built nothing, changed nothing in the family's code. Checked branch `v54-w3-d` at `b9907ab` — its
code as of `7bc76e6`; `5860677` and `b9907ab` above it add only the notes and the senior review — against the merge
base with design-v5, `d40f209` (design-v5's tip `1c03e3b` adds no CSS, JS or template since).

**Lane.** Lane 6, port 8786 (this role's alone; the reviewer worked on 8886). The dev server from
`C:/tmp/ile_wt/v54-w3-d` on `ile_v5_l6`, `ILE_REFERENCE_DATE=2026-10-03` — `2026-10-01` for the home's passage only
(gate G3 closed by the flag's own date, no data changed) —, `DB_CONN_MAX_AGE=0`, `--noreload`, no preview flag; the
merge base served on the same port from an export of `d40f209` in this role's scratch folder for every before/after.
Signed-in pages through sessions minted with `Client.force_login` on `ile_v5_l6` (no password used, typed or stored),
revoked at the end. Headless Playwright Chromium (the venv's), its own profile under
`C:/tmp/ile_v5_council/.profiles/w3-d-a11y-perf/`; one browser and no pytest at a time; every series waited on
`PERFORMANCE_BENCHMARK_LOCK` (never present, never created). **No run crashed.** Never 8780, 8782, 9222 or 9223.

**A first sitting of this check was cut at 22:47 on 11 October**, in the middle of its console before/after and before
it wrote anything. Its finished series ran on the same code and data and are kept: 1024 / 1280, 320, text spacing,
reduced motion, forced colours, at rest, and the home's series. This sitting re-ran the desktop and phone passes
whole (`desk-r2/`, `phone-r2/`: the same figures, load for load), re-ran the console before/after whole, re-ran the
home's before/after at n = 9, and added what the first sitting had not reached: the tap's cost and its traces, the
Stepper's hit test, page-level checks of the opened spine and of text spacing, the nodes on pixels, the merge base's
axe, the motion probe with a positive control, and the journey's cost isolated in the page on both trees.

Evidence: `C:/tmp/ile_v5_council/evidence/v54/w3-d/a11y-perf/` — `desk-r2/`, `phone-r2/` (keyboard, pixel contrast,
hit areas, the accessibility tree, axe; one JSON per page and region crops), `mid/`, `reflow/`, `spacing/`, `reduce/`,
`forced/`, the home's `*-home/`, `desk-base/` (the merge base), `extra/`, `tap-head.json`, `tap-trace/`,
`click-head.json`, `trans-head.json`, `trans-base.json`, `relayout-head.json`, `relayout-base.json`, `rest.json`,
`rest-r2.json`, `perf/` (`runs-console-r2*`, `runs-home-r2*`, traces). Probes:
`C:/tmp/ile_v5_council/.work/w3-d/w3-d-a11y-perf/`.

## Verdict — SHIP_AFTER_FIXES

**1 blocking · 0 major · 2 minor** in W3-D's files. The blocking one is the owner's V5.8 rule, not a broken page: the
console page types' shared CSS lands **603 B gzip over its hard ceiling** (51 530 against 50 927 B — the review's M1,
measured again here); the merge is sent back until the rail's sheet loads only where a journey is drawn. **No WCAG 2.2
AA failure in the journey** — fr and ar; 1440, 1280, 1024, 390 touch and 320; keyboard, names and roles, contrast on
pixels, targets, reduced motion, forced colours, text spacing. **No load regression attributable to W3-D:** the
journey adds 0.4–2.3 ms of style and layout at CPU × 1 (3–19 ms at × 4) over V4's, isolated in the page; no script,
no request, nothing at load, nothing looping; the public pages lose 1 281 B gzip. The two minors: the phone's «Où j'en
suis» costs a 64–153 ms task at × 4 when opened (INP 96–128 ms — most of it the shell's `html:has()` rules, not the
journey), and the Stepper's line takes the pointer in a 2 px strip of each question link.

## What was measured

| Key | Account | Page | What it shows |
|---|---|---|---|
| D1 | `seed-person` | `/espace-reserve/` | the file **on threshold A** (SELECTION): eight items, the threshold current |
| D2 | `qa-person` | `/espace-reserve/` | step 2 |
| D3 | `qa-doc-person` | `/espace-reserve/` | step 1 (W1-0's dashboard persona) |
| F1 | `seed-person` | `/espace-reserve/dossiers/0FEEBAE3A9/` | the case file: the dated spine on threshold A, the timeline (12 events) |
| F2 | `qa-doc-person` | `/espace-reserve/dossiers/EE167596D4/` | the case file at step 1 (W1-0's case-file persona) |
| S1 | `qa-fresh-person` | `/espace-reserve/ma-situation/` | «Ma situation»'s Stepper, nothing answered |
| S2 | `qa-doc-person` | `/espace-reserve/ma-situation/` | the same, W1-0's persona |
| H1 | — | `/` (on 1 October) | the home's passage «la linea», four steps |

× fr / ar. Passes: 1440 × 900 (fine pointer) and 390 × 844 (phone emulation, touch) — keyboard walk, pixel contrast,
hit areas, Chromium's accessibility tree, axe-core (W1-0's copy) on `wcag2a/2aa/21a/21aa/22aa` and `best-practice`,
W1-0's `health.js`; 1024 × 768 and 1280 × 800 (the level line's floor); 320 × 640 (400 % reflow); WCAG 1.4.12 text
spacing at 1440, 1280, 1024 and 390 (the home also at 768); reduced motion (`emulateMedia`) and forced colours
(Chromium's emulation) at 1440 and 390, the disclosure opened from the keyboard wherever it is shown. **216 recorded
accessibility loads (210 on the branch, 6 on the merge base): 0 CSP reports, 0 console errors, every response 200.**

How the probes read pixels (W3-B's probes, the journey's own added). The keyboard walk clips every stop focused, then
the same clip at the same scroll with nothing focused: the indicator is the pixels that changed. Contrast: every text
run of `<main>` — and of each journey region, the opened list included — fully in view and under no fixed layer, its
computed colour with its opacity chain against the pixels under it, the page re-drawn with every glyph transparent:
the dominant pixel, and the worst pixel covering ≥ 5 % of the run. Hit areas: `elementFromPoint` probed outward from
each target's centre.

## Accessibility

| Check | Result |
|---|---|
| axe 2.0–2.2 A/AA | **0 violations from the journey**, 1440 and 390, fr and ar; best-practice 0. One violation on the case file at 1440 (F1, fr and ar): `scrollable-region-focusable` on the inspector `aside.file-grid__inspector` — **the merge base fails the same way** (`desk-base/F1-*`): the scroller is W3-E's (O1 below). «Incomplete» never in the journey: W3-A's night rail, the console menu's `aria-controls` to its closed drawer, the case file's state select and «Ma situation»'s fields |
| Keyboard, fr and ar | the journey is reading matter and puts **no stop** in the tab order at 1440 (the level line, the spine and the timeline are static lists — right) and exactly one on phones: «Où j'en suis», after the NowPanel's primary; Enter opens it onto the spine and closes it again. «Ma situation»: the eight question links in order, each named by its question. **1 754 stops over 70 walks** (1440, 390, forced colours; fr and ar): every one named, every one `:focus-visible` |
| Focus visible | the journey's stops: the summary's ring — laguna-550, 2 px at 2 px — change contrast **3.94 : 1**, ring fill 1.48; the Stepper's links 3.94 : 1, fill 1.05–1.17; under forced colours Highlight, 11.31 : 1. No weak ring in the journey. The home's two weak readings are not the journey's: the promoter's link cut by the viewport's bottom edge (W3-B's O1 pattern) and the skip link caught mid-entrance in Arabic |
| Focus not obscured (2.4.11) | 0 stops hidden or partly covered by a sticky or fixed layer, journey or not (the shell's `scroll-padding-block` holds on phones) |
| Names, roles, structure | the dashboard at 1440: `list «Où j'en suis»`, seven items — eight on threshold A, the current one «Autorités compétentes : décisions administratives · Phase gérée par un acteur autorisé · Vous êtes ici», `aria-current="step"`; threshold B hidden and its caption said in step 6 («Territoire italien : accueil et inclusion. Arrivée et premières démarches»); the shores and every glyph hidden; no disclosure exposed at the wide width. Phones: `DisclosureTriangle «Où j'en suis» expanded=false`, the list absent from the tree until Enter, then `expanded=true` and the same list. The case file: `list «Où en est ce dossier»` / «أين وصل هذا الملف», each reached step with its date. «Ma situation»: `list «Progression»`, eight items, the current `aria-current="step"`. One h1; 0 nameless controls. Behind / here / ahead is carried by the order and `aria-current`, not by the dots alone |
| Contrast on pixels | **1 852 text runs, 0 below AA** against the dominant pixel; one below AA against its worst pixel — a timeline date whose box crosses another colour on ≥ 5 % of its pixels (5.88 : 1 dominant, 4.05 against that colour), the same run with the same figures at the merge base. The journey's **492 runs**: «Vous êtes ici» **5.24 : 1** (`--accent-text` on `--surface-selected`, 12–14 px at 600 — DS 2026's documented pair, AA asked), the labels ahead 5.88 (text-3), behind 6.87 (text-2), the shores 6.87, the dates 5.88, «Étape n sur 7» 6.87, the summary 6.05, the state chip's word **7.23** (COLOUR §10's AAA rule for state words holds), the home's passage labels 13.67–14.11. No rule of the system asks 7 : 1 of the journey's other words: none is a state word or a notice title |
| Non-text contrast (1.4.11) | the nodes on pixels (1440, 2× render): the ink dot behind 15.56 : 1, the current ring 6.05 (5.24 on its wash), the open ring ahead **3.59**; the passage's rings in text-1. The line ahead (`--line-rhythm`) and the threshold's hairline stay under 3 : 1 by design — the decorative hairline of the foundation; the nodes, the glyphs and the words carry what they say |
| Targets (2.5.8; 44 on touch) | «Où j'en suis» 358 × 44 at 390, fr and ar; the Stepper's links 270 × 44 (64 for a two-line question) at 1440 and 44 × 44 on the phone row — where each link's own line covers a 2 px strip of it (finding 3; a 24 × 24 live square remains); 0 targets under 24 px without the spacing exception, journey or not |
| Arabic | the level line mirrored («المغرب» at the reading start, the line right to left, the thresholds' captions on the mirrored side), the spine on the right, the Stepper's phone row from the right; the dates and the passage's 01–04 not mirrored; **no Arabic text under 14 px** |
| Reduced motion — a real still | `emulateMedia({reducedMotion: "reduce"})`: 0 animations at load, at + 1 s, after the fold opens, after a Stepper link, after two Tabs (32 loads); every journey transition computes to 0 s. With motion allowed: **0 transitions and 0 animations in the first 2.5 s** of every journey page, branch (28 loads) and merge base (16) alike — the probe's positive control, the HealthStrip's `strip-fill`, caught at 86 ms on `qa-person`'s case file (W3-C / W3-E's) |
| Forced colours | system colours only: the lines GrayText (travelled CanvasText), the dots CanvasText, the current ring Highlight on Canvas, the wash dropped, «Vous êtes ici» a CanvasText-edged pill; the passage's rings CanvasText, the current one Highlight. Usable at 1440 and 390, closed and opened (`forced/`, `extra/spine-*-forced.png`) |
| 400 % reflow (320 × 640) | 0 horizontal overflow, 0 clipped text, 0 overlapping or escaping runs, closed and opened, fr and ar |
| Text spacing (1.4.12) | 0 overflow at 1440, 1280, 1024 and 390; no journey text clipped (the one clipped run is the rail's account name, W3-A's ellipsis, before and after). At 1024 and 1280 (fr) «Accompagnement et inclusion» then runs 15–24 px past the list's box into the gutter: drawn whole — no clipping ancestor, no page overflow, no overlap (`extra/spacing-fr-1024.png`). No loss of content |
| The opened spine | the current node's ring and its 32 px wash are whole on the page at 390, fr and ar, normal and forced (no clipping ancestor; the region crops cut them only at the element's box — `extra/spine-*.png`); 320 has the same 16 px gutter for its 6 px of wash |

## Performance

**CSS and JS** — gzip −9 (mtime 0) of the committed bundles, the merge base against the branch; the ceilings are
DL54-87's (V5.8: hard):

| Bundle | `d40f209` | `v54-w3-d` | Δ |
|---|---|---|---|
| `dist/main.css` (every page) | 41 880 | 40 599 | **−1 281** |
| `dist/portal/console.css` | 7 072 | 8 956 | +1 884 |
| `dist/portal/portal.css` | 1 975 | 1 975 | 0 |
| `dist/pages/css/pages.css` (the home) | 4 083 | 4 497 | +414 |
| `dist/situation.js` («Ma situation») | 1 137 | 1 206 | +69 |
| every other JS bundle | — | — | 0 raw (rebuilt: new chunk names; ±2 B gzip) |

| Page type | `d40f209` | `v54-w3-d` | Ceiling | |
|---|---|---|---|---|
| console pages (main + console + portal) | 50 927 | **51 530** | 50 927 | **+603 over** (finding 1) |
| the home (main + pages + hero) | 56 531 | 55 664 | 57 191 | 1 527 under |
| a public interior page (main) | 41 880 | 40 599 | 42 531 | 1 932 under |
| `dist/main.css` | 41 880 | 40 599 | 46 080 | 5 481 under |

**Requests** before `load`: CSS 3, JS 7 on the dashboard and the case file, 3 + 8 on «Ma situation» — unchanged, and
under W1-0's before set (3 + 8; 3 + 9). No new module: there is no `journey-rail.js`.

**What the journey costs a load, isolated in the page.** In one loaded page the journey's region is taken out
(`display: none` through the CSSOM) and put back, and the forced style + layout of putting it back is timed: 25
repetitions, the median, on each tree, 1440 (`relayout-*.json`):

| Region | V4 at `d40f209` — × 1 / × 4 | W3-D — × 1 / × 4 | elements |
|---|---|---|---|
| the dashboard's «Mon parcours», threshold A — fr | 0.6 / 5.2 ms | 1.3 / 13.9 ms | 30 → 75 |
| the same — ar | 1.2 / 8.4 | 1.6 / 11.4 | |
| the dashboard, step 1 — fr | 0.7 / 5.5 | 1.4 / 12.2 | 30 → 75 |
| the same — ar | 0.8 / 6.2 | 2.0 / 13.7 | |
| the case file (journey + timeline) — fr | 2.1 / 16.1 | 3.3 / 23.7 | 135 → 177 |
| the same — ar | 2.3 / 18.9 | 4.6 / 37.6 | |
| «Ma situation»'s Stepper — fr | 0.6 / 3.7 | 0.6 / 4.7 | 35 → 35 |
| the same — ar | 0.8 / 7.4 | 0.8 / 7.0 | |

The level line, the spine and the timeline add **0.4–2.3 ms at × 1** (3–19 ms at × 4) to the page's style and layout;
the Stepper nothing. That is the whole of the journey's load cost: no script, no observer, no animation (traced
below), inside PFR's resolution of the first-render task (+30 ms) at × 4.

**Cold loads before / after** (W1-0's `trace.py` protocol on the lane: CPU × 4, no network throttling, the dev server's
uncompressed CSS, a fresh profile and the cache disabled per load, interleaved in blocks — BASE then HEAD, HEAD then
BASE …, each after a warm-up — medians; the block columns give HEAD − BASE inside each block):

| Cell | n | first-render task | LCP (blocks) | LCP element | CLS max |
|---|---|---|---|---|---|
| dashboard, threshold A — fr 1440 | 5 / 5 | 24.5 → 32.4 | 744 → 976 (−8, +296) | `p.db-empty` both | 0.0255 → 0 |
| the same — ar 1440 | 5 / 5 | 23.5 → 95.0 | 696 → 1 152 (+256, +412) | `p.db-empty` both | 0 → 0 |
| the same — fr 412 | 5 / 5 | 35.6 → 41.5 | 584 → 784 (+200, +82) | `h2#db-now-title` both | 0 → 0 |
| dashboard, step 1 — fr 412 | 5 / 5 | 31.9 → 38.6 | 760 → 756 (+80, −8) | `h2#db-now-title` both | 0 → 0 |
| case file — fr 1440 | 5 / 5 | 34.3 → 26.0 | 612 → 720 (+112, −72) | `p.empty` → `span.ctx__resp` | 0.0005 → 0.0004 |
| case file — fr 412 | 5 / 5 | 44.0 → 38.4 | 724 → 728 (+4, −124) | `p.panel__text` → `span.ctx__resp` | 0 → 0 |
| «Ma situation» — fr 1440 | 5 / 5 | 27.5 → 32.9 | 564 → 700 (+144, +160) | `p.ws-head__lead` both | 0 → 0 |
| «Ma situation» — fr 412 | 5 / 5 | 42.4 → 39.7 | 656 → 596 (−60, −70) | `p.ws-head__lead` both | 0.0054 → 0.0054 |
| the home — fr 1440 | 9 / 9 | 25.8 → 31.4 | 740 → 976 (+36, −12, +220) | the door's image both | 0 → 0.0016 |
| the home — fr 412 | 9 / 9 | 87.4 → 41.2 | 756 → 784 (+212, −128, +64) | the door's image both | 0 → 0 |
| the home — ar 412 | 9 / 9 | 45.5 → 39.2 | 832 → 920 (+104, +144, −180) | the door's image both | 0 → 0 |

These figures are bound by the machine, not by the branch, and are not read as a regression:
- **The machine's speed moved by up to 2.2× between loads** (other lanes share it): the stylesheet parse — the same
  work on both trees, ±1.2 % of CSS — took 11.6–25.0 ms across the saved traces, 28.8 ms in the Arabic dashboard's
  HEAD trace against 12.9 ms in its BASE trace. Normalized by it, that load's layout is the base's (layout ÷ parse
  13.70 against 13.51), and the dashboards' layouts sit within −6 to +14 % of the base's — the journey's 45 extra
  elements, as the isolated measure says.
- **Block differences change sign** in seven of the eleven cells; «Ma situation»'s +136 ms comes with an identical DOM
  (605 elements) and an identical Stepper cost; the home loses CSS (867 B gzip, 7.9 KB raw) and four elements.
- **The Arabic dashboard's first-render task** (95 ms against 23.5) comes from the loads in which the first paint holds
  the whole document's layout — 35–65 ms of layout on either tree: 3 of 5 HEAD loads here, and the cut first sitting
  caught one on the merge base (`runs-console.jsonl`, BASE ar r4: 88.9 ms, 47.3 ms of layout).
- **LCP elements**: the same on every cell but the case file, where the empty-state paragraph that was the largest
  text now sits below the first viewport under the taller dated spine and the context header's line takes its place
  — earlier on the page, its time no worse within the noise.
- **Against W1-0's «before» set** (V4 on 8782): the requests are fewer (above), the dashboard's LCP element is W3-B's
  NowPanel on both trees, and W3-B measured its dashboard 252–300 ms ahead of V4 on the compressed twin at its merge —
  0.4–2.3 ms of layout at × 1 does not move that. CLS ≤ 0.0054 everywhere (the 0.0054 is «Ma situation» at 412 on
  both trees), far under 0.05.

**Long tasks.** The journey runs no task of its own at load or after it. The one it causes is the person's own tap on
«Où j'en suis» on a phone (finding 2): at CPU × 4, **96 ms (seed-person) and 128 ms (qa-doc-person) of interaction**
(medians of 5), long tasks of 71–174 ms; closing it 40–48 ms, no long task; a tap on the plain h2 beside it 40–48 ms,
no long task (`tap-head.json`). Traced (`tap-trace/head-seed.json`): the open's task, 103–153 ms, is style 77–106 ms
over three recalculations of **282, 282 and 390 elements** — the whole document twice, then with the list — and
layout 11–26 ms; the h2's tap recalculates the same 282 elements once (23–29 ms). Opened by script, with no tap and
no focus change, the toggle costs one recalculation of 390 elements (48–64 ms of task); with the four `html:has(…)`
rules of `main.css` and `console.css` deleted through the CSSOM (a probe, never shipped) the same toggle recalculates
**112 elements** and costs 23–42 ms (`tap-trace/has-head.json`) — the `[open]` attribute invalidates the whole
document through the shell's `html:has(.console-drawer[open])`. The journey's own share of the open is that 23–42 ms at
× 4 (≈ 6–10 ms at × 1). INP stays far under 200 ms; it replaces V4's list laid out at every load.

**At rest — nothing loops.** 5 s windows on the fourteen pages (twice, `rest.json`, `rest-r2.json`), and again after
the phone's fold has opened: 0 style recalculations, 0 layouts, 0 `requestAnimationFrame` or timer calls, 0 running
animations; idle task time ≤ 13 ms in 5 s.

## Findings

1. **Blocking (the merge rule) — the console page types' shared CSS is 603 B over its hard ceiling.** main + console
   + portal = **51 530 B** gzip −9 against **50 927 B** (DL54-87); V5.8 sends a merge that grows a shared bundle back.
   The rail's drawing is the journey's own CSS and three console pages use it (four with the review's M2). *Fix* (the
   review's M1): take `v5/_journey-rail.css` out of `console.css` into a page-only sheet (for instance
   `apps/portal/static/portal/journey.css` → `css/dist/portal/journey.css`) linked in `{% block extra_head %}{{ block.super }}…{% endblock %}` on the
   dashboard, «Ma situation», the case file — and «Mon parcours» with the review's M2. Estimated here by deleting the
   journey's rules from the committed bundle: **the console page types 49 610 B (1 317 under the ceiling)**; the
   journey's pages 49 610 + 2 622 B in four sheets — «plus a page's own sheet», as DL54-87 words it. Requests stay
   within W1-0's count (3 + 7 → 4 + 7 against 3 + 8; «Ma situation» 4 + 8 against 3 + 9). Weigh before → after at the
   merge.
2. **Minor — the phone's «Où j'en suis» costs a 64–153 ms task at CPU × 4 when opened** (INP 96–128 ms), not the
   notes' «≈ 27 ms at × 4» (measured on the lane: style and layout, which compression does not change). Under INP's 200 ms and no regression (V4 laid the list out at every load), and most of it
   is the shell's: the `[open]` toggle recalculates the whole document through `html:has(.console-drawer[open])`, and
   any tap recalculates it once more. *Fix:* the notes say what was measured (their figure is the journey's own share,
   23–42 ms at × 4); the `html:has()` lead goes to W3-A / the W4 performance sweep (O3) — nothing to change in W3-D's
   files.
3. **Minor — the Stepper's line takes the pointer.** `.wstep__item::before` is absolutely positioned, so it paints
   over its own link: on the phone row a tap on the 2 px line just past a node lands on the `li` and does nothing (the
   third question stays unselected — `click-head.json`); at 1440 the same for the 2 px vertical line under a node.
   Each link keeps a live 24 × 24 square (the measured hit from the centre is 32 × 44 on the phone row), so 2.5.8
   holds — it is a dead strip inside a target. *Fix:* `pointer-events: none` on `.journey > li::before,
   .tl__row::before, .wstep__item::before` in `_journey-rail.css` §2 — one declaration.

## Seen on the way — outside this area (for the orchestrator; not counted in the verdict)

- **O1 · W3-E's case file — the inspector scrolls inside itself with nothing focusable in it** (pre-existing: the
  merge base fails the same axe rule). `aside.file-grid__inspector` («Suivi du dossier», `overflow-y: auto` from 80rem
  in `v4/workspace.css`, `templates/cases/detail.html`) outgrows its height with `seed-person`'s twelve events.
  Chromium and Firefox make the scroller focusable — the walk stops on it, its ring visible —, Safari does not: there
  the timeline's latest event (the review's m1) is out of keyboard reach. *Fix:* `tabindex="0"` on the labelled aside,
  or no inner scroll, with m1.
- **O2 · W3-A's shell — under forced colours the current page's entry shows no focus.** `_shell.css`'s forced-colours
  block draws `outline: 2px solid Highlight; outline-offset: -2px` on `.rail__item[aria-current="page"]` and
  `.console-bottom__item[aria-current="page"]` at all times — the same outline as the focus ring: 0 changed pixels
  between focused and unfocused on 22 of the 28 forced-colours walks (the current rail entry at 1440, the current bar
  entry at 390; fr and ar). WCAG 2.4.7 in forced colours. *Fix:* another current marker under forced colours (for
  instance a `border-inline-start` in Highlight) so that focus still adds its outline.
- **O3 · the console's `html:has(.console-drawer[open])` recalculates the whole document on every `[open]` toggle**
  (`console.css`): the journey's disclosure pays 390 elements for its 112 (finding 2), and the shell's own disclosures
  (the language switcher, the Academy, the account) would pay the same. A class set by the drawer's own script would
  take it out (W3-A / W4-B). Separately, any tap in the console recalculates the document once (282 elements, the plain
  h2 included, with or without the `html:has()` rules) — worth a look in the same sweep.

## Not checked

WebKit and Firefox (the review's m6: `::details-content`'s fallback — the card and its disclosure at every width — was
read, not run); a screen reader (the tree read is Chromium's); a real phone; the compressed twin 8782 (the lane's dev
server serves the CSS uncompressed and unthrottled: the before/after is relative, on one server, and its absolute
figures are not W1-0's); SUSPENDED and CLOSED files (none in the lane's data — the review's M3 holds for the
accessibility tree too: `aria-current="step"` would sit on step 1); «Mon parcours» (it draws no journey: the review's
M2); the door pages' passage (W3-F1's merge, the review's M4).

## The lane, cleaned

The five minted sessions revoked on `ile_v5_l6` (`sessions.py revoke`: 5 rows deleted, the cookie file removed);
the server on 8786 stopped; no browser of this role left running and the first sitting's leftover performance profile
deleted; the benchmark lock never created; scratch and evidence outside every repository. This report is the only
file this role wrote in the worktree.
