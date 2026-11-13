# V5.15 · Lane C · W3: page headers, art direction per page, imagery pass, section design (label v515-c-build)

Branch `v515-c`, cut from lane C's W2 branch `v512-c-w2` (b7fe066), then design-v5 `ece1eeb` merged in (3861303) — the W2
photographs and compositions (home, institutions, universités, entreprises, parcours, Forum) reach the preview with W3.
Built on W1/W2's systems: lane A's reveal sheet (`v5/_reveal.css`: M1 head hairline, M2 mask, M3 data-grade, M4 marks),
lane B's sprite and concept glyphs, lane C's slot registry and `{% photo %}`.

## 1. Carry-overs of DECISIONS §16 (done first)

| Item | What changed |
|---|---|
| **M-3** (A × C) | `templates/components/photo.html` now carries lane A's contract: `data-reveal="mask"` on the figure of every body frame (never on the eager LCP frame), the `<img>` stays inside `<picture>`, `treatment="develop"` → `data-grade="bw-scroll"`, new `treatment="bw"` → `data-grade="bw"`. C's own `.foto--develop` scroll mechanism and its keyframes are **deleted** from `v5/_photo.css`; html.rm and reduced motion are honoured by lane A's sheet. The owner now sees masked reveals on every body photograph and B/W → colour on the home diptych, the Formation frame and (on hover/focus) the Institutions chamber. |
| **M-2** (Q2) | `apps/legal/views._legal_page` raises **404** for an unpublished **substantive** document (V5.14 categories C/D: `note-legali`, `condizioni-di-utilizzo`, `avvertenze`; `SUBSTANTIVE`) unless the preview flag is on (`ILE_LEGAL_OPEN_FIELDS_ALLOWED`, which `prod.py` forces off): the public never sees «Page en cours de préparation»; the preview hub's legal rows still reach them. The privacy notice and the cookie information (A/B, lane P) keep their route and their blocked state — privacy is never hidden. `apps/legal/apps.py` registers the three C/D routes behind the `legal_pages` gate (`requires_gate`), so the route suites expect their 404 and `core.links` hides links to them while it is closed. `templates/community/join.html` links the terms only through `{% legal_links "terms" %}`. Recorded slice of lane P's `apps/legal` (DECISIONS §16 assigns M-2 to lane C). Other lanes' links — see Requests. |

## 2. What the owner sees where (8780 after the merge; lane server 8785 now)

**Page Headers — «il frontespizio».** `templates/pages/partials/_ingresso.html` (the one header of the public interior)
is now a band with a material ground and a per-page drawing; the reading pages (FAQ, glossary, Vivre en Italie) wrap
their head in the same band. One system, a purposeful composition per page (V5.15 §3/§4):

| Page | Composition (motif · tone · frame) |
|---|---|
| `/fr/parcours/`, a pathway sheet | **route** — a drawn journey line, stations lighting one after another · paper · person at the window (W2) |
| `/fr/entreprises/` | **economic** — a production skyline under a rising line · paper · workshop (W2), now a 6/6 landscape split |
| `/fr/institutions/` | **civic** — a colonnade and entablature (architecture, governance) · paper · council table (W2) |
| `/fr/universites-et-formation/` | **learning** — ruled lines and an ascending progression · paper · reading room (W2) |
| `/fr/formation/` | **learning** · paper · NEW: a trainee hands the torch to another (5265332) |
| `/fr/diplomes-et-titres/` | **learning** · paper · NEW: an open accordion case of papers (4792286) |
| `/fr/projet-pilote/` | **mission** — the brand's arch geometry, gold point of light · **night** · NEW diptych «two territories»: a misty poplar plain (11010756) and flowering fields under a range (36909829), the second a step lower |
| `/fr/le-projet/` | **mission** · **night** · NEW: a great study hall from a gallery (10323211) — the system vision |
| `/fr/reseau/` | **network** — five nodes around one centre · **night** · NEW: one shared table from above (34632581) |
| `/fr/contact/` | **contact** — a coordinate grid and a located point with two rings · paper · NEW: a civic square between two palazzi (14581980) |
| `/fr/agami/` | **civic** · paper · no photograph (Q5) |
| `/fr/attention-aux-fraudes/` | **legal** — two margin rules and ruled lines: restrained · paper · no photograph |
| `/fr/faq/` | **route** · the search seat becomes a frosted raised plate over the grid |
| `/fr/glossaire/` | **learning** · the same search plate |
| `/fr/vivre-en-italie/` | **territory** — contour lines · NEW 21:9 street of stucco façades under the approved intro (12900263) |

Every band: the 12-column architectural hairline grid fading toward the reading edge, a warm light from the far side (gold
on night), a fine grain; the folio (concept glyph in a disc — lane B's sprite — the label in tracked capitals, a rule that
draws); the h1 at a display size (36 → 56 px); the lead at 20 → 22 px; the photograph in a passe-partout (a hairline
frame offset behind it slides into register) with a depth shadow; the trail sits on the band (on night inks on a night
band). Motion: strokes draw once (pathLength), nodes come one after another on `--spring-soft`, the end point's light
breathes in once, a slow parallax as the band leaves (scroll timeline). Arabic: the drawing, the grid fade, the light and
the passe-partout mirror; photographs never flip.

**Imagery Pass.** 11 new licensed frames (Pexels, provenance, register §3.3, AUM §10), each in one slot site-wide — the
uniqueness test covers the hero and portico families. Body frames: `/institutions/` the assembly hall beside the
recipients' statement (B/W, colour under pointer/focus); `/entreprises/` a 21:9 band of greenhouse tunnels at dusk (the
productive territory) between «Trois temps» and the form; `/formation/` a row of microscopes beside «Second temps» (B/W →
colour as it enters). The mega menu keeps its four dedicated portico frames (cms_nav `_DOOR_PHOTOS`), which appear on no
page: lane A's redesign can draw them as they are.

**Section design.** `/fr/le-projet/` «Les espaces de l'écosystème» → four weighted tiles (audience glyph in a disc, the
accent rule along the foot drawing across on hover, lift + depth, whole tile the target). `/institutions/` → editorial
split (statement | photograph). `/entreprises/` → photographic band. `/formation/` → the after-arrival frame beside its
text on the line.

