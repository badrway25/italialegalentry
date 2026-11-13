# W4-D part 2 — independent review

Reviewer `w4d2-review`, 27 October 2026, Opus 5.5. I built nothing on this branch. I read `git diff design-v5...HEAD`
on `v54-w4-d` at `d2a56d3` (9 commits, 43 files). Tests ran on `test_ile_v5_l9`, one pytest and one Chromium at a
time, with `-p no:randomly`. The lane server ran on 8789 (`ile_v5_l9`, reference date 3 October 2026), and the
personas used a minted session (force_login) that was revoked at the end. My scratch files live in this session's
scratchpad, outside every repository. I wrote nothing to the branch except this file, and I have not committed it.

**Verdict: SHIP_AFTER_FIXES.** The four fixes are correct and tested in both directions. Nothing is weakened and no
access is widened. Every deletion is dead, and the shared CSS is lighter only. The release notes are accurate, with
no secret, no recipe, no bridge and no confidential-material paragraph. What remains is merge-step work (the
design-v5 sync and the ownership manifest) and three minor wording points. There is no P0 and no P1.

## 1. A1: the assessment carries its pathway's sources

- **Through the real views, not the service helper.** I wrote a throw-away probe (deleted afterwards). It does this:
  `seeded` + `phase3_open`; two `PathwaySource` rows on `salaried_work`, one with an internal note; one rule walked
  to ACTIVE; a person signed in with force_login; `POST /fr/orientation/`; then every step's form posted until
  `/resultat/`. The assessment's `sources` were: the rule's source first, then «Portale Integrazione Migranti …»
  (url, `authority` = the publisher, `consulted_on` = `2026-09-30`, `reference` empty), then «Decreto flussi 2026 —
  scheda». No `note` and no `added_by` appear. The page `/fr/espace-reserve/dossiers/<ref>/pre-evaluation/<pk>/`
  lists all three in that order, with the link and «consultée le 2026-09-30». A root-level ERROR trap over the run
  recorded nothing.
- **Red before the fix.** I swapped in design-v5's `apps/cases/intake.py` for one run (restored with
  `git checkout`; the tree is clean). `tests/test_assessment_sources_w4_d.py` fails with the real defect:
  `FieldError("Cannot resolve keyword 'order' …")` logged as «pathway sources unavailable for salaried_work». With
  the fix it is green.
