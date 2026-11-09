# V5.30 · Stream C — the authenticated platform product pass (v530-plat)

Branch `v530-plat` from `v530` (1420e1c6). The owner's V5.30 §9–§14 under the ULTRA FAST constraint: a small reusable
product toolkit on the existing models, permissions, workflows and routes — no new backend subsystem, no migration.
Plus the V5.29 baseline matrix's blocker **B3**, assigned to this stream by the orchestrator's note (7 Nov 21:45).

## §0 · The audit (one pass) and what is deferred

| Surface (role) | Model · queryset (scope) | Before | Verdict |
|---|---|---|---|
| «Communications» (every role) | `portal.Message` · `inbox(user)` (own, visible) | newest first, 10 a page, no search | **toolkit** — real fields: subject/body, read state, date |
| «Mes documents», the account's files (person) | `documents.PrivateDocument` · `documents_for(user)` (own, alive) | a table, 20 a page, no search | **toolkit** — real fields: name/description, kind, date, size; the register's `?état=` kept |
| «Mes dossiers» (person, professional, operator) | `cases.CaseFile` · `readable_by(user)` (own + live mandates) | every readable file, no narrowing | **toolkit** — state, objective, own/entrusted, reference or entrusted person's name; drawn from two files on |
| The register of pieces (person) | `documents` presenters | search, state filter, preview drawer, delete confirm (W3-C) | kept: already the toolkit's pattern (quick view = the piece drawer) |
| A need's withdrawal (company) | `companies.CompanyNeed` · WITHDRAWN terminal | a plain POST form | **destructive confirm** (the system's alert dialog) |
| Person / company dashboards | `cases.presenters.timeline` (audit trail) · `companies.NeedEvent` | no recent activity | **«Activité récente»** from that history only |
| Organisation dashboards, the company's calm bridge, empty communications | — | an arches-and-route drawing | **product-first**: the space's glyph in a disc |
| Mes demandes · company needs · help desk queue · Academy · Forum lists | Python list / E-3 group filter / staff queue | 0–4 rows per persona or their own filter | deferred (below) |

Deferred, and why: **saved views** (no preference store exists — the URL is the persistence: bookmarkable, Back-safe);
**bulk actions** (no safe batch operation in any backend: ui-ux-pro-max «Bulk Actions» rejected); «Mes demandes» (a merged
Python list of four models, 0–1 rows per persona — the spec accepts a list, so it is a declaration away), the company needs
register (its own E-3 holder filter; sector/territory would extend it — after acceptance), the help desk queue (a staff
surface, no persona), the Academy/Forum lists; the notification centre (needs an async fragment view — W2-A's hand-off);
returning «Marquer comme lue» to a filtered list (the redirect is an enumerated value, never a URL: kept).

## §1 · The toolkit's API

**Server** — `apps/portal/listing.py`: `ListSpec(name, search=, search_label=, filters=[Filter(key, label, choices,
apply, present=)], dates=DateRange(label, apply), sorts=[Sort(key, label, apply)], preserve=[…])`. `read(GET)` keeps only
the spec's keys, each value checked (a choice, an ISO day — two days put in order —, a sort key; the search folded and cut
at 80); `apply(scoped, state)` only narrows or orders the rows THE VIEW scoped (querysets or lists); `context(state,
scoped=, count=, total=, path=)` feeds the templates (chips with their removal URL, clear-all, the pagination's query,
the choices the rows hold). Specs: `portal.lists.MESSAGES`, `portal.lists.FILES`, `cases.lists.spec(user)`.
**Templates** — `components/listing/toolbar.html` (one GET form: search with the magnifier as submit, the sort, «Filtres» +
its count; the count, the chips, «Tout effacer»), `components/listing/drawer.html` + `filters.html` (the overlay system's
drawer: radios of the present choices, «Du»/«Au»), `components/listing/empty.html` (nothing matches).
**Sheet** — `portal/listing.css` (page-only, linked while the bar shows). **Module** — `static/js/src/listing.js` (the sort
applies when chosen; empty fields and the default order stay out of the URL). Without script everything works.
**Modal / drawer** — the overlay system (W2-A, `static/js/src/overlay.js`, `components/{drawer,dialog}.html`) IS the
primitive: focus contained (Tab wraps), Esc, the opener refocused, the page behind `aria-hidden` with the scrim and the
scroll lock — `show()` + the trap by its measured INP rule (CONTRACT §1), `showModal()` kept for light pages; the drawer
from the inline end (mirrors in Arabic), a full-width sheet on a phone, a fade without slide under reduced motion; the
destructive variant = `kind="alert"` (the safe answer focused, Esc = safe, the garnet outline last). No second system.

