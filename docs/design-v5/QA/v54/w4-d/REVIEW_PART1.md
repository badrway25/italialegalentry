# W4-D, part 1 — release engineering: independent review

16 October 2026 · w4d1-review (reviewer; built nothing) · branch `v54-w4-d` at `a3b6cc7` (five commits), from
design-v5 `0a8351b` · the owner's V5.10 (the release decision), V5.9 (never deploy, never name the server), V5.5 (one
review, then fix, then ship).

**Verdict: SHIP_AFTER_FIXES.** Nothing blocks.

- **CI.** The matrix is correct. Both runs will start, and each one means what its name says.
- **Deployment documents.** The runbook, the checklist and ROLLBACK.md name the same release, the same reference tag
  and the same restore rule.
- **Go-live calendar.** `GO_LIVE_PHASE.md` holds against the real calendar, checked on a lane server with today's
  clock.
- **Release notes.** Their figures match their sources.

There are two major findings, both in the documents, and each is a few lines to fix:

- ROLLBACK.md §7's migration re-check uses a pathspec that matches no file, so it can never report a difference.
- The runbook and the checklist now set two different bars for PRODUCTION_READY.

There are five minor findings. No re-review is needed: the fixes are proved by the targeted tests and by one pathspec
control.

## How it was checked

- **Read first:** V5.10, V5.9 and V5.5 with their addenda; the whole diff `design-v5...HEAD` (11 files, +935 / −43);
  `NOTES.md`.
- **CI:**
  - I parsed the YAML. Each `${{ … }}` sits where GitHub allows the `matrix` context: the job name, the service
    image, `with` and `env`.
  - I ran the new step exactly as written against the shared PostgreSQL 17. With `PG_MAJOR=17` it exits 0; with
    `PG_MAJOR=16` it exits 1 with `AssertionError: 17`.
  - I re-resolved the install line myself (pip 26.2.1, `--dry-run --report`, manylinux x86_64 wheels only, Python
    3.12 and 3.13). Each version resolves to 67 distributions, the constraints keep all 19 pins, and no source
    distribution is needed.
  - No 3.13-only library call exists in the tree, and no test skips by Python version.
  - setup-python's pip cache key contains the interpreter version, so each run keeps its own cache.
  - GitHub's changelog confirms the `ubuntu-latest` notice the workflow quotes (17 September 2026: Ubuntu 26.04
    rolls out gradually from 19 October to 19 November).
- **Documents and tests:**
  - **Bash syntax.** I extracted every bash block from the three documents (38 + 3 + 6 = 47) and ran `bash -n` with
    Git Bash: 0 errors.
  - **Tests.** `tests/deployment` and the calendar test: **100 passed** in 61.9 s (`TEST_DATABASE_URL=…/ile_v5_l9`,
    `-p no:randomly`, one pytest at a time). `ruff check` and `ruff format --check` are clean on the three test
    files.
  - **Commit hygiene.** `git diff --check` is clean, no changed file has a CR byte, and all five commits carry the
    trailer.
  - **Release facts, read-only.** I checked these in the publication repository and on GitHub:
    - `a3ac318`'s full SHA is `a3ac318304beb4504134762bfa6e9c4e4ce600f1`, and it is the root commit of design-v5's
      published history.
    - GitHub today has `main` = `a3ac318`, `design-v5` = `e6873ba` and no tag.
    - `a3ac318`'s tree is local `2b16eb3`'s (`bb57c0b`).
    - Both trees hold 39 numbered migration files, and no migration differs between `2b16eb3` and `0a8351b` (checked
      with a pathspec that works and with a grep of the full diff).
    - Neither F-8, W4-A nor W4-C adds a migration today.
  - **Checklist A-2.** I checked its `ls-remote` command on a throwaway repository with one annotated and one
    lightweight tag. The plain line and the `^{}` line read exactly as the checklist says.
