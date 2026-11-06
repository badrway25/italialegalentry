# Lane PX — imagery attribution — the reviewer's targeted gate, round 2 on the committed head (label v524-px-qa, 5 November 2026, 21:27 → 21:47)

Branch `v524-px`, worktree `C:/tmp/ile_wt/v524-px`, **head `2031bcb134f4943033a7ca8a1bd14ac34ac35b0e`** (one commit over `design-v5` HEAD
`4bafcfa0` = tag `v522/p2`; 21 files, 823 insertions, 57 deletions; working tree clean). This round re-runs the whole gate of
FINAL_DELIVERY_V2.md §3.2 «Gate (reviewer, targeted)», items 1–7, on the committed tree after the builder's improve round
(label v524-px-improve: B1 NOTES §6–§7 filled, B2 the commit, m1 the plate rule on every non-slot figure, m2 the news byline's
no-break colon) — plus the harness's headed inspection (reduced motion, keyboard, axe on the changed sections, Arabic at the
affected widths) and the budgets on the built dist. No six-dimension re-scoring (the lane changes no composition — R9, V5.25 §5).
Round 1 (20:41 → 21:02, on the then-uncommitted tree) is preserved verbatim at `QA_round1_20h41_uncommitted-tree.md` beside this
file; the NOTES' citations «QA.md §1 / §7 / §9» refer to that round's sections, which this file keeps in the same order.

Machine discipline (R12): lane server **8792** on `ile_v5_l4` (the builder's launcher `.work/v524-px/run_8792.py`, started 21:28 by
the reviewer on the committed tree — 0 unapplied migrations on l4, `manage.py check` 0 — and stopped at the end of this round);
pytest on **`test_ile_v524_px`** (the task's; the six gate modules) and
**`test_ile_v524_pxbr`** (the three browser twins, then the extra guards once the twins released it); the browser twins under **`CHROMIUM_LOCK_A`** (label `v524-px-qa2/b1_twins`,
21:28:52 → 21:38:22, released), the headed inspection under **`CHROMIUM_LOCK_B`** (label `v524-px-qa2/h1_headed`, 21:29:40 → 21:33:20, released);
the crawl and the HTML comparisons took no slot (headless probes). `PYTHONIOENCODING=utf-8`; the `.env` not read
(`ILE_READ_ENV_FILE=0`); `ILE_WHATSAPP_NUMBER` unset; the private sentinel table read in-process by the guard, never printed.
Scripts, logs and measures: `C:/tmp/ile_v5_council/.work/v524-px-qa2/` (`run.sh`, `browser_session.sh`, `headed_session.sh`,
`headed_px.py` + `headed.json` + `summarise_headed.py`, `crawl.py` + `analyse.py` + `pages.json` + `summary.json` + `analyse.txt`,
`dist1.sha`, `dist2.sha`, `gzip_measures.txt`, `logs/`). Stills: `C:/tmp/ile_v5_council/evidence/v524/px/qa2/` (120 files).

## 0. Verdict

**PASS on every gate item; no blocker.** The product change holds on the committed head exactly as it held on the tree of round 1:
60 frames inspected headed in 24 cells, 0 captions, 0 credits, every `<figure>`'s children exactly `[picture]`, every `<picture>`
box identical to the base's in all 30 lane/base pairs at 1440 and 390 in fr and ar; the crawl of 2 156 pages clean; the targeted
suites green (257 + 63 + 505 passed); two identical builds, the dist byte-identical to `design-v5`'s,
`main.css` 32 716 B and every route sheet at the base's figure (no CSS touched); locked copy and both contact channels unchanged;
the 21 files LF. Round 1's two blockers are closed (B1 the NOTES §6–§7 filled with the figures; B2 the one commit `2031bcb1`),
its minors m1 and m2 are applied as strictly stronger invariants (V5.20) and verified here, m3 and m4 stay recorded (R14). Two
new minors recorded below (m5, m6), neither a defect of the product. **Ready for the steward's R11/R13 steps.**

## 1. Gate item 1 — the targeted modules

Command (R12, one pytest per database; `-p no:randomly -p no:cacheprovider -q`; `logs/g1_gate.log`):

```
pytest tests/compliance/test_imagery_v512.py tests/compliance/test_imagery_credits_v524.py tests/compliance/test_figure_caption.py
       tests/frontend/test_interior_w3_f1.py tests/frontend/test_sezioni_v522_s2.py apps/pages/tests/test_home.py -m "not browser"
```

Result on `test_ile_v524_px`: **257 passed in 739.22 s (12:19), 0 failed, 0 error, 0 skipped** (21:29:34 → 21:41:56). Round 1 on the same modules (then on `test_ile_v524_pxqa`): 257 passed
in 837.92 s; the builder's improve-round run (the six + `apps/news/tests`): 327 passed in 612.38 s.

The three browser twins under `CHROMIUM_LOCK_A` on `test_ile_v524_pxbr` (`apps/ecosystem/tests/test_browser.py
apps/pages/tests/test_browser.py tests/frontend/test_sezioni_browser_v522_s2.py -m browser`; `logs/b1_twins.log`, `.lock`):
**63 passed in 566.98 s (9:26), 0 failed, 0 skipped** (21:28:52 → 21:38:21). Round 1: 63 passed in 640.28 s; the builder: 63 passed in 571 s.

Extra guards around the change, on `test_ile_v524_pxbr` once the twins released it, concurrently with G1 (R12: one pytest per database; `logs/g2_extra.log`): `apps/pages/tests/test_home_v522_h.py`,
the three twins' non-browser parts, `tests/compliance/test_locked_content.py` (locked copy byte-identical),
`tests/compliance/test_public_pages.py` and `apps/pages/tests/test_contact_channels_v519.py` (the contact channels compared in
process), `tests/security/test_confidential_material.py` (with `ILE_CONFIDENTIAL_SENTINELS`),
`tests/compliance/test_no_personal_data_in_repository.py`, `apps/ecosystem/tests/test_companies_page.py` (the curated plate's
caption, D6 «unchanged»), `apps/forum/tests`, `apps/news/tests`, `apps/cms/tests` (the models that gained `attribution_required`):
**505 passed, 1 skipped, 63 deselected (the browser-marked ones), 0 failed in 502.99 s (8:22)** (21:38:45 → 21:47:12). The one skip is `apps/pages/tests/test_contact_channels_v519.py`'s configured-number test, environment-bound by design (`ILE_WHATSAPP_NUMBER` unset and the `.env` not read in the reviewer's process — the number is never printed); the same module's static channel checks passed. Round 1's equivalent run without that module: 451 passed, 63 deselected in 311.99 s. The confidential-material guard ran in-process with the private table and passed.

