# V5.24 lane CLOSING — the reviewer's targeted gate (label `v524-closing-qa`, 7 November 2026, 10:20–12:00)

Reviewed: branch `v524-closing`, worktree `C:/tmp/ile_wt/v524-closing`, **committed head `f9b70cfa`** on `design-v5` `88caed4a`
(= `design-v5` HEAD, the v524-plat merge; no rebase needed). Gate: `FINAL_DELIVERY_V2.md` §3.9 «Gate (reviewer)» items (1)–(6), the
committed work order's hygiene, and — binding above the work order — **V5.29's «CLOSING GATE CORRECTIONS» (owner, 7 Nov 09:41)**, whose
six items are «GATE ITEMS (each unmet item is a CLOSING BLOCKER for the reviewer and the fix round)». V5.25 §2 / V5.28 (targeted, never
the matrix; no re-scoring), V5.20 (no test loosened), R6, R12, R14.

Machine discipline (R12): lane server **8786** on database lane **l8** (`ile_v5_l8`, the lane's own launcher
`.work/v524-closing/tools/run_8786.py`, `--noreload`, the committed tree), started 10:21, **stopped at the end**; pytest one run per
database on `test_ile_v524_closingqa`, `_b`, `_c`; headed Chromium (`chromium-1234`) under **`CHROMIUM_LOCK_A`**, label
`v524-closing-qa`, 10:32 → 10:45, **released**; every other browser run headless (no slot). Nothing in any repository was changed by
this review (`git status` of the worktree empty before and after; two `npm run build` runs rewrote the dist byte-identically). Logs: `.work/v524-closing-qa/logs/`; frames and probes:
`evidence/v524/closing/qa/`.

## 0. Verdict

**FAIL — 7 blockers (B1–B7), 5 minors.** The lane's own work holds where the §3.9 gate looks at it — the 30 cuts are proven dead
(re-derived by the reviewer from the raw coverage, not read from the NOTES), the legacy pages render as before but for the fade-up
(and better: the base leaves chapter heads at opacity 0 after a fast scroll, the lane draws them at rest), every recorded ceiling of the
named guards equals its measure (recomputed), the catalogue is 100 % with no fuzzy, HANDOFF_V2's primitives all exist. It does not merge
as it stands because:

- **B1** two reds the lane itself introduced (guards of a removed rule and of a converted rule — green on the base, red on the lane);
- **B2–B4** three of the owner's 09:41 gate items are unmet: shell.js 4 866 > 4 700 with its ceiling not restored (B2), main.css's
  headroom 59 B (B3), two of the nine carried reds still red (B4: the side sheet's night foot [fr], the phone row [fr]);
- **B5** the committed `docs/design-v5/FINAL_DELIVERY_V2.md` names the private sentinel table's location (the first tracked file to do
  so) against the owner's 11 Oct rule and before a push to a PUBLIC repository;
- **B6** (gate item 2) follows from B1: a guard around the removed rules is red;
- **B7** one more red on the tree, not the lane's: `test_console_shell_w3_a.py` reads a portal Arabic rule PLAT converted to the
  subject form (red on the base `88caed4a` too) — V5.29 wants CLOSING to leave 0 reds, so it is CLOSING's.

F2-m1 (gate item 4) was not done; under R6 it is recorded as **P2 with the base's figure beside it — not a blocker** (m1).

## 1. Gate item (1) — the coverage report: every removed rule unused everywhere — PASS

Re-derived independently from `.work/v524-closing/cov/results.jsonl` (the lane's raw CDP rule usage) against the frozen start
snapshot `distA` (49 CSS bundles), not from `coverage_report.json`'s verdicts:

- **Scenarios: 2 034, 0 errors** — 2 000 × 200, and the intended 14 × 404, 14 × 403, 2 × 400, 2 × 500, 2 × 429 (the error pages and
  specimens). By kind: wid 576 · per 276 · pub 248 · perw 138 · perrm 138 · rm 128 · fc 128 · dark 128 · land 64 · pr 64 · fine390 64
  · post 40 · err 34 · nav 8. fr and ar at 1440 (202 each) and 390 (170 each), plus 9 other widths, it/en at 1440.
- **Every route in both languages and both widths:** all 114 fr/ar public pages of the lane's crawl (57 routes × 2, gated routes
  open on l8) are present at 1440 AND 390 (0 missing).
