# V5.22 lane H — Homepage Composition V2 (label v522-h-build)

> **Erratum (v524-home, 6 Nov 2026):** credits removed by v524 (V5.24 §2) — wherever this file says a photograph's credit stands in its corner or under its frame (M1 e, the pilot's halves, the Arabic page's credit colon), the credit is gone from the product; the provenance stays internal (lane PX, `IMAGE_LICENSES.md`).

Branch `v522-h` (worktree `C:/tmp/ile_wt/v522-h`), cut from `design-v5` at `22b0ddd` (lanes S and M merged). Lane
server 8785 on the lane database `ile_v5_l5`; tests on `test_ile_v5_l5`; headed `chromium-1234` under lock slot A.
Binding: `directives/V5_22_*.md`, SECTION_SYSTEM_V2 §0, §0.1, §1, §2, §3.1, §4–§8, §9.3, §9.7–§9.9, §10; the audits in
`evidence/v522/`. Evidence of this lane: `C:/tmp/ile_v5_council/evidence/v522/h/` (r0–r9, axe, sweep, perf, catalogue).

The home's sections are now one system: each one is a library pattern of lane S (`components/sezioni/*`, the
`.sez` shell, the section runtime and its verbs), on its own ground, with one head, one signature entrance played
once, and lane M's frames. Lane H edited no file of S or M (§9.7): the home's own material is
`static/css/v5/_casa.css`, a page-only partial imported by the home's sheet alone.

Preview label (§9.9 item 8): «Homepage Composition V2» — the steward's `live_status` writes it; lane H writes no
steward file.

---

## 1. What the owner sees, where

Order and grounds with gate G3 open (the back office still orders the sections; `services._grounds` resolves the two
light grounds so that two of one kind never touch, whatever the order — §1 rule 5):

