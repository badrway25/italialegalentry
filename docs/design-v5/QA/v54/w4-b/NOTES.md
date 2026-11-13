# W4-B — Motion audit: notes (w4-b-impl-1, 16 October 2026)

Plan §3.6 item 2 (W4-B), §1.5, §2.6, K17; V5.5 delivery mode (implement → review once → fix → ship). Worktree
`C:/tmp/ile_wt/v54-w4-b`, branch `v54-w4-b` from design-v5 `8ab5b89` (integration checkpoint 3). Lane 8 (8788,
`ile_v5_l8`, `ILE_REFERENCE_DATE=2026-10-03`, `DB_CONN_MAX_AGE=0`, `--noreload`, no preview flag); tests on
`test_ile_v5_l8`. Evidence: `C:/tmp/ile_v5_council/evidence/v54/w4-b/`; scratch: `C:/tmp/ile_v5_council/.work/w4-b/w4-b-impl-1/`.
The audit, written before any change: `AUDIT.md` (this folder). The decisions: DL54-153 (DL54-132 on the branch,
renumbered at the merge, after design-v5's DL54-132 … DL54-152).

## 1. What changed

| # | Finding (AUDIT.md §10) | Fix | Commit |
|---|---|---|---|
| F2 | The Motion library (`motion` 13.4.1) on every page type (a 26.5 KB gzip chunk), still called by shell.js's reveal and «Ma situation»'s question change; the home's script 51 249 B gzip against §2.6's 45 KB | `situation.js` on `play()` (the Web Animations API through motion.js's gate); shell.js's reveal deleted (F1); `motion.js` without the re-exports and the JS springs; `npm uninstall motion --package-lock-only --ignore-scripts` (with it `framer-motion`, `motion-dom`, `motion-utils`, `tslib`; no `node_modules` touched); `test_frontend_bundle_is_current.py`'s Motion-exports test rewritten (the helpers exported; no source, package file or bundle carrying the library); the JS dist rebuilt from clean | `a401d4f` |
| F1 | `[data-reveal]` (shell.js), `.reveal` (components.css §29) and `main.js`'s `initReveal` / `initCounters` hide text until a script shows it; no page carried any of them | all deleted, with `.counter`; DS 2026 §12, §16 and A11Y §7 updated; the inventory figures regenerated | `8a920e8` |
| — | W2-C1's A11Y_PERF item 5: `nav.js` and `hero.js`, each imported by one entry, were entries themselves (a chunk + a stub nobody loads: one script request too many) | `scripts/build_frontend.mjs`'s `INLINED` list: inlined into `shell.js` and `home.js`; the bundle test follows the list | `ec7b935` |
| F3 | The rail's fold transitions `inline-size` and `padding-inline-start` (R10; the properties law) | instant: the two transitions leave `_shell.css` | `9ddfe39` |
| F4, F5 | The portico animates from the keyboard (Esc's exit, the chevron, the architrave's fade); the skip link slides 120 ms on Tab | one `html[data-input="key"]` rule in `chrome.css`; the skip link's transition leaves V1 `base.css` | `7901a7a` |
| O2 (W3-D) | Forced colours: the current page wears the focus ring's outline at rest | the lit Highlight disc and, in the rail, the word underlined | `55efe3e` |
| m4 (intfix) | The overlay's resize re-read had no behavioural test | a resize step beside the 400 % test | `00bc0d4` |
| — | The audit's outcomes pinned in a browser | `tests/frontend/test_motion_browser_w4_b.py` (7 tests; 5 fail on design-v5's tree) | `ffb4f7e` |
| — | The record | DL54-153; DS 2026 §12's audit paragraph; `docs/design-v2/FRONTEND_DEPENDENCIES.md` | `b124e3f` |

The m2 / m3 answers ride in `8a920e8` (the static test `tests/frontend/test_single_submit_w4_b.py`; `initMisc`'s comment).

## 2. Measures

**Script per page type, gzip -9** (the steward's measure of DL54-101: the import closure of the entries a page's
template loads, + `main.js` + `head.js`, + `rail-pref.js` on console pages; `.work/w4-b/w4-b-impl-1/jsweigh.py`,
`evidence/v54/w4-b/jsweigh/`):

| Page type | Before (design-v5 `8ab5b89`) | After | Script requests |
|---|---|---|---|
| the home | 51 249 B | **24 138 B** (−27 111) | 9 → 7 |
| a public page (door, interior, error) | 43 674 B | 16 781 B (−26 893) | 7 → 6 |
| an entrance page (login, sign-up, reset) | 45 351 B | 18 462 B (−26 889) | 8 → 7 |
| a console page (dashboard, registers) | 46 070 B | 19 178 B (−26 892) | 9 → 8 |
| «Ma situation» | 47 292 B | 20 415 B (−26 877) | 10 → 9 |
| «Mes pièces» (served, with the drawer's dynamic imports at load) | 54 412 B | 27 520 B (−26 892) | 12 → 11 |

§2.6's «a public page ≤ 45 KB» (46 080 B) holds on every page type; no page's script grew; the request ratchet (over
by one since DL54-101) holds. No bundle carries the library: its identifiers (`staggerChildren`,
`spring-duration-limit`, `value-not-animatable`, `resolveKeyframes`, `transformPerspective`, `MotionValue`, …) are in 1
file of design-v5's dist and in 0 of this branch's — and `test_frontend_bundle_is_current.py` now holds it.

**Shared CSS** (gzip -9, V5.8 — the ratchet only goes down): `dist/main.css` 35 483 → **35 391 B** (−92, every page);
the console page type (main + console + portal) 44 196 → **44 052 B** (−144); every page sheet unchanged.

**«Ma situation»'s question change, before → after** (a per-frame sampler of both questions' computed opacity and
transform, 1440 and 390, fr and ar; `evidence/v54/w4-b/audit-base/situation-*.json` → `step1-head/`):

| | Motion (design-v5) | `play()` (this branch) |
|---|---|---|
| the leaving question | opacity 1 → 0 in 120 ms (Motion's default ease-out: the `easing:` option it was given is Motion One's name, ignored) | 1 → 0 in 120 ms, `--motion-fast`, `--ease-enter` |
| the arriving question | starts at 122–136 ms; one frame at full opacity before its animation; opacity 0 → 1 and 16 px → 0 in 200 ms (`x`, a JS frame loop) | starts at 132–134 ms, no flash; opacity 0 → 1 and `translateX(16px)` → 0 in 200 ms, `--motion-standard`, `--ease-enter`; −16 px in Arabic |
| the whole change | 336–352 ms | 331–349 ms |
| at half its clock, the arrival | opacity 0.76, x 5.2 px | opacity 0.93, x 1.9 px (the enter curve, front-loaded) |
| afterwards | inline styles committed, then scrubbed a frame later | no `style` attribute, no animation holding a question |
| under reduced motion | swapped at once | swapped at once, no animation created |

**R10, the rail's fold** (the dashboard at 1440, n = 5, frames timed by `requestAnimationFrame`, layout from a trace;
`evidence/v54/w4-b/rail-r10/`): CPU × 1 — 15 frames in 260 ms, gaps 16.7 ms; CPU × 4 — 8 frames, gaps 67–117 ms, 45 ms of
layout a press over 7 layouts; CPU × 4 with `contain: layout` on the workspace and the rail — 9.5 frames, gaps 50–117 ms.
Not 60 fps → instant, as R10 rules. After: the rail is 64 px in the press's own task (`test_motion_browser_w4_b.py`).

**O2, forced colours** (the current entry shot at rest and focused from the keyboard; `evidence/v54/w4-b/forced-focus/`):
pixels changed by the focus — before 0 / 0 / 0 / 0 (fr 1440, fr 390, ar 1440, ar 390); after 1 060 / 508 / 1 060 / 620.

**O3, `[open]` toggles in the console** (the person's dashboard at 390, CPU × 4, «Où j'en suis» opened by script and by a
tap, n = 3; `evidence/v54/w4-b/o3/head.json`): the style recalculation touches the disclosure's own 112 elements (of 574 on
the page), with or without the two `html:has()` rules left (`html:has(.site-header)`, `html:has(body.console)`); a tap adds
15 + 2 elements (the input's modality and `:active`), not the document; longest task 20–41 ms. W3-D's 390 elements were
`html:has(.console-drawer[open])`, which left with W2-A (`e5fa845`). Nothing to fix.

**Motion at rest and at load, after**: the audit's 68 loads and the extra probes run again on this branch (`evidence/v54/w4-b/audit-head/`, `extra-head/`) differ from design-v5's in exactly what was fixed — the rail's `padding-inline-start` / `width` transitions gone, the portico's exit, chevron and architrave fade gone after Esc, the skip link's slide gone (and the loose piece's alert dialog now drawn: 320 ms in, one 80 ms opacity under the setting) —; nothing new at load anywhere; in the console nothing at load but the entrance release; at rest 0 running animations and 0 `will-change` on every load; 0 console errors (the 404 page's own 404 apart) and 0 CSP reports.

## 3. Hand-offs to W4-B — each answered

| From | Item | Answer |
|---|---|---|
| intfix REVIEW m2 | the catch is the one release only while every guarded form submits through a `.btn` | a static test of the premise — `tests/frontend/test_single_submit_w4_b.py`: the project's guarded forms and the templates they include submit only through `button.btn` (no `<input type=submit>`), allauth's button element renders a `.btn` (`button.html`, `button__manage.html`), allauth's packaged templates write no raw submit control; a mutation to a plain button fails it. Not the other option (a release on shell.js's early return): it would drop the double-submit refusal for any such form |
| intfix REVIEW m3 | `initMisc`'s comment names loader.js as the only lifter | it names shell.js's catch too, and the test above |
| intfix REVIEW m4 | no behavioural test of the resize re-read | `test_a_resize_makes_the_scrolling_body_a_stop_and_takes_it_back` in `test_overlays_browser_w2_a.py` (beside the 400 % test, both motion settings); both cases fail with the re-read removed |
| W3-D O3 | `html:has(.console-drawer[open])` recalculates the document on every `[open]` toggle | measured: gone with W2-A; an `[open]` toggle costs its own subtree (§2) |
| W3-D O2 | forced colours: the current entry draws the focus outline at rest (2.4.7) | fixed (§1, §2) |
| W1-D NOTES / REVIEW | `initReveal` and the counters read the media query and run a frame loop outside the gate | both deleted (no page used them) |
| W2-C1 A11Y_PERF item 5 (NOTES, REVIEW) | `nav.js` split into a chunk + stub: one script request more on every public page | inlined (§1) |
| W2-C2 NOTES / SHIPPED, DL54-101 item 4, DL54-102 | the home's script over 45 KB until W4-B removes the Motion library | 24 138 B gzip |
| W3-D A11Y_PERF (O3's second half) | «any tap in the console recalculates the document once (282 elements)» | measured: 15 + 2 elements a tap now (§2) |

## 4. The smoke (lane 8, HEAD)

48 loads (`.work/w4-b/w4-b-impl-1/plan_smoke.json`, `evidence/v54/w4-b/smoke-head/` and its `sheets/`): fr and ar, 1440 × 900 and 390 × 844 (touch), the setting off and on — the home (the hero after its discovery: E2 at 1440, E3 at 390, the door stage never mirrored; the chapters under it), the phone's «Menu» sheet, the login «Il varco» (at rest, the e-mail's focus — the four ways lit —, a submit with a made-up address and the password field left EMPTY: the loader's submit path, then the form's refusal), the sign-up (an entrance page: the arrival at 1440, none on the band), the console's entrance release on the dashboard (a freshly minted session: the rail's mark lit at load + 250 ms and at rest after; under the setting the still from the first frame), «Ma situation»'s question change (mid-change at 150 ms: the arriving question translucent and 16 px in the reading direction — from the right in French, from the left in Arabic —; already in under the setting; no `style` attribute left after), the phone's console drawer, and «Mes pièces»'s alert dialog (a loose piece put on the lane through the product's own Dépôt for it — its busy key and its filed answer captured in `smoke-upload/` — and deleted again at the end). Every load 200 (the 404 its 404), 0 console errors, 0 CSP reports; I looked at every sheet: the motion and the reduced captures land on the same still, the Arabic pages mirror and the stage, the mark and the key do not. Forced colours: `forced-focus/` (O2). The L1 key mid-flight on the login could not be shot (§7).