- **The DENY holds.** An outcome with no rule in force cites no source, the pathway's included (`if legal is None
  or not legal.findings: return collected`). The page's and the dashboard's sentences stay as they were.
  `reassess()` cites the same sources, and it still decides whether to record a new row on outcome and applied
  rules only. So assessments recorded before the fix do not set off a wave of new rows after the deployment.
- **The swallowed-exception hunt is real.** My own recorder patches `logging.Logger.callHandlers` and keeps every
  ERROR record emitted by non-test code under `apps/`. Positive control: a forced `PathwaySource` failure is
  recorded at `cases/intake.py:292`. Then `apps/cases` + `apps/orientation` (`-m "not browser"`): **314 passed, 3
  skipped** (the three skips already on design-v5: no rule in force on the seed). **7 records, all deliberate:**
  six from `test_demonstration_notice.py` (`cases/views.py:263`, hand-written snapshots that cannot be replayed),
  and one from `test_a_failure_opening_the_case_never_loses_the_result` (`orientation/services.py:427`, an injected
  ZeroDivisionError). The builder's table names the same sites.

## 2. A2–A4: correct, tested both ways, nothing widened

- **A2 (F-3).** `virtual_forum_enabled()` and `newsletter_enabled()` now also require `legal_pages_available()`.
  This only narrows. Every consumer goes through the gate: community views, `governance_services`, `cms_nav`
  `_GATE_FUNCTIONS`, `core.links`, the admin badges, `forum.services`. The rewritten tests (`test_join`, two
  newsletter tests) describe a state that can no longer exist: the legal pages open G2 together with these gates.
  The rewrites keep every no-row assertion. The new compliance file covers DENY, ALLOW, the override and «blocked
  in the console ⇒ closed». I ran `apps/community`, `apps/news`, `apps/forum`, `apps/core`, the second-factor file
  and W3-F2's content pages: **395 passed**. Then `test_cms_nav` + W3-F2's browser file: **22 passed**.
- **A3 (F-4).** allauth's element tag passes `origin` (the template name, `allauth/templatetags/allauth.py:119`),
  and `gates` is the context processor's snapshot dict, so `gates.public_forms_enabled` is a boolean (not the
  always-true `GateStatus`). The sign-in's only `p` is the invitation, so nothing else is withheld. The tests cover
  fr and ar in both states, the override, and the password-reset paragraph that stays.
- **A4 (Q-8).** `CaseAssignment.clean()` refuses a new row on a CLOSED file, read from the database. `assign()` is
  `@transaction.atomic` and locks the row with `select_for_update` first. In the admin, every field except
  `revoked_at` is read-only on change, so a grant cannot be moved onto a closed file. `assign()` is the only place
  that creates a `CaseAssignment` outside tests. The refusal is an existing msgid with a French translation. Ending
  a grant stays possible, a suspended file is assigned as before, and the operator's and administrator's 403s are
  unchanged.
- I ran the six new or changed W4-D test files: **43 passed**.

## 3. B: deletions dead, no visual regression, shared CSS lighter

- **Dead, by my own `git grep`** (docs and dist excluded): `hero_lines`, `components/hero.html` (no include),
  `--duration-reveal`, `--reveal-distance`, `--reveal-index`, `--nav-drawer-top`, `data-reveal-once`,
  `.page-home .reveal`: zero hits. The deleted `.entrances` / `.entrance*` selectors match no class in templates,
  apps, scripts or seeds. `home-entrances` and `pathway-entrance` are other classes.
- **Captures.** I exported the branch point (`96b6e96`, design-v5 when the branch forked; W4-C's later footer and
  join changes would only add noise) and compared it with HEAD. Pages: the home, the sign-in, a pathway, «Mon
  parcours» × fr, ar × 1440, 390 (touch), full page. Result: **11 of 16 identical**. Four differ only by the Arabic
  meta-row colon, closed up (intended, G-14; I looked at each). The fifth is a 3 × 4 px spot at the logo plate's
  corner on «Mon parcours» fr 1440, and the base differs from itself there on a second run: noise. HEAD captured
  twice: 16 of 16 identical.
- **Weights** (`weigh_pages.py`, design-v5 → HEAD): main.css 31 637 → 31 244; the sign-in 36 498 → 36 105; the home
  46 002 → 45 591; the console page types 39 798 → 39 405; the company dashboard 39 987 → 39 594; «Mes pièces»
  45 362 → 44 971. No ceiling was raised. The bundle-currency, design-docs, token and shim tests: **192 passed, 1
  xfailed** (`test_the_shim_is_gone`, already xfail on design-v5).

## 4. The release notes

- **Checked against the decision log:** W4-A's row against DL54-157 and DL54-158; the weights against DL54-154,
  DL54-158 and DL54-160 (31 799 → 31 244 and 39 978 → 39 405 are exact); F-8's paragraph against sec-f8; the rule
  counts (16 = 11 + 5) are held by a test against the seed.
- **Nothing a release note must not carry.** No secret, no recipe, no database bridge, no local infrastructure, no
  confidential-material paragraph. The words «bridge», «droplet» and «secret» that do appear are earlier text or the
  product's own words, not part 2's.
- **ROLLBACK.md §7** now says «at `v2.0.0`» and the tripwire pins the 39 released blob ids. W4-C adds no migration,
  so the statement survives the sync.

## 5. Things a release candidate must not carry

The added lines contain no `print(`, `breakpoint`, `pdb`, `DEBUG = True`, `console.log` or `debugger`. There is no
TODO, FIXME or XXX, and no new `skip` or `xfail`. The tree carries no `breakpoint()` or `import pdb` under `apps`,
`config`, `static/js/src` or `templates`.

## Findings

| # | Severity | Finding | Fix |
|---|---|---|---|
| M1 | major (merge step) | The branch has not merged design-v5 since W4-C landed (`3ca6579`, DL54-160). Its base is `96b6e96`. An in-memory `git merge-tree` is clean, including `RELEASE_NOTES_v2.0.0.md` and `static/js/src/console.js` (comment-only edits here, so the dist bundle is unaffected). After the sync, §1's W4-C row («*merging as this draft was completed*») and the header's «W4-C's merge … its branch's» are stale. | `git merge design-v5`. In §1, turn W4-C's row into «merged 27 Oct» and drop the header's caveat. Re-run the targeted set (the six W4-D files, the bundle-currency and design-docs tests, `apps/community`, `apps/news`, `apps/forum`). |
| M2 | major (merge step) | `scripts/check_ownership.py w4-d design-v5` reports **9** paths outside any family's slice. NOTES «For the team and the merge step» lists 6, and misses `apps/community/tests/test_join.py`, `apps/forum/tests/conftest.py` and `apps/forum/tests/test_governance_flag.py`. | The steward assigns all 9 in `OWNERSHIP_V54.json` before the merge. Correct NOTES' list. |
| m1 | minor | The release notes (§2, A1) say the assessment now cites the pathway's sources with their «publisher». The value is stored (`authority`), but no template draws `authority`, for the rules' sources or the pathway's. The page shows title, link and consultation date. | Say «title, link, consultation date» (the publisher kept in the record), or leave it for the copy packet. No new words in this build. |
| m2 | minor | `cms_nav._row_visible` (and `ContentBlock.requires_flag`) read a raw flag. A back-office menu row or block keyed `requires_flag="virtual_forum"` or `"newsletter"` would still be drawn without the legal pages and point at a 404. No seed does this, and `requires_gate` exists for exactly that. | Record it for after the release: map those two flag names to their gates in `_row_visible`, or document that editors use `requires_gate`. |
| m3 | minor | `community/admin.py`'s changelist badge «Funzionalità disattivata (flag virtual_forum)» now also shows when the flag is on and the legal pages are not published. The hint names the wrong cause. | Admin-only and an existing msgid. Record it for B1 (a sentence naming G1), or leave it as is. |

Nothing above is a defect in the four fixes themselves.
