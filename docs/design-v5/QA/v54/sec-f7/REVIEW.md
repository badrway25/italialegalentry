# F-7 — who may move a case file, and the dashboard of a held file — independent review

Lane `sec-f7-review` (independent reviewer; built nothing), 16 October 2026. Reviewed: branch `v54-sec-f7` at
`9a9bb5c` — `git diff design-v5...HEAD` (merge base `fec37d3`), 6 commits, 10 files (`apps/cases/models.py`,
`services.py`, `apps/selection/services.py`, `apps/portal/services.py`, `templates/portal/dashboard.html` — one
condition —, `docs/platform/CASE_LIFECYCLE.md` — one line —, the notes and three test modules). Judged against
`docs/platform/CASE_LIFECYCLE.md` §4 (the «Chi può» column, rule 2) and the brief. Directive V5.9 kept: nothing
deployed, no server, DNS or certificate touched, no package added. Personas only through minted sessions
(`Client.force_login`); no password typed anywhere. Lane 7: pytest on `test_ile_v5_l7`, one run at a time,
`-p no:randomly`; no server started (the builder's captures were reused and looked at). My tests live outside the
repository (`C:/tmp/ile_v5_council/.work/sec-f7/review/`): a passing test means the attack failed; a `test_probe_*`
asserts the strict reading of §4 (or a hardening property) and **fails** where the branch differs — each failing probe
is a finding below.

## Verdict — SHIP_AFTER_FIXES (nothing blocking)

**F-7 is closed for the person, and nothing regresses.** Through the transition view, every account in every state was
sent every state as a forged target. The cast was 16 accounts: the owner; each assignee capacity live, revoked and
expired; staff and role holders with no assignment; a stranger; the administrator; a superuser. The setups were the 10
states plus a suspension made by each of four capacities. In every case, what moved is exactly §4's set for that
capacity. The administrator moved to its documented wider set (finding 1). Every move wrote one audit event naming the
account and one notification to the person; every refusal wrote neither. The page's offer equals what the domain
accepts for 21 accounts in every state, legacy suspended rows included. The person's suspend, close and
resume-own-suspension still work. So do the operator's and the professional's §4 moves, the authorised actor's
selection path, CR-03, read-only CLOSED, the suspension reason and notifications in the person's language. 78 of my 89
tests hold (the 11 that fail are the probes), and the builder's suites pass (713 passed, 3 skipped, browser tests
excluded). The control: my person matrix on design-v5 `fec37d3` reproduces F-7 (the person moves ORIENTED →
ADMIN_PROCESS, TRAINING → SELECTION, PRE_DEPARTURE → ENTERED, and out of anybody's suspension to any state; the
operator and the professional make every declared move). Part B tells a held file's owner the truth in live words,
shows nothing they may not read and keeps the NowPanel's grammar.

**Two major findings in F-7's own subject, who may move a file.** (1) The branch puts the administrator on every
declared row. That includes the two rows of the authorised actor's reserved activity, the very move F-7 names: from the
case page, an administrator opens SELECTION with no mandate and no process, and concludes it positively. (2) The back
office lets an operator give itself a capacity the column refuses, then make that capacity's moves on the case page.
Neither is a regression: on design-v5, any account holding «change» could make any declared move. So the branch is a
strict improvement and nothing blocks. Both fixes are small and belong in this branch, so fix them before the merge.
Five minor findings follow: three on what the branch adds, two that predate it.

## Findings

