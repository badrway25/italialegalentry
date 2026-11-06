# V5.22 lane P1 — Page Composition V2: journeys and spaces (label v522-p1-build)

Branch `v522-p1` from design-v5 `22b0ddd` (the steward's record of the v522-s merge; worktree `C:/tmp/ile_wt/v522-p1`).
Scope: SECTION_SYSTEM_V2 §9.4 and §3.3–§3.10 — Projet pilote, Parcours (+ the interim page), the eight pathway sheets,
Entreprises (+ the «Recueil des besoins» head), Institutions (+ the collaboration head), Universités et formation,
Formation, Diplômes et titres. Built on lane S's library (merged) and lane M's frames (merged); H and P2 build in
parallel. Not merged: the branch waits for the steward.

- Database lane l6 (`ile_v5_l6`, migrated; its content is `ile_v5`'s, not refreshed); tests on `test_ile_v5_l6`, one
  pytest at a time.
- Lane server 8786 (dev settings, `ILE_DESIGN_PREVIEW=1`, `ILE_REFERENCE_DATE=2026-10-03`, `--noreload`), stopped at
  the end. Its `.env` is a copy of lane S's with `DATABASE_URL` pointed at l6 (the WhatsApp number never printed).
- Headed Chromium (chromium-1234) for every visual check; the browser tests run Playwright's own Chromium. Lock slots:
  B 20:56–21:00; A 21:16–21:20, 21:26–21:31, 21:43–21:45, 22:36–22:38, 22:39–22:42, 22:42–22:43, 22:51–22:53,
  22:57–22:58 and the closing session (§5); each released. **One breach, recorded:** at 21:13 a capture of five pages
  (about two minutes, headed) ran while both slots were held by lanes P2 and H — my lock command printed «both busy»
  and the shell went on to the capture. Every later session was gated on taking the slot (`… || exit 1`, then
  `tools/with_lock.sh`, which waits for a free slot).
- Scripts: `C:/tmp/ile_v5_council/.work/v522-p1/` (`tools/shots.py` the headed captures and their probes,
  `tools/icons_probe.py`, the `patch_*.py` edits, `logs/`). Evidence: `C:/tmp/ile_v5_council/evidence/v522/p1/`
  (`r1` … `r8`, full-page captures with `report.json`; `catalogue/` the five msgids' renderings).

## 1. What the owner sees, and where

Every body below is a V2 section (`.sez`, its ground and rhythm declared, one moment a page at most); the chapter device
(`chapter__head`, the bare marks, the V4 registers) has left these bodies — only the preserved «Recueil des besoins» form
keeps its chapter and sticky side (§24, EN-3). The heads are KEEP (lane S's T1 folio seals). One stylesheet request a
page, as before: each page links its own sheet (`css/dist/<family>/<page>.css`), which is the family's sheet (its
import list unchanged), then lane S's library and the page's partials. In Arabic every route runs with the page and a
French locked label keeps its own direction, ending on its marker's side.

**Projet pilote** `/xx/projet-pilote/` (§3.3)
- PP-1, paper band: the pilot's T1 seal `ile-pilota` beside «La séquence du projet pilote»; the eight locked stations on
  «la linea V2» — ILE Mono numerals at 36, each station's concept tile (`icons.PILOT_STATION`, station 6 `ile-arch` the
  page's one gold node), the locked capitals, whole words at every width; one stepped row from 80 rem, 4 + 4 with a
  carriage return from 48 rem, down the reading edge on a phone. The mandatory notice is the route's terminal status
  plate right under it («attesa» register, a dashed drop from the route), whole, never collapsible. LINE DRAW.
- PP-2, stone, the page's moment: two arched doors — the companies' on night (its half of the team sentence, cut at its
  own full stop; the locked primary), the institutions' on paper (its half; the locked secondary); the help line under
  both. On entry the thresholds light, the primary's first; hover and focus raise a door.
- PP-3, the stone strip «l'approdo»: the Forum typographic on its night face (Q4), the mission motif low, one light sweep.

**Parcours** `/xx/parcours/` (§3.4; `index_interim.html` speaks the same language)
- PA-1, the moment «il tracciato delle famiglie»: the eight pathways on four family lanes (work, study, family, other),
  each lane headed by its licensed family frame (drawn exactly at its `sizes`), the numerals 01–08 the prescribed order.
  The family filter (native radios) lights its lane and turns the others to the quiet ink (never an opacity); every
  station stays in the layout; a polite line says the count («3 parcours affichés»).
- PA-2, brand band «Comment ça marche»: the locked sentence cut on its own arrows into four plates (numerals by CSS
  counters, `icons.HOW_STEP` tiles), station 1 to the questionnaire, station 3 to Formation; the caveat under them.
- PA-3: «Dans l'Espace Personnes» as lane S's grid, then «la protezione» in its own stone band.

**The eight pathway sheets** `/xx/parcours/<slug>/` (§3.5)
- The «Aperçu» strip; PS-1, the moment «il filo»: the five milestones down a rail with their tiles (`icons.SHEET_STEP`),
  dashed nodes (still being verified); the documents as plates; the Sommaire hidden from 64 rem.
- PS-2, night band «chi décide»: the authorities as an arc of seats (`icons.AUTHORITY_SEAT`), each link with its host;
  the ILE node with the lead «Liste indicative… n'intervient pas… ne délivre aucune autorisation».
- PS-3 «la protezione» (+ the editors' warnings as plates); PS-4 «Ressources»: each Italian term a disclosure
  (`<details name="termini">`) opening its locked definition (`p3.glossary.terms`, its `lang` kept) with «Voir dans le
  glossaire»; the space's links a compact row with their glyphs. PS-5 «la boussole» (anchor `orientation-chapter-title`
  kept: the registry's concept for the orientation chapter).

**Entreprises** `/xx/entreprises/` (§3.6): EN-1 the quotation (its rule draws down) and «il flusso», the three moments
(`icons.COMPANY_MOMENT`); EN-2 the territory panorama band; EN-3 the form, preserved; EN-4 «Transparence», the
question and its answer cut at its own «Non.» and colon into the split (a drawn divider); EN-5 «l'approdo».
**Recueil des besoins** `/xx/entreprises/recueil-des-besoins/`: the compact frontispiece (`ile-impresa`), the form
untouched.

**Institutions** `/xx/institutions/` (§3.7): IN-1 «l'emiciclo» on the chamber photograph — six seats on an arc
(`icons.RECIPIENT_SEAT`), the locked recipients sentence whole on its plate, each recipient a span that lights its seat
(hover, focus); the proposal link and the help line; IN-2 «l'approdo». **Collaboration** heads
(`/xx/collaboration/institutions/`, `…/universites-formation/`): the compact frontispiece (`ile-istituzione` with the
hemicycle's note when G3 is open; `ile-sapere`).

**Universités et formation** `/xx/universites-et-formation/` (§3.8): U1 «la filiera» — three plates on a route
(«Avant le départ», «En Italie», «Après l'arrivée»), the research branch on the second, the gold arch at the arrival;
the campus destination frame (`universities.exchange`, drawn at its `sizes`) on 7/12, the last plate overlapping it;
«Tous les parcours réguliers» and the help line.

**Formation** `/xx/formation/` (§3.9): F1 «la traversata» — the two times on one crossing line from the `earth` node to
the gold `ile-arch`, each its kicker, h2, text, link and frame under the line (`training.before`, `training.after`),
the first time's notice docked to its frame, always visible; the locked body whole, its first sentence set larger in
place; the line drawn by scroll. F2 the grid (Diplômes the wide tile), «la protezione», «la boussole».

**Diplômes et titres** `/xx/diplomes-et-titres/` (§3.10): D1 «le dossier» — five stations (numerals, `icons.DIPLOMA_STEP`
tiles, dashed nodes; the status said in words under them, «En attente de vérification»); stations 3–5 open their term's
locked definition in place, one at a time, the first open at load; D2 «Qui décide ?» the sticky aside (a raised stone
plate, the stamp tile, the statement verbatim). «la protezione», the grid (Formation the wide tile), «la boussole».

## 2. Deviations from the prescription (each a decision taken here, for review)

1. **PP-1's seal beside the title, not in the route's first seat.** Lane S's stepper draws `origin_seal` in station 1's
   seat, which drops station 1's tile (`briefcase-business`) and breaks §4.10's register rule (the pilot's eight
   stations all or none: `test_interior_w3_f1` failed 7/8). §3.3 lists eight tiles and «the T1 `ile-pilota` seal beside
   the title»: both are drawn that way. Request to S below.
2. **PP-2 is the pilot's moment, PP-1 a band** (§3.3's table has the route as the moment): the page's two actions are
   its interactive section; one moment a page (§1 rule 5).
3. **Diplômes on a phone: one definition open at a time**, as from 64 rem (§3.10 asks «on phones all are open»). The
   native exclusive disclosure (`name`) keeps one open at every width; opening all on phones needs script or a second
   markup. Left for review.
4. **The approdo tiles are typographic** (no glyphs): the Forum tile is typographic (Q4) and a register draws its glyphs
   all or none.
5. **The pathway terms keep no chip**: each term is the summary of its own disclosure in lane S's «indice» row (PS-4's
   «each Italian term chip is a `<details>`»), the chip's border dropped in that row. This leaves
   `test_state_chips_carry_a_register::test_a_tag_is_a_term…` below its floor (§5, requests).
6. **New strings render in French on it/en/ar pages until the catalogue pass** (§6): the three kickers of «la filiera»,
   the hidden «Destinataires», «Voir dans le glossaire».

## 3. Provenance (21st.dev, adapted — no code copied, no package added)

| Section | 21st.dev candidate (id) | Taken | Refused |
|---|---|---|---|
| PP-2 «due porte» | Split Hero With Image Cards (19078) | two inverted faces side by side, each its own call | avatars, social proof, image overlays |
| EN-4 «Transparence» | Comparison Section (26826) | the question and its answer as two sides of one divider | check/cross columns, pricing tiers |
| IN-1, PS-2 arcs | MultiOrbitSemiCircle (5180) | seats on a half-circle around a centre | orbiting motion, avatars, logos |
| U1 «la filiera» | Metro Map Image Gallery (43148); Animated Roadmap (8113) | stations on a line toward a destination frame; the branch | gallery scroll-jacking, progress percentages |
| F1 «la traversata» | Lifeline (32658) | one line crossing two times, frames under it | timeline dates, a progress fill |
| D1/D2, PA-2 | Sticky Content Wrapper (26064); Vertical How It Works Timeline (26902); Timeline (35051) | the pinned aside beside a process; numbered plates on a rail | ticks, completion states, counters animating |

## 4. Budgets (gzip -9, measured on the built tree)

| Sheet | Bytes | Ceiling (`test_pages_v522_p1`) |
|---|---:|---:|
| `ecosystem/ecosystem.css` (the family's) | 4 874 | 11 264 |
| `ecosystem/pilot.css` | 8 974 | 9 728 |
| `ecosystem/companies.css` | 8 142 | 9 216 |
| `ecosystem/institutions.css` | 8 182 | 9 216 |
| `ecosystem/universities.css` | 7 419 | 8 448 |
| `pathways/pathways.css` (the family's) | 4 716 | 11 264 |
| `pathways/index.css` | 9 424 | 10 240 |
| `pathways/sheet.css` | 9 499 | 10 240 |
| `pathways/training.css` | 8 640 | 9 728 |
| `pathways/diplomas.css` | 8 802 | 9 728 |
| `main.css` | 32 718 | 32 718 (untouched) |

Every page's stylesheets together (its page sheet, `fronte.css`, the global sheets) stay under the 56 320 B page total
(asserted per page). Requests per page unchanged (one page sheet replaces the family sheet).

## 5. Tests

**New modules** (lane P1's, §9.7: a lane's browser checks in `test_*_v522_<lane>.py`):
- `tests/frontend/test_pages_v522_p1.py` — 55 cases: each page's one sheet, its import list and its ceiling, the page
  totals; the form pages' sheets; the chapter device gone, every body a V2 section with its ground and rhythm, one
  moment at most; one primary and the registry's glyphs only (never `ile-steps`, never a check but the diplomas'
  `badge-check`); the pilot's seal beside its title, its eight tiles in `PILOT_STATION` order and the status plate
  after them; the doors cut per language; the route board (the eight on their lanes, the native filter, the polite
  count, a non-live station); «Comment ça marche» whole; «la protezione»; the sheet's rail, arc of seats with hosts,
  terms in place and «la boussole»; the companies' flow, split and approdo; the hemicycle's sentence as spans lighting
  their seats; «la filiera»; «la traversata»; the dossier (its status in words, one definition open, «Qui décide ?»);
  the form pages' compact heads.
- `tests/frontend/test_pages_browser_v522_p1.py` — 11 cases (Chromium, gate G3 open): the ten pages hold their width at
  1440, 768 and 390 in fr and ar; a section below the fold waits, plays once and holds nothing of its own; under
  reduced motion no state is written and nothing runs; every family frame, the two times' frames and the campus frame
  drawn at their `sizes` at six widths in fr and ar; the family filter keeps the eight stations and turns the other
  lanes to the quiet ink (never an opacity) with the polite count; the diplomas' definitions open from the keyboard,
  one at a time, the focus visible; without script every station, milestone and term stands; the pilot's capitals
  never broken inside a word at 1280, 1366 and 1440; in Arabic the French titles end on their marker's side, the lane
  names untracked, the pilot's route running with the page.

**Updated under V5.20's strict rule** (each change cites SECTION_SYSTEM_V2, the approved composition, and keeps the same
invariant or a stronger one; only P1's pages' assertions moved):
- `apps/ecosystem/tests/test_companies_page.py`, `test_gated_pages.py`, `test_compliance.py` (§3.3, §3.6–§3.8: the
  quotation and «il flusso», the transparency split, the hemicycle's sentence as spans, the filiera's links, «la linea
  V2» and the terminal status plate, l'approdo; the spaces' V2 partials under the same token and motion rules);
- `apps/pathways/tests/test_views.py`, `test_compliance.py`, `conftest.py` (§1 rule 6, §3.4, §3.5, §3.9: a re-composed
  locked text read whole in its element; the numerals as the prescribed order; «la protezione»; «il filo»);
- `tests/frontend/test_interior_w3_f1.py` — how it works (PA-2's plates), the terms' targets (44 px under every pointer
  now, a stronger floor) and the pilot's row (§3.3 PP-1: one row from 80 rem; M5's whole words measured in the
  browser), the pilot's labels (the large passage's capitals), the authority's host (PS-2's arc);
- `tests/frontend/test_orientation_w3_f1.py` — the six-icon ceiling with lane S's §4.10 register rule (as in
  `test_interior_w3_f1`), the advice pages ending on «la boussole» with the grid leaving the page's own tile out, the
  diplomas' dossier, Formation's traversata, the anti-fraud entry as «la protezione» (its seal, its title, its locked
  body whole — still said three times, never amber).

**Shared guards met in P1's own files** (no guard edited): `templates/ecosystem/partials/pilot_flow.html` is back
(§3.3 names it; `stepper.html` and DESIGN_SYSTEM_2026 cite it) and holds PP-1; the pilot's capitals rule lives in
`_spaces.css`, the family's one modifier sheet of «la linea» (`test_journey_w3_d`); no gradient in an app sheet — the
doors' thresholds, the arrival lights and the hall's veil are shadows on tokens, the night door's face
`--grad-brand-dark` (`test_design_docs`); the registers' variable glyphs are registry-fed names (`entry.glyph`, `glyph`)
or the composition's own literal symbols (O14 lint); the orientation band keeps the anchor `orientation-chapter-title`
(`test_icons`); W4-A's D5 rule kept for S-close (request 3); no library name in a template comment.

**Runs (targeted, one pytest at a time on `test_ile_v5_l6`):**
- Final non-browser pass (`-m "not browser"`: the two families' app tests, `apps/enquiries/tests`, the lane's module,
  the shared page modules and guards that read these pages — interior, orientation, frontispiece, journey, chapter
  marks, icons, sezioni, mobile/RTL, bundle, pipeline, tokens, motion, loader, chips, forms, design docs, O14, imagery
  —, `tests/i18n`, `tests/compliance`, `apps/pages/tests/test_prescribed_fragments.py`, `test_templates_static.py`):
  **1 805 passed, 9 failed** (31 min), the nine all named:
  - the five new msgids (§6): `test_catalogues.py` ×4 and `test_page_integrity.py::test_latin_text_on_arabic_pages…`,
    until the catalogue pass;
  - lane S's three, red on design-v5 since the v522-s merge (DL54-182, «handed to lane S»):
    `test_loader_rules.py::test_l3…` (`sezioni/mappa.html`), `test_state_chips…::test_data_register…`
    (`sezioni/approdo.html`), `test_rtl_static.py::test_every_horizontal_shift…` (`_sec-tracciato.css`);
  - one caused by P1's recomposition, for S: `test_state_chips…::test_a_tag_is_a_term…` (request 2).
- Browser (Chromium, slot A 23:25–23:28): `test_pages_browser_v522_p1.py` **11 passed**, and lane M's
  `test_imagery_v522_m.py::test_the_live_campus_frame…` **12 passed** on this branch (the campus frame, recomposed in
  «la filiera», still drawn at its `sizes`, its 3:2 file and its pick).
- Fixed on the way: a CSP-blocked string predicate (now a function with its argument); the pilot capitals' rule losing
  to the library's on bundle order (now one class more specific); the frontispiece's own load halo counted against a
  section (the check now scoped to the section).
- `ruff check` and `ruff format --check` clean on the lane's Python; LF everywhere; `npm run build` reproducible (a
  second build leaves the tree unchanged); `main.css` 32 718 B gzip -9, untouched.

