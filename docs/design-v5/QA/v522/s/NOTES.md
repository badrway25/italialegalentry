# V5.22 lane S — Section System V2 foundation, Icon Treatment V2, Motion Density V2 (label v522-s-build)

Branch `v522-s` from design-v5 `8c0941c` (worktree `C:/tmp/ile_wt/v522-s`). Scope: SECTION_SYSTEM_V2 §9.1. That is the
section runtime, the motion vocabulary V2, the composition library (eleven patterns), Icon Treatment V2 (the thirteen
ILE marks, the T1 seat, the folio seals, the retired bare mark, the login key), the locked-copy helpers, guards,
budgets and docs. Lane S composes no page section. The home (H), the journeys and spaces (P1) and the system pages
(P2) compose with this library in their own family sheets.

- Database lane l3 (`test_ile_v5_l3`, one pytest at a time).
- Lane server 8783: dev settings, `ILE_DESIGN_PREVIEW=1`, `ILE_REFERENCE_DATE=2026-10-03`. Stopped at the end.
- Chromium lock slot A, each session released. The 21:52–22:34 session ran 42 minutes, beyond the 25-minute hold; the
  slot was released and taken again before any further browser work. Later sessions: 22:34–22:54, 23:04–23:11 and
  00:17–00:20.

## 1. What the owner sees, where

**Now, on every page that has a head folio** (lane server 8783; on design-v5 once merged):

- **The folio becomes the page's T1 seal**, in place of the old glyph disc. The seal is a small arch seat, 56 × 68,
  with its 32 px ILE mark standing on the label's rule, which now serves as its sill. It draws once at load: the arch,
  then the mark, then its 12–18 % tone. Under reduced motion it stands still.

  | Page | Mark |
  |---|---|
  | Parcours `/xx/parcours/` (the seat at the top of the route spine) | `ile-percorso` |
  | each pathway sheet `/xx/parcours/<slug>/` («Parcours régulier n/8») | `ile-percorso` |
  | Entreprises `/xx/entreprises/` | `ile-impresa` |
  | Institutions `/xx/institutions/` | `ile-istituzione` |
  | Universités `/xx/universites-et-formation/` (`school` becomes `ile-sapere`) | `ile-sapere` |
  | Formation `/xx/formation/` | `ile-formazione` |
  | Attention aux fraudes `/xx/attention-aux-fraudes/` | `ile-scudo` |

  Evidence: `evidence/v522/s/heads/` (fr and ar at 1440 and 390, reduced motion) and `heads/seals_ar.png` (zoom).
- **The folio discs with no custom mark leave**, and the label stands alone (§4.2; D0, C0 and the Réseau decision):
  Diplômes (`award`), Contact (`map-pin`), Réseau (`users`) and AGAMI (`scale`; same reasoning as D0, since a Lucide
  disc in the folio seat is the old device).
- **No bare Lucide mark above a chapter title any more**, except on the home:
  - `_chapter_head.html` no longer draws one, and `{% chapter_mark %}` without a class renders nothing. The interior
    chapters and the FAQ, community, Vivre-topic, news and partner labels lose their mark.
  - The premium forms' glyph tiles pass their class and are unchanged (§9.8).
  - **The home keeps its chapters' marks** until lane H recomposes it. §9.7 says S never removes a legacy behaviour
    that a not-yet-migrated page still uses, and H's own `test_home.py` asserts these marks. Its head names the class,
    so the home draws exactly what it drew before.
- **Login** (`/xx/compte/login/`): the eyebrow key is 20 px in ink (`entrance.css`, one rule: §9.8 exception 1).
- **M21:** the pointer spotlight on paper cards and links is `--accent-mark` at 10 % instead of oro-300. Gold stays
  only on the night door plate (`.porta`).
- **M22:** the Entreprises photo band (`/xx/entreprises/`, from 48 rem) now drifts slowly against its frame, as
  M22 intends. Before, M2's zoom-and-mask reveal outranked the drift rule (0,3,2 over 0,3,1), so the band opened
  under a mask like any other photograph. The image is now addressed at (0,4,0), and the band's picture is not
  masked.

**When H, P1 and P2 merge:** the composition library below, on their pages. Every partial's header states its contract
(context keys, the wrapper the caller writes, its motion and its still). The evidence is fixtures, never site pages:
`evidence/v522/s/fixtures_768/` (all 20 fixtures, fr and ar), `fixtures_390/` (each section alone),
`fixtures_1440_rm/` (reduced-motion stills), and `marks/` (the thirteen marks at every size).

## 2. What was built (§9.1, item by item)

1. **Runtime** (`static/js/src/rise.js`, 1 326 B gz):
   - `[data-sec]` sections below the fold get `data-sec-state="wait"`, then `"in"` at 25 % of the section, or 25 % of
     the viewport for a tall section, through one IntersectionObserver.
   - A section is also released on focus, hash change and print.
   - Nothing is written when calm (reduced motion, `.rm`, keyboard input).
   - The modules (`sezioni/indice|mappa|flow|spia|racconto.js`) are split chunks, loaded only when a `[data-sec-js]`
     asks for one.
2. **Motion vocabulary V2** (`_reveal.css`, `core/reveal.css` 3 424 B):
   - Verbs declared by `data-verb`: draw, draw-y, stroke, mask, develop, ink, slide, settle, depth, light, zoom, node.
   - `.sez-seq` stagger indexes and the seal's draw choreography.
   - Every entrance is fill `backwards`, with holds only under `prefers-reduced-motion: no-preference`.
   - The M22 specificity fix and the M21 accent.
   - No new duration or curve token.
