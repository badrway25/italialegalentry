# V5.24 lane PUB2 — system, trust and reading: the professional pass (label v524-pub2-build)

Branch `v524-pub2` (worktree `C:/tmp/ile_wt/v524-pub2`), cut from `design-v5` at `4e882904` (the v524-lib merge: lanes S, M, P1,
S2, H, P2, PX, T and LIB merged). Lane server 8789 on the lane database `ile_v5_l5` (dev settings, `ILE_DESIGN_PREVIEW=1`,
`ILE_REFERENCE_DATE=2026-10-03`; the clone in step with `ile_v5`: 75 migrations, 19 users, no refresh needed); pytest on
`test_ile_v524_pub2` (the browser set on `test_ile_v524_pub2b`, one pytest at a time per database); headed `chromium-1234` under a
Chromium lock slot (label `v524-pub2-eye`); headless probes and the browser twins without a slot (R12). Binding: V5.24 §7–§10,
§11–§14, §19 (the second page group), V5.25 (known defects, targeted checks, no score loops), V5.26 §1–§2, §5–§9 (the FAQ list,
not every section interactive, the abstraction rule, §9's question), V5.20 (the strict test rule), V5.27 (the Arabic hybrid —
applied by lane AR; this lane changes no locked text and no `lang` box), `FINAL_DELIVERY_V2.md` §0–§2 (R3 the «raccordo», R4 a/e
the budgets never raised, R7 the Arabic wraps that touch this lane's templates, R9 KEEP wherever the composition passed, R10 the
real tools, R12, R14) and §3.6; `evidence/v524/BACKGROUND_MATERIAL_V2.md` §3.1–§3.4, §5.2; `TYPOGRAPHY_V2.md` §4.2, §5, §6 with
lane T's contract (`QA/v524/t/NOTES.md` §4) and lane LIB's (`QA/v524/lib/NOTES.md` §4: the raccordo as built, its placement rule);
`IMAGERY_ATTRIBUTION.md` D3–D5 as lane PX applied them; `ARABIC_AUDIT.md` + `arabic/02_class_b_wraps.md` W1.2, W1.3, W5.3 and the
fragments. Evidence of this lane: `C:/tmp/ile_v5_council/evidence/v524/pub2/` (`shots/` the headed stills, `headed_measures.json`,
`geom_*.json` the headless geometry); scratch `C:/tmp/ile_v5_council/.work/v524-pub2/` (`tools/`: `edit1_templates.py`,
`edit2_css.py`, `measure.py`, `probe.py`, `geom.py`, `coverage.py` + `coverage_filter.py`, `headed_shots.py`, `run.sh`, `serve.sh`;
`logs/`: the builds, the measures, the coverage reports, the test logs).

## §R. Recovery inventory (6 Nov 2026, label v524-pub2-build, resumed run; V5.28 RECOVER → COMPLETE)

The previous build agent died on the account's credit outage; its work is the checkpoint `decdacb2` («WIP recovery: …») on
`4e882904`. Nothing was recreated, reset or regenerated; this run builds on that commit.

- **Files already changed** (`git diff --stat 4e882904 decdacb2`: 40 files, +965 −142): the templates of §2 (FAQ, glossary
  index + term, living/topic, Forum hero / presentation / permanent sections, project, agami, antifraud, `_canali`,
  `_rete_pannelli`); the sheets `_faq-v2`, `_lessico-v2`, `_forum` + `forum.css`, `_agami`, `_canali`, `_contatto`, `_frodi`,
  `_projet`, `_rete`, `interior.css`, NEW `projet.css`; `apps/faq/services.py`; the tests `test_interior_v522.py`,
  `test_materia_v524_lib.py`, `test_typography_v2.py` (V5.20 slices) and the two NEW lane modules; the rebuilt dist (8 sheets);
  this file and the one line of `QA/v522/p2/NOTES.md`.
- **Implementation completed**: every row of §3.6's table (§1–§2 below) — the grounds, the incastro, the raccordo, the label
  role, the steps, PX's guards, AR's wordings, the Privacy Policy run; the budgets measured (§6); the headless probes (§7).
- **Implementation incomplete**: §8 (test counts) and §9 (the headed eye) TBD; the V5.29 FAQ priority (§10–§13 of V5.29: the
  semantic icon set, lighter titles, the open choreography, the search / filter / deep links / related) not started — it
  needs design-v5's SYS merge (the ink roles, the weight map, `.sez-tile`'s vault and `--tile-ink`) merged first.
- **Tests already written**: `tests/frontend/test_pages_v524_pub2.py` (static, 27 cases), `test_pages_browser_v524_pub2.py`
  (browser), and the V5.20 slices above.
- **Tests already passing** (re-run now on `decdacb2`, `test_ile_v524_pub2`, `-m "not browser"`: the two lane modules,
  `test_materia_v524_lib.py`, `test_typography_v2.py`, `test_interior_v522.py::test_the_family_sheets_…`): **188 passed,
  5 failed**. The earlier browser run (`logs/browser1.log`) 71 passed.
- **Remaining defects** (the five reds): (1) `interior.css`'s comment names `_materia.css`, which the two import guards
  read as text (`test_interior_v522.py` and the lane's route-sheet test) — the comment says «the material partial»;
  (2) the lane's label test counted two channel kinds, the WhatsApp channel being drawn only where the number is configured
  (option B; unset in the test environment) — every rendered kind carries the role, and the template's two kinds are read
  from its source; (3) Vivre's accepted touch was written with section names its markup does not carry (the panorama has no
  `data-sec`, the second band is `mosaico`) — the touch is recorded under the names the page renders (KEEP whole, one
  ground by decision).

## 0. The decision in one screen

