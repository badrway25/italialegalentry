# W1-A · Foundation — accessibility + performance check (`w1-a-a11y-perf`)

Italy Legal Entry™ design V5 · V5.5 «Delivery mode» (implement → review once → fix → ship) on V5.4 · 8 October 2026,
19:50–20:50 (+02:00) · plan `docs/design-v5/V5_4_EXECUTION_PLAN.md` §1.1–§1.4, §1.6, §1.8, §2.5, §2.6, §3.1 items 6, 8, 9
and 11, §3.3 item 4 · DL54-01 · branch `v54-w1-a` at `b90479b` (clean; `v54/base` = `f11d131`; design-v5 merged in at
`a346e20`; during the pass HEAD moved to `799fa25` by two commits that add `REVIEW.md` only — no product file changed,
so every measurement below is of HEAD's CSS, fonts and templates). I built nothing of W1-A: one pass, as the directive asks. No git write: this file is left in the family's QA
folder for the merge step to carry.

| | |
|---|---|
| **Verdict** | **SHIP AFTER FIXES — 0 blocking, 0 major, 3 minor.** The foundation introduces no accessibility regression and no performance regression on 76 cells (19 page types × fr, ar × 1440 and 390) compared with the W1-0 «before» set, and the same probe on the v54/base product on the same lane attributes every remaining defect to V4 sheets other families own. Two of the minors are one-line corrections inside W1-A's own slice (m1 the skip link's ring colour, m2 a width guard beside the typed-text rule); m3 is the Arabic font budget on two page types, to take or leave. Performance is better on every paired cell. |
| **Servers** | The lane's own 8783 (`C:/tmp/ile_wt/v54-w1-a` at `b90479b`, `ile_v5_l3`, `ILE_REFERENCE_DATE=2026-10-03`, `DB_CONN_MAX_AGE=0`, `--noreload`, no preview routes); the bundle it serves is byte-identical to the committed `static/css/dist/main.css` (sha256 `df41905a…`, 238 800 B). For attribution and the paired traces, a **before** server I started on 8793 from `C:/tmp/ile_wt/v5-live` (`v54/w1-p` = the v54/base product CSS, fonts and head: only `designpreview.css` differs from `v54/base`) with the same clone `ile_v5_l3`, the same date, `DB_CONN_MAX_AGE=0`, `PGAPPNAME=ile-lane-3-before`, `--noreload`; stopped at the end. |
| **Browser** | Playwright 1.63, headless Chromium, a fresh profile per cell under `C:/tmp/ile_v5_council/.profiles/w1-a-a11y-perf/` (deleted after). Phones emulated (mobile + touch). No screen reader, no WebKit or Firefox, no real device. I did not load 8780, 8770–8772, 8782, the other lanes' 8785 / 8787 / 8789, nor Chrome 9222 / 9223. |
| **Lock** | Every cell of every series waited while `C:/tmp/ile_locks/PERFORMANCE_BENCHMARK_LOCK` existed (the series paused 815 s and again during my second window). The lock was mine for the two trace windows: AB1 20:07:06–20:21:01 (13.6 min, 58 loads) and AB2 20:22:31–20:29:22 (6.6 min, 22 loads), each with the 60 s settle, the load sampled (51–73 % before, 63–65 % during: the machine carried other families' work), the lock deleted in `finally`. |
| **Writes** | Four sessions minted with `Client.force_login` on `ile_v5_l3` (`qa-doc-person`, `qa-person`, `qa-company`, `demo-professionnel`) by `C:/tmp/ile_v5_council/.work/w1-a/w1-a-a11y-perf/mint_sessions_a11y.py` — outside every repository; no password used, typed or stored — writing what a sign-in writes (a session row, `last_login`, an `auth.login` audit row); revoked at the end, the cookie file removed. No other POST. Nothing in the worktree except this file. |
| **Evidence** | `C:/tmp/ile_v5_council/evidence/v54/w1-a/a11y-perf/` (E/ below): `runs/*.jsonl` (one record per cell), `shots/<mode>/` (viewport stills), `crops/`, `probes/`, `perf/` (traces, runs, `summary.json`), `before-lane/` (the same probe on 8793), `summary-*.json|txt`, `small_text.json`, `logs/`. Tools in `C:/tmp/ile_v5_council/.work/w1-a/w1-a-a11y-perf/tools/`: `a11y_probe.py`, `ab_trace.py` (on W1-0's `trace.py` / `analyse.py` / `an_pfr.py`), `perf_compare.py`, `summarise_a11y.py`, `small_text.py`, `probe_legend_ring.py`, `probe_fc_bar.py`, `write_report.py`. |

---

## 0. In short

**What holds, measured (every figure below is from this pass, on the lane):**
- **Keyboard walk, fr and ar, 1440 and 390:** 2 442 real-Tab stops on 76 cells, **0 without a visible indicator** (the W1-0 instrument: a visible style change on the element or its neighbours; its negative control is in the before set's README). Every stop draws W1-A's ring: 2 278 rings measured on pixels, 2 px laguna-550 at a 2 px offset on paper, laguna-400 on night, following the element's radius.
- **The ring on pixels:** sampled on its four sides against the ground outside and the element inside. Against the ground it holds 3.10–3.94 : 1 on paper (laguna-550 on carta-50 3.70, on white 4.11, on the selection wash 3.41) and 14.6–15.1 : 1 in forced colours; against the element inside 3.26–8.73 : 1. The one ring under 3 : 1 against the page is the skip link's (m1). The four hero-legend rows the sampler called «not painted» are painted (`E/probes/legend-row-focus-1440-x3.png`): the row grows on focus and the sample read the old box.
- **Focus never hidden by W1-A's work.** 26 stops end partly and 8 entirely under a pinned layer — all under V4's fixed console bottom bar at 390, the pathway page's sticky section nav at 1440 and the wizard's sticky foot; the same stops end there on the v54/base product on the same lane (`E/before-lane/`). Pre-existing, listed for their owners in §4; W1-A changes none of them.
- **Names and roles unchanged:** axe-core 4.13 (WCAG 2.0–2.2 A/AA) 6 violation nodes on 76 cells against 8 in the before set — the forum register's eyebrow (4 cells, `#d3d2cc` on `#f4f3f0` 1.36 : 1, W3-F1's sheet, identical before) and the login's reset link `target-size` (fr only now: 2, where the before set had 4 — the Arabic help line at 24 px cleared it). No new rule fires.
- **Contrast on pixels:** 7 978 visible text nodes, 2 056 distinct colour pairs, read against the dominant pixel colour of each line box in a screenshot (gradients, glass and photographs included, occluded boxes excluded). Every pair ≥ 4.5 : 1 — the system's bar for all text, DS 2026 §4.4 — except the forum eyebrow above. The lowest held pair is 4.61 (documents), then 4.92 (the lock-up's «Italy» green on the header's glass). The system does not demand 7 : 1 anywhere; for information, 816 pairs under 16 px sit between 4.5 and 7 : 1 (white on the flat primary 5.29, `--text-2` on paper 6.46, `--text-3` 5.14–5.53, laguna text 5.69, the night footer 6.6).
- **Reduced motion is a real still:** 32 cells (8 flagship page types × fr, ar × 1440, 390) under `prefers-reduced-motion: reduce` — 0 running animations, 0 infinite animations, `--motion-fast` resolves to `0ms`, and two stills 1 s apart differ by **0 pixels** on every cell. The hero's route animation is gated by `no-preference`; `--motion-key / -door / -luce` have no consumer yet.
- **Forced colours usable:** 32 cells; the stills of the home, the login, the dashboard and the documents at 1440 and 390 read in the forced palette (backplates behind the hero's text, the door stage kept, chips and buttons with their borders). Focus is the system `Highlight` outline on every stop (`E/probes/fc-390-*.png`), 14.6–15.1 : 1 at 1440.
- **Reflow at 320 × 640:** 38 cells (19 page types × fr, ar) — no horizontal overflow on 17 page types; the two that overflow did so before W1-A (§4, m2 and W3-D).
- **Text spacing (1.4.12):** 32 flagship cells with line-height 1.5, paragraph 2 em, letter 0.12 em, word 0.16 em — 0 overflow, nothing lost; the counts that move are a third line-clamped label in the console bottom bar and the header's lock-up touching the first nav link at 1440 (W2-C1's chrome).
- **Targets:** targets under 24 px fall from 90 to 52 across the 76 cells (the Arabic 24 px help line; what remains is V4's console breadcrumb and bar links at 20 px, W3-A's). Under a coarse pointer the targets under 44 px are V4 components (the account menu's 36 px rows, the password toggle, checkboxes) — W2-A / W1-C, unchanged by W1-A.
- **Health:** 0 CSP violations, 0 console errors (the 404 page's own «Failed to load resource» only) on 76 + 38 + 32 × 3 cells; RTL: no physical property in the four V5 sheets, Vazirmatn on every Arabic role with Host for the Latin runs.
- **Performance, paired on the same lane (n = 4 per cell and server, interleaved, profile A, CPU ×4):** LCP −558 to −886 ms on all ten cells, the first-render task −16 to −168 ms, TBT and the longest task lower everywhere, long tasks > 50 ms equal or fewer (documents fr 7 → 7.5 within the spread), CLS ≤ 0.021 before and ≤ 0.018 after, the LCP element unchanged on every cell, fonts 217–535 KB → 21–63 KB per page, CSS + JS requests equal. `dist/main.css` 35 819 → 42 623 B gzip (+6.8 KB; on the wire with hashed `url()`s ≈ 43.1 KB): every page type stays inside its Wave-1 allowance (headroom ≈ 1.2–1.7 KB) and under the 45 KB ceiling; JS and the page sheets are byte-identical to the before set. 0 animations running at rest on any traced load.

**What is W1-A's to fix (minor):**
- **m1 — the skip link's ring is laguna-400 on paper (1.59 : 1 on the portico, 1.67 on the console)** — V1 `base.css` `.skip-link:focus-visible { outline-color: var(--focus-ring-inverse) }`, and W1-A's aliases point `--focus-ring-inverse` at laguna-400. Against the link's own navy box it is 8.73 : 1, so the focus is visible; against the page it is not, and plan §1.6 asks for ≥ 3 : 1 against both neighbours. Before W1-A the ring was paper on paper (1.03–1.08). Fix: `outline-color: var(--focus-ring)` (laguna-550: 3.70 on carta-50, 3.55 on the navy box). V1 `base.css`'s focus rules are in W1-A's slice.
- **m2 — `input[type=file]` at 320 px:** on `document-requirement` the file input's intrinsic width grows from 306 to 332 px with Host Grotesk (its font size stays 15 px: the typed-text rule excludes `type=file`), so the page's 2 px horizontal overflow at 320 becomes 28 px (fr and ar); 360 px and up are clean, as before. Fix: `max-inline-size: 100%` on the file input — one line beside W1-A's typed-text rule in `v5/base.css` (`input, select, textarea { max-inline-size: 100% }`), or in W1-C's field rules.
- **m3 — the Arabic font budget on two page types:** `document-requirement` and `dashboard-person-terms-pending` print a lowercase hex hash and a rule version, which pulls ILE Mono's second file (7.3 KB): 63 144 B against the 56 KB Arabic budget (the French console stays at 30 916 B under 32 KB). V4 downloaded 484–525 KB there. Take or leave: moving `a–f` and `v` into the core costs ≈ 1 KB on every console page that prints a reference and removes the second file from these two (the implementer's note). Not a regression; a budget line.

---

## 1. Protocol

- **Cells.** 19 page types of the W1-0 inventory, chosen to cover every surface the foundation re-values: home, the open navbar, the persons' door, a pathway page, the FAQ, the contact form, the forum registration, the login, the signup, the person dashboard, «Mes pièces», a document requirement, the case file, the deadlines, «Ma situation», the helpdesk, the company dashboard, the staff queue and the 404 (reached through `/_errors/404/`, the same view, because the lane runs `DEBUG` on) — × fr, ar × 1440 × 900, 390 × 844 = 76 cells. Modes: reduced motion, forced colours and text spacing on 8 flagship page types (32 cells each); 320 × 640 on all 19 (38 cells); the contrast-on-pixels pass on the 76.
- **The W1-0 instrument, unchanged** (`health.js`): overflow, clipped text, overlapping targets, targets under 24 px, axe-core 4.13.0 WCAG 2.x A/AA, the real-Tab focus walk. Compared cell by cell with `MANIFEST.json → summary_by_page_type`.
- **Added by this pass:** per focus stop, the outline sampled on pixels (ring, outer neighbour, inner neighbour, four sides), `elementFromPoint` on nine points of the focused box (covered by a pinned layer?), the box in the viewport; per text node, the computed colour against the dominant pixel colour of its first line box (4 or 5 screens a page), occluded boxes skipped; targets under 44 px under a coarse pointer; `document.getAnimations()`, transition durations and `will-change` at rest; two stills 1 s apart; the text-spacing override injected in a context that bypasses the browser's CSP only (the server's CSP is untouched); the Latin 12 px / Arabic 14 px floors on every visible text node (`small_text.py`, 15 page types).
- **Attribution.** The same probe on the before server 8793 (v54/base product, same clone, same sessions) on 20 cells (home, pathway page, documents, document requirement, login) plus the contrast pass on signup and the forum registration and the 320 series on four console pages: every defect that remains after W1-A is present before it, with the figures in §4.
- **Performance.** `ab_trace.py` = W1-0's `trace.py` run on both servers alternately (before, after, before, …; the order reversed every run): 10 cells × 2 servers × 4 runs = 80 cold loads under profile A (150 ms RTT, 1.6 Mbps / 750 kbps), CPU ×4, cache disabled, a fresh profile per load; LCP, FCP, CLS (session window, before the first input), the first-render task (the main-thread task holding the first Paint), the longest load task, the load tasks > 50 ms, TBT, the INP proxy, the bytes per kind. **The absolute numbers are not the 8782 numbers** (the dev server serves static files uncompressed and with `DEBUG` on, the machine was at 51–73 %): what is read is after − before on the same lane at the same minute, with the W1-0 8782 medians beside them for scale. The plan's PASS on 8782 (n ≥ 9, under the lock, by the Performance Lead) is not replaced by this check.

## 2. Accessibility — the measurements

### 2.1 Keyboard and focus (2.1.1, 2.4.7, 2.4.11, 1.4.11)

| Series | Cells | Tab stops | Without indicator | Rings measured on pixels | Ring < 3 : 1 against the ground | Partly / entirely under a pinned layer | Out of the viewport |
|---|---|---|---|---|---|---|---|
| main (fr + ar, 1440 + 390) | 76 | 2 442 | **0** | 2 278 | 44 — all the skip link (m1) | 26 / 8 — V4's bottom bar, section nav, wizard foot (§4) | 0 |
| forced colours (8 flagships) | 32 | 982 | 6 — the bottom bar's **current** item, which already carries the same inset `Highlight` outline before focus (W3-A; the before set found the same 4) | 914 | 1 (the bar's item against the bar: 2.3 — the bar's own ground, W3-A) | 11 — the bottom bar | 0 |
| before server, 20 cells | 20 | 586 | 0 | — | the skip link at 1.03–1.08 | the same stops, same layers | 0 |

Rings on paper: 3.10 (the arrow links on carta-100), 3.26–3.44 (the utility bar and the language segment), 3.70 (carta-50), 3.76–3.94 (white sheets and fields); on night: laguna-400 at 9.9 : 1 (the hero legend, the rail). Every ring follows the element's radius; the fields' 5 px halo is W1-C's to retarget where `components.css` / `entrance.css` still win (the login's fields keep V4's own ring, visible). `scroll-padding-block-start` is kept in V1 `base.css` and `v2/shell.css`; no stop ended under the sticky header.

### 2.2 Names and roles (axe-core 4.13.0, WCAG 2.0–2.2 A/AA)

| | Now (76 cells) | Before set (same cells) |
|---|---|---|
| violation nodes | 6 | 8 |
| `color-contrast` | 4 — `.forum-hero__eyebrow` «FORUM VÉNÉTIE–MAROC», `#d3d2cc` on `#f4f3f0`, 1.36–1.37 : 1 (fr + ar × 2) | 4 — the same node |
| `target-size` | 2 — the login's «Mot de passe oublié ?» (fr × 2) | 4 (fr + ar × 2) |
| any other rule | 0 | 0 |

### 2.3 Contrast on pixels (1.4.3, 1.4.11)

7 978 text nodes · 2 056 distinct (fg, bg, size, weight) pairs · 76 cells · 4–5 screens a page. Pairs under 4.5 : 1: **the forum eyebrow** (above) and one line-box sample on the signup's footer legal links (`#b9c5d6` with 43 % paper pixels in its box) that the before server returns identically (1.59 on «Mentions légales») and that a direct probe of the same links shows at `#b9c5d6` on `#071226` = 9.9 : 1 — a sampling edge, not a defect. Lowest held pairs: 4.61 (documents), 4.92 (`#157a3c` «Italy» on the glass `#f5f4f1`), 5.14 (`--text-3` on carta-100), 5.29 (white on the flat primary), 5.48, 5.53, 5.69. Minority colours under a line box (hairlines `#d3d2cc`, icons, the lock-up's letters) are reported in `summary-text.json → textured_sample` and are not the text's ground. Families seen on pixels: Host Grotesk, ILE Wordmark, ILE Mono, Vazirmatn — nothing else.

### 2.4 Reduced motion (2.3.3, the standing rule)

32 cells: running animations 0, infinite 0, `--motion-fast` = `0ms`, transition durations `0s` on every sampled control, stills 1 s apart identical (0 differing pixels) on all 32. `will-change` at rest: 1 element on the home, the login and the open navbar at 1440 (V4's hero / door stage, W2-D) — plan §2.6 asks for 0; not W1-A's.

### 2.5 Forced colours

32 cells, stills in `E/shots/forced-colors/`. Read by eye: the home at 1440 and 390 (`E/shots/forced-colors/home-fr-1440x900.png`, `-390x844.png`), the dashboard at 390, the login. The focus ring is the system `Highlight` (Chromium's emulation paints it `rgba(5, 0, 73, .8)`), present on every stop of the targeted probe (`E/probes/fc-390-stop*.png`, `fc-390-bottombar-x2.png`); the sampler's «not painted» counts in this mode are its own limitation (it compares the alpha-blended pixel with the unblended computed colour), not a finding. The chips keep their marks and edges (W1-A's `forced-colors` block), the buttons their borders.

### 2.6 Reflow (1.4.10) and text spacing (1.4.12)

- **320 × 640, 38 cells:** horizontal overflow on `document-requirement` (28 px, fr + ar — m2) and `situation` (fr 22 px, ar 8 px: `div.wiz__foot`, the wizard's sticky foot, 351 → 342 px before → after, W3-D); none on the other 17 page types. Clipped at 320: the console bar's title ellipsis on every console page (fr + ar) and the bottom bar's line-clamped labels (W3-A, as at 390). Targets under 24 px: 0.
- **Text spacing, 32 cells:** 0 overflow; clipped +1 on six console cells at 390 (a third bottom-bar label line-clamped) and the helpdesk's bar title; overlapping targets +2 on the home / navbar at 1440 (the lock-up touching «Personnes» and its sub-menu toggle when letter-spaced — W2-C1) and +1 / +2 on the login (the password toggle and the reset link against the field — W2-B). Nothing becomes unreadable or unreachable.

### 2.7 Targets (2.5.8, SP-8)

Under 24 px (fine pointer, 1440 + 390): 52 now against 90 before — V4's console breadcrumb links and `a.console-bar__link` at 20 px (W3-A), unchanged in count per cell or lower. Under 44 px under a coarse pointer (390): `button.account-menu__link` 222 × 36 (W2-A), `button.form-field__toggle` and the checkboxes (W1-C), the honeypot field. W1-A keeps `--hit-min` at 44 px for the sixteen V4 controls that read it (aliases) until W1-C retargets them.

### 2.8 The type floors (plan §1.1), on pixels

`small_text.py`, 15 page types × fr, ar × 1440, 390. Under 12 px Latin: the lock-up's «™» (7.7 px at 390, 11 px at 1440 — the brand drawing, every page) and `span.note__marker` (9.4 / 10.1 px, the documents page's footnote markers, W3-C's sheet). Under 14 px Arabic: the console bottom bar's five labels at 11 px (W3-A — the implementer's note: at 14 px the fixed bar clips them). Nothing else: the console's one-step rise below 48 rem holds (bodies at 16, labels 15, meta 14, captions 13), typed text is 16 px in every field at every width.

## 3. Performance

### 3.1 Bytes and requests (the lane; the before set's figures from `MANIFEST.json`)

| | Before | After | Allowance / budget |
|---|---|---|---|
| `dist/main.css` raw | 217 057 B | 238 800 B | — |
| `dist/main.css` gzip -9 (plain) · on the wire with hashed `url()`s | 35 819 · 36 294 B | 42 623 · ≈ 43 100 B (the implementer's manifest-rewritten 42 773) | ≤ 45 KB (46 080 B) ✓ |
| page type totals (gzip) | home 39 114 · door 36 294 · interior 36 294 · login 37 502 · dashboard 41 668 · «Mes pièces» 42 839 · case file 41 668 | each + 6.5–6.8 KB | each ≤ before + 8 KB ✓ (headroom ≈ 1.2–1.7 KB for W1-B / W1-C / W1-D) |
| page sheets (raw / gzip) | pages 14 123 / 2 820 · entrance 4 467 / 1 208 · portal + console 25 003 / 5 374 · documents 5 004 / 1 171 | identical | — |
| JS | unchanged (no JS file in the diff) | identical | — |
| CSS + JS requests before `load` | home 10 · login 8 · dashboard 11 · documents 12 | equal on every traced cell | ≤ before ✓ |
| font requests · bytes, Latin public | 5–6 · 217 732–304 340 B | 2 · 20 956 B | ≤ 25 KB ✓ |
| Latin console | 5 · 217 732 B | 3 · 23 644 B (document requirement 4 · 30 916 B) | ≤ 32 KB ✓ |
| Arabic public | 11–13 · 484 456–525 044 B | 3 · 53 184 B | ≤ 56 KB ✓ |
| Arabic console | 11–13 · 352 456–504 956 B | 4 · 55 872 B; **document requirement 5 · 63 144 B** | ≤ 56 KB — m3 |
| font preloads | 2 / 2 | 2 Latin / 3 Arabic, all used on the first screen | ≤ 2 / ≤ 3 ✓ |
| external or `data:` resources in the bundle | one `data:` SVG (the select chevron, V4) | the same; every `url()` self-hosted; 0 `@import` left | CSP-clean ✓ |

### 3.2 Paired cold loads, before (8793) → after (8783), medians of n = 4 each, ms

Spread = min–max of the 4 loads (before / after). Long tasks = load-phase tasks > 50 ms (median count). W1-0 = the 8782 before set's medians (LCP / first-render task / long tasks), for scale only.

| Cell | n | LCP b → a (Δ) | LCP spread b / a | First-render task b → a (Δ) | FRT spread b / a | Longest task b / a | TBT b / a | Long tasks b / a | CLS b / a | INP proxy b / a | Font bytes b / a | W1-0 8782 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| home · fr · 1440 | 4 + 4 | 3670 → 2852 (-818) | 3456–3768 / 2704–2944 | 240 → 115 (-125) | 231–282 / 94–143 | 326 / 216 | 1234 / 569 | 12.0 / 10.0 | 0.0151 / 0.0087 | 76 / 64 | 304 340 / 20 956 | 2064 / 710 / 6 |
| home · fr · 412 | 4 + 4 | 3504 → 2802 (-702) | 3400–3604 / 2772–2804 | 122 → 78 (-43) | 64–190 / 59–84 | 391 / 147 | 1226 / 407 | 11.5 / 11.0 | 0.0000 / 0.0000 | 56 / 64 | 304 340 / 20 956 | 2100 / 746 / 6 |
| home · ar · 1440 | 4 + 4 | 3616 → 3044 (-572) | 3440–4904 / 2996–3244 | 260 → 129 (-131) | 191–289 / 94–203 | 815 / 206 | 2297 / 716 | 11.5 / 11.5 | 0.0211 / 0.0034 | 56 / 64 | 535 436 / 53 184 | 2356 / 938 / 12 |
| home · ar · 412 | 4 + 4 | 3802 → 3130 (-672) | 3456–3844 / 2972–3220 | 168 → 102 (-66) | 138–251 / 83–140 | 603 / 273 | 2057 / 723 | 11.0 / 10.5 | 0.0035 / 0.0000 | 60 / 56 | 515 348 / 53 184 | 2328 / 914 / 12 |
| login · fr · 1440 | 4 + 4 | 3496 → 2688 (-808) | 3328–3600 / 2576–2876 | 304 → 136 (-168) | 254–323 / 118–149 | 333 / 140 | 522 / 156 | 7.5 / 5.0 | 0.0168 / 0.0178 | 76 / 76 | 217 732 / 20 956 | 1720 / 397 / 2 |
| login · ar · 412 | 4 + 4 | 3628 → 2944 (-684) | 3488–3740 / 2908–3132 | 180 → 82 (-98) | 127–199 / 79–100 | 420 / 127 | 1151 / 209 | 11.0 / 6.5 | 0.0008 / 0.0000 | 80 / 64 | 484 456 / 53 184 | 1872 / 483 / 3 |
| dashboard-person · fr · 1440 | 4 + 4 | 3944 → 3058 (-886) | 3804–4184 / 2876–3340 | 136 → 78 (-58) | 82–165 / 68–83 | 407 / 248 | 621 / 297 | 8.0 / 6.5 | 0.0014 / 0.0011 | 36 / 36 | 217 732 / 23 644 | 1604 / 405 / 4 |
| dashboard-person · ar · 412 | 4 + 4 | 3782 → 3224 (-558) | 3484–3872 / 3184–3388 | 127 → 87 (-40) | 96–148 / 78–101 | 526 / 400 | 1119 / 428 | 9.5 / 4.0 | 0.0002 / 0.0000 | 48 / 44 | 352 456 / 55 872 | 1740 / 449 / 5 |
| documents · fr · 1440 | 4 + 4 | 3582 → 2952 (-630) | 3448–4152 / 2776–3444 | 82 → 66 (-16) | 62–103 / 52–75 | 275 / 260 | 502 / 343 | 7.0 / 7.5 | 0.0011 / 0.0011 | 32 / 32 | 217 732 / 23 644 | 1552 / 354 / 3 |
| documents · ar · 412 | 4 + 4 | 3726 → 3032 (-694) | 3376–4372 / 2812–3144 | 118 → 70 (-48) | 85–149 / 59–89 | 458 / 232 | 966 / 280 | 10.5 / 7.0 | 0.0145 / 0.0000 | 52 / 36 | 372 956 / 55 872 | 1672 / 399 / 3 |

**Reading.** On every cell the after is faster: LCP −558 … −886 ms, the first-render task −16 … −168 ms, the longest task and TBT down, long tasks equal or fewer (the one rise, documents fr 7 → 7.5, is half a task inside both spreads). CLS stays under 0.021 before and 0.018 after (login fr 1440: 0.0168 → 0.0178, both far under the 0.05 flagship budget; the capture-load CLS of the 76 cells is 0 with the fonts preloaded and the fallbacks metric-matched). The LCP element never changes (`image.doorway__img` on the home and the login at 1440; the lead paragraph on phones and console pages). `document.getAnimations()` at rest: 0 running on every traced load. The before/after difference is what the fonts do — six to thirteen V4 files of 217–535 KB against two to five of 21–63 KB, preloaded per script — on a dev server that serves them uncompressed; on 8782 the gain is smaller in absolute terms, the direction the same.

### 3.3 Not measured here

The 8782 PASS of plan §2.6 (n ≥ 9 under a quiet lock, LCP ≤ 2.5 s per page type, the first-render task against the before set to ± 30 ms) remains the Performance Lead's; this check establishes that there is no regression to look for. No HTTP/2, no real device, no Safari.

## 4. Findings

| # | Severity | Finding | Where | Before W1-A | Owner · fix |
|---|---|---|---|---|---|
| m1 | minor | The skip link's `:focus-visible` ring is laguna-400 on the page: 1.59 : 1 (portico) / 1.67 (console) against the page, 8.73 against the link's navy box; plan §1.6 wants ≥ 3 : 1 on both sides | every page (44 of 44 cells where the walk reached it) | paper on paper, 1.03–1.08 | **W1-A** (V1 `base.css`'s focus rules are in the slice): `.skip-link:focus-visible { outline-color: var(--focus-ring); }` → 3.70 on carta-50, 3.55 on the navy box |
| m2 | minor | `input#id_file` (type=file) is 332 px wide at 320 px with Host Grotesk (306 px before): the page scrolls sideways by 28 px instead of 2 | `document-requirement` fr + ar, 320 × 640 only (360 and up clean) | overflow 2 px | **W1-A** (one line beside the typed-text rule in `v5/base.css`: `input, select, textarea { max-inline-size: 100%; }`) or W1-C's field rules |
| m3 | minor | ILE Mono's second file (lowercase hex, `v1`) puts two Arabic console page types at 63 144 B of fonts against the 56 KB budget | `document-requirement`, `dashboard-person-terms-pending` (ar) | 484 456–525 044 B | W1-A, to take or leave: `a–f` + `v` into the core (+≈ 1 KB on console pages that print a reference), fonts regenerated and `FONTS_V5.md` hashes updated |
| n1 | note (pre-existing) | Focus ends under the fixed console bottom bar at 390 — entirely: documents «Remplacer la pièce», the company dashboard's «Tous mes besoins», the deadlines page's footer legal links; partly: the requirement form's date field, the helpdesk entries, the staff queue's entries. WCAG 2.4.11 | 10 console cells at 390 | the same stops under the same bar (`E/before-lane/`) | W3-A: `scroll-padding-block-end: calc(var(--bottom-bar-h) + var(--s-4))` while the bar is shown (console.css, < 64 rem) |
| n2 | note (pre-existing) | «Tous les parcours réguliers» ends under the sticky section nav at 1440 on the pathway page; the «Ma situation» date field under the wizard's sticky foot at 390 | `pathway-detail` fr + ar 1440; `situation` fr 390 | identical | W3-F (section nav), W3-D (the foot) — a `scroll-margin` on the content under each sticky bar |
| n3 | note (pre-existing) | In forced colours the bottom bar's current item shows no change on focus: `[aria-current="page"]` already carries the inset `Highlight` outline the focus draws | dashboard, documents, case file at 390 | the before set's finding (4 cells), now 6 | W3-A: a different current-state mark in forced colours (`border-block-start` CanvasText, or an inset ring of 1 px) |
| n4 | note (pre-existing) | The forum eyebrow at 1.36 : 1; the Arabic bottom-bar labels at 11 px; the documents' footnote markers at 9.4 px; the console breadcrumb and bar links at 20 px; the account menu's 36 px rows and the password toggle under a coarse pointer; the login's reset link (`target-size`); one `will-change` at rest in the V4 hero | listed cells | identical | W3-F1 · W3-A · W3-C · W3-A · W2-A / W1-C · W2-B · W2-D |
| n5 | note | At 320 px the console bar's title ends in an ellipsis on every console page and «Ma situation»'s sticky foot is 342 px wide (351 before) | all console page types at 320 | the same or worse | W3-A, W3-D (the bar and the foot are redrawn) |

## 5. «No page worse» — the instrument's counts on this pass against the before set (76 cells)

| Count | Before set | This pass | Note |
|---|---|---|---|
| pages with horizontal overflow | 0 | 0 | — |
| clipped text | 32 | 32 | the console bottom bar's line-clamped labels and the bar titles at 390, as before; the staff queue's two rail labels |
| overlapping targets (same layer) | 12 | 15 | +2 `situation` fr 390 (the sticky foot over the date field at scroll 0), +1 `helpdesk-queue` ar 1440 (the rail's last item under its collapse button) — the implementer's two hit-tested artefacts, confirmed |
| targets under 24 px | 90 | 52 | the Arabic help line and small roles raised to 14 px |
| missing focus indicators | 0 | 0 | — |
| axe violation nodes | 8 | 6 | §2.2 |
| CSP violations · console errors | 0 · 0 | 0 · 0 | the 404 page's own resource line excepted, as in the before set |
| largest capture CLS | 0.0977 | 0 | no layout-shift entry on any of the 76 loads |

## 6. Instrument notes (for the next reviewer)

- The ring sampler reads the focused box once it holds still; an element that grows after a delayed class change (the hero legend rows) can still be read on its old box — verified by eye where it happened. In forced colours it compares an alpha-blended pixel with an unblended computed colour and under-reports; the targeted probe is the evidence there.
- Text contrast is sampled on the first line box of each text node; a line box that straddles the edge of a band yields a mixed ground (flagged `textured`, with the dominant colour's share). The 'none' run's own contrast figures predate the occlusion check and are superseded by `runs/a11y-text.jsonl`.
- The crops under `E/crops/` scroll the element to 40 px from the top, where the sticky header can cover it; the records, not the crops, are the measurement.
- Phones are emulated; no screen reader was run; names and roles are axe's reading, not a human one — W1-A changes no name, role or state.

## 7. Appendix — the 76 cells

Columns: overflow now/before · clipped now/before · overlapping now/before · targets < 24 now/before · Tab stops / without indicator · rings measured · ring vs ground, min · stops under a pinned layer (entirely) · axe nodes now/before · text pairs / under 4.5 / min ratio · font bytes (requests).

| Cell | ovf | clipped | overlap | < 24 | stops / missing | rings | ring min | pinned (full) | axe | text pairs / fails / min | fonts (req) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| case-file ar 1440x900 | 0/0 | 0/0 | 0/0 | 4/5 | 29 / 0 | 29 | 4 | 0 (0) | 0/0 | 27 / 0 / 5 | 55872 (4) |
| case-file ar 390x844 | 0/0 | 0/0 | 0/0 | 0/1 | 16 / 0 | 16 | 2 | 0 (0) | 0/0 | 25 / 0 / 5 | 55872 (4) |
| case-file fr 1440x900 | 0/0 | 0/0 | 0/0 | 4/4 | 29 / 0 | 29 | 4 | 0 (0) | 0/0 | 30 / 0 / 5 | 23644 (3) |
| case-file fr 390x844 | 0/0 | 3/3 | 0/0 | 0/0 | 16 / 0 | 16 | 2 | 0 (0) | 0/0 | 27 / 0 / 5 | 23644 (3) |
| company-dashboard ar 1440x900 | 0/0 | 0/0 | 0/0 | 2/3 | 25 / 0 | 25 | 4 | 0 (0) | 0/0 | 33 / 0 / 5 | 55872 (4) |
| company-dashboard ar 390x844 | 0/0 | 0/0 | 0/0 | 0/1 | 20 / 0 | 20 | 2 | 1 (1) | 0/0 | 36 / 0 / 5 | 55872 (4) |
| company-dashboard fr 1440x900 | 0/0 | 0/0 | 0/0 | 2/2 | 25 / 0 | 25 | 4 | 0 (0) | 0/0 | 33 / 0 / 5 | 23644 (3) |
| company-dashboard fr 390x844 | 0/0 | 3/3 | 0/0 | 0/0 | 20 / 0 | 20 | 2 | 1 (1) | 0/0 | 34 / 0 / 5 | 23644 (3) |
| contact-form ar 1440x900 | 0/0 | 0/0 | 0/0 | 0/1 | 43 / 0 | 41 | 2 | 0 (0) | 0/0 | 31 / 0 / 5 | 53184 (3) |
| contact-form ar 390x844 | 0/0 | 0/0 | 0/0 | 0/1 | 29 / 0 | 27 | 3 | 0 (0) | 0/0 | 25 / 0 / 5 | 53184 (3) |
| contact-form fr 1440x900 | 0/0 | 0/0 | 0/0 | 0/0 | 43 / 0 | 41 | 2 | 0 (0) | 0/0 | 32 / 0 / 5 | 20956 (2) |
| contact-form fr 390x844 | 0/0 | 0/0 | 0/0 | 0/0 | 29 / 0 | 27 | 2 | 0 (0) | 0/0 | 25 / 0 / 5 | 20956 (2) |
| dashboard-person ar 1440x900 | 0/0 | 0/0 | 0/0 | 2/3 | 28 / 0 | 27 | 4 | 0 (0) | 0/0 | 39 / 0 / 5 | 55872 (4) |
| dashboard-person ar 390x844 | 0/0 | 0/0 | 0/0 | 0/1 | 17 / 0 | 16 | 2 | 0 (0) | 0/0 | 37 / 0 / 5 | 55872 (4) |
| dashboard-person fr 1440x900 | 0/0 | 0/0 | 0/0 | 2/2 | 28 / 0 | 27 | 4 | 0 (0) | 0/0 | 42 / 0 / 5 | 23644 (3) |
| dashboard-person fr 390x844 | 0/0 | 3/3 | 0/0 | 0/0 | 17 / 0 | 16 | 2 | 0 (0) | 0/0 | 39 / 0 / 5 | 23644 (3) |
| deadlines ar 1440x900 | 0/0 | 0/0 | 0/0 | 3/4 | 24 / 0 | 24 | 4 | 0 (0) | 0/0 | 17 / 0 / 6 | 53184 (3) |
| deadlines ar 390x844 | 0/0 | 0/0 | 0/0 | 0/1 | 12 / 0 | 12 | 2 | 3 (0) | 0/0 | 13 / 0 / 6 | 53184 (3) |
| deadlines fr 1440x900 | 0/0 | 0/0 | 0/0 | 3/3 | 24 / 0 | 24 | 4 | 0 (0) | 0/0 | 20 / 0 / 6 | 20956 (2) |
| deadlines fr 390x844 | 0/0 | 3/3 | 0/0 | 0/0 | 12 / 0 | 12 | 2 | 3 (3) | 0/0 | 13 / 0 / 6 | 20956 (2) |
| document-requirement ar 1440x900 | 0/0 | 0/0 | 0/0 | 4/5 | 25 / 0 | 24 | 4 | 0 (0) | 0/0 | 35 / 0 / 5 | 63144 (5) |
| document-requirement ar 390x844 | 0/0 | 1/1 | 0/0 | 0/1 | 12 / 0 | 11 | 2 | 1 (0) | 0/0 | 26 / 0 / 5 | 63144 (5) |
| document-requirement fr 1440x900 | 0/0 | 0/0 | 0/0 | 4/4 | 25 / 0 | 24 | 4 | 0 (0) | 0/0 | 39 / 0 / 5 | 30916 (4) |
| document-requirement fr 390x844 | 0/0 | 4/4 | 0/0 | 0/0 | 12 / 0 | 11 | 2 | 1 (0) | 0/0 | 29 / 0 / 5 | 30916 (4) |
| documents ar 1440x900 | 0/0 | 0/0 | 0/0 | 2/3 | 39 / 0 | 38 | 3 | 0 (0) | 0/0 | 34 / 0 / 5 | 55872 (4) |
| documents ar 390x844 | 0/0 | 0/0 | 0/0 | 0/1 | 28 / 0 | 27 | 2 | 1 (0) | 0/0 | 33 / 0 / 5 | 55872 (4) |
| documents fr 1440x900 | 0/0 | 0/0 | 0/0 | 2/2 | 39 / 0 | 38 | 3 | 0 (0) | 0/0 | 38 / 0 / 5 | 23644 (3) |
| documents fr 390x844 | 0/0 | 3/3 | 0/0 | 0/0 | 28 / 0 | 27 | 2 | 1 (1) | 0/0 | 34 / 0 / 5 | 23644 (3) |
| door-persons ar 1440x900 | 0/0 | 0/0 | 0/0 | 0/1 | 50 / 0 | 42 | 2 | 0 (0) | 0/0 | 35 / 0 / 5 | 53184 (3) |
| door-persons ar 390x844 | 0/0 | 0/0 | 0/0 | 0/1 | 36 / 0 | 28 | 3 | 0 (0) | 0/0 | 19 / 0 / 5 | 53184 (3) |
| door-persons fr 1440x900 | 0/0 | 0/0 | 0/0 | 0/0 | 50 / 0 | 42 | 2 | 0 (0) | 0/0 | 36 / 0 / 5 | 20956 (2) |
| door-persons fr 390x844 | 0/0 | 0/0 | 0/0 | 0/0 | 36 / 0 | 28 | 2 | 0 (0) | 0/0 | 19 / 0 / 5 | 20956 (2) |
| error-404 ar 1440x900 | 0/0 | 0/0 | 0/0 | 0/1 | 42 / 0 | 36 | 2 | 0 (0) | 0/0 | 26 / 0 / 5 | 53184 (3) |
| error-404 ar 390x844 | 0/0 | 0/0 | 0/0 | 0/1 | 28 / 0 | 22 | 3 | 0 (0) | 0/0 | 19 / 0 / 5 | 53184 (3) |
| error-404 fr 1440x900 | 0/0 | 0/0 | 0/0 | 0/0 | 42 / 0 | 36 | 2 | 0 (0) | 0/0 | 27 / 0 / 5 | 20956 (2) |
| error-404 fr 390x844 | 0/0 | 0/0 | 0/0 | 0/0 | 28 / 0 | 22 | 2 | 0 (0) | 0/0 | 19 / 0 / 5 | 20956 (2) |
| faq ar 1440x900 | 0/0 | 0/0 | 0/0 | 0/1 | 48 / 0 | 45 | 2 | 0 (0) | 0/0 | 30 / 0 / 5 | 53184 (3) |
| faq ar 390x844 | 0/0 | 0/0 | 0/0 | 0/1 | 34 / 0 | 31 | 3 | 0 (0) | 0/0 | 23 / 0 / 5 | 53184 (3) |
| faq fr 1440x900 | 0/0 | 0/0 | 0/0 | 0/0 | 48 / 0 | 45 | 2 | 0 (0) | 0/0 | 31 / 0 / 5 | 20956 (2) |
| faq fr 390x844 | 0/0 | 0/0 | 0/0 | 0/0 | 34 / 0 | 31 | 2 | 0 (0) | 0/0 | 23 / 0 / 5 | 20956 (2) |
| forum-register ar 1440x900 | 0/0 | 0/0 | 0/0 | 0/1 | 37 / 0 | 35 | 2 | 0 (0) | 1/1 | 30 / 1 / 1 | 53184 (3) |
| forum-register ar 390x844 | 0/0 | 0/0 | 0/0 | 0/1 | 23 / 0 | 21 | 3 | 0 (0) | 1/1 | 21 / 1 / 1 | 53184 (3) |
| forum-register fr 1440x900 | 0/0 | 0/0 | 0/0 | 0/0 | 37 / 0 | 35 | 2 | 0 (0) | 1/1 | 30 / 1 / 1 | 20956 (2) |
| forum-register fr 390x844 | 0/0 | 0/0 | 0/0 | 0/0 | 23 / 0 | 21 | 2 | 0 (0) | 1/1 | 21 / 1 / 1 | 20956 (2) |
| helpdesk ar 1440x900 | 0/0 | 0/0 | 0/0 | 3/4 | 30 / 0 | 30 | 4 | 0 (0) | 0/0 | 22 / 0 / 5 | 55872 (4) |
| helpdesk ar 390x844 | 0/0 | 0/0 | 0/0 | 0/1 | 18 / 0 | 18 | 2 | 3 (0) | 0/0 | 19 / 0 / 5 | 55872 (4) |
| helpdesk fr 1440x900 | 0/0 | 0/0 | 0/0 | 3/3 | 30 / 0 | 30 | 4 | 0 (0) | 0/0 | 28 / 0 / 5 | 23644 (3) |
| helpdesk fr 390x844 | 0/0 | 3/3 | 0/0 | 0/0 | 18 / 0 | 18 | 2 | 5 (0) | 0/0 | 18 / 0 / 5 | 23644 (3) |
| helpdesk-queue ar 1440x900 | 0/0 | 0/0 | 1/0 | 3/4 | 30 / 0 | 30 | 4 | 0 (0) | 0/0 | 22 / 0 / 6 | 55872 (4) |
| helpdesk-queue ar 390x844 | 0/0 | 0/0 | 0/0 | 0/1 | 16 / 0 | 16 | 2 | 1 (0) | 0/0 | 17 / 0 / 6 | 55872 (4) |
| helpdesk-queue fr 1440x900 | 0/0 | 2/2 | 0/0 | 3/3 | 30 / 0 | 30 | 4 | 0 (0) | 0/0 | 23 / 0 / 6 | 23644 (3) |
| helpdesk-queue fr 390x844 | 0/0 | 4/4 | 0/0 | 0/0 | 16 / 0 | 16 | 2 | 2 (0) | 0/0 | 20 / 0 / 6 | 23644 (3) |
| home ar 1440x900 | 0/0 | 0/0 | 0/0 | 0/1 | 60 / 0 | 52 | 2 | 0 (0) | 0/0 | 39 / 0 / 5 | 53184 (3) |
| home ar 390x844 | 0/0 | 0/0 | 0/0 | 0/1 | 46 / 0 | 38 | 3 | 0 (0) | 0/0 | 21 / 0 / 5 | 53184 (3) |
| home fr 1440x900 | 0/0 | 0/0 | 0/0 | 0/0 | 60 / 0 | 52 | 2 | 0 (0) | 0/0 | 40 / 0 / 5 | 20956 (2) |
| home fr 390x844 | 0/0 | 0/0 | 0/0 | 0/0 | 46 / 0 | 38 | 3 | 0 (0) | 0/0 | 24 / 0 / 5 | 20956 (2) |
| login ar 1440x900 | 0/0 | 0/0 | 1/1 | 0/1 | 40 / 0 | 37 | 2 | 0 (0) | 0/1 | 29 / 0 / 5 | 53184 (3) |
| login ar 390x844 | 0/0 | 0/0 | 1/1 | 0/1 | 26 / 0 | 23 | 4 | 0 (0) | 0/1 | 21 / 0 / 5 | 53184 (3) |
| login fr 1440x900 | 0/0 | 0/0 | 1/1 | 0/0 | 40 / 0 | 37 | 2 | 0 (0) | 1/1 | 30 / 0 / 5 | 20956 (2) |
| login fr 390x844 | 0/0 | 0/0 | 1/1 | 0/0 | 26 / 0 | 23 | 4 | 0 (0) | 1/1 | 21 / 0 / 5 | 20956 (2) |
| navbar-open ar 1440x900 | 0/0 | 0/0 | 0/0 | 0/1 | 60 / 0 | 52 | 2 | 0 (0) | 0/0 | 38 / 0 / 5 | 53184 (3) |
| navbar-open ar 390x844 | 0/0 | 0/0 | 0/0 | 0/1 | 16 / 0 | 16 | 4 | 0 (0) | 0/0 | 8 / 0 / 5 | 53184 (3) |
| navbar-open fr 1440x900 | 0/0 | 0/0 | 0/0 | 0/0 | 60 / 0 | 52 | 2 | 0 (0) | 0/0 | 38 / 0 / 5 | 20956 (2) |
| navbar-open fr 390x844 | 0/0 | 0/0 | 0/0 | 0/0 | 16 / 0 | 16 | 4 | 0 (0) | 0/0 | 8 / 0 / 5 | 20956 (2) |
| pathway-detail ar 1440x900 | 0/0 | 0/0 | 0/0 | 0/1 | 63 / 0 | 63 | 2 | 1 (1) | 0/0 | 35 / 0 / 5 | 53184 (3) |
| pathway-detail ar 390x844 | 0/0 | 0/0 | 0/0 | 0/1 | 49 / 0 | 49 | 3 | 0 (0) | 0/0 | 21 / 0 / 5 | 53184 (3) |
| pathway-detail fr 1440x900 | 0/0 | 0/0 | 0/0 | 0/0 | 63 / 0 | 63 | 2 | 1 (1) | 0/0 | 34 / 0 / 5 | 20956 (2) |
| pathway-detail fr 390x844 | 0/0 | 0/0 | 0/0 | 0/0 | 49 / 0 | 49 | 2 | 0 (0) | 0/0 | 20 / 0 / 5 | 20956 (2) |
| signup ar 1440x900 | 0/0 | 0/0 | 2/2 | 0/1 | 44 / 0 | 42 | 2 | 0 (0) | 0/0 | 31 / 0 / 5 | 53184 (3) |
| signup ar 390x844 | 0/0 | 0/0 | 2/2 | 0/1 | 30 / 0 | 28 | 3 | 0 (0) | 0/0 | 25 / 1 / 2 | 53184 (3) |
| signup fr 1440x900 | 0/0 | 0/0 | 2/2 | 0/0 | 44 / 0 | 42 | 2 | 0 (0) | 0/0 | 31 / 0 / 5 | 20956 (2) |
| signup fr 390x844 | 0/0 | 0/0 | 2/2 | 0/0 | 30 / 0 | 28 | 3 | 0 (0) | 0/0 | 24 / 0 / 5 | 20956 (2) |
| situation ar 1440x900 | 0/0 | 0/0 | 0/0 | 3/4 | 30 / 0 | 30 | 4 | 0 (0) | 0/0 | 27 / 0 / 5 | 53184 (3) |
| situation ar 390x844 | 0/0 | 0/0 | 0/0 | 0/1 | 18 / 0 | 18 | 2 | 0 (0) | 0/0 | 19 / 0 / 5 | 53184 (3) |
| situation fr 1440x900 | 0/0 | 0/0 | 0/0 | 3/3 | 30 / 0 | 30 | 4 | 0 (0) | 0/0 | 29 / 0 / 5 | 20956 (2) |
| situation fr 390x844 | 0/0 | 3/3 | 2/0 | 0/0 | 18 / 0 | 18 | 2 | 1 (0) | 0/0 | 19 / 0 / 5 | 20956 (2) |

The ring minimum of 1.59 / 1.67 in every cell is the skip link (m1); the next lowest rings are 3.10–3.94. The text minimum of 1.37 on the forum cells is the eyebrow (n4); 1.59 on `signup ar 390` is the sampling edge of §2.3.