## 6. New user-facing strings (FR msgids; renderings for the catalogue pass)

`locale/**` is S-close's (§9.7): the five msgids are not in the catalogue on this branch, so
`tests/i18n/test_catalogues.py` (4 cases) and `tests/i18n/test_page_integrity.py::test_latin_text_on_arabic_pages…`
fail on exactly these five, as lane M's did. Ready for the merge: `evidence/v522/p1/catalogue/p1_catalogue_entries_{it,en,ar}.po`
(`scripts/i18n_audit.py --sync`, these msgstr, `--compile`). Locked text is never translated; the Arabic is reviewed
for RTL (no Latin inside, no punctuation that flips).

| FR (msgid) | Where | IT | EN | AR |
|---|---|---|---|---|
| Avant le départ | `apps/ecosystem/services.py` (U1 kicker) | Prima della partenza | Before departure | قبل المغادرة |
| En Italie | `apps/ecosystem/services.py` (U1 kicker) | In Italia | In Italy | في إيطاليا |
| Après l’arrivée | `apps/ecosystem/services.py` (U1 kicker) | Dopo l’arrivo | After arrival | بعد الوصول |
| Destinataires | `templates/ecosystem/institutions.html` (IN-1's hidden h2) | Destinatari | Recipients | الجهات المستهدفة |
| Voir dans le glossaire | `templates/pathways/detail.html`, `diplomas.html` | Vedi nel glossario | See in the glossary | انظر في مسرد المصطلحات |

The terminology follows the catalogue: «Glossaire» → «Glossario» / «Glossary» / «مسرد المصطلحات»; «Formation avant le
départ» → «التكوين قبل المغادرة». D1's caption reuses the catalogue's «En attente de vérification» (no new msgid).

## 7. Requests to other lanes

**Lane S (library and shared guards; nothing of theirs edited here):**
1. `components/stepper.html` — `origin_seal` draws the seal in station 1's seat and drops its tile, which breaks §4.10's
   all-or-none rule for a register (the pilot failed 7/8 in `test_interior_w3_f1`). P1 draws the eight tiles and sets
   the seal beside the title (§3.3). If the seal should open the route, draw it as an unnumbered origin before
   station 1, or let the guard count a station's `.sigillo` as its glyph.
2. `tests/frontend/test_state_chips_carry_a_register.py::test_a_tag_is_a_term…` — its floor (≥ 9 tags, `pathways/detail.html`
   among them) predates §3.5 PS-4 and §3.10 D1, which turn the pathway's and the diplomas' term chips into disclosures
   (no `class="tag"` left in either template; 5 found: `community/room.html`, `companies/need_detail.html` ×2,
   `helpdesk/detail.html` ×2). A strict-rule update: the exact set of the remaining templates, and the terms'
   disclosures carry neither a register nor a mark. **Red on this branch until then.**
3. `tests/frontend/test_mobile_rtl_w4_a.py::test_the_page_only_sheets_hold_the_rest` pins W4-A's D5 rule
   (`.linea__more a`) in `_pathways.css`; no page of the family draws it any more. P1 kept the rule (commented) for
   S-close's coverage-measured dead-rule pass (§9.6), which can retire it with its guard line.
4. `tests/frontend/test_design_docs.py::_vocabulary_before` does not let a page partial read the library's documented
   properties (`--sez-i` of `.sez-seq`, `--aud` of `[data-audience]`, `--sez-gap`). P1's partials therefore declare
   their own stagger indices (`--pp-i`, `--fi-i`, `--ds-i`, `--co-i`), use the audience tokens, and restate `--sez-gap`'s
   clamp once (`_pilot.css`). If the library's vocabulary should be readable, the guard can learn it.
5. `_sec-tracciato.css` — the route board's light runs left-to-right in Arabic: P1's page rule
   (`[dir="rtl"] .percorsi-tracciato .tracciato__linea::after` in `_index.css`) mirrors it; the library's own twin
   would also clear S's red `tests/i18n/test_rtl_static.py` case.
6. `_sezioni.css` — `.testa__label` (and other ILE Mono labels) keep their tracking in Arabic, which breaks Arabic
   words; P1 untracks them under `:lang(ar)` in its partials (`_spazi-v2.css`, `_persone-v2.css`).
7. `_fronte.css` — the collaboration form's hemicycle note (`ecosystem/partials/emiciclo_nota.html`, the institutions'
   compact head when G3 is open) has no layout rule on those pages, which load `fronte.css` and `lettura.css` but no
   P1 sheet: a small `.emiciclo-nota` rule (the drawing beside the sentence) belongs in `_fronte.css`.
