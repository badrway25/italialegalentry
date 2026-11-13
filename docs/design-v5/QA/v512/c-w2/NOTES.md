# V5.12 · Lane C · W2: imagery pipeline and the compositions of five pages + the Forum (label v512-c-w2)

Branch `v512-c-w2`, cut from design-v5 `6251475` (v512 W1 merged).

**Scope** (DECISIONS «Waves», W2 row for C, and §12 for C):
- the imagery pipeline (§6): builder, slot registry, partial, page-only sheet, provenance, test;
- the slots of the home, `/institutions/`, `/universites-et-formation/`, `/entreprises/`, `/parcours/`;
- the §7 compositions of those five pages and of `/forum/`;
- Q1 (owner answer A): the hero's H1 is the visible name, and the name appears once;
- Q2: the search for Allegato 1 (recorded below); the 404 of the unpublished legal pages is a request to lane P;
- Q4 / Q6: Forum without stock and without a Virtual-Forum pointer (checked).

**Discrepancy recorded.** The task text says «Q1–Q8 are NOT answered: apply the Director's default (Q1 hero frozen)».
DECISIONS §12 records the owner's binding answers of 28 Oct 11:35 (directive `V5_13_OWNER_DECISIONS_Q1_Q8.md`),
which assign Q1 to lane C in W2 and unfreeze the hero templates and `hero.css` for that change only. I followed §12.
If the orchestrator wants the default instead, the Q1 change is confined to `templates/pages/home/_hero.html`, the
statement block of `apps/pages/static/pages/css/hero.css` and three assertions of `apps/pages/tests/test_home.py`.

## What changed

### The imagery pipeline (DECISIONS §6)

| Piece | What it does |
|---|---|
| `tools/build_derivatives.py` | Recipes (Pexels id, crop per ratio, redactions, extra desaturation) → crop → redact → the one V5 grade → Lanczos → unsharp → AVIF + WebP at 480/800/1200/1600, never upscaled, metadata and ICC stripped. It steps the quality down until each budgeted file fits (LCP 60 KB, body 45 KB, band 60 KB). It writes `static/img/v5/<family>/` and `PROVENANCE.json` (author, Pexels page, crops in px and fractions, redactions, bytes, sha256). `--check` verifies the hashes. The originals stay outside the repository. |
| `apps/pages/imagery.py` | The static slot registry: key, family, slug, wide ratio, narrow ratio (art direction below 64 rem), French alt msgid, role (lcp/body/band), `sizes`, diptych pair, treatment. `picture(key)` builds the AVIF/WebP sources from the provenance. |
| `apps/pages/templatetags/pages_imagery.py` + `templates/components/photo.html` | `{% photo "<key>" "<class>" %}`: `<figure><picture>` with AVIF then WebP, wide then narrow, explicit width and height, `fetchpriority=high` on the landing's one LCP image, `loading=lazy decoding=async` elsewhere; the figcaption is the credit only («Photo : author / Pexels»), never a place, date or event. |
| `static/css/v5/_photo.css` | A **partial** (the build makes only partials of `static/css/v5/`; DECISIONS names it `photo.css`): imported by the three page sheets that draw photographs (`ecosystem.css`, `pathways.css`, `pages.css`), never by `main.css`. The figure, the credit, the 7 / 5 entrance with the photograph in the end seat (the photograph above the words on a phone), and «develop»: black-and-white → colour as the frame enters the view, a scroll-driven animation (`animation-timeline: view()`), only under `prefers-reduced-motion: no-preference` and only where supported; otherwise colour from the start. |
| `templates/pages/partials/_ingresso.html` | A `slot` branch: the photograph takes the end seat and the door's way in moves under the lead, on the paper (the existing `.ingresso__way` design). |

**The eight frames** (all Pexels; register rows in `docs/IMAGE_LICENSES.md` §3.1; placements and the §6 check outcomes in `docs/design-v5/ASSET_USAGE_MATRIX.md` §9):

