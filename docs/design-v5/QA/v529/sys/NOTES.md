# V5.29 stream SYS — the shared visual system (label `v529-sys-build`, branch `v524-sys`)

Base: lane HOME's head `560021e5` (design-v5 `e6e6c34b` already inside it), HOME's work kept. Lane server 8793, database
lane l9; pytest on `test_ile_v529_sys`. Directive: V5_29_FINAL_PREMIUM_VISUAL_REMEDIATION.md (§6 order: the system first).

## §0 The decision (one critique, one decision)

The critique: headless stills of Homepage, FAQ, Parcours, Entreprises, Institutions, Fraudes and /ar/ at 1440 and 390
(`C:/tmp/ile_v5_council/evidence/v529/sys/base_*.png`), read with impeccable's laws (SKILL.md, critique.md,
typography.md, color-and-contrast.md) and one ui-ux-pro-max design-system query («government legal institutional premium
trust navy warm neutral», variance 3, motion 2, density 4).

What makes the pages read RAW · BLACK · BOLD is the system, not the families: one near-black ink (#15222a, 14.6 : 1) for
every title and most body text, a 600 weight on every title, label, keyword and primary call, and the plates as flat white
boxes with a 1 px inset line. impeccable: «never #000, tint every neutral toward the brand hue», «hierarchy through scale +
weight contrast», «cards are the lazy answer»; ui-ux-pro-max: a navy-ink foreground with a slate secondary, subtle
200–250 ms hover, «sharp shadows if any».

**Decision.** Host Grotesk and Readex Pro are kept (the weights they ship, 400–700 variable, carry the result). The system
is re-inked and lightened: the ink moves to a deep institutional ink tinted toward the night (#222f3d, 12.3 : 1 on the
page), the secondary to a refined slate (#4e5b68), the muted to #56626e, all named by eight semantic text roles in
`v5/tokens.css` and mapped onto the existing aliases; the weight map drops one step (display, titles, labels 500; strong
600), hierarchy carried by size, tracking and colour; the plate becomes a layered material (a warm face, a lit top arris, a
night-tinted two-layer shadow) inherited by every page; «la protezione» becomes one compact trust band. No new family, no
new string.

## §1 Units — tool → decision → change

0. impeccable (critique, typography, color-and-contrast) + ui-ux-pro-max (one design-system query) → the system, not the
   families, makes the pages heavy → §0. (design-critique / design-handoff are not installed; not used.)
1. impeccable color-and-contrast («no #000, tint toward the brand», measured pairs) → re-ink, roles → `v5/tokens.css`:
   `--p-inchiostro-900` #15222a → #222f3d (12.27 : 1 on carta-50), -600 → #4e5b68 (6.27), -500 → #56626e (5.62); roles
   `--text-primary / -secondary / -muted` (the same primitives as `--text-1/2/3` and the `--ink` aliases, so every sheet
   inherits), `--text-legal` (the warm ash ink `--p-cenere-900`, 11.59), `--text-accent` (the route's bronze, 6.40). The
   inverse, interactive and status roles are the system's own `--text-on-night-1`, `--accent-text`, `--notice-*-text`:
   not doubled, because main.css's ratchet (32 716 on the tests' zlib measure) cannot carry seven synonyms. The pairs test
   holds the new roles on every paper (532 pairs); DS 2026 §5 rows recomputed. No sheet wrote a literal black text colour
   (grep). Paid in main.css: four unread declarations retired (`--accent-2`, `--accent-glow`, `--he-step`, the aliases'
   `--t-numeral-size`).
2. impeccable typography («hierarchy through scale + weight contrast») → one step down → `--w-title/-display/-label` 500,
   `--w-strong` 600 (never 700); the library's literal 600s on the tokens; the unused side-stripe `.sez-statement` retired.
   Host Grotesk and Readex Pro kept.
3. ui-ux-pro-max («architectural light, not a gradient behind everything») → the stone and the brand wash lit by one soft
   radial light from the band's head on the reading side (`--sez-luce`, RTL twin) in `_sezioni.css`; pietra keeps its grid,
   carta viva / velatura / raccordo / incastro unchanged (LIB's measured recipes); paper plain, night its grain.
4. impeccable («cards are the lazy answer») + emil-design-eng (depth by layered shadow, never animated) → the plate primitive
   `.sez-plate` is a material: a face lit from above into the sheet's tone, the contact shadow plus a long low ambient in the
   night's colour (pre-painted layer, SH-4 kept); `strato__titolo` the quiet line (ui step, 500, the slate), «Non.» and the
   body the strong one; `he__body` at a 48 rem measure, its first line (the fold's peek) in the primary ink, the rest in the
   slate. Inherited by `strato__lastre`, `sez-plate`, `home-trust__grid` / `integrita__tavola`, `indice__palco`, the
   mosaico, approdo and tracciato plates.
5. impeccable (icon audit: importance, container, colour role, optical size) → `.sez-tile`: the vault in the laguna's first
   light (no grey box), the glyph ink by importance (`--tile-ink`: slate at rest, laguna on the lg door/panel tile and under
   its owner's hover / focus / selection), one optical stroke at every scale (lg 1.25, sm 1.75 on the 24 grid).
6. impeccable distill + quieter → «la protezione» one compact trust band (components/sezioni/protezione.html,
   `v5/_sec-lastre.css`): the seal (24 in 44 × 54) at the reading edge beside the locked title (label role, legal ink) and
   body (first sentence at the body step, the rest at the small step, two columns from 64 rem), the call at the far end, a
   30 % laguna-wash tint, the 2 px ink top rule, a plain plate, the strip rhythm; height 216 px at 1440 (fr); on a phone
   the seal, title, body and call stack on one start (542 px at 390).
   V5.24's sill and far shield retired. «Optional expandable detail» refused: the locked text is legally required whole and
   visible (SECTION_SYSTEM_V2 §1 rule 7). Verified: home 1440 fr + ar, home 390 fr, Parcours 1440 + 390.

## §2 The pages that keep «la protezione», and why

- `/xx/` (home S6): a back-office section (`SectionKey.ANTIFRAUD`, gate phase 3) the editors can switch off; it closes the
  trust band, the first page a newcomer meets. Kept, compact.
- `/xx/parcours/`: the Espace Personnes hub — the locked text's prescribed place (Impl. p.10 §3.8.1, CONTENT_SOURCE_MAP).
- `/xx/parcours/<route>/` (`#avertissements`): the route's own warnings join it — the reader is choosing a route.
- `/xx/formation/`, `/xx/diplomes-et-titres/`: Espace Personnes pages where paid «training + visa» and «recognition»
  offers are the frauds the text names; removing it would also put two paper bands together on the diplomas page.
- Nowhere else draws it (the fraud page has its own idiom, `_frodi.css`). So no page lost it: every use is justified, each
  is now compact.

## §3 Contract items (not this stream's files)

- **PUB2 (FAQ):** the icon primitive is ready — `.sez-tile` sm / md / lg (20 / 24 / 32 glyphs, optical strokes) and the
  `--tile-ink` hook; PUB2 maps the semantic set (documents, access, pathway, company, institution, university, legal source,
  security, fraud, account, support, deadlines, eligibility) and may set `--tile-ink` per role. The explorer's rules stay
  in `_sec-indice.css` (it imports `_sec-indice-base.css`): `faq.css` keeps importing `_sec-indice.css`. `_lessico-v2.css`
  writes a literal 600 → `var(--w-title)`.
- **PUB1:** `_training.css`, `_diplomas.css` literal 600 → `var(--w-title)`; `_persone-v2.css` `.persone-protezione
  .protezione { margin-inline: 0 }` is now redundant (the band spans its field) and can go; the Institutions Italy–Morocco
  background is PUB1's.
- **PLAT:** `_platform.css` (4×) and `_frame.css` (3×) literal 600 → `var(--w-title)` / `var(--w-strong)`; the console
  inherits the ink roles and the weight map.
- **Others:** `forum/_forum.css` (2×), `pages/css/_projet.css` literal 600 → tokens (their owners).

## §4 Budgets (gzip -9; nothing raised)

| | HOME 560021e5 | now | ceiling |
|---|---|---|---|
| main.css (the tests' zlib -9) | 32 695 | 32 714 | 32 716 |
| **home total** | **61 732** | **61 328** | **61 440 — closed** |
| pages.css | 11 680 | 11 237 | 12 288 |
| hero.css | 10 838 | 10 849 | 11 264 |
| `_sezioni.css` (alone) | 2 343 | 2 333 | 2 382 |
| `_sec-strato.css` (alone) | 1 557 | 654 | 1 638 → **717** (lowered) |
| `_sec-lastre.css` (alone, new) | — | 1 262 | 1 331 (new sheet) |
| `_sec-indice.css` (alone) | 1 404 | 524 | 1 434 → **614** (lowered) |
| `_sec-indice-base.css` (alone, new) | — | 1 207 | 1 229 (new sheet) |
| glossary / term / living totals | 54 153 | 54 165 | 54 272 |
| AGAMI total | 55 856 | 56 019 | 56 320 |

How the home closed (V5.29 compaction, in order): the protection compacted (sill, far shield, container query gone); the
plates' and the index's sheets split so the home bundles what it draws (`_sec-lastre.css`, `_sec-indice-base.css`;
every other importer keeps the whole sheet, same order); rules made dead or unused retired (`.sez-statement`, `.sez__grid`,
`.sez-squadre` moved to a partial of its own, `v5/_squadre.css`, imported by AGAMI's sheet only; four unread
declarations). **Ceilings re-recorded: none raised** (two lowered, two new).

Post-acceptance candidates (R14): main.css carries ≈ 1 KB gzip of legacy `:root` declarations that a later `:root`
redeclares (static/css/tokens.css ≈ 690 B, v2/tokens.css ≈ 350 B; tool `.work/v529-sys/tools/dupe_root.py`) — CLOSING,
with test_design_docs' legacy-token readers; `.fronte__name` keeps 700 (FINAL_DELIVERY_V2 §3.3's letter); the hero
description's far side stays open (the composition HOME kept).

## §5 Tests and the merge (one pytest per database; headless probes, no slot)

design-v5 merged twice (`e6e6c34b` at the start, already inside HOME's head; `0ad88a42` with lane AR at the end, clean;
AR ships 0 CSS, the rebuild is identical). After the last merge, on `test_ile_v529_sys_b`: the token, typography, library,
pattern-sheet, bundle, pipeline, design-docs, chapter-mark, static-asset, V4-token and legacy-shim modules **1 069 passed**;
the protection's browser tests (LIB's, rewritten; lane S's locked-text test) and LIB's browser module **17 passed**. On
`test_ile_v529_sys`: the home's modules (`test_home.py`, `test_home_v522_h.py`, `test_home_v524_home.py`), the
frontispiece's budgets (home total included), orientation, P1 pages, interior, content pages, locked split: **479 passed,
8 failed — every failure is lane AR's merge, not this stream's**: the eight assert French on `/ar/` where AR's V5.27
renderings now put Arabic (the hero promise, the pilot's title, the orientation route, the recipients' sentence, «French on
an Arabic page says so», the newsletter's refusal, the form pages' band); four of them were re-run on a clean checkout of
`design-v5` (`0ad88a42`) and fail there identically. A fifth AR consequence is the lane S browser test
`test_the_protection_s_french_title_is_one_left_to_right_box_on_the_body_s_edge`: the title is now Arabic on `/ar/` (it fails
on `design-v5` too). **Steward / AR items** — not changed here (no test loosened by this stream).

Tests changed under V5.20 citing V5.29 (each the same or a stronger invariant): `test_typography_v2.py` (the weight map,
never 700), `test_v5_tokens.py` (the new roles added to the pairs), `test_materia_v524_lib.py` (the protection as one
compact band, the tile's two inks on its vault, the plates read in `_sec-lastre.css`, the two new sheets in LIB_SHEETS),
`test_materia_browser_v524_lib.py` (the band at 1440, 1024 and 390, fr and ar), `test_sezioni_v522_s.py` (two ceilings
lowered, two new), `test_sezioni_v522_s2.py` (the index rules read across its two sheets), `test_home_v522_h.py` (the home's
imports, the plain plate).

The lane server 8793 is stopped. Stills: `C:/tmp/ile_v5_council/evidence/v529/sys/` (`base_*` before, `u5_*`, `prot3_*`,
`final_prot_ar_*`, `hebody_*`, `trust_*` after).

## §6 The one fix round (label `v529-sys-fix`)

design-v5 re-merged first (`abeb04a8` + `0ad88a42`, clean, 0 CSS): the three AR home failures are the steward's amendments.
Blocker — `test_home_browser_v524_home.py::test_the_seams_stand_where_the_director_placed_them` asserted V5.24's retired
sill and bookend: amended under V5.20 citing V5.29 §4 (no sill, no bookend, pietra and its grid's mask direction kept, the
band ≤ 240 px at 1440 fr; every other seam kept). The module on `test_ile_v529_sys_b` (`DJANGO_ALLOW_ASYNC_UNSAFE=true`,
as lane HOME ran it): **8 passed**, fr and ar.
Minor — the tile glyph on stretched-link plates stayed slate (the tile is the link's sibling): `_sezioni.css` gains
`.sez-plate:has(.sez-stretch:is(:hover, :focus-visible)) { --tile-ink: var(--accent-text) }` (§1.5 now true). Two builds
identical; main.css 32 714 / 32 716, home 61 328 / 61 440, every page total under its ceiling; budget/sheet modules **402
passed**; headed Chrome under slot A (`tools/tileink.py`): FAQ fr + ar, three plates each, rest slate, focus and hover laguna.
Post-acceptance candidates (R14, not fixed): `.protezione__testo` columns break mid-sentence (CLOSING); `.he-station__label`
literal near-black → `var(--text-secondary)` (CLOSING); the FAQ question flush at 390 (PUB2); axe
landmark-complementary-is-top-level on the protection's `<aside>` inside `<main>` (CLOSING; markup predates SYS).
Lane server 8793 stopped at the round's end.
