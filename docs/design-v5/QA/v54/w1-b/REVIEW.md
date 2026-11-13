# W1-B — the icon system · senior review (one pass, V5.5)

Italy Legal Entry™ · design V5 · V5.4 plan §1.7, §2.3, §3.3 item 5 · V5.5 delivery mode · label **w1-b-review** ·
9 October 2026 · branch `v54-w1-b` at `d9e6b07` (W1-A and the publication commits merged in), worktree
`C:/tmp/ile_wt/v54-w1-b`, reviewed on its own server **127.0.0.1:8886** (`ile_v5_l6`, `ILE_REFERENCE_DATE=2026-10-03`,
`ILE_DESIGN_PREVIEW=1` on its own port for the board). I built nothing; one pass, design + UX + taste together, against the
owner's bar («credible alongside excellent international digital products») and the settled direction (plan §1.7,
DL54-20 … 24, the research map «IC»).

## Verdict — SHIP_AFTER_FIXES

The icon system itself is at the bar: one hand across the whole product, the four audiences and the four domains
unmistakably distinct at 16, 20 and 24 px, correct flips in Arabic, no stock-icon feel where the registry places a glyph.
Three things visible on the real pages are below the bar and each is a few lines: the console rail still *says* V4
meanings with the new drawings (M1); the empty states draw a thinner hand than the rest of the page (M2); the empty-state
default makes `document` mean «nothing here yet» on ten public pages (M3). None needs a design decision; none touches the
sprite, the registry or the tag. No P0: no broken page, no wrong direction, nothing unusable, no data or security problem.

## What I looked at

- **The real pages, fr and ar, 1440 / 1366 / 390 / 360** — 204 full-page captures on 8886 with a probe of every `<use>`
  (`C:/tmp/ile_v5_council/evidence/v54/w1-b/review/pages/run1|run2|run2co/`, `log.json` per run): the implementer's
  29-page set at the four widths (run1, 116); 38 more pages at 1440 and 390 — network, companies, project, Forum,
  formation, diplômes, glossaire, partenaires, login, pathway detail, living topics, FAQ, the console's situation / guichet /
  formation / selection / account pages, and the Arabic console (run2, 76); the company workspace with a company persona
  (run2co, 12). Sessions minted with `Client.force_login` by a scratch script outside every repository (no password used,
  typed or stored).
- **Element crops of the icon contexts at DPR 1 and 2** (`…/review/contexts/ctx2/`; `ctx1/` is a first pass whose
  below-the-fold crops are mis-framed): utility bar, header, hero legend, drawer, network discs, pathway list,
  anti-fraud links, rail, bottom bar, breadcrumbs, document rows and row menu, actor discs, meta rows, notices, empty
  states, footer — fr and ar, 1440 and 390, person and company personas; the open account menu from the page runs
  (`fr-dashboard-menu`, `ar-dashboard-menu`). Crops from the full pages for the mobile first screens, the 1366 and 360
  screens, the rows and the empty states (`…/review/mobile-crops/`).
- **The specimen board** `/__design-v5/specimens/icons/` at 1440 1× and 2× and 390 2× (`…/review/sheet/`: 297 symbols
  drawn, 0 unresolved, the Arabic block mirrored, the French not) and its seven sections cropped at 2× (`…/sheet/crops/`).
- **The implementer's evidence**: the one-hand sheet beside raw Lucide at 1× and 2× (`impl-1/lucide/`), the distinctness
  strip and the raster measurement (`impl-1/measure/`).
- **The code**: `apps/core/icons.py`, the `svg_icon` tag and filters, `components.css` §2, the sprite, every `svg_icon`
  call site (57 + 14 + 5 `arrow` sites and every other literal), the producers that still emit V4 ids, the CSS of every
  icon slot, every `stroke-width` left in the non-generated sheets.
- **Tests, on a review-only test database** (`test_ile_v5_review`): `test_icons.py` + `test_svg_wellformed.py` +
  `test_static_assets.py` + `apps/pages/tests/test_templates_static.py` — **251 passed in 2.1 s**; the mirrors slice of
  `tests/i18n/test_rtl_browser.py` (`-m browser -k "mirrored or breadcrumb"`) — **5 passed in 90 s**.
- `scripts/check_ownership.py w1-b design-v5`: 117 inside, 41 slice, 1 generated, **4 OUTSIDE — exactly DL54-24's**
  (`apps/documents/requirements.py`, `apps/pages/tests/test_templates_static.py`, `static/css/dev/specimen-icons.css`,
  `static/css/v4/workspace.css`): the steward writes them into the manifest at the merge, as the plan says.

## What passes (measured, not assumed)

