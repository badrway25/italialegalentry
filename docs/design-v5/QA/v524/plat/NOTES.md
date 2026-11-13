# Lane PLAT — the platform, typography only (V5.24 final delivery; FINAL_DELIVERY_V2.md §3.7, R8; V5.29)

Label `v524-plat-build`. Worktree `C:/tmp/ile_wt/v524-plat`, branch `v524-plat`.

## §R Recovery inventory (6 Nov 2026, after the credit interruption)

Recovered, not recreated: HEAD `f17bc286` «WIP recovery: platform typography V5.27 after credit interruption» on
`4e882904` (design-v5 at the lane's cut). Nothing was reset, rebased or regenerated.

**Files already changed (source; 25 with the dist):** `apps/portal/services.py`; `apps/portal/static/portal/portal.css`;
`apps/portal/static/portal/v5/` `_dashboard.css`, `_depot.css`, `_frame.css`, `_journey-rail.css`, `_platform.css`,
`_registers.css`, `_shell.css`, `_table.css`, `_workspace.css`; `templates/portal/` `dashboard.html`,
`dashboard_organisation.html`, `organisation.html`, `partials/atrium_eyebrow.html`; tests
`apps/portal/tests/test_platform_v515_d.py` (two eyebrow regexes + the date's face, under V5.20), `tests/frontend/test_typography_v2.py`
(the portal rows of TYPOGRAPHY_BURNDOWN emptied to three residues); NEW `tests/frontend/test_platform_v524_plat.py`,
`tests/frontend/test_platform_browser_v524_plat.py`; the dist (`documents.css`, `portal/console.css`, `journey.css`,
`platform.css`, `portal.css`, `registers.css`).

**Implementation completed:** F-8 (`.ws-head__lead` and the atrium / organisation leads on `--measure-small`; the workspace
title on `--u-title-lg` with `--track-band` and `--ar-lh-plus`); F-4 (every console eyebrow / fact label / lattice label the
label role by name `t-label`, the sheets restating only the size); F-3 / §4.2 (`.lattice__figure`, `.db-next__day` on
`--u-numeral` 600 tabular in the sans; `.ring-dial__count`, `.org-refs__index`, `.reg-step::before`, `.org-id__fact time` off
the mono; `.reg-band__n` at 600; the refs stay in the mono); F-7 (every portal `:lang(ar)` descendant rule in the subject form or
deleted where the tokens already set `letter-spacing: 0` in Arabic; `.db-now__title:lang(ar)` 20/32); `portal.css`'s legacy
`--font-size-small` → `--u-ui`.

**Implementation incomplete:** (1) AR's W3.2 call — written against a guessed `displayed_text(text) -> str` with an
`ImportError` fallback; lane AR's merged helper is `displayed_text(text, language) -> (text, language)` (see defects);
(2) V5.29 not applied — SYS's merge (literal weights, ink roles) not yet in the branch, and SYS's contract item for PLAT
(`_platform.css` 4×, `_frame.css` 3× literal 600 → `--w-title` / `--w-strong`) open; (3) NOTES (this file) beyond §R;
budgets not recorded; design-v5 (cifix, AR, SYS + HOME, PUB1) not merged.

**Tests already written:** `test_platform_v524_plat.py` (static contract), `test_platform_browser_v524_plat.py` (6 browser
cases), the two amended modules above.

**Tests passing now (recovery head, run 6 Nov):** `test_platform_v524_plat.py` + `test_typography_v2.py` +
`test_platform_v515_d.py` — 287 passed; `test_platform_browser_v524_plat.py` 6 passed (headless); the four errors of
`test_typography_v2.py::test_arabic_product_sizes_leadings_and_faces` are the environment's (red on design-v5 too without
`DJANGO_ALLOW_ASYNC_UNSAFE=1`, as HOME's NOTES record) — with it, 2 passed.

**Remaining defects:** D1 `_requirement_text` would hand a tuple to the template once AR is merged (and its `!=` test would
read every line as translated) — rewrite on AR's signature, the record's language passed, the `lang` / `dir` from the
helper's returned language. D2 the SYS contract (literal 600s) and the V5.29 pass over the person / company / institution
dashboards and a document page at 1440 / 390 for heavy black / bold left by literal values. D3 budgets and notes.

## §1 What changed (on top of §R's recovered work)

1. **design-v5 merged** (cifix, AR, SYS + HOME, PUB1 — SYS first, as V5.29 orders): one conflict, T's burn-down table in
   `tests/frontend/test_typography_v2.py` — HOME's and PUB1's merged rows kept, the platform's rows the lane's three
   residues. The dist rebuilt: identical to the merged dist (two builds identical).
2. **D1 fixed — AR's W3.2 call** (`apps/portal/services.py`, `case_lines`): the guessed `_requirement_text` wrapper and its
   `ImportError` fallback deleted; the line reads `documents.services.displayed_text(text, item.language) -> (words,
   language)` (imported where the function's other documents imports are) and the row's `lang` / `dir` come from the
   returned language. One rule added because the templates (`cases/detail.html`, `cases/partials/line_dialog.html`, not
   PLAT's) give a line's title and detail ONE `lang` / `dir`: a line whose detail has no catalogue entry keeps both in the
   record's words, isolated — never French under the page's Arabic direction. The lane's two W3.2 tests rewritten on the
   real catalogue (no monkeypatch): a catalogued line reads the Arabic and carries no span; an uncatalogued or
   half-catalogued line keeps the record's words with `lang="fr" dir="ltr"`; a French page carries no span.
3. **V5.29 on the platform** (typography and colour tokens only — R8): SYS's contract item applied — `_frame.css`
   `.ctx__title`, `.ws-head__title` 600 → `--w-title`; `_platform.css` `.ctx__greeting` 500 → `--w-title`,
   `.atrium__intro > summary` 600 → `--w-control`, `.lattice__label` 600 → `--w-label`, `.org-refs__link` 500 →
   `--w-control` (the other two of SYS's «4×» had already gone with the recovered label-role conversion); V1's `--ink`,
   `--ink-2`, `--ink-3` in `_frame.css` / `_platform.css` → `--text-1/-2/-3` (same values today; the roles by name, so the
   ink roles reach the console). The numerals and figures already read `--w-title` (500 under SYS's map; TYPOGRAPHY_V2
   §4.2's 600 is now the token's business). No composition, material or icon change.

## §2 Tools → decision → change

- ui-ux-pro-max (the work order's tool for this lane: a11y and touch first) → the check that decides is «nothing under
  14 px on phones / in Arabic, weight hierarchy not bold» → kept T's Arabic guards in the browser module and added the
  role-weight ceiling (≤ 500) there, plus a static guard (no literal weight ≥ 500, no `--ink*`) over the platform's sheets.
- impeccable (typography: «hierarchy through scale + weight contrast», the method SYS applied) → the platform takes the
  map through the tokens, not by its own values → the six literal weights moved onto `--w-title` / `--w-label` /
  `--w-control`.
- No 21st component (R9); no other tool used.

## §3 Contract items applied / requests to other lanes

- Applied in PLAT's files: SYS's item (§1.3); T's token names (`--u-title-lg`, `--u-numeral`, `--measure-small`,
  `--numeric-data`, `--ar-lh-plus`, `--track-band`, `t-label`); AR's W3.2 (§1.2). PX's `attribution_required`: no
  platform template draws a credited photograph — nothing to apply.
- Requests (not fixed — other lanes' files): CLOSING — the three portal residues of TYPOGRAPHY_BURNDOWN
  (`_platform.css` `.lattice__label`'s capitals until `templates/academy/catalogue.html` carries `t-label`; `_shell.css`
  `.rail__wordmark` 12.5 px, the lock-up's size, R1; `_workspace.css` `.ws-case__ref`, the audit's seat name
  `.doc-workspace__ref` carried by no template) and `academy.css`'s `.academy-attendance__ref` (its template takes `t-ref`).

## §4 Post-acceptance candidates (seen, not fixed — R14)

- `/ar/espace-reserve/mon-organisation/` at 390: the atrium's drawing sits over the eyebrow's line at the head's top
  (composition — a preserved family; not a type defect).

## §5 Budgets (gzip -9 on the built dist; base = design-v5 at the lane's cut 4e882904; nothing raised, no ceiling re-recorded)

| sheet | base | design-v5 now | branch |
|---|---|---|---|
| main.css (≤ 32 716) | 32 695 | 32 714 | 32 714 (untouched) |
| portal/console.css (≤ 8 032) | 8 032 | 8 032 | 7 969 |
| portal/platform.css (≤ 5 014) | 5 014 | 5 014 | 4 998 |
| portal/registers.css (≤ 2 984) | 2 984 | 2 984 | 2 960 |
| portal/journey.css (≤ 2 728) | 2 728 | 2 728 | 2 726 |
| portal/situation.css (≤ 2 243) | 2 243 | 2 243 | 2 243 |
| portal/case.css (≤ 955) | 955 | 955 | 955 |
| portal/portal.css | 1 045 | 1 045 | 1 042 |
| documents/documents.css | 5 564 | 5 564 | 5 531 |
| organisation, academy, companies, helpdesk, selection | 933 · 192 · 189 · 262 · 463 | same | same |

Fonts unchanged (0 font bytes), 0 JS, **0 strings (no new msgid)**, no migration. Two builds identical; dist committed.

## §6 Checks and tests (6–7 Nov 2026, TEST_DATABASE_URL …/test_ile_v524_plat, one pytest at a time)

- Static: `test_platform_v524_plat.py` + `test_typography_v2.py` + `apps/portal/tests` (non-browser) — 535 passed; with
  `apps/documents/tests` + `test_dashboard_w3_b.py` on the merged tree — 548 passed (before the V5.29 unit).
- Browser (headless, no slot — R12): `test_platform_browser_v524_plat.py` + the browser tests of `apps/portal/tests`,
  `apps/documents/tests`, `apps/cases/tests` — 14 passed; `test_typography_v2.py::test_arabic_product_sizes…` 2 passed
  (needs `DJANGO_ALLOW_ASYNC_UNSAFE=1`, as on design-v5).
- V5.29 probe (headless; the test live server with the browser module's fixtures — person, company, institution — in
  place of a lane server on 8790, which this run did not need): the person / company / institution dashboards, «Mes
  documents» and «Mon organisation» at 1440 and 390, fr and ar — every visible text element's computed weight and
  colour: nothing at ≥ 600 but the rail's wordmark (`--w-wordmark`, the brand, R1) and the footer promoter's `<strong>`
  (`--w-strong`, emphasis); no near-black (< rgb 20) text; 0 console errors. Stills and JSON:
  `C:/tmp/ile_v5_council/evidence/v524/plat/` (20 PNG + 20 JSON).

## §7 Test changes (V5.20, each citing V5.24 / FINAL_DELIVERY_V2 §3.7 and, for the weights, V5.29)

- `apps/portal/tests/test_platform_v515_d.py` (recovered): the eyebrow regexes read `atrium__eyebrow t-label` (the same
  word, plus the role); the identity date's rule asserts `nowrap` + `--numeric-data` and NOT the mono (stronger).
- `tests/frontend/test_typography_v2.py`: the platform's burn-down rows emptied to three recorded residues (a lower count).
- The lane's own browser module: the literal `"600"` of TYPOGRAPHY_V2 §4.3 replaced by the role's weight read from the
  tokens AND a ceiling of 500 (V5.29 §6) — same invariant (the element on its role) and a stronger one.
- NEW static guard `test_the_platform_writes_no_literal_title_weight_and_no_v1_ink` over every portal sheet,
  `documents.css`, `companies.css`, `academy.css`.
- `tests/frontend/test_console_shell_browser_w3_a.py::test_the_shell_draws_two_corners_no_shadow_at_rest_and_one_edge_for_every_page_header`:
  the five console heads' title weight `"600"` → `"500"` — the consequence of SYS's contract item (the literal 600 of
  `.ws-head__title` / `.ctx__title` on `--w-title`), cited to V5.29 §5–§6 in the test; size, line and the one-edge
  invariant unchanged.

## §8 Final run on the committed head (7 Nov 2026)

- `apps/documents/tests` + `apps/cases/tests` + `test_dashboard_w3_b.py` + `test_console_shell_browser_w3_a.py` (all,
  browser included): 497 passed, 2 failed → after the amendment above, 1 red left:
  `test_il_lume_marks_the_current_page_once_per_rail_copy_and_a_lone_glyph_shows_its_word` (Lume's glyph
  `rgb(34, 47, 61)` against the literal `rgb(21, 34, 42)`) — **the base's red**: red on design-v5 31f5ceff too (SYS's
  re-valued ink; Lume is a preserved family, not PLAT's — for SYS's steward / CLOSING).
- `manage.py check` clean; `ruff check` clean; `ruff format` clean on the lane's files (the two amended shared modules
  were unformatted on the base already and are left as they were).
- The lane server on 8790 was not started (the probe used the test live server); nothing to stop.