3. **Library:**
   - The shell is `_sezioni.css`: grounds, rhythm, `.testa` roles, T2 tile, T2a disc, plates, stretched links, the
     body seat sizes, RTL isolation of French text, forced colours.
   - The seat is `_sigillo.css` with `components/sezioni/sigillo.html`.
   - Eleven pattern partials and sheets are listed in §3.
   - `stepper.html size="large"` with `_linea-v2.css` (F).
   - `photo.html` treatment `select` and the `.panorama` layout are in `_photo.css` (D). The panorama's motion (the
     frame widening, the diptych developing) is in `_reveal.css`: a photograph's motion has one home, and
     `_photo.css` animates nothing (`apps/ecosystem/tests/test_compliance.py`).
   - `apps/core/static/core/sezioni.css` bundles the whole library for the fixtures only. A page never links it.
4. **Icon Treatment V2:**
   - The registry is `apps/core/icons.py`: `MARKS`, `MARK`, `FOLIO`, `PILOT_STATION`, `COMPANY_MOMENT`,
     `RECIPIENT_SEAT`, `AUTHORITY_SEAT`, `SHEET_STEP`, `DIPLOMA_STEP`, `HOW_STEP`.
   - The thirteen marks are drawn once on the 48 grid (`static/icons/marks/`). `scripts/build_icons.py` makes their
     inline partials (`components/sezioni/marks/_<id>.html`) and the T2 sprite `img/icons-marks.svg`.
   - Seven Lucide 1.48.0 glyphs under the ILE treatment, each with a licence row (84 glyphs).
   - Filters `mark_of` and `folio_mark`. `_ingresso.html` gains `seal` and `compact`, and the compact band rule is in
     `_fronte.css`.
5. **Locked copy:**
   - `apps/cms/locked_split.py` handles sentences, `:` `;` `→` `,` splits kept with the part before, the first clause
     and the keyword (only when ≤ 3 words).
   - The filters are `locked_spans` and `emphasize`, plus the tag `locked_text`.
   - The joined text always equals the locked text. Tested on `p3.antifraud.body`, `p3.institutions.recipients` and
     `p3.persons.how_it_works`.
6. **Guards and budgets:** see §4 and §5.
7. **Docs:**
   - `DESIGN_SYSTEM_V5.md` §14: shell, tiers, marks, folio, retirement, colour and gold, the register exemption, the
     motion vocabulary.
   - `COMPONENT_PROVENANCE.md`: V5.22 rows for every pattern, with the 21st.dev references taken and refused.
   - `ICON_LICENSES.md` and `DESIGN_SYSTEM_2026.md` (regenerated icon list).

## 3. Budgets measured (gzip -9)

| Sheet / file | Measured | Ceiling |
|---|---|---|
| `main.css` | **32 718** | 32 718 (untouched; none of its four ceilings moved) |
| `core/reveal.css` | 3 532 | 6 144 |
| `pages/css/fronte.css` | 6 138 | 6 144 (the folio seal paid for by the removed disc rules) |
| `accounts/entrance.css` | 4 845 | (existing guards) |
| `pages.css` · `interior.css` · `ecosystem.css` · `pathways.css` (they import `_photo.css`) | 4 649 · 4 070 · 5 341 · 5 500 | 12 288 · 11 264 · 11 264 · 11 264 |
| `_sezioni.css` · `_sigillo.css` (standalone, esbuild-minified) | 2 366 · 876 | (counted in each family sheet) |
| `_sec-campata` · `_sec-boussole` · `_sec-tracciato` · `_sec-racconto` | 973 · 643 · 1 432 · 895 | 1 229 · 716 · 1 434 · 1 229 |
| `_sec-mosaico` · `_sec-mappa` · `_sec-emiciclo` · `_sec-filo` | 1 125 · 1 301 · 691 · 1 021 | 1 229 · 1 434 · 716 · 1 024 |
| `_sec-passaggio` · `_sec-strato` · `_sec-indice` | 614 · 1 424 · 1 405 | 614 · 1 638 · 1 434 |
| panorama layout + «select» added to `_photo.css` | 512 | 716 |
| `_linea-v2.css` added to the passage | 901 | 1 229 |
| `core/sezioni.css` (fixtures only) | 10 364 | — |
| JS: `rise.js` · indice · mappa · flow · spia · racconto | 1 326 · 1 033 · 892 · 605 · 577 · 408 | 1 536 · 1 536 · 1 536 · 1 331 · 1 024 · 922 |
| `img/icons-marks.svg` | 8 439 raw · 2 253 gz | 16 384 raw |

**Per page**, every stylesheet linked, summed:

| Page | Total |
|---|---|
| `/fr/` | 54 603 |
| `/fr/entreprises/` | 58 589 (52 KB without the preserved form sheets, which the page-type ceiling excludes) |
| `/fr/contact/` | 49 451 |
| `/fr/parcours/` | 50 881 |
| `/fr/faq/` | 49 491 |
| `/fr/forum/` | 42 623 |
| `/fr/institutions/` | 50 722 |
| `/fr/formation/` | 50 881 |

The per-page ceilings are in `test_frontispiece_v515_c.py`.

