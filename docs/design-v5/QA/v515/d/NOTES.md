# V5.15 lane D (label `v515-d-build`): notes — platform design energy, the organisation experience, terminology

- **Branch:** `v515-d`, from `design-v5` at `ece1eeb` (v512 W2 + v516-p2 merged). **Worktree:** `C:/tmp/ile_wt/v515-d`.
- **Database lane:** l6 (`ile_v5_l6`, tests on `test_ile_v5_l6`). **Lane server:** 8786 (launcher outside the repo:
  `C:/tmp/ile_v5_council/.work/v515-d/srv/run_8786.py`; stopped at the end).
- **Binding:** V5.15 (the owner's creative override, §20 «the platform must not collapse into static rectangles»),
  DECISIONS §15 lane D, §16 (carry-over), §9 (terminology), §3 (21st selections: «Contextual cards — Feature Bento
  27082 — a 1 px hairline lattice with mixed cells, no fabricated metrics» is lane D's), §10.0 (shared files).

## §16 carry-over (done first)

- `apps/portal/tests/test_views.py::test_dashboard_for_a_fresh_account_shows_empty_states_not_numbers` — stale since
  the empty-wall collapse (W2, D-20). It now asserts the new calm state as precisely as the old one: exactly one
  «Aucune échéance ni communication pour l’instant.» (`db-empty db-calm`), no «… apparaîtront ici», no head of the
  dates or of the communications, still no figure (`data-count`), no organisation card, the account's name and address.
- The launcher's persona pages (`run_8780.py`) are the **merge steward's** item (§16), not this lane's: nothing outside
  the repository was edited for 8780.

## What the owner sees, and where

| Where (8780 after merge; 8786 now) | What |
|---|---|
| Every console page of the space: «Tableau de bord» (person, company bridge, organisation), «Mes demandes», «Communications», «Mes échéances», «Mon parcours», «Ma situation», «Mes documents», «Mes dossiers», a request, a communication, «Mon organisation» | **The atrium** — the page head is no longer a title on the bare page: one composed sheet (the panels' 8 px corner, a hairline border — never a shadow: the NowPanel stays the screen's one raised plane —, the lagoon's wash and the key's gold wash, the architect's 32 px grid fading toward the words, the key's hairline of light along its foot). On the reading end, the **ILE drawing**: a portico of three arches, the middle one holding the door with its gold keyhole, and the route that comes station by station to that door. **At load** the arches draw one after another (60 ms apart, 900 ms), the route draws (1.2 s), its stations pop, the key's light travels the route once and rests at the door; the keyhole comes to full gold. The eyebrow is the space's name on a short gold rule; the title is set larger (28 → 36 px). Tinted by the space: person (sand), institution (silver), university (sage), company (blue). Mirrored as a whole in Arabic. On a phone the atrium is a full-bleed band (into the 16 px gutter), compact, the portico small and faint behind the eyebrow — it adds no height, so the first piece of «Mes documents» stays above the bottom bar. |
| Person's dashboard, first row (beside the NowPanel) | **The lattice** (21st Feature Bento 27082, adapted): one 1 px hairline lattice of mixed cells — **Avancement**: the checklist's two counts and a ring drawn from them (the arc draws at load; with nothing done, the track alone — never a fake «0 %»); **Où j’en suis**: «Étape 2 sur 7», the step's name, seven ticks (behind in lagoon, here in gold, ahead in paper); then the file's facts (objective, who intervenes), its link «Votre dossier» in the head. A held file (suspended, closed) has no step cell: a place the system does not know is never shown. |
| Person's dashboard, the side column | One lattice: **Mes échéances** with the next date set large (day in ILE Mono, month and year beside it; amber when soon, terracotta when overdue — decorative, the list under it says it with its word) and **Communications**; with neither, **one calm cell** (the dates' glyph on a lagoon disc + the calm sentence). |
| The NowPanel | Its top edge of light (the key's gradient; terracotta when an overdue date takes it over). It is the screen's action: it stands at rest from the first frame (never faded, never moving); the lattice and the side rise beside it, 120 ms in. |
| Organisation dashboard (qa-institution, qa-university) | The head carries the organisation's **identity plate**: its seal (the audience glyph in gold on night, double-ringed) and its name. The calm state is a **composed panel**: two porticoes joined by one route (drawn at load), the calm sentence set as a title, the approved CTA (G2 only). **«Le projet» as tiles**: 01–05 index in Mono, the section's glyph in a squared container, the word, the way on; a tile lifts 2 px with depth under a fine pointer. The identity sheet's disc on night. |
| «Mon organisation» | The atrium; the identity sheet as a lattice cell; «Le projet» as the same tiles. |
| Every lattice cell, tile, calm panel | **The spotlight** (21st Spotlight 35180, adapted): a soft lagoon light that follows a fine pointer across the cell (two custom properties, once a frame); never on touch, never instead of the focus ring. |
| The load envelope | Finite, ≤ 1.7 s, then the page rests: nothing loops and **nothing is scroll-linked** (a `view()` timeline never ends — tried in round 1 and removed: the page was never at rest for its pointer, rows moved under a click). The animations fill `backwards` only, so a finished one leaves `document.getAnimations()`. |
| Reduced motion (setting or `html.rm`) | The **branded still**: the portico, the door, the route and the keyhole drawn complete, the ring at its arc, every plane in place; no light travelling, no rise. The spotlight still answers the pointer (a hover state), at once. |
| Rail, Arabic | The section «Échanges» says «التبادلات» — the duplicate «المراسلات» over «المراسلات» is gone (§9). |

## Files

- `apps/portal/static/portal/v5/_platform.css` (new partial) + `apps/portal/static/portal/platform.css` (new page-only
  entry) → `static/css/dist/portal/platform.css`. Linked by the 13 console templates that draw the atrium, after their
  own sheets. **Never** `main.css`, never `console.css`.
- `static/js/src/platform.js` (new top-level entry → `static/js/dist/platform.js`): the spotlight only; one delegated
  listener per `data-spot-group`.
- `templates/portal/partials/atrium_art.html` (new): the drawing (decorative: `aria-hidden`, `focusable="false"`, no word).
- `templates/portal/{dashboard, dashboard_organisation, organisation, requests, messages, deadlines, pathways,
  situation, documents, request_detail, message_detail}.html`, `templates/cases/index.html`,
  `templates/documents/index.html`: the head's hook `data-atrium="<space>"` (the class strings the tests read are
  unchanged), the drawing's include, the sheet and the module. `templates/cases/index.html` and
  `templates/documents/index.html` are touched in their head only (lane-less files; one hook each).
- `apps/portal/services.py`: `journey_at()` (the current step's rank in the catalogue's words, or None),
  `progress_figure()` (the checklist's two counts and the arc on pathLength 100 — the SVG's own attribute: the CSP
  allows no inline style); `dashboard_context` passes `journey_at`, `progress_figure`.
- `locale/{it,en,ar}/LC_MESSAGES/django.po` + `.mo`: two corrections (below). `docs/I18N_RTL.md` §5: 18 glossary rows
  and the V5.15 note.

## 21st.dev components adapted (rows for `docs/design-v5/COMPONENT_PROVENANCE.md` — lane A owns the file)

| Family | 21st.dev component (id · URL) | Taken | Not taken | ILE implementation | Wave |
|---|---|---|---|---|---|
| Contextual cards (dashboard lattice) | Feature Overview Bento · 27082 · `21st.dev/@mohammadshehadeh/components/feature-10` (MIT, Hirael) | The 1 px hairline lattice (gap 1 px on the hairline colour, one outer radius, cells flat inside) and its mixed cells: a figure cell, a list cell, a wide cell | Its metrics tiles with invented figures (ILE: only the checklist's counts and the journey's rank, both held by the system), its quote/avatar cell, its card components, Tailwind | `apps/portal/static/portal/v5/_platform.css` §2, `templates/portal/dashboard.html` (`.lattice`, `.db-side--lattice`) | W3 |
| Spotlight (cells, tiles) | Spotlight · 35180 · `21st.dev/@kevingirelli/components/spotlight` | The pointer-following radial light written as two custom properties once a frame, touch skipped, the light behind the content in its own stacking context | Its lit edge ring (the cells already have the hairline), its React Slot, any light from the keyboard | `static/js/src/platform.js`, `_platform.css` §5 | W3 |
| Page head (console atrium) | Welcome Banner · 26795 · `21st.dev/@uiable/components/welcome-banner` — reviewed, **principle only** | A dashboard's first widget as a composed banner: words on the reading start, an illustration on the end | Its illustration, its CTA, its copy, its gradient; the drawing is ILE's own geometry (portico, door, key, route) | `templates/portal/partials/atrium_art.html`, `_platform.css` §1 | W3 |
| Progress ring | Circular Progress · 22095 · `21st.dev/@shadcnui-blocks/components/progress-10` — reviewed | An SVG ring on two circles (track + arc), the arc drawn at load | The centred percentage (ILE: never a percentage; the counts are said in words beside it) | `_platform.css` §2 (`.ring`) | W3 |

Reviewed and not taken: Bento Grid 622, 1197, 9594 (shadowed tile grids with hover scale: a SaaS board), Financial
Bento 30742 (charts and invented figures), Spotlight Card 2487 / 2220 (coloured glow, «neon» against V5.15 §18),
Cursor Spotlight 18361 (dims the whole container), Banner 1535 / Gradient Hero 31116 (marketing gradients).

## Budgets (gzip -9 on the built files)

| Asset | Before | After | Note |
|---|---|---|---|
| `static/css/dist/main.css` | — | **unchanged** | not touched |
| `static/css/dist/portal/console.css` | — | **unchanged** | not touched |
| `static/js/dist/shell.js`, `console.js` | — | **unchanged** | not touched |
| `static/css/dist/portal/platform.css` (page-only, new) | — | **3 165 B** | 13 console pages |
| `static/js/dist/platform.js` (page-only module, new) | — | **490 B** | same pages |

Measured in headed Chromium 1234 on 8786 (`motion_probe.py`, final round): **CLS 0** on every probe (person, university
× 1440 / 390 / 390 reduced); **LCP** 148–352 ms (local); the atrium's light animates (`plat-light`) under no-preference
and is `none` under reduce; after scrolling to the foot, **0** sections left below opacity 1 in view. Transform,
opacity and stroke offsets only — no layout property animates.

## Checked by eye (headed Chromium, Chromium lock held)

Shots in `C:/tmp/ile_v5_council/.work/v515-d/shots/` (`base` = before, `r1`–`r3` = rounds, `motion/` = the probe):
person (with a file, the documents persona, a fresh account), institution, university, company dashboards;
«Mon organisation»; the registers' pages; «Mon parcours», «Ma situation», «Mes dossiers»; fr + ar at 1440 and 390,
ar at 390 under reduced motion. **Horizontal overflow at 390: 0 px** on every console page probed (the only overflow
measured, 23 px, is the public 404 page reached by a wrong probe URL — not a console page, not this lane's).
Round-by-round fixes (`r1` → `r4`): the route crossed the lead's words (the drawing now fades in from the words' side, the words
hold 54 %); the tiles' chevron wrapped (four tracks); a ring at «0 sur 5» drew a stray cap (the arc is drawn only
with something done); the facts strip drew a box inside its cell (its padding and box removed inside the lattice); the browser guards then
showed the system's rules the first build broke, and the build was brought back inside them — corners 12 → 8, every
edge a border (no second raised plane), the NowPanel never faded, no scroll-linked motion, a compact head (the desktop
atrium 11 → 8.5 rem; the phone band adds no height).