The second page group takes the material and the type roles the Director decided — nothing else (R9): the FAQ explorer, the
glossary register, the term page's scheda, the Forum's «dal dialogo ai progetti», AGAMI's identity band and the fraud page's one
band on STONE, the two «il rimando» strips on PAPER (0 B: attributes); two seams drawn with LIB's primitives — Le projet's
«incastro» (the doors' arched tops the whole 64 px over the volumes) and the Forum's «raccordo» (the stations' line starts in the
pair's foot and lands with its node on the band's head line); the mono folios of the FAQ category, AGAMI's registers, the Réseau
hub and the channels' kind become the label role by name (`t-label`); every clamp of the lane's sheets reads the twelve steps
(the two addresses through container queries), every Arabic rule stands in the subject form; the Forum eyebrow and the theme
page's sentence take AR's wordings; PX's guard reaches the Forum's two bylines; «Privacy Policy» is an isolated English run in the
FAQ's links. Two things the letter did not foresee were decided here and are recorded (§6): the material partial reaches the
institutional pages through a route sheet of Le projet's own (the Réseau and AGAMI totals could not take it on the shared sheet
— R4 a), and the doors' band carries its head in the outline only (a visible head would have stood over the photograph, not the
doors). The term page's «pietra» was conditional on `_lettura.css` freeing ≈ 770 B: the coverage pass freed nothing that a
template does not still name (§6), so the band takes stone, as R4 e says. No page total raised, `main.css` untouched (32 695 B),
0 JS, 0 images, no migration; the catalogue +2 msgids (AR's renderings, §5) − 2 (the retired wordings).

## 1. What the owner sees, where

| Page | What changes |
|---|---|
| FAQ | the explorer on stone: the index rows and the white answer sheet read as a sheet on a desk, the cut from the paper head is real; «Pour aller plus loin» on paper before the night footer; the category's name «Général» in the label role (Host Grotesk 13/16 600; Readex Pro 14/20 in Arabic — no mono); «Lire la Privacy Policy» with the policy's name as its own English run |
| Glossaire | the register on stone (the white term cards become plates on a ground), the rimando on paper; the drawn letters at 600 |
| a term page | the scheda band on stone — the raised definition plate on a ground, the page no longer one tone from head to foot; the term at display size (44 → 64, 600) under the compact head; the outlined initial on the scale (4.5 display steps: 198 → 288 px) |
| Le projet | the panorama's frame ends on the seam and the four night doors rise 64 px into the volumes; the band's title lives in the outline (the doors name their spaces); the French statement column at the reading measure and, on the Arabic page, at its Latin leading; the caps title at 24/30 |
| Forum | «dal dialogo ai progetti» on stone (night → paper → stone → night → stone); a 2 px structure line rises 48 px (32 on phones) into the pair's foot and runs down to the band's head line, where its teal node lands — from 64 rem on the objectives' station axis, the title stepped onto the stations' text axis and the grey route line run up to the node: one line from the pair's foot to the arrival; the eyebrow «Dialogue institutionnel permanent» (it/en/ar through the catalogue, no French branch); the titles on the band step |
| AGAMI | the identity band on stone with the colonnade plate's face raised; the plate's label and every register label in the label role — in Arabic, Readex Pro instead of the mono's system fallback; the address on the steps its column holds |
| Fraudes | the one body band on stone: the report plate and the route tiles as plates on a ground; the address on the steps its plate holds |
| Réseau · Contact · Vivre | the labels through the role (the hub's «En bref», the channels' «Numéro vert» / «WhatsApp»); nothing else moves (KEEP whole) |

## 2. What changed (files owned per §3.6)

**Templates.** `faq/index.html` (the explorer `data-ground="stone"`, the rimando `"paper"`, `t-label` on the single category's h2);
`glossary/index.html` (the register stone, the rimando paper); `glossary/term.html` (the scheda stone); `pages/project.html`
(`data-incastro` on `.projet-porte`, the head `hidden=True`, `{% block route_sheet %}` → `pages/css/projet.css`, `{% load static %}`);
`forum/partials/presentation.html` (the filo stone, `<span class="sez-raccordo" data-verb="draw-y" aria-hidden="true">` as the
band's FIRST child); `forum/partials/hero.html` (the eyebrow msgid «Dialogue institutionnel permanent», the `lang="fr"` branch and
its comment deleted — W1.2; the byline guarded by `event.hero_image.attribution_required` — PX D4); `forum/partials/permanent_sections.html`
(`media.attribution_required` — PX D4); `pages/agami.html` (the identity band stone; `t-label` on `.agami-id__etichetta`, the
registers' `dt`s and the two `.agami-id__etichetta-voce`); `pages/antifraud.html` (the band stone); `living/topic.html` (the meta
description's sentence — W1.3); `pages/partials/_canali.html` (`t-label` on the two kinds — the links, names, numbers and `bdi`
untouched: the channels' architecture is preserved, §9.8); `pages/partials/fronte/_rete_pannelli.html` (`t-label` on the hub's h2).

**Sheets.** `cms/_faq-v2.css` (the category: layout + colour, the role draws the type; the `--titolo` variant on `--t-band`
600); `cms/_lessico-v2.css` (the letters `--w-display`; the term title on `--t-display` through
`.page-glossary-term [data-fronte][data-compact] .ingresso__title` — the compact head's title-2 loads after the route sheet;
`.scheda__iniziale` `calc(var(--t-display) * 4.5)`; the Arabic rule in the subject form; the `.vivere-panorama__quadro .foto__credit`
rule deleted — PX D3); `forum/_forum.css` (`.forum-titolo` on `--t-band`; the raccordo's placement — `--risalita` a strip's measure,
`--sez-raccordo` the rise plus the band's padding, `--raccordo-x` from the layout's tokens: the container's margin below 64 rem,
the second column's start + 11 px from 64 rem; the objectives' title `padding-inline-start: var(--s-12)`; `.forum-obiettivi::before`
run up by the title's line and margin; the dead `.forum-cta__actions` rule and the `.forum-action` print selector gone);
`forum/forum.css` (imports `_materia.css` after `_sigillo.css`); `pages/_agami.css` (the plate `--surface-raised`; the labels'
type gone to the role; `.agami-id__nome` on `--t-band`; the Arabic descendant rule gone; the address `--t-body` → `--t-entry` at
`@container (min-width: 18rem)` → `--t-band` at 24 rem); `pages/_rete.css` (the hub label's type gone to the role);
`pages/_contatto.css` (the title on `--t-band`; the doors' drawing for `.contatto-porte` — the arrow's shift, the words under
the arch, the keyboard rule — now here, since `_projet.css` is Le projet's alone); `pages/_frodi.css` (the title on `--t-band`;
the address `--t-body` → `--t-entry` at 18 rem); `pages/_canali.css` (the kind: colour only; the Arabic rule gone; the number on
`--t-band` from 48 rem); `pages/_projet.css` (`.projet-panorama { padding-block-end: 0 }`; `.projet-porte .testa { margin: 0 }`;
the steps' French paragraphs `font-size: var(--t-lead); line-height: var(--t-lead-lh)` — F-7; the statement column
`max-inline-size: var(--measure-body)` — F-8; the caps title 24 / `--t-band-lh`; the doors' rules narrowed to `.projet-porte`);
`pages/interior.css` (no longer imports `_projet.css`); NEW `pages/projet.css` (`_materia.css` + `_projet.css`, linked by
`project.html` between `interior.css` and `fronte.css`).

**Python.** `apps/faq/services.py`: `context_links()` renders a label whose text holds «Privacy Policy» with that run in
`<span lang="en" dir="ltr">` (`format_html`; the catalogue entries untouched — the name is verbatim in it/en/ar) — W5.3 for the
FAQ's `_item.html` and `_collegamenti.html`.

**Tests.** `apps/pages/tests/test_interior_v522.py` (V5.20: `ROUTE_SHEETS` gains `pages/css/projet.css`; the import test asserts
`_projet.css` and `_materia.css` OUT of the shared interior sheet and `_materia.css` out of `main.css`; the route-sheet order test
gains `/fr/le-projet/`); `tests/frontend/test_typography_v2.py` (lane T's module, two slices under V5.20: the eight rows of this
lane's sheets measured 0 and deleted — a lower equality; `/ar/le-projet/` and `/ar/agami/` moved from `ARABIC_PAGES_BURNDOWN`
into `ARABIC_PAGES` — a stronger invariant, the four guards hold there now); NEW `tests/frontend/test_pages_v524_pub2.py` (the
grounds and the adjacency rule with the two recorded touches, the incastro's markup, the raccordo's markup and placement, the
material partial page-only, the roles by name, the sheets' disciplines, PX's guards, AR's wordings, the Privacy Policy run, the new
sheet's ceiling at its measure 2 219 B, Le projet's total ≤ 56 320); NEW `tests/frontend/test_pages_browser_v524_pub2.py` (the
raccordo lands within 2 px of the head line and on its axis at 1440 and 390 fr/ar, plays once and leaves `getAnimations()`,
stands drawn under reduced motion with no state written; the doors 64 px over the volumes at 1440/1024/390 fr/ar; AGAMI's
registers in the role's face, never ILE Mono; the FAQ explorer on the area's ground with its plate raised).

**Docs.** This file; `QA/v522/p2/NOTES.md` line 322 corrected (the panorama's credit inset: credits removed by v524, V5.24 §2).

## 3. Tool → decision → change (V5.26 §4; real names per `evidence/v524/TOOLS_AVAILABILITY.md` — no «design-critique»,
no «design-handoff»)

| Tool (real name, path) | Decision | Change |
|---|---|---|
| `impeccable` (`~/.claude/skills/impeccable/SKILL.md` — the shared design laws: «Cards are the lazy answer», «Identical card grids», the AI-slop test; `reference/critique.md`'s §24 questions once per page at the end) | the audit's two reading bands were a white card grid and a white sheet on off-white: the one thing that still read as a document. The ground, not the card, is the answer — stone under the plates makes them plates (a sheet on a desk), and the rimando strips stop being a second stone band in a row | FAQ explorer / glossary register / scheda / identity band / fraud band → stone; the two rimandi → paper; AGAMI's plate face raised so it reads as a plate on the band |
| `impeccable` `reference/typography.md` + `typeset.md` («Use fewer sizes with more contrast», «ALL-CAPS tracking», one family in weights) and TYPOGRAPHY_V2 §4.2 | every label of this lane's pages is ONE role (13/16 600 +0.08 em Host Grotesk; 14/20 Readex Pro without capitals) instead of four mono folios; titles on the band step, the term on the display step, the initial a multiple of the display step — no size the scale does not name | `t-label` in six templates; the sheets' type declarations gone to the role; `--t-band`, `--t-display`, `calc(var(--t-display) * 4.5)` |
| `taste-skill` (`design-taste-frontend`, `~/.claude/skills/taste-skill/SKILL.md` Rule 4 «Anti-Card Overuse»: cards only when elevation communicates hierarchy) | on stone the raised plates carry the hierarchy (the answer sheet, the definition plate, the report plate, the identity plate); the term cards and the index rows need no second container | no new container anywhere; the explorer's plate and the scheda's plate keep `--surface-raised`, the bands take the area's ground |
| `figma:figma-use-motion` / `figma-implement-motion` (`~/.claude/plugins/cache/claude-plugins-official/figma/2.2.157/skills/…` — the method: one timeline, phases in order, an ease-out curve, the duration the phase needs; the Figma MCP unauthenticated, no file read) | the Forum seam is ONE phase after the band's own: the pair's hairline draws at load, the reader scrolls, the band enters and the raccordo draws top → bottom (from the pair's foot to its node) over `--motion-draw` on `--ease-sine`, `--sez-d` one draw after the band's line — the primitive's beat, no duration or curve of this sheet's; under reduced motion the line stands drawn | `data-verb="draw-y"` on the span (the primitive's verb); `inset-block-start: calc(-1 * var(--risalita))` so the draw begins in the pair's foot; no new keyframe, no new token |
| `find-animation-opportunities` (`~/.claude/skills/find-animation-opportunities/SKILL.md` — the four-question gate: frequency, purpose, …) | the raccordo passes (once a visit; purpose: spatial continuity — where the route comes from); the grey line's extension up to the node is a still (no motion); the incastro is a still (no parallax on the doors over the photograph: decoration on a reading surface) | nothing animated beyond the primitive's draw |
| `ui-ux-pro-max:ui-ux-pro-max` (`~/.claude/plugins/marketplaces/ui-ux-pro-max-skill/.claude/skills/ui-ux-pro-max/SKILL.md` — rule 1 Accessibility CRITICAL: contrast, keyboard, labels; the UX guidelines for headings and text layout) | the doors' band keeps its `h2` for the outline (`aria-labelledby` intact, heading navigation intact) as a visually hidden title rather than dropping it or reordering it under the doors; the two addresses keep «one line at every width» through container-query steps on the scale (the invariant the P2 browser test holds at eight widths) rather than a fluid cqi clamp | `hidden=True` on the testa include; `@container` ladders in `_agami.css` and `_frodi.css` |
| `ui-ux-pro-max` a11y rule (decorative elements `aria-hidden`) | the raccordo and the drawn initial are drawings | `aria-hidden="true"` on the span (the primitive's contract); the initial already aria-hidden |
| Chromium CSS coverage (`CSS.startRuleUsageTracking` through Playwright — `tools/coverage.py`, the V5.20 method; `coverage_filter.py` maps the dist's unused rules to one partial and checks every class against every template) | `_lettura.css`: 88 of its rules unused on the 27 reachable reading routes (fr, ar; 1440, 390), 0 dead by construction — every class is still named by a legacy template (news, community, partners, legal, consents, enquiries), which CLOSING's rule keeps → the partial frees nothing now → the term page takes STONE (R4 e). `_forum.css`: 46 unused, 1 dead by construction (`.forum-cta__actions`) + the `.forum-action` print selector no template names | `_forum.css` −2 rules (the ceiling holds at 7 832 ≤ 8 192 regardless: the base's 7 303 was the pre-LIB 7 369 the letter counted from); the scheda band `data-ground="stone"` |
| The audit's own probe method re-aimed at 8789 (`tools/geom.py`, `probe.py`: the seams' geometry, the roles' faces, the addresses' lines, overflow, console) | the placements verified at 1440 · 1024 · 390 · 375 · 360 in fr and ar before the headed session | §7 |
| `21st.dev` MCP | not used: no new pattern enters (R9); the two libraries are in place | — |

**The FAQ against V5.26 §1's list (R9, one paragraph).** The FAQ already has the premium searchable explorer (the head's search
in its end seat, the empty search state through `components/empty_state.html`, the reset link), the category navigation (tabs
from 64 rem, exclusive disclosures below), the active question (the gliding marker, the address in step), the permalinks landing
on the open answer at the first paint, contextual icons (the T1 `ile-domande` seal in the plate's corner, the fraud question's
shield), the smooth restrained expansion (the 320 ms glide, instant from the keyboard), the related-topic navigation («il
rimando»), keyboard access and Arabic RTL (the French runs ending on the reading edge). What it lacked was the ground: the white
answer sheet beside the index on off-white still read as a document — it now stands on stone, and the rimando on paper closes the
page before the night footer. «Popular / helpful topics» are not added: there is no real data (V5.26 §1 «if real data exists»),
and a fabricated ranking would be the catalogue look the owner refused. The category's name takes the label role. Nothing else of
the explorer moves (KEEP).

## 4. Contract items — applied for other lanes · requested of other lanes · deviations recorded

**Applied here for other lanes.** (a) T's contract (TYPOGRAPHY_V2 §4.2, §6; `QA/v524/t/NOTES.md` §4): the burn-down rows of
`_faq-v2.css`, `_lessico-v2.css`, `_forum.css`, `_agami.css`, `_canali.css`, `_contatto.css`, `_frodi.css`, `_rete.css` emptied
(clamp 9, mono 4, ar-descendant 3, uppercase 5 → 0) and deleted from `TYPOGRAPHY_BURNDOWN`; `/ar/le-projet/` (T's row: the French
h2 at 24/32 — now 24/30 — and LIB's finding: the French statement at 20/32 on the phone — now 20/28 through its own leading) and
`/ar/agami/` (T's row: the registers in ILE Mono — now the role, Readex Pro) moved into `ARABIC_PAGES`. (b) LIB's contract
(`QA/v524/lib/NOTES.md` §4 c): the attributes `data-ground="stone"` / `data-incastro` and the class `sez-raccordo` with
`data-verb="draw-y" aria-hidden="true"` as the FIRST CHILD of the band it enters, `--sez-raccordo` set on the placement to the
distance from the seam to the head line (a band's padding, not a strip's), `--raccordo-x` on the route; the import after the shell.
LIB's request to PUB2 (`_projet.css:172`'s French h2 leading) applied: 24/30 (`--t-band-lh`). (c) PX's contract (IMAGERY_ATTRIBUTION
D3, D4): the `.foto__credit` rule of `_lessico-v2.css` deleted; `{% if … attribution_required %}` in `hero.html` and
`permanent_sections.html`. (d) AR's contract (02_class_b_wraps W1.2, W1.3, W5.3): the Forum eyebrow's msgid and its French branch,
the theme page's sentence, the «Privacy Policy» run in the FAQ's links. The new msgids are listed in §5 for the catalogue.

**Requested of other lanes (R14; not fixed here):**
- **AR / the steward's catalogue sync at this lane's merge (R13)** — the two msgids of §5 with the fragments' renderings
  (`evidence/v524/arabic/fragments/{ar,it,en}.po` §A); the two retired msgids («Espace permanent de dialogue et de coopération»,
  «Vivre en Italie — %(topic)s : fiches pratiques pour accompagner l’intégration après l’entrée régulière.») leave the catalogue
  with `scripts/i18n_audit.py --sync`. Until the sync, it/en/ar show the French msgid of the Forum eyebrow (gettext's fallback).
- **AR (V5.27, R7′)** — on `/ar/forum/` the Forum's titles and the pair's texts are still class-C French runs: the objectives'
  column and the pair's statement are LTR boxes, so the phone raccordo on the (RTL) reading edge stands across from the French
  statement's rule, which is on the left; once the Forum's institutional copy is rendered in provisional Arabic (C-UI) the columns
  turn RTL and the two lines share the edge. Nothing to change in this lane's placement.
- **CLOSING** — (1) `tests/frontend/test_frontispiece_v515_c.py` `SHEETS`: fold in `pages/css/projet.css` (2 219 B at this lane's
  measure, held in `test_pages_v524_pub2.py` meanwhile) and `PAGE_TOTALS` «interior (project)» `/fr/le-projet/` (55 412 /
  56 320 — the heaviest interior page now); the interior pages' measures (§6) for the ratchet. (2) `_lettura.css`'s 88 rules
  unused on the reading routes are the legacy pages' (news, community, partners, legal, consents, enquiries): CLOSING's coverage
  over EVERY route decides them, not this lane. (3) The dead `.forum-cta__actions` is gone; `.page-forum .empty-state*` stays
  (`forum/register.html` names the component). (4) The Forum's event-mode partials (programme, speakers, gallery, registration,
  the virtual-forum teaser) still compose `chapter` heads: out of this lane's tables (V5.25 §1).
- **LIB** — a `.sez` head rendered `hidden` keeps `.testa`'s `margin-block-end: var(--sez-gap)` (an empty 48–64 px band above the
  content); this lane zeroes it in `_projet.css` — the library could do it once (`.testa:has(> .visually-hidden) { margin: 0 }`).
- **Steward** — the family `v524-pub2` in `OWNERSHIP_V54.json` with these `owns`: `templates/faq/**`, `templates/glossary/**`,
  `templates/living/**`, `templates/forum/**`, `templates/pages/{project,agami,antifraud}.html`, `templates/pages/partials/_canali.html`,
  `templates/pages/partials/fronte/_rete_pannelli.html`, `apps/faq/services.py`, `apps/cms/static/cms/{_faq-v2,_lessico-v2}.css`,
  `apps/forum/static/forum/{forum,_forum}.css`, `apps/pages/static/pages/css/{interior,projet,_projet,_agami,_rete,_contatto,_frodi,_canali}.css`,
  `apps/pages/tests/test_interior_v522.py`, `tests/frontend/test_pages_v524_pub2.py` (new), `test_pages_browser_v524_pub2.py` (new),
  `tests/frontend/test_typography_v2.py` (slice: the eight rows and the two Arabic pages), `docs/design-v5/QA/v522/p2/NOTES.md`
  (one line), `docs/design-v5/QA/v524/pub2/**`, the rebuilt dist (`static/css/dist/{cms/faq,cms/lessico,forum/forum,pages/css/interior,
  pages/css/agami,pages/css/rete,pages/css/frodi,pages/css/projet}.css`).

**Deviations from §3.6's letter, each with its reason:**
1. **`interior.css` does NOT import `_materia.css`; Le projet gets a route sheet** (`pages/css/projet.css` = `_materia.css` +
   `_projet.css`). The letter's arithmetic held the sheet (8 827 + 770 ≤ 11 264) but not the page totals: `/fr/reseau/` stood at
   55 913 and `/fr/agami/` at 55 856 against the 56 320 letter — the partial on the shared sheet would have passed both (R4 a:
   «page-type totals are never raised»). Only Le projet uses the material (the incastro); the other institutional pages take their
   grounds from the shell. The route-sheet pattern is the product's own (P2's round 2: `rete.css`, `agami.css`, `frodi.css`;
   V5.26 §7 «page-only sheets»). Result: every interior page lighter (Réseau 55 913 → 54 954, AGAMI 55 856 → 54 858, Contact
   54 096 → 53 193, Fraudes 55 296 → 54 392), Le projet 54 096 → 55 412 ≤ 56 320. The doors' shared drawing (the arrow's shift,
   the words under the arch) is restated for `.contatto-porte` in `_contatto.css` (+86 B on the interior bundle): one drawing, two
   homes — the abstraction rule (V5.26 §8) would want it in the library's mosaico sheet; a request for after acceptance.
2. **The doors' band's head is the outline's** (`hidden=True`: a visually hidden `h2`, no rule). The audit's incastro wants the
   doors' arched tops over the photograph; the centred router head stood between the panorama and the doors, so the overlap would
   have lifted the TITLE into the photograph (ink over a frame, the doors untouched). Moving the head under the doors breaks the
   reading order; hiding it keeps the section's name for the outline and lets the doors — each naming its space and its way in —
   be the composition (V5.26 §5: «strongest with one powerful image … strong composition»). The panorama's bottom padding goes to
   0 so the frame's foot IS the seam (the band's own 96 px of paper under the image had stood between them).
3. **The raccordo's x and length are set per layout, not the primitive's defaults** (LIB's note foresees it): a band's head line is
   its own padding away (96 px at 1440, 64 on phones), not a strip's 48; and the line should start IN the pair's foot (the audit:
   «the stations' line starts 48 px up, in the pair's foot»), so the span is placed `--risalita` above the seam and runs
   `--risalita` + the padding. From 64 rem it stands on the objectives' station axis (the rings' centres: the second column's
   start + 11 px, computed from `--container`, `--grid-margin`, the grid's 5 : 7 and its 64 px gap, so it mirrors in Arabic by
   itself); the objectives' title steps 48 px in onto the stations' text axis (the clauses' own indent — the node would otherwise
   have sat over the «O» of OBJECTIFS) and the grey route line runs up from the first station to the node: one continuous line
   from the pair's foot to the arrival. Below 64 rem the objectives' column stands under the «what» column, far from the seam, so
   the line continues no route there: it crosses the seam on the reading edge (the container's content edge, where the pair's
   statement rule stands) and lands on the head line beside the band's first title.
4. **The term page's scheda is stone, not pietra** (R4 e's second branch): `_lettura.css` frees nothing a template does not still
   name (§3, the coverage row), and `lettura.css`'s import would have put every reading page over 54 272 (the FAQ 53 658 + 788,
   the glossary family 54 093 + 788).
5. **`.scheda__iniziale` is `calc(var(--t-display) * 4.5)`** (198 → 288 px; was `clamp(10rem, 22vw, 20rem)`, 160 → 317): the one
   decorative size of the lane reads the scale rather than a clamp of its own; smaller at 1440 by 29 px, larger on phones by
   38 px where it stands behind the opaque plate.
6. **The two addresses take the steps by container query** (`--t-body` → `--t-entry` at 18 rem → `--t-band` at 24 rem for AGAMI;
   `--t-body` → `--t-entry` at 18 rem for the fraud plate) in place of the cqi clamps: the P2 invariant «the address stands on one
   line at the eight widths» holds (the browser test; §7: one line at 1440 · 1024 · 390 · 375 · 360, fr and ar).
7. **The caps title of Le projet is `1.5rem` / `--t-band-lh`** (24/30): a value of the scale, one step under its 28 px neighbours
   as the finishing round composed it; `--t-band` itself is fluid (24 → 28) and would have made the two titles equal from 1024.
8. **The Forum's `_forum.css` dead-rule removal frees 2 rules, not «≥ 20 B» as a condition**: the letter's 13 B overrun was
   computed on the pre-LIB measure (7 369); LIB's merge had already brought the sheet to 7 303, so the import fits with 360 B to
   spare (7 832 ≤ 8 192). The two dead rules go anyway (coverage + no template names them).

**V5.29 run (7 Nov) — contract items.** (a) *SYS applied here*: the weight map's literal weights in this lane's sheets on the
tokens (`_forum.css` 4×, `_projet.css` 2× — value-identical); the FAQ's glyphs in `.sez-tile--sm` with `--tile-ink`'s states.
SYS's request «`_lessico-v2.css` literal 600 → `--w-title`» needed nothing: the sheet has no literal weight. (b) *A library
slice (for the steward's manifest)*: `templates/components/sezioni/indice.html` — two class attributes, explorer form only
(§12). (c) *Steward, at this lane's merge* — the orchestrator's V5.29 note of 21:25: PUB2's 26 rows of
`tests/i18n/arabic_allowlist.py` ARABIC_BURNDOWN are the merge steward's to burn (this run changed no Arabic text, R7′ renderings
untouched); `scripts/i18n_audit.py` KEEP_SOURCE's Forum-eyebrow row is answered by §5's msgid (the French branch is gone from
`hero.html`) — the row leaves with the catalogue sync; the carried browser test `test_the_forum_ring_turns_round_its_hub_and_mirrors_in_arabic`
was not run in this run (the Forum's ring is KEEP). (d) *SYS / CLOSING*: `test_icons.py::test_no_sheet_draws_a_glyph_with_a_thinner_hand_than_the_icon_rule`
is red on design-v5 itself (`.sez-tile--lg .icon { stroke-width: 1.25 }`, SYS's optical stroke vs the 1.5 px floor) — an owner
of the rule must either record it in `THINNER_RULES_WITH_AN_OWNER` under V5.20 citing V5.29 or restore 1.5. (e) *LIB*: a phone
permalink is jumped to before the web font swaps, so any change of the questions' wrap shifts the landing (§12); `indice.js`
could re-place the named heading once `document.fonts.ready` resolves — a post-acceptance candidate.

## 5. New msgids (the catalogue entries for the steward's sync at the merge — AR's renderings, `fragments/*.po` §A, Arabic reviewed
by the audit's native-reader pass)

| msgid (French source) | it | en | ar | where |
|---|---|---|---|---|
| `Dialogue institutionnel permanent` | Dialogo istituzionale permanente | Permanent institutional dialogue | حوار مؤسسي دائم | `templates/forum/partials/hero.html` (the permanent Forum's eyebrow; replaces «Espace permanent de dialogue et de coopération», lifted from the locked p2.forum.what.body — W1.2) |
| `Vivre en Italie — %(topic)s : repères pratiques pour s’installer et vivre au quotidien en Italie.` (python-format) | Vivere in Italia — %(topic)s: riferimenti pratici per stabilirsi e per la vita quotidiana in Italia. | Living in Italy — %(topic)s: practical pointers for settling in and everyday life in Italy. | العيش في إيطاليا — %(topic)s: معالم عملية للاستقرار والحياة اليومية في إيطاليا. | `templates/living/topic.html` (a theme's meta description; replaces the closing clause of the locked p3.living.body — W1.3; the themes answer 404 today) |

Retired: the two former msgids above. No other string; the «Privacy Policy» run uses the catalogue's own labels. JS: 0. Images: 0.
Migrations: 0.

## 6. Budgets (gzip -9 = Python `gzip.compress(…, 9)` on the built dist; the partials minified alone with the repository's esbuild;
before = `4e882904`; two `npm run build` identical, the dist committed)

| Measure | Before | After | Ceiling | Note |
|---|---|---|---|---|
| `pages/css/interior.css` (dist) | 8 873 | 7 970 | 11 264 | − `_projet.css`, + the contact doors' rules |
| `pages/css/projet.css` (dist, NEW) | — | 2 219 | **2 219** (the measure; `test_pages_v524_pub2.py`) | `_materia.css` 788 + `_projet.css` |
| `pages/css/agami.css` · `rete.css` · `frodi.css` (dist) | 1 760 · 1 817 · 1 200 | 1 665 · 1 761 · 1 199 | 2 048 · 2 048 · 1 536 | the roles |
| `forum/forum.css` (dist) | 7 303 | 7 832 | 8 192 | + `_materia.css`, the placement; − 2 dead rules |
| `cms/faq.css` · `cms/lessico.css` (dist) | 1 935 · 2 384 | 1 889 · 2 324 | 2 048 · 2 560 | the role; the credit rule gone, the term title's selector |
| `cms/lettura.css` · `pages/css/fronte.css` · `main.css` | 6 546 · 6 009 · 32 695 | unchanged | 9 216 · — · ≤ 32 716 (R4 c) | untouched by construction |
| the partials alone: `_agami` 1 760 → 1 665 · `_rete` 1 817 → 1 761 · `_frodi` 1 200 → 1 199 · `_contatto` 953 → 1 039 · `_canali` 884 → 803 · `_projet` 1 574 → 1 614 · `_faq-v2` 890 → 846 · `_lessico-v2` 2 384 → 2 324 · `_forum` 3 871 → 3 994 | | | | |
| **page totals** (the frontispiece test's method) | | | | |
| reading: `/fr/faq/` | 53 704 | 53 658 | 54 272 | |
| reading: `/fr/glossaire/` · term · Vivre | 54 153 | 54 093 | 54 272 | |
| forum: `/fr/forum/` | 46 517 | 47 046 | 54 272 | |
| interior: `/fr/contact/` · `/fr/reseau/` · `/fr/agami/` · `/fr/attention-aux-fraudes/` | 54 096 · 55 913 · 55 856 · 55 296 | 53 193 · 54 954 · 54 858 · 54 392 | 56 320 | every one lighter (deviation 1) |
| interior: `/fr/le-projet/` | 54 096 | 55 412 | 56 320 | the heaviest interior page now (908 B under the letter) |
| JS · images · migrations | — | 0 · 0 · 0 | | |

## 7. Probes (headless, no slot; `tools/geom.py` on 8789; `evidence/v524/pub2/geom_{fr,ar}_{1440,1024,390,375,360}.json`)

| Cell | the raccordo (first child · rise above the seam · node off the head line · off the axis) | the incastro (door over the photo · padding) | the term title · the initial | the addresses (one line: fraud · AGAMI) | overflow · console errors |
|---|---|---|---|---|---|
| fr 1440 | yes · 48 · 0 · 0 (the station axis) | 64 · 0 | 64/64 · 288 px | 20 px · 28 px, 1 line each | 0 · 0 |
| fr 1024 | yes · 41 (4vw) · 0 · 0 | 64 · 0 | 56.4 · 254 px | 20 · 28 | 0 · 0 |
| ar 1440 | yes · 48 · 0 · 0 (mirrored) | 64 · 0 | 64/70.4 · 288 px | 20 · 28 | 0 · 0 |
| fr 375 · ar 360 | yes · 32 · 0 · ±11 (the reading edge, by design — deviation 3) | 64 · 0 | 44 · 198 px | 17 · 20 | 0 · 0 |

T's four Arabic guards (`_ARABIC_GUARDS_JS`, 1440 and 390) on `/ar/le-projet/`, `/ar/agami/`, `/ar/faq/`, `/ar/glossaire/`, the term
page, `/ar/forum/`, `/ar/attention-aux-fraudes/`, `/ar/contact/`, `/ar/reseau/`, `/ar/vivre-en-italie/`: no finding; Readex Pro
loaded, no Vazirmatn. The label role in Arabic: Readex Pro 14/20 600, no capitals, no tracking (AGAMI's registers, the FAQ's
category, the hub, the kinds); an Italian register label (`lang="it"`) keeps Host Grotesk with the capitals.

## 8. Tests run (counts; one pytest at a time per database; `PYTHONIOENCODING=utf-8`, the sentinel table in-process; logs under
`C:/tmp/ile_v5_council/.work/v524-pub2/logs/`)

All on the lane's tree, targeted (V5.25 §2), `test_ile_v524_pub2` (static) and `test_ile_v524_pub2b` (browser, headless):
- Recovery run on `decdacb2` (`logs/recov_static.log`): the two lane modules + `test_materia_v524_lib.py` + `test_typography_v2.py`
  + the interior import test — 188 passed, 5 failed (the three defects of §R; fixed in `d31b9d08`).
- After the merge of design-v5 (`logs/merge_static.log`): the lane modules, `test_materia_v524_lib.py`, `test_interior_v522.py`,
  `test_typography_v2.py`, `apps/faq` — 273 passed, 2 failed (the channels' kinds read on the contact form's plate: the test
  scoped to `ul.canali`) → 2 passed.
- The gate's static set after the FAQ pass (`logs/gate_static.log`): `apps/faq`, `apps/glossary`, `apps/living`, `apps/forum`,
  `test_contact_channels_v519.py` (must not weaken), `test_interior_v522.py`, `tests/compliance/test_locked_content.py`,
  `test_icons.py`, `test_sezioni_v522_s.py`, `test_sezioni_v522_s2.py`, `test_content_pages_w3_f2.py`, `test_faq_v529_pub2.py`,
  `test_pages_v524_pub2.py`, `test_typography_v2.py`, `test_materia_v524_lib.py`, `test_frontispiece_v515_c.py` —
  **904 passed, 1 skipped (the WhatsApp number unset — option B), 1 failed: the base's** `test_icons.py::test_no_sheet_draws_a_glyph_with_a_thinner_hand_than_the_icon_rule`
  (`_sezioni.css` `.sez-tile--lg .icon { stroke-width: 1.25 }` — stream SYS's optical stroke; this lane's tree has `_sezioni.css`,
  `components.css` and `test_icons.py` byte-identical to design-v5: a design-v5 red for SYS / CLOSING, not this lane's).
- The browser set (`logs/gate_browser.log`, `-k` FAQ / explorer / pub2 / seams over `test_pages_browser_v524_pub2.py`,
  `test_content_pages_browser_w3_f2.py`, `test_pages_browser_v522_p2.py`, `test_sezioni_browser_v522_s2.py`): 28 passed, 4 failed →
  fixed (`logs/gate_browser2.log`: **6 passed** — the plate test reading SYS's material; the permalink landing M1 fr / ar after
  the inset fix; the CLS test).
- Final (`logs/final_static.log`): the frontispiece budgets, the FAQ module, the lane module, `apps/faq` — **166 passed**, 0 failed (after the
  2 207 measure).
- `ruff check .` clean; `ruff format` on the lane's Python; LF everywhere; two `npm run build` identical (`logs/dist13.sha` =
  `dist14.sha`), the dist committed.

**Test changes under V5.20 (each the same or a stronger invariant, reason cited):** `apps/faq/tests/test_views.py`
(`test_published_translation_is_rendered_but_draft_is_not`: the heading read by its whole text — it now holds the aria-hidden
glyph tile before its words; V5.29 §10–§13, FINAL_DELIVERY_V2 §3.6); `tests/frontend/test_frontispiece_v515_c.py` (`cms/faq.css`
2 048 → 2 207, V5.29 — §12 «ceilings re-recorded»); the lane's own new modules (`test_pages_v524_pub2.py`: Vivre's touch by its
rendered names, the channels drawn, PROJET 2 219 → 2 222; `test_pages_browser_v524_pub2.py`: the plate painted by a colour or
SYS's material); LIB's `test_materia_v524_lib.py` and T's `test_typography_v2.py` slices as recorded by the recovered build (§2).

## 9. The eye (the gate's pages, headed `chromium-1234` under a slot; `evidence/v524/pub2/shots/`)

The FAQ (V5.29's priority): headed `chromium-1234` under `CHROMIUM_LOCK_A` (label `v524-pub2-faq-eye`), stills and measures in
`evidence/v524/pub2/faq/` — §12. The other pages of §3.6's table were not re-composed in this run (KEEP / the recovered build's
probes, §7); their seams are held by the lane's browser module (green, §8). The reviewer's targeted gate (§3.6 «Gate») is the
next step and is not claimed here.

## 10. V5.26 §9 — «Would an expert digital product team have chosen this exact composition for this exact information?»

- **FAQ** — yes: a searchable explorer whose index and answer sheet stand on a desk, the category a label, the ways on in a paper
  strip before the footer; nothing added for its own sake (no «popular topics» without data).
- **Glossaire + term** — yes: a thumb index beside term plates on a ground; the term page one plate on stone with its drawn
  initial, the term at display size — the dictionary's page, not an article.
- **Le projet** — yes: the story beside its figure, the volumes full bleed, and the four doors rising from the photograph into the
  stone — the system's spaces as an architectural fact, no title needed over them.
- **Forum** — yes: the typographic pair, then the route that visibly begins in its foot and runs through the objectives to the
  arrival; the ring on night; the actions on stone.
- **AGAMI** — yes: the drawn colonnade plate on stone beside the promoter's text, the identification plate on night with its
  registers in the institutional label; every field once (Q9).
- **Fraudes** — yes: the report plate and the three routes as plates on a ground under the head's one warning; calm.
- **Réseau · Contact · Vivre** — KEEP (the audit's verdict; the labels through the role only).

## 11. Not done, by design or out of scope (R14: post-acceptance candidates, not fixed here)

- The FAQ stage keeps the tallest answer's height (lane P2's CLS rule): a short answer leaves the plate's lower third empty at
  1440 — KEEP (CLS 0 on permalinks outranks it); the font-swap landing (§4 «V5.29 run» e).

- The doors' drawing restated for the contact page (`_contatto.css`) and Le projet's (`_projet.css`): one home in the library's
  mosaico sheet would be the abstraction rule's answer (V5.26 §8) — LIB / CLOSING.
- The Forum's event-mode chapters (`chapter--area`: programme, speakers, registration, the virtual-forum teaser) between the
  night ring and the actions — legacy templates, out of the tables (V5.25 §1).
- PX's typographic nit on the two bylines' colon (a plain space before «:», `hero.html`) — recorded by PX as post-acceptance;
  the line was edited here for the guard only.
- `_lettura.css`'s legacy rules (news, community, partners, legal, consents, enquiries) — CLOSING's coverage over every route.
- The headless screenshots show Le projet's panorama frame empty (the lazy image not decoded at capture); the headed stills are
  the record.

## 12. V5.29 §10–§13 — the FAQ, the priority (built on SYS, merged first: design-v5 `31f5ceff` into the branch, `e55d97c1`)

**Critique (impeccable's critique method, once, in one head — the fast track; headless stills 1440 · 390 fr / ar and the empty
search, `.work/v524-pub2/probe0/`).** (1) The index was a column of plain text rows, one glyph in nine (the fraud shield): the
eye had nothing to scan by subject — the «generic accordion» the owner names. (2) Every row stood in the primary ink; a chosen
row differed by colour only. (3) On a phone the questions stood flush on the plate's edge (SYS's post-acceptance note «the FAQ
question flush at 390 (PUB2)») — fixed with a 12 px inset: 16 px moved a permalink 56 px past the letterhead (the
fallback face's wrap before the font swap, which the anchor jump measures; `test_pages_browser_v522_p2.py` M1). (4) A search without answer was a small notice on half a band, then a second paper band (results
paper → rimando paper): a dead end. (5) Weights were already on SYS's map (500 for titles and rows) — no change needed there.

| Tool (real name, path) | Decision | Change |
|---|---|---|
| `impeccable` critique (`~/.claude/skills/impeccable/reference/critique.md`: hierarchy, discoverability, states; `onboard.md` «No results: suggest a different query, keep the way on») | the subject of each question must be scannable before its words; a no-result search must keep every question one step away; the phone row needs its inset | one glyph per question in the index, on the phone's rows and on a search's answers; the empty search beside the whole register; the plate's inline padding (12 px) below 64 rem |
| 21st MCP (`mcp__21st__search`, one query «premium FAQ help center with category icons search and accordion» — R9: no component enters) | the premium help-centre pattern is a category rail + a per-question icon + a support way out; «helpful / not helpful» buttons and three-column accordions refused (noise, no data) | the explorer kept (it already is the master–detail rail); the icons added; the support way out is the existing «il rimando» (the contact tile) |
| the registry's own icon rules (`apps/core/icons.py` TWINS, the check rule) with `ui-ux-pro-max`'s icon guidance (one meaning per glyph, consistent set) | never two look-alikes in one list: no second shield beside the fraud mark (data protection → `lock`, not `shield-check`); `compass` is the only circle-family member in the list | `faq.views.GLYPHS`: visas `stamp` (the competent authority), recruitment `briefcase`, pre-assessment `compass` (eligibility / orientation), decreto flussi `book-text` (legal source), diplomas `university`, prior refusal `signpost` (the pathway), who `institution`, data `lock` (security), fraud `ile-scudo` (the brand's own ILE SVG) |
| SYS's icon primitive (`v5/_sezioni.css` `.sez-tile--sm`: 40 px vault, 20 px glyph at stroke 1.75, `--tile-ink`, the foot rule) | every glyph sits in the primitive, no FAQ-made container; the tile's own states are the «small icon transformation» (ink slate → laguna, the foot rule 40 % → 100 %, the glyph's 2 px shift on hover) | the row glyph `indice__glifo sez-tile sez-tile--sm` (explorer form only); the same tile in the panel heading (shown below 64 rem where the heading is the row; hidden beside the seal above — one concept per stage); `faq-item__glifo` in a search's summaries |
| `figma:figma-use-motion` (the method only — no Figma file: one timeline, phases in order, ease-out, the duration the phase needs) | opening is three phases on one beat: the tile inks and its rule runs (the primitive's `--motion-emphasized`), the divider deepens to the structure line, the answer comes in (opacity + 6 px, `--motion-standard`, `--ease-enter`); desktop keeps lane S's GLIDE (marker + clip-path cross) and adds only the chosen row's quiet face; nothing from the keyboard (`data-input="key"`), nothing under reduced motion (`prefers-reduced-motion`, `.rm`), nothing at load (the answer animates only while its button holds the focus — a permalink opened at arrival never moves) | `faq-svela`; `.indice__apri[aria-expanded="true"] .sez-tile`; the `[data-on]` divider; `.indice__voce[aria-selected="true"]` face + divider |
| `impeccable` `reference/typography.md` («hierarchy through scale + weight contrast, not bold») | the questions at 500 everywhere (SYS's `--w-control` / `--w-title`); hierarchy by ink: rest `--text-2`, hover `--text-1`, chosen `--accent-text` | `.faq-esploratore .indice__voce` colour by state |

**Decisions recorded.** (a) *Thematic index / category filter*: the register holds ONE category (nine prescribed questions);
the category navigation (`faq__toc`) already appears by itself the day an editor adds a second category. A filter over nine
questions in one category would be the overload V5.29 §13 forbids («calm, not overloaded»), and a theme taxonomy invented here
would be fabricated structure on locked copy — so the thematic index IS the index: each row says its subject by its glyph.
(b) *Search*: the head's search (V5.22 Q0 KEEP) kept; the result band moves to stone (stone → paper before the footer, as the
explorer); the empty state stands beside «Questions fréquentes» — the nine questions as links to their permalinks with their
tiles (0 new strings: the heading reuses the page's msgid). (c) *Deep links*: every question keeps its permalink (the address
follows the chosen question; «Lien direct vers cette question» under each answer; the empty search's links land on `#key`).
(d) *Related topics*: per answer its chips (context links) and the page's «il rimando» — unchanged. (e) *Keyboard*: lane S's
tablist (arrows, Home, End) kept; a visible inset focus ring on the rows (`--focus-ring`, `outline-offset: -2px`, never clipped).
(f) The locked questions and answers byte-identical (`tests/compliance/test_locked_content.py` green); the AR lane's R7′
renderings untouched (no template text changed, no `lang` box changed).

**Files.** `apps/faq/views.py` (GLYPHS, `glyph()`, the explorer's items, `results`, `suggestions`); `templates/faq/index.html`
(the result band on stone, the empty search's register); `templates/faq/_item.html` (the optional `glyph`);
`apps/cms/static/cms/_faq-v2.css` (the states, the phone inset, the choreography, the empty search, the Arabic row with its tile
on the reading edge); `templates/components/sezioni/indice.html` — **a library file (lane S / LIB's family): a slice of two class
attributes, explorer form only (the FAQ is the only `form="explorer"` user — grep), recorded for the steward's ownership
manifest**; NEW `tests/frontend/test_faq_v529_pub2.py`; `apps/faq/tests/test_views.py` (V5.20, §8).

**Ceilings re-recorded (V5.20 citing V5.29 — an explicit owner decision requiring the redesign; nothing in the sheets was dead
to pay with: every rule of `_faq-v2.css` is named by `faq/index.html` or `indice.html`; `_projet.css`'s change is SYS's
value-identical token contract):**

| Ceiling | Before | After | Where |
|---|---|---|---|
| `cms/faq.css` (dist, gzip -9) | 2 048 (measure 1 887) | **2 207** (the measure) | `tests/frontend/test_frontispiece_v515_c.py` SHEETS |
| `pages/css/projet.css` (dist, new in this lane) | 2 219 | **2 222** (the measure) | `tests/frontend/test_pages_v524_pub2.py` PROJET_CSS_CEILING |

Not raised: `main.css` 32 714 ≤ 32 716 (untouched by this lane); the reading page `/fr/faq/` ≈ 54 038 ≤ 54 272 (the linked
sheets summed on 8789; the frontispiece test green); `/fr/le-projet/` ≈ 55 489 ≤ 56 320; `/fr/forum/` ≈ 47 098 ≤ 54 272;
`forum.css` ≤ 8 192. 0 JS, 0 images, 0 strings, 0 migrations.

**Checked in real Chrome** (headed `chromium-1234` under `CHROMIUM_LOCK_A`, label `v524-pub2-faq-eye`, 7 Nov ≈ 00:02–00:06,
released; `tools/faq_eye.py`, stills + `faq_eye.json` in `evidence/v524/pub2/faq/`): FAQ at 1440 · 1024 · 390 in fr and ar
(+ 390 under reduced motion, fr and ar) — 9 glyphs, 0 repeated, in every cell; the chosen row's tile laguna with its rule at 1,
the address in step (`#faq_diplomas`); ArrowDown moves the focus with a solid ring; on a phone the opened question's tile
laguna, rule 1, the answer shown, `faq-svela` once on open and nothing under reduced motion; the empty search 9 links; 0 console
errors; 0 overflow.

**V5.26 §9 — the FAQ.** Would an expert product team have chosen this composition for this information? Yes: nine prescribed
answers in one category are best read as an index beside one answer sheet; the subject glyphs make the index scannable without
adding a layer; the open state is felt (ink, rule, divider, reveal) but quiet; a failed search turns into the register itself.
Nothing was added that the content cannot carry (no ranking, no votes, no invented themes).