**Close to the ceiling** (S-close ratchets): `_sec-tracciato` (2 B left), `_sec-filo` (3 B), `_sec-passaggio` (0 B)
and `fronte.css` (6 B).

## 4. Tests

| File | Tests | State |
|---|---|---|
| `tests/frontend/test_sezioni_v522_s.py` (new) | 39 | pass |
| `tests/frontend/test_sezioni_browser_v522_s.py` (new) | 19 | pass, 156 s |
| `apps/cms/tests/test_locked_split.py` (new) | 8 | pass |
| `test_icons.py`, updated | 25 | pass |
| `test_chapter_marks.py`, updated | 2 | pass |
| `test_motion_v512_a_w2.py`, updated | 20 | pass |
| `test_interior_w3_f1.py`, updated | 88 | pass |
| `test_frontispiece_v515_c.py`, updated | 87 | pass |
| `test_css_tokens_exist.py`, updated | 122 | pass |
| `test_design_docs.py`, updated | 40 | pass |
| `test_journey_w3_d.py`, updated | 41 | pass |

What the new browser tests cover:
- every fixture at the eight widths of §9.9 in fr and ar, with no sideways scroll and no text cut by a section's clip;
- a section below the fold waits, plays once and holds nothing (`getAnimations()` empty after the entrance);
- under reduced motion no state is written and nothing moves;
- the tabs and the map work from the keyboard in fr and ar;
- without script every panel stands, in reading order;
- the protection keeps its locked `textContent`.

**Regression runs** (targeted, one pytest at a time on lane l3):
- **The touched suites,** with the §5 fixes: 417 passed and 2 failed, both on undeclared custom properties. The fix
  is the `test_css_tokens_exist.py` row below; that file then passed (122).
- **Batch 1:** SVG well-formedness, design docs, static assets, `test_templates_static`, the O14 lint, terminology,
  components, layout and `apps/core`. 516 passed and 2 failed:
  - The icon list did not name the third sprite. Fixed by updating `test_design_docs.py` (row below).
  - The O14 lint (`test_no_template_draws_a_check_in_a_status_context`) flagged six partials whose register glyph was
    chosen by a loop variable it does not know as registry-fed (`t.glyph`, `n.glyph` and others). §6 has the fix.
- **After both fixes:** 542 passed. This covered the O14 lint, design docs, SVG, `test_templates_static`, the
  interior suite and the lane's own tests.
- **Batch 2:** tokens, design preview, orientation, journey, content and service pages, institutional, home,
  prescribed fragments, static assets, terminology, components, layout and `apps/core`. 1 325 passed and 3 failed:
  - Two cases of `test_home.py`: the home's chapter marks. They are kept until H (§6), and `test_home.py` then passed
    (77).
  - `test_journey_w3_d.py::test_one_rail_drawing_and_one_passage_drawing_never_a_third` did not know `_linea-v2.css`.
    It is now registered as a modifier of the one passage (row below), and that file then passed (41).
- **Then** the home, journey, chapter-mark and lane suites: 159 passed.
- **Batch 3:** `apps/ecosystem`, `apps/pathways`, `apps/accounts`, `apps/cms`, the frontispiece and interior suites.
  692 passed and 1 failed:
  - `apps/ecosystem/tests/test_compliance.py` (lane P1's module) forbids `@keyframes` in `_photo.css`, where the
    panorama's widening sat.
  - The motion moved to `_reveal.css`, its single home for a photograph's motion; no test changed.
  - The suites that move touches then passed (290: the ecosystem compliance module, the lane's own, motion, bundle,
    tokens and frontispiece), and so did the browser module (19, at 00:17–00:20).
- **Batch 4:** orientation, enquiries, FAQ, community, Vivre, glossary, news, partners, forum and the design preview
  app: 657 passed.
- **The two portal modules that read the icon registry** (`test_compliance.py`, `test_platform_v515_d.py`): 104
  passed.

In all, about 3 700 test runs, with some suites in more than one batch. Every failure found was fixed, and each
fix was rerun green.

**Updated tests, under the V5.20 strict rule** (each cites V5.22 SECTION_SYSTEM_V2 in place, with an equal or
stronger invariant):
- **`test_icons.py`:** three sprites; the source bijection now spans `static/icons/marks/`; 146 symbols; the
  `chapter_mark` default retired.
- **`test_chapter_marks.py`:** seals or typographic labels, never a bare mark, never an svg before the title. The home
  is held to V5.12's invariants until lane H (§6).
- **`test_motion_v512_a_w2.py`:** `sez-tone`, `sez-layer` and `sez-sweep` are added to the hiding set, bounded to
  pseudo-element layers or `.sg-t`.
- **`test_interior_w3_f1.py`:** the register exemption: `data-register` all-or-none, symbols registered.
- **`test_frontispiece_v515_c.py`:** the blanket 6 KB for four sheets becomes §7.1's per-sheet ceilings plus
  per-page totals.
- **`test_css_tokens_exist.py`:** `--n`, `--sel`, `--spia-y` and `--spia-h` join `RUNTIME_PROPERTIES`, with their
  writers named (`mappa.js`, `spia.js`). Every reference keeps a fallback for the still.
- **`test_design_docs.py`:** the icon list must name every symbol of the three sprites, and the no-literal-colour rule
  now also covers `icons-marks.svg`.
- **`test_journey_w3_d.py`:** `_linea-v2.css` joins the passage's modifiers. The same check holds it to never
  redrawing the passage.

## 5. Found and fixed in the headed pass (1440, 768, 390; fr and ar; reduced motion)

- **«La traccia» cut its own content at 390** in fr (to the right) and ar (to the left). The chip row is a
  `<fieldset>`, whose browser minimum width is its content's. The nowrap chips widened the whole section, and
  `.sez`'s inline clip hid the overflow, so the page never scrolled and the old test passed.
  - Fixed with `min-inline-size: 0`.
  - The browser test now fails on any text outside the viewport unless it sits in its own scroller. The probe was
    checked against the defect re-injected, and it catches both directions.
  - Evidence: `evidence/v522/s/fixes/tracciato_*`.
- **«L'approdo» replayed the frontispiece's 4.3 s draw** on its bookend motif at load, below the fold. The motif's
  rules were scoped by `.fronte__motif` alone. The bookend now stands still (`_sec-strato.css`), and the entrance
  test passes for it.
- **«Il panorama»:**
  - The plate's title was paper ink on the night plate, because `main.css` gives every heading `--ink`. It now takes
    the plate's ink.
  - The credit moved to the top corner: below 64 rem the plate overlapped it. Evidence: `fixes/panorama_*`.
- **«L'indice» as a disclosure (< 64 rem) had no affordance.** It now has a chevron at the row's end that turns when
  open, as the native disclosure does. It is flex-aligned and logical, so it sits correctly in both scripts. Evidence:
  `fixes/indice_*`.

## 6. Recorded choices and deviations

- **`_linea-v2.css` is its own partial**, imported after `_journey-passage.css`. If V2 were inside the passage, the
  questionnaire's `wizard.css`, which imports the passage, would exceed its 6 KB (`test_forms_v515_b`). Every rule is
  qualified `.linea--large`.
- **«La boussole» (A) and «l'emiciclo» (H) have page-only partials** (`_sec-boussole.css`, `_sec-emiciclo.css`, 716
  each), so the campata and mappa sheets stay under their ceilings. The map's ring positions are written by
  `mappa.js` (`--n`, `--i`, `--sel`). Without script, and on a ring narrower than 300 px, the map is a list.
