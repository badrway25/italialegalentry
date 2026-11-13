# W1-B — the icon system · implementation notes

Italy Legal Entry™ · design V5 · V5.4 plan §1.7, §2.3, §3.3 item 5 · V5.5 delivery mode · label **w1-b-impl-1** ·
8 October 2026, resumed 9 October · branch `v54-w1-b`, worktree `C:/tmp/ile_wt/v54-w1-b`, lane 6 (8786, `ile_v5_l6`).

**Resumed after the usage cut.** The five uncommitted files of the interrupted start (the sources, the registry, the
build, the sprite, DS 2026 §13's list) were read, checked (`scripts/build_icons.py --check` current; the ownership check
at `047e2e2`: 112 inside, 1 slice, PASS) and kept — committed as `e324ce0` with the one addition the plan asks for
(§2.3: the five V4 alias symbols). Then `design-v5` was merged (`703be0f`: the clock fix `2e3d602` + `e16e811`, W1-K's
calibration record, W1-P shipped). Evidence: `C:/tmp/ile_v5_council/evidence/v54/w1-b/impl-1/` (E/ below). Scratch:
`C:/tmp/ile_v5_council/.work/w1-b/w1-b-impl-1/` (the source generator of the start, the measurement tool, the session
minting and capture tools — nothing of it enters the repository).

