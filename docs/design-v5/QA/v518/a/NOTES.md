# V5.18 · stabilisation lane A (label v518-a-fix)

29 October 2026 · branch `v518-a` from design-v5 `238dc1c` · worktree `C:/tmp/ile_wt/v518-a` · lane server 8783
(`config.settings.dev`, `ILE_DESIGN_PREVIEW=1`, `ILE_REFERENCE_DATE=2026-10-03`, database `ile_v5_l3`) · tests on
`test_ile_v5_l3` · binding: V5.18 (`directives/V5_18_FINAL_VISUAL_ACCEPTANCE_GATE.md`: «Do not use stabilisation as an
excuse for another broad redesign»), DECISIONS §10.0 · the audit: `evidence/v518/AUDIT_resp.md`, `AUDIT_quality.md`,
`workflows_v515/v518_findings.json`.

Scope: B1, P8, P11, P12, P-1, the 18 `c-rise` browser failures of `test_dashboard_browser_w3_b`, and the stale tests of
lane A's families named in T3 (the loader veil's hidden halo in the three-corners guard, the home tiles' «nothing loops»).
Nothing else was touched. No copy was written or changed; no new msgid.

## Fixes

| Id | Root cause | Fix | Files |
|---|---|---|---|
| **B1** Parcours: the compass over «ESPA» | M19's `rise-in … both`: rise-in has a `from` keyframe only, so the forwards fill added nothing but kept a `translate` in effect for ever — each head part stayed the containing block of what is absolutely placed inside it (`.fronte__glyph` landed on `.ingresso__label`) | `both` → `backwards` (the end state is the element's own) | `static/css/v5/_reveal.css` |
| **18 × c-rise** (`test_dashboard_browser_w3_b`, person 10 + company 8) | **Regression, same cause as B1**: `c-rise … both` kept 420 ms rises listed by `getAnimations()` for ever («nothing animates at load: ['c-rise']»), and a translate left on every dashboard block (a stacking context on each) | `both` → `backwards`; the test's settle now also waits for `c-rise` (finite, ≤ 2.5 s), as it waits for lane D's envelope; reduced motion still asserts 0 animations | `apps/portal/static/portal/v5/_motion.css`, `tests/frontend/test_dashboard_browser_w3_b.py` |
| **P8** hero peek 19 px short | `--utility-h: 32px` survived the removal of the institutional bar (v515-a) and `hero.css` adds it into `--chrome` | `--utility-h: 0px` at the top level (the narrow restatement was already 0). Re-measuring showed the second half: a hero 32 px taller grew the door (its stage is sized on the hero's height), the niche took 26 px from the wall and Institutions' gloss went to 6 lines at 1440 × 900 (the guard's ≤ 5). The door is now sized on `--door-room`, the height the hero had under the bar: the 32 px given back are air above the promise and the arch, the door, the niche and the wall's columns are exactly what the owner has seen since V5.15 | `static/css/v5/tokens.css`, `apps/pages/static/pages/css/hero.css`; the token tables of `docs/design/DESIGN_SYSTEM_2026.md` and `docs/design-v5/DESIGN_SYSTEM_V5.md` (the documented contract `test_v5_tokens` reads) |
| **P11** sheet language links 24 px | the 44 px floor applied only under `(pointer: coarse)`; the sheet is a finger's surface at every pointer | `.nav-sheet .lang-seg__list--names .lang-seg__link` takes `min-block-size`/`min-inline-size: var(--hit-primary)` (the coarse-pointer drawing, everywhere in the sheet) | `static/css/v5/chrome.css` |
| **P12** login → platform without the central veil | the sign-in's form names its door (`data-loader-host`), which `threshold.js` excluded from the navigations, and `loader.js` engaged the door instead | V5.18 §4 makes it the central veil's. `submits()` no longer excludes a host form; `after()` returns whether the threshold took the page; `shell.js` hands that answer to `loader.submitted(…, veiled)`, which leaves the host at rest when the veil carries the submit. Pointer: the veil at the press, centred and branded, through the (real) wait of the sign-in, continued by the arrival (`lume-in`); keyboard: the still after `--motion-wait`; reduced motion: the still. Under `lume-go`/`lume-in` the door's and the rail tile's View Transition names are already dropped (motion.css, portal `_motion.css`), so the off-centre gold tile flight and the 360 cross-fade ghost are gone. The console's rail release still plays after the veil — coherent (the tile's own light, once, in its seat) | `static/js/src/lume/threshold.js`, `static/js/src/shell.js`, `static/js/src/loader.js` (+ dist) |
| **P-1** public Forum head static | M1's hairline needs `:has(+ .chapter)`; the Forum's night band is followed by `.forum-sections`. The head's M19 sequence did run (label, title, lead, aside), but the «Sommaire» plate rose as one block | the same M1 stroke on `.ingresso.forum-hero:has(+ .forum-sections)` (its own rules, the shared selector untouched); the sommaire's title rises with the aside's step and its rows one after another (250 ms + 40 ms each, the plate itself no longer rising — one translate, never two). No new keyframes, nothing under reduced motion | `static/css/v5/_reveal.css` |

Dist rebuilt (`node scripts/build_css.mjs`, `node scripts/build_frontend.mjs`): the loader's shared chunk was renamed
(`chunk-ZGNCZFOF.js` → `chunk-ZEHIF7XG.js`, the old one removed). `chunk-ESW3PKTX.js` is unreferenced on design-v5
already (not this lane's; left).

## Stale tests updated to the new behaviour (no guard weakened)

* `tests/frontend/test_lume_v512_a.py` — `submits()` no longer names `loaderHost` (asserted absent), `after()` says
  whether it took the page.
* `tests/frontend/test_loader_rules.py` — the hook passes `veiled`; `submitted()` engages the host only when not veiled.
* `tests/frontend/test_entrance_w2_b.py` — the sign-in's submit test now asserts the new contract: pointer → `lume-go`
  at once, the door NOT engaged, the button `aria-busy`, the lights as the form left them; keyboard → nothing at once,
  `is-departing` after the wait, the door not engaged. (Renamed: `…_the_central_veil_takes_the_page_and_the_door_rests`.)
* `tests/frontend/test_browser_w3_f1.py` (T3 «three corners») — `RADII_JS` counts what is seen: the opacity composed
  with the ancestors' (the veil, kept laid out at rest under `html.lume-warm` at ground opacity 0.002, held
  `.lume-veil__halo`'s `50% 30.8%`).
* `apps/pages/tests/test_browser.py` (T3 «nothing loops») — a loop is an animation with infinite iterations or still
  running on the document's clock; the scroll-driven reveals (ScrollTimeline/ViewTimeline, one iteration) are not.
* `tests/frontend/test_dashboard_browser_w3_b.py` — see c-rise above.
* `tests/frontend/test_loader_w1_d.py` (the busy key's 3 : 1) — the specimen login form is declared outcome-bearing, the
  case where the button's key is the one indicator (no veil over it, asserted); the contrast measure is unchanged.

## Checked in HEADED Chromium 1234 on 8783 (`CHROMIUM_LOCK`, label v518-a-fix)

Probes and frames: `C:/tmp/ile_v5_council/.work/v518-a/` (`probe.py`, `p12b.py`, `shots/`).

* **B1** `/xx/parcours/` 1440 · 1024 · 768 · 390, fr · ar (+ it · en at 1440/768), with and without reduced motion:
  the glyph's box is the text column's start in every case (fr 1440: glyph x 92–128, label 164–806; ar mirrored
  1296–1332), identical to the reduced-motion still; 0 `rise-in` left in `getAnimations()` once settled; no overflow.
* **P8** `/fr/` 1440 × 900: niche bottom 852.8 (peek 47.2 ≈ 48), chrome `0 + 64 + 1`; `test_the_hero_holds_its_geometry`
  passes (gloss lines ≤ 5 again). 1920 × 1080: the hero is capped by its own rows (no defect seen); 1280 × 720: the
  composition's rows are taller than the hero there (8 px peek) — as before, not a P8 cell.
* **P11** sheet at 360 · 390 · 430 · 768, fr · it · en · ar, fine pointer and touch: the four names 44 px tall, ≥ 44 px
  wide, the row wraps nowhere, sheet body without horizontal overflow (`shots/p11_*`).
* **P12** login → `/xx/espace-reserve/` at fr 1440, en 360, fr 768, ar 390 (+ ar 390 reduced motion), by CDP screencast
  (`shots/p12_*`): `lume-go` on the login page at the press, the door not engaged (`door-stage sig varco__door`), the
  central doorway centred (mark centre = content width / 2 ± 1 px), «Chargement…» during the sign-in's real wait,
  `lume-in` on the dashboard continuing the clock, gone after ≈ 900 ms; no login form ghosted over the dashboard at 360;
  under reduced motion the still and its fades. No delay added.
* **P-1** `/xx/forum/` 1440 and 390, fr · ar (+ it · en 1440): at load `reveal-rule` on the band's `::after`, the head's
  `rise-in` and the sommaire's title + 5 rows in sequence; under reduced motion none; settled shots `shots/p1_*`.

## Tests (lane l3, `test_ile_v5_l3`)

* Browser (lock held), `test_dashboard_browser_w3_b.py` + `apps/pages/tests/test_browser.py`: **50 passed, 5 failed** —
  all 18 c-rise cases pass, hero geometry and tiles pass. The 5 left are not this lane's:
  - `test_the_bridge…` ×4: lane D's sections `[deadlines, messages, organisation]` vs the test's list (DL54-174 carry-over);
  - `…first_viewport[390x844-fr]`: a `.chip` in the dashboard head wraps to two lines in French (44 px tall, so its 12 px
    radius no longer reads «full») — lane D's head; it was masked by the c-rise assertion before.
* Browser, the loader / motion / entrance families (`test_lume_v515_a`, `test_lume_v512_a`, `test_entrance_w2_b`,
  `test_entrance_form_w2_b`, `test_browser_w3_f1`, `test_loader_w1_d`, `test_motion_v512_a_w2`,
  `test_reduced_motion_w1_d`, `test_header_fits_the_narrowest_viewport`): **112 passed, 5 failed** on the first run;
  `test_loader_w1_d::test_the_busy_key_reads_three_to_one_on_its_ground` ×2 was this lane's (the sign-in is now veiled,
  which dimmed the specimen key): its specimen form is declared outcome-bearing — the case where the key IS the one
  indicator — and it asserts no veil over the key: **2 passed**. Left, not this lane's: P7 (`…target_floor[True]`, C) and
  `test_header_fits_the_narrowest_viewport` ×2, which fail identically on design-v5 `238dc1c`.
* Non-browser, the affected modules (motion, lume ×2, loader rules, v4/v5 tokens, rm parity, motion gate, nav sheet,
  entrance, loader w1-d, design docs, rtl static, css tokens, `apps/pages`): **1254 passed, 5 failed**, none this lane's:
  lane C's `_fronte.css` T1/T2 (`--spine-end`; `text-align: right`) and the 27 `#000` literals the brand-colour guard
  reports in `_fronte.css`; m-6 (`_platform.css` gradients, D); `test_nav_sheet_w2_c2`'s seat label (orchestrator/D).
  `test_login_invitation_w4_d.py` fails 3 on design-v5 `238dc1c` too (pre-existing, not touched).
* Lane server 8783 stopped at the end; the Chromium lock released (held 17:02–17:10, 17:40–17:43, 17:45–17:51,
  17:53–18:07, 18:10–18:12, each under 25 minutes).

## For the other lanes

* **C**: `_reveal.css` M19 also rises `.ingresso__text`, the wrapper of label/title/lead on the composed heads — the
  parts' rises compound inside it (pre-existing; harmless since the fill is backwards; worth a look when the heads
  are next touched).
* **D**: the 390 fr dashboard chip above.