- **All 30 removed rules checked (more than the 20 asked):** for each, every selector occurrence of its unproducible token in every
  bundle the report lists for it — **125 rule × sheet pairs, 0 used in any of the 2 034 scenarios**; the four `.lg\:col-*` found in
  `main.css` and unused. Across all 49 bundles, the only used occurrences of the same tokens are inside three rules the lane KEPT
  (`_reveal.css`'s `:is([data-parallax], .bande-foto__frame)` ×2 and `:is(.registro__glyph, …)`, the portal registers'
  `.reg-page :is(.form-field__help, .form__required-note)`) — a rule used anywhere was kept. Method control: a known-used rule
  (`.chapter__head` in `cms/lettura.css`) is found used by the same offset reconstruction.
- **Unproducible:** `git grep` over templates, JS sources and Python for the 18 tokens → 0 producers (`forum-form__required-note` is
  another class). The only non-CSS references are tests — and one of them READS a removed rule: B1(a).

## 2. Gate item (2) — the targeted modules and the guards — FAIL (B1); the ceilings equal the measures — PASS (gaps: m2)

**Run** (`test_ile_v524_closingqa`, 23 min): the eight named modules (`test_chapter_marks`, `test_journey_w3_d`,
`test_frontispiece_v515_c`, `test_pages_v522_p1`, `test_home_v522_h`, `test_sezioni_v522_s`, `test_typography_v2`,
`test_rm_flag_parity`) + the guards around the cuts and conversions (`test_mobile_rtl_w4_a`, `test_o14_lint`, `test_forms_v515_b`,
`test_icons`, `test_css_tokens_exist`): **758 passed, 1 failed** — `test_mobile_rtl_w4_a.py::test_the_page_only_sheets_hold_the_rest`.
A grep of every test for every removed or converted selector found the second: `test_lume_v512_a.py` → **16 passed, 1 failed**. Both
**pass on the base `88caed4a`** (2 passed, same runner): they are the lane's.

**Ceilings = measures (recomputed by the reviewer, gzip -9 of the committed dist / of the build record):**

