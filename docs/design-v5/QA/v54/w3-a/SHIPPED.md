# W3-A shipped — 11 October 2026

**Platform shell — the console's rail / sidebar, bar and page frame («Tre livelli»).** Tag **`v54/w3-a`** (design-v5
`33f2b2e`, the status commit, as for the earlier families); merge commit `59bbb5c`. The owner's preview on
http://127.0.0.1:8780 serves it: v5-live checked out at the tag, 8780 restarted at 12:09 and verified. Steward's
merge, label `w3-a-merge`, under `DESIGN_V5_MERGE_LOCK` from 10:54. Reviewed once and fixed (V5.5): `REVIEW.md` and
`A11Y_PERF.md` are both SHIP_AFTER_FIXES; their majors (REVIEW M1 — a staff member's home was a person's dashboard;
A11Y M1 — the console footer's 20 px links) and the area's minors were closed in the fix pass (`NOTES.md`, «Review
fixes»). No reviewer has read the fix pass again.

## What shipped

- **One builder for every rail** (`apps/portal/services.py`: `shell_navigation(user, space, active)`, `shell_space`):
  two spaces — «Espace réservé», «Espace entreprise» — decided by the route, one rail per space with the same keys
  on every address; the Academy, the help desk, the selection module and the company space ask the builder instead
  of drawing a rail of their own. A role's registers come first under «Mon rôle»; the other space is named at the
  rail's head; «Communications d’identité» is a row for the account somebody has asked, and for no one else.
- **The rail in three levels** (`templates/partials/portal_chrome.html`, `templates/portal/partials/rail_nav.html`,
  `apps/portal/static/portal/v5/_shell.css`): the space as the line under the name, the section as a word on the
  text axis, the page as glyph + word on one axis; **«il lume»** — the current page's glyph on a lit paper disc —
  once per rail copy, no edge bar; a scroll edge at the list's end while more follows.
- **The pinned foot**: who the account is (the audience's glyph, the name → the profile), «Se déconnecter», the
  rail's control, the language by its own name (the four open above it), «Site public». One row in the four
  languages; under a person's own text spacing it wraps instead of overlapping.
- **Open from 80rem and remembered, compact (64 px) below** (`static/js/rail-pref.js`, `static/js/src/console.js`):
  `ile.rail` written on `<body>` before the first frame; nothing animates at load but the loader's release on the
  mark (W1-D); the word of a lone glyph stands beyond the rail's edge and leaves on Esc.
- **The page frame** (`templates/portal/base_portal.html`): the context bar is the page's level (the breadcrumb),
  one start edge, one page header by the frame's own rules, a console button on the control's corner, the footer as
  one line (its links 24 px, 44 under a finger), two native skip links.
- **Below 64rem the rail laid flat**: the top bar is the rail's head (the mark → the space's first page, the page's
  title, the account), the bottom bar its pages (four entries at most, the live labels whole on one line or two
  runs, «Menu» once at the reading end), the drawer the whole rail with its foot; «Menu» a link that script turns
  into a button (it still opens the drawer without script); the case file's action bar takes the four entries'
  place; 114 px of chrome in French, 103 in Arabic (V4: 113 with broken and clipped words, 174 on the case file,
  177 on «Ma situation»).
- **Where a space starts**: an account that holds a role's register (operator, administrator, professional,
  authorised actor) starts at its first register — the mark, the phone's tile, the drawer's mark —, every other
  account at the dashboard; a space's first page ends its trail on itself («Espace réservé › Tableau de bord»).
- **Arabic** mirrored (rail, tips, drawer, foot, chevrons); the mark never mirrors.
- **What left the cascade**: the platform shell's legacy blocks of `portal.css` (the V1 platform bar and footer and
  their companions) and W1-A's two patches for V4's phone bar in `v5/base.css`.

## The merge