**Typography (decided, no catalogue).** One family stays — Host Grotesk for Latin, Vazirmatn for Arabic, IBM Plex Mono
for folios — because it is institutional, multilingual and already self-hosted (no font weight added to LCP). The change
is the hierarchy: a display step for page heads (clamp 36→56 px, −0.028 em, 600), tracked capital folios at 12 px, a
20→22 px lead, Arabic heads at line-height 1.35 with no negative tracking. Never a newspaper: no serif display, no
italic, no column rules.

## 3. Review (headed Chromium, Chromium lock taken and released each run)

Headed walks (real scroll, reveals playing) with `chromium-1234` (the installed headed build): fr 1440 (entreprises,
le-projet, formation, institutions), ar 1440 (formation, projet-pilote, réseau), fr/ar 390 with reduced motion
(institutions, contact, FAQ, Vivre en Italie); full-page shots fr 1440/390 of 11 pages, ar 1440 of 3 pages. Scripts and
shots outside the repo: `C:/tmp/ile_v5_council/.work/v515-c/` (`shots.py`, `walk.py`, `before/`, `r1`–`r4/`, `w1`–`w3/`,
`look/`). No horizontal scroll on any lane C page at either width (the only HSCROLL seen was the 404 page at 390, not a
lane C file).

Self-score against «a premium institutional legal-tech platform»: heads 4/5 (paper bands) – 4.5/5 (night bands);
imagery 4/5; body sections 3.5/5 — the long-copy chapters (head at the edge | prose) remain the W2 grammar on pages whose
copy is locked prose; they are now framed by a strong head and photographs. Improved after the first look: the band height
(no 62vh void), the 3:2 split (6/6), the motif kept away from the words on phones, the frame offset inside the phone gutter,
the second-time frame moved beside its text.

## 4. Budgets (gzip -9)

| Sheet | Before → after |
|---|---|
| `main.css` (shared) | 31 288 → **31 288** (unchanged; nothing of this lane in it) |
| `pages/css/fronte.css` (NEW, page-only, linked by the head itself before the band) | — → 2 854 B |
| `pages/css/interior.css` | 2 310 → 3 106 B (+ `_photo.css`, `_compose.css`) |
| `ecosystem/ecosystem.css` | 4 355 → 4 755 B |
| `pathways/pathways.css` | 4 492 → 4 924 B |
| JS | none added |

Images: every budgeted derivative of the new frames ≤ 60 KB (LCP/band) / ≤ 45 KB (body); at 1440 1x the LCP files are
7–18 KB AVIF. `static/img/v5/`: 184 files, 7.3 MB on disk (W2: 88 files, 2.8 MB) — the 1600/1920 widths are only picked
by 2x+ wide screens. CLS: explicit width/height on every `<img>` and `<source>`; the band's sheet is linked before it, so
it never repaints. Mobile LCP under throttling not measured here (the reviewer's Lighthouse pass).

## 5. Tests

New: `tests/frontend/test_frontispiece_v515_c.py` — 42 tests (12 pages × the frontispiece; 3 reading pages × the band;
15 pages × one LCP / lazy-and-masked body frames / img inside picture / no own B/W mechanism; 3 section compositions and
their grade; the pilot diptych; the Arabic band; the band's motion only under no-preference and never on html.rm, the
drawing mirrored and no photograph flipped; the compositions' lift gated; the sheets page-only and ≤ 6 KB; M-2: three
unpublished C/D legal routes 404 outside the preview and 200 in it; the privacy notice never a 404; the terms linked only once published).

Brought to the decisions (each superseded assertion now asserts the new rule):
- `apps/pages/tests/test_home.py::test_black_and_white_rests_only_in_the_hero` — the diptych carries `data-grade="bw-scroll"`, every frame under the hero `data-reveal="mask"`, and lane A's sheet has the reduced-motion and html.rm guard (was: `.foto--develop` + C's own keyframes).
- `tests/compliance/test_imagery_v512.py::test_the_home_draws_the_diptych_and_the_ecosystem_frame_lazily` — two `bw-scroll`, no `foto--develop`.
- `apps/ecosystem/tests/test_compliance.py::test_stylesheet_uses_tokens_logical_properties_and_no_motion` — `_compose.css` in the import list and the token/logical scan; `_photo.css` animates nothing; `_compose.css` no keyframes, its lift under no-preference.
- `tests/frontend/test_interior_w3_f1.py::test_page_sheets_are_plain_import_lists_in_the_collected_tree` — the three sheets' new import lines.

Also brought to the decisions: `tests/i18n/test_page_integrity.py::test_blocked_legal_page_titles_follow_the_page_language`
(I18N-07) — it now asserts the public 404 of the three C/D pages AND still reads their lazy blocked titles where they are
drawn (the preview); `tests/compliance/test_imagery_v512.py::test_the_weights_hold_their_budget` — a 21:9 band's
budgeted widths are its 1200/1600 (the widths a 1x desktop takes for a full-width band); `test_interior_w3_f1::
test_one_primary_action_and_at_most_six_icons_in_the_body` — the frontispiece's folio glyph is counted with the head
marks, as chapter marks are, not as a body icon (the six-icon ceiling of the body stands). An untranslated alt now carries
`lang="fr"` (`imagery.Picture.alt_lang`) until D's pass.

Runs (database lane l5 `test_ile_v5_l5`, one pytest at a time, `-m "not browser"`):

