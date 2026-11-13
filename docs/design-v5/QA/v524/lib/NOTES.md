# V5.24 lane LIB — the library: material, transitions, faces, verbs, type roles (labels v524-lib-build · v524-lib-improve)

Branch `v524-lib` (worktree `C:/tmp/ile_wt/v524-lib`), cut from `design-v5` at `554c82d2` (the v524-t merge: lanes S, M, P1,
S2, H, P2, PX and T merged). Lane server 8786 on the lane database `ile_v5_l5` (dev settings, `ILE_DESIGN_PREVIEW=1`,
`ILE_REFERENCE_DATE=2026-10-03`; the clone in step with `ile_v5`: 75 migrations, 19 users, no refresh needed); pytest on
`test_ile_v524_lib`, one at a time; headed `chromium-1234` under a Chromium lock slot (label `v524-lib-eye`); headless probes and
the browser twin without a slot (R12). Binding: V5.24 §7–§10, §15–§17 (the material, the seams, the icon faces, the verbs),
§11–§14 (the type roles in the library), V5.25, V5.26 §4–§8 (tool → decision → implementation; one primitive for one shared
behaviour), V5.20 (the strict test rule), `FINAL_DELIVERY_V2.md` §0–§2 (R3 the «raccordo» rename, R4 c/f the budgets, R9, R10
the real tools, R12, R14 the scope guard) and §3.3, `evidence/v524/BACKGROUND_MATERIAL_V2.md` §3.1, §3.2, §3.4, §3.5, §4.1 rows
1–4, `TYPOGRAPHY_V2.md` §4.2, §6 with lane T's contract and burn-down rows (`QA/v524/t/NOTES.md` §4), `IMAGERY_ATTRIBUTION.md`
D1–D8 as lane PX applied it (the five partials' credit rules are this lane's). Evidence of this lane:
`C:/tmp/ile_v5_council/evidence/v524/lib/` (`shots/` the headed stills, `headed_measures.json`, `probe_ar.json` the headless
Arabic probe, `console_errors.json`); scratch `C:/tmp/ile_v5_council/.work/v524-lib/` (`tools/`: `edit1-3.py` the three edit
passes, `measure.py`, `probe_ar.py`, `headed_shots.py`, `run.sh`, `chromium_slot.py`; `logs/`).

## 0. The decision in one screen

The library gives the page lanes the material they were promised and nothing they were not: one new page-only partial
(`static/css/v5/_materia.css`, 788 B gzip -9 minified alone, ≤ 800) with the four grounds' recipes and the four seam
primitives of BACKGROUND_MATERIAL_V2 §3.1–§3.2 under the Director's names (R3: «il raccordo», `.sez-raccordo`, never «varco»);
the T2 tile's face becomes the seal's niche on every page at once; «la protezione» stands on a drawing table — the shield drawn
low on the far side as the band's bookend, the plate's 3 px rule run on as a 1 px sill to the container's edge; the grid's tiles
stop settling and say «a threshold» instead (the rule draws, the glyph inks, the floor lights once — the light's rules live in
the mosaico sheet as the audit placed them, §4.1; PUB1's «Comment ça marche» plates take the same rules in `_index.css`); the
raccordo is the first child of the band it enters (every `.sez` isolates: hung under the leaving band it was painted over — the
reviewer's pixel proof, §10 B2); the library's type reads the twelve
steps — the head's label is the label role by name (`t-label`), the numerals the numeral role (sans 600 tabular, 28/32 or
36/40), the keyword and the term title at 600, no clamp, no mono seat, no descendant-form Arabic rule in LIB's sheets (the
two recorded residues of `_fronte.css` below); the five partials' credit rules are gone. No page composition moves (R9), no
template of a page lane is touched, `main.css` is untouched (32 695 B), 0 JS, 0 strings, 0 images, no migration.

## 1. What the owner sees, where