## §2 · Where it is used, and why

- «Communications» — every role reads it; search, «État» (Lues / Non lues, offered only when both exist), period, three
  orders. The band still counts the inbox's unread.
- The account's files on «Mes documents» — the document experience (§13): type (the kinds held), period, search, four
  orders; the register's `?état=` rides along; the table already stacks by its container (`_table.css`).
- «Mes dossiers» — the professional's and operator's list; one queryset, never a second rule; a person's single file
  draws no bar (SHOW_FROM = 2).
- The need's withdrawal — irreversible, so the alert dialog (the help desk closure's grammar), the reason in view.

## §3 · The dashboards

Person: «Activité récente» — the file's three latest events through `cases.presenters.timeline` (the actor a type, never a
name) in the case file's own component, «Tout l'historique» on the file; under «Mes documents», the side column spanning
its row. Company: its needs' latest events (`companies.NeedEvent`, the company's own copy of each history), each opening
its need. Institution / University: the calm panel's drawing replaced by the space's seal in a disc (also the company's
calm bridge and the empty communications) — no KPI, no invented figure; quick actions stay the existing ones (NowPanel,
«Nouveau besoin», the locked CTA) — not overloaded.

## §4 · Tool lines (real tools only)

- PROBLEM a filter bar people trust → **21st.dev** «Filter Toolbar» 35030 / «Data Table Toolbar» 39966 → DECISION chips
  «field value ×» + clear-all; search at the inline start, tools at the end; no column visibility, export or bulk bar →
  IMPLEMENTATION `components/listing/toolbar.html`.
- PROBLEM where the advanced filters live → **21st.dev** «Sheet» 35214 → DECISION a side drawer with head, scrolling body,
  pinned foot → IMPLEMENTATION the overlay system's drawer + `filters.html`.
- PROBLEM a destructive act → **21st.dev** «Alert Dialog» 702 (shadcn) → DECISION question title, consequence, safe answer
  focused, destructive last → IMPLEMENTATION `companies/partials/withdraw_dialog.html` on `kind="alert"`.
- PROBLEM nothing matches → **21st.dev** «Empty» 19750 → DECISION glyph, title, one sentence, one act — no illustration →
  IMPLEMENTATION `components/listing/empty.html`.
- PROBLEM chips and tables on a phone → **ui-ux-pro-max** (ux: «Chip Collection Reflow», «Compact Control Semantics»,
  «Table Handling», «Bulk Actions») → DECISION chips wrap, never clipped; each removal a native link named by its field
  and value; the table stacks (already); bulk rejected → IMPLEMENTATION `_listing.css` §2, the toolbar's `aria-label`.

## §5 · Security tests (P0 class)