| # | Severity | Finding | Fix |
|---|---|---|---|
| 1 | major — domain | `transition_actors` adds the administrator to **every** declared row («o superiore», generalised). §4 names it on three rows only: suspend, close, and lift a suspension as «superiore». So an administrator still makes, from the case page, TRAINING → SELECTION whenever an authorised actor is merely assigned, and SELECTION → ADMIN_PROCESS («esito positivo della selezione»), both CR-03's reserved activity. It also makes DRAFT → ORIENTED (an orientation nobody ran), the professional's review conclusions, the five rows §4 does not declare (rule 2) and SUSPENDED → any active state. The doc test compares the data with §4 «beside the administrator», so it cannot see any of this | the administrator only where §4 names it; at least, now, never on TRAINING → SELECTION, SELECTION → ADMIN_PROCESS, DRAFT → ORIENTED; its other rows as explicit data the doc test checks (below) |
| 2 | major — back office | `role:operator` holds `cases.change_*`. The IA lists the operator among back-office users, and sec-f5's admin site admits it once its second factor is satisfied. In the back office it **gives itself a capacity** the column refuses it: `CaseFileAdmin` leaves `person` editable, so it makes itself the owner and closes the file as «persona» from any state; `CaseAssignmentAdmin` and the inline leave `role`, `assignee` and `case` editable, so it turns its assignment into a professional's and concludes a review, or takes over another file's assignment and moves a file it could not even read (404 before). No domain audit event, no notification. Reproduced on the branch and on the merged tree | `person` and `suspension_reason` read-only in `CaseFileAdmin`; the assignment's fields read-only in both admin screens, revocation through an action that calls `services.revoke_assignment`; the four probes kept as regression tests |
| 3 | minor — hardening (new code) | `suspended_by` takes the latest suspension event **whatever its date**. A file set SUSPENDED by any path that writes no event (a restore, a data fix, a future import) is attributed to an *older* suspension, and the person may then lift a suspension they did not make | bind the event to the current suspension: `created_at__gte=case.status_since` (and/or `metadata__from=case.previous_status`) |
| 4 | minor — functional (new code) | if the authorised actor's case assignment is revoked while its process is open, `conclude` is refused whole: the process stays open and the file stays in SELECTION with no authorised actor answerable (rule 1). Before F-7 the conclusion went through | answer the selection's exit rows from the open process (the service already checked `is_operator`), or keep SELECTION → TRAINING as the administrator's way out (finding 1) |
| 5 | minor — hardening (pre-existing) | `transition` checks WHO on the object it is handed and saves without re-reading or locking the row. A request that loaded the file before another account's move overwrites the newer state. Seen: the person's in-flight resume wrote ORIENTED over an administrator's ENTERED | `select_for_update()` on the row at the top of the atomic block, the checks and the save on the locked row |
| 6 | minor — audit fidelity (pre-existing) | `audit.services.record` falls back to `request.user` when no actor is given. The platform's moves made inside the person's request (the orientation service's DRAFT → ORIENTED, ORIENTED → REVIEW_REQUIRED) are recorded with the **person** as actor, and the timeline says «Vous» | the platform path records no actor (an explicit «system» call of `record`) |
| 7 | minor — Part B, words | four places where a held file's screens could be truer, all for the copy packet: a closed file's «Mes documents» empty state promises a list; «pour l'instant» on a closed file's page; a suspended file's page names a next action its dashboard does not; «Votre dossier» three times | the copy packet B1 (below); no falsehood about the state |

### 1. The administrator on every declared row

`cases.models.transition_actors` ends with `return names | {_WHO.ADMINISTRATOR}` (`apps/cases/models.py:172`), for every
row the graph declares. §4 names the administrator on three rows: «qualunque attivo → SUSPENDED: persona, operatore,
amministratore», «qualunque → CLOSED: persona, amministratore», and, as «superiore», «SUSPENDED → stato precedente».
That it is *named* on two rows is the table saying it is not on the others. The notes' reading, «o superiore» from
the resume row applied to every row, is an interpretation §4 does not make. The new line of `CASE_LIFECYCLE.md`
(«La colonna «Chi può» è … applicata da `cases.services.transition`») does not say so either.

What the probe saw (`test_probe_the_administrator_makes_only_the_moves_section_4_names_for_it`), the moves an
administrator makes beyond §4's:

| From | Beyond §4 |
|---|---|
| DRAFT | ORIENTED |
| ORIENTED | REVIEW_REQUIRED, TRAINING, ADMIN_PROCESS |
| REVIEW_REQUIRED | ORIENTED, TRAINING, ADMIN_PROCESS |
| TRAINING | **SELECTION**, ADMIN_PROCESS, ORIENTED |
| SELECTION | **ADMIN_PROCESS**, TRAINING |
| ADMIN_PROCESS | PRE_DEPARTURE, REVIEW_REQUIRED |
| PRE_DEPARTURE | ENTERED, ADMIN_PROCESS |
| ENTERED | POST_ENTRY |
| SUSPENDED (whoever suspended) | DRAFT, ORIENTED, REVIEW_REQUIRED, TRAINING, SELECTION, PRE_DEPARTURE, ENTERED, POST_ENTRY |

Two rows of this table are F-7 itself. The brief names «TRAINING → SELECTION whenever an authorised actor is assigned
(a reserved activity, CR-03)». `test_probe_the_administrator_opens_and_concludes_a_selection_from_the_case_page`
shows it from the case page: the administrator moves the file into SELECTION («Fase gestita da soggetto
autorizzato») and on to ADMIN_PROCESS («esito positivo della selezione»), with **no `SelectionProcess`, no mandate and
no act of the authorised actor**. The journey «La soglia» then draws both as facts. CR-03's own check passes because an
authorised actor is assigned. The project's own words refuse this: «An administrator is not that actor; the act
belongs to the operator, in the workspace» (`apps/selection/admin.py:92`). DRAFT → ORIENTED is the same kind of
dishonesty: it draws «Orientation terminée» for an assessment that does not exist.

The doc test cannot see any of it. `test_the_data_says_what_section_4_says` compares the data and §4 through
`_beside_the_administrator` (`apps/cases/tests/test_transition_actors.py:262`), and
`test_the_administrator_is_on_every_declared_row_…` asserts the widening as a rule.

**Fix.**

- **Now:** do not add the administrator to TRAINING → SELECTION, SELECTION → ADMIN_PROCESS or DRAFT → ORIENTED. CR-03
  is a legal boundary, not a design choice, and the orientation service is the only one that may claim an orientation.
- **Keep, explicitly:** SELECTION → TRAINING may stay the administrator's as the way out of a stuck selection (finding
  4). It asserts no outcome.