Self-score against «a premium institutional legal-tech platform»: dashboards and organisation space **4/5** (the
atrium and lattice give the console a composed, branded first screen with real motion; what keeps it from 5 is
outside this lane: the rail's section labels float in tall empty bands — `_shell.css`, lane A).

## Terminology (final catalogue pass for this lane)

- **§9 corrections:** the rail's section «Échanges» → it «Comunicazioni», en «Communications», ar «التبادلات» (was
  «Scambi», «Exchanges», «المراسلات» — the Arabic duplicated the item under it); «Votre rôle» it «Ruolo» → «Il suo
  ruolo» (the «Lei» register of «La sua area»).
- **Glossary rows** (`docs/I18N_RTL.md` §5, from the catalogues, PROVISIONAL for EN/AR — Q3): Échanges, Espace
  Universités et Formation, Espace entreprise, Équipe du projet, Mon organisation, Nature de l’organisme, Votre rôle,
  Votre espace, Le projet, Ma situation, Mes dossiers, Dossier, Votre dossier, Pièce demandée, Guichet numérique,
  Avancement, Où j’en suis, Sécurité du compte.
- **New msgids: none.** Every word this lane draws is already in the catalogue («Avancement», «Où j’en suis»,
  «Étape %(n)s sur %(total)s», the calm sentences). `scripts/i18n_audit.py`: OK, 100 % in it/en/ar/fr (3616 msgids).
- The other lanes' W3 msgids: the merge steward's catalogue pass after A → B → C (as in W2).

## Tests (`TEST_DATABASE_URL=…/test_ile_v5_l6`; browser runs under the Chromium lock)

- **New:** `apps/portal/tests/test_platform_v515_d.py` — **33 tests, all pass**: the atrium on the dashboard (4
  languages; a decorative drawing: `aria-hidden`, `focusable="false"`, no word; one h1; the eyebrow is the space's
  name) and on the registers' pages (sheet and module linked once); `progress_figure` (counts, never a percentage; none
  without a checklist); `journey_at` (the catalogue's words); the file's lattice in 4 languages (ring, «Où j’en suis»,
  7 ticks, one «here», no inline style, no «%»); a ring with nothing done draws its track alone; no ring without a
  checklist; a held file (suspended, closed) has no step cell; the side lattice (the large date decorative, both
  registers, no calm cell) and the calm cell alone; the organisation's identity plate, calm panel and tiles (01…n, one
  per open public page) in 4 languages; «Mon organisation»; the sheet page-only (never in main.css / console.css); the
  motion guarded (no-preference + `html:not(.rm)`, duration tokens, nothing outside the guard, no `infinite`, no
  `animation-timeline`, the NowPanel never animated, no shadow at rest, corners 8 · 4 · full, no `!important`); the
  spotlight module (two properties only, mouse only, no key handler); §9's two terms.