| Guard | Result |
|---|---|
| `main.css` in the 7 modules that hold it | 32 657 = measure 32 657 |
| `test_frontispiece_v515_c.py` SHEETS (16) and PAGE_TOTALS (12, from the served pages' links) | all 28 equal (home 61 260, landing 53 647, interior 53 009, pathways 55 619, reading 53 917, forum 47 021, glossary / term / living 54 061, network 54 770, promoter 54 787, fraud 54 208) |
| `test_pages_v522_p1.py` CEILINGS (10), PAGE_TOTAL | all equal; PAGE_TOTAL 55 619 = the max of the 8 route pages (Parcours) |
| `test_home_v522_h.py` pages.css · hero.css | 11 239 · 10 849 = measures |
| `test_sezioni_v522_s.py` SHEET_CEILINGS (14 pattern sheets) · rise.js | all 14 equal · 1 286 = measure |
| `test_fonts_budget_v2.py` files · mono pair · set | equal (19 208 · 14 096 · 16 128 · 1 748; 9 960; 61 140) |
| not at measure | INCREMENTS (panorama 716 vs 576, passage V2 1 229 vs 1 225), fonts' PAGE_CEILINGS (browser), the five chunk letters — m2 |

## 3. Gate item (3) — the legacy pages render as before but for the fade-up — PASS

Headed, under the slot, fr at 1440 and 390, the lane (8786) beside the base (the preview 8780 serving `88caed4a`), full-page frames
after a slow scroll down and back: the questionnaire's start and a step page, **the result page** (driven through the wizard on each
server), the news list and a published article (lane only: the base's database has no live article — 404), the privacy policy and the
note legali, the contact form, Entreprises with its `#formulaire`, the institutions' proposal form, the Forum registration (closed).

| Check | Lane | Base |
|---|---|---|
| overflow · h1 · console errors | 0 · 1 · 0 on all 22 frames | 0 · 1 · 0 |
| `[data-rise]` rows / held at opacity 0 after the scroll | **0 / 0** everywhere | the Entreprises `#formulaire` head (1440 and 390), the questionnaire's head (390), the result page's heads and prose (3 at 1440, 5 at 390) still at opacity 0 |
| pixel / DOM diff | only the database's gates: the footer's three legal links + «Actualités» (+32 px at 1440, +128 at 390), the «Partenaires» door on Entreprises (+160 at 390), the note legali's test text | — |

Beyond these, the pixel diffs are sub-pixel only (a breadcrumb chevron's antialiasing, 4 × 4 px; a decorative ground line mid-draw,
one frame of an animation in flight); the forms' bodies (fields, rail, consent, actions) are unchanged. The fade-up's
removal is the only behavioural change, and it removes a base defect (content stuck invisible under a fast scroll).

## 4. Gate item (4) — F2-m1's figures with the base's beside them — NOT DONE (m1, P2 per R6)

No trim and no paired 8782 measure on this tree. The lane changed no keyboard-tier rule and no modality rule (0 `data-input` lines in
the source diff), so R6's standing record applies, in R6's words: **the first Tab within 200 ms in all four cells (160 · 176 · 128 ·
168 ms); the desktop pointer after the keyboard over on the lane and on the base alike (216 · 248 against the base's 176 · 208) — P2
recorded with the base's figure beside it, not a blocker, not a P0/P1.** The trim and its measure move to the matrix, whose INP cells
measure per R6.

## 5. Gate item (5) — the catalogue — PASS

`scripts/i18n_audit.py` (read-only, no `--sync`) on the committed tree: it / en / ar / fr **3 746 msgids, 3 746 translated, 0
untranslated, 0 fuzzy, 0 obsolete — 100.0 %** each; `grep '#, fuzzy'` 0 in the four `.po`. `tests/i18n/test_arabic_completeness.py`
+ `test_locked_renderings_v524.py` + `test_catalogues.py`: **111 passed, 1 skipped** (the environment-bound skip: the dev board is not
served under the test settings). `ARABIC_BURNDOWN` gone, `KEEP_SOURCE == {}`, `DEFERRED_WHOLE` empty (asserted). The consent caption on
`/ar/contact/formulaire/` renders in Arabic beside the French wording (`lang="fr"` label, `.locked-caption` in the box's help).

## 6. Gate item (6) — HANDOFF_V2.md read once — PASS (inaccuracies: m3)

Every primitive and attribute it names exists in the tree as named: `.sez` with `data-sec` (23 patterns in use — all the named ones),
`data-ground` paper · stone · pietra · brand · night · photo, `data-rhythm`, `_materia.css` with `data-luce="origine"`,
`data-sfuma` stone · paper · brand · night, `data-incastro`; `.sez-raccordo` (`--risale`, `--notte`, `data-verb="draw-y"`,
`--sez-raccordo`, `--raccordo-x` read with a fallback in `_materia.css`); `.sez-plate`, `.sez-stretch`, `.sez-tile--sm/--lg`,
`.sez-disc`, `.sigillo--body`, `.protezione__campo`; `data-sec-state`, `data-sec-js` (indice · mappa · flow · spia · racconto);
`initBrandKey`; the seven motion tokens with the stated values and the five easings; the twelve type steps; the mono seat list
(`.ws-case__ref` corrected); `.locked-caption`, `SOURCE_ROUTES`, `DERIVED_ROUTES`; `TYPOGRAPHY_EXCEPTIONS`; `reveal-mark`,
`data-rise`, `_chapter_head.html`. The tools table matches `evidence/v524/TOOLS_AVAILABILITY.md` (design-critique / design-handoff
«no», never named as used).

## 7. The committed work order — FAIL (B5)

`docs/design-v5/FINAL_DELIVERY_V2.md` is byte-identical to the director's file (LF, 0 CR). No phone number, no e-mail address, no
private-table value (checked in process against the configured table; values never printed — 0 hits, also in HANDOFF_V2 and the
NOTES). **But line 218 writes the private sentinel table's full local path** (`ILE_CONFIDENTIAL_SENTINELS=` followed by the path of the
private documents folder). At the base no tracked file names it (`git grep` 0); the repository's own rule (owner, 11 Oct 2026,
`d1a91610`; `.env.example:161` writes `<file outside the repository>`) states the confidential material's location without a recipe,
and `origin` is PUBLIC — once merged and pushed, removal costs a history rewrite.

## 8. V5.29 «CLOSING GATE CORRECTIONS» (owner, 7 Nov 09:41) — each unmet item a CLOSING BLOCKER

| Item | Result |
|---|---|
| 1. shell JS ≤ 4 700, the test ceiling restored to 4 700 | **UNMET — B2.** `static/js/dist/shell.js` 4 866 B gzip -9; `test_motion_v512_a_w2.py:122` still `<= 4_866`. Not in the lane's NOTES |
| 2. main.css meaningful headroom below 32 716, ratchet to the measure | **UNMET in the reviewer's judgement — B3.** 32 712 → 32 657 (−55 B), ratcheted (7 modules); headroom **59 B** ≈ one small rule. Of the classes the owner named, duplicate declarations, unused tokens and superseded protection styles were not addressed; 193 rules of `main.css`'s own sources are unused in all 2 034 scenarios and kept only because their token appears in a live file |
| 3. the nine known reds → 0 | **UNMET — B4** (and B1 adds two). Headless on the committed head: the home's one-system ×2, the whole home browser module (incl. round 2's French runs ×6), Lume's glyph, the three FAQ content-page tests, the side sheet's slide → **50 passed**; **2 failed, identical on the base**: `test_browser_w2_c2.py::test_the_side_sheet_ends_on_its_night_foot[fr]` («the primary on one line»: 2 lines in a 371 px column at 1024) and `test_header_fits_the_narrowest_viewport.py::test_the_name_and_the_menu_button_share_the_phone_row[fr]` («Menu» 2.3 px past the column at 369, `/fr/parcours/`). The test_icons stroke red is fixed in the product (non-scaling sprite strokes confirmed in `components.css` §2) |
| 4. ARABIC_BURNDOWN / KEEP_SOURCE → 0 | MET (§5) |
| 5. no `uv` | MET (0 calls in the repository) |
| 6. dead old editorial styles removed, coverage-proven | MET (§1) |

