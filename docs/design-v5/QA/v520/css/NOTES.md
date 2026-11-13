# V5.20 final technical gate — lane v520-css: the shared stylesheet back under budget, the Arabic home's phone menu

30 October 2026 · branch `v520-css` from design-v5 `e2098dd` (tag `v518/green`) · worktree `C:/tmp/ile_wt/v520-css` ·
database lane l5 (`ile_v5_l5`, a fresh copy of the preview database `ile_v5`; tests on `test_ile_v5_l5`) · lane server
8785 (the acceptance launcher's nine personas, outside the repository: `C:/tmp/ile_v5_council/.work/v520-css/srv/`).
Binding: V5.20 (`directives/V5_20_FINAL_TECHNICAL_GATE_STRICT_TEST_RULE.md`: «shared stylesheet over budget» is a
release blocker; «prefer deduplication, dead-rule removal and route-specific loading over simply raising the limit»; the
strict test-update rule), V5.18, V5.8 (shared bundles ratchet down), V5.15, V5.12. No visual change, no locked copy
touched, no msgid added, nothing machine-translated, no secret or personal datum written anywhere.

## 1 · main.css: 33 530 → 32 718 B gzip -9

| | before (`e2098dd`) | after | |
|---|---|---|---|
| `static/css/dist/main.css` raw | 173 813 B | 166 224 B | −7 589 B |
| `static/css/dist/main.css` gzip -9 (Python's zlib 1.3.1, as the budget tests weigh it) | **33 530 B** | **32 718 B** | **−812 B**; 730 B under the old 33 448 line (the cut alone: 32 712; +6 B for §3's anchor rule) |

Every page type pays 812 B less (`.work/w2-a/w2-a-merge/weigh_pages.py e2098dd WT`): interior 33 530 → 32 718, the
login 38 368 → 37 556, the home 48 495 → 47 698 (its page-only `hero.css` +15 B: the Arabic rule of §3), console pages
42 611 → 41 799, the company dashboard 42 800 → 41 988, «Mes pièces» 48 175 → 47 363. No other bundle changed.

### What left main.css — and why nothing on a page can change

1. **Declarations a later declaration always beats (deduplication) — 207.** In one sheet, a declaration is dead when a
   LATER declaration of the same property, in a rule with the SAME selector, either at top level or in the same at-rule
   context, with compatible importance, follows it: same specificity, later in the one cascade, it wins on every element
   at every viewport. `@starting-style` and `@supports` contexts were left alone. Found on the minified bundle, mapped
   back to the sources through esbuild's sourcemap (every custom-property declaration maps to its exact source column;
   checked on all 1 620), cut in the sources:
   - `static/css/v4/tokens.css` — 154 (design V5 re-declares after it almost every name V4 valued: the navy chapter,
     the accent and its gradients, surfaces, shadows, radii, the Plex faces, both type scales, the console layout,
     controls, icons, the z levels, durations and curves, the reduced-motion zeroes);
   - `static/css/v2/tokens.css` — 33 (shadows, voices, line heights and tracking, three space steps, curves, two radii,
     the letterhead's heights and their narrow override);
   - `static/css/_legacy-tokens.css` — 7 names a later layer declares after the shim (`--radius-pill`, `--font-mono`,
     `--utility-height`, `--header-height`, `--ease-standard`, `--z-dropdown`, `--z-skiplink`);
   - `static/css/v2/bridge.css` — 3 (the motion durations), `static/css/v5/tokens.css` — 1 (`--hit-min`, re-pointed by
     `v5/aliases.css`);
   - standard properties restated identically or superseded under the same selector: `base.css`'s first `body` block
     (font-family, size, line-height, opsz, colour — restated by its second `body` block), `h3`'s V1 letter-spacing and
     the caption's line-height (both superseded in `v5/base.css`), the sheet door row's size and line-height
     (superseded 145 lines later in `v5/chrome.css`).
2. **Custom properties nothing reads (dead declarations) — 24 declarations, 19 names.** A liveness pass from every
   reader: any `var()` in a CSS source outside main.css's own sources, any mention in a template, script, Python module
   or data file, any mention in a test, a `var()` in a standard property or an at-rule of main.css; `--a`'s value
   reading `--b` keeps `--b` alive while `--a` is. Removed only when no living design document names the token
   (DESIGN_SYSTEM_2026 — its §17 excepted, rewritten with the shim's countdown —, DESIGN_SYSTEM_V5, ACCESSIBILITY,
   DESIGN_SYSTEM_V2 / V4) and when no declaration that stays reads it: `--chip-pattern`, `--chip-pattern-size`,
   `--chip-fill-kind` (`v5/tokens.css`), `--lume-night`, `--lume-gold` (`v5/lume.css`), `--lume-line-night`
   (`v5/tokens.css`) and thirteen shim names (`--color-white`, the `--color-success` / `-info` / `-warning` /
   `-pending` pairs, `--container-max` / `-wide`, `--font-size-label` / `-button`).
3. **Rules no page can match — 2.** `:root .hero__title[translate="no"]` (`v5/base.css`; no template writes
   `hero__title`) and the shim's `.numeral` class (no template, script or module writes it).

The shim shrank by twenty names and a class: 75 → 55 names, 2 → 1 class; `tests/frontend/test_legacy_token_shim.py`'s
ceilings went down with it (55 · 1 · 151 references — the census, not the 1 515 of 21 September) and
DESIGN_SYSTEM_2026 §17 lost the twenty rows and says why (§2's row too). The error pair `--color-error-fg` / `-bg`
stays: `docs/ACCESSIBILITY.md` §6 names it. Twelve V1 tokens lost their last design-system consumer with these
declarations (`--state-done` / `-info` / `-warn` / `-pending` `-fg` / `-bg`, `--t-ui-size`, `--track-normal`,
`--radius-control`, `--z-dialog`): DESIGN_SYSTEM_2026 §3 now labels them «riserva» with the consumer that left, as its
own definition and `test_reserve_labels_match_the_design_system_stylesheets` require.

**Left on purpose — the steward's candidates, each needing a design-document amendment with it:** 70 more custom
properties nothing reads, kept because DESIGN_SYSTEM_V5 / DESIGN_SYSTEM_2026 / ACCESSIBILITY name them or a kept
declaration reads them (598 B gzip, measured: the palette steps no component reads, the `--popover-*`, `--toast-w`,
`--table-row-h`, `--inspector-w`, loader and journey tokens, `--chip-bg-hover` and the seven `--tone-*-bg-hover`,
`--container-lg` / `-xl` / `-xxl` …; the list: `.work/v520-css/kept_dead_tokens.json`); V1's
`tokens.css` (≈ 470 B gzip of overridden declarations), whose every token DESIGN_SYSTEM_2026 §3 documents with its
literal value and whose contrast table recomputes from it; the documented V1 utilities and components no template uses
any more (`.zones`, `.t-plate`, `.split`, `.lg:col-*`, `.form__required-note`, `components/institutional_banner.html`
and its `.institutional-banner*` rules).

**Route-specific loading — measured, not used.** The coverage (§2) found 36 rules (4 021 B raw) used on console pages
only; most are element rules a public page can also draw (`h4`–`h6`, file inputs, `:read-only`, `[dir=rtl] li`, the
signed-in account seat of the public letterhead), the rest the case file's register (`.outcome*`, `.sources*`,
`.note`). Moving them into `portal/console.css` would put them after main.css in the cascade (a winner can change), and
the console page type's total would rise by the split's compression loss (V5.8 rule 1). With the ratchet restored by
deletions alone, no rule moved.

## 2 · The coverage run (the source of the dead-rule list)

Chromium rule-usage coverage (CDP `CSS.startRuleUsageTracking` / `CSS.takeCoverageDelta`) of the ORIGINAL main.css on
8785, 1 320 scenarios: every public route × fr / it / en / ar × 1440 / 390 (scrolled; the doors at 1440 or the sheet and
its doors below 64rem; every `<details>`, popover and dialog opened; ten Tab presses; hover / focus / focus-visible /
active forced on 260 distinct elements; every form's submit pressed and its fields filled), every persona page of the
index for the nine personas × 1440 / 390, 20 pages × fr / ar × 9 more widths (1680 … 320) and 844 × 390, reduced motion,
forced colours, print, a fine pointer at 390, eight forms posted empty (the server's error state), a real page change
answered 2.2 s late (the Lume veil, the doorway, the key, the light), the error pages, the preview's specimens. **804 of
999 style rules were used; the 195 others (17 753 B raw) are listed one by one in `UNUSED_RULES.md`** with the verdict
of the producer check (templates' class attributes and tag arguments, JavaScript strings and class toggles, Python
strings; the CMS stores escaped text with no `class=`). 189 have a producer — live behaviour the run could not reach (a
signed-in public page, staff and moderator surfaces, an uploaded logo, a leaving toast, disabled controls,
`html.no-js`, a slow navigation's phases, the home sections the CMS can switch on: `pages/home/_{key}.html` is chosen at
run time) — and stay.

## 3 · The Arabic home's phone menu: the brand mark no longer jumps

**Defect** (group P, `QA/v518g/p/NOTES.md`): on the home the letterhead shows the mark alone (Q1, «one name on the
screen»); below 48rem «Menu» opens the sheet, whose head is the letterhead's own row (W2-C2) and drew the whole lock-up.
In French the words grow after the mark and the mark stays; in Arabic the Latin wordmark is a left-to-right isolate
(I18N-06) whose mark is its LEFT end, so the mark landed ~183 px left of where the bar draws it.

**Fix**, two rules, the brand's lock-up order untouched:
- `apps/pages/static/pages/css/hero.css` (page-only, after Q1's own rule): `[dir="rtl"] .page-home .nav-sheet__head
  .lock__text { display: none; }` — in Arabic the home's sheet head keeps the bar's lock-up, the mark alone. French is
  unchanged (its words grow after the mark); from 48rem the side sheet's head draws no lock-up (`v5/chrome.css`).
- `static/css/v5/chrome.css`: `.nav-sheet__head > .brand--lockup { direction: ltr; }` — the head's lock-up anchors as
  the letterhead's does (`v5/motion.css`: «the anchor is ltr, as the lock-up is»). Measuring after the first rule alone
  showed the mark still 6 px off: a mark alone sits in a 44 px target box (`--hit-primary`), at the box's left in the
  bar (ltr) and at its right in the head (rtl). The same 6 px existed on EVERY Arabic page at ≤ 20.5rem (328 px), where
  both rows draw the mark alone; the rule closes both.

**Measured in HEADED Chromium 1234** (`.work/v520-css/tools/headed_sheet.py`, lane server 8785, «Menu» tapped, the
visible mark's box before and after; before = the original bundles answered by route, after = the served files):

| | 320 | 360 | 375 | 390 | 430 | 600 | 768 |
|---|---|---|---|---|---|---|---|
| ar, home — before | 6 px | 183 px | 183 px | 183 px | 183 px | 184 px | 0 (side sheet) |
| ar, home — after | **0** | **0** | **0** | **0** | **0** | **0** | 0 |
| ar, «Le projet» — before / after | 6 / **0** | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 |
| fr, home and «Le projet» — before / after | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 |

Captures (top strip, closed and open, each case): `.work/v520-css/headed_base/`, `.work/v520-css/headed/`;
`headed/ar-home-390-before-after.png` shows the four states. The computed-style A/B of the cut bundle against the final
one (16 scenarios, fr / ar, the home, «Le projet», «Contact», a console page, the sheet open) differs only inside the
sheet's head: the lock-up's `direction` on every Arabic page, and on the Arabic home the hidden words (with the 44 px
box and «Fermer»'s auto margin that follow); nothing in French, nothing on the console.

## 4 · Verification

- **Computed styles, element by element, A/B** (`.work/v520-css/tools/ab_styles.py`): the same page loaded twice on
  8785, main.css answered once from the original build and once from the cut build (Playwright route; everything else
  identical), every element's computed style — itself, `::before`, `::after`, every property, custom properties
  included — hashed after the motion settles (the rise's IntersectionObserver timing normalised: every held block
  risen), plus every custom property main.css declares, read on the root and the body. **267 scenarios** (172 public:
  every route × fr / ar × 1440 / 390, the home and three pages in it / en; 74 persona pages of the nine personas; the
  sheet open, a door open, the language popover open, reduced motion, forced colours; the seven error and state pages),
  **686 609 element and token readings: 0 property differences** beyond the 19 removed custom properties (absent by
  construction). 48 first-pass hash differences were all timing (31 differed between two loads of the same build, 5 did
  not reproduce, 12 re-read in full showed no differing property — the ancestor chain of one photograph whose load
  state differed between the two loads).
- **Pixels** (`.work/v520-css/tools/ab_pixels.py`): 12 pages — the home, «Le projet», «Parcours», «Entreprises»,
  «Contact», the FAQ, the login, the glossary, «Vivre en Italie», the contact form, a person's dashboard and «Mes
  documents» — × fr / ar × 1440 / 390, full page, motion disabled at capture: **47 of 48 pairs pixel-identical** at
  the first pass (cut bundle routed), the 48th the home at 1440 whose hero has a script-timed phase: three captures of
  each build fall into the same three phases, and every capture of the new build is pixel-identical to a capture of the
  original (`.work/v520-css/pixels/recheck/`). One first-pass «Entreprises» pair differed by a photograph not yet
  decoded at capture; its nine re-captured pairs are all 0 px. Against the final served files (§3's two rules
  included; the sheet closed): 46 pairs identical at once, the French home at 390 identical to the original's second
  capture, the Arabic home at 1440 matched capture for capture (0 px) on re-capture, as above.
- **Coverage, the cut never touched a used rule**: the two rules removed were never used by the 1 320 scenarios (§2);
  every other cut is a declaration, not a rule.

## 5 · Tests changed, judged under V5.20's rule

| Test | Change | The rule's four conditions |
|---|---|---|
| `test_forms_v515_b::test_budgets`, `::test_the_empty_state_brings_its_sheet_once_and_main_css_does_not_rise`; `test_motion_v512_a_w2::test_the_budgets_hold`; `test_lume_v515_a::test_the_shared_sheet_s_measured_exception` | main.css ceiling **lowered** to the measure: 33 530 / 33 600 / 33 600 → **32 718** B, cited «V5.20: ratchet restored by dead-rule removal» | V5.20 orders the budget fixed by deletion, never by raising the limit (decision); the bundle is 32 718 B (implemented); a lower ceiling is a stronger invariant; cited in each test |
| `test_legacy_token_shim` | `MAX_SHIM_TOKENS` 75 → 55, `MAX_SHIM_CLASSES` 2 → 1, `MAX_LEGACY_USAGES` 1 515 → 151 (the census) | the file's own rule («LOWER the numbers here in the same commit»); lower ceilings, stronger; cited |
| `test_browser_w2_c2::test_the_sheet_opens_and_closes_on_the_overlay_system[ar]` | was: in Arabic the sheet's head draws the words and its mark is the isolate's left end (group P's description of the defect); now: **the mark does not move in either direction** (`headMark == barMark` for fr AND ar), and in Arabic the head is the bar's row (no words) | the old expectation conflicts with V5.20's explicit item 4 (a visible RTL defect: the brand must not jump); the new behaviour is the fix of §3; the invariant is stronger (French-only before); cited in the test |
| `test_browser_w2_c2::test_the_brand_mark_holds_its_place_when_the_sheet_opens` | **new**: fr / ar × the home and «Le projet» × 320, 360, 390, 430, 768 — the mark holds its place below 48rem, the side sheet draws no lock-up from 48rem | — |

Runs (lane l5, `test_ile_v5_l5`, CI's environment: no `.env` read, CI's placeholders, `PYTHONIOENCODING=utf-8`):

- Browser, under the Chromium lock: `tests/frontend/test_browser_w2_c2.py`, `tests/i18n/test_rtl_browser_w2_c2.py`,
  `tests/frontend/test_header_fits_the_narrowest_viewport.py` — **37 passed**.
- Non-browser, on the final tree: every test file that reads a stylesheet, the design documents, the shim's
  countdown, the tokens, the budgets, the sheet, the overlays, the pipeline, the ownership manifest and the home
  (29 files) — **1 406 passed**, 2 xfailed (the shim's «finish line» and the showcase's strict captions marker, both
  expected), 0 failed. Earlier on this branch, before the documentation pass: `tests/frontend` + `tests/i18n`
  non-browser, 1 302 passed up to the one §17 row-set failure the rewrite of §17 then answered. The machine-wide full
  suites are the final gate's (V5.20: a fresh copy, both halves).
- `manage.py check`: no issues; `makemigrations --check --dry-run`: no changes; `ruff check` on every touched Python
  file: clean.

## Files

- CSS sources: `static/css/v4/tokens.css`, `v2/tokens.css`, `v2/bridge.css`, `_legacy-tokens.css`, `base.css`,
  `v5/tokens.css`, `v5/base.css`, `v5/chrome.css`, `v5/lume.css`; `apps/pages/static/pages/css/hero.css`; built:
  `static/css/dist/main.css`, `static/css/dist/pages/css/hero.css`.
- Docs: `docs/design/DESIGN_SYSTEM_2026.md` (§2 weights and rows, §3 twelve rows now «riserva», §17), this folder
  (`NOTES.md`, `UNUSED_RULES.md`).
- Tests: `tests/frontend/test_forms_v515_b.py`, `test_motion_v512_a_w2.py`, `test_lume_v515_a.py`,
  `test_legacy_token_shim.py`, `test_browser_w2_c2.py`.
- Outside the repository (evidence, tools): `C:/tmp/ile_v5_council/.work/v520-css/` — `cov/` (coverage), `ab_main/`
  (computed-style A/B), `pixels/` (captures), `headed/`, `headed_base/` (the sheet), `tools/`.