| Run | Result |
|---|---|
| Lane C batch 1 — `test_frontispiece_v515_c.py`, `test_imagery_v512.py`, `test_figure_caption.py`, `apps/pages/tests/test_home.py`, `apps/ecosystem`, `test_interior_w3_f1.py`, `test_cms_nav.py`, `test_templates_static.py`, `test_css_bundle_is_current.py` | 512 passed, 3 failed → the 3 fixed (icon count rule, 21:9 budget widths, the grain's inner `url()`), rerun 18/18 |
| Batch 2 — `apps/legal`, `test_icons.py`, `test_forms_legal_basis_v516.py`, `test_public_pages.py`, `test_content_pages_w3_f2.py`, `test_layout.py`, `test_service_pages_w3_f2.py`, `test_page_integrity.py`, `apps/pathways`, `apps/living`, `apps/faq`, `apps/glossary` | 414 passed, 47 failed → the 36 caused here (C/D 404 extended to privacy; the error pages' privacy link) fixed by narrowing to C/D and restoring the privacy link |
| Final — `test_page_integrity.py`, `test_frontispiece_v515_c.py`, `test_imagery_v512.py`, `test_css_bundle_is_current.py`, `test_public_pages.py`, `apps/legal` | **134 passed, 1 failed**: `test_latin_text_on_arabic_pages_carries_its_own_lang_attribute` — four W2 lane C msgids still untranslated in AR («Le même geste», «Autres voies», the parcours count line ×3): D's catalogue pass (listed in W2's notes; repeated below) |
| Pre-existing on design-v5 `ece1eeb` (run there, same database: **11 failed**, identical) | `test_service_pages_w3_f2`: `test_400_and_500_render_without_the_database…[400/500]`, `test_every_account_page_stands_in_one_frame` ×6, `test_the_profile_s_personal_fields…`, `test_the_situation_s_personal_facts…` ×2 — none of this lane's files |

`tests/frontend/test_frontispiece_v515_c.py`: 42 tests, all passing.

## 6. New msgids (for D's catalogue pass)

All are alt texts in `apps/pages/imagery.py` (French source):
- «Dans un atelier de formation, une main tend la torche de soudage à une autre, au-dessus de l’étau»
- «Une rangée de microscopes sur une paillasse claire»
- «Un classeur à soufflets ouvert sur une table de bois, rempli de pièces rangées»
- «Une rangée de peupliers nus au bord d’une plaine labourée, dans la brume»
- «Des champs en fleurs au pied d’une chaîne de montagnes enneigées»
- «Une grande salle d’étude vue depuis une galerie : verrières, longues tables, lustres»
- «Une longue table partagée vue d’en haut : ordinateurs, carnets, papiers»
- «Une rue de façades enduites aux couleurs chaudes, volets et balcons fleuris»
- «Une place pavée entre deux palais ; quelques passants s’éloignent»
- «Des serres en tunnel à travers une plaine cultivée, au crépuscule»
- «Les pupitres et les micros d’une salle d’assemblée, sièges vides»

No template string added; «Photo» reused. No longer used: none.

Still waiting from W2 (lane C's W2 notes; the Arabic language-of-parts test fails until they are translated): «Le même
geste», «Autres voies», and the parcours count line «%(n)s parcours affiché / affichés».

## 7. Requests to other lanes

- **Lane A — `COMPONENT_PROVENANCE.md` rows** (adapted as design-engineering raw material, rebuilt in vanilla CSS on ILE tokens, no code imported):
  - «Animated Grid» (21st.dev, rmahammad, id 29376: CSS-only grid, radial fade, reduced-motion aware) → the frontispiece's 12-column hairline grid with its reading-edge fade (`v5/_fronte.css` §1);
  - «Background Beams» (21st.dev, manuarora700, id 1152: SVG paths carrying light) → the per-page motif drawn once with pathLength, nodes and the end light (`templates/pages/partials/motifs/*`, `_fronte.css` §4);
  - «Editorial Collage Hero» (21st.dev, felipemenezes098, id 19074: layered images over a wash) → the passe-partout frame behind the head photograph and the pilot's stepped diptych (`_fronte.css` §5);
  - «Scroll animated timeline» (21st.dev, ibrandify, id 35029) → reviewed for the Formation passage; kept the existing «linea» and added the frame beside the second time (`_compose.css` §3);
  - «Split Hero With Image Cards» (id 19078) and «Hero Section» (redrob-labs, id 38090) reviewed, not adopted (avatar social proof / film backgrounds do not fit an institutional head).
- **Lane A — mega menu**: the four portico frames stay dedicated to the menu (`static/img/portico/`, `cms_nav._DOOR_PHOTOS`); no page draws them. Reveal: the head's photograph is eager and never masked; please keep `.figura > picture { overflow: clip }` from clipping the passe-partout only on curated heads (it does today; acceptable).
- **Lane A — `base.html`**: nothing needed; the band links its own sheet. M1's head hairline still draws on `.ingresso` (the band no longer clips; only its ground does). On the three reading pages the head is inside `.fronte-wrap`, so M1's `:has(+ .chapter)` no longer matches there — if A wants the draw there too, add `.fronte-wrap` to that selector.
- **Lane B** — `templates/enquiries/partials/form_shell.html` links `{% url 'legal:privacy' %}` unconditionally: move it onto `{% legal_links "privacy" %}` (M-2). The orientation templates include `_ingresso.html` and get the plain band; pass `motif="route" glyph="compass"` there if you want the drawn route (one line per include).
- **Lane D** — `templates/documents/partials/depot.html` and `templates/documents/terms_required.html` resolve `{% safe_url 'legal:terms' %}` regardless of publication: move them onto `{% legal_links "terms" %}` (M-2). Catalogue pass: the 11 msgids above.
- **Steward** — run the browser suites that measure the heads: `apps/pages/tests/test_browser.py`, `apps/ecosystem/tests/test_browser*`, `tests/frontend/test_browser_w3_f1.py` (the band is taller than the W2 entrance and the 3:2 heads are 6/6), and the reveal suites (`test_motion_v512_a_w2`) now that photographs carry `data-reveal`.
- **Steward — ownership** (`docs/design-v5/OWNERSHIP_V54.json`, steward-written): record the family `v515-c` — whole
  files it created (`static/css/v5/_fronte.css`, `_compose.css`, `apps/pages/static/pages/css/fronte.css`,
  `templates/pages/partials/motifs/*`, `tests/frontend/test_frontispiece_v515_c.py`, `static/img/v5/{formation,diplomes,projet,reseau,vivre,contact}/**`,
  this notes folder) and slices of what it changed: `apps/legal/views.py` + `apps.py` (M-2, lane P's files),
  `templates/community/join.html` (the terms link), the three test files brought to the decisions.


## Round 1 improvements (label v515-c-improve1)

Quality round 1 scored lane C 3–4/5 (art direction 3, motion 3.5, sections 3). Every major is fixed and so are the
cheap minors. Each fix below was checked in a browser after it was made: 1440/1024/768/390 fr, 1440/390 ar, headed
Chromium (`chromium-1234`) for the Arabic heads and the body walk, under the Chromium lock. Scripts and shots are
outside the repo in `C:/tmp/ile_v5_council/.work/v515-c/` (`look1.py`, `lcp1.py`, `shots_i1.py`; `i1/before`,
`i1/a1`–`a3`, `i1/walk`).

### The majors

| Finding | What changed |
|---|---|
| **Formation «Second temps» covered** (`_compose.css` §4, absolute frame) | The absolute frame is gone. From 64 rem the step's grid gets a third track: `var(--linea-node) | minmax(0,1fr) | minmax(0,26rem)`. The frame sits in column 3, rows 1–4, with a `--s-6` inline-start margin. Below 64 rem it stays under the text in the words' column. Checked at 1440 and 1024: the frame no longer overlaps the text. Guarded by `test_the_second_time_frame_has_its_own_column_never_over_the_text`. |
| **The drawing under the words** (`_fronte.css` §4, phones; the pathway index) | Below 64 rem the motif is now placed according to what stands at the top of the head. Photo first: the motif stays up with the photo. Words first, then the pilot's diptych: the motif goes behind the diptych at the band's foot. Words first, then an index, door, panel or composed seat: no motif. Words alone: the motif gets its own 7 rem strip under the last line, and the band grows to hold it. On pathway sheets the «Sommaire de la page» is now a raised opaque plate, so the route never crosses its links. Every motif now uses `preserveAspectRatio="… meet"`, not `slice`, so a node can no longer be clipped at the band's edge. That was also the cause of AGAMI's colonnade losing its entablature. |
| **11 of 16 heads on one grid; the motif hidden behind the photo** | New `compose` contract on `_ingresso.html` (`data-compose`). On five pages the drawing now *composes* the head (`_fronte.css` §8): **Parcours `route`**: a journey line runs from the folio's disc through station rings on the title, the lead and the question, down to the orientation button. It ends in a gold point with a halo (it draws once, and the stations arrive in order). The words take 7 columns and the portrait 4. **Réseau `network`**: the shared table in a disc at the centre, with the five actors on one ring (glyph disc and name, using the register's existing strings; aria-hidden, because the register below remains what a screen reader reads). Spokes and a pentagon draw, and the actors arrive one by one. **Contact `contact`**: a coordinate plate (grid, two dashed axes crossing on the located point and its rings, a route arriving from the square). The photo is inset on the plate, and the address is the head's action (a 48 px glyph disc and the e-mail in display weight). **Le projet `arch`**: the study hall inside the brand's arch, with the arcs in register and a gold keystone light. **Entreprises `skyline`**: a production skyline 1440 × 220 wide (shed roofs, chimney, crane, offices, silo, under a rising line with nodes) runs along the band's foot, in front of the ground and partly under the frame. With the pilot's diptych and the two type-led heads (below), 8 of the 16 heads now differ in structure, not only in their photo. The vertical rhythm also varies: the top padding is lower (`--s-10`), the route head is start-aligned, and the composed seats set their own height. The ~150 px gap above the folio is gone on Réseau, Contact and Le projet. |

### The minors

| Finding | What changed |
|---|---|
| Pilot diptych 191 px | From 64 rem: words in columns 1–6, pair in columns 7–12 with a `--s-6` gap. Each frame is now **292 px** at 1440 (218 px at 1024), and the second is stepped down by `--s-16`. The mission arch is redrawn centred and set behind the pair (box 48 %, inset 3 %). Its node and halo are removed in the diptych, so nothing shows between the frames. |
| `sizes` understated | 6/6 heads: `(min-width: 80rem) 38rem, (min-width: 64rem) 46vw, 100vw`. 4:5 heads: `32rem / 38vw / 100vw`. Pilot: `18.5rem / 22vw / 46vw`. Composed seats declare the width the *image* is drawn at: arch `40rem / 48vw / 120vw` (a 3:2 file covering a tall arch), disc `26rem / 30vw / 70vw`, plate inset `28rem / 33vw / 76vw`. Second-time frame: `26rem`. `grande-salle-etude` never had `soft` (its recipe has none); its haze is window glare in the source. The arch now crops it to the bright, structured middle, and the 800 w file is chosen at 1440. |
| Assembly hall `bw` unreachable by touch/keyboard | `institutions.chamber` now uses `treatment="develop"` (lane A's `bw-scroll`), so colour arrives as it enters for every input. |
| Fraudes a placeholder; AGAMI a barcode | **Fraudes (`notice`)**: folio with the shield glyph and the label «Espace Personnes» (the space the page belongs to; repeating the h1 would break Q1). The prescribed notice (`p3.antifraud.body`, verbatim, the same warning component) moves from the first chapter into the band as its panel (columns 7–12, depth 3). **AGAMI (`name`)**: the name in two weights through the `fronte_name` filter. It only adds two spans; every character stays in order, and a test checks this: «AGAMI» at 52–104 px / 700, then «— Dialogo Giuridico Interculturale APS» at 22–36 px / 400. The colonnade is redrawn: pediment with its light, cornice, frieze with triglyph ticks, capitals, six fluted columns, three-step stylobate, at 0.58. |
| Le projet: four near-empty tiles; doubled underline | Each tile now carries its space's one line (the network register's existing sentence, through `space_links()` `text`). The link underline is removed inside `.spazi` (the foot rule is the hover cue), and the description is aligned under the title. |
| Caps h1s push the action down | From 64 rem a capitals h1 is capped at **2.5 rem**, measure 23 em, and its lead at 34 rem / 20 px. Below 64 rem a capitals head draws its frame **16:9**. The words are unchanged. Measured at 1440 × 900: Parcours action **847 px** (was 919), Entreprises **753 px** (was 855). |
| fronte.css linked mid-body | Every lane C page now links `css/dist/pages/css/fronte.css` in `{% block extra_head %}`: `pages/institutional_base.html`, `ecosystem/_layout.html`, the five pathway templates, FAQ, glossary and Vivre. These pages pass `fronte_linked=True`. The in-body link is kept only for heads other lanes include without it (orientation, Forum registration). |
| `cms_nav` double highlight | `_OWNER_SECTION` gives a page linked from two panels a single section: pilot → **Projet**, Formation → **Personnes**. Rows in other panels are no longer current. Measured: pilot `current = [Projet]`, formation `[Personnes]` (plus its own row). |
| Pilot's second frame lazy and masked | New slot role `head`: eager, `decoding="async"`, no `fetchpriority`, no `data-reveal`. `pilot.fields` uses it. The page still has one LCP. |
| M-2 (`depot.html`, `terms_required.html`, lane D) | Still open outside lane C. The request below is repeated: the steward should not merge W3 until lane D moves these templates to `{% legal_links "terms" %}`. |

### Motion (lane C side)

The composed heads no longer draw behind a photo. The route spine draws in 1.5 s, then four stations arrive between 550 and 1600 ms and the gold arrival point pulses once. In the network, five spokes draw and five actors arrive over 700–1180 ms. The arch's line draws while its keystone light comes in. In the contact head the route reaches the point and the rings settle. Every animation sits inside `prefers-reduced-motion: no-preference` and `:root:not(.rm)` (the existing guard test covers the new rules). Under reduced motion each head is a complete still. Lines that draw no longer use `vector-effect: non-scaling-stroke`, because screen-space dashes broke the `pathLength` draw. The faint lines keep it.

### Arabic

Every composition mirrors through logical properties, and photographs never flip. The network ring and the arch are symmetric. The contact plate's lines are mirrored with `scaleX(-1)`, together with the inset. On the route head, a French title or lead inside the RTL column is LTR, so its station is placed on its inline *end*, where the line stands. Checked at ar 1440 and 390: no horizontal scroll on any of the 7 heads. Réseau at fr 390 overflowed once (node boxes 8 rem wide). Nodes are now `max-content` below 48 rem, with names from 48 rem.

### 21st.dev (rows for lane A's `COMPONENT_PROVENANCE.md`)

These are design-engineering references only. They were rebuilt in vanilla CSS/SVG on ILE tokens and no code was imported:
- «Nodes» (abhishek-mallick, id 40282) and «Hub» (id 40299, hub and tiles linked back): the network ring around one centre, the actors arriving, the spokes drawing (`templates/pages/partials/fronte/_rete.html`, `_fronte.css` §8).
- «Timeline» (manuarora700, id 857, the scroll beam) and «Scroll animated timeline» (ibrandify, id 35029): the journey spine with its stations and its arrival light (`_fronte.css` §8 route).
- «Hero 115» (shadcnblocks, id 608, radial circle pattern): the arcs in register around the arch (`fronte/_arco.html`).
- Reviewed and not adopted: «Lattice Hero» (id 26027, WebGL), «Cinematic Orbit Hero» (id 32357), «Interactive Dot Grid Hero» (id 20044, canvas). Each needs a canvas or WebGL runtime for a head that SVG + CSS can draw.

### Budgets (gzip -9)

| Sheet | build → round 1 |
|---|---|
| `main.css` (shared) | 31 288 → **31 288** (unchanged) |
| `pages/css/fronte.css` (page-only, now in `<head>`) | 2 854 → **~5.0 KB**, within its 6 KB ceiling (test). This is the cost of the five composed heads. |
| `pages/css/interior.css` / `ecosystem.css` / `pathways.css` | 3 106 → ~3.15 KB / 4 755 → ~4.8 KB / 4 924 → ~4.96 KB |
| JS / images | none added |

**LCP (mobile, my own throttle, dev server):** 390 × 844 at DPR 2, CPU 4×, 1.6 Mbps / 150 ms, cache off, the uncompressed `runserver` static. Median of 3 runs: Pilote fr 2548 ms (text), Contact ar 2436 ms, Formation ar 2776 ms, Parcours 2208, Réseau 2160, Le projet 2332. CLS 0 on all of them. This throttle is harsher than the reviewer's, so these numbers cannot be compared directly with the review's. The steward's Lighthouse pass on the collected and compressed build is still the measure of record. Formation ar's LCP image is the 800 w frame at DPR 2.

### Tests (database lane l5, `test_ile_v5_l5`, one pytest at a time)

- `tests/frontend/test_frontispiece_v515_c.py`: brought to the round's decisions. The sheet is now in `<head>` and not in `<main>`. A head's second frame is unmasked, eager and has no fetchpriority. New tests cover: the seven compositions and what stands in each head, the five network names hidden from assistive technology with the register still present, the fraud notice once and in the head, the promoter's name character-exact, one owner section for the pilot and for Formation, the second-time frame in its own column, the drawn `sizes`, and the assembly hall developing.
- `tests/frontend/test_cms_nav.py::test_rows_override_fallback_and_respect_visibility_flags_and_gates`: this test's manual row linked `/fr/avvertenze/` and its flag row linked `legal:terms`. Both are C/D legal pages, which 404 until published since the build's M-2. They now link two open routes (`/fr/privacy-policy/`, `pages:contact`). The test's subject (rows, visibility, flags and gates) is unchanged.
- `tests/frontend/test_interior_w3_f1.py::test_one_primary_action_and_at_most_six_icons_in_the_body`: the network head's five actor glyphs and the contact action's disc are now counted with the head's marks, as the folio glyph already was. These are the head's drawing (aria-hidden), and the six-icon ceiling for the body still applies.
- Runs:
  1. Frontispiece + imagery + `test_cms_nav` + `apps/pages/tests/test_home.py`: 157 passed and 1 failed (the nav row above). Fixed; rerun 11/11.
  2. Broader batch (`apps/pages`, `apps/ecosystem`, `apps/pathways`, `test_interior_w3_f1`, `test_templates_static`, `test_css_bundle_is_current`, `test_public_pages`, `test_content_pages_w3_f2`, `test_page_integrity`, `test_layout`, `test_locked_content`, `test_figure_caption`): **870 passed, 2 failed**.
     - The icon ceiling on /reseau/ (above) was fixed; rerun `test_interior_w3_f1` 88/88.
     - `test_latin_text_on_arabic_pages_carries_its_own_lang_attribute` is the pre-existing failure from W2: four lane C msgids are still untranslated in AR, waiting for D's catalogue pass.
  3. Final: frontispiece + `test_css_bundle_is_current` + `test_cms_nav` + `apps/ecosystem/tests/test_compliance.py`: **94 passed**.

### Requests (unchanged unless stated)

- **Lane D**: `templates/documents/partials/depot.html:78,82` and `templates/documents/terms_required.html:24` → `{% legal_links "terms" %}` (M-2). **The steward must not merge W3 until this is done.** Catalogue: no new msgid this round. All the strings were already in the catalogue: «Espace Personnes», the actors' titles and sentences, «Votre protection».
- **Lane A**: the provenance rows above. Lane A's reveal marks (`.registro__glyph` on `.spazi`) appear only once the page scrolls. That is intended, so no request.
- **Steward**: Lighthouse on the collected and compressed build for Pilote fr, Contact ar and Formation ar. Ownership: add `templates/pages/partials/fronte/*` (new, whole files) to the family `v515-c`. Slices this round: `apps/pages/services.py` `space_links()` (one key), `apps/pages/templatetags/pages_imagery.py` (`fronte_name`), `tests/frontend/test_cms_nav.py` (the row above).

## Round 2 improvements (label v515-c-improve2)

Quality round 2 scored lane C 3.5–4.5/5 (imagery 3.5, sections 3.5). The three majors are fixed, and so are the
minors lane C can act on (m-1 to m-9, m-11). m-10 belongs to the steward and m-12 to lane D. I checked each fix in
headed Chromium (`chromium-1234`) under the Chromium lock, on lane server 8785 (l5): fr at 1440/1280/1024/768/390/360,
ar at 1440/1280/1024/390, it at 360. The scripts and screenshots are outside the repo in
`C:/tmp/ile_v5_council/.work/v515-c/` (`r2run*.py`, `ev_all.js`, `ev_training.js`; `i2/a1`–`a3` with `res.json`).

### The majors

| Finding | What changed | Measured |
|---|---|---|
| **MJ-1**: the B/W frames never developed. Two animation shorthands landed on one img and the zoom won. | `v5/_photo.css` (lane C's page-only partial, in the interior, pathways, ecosystem and home sheets) now holds the combined rule the review prescribed, under lane A's own guards (`@supports (animation-timeline: view())`, no-preference, `:root:not(.rm)`): `[data-reveal="mask"][data-grade="bw-scroll"] > picture > img { animation: reveal-zoom …, reveal-colour …; animation-timeline: view(), view(); animation-range: entry 0% cover 45%, entry 40% cover 50% }`. Its specificity (0,4,2) beats both of lane A's rules, which are unchanged. Mask, zoom and colour all run. A request to lane A follows below. | At mid-viewport the img computes `grayscale(0)` (`animationName` = `reveal-zoom, reveal-colour`) on Formation fr/ar at 1440/1280/1024, Institutions fr at 1440 and 390 (touch), and the home diptych fr at 1440 and 390. Far below the fold the same frame computes `grayscale(1)`. New browser test: `tests/frontend/test_browser_v515_c.py`. |
| **MJ-2**: in Arabic, the promoter's name read «… APS —». | `fronte_name` now emits `<span class="fronte__name" lang="it" dir="ltr">` and `<span class="fronte__name-rest" lang="it" dir="ltr">— …</span>`. The Italian legal name is tagged (WCAG 3.1.2) and isolated LTR. Under `[dir=rtl]` both lines align right. That selector is stronger than base.css's start-aligned Latin run, so the h1 lines up with its folio. No character changes, and the existing character-exact test still passes. | ar at 1440 and 390: «AGAMI», then «— Dialogo Giuridico Interculturale APS», both on the right edge under the folio. Test: `test_the_promoter_name_reads_ltr_in_arabic`. |
| **MJ-3**: Formation «Second temps» was lopsided (text ~360 px, frame 392 px, ~420 px empty). | `_compose.css` §4, from 64 rem: the chapter's body spans the whole container (`grid-column: 1 / -1`, only for the training phases). Both times use the tracks `var(--linea-node) minmax(0,34rem) minmax(0,1fr)`, so «Premier temps» and «Second temps» share one text column. The frame sits in track 3, at `grid-row: 2 / span 3` (top-aligned with the h2), with a `--s-10` inline-start margin, and fills to the container's edge. `training.after` sizes are now `(min-width: 80rem) 38rem, (min-width: 64rem) 40vw, 100vw`. | Text 544 px. Frame **612 × 432** at 1440 (800 w file), 468 × 336 at 1280, 301 × 225 at 1024. Frame top at 1272, h2 at 1280. Mirrored in ar (frame on the left, text on the right). No overlap. |

### The minors

| Finding | What changed | Measured |
|---|---|---|
| m-1: motif debris in the outer gutter | `notice` joins the composed seats whose ground motif stands down. From 64 rem, on uncomposed heads with a seat (photo or index) and on the reading pages' band (search plate), the motif now ends at the content edge (`inset-inline-end: max(0px, (100% - var(--container))/2 + var(--grid-margin))`, 56 % wide), and its gold end node and halo are hidden. | At 1440 on Formation, Institutions, Universités, FAQ, Glossaire and Vivre: motif box 535–1333 against a content edge at 1332, 0 visible end nodes. Fraudes: motif `display: none`. |
| m-2: arcs through the pilot credits | `.ingresso__pair .foto__credit` now sits on a band-tone chip (`color-mix(… --fronte-bg-1 88%)`, 2 × 8 px). | fr 1440: both credits read clearly over the arcs. |
| m-3: Parcours action below the fold | From 64 rem the route lead is 18 px / 1.55 at 34 rem, and the way sits `--s-6` under it. Below 48 rem a capitals head reads its words and its action first and its photograph after (the drawing stands down), with a 17 px lead. The locked copy is unchanged. | Action bottom: **842** at 1440 and **898** at 1024, both inside 900. **842** at 390 (was 1146), 950 at 360 (was 1242), 870 at ar 390 (was 1178). |
| m-4: the @ disc was on the wrong side in Arabic | The link keeps the page's direction. Only the address carries `.email` (base.css LTR isolate). | ar 1440: the disc is at x 1284–1332 (the reading edge), the address at 912–1268. |
| m-5: network glyphs had no names on phones | The names now show at every width: caption size, 6.5 rem max on phones, and the ring gets `--s-16` below it. | fr/it/ar at 360 and fr at 390: all 5 names drawn, no horizontal scroll. |
| m-6: Fraudes folio disagreed with the breadcrumb and nav | `_OWNER_SECTION` gains `pages:antifraud → pathways:index`. The breadcrumb is now «Accueil › Espace Personnes › Attention aux fraudes». | `current = [Personnes]`. The test is parametrised with the page. |
| m-7: a curated library photo could replace a composed head | The three includes no longer pass `photo=photo` (the view keeps it for SEO). `_ingresso.html` now tests `aside_template` before `photo`. | Test: `test_a_curated_library_photograph_never_replaces_a_composed_head` (Le projet, Réseau and AGAMI, with every library slot curated). |
| m-8: Fraudes notice at 20 px on phones | Below 48 rem the head's notice body is `--t-body` and the panel padding is `--s-5 --s-4`. | 17 px. Head 917 px tall at 390 (was 953). The lone «»» on its own line needs an NBSP inside the locked copy, so I raised it with the owner and left the copy untouched. |
| m-9: pilot diptych at 768–1023 | Between 48 and 64 rem the pair is capped at 34 rem and centred. | At 768: frames 264 px, band 816 px (was over 1000). |
| m-11: caps heads were photo-first on phones | Same remedy as m-3. | Entreprises at 390: action bottom 730 (band 982, was 1040). Diplômes at 390: band 949 (was 1112). |
| m-10: LCP on the compressed build | Not lane C's to measure. The steward runs Lighthouse on Pilote fr, Formation ar and Contact ar before merge. | — |
| m-12: `depot.html` / `terms_required.html` | Lane D's (M-2). The request is repeated below. | — |

### 21st.dev (rows for lane A's `COMPONENT_PROVENANCE.md`)

Design references only, rebuilt in vanilla CSS on ILE tokens. No code was imported.
- «Blog 8» (shadcnblockscom, id 687: a row with a large image at the far edge) and «Feature with image» (tommyjepsen, id 1337): the Formation editorial split, a 34 rem text column beside a frame that fills to the container edge (`_compose.css` §4).
- Reviewed and not adopted: «Horizontal Feature Reveal» (hyperiux, id 26062) needs GSAP SplitText and parallax, a runtime for a two-row split. «Editorial Image Hero» (id 19077) puts a full-width image above the text, which would push the locked text below the fold.

### Budgets (gzip -9, build → round 2)

| Sheet | Before | After |
|---|---|---|
| `main.css` (shared) | 31 288 | **31 288** (unchanged) |
| `pages/css/fronte.css` (page-only) | 5 104 | 5 318 (within its 6 KB ceiling) |
| `pages/css/interior.css` / `pathways/pathways.css` / `ecosystem/ecosystem.css` / `pages/css/pages.css` | 3 158 / 4 963 / 4 794 / 4 123 | 3 303 / 5 102 / 4 939 / 4 279 (the MJ-1 rule and the split, page-only) |
| JS / images | — | none added (the 800 w microscopes file already existed) |

### Tests (database lane l5, one pytest at a time)

- `tests/frontend/test_frontispiece_v515_c.py`: new `test_the_promoter_name_reads_ltr_in_arabic` and `test_a_curated_library_photograph_never_replaces_a_composed_head` (3 cases). The one-section test now covers Fraudes.
- New `tests/frontend/test_browser_v515_c.py` (browser): a developing frame is in full colour at mid-viewport (Formation and Institutions, at 1440 and 390) and grey before it enters.
- Run 1: frontispiece + cms_nav + imagery + bundle: **91 passed**.
- Run 2: the same plus `test_interior_w3_f1`, `test_motion_v512_a_w2`, `apps/pages/tests/test_home.py` and `test_figure_caption`: **286 passed, 2 failed**. Both failures were in lane A's browser test `test_the_head_s_hairline_draws_at_load…`. That file launches Chromium, and I ran it in this batch without the lock. That was my error; run 3 repeats it under the lock.
- Run 3, under the Chromium lock: `test_browser_v515_c.py` passed **5 of 5** (Formation and Institutions in colour at mid-viewport at 1440 and 390, grey before they enter). Lane A's `test_the_head_s_hairline_draws_at_load…` failed in both cases (**2 failed**). It waits for `.page-header + .chapter` on `/fr/faq/`, and lane A's M1 hairline is drawn on `:is(.ingresso, .page-header):has(+ .chapter)`. Since the W3 build (fb4542a, not this round), the reading pages' header has stood inside the band, as `.fronte-wrap > .page-header` followed by `.chapter`. So that selector never matches on FAQ, Glossaire and Vivre: the test times out and the hairline is not drawn there. See the request to lane A below.

### Requests

- **Lane A**: move the MJ-1 combined rule (end of `v5/_photo.css`) into `_reveal.css`, or move the zoom onto `<picture>`. Lane C then removes its copy. Lane A also adds the provenance rows above.
- **Lane A (M1 hairline, found in run 3)**: extend the head hairline in `_reveal.css` (the three rules on `:is(.ingresso, .page-header):has(+ .chapter)::after`) to `.fronte-wrap`. Also change `tests/frontend/test_motion_v512_a_w2.py::test_the_head_s_hairline_draws_at_load…`, which waits for `.page-header + .chapter` and probes `.ingresso, .page-header`, to `:is(.page-header, .fronte-wrap) + .chapter` and `.fronte-wrap`. Until then, FAQ, Glossaire and Vivre draw no head hairline and that test fails. Lane C does not edit lane A's sheet or test (§10.0).
- **Lane D**: point `templates/documents/partials/depot.html:78,82` and `templates/documents/terms_required.html:24` to `{% legal_links "terms" %}` (M-2 / m-12). **The steward must not merge W3 until this is done.** Catalogue: no new msgid (the breadcrumb's «Espace Personnes» is already in it).
- **Owner (via the Director)**: the closing guillemet of `p3.antifraud.body` wraps alone on phones. Only an NBSP inside the locked copy fixes that, so lane C left the copy as it is.
- **Steward**: Lighthouse on the collected, compressed build (Pilote fr, Formation ar, Contact ar). Slices this round: `apps/pages/views.py` (the antifraud breadcrumb, one line), `apps/cms/templatetags/cms_nav.py` (`_OWNER_SECTION`, one row), `apps/pages/templatetags/pages_imagery.py` (`fronte_name`), `apps/pages/imagery.py` (one `sizes`). New whole file: `tests/frontend/test_browser_v515_c.py`.

## Finishing round F1 (label v515f-c-improve1)

Base: `design-v5` at 7f2a02d (lanes P2/P3: the privacy classification and V5.17's governance correction) merged into
v515-c first (e273e7c), with no conflict. The compliance lanes' guards are unchanged, and lane C's presentation is
unchanged.

### The review's findings

| Finding | Status in F1 |
|---|---|
| **major**: round 3's headed inspection never ran, because of lock contention | **Run.** The round-3 scripts (`C:/tmp/ile_v5_council/.work/v515-c-qa3/interact3.py`) ran in headed Chromium (`chromium-1234`) under the Chromium lock, on lane server 8785 restarted on the merged code. Evidence: `C:/tmp/ile_v5_council/evidence/v515/c/r3/` (interact3.json and 90 screenshots). After the F1 changes, a second headed sweep ran (`qa_f1.py`, 206 loads): fr and ar at 1440/1024/768/390/360 for all 16 pages, plus reduced motion at 1440 and 390 on the composed heads. Evidence: `…/evidence/v515/c/f1/` (f1.json and screenshots). The review's own server (on 8785 since 05:37) was stopped. |
| minor: `test_page_integrity::test_latin_text_on_arabic_pages_carries_its_own_lang_attribute` fails | **Still failing, named here as asked:** 1 failed, 274 passed on l5 after the merge. The four untagged French msgids («Le même geste», «Autres voies», «N parcours affiché(s)») wait for lane D's catalogue pass (§10.0). The steward treats this test as a merge blocker until then. |
| minor: lane A dependencies (the combined zoom+colour rule; the head hairline on `.fronte-wrap`) | **Lane A's.** The request is repeated below. Measured again: FAQ, Glossaire and Vivre still draw no head hairline (`::after` content `none`). |
| minor: M-2 / m-12 `depot.html`, `terms_required.html` | **Lane D's.** The request is repeated below. |

### Measured in headed Chromium (round-3 probes, on the merged code)

- **The B/W frames develop.** Formation `training.after`, Institutions `institutions.chamber`, and the home diptych `marble` and `cedar` were checked in fr and ar, at 1440 and at 390 (touch). Each computes `grayscale(1)` before it enters, about `grayscale(0.6)` when it enters at 85 % of the viewport, and `grayscale(0)` at mid-viewport. Under reduced motion each is still and in colour, with no animation.
- **Formation split.** At 1440 the text column is 544 px and the frame is 612 × 432, top-aligned with the h2 (frame at 1272, h2 at 1280). At 1280 the frame is 468 × 336; at 1024 it is 301 × 224. The layout is mirrored in ar and is the same in en. At 768 and 390 the frame stacks under the text. Nothing overlaps at any width.
- **Heads.** AGAMI in ar has both lines right-aligned at 1332 (`lang=it dir=ltr`). On Contact in ar, the @ disc sits at 1284–1332, on the reading edge. Réseau shows all five names at 1440 and 390, in fr and ar. Fraudes keeps the trail «Accueil › Espace Personnes › Attention aux fraudes», its notice is 17 px on phones, and its nav current is Personnes. The pilot credits sit on the band-tone chip.
- **Real navigation.** Header clicks to Parcours, Réseau, Contact and Le projet reach their pages in fr and ar. Keyboard: on Parcours the 4th Tab after the chrome reaches the orientation action, and on Contact it reaches the address. The focus ring is 1.6 px solid teal at every stop.

### What F1 changed (real defects the headed run found)

1. **Head layout keyed on the page, not on the case of the string.** The head's capitals test (`title|upper == title`) is true for every Arabic title, because Arabic has no case. So every Arabic photo head (Institutions, Universités, Formation, Réseau, Contact…) carried `ingresso__title--caps` and took the capitals layout that its French page does not: words before photo on phones, the narrowed lead, the 16:9 frame, the drawing stood down. The layout is now named by the page: `words_first=True` on Parcours, Entreprises, Diplômes and the pilot sets `data-words-first` on the band, and `_fronte.css` keys its four layout rules on it. `ingresso__title--caps` is now purely typographic and needs a cased letter. The same rule now applies in `_chapter_head.html`, Formation's phase label and the anti-fraud callout's title. Measured: the head action is inside the first screen on Parcours, Entreprises and Contact in fr and ar at 1440, 1024 and 390, with and without reduced motion. Parcours fr 390: bottom 810 / 844. Parcours ar 390: 830. Entreprises fr 390: 730. Entreprises ar 390: 763. In ar, Institutions now reads photo-first, as its French page does.
2. **Capital section titles.** «POURQUOI ITALY LEGAL ENTRY» on Le projet stood at 28/36, untracked, beside mixed-case titles at the same size, and read louder than they did. `_chapter_head.html` now adds `chapter__title--caps` to a cased capital title. In `_compose.css` §5 such a title is tracked (`--track-display-caps`, case features), and from 48 rem it is set at 24/32. The class is doubled so that, on the Arabic page, the French run outweighs base.css's `:lang(ar) h2` reset. Measured: fr 1440 and 768 at 24 px with +0.48 px tracking; ar 1440 at 24 px. At 390 it is 20/28, tracked. The words are unchanged.

### Budgets (gzip -9, round 2 → F1)

| Sheet | Before | After |
|---|---|---|
| `main.css` | 31 288 | unchanged |
| `pages/css/fronte.css` | 5 325 | 5 340 (ceiling 6 KB) |
| `pages/css/interior.css` / `pathways/pathways.css` / `ecosystem/ecosystem.css` | 3 290 / 5 089 / 4 925 | 3 350 / 5 130 / 4 988 |
| JS / images | — | none added |

### Tests (database lane l5, one pytest at a time)

- After the merge: frontispiece, page integrity, home, interior W3-F1, cms_nav and imagery gave **274 passed, 1 failed**. The failure is the page-integrity test above, waiting on lane D.
- New in `test_frontispiece_v515_c.py`: `test_the_head_s_layout_follows_the_page_not_the_case_of_the_string` (8 pages × fr/ar) and `test_a_capitals_chapter_title_is_tracked_and_an_arabic_one_is_not_marked` (fr/ar).
- `test_frontispiece_v515_c.py` + `test_content_pages_w3_f2.py`: **130 passed**.
- Under the Chromium lock (09:38–09:42): `test_browser_v515_c.py` + `test_frontispiece_v515_c.py` passed **85 of 85**. The browser part (develop: grey before entry, colour at mid-viewport) is included.

### Requests (carried over; nothing new for the other lanes)

- **Lane A**: adopt the combined zoom+colour rule (end of `v5/_photo.css`) in `_reveal.css`, then lane C deletes its copy. Extend the head hairline and its test to `.fronte-wrap` (FAQ, Glossaire and Vivre were measured again in F1 and still draw none). Add the 21st.dev provenance rows from round 2.
- **Lane D**: translate the four msgids for the page-integrity test; switch `depot.html:78,82` and `terms_required.html:24` to `{% legal_links "terms" %}`. The steward does not merge W3 before both are done.
- **Owner (via the Director)**: the NBSP inside the locked `p3.antifraud.body`. Unchanged.
- **Steward**: Lighthouse on the compressed build (Pilote fr, Formation ar, Contact ar). New slices this round, all in lane C's own files: `templates/pages/partials/_ingresso.html` (`words_first`), `_chapter_head.html` (the capitals class), the cased-letter test in `templates/pathways/training.html` and `_antifraud_callout.html`, one `words_first=True` per head include in `templates/ecosystem/companies.html`, `pilot.html`, `templates/pathways/index.html` and `diplomas.html`.