## 9. Further runs on the committed head

- `tests/compliance`, `tests/security` (with the private sentinel table, in process), `test_check_ownership`, the document-count and
  design-inventory tests, `apps/enquiries`, `apps/consents`: **569 passed** (`test_ile_v524_closingqa_c`).
- `ruff check .`: All checks passed. Changed files: 80, all `i/lf w/lf`.
- **The non-browser sweep** — `tests/frontend`, `apps/pages/tests`, `apps/cms/tests` minus the modules of §2 (`test_ile_v524_closingqa_b`,
  61 min): **2 908 passed, 2 failed, 1 skipped, 2 xfailed** — `test_lume_v512_a.py::test_the_page_says_it_once_in_words_written_by_the_template`
  (B1b, the lane's) and `test_console_shell_w3_a.py::test_the_bar_s_words_are_the_live_labels_whole_and_never_under_the_scale_s_floor`
  (`no rule for ':lang(ar) .console-bottom__item'` — **red on the base too**, from the v524-plat merge `47838596`: B7). The skip is the
  environment-bound one (`ILE_WHATSAPP_NUMBER` unset, option B); the two xfails are the standing strict markers.
- The modules nearest the lane's Python and CSS changes (home, services, locked split, pathways services, FAQ views, form components,
  design docs, Lume ×2, motion budgets, materia, platform, fonts): **390 passed, 1 failed** (B1b again); `apps/pathways/tests`: **101 passed**.
