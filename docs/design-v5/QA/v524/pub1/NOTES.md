# V5.24 lane PUB1 — journeys and spaces: the material pass + V5.29's «l'intesa» (label v524-pub1-build)

Branch `v524-pub1` (worktree `C:/tmp/ile_wt/v524-pub1`), cut from `design-v5` at `4e882904` (the v524-lib merge: lanes S, M,
P1, S2, H, P2, PX, T and LIB merged; tags `v522/*`, `v524/px`, `v524/lib`). Lane server 8788 on the lane database `ile_v5_l4`
(dev settings, `ILE_DESIGN_PREVIEW=1`, `ILE_REFERENCE_DATE=2026-10-03`; the clone in step with `ile_v5`: 75 migrations, 19
users, no refresh needed); pytest on `test_ile_v524_pub1`, one at a time (the headless browser twins on a second lane database
`test_ile_v524_pub1b`, so neither waited — R12); headed `chromium-1234` under a Chromium lock slot (label `v524-pub1-eye`,
one session); headless probes without a slot. Binding: V5.24 §7–§17 (the material, the seams, the verbs) and §11–§14 (the
type roles), V5.25 (targeted checks, no score loop), V5.26 §4–§9 (tool → decision → implementation; the abstraction rule;
«would an expert team have chosen this exact composition for this exact information?»), V5.20 (the strict test rule), V5.22
§9.7–§9.8, `FINAL_DELIVERY_V2.md` §0–§2 (R3 the «raccordo» name, R4 b the recorded ceilings, R5 the two deviations, R9 KEEP,
R10 the real tools, R12, R14 the scope guard) and §3.5, `evidence/v524/BACKGROUND_MATERIAL_V2.md` §3.2–§3.4, §4.2, §5.3,
`TYPOGRAPHY_V2.md` §4.2, §6 with lane T's contract (`QA/v524/t/NOTES.md` §4: the burn-down rows of PUB1's sheets), lane
LIB's contract (`QA/v524/lib/NOTES.md` §4 c: the raccordo the FIRST CHILD of the band it enters; `--raccordo-x`,
`--sez-raccordo`; the requests to PUB1), lane PX's contract (`attribution_required`). Evidence of this lane:
`C:/tmp/ile_v5_council/evidence/v524/pub1/` (`probe_p1.json` the headless probe of the eight pages at 1440 · 1024 · 390, fr
and ar; `shots/` the headed stills; `headed_measures.json`, `headed_console.json`); the lane's tools and logs under
`C:/tmp/ile_v5_council/.work/v524-pub1/` (`tools/edit1-3.py` the three edit passes, `measure.py`, `probe.py`,
`headed_shots.py`, `run.sh`; `logs/`).

Scope held (§3.5): the eight page types' templates and sheets, the tests the section names, nothing else — no library partial,
no `main.css`, no template of another lane, **0 JS, 0 strings, 0 images, no migration**. The compositions the reviews passed
stay as they are (R9): every change below is a ground, a seam, a verb, a role or an order.

## §R. Recovery inventory (6 Nov 2026, label v524-pub1-build, resumed after the credit interruption — V5.28 RECOVER, never recreate)

Recovered from the checkpoint `da86c645` («WIP recovery: journeys and spaces V5.27 after credit interruption») on top of
`4e882904`; the worktree and the branch kept as they were (no reset, no rebase, no regeneration). design-v5 has since moved to
`e6e6c34b` (v524-cifix, DL54-190): merged into the branch after this inventory.