| Slot | Frame | Where |
|---|---|---|
| `home.pilot.cedar` + `home.pilot.marble` | 30563520 (M. Idrissi) + 6713855 (T. Miroshnichenko) | home «Projet pilote»: the diptych «le même geste», develops as the band enters |
| `home.ecosystem` | 33543226 (E. Gokceoglu) | home «Un écosystème institutionnel», beside the promoter |
| `pathways.hero` | 7594198 (M. Nilov) | `/parcours/`, LCP |
| `companies.hero` | 7180823 (Thirdman) | `/entreprises/`, LCP |
| `institutions.hero` | 6949366 (W. Pfennig) | `/institutions/`, LCP |
| `universities.hero` + `universities.exchange` | 9489906 (Y. Shuraev) + 31367507 (Y. Çelik) | `/universites-et-formation/`, LCP + body |

**Deviations from the pre-screened plan, after the full-resolution check:**
- **31367507** shows three identifiable students. O55 stays (C12), so the crop keeps only the hands, a book and a folder. The book covers and the folder's lines are blurred.
- **9489906**: the two readers are identifiable at 1600 px, and the spiral stair is O54. The crop is the reading room's end bay, with nobody in it.
- **7180823**: 3:2 only. The face is cropped out under the chin. A 4:5 crop lost either the hand or the piece. The caliper's marking is blurred, and the red is −15 % saturation.
- 31367507's original was not in the research cache. It was fetched once (the API call for the author, the CDN for the file) into `C:/tmp/ile_v5_council/.work/v512-c-w2/originals/`. The key was read from the environment and never printed or written.

### The compositions (DECISIONS §7)

