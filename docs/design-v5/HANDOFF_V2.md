# HANDOFF V2 — the design system after V5.24 / V5.29 (lane CLOSING, 7 November 2026)

What a developer or designer needs to build a new section of Italy Legal Entry without regressing it. Concise by
design (V5.24 §26); the long forms are `SECTION_SYSTEM_V2.md` (with its V5.24 errata), `FINAL_DELIVERY_V2.md` (the
work order and rulings R1–R14), `DESIGN_SYSTEM_2026.md` (the sheet inventory, Italian) and the lanes' notes under
`QA/v524/<lane>/NOTES.md`. Every name below exists in the tree as written.

## 1. Tools used — real provenance (V5.27 §6; `evidence/v524/TOOLS_AVAILABILITY.md`)

| Requested name | Installed? | Real tool used | Lanes that used it (tool → decision → change in their NOTES) |
|---|---|---|---|
| figma-use-motion | yes (`figma@claude-plugins-official` 2.2.157; its Figma MCP not authenticated) | skills `figma:figma-use-motion`, `figma:figma-implement-motion` — the method applied to the product's own tokens | T, LIB, HOME, PUB1, PUB2 |
| design-critique | **no** (no such plugin in any configured marketplace) | `impeccable` (user skill: critique, audit, typography, typeset), `taste-skill`, `frontend-design:frontend-design` | T, PX, LIB, HOME, PUB1, PUB2, PLAT, AR |
| design-handoff | **no** | this file, `COMPONENT_PROVENANCE.md`, the lanes' NOTES, the decision log | CLOSING |
| ux ui max github | yes (`ui-ux-pro-max@ui-ux-pro-max-skill`) | skills `ui-ux-pro-max:ui-ux-pro-max`, `:design-system`, `:ui-styling` | T, LIB, HOME, PUB1, PUB2, PLAT, AR |
| — | yes (user skills) | `improve-animations`, `find-animation-opportunities`, `animate`, `emil-design-eng` | T, LIB, PUB1, PUB2 (motion surveys and the four-question gate) |
| — | yes (MCP) | `21st.dev` (`mcp__21st__search`) — research only, no 21st component in the product (R9) | T, PX, HOME, PUB1, PUB2, PLAT |
| — | yes | Chromium through Playwright (CDP rule-usage coverage, A/B computed styles, probes) | PX, PUB2, AR, CLOSING |

«design-critique» and «design-handoff» were never used: they do not exist here.

## 2. The section and its attributes (the library, `static/css/v5/_sezioni.css`, `_sec-*.css`)

- A V2 section is `<section class="sez …" data-sec="<pattern>" data-ground="<kind>" data-rhythm="band|moment">`.
  Patterns: `campata`, `tracciato`, `racconto`, `panorama`, `mosaico`, `linea`, `mappa`, `filo`, `passaggio`,
  `strato`, `indice` (+ «la boussole», «la protezione»). Markup in `templates/components/sezioni/**`.
- **Grounds** (`data-ground`): `paper`, `stone`, `pietra` (one kind with stone for adjacency; never touching it),
  `brand`, `night`, `photo`. Two grounds of one kind never touch.
- **Material** (`static/css/v5/_materia.css`, page-only, never `main.css`): `data-luce="origine"` (carta viva),
  `data-sfuma="stone|paper|brand|night"` (velatura), `data-incastro` (the overlap).
- **Seams**: «il raccordo» `.sez-raccordo` (`aria-hidden="true"`, `data-verb="draw-y"`, `--sez-raccordo`,
  `.sez-raccordo--risale`, `.sez-raccordo--notte`), the FIRST child of the band it enters; its x is the page parameter
  `--raccordo-x` (read with a fallback, never declared by a sheet: a route sheet sets `inset-inline-start`).
- **Faces**: `.sez-plate` (+ `.sez-stretch`, the whole plate the link's target), `.sez-tile` (`--sm`, `--lg`, the niche
  face), `.sez-disc`, `.sigillo` (the arch seat, `sigillo--body`). The trust band «la protezione» is ONE compact band
  (`.protezione__campo`, V5.29 §4), never dominant, removed where not justified.
- **Runtime** (`static/js/src/rise.js`): `data-sec-state="wait|in"` written once per section below the fold;
  `data-sec-js="indice|mappa|flow|spia|racconto"` loads the interactive module on demand. Nothing is held in view at
  load, under reduced motion, under `html.rm`, from the keyboard (`html[data-input="key"]`), without script, in print.

## 3. Motion

