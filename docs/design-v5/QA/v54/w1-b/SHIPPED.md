# W1-B shipped — 9 October 2026

**Semantic icon system — one ILE hand, distinct meanings.** Tag **`v54/w1-b`** (design-v5 `f53a885`); the owner's
preview on http://127.0.0.1:8780 serves it (v5-live checked out at the tag, 8780 restarted at 16:41 and verified).
Steward's merge, label `w1-b-merge`, under `DESIGN_V5_MERGE_LOCK` from 16:14.

## What shipped

- **One sprite, one hand.** `static/img/icons.svg`, built from `static/icons/src/` by `scripts/build_icons.py`:
  110 symbols (4 identity, 8 status, 61 concept, 37 utility) + 3 V4 aliases that still have a producer (`home`,
  `list`, `globe`), 31 049 B raw, 6 452 B gzip. Every glyph is a 1.5 px stroke at 14–24 px (1.67 px at 32, 2 px at
  48), square caps, miter joins, `currentcolor`. The donors' notices are in `docs/design-v5/ICON_LICENSES.md`.
- **One concept, one glyph.** The registry `apps/core/icons.py` (tiers, floors, twins, the closed flip list, the
  concept maps) is the only way a concept reaches a template; the `svg_icon` tag resolves through it, serves the
  sprite with its content hash and draws nothing for a name it does not know.
- **Distinct meanings.** Persona `person` ≠ Impresa `building` ≠ Istituzione `institution` ≠ Università `university`;
  documents ≠ a case `folder` ≠ Academy `book-open` ≠ Forum `handshake`; the mark's key for «Espace réservé»;
  `shield-alert` for the anti-fraud entries and `shield` for the account's security; `at-sign` for an e-mail address;
  the due dates calendar · clock · alarm-clock; the actors through the registry (the authority `stamp`, the authorised
  actor `badge-dot`, the project team `ile-mark`).
- **The console says the V5 meanings** (review M1): the rail, the bottom bar and the drawer of the person's and the
  company's space draw the registry's maps — the journey `ile-steps`, a case `folder`, the requests `send`, the
  deadlines `calendar-clock`, the Guichet `concierge-bell`, the Academy `book-open`, the needs `wrench`, the analysis
  `map`.
- **An empty state says which space is empty** (review M2, M3): its domain's glyph, or the neutral mark `empty` —
  never `document` by default — drawn by the one hand.
- **RTL.** Only the closed flip list mirrors (`arrow`, `arrow-start`, `chevron-end`, `logout`, `send`, `signpost`,
  `panel-left-close`); the mark, the key, the steps, the statuses and the audiences never do.
- **Forced colours.** An icon is the ink of the text beside it and paints no ground.
- **The icon board** `/__design-v5/specimens/icons/`: the audiences at 14–32 px, the domains on paper and night,
  «i cerchi», the notices, the directions LTR and RTL, every symbol with its floor.

## The merge

- design-v5 `9beb11e` (no-ff; `a906d6d` + `99cf594`). The family branch already held design-v5 (`a906d6d`): the
  pre-merge sync was a no-op.
- Ownership: the nine paths outside the slice were read in the diff, judged the family's (DL54-30, DL54-36) and written
  into `OWNERSHIP_V54.json` under w1-b, as slices wherever another family holds the file (`99cf594`); three existing
  slices name what the family wrote. `scripts/check_ownership.py w1-b design-v5`: 122 inside, 57 slice, 1 generated —
  PASS.
- Bundles rebuilt from a clean `static/js/dist` in both worktrees: on design-v5 byte-identical to the committed ones
  (`main.css` 42 747 B gzip). `scripts/regen_design_inventory.py --write`: two §2 weights (`f81f8ba`).
  `docs/qa/design/capture.py` on the lane: 43 captures, 842 icons laid out, 0 empty — the committed report, figure for
  figure, so it was not re-committed.
- Steward's files (`f53a885`): `live_status.json` — the family row, state `v5`, tag `v54/w1-b`; no surface key changes,
  because no page type's composition passes with an icon family (the pages stay «V4 + fondation»).
  `CHANGELOG_V54.md` — the new entry, and the list re-ordered newest first, as the strip's contract reads it (it shows
  the first three items; the earlier entries had been appended oldest first and are moved, not reworded).

