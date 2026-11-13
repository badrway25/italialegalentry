# W1-B · Icon system — accessibility + performance check (`w1-b-a11y-perf`)

Italy Legal Entry™ design V5 · V5.5 «Delivery mode» (implement → review once → fix → ship) on V5.4 · 9 October 2026,
08:40–09:55 (+02:00) · plan `docs/design-v5/V5_4_EXECUTION_PLAN.md` §1.7, §2.5, §2.6, §3.1 items 6, 8, 9 and 11,
§3.3 item 5 · DL54-20 … DL54-24 · branch `v54-w1-b` at `d9e6b07` (clean; merge-base = design-v5 `db55a67`, which
holds W1-A shipped). I built nothing of W1-B: one pass, as the directive asks.

| | |
|---|---|
| **Verdict** | **SHIP AFTER FIXES — 0 blocking, 0 major, 2 minor (one of them to take or leave).** The icon system introduces no accessibility regression and no performance regression: no health count is worse than the W1-0 before set on 100 cells, every one of the 3 496 icons is decorative and named by its control, 0 unresolved, 0 below its floor, 0 under 3 : 1 on pixels, the RTL flip list holds exactly, reduced motion is a still, forced colours read, and the paired traces at n = 10 on the home show LCP −34 / +32 ms with the first-render task, CLS and the LCP element unchanged. The one thing to fix is the family's own specimen board at phone width (two side-scrolling tables with no keyboard access, and 11 px labels); the other minor is the row menu's `ellipsis-vertical`, which reads lighter than the ink at 1× — the Iconography Director's call. Performance is a PASS on this lane's evidence; the 8782 figure stays the Performance Lead's. |
| **Servers** | The lane's own 8786 (`C:/tmp/ile_wt/v54-w1-b` at `d9e6b07`, `ile_v5_l6`, `ILE_REFERENCE_DATE=2026-10-03`, `DB_CONN_MAX_AGE=0`, `ILE_DESIGN_PREVIEW=1` + `ILE_DESIGN_PREVIEW_PORT=8786` so the board route answers, `--noreload`; the implementer's process, restarted by them on the merged tree — the sprite it serves is the committed one, sha256 `dbbb2fe693ff…`, and its `dist/main.css` is byte-identical to the committed bundle, `46c1dc07f821…`). For attribution and the paired traces, a **before** server I started on 8793 from `C:/tmp/ile_wt/v5-live` (`8d45acd` = tag `v54/w1-a`; the merge-base `db55a67` differs from it in Python, test and two untouched templates only, so its CSS, sprite and call sites are the merge-base product's) with the same clone `ile_v5_l6`, the same date, `DB_CONN_MAX_AGE=0`, the same preview flag (so the cookie names agree), `PGAPPNAME=ile-lane-6-before`, `--noreload`; stopped at the end. |
| **Browser** | Playwright 1.63, headless Chromium, a fresh profile per cell under `C:/tmp/ile_v5_council/.profiles/w1-b-a11y-perf/` (deleted after). Phones emulated (mobile + touch). No screen reader, no WebKit or Firefox, no real device. I did not load 8780, 8770–8772, 8782, the other lanes, nor Chrome 9222 / 9223. |
| **Lock** | Every cell of every series waited while `C:/tmp/ile_locks/PERFORMANCE_BENCHMARK_LOCK` existed. The lock was mine for the trace windows — AB1 08:58:49–09:09:57 (held 11.1 min, 56 loads), LAB1 09:37:39–09:39:51 (held 2.0 min, 12 lab loads) and AB3 09:40:09–09:45:36 (held 5.5 min, 24 loads; the label skips AB2 because the lab window is the second entry of `windows.jsonl`) — each with the 60 s settle, the machine load sampled, the lock deleted in `finally`. |
| **Writes** | Four sessions minted with `Client.force_login` on `ile_v5_l6` (`qa-doc-person`, `qa-person`, `qa-fresh-person`, `qa-company`) by `C:/tmp/ile_v5_council/.work/w1-b/w1-b-a11y-perf/mint_sessions_w1b_a11y.py` — outside every repository; no password used, typed or stored — writing what a sign-in writes (a session row, `last_login`, an `auth.login` audit row); revoked at the end, the cookie file removed. No other POST. Nothing in the worktree except this file. |
| **Evidence** | `C:/tmp/ile_v5_council/evidence/v54/w1-b/a11y-perf/` (E/ below): `runs/*.jsonl` (one record per cell), `shots/<mode>/`, `shots/icons-<server>/`, `crops/`, `perf/` (traces, runs, `summary.json`, `lab/`), `summary-*.json|txt`, `logs/`, `PAGE_TYPES.json` (the W1-0 inventory + the specimen board). Tools in `C:/tmp/ile_v5_council/.work/w1-b/w1-b-a11y-perf/tools/`: W1-A's instruments unchanged but for the constants (`a11y_probe.py`, `health.js`, `ab_trace.py` on W1-0's `trace.py` / `analyse.py` / `an_pfr.py`, `perf_compare.py`, `summarise_a11y.py`) and this family's own: `icon_probe.py` (every sprite icon of every cell, on pixels, on both servers), `icon_summary.py`, `bytes_compare.py`, `lab_sprite.py` (the sprite's main-thread cost in isolation). |

---

## 0. In short

**What holds, measured (every figure below is from this pass, on the lane):**
- **No count worse than the W1-0 before set on any of the 100 product cells** (25 page types × fr, ar × 1440 and 390):
  overflow, clipped text, overlapping targets, targets under 24 px, missing focus indicators, axe nodes, axe contrast
  failures — none rose; several fell (targets under 24 px 102 → 52, axe nodes 4 → 2) for W1-A's reasons, not this
  family's.