- Tokens only (`tokens.css`): `--motion-fast` 120 · `--motion-standard` 200 · `--motion-emphasized` 320 ·
  `--motion-slow` 480 · `--motion-draw` 900 · `--motion-route-light` 1 200 · `--motion-stagger` 60 ms; easings
  `--ease-enter`, `--ease-exit`, `--ease-layout`, `--ease-sine`, `--ease-turn`. No new duration or curve.
- Verbs (`data-verb`, SECTION_SYSTEM_V2 §5.1): `draw`, `draw-y`, `mask`, `ink`, `light`, … — one signature per
  section, neighbours differ; every animation ends `finished`, nothing loops.
- **No fade-up default** (CLOSING): `translateY + opacity` is never a section's motion; `rise.js` no longer moves a
  page without a V2 section (legal, CMS reading, news, partners, questionnaire) nor any chapter head; it survives only
  on the rows of plain lists inside V2 pages. The two form pages' `reveal-mark` and the portal's `data-rise` stay.
- The brand key turns once (reveal, hover, keyboard focus), never under reduced motion — in the stylesheet since
  CLOSING (V5.29 09:41 item 1): `static/css/v5/chrome.css` §1, `@keyframes brand-key` played while the latch
  `--lock-turn` is on (`@property` on the layered mark `.lock-sig`; on at once, off `--motion-key` after the pointer
  or the focus left; a style query), fill `backwards` — one whole turn at a time; no script (`shell.js` ≤ 4 700 B).

## 4. Typography (R1, TYPOGRAPHY_V2, V5.29)

- Host Grotesk (Latin, 400–700), **Readex Pro** (Arabic, 400–700), ILE Mono on one seat
  (`code, kbd, pre, .t-ref, .ctx__ref, .ws-case__ref, .error-page__ref, .db-ref, .reg-ref`).
- **Twelve steps** (`--t-display`, `--t-title-1`, `--t-title-2`, `--t-band`, `--t-entry`, `--t-lead`, `--t-body`,
  `--t-ui`, `--t-small`, `--t-label`, `--t-caption`, `--t-field` + `-lh`); weights 400 reads · 500 acts · 600 intitles ·
  700 emphasis; roles `.t-label` and `.t-numeral`; the phone step-up (nothing under 14 px); text on the semantic ink
  roles, never pure black; hierarchy by size + weight + colour, not bold.
- Guard: `tests/frontend/test_typography_v2.py` — a new clamp, literal size, mono outside its seat, descendant-form
  Arabic rule or eyebrow fails; the closed register `TYPOGRAPHY_EXCEPTIONS` lists the decided residues and only shrinks.

## 5. Icons (SECTION_SYSTEM_V2 §4)

Tiers T1 seal (arch seat) · T2 tile · T2a disc · T3 utility · T4 status ring · T5 identity. One hand: 1.5 px drawn
(the sprite's strokes are non-scaling; nothing thinner — `test_icons.py`); colour from the context, gold from a budget;
each icon semantic, never repeated as decoration (V5.29 §18).

## 6. Arabic (R7′, V5.27)

Every Arabic type rule in the subject form `.x:lang(ar)`; the C-UI locked texts in provisional professional Arabic
(`apps/cms/locked_renderings.py`, flagged internally); a C-SUBST-FR text in French with its caption `.locked-caption`
on its own page (`SOURCE_ROUTES`) and its pointer line elsewhere; the team's acknowledgement of the notice identified
the same way on its own forms (`DERIVED_ROUTES`); C-OFFICIAL names kept. Unintended French on `/ar/` = 0
(`tests/i18n/test_arabic_completeness.py`; the burn-down table is closed and deleted).

## 7. Budgets and ratchets (gzip -9; only down)

`main.css` and every per-sheet / per-page ceiling are recorded at their measure by CLOSING (the tests named in
`QA/v524/closing/NOTES.md` §4 and §11): `main.css` 32 105 B under the hard 32 716 (611 B of headroom), `shell.js`
4 648 B under its restored 4 700; page-type letters: home ≤ 61 440, landings / interior / pathways ≤ 56 320, reading
pages and the Forum ≤ 54 272; JS at or under today's (`rise.js` 1 286); fonts per TYPOGRAPHY_V2 §4.7. A lane that adds
a rule to a sheet `main.css` imports removes at least as many bytes.

## 8. No regression to chapter layouts

A new public section is a V2 section of the library on a ground of the six kinds, never a `chapter` with a head on a
fifth column. `_chapter_head.html` and the `.chapter*` rules stay only for the legacy templates that still include
them (the questionnaire, news, community, consents, partners, the forum's gated partials, the preserved forms'
`.chapter--area`); no new template includes them.