- **T2a large disc:** 32 px glyph in a 64 px disc (§4.6) rather than the table's «40 in 64», for stroke parity with
  the T2 tiles.
- **`DESIGN_SYSTEM_V5.md`:** the doc named §13, but §13 was taken, so the system went into §14.
- **The pilot mark's geography:** a horseshoe arch at the start (Morocco) and an ogee at the end (Veneto), joined by
  an arrowed route arc. The first, symmetric arc read as headphones.
- **`chapter_mark` is retired at the tag:** without a class it renders nothing. This follows §4.2 «bare marks …
  retired», with the forms' glyph tiles kept.
- **The home's chapters keep their marks until H.** Batch 2 of the regression showed that retiring them now would fail
  `apps/pages/tests/test_home.py::test_the_chapters_carry_one_section_device_and_no_running_head`. That module belongs
  to H (§9.7), and the integrated tree must stay at zero failures (§9.9 gate 7).
  - `_section_header.html`, used by the home alone, names its class again.
  - `test_chapter_marks.py` holds the home to the V5.12 invariants (a registered concept, never the stair, one concept
    once, no twins) and every other page to the V2 rule (no glyph above a title).
  - `test_sezioni_v522_s.py` checks that the home's head is the only one left.
- **Per-page totals exclude the form sheets** (forms, steps, glyph), which are preserved family sheets (§9.8). With
  them, Entreprises is 58.6 KB.
- **O14 over a glyph the doc named:**
  - §3.3 PP-1 gives the pilot's station 4 («Préparation avant le départ») `list-checks`, and §3.5 PS-1 gives it to
    the pathway sheet's milestone 4. That glyph draws two ticks: it is `CHECK_BEARING` («never a state, a chip or a
    rail»), and PP-1's own list says «never a check».
  - Both stations take the registry's glyph for the concept instead: `clipboard-list`, the journey's «preparing the
    departure» (`DOMAINS["journey"]["pre_departure"]`). It draws no tick, has no twin and is not a pathway glyph.
  - The diplomas' third station keeps `badge-check`: the seal, an authority's act, and the one check a sequence may
    hold.
  - `test_sezioni_v522_s.py` now asserts it: every V2 sequence and seat is check-free, except the diplomas' seal.
- **The register partials name their loop variable `item`** (`approdo`, `filo`, `indice`, `mappa`, `mosaico`,
  `tracciato`), so the O14 lint reads a glyph inside `[data-register]` as registry-fed (`item.glyph`). The guard above
  ensures that those registries hold no check. The rename changes no output: all forty fixture renders are identical
  byte for byte, except the two stations whose glyph changed.
- **21st.dev:** each pattern's references are re-read and recorded in `COMPONENT_PROVENANCE.md`. «Scroll Spy» 23554
  was fetched in full; its last-section rule (the last part lights at 60 % visible) is adopted in `spia.js`.

## 7. New user-facing strings

**None.** Every word in the library comes from its caller: locked content, catalogue msgids or registry labels. The
two strings the partials print, «Lire la page « Attention aux fraudes »» (protection) and «Étape %(n)s sur
%(total)s» (stepper), are existing msgids with it/en/ar translations already in `locale/`. The seals, marks and
chevrons are `aria-hidden`.

