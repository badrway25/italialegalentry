# V5.30 · stream B — AGAMI / brand / content assets (lane v530-agami-build) — NOTES

Branch `v530-agami` from v530 1420e1c6. Scope: the AGAMI page (/xx/agami/) from verified material, the promoter's own
image assets, their registration, the page's tests. Not touched: header, footer, the library, other pages, the platform.

## 1 · Source pass (once) — details in PROVENANCE.md

| Material | Decision |
|---|---|
| Official logo, framed form (AGAMI project, `foto/logo-agami2.png`, 2 172 px) | selected → head's composed seat |
| Official logo, round seal (AGAMI project, `core/static/core/img/brand/`, lossless) | selected → identification plate |
| The website's header / footer lockups and seal | compared only (lower-resolution renderings of the same mark) |
| 12 portraits of named professionals | skipped — third parties' personal data |
| 8 round-table photographs | skipped — identifiable people and legible name cards in every frame; no face-free crop of quality |
| 1 video; the project's ILE flyer and logo; the website's stock and people photographs | skipped |
| AGAMI's tagline and motto, each in its four published versions (agamieuromed.org) | used word for word (catalogue); no team translation |
| Role facts (promoter of ILE and of the Forum, legal dialogue Italy – Morocco, since 2011) | ILE's tracked copy (`p2.forum.who.body`, `faq_who`, the page description) |

No photograph remains: the logo is the page's one image (V5.13 Q5: a strong institutional composition over an
irrelevant image). No person named, no fact, figure, partnership or event added; the Q9 block unchanged.

## 2 · Research / critique (one pass)

- PROBLEM the page read as another page of the architecture template (a drawn temple three times: head motif, identity
  plate, bookend) and showed nothing authentic of AGAMI → TOOL impeccable (`~/.claude/skills/impeccable/reference/critique.md`,
  the design-review half: the sameness test, hierarchy, missed opportunities; its deterministic CLI is not installed offline,
  not run) → DECISION the official logo as the head's real image, AGAMI's own published words as the lead and the
  relationship's voice, one dominant language per band, every temple retired → IMPLEMENTATION `templates/pages/agami.html`,
  `pages/partials/agami/_insegna.html` · `_marchio.html` · `_in_breve.html`, `_agami.css`.
- PROBLEM which identity pattern without photographs → TOOL 21st.dev MCP (`mcp__21st__search` «institutional about
  organisation hero with logo plate and key facts sidebar», one query) → DECISION keep the split «statement + media figure»
  (redrob-labs «Hero Section», adapted); reject trust avatars, client-logo marquees and stats pills (SaaS clichés, gate G6, no
  invented figures) → IMPLEMENTATION the head's composed seat and the «En bref» fact panel (Django SSR, ILE tokens, RTL; no
  component code used).

## 3 · Composition (one dominant motif per band)

- **Head «l'insegna»** (paper): label + folio seal, the name in two weights (kept), AGAMI's published tagline as the lead;
  the official logo on its white plate in the composed seat (≤ 34 rem, the page's one LCP image). The seat composes the head,
  so the ground's drawing stands down (as on every composed head). Phone: the logo under the words, full width.
- **A «l'identità»** (stone): «En bref», the role panel on the raised plate (masked from the reading edge), beside the
  promoter's prescribed text and the FAQ disclosure (both unchanged). No drawing.
- **K «la targa»** (night): the identification plate, now headed by the official seal (decorative, lazy); every Q9 field as
  before.
- **«l'approdo»** (stone): «Entre l'Italie et le Maroc», AGAMI's published motto (primary ink: ≥ 8.7 : 1 on the ground's
  darkest pixel), the ways on, on the Italy + Morocco ground — `ecosystem/partials/intesa.html` included **exactly as it is
  today** (CSS: `_agami.css` imports `ecosystem/_intesa.css`); stream A generalises the primitive: **the merge steward
  re-checks this include and import against A's primitive**. No drawn bookend.
- RTL: placement mirrors (the seat to the far side, the Italy fields to the reading edge); the logo, the seal and the flags
  never mirror. The project's name isolated (`bdi`) in the panel so its ™ stays at its end.

## 4 · Assets and registration

