# W3-B — Dashboard and cards — notes

Family W3-B of the V5.4 plan (`docs/design-v5/V5_4_EXECUTION_PLAN.md` §3.5 item 4, §1.15, §1.18 Track T, §3.1 item 7),
worked in the owner's delivery mode (V5.5: implement → review once → fix → ship). Branch `v54-w3-b`, worktree
`C:/tmp/ile_wt/v54-w3-b`, from design-v5 at `1c001e6` (W3-A merged). Evidence outside every repository:
`C:/tmp/ile_v5_council/evidence/v54/w3-b/` (E/ below).

## Step 1/2 — the person's dashboard (implementer w3-b-impl-1, 11 October 2026)

**Lane.** Lane 6: dev server 8786 from this worktree on `ile_v5_l6` (`ILE_REFERENCE_DATE=2026-10-03`,
`DB_CONN_MAX_AGE=0`, `--noreload`, no preview flag), pytest on `test_ile_v5_l6`, one pytest and one headless Chromium
of mine at a time, with its own profile (`C:/tmp/ile_v5_council/.profiles/w3-b-impl-1/`). Signed-in pages through
sessions minted with `Client.force_login` by a scratch script outside the repository — no password used, typed or
stored — revoked at the end. Never 8780, 8782, Chrome 9222 / 9223. No browser run ended on a crash.

**Personas** (the lane's clone of the QA data): «pas encore de dossier» — `qa-fresh-person`; a file with pieces due
— `qa-person` (`E46E03B461`, oriented, seven pieces with dates, the conditions not accepted); a file with a piece to
replace — `qa-doc-person` (`EE167596D4`, draft); an advanced file — `seed-person` (`0FEEBAE3A9`, «Fase gestita da
soggetto autorizzato», an authorised actor assigned, nothing asked of the person).

### What was built

- **T1, the unified next action** (`apps/cases/services.py`, a presenter change only — DL54-75). One next action over
  every open obligation of the file — its checklist items AND the pieces it still waits for — on the precedence the
  function already had: a blocking outcome (now leading to its page), the review rung, the overdue obligation, the
  nearest date (on a tie the checklist item first, as before), the person's own open obligation (else anybody's), the
  questionnaire, nothing. A piece standing for a checklist item counts once. Pieces are read through the documents
  app's own query-time authorisation (`reader`); without a reader only the CASE access class — a title kept to the
  person and the administration never reaches a caller that does not say who is looking. The case views pass the
  reader, so the dashboard and the case name the same piece. Before T1, `qa-person`'s dashboard named an authority's
  checklist item with no date and no act while three of the person's pieces were due; now it names «Acte d’état
  civil légalisé», À remplacer, 05.11.2026.
- **F9** (`apps/portal/services.py`): the card grid is built only for the accounts that draw it (`bridge_cards`);
  a person's dashboard builds none — six presenters and their queries ran on every person's dashboard for a grid
  nobody saw. The legacy pre-assessment reads its one card alone (one presentation, tested).
- **The NowPanel** (`now_panel`): four variants chosen by the system — «à vous», «en attente d'un tiers», «rien à
  faire», «pas encore de dossier» — and an overdue date of the account that takes it over and is drawn there only.
  ONE primary, the act itself in the register's words («Déposer la pièce», «Remplacer la pièce», «Accepter les
  Conditions» where the conditions gate blocks the filing). DL54-74.
