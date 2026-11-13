# V5.24 lane PX — Imagery V2 · credits: the visible stock credits leave the product (labels v524-px-build, v524-px-improve)

Branch `v524-px` from design-v5 `4bafcfa0` (= tag `v522/p2`; worktree `C:/tmp/ile_wt/v524-px`). Binding: V5.24 §2–§3,
§23, §30 (2 Nov 2026), V5.25 (known defects, targeted checks, one gate), V5.26 §4 (tool → decision → implementation),
V5.20 (the strict test rule), the work order `C:/tmp/ile_v5_council/.work/v524-audit/director/FINAL_DELIVERY_V2.md`
§3.2 (this lane; R2 adopts `evidence/v524/IMAGERY_ATTRIBUTION.md` D1–D8 whole), SECTION_SYSTEM_V2 §8 (no person's name
copied into another document), §9.7 (ownership), §9.8 (preserved families: none touched). First lane in the merge order
(§0.5): the shared test modules and the two two-line slices are PX's so that every later merge leaves `design-v5` green.

- Database lane l4 (`ile_v5_l4`, already current — 0 unapplied migrations, the nine QA accounts present); pytest on
  `test_ile_v524_px` (non-browser) and `test_ile_v524_pxbr` (the browser twins) — one pytest per database (R12).
- Lane server 8792: `C:/tmp/ile_v5_council/.work/v524-px/run_8792.py` (the acceptance launcher copied with the tree,
  the database and the port changed: dev settings, `ILE_DESIGN_PREVIEW=1`, `ILE_REFERENCE_DATE=2026-10-03`, the nine
  personas). Stopped at the end of the lane. No `.env` in the worktree: no WhatsApp number anywhere in this lane's
  process or files.
- Chromium: the browser twins ran headless under slot B (`v524-px/b1_twins`, released); the stills and the crawl are
  headless probes and took no slot (R12). No headed session: an attribution change is a DOM question; the eye's check
  («no empty caption box», the frames unchanged) is made on the stills.
- Repository files LF (every edit through Python `read_bytes` / `write_bytes`; checked). `PYTHONIOENCODING=utf-8`.

## 0. The decision in one screen

The visitor saw, under or over every photograph of the public site, «Photo : *Name* / Pexels» (fr), «Foto: … / Pexels»
(it), «Photo: … / Pexels» (en), «صورة: … / Pexels» (ar) — 104 credits (26 slot frames × 4 languages) on the merged
tree, a 12 px line under the frame, 14 px in Arabic, a chip on the night grounds and the diptychs. Every one came from
ONE line, `templates/components/photo.html`'s `<figcaption class="foto__credit">`, fed by `apps/pages/imagery.py`'s
`Picture.credit`. Every photograph the product serves is Pexels License («Attribution is not required») or the owner's;
the retired Unsplash library renders nowhere; no CC BY asset exists → **nothing to replace, the credit leaves**, the
provenance stays internal (`PROVENANCE.json`, `IMAGE_LICENSES.md`, `ASSET_USAGE_MATRIX.md`, the figure's `data-slot`,
the development specimen board). No hidden attribute replaces it (nothing reads it; a name lives in one place, §8).
The curated-plate path (`cms.MediaAsset`, 0 publishable rows today) becomes licence-aware: a byline renders only when
the licence demands it. One production-facing test is the gate's «Pexels-visible-label check».

## 1. What the owner sees, where

Lane server 8792 (on `design-v5` once merged), every photographed page in fr, it, en and ar: the same frames, in the
same places, at the same sizes — **no line and no chip under or on any of them**. Nothing else moves: the frame's box
is the `<picture>` (explicit width and height, CLS 0 as before), the sections' rhythm is the grid's, not the caption's.
Measured on the lane server against the base 8780 (`logs/html_delta.txt`): 52 frames in fr + ar, every `<figcaption>`
gone (4→0 on the home, 5→0 on Parcours, 3→0 on Formation, 2→0 on Entreprises, Institutions, Universités, Projet
pilote, Le projet, 1→0 on Diplômes, Réseau, Contact, Vivre), **−75 … −100 B of HTML per frame** (−4 255 B over 34
pages; the pages without a stock frame — AGAMI, Fraudes, FAQ, Glossaire, Forum — byte-identical). Stills (§8): the four
gate pages at 1440 and 390, then every fr/ar page that carries a slot.