- **Go-live calendar:**
  - **The server.** A lane server on `127.0.0.1:8789`: development settings, DEBUG on, `ILE_REFERENCE_DATE` empty,
    the real clock (16 October 2026, 10:20–10:23, Rome).
  - **(a) The lane database as it is.** `ile_v5_l9` is a QA copy whose flags were set by hand: `phase3_public`,
    `forum_permanent_mode`, `newsletter` and `forms_override_without_legal` are on. This is the document's §2.2
    state.
  - **(b) A fresh deployment.** A throwaway `ile_v5_l9_review`, built the way a deployment starts: `migrate`, then
    `seed_all` with `ILE_SEED_DEMONSTRATION_DATA=0`. Its only flag row is `newsletter`, off. This is §2.1.
  - **What I probed.** In each state, eleven paths, plus every internal link of eight pages in state (b).
  - **Cleanup.** The throwaway database is dropped, the copy of the media library the seed wrote into the worktree is
    removed, and the server is stopped.
- **Release notes:** I traced every figure to its source:
  - `live_status.json`: the 18 family rows and the 75 surfaces.
  - The W1-0 baseline, `C:/tmp/ile_v5_council/evidence/v54/w1-0/before/README.md`: the CSS «before» column.
  - The families' `A11Y_PERF.md` files: the JavaScript «before» column.
  - DL54-154 items 4 and 5: every «after» figure.
  - DL54-41 and DL54-44: the 43 933 B peak.
  - DL54-131: checkpoint 3's 5 108 and 519 tests and its three fixes.
  - DL54-130, DL54-132 and DL54-152: the dates of F-5, F-7 and the NUL guard.
  - The code: `core.E001`, `core.W001`–`W003`, `/healthz/` with `SELECT 1`, TOTP only.
  - GitHub, read with `gh api` and `ls-remote`: public, wiki enabled but no wiki repository, Dependabot alerts and
    automated fixes off, secret scanning and push protection on, no protected branch, no ruleset.