- **The other rows:** the operator's and professional's rows, ENTERED → POST_ENTRY (Q5), the five undeclared rows and
  SUSPENDED → non-previous (Q1) should be an explicit data set beside `TRANSITION_ACTORS`, e.g. `ADMINISTRATOR_ROWS`.
  Each entry needs its reason, until the owner's answer to Q1/Q5 puts the rows in §4 or removes them.
- **The doc test:** compare the administrator too: §4's three rows plus that set, and nothing else.
- My two probes become the regression tests, with their expectation adjusted to the decision.

### 2. The back office hands out capacities

Since the fix, WHO may move a file is read from the account's **capacity** on it: owner, or the role of a live
assignment. The branch pins that the back office cannot write `status` (`TestTheBackOffice`, commit `ef1d545`, «the
back office cannot move a case file»). That holds: a superuser posting `status`, `previous_status`, `closed_at` and
`status_since` into the change form changes none of them, and no action or bulk action moves a file. But the
capacities themselves are editable:

- `CaseFileAdmin.fields` holds `person` with no read-only marking (`apps/cases/admin.py:63-78`).
- `CaseAssignmentAdmin` (`:111-116`) and `AssignmentInline` (`:30-43`) leave `case`, `assignee`, `role`, validity and
  `revoked_at` editable.
- `role:operator` holds `cases: view, change` (`apps/accounts/roles.py:160-161`). The IA puts the operator in the back
  office («Back-office (… operatore, amministratore)», `PLATFORM_INFORMATION_ARCHITECTURE.md:150`).
- Production grants it: the `accounts.roles` seed is not gated, and the runbook runs `seed_all` at every release
  (`PRODUCTION_DEPLOYMENT_RUNBOOK.md:323`).

Each probe goes through real admin form posts: the change form is fetched, parsed and posted back.

| Probe | What the operator does | Result |
|---|---|---|
| `test_probe_the_operator_becomes_the_owner_in_the_back_office_and_closes_the_file` | refused CLOSED from ORIENTED on the case page, as §4 says; sets `person` = itself in the CaseFile form; posts CLOSED again | saved (302); **the file is CLOSED**, recorded as the operator's move |
| `test_probe_the_operator_gives_itself_the_professionals_capacity_and_concludes_a_review` | refused REVIEW_REQUIRED → ORIENTED; turns its own OPERATOR assignment into PROFESSIONAL in `CaseAssignmentAdmin` | **the review is concluded** (§4: «professionista» alone) |
| `test_probe_the_operator_takes_over_another_files_assignment_and_moves_that_file` | on a file it cannot read (404), edits the training body's assignment: assignee → itself, role → operator | **ORIENTED → ADMIN_PROCESS on that file** |
| `test_probe_a_suspended_files_reason_is_rewritten_in_the_back_office_without_a_domain_event` | rewrites a suspended file's reason | rewritten; **0 `case.*` audit events** (only the admin's LogEntry). The person reads that text on the NowPanel |