`tools/build_derivatives.py --marks --originals <the AGAMI project>` (no grade, never cropped or upscaled, AVIF 4:4:4 +
WebP, alpha kept, EXIF/XMP/ICC out) → `static/brand/agami/` (framed 480–1 600 px ≤ 60 KB; seal 176–353 px ≤ 30 KB) +
`PROVENANCE.json`; registered in `apps/pages/imagery.py` (`MARKS`, `mark()`, apart from the Pexels `SLOTS`, whose stock
invariants do not describe the promoter's own marks). Alt text: fr source + professional it / en / ar; the seal `alt=""`.

## 5 · Budgets

main.css 32 105 (unchanged) · shell.js 4 648 (unchanged) · no new JS module.
**Ceilings re-recorded** (V5.20 citing V5.30 §8, `tests/frontend/test_frontispiece_v515_c.py`): `pages/css/agami.css`
1 778 → **2 015** and the page total «interior (promoter)» 54 235 → **54 472** — the Italy + Morocco ground (709 B alone)
joined the route sheet; the retired colonnade, its light and sill and the corner brackets paid about 470 B of it first.
Dead files removed: `pages/partials/agami/_colonnato.html`, `static/css/v5/_squadre.css` (drawn by AGAMI's plate only).
Left for the integration (stream A's sheet): `[data-compose="name"] .fronte__motif { opacity }` in `v5/_fronte.css` is now
unreachable on screen (the AGAMI head is the only name head and its seat stands the motif down).

## 6 · Tests

New `tests/compliance/test_agami_assets_v530.py` (35): the Q9 block exactly the owner's and no other identifier (4 langs);
no EXIF/XMP/ICC/GPS in any AGAMI file nor its container (WebP chunks, AVIF item and colour boxes); every file listed, both
formats, ceilings, never upscaled, never cropped or mirrored; only the two logo forms from their two sources; no
portrait- or round-table-shaped name in `static/`, no template into the project's folders; the page drawing the marks, the
verified role panel, AGAMI's tagline and motto verbatim, the intesa behind the ways on.
Restated under V5.20 citing V5.30 §8 (same or stronger invariant): `test_interior_v522::test_the_promoter_page_identity_and_plate`
(the masked plate holds the role panel; no drawing in the band), `test_pages_browser_v522_p2::test_the_identity_plate_keeps_its_box_when_the_question_opens`
(was «the portico keeps its scale»), `::test_agami_s_identity_band_plays_its_signature_in_view_at_load` (the mask alone; the
old «mirrored in Arabic» becomes «nothing of AGAMI's is mirrored»).

**Targeted runs, once, on the final head `89c345e4`** (8 Nov 2026; test database `test_ile_v530_agami`) — 277 passed, 0 failed,
0 skipped:
- `tests/compliance/test_agami_assets_v530.py` (35), `apps/pages/tests/test_interior_v522.py` (37),
  `tests/frontend/test_frontispiece_v515_c.py` (93, the re-recorded ceilings), `tests/compliance/test_imagery_v512.py` (39),
  `tests/compliance/test_imagery_credits_v524.py` (5), `apps/pages/tests/test_institutional.py` (45) → 254 passed;
- Chromium (headless): `tests/frontend/test_pages_browser_v522_p2.py -k "identity_plate or agami or v2_disclosure"` (the two
  restated browser tests, AGAMI's disclosure rows) → 6 passed; `tests/frontend/test_imagery_v522_m.py` → 17 passed.

**Headed check of the final head** (Chromium 151, slot A, lane 8796 on `ile_v5_l4`, stopped since; stills and
`headed_check.json` in `C:/tmp/ile_v5_council/evidence/v530/agami/final_89c345e4/`; the stills beside that folder are of earlier
heads): `/fr/agami/` and `/ar/agami/` at 1440 · 1024 · 390 —
- horizontal overflow 0, one h1, 0 console errors, 0 failed requests, 0 tracebacks in the server's log; the logo, the seal and
  the Italy + Morocco ground never mirrored (`dir="rtl"` on the Arabic page, the ground's fields in the same left-to-right order);
- axe (wcag2a/aa, 2.1) on `main`: **0 violations** in all six cells; its one «incomplete» rule is colour contrast (the tool cannot
  read gradient and pseudo-element grounds), so the band on the new ground is measured directly: worst 8.78 : 1 (title, fr at
  1024), the motto's worst 8.81 : 1 (the same cell; `contrast_relation_band.txt` beside the stills);
- reduced motion (fr + ar, 1440): 0 animations running in `main`;
- keyboard (fr + ar, 1440): 7 stops in `main`, each with its ring (a tile's ring is on its plate — the earlier report's
  `ring: false` read the stretched link, whose own outline is off by design); the promoter's question opens with Enter.

## 7 · Files (for the steward's slice)

Whole: `templates/pages/partials/agami/{_insegna,_marchio,_in_breve}.html`, `static/brand/agami/**`,
`tests/compliance/test_agami_assets_v530.py`, `docs/design-v5/QA/v530/agami/{NOTES,PROVENANCE}.md`.
Slices: `templates/pages/agami.html`, `apps/pages/static/pages/css/_agami.css` (+ dist `pages/css/agami.css`),
`apps/pages/views.py` (agami view: the marks), `apps/pages/imagery.py` (MARKS), `tools/build_derivatives.py` (--marks),
`locale/*/LC_MESSAGES/django.{po,mo}` (7 msgids), the three restated tests, the two re-recorded ceilings.
Removed: `templates/pages/partials/agami/_colonnato.html`, `static/css/v5/_squadre.css`.