8. `panorama.html` — the photo credit of a full-bleed band (100vw) sits under the scrollbar at its inline end.
9. `_sezioni.css` — `[dir="rtl"] .sez [lang="fr"]:not(html)` turns any French-tagged element of a section
    left-to-right, containers included: «la linea V2» puts the labels' `lang` on its `<ol>`, so in Arabic the pilot's
    whole route ran 01 → 08 from the left, its labels drifting off their tiles (found in the closing check; it was
    already so at r3). P1 gives the list the page's direction back (`_spaces.css`, measured by
    `test_an_arabic_page_keeps_its_french_titles_on_their_marker_s_edge`); the library rule should exclude lists
    (base.css's principle), which also covers the home's S2 if it shows a French fallback.
10. S-close: `templates/pathways/_antifraud_callout.html` is dead (no template includes it; `test_mobile_rtl_w4_a`
   still reads it); `docs/design/DESIGN_SYSTEM_2026.md` §2.1 describes the V5.4–V5.12 compositions of `ecosystem.css`
   and `pathways.css` — the eight page sheets need their rows (the three pathway templates now name the family's
   sheet in their comments, which keeps the inventory truthful meanwhile).

**The steward:** carry the five msgids' entries (`evidence/v522/p1/catalogue/`) in P1's merge commit, as for lane M,
so design-v5 keeps the catalogue at FAILURES 0 until S-close.

**Lane P2:** `tests/frontend/test_interior_w3_f1.py` and `tests/frontend/test_orientation_w3_f1.py` cover pages of both
lanes; P1 changed only its own pages' assertions there (§5), first in the merge order (§9.7 «Shared test modules»).
P2 rebases on them.

## 8. Not done

- §3.10 D1 on a phone: one definition open at a time instead of all (deviation 3).
- Headed passes not taken at every width in Arabic: ar 1440 (all pages and the two form heads), ar 390 (Parcours, a
  sheet, Diplômes, Projet pilote, Entreprises, Institutions, Universités, Formation); ar 768 only through the browser
  tests' overflow probe (all ten pages at 1440, 768 and 390 in fr and ar).
- The catalogue (§6): not in `locale/**` (S-close's).

## Round 1 improvements (label v522-p1-improve1)

Answers `evidence/v522/p1/QA_ROUND1.md` (5 major, 12 minor; pilot below the bar on five dimensions, Parcours and the
sheets each losing an interaction, Formation's notice illegible). Branch `v522-p1`, worktree `C:/tmp/ile_wt/v522-p1`, on
design-v5 `22b0ddd` (unchanged since the build: nothing to merge). Lane server 8786 (DB l6, reference date 3 Oct);
a temporary 8796 (same tree and DB, 25 Sept: gate G3 closed) for the interim page, stopped after its check. Headed
chromium-1234 for every check. Tools: `C:/tmp/ile_v5_council/.work/v522-p1-improve1/tools/` (`probe.py` headed
probes and captures, `sweep.py` the width sweep, `axe_keys.py` / `keys2.py` axe and the keyboard walk, the `patch_*.py`
edits, `with_lock.sh`); evidence `C:/tmp/ile_v5_council/evidence/v522/p1/imp1/`. Lock sessions (`logs/locks.log`), each
under 25 min and released (2 November): B 00:55, B 01:01–01:10 (short probes), A 01:11–01:20, A 01:25, B 01:33–01:35,
A 01:35–01:43 (sweep, axe, keys, interim, stills), A 01:50, B 01:50, B 01:53, then the browser tests: A 02:24–02:27,
B 02:32–02:36, A 02:40–02:44, A 02:51, B 02:59, B 03:00–03:03, B 03:03–03:05, B 03:05–03:13, B 03:13–03:14.

### R1. What changed, finding by finding

**M1 — the pilot's capitals (PP-1).** §3.3's «one gently stepped row» from 80 rem (`ecosystem/_spaces.css`, the
family's one modifier sheet of «la linea»): the odd stations' capitals above the route, the even ones' below it, each
numeral at the line beside its tile (rows: capitals · numeral · tile · numeral · capitals; the route at the tiles' foot).
Two neighbours never share a line, and a station's words have two columns' room less 16 px
(`max-inline-size: calc(200% + 2 × gap − 16 px)`), balanced on two lines when they need two. Measured (the text boxes
of every pair of labels): the closest pair 32 px apart at 1280, 33 at 1366, 28 at 1440, 58 at 1920 (fr), 29 at 1440
(ar); 31 at 1024 and 23 at 768 (4 + 4, carriage return, unchanged); no word broken at any width.
`test_the_pilot_s_capitals_never_break_inside_a_word` now measures every word and every pair of boxes (≥ 16 px) at
1280, 1366, 1440 and 1920 in fr, it, en and ar — the predicate `lines <= words` is gone (m12).

**M2 — the pilot below the bar.** §3.3's map restored: PP-1 is the page's moment (`data-rhythm="moment"`), PP-2 a band.
- *The route plays on a desktop.* The route is its own trigger (`data-sec="linea"` on `[data-diagram="pilot-sequence"]`,
  S's runtime): at 1440 × 900 the section's top is in the first screen but the route waits (measured `wait` at load) and
  draws segment after segment when it is seen; the section's own release (a phone) leaves the route's verbs alone.
- *Station 6 is the arrival.* `ile-arch`'s node is edged in the identity gold, its threshold rule run to the whole foot in
  gold, a gold light at its sill (26 %, a box-shadow on tokens — no gradient in an app sheet), its label at 600; the
  light comes when the line reaches it (1.4 s). The glyph keeps its ink (§4.4). One gold element in the body.
- *The terminal plate.* The status notice spans the route's width from 64 rem — its title on its line's start, its
  words at their measure beside it (no empty half); from 80 rem the route runs on past station 8 and turns down, dashed
  in the «attesa» register, into the plate's far corner. Still whole, never collapsible.
- *The seal* is the body seat (72 × 88 from 80 rem).
- *The doors (PP-2)* are a band sized to their content (≈ 0.75 vh at 1440): the head on four columns, two TRUE arched
  doors on the other eight — crowns full semicircles (the radii clamp to half the width), feet square — standing on one
  sill 12 px past each side: the brand's doorway, and the `ile-pilota` mark (two arches across one sill) at the scale of
  the page. Each door's audience disc in its crown, its half of the team sentence at the springing line, its locked call;
  the help line under the sill. The two doors stand at one height, their calls on one line (a row of auto, auto, 1fr,
  the call at the foot). Below 80 rem the head above; on a phone the doors stacked.
- *The approdo (PP-3)*: a one-tile band lays its tile across the band beside the head — the Forum's name and its line
  side by side on the night face (`_spazi-v2.css`, any space page with one tile) — never a lone card in half an empty
  strip.
- *Interaction*: under the hand the route lights up to the station pointed at (accent, never gold); the doors (m6).

**m6 — the doors' parity.** Hover and keyboard focus alike raise a door 2 px and bring its threshold to full light
(measured on focus: `translate: 0px -2px`); from the keyboard at once.

**M3 — Parcours on a phone.** The choice and its count line are one bar (`.percorsi-scelta`, `pathways/_tracciato.html`),
sticky under the letterhead below 48 rem, with its own ground and a hairline under it; the legend is kept as the
fieldset's name and not printed (it overprinted the board); the count is read in the bar. A chosen family folds the other
lanes to their names (their frames and stations leave until «Tous»), so the chosen lane stands under the bar — measured
at 390: «Autres voies» from the board's top, the lane at 592 px under the bar's foot at 155, «1 parcours affiché» in the
bar; fr and ar. Cards scroll in under the bar from the keyboard (`scroll-margin`; the walk: no focus under the bar or
the letterhead, fr and ar). The phone board is shorter: a lane's name on a plate at its frame's top corner, a card's
line across the card's width, tighter leading, lanes closer — PA-1 3 433 → 3 050 px at 390 (4.1 → 3.6 screens),
3 600 → 3 222 at 360 (4.5 → 4.0). *Limit:* a choice made while reading deep in another lane folds the board above
the reader, who then stands below it; CSS cannot scroll — request 11 to lane S (a few lines in the section runtime).

**M4 — the sheets' rail.** The «Sommaire» is the page's (`templates/pathways/detail.html`, `_sheet.css`): ONE sticky rail
(`nav.filo__rail.scheda-rail`, `data-sec-js="spia"`, named by its visible title «Sommaire de la page») spanning every part
it names — Aperçu when present, Étapes, Documentation, Autorités, Avertissements, Ressources, Orientation. From 64 rem the
parts keep their full-bleed grounds and set their words on the nine columns after the reading edge's three; the rail
stands on those three as a paper plate that reads on every ground (PS-2's night band drawn under it); only the plate
takes the pointer. Measured at 1440: the plate at 80–380 px at `#autorites` and at `#orientation`, `aria-current`
marking «Autorités», then «Orientation». Below 64 rem the head's «Sommaire» is the index, as before. In Arabic the rail
is on the right.

**M5 — the Formation notice.** Docked under its frame at the frame's width (not on the 2/12 beside it): 21.6 rem of words
at 1440 (3 lines), 18.6 rem at 1280 (4), 15.1 rem at 1024 (4, under the frame as asked below 80 rem), 13.5 rem at 390;
never a word broken (`overflow-wrap: normal; hyphens: manual`). The two times now share rows (a subgrid of columns and
rows): the nodes, kickers, titles, texts and frames each on one row, the frames top-aligned, each time's link under its
text. New browser test on the measure at 1024, 1280 and 1440.

**m5 — Formation's titles** at one size (28 px; the locked capitals tracked). **Formation's interaction**: a time answers
the hand and the focus alike — its node's threshold runs and its glyph shifts 2 px; the second time's sends the light
along the crossing from the origin to Italy's arch.

**m1 — one reading edge per French box in Arabic.** Station cards: title and line on the card's edge, with the numeral
(measured at ar 1440: |end(title) − end(line)| ≤ 2 px on the eight cards, now a browser assertion); the filiera's
plates (title, line, the branch's) the same; Formation's second time: title and body from the block's own start. Also:
an Arabic page's French authority name centred on its seat like the Italian ones (PS-2).

**m2 — the campus frame develops** as the route arrives (900 ms after the section's release): the page rule now
outweighs the library's still for a V2 section's photograph (`.sez [data-reveal="mask"] > picture > img { animation:
none }` beat it). Measured: `grayscale(1)` while the section waits, `none` once the route has arrived (browser test).

**m3 — EN-4**: the two halves at one ink and one weight (the boundary is never the quieter half).
**m9 — the numerals** are read with their stations (no `aria-hidden`): the prescribed order is said.
**m10 — the interim strip's lead** at 36 rem (measured 576 px at 1440, G3 closed on 8796).
**m11 — U1's title** «Formation et mobilité régulière» (an existing catalogue msgid, translated in it/en/ar).
**m12 — tests**: see M1 and §R4.

**Budget move (no change on screen).** The preserved form's chapter rules (EN-3) left the family's partial for the one
page that draws them (`_spaces.css` → `_companies.css`, unchanged, later in that page's bundle; the form section's
geometry measured identical to the base preview 8780: side 92/308/397/228, panel, form 388/592/840/720). The three other
spaces stop carrying them. The family's partial moves nothing (`apps/ecosystem/tests/test_compliance.py`): the
pilot's motion and its arrival live in `_pilot.css`, on the route's own structure.

### R2. Not done, and why

- **m4 (the collaboration head's hemicycle note).** The form pages load lane S's sheets only (`fronte.css`, `lettura.css`;
  `test_the_form_pages_add_the_band_s_sheet_and_nothing_else`), so the side annotation needs a rule in `_fronte.css` —
  request 7 below, now with the rule.
- **m7** is not P1's (the catalogue and S's guards). This round adds **no** msgid (every new string is an existing one).
- **m8 (Diplômes on a phone: one definition open at a time).** Kept as deviation 3 for the Director: «all open on phones»
  needs a second markup (the locked definitions printed twice — RH-5) or a script; the native exclusive disclosure
  stays the same at every width, each definition one tap away, the first open.
- **Parcours on a desktop** (composition and imagery targets 4.5): not recomposed this round; the reviewer called the
  board, its frames and its filter strong.
- **A measuring note for the reviewer.** Playwright's full-page capture lays the page out at another width for an instant
  (measured on /parcours/: `matchMedia` change events for `(min-width: 48rem)` and `(min-width: 80rem)`, a `resize`):
  every entrance keyed to a width query replays — the heads' own sequences on every page, and the pilot's route — so a
  full-page capture with motion shows them mid-draw. Judge motion in viewport captures (or with reduced motion, the
  designed still).

### R3. Self-scores (§26, at 1440 and 390, fr and ar)

| Page | Comp. | Motion | Imagery | Interaction | Institutional | Coherence |
|---|---|---|---|---|---|---|
| Projet pilote | 4 | 4 | 4 | 4 | 4.5 | 4.5 |
| Parcours | 4 (desktop unchanged; target 4.5) | 4 | 4 (target 4.5) | 4.5 | 4.5 | 4.5 |
| Pathway sheets | 4 | 4 | 4 | 4 | 4.5 | 4.5 |
| Entreprises | 4 (m3 only; target 4.5) | 4 | 4.5 | 4 | 4.5 | 4.5 |
| Collaboration heads | 3.5 (m4, request 7) | 4 | 4 | n/a | 4.5 | 4 |
| Universités | 4 | 4 | 4 | 4 | 4.5 | 4.5 |
| Formation | 4 | 4 | 4.5 | 4 | 4.5 | 4.5 |
| Diplômes, Institutions, Recueil | unchanged (passed) | | | | | |

### R4. Tests

**Changed under V5.20's strict rule** (each old expectation conflicts with SECTION_SYSTEM_V2's approved composition or
with QA_ROUND1's finding; the new behaviour intended; the same invariant or a stronger one):
- `tests/frontend/test_pages_browser_v522_p1.py` — `test_the_pilot_s_capitals_never_break_inside_a_word`: every word on
  one line and every two labels' boxes ≥ 16 px apart, four widths × four languages (stronger: overlaps are caught);
  `test_a_section_below_the_fold_waits…`: the pilot's route held at 1440 × 900 and drawn once (M2 f), the campus frame
  black and white while waiting and in colour after (m2); `test_an_arabic_page…`: a card's French title and line on one
  edge (m1). New: the status plate across the route and station 6's gold (M2 e), the phone's bar and choice (M3), the
  sheet's rail in reach from every part (M4), the Formation notice's measure (M5).
- `tests/frontend/test_pages_v522_p1.py` — the pilot's moment/band, the route's trigger, the body seat, the doors on one
  sill (M2); the board's bar holds the choice and its count, the numerals read (M3, m9); the sheet's rail spans every part
  it names and the first part holds no index (M4: stronger — the old test accepted a rail inside «Étapes»); U1's title (m11).
- `tests/frontend/test_interior_w3_f1.py` — the pilot's row: the caps rule and the stepped row's structure (m12); only
  this block edited (the module is shared with P2 and not ruff-format clean at its base: no reformatting).
- `tests/frontend/test_browser_w3_f1.py::test_the_pilot_s_stations_never_break_a_word` (shared module; P1's pages, P1
  first after H) — on the V2 markup: every word whole at 1280, 1366 and 1440, eight on one row from 80 rem (§3.3, where
  fdd6e34 put eight a row only from 90 rem: legibility now held by the stepped row — odd capitals above the route, even
  below, asserted — and by the ≥ 16 px measure above).
- `apps/ecosystem/tests/test_browser.py` (P1's) — left red by the build (it read `.pilot-diagram`, the recruitment notice,
  `p.chapter__statement`, `ul.approdi` and the family's one sheet request, all gone with the V2 recomposition; the build
  ran its own browser module only): each check on the V2 markup with the same invariant (the sequence vertical on a
  phone and one mirrored row on a desktop, never clipped, never hidden; each page's own sheet from the family's folder;
  French fallbacks keeping their direction, lists mirrored).
- `tests/frontend/test_browser_v515_c.py` (V5.15's developing frames; P1's two pages only) — the frame is brought to the
  middle at once (`behavior: 'instant'`) before it is read: the page's `scroll-behavior: smooth` made the 600 ms wait read
  Formation's second frame short of the middle at 390 (grayscale 0.03; at the middle it is grayscale(0), measured). The
  assertion is unchanged.
- `tests/frontend/test_mobile_rtl_w4_a.py` — the Formation entry of the stand-alone links' target floor reads the V2
  page's way-further links (`.traversata__altro a`; the old line's `.linea__more` left with its markup at the build — red
  since then): the same floor, measured on them (finger 282 × 56 and 232 × 44, pointer 56 and 28 px high). The
  static D5 line of request 3 stays for S-close.
- `apps/pathways/services.py` — `FAMILY_SIZES_V2` on a phone follows the narrower trunk indent (100vw − 5.5 rem from
  26.875 rem, 100vw − 5 rem below): the frames drawn exactly at their `sizes` again (the browser test measures it).

**Runs**: see §R5.

### R5. Runs, budgets, evidence

**Runs** (lane DB `test_ile_v5_l6`, one pytest at a time; the machine shared with lanes H and P2):
- Non-browser, targeted (`tools/run_nonbrowser.sh`: the two families' app tests, `apps/enquiries/tests`, the lane's
  module, the shared page modules and the guards that read these pages, `tests/i18n`, `tests/compliance`,
  `test_prescribed_fragments`, `test_templates_static`): **2 347 passed, 10 failed** (31 min). Nine are the build's
  declared nine, unchanged (§5 of the build notes; QA_ROUND1 m7: the five msgids' catalogue cases until the steward
  carries `p1/catalogue/*.po`, S's three, the tag guard of request 2). The tenth was this round's — the locked label of
  station 6 quoted in a `_pilot.css` comment (`apps/ecosystem/tests/test_compliance.py::test_prescribed_texts_are_never_
  hand_copied…`): the comments now name it in words; re-run with every CSS-reading guard after the last edits: **603
  passed, 1 failed** (S's `test_every_horizontal_shift_has_its_rtl_twin`, `_sec-tracciato.css`, unchanged).
- Browser, the lane's module and lane M's campus probe: **31 passed** (after two fixes found by the first run: the family
  frames' phone `sizes` follow the narrower trunk indent — `pathways.services.FAMILY_SIZES_V2` 100vw − 5.5 / 5 rem —,
  and the hidden legend's box zeroed).
- Browser, the older modules that read P1's pages — `apps/ecosystem/tests/test_browser.py` and
  `tests/frontend/test_browser_w3_f1.py`: **41 passed** (both were red since the build on V5.4 selectors, §R4);
  `test_browser_v515_c.py`, `test_orientation_browser_w3_f1.py`, `test_seal_heads_browser_v522_s.py`,
  `test_reduced_motion_w1_d.py`: **27 passed** (one fix: the developing frame read mid-scroll, §R4);
  `test_mobile_rtl_w4_a.py`, `test_content_pages_browser_w3_f2.py`, `tests/i18n/test_rtl_browser.py`,
  `test_header_fits_the_narrowest_viewport.py`: **71 passed** (one fix: Formation's stand-alone link, §R4).
- `ruff check` / `ruff format --check` clean on the lane's Python (the two shared modules that are not format-clean at
  their base are not reformatted); LF everywhere; `npm run build` reproducible (a second build leaves the tree
  unchanged); `main.css` 32 718 B gzip -9, untouched.

**Budgets** (gzip -9, the built tree): `ecosystem/pilot.css` 9 469 / 9 728 · `companies.css` 8 582 / 9 216 ·
`institutions.css` 8 365 / 9 216 · `universities.css` 7 605 / 8 448 · `ecosystem.css` (family) 4 977 / 11 264 ·
`pathways/index.css` 9 719 / 10 240 · `sheet.css` 9 676 / 10 240 · `training.css` 8 744 / 9 728 · `diplomas.css`
8 853 / 9 728 · `pathways.css` 4 716 / 11 264 · `main.css` 32 718 (untouched). JS: no change (the build leaves
`static/js/dist` as it was).

**Headed checks** (`evidence/v522/p1/imp1/`): `sweep/sweep.json` — 11 pages × 8 widths × 4 languages = 352 runs,
reduced motion: 0 overflow, 0 text outside the viewport, 0 script error; `axe/` — axe-core 4.13 (WCAG 2.0–2.2 A/AA)
on the pilot, Parcours, a sheet, Entreprises, Universités and Formation at 1440 and 390 in fr and ar: 0 violations;
`axe/keys2.json` — the keyboard walk (Parcours 390 fr/ar, a sheet 1440): no focus under the bar or the letterhead, the
rail's links reachable; `full/` — reduced-motion stills of nine pages fr/ar at 1440/390; `p1`–`p3`, `q` the pilot
(motion and still; labels' measures in `p1/probe.json`, `p2/probe.json`), `pa1` Parcours's phone choice, `ps1` the
rail, `f1` Formation, Universités, EN-4, `interim` the G3-closed strip, `form`/`form_base` the preserved form against
the base.

### R6. Requests to other lanes (round 1)

7 (restated, with the rule) — **lane S, `_fronte.css`**: the collaboration head's hemicycle note
(`ecosystem/partials/emiciclo_nota.html`, unchanged markup) needs its layout where the form pages read their sheets:
`.emiciclo-nota { display: grid; grid-template-columns: auto minmax(0, 1fr); align-items: start; gap: var(--s-4); }`
`.emiciclo-nota__disegno { inline-size: 96px; block-size: auto; color: var(--accent-mark); }`
`.emiciclo-nota__frase { max-inline-size: var(--measure-small); margin: 0; font-size: var(--t-ui); line-height: 1.5;
color: var(--text-2); }` — the drawing beside the sentence, the sentence a side annotation (§3.7 IN-H, QA_ROUND1 m4).
11 — **lane S, the section runtime**: a chosen lane of a route board should come into view on a phone when the choice
is made deep in another lane (`.tracciato--scelta` below 48 rem: on `change`, the chosen `[data-lane]` scrolled to its
top under the bar — `scroll-margin` is set —, instant under reduced motion and from the keyboard). P1 folds the other
lanes in CSS (QA_ROUND1 M3's accepted alternative), which serves a choice made at the board's top.
12 — **lane S / the reviewer**: Playwright's full-page capture flips the width queries for an instant and replays every
width-keyed entrance (R2); S's fixtures and the QA tools may want viewport captures for motion.

## Round 2 improvements (label v522-p1-improve2)

Answers `evidence/v522/p1/QA_ROUND2.md` (2 major, 9 minor; Parcours interaction 3.5, the institutions' collaboration
head 3.5 / 3.5, the composition and imagery targets of Parcours and Entreprises at 4 against 4.5). Branch `v522-p1`,
worktree `C:/tmp/ile_wt/v522-p1`, on design-v5 `22b0ddd` (unchanged since the build: nothing to merge). Lane server
8786 (DB l6, reference date 3 Oct; restarted after each template or Python change — `--noreload`). Headed chromium-1234
for every check. Tools: `C:/tmp/ile_v5_council/.work/v522-p1-improve2/` (`tools/deep.py` the choice made deep in the
board, `keys_board.py` the arrows through the families, `final_probe.py` stills, no-JS and the Tab / Shift+Tab walk,
`leading_probe.py`, `sweep.py`, `axe_keys.py`, `probe.py` with `specs/*.json`, `exp/` the alignment experiments, the
`patch_*.py` edits, `with_lock.sh`); evidence `C:/tmp/ile_v5_council/evidence/v522/p1/imp2/`. Lock sessions
(`logs/locks.log`, 2 November, each released, none over 9 min, no takeover): A 04:15, A 04:18–04:19, B 04:19–04:20,
A 04:26–04:27, B 04:39–04:40, B 04:40, B 04:41, A 04:47–04:48, A 04:48–04:49, A 04:50, A 04:53, B 05:01, B 05:04,
B 05:06–05:09, B 05:09–05:15, B 05:15–05:19, A 05:19–05:27, A 05:33–05:34, A 05:35–05:40, A 05:40–05:41,
A 05:42–05:45, A 05:45–05:47, A 05:54–05:57, A 05:57–05:58, A 05:58–05:59, B 05:59–06:00, B 06:01, B 06:02–06:03,
B 06:03–06:04, B 06:05, A 06:26–06:28, A 06:29–06:34, A 06:34–06:38, A 06:38–06:45.
**One breach, recorded:** at 05:45 a browser run was started on the lane's test database while the non-browser run was
still using it (one pytest per database lane); both deadlocked. Both were stopped (two orphaned python processes ended
by hand), then run again one after the other; the results below are those of the clean runs.

### R1. What changed, finding by finding

**M1 — Parcours: a choice made anywhere in the board brings its lane under the bar.** Request 11 (lane S's runtime)
is no longer needed: the browser's own focus does it, with no script (`pathways/_tracciato.html`, `_index.css`).
- *The board is the families' group.* The route board is a `fieldset` whose legend names the five native radios. «Tous»
  stays in its chip; **each family's radio stands at its own lane's head**, and its chip is its `<label for>`. A tap on a
  chip — anywhere in the board, the bar being sticky — checks the radio and moves the focus to it, and the browser
  scrolls it into view. The arrows do the same from the keyboard (one tab stop, Arrows/Home/End as any radio group).
- *Nothing leaves the layout* (§0.1, §2 B, §3.4): round 1's phone fold is gone — it was the deviation that stranded a
  reader. The chosen lane takes its full ink, its frame develops, the light runs its rail (the library's
  `--lane-lit`); the other lanes take the quiet ink, never an opacity; the count is read in the bar.
- *Where the lane lands.* Chrome centres a focused element that was out of sight and aligns the nearer edge of one that
  was partly in sight (measured: `exp/align*.py`). So on this page html's scroll-padding takes the bar's reach as well
  as the letterhead's (`html:has(.percorsi-tracciato)`, page sheet only), and the radio's box starts at its lane's top
  and is exactly as tall as the reading area: in both modes the lane's top lands right under the bar. Measured
  (`deep3`, wheel then tap, fr and ar): 300 / 900 / 1 500 / 2 200 px into the board → the lane at 157 px under a bar
  ending at 140 (390 and 360), at 132–134 under a bar ending at 116 (1 280, 1 440); the board's height unchanged
  (2 387 / 1 125 px), the eight stations drawn, the count in the bar. Without script the same (`final/nojs_*`:
  157 / 140, fr and ar). From the keyboard the move is instant (html's `scroll-behavior` under `data-input="key"`) and
  the focused control never sits under the bar (`keys3`: the focus box from 157/158 px at 390, 134 at 1 440); the Tab
  and Shift+Tab walk through the board puts no focus under the bar at 1 440 (fr, ar) or 390 (`final/final.json`).
  The ring shows on the chip and on the lane's name (the radio itself is invisible).
- *The bar* is one sticky bar at every width now (from 64 rem on one row, the count at its end), so the choice and its
  result are read together on a desktop too.

**M2 — the institutions' collaboration head: one annotation.** Request 7 (lane S's `_fronte.css`) is no longer needed:
the note is recomposed with what the form pages already load (`ecosystem/partials/emiciclo_nota.html`; the form pages
still add `fronte.css` and nothing else). The box under the lead takes the band's `.ingresso__lead` (its margin and
measure, so the note hangs from the lead's reading edge); inside it one row that never wraps (main.css
`.meta-row__item`), the hemicycle drawing — now on its sill — in a seat that never shrinks (main.css `.chip__meter`:
`flex: none`; a bare SVG gives way, main.css capping every SVG at its box), and the locked sentence in main.css's
secondary text (`.card__text`: 15/24, the quiet ink, the small measure — §6.2's side annotation). The prescribed
introduction now carries its language (`lead_lang`, `templates/enquiries/collaboration_proposal.html`, header block
only), so in Arabic the lead and the note are two French boxes hanging from the same right edge. Measured
(`look3`, `collab2`): the drawing 108 × 54 beside the sentence at 1 440 and at 390 (it no longer stacks above it), the
sentence 15/24 against the lead's 22; in Arabic the lead's box and the note's box both 724–1 332 px, the drawing on the
right; the head 477 px at 1 440 with the formwork at 581 px — in the first screen; at 390 the head 647 px, the form at
768 (one screen).

**m1 — Universités: the destination from the second plate's line.** The three plates stand on the route's own rows (a
subgrid), so the campus frame stands from the second plate beside the second and third, the last plate still laid
over its edge (`_universities.css`). Measured: frame top = second plate top (1 296 / 1 296), the last plate over the
frame's edge; the empty quadrant is now the strip beside the first plate. The frame's width — and its `sizes` — are
unchanged (lane M's campus test: green).

**m2 — French runs in Arabic keep the Latin leading.** The Parcours cards' title and line (`1.75rem`, as on the French
page), and — found by a probe of every French run in P1's Arabic sections (`leading_probe.py`) — Formation's second
time body and Diplômes' definitions, which took the Arabic 32 px at 17 px. Also fixed on the way: in an Arabic card on a
phone the arrow touched a French title's first letter (`←Études`): the title's room is now on its own start.

**Found on the way — the Arabic light ran left to right.** Round 1's right-to-left light (`sez-run-rtl`) was keyed
`:root… [dir="rtl"] .percorsi-tracciato …`, a `[dir]` *under* the root, while the page's direction is the root's own
attribute: it matched nothing, so in Arabic the light crossed the chosen lane's rail from left to right. Now
`:root[dir="rtl"]…`; measured with motion allowed (`motion_probe.py`): a choice runs `sez-run` in French and
`sez-run-rtl` in Arabic, the frame develops (grayscale 1 → none), and nothing is running 2.2 s later.

**m3 — the phone bar's chips** scroll inside the bar with no scrollbar drawn; their far edge fades into the bar's ground
(a shadow in the ground's own token — no gradient in an app sheet), and the row keeps 32 px of air at its end so the last
chip scrolls clear of the fade.

**m4 — the pilot's doors at 768:** the calls start on one line, right under their words (`align-self: start`; the words
hold two lines in both doors). Measured: tops 2 286 / 2 286 (fr 768), 2 303 / 2 303 (ar 768), equal at it 1 024 and
en 1 280. (A shared subgrid was tried first: the arch's percentage crown padding broke it — the disc overprinted the
words at 768; reverted.)

**m5 — one rule under the doors:** the help line stands on the doors' sill, its own hairline gone (measured: border 0,
the line 24 px under the sill).

**m6 — the deep case in the tests:** see R4.

**m9 and the composition and imagery targets.**
- *Parcours — the fork.* The two one-station lanes (Famille, Autres voies) share the board's last row from 48 rem
  (`pathways.services.route_board`: `fork`, per-lane `frame_sizes`): from 64 rem on the rows' own columns — the first
  a head and one card, the second a frame one card wide and its card, its rail continuing the first's — so the board is
  one 4-column grid with no row two-thirds empty; from 48 to 64 rem the pair side by side, each frame strip over its
  card, and the three-station lanes three-up (two-up left a lone card beside an empty half at 768). The board went from
  about 1 800 to 1 125 px at 1 440.
- *Parcours — the lanes' names on their frames* at every width (a plate at the frame's top corner, as a phone had it):
  the name and the picture read as one head, and the frames align with the cards' tops.
- *Entreprises EN-1 — statement → process.* Each moment opens on its ILE Mono numeral at 36 (§2 F's anatomy, the three
  moments' own order: never a rank), its text at 17/28; from 80 rem the process's caption stands beside the quotation,
  on its last line, the route under both — the head is no longer a second block stacked under the first, and the right
  third of the band is no longer empty. In Arabic it mirrors (the French quotation keeps its rule at its own start).

### R2. Not done, and why

- **m7** (the catalogue and lane S's guards) is not P1's: the steward carries `p1/catalogue/*.po` at merge; the U1
  kickers stay French on it/en/ar until then. This round adds **no** msgid (no new user-facing string).
- **m8** (Diplômes on a phone: one definition open at a time) stays deviation 3, for the Director.
- **The collaboration head's coherence with its form's own tile** (the head's `ile-istituzione` seal, the preserved
  form head's Lucide building tile; `ile-sapere` and the cap tile on the universities' page): the form section is
  preserved (§9.8) — not touched.

### R3. Self-scores (§26, at 1 440 and 390, fr and ar)

| Page | Comp. | Motion | Imagery | Interaction | Institutional | Coherence |
|---|---|---|---|---|---|---|
| Parcours | 4.5 (the fork, the named frames) | 4 | 4.5 | 4.5 (a choice brings its lane, everywhere) | 4.5 | 4.5 |
| Collaboration — institutions (head) | 4 | 4 | 4 | n/a (form) | 4.5 | 4.5 |
| Collaboration — universités (head) | 4 | 4 | 4 | n/a (form) | 4.5 | 4.5 (the lead's language) |
| Entreprises | 4.5 (EN-1) | 4 | 4.5 | 4 | 4.5 | 4.5 |
| Universités et formation | 4.5 (m1) | 4 | 4 | 4 | 4.5 | 4.5 (m7 aside) |
| Projet pilote | 4 | 4 | 4 | 4 (m4, m5) | 4.5 | 4.5 |
| Pathway sheets, Formation, Diplômes, Institutions, Recueil | unchanged, or the m2 leading only | | | | | |

### R4. Tests

**Changed under V5.20's strict rule** (each old expectation conflicts with SECTION_SYSTEM_V2's approved composition —
§0.1, §2 B and §3.4 «nothing leaves the layout», «the existing radios choose a lane» — or with QA_ROUND2's finding; the
new behaviour intended; the same invariant or a stronger one):
- `tests/frontend/test_pages_browser_v522_p1.py::test_on_a_phone_the_family_choice_is_one_bar_and_brings_its_lane_under_it`
  — the old assertion was round 1's fold («only the chosen family's stations are drawn»), the very behaviour that
  stranded a reader, and it chose only at the board's top. Now, in fr and ar, with a touch context: the bar sticky on its
  own ground, holding the chips and the polite count, the legend clipped but naming the fieldset of five radios; then
  five choices after a **wheel** scroll to the board's top, 900 px and 1 500 px into it (QA_ROUND2 m6): each time the
  chosen lane right under the bar (`barBottom ≤ laneTop ≤ barBottom + 40`), the bar in view, the board's height and its
  eight stations unchanged, the chosen family's count in the bar; «Tous» lights every lane again. Stronger.
- `…::test_choosing_a_family_keeps_every_station_and_lights_its_lane` — the selector named a radio inside the chip
  (`label:has(input[value=work])`); now the chip `[for]`. Same invariants (eight stations, the quiet ink never an
  opacity, «3 parcours affichés»), plus the lane under the bar on a desktop, the board's height unchanged, and the far
  end («Autres voies» chosen from the board's top). Stronger.
- `…::test_an_arabic_page_keeps_its_french_titles_on_their_marker_s_edge` — adds m2: the sixteen French runs of the
  Arabic cards at the French page's 28 px leading.
- `tests/frontend/test_pages_v522_p1.py::test_the_route_board_holds_the_eight_pathways_on_their_family_lanes` — the old
  assertions (five radios inside the bar's fieldset; one `sizes` for four frames) conflict with the recomposition (the
  radios at the lanes' heads; the fork's frames drawn at the fork's widths). Now: the board is a fieldset, its legend
  first; the five radios in order, «Tous» checked in its chip, each family's the first element of its lane, each chip
  its label with the lane's name; the polite count in the bar; each frame's `sizes` its lane's (the head's for the
  three-station lanes, `FAMILY_SIZES_FORK_START/END` for the pair — the browser test measures every one at six widths
  in fr and ar); the pair's lanes marked `--start` and `--end`. Same invariants or stronger.
- `…::test_the_form_pages_open_on_their_space_s_compact_band_and_keep_their_form` — adds M2: the drawing and the
  sentence in one row, the drawing first, the sentence not a lead; in Arabic the lead and the note both `lang="fr"`.

**New** (lane P1's browser module): `test_the_institutions_head_sets_its_recipients_as_one_annotation_beside_the_hemicycle`
(fr, ar; 1 440 and 390: the drawing ≥ 96 px beside the sentence, at the reading edge, the sentence ≤ 15.5 px under the
lead's size; in Arabic two LTR boxes on one right edge; the formwork in the first screen at 1 440);
`test_the_pilot_doors_calls_start_on_one_line_and_the_sill_is_their_only_rule` (fr/ar 768, it 1 024, fr 1 440);
`test_the_campus_frame_stands_from_the_second_plate_and_the_last_plate_lies_over_it` (fr, ar);
`test_the_companies_three_moments_open_on_their_numerals`.

### R5. Runs, budgets, evidence

**Runs** (lane DB `test_ile_v5_l6`, one pytest at a time after the breach above):
- Browser, the lane's module: **25 passed** (19 kept, 6 new; the first run after the breach met the killed run's seed
  rows in its first test, which passed alone at once), and **25 passed** again after the round's last three CSS changes
  (the page's scroll-padding, the Formation and Diplômes leading, the Arabic light).
- Browser, the other modules that read these pages: `apps/ecosystem/tests/test_browser.py`,
  `test_browser_w3_f1.py`, `test_imagery_v522_m.py` **58 passed**; `test_browser_v515_c.py`,
  `test_orientation_browser_w3_f1.py`, `test_seal_heads_browser_v522_s.py`, `test_reduced_motion_w1_d.py`,
  `test_journey_browser_w3_d.py` **39 passed**; `test_mobile_rtl_w4_a.py`, `test_content_pages_browser_w3_f2.py`,
  `tests/i18n/test_rtl_browser.py`, `test_header_fits_the_narrowest_viewport.py`, `test_forms_v515_b.py` **74 passed** —
  each group run once more after the last CSS changes: 58, 39 and 74 passed.
- Non-browser, targeted (`tools/run_nonbrowser.sh`: round 1's list plus the chip and component guards and the
  locked-split equality tests): **2 403 passed, 9 failed** (27 min 41 s). The nine are the build's declared nine,
  unchanged (§5 of the build notes; QA_ROUND1 and QA_ROUND2 m7): the five msgids' catalogue cases until the steward
  carries `p1/catalogue/*.po` (`test_catalogues.py` ×4, `test_page_integrity.py::test_latin_text_on_arabic_pages…` —
  «Voir dans le glossaire», «Destinataires», the three U1 kickers); lane S's three, red on design-v5 since the v522-s
  merge (`test_loader_rules.py::test_l3…`, `test_state_chips…::test_data_register…`, `test_rtl_static.py::test_every_
  horizontal_shift…` — `_sec-tracciato.css` only); the tag guard of request 2. None names a rule of this round.
- `ruff check` / `ruff format --check` clean on the lane's Python; LF everywhere; `npm run build` reproducible;
  `main.css` 32 718 B gzip -9, untouched.

**Budgets** (gzip -9, the built tree): `pathways/index.css` 10 095 / 10 240 · `training.css` 8 759 / 9 728 ·
`diplomas.css` 8 866 / 9 728 · `sheet.css` 9 676 / 10 240 · `ecosystem/pilot.css` 9 487 / 9 728 · `companies.css`
8 682 / 9 216 · `institutions.css` 8 365 / 9 216 · `universities.css` 7 614 / 8 448 · the family sheets unchanged ·
`main.css` 32 718 (untouched). No JS, no image, no request added; the form pages still add `fronte.css` only.

**Headed checks** (`evidence/v522/p1/imp2/`): `sweep/sweep.json` — 12 pages (the eleven of round 1 and the universities'
collaboration head) × 8 widths × 4 languages = 384 runs under reduced motion: 0 overflow, 0 text outside the viewport,
0 script error; `axe/axe_keys.json` — axe-core 4.13 on the pilot, Parcours, Entreprises, Universités and the two
collaboration heads at 1 440 and 390 in fr and ar: 0 violations (24 runs); `deep1`–`deep3` the choice made deep in the
board; `keys/` and `logs/keys*.log` the arrows; `final/` stills of the six recomposed sections (fr, ar, 1 440, 390),
the no-JS choice and the walk; `board1` the board at 1 920 / 1 440 / 1 280 / 1 024 / 768 / 390; `look*`, `collab*`.

### R6. Requests to other lanes (round 2)

- **Lane S — requests 7 and 11 withdrawn**: P1's own compositions now do both (R1 M1, M2).
- **Lane S — new, 13 (for S-close or the library):** the hemicycle note borrows three main.css classes for their layout
  (`.meta-row__item`, `.chip__meter`, `.card__text`). If one of them changes its look, the note changes with it; a
  dedicated `.emiciclo-nota` rule in `_fronte.css` (request 7's text) would let P1 switch back to its own names.
- **Lane S — new, 14:** a library rule for French runs in right-to-left sections (`[dir="rtl"] .sez [lang="fr"]`: the
  Latin leading) would cover every lane's French runs at once; P1 sets it in its own sheets for the three it measured.
- **Lane S / the steward — for awareness:** on /parcours/ only, P1's page sheet extends html's `scroll-padding-block-start`
  by the sticky bar's reach (`html:has(.percorsi-tracciato)`; v5/chrome.css keeps the letterhead's elsewhere).
- **The steward:** carry `p1/catalogue/*.po` (round 1's five msgids) in P1's merge commit, as before; this round adds none.