- **One hand.** On all 204 captures every visible glyph computes to `1.5px square miter` — except `.icon--xl` at 1.67 px
  (the plan's step-up) and the one override named in M2. 0 unresolved `<use>`, 0 symbols rendered below their `MIN_SIZE`
  floor, 0 unknown ids, 0 V4 ids in the markup (the tag resolves the five aliases; the sprite is served once, hashed:
  `icons.svg?v=dbbb2fe693ff`), 0 console errors on a product page, no horizontal scroll (the 404 entries are Django's
  technical page under DEBUG). The lane log holds no «svg_icon: no icon called».
- **Beside raw Lucide the sprite reads as ILE.** Square caps, miter joins and the 1.5 px stroke flatten Lucide's round
  2 px look across the 64 donors; the identity tier (arch, key, steps, mark) and «i cerchi» are the product's own; the
  re-proportioned V4 drawings sit on one live area. The donors are still recognisably Lucide geometry — Q5 accepted that —
  and the stock feel stays down because a glyph never stands without its word and the registry places every concept.
- **The four audiences are unmistakably different** at 14 → 32 px on the board, in the 24 px actor discs (16 px glyph),
  in the hero legend (16 px on night) and in the 56 px discs of the network page (fr and ar): a bust, a tower with its
  annex, a pediment on columns, a mortarboard. The documents page is the hard case and it holds: person / stamp /
  mortarboard / tower in one 16 px column at 1440 and at 390, fr and ar.
- **Documents, Case, Academy, Forum are each clear on the board and in the registry** (`document`, `folder`, `book-open`,
  `handshake`; the closest pair `folder` / `book-open` measures 0.62 at 16 px). On the real pages only `document` and
  `book-open` (as a pathway) render today — M1 says why.
- **RTL.** On every Arabic page the flip class sits on the closed list and on nothing else: `arrow`, `arrow-start`,
  `chevron-end` (breadcrumbs), `logout`, `send` («طلباتي» points left), `signpost`; the key, the steps (Q8), the mark, the
  audiences, `history`, `refresh-cw` and the status marks never mirror. Checked on the overlays too: the open account
  menu (key / profile / shield unflipped, `logout` mirrored), the phone drawer's «Espace réservé» key, the bottom bar,
  the row menu (eye / download / history unflipped), the breadcrumbs, the footer, the anti-fraud links (`signpost`
  mirrored). The board's direction section shows the pairs side by side; the browser mirrors test passes.
- **Legible at the three sizes.** 16 px: the actor discs, the due dates, the meta rows, the account menu; 20 px: the rail,
  the bottom bar, the notices, the row menus, the search; 24 px: the network discs, the journey stations, the «Comment ça
  marche» steps. The key at 14 px in the utility bar is at its measured floor and still reads as a key.
- **Semantics on the pages W1-B re-mapped**: the key for «Espace réservé» ×5 (one object for one idea, never `lock`);
  `circle-user-round` / `shield` / `logout` in the account menu; `stamp` for the authority, `badge-dot` for the authorised
  actor, `ile-mark` for the team; `at-sign` for an address (the error page too); `shield-alert` for the anti-fraud entry
  everywhere; the pathways through `PATHWAY`; the due dates through `DUE` (the «expire dans 3 jours» row carries `clock`,
  the rest `calendar`); the row menu `ellipsis-vertical` → `eye` / `download` / `history`; the living index typographic.
- **CSP, a11y, no package.** No inline style or script added in the template diff; the board has its own sheet; the
  sprite is self-hosted. Decorative glyphs carry `aria-hidden="true" focusable="false"`, a labelled one `role="img"
  aria-label`; every glyph sits beside its word (the collapsed rail below 90 rem is the exception, W3-A's). `currentcolor`
  only — forced colours follow the text. No icon library in `package.json`; `ICON_LICENSES.md` names the 64 donors with
  the ISC notice.

## Findings

### Major — fix before the merge (each a few lines; no new design)

**M1 · The console rail still says V4 meanings with the V5 drawings.** `portal.services.NAV_GLYPHS` and the company rail
emit `map-pin` = Mon parcours, `briefcase` = Mes dossiers, `handshake` = Guichet numérique, `university` = Academy,
`calendar` = Mes échéances (company: `briefcase` = Mes besoins, `map-pin` = Analyse). In the new system those drawings
mean the journey (`ile-steps`), the professional (`briefcase`), the Forum (`handshake`), the training body / Università
(`university`), a date (`calendar`). Measured on the 204 captures: `handshake` renders **136** times and every one means
«help desk»; `briefcase` 208 times, never once as the professional it stands for; the mortarboard appears **twice with two
meanings on the documents page** (rail «Academy» and the row's «L'organisme de formation»); `folder`, `concierge-bell`,
`list-ordered`, `wrench`, `map`, `inbox` never render anywhere. At 1366 the rail is glyph-only (`console.css`: labels only
from 90 rem), so on the most common laptop width those four glyphs are the whole signifier. DL54-23 hands the rail to W3-A
and that is the plan — but the registry's `NAV` and `COMPANY_NAV` are written, tested and keyed on the producers' own keys,
the aliases keep every page drawing, and no test pins the V4 ids. **Fix:** `NAV_GLYPHS = dict(icons.NAV)` in
`apps/portal/services.py` and the four ids of `companies.services.navigation` from `icons.COMPANY_NAV` (two files, ~6 lines,
no CSS: `concierge-bell` and `wrench` are floor 20 and the rail draws 20 px) — written into W1-B's merge as a justified
extra path (plan §2.2), or W3-A's rail re-map merged before the integration milestone; either way, not shipped to the
preview as it is.

**M2 · The empty states draw a thinner hand.** `components.css` §23 `.empty-state__icon { stroke-width: 1.25 }` was
2.1 px on the scaling sprite and is **1.25 px** since DL54-20 (named there, handed to W3-E): the home's «Actualités» state
(40 px), every public «en cours de préparation» state, the dashboard cards' states (28 px) and the console's deadlines /
messages / requests states (24 px) all read lighter than every other glyph on their page (`run1/log.json`: the only
`1.25px` entries). «No page worse than before» is W1-B's own gate. **Fix:** delete the declaration (the `.icon` rule's
1.5 px applies; at 40 px the plan's table would give ≈ 1.8, so `1.67` is also right for that seat) — one line, written
into the merge like DL54-24's paths.

**M3 · `document` means «nothing here yet».** `components/empty_state.html` defaults its glyph to `document` and 22 of its
28 call sites pass none: the FAQ, the glossary, the Forum, the partners, the news index, the living index and topics, the
pathway detail's four states — and `pages/home/_news.html` asks for `document` explicitly. `document` is the concept glyph
of «Mes pièces» (toned, through the registry); on the home it now says «no news». One glyph, two concepts — the disease the
registry was built to cure, on ten public pages. **Fix:** the partial draws a glyph only when one is passed
(`{% if icon %}`), the home news and the news index pass `newspaper` (floor 20; the slot is 40 px); the console callers
already pass their domain glyph.

### Minor — polish, owners named

**m1 · The living topic's heading glyph floats.** `.icon--heading` has no rule anywhere, so the topic glyph (the house on
«Logement») renders at the default 20 px on its own line above a 40 px title, fr and ar, 1440 and 390 — an orphaned mark.
Either `.icon--heading` sized to `--icon-xl` and inline with the title, or no glyph on the topic page (W3-F2's page;
W1-B's call site).

**m2 · The pathway rows carry three markers.** Numeral, a 16 px accent glyph alone above the title
(`.pathway-list__icon`, no rule), and the arrow — IC rule 6 / HO-7 («one marker per thing») and the «donors side by side
in equal rows» risk of IC §11.5. W1-B's mapping (factory, id-card, book-open, university, users, store, flask-conical,
split) is right; W3-F1's recomposition should keep the numeral or the glyph, and a kept glyph sits on the title line at
20 px.

**m3 · `handshake` is the weakest drawing at 20 px** — the two cuffs merge in the rail at 1366 and 1440. When it becomes
the Forum's glyph (M1), keep it at ≥ 24 px wherever it is the only identifier, or drop the cuff lines in its one source.

**m4 · The documents filter chips still draw V4's chip marks** («Manquant» and «À remplacer» share a circular-arrows
mark); `v3/chip.css` `.chip__g { stroke-width: 2.6 }` would now be 2.6 px if it rendered. W1-C's chip board, with `STATUS`
ready.