- **The pre-merge sync.** The branch took design-v5 first (`4394387`; design-v5 was `3c288d6`, 114 commits ahead:
  W2-D's hero, W1-C's core components, the regression-1 fixes). Two conflicts in prose, both areas kept — the decision
  log (below) and DS 2026 (§2: design-v5's table with W1-C's six sheets, and the family's sentence on the two patches
  that left `v5/base.css`; §2.1: the family's `console.css` row beside W1-C's `entrance.css` row; §16: the
  `console.js` paragraph, and W1-C's sentence on `localStorage` told where `ile.rail` is written and read) —, and the
  dist files, not resolved by hand: rebuilt from a clean dist. `v5/base.css`, `tokens.css`, `test_icons.py` and
  `test_browser_w1_b.py` merged clean and were read.
- **Numbering.** W2-D's entries and W1-C's thirteen hold DL54-39 … DL54-57 on design-v5, so the family's fifteen
  entries are **DL54-58 … DL54-72** (add 19), content unchanged but for their cross-references and their two
  «Numbering» paragraphs; the index gained the fix pass's row. The code and DS 2026 cite the new numbers (`dd74dac`);
  `NOTES.md`'s closing section says how to read the old numbers in the notes, the review and the accessibility
  report. The steward's record of the merge is **DL54-73** (`2e64797`).
- **Ownership.** `scripts/check_ownership.py w3-a design-v5` listed the eleven paths the family declares (DL54-65,
  DL54-71, DL54-72); each was read in the diff and written under w3-a as a slice (`5290459`), with the slices of
  `apps/portal/services.py` and DS 2026 named as written. After it: 12 inside, 15 slice, 17 generated, and the
  manifest itself, the one steward-only path.
- **Bundles** rebuilt from a clean `static/js/dist` and `static/css/dist` in the branch (in the merge commit, and
  again after the citation commit: byte for byte the same) and in design-v5 after the merge (`884a743`; the shared
  chunks take that worktree's names). `scripts/regen_design_inventory.py --write` rewrote two figures in the branch
  (`580ea36`: `v5/tokens.css` 59.1 KB with the two scroll-edge tokens, `static/js` 20.4 KB) and finds design-v5
  current after the merge. `docs/qa/design/capture.py` was not run: it captures the home, the privacy page, the login
  and the 404 — no console page —, and nothing it captures changed (the compiled `main.css` differs from design-v5's
  by the two tokens and the three retired patch rules, all console-only).
- **Bytes** (gzip −9): `dist/main.css` 42 452 B (−9), `dist/portal/console.css` 5 292 B (+2 356),
  `dist/portal/portal.css` 2 263 B (−424): **50 007 B in the three sheets every console page loads** — 1 923 B over
  their total at `v54/w1-c`, the end of Wave 1 (48 084 B), and 147 B over the dashboard's Wave-1 allowance
  (49 860 B). Recorded as measured, under V5.5's performance rule and the area's A/B (no regression against the W1-0
  before set), in DL54-73 item 3: the console page types' ceiling is 50 007 B from here, and it does not rise.
  `dist/console.js` 2 038 B gzip (+362). `main.css` stands 3 628 B under its 45 KB ceiling.
- **Order.** The area merged before W2-A, which plan §3.2 puts first (W2-A has no branch): DL54-73 item 4.
- **One red on the merged tree, closed by keeping both areas.** W1-C's O14 lint
  (`test_o14_lint.py::test_no_template_draws_a_check_in_a_status_context`) refused the rail foot's
  `{% svg_icon space.who_icon %}`: a symbol named by a variable inside a status context, which the lint cannot trace
  to the registry. The producer now hands the registry's concept (`who_domain`, `who_key`, beside `who_icon`) and the
  foot draws it through the `concept` filter (`56be416`; DL54-73 item 5): the same symbol for every account, the
  lint as written.
- **Tests** (lane `test_ile_v5_l6`, one pytest at a time, on the branch after the sync): non-browser, before the lint
  fix — `tests/test_phase_console.py`, `tests/test_check_ownership.py`, `tests/test_regen_design_inventory.py`,
  `apps/portal`, `apps/companies`, `apps/academy`, `apps/helpdesk`, `apps/selection`, `apps/documents`, `apps/cases`,
  `tests/security`, `tests/frontend`, `tests/i18n`: **2 746 passed**, 3 skipped, 2 xfailed, **1 failed** (the O14
  lint, above; 24 min). After the fix: `test_o14_lint`, `test_console_shell_w3_a`, `test_icons`,
  `test_console_shell_stylesheets`, `tests/test_phase_console.py`, `apps/portal` — **343 passed**; `apps/companies`,
  `apps/academy`, `apps/helpdesk`, `apps/selection`, `tests/security`, `test_design_docs`,
  `test_css_bundle_is_current`, `test_frontend_bundle_is_current` — **526 passed**. Browser (headless Chromium, no run
  crashed): `test_console_shell_browser_w3_a`, `test_console_phone_browser_w3_a`, `apps/portal/tests/test_browser.py`,
  `tests/i18n/test_rtl_browser.py`, `test_browser_w1_b`, `test_loader_w1_d` — **121 passed**. On design-v5 after the
  merge and the rebuild: `test_design_docs`, the two bundle tests, `test_o14_lint`, `test_console_shell_w3_a`,
  `tests/test_check_ownership.py` — **201 passed**. Not run: the full suite (V5.5: the integration checkpoint). Logs:
  `C:/tmp/ile_v5_council/evidence/v54/w3-a/merge/`.
- `live_status.json`: the family row w3-a, state v5, tag v54/w3-a, its review as the decision; no surface key (see
  «Not done»). `CHANGELOG_V54.md`: the entry first.

## On http://127.0.0.1:8780 (all 200, no traceback, after the restart)

- http://127.0.0.1:8780/fr/ · http://127.0.0.1:8780/ar/ · http://127.0.0.1:8780/__design-v5/ — the strip names
  `v54/w3-a`; the index lists the family as passed, with its review
  (http://127.0.0.1:8780/__design-v5/decisioni/w3-a/REVIEW.md).
- **The console, desktop** — `/__design-v5/` → «Personas» → «Entrer» on «Personne avec dossier» (qa-doc-person, no
  password; the preview's sessions are read-only): http://127.0.0.1:8780/fr/espace-reserve/ (the dashboard: the night
  rail in three levels, «il lume» on «Tableau de bord», the foot with the account, «Se déconnecter», the rail's
  control, the language and «Site public»; the trail «Espace réservé › Tableau de bord»), then any entry of the rail —
  http://127.0.0.1:8780/fr/espace-reserve/mes-documents/, …/mon-parcours/, …/communications/, …/dossiers/,
  http://127.0.0.1:8780/fr/espace-reserve/guichet/ (the help desk) and http://127.0.0.1:8780/fr/espace-reserve/formation/
  (the Academy), which draw the same rail now. In Arabic: http://127.0.0.1:8780/ar/espace-reserve/ (the mirror).
- **Compact and open** — between 1024 and 1279 px wide the rail is compact (64 px, the glyphs alone; a glyph's word
  appears beside it on hover and focus); the control at the foot opens and folds it, and the choice is kept.
- **The phone** — the strip's phone frame, or a window under 1024 px: the top bar (the mark, the page's title, the
  account), the bottom bar (four entries at most and «Menu»), the drawer with the whole rail and its foot; on the
  case file (http://127.0.0.1:8780/fr/espace-reserve/dossiers/EE167596D4/) the page's action bar takes the entries'
  place.
- **The company space** — «Entreprise — Cantiere Adriatico» (qa-company):
  http://127.0.0.1:8780/fr/espace-reserve/entreprise/ — «Espace entreprise», its own rail, the way back to «Espace
  réservé» at the head, the trail «Espace entreprise › Tableau de bord».
- The staff start (an operator's or a professional's mark leading to their first register) has no persona in the
  preview — the four personas are persons and a company by design (DL54-18); it is held by the area's tests.

Checked after the restart, by request only (no browser on the owner's server;
`C:/tmp/ile_v5_council/evidence/v54/w3-a/merge/verify_8780.log`): `/fr/`, `/ar/`, `/it/`, `/en/`, `/__design-v5/`, the
index, the review and the login answer 200, and the strip names `v54/w3-a`. Through the preview's own persona switch
(qa-doc-person, then qa-company; no password; «Sortir» after each): the dashboard in fr, ar, it and en, «Mes
documents», «Mon parcours», «Communications», «Mes dossiers», the case file, the help desk, the Academy and the
company space in fr and ar — each 200, with the shell's rail, its control, the bottom bar, the drawer and the footer
in the markup, no traceback in the server's log.

## Not done

- **No surface key in `live_status.json`.** The shell is the chrome of every console page; no page type's
  composition is complete until its own family ships (the dashboard W3-B, the documents W3-C, the journey W3-D, the
  case file and the secondary pages W3-E), so the console pages stay «V4 + fondation» in the index — with the V5
  shell around them. The family row says what shipped.
- **Waiting for the overlay system (W2-A, not started):** the notification centre (popover, a sheet on phones — a
  gate item of plan §3.5 item 3), the console's account popover (V4's menu stays in the phone's top bar, its rows
  44 px under a finger), the drawer onto the overlay system (today's `<dialog>`; without script the drawer opened
  by `:target` is not modal). DL54-73 item 4.
- **Waiting for copy (B1):** the labelled 80 px compact rail (between 64rem and 80rem the default is glyphs alone),
  «Changer d'espace» as a label, the bottom bar's short labels (until then a role's bar holds three entries and
  «Menu» below 30rem, and French labels stand on two runs on most phones).
- **No control yet:** «Aller à…» for staff (plan D06) — nothing in the product to attach it to.
- **Other families' (the notes' «What is left, and whose»):** W1-B — the rail control's twin glyph for the compact
  state (`panel-left-open` is not in the sprite); W3-B — a home of staff's own (the shell sends them to their first
  register meanwhile), the empty dashboards' h1 «ESPACE RÉSERVÉ» against its locked copy, the person dashboard's
  pre-assessment panel head that overflows a phone in it / en; the accounts module (L-09) — the sign-in still lands
  operators and administrators on the person dashboard (`accounts.adapters.get_login_redirect_url`), and the account
  menu's «Espace réservé» and every producer's breadcrumb root still lead to the dashboard; W3-E / companies — in
  «Espace entreprise» the mark leads to the company dashboard even for a project reader without a company, whose
  rail does not list it; the selection workspace's last crumb says «Sélection autorisée» where its entry and h1 say
  «Processus assignés»; the Academy's pages have no «Espace réservé» level in their trail.