- **Stale tests brought to the new behaviour (no guard weakened):**
  - §16 carry-over `apps/portal/tests/test_views.py::test_dashboard_for_a_fresh_account_shows_empty_states_not_numbers`
    (above);
  - `apps/portal/tests/test_held_file.py` — the head is found by `<header class="ctx db-head"` (it now also carries
    `data-atrium`); same assertions;
  - `tests/frontend/test_dashboard_browser_w3_b.py`, `test_journey_browser_w3_d.py`, `test_documents_browser_w3_c.py`,
    `test_drawer_browser_w3_c.py` — the page is read «at rest» after lane D's FINITE load envelope (`_settle` waits
    only for animations of the atrium and the platform's planes that end within 2.5 s — **never** the journey's).
    Every gate is unchanged: «moving» still refuses any loop, any scroll-linked timeline and any journey motion on a
    return; the primary in the first viewport, one raised plane, ≤ 2 shadows, corners 4/8/full, the first piece above
    the bottom bar, the open row under the pointer.
- **Runs:**
  - non-browser ring (`apps/portal/tests`, `test_dashboard_w3_b`, `test_organisation_space_v512_d`,
    `test_console_shell_stylesheets`, `test_static_pipeline`, `test_frontend_bundle_is_current`, `test_documents_w3_c`,
    `test_case_file_w3_e`, `tests/i18n`): **718 passed** (final). An earlier, wider ring (+ `test_console_shell_w3_a`,
    `test_terminology_v512_d`, `test_layout`, `test_overlays*`, `test_o14_lint`, `test_chips_registry`,
    `test_interior_w3_f1`, `test_icons`, `test_requirement_views`): 1105 passed; its 24 failures all fixed above.
  - browser (`test_dashboard_browser_w3_b`, `test_journey_browser_w3_d`, `test_documents_browser_w3_c`,
    `test_drawer_browser_w3_c`): **79 passed, 5 failed — the 5 fail identically on `design-v5` `ece1eeb`** (run there):
    `test_the_bridge_has_no_raised_plane_no_primary_and_flat_registers` ×4 (expects the bridge's five registers; W2's
    organisation dashboard draws its registers with rows only) and `test_the_one_primary_…[390x844-fr]` (a DRAFT file's
    long state chip wraps to a plate with a 12 px corner).
  - **Not mine, failing on `design-v5` as well** (run there, same database): `test_console_shell_browser_w3_a` ×19
    (the rail's count with the Academy gate, the foot's legal list, the 1366 rail …), `test_console_phone_browser_w3_a`
    ×2 (§16, lane A's), `test_overlays_console_browser_w2_a` ×2 (the Academy entry). For lane A / the steward.
- `ruff check` / `ruff format --check` clean on every touched Python file; `scripts/i18n_audit.py` OK, 100 %; no model
  change, no migration; `npm run build` with the installed packages (no new dependency).

## Requests to other lanes and the steward

- **A** (`apps/portal/static/portal/v5/_shell.css`, the rail): the section labels («Parcours», «Dossier», «Échanges»)
  float in tall empty bands at 1440 — the band's height reads as a gap, not a group. Also: if the atrium should
  become the console's default head, the `@import url("v5/_platform.css")` can move into `console.css` (+3.2 KB on
  every console page) — kept page-only here per V5.8.
- **A** (`docs/design-v5/COMPONENT_PROVENANCE.md`): the four rows above.
- **Steward:** after the W3 merges, the launcher's persona pages for the organisations (§16), and the catalogue pass
  for the other lanes' msgids.

## Not done in this branch

- The case file's own head (`templates/cases/detail.html`, W3-E's composition with its actions) and the Academy's
  console pages keep their heads: the atrium is not forced on a page whose head carries actions until it is designed
  with them.

## Round 1 improvements (label `v515-d-improve1`)

Quality round 1 scored the lane 2.5–4 (evidence: `C:/tmp/ile_v5_council/evidence/v515/d/QA_ROUND1.md`). Every major and
every cheap minor is addressed; measured in headed Chromium 1234 on 8786 (Chromium lock held), probe
`C:/tmp/ile_v5_council/.work/v515-d/improve1/probe.py`, shots in `.work/v515-d/improve1/r1`, `r2`.

