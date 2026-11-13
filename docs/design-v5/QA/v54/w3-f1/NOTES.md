# W3-F1 · The doors, the project pages and orientation — step 1/2: THE DOORS AND THE PROJECT PAGES

Implementer `w3-f1-impl-1` · 11 October 2026 · V5.5 delivery mode (implement → review once → fix → ship) on V5.4's
decisions · plan `docs/design-v5/V5_4_EXECUTION_PLAN.md` §3.5 item 1, §1.18 D26, §1.4, §1.16, §1.3, §1.7, §2 ·
branch `v54-w3-f1` (worktree `C:/tmp/ile_wt/v54-w3-f1`), from design-v5 `0c4cc46` · lane 7: `127.0.0.1:8787`, database
`ile_v5_l7`, `ILE_REFERENCE_DATE=2026-10-03` (gate G3 open, the Forum in permanent mode, public forms open by the
administrative derogation) · evidence `C:/tmp/ile_v5_council/evidence/v54/w3-f1/` (E/ below).

## 1. What the pages are now

**One grammar for the public interior** — `static/css/v5/_interior.css` (a page partial, plan §2.3: never in
`main.css`), the home's chapter grammar under the hero carried into every interior page, and three page partials in
`templates/pages/partials/` (W3-F1's glob):

| Part | What it draws | Where |
|---|---|---|
| the trail | the breadcrumbs at 13/20, the current page in ink, the chevrons in the quiet ink | `_interior.css` §1 (scoped to `.interior`: W3-F2's pages keep §9 until their run) |
| the entrance «l'ingresso» | the space's name, the h1 and the lead, verbatim, at the reading edge (36/44 from 48rem, 28/36 on a phone; a prescribed title in capitals tracked as capitals); the end seat holds the page's picture: a curated photograph with its caption and credit (D26), else the door card drawn «la porta», else «Sommaire de la page» | `_ingresso.html`, §2 |
| «la porta» | the portico's door card (W2-C1, `v5/chrome.css` §5) with its photograph replaced by a drawing: the night plate, the brand's three steps lit in the door's tint (a 2 px top edge over a face at the tint's 14 %; the arris's one seat is a night plate, §1.4), the audience glyph once on the 36 px night disc at the bottom-start corner (BI04), the door's accent as a 3 px rule along the foot. Decorative (`aria-hidden`): the h1 names the door. The stair never mirrors (Q8); the disc moves with the inline start | §2 |
| the chapters | one section device at the reading edge — the mark's steps (`ile-steps`), the title (28/36), the lead — four columns of twelve and sticky from 75rem, above the body below; 48 · 64 · 96 px; hairlines between chapters on one ground; the stone for the action and the form | `_chapter_head.html`, §3 |
| the register | rows on shared hairlines, the title over its text, the whole row the target (one tab stop), no glyph and no arrow — except where the glyph says WHO (the audiences, the actors: the registry's, once a row) | §4 |
| «la linea» | a real sequence on a level line: numerals over open stations (outline = open — nothing on this site settles a step), the words under them; down the reading edge on a phone and in a pathway's sheet, across its column elsewhere | `_linea.html`, §5 |
| D26's slots | one inset (a notice) · one action (the action card of `v5/card.css`, the raised panel of its screen) · an authority's host beside its link · a caption and a credit under every photograph · «who can help me» with live text only (`Besoin d'aide ? Écrivez-nous :` + the site's address — an existing catalogue string, translated in it/en/ar) | §6 |
| what is being verified | said in words on a broken (dashed) edge — the «attesa» register's sign — never a glyph in a box | §6 |
| Arabic, forced colours, print | a French prescribed text keeps its own direction on the Arabic page (end-aligned in a head, its own alignment in a body, as on the home); the plate and the disc keep an edge under forced colours | §7 |

**The pages** (each with its ar twin; the chain of questions, RH-6, in brackets):

- **/parcours/** — the person door (what is this space?) → the eight pathways as a register (which ways exist?) → «Comment ça marche» as the statement beside the questionnaire, the page's one action (how does it work, where do I start?) → the space's other areas, the anti-fraud callout as the one inset, «who can help me» (where else, and who can help?). The interim page (gate G3 closed) takes the same grammar: the two moments on the line.
- **/parcours/<clé>/** (the sheets) — the entrance holds the order («Parcours régulier 1/8»), the locked title and description, the metadata row (no glyph) and the page's index; one chapter per section; the steps on the line down the reading edge; the authorities with their host; «Termes utiles» in one row; the questionnaire as the one action.
- **/entreprises/** — the company door → «Trois temps, une même démarche»: the prescribed quotation as the statement and the three moments on the line → «Recueil des besoins»: the enquiries app's own form on the stone (the one action) with the single-address line → the transparency notice (the one inset, gate G3) → «Pour aller plus loin».
- **/institutions/**, **/universites-et-formation/** — the door → the recipients as a register of words (the verbatim sentence visually hidden, as before) → the prescribed button on the action card, «who can help me» → «Pour aller plus loin». The universities' sentence is said once (RH-5): its presentational breakdown into «Acteurs» / «Domaines» — the same words a screen below — left the page.
- **/projet-pilote/** — the entrance → the eight prescribed stations on one level line across the whole column (four a row from 48rem, eight from 80rem), the notice right after it (the one inset) → the action card (one primary: the companies' interest; the institutions' way as its secondary) → «Pour aller plus loin». `pilot-flow.svg` (a growth curve ending on a gold node) retired, CREATIVE_DIRECTION_V5 §19.
- **/forum/** (+ inscription, confirmation) — the entrance on the night ground, the page's one night chapter above the footer's (RH-8), with the page's index in the end seat → the prescribed sections as chapters (capitals in the copy, tracked) → the programme as a document (PX15) → the tribune as a register (PX16) → the permanent sections as registers (a photograph only with its caption) → «Participer et collaborer», the one action (one primary). Registration and confirmation: the entrance, one chapter at the reading measure.
- **/le-projet/** (and, sharing its base, /agami/, /reseau/, /contact/, /attention-aux-fraudes/) — the entrance (the name drawn once, as the h1, by the wordmark's own class) → «En bref» → why → who carries it → the four spaces as a register whose glyph says which audience → the mark, quiet. No side column on any interior page: the sibling spaces and pages are the chrome's doors («Il portico»), and a page does not repeat its chrome.

## 2. Decisions met during the build (DL54-78, DL54-79 — renumber at the merge)

1. **Imagery (§1.16): no approved frame is left for any door's lead.** Every audience frame in the repository is that
   audience's navbar-panel frame and its hero-entrance frame (person `lectrice-bibliotheque-dos`, company
   `chai-cuve-chene`, institution `table-en-seance`; university `cours-tableau-dos` in the panel and
   `paillasse-deux-etudiantes` in the hero), and the panel is on every page, so the rule «a frame already used by the
   navbar panel or the hero entrance of that audience is not reused as this page's lead» leaves none; the V1–V4
   library is retired (AUM §7) and renders nowhere until curated (`cms.MediaAsset.is_publishable`). The lead is the
   door card drawn (above). The slot takes a curated photograph the day one is captioned — the photograph then
   replaces the drawing, with its caption and credit, as the page's LCP image (never lazy). Not used, on purpose:
   `paillasse-deux-etudiantes` lower on the universities page (allowed by the letter, but it needs a caption in live
   text in four languages that does not exist).
2. **Three corners a screen (§1.3):** the chrome draws 6 on every screen (the targa; the phone's toggle), so the
   interior's cards and its plate fold their 8 into that 6 (`.interior { --card-radius: var(--radius-md) }`): 4 · 6 ·
   full, measured ≤ 3 on every capture.
3. **No side column** (the ecosystem's «Les espaces de l'écosystème», the institutional pages' local navigation, the
   pathways' «Dans l'Espace Personnes» aside): the chrome holds those links; the pathway pages keep «Dans l'Espace
   Personnes» as a closing register, because a reader at the end of a sheet wants the next step.
4. **One index, in the entrance, never sticky:** the pathway sheet's and the Forum's «Sommaire de la page» (an
   existing catalogue string, until now an aria-label) — the V4 sticky section bars are gone (W1-C's O2).
5. **One primary per page** (D26 «one action»): the pilot keeps the institutions' button as a secondary; the Forum in
   permanent mode makes the pilot's interest its primary (it had two secondaries on a navy band).
6. **Page sheets as plain import lists** in the collected tree (the steward's rule): `ecosystem/ecosystem.css`,
   `forum/forum.css`, `pages/css/interior.css` (new: the institutional pages leave `pages.css`, which is the home's
   alone now), `pathways/pathways.css` (new: the pathway pages had no page sheet — one CSS request more before
   `load` on the door-persons and pathway-detail page types). Each page's own rules in an app partial beside it
   (`_spaces.css`, `_forum.css`, `_institutional.css`, `_pathways.css`), so that W3-D's passage is one more line.
7. **The universities' breakdown removed** (RH-5), **the pilot illustration retired** (CD §19), **`DEFAULT_ICONS`
   from the registry** (W1-B), **authorities' host** computed in `pathways.services.authorities` (D26).
8. **What is being verified is said in words** on the «attesa» edge (the pathway sheet's four pending sections): a
   glyph in each would break the six-icon ceiling. **The Forum's two empty pages** (no edition yet) keep the empty
   state's own glyph — W1-B's contract, the handshake says which space is empty — drawn by `_forum.css` as the same
   row (no dashed box, nothing centred); `test_icons`' floor of empty-state callers 25 → 21 follows the sheet.
9. **Arabic:** a French head reads left to right and ends on the reading edge, whether the locked text tags its
   element or wraps itself in one span (the leads an `{% locked … as %}` passes); a French station's words on «la
   linea» end beside their numeral and ring (a step's body carries its language too). Text-level isolation is
   `static/css/base.css`'s fallback rule (RTL-01, RTL-09); bodies keep their own alignment, as on the home.
10. **The prescribed pathway descriptions stand as written** (lower case first) in the register, as on the home's.

## 3. Measures (lane 7; E/s4, E/s4w, E/a11y, E/forced; the before set in E/before)

| Page (fr) | screens 1440 before → after | 390 before → after | corners in the first screen | icons in the body (identity marks apart) |
|---|---|---|---|---|
| /parcours/ | 3.57 → 3.39 | 6.61 → 6.22 | 6 · full | 4 (the person disc, the action's arrow, the shield, the callout's arrow) |
| a pathway's sheet | 6.06 → 4.43 | 8.19 → 6.90 | 6 | 3 |
| /entreprises/ | 5.26 → 5.08 | 7.53 → 7.34 | 6 · full | 2 (the building disc, the shield) |
| /institutions/ | 2.09 → 2.33 | 3.79 → 3.74 | 6 · full | 2 |
| /universites-et-formation/ | 2.20 → 1.90 | 4.02 → 3.14 | 4 · 6 · full | 2 |
| /forum/ | 4.65 → 4.69 | 6.87 → 7.48 | 6 | 0 |
| /forum/inscription/ · confirmation | 1.22 / 1.17 → 1.33 / 1.35 | 2.08 / 2.15 → 2.10 / 2.19 | 4 · 6 | 0 |
| /le-projet/ | 2.69 → 2.53 | 4.37 → 4.17 | 6 | 4 (the four audiences, once a row) |
| /projet-pilote/ | 2.62 → 2.46 | 4.69 → 4.22 | 6 | 2 |

- **Overflow:** 0 on every capture — 14 pages × fr, ar × 1440, 390, and 7 pages × fr × 1366, 1024, 360 (E/s4w).
- **axe-core** (W1-0's copy, injected; `wcag2a … wcag22aa`): **0 violations** on 14 pages × fr, ar × 1440, 390 (56
  runs). The Forum eyebrow that failed contrast in W1-A's sweep is in the night's own ink now.
- **Focus:** a real-Tab walk of 40 stops per run: 0 stops without a visible indicator; the order is the chrome, the
  trail, the index, the body in DOM order, the action, the footer.
- **Forced colours** (Chromium's emulation): the plate and the disc keep their edges, the treads their top lines, the
  line its rings and stroke (E/forced).
- **Motion:** none — no transition, no keyframe, no `.reveal` left on these pages; reduced motion changes nothing.
- **CLS 0** on six pages × 1440, 390 (PerformanceObserver, lane); the LCP element is the entrance's lead or the first
  statement (text: the door card is CSS, no image request), 112–264 ms on the unthrottled lane — not the production
  shape (8782 was not used).
- **The home is pixel-identical** before and after the split of `pages.css` (fr, 1440 × 5065 and 390 × 8310, the same
  capture conditions; E/home-check).
- **The final set:** 15 pages (the home included) × fr, ar × 1440, 1366, 1024, 390, 360 = 150 captures, 0 overflow,
  0 console error, ≤ 3 radii in the first screen on every page of the area (E/final).
- **CSS (gzip −9)** — `dist/main.css` 42 472 → **42 316** (−156: the dead rules out). Page sheets: ecosystem 1 932 →
  3 172 · forum 2 147 → 3 671 · pages.css (the home's) 4 083 → 3 361 · interior.css (new) 3 047 · pathways.css (new)
  3 113. **Page-type totals:** home 57 132 → 56 254 (−878) · institutional pages 46 555 → 45 363 (−1 192) · ecosystem
  44 404 → 45 488 (+1 084) · Forum 44 619 → 45 987 (+1 368) · **door-persons and pathway-detail 42 472 → 45 429
  (+2 957; 943 B over §2.6's Wave-1 ceiling of 44 486, and one CSS request more)**. The interior's grammar is new CSS
  while the legacy page header, breadcrumbs and local navigation stay in `main.css` for W3-F2's pages and the second
  step's two pages; `main.css` sheds them when those pages move (§9, §10, §18, §19, §24, layout.css's editorial parts).
  Under V5.5's performance rule this is recorded for the steward, not traded against the pages: no LCP or long-task
  measurement on 8782 was taken in this step (the lane is not the production shape).

## 4. Items handed to W3-F1 by earlier areas

| From | Item | Answer |
|---|---|---|
| W1-A NOTES §ship sweep | the Forum eyebrow's contrast (axe, 4 → 4) | **done** — `.ingresso--night .ingresso__label` in `--text-on-night-2`; axe 0 on /forum/ fr + ar × 1440 + 390 |
| W1-B NOTES | the arrow density of the public editorial body (six-icon ceiling, DL54-29 item 1) | **done** on every page of this step — no arrow on a row or a link line; ≤ 4 icons in a body (table above); the identity marks of the section device apart |
| W1-B NOTES | `pagination__icon-prev` is dead CSS in §22 | **done** — the two rules deleted (`components.css` §22) |
| W1-B NOTES (review m2) | the pathway rows carry a numeral, a lone glyph above the title and an arrow; `.pathway-list__icon` has no rule | **done** — one marker per row, none (the title over the description, the row is the link), as on the home's register |
| W1-B NOTES (review m2) | the «Étapes» timeline squeezes its labels into letter-wide columns at 1440 | **done** — the steps on «la linea», down the reading edge at every width |
| W1-B NOTES | `pathways.services.DEFAULT_ICONS` still names V4 ids | **done** — `dict(icons.PATHWAY)`; the alias `globe` loses this producer (`living.catalogue` is W3-F2's) |
| W1-C NOTES | «Termes utiles»: the first row's two tags 4 px apart in height; the list touches the box under it | **done** — `.termes__list` (one row, tags of one height, 8 px apart), 32 px of chapter flow under it |
| W1-C NOTES | the two phases of «Formation» take the card's flow | **noted** — `/formation/` is the second step's page |
| W1-C NOTES (m3) | «Demande transmise»: the inline space between two buttons | **not this area's** — `templates/enquiries/done.html` is W3-F2's (the manifest); handed on |
| W1-C NOTES (O2) | the pathway page's sticky bar over its side column | **done** — no sticky bar, no side column: the index in the entrance |
| W1-C NOTES | the anti-fraud callout's measure | **done** — the callout stands in the body column; its lines at `--measure-body` |
| W1-C NOTES | «Pour aller plus loin» 6 px under the FAQ's last row | **done** — two chapters, 64 / 96 px apart |
| W1-C NOTES (O4) | `.section--verso > .t-prose` 1.06 : 1 on the pre-evaluation | **second step** — the orientation result page |
| W2-D NOTES | `templates/pages/partials/_section_header.html` (W3-F1's in the manifest, only the home includes it) | **unchanged** — the interior has its own chapter head (`_chapter_head.html`), the same device |
| W3-A NOTES | «Ma situation» draws five corners (the wizard's panel 12, its field 6); the questionnaire's foot and its one act | **second step** (the orientation wizard) |

## 5. Question headings proposed for the owner's copy packet (B1 item 7) — not written

«Les parcours réguliers» → «Quelle voie régulière correspond à ma situation ?» · «Dans l'Espace Personnes» → «Où
trouver d'autres informations ?» · «Trois temps, une même démarche» → «Comment se déroule la démarche ?» · «Recueil des
besoins» → «Comment signaler les besoins de mon entreprise ?» · «Ce que la plateforme fait, et ne fait pas» → «Que fait
la plateforme — et que ne fait-elle pas ?» · «Destinataires» → «À qui s'adresse cet espace ?» · «Proposer une
collaboration» / «Proposer un partenariat» → «Comment proposer une collaboration ?» · «La séquence du projet pilote» →
«Comment le projet pilote est-il organisé ?» · a pathway's sheet: «Aperçu» → «De quoi s'agit-il ?», «Étapes» → «Quelles
sont les étapes ?», «Documentation généralement requise» → «Quels documents sont généralement demandés ?», «Autorités et
acteurs compétents» → «Qui décide ?» (the diplomas page's own heading), «Avertissements» → «À quoi faut-il faire
attention ?», «Ressources» → «Où en savoir plus ?» · «Pour aller plus loin» → «Et ensuite ?». The «who can help me»
line is today «Besoin d'aide ? Écrivez-nous :» (allauth's layout string): the packet may give it its own wording.

## 6. Paths outside the slice (for the merge step's manifest)

- `static/css/v5/_interior.css` — new partial, imported by the four page sheets (W3-F2's pages will import it too).
- `apps/pages/static/pages/css/interior.css`, `_institutional.css` — the institutional pages' new sheet (the slice
  names `pages.css` only).
- `apps/ecosystem/static/ecosystem/_spaces.css`, `apps/forum/static/forum/_forum.css` — partials beside the owned sheets.
- `apps/pathways/static/pathways/pathways.css`, `_pathways.css` — new (no family holds `apps/pathways/static/`).
- `apps/pathways/services.py` — `DEFAULT_ICONS` from the registry; `authorities()` returns `host`.
- The app tests retargeted to the new markup, their intent kept: `apps/ecosystem/tests/test_{companies_page,compliance,gated_pages,browser}.py`,
  `apps/pathways/tests/test_{views,services}.py`, `apps/forum/tests/test_{forum_page,forum_mode}.py`,
  `apps/pages/tests/test_institutional.py`.
- `static/img/illustrations/pilot-flow.svg` (deleted; it landed in `3df3639`, the grammar's commit, though the
  ecosystem commit's message names it) and DS 2026 §2.1 / §14.1 (the slice names its pages' components' prose).
- `static/css/components.css` (§22, §24) and `static/css/layout.css` — inside the deletion map's slices.
- `tests/frontend/test_icons.py` (W1-B's): the floor of empty-state callers, 25 → 21 (item 8 above);
  `apps/ecosystem/tests/test_browser.py`: the stations on the line, the action card, the entrance's classes.
- New per-family files (in the slice `tests/**/test_*_w3_f1.py`): `tests/frontend/test_interior_w3_f1.py`,
  `tests/frontend/test_browser_w3_f1.py`.

## 7. Tests (targeted, V5.5 — one pytest at a time, `TEST_DATABASE_URL=…/test_ile_v5_l7`)

The full suite is the integration checkpoint's; these are the area's targeted runs, in order.

## 8. Runs

| Run | Result |
|---|---|
| `apps/ecosystem/tests`, `apps/pathways/tests`, `apps/forum/tests/test_forum_{page,mode,registration}.py`, `apps/pages/tests/test_institutional.py` (`-m "not browser"`), after the markup moved | 351 passed, 2 failed → fixed (the sheet's `data-steps`, the contact button's size class) → passed |
| after `git merge design-v5` (the steward's static pipeline): `npm run build:css` | the committed dist byte for byte (the scratch build in the collected tree had written the same files) |
| `test_static_pipeline`, `test_css_bundle_is_current`, `test_frontend_bundle_is_current`, `test_design_docs`, `test_o14_lint`, `test_state_chips_carry_a_register`, `test_icons`, `test_v5_tokens`, `test_css_tokens_exist`, `test_legacy_token_shim`, `test_static_assets`, `test_layout` | 901 passed, 1 xfailed (the shim's own), 1 failed (`test_icons`' floor of empty-state callers → the Forum's empty states restored, the floor 25 → 21) → passed; one error was `caplog` missing under `-p no:logging` (the run's flag), passed without it |
| `tests/i18n`, `tests/compliance`, `apps/pages/tests`, `apps/orientation/tests` (`-m "not browser"`) | 727 passed |
| `tests/frontend/test_interior_w3_f1.py` (new) | 54 passed |
| browser: `tests/frontend/test_browser_w3_f1.py` (new), `apps/ecosystem/tests/test_browser.py`, `apps/pages/tests/test_browser.py`, `tests/i18n/test_rtl_browser.py` | 76 passed, 0 skipped (`-rs`), no crash — after one fix (the Espace Entreprises' transparency notice, in French on the Arabic page, reads left to right again: a French block that is not a text element) |
| the final round — design docs, bundles, static pipeline, icons, O14, chips, the family's tests, the ecosystem, pathways, institutional and Forum tests, on HEAD | the static set on HEAD — test_design_docs, test_icons, test_o14_lint, test_state_chips_carry_a_register and the pathway views: 278 passed (18 s); a last pass over the ecosystem, pathways, institutional and Forum app tests on HEAD was started, then cut by the machine's load (other lanes' suites ran beside it: ≈ 2 tests a minute) — every file it covers passed on the commits above, and the templates changed since (the Forum's empty states, the line's language attribute, the pathway register's class) were re-run there (181 and 278 passed) |

## 9. Left for later

- **Step 2** (this area): /orientation/, /diplomes-et-titres/, /formation/ — and their V4 partials still drawn
  (`_orientation_cta.html`, `_side_links.html`, `_metadata_row.html`); the wizard (corners, foot, the stepper at 360).
- **W3-F2** takes the rest of §9, §10, §18, §19, §24 and layout.css's editorial parts as its pages move; then
  `main.css` sheds the legacy page header, breadcrumbs and local navigation, and the interior's page types come back
  under their ceilings.
- **W3-D** may draw the public passage on these pages: one import line in a page sheet; the pilot's sequence on «la
  linea» is the same diagram language.
- **The Image Art Director**: a frame per door (a curated, captioned asset takes the entrance's seat at once); the
  Forum's own frames (D20). RH-3 on the Forum's phone page (≈ 3 screens of prescribed prose without a figure) waits
  for them.

## 10. Seen on the way (other areas')

- The navigation marks «Institutions» current on /forum/ and «Entreprises» on /projet-pilote/ (the door whose panel
  holds the page) — W2-C1 / W2-C2's to confirm.
- On /ar/forum/ two UI strings stand in French (`Espace permanent de dialogue et de coopération`, `FORUM PERMANENT
  VÉNÉTIE–MAROC`): the catalogue's (the owner's translators, B2).
- The company needs form's labels are French on the Arabic page (prescribed labels; W3-F2 / B2).
- `/contact/` is in W3-F2's page list but its template is W3-F1's (`templates/pages/**`): it moved with the
  institutional base in this step; W3-F2 finds it on the interior's grammar.
- `docs/ACCESSIBILITY.md` (2.4.11, and the sticky layers' note) and `docs/design/ASSET_REGISTRY.md` (the
  illustrations) still name `.section-nav` and `pilot-flow.svg`, both retired here — the steward's / their owners'
  to update (A11Y is not this area's).

---

# Step 2/2: ORIENTATION, THE ADVICE PAGES AND THE WIZARD

Implementer `w3-f1-impl-2` · 11 October 2026 · V5.5 delivery mode on V5.4's decisions · plan §3.5 item 1 (continued),
§1.18 D26, §1.4 RH / SH, §1.3, §1.7, §2.2, §2.3 · same branch and lane as step 1 (`127.0.0.1:8787`, `ile_v5_l7`,
`ILE_REFERENCE_DATE=2026-10-03`) · evidence `C:/tmp/ile_v5_council/evidence/v54/w3-f1/step2/` (E2/ below) · decisions
DL54-80, DL54-81 (the steward renumbers at the merge).

## 11. What the pages are now

| Page (fr + ar) | Now |
|---|---|
| **/orientation/** (the questionnaire's first page) | the entrance («Espace Personnes», the h1, the lead, verbatim) → «Comment se déroule le questionnaire»: its three moments on «la linea» (across from 48rem, the fragments' first letter set in capitals by CSS, the words unchanged) and the ONE inset, «À lire avant de commencer» (the prescribed sentence once G3 is open) → on the stone the ONE action: the action card «Questionnaire d'orientation» — what it is, «Commencer →» (52 px), the way back in with a resume code; the pathways' presentation as a quiet line. Without a ruleset: the pending notice and the live «who can help me» line |
| **a step** (/orientation/session/…/) | the page's title and its sentence at the reading edge; the progress as a quiet register — «Question 2 · 35 %» over a 2 px line on its hairline, filled from the reading edge (`role="progressbar"`, its value in words), no pill, no movement; the question as the fieldset's legend (entry size); «Pourquoi cette question ?» as a native disclosure with a drawn chevron; «Plusieurs réponses possibles.» before the choices and in the group's `aria-describedby`; the choices as plates (4 px, a hairline) around the native radio / checkbox of v5/field.css (24 px), the whole plate the target, the control on top of it; chosen = the edge doubled in the primary's fill + the control's own mark; ONE primary «Continuer» first in the DOM (Enter), «Précédent» after it, after a hairline — part of the page, «Continuer» taking the row on a phone; the session's reference, quiet |
| **a refused answer** | the words said beside the refusal's mark (`circle-alert`), announced (`role="alert"`), wired to the group (`aria-describedby="answer-error"`, `aria-invalid`), every plate's edge doubled in the refusal's ink — never colour alone |
| **the pre-evaluation** | the entrance («Votre pré-évaluation», the result as the h1) holding the ONE inset under the h1 — the informational banner, so the result and what it is worth read together → «Ce que cela signifie» (the reading measure) → «Famille de parcours correspondante»: the prescribed title over its description, as written, on a register row, then «Consulter la page du parcours» (secondary) → «Prochaines étapes à caractère informatif»: the groups, «Points d'attention» on the warning's broken edge with the anti-fraud page → «Formation avant le départ» when asked → the record's note, quiet: «Avertissement» (the prescribed sentence once G3 is open), the reference, the date, the two versions → on the stone: the resume code shown once (the warning's register: its mark, its words, its broken edge; the code on a plate, selectable whole) and the actions (save — the one primary when it is offered —, start again, print) |
| **/orientation/reprendre/**, «Enregistrement indisponible» | the entrance, then the form at the reading edge: the field «la lastra» (16 px typed text, 52 px), its error wired by Django and said beside a drawn mark, «Reprendre» (the one primary) and «Commencer un nouveau questionnaire» after a hairline; the gate's own notice and the way back |
| **/diplomes-et-titres/** | the entrance (the prescribed title in capitals, tracked, and its body; the sheet's metadata row, no glyph) → «Les démarches, étape par étape»: the five moments on «la linea» down the reading edge, each station open and broken (still being verified — said in words under the line), each glossary term under its own station (V4's timeline squeezed the labels into letter-wide columns at 1440) → «Qui décide ?» with the anti-fraud callout as its inset → «Dans l'Espace Personnes», the closing register (its own row left out) → on the stone the one action and «who can help me» |
| **/formation/** | the entrance (+ the metadata row) → the two moments of one path as two stations of «la linea»: each moment's word («Premier temps», «Second temps») in the numeral's seat beside its open ring, its title at the entry's size (the prescribed «FORMATION APRÈS L'ARRIVÉE» tracked), its text at the reading size and measure, its one way further; the first carries the page's notice (no attestation is an administrative approval) → «Dans l'Espace Personnes» with the anti-fraud callout → on the stone the one action and «who can help me». No card |
| **/attention-aux-fraudes/** | the entrance (the prescribed title as the h1, nothing above it) → the prescribed text, byte-identical, as the page's one inset — now a warning notice of the core components with a visible title, «Votre protection» (the label left the entrance for it), the anti-fraud mark once and the broken rule → where to report → where to read about the regular ways |
| **the anti-fraud callout** (on /parcours/, a pathway's sheet, the two advice pages) | a warning notice (amber, the edge broken): the anti-fraud entry's mark, the prescribed title in the register's word with its capitals tracked, the body, «Lire la page …» — the kind said three times; on the Arabic page the French title is a run inside a heading that ends on the reading edge beside the mark |
| **«Ma situation»** (console; markup W3-E's / W3-D's, untouched) | `v4/wizard.css` retired for the console partial `v5/_wizard.css`: the question on the screen's ONE raised panel at 8 px (was 12), the date field the plate of v5/field.css at 4 px (was 6), the foot part of the page at every width after a hairline (was sticky glass at 8 px) — 4 · 8 · full, three corners; no light behind the question; the OptionCards as plates, the chosen one's edge doubled and the person's own check (O14); the Stepper's current node thicker and in the primary, its words in ink and weight (never colour alone; on a phone the ring's weight says it), answered nodes filled, the line a hairline |

## 12. Decisions met during the build (DL54-80, DL54-81)

1. **The advice pages read like a pathway's sheet** and end the same way (the closing register, then the stone with the
   one action and «who can help me»); V4's side column, CTA band and two-glyph metadata row leave with their last
   consumers (`_side_links.html`, `_orientation_cta.html`, `_metadata_row.html` deleted).
2. **A real sequence stands on «la linea»** — the diplomas' five moments, Formation's two (DL54-55 makes a phase a
   record, but two phases in a row are a sequence; card.css itself says a row of records is a list, not boxes).
3. **The fraud warning is amber with its edge broken** — mark, words, rule; on its own page the inset gains a visible
   title («Votre protection», an existing string), since a hidden one left the notice saying its kind twice.
4. **The questionnaire's keyboard model**: a step reached from the questionnaire (the referrer is one of its pages)
   puts the focus on the new question — no ring on that programmatic, untabbable target; opened otherwise, the browser's
   start. Every answer is a full post (HTMX is not loaded), so without it a keyboard user started each step at the top.
5. **The pre-evaluation keeps one inset** (the banner, in the entrance); the disclaimer joins the record's facts as the
   quiet note; the one-time resume code keeps the warning's register (a secret to keep, not an editorial inset); the
   family's title links nothing, the way to its sheet is said in words on a secondary button (a single row whose
   title is a link reads as a fact, not as a way on a touch screen).
6. **«Ma situation»'s guided form becomes a console partial** (it never belonged in the cascade every page loads); the
   console's corners are W3-B's (8 for a panel), so the panel folds 12 → 8 and the field 6 → 4.
7. **On the Arabic page** a French question and a French choice end on the reading edge (the question as every French
   head of the interior, a choice beside its control); the help and the bodies keep their own alignment.

## 13. Measures — the whole area together (lane 7; E2/area, E2/sweep*, E2/a11y, E2/forced)

| What | Result |
|---|---|
| Every page of the area × fr, ar × 1440, 390 (23 pages and states; the home beside them as the reference, W2-D's) | 92 captures of the area: **0 horizontal overflow, 0 CSP report, 0 console error, ≤ 3 radii in the first screen on every one**; no shadow of level ≥ 3 at rest on any public page; on «Ma situation» one (the chrome's menu, W3-A's: «the rail's one menu») |
| Overflow sweep 320 · 360 · 375 · 412 · 430 px × fr, ar × 22 pages and states (`--no-png`) | 237 records (the questionnaire's flow re-run after the lane's restart: its start is throttled at 20 per 10 minutes) — **0 overflow, 0 CSP, 0 error, ≤ 3 corners in every first screen** |
| axe-core (W1-0's copy, `wcag2a … wcag22aa`) × the step's 10 pages and states × fr, ar × 1440, 390 | **0 violations** on 40 runs |
| Real-Tab walk, 40 stops a run (40 runs) | every stop ringed — the one stop the probe flags on «Ma situation» is the date field's calendar button, ringed by v5/field.css's own rule inside the control's shadow tree (W1-C's A9), which a script reading `document.activeElement` cannot see |
| Forced colours (Chromium's emulation; E2/forced) | the progress keeps its track and its fill (GrayText / CanvasText), a chosen plate its Highlight outline, the radios the system's own, the panel and the nodes their edges |
| Reduced motion / keyboard (tier 0) | a choice's transitions at 0 s in both (test_orientation_browser_w3_f1); nothing on these pages moves on its own |
| Typed text, targets | 16 px in the resume field (52 px high); the plates ≥ 56 px; «Continuer» 52 px |
| Screens (fr 1440 / 390), before → after | /orientation/ 1.96 → 2.14 / 3.17 → 3.45 · a step 1.51 → 1.69 / 2.43 → 2.55 · the pre-evaluation 3.20 → 3.58 / 5.27 → 5.60 · /diplomes-et-titres/ 3.48 → 3.60 / 6.15 → 5.92 · /formation/ 2.53 → 3.30 / 5.02 → 5.42 (the phases at the reading size instead of two narrow cards and a side column) · «Ma situation» 1.48 → 1.49 / 1.91 → 1.98 |
| Corners in the first screen, before → after | «Ma situation» 4 · 6 · 8 · 12 · full → **4 · 8 · full**; a step 4 · 6 · full (the plates 6 → 4, the progress pill gone); /formation/ 4 · 6 · 8 → 4 · 6 |
| The picture cadence on the door pages (the largest stretch of the page without a picture or a drawn figure — the door card, «la linea», a figure —, in screens; RH-3 asks ≤ 2) | /institutions/ 1.2 / 1.78 · /universites-et-formation/ 0.77 / 1.11 · /projet-pilote/ 1.05 / 1.46 · /le-projet/ 1.82 / **2.74** · /parcours/ **2.25** / **4.01** · /entreprises/ **3.47** / **4.20** · /forum/ **3.97** / **6.04** (1440 / 390). Over two screens: the stretches between the door card and the end (the pathways' register, «Comment ça marche», the callout), the companies' needs form, the Forum's prescribed prose. No approved frame is left for those slots (§1.16, step 1's decision 1) and «la linea» is kept for real sequences: they wait for the Image Art Director's curated, captioned frames — a frame takes its seat with one partial, as step 1 wrote |
| Icons in the editorial body (identity marks apart) | ≤ 4 on every page of the step — the advice pages: the notice's mark where there is one, the callout's mark and arrow, the action's arrow; the first page 2; a step 0 (1 with its error's mark); the pre-evaluation 2 (the banner's, the code's) |

## 14. The deletion-map rows retired, and the CSS (gzip −9)

| Row (plan §2.3, W3-F1's) | Retired |
|---|---|
| `v4/wizard.css` | **the file** (11 959 B raw): its rules rewritten on V5 as the console partial `apps/portal/static/portal/v5/_wizard.css`; main.css's import line through the steward's rule (§2.2) |
| V1 `layout.css`'s editorial parts, by page | `.section--rule`, `.section--tight`, `.grid-auto`, `.layout-sidebar--end`, `.stack--sm`, `.stack--lg` — the two advice pages were their last consumers (`layout.css` 9 296 → 8 795 B) |
| `components.css` §9, §10, §18, §19, §24 | nothing this step: §19 is still drawn by `portal/partials/access_point.html`, §24 by allauth's manage layout, §10 and §9 by W3-F2's pages, §18 by the home — W3-F2 and the console families take them |

**`dist/main.css`: 42 316 → 41 212 B gzip (−1 104 on every page type)** — 41 273 with `v4/wizard.css` out (−1 043),
41 212 with the layout rules (−61). Page types (main.css + the page's own sheets), before → after:

| Page type | Before | After | Ceiling (Wave 1 / DL54) |
|---|---|---|---|
| home | 56 254 | 55 150 | follows main.css (DL54-44) |
| institutional pages | 45 364 | 44 266 | 44 486 — **back under it** |
| ecosystem | 45 489 | 44 385 | 44 486 — **back under it** |
| Forum | 46 093 | 44 989 | 44 486 — 503 over (was 1 607) |
| door-persons, pathway-detail, «Diplômes», «Formation» | 45 430 | **44 486** | 44 486 — at it (was 943 over) |
| the orientation pages | 43 659 | **45 533** | 44 486 — **1 047 over**: they draw the interior's grammar now (≈ 3 KB) where V4 had a 1.3 KB sheet of their own; recorded for the steward under V5.5's performance rule (text LCP, no image, no new request) |
| the console page types | 49 894 | 49 986 | 50 086 — under it (the guided form moves from main.css into the console entry: console.css 5 304 → 6 500) |

No LCP or long-task measurement on 8782 in this step (the lane is not the production shape); CLS: the pages draw no
image and no late block.

## 15. Items handed to this step, and the answers

| From | Item | Answer |
|---|---|---|
| W3-A (DL54-70, NOTES) | the questionnaire's foot is part of the page below 64rem; its ONE act «Continuer» | **done** — part of the page at every width (no glass, no sticky), after a hairline; one primary a screen (situation.js: «Continuer», the submit on the last question), full width on a phone. The action bar (`data-console-action`) needs the page's markup (W3-E's template): not written |
| W3-A NOTES | «Ma situation» draws five corners (the panel 12, its field 6) | **done** — 4 · 8 · full at 1440 and 390, fr and ar (test_orientation_browser_w3_f1) |
| W1-C NOTES | the wizard's own input (6 px) and question panel (12 px) (handed to W3-D) | **done here** with the retirement of `v4/wizard.css` |
| W1-C NOTES (O3) | the wizard's sticky foot, its 20 px radios | **done** — the foot static; the public wizard's radios are v5/field.css's 24 px; «Ma situation»'s OptionCards draw a 24 px mark |
| W1-C NOTES | the two phases of «Formation» take the card's flow | **superseded** — the phases are two stations of «la linea»; W1-C's test keeps the showcase's case |
| step 1 §9 | /orientation/, /diplomes-et-titres/, /formation/ and their V4 partials; the wizard (corners, foot, the stepper at 360) | **done** — no overflow at 320–430 px, the phone's Stepper a row of nodes |
| step 1 §4 (W1-C O4) | `.section--verso > .t-prose` 1.06 : 1 «on the pre-evaluation» | **not this area's** — the markup is `templates/cases/assessment.html` (the case's pre-evaluation, W3-E's); the orientation result draws no `.section--verso` |

## 16. Paths outside the slice (for the merge step's manifest) — step 2's, beside §6's

- `apps/portal/static/portal/v5/_wizard.css` — new: «Ma situation»'s guided form, console-only (plan §2.3's place for
  console-only CSS); `apps/portal/static/portal/console.css` — its one import line, after the shell (§2.2's rule).
- `apps/pathways/static/pathways/_pathways.css` — step 1's partial, extended (the diplomas' terms, Formation's line, the
  callout).
- `tests/frontend/test_console_shell_w3_a.py` — the import-list test accepts a family's partial after the shell (as
  W3-B's branch writes it); `tests/frontend/test_chips_cards_w1_c.py` — the interior's chip and tag placements named,
  Formation no longer draws cards (the showcase keeps the case).
- DS 2026 §2's table regenerated by `scripts/regen_design_inventory.py` (the row of `v4/wizard.css` removed, the
  weights of `layout.css` and `components.css`), as W2-D did; §2.1 and §10 are the slice's prose.
- New per-family files (in the slice): `tests/frontend/test_orientation_w3_f1.py`,
  `tests/frontend/test_orientation_browser_w3_f1.py`; `templates/orientation/_result_banner.html` (new, in the slice).
- `scripts/check_ownership.py w3-f1 design-v5`: 23 paths outside — §6's nineteen and these four
  (`console.css`, `_wizard.css`, `test_chips_cards_w1_c.py`, `test_console_shell_w3_a.py`).

## 17. Runs (targeted, V5.5 — one pytest and one browser at a time, `TEST_DATABASE_URL=…/test_ile_v5_l7`)

The full suite is the integration checkpoint's; these are the step's targeted runs, in order.

| Run | Result |
|---|---|
| `apps/orientation/tests`, `apps/pathways/tests`, `apps/pages/tests/test_institutional.py`, `tests/compliance`, `test_interior_w3_f1`, `test_console_shell_w3_a`, `test_chips_cards_w1_c` (`-m "not browser" -x`) | 427 passed, then 1 failed: `test_the_chip_is_drawn_by_one_sheet` — step 1's two placements (`_interior.css` `.registro__row > .chip`; `_pathways.css` `.termes__list .tag`, with a hover that painted the tag) were not in W1-C's list → the hover left to v5/chip.css, the two placements named in the test |
| `test_chips_cards_w1_c`, `test_design_docs`, `test_css_bundle_is_current`, `test_frontend_bundle_is_current`, `test_o14_lint` | 118 passed |
| `tests/frontend/test_orientation_w3_f1.py` (new) | 30 passed |
| browser: `tests/frontend/test_orientation_browser_w3_f1.py` (new) | 11 passed, 0 skipped |
| `tests/i18n` (all, non-browser), `apps/ecosystem/tests`, `apps/pages/tests`, `apps/forum/tests/test_forum_{page,mode,registration}.py`, `test_banner.py`, `tests/frontend/test_layout.py`, `test_static_pipeline` (a real `collectstatic` under the manifest storage), `test_state_chips_carry_a_register`, `test_icons`, `test_static_assets`, `test_css_tokens_exist`, `test_interior_w3_f1`, `test_chips_registry`, `tests/test_regen_design_inventory.py` (`-m "not browser"`) | **1 126 passed**, 86 deselected (31 min, other lanes' suites beside it) |
| browser: `tests/i18n/test_rtl_browser.py`, `test_rtl_browser_entrance.py`, `test_rtl_browser_nav.py`, `apps/ecosystem/tests/test_browser.py`, `apps/pages/tests/test_browser.py`, `tests/frontend/test_browser_w3_f1.py`, W3-A's `test_the_questionnaire_s_foot_is_part_of_its_page_and_the_bar_keeps_its_entries`, `test_orientation_browser_w3_f1.py` | **104 passed**, 0 skipped (`-rs`), no crash |
| on HEAD, after the last template and partial changes: `apps/orientation/tests`, `apps/pathways/tests`, `apps/portal/tests/test_situation.py`, `tests/compliance`, `test_orientation_w3_f1`, `test_design_docs`, the two bundle-currency tests, `test_o14_lint`, `test_chips_cards_w1_c`, `test_console_shell_w3_a`, `test_state_chips_carry_a_register`, `test_static_pipeline` | **613 passed** (6 min 36 s); then the two family files after `ruff format`: 41 passed |
| `ruff check` on the Python the step touched; `scripts/regen_design_inventory.py` (check) | `ruff check`: all checks passed; the inventory: «the inventory tables and the counts are current» |

## 18. Left for later

- **W3-D**: the Stepper of «Ma situation» stands in `v5/_wizard.css` until the journey family redraws it
  (`components/wizard_stepper.html` is theirs); the public passage may come to the advice pages with one import line.
- **W3-E**: «Ma situation»'s one act as the phone's action bar (`data-console-action` on the page's markup); the
  case's pre-evaluation (O4).
- **The Image Art Director**: RH-3 on /parcours/, /entreprises/, /forum/ (and /le-projet/ on a phone) waits for curated,
  captioned frames (§13).
- **The steward**: the orientation pages' page type (45 533, 1 047 over the interior's Wave-1 ceiling) and the Forum's
  (503 over) to record; DS 2026 §2 is regenerated on this branch.
- **B1 item 7** (the reader's questions as headings): «Les démarches, étape par étape» → «Comment se déroulent les
  démarches ?», «Qui décide ?» (already one), «Comment se déroule le questionnaire» (already one), «Ce que cela
  signifie» → «Que signifie ce résultat ?», «Prochaines étapes à caractère informatif» → «Que faire ensuite ?» —
  proposed, not written.

## 19. Seen on the way (other areas')

- The account menu's list on «Ma situation» at 320–430 px carries a level-3 shadow while closed (counted at rest by
  the probe) — W3-A's to look at; the area's rule «one at rest» holds.
- The anti-fraud chapter of the home is W2-D's «gradino» and was not touched; it keeps the institutional register.

---

# Review fixes (the fix pass, `w3-f1-fix`, 11 October 2026)

The senior review (`REVIEW.md`: no blocking item, five majors, eight minors) and the accessibility and performance
check (`A11Y_PERF.md`: one major, two minors), fixed in one pass (V5.5: implement → review once → fix → ship), each on the
review's one direction. Lane 7 (127.0.0.1:8787, `ile_v5_l7`, `ILE_REFERENCE_DATE=2026-10-03`, `DB_CONN_MAX_AGE=0`,
`--noreload`, no preview flag); one headless Chromium at a time with its own profile (`.profiles/w3-f1-fix/`); one
pytest at a time on `test_ile_v5_l7`; `PERFORMANCE_BENCHMARK_LOCK` checked before every browser series and build (never
present); no run crashed. The pass was resumed after its first agent stopped at the session limit (22:39) with the code
written and nothing committed: that work was read line by line, re-measured on the lane and completed; one defect of
its own was found and fixed before the commit (§21). Decision log: DL54-82. Evidence: E/ =
`C:/tmp/ile_v5_council/evidence/v54/w3-f1/fix/` (`measure/` the first screens and the metrics by page, language and
size; `sections/` the fixed sections; `wizard/` the questionnaire; `shots/` the first agent's captures).

## 20. What was fixed

| Item | What the page does now |
|---|---|
| **M1** «la porta» | The end seat's plate keeps its night, its disc and its accent rule and carries the door's way in (`pages/partials/_via.html`): on /parcours/ (and the interim page) the questionnaire's action card — «Identifiez la voie régulière à explorer», its sentence, «Commencer le questionnaire d'orientation», the page's one primary; on /institutions/ and /universites-et-formation/ the prescribed button and its one sentence, the page's one primary (their action chapters below are gone: the action is said once); on /entreprises/ «Recueil des besoins» as a secondary that leads to the form, whose submit stays the one action. The stair is gone. A curated, captioned photograph takes the seat the day it exists, and the way then stands under the lead (`.ingresso__way`). On the night the controls take their night faces (`.on-inverse`). The sentence keeps its language where the translators have not given it yet (/ar/entreprises/: `lang="fr"`) |
| **M2** RH-3 | /parcours/: «Comment ça marche» on «la linea» — the locked sentence cut on its own « → » into four stations, its opening words as hidden text, its caveat under them (`pathways.services.how_it_works`: joined back, the registry's sentence, character for character, in fr, it, en, ar; a sentence of another shape stands whole); the stations' first letters raised in CSS only. /entreprises/: the six short single-line fields two by two from 64rem (the page ≈ 290 px shorter at 1440), and the form's region recorded outside RH-3's cadence (DL54-82 item 2). /forum/ and /le-projet/ on a phone: the waiver written into DL54-82 with the condition that lifts it (curated, captioned frames, §1.16) |
| **M3** the percentage | «Question n sur N au maximum» (the catalogue's string, already translated in it / en / ar and used as the bar's `aria-valuetext`) is the visible count; the «· p %» span and its rule are gone; the quiet line stays. FM12's test: no «%» in a rendered step, its attributes included, and no `<progress>`, in fr and ar, on the first step and the next |
| **M4** «Commencer» | The questionnaire's first page: «À lire avant de commencer» under the lead (`orientation/_start_notice.html`, the entrance's `meta_template`), the action card in the end seat (`orientation/_start_action.html`, `aside_template`) from 64rem and right after the inset on a phone, the three moments after it; one place for the action |
| **M5** «ACCOMPAGNEMENT» | Eight stations a row from 90rem, four a row below it (`_spaces.css`) |
| **m1** the programme | A time column only when every row has a time (CD §20): the rows are numbered 01 … 08 and the first keeps its words whole, «15h00 — Accueil et enregistrement» (`ForumProgramItem.__str__`); with every row timed, the time column returns (tested) |
| **m2** the Arabic stair | Moot: the stair left with M1 |
| **m3** the Forum's index | One link a row, on its hairline, at every width (the wrapping row below 64rem is gone) |
| **m4** «Destinataires» | The prescribed sentence as written is the chapter's body (`chapter__statement`, `lang` where it is French); the presentational list, its partial (`ecosystem/partials/enumeration.html`) and its rules are deleted |
| **m5** a step's head | The compact title alone (the entry's size); the sentence is said once, on the first page |
| **m6** French on Arabic pages | The Forum's untranslated eyebrow and name carry `lang="fr"` (and the trail's link to the Forum on the registration pages: `apps/forum/services.py` gives the view the name's language when the catalogue returns the msgid); /agami/'s question and answer carry their language on their own elements, so they are tagged and read left to right with their «?» and «.» at the end |
| **m7** the Arabic lead | `_interior.css` §7: a head (the space's name, the h1, a chapter's title) ends on the reading edge; a French lead keeps its own start, in a box on the reading edge no wider than its words — seven to eleven lines no longer end ragged on the left, and a one-line lead still meets the reading edge. The home's half is W2-D's (§23) |
| **m8** the double current marker | Handed to W2-C1 / W2-C2 (§23) |
| **A11Y 1** SP-8 | The trail's links and the chapters' forward links (`.chapter__more > a`, `.chapter__links > a`) are boxes on `--hit-min` (24 px), and on `--hit-primary` (44 px) under a coarse pointer, with the «Termes utiles» tags (`_pathways.css`) and /contact/'s address (`_institutional.css`); boxes, not pseudo-targets, so two rows of links never overlap |
| **A11Y 2** French unmarked or undirected | As m6 |
| **A11Y 3** the page types' CSS | Recorded (DL54-82 item 7; §22), and lowered where it was cheap: the door card's rules leave the interior's grammar for `static/css/v5/_porta.css` |

## 21. Found and fixed during the pass

- **A comment on the page.** The first agent's note in `pages/agami.html` was a `{# … #}` written over two lines;
  Django's one-line comment does not span lines, so its words stood on /fr/agami/ and /ar/agami/ (in Arabic, a column of
  fragments beside the FAQ's head). The note moved into the file's header comment; two tests now guard it — no
  unclosed `{#` in the area's template folders, and no template syntax in the rendered `main` of the thirteen
  interior pages in fr and ar.
- **The Arabic caveat.** Under «Comment ça marche» on /ar/parcours/, the one-line French caveat floated mid-column (its
  box the full measure, its words starting at its left): its box is now no wider than its words and stands on the
  reading edge, under the first station, as the leads do (m7).
- **The door card loads only on the doors** (V5.8: a surface's own CSS loads only where it is drawn). Its rules — the
  plate, the disc, the way, their forced-colours and print states — move from `_interior.css` to
  `static/css/v5/_porta.css`, imported after the interior's grammar by `pathways/pathways.css` and
  `ecosystem/ecosystem.css` alone; «Comment ça marche»'s rules move to `_pathways.css`. The Forum, the project's pages
  and the questionnaire shed ≈ 300–340 B gzip each; the doors render pixel for pixel as before (the controls' positions
  and the pages' heights measured before and after the split: identical).
- **DS 2026 follows the pages.** The §2.1 rows of the area's sheets still drew «i tre gradini accesi», «l'enumerazione
  dei destinatari come registro di parole», «otto da 80rem», and §10's page index «sotto 64rem una riga di link che
  vanno a capo»: rewritten as built (the rows of `ecosystem.css`, `interior.css`, `pathways.css`, `forum.css`,
  `wizard.css`; §10's «Sommario di pagina» and «la linea»'s consumers). `scripts/regen_design_inventory.py`: current.
- **CI's lint.** Four test lines over 120 characters in the app tests (`ruff check .` runs in CI; E501 is not ignored
  under `apps/*/tests/`), one of them older than this pass: shortened; the touched Python files in ruff's format.

## 22. Measures (lane 7; E/measure, E/sections, E/wizard)

**The door's way in — the control's top in px (fr / ar)**, `measure.py`:

| Page | 1440 × 900 | 1366 × 768 | 390 × 844 | 360 × 800 | the review |
|---|---|---|---|---|---|
| /parcours/ — «Commencer le questionnaire d'orientation» | 413 / 389 | 437 / 389 | 797 / 779 | 885 / 807 | 1.8 / 2.2 / 3.3 / 3.7 screens |
| /entreprises/ — «Recueil des besoins» (the submit stays below) | 293 / 293 | 293 / 293 | 697 / 710 | 697 / 710 | the submit at 3.6–5.1 screens |
| /institutions/ — the prescribed button | 317 / 293 | 317 / 293 | 501 / 490 | 501 / 490 | — |
| /universites-et-formation/ — the prescribed button | 317 / 293 | 317 / 293 | 565 / 520 | 617 / 550 | first screen at desktop only |
| /orientation/ — «Commencer» | 342 / 342 | 370 / 342 | 882 / 809 | 986 / 861 | 1 152 / 1 200 / 1 512 / 1 644 |

**RH-3 — the largest stretch of `main` without a picture or a drawn figure** (the door card, «la linea», a figure; the
builder's measure), in screens, fr: /parcours/ 0.98 · 1.84 · 2.00 at 1440 · 390 · 360 (was 2.25 / 4.01);
/institutions/ 0.79 · 1.12 · 1.28; /universites-et-formation/ 0.46 · 0.66 · 0.73; /projet-pilote/ 1.05 · 1.46 (1440 ·
390); /entreprises/ 3.15 · 4.23 · 4.62 (was 3.47 / 4.20; the form, recorded outside the cadence); /le-projet/ 1.90 ·
2.85 (waived on a phone); /forum/ 3.99 · 6.18 · 6.90 (waived). Arabic within 0.1 of these.

**Health.** 0 horizontal overflow, 0 CSP report, 0 console error, every response 200: 18 pages × fr, ar × 1440 and 390
(the doors and orientation also at 1366 and 360). **Targets:** no trail or forward link under 24 px at 1440; the boxes
under 24 px that remain are a register row's title link (the whole row is the target) and the inline address in «Besoin
d'aide ? Écrivez-nous :» (the inline exception); under a coarse pointer at 390 the trail and the forward links answer on
44 px (the browser test). **The pilot:** four a row at 1280 and 1366, eight at 1440; no word breaks (fr, ar; the browser
test). **The questionnaire** (`wizard.py`, fr and ar × 1440 × 900, 1366 × 768, 390 × 844): «Question 1 sur 3 au maximum»
/ «السؤال 1 من أصل 3 كحد أقصى», then «Question 2 …»; no «%» in a step's markup or text, no `<progress>`; «Continuer» at
832–884 px on the first question at 1440 × 900 (was 920), 724 on the second. **French on Arabic pages:** the Forum's
eyebrow, name and trail link, /agami/'s question and answer and the companies' way sentence carry `lang="fr"`; the
translated way sentences carry none.

**The CSS** (GNU `gzip -9 -n` of the committed bundles, by page type; HEAD `25a3322` → the fix pass):

| Page type | before | after | the interior's ceiling 44 486 |
|---|---|---|---|
| `dist/main.css` (every page; the shared payload) | 41 203 | **41 203** | unchanged |
| persons (`main.css` + `pathways.css`) | 44 464 | 44 586 | 100 over |
| ecosystem (`main.css` + `ecosystem.css`) | 44 362 | 44 483 | 3 under |
| Forum (`main.css` + `forum.css`) | 44 970 | 44 671 | 185 over |
| institutional (`main.css` + `interior.css`) | 44 244 | 43 915 | under |
| orientation (`main.css` + `wizard.css`) | 45 513 | 45 172 | 686 over |

The doors' types grow by the fix's own rules (the way in, the line of «Comment ça marche», the targets); the others
shrink with the door card's split. After the merge, design-v5's −646 B on `main.css` (W3-B) leaves only orientation
over (≈ 40 B); W3-F2's deletions bring it under. JS unchanged.

## 23. Not done, and why

- **CD §10's «primary within 560 px at 360 × 800»** is reached on /institutions/ (501 / 490) and on
  /universites-et-formation/ in Arabic (550), not on /parcours/ (885 / 807), /universites-et-formation/ in French (617)
  or /entreprises/ (697 / 710, a secondary). The locked leads run ten to twelve lines on /parcours/ at 360–390 px; the
  rule was written for a lead of at most three lines, and the control is not set above the lead, whose disclaimer is
  read first. A shorter lead is a copy decision (B1), not a layout one.
- **/orientation/ on a phone**: «Commencer» follows the lead and the inset, both prescribed before it in the reading
  order (882 / 986 px at 390 × 844 / 360 × 800).
- **m5 at 1366 × 768**: the first question's six plates (58 px, kept as the review asked) set «Continuer» 64 px under the
  fold; the second question's within 8 px.
- **m7's other half** — the home's French lead on the Arabic page (W2-D's `pages.css`): one rule for both, through the
  steward, with the interior's as the model (`_interior.css` §7: a head `direction: ltr; text-align: end`; a lead
  `inline-size: fit-content; direction: ltr; text-align: start`).
- **m8** (the chrome) — handed to **W2-C1 / W2-C2**: `cms_nav._mark_current` makes a door current whenever one of its
  children matches, so «Institutions» and «Forum Vénétie–Maroc» are both current on /forum/ (only the Forum on
  /forum/inscription/), «Personnes» and «Universités & Formation» on /formation/. Their fix: when a top-level link or a
  single door owns the page, mark only that one, the same on every page of a section.
- **A11Y 3**: the page types over the interior's ceiling are recorded, not traded against the pages (§22, DL54-82
  item 7), as DL54-81 asked.
- **A door card's control on two lines at 1440** in French («Commencer le / questionnaire d'orientation», «PROPOSEZ UNE
  / COLLABORATION INSTITUTIONNELLE»): kept — on the plate the control takes the plate's measure and its words wrap rather
  than overflow (`_porta.css`), a choice of the pass.
- **A11Y_PERF's observations** O1–O4 are other areas' (W2-C1, W3-A); O5 (a chosen plate's sign under forced colours), O6
  (`role="status"` on static content) and O7 (focusing the refusal's line) are optional and are not taken up here.

## 24. Paths outside the slice — the fix pass's, beside §6 and §16

- New: `static/css/v5/_porta.css` (the door card's partial, beside `_interior.css`).
- Newly touched: `apps/forum/services.py` and `apps/forum/views.py` (the Forum's untranslated name says its language on
  the page and in the trail); `apps/pathways/views.py` (`how`, the cut sentence); `apps/pathways/tests/test_compliance.py`
  (a locked text cut for layout is read back whole).
- Touched again (outside since steps 1 and 2): `static/css/v5/_interior.css`, `apps/pathways/services.py`, the page
  sheets and partials (`ecosystem.css`, `_spaces.css`, `_forum.css`, `_institutional.css`, `pathways.css`,
  `_pathways.css`), the app tests of ecosystem, forum and pathways; DS 2026's rows of the area's sheets (W3-F1's prose).
- `scripts/check_ownership.py w3-f1 design-v5`: 28 paths outside — §6 and §16's 23 and the five above (the steward
  assigns them in the manifest at the merge); DS 2026 is W3-F1's prose there (a slice).

## 25. Runs (targeted, V5.5 — one pytest and one browser at a time, `TEST_DATABASE_URL=…/test_ile_v5_l7`)

| Run | Result |
|---|---|
| r1 — the family's files (`test_interior_w3_f1`, `test_orientation_w3_f1`), the bundle, pipeline (a real `collectstatic`), design-docs, chips, icons, O14, state-chip, layout, static-assets, tokens, chips-registry and JS-bundle checks, `apps/ecosystem/tests`, `apps/pathways/tests`, `apps/orientation/tests`, the Forum's page, mode, registration and banner tests, `apps/pages/tests/test_{institutional,templates_static,prescribed_fragments}.py`, `tests/compliance`, `tests/test_regen_design_inventory.py`, `tests/i18n` (`-m "not browser"`) | **1 440 passed, 1 failed**, 58 deselected (29 min 34 s, other lanes' suites beside it): `test_prescribed_texts_are_never_hand_copied_in_templates_or_python` — the M5 notes in `pilot_flow.html` and `_spaces.css` quoted the seventh station's locked word → reworded (the station named by its place) |
| r2 — `apps/ecosystem/tests/test_compliance.py`, `test_css_bundle_is_current.py` (after the rebuild) | 26 passed |
| browser — `tests/frontend/test_browser_w3_f1.py`, `apps/ecosystem/tests/test_browser.py`, `tests/frontend/test_orientation_browser_w3_f1.py`, `tests/i18n/test_rtl_browser.py`, `test_rtl_browser_entrance.py`, `apps/pages/tests/test_browser.py`, W3-A's `test_the_questionnaire_s_foot_is_part_of_its_page_and_the_bar_keeps_its_entries` | **106 passed**, 0 skipped (`-rs`; 11 min 50 s), no crash |
| r3 — after ruff's format, the four line fixes and the last DS wording: the family's two files, `test_design_docs`, `test_css_bundle_is_current`, `apps/ecosystem/tests`, `apps/forum/tests/test_forum_page.py`, `apps/pathways/tests/test_{compliance,views}.py` (`-m "not browser"`) | **411 passed**, 19 deselected (12 min 13 s) |
| axe-core 4.13.0 (W1-0's copy, evaluated through the driver), WCAG 2.0–2.2 A/AA — the four doors, /orientation/, /agami/, /forum/, /forum/inscription/, /projet-pilote/ × fr, ar × 1440, 390 touch (`axe_smoke.py`) | **0 violations** on 36 loads; «incomplete»: color-contrast only (the chrome's text, as the check found); the door card's text 15.33 : 1 (the title) and 9.94 : 1 (the sentence) on the night |
| the lane's probes — `measure.py` (positions, RH-3, overflow, CSP, console, targets; 18 pages), `sections.py` (the fixed sections), `wizard.py` (the questionnaire, fr and ar × 3 sizes) | as in §22 |
| `ruff check .` (CI's lint), `ruff format` on the touched Python; `scripts/regen_design_inventory.py`; `git diff --check` | all checks passed; «current»; clean |

The lane server is stopped and 8787 is free; no browser of this pass is open; the questionnaire's anonymous sessions
created by the probes stay on the lane clone (no personal data), as the check's did. The scratch scripts are in
`C:/tmp/ile_v5_council/.work/w3-f1/w3-f1-fix/`.

---

## Steward — the merge stopped at the shared-CSS gate (12 October 2026, 00:50–02:15)

The steward (label w3-f1-merge). **Nothing was merged**: this step left design-v5 untouched (it stood at `abbabda`,
W2-A's shipped note), v5-live and 8780 as W2-A's merge left them (`v54/w2-a`); no `v54/w3-f1` tag, no
`live_status.json` change. The merge lock was
never taken: W2-A's merge held it from 00:39, W3-F2's from 01:50, and the gate below settles the merge without touching
design-v5. This branch is as the fix pass left it (`14343ac`), plus this section. Evidence:
`C:/tmp/ile_v5_council/evidence/v54/w3-f1/merge/` (`budget_gate.log`, `trial-a.log`); scripts:
`C:/tmp/ile_v5_council/.work/w3-f1/w3-f1-merge/`.

**What was done.** The pre-merge sync rehearsed in a scratch worktree (detached at `14343ac`, removed afterwards):
`git merge --no-commit` of W2-A's branch at `baa88cc`, whose sources are design-v5's at `abbabda` (they differ only
in the JS bundles' chunk names and the steward's status files). Conflicts, both areas kept: `console.css` (the import
list: the shell, W3-B's `v5/_dashboard.css`, then this area's `v5/_wizard.css`), `layout.css` (both sides deleted rules
in one hunk: the union of the deletions), the decision log (design-v5's entries first, this area's renumbered after
them, the fix pass's index row added), DS 2026 (§2's rows design-v5's, regenerated; §2.1's `console.css` row names
both partials; W2-A's `overlay-panels.css` row kept); the bundles deleted and rebuilt (`npm run build`). Found on the
merged tree only — **one semantic conflict**: W2-A deleted `.section--c` and this area `.section--tight`, the two last
consumers of `--rank-c-block`, so DS 2026 §3.12 calls a token used that no sheet consumes
(`test_design_docs.py::test_reserve_labels_match_the_design_system_stylesheets`, red on the merged tree, green on each
branch); the remedy is the row labelled «riserva» (`fix_rank_c.py`). A class-by-class search of what the merge drops
from the bundles: nothing another family's template draws, but the design showcase's (dev) sample foot of the guided
form (`.wiz__foot--sample`), unstyled like the console samples beside it since W3-A. The area's targeted non-browser
tests on the rehearsal (`tests/i18n`, `tests/compliance`, the orientation, ecosystem, pages and pathways apps, the
Forum's public tests, `test_layout`, `test_design_docs`, the two bundle checks, O14, the state chips, the family's
files, the W1-C / W3-A / W1-B test files it touched, `tests/security`, the ownership and inventory tests;
`test_ile_v5_l7`): **1 852 passed**, 91 deselected, 0 failed (38 min 46 s) with the `--rank-c-block` fix in. The browser
batches were not run: the gate had failed by then.

**The gate** — the owner's V5.8 and the orchestrator's reading of it as clarified on 12 October at 01:55 (the V5.8
directive file): «The ceilings are the PAGE-TYPE ceilings recorded in the decision log (as of DL54-95 …: console page
types 50 927 B · interior page 42 540 B · login 47 392 B · home 57 191 B · «Mes pièces» 52 099 B · company dashboard
51 800 B). They are hard … deletions by any family make room under the same ceilings — the ceilings do not drop with
them … A merge that would take ANY page type over its ceiling stops and sends the family back to move its rules into
its page-only sheet or delete what it replaces; quality is not cut to make the number, and the ceiling is never
re-recorded higher.» On the rehearsal's bundles, `gzip.compress(data, 9)` (the stewards' measure):

| Page type | design-v5 `abbabda` | merged | change | ceiling | over by |
|---|---|---|---|---|---|
| console page types (`main` + `console` + `portal`) | 50 893 | 50 675 | −218 | 50 927 (DL54-87 item 3) | — |
| «Mes pièces» (+ `documents.css`) | 52 065 | 51 847 | −218 | 52 099 | — |
| the company's dashboard (+ `companies.css`) | 51 766 | 51 548 | −218 | 51 800 | — |
| an interior page (`main.css` alone) | 42 152 | 40 802 | −1 350 | 42 540 (DL54-73 + DL54-76 item 5) | — |
| the login (+ `entrance.css`) | 47 013 | 45 663 | −1 350 | 47 392 (DL54-76 item 4) | — |
| the home (+ `hero.css`, `pages.css`) | 56 803 | 54 721 | −2 082 | 57 191 (DL54-87 item 3) | — |
| **the persons pages** — /parcours/, the sheets, /diplomes-et-titres/, /formation/ (`main.css` alone → + `pathways/pathways.css`) | 42 152 | **44 185** | +2 033 | 42 540 (an interior page) | **1 645** |
| the ecosystem doors (+ `ecosystem.css`) | 44 084 | 44 082 | −2 | 44 472 (42 540 + the sheet at `v54/w1-c`) | — |
| the Forum (+ `forum.css`) | 44 299 | 44 270 | −29 | 44 687 (the same convention) | — |
| the institutional pages (`pages.css` → `pages/css/interior.css`) | 46 235 | 43 514 | −2 721 | 46 623 (the same convention) | — |
| **orientation** (+ `orientation/wizard.css`) | 43 484 | **44 771** | +1 287 | 43 872 (the same convention) | **899** |

The shared bundles fall — `dist/main.css` 42 152 → 40 802 B, `portal/console.css` 6 809 → 7 941 B (the guided form,
out of `main.css`) — but **the persons page type, an interior page with a recorded ceiling, lands 1 645 B over it**:
those pages loaded `main.css` alone and now load `pathways/pathways.css` (3 383 B: `_interior.css` ≈ 2 600 B gzip on
its own, `_porta.css` ≈ 850, `_pathways.css` ≈ 740). The orientation pages grow by 1 287 B (their sheet 1 332 →
3 969 B: `_interior.css` and the questionnaire's own rules); no figure of theirs is recorded, and by the home's
convention (DL54-44 item 3: `main.css`'s ceiling plus the page's own sheet as it weighed) they are 899 B over. The
merge stops; no ceiling is recorded or lowered. After W3-F2's merge (`main.css` −688 B on `abbabda` by its steward's
measure; one deletion shared with this area) the persons pages would still stand ≈ 1.0 KB over and orientation
≈ 0.25 KB over — an estimate; the budget fix measures on its own sync.

**What the merge needs, on the merged tree** (the orchestrator's levers: reuse, delete what the surface replaces,
page-only sheets; quality is not cut): the persons pages at most 42 540 B, the orientation pages back to their figure,
every other page type under its ceiling (all are today, with room). The levers seen at the gate:
- **delete what the interior replaces, once W3-F2 has landed**: the legacy trail, page header and local navigation of
  `components.css` (§9 ≈ 380 B gzip on its own, §10 ≈ 730, §24 ≈ 500), the pathway list (§18 ≈ 650: the home's?) and
  the timeline (§17 ≈ 720: the case timeline's?), and what is left of `layout.css`'s and `register.css`'s editorial
  parts — each rule only when no template of design-v5 or of any in-flight worktree draws it, proved as W2-A's budget
  fix proved its deletions (DL54-94 item 4); this lowers every page type, the persons and orientation pages with them;
- **one interior grammar, not two**: W3-F2's `static/css/v5/_lettura.css` re-draws the trail and the page header for
  the content pages while `_interior.css` draws them for this area's — V5.8: «no duplicated component families»;
- what the two page sheets carry that their pages do not draw.
Or the orchestrator rules that a page type drawn anew in page-only sheets is recorded as measured — W3-F2's steward is
drafting that reading for its own content, account and error pages (and lowers three ceilings) — and then this merge
passes as measured above, unchanged.

**For the next merge.** design-v5 holds DL54-01 … DL54-95; W3-F2's merge, in progress, takes DL54-96 … DL54-99 by its
draft, so this area's five entries would become DL54-100 … DL54-104 (the steward renumbers at the merge that lands;
`resolve_dl.py` numbers them after design-v5's last). The 27 paths outside the slice after the sync — §6, §16 and §24's
28 less `tests/frontend/test_console_shell_w3_a.py`, which W3-B had changed in the same lines — are listed with their
reasons in `assign_paths.py`, which refuses to write unless `check_ownership.py` reports exactly those. The
`--rank-c-block` row and the three conflicts above recur at the next sync.

---

# Budget and consolidation (the budget pass, `w3-f1-fix`, 12 October 2026)

The orchestrator's DEFINITIVE RULING on the owner's V5.8 (12 October, 02:15; the last section of
`directives/V5_8_CONTINUE_GITHUB_CSS_BUDGET.md`) replaced the reading the steward's gate applied (§«Steward» above):
(1) the shared bundles never rise and ratchet down; (2) page-only sheets are allowed for what a surface draws, after
reuse and deletion, with a performance sanity check, a page type's first page sheet recorded at its measured size;
(3) no duplicated component family — W3-F2's `_lettura.css` redrew the trail and the page header that `_interior.css`
draws too, and this area, merging second, consolidates them. The pass waited for `v54/w3-f2` (present at 02:40, on
`bfd2901`), merged design-v5, consolidated, deleted, trimmed, measured. Lane 7 (127.0.0.1:8787, `ile_v5_l7`,
`ILE_REFERENCE_DATE=2026-10-03`, `DB_CONN_MAX_AGE=0`, `--noreload`, no preview flag); one headless Chromium at a time
with its own profile (`.profiles/w3-f1-fix-budget/`); one pytest at a time on `test_ile_v5_l7`;
`PERFORMANCE_BENCHMARK_LOCK` checked before every browser series and build (never present); no run crashed. Signed-in
pages through one session minted with `Client.force_login` on `ile_v5_l7` (`seed-person`; no password used, typed or
stored), revoked at the end. Decision log: **DL54-105**. Evidence: E/ = `C:/tmp/ile_v5_council/evidence/v54/w3-f1/budget/`
(`snap/<state>/<set>/` a full-page PNG and the computed style of every element per page × language × width;
`cmp_*.txt` the comparisons; `weigh_final.txt`; `perf/`; `proof_*.txt`, `coverage_r1.log`; `firstscreen/`, `contact/`);
scripts: `C:/tmp/ile_v5_council/.work/w3-f1/w3-f1-fix/budget/`.

## 26. The sync (`76429f2`)

design-v5 at `v54/w3-f2` merged (106 commits). The steward's scripts were the guide, brought up to the tree with W3-F2
on it (`resolve_sync.py`): `console.css` — W3-B's dashboards, then this area's guided form; `layout.css` — both sides
deleted rules in one hunk, the union; DS 2026 — §2 design-v5's rows then `scripts/regen_design_inventory.py --write`
(the `v4/wizard.css` row out), §2.1 design-v5's rows (W2-A's overlay panels, W3-F2's three page sheets) with this
area's `console.css` clause and its `forum.css`, `wizard.css` and `wizard.js` rows, §10's `local_nav.html` (no page
includes it), §10.1 both areas' rows; the decision log — design-v5's entries first, this area's five renumbered after
DL54-99 (below); `--rank-c-block` labelled «riserva» in §3.12 (`fix_rank_c.py`); `static/css/dist` and `static/js/dist`
deleted and rebuilt (`npm run build`). Before anything else changed, the targeted documents and bundle checks and both
families' files: 187 passed, 1 failed — §10's `local_nav.html` still cited allauth's manage layout as its consumer
(W3-F2 replaced it with the account's own section list): fixed with the consolidation.

## 27. One partial for the public interior's shared components — `static/css/v5/_pagina.css` (`7cdaba8`)

| Component | drawn once in `_pagina.css` | each surface keeps |
|---|---|---|
| corners | `--card-radius: var(--radius-md)` on both body scopes | — |
| the trail | its box (13/20, `--s-4` above), the items' ink, the 6 px chevron in `--text-3`, each link a 24 px box (`inline-block`, 2 px), its target 44 px under a finger (`::after`, 10 px above and below; rows 20 px apart), the hover under a hovering hand, the current page in ink at 500 | — (`_interior.css` and `_lettura.css` draw no trail) |
| the head | one drawing for the two vocabularies — W3-F1's `.ingresso` (`__label`, `__title`, `__lead`, `__meta`) and W3-F2's `.page-header` (`__eyebrow`, `__title`, `__lead`, `__meta`, `__contact`): the space, the label, the h1 at 28/36 → 36/44, the capitals tracked, the lead at 17/28 → 20/28 | W3-F1: the entrance's grid and end seat (the door card, the action card, the index); W3-F2: the head's seat with its search, the glyph, the contact line, a lead of several blocks, the label as written |
| the chapters | the band (48 → 64 px), the hairline under the head and between bands, the grid (the head on four columns of twelve, the body on eight, from 75rem; the head sticky), the mark, the title, the lead, the body, the quiet label, the row of links' container | W3-F1: the anchor under the letterhead, the area band, the body's rhythm, the statement, prose, small print, the lead's rise from 48rem, its forward links' boxes, the quiet chapter's space; W3-F2: its quiet chapter's space, its list of links, the rhythm of a body (written last, so it wins), the legal page |
| the register | the rows on shared hairlines, the title, the text, a row's chip, two columns from 48rem | W3-F1: titles in ink, the whole row the target, a fragment, a row still being prepared, the glyph rows, the word rows; W3-F2: titles in the link's colour, the row as one link only in `registro--links`, its meta, the links inside a row |
| D26's shared slots | an authority's host, a photograph (`--card-radius`, the passe-partout) and its caption, «who can help me» and its one-box address | the inset and the action card (W3-F1); the verification line, prose, the fine print, the sources (W3-F2) |
| print | the chapter head unstuck | its own |

The six page sheets import it first: `pathways/pathways.css`, `ecosystem/ecosystem.css`, `forum/forum.css`,
`pages/css/interior.css`, `orientation/wizard.css` (W3-F1) and `cms/lettura.css` (W3-F2); then the surface's own
partial(s). A shared rule carries one selector (the body scopes the two partials used are not needed: the page sheets
load after main.css, so equal specificity wins by order; none of them loads on a console page). The service pages'
sheet (`_servizio.css`, W3-F2's step 2) keeps its own trail and help line by its design («only what these pages draw is
restated here»): the account and error pages draw none of the head, chapters or register, and importing the shared page
would load rules they never draw (rule 2) — the remainder of W3-F2's review m11, recorded rather than traded.

**Measured** (`snap.py` + `compare.py`: every pixel and the computed style of every element, its `::before` and
`::after`, 148 captures — W3-F2's twelve pages, W3-F1's seventeen, the home, seven signed-in pages; fr and ar; 1440
and 390; the noise floor measured by a second identical run: 148 / 148 identical once the chrome's JS state at capture
time and the 500 page's reference are set aside): **W3-F2's pages, the home and the signed-in pages identical (80 of
80).** W3-F1's pages take W3-F2's drawing where the two differed — three changes, each one drawing now: the trail's
links are 24 px boxes whose target grows to 44 px under a finger (they were 44 px boxes everywhere: `--hit-min` still
carries V4's 44 px through `v5/aliases.css`, so the fix pass's «boxes on `--hit-min` (24 px)» were 44 px boxes — the
trail now sits 20 px tighter above the entrance, as on W3-F2's pages); «who can help me»'s address is one box
(`inline-block`, as on W3-F2's pages); the quiet chapter's label is untracked (the h2's −0.26 px was the title's
tracking on a 13 px label). CSS (gzip −9): W3-F1's page types +179 … +183 B, the content pages +61 B (the head's two
vocabularies in one drawing, the trail's touch target) — paid back by §28 and §29.

## 28. What left the shared bundle, and the proof (`057f4fd`)

The proof for each rule: `class_uses.py` (every template, Python, JS and JSON file of the merged tree, and the files
each in-flight worktree changed against its merge base — v54-w3-c, v54-w3-d, v54-w2-c2, v54-devops and the W3-C trial
worktree; a component template checked for the templates that include it) and `dead_rules.py`, then the 148-capture
comparison (E/`proof_prefix.txt`, `proof_hero_word.txt`, `cmp_dele.txt`).

| Rule(s) | Why it could go |
|---|---|
| `components.css` §9: `.breadcrumbs` (box, type), `.breadcrumbs__item a`, `a:hover`, `[aria-current]` | every page that draws a trail re-draws them: the shared page (`_pagina.css` §1), the account pages (`_servizio.css` §1), the console's bar (`_shell.css` §3); the skeleton — list, item, chevron, its mirror — stays, read by all three |
| §10: `.page-header` (box), `__title`, `__lead`, `__meta`, `--center` (+ its children); the label reduced to capitals and case-sensitive forms | re-drawn by the shared page and the console's frame (`_shell.css` §4); `--center` has no caller; the console still reads the running head's capitals |
| §10: the legacy hero (`.hero`, `__eyebrow`, `__title`, `__subtitle`, `__body`, `__actions`, `__figure`, `__rule`, `--inverse`, `--muted`, `--compact`) | `components/hero.html` has no includer (the home's hero is `.he*`, W2-D) |
| §24: the local navigation (`.local-nav*`, 12 rules) | `components/local_nav.html` has no includer since this area's doors and institutional pages and W3-F2's account pages; the QA probe `scripts/qa_chrome_signin.py` only reads link texts with it |
| `register.css`: the page header's capital titles | re-drawn by the shared page (`--track-display-caps`) and the console's frame; DS 2026 §3 labels `--track-caps-display` «riserva» (its last consumer) |
| `register.css`: the folio in `.zones__rail`, the gloss in `.zones__margin`, `.plate--verso` (6 rules), the home plate (`.home-plate__*`, the verso buttons) | no template draws the zones' rail or margin, the verso plate or the home plate |
| `layout.css`: `.zones__content > .prose`, `.layout-sidebar` (+ its aside), `.rule--accent` | no template; the sidebar's last consumer, allauth's manage layout, left with W3-F2 |
| `_lettura.css`: the resets of the legacy page header (its box's rule and space, the label's face and tracking) | dead once §10's box and label left; the label stays reset from the console's capitals |

Together: `main.css` 40 215 → 39 313 B gzip (−902) on every page; `cms/lettura.css` −16 B more (its dead resets).

Left, because something still draws them: §17 the timeline (the design showcase's sample; W3-D retires it with
`components/timeline.html` once this merge lands, its NOTES «For W3-F1» item 4), §19 the CTA panel (the console's access
point), the jurisdiction bar (a component W2-D kept on purpose), the outcome's modifiers (composed in templates:
`outcome--{{ … }}`), the sequence's crossing (W3-D deletes it on its branch), `.section--d` and `.section--process`
(documented by DS 2026 §3's ranks; W4-D's sweep), §2's two dead icon modifiers and §12's (W1-B's and W2-E's sections).
Comparison: 148 of 148 captures identical to the consolidated state.

## 29. A page sheet holds what its pages draw (`f058ef4`)

- **The pathway list leaves the shared sheet for its one consumer's.** `components/pathway_list.html` is included by
  `templates/pages/home/_pathways.html` alone (this area's doors draw the pathways as a register). The home's `pages.css`
  already re-drew the list; of §18 it still read two things — the titles' face (`--font-display`: Host on the Arabic
  page, where the row's ground is Vazirmatn) and the stretched link — which its own rules now say. `main.css` −202 B on
  every page; the home −183 B.
- **`_interior.css`'s one-surface rules go to that surface's partial** (`coverage.py`: the page sheet's CSSOM against
  every page of its type, fr and ar; then a grep of every template, because a state not visited — a pending row, a
  photograph — still counts): the wide chapter → `_spaces.css` (the pilot alone); the register whose rows name WHO →
  `_institutional.css` (/reseau/, /le-projet/); a row's fragment, a row still being prepared and what is still being
  verified → `_pathways.css`. Each at the top of its partial, where it stood in the cascade. «la linea» stays in
  `_interior.css` for W3-D, which moves it into `_journey-passage.css` and imports it in the sheets that draw it (its
  NOTES «For W3-F1» item 1), so the Forum and the institutional pages shed it then.
- Comparison: 144 of 148 captures identical; the home's four differ only in the computed style of its hidden numerals
  (`display: none`, §18's colour and size gone) — no pixel moved.

## 30. Before → after, page type by page type (gzip −9 of bundles rebuilt from a clean dist; E/`weigh_final.txt`)

| Page type | design-v5 `v54/w3-f2` | the sync | consolidated | deleted | **final** | final − design-v5 |
|---|---|---|---|---|---|---|
| `main.css` — every page (SHARED) | 41 464 | 40 215 | 40 215 | 39 313 | **39 111** | **−2 353** |
| the console page types: main + console + portal (SHARED) | 50 205 | 50 088 | 50 088 | 49 186 | **48 984** | −1 221 |
| «Mes pièces» (+ documents) | 51 377 | 51 260 | 51 260 | 50 358 | **50 156** | −1 221 |
| the company's dashboard (+ companies) | 51 078 | 50 961 | 50 961 | 50 059 | **49 857** | −1 221 |
| the login (+ entrance) | 46 325 | 45 076 | 45 076 | 44 174 | **43 972** | −2 353 |
| the home (+ hero, pages) | 56 115 | 54 134 | 54 134 | 53 232 | **53 049** | −3 066 |
| **the persons pages** (main → + `pathways.css`, their first page sheet) | 41 464 | 43 598 | 43 777 | 42 875 | **42 605** | **+1 141** |
| the ecosystem doors (+ `ecosystem.css`) | 43 396 | 43 495 | 43 678 | 42 776 | **42 446** | −950 |
| the Forum (+ `forum.css`) | 43 611 | 43 683 | 43 865 | 42 963 | **42 605** | −1 006 |
| the institutional pages (+ `pages.css` → `interior.css`) | 45 547 | 42 927 | 43 110 | 42 208 | **41 908** | −3 639 |
| **orientation** (+ `orientation/wizard.css`) | 42 796 | 44 184 | 44 363 | 43 461 | **43 150** | **+354** |
| the content pages (+ `cms/lettura.css`) | 45 520 | 44 271 | 44 332 | 43 414 | **43 212** | −2 308 |
| the account pages (+ `cms/servizio.css`) | 43 890 | 42 641 | 42 641 | 41 739 | **41 537** | −2 353 |
| the error pages (+ `cms/errori.css`) | 45 093 | 43 844 | 43 844 | 42 942 | **42 740** | −2 353 |

The shared payload falls on every page (`main.css` −2 353 B; the console page types −1 221 B, `console.css` +1 132 B
carrying «Ma situation»'s guided form out of `main.css`, DL54-103). Every recorded ceiling of DL54-99 holds with room.
Two page types grow, each through its own page-only sheet, for what its pages draw (V5.8 rule 2): the persons pages,
which had no sheet before (their first: the shared page, W3-F1's own parts, the door card, the pathways' rules), and
orientation (its V4 sheet replaced by the interior's grammar and the questionnaire's rules) — for the steward to record
as measured.

## 31. The performance sanity check (V5.8 rule 2; E/`perf/`)

The lane (dev server: uncompressed static, so the CSS bytes weigh more than in production), CPU ×4, 150 ms RTT,
1.6 / 0.75 Mbps, a fresh context a load, one discarded warm-up a cell; design-v5 at `v54/w3-f2` served from an export of
its tree (removed afterwards, with its copy of `.env`) and the branch, in blocks design-v5 · branch · branch ·
design-v5 · branch, n = 8 a cell a block; the medians of the block medians:

| Cell | LCP design-v5 → branch (ms) | FCP design-v5 → branch (ms) | LCP element |
|---|---|---|---|
| the person door, fr 1440 | 1 897 → 1 902 (blocks 1 890 – 1 926) | 1 812 → 1 796 | the entrance's lead, both |
| a pathway sheet, fr 412 | 1 935 → 1 922 | 1 818 → 1 806 | the entrance's lead, both |
| orientation's first page, fr 412 | 1 937 → 1 912 | 1 831 → 1 790 | the entrance's lead, both |
| the person door, ar 412 | 2 097 → 2 134 (blocks 2 094 – 2 146 against 2 082 – 2 112) | 1 965 → 1 948 | the entrance's lead, both |

FCP equal or earlier in every cell (`main.css` 222 → 205 KB uncompressed); LCP within the series' spread everywhere
(+37 ms at most, on the Arabic door, whose blocks overlap). No meaningful LCP or first-render regression (V5.5).

## 32. Review fixes — what this pass changed in them

The review's five majors and eight minors and the check's three findings stand fixed as «Review fixes» (§20–§25)
records; this pass changed one fix and corrected one figure:

| Finding | Change in this pass | Evidence |
|---|---|---|
| A11Y finding 1 (SP-8) | The trail's targets are the shared page's — W3-F2's drawing: a 24 px box at rest, 44 px under a finger through its `::after`, rows 20 px apart; the forward links keep their boxes. The fix pass's «24 px» boxes were 44 px (`--hit-min` = 44 px through `v5/aliases.css`): DL54-105 item 2 corrects DL54-104 item 6 | `cmp_consol.txt`; `test_browser_w3_f1.py::test_the_trail_and_the_forward_links_stand_on_the_target_floor` now probes the target (a point 21 px above and below a link's middle lands on it under a finger, 11 px with a mouse): 2 passed |
| A11Y finding 3 (the page types' CSS) | Re-measured and lowered (§30): the shared payload −2 353 B; the persons pages and orientation the two page types over design-v5's figures, by their page sheets | `weigh_final.txt`, `perf/` |

## 33. Not done, and why — and what is handed on

- **The service pages' trail and help line** (W3-F2's `_servizio.css` §1, §4) stay their own: the account and error
  pages would otherwise load the whole shared page (§27). If a third surface ever draws the trail alone, a trail-only
  partial is the next step — **handed to W3-F2 / the steward** (m11's remainder).
- **`--hit-min`** still carries V4's 44 px in the effective cascade (`v5/aliases.css`, «until its owning family
  retargets the consumers»): a V5 partial that writes `var(--hit-min)` gets 44 px. **Handed to W4-D** (the aliases'
  sweep); this area's forward links keep their 44 px boxes meanwhile (compliant, taller than meant).
- **Orphan component templates** — `components/hero.html` and `components/local_nav.html` (no includer, now no rules),
  `components/timeline.html` (the showcase only; W3-D's), `components/cta_panel.html` (the showcase; its rules stay for
  the console's access point): their DS 2026 §10 entries say so; deleting the files and their entries is **W4-D's**
  sweep of the component catalogue (and `ecosystem.services.local_nav`, now unused, with them).
- **§17 the timeline** — W3-D's planned retirement (above). **«la linea»** — W3-D's planned move (above).
- **The design showcase** (`/_design/`, dev only) loads `main.css` alone: its samples of the trail and of the page
  header lose the legacy box, type and colours §9 and §10 gave them (as its guided-form and console samples did with
  W3-A and W2-A); the product's pages draw both through their sheets.
- **`.section--d` / `.section--process`, the jurisdiction bar** — documented or kept on purpose by others: W4-D, W2-D.

## 34. Paths outside the slice — this pass's, beside §6, §16 and §24

`scripts/check_ownership.py w3-f1 design-v5`: 54 inside, 17 slice, 24 generated, **31 outside** — the steward's 27
(§«Steward») and four new, each the consolidation's:
- `static/css/v5/_pagina.css` (new: the shared page of the public interior — both families' page sheets import it);
- `static/css/v5/_lettura.css` (W3-F2's partial: the shared components out, the dead resets of the legacy page header
  out; W3-F2's words kept wherever its rules stay);
- `apps/cms/static/cms/lettura.css` (W3-F2's entry: the shared page imported first);
- `tests/frontend/test_content_pages_w3_f2.py` (W3-F2's test: its entry's exact import list).
Touched again, in the slice or the shared files' slices: `static/css/components.css`, `layout.css`, `register.css`
(the deletion map's rows «W3-F1 / W3-F2, by page», §18 by its one page), `apps/pages/static/pages/css/pages.css` (the
pathway list's whole drawing), DS 2026 (the component entries, §3's reserve, §2.1's rows, regenerated §2).

## 35. Tests and runs (targeted, V5.5 — one pytest and one browser at a time, `TEST_DATABASE_URL=…/test_ile_v5_l7`)

| Run | Result |
|---|---|
| after the sync — DS 2026, the bundle and inventory checks, both families' files (`-m "not browser"`) | 187 passed, 1 failed: §10's `local_nav.html` still cited allauth's manage layout → fixed (§26) |
| after the consolidation — the same set, `test_orientation_w3_f1` | first 256 passed, 7 failed — the expected ones: the four page sheets' and orientation's import lists, the trail's rules read in `_interior.css`, §10's `local_nav.html` — retargeted (§27); then 222 passed, 1 failed: the new test's duplicate-rule check also caught a descendant rule (`.registro__row :is(…) a`) → narrowed to a rule whose selector is the shared one; then the two tests: 2 passed |
| after the deletions — the documents, bundle and inventory checks, both families' unit files | 235 passed, 1 failed: `--track-caps-display` documented as used, its last consumer gone → DS 2026 §3 labels it «riserva»; then `test_design_docs`, the inventory: 46 passed |
| after the trims — the documents, bundle and inventory checks, both families' unit files, `apps/pages/tests/test_home.py`, `test_layout` | **278 passed** (10 min 13 s) |
| r1 — the targeted batch (`-m "not browser"`): `tests/i18n`, `tests/compliance`, `apps/orientation/tests`, `apps/ecosystem/tests`, `apps/pages/tests`, `apps/pathways/tests`, the Forum's page, mode, registration and banner tests, `test_interior_w3_f1`, `test_orientation_w3_f1`, W3-F2's `test_content_pages_w3_f2` and `test_service_pages_w3_f2`, `test_layout`, `test_design_docs`, `test_css_bundle_is_current`, `test_frontend_bundle_is_current`, `test_static_pipeline` (a real `collectstatic`), O14, the state chips, the icons, the inventory, the console sheets' and the template comments' checks | **1 555 passed, 1 failed**, 91 deselected, 0 skipped (31 min 37 s, other lanes' suites and browsers beside it): `apps/ecosystem/tests/test_compliance.py` read `ecosystem.css`'s old import list → retargeted, with W1-C's chip test (the register row's chip is placed by `_pagina.css` now): **38 passed** |
| b1 — `test_browser_w3_f1` (the target probe), `test_orientation_browser_w3_f1` | **23 passed**, 0 skipped |
| b2 — `apps/ecosystem/tests/test_browser.py`, `apps/pages/tests/test_browser.py` (the home among them) | **47 passed**, 0 skipped |
| b3 — `tests/i18n/test_rtl_browser.py`, `_entrance`, `_nav`, `_overlays` | **44 passed**, 0 skipped |
| b4 — W3-F2's `test_content_pages_browser_w3_f2`, `test_service_pages_browser_w3_f2` | **16 passed**, 0 skipped |
| the lane's probes — `snap.py` × 5 states (148 captures each), `compare.py`, `coverage.py`, `perf.py` × 5 blocks, `weigh.py`; `class_uses.py`, `dead_rules.py` | as in §27 – §31 |
| `ruff check` and `ruff format --check` on the touched Python (W1-C's chip test left in its own format: one entry changed); `scripts/regen_design_inventory.py`: current; `git diff --check`: clean | passed |

No browser run crashed. The lane server is stopped and 8787 is free; no browser of this pass is open; the minted
session is revoked (1 row) and its secrets file removed; the pass's browser profiles and the design-v5 export (with its
copy of `.env`) are deleted. The scratch scripts are in `C:/tmp/ile_v5_council/.work/w3-f1/w3-f1-fix/budget/`.


## How to read the decision-log numbers written before this pass

W3-F2's merge (DL54-96 … DL54-99) reached design-v5 first, so at the sync this area's five entries became **DL54-100 …
DL54-104** — the same order, add 22 —, content unchanged but for their cross-references; the index gained the fix
pass's row. This pass is **DL54-105**; the steward's record of this merge will be DL54-106. In this file, `REVIEW.md` and
`A11Y_PERF.md`, every DL54-78 … DL54-82 written before 12 October is the family's own: 78 → 100 (step 1, the interior
as built), 79 → 101 (step 1, the page sheets and the CSS), 80 → 102 (step 2, orientation and the advice pages), 81 →
103 (step 2, «Ma situation»'s guided form), 82 → 104 (the fix pass). The «Steward» section's DL54-96 … DL54-101 were its
draft before W3-F2 landed: read them as DL54-100 … DL54-104 and DL54-106. The accessibility report's «DL54-87» is
design-v5's own (the console page types' ceiling).

## How to read the decision-log numbers — after the steward's sync (12 October 2026)

Between the budget pass's sync and the steward's merge, design-v5 took W2-C2's entries DL54-100 and DL54-101 and the
record of its merge, DL54-102: that merge reached design-v5 first. At the steward's sync this area's six entries were
renumbered after them, the same order, add 3: 100 → 103 (step 1, the interior as built); 101 → 104 (step 1, the page
sheets and the CSS); 102 → 105 (step 2, orientation and the advice pages); 103 → 106 (step 2, «Ma situation»'s guided
form); 104 → 107 (the fix pass); 105 → 108 (the budget and consolidation pass). Their content is unchanged but for their
own cross-references (each DL54-100 … DL54-105 inside them, which was always this area's own, moved with them). **The
steward's record of this merge is DL54-109.** In this file, `REVIEW.md` and `A11Y_PERF.md`, read every number this area
wrote for itself with both mappings: DL54-78 … DL54-82 (written before 12 October) → DL54-103 … DL54-107; DL54-100 …
DL54-105 (the budget pass and the section above) → DL54-103 … DL54-108; the «Steward» section's draft DL54-96 … DL54-101
→ DL54-103 … DL54-107 and DL54-109. design-v5's own numbers (DL54-99 and below, the accessibility report's DL54-87) did
not move.