- `npm run build` twice: exit 0, the 80 dist files' sha256 identical between the two builds and equal to the committed dist (`git status`
  empty after both).

## 10. Blockers — must be fixed before merge

| # | Where | Defect | Fix |
|---|---|---|---|
| B1a | `tests/frontend/test_mobile_rtl_w4_a.py:159` | asserts `.linea__more a { display: inline-block;` in `_pathways.css`, a rule the lane removed — red on the lane, green on the base; by the lane's own criterion («dead rules a test reads are kept») it should have been kept or the test restated | restate under V5.20 (the stand-alone link's floor moved to `.traversata__altro a` with lane P1's «la traversata», an approved decision already cited at `:362`): assert that rule's `display: inline-block` where it lives and that no live template carries `linea__more` (equal or stronger), citing §3.9 a and the coverage report |
| B1b | `tests/frontend/test_lume_v512_a.py:200` | `_rule(lume, ":lang(ar) .lume-veil__word")` no longer matches after the subject-form conversion (`lume.css:249` `.lume-veil__word:lang(ar)`) — red on the lane, green on the base | read the subject-form selector (same invariant: Arabic letter-spacing 0), citing R1 / TYPOGRAPHY_V2 (every Arabic type rule in the subject form) and the probe's zero-change proof |
| B2 | `static/js/src/shell.js` (+ the inlined `nav.js`), `tests/frontend/test_motion_v512_a_w2.py:122` | shell.js 4 866 B > 4 700; the ceiling not restored | V5.29 09:41 item 1 as written: CSS-only key where possible, reuse the shell's page-ready / interaction state and reduced-motion handling, delete duplicated / dead shell code; restore the ceiling to 4 700 (never raise); keep the accepted key behaviour |
| B3 | `main.css` sources | headroom 59 B | V5.29 09:41 item 2: surgical cuts of the named classes (re-declared declarations of one context, custom properties nothing reads, superseded protection styles, obsolete chapter / layout helpers), each proven by coverage + V5.20 A/B (0 unintended differences), the 193 coverage-dead rules of `main.css`'s sources checked against their real producer; ratchet to the new measure and report the headroom |
| B4 | the side sheet at 1024 [fr]; the phone row at 369 [fr] | two carried reds still red (identical on the base) | classify each under V5.29 item 3: A (a real defect — text past the column at 369 is «broken mobile»; a wrapped primary in the sheet) → fix in the product without reopening the accepted navbar width / brand scale; B only if an approved V5.29 change made the expectation obsolete → restate with the new invariant, cited |
| B5 | `docs/design-v5/FINAL_DELIVERY_V2.md:218` | names the private sentinel table's local path | replace the path by a placeholder (`<the private sentinel table, outside the repository>`) — the only edit to the copied work order, recorded as such |
| B6 | gate item (2) | a guard around the removed rules is red | closes with B1 |
| B7 | `tests/frontend/test_console_shell_w3_a.py:701` | `_rule(phone, ":lang(ar) .console-bottom__item")` finds nothing since PLAT wrote the rule in the subject form (`.console-bottom__item:lang(ar)`) — red on the base `88caed4a` as well, missed by the PLAT review | restate the selector to the subject form (same invariant), citing R1 / TYPOGRAPHY_V2 and PLAT's conversion (V5.20: an approved decision) |

## 11. Minors (recorded; not blocking)

- **m1** F2-m1 not done (§4) — P2 per R6, carried to the matrix.
- **m2** Ceilings not at their measure: `test_sezioni_v522_s.py` INCREMENTS (716 → 576, 1 229 → 1 225) — a one-line ratchet; the fonts'
  PAGE_CEILINGS need a browser measure (fonts unchanged); the chunk letters (indice 1 536 / 1 238, mappa 1 536 / 1 037, flow 1 331 /
  605, spia 1 024 / 806, racconto 922 / 408) are §7.2 letters, the work order re-records rise.js only.