- **Keyboard walk, fr and ar, 1440 and 390:** 3 328 real-Tab stops, **0 without a visible indicator**, 3 096 rings
  measured on pixels. No icon is in the tab order: every one of the 3 496 `<svg>` in the 100 cells' DOM carries
  `aria-hidden="true" focusable="false"`, none a `tabindex`, and every control that holds an icon has a text or
  visually-hidden name (0 unnamed, before and after). The stops that end under a pinned layer (15 partly, 11 entirely)
  and the ring under 3 : 1 (the skip link, W1-A's open m1; three textareas of the companies' needs form, W1-C's field
  ring) are V4's and W1-A's, identical on the before server.
- **Names and roles:** axe-core 4.13 (WCAG 2.0–2.2 A/AA) 2 violation nodes on the 100 product cells against 4 in the
  before set on the same cells (the login's reset link `target-size`, fr only); 0 `color-contrast`. On the family's
  specimen board at 390 px axe adds `scrollable-region-focusable` × 2 (fr and ar): the board's two side-scrolling
  tables cannot be reached by keyboard — **m1**, the one thing W1-B must fix.
- **Contrast on pixels — text:** 11 454 visible text nodes, 2 763 distinct pairs, read against the dominant pixel colour
  of each line box. Every pair ≥ 4.5 : 1 except one sample of the open-navbar cell — the hero's display title «ITALY
  LEGAL» read against the open panel's white (1.13: the panel overlaps the title's line box; the title is near-white on
  the night stage and the before server returns the same sample) — a sampling edge, not a defect. Lowest held: 4.61
  («Mes pièces», as W1-A), 4.73 (the board's `nullo` label on night), 4.92 (the lock-up's «Italy» on glass). The system
  demands 7 : 1 nowhere; 1 006 pairs under 16 px sit between 4.5 and 7 : 1 (information).