`ruff check .` → All checks passed · `manage.py check` → System check identified no issues · `makemigrations --check --dry-run` →
No changes detected · `scripts/check_ownership.py --validate` → coherent (59 families, 2 362 entries; the family `v524-px` is the
steward's R11 step, its `owns` globs and slices listed in NOTES §4).

## 2. Gate item 2 — the rendered crawl (the audit's `crawl.py` + `analyse.py`, pointed at 8792, nine personas)

Re-run on the committed tree at 21:29:39 → 21:35:48 (`.work/v524-px-qa2/{pages.json, summary.json, analyse.txt, logs/crawl.log}`;
GET only; the nine personas entered through the preview's switch, 200 each): **2 156 HTML pages, all 200** — 184 public (46 routes ×
4 languages, 29 s) + 1 972 signed-in (220 per person/company persona, 216 per organisation persona). **`<figcaption>`: 0 · slot
credits (`.foto__credit`): 0 · other figcaptions: 0 · attribute hits (alt / title / aria-label / content / href naming pexels |
unsplash | photo by): 0 · script / JSON-LD hits: 0 · HTML comment hits: 0 · Unsplash-library files served: none.** Visible-text
hits by kind: the footer's «© 2026 AGAMI — Dialogo Giuridico Interculturale APS» × 1 684 and the glossary term pages' legal-source
field «المصدر» × 57 — exactly F5's two false positives, outside the production test's patterns by construction; nothing else. The
26 slots are drawn on their 13 routes × 4 languages as the registry says; the personas' 432 slot-bearing pages are the public
pages seen signed in, 0 figcaptions. (The audit's figure before the change on the same tree: 104 credits on 52 public pages.)
Round 1 and the builder's crawl gave the same counts.

## 3. Gate item 3 — source grep over `templates/**` and `apps/*/templates/**` (excluding `templates/dev/**`)

`foto__credit`, `Pexels`, `Unsplash`, `Photo by`: **one hit**, `templates/components/photo.html:6`, inside the `{% comment %}` block
(the licence note: «the Pexels License requires no attribution … the full record (licence, author, Pexels page) is …»). Nothing
outside a comment; `apps/*/templates`: 0. `foto__credit` outside CSS: only the two tests that assert its absence
(`test_imagery_credits_v524.py:45` SOURCE_WORDS, `test_sezioni_browser_v522_s2.py:403`). Stale names of the renamed tests anywhere
in the tree (`.py`, `.md`, `.sh`, `.json`): 0.

## 4. Gate item 4 — every D6 row applied as written (V5.20's four conditions cited), re-read on the commit's diff

| Row | Applied in `2031bcb1` | Invariant |
|---|---|---|
| `test_imagery_v512.py` `test_every_slot_is_licensed_and_credited` | renamed `…_and_its_author_recorded`; the five assertions byte-identical (licence, photographer, page, id, files); docstring | same |
| `…_keeps_its_credit` | `…_and_its_author_stays_recorded`: photographer non-empty, `not hasattr(pic, "credit")`, the tag rendered through the engine has no `<figcaption` and no «Pexels» | stronger |
| `…` the tag draws a lazy figure | `"<figcaption" not in html and "Pexels" not in html` | stronger |
| `test_interior_w3_f1.py` the door's entrance | `select_one("figcaption") is None and "Pexels" not in str(photo)` | stronger |
| `…` «a plate is captioned, a stock frame is not» | every figure WITHOUT `data-slot` captioned; no `data-slot` figure captioned or naming Pexels (m1's complement form; docstring cites m1 + V5.20) | stronger than the audit's row |
| `test_figure_caption.py` (7 routes) | the same two invariants (complement form); module docstring; NEW `test_a_curated_asset_s_byline_follows_its_licence` (five free licences → publishable, no byline; CC BY → byline; `other` + `attribution=required` → byline) | stronger + new |
| `apps/pages/tests/test_home.py` | the same two invariants (complement form, renamed); the ecosystem bay comment → «no credit (V5.24 §2)» | stronger |
| `apps/ecosystem/tests/test_browser.py` | `figure.figura` vs `figure.figura figcaption`, plus `figure[data-slot] figcaption` == 0 | as written |
| `apps/pages/tests/test_browser.py` | comment only; assertions unchanged | same |
| `test_sezioni_v522_s2.py` | asserts `photo.html`'s markup has no figcaption; the source loop reads `_ingresso.html` AND `news/detail.html` (m2); the rendered `&nbsp;:` assertion unchanged | stronger |
| `test_sezioni_browser_v522_s2.py` | retargeted to a CC BY `MediaAsset` through `pages.services.photo_from_asset` → `_ingresso.html` in the library's bare page; the same colon invariant; plus `figure[data-slot] figcaption, .foto__credit` == 0 | as written + stronger |
| `test_home_v522_h.py` | `"<figcaption" not in frame`; docstring | as written |
| `test_companies_page.py:218`, `test_design_preview.py:1335` | not in the diff | unchanged |

Every changed test cites V5.24 §2 + FINAL_DELIVERY_V2.md §3.2 D6 + V5.20 in its docstring or comment; the m1/m2 modules cite the
reviewer's finding as well; no skip, no timeout, no assertion dropped without a stronger replacement. The complement form of m1
is safe on the walked routes: the product templates hold seven `<figure>` tags — `components/photo.html` (`data-slot`), five `figura`
plates each with a `<figcaption>` (`_ingresso.html:72/77`, `news/detail.html:59/61` conditional, `pathways/detail.html:64/66`,
`forum/partials/hero.html:48/50`, `permanent_sections.html:51/57`) and the enquiries blockquote figure
(`enquiries/company_needs.html:28`) — and none of the three modules' route lists (`PHOTO_PAGES`, `INTERIOR`, `/fr/`) walks the
enquiries page (see m5).

## 5. Gate item 5 — the stills (HEADED chromium-1234 under `CHROMIUM_LOCK_B`; `headed_px.py`; `headed.json`)

Pages `/fr/entreprises/`, `/fr/institutions/`, `/ar/parcours/`, `/fr/le-projet/` (the gate's four) + `/ar/entreprises/`,
`/ar/institutions/` (Arabic at the affected widths) × **1440×900 and 390×844** × motion on / `prefers-reduced-motion: reduce`
= **24 cells, 60 frames** measured on the lane, each (motion on) paired with the same frame on the base 8780 (`4bafcfa0`, the credits
still there). Stills: `C:/tmp/ile_v5_council/evidence/v524/px/qa2/<lang>_<width>[_rm]_<page>__<slot>.png` (the frame) and
`…__<slot>__viewport.png` (the viewport around it) — 120 files; round 1's 120 (`…/px/qa/`), the builder's headless 124
(`…/px/*.png`) and the improve round's 30 (`…/px/improve/`) stand beside them; the audit's before-stills are `…/pexels/`.

- **Captions / credits:** 0 `<figcaption>`, 0 `.foto__credit` in all 60 frames; every figure's children exactly `['picture']`;
  `::after` content none; page level in every cell: `.foto__credit` 0, `figure[data-slot] figcaption` 0, visible «Pexels | Unsplash |
  Photo by» 0, horizontal overflow 0, one `h1`, `dir` rtl on `/ar/`.
- **The frames unchanged:** the `<picture>` box is identical lane/base in **30 of 30 pairs** (companies.hero 608×405 at 1440, 335×189
  at 390; companies.territory 1440×617 / 390×167; institutions.hero 503×628 / 335×223; institutions.chamber 1425×900 / 375×844;
  pathways.hero 397×497 / 335×189; the four family frames 290×193 (other 282×188) / 295×127; project.hall 288×422 / 157×230;
  project.volumes 1440×617 / 390×488).
- **No empty caption box:** the `<figure>`'s bottom coincides with the picture's (`pic→fig bottom` 0 px on the lane in all 60 frames,
  against 48 px (fr) / 52 px (ar) on the base for the entrance frames, 28 px on the four family frames of Parcours, 0 on the bands and
  the chip frames where the caption was overlaid) — the figure shrinks by exactly the caption's height and nothing else moves.
- **Read on the stills (reviewer's eye, before → after):** `pexels/fr_1440_entreprises__companies.hero.png` shows the 12 px
  «Photo : Thirdman / Pexels» line under the calliper frame → `qa2/fr_1440_entreprises__companies.hero.png` ends at the picture, the
  drafting ornament beneath it untouched (`…__viewport.png`); the hemicycle's night ground carried a 195 × 20 px chip in its top-end
  corner (`pexels/fr_1440_institutions__institutions.chamber.png`) → none (`qa2/…chamber.png`, the arc of six seats and the plate
  unchanged); the Arabic Parcours entrance carried «صورة: Mikhail Nilov / Pexels» at its foot (`pexels/ar_1440_parcours__pathways.hero.png`)
  → clean (`qa2/ar_1440_parcours__pathways.hero.png`, the frame's foot against the drafting grid in `…__viewport.png`); Le projet's
  night frontispiece frame identical before/after (its credit was absolute under the frame, outside the element). The same at 390
  (`qa2/fr_390_entreprises__companies.hero.png`, `fr_390_institutions__institutions.chamber.png`, `ar_390_parcours__pathways.hero.png`,
  `fr_390_le-projet__project.hall.png`).
- **Reduced motion:** the same 60 measures under `reduce` (the `_rm` stills): identical boxes, 0 captions, 0 console errors.
- **Keyboard:** on every page at both widths the first Tab sets `html[data-input="key"]` and lands on the skip link; 0 of the next
  20 Tabs land inside a `figure[data-slot]` (nothing focusable in a frame); 0 slot captions after 21 Tabs.
- **axe-core 4.13 (WCAG 2.0/2.1/2.2 A + AA) on the changed sections** — the closest `[data-section]` / `section` / `article` around
  each frame (`header.ingresso` on every page, `#destinataires` on Institutions, `section.sez.sez--tracciato` on Parcours): **0
  violations in all 12 cells.** Document level: 0 in 10 cells; `target-size` serious ×1 in the same two cells as round 1, both after
  the 21-Tab keyboard pass and both outside PX's change — `.approdo__link.sez-stretch[href$="projet-pilote/"]` (`/fr/entreprises/` 390)
  and `.site-footer__email` (`/ar/institutions/` 390) — m3, recorded for the matrix's axe cells (R14).
- Console: 0 errors, 0 page errors in all 24 cells.

## 6. Gate items 6 and 7

- (6) `MediaAsset.is_publishable` unchanged: the diff of `apps/cms/models.py` removes 0 lines and adds only the
  `attribution_required` property (its source still 11 lines); the registry read in process: **26 slots**, `picture("companies.hero")`
  has no `credit` attribute, every slot's record has a Pexels License, a photographer and a `pexels.com/photo/` page —
  `test_every_slot_is_licensed_and_its_author_recorded` asserts the same five things it did (body byte-identical to the V5.12 test).
- (7) `/__design-v5/specimens/imagery/` on 8792: **200, 11 slot figures, 0 figcaptions, 11 data sheets «Pexels <id>»** (11499083,
  27177298, 29454379, 29976379, 30563520 …) — the internal provenance kept, the frames uncaptioned.
- (m2 re-verified) the news byline fragment of `templates/news/detail.html:61` rendered through the engine with a stub asset:
  CC BY → fr « — Photo&nbsp;: X», it « — Foto: X», en « — Photo: X», ar « — صورة: X»; Pexels-licensed → empty in every language.

## 7. Budgets (gzip -9 on the built dist; `npm run build` twice with the installed packages)

Two builds identical (`dist1.sha` = `dist2.sha`: the 77-file list's sha256 `e2d7a53e…` both times, 21:28:25 and 21:28:26), `git status
static/` empty after both; `git diff design-v5 HEAD -- static/css/dist static/js/dist` empty: **the dist is byte-identical to the
base's.** PX touches no stylesheet (D3): every sheet measures as the base's (`gzip_measures.txt`).

| Sheet | lane | base | ceiling |
|---|---|---|---|
| `main.css` | **32 716** | 32 716 | ≤ 32 716 (R4 c) |
| `pages/css/pages.css` · `hero.css` · `fronte.css` · `interior.css` | 11 306 · 10 899 · 6 141 · 8 827 | same | home ≤ 61 440 total; interior 11 264 |
| `core/sezioni.css` · `core/reveal.css` | 11 308 · 3 526 | same | — |
| `ecosystem/{ecosystem,companies,institutions,pilot}.css` | 4 977 · 8 701 · 8 381 · 9 508 | same | pilot 9 728 |
| `pathways/{pathways,index,diplomas,training,sheet}.css` | 4 716 · 10 117 · 8 895 · 8 788 · 9 701 | same | index 10 240 |
| `cms/lettura.css` · `cms/faq.css` · `cms/lessico.css` | 6 512 · 1 935 · 2 384 | same | 9 216 · 2 048 · 2 560 |
| `pages/css/rete.css` · `agami.css` · `frodi.css` · `forum/forum.css` | 1 817 · 1 760 · 1 200 · 7 369 | same | 2 048 · 2 048 · 1 536 · 8 192 |

HTML (lane 8792 against base 8780, the CSRF token and the port masked): `/fr/` 129 422 → 129 083 B (−339, 4 frames), `/ar/parcours/`
79 499 → 79 112 (−387, 5 frames), `/fr/entreprises/` 77 470 → 77 316 (−154), `/fr/institutions/` 60 676 → 60 511 (−165),
`/fr/le-projet/` 62 489 → 62 330 (−159), `/ar/entreprises/` 76 283 → 76 143 (−140), `/ar/institutions/` 59 736 → 59 585 (−151) —
**−70 … −85 B per frame**, `<figcaption>` / `foto__credit` / «Pexels» counts 4→0, 5→0, 2→0 on each; the pages without a slot frame
(`/fr/agami/`, `/ar/faq/`) byte-identical once masked. JS 0, images 0, fonts 0. Catalogue +0 −0 (no `locale/**` file in the diff;
`msgid "Photo"` still used by `_ingresso.html`, `news/detail.html`, `pathways/detail.html`, `forum/partials/hero.html`).

## 8. Preserved families, locked copy, contact channels, ownership

- Locked copy: no `{% locked %}` tag, no registry file, no `apps/cms/locked_content.py`, no `locked_content.sha256.json` in the
  diff; `tests/compliance/test_locked_content.py` green in G2 — byte-identical.
- Both contact channels: `/fr/contact/` and `/ar/contact/` fetched from 8780 and 8792 and compared in process — the `tel:` href set
  equal (1), the `wa.me` href set equal (1), the `<bdi dir="ltr">` count equal (2); nothing printed. The contact page loses only its
  slot frame's figcaption (1 → 0).
- §9.8 families: no file of the navbar, the mega menus, Lume, the forms, the privacy pages, `base.html`, `tokens.css`, `main.css`,
  the portal or the platform in the diff (the 21 files: 4 product templates/models/services, 2 slices, 11 test modules, 1 new test,
  2 documents, the NOTES); the nine personas' signed-in pages in the crawl (§2) render as before (0 figcaptions there on the base
  too — the platform never drew a slot frame).
- Repository files LF: all 21 changed/new files 0 CRLF, 0 backspace bytes.
- Tools (V5.26 §4, R10): the lane's NOTES §3 and §10 record each real tool → decision → change (the audit's crawler, headless and
  headed Playwright Chromium, the Django template engine) and the design skills as **not used by decision** (no composition,
  component or motion reopened — R9, V5.25 §1); no «design-critique» / «design-handoff» claimed; no 21st component. The reviewer
  concurs: an attribution change is a DOM question, and the abstraction rule is respected (one property on the two models, one
  guard form offered to every caption template, no one-off CSS).

## 9. Findings

**Blockers: none.** Round 1's B1 and B2 are closed (NOTES §6–§7 hold the figures; the one commit `2031bcb1` carries the 21 files,
LF, the register-form message).

**Minor (recorded, not blocking):**

- **m1 — CLOSED (applied, verified).** The complement form («every figure without `data-slot` is captioned») in the three modules;
  green in G1; 0 uncaptioned non-slot figures in the headed DOM of the eight motion-on cells.
- **m2 — CLOSED (applied, verified).** `news/detail.html:61` takes `_ingresso.html:77`'s no-break colon form; the s2 source loop
  reads both templates; rendered in the four languages (§6).
- **m3 — stands (outside PX).** axe `target-size` after a keyboard pass on `.approdo__link.sez-stretch` (Entreprises 390) and
  `.site-footer__email` (Institutions ar 390): reproduced identically in this round, not at rest; for the matrix's axe cells (R14).
- **m4 — stands (other lanes).** The dead `.foto__credit` rules — 17 in the source sheets (14 + 2 + the dev specimen sheet), bundled
  into 15 dist files, 0 in `main.css` — stay until LIB / PUB1 / HOME / PUB2 / CLOSING delete them (NOTES §4 lists every file:line).
- **m5 — NEW, a note for the m1 form's future walkers.** The complement rule treats every non-`data-slot` `<figure>` as a plate that
  must be captioned; the one such figure that is not a plate is the enquiries page's blockquote
  (`templates/enquiries/company_needs.html:28`, `figure.blockquote`), on a route none of the three modules walks today. A lane that
  adds `/fr/entreprises/recueil-des-besoins/` to `PHOTO_PAGES` / `INTERIOR` would have to exclude `figure.blockquote` (or scope the
  rule to `figura`) — a one-line note for CLOSING's test pass; no change now (R14).
- **m6 — NEW, the contract's three remaining bylines (other lanes).** `pathways/detail.html:66` and `forum/partials/hero.html:46` still
  print « — Photo : {{ credit }}» whenever a credit is recorded, and `permanent_sections.html:57` «© {{ credit }}» — the PUB1/PUB2
  contract guard `{% if …credit and …attribution_required %}` (NOTES §4) is not yet applied, as the merge order foresees (PX merges
  first). Latent today (0 publishable assets, 0 CC BY); the gate's production test does not catch a person's name by construction
  (F5), so a future Pexels-licensed curated plate on those three surfaces would print its author until the owning lanes apply the
  guard. Recorded for the steward to check at PUB1's and PUB2's gates.

## 10. Scores (the gate's measured surfaces; no composition change → 4 where a dimension is not applicable)

The lane moves no dimension of the four gate pages (their scores stand from their lanes' merges — Entreprises, Institutions and
Parcours DL54-183/184, Le projet DL54-186; V5.25 §5, R9). Imagery is the one dimension PX touches, and only by removing the
stock-catalogue signal (V5.24 §3): the frames, their sizes, grades, masks and positions are unchanged. See the structured result:
Entreprises, Institutions, Parcours (ar), Le projet — at 1440 and 390, fr and ar.
