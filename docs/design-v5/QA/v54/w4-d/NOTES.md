# W4-D — integration readiness — lane notes

## Part 1 — release engineering

Lane `w4d1-build`, branch `v54-w4-d` (worktree `C:/tmp/ile_wt/v54-w4-d`, created from `design-v5` at `0a8351b`),
16 October 2026, Opus 5.5. Briefs read first, in full: the owner's V5.10 (the release decision: GitHub's `main` at
`a3ac318` tagged `pre-v5-main-2026-10`, `main` fast-forwarded to the validated `design-v5` snapshot, one annotated
tag `v2.0.0` — the orchestrator's work, never this lane's), V5.9 (never deploy, never touch a server, DNS, a domain or
a certificate; never name the production server) and V5.5 with its addenda. The family's slices in
`docs/design-v5/OWNERSHIP_V54.json` (`w4-d`, delegated); `.github/workflows/ci.yml` edited as the steward's delegate.

**Hard limits kept.** No deployment, no contact with any server, no DNS or domain operation, no certificate. No push,
no tag, no merge. No package added to the project, nothing installed into the project's `.venv`: the resolver proofs
and the Python 3.12 runs used two throwaway virtual environments under `C:/tmp/ile_v5_council/.work/w4-d/w4d1-build/`
(outside the repository). No secret; no server address or name in any file. No template, CSS or JS file touched (W4-A,
W4-C and F-8 are in flight on their own branches). Tests: `TEST_DATABASE_URL=…/ile_v5_l9`, one pytest at a time,
`-p no:randomly`, never the full suite; no lane server was needed (the pages were rendered through the test client).

### Delivered

