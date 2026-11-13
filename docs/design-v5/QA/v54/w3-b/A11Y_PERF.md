# W3-B · Dashboard and cards — accessibility + performance check (one pass)

Label `w3-b-a11y-perf`, 11 October 2026 — the family's one accessibility/performance check (V5.5: implement → review
once → fix → ship). Built nothing, changed nothing in the family's code. Checked branch `v54-w3-b` at `41a725a`
(step 1 + step 2; `dc11c2f` above it adds only the senior review's `REVIEW.md`), merge base with `design-v5` `1c001e6`.

**Lane.** Lane 6, port 8786 (this role's alone — the reviewer worked on 8886). Accessibility on the dev server from
`C:/tmp/ile_wt/v54-w3-b` (`ile_v5_l6`, `ILE_REFERENCE_DATE=2026-10-03`, `DB_CONN_MAX_AGE=0`, `--noreload`, no preview
flag). Performance on the same port: the merge base (an export of `1c001e6` in this role's scratch folder) and the
worktree served in turn, then the worktree's compressed twin — the plan's 8782 shape: DEBUG off,
`CompressedManifestStaticFilesStorage`, hashed URLs, gzip on the wire, `collectstatic` into a scratch root (settings
outside every repository: W3-A's check's file, re-pointed). Signed-in pages through sessions minted with
`Client.force_login` on `ile_v5_l6` (no password used, typed or stored), revoked at the end; each session's entrance
release taken by one warm-up load before the measured passes. Two lane-only accounts — an institution (two dates, one
overdue; an unread message) and a university — with unusable passwords, created for the bridge and deleted at the end
with everything they owned. Headless Playwright Chromium (the venv's 1.63), its own profile under
`C:/tmp/ile_v5_council/.profiles/w3-b-a11y-perf/`; one browser and no pytest at a time; every series waited on
`PERFORMANCE_BENCHMARK_LOCK` (never present; never created). **No run crashed.** Never 8780, 8782, 9222 or 9223.

**Shared data.** The reviewer's lane data put an overdue date on `qa-person` during the first passes, then removed it:
`qa-person` was walked in both states — the NowPanel's takeover (kept as `takeover-P1-*`) and the conditions gate.

Evidence: `C:/tmp/ile_v5_council/evidence/v54/w3-b/a11y-perf/` — `desk/` and `phone/` (keyboard, pixel contrast, hit
areas, accessibility tree, axe — one JSON per page), `reflow/`, `spacing/`, `reduce/`, `forced/`, `forced-rail/`,
`perf/` (the before/after runs and traces, `summary.json`, `shifts.json`), `twin/twin-head/` (the W1-0-protocol runs,
traces, `summary.json`), `rest.json`. Probes: `C:/tmp/ile_v5_council/.work/w3-b/w3-b-a11y-perf/`.

## Verdict — SHIP_AFTER_FIXES

0 blocking · 2 major · 5 minor. Both majors sit in W3-B's own diff and are small: a deadline's own words drawn with no
direction on Arabic pages (the review's M2, confirmed on pixels), and the conditions gate's primary whose Arabic name
does not contain its visible words (WCAG 2.5.3 — gone if the review's M1 is applied). Otherwise no WCAG 2.2 AA failure
in the three dashboards (fr, ar; 1440, 390 touch, 320; reduced motion, forced colours, text spacing). **No performance
regression:** JS unchanged, CSS +761 B gzip (inside §2.6's once-only allowance, whose conditions the measures meet),
LCP 250–300 ms earlier than V4 and no worse than the merge base, the first-render task and the longest task far under
V4's, CLS 0 on the production-shaped twin, nothing loops.

## What was measured

10 page states × fr / ar:

| Key | Account | Page | What it shows |
|---|---|---|---|
| P1 | `qa-person` | `/espace-reserve/` | «à vous» — the conditions gate («Accepter les Conditions»), and the overdue takeover while the reviewer's date stood; 7 pieces, the folds |
| P2 | `qa-doc-person` | `/espace-reserve/` | «à vous», «Remplacer la pièce» |
| P3 | `qa-fresh-person` | `/espace-reserve/` | «pas encore de dossier», the owner's door |
| P4 | `seed-person` | `/espace-reserve/` | «rien à faire» |
| C1 | `qa-company` | `/espace-reserve/entreprise/` | the company, «Ouvrir le besoin», four needs |
| C2 | `seed-company` | `/espace-reserve/entreprise/` | the company account without a company, «Déclarer mon entreprise» |
| B1 | lane-only institution | `/espace-reserve/` | the bridge: «1 en retard», «1 non lue» |
| B2 | lane-only university | `/espace-reserve/` | the bridge: its organisation, empty lines |
| B3 | `seed-actor` | `/espace-reserve/` | the bridge: an authorised actor |
| B4 | `qa-company` | `/espace-reserve/` | W1-0's «org-bridge» URL — now the person's no-file dashboard (the account is typed «person») |

Passes: 1440 × 900 (fine pointer) and 390 × 844 (phone emulation, touch) — keyboard walk, pixel contrast, hit areas,
accessibility tree, axe-core 4.13.0 (W1-0's copy) on `wcag2a/2aa/21a/21aa/22aa` and `best-practice`, W1-0's
`health.js`; 320 × 640 reflow; WCAG 1.4.12 text spacing at 1440 and 390; reduced motion (`emulateMedia`) and forced
colours (Chromium's emulation) at 1440 and 390. **184 recorded page loads: 0 CSP reports, 0 console errors, every
response 200.**

How the probes read pixels. The keyboard walk clips every stop focused, then the same clip at the same scroll with
nothing focused: the indicator is the pixels that changed (ring fill = changed pixels in a 6 px band round the box ÷ a
2 px perimeter; change contrast = the median ratio between each changed pixel's two colours). Contrast: every text run
of `<main>` fully in view and under no fixed layer — its computed colour, with its opacity chain, against the pixels
under it, the page re-drawn with every glyph transparent: the dominant pixel, and the worst pixel covering ≥ 5 % of the
run. Hit areas: `elementFromPoint` probed outward from each target's centre.

## Accessibility

| Check | Result |
|---|---|
| axe 2.0–2.2 A/AA | **0 violations** on 44 loads (1440 and 390); best-practice 0. «Incomplete» only in W3-A's chrome (the rail's words on its night ground, which axe cannot resolve; the phone bar's `aria-controls` to the closed drawer). axe's label-in-name rule is experimental and off: finding 2 was read by hand |
| Keyboard, fr and ar | skip links → rail (the bar on phones) → the NowPanel's primary → «Votre dossier» → «Voir mes documents» → each row's act (`aria-describedby` = its piece) → the folds → the pre-assessment → the account's links → footer. The company: the primary → «Voir et modifier l'identité» → «Tous mes besoins» → each need (its title; a draft: its act, described by the need) → «Nouveau besoin». The bridge: «Toutes mes échéances» → «Toutes mes communications» → the message → «Mon profil» → the account's links. **978 stops** at 1440 and 390: every one named, every one `:focus-visible`, every ring measured on pixels |
| Focus visible | laguna-550, 2 px at 2 px on paper — change contrast **3.94 : 1** on carta-25, 4.11 on white (COLOUR §9's figures); laguna-400 inset on the night rail, 7.65–9.93. Ring fill ≥ 0.97 of a 2 px perimeter on 977 / 978 stops; the one below (0.56, C1 fr) is a stop Tab scrolls flush with the viewport's bottom edge — its ring's lower edge cut by the viewport (O1) |
| Focus not obscured (2.4.11) | **0 stops** hidden or partly covered by the sticky bar (desktop) or the bottom bar (phones: the shell's `scroll-padding-block: 4rem 5.5rem` holds). Skip links: their 120 ms entrance starts above the edge and rests at top 8 px (instant under reduced motion) |
| Contrast on pixels | **1 844 text runs, 0 below AA** — also against the worst pixel. State words ≥ **7.18 : 1** (the azione «1 en retard» on its body is the floor): COLOUR §10's AAA rule for state words holds. Text under 16 px between 4.5 and 7 : 1 is W1-A's tokens as designed — white on the primary 5.29 (15 px), laguna-700 links 6.05 (13–14 px), text-3 labels 5.88–6.14 (12–14 px: the NowPanel's `dt`, the journey's shores, the company eyebrow), text-2 meta 6.87; none is a state word or a notice title, so no rule of the system asks 7 : 1 of them |
| Names, roles, structure | 0 nameless controls (CDP accessibility tree); one h1; the NowPanel a region named by its h2; the folds' h2 inside `<summary>` exposed as level-2 headings; the ledger's marks `aria-hidden`, the group's word and count as text; unread = weight + «Non lue» (the dot hidden). Locked French on Arabic pages in `<span lang="fr">`; piece titles `lang="fr" dir="ltr"`. 2.5.3 holds in fr, en, it — not in ar (finding 2) |
| Arabic | mirrored grid, arrows and chevrons flipped; **no Arabic text under 14 px** (the type system's floor); record words isolated everywhere but finding 1 |
| Reduced motion — a real still | **0 animations** at load, at 1 s, after a fold opens, a hover, two Tabs (40 loads, 1440 and 390); every transition computes to 0 s (links, buttons, the fold's chevron, chips, the NowPanel); the session's entrance release resolves to finished 0-ms animations. With motion: 0 running animations 2.5 s after load on every page |
| Forced colours | the NowPanel keeps a 1 px CanvasText edge (no shadow); chips keep their 1 px edge — dashed for the attesa states, so the shape still speaks; the ledger's marks follow `currentColor` (shape = state); the ring in Highlight (change contrast 15.1 : 1); readable at 1440 and 390 (`forced/*.png`). One shell defect: finding 5 |
| Reflow 320 × 640 | 0 overflow, 0 clipped text, 20 / 20 pages |
| Text spacing (1.4.12) | 0 overflow at 1440 and 390; nothing of the dashboards clipped — the only ellipsis is the rail's account name (W3-A's, clipped before the spacing too) |
| Targets | fine pointer: every target ≥ 24 px or spaced (the breadcrumb «Accueil» 43 × 20 has the spacing exception — W3-A's); the primary 44 tall; row acts 36 (`btn--sm`, §1.8's fine-pointer size). Coarse pointer (390 touch): every control 44 tall or more — section links, list links, row acts, account links 44, the folds 55, primaries ≥ 44 — except the inline link of an empty line (finding 3) |
| Against W1-0's «before» set | no count rose on the dashboards' page types: overflow 0, axe contrast failures 0, focus missing 0, CSP 0, console errors 0. The overlapping pairs this pass's health counts list are the two off-screen skip links stacked on each other (W3-A's, every console page) and the sticky bar over content scrolled under it at the walk's last position — a measuring position, not a collision |

## Performance

**Weight** (`gzip -9` of the committed bundles, the steward's method):

| | W1-0 «before» (V4) | merge base `1c001e6` = DL54-73's ceiling | `v54-w3-b` | W3-B's delta |
|---|---|---|---|---|
| console page types (main + portal + console) | 41 668 | 50 007 | 50 768 | **+761** (+1.5 %) |
| the company's dashboard (+ companies.css) | 42 541 | 50 880 | 51 641 | +761 |
| `dist/main.css` | 36 294 | 42 452 | 41 802 | −650 (45 KB cap at every merge: holds) |
| `dist/portal/console.css` | — | 5 292 | 7 012 | +1 720 (the dashboards' partial) |
| `dist/portal/portal.css` | — | 2 263 | 1 954 | −309 |
| JS | 36 706 · 8 requests | 40 578 · 7 | 40 578 · 7 | **0** (no script in the diff) |

On the wire (the twin): CSS 3 requests / 50 831 B (4 / 51 704 B on the company's page), JS 7 / 40 578 B, fonts 3 /
23.6 KB in French (budget ≤ 32 KB) and 4 / 55.9 KB in Arabic (≤ 56 KB). CSS + JS requests before `load`: 10, V4's 11.
§2.6 item 5 read on this: over the ceiling by 761 B after the legacy rules were deleted (main −650, portal −309); the
page-partial move was weighed and refused by the implementer (every session lands on a dashboard); LCP and the first
render no worse (below) — the once-only raise (≤ 2 KB) is open to the CD (finding 7).

**Before / after on the lane** — interleaved blocks BASE · HEAD · HEAD · BASE, n = 7 a cell, CPU ×4, no network
throttling (the dev server sends the CSS uncompressed: a throttled network would measure bytes production never sends),
cold, W1-0's trace analysis; medians:

| Cell | LCP BASE → HEAD (ms) | longest task | Σ (task − 50 ms) | LCP element BASE → HEAD | CLS max BASE / HEAD |
|---|---|---|---|---|---|
| person fr 1440 | 976 → 1040 | 156 → 156 | 184 → 234 | `p.empty` → `p.db-empty` | 0 / 0.0002 |
| person ar 1440 | 988 → 948 | 213 → 152 | 349 → 276 | `h1.ctx__title` → `h2.db-now__title` | 0 / 0.0144 (one load) |
| person fr 412 | 876 → 880 | 176 → 154 | 257 → 208 | `p.panel__title` → `h2.db-now__title` | 0 / 0 |
| person ar 412 | 864 → 1044 | 238 → 219 | 239 → 352 | `p.panel__title` → `h2.db-now__title` | 0 / 0 |
| company fr 1440 | 688 → 840 | 174 → 169 | 194 → 242 | `p.panel__title` → `h2.db-now__title` | 0.0005 / 0.0153 |
| company fr 412 | 704 → 652 | 168 → 183 | 202 → 255 | `p.panel__title` → `h2.db-now__title` | 0 / 0 |
| bridge fr 1440 | 728 → 700 | 115 → 126 | 127 → 137 | `p.ws-head__lead` both | 0.0005 / 0 |

The spreads overlap on every cell (person ar 412: LCP 716–1316 before, 712–1408 after — `perf/summary.json`) and the
differences change sign from cell to cell: no consistent regression; the longest task is lower in 5 of 7 cells. The
interaction proxy (h1 click + Tab) is the same before and after (136 / 136 ms at ar 412).

**Against the W1-0 «before» set, with its own protocol** — the compressed twin; W1-0's `trace.py` byte-identical
(profile A 150 ms RTT 1.6 / 0.75 Mbps, CPU ×4, cache off, a fresh profile per load); n = 9; medians [range]; V4 =
W1-0's medians on 8782:

| `dashboard-person` | LCP | first-render task | longest task | tasks > 50 ms | CLS | LCP element |
|---|---|---|---|---|---|---|
| fr 1440 | **1328** [1232–1692] · V4 1604 | **53** · V4 405 | **104** · V4 405 | 3 · V4 4 | 0 · V4 0 | `p.db-empty` · V4 `p.empty` |
| fr 412 | **1284** [1184–1404] · V4 1584 | **39** · V4 370 | **117** · V4 370 | 4 · V4 4 | 0 · V4 0 | `h2.db-now__title` · V4 `p.panel__title` |
| ar 1440 | **1532** [1400–1784] · V4 1792 | **57** · V4 500 | **145** · V4 500 | 5 · V4 7 | 0 · V4 0.0001 | `h2.db-now__title` · V4 `h1.ctx__title` |
| ar 412 | **1488** [1332–1816] · V4 1740 | **42** · V4 449 | **154** · V4 449 | 4 · V4 5 | 0 · V4 0 | `h2.db-now__title` · V4 `p.panel__title` |

LCP 252–300 ms earlier than V4 on every cell (≤ 2.5 s everywhere); the first-render task 39–57 ms where V4's was
370–500; the longest task 104–154 ms where V4's was 370–500 — and lower than W3-A's own twin of the pre-W3-B dashboard
(118–205); no more tasks over 50 ms than V4; CLS 0 on all 36 loads; the LCP element is the NowPanel's title wherever
it is not the side column's empty line — never worse. The company's dashboard (no W1-0 trace exists): LCP 1180–1536 ms,
CLS 0 on 20 loads, longest task 109–214 ms. Tasks over 50 ms after the first render remain — style and layout passes as
the sheets, the fonts and the sprite land (≈ 0.9–1.4 s), and the shell's script — as V4 had 4–7 a load; W3-B adds no
script and the lane's before/after shows none added.

**At rest** (`rest.json`, the twin, 7 pages × 1440 and 390, a 5 s window 3 s after load): 0 `requestAnimationFrame`,
0 timers, 0 style recalculations, 0 layouts, ≤ 2 ms of task time, 0 running animations — **nothing loops**.

## Findings

**1 · major · W3-B — In Arabic, a deadline's own words are drawn with no direction (the NowPanel's takeover; the
lists).** The takeover branch of `portal.services.now_panel` keeps `_now_base()`'s empty `words`, and
`templates/portal/partials/now_panel.html` l.21–22 emits `lang`/`dir` only when `now.words.lang` is set; the `Deadline`
model records no language. On an Arabic page the French title takes the page's RTL base direction and its edge
punctuation moves: «[w3b-review] Rendez-vous au consulat — confirmer la date» is drawn «Rendez-vous au consulat —
confirmer la date [w3b-review]» at 1440 and «Rendez- [w3b-review] vous au consulat…» at 320; «Note de test (lane 6,
revue).» is drawn «.Note de test (lane 6, revue)» (`P1-ar-1440-nowpanel-crop.png`, `reflow/P1-ar-320-top.png`). The
order a screen reader reads is right; the order a reader sees is not — on the panel that carries the most urgent state.
The same gap waits in the lists: `templates/portal/dashboard.html` l.168 (`deadline.title`), l.187 (`message.subject`),
l.257 (`document.label`), `templates/companies/dashboard.html` l.136 (`message.subject`). *Fix* (the review's M2 —
one change): the takeover's words get `dir="auto"` and the partial emits `dir` whenever the presenter sets one, with
`.db-now__title[dir], .db-now__text[dir]` hugging their box on the reading edge as `[lang]` does; `dir="auto"` on those
four `.db-list__title`, as `card.html` already does; a test that draws the Arabic takeover and asserts the attribute.

**2 · major · W3-B — WCAG 2.5.3 (A) in Arabic: the conditions gate's primary is named with words it does not show.**
`_now_acts` gives «Accepter les Conditions» the `aria_label` «Accepter les Conditions d'utilisation». In French,
English and Italian the name begins with the visible words; in Arabic the visible label is «قبول الشروط» and the name
«قبول شروط الاستخدام», which does not contain it (live on `qa-person`, `desk/P1-ar-1440.json`, `phone/P1-ar-390.json`:
the focus stop is announced «قبول شروط الاستخدام»). A speech-input user saying the words on the button may not reach
it; the team cannot word the Arabic catalogue to fit. *Fix:* the review's M1 removes this button (the primary becomes
«Consulter» with the register's own note) and the label with it. If the button stays: drop the `aria_label` (the visible
words are the name) and give the longer wording as `aria-describedby`.

**3 · minor · W3-B — Under a coarse pointer, the link inside an empty line stays 28 px.** `.db-empty a` (the bridge's
«Commencer l'orientation», the Academy fold's «Academy» when there is no enrolment) has a 2 px padding and no
`pointer: coarse` rule: 28–29 px tall on touch, where `_dashboard.css` §8 says «every link of the page is 44 px tall
(SP-8)» and plan §1.8 gives every control a 44 px hit area under a coarse pointer. WCAG 2.5.8's inline exception covers
it: the plan's rule, not a failure. *Fix:* add `.db-empty a` to the `pointer: coarse` rule
(`display: inline-flex; align-items: center; min-block-size: var(--hit-primary)`, or the padding that makes 44), or
reword the comment to except the inline links.

**4 · minor · W3-B — The needs register reflows when the web font arrives late (CLS up to 0.015).** The company's rows
share subgrid columns and the end column is `auto`: «Demo — Agenzia per il lavoro autorizzata (fictive)» (capped at
15 rem) re-wraps when Host Grotesk replaces its fallback, the end column grows 189 → 240 px, the need's meta line
re-wraps in the narrower first column and the rows under it drop 16 px (`perf/shifts.json`: 3 of 6 cold loads on the
dev server, 0.0046–0.0148; the before/after series 5 of 7, ≤ 0.0153; the merge base ≤ 0.0005). On the twin, where the
font is preloaded and lands before the first paint, 0 on 20 loads. Under the flagship gate (0.05), over the swap target
(0.01) when it happens. *Fix:* a fixed end track on `.db-tasks--needs` (e.g. `grid-template-columns: minmax(0, 1fr) auto
minmax(0, 15rem)`), so no swap can resize the shared columns; the person's register (`auto` end columns too; one
0.0144 load in ar 1440 out of 7) can take the same rule.

**5 · minor · W3-A (the shell; reported, not W3-B's diff) — In forced colours, focus on the current entry is
invisible.** The rail's and the phone bar's current entry («Tableau de bord», `aria-current="page"`) is drawn at rest
with the same 2 px Highlight inset outline as the focus ring: focusing it changes **0 pixels** at 1440 and 390, on every
dashboard (`forced-rail/compare.png`; 40 of the 862 forced-colours stops). *Fix (W3-A):* draw the current state another
way under `forced-colors: active` (a 3 px `border-inline-start` in CanvasText, or an underline) and keep the outline for
focus alone.

**6 · minor · W3-B (optional) — The NowPanel's name drops whose move it is.** The section is
`aria-labelledby="db-now-title"`: heading and region navigation announce the obligation («Diplome ou titre de
formation») without the eyebrow that says it is «Votre prochaine action» or «Prochaine étape». *Fix:* give the eyebrow
an id and label the region with both (`aria-labelledby="db-now-eyebrow db-now-title"`); the h2 stays the obligation.

**7 · minor · the merge step — CSS +761 B gzip over DL54-73's ceiling.** Inside §2.6 item 5's once-only raise
(≤ 2 KB), whose conditions (LCP and the first render no worse) the twin and the lane's before/after meet; the merge step
records the raise in DL54 as DL54-81 asks, and W3-C / W3-E's deletions (624 B + 866 B, the implementer's measure) bring
the console page types back under.

## Observations (no finding)

- **O1 (W3-A):** at desktop widths the shell sets only `scroll-padding-block-start`: a control Tab brings up from below
  lands flush with the viewport's bottom edge and its ring's lower edge is cut (1 of 526 stops in the normal walk at
  1440, 4 of 862 in forced colours; the control itself fully in view — not a 2.4.11 failure). A
  `scroll-padding-block-end: var(--s-4)` beside the phones' `4rem 5.5rem` would keep the whole ring.
- **O2 (the Performance Lead):** the interaction proxy on these pages (h1 click + Tab, CPU ×4) is 32–104 ms median on
  the twin against V4's < 16 ms — already 32–80 ms on W3-A's twin of the pre-W3-B dashboard, unchanged by W3-B on the
  lane's before/after; under the 200 ms INP budget.
- **O3:** the phone bar appears mid-page in the 320 × 640 full-page captures — fixed elements drawn where they stand in
  the first viewport; not a layout fault.

## Clean-up

The nine minted sessions revoked; the two lane-only accounts deleted with everything they owned (their role grants stay
in the lane's audit trail); the lane server and the twin stopped (8786 free); the merge-base export, the twin's static
root and the browser profile removed; the evidence scanned for cookie strings (0 hits). Nothing written into the
worktree but this file.
