# V5.29 SYS — the one senior visual review (label `v529-sys-review`)

Branch `v524-sys`, head `39e53589`, lane server 8793 (db `ile_v5_l9`, now stopped). Real Google Chrome, headed, slot
CHROMIUM_LOCK_A (18:10–19:14 CET; released, held past the 25-minute limit because the pytest run was slow). Pytest on
`test_ile_v529_sysrev`. Stills, clips, `measures.json`: `evidence/v529/sys/review/`.

**Verdict: FAIL, 1 blocker.** It is not a visual defect: the visual result passes. The branch fails a targeted test
because of its own change, so it cannot be merged as it stands. The fix is one test amendment.

## Blocker

**B1. A HOME browser test fails because of this stream.** The test is
`apps/pages/tests/test_home_browser_v524_home.py::test_the_seams_stand_where_the_director_placed_them[fr|ar]`. It fails at
line 141 with `getComputedStyle … not of type 'Element'`. The test still asserts the V5.24 bookend `.home-antifraud
.sez-fondale` and the sill `.protezione__davanzale`. SYS removed both on the owner's order (V5.29 §4). The builder never
ran this module, and NOTES §5 does not list it.

Fix: amend the test under V5.20, citing V5.29 §4. The new assertions are the compact band: no sill and no bookend, the
pietra ground and its grid mask direction kept, and the band ≤ 240 px at 1440 in fr. That is the same invariant or a
stronger one. Keep every other seam assertion and re-run the module.

## Minor (not blocking)

- m1. The tile glyph does not turn laguna on keyboard focus or hover on stretched-link plates. On the FAQ's «Pour aller
  plus loin» it measures `rgb(78,91,104)` while its plate shows the focus ring. The cause: `.sez-tile` is a sibling of
  `.sez-stretch`, so `:is(a,button,[data-owner]):is(:hover,:focus-visible) .sez-tile` never matches. Focus itself is
  visible, so this is not an a11y defect. Fix: `.sez-plate:has(.sez-stretch:is(:hover,:focus-visible))` sets
  `--tile-ink`, within the budget, and NOTES §1.5 is corrected.
- m2. From 64 rem the protection's two-column body breaks in the middle of a sentence («… ce sont des | pratiques …»).
  Acceptable. A later candidate: break the columns at a sentence.
- m3. The hero's route station labels (`.he-station__label`, 5 small capitals) still use `rgba(7,18,38,.86)`, a
  near-black. They are the only near-black text left on the reviewed pages and they do not dominate. A later candidate:
  `--text-secondary`.
- Not this stream (post-acceptance or another owner):
  - The FAQ accordion at 390 has its question text flush against the plate's edge. `base_faq_390` shows the same, so it
    predates SYS. It is PUB2's.
  - axe reports «landmark-complementary-is-top-level» (moderate) on the protection's `<aside>` inside `<main>`. The markup
    predates this stream.
  - The platform's h1 is still 600, a literal in PLAT's file (§3 contract).
  - 3 Arabic test failures in `test_home*.py` belong to lane AR. design-v5 `abeb04a8` (the steward) has already amended
    them, so they clear on the re-merge.

## Essentials

- **Targeted tests.** 1 354 passed, 3 failed (the AR items above). The suite covered tokens, typography, LIB, the
  section library, the bundles, the pipeline, locked texts and renderings, home, frontispiece, Lume, navigation, forms
  and log privacy.
- **Browser modules.** 54 passed, 2 failed (B1). They covered LIB materia, contact channels, lane S sections and the HOME
  browser module.
- **main.css.** 32 702 B on zlib -9, under the 32 716 ceiling; no ceiling was raised.
- **Locked copy.** The `p3.antifraud.body` rendering on fr home and on Parcours is byte-identical to the one on the fraud
  page. The protection template still renders it whole through `locked_text` / `locked_spans`.
- **Contact channels.** The e-mail, the freephone number and WhatsApp are all present in the footer (checked in process).
  The configured number appears in no tracked file and in no part of the branch diff.
- **Preserved families.** Navbar, Lume, contact, privacy, forms and the role model show no change in the diff and their
  tests are green. Their stills show no regression.
- **Keyboard and motion.**
  - The home and Parcours «Lire la page» calls show a 1.6 px laguna ring.
  - The FAQ tiles show the plate ring, in fr and ar.
  - The reduced-motion stills are static and complete (`rm_*`).
- **Layout.** At 1440, 1024 and 390 the pages scroll sideways by 0 px. RTL mirrors the band and the light, and the band
  is 114 px tall in ar.

## V5.29 §23

| # | Answer | Evidence |
|---|---|---|
| 1 raw CSS grids | NO, on this stream's primitives | The plates (trust tablet, steps, Espace tiles, mosaico) have a lit face and a two-layer shadow. The trust tablet is an uneven 2 + 2 layout. |
| 2 pure/heavy black | NO | Ink is `#222f3d`, secondary `#4e5b68`. Across 21 page/width captures, near-black text appears only in m3. |
| 3 bold headings | NO | Every h1–h3 on the public pages is at 500. Across 21 captures, 0 text elements are at 700 or more. |
| 4 backgrounds designed | YES | Stone and brand bands get a radial light at the head on the reading side, mirrored in ar: home orientation, Parcours, FAQ. |
| 5 cards / materials | YES | Lit plates; question titles quieter (ui step, 500, slate), so «Non.» and the answers lead. |
| 6 FAQ premium | not this stream (PUB2) | SYS's tiles and plates on the FAQ are refined and semantic. The mobile padding note goes to PUB2. |
| 7 icons semantic | YES (m1 minor) | FAQ: 3 different glyphs. Parcours: 8 different pathway glyphs. Espace Personnes: 5 different. Tinted vault, slate glyph. |
| 8 protezione discreet | YES | One compact band: 213 px at 1440 fr, 114 px ar, 292 px at 1024. At 390 it is 547 px, because the locked text must stay whole. No far shield, no sill. |
| 9 Institutions Italy–Morocco | not this stream (PUB1) | — |
| 10 less editorial | YES | Lighter weights, re-inked text, quieter plate titles, the hero description at a 48 rem measure. |