## Where to see it — http://127.0.0.1:8780

- `/__design-v5/` — the live home under the strip; «Novità» opens on this entry. `/__design-v5/index/` lists the family
  as passed and links the board.
- `/__design-v5/specimens/icons/` — the icon board. `/__design-v5/decisioni/w1-b/REVIEW.md` — the senior review.
- `/fr/` and `/ar/` — the key on the letterhead's plate, the four audiences, the anti-fraud entries; in Arabic only the
  arrows and the chevrons mirror.
- `/fr/reseau/` (the audiences' discs) · `/fr/attention-aux-fraudes/` · `/fr/contact/` · `/fr/parcours/` and
  `/fr/parcours/salaried_work/` (the pathway's glyph on its eyebrow) · `/fr/vivre-en-italie/logement/` ·
  `/fr/faq/`, `/fr/glossaire/`, `/fr/actualites/`, `/fr/forum/` (their empty states, where a list is empty).
- Signed in through a persona of the strip: `/fr/espace-reserve/` (the rail; the bottom bar and the drawer on a
  phone), `/documents/` (the row menu, the due dates, the actors' discs), `/fr/espace-reserve/mes-echeances/`,
  `/fr/espace-reserve/communications/`, `/fr/espace-reserve/entreprise/` (the company's rail).

Checked on 8780 after the restart, by request only (no browser on the owner's server): `/fr/`, `/ar/`, `/it/`, `/en/`,
`/__design-v5/`, the index, the board and the review answer 200; of the 86 public pages the index lists, 84 answer 200
and 2 answer 404 by design (the virtual forum, closed); the 61 signed-in pages redirect to the sign-in without a
session; 3 590 `<use>` on those 86 pages, every one a symbol of the sprite, none a V4 alias, each with the sprite's
hash; the server log holds no unknown icon name and no traceback; no database connection left open.

## Tests (lane 6, `test_ile_v5_l6`; the branch with design-v5 merged in; every run completed, none crashed)

- Not in a browser — **1 146 passed, 0 failed, 0 skipped, 1 expected failure** (the showcase's strict marker, not this
  family's): the icon, sprite, SVG, static-asset, design-document, bundle-currency, showcase, preview, ownership,
  RTL-static and page-template files 699 · `tests/i18n/test_page_integrity.py` 24 · `apps/portal` and
  `apps/companies` 299 · `tests/security` 124.
- In a browser (Chromium, one at a time) — **17 passed, 0 skipped**: the mirrors slice of
  `tests/i18n/test_rtl_browser.py` 5 · `tests/frontend/test_browser_w1_b.py` 4 · `apps/portal/tests/test_browser.py` 8.
- On design-v5 after the merge and the regeneration: 273 passed (design documents, bundle currency, icons, static
  assets, SVG, ownership).
- The full suite is the integration checkpoint's (V5.5); it was not run here.

## Not done

- **Other families' compositions** (named in `NOTES.md` «Handed to»): the rows the modules append to the rail without a
  glyph, the help desk's doubled row and the collapse control (W3-A); `_requests_card(icon="list")`, the last producer
  of the alias `list` (W3-B); the 16 px due-date slot against `alarm-clock`'s 20 px floor (W3-C); the empty state's disc
  under forced colours (W3-E); the pathway rows' three markers and the V4 ids of `pathways.services.DEFAULT_ICONS` and
  `living.catalogue` — with them the aliases `home` and `globe` leave (W3-F1, W3-F2); the filter chips' V4 marks and
  the accordion's `plus` (W1-C); the arrow density of the public editorial body (W2-E, W3-F).
- **Not run:** Firefox and WebKit; a real Windows contrast theme (forced colours were Chromium's emulation); a screen
  reader; the performance PASS on 8782 (the family's own check measured no regression on the lane); a Moroccan reader
  for `ile-steps`, which never mirrors.
- **Not this family's, still open on design-v5:** six cases of `test_state_chips_carry_a_register` fail at the tag, on
  four of the preview's own templates (`_family.html`, `_row.html`, `_strip.html`, `index.html`). Those templates, the
  test and the chips registry are byte-identical at `a906d6d` and at the tag: the merge did not cause them.