None of these goes through `services.assign`: no `case.assigned` event, no notification to the displaced assignee or
to the person. The operator must hold `is_staff`, and in production its second factor too. That is the account's own
holder acting, so MFA does not change the finding.

**On the merged tree too.** I took design-v5 `f447c28` with sec-f5 merged, plus this branch (`git merge-tree`: tree
`ebccc2d`, no conflict), and extracted it with `git archive` (no worktree, no commit). The default admin site there is
`accounts.admin_site.BackofficeAdminSite`. The same four probes fail and the same four checks hold.

The notes saw the inline (Q10, «outside F-7 … not its status») but not `person`. After this fix, though, a capacity
*is* the right to a status move.

**Fix (in `apps/cases/admin.py`, this family's app; no path in common with sec-f5):**

- `person` and `suspension_reason` into `CaseFileAdmin.readonly_fields`. A file's owner never changes, because a new
  file is opened. The reason is written by the domain with the move (rules 3 and 4).
- `TestTheBackOffice::test_a_suspended_files_reason_cannot_be_emptied_there` then becomes «cannot be edited there».
- In `AssignmentInline` and `CaseAssignmentAdmin`, every field read-only. Revocation becomes an admin action calling
  `services.revoke_assignment`, which audits and notifies, as the policy's own docstring says («only administrators
  create or revoke outside the services»).
- An alternative is to narrow `role:operator` to view on `cases.caseassignment` through an `app.model` key of
  `ROLE_PERMISSIONS`.
- Keep my four probes as regression tests, inverted.

### 3. «Chi ha sospeso» is read from an event that may belong to another suspension

`suspended_by` (`apps/cases/services.py:258`) picks the newest `case.transition` event with `to = suspended`. Today
every suspension writes its event in the same atomic block, so the two agree. The function's own docstring counts on
rows the code did not write, though («a seeded file …»). Any SUSPENDED row without its event inherits the previous
suspender. `test_probe_a_suspension_written_without_its_event_is_attributed_to_an_older_suspender` sets it up: the
person suspends and resumes, then a row is restored as SUSPENDED with no event. `suspended_by` answers the person,
who may then lift it. Fix: `.filter(created_at__gte=case.status_since)`. The event is created after `status_since` is
set, in the same transaction. Without a match the answer is None, so only the administrator may lift it.

### 4. A selection that cannot be concluded

`_authorised_actor_transitions` requires an unrevoked AUTHORISED_ACTOR assignment on the file. If it was revoked while
the process is open, by an administrator through `services.revoke_assignment` or by the back office's `revoked_at`,
`conclude` raises inside its atomic block. The process stays open and the file stays in SELECTION with nobody
answerable for it (§4 rule 1). `test_probe_a_revoked_case_assignment_leaves_the_file_stuck_in_selection` shows it:
«conclude refused; file selection, process closed=False». Before the branch the conclusion went through.

Fix: let the exit rows (SELECTION → TRAINING / ADMIN_PROCESS) be answered by the open process. `conclude` could pass
it, and the domain checks that it is this file's process (`process.case_id == case.pk`) concluded by a live operator
of its actor; the service has already checked `is_operator`. `conclude` marks the process closed before it moves
the file, so the check must not require an open process. Or rely on the administrator's SELECTION → TRAINING kept
in finding 1.

Related, and fine: an `ActorOperator` whose `role:authorised_actor` was withdrawn now opens nothing. `open_process`
rolls back whole, with no process, no assignment and no move. That is fail-closed.

### 5. A move computed on a stale row