- **Contrast on pixels — icons (the family's own measure):** 1 062 visible icons sampled in their own boxes, **0 under
  3 : 1**; the lowest 4.14 : 1 (the hero legend's four audience glyphs at the rows' rest opacity on the night stage,
  W2-D's hero) and 4.38 at 1440, then 5.14 (the empty states' glyph), 5.29 (a white arrow on the flat primary), 5.5–15.6
  everywhere else. 10 «not painted» readings are the instrument's threshold on `ellipsis-vertical`'s three small dots,
  which the crop shows painted (`E/crops/documents-fr-1440-ellipsis-x3.png`).
- **The icons as drawn:** 1 260 visible icons, **0 unresolved `<use>`**, **0 below its registry floor**; the stroke is
  1.5 px on 1 212 of them, 1.67 px on the 12 `icon--xl` marks and 1.25 px on the 36 empty-state glyphs (1.25 px before
  W1-B too: a 24 px drawing inside a 48 px padded box — DL54-20's «2.1 px before» holds only where `components.css`'s
  40 px rule wins, nowhere in this set). Before W1-B the same sites drew 0.88 px (14 px icons), 1.0 px (16 px), 1.25 px
  (20 px), 1.5 px (24 px) and 2.08 px (the 40 px marks): one hand now, as the plan's table asks.
- **RTL:** on the 50 Arabic cells the flip class sits on exactly the `FLIP_RTL` symbols (0 mismatches on 1 748 icons),
  every flip-class icon is mirrored (`matrix(-1, …)`), no other icon is (the open navbar's disclosure chevron turns 180°,
  a rotation, on both servers), the key, the steps and the mark never are; in French nothing is mirrored.
- **Reduced motion is a real still:** 36 cells (9 page types × fr, ar × 1440, 390) — 0 running animations, 0 infinite,
  `--motion-fast` = `0ms`, two stills 1 s apart differ by **0 pixels** on every cell. (In the normal mode the home runs
  the V4 hero's 4 infinite route animations at rest, before and after alike — W2-D's, not this family's.)
- **Forced colours usable:** 36 cells; the stills of the home (1440, 390) and «Mes pièces» (390) show the key, the
  audience glyphs, the status marks, the actor discs and the bottom bar's glyphs in the system palette (`currentcolor`
  strokes follow the forced text colour; the 12 % tone fills fade). Focus is the system `Highlight` on every stop but the
  bottom bar's current item (6 stops, W3-A's n3 of W1-A's pass), 14.6–19.7 : 1 at 1440.
- **Reflow at 320 × 640:** 52 cells (26 page types × fr, ar): horizontal overflow on **one** cell — the terms-pending dashboard, fr, where V4's console bottom bar runs 9 px past the viewport, identically on the before server (W3-A); the clipped text is the console bar's title ellipsis and the bottom bar's line-clamped labels (W3-A), as at 390; targets under 24 px 0; the board's tables scroll inside their wrappers without a page overflow. The icons, fixed-size and `flex: none`, reflow nothing.
- **Targets:** under 24 px 52 on the 100 cells (102 before: V4's console breadcrumb and bar links at 1440, W3-A); under
  44 px on a coarse pointer: the account menu's 222 × 36 rows (W2-A), the password toggle (W1-C), the honeypot — all
  pre-existing; no icon-bearing control under 24 px. The icons change no target.
- **Health:** 0 CSP violations on 104 + 36 + 36 + 52 cells (the policy is the strict one on every page, the board
  included: `script-src 'self'; style-src 'self'`; the board carries 0 inline style or script); 0 console errors besides
  the 404 page's own «Failed to load resource»; the sprite is fetched once per page.
- **Performance:** **no regression.** Paired cold loads on the lane (profile A, CPU ×4; `E/perf/compare.txt`): with the two home cells at n = 10 per server, LCP −34 / +32 ms (fr 1440 / ar 412), the first-render task −8.5 / +16 ms, FCP, the longest task, the long-task count and CLS (≤ 0.015) unchanged, the LCP element the same on every cell; the five other cells at n = 4 sit inside their spreads (the one +248 ms, the Arabic dashboard, pairs a 69 % busy load with a 24 % one and is repeated by neither FCP nor the first-render task). AB1's +100…+150 ms on the home (3 of 4 pairs, the machine at 60 %) vanished in the quiet window AB3 (pairwise medians −36 / +18 ms at 25–33 %). The lab isolation shows the 114-symbol sprite costs the main thread nothing measurable against the 36-symbol one (238 vs 247 ms of work in the 1.5 s after its arrival at CPU ×4; Layout 94 vs 92, Paint 33 vs 35, ParseHTML 18 vs 21 ms). Bytes: `main.css` +73 B gzip, every page type 1 722 B under its Wave-1 allowance, JS and page sheets identical; the sprite 6 130 → 31 963 B raw — one request, fetched after the stylesheets, +4.7 KB gzip on the compressed twin (+25.8 KB raw on this lane, which serves static files raw: its download grew from ≈ 200 to ≈ 330 ms at 1.6 Mbps without moving FCP or LCP). Nothing loops: 0 animations added; the home's 4 infinite V4 hero routes run before and after alike.

**What is W1-B's to fix:**
- **m1 — the specimen board at phone width (`templates/dev/designpreview/specimens/icons.html`, `static/css/dev/specimen-icons.css`):** at 390 px the audience table's wrapper `.sp-scroll` and the journey line `.sp-line` scroll sideways and cannot be reached or scrolled from the keyboard (axe `scrollable-region-focusable`, WCAG 2.1.1; fr and ar). Fix: `tabindex="0" role="region" aria-labelledby="<the section's h2 id>"` on each scrolling wrapper, or let the rows wrap below 48 rem. In the same pass: the `code` ids and the `th` size labels are 11 px (`.sp-table code`, `.sp-table th`), under the 12 px Latin floor of plan §1.1 that W1-A's check measures on every page — 12 px (`--font-size-caption`). Dev-only, inside the family's slice, ten minutes.
- **m2 — the row menu's mark, to take or leave (`static/icons/src/ellipsis-vertical.svg`):** Lucide's three stroked circles of radius 1 render at 20 px as three dots whose anti-aliased ink is lighter than `currentcolor` (the instrument read them as unpainted; the ×3 crop shows three faint dots). The button keeps its name («Ouvrir le menu de la pièce») and its ≥ 44 px box, so nothing fails; filled dots (`fill="currentColor"`, which the build already allows for the tone fills) would read as the ⋮ everyone knows at every size. The Iconography Director's call, judged on the chip board with W1-C if preferred.

---

## 1. Protocol

- **Cells.** 26 page types — every template family the icon diff touched, plus the specimen board: home, the open
  navbar, the four doors (persons, companies, institutions, universities), AGAMI, the anti-fraud page, a pathway page,
  «Vivre en Italie» (index and a topic), contact, the login, the 404 (`/_errors/404/`, the product's own page: the lane
  runs `DEBUG`), the person dashboard (full, empty, terms pending), «Mes pièces», the deadlines, the requests, the
  messages, «Mon parcours», the case file, the profile, the company dashboard, and `/__design-v5/specimens/icons/` —
  × fr, ar × 1440 × 900, 390 × 844 = **104 cells** for the main pass. Modes: reduced motion and forced colours on 9
  page types (the seven flagships the diff touches + the anti-fraud page and the deadlines: 36 cells each); 320 × 640
  on all 26 (52 cells). The icon probe on the same 100 product cells, on both servers (200 cells).
- **The W1-0 instrument, unchanged** (`health.js`, W1-A's `a11y_probe.py`): overflow, clipped text, overlapping
  targets, targets under 24 px (under 44 on a coarse pointer), axe-core 4.13.0 WCAG 2.0–2.2 A/AA, the real-Tab focus walk
  with the ring measured on pixels, obscuring by pinned layers, text contrast on pixels (the computed colour against the
  dominant pixel colour of each line box; 4.5 : 1 for every text, DS 2026 §4.4). Compared cell by cell with the W1-0
  before set (`MANIFEST.json → summary_by_page_type`), as W1-A's check was.
- **This family's instrument** (`icon_probe.py`): every `<svg>` whose child is a `<use>` — the symbol id, the rendered
  box against the registry floor (`apps/core/icons.py MIN_SIZE`, read as pure Python from the worktree), the computed
  stroke (CSS px under `vector-effect: non-scaling-stroke`; units × size / 24 on the scaling V4 sprite), the transform
  (the RTL flip against `FLIP_RTL`), `aria-hidden` / `role` / `aria-label` / `focusable` / `tabindex`, the nearest
  interactive ancestor and its accessible name (text, `aria-label`, `title`; visually-hidden text included), `<use>`
  resolution (`getBBox`), occlusion; and on pixels, for every visible icon of the first screens, the effective colour
  (alpha and cumulative opacity blended) against the dominant colour of the icon's own box (the ground it sits on: a
  disc, a chip, a glass band, the night stage) and whether pixels near that colour were painted at all. The «worst»
  colour of an icon's box is its own anti-aliasing and is not read as a ground. Animations running at rest and
  `will-change` on every cell (anything looping).
- **Attribution.** The same probes on the before server 8793 (the merge-base product with the V4 sprite): the icon probe
  on every cell (a per-call-site before/after table: id, size, stroke, contrast); the health probe on
  the open navbar, the pathway page, the deadlines, «Mes pièces» and the company dashboard (fr, 1440 + 390) and the terms-pending dashboard at 320 px — the cells where a count or a sample asked for it.
- **Static checks** (no browser): the sprite's XML (`xml.etree`), the registry imported as pure Python, the alias
  symbols against their targets, the bundles' bytes (`gzip -9`), the CSP header of the home and the board,
  `scripts/build_icons.py --check`.
- **Performance.** `ab_trace.py` = W1-0's `trace.py` on both servers alternately (before, after, before, …; the order
  reversed every run): the W1-0 flagship cells the diff touches — home fr 1440, home ar 412, login fr 1440, the person
  dashboard fr 1440 and ar 412, «Mes pièces» fr 1440 and ar 412 — n = 4 per server in AB1, then n = 6 more per server on the two home cells in the quiet window AB3 (n = 10 in all), profile A (150 ms RTT,
  1.6 Mbps / 750 kbps), CPU ×4, cache disabled, a fresh profile per load; LCP, FCP, CLS, the first-render task, the
  longest load task, the load tasks > 50 ms, TBT, the INP proxy, the bytes per kind. Then `lab_sprite.py`: the sprite's
  main-thread cost in isolation — one synthetic page per sprite on the lane's own origin (fulfilled by Playwright's
  route, so no network enters the comparison), 53 `<use>` with the home's symbols, the sprite itself fulfilled from
  memory, CPU ×4, the main-thread task time in the 1.5 s after the sprite's `responseEnd`. **The absolute numbers are
  not the 8782 numbers** (the dev server serves static files raw — the V5 sprite is 31 963 B on the wire here and
  6 412 B gzip on the twin — with `DEBUG` on; the machine carried the other families' lanes and my own paused browsers):
  what is read is after − before on the same lane at the same minute, with the W1-0 8782 medians beside them for scale.
  The plan's PASS on 8782 (n ≥ 9, under the lock, by the Performance Lead) is not replaced by this check.

## 2. Accessibility — the measurements

### 2.1 Keyboard and focus (2.1.1, 2.4.7, 2.4.11, 1.4.11)

| Series | Cells | Tab stops | Without indicator | Rings measured on pixels | Ring < 3 : 1 against the ground | Partly / entirely under a pinned layer | Out of the viewport |
|---|---|---|---|---|---|---|---|
| main (fr + ar, 1440 + 390) | 100 product cells | 3 328 | **0** | 3 096 | 64 — the skip link on every cell the walk reached it (laguna-400 on paper, 1.45–1.59 : 1 against the page, 8.73 against its own box: W1-A's m1, still open on this tree) and the three textareas of the companies' needs form (W1-C's field ring) | 15 / 11 — V4's fixed console bottom bar at 390 (the deadlines' footer links, «Tous mes besoins», «Voir le détail de la pré-évaluation», «Remplacer la pièce», «Commencer l'orientation») and the pathway page's sticky section nav at 1440 («Tous les parcours réguliers»): W1-A's n1 / n2, the same stops on the before server | 0 |
| forced colours (9 page types) | 36 | 982 | 6 — the bottom bar's **current** item (case file, dashboard, «Mes pièces» at 390, fr + ar), which already carries the inset `Highlight` outline before focus (W3-A; the before set found the same) | 914 | 0 (14.6–19.7 : 1 at 1440) | the same stops | 0 |
| the specimen board | 4 | 0 at 1440, 2 at 390 | 0 | — | — | — | 0 |

The 24 «not painted» readings of the main series are the hero legend's four rows at 1440 (the row grows on focus and the
sample read the old box — W1-A's finding, the ring is there in `E/shots`) and the eight stops that end under the bottom
bar. No icon is a stop: of the 3 496 `<svg>` in the 100 cells' DOM, 3 496 carry `aria-hidden="true" focusable="false"`,
0 a `tabindex`, 0 a `role` (no call site passes the tag a label, so every icon is decorative and its control carries the
name: `doc-row__more` «Ouvrir le menu de la pièce», `nav-toggle` «Menu», the rail items, the bottom bar's items — 0
unnamed controls among the icon-bearing ones, before and after).

### 2.2 Names and roles (axe-core 4.13.0, WCAG 2.0–2.2 A/AA)

| | Now (100 product cells) | Before set (same cells) | The board (4 cells) |
|---|---|---|---|
| violation nodes | 2 | 4 | 4 |
| `target-size` | 2 — the login's «Mot de passe oublié ?» (fr × 2; W2-B) | 4 (fr + ar × 2) | 0 |
| `scrollable-region-focusable` | 0 | 0 | **4** — `.sp-scroll` (the audience table's wrapper) and `.sp-line` (the journey line) at 390, fr and ar: side-scrolling regions with no keyboard access (**m1**) |
| `color-contrast` | 0 | 0 | 0 |
| any other rule | 0 | 0 | 0 |

### 2.3 Contrast on pixels (1.4.3, 1.4.11)

**Text.** 11 454 text nodes · 2 763 distinct (fg, bg, size, weight) pairs · 104 cells · 4–5 screens a page. Pairs under
4.5 : 1: one — the open-navbar cell's hero display title «ITALY LEGAL» (64 px, `#eef1f6`) read against `#ffffff`, the
mega-menu panel that overlaps the title's line box when the first door is open (the title sits on the night stage;
the before server returns the same sample, 1.13 on the same box) — a sampling edge, not a defect. Lowest held pairs: 4.61 («Mes pièces»), 4.73 (the board's `nullo`
label on its night panel), 4.92 (`#157a3c` «Italy» on the glass), 5.14 (`--text-3` on carta-100), 5.29 (white on the
flat primary). 15 textured samples (the hairline under a link, a bar label over its icon) are the ground's texture, as
in W1-A's pass. Families seen on pixels: Host Grotesk, ILE Wordmark, ILE Mono, Vazirmatn.

**Icons** (`E/summary-icons.json`, `E/runs/icons-after.jsonl`). 1 062 visible icons sampled in their own boxes over the
100 cells (the rest sit below the sampled screens, inside closed menus, or under a pinned layer at the sample's
moment). Primary ratio — the effective ink against the dominant colour of the icon's box:

| Where | Ink → ground | Ratio |
|---|---|---|
| the hero legend's four audience glyphs at rest (the rows are dimmed until hover; W2-D) | `#75849a` → `#10233f` (390) · `#738094` → `#0a1932` (1440) | **4.14** · 4.38 |
| the empty states' glyph (`--ink-3` on `--min-1`) | `#55646b` → `#ecebe6` | 5.14 |
| the arrow inside a primary button | `#ffffff` → `#12777f` | 5.29 |
| the page-links, meta rows, the console bar | `#55646b` → `#f4f3f0` | 5.53 |
| `link-arrow` arrows | `#0f6a72` → `#f4f3f0` / `#ecebe6` | 5.69 / 5.29 |
| the actor discs (`glyph__icon`, 16 px in the 24 px disc) | `#4a5a62` → `#ecebe6` | 6.0 |
| the rail (`rail__glyph`, night) | `#b9c5d6` → `#0b1a33` | 9.9 |
| the anti-fraud `shield-alert` marks, the nav toggles | `#0f2547` → `#ecebe6`, `#15222a` → `#fbfaf8` | 12.8–15.6 |

0 under 3 : 1 on either server (the V4 strokes read the same inks). 10 «not painted» readings — `ellipsis-vertical`
on the three document rows of «Mes pièces» (fr + ar × 1440 + 390): the symbol is three stroked circles of 1 unit
whose anti-aliased dots are lighter than the ink; the ×3 crop shows them painted (`E/crops/documents-fr-1440-ellipsis-x3.png`).

### 2.4 Reduced motion (2.3.3, the standing rule)

36 cells: running animations 0, infinite 0, `--motion-fast` = `0ms`, stills 1 s apart identical (0 differing pixels)
on all 36 (`E/summary-reduced-motion.json`, `E/shots/reduced-motion/`). `will-change` at rest: 1 element on the home,
the open navbar, the login and the anti-fraud page at 1440 (the V4 door stage, W2-D) — plan §2.6 asks for 0; not this
family's. The icons add no animation and no transition: `document.getAnimations()` on the 100 cells in the normal mode
reports the same 5 running (4 infinite) on the home and the open navbar before and after (the V4 hero's routes), 0
elsewhere.

### 2.5 Forced colours

36 cells, stills in `E/shots/forced-colors/`. Read by eye: the home at 1440 and 390, «Mes pièces» at 390. The icons
keep their drawing in the forced palette — `stroke: currentcolor` follows the forced text or link colour (the key beside
«Espace réservé» in `LinkText`, the audience glyphs beside their labels, the document and actor discs, the status marks
of the chips, the bottom bar's glyphs); the 12 % tone fills (`fill: currentColor; fill-opacity: .12`) fade into a faint
tint and nothing rests on them. Focus is the system `Highlight` on every stop but the bottom bar's current item (§2.1).
The sampler's «not painted» counts in this mode are its own limitation (it compares the alpha-blended pixel with the
unblended computed colour), as W1-A recorded.

### 2.6 Reflow (1.4.10)

**320 × 640, 52 cells** (`E/runs/a11y-none-320.jsonl`, `E/summary-320.txt`): horizontal overflow on one cell — `dashboard-person-terms-pending` fr, `nav.console-bottom` and its «Menu» item 9 px past the viewport; the same 9 px on the before server (`E/runs/a11y-none-before320.jsonl`), so V4's bottom bar (W3-A), not the icons (its glyphs are 20 px on both servers). None on the other 25 page types, the board included. Clipped at 320: the console bar's title ellipsis on every console page (fr + ar) and the bottom bar's line-clamped labels in French (W3-A, as at 390). Targets under 24 px: 0. 0 CSP violations; the 404's own console line only.

Text spacing (1.4.12) was not re-run: W1-B changes no text metric; W1-A's pass measured it on the same type system.

### 2.7 Targets (2.5.8, SP-8)

Under 24 px (fine pointer, 1440 + 390): 52 on the 100 cells against 102 before on the same cells — V4's console
breadcrumb links and `a.console-bar__link` at 1440 (W3-A), unchanged or lower per cell. Under 44 px under a coarse
pointer (390): `button.account-menu__link` 222 × 36 (W2-A), `button.form-field__toggle` (W1-C), the honeypot field. No
icon changes a target's box; the row menu's button (`doc-row__more`) and the nav toggles are not in either list.

## 3. The icons themselves — what the family's instrument found (`E/summary-icons.txt`)

- **The sprite, statically.** 114 symbols (109 + the 5 aliases of DL54-21), 31 963 B raw — 805 B under the 32 768 B
  ceiling — 6 412 B `gzip -9`; every symbol `viewBox="0 0 24 24"`, no width or height; 111 stroked shapes, **111** with
  `vector-effect="non-scaling-stroke"`; 49 tone fills, all `currentColor` (`.12` on 31 concept symbols, plain on the
  settled status discs); 0 `style` attributes, 0 hex colours; the root `aria-hidden="true" focusable="false"`. The
  registry's 109 symbols are the sprite's minus the aliases; each alias draws its target's geometry
  (`globe → languages`, `home → layout-dashboard`, `list → send`, `user → person`, `key → ile-key`) and the tag never
  emits an alias id. `FLIP_RTL` has seven members; the floors are 14 px (78 symbols), 16 (22) and 20 (9).
  `scripts/build_icons.py --check`: current.
- **Resolution and floors.** 100 cells × 2 servers: 1 260 visible icons after (1 352 before), **0 unresolved `<use>`**
  (every `getBBox` > 0), **0 below its floor**. The sprite is fetched once per page (`?v=dbbb2fe693ff`, 31 963 B on the
  dev server), 0 CSP violations, 0 console errors beyond the 404's own.
- **Sizes by class (after):** `icon` 20 px (284) · 16 (210, sized by component rules) · 14 (28, the utility bar's key
  at its 14 px floor); `icon--sm` 16 (196); `icon--lg` 24 (16); `icon--xl` 32 (12); `glyph__icon` 16 (76) and 20 (4);
  `rail__glyph` 20 (208); `doorway-legend__glyph` 16 (32); `empty-state__icon` 48 (36: the 24 px drawing in its padded
  disc); `doc-row__due-icon` 16 (12); `page-links__icon` 20 (12); `notice__icon` 20 (8).
- **Strokes.** After: 1.5 px × 1 212, 1.67 px × 12 (`icon--xl`), 1.25 px × 36 (`empty-state__icon`). Before, the same
  sites: 0.88 px × 64 (14 px icons), 1.0 px × 502 (16 px), 1.25 px × 682 (20 px), 1.5 px × 56 (24 px), 2.08 px × 12
  (40 px marks), 1.25 px × 36 (the empty states: 1.25 units at 24 px — not DL54-20's «2.1 px before», which only holds
  where `components.css`'s 40 px rule wins; on every page of this set `v4/workspace.css`'s 24 px + 12 px padding wins).
  So W1-B's weight is heavier than V4 at 14–20 px (0.88–1.25 → 1.5 px: better legibility, the plan's table) and lighter
  at 32–40 (2.08 → 1.67). No chip glyph is rendered on any page today (`.chip__g` has no producer), so its 2.6 stays a
  note for W1-C.
- **The per-call-site table** (1 364 matched sites, `E/summary-icons.json → sites`): 374 changed symbol —
  `shield → shield-alert` × 80 (the anti-fraud entries), `mail → at-sign` × 76, `user → circle-user-round` × 42,
  `home → layout-dashboard` × 40, `lock → ile-key` × 38, `list → send` × 18, `menu → ellipsis-vertical` × 12 (the row
  menus), `shield → stamp` × 8 (the authority's disc), `briefcase → factory` × 8 and the pathway set (`id-card`,
  `users`, `store`, `flask-conical`, `split`, `book-open`), `info → circle-help`, `compass → signpost`, `list → book-a`,
  `handshake → badge-dot` (the authorised actor), `calendar → calendar-clock`, `list → ile-steps`, `home → house`;
  48 changed size — the 36 `glyph--sm` discs 14 → 16 px (DL54-24 item 2) and the 12 anti-fraud marks 40 → 32 px
  (`icon--xl` on the scale); 104 removed — the ecosystem enumerations' bullets (`check` × 28, `institution` × 24,
  `university` × 12) and the living index's ten topic-card icons (× 4 cells), now typographic; 12 added — a `calendar`
  on the compact document rows whose due date carried no urgency glyph before (`DUE[""]`).
- **RTL, Arabic cells (50 × 2 servers):** flip class ⇔ `FLIP_RTL` on all 1 748 icons (0 mismatches); every flip-class
  icon mirrored (`matrix(-1, 0, 0, 1, …)`): the arrows, `chevron-end`, `send`, `signpost`, `logout`; 0 other icon
  mirrored — the open navbar's disclosure `chevron` reads `matrix(-1, 0, 0, -1, …)`, a 180° turn, on both servers;
  `ile-key` beside «الفضاء الخاص», `ile-steps`, `ile-mark`, the audiences and `arrow-up-right` never carry the class or
  a transform. In French 0 icons are mirrored. (`E/shots/icons-after/home-ar-1440x900.png`: the key keeps its drawing,
  the CTA arrow points inline-end.)
- **A plan deviation to name, not an accessibility defect:** §1.7 says the four audiences are «never below 20 px» and
  «in chrome discs the glyph is drawn at 24 px»; the registry sets their floors at 14 / 14 / 16 / 16 on the measured
  sprite and the implementer raised the `glyph--sm` disc's glyph to 16 px (DL54-24 item 2, the raster measurement in
  E/impl-1/measure). On the pages the audiences appear at 16 px in the hero legend and the actor discs, always beside
  their words (the `glyph.html` contract: «never a glyph alone»), at ≥ 4.14 : 1. The Iconography Director's call, made
  with evidence; the CD may ratify it in DL54.

## 4. Performance

### 4.1 Bytes and requests (the lane; the before set's figures from `MANIFEST.json`; `E/summary-bytes.json`)

| | design-v5 (`db55a67`, = W1-A shipped) | v54-w1-b | Allowance / budget |
|---|---|---|---|
| `dist/main.css` raw · `gzip -9` | 238 800 · 42 623 B | 238 950 · 42 696 B (+150 · +73 B: `components.css` §2) | ≤ 45 KB (46 080 B) ✓ |
| page type totals, gzip (the tool's Python gzip, +68 B on `main.css`) | — | home 45 584 · door 42 764 · interior 42 764 · login 43 972 · dashboard 48 138 · «Mes pièces» 49 309 · case file 48 138 | each ≤ before + 8 KB ✓ — headroom **1 722 B** on every page type (W1-A left ≈ 1.8 KB; W1-B spent 73 B) |
| page sheets, JS | identical (no JS file in the diff; the page sheets' bytes equal) | identical | — |
| CSS + JS requests before `load` | home 10 · door 7 · login 8 · dashboard 11 · «Mes pièces» 12 | equal on every cell | ≤ before ✓ |
| the sprite, raw · gzip | 6 130 · 1 742 B (36 symbols) | **31 963 · 6 412 B** (114 symbols) | ≤ 32 KB raw ✓ (805 B of headroom); ≈ 6 KB gzip as the plan expected |
| the sprite's requests | 1 per page, after the stylesheets | 1 per page, after the stylesheets (starts at ≈ 2.2–2.6 s on the throttled lane, 200 → 330 ms long) | — |
| the document | — | +283 … +690 B raw (the content hash on every `<use>`; the enumerations' glyphs gone) | — |
| fonts, images | unchanged | unchanged (font requests and bytes equal; image requests equal, the sprite counted among them on both) | — |

On the wire the only change is the sprite: +25.8 KB raw on the dev lane, **+4.7 KB gzip on the compressed twin and in
production**, where the plan's figures are measured.

### 4.2 Paired cold loads, before (8793) → after (8786), profile A, CPU ×4

Medians, ms; spread = min–max; long tasks = load-phase tasks > 50 ms (median count); W1-0 = the 8782 before set's medians (LCP / first-render task / long tasks), for scale only. Home cells: n = 10 per server (AB1 4 + AB3 6); the others n = 4 (AB1, the machine at 45–60 %).

| Cell | n | LCP b → a (Δ) | LCP spread b / a | First-render task b → a (Δ) | Longest task b / a | TBT b / a | Long tasks b / a | CLS b / a | INP proxy b / a | LCP element | W1-0 8782 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| home · fr · 1440 | 10 + 10 | 2630 → 2596 (−34) | 2584–2980 / 2524–3120 | 110.1 → 101.6 (−8.5) | 164 / 150 | 137 / 178 | 7.0 / 7.0 | 0.0132 / 0.0148 | 40 / 48 | `image.doorway__img` both | 2064 / 710 / 6 |
| home · ar · 412 | 10 + 10 | 2784 → 2816 (+32) | 2652–3068 / 2604–3132 | 117.5 → 133.8 (+16) | 183 / 197 | 257 / 269 | 5.0 / 6.0 | 0.0000 / 0.0000 | 40 / 40 | `p.hero__body` both | 2328 / 914 / 12 |
| login · fr · 1440 | 4 + 4 | 2594 → 2590 (−4) | 2580–2700 / 2428–2644 | 144.1 → 140.2 (−4) | 157 / 140 | 133 / 73 | 4.5 / 5.0 | 0.0222 / 0.0195 | 52 / 68 | `image.doorway__img` both | 1720 / 397 / 2 |
| dashboard-person · fr · 1440 | 4 + 4 | 2840 → 2756 (−84) | 2508–2976 / 2552–3188 | 62.5 → 70.8 (+8) | 161 / 185 | 161 / 158 | 5.5 / 5.0 | 0.0006 / 0.0006 | 28 / 28 | `p.empty` both | 1604 / 405 / 4 |
| dashboard-person · ar · 412 | 4 + 4 | 2904 → 3152 (+248) | 2780–3224 / 2812–3400 | 45.6 → 55.5 (+10) | 259 / 302 | 231 / 290 | 3.5 / 5.5 | 0.0 / 0.0 | 32 / 40 | `p.panel__title` both | 1740 / 449 / 5 |
| documents · fr · 1440 | 4 + 4 | 2736 → 2664 (−72) | 2460–2944 / 2440–3084 | 60.2 → 67.6 (+7) | 145 / 173 | 198 / 213 | 6.5 / 7.5 | 0.0013 / 0.0003 | 28 / 24 | `p.doc-page__lead` both | 1552 / 354 / 3 |
| documents · ar · 412 | 4 + 4 | 2834 → 2842 (+8) | 2680–2936 / 2804–2924 | 55.2 → 42.5 (−13) | 217 / 175 | 203 / 114 | 5.0 / 3.0 | 0.0 / 0.0 | 28 / 28 | `p.doc-page__lead` both | 1672 / 399 / 3 |

**The quiet window alone (AB3, runs 4–9, the machine at 25–33 %):** home fr 1440 LCP 2616 → 2580 (pairwise after − before per run: +68, −32, −4, −108, −280, −40; median −36), FCP 2416 → 2404, first-render task 110 → 102, long tasks 6.5 / 6.5, CLS 0.007 / 0.015; home ar 412 LCP 2784 → 2774 (pairs +16, +20, +60, +112, −196, −36; median +18), FCP 2614 → 2606, first-render task 122 → 134, long tasks 5 / 4, CLS 0 / 0.

**Reading.** AB1 (the machine at 45–60 %, my own browsers paused on the lock, the other families' lanes running) showed the home +100…+150 ms later in 3 of 4 pairs with FCP unchanged; AB3, taken once every probe had ended, shows no such thing (−36 / +18 ms pairwise, inside the plan's 50 ms resolution), and the first-render task — the stable metric — moves by less than ±16 ms on every cell. The Arabic dashboard's +248 ms is one pair at 69 % busy against 24 % (its FCP and first-render task do not repeat it); «Mes pièces» ar 412 and dashboard fr 1440 move the other way by as much. The long-task counts rise by 0.5–2 on four cells and fall on two: with the V4 hero's routes animating through the load phase at CPU ×4, a half-task is noise. The mechanism that could have mattered is visible in the resource timings: the sprite is fetched after the stylesheets (home fr 1440: 2 288–2 492 ms before, 2 280–2 622 ms after; 6 130 vs 31 963 B on this raw-serving lane), overlapping neither the doorway image (done at ≈ 1.25 s) nor the first paint; its extra ≈ 130 ms of transfer here shrinks to ≈ 25 ms where the sprite is gzip-compressed (8782, production). The LCP element never changes; CLS stays under 0.025 on every load (the plan's flagship ceiling is 0.05).

### 4.3 The sprite's main-thread cost in isolation (`E/perf/lab/`)

Two synthetic pages on the lane's own origin, identical but for the sprite each `<use>` points to — the V4 sprite (6 130 B, 36 symbols, `design-v5:static/img/icons.svg`) and the V5 sprite (31 963 B, 114 symbols) — both fulfilled from memory by Playwright's route, 53 `<use>` with the home's symbols, the `.icon` rule inline, CPU ×4, 6 cold loads each, alternating, inside the LAB1 window (`E/perf/lab/lab-sprite.jsonl`, traces in `E/perf/lab/traces/`). All 53 `<use>` resolved on every load. Main-thread task time in the 1.5 s after the sprite's `responseEnd`: **V4 247 ms (197–299), V5 238 ms (214–270)**; the longest task 82 vs 84 ms; Layout 92 vs 94, UpdateLayoutTree 28 vs 23, Paint 35 vs 33, ParseHTML 21 vs 18 ms; the whole load's tasks 390 vs 372 ms; the first paint after the sprite 75 vs 78 ms. The five-fold bigger sprite document costs the renderer nothing the instrument can see at ×4 throttling: the work is the 53 instantiations, the same on both.

### 4.4 Not measured here

The 8782 PASS of plan §2.6 (n ≥ 9 under a quiet lock, LCP ≤ 2.5 s per page type, the first-render task against the
before set to ± 30 ms, with the sprite gzip-compressed as WhiteNoise serves it) remains the Performance Lead's. No
HTTP/2, no real device, no Safari.

## 5. Findings

| # | Severity | Finding | Where | Before W1-B | Owner · fix |
|---|---|---|---|---|---|
| m1 | minor | The specimen board's two side-scrolling regions at phone width (`.sp-scroll`, `.sp-line`) have no keyboard access — axe `scrollable-region-focusable`, WCAG 2.1.1 — and its `code` / `th` labels are 11 px, under the 12 px Latin floor of plan §1.1 | `/__design-v5/specimens/icons/` at 390 (fr + ar); every width for the labels | the board is new | **W1-B** (`templates/dev/designpreview/specimens/icons.html`, `static/css/dev/specimen-icons.css`): `tabindex="0" role="region" aria-labelledby` on each scroller, or wrap the rows below 48 rem; labels at 12 px |
| m2 | minor, to take or leave | `ellipsis-vertical` (the row menu) renders as three faint anti-aliased dots at 20 px: three stroked circles of radius 1 whose ink reads lighter than `currentcolor` | «Mes pièces», every document row (fr + ar, 1440 + 390) | `menu` (three lines) | **W1-B** (`static/icons/src/ellipsis-vertical.svg`): filled dots `fill="currentColor"`, or keep it — the Iconography Director's call |
| n1 | note (plan deviation, not a defect) | The audiences render at 16 px in the hero legend and the `glyph--sm` actor discs; plan §1.7 says «never below 20 px» and «in chrome discs the glyph is drawn at 24 px»; the registry's floors are 14 / 14 / 16 / 16 on the measured sprite (DL54-24 item 2). Always beside their words, ≥ 4.14 : 1 | home (W2-D's legend), the actor discs | 14 px in the discs | the CD: ratify the measured floors in DL54, or ask W1-B for 20 px discs |
| n2 | note (pre-existing) | The skip link's ring is laguna-400 on the page (1.45–1.59 : 1; 8.73 against its own box) on every cell the walk reaches it | every page | identical | W1-A's m1, still open on `db55a67`: `.skip-link:focus-visible { outline-color: var(--focus-ring); }` |
| n3 | note (pre-existing) | Focus ends under the fixed console bottom bar at 390 (the deadlines' footer links, «Tous mes besoins», «Voir le détail de la pré-évaluation», «Remplacer la pièce», «Commencer l'orientation») and under the pathway page's sticky section nav at 1440; in forced colours the bar's current item shows no change on focus; at 320 the bar runs 9 px past the viewport on the terms-pending dashboard | console pages at 390 / 320; `pathway-detail` at 1440 | identical (before server) | W3-A (`scroll-padding-block-end`, a different current-state mark, the bar's five items at 320), W3-F (the section nav) |
| n4 | note (pre-existing) | The login's reset link (axe `target-size`, fr); the account menu's 222 × 36 rows and the password toggle under a coarse pointer; the companies' needs form's textarea ring; the console breadcrumb and bar links at 20 px; the hero's 4 infinite route animations and 1 `will-change` at rest in the normal mode | listed cells | identical | W2-B · W2-A / W1-C · W1-C · W3-A · W2-D |
| n5 | note (for the record) | `DUE[""]` draws a `calendar` on a compact document row's plain due date that carried no glyph before (12 sites); decorative, aria-hidden, the date beside it — the map's comment («no urgency is a plain date») and its value disagree | the terms-pending dashboard's compact rows | no glyph | W1-B, one word either way; no accessibility effect |

**Not done here:** the 8782 PASS (the Performance Lead's: n ≥ 9, the sprite gzip-compressed, LCP ≤ 2.5 s per page type); Firefox / WebKit; a screen reader; a real device; text spacing (unchanged by this family; W1-A's pass holds).