The development board `/__design-v5/specimens/imagery/` (never mounted in production) still draws its 11 frames through
the same tag — now without captions — and keeps its 11 data sheets («Pexels <id>», the AVIF ladders, the ceilings):
exactly the internal provenance the owner wants kept (gate item 7).

## 2. What changed (IMAGERY_ATTRIBUTION D1–D8; files owned per §3.2)

**D1 · `templates/components/photo.html`** — the `<figcaption class="foto__credit">…</figcaption>` deleted; the figure
keeps `<picture>`, `data-slot`, `data-reveal`, `data-grade`; no `data-credit` / `data-author`. The comment's caption
paragraph rewritten (no caption; licence; the record; `data-slot` the pointer; the curated plate's byline rule; the test
that holds it). The now-unused `{% load i18n %}` dropped.

**D2 · `apps/pages/imagery.py`** — `Picture.credit` and `credit=f"{rec['photographer']} / Pexels"` removed (the unused
`rec = record(slot)` with them); `record()` and `provenance()` unchanged (the tests read licence, author, page); the two
comments («its credit still shown», «the credit stays visible») and the module docstring corrected («No credit is
rendered (V5.24 §2); provenance is internal»).

**D3 · CSS** — none of PX's: the 14 + 2 `.foto__credit` rules are **dead selectors** until their owners delete them (§4).
PX changes no stylesheet: `main.css` and every route sheet are byte-identical to the base (§6).

**D4 · the curated-asset path, licence-aware** —
- `apps/cms/models.py` `MediaAsset.attribution_required` (property, no migration): `license == CC_BY` or
  `"attribution=required" in license_notes`. `is_publishable` unchanged — the credit stays *recorded*.
- `apps/forum/models.py` `ForumMedia.attribution_required`: a row drawn from the library follows its asset; a file
  uploaded on the row is the event's own material (no licence record, no byline); a third party's attribution-licensed
  file enters through the library, whose licence decides.
- `apps/pages/services.py` (the two two-line slices, lines 241 and 259): `Photo.attribution_required: bool = False`,
  set from `asset.attribution_required` in both `Photo(...)` of `photo_from_asset`.
- `apps/ecosystem/services.py` (the equivalent): `Photo.attribution_required: bool = False` on the frozen dataclass, set
  in both `Photo(...)` of `photo_for` (the ecosystem's `Photo` carries no credit field — the entrance partial reads
  `photo.credit` as empty there; the attribute is the contract's symmetry).
- `templates/pages/partials/_ingresso.html:77`: `{% if photo.credit and photo.attribution_required %} — Photo … {% endif %}`
  (the French no-break colon rule of v522-s2 untouched).
- `templates/news/detail.html:61`: the figcaption's condition and the byline's both take `and image.attribution_required`.
- The three other caption templates are other lanes' (§4, contract items): `pathways/detail.html:66` (PUB1),
  `forum/partials/hero.html:46` and `forum/partials/permanent_sections.html:57` (PUB2).

**D5 · documents (erratum, no history rewritten)** — `docs/IMAGE_LICENSES.md`: §1.3 «mai mostrata» paragraph; new §1.10
(D8's rule for an attribution-required image: never into the slot registry; a curated `MediaAsset` with `cc_by`, or
replaced through the pipeline); §3.1 and §3.4 «autore registrato, non mostrato» (the former wording dated); new §3.5
«V5.24 — i crediti visibili rimossi» (the decision, the verification, what changed, the test). `docs/design-v5/
ASSET_USAGE_MATRIX.md`: one erratum paragraph at the head of §11 (the rows' «credit shown / visible» describe the V5.22
state). Both documents hold no photographer's name (`test_v522_the_registers_hold_a_row_per_frame_and_no_person_s_name`
still green). The errata outside PX's two documents go to CLOSING and HOME (§4).

**D6 · the tests that asserted the credit** — every row of the audit's table applied under V5.20 (the four conditions:
the owner's decision V5.24 §2 cited in each docstring with FINAL_DELIVERY_V2.md §3.2 D6; the same invariant or a
stronger one; no skip; no timeout raised):