| Where (today, on this branch alone) | What changes |
|---|---|
| every T2 tile (the Parcours board's cards, the grids, the sheets' steps, the Forum's and AGAMI's tiles) | the white square becomes a niche: the vault in shade (`--line-rhythm`), the floor in light — the glyph in a recess on the plate's rule, 12.9:1 |
| «la protezione» on Parcours, the eight sheets, Formation, Diplômes, the home's S6 (on stone today; `pietra` when the page lanes import the partial) | the shield bookend low on the far side at 30 % of the structure's ink; the plate's rule continued as a 1 px sill to the band's edge, drawn after the plate's own rule; where the field's free span beside the 56 rem plate is under the shield's 12 rem — a field under 68 rem: every phone, 1024, the sheets' 912 px column — the bookend stands down and the sill alone runs on (a container query on the field, §10 B3) |
| the grids E «il mosaico» (Parcours, Formation, Diplômes, the pathway sheets' resources, FAQ's and the glossary's «il rimando») | the tiles no longer pop as squares: the card's rule draws to its resting 40 %, the glyph inks, the floor lights — a threshold; the doors' and the actors' discs keep their settle |
| the section heads (every V2 band) | the panel label in the label role (Host Grotesk 13/16 600, uppercase; 14/20 and no capitals in Arabic) instead of the ILE Mono folio; the title on `--t-title-2` / `--t-band` with the Arabic leading and a French title's Latin leading from the tokens |
| the page heads (every frontispiece) | the h1 on `--t-title-1` (Arabic 1.18; a French h1 on an Arabic page at 1.08 — F-7 closed for the sheets), the folio label 13/16 600 (14 in Arabic, no capitals), the lead 20/28 → 22/32, the caps h1 (the Forum's prescribed name, Parcours' and Entreprises' locked caps titles) on `--t-title-2` with the capitals' +0.02 em, the compact head on `--t-title-2`, the Contact address link on `--t-band`, the AGAMI name device with the display's tracking |
| the numerals (the sheets' filo, «la linea V2» stations, the board's station numbers) | Host Grotesk 600 tabular at 36/40 (stations, beside the rail) or 28/32 (rows), never the mono |
| the trust tablet's «Non.» and the term page's title | 600, the title and display weights of the family |
| the account and error pages | the account title and the error title on `--t-title-2` from 48 rem; the TOTP secret and the recovery codes in the sans (tabular, tracked) |
| the seams — raccordo, velatura, carta viva, incastro | drawn by the page lanes (HOME, PUB1, PUB2) on their pages with the partial's attributes and class; the fixtures prove them here — the raccordo painted across the seam and landing on the entered band's head rule (`shots/fx_raccordo-*_seam.png`), the doors' arched tops the whole 64 px over the band above (`shots/fx_incastro-*.png`) |

## 2. What changed (files owned per §3.3)

**New `static/css/v5/_materia.css`** (page-only, after `_sezioni.css`, never `main.css`; tokens and `color-mix` of tokens only,
logical properties only, no duration, curve, animation or transition of its own):
- `.sez[data-ground="pietra"]`: `--surface-area` + a `::before` drafting grid (1 px `color-mix(in srgb, var(--line-rhythm) 70%, transparent)` every 48 px, both axes) masked `to left` from the far side to 62 % (`--p-notte-950` stands for «opaque» — a mask reads alpha, no literal colour), the `[dir="rtl"]` twin `to right`;
- `.sez[data-ground="paper"][data-luce="origine"]`: `radial-gradient(60% 50% at 0 0, color-mix(in srgb, var(--accent-mark) 10%, transparent), transparent 70%)` over `--surface-page`; RTL `at 100% 0`;
- `.sez[data-sfuma="stone|paper|brand|night"]::after`: `block-size: 12rem` (8 rem under 48 rem), `linear-gradient(transparent, var(--sez-next))`, `--sez-next` = `--surface-area` / `--surface-page` / `--accent-wash` (the wash's first light, as `_casa.css` H0) / `--surface-night`, `z-index: -1` (above a photograph, under the words);
- `.sez-raccordo` (`data-verb="draw-y"`, `aria-hidden`) — **the first child of the band it ENTERS** (every `.sez` isolates and a later sibling paints over an earlier one: a span hung under the leaving band's foot was covered by the next ground — the gate's B2, fixed in the improve round): `--sez-raccordo: clamp(var(--s-8), 4vw, var(--s-12))` — 48 px at 1440, 32 at 390 (the letter's figures), fluid between: it is a strip's own padding, so the node lands on a strip's head rule at every width; `inset-block-start: 0` (from the seam down), `inset-inline-start: var(--raccordo-x, 0)` (the page lane places it on its route), 2 px `--line-structure`, `z-index: 1`, `--sez-d: var(--motion-draw)` (after the band's own line); the 6 px `--accent-mark` node (`::after`, centred on the line's end); `.sez-raccordo--notte` (`--accent-night`, entering night); `.sez-raccordo--risale` (the line that rises from a band into the one above — the board's trunk into the head's foot —, the same child of the later band, `transform-origin: 0 100%`, its node at the top);
- `.sez[data-incastro]`: `margin-block-start: calc(-1 * var(--s-16))`, `padding-block-start: 0` (the doors begin at the raised edge — the band's own 96 px padding had sunk the first door 32 px under the seam, the gate's B4), `background: linear-gradient(transparent var(--s-16), var(--surface-area) 0)`, its children `position: relative; z-index: 1` (the doors' arched tops the whole 64 px over the photograph);
- stills: `@media (forced-colors: active), print` hides the grid and the velatura; forced colours draw the raccordo and its node in `CanvasText`.

**`static/css/v5/_sezioni.css`** (the shell): `.testa__title` on `--t-title-2` / `--t-title-2-lh` / `--track-title-2`, the process and
router heads on `--t-band` / `--track-band`; the descendant rule `:is(:lang(ar), [dir="rtl"]) .testa__title` deleted (the tokens'
`:lang(ar)` block and its Latin boundary give the Arabic leading and a French title's Latin leading — F-7); `.testa__label` layout
and ink only, the type the role's by name (`t-label` in `_testa.html`) with the role's tokens restated under the class as a safety
net (§4: four lines — size, leading, weight, tracking; the capitals and their feature setting are the role's); the T2 tile's
niche face `linear-gradient(var(--line-rhythm), var(--surface-raised) 85%)` and `isolation: isolate` on every tile (a pattern's
floor layer sits between the vault and the glyph; 0 B gzip in the shell, m5); the light itself is NOT here (the shell is in every
page sheet and the home's total is the §7.1 letter — the gate's B1): it lives in `_sec-mosaico.css`; `.sez-keyword` 600 on
`--t-title-2`; `.sez-numeral` the numeral role at 36/40 (sans, 600, `--numeric-data`). **`components/sezioni/_testa.html`**:
`class="testa__label t-label"`.

**`components/sezioni/protezione.html` + `static/css/v5/_sec-strato.css`**: the plate in a field `.protezione__campo` (position
relative, grid — the plate's 68 px stand never collapses through it); `.protezione__davanzale` (`data-verb="draw"`, `--sez-d:
var(--motion-draw)`: after the soglia) at `inset-block-start: 68px`, `inset-inline: min(100%, 56rem) 0` — from the plate's far
edge to the container's, nothing on a phone where the plate is the whole field; the field is a size container
(`container-type: inline-size`) and `@container (max-width: 67.999rem) { .sez-fondale { display: none } }` stands the bookend
down wherever its 12 rem would sit behind the 56 rem plate — a field under 68 rem: every phone, 1024 (a 929 px field), the
sheets' 912 px column (the gate's B3; the 63.999 rem viewport media it replaces missed 1024 and the sheets); `.sez-fondale`
(aria-hidden) holding the
`ile-scudo` mark partial as a line drawing: `.approdo__fondale`'s layer generalised (`inset: auto 0 calc(-1 * var(--s-12))`,
12 rem, `z-index: -1`, overflow hidden, still), the svg 12 rem at the far side (`margin-inline-start: auto`), `fill: none`,
`stroke: var(--line-structure)`, `stroke-width: 0.375` (1.5 px at scale 4), `opacity: 0.3`; hidden under 64 rem. `.strato__corpo--parola
.ls-1` (the «Non.» keyword) on `--t-title-2` at 600; `.strato__lastra--scheda .strato__titolo` at `--w-display` with
`--track-display`; `.protezione__titolo` tracking `--track-label`; the `.strato__fondo .foto__credit` rule gone.

**`components/sezioni/mosaico.html` + `static/css/v5/_sec-mosaico.css`**: the glyph tile's verb `ink` (a disc's — `porte` or
`disc` — stays `node`); the tile's face light lives here as BACKGROUND_MATERIAL_V2 §4.1 placed it (the improve round, B1):
`.mosaico .sez-tile::before` the lit floor (`transparent 40%` → `--surface-raised`, `inset: 0`, `z-index: -1`, the radius
inherited), `opacity: 0` in `wait`, `sez-layer` over `--motion-standard` after `--motion-slow` + the sequence's stagger in `in`,
under `prefers-reduced-motion: no-preference` and `:root:not(.rm):not([data-input="key"])`, fill backwards; PUB1's «Comment ça
marche» plates take the same rules in `_index.css` scoped to their plates (§4.1's ≈ 80 B): 1 203 → 1 355 B (§6).

**`static/css/v5/_fronte.css`**: the compact title on `--t-title-2`; the folio label on the role's tokens (`--t-label`,
`--t-label-lh`, `--w-label`, `--track-label`, `--feat-caps`, uppercase — restated: §4) and `:lang(ar) { text-transform: none }` in
the subject form; the h1 on `--t-title-1` / `--t-title-1-lh` / `--track-title` and the descendant rule at lines 194–198 deleted;
the caps h1 on `--t-title-2` / `--t-title-2-lh` / `--track-display-caps` (its 64 rem `2.5rem` literal gone); the lead on
`--t-lead-lh` (its 64 rem `1.375rem` literal gone: the tokens carry 22/32); the words-first lead at ≥ 64 rem on `--t-entry` /
`--t-entry-lh` (20/28 — a French lead on an Arabic page at 1.4, F-7); the route head's lead `1.125rem` → `--t-body` / `--t-body-lh`;
the Contact address link's clamp → `--t-band` / `--t-band-lh` / `--track-band`; `.fronte__name` `letter-spacing:
var(--track-display)` and nothing else (R3.3); the seven `.foto__credit` rules gone; the header's stale «Vazirmatn».

**`static/css/v5/_sec-tracciato.css` + `components/sezioni/tracciato.html`**: `.tracciato__num` the numeral role — `t-numeral`
in the template, size / leading / weight restated in the sheet for PUB1's board (§4), the sans inherited, the mono gone.
**`static/css/v5/_linea-v2.css`**: the station numeral on `--t-numeral` / `--t-numeral-lh` (28/32 down the edge) and
`--t-numeral-lg` at `line-height: 1` across (36 in a 36 px line box: a solo numeral whose box is the grid's first row — the row
V5.22 composed the marks, the route and lane H's hero line on; the gate's B6: at 36/40 the row grew 4 px and the home's hero line
missed the orientation seal's sill by 4 px); the route's inset and the carriage return read the same `--t-numeral-lg` in place of
`--t-title`.
**`static/css/v5/_sec-filo.css` + `components/sezioni/filo.html`**: `.filo__num` 28/32, 36/40 beside the rail.
**`static/css/v5/_servizio.css`**: the error and account titles on `--t-title-2` from 48 rem; the TOTP secret / recovery codes
without the mono (`--numeric-data`, `--track-label`); the `:lang(ar)` title rule deleted (the tokens carry it).
**`static/css/v5/_photo.css`, `_compose.css`, `_sec-mappa.css`**: the credit rules gone (PX's contract).
**`apps/core/static/core/sezioni.css`** (the fixtures' bundle, the library's own test kit; not named in §3.3 — a one-line
deviation, recorded): imports `_materia.css` after the shell so the fixtures prove it.

## 3. Tool → decision → change (V5.26 §4; real names per `evidence/v524/TOOLS_AVAILABILITY.md` — no «design-critique», no «design-handoff»)

| Real tool (path) | Decision | Change |
|---|---|---|
| `impeccable` — `~/.claude/skills/impeccable/SKILL.md` (the shared design laws: the AI-slop tells, the absolute bans — side stripes, gradient text, glass, identical card grids; «cards are the lazy answer») | the T2 tile is the one «identical card» tell left in every grid: its face becomes a niche (shade above, light below), not another white square; the pietra grid is a drafting ground masked toward the plate, never a side stripe or a frame; no glass, no gradient text, no blurred image field (the audit's refusals held) | `_sezioni.css` §3 (the face), `_materia.css` (the grid's mask), `_sec-strato.css` (the bookend as a line drawing, not a badge) |
| `taste-skill` — `~/.claude/skills/taste-skill/SKILL.md` (Rule 4 anti-card overuse: elevation only where it carries hierarchy; §7 no outer glows) | «la protezione» keeps its one raised plate; the band around it gains structure (the sill continuing the plate's rule, the bookend) instead of a second box; the tile's light is a layer of the face, no glow | `protezione.html`, `_sec-strato.css`, `_sezioni.css` |
| `figma:figma-use-motion` + `figma:figma-implement-motion` — `~/.claude/plugins/cache/claude-plugins-official/figma/2.2.157/skills/figma-use-motion/SKILL.md`, `…/figma-implement-motion/SKILL.md` (the Figma MCP is not authenticated: the method applied to the product's tokens — pick the phases first; one timing language; honour reduced motion with the resting state; validate one animation end to end; factor repeated motion into one component with the varying value as a parameter) | the raccordo's phases: the section's own line draws (0 → 900 ms) · the raccordo draws (900 → 1 800, `--sez-d: var(--motion-draw)`) · its node rounds off as the draw ends — the node is the line's tip (no second animation: with `scale` on the span the tip is a drop flattening into a circle, hidden only by its own thinness) — on the existing `draw-y` verb, `--ease-sine`, fill backwards; `--raccordo-x` the one parameter the pages vary; the tile's light one step after its rule begins (`--motion-slow` + the stagger), `--motion-standard` long | `_materia.css` (`.sez-raccordo`, no rule of its own for the node), `_sec-mosaico.css` (the light), the browser twin's timing assertions (delay 0.9 s, the node within 2 px of the head rule) — and, the improve round, «validate one animation end to end» taken literally: the reviewer's pixel proof showed the drawn line unpainted under the next ground; the span moved into the band it enters, the twin now reads the paint (the line's column against the ground beside it) |
| `find-animation-opportunities` — `~/.claude/skills/find-animation-opportunities/SKILL.md` (the four-question gate: frequency, purpose, speed, function) | PASS: the raccordo (occasional — once per seam per visit; spatial consistency — where the route goes; 900 ms on a marketing surface; not functional data); the tile's floor light (state indication — a threshold; 200 ms); the sill's draw (spatial consistency — the plate's rule run on; once). REJECTED: a parallax on the pietra grid (decoration on a reading surface), a drift or shimmer on the velatura (a gradient must not animate, §6.1), the bookend's stroke draw (out of sight, decoration), any hover motion on index rows (tens of times a visit, keyboard-reached), a node that lights apart from the line (a second beat for no information) | nothing animates in `_materia.css` of its own; the still rules under forced colours and print |
| `ui-ux-pro-max` (`~/.claude/plugins/marketplaces/ui-ux-pro-max-skill/.claude/skills/ui-ux-pro-max/SKILL.md`, the priority a11y → touch → performance before style) | the bookend hides wherever it would sit half behind the plate — the FIELD's free span, not the viewport, is what decides (the improve round: a 64 rem viewport media left the shield behind the plate at 1024 and on the sheets at every width; a container query on the field, 68 rem = the 56 rem plate + the 12 rem shield, stands it down exactly there); the sill has zero length on a phone (no stray line); the niche face measured for the glyph (12.9:1 on the darkest stop); the TOTP secret and recovery codes leave the mono only because their alphabets (base32; allauth's code set without l, o, 0, 1) need no disambiguation | `_sec-strato.css` (`container-type: inline-size` on the field, the `@container` query), `_servizio.css`, `test_materia_v524_lib.py::test_the_tile_s_face_is_a_niche_and_keeps_the_glyph_legible`, the twin's 1024 case |
| the typography audit's crawler, re-aimed at 8786 (`tools/probe_ar.py`: lane T's four Arabic guards on the burn-down pages) | the sheet `/ar/parcours/salaried_work/` passes all four guards at 1440 and 390 → it joins T's guarded list; Entreprises' and Le projet's residues are PUB1's and PUB2's | `test_typography_v2.py` (ARABIC_PAGES + the two rows reworded, §4), `_fronte.css` (the words-first lead's leading found by the probe: 20/32 → 20/28) |

## 4. Contract items — applied for other lanes · requested of other lanes · deviations recorded

**Applied here for other lanes.** (a) T's contract (TYPOGRAPHY_V2 §4.2, §6): every type rule in LIB's sheets reads the twelve
steps and the roles; T's burn-down rows for `_sezioni.css`, `_sec-tracciato.css`, `_linea-v2.css`, `_servizio.css` deleted
(equality → measured 0), `_fronte.css` lowered 6·2·1·1 → `{"clamp": 2, "uppercase": 1}` with its reasons in the table (gate 4;
V5.20: the same test, a lower equality); `/ar/parcours/salaried_work/` moved from `ARABIC_PAGES_BURNDOWN` into `ARABIC_PAGES`
(a stronger invariant: all four guards now hold there), the two remaining rows reworded to their page lane's residue. (b) PX's
contract (IMAGERY_ATTRIBUTION D1–D8): the `.foto__credit` rules of `_photo.css` (3), `_fronte.css` (7), `_sec-strato.css` (1),
`_compose.css` (1), `_sec-mappa.css` (1) deleted — 13 rules, the five partials the Director named. (c) The material contract the
page lanes build against (BACKGROUND_MATERIAL_V2 §3 as renamed by R3): the attributes `data-ground="pietra"`, `data-luce="origine"`,
`data-sfuma="stone|paper|brand|night"`, `data-incastro`; the class `sez-raccordo` (+ `--risale`, `--notte`) with `data-verb="draw-y"
aria-hidden="true"` and `--raccordo-x` — **placed as the FIRST CHILD of the band the line enters** (before its `.container`; the
`--risale` line likewise a child of the lower band, rising into the one above), its length `--sez-raccordo` = a strip's padding so
the node lands on a process or statement head's rule; a page lane landing on a PANEL head (the rule centred in the label's line)
or on a band's deeper padding sets `--sez-raccordo` on its placement (inline or a page rule) to the distance from the seam to the
head rule's axis; the node is `--accent-mark`, so `--raccordo-x` lands it beside the head rule's start or on a structure line,
never inside the 48 px gold rule where it would vanish by colour (the reviewer's m4); the import `@import url("../css/v5/_materia.css")`
(from `apps/<app>/static/<app>/`) after `_sezioni.css`.

**Requested of other lanes (R14; not fixed here):**
- **PUB1** — `templates/pathways/_tracciato.html` names two library classes without their roles: `class="tracciato__nome testa__label"`
  → add `t-label` (the label role; the sheet restates size/weight/tracking meanwhile, never the capitals), `class="tracciato__num"`
  → add `t-numeral` (the tabular figures; size/leading/weight restated meanwhile). The PA-2 «Comment ça marche» plates:
  `data-verb="ink"` on their tiles and the three light rules of `_sec-mosaico.css` (`::before` the floor, `opacity: 0` in `wait`,
  `sez-layer` in `in`) copied into `_index.css` scoped to the plates (BACKGROUND_MATERIAL_V2 §4.1's ≈ 80 B — the shell carries no
  light, B1). The sheets' `_sheet.css` / `_index.css` burn-down rows are theirs.
- **HOME** — `templates/pages/home/_ecosystem_colophon.html` names `testa__label colofone__label` twice → add `t-label` (same
  interim). The home's S6 band imports `_materia.css` through `pages.css` for `pietra`; the sill and the bookend already draw on stone.
- **PUB2** — `/ar/le-projet/`: `_projet.css:172` `.racconto .racconto__titolo[id="project-why-title"]:not(:lang(ar))` gives the French
  h2 its 2rem leading (24/32 = 1.33 > 1.3: T's guard) — the library's `.racconto__titolo` reads `--t-band-lh` (1.25 inside a `lang="fr"`
  run); the `_projet.css` rule is theirs. The FAQ explorer's `.faq-esploratore__categoria` and AGAMI's registers: their rows.
- **CLOSING** — (1) `templates/pages/partials/_ingresso.html:62` (lane PX's file, closed): `class="ingresso__label t-label"`, then
  delete the six restated declarations and the `:lang(ar)` rule of `_fronte.css` «3 · the type» and the row `{"uppercase": 1}`; (2) once
  HOME and PUB1 carry `t-label` / `t-numeral`, drop the five restated lines of `.testa__label` and the three of `.tracciato__num`;
  (3) `.sez-keyword` has no consumer in any template (a §6.2 device): coverage decides; (4) the name device's two clamps stay by the
  Director's letter (`.fronte__name`, `.fronte__name-rest`) — the burn-down table keeps `_fronte.css: {"clamp": 2}` as a recorded
  residue, not a defect; (5) `apps/core/static/core/sezioni.css` (the fixtures' bundle, 11 290 → 11 727 B) has no ceiling: none added.
- **Steward** — the family `v524-lib` in `OWNERSHIP_V54.json` with these `owns`: `static/css/v5/_materia.css` (new), `_sezioni.css`,
  `_sec-strato.css`, `_sec-mosaico.css`, `_sec-tracciato.css`, `_sec-filo.css`, `_sec-mappa.css`, `_linea-v2.css`, `_servizio.css`,
  `_fronte.css`, `_photo.css`, `_compose.css`, `templates/components/sezioni/{_testa,protezione,mosaico,tracciato,filo}.html`,
  `apps/core/static/core/sezioni.css`, `tests/frontend/test_materia_v524_lib.py` (new), `test_materia_browser_v524_lib.py` (new),
  `tests/frontend/test_typography_v2.py` (slice: the burn-down rows of LIB's sheets and the Arabic page rows), `docs/design-v5/COMPONENT_PROVENANCE.md`
  (the V5.24 block), `docs/design-v5/QA/v524/lib/**`, the rebuilt dist (`static/css/dist/**`: 19 sheets).

**Deviations from §3.3's letter, each with its reason:**
1. **The raccordo has no `wait` / `in` rule of its own in `_materia.css`** (R3 lists «the wait / in rules on [data-sec-state]»): the
   verb is `_reveal.css`'s `draw-y`, whose generic rules already hold the first frame (`scale: 1 0`) and play `sez-draw-y` on the
   trigger with `--sez-d`; a second rule for the node (`opacity` after the draw) cost 150 B and a second beat the four-question gate
   rejected — the node is the line's tip. Measured: 788 B against the 800 ceiling with the rule out (919 with it in). **And the span
   is the ENTERED band's first child with `inset-block-start: 0`** (R3 / §3.2 wrote `inset-block-end: calc(-1 * var(--sez-raccordo))`
   on the leaving section): every `.sez` is a stacking context (`isolation: isolate`) and a later sibling paints over an earlier
   one, so a line hung under the leaving band's foot was covered by the next ground — nothing painted (the gate's B2, the
   reviewer's dark-pixel fraction 0.00 as built). Fix B of the review (the Director's choice): robust for consecutive seams,
   779 → 788 B; fix A (`.sez:has(.sez-raccordo) { z-index: 1 }`) passed the ceiling and let two consecutive raccordi cover each other.
2. **`--sez-raccordo` is `clamp(var(--s-8), 4vw, var(--s-12))`**, not two values under a media query: 48 at 1440 and 32 at 390 as
   the letter says, and equal to a strip's own padding at every width, so the node lands on the next strip's head line everywhere
   (the browser twin's assertion); a page lane may still set `--sez-raccordo` on its own placement.
3. **`.sez[data-incastro]`**, not `.sez--porte[data-incastro]`: the attribute is the contract (the doors are its one user today);
   the ground painted is `--surface-area` (the letter's), its children lifted.
4. **The tile's floor light lives in `_sec-mosaico.css`** (the audit's placement, §4.1) — the build round had housed it in the shell
   as «one home for every tile that inks»; the gate's B1 overturned that: the shell is bundled by every page sheet, and the home's
   total went to 61 470 B against the §7.1 letter 61 440 (R4 a never raises it; §0 item 4 every merge leaves `design-v5` green). The
   improve round moved the three rules (the `::before` floor, `opacity: 0` in `wait`, `sez-layer` in `in`) to the mosaico sheet
   scoped `.mosaico .sez-tile::before`, folded the tile's `isolation: isolate` into the shell's `.sez-tile` (0 B gzip there; m5) and
   dropped the `font-feature-settings` line from the `.testa__label` net (the capitals' setting is the role's): the shell 2 514 →
   2 382 B, `pages.css` 11 357 → 11 302, the home 61 470 → **61 415 ≤ 61 440** (the base 61 419). `_sec-mosaico.css` 1 203 → 1 355:
   the audited «≈ 120» was an estimate — the same block cost 70 B among the shell's many like selectors and costs 152 B alone in the
   small sheet, and no declaration can go (the layer's corner, its first frame, its delay); every spelling was measured (unscoped
   state rules 1 353, the delay reordered 1 353–1 355) — the ceiling is re-recorded at the measure under R4 f, cited in
   `test_sezioni_v522_s.py` and `test_materia_v524_lib.py`, never up; no route sheet passes its ceiling (§6). PUB1's plates take
   their audited ≈ 80 B in `_index.css` (§4, request).
5. **The role's tokens are restated under `.testa__label` and `.tracciato__num`** (no capitals, no mono, no clamp — nothing the
   burn-down counts): two page-lane templates name the classes without the roles (HOME's colophon, PUB1's board); without the net
   their labels and numerals would fall to the body's 17/400 on the preview between this merge and theirs. CLOSING drops the net.
6. **`[data-fronte] .ingresso__label` keeps `text-transform: uppercase`** (the one uppercase the table still counts for `_fronte.css`):
   `_ingresso.html` is lane PX's file whole (§3.2) and PX is closed — the request goes to CLOSING; the label's size, leading, weight
   and tracking are the role's tokens already, and the Arabic rule is in the subject form.
7. **The bookend stands down wherever the FIELD's free span beside the plate is under its 12 rem** — a container query on
   `.protezione__campo` (`container-type: inline-size`; `@container (max-width: 67.999rem)`: the 56 rem plate + the 12 rem shield),
   not a viewport media: the build round's `@media (max-width: 63.999rem)` left the shield 159 px behind the plate at 1024 (a 929 px
   field) and 176 px behind it on the eight pathway sheets at 1440 (a 912 px column) — the gate's B3, against V5.25 §2's «desktop
   composition → 1440 + 1024». The letter places it «low on the far side» — a wide field's device; `_sec-strato.css` 1 541 → 1 557
   (≤ 1 638). The design system already queries containers (`_formwork.css`).
8. **The caps h1 (`.ingresso__title--caps`) on `--t-title-2` with `--track-display-caps`**, one step under the plain h1 as its 40 px
   stood one step under 56: 36 at 1440, 28 at 390 (30 before) — the only size the letter did not name; `max-inline-size: 23em` kept.
9. **The lead's measure stays 38 rem** (`[data-fronte] .ingresso__lead`): the audit's 36 rem would re-wrap every approved head's
   lead; a measure is not a clamp, and the heads are preserved compositions (KEEP). Recorded for CLOSING's docs pass.
10. **The route head's 18 px lead → 17/28 (`--t-body`)** and **the words-first lead at ≥ 64 rem → 20/28 (`--t-entry`)**: the scale's
    steps nearest the literals; the first keeps Parcours' way control in the first screen (round 2 of W3's reason), the second gives
    a French lead on an Arabic page a Latin leading (T's guard: ≤ 1.5; the probe found 1.6 with `--t-lead-lh`).
11. **`apps/core/static/core/sezioni.css`** edited (one `@import`): the library's fixtures bundle, no lane's in §3 — so that the
    fixtures (the «specimen board» of gate 2: the library is no catalogue in the product, §5/§29) can prove the material.
12. **`tests/frontend/test_typography_v2.py`** (lane T's module) edited in two slices under V5.20, each a lower equality or a
    stronger guard: the burn-down rows of LIB's sheets (gate 4 says «T's burn-down table emptied for LIB's sheets») and the Arabic
    page rows (a page that passes moves into the guarded list; the two residues renamed to their lanes).

## 5. New msgids

None (0 strings). JS: 0. Images: 0. Migrations: 0.

## 6. Budgets (gzip -9; the partials minified alone with the repository's esbuild, the dist as built; before = `554c82d2`)

| Measure | Before | After | Ceiling | Note |
|---|---|---|---|---|
| `_materia.css` (new) | — | 788 | ≤ 800 (§3.3) | per importing sheet; the page lanes pay it in their route sheets (783 in the build round; + the raccordo's inset and the incastro's padding) |
| `_sezioni.css` | 2 444 | 2 382 | ≤ 2 382 (the measure, `test_materia_v524_lib.py`) | the niche face and the tile's context, the label role's net (four lines), the numeral role; − 62 against the base (the mono folio and the clamps gone; the light NOT here — B1) |
| `_sec-strato.css` | 1 423 | 1 557 | 1 638 (unchanged) | + 134 ≤ the audited ≈ 160: the field (a size container), the sill, the bookend, the container query |
| `_sec-mosaico.css` | 1 203 | 1 355 | **1 355 (re-recorded at the measure, R4 f; was 1 229)** | + 152: the tile's face light (the audited «≈ 120» an estimate — every spelling measured 1 353–1 365; deviation 4) |
| `_sec-tracciato.css` | 1 418 | 1 420 | 1 434 (unchanged) | the numeral role restated (longhand, the variant through the class) |
| `_sec-filo.css` | 999 | 1 012 | 1 024 (unchanged) | the numerals 28/32 and 36/40 |
| `_linea-v2.css` | 1 618 | 1 622 | the passage increment ≤ 1 229 (unchanged, green) | the numeral role; the across numeral in a 36 px line box, the geometry on the same size (B6) |
| `_fronte.css` | 5 637 | 5 507 | — | − 130: seven credit rules, two literals, four clamps |
| `_servizio.css` | 2 426 | 2 388 | — | − 38 |
| `_photo.css` · `_compose.css` · `_sec-mappa.css` | 1 174 · 1 212 · 1 320 | 1 071 · 1 199 · 1 307 | the panorama increment ≤ 716 (unchanged, green) | the credit rules |
| `main.css` (dist) | 32 695 | 32 695 | ≤ 32 716 (R4 c) | untouched by construction (imports none of the partials) |
| `pathways/index.css` · `sheet.css` · `training.css` · `diplomas.css` (dist) | 10 117 · 9 701 · 8 788 · 8 895 | 10 188 · 9 695 · 8 843 · 8 950 | 10 240 · 10 240 · 9 728 · 9 728 (P1's; R4 b) | + 71 / − 6 / + 55 / + 55 before PUB1's import (the sheets that bundle the mosaico carry the light; the sheet's does not) |
| `pathways/pathways.css` · `ecosystem/ecosystem.css` (dist) | 4 716 · 4 977 | 4 621 · 4 886 | 11 264 | the credits |
| `ecosystem/pilot.css` · `companies.css` · `institutions.css` · `universities.css` (dist) | 9 508 · 8 701 · 8 381 · 7 630 | 9 477 · 8 708 · 8 368 · 7 504 | 9 728 · 9 216 · (P1's) · 8 448 | |
| `pages/css/pages.css` · `hero.css` · `fronte.css` · `interior.css` (dist) | 11 306 · 10 899 · 6 141 · 8 827 | 11 302 · 10 899 · 6 009 · 8 873 | 12 288 · 11 264 · — · 11 264 | **the home 61 415 / 61 440** (main 32 695 + pages 11 302 + hero 10 899 + reveal 3 526 + portico 2 993; the base 61 419; the build round's 61 470 was B1) |
| `cms/lettura.css` · `servizio.css` · `errori.css` · `forum/forum.css` (dist) | 6 512 · 2 879 · 3 647 · 7 369 | 6 546 · 2 838 · 3 609 · 7 303 | 9 216 · — · — · 8 192 | the reading pages and the Forum under their letters (`test_frontispiece_v515_c.py`, 93 passed) |
| `core/sezioni.css` (dist, the fixtures' bundle) | 11 308 | 11 759 | none | + `_materia.css` |
| JS (`rise.js`, the modules) | unchanged | unchanged | §7.2 | 0 JS |

The page-type totals (`test_frontispiece_v515_c.py`, every page type under its §7.1 letter — the home 61 415, no total raised)
are measured in §7; two `npm run build` runs identical (77 files; `logs/imp_dist1.sha` = `imp_dist2.sha`), the dist committed.

## 7. Tests run (counts; database `test_ile_v524_lib`, one pytest at a time per database — the browser set on a second lane
database `test_ile_v524_libb` so neither waited; `PYTHONIOENCODING=utf-8`, the sentinel table in-process; logs under
`C:/tmp/ile_v5_council/.work/v524-lib/logs/imp_*.log`)

| Run | Modules | Result |
|---|---|---|
| `imp_static3.log` | `tests/frontend/test_materia_v524_lib.py` (the lane's static module, V5.20-cited), `test_sezioni_v522_s.py` (lane S's library module with the re-recorded mosaico ceiling) | 61 passed |
| `imp_browser2.log` (headless, no slot) | `tests/frontend/test_materia_browser_v524_lib.py` — the raccordo at 1440 and 390, fr and ar, incl. the paint (the line's column 41 points darker than the ground beside it), the bookend at 1440 and 1024, the incastro, the mosaico verb, reduced motion and the keyboard | 14 passed |
| `imp_totals.log` | `tests/frontend/test_frontispiece_v515_c.py` — every page type under its §7.1 total (the home 61 415 ≤ 61 440) | 93 passed |
| `imp_static_set.log` | `test_pages_v522_p1.py` (the route sheets' ceilings), `test_rm_flag_parity.py` (untouched), `tests/i18n/test_rtl_static.py`, `test_static_pipeline.py`, `tests/compliance/test_locked_content.py`, `test_imagery_credits_v524.py`, `test_typography_v2.py` (T's burn-down, LIB's rows emptied), `test_v5_tokens.py`, `test_fonts_budget_v2.py`, `test_design_docs.py`, `test_css_bundle_is_current.py` (the committed dist = the build), the neighbours `test_sezioni_v522_s2.py`, `apps/pages/tests/test_interior_v522.py`, `test_chapter_marks.py`, `test_layout.py`, `test_motion_v512_a_w2.py`, `apps/pages/tests/test_home_v522_h.py`, `test_home.py`, `apps/pathways/tests`, `tests/test_check_ownership.py` (`-m "not browser"`) | in flight at the commit (the harness closed the round first): the result is the last line of logs/imp_static_set.log — the steward reads it before the merge; the two base reds of m2 are expected there |
| `imp_browser_set.log` (headless, no slot) | `test_sezioni_browser_v522_s.py`, `test_seal_heads_browser_v522_s.py` (the library's own browser contracts), `apps/pages/tests/test_home_browser_v522_h.py` (lane H's — `test_the_hero_line_runs_down_into_the_orientation_seal_sill[fr/ar]` the gate's B6), `test_pages_browser_v522_p1.py`, `test_sezioni_browser_v522_s2.py` | in flight at the commit: the last line of logs/imp_browser_set.log — the steward reads it before the merge; the three + two base reds of m2 are expected there, the hero-line test is the one to read (the headed measure already gives 0.0 px) |
| `ruff check` on the three test modules and the build | 0 |

Red on the base `design-v5` `554c82d2` already and not this lane's (the reviewer's m2, verified by its control run; the steward
/ CLOSING re-point them under V5.20 on T's tokens): `test_home_v522_h.py::test_final_round_the_arabic_titles_…` (`--t-folio-lh`
now an alias), `test_home_browser_v522_h.py::test_final_the_arabic_index_s_titles_…` × 3 (the S3 connector under the Arabic
label's 20 px line) and `test_pages_browser_v522_p1.py::test_the_institutions_head_…` × 2 (16 px on a phone against a 15.5 cap).

## 8. Stills (`C:/tmp/ile_v5_council/evidence/v524/lib/shots/`; headed `chromium-1234` under `CHROMIUM_LOCK_A`, label
`v524-lib-improve-eye`, 6 Nov 2026 01:49:35 → 01:51:58, the lane server 8786 on `ile_v5_l5`; measures in
`evidence/v524/lib/headed_improve.json`, console `console_errors_improve.json`: 0 errors, overflow 0 on every frame)

| Frame(s) | What is seen |
|---|---|
| `fx_raccordo-{fr,ar}_{1440,1024,390}[_rm].png` + `*_seam.png` (the 160 × 120 px crop at the seam) | the raccordo PAINTED from the seam down to its node ON the entered strip's head rule: height 48 · 41 · 32, 0.0 px off the band's top edge, 0.0 px off the rule's top at every width in both directions; the line's column 193 against the ground's 235 (luminance 0–255); `scale: none` at rest, 0 animations running after the draw; the same still under reduced motion |
| `fx_incastro-{fr,ar}_{1440,1024,390}[_rm].png` | the doors' band 64 px up, the first door's arched top the whole 64 px over the paper band above (`doorOverAbove` 64 in every cell; 520 → 424 at 1440) |
| `fx_pietra-{fr,ar}_{1440,1024,390}[_rm].png` | 1440: the drafting grid on the far side fading toward the plate, the sill 344 px from the plate's far edge to the container's, the shield 1140–1332 (fr) / 92–284 (ar) low on the far side, nothing over the plate; 1024: a 929 px field, the plate 896, the sill 33 px, the bookend `display: none`; 390: the plate the whole field, no sill, no bookend |
| `parcours_{fr,ar}_{1440,1024,390}_protezione.png`, `sheet_{fr,ar}_{1440,1024}_protezione.png` | the product: Parcours at 1024 with the sill alone (the shield stood down — B3 closed), at 1440 with the bookend beside the plate; the salaried_work sheet's 912 px column at 1440 with its 16 px sill and no bookend (m9: right by construction), at 1024 the plate the whole column |
| `home_{fr,ar}_{1440,1024}_head.png`, `home_*_orientation.png` | the hero's first screen as before; the hero line meeting the orientation seal's sill — `lineBottom − sealBottom` 0.0 px at 1440 and 1024, fr and ar (B6 closed) |
| `fx_mosaico-{fr,ar}_1440.png`, `fx_luce-{fr,ar}_1440.png` | the grid's tiles after the trigger: rule drawn, glyph inked, the floor lit from the mosaico sheet (B1's new home); carta viva's light at the origin corner, mirrored |

The build round's frames of 6 Nov 00:10 (the fr pass: the other fixtures, the real pages' heads and bodies) stay beside them;
the reviewer's own 187 frames are under `evidence/v524/lib/qa/`.

## 9. Not done, by design or out of scope (R14: post-acceptance candidates, not fixed here)

- The page lanes' placements (the grounds, the raccordi, the velature, the incastro, the imports) — HOME, PUB1, PUB2 by their tables.
- `.sez-keyword` without a consumer; the legacy aliases (`--t-title`, `--t-folio`…) still read by other lanes' sheets — CLOSING.
- The `tracciato__nome` / `colofone__label` / `tracciato__num` role classes in HOME's and PUB1's templates (§4).
- `/ar/le-projet/`'s French h2 leading (`_projet.css:172`) — PUB2; the pathway sheets' `_sheet.css` descendant rule — PUB1.
- Observed, not touched (R14): on `/ar/le-projet/` at 390 two `span.ls` runs of a French statement read 20/32 (1.6) inside the
  project's statement column (`_projet.css`) — a PUB2 surface; AGAMI's registers in the mono (`_agami.css`) — PUB2's row.
- The reviewer's m6 (`fronte-halo` and the entrance's `varco-*` loops running at rest on the frontispieces and the login — the
  heads' and the entrance's own motion, pre-existing on the base) and m7 (the mono still fetched by the pages' own seats and the
  preload) — matrix items for CLOSING, not this lane's.

## 10. The improve round (label `v524-lib-improve`, 6 Nov 2026 01:10 → 02:10) — the reviewer's gate answered

`evidence/v524/lib/QA.md` (label `v524-lib-qa`, 00:13–00:55): FAIL, 6 blockers, 9 minors. Every blocker fixed, the cheap minors
taken, the rest recorded; nothing outside the tables touched (R14). Tool → decision → change for the round:

| Finding | Decision (the real tool behind it) | Change | Proof |
|---|---|---|---|
| **B1** the home 61 470 > 61 440: the shell grew 70 B with the light and the label net; `pages.css` bundles the shell | the audit's placement wins over the build round's «one home» abstraction — the shell is in EVERY page sheet, so a light only the grids draw does not belong there (V5.26 §8 read correctly: one primitive for one shared behaviour, placed with the pattern that has the behaviour); variant C of QA.md §7.2 measured | the three light rules → `_sec-mosaico.css` scoped `.mosaico .sez-tile::before`; `isolation: isolate` folded into `.sez-tile` (m5; 0 B); `font-feature-settings` out of the `.testa__label` net; `_sec-mosaico.css` re-recorded 1 229 → 1 355 (R4 f; deviation 4), the shell recorded at 2 382 | `pages.css` 11 302, the home **61 415 ≤ 61 440** (`test_frontispiece_v515_c.py` 93 passed); every route sheet under its ceiling (§6) |
| **B2** the raccordo never painted (`.sez` isolates; the protrusion under the next band's ground) | `figma-implement-motion`'s «validate one animation end to end» had been read as rects and `getAnimations()`; the reviewer's pixel proof is the end-to-end test. Fix B (the Director's): the span is the first child of the band it ENTERS, drawn from the seam down — robust for consecutive seams, inside the ceiling; fix A (a lifted section) passed the ceiling and broke two seams in a row | `_materia.css` `inset-block-start: 0`; the fixture's span moved into the entered strip (a process head: its rule at the content edge, where a 48 / 32 px line lands — a panel head's rule sits in its label's line, 7–9 px lower: the page lanes set `--sez-raccordo` for such a landing, §4 (c)); the twin addresses the entered band by its attributes, waits for `data-sec-state="in"`, asserts the node on the head rule (≤ 2 px) and READS THE PAINT (the line's column against the ground 12 px beside it); COMPONENT_PROVENANCE's row | `fx_raccordo-*_seam.png`: the line and its node on the rule; luminance 193 vs 235; 0.0 px off the rule at 1440 · 1024 · 390, fr and ar |
| **B3** the bookend behind the plate at 1024 and on the sheets | `ui-ux-pro-max`'s rule («noise behind the plate») applied to the right measure: the field's free span, not the viewport — a container query (the system's own device, `_formwork.css`) | `.protezione__campo { container-type: inline-size }`, `@container (max-width: 67.999rem) { .sez-fondale { display: none } }` in place of the 63.999 rem media; the twin's 1024 case; `protezione.html`'s contract comment | Parcours 1024: the sill 33 px, the bookend gone; the sheet 1440: the sill 16 px, no bookend; Parcours 1440: the bookend 1140–1332 beside the plate |
| **B4** the incastro inert (the band's own padding sank the first door 32 px under the seam) | the overlap the audit drew is the doors' arched tops OVER the photograph: the band's top padding has no role above the raised edge | `.sez[data-incastro] { padding-block-start: 0 }`; the twin asserts the first door ≥ 63 px over the band above | `fx_incastro-*.png`: the arches rising into the paper band; `doorOverAbove` 64 in every cell |
| **B5** the two new modules red and lint red | the tests say what the product does, exactly: `_rule` reads a rule OUTSIDE every at-rule block (a brace-matched stripper); the burn-down counts `font-size: clamp(` (a padding's clamp is not a type size); the unused name gone; the twin's entered band by its own attributes, `wait_for_function` for the phone trigger (no timeout raised), the reduced-motion loop ending on the raccordo page, one pixel assertion | `test_materia_v524_lib.py`, `test_materia_browser_v524_lib.py` (V5.20: the same invariants or stronger, each cited) | 61 + 14 passed; `ruff check` 0 |
| **B6** the home's hero line 4 px off the orientation seal's sill (the numeral role's 40 px leading grew the linea's first row) | the across numeral is a solo glyph whose line box IS the grid's first row: its leading is its size (36 px — the system's own idiom for solo numerals, as `.sez-numeral` and the linea had it); the role's 40 px leading serves numerals in flow (the filo, the down variant). The reviewer's substitution alone (`--t-numeral-lg` in the two calcs) would have left the row at 40 and put the route 4 px above the marks' foot — measured before deciding | `_linea-v2.css`: the across numeral `font-size: var(--t-numeral-lg); line-height: 1`, the route's inset and the carriage return on `--t-numeral-lg` | `home_*_orientation.png`: `lineBottom − sealBottom` 0.0 at 1440 and 1024, fr and ar; lane H's `test_the_hero_line_runs_down_into_the_orientation_seal_sill[fr/ar]` (§7) |
| m1 (+70 B shell), m5 (fold the isolation) | moot / taken with B1 | — | — |
| m3 (NOTES stale, §7–§8 unfilled, the fr pass only) | refreshed | §6–§8, §10; the headed session in both languages at three widths | — |
| m4 (the node's colour on the rule) | a placement note, not a rule change: the node stays `--accent-mark` (the arrival's mark); the pages land it beside the rule's start or on a structure line | §4 (c) | — |
| m2, m6, m7 (the base's reds; the heads' loops; the mono seats) | not this lane's — recorded for the steward / CLOSING / the matrix | §7, §9 | — |
| m8, m9 | by design, recorded | — | — |

**Deviations of this round from the reviewer's proposed fixes, each measured:** (i) B6 — `line-height: 1` on the across numeral
in addition to the two `calc()` substitutions (the row, not only the inset, had grown); (ii) B1 — `_sec-mosaico.css` lands at
1 355, not within 1 203 + 120: the scoping the review suggested was already in place in its 1 365 figure, every spelling measured
1 353–1 365, nothing removable (deviation 4) — re-recorded at the measure under R4 f; (iii) B2 — the fixture's entered strip
carries a PROCESS head so that the node lands on the head RULE within 2 px with the letter's 48 / 32 px line (the panel head's
rule is centred in its label's line, 7–9 px below the content edge; the Director's alternative «assert against the label's box»
would have read the head's line box, not its rule); a panel landing is a placement matter, §4 (c).

**Discipline.** `CHROMIUM_LOCK_A` taken 01:49:35 and released 01:51:58 (label `v524-lib-improve-eye`; slot B untouched; the
merge lock `DESIGN_V5_MERGE_LOCK` not mine, left as found); the lane server 8786 (`ile_v5_l5`) started for the headed session
and stopped at the lane's end; `test_ile_v524_lib` and `test_ile_v524_libb` one pytest each; `PYTHONIOENCODING=utf-8`;
`ILE_WHATSAPP_NUMBER` unset, no private value printed; every repository file LF (`read_bytes` / `write_bytes`); two identical builds,
the dist committed; nothing pushed, no tag, `main` untouched.