## What the merge carries besides the fixes

DL54-24's four paths into the manifest; `static/css/dist/main.css` rebuilt from clean; the DS 2026 §13 count («114 icone.»)
and the two §2 weights regenerated by `regen_design_inventory.py`; DL54-20 … 24 renumbered only if another family's
entries land first. The `/fr/forum-virtuel/` 404 (the community app) and the `/fr/espace-reserve/forum-permanent/` 503
(the governance module answers «momentanément indisponible» by design) are not the icon family's and not icon defects.

## How to re-run

```
# the review server (its own port; the preview answers only it)
DATABASE_URL=postgres://ile:ile-dev-password@127.0.0.1:5439/ile_v5_l6 ILE_REFERENCE_DATE=2026-10-03 DB_CONN_MAX_AGE=0 \
  ILE_DESIGN_PREVIEW=1 ILE_DESIGN_PREVIEW_PORT=8886 python manage.py runserver 127.0.0.1:8886 --noreload
# the family's fast tests on a review database
TEST_DATABASE_URL=postgres://ile:ile-dev-password@127.0.0.1:5439/test_ile_v5_review python -m pytest -q -p no:randomly \
  tests/frontend/test_icons.py tests/frontend/test_svg_wellformed.py tests/frontend/test_static_assets.py \
  apps/pages/tests/test_templates_static.py
python -m pytest -q -m browser tests/i18n/test_rtl_browser.py -k "mirrored or breadcrumb"
# the capture and crop tools (scratch, outside the repositories): C:/tmp/ile_v5_council/.work/w1-b/w1-b-review/
#   capture_review.py set.json|set2.json|set_company.json <label> [widths] [session] · crop_contexts.py contexts.json <label>
#   capture_board_review.py · mint_session.py person|company (Client.force_login, no password)
```
