# V5.18 stabilisation — lane C (label v518-c-fix)

Branch `v518-c` from design-v5 `238dc1c` (all W3 lanes merged), worktree `C:/tmp/ile_wt/v518-c`, database lane l5,
lane server 8785. Binding: V5.18 §2 («Do not use stabilisation as an excuse for another broad redesign»), V5.15,
V5.12, V5.17, DECISIONS §10.0. Findings from `evidence/v518/AUDIT_resp.md`, `AUDIT_quality.md` and
`workflows_v515/v518_findings.json`. Minimal targeted fixes only; no locked text touched, no msgid added or
reworded, nothing machine-translated.

## What changed

| Finding | Fix | Files |
|---|---|---|
| **B2** page-header CTA below the first screen (Parcours, Entreprises, Institutions, Universités & Formation; 768–360; 4 languages) | The audit's three parts: (1) the «words first, photograph after» order and the motif's stand-down widened from `max-width: 47.999rem` to `63.999rem`; (2) selected by `[data-fronte]:has(.ingresso__way)` as well as `[data-words-first]`, so the four door heads read words first below 64rem; (3) below 48rem `.ingresso__way` is a flex column with the button right after the way's question (`order`), its sentence after the button; the lead and its notice stay above, untouched. Measured, that left Parcours at 375 × 667 / 360 × 740 and Entreprises at 375 × 667 still short (the Parcours lead is the locked notice, 11–13 lines), so the door heads on a phone are held a step closer: 24 px under the trail, 16 px between label/title/lead/way, the lead at the body size on a 1.5 line (WCAG 1.4.8's spacing). On a short phone (≤ 760 px tall) the button follows the lead itself, the way's question and sentence under it, the head 16 px under the trail. DOM order unchanged (focus and reading order as before). | `static/css/v5/_fronte.css` §4, dist rebuilt |
| **B3** Entreprises menu says its sentence twice | The `("company", "enquiries:company_needs")` second line removed from `_SECOND_LINES`: the entry carries its title alone; the door's locked gloss above it keeps the sentence. | `apps/cms/templatetags/cms_nav.py` |
| **P-4** Personnes panel half filled (3 of 6 entries with a second line) | Option «present all six consistently». No existing short live sentence exists for «Diplômes et titres» or «Vivre en Italie» (their only ledes are the locked bodies, 268 and 245 characters, never cut; the catalogue holds no translated short line for either), so adding lines was impossible without new copy. The three person-panel second lines (Formation, FAQ, Glossaire) are removed instead: six titles alike. The own-space legal notice stays in the panel's foot. The three msgids remain in use on their own pages (training, FAQ, glossary), so the catalogue is unchanged. | `apps/cms/templatetags/cms_nav.py` |
| **P7** «Accueil» 24 px under a finger on the band heads | Cause found: the trail's full-bleed ground was a 100vmax box-shadow held to the row by `clip-path: inset(0 -100vmax)`; the clip also clipped the link's 44 px `::after` target (v5/_pagina.css §1) to the trail's box — it failed on every band head (le-projet, agami…), not only the night ones. The ground is now a `border-image` cast sideways (`fill 0 / 0 / 0 100vmax`): same paint, nothing clipped, no shadow (which also removes the breadcrumbs entry from the content-pages grammar failures). | `static/css/v5/_fronte.css` §2 |
| **T1** `--spine-end` dead hook | `inset-block: 46px 28px`. | `_fronte.css` |
| **T2** `text-align: right` | `text-align: end` — the run is `dir="ltr"`, so its end is the same right edge. | `_fronte.css`; `test_frontispiece_v515_c` pins `end` |

## Tests updated to the new behaviour (none weakened)

- `test_cms_nav::test_portico_gives_every_door_its_panel_from_live_content`: Personnes `[False] * 6`; Entreprises
  `[False, True]` plus an assertion that the gloss still carries the sentence.
- `test_browser_w3_f1::test_the_door_card_carries_its_way_in_the_first_screen…`: **tightened** — the control's
  bottom ≤ the viewport height (was: its top < 1.25 vh on phones), at 1440×900, 1024×768, 768×1024, 430×932,
  390×844, 375×667, 360×740 (was 1440 and 390), fr and ar.
- `test_browser_w3_f1` RADII_JS (three corners): lane A's `.lume-veil` (the transition overlay, measured visible at
  `load` with its 50% / 30.8% halo) is not counted; everything else as before.
- `apps/pages test_a_finger_on_the_tiles…`: «nothing loops» now asserts no time-based animation still running and
  no infinite iteration anywhere; lane A's scroll-driven ViewTimeline reveals (iterations 1, bound to the scroll)
  are no longer counted as loops.