## 5. Tests

All on `test_ile_v5_l8`, one pytest and one browser at a time, no crash.

- **Non-browser, the targeted set** (`-m "not browser"`): `test_script_motion_gate`, `test_frontend_bundle_is_current`, `test_css_bundle_is_current`, `test_static_pipeline`, `test_loader_rules`, `test_loader_w1_d`, `test_entrance_w2_b`, `test_entrance_form_w2_b`, `test_overlays`, `test_overlays_console_w2_a`, `test_nav_sheet_w2_c2`, `test_journey_w3_d`, `test_console_shell_w3_a`, `test_console_shell_stylesheets`, `test_design_docs`, `test_v5_tokens`, `test_rm_flag_parity`, `test_css_tokens_exist`, `test_single_submit_w4_b`, `test_components_w1_c`, `tests/i18n/test_rtl_static.py`, `apps/pages/tests` — **1 313 passed**; after the last commits the quick static set again: 138 passed; `ruff check .` clean; `manage.py check` clean; `regen_design_inventory.py`: current.
- **Browser, the targeted set** (`-m browser`): `test_motion_browser_w4_b` (new), `test_loader_w1_d`, `test_reduced_motion_w1_d`, `test_overlays_browser_w2_a` (with m4's new test), `test_overlays_console_browser_w2_a`, `tests/i18n/test_rtl_browser_overlays.py`, `test_nav_sheet_w2_c2`, `test_browser_w2_c2`, `test_browser_w2_c1`, `tests/i18n/test_rtl_browser_nav.py`, `test_rtl_browser_w2_c2.py`, `test_journey_browser_w3_d`, `test_console_shell_browser_w3_a`, `test_console_phone_browser_w3_a`, `tests/i18n/test_rtl_browser.py`, `test_rtl_browser_entrance.py`, `tests/frontend/test_browser.py`, `apps/pages/tests/test_browser.py` (the hero), the entrance's browser tests, `test_documents_browser_w3_c`, `test_drawer_browser_w3_c`, `test_depot_browser_w3_c`, `test_dashboard_browser_w3_b` — **410 passed, 2 failed**: W3-A's two forced-colours tests, which pinned the outline at rest that O2 removes; updated (`286da57`), they pass (2 passed). Then a safety set — `apps/portal/tests/test_browser.py`, `apps/ecosystem/tests/test_browser.py`, `test_browser_w1_c`, `test_orientation_browser_w3_f1`, `test_browser_w3_f1`, `test_content_pages_browser_w3_f2`, `test_service_pages_browser_w3_f2`, `test_browser_w1_b`, `test_browser_chips_w1_c` and the two W3-A shell files whole — **158 passed**.
- The new tests bite: `test_motion_browser_w4_b.py` on design-v5's tree — 5 of 7 fail (the two that pass are the reduced-motion cases, already true); m4's test with the resize re-read removed — both cases fail; m2's test with a plain `<button>` on the profile form — fails.
- Not run: the full suite (V5.5: the integration checkpoint's), Firefox and WebKit (not installed).

## 6. Paths outside the slice — for the merge step to write into OWNERSHIP_V54.json

`scripts/check_ownership.py w4-b design-v5` (with this file committed) → 4 inside, 6 slice, 22 generated, 13 delegated,
**2 outside, 2 steward-only → FAIL**, by design of this step:

- `package.json`, `package-lock.json` (steward-only): the `npm uninstall motion --package-lock-only --ignore-scripts` the
  orchestrator asked of this area; design-v5's own `node_modules` still holds the five packages until the steward's next
  `npm ci` prunes them (no build imports them any more);
- `scripts/build_frontend.mjs` (no owner): the `INLINED` list, W2-C1's item 5 handed to «W4-B / the steward»;
- `docs/design-v2/FRONTEND_DEPENDENCIES.md` (no owner): the dependency registry's own rule — no row for a dependency that
  is not there — so the `motion` row says it left, and when;
- delegated, each in AUDIT.md §10 / DL54-153 item 9: `static/js/src/situation.js` (F2), `static/js/src/shell.js` (the
  reveal), `static/js/main.js` (`initCounters`, `initMisc`'s comment — beside the slice's `initReveal`),
  `static/css/v5/chrome.css`, `static/css/base.css` (F4, F5), `apps/portal/static/portal/v5/_shell.css` (F3, O2),
  `templates/base.html` (one `{% comment %}` that named Motion), `docs/design/DESIGN_SYSTEM_2026.md` (§11.6, §12, §16 and
  the figures by `regen_design_inventory.py`), `docs/ACCESSIBILITY.md` (§7), `tests/frontend/test_console_shell_w3_a.py`,
  `test_console_shell_browser_w3_a.py` and `test_console_phone_browser_w3_a.py` (the rail's transition, the forced-colours
  outline at rest — O2), `test_design_docs.py` (beyond the section count: the reduced-motion check and a runtime name),
  `test_css_tokens_exist.py`, `test_overlays_browser_w2_a.py` (m4).

`components.css` is in W3-E's diff too (§23) — this branch deletes §29, far below. A trial merge of the two branches
(`git merge-tree --write-tree v54-w3-e v54-w4-b`) merges `components.css` and `base.css` cleanly and conflicts only where it
must: the generated dist trees (rebuilt from clean by the steward), DS 2026 §2's inventory table (regenerated by both:
`regen_design_inventory.py --write` after the merge) and DL54's two appended tails (the table row and the section: keep
both, renumber this one). W3-E's other DS 2026 hunks (§11.10, §12's V4 history) stand apart from this branch's.