## After the one fix round (`v529-sys-fix`) — the verdict as the workflow returned it, verbatim

```json
{"pages": [{"page":"Homepage /fr/ + /ar/ (1440/1024/390)","composition":4,"motion":4,"imagery":4,"interaction":4,"institutional":4,"coherence":4,"note":"PASS visually: compact protection band (213 px fr, 114 px ar), lit plates, ink #222f3d, titles at 500, he__body at 48 rem. Merge blocked only by B1, a test failure."},{"page":"FAQ /fr/faq/ + /ar/faq/","composition":4,"motion":4,"imagery":4,"interaction":4,"institutional":4,"coherence":4,"note":"PASS for SYS's part: 3 different semantic tiles, plate focus ring fr/ar. Question text flush to the plate edge at 390 predates SYS (PUB2's)."},{"page":"Parcours /fr/parcours/ + /ar/parcours/","composition":4,"motion":4,"imagery":4,"interaction":4,"institutional":4,"coherence":4,"note":"PASS: 8 different pathway glyphs, lit step plates, compact protection band; 0 px sideways scroll at 390."},{"page":"Entreprises /fr/entreprises/","composition":4,"motion":4,"imagery":4,"interaction":4,"institutional":4,"coherence":4,"note":"PASS: inherits the ink, weights and plates; no regression."},{"page":"Formation /fr/formation/","composition":4,"motion":4,"imagery":4,"interaction":4,"institutional":4,"coherence":4,"note":"PASS: compact protection band justified; tiles tinted."},{"page":"Fraudes /fr/attention-aux-fraudes/","composition":4,"motion":4,"imagery":4,"interaction":4,"institutional":4,"coherence":4,"note":"PASS: the page keeps its own idiom; the held accordion rises on a real scroll, same as on 8780 (not a defect)."},{"page":"Platform /fr/espace-reserve/ (qa-person)","composition":4,"motion":4,"imagery":4,"interaction":4,"institutional":4,"coherence":4,"note":"PASS: inherits the ink roles; h1 600 is PLAT's literal (contract item)."}],
 "minors": [{"severity":"minor","where":"static/css/v5/_sezioni.css (.sez-tile --tile-ink rule)","detail":"On stretched-link plates the tile glyph stays slate (rgb(78,91,104)) on keyboard focus and on hover, for example the FAQ's «Pour aller plus loin» in fr and ar. The cause: `.sez-tile` is a sibling of `.sez-stretch`, so `:is(a,button,[data-owner]):is(:hover,:focus-visible) .sez-tile` never matches. The plate's focus ring is visible, so this is not an a11y defect, but NOTES §1.5 claims the glyph turns laguna.","fix":"Add `.sez-plate:has(.sez-stretch:is(:hover,:focus-visible)) { --tile-ink: var(--accent-text) }` within the main.css budget, or correct NOTES §1.5."},{"severity":"minor","where":"static/css/v5/_sec-lastre.css (.protezione__testo columns ≥ 64 rem)","detail":"The two-column locked body breaks in the middle of a sentence («… ce sont des | pratiques illégales …»).","fix":"Post-acceptance candidate: break the columns at a sentence."},{"severity":"minor","where":"apps/pages/static/pages/css/hero.css (.he-station__label)","detail":"The 5 hero route labels still use the literal near-black rgba(7,18,38,.86). They are the only near-black text left on the reviewed pages and they do not dominate.","fix":"Post-acceptance candidate: use var(--text-secondary)."},{"severity":"minor","where":"not this stream — FAQ 390 accordion (PUB2), protection <aside> landmark, test_home*.py AR failures","detail":"Three items that predate SYS or belong to other owners: (1) at 390 the FAQ question text sits flush against the plate edge, identical in base_faq_390 (PUB2's); (2) axe reports landmark-complementary-is-top-level (moderate) on the protection's <aside> inside <main>, markup that predates SYS; (3) 3 AR failures (test_arabic_home_is_rtl_and_marks_french_fallback, test_the_morocco_italy_model_is_said_once_by_the_heros_path[ar], test_the_orientation_route_in_another_language_carries_the_french_it_is_cut_from), already amended on design-v5 at abeb04a8.","fix":"Re-merge design-v5 (abeb04a8) before the SYS merge, and hand the other items to PUB2 / CLOSING as post-acceptance candidates."}],
 "new_strings": [], "not_done": []}
```

The owner's ruling, 6 Nov 2026 19:36 (V5_29_FINAL_PREMIUM_VISUAL_REMEDIATION.md): the SYS review is ACCEPTED; B1 is
handled surgically — the seam test asserts the compact band and the ABSENCE of the sill and the bookend, citing
V5.29 §4; the steward verified the three proofs before merging (DL54-193).
