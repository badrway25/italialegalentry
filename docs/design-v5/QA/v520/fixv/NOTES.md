# V5.20 final technical gate — lane v520-fixv: the test-change audit's violations fixed in the product, the guards restored

30 October 2026 · branch `v520-fixv` from design-v5 `e2098dd` (tag `v518/green`) · worktree `C:/tmp/ile_wt/v520-fixv` ·
database lane l7 (`ile_v5_l7`, a fresh copy of the preview database `ile_v5`; tests on `test_ile_v5_l7`) · lane server
8787 (the acceptance launcher's personas, outside the repository: `C:/tmp/ile_v5_council/.work/v520-fixv/srv/`).
Binding: V5.20 (`directives/V5_20_FINAL_TECHNICAL_GATE_STRICT_TEST_RULE.md`: the strict test-update rule; «animation
remaining applied after completion», «hard-coded colours bypassing tokens» and unexpected skips are gate items), V5.18,
V5.19, V5.17, V5.15, V5.12. The audit: `evidence/v520/TEST_CHANGE_AUDIT.md` (V1–V13). No visual redesign, no locked
copy touched, no msgid added (the two trail labels are existing msgids, translated in it/en/ar), nothing
machine-translated, no secret, no personal datum and no telephone number written anywhere; production untouched.

## 1 · The violations, one by one

| | Audit | Here |
|---|---|---|
| V1, V2 | main.css ceilings | **lane v520-css** (its own brief: «do not touch main.css budgets»). This lane adds 0 B to main.css (§6). |
| V3 | `MOVING_JS` let a finished `c-rise` through | **restored exactly** (`test_dashboard_browser_w3_b`); the product already fills `backwards` |
| V4 | the home's «nothing loops» counted only running animations | **restored in its strongest form** (`apps/pages/tests/test_browser.py`): any time-based animation still listed fails |
| V5 | the Arabic brand jump | **lane v520-css** (its commit `76d0750`: the mark holds in both directions) — not touched here |
| V6 | the formwork's own 7-value corner set | **product on the scale** (xl · md · full); `FORMWORK_CORNERS` gone, §1.3 over the whole `<main>` again |
| V7 | eight surfaces admitted with ANY shadow | **each admitted surface pinned to its value**, read from the tokens where it stands; selectors scoped |
| V8 | two head surfaces admitted with ANY raised shadow | **pinned to their tokens**, at most one per first screen; the parse that missed `color()` drops fixed |
| V9 | any `.chip` counted as the pill | **restored exactly**; the chip's wrap is fixed in code (lane D) |
| V10 | the WhatsApp URL in any attribute | **lane v520-wa** (`1f600d7`: `whatsapp_link_set_aside`) — not touched here |
| V11 | 4 skips of `/xx/faq/` | **run and assert 200**: the FAQ opened for its case by a fixture |
| V12 | the trail's current crumb «Mon compte» on two pages | **product fixed** (`accounts.shell._page_label`); the two rows restored as at `238dc1c` |
| V13 | the WhatsApp number in test files | **lane v520-wa** — not touched here |
| §6 rows 1–3 | 3 intake skips «no rule in force» | **run and assert** on the seeded ruleset put in force for a demonstration in the test database; the pre-production truth asserted by a new test |
| O59 note | RADII_JS skipped the veil by name | **dropped** (the composed opacity already leaves the warm veil out) |
| O64 follow-up | the check rule's wording | `ICON_SEMANTIC_MAP.md`'s [RT] check rule names the language menu's active item, as `icons.CHECK_BEARING` does |
| §7 | `both` / `forwards` fills on time-based animations | **page-only sheets: all `backwards`**, the held final states moved into their rules (§4); main.css's left to its lane |

### V3 — `tests/frontend/test_dashboard_browser_w3_b.py`

`MOVING_JS` is the audit's exact restoration: every animation in the workspace, `c-rise` included. `c-rise` fills
`backwards` (`apps/portal/static/portal/v5/_motion.css:181`, `static/css/v5/_conto-console.css:36`), so an ended rise
leaves `getAnimations()`; a `both` fill coming back would fail here. The `c-rise` await in `SETTLE_JS` stays (a wait on a
finite animation, O57); its comment no longer says «moving admits it». **29 passed** (the whole file, Chromium).

### V9 — the same file, `GATE_JS`

The radius line as at `238dc1c` (no `.chip` exception): a chip counts as the pill by its drawing. The step chip that
wrapped on a phone keeps «Étape 1 sur 7» on one line since lane D (`72dbf14`, `test_terminology_v512_d`). Same run.

### V4 — `apps/pages/tests/test_browser.py::test_a_finger_on_the_tiles_scrolls_without_a_press_and_taps_with_one`

`return forever || timed;` — a time-based animation still listed fails whether it is running, paused or finished and held
by its fill; finite scroll-driven reveals (V5.15 §6 «section reveals», ViewTimeline) pass; anything infinite fails.
**Passes at HEAD** (no product change needed on the home).

### V6 — the formwork on the corner scale

Measured before (headed Chromium, the three formwork pages × fr/ar × 1440/768/390): inside the formwork 12 · 6 · 8 ·
4 · 6.4 · 999 · 1 px. After: **12 · 6 · 999** (contact form: 12 · 6) — with the targa's 6, three values, as
`tokens.css` asks («at most three distinct radii on a screen at rest»).

| Element | Was | Now | Where |
|---|---|---|---|
| the formwork's buttons (the action, «Continuer», «Précédent») | 4 (sm) | 6 (md) | `.formwork { --btn-radius: var(--radius-md) }` beside its `--field-radius`; `.formwork .btn` reads it in the console too, whose `.console .btn` sets sm |
| the consent's box | 8 (lg) | 6 (md) | a plate with the fields' sheet face: «the plate inside the formwork: 6 px corners» (the sheet's own §5) |
| the review's parts (last step of the two multi-step forms) | 8 (lg) | 6 (md) | the same plate |
| the glyph tiles inside the formwork (sm in the side, md in a step's legend) | 6.4 / 8.8 | 6 (md) | `.formwork .glyph-tile` |
| the section head's lg tile (outside `.formwork`, above it) | 11.2 | 12 (xl) | `.formwork-section__head > .glyph-tile` — the formwork's containers' corner |
| the head rail's bars, the side rail's connectors | 1 px | full | a 2 px bar's round ends: renders the same |
| the panel's light (`::before`, 3 px) | literal `3px` | full | renders the same 3 px |

No element moves; the largest change is under 3 px on a corner (a step legend's tile, 8.8 → 6). The Icon Visual System's 0.2 × side stays everywhere else
(the empty states, the wizard, the entrance): outside V6's scope, an open item for the Director, not a failing guard.

Test (`tests/frontend/test_content_pages_browser_w3_f2.py`): the PROBE line is the audit's restoration
(`if (drawn && v !== '0px') radii.add(v)`), `FORMWORK_CORNERS` is gone, §1.3 applies to the whole `<main>`, and the
«no formwork drawn» presence check stays through `out.formwork`.

### V7 — the content pages' admitted shadows

`V515_RAISED` is now an ordered list of (selector, allowed values); the first selector an element matches is its rule.
Each allowed value is an expression resolved **where the element stands** (a probe appended to its parent takes the
expression, as `test_browser_chips_w1_c`'s `SHADOW_JS` does), so a surface drawing anything else fails
(«an admitted surface off its value»), and a shadow at rest on any other element fails as before. Scoped to the
decisions:

| Surface | Allowed | Decision |
|---|---|---|
| `.fronte-wrap .search-form` | `inset 0 0 0 1px color-mix(--line-structure 30 %)`, `--shadow-3` | DL54-172 |
| `.fronte__wide img` (before `.foto__img`) | the band photograph's print drop, its exact value | DL54-172 |
| `.foto__img` | `--passe-partout` only (was: any shadow on any photograph) | DL54-172 |
| `.formwork__grid` | `--shadow-3` | DL54-173 |
| `.formwork .formwork__panel`, `.formwork .form-field__check` | `inset 0 0 0 1px --line-rhythm` | DL54-173 |
| `.formwork .glyph-tile`, `.formwork-section__head > .glyph-tile` (was: any tile anywhere) | the paper seal (`--line-rhythm` hairline, 1 px light, **`--shadow-1-dark`**) or the night seal | DL54-173 |
| `.formwork .steps-rail__tile`, `.formwork .steps-head__tile` | the hairline (rest), the gold hairline (done), the current tile's gold ring, exact | DL54-173 |

Product: the glyph tile's under-shade `0 1px 2px color-mix(--surface-night 12 %)` becomes **`var(--shadow-1-dark)`** —
level 1's night twin, the 12 % the seal was drawn with (notte-950 for notte-900: under 2/255 per channel at the
shade's darkest pixel; the A/B captures in §3 show no difference above 8/255). The band photograph's drop and the step
tiles' gold ring stay the compositions' own materials, pinned to their exact values (§4).

### V8 — `tests/frontend/test_orientation_browser_w3_f1.py`

- `ADMITTED_RAISED` maps each surface to its token: the head photograph → **`var(--fronte-print)`**, the fraud page's
  notice → **`var(--shadow-3)`**; any other value fails (`wrong`), and **at most one** admitted raised surface stands
  on a first screen (`named <= 1`).
- The raised-shadow parse stripped only `rgba(…)`: a drop drawn with `color-mix()` computes as `color(srgb …)`, so the
  page heads' drops were never counted as raised at all. It now strips every colour function. Checked on the lane
  server: the head photograph counts as raised (`named` 1), a wrong pin is caught, nothing admitted → `raised` 1.
- Product: `--fronte-print` is declared once on `[data-fronte]` (`v5/_fronte.css`) and read by the two head
  photographs that drew it as two literal copies (the audit's duplicate); `test_frontispiece_v515_c` pins its value.
  The other heads' drops (diptych, band, network, arch) are unchanged.

### V11 — `apps/pages/tests/test_contact_channels_v519.py`

`faq_case_open` (`apps/pages/tests/conftest.py`): for the case whose `path` is `faq/`, gate G3 open (`phase3_open`) on
the seeded data, whose locked FAQ `seed_all` already holds; every other case is served as before. The skip became
`assert response.status_code == 200` — a 500 on `/`, `/contact/`, `/le-projet/` or `/agami/` fails too. The file is
lane v520-wa's: the change is two hunks (a decorator line, the skip), and `git merge-tree` with `v520-wa` (and with
`v520-css` + `v520-wa` merged) is clean. **42 passed, 0 skipped** (was 4 skipped).

### V12 — `apps/accounts/shell.py::_page_label`

«Supprimer mon compte» for `accounts:delete_request`, «Se déconnecter» for `account_logout` (existing msgids, translated
in it, en and ar): the trail reads «Espace réservé › Mon compte › Supprimer mon compte», the console bar's title with it.
`test_service_pages_w3_f2`'s two rows are back to their `238dc1c` trail.

### The three intake skips — `apps/cases/tests/test_intake.py`

`demonstration_rules_in_force`: the product's own `manage.py rules_activate_demonstration` in the test database (the
switch `ILE_SEED_DEMONSTRATION_DATA` opened for the test alone): 16 seeded rules through the real chain (four eyes,
verified sources), the approver «DIMOSTRAZIONE — nessun giurista ha approvato questa regola» in every snapshot. On
the pathway the seeded questionnaire reaches (`salaried_work`): 4 rules apply, 3 requirements missing, the outcome
`missing_requirement`, 6 sources each with a precise reference, 3 checklist lines carrying their reference. The three
tests assert their precondition instead of skipping on it. New: `test_with_no_rule_in_force_the_assessment_applies_none_and_cites_nothing`
— the pre-production truth (no rule in force; no rule applied, no source, the questionnaire's own outcome, no legal
checklist line). **23 passed, 0 skipped** (was 19 passed, 3 skipped).

### O59 — `tests/frontend/test_browser_w3_f1.py`

The `.closest('.lume-veil')` skip in `RADII_JS` is gone: the composed opacity already leaves the warm veil (0.002) out,
and a veil left standing over a page at rest is seen, so its corners count.

## 2 · Every test changed, under V5.20's rule

| Test | Change | 1 · decision | 2 · implemented | 3 · invariant | 4 · cited |
|---|---|---|---|---|---|
| `test_dashboard_browser_w3_b` `MOVING_JS` | the `c-rise` exclusion removed | V5.20 (finished animations must not stay applied) | `c-rise … backwards` (lane A) | stronger (as at `238dc1c`) | in the comment |
| `test_dashboard_browser_w3_b` `GATE_JS` | the `.chip` exception removed | V5.20; lane D's one-line chip | `72dbf14` | stronger (as at `238dc1c`) | in the comment |
| `apps/pages` `test_browser` | `forever \|\| timed` | V5.15 §6 (reveals) + V5.20 | — (passes at HEAD) | stronger | in the comment |
| `test_content_pages_browser_w3_f2` | PROBE restored, `FORMWORK_CORNERS` gone, `V515_RAISED` pinned and scoped | V5.15 §18 (shadow hierarchy) for the surfaces; tokens.css §1.3 for corners | §3 | stronger | in the comments |
| `test_orientation_browser_w3_f1` | pinned, at most one, parse fixed | V5.15 §18, DL54-172 | `--fronte-print` | stronger | in the comment |
| `test_frontispiece_v515_c` | new: the print's value | — | `--fronte-print` | new guard | docstring |
| `test_contact_channels_v519` | skip → assert 200, FAQ opened | V5.20 (no skip where the feature can be enabled) | fixture | stronger | decorator + conftest |
| `test_service_pages_w3_f2` | two trail rows as at `238dc1c` | the breadcrumb contract («the last item is the current page») | `_page_label` | stronger | in the comment |
| `test_intake` | 3 skips → asserts; a new pre-production test | V5.20 | fixture | stronger | module docstring + fixture |
| `test_browser_w3_f1` `RADII_JS` | the veil's name-skip dropped | the audit's O59 note | — | stronger | in the comment |

No assertion loosened, no timeout raised, no skip or xfail added, no test removed.

## 3 · Headed Chromium (1440 · 768 · 390, fr · ar)

`C:/tmp/ile_v5_council/.work/v520-fixv/headed/` (`tools/headed_formwork.py`, `tools/headed_console_formwork.py`;
Chromium 1234, headed, lane server 8787, the same server before and after the build):

- **The three formwork pages** (contact, company needs, institutions): every capture differs from its «before» only at
  the corners listed in §1 V6 (110–180 pixels above 8/255 per capture: the action, the consent box, the side's tiles).
  Nothing moves, nothing changes colour; the formwork reads as one family of controls (fields, buttons, plates at 6).
- **The page heads** (FAQ, Glossaire, Diplômes et titres, Attention aux fraudes, Orientation, Formation, Vivre en
  Italie, Entreprises, Le projet): **0 pixels above 8/255** from the shadow changes; the only differences are the
  heads' own drawings caught at another phase (the route's halo, timing).
- **The console's formwork** (the company's «nouveau besoin», persona `qa-company`): radii 12 · 6 · 999 after (4 was
  the button); «Continuer» and the steppers now share the fields' corner.

Verdict: no accepted surface degraded; corner consistency (V5.1 §85) improved where the guard measured it.

## 4 · The audit's §7: finished animations still applied by their fill

V5.20 lists «animation remaining applied after completion» among the release blockers; the audit's §7 named the
time-based animations still filling `both` or `forwards`. Measured, not guessed (`tools/fill_survey.py`, lane server,
21 public pages × fr/ar × 1440/390 scrolled through, five console pages): for every FINISHED
time-based animation still in `getAnimations()`, its animated properties read with the fill as written and again with
`backwards`.

- **Identical at the end** (only the serialisation differs: `matrix(1, 0, 0, 1, 0, 0)` for `none`, `0px` for `none`):
  `formwork-light`, `fronte-rule`, `fronte-node`, `fronte-register(-rtl)`, `fronte-spine`, `reveal-rule`; by their
  keyframes (a `from` alone, or a `to` equal to the element's own style) also `fronte-arrive`, `receipt-ring`,
  `receipt-dot`, `reveal-fill`, `reveal-settle`, `famiglia-in`, `m5-down`, `m5-settle`, `m11-chip`.
- **A final state held by the fill**, different from the element's own: the drawing's line (`fronte-draw`,
  `forwards`: dash offset 0 held over the rule's 1) and the end point's light (`fronte-halo`: opacity 0.45 held over
  0.75 · 1 · 0.4; the contact motif's ring held at 1 over 0.6).

Fixed in the page-only sheets — every finite time-based fill is now `backwards` (V5.18's «backwards, never both»):
`v5/_formwork.css`, `v5/_fronte.css` (12 rules), `v5/_receipt.css` (×2), `v5/_reveal.css` (×4),
`pathways/_pathways.css`, `portal/v5/_journey-rail.css` (×2), `portal/v5/_motion.css`. Where the fill held a final
state, that state moved into the rule that runs the animation, inside its no-preference block (reduced motion is
untouched): the line's dash offset is its own (the keyframes start it at 1 and the backwards fill hides it during
the delay), the light rests at 0.45 in its own style, the motif's nodes and ring keep the opacity 1 the fill held.

A/B at rest (`tools/ab_rest.py`: 14 pages × fr/ar × 1440/390, captured 5.5 s after load, before and after on the
same server): animations held after their end **256 on 48 page states → 0**; the captures show no design difference —
the pixels that differ are the drawings' stroke anti-aliasing (a line no longer kept on its animation's layer:
«AGAMI», «Le projet», «Entreprises», checked side by side in `ab_rest/cmp_*.png`).

**Left as they are, main.css's sheets** (lane v520-css holds the budget at its measure with 0 B headroom; a change
there is theirs to weigh), read from their rules, not measured here: `v5/chrome.css`:837–851, the phone sheet's four
entrance animations, held while the sheet is open (two without a delay can drop their fill, two with one need
`backwards`: ±0 B raw); `v5/loader.css`,
`v5/lume.css`, `v5/_loader-light.css`, the loader's deliberate hold (the audit's own exception); `v5/motion.css`'s
`lume-in` / `lume-out`, bounded by the class that runs them. The scroll-driven `linear both` rules (`_reveal.css`,
`_photo.css`, `fronte-drift`) are out of scope (V5.15 §6, bound to the scroll).

## 5 · What stays outside the hierarchy, and why (the Director's to decide)

- The page heads' print drops (`_fronte.css`: the entrance and the plan → `--fronte-print`; the band, the diptych, the
  network, the arch keep theirs) are lane C's designed materials (DL54-172). Putting them on `--shadow-3/4` would
  visibly change accepted heads; a new global level needs an SH-1 amendment (`test_v5_tokens`: «V5 declares no other
  shadow») and main.css bytes (0 B headroom after v520-css). Here they are single-sourced where two copies existed and
  pinned to their exact value where a guard admits them.
- The step tiles' gold ring is a state indicator (the current step), not an elevation: pinned exactly.

## 6 · Weights

main.css: **unchanged, byte for byte** (33 530 B gzip -9 here, as at `e2098dd`: no main.css source touched, so lane
v520-css's cut stands as measured). The page-only bundles, gzip -9 (Python's zlib, as the budget tests weigh them):

| Bundle | `e2098dd` | here | Δ |
|---|---|---|---|
| `core/forms.css` (≤ 6 KiB) | 5 513 | 5 551 | +38 |
| `pages/css/fronte.css` (≤ 6 KiB) | 5 490 | 5 508 | +18 |
| `pathways/pathways.css` | 5 119 | 5 126 | +7 |
| `core/receipt.css` | 1 403 | 1 406 | +3 |
| `portal/journey.css` | 2 725 | 2 728 | +3 |
| `core/glyph.css` (≤ 2 KiB) | 1 572 | 1 571 | −1 |
| `core/steps.css` (≤ 3 KiB) | 2 317 | 2 316 | −1 |
| `orientation/wizard.css` | 5 847 | 5 846 | −1 |
| `core/reveal.css` | 2 381 | 2 379 | −2 |
| `portal/console.css` | 8 036 | 8 032 | −4 |

## 7 · Runs

Lane l7 (`test_ile_v5_l7`), CI's environment (no `.env` read, CI's placeholders, `ILE_CONFIDENTIAL_SENTINELS` and
`ILE_WHATSAPP_NUMBER` unset), `PYTHONIOENCODING=utf-8`; Chromium under the machine's lock
(`C:/tmp/ile_locks/CHROMIUM_LOCK`, label `v520-fixv`, every session under 25 min).

- **Browser, after every product edit** (`tools/browser_session.sh`):
  - session 1 — `test_motion_v512_a_w2`, `test_journey_browser_w3_d`, `test_browser_v515_c`, `test_browser_w3_f1`,
    `test_reduced_motion_w1_d`, `test_forms_v515_b`, `test_depot_browser_w3_c`: **67 passed**;
  - session 2 — `test_content_pages_browser_w3_f2` (V6, V7), `test_orientation_browser_w3_f1` (V8),
    `test_dashboard_browser_w3_b` (V3, V9), `apps/pages/tests/test_browser.py` (V4), `test_documents_browser_w3_c`,
    `test_browser`, `test_browser_w1_c`: **126 passed**.
- **Non-browser**: `apps/cases/tests/test_intake.py` **23 passed, 0 skipped** (was 19 + 3 skipped);
  `apps/pages/tests/test_contact_channels_v519.py` **42 passed, 0 skipped** (was 4 skipped);
  `test_service_pages_w3_f2` + `test_account_shell_v512_b` **56 passed**; the final batch (`tools/nb_final.sh`: every
  frontend test module that reads a changed sheet or bundle, the changed tests' modules, the shell, the intake, the
  contact channels, the ownership and confidential-material guards; 49 modules): **2 166 passed, 0 failed, 1 skipped**
  (the private sentinel table: `ILE_CONFIDENTIAL_SENTINELS` unset, environment-bound, its reason printed), 1 xfailed (the
  shim's finish line, `test_legacy_token_shim`, an older recorded debt), 192 browser cases deselected (run above).
- `manage.py check`: no issues · `makemigrations --check --dry-run`: no changes · `ruff check .`: all checks passed.
- `git merge-tree` of this tree with `v520-wa`, with `v520-css`, and with the two merged: **clean** (no conflict).

Skips this lane leaves in a CI-style run: none of its own. After the merge with v520-wa the two environment-bound ones
remain, each printing its reason: the private sentinel table (`ILE_CONFIDENTIAL_SENTINELS`) and the configured
WhatsApp number (`ILE_WHATSAPP_NUMBER`).

## Files

- Product: `apps/accounts/shell.py`; `static/css/v5/_formwork.css`, `_steps.css`, `_glyph.css`, `_fronte.css`,
  `_receipt.css`, `_reveal.css`; `apps/pathways/static/pathways/_pathways.css`; `apps/portal/static/portal/v5/_journey-rail.css`,
  `_motion.css`; built (`node scripts/build_css.mjs`): `static/css/dist/core/forms.css`, `core/steps.css`, `core/glyph.css`,
  `core/receipt.css`, `core/reveal.css`, `orientation/wizard.css`, `pages/css/fronte.css`, `pathways/pathways.css`,
  `portal/console.css`, `portal/journey.css` (main.css untouched).
- Tests: `tests/frontend/test_dashboard_browser_w3_b.py`, `test_content_pages_browser_w3_f2.py`,
  `test_orientation_browser_w3_f1.py`, `test_frontispiece_v515_c.py`, `test_service_pages_w3_f2.py`,
  `test_browser_w3_f1.py`; `apps/pages/tests/test_browser.py`, `conftest.py`, `test_contact_channels_v519.py`;
  `apps/cases/tests/test_intake.py`.
- Docs: `docs/design-v5/ICON_SEMANTIC_MAP.md` (the check rule names the language menu, O64); this file.
- Outside the repository: `C:/tmp/ile_v5_council/.work/v520-fixv/` — `tools/`, `headed/`, `ab_rest/`, `fill_survey.json`,
  the run logs (`intake*.log`, `v11.log`, `v12.log`, `b*.log`, `bs1.log`, `bs2.log`, `nb_final.log`), `srv/` (the lane server).