| # | Section | Ground · rhythm | 1440 (and 1280, 1024) | 768 | 390 (and 430, 375, 360) |
|---|---|---|---|---|---|
| H0 | the hero's foot «la soglia» | paper wall | a 2 px bronze line leaves the statement 12 px off the reading edge and runs down to the hero's foot; the paper fades into the orientation's wash over 96 px — no cut | same, the line 12 px off the statement | the line ends on its node above the doors |
| S1 | «il passaggio» — the four doors | stone · band | not drawn: the hero's four origins are the doors (V5.15 rule, kept) | not drawn | one rail: four equal plates (night arch seat, glyph disc, title, sentence, call), the next one peeking, snap, its own progress rule; the page never scrolls sideways |
| S2 | «la linea V2» — how the orientation works | the page's one brand wash · band | the line from the hero goes on down the band and stops on the sill of the orientation's T1 seal, where the route begins; four stations across (mono 01–04, the seal, then glyph tiles), the locked sentence cut at its own commas, said whole once for assistive technology; the caveat drawn once at the route's end; the call «Commencer le questionnaire d’orientation»; the Lume portico drawn faint at the band's end | the route across, four stations | the route down the reading edge |
| S3 | «l'indice» — the eight regular pathways | paper · band | the index (eight rows, the registry glyph and the prescribed title, the 2 px marker on the reading edge) beside the stage (a raised sheet: tile, title, prescribed description, «Voir le parcours» where the sheet is published); the first is selected; the order is the locked order, no numeral | eight disclosure rows (40 px glyph tiles), one open at a time | the same rows |
| S4 | «il panorama» — the pilot | night · the page's one moment | the night column between two full-height 2:3 panels (cedar, marble — lane M's re-crops) developing from black and white into colour as the band arrives; the gold thread above and below the title; the lead «Le même geste, sur le cèdre et sur le marbre : deux savoir-faire, deux rives, un même projet.»; one link | the pair under the statement | the panels stacked (3:2), then the title, lead and link |
| S5 | «lo strato» — what the platform does and does not do | the masonry photograph under its veil · band | four plates, each a question, its «Non.» as the keyword and the locked answer whole; each plate opens its own FAQ entry (`/faq/#faq_visas` …); «Toutes les questions fréquentes» | two by two | one column |
| S6 | «la protezione» | stone · band | the one warning plate of every page, raised, its seal; the locked anti-fraud body set on its own full stops | same | same |
| S7 | «la campata» — the promoter | paper (stone when the news sits before it) · band | the working table under the arch (lane M's 4:3) beside the colophon: «Promoteur», AGAMI (Italian, LTR), the locked answer with «depuis 2011» and «Italie–Maroc» inked, «En savoir plus sur le promoteur» | the frame above the colophon | same |
| S8 | the reserved row | night · strip | the page's last door, slim: the T5 seal whose key is in the identity's gold and turns a quarter on its own button; «CONNEXION»; the footer continues the night (no gap, a soft night rule) | same | same |
| — | news (when an article is published) | paper | the V2 shell and a statement head; the cards unchanged | | |

**Gate G3 closed:** the hero and its line as above; S2 keeps the neutral stepper and ends on the editorial note
(«pré-évaluation à caractère informatif») and the call; S3 is the neutral families as a still index (no stage, no
destination) with the note of what comes; S5 is two plates («Ce que fait la plateforme» / «Ce qu’elle ne fait pas»);
no pilot, no warning plate, no reserved row; S7 as above.

**Arabic:** the mirror. The route and the index read in French where the text is locked French (`lang="fr"` on the
run, the route itself right-to-left in the page's order); the panels and the arch mirror; the colophon's name stays
LTR. **Italian and English:** the pilot's lead shows in French, marked `lang="fr"`, until the catalogue pass (§7).

**Motion:** one signature entrance per section, once, from the library's verbs (draw-y, stroke, develop, depth, light,
node); nothing loops; the keyboard and reduced motion see the designed still at once (every line drawn, every photograph
in colour, no state written).

**No JavaScript:** the content complete in reading order — the eight pathways as anchors then eight panels, the
doors as a stacked list, every locked text whole.

## 2. What changed in the code

- `apps/pages/services.py` — the data the sections need: the doors' glyphs; the orientation's stations (the locked
  sentence cut by `pathways.services.how_it_works`, its glyphs, the whole sentence, the caveat or the note as the
  route's terminal, the call as its arrival); the pathways' stages (anchor, title, glyph, description, the link only
  when the sheet is published); the trust plates' FAQ permalinks; `SectionView.ground` and `_grounds()`.
- `apps/pages/content.py`, `apps/pages/seeds.py` — the pilot's new lead; `SUPERSEDED_DEFAULTS` lets the seed bring a
  row still holding the old default to the new one, never an editor's text.
- `templates/pages/home/_*.html` — every section re-composed on the library (the hero: only its foot);
  `templates/components/entrances.html` — the `rail` branch (S1); new `_ecosystem_frame.html`,
  `_ecosystem_colophon.html`.
- `apps/pages/static/pages/css/pages.css` — rewritten: the library partials imported, the shell, S1–S8 and their RTL;
  `hero.css` — H0 only (the line, the fade, the foot); `static/css/v5/_casa.css` (new) — the home's gradients and
  threads, tokens only (app sheets may hold no gradient).
- `docs/design/DESIGN_SYSTEM_2026.md` — `pathway_list.html` has no consumer since V5.22.

## 3. 21st.dev provenance (rows for `COMPONENT_PROVENANCE.md`, lane S's columns; principles adapted, no code taken)

| Family | 21st.dev component (id · URL) | Taken | Not taken | ILE implementation | Wave |
|---|---|---|---|---|---|
| L · S3 index and stage | Feature Tab Switcher · 27081 · `21st.dev/@mohammadshehadeh/components/feature-11` (read in full) | a vertical tab list beside a panel that previews the selected item; the arrow keys move and the panel follows | the product chrome, autoplay, the animated panel swap, React | `templates/pages/home/_pathways.html` on `sezioni/indice.html` + `indice.js`; `pages.css` §6 | V5.22 H |
| J · S1 doors on phones | Snap Carousel · 23559 · `21st.dev/@ddoemonn/components/snap-carousel` | peek edges, snap, keyboard reach | drag physics, momentum flicking, dots, the headless hook | `components/entrances.html` (`rail=True`) on `_sec-passaggio.css` | V5.22 H |
| D · S4 pilot panels | Scroll Reveal Image · 24466 · `21st.dev/@unlumen/components/scroll-reveal-image` | the panel developing as the band arrives | blur, zoom, scroll-jacking | `_pilot.html` on `.panorama--coppia` and the verb develop | V5.22 H |
| K · S5 plates on stone | Spotlight · 35180 · `21st.dev/@kevingirelli/components/spotlight`; Corner Frame · 35211 · `21st.dev/@kevingirelli/components/corner-frame` | the plate's lit edge and depth under the hand | glow, glass | `_trust.html` on `sezioni/strato` (`.sez-plate`, verb depth) | V5.22 H |
| A · S7 the arch | SVG Clip Mask · 31436 · `21st.dev/@educalvolpz/components/svg-clip-mask` | the photograph seen through the brand's arch | the morph loop | `_ecosystem.html` on `sezioni/campata.html` (`frame="arch"`) | V5.22 H |
| I · H0 → S2 the line | Scroll animated timeline · 35029 · `21st.dev/@ibrandify/components/scroll-timeline` | a line drawn as it is reached | scrubbing, Lenis, GSAP | `.he__soglia`, `.orienta__soglia` (verb draw-y) | V5.22 H |

## 4. Budgets (gzip -9, Python `gzip.compress(…, 9)`, dist)

| Sheet | design-v5 `22b0ddd` | v522-h | Ceiling (§7.1) |
|---|---|---|---|
| `pages/css/pages.css` | 4 732 | **10 536** | 12 288 |
| `pages/css/hero.css` | 10 711 | **10 867** | 11 264 |
| `main.css` | 32 718 | **32 718** (untouched) | 32 718 |
| `core/reveal.css` · `core/portico.css` | 3 549 · 2 993 | unchanged | — |
| **Home, all sheets linked** | 54 703 | **60 663** | ≤ 61 440 |

JavaScript unchanged: `home.js` 7 357, `rise.js` 1 327, one section chunk on the home (`indice`, 1 088). Requests
before `load`: unchanged (the partials are bundled into `pages.css`; no new file is linked).

## 5. Review (headed chromium-1234)

- **Widths × languages:** 1440, 1280, 1024, 768, 430, 390, 375, 360 in fr, ar, it and en (32 runs, `r8/sweep.json`):
  horizontal overflow 0, no element of `<main>` wider than the page, console errors 0. The focus walk flagged only the
  trust plates' stretched links, whose ring is drawn on the plate by design (`.sez-plate:has(.sez-stretch:focus-visible)`,
  checked visually: `r8/focus_trust_*.png`).
- **axe-core 4.13** (WCAG 2.0/2.1/2.2 A and AA), the page played through first: 0 violations of any impact in 24 runs
  — fr, ar, it, en at 1440, 768, 390; fr and ar at 1440 and 390 gate closed, and under reduced motion in both gate
  states (`r7*/axe.json`).
- **Reduced motion, keyboard, no-JS, gate closed:** captured in `r3`, `r5`, `r7`; the stills are asserted in tests (§6).
- **Performance, indicative only** (8785 is runserver, not the compressed twin 8782 of §5.3; CPU × 4, slow 4G, n = 3,
  `r9/perf.json`): CLS 0.008–0.018 on fr and ar desktop and on the fr phone; on the ar phone up to 0.079, a single
  shift attributed to the root element when the «Lume» veil lifts (`html.lume-first`), no section of the home among
  its sources. The tabs' own switch costs 24–48 ms at rest; the first input of a visit costs more — the first Tab
  184–200 ms, the first pointer press 128–256 ms, most of it the document-wide restyle when `head.js` and `hero.js`
  set the input modality on `<html>` (the first Tab costs 56–96 ms on 8782, whose tree differs: 948 elements against
  1 354, of which +183 come from the home's sections). At rest: no long task, no running animation; `will-change`
  only on the loader's `.lume-veil__ground` and `.lume-veil__stage`. The gate is the integrator's, on 8782.

## 6. Tests

New (lane H):

- `apps/pages/tests/test_home_v522_h.py` — **18 passed**: every section a V2 section and no two grounds of one kind
  touching, both gate states; the grounds holding when the back office reorders or adds a section; the hand-off
  markup; the route as the locked sentence cut and said once, its French run in another language, the note when
  closed; the pathways' stage linking only a published sheet; the pilot's lead and the seed upgrade that never touches
  an editor's text; the trust plates' own FAQ permalinks (the FAQ keeps them) and the masonry ground; the warning plate;
  the promoter under the arch; the reserved key; the page-only sheets and their ceilings; the home's gold spent on
  three things and nothing of its own moving.
- `apps/pages/tests/test_home_browser_v522_h.py` — **11 passed**: the hero's line meeting the seal's sill (fr, ar at
  1440, 1024, 768); each section waits, plays once and holds nothing (V5.20 `getAnimations()`); reduced motion writes no
  state and draws the still; the index from the keyboard with the page not moving (fr, ar); drawn width = `sizes` for
  the pilot's panels and the arch at 1440, 1280, 1024, 768, 390 (fr, ar — lane M's request); the key turning on its
  button and never under reduced motion; the phone's rail crossed plate by plate, each focused plate whole (fr, ar).

Updated under the strict rule (V5.20), each change citing V5.22 / SECTION_SYSTEM_V2 §3.1 in place, every invariant kept
or made stronger, nothing loosened, no timeout raised, no skip:

- `apps/pages/tests/test_home.py` (77 passed) — the entrances, orientation, pathways, trust, antifraud and reserved
  tests read the V2 markup; the locked texts the V2 home sets in typographic levels (`p3.antifraud.body`, the trust
  answers, the promoter's answer) are held to their element's `textContent`, character for character;
  `test_the_chapters_carry_one_section_device_and_no_running_head` becomes
  `test_the_sections_open_with_one_head_and_no_glyph_above_a_title` (§3.1: one head per section, no glyph above a title).
- `apps/pages/tests/test_browser.py` (28 passed) — the banner without JavaScript, the doors as a rail on phones, the
  hero's edges, the phone with the gate open, and `test_the_home_under_the_hero_is_one_system` rewritten on the V2 sections.
- `tests/frontend/test_french_typography_w2_d.py` (13 passed; family w2-d, no V5.22 lane holds it) —
  `test_the_home_draws_its_own_strings_with_the_spaces_and_the_locked_copy_as_written`: the team-authored sentence it
  checks for the no-break space is now the pilot's new lead («sur le marbre», U+00A0, «: deux savoir-faire»); the trust
  answers and the anti-fraud body, re-composed in typographic levels, are held to their element's `textContent`; the
  count of every no-break space the filter wrote is unchanged.

Runs on the final tree (one pytest at a time, `test_ile_v5_l5`):

| Suite | Result |
|---|---|
| `test_home_v522_h.py` + `test_home.py` | 95 passed |
| the rest of `apps/pages/tests`, not browser | 370 passed |
| the other suites that open the home (partners gate, Forum banner, news views, portal compliance, public pages, imagery V5.12, go-live calendar, HTML compression, error pages, legacy URLs, MFA middleware) | 131 passed |
| `test_home_browser_v522_h.py` + `apps/pages/tests/test_browser.py` | 39 passed |
| `tests/frontend/test_browser.py` + `test_motion_browser_w4_b.py` | 24 passed |
| `test_mobile_rtl_w4_a.py` + `test_reduced_motion_w1_d.py` (home, focus, reduced motion) | 9 passed |
| `test_frontispiece_v515_c.py` + `tests/i18n/test_rtl_browser.py` (browser) | 23 passed |
| `tests/frontend` + `tests/i18n`, not browser | 2 852 passed, 2 xfailed, 10 failed: the typography test above (since updated, 13 passed) and the nine expected reds below |
| ruff check and format, `manage.py check`, `makemigrations --check` | clean |

Expected reds owned elsewhere (requests in §8): `tests/frontend/test_chapter_marks.py` (the home's old chapter
devices), `tests/frontend/test_journey_w3_d.py::test_the_home_draws_the_orientations_neutral_steps_on_the_public_passage`
(the home's old include string), `tests/i18n/test_catalogues.py` (the two new msgids until the catalogue pass); red on
`design-v5` before this lane: `test_rtl_static` (`_sec-tracciato`), `test_loader_rules` (`data-seat`),
`test_state_chips` (`data-register`).

## 7. New user-facing strings (FR msgids; professional it/en/ar for the catalogue pass)

Entries ready to paste: `evidence/v522/h/catalogue_entries_{it,en,ar}.po`. Locked text is never translated: the route's
stations, the pathways, the answers stay the locked French where no locked translation exists, marked `lang="fr"`.

| msgid (source) | it | en | ar |
|---|---|---|---|
| «Le même geste, sur le cèdre et sur le marbre : deux savoir-faire, deux rives, un même projet.» (`apps/pages/content.py`, the pilot's lead; replaces «Des besoins des entreprises au suivi : la séquence du projet pilote, étape par étape.») | Lo stesso gesto, sul cedro e sul marmo: due saperi, due sponde, un unico progetto. | The same gesture, on cedar and on marble: two crafts, two shores, one project. | الحركة نفسها، على خشب الأرز وعلى الرخام: حرفتان، وضفّتان، ومشروع واحد. |
| «Voir le parcours» (`apps/pages/services.py`, the stage's link) | Vedi il percorso | View the pathway | عرض المسار |

Arabic reviewed: «الحركة نفسها» is the catalogue's existing rendering of «Le même geste» (the panel's label);
«ضفّتان» is the usual word for the Mediterranean's two shores; «عرض المسار» follows «عرض مساراتي» («Voir mes parcours»).

## 8. Requests to other lanes

- **S:** (1) `tests/frontend/test_chapter_marks.py` keeps the home's exception «until lane H recomposes it»
  (`HOME_EXPECTED = {"/fr/": {"compass", "signpost"}}`): the home now passes the rule every other page holds — no
  bare mark, no glyph above a title, each seal once (`ile-orienta`, `ile-scudo`, `ile-accesso`, checked on /fr/ and
  /ar/) — so the exception can go, a stronger invariant.
  (2) `test_journey_w3_d.py::test_the_home_draws_the_orientations_neutral_steps_on_the_public_passage` matches the old
  include string; the home now includes `stepper.html size="large" … across=True origin_seal="ile-orienta"
  terminal=… end_action=…`. (3) `sezioni/indice.js` switches to tabs at a hard-coded 64 rem; §3.1 S3 asks for the tabs
  from 48 rem — a hook (`data-wide` or a custom property) would let the home choose. (4) `stepper.html` puts `lang` on
  the `<ol>`, and the library's French-run rule turns the whole route left-to-right on RTL pages; the home counters it
  (`[dir="rtl"] .page-home .sez ol[lang] { direction: rtl; }`), every other consumer still needs it in the library.
  (5) `DESIGN_SYSTEM_V5.md` PX05 still names the home as a consumer of `pathway_list.html`.
- **Steward:** OWNERSHIP family `v522-h` with its new files (`static/css/v5/_casa.css`,
  `templates/pages/home/_ecosystem_frame.html`, `_ecosystem_colophon.html`, the two test modules); after the merge,
  `manage.py seed_all --only pages.home_sections` on each shared database (the untouched old pilot lead moves to the
  new one); the catalogue pass with the entries of §7; the preview label; the provenance rows of §3.
- **P2:** keep the FAQ permalinks `faq_visas`, `faq_recruitment_agency`, `faq_preassessment_guarantee`,
  `faq_diplomas` — the trust plates open them (asserted in `test_home_v522_h.py`).
- **M:** the ecosystem's 4:3 under the arch is drawn at about 50–57 vw on desktop, where its softness shows (your
  §9.12); a sharper source in the next imagery pass.
- **Integrator / shell:** measure LCP, CLS and INP on 8782 after the merge (§5); if the first input of a visit passes
  200 ms there, the cost is the document-wide restyle of the input-modality switch; the loader's veil holds
  `will-change` at rest.

## 9. Deviations and not done

- The index is tabs from 64 rem, not 48 rem (S's module; request above). Between 48 and 64 rem it is the disclosure.
- S1 shows on phones only: from 40 rem the hero's four origins already are the doors (V5.15's rule against a block that
  repeats the hero's question, kept).
- On a phone the trust band is long (about 1 560 px): the four locked answers stay whole, never truncated.
- LCP, CLS and INP on 8782 are the integrator's (§5 gives indicative numbers only).

## 10. Scores (§10; self-assessed at 1440 and 390, fr and ar; the reviewer verifies)

| Dimension | Before (audit) | Target | Self-assessed fr | Self-assessed ar |
|---|---|---|---|---|
| Composition | 2.5 | 4.5 | 4.5 | 4.5 |
| Motion | 2.5 | 4 | 4 | 4 |
| Imagery | 2.5 | 4 | 4 | 4 |
| Interaction | 2 | 4 | 4 | 4 |
| Institutional | 3.5 | 4.5 | 4.5 | 4.5 |
| Coherence | 3 / 2.5 | 4.5 | 4.5 | 4 (the route's direction rests on the home's counter-rule until S fixes the library) |

---

## 11. Round 1 improvements (label `v522-h-improve1`, 2 November 2026)

Answer to `evidence/v522/h/QA_ROUND1.md` (head `b9b4617`, NOT PASSED, 4 major, 12 minor). Same branch and worktree;
design-v5 has not moved since `22b0ddd`, so no merge was needed. Lane server 8785 on `ile_v5_l5`, tests on
`test_ile_v5_l5`, headed `chromium-1234` under lock slots A or B, at most 25 minutes a session, released between
sessions. A base server from the design-v5 worktree ran on 8775 for the paired measurements and was stopped at the end.
Scripts and raw output are in `C:/tmp/ile_v5_council/.work/v522-h-imp1/`. Captures are in `evidence/v522/h/imp1/`.

### 11.1 What changed, finding by finding

| Finding | What the owner now sees | Where |
|---|---|---|
| **M1 a**: the hand-off | The orientation's head follows the hero's statement at the foot's own distance (24 px + 24 px; 0–40 px measured between the statement's box and the head). The «150 px of empty wash» is gone. The hero's line now leaves from a station node: the hero's own 9 px bronze ring at the statement's first line. It runs down the reading edge beside the statement and the head without a break. Its foot turns into the origin seal's sill on a 12 px corner, the hero's radius, so the corner is the only way into the route. The condition «the orientation comes right after the hero, the phone's doors excepted» is computed once (`services._hand_off`, class `home-orientation--soglia`). The four `:is(.he + …)` selectors are gone. | `_hero.html` (foot), `hero.css`, `_orientation.html`, `pages.css` §5, `_casa.css`, `services.py` |
| **M1 b**: S2 | The route's origin is the body seal from 64 rem: 40 in 72 × 88, as §3.1 S2 asks (the route's marks row and column follow). Its face is the raised paper of the wash (§4.4) and its edge the route's ink, so it no longer reads as a grey headstone. The needle's north half is filled, as a compass's is, from one gradient defined in the portico's drawing, so it no longer reads as a leaf. From 64 rem the process head sets its lead beside its title, as the statement heads do, so the right 55 % of the band is no longer empty. | `_orientation.html`, `pages.css` §2, §5 |
| **M1 c**: «la protezione» | It is no longer centred. The build round's `margin-inline: auto` is gone, and the plate hangs from the reading edge under the tablet's own edge, at its own 56 rem measure, as on every page. A two-column layout across the container was built and measured, then dropped: it left the warning's column half empty, and on the Arabic page a left-to-right French body would have put the warning on the far side. No hairline separates S5 and S6: the masonry fades into the same stone. | `pages.css` §8, `_antifraud.html` |
| **M1 d**: the key | The key alone is drawn in the identity's gold, by `.page-home .home-reserved .sigillo.home-reserved__sigillo .sg-g--key` (0,5,0), which beats the night seat's ink. The doorway it stands in keeps the night's ink. Measured: the key's colour is `--identity-key`. | `pages.css` §10 |
| **M1 e**: the arch | The picture is clipped to the arch itself (`--card-radius`), so the foot stands square on the sill (the bottom corners measure 0 px). The sill and the arch's outline, 12 px out, standing on the sill's ends, are one decorative drawing, each line drawn once (the verb «stroke»). The photograph rises in the arch: the verb «mask» on the frame's own wrapper, its first frame a low segment of the arch, and its credit never masked. It settles from 1.04 to 1 over `--motion-draw`. Both run on `--ease-sine`: on `--ease-enter` the arch was open within a tenth of its course, too soon to be seen. Lane S's own `arch` verb has no `from` keyframe and flips its clip at mid-course. On the home its course is spent before it starts: `--sez-d: -900ms`, the vocabulary's own delay, reset to 0 on the frame's wrapper and on the sill. No `!important`, so the template guard holds. Lane S's settle on the image is cancelled by the shell's `animation: none` (0,5,2 over 0,5,1), so the settle is the image's own transition on a duration token. Probed at 100 ms steps: the media's clip is `none` from the first frame of «in», the aperture rises from 42 % to 0 in about 600 ms, the image settles in about 600 ms, and the outline draws from 300 to 1 100 ms. Both go to lane S (§11.5). | `_ecosystem_frame.html`, `pages.css` §9 |
| **M1 f**: rhythm | The paper bands (pathways, ecosystem) and the integrity band use `clamp(48, 6vw, 80)` instead of `clamp(64, 8vw, 96)`. The band after «la protezione» is tightened the same way. At 1440 the bands are now orientation 654, pathways 698, pilot (the moment) 738, trust 902, antifraud 613, ecosystem 861 and the reserved strip 169. Before they were 758 / 730 / 738 / 868 / 629 / 893 / 169. The page is 6 112 px, against 6 262. | `pages.css` |
| **M1** (trust): «four equal white cards on a grey veil» | The four answers are **one raised tablet set into the wall**. Its four fields are laid in the masonry's running bond, 5 \| 7 over 7 \| 5 from 48 rem, so the joints never line up, like the courses behind them. The way to every question («Toutes les questions fréquentes») is the tablet's plinth. The veil is deep (88 %) under the head, so the words read, and light (42 %) around the tablet, so the dressed courses read as stone, not murk. The tablet settles once over its shadow layer (DEPTH), and the «Non.» rules draw 60 ms apart. A field answers the hand and the focus with a lit top edge (a 2 px accent line) and its ring inside the field. It never lifts: a slab does not float. Each question still opens its own FAQ entry. | `_trust.html`, `pages.css` §8, `_casa.css` |
| **M2 a**: route labels (ar) | Each French station label is its own left-to-right box hanging from its station's edge, its lines starting on its own start. The build round had end-aligned, ragged-start text. Measured: `direction: ltr`, `text-align: start`, the box's edge on the station's edge within 1 px. | `pages.css` §5 |
| **M2 b**: stage (ar) | The panel's one column is `fit-content(var(--measure-lead))`, laid from the reading edge. The French title and description share one start edge (measured within 1 px). The description carries its own `lang`. The way to the sheet («Voir le parcours») is said in the page's language, outside any French box (m4). | `pages.css` §6, `services.build_pathways` |
| **M2 c**: the folio (ar) | `.colofone__label:lang(ar)`: the page's own face, no tracking, no capitals. Measured: not ILE Mono, letter-spacing `normal`. The library's `.testa__label` goes to lane S (§11.5). | `pages.css` §9 |
| **M3**: INP | Measured and diagnosed (§11.3). The first input of a visit restyles the whole document because of **one rule in `motion.css`** (main.css, a preserved family), not because of the V2 verbs: `[data-input="key"] .accordion__item::details-content`. With that rule left out, the first Tab drops from 184 to 96 ms median on the home (base: 152 to 72). The fix belongs to that rule's owner (§11.5). `content-visibility: auto` on the home's bands was built and measured, then dropped: it cut the restyle, but focus navigation then forced six layouts on the first Tab (keydown 506 ms traced). | measurement only |
| **M4**: strings and guards | This round adds no new string. The two build-round msgids are still the merge's to carry: `evidence/v522/h/catalogue_entries_{it,en,ar}.po` was re-verified, each msgid byte-identical to `apps/pages/content.py` and `services.py`. The S guards (`test_chapter_marks.py`, `test_journey_w3_d.py`) and `seed_all --only pages.home_sections` are unchanged requests (§8, §11.5). | evidence |
| **m1**: gate closed | The five neutral families are the index's own rows across the band, three across from 48 rem. Each has its tile: the registry's glyph of the pathways it gathers, from `content.PATHWAY_FAMILY_KEYS` through `icons.PATHWAY`, decorative. The note of what comes sits under them. Nothing to select, nothing to open. | `_pathways.html`, `content.py`, `services.py`, `pages.css` §6 |
| **m2**: S3 entrance on phones | The pathway titles are wrapped at render in a span carrying the verb «ink» (the text is the locked title, character for character). The disclosure rows of a phone now come to their ink 60 ms apart, in the index's own order (`--sez-i` from `sibling-index()`). | `services.build_pathways`, `pages.css` §6 |
| **m3**: the route's light | The light along the route on the end call's hover or focus is now a 4 px pass of `--accent-text` over the 2 px route, one station after another (measured opacity 0 → 0.9 → 0, 120 ms apart). | `pages.css` §5 |
| **m4**: language of parts | See M2 b. Until the catalogue has «Voir le parcours», the link is the French it falls back to and carries `lang="fr"` (`services.ui`), then the page's language. | `services.build_pathways` |
| **m5**: «VÉNÉTIE– / MAROC» | `{{ d.title\|emphasize:"VÉNÉTIE–MAROC" }}` sets an emphasis-free span with `white-space: nowrap`, and the heading's textContent is the locked title. The display size never lets the run outgrow its column: `min(--t-display, (100cqi − 2 × page-pad) / 8.6)`, and from 64 rem `(40cqi − 4rem) / 8.6`. Measured at the 7 widths 360–1440: two lines, «PROJET PILOTE / VÉNÉTIE–MAROC», always inside the seam or the panel. | `_pilot.html`, `pages.css` §7 |
| **m6**: the doors | The seat is a lunette: its arch rises the seat's whole height, so it reads as a doorway, not a header band. The call follows its sentence, and the plates' common height gathers under the call. | `components/entrances.html`, `pages.css` §4 |
| **m7**: trust on phones | One tablet, no gaps, tighter fields: 1 458–1 476 px at 390, fr and ar (was 1 557). The four locked answers stay whole, so the §3.1 estimate of about 820 px is not reachable without cutting a locked text (§11.6). | `pages.css` |
| **m8**: S2 at 768 | From 48 to 64 rem the station labels are at body size: three lines, and four for the longest. | `pages.css` §5 |
| **m9**: soft ecosystem frame | Lane M's (unchanged request, §8). | — |
| **m10**: the key out of the eye's path | The seat stands beside «CONNEXION» (measured 20 px from the button), so the key turns where the eye already is. The words hang from the reading edge. | `_reserved.html`, `pages.css` §10 |
| **m11**: page length | See M1 f. 1440: 6 112 px (6 262). 390: 9 204 px (9 342). | — |
| **m12**: notes accuracy | Corrected here. The key is now really gold. The build round's «768: the pair under the statement» is in fact above it. The build round's indicative LCP from `r9/perf.json` on runserver was 3.1–4.0 s, not comparable to 8782. The shared design-system doc hunk of the build round stays for the steward to read. | — |

### 11.2 Budgets (gzip -9, dist, after `npm run build`)

| Sheet | Round 0 (b9b4617) | Round 1 | Ceiling |
|---|---|---|---|
| `pages/css/pages.css` | 10 536 | **11 263** | 12 288 |
| `pages/css/hero.css` | 10 867 | **10 899** | 11 264 |
| `main.css` | 32 718 | **32 718** (untouched) | 32 718 |
| `core/reveal.css` · `core/portico.css` | 3 549 · 2 993 | unchanged | — |
| **Home, every sheet linked** | 60 663 | **61 422** | ≤ 61 440 |

The total was over the ceiling (61 993) after the first pass. It came back under without touching any other lane's sheet:
- the news' empty-row rules were removed: the row is never drawn, because `build_news` returns no section without an article, and if it ever is, the shared component styles it (comment in `_news.html`);
- the S2 hand-off condition became one class;
- SVG presentation (fill, stroke width, `vector-effect`, overflow) moved to the drawings' own attributes;
- the bond's spans were written as two rules;
- rules the library already says were dropped.

The lane's own guards (`test_templates_static.py`) caught three things in the first pass, all now fixed:
- a gradient in an app stylesheet: the field's lit edge moved to `_casa.css`, the home's partial for grounds and threads;
- an `!important`: replaced by the vocabulary's negative delay;
- a literal duration: now `--motion-draw`, zeroed under reduced motion like every token.

JS is unchanged (home.js 7 357, rise.js 1 327, the indice chunk 1 088). `npm run build` is reproducible: only the two page sheets changed.

### 11.3 M3: the measurements behind the diagnosis

All runs used headed chromium-1234 with CPU throttled ×4 (CDP), 1440 × 900, lane 8785 and base 8775 (design-v5 `22b0ddd`),
the same database and runserver. The machine was not quiet (other lanes' browsers ran), so every cell is paired with the base.

- **First Tab, Event Timing**, n = 5 interleaved: lane 184 ms median, base 152. The S3 tab click on the lane was 48–56 ms. The phone disclosure tap (412 × 823, touch) was 104–136 ms (median 112–128 over two series).
- **Trace of the first keydown**: the lane spends 154–158 ms in two `UpdateLayoutTree` passes, the first restyling **974–1 155 of 1 385 elements**. The base spends 92–109 ms on 853 of 1 180.
- **Which sheet?** The `data-input` flip was replayed with each sheet disabled. Without `main.css` it restyles 304 elements. Without `pages.css` it still restyles 1 046, and without `hero.css` or `reveal.css` it still restyles the whole page. Replaying `main.css`'s 14 `data-input` rules one by one, 13 cost 304–387 elements. One costs **1 328**: `@media (prefers-reduced-motion: no-preference) { @supports selector(::details-content) { … [data-input="key"] .accordion__item::details-content { … } } }` in `static/css/v5/motion.css`. Blink cannot scope an invalidation that ends on that pseudo-element, so it invalidates the whole subtree.
- **What if**: `main.css` was served less that one rule (a constructed sheet, n = 5). The first Tab drops from 184 to **96 ms** median on the home and from 152 to 72 on the base.
- The home's own share: +205 elements (the V2 sections) at about 14 µs an element unthrottled. The V2 verbs' `:root:not([data-input="key"])` prefix is not the culprit: those rules cost about 304 elements together.
- Rejected: `content-visibility: auto` on the home's `.sez` bands. It cut the first restyle to 974 elements, but the Tab's focus navigation then forced the skipped bands' style and layout: 7 `UpdateLayoutTree` and 6 `Layout` passes, 506 ms traced. Reverted.

### 11.4 Tests

New in `apps/pages/tests/test_home_v522_h.py` (27 passed):
- the hand-off computed only right after the hero;
- the hand-off class and the needle's one gradient;
- the trust tablet and its plinth, and the bond's spans;
- the closed gate's family tiles;
- the stage's languages of parts and the inked title span (ar);
- the pilot's nowrap span and its text;
- the reserved seat beside its button and the gold rule;
- the arch's rising wrapper and its drawing;
- the plate never centred, the 72 × 88 seal, the Arabic labels' and stage's rules, the Arabic folio.

New in `apps/pages/tests/test_home_browser_v522_h.py` (13 passed): `test_round_1_…` (fr, ar, 1440, reduced motion) measures:
- the head 0–40 px under the statement;
- the seal at 72 × 88;
- the plate on the tablet's reading edge;
- the key in the computed identity gold, within 32 px of its button;
- the arch's foot square;
- the drawing 24 px wider than the frame;
- in ar: each French label's own box and start, one start edge for the stage, the folio not monospaced nor tracked.

Updated under the V5.20 strict rule, `apps/pages/tests/test_home.py`, two assertions:
- `test_phase3_prescribed_texts_present_when_open`: `p3.pilot.title` joins `RECOMPOSED`;
- `test_the_morocco_italy_model_is_said_once_by_the_heros_path`: the pilot block.

Both now hold the title to its heading's textContent, exactly the locked title, where they held it to an unbroken substring of the HTML. The span is a render-time re-composition allowed by SECTION_SYSTEM_V2 §1 rule 6, an approved decision, here for QA_ROUND1 m5. The invariant is the same text, checked on the whole element, so it is stronger. Nothing was loosened, no timeout raised, no skip added.

Headed checks, chromium-1234 under a lock slot. Evidence is in `evidence/v522/h/imp1/`: `sweep/`, `sweep_closed/`, `axe/`, `closed/`, `final2/`, `arch2/` and `r1`–`r6`.
- **Sweep:** 8 widths × fr, ar, it and en, gate open. Overflow 0 in 32 runs, no element of `<main>` wider than the page, 0 console errors. The 4 focus stops the walk flags are the trust questions' stretched links, whose ring is drawn on their field by design (captured: `focus_cell_*.png`). The one wide element found at 360 (the pilot title's nowrap run) was fixed by the column-fitted size; per-width measures are in §11.1 m5.
- **Gate closed:** fr and ar × 8 widths, overflow 0, no flagged focus.
- **axe-core 4.13:** WCAG 2.0, 2.1 and 2.2, A and AA, page played through first. **0 violations in 12 runs**: fr, ar, it and en at 1440 and 390, plus fr and ar under reduced motion.
- **Probes:** the arch's entrance at 100 ms steps; the route light's flash per station; the reserved key's colour; the protezione's edge; the Arabic labels and stage edges (the browser test above).

Runs on the final tree, one pytest at a time on `test_ile_v5_l5`:

| Suite | Result |
|---|---|
| `test_home_v522_h.py` + `test_home.py` + `test_templates_static.py` + `tests/frontend/test_journey_w3_d.py` + `tests/i18n/test_page_integrity.py` + `tests/frontend/test_frontispiece_v515_c.py` + `tests/frontend/test_design_docs.py` (the final tree) | 427 passed, 1 failed: `test_journey_w3_d::test_the_home_draws_the_orientations_neutral_steps_on_the_public_passage`, lane S's guard on the old include string (§8, expected) |
| `apps/pages/tests` (not browser) + `tests/compliance/test_locked_content.py` | 488 passed, 2 failed in the first run (`test_templates_static.py`: the `!important` and a literal transition duration; both fixed, and the module re-run: 132 passed) |
| `tests/frontend` + `tests/i18n` (not browser) | 2 851 passed, 2 xfailed, 11 failed in the first run. Two were this round's and are fixed, then re-run green: the stage link's French fallback without its `lang` (`test_page_integrity`), and the home sheet naming the passage's classes (`test_one_rail_drawing_and_one_passage_drawing_never_a_third`, now `.linea-v2` and elements). The other 9 are the build round's expected reds: `test_chapter_marks` and the journey include string (lane S), `test_catalogues` ×4 (the merge's catalogue), and `test_rtl_static`, `test_loader_rules`, `test_state_chips` (red on design-v5 before this lane). |
| `test_home_browser_v522_h.py` | 13 passed (the final tree) |
| `apps/pages/tests/test_browser.py` | 28 passed (the final tree) |
| ruff check and format (`apps/pages`) | clean |

### 11.5 Requests to other lanes (new this round)

- **Lane S:**
  1. `sez-arch` (`_sec-campata.css`) has only a `to` keyframe. From the `in` state's `clip-path: none` it is not interpolable, so the clip flips at mid-course to a semicircle and back. Give it the `from` of its wait rule. Meanwhile the home spends its course at once (`--sez-d: -900ms`).
  2. `_sezioni.css`'s `:root:not(.rm) .sez [data-reveal="mask"]:not([data-grade="bw-scroll"]) > picture > img { animation: none }` (0,5,2) cancels `_sec-campata.css`'s settle (0,5,1) on every page. Exempt `.campata__media`, or raise the settle.
  3. `.testa__label:lang(ar)`: the page's face, no tracking, no capitals. The home sets it on `.colofone__label` only.
  4. In `_sec-indice.css`, the disclosure rows (a phone) have no entrance of their own. The home inks its titles through a span from its service; the library could do it for every page.
  5. Unchanged from §8: the chapter-marks and journey guards, the 48 rem tabs hook, the `ol[lang]` direction.
- **Owner of `static/css/v5/motion.css`** (main.css, the Lume and motion family, preserved, so through the steward): the `::details-content` rule above makes every page's first keyboard or pointer input restyle the whole document. Moving the modality out of that selector, for example a custom property set on `.accordion__item` under `html[data-input="key"]` and read by `::details-content`, would scope it. Measured gain on the home: 184 → 96 ms (§11.3). This is the M3 fix. Lane H cannot make it.
- **Steward:** unchanged from §8 (OWNERSHIP rows, `seed_all --only pages.home_sections`, the catalogue entries, the preview label, the provenance rows). New file rows: none.
- **Lane M:** unchanged (m9, the ecosystem frame's softness).

### 11.6 Deviations and not done

- «la protezione» hangs from the reading edge at its own measure instead of spanning the container (the reviewer's first option). The spanning two-column plate was measured and dropped (§11.1 M1 c).
- M3: the root cause is in a preserved family. The home's first Tab stays at the base plus about 30 ms (184 against 152 median in this lane's final series, max 304 on a busy machine). The reviewer's quieter-machine numbers (200 / 208) need the motion.css fix to be safely under 200.
- m7: the trust band on a phone is about 1 470 px. Reaching 820 would need shortening a locked answer, which is not allowed.
- The settle of the ecosystem's photograph is a transition (1.04 → 1, `--motion-draw`, `--ease-sine`), not the verb itself, because the library's verb is cancelled by its own shell (§11.5, S 2).
- The phone index's 60 ms order comes from `sibling-index()` (Chromium). Where it is not supported, the rows ink together: the delay falls back to 0 and nothing is held.
- The pilot's moment is still 82 vh (§3.1), shorter than the integrity band (902 px). The 2:3 panels would crop past lane M's re-crops at a full viewport.

### 11.7 Self-scores (§10; fr and ar, 1440 and 390; the reviewer verifies)

| Dimension | Round 0 (reviewer) | Round 1 (self) fr | Round 1 (self) ar |
|---|---|---|---|
| Composition | 4.0 | 4.5 | 4.5 |
| Motion | 4.0 | 4.5 | 4.5 |
| Imagery | 4.0 | 4.0 | 4.0 |
| Interaction | 4.0 | 4.0 (INP rests on the motion.css fix) | 4.0 |
| Institutional | 4.5 / 4.0 | 4.5 | 4.5 (it/en/ar wait for the catalogue merge) |
| Coherence | 4.0 / 3.5 | 4.5 | 4.5 |

## 12. Round 2 improvements (label `v522-h-improve2`, 2 November 2026)

Answer to `evidence/v522/h/QA_ROUND2.md` (head `88999bb`, NOT PASSED, 2 major, 8 minor). Same branch and worktree;
design-v5 is still `22b0ddd`, so no merge was needed. Lane server 8785 on `ile_v5_l5`, tests on `test_ile_v5_l5`, headed
`chromium-1234` under lock slot B, at most 25 minutes a session, released between sessions. For the paired measures two
more dev servers ran on the same database and were stopped at the end: 8775 = the base `22b0ddd` (the design-v5
worktree) and 8774 = the round-1 head `88999bb` (a detached worktree, `C:/tmp/ile_wt/v522-h-r2prev`, removed at the end).
Scripts and raw output: `C:/tmp/ile_v5_council/.work/v522-h-imp2/`. Captures: `evidence/v522/h/imp2/` (`before/`,
`after2/`, `labels_try/`, `arch/`, `arch_seek/`, `perf/`, `sweep/`, `modes/`).

### 12.1 What changed, finding by finding

| Finding | What the owner now sees | Where |
|---|---|---|
| **M1 a**: the reserved row (ar, from 64 rem) | The French title and its sentence are one quotation hung from the reading edge: the title takes the sentence's measure, so both start on the box's own edge. Measured: title and sentence start at x 868 / 868 (1440), 716 / 716 (1280), 513 / 513 (1024), 267 / 267 (768), 16 / 16 (390, 360). Before: 328 / 868 and 267 / 513. | `pages.css` §10 |
| **M1 b**: the phone index (ar) | Each disclosure row reads, from the reading edge, tile · title … chevron. The inserted button keeps the page's direction and only the French title runs left to right in its own isolate, as the tab rows already did. Measured at 390: button `direction: rtl`, the chevron's end margin on the left (6 px), the title's ink between the chevron and the tile (one-line titles hug the tile: ink 186–307 beside the tile at 319). | `pages.css` §6 |
| **M2**: INP | Not closable in lane H's files: the root cause is the preserved `motion.css` rule (§12.3), and most of the rest is the library's own `[data-input]` rules. What lane H could do, it did: every rule of the home's sheet that Blink cannot file under a class (an `:is()` or a bare `:nth-child` as its subject) is now written so that it can, and the ecosystem's keyboard rule names its image's class instead of the `img` tag. Measured gain: small, inside the machine's noise (§12.3). The requests are in §12.5. | `pages.css` (selectors only, no visual change) |
| **m1**: the arch draws as dashes | The outline grows as one line from a foot, over the crown, to the other foot, and the sill as one line from its end. The drawing keeps its 1 px non-scaling stroke; each line's `pathLength` now makes the verb's single dash longer than the line on screen at every width (the arch 0.125, the sill 0.1: dashes of 2 080–2 150 px and 1 000 px against measured lines of 699–1 947 px and 337–968 px). **Corrected in the final fix round (QA_ROUND3 m1, m4; §13.1):** this held on a 1× screen only. The dash is laid in device pixels, so on the reviewer's 1.25× display a detached piece of the far leg showed first at 880–1023 px and from 1600 px, and on a 2× or 3× screen both lines drew as pieces. The frames had been sought at 1440, 1024 and 390, at 1×. | `_ecosystem_frame.html` |
| **m2**: the phone index inks at once | The eight rows ink in the index's order, 60 ms apart (0, 60 … 300 ms, the library's six steps). Each panel carries its rank as an integer (`.indice__pannello:nth-child(n)`, as the library's rows do); the unregistered `sibling-index()` is gone. Measured delays on the titles' spans: 0 s, 0.06 s, 0.12 s, 0.18 s, 0.24 s, 0.3 s, 0.3 s, 0.3 s. | `pages.css` §6 |
| **m3**: the colophon (ar) | The name, in its two parts, and the French answer are one left-to-right box hung from the reading edge: the name's `text-align: end` is gone, so both start on the same edge (x 92 / 92 / 92 at 1440, 32 at 1024, 16 at 390). The Arabic folio and button keep the page's direction. | `pages.css` §9 |
| **m4**: the route's labels (ar) | Each French caption stands at a caption's measure (12.5 em), hung from its own station's edge, never across its whole column: at 1440 the four boxes start 42 px further from the previous station (the second caption 66 px clear of the third station's tile instead of 24) and three of them keep two lines. Candidates 72 %, 80 %, 11 em, 12 em and 12.5 em were measured at 1440, 1280, 1024, 768 and 390 (`labels_try/`): 12 em broke «pré- / évaluation»; 12.5 em does not. | `pages.css` §5 |
| **m5**: «la protezione» title (ar) | Lane S's partial: request in §12.5. | — |
| **m6**: rhythm | Not changed: the Director's call (§3.1 sets 82 vh from 64 rem). The moment would need a full viewport and the 2:3 panels would then crop past lane M's re-crops. | — |
| **m7**: notes accuracy | Corrected here: the budgets of §12.2 are measured on the dist after `npm run build`; the phone rows' order is now measured, not assumed. | — |
| **m8**: carried | The merge conditions are unchanged except one: «Voir le parcours» is withdrawn (below), so the catalogue entries carry only the pilot's lead. | `evidence/v522/h/catalogue_entries_{it,en,ar}.po` |
| Institutional (it/en/ar) | The stage's way to a pathway's sheet is now said in the page's language: it is the product's own words for that way, the orientation result's «Consulter la page du parcours», a msgid the it/en/ar catalogues already hold («Consulta la pagina del percorso», «See the pathway page», «الاطلاع على صفحة المسار»). The French fallback and its `lang="fr"` are gone from the stage; no new msgid. The pilot's team lead stays French on it/en/ar until the merge carries its entries. | `services.build_pathways` |

### 12.2 Budgets (gzip -9, dist, after `npm run build`)

| Sheet | Round 1 (`88999bb`, measured) | Round 2 | Ceiling |
|---|---|---|---|
| `pages/css/pages.css` | 11 252 | **11 281** | 12 288 |
| `pages/css/hero.css` | 10 899 | 10 899 (untouched) | 11 264 |
| `main.css` | 32 718 | 32 718 (untouched) | 32 718 |
| `core/reveal.css` · `core/portico.css` | 3 549 · 2 993 | unchanged | — |
| **Home, every sheet linked** | 61 411 | **61 440** | ≤ 61 440 |

- The round's rules cost 33 B. Four came back without touching any other lane's sheet: the closed gate's note and the
  section note had identical declarations, so they are one rule now; and the banner's RTL lines, written as class-led
  selectors, cost nothing in gzip.
- The home now sits exactly at its ceiling (0 B headroom). `test_frontispiece_v515_c.py` holds it (≤). Any later change
  to the home's sheets has to pay for itself.
- One cheaper-looking rewrite was measured and dropped because gzip made it dearer: the door arrow's direction as one
  `calc()` on `--sez-dir` instead of its four rules (+5 B).
- JS is unchanged (home.js 7 357, rise.js 1 327, the indice chunk 1 088). `npm run build` is reproducible: only
  `dist/pages/css/pages.css` changed.

### 12.3 M2: what lane H can and cannot close

All runs: headed chromium-1234, CPU throttled ×4, 1440 × 900, cold loads, three dev servers on the same database —
8775 the base `22b0ddd`, 8774 the round-1 head `88999bb`, 8785 this round — interleaved, the order turning each round.
The machine was busy (two other lanes' headed sessions), so only paired differences mean anything. Raw: `imp2/perf/`.

- **Event Timing, the first Tab (keydown duration), median (max):**

  | Run | Base | Round 1 | Round 2 |
  |---|---|---|---|
  | desk fr, n 7 | 168 (216) | 224 (392) | 288 (416) |
  | desk ar, n 7 | 208 (336) | 280 (536) | 264 (368) |
  | desk fr, n 9 | 152 (280) | 248 (416) | 272 (576) |

  The two lane heads overlap inside the noise; both stay about 60–120 ms above the base.
- **The style recalc inside that keydown** (UpdateLayoutTree, trace, n 7, fr), median (min) and elements restyled:

  | | Base | Round 1 | Round 2 |
  |---|---|---|---|
  | served | 141.7 (78.0) ms, 853 | 183.5 (148.3) ms, 1 139 | 176.9 (143.3) ms, 1 138 |
  | `motion.css` rule dropped from the CSSOM | 122.0 ms, 294 | 147.7 ms, 510 | 149.5 ms, 509 |

- **Why.** Two causes, neither in a lane H file:
  1. The preserved `motion.css` rule `[data-input="key"] .accordion__item::details-content` restyles the whole
     document on the first keyboard input (1 138 elements against 509 without it). Unchanged diagnosis (§11.3).
  2. Without it, the flip of `html[data-input]` still restyles 509 elements on the home against 294 on the base. The
     invalidation set Chromium builds for that attribute (tracked: `imp2/perf/invalid_lane_fr.json`) holds the tag
     names `a, circle, img, input, line, path, polyline, select, textarea`, 58 classes and the attributes `data-rise,
     data-sec-state, data-spotlight, data-verb, type`. The tag names come from the vocabulary's
     `[data-sec-state="wait"] :is([data-verb~="stroke"], [data-verb~="stroke"] :is(path, circle, line, polyline))`
     and from `main.css`; with them every SVG shape, link and image of the page restyles. Of the 58 classes, lane H's
     sheet adds three (`passaggio__freccia`, `passaggio__arco`, `foto__img`).
- **Selector cost** (Chromium's selector stats, same keydown, rule dropped, instrumented times): lane 63.4 ms against
  base 42.4. `main.css` 46.9 against 35.2 (it scales with the elements restyled), the library partials the home imports
  8.3 against 0.2, lane H's `pages.css` + `_casa.css` 4.2 against 1.2, `hero.css` 3.3 against 4.6. The library's two
  dearest selectors are `html[data-input="key"] :is(.sez-tile .icon, .sez-disc, .sg-g--key)` (1.8 ms) and
  `:is(.sez, .ingresso, [data-sigillo-scope]):has(:is(.btn--primary, [data-azione]):is(:hover, :focus-visible))`
  (1.1 ms). Both are tried against every element: their subject starts with `:is()`, so Chromium cannot file them
  under a class.
- **What lane H did.** The same fault in the home's own sheet: every rule whose subject started with an `:is()` or a
  bare `:nth-child` is now written so that Chromium files it under a class (`.page-home .home-pathways,
  .page-home .home-ecosystem`; `.passaggio__titolo:lang(ar), .passaggio__cta:lang(ar)`; `.pilota__lead,
  .pilota__nota, .pilota__azione`; the statement and process heads; `.page-home .sez h2, .page-home .sez h3`; the
  door arrow's keyboard rule; the banner's RTL lines; the bond's fields; the index's ranks; the colophon's name; the RTL
  rows), with the same targets and, but for the bond's fields (one class more, no rule of the page competes), the same
  specificity. `.colofone > *` and `.integrita__tavola > * + *` stay: their parent's class rejects them early. The
  ecosystem's keyboard rule names `.foto__img`, not the `img` tag. In the trace this is a few milliseconds (176.9
  against 183.5 served), inside the noise. Lane H's share of the selector time is 4.2 of 63.4 ms.
- **Not done, and why.** `content-visibility` on the bands (round 1: the Tab's focus navigation then forced the skipped
  bands' style and layout, 506 ms); removing elements (the 204 extra elements are the V2 compositions themselves);
  any edit to `motion.css` or the library (preserved family; lane S's files).
- **Mouse and touch** are not affected by either cause: the reviewer measured the first click at 40–52 ms and the first
  tap at 108–128 ms; this round changes neither path.

### 12.4 Tests

Updated under the V5.20 strict rule, all four in lane H's own module `apps/pages/tests/test_home_v522_h.py` (written by
this lane in V5.22), each for an approved decision, each holding the same or a stronger invariant; nothing loosened, no
timeout raised, no skip:
- `test_the_pathways_stage_links_a_published_sheet_and_only_that`: the stage's way to a published sheet is now the
  catalogue's «Consulter la page du parcours», where it was «Voir le parcours» (SECTION_SYSTEM_V2 §1 rule 6, the
  language of parts; QA_ROUND2's institutional finding). Same invariant: one link per published sheet, none otherwise.
- `test_the_stage_says_its_way_in_the_page_s_language_and_its_texts_in_their_own`: on the Arabic page the link must be
  the Arabic msgstr with no `lang` attribute. Round 1 accepted the tagged French fallback, so this is stronger.
- `test_the_ecosystem_photograph_rises_in_its_arch_and_its_doorway_is_drawn`: the two paths' `pathLength` is now 0.1
  (sill) and 0.125 (arch), where it was 1 (§3.1 S7 «the arch outline draws», §5.1 LINE DRAW; QA_ROUND2 m1). The browser
  half (below) checks what the attribute is for: one dash covers each line on screen.
- `test_the_trust_answers_are_one_tablet_set_in_the_wall_with_its_plinth`: the bond's selector names its fields
  (`.integrita__tavola > .integrita__lastra:is(…)`), for INP (§5.3; QA_ROUND2 M2). Same invariant: spans 5 and 7, the
  joints never line up.

New in `apps/pages/tests/test_home_browser_v522_h.py`:
- `test_round_2_the_arabic_page_hangs_each_french_run_from_one_edge` (1440, 1280, 1024, 768, 390, 360): the reserved
  row's title and sentence share their start edge within 1 px; the colophon's name, in its two parts, and the French
  answer too; each route caption stands at 12.5 em at most and, across the route, on its station's edge.
- `test_round_2_a_phone_s_disclosure_row_reads_tile_title_chevron_and_inks_in_order` (fr, ar at 390): the button keeps
  the page's direction, the chevron's end margin is on the row's end, the title's ink lies between the tile and the
  chevron; the eight ranks are `"", 1 … 5, 5, 5` and the titles' delays 0 s … 0.3 s once the section plays.
- `test_round_2_the_arch_s_outline_and_sill_draw_as_one_stroke_each` (eight widths, 360–1440, and 1023): each line's
  dash (user length / pathLength) is longer than the line on screen.

Runs on the final tree, one pytest at a time on `test_ile_v5_l5`:

| Suite | Result |
|---|---|
| `test_home_v522_h.py` + `test_home.py` + `test_templates_static.py` | 236 passed |
| `test_prescribed_fragments.py`, `tests/compliance/test_locked_content.py`, `tests/frontend/test_french_typography_w2_d.py`, `test_services.py`, `test_review2.py`, `tests/frontend/test_frontispiece_v515_c.py` (the per-sheet and per-page ceilings), `test_design_docs.py`, `test_css_bundle_is_current.py`, `test_static_pipeline.py` | 272 passed |
| `apps/pages/tests` (not browser) + `tests/frontend/test_journey_w3_d.py` + `tests/frontend/test_chapter_marks.py` | 515 passed, 2 failed: exactly lane S's two declared guards (§8, the merge conditions) |
| `tests/i18n/test_catalogues.py` + `tests/i18n/test_page_integrity.py` | 73 passed, 4 failed: the declared catalogue reds, now naming one msgid (the pilot's lead) |
| `test_home_browser_v522_h.py` + `apps/pages/tests/test_browser.py` (headed lock B) | 50 passed |
| ruff check and format (`apps/pages`) | clean |

Headed checks, chromium-1234, lock slots A and B (evidence `imp2/`):
- **Sweep:** fr and ar × 1440, 1280, 1024, 768, 430, 390, 375, 360; it and en × 1440, 1024, 768, 390, 360. Overflow 0,
  no element of `<main>` wider than the page, 0 console errors, no focus stop hidden or without its ring in 26 runs.
  Page heights at 1440: fr 6 112, ar 6 105. The route captions keep 2 lines at 1440 except the fourth (3) on the Arabic
  page; the pilot title two lines at every width.
- **axe-core 4.13** (WCAG 2.0, 2.1 and 2.2, A and AA, after a play-through): **0 violations in 8 runs** (fr and ar,
  1440 and 390, with and without reduced motion). Incomplete as before: contrast over photographs and gradients, and
  the preserved nav toggle's `aria-controls`.
- **Reduced motion:** no `data-sec-state` written (fr, ar, 1440, 390); only Lume's still-out runs.
- **No-JS:** 8 of 8 panels shown, the doors on phones, the four trust fields, no locked text hidden.
- **Keyboard:** 31–34 stops; the index's arrows, Home and End with the page fixed. The four trust questions' rings are
  drawn on their fields (by design); the header links and the skip link are preserved chrome.
- **The arch, sought frame by frame** (`imp2/arch_seek/`, fr 1440, 1024, 390 and ar 1440: every animation of the frame
  paused and sought to 0 … 1 500 ms): the sill draws from 0 to 900 ms and the outline from 600 to 1 500 ms, one line from
  the foot on the reading edge over the crown, never segments.

### 12.5 Requests to other lanes (new this round)

- **Owner of `static/css/v5/motion.css`, through the steward** (preserved family; unchanged request, measured again
  in §12.3): `[data-input="key"] .accordion__item::details-content` makes the first keyboard input of every page
  restyle the whole document (1 138 elements on the home, 509 without it; base 853 / 294). Suggested: a custom property
  set on `.accordion__item` under `html[data-input="key"]`, read by `::details-content`. This closes most of M2.
- **Lane S** (the rest of M2, and m5):
  1. `_reveal.css`: `[data-sec-state="wait"] :is([data-verb~="stroke"], [data-verb~="stroke"] :is(path, circle, line,
     polyline))` under `:root:not([data-input="key"])`. Its tag names make every SVG shape of the page restyle when
     `html[data-input]` flips. Put the verb (or a class) on the shapes themselves, as the home's drawings do
     (`<path data-verb="stroke">`), and drop the tag branch.
  2. `html[data-input="key"] :is(.sez-tile .icon, .sez-disc, .sg-g--key)`: the dearest library selector on the home's
     first input (1.8 ms instrumented). Its `.icon` feature restyles every icon of the page, and its `:is()` subject is
     tried against every element. Suggested: `html[data-input="key"] .sez-tile > .icon` and the two others as their own
     class-led selectors.
  3. `_sigillo.css` `:is(.sez, .ingresso, [data-sigillo-scope]):has(…)` (1.1 ms): three class-led selectors instead of
     one `:is()` subject.
  4. `_sec-indice.css` `.indice__lista > :nth-child(n)`: `.indice__riga:nth-child(n)`, so the rows' ranks are filed under
     a class (the home does the same for its panels).
  5. m5: `components/sezioni/protezione.html`: `.protezione__titolo` stays right-to-left around its `<span lang="fr">`,
     so on the Arabic page «ATTENTION AUX FRAUDES» stands at the right while the French body is flush-left in its box.
     Give the title an LTR box when its run is French (one rule in the library: every page that shows the plate gains
     it at once).
  6. Unchanged from §8 and §11.5: the chapter-marks and journey guards, the 48 rem tabs hook, the `ol[lang]` direction,
     the `sez-arch` `from` keyframe, the campata settle cancelled by the shell, `.testa__label:lang(ar)`, a phone index
     entrance in the library.
- **Steward:** the catalogue entries now carry one msgid, the pilot's lead
  (`evidence/v522/h/catalogue_entries_{it,en,ar}.po`, re-verified byte-identical to `content.py`). «Voir le parcours»
  is withdrawn: no entry is needed for it.
  `tests/i18n/test_catalogues.py` now names only the lead (4 reds, the declared merge condition). Unchanged:
  `seed_all --only pages.home_sections` on the shared databases; the OWNERSHIP rows of §8 (no new file this round);
  the preview label.
- **Lane M:** unchanged (the ecosystem frame's softness, m9 of round 1).

### 12.6 Deviations and not done

- **M2 is not closed.** It needs the `motion.css` change and the library's requests above. Lane H's own share was cut
  where it could be (selectors), and it is within the noise of a busy machine. §9.9 item 6 stays open until the steward
  routes the change; then lane H re-measures on 8782, quiet, n ≥ 9, fr and ar, desk and phone.
- **m6** (the moment shorter than the integrity band) is the Director's call and is unchanged.
- **The home's CSS total is exactly at its ceiling** (61 440 of 61 440 B).
- The arch outline relies on how Chromium lays a non-scaling stroke's dash (in screen pixels, scaled by the user length
  over `pathLength`). An engine that lays it in user units would draw each line in about a tenth of its course: fast,
  but still one line, never segments. At rest, from the keyboard and under reduced motion, nothing is dashed.
  **Corrected in the final fix round (QA_ROUND3 m4; §13.1):** «screen pixels» are DEVICE pixels — the dash shrank
  with the screen's pixel ratio and drew as pieces on any screen above 1×. The lines now carry no dash (§13.1).
- On a phone, a French pathway title that wraps to two lines on the Arabic page fills its box between the chevron and
  the tile and starts at the box's own (left) edge. That is §1 rule 6's quotation box, and the tab rows do the same.
  **Corrected in the final fix round (QA_ROUND3 M1, m4; §13.1):** this was the defect, not §1 rule 6. Rule 6 asks for
  one box per run hung from the reading edge, never a list whose items alternate sides; at 1024–1280 and on every
  phone the list zig-zagged. The titles now stand on one edge (§13.1).
- **Deviation from §3.1 S3, recorded in the final fix round (QA_ROUND3 m4):** the stage's way to a published sheet is
  «Consulter la page du parcours», where §3.1 S3 names «Voir le parcours». It is the product's existing catalogued
  string, with professional it/en/ar, no new msgid and no fallback, and it leads to the same destination. Recorded for the
  Director and the steward (§12.1, «Institutional»).
- The route captions on phones stand at 12.5 em too: one caption of four takes a third line (+32 px).
- The pilot's lead stays French on it/en/ar until the merge carries its entry (merge condition).

### 12.7 Self-scores (§10; fr and ar, 1440 and 390; the reviewer verifies)

| Dimension | Round 2 (reviewer) fr / ar | Round 2 (self) fr | Round 2 (self) ar | Why |
|---|---|---|---|---|
| Composition | 4.5 / 4.5 | 4.5 | 4.5 | unchanged compositions; the Arabic French runs now stand as quotation boxes |
| Motion | 4.0 / 4.0 | 4.5 | 4.5 | m1 (the arch draws as one line) and m2 (the phone rows ink in order), the two reasons it was held at 4 |
| Imagery | 4.0 / 4.0 | 4.0 | 4.0 | unchanged (the ecosystem frame's softness is lane M's) |
| Interaction | 4.0 / 4.0 | 4.0 | 4.0 | held by M2: the first keyboard input waits for the `motion.css` change and the library's |
| Institutional | 4.5 / 4.0 | 4.5 | 4.0 (it/en 4.0) | the stage now speaks the page's language; the pilot's lead waits for the merge |
| Coherence | 4.5 / 4.0 | 4.5 | 4.5 | M1 a, M1 b, m3, m4: every French run on the Arabic page hangs from one edge — **not confirmed by QA_ROUND3 (M1): the index's titles stood on two edges at 1024–1280 and on phones; closed in §13** |

## 13. Final fix round (label `v522-h-fix`, 2 November 2026)

This answers `evidence/v522/h/QA_ROUND3.md` (head `c17146f`), which did NOT PASS with 2 major and 7 minor findings.

**Where the work ran.**
- Same branch and worktree.
- design-v5 has moved to `269cf39` (lanes S, M and P1 merged). It is not merged into the lane: the next step merges
  design-v5 with `v522/s2` and re-reviews.
- Lane server 8785 on `ile_v5_l5`; tests on `test_ile_v5_l5`, one pytest at a time.
- Headed `chromium-1234` under lock slots A and B, at most 25 minutes a session, released between sessions.

**Where things are.**
- Scripts and raw output: `C:/tmp/ile_v5_council/.work/v522-h-fix/`.
- Evidence: `evidence/v522/h/fix/`. The key crops are `fix_*.png`.

### 13.1 What changed, finding by finding

| Finding | What the owner now sees | Where |
|---|---|---|
| **M1**: the Arabic index's French titles on two edges | The eight titles stand on one edge, the reading edge's, at every width. Each title is the row's remainder (`flex: 1`, so a long title never squeezes its glyph either), and its lines are set against its glyph or tile at the end of its own left-to-right box. This is recorded as the **RTL label exception**, like §2 F's French labels centred under their tiles: a label beside its tile, never a paragraph. Measured at rest, ar, at 1440, 1280, 1024, 768, 430, 390, 375 and 360: edge spread **0.00 px** at every width (wrapped titles 0, 2, 3, 0, 2, 3, 3, 4); each title 12.0 px from its glyph; glyphs 20 px (tabs) or 40 px (tiles). Before: wrapped titles started 220–290 px from their glyph (tabs) or 71 px from their tile (phones). French is unchanged: titles hug their glyphs, and the 1.6–4.2 px start-edge drift at 1024–1280 is m3, the library's glyph. `fix_M1_ar_{1280,1024,390,360}_index_one_edge.png`, `m1_m2_measure.json` | `pages.css` §6 |
| **m1**: the arch's outline — a detached piece of its far leg | **The cause is the screen's pixel ratio.** A stretched non-scaling stroke's dash is laid in **device** pixels. Round 2's dash (user length ÷ pathLength, 2 082 px) is therefore 1 665 CSS px on the reviewer's 125 % display, 1 041 at 2× and 694 at 3×. Measured with the full Chromium build at a forced device scale factor (`probe_*.json`, `red_*.json`): at 2×, the outline's far half and a piece of the sill were painted before their lines began (1023: outline 1 040–1 978 px painted at 300 ms); at 3×, both drew as dashes. The emulated factor changes nothing, and the headless shell lays the dash at 1× whatever the factor — which is why every test passed. **No pathLength holds for every screen.** The suggested 0.06 gives a dash of 4 333 px: still pieces at 3× for any line over 1 444 px (a 3× phone in landscape draws about 1 700), and a pace that changes with the screen. **So the visible lines now carry no dash at all.** Each is drawn through its own **mask**: the same path, 12 user units wide, in the drawing's own user space, with mask-type alpha and the text's ink (no literal colour). The mask carries the verb «stroke» with `pathLength` 0.99, one dash a hundredth longer than the line, so no sliver of a second dash shows at the far end. A user-space dash scales with the drawing, never with the screen. Measured identical at 1×, 2× and 3× (a forced factor in the full Chromium build: fr 360, 768, 1023, 1440, 1600 and 1920, ar 390 and 1440; and in the tests' shell at 1× and 2×, fr 390): the sill grows from its end over 0–900 ms; the outline grows from its foot on the reading edge, over the crown, to the other foot over 600–1 500 ms (at 1440: 352 px at 900 ms, 1 226 at 1 200, whole at 1 500), one run each, never segments. Its pace is the verb's own, and its delay stays in `pages.css` (600 ms). `fix_m1_before_fr_1023_headed125_300ms_far_leg_piece.png` (the round-2 markup on the reviewer's display), `fix_m1_{fr_1023,ar_1440}_dsf2_arch_{300,1100,1650}ms.png` | `_ecosystem_frame.html`, `pages.css` §9 (comment, the drawing's delay reset) |
| The phone doors' lunettes (found with m1's cause) | The same defect on every real phone. On a 2× phone the lunette's far half was painted before its line began; on a 3× phone it drew as dashes (measured at 390, fr). The same fix applies: each door's arch is drawn through its own mask, whose id is the door's rank. It is now one run from its foot: at 390 fr at 1×, 2× and 3×, and at 360 and 430 ar at 3×. `fix_doors_fr_390_dsf2_lunette_{0,450,1300}ms.png` | `components/entrances.html` |
| **m2**: the colophon's connector 6 px above its rule | The 1 px connector runs on the folio's 2 px rule, centre line on centre line: `inset-block-start: calc(0.5rem - 0.5px)`, which is half the folio's 1 rem line (`--t-folio-lh`, so it follows the reader's font size) less half its own pixel. Measured fr and ar at 1440, 1280 and 1024: centre offset **0.00 px**, and the connector ends exactly where the rule begins. Below 64 rem it is not drawn (unchanged). `fix_m2_{fr,ar}_1440_connector_on_rule.png` | `pages.css` §9 |
| **m3**: the index glyph squeezed in wrapped rows | Requested from lane S2, whose brief carries `.indice__glifo { flex-shrink: 0 }`. **No page-level override was added**: the orchestrator's instruction is to add it only if S2 does not provide it. On the Arabic page M1's `flex: 1` already keeps the glyphs at 20 px. On the French page the squeeze (15.8–18.4 px at 1024–1280) waits for S2's rule. | — (lane S2) |
| **m4**: NOTES accuracy | §12.1's m1 row, §12.6's arch and phone-title bullets and §12.7's coherence reason are corrected in place, each marked «Corrected in the final fix round». The stage's label is listed in §12.6 as a deviation from §3.1 S3. | this file |
| **M2**: INP of the first keyboard input | **The lane-H side is prepared; it waits for lane S2.** (1) Every shape of the home that carries the verb «stroke» carries it itself: 6 of them, all inside masks now, and no `svg`/`g` holds the verb for its children. S2 can therefore drop the vocabulary's `[data-verb~="stroke"] :is(path, circle, line, polyline)` tag branch (request 1) without the home losing a line. (2) The index rows are `li.indice__riga`, the selector of request 4. (3) Lane H's own `[data-input]` rules are class-led (round 2), and the forced-colours rule of `pages.css` is now a class-led list rather than an `:is()` subject. (4) The re-measure rig is ready: `.work/v522-h-fix/inp_rerun.py`, the reviewer's round-3 rig parametrised by the two twins' URLs. Run it after S2 merges, on a quiet machine, n ≥ 9, fr and ar, desk and phone: it measures the first Tab and the first pointer input after keyboard use. | `pages.css` (forced colours), templates (the verbs on their shapes) |
| m5, m6, m7 | Carried. **m5** (the «la protezione» title on the Arabic page) and the photo credit's colon are in lane S2's brief. **m6** (rhythm) is the Director's call. **m7** covers the merge conditions — the pilot lead's catalogue entries, S's two guards, `seed_all --only pages.home_sections` — and lane M's frame. | — |

### 13.2 Budgets (gzip -9, dist, after `npm run build`)

| Sheet | Round 2 | Final round | Ceiling |
|---|---|---|---|
| `pages/css/pages.css` | 11 281 | **11 277** | 12 288 |
| `pages/css/hero.css` | 10 899 | 10 899 (untouched) | 11 264 |
| `main.css` | 32 718 | 32 718 (untouched) | 32 718 |
| `core/reveal.css` · `core/portico.css` | 3 549 · 2 993 | unchanged | — |
| **Home, every sheet linked** | 61 440 | **61 436** (4 B headroom) | ≤ 61 440 |

**What the fixes cost.** M1 costs 3 B. m2's connector rule costs about 12 B. The masks are markup only, so they cost no CSS.

**Where the bytes came from.** Equivalent rewrites of lane H's own rules recovered about 20 B:
- the news titles' two link rules folded;
- the reserved row's Arabic title joined the doors' Arabic no-tracking rule (its 0,2,0 specificity holds it over its own
  0,1,0 tracking);
- the integrity band's padding joined the paper bands' rule;
- the banner's three lines placed by `grid-area` (the same lines and spans, checked in the CSSOM);
- the register's area names on single spaces;
- the drawing's delay reset on the drawing itself;
- the connector rule's short selector (the home's one connector);
- the forced-colours `:is()` list written as a plain list.

**The proof that nothing else moved.** A computed-style diff of every element of `<main>` (33 properties and its box)
under round 2's `pages.css` and this round's, at fr and ar × 1440, 1024 and 390 (`style_diff.json`):
- in French only the connector changed;
- in Arabic only the index's titles and the connector changed.

**JS and the build.** JS is unchanged. `npm run build` is reproducible: only `dist/pages/css/pages.css` changed.

**For the steward.** `core/reveal.css` counts in the home's total. Lane S2's `_reveal.css` changes will move it, so the
H merge re-measures the total.

### 13.3 Tests

**Updated under the V5.20 strict rule.** Both are in lane H's own modules, written by this lane in V5.22. Each holds a
stronger invariant, cites its reason, loosens nothing, raises no timeout and adds no skip.
- **`test_the_ecosystem_photograph_rises_in_its_arch_and_its_doorway_is_drawn`** (`test_home_v522_h.py`).
  - *Before:* the two paths' `pathLength` was 0.1 and 0.125, a dash on the visible line.
  - *Now:* each visible line carries no dash and no verb. It is masked by its own mask: user space, alpha, the line's
    own path, the verb with pathLength 0.9–1, wide enough to cover the line, in the text's ink. The outline's
    per-width CSS path shapes both the line and its mask.
  - *Why:* QA_ROUND3 m1; §3.1 S7, §5.1 LINE DRAW.
- **`test_round_2_the_arch_s_outline_and_sill_draw_as_one_stroke_each`** (`test_home_browser_v522_h.py`) is replaced by
  `test_final_the_doorway_is_painted_as_one_line_from_its_foot`. The reviewer asked for exactly this: «replace the
  model assertion with a painted one» (QA_ROUND3 m1, §6).
  - The old test asserted a model of the dash that no 2× screen paints.
  - The new one inks the visible lines through the CSSOM (a measuring aid only), seeks every animation of the section
    and walks each line's own 241 screen points on the screenshot. It runs at 1× and 2×, at 1023, 1920 and 390 fr and
    1440 ar.
  - At 300 ms the outline is unpainted, far leg included, and the sill grows from its end.
  - At 1 000 ms the outline is one run from its foot and its far leg is still bare.
  - At 1 650 ms both lines are whole.

**New tests.**
- `test_home_v522_h.py::test_final_round_no_line_of_the_home_lays_its_dash_on_a_non_scaling_stroke` (fr, ar) guards
  the defect's class. No shape of the home carries both the verb «stroke» and a non-scaling stroke. The four door
  lunettes are drawn through their own masks with unique ids (`passaggio-arco-1…4`), and the home has six masks.
- `test_home_v522_h.py::test_final_round_the_arabic_titles_stand_against_their_glyphs_and_the_connector_on_its_rule`
  checks M1's and m2's rules in the sheet, and that `--t-folio-lh` is 1 rem.
- `test_home_browser_v522_h.py::test_final_a_phone_door_s_lunette_is_painted_as_one_line_from_its_foot` runs at 1× and
  2×, at 390 fr and 360 ar.
- `test_home_browser_v522_h.py::test_final_the_arabic_index_s_titles_stand_on_one_edge_and_the_connector_on_its_rule`
  runs at the eight widths. In Arabic: one edge within 1 px, each title 12 ± 1 px from its glyph, the glyphs one size,
  and a wrapped title present wherever one wraps (the case M1 is about). In French and Arabic: the connector's centre
  within 0.5 px of the rule's from 64 rem, its end where the rule begins, and no connector below 64 rem.

**What the painted test can and cannot show.** These tests run in Playwright's headless shell, which lays a non-scaling
dash at 1× whatever the forced factor; this was measured on the real page. The device-pixel defect therefore cannot be
reproduced there. Its class is guarded structurally (the first new test), and its fix was measured in headed and full
Chromium at a forced 1×, 2× and 3× (§13.1).

**The painted tests bite.** Against round 2's markup, swapped in and then restored byte for byte, all four cases fail:
- the doorway's, because round 2's outline was already whole at 1 000 ms at 390, drawn in under half the verb's course;
- the lunette's, because round 2 has no masked line to draw.

**Runs on the final tree** (one pytest at a time on `test_ile_v5_l5`):

| Suite | Result |
|---|---|
| `test_home_v522_h.py`, `test_home.py`, `test_templates_static.py`, `test_prescribed_fragments.py`, `tests/compliance/test_locked_content.py`, `tests/frontend/test_french_typography_w2_d.py`, `test_services.py`, `test_review2.py`, `tests/frontend/test_frontispiece_v515_c.py` (the per-sheet and per-page ceilings), `test_design_docs.py`, `test_css_bundle_is_current.py`, `test_static_pipeline.py` | **510 passed** (round 3: 508, plus the 2 new static tests) |
| `tests/frontend/test_chapter_marks.py`, `test_journey_w3_d.py`, `tests/i18n/test_catalogues.py`, `tests/i18n/test_page_integrity.py` | 114 passed and 6 failed: exactly the declared merge conditions, unchanged (S's two guards; the catalogue's four, each naming one missing msgid, the pilot's lead) |
| `test_home_browser_v522_h.py` (Playwright's headless shell, lock B) | **33 passed** |
| `apps/pages/tests/test_browser.py` (lock B) | **28 passed** |
| The painted tests against round 2's markup (swapped in, then restored byte for byte) | 4 of 4 fail, as they should |

**Lint and line endings.** ruff check and format on the two test modules: clean. Every changed file is LF.

### 13.4 Headed checks (chromium-1234; `evidence/v522/h/fix/`)

- **Sweep:** fr and ar at the eight widths, it and en at 1440, 1024, 768, 390 and 360. Overflow 0, no element of
  `<main>` wider than the page, 0 console errors and 0 focus stops hidden or without a ring in 26 runs
  (`sweep_{fr,ar,iten}/sweep.json`). Page heights are as in round 2 (fr 6 112 and ar 6 105 at 1440).
- **axe-core 4.13** (WCAG 2.0, 2.1 and 2.2, A and AA, after a play-through): **0 violations in 8 runs** (fr and ar, 1440
  and 390, with and without reduced motion). The incompletes are as before: contrast over photographs and gradients,
  and the preserved nav toggle's `aria-controls`.
- **Reduced motion:** no `data-sec-state` is written; only Lume's still-out runs.
- **No-JS:** 8 of 8 panels shown, the doors on phones, the four plates, no locked text hidden.
- **Keyboard:** 31 stops at 1440 and 34 at 390, unchanged. The index's arrows, Home and End work with the page fixed.
  The skip link and the header's links are preserved chrome. The trust questions' rings are drawn on their fields, by
  design.
- **The key crops:** `fix_M1_*`, `fix_m1_*`, `fix_doors_*` and `fix_m2_*`.

### 13.5 Requests to other lanes (new or updated)

- **Lane S2** (already in its brief):
  - m3: `.indice__glifo { flex-shrink: 0 }`;
  - m5: the «la protezione» title in a left-to-right box when its run is French;
  - the photo credit's space before the colon only in French;
  - INP requests 1–4 and the one `motion.css` rule (§12.5).
- **Lane S2 / S-close (new):** a stretched non-scaling stroke that carries the verb «stroke» draws as pieces on every
  screen above 1×, because its dash is laid in device pixels.
  - The library's fixture (`tests/frontend/sezioni_fixtures.py`, the passaggio arch) still has the round-2 form,
    `pathLength="1"` on a non-scaling path, and so does the header comment of `_sec-passaggio.css`.
  - The home's two drawings show the form that holds: the line drawn through a user-space mask that carries the verb.
  - On design-v5 at `269cf39`, no other template has the verb on a non-scaling shape (checked). Lane P2's pages should
    be checked at their merge.
- **Steward:**
  - The home's total has 4 B of headroom, and `core/reveal.css` (S2) counts in it: re-measure at the H merge.
  - No new msgid this round; the catalogue entries still carry only the pilot's lead.
  - No new file, so the OWNERSHIP rows are unchanged.
  - The stage's label is a deviation from §3.1 S3 (§12.6), recorded for the Director.

### 13.6 Deviations and not done

- **m1 is not the prescribed «pathLength ≈ 0.06 with its own pace in `pages.css`».** That margin fails on a 3× screen
  for any line over 1 444 px, and its pace would change with every screen.
  - The user-space mask holds on every screen, at the verb's own pace.
  - The outline's own delay stays in `pages.css` (600 ms).
  - No keyframe and no new token: `pages.css` animates nothing, and `test_the_home_moves_nothing_of_its_own…`
    guards that.
- **M2 is not closed.** It waits for lane S2's selectors and `motion.css` rule; then comes the re-measure with
  `inp_rerun.py`. §9.9 item 6 stays open until then.
- **m3 is left to lane S2,** as instructed. The French glyph squeeze at 1024–1280 stays until S2 merges; the Arabic list
  does not depend on it.
- **design-v5 is not merged into the lane.** That is the next step, with `v522/s2`.
- Carried: m6 (the Director's), m7 (the merge conditions) and lane M's frame.

### 13.7 Self-scores (§10; fr and ar, 1440 and 390; the reviewer verifies)

| Dimension | Round 3 (reviewer) fr / ar 1440 / ar 390 | Final (self) fr | Final (self) ar | Why |
|---|---|---|---|---|
| Composition | 4.5 / 4.5 / 4.5 | 4.5 | 4.5 | unchanged compositions |
| Motion | 4.5 / 4.5 / 4.5 (4.0 at 880–1023 and ≥ 1600) | 4.5 | 4.5 | m1 closed at every width and on every screen (1×–3×); the doors' lunettes draw as one line on real phones |
| Imagery | 4.0 / 4.0 / 4.0 | 4.0 | 4.0 | unchanged (the ecosystem frame's softness is lane M's) |
| Interaction | 4.0 / 4.0 / 4.0 | 4.0 | 4.0 | held by M2 until lane S2 merges |
| Institutional | 4.5 / 4.0 / 4.0 | 4.5 | 4.0 (it/en 4.0) | the pilot's lead stays French on it/en/ar until the merge carries its entry |
| Coherence | 4.5 / 4.5 / **4.0** | 4.5 | **4.5** | M1 closed: the Arabic index's titles on one edge at every width; m2: the connector on its rule |

## 14. Improve after the final review (label `v522-h-final-improve`, 2–3 November 2026)

This answers `evidence/v522/finish/v522-h-final-qa1.md` (head `4afed99` merged for review with design-v5 `28fa9fa`),
which did NOT PASS with 2 major (F-M1, F-M2) and 6 minor findings (F-m1 … F-m6).

**Where the work ran.**
- Same branch and worktree. design-v5 `28fa9fa` (`v522/s2`, DL54-184) is now merged into the lane (§14.1).
- Lane server 8785 on `ile_v5_l5` (reference date 2026-10-03, G3 open); a second dev server of the same tree on 8776
  (2026-09-30, G3 closed) and a dev server of the base (`git archive 28fa9fa`) on 8775, both on `ile_v5_l5`, for paired
  measures; all three stopped at the end. Tests on `test_ile_v5_l5` (non-browser) and `test_ile_v5_l5b` (browser), one
  pytest at a time per database.
- Headed `chromium-1234` under one lock slot a session (A or B, ≤ 25 minutes, released between sessions; log
  `.work/v522-h-final-improve/logs/locks.log`). The P2 lane's final round ran on the machine at the same time.

**Where things are.**
- Scripts and raw output: `C:/tmp/ile_v5_council/.work/v522-h-final-improve/` (`tools/`, `logs/`).
- Evidence: `evidence/v522/h/final-improve/` — `pilot_before/` (ar, fr) and `pilot_after2/` (ar, fr, it, en: the
  statement at the 8 widths, crops and `pilot.json`), `plates/` (gate closed), `sweep.txt`, `axe.json`, the key crops
  `fi_*.png` at its root, and `requests/F-M2_first_key_attribution.md` (for the steward).

### 14.1 The merge

- `0191e444` — `git merge --no-ff design-v5` (`28fa9fa`): **no conflict**; the lane's diff since its base `22b0ddd`
  (28 files) and design-v5's (122 files) have no file in common.
- `7a8eecd9` — `npm run build` with the installed packages: only `static/css/dist/pages/css/pages.css` changes
  (11 277 → 11 299 B gzip -9: it bundles lane S2's library rules); a second build changes nothing.
- `aa640b08` — **the catalogue entry carried on the branch** (the final review's F-m5, simulated there as the steward
  would run it): `i18n_audit.py --sync` (+1 −1: the pilot's lead in, the old lead out), the three msgstr of
  `evidence/v522/h/catalogue_entries_{it,en,ar}.po` (msgids byte-identical to `content.py`), `--compile`: OK, 100 %,
  3 697 msgids in it/en/ar/fr, LF. The Arabic as reviewed in the final review. The steward's own pass at the merge is
  then +0 −0 for lane H.

### 14.2 What changed, finding by finding

| Finding | What the owner now sees | Where |
|---|---|---|
| **F-M1** — the Arabic pilot statement on two alignments | The page's moment says one statement on one alignment in every language. On the Arabic page the locked French title now follows its seam as its Arabic lead and link do: **centred on the gold thread's axis from 64 rem, its lines ending on the reading edge below**. Measured headed (`pilot_after2/pilot.json`, reduced motion): ar 1440 / 1280 / 1024, every title line, lead line and the link within **0.0 px** of the axis (before: 50.0 / 43.7 / 33.6 px off); ar 768 → 360, the right edges of title, lead and link within **0.0 px** (before: spreads of 240.5 / 101.0 / 67.8 / 64.9 / 61.8 px). fr, it and en unchanged (0.0 px, centred from 64 rem, one left edge below). Below 64 rem the title's two display lines end on the reading edge (`text-align: end` in its own LTR box: the RTL label exception of §2 F, as the index's titles); a fit-content box was not taken — when the title wraps the box fills the column and its lines would start at the far edge again. `pilot_after2/ar_{1440,768,390}_statement.png` | `pages.css` §7 (two rules, `[dir="rtl"] .page-home .pilota__titolo[lang]`, 0,4,0 over §1's 0,3,1) |
| **F-m2** — the lead's last line one word | `text-wrap: pretty` on the lead. At the 8 widths in fr, it, en and ar the lead's last line holds at least two words (ar 768: «ومشروع واحد.», before «واحد.» alone). No line count changed (no box changed size: §14.4). | `pages.css` §7 |
| **F-m1** — gate closed, the two interim plates stretched to one height | The two plates stand each at its own height on the stone. Measured (`plates/plates.json`): fr 1440 and 1280 164 / 272 px, 1024 192 / 356 px; ar 164 / 244, 192 / 272 px — 0 px of empty plate under the last statement in each. `plates/closed_fr_1440_trust_plates.png` | `pages.css` §8 (`align-items: start` on the two-plate layering — on the home only the closed gate uses it) |
| **F-M2** — the first keyboard input | **Lane H's share done; the decision is the steward's.** Lane H's two `[data-input]` rules are folded into one class-led rule (`transition-duration: 0s` on the doors' arrows and arches and the promoter's photograph; `transition: none` was tried and refused by `test_templates_static.py`'s token guard). Measured (§14.3): the home's own rules restyle **no element** at the first key, before and after the fold; the +247 elements over the base are the library's (≈ 150 the motion vocabulary's `:root:not([data-input="key"])` guards, 39 the keyboard tier's inherited `--sez-t`) and the Tab's own restyle. Request for the ruling: `requests/F-M2_first_key_attribution.md` | `pages.css` §4 |
| **F-m5** — merge conditions | The catalogue entry carried (§14.1). Lane S's two guards updated under V5.20 (§14.5). For the steward: the OWNERSHIP rows, the seed, the label (§14.7). | locale, two guard tests |
| F-m3, F-m4, F-m6 | Not lane H's files (§14.8). | — |

### 14.3 F-M2: what the first key restyles, and whose it is

Deterministic counts, not times: the largest `UpdateLayoutTree` of a Chromium trace around the first Tab, the page at
rest at its top, 1440 × 900, `/fr/`, two dev servers on one database (the lane at 8785, the base `28fa9fa` at 8775),
headed chromium-1234, no throttling. Before the Tab an experiment deletes CSSOM rules by a predicate on their selector
(`tools/flip_lab.py`; raw `logs/flip_lab_fr*.json`).

| Rules deleted before the Tab | Lane (1 396 elements) | Base (1 180) |
|---|---|---|
| none | **525** | **278** |
| lane H's own `[data-input]` rules | **525** (0) | 278 |
| the library's keyboard tier (`--sez-t` on `.sez-tile`, `.sez-disc`, `.sg-g--key`) | 486 (−39) | 278 |
| … replaced by direct rules on the animated parts | 486 (−39) | 278 |
| the vocabulary's 54 guards `:root:not(.rm):not([data-input="key"]) …` | **375 (−150)** | 278 |
| … the `[data-verb]` / «linea» / «sigillo» / «strato» / «indice» guards alone | −67 / −32 / −21 / −17 / −15 | — |
| main.css's 14 modality rules (preserved, §9.8) | 383 (−142) | 131 (−147) |
| every rule naming `data-input` | 116 | 87 |

On the final tree (after the fold; `logs/flip_final_{fr,ar}.json`): `/fr/` 525 against 278, `/ar/` 542 against
284; without lane H's rule 525 and 542; without the vocabulary's guards 375 and 389.

**Reading.** The counts agree with the final review's (523 / 276 fr, 539 / 316 ar on the compressed twins). Lane H's rules account for
none of the difference; it lives in lane S's library (the guards invalidate every verb, seal part, route step and plate
keyword of the 8 sections still waiting at the top of the page; the tier's custom property restyles the tiles' subtrees,
`<use>` shadow trees included) and in the Tab's own restyle on a longer page. Route (a) on the tier alone recovers 39
of 247; the guards would need a runtime decision in `rise.js` / `_reveal.css` (lane S, the Director: «the keyboard sees
the still»). Lane H's recommendation to the steward: **route (b)** — the base of record for §9.9 item 6 is the home
before V2 (S2's review: −4 to +8 ms against `269cf39`), and the cost against `28fa9fa` (+32 to +84 ms on the twins, the
absolute INP under 200 ms on a quiet machine) is recorded — or route (a) handed to lane S with the table above and a
quiet re-measure after it. The twins were not re-run here: nothing lane H changed moves the flip (the counts above).

### 14.4 Budgets (gzip -9, dist, after `npm run build`)

| Sheet | Final fix round (branch alone) | Merged (`7a8eecd9`) | This round | Ceiling |
|---|---|---|---|---|
| `pages/css/pages.css` | 11 277 | 11 299 | **11 306** | 12 288 |
| `pages/css/hero.css` | 10 899 | 10 899 | 10 899 (untouched) | 11 264 |
| `main.css` | 32 718 | 32 716 | 32 716 (untouched) | 32 718 |
| `core/reveal.css` · `core/portico.css` | 3 549 · 2 993 | 3 526 · 2 993 | unchanged | — |
| **Home, every sheet linked** | 61 436 | 61 433 | **61 440** (0 B headroom) | ≤ 61 440 |

**What the fixes cost.** The round's rules cost about +28 B and the equivalent rewrites below recovered about 21 B
(net +7 B, 11 299 → 11 306; gzip sizes do not add exactly, so the split is indicative).

**Where the bytes came from (equivalent rewrites only).** Each declaration removed was first found to change no
computed value when deleted from the CSSOM, on every element and pseudo-element, at fr / ar / it × 1440, 1024, 768,
390 (`tools/redundant.py`), then read against the rule that makes it redundant:
- the news titles' hover: `color` (the row's own rule sets the same ink and outranks `a:hover`) and the thickness folded
  into the `text-decoration` shorthand;
- `font-weight: var(--w-title)` on three headings and `text-wrap: balance` on two (base.css's `h1, h2, h3` rules);
- `flex: none` on the doors' arrow (`.icon`), `list-style: none` on the doors' list (`ol[role="list"]`);
- `display: grid` on the pilot's diptych and `position: relative` on its frames (the library's `.panorama`,
  `.panorama__quadro`);
- the reading text's repeated `line-height: 1.5rem` below 64 rem (each element's own rule sets it);
- the trust fields' padding written as its one differing side (`padding-block-end`; the others are the library's
  `.strato__lastra`).

**The proof that nothing else moved** (`tools/style_diff3.py`; `logs/style_diff4.json`): the committed sheet and this
round's served in turn for the same URL, every element's and pseudo-element's computed value of every property this
round touches, and every element's box, at fr / ar / it × 1440, 1024, 768, 390, gate open and gate closed (24 states).
The only differences are the intended ones: the lead's `text-wrap-style` (all), the Arabic title's `text-align` (ar),
the closed gate's `align-items` and its plates' heights. A control run serving the same sheet twice: 0 differences.

### 14.5 Tests

**Updated under the V5.20 strict rule** — both in lane S's shared guards, as the final review's merge condition and S2's
review (m3) asked; each cites V5.22 / SECTION_SYSTEM_V2 §3.1 and §4, holds a stronger invariant, loosens nothing, raises
no timeout, adds no skip. They are slices of family `v522-h` for the steward (§14.7).
- `tests/frontend/test_chapter_marks.py` — the home's exemption goes. *Before:* the home was skipped by the «no bare
  mark» rule and only had to show V5.12's two chapter marks (`HOME_EXPECTED {'compass', 'signpost'}`), which the V2 home
  no longer draws. *Now:* the home is held to the rule every page holds (no stair, no bare mark, no glyph above a title,
  one concept once), and its seals must be exactly `ile-orienta`, `ile-scudo`, `ile-accesso`, in that order, each once,
  on `/fr/` and `/ar/`.
- `tests/frontend/test_journey_w3_d.py::test_the_home_draws_the_orientations_neutral_steps_on_the_public_passage` —
  *before:* the pre-V2 include string; *now:* the one include of `components/stepper.html` with every V2 parameter
  (`size="large"`, `across=True`, `origin_seal="ile-orienta"`, the terminal, the end action, `only`), and still no
  `sequence__` class.

**New.**
- `test_home_v522_h.py::test_final_review_the_arabic_pilot_title_takes_its_seam_s_alignment_and_the_lead_never_ends_on_one_word`
  — the two title rules (end, then centre inside the 64 rem block), the lead's `text-wrap: pretty`, the interim plates'
  `align-items: start`.
- `test_home_v522_h.py::test_final_review_the_home_reads_the_input_s_modality_in_one_rule` — the home's three sheets
  name `data-input` in exactly one rule, its three class-led subjects, `transition-duration: 0s`, and the elements it
  names exist.
- `test_home_browser_v522_h.py::test_final_review_the_pilot_statement_stands_on_its_seam_axis_or_its_reading_edge` — at
  the 8 widths, in ar, fr, it and en, with the catalogue's entry present (the lead in the page's language, no `lang`;
  Arabic letters on the Arabic page; the title the locked French): from 64 rem the title's lines, the lead's lines and
  the link within 2 px of the thread's axis; below, one reading edge within 1 px (the right on the Arabic page); the
  lead's last line never one word. **It bites:** against the merged tree's sheet, swapped in and restored byte for
  byte, it fails at all 8 widths (ar 1440: centres 669 / 707 against the axis 720; ar 390: right edges 292 / 342
  against 374).

**Runs on the final tree** (one pytest at a time per database):

| Suite | Result |
|---|---|
| **The home and lane H's own** — `test_home_v522_h.py`, `test_home.py`, `test_templates_static.py`, `test_prescribed_fragments.py`, `tests/compliance/test_locked_content.py`, `tests/frontend/test_french_typography_w2_d.py`, `test_services.py`, `test_review2.py`, `tests/frontend/test_frontispiece_v515_c.py` (the per-sheet and per-page ceilings), `test_design_docs.py`, `test_css_bundle_is_current.py`, `test_static_pipeline.py` | **512 passed** (the final review's 510 and the 2 new guards; a first run caught the fold written as `transition: none` — §14.9) |
| **The guards around the merge** — `test_chapter_marks.py`, `test_journey_w3_d.py`, `tests/i18n/test_catalogues.py`, `test_page_integrity.py`, `test_rtl_static.py`, `test_locked_texts.py`, `test_loader_rules.py`, `test_state_chips_carry_a_register.py`, `test_o14_lint.py`, `test_sezioni_v522_s.py`, `test_sezioni_v522_s2.py`, `test_interior_w3_f1.py`, `test_orientation_w3_f1.py`, `tests/compliance/test_imagery_v512.py` | **738 passed** (the final review: 736 passed and lane S's two guards red; the catalogue tests green without a simulated pass) |
| **Security and contact** (the private sentinel table and the configured number read in process, never printed) — `tests/security/test_confidential_material.py`, `tests/compliance/test_no_personal_data_in_repository.py`, `apps/pages/tests/test_contact_channels_v519.py`, `tests/compliance/test_phase3_texts_not_leaked.py` | **82 passed, 0 skipped** |
| **Browser** (Playwright's headless shell, `test_ile_v5_l5b`, lock A) — `test_home_browser_v522_h.py`, `apps/pages/tests/test_browser.py` | **69 passed** (the final review's 61 and the 8 new) |
| The new browser test against the merged tree's sheet (swapped in, restored byte for byte) | 8 of 8 fail, as they should |

**Lint and line endings.** `ruff check .`: all checks passed; `ruff format --check` on the changed test modules: clean;
`manage.py check`: no issues; `makemigrations --check`: no changes. Every changed file is LF.

### 14.6 Headed checks (chromium-1234)

- **The pilot statement** (`pilot_before/`, `pilot_after2/`): 8 widths × fr, ar, it, en, reduced motion — §14.2.
- **Gate closed, the plates** (`plates/`): fr and ar at 1440, 1280, 1024 — §14.2.
- **Sweep** (`sweep.txt`): fr, ar, it, en at the 8 widths (gate open) and fr, ar at 1440 and 390 (gate closed), after
  a play-through: horizontal overflow 0, no element of `<main>` wider than the page, 0 console errors in 36 runs; page
  heights at 1440 fr 6 112 (unchanged), ar 6 103.
- **axe-core 4.13** (WCAG 2.0–2.2 A and AA, after a play-through; `axe.json`): **0 violations** in 8 runs (fr and ar,
  1440 and 390, with and without reduced motion).

### 14.7 For the steward (the merge of `v522-h`)

- **OWNERSHIP, family `v522-h`** (`FAMILY_ID` already admits `v5<nn>-h`): whole files `static/css/v5/_casa.css`,
  `templates/pages/home/_ecosystem_frame.html`, `templates/pages/home/_ecosystem_colophon.html`,
  `apps/pages/tests/test_home_v522_h.py`, `apps/pages/tests/test_home_browser_v522_h.py`; slices for what the lane
  changed in shared files — new this round: `tests/frontend/test_chapter_marks.py`,
  `tests/frontend/test_journey_w3_d.py` (lane S's guards, the cited V5.20 updates) and `locale/**` (the catalogue entry).
- **The catalogue**: already on the branch (`aa640b08`); the merge's pass is +0 −0 for lane H. Lane P2's merge, after
  this one, unions its own entries.
- **The seed**: `manage.py seed_all --only pages.home_sections` on each shared database (an untouched old pilot lead
  moves to the new one; an editor's text is never touched — `SUPERSEDED_DEFAULTS`).
- **The preview label**: «Homepage Composition V2».
- **F-M2**: the ruling (§14.3; `requests/F-M2_first_key_attribution.md`).
- **The home's CSS total is at its ceiling** (61 440 / 61 440): any later change to `core/reveal.css` counts in it.

### 14.8 Requests (lane S, S-close, the Director)

- **Lane S / S-close — F-m3:** «la protezione»'s locked anti-fraud body has plain spaces inside its guillemets, so on
  phones a guillemet breaks from its word («« vendre / » un visa» at 390; «vous « / vendre »» at 375 and 360). A
  no-wrap span around each «…» group through `locked_spans` keeps `textContent` byte-identical; one change in
  `components/sezioni/protezione.html` serves every page with the plate.
- **S-close / the Director — F-m6:** the orientation's caveat plate (`.linea__terminale`, `_linea-v2.css`) on the
  Arabic page keeps its rule on the reading edge while its French line starts at the plate's far end; the ruling S2's
  reviewer gave for «la protezione»'s wide plates should cover it, or it takes «la protezione»'s treatment.
- **Lane S — F-M2, route (a), if the steward chooses it:** the table of §14.3.
- **The Director — F-m4:** the moment is 738 px (0.82 vh at 1440 × 900) after an integrity band of 1 515 px; §3.1 sets
  ≈ 82 vh, §1 rule 5 ≥ 1 viewport.

### 14.9 Deviations and not done

- **F-M2 is not closed by this round**: lane H's share is done and measured as nil; §9.9 item 6 stays open until the
  steward's ruling is recorded.
- `text-align: match-parent` (one rule for both breakpoints) was tried and dropped: Chromium 151 supports only
  `-webkit-match-parent`. The two explicit rules cost the same bytes and hold in every engine.
- The folded keyboard rule keeps `transition-duration: 0s`, not `transition: none`: the home's token guard
  (`test_templates_static.py::test_stylesheet_motion_relies_on_design_system_durations`) holds every `transition`
  shorthand to a duration token.
- F-m1's rule names the library's two-plate modifier (`.strato__lastre--2`), 4 B cheaper than the home's own class; on
  the home only the closed gate uses it, and the sheet is page-only.
- Lane S's two guards are updated on this branch (the merge condition), not by lane S.
- The home's sheets sit at their ceiling (0 B headroom).
- Carried: F-m3 (lane S / S-close), F-m4 (the Director), F-m6 (S-close / the Director); lane M's ecosystem frame.

### 14.10 Self-scores (§10; fr and ar, 1440 and 390; the reviewer verifies)

| Dimension | Final review fr / ar 1440 / ar 390 | Now fr | Now ar | Why |
|---|---|---|---|---|
| Composition | 4.5 / 4.5 / 4.5 | 4.5 | 4.5 | unchanged compositions |
| Motion | 4.5 / 4.5 / 4.5 | 4.5 | 4.5 | unchanged |
| Imagery | 4.0 / 4.0 / 4.0 | 4.0 | 4.0 | unchanged (lane M's frame) |
| Interaction | 4.0 / 4.0 / 4.0 | 4.0 | 4.0 | held by F-M2 until the steward's ruling |
| Institutional | 4.5 / 4.5 / 4.5 | 4.5 | 4.5 | the lead in the page's language in it, en and ar (the catalogue entry on the branch) |
| Coherence | 4.5 / **4.0** / **4.0** | 4.5 | **4.5** | F-M1: the Arabic moment on one axis from 64 rem and one edge below; F-m2: no lone word |
