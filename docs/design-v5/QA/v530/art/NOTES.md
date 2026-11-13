# V5.30 — stream A «PUBLIC ART DIRECTION / DESIGN SYSTEM» — NOTES (label v530-art-build)

Branch `v530-art` from `v530` (1420e1c6), worktree `C:/tmp/ile_wt/v530-art`, lane server 8795 on `ile_v5_l3`. Directive:
`directives/V5_30_FINAL_ART_DIRECTION_PLATFORM_PASS.md` (PUBLIC 1–7) and the orchestrator's note of 7 Nov 21:45 (the V5.29
baseline matrix's blocker 1, assigned to this stream). Evidence (outside the repository): `evidence/v530/art/`.

## §0 The decision

The public site did not have too many motifs in any one place; it had the SAME motifs as the default of every place. The
cure is in the shared composition system, not on twenty pages: the library's primitives get a QUIET DEFAULT and the
signature stays only where a template asks for it deliberately.

1. **The seal** (`components/sezioni/sigillo.html`, `v5/_sigillo.css`): a quiet niche TILE by default (the seat's width
   square, the card's 8 px corner, no sill); the ARCH seat on its sill (`arch=True` → `sigillo--arco`) only where its sill
   becomes a route — the home's orientation origin, the Parcours route head — and on the brand's two bookends — the home's
   reserved door, the Forum's hemicycle. Every interior head, «la protezione», the FAQ answer, the pilot's sequence head and
   the Vivre head now carry the tile.
2. **The frontispiece** (`v5/_fronte.css`): the twelve-column hairline grid left every head's ground; the offset hairline
   frame behind the head photograph left (its print stays); the page's drawing stands only on a head that COMPOSES with it
   (`data-compose`: the route spine, the network ring, the contact plate, the project's arch, the skyline, the notice) —
   never behind a photograph.
3. **The closing band** (`components/sezioni/approdo.html`, `ecosystem/partials/approdo.html`, `v5/_sec-strato.css`): the
   bookend — the head's drawing repeated at the page's foot — left the library (markup and rules).
4. **«Le porte»** (`v5/_sec-mosaico.css`) and **the pilot's two doors** (`ecosystem/_pilot.css`): material night/raised
   plates on the card's corner, no longer arched doors on a sill. The hero's doors are the brand's door.
5. **The home** — LEGAL-TECH · INSTITUTIONAL · PREMIUM · MODERN: hero (the brand moment: doors + route) → orientation (the
   route continues; the background portico of three arches left) → pathways (tabbed reveal) → pilot (immersive
   photography) → trust (material plates on the photo ground) → protection (the compact band, tile seal) → **the
   cooperation moment** (the ecosystem: a plain photograph split — the colophon at the reading edge, the frame inside its
   columns — over the Italy + Morocco field, the arch frame and its drawn doorway gone) → reserved (the door bookend).
6. **The brand** (`v5/chrome.css`, `v5/motion.css`): the lock-up 40/21 from 80 rem (was 36/19; the verbatim 38/20 ratio;
   the layered mark follows) — the header 64 px, one row, the key's CSS-only turn unchanged.
7. **The container roles** (`v5/tokens.css` §3.6) and **the footer** on the letterhead's shell; **Entreprises' form**: the
   band head no longer stands over the wide form (the matrix's blocker 1).
8. **«L'intesa»** generalised into ONE primitive with variants and placed on the home and Réseau (§5).

## §1 The motif inventory (1440, fr; headless, reduced motion; `evidence/v530/art/audit/inventory-{before,after}-1440.json`)

Families per section: A arch / door form · S the arch seal (before) or tile (after) · L route line / thread / seam ·
C outlined circle / ring · G drafting grid · R raccordo · D drawing (inline SVG ≥ 96 px). «→» = after this stream.

| Page | Section | Before | After |
|---|---|---|---|
| Home | hero | A doors · L route · D stage | kept — the brand moment |
| Home | orientation | A portico ×3 + arch seal · L route · D | A the route's origin seal only (its sill is the route) · L route |
| Home | pathways | — (tabs) | — (tabs) |
| Home | pilot | L gold thread · R seam · photographs | kept — immersive photography |
| Home | trust | material plates on the photo ground | kept |
| Home | protection | A arch seal · L sill · G pietra | tile · G pietra (the material, a texture) |
| Home | ecosystem | A arched frame + drawn doorway + sill · L connector | photograph in a plain frame · the intesa field (one motif) |
| Home | reserved | A arch seal (night) | kept — the door bookend |
| Le projet | head | A brand arch frame · C ring · D | kept — compose «arch», the page's one signature |
| Le projet | En bref (racconto) | A · L · D the system figure | kept — a process figure |
| Le projet | panorama · porte | photograph · A four arched doors | photograph · material plates |
| Projet pilote | head | D mission arcs behind the diptych · A seal | photographs only |
| Projet pilote | sequence | A arch seal · L route | tile · L route (the journey's signature) |
| Projet pilote | participer · approdo | A two arched doors + sill · A/C/D bookend | plates · tiles only |
| Parcours | head | A arch seal · L spine · C rings | kept — compose «route», the journey's signature |
| Parcours | board · protection | L lanes · R · A arch seal · G | L lanes · R · tile · G |
| Pathway sheet | head · body | A seal · L curve · D / A seal · L rail · C arc · G · R · D | tile / tile · L rail · C the authorities' arc · G · R |
| Entreprises | head | A seal · L skyline line · C node · D · grid · frame | tile · the skyline (compose: the page's signature) |
| Entreprises | demarche · form · approdo | L measured curve · — · A/D bookend | L curve (the process) · the band head · tiles only |
| Institutions | head · aula · approdo | A seal · D civic · grid · frame / photo / D bookend + intesa | tile · photograph / photo / the intesa (stronger) |
| Collaboration | head | A seal · D colonnade · faint intesa · D hemicycle note | tile · the intesa (dominant, stronger) · the note's small seat drawing |
| Universités · Formation | head | A seal · D learning · grid · frame | tile · photograph |
| Formation | protection · boussole | A seal · G / C compass | tile · G / C compass (the orientation's one moment) |
| Réseau | head · approdo | C ring · L · D (interactive map) / A/C/D bookend | kept / the intesa |
| FAQ · Glossaire · Vivre | head | L/D route, learning, territory drawings · A seal (Vivre) | plain heads · tile |
| Fraudes | head · frodi | A seal / G · L | tile / G · L |
| Contact | head · porte | D coordinate plate · C · photo / A three arched doors | kept (compose «contact») / plates |
| Forum | head · sections | A hemicycle + arch seal / A · L · C ring · R · D bookend | kept / the bookend gone |

## §2 The tool lines (PROBLEM → TOOL → DECISION → IMPLEMENTATION; real names only)

- Every section defaults to the architecture vocabulary («same template») → **impeccable** (`reference/critique.md`:
  composition and rhythm, «layout sameness»; applied as the directive's per-page logo test on 17 pages) → fix the library's
  DEFAULTS, keep each signature where a page asks for it → the tile seal, the head's grid / frame / non-composed motif gone,
  the bookend retired, the door plates (§0 1–4).
- What alternates with the geometry → **21st.dev MCP** (`mcp__21st__search`: split media — «Split Content Section» 28310,
  «Editorial Collage Hero» 19074; bento — «Feature Section with Bento Grid» 1327; sticky storytelling — «Scroll 01» 18041)
  → ONE direction, «an image-led split over an atmospheric material field»; no component pasted (the library's campata,
  mosaico and racconto already carry split, bento and sticky) → the home's cooperation moment (a plain photograph split
  over «l'intesa» atmosfera), the doors as material plates.
- The brand key's timing → **figma-use-motion** (the skill's phase method: start · mid · settle) → KEPT: the 16°
  preparation, the 364° turn and the settle already are the three phases; no timing change, shell.js untouched → only the
  lock-up's optical size (40/21), the layered mark following.

## §3 The per-page question — «If I remove the logo, is it still another page of the same architecture-themed template?»

| Page | Before | After |
|---|---|---|
| Home | yes — five arches stacked (doors, route seal, portico, arched frame, reserved door) | **changed** — one door (the hero) and its bookend; route, tabs, photographs, plates, a photograph on the Italy–Morocco field |
| Le projet | yes — arch frame, arch diagram, four arched doors | **changed** — the doors are plates; the head's arch stays as the project's one signature |
| Projet pilote | yes | **changed** — no motif behind the diptych, tile, plates, no bookend |
| Parcours | partly | **changed** — the route head kept (the journey), the protection's arch gone |
| Pathway sheet | yes | **changed** — plain head, tile; the steps' rail and the authorities' arc are content |
| Entreprises | yes | **changed** — tile, no grid / frame / bookend; the skyline stays as the page's signature |
| Institutions | yes | **changed** — a clean photographic head; the Italy–Morocco band |
| Collaboration (Institutions) | yes — colonnade + seal + faint flags | **changed** — the Italy + Morocco field is the head's one motif |
| Universités · Formation | yes | **changed** — clean photographic heads |
| Réseau | no — the ring is the content | **kept** head; the closing band changed (the intesa) |
| FAQ · Glossaire · Vivre · Fraudes | yes — a drawing and an arch seal on every head | **changed** — plain heads, tiles |
| Contact | no — the coordinate plate is the content | **kept** head; the doors are plates |
| Forum | no — the hemicycle is the Forum | **kept** head; the bookend gone |

## §4 The container roles (`static/css/v5/tokens.css` §3.6)

| Role | Token | Width | Reason / where |
|---|---|---|---|
| shell-wide | `--shell-wide` (= `--site-shell-max`) | the column + 10 rem, capped by the gutters | the letterhead AND the colophon share one inner edge (the footer now stands on it: `.site-footer { --container: var(--shell-wide) }`) |
| content-standard | `--content-wide` | 1176 · 1320 · 1440 px | every section's column; compositions and image `sizes` are measured on it |
| content-narrow | `--content-narrow` (= `--measure-body`) | ≈ 70 ch | the reading and legal measure; applied to `_lettura.css`'s four literal 36 rem widths |
| form-wide | `--form-wide` | the shell | the premium form and its band (`v5/_formwork.css`, unchanged) |
| media-wide | — (documented) | full bleed or inside the column | an image band is a deliberate full bleed (the panorama) or a split's frame inside the column — never an accidental third width |

Applied: the footer (shell, compact: a 40 px band, the long navigation in two columns from 64 rem, its brand on the header's
edge — measured 40 px at 1280/1440, 200 px at 1920); the header keeps the shell. Entreprises' form (blocker 1): from
64 rem the side panel is the band's head across the band, static (the chapter's head beside the request's panel), the
formwork under it on the shell with its own sticky night side — nothing stands over the form. The V1 helpers no template
writes (`.zones` and its 176–220 px rail — a third structural width —, `.split`, `.measure`) left `layout.css`. Reading and
legal measures untouched.

## §5 «L'intesa» — the include and its variants

```django
{% include "ecosystem/partials/intesa.html" with id="<unique prefix>" variant="campo|atmosfera|pannello" night=<True|False> only %}
```

- The band must be a stacking context (every `.sez` is; a head wraps itself in `<div class="intesa-campo">`); the layer is
  its first child, aria-hidden, without text, pointer-transparent.
- `variant`: **campo** (default — a head's or a closing band's ground: Italy's fields at the reading edge, Morocco's field
  and pentagram at the far corner, meeting around the words) · **atmosfera** (a section's broad field: larger, Italy
  softened at both ends, Morocco's centre near the far lower corner, the band's photograph over its near half) ·
  **pannello** (inside one contained panel or card: the fields measured on the panel, clipped by its corner — the variant
  for AGAMI's relationship panel, stream B). `night=True`: screened into a night ground.
- Sheets: the page's sheet imports `static/css/v5/_intesa.css` (from an app sheet `@import url("../css/v5/_intesa.css");`;
  from `pages/css/` `../../css/v5/_intesa.css`) and, for atmosfera only, `v5/_intesa-atmosfera.css` after it.
- Flags NEVER mirrored: no transform on either drawing or any ancestor; in Arabic only the placement follows the reading
  edge. Reduced motion: still. Phones: lighter fields, the pentagram hidden (never a line through a sentence).
- Placed: the Institutions collaboration head (campo, existing include, now stronger), the Institutions «Pour aller plus
  loin» (campo, existing), the home's cooperation moment (atmosfera, new), Réseau's «Pour aller plus loin» (campo, new).
  Stream B places the fourth on AGAMI.

## §6 Budgets (gzip -9 of the built dist)

- `main.css` **32 084** (≤ the 32 105 ratchet, ≤ 32 716 hard): the lock-up, the footer's shell and two columns and two role
  tokens paid by the dead V1 helpers (`.zones`, `.split`, `.measure`). `shell.js` **4 648** (untouched).
- Down: fronte.css 5 995 → 5 839 · interior.css 7 842 → 7 731 · lettura 6 543 → 6 530 · sezioni 11 806 → 11 729 ·
  companies 8 480 → 8 389 · pilot 9 701 → 9 583 · forum 7 849 → ≈ 7 790 · index 10 452 → 10 354 · sheet 10 007 → 9 921 ·
  training 9 079 → 8 981 · diplomas 9 225 → 9 126; every page type 70–300 B lighter except the two below.
- **Ceilings re-recorded** (V5.20, citing V5.30 §7 — the Italy + Morocco primitive the owner asked for, after paying with
  what the change made dead: the ecosystem's arch rules, its sill's light and connector, the portico's drawing, the
  bookend): `pages/css/pages.css` 11 239 → **11 626**; `pages/css/rete.css` 1 761 → **2 384**;
  `ecosystem/institutions.css` 9 007 → **9 041**; page totals home 60 708 → **61 074**, Réseau 54 218 → **54 553**;
  `ecosystem/intesa.css` 712 → 871 (no ceiling, a comment updated).

## §7 Tests

- Restated under V5.20 citing V5.30 (same or stronger invariant): `tests/frontend/test_brand_shell_v529.py::
  test_the_lockup_is_one_step_up_from_80rem_in_both_states` (40/21, ratio, height held); `apps/pages/tests/
  test_home_v522_h.py::test_the_promoter_stands_beside_the_working_table_under_the_arch` and `::test_the_ecosystem_
  photograph_rises_in_its_arch_and_its_doorway_is_drawn` (the arch asserted ABSENT, the plain frame, the field present);
  `apps/pages/tests/test_home_browser_v522_h.py::test_final_the_doorway_is_painted_as_one_line_from_its_foot` and round 1's
  M1 e (no doorway at any time, the card's corner); the ceilings of §6.
- New: `tests/frontend/test_intesa_browser_v530.py` — one primitive on four surfaces with its variant, never mirrored in fr
  and ar at 1440 · 1024 · 390, still under reduced motion; the home's words ≥ 4.5 : 1 on the field.
- Docs held: DESIGN_SYSTEM_2026 §2 weights (regen script), §3 `--cooperation` (now consumed) and `--container-rail`
  (reserve), §7 the removed helpers annotated.