## 8. Requests to other lanes (§9.7: lane S edited none of their files)

- **H, P1, P2:**
  - Import `v5/_sezioni.css` and the pattern partials you compose into your family sheet (`pages.css`,
    `interior.css`, `ecosystem.css`, `pathways.css`, `lettura.css`, `forum.css`).
  - Add `v5/_linea-v2.css` after `v5/_journey-passage.css` wherever a `size="large"` stepper is used.
  - Every sheet that draws a body seal imports `v5/_sigillo.css`. `fronte.css` already does; `pages.css` must, for
    the home.
- **H, P1, P2:**
  - Wrap each section as its partial's header says: `<section class="sez sez--<name>" data-sec="<name>"
    data-ground="…" data-rhythm="…" data-verb="…" aria-labelledby="…">`.
  - Add `data-sec-js="<module>"` on the tabs, map, flow, rail and story; `data-register` on any list that keeps its
    register glyphs (§4.10).
- **P1, P2:** the pilot's eight stations and a sheet's five milestones come from `icons.PILOT_STATION` and
  `icons.SHEET_STEP`, with station or milestone 4 as `clipboard-list` (O14, §6). Never write `list-checks` on a station.
- **P2:**
  - FAQ: `{% chapter_mark "faq" %}` now renders nothing. The FAQ, community and Vivre-topic templates can drop the
    calls when you recompose them.
  - The glossary term page takes `_ingresso.html` with `compact=True seal="ile-lessico"`.
- **H:**
  - The entrances' `rail=True` markup uses `.passaggio`, `.passaggio__lastra` and `.passaggio__arco`
    (`_sec-passaggio.css`).
  - When the V2 home replaces its chapters, retire their bare marks. Drop `_section_header.html`, or its two
    `chapter_mark` calls.
  - Update `test_home.py::test_the_chapters_carry_one_section_device_and_no_running_head`, which today asserts one
    concept mark per chapter. Its V2 form is «no glyph above a title; a theme is a T1 seal inside its composition».
  - S-close then removes the home exception from `test_chapter_marks.py` and `test_sezioni_v522_s.py`.
- **M:**
  - The panorama needs a band slot with a 4:5 phone crop, because below 48 rem the frame is 4:5.
  - `companies.territory`, used by the fixture, has only 21:9, so on a phone it draws a short strip.
  - Slots for «la panoramica» and the pathway lanes use the treatment `select`.
- **Steward:** the preview label «Section System V2 · Icon Treatment V2 · Motion Density V2», and OWNERSHIP rows for
  the new files.
- **S-close:**
  - Remove the dead rules `.chapter__mark` and `.fronte__glyph` from the sheets that still carry them.
  - Retire the reveal-mark rules and the old rise.
  - Ratchet every ceiling in §3 to its measure.
  - A locale pass when the composing lanes add strings.
- **Everyone:** `ecosystem/portal test_compliance` and `pages test_templates_static` read only the chrome and body
  sprites. A marks-sprite glyph in a template literal must arrive through data, or through the `sigillo` partial,
  never as a literal `svg_icon "ile-…"`.

## 9. Not done, or open

- `flow.js` (F's connector beam) is built and measured, but no fixture exercises it in a browser. It runs once a page
  composes F with `data-flow-node`.
- No page composes a V2 section yet, by design. The library is proven on fixtures only, and its first page-level proof
  is H, P1 and P2.
- The full test suite was not run, only the targeted batches in §4. Apps outside those batches render no template
  lane S changed: portal (beyond its two icon modules), companies, cases, documents, helpdesk, academy, audit,
  consents, integrations, legal, notifications, rules and selection.
- Two late changes were proved by tests and byte-for-byte render comparisons rather than a new headed shot: the
  `clipboard-list` glyph on two stations, and the home's chapter marks kept, which looks exactly as before S.

## 10. Round 1 improvements (label v522-s-improve1, 1 November 2026)

The senior review (`evidence/v522/s/QA_ROUND1.md`, 31 Oct) failed the lane on three majors and thirteen minors. A first
attempt at this round was cut by an account limit on 31 Oct; the orchestrator saved its work as `8be8d22` on the merge
`d4c9d8a` (design-v5 `fbfa4af`, lane M merged, no conflict). This round reviewed `8be8d22` change by change, kept what
fixed a finding, corrected what was wrong or incomplete, and completed the rest.

- Lane server 8783 from this worktree (dev settings, `ile_v5_l3`, `--noreload`; the stale 8783 the cut attempt had left
  running was stopped first). Stopped at the end.
- Headed Chromium (chromium-1234), lock slot A: 14:22–14:41, 14:47–14:52, 15:05–15:18, 15:37–15:54, 15:56–16:01,
  16:02–16:04, 16:08–16:10, 16:30–16:35 and 16:36–16:38, each under 25 minutes and released (the browser tests ran
  headless inside those sessions). Scripts and data: `C:/tmp/ile_v5_council/.work/v522-s-imp1/`; evidence:
  `evidence/v522/s/imp1/`.
- Tests on `test_ile_v5_l3`, one pytest at a time.

### 10.1 The three majors

**M1 — the tabs and the map at axe 0.** Kept from `8be8d22`: while a list is a tablist its items step out of the tree
(`role="none"`) and step back when it is a list again; a panel's heading holds its button only as a phone's disclosure
(`indice.js`, `mappa.js`). Verified on the final tree: **144 axe runs** (the 24 fixtures × fr, ar × 1440, 1024, 390; axe-core from
`.work/w1-0-before`, the CSP bypassed in the check only) — **0 violations of any impact** (`imp1/axe.json`). Guarded by
`test_a_tablist_owns_its_tabs_and_a_list_its_items`: the ownership an accessibility tree reads (through `role="none"`
and plain wrappers) — a tablist owns tabs only, a list owns list items only, a disclosure button says whether it is
open — for indice, explorer and mappa at 1440 and 390, fr and ar. axe itself is not a dependency of the repository (a
new npm package needs a recorded reason and licence); the guard pins the three rules axe failed.

**M2 — «la linea V2» stands drawn.** Kept from `8be8d22`: the V5.12 scroll-linked reveal (M5) never drives
`.linea--large`; the origin seal stands on the marks' row, its sill drawn in the route's ink and weight as the route's
first stretch; from 48 to 80 rem the rows of four join by a carriage return (the route turns down at the row's end,
runs back under it and enters the next row's first mark, so row 2 reads in the reading direction). Verified in view at
load and from the keyboard at 390, 768, 1024, 1280 and 1440, fr and ar: every connector at scale 1, unclipped, driven
by no animation (`data2/linea.json`); below the fold the route draws (mask, draw, ink, node, stroke) and leaves
`getAnimations()` empty. Guarded by `test_la_linea_stands_drawn_at_rest_in_view_at_load_and_from_the_keyboard`.

**M3 — the seal folio and the head's call.**
- From 48 rem, and on every head whose band keeps its 40 px (the sheet, Formation, Fraudes, at every width): as
  `8be8d22`, the seat rises 28 px into the band's top padding, 12 px under the trail. Measured at 13 sizes × fr, ar ×
  the seven seal heads against fdd6e34: the title +2 to +4 px, never more; the call inside the first screen everywhere
  (Entreprises 1280 × 720: 698.8 / 720; Parcours 1024 × 768: 747.9 / 768) (`data2/heads_after3.json`).
- **Changed: the phones' door heads.** `8be8d22` hid the seal on every phone's door head (Parcours, Entreprises,
  Institutions, Universités), which left an underlined label where fdd6e34 had its concept disc: the four pages' phone
  heads lost their mark. The seal now stands there: it rises 16 px into the door head's 24 px (8 px under the trail)
  and stands 12 px over the title. **The title is 12 px lower than with the disc — a recorded deviation from the
  review's «±4 px»**: the 24 px band (V5.18 B2) cannot hold a 68 px seat within 4 px without crowding the trail or the
  title, and dropping the seal lowered those heads below fdd6e34. The call stays at least 34 px inside the first screen
  (Parcours, the longest lead: 765.5 / 800 at 360 × 800, 740 / 812 at 375 × 812, 686.5 / 844 at 390 × 844).
- On a short phone (≤ 760 px tall: 375 × 667, 360 × 740), where the call had 5 px to spare, the door head's folio is
  typographic — the label and its drawn rule in the disc's 36 px, as on the four heads without a mark: the title does
  not move.
- **Found and fixed (not in the review): Parcours' route broke at the seal.** The build had moved the route's line to
  the seal's centre (28 px) and left the stations' rings, the arrival point and its halo on the disc's (18 px): a
  10 px dog-leg under the seal at every width from 48 rem. They now stand on the seal's axis (fr and ar,
  `imp1/f2_after_*_parcours.png`; before: `imp1/f1_before_fr_1440x900_parcours.png`).
- Forced colours: the folio's rule — the seal's sill — is drawn in CanvasText (the seat stood on nothing:
  `imp1/forced_entreprises.png`).
- Guarded by `tests/frontend/test_seal_heads_browser_v522_s.py` on the seeded site: the call in the first screen at
  1024 × 768, 1280 × 720, 1366 × 768, 390 × 844, 375 × 812, 360 × 800 and 375 × 667 for the seven seal heads, fr and
  ar; the title's offset in its column (+4 px at most, +12 on a phone's door head); the seat 8 px under the trail and
  12 px over the title; the route head's one axis. Each check was run against its defect re-injected (the rise
  removed; the rings back at 18 px) and failed as it should.

### 10.2 Composition work on the library (the scores' imagery, composition and interaction)

- **F «il flusso»** — the measured variant was a broken fixture (its zig-zag counted the SVG the module prepends into
  the list; the curve ran behind opaque plates). It is now a partial of its own, `components/sezioni/flusso.html` +
  `_sec-flusso.css` (868 B; new ceiling 922): **stage panels hung on one measured curve** — each station's T2 tile a
  node on the line, its panel hanging under it by a short rule, every second station a step lower from 48 rem so the
  line undulates over the panels and never passes behind a word; below 48 rem the nodes stand down the reading edge
  and the line runs straight through them. `flow.js` draws in the `[data-flow]` wrapper, never inside the list; the
  curve draws on the trigger, the nodes' rules light as it reaches them, the end call's hover and focus send one light
  along it. It is EN-1's composition (§3.6): the fixture draws Entreprises' three moments (`company_moments()`,
  `icons.COMPANY_MOMENT`). Guarded by `test_the_measured_flow_runs_one_curve_through_every_node` (wrapper, one curve
  per gap, ends on the first and last nodes, right to left in Arabic) and a static check of the partial.
- **E «il mosaico»** — the grid read as an even card list with a photo pasted on a card. Now: the lead first; with its
  frame (from 48 rem) **the photograph is the lead's ground** and its words stand on a raised plate at its foot, the
  credit in the corner; a **count-aware bento** — 1 + 4 two by two on four columns, 1 + 3 stacked beside a 2 × 3 lead,
  1 + 2 beside a 2 × 2 — so no tile stretches empty and no cell is left; without a frame the lead is the wide tile over
  the whole first row, its glyph tile at 64 beside its title at 28, and the compact tiles share the next row (a fixture
  of its own, `mosaico-ampio`: the wide tile PA-3, F2 and D3 will use). 1 200 / 1 229 B (the five audience accents now
  named once, `--aud` in `_sezioni.css`; the unused `kicker` key removed).
- **B «il tracciato»** — each lane now hangs from **a rail that leaves the trunk** and runs across its head and its
  cards; the lane's name stands over its frame (no longer under the credit); three columns, so a lone card keeps its
  own instead of stretching across the lane. 1 395 / 1 434 B.
- **D «il panorama»** (m11) — a band slot without its portrait crop is drawn on a phone as the strip it is: its plate
  under it, never over it, and its moment's height released. The 4:5 crop of `companies.territory` stays lane M's.
- **J «il passaggio»** (m2) — a fixture of its own, and two defects found by it: base.css's `ol[role="list"]` (0,1,1)
  took the rail's bleed and start padding (the rule is now (0,1,1) itself), and the browser's own focus scroll left a
  peeking plate where it was — while a plate holds the keyboard's focus it is now the rail's one snap position, so Tab
  brings the whole plate in (CSS only; touch is unaffected). 611 / 614 B. Guarded by
  `test_the_passage_snaps_inside_itself_and_brings_a_focused_plate_into_its_rail`.
- **K's light** (m8) — the sweep required the light to be a descendant of the section; a section that declares
  `data-verb="light"` itself now sweeps once (`_reveal.css`). Guarded by
  `test_a_band_that_declares_its_light_sweeps_it_once_as_it_enters` (strato, approdo).
- **RTL** (m5, recorded and extended) — «la linea»'s French labels hang from the marker's edge (W3-F1's rule, coherent:
  numeral, tile and label share one edge in both directions), not «centred under their tiles» as §2 F's RTL line
  says. The same rule now holds for a station's card (B), a flow's panel (F) and a mosaic tile (E): an Arabic page
  showed numerals on the right and French words starting on the left of the same card. A section's French title
  stands under its head rule, on the reading edge. A free French paragraph keeps its own start (§1 rule 6). Guarded
  statically.

### 10.3 The minors

| | Finding | Round 1 |
|---|---|---|
| m1 | keyboard focus animates | `8be8d22` gated the linea's end-call flash, the needle's turn, the tile threshold and the seal light; verified (18 fixtures, 6 Tab presses each): no time-based animation runs on keyboard focus. «Il filo»'s scrubbed line follows the reader's own scroll (§0.1 scrubbed progress), not an entrance — left as designed |
| m2 | J and flow without fixtures | both fixtures, both browser tests (above) |
| m3 | Arabic fixtures without `lang` | `8be8d22`: every French sample on it/en/ar carries `lang="fr"`; checked in the ar shots (final punctuation at the end of each run) |
| m4 | the folio seal faint | `8be8d22`: the edge a border at 62 % (forced colours keep the arch), the vault in shade; this round: the sill in forced colours. The empty crown is the niche's shade over a mark that stands on its sill — kept |
| m5 | RTL labels | recorded and extended (§10.2) |
| m6 | the explorer's concept twice | `8be8d22`: the answer plate draws its seal only (`imp1` explorer shot) |
| m7 | frameless mosaico and tracciato | the framed bento lead, the lanes with their family frames (§10.2) |
| m8 | K light never exercised | fixed in `_reveal.css`, guarded |
| m9 | `test_chapter_marks` traceability | `8be8d22` restores the home's V5.12 expectation (`HOME_EXPECTED`) as written |
| m10 | EN-3 lost its briefcase | recorded for the Director: it was a bare chapter mark, retired by §0 item 3; the form pages keep their glyph tiles. A tile above EN-3's title would bring back the retired device; S recommends accepting the retirement (§0.3). EN-3 is P1's if the Director wants the forms' tile idiom there |
| m11 | panorama strip on phones | fixed (§10.2) |
| m12 | racconto stroke scales | `8be8d22`: a non-scaling 2 px line, as «la boussole» |
| m13 | LCP/CLS/INP not measured; fronte.css headroom | budgets measured (below). LCP/CLS/INP **not measured**: the compressed twin 8782 is switched only by the Performance Lead under the lock (SERVERS.md) — request below. This round adds no eager image, no layout-animating property and no JS on a real page; the flow's overlay is absolutely positioned. fronte.css: the duplicate `padding-block` at 64 rem (the base rule's own value) removed and the seat's default tone left to its fallbacks: 6 141 / 6 144 B |

### 10.4 Budgets (gzip -9, the tests' method)

| File | Round 1 | QA (4c738be) | Ceiling |
|---|---|---|---|
| `main.css` | 32 718, byte-identical | 32 718 | 32 718 |
| `core/reveal.css` | 3 549 | 3 532 | 6 144 |
| `pages/css/fronte.css` | 6 141 | 6 138 | 6 144 |
| `pages.css` · `interior.css` · `ecosystem.css` · `pathways.css` | 4 732 · 4 148 · 5 421 · 5 577 | 4 649 · 4 070 · 5 341 · 5 500 | 12 288 · 11 264 · 11 264 · 11 264 |
| `_sec-mosaico` · `_sec-tracciato` · `_sec-passaggio` · `_sec-flusso` (new) | 1 200 · 1 395 · 611 · 868 | 1 125 · 1 432 · 614 · — | 1 229 · 1 434 · 614 · 922 |
| other pattern sheets (campata · racconto · mappa · filo · strato · indice · boussole · emiciclo) | 973 · 915 · 1 320 · 999 · 1 422 · 1 400 · 651 · 661 | — | unchanged |
| panorama in `_photo.css` · passage V2 (`_linea-v2.css`) | +597 · +1 226 | +512 · +901 | 716 · 1 229 |
| `rise.js` · chunks indice · mappa · flow · spia · racconto | 1 327 · 1 088 · 901 · 605 · 577 · 408 | 1 326 · 1 033 · 892 · 605 · 577 · 408 | 1 536 · 1 536 · 1 536 · 1 331 · 1 024 · 922 |

### 10.5 Tests

- **The review's targeted set** (15 modules: `test_sezioni_v522_s`, `test_locked_split`, `test_icons`,
  `test_chapter_marks`, `test_motion_v512_a_w2`, `test_interior_w3_f1`, `test_frontispiece_v515_c`,
  `test_css_tokens_exist`, `test_design_docs`, `test_journey_w3_d`, `test_css_bundle_is_current`,
  `apps/pages/tests/test_home`, `test_prescribed_fragments`, `test_static_pipeline`,
  `apps/ecosystem/tests/test_compliance`): **650 passed** (one run of 649 + 1, whose one failure was its own new RTL
  check reading the sheet I edited during the run; the module re-run alone: 42 passed). Log:
  `.work/v522-s-imp1/logs/pytest_targeted.log`.
- **Browser** (headless, under the lock): `test_sezioni_browser_v522_s.py` **29 passed** (19 + 10 new) and
  `test_seal_heads_browser_v522_s.py` (new) **4 passed** — 33 in 4 min 55 s.
- New guards: the flow partial's wrapper, the RTL marker rule, `_sec-flusso.css`'s ceiling (static); the ARIA
  ownership, «la linea» at rest, the measured flow, the passage, the band's light, the heads' call and axis (browser).
- **No assertion was loosened, no test skipped, no timeout raised.** `test_journey_w3_d`'s «one passage drawing»
  flagged the first draft (the flow's sheet named `.linea__arrivo`): the sheet now names its own hook
  (`.flusso__arrivo`) and the test is unchanged.
- The home: 0 differing pixels against fdd6e34 in the reduced-motion full-page stills (fr 1440, fr 390, ar 1440).
- ruff clean; every changed source file LF.
- Not run: the full suite (the integrated tree's gate, §9.9 item 7).

### 10.6 Requests to other lanes (§9.7)

- **P1:** EN-1 composes `components/sezioni/flusso.html` (`steps` from `company_moments()` with `icons.COMPANY_MOMENT`;
  `ecosystem.css` imports `_sec-flusso.css` after `_linea-v2.css`; the section `data-sec="flusso"`). The grids of PA-3,
  F2 and D3: the lead first (`lead: True`); without a frame it is the wide tile; a `frame_slot` (develop) makes it the
  framed bento. PA-1's lanes take their `frame_slot` (`pathways.family.*`).
- **H:** the entrances' rail is `<ol class="passaggio" role="list">`; the plates' interior is the home's sheet's.
- **M:** a 4:5 crop for `companies.territory` (already requested); until then the panorama draws a strip on phones.
- **H, P1, P2:** a band that sweeps its light declares `data-verb="light"` on its section.
- **Performance Lead:** LCP, CLS and INP of S's real-page deltas on 8782 (`fronte.css` +633 B, `reveal.css` +1 170 B,
  `rise.js` +454 B against fdd6e34).
- **Director:** m10 (EN-3's retired mark).

New user-facing strings: none. The flow's fixture title and samples live in the test fixtures only.

### 10.7 Self-assessment (§26, 1–5; for the reviewer to verify)

| Surface | Comp. | Motion | Imagery | Interaction | Institutional | Coherence | What moved it |
|---|---|---|---|---|---|---|---|
| The library, 24 fixtures | 4 | 4 | 4 | 4 | 4 | 4 | F hung on its curve; E's framed bento and wide tile; B's rails and frames; D's strip; J's rail and Tab; tabs and map at axe 0; K's light live; one RTL edge rule |
| Parcours | 3 | 2.5 | 2.5 | 3 | 3.5 | 4 | the head's route whole again (seal, line, stations on one axis); the seal on phones. The body is P1's (§9.4) |
| Entreprises | 3.5 | 3 | 3.5 | 3.5 | 4 | 3.5 | the seal on phones, the call in the first screen at 1280 × 720 (698.8 / 720). The body is P1's |

Lane S's bar for pages (§9.9 item 1) is «no page lower on any dimension than at fdd6e34»: met at the scored widths and
at the 13 sizes of §10.1. The pages' own targets (§10) are reached by the lanes that compose their bodies with this
library (H, P1, P2).