**Files already changed (38, `git diff --stat 4e882904 da86c645`).** Templates: `pathways/{index,detail,training,diplomas,_tracciato}.html`,
`ecosystem/{pilot,companies,institutions,universities}.html`, `ecosystem/partials/pilot_flow.html`. Sheets: `pathways/{_index,
_persone-v2,_sheet,_diplomas,_training}.css` and the four route sheets' imports; `ecosystem/{_companies,_institutions,_spazi-v2,
_universities}.css` and `institutions.css`, `pilot.css` imports. The rebuilt dist (8 sheets). Tests: `test_pages_v522_p1.py`,
`test_pages_browser_v522_p1.py`, `test_typography_v2.py` (PUB1's rows), NEW `test_pages_browser_v524_pub1.py`. These notes.

**Implementation completed.** All of §3.5's decision table (§1–§2 below): the three raccordi, the come plates' verb, the three
carta viva grids, pietra under every protection, the velatura, the pilot's wash, the démarche's stone, the filiera's wash and
sfumatura, Formation's order, the type roles (T's burn-down rows), PX's credit / attribution contract, the ceilings recorded
under R4 b. `npm run build` on the recovered tree: the committed dist IS the build (no diff).

**Implementation incomplete.** (1) §8 tests, §9 the eye, §10 the V5.26 §9 answers, §11–§12 were `TBD`; (2) the V5.29 addition
(the Institutions Italy + Morocco background) not started; (3) the merge of design-v5 (v524-cifix) not done.

**Tests already written.** The four modules above; `apps/pathways/tests`, `apps/ecosystem/tests` unchanged.

**Tests already passing (run now, targeted, `test_ile_v524_pub1`).** `test_pages_v522_p1.py`, `test_typography_v2.py`,
`test_materia_v524_lib.py`, `apps/pathways/tests`, `apps/ecosystem/tests`: **512 passed, 1 deselected** (19 min; the earlier
`test_materia…page_only_partial` red of the dead agent's log is green on this tree).

**Remaining defects.** (a) `apps/pathways/tests/test_views.py::TestPhase3Index::test_eight_pathways_in_prescribed_order_with_exact_texts`
red: its regex reads `<span class="tracciato__num"` and the numeral now also carries `t-numeral` (LIB's request) — a test
reading fix, same invariant (V5.20); (b) the dead agent's last browser log: `test_each_raccordo…[1440-ar]` (the paint probe read
243 vs 193 at Parcours) and `test_under_reduced_motion…`, plus two «Target crashed» (Chromium, environment) — re-run on the
merged tree and fixed if real.

## 0. The decision in one screen

The eight pages take the material the library shipped and nothing else: «pietra» under every protection, «carta viva» under
the three router grids, the velatura at the chamber's foot, the brand wash under the pilot's route and the filiera, stone
under the sheets' steps and the companies' démarche, the two orders and rhythms R5 records — fourteen seams of one kind on
the merged pages become none; three seams are crossed by «il raccordo» (the board's trunk rising into the head's foot, the
filo's line into the night arc, the dossier's route into the protection), each the first child of the band it enters and
placed on its route's own x by one shared measure (`--bordo-lettura`, the reading edge from the band's edge); the «Comment ça
marche» plates stop settling and say «a threshold» (the tile's foot rule draws, its glyph inks, its floor lights); every
label, kicker and numeral of the space reads the twelve steps' roles by name (T's burn-down emptied but for one recorded
residue); the credit chip leaves the chamber; the sheets' figure draws a byline only when a licence asks for one. Budgets:
every route sheet under 11 264 (R4 b, recorded, not raised), every page total under 56 320, `main.css` untouched.

## 1. What the owner sees, where

| Page | What changes (the composition kept) |
|---|---|
| Parcours | the board's trunk rises 48 px (32 on a phone) out of the board into the head's foot — the route leaves the head; the four «Comment ça marche» plates no longer pop as squares: each tile's foot rule draws, its glyph inks, its floor lights, 60 ms apart; «Dans l'Espace Personnes» stands on lit paper (one radial light at the band's origin corner, mirrored in Arabic); «la protezione» on the drawing table — the drafting grid on the far side, the shield bookend, the sill |
| the eight sheets | «Étapes» on stone as a band (the head's paper no longer touches the body's); the filo's line crosses into the night: a line in the night's accent from the seam down to «chi decide»'s head rule, where its gold node lands; «la protezione» on pietra; the rail's title in the label role |
| Projet pilote | the route on the page's one wash (brand), the status plate standing on it, as a band; the two doors on paper on their sill; night → brand → paper → stone, no two grounds of one kind touching |
| Entreprises | «la démarche» on stone — the quotation (now at the title's weight), the measured curve and its three panels read on it; a strict paper / stone alternation down the page; the moments' numerals in the sans |
| Institutions | the chamber's foot dissolves into the approdo's stone over 12 rem (8 on a phone), the way out and the help line standing above the fade; the credit chip gone |
| Universités | the filiera on the page's one wash, its top fading in from the head's paper; the plates' kickers in the label role |
| Formation | Diplômes' order: the traversata, «la protezione» on pietra, the grid on lit paper (its tiles ink and light), the boussole; the two times' kickers in the label role |
| Diplômes | the dossier's route crosses into «la protezione»: a line from the seam down to the plate's rule, its node where the route meets the shield's sill; the grid on lit paper; the stations' numerals in the sans |
| everywhere | no ILE Mono seat left in the space's sheets; the French runs on the Arabic pages at their Latin leading through the tokens alone |

## 2. What changed (files owned per §3.5)

**Templates.** `templates/pathways/index.html` — the board's first child `<span class="sez-raccordo sez-raccordo--risale"
data-verb="draw-y" aria-hidden="true">`; the come tiles `data-verb="ink"`; the grid `data-luce="origine"`; the protection
`data-ground="pietra"`. `templates/pathways/_tracciato.html` — `t-label` on the lane's name, `t-numeral` on the station's
numeral (LIB's request). `templates/pathways/detail.html` — `#etapes` `data-ground="stone" data-rhythm="band"`;
`#documentation` → `paper` (see §4, deviation 3); `#autorites`'s first child the `--notte` raccordo; `#avertissements` → pietra;
the rail's title `t-label`; the figure's byline behind `credit and attribution_required` (PX's contract).
`templates/pathways/training.html` — the protection band moved before the grid (R5), on pietra; the grid `data-luce`; the
kickers `t-label`. `templates/pathways/diplomas.html` — the protection on pietra with the raccordo as its first child; the grid
`data-luce`. `templates/ecosystem/pilot.html` — `#sequence` `brand` + `band`; `#participer` `paper`.
`templates/ecosystem/companies.html` — `#demarche` `stone`. `templates/ecosystem/institutions.html` — `data-sfuma="stone"`.
`templates/ecosystem/universities.html` — `#filiere` `brand`; the kickers `t-label`. Every header comment records the V5.24
decision; `partials/pilot_flow.html`'s stale «ILE Mono» word corrected.

**Route sheets.** `pathways/{index,sheet,training,diplomas}.css`, `ecosystem/{pilot,institutions}.css` import
`../css/v5/_materia.css` after `_sec-strato.css`; `companies.css` and `universities.css` do not (§4, deviation 1).

**Page partials.**
- `pathways/_index.css`: the `.come__num` on the numeral role (`--t-numeral`, `--t-numeral-lg` from 64 rem, 600, tabular; the
  route-across calc reads the same step); the PA-2 verb — `.come .sez-tile::before` the lit floor (an inner shadow in
  `--surface-raised`), `opacity: 0` in `wait`, `sez-layer` over `--motion-standard` after `--motion-slow` + the plate's stagger
  (`--co-i`) in `in`; the tile's foot rule `scale: 0 1` in `wait` and `sez-draw` to its resting 40 % in `in`; the raccordo's
  placement `.percorsi-famiglie > .sez-raccordo { --raccordo-x: calc(var(--bordo-lettura) + 23px) }`; the descendant-form rule
  `[dir="rtl"] .percorsi-tracciato :is(.tracciato__titolo, .tracciato__riga)[lang="fr"] { line-height }` deleted (the tokens'
  Latin boundary carries it — measured 28 px, §7).
- `pathways/_persone-v2.css`: `.sez-raccordo { --bordo-lettura: calc(max(0px, (100% - var(--container)) / 2) + var(--grid-margin)) }`
  — the container's content start measured from the band's edge, the one measure the three raccordi read (a percentage in a
  custom property resolves where it is read: against the band); the `:lang(ar) :is(.testa__label, .tracciato__nome,
  .traversata__kicker)` rule deleted (the label role's own Arabic rule, `base.css`).
- `pathways/_sheet.css`: `.scheda-rail__titolo` keeps its margin and ink, the type is the role's; its `:lang(ar)` twin deleted;
  the raccordo's placement `.scheda-decide > .sez-raccordo { --sez-raccordo: clamp(var(--s-16), 8vw, var(--s-24)); --raccordo-x:
  calc(var(--bordo-lettura) + 19px) }`, from 64 rem the body's second column added (`(min(100%, var(--container)) - 2 *
  var(--grid-margin) - var(--s-6)) * 3 / 12 + var(--s-6)`).
- `pathways/_diplomas.css`: `.dossier__num` on the numeral role (28 / 36 from 64 rem, 600, tabular, its box its size); the
  `[dir="rtl"] .dossier__definizione[lang="fr"]` rule deleted; the raccordo's placement `.persone-protezione > .sez-raccordo {
  --sez-raccordo: calc(clamp(var(--s-16), 8vw, var(--s-24)) + 68px); --raccordo-x: calc(var(--bordo-lettura) + 23px) }`, 27 px
  from 64 rem (the 56 px tile).
- `pathways/_training.css`: `.traversata__kicker` the role's; the `[dir="rtl"] … .traversata__corpo[lang="fr"]` rule deleted.
- `ecosystem/_universities.css`: `.filiera__kicker` the role's; the sfumatura — `.universita-filiera::before { inset: 0;
  z-index: -1; box-shadow: inset 0 4rem 3rem -2rem var(--surface-page) }` (2.5 / 2 / −1.25 rem on phones), hidden under forced
  colours and in print.
- `ecosystem/_institutions.css`: the `.istituzioni-aula__fondo .foto__credit` rule deleted (PX's contract); `.istituzioni-aula {
  padding-block-end: 12rem }` (8 rem on phones) — the velatura's own room (§3).
- `ecosystem/_companies.css`: the quotation on `--t-title-2` / `--t-title-2-lh` / `--w-title` / `--track-title-2` (the clamp
  gone); the moments' numeral on `--t-numeral-lg`, 600, tabular (the mono gone).
- `ecosystem/_spazi-v2.css`: the `:lang(ar) :is(.testa__label, .filiera__kicker)` rule deleted.

**Tests** (V5.20: each change cited where it stands; the same invariant or stronger).
- `tests/frontend/test_pages_v522_p1.py`: the eight route sheets' ceilings RECORDED at 11 264 (R4 b; the measures written
  beside them for CLOSING's ratchet); the ground set gains `pietra`; the pilot's route `brand` + `band` and the doors `paper`
  (R5); every protection on `pietra`; NEW — the grounds' sequence and the adjacency rule on every page type (stone ≡ pietra;
  the one accepted touch: the head's paper against a paper moment or strip), the material and the seams where the Director
  placed them (the three raccordi as first children with their modifiers, the three `data-luce`, the velatura, the come
  tiles' `ink`, Formation's order, the pilot's wash, the démarche's stone, the filiera's wash, the imports), the roles
  (`t-label` ×4 lane names, ×2 kickers, ×3 kickers, the rail title; `t-numeral` ×8; no mono seat and no font-size clamp in
  the ten sheets), the figure's byline guard.
- `tests/frontend/test_typography_v2.py` (lane T's module, a slice): PUB1's eight burn-down rows lowered to the measure —
  six deleted (`_sheet`, `_diplomas`, `_training`, `_companies`, `_universities`, `_spazi-v2`), `_index.css` and `_persone-v2.css`
  at `{"uppercase": 1}` with the reason (§4, residue).
- `tests/frontend/test_pages_browser_v522_p1.py`: the institutions' annotation asserted AT the ui step (15; 16 under 48 rem
  by T's phone step-up) and under the lead — exact, where a 15.5 cap predating T read a phone's 16 px as a second lead (the two
  reds the base carried since T's merge, LIB NOTES §7).
- NEW `tests/frontend/test_pages_browser_v524_pub1.py` (headless, no slot): each raccordo the first child of its band, waits,
  draws once after the band's line (`--sez-d` 0.9 s), leaves `getAnimations()`, lands within 2 px of its line (the seam up
  into the head's foot; the night band's head rule; the plate's 3 px rule), on its route's x (±1.5 px, mirrored in Arabic),
  and is PAINTED (the line's column against the ground 12 px beside it; the night line lighter) — fr and ar, 1440 and 390; the
  velatura a still (12 / 8 rem) with the words above it; the come tiles ink, light and draw their rule, never settle; the three
  grids carta viva; Formation's order; the pilot's wash and plate; the sfumatura still; reduced motion and the keyboard; the
  eight pages' width at 1024 and 360 with 0 console errors.

## 3. Tool → decision → change (V5.26 §4; real names per `evidence/v524/TOOLS_AVAILABILITY.md` — no «design-critique», no «design-handoff»)

| Real tool (path) | Decision | Change |
|---|---|---|
| `figma:figma-use-motion` + `figma:figma-implement-motion` — `~/.claude/plugins/cache/claude-plugins-official/figma/2.2.157/skills/figma-use-motion/SKILL.md`, `…/figma-implement-motion/SKILL.md` (the Figma MCP is not authenticated: the method applied to the product's tokens — pick the phases; one timing language; factor repeated motion into one component with the varying value as a parameter; honour reduced motion with the resting state; **validate one animation end to end**) | the three raccordi share LIB's one timing (the band's own line 0 → 900 ms, the raccordo 900 → 1 800 ms on `draw-y`, `--ease-sine`, the node its tip) and vary by two parameters only — the length (`--sez-raccordo`: a strip's 48 / 32 px is the primitive's; a BAND's padding, or the padding + the seal's 68 px stand, where the node must land on the band's head line, LIB §4 c) and the x (`--raccordo-x`), which the three placements derive from ONE shared measure (`--bordo-lettura`) instead of three literal offsets; the end-to-end validation taken literally: the headless probe read every raccordo's box against its landing (0 px off at 1440 · 1024 · 390, fr and ar, §7) and the browser twin reads the paint | `_persone-v2.css` (`--bordo-lettura`), `_index.css`, `_sheet.css`, `_diplomas.css` (the placements), `test_pages_browser_v524_pub1.py` |
| `find-animation-opportunities` — `~/.claude/skills/find-animation-opportunities/SKILL.md` (the four-question gate: frequency, purpose, speed, function) | PASS: the come plates' floor light (state — a threshold reached; once; 200 ms) and their tile's foot rule drawing to 40 % (spatial — the plate's threshold; once); the three raccordi (spatial continuity — where the route goes; once per seam per visit; ≤ 900 ms; a marketing surface). REJECTED: any motion on the velatura or the sfumatura (a gradient must not animate — §6.1: they are grounds), a drift on the pietra grid, a second beat for the raccordo's node, any hover motion on the come plates beyond the library's threshold run (tens of times a visit) | nothing animates in the grounds; the come plates' two verbs only |
| `impeccable` — `~/.claude/skills/impeccable/SKILL.md` (the shared design laws: «cards are the lazy answer», no identical card grids, the AI-slop test; `reference/typography.md`: hierarchy by scale and weight, never a flat scale) | the come plates were «four white squares popping on a wash» — the fix is the verb, not a new plate: the rule, the ink and the floor say «a threshold» as the grids now do; the Entreprises quotation at 500 under 36 px was the lightest text of its band — a statement intitles (600) on the title step; the institutions' credit chip was the last pasted square on the chamber | `_index.css` §PA-2, `_companies.css`, `_institutions.css` |
| `taste-skill` — `~/.claude/skills/taste-skill/SKILL.md` (Rule 4 anti-card overuse: elevation only where it carries hierarchy; §7 no glows) | the filiera's top fade and the come tiles' floor light are drawn as inner shadows in the page's own tokens — no gradient, no glow, no new layer stacked on the plates; the pilot's doors keep their one raised face on paper (no second box) | `_universities.css`, `_index.css`, `_pilot.css` untouched |
| `ui-ux-pro-max` — `~/.claude/plugins/marketplaces/ui-ux-pro-max-skill/.claude/skills/ui-ux-pro-max/SKILL.md` (a11y → touch → performance before style; contrast on layered grounds) | the velatura would have laid stone under the chamber's night ink (the way out and the help line stand in the band's last 160 px: 17–50 % stone under `--text-on-night-2` fails contrast) — the band's foot takes the fade's exact room (12 / 8 rem) so the words stand above it, and the twin asserts it; the kickers become the label role (13/16 600 caps; 14/20 no caps in Arabic — the floor), never the mono (an Arabic kicker in the mono fell to a system face) | `_institutions.css`, the four kicker rules, `test_pages_browser_v524_pub1.py` |
| the material audit's probe (`.work/v524-audit/v524-material/probe.py`), re-aimed at 8788 as `tools/probe.py` | the grounds' sequence, the touches, the roles' computed type, the French runs' leading, the raccordi's boxes, overflow and console on the eight pages × 3 widths × 2 languages read before the eye — the three descendant-form leading rules proved redundant (28 px without them) and were deleted rather than rewritten | `probe_p1.json`; `_index.css`, `_diplomas.css`, `_training.css` |

## 4. Contract items — applied for other lanes · deviations recorded · requests to other lanes

**Applied here for other lanes.** (a) T's contract (TYPOGRAPHY_V2 §4.2, §6; `QA/v524/t/NOTES.md` §4): every type rule of
PUB1's ten sheets reads the twelve steps and the roles — the eight burn-down rows lowered (§2); 0 `var(--f-mono)`, 0 clamp in a
font-size, 0 descendant-form Arabic rule. (b) LIB's requests (`QA/v524/lib/NOTES.md` §4): `t-label` on `.tracciato__nome`,
`t-numeral` on `.tracciato__num` (`_tracciato.html`); the come plates' `ink` and their light in `_index.css` (the shell carries
none, B1). (c) PX's contract (IMAGERY_ATTRIBUTION D5, D6): the `.foto__credit` rule of `_institutions.css:47-56` deleted; the
sheets' figcaption byline behind `credit and attribution_required` (`detail.html`). (d) The Director's R5: the two rhythm
deviations recorded in the templates' comments and asserted by the tests (the pilot's route and the sheets' steps are bands —
content-bound).

**Deviations from §3.5's letter, each with its reason:**
1. **`companies.css` and `universities.css` do not import `_materia.css`** (the table lists the import for all eight). Entreprises'
   change is a ground (`stone`, 0 B) and its page draws no recipe; Universités' is a ground (`brand`) and the sfumatura, which
   the partial does not carry (deviation 2). An import no attribute reads would add ≈ 790 B to each for nothing — «a page
   carries only what it draws» (the sheets' own contract, SECTION_SYSTEM_V2 §7.1). Asserted in `test_pages_v522_p1.py`
   (`MATERIA_IMPORTS`); the day either page takes a recipe, the import comes with it.
2. **The sfumatura is drawn in `_universities.css`, not by a primitive.** BACKGROUND_MATERIAL_V2 §3.2 names «sfumatura» (the
   velatura at 6 rem) at the filiera's TOP; `_materia.css`'s velatura dissolves a FOOT (`inset-block-end: 0`), and the band above
   is the frontispiece — not a `.sez`, so `data-sfuma` has nowhere to stand. The page sheet draws the start-side fade as a
   `::before` layer, in the page's token, with the page-sheet idiom (an inner shadow: `tests/frontend/test_design_docs.py`
   refuses a gradient in an app sheet; `_institutions.css`'s veil is written the same way). A start-side twin is requested of
   LIB below; when it lands the page rule goes and the attribute takes its place.
3. **The sheets' `#documentation` band is paper** (the audit's table does not name it; it was stone). With `#etapes` on stone, a
   sheet that has verified documents would set stone on stone — a regression of this lane's own change (R14), and 0 B. No seeded
   sheet draws the band today; the adjacency test reads whatever renders.
4. **The come plates' light is an inner shadow, not the mosaico's gradient.** LIB's request says «the three light rules copied
   into `_index.css`»; the guard of `test_design_docs.py` refuses `gradient(` in an app sheet (as it should: tokens only). The
   floor lights the same way to the eye (`inset 0 -1.75rem 0.75rem -0.25rem var(--surface-raised)`, the tile isolating, the
   layer under the glyph); the `wait` / `in` rules are the mosaico's, `--co-i` the plate's own stagger (`_vocabulary_before`
   does not let a page partial read the library's `--sez-i`, P1 NOTES §7 item 4).
5. **The Diplômes raccordo lands on the plate's 3 px rule, 164 px (132 on phones) into the band**, not the letter's 48 px: the
   pietra band has no head rule but the plate's soglia (the band's padding + the seal's 68 px stand); LIB §4 c says a lane
   landing on a deeper line sets `--sez-raccordo` to the distance. Likewise the sheet's raccordo is the night band's padding
   (96 at 1440, 64 on phones) so its node lands on the head rule, not mid-padding.
6. **The Entreprises quotation moves from 500 to `--w-title` (600)** with its clamp → `--t-title-2`: TYPOGRAPHY_V2 §4.3 («600
   intitles — statements») and V5.24 §12 (no thin headings); the clamp's own range was 24 → 36, the step's 28 → 36 (a phone
   gains 4 px on a one-sentence statement). The letter names only «clamps → tokens»; the weight is recorded here.
7. **Two burn-down rows stay at `{"uppercase": 1}`** (`_index.css`, `_persone-v2.css`): `.come__testo::first-letter` and
   `.mosaico__riga::first-letter` capitalise the first letter of a locked fragment that the sentence writes in lower case (the
   plates cut «Comment ça marche» on its own arrows; the grid's lead line). A sentence-initial capital is a typographic
   convention of the composition the review passed, not an eyebrow or a kicker (the rule's target, TYPOGRAPHY_V2 §6); the
   text's characters are unaltered. Recorded as a residue like `_fronte.css`'s two clamps (LIB NOTES §4), the table equal to
   the measure.
8. **The institutions' band grows 12 rem (8 on phones) at its foot** for the velatura's room (§3): the chamber's photograph
   fills it — the dissolve into the stone is what the audit drew, and the words never stand on it.
9. **`tests/frontend/test_typography_v2.py` (lane T's module) edited in one slice** (PUB1's eight rows) under V5.20 — the gate's
   «T's burn-down emptied for these sheets» — each a lower equality.

**Requests to other lanes (R14; not fixed here):**
- **LIB** — (1) a start-side velatura (`data-sfuma-start="paper|stone|brand|night"`, a `::before` twin of the foot's `::after`,
  6 rem for the sfumatura) so Universités' page rule can leave (deviation 2); (2) the band's own padding as a readable
  property (`--sez-pad` on `.sez`, restating the shell's clamp once) so a raccordo landing on a band's head rule reads
  `--sez-raccordo: var(--sez-pad)` instead of restating `clamp(var(--s-16), 8vw, var(--s-24))` in two page sheets; (3) the
  mosaico's floor light as a page-sheet-safe recipe (an inner shadow or a token for the lit floor) so a page lane's tiles can
  copy the rules without a gradient (deviation 4).
- **CLOSING** — (1) ratchet the eight route sheets' ceilings from 11 264 to the measures written beside them in
  `test_pages_v522_p1.py` (§3.9 c); (2) with `t-label` / `t-numeral` now on PUB1's templates, the restated nets of
  `.testa__label` (five lines) and `.tracciato__num` (three) in the library can go, as LIB planned (LIB NOTES §4); (3) the two
  `::first-letter` capitals: either admit a sentence-initial capital on a locked fragment to the typography guard's allowed
  list or keep the rows as the recorded residue; (4) `_persone-v2.css` and `_spazi-v2.css` keep one comment each where their
  Arabic rules stood — delete the comments with the aliases pass.
- **AR** — nothing: no locked text touched, no string added; the Arabic pages re-checked at AR's gate (3) and the matrix (R7′).
- **Steward** — the family `v524-pub1` in `OWNERSHIP_V54.json` with these `owns`: `templates/pathways/**`,
  `templates/ecosystem/**`, `apps/pathways/static/pathways/**`, `apps/ecosystem/static/ecosystem/**`,
  `tests/frontend/test_pages_v522_p1.py`, `tests/frontend/test_pages_browser_v522_p1.py`,
  `tests/frontend/test_pages_browser_v524_pub1.py` (new), `tests/frontend/test_typography_v2.py` (slice: PUB1's rows),
  `docs/design-v5/QA/v524/pub1/**`, the rebuilt dist (`static/css/dist/{pathways,ecosystem}/*.css`: 8 sheets) — and, for V5.29 (§13): the header block slice of `templates/enquiries/collaboration_proposal.html`, NEW `templates/ecosystem/partials/intesa.html`, `apps/ecosystem/static/ecosystem/{_intesa,intesa}.css`, `static/css/dist/ecosystem/intesa.css`, `apps/pathways/tests/test_views.py` (the numeral regex, §R a).

## 5. New msgids

None (0 strings; the catalogue +0 −0). JS: 0. Images: 0. Migrations: 0. No locked text touched.

## 6. Budgets (the V5.24 pass; V5.29's additions in §13) (gzip -9 = Python `gzip.compress(…, 9)` on the built dist; before = `4e882904`; two `npm run build` identical, the dist committed)

| Sheet (dist) | Before | After | Ceiling | Note |
|---|---|---|---|---|
| `pathways/index.css` | 10 188 | 10 655 | 11 264 (R4 b; was 10 240) | + 467: `_materia.css` (788 alone, less in the bundle), the PA-2 verb (the light, the rule), the raccordo's placement; − the mono seat, − the rtl rule |
| `pathways/sheet.css` | 9 695 | 10 147 | 11 264 (was 10 240) | + 452: the partial, the placement with its 64 rem twin; − the rail title's six lines and its Arabic twin |
| `pathways/training.css` | 8 843 | 9 257 | 11 264 (was 9 728) | + 414: the partial; − the kicker's four lines, − the rtl rule |
| `pathways/diplomas.css` | 8 950 | 9 388 | 11 264 (was 9 728) | + 438: the partial, the placement; − the mono seat, − the rtl rule |
| `ecosystem/pilot.css` | 9 477 | 9 851 | 11 264 (was 9 728) | + 374: the partial (the grounds are attributes, 0 B) |
| `ecosystem/companies.css` | 8 708 | 8 625 | 11 264 (was 9 216) | − 83: the quotation's clamp and the numeral's mono gone; no import (deviation 1) |
| `ecosystem/institutions.css` | 8 368 | 8 724 | 11 264 (was 9 216) | + 356: the partial, the foot's room; − the credit chip (ten lines) |
| `ecosystem/universities.css` | 7 504 | 7 519 | 11 264 (was 8 448) | + 15: the sfumatura and its stills; − the kicker's four lines; no import (deviation 1) |
| `pathways/pathways.css` · `ecosystem/ecosystem.css` | 4 621 · 4 886 | unchanged | 11 264 | untouched |
| `main.css` | 32 695 | 32 695 | ≤ 32 716 (R4 c) | untouched by construction (imports none of the partials) and measured |

Page totals (the sheets a page links on a desktop, the form sheets excepted — `test_pages_v522_p1.py`'s rule; the shared
chrome main + fronte + reveal + portico = 45 223): Parcours **55 878** · a sheet 55 370 · Formation 54 480 · Diplômes 54 611 ·
Projet pilote 55 074 · Entreprises 53 848 · Institutions 53 947 · Universités 52 742 — every one ≤ 56 320 (the Director expected
Parcours at 56 263 with 57 B left; LIB's `fronte.css` and `main.css` savings and this lane's deletions leave 442). JS 0; fonts
untouched; 0 strings.

## 7. Probes (headless, no slot; `evidence/v524/pub1/probe_p1.json`; the lane server 8788; 8 pages × 1440 · 1024 · 390 × fr · ar = 48 cells)

- **Grounds and seams** (the adjacency rule, stone ≡ pietra): Parcours paper → paper* → brand → paper (carta viva) → pietra;
  the sheet paper → stone → night → pietra → paper → brand; the pilot night → brand → paper → stone; Entreprises paper → stone →
  paper → stone → paper → stone; Institutions paper → photo → stone; Universités paper → brand; Formation paper → paper* →
  pietra → paper → brand; Diplômes paper → paper* → pietra → paper → brand — **0 same-kind seams** in 48 cells (`*` the head →
  moment touch the audit accepts on these moments' own frames).
- **The raccordi** (reduced motion in the probe: the stills): Parcours `--risale` x 123 at 1440 fr (the container's content
  start 100 + the trunk's 23), 48 px above the seam; x 345 at 390 ar (the mirror of 20 + 23), 32 px; the sheet `--notte` x 447
  at 1440 fr (100 + the body's second column 328 + the filo's 19), 96 px from the seam to the head rule; x 991 at 1440 ar (the
  mirror); x 39 at 390, 64 px; Diplômes x 127 at 1440 (100 + 27), 164 px to the plate's rule; x 345 at 390 ar, 132 px — every
  node 0 px off its line, the night line in `--accent-night` (`rgb(127, 209, 216)`), the others in `--line-structure`.
- **The material**: the velatura 192 px (128 on phones) in the stone's colour with the band's foot at the same measure; carta
  viva's light at `0 0` (fr) and `100% 0` (ar); the pietra grid 48 px masked `to left` (fr) / `to right` (ar); the come tiles
  `ink` with their floor layer; the filiera's `::before` inner shadow.
- **The roles**: every `t-label` Host Grotesk 13/16 600 uppercase (fr) and Readex Pro 14/20 600, no capitals (ar); the
  kickers and the rail title the same; every numeral Host Grotesk / Readex Pro 600, 28/32 or 36 (36/40 beside the rail); the
  Entreprises quotation 36/41.4 600 −0.72 px; the moments' numeral 36 px 600. **0 elements in ILE Mono** on the eight pages in
  either language.
- **The French runs on the Arabic pages** without the three deleted rules: `.filo__titolo` 20/28, `.dossier__definizione` 17/28,
  `.traversata__corpo` 17/28, `.tracciato__riga` 16/24 (the phone step-up), `.tracciato__titolo` 17/23.8 (the phone card's own
  1.4) — the tokens' Latin boundary (`:where(:root:lang(ar)) :where([lang="fr"], …)`) carries the leading; nothing double-spaced.
- **Overflow 0 and console errors 0** in all 48 cells; every page 200 in both languages.

## 8. Tests run (counts; `test_ile_v524_pub1` for the static set, `test_ile_v524_pub1b` for the browser twins — one pytest each; `PYTHONIOENCODING=utf-8`, the sentinel table in-process; logs under `C:/tmp/ile_v5_council/.work/v524-pub1/logs2/`)

| Run | Tree | Result |
|---|---|---|
| `r_static` — `test_pages_v522_p1.py`, `test_typography_v2.py`, `test_materia_v524_lib.py`, `apps/pathways/tests`, `apps/ecosystem/tests` | the recovered checkpoint | **512 passed**, 1 deselected (the numeral regex, §R a) |
| `r_num` — the prescribed-order test, its regex reading `tracciato__num t-numeral` (V5.20: same invariant) | merged with design-v5 | 1 passed |
| `b2` — `test_pages_browser_v524_pub1.py` (headless) | merged + «l'intesa» | 14 passed, 2 failed: the recipients' note on a phone at 3.2:1 on the composed ground (the pentagram's line and the red field under the sentence) — a real defect of this lane's change, fixed (§13), not a test change |
| `b3` — the same module `-k intesa` | after the fix | **5 passed** |
| `b4` — the whole module + `test_pages_browser_v522_p1.py` | the lane's head | **41 passed**, 0 failed, 0 skipped (9 min) |
| `s2` — `test_pages_v522_p1.py`, `test_design_docs.py`, `test_css_bundle_is_current.py`, `test_static_pipeline.py`, `test_interior_w3_f1.py`, `test_frontispiece_v515_c.py`, `test_chapter_marks.py`, `test_loader_rules.py`, `test_static_assets.py`, `apps/enquiries/tests` | merged + «l'intesa» | **428 passed** |
| `s3` — `test_pages_v522_p1.py`, `apps/ecosystem/tests`, `test_materia_v524_lib.py`, `test_typography_v2.py` | the lane's head | **498 passed**, 0 failed (22 min) |
| `b5` — `test_pages_browser_v524_pub1.py`, after merging design-v5 `0ad88a42` (v524-ar) | the lane's head | **16 passed** |
| `s4` — `test_pages_v522_p1.py`, `apps/ecosystem/tests`, `apps/pathways/tests/test_views.py`, `tests/i18n/test_arabic_completeness.py`, `test_css_bundle_is_current.py` | the lane's head after the AR merge | 328 passed, **3 failed — the BASE's**: `test_pages_v522_p1.py::test_the_form_pages_open_on_their_space_s_compact_band_and_keep_their_form` (the head's lead now `lang="ar"`), `::test_the_recipients_spans_rebuild_the_sentence` (the Arabic recipients one item, not six), `apps/ecosystem/tests/test_browser.py::test_french_fallback_keeps_its_punctuation_in_place_on_the_arabic_pages` (the French run gone) — all three red on a clean detached checkout of design-v5 `0ad88a42` (control run, `logs2/base3.log`): V5.27's hybrid renderings landed by lane AR, the tests still reading French on `/ar/`. NOT this lane's change and not amended here: the design-v5 worktree holds an uncommitted fix in progress (`apps/cms/locked_renderings.py`, `apps/ecosystem/services.py`, …) — the steward's; this branch takes it with the next `git merge design-v5`. |

The dead agent's last browser reds (§R b) were the probe's own: `_bring` scrolled with the shell's `scroll-behavior: smooth`
(`base.css`), so the raccordo's box, the band's box and the paint sample were read against a page still moving (77 px off,
«not painted» at 243 vs 241). The scroll is now `behavior: "instant"` — the assertions unchanged (V5.20: a reading fix, the
same invariant); the six raccordo cells green in `b2`. The «Target crashed» cells were the machine's (none since).
Ruff: the lane's three test modules were unformatted in the checkpoint (ruff format applied; `ruff check` clean).

## 9. The eye (gate 2)

- **The eight pages** — the dead agent's headed session (`chromium-1234` under a Chromium lock slot, label `v524-pub1-eye`,
  6 Nov 05:09–05:10; `tools/headed_shots.py`; `logs/headed1.log`): **200 frames**, 72 cells (1440 · 1024 fr, 390 · 360 fr + ar,
  1440 ar, reduced motion at 1440 fr and 390 ar), **0 console errors, 0 overflow, 0 running at rest, 0 mono**; every raccordo
  0 px off its line (Parcours 48 / 32 px rising, the sheet 96 / 64 px on the night band's head rule, Diplômes 164 / 132 px on
  the plate's rule). Stills `evidence/v524/pub1/shots/`, measures `headed_measures.json`, console `headed_console.json`. Kept
  (V5.28: never rebuild existing work); the cifix merge moved nothing on these pages (the colophon connector only; the build
  identical).
- **«L'intesa»** — headed `chromium-1234` under `C:/tmp/ile_locks/CHROMIUM_LOCK_A` (label `v524-pub1-intesa-eye`, taken and
  released in one session, < 2 min; `tools/headed_intesa.py`): the collaboration proposal's head at 1440 · 1024 · 390 fr and
  1440 · 390 ar (a frame mid-reveal at 0.6 s and the settled still), reduced motion at 1440 fr, the landing's approdo at 1440
  fr and 390 ar — **0 overflow, 0 console errors** in the 8 cells; stills `evidence/v524/pub1/intesa/headed_*.png` (and the
  headless iteration stills `a_*.png`, `before_*.png` beside them). The reveal's two animations then left getAnimations() once
  the fill was removed (the first session read 2 «running»: a `both` fill keeps a finished animation listed — fixed, §13).

## 10. V5.26 §9 — «would an expert digital product team have chosen this exact composition for this exact information?»

- **Parcours** — yes: the board is the page's one interactive journey (kept), the head now hands its route down into it (the
  raccordo), the four plates say «a threshold» with one verb instead of popping; one lit grid, one stone protection.
- **The eight sheets** — yes: steps on stone as a band (the procedure reads as one object), the filo crossing into «chi
  decide» is the information's own continuity (who decides comes after the steps), the protection on pietra like everywhere.
- **Projet pilote** — yes: the route is the page's subject, so it gets the page's one wash; the status plate stands on it,
  saying «not authorised» where the route is drawn.
- **Entreprises** — yes: the démarche is the page's argument, on stone between paper strips; the panorama keeps its window.
- **Institutions** — yes: the chamber (the recipients) dissolves into the ways onward; «Pour aller plus loin» — the Forum
  Vénétie–Maroc and the pilot, the bilateral cooperation itself — now stands on the Italy + Morocco ground (§13), the one band
  of the space where the two countries' meeting is the content.
- **Collaboration proposal (institution)** — yes: a form page's head is compact by design (preserved); the two countries
  framing the proposal's words at the two edges is the most an institutional form head should carry — identity without a poster.
- **Universités** — yes: the filiera on the wash, its top faded in from the head's paper (no seam of one kind).
- **Formation** — yes: Diplômes' order (crossing → protection → grid → compass): the protection sits where the reader meets
  the risk, before the offer.
- **Diplômes** — yes: the dossier's route runs into the protection — the documents and their verification are one sequence.

## 11. Not done, by design or out of scope (R14: post-acceptance candidates, not fixed here)

- **SYS (V5.29's shared visual system)** had not merged into design-v5 when this lane finished (design-v5 at `e6e6c34b`):
  nothing to inherit yet. When it merges: `git merge design-v5` into this branch, rebuild, re-run `b4`/`s3`; the pages draw only
  the library's primitives and T's tokens, so they inherit without page one-offs.
- **AR** — visible French on `/ar/` in this lane's pages, all locked / class C-SUBST content of the AR lane: the pilot tile's
  «PROJET PILOTE VÉNÉTIE–MAROC» and its line on the institutions' approdo, the Forum tile's subtitle, the collaboration
  head's lead and recipients' note (registry `lang="fr"`). Not touched (locked; R7′ is AR's).
- **T / SYS** — (1) national colour tokens: the palette has no Italian / Moroccan green or red, so `_intesa.css` names four
  page-local properties as colour mixes of palette tokens (`--cooperation`, `--p-laguna-550`, `--p-granata-600`,
  `--p-cotto-600`); a `--flag-it-*` / `--flag-ma-*` quartet in `v5/tokens.css` would let the partial read names. (2) A trap
  found on the way: the legacy `--rubric` is re-declared later in the cascade as `var(--ink-3)` (grey) and `--cooperation` as
  `var(--ok-700)` — a sheet reading `--rubric` for a red paints grey (this lane's first draft did). CLOSING's aliases pass.
- **CLOSING** — the eight route sheets' ceilings to their measures (§6); `institutions.css` now 9 149.
- The approdo's tiles are opaque, so on the landing the Italian fields read in the band's margin and Morocco's quarter beside
  the pilot tile — intended (the content dominant), recorded for the matrix's eye.

## 12. Discipline

R12: one pytest per database (`test_ile_v524_pub1`, `test_ile_v524_pub1b`), the lane server 8788 on `ile_v5_l4` (dev settings,
`ILE_DESIGN_PREVIEW=1`, `ILE_REFERENCE_DATE=2026-10-03`; `tools/serve.sh`), stopped at the lane's end; headed Chromium only
under `CHROMIUM_LOCK_A` (noclobber, label + time, released); headless probes without a slot; LF files (Python bytes writes;
heredocs); `npm run build` with the installed packages — two builds identical, the dist committed. Commits on `v524-pub1`
only, a «WIP: pub1 — …» checkpoint after every unit; design-v5 merged once (`git merge design-v5`, the cifix), never rebased;
nothing pushed, tagged or merged into design-v5; main untouched. The WhatsApp number and the private table never printed (the
stills show the footer as the page renders it; no page text written out). 0 strings, 0 JS, 0 images, 0 migrations.

## 13. V5.29 §15–§17 — «l'intesa», the Italy + Morocco ground of the Espace Institutions

**Where.** `/xx/collaboration/institutions/` (`enquiries:institution_proposal`, `apps/enquiries/urls.py`) — the head: the
compact civic band and the recipients' note stand inside `.intesa-campo`, the composition its first child (the header block
of `templates/enquiries/collaboration_proposal.html`, the form untouched; an institution only — a university's page draws
none). The landing `/xx/institutions/` (`ecosystem:institutions`) — «Pour aller plus loin», the band whose content is the
bilateral cooperation itself (the Forum Vénétie–Maroc, the Venice–Morocco pilot): the composition the band's first child,
behind the tiles on its stone. One composition, two seats.

**What.** `templates/ecosystem/partials/intesa.html` (NEW; aria-hidden, focusable=false, no text): two inline SVGs —
Italy's three vertical fields at the reading edge (green · the paper as white · red; `clamp(3.75rem, 7vw, 6.5rem)` wide so they
end at the reading edge; full band height, softened by a 7-unit blur, faded in at the top and out toward the foot by their own
gradients, 20 % — 16 % on phones), Morocco at the far edge's foot, its centre on the band's lower corner so only a quarter
shows (a soft radial red field at 22 % — 10 % on phones — and the green pentagram as ONE 1 px line at 30 %, standing down on
phones). `apps/ecosystem/static/ecosystem/_intesa.css` (NEW partial): every fill and stop painted from the palette's tokens
(four page-local mixes, §11), `mix-blend-mode: multiply` so dark ink stays dark, `z-index: 1` in a head (over the frontispiece's
own ground, which is not this lane's), `-1` on a section band (behind the tiles); forced colours and print: gone.
`apps/ecosystem/static/ecosystem/intesa.css` (NEW entry, one import) linked by the institution proposal only;
`institutions.css` imports the partial.

**RTL.** The placement mirrors (logical insets: Italy at the start edge — the right in Arabic —, Morocco at the far foot —
the left), the reveal's clip mirrored; the FLAGS NEVER: no transform anywhere on the drawings or their ancestors, the Italian
green left of the red in both languages, the pentagram upright with its left arm on the left — asserted in the browser test
at `/ar/` (screen matrices, the bands' boxes, the star's five points through `getScreenCTM`).

**Motion.** One slow mask reveal from each drawing's OUTER edge inward (the two meet around the words): the library's
`reveal-mask` (core/reveal.css, already linked on every public page) on `--motion-luce` (2.2 s) and `--ease-enter`, no fill;
at load in a head, on the band's own trigger on the landing (rise.js `wait` → `in`); reduced motion: no rule, no state — a
still composition (asserted).

**Contrast (measured).** The text made transparent, the darkest pixel of the composed ground under each text box against
the text's own ink: the head's title, lead and recipients' note ≥ 4.5:1 at 1440 and 390, fr and ar (the test). On a phone
the first draft put the pentagram's line and the red field under the note (3.2:1): the line stands down and the field
lightens there — 4.8:1 measured.

**Tool → decision → change** (real names, `evidence/v524/TOOLS_AVAILABILITY.md`):

| Tool (path) | Decision | Change |
|---|---|---|
| `impeccable` — `~/.claude/skills/impeccable/SKILL.md` (colour strategy; «cards are the lazy answer»; the absolute bans; the AI-slop test) | a «full palette» used deliberately — three named roles (Italy's green, the reds, Morocco's green as a line) and nothing else; no glass, no gradient text, no flag pasted as a card or a badge; the content dominant | the forms are fields and one line, never a flag rectangle; the four colour roles named in the partial |
| `ui-ux-pro-max` — `~/.claude/plugins/marketplaces/ui-ux-pro-max-skill/.claude/skills/ui-ux-pro-max/SKILL.md` (a11y and contrast on layered grounds before style) | a decorative layer over a head must not cost the words their contrast: multiply, low opacity, and a measured gate | `mix-blend-mode: multiply`; the contrast test; the phone fix (the line stands down, the field lightens) |
| `animate` — `~/.claude/skills/animate/SKILL.md` (should it animate; purpose; the codebase's tokens; reduced motion ships with it) | low frequency (once per visit), purpose orientation (the two sides meeting); the existing keyframe and tokens, not a new one; no fill so it leaves; reduced motion a still | `reveal-mask` on `--motion-luce` / `--ease-enter`, from each outer edge; the band trigger on the landing |
| 21st MCP | not used (R9: no 21st component enters; a decorative background needs no component) | — |

**Budgets (gzip -9 of the built dist).** `main.css` 32 695 (untouched, ≤ 32 716). `ecosystem/institutions.css` 8 724 → **9 149**
(≤ 11 264; the partial + the merged base's rounding). `ecosystem/intesa.css` NEW **712**. Page totals: Institutions 53 947 →
**54 372** (≤ 56 320); the institution proposal 51 769 → **52 481** without the form sheets (58 032 with them; a form page has
no §7.1 total — recorded), the university proposal unchanged 51 769. No dead rule to delete first (the partial is all new,
every rule drawn by both seats). **Ceilings re-recorded: none.**

**Test changes (V5.20, each cited in place).** `test_pages_v522_p1.py::test_the_form_pages_add_the_band_s_sheet_and_nothing_else`
— the institution proposal's ecosystem sheets must be EXACTLY `["css/dist/ecosystem/intesa.css"]`, the two other form pages
exactly none (before: none for all three) — the owner's V5.29 §15–§17 order, the invariant named exactly («never a space's page
sheet»). NEW in `test_pages_browser_v524_pub1.py`: `test_the_institutions_collaboration_head_stands_on_l_intesa_unmirrored_and_the_words_keep_their_contrast`
(1440 / 390 × fr / ar) and `test_l_intesa_reveals_once_from_each_outer_edge_and_leaves_and_the_landing_s_approdo_carries_it`.

**New msgids.** None (the composition carries no text). **Contract items for other lanes:** §11 (T / SYS tokens; CLOSING
the `--rubric` trap; AR the French on `/ar/`).

**V5.29's ten questions, for this lane's surfaces.** (1) raw CSS grids left — no new grid; (2) pure / heavy black — none added;
(3) headings on bold — untouched (T's roles); (4) backgrounds designed — yes, the one composition placed where the content is
the cooperation; (5) cards / materials — the library's, unchanged; (6) FAQ — not this lane; (7) icons — none added;
(8) protezione__campo — LIB's / SYS's primitive, unchanged here; (9) Institutions communicates Italy–Morocco elegantly — yes,
subtle, cropped, tokenised, unmirrored; (10) less editorial — the head gains identity without a word.