`test_probe_a_move_computed_on_a_stale_row_overwrites_a_newer_state` interleaves two moves deterministically. The
person's request holds the file as «suspended by me, previously ORIENTED». An administrator moves it to ENTERED. The
person's save then writes ORIENTED over ENTERED, a move ENTERED → ORIENTED nobody may make. The same window lets a
stale suspension record an old `previous_status`, so a person could undo an operator's move by suspending and resuming.
The window is one request (milliseconds) and the flaw predates the branch, but the WHO check now depends on the row
being current. Fix: `CaseFile.objects.select_for_update().get(pk=case.pk)` first inside `transition`'s atomic block,
then the checks and the save on that row (and refresh the caller's instance).

### 6. The platform's moves recorded as the person's

`record(request, actor=None, …)` takes `request.user` (`apps/audit/services.py:44`). `record_assessment` runs inside
the person's request and calls `transition` with no actor, so the system's DRAFT → ORIENTED and ORIENTED →
REVIEW_REQUIRED carry the person as actor (`test_probe_a_platform_move_made_inside_a_request_is_recorded_as_the_persons`).
The timeline then says «Vous». This is harmless for «chi ha sospeso», because the platform never suspends, but rule 3
asks the trail for the actor.

### 7. The words of a held file (copy packet B1)

None of these misstates the file's state; they are where the screens could be truer:

- **(a) A closed file's «Mes documents» empty state** reads «Ne téléversez que les documents qui vous sont demandés …
  la liste apparaîtra ici avec l'état de chacun». The branch draws it newly: before, a closed file's owner had no file
  on the dashboard. On a read-only file it invites an upload and promises a list.
- **(b)** The closed file's page: «Aucune action ne vous est demandée pour l'instant». This is the notes' word 4; I agree.
- **(c) A suspended file's own page** names «Votre prochaine action — Passeport en cours de validité» while its
  dashboard panel names none. The notes keep next actions on a suspended file on purpose, but the two screens now
  disagree on whether something is asked.
- **(d)** «Votre dossier» three times on the suspended dashboard: eyebrow, primary and the Dossier strip's link. This is
  the notes' word 3.

## Every vector of the brief

| Vector | What was tried | Result | Tests |
|---|---|---|---|
| The person, every state × every target | **Setups:** 10 states, plus SUSPENDED made by the person, the operator, the administrator and the platform (previous = ADMIN_PROCESS). **Targets:** every state, POSTed to the transition view; database and trail read back | **Active state:** SUSPENDED (with a reason) and CLOSED only. **Own suspension:** the previous state and CLOSED. **Anybody else's:** CLOSED. **CLOSED:** nothing (403). One event + one notification per move, none per refusal | `test_every_account_every_state_every_target_through_the_view[owner]` |
| Forged targets | 16 junk values (empty, case variants, padding, NUL, newline, `;`, 5 000 characters, Arabic, `None`, `__all__` …), a doubled `status` field, extra fields (`as_authorised_actor`, `actor`), on four setups | nothing moved, no event | `test_the_person_forges_junk_and_doubled_targets` (4) |
| Method, CSRF | POST without a token; GET | 403; 405; nothing moved | `test_the_transition_view_is_post_only_and_csrf_protected` |
| Resuming somebody else's suspension | made by the operator, the administrator, the platform | no resume offered; every active target refused; `resume()` raises; CLOSED stays open to the person. The latest suspender decides; the person's own resume goes back only to where the file was | `test_the_person_cannot_lift_…` (3), `test_an_unattributable_…`, `test_the_person_lifts_their_own_…` |
| Each assignee role, live / revoked / expired | operator and professional live; authorised actor and training body live; operator and professional revoked and expired; authorised actor expired | **Live operator / professional:** exactly their §4 rows. **Live authorised actor / training body:** 403 on every POST (the policy). **Revoked / expired:** 404 | matrix (9 accounts) |
| Staff without assignment | role:staff (staff flag), role:operator (staff flag) and role:professional unassigned, a stranger | 404 everywhere | matrix (4) |
| The administrator, a superuser | the matrix, then §4 strictly | every declared move: finding 1 | matrix (2), two probes |
| The back office | `person`, assignment `role` / `assignee` / `case`, `suspension_reason`; `status` and its trace posted by a superuser; bulk actions; adding an assignment; the administrator role's access | capacities editable (finding 2). `status` not writable; no action moves a file; the operator cannot add an assignment; role:administrator has no `cases` permission (403) | `test_review_backoffice.py` (4 probes, 4 held), also on the merged tree |
| The authorised actor's path | `open_process`; `conclude` by a co-operator through the view; the person concluding; the authorised actor on the case page; the operator without its role; a stranger holding the role; read-only CLOSED; a revoked case assignment | one event per move, actor named; person 403; the case page 403; fail-closed; read-only holds; finding 4 | `test_review_selection.py` (7 held, 1 probe) |
| The platform's path | `record_assessment` (DRAFT → ORIENTED, ORIENTED → REVIEW_REQUIRED; a STOP never advances), the reassessment (active files only), the questionnaire on a suspended file (opens a second file: Q11, pre-existing) | §4's «sistema» rows only; finding 6 for the actor recorded | code read; probe |
| Management commands, seeds | 27 command modules | none references a case (only `rules_activate_demonstration` calls a `transition`, on rules). `selection.chain` walks ORIENTED → TRAINING on the platform path, gated by `demonstration_data_allowed()` | source scan |
| Any other writer | views, forms, API, signals, the audit trail | outside `cases.services`, only `cases.intake` (the pathway key) and the admin write a file. No ModelForm, no API endpoint. «case.transition» is written by `cases.services` alone (dynamic actions are namespaced `community.*`). `AuditEventAdmin` refuses add / change / delete even to a superuser, so «who suspended» cannot be forged | source scan |
| `transitions_available` never offers a refused target | 21 accounts × 14 setups, plus suspended rows whose `previous_status` is empty, CLOSED or SUSPENDED. The 21 are the cast's 16 and five edge accounts: an administrator assigned as professional; one assigned as training body; an operator-and-professional; a training body newer than an operator; an operator newer than an authorised actor. The owner is also made its own file's operator | offered == accepted everywhere. An administrator assigned as professional acts as the professional, and as training body gets nothing (the policy's first live assignment). The owner-operator acts as the person | `test_offered_equals_accepted_…` (4), `test_edge_accounts_…` |
| Concurrency | a move computed on a stale row | finding 5 | probe |

## The legitimate flows — kept

- **The person:** suspends with a reason, closes from any state, and lifts a suspension they made back to where the
  file was, through the view.
- **The operator:** ORIENTED → REVIEW_REQUIRED / TRAINING / ADMIN_PROCESS, ADMIN_PROCESS → PRE_DEPARTURE,
  PRE_DEPARTURE → ENTERED, POST_ENTRY → CLOSED, suspends, and lifts its own suspension.
- **The professional:** REVIEW_REQUIRED → ORIENTED / TRAINING. All through the view.
- **The authorised actor:** opens a selection; a co-operator concludes it to ADMIN_PROCESS or back to TRAINING.
- **CR-03:** binds the administrator, the superuser and the platform's path.
- **CLOSED:** read-only for all 16 accounts, in the domain and on the page (no state control).
- **The suspension reason:** required for four accounts × three blanks, stored stripped, cleared on resume. A
  whitespace reason is refused through the view.
- **Audit and notifications:** one `case.transition` per move (actor, from, to, reason) and one notification. A move a
  French-speaking operator makes reaches the person in **their** language (ar, it, en: subject and state label).
- **Status codes:** the policy's 403 and the stranger's 404 are unchanged.
- **The builder's suites, re-run here** on lane 7, browser tests excluded: 713 passed, 3 skipped, for
  `apps/cases apps/selection apps/portal tests/security tests/frontend/test_dashboard_w3_b.py`
  `tests/frontend/test_journey_w3_d.py -m "not browser"`. Two `caplog` tests errored in my first run only because I
  had disabled pytest's logging plugin; re-run with it, both pass. The builder's two new modules: 73 passed.
- **Integration:** the branch merges cleanly into design-v5 `f447c28` (`git merge-tree`: no conflict; no path in
  common with sec-f5's merge).

## Part B — the dashboard of a held file

- **Truth, privacy and grammar, on 20 pages:** five held states × fr, ar, en and it. The states are suspended by the
  person, by an operator, by the administrator; closed by the person; closed by an operator from POST_ENTRY. On each:
  - 200, no «pas encore de dossier», no door;
  - **exactly one raised panel** (`card card--action`), `data-now` = suspended / closed, and the panel leads to the
    file;
  - suspended: **the reason once on the page** (the Dossier strip's notice steps aside) and no questionnaire;
  - closed: the questionnaire, which opens a new file, and the file;
  - the head: the reference and the state's chip with its register (`data-register`);
  - the journey: nothing «here» (no `aria-current="step"`, no «Vous êtes ici»);
  - **nothing the person may not read:** a professional's internal help-desk note on the file, the assignments'
    mandate notes and the operator's e-mail address never appear.
- `held_case` is pinned to the owner: an assignee, the administrator and a stranger get no held file on their
  dashboard. An active file always wins. A closed file's pieces are listed without «Déposer» / «Remplacer».
- The reason is drawn as text: a reason carrying `<script>` and an `onerror` image comes out escaped on the panel in
  fr and ar (the `typo` filter keeps a plain string plain).
- **Live words:** the seven msgids the fix draws are present, translated, neither fuzzy nor obsolete, and compiled in
  fr, ar, en and it. They are «Votre dossier», «Dossier suspendu», «Commencer le questionnaire», «Un fascicolo concluso
  non si riapre: se ne apre uno nuovo.», «Sospeso», «Percorso concluso» and the refusal.
- **Grammar:** the held variants draw the panel's base card. No stylesheet targets `db-now--suspended` / `--closed`,
  and the company's panel uses neither name.
- **The builder's 14 captures, looked at:** the dashboards in fr and ar at 1440 and 390, and the case pages. All 200,
  no console error, no overflow. The Arabic panel is mirrored, with the French reason in its own direction. The
  suspended page offers its previous state and CLOSED only.
- The words that could be truer: finding 7.

## Outside this fix — observations, not findings

- **The lifecycle's tail has no performer.** ENTERED → POST_ENTRY is «sistema — automatica» and nothing performs it.
  Operators made it by hand before; now only the administrator can (Q5). An operator-run file therefore stops at
  ENTERED, and the operator's POST_ENTRY → CLOSED is out of reach without the administrator. The training body, named
  for ORIENTED → TRAINING, holds no «change» (Q2). The professional no longer suspends or closes (Q7). These are
  narrowings, all in the notes, and the owner's to answer.
- **CR-03's check does not look at the role.** `CaseFile.has_valid_authorised_actor` filters on a reference and a
  validity, so an OPERATOR assignment carrying a reference satisfies it
  (`test_probe_cr03_counts_any_assignment_that_carries_a_reference`). `services.assign` accepts a reference on any role,
  and with finding 2 an operator could type one into its own assignment. The branch does not weaken this, but the
  hardening pass should filter `role=AUTHORISED_ACTOR`.
- **The policies' administrator branch ignores read-only.** On a CLOSED file the transition view answers the
  administrator 302 plus the domain's refusal, and the owner 403. The checklist policy lets an administrator change a
  closed file's lines. Neither is a state change.
- **Q11 and Q12 confirmed by reading.** The questionnaire's own entry still opens a second file beside a suspended one.
  `conclude` revokes only the concluding operator's assignment.

## Reproduce

```
# the branch (expected on 9a9bb5c: 11 failed — the probes: findings 1-6 and the CR-03 observation — 78 passed)
cd C:/tmp/ile_wt/v54-sec-f7
TEST_DATABASE_URL=postgres://ile:ile-dev-password@127.0.0.1:5439/ile_v5_l7 PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 \
  C:/tmp/italylegalentry/.venv/Scripts/python.exe -m pytest -c pyproject.toml --rootdir . -p no:randomly -p no:cacheprovider \
  C:/tmp/ile_v5_council/.work/sec-f7/review/test_review_f7.py C:/tmp/ile_v5_council/.work/sec-f7/review/test_review_backoffice.py \
  C:/tmp/ile_v5_council/.work/sec-f7/review/test_review_selection.py C:/tmp/ile_v5_council/.work/sec-f7/review/test_review_dashboard.py \
  C:/tmp/ile_v5_council/.work/sec-f7/review/test_review_extra.py
# the merged tree / the control: copy the worktree's .env into the extracted tree (removed after my runs), then run
# from it with REVIEW_ROOT set to it
#   review/merged_tree     (design-v5 f447c28 + v54-sec-f7, git merge-tree ebccc2d)
#   review/control_fec37d3 (design-v5 before the fix)
```

## Not done

- No change to the branch's code or tests: I review, I do not build. This file is the only one added, and it is not
  committed.
- The full suite was not run, nor the browser suites. The template change is one condition, and the builder ran the
  dashboard's 27 browser tests and the portal's 8. The areas the change reaches were run: my 89 tests and the builder's
  suites above.
- No lane server was started; the builder's captures were looked at instead.