| Module | Before | After |
|---|---|---|
| `tests/compliance/test_imagery_v512.py` | `test_every_slot_is_licensed_and_credited` (the record) | renamed `…_and_its_author_recorded`, assertions unchanged, docstring |
| idem | `…keeps_its_credit`: `pic.credit.endswith(" / Pexels")` | `…_and_its_author_stays_recorded`: the record's author non-empty **and** `not hasattr(pic, "credit")` **and** the rendered tag has no `<figcaption` and no «Pexels» (stronger) |
| idem `:435` | `'<figcaption class="foto__credit">' in html` | `"<figcaption" not in html and "Pexels" not in html` |
| `tests/frontend/test_interior_w3_f1.py:108` | `figcaption.foto__credit … endswith("/ Pexels")` | `select_one("figcaption") is None and "Pexels" not in str(photo)` |
| idem `:349` | `count("<figure") == count("<figcaption")` | renamed `test_a_plate_is_captioned_a_stock_frame_is_not_…`: every `figure.figura` has a figcaption **and** no `figure[data-slot]` has one or names Pexels (the rule as it was + a new one); the module docstring |
| `tests/compliance/test_figure_caption.py` (7 routes) | the same count | the same two invariants; module docstring; **new** `test_a_curated_asset_s_byline_follows_its_licence` (Pexels, Unsplash, CC0, client, original → publishable and no byline; CC BY → byline; `other` + `attribution=required` → byline) |
| `apps/pages/tests/test_home.py:160-174`, `:716` | the same count; comment «credited» | the same two invariants (renamed `test_a_plate_is_captioned_and_a_stock_frame_is_not`); comment «no credit (V5.24 §2)» |
| `apps/ecosystem/tests/test_browser.py:103-105` | `figure` == `figcaption` locators | `figure.figura` == `figure.figura figcaption`, plus `figure[data-slot] figcaption` == 0 |
| `apps/pages/tests/test_browser.py:89-93` | comment | comment: «a curated plate without its caption is a defect; a stock frame carries none (V5.24 §2)»; assertions unchanged |
| `tests/frontend/test_sezioni_v522_s2.py:155-170` | the colon rule checked in `photo.html` and `_ingresso.html` | `_ingresso.html` only, plus the assertion that `photo.html`'s markup has no figcaption; the rendered `&nbsp;:` assertion unchanged |
| `tests/frontend/test_sezioni_browser_v522_s2.py:347-358` | read `.foto__credit` on the panorama fixture | renamed `test_the_plate_s_byline_…`: a CC BY `MediaAsset` (unsaved, built as `test_frontispiece_v515_c.py:385` builds its curated photograph) through `pages.services.photo_from_asset` → `_ingresso.html` in the library's bare page; the same invariant (French no-break space before the colon, none in it/en/ar) on the plate's byline, plus `figure[data-slot] figcaption, .foto__credit` count 0 |
| `apps/pages/tests/test_home_v522_h.py:441` | `"foto__credit" in frame` | `"<figcaption" not in frame`; docstring |
| `apps/ecosystem/tests/test_companies_page.py:218` | `"<figcaption>" in figure` | unchanged (the curated plate keeps its caption; its Unsplash byline is simply absent) |
| `tests/frontend/test_design_preview.py:1335` | dev index copy «(Pexels)» | unchanged (not a product surface) |

**D7 · NEW `tests/compliance/test_imagery_credits_v524.py`** (`@pytest.mark.compliance`) — (1) the SOURCES: no product
template (`templates/**`, `apps/*/templates/**`, `templates/dev/**` excluded) names `Pexels`, `Unsplash`, `Photo by`,
`pexels.com`, `unsplash.com`, `foto__credit`, `creditText` outside `{% comment %}` / `{# #}`; `photo.html`'s markup
has no figcaption, no «credit», no «author»; (2) the RENDERED public site: every route of `core.public_routes` in the
four languages — the ungated ones, the Phase 3 ones (`phase3_open`) and the legal ones (`legal_published`) at 200, the
others when they answer 200 — plus the 404 (through the site), the 429 and the 500 (through `core.views`): the visible
text (comments, scripts, styles, templates, noscript stripped, entities resolved) matches none of `\bPexels\b`,
`\bUnsplash\b`, `\bPhoto by\b`, `(?:Photo|Foto|صورة)\s*[:\u00a0]\s*.{0,80}/\s*(?:Pexels|Unsplash)`,
`pexels\.com|unsplash\.com`; no `<figcaption` inside any `figure[data-slot]`; no `alt`/`title`/`aria-label`/`content`
and no JSON-LD naming a stock source; (3) the RENDERED platform: the preview's four personas (built as
`test_design_preview.py::accounts` builds them, `force_login`) over `designpreview.live.PERSONA_PAGES` in fr and ar, and
an institution's and a university's organisation space (role + `Organisation` + OWNER `Membership`, as the acceptance
seed does) over the portal's pages — a page a fresh account cannot reach is skipped, the dashboards must render and the
walk must render ≥ 30 pages; (4) the REGISTRY: `not hasattr(picture, "credit")`; licence, author and page recorded for
every slot. The footer's «©» and the glossary's «Source» are outside every pattern by construction (F5).

