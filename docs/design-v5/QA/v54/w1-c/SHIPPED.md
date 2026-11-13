# W1-C shipped — 11 October 2026

**Core components — buttons, fields, status chips, cards, notices, tabs.** Tag **`v54/w1-c`** (design-v5 `e0a5004`,
the status commit, as for the earlier families); merge commit `e473514`. The owner's preview on http://127.0.0.1:8780
serves it: v5-live checked out at the tag, 8780 restarted at 09:28 and verified. Steward's merge, label `w1-c-merge`,
under `DESIGN_V5_MERGE_LOCK` from 09:18. Reviewed once and fixed (V5.5): `REVIEW.md` and `A11Y_PERF.md` are both
SHIP_AFTER_FIXES; the majors (M1–M4, A1–A3, P1) and the area's minors were closed in the fix pass (`NOTES.md`,
«review fixes»). No reviewer has read the fix pass again.

## What shipped

- **Buttons** (`static/css/v5/buttons.css`): the slab on V3's property API; every primary flat (no gradient, no
  shadow); secondary, soft, ghost, danger, icon (40 px, 44 px hit area); 36 / 44 / 52 px, 44 px under a coarse
  pointer; one press gesture, nothing under reduced motion; disabled by colour, never by opacity; forced colours kept.
- **Fields «la lastra»** (`static/css/v5/field.css`, `templates/components/form_field.html`): label above, help and
  errors wired through `aria-describedby`; 52 px on public pages, 44 px in the console; the password show / hide is a
  glyph with one channel; the entrance draws no field of its own any more.
- **Status chip «i cerchi»** (`static/css/v5/chip.css`, `templates/components/chip.html`, `apps/core/chips.py`, the
  `chip` tag): a mark, a word and an edge — the state said three times, never by colour alone — with one producer;
  the 41 product templates that drew a chip by hand call it; the O14 lint holds it.
- **Cards by function** (`static/css/v5/card.css`): the record, the link, the choice — never one box for everything
  (no card board, plan §1.15).
- **Notices** (`static/css/v5/notice.css`) on the register of their message; **tabs** with one travelling indicator
  and the **disclosure** (`static/css/v5/tabs.css`).
- **What left the cascade**: `static/css/v3/buttons.css`, `static/css/v3/chip.css`, `static/css/v4/buttons.css`
  (deleted, with their imports), `components.css` §1, §3, §4, §13–§15 and §20's field rules, the pill block of
  `v4/workspace.css`, the notice block of `v4/shell.css`, the V4 input of the entrance sheet.
- **Board**: «La tavola dei chip» in the preview index (`/__design-v5/specimens/chips/`).

## The merge

- The branch already stood on design-v5's head (`a0e32b4`): `git merge design-v5` brought nothing, no conflict.
- **Ownership.** `scripts/check_ownership.py w1-c design-v5` listed 60 paths outside the slice; each is justified by
  DL54-50 and DL54-57 and was written into `OWNERSHIP_V54.json` under w1-c with its slice and reason (`b5dedc0`),
  with two more the script reads as shared (`components.css` §16, the field assertions of `test_design_docs.py`).
  After it: 0 outside; the manifest itself is the one steward-only path.
- **Bundles** rebuilt from a clean dist in the branch (no change) and again in design-v5 after the merge (`05f9d6d`;
  chunk names follow that worktree). `regen_design_inventory.py` rewrote six weights of DS 2026 §2 (`cf0cb93`).
- **Tests** (lane `test_ile_v5_l8`, one pytest at a time): `test_chips_registry`, `test_state_chips_carry_a_register`,
  `test_o14_lint`, `test_layout.py`, `apps/accounts`, `test_v5_tokens`, `test_css_bundle_is_current`,
  `test_frontend_bundle_is_current`, `test_design_docs`, `test_components_w1_c`, `test_chips_cards_w1_c`,
  `tests/security`: **1060 passed**; `tests/i18n/test_rtl_browser.py -k form`: 1 passed; on design-v5 after the
  merge, `test_design_docs` + the two bundle tests: 48 passed. Not run: the full suite (integration checkpoint).
- `live_status.json`: the family row w1-c, state v5, tag v54/w1-c; no surface key (components, no page type's
  composition changed). `CHANGELOG_V54.md`: the entry first.

## On http://127.0.0.1:8780 (all 200, no traceback, after the restart)

- http://127.0.0.1:8780/fr/ · http://127.0.0.1:8780/ar/ · http://127.0.0.1:8780/__design-v5/
- the fields and buttons: http://127.0.0.1:8780/fr/compte/login/ · http://127.0.0.1:8780/ar/compte/login/ ·
  http://127.0.0.1:8780/fr/compte/signup/ · http://127.0.0.1:8780/fr/contact/ ·
  http://127.0.0.1:8780/fr/entreprises/recueil-des-besoins/ · http://127.0.0.1:8780/fr/orientation/
- the chips and cards: http://127.0.0.1:8780/__design-v5/specimens/chips/ · http://127.0.0.1:8780/fr/parcours/ ·
  http://127.0.0.1:8780/fr/parcours/salaried_work/ · signed-in console pages (documents, cases, selection,
  governance) through the preview's personas.

## Not done

- No browser pass at the merge: the signed-in console pages were not re-checked by the steward (the area's browser
  tests passed on the branch before the merge, 24 passed per `NOTES.md`).
- The specimen boards «La serie dei bottoni» and «La serie dei campi» have no template (unlinked in the index; 404).
- Handed to other families (NOTES.md «Handed to»): «En retard» still drawn as a refusal until W3-C changes the
  producer to `overdue`; `SCAN_BADGES` beside the registry (W3-C); the inline space between paired buttons (W3-B,
  W2-A, W3-F1); the console's fixed bar over the focus at phone width (W3-A); the showcase rows for soft / icon
  buttons and the extra field states (`templates/dev/showcase.html`, next family that edits it).
- The 2.59 : 1 ring beside its halo on public text fields: a token change through the steward (laguna-600), open.
