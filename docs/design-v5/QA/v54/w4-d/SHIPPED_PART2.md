# W4-D part 2 shipped — 27 October 2026

**Integration readiness — the last build before the release candidate. Wave 4 is complete.** Tag **`v54/w4-d`**
(design-v5 `a475095`, the status commit, as for the earlier families); merge commit `7096b37`. The owner's preview on
http://127.0.0.1:8780 serves it: v5-live checked out at the tag (`.env` unchanged), 8780 restarted at 22:34 on
27 October and verified by request (`verify_8780.log`: every request as expected, 0 failures; no traceback in the server
log). Steward's merge, label `w4d2-merge`, under `DESIGN_V5_MERGE_LOCK` (taken at 21:27:47, one attempt), on the Docker
database. Reviewed once and fixed (V5.5): `REVIEW_PART2.md` was SHIP_AFTER_FIXES with no P0 and no P1; both majors and
the cheap minors fixed in the one fix pass (`NOTES.md` «Part 2 — review fixes»). The record: DL54-155 (part 1) and
DL54-161 (part 2 and its merge).

## What shipped

W4-D composes no page: it readied the product for the release candidate, fixing in the owning families' files.

- **The questionnaire's assessment cites the pathway's sources again** (A1). `cases.intake` read three fields the
  pathway source never had; a logging guard hid the error on every completed questionnaire. The sources now come from
  the model's own fields — title, link, consultation date — after the rules' sources, and the reassessment cites the
  same; an outcome with no rule in force still cites none. Every other silent guard of the case apps was hunted: twelve
  records, all deliberate.
- **The Virtual Forum and the newsletter open only with the legal pages** (A2, part 1's F-3): the gate now enforces the
  dependency the phase console already declared.
- **The sign-in invites to the sign-up only while it is open** (A3, F-4): allauth's invitation paragraph is withheld
  while G2 keeps the sign-up closed; allauth's words, no new msgid.
- **A closed case file takes no new assignment** (A4, F-8's Q-8, CASE_LIFECYCLE §4 rule 5), checked on the locked row.
- **The rule counts follow the seed** (A5): 16 candidates, 11 drafted + 5 legacy, none in force, in the QA report and
  the rule-engine governance.
- **The rollback's tripwire pins the 39 released migrations** (A6), and ROLLBACK.md §7 speaks at `v2.0.0`.
- **The last proven-dead code out** (B): the old hero component, a filter no template read, the home's dead reveal rule,
  four legacy tokens nobody read, a dead attribute; the legacy shim's ceilings lowered (138 tokens, 2 classes).
- **W4-A's and W4-C's cheap hand-offs** (C): the meta row's colon closed up in every language, the French no-break space
  under `:lang(fr)` only (G-14); the focus ring no longer cut at the viewport's bottom edge; DS 2026's final pass,
  every inventory table current.
- **The release notes of v2.0.0 complete for the candidate** (D), the fourteen V5.10 gates left to the validation.
- **Shared CSS (V5.8)**: on the merged tree, `main.css` 31 637 → **31 244 B** gzip on every page, the console page types
  39 798 → **39 405 B**, the home 46 002 → 45 591 B.

## The merge

- design-v5 `6fddeaa` → merge `7096b37` (`--no-ff`, no conflict: the branch already held design-v5 since W4-C landed),
  `ea77197` (DL54-161), `a475095` (the status and the changelog; tag `v54/w4-d`), then this note. The inventory was
  current (no commit).
- On the branch before the merge: `0a43091` — the 9 paths in no family's slice and the 18 delegated paths assigned to
  w4-d as slices with their reasons; `f18e91f` — the two sign-in measures of W2-B's file given the open sign-up (red
  after F-4: the invitation they measured is withheld while G2 is closed), recorded as a slice.
- Ownership (`check_ownership.py w4-d design-v5 --head 0f3aded`, the area's own diff): 13 inside, 29 slice,
  2 generated — PASS; the merged diff adds the steward's slice and the manifest (steward-only, this merge's write).
  `--validate`: 30 families, 813 entries.
- Bundles rebuilt from a clean dist: byte for byte. `manage.py check` clean; `makemigrations --check`: no changes.
- Targeted tests on the merged branch (`test_ile_v5_l9`), one pytest and one Chromium at a time: **1 816 passed**,
  3 skipped (the standing intake skips), 1 xfailed (the shim's debt); browser **247 passed, 2 failed** — the two sign-in
  measures above, fixed: the entrance file and its RTL file **69 passed**. Preview, ownership, design-docs and inventory
  tests on design-v5 after the status commit: 400 passed. The full suite is the release-candidate validation's.
- Evidence: `C:/tmp/ile_v5_council/evidence/v54/w4-d/merge-part2/`.

## On http://127.0.0.1:8780

- http://127.0.0.1:8780/__design-v5/ — the strip names `v54/w4-d`; the index carries the family row w4-d and
  http://127.0.0.1:8780/__design-v5/decisioni/w4-d/REVIEW_PART2.md
- http://127.0.0.1:8780/fr/ and http://127.0.0.1:8780/ar/
- http://127.0.0.1:8780/fr/compte/login/ and http://127.0.0.1:8780/ar/compte/login/ — the invitation is drawn here
  because the preview's database has the sign-up open; on a seed with the legal pages unpublished it is withheld (A3)
- Through the preview's persona switch (`qa-doc-person`): http://127.0.0.1:8780/fr/espace-reserve/,
  http://127.0.0.1:8780/fr/espace-reserve/dossiers/EE167596D4/ and their Arabic twins

## Not done

- **After the release**: `cms_nav._row_visible` (W2-C1) and `ContentBlock.requires_flag` should resolve `virtual_forum`
  and `newsletter` through their gates; the letterhead's shift; the 149 team-written French strings beside « » : ; ? !;
  the legacy token shim's migration; W3-D's `descriptive` journey variant, `cta_panel.html`,
  `ecosystem.services.local_nav`.
- **Copy packet B1**: the Forum's back-office badge naming the legal pages when they keep the Forum closed.
- **For the owner**: F-8's Q-1…Q-7 and Q-9 (Q-8 answered by CASE_LIFECYCLE §4 rule 5, reversible); the Forum's mode and
  its words after the launch event; the Virtual Forum not before the legal pages; phase 3's authorisation; the GitHub
  settings (release notes §5).
- **Next**: the release-candidate validation (V5.10's fourteen gates, the full suite). No push, no public tag, nothing
  on `main`, nothing deployed.
- **Not run**: Playwright WebKit and Firefox (no binary on this machine), a real phone, a screen reader used by a person.