**Resumed again on 9 October, after the network outage.** The branch held the three code commits (`e324ce0`,
`d4bba6f`, `8631846`) and eleven uncommitted files; each was read against `git diff`, checked (LF bytes, a CSP scan
of the board, the ownership checker's verdicts) and committed in steps: `c6cc983` ICON_LICENSES.md · `07fabc7` the
specimen board · `a0f2ef0` DL54-20 … 24 · `10b8fbb` the four tests of chunk 1 · `26b3bc2` the page-integrity flip
detector · `44a19e0` the browser mirrors check · then these notes. `design-v5` had not moved (merge-base
`051e7f5` = its HEAD): nothing to merge. The lane server was restarted from the current tree (the 8 Oct process
predated the last commits; the dev server runs `--noreload`, and the cached template loader does not watch files)
through a scratch wrapper that exports the lane's variables **including `ILE_DESIGN_PREVIEW_PORT=8786`**: the preview
answers its own port only (`apps/designpreview/access.py`), so without it the board route is a 404; and with the
preview on the session cookie is `ile_v5_sessionid` (`config/settings/dev.py`), so the lane session is minted under
the same flags. The acceptance crop, the rendered-floor probe, the 58-page run (run3) and the board were then taken
again on the final tree.

**Then `design-v5` moved** (W1-A shipped: `8c3caad`, the steward's `4af28e0` / `8d45acd` / `474ced9`), and was merged
as `255b41f`: only the generated bundle `static/css/dist/main.css` conflicted
(merge=binary) and was rebuilt from the merged sources (`npm run build:css`); no template, no Python file, no DL54
number moved (design-v5 holds nothing beyond DL54-19, so DL54-20 … 24 keep their numbers). After the merge:
RBAC with `--create-db` 7 passed in 34.29s; chunk 1 **296 passed**; `test_page_integrity` **24 passed**; the browser mirrors **5 passed**; run4 (E/pages/run4/) — 58 captures, the symbol counts identical to run3 on every page, 0 unresolved `<use>`, the same flips; the board 297 drawn / 0 unresolved; the floors probe 977 drawn / 0 below a floor; `scripts/check_ownership.py w1-b design-v5`: 117 inside, 41 slice, 1 generated, the 4 paths of DL54-24 outside (for the steward's manifest).

**And once more** (the publication commits `759024c`, `7164633`, `024e3c6`, `db55a67`: the public tree, the ruff
findings, README, `.gitignore`, `.env.example`, a minimal CI), merged as `24cc184` with one auto-merge —
`apps/documents/requirements.py`, which keeps `ACTOR_GLYPHS = dict(icons.ACTOR)` — and no conflict; the lane server was
restarted on the merged tree (Python modules changed). After it: chunk 1 with `apps/documents` **443 passed**;
`test_page_integrity` **24 passed**; the browser mirrors **5 passed**; run5 (E/pages/run5/) identical to run4 on every
page, 2 116 `<use>`, 0 unresolved, the console pages signed in; the board 297 / 0; the floors probe 977 / 0; the server
log 0 «no icon called». HEAD after these notes is the branch's tip; `design-v5` was level with it at that moment.

## 1. What is implemented

**The sprite — one hand.** `static/icons/src/<id>.svg` (109 sources: the 22 pictorial V4 drawings re-proportioned
to the 21.5-unit live area, `building` / `document` / `info` / `warning` redrawn, the identity tier and «i cerchi» from
gate 0 with the review's candidates, 64 Lucide 1.48.0 donors under the ILE treatment) → `scripts/build_icons.py` →
`static/img/icons.svg`: **109 symbols + 5 V4 aliases (`user`, `home`, `list`, `globe`, `key`), 31 963 B raw, 6.5 KB
gzip**, strict XML, no colour, no style, no width of its own. Every stroked shape of a symbol is merged into one path
drawn with `vector-effect="non-scaling-stroke"`, so the `.icon` rule's stroke is CSS px at every size (DL54-20).
`--check` is the currency test; the build refuses a source that is not strict XML, not on the 24 grid, carries a
colour or a style, or whose origin comment disagrees with the registry.

**The registry** `apps/core/icons.py` (pure Python): `SYMBOLS` (tier, floor, donor, meaning), `GROUPS` (the sheet's
and §13's order), `MIN_SIZE`, `FLIP_RTL` (the closed list: arrow, arrow-start, chevron-end, logout, send, signpost,
panel-left-close), `TWINS`, `CHECK_BEARING`, `SHARED`, the concept maps (`AUDIENCE`, `ACTOR`, `NAV`, `COMPANY_NAV`,
`CARD`, `PATHWAY`, `LIVING`, `JOURNEY`, `STATUS`, `NOTICE`, `DUE`, `ALERT`), `LEGACY`, `resolve()`, `concept()`,
`floor_violation()`.

**The tag** (`apps/core/templatetags/ile_core.py`): `{% svg_icon %}` resolves an alias to its V5 symbol, adds
`icon--flip-rtl` to the flip-list symbols and strips it from every other, draws nothing for an empty or unknown name
(logged), and serves the sprite **with a content hash** (`/static/img/icons.svg?v=<sha256[:12]>`, unless the manifest
storage already hashes the name). Filters `concept` (`{{ card.key|concept:"card" }}`) and `actor_glyph`; tag
`icon_registry` for the board.

**CSS** — `components.css` §2 rewritten: `.icon` 1.5 px, square caps, miter joins, `currentcolor`; `.icon--xs … --hero`
on `--icon-xs … --icon-hero`; `.icon--xl` 1.67 px, `.icon--hero` 2 px. `static/css/dist/` rebuilt (`npm run build:css`).

**Every call site re-mapped** (not the rail, W3-A's): the key `ile-key` for «Espace réservé» ×5 (utility bar, drawer,
home band, access point, account menu); the account menu (`circle-user-round`, `shield` for «Sécurité du compte»,
`logout`); the actors through the registry (`ACTOR_GLYPHS = icons.ACTOR`: the authority is `stamp`, the authorised
actor `badge-dot`, the project team `ile-mark`); the notices per kind (`NOTICE`), the allauth alert per level
(`ALERT`), form errors `circle-alert`, the unavailable form and card `circle-pause`; the due dates through `DUE` (doc
rows, dashboard, case file: calendar · clock · alarm-clock); the row menu `ellipsis-vertical`, «Consulter» `eye`, the
versions `history`; the pagination `arrow-start`; e-mail addresses `at-sign` ×6; the anti-fraud entries `shield-alert`
×4; the anti-fraud page's links `circle-help` / `signpost` / `book-a`; the message's sender `ile-mark` and its read
state `mail-open`; the rules version `history`, the reference `hash`; the pathways through `PATHWAY` (index, detail
eyebrow) and «Comment ça marche» `ile-steps`; the living topic through `LIVING`; the living index, the pathway
document list and the ecosystem enumerations typographic (no glyph per bullet; no `check` as a bullet); the
dashboard cards through `CARD` (header and empty state); the deadlines and requests empty states; the access point
`layout-dashboard`. Count: 58 template files touched by the re-mapping or the aliases.

**Tests.** `tests/frontend/test_icons.py` (16 tests: registry = sprite; strict, clean, under the ceiling; the sources'
origins; the build current; tiers, floors, flip list, twins, check rule consistent; the tone on the concept tier;
shared symbols reviewed; twins never in one list domain; template literals never an alias, a mark or the seal;
check-bearing symbols out of chips, nodes, rails and discs; no literal below its floor; the producers' maps are the
registry's; the tag's behaviour and hash; no icon library; the licences name every donor).
`test_svg_wellformed.py` (+ the sources), `test_static_assets.py` (the V5 id set), `tests/i18n/test_page_integrity.py`
(`_FORWARD_ICONS` = `FLIP_RTL`, and no other symbol carries the class), `apps/pages/tests/test_templates_static.py`
(the icon list read from the sprite).

**Documents.** `docs/design-v5/ICON_LICENSES.md` (what is whose; the 64 donors with the applicable notice; ISC and MIT
verbatim; how a donor enters and leaves). DS 2026 §13 prose rewritten (the list regenerated by the build, «114
icone.» as `regen_design_inventory.py` reads it). DL54-20 … DL54-24. The specimen board
`/__design-v5/specimens/icons/` (`templates/dev/designpreview/specimens/icons.html` + `static/css/dev/specimen-icons.css`):
the four audiences at 14–32 px and in their discs, fr and ar; the platform domains on paper and night; the journey
line; responsibility; «i cerchi» at 14 / 16 / 20 px on paper and night; the notices, the due dates, the actions;
direction LTR and RTL; every symbol from the registry with its floor.

## 2. Measures

- **Sprite:** 31 963 B raw (ceiling 32 768), 6 485 B gzip, 114 symbols (109 + 5 aliases); 0 hex, 0 style, 0 width.
- **Raster measurement** (E/measure/: `metrics.md`, `metrics.json`, the raster at 1× (`raster`, suffix `@1x`, PNG), crops ×6; method IC §11.1: every
  symbol at 14 / 16 / 20 / 24 px through the V5 `.icon` rule, headless Chromium DPR 1 and 4, a 0.5 px closing on the
  4× raster, fuzzy Jaccard at 16 px):
  - **Floors:** the registry and the measurement agree for 107 of 109 symbols; two were raised to the measured floor
    (`newspaper` 20, `alarm-clock` 20 — 10.9 % at 16 px even without its feet); six keep the review's stricter floor
    (`institution` and `university` 16, `handshake` 20, `factory`, `languages`, `house` 16).
  - **Live area at 24 px:** median 21.5 units; `institution` was at 24.0 (its 32° miter corners spiked past the box —
    the roof and the base are separate subpaths now: 21.0) and `quote` at 18.0 (re-proportioned: 21.5). Outside
    19.5–22.5 by design: `ile-key` 18.5 (the key as the review draws it), the four outline marks 19.0 (16 px chip
    glyphs), `list-ordered` 19.25 (the donor).
  - **Twins (≥ 0.75 at 16 px):** every registered group confirmed (`st-conforme` / `st-azione` 0.886, `badge-dot` /
    `badge-check` 0.881, `shield` / `shield-alert` 0.867, `pen-line` / `pencil` 0.811, `building-2` / `school` 0.751);
    and the circle family is one group now that `info` and `clock` sit at the donors' radius — `info` / `circle-alert`
    0.938, `circle-alert` / `clock` 0.892, `circle-help` / `info` 0.840, `compass` / `circle-pause` 0.757 — the registry
    says so; no list domain holds two of them (tested).
- **Distinctness, the acceptance pairs** (E/measure/: `audiences-domains-16-20-24px-1x-x6.png`, `distinct.md`,
  `distinct.json`; the same method at 16 and 20 px): Persona / Impresa / Istituzione / Università and Documents /
  Case / Academy / Forum, every pair under the 0.75 twin threshold — the closest are `folder` / `book-open` 0.618
  and `building` / `institution` 0.578 at 16 px (0.645 and 0.505 at 20 px); the rest 0.26–0.37. Each of the eight
  reads as its own thing at 16, 20 and 24 px in the ×6 strip.
- **The one-hand sheet** (E/lucide/: `lucide-vs-ile` at 1× and 2× (suffixes `@1x` and `@2x`, PNG), the page): the 64 donors beside raw Lucide at
  24 and 16 px, then the 45 ILE drawings — one weight, one cap, one join across the sheet.
- **Pages** (E/pages/run2/ on 8 Oct and E/pages/run3/ on 9 Oct, the final tree: 58 captures each, `log.json`): fr
  and ar, 1440 and 390, public and console with a session minted by `Client.force_login` on `ile_v5_l6` — run3:
  **2 116 `<use>`, 0 unresolved**, **0 console errors** besides the technical 404 page's own status, no horizontal
  scroll on a product page, computed stroke 1.5 px everywhere (1.67 px on the xl marks; 1.25 px on
  `.empty-state__icon`, §3), the flip class only on the list's symbols (`arrow`, `chevron-end`, `logout`, `send`,
  `signpost`), and the symbol counts of every one of the 58 pages identical between run2 and run3; the lane server's
  log holds **0 «svg_icon: no icon called»**. The «404» entries are Django's technical page (the dev server runs
  DEBUG; at 390 it is the one that scrolls sideways): not the product's.
- **Rendered floors** (E/pages/run3/`floors.md`, `floors.json`): on the same 58 captures every drawn symbol's rendered
  box against `MIN_SIZE` — **977 drawn symbols, 0 below its floor, 0 unknown ids**; the smallest renderings are the
  key at 14 px (its floor) in the utility bar, and the audiences, `document`, `stamp`, `calendar`, `history` at 16 px
  (their floors). `alarm-clock` never meets the 16 px `.doc-row__due-icon` on the QA persona's data: W3-C's item in
  §3 stands on the CSS, not on a capture.
- **The board** (E/sheet/, re-taken 9 Oct): 297 symbols drawn, 0 unresolved, 0 console messages, the Arabic block
  mirrored (`matrix(-1, …)`), the French one not; 1440 at 1× and 2×, 390 at 2× without horizontal scroll.
- **Tests** (lane 6, `TEST_DATABASE_URL` = `test_ile_v5_l6`, `-p no:randomly`). 8 Oct: chunk 1 — `test_icons`,
  `test_svg_wellformed`, `test_static_assets`, `test_design_docs`, `test_css_bundle_is_current`,
  `apps/pages/tests/test_templates_static.py`, the portal and ecosystem compliance scans, `apps/documents`, `apps/core`:
  **475 passed** (2 min 02 s); chunk 2 — `tests/i18n/test_page_integrity.py`: **24 passed** (2 min 12 s). 9 Oct, on
  the final tree: chunk 1 (the six files of the family, without the app suites) — **296 passed** (5 s); chunk 2 —
  **24 passed** (1 min 56 s); chunk 3 — `apps/portal/tests`, `apps/cases/tests`, `apps/accounts`,
  `apps/companies/tests`, `apps/pathways`, `apps/living`, `apps/documents`, `apps/core`: **763 passed, 3 skipped, 1 failed in 16 min 21 s — `apps/accounts/tests/test_rbac.py::test_ensure_roles_creates_every_group_idempotently` (`created == 6`, not 15: nine role groups were already in the reused test database, left by the 8 Oct chunk 3 that the outage killed mid-run); re-run after the merge with `--create-db`: 7 passed in 34.29s — nothing of the icon system**; the mirrors
  slice of `tests/i18n/test_rtl_browser.py` (`-m browser -k "mirrored or breadcrumb"`, pytest-django's
  `live_server`): **5 passed (the mirrors test and the -k matches) in 41.8 s; 5 passed again after the merge**. The full suite is an integration checkpoint's (V5.5), not this family's.
- **Ownership** (`scripts/check_ownership.py`): every path inside the family's slice except the five of DL54-24
  (`apps/documents/requirements.py`, `static/css/v4/workspace.css:377`, `apps/pages/tests/test_templates_static.py`,
  `static/css/dev/specimen-icons.css`, the filters in `ile_core.py`) and the generated `static/css/dist/`. A check
  against `design-v5` also lists W1-A's files, which this branch carries (it was branched from `v54-w1-a` and W1-A is
  not merged yet); the check against `047e2e2` before the design-v5 merge was clean.

## 3. What is left, and for whom

- **The reviewer (one review, V5.5):** the board at 1× and 2× (E/sheet/) and the one-hand sheet (E/lucide/); the
  eight marks as marks — the chip board (W1-C) re-judges them in their chips (DL54-22, Q13).
- **W1-C:** the accordion keeps `plus` until its rebuild (the map's `chevron` turning 180° is §15's rule); `v3/chip.css`'s
  `.chip__g { stroke-width: 2.6 }` now reads as px — write 1.5 (or none); the marks through `STATUS` in `.chip__g`.
- **W3-A:** `NAV_GLYPHS` and the company rail — the registry's `NAV` / `COMPANY_NAV` are written for them; until then
  the aliases draw (`home` → `layout-dashboard`, `list` → `send`), and `check` (selection), `handshake` (Guichet),
  `map-pin` (journey), `university` (Academy), `briefcase` (cases) keep their V4 meaning in the rail.
- **W3-C:** `.doc-row__due-icon` is 16 px and `alarm-clock`'s floor is 20 (10.9 % at 16 px): a 20 px slot, or a
  simpler overdue mark; the identity `document` disc on every row (Q1 / Q4, the owner's).
- **W3-E:** `.empty-state__icon { stroke-width: 1.25 }` now means 1.25 px: 1.5, or none (the §2 rule).
- **W3-F1 / W3-F2 / W2-E:** the arrow density of the public editorial body (the six-icon ceiling, DL54-23 item 1);
  `pagination__icon-prev` is dead CSS in §22.
- **The steward:** the five extra paths of DL54-24 into the manifest; `regen_design_inventory.py` finds «114 icone.»
  and two stale §2 weights to regenerate at the merge (`components.css` 72.2 → 73.0 KB, `v4/workspace.css` 53.2 → 53.3
  KB — within the ± 10 % the test allows; families never edit them);
  the aliases leave with their last producer; DL54-20 … 24 are numbered on this branch (renumber at the merge if
  another family's entries land first).
- **The steward, the slices:** `tests/i18n/test_page_integrity.py` — beyond line 59 the detector `_unflipped` now also
  fails a symbol outside the list that carries the class (the slice's intent, both directions), with the import of
  `core.icons`; `tests/frontend/test_static_assets.py` — lines 234–270, inside :177–277.
- **Whoever runs the lane:** `ILE_DESIGN_PREVIEW_PORT=8786` with `ILE_DESIGN_PREVIEW=1`, or the board route is a 404;
  under those flags the session cookie is `ile_v5_sessionid`, so a session minted for the captures must be minted under
  the same flags (§4). The worktree's `.env` names the V4 control database `ile`: the lane's `DATABASE_URL` must be
  exported, never left to the file.
- **Not done here:** the full suite (an integration checkpoint's); Firefox / WebKit; a Moroccan reader for Q8 (`ile-steps`
  never mirrors, as the plan settled); forced colours on Windows High Contrast (emulated only in the review).

## 4. How to run

```
# the lane (plan §2.8; LANES.json lane 6)
DATABASE_URL=postgres://ile:ile-dev-password@127.0.0.1:5439/ile_v5_l6 ILE_REFERENCE_DATE=2026-10-03 DB_CONN_MAX_AGE=0 \
  ILE_DESIGN_PREVIEW=1 ILE_DESIGN_PREVIEW_PORT=8786 PGAPPNAME=ile-lane-6 python manage.py runserver 127.0.0.1:8786 --noreload
# (the preview answers its own port only; under these flags the session cookie is ile_v5_sessionid)
# the sprite and the §13 list
python scripts/build_icons.py            # python scripts/build_icons.py --check
npm run build:css                        # after a change to components.css §2
# the family's tests
TEST_DATABASE_URL=postgres://ile:ile-dev-password@127.0.0.1:5439/test_ile_v5_l6 python -m pytest -q -p no:randomly \
  tests/frontend/test_icons.py tests/frontend/test_svg_wellformed.py tests/frontend/test_static_assets.py \
  tests/frontend/test_design_docs.py tests/i18n/test_page_integrity.py apps/pages/tests/test_templates_static.py
python -m pytest -q -m browser tests/i18n/test_rtl_browser.py -k "mirrored or breadcrumb"
# the measurement and capture tools live in C:/tmp/ile_v5_council/.work/w1-b/w1-b-impl-1/ (measure_w1b.py, crops_w1b.py,
# mint_session.py, capture_pages.py, capture_board.py, probe_floors.py) and write under evidence/v54/w1-b/impl-1/
```

## Review fixes — the fix pass (label w1-b-fix, 9 October 2026)

The family's implementer again, under V5.5 (implement → review once → fix → ship), on the two verdicts of 9 October:
`REVIEW.md` (SHIP_AFTER_FIXES: M1–M3, m1–m4) and `A11Y_PERF.md` (SHIP AFTER FIXES: m1, m2, n1–n5), plus the one
finding the a11y check of «Il portico» handed to the icon system (W2-C1 `A11Y_PERF.md` 7: forced colours). Lane 6
(8786, `ile_v5_l6`, `ILE_REFERENCE_DATE=2026-10-03`); evidence `C:/tmp/ile_v5_council/evidence/v54/w1-b/fix/` (E/fix/
below, with an `INDEX.txt`); scratch and tools `C:/tmp/ile_v5_council/.work/w1-b/w1-b-fix/`; profiles under
`.profiles/w1-b-fix/` (removed at the end). One browser and one pytest at a time; every browser series and every
build waited on `PERFORMANCE_BENCHMARK_LOCK` (never held during this pass). The signed-in pages used sessions minted
on `ile_v5_l6` with `Client.force_login` (`sessions_w1b_fix.py`: seven QA personas; no password used, typed or
stored), revoked at the end.

**Resumed after a cut.** The branch held two uncommitted files of the pass the network drop cut
(`apps/portal/services.py`, `apps/companies/services.py`: the rails on the registry). Read against `git diff`, both
were right and were kept — stashed by hash for the merge, with a copy of the patch outside the repository (the stash
list is shared by every worktree), then re-applied and committed as `c7b257c`.

**Numbering.** W2-C1's entries reached design-v5 first as DL54-20 … 25: this family's five are **DL54-26 … 30**
(content unchanged), and the pass adds DL54-31 … 36. Wherever the notes above, `REVIEW.md` or `A11Y_PERF.md` say
DL54-20 / 21 / 22 / 23 / 24, read DL54-26 / 27 / 28 / 29 / 30.

### The merge of design-v5 (20 commits: the navbar «Il portico», tag `v54/w2-c1`) — first, as `7b7fcbd`

Four conflicts: `DECISION_LOG_V54.md` (the renumbering above); `templates/partials/header.html` (design-v5's
«la targa», with this family's symbol — the plate's key is `ile-key`, twice; W2-C1 had written the V4 alias `key`,
which a template may not write); `templates/partials/utility_bar.html` (design-v5's side: the entrance left the
bar); `static/css/dist/main.css` (rebuilt from the merged sources, `npm run build:css`). What the merge brought and
this family re-mapped (`41752ca`): the anti-fraud foot of a door panel and of the drawer drew `shield` — «Sécurité du
compte» since the icon system — and draws `shield-alert`; the browser mirrors check read the key in the
institutional bar and reads it on the letterhead's plate. And `3faad50`: the family's own four `ruff` findings (CI
runs `ruff check .` since the publication commits; `apps/core/icons.py`, `scripts/build_icons.py`).

### The fixes — finding → change → evidence

| Finding | Change | Evidence |
|---|---|---|
| **Review M1** — the rail says V4 meanings with the V5 drawings | `portal.services.NAV_GLYPHS = dict(icons.NAV)`; `companies.services.navigation` draws `icons.COMPANY_NAV[key]` (`c7b257c`; DL54-32). Journey `ile-steps` · Mes dossiers `folder` · Mes demandes `send` · Mes documents `document` · Mes échéances `calendar-clock` · Communications `mail` · Guichet `concierge-bell` · Academy `book-open` · Processus assignés `list-ordered` · Demandes qui me sont confiées `inbox` · Mes besoins `wrench` · Mon entreprise `building` · Analyse territoriale `map` | E/fix/pages/final/ (`log-person.json`, `log-roles.json`: the rail, the bottom bar and the drawer symbol by symbol, fr and ar, 1440 / 1366 collapsed / 390, for a person, a company, a professional, an authorised actor and a project reader); sheets `rail-person`, `rail-roles`, `bottom-drawer-person` in E/fix/pages/sheets/. On the 112 final captures `handshake`, `briefcase` and `map-pin` are drawn **0** times; `university` 10 times, all as the audience or the study pathway; `calendar` 10 times, all as a date. `test_the_rails_emit_the_registrys_symbol_for_every_entry`; `test_browser_w1_b.py` (rail, bottom bar, drawer, at their floors) |
| — the aliases after it | Each checked against who still emits it (`bcb2ef1`; DL54-32): `user` and `key` **leave** the registry and the sprite (no producer; the dev showcase's list — `apps/core/dev.py` — names symbols only now); `home` stays for `living.catalogue` and resolves to `house`, the V4 drawing renamed; `list` stays for `_requests_card` (W3-B); `globe` for the living catalogue and the pathways' defaults | the alias set pinned in `test_icons.py`; `test_no_python_producer_and_no_dev_list_emits_a_retired_v4_id`; 0 alias ids in the markup of the 112 captures |
| **Review M2** — the empty states draw a thinner hand | `components.css` §23: `stroke-width: 1.25` removed from `.empty-state__icon` — the glyph is the `.icon` rule's (`89fae78`; DL54-33) | computed stroke on the 112 captures: 1.5 px × 1 892, 1.67 px × 10 (`icon--xl`), **no 1.25 px**; `test_no_sheet_draws_a_glyph_with_a_thinner_hand_than_the_icon_rule` |
| **Review M3** — `document` means «nothing here yet» | A new symbol, `empty` — a frame drawn in dashes, four mitred corners and one dash a side (ILE drawing, utility tier; `cf5f5c7`) — is the partial's default; the pages whose domain has a glyph pass it: FAQ `circle-help`, glossary `book-a`, news `newspaper` (home and index), Forum `handshake`, «Vivre en Italie» `sprout` (`89fae78`; DL54-33). A region under its own heading (a pathway page's four sections, a topic's sheets, the profile's organisations) and a page whose domain the registry does not draw (the partners, the community) keep the neutral mark | chosen on E/fix/candidates/ (six drawings at 14–32 px, 1×, 2×, 4×, in the disc and in the box); measured E/fix/measure/`metrics.md`: 12.2 % sub-pixel space at 14 px, 0 % from 16 (floor 16), live area 19.5, the closest symbol 0.51 alike at 16 px — no twin, and 0 unregistered twins on the whole sprite. On the pages: sheets `empty-fr-1440`, `console-empty-fr`, `forum-empty` (the Forum's two states rendered from the real templates with no event, nothing written). 36 `empty` and no `document` as a default on the 112 captures; `test_the_empty_state_draws_its_space_or_the_neutral_mark_never_document_by_default` |
| **W2-C1 a11y 7** — an icon keeps its authored colour under forced colours | `components.css` §2: `@media (forced-colors: active) { .icon { color: inherit !important; background: none !important; } }` (`d4e129c`; DL54-34) | E/fix/forced/: 26 cells (13 pages × a light and a dark forced palette). Before (the merge's bundle): 502 icons, **140** not a system colour, **20** under 3 : 1 on their ground (the home's navy arrows 1.38 : 1 on a dark canvas, the footer's night ink 1.75 : 1 on a light one). After (the product as served, CSP intact): **0 / 0**, and 0 off their text's colour. Crops before / after: `forced-crops-dark`, `forced-crops-light`. Tried and refused: `forced-color-adjust: auto` (300 of 384 lose the palette), `color: CanvasText` without `!important` (72 of 384 still authored). `test_browser_w1_b.py` reads the home in both palettes and fails without the rule (checked: 2 failed with the rule cut out of the bundle) |
| **Review m1** — the living topic's glyph floats | `.icon--inline` (`components.css` §2): a glyph set in a line of text sits on that line — the reset draws every svg as a block. The topic's glyph and the pathway page's sit in their eyebrow, 16 px (`bf1b6f0`; DL54-35) | E/fix/pages/sheets/`eyebrow1-zoom` (fr and ar, 1440 and 390); final series `log-eyebrow.json` |
| **Review m3** — `handshake` is the weakest at 20 px | Floor 24 px (was 20): no seat draws it smaller — the rails no longer draw it, the Forum's empty states draw 24 px (`cf5f5c7`). A 20 px seat redraws it first | E/fix/measure/`rail-symbols-14-16-20-24px` (×6 and 4×); the floors probe on the 112 captures: 0 below a floor, measured on the glyph's content box |
| **a11y m1** — the board at phone width | The audience table's box is a named, focusable region; the journey line wraps instead of scrolling; the small labels are 12 px (`d6eb263`) | E/fix/board/`board-check.json`: axe-core 4.13 (WCAG 2.0–2.2 A/AA) **0 violations** at 1440, 1024, 768, 390 and 320 (was 2 nodes at 390); 0 text nodes under 12 px; the only side-scrolling box is the named region; 304 `<use>`, 0 unresolved |
| **a11y m2** — the row menu's faint dots | `ellipsis-vertical` draws three 1-unit squares: the 1.5 px stroke makes a solid dot of 2.1–2.8 px at every size (`cf5f5c7`) | E/fix/candidates/ (six ways to draw the dots, 1× ×3 and 2×); «Mes pièces» with a menu open: E/fix/pages/sheets/`fr-documents-menu-1440-main` |
| **a11y n1** — the audiences at 16 px against the plan's «never below 20 px» | The measured floors stand (14 / 14 / 16 / 16; the `glyph--sm` disc draws 16 px): the senior review judged them there and passed them. Recorded as a decision (DL54-35 item 4) | — |
| **a11y n5** — `DUE[""]` | The comment says what the map does: a plain due date draws `calendar`, so the rows of one list carry a glyph each or none (`cf5f5c7`) | — |

**Not fixed here, by decision.** Review m2 (the pathway rows' three markers) and m4 (the filter chips' V4 marks)
are compositions of other families: «Handed to» below.

### What the wider test runs found on the branch (nobody had run these suites on it)

Looking for exactly this, the pass ran the rest of the suite in chunks. Four things had been failing since the
implementation, all the family's doing, all fixed here:

1. `tests/i18n/test_rtl_static.py::test_previous_page_icon_points_backwards_in_both_directions` — RTL-07's guard
   pinned the V4 mechanism (the forward arrow turned by `.pagination__icon-prev`); the family's `arrow-start`
   replaced it. The guard follows the mechanism (`fa20496`).
2. `tests/frontend/test_design_preview.py::test_the_index_lists_the_foundation_s_specimen_boards` — the index links
   the icon board since it exists; the test said «non ancora» (`fa20496`).
3. `tests/i18n/test_catalogues.py` (4 tests) — the board wrapped four strings in `{% translate %}` that were not
   the product's: now the product's own words, or the board's Italian chrome (`d6eb263`).
4. `tests/compliance/test_no_personal_data_in_repository.py` — two evidence file names in these notes had the shape
   of an e-mail address (a name, an at-sign, `1x.png`): reworded above (this commit).

### Measures after

- **The sprite:** 110 symbols + 3 aliases = 113 ids (was 109 + 5), **31 049 B raw** (was 31 963; ceiling 32 768),
  6 452 B gzip; `scripts/build_icons.py --check` current; 0 registry floors below the measured floor, 0 pairs at or
  above 0.75 outside a `TWINS` group.
- **The bundle:** `main.css` **42 747 B gzip** (design-v5 at `a906d6d`: 42 645; the merged branch before the fixes:
  42 702) — 3 333 B under the 46 080 B allowance. No JS file changed.
- **The final series** (E/fix/pages/final/, the final tree): **112 captures** — public 38, the person's console 32,
  the roles 30, the eyebrows 12 — fr and ar, 1440 / 1366 / 390: 4 596 `<use>`, 1 902 visible icons, 51 distinct
  symbols, **0 unresolved, 0 below a floor, 0 alias or unknown id, 0 flip-list error, 0 console message, 0 failed
  request, 0 page scrolling sideways**, every status 200.
- **No name the registry does not know** (an unknown name draws nothing and is only logged, so a browser cannot
  see it): an in-process crawl of 156 public pages — the four languages × 39 paths, every living topic and every
  pathway among them (`crawl_unknown_icons.py`; no login, nothing written) — 6 776 `<use>`, **0 «svg_icon: no icon
  called»**; no Python producer and no list names the two retired aliases (tested).
- **Looked at** (not only probed): the rails and the drawer of five personas, fr and ar; the bottom bar; every
  empty state above; the two eyebrows; the open door panel and the phone drawer of «Il portico» (the key, the
  anti-fraud foot); «Mes pièces» with a row menu open; forced colours on a dark and a light canvas; the board at
  1440 and 390.

### Tests (lane 6, `test_ile_v5_l6`, `-p no:randomly`; every figure a completed run on the final code)

- **Non-browser, in chunks** (the whole suite, as it turned out): the frontend and documentation files 475 passed,
  1 xfailed · the page integrity audit and `apps/companies` 121 · `apps/portal` 202 · home, institutional, FAQ,
  glossary, living, partners 245 · news, pathways, the Forum's page and registration 208 · ecosystem, enquiries,
  cms, `tests/compliance` 335 · `apps/pages` 291 · `tests/i18n` 204 · academy, help desk, selection 192 ·
  orientation, security, back-office, community, the root files 441 · accounts, cases, documents 326 (3 skipped,
  as on 9 October) · the remaining apps and token files 1 115 (1 xfailed) · `test_design_preview.py` 297.
  The failures met on the way are the four above, re-run green (408 passed over the five files), and one that is the
  machine's: `test_no_source_is_newer_than_its_bundle` (the merge re-wrote JS sources, so the committed bundle's
  file time was older; it passes once the bundles are marked current, which is what CI does — no JS was rebuilt).
- **Still failing, and not this family's:** `tests/frontend/test_state_chips_carry_a_register.py`, 6 cases on the
  preview's own templates (`dp-state` read as a chip without a register) — the same 6 fail on design-v5 at `a906d6d`.
- **Browser** (`-m browser`, Chromium headless, no crash): `test_browser_w1_b.py` **4 passed** · the mirrors slice
  of `test_rtl_browser.py` **5 passed** · `test_browser_w2_c1.py`, `test_header_fits_the_narrowest_viewport.py`,
  `test_rtl_browser_nav.py`, `test_browser.py` **30 passed** · the whole `test_rtl_browser.py` and
  `apps/portal/tests/test_browser.py` **31 passed**.
- `ruff check .` clean; `manage.py check` and `makemigrations --check --dry-run` clean.
- Two background runs started with too wide a selection were stopped by hand before they ended; they are not
  evidence and no figure above comes from them. No browser run crashed.
- Not run: the suite in ONE run (an integration checkpoint's); Firefox / WebKit; a real Windows contrast theme (the
  forced palettes are Chromium's emulation); a screen reader; the 8782 performance PASS (the Performance Lead's).

### Ownership

`scripts/check_ownership.py w1-b design-v5`: 121 inside, 49 slice, 1 generated, **9 OUTSIDE** — DL54-30's four files
and five of this pass, each with its reason in **DL54-36** for the steward's manifest: `apps/portal/services.py`
(W3-A's «NAV_GLYPHS → the registry»; one assignment and an import), `apps/companies/services.py` and
`apps/core/dev.py` (nobody's), `tests/i18n/test_rtl_static.py` (one function, W1-A's file),
`tests/frontend/test_design_preview.py` (one assertion, W1-P's file). Inside a file the slice names only in part:
`components.css` §23 (one declaration, W3-E's section).

### Handed to

- **W3-A (the console shell):** (1) the rows the modules append to the rail **without a glyph** — the selection
  module's own rail (three rows), the Academy's «Mes formations», the help desk's «Désignation des professionnels»,
  the Forum governance rows: below 90rem the rail is glyph-only and such a row shows nothing; `icons.NAV` already
  holds `selection` and `helpdesk-queue`, the others need a key and a symbol each (a glyph column is all or
  nothing); (2) on the help desk's pages a professional's rail lists «Demandes qui me sont confiées» **twice** — the
  portal's row with `inbox`, then the module's own (`helpdesk.views._navigation` appends it without reading what is
  there); (3) the rail's collapse control draws `chevron-end`; the registry holds `panel-left-close` for it;
  (4) `A11Y_PERF.md` n3 (focus under the bottom bar, its current item under forced colours, 9 px at 320).
- **W3-B (the dashboard):** `_requests_card(icon="list")` is the last producer of the alias `list` (and the
  deadlines card's `icon="calendar"` says V4's meaning; the card draws `CARD`'s symbol first): when the cards read
  `icons.CARD`, `list` leaves `LEGACY` and the sprite.
- **W3-C (documents):** unchanged from §3 — `.doc-row__due-icon` is 16 px and `alarm-clock`'s floor is 20.
- **W3-E (the empty state, the secondary pages):** under forced colours the empty state's disc is gone (an icon
  paints no ground there): a ring, if the rebuilt component wants one. §23 is otherwise untouched.
- **W3-F1 (the public interior):** review m2 — the pathway rows carry a numeral, a glyph alone above the title and
  an arrow (`.pathway-list__icon` has no rule; `.icon--inline` exists now if the glyph is kept); the pathway page's
  «Étapes» timeline squeezes its labels into letter-wide columns at 1440 (on the review's captures too: not an icon
  matter); `pathways.services.DEFAULT_ICONS` still names V4 ids.
- **W3-F2:** `living.catalogue`'s icons (`home`, `globe`, …) and the model's help text («ex. home»): with them and
  the pathways' defaults, the aliases `home` and `globe` leave; the two dead `.pagination__icon-prev` rules of §22.
- **W1-C (the chips):** review m4 — the documents filter chips' V4 marks; `v3/chip.css` `.chip__g { stroke-width:
  2.6 }` is px now; the accordion's `plus` (DL54-29 item 2).
- **W2-E (the home):** `components.css` §12 `.entrance__icon { stroke-width: 1.1 }` — a dead rule that would draw
  thinner than the hand (named with its owner in `test_icons.py`); the home's news block paints its empty state's
  disc on a ground of the same tone.
- **W2-C2 / W2-A (`v5/chrome.css`) and W2-D (`v4/hero.css`):** their three forced-colours icon colours (the plate's
  key and the account glyph `CanvasText`, the door's chevron `ButtonText`, the legend's glyphs `CanvasText`) no
  longer decide — the icon inherits with `!important`; the declarations can go.
- **W1-P / W1-C / the steward:** the six `test_state_chips_carry_a_register` failures on the preview's templates
  (above), on design-v5 itself.
- **The steward, at the merge:** the nine paths into the manifest (DL54-30, DL54-36); the bundles from clean;
  `scripts/regen_design_inventory.py` finds two stale §2 weights (`components.css` 53.9 → 56.2 KB,
  `v4/workspace.css` 53.2 → 53.3 KB — inside the ± 10 % the test allows; families do not edit them);
  `capture-report.json`; `docs/qa/rtl/*.png` are written by the RTL browser file (`test_documentation.py` cites them).
- **Unchanged and others':** `A11Y_PERF.md` n2 (the skip link's ring, W1-A's m1) and n4.

### Commits of this pass

`7b7fcbd` the merge · `3faad50` lint · `41752ca` the navbar's call sites, the mirrors check · `c7b257c` the rails
(M1) · `bcb2ef1` the aliases · `cf5f5c7` the sprite (`empty`, the dots, the handshake's floor) · `89fae78` the empty
state (M2, M3) · `bf1b6f0` the eyebrow's glyph (m1) · `d4e129c` forced colours, the browser tests · `d6eb263` the
board (a11y m1) · `fa20496` the two tests that follow · `b190f8f` DS 2026 §13, DL54-31 … 36 · this commit: these notes.

### How to re-run

```
# the lane and the family's tests: §4 above. This pass's tools, in C:/tmp/ile_v5_council/.work/w1-b/w1-b-fix/:
python sessions_w1b_fix.py mint qa-doc-person qa-company demo-professionnel seed-actor qa-admin qa-fresh-person   # … revoke
python capture_fix.py <label> public person roles eyebrow     # captures, crops and one probe log per set
python forced_probe.py <label> product|before                 # forced colours, light and dark, 26 cells
python board_check.py                                         # the board: axe-core, scrolling regions, 12 px, floors
python measure_fix.py                                         # the sprite measured (floors, twins, live area)
python -m pytest -q -m browser tests/frontend/test_browser_w1_b.py
```

### Lane state at hand-over

The lane server on 8786 is stopped; the seven minted sessions are revoked on `ile_v5_l6` and the profile folder is
removed; no browser of this pass is running. The worktree is clean at the pass's last commit.