- **Hard limits:** I scanned all 935 added lines:
  - no IP address, no server name, no e-mail address, no secret, no personal name;
  - the only domains are `github.com` (the repository's address, already in the documents) and `schema.org`.

## The brief's checks

| Check | Result |
|---|---|
| **(1) Both matrix jobs run** | Yes. A matrix made only of `include` gives two jobs. `fail-fast: false` sits under `strategy`. |
| The service image per job | `postgres:${{ matrix.postgres }}-alpine`, which gives `postgres:16-alpine` / `postgres:17-alpine`. The `matrix` context is allowed in `services.<id>.image`. |
| `DATABASE_URL` / `TEST_DATABASE_URL` ports | Unchanged: `127.0.0.1:5432`. Each job has its own runner and its own service container, so the two runs cannot collide. The runner's own PostgreSQL is stopped by default, and the new step would catch a wrong major. |
| The Python version per job | `python-version: ${{ matrix.python }}`, from the strings `"3.12"` and `"3.13"` (no float trap). |
| The constraints | `pip install -r requirements/dev.txt -c requirements/constraints.txt`. I re-resolved it for both versions: 67 distributions, 19/19 pins, wheels only. |
| The job names | They expand to «Python 3.12 · PostgreSQL 16 (production target) — check · migrations · ruff · pytest» and «Python 3.13 · PostgreSQL 17 (development) — …». The job id `test` is unchanged. GitHub has no branch protection and no ruleset, so no required check breaks. |
| Caching per Python version | Yes. setup-python's key is OS, architecture, OS version, Python version, package manager and the hash of `requirements/*.txt`. The constraints file is part of that hash. |
| YAML or expression errors | None. |
| Could the 3.12 job pass vacuously? | No. Every step is unconditional, there is no `continue-on-error`, and both runs use the same pytest selection. No test skips by Python version: the only `importorskip` calls are in browser files, which both runs exclude. The version step fails on a wrong PostgreSQL major, and setup-python fails if 3.12 is missing. One caveat: «production target» means the server's major versions (m2). |
| **(2) The three documents agree with each other and with V5.10** | Yes on four points: the tag names, `main` promoted by fast-forward (`a3ac318` is design-v5's root on GitHub), the reference tag that is never a server rollback, and a downgrade being a restore. Two exceptions: **M1** (the re-check command) and **M2** (PRODUCTION_READY). |
| No server name, secret or confirmed domain | None (scan above). `example.com` is still the runbook's placeholder. |
| `bash -n` | 47 of 47 blocks parse. |
| The runbook tests | 100 passed. |
| **(3) GO_LIVE_PHASE.md against the real calendar** | It holds. See the table below. Every flag the code reads (seven) appears in §1. F-3 is confirmed in the code. One completeness gap: m5. |
| **(4) The release notes** | Accurate, with two exceptions: m1 (the rule counts) and m4 (where the policy paragraph is published). F-8 is marked «pending F-8's merge». The fourteen gates map one-to-one to V5.10's list. No secret and no personal datum. |

### The go-live probe — 16 October 2026, real clock

| Page | (b) Fresh deployment — §2.1 | (a) QA flags — §2.2 | Document |
|---|---|---|---|
| `/fr/` | 200. The interim hero (`data-hero-variant="interim"`): «Un écosystème pour les parcours réguliers vers l'Italie», «Orientation · Formation · Mobilité régulière», «Découvrir le questionnaire d'orientation», «Espace entreprises». No `data-banner="forum"` and no link to the registration. «v2.0.0 — Fase 1». | 200. The Phase 3 hero, no banner. | ✓ |
| `/fr/forum/` | 200. «Événement institutionnel» and «Rovigo — 2 octobre 2026». The registration chapter is there but closed (`data-registration="closed"`, «Les inscriptions sont closes.»). No registration button and no form. The schema.org `Event` is present (F-5). No Virtual Forum teaser. F-1's three sentences. No countdown. | 200. «FORUM PERMANENT VÉNÉTIE–MAROC», «Espace permanent de dialogue et de coopération», «Rencontre de lancement». No registration chapter and no `Event`. F-1's sentences. | ✓ |
| `/fr/forum/inscription/` | Closed, no form. | Closed, no form. | ✓ |
| `/ar/forum/` | The dated line carries `lang="fr"`; registration closed. | `lang="fr"`. | ✓ |
| Institutions, Universités, Projet pilote, FAQ | 404 × 4 | 200 × 4 | ✓ |
| `/fr/forum-virtuel/` | 404 | 404 (flag off) | ✓ |
| `/fr/compte/login/` · `/fr/compte/signup/` | F-4's sentence is on the sign-in page; the sign-up answers «Inscriptions fermées». | The sentence is there; the sign-up is open, because of the QA override (not a deployment state). | ✓ F-4 |
| Internal links | 40 distinct links from eight pages, all 200. | — | ✓ (the document's 113 come from more pages) |

## Findings

### Major

**M1 — ROLLBACK.md §7's migration re-check can never report a difference.**

- **Where.**
  - ROLLBACK.md §7: `git diff --name-status pre-v5-main-2026-10 v2.0.0 -- 'apps/*/migrations/'`, introduced with «this
    prints nothing when no migration differs».
  - `tests/deployment/test_release_tags_w4_d.py:109` pins that exact string.
  - `NOTES.md` §2 proves «no migration differs today» with the same pathspec.
- **Why it fails.** When a pathspec contains a wildcard, git matches it against the whole path. `'apps/*/migrations/'`
  therefore asks for a path that ends in `/migrations/`, and no file path does.
- **Proof.**
  - On `e9f361c`, which adds `apps/rules/migrations/0002_…`, the command prints nothing. Section 1's own pathspec,
    `'apps/*/migrations/*.py'`, lists the file.
  - `git ls-files -- 'apps/*/migrations/'` lists 0 files, while `'apps/*/migrations/*.py'` lists 67: 39 numbered
    migrations and 28 `__init__.py`.
- **Impact.**
  - The line «check it again on the release — F-8 was still in flight» gives an all-clear whatever the release holds.
  - Today's statement is true: I verified it with a working pathspec and a grep of the full diff, and no in-flight
    branch adds a migration. So nothing false has shipped. But the check meant to catch the day the statement becomes
    false cannot catch it.
  - The release notes' «no migration was added» rests on the same re-check at the release.
- **Fix.**
  - Use `-- 'apps/*/migrations/*.py'` in §7, in `NOTES.md` §2 and in the test's pinned string.
  - Add a control to the test: the documented pathspec must match the tree, for example `git ls-files` with it lists
    the 39 numbered files. CI's checkout has the index, even shallow.
- **Same cause elsewhere (minor).** The runbook's step 15, item 2 (devops, `119f655`, before this branch) has the same
  pathspec: `diff --stat HEAD "refs/tags/$ILE_TAG" -- requirements/ 'apps/*/migrations/'` shows the requirements and
  never the migrations. `migrate --plan` in item 7 still shows the truth, so it only misleads the preview. Fix it in
  the same pass; the file is already delegated to this family.

**M2 — The runbook and the checklist now set two bars for PRODUCTION_READY.**

- **The new runbook *States* row** asks for:
  - A-1 … A-22 passed on the release commit with evidence;
  - the handoff «naming each of the owner's items A-23 … A-28 open or closed».
- **Checklist §A, unchanged,** still says: «The project is called ready for server deployment only when every line is
  ticked (see *States* in the runbook)». §A's lines run to A-28.
- **What changed without a record.**
  - The runbook's previous condition, «the go-live blockers are closed or accepted by the owner in writing», is gone.
  - `NOTES.md`'s list for the merge step does not mention the change.
  - `test_the_states_are_the_owners_three` pins the new wording.
- **Why it matters.**
  - PRODUCTION_READY is the state the orchestrator reports to the owner (V5.9 §16: «do not declare ready too early»).
    A reader of the checklist and a reader of the runbook would now declare it on different evidence.
  - The builder has a point: A-25 (SMTP from the server) and A-28 (backups running) can only close on the server.
    But the old wording already covered that with the owner's written acceptance.
- **Fix.**
  - Set one bar in both documents: A-1 … A-22 ticked on the release commit with evidence, and each of A-23 … A-28
    either closed or accepted in writing by the owner as open until go-live, and named in the handoff.
  - Reword checklist §A's sentence to say exactly that, and update the test.
  - The merge step records the definition in the decision log.

### Minor

**m1 — Release notes §6: the rule counts are wrong.**

- **What the notes say.** «13 drafted from the norm, 3 inherited from the previous platform».
- **What the seed writes.** 16 candidates over 15 sources: 11 `draft` / `drafted_from_source` and 5
  `legacy_candidate` / `legacy_derived`.
  - On the fresh seed, `seed_all` printed `seed rules.legal_ruleset: {'sources': 15, 'drafted': 11,
    'legacy_candidates': 5}`, and the table agrees.
  - `ACTIVE_RULES` and `REVIEW_RULES` have held 11 and 5 entries since `e9f361c` (21 September).
- **Where the figure came from.** `docs/platform/RULE_ENGINE_GOVERNANCE.md:233` and `docs/QA_REPORT.md:266`, which
  carry the same stale count.
- **Fix.** Write «16 candidates — 11 drafted from the norm, 5 taken from the previous platform». Hand the two older
  documents to the steward; they are outside w4-d's slices.

**m2 — «Production target» claims more than the run proves.**

- **What the text says.** The ci.yml comment: «Ubuntu 24.04 LTS's own Python 3.12 and PostgreSQL 16». The test
  docstring: «CI runs exactly that».
- **What CI actually runs.**
  - setup-python installs its own CPython 3.12.x build (the latest patch), not Ubuntu's 3.12.3.
  - `postgres:16-alpine` is built on Alpine (musl), not Ubuntu's glibc `postgresql-16`. The runbook's step 6 creates
    the database with the cluster's default locale.
- **What the run proves.** The server's major versions, the pinned closure and the Linux wheels. That is what matters,
  but it is not the distribution's own builds.
- **The added step.** «The interpreter and the database are the matrix's» asserts only the database. Python is
  printed, and setup-python already guarantees its version.
- **Fix.**
  - Say «the server's major versions» in the comment, in the docstring and in the runbook row.
  - Optional: use the Debian `postgres:16` image (glibc) for the production-target entry, and keep `-alpine` for the
    development entry, which `docker-compose.yml` uses.

**m3 — The migration tripwire checks a count, not the files.**

- **The gap.** `test_the_rollback_statement_about_the_migrations_is_still_true` passes as long as there are 39 numbered
  files. An edited migration, or one added and one removed, makes §7 false and leaves the test green.
- **Fix.**
  - Compare a digest of the 39 files' paths and contents, or their blob ids at `0a8351b`.
  - Once `v2.0.0` exists, freeze §7's sentence as «at `v2.0.0`» so that later releases need not edit it.

**m4 — Release notes §5: the confidential-material paragraph belongs to the owner.**

- **It is accurate.** Its subject is the owner's and the rights-holder's to state, not a public draft's.
- **Fix.** Move the paragraph to the release-candidate report and the owner's handoff, or let the owner choose its
  public wording.
- *The steward, at the merge (16 October 2026): this finding's own description is shortened to that — a review
  file is published with the tree, and m4 keeps the paragraph's substance out of it.*

**m5 — GO_LIVE_PHASE.md does not account for every gate.**

- **The gap.** The commit message says «G1…G11», but §1's table names G1–G6 and G11 only.
- **The missing gates.** G0 (the content lock), G7 (™/®), G8 (the public addresses), G10 (the translations) and G12
  (EU hosting) read no date and no phase flag. G9 appears only as the `analytics` row.
- **Fix.** Add one sentence saying so; it makes «every gate» checkable. Every flag the code reads, seven in all, is
  already in the table.

**Nits (not findings).**

- **«Never a rollback target».** V5.10 calls `pre-v5-main-2026-10` «a rollback/reference point». The documents say
  «never a rollback target of this server». Both are right; quote V5.10 and add «of the repository's history, not of
  this server», so that the owner reads no contradiction.
- **NOTES' ownership count.** It says 3 inside; there are 4 since the notes' own commit.
- **GO_LIVE_PHASE.md §2.1.** «the page's one action» introduces two actions.

## For the merge step (housekeeping, not findings)

1. **The release notes need an owner.** `docs/RELEASE_NOTES_v2.0.0.md` is in no family's slice. The checker reports
   4 inside, 6 delegated, 1 outside: FAIL until the steward assigns it.
2. **The decision log.** Record what `NOTES.md` lists: the matrix and its names, the added step, the release naming,
   the go-live verdict. Add M2's PRODUCTION_READY definition once it is fixed.
3. **F-3 is real.** `core/phases.py` says «a gate whose dependency is closed cannot be opened by flipping its own flag».
   `core/gates.py`'s `virtual_forum_enabled()` and `newsletter_enabled()` read the flag alone, so the console's own
   text is false until the fix lane runs. Schedule that lane before the release-candidate validation, or list F-3
   with its class in the report's outstanding defects (gate 12).
4. **The leftover container.** `ile-w4d-pg16` is still listed as «Created»: never started, holding no port. Remove it
   with `docker rm -f ile-w4d-pg16`.
5. **CI watchers.** The job names changed and the id `test` did not. The first push runs two jobs in parallel.
6. **Gate 14's note.** «the preview runs with a reference date of 3 October» is verified for the measuring server
   (`settings_8782.py`, plan §2.8). I did not verify it for the 8780 process, which I did not touch. It changes
   nothing: 3 and 16 October give the same gate states.

**Left behind by this review:** this file only. The throwaway database is dropped, the seed's copy of the media
library is removed from the worktree, the lane server is stopped and port 8789 is free.

Source for the runner notice: [GitHub changelog, 17 September 2026 — Ubuntu 26 generally available and `latest`
migration](https://github.blog/changelog/2026-09-17-ubuntu-26-generally-available-and-latest-migration).