| Finding | What changed |
|---|---|
| **Major — the drawing truncated at rest** (non-scaling-stroke + pathLength dash) | `vector-effect: non-scaling-stroke` removed from every dashed stroke (atrium and the organisation's calm panel); it stays only on the undashed grid and stations. The strokes are set in the viewBox's units from the drawing's known scale per layout (`--atrium-sw`: 1.15 desktop, 1.6 at 1024–1279, 2.15 at 768–1023 and beside an action, 5.5 on a phone). The light has `opacity: 0` at rest — no gold stub. **Measured on 384 probes** (16 pages × 8 widths × fr/ar + ar reduced motion): the route's rendered end = the door's centre (0 px on all), the door's right leg inked everywhere (luminance ≤ 81), the third arch's right leg inked (≤ 202 on ~245 paper). Guard: `tests/frontend/test_platform_browser_v515_d.py` (route end vs door; the door's and the arch's right legs carry ink at rest; light opacity 0) at 1440/768/390, no-preference and reduce. |
| **Major — the drawing under the h1 and the lead on phones** | The drawing is no longer an absolute layer behind the words: from 48 rem it is **its own grid column** (words · drawing · action), so no word can lie on it; on a phone the whole drawing is **a 2 rem mark** at the reading end of the head's first lines (the eyebrow and the title stop 6.5 rem before it) — it adds no line. The eyebrow (the space's name, the rail's own word — `portal/partials/atrium_eyebrow.html`) is now on **every** atrium page. **textOverArt = 0 on 384 probes** (was 30 of 32 phone probes). Guard: `test_no_word_of_the_head_lies_on_the_drawing` at the 8 review widths, fr + ar, on the dashboard, a register and the Guichet (with its action). Also fixed on the way: the shell's `.console__workspace > .ctx { padding-block-end: 0 }` left the ContextHeader atria with no foot (the meta row touched the gold hairline) — the atrium keeps its own foot. |
| **Major — coverage: case file, Academy, Guichet, account** | The atrium has an **action slot** (`.ws-head__action` → a third column; the drawing narrows to 15 rem beside it; below 1280 the action goes under the words). Applied to **the case file** (`cases/detail.html`), **the Academy** (catalogue, «Mes formations», a course — with its «M’inscrire» action —, an enrolment, a plan; `academy/base_academy.html` links the sheet and the spotlight module once), **the Guichet numérique** (its list with «Ouvrir une demande», a request, opening a request, the professional's queue, the dispatch; `helpdesk/base_helpdesk.html` links the sheet). The Academy's «Où j’en suis» strip is now **a lattice of counts** (three cells, the count set large in ILE Mono, spotlight). **Account pages** (`compte/profil`, `compte/2fa`): their head is drawn by lane B's account frame (`allauth/layouts/_console.html`, `accounts/profile.html`, allauth's MFA templates) — **request to lane B** below; not edited here (§10.0). |
| Minor — ring at «0 sur 5» read as a spinner | The ring is **segmented**: one segment per checklist item (2-unit gaps on pathLength 100, `portal.services.progress_figure()["segments"]`), done in lagoon, the rest hairline; a continuous arc above 12 items. Done segments fade in at load. |
| Minor — «Étape n sur 7» twice | The step cell is drawn only where the journey is not drawn on the screen (never, today, on the person's dashboard); the file's lattice is now the ring beside the facts (`lattice__grid--file`, 1 : 2). |
| Minor — heights; the university head 290 px at 390 | The atrium has one rhythm: desktop min 8.5 rem, padding 20/16, 24 px to the content (the registers' and the documents' 32 px heads aligned to it); on a phone a band of 8 px padding, the lead at the small size, 16 px to the content — so the eyebrow on every page adds no height to the phone's first screen (the documents' first piece stays above the bottom bar). The organisation's locked presentation is **folded under «Présentation»** below 64 rem (`<details class="atrium__intro">`, the locked text verbatim and once); from 64 rem the summary is hidden and the text shown (`::details-content`, behind `@supports`; without support it stays a disclosure). The university head at 390: **213 px** (was 290). |
| Minor — Mon organisation dead column, orphan gaps | «Mon organisation» takes the workspace: the identity sheet's facts are a 2-column hairline lattice (eyebrow labels); «Le projet» tiles in four tracks (three for 3 or 5 tiles); on the dashboard two tracks, an odd last tile takes the row (no orphan «05»). The ~48 px gap under «Le projet» was a shell flow margin (32 px) on the list — zeroed for the tiles. |
| Minor — tile hover raised a second plane | No lift, no shadow: the border's step and the spotlight (the NowPanel stays the only raised plane). |
| Minor — raw colour, radii, comment | `rgba(195,154,43,.12)` → `color-mix(var(--identity-key) 12%)`; the ticks and the eyebrow's rule `var(--radius-full)`; the drawing's comment names `_platform.css` §1. The sheet test now refuses any `rgba(`, any raw px radius, any `--shadow` value. |
| Minor — motion tied to the Lume | As the key's light reaches the door the **keyhole turns a quarter** (`plat-turn`, `transform-box: fill-box`, 240 ms on `--motion-fast × 2`, `--ease-turn`), once; absent under reduced motion / `html.rm` (the still shows it upright). Envelope still ≤ 1.92 s, finite. |
| Minor — terminology «Comunicazioni» over «Comunicazioni» | Followed the binding §9 table; **escalated to the Director** below. |

**Budgets (gzip -9):** `static/css/dist/portal/platform.css` 3 165 → **4 130 B** (page-only; +0.9 KB for the grid head,
the action slot, the phone row, the counts lattice, the segmented ring, the disclosure); `js/dist/platform.js` 490 B
(unchanged). `main.css`, `console.css`, `shell.js`, `console.js` unchanged. The Guichet and Academy pages now load the
page-only sheet (+4.1 KB gz each). CLS: the head's grid is static; nothing animates layout.

**Tests:** `apps/portal/tests/test_platform_v515_d.py` **51 passed** (new: the segmented ring, the eyebrow on 9
atrium pages, the case file's atrium, the Guichet's action beside the drawing, the Academy's counts lattice, the
folded presentation verbatim in 4 languages, no non-scaling stroke on a dashed path); non-browser ring
(`apps/portal/tests apps/academy apps/helpdesk apps/cases apps/documents apps/ecosystem tests/i18n`, not browser):
**1233 passed, 3 skipped**; browser (`test_platform_browser_v515_d`, `test_dashboard_browser_w3_b`,
`test_journey_browser_w3_d`, `test_documents_browser_w3_c`, `test_drawer_browser_w3_c`, the bundle/pipeline/stylesheet
checks, `test_organisation_space_v512_d`, the lane's own): **218 passed, 5 failed — the same 5 that fail on
`design-v5` and on this lane's previous head** (the bridge's registers ×4, the DRAFT chip's 12 px corner at 390-fr;
recorded in the build notes above). Two regressions this round caught and fixed before the commit: the eyebrow row
pushed the documents' first piece under the phone's bottom bar (360/390) and the drawer's second row out of the 1440
viewport in Arabic — the compact rhythm above brought both back (passing on the previous head and now). Final headed
probe `r3`: **384 probes, textOverArt 0, route end = door (0 px), door and arch legs inked, HTTP 200 on all**.

**Requests:**
- **Lane B** (account frame): give «Mon compte» and the security pages the atrium head — in `accounts/profile.html`
  (`<header class="conto__head">`) and the allauth manage pages' title: `data-atrium="person"`, the two includes
  `portal/partials/atrium_art.html` + `portal/partials/atrium_eyebrow.html`, the page-only
  `css/dist/portal/platform.css` in `extra_head`. The form bodies stay B's.
- **Director** (§9): with «Échanges» → «Comunicazioni» / «Communications», the rail reads the section and its single
  item identically in it and en (the duplicate just removed in Arabic). Either a different section word (it
  «Corrispondenza», en «Correspondence»), or the rail drops a section label equal to its single item (lane A,
  `_shell.css` / rail service). Not changed here.
- **Lane A** (`COMPONENT_PROVENANCE.md`): no new 21st component this round; the ring row (Circular Progress 22095)
  gains «segmented, one segment per item» in the ILE column.

## Round 2 improvements (label `v515-d-improve2`)

Quality round 2 scored the lane 3.5–4 (atrium 3.5, lattice 3.5, motion 4, Q7 3.5, coverage 4, terminology 4). Every
major and the cheap minors are addressed below; measured in headed Chromium 1234 on 8786 (Chromium lock held), probes
`C:/tmp/ile_v5_council/.work/v515-d/improve2/` (`measure.py`, `insp.py`, `motion.py`; shots `r1`–`r5`, contact sheets
`s1440.png`, `s768.png`, `s390b.png`, `s_org.png`, `s_ring.png`, `s_motion.png`).

| Finding | What changed |
|---|---|
| **Major — one portico pasted on ~30 pages; a faint sketch at 1440, a 6 × 2 rem mark on phones, a 15 rem sticker beside an action, an empty wash at 768–1279** | `atrium_art.html` takes a **`figure`** and draws **a composition per family in one grammar** (a ground line, the door with its gold keyhole, the route that reaches it, the light): **route** — the file (dashboard, case file, «Mes dossiers», «Mon parcours», «Ma situation», «Mes échéances»): the journey's **seven stations, the file's own step lit in gold** (`atrium_at` = `journey_at.n`; on the case file the new `journey_rank` filter), the ones behind in lagoon, a pedimented portico at the end; **counter** — the Guichet ×5 and «Mes demandes»: one wide counter arch, its counter, two stations facing across it, the hatch as the door; **thresholds** — the Academy ×5: three thresholds rising step by step; **sheets** — the documents: three sheets standing on a portico's threshold; **exchange** — the communications: two porticoes, the route going from one to the other; **seal** — the organisation's dashboard and «Mon organisation»: the arcade of three arches with the **audience's seal** (double ring + the registry glyph in gold through an SVG `<use>`, mirrored back in Arabic) in the central arch. The drawing is a 360 × 200 box that **fills its column's height** (`contain: size` on the column so it never sizes the head, `xMaxYMax meet`, the route's lead-in clipped at the column's edge); the arcade ink raised 55 → **75 %**. The action now sits **under the words at every width** and the drawing keeps its column beside both (26 rem ≥ 1280, 20 rem 1024–1279, 16 rem 768–1023). **On a phone** the mark is replaced by **the band** (`atrium__band`: the route, seven stations — the file's step lit —, the door with its key), drawn **on the eyebrow's row** from the space's name to the door with CSS anchor positioning (`@supports (anchor-name)`; elsewhere a 2 rem row at the head's foot). Not at the head's foot as the reviewer proposed: a 40 px foot row pushed the documents' first piece under the phone's bottom bar (`test_documents_browser_w3_c`, 4 failures measured) — on the eyebrow's row it adds no height and the gate holds. **Measured, 208 probes** (13 pages × 8 widths × fr/ar): ink ≥ 60 % of the head's height on every probe ≥ 768 (min 0.61, typically 0.70–0.80; was 0.19–0.63), no overflow, HTTP 200 everywhere. Guard: the browser test now asserts ink ≥ 60 % at ≥ 768 on the dashboard, a register and the Guichet in fr/ar, and checks the band on phones. |
| **Major — the eyebrow showed the fallback «Espace réservé» on 12 of 19 pages** | The word is resolved from the **account**: `portal.services.atrium_space_label()` (the organisation's space name for an institution/university — the organisation dashboard's eyebrow —, else `roles.space_label`, the person dashboard's) through a new tag library `apps/portal/templatetags/atrium.py` (`{% atrium_space %}`). The include parameter is renamed **`atrium_label`** (no context leak); the dashboards no longer pass one. «Mon organisation»'s eyebrow carries `atrium__eyebrow`. **0 fallback on 208 probes.** Tests: every atrium page's eyebrow equals the dashboard's in fr/it/en/ar (person) and an organisation's pages say its space (4 languages). |
| **Major — the 0/5 ring read as a loading spinner** | Undone segments are a **1.5 hairline track** (`--line-structure`: on the sheet `--line-rhythm` measured too faint to read as a track), done segments the full 5 in lagoon; the **count stands in the ring** (`0/5`, ILE Mono, the total in `--text-3`; decorative, the words beside it say it) — a dial. 21st reviewed: Circular Progress (diceui) 24462 (track · range · value-text parts — the composition taken, its percentage not). Browser guard: no undone segment wider than 2, the count centred in the ring. |
| **Major — the «Présentation» chevron sideways in Arabic** | The L of the two logical borders has its corner at the inline end; Arabic now rotates the other way (`-45deg` / `-225deg`), so the corner points down closed and up open in both scripts (physical borders were refused by `test_rtl_static`). Browser guard: the transformed corner's vector, fr and ar, closed and open. |
| **Major — Q7: ~70 px void before «COLLABOREZ AVEC NOUS», orphan tile 05 at 768–1023** | Two causes found by measure: the main column was stretched to the side column's height and its auto rows shared the surplus (`align-content: start`), and the shell's flow rule gave the register's list 32 px above and below (`margin-block: 0` in the organisation's registers). The CTA is pulled to **16 px under the last row, on the reading end** (under «Toutes mes communications»). The tile rules are a **container query** on «Le projet» (one track; two from 34 rem with an odd last tile taking the row; four/three on «Mon organisation» from 60 rem): **05 takes the row at 768**. Measured: last row → CTA = 16 px at 1440 and 768. |
| Minor — account / 2FA heads | Still lane B's files (§10.0); the request stands below. |
| Minor — the Guichet head 245–265 px on phones | The head's lead is the first sentence («Poser une question à une personne, pas à une machine.»); the second (catalogue copy, not locked) opens the page's closing clause. The existing translations split at their own full stop in it/en/ar (no new wording); `i18n_audit` 100 %, 3617 msgids. Guichet head at 390: **153 px** (was 293 in r1 of this round, ~255 at the review). |
| Minor — Academy counts looked interactive | Each cell is the way to its register on «Mes formations» (`#mine-ongoing-title`, `#mine-done-title`, `#mine-plans-title`), the whole cell the hit area, its focus ring the cell's (`:has(:focus-visible)`), a glyph in the squared container (book-open, history, map — list-checks is reserved to the person’s own choice, O14). |
| Minor — keyhole drawn sideways before its turn | `plat-key` starts at opacity 0: the key appears with the light, then turns. |
| Minor — it/en «Comunicazioni»/«Communications» over its single item | Unchanged: the Director's decision (escalated since round 1). |

**Motion** (headed, no-preference, frames at 250/700/1300/2100 ms, `s_motion.png`): the arcade draws, the route and its stations come, the light travels to the door, the keyhole appears and turns; at rest by ~1.6 s, `0` atrium animations left (1440 and 390 ar). The band tells the same story on a phone. Reduced motion: the branded still (the drawing complete, the step lit).

**Budgets (gzip -9):** `static/css/dist/portal/platform.css` 4 130 → **4 640 B** (page-only, +0.5 KB: the figures' rules, the band, the dial, the linked counts, the container query); `js/dist/platform.js` 490 B (unchanged); `main.css`, `console.css`, `shell.js`, `console.js` unchanged. The figures add markup only to the pages that draw them (one figure per page, ~1.5 KB of SVG).

**Tests (lane l6):** `apps/portal/tests/test_platform_v515_d.py` **70 passed** (new: eyebrow = dashboard in 4 languages, organisation's space, one figure per family, the route lights the file's step on the dashboard and the case file, the seal's glyph, the Guichet's short lead and clause, the Academy's linked counts, the dial's count); `tests/frontend/test_platform_browser_v515_d.py` **16 passed** (ink ≥ 60 %, band on phones, every figure complete at rest on 5 pages at 1440/1024/768 × motion/reduce, hairline ring, chevron fr = ar); `test_documents_browser_w3_c` all pass (after the band moved to the eyebrow's row); `test_dashboard_browser_w3_b`, `test_journey_browser_w3_d`, `test_drawer_browser_w3_c`: the **same 5 failures as `design-v5` and the previous head** (the bridge's registers ×4, the DRAFT chip's corner at 390-fr), nothing new. Non-browser ring (`apps/portal/tests apps/academy apps/helpdesk apps/cases apps/documents apps/ecosystem tests/i18n` + the icons, O14, static pipeline, bundle, stylesheets, organisation-space and terminology checks): **1437 passed, 3 skipped, 2 failed** on the first run — `test_rtl_static` (the chevron's physical borders: now logical borders with an RTL rotation, the browser guard reads the corner's direction) and `test_o14_lint` (`list-checks` is reserved to the person's own choice: the plans' glyph is `map`) — both fixed and re-run green (244 passed with the lane's file); browser guards re-run **16 passed**.

**Requests (unchanged from round 1):**
- **Director / W3 merge plan:** assign the account and 2FA heads (`accounts/profile.html`, the allauth manage pages — lane B's files) explicitly to lane B or D; the change is the two includes + the page-only sheet (`figure` may stay default).
- **Director (§9):** the it/en section label equal to its single item.
- **Lane A** (`COMPONENT_PROVENANCE.md`): add Circular Progress · 24462 · `21st.dev/@diceui/components/circular-progress` — taken: the dial's parts (track, range, value text at the centre); not taken: percentage, indeterminate state, React; ILE: `_platform.css` §2 `.ring-dial`, `templates/portal/dashboard.html`.

## Finishing round F1 (label `v515f-d-improve1`)

Round 3 scored the lane 3.5–4: atrium 4, dashboards and lattice **3.5**, motion 4, Q7 **3.5**, coverage 4, terminology 4.
First, `design-v5` (`7f2a02d`, lanes P2/P3) was merged into the branch. The merge had no conflicts and no migrations, and the
compliance lanes' guards are untouched. Every major and minor of round 3 was then addressed. Checks were done in headed
Chromium 1234 on 8786 with the Chromium lock (noclobber, label `v515f-d-improve1`, held only while a browser was open).
Probes and shots are in `C:/tmp/ile_v5_council/.work/v515-d/f1/` (`shot.py`, `insp.py`).

| Finding | What changed |
|---|---|
| **Major: the side identity card split words and dates at 1024–1280** («Responsabl\|e», «28.10.202\|6») | Every page that draws the identity sheet (`org-id--lattice`: the organisation's dashboard, «Mon organisation», the company's dashboard) now shows its facts as a **lattice of cells**. In each cell the label is an eyebrow over its value. The number of columns depends on the **sheet's own width** (`container: org-id`): two per row from 21 rem, one below. It no longer depends on the viewport, and the 64 rem media rule was removed. A value breaks only between words (`overflow-wrap: break-word`). A date never breaks and is set in ILE Mono (`.org-id__fact time`). A web address may still break anywhere. Guard: `test_the_organisation_and_company_heads_fill_their_column_and_no_fact_splits_a_word` measures one Range per word at 1440/1280/1024/768 in fr and ar, on the institution, university and company dashboards. |
| **Major: the company persona's dashboard was a bare list under the atrium** | The company has its own composition, built from the organisation's patterns. **Atrium:** `data-atrium="company"` (the company wash) and the **seal figure with the company's glyph** (`icons.AUDIENCE["company"]`). **Main column:** registers with rows. With none, the **calm panel** (the two porticoes joined by one route), whose primary way on is «Espace entreprise». **Side:** the **identity sheet** with a seal on night, the name, and the facts lattice. «Mon compte» is folded in as the sheet's foot (once). With registers present, «Espace entreprise» becomes the sheet's foot action. Data: `portal.services.dashboard_context()["company"]` = `organisation_identity(user)` + glyph (member_of, deny by default). Every word comes from the catalogue. `organisation.css` is linked by this page only. The calm drawing is one partial, `portal/partials/calm_art.html`, shared with the organisation dashboard and the empty communications register. |
| Minor: the counter's route ended 27–40 px under the door | The route and the light climb onto the counter (`… H58 C66 190 64 148 74 148 H164`) and reach the hatch's threshold. Guards: the static `test_every_figures_route_and_light_arrive_at_the_doors_threshold` (all 7 figures, x between the door's legs, \|Δy\| ≤ 2), and in the browser `routeEndVsThreshold` ≤ 2 px on the five figure pages × 3 widths × motion/reduce. |
| Minor: phones showed the same 7-station journey on every family, station 1 «done» with no data | The band draws **the family's own motif** before the door: the file's seven stations and its step (route), two facing stations over the counter, three rising thresholds, two sheets, a second door (exchange), the seal's ring, and two arches (default). A station is «done» **only from the file's data** (`atrium_at`). The stations moved clear of the band's fade mask. Test: `test_the_phones_band_draws_the_familys_motif_and_never_a_done_station_without_data`. |
| Minor: the gold «here» station was illegible | It is drawn larger (r 6.5, paper halo 3) inside a **1 px gold ring** (`.atrium__halo`, r + 4; the band's r + 2). The ring answers once as the key's light passes (`plat-halo`, `--motion-fast × 3`, delayed by the station's place on the route via `data-at`). This stays inside the finite envelope and is absent under reduced motion. |
| Minor: two focus rings on an Academy count | `.lattice__cell--link .lattice__go:focus-visible { outline: none }` now wins over the shell's link outline. Browser guard: `test_an_academy_count_takes_one_focus_ring_the_cells` (keyboard Tab, link `none`, cell `solid`). |
| Minor: the organisation's CTA floated alone between two sections | With registers present, the approved CTA is **the identity sheet's foot action**, at full measure. With none, it stays in the calm panel. The `.org-act` row and its rules are gone. |
| Minor: the company's eyebrow «ENTREPRISE» broke the «Espace …» pattern | `atrium_space_label` gives a company **«Espace Entreprises»** (`COMPANY_SPACE_LABEL`), the public space's name. It is already translated in every catalogue (it «Area Imprese», en «Enterprises Area», ar «فضاء الشركات»), so there is no new msgid or translation. Tests: dashboard and communications in 4 languages. |
| Minor: organisation heads below 60 % ink at 768–1023 (0.54–0.59) | At 768–1279 the seal column takes 2 rem more on `[data-atrium]:has(.atrium__intro)` and `[data-atrium="company"]` (18 / 22 rem). Both organisation dashboards and the company's are now in the ink guard (≥ 0.6 at 1440/1280/1024/768, fr + ar). |
| Minor: the empty Communications page (icon, heading, sentence, ~500 px of nothing) | The **calm panel** with the exchange's two porticoes and the register's own words («Aucune communication», «Les messages que l'équipe vous adresse apparaîtront ici.»), `role="status"`, drawn once at load. |
| Found on the way: «Mon compte»'s links on a ruled row of their own on every dashboard | The base sheet's `ul[role=list]` (32 px margin + hairline) outweighed `.db-account__links`. Fixed with `.db-account__links[role="list"] { margin: 0; border: 0 }` in the page-only sheet. |
| Lane C's carry-over M-2 / m-12 (merge blocker) | `templates/documents/partials/depot.html` (×2) and `templates/documents/terms_required.html` now link the Conditions only through `{% legal_links "terms" %}`, so nothing points to a 404 while the gate is closed. Test: `test_the_deposits_gate_links_the_terms_only_when_they_are_published`. |

**Not done here (requests):**
- **Lane C → D catalogue pass:** «Le même geste», «Autres voies» and «N parcours affiché(s)» (lane C's W2 msgids) do not exist on this branch, so they cannot be translated here. They must be translated in the W3 catalogue pass after lane C merges. Until then `tests/i18n/test_page_integrity.py::test_latin_text_on_arabic_pages_carries_its_own_lang_attribute` fails on v515-c, and the steward treats that as a merge blocker.
- **Director / W3 merge plan:** the account and 2FA heads (lane B's files). This is unchanged since round 1.
- **Director (§9):** the it/en rail section label equals its single item. Unchanged.
- **Lane A (`COMPONENT_PROVENANCE.md`):** Circular Progress · 24462 (unchanged from round 2).

**Budgets (gzip -9):** `static/css/dist/portal/platform.css` 4 645 → **4 998 B** (page-only; +0.35 KB for the container lattice, the band motifs, the halo, the calm register and the foot). The company dashboard
now also links the page-only `organisation.css`. `main.css`, `console.css`, `shell.js`, `console.js` and `platform.js` are unchanged.

**Headed check** (Chromium 1234, lock held, viewport shots `f1/z-*.png`, `c2-*.png`): the company at 1440 ar / 390 fr reduced
motion; the institution at 1280 ar and 768 fr; the university at 1024 fr reduced motion; the person's dashboard at 390 ar and
1440 ar reduced motion (the halo ring on step 1, the band's stations clear of the fade); the Academy at 390; the documents at
390 ar; empty Communications at 1440 fr and 390 ar reduced motion. HTTP 200 everywhere and no horizontal overflow.
Note: a Playwright `full_page` screenshot after the envelope shows the seal figure blank (a capture artefact; the same page in a viewport shot
and the geometry probe show the drawing complete). The browser guards read the page itself.

**Tests (lane l6, `test_ile_v5_l6`):** `apps/portal/tests/test_platform_v515_d.py` **93 passed** (+23: company
composition in 4 languages, company eyebrow, every figure's route on its threshold, the band motif per family, no
done station without data, the halo, the organisation CTA in the sheet's foot, the calm communications register, the
lattice's container rules, the Dépôt's terms link). `tests/frontend/test_platform_browser_v515_d.py` **21 passed** (+5:
organisation/university/company heads ink ≥ 0.6 and no fact splitting a word at 1440/1280/1024/768 fr+ar; one Academy
focus ring; route end on the door's threshold on 5 figure pages × 3 widths × motion/reduce). Non-browser ring
(`apps/portal/tests apps/documents apps/companies apps/legal tests/i18n`): **920 passed, 1 failed**:
`test_views.py::test_company_account_sees_its_organisation_card` read the old bridge card. It now reads the company's identity sheet
(same assertion: the organisation's name and city), and it is green with `test_platform_v515_d` (128 passed). Browser:
`test_documents_browser_w3_c` all green; `test_dashboard_browser_w3_b` + `test_organisation_space_v512_d`: the
**same 5 failures as design-v5 and the previous heads** (the bridge's registers ×4 on an institution, which now has its own
dashboard; the DRAFT chip's 12 px corner at 390-fr). `test_the_consoles_empty_state_spans_the_main_column` now accepts
the calm panel (`:is(.empty-state, .reg-calm)`, same rule: it spans the main column) and passes. Ownership of that test is W3-B's
file and is recorded for the steward.

## Finishing round F2 (label `v515f-d-improve2`)

**Merged first:** `design-v5` at `10b268d` (lanes P2/P3, lane A's portico sheets). The only conflicts were the four
binary `.mo`; the `.po` merged clean and the `.mo` were recompiled from them (`scripts/i18n_audit.py --compile`:
3 616 msgids, 100 % in it/en/ar/fr, no error). The compliance lanes' guards came in untouched.

**M-1 (major, motion) — the gold station's beat drawn off its place.** `plat-pop` and `plat-halo` animated
`transform`, which on an SVG element REPLACES its `transform` attribute while the animation runs: each station popped
36 units off its rest (−36 on the figure, +30 on the band) and jumped back, and the ring's whole answer was drawn
around station 3 (station 1 on the phone's band). Two changes, each sufficient alone:
- the keyframes animate the individual `scale` property (0.6 → 1; ring 0.4 → 1.35 → 1), which composes with any
  transform;
- the translate moved from every circle to its parent `<g>` (`atrium_art.html`: the stations' group and a group
  around the ring, on the figure and on the band), so no animated element carries a transform attribute at all.
Measured in headed Chromium on 8786, every animation frame for 2.6 s from commit (≈600 frames, ~49 inside the ring's
beat): the ring's and the gold station's centre never leave the station's rest centre — worst 0.0001 px — at 1440 and
390, fr and ar. Reduced motion: 0 running atrium animations, the still image unchanged.

**m-1 — the university's seal at 0.54–0.56 of its head (1024).** The space's locked presentation now opens in the head
from **80rem** (it was 64rem); at 1024–1279, as below, it is folded under «Présentation» (the text verbatim, only
folded). The university's head at 1024 drops from 281–294 px to 205 px (218 ar); its ink is **0.786** (fr/it/en) and
**0.79** (ar) at 1024, 0.69–0.73 at 768, 0.79–0.80 at 1280/1440. Every organisation and company head is ≥ 0.6 at
1440/1280/1024/768 in the four languages (48 loads). The browser guard reads fr, **en** and ar.

**m-2 — the band 100 px beside a long space name (360–375).** The eyebrow's anchored measure leaves the band **10rem**
(it was 7rem): the band is **148 px** at 360/375/390 for «ESPACE UNIVERSITÉS ET FORMATION» (two lines, as before),
162–177 px in Arabic; no overlap with the eyebrow, no horizontal overflow, across the four personas × three widths ×
four languages. The seal motif and the door read as drawings again (`shots/band-qa-university-360-*.png`).

**m-3 — the Academy count's pale second box.** `box-shadow: none` joins `outline: none` on the label link's
`:focus-visible`; computed: outline none, box-shadow none, the cell's ring solid. The browser test now asserts the
box-shadow too.

**m-4 — the company's head («ESPACE RÉSERVÉ» and a lead that speaks to a person): not changed, recorded.** Both are
the locked access-point wording (`p3.reserved.title` / `p3.reserved.body`, rendered only through `{% locked %}`), so the
lane may not swap them. **Request → Director (§9 pass):** decide whether the company's dashboard keeps the prescribed
access-point title and body or takes the organisation dashboards' «Tableau de bord» and an existing organisation lead
(no new copy, no machine translation needed: both msgids exist).

**Tests (lane l6).** `tests/frontend/test_platform_browser_v515_d.py`: new
`test_the_gold_stations_pop_and_its_ring_stay_on_the_station` (the ring and the station restarted, paused and sampled
at 20/60/90 % of their beat, each within 1 px of the station's rest centre; 1440 and 390; fr and ar); the Academy focus
test checks box-shadow; the organisation ink guard reads en as well.

The full non-browser ring (`apps/portal/tests tests/i18n tests/frontend`, 2 926 tests, 43 min) found lane D debts from
the earlier rounds that the targeted runs had not read; fixed here:
- `test_script_motion_gate`: `platform.js` called `requestAnimationFrame` itself — it now takes the gate's
  `nextFrame()` (`static/js/src/motion.js`; the existing shared chunk, no new request);
- `test_v5_tokens` (no literal colour outside the token sheets): the masks read `black`, the print rule `CanvasText`;
- `test_css_tokens_exist` / `test_design_docs` unknown token: `--spot-x` / `--spot-y` are declared on `[data-spot]`
  (the cell's centre) and written inline by the module;
- `test_icons` and `test_design_docs::test_usato_in_minimum_counts_are_true`: the empty-state caller floors (15 → 14,
  «almeno altri 12» → 11) say why — the empty Communications register is the calm panel since F1;
- `test_journey_w3_d` (4): the dashboard's journey section carries `data-rise`; the sheet-order checks read the
  journey's / situation's sheet before lane D's `portal/platform.css`, which every atrium page links last;
- `test_dashboard_w3_b::test_the_bridge_says_where_the_accounts_work_lives_in_the_rails_words`: a company with nothing
  due finds «Espace entreprise» as the calm panel's one primary (F1), same words and link.
Left failing, **not lane D's** and identical on `design-v5` `10b268d` (measured on a detached worktree, then removed):
`test_cms_nav` portico panels, `test_login_invitation_w4_d` ×3, `test_nav_sheet_w2_c2` account popover,
`test_service_pages_w3_f2` ×12, `test_mobile_rtl_w4_a` 500 semicolon, `test_o14_lint` (`partials/header.html` «check»).

**Results (lane l6):** browser — `test_platform_browser_v515_d.py` + `test_documents_browser_w3_c.py` **50 passed**
(under the lock, 13:15–13:21); non-browser — the lane-touched files (`test_platform_v515_d`, `test_journey_w3_d`,
`test_dashboard_w3_b`, `test_icons`, `test_design_docs`, `test_v5_tokens`, `test_script_motion_gate`,
`test_css_tokens_exist`, `test_css_bundle_is_current`) all green except the one gradient rule below.
Budgets: `platform.css` and `platform.js` stay page-only; `platform.js` imports the existing motion chunk.

**Request → Director / steward (DS 2026 vs V5.15):** `test_design_docs::test_conforming_app_stylesheets_use_only_design_tokens`
forbids any `gradient(` in an app stylesheet; `_platform.css` carries eleven — the atrium's wash, the band's and
the figure's edge masks, the spotlight — all from V5.15's brief and accepted by three reviews. Decide: either these
become token values in a `static/css/v5/` sheet (lane A, §10.0), or `_platform.css` is listed in
`KNOWN_NON_CONFORMING_APP_STYLESHEETS` with its §2.1 row. Lane D did not move them into a shared sheet on its own.

**Evidence:** `C:/tmp/ile_v5_council/.work/v515f-d-improve2/` (`probe.py`, `probe.json`, `probe.log`, `shots/`),
headed Chromium 1234 under the lock (taken 11:50, released at the end of the probe).

**Requests carried (unchanged):** the Mon compte / 2FA atrium heads (lane B's files, Director's assignment); the it/en
rail label equal to its single item (Director §9); Circular Progress · 24462 in `COMPONENT_PROVENANCE.md` (lane A).

**Ownership (for the steward, §10.0):** this round wrote, intent kept, in files other families own: the floor and its
comment in `tests/frontend/test_icons.py` (w1-b; the steward's earlier floor write), the company branch of
`test_dashboard_w3_b.py::test_the_bridge_says_where_the_accounts_work_lives_in_the_rails_words` (w3-b), `_sheets()` and
the dashboard's section split in `test_journey_w3_d.py` (w3-d), and the empty-state «Usato in» floor in
`docs/design/DESIGN_SYSTEM_2026.md` §10 (w3-e's line). Each is the consequence of lane D's own F1 change; please confirm at
the W3 merge.

## Finishing round F1 (W3 finishing pass, label `v515f-d-improve1`)

Binding: the F2 review (`C:/tmp/ile_v5_council/workflows_v515/d_state.json`): one major (the seal glyph in Arabic),
atrium at 3.5, every other family at 4.

**Merge first.** `design-v5` `9e65841` (lanes B and C) merged into `v515-d` (`b7aef0b`). Conflicts: the four `.mo`
(recompiled from the merged `.po` with `scripts/i18n_audit.py --compile`: 3 650 msgids, 100 % in it/en/ar/fr, no
error; no locked text touched, nothing machine-translated) and
`tests/frontend/test_dashboard_browser_w3_b.py::test_the_consoles_empty_state_spans_the_main_column`, where lane B's
rule (the empty state on the start edge, at the reading measure, with no surface) met lane D's calm panel on
«Communications». Both are kept: lane B's start edge holds for both, lane B's measure and no-surface rule for
`.empty-state`, and lane D's `.reg-calm` spans the main column.

**M-1 (major), fixed: the seal glyph in Arabic.** The cause was the RTL counter-flip
`[dir="rtl"] .atrium__glyph-icon { transform: scaleX(-1); transform-box: fill-box; transform-origin: center }`.
Chromium resolves a `<use>`'s fill-box without its x/y, so the origin was about 7.9 px 5.6 px. That threw the glyph
about 150 drawing units out of its seal: the university and institution seals were empty, and the company's head had a
stray gold mark. The fix takes CSS out of the mirror. In Arabic the `atrium_glyph` tag
(`apps/portal/templatetags/atrium.py`) wraps the `<use>` in `<g class="atrium__glyph-flip"
transform="matrix(-1 0 0 1 2·x+size 0)">`. This is the mirror about the glyph's own centre, in the drawing's units
(320 for the seal at 150/52/20). The CSS rule is gone (`v5/_platform.css`; `npm run build`, `portal/platform.css`).
The French markup is unchanged.

**Atrium raised to 4.** The 3.5 came from the major alone. The F2 review praised the figures, the motif per family on
the phone band, the legible «here» station and the 148 px band. Now the audience glyph, which is the point of the
organisation figure, stands in its seal and reads the right way round in every direction:
- measured in headed Chromium on 8786 for the university, institution and company personas, fr and ar, at 1440, 1024
  and 768, with motion and under reduced motion;
- the glyph's box centre sits 0.0–0.5 px from the seal ring's centre;
- the net screen transform is not mirrored (`a` > 0 in ar);
- 0 px horizontal scroll and 0 animations running after the envelope;
- at 390 the band is drawn, with no glyph by design.

Shots: `C:/tmp/ile_v5_council/evidence/v515/d/f1d-head-*.png`. Probe:
`C:/tmp/ile_v5_council/.work/v515f-d-f1/probe.py`. The lane server was restarted: it runs `--noreload`, and before
the restart it still served the old tag.

**Guard.** New: `tests/frontend/test_platform_browser_v515_d.py::test_the_seals_glyph_stands_in_its_seal_in_every_direction`
covers 1440, 1024 and 768 × institution, university and company × fr and ar. It checks that the glyph's centre is
within 2 px of the M160 62 ring's centre, inside the drawing, and not mirrored.

**Tests (lane l6, `test_ile_v5_l6`).**
- Browser, under the Chromium lock (taken 14:49, released 15:00): `test_platform_browser_v515_d.py` **26 passed**,
  and `test_dashboard_browser_w3_b.py -k empty_state` **1 passed**.
- Non-browser: `apps/portal/tests/test_platform_v515_d.py`, `tests/frontend/test_design_docs.py` and
  `tests/i18n/test_rtl_static.py` give **236 passed, 2 failed**. Neither failure is new:
  - the gradient rule (m-6 below);
  - `test_rtl_static[static/css/v5/_fronte.css]` (`text-align: right`): lane C's file, already recorded as
    pre-existing on `design-v5` in DL54-173.

**Minors left open (not lane D's) and requests.**
- **m-5 → Director §9:** the company's locked «ESPACE RÉSERVÉ» h1 and the person-facing lead appear in French on the
  it/en/ar company dashboards (`p3.reserved.*`, locked). Lane D does not change locked copy. Options: keep the strings,
  or use the translated «Tableau de bord» h1 and an existing organisation lead, as the institution and the university
  do. No new machine translation.
- **m-6 → steward/Director:** `test_conforming_app_stylesheets_use_only_design_tokens` is red, with 11 gradients in
  `_platform.css`. Unchanged; see the request above.
- **New → Director / lane B:** «Communications» with no messages shows lane D's calm panel (a quiet surface across
  the main column). Lane B's merged guard wants a surfaceless statement at the reading measure. The test keeps both
  rules for now. Decide which one governs on platform registers.
- **Carried:** the Mon compte / 2FA atrium heads (lane B's files); the it/en rail label; the Circular Progress
  provenance row (lane A).

**Ownership (§10.0):** this round wrote the merge resolution in `tests/frontend/test_dashboard_browser_w3_b.py` (w3-b's
file, the empty-state test). Both rules are kept as described above. Please confirm at the W3 merge.