| Page | Composition now |
|---|---|
| `/institutions/` | Split entrance: label, h1 and lead, with the way in (sentence + the prescribed button) under them, beside the council-table photograph (4:5; 3:2 above the words on a phone). Then «Destinataires»: the prescribed sentence as the page's editorial statement, at band size with the accent rule at the reading edge. Then «Pour aller plus loin» as weighted tiles: the Forum on the night tile, the pilot on the paper tile. |
| `/universites-et-formation/` | 7 / 5 entrance with the reading-room photograph and the way in under the lead. Then a «lo scambio» section: the campus photograph beside «Pour aller plus loin» (Formation on the night tile, Parcours on the paper tile) and the help line. |
| `/entreprises/` | Workshop photograph in the entrance (3:2), with the way in under the lead. «Trois temps»: the prescribed quotation as a pull-quote (band size, accent rule) over the existing three-station linea. «Recueil des besoins»: the form beside a side-anchored panel (the chapter head, the request's sentence, where requests go), sticky from 64 rem. «Pour aller plus loin» as tiles. The form itself is lane B's and is untouched. |
| `/parcours/` | Person-at-the-window photograph in the entrance, with the questionnaire's way in under the lead. The eight pathways as a numbered two-column index (large accent numerals 01–08) with a families filter: Tous / Travail / Études et formation / Famille / Autres voies. The filter is radio chips read by CSS `:has()`, with no script; without `:has()` all eight stay listed; the rows fade in under no-preference. «Comment ça marche» stays on the linea. |
| `/forum/` | Three movements, no stock image (Q4). (1) The identity hero with its dateline (unchanged), then «Qui sommes-nous» and «Pourquoi» as one editorial pair, split by a hairline. (2) «Qu'est-ce que le Forum / Objectifs / À qui» as one spread on the stone: 5/4/3 columns on hairlines from 80 rem; 1 + 2 from 64 rem; stacked on a phone. (3) «Participer et collaborer» on the night band, its actions on a hairline plate. Anchors and the page index are unchanged. |
| Home | Above the fold, only Q1 changed (below). The pilot band now has the diptych beside the statement, the second half a step lower. The ecosystem section has the working-table photograph beside the promoter (5fr / 7fr from 64 rem). No new box, no new text. |

**Not done, on purpose:**
- The recipients sentence (institutions) and the seven terms of the universities lead are each **one locked sentence per language**. They are not cut into a numbered index or chips.
- W3-F1's review m4 read such fragments as «a list with typos».
- The standing rule says locked copy is never reworded, and the Arabic and Italian sentences do not split on the same commas.
- Their composition is carried by type, the photograph and the tiles instead.
- The Forum's objectives sentence is kept whole for the same reason; it is not split on «;».

### Q1: the visible H1, one name on the screen

- `_hero.html`: the h1 is the name «ITALY LEGAL ENTRY™». It is visible: the wordmark face, navy, tracked as the lock-up, `translate="no" lang="en" dir="ltr"`. The promise is a `<p class="he__promise">` under it, verbatim.
- `hero.css`: on the home only, `.page-home .site-header .lock__text { display: none; }`. The header keeps the brand mark; its link keeps its accessible name («Italy Legal Entry™ — accueil»). This removes the second name stacked above the H1.
- In Arabic the Latin name ends on the wall's start edge, as the promise does.
- The interim variant (G3 closed) is unchanged.

### Q2: the search for Allegato 1 (recorded as the owner asked)

- **Repository:** `git grep` for «Allegato 1» matches only references to its absence: models, gates, docs, the locked registry. There is no Italian legal text.
- **Supplied documents in `C:/tmp`:**
  - `ILE_Annexe_1_Textes_Juridiques_FR.txt/.pdf` is the **French courtesy translation** (Avv. Badrane, 14 Sept 2026). Its own first page says «la version italienne (Allegato 1) fait seule foi».
  - None of `ILE_Document_Implementation_FR.txt`, the Master Dossier, the AGAMI package or `Modifiche sito AGAMI` contains the Italian Allegato 1.
  - `wf1_allegato_meta.json` is unrelated (an automation export).
- **Result:** no verified Italian source. The C/D legal pages stay unpublished, and nothing is drafted or translated.
- Making them unreachable (404) is in `apps/legal`, which lane P is changing now. See the requests below.

## What the owner sees (8780, after the merge)

| URL | What is new |
|---|---|
| `/fr/` | The H1 «ITALY LEGAL ENTRY™» is visible above the promise, and the header shows the mark alone. Lower down: the pilot band's two hands (cedar and marble) go from black-and-white to colour as they scroll in, and the ecosystem section has the working-table photograph. |
| `/fr/institutions/` | The council-table photograph beside the title. The recipients sentence is set as a large statement. Two weighted tiles: the Forum on night, the pilot on paper. |
| `/fr/universites-et-formation/` | The reading-room photograph beside the title. The campus «hands and books» photograph beside the two tiles. |
| `/fr/entreprises/` | The workshop photograph. The pull-quote. The form with its sticky side panel. Tiles at the foot. |
| `/fr/parcours/` | The person-at-the-window photograph. The numbered index with the five filter chips; try «Famille» or «Travail». |
| `/fr/forum/` | The pair, the three-column spread, and the night «Participer» band. |
| Every page in `/ar/` | The same compositions, mirrored. The photographs are never flipped. |

## Checks on lane server 8785

Lane server setup: l5 database, dev settings, `ILE_DESIGN_PREVIEW=1`, `ILE_REFERENCE_DATE=2026-10-03`.

- **Screenshots:** the six pages in fr and ar, at 1440 and at 390. The 390 pass ran with `reduced_motion=reduce`. The Chromium lock was taken and released for each run.
- **Horizontal scroll:** none on any page at either width; the script reports overflow and printed nothing.
- **Shots and scripts:** outside the repository, in `C:/tmp/ile_v5_council/.work/v512-c-w2/` (`before/`, `r1/`, `r2/`, `shots.py`, `probe.py`, `look/` for the crop sheets).
- **Fix found by probing:** the RTL text-align of the hero name lost to a stronger rule. It is now `[dir="rtl"] .he .he__title > .he__name { text-align: end; }`, measured `end`.
- **Fix found in the screenshots:** a chapter head nested inside a composed column took `.chapter__head`'s grid placement (1 / span 4, sticky) and broke the column into implicit tracks. The columns now reset it in `_spaces.css` and `_forum.css`.

## Budgets

| Item | Before → after |
|---|---|
| `main.css` (shared) | unchanged (0 B; byte-identical dist) |
| `ecosystem.css` (page-only, gzip -9) | 3 467 → 4 355 B |
| `pathways.css` | 3 661 → 4 422 B |
| `pages.css` (home) | 3 782 → 4 276 B |
| `hero.css` | 10 568 → 10 695 B |
| `forum.css` | 3 097 → 3 390 B |
| JS | none added |
| LCP files, 1440 px at 1x (480w AVIF) | 6–14 KB |
| LCP files, 390 px at 3x (3:2 1200w AVIF) | 17–28 KB (budget 60 KB) |
| Body files | ≤ 45 KB at every budgeted width (the test holds it) |
| Home images below the fold, lazy | three frames at ≈ 13–20 KB each at 1x |
| `static/img/v5/` | 88 files, 2.8 MB on disk; the largest is `bibliotheque-salle-lecture-4x5-1600.webp`, 125 KB, picked only by a 2x+ wide screen |

CLS: every `<img>` carries width and height and its `<source>`s carry theirs; the art-directed ratio changes only at the 64 rem media boundary. Mobile LCP was not measured under throttling here: the LCP files are 17–28 KB, and the reviewer's Lighthouse pass should confirm < 2.5 s on `/institutions/` and `/parcours/`.

## Tests

All runs used database lane l5 (`TEST_DATABASE_URL=…/test_ile_v5_l5`), one pytest process at a time, `-m "not browser"`.

**New:**
- `tests/compliance/test_imagery_v512.py`, 13 tests: licence and author; forbidden vocabulary in slugs and alts; the file-name ban; **one frame = one slot across the site, the hero and portico families included**; pair symmetry; hashes; weight budgets; both formats and explicit dimensions; each landing draws exactly one `fetchpriority=high` image and only lazy others; the home's three frames are lazy, and the diptych alone develops.
- `apps/pages/tests/test_home.py::test_the_home_shows_the_name_once`.

**Brought to the decisions (each superseded rule now asserts the new one, never nothing):**
- `test_home.py`:
  - the hero h1 tests assert the visible name and the promise `<p>`, and that the name is not visually hidden;
  - `test_ecosystem_shows_the_promoter_alone…` allows exactly one image, the `home.ecosystem` slot, and still no logo;
  - `test_black_and_white_rests_only_in_the_hero` admits only the three home slots under the hero, `develop` only on the diptych, the reduced-motion guard in `_photo.css`, and still no filter in `pages.css`.
- `tests/compliance/test_figure_caption.py`: docstring note only. Its count (no `<figure>` without `<figcaption>`) holds, because every V5 frame carries its credit caption.

**Steward:** the full-page screenshots show the diptych in black and white because they are taken at scroll 0, where the frame is out of view. In the browser it takes its colour as the band scrolls in, and keeps it once it has passed.

**Also brought to the decisions:**
- `tests/frontend/test_interior_w3_f1.py`:
  - the night door card on the four landings becomes `test_a_door_s_entrance_carries_its_photograph_and_its_way_in`: the slot photograph in the end seat, eager and credited; the way in under the lead with its text and its one control; the page's one primary is that control, as W3-F1's M1 asked;
  - the person's questionnaire test reads the way in;
  - `_photo.css` was added to the two page sheets' import lists.
- `apps/ecosystem/tests/test_compliance.py`:
  - `_photo.css` in the import list;
  - «nothing moves» is now «the spaces' sheet animates nothing and switches its transitions off under reduce; `_photo.css` has one keyframes, behind no-preference».
- `apps/ecosystem/tests/test_companies_page.py`: without a curated asset the page shows the `companies.hero` slot and the way under the lead; the pull-quote class is accepted.
- `apps/ecosystem/tests/test_gated_pages.py`: the recipients sentence, still verbatim, now carries `destinataires__statement`.
- `tests/frontend/test_cms_nav.py::test_portico_gives_every_door_its_panel_from_live_content`:
  - It was **already failing on the base** (6251475): the W1 hide gate takes «Actualités» out of the «Projet» panel, and the test still listed it.
  - It now asserts the four rows, with the reason.
- A curated, captioned back-office photograph (`MediaAsset`) **keeps precedence** over a slot in `_ingresso.html`: documentary over stock. This keeps the W3-F1 tests of the curated path.
- `_hero.html`'s comment no longer quotes the prescribed name (`test_templates_never_hand_copy_prescribed_texts`).

**Runs:**

| Run | Result |
|---|---|
| Broad targeted run, before the last fixes | 1 281 passed, 22 failed. 18 were the stale tests above (now fixed). 4 fail **identically on the base** 6251475, run in `C:/tmp/ile_wt/design-v5`: `test_cms_nav` portico (fixed here, above), `test_service_pages_w3_f2::test_400_and_500…[400]` and `[500]`, and `test_mobile_rtl_w4_a::test_the_500_keeps_its_semicolon_with_its_words`. The last three concern the standalone error pages: none of this lane's files, so they are not fixed here. |
| Final run, fresh test database (`--create-db`) | **446 passed, 0 failed**. Files: `apps/ecosystem`, `test_interior_w3_f1.py`, `test_cms_nav.py`, `apps/pages/tests/test_templates_static.py`, `apps/pages/tests/test_home.py`, `tests/compliance/test_imagery_v512.py`, `tests/compliance/test_figure_caption.py`, `test_css_bundle_is_current.py`. |

The `test_ile_v5_l5` database had picked up another branch's schema: `legal_legaldocument.seed_checksum`, from lane P. Hence `--create-db`.

**Browser tests** (`-m browser`) were not run, given the one-Chromium rule and the steward's W2 merge pass. These read the changed pages:
- `apps/pages/tests/test_browser.py`: the hero's geometry; `promise` is still `.he__promise`, now a `<p>` under a visible h1 line, so the statement is about 40 px taller;
- `apps/ecosystem/tests/test_browser*`;
- `tests/frontend/test_interior*browser*`.

**Scan** on 8785: `<main>` of the six pages × fr/it/en/ar has 0 occurrences of «en préparation / en cours de vérification / en cours de définition / prochainement / seront publiés» and 0 references to `images.pexels`.

## New msgids (for D)

| msgid | Where |
|---|---|
| «Le même geste» | the diptych's group label, `_pilot.html` |
| «Autres voies» | the pathways filter chip |
| «Une main guide un ciseau à bois dans une sculpture de cèdre aux motifs géométriques» | alt, `imagery.py` |
| «Une main guide un ciseau sur un bloc de marbre» | alt |
| «Autour d’une table de travail, des mains, des documents annotés et des micros de séance» | alt |
| «Une personne vue de dos, assise à son bureau devant une grande fenêtre» | alt |
| «Dans un atelier, des mains mesurent une pièce au pied à coulisse» | alt |
| «Une table de séance vide : micros, écrans éteints et chevalets sans nom» | alt |
| «Une salle de lecture : bibliothèques vitrées, tables de bois et lumière des fenêtres» | alt |
| «Sur un campus, des étudiants échangent, un livre et un classeur à la main» | alt |

Reused, already in the catalogue: «Photo», «Familles de parcours», «Tous», «Travail», «Études et formation», «Famille». On `/ar/` today «Autres voies» shows in French until D's pass. The way-in sentence «Signalez les besoins professionnels de votre entreprise.» in the companies' side panel carries `lang="fr"` while untranslated, as the entrance already does.

No longer used: none.

## Requests to other lanes

- **Lane P (`apps/legal`), Q2.** While a C/D document is unpublished, its route should answer 404 to the public, with the preview/phase console still reaching it. Gate each route on `document_available(kind)`, as lane P's own notes propose, through a per-route `requires_gate` in `apps/legal/apps.py` or in the view. That also takes the five routes out of the sitemap and lets `cms_nav.resolve_url` drop any menu row to them automatically. Lane C did not edit `apps/legal`, because lane P's branch rewrites `views.py` and `services.py` now. If lane P prefers lane C to make the change after its merge, say so and it is a W3 item.
- **Lane D (footer):** per §13, link «Privacy Policy» and «Cookie Policy» only when published, and drop the three C/D links while unpublished (lane P's notes say the same). `footer.html` is D's.
- **Lane A (`COMPONENT_PROVENANCE.md`):** rows for lane C's components, adapted from 21st.dev families as raw material and rebuilt on ILE tokens, with no code imported:
  - «gli approdi» (weighted link tiles: the «feature card / link card» family);
  - the families filter (the «filter chips / segmented tabs» family);
  - the image «develop» reveal (the «scroll reveal / grayscale-to-colour image» family).
- **Lane A (motion):** the «develop» reveal and the filter rows' fade are CSS in lane C's page-only sheets, each behind `prefers-reduced-motion: no-preference`. If A's M-series ships a shared reveal primitive, the diptych can move onto it.
- **Lane B (icons):** the tiles draw only the existing `arrow`. No concept glyph was used for the Forum or the pilot, to avoid borrowing an unrelated symbol. If B adds a Forum glyph (`messages-square`) and a pilot/route glyph in W2, the tiles can take them.
- **Lane D, preview hub:** nothing new to annotate. No route was added or removed.

## Not done in W2 (by the wave plan)

- The remaining §6/§7 pages are W3: orientation band, formation, diplomas, projet-pilote, le-projet, réseau, vivre-en-italie, agami, faq, glossary, fraud, contact, the portico's four dedicated frames, and the platform's «no case yet» crop.
- The licence register has rows for every W2 frame (§3.1) and, new, for the hero and portico Pexels families (§3.2, gap I-5). Completing it for the W3 frames is the W3 item (DECISIONS lane C acceptance 8).

## For the steward (ownership manifest)

**Files this lane created** (whole files):
- `tools/build_derivatives.py`
- `apps/pages/imagery.py`
- `apps/pages/templatetags/pages_imagery.py`
- `templates/components/photo.html`
- `static/css/v5/_photo.css`
- `static/img/v5/**`
- `tests/compliance/test_imagery_v512.py`
- `docs/design-v5/QA/v512/c-w2/NOTES.md`

**Slices** (files this lane changed in place):
- `templates/pages/partials/_ingresso.html`
- `templates/pages/home/{_hero,_pilot,_ecosystem}.html`
- `templates/ecosystem/{institutions,universities,companies}.html`
- `templates/pathways/index.html`
- `templates/forum/partials/{presentation,cta_row}.html`
- `apps/ecosystem/static/ecosystem/{ecosystem,_spaces}.css`
- `apps/pathways/static/pathways/{pathways,_pathways}.css`
- `apps/pages/static/pages/css/{pages,hero}.css` (hero.css: Q1 only)
- `apps/forum/static/forum/_forum.css`
- `docs/IMAGE_LICENSES.md` (§3.1, §3.2)
- `docs/design-v5/ASSET_USAGE_MATRIX.md` (§9)
- the tests listed above.

**Generated:** `static/css/dist/{ecosystem,forum,pathways,pages/css/pages,pages/css/hero}.css`.

## Fixes after review (v512-c-fix-w2)

One finding was raised against this lane, a minor. It was fixed.

**The /parcours/ families filter** (`templates/pathways/index.html`)
- The family map has moved out of the template. Before, the template ran substring tests on `entry.key`. Now there is one tuple, `pathways.services.PATHWAY_FAMILIES`, with a reverse map `FAMILY_OF`. Each `IndexEntry` carries its `family` (the default is `other`), and the template writes `data-family="{{ entry.family }}"`.
- There is now a polite count line, `<p class="famiglie__count" role="status" aria-live="polite">`, under the chips. It holds one sentence per family («N parcours affiché(s)»), and the counts come from `services.family_counts()` in the view. CSS keeps only the checked family's sentence; when no family is chosen, or the browser has no `:has`, the «all» sentence shows (8). The styles are in `_pathways.css` (page-only). `pathways.css` was rebuilt with `npm run build:css`, and only that dist file changed.
- **Gap, recorded:** the filter still runs on CSS alone, with no JS. Whether a screen reader announces a live region whose visible child changes through CSS `display` depends on the browser. Chromium treats it as a content change, but other browsers may not. If a guaranteed announcement is required, it needs a small page script (lane A's call). The count is always readable in the page whether or not it is announced.
- **New msgid, for lane D** (a plural): `%(n)s parcours affiché` / `%(n)s parcours affichés` (in the template it is `{{ n }}`, `blocktranslate count n=…`). The EN/AR wording is provisional under Q3.
- **Test:** `apps/pathways/tests/test_views.py::TestPhase3Index::test_the_families_come_from_the_registry_and_the_count_line_says_each`. It checks that every locked key has a family, that the rows' `data-family` equals `FAMILY_OF`, that the status line is polite, and that the counts are all = 8, work 3, study 3, family 1, other 1.
- **Files** (slices added to the manifest above): `apps/pathways/services.py` and `apps/pathways/views.py` (the family tuple and the counts; this lane already changed them in W1), `apps/pathways/tests/test_views.py`.