- **The shell's next pass:** `.console .btn { border-radius: var(--radius-sm) }` in `_shell.css` §4 is redundant
  now that W1-C's buttons draw `--btn-radius` (4 px) — as its own comment foresaw —, and in the console it also gives
  a link-styled button's ring a 4 px corner instead of W1-C's 2 px; one rule to delete.
- **`docs/ACCESSIBILITY.md`** does not name the console's rail and phone chrome yet (its keyboard model §3 and the
  rows of 1.4.10, 1.4.12, 1.4.13, 2.4.11 and 2.5.8 are W2-C1's and W1-A's slices): the facts are in DS 2026 §11.6.
- **Performance:** the Performance Lead's first-render measure on 8782 was not made — 8782 cannot be rebuilt while
  `collectstatic` refuses the console's raw entry (`console.css` imports `v5/_loader-light.css` by a path that leaves
  `STATIC_ROOT`; DL54-44 item 4, open): a deployment blocker for design-v5 as a whole, not this area's. The ceiling is
  recorded in DL54-73 item 3.
- **Not checked at the merge:** no browser on 8780 (by rule) — the console pages were checked there by request only;
  real devices, WebKit and Firefox were never run (the area's notes); `ruff check .` reports the six findings design-v5
  already has (W1-D's `apps/accounts/apps.py`, `scripts/gen_loader_light.py`), none from this area.
- **The full suite** was not run (V5.5: the integration checkpoint runs it).