- **The page** (`templates/portal/dashboard.html`, `apps/portal/static/portal/v5/_dashboard.css` — a console partial
  imported by `console.css` after the shell, inside the app's static folder): the DOM's order h1 → NowPanel →
  journey; the NowPanel the one raised plane (W1-C's action card); the file's facts in W1-C's summary strip, beside
  the NowPanel from 64rem; «il registro» — the pieces by who holds them, the colour the group's, the shape the
  state's, the group words the catalogue's (DL54-76); every piece the person must act on with its act, then the pieces
  in somebody else's hands with who holds them; the dates and the communications as flat lists; what is secondary in
  W1-C's native disclosures (the Academy open when there is an enrolment); the account in one quiet line until W2-A's
  account popover; the owner's door in the console's one empty state, with the doorway component as drawn (DL54-77).
  The journey is W3-D's, placed and drawn still at load by one scoped rule.
- **Legacy rules deleted** (the bust rule's first remedy): the dashboard's own V4 rules in `static/css/v4/workspace.css`
  and the old account panel in `apps/portal/static/portal/portal.css`; the two dashboard-only variants nothing calls
  any more (DocumentRow `--compact`, HealthStrip `--compact`) and the journey's dashboard wrapper. DL54-78.
- **Tests**: `tests/frontend/test_dashboard_w3_b.py` (31 — T1 rung by rung, the variants, the takeover, F9, the pieces,
  the page's gate, no new copy, the partial's rules) and `tests/frontend/test_dashboard_browser_w3_b.py` (12, browser
  — the first viewport at five sizes in fr and ar, motion, planes, corners, overflow, the reading edge, forced
  colours). The dashboard's tests that pinned V4's markup and the hidden grid retargeted, intent kept.
- **Docs**: `DESIGN_SYSTEM_2026.md` §11.7 «Il cruscotto della persona», §2.1's console row, three §10 entries kept
  true; DL54-74 … DL54-78.

### The gate (plan §3.5 item 4), measured

Lane 8786, the four personas × fr / ar × 1920 × 1080, 1440 × 900, 1366 × 657, 1024 × 768, 390 × 844 (phone emulation),
plus full pages, reduced motion and forced colours: 64 drawings (`E/final/report.json`, `E/final/*.png`).

| Item | Result |
|---|---|
| one primary in the first viewport, with its piece and its date | yes on every drawing where the person has an act (`qa-person`, `qa-doc-person`, `qa-fresh-person`): 1 primary, its bottom inside the first viewport — at 1366 × 657 too; «rien à faire» draws none, as it should. The piece and its date are in the NowPanel; `qa-doc-person`'s piece has no date in the data, so none is drawn |
| no requirement id drawn twice | 0 on 64 drawings (`data-piece` counted); the NowPanel's piece is not repeated in the list |
| DOM order h1 → NowPanel → journey | yes on every drawing (no journey without a file) |
| ≤ 1 raised panel, ≤ 2 shadow values | 1 raised plane (the NowPanel); 2 values — the NowPanel's and the journey node's halo (W3-D's component) —, 1 without a file, 0 under forced colours |
| no stat card on a person's screen | none (tested) |
| the four NowPanel variants composed | yes — `qa-person` / `qa-doc-person` «à vous», `seed-person` «rien à faire», `qa-fresh-person` «pas encore de dossier»; «en attente d'un tiers» and the takeover composed in the tests (no QA account holds them today) |
| corners | 4 · 8 · full (the chips' pill and the discs) |
| nothing animates at load | 0 animations on 64 drawings (V4's journey drew six at every visit) |
| overflow · errors · CSP | 0 · 0 · 0 on 64 drawings |
| text under 14 px at 390 | 0–9 % of the characters (the gate: ≤ 35 %) |
| keyboard (fr, ar) | skip link → the NowPanel's primary → «Votre dossier» → «Voir mes documents» → each row's act (described by its piece) → the disclosures → the account's links; every stop with the 2 px ring (`E/final/keyboard-walk.txt`) |
| performance (smoke, not a benchmark) | lane dev server, unthrottled: LCP 430–445 ms with a file, 250–285 ms without; CLS 0; one long task of 56 ms in 24 loads (`E/final/perf-smoke.json`). The formal measure on 8782 is the Performance Lead's |

### §3.1 item 7 — the screen's identity carriers

- **«Il lume»** in the rail (W3-A) — the dashboard's entry lit.
- **«La soglia»** — the journey rail (W3-D's component, still at load here).
- **«I cerchi»** — every state a chip with its mark (the NowPanel's piece, every row, the file's status in the header).
- **«Il registro»** — the pieces by who holds them, 16 px marks coloured by the group.
- **ILE Mono** — the file's reference in the header.
- **The door in its one empty state** — «pas encore de dossier».
- The swap test: with the logo removed, the night rail with its lit disc, the journey's two shores and the ledger
  of state marks still say ILE; the silhouette is not «1 px border + rounded-md + grey caption» — one raised plane,
  everything else flat under hairlines.

### The value matrix (plan §1.15, `platform.md` §4.2) — what replaced personalisation

| Gesture | Person | Company | Institution | University | What the dashboard does instead |
|---|---|---|---|---|---|
| drag to reorder regions | show: the order follows legal priority, which the system knows best | show: four regions | show: no workspace yet | show | **the system orders priority**: the NowPanel's four variants, an overdue date taking it over |
| reorder with buttons | show | low | — | — | — |
| resize | show (measures designed: 8 / 4; one column on a phone) | show | show | show | the grid's own measures |
| hide / show | **harmful** for binding regions; modest for secondary ones | modest | — | — | **native disclosures for the secondary only** (the Academy, «Derniers dépôts», the pre-assessment's sources), the default picked by the server, never remembered; a binding region never folds |
| stored preference | language, e-mail notifications, the rail (all exist) | the needs filter, in the URL | — | — | **kept**: language, notifications, the rail's collapse; filters in the URL (`?état=`) |
| pin an object | — (one file) | later: a need | later | later | later, outside V5.4, for organisation and staff lists (B: the privacy text first) |

No drag, no resize, no hidden binding region: WCAG 2.5.7 / 2.1.1 alternatives, plural strings in four languages and
tests for every role would buy little where priority follows legal obligations.

### The CSS weight

`dist/portal/console.css` 5 292 → 6 935 B gzip (+1 643, the partial); `dist/main.css` −270 and `dist/portal/portal.css`
−68 (the legacy rules deleted). The console page types' three sheets: 49 941 → 51 246 B gzip (+1 305, `gzip -9` on the
committed bundles), about 1.2 KB over the ceiling DL54-73 recorded. Reported in DL54-78 under V5.5; the merge step
records the ceiling.

### Tests run (targeted, V5.5 — not the full suite)

One pytest at a time on `test_ile_v5_l6`; no run ended on a crash.

- **Non-browser** — `apps/portal`, `apps/companies`, `apps/cases`, `tests/test_phase_console.py`, `tests/security`,
  `tests/frontend/test_dashboard_w3_b.py`, `test_console_shell_w3_a.py`, `test_console_shell_stylesheets.py`,
  `test_css_bundle_is_current.py`, `test_frontend_bundle_is_current.py`, `test_design_docs.py`: **668 passed**, 3 skipped
  (the suite's own, not this step's), 0 failed. Before that, on the way: `test_o14_lint.py`,
  `test_state_chips_carry_a_register.py`, `test_icons.py`, `tests/i18n/test_rtl_static.py`, `test_v4_tokens.py`,
  `test_v5_tokens.py`, `test_css_tokens_exist.py` — green.
- **Browser** (`-m browser`, `-rs`) — `apps/portal/tests/test_browser.py`, `tests/frontend/test_dashboard_browser_w3_b.py`,
  `test_console_shell_browser_w3_a.py`, `test_console_phone_browser_w3_a.py`, `tests/i18n/test_rtl_browser.py`:
  **107 passed, 0 skipped**, 0 failed.
- **Retargeted, intent kept** (they pinned the V4 dashboard or the hidden grid): `apps/portal/tests/test_views.py` (2),
  `test_services.py` (the `_cards` helper reads `bridge_cards`), `test_review.py` (2); W3-A's
  `test_the_console_entry_is_an_import_list_the_light_sheet_first_then_the_shell` (the families' partials after the
  shell). Ruff clean on every changed Python file; every changed file LF.
- **Ownership** (`scripts/check_ownership.py w3-b design-v5`): 4 inside, 6 slice, 3 generated, **5 outside** — each
  justified in DL54-78 for the merge step to record: `apps/cases/views.py`, `apps/portal/tests/test_views.py`,
  `test_services.py`, `test_review.py`, `tests/frontend/test_console_shell_w3_a.py`.

### Copy packet for the owner

**No new microcopy was introduced**: every word on the dashboard is a catalogue string (tested). What the team would
propose once B1 signs — French drafts only; the team never translates Arabic:

1. The ledger's group words «À vous · En cours · Réglées» (plan D15, B1 item 3) — the build uses «À faire · En cours ·
   Valide», existing strings.
2. «Sans échéance» beside a piece with no date (the NowPanel draws no date fact today).
3. For «rien à faire», one sentence naming whose hands the file is in: «Votre dossier est entre les mains de :
   {intervenant}.»
4. «En attente d'un tiers» as the word of the rows in somebody else's hands.
5. A deadline's distance in words — «dans 9 jours», «en retard de 3 jours» (D17, B1 item 4).

### What is left, and whose

- **W3-B step 2**: the company dashboard and the institution / university bridge (`templates/companies/dashboard.html`,
  the bridge part of `portal.css`, the dashboard part of `companies.css`); the V4 Panel / facts / HealthStrip /
  ContextHeader rules leave `v4/workspace.css` with their last consumers (the case file — W3-E —, the company
  dashboard, «Ma situation», the documents pages — W3-C).
- **W3-D**: the journey rail's redraw (still at load — the dashboard's scoped rule then becomes redundant) and the
  `SELECTION` mapping (`seed-person`'s advanced file still sits on step 1 of the rail).
- **W3-C**: the documents page's primary through `next_action(case, reader=user)` when it is a piece (T1's third
  screen); the deadline kinds (F13); the `compact` branches left in `document_row.html` and `health_strip.html`.
- **W2-A**: the account popover — then the account's line leaves the dashboard.
- **W2-B**: `_door.css` — then the door's paint leaves `v4/hero.css`.
- **The merge step**: the five paths outside the slice (DL54-78), the CSS ceiling, the inventory tables.
- **The Performance Lead**: the dashboard on 8782 under the lock.

## Step 2/2 — the company's dashboard and the bridge (implementer w3-b-impl-2, 11 October 2026)

**Lane.** The same lane 6: dev server 8786 from this worktree on `ile_v5_l6` (`ILE_REFERENCE_DATE=2026-10-03`,
`DB_CONN_MAX_AGE=0`, `--noreload`, no preview flag), pytest on `test_ile_v5_l6`, one pytest and one headless Chromium
of mine at a time, its own profile (`C:/tmp/ile_v5_council/.profiles/w3-b-impl-2/`). Sessions minted with
`Client.force_login` by a scratch script outside the repository — no password used, typed or stored — revoked at the
end. The lane's clone holds no institution and no university account: two lane-only accounts were added for the
bridge's drawings (`w3b-institution@…`, `w3b-university@…`, unusable passwords, one organisation each, two deadlines
and a message for the institution) and deleted at the end with everything they owned (their two role grants stay in
the lane's audit trail, as an audit trail does); the nine sessions revoked; the lane server stopped. Never 8780,
Chrome 9222 / 9223. No browser run ended on a crash.

**Personas.** The company with its company — `qa-company` (`Cantiere Adriatico S.r.l.`, verified, four needs: a
complete draft, transmitted, under review, taken over by an authorised agency); the company account without a company
— `seed-company` (the declaration; on «Espace réservé» it gets the bridge); the bridge — `w3b-institution` (a deadline
overdue, one in 17 days, an unread message, its organisation), `w3b-university` (its organisation only: every other
region empty), `seed-actor` (an authorised actor, a professional account); the four persons of step 1, for the
regression.

### What was built

- **The company's dashboard** (`templates/companies/dashboard.html`; DL54-79): the person's grammar, not a second
  system. The page header without an action — «Entreprise», the legal name as the h1 (its own direction, its box on
  the reading edge), the verification as a word with its register, sector, place. **The NowPanel** — the company's one
  next action from `companies.services.next_action` (unchanged), composed by `portal.services.company_now_panel`:
  «à vous» with its ONE primary in the presenter's words («Déclarer mon entreprise», «Compléter le besoin», «Ouvrir le
  besoin», «Créer un besoin»), «en attente d'un tiers» while the project verifies the company or examines the needs
  (no primary), «rien à faire». The need the act is about lends its state chip and is drawn there only
  (`data-need`). **«Mon entreprise»** — W1-C's summary strip beside the NowPanel from 64rem: the immatriculation in
  ILE Mono, the referent (the legal name is the h1: said once), the sentence on the verification. **«Mes besoins en
  compétences»** — «il registro» of the needs by who holds them (À faire · En cours · Clos, the chips' marks coloured
  by the group), then the company's drafts with their act, then the needs in somebody else's hands with who answers
  for them, then the closed ones, five at most; «Tous mes besoins»; «Nouveau besoin» under the list. One destination,
  one stop: a draft's way to its page is its act, another need's is its title. **«Communications»**, flat. Without a
  company: the workspace head and the declaration on the NowPanel; the door stays the person's one empty state.
  `companies.css` gains nothing: the company's dashboard draws with the dashboards' partial, the sheet keeps the
  company band and the workspace's other pages (W3-E's).
- **One NowPanel** (`templates/portal/partials/now_panel.html`): extracted from the person's dashboard; the person's
  and the company's dashboards include it. `portal.services._now_base` gives both presenters the same keys.
- **The bridge** (`templates/portal/dashboard.html`, `templates/portal/partials/card.html`; DL54-80): the accounts that
  are not a person get **no NowPanel** — the system knows no next action for them, and «rien à faire» would be a claim
  it cannot make (an authorised actor's work is in «Processus assignés») —, their registers as flat sections in the
  person's grammar, the system still ordering priority: the main column first says what is due and what came in (the
  dates — an overdue one in azione, terracotta, as on the person's page, never the red of a refusal —, the
  communications), then what was sent and filed (requests, documents); the organisation stands beside, as the
  file's facts do on a person's page. Each with its domain's glyph, its word, a state worth saying as a chip («1
  en retard», «1 non lue»), its one link, its rows with date, kind and state; an empty region is one line. Then the
  person's pre-assessment section (the orientation register gives way to it: never twice) and the account's line.
  `bridge_cards` (F9) is unchanged.
- **Legacy rules deleted** (DL54-81): in `static/css/v4/workspace.css` the facts (the slice's row — their last
  consumer), the company dashboard's section, the 12-column workspace grid, the lone next step, the bridge's
  assessment panel, every rule of the needs table; in `portal.css` the bridge part (the card grid and its cards).
  **Panel, ContextHeader and HealthStrip stay**: the case file (W3-E), «Ma situation» (W3-E), «Mes pièces» and the
  register (W3-C) still draw them; deleting them here would break those pages.
- **Tests**: `tests/frontend/test_dashboard_w3_b.py` +16 (the company's NowPanel rung by rung; the needs' ledger and
  order with the NowPanel's need once; the page's gate; the four company variants; a need prepared before the
  verification, the creation offered once; Arabic; the bridge's four — its order, the university's empty lines, the
  azione chips, the pre-assessment once; the catalogue check of the company page and both partials; one NowPanel
  partial; the legacy rules gone) — 47 in all;
  `tests/frontend/test_dashboard_browser_w3_b.py` +13 (the company's primary in the first viewport at 1440 · 1024 ·
  834 · 390 in fr and ar with one plane and the need once; reduced motion + forced colours; the bridge with no plane and
  no primary at 1440 and 390 in fr and ar, a row's own words on the reading edge) — 25 in all. Retargeted, intent
  kept: W1-C's
  `test_no_stat_card_grid_on_a_persons_or_a_companys_screen` (the bridge's grid it pinned is gone) and the `_card`
  helper of `apps/portal/tests/test_views.py`.
- **Docs**: DS 2026 §11.7 «I cruscotti — la persona, l'impresa, il ponte», §2.1's console row, §10's `doorway.html`
  consumer (the NowPanel partial now), §2's row of `v4/workspace.css` (its sentence, and its weight through
  `scripts/regen_design_inventory.py --write`: 52.2 → 45.7 KB, the one stale figure); DL54-79 … DL54-81.

### The gate (plan §3.5 item 4), measured on the company's dashboard and the bridge

Lane 8786: the company (with a company, without one), the bridge (institution, university, authorised actor, a company
account without the person's role) and the four persons × fr / ar × 1920 × 1080, 1440 × 900, 1366 × 657, 1024 × 768,
834 × 1112 (the 768–1023 band), 390 × 844 and 360 × 800 (phone emulation), 844 × 390 (a phone on its side), full
pages, reduced motion + forced colours: 45 measured drawings in `E/impl2-smoke2/` and `E/impl2-smoke3/` (each
session's first load a warm-up; `E/impl2-summary.json`), 17 on the final tree in `E/impl2-final/` (the bridge's
order, the azione chips), 20 more in `E/impl2-smoke1/`.

| Item | Result |
|---|---|
| one primary in the first viewport, with its obligation (and its date when the data has one) | the company: 1 primary on every drawing where the act is the company's («Ouvrir le besoin», «Déclarer mon entreprise»), its bottom inside the first viewport at every size but a phone on its side (844 × 390: 278 px between the two bars hold the header and the NowPanel's title; the primary is one short scroll below, as on the person's); the need and its state in the NowPanel; no date — the company's next action carries none. The bridge: none, by decision (DL54-80) |
| no requirement id drawn twice | 0 on every drawing (`data-piece` and `data-need` counted): the NowPanel's need is not in the list |
| DOM order h1 → NowPanel (→ journey) | yes on every company drawing (no journey on a company's screen); the persons' as in step 1 |
| ≤ 1 raised panel, ≤ 2 shadow values | the company: 1 raised plane (the NowPanel), 1 shadow value, 0 under forced colours; the bridge: 0 and 0; the persons unchanged (1 and 2) |
| no stat card on a person's or a company's screen | none (tested, static and in the browser); nor on the bridge |
| corners | 4 · 8 · full (the chips' pill is their own 12 px, as in step 1) |
| nothing animates at load | 0 animations on every measured drawing (the warm-up load takes each session's entrance release, W1-D) |
| overflow · console errors · CSP · bad responses | 0 · 0 · 0 · 0 |
| targets under 24 px in the workspace | 0 |
| text under 14 px at 390 | 0–3.3 % of the characters (the gate: ≤ 35 %) |
| keyboard (fr and ar) | the company: skip link → the NowPanel's primary → «Voir et modifier l'identité» → «Tous mes besoins» → each need → «Nouveau besoin» → the footer; the bridge: skip link → «Toutes mes échéances» → «Toutes mes communications» → the message → «Mon profil» → the account's links → the footer; every stop with the 2 px ring (`E/impl2-final/keyboard-walk-*.txt`) |
| Arabic | mirrored; a Latin legal name, a need's title and the referent keep their direction in inline isolates, on the reading edge |
| performance (smoke, not a benchmark) | lane dev server, unthrottled, 3 measured loads a cell: the company LCP 244–284 ms, without a company 168–228 ms, the bridge 268–288 ms, the person 388–464 ms (as in step 1); CLS 0 everywhere; one long task of 54 ms in 48 loads (the person, ar) — `E/impl2-smoke2/perf-smoke.json` |

### §3.1 item 7 — the identity carriers of the two screens

- **The company's dashboard**: «il lume» in the rail (the company space's dashboard lit); «I cerchi» — every state a
  chip with its mark: the verification in the header, the NowPanel's need, every need; «il registro» of the needs,
  16 px marks coloured by the group; ILE Mono for the need references and the immatriculation; the NowPanel, the same
  raised plane as the person's. Swap test: with the logo removed, the night rail with its lit disc, the ledger of
  state marks and the mono references still say ILE; one raised plane, everything else flat under hairlines.
- **The bridge**: «il lume», «I cerchi» (each row's state: a request's, a file's scan, a deadline's «En retard», «Non
  lue», the membership's role) and the registry's concept glyphs at each register's head; the silhouette of the
  person's page without its raised plane.

### The value matrix (plan §1.15, `platform.md` §4.2) — what each persona gains, and the personalisation weighed

| Persona | What the dashboard now gives | Personalisation weighed | Done? Why |
|---|---|---|---|
| Person (step 1) | the NowPanel's four variants and the overdue takeover; the pieces by who holds them, the person's own first with their act; dates and communications flat; the secondary folded | drag or button reorder, resize, hide / show, a stored layout, pinning | **No board.** Priority follows legal obligations, which the system knows (T1); hiding a binding region would be product policy (C); drag needs WCAG 2.5.7 / 2.1.1 alternatives and four languages for little value. **Kept**: language, e-mail notifications, the rail's collapse; native disclosures for the secondary (the server's default, not remembered); filters in the URL |
| Company (step 2) | its one next action with its one primary — transmit the draft that is complete, complete the one that is not, wait for the verification — said first; its needs by who holds them, its own drafts first with their act, who answers for the others; its identity at a glance | reorder the four regions; a needs filter on the dashboard; pin a need | **No reorder**: four regions, in the order the company's work follows. **The filter** lives in the URL on «Mes besoins», the register (`?état=`), not on the dashboard. **Pinning** a need: later, outside V5.4 — the privacy text first (B) |
| Institution (step 2) | first what is due — an overdue date said by its chip — and what came in, then what it sent and filed, the organisation it belongs to beside; nothing invented | a NowPanel «rien à faire»; hiding the empty regions; reorder | **No NowPanel** — a next action the system does not know would be a claim (DL54-80). **Empty regions shown as one line** each, not hidden: a region the account can use says where things will appear. **No reorder**: the system's order — due, received, sent — is stable, and a stable order orients |
| University (step 2) | the same as the institution — today its organisation and four lines saying who fills each other region and when | the same | the same |
| Professional / authorised actor | the bridge; the work's first page is «Mon rôle» in the rail (W3-A: where the space starts) | shortcuts to the role's registers on the dashboard | **No**: the rail carries them; «Navigation rapide» repeated the rail and was not drawn (D-3) |

No drag, no resize, no stored layout, no hidden binding region, on any of the four dashboards: the system orders
priority; what is secondary folds natively; filters are URLs; the existing per-account preferences stay.

### The CSS weight — the ceiling not reached

The steward's measure (`gzip.compress(…, 9)`): the console page types' three sheets **51 308 → 50 768 B** with this
step (`dist/main.css` −376, `dist/portal/portal.css` −241, `dist/portal/console.css` +77 after consolidating the
partial); **761 B over the 50 007 B ceiling of DL54-73** (step 1 left it 1 301 over). The rows of the deletion map that
cannot leave yet weigh 624 B (Panel 175, ContextHeader and the workspace head 166, HealthStrip 181, the meter 102 —
measured by deletion), the case file's own V4 section 866 B: W3-C's and W3-E's redraws bring the console under the
ceiling. Weighed and refused: the dashboard partial as a page sheet of the three dashboards (the thirty other console
page types would drop to ≈ 49 050 B, the dashboards rise to ≈ 51 400 B, and every session — they all open on a
dashboard — would load ≈ 640 B more); cutting the dashboards' own rules. Recorded in DL54-81 for the merge step.

### Tests run (targeted, V5.5 — not the full suite)

One pytest and one browser of mine at a time, on `test_ile_v5_l6`; no browser run ended on a crash.

- **Non-browser** (`-m "not browser"`, one run) — `apps/portal`, `apps/companies`, `apps/cases`,
  `tests/test_phase_console.py`, `tests/security` (the object-permission and authorisation audits, untouched),
  `tests/frontend/test_dashboard_w3_b.py`, `test_console_shell_w3_a.py`, `test_console_shell_stylesheets.py`,
  `test_css_bundle_is_current.py`, `test_frontend_bundle_is_current.py`, `test_design_docs.py`,
  `test_chips_cards_w1_c.py`, `test_o14_lint.py`, `test_state_chips_carry_a_register.py`, `test_icons.py`,
  `tests/test_regen_design_inventory.py`: **896 passed, 1 failed**, 3 skipped (the intake suite's own: no rule in
  force), 8 deselected. The one red was this step's: `test_component_css_blocks_and_consumers_are_real` — DS §10's
  `doorway.html` still cited the dashboard template as its consumer, and the door now lives in the NowPanel partial; the
  entry follows. On the final tree, everything the late changes touch ran again — `apps/portal`, `apps/companies`,
  `tests/security`, `test_dashboard_w3_b.py`, `test_design_docs.py`, `test_css_bundle_is_current.py`,
  `test_chips_cards_w1_c.py`, `test_state_chips_carry_a_register.py`, `test_o14_lint.py`,
  `tests/test_regen_design_inventory.py`: **710 passed, 0 failed**.
- **Browser** (`-m browser`, `-rs`) — `apps/portal/tests/test_browser.py`,
  `tests/frontend/test_dashboard_browser_w3_b.py`, `test_console_shell_browser_w3_a.py`,
  `test_console_phone_browser_w3_a.py`, `tests/i18n/test_rtl_browser.py`: **120 passed, 0 skipped**, 0 failed — step 1's
  107 and this step's 13 (the company at 1440 · 1024 · 834 · 390 in fr and ar with one plane and the need once; reduced
  motion and forced colours; the bridge at 1440 and 390 in fr and ar). After the step's last changes (the azione chips,
  the rows' isolate and their reading edge) the family's files ran again — `test_dashboard_w3_b.py`,
  `test_dashboard_browser_w3_b.py`, `test_css_bundle_is_current.py`, `test_design_docs.py`: **117 passed**, 0 skipped.
- **Retargeted, intent kept**: W1-C's `test_no_stat_card_grid_on_a_persons_or_a_companys_screen` (it pinned the
  bridge's grid, now gone: no counted box on a person's or a company's screen, the bridge never a person's) and the
  `_card` helper of `apps/portal/tests/test_views.py` (a bridge register by its `data-card`). Ruff clean on every
  changed Python file; every changed file LF.
- **Ownership** (`scripts/check_ownership.py w3-b design-v5`): 6 inside, 7 slice, 3 generated, **9 outside** — step 1's
  five (DL54-78) and this step's four (DL54-81: `apps/companies/views.py`, `templates/portal/partials/now_panel.html`,
  `templates/portal/partials/card.html`, `tests/frontend/test_chips_cards_w1_c.py`), each justified for the merge step.

### Copy packet for the owner (step 2)

No new microcopy: every word on the company's dashboard, the NowPanel and the bridge's register is a catalogue string
(tested). French drafts the team would propose once B1 signs — the team never translates Arabic:

1. A total for the needs' ledger — «{n} besoins» (the ledger shows its groups' counts only).
2. «et {n} autres besoins» under the list when the company has more than five (today «Tous mes besoins» stands in).
3. For the bridge's institution or university with nothing yet, one sentence naming what the space will hold once
   their workspace opens (today each region says it in its own line).

### What is left, and whose

- **W3-C and W3-E**: Panel, ContextHeader and HealthStrip leave `v4/workspace.css` with their last consumers — «Mes
  pièces» and the register (W3-C), the case file and «Ma situation» (W3-E) —, the case file's own section with it;
  that is what brings the console page types under the ceiling (DL54-81). `companies/partials/need_table.html` is
  drawn by no page now (the dev showcase only): W3-E decides whether it goes.
- **W2-A**: the account popover — then the account's line leaves both dashboards.
- **W2-B**: `_door.css` — then the door's paint leaves `v4/hero.css` (the person's empty state).
- **The merge step**: the four new paths outside the slice (DL54-81) with step 1's five (DL54-78); the ceiling; DL54-79
  … 81 renumbered if W2-B's merge takes those numbers first; the inventory tables (DS §2's weight of
  `v4/workspace.css` already regenerated on the branch).
- **The Performance Lead**: the dashboards on 8782 under the lock.

## Review fixes (implementer w3-b-fix, 11 October 2026)

The fix pass of V5.5 (implement → review once → **fix** → ship) on `REVIEW.md` (w3-b-review) and `A11Y_PERF.md`
(w3-b-a11y-perf). Every major item fixed; every minor of W3-B fixed but one optional part (below); the items of other
families handed over. No new copy: every word is a catalogue string (tested). DL54-82.

**Lane.** Lane 6: dev server 8786 from this worktree on `ile_v5_l6` (`ILE_REFERENCE_DATE=2026-10-03`,
`DB_CONN_MAX_AGE=0`, `--noreload`, no preview flag); pytest on `test_ile_v5_l6`; one pytest and one headless Chromium of
mine at a time, its own profile (`C:/tmp/ile_v5_council/.profiles/w3-b-fix/`); every series waited on
`PERFORMANCE_BENCHMARK_LOCK` (never present). Sessions minted with `Client.force_login` by a scratch script outside the
repository — no password used, typed or stored — and revoked at the end (8 rows). Lane-only data, tagged `[w3b-fix]`
and deleted at the end: an institution and a university (unusable passwords; an overdue date and an unread message whose
subject ends in brackets and a point), an overdue date with a source note on `qa-person` (the takeover), a second date
and a message on `qa-person`, a message on `qa-company`. The server stopped; the browser closed between series. **No run
crashed.** Never 8780, 8782, 9222 or 9223. Evidence: `C:/tmp/ile_v5_council/evidence/v54/w3-b/fix/` (`smoke-a/`,
`smoke-b/`, `smoke-c/`, `inst-touch/`, each with its `report.json`). Scripts: `C:/tmp/ile_v5_council/.work/w3-b/w3-b-fix/`.

### What was fixed

| Item | The fix | Where | Seen on the lane |
|---|---|---|---|
| **M1** (review) + **2.5.3** (check, finding 2) | while the Conditions gate blocks the filing, the NowPanel's primary is «Consulter» on the piece's own page (which states the gate), the note the register's own «Acceptation des Conditions d'utilisation requise.»; the button that led to the empty terms page is gone with its `aria_label` (the partial takes none any more) | `portal.services._now_acts`, `_now_gate_note`; `now_panel.html` | `qa-person` fr / ar × 1440, 1366 × 657, 390, 360: «Consulter» / «الاطلاع» → `/documents/requirements/…/`, the note, no `aria-label`, the primary inside the first viewport |
| **M2** (review) + **finding 1** (check) | the takeover's words `dir="auto"`, the partial writes `dir` whenever the presenter sets it; `.db-now__title[dir]`, `.db-now__text[dir]` hug their box on the reading edge; `dir="auto"` on every `.db-list__title` of both dashboards (a date's title, a message's subject, a file's name); found on the way, the same defect: the pre-assessment's rationale (its final point drawn at the line's start in Arabic) and an organisation's name in the file's strip | `now_panel`, `now_panel.html`, `_dashboard.css` §2, `portal/dashboard.html`, `companies/dashboard.html` | `qa-person` ar 1440 / 390 / 320: «[w3b-fix] Rendez-vous au consulat — confirmer la date» drawn in order (its «[» left of its last letter on one line; the box 25 px from the panel's reading edge), «المصدر: Note de test (lane 6, correctifs).» with its point at the end; the lists' «[w3b-fix] Entretien (consulat de Rabat).», «[w3b-fix] Pièce reçue (passeport).», the company's «[w3b-fix] Besoin reçu (soudure).» in order; the rationale's last line ends on its point |
| **M3** (review) | `.portal__main .empty-state { max-inline-size: none; margin-inline: 0 }` restored (W3-C / W3-E retire it with their redraw) | `portal.css` | «Communications», «Mes échéances», «Mes demandes», «Mon parcours» (`qa-fresh-person`, 1440): the empty state 1128 px wide at x = 280 — the main column's box exactly |
| m1 | when the only date is the one the NowPanel took over, «Mes échéances» is not drawn (the panel holds it and the way to every date); a second date brings the section back with its link | `portal/dashboard.html` | `qa-person` with the takeover alone: no section, «Communications» in the side; with a second date: the section, its row, its link |
| m2 | «rien à faire» names the file's most recent live assignment — role — organisation (isolated) | `now_panel`, `_now_holder` | `seed-person`: «Responsable · Acteur autorisé — Agenzia Mediterranea per il Lavoro (données de test)», fr and ar |
| m3 | a piece the person answers for, filed or in review, names no party (its chip says it) | `portal/dashboard.html` | `qa-doc-person`: «Passeport… · Déposé» with no party; «Nulla osta… · Déposé · L'autorité compétente» |
| m4 (team decision) | the NowPanel carries the need page's own act: its POST form and its words «Transmettre au projet», with the need in view (title, state, reference in ILE Mono), «Ouvrir le besoin» quiet beside it; only when the account may submit (`can(user, "submit", need)`) — otherwise the link as before. DL54-82 | `company_now_panel`, `company_dashboard(…, user=)`, `now_panel.html`; `companies/views.py` passes the user | `qa-company` fr / ar × 1440, 1024, 390, 360: a `<button>` posting to `…/mes-besoins/BD1F1C30DB/transmettre/`, inside the first viewport everywhere (bottom 523 px at 1024 × 768, 638 px at 360 × 800); the test posts it and the need is «Transmis» |
| m5 | the NowPanel's title and text through W2-D's `typo` (no-break space inside « » and before : ; ! ?; never a prescribed text) | `now_panel.html` | `qa-company` 390 / 360: «Transmettez le besoin / «Soudure d'assemblage sur / charpente métallique» au projet» — the guillemet stays with its word |
| m6 + **finding 3** (check) | under a coarse pointer a list link's words are centred in its 44 px and its row's gap is 0; an empty line's link is 44 px too | `_dashboard.css` §8 | the institution at 390 touch: the link 44 px, its date 12 px under the subject (was ≈ 28); `seed-actor`'s «Commencer l'orientation» 44 px |
| m7 | the «Responsable» disc and its word in one non-wrapping group | `now_panel.html`, `_dashboard.css` §2 | `qa-company` 360: «Votre entreprise» on its disc's line (all 24 drawings) |
| m8 | the takeover's note under the catalogue's «Origine :» | `now_panel`, `now_panel.html` | «Origine : Note de test…» / «المصدر: …» |
| m9 | the company account without a company has «Communications» beside the NowPanel | `companies/dashboard.html` | `seed-company` 1440: the side at the NowPanel's row (fr: x = 1048; ar: x = 32) |
| m10 | the bridge heads its main column with one quiet link to where the account's work lives, in the rail's words; none for an institution or a university | `_bridge_space`, `portal/dashboard.html` | `seed-company` → «Espace entreprise» (`/fr/espace-reserve/entreprise/`); `seed-actor` → «Processus assignés»; 44 px on touch |
| m11 | the progress's two figures and the word between them tied by no-break spaces | `_progress_words`, `portal/dashboard.html` | `qa-person` ar 1440: «العناصر المكتملة:» / «0 من 5» — the figures on one line, every drawing |
| finding 4 (check) | the needs' end track a fixed measure, `minmax(0, 15rem)`: a late font can no longer resize the shared columns | `_dashboard.css` §5 | `qa-company`: 313 · 150 · 240 px at 1440, 158 · 150 · 240 at 1024 — the font-loaded state the auto track reached after the swap |
| finding 6 (check) | the NowPanel's region named by its eyebrow and its obligation (`aria-labelledby="db-now-eyebrow db-now-title"`) | `now_panel.html` | every NowPanel drawing |

Health on the 46 smoke drawings: 0 horizontal overflow, 0 console errors, 0 responses ≥ 400, 0 CSP reports. One
oddity, said: in the first series the institution's four touch drawings evaluated `pointer: fine` (the list link
24 px, as at a desk) while the same context's last drawing evaluated `coarse`; redrawn in a fresh touch context
(`inst-touch/`) and on `qa-person`'s phones (`smoke-b/`), the link is 44 px with its date 12 px under the subject,
and `tests/frontend/test_dashboard_browser_w3_b.py` now pins it in a fresh context.

### Not done, and why

- **Finding 4's optional part** — the person's register keeps `auto` end columns: a fixed end track there would narrow
  the pieces' titles at 1024–1440 (four columns in 8 of 12), for one shift in seven cold loads on the dev server
  (0.0144) and none on the production-shaped twin, where the font is preloaded.
- **A case's suspension reason** (its notice) stays unisolated: `components/notice.html` (W1-C) has no direction
  parameter; rare, said here.
- **Multi-line French on an Arabic page** (a takeover title at 320) wraps in its own direction inside a box that takes
  the whole width — the existing rule for a piece's title; its order and punctuation hold.

### Handed over (not W3-B's merge)

- **W3-A** — the check's finding 5: in forced colours the current rail / phone-bar entry draws the focus ring's outline
  at rest, so focus on it changes 0 pixels; show the current state another way (a border or an underline) and keep the
  outline for focus.
- **W3-C** — the register row's «Accepter les Conditions» (`components/document_row.html`) leads to the same placeholder
  terms page: the same resolution as M1 (the catalogue's «Acceptation des Conditions d'utilisation requise.», no promise
  of an act) until the G1 acceptance flow exists.
- **W3-D** — `seed-person`'s file reads «Phase gérée par un acteur autorisé» while the journey says «Vous êtes ici · 1»
  (the `SELECTION` mapping in `journey_for`, already handed over), and one fixed place for «Vous êtes ici».
- **The merge step** — the check's finding 7 and DL54-81 / DL54-82: the console page types' CSS 50 849 B gzip, 842 B over
  DL54-73's ceiling — record §2.6 item 5's once-only raise (≤ 2 KB); LCP and the first render no worse (the check's
  twin); W3-C / W3-E's planned deletions (624 B + 866 B) bring it back under.

### The weight

`gzip -9` of the committed bundles: `dist/portal/console.css` 7 012 → 7 072 B (+60), `dist/portal/portal.css` 1 954 →
1 975 B (+21); `dist/main.css` unchanged; JS unchanged. The console page types 50 768 → 50 849 B; the company's
dashboard 51 641 → 51 722 B.

### Tests run (targeted, V5.5 — not the full suite)

One pytest and one browser of mine at a time, on `test_ile_v5_l6`; no run ended on a crash.

- **Non-browser** (`-m "not browser"`) — `apps/portal`, `apps/companies`, `tests/security`, `tests/test_phase_console.py`,
  `tests/frontend/test_dashboard_w3_b.py`, `test_chips_cards_w1_c.py`, `test_o14_lint.py`,
  `test_state_chips_carry_a_register.py`, `test_css_bundle_is_current.py`, `test_design_docs.py`,
  `test_console_shell_w3_a.py`, `test_console_shell_stylesheets.py`, `test_icons.py`, `tests/i18n/test_rtl_static.py`:
  **855 passed**, 0 failed (8 deselected: browser). After the last changes (the bridge-space helper written as what it
  is; the rationale's and the strip's isolates; DS 2026 §11.7; DL54-82): `test_dashboard_w3_b.py`,
  `apps/portal/tests/test_views.py`, `test_review.py` — **122 passed**; `test_design_docs.py`,
  `test_css_bundle_is_current.py`, `test_dashboard_w3_b.py`, `tests/test_regen_design_inventory.py`, `test_o14_lint.py`
  — **164 passed**.
- **Browser** (`-m browser`, `-rs`) — `tests/frontend/test_dashboard_browser_w3_b.py`: **27 passed** (25 and the fix
  pass's 2: under a finger a list link 44 px with its date tight under its subject and an empty line's link 44 px; the
  console's empty state across the main column, fr and ar); `apps/portal/tests/test_browser.py`,
  `test_console_shell_browser_w3_a.py`, `test_console_phone_browser_w3_a.py`, `tests/i18n/test_rtl_browser.py`: **95
  passed**, 0 skipped — 122 in all, 0 failed.
- **The fix pass's tests** (`test_dashboard_w3_b.py`, 47 → 60): M1 and the name — «Consulter» and the register's note,
  nothing pointing at the terms page, no `aria-label`, fr and ar, the gate lifted gives «Déposer la pièce» back; M2 —
  the Arabic takeover's title `dir="auto"` and its note under «المصدر:» / «Origine :» (the check's «a test that draws the
  Arabic takeover and checks the attribute»), every list's own words isolated (the template's four spans, the
  rationale, the organisation); m1 — the takeover's only date leaves no section, a second brings it back with its link;
  m2 — «rien à faire» names the live assignment, the organisation isolated; m3 — a filed piece names no party; m4 — the
  need page's own form on the NowPanel, posted (the need «Transmis»), the link kept for an account that may not
  submit; m5 — a no-break space inside the title's guillemets; m9 — the company account without a company has its
  communications beside the NowPanel; m10 — «Espace entreprise», «Processus assignés», nothing for a university; m11 —
  the progress figures tied, fr and ar; finding 6 — the region's two-part name; the partial's rules (the `[dir]` hug,
  the coarse-pointer rules, the disc and its word, the needs' fixed track); M3 — the restored rule in the source and the
  bundle. Retargeted, intent kept: the one-NowPanel test (one primary, a form or a link in one if / elif — never both).
  Ruff clean on every changed Python file; every changed file LF.

### Ownership

`scripts/check_ownership.py w3-b design-v5`: 8 inside, 7 slice, 3 generated, **9 outside** — the same nine as before,
each justified in DL54-78 / DL54-81 for the merge step to record; the fix pass adds no path outside the slice
(`apps/companies/views.py`, already one of them, passes one more argument; `portal.css`'s restored rule is the one the
slice's «bridge part» deletion took).

---

## Merge step — the steward's note on numbering (11 October 2026; label w3-b-merge)

W2-B's two entries, the record of their merge and the static pipeline reached design-v5 first as DL54-74 … DL54-77,
so at the family's merge its nine entries became **DL54-78 … DL54-86** — the same order, add 4 —, content unchanged but
for their cross-references (the pre-merge sync, `3c24d67`); the index gained the fix pass's row (DL54-86), which the
branch had not written. The steward's own record of the merge is **DL54-87**. The code and DS 2026 cite none of the
moved numbers. As step 2 foresaw («DL54-79 … 81 renumbered if W2-B's merge takes those numbers first»), it did.

How to read the numbers written before the merge — in this file, `REVIEW.md` and `A11Y_PERF.md` alike, every one of
them is the family's own:

| Written | Read | The entry |
|---|---|---|
| DL54-74 | **DL54-78** | the person's dashboard: the order, the NowPanel's four variants and the takeover |
| DL54-75 | **DL54-79** | T1, the unified next action |
| DL54-76 | **DL54-80** | «il registro» on the dashboard |
| DL54-77 | **DL54-81** | the door in the console's one empty state |
| DL54-78 | **DL54-82** | step 1's paths outside the slice, the legacy rules, the CSS weight |
| DL54-79 | **DL54-83** | the company's dashboard |
| DL54-80 | **DL54-84** | the bridge |
| DL54-81 | **DL54-85** | step 2's paths outside the slice, the legacy rules, the ceiling not reached |
| DL54-82 | **DL54-86** | the fix pass |

The ranges follow: «DL54-74 … DL54-78» is DL54-78 … DL54-82; «DL54-79 … DL54-81» (and «DL54-79 … 81») is DL54-83 …
DL54-85. Every «DL54-73» is design-v5's own, unchanged — the steward's record of the w3-a merge, whose ceiling of
50 007 B DL54-76 item 5 moved to 50 086 B before this merge (the door stage's token block in `main.css`).