- `test_content_pages_browser_w3_f2::…grammar…`: the V5.15 raised surfaces admitted **by name** with their decision
  (`V515_RAISED`: the band's search seat and the photograph's passe-partout — lane C, DL54-172; the formwork panel and
  grid, the glyph tile, the consent box, the steps' tiles — lane B, DL54-173). Any other shadow at rest still fails;
  the corner, Arabic 14 px, 16 px field, h1 and overflow checks are untouched.

## Measured (headed Chromium 1234, under the lock, lane server 8785)

- B2: 4 pages × 4 languages × 1440/1280/1024/768/430/390/375/360 = 128 loads — baseline **53 below**, after the fix
  **0 below**, no horizontal overflow (`evidence/v518/c/base`, `r2`, `r4`; screenshots `b2_<lang>_<w>_<page>.png`).
  Tightest: ar 375×667 Parcours, 8 px to spare.
- P7: elementFromPoint ±21 px around «Accueil» and «Le projet» on /fr/le-projet/ and /fr/agami/ at 390 coarse: all
  inside (was false at +15/+21, hitting `.ingresso`); `evidence/v518/c/r4/p7.json`.
- B3/P-4: mega panels fr/ar/it/en at 1440 and 1024 and the phone sheet at 390/360 (`evidence/v518/c/r3/`): Entreprises
  «Besoins professionnels» title only, Projet pilote keeps its line; Personnes six titles; no panel overflow.

## Tests run (database lane l5, one pytest at a time)

- `test_browser_w3_f1.py` (all) + the tiles test: 23 passed after the short-phone step (one red before it: ar
  375×667 at 673/667 in the test's desktop-emulated viewport, classic scrollbar).
- `test_content_pages_browser_w3_f2.py`: 10 passed; the grammar test **still red, not lane C's**: (a) the formwork
  pages' corners (5–6 values on /contact/formulaire/, /entreprises/recueil-des-besoins/, /collaboration/
  institutions/ — lane B's formwork, «the Director's to rule» per DL54-173); (b) Arabic 12 px text
  (`form-field__optional`, `steps-head__tile`) — P10, lane B.
- Non-browser (`-m "not browser"`): test_cms_nav, test_frontispiece_v515_c, test_css_tokens_exist, tests/i18n/
  test_rtl_static, test_css_bundle_is_current, test_interior_w3_f1, test_nav_sheet_w2_c2, test_content_pages_w3_f2,
  test_static_pipeline, tests/i18n/test_page_integrity, apps/pages test_home: **558 passed, 1 failed** —
  `test_nav_sheet_w2_c2::test_signed_in_the_targa_seat…`, the audit's T3 «seat label» stale test (orchestrator's).
- Final headed sweep (`r4`): B2 128/128 inside the first screen, no overflow; P7 every trail link ≥ 44 px under a
  finger, ≥ 24 px with a mouse (fr/ar, 1440/390, le-projet, projet-pilote, parcours, agami).

## Not done here / for others

- The formwork corners in the grammar guard (Director / lane B) and P10 (lane B).
- The other T3 items are not this lane's: test_routing ungated count, the seat label, the dashboards' c-rise.

## Refix after the integrated review (label v518-c-refix)

The integrated review (`evidence/v518/INTEGRATED_REVIEW.md`, polish items 1 and 2) on lane C:

| Item | Cause | Fix |
|---|---|---|
| 1 · /ar/parcours/ at 375 × 667: the CTA 620–672 against 667 (5 px) | Measured in a desktop-emulated context (classic 15 px scrollbar: a 360 px column). The French capitals title on the Arabic page (`lang="fr"`) took the Arabic leading (1.35, `[dir="rtl"]` rule) below 64 rem, while from 64 rem the capitals rule already gave it 1.1: three Latin lines 24 px taller than on the French page. | The capitals rule (`:not(:lang(ar))`) carries `line-height: 1.08` as the title's base does: a Latin title keeps its Latin leading on an Arabic page at every width (letter-spacing was already handled there). |
| 2 · the via title «Identifiez la voie régulière à explorer» shown after its own button on short phones (WCAG 1.3.2 / 2.4.3) | The short-phone step of B2 put `.via__action` at `order: -3`, before the title's `-2`. | The `order: -3` removed: the title, the button and the sentence read title → button → sentence at every phone size. To keep the button in the first screen with its question above it, the short-phone step (≤ 47.999rem and ≤ 760 px tall, door heads only) holds the head one step closer: the lead at 16 px on a 1.5 line (was 17 px), 12 px between label/title/lead/way, 8 px between the way's parts. Nothing else moves; no copy touched. |

Measured (headed Chromium 1234 under the lock, lane server 8785, `evidence/v518/c-refix/`; `base` before, `t2` after):
4 doors × 4 languages × 8 sizes (1440–360) on phone contexts, plus 390/375/360 again desktop-emulated (classic
scrollbar) = 192 loads: **192 inside the first screen, 0 order inversions** (the via title above its button wherever
both stand), no horizontal overflow. Tightest: 375 × 667 desktop-emulated Parcours fr/it/ar, CTA bottom 662 / 667;
ar 375 × 667 on a phone context 638 / 667. Before: the Parcours via title after its button at 375 × 667 and 360 × 740 in
every language (`base/m.json`).

Tests: `test_browser_w3_f1::test_the_door_card…` now also asserts the way's question ends above its control at the
seven sizes, fr and ar (stricter, nothing relaxed). `test_browser_w3_f1.py` + `apps/pages/tests/test_browser.py`:
49 passed, 1 failed — `test_the_hero_holds_its_geometry` (the home hero's 48 px peek, 18.7 px off), **red on the
branch head without this change too** (checked by stash), the home hero is not lane C's sheet. Non-browser:
test_frontispiece_v515_c, test_css_bundle_is_current, test_css_tokens_exist, tests/i18n/test_rtl_static,
test_interior_w3_f1, test_static_pipeline, test_content_pages_w3_f2: 435 passed.