- **m3** HANDOFF_V2.md: rise.js «1 294» — the measure and the ceiling are 1 286 (gzip -9 as the test measures); `data-rhythm`
  «band|moment» omits `strip` (14 template uses, styled); `--t-field` has no `-lh`.
- **m4** NOTES §8 «§1's 33 cuts» against §1's 30.
- **m5** `test_content_pages_browser_w3_f2.py:77` keeps `.fronte__wide img` in its probe list — the rule and its markup are gone; it
  matches nothing (harmless; drop it with a citation when the module is next touched).

## 12. Scores

No six-dimension re-scoring (V5.25 §2, V5.28: no repeated scoring). The checked legacy surfaces carry 4 on every dimension as «not
re-scored — render-as-before check only»; their gate result is §3's PASS.

## 13. Housekeeping

Lane server 8786 stopped (the launcher and its child). Slot `CHROMIUM_LOCK_A` released at 10:45. No repository file written; no push,
no tag, main untouched.

## After the one improve round (`v524-closing-improve`, head `ff0e3067`) — the verdict as the workflow returned it, verbatim

```json
{
  "pass": true,
  "summary": "CLOSING review: 8 blockers, all fixed in the one improve round (ff0e3067): the two lane-introduced reds restated (subject form / la traversata), shell.js 4 866 → 4 648 under the restored 4 700 (the key CSS-only), main.css 32 712 → 32 105, the side sheet and the phone row fixed in the product, the work order copy names no private location, the console shell red restated; minors recorded.",
  "review": [{"page":"Questionnaire start /fr/orientation/ (1440, 390)","composition":4,"motion":4,"imagery":4,"interaction":4,"institutional":4,"coherence":4,"note":"Not re-scored: no repeated scoring under V5.25 §2 / V5.28, so 4 is a placeholder. Render-as-before check PASS: 0 overflow, one h1, 0 console errors, no rise. Th"},{"page":"Questionnaire step + result page (1440, 390)","composition":4,"motion":4,"imagery":4,"interaction":4,"institutional":4,"coherence":4,"note":"Not re-scored. Driven through the wizard on the lane and on the base. Identical except the gated footer. On the base, 3 to 5 heads and prose blocks stay at opac"},{"page":"News list + published article /fr/actualites/… (1440, 390)","composition":4,"motion":4,"imagery":4,"interaction":4,"institutional":4,"coherence":4,"note":"Not re-scored. Lane only, because the base database has no live article (404). Clean render: 0 overflow, one h1, 0 errors, no rise."},{"page":"Legal pages: privacy policy, note legali (1440, 390)","composition":4,"motion":4,"imagery":4,"interaction":4,"institutional":4,"coherence":4,"note":"Not re-scored. Same as the base apart from the database's test text and the gated footer links. The only other pixel difference is a sub-pixel chevron."}],
  "minors": [{"severity":"minor","where":"tests/frontend/test_mobile_rtl_w4_a.py:159 (apps/pathways/static/pathways/_pathways.css)","detail":"FIXED in the one improve round: Red introduced by the lane. The test asserts `.linea__more a { display: inline-block;` in _pathways.css, but the lane removed that rule as one of its 30 cuts. It fails on f9b70cfa and passes on base 88caed4a. The lane's own crit","fix":"Restate the test under V5.20. The stand-alone link's touch floor moved to `.traversata__altro a` with lane P1's «la traversata», an approved decision already ci"},{"severity":"minor","where":"tests/frontend/test_lume_v512_a.py:200 (static/css/v5/lume.css:249)","detail":"FIXED in the one improve round: Red introduced by the lane. `_rule(lume, \":lang(ar) .lume-veil__word\")` matches nothing since the lane converted the rule to the subject form `.lume-veil__word:lang(ar)`. It fails on the lane and passes on the base.","fix":"Read the subject-form selector. The invariant is unchanged (Arabic letter-spacing 0). Cite R1 / TYPOGRAPHY_V2 (every Arabic type rule in the subject form) and t"},{"severity":"minor","where":"static/js/dist/shell.js (sources static/js/src/shell.js + nav.js); tests/frontend/test_motion_v512_a_w2.py:122","detail":"FIXED in the one improve round: V5.29 09:41 gate item 1 is unmet. shell.js measures 4 866 B gzip -9 against the required ≤ 4 700, and the test ceiling is still 4 866 instead of being restored to 4 700. The lane's NOTES do not mention it.","fix":"Do it as V5.29 item 1 says: keep the accepted key behaviour, make the key CSS-only where possible, reuse the shell's page-ready / interaction state and its redu"},{"severity":"minor","where":"main.css sources (static/css/*.css, static/css/v5/*.css imported by main.css)","detail":"FIXED in the one improve round: V5.29 09:41 gate item 2 is unmet in the reviewer's judgement. main.css went from 32 712 to 32 657 B (−55 B) and is ratcheted in 7 modules, which leaves 59 B under the hard 32 716: about one small rule. The owner asked for MEANIN","fix":"Make surgical cuts of the named classes: declarations re-declared later in the same context, custom properties nothing reads, superseded protection styles, obso"},{"severity":"minor","where":"tests/frontend/test_browser_w2_c2.py::test_the_side_sheet_ends_on_its_night_foot[fr]","detail":"FIXED in the one improve round: Carried red, still red on f9b70cfa and identical on the base. The test expects the primary on one line, but it takes 2 lines in the 371 px column of the 1024 px sheet. V5.29 item 3 requires the nine known reds to reach 0.","fix":"Classify it under V5.29 item 3. If it is A (a real defect), fix the product without reopening the accepted navbar width or brand scale. Only if an approved V5.2"},{"severity":"minor","where":"tests/frontend/test_header_fits_the_narrowest_viewport.py::test_the_name_and_the_menu_button_share_the_phone_row[fr]","detail":"FIXED in the one improve round: Carried red, still red and identical on the base. «Menu» runs 2.3 px past the column at 369 px on /fr/parcours/. That is text past the column on a phone, which falls in the blocking class 'broken mobile'. V5.29 item 3 applies.","fix":"Fix it in the product (A) without reopening the accepted brand scale: for example the row's gap or padding arithmetic at ≤ 369 px. Restate the test only if an a"},{"severity":"minor","where":"docs/design-v5/FINAL_DELIVERY_V2.md:218","detail":"FIXED in the one improve round: The committed copy of the work order writes the private sentinel table's full local path in the ILE_CONFIDENTIAL_SENTINELS line. It is the first tracked file to name that location (git grep finds 0 at the base). The owner's 11 O","fix":"Replace the path with a placeholder such as `<the private sentinel table, outside the repository>`. Record it as the only edit to the copied work order."},{"severity":"minor","where":"tests/frontend/test_console_shell_w3_a.py:701 (apps/portal/static/portal/v5/_shell.css:1148)","detail":"FIXED in the one improve round: A red on the tree that is not the lane's. `_rule(phone, \":lang(ar) .console-bottom__item\")` finds nothing because the v524-plat merge (47838596) wrote the rule as `.console-bottom__item:lang(ar)`. It is red on base 88caed4a too,","fix":"Restate the selector to the subject form with the same invariant (Arabic ≥ 14 px, font-size 0.875rem). Cite R1 / TYPOGRAPHY_V2 and PLAT's approved conversion un"},{"severity":"minor","where":"Gate item (4), F2-m1 (R6)","detail":"Not done: no trim of the keyboard-tier guards or of H's modality rule, and no paired 8782 measure. The lane changed no keyboard or modality rule, so R6's standing record applies. The first Tab is within 200 ms in all four cells (160 · 176 · 128 · 168 ms). The ","fix":"Carry the trim and its paired measure (n ≥ 5, desk and phone, fr and ar) to the matrix's INP cells. Record the result in R6's words in the DL entry."},{"severity":"minor","where":"tests/frontend/test_sezioni_v522_s.py INCREMENTS; tests/frontend/test_fonts_budget_v2.py PAGE_CEILINGS","detail":"Some ceilings are not at their measure. INCREMENTS: panorama 716 against a measure of 576, passage V2 1 229 against 1 225. The fonts' per-page fetch ceilings were not browser-measured. The five chunk letters are §7.2 letters, and the work order re-records rise","fix":"Ratchet INCREMENTS to 576 / 1 225. Record PAGE_CEILINGS at a browser measure, or record that the fonts are unchanged."},{"severity":"minor","where":"docs/design-v5/HANDOFF_V2.md §2, §4, §7","detail":"HANDOFF_V2 gives rise.js as «1 294», but the gzip -9 measure and the ceiling are 1 286. data-rhythm is given as «band|moment», which omits `strip` (14 template uses, styled). --t-field is listed with '+ -lh' but has no -lh. Every primitive and attribute it nam","fix":"Correct the three statements."},{"severity":"minor","where":"docs/design-v5/QA/v524/closing/NOTES.md §8","detail":"§8 says «§1's 33 cuts», but §1 records 30.","fix":"Change 33 to 30."},{"severity":"minor","where":"tests/frontend/test_content_pages_browser_w3_f2.py:77","detail":"The probe list still holds `.fronte__wide img`, whose rule and markup are gone, so it matches nothing. Harmless but stale.","fix":"Drop the entry with a citation when the module is next touched."}],
  "new_strings": [],
  "not_done": ["F2-m1 (R6) is carried to the matrix's INP cells (n ≥ 5, desk and phone, fr and ar, paired on 8782), as R6 records it: first Tab within 200 ms in all four cells; desktop pointer-after-keyboard over 200 ms on both lane and base (216 · 248 against the base's 176 · 208), so P2 with the base's figure beside it, not a blocker. This round changed no keyboard-tier or modality rule.","V1 tokens.css: 86 declarations that a later layer re-declares (≈ 683 B gzip) are left as a post-acceptance candidate; each is bound to a DESIGN_SYSTEM_2026 §3 row and to the contrast tests, so it needs a document amendment","79 custom properties nothing reads (for example the seven --tone-*-bg-hover and --shadow-2-dark) are left as candidates; each is named by DESIGN_SYSTEM_2026 or ACCESSIBILITY, or asserted by a contrast or census test","V1 layout helpers among the coverage-dead rules (.zones, .section, .grid, .split, .stack, .measure, .flow, .t-plate, .lead) are kept: they need a producer audit and a DESIGN_SYSTEM_2026 §7 amendment first","pages.services.JURISDICTION_SEGMENTS and jurisdiction_segments() remain in the trust context with no reader (4 msgids); post-acceptance candidate","In a browser without container style queries the CSS key stays still, which is the reduced-motion state (same as the route board's lit lane)","scripts/regen_design_inventory.py reports figures that were already stale before this round (weights of v5/tokens, aliases, buttons, field and chrome; the §13 icon list); the steward's regeneration should handle them","Steward work at the merge: the v524-closing family in OWNERSHIP_V54.json must also cover apps/core/dev.py, apps/pages/services.py, templates/pages/home/_trust.html, the two deleted templates/components files, static/css/{register,components}.css, static/css/v2/tokens.css, static/css/v5/{chrome,base}.css, static/js/src/{nav,shell}.js, locale/* and docs/design/DESIGN_SYSTEM_2026.md; then the DL entry, live_status and CHANGELOG"]
}
```

The improve round fixed the eight blockers the workflow counted (B1a, B1b, B2, B3, B4 ×2, B5 and B7 of the document
above; B6 closed with B1) and m2; the steward's merge (DL54-198) carries m1 (F2-m1, R6: the matrix's INP cells, P2
with the base's figure beside it), m3's two statements left, m4, m5 and the builder's not_done with their owners
(the matrix / after acceptance), and records the four browser reds it restated on the merged tree under V5.20.