`tests/frontend/test_listing_v530_plat.py`: for each improved list a SECOND account's rows never appear under every
combination of search × filter × period × sort (72 / 96 / 162 combinations) plus hostile values (an ORM path as a sort,
`__all__`, an SQL-like type, an impossible date, markup, `%`, 500 characters, raw `owner`/`person`/`id__gt` keys): ignored or
escaped. No new permission, no migration; CSRF on every POST (the withdrawal's form); `listing.js` writes no markup or style
(asserted); CSP unchanged (no new origin, 0 violations in the browser tests).

## §6 · Budgets

main.css 32 105 B (unchanged, ≤ 32 716) · shell.js 4 648 B (unchanged, ≤ 4 700). NEW files, recorded at their measure
(V5.20, citing V5.30): `static/js/dist/listing.js` **343 B**, `static/css/dist/portal/listing.css` **1 258 B**. Owned sheets
under their recorded ceilings: platform.css 4 941 (paid by the calm drawing's dead rules, was 4 998; ceiling 5 014),
console.css 7 995 (8 032), registers.css 2 964 (2 984). Fonts (B3): the console now fetches the base mono alone — 23 644 B
Latin (≤ 24 000), 39 772 B Arabic (≤ 40 000). Ceilings re-recorded: none.

## §7 · Tests

New: `test_listing_v530_plat.py` (spec, scoping, narrowing, chips, empty result, pagination, the dialog, the dashboards,
the calm panel, B3, budgets) · `test_listing_browser_v530_plat.py` (modal trap, Esc, refocus, inline end fr/ar, full
height, phone width, no slide under reduced motion, URL / chips / clear-all / sort / Back, the withdrawal's safe Esc).
Restated: none. Targeted batch (overlays, platform sheets, typography, documents, case file, dashboards, bundles, icons,
design docs, portal / cases / documents apps): 1 281 passed before the two fixes it found (one primary a screen; the
panels guard reading a comment), both green after. Headed Chrome (slot): 52 loads at 1440 / 1024 / 390, fr + ar —
overflow 0, console errors 0, axe 0 on the 20 changed sections; reduced motion: no translation at any frame; keyboard: the
search, the drawer contained, the focus back on «Filtres» (the first run found the drawer pushed 48 px down by the
column's flow margin — fixed, asserted). Then on the final build: bundles, sheets, typography, fonts, motion budgets and
overlays 301 passed; the confidential-material guard (private table configured) and the ownership tests 201 passed;
`ruff check .` 0, `manage.py check` 0, `makemigrations --check` no change; the catalogue 100 % in four languages; the
rendered /ar/ crawl of the changed pages (the repository's detector): 0 UI string in French — its 26 findings are the
personas' seeded records (message subjects, need titles, case items: the matrix's N7, data). Stills:
`C:/tmp/ile_v5_council/evidence/v530/plat/`.

B3 (fonts): the reference seats kept to ILE Mono's base subset — the «·» separator in the sans, «v1» in the sans (as on the
orientation result), a legal basis («art. 22») and an Academy origin as text, a request's reference and a fingerprint in
capitals; the 7 272 B extended file is no longer fetched on any persona page probed.

## §8 · Recovery verification (8 Nov 2026) and one defect found

After the usage-limit stop: branch clean; `test_listing_v530_plat.py` 23 passed; `ruff check` on the 8 changed Python modules
0; §6's figures re-measured with the guards' own method (`gzip.compress(…, 9)`): equal, main.css byte-identical to `v530`;
the 33 new msgids present in all four `.mo`, 0 fuzzy. NOT re-run: the browser module, the headed check, §7's batches.

**Fixed before the merge (8 Nov, the closure round): `.lst` now stands directly under the console bar (`calc(var(--ctx-h) + 1px)`) and above the rows' stretched links (`--z-sticky`), the table head's rule is gone (the bar's height varies as chips wrap), and `test_on_a_desk_the_bar_stays_in_reach_directly_under_the_console_bar` asserts it.** The defect as it was found:
The toolkit's two sticky rules (`_listing.css` §2, ≥ 64 rem) have no visible effect. Once the page scrolls, the console's own
sticky bar (`header.console-bar`: 0–57 px, z-index 20) covers the list's bar (`.lst`: 0–60 px, z-index 1), and the bar sits
over the files table's head (`thead th`: 0–40.5 px): search, filters and column heads all leave the view. Measured headless
on Mes documents and Communications at 1440 and 1024; Mes dossiers has the same rule, not probed. The sheet's comment «the
console has no top bar there» is wrong and no test asserts the behaviour. No overlap glitch: the page looks normal, the
requirement (V5.30 §12, «sticky header») is simply not met. Recommended: offset `.lst` by the console bar's height, drop the
table head's rule (the bar's height varies as chips wrap), assert it in the browser module. Still:
`C:/tmp/ile_v5_council/evidence/v530/plat/probe_sticky-head_fr_1440.png`.