**D8 · the rule for a future attribution-required asset** — written as `docs/IMAGE_LICENSES.md` §1.10 (and restated in
§3.5): never into the slot registry (`test_every_slot_is_licensed_and_its_author_recorded` requires the Pexels
License); only as a curated `MediaAsset` with `license=cc_by` (D4 draws its byline), or replaced by a Pexels/Unsplash
frame of the same subject through the existing pipeline with its three register rows.

## 3. Tool → decision → change (V5.26 §4; §3.2 Tools: the audit's crawler, headless Chromium for the stills)

| Tool | Decision | Change |
|---|---|---|
| The audit's crawler `crawl.py` + `analyse.py` (copied to `.work/v524-px/`, pointed at 8792; GET only, the nine personas through the preview's switch) | the surface list the production test must cover — the 46 public routes × 4 languages, the signed-in pages of the nine personas (113 platform-only paths, 0 photographs), the F5 false positives («©», the glossary's «Source») | D7's route set (`core.public_routes` + the error pages + `PERSONA_PAGES` + the organisation space) and its stock-only vocabulary; the re-run after the change is §7's figure |
| Headless Chromium (Playwright, `stills_px.py`, reduced motion, 1440 and 390, no slot) | «no empty caption box»: the `<figure>`'s children are `picture` only, the figure's box is the picture's — no `margin-block-start` orphaned under the frame, no chip plate left on the night grounds (the chip's plate was the caption's own background: gone with it) | nothing further to change: the frames' boxes are unchanged (the caption sat outside the `<picture>`), so no CSS correction is PX's; the dead `.foto__credit` rules are each owner's deletion (§4) |
| `impeccable`, `taste-skill`, the motion skills, 21st | **not used — by decision**: PX reopens no composition (R9; V5.25 §1), adds no component and no motion; the one visual question («does the frame's foot read clean without its line?») is answered by the stills | — |

## 4. Contract items — applied for other lanes / requested of other lanes

**Applied by PX from others' contracts:** none were due — TYPOGRAPHY_V2 §4.2's token names and BACKGROUND_MATERIAL_V2 §3's
attributes (R3's «raccordo») name no file of PX's. **PX's own contract offered to every lane:** `attribution_required`
(on `cms.MediaAsset`, `forum.ForumMedia`, `pages.services.Photo`, `ecosystem.services.Photo`) and the guard form
`{% if <asset>.credit and <asset>.attribution_required %}`.

**Requests (each lane applies in its own files; dead selectors and latent paths meanwhile):**

- **LIB** — delete the `.foto__credit` rules: `static/css/v5/_photo.css:34-40` (+ its comment line 34), `:42-44`,
  `:144-152` (the corner chip, comment included); `_fronte.css:566-568`, `:638-640`, `:717-722`, `:1014-1020`,
  `:1182-1184`, `:1269-1275`, `:1392-1400` (comment + rule); `_sec-strato.css:89-94`; `_compose.css:64-66`;
  `_sec-mappa.css:120`. Keep `base.css:26` (`figcaption` line-height) and `_pagina.css:363` (`.figura figcaption`): the
  curated plates. ≈ 2 371 B of source; every bundling route sheet can only shrink (re-measure gzip -9 against its ceiling).
- **PUB1** — `apps/ecosystem/static/ecosystem/_institutions.css:47-56` (the hemicycle chip); `templates/pathways/detail.html:66`:
  `{% if pathway.hero_image.credit and pathway.hero_image.attribution_required %} — … {% endif %}`.
- **HOME** — `apps/pages/static/pages/css/pages.css:710` `.pilota__quadro .foto__credit { z-index: 1; }`; the comments
  `templates/pages/home/_trust.html:15` («its credit in the corner») and `_ecosystem_frame.html:10` («the photograph's
  credit stays under the frame»).
- **PUB2** — `apps/cms/static/cms/_lessico-v2.css:376-383` `.vivere-panorama__quadro .foto__credit`;
  `templates/forum/partials/hero.html:46`: `{% if event.hero_image.credit and event.hero_image.attribution_required %}`;
  `templates/forum/partials/permanent_sections.html:57`: `{% if media.credit and media.attribution_required %}` (the
  property is on `ForumMedia`).
- **CLOSING** — the doc errata outside PX's two documents: `docs/design-v5/SECTION_SYSTEM_V2.md` §8 block (lines 203, 316,
  330, 793, 801, 875, 1774, 1892 superseded by V5.24 §2); `docs/design/DESIGN_SYSTEM_2026.md:2953-2958` («la sola
  didascalia del credito» → «nessuna didascalia»), `:4379-4384` (the caption contract is the curated plates'); the H/P2
  NOTES lines (`QA/v522/p2/NOTES.md:322`; one line «credits removed by v524 (V5.24 §2)» in each); the development sheet
  `static/css/dev/specimen-imagery.css:76` `.spi .foto__credit` (dead; no lane named — a cleanup candidate);
  `live_status.json` family «Imagery V2 · credits».
- **GATE** — `pytest tests/compliance/test_imagery_credits_v524.py -m compliance` listed in the gate's command file next to
  `test_public_pages.py` (V5.24 §30 «Pexels-visible-label check»).
- **Steward (R11)** — the family `v524-px` in `OWNERSHIP_V54.json`: `owns` = `templates/components/photo.html`,
  `apps/pages/imagery.py`, `templates/pages/partials/_ingresso.html`, `templates/news/detail.html`,
  `tests/compliance/test_imagery_v512.py`, `tests/compliance/test_figure_caption.py`,
  `tests/compliance/test_imagery_credits_v524.py`, `tests/frontend/test_interior_w3_f1.py`,
  `apps/pages/tests/test_home.py`, `apps/pages/tests/test_home_v522_h.py`, `apps/pages/tests/test_browser.py`,
  `apps/ecosystem/tests/test_browser.py`, `tests/frontend/test_sezioni_v522_s2.py`,
  `tests/frontend/test_sezioni_browser_v522_s2.py`, `docs/IMAGE_LICENSES.md`, `docs/design-v5/ASSET_USAGE_MATRIX.md`,
  `docs/design-v5/QA/v524/px/**`; slices: `apps/cms/models.py` (the `attribution_required` property),
  `apps/forum/models.py` (idem on `ForumMedia`), `apps/pages/services.py` (the `Photo` field and the two calls),
  `apps/ecosystem/services.py` (idem).

## 5. New user-facing strings

None: catalogue **+0 −0**. `msgid "Photo"` stays (the curated captions of `_ingresso.html`, `news/detail.html` and the
other lanes' three templates; `apps/forum/models.py:393`). No locked text touched; nothing machine-translated.

## 6. Budgets measured (gzip -9 on the built dist; before = base `4bafcfa0`, after = this branch)

`npm run build` twice with the installed packages — by the reviewer at 20:41 (`.work/v524-px-qa/logs/build{1,2}.log`,
`dist{1,2}.sha`: the 77-entry list's sha256 `57086b47…` both times) and again by the improve round at 21:10
(`.work/v524-px-improve/logs/`, the 47 sheets' list `ab624ac8…` both times): **two identical builds, `git status static/`
empty after each — the dist is byte-identical to HEAD and to `design-v5`'s `4bafcfa0`** (every file under
`static/css/dist` compared byte for byte: 0 differences). PX touches no stylesheet (D3): every sheet measures as the base's.

| Sheet | lane | base | ceiling |
|---|---|---|---|
| `main.css` | **32 716** | 32 716 | ≤ 32 716 (R4 c, the ratchet) |
| `pages/css/pages.css` · `hero.css` · `fronte.css` · `interior.css` | 11 306 · 10 899 · 6 141 · 8 827 | same | home ≤ 61 440 total; interior 11 264 |
| `core/sezioni.css` · `core/reveal.css` | 11 308 · 3 526 | same | — |
| `ecosystem/{ecosystem,companies,institutions,pilot}.css` | 4 977 · 8 701 · 8 381 · 9 508 | same | pilot 9 728 |
| `pathways/{pathways,index,diplomas,training,sheet}.css` | 4 716 · 10 117 · 8 895 · 8 788 · 9 701 | same | index 10 240 |
| `cms/lettura.css` · `cms/faq.css` · `cms/lessico.css` | 6 512 · 1 935 · 2 384 | same | 9 216 · 2 048 · 2 560 |
| `pages/css/rete.css` · `agami.css` · `frodi.css` · `forum/forum.css` | 1 817 · 1 760 · 1 200 · 7 369 | same | 2 048 · 2 048 · 1 536 · 8 192 |

HTML: −75 … −100 B per frame (`.work/v524-px/logs/html_delta.txt`: 34 fr/ar pages, −4 255 B); on the lane server `/fr/`
129 850 B, `/ar/parcours/` 82 362 B, `/fr/entreprises/` 77 924 B — 0 figcaptions, 0 «Pexels», 0 `foto__credit`. The pages
without a slot frame (AGAMI, Fraudes, FAQ, Glossaire, Forum) render as on the base but for the port in the alternate
links. JS 0, images 0, fonts 0. Catalogue +0 −0 (`git diff -- locale` empty).

## 7. Tests run (counts)

R12: one pytest per database; `-p no:randomly -p no:cacheprovider -q`; CI's placeholders, the `.env` not read, the private
sentinel table read in-process by the guard and never printed.

The builder's runs (`.work/v524-px/logs/`, `test_ile_v524_px` / `test_ile_v524_pxbr`): `t1_targeted` the changed modules,
`t2_new` the new module **5 passed**, `t3_interior` **93 passed**, the three browser twins **63 passed in 571 s** under
slot B (`b1_twins`). An orphaned pytest of the force-closed build turn (PID 28344, 20:21:18 → 20:51:11, «4 failed, 921
passed») ran an INTERMEDIATE `test_interior_w3_f1.py` whose `assert figures, path` failed on the four interior pages
without a figure; that line was removed before `t3_interior`; the final module is what the gate runs.

The reviewer's gate (`evidence/v524/px/QA.md` §1, label v524-px-qa):
- gate item 1 — the six modules `-m "not browser"` on `test_ile_v524_pxqa`: **257 passed in 837.92 s** (0 failed, 0 error, 0 skipped; 20:42:33 → 20:56:35);
- the three browser twins under `CHROMIUM_LOCK_A` on `test_ile_v524_pxqabr`: **63 passed in 640.28 s**;
- the extra guards around the change (`test_home_v522_h.py`, the twins' non-browser parts, `test_locked_content.py`,
  `test_public_pages.py`, `test_confidential_material.py` with `ILE_CONFIDENTIAL_SENTINELS`, `test_no_personal_data_in_repository.py`,
  `test_companies_page.py`, `apps/forum/tests`, `apps/news/tests`, `apps/cms/tests`): **451 passed, 63 deselected in 311.99 s**
  (0 failed, 0 skipped — the confidential-material guard ran in-process with the private table);
- `ruff check .` → All checks passed · `manage.py check` → 0 issues · `makemigrations --check --dry-run` → No changes detected.

The improve round (§10; the six gate modules + `apps/news/tests`, one pytest on `test_ile_v524_px`, 21:12:38 → 21:22:54,
`.work/v524-px-improve/logs/t1_gate.log`): **327 passed in 612.38 s**; `ruff check` on the touched modules 0. The browser twins were not re-run
(their modules are untouched by the round; 63 passed on this tree at 20:53 — V5.25 §7, targeted tests only).

The rendered crawl of the lane server (the audit's `crawl.py` + `analyse.py`, pointed at 8792; GET only; the nine
personas entered through the preview's switch; `.work/v524-px/{pages.json, summary.json, analyse.txt, logs/crawl.log}`):
**2 156 HTML pages, all 200** — 184 public (46 routes × 4 languages) + 1 972 signed-in (220 per person/company persona,
216 per organisation persona). **`<figcaption>`: 0 · slot credits (`.foto__credit`): 0 · attribute hits (alt / title /
aria-label / content / href naming pexels | unsplash | photo by): 0 · script / JSON-LD hits: 0 · HTML comment hits: 0 ·
Unsplash-library files served: none.** Visible-text hits by kind: the footer's copyright line «© 2026 AGAMI — Dialogo
Giuridico Interculturale APS» × 1 684 and the glossary term pages' legal-source field «المصدر» × 57 — exactly the two
false positives of IMAGERY_ATTRIBUTION F5, outside the test's patterns by construction; nothing else. The audit's figure
before the change on the same tree: 104 credits on 52 public pages (26 slots × 4 languages).

## 8. Stills (`C:/tmp/ile_v5_council/evidence/v524/px/`)

Headless Chromium (Playwright, `.work/v524-px/stills_px.py --all`, reduced motion emulated so masks and B/W grades are at
rest, device scale 1, no lock slot — R12), on the lane server 8792 after the change: the gate's four pages
(`/fr/entreprises/`, `/fr/institutions/`, `/ar/parcours/`, `/fr/le-projet/`) and then every fr + ar page that carries a
slot, at **1440 and 390** — **124 files**: one element still per `figure[data-slot]` (`<lang>_<width>_<page>__<slot>.png`,
100 frames) and one full-page still per page at 1440 (`<lang>_1440_<page>__page.png`, 24 pages). Measures
(`.work/v524-px/stills_px.json`): **100 frames, 0 with a `<figcaption>`, 0 with a `.foto__credit`, every figure's children
exactly `[picture]`** (no empty caption box: the figure's box is the picture's); **48 page measures: 0 stray
`.foto__credit`, 0 caption inside a slot figure, 0 visible «Pexels | Unsplash | Photo by»**. Four element shots timed
out, as in the audit: `network.table` on `/fr/reseau/` and `/ar/reseau/` at both widths (the night head's frame behind the
map's panel) — its state is on the page stills `fr_1440_reseau__page.png` / `ar_1440_reseau__page.png` and in the page
measure (0 captions). Read against the audit's before-stills (`evidence/v524/pexels/<lang>_1440_<page>__<slot>.png`):
the calliper frame of Entreprises ends at its picture (no 12 px line), the hemicycle's night ground has no chip in its
top-end corner, the Arabic Parcours entrance has no 14 px caption at its end edge, Le projet's night frontispiece has
no line under its frame — the frames themselves at the same sizes and places.

## 9. Not done, by design or out of scope (R14: post-acceptance candidates, not fixed here)

- ~~`templates/news/detail.html:61` prints «Photo : » with a plain space~~ — APPLIED in the improve round (§10, m2): the
  line is PX's by §3.2 and the review named it.
- The retired Unsplash library (73 files, ≈ 6.9 MB under `static/img/photos/`, copied into `MEDIA_ROOT` by the seed)
  renders nowhere (F6); D4 makes a future curation harmless. Deleting it is a later cleanup, not a V5.24 defect.
- The owner's door photograph's written rights record (IMAGE_LICENSES §7.1, D22): a go-live checklist item (F7), not a
  change of this lane; recorded for §6 of the work order.
- The `.foto__credit` rules in the other lanes' sheets (dead until each owner deletes them, §4) — by §9.7, not PX's.

## 10. Improve round (label v524-px-improve, 5 Nov 2026 21:05 → 21:30) — the reviewer's findings (QA.md §9) answered

The reviewer's targeted gate PASSED on items 1–7 (QA.md §0); its two blockers were completeness items of this deliverable
and its four minors are answered here. No product composition is reopened (R9, V5.25 §1).

- **B1 — §6 and §7 filled** from QA.md §7 and §1 (above).
- **B2 — one commit on `v524-px`** with the 21 files (19 modified, `tests/compliance/test_imagery_credits_v524.py`, this
  NOTES; LF confirmed on every one), the lane's register-form message citing V5.24 §2 and FINAL_DELIVERY_V2.md §3.2 D1–D8
  with this round's changes. The steward's R11/R13 steps follow (the family `v524-px` in `OWNERSHIP_V54.json` with §4's
  `owns` globs and slices, `FAMILY_ID` extended, `check_ownership v524-px 4bafcfa0 --head <lane head>`, the merge).
- **m1 — the «neither» figure, APPLIED** (V5.20, a stronger invariant, cited in the three docstrings):
  `tests/compliance/test_figure_caption.py`, `tests/frontend/test_interior_w3_f1.py`, `apps/pages/tests/test_home.py` —
  `if "figura" in attrs:` → `if "data-slot=" not in attrs:` in the three loops. The first rule now holds on EVERY figure
  that is not a stock frame, the exact complement of the second: together they cover every figure as the old count did
  (and more: a slot frame may no longer hide a caption). Safe by construction — the product templates hold seven
  `<figure>` tags: `components/photo.html` (`data-slot`), five `figura` plates each with an unconditional `<figcaption>`
  (`_ingresso.html:72`, `news/detail.html:59` — conditional there, on a route no module walks and none renders today —,
  `pathways/detail.html:64`, `forum/partials/hero.html:48`, `permanent_sections.html:51`) and the enquiries blockquote
  figure (`enquiries/company_needs.html:28`, a page none of the three modules walks). Verified by the three modules in the
  round's run (§7) and in the DOM of the headed session (`uncaptioned_non_slot_figures` 0 in all 8 cells).
- **m2 — the news byline's colon, APPLIED:** `templates/news/detail.html:61` takes `_ingresso.html:77`'s form —
  `{% get_current_language as credit_lang %}{% translate "Photo" %}{% if credit_lang == "fr" %}&nbsp;:{% else %}:{% endif %}`
  — v522-s2's rule (lane H's QA_ROUND3 m7: the no-break space before the colon in French only) on the second byline PX
  owns (the line is PX's by §3.2; the round's one template change). `tests/frontend/test_sezioni_v522_s2.py`'s loop now
  reads both templates (stronger; cited). Rendered through the engine with a CC BY asset's fields: fr «Photo&nbsp;: X», it
  «Foto: X», en «Photo: X», ar «صورة: X»; a Pexels-licensed asset draws no byline; the template compiles. The lane database
  holds 0 articles and 0 CC BY assets, so no page renders the byline today (the news app answers 404 on the preview). The
  same plain-space colon stands in `pathways/detail.html:66` and `forum/partials/hero.html:46` — PUB1's and PUB2's lines
  (they take the contract guard, §4); the no-break form is offered with it.
- **m3 — axe `target-size` after the 21-Tab pass** (`.approdo__link.sez-stretch` on `/fr/entreprises/` 390,
  `.site-footer__email` on `/ar/institutions/` 390): outside PX's change (the approdo band is P1/P2's, the footer a preserved
  family), not reproduced at rest on base or lane, 0 violations in the changed sections in all 12 cells — **recorded for
  the ONE matrix's axe cells (R14); no PX action.**
- **m4 — the dead `.foto__credit` rules** (14 + 2, ≈ 2 371 B source): §4 lists every file:line per owner; each deletes and
  re-measures its bundling sheet gzip -9 against its ceiling (only down); `static/css/dev/specimen-imagery.css:76` to CLOSING.
  **Recorded; no PX action** (§9.7).

**§10 targets.** The lane changes no composition, motion, interaction or type on any page; the four gate pages keep the
scores of their lanes' merges (Entreprises, Institutions and Parcours DL54-183/184, Le projet DL54-186; V5.25 §5, R9) —
no dimension is moved by this lane, and the one it touches, imagery, loses its stock-catalogue signal (V5.24 §3: «must NOT
look like an image catalogue or stock-photo demo»). No design work is PX's here; any would be new scope (R14).

**Tool → decision → change (V5.26 §4), this round.** Playwright headed Chromium (`headed_improve.py`, chromium-1234,
`CHROMIUM_LOCK_A` 21:14:03 → 21:14:52, label `v524-px-improve/h1_headed`, released) → the four gate pages at 1440 and
390 read clean after the round's edits on the final tree → no further change (the stills below). The audit's crawler was
not re-run: the round changes no rendered public page (0 CC BY assets). `impeccable`, `taste-skill`, the motion skills and
21st: not used, by decision (as §3 — no composition, component or motion is touched).

**Headed check (R12, under a slot; lane server 8792 on `ile_v5_l4`, started 21:10 for the round and stopped at its end).**
`/fr/entreprises/`, `/ar/parcours/`, `/fr/le-projet/`, `/fr/institutions/` × 1440×900 and 390×844 — 8 cells, **22
frames: 0 `<figcaption>`, 0 `.foto__credit`, every figure's children exactly `[picture]`, `::after` none; page level: 0
slot captions, 0 uncaptioned non-slot figures, 0 visible «Pexels | Unsplash | Photo by», overflow 0, one `h1`, `dir`
rtl on `/ar/`; the first Tab sets `html[data-input="key"]`; 0 console errors, 0 page errors.** Stills (30 files):
`C:/tmp/ile_v5_council/evidence/v524/px/improve/<lang>_<width>_<page>__<slot>.png` (22 frames) and `…__viewport.png`
(8); measures `.work/v524-px-improve/headed.json`.

**Post-acceptance candidates (R14), unchanged from §9 plus:** m3 (the matrix's axe cells); the PUB1/PUB2 bylines' colon
(their owners, with the contract guard).