| Commit | Item | Files |
|---|---|---|
| `4676ffd` | 1 — CI | `.github/workflows/ci.yml`; the CI lines of the runbook (§0's Python row, *Known limits*), checklist A-26, README «Requisiti» |
| `d2e217b` | 2 — the release in the deployment documents | `docs/deployment/PRODUCTION_DEPLOYMENT_RUNBOOK.md`, `PRODUCTION_CHECKLIST.md`, `ROLLBACK.md`; `tests/deployment/test_runbook_matches_the_code.py` (one assertion); `tests/deployment/test_release_tags_w4_d.py` (new) |
| `98ae0ad` | 3 — the go-live phase and the date gates | `docs/design-v5/QA/v54/w4-d/GO_LIVE_PHASE.md`; `tests/compliance/test_go_live_calendar_w4_d.py` (new) |
| `883b48c` | 4 — the release notes, draft | `docs/RELEASE_NOTES_v2.0.0.md` |
| this commit | the notes | `docs/design-v5/QA/v54/w4-d/NOTES.md` |

### 1. CI

**The change.** `runs-on: ubuntu-24.04` (GitHub's notice: `ubuntu-latest` moves to Ubuntu 26 from 19 October 2026;
the server is 24.04). One job, a matrix of two with `fail-fast: false`: the production target (Python 3.12,
`postgres:16-alpine`) and the development stack (Python 3.13, `postgres:17-alpine`); the job's name says which —
«Python 3.12 · PostgreSQL 16 (production target) — check · migrations · ruff · pytest» and «Python 3.13 · PostgreSQL 17
(development) — …». Install: `python -m pip install -r requirements/dev.txt -c requirements/constraints.txt` (open since
DL54-121). Every other step kept; one step added after the install, «The interpreter and the database are the
matrix's»: it prints the Python version and fails if the service answers with another PostgreSQL major — the job's
name stays true (exercised against the local PostgreSQL 17: `PG_MAJOR=17` passes, `PG_MAJOR=16` fails with
`AssertionError: 17`). The job id stays `test`. GitHub (read-only `gh api`): neither branch is protected and the
repository has no ruleset, so the new job names break no required check — but a script that watches CI by the old
name «check · migrations · ruff · pytest» must follow.

**The proofs, before the change.**
- *The constraints resolve with dev.txt* — `pip install --dry-run --ignore-installed --report` with
  `--only-binary=:all:`, the manylinux platform tags up to glibc 2.39 (Ubuntu 24.04) and `--python-version 3.12` (pip
  25.0.1) and `3.13` (pip 25.1.1): both resolve, 67 distributions each, the 19 pinned packages of `constraints.txt` at
  their pinned versions (19/19, no mismatch), 48 dev-only distributions resolved around them, wheels only — no
  compiler on the runner (the platform-specific ones: Pillow, psycopg-binary, cryptography's `manylinux_2_34`, cffi,
  greenlet, PyYAML, coverage, msgpack, charset-normalizer, tomli, ruff, Playwright's driver). Then a real install in a
  throwaway Python 3.12.10 venv (Windows): `pip install -r requirements/dev.txt -c requirements/constraints.txt` exit 0,
  `pip check` «No broken requirements found.».
- *Every source compiles under Python 3.12* — with a real 3.12.10 interpreter, `compile()` of the 817 tracked `.py`
  files (no bytecode written): 0 `SyntaxError`, 0 warnings.
- *The application runs on 3.12* — `manage.py check`: no issues; `makemigrations --check --dry-run`: «No changes
  detected»; a targeted suite on 3.12 (`tests/deployment`, the env-example guard, the compliance gates and gated links,
  the Forum's modes, the back office's second factor, `apps/cases/tests`): 394 passed, 3 skipped (the three intake
  cases that skip without a rule in force), and the env-example guard failed once — on this lane's own temporary probe,
  which read an undeclared variable; with the probe gone it passes on 3.12 (24 passed with the two new w4-d files).
- *YAML* — `yaml.safe_load` parses it; the matrix's two entries define the same keys; every `${{ … }}` is a plain
  context path and every `matrix.*` names a key of both entries; expanded: images `postgres:16-alpine` /
  `postgres:17-alpine`, Python `3.12` / `3.13` (strings, not floats). `tests/deployment/test_release_tags_w4_d.py` keeps
  it: `ubuntu-24.04`, fail-fast off, the two pairs, the install with the constraints, and the oldest Python CI runs
  equal to `requires-python`.
- *PostgreSQL 16 locally* — not done: a throwaway `postgres:16-alpine` container (port 5441) was created but Docker
  Desktop never started it within minutes, while the shared database stayed healthy; the attempt was abandoned so as
  not to load the shared Docker. **Leftover**: the container `ile-w4d-pg16` may still be listed as «Created» (never
  started, no port held); its removal was queued — if it is still there: `docker rm -f ile-w4d-pg16`. CI's
  production-target run is the PostgreSQL 16 proof.

**Documents that follow.** The runbook's §0 Python row and *Known limits* (Python 3.12, PostgreSQL 16), checklist A-26
(now «team (CI)»), README's «Requisiti» line («la CI prova sia 3.12 con PostgreSQL 16 … sia 3.13 con PostgreSQL 17»).

### 2. The release in the deployment documents

- The runbook: `export ILE_TAG=v2.0.0`; step 3 says the handoff's SHA is the commit (an annotated tag); *RELEASE TAGS*
  rewritten: `v2.0.0` annotated on the commit GitHub's `main` points to after the fast-forward, `pre-v5-main-2026-10`
  on `a3ac318304beb4504134762bfa6e9c4e4ce600f1` as the pre-V5 platform's reference point (never deployed, never a
  rollback target of the server), no candidate tag, a tag never moved; *States* rewritten as V5.9 defines them under
  V5.10 (RELEASE_CANDIDATE = one design-v5 snapshot named by its SHA after the fourteen gates; PRODUCTION_READY = that
  commit is `main`, both tags exist, A-1 … A-22 with evidence, the handoff written naming A-23 … A-28).
- The checklist: A-1 (the publication repository's design-v5 snapshot), A-2 (`ls-remote` of `main`, `design-v5`, both
  tags with their `^{}` lines, no other tag; both CI runs green), A-27 (decided), C-7 (the reference tag is not a
  previous tag of the server).
- ROLLBACK.md: `PREVIOUS_TAG=v2.0.0`; a line under the table; §7 «The pre-V5 platform» — what going back to it would
  mean: it predates F-5, F-7, F-8 and the NUL guard; **no migration differs today** (`git diff --name-status 2b16eb3
  0a8351b -- 'apps/*/migrations/*.py'` prints nothing — the pattern as the review fixes corrected it, the first one
  listed no file —: 39 identical files, byte for byte — the tree of `a3ac318` is local `main`'s `2b16eb3`, checked:
  both trees `bb57c0b`; the models' diff since is non-schema: TRANSITION_ACTORS, a clock call, a key list; F-8, W4-A
  and W4-C add none so far); and the rule regardless: a downgrade is a restore of the verified
  pre-migration dump, never a `migrate` backwards on live data; at the first deployment there is no dump to return to.
- Tests: `test_the_release_gate_compares_the_tags_commit` pinned the placeholder `"refs/tags/<tag>^{}"`; it now names
  `v2.0.0` and the reference tag (the reason in its docstring). New `tests/deployment/test_release_tags_w4_d.py`: the
  tag is the version label (base.py and the model's default), the three documents name one release and one reference
  SHA, no candidate tag is deployed or rolled back to, the three states, a downgrade is a restore, **the rollback's
  migration count (39) is the tree's** — a migration added later fails it until §7 says what it changes; since the
  review fixes, the 39 files' blob ids (m3) —, and CI's production target. `tests/deployment`: 97 passed.

### 3. The go-live phase

`GO_LIVE_PHASE.md`. Rendered on a fresh seed (no flag row) at five moments from 16 October to 15 December 2026, French
and Arabic, every internal link followed (113 / 161–167 distinct, all 200 or 302): no past-dated call to action, no
countdown, no open registration for the past event, no phase that shows nothing. Nothing to fix in code. The interim
variant of the hero and the chrome is V5's own and tested (no build). `tests/compliance/test_go_live_calendar_w4_d.py`
(3 passed, 17 s; a control finds the registration button while registration is open, so «not found» means gone).

### 4. The release notes

`docs/RELEASE_NOTES_v2.0.0.md` — sources: `CHANGELOG_V54.md`, `live_status.json`, the decision log (DL54-87, -121,
-130, -131, -132, -152, -154), the W1-0 baseline (`evidence/v54/w1-0/before/`), the families' SHIPPED and NOTES files,
the DevOps notes; the GitHub settings read with `gh api` on 16 October. F-8's paragraph «pending F-8's merge»; the
fourteen V5.10 gates «to be filled by the release-candidate validation», with a column «at this draft».

### For the owner

1. **The Forum after its event — words** (`/fr/forum/`, both modes; locked texts, a written transmission):
   «Au cours du Forum seront également présentés Italy Legal Entry et le projet pilote Vénétie–Maroc.»
   (`p2.forum.what.body`); «Le programme détaillé des interventions est en cours de définition et sera mis à jour sur
   cette page.» (`p2.forum.programme.note`); «Sont prévues, entre autres, les interventions d'un Sénateur de la
   République, … Les noms des intervenants seront publiés avec le programme définitif.» (`p2.forum.speakers.body`); in
   event mode also «La participation est gratuite, sur inscription préalable.» (`p2.forum.registration.intro`) above
   «Les inscriptions sont closes.». New words for after the event — or keep them as the launch meeting's record.
2. **The Forum's mode at the deployment** (`/fr/forum/`): with `forum_permanent_mode` off, the page presents the past
   launch event as «Événement institutionnel». Recommended: switch it on at the deployment (back-office, the flag, or
   the edition's «mode de la page» = permanent) — existing words only: «FORUM PERMANENT VÉNÉTIE–MAROC», «Espace
   permanent de dialogue et de coopération», «Rencontre de lancement : …».
3. **The Virtual Forum** (`/fr/forum-virtuel/` and the Forum page's teaser): not before the legal pages are published —
   switched on earlier it offers «Créer un compte» to a sign-up that answers «Inscriptions fermées» (G11's own rule;
   item 3 of «For the team»).
4. **Phase 3**: the go-live phase is the owner's authorisation of `phase3_public` (its date condition holds since
   2 October); both variants are ready.
5. **GitHub settings** (read 16 October 2026): wiki enabled and unused; Dependabot alerts and security updates off;
   secret scanning and push protection on.
6. The F-5, F-7, B1 and deployment questions are gathered in the release notes, §5.

### For the team and the merge step

1. **Ownership** (`check_ownership.py w4-d design-v5`: 5 inside since the notes and the review, 6 delegated,
   1 outside → FAIL until assigned):
   `docs/RELEASE_NOTES_v2.0.0.md` is in no family's slice — the steward assigns it (w4-d) before the merge. Delegated
   paths, each changed as written above: `.github/workflows/ci.yml` (the steward's), `README.md` (one line of
   «Requisiti», outside devops' and sec-f5's slices), `docs/deployment/{PRODUCTION_DEPLOYMENT_RUNBOOK,
   PRODUCTION_CHECKLIST,ROLLBACK}.md` (devops; no sec-f5 line touched), `tests/deployment/test_runbook_matches_the_code.py`
   (devops; one assertion and its docstring).
2. **Decision log**: no entry written on this branch — four families append to it in parallel; the merge step records
   this part (the matrix and its name, the added step, the release naming in the documents, the go-live verdict).
3. **F-3 — the Virtual Forum's and the newsletter's dependency** (`GO_LIVE_PHASE.md`): the phase console declares
   `depends_on=("legal_pages_available",)` for `virtual_forum_enabled` and `newsletter_enabled` and says a closed
   dependency blocks the flag; `core.gates` reads the flags alone (`forum.governance_services.governance_enabled`
   already names the second condition «the day the gate gains» it). The fix — both gates also require
   `legal_pages_available()` — needs `legal_published` in the fixtures that switch these flags on
   (`apps/community/tests/conftest.py`'s `flag_on`, `apps/forum/tests/conftest.py`'s governance fixture,
   `apps/forum/tests/test_forum_mode.py`'s two Virtual Forum cases, `tests/frontend/test_cms_nav.py`,
   `tests/frontend/test_content_pages_w3_f2.py` and its browser file): a targeted fix lane with those tests.
4. **F-4 — the sign-in's invitation to a closed sign-up**: `templates/account/login.html` renders allauth's block with
   «Si vous n'avez pas encore créé de compte, merci de vous enregistrer au préalable.» while G2 closes the sign-up;
   hiding it means not inheriting that paragraph — W2-B's page, after W4-A.
5. **The orchestrator's CI watch**: the job names changed (above); the job id `test` did not. The first push of this
   workflow runs two jobs of about the same length in parallel.
6. **W4-D part 2** (not this pass): the deletion map's last row, dead code, DS 2026 final, the whole-product council;
   the release notes' figures and gates after it.

### Tests run here

| Run | Result |
|---|---|
| `tests/deployment` (after item 2) | 97 passed |
| `tests/compliance/test_go_live_calendar_w4_d.py` | 3 passed |
| `tests/test_env_example_is_complete.py`, `tests/frontend/test_design_docs.py`, `tests/security`, the calendar test, the personal-data guard (after item 3) | 218 passed (the confidential-material guard ran with its private table) |
| `tests/deployment`, `test_design_docs.py`, `tests/security`, the env-example and personal-data guards (after item 4) | 312 passed |
| Python 3.12.10 (throwaway venv): `check`, `makemigrations --check`, the targeted suite above; then the env-example guard and the two new files | clean, clean, 394 passed / 3 skipped (+ the probe artefact, see §1); 24 passed |
| `ruff check` / `ruff format --check` on the new and changed test files | clean |

## Part 1 — review fixes

Lane `w4d1-fix`, branch `v54-w4-d` (worktree `C:/tmp/ile_wt/v54-w4-d`), 16 October 2026, Opus 5.5. Read first:
`REVIEW_PART1.md` (SHIP_AFTER_FIXES: nothing blocking, two majors, five minors, three nits, six housekeeping items) and
the owner's V5.10, V5.9 and V5.5 with its addenda. Both majors, the five minors and the three nits are fixed, each with
its proof; m2's optional image change is not taken (below). Part 1's hard limits held: no deployment, no server, DNS,
domain or certificate; no push, no tag, no merge; no package; no secret, no address, no server name (every added line
scanned); no template, CSS or JS file; no file of W4-A, W4-C or F-8; tests one at a time on `ile_v5_l9`, no lane
server.

| Finding | Fix | Commit | Proof |
|---|---|---|---|
| **M1** — ROLLBACK.md §7's migration re-check matched no file | `-- 'apps/*/migrations/*.py'` in §7 and in the runbook's step 15 preview (the same cause, before this branch); the test pins the command; a control asks `git ls-files` that every migration pattern of the three documents lists every migration file | `579c01d` | the control red on the previous documents (0 of 39 listed), green now; on `e9f361c`, which adds a migration, the fixed commands list it and the old ones printed nothing; `2b16eb3` → `0a8351b`: nothing; 47 bash blocks parse |
| **M2** — two bars for PRODUCTION_READY | one bar, in the same words in the runbook's *States* and checklist §A: «A-1 … A-22 ticked with evidence on that commit, and each of A-23 … A-28 closed or accepted in writing by the owner as open until go-live»; the handoff names each of A-23 … A-28 with its state; the parts of A-1 … A-22 that run on the server or on the temporary host (A-8, A-10, A-11, A-13, A-14, A-15, A-16, A-21, A-22) are the owner's, at the deployment, and the handoff lists them; §B's second line points to the bar | `e968e0d` | the two tests red on the previous documents (2 failed), green now |
| **m1** — the rule counts of the release notes | «16 candidates — 11 drafted from the norm, 5 taken from the previous platform» | `a6b9dc2` | `apps/rules/seeds.py` read by AST: `SOURCES` 15, `ACTIVE_RULES` 11 (written `DRAFT`), `REVIEW_RULES` 5 (written `LEGACY_CANDIDATE`) |
| **m2** — «production target» claimed Ubuntu's builds | «the server's major versions» in ci.yml's comment, the test's docstrings, the runbook's Python row and *Known limits*, A-26 and the release notes' CI line; the version step asserts the interpreter's minor version too | `ecd691f`, `db311e0` | the step run as ci.yml writes it, line by line: Python 3.13.5 and 3.12.10 each pass with their own version and fail with the other; against PostgreSQL 17, `PG_MAJOR=17` passes and `16` fails; the YAML parses, every `${{ }}` is `github.ref` or a key both matrix entries define; the step's env and both asserts pinned by the test |
| **m3** — the migration tripwire counted files | the 39 numbered files with their git blob ids at `0a8351b` — the same list as `a3ac318`'s —, each id computed from the checkout | `9c67417` | an edited migration, and a renamed one (39 files still), each fail the new test and passed the count |
| **m4** — the confidential-material paragraph | out of the public release notes; its substance goes to the orchestrator for the release-candidate report and the owner's handoff (this lane's return), not to a published file | `a6b9dc2` | — |
| **m5** — the gates GO_LIVE_PHASE.md left unnamed | one paragraph in §1: G0, G7, G8, G10 and G12 read neither a date nor a phase flag; G9 is only the `analytics` default, which no code reads; the gates document's flags for G7, G8 and G9 are read by no code either | `0fe5b66` | grep of `apps`, `templates`, `config` and `static/js/src`, the tests left out |
| nits | V5.10's «a rollback/reference point» quoted — of the repository's history, not of this server (ROLLBACK.md §7, the runbook's *RELEASE TAGS*); GO_LIVE_PHASE.md §2.1's «one action» is the action card, with its primary and its secondary; NOTES' ownership count (5 inside) | `cce5d9b`, `0fe5b66`, this commit | `templates/forum/partials/cta_row.html`; `check_ownership.py w4-d design-v5` |
| housekeeping 6 — gate 14's note | the preview's reference date stated as the plan's (§2.8), verified for the measuring server's settings only (release notes §7, GO_LIVE_PHASE.md §1) | `a6b9dc2`, `0fe5b66` | `settings_8782.py` read; the running preview not touched |
| NOTES §2 | the pattern of the «no migration differs» proof corrected | this commit | re-run with it: nothing; the two trees' 39 path and blob pairs identical |

**Not taken.** m2's option — the Debian `postgres:16` image (glibc) for the production-target run. The collation of
the server's cluster follows the droplet's locale when the package creates it, which nothing here knows (a C.UTF-8
locale sorts by code point, as Alpine's musl does), so neither image is the server's build; the wording now claims the
major versions only.

**Found on the way.** The first pin of the version step (`ecd691f`) wrote its two asserts as literal strings, which
`tests/test_env_example_is_complete.py` reads as variables the application reads (1 failed of 215 in the guards' run);
`db311e0` writes them as patterns.

### For the team and the merge step (after the review fixes)

1. **Ownership** — `check_ownership.py w4-d design-v5`: 5 inside, 6 delegated, 1 outside → FAIL until the steward
   assigns `docs/RELEASE_NOTES_v2.0.0.md`. The review fixes added no path.
2. **Decision log** — besides part 1's list: M2's definition of PRODUCTION_READY in its exact words (the runbook's
   *States*, checklist §A) and the version step that asserts both versions.
3. **The steward** — two older documents carry the stale rule count «13 / 3»: `docs/platform/RULE_ENGINE_GOVERNANCE.md`
   (line 233) and `docs/QA_REPORT.md` (line 266). Neither has an owner (`check_ownership.py --owners`), so this lane
   left them: 16 candidates over 15 sources, 11 drafted (`DRAFT`), 5 from the previous platform (`LEGACY_CANDIDATE`).
4. **F-3** — real: `core.gates` reads `virtual_forum` and `newsletter` alone, while the phase console says a closed
   dependency blocks them. A fix lane before the release-candidate validation, or the report's outstanding list with
   its class (gate 12).
5. **Once `v2.0.0` exists** — ROLLBACK.md §7 says «at `v2.0.0`», and
   `test_the_rollback_statement_about_the_migrations_is_still_true` holds only the released files (none edited or
   removed): a later migration is the next release's business (§1).
6. **The leftover container `ile-w4d-pg16`** — removal attempted (`docker rm -f -v`): the command timed out after
   300 s, as `docker inspect` did after 240 s. Docker answers `ps`, but its health checks report «unhealthy» for
   containers whose databases answer — the lane database among them, which served every test here. The container is
   still «Created», holding no port. When Docker answers: `docker rm -f -v ile-w4d-pg16`.
7. **CI watchers** — nothing new: the job names and the step's name are part 1's.

### Tests run (review fixes)

| Run | Result |
|---|---|
| `tests/deployment` | 99 passed (part 1's 97, the pattern control, the PRODUCTION_READY bar) |
| `tests/deployment/test_release_tags_w4_d.py` on the previous documents | red, as it must be: 2 failed for M1, 2 failed for M2 |
| `tests/compliance/test_go_live_calendar_w4_d.py` | 3 passed |
| `tests/test_env_example_is_complete.py`, `tests/frontend/test_design_docs.py`, `tests/security`, the personal-data guard | 215 passed (the confidential-material guard with its private table) |
| `ruff check` and `ruff format --check` on the changed test file; `git diff --check`; no CR and no NUL byte in any changed file | clean |
| `bash -n` on every bash block of the three deployment documents | 47 of 47 parse |

## Part 1 — at the merge (the steward)

Lane `w4d1-merge`, 16 October 2026, Opus 5.5: the steward's merge of part 1 into design-v5, recorded in DL54-155.
`DESIGN_V5_MERGE_LOCK` taken at 11:18:17. No tag, no push, no 8780 change, nothing deployed.

1. **The sync.** design-v5 was at `0a8351b`, which is the branch's own base, so `git merge design-v5` printed «Already
   up to date». No source changed on either side, so no bundle was rebuilt.
2. **The manifest** (`331512d`). `docs/RELEASE_NOTES_v2.0.0.md` is now w4-d's whole file. The six delegated edits are
   recorded as w4-d slices. I read each one in the diff, and each stays inside its slice:
   - `.github/workflows/ci.yml`, the steward's delegated edit (the file stays the steward's);
   - the runbook, the checklist and ROLLBACK.md;
   - README's «Requisiti» line;
   - the release-gate assertion of `test_runbook_matches_the_code.py`.

   Every file but ci.yml stays devops's. The family's note now says this, for part 2's merge.
   `check_ownership.py w4-d design-v5`: 5 inside, 6 delegated, 1 outside → FAIL before; 6 inside, 6 slice → PASS with
   the extended manifest. After its commit, the manifest joins the diff as the steward's own steward-only path.
   `--validate`: 29 families, 745 entries.
3. **REVIEW_PART1.md's m4** (`859c7d8`). The finding, its verdict and its fix are kept; the paragraph's substance is
   not. A family's QA folder is published with design-v5's snapshots: the publication repository's design-v5 tree holds
   every family's REVIEW.md. Published as written, the review would have put back what m4 took out of the release
   notes.
4. **The scan** of the added lines (12 paths, 1 391 lines):
   - no IPv4 address, no server name, no e-mail address, no secret-like assignment or token;
   - two URLs only: github.com (the repository's own address) and github.blog (the runner notice);
   - no CR, no NUL; `git diff --check` clean.

   No template, stylesheet or script changed, so the shared CSS payload is unchanged (V5.8).
5. **The tests** on the merged branch: `TEST_DATABASE_URL=…/ile_v5_l9`, `-p no:randomly`, one pytest, at
   `859c7d8` (the tree merged here, apart from these notes): **384 passed** in 4 min 18 s, none skipped, none failed.
   - `tests/deployment` 99;
   - `tests/security` 157 (the confidential-material guard ran with its private table: the check that skips without
     it did not skip);
   - `test_design_docs.py` 40; the environment template 14; the checker's tests 57;
   - both bundle-currency tests 10; the go-live calendar 3; the personal-data guard 4.

   Also clean: `manage.py check` (no issues) and `makemigrations --check --dry-run` («No changes detected»), both on
   `ile_v5_l9`; `ruff check` and `ruff format --check` on the branch's three test files. W4-C's measurement windows
   ran back to back, so this run took its turn through `PERFORMANCE_BENCHMARK_LOCK`: taken at 11:43:24 when it was
   free, released at 11:47:46.
6. **Not done here, on purpose:**
   - The two documents with the stale rule count «13 / 3» (`docs/platform/RULE_ENGINE_GOVERNANCE.md` l. 233,
     `docs/QA_REPORT.md` l. 266) are not in this merge's diff. Neither has an owner, so they wait for part 2's merge or
     the steward's next pass, with an assignment.
   - I did not touch the leftover container `ile-w4d-pg16`: Docker is shared, and its removal stays as «Part 1 —
     review fixes» item 6 says.
   - F-3 stays open, as item 4 of the same list says.
