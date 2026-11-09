# Lane CLOSING — cleanup, ratchets, catalogue, handoff (label `v524-closing-build`, 7 November 2026)

FINAL_DELIVERY_V2.md §3.9 (a)–(g), V5.28 §11 (surgical: dead rules, dead JS, duplicates — not an architecture
project), V5.29's leftovers and its 21:25 / 06:10 notes. Branch `v524-closing` from design-v5 `88caed4a` (every v524
lane merged); worktree `C:/tmp/ile_wt/v524-closing`; database lane l8 (`ile_v5_l8` refreshed from `ile_v5`; test
databases `test_ile_v524_closing`, `_b`, `_c`, one pytest per database); lane server 8786 (stopped at the lane's end).
Tools, logs and evidence: `C:/tmp/ile_v5_council/.work/v524-closing/` and `C:/tmp/ile_v5_council/evidence/v524/closing/`.

> **The improve round (label `v524-closing-improve`, 7 November 2026) — §11.** It fixed the review's eight blockers and
> two minors; where its figures differ from §0 and §4 they supersede them: `main.css` **32 105** B (611 B under 32 716),
> `shell.js` **4 648** B under its restored 4 700, the brand key in CSS, every ceiling at the final measure.

## 0. What changed (one screen)

| Item | Result |
|---|---|
| (a) dead CSS | 30 source rules removed, each unused in all 2 034 coverage scenarios AND naming a class no live template, script, module or row can produce; 12 dead rules kept because a test or a documented token reads them; A/B computed styles: 0 differences but the intended ones |
| (b) fade-up | `rise.js` moves no page without a V2 section and no chapter head (the companies' `#formulaire` head included); 1 325 → 1 286 B |
| (c) ratchets | every ceiling of the named guards at its measure (§4); `main.css` 32 712 → 32 657; T's burn-down closed into the rule-by-rule register `TYPOGRAPHY_EXCEPTIONS` |
| Arabic | `ARABIC_BURNDOWN` 7 → 0 and deleted with its mechanism; `KEEP_SOURCE` and `DEFERRED_WHOLE` empty (asserted) |
| reds | the reds carried to CLOSING (DL54-195 … 197, the 06:10 note) fixed in the product or restated on the approved decision under V5.20 (§6) |
| (d) F2-m1 | NOT done in this run (§7) |
| (e) catalogue | `i18n_audit.py --sync --compile`: +0 −0, 3 746 msgids, 100 % in it/en/ar/fr, 0 fuzzy; no new string |
| (f) docs | SECTION_SYSTEM_V2 five errata; DS 2026's PX blocks; NEW `HANDOFF_V2.md`; the work order as `FINAL_DELIVERY_V2.md`; live_status family `v524-closing`; CHANGELOG (Italian) |
| (g) FAMILY_ID | already extended by the stewards (`…|closing|mfix|cifix|sys|brand`): nothing to do |

## 1. The coverage report (§3.9 a)

**Method** (the V5.20 method, extended to every sheet): `tools/cov_all.py` — Chromium (chromium-1234, headless, no slot)
through Playwright, CDP `CSS.startRuleUsageTracking` / `takeCoverageDelta`, every `static/css/dist/**` sheet answered from
the frozen snapshot of the lane's start (`distA`) so the offsets stay those of the sourcemaps (`tools/build_maps.mjs`:
every entry built exactly as `scripts/build_css.mjs` builds it, external sourcemaps, verified identical to the dist).
Every gate open on `ile_v5_l8` (`tools/open_gates.py`: the five legal documents published with the test text, one live
article, one authorised partner, the virtual forum and newsletter flags — test-only content, lane database only).

**Scenarios: 2 034, 0 errors** — `pub` 248 (every public page reachable from the homes plus `core.public_routes`, gated
routes included, and the dev board's page list, fr and ar at 1440 and 390, it/en at 1440; «full»: scrolled, the header's
doors / sheet / popovers, every details / popover / dialog / tab opened, ten Tabs, hover-focus-active forced, the forms'
client validation) · `per` 276 + `perw` 138 + `perrm` 138 (the nine personas' pages, fr and ar at 1440 and 390, 1024,
reduced motion) · `err` 34 (the four error pages, the preview's 404 / 429, an unknown path, the dev board and its
specimens) · `post` 40 (the seven forms + login, password reset, orientation, Entreprises posted empty, fr and ar, both
widths) · `wid` 576 (32 pages × nine other widths) · `land` 64 · `rm` 128 · `fc` 128 · `dark` 128 · `pr` 64 · `fine390` 64 ·
`nav` 8 (a slow real navigation: Lume).

**Criterion** (`tools/closing_report.py`, `tools/strict.py`): a source rule goes only when (1) every occurrence of it in
every dist sheet that bundles its file is unused in every scenario (a bundle that includes the file without an
occurrence of the rule — esbuild merged or dropped it — keeps it), AND (2) every selector of its list names a class / id /
data-attribute no live template, script, Python module or database row can produce (V5.20's producers, dynamic prefixes
included; a BEM token counts anywhere in a live file; a template is live when a convention loads it or a live file or a
test names it, folder-built names included), AND (3) it is a plain style rule. A rule a legacy template still uses fails
(2) and stays: 1 180 rules are unused in coverage but producible — kept (`evidence/v524/closing/unused_but_producible.json`).

**Removed (30)** — `evidence/v524/closing/coverage_report.json` holds each with its sheets and its unproducible token:

| Source | Rules |
|---|---|
| `static/css/v5/_compose.css` | `.destinataires__photo` ×2, `.bande-foto`, `.bande-foto__frame img`, `.bande-foto + .chapter`, `.spazi .registro__text.spazi__text`, `.spazi .registro__glyph` |
| `apps/portal/static/portal/v5/_wizard.css` | `.opts__hint`, `.opts__grid` ×2, `.opt__mark` ×7 (incl. its checked / empty states), `.opts--error .opt` |
| `apps/pathways/static/pathways/_pathways.css` | `.linea__more a` ×2, `.linea__more a::after` |
| `static/css/v5/_fronte.css` | `.fronte__band`, `.fronte__wide`, `.fronte__wide img` |
| `static/css/layout.css` | `.lg\:col-3`, `-4`, `-6`, `-8` |
| `static/css/v5/_pagina.css` | `.chapter__head--quiet` |
| `static/css/v5/field.css` | `.form__required-note` |

**Dead but kept (12)**, because a test or a documented token reads them: `_compose.css`'s `.training-phase*` four
(`test_frontispiece_v515_c.py::test_the_second_time_frame_has_its_own_column_never_over_the_text`), `_sezioni.css`'s
`.sez-keyword` (`test_materia_v524_lib.py`, LIB NOTES §4 (3): «coverage decides» — it decided dead, the test keeps it),
`_glyph.css`'s `.glyph-tile--warm`, `--neutral`, `--solid` (`test_forms_v515_b.py`), `base.css`'s `.t-plate` and `layout.css`'s `.zones` ×2 (their tokens are documented as used, `test_design_docs.py`).
The named candidates `chapter__*`, `section__header`, `he__body`, `reveal-mark` and `_lettura.css`'s glossary rules
were all producible by a live template (the legacy pages, the hero's preserved foot): kept, as §3.9 a says.

**A/B** (`tools/ab_all.py`, V5.20's `ab_styles.py` on the whole dist): 277 page states (every public page fr / ar at 1440
and 390, it / en, the personas' pages, the sheet / door / language popovers, reduced motion, forced colours, the error
pages, five pages at 1024), every element's computed style with its pseudo-elements and custom properties, A = the
lane's start, B = the lane's dist: run 1 (the cuts and the subject forms) 0 real differences; run 2 (+ the icon stroke,
the page parameter) only the intended: `stroke-width` 1.25 → 1.5 px on the large tiles (288 states), the custom property
`--raccordo-x` gone from four rules whose `inset-inline-start` is unchanged (16), noise (8 empty, 1 animation in flight).

## 2. The fade-up (§3.9 b)

`static/js/src/rise.js`: `initRise()` returns on a page without `[data-sec]` (the legal pages, the CMS reading templates,
published news, partners, the questionnaire — where coverage showed the rise was the only motion); `SINGLES` (chapter
head / statement / prose) deleted, so no chapter head rises (the Entreprises `#formulaire` head included; its form body
untouched). The rows of plain lists inside V2 pages keep the rise (the glossary's and AGAMI's disclosures, the sheets
read `[data-rise]`). The two form pages' `reveal-mark` and the portal's `data-rise` untouched (§9.8).

## 3. Typography: T's burn-down closed (§3.9 c)

- 18 descendant-form Arabic rules → the subject form, each proved zero-change by `tools/probe_subject.py` (the old and the
  new selector match the same elements on every Arabic page at 1440 and 390): entrance 2, wizard 1 (`:not(:lang(fr))`
  kept for its specificity), formwork 4, glyph 1, portico 3, receipt 1, steps 1, chrome 3, field 1, lume 1. Two were NOT
  converted: `:lang(ar) .lock__wm` (the wordmark is `lang="en"`: 366 elements differ) and `:lang(ar) .lang-seg__link`
  (each link in its own language) — registered.
- Two dead fallbacks: `var(--t-lead, 1.125rem)`, `var(--u-eyebrow, 0.75rem)` (both declared on `:root`).
- The mono seat list's name: `.doc-workspace__ref` (no template) → `.ws-case__ref` (PLAT NOTES §4).
- `TYPOGRAPHY_BURNDOWN` deleted; `TYPOGRAPHY_EXCEPTIONS` (rule by rule, with reasons) and `test_every_counted_rule_is_a_registered_exception`
  (equality per rule; V5.20 stronger than counts); `test_platform_v524_plat.py` reads the register (its RESIDUES 4 → 3).

## 4. Ceilings: before → after (gzip -9)

Every dist sheet the lane changed (the other 53 are byte-identical):

| Sheet | Before | After |
|---|---|---|
| main.css | 32 712 | 32 657 |
| ecosystem/companies.css · ecosystem.css · institutions.css · pilot.css · universities.css | 8 645 · 4 886 · 9 164 · 9 867 · 7 524 | 8 480 · 4 719 · 9 007 · 9 701 · 7 366 |
| pathways/diplomas.css · index.css · pathways.css · sheet.css · training.css | 9 398 · 10 637 · 4 621 · 10 182 · 9 290 | 9 225 · 10 452 · 4 423 · 10 007 · 9 079 |
| pages/css/interior.css · fronte.css · pages.css | 7 986 · 6 048 · 11 246 | 7 842 · 5 995 · 11 239 |
| portal/situation.css | 2 243 | 2 033 |
| core/forms.css · glyph.css · portico.css · receipt.css · steps.css · sezioni.css | 5 603 · 1 571 · 2 993 · 1 406 · 2 316 · 11 810 | 5 600 · 1 571 · 2 989 · 1 400 · 2 314 · 11 806 |
| orientation/wizard.css · forum/forum.css · cms/lettura.css · accounts/entrance.css | 5 846 · 7 866 · 6 551 · 4 845 | 5 837 · 7 849 · 6 543 · 4 844 |
| js/dist/rise.js | 1 325 | 1 286 |

The ceilings recorded at these measures (`tools/ratchet.py`, never up; the table of every ceiling old → new in
`.work/v524-closing/logs/ratchet.json`): `main.css` in the six modules that hold it; `test_frontispiece_v515_c.py` SHEETS
and PAGE_TOTALS (home 61 260, landing 53 647, interior 53 009, pathways 55 619, reading 53 917, forum 47 021, glossary /
term / living 54 061, network 54 770, promoter 54 787, fraud 54 208 — each under its §7.1 letter); `test_pages_v522_p1.py`
CEILINGS and PAGE_TOTAL; `test_home_v522_h.py` pages / hero; `test_sezioni_v522_s.py` SHEET_CEILINGS and rise.js;
`test_fonts_budget_v2.py` the files, the mono pair and the set (fonts unchanged; the per-page fetch ceilings are the
browser's and stay).

## 5. Arabic: the burn-down at zero (V5.29 21:25 note)

- HOME's two rows: `pages.services.build_pathways` reads `index_entries(lang=…)` — the titles' provisional Arabic, the
  descriptions' pointer line off their page, each part its own `lang`; `DEFERRED_WHOLE` empty.
- CLOSING's five rows: the consent wordings stay French (the record keeps what the box shows; never translated) and are
  identified by the locked layer's caption as the box's help text (`enquiries.forms.consent_caption`): the companies'
  consent on its two source routes, the acknowledgement (which opens that prescribed sentence) on its own forms
  (`cms.locked_renderings.DERIVED_ROUTES`: contact, institution and university proposals).
- `tests/i18n/arabic_allowlist.py` without the table; `test_arabic_completeness.py` without the mechanism and with
  `test_the_burn_down_is_closed` (no table, `KEEP_SOURCE == {}`, `DEFERRED_WHOLE` empty); `test_locked_renderings_v524.py`
  asserts the pathways' whole key rendered. tests/i18n + enquiries + consents + pathways: 578 passed, 1 skipped.

## 6. The reds (06:10 note; DL54-195 … 197)

| Red | Treatment |
|---|---|
| `test_icons.py` thinner hand (`.sez-tile--lg .icon` 1.25) | product: the rule deleted — the sprite's strokes are non-scaling, so 1.25 drew 1.25 px; the large tile now draws the one 1.5 px hand (SYS's own stated aim was ≈ 1.6 px drawn) |
| `test_css_tokens_exist.py` page parameter declared | product: four sheets wrote `--raccordo-x`; they now write `inset-inline-start` (computed position identical, A/B) |
| `test_browser.py` home system (`.integrita__domanda` 15 < 17; the 14 px band body; no French run) | test restated (V5.20, V5.29 §4 / §6 and R7′): the question at exactly the ui step, never larger than its answer, ≤ 500; the compact band's body at the 14 px floor; any French run LTR |
| `test_home_browser_v522_h.py` round 2 French runs (6 widths) | test restated (R7′): the colophon's answer off its page is the Arabic pointer line, RTL; the caption measure for a French label |
| `test_home_v522_h.py` the stage's texts | test restated (R7′, the HOME contract): titles Arabic, descriptions the pointer line |
| `test_console_shell_browser_w3_a.py` Lume glyph ink / weight | test restated (V5.29 SYS ink, PLAT `--w-title`): read from the role tokens |
| `test_typography_v2.py` / `test_platform_v524_plat.py` (the burn-down) | §3 |
| `apps/faq/tests/test_views.py`, `test_interior_v522.py`, `test_interior_w3_f1.py` (PUB2's) | green on this tree (no change needed) |
| `test_content_pages_browser_w3_f2.py` (three: the FAQ's glyphs, its Latin heads) | test restated (V5.29 §10–§13 the explorer's per-question glyph tiles counted apart; R7′ the FAQ questions Arabic, measured where left, not required) |
| the other PUB / LIB / motion browser modules | green (204 tests, `logs/t_reds_b2.log`) |

## 7. F2-m1 (R6) — not done in this run

The trim of the library's keyboard-tier guards (`:root:not([data-input="key"])` ≈ 150 elements restyled at the flip,
`--sez-t` 39) and lane H's one modality rule, with its paired 8782 measure against `v522/p2` (n ≥ 5, desk + phone, fr +
ar), was not reached: the coverage, the A/B passes and the reds' suites took the run on this machine (the targeted
pytest modules run 10–25 min each beside the other sessions). R6 stands as recorded at DL54-185: the first Tab within
200 ms in all four cells (160 · 176 · 128 · 168 ms), the desktop pointer after the keyboard over on the lane and on the
base alike (216 · 248 against the base's 176 · 208) — **P2 recorded with the base's figure beside it, not a blocker**.
The `improve-animations` survey and the trim are carried to the matrix / gate's fix round.

## 8. Tools → decision → change (real provenance, V5.27 §6)

| Tool (real) | Decision | Change |
|---|---|---|
| Chromium via Playwright, CDP rule-usage coverage (`tools/cov_all.py`, after `.work/v520-css/tools/coverage_async.py`) | a rule goes only if unused everywhere AND unproducible | §1's 33 cuts |
| V5.20 `ab_styles.py` (via `tools/ab_all.py`) | the cuts and conversions must not move a computed style | 0 unintended differences |
| Chromium probe (`tools/probe_subject.py`) | the subject form only where it matches the same elements | 18 conversions, 2 registered |
| `scripts/i18n_audit.py --sync --compile` | the single catalogue pass | +0 −0, 100 % |
| `improve-animations` | not used (F2-m1 not reached, §7) | — |

## 9. Checks run on this tree

`ruff check .` 0; two CSS builds identical (dist committed); `test_confidential_material.py` in process with the
private sentinel table (values never printed) + `test_design_docs.py` + `test_css_bundle_is_current.py` +
`test_css_tokens_exist.py` 226 passed; the gate's targeted static modules (`test_chapter_marks`, `test_journey_w3_d`,
`test_frontispiece_v515_c`, `test_pages_v522_p1`, `test_home_v522_h`, `test_sezioni_v522_s`, `test_typography_v2`,
`test_rm_flag_parity`, `test_icons`, `test_materia_v524_lib`, `test_platform_v524_plat`, `test_fonts_budget_v2`,
`test_layout`, `test_interior_w3_f1`, `test_legacy_token_shim`) green after the fixes; the i18n set 578 passed; the
browser modules of the reds green (see the steward's targeted run for the PUB / LIB browser batch, `logs/t_reds_b2.log`).

## 10. Post-acceptance candidates (R14, not fixed)

- 1 180 rules unused in coverage but producible by a live template: a template-level cleanup (the questionnaire,
  community, news, consents) would free more bytes; out of CLOSING's scope (no re-composition of legacy pages).
- `static/css/dev/specimen-imagery.css:76` `.spi .foto__credit` (dev sheet, PX NOTES): dead, left.
- The academy attendance reference outside the mono seat list (registered residue).

## 11. The improve round (label `v524-closing-improve`, 7 November 2026) — the review's blockers and minors

The reviewer's eight blockers and two minors of `f9b70cfa`, each fixed on the lane's branch (the commits
`e7a97057` … the round's last), targeted checks and targeted tests only; nothing loosened, no new scope (R14).

| # | Finding | Treatment |
|---|---|---|
| B1 | `test_mobile_rtl_w4_a.py:159` read `.linea__more a { display: inline-block; }`, a rule the coverage pass removed | test restated (V5.20; SECTION_SYSTEM_V2 §3.9 «la traversata», lane P1's approved decision, and §3.9 a, the coverage report — the rule's own comment said this pass «retires the rule and its guard»): the rule cannot come back, no live template / script / module draws `linea__more`, Formation's two ways further are `.link-arrow` (`training.html`), whose `display: inline-flex` and 44 px `::after` under a finger stand in `buttons.css`; the floor itself stays measured in the browser (`PUBLIC_TARGETS`) — stronger |
| B2 | `test_lume_v512_a.py:200` read `:lang(ar) .lume-veil__word` | test restated (R1, TYPOGRAPHY_V2 — every Arabic type rule in the subject form; `tools/probe_subject.py`'s zero-change proof, §3): the subject form read, the descendant form asserted absent |
| B3 | `shell.js` 4 866 B against the owner's 4 700 (V5.29 09:41 item 1) | **4 866 → 4 648 B**, the ceiling **restored to 4 700** (`test_motion_v512_a_w2.py`). The key's turn left the script: `nav.js`'s `initBrandKey` (WAAPI through `play()`) is gone and the turn is CSS only, in the lock-up's own section (`static/css/v5/chrome.css` §1): `@keyframes brand-key` with the accepted shape (−16° at 14 %, 364° at 80 %, 360°; `--motion-key`; `--ease-enter` → `--ease-turn` → `--ease-enter` as literal curves), played while the latch `--lock-turn` is on — `@property` on the layered mark `.lock-sig` (no transition of its own, so the link keeps its colour transition and its keyboard tier 0), on at once on the brand's `:hover` / `:focus-visible`, off `--motion-key` after the pointer or the focus left, on for the page's first style (`@starting-style`: the brand's reveal) — through a style query (`@container style(--lock-turn: 1)`, the route board's idiom), fill `backwards` (V5.20: nothing stays applied after the turn), all under `prefers-reduced-motion: no-preference` and `:root:not(.rm)` (the existing gate; `--motion-key` is zeroed there too). Dead shell code out with it: the layout request's «forced» flag (`layout()` takes no argument), `lead()`'s unread return, the nav's `is-enhanced` class (no sheet reads it), the spotlight's `.page-links__link` (no template draws it). Probed headless on 8786 (fr / ar, 1440 / 390): the reveal turns once; a hover turns; a pointer that leaves mid-turn lets it finish; a second pass during the turn does not restart it; at rest and with the focus held after the turn `getAnimations()` is empty; a Tab focus turns it; under reduced motion and `html.rm` nothing moves. A browser without container style queries keeps the key still (the reduced-motion state), as the route board's lit lane. Tests restated: `test_brand_shell_v529.py::test_the_key_alone_turns_once_through_the_gate` (the same invariants read on the CSS, plus «no script turns the key» and «no transition on the link»), the 4 700 ceiling |
| B4 | `main.css` 32 657: 59 B under the hard 32 716 — not the «meaningful headroom» of item 2 | **32 657 → 32 105 B: 611 B of headroom** (the key's CSS paid for inside it). (a) **Duplicate declarations** — the 45 V2 values (`static/css/v2/tokens.css`: the mineral and midnight palettes, the accent, the error / seal / pending steps, the eleven sizes, the six durations) that a later top-level `:root` of the cascade re-declares (`v5/aliases.css`, `v5/tokens.css`, `v4/tokens.css`): never computed, −365 B; the design showcase (`apps/core/dev.py`), the one reader of those literals, now prints the effective cascade — its own promise and the strict xfail's stated fix (`test_design_showcase.py`: the marker dropped, the assertion is the test). (b) **Dead V1 selectors** — the 193 coverage-dead rules checked against their real producer: the jurisdiction bar (`register.css`, 20 rules) and the institutional banner (`components.css` 7 + `v5/base.css` 1) were kept only because their tokens appear in their own templates, `components/jurisdiction.html` and `components/institutional_banner.html`, which no live template includes (comments name them; the council's UI inventory already marked the banner DEAD): the two components left with their rules, −410 B; DS 2026 amended (§1.2, §1.4's hatch exception, §2, §4.5, §8.7, §10 «51 file», §3 `--cooperation` → riserva), the catalogue synced (−1: «Répartition des responsabilités le long du parcours»; 3 745 msgids, 100 % it / en / ar / fr, 0 fuzzy). (c) **Superseded protection styles** — none in `main.css`: the protection band is page-only (`_sec-lastre.css`, SYS's current band; the sill and the bookend left with SYS). (d) **Unused tokens** — 79 names nothing reads, every one bound to DS 2026 / ACCESSIBILITY or a contrast test (`test_v5_tokens.py`, `test_static_assets.py`): recorded as candidates (below), not cut. **Proof:** the cut rules are in the coverage report's unused set (all 2 034 scenarios) with no live producer; the V2 values are overridden in the one cascade; the V5.20 A/B (`tools/ab_all.py`, 277 page states, A = `f9b70cfa`'s dist, B = this dist, `--lock-turn` ignored as a new registered name): see §11.2 |
| B5 | `test_browser_w2_c2.py::test_the_side_sheet_ends_on_its_night_foot[fr]` (the primary on two lines at 768) | **class A, fixed in the product**: Typography V2's coarse-pointer step-up sets the French call at 17 px — 299.5 px of words, 373.5 px with the large button's 24 / 20 sides in a 371 px column. The sheet's block primary takes the medium sides (20 / 16) from 48rem (`chrome.css`; its words are centred, the sides only matter when the call is long): one line in fr, it, en, ar (probed); the accepted navbar width and brand scale untouched; the test green unchanged |
| B6 | `test_header_fits_the_narrowest_viewport.py::test_the_name_and_the_menu_button_share_the_phone_row[fr]` («Menu» 2.3 px past at 369) | **class A, fixed in the product**: the phone step-up sets «Fermer» at 16 px, so the button is 91.9 px (88.6 when the row's arithmetic was written) and 227.5 + 12 + 91.9 > 329. The row's minimum air is 8 px under 48rem (`chrome.css`): the end zone stands on the column's end (`margin-inline-start: auto`), so wherever 12 px fitted nothing moves (the A/B: the gap's value and the auto margin only), and at 369 the air is 9.7 px; the lock-up's scale untouched; the test green unchanged |
| B7 | `docs/design-v5/FINAL_DELIVERY_V2.md:218` named the private sentinel table's local path | replaced by `<the private sentinel table, outside the repository>` — the **only edit** to the copied work order; `git grep` finds 0 private locations |
| B8 | `test_console_shell_w3_a.py:701` read `:lang(ar) .console-bottom__item` | test restated (R1 / TYPOGRAPHY_V2 F-7, PLAT's approved conversion merged at `47838596`): the subject form read (Arabic ≥ 14 px, `font-size: 0.875rem`), the descendant form asserted absent |
| m1 | F2-m1 (R6) not done | **carried to the matrix's INP cells** (n ≥ 5, desk + phone, fr + ar, paired against `v522/p2` on 8782) and recorded in R6's words: the first Tab within 200 ms in all four cells (160 · 176 · 128 · 168 ms); the desktop pointer after the keyboard over on the lane and on the base alike (216 · 248 against the base's 176 · 208) — **P2 with the base's figure beside it, not a blocker**. This round changed no keyboard-tier guard and no modality rule (the key's rules read `:root:not(.rm)` and `:hover` / `:focus-visible`, never `[data-input]`) |
| m2 | ceilings not at their measure | `INCREMENTS` 716 → **576**, 1 229 → **1 225** (`test_sezioni_v522_s.py`); the fonts' per-page bytes **measured in Chromium** (headless, the woff2 resources' encoded bytes as the browser tests read them, 12 public pages fr + ar and a person's console): Latin public **20 956**, Latin console **23 644**, Arabic public **37 084**, Arabic console **39 772** — `PAGE_CEILINGS` at the measure (and a new check that they stand under the TYPOGRAPHY_V2 letters), `test_browser.py` 30 916 → 20 956 (the home fetches no mono any more, asserted), `tests/i18n/test_rtl_browser.py` 47 044 → 37 084 |

### 11.1 Measures (gzip -9) and ceilings

| | Before the round (`f9b70cfa`) | After |
|---|---|---|
| `static/css/dist/main.css` | 32 657 | **32 105** (611 B under 32 716) |
| `static/js/dist/shell.js` | 4 866 | **4 648** (ceiling 4 700, restored) |
| page totals (`test_frontispiece_v515_c.py` PAGE_TOTALS, `test_pages_v522_p1.py` PAGE_TOTAL) | home 61 260 · landing 53 647 · interior 53 009 · pathways 55 619 · reading 53 917 · forum 47 021 · glossary / term / living 54 061 · network 54 770 · promoter 54 787 · fraud 54 208 | home 60 708 · landing 53 095 · interior 52 457 · pathways 55 067 · reading 53 365 · forum 46 469 · glossary / term / living 53 509 · network 54 218 · promoter 54 235 · fraud 53 656 |

Every ceiling recorded at the final measure by `tools/ratchet.py` (only down; the round's interim 32 069 of a WIP
checkpoint was re-recorded at the final 32 105 before the round closed): `main.css` in the six modules that hold it
(`test_forms_v515_b.py` ×2, `test_frontispiece_v515_c.py`, `test_lume_v515_a.py`, `test_motion_v512_a_w2.py`,
`test_pages_v522_p1.py`, `test_home_v522_h.py`), the page totals, `INCREMENTS`, the fonts' page bytes.

### 11.2 The V5.20 A/B of this round

`tools/ab_all.py --a distA_improve --b distB_improve` (A = `f9b70cfa`'s whole dist tree, B = this round's), 277 page
states (every public page fr / ar at 1440 and 390, it / en, the personas' pages, the sheet / door / language
popovers, reduced motion, forced colours, the error pages, five pages at 1024), every element's computed style with its
pseudo-elements and custom properties: 277 compared, 0 errors; the differences, every one
intended or explained: (1) `.lock-sig`'s `transition-property` / `transition-delay` (the latch; 197 states — every
page with the letterhead); (2) `.nav-sheet__primary`'s sides 24 / 20 → 20 / 16 and the `--btn-pad` / `--btn-pad-end` its
icon inherits (113 states ≥ 48rem, B5); (3) `.site-header__inner`'s gap 12 → 8 px (86 states < 48rem, B6) and, with it,
the end zone's auto margin 4 px wider (86): the boxes do not move where 12 px fitted; (4) a read-out, not a style: on
the four language pairs of Le projet and Contact (16 element-states) Chromium's `getComputedStyle` returns «0px» for
the `auto` margins of `.ingresso__inner` / `.ingresso__aside` once the sheet carries a style query (the key's
`@container style()`), where it returned the used 60 / 64 / 38.5 / 32 px — the boxes are identical in A and B (left,
top, width, height probed at fr 1440, fr 390, ar 1440, it / en / ar contact, it le-projet, with the fonts settled),
the read-out comes back when the `@container` rule is taken out, and no script of the product reads a computed margin
(`static/js/src`: 0). The cuts — the V2 values, the two components' rules — move nothing (0 differences of their own).
Noise as the tool classes it: 56 noisy, 63 unconfirmed (a re-read did not repeat them). Logs:
`.work/v524-closing/logs/ab_improve.log`, `.work/v524-closing/ab_improve/ab.jsonl`.

### 11.3 Tools → decision → change (real provenance, V5.27 §6)

| Tool (real) | Decision | Change |
|---|---|---|
| `animate` skill (`~/.claude/skills/animate/SKILL.md` §3 «pick the tool», §6 «interruption and exit») | the reveal is predetermined motion while the page loads → CSS; a hover can be fired twice in a second, and a keyframe restarts from zero → a latch that never restarts a running turn and lets a begun turn finish | the key's turn in `chrome.css` §1 (`brand-key`, `--lock-turn`) |
| Chromium via Playwright (headless, no slot): `latch_probe.py`, `key_probe.py` | the two CSS latches tried on a test page: a discrete `<custom-ident>` in `animation-name` does not run; the style query on a transitioning registered number does — and on the product: reveal, hover, leave, second pass, rest, focus, reduced motion | the style-query latch |
| V5.20 A/B (`tools/ab_all.py` over `.work/v520-css/tools/ab_styles.py`) | the first run showed the latch's `transition-property` on `.brand` replacing the link's own colour transition | the latch moved to `.lock-sig`; the re-run's differences are the intended ones only |
| Chromium probes `probe_rows.py`, `font_probe.py` | the row's and the sheet's arithmetic (the 16 / 17 px step-up), the fonts each page fetches | B5, B6, m2 |
| the lane's coverage report (`evidence/v524/closing/coverage_report.json`, `unused_but_producible.json`) + a producer check | a coverage-dead rule goes only when its producer is itself dead | the jurisdiction bar and the institutional banner |
| `scripts/i18n_audit.py --sync --compile` | the catalogue follows the sources | −1 msgid, 3 745, 100 % |
| `improve-animations` | not used: F2-m1 carried to the matrix (m1) | — |

### 11.4 Checks of the round

- `ruff check .` 0; `manage.py check` no issue; `makemigrations --check` no change; `npm run build` twice: the 81
  dist files identical, the dist committed; `git grep` finds no private location; the catalogue 3 745 msgids, 100 %
  in it / en / ar / fr, 0 fuzzy (`i18n_audit.py --sync --compile`: +0 −1).
- Targeted static modules (one pytest, `test_ile_v524_closing`, `-m "not browser"`; logs/i11_static.log): **2 577
  passed**, 1 skipped (the dev board is not served in the test environment, as at the review), 1 xfailed (the legacy
  shim's planned xfail), **0 failed** — the gate's targeted modules (`test_chapter_marks`, `test_journey_w3_d`,
  `test_frontispiece_v515_c`, `test_pages_v522_p1`, `test_home_v522_h`, `test_sezioni_v522_s`, `test_typography_v2`,
  `test_rm_flag_parity`), every module this round restated, the token / document / showcase / bundle guards
  (`test_v4_tokens`, `test_v5_tokens`, `test_design_docs`, `test_design_showcase`, `test_css_bundle_is_current`,
  `test_frontend_bundle_is_current`, `test_css_tokens_exist`, `test_legacy_token_shim`, `test_static_assets`,
  `test_loader_rules`, `test_overlays`, `test_nav_sheet_w2_c2`, `test_regen_design_inventory`, `test_check_ownership`),
  the home and template guards, `tests/security/test_confidential_material.py` in process with the private sentinel
  table (values never printed), the i18n catalogues, renderings and Arabic completeness.
- Browser modules (headless Chromium, no slot; logs/i8_browser.log, i9_ring.log, i10_browser2.log): the header
  (`test_header_fits_the_narrowest_viewport.py`), the sheet (`test_browser_w2_c2.py`), `tests/frontend/test_browser.py`,
  the Arabic faces (`tests/i18n/test_rtl_browser.py::test_arabic_typefaces_are_applied_and_loaded`), the motion
  (`test_motion_browser_w4_b.py`), the home (`apps/pages/tests/test_browser.py`): **87 passed** — the two carried reds
  (B5, B6) green, and one more red found and fixed on the way: `test_the_account_menu_from_the_night_foot_draws_the_paper_ring[fr|ar]`
  read the glyph at the pre-SYS ink #4a5a62; restated at the approved `--p-inchiostro-600` #4e5b68 (V5.29 §5 / §8, SYS
  `c8d9f0e1`, accepted 6 Nov 19:36; V5.20 — the same invariant, the paper's ink and never the night's). Lume ×2 and the
  mobile / RTL browser module: **44 passed**.

### 11.5 Post-acceptance candidates (R14, not done)

- V1's `tokens.css`: 86 declarations a later layer re-declares (≈ 683 B gzip), every one a row of DESIGN_SYSTEM_2026 §3
  with its literal value and the contrast table's source (`test_static_assets.py`) — a design-document amendment.
- 79 custom properties nothing reads, each named by DESIGN_SYSTEM_2026 / ACCESSIBILITY or asserted by a contrast test
  (e.g. the seven `--tone-*-bg-hover`, `--shadow-2-dark` in the shadow census) — each needs its document or test
  amended with it.
- V1's layout helpers among the 193 coverage-dead rules (`layout.css`: `.zones`, `.section`, `.grid`, `.split`, `.stack`,
  `.measure`, `.flow`; `base.css`: `.t-plate`, `.lead`): no static template writes them, but their names are generic
  words a Python string, a CMS row or a form widget can carry, and DESIGN_SYSTEM_2026 §7 documents them — a producer
  audit and a §7 amendment first (the rest of the 193 are states the crawl did not reach — hover, no-js, the
  departing veil, error and empty states — and stay).
- `pages.services.JURISDICTION_SEGMENTS` / `jurisdiction_segments()`: the bar's data, still in the trust chapter's
  context, read by nothing (four msgids).
- `scripts/regen_design_inventory.py` reports figures stale before this round (`v5/tokens.css`, `aliases.css`,
  `buttons.css`, `field.css`, `chrome.css` weights; §13's icon list): the steward's regeneration.
- Firefox: the CSS key needs container style queries; without them it stays still (the reduced-motion state).
- For the steward (ownership): this round touched, beyond the lane's files, `apps/core/dev.py`,
  `apps/pages/services.py`, `templates/pages/home/_trust.html`, the two deleted `templates/components/` files,
  `static/css/{register,components}.css`, `static/css/v2/tokens.css`, `static/css/v5/{chrome,base}.css`,
  `static/js/src/{nav,shell}.js`, `locale/*/LC_MESSAGES/django.{po,mo}`, `docs/design/DESIGN_SYSTEM_2026.md`.