## 7. Left, and for whom

- **W3-E / the steward, after W3-E's merge**: `console.js`'s `afterPaint().then(() => … is-ready)` and its header line «what
  moves is the rail's width» are now a hook without a transition (W3-E's file, not touched here; the browser tests wait on
  `is-ready`, so it can stay). On design-v5 the case file still draws V4's progress meter — `.meter__notch--on` →
  `notch-fill` at load where a case has requirements; W3-E's case file and its removal of `v4/workspace.css` take both out.
- **W4-D (the legacy sweep)**: `components/hero.html` (included by no template; it carried the last `.reveal`), the
  `.entrance` / `.entrance__cta` rules left in `components.css`, `--duration-reveal` / `--reveal-distance` /
  `--reveal-index` in `_legacy-tokens.css`, the `hero_lines` filter of `apps/cms/templatetags/cms_nav.py` (no template uses
  it), `data-reveal-once` on `orientation/result.html` (no script reads it), and the dead guard
  `html.js .page-home .reveal { opacity: 1; }` of `apps/pages/static/pages/css/pages.css` (l. 43–45; no `.reveal` is left
  anywhere — the review's leftover, added in «Review fixes»).
- **W1-A / the steward (one comment)**: `v5/tokens.css` l. 468 calls the springs «CSS twins of motion.js»; the JS twins left.
- **DevOps / W1-D**: the three dynamic-import entries with fixed names (`loader.js`, `depot.js`, `piece-drawer.js`) under a
  one-year `WHITENOISE_MAX_AGE` (intfix review, «seen on the way»): the build's `INLINED` mechanism could make them hashed
  chunks, but `test_depot_w3_c.py` pins `dist/depot.js` — a decision for them, not taken here.
- **Not seen**: the L1 engage and the L2 key mid-flight on the login — Playwright waits for a pending POST navigation
  before it evaluates or shoots, so the frames between the press and the answer cannot be captured that way; the Dépôt's
  in-page submit shows L2's key (`evidence/v54/w4-b/smoke-upload/busy.png`) and `test_loader_w1_d.py` holds the engage.
  Firefox and WebKit not installed; no real phone; no person watched the motion at speed (plan §6's honest limit).

## 8. The lane, cleaned

The lane server on 8788 stopped (`lane.py stop`: the port free); the three minted sessions revoked on `ile_v5_l8` (3 rows deleted, the secrets file removed); the loose piece put on the lane for the dialog's smoke deleted through the product (its row stays soft-deleted, as the product keeps a deletion; its file removed from the worktree's `private_media/`); no browser of mine left running; 8780, 9222 and 9223 never touched; the benchmark lock never present when a build, a browser series or a suite started. Scratch scripts in `.work/w4-b/w4-b-impl-1/` (the instrument `motionlog.js`, `probe.py`, `rail_fps.py`, `o3_probe.py`, `forced_focus.py`, `jsweigh.py`, the plans); `base/` there is an export of design-v5 `8ab5b89` used for the before measures.

## Review fixes (w4-b-fix, 16 October 2026)

One fix pass after the senior review (`REVIEW.md`: SHIP_AFTER_FIXES, four minors) and the accessibility / performance
check (`A11Y_PERF.md`: SHIP_AFTER_FIXES, one major, two minors — the review's m1–m3 seen from the accessibility side).
Every item is fixed; nothing is left open in the area. Lane 8 (8788, `ile_v5_l8`, `ILE_REFERENCE_DATE=2026-10-03`,
`DB_CONN_MAX_AGE=0`, `--noreload`, no preview flag); tests on `test_ile_v5_l8`; scratch `.work/w4-b/w4-b-fix/`; evidence
`evidence/v54/w4-b/fix/`.

| Item | What was wrong | Fix | Commit |
|---|---|---|---|
| A11Y major · review m1 | «Ma situation»'s question change asked from the keyboard (Enter on «Continuer», Space on «Précédent», Enter on a Stepper link) ran the pointer's 120 + 200 ms; the focused question's ring showed ≈ 320 ms after the key (tier 0, R-07) | `situation.js` asks the input's modality beside the gate: under `html[data-input="key"]` (head.js writes it on the keydown, before the click) no animation is created — the question swaps in the key's own task with the focus and its ring on it, as under reduced motion | `98e0b96` |
| A11Y 2 · review m2 | A return within the 120 ms leaving fade («Continuer» then «Précédent» 40 ms later; the Stepper's Q3 then Q1) left no question drawn and the focus on `body`: the first change's late step hid the question the second had shown | each change takes a turn (`const turn = ++generation`) and every late step returns when its turn has passed; a change asked while another is in flight lands it first — the steps' running animations cancelled, their inline opacity cleared — and plays its own arrival only | `98e0b96` |
| A11Y 3 · review m3 | The console bar's trail links ran the links' 120 ms colour fade when Tab focused them | `html[data-input="key"] a { transition-duration: 0ms; }` beside the links' transition in `v5/base.css` (W1-A's sheet, through the delegation, as F4 and F5) | `ebcc978` |
| review m4 | `--ease-exit` outside its one role in ten declarations (MS-O1 / MS-O2), after the superseded council table | `--ease-enter` in all ten — `v5/chrome.css` 419–420 (the portico's pointer exit), `v5/overlays.css` 111 and `v5/_overlay-panels.css` 79 (the menu items' and the close control's hover colours), `portal/v5/_shell.css` 228, 316, 387, 446, 1134, 1170 (the rail's rows, tools and foot, the phone bar); the two hover rules that only switched the curve back (`overlays.css` 116, `_overlay-panels.css` 82) lose that clause | `ebcc978` |
| review, for the merge | DL54-132 is sec-f7's on design-v5; `check_ownership.py` FAILs on four paths by design | left to the merge step, as the item says — what to do is below («At the merge») | — |
| the record | AUDIT.md had marked those four lines compliant; DL54-153 said every other motion met its tier | AUDIT.md: the four rows marked ✗ and a §11 (F6–F9); DL54-153: item 1 says what the audit missed, item 9 the paths the fixes added, item 10 the fixes; DS 2026 §12's audit paragraph and ACCESSIBILITY.md §7 item 4 extended | `05d377e` |

**The interruption, as `situation.js` now plays it.** A change in flight is the time from the press to the end of the
arrival: until the leaving fade has run the arriving question carries an inline opacity of 0, and during the arrival its
animation runs. A second change first lands the first (`land()`): the animations it holds are cancelled and no question
keeps an inline opacity; the leaving question is simply hidden and the new one plays its 200 ms arrival from 16 px —
never a second fade, never two panels. The first change's late steps (the arrival after the fade, its `settled()`) ask
whether their turn is still the current one and do nothing otherwise; a press on the current question (the Stepper's own
node) changes nothing and takes no turn. Under reduced motion and from the keyboard nothing is in flight to land.

**Measures.**

- **The smoke on lane 8** (`smoke.py`, 36 cases, one headless Chromium, fr and ar, 1440 × 900 and 390 × 844 touch;
  `evidence/v54/w4-b/fix/smoke.json` and the captures, looked at):
  - the pointer's change unchanged: the leaving question 120 ms, then the arriving one 200 ms from 16 px (−16 px in
    Arabic), one question at opacity 1 afterwards, no `style` attribute, nothing held;
  - from the keyboard (a Tab walk to «Continuer», Enter, then Tab to «Précédent», Space): in the click's own task the new
    question alone is shown, opacity 1, no `style`, the focus on it and `:focus-visible` (its ring drawn at once), 0
    animations — every cell;
  - the interruptions — «Continuer» then «Précédent» 40 ms later, the Stepper's Q3 then Q1, «Continuer» twice 40 ms
    apart, and «Continuer» then «Précédent» 200 ms later (during the arrival): each ends on exactly one question at
    opacity 1 and in place, no `style` attribute, the focus on it, the counter and the Stepper on it, nothing held; the
    second change plays the arrival only (−16 px for a return in French, +16 px in Arabic) — every cell;
  - under reduced motion: swapped at once, 0 animations;
  - the dashboard from the keyboard (45 Tabs, fr and ar): the trail's «Accueil» / «الرئيسية» reached, **0 transitions**;
    a door page (30 Tabs): 0; the portico's pointer exit, sampled after a click closed it: opacity 0.27 at 33 ms (fr),
    0.12 at 50 ms (ar), `cubic-bezier(0.25, 1, 0.5, 1)` over 120 ms — on `--ease-exit` it stood at ≈ 0.92 at 33 ms
    (computed from the curve);
  - the home (1440, 390) and the login (1440), fr and ar: 200, 0 console errors, 0 CSP reports, 0 animations running
    at rest; every other case 0 errors and 0 CSP reports too.
- **Script** (gzip −9): `dist/situation.js` 1 237 → 1 382 B — «Ma situation» 20 415 → 20 560 B; every other page type
  unchanged (no other bundle changed).
- **Shared CSS** (GNU gzip −9 −n from stdin — a few dozen bytes off §2's figures, which used another gzip; the direction
  is the measure): `main.css` 35 355 → **35 349 B** (−6, every page); the console page type (main + console + portal)
  44 016 → **44 007 B** (−9); `core/overlay-panels.css` (page-only) 2 071 → 2 060 B. The ratchet holds: down again.

**Tests** (one pytest and one browser at a time; the benchmark lock never present when a build, a browser series or a
suite started; no crash):

- the new and changed cases bite — on the previous tree: the six «Ma situation» cases fail on the previous `situation.js`
  bundle (the keyboard's change animated; the returns leave no question drawn; the double press faded twice), the two
  trail cases on the previous `main.css` (a `color` transition running, 0.12 s), the two static guards on the previous
  sheets; all pass on this branch (`7f42599`: the in-flight cases assert the interruption's invariants — one fade, the
  first question's, and the last change's arrival last — so a loaded machine that runs the page's 40 ms timer late
  cannot turn them red);
- non-browser, the static set the fixes touch: the implementer's targeted set (§5) with `test_motion_rules_w4_b.py` and `apps/portal/tests/test_situation.py` — **1 333 passed** on the final tree (on the way: the twelve static files the CSS touches, 805 passed; after the docs, 61); `ruff check .` and `manage.py check` clean; `regen_design_inventory.py` current;
- browser: two batches on the final code — **188 passed** (this file, the overlays public, console and RTL, the console shell and phone bar, the portico and the sheet with their RTL files, W1-C's components, W1-D's reduced motion), then **196 passed** (the public pages, the content pages, the Dépôt, «Mes pièces» and its drawer, the orientation questionnaire, the RTL pages and the entrance, the hero, the journey, the portal pages, the dashboard); this file again after its assertion change, 15 passed; 0 failed, 0 errors.

**At the merge (for the steward).**

1. Renumber W4-B's decision-log entry — the table row and the `## DL54-132 · 16 October 2026 · W4-B …` heading — to the
   next free number after W3-E's entries, and its mentions: this file (the header, §1's «The record» row, §6 and
   «Review fixes»), the entry's own note, `A11Y_PERF.md` (finding 1, twice) and `REVIEW.md` («For the merge step»).
2. Write into `OWNERSHIP_V54.json` the four paths that FAIL by design, with their reasons: `package.json` and
   `package-lock.json` (steward-only: the `npm uninstall motion --package-lock-only --ignore-scripts` the orchestrator
   asked of this area), `scripts/build_frontend.mjs` (no owner: the `INLINED` list, W2-C1's item 5 handed to «W4-B / the
   steward») and `docs/design-v2/FRONTEND_DEPENDENCIES.md` (no owner: the registry's `motion` row). The fix pass added
   no path outside the slice: `v5/base.css` (W1-A), `v5/overlays.css` and `v5/_overlay-panels.css` (W2-A) are
   delegated, `tests/frontend/test_motion_rules_w4_b.py` is inside (`tests/**/test_*_w4_b.py`).
   `check_ownership.py w4-b design-v5 --working-tree`: 7 inside, 6 slice, 23 generated, 16 delegated, 2 outside,
   2 steward-only → FAIL on exactly those four.
3. Rebuild the dist trees from clean, and run `regen_design_inventory.py --write` after DS 2026 §2 is merged (this pass
   moved `v5/base.css` 7.7 → 7.9 KB).

**Left for others.** W4-D: the dead guard `html.js .page-home .reveal` of `apps/pages/static/pages/css/pages.css` joins
§7's sweep list. Nothing else new; §7 stands.

**The lane, cleaned.** The server on 8788 stopped (the port free); the one minted session revoked on `ile_v5_l8` (1 row,
the secrets file removed); no browser of this pass left running; 8780, 8782, 9222 and 9223 never touched.

## At the merge (the steward, 16 October 2026)

Label `w4-b-merge`, under `DESIGN_V5_MERGE_LOCK` (taken 07:32:08, design-v5 at `5bf2f90`, the devops-2 record).
Scratch `C:/tmp/ile_v5_council/.work/w4-b/w4-b-merge/`; evidence `C:/tmp/ile_v5_council/evidence/v54/w4-b/merge/`. The
steward's record: **DL54-154**.

- **The sync** (`d707d32`): design-v5 at `5bf2f90` merged into this branch — 91 commits: the sec-f7 merge and its
  record DL54-132; W3-E, its merge, its rebuild and DL54-133 … DL54-151; the private-root probe's test; the devops-2
  merge and its record DL54-152. Three conflicts: the decision log (design-v5's whole, this family's row and block
  appended); DS 2026 §2's generated table (design-v5's side, then `regen_design_inventory.py --write`:
  `components.css` 14.9 KB and 9 sections, `v5/base.css` 7.9 KB, `v5/chrome.css` 51.0 KB); the dist trees (deleted and
  rebuilt with `npm run build`; every bundle neither side conflicted on came out byte for byte the merge's). Four files
  merged on their own and were read: `base.css`, `components.css` (W3-E's §23 beside this family's §29 deletion) and
  W3-A's two shell test files (W3-E's cases beside this family's). No merged source imports the library or an export
  `motion.js` lost; no template, W3-E's included, draws `.reveal` or `[data-reveal]`.
- **The number** (`7e20cbf`): this family's entry is **DL54-153** on design-v5 (DL54-132 on the branch: design-v5 gave
  DL54-132 to sec-f7, DL54-133 … DL54-151 to W3-E and its merge, DL54-152 to devops-2). The six mentions of it in this
  file and in `A11Y_PERF.md` follow; the three that say design-v5's DL54-132 is sec-f7's — «Review fixes», item 1 of
  «At the merge (for the steward)» above, and `REVIEW.md` «For the merge step» — stay as written.
- **The manifest** (`bac3e12`, `b113836`): the four paths of §6 and «At the merge (for the steward)» item 2, each read
  in the diff. `scripts/build_frontend.mjs` (the `INLINED` list and its two comments) and
  `docs/design-v2/FRONTEND_DEPENDENCIES.md` (the `motion` row and the «Decisione d'uso» paragraph) are this family's
  slices of files no family held. `package.json` and `package-lock.json` carry the dependency's removal, which plan
  §3.6 item 2 gives the steward in this merge: adopted as the steward's own write (the lock coherent: no remaining
  package requires `motion`, `framer-motion`, `motion-dom`, `motion-utils` or `tslib`), and the files stay the
  steward's whole, with no family slice — the slices first written for them broke `tests/test_check_ownership.py`'s pin
  «package.json: steward (whole file), steward only» and changed no verdict (the checker reads steward-only first), so
  `b113836` took them out. `check_ownership.py w4-b design-v5`: before, 7 inside, 6 slice, 23 generated, 16 delegated,
  2 outside, 2 steward-only; after, 7 inside, 8 slice, 23 generated, 16 delegated and the three steward-only paths the
  steward writes itself at this merge (the manifest, the two package files); 0 outside. `--validate`: coherent,
  29 families, 738 entries.
- **The payload** (`budget_gate_branch.log`, `jsweigh.log`): `main.css` 31 906 → 31 799 B gzip (−107, every page); the
  console page types 40 140 → 39 978 B (−162); no page type grows. The script per page type: the home 51 249 → 24 138 B
  gzip (9 → 7 requests), a public page 43 674 → 16 781, an entrance page 45 351 → 18 462, a console page
  46 060 → 19 168, «Ma situation» 47 282 → 20 537.
- **The tests** (lane `test_ile_v5_l8`; one pytest and one browser of the steward's at a time, the benchmark lock
  absent at every start; V5.5: targeted, not the full suite): non-browser — the merge brief's list (the motion gate, both
  bundle-current tests, the static pipeline, the loader's rules and W1-D's loader file, the entrance's two files and
  the login form's, W2-A's overlay files, W2-C2's sheet and browser files, W3-D's journey, W3-A's shell files and the
  console's stylesheets, the design docs, `apps/pages/tests`, `tests/security`) with this family's two static files,
  W1-D's reduced motion, devops-2's `tests/deployment/test_static_caching.py` (the import graph this family's build
  writes) and the checker's and the inventory's tests: **846 passed, 1 failed** (15 min) — `tests/test_check_ownership.py`'s
  pin «package.json: steward (whole file), steward only», broken by the steward's own first manifest entries
  (`bac3e12`), fixed in `b113836`: the file again **57 passed**; 0 skipped. Browser (headless Chromium): this family's
  `test_motion_browser_w4_b.py`, W1-D's loader and reduced motion, the entrance's files and its RTL file, W2-A's
  overlay files and their RTL file, W2-C2's sheet and browser files, W3-D's journey, W3-A's shell and phone files,
  `tests/i18n/test_rtl_browser.py`, `apps/pages/tests` (the hero) — **310 passed**, 0 skipped, 0 failed (32 min 33 s),
  no crash. `ruff check .` clean; `manage.py check`: no issue; `makemigrations --check --dry-run`: no changes;
  `git diff --check` clean; no CR byte in a text file the branch changes; no inline style or script, no external URL,
  no secret in the added lines (`tests_*.log`, `checks.log`).
- **`node_modules`**: design-v5's still holds `motion`, `framer-motion`, `motion-dom`, `motion-utils` and `tslib`; no
  build imports them, and this programme's standing rule allows no `npm ci` or `install` — they leave at the next
  `npm ci`.
- **§7's «DevOps / W1-D» item** (the three dynamic-import entries with fixed names under a one-year cache) is met by
  the devops-2 merge, now on this branch: every file a page loads is a hashed, immutable name at collectstatic, a plain
  name revalidated after a minute (DL54-152).
