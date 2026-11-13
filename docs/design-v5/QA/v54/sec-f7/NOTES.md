# sec-f7 — WHO may move a case file (finding F-7) and the dashboard of a held file — notes

A security / domain-integrity fix, not design work (V5.5 delivery mode; V5.9: nothing deployed, production untouched).
Branch `v54-sec-f7`, worktree `C:/tmp/ile_wt/v54-sec-f7`, from design-v5 at `fec37d3`. Implementer `sec-f7-fix`,
15 October 2026. Lane 7: dev server 8787 from this worktree on `ile_v5_l7` (`DB_CONN_MAX_AGE=0`, `--noreload`, no
preview flag, no reference date); pytest on `test_ile_v5_l7`, one run at a time, `-p no:randomly`. Scratch scripts,
logs and captures outside every repository: `C:/tmp/ile_v5_council/.work/sec-f7/`.

## 1. The finding, its root cause, the reproduction

**F-7** (W3-D's review, confirmed by the orchestrator on design-v5 `fec37d3`): `cases.policies.case_policy` gives the
file's owner «change» while the file is active, and `cases.services.transition` / `transitions_available` filtered
only by the declared graph (`models.transitions_from`) and that object policy — never by WHO may make each move. So a
person could move their own file ORIENTED → ADMIN_PROCESS («Procédure administrative en cours»), ADMIN_PROCESS →
PRE_DEPARTURE, PRE_DEPARTURE → ENTERED, and TRAINING → SELECTION whenever an authorised actor was assigned (a reserved
activity, CR-03) — and the journey «La soglia» then drew it as a fact. The approved specification is
`docs/platform/CASE_LIFECYCLE.md` §4, the «Chi può» column, and its rule 2: «Una transizione non dichiarata in questa
tabella è rifiutata dal dominio, non solo nascosta nell'interfaccia».

**Root cause.** The column existed only in the document. The domain had the WHAT (`ALLOWED_TRANSITIONS`) and a
whole-file permission («change»), and nothing between them; the case page offered every declared move to every account
holding «change» (the owner, a professional or operator assignee, the administrator).

**Reproduced first** — `apps/cases/tests/test_transition_actors.py::TestTheFindingReproduced`, 12 tests, all failing on
`fec37d3` before any code changed (`.work/sec-f7/repro_before_fix.txt`): the person moves ORIENTED → ADMIN_PROCESS,
ADMIN_PROCESS → PRE_DEPARTURE, PRE_DEPARTURE → ENTERED and TRAINING → SELECTION (with a valid authorised actor
assigned) through the transition view; `transitions_available` offers the person those targets; `services.transition`
accepts them with the person as actor.

## 2. The fix — the column as data, enforced by the domain

### 2.1 The table as implemented (`apps/cases/models.py`, beside `ALLOWED_TRANSITIONS`)

`TransitionActor` names the capacities: `person` (the owner), the four `AssignmentRole` values (`professional`,
`authorised_actor`, `training_body`, `operator` — an assignee acts in the capacity of its live assignment),
`administrator`, `system` (the platform: `transition` called without an actor). `TRANSITION_ACTORS` names, for every
row the graph declares, the capacities BESIDE the administrator; `transition_actors(status, target)` adds the
administrator to every declared row («o superiore») and returns nothing for an undeclared one.

| From | To | Who (§4) | As implemented |
|---|---|---|---|
| DRAFT | ORIENTED | sistema | system |
| ORIENTED | REVIEW_REQUIRED | sistema, operatore | system, operator |
| ORIENTED | TRAINING | operatore, ente formativo | operator, training body (named; not granted — §2.2) |
| ORIENTED | ADMIN_PROCESS | operatore | operator |
| REVIEW_REQUIRED | ORIENTED | professionista | professional |
| REVIEW_REQUIRED | TRAINING | professionista | professional |
| TRAINING | SELECTION | soggetto autorizzato | authorised actor (the selection service's path — §2.3) |
| SELECTION | ADMIN_PROCESS | soggetto autorizzato | authorised actor (idem) |
| ADMIN_PROCESS | PRE_DEPARTURE | operatore | operator |
| PRE_DEPARTURE | ENTERED | operatore | operator |
| ENTERED | POST_ENTRY | sistema | system |
| POST_ENTRY | CLOSED | operatore, persona | operator, person (`CLOSE_ACTORS_FROM`) |
| any active | SUSPENDED | persona, operatore, amministratore (DRAFT: persona, operatore) | person, operator (`SUSPEND_ACTORS`) |
| SUSPENDED | the previous state | chi ha sospeso, o superiore | the account that suspended (from the audit trail — §2.4) |
| any | CLOSED | persona, amministratore | person (`CLOSE_ACTORS`) |
| REVIEW_REQUIRED → ADMIN_PROCESS · TRAINING → ADMIN_PROCESS · TRAINING → ORIENTED · ADMIN_PROCESS → REVIEW_REQUIRED · PRE_DEPARTURE → ADMIN_PROCESS | | *not in §4* | nobody beside the administrator (Q1) |
| SELECTION | TRAINING | *not in §4* | authorised actor — `selection.services.conclude` (a selection that ends without a referral) (Q1) |
| SUSPENDED | any other active state | *not in §4* (§4: the previous state only) | nobody beside the administrator (Q1) |

The administrator (and a superadmin) is on every declared row. `test_the_data_says_what_section_4_says` reads §4's
table from the document itself and checks every row against the data (17 rows; the rows §4 does not declare must stay
empty but for SELECTION → TRAINING) — the day the owner changes the table, the test says the data must follow.

> Superseded by «Review fixes», finding 1: the administrator is now on the rows §4 names it for and on the two
> `BEYOND_SECTION_4` declares; the rows marked «nobody beside the administrator» above are nobody's; the doc test
> compares the administrator too.

### 2.2 The effective right — the object policy AND the column, never one without the other

`cases.services.permitted_transitions(case, user)`: nothing on a read-only (CLOSED) file; nothing without the object
policy's «change» (`cases.policies.case_policy`, unchanged); then the capacities the account stands in towards the file,
read as the policy reads them (`_capacities`: a superadmin is the administrator; otherwise the owner is the person,
whatever else the account holds; otherwise every live assignment's role; otherwise an administrator), intersected with
the capacities whose «change» comes from that policy (person, professional, operator, administrator), and the column
for each declared row. **This fix widens nobody's access**: the training body and the authorised actor, whom the column
names and the policy refuses «change», get nothing on the case's path (Q2, Q3). Per role, on a file whose authorised
actor is assigned (so CR-03 never blocks SELECTION) — the same map `test_every_role_is_offered_exactly_what_the_domain_accepts`
asserts:

| Role | Moves offered and accepted |
|---|---|
| the person (owner) | any active state → SUSPENDED (a reason required, as before) or CLOSED; SUSPENDED → its previous state if THEY suspended it, and → CLOSED |
| operator (live assignee) | ORIENTED → REVIEW_REQUIRED / TRAINING / ADMIN_PROCESS; ADMIN_PROCESS → PRE_DEPARTURE; PRE_DEPARTURE → ENTERED; POST_ENTRY → CLOSED; any active → SUSPENDED; SUSPENDED → previous if it suspended it |
| professional (live assignee) | REVIEW_REQUIRED → ORIENTED / TRAINING — nothing else (Q7) |
| administrator, superadmin | every declared move of the graph (SUSPENDED → any active state or CLOSED included) |
| authorised actor, training body | nothing on the case page or through `transition(actor=…)` (the view answers 403, as before) |
| a stranger | nothing (404, as before) |

> Superseded by «Review fixes», finding 1, for the administrator and a superadmin: any active state → SUSPENDED, any
> state → CLOSED, SUSPENDED → the state it left, SELECTION → TRAINING and ENTERED → POST_ENTRY — nothing else.

`transition(case, target, actor=…, …)`: after the existing graph check, whenever an actor is given, a target outside
`permitted_transitions` raises **`TransitionNotPermitted`** (a `TransitionRefused`, so a `ValidationError`: the view
turns it into the domain's message, never a 403 from the service; the 403 stays the object policy's, in the view). The
message is the domain's existing sentence «Transition non autorisée de « X » à « Y ». » — already in fr/ar/en/it, no new
copy. **`actor=None` stays the platform's path**, unchecked as before: the orientation service (`record_assessment`:
DRAFT → ORIENTED, ORIENTED → REVIEW_REQUIRED), the selection seeds (ORIENTED → TRAINING), the tests' set-ups.
`transitions_available` is `permitted_transitions` minus what CR-03 still blocks, in the lifecycle's order (it used to
follow a frozenset's iteration order).

### 2.3 The authorised actor's moves — the selection service's path, made explicit

`selection.services.open_process` (TRAINING → SELECTION) and `conclude` (SELECTION → ADMIN_PROCESS or back to
TRAINING) move the file with `actor=operator` — an operator of the authorised actor, assigned as AUTHORISED_ACTOR, whom
the case policy gives no «change» («an authorised actor acts on the selection process, not on the case file»). Under
«policy AND column» those calls would have been refused. They now pass **`as_authorised_actor=True`**: the case domain
then accepts only the column's authorised-actor rows, only for an account holding the authorised actor's role, only on a
file holding an unrevoked AUTHORISED_ACTOR assignment (`_authorised_actor_transitions`; a fresh query, because the
selection service assigns the actor a moment before it moves the file). WHICH authorised actor may act on WHICH process
stays the selection service's answer (a live operator of the actor under a live mandate: `is_operator`), and CR-03's
own check still guards the way into SELECTION. Not a per-user assignment check: any live co-operator of the actor may
conclude a process (`conclude` is called with `request.user`), and a co-operator holds no assignment of their own.

> Amended by «Review fixes», finding 4: the way back to TRAINING no longer needs the assignment standing (a selection
> whose assignment was revoked while its process was open can still be concluded without a referral).
`conclude` now moves the file BEFORE it revokes the mandate's assignment (the move is made while the mandate stands);
the selection suite's assertions are on final states and pass unchanged. Without the flag the same account is refused:
the case page offers it no control and the case's transition view answers 403, as before.

### 2.4 «Chi ha sospeso» — the audit trail, not a new column

> Amended by «Review fixes», finding 3: only THIS suspension's event answers (created since `status_since`, its
> `from` the file's `previous_status`).

`cases.services.suspended_by(case)` reads the actor of the latest `case.transition` event whose `to` is `suspended`.
**Choice: the audit trail, no migration** — it is reliable for this: `transition` writes the event inside the same
atomic block as the move (a status and its event commit together or not at all); no screen edits or deletes an event
(`audit.admin` refuses add, change and delete) and no job purges them; the event names the account the move was made by
(`record(actor=…)`). It also covers the files suspended before this fix, which a new nullable column would not. When
the trail cannot attribute the suspension — the platform's path, a seeded file, an account since deleted (the event's
actor is `SET_NULL`) — only the administrator lifts it («o superiore»). «Superiore» is read as the administrator alone
(Q4). `makemigrations --check`: «No changes detected».

## 3. Every other way a case's status can change — checked

| Path | Finding |
|---|---|
| `cases.views.transition` | `require(change)` then `services.transition(actor=request.user)` — now refused by the column (the reproductions) |
| `cases.services` | the only writer of `CaseFile.status` (`transition`; `open_case` creates DRAFT); `resume` goes through `transition` (the «who suspended» rule applies) |
| `cases.services.record_assessment` / `cases.intake` / `portal.reassess_person` | platform path (`actor=None`), fixed targets computed by the engine — unchanged |
| `selection.services.open_process`, `conclude` | the authorised actor's path, explicit (§2.3) |
| Django admin / unfold back office (`/backoffice/`, `CaseFileAdmin`) | `status`, `previous_status`, `status_since`, `closed_at` read-only, not in the form; no custom action (only Django's `delete_selected`, behind the delete permission); a suspended file's reason cannot be emptied (`CaseFile.clean`) — now pinned by `TestTheBackOffice`. Not a status path but noted (Q10): the assignment inline is editable |
| management commands | none touches a case status (`documents_refresh_requirements` moves document requirement states only) |
| seeds | `selection.seeds` walks DRAFT → ORIENTED → TRAINING on the platform's path; `documents` / `helpdesk` seeds read files |
| signals | none moves a status (`helpdesk.receivers` opens a ticket on a REVIEW_REQUIRED assessment) |
| API (`apps/integrations`) | no case endpoint |
| forms | no ModelForm of `CaseFile` outside the admin |
| data migrations | `cases/migrations/0001_initial` only |
| direct ORM writes | none outside `cases.services` (searched: `.status =`, `update(status`, `status=CaseStatus.`) |

## 4. The dashboard of a person whose latest file is suspended or closed

**Before:** W3-B's dashboard told such a person «Vous n'avez pas encore de dossier…» and offered the questionnaire,
because `portal.services.active_case` keeps the active statuses only (NOW_NO_CASE) — and for a suspended file the
questionnaire would open a second file beside it (`cases.intake.case_for_purpose` reads the active files only).

- `portal.services.held_case(user)`: the latest SUSPENDED file (it can still move), else the latest CLOSED one, through
  `readable_by`. `dashboard_context` uses `active_case(user) or held_case(user)`; for a held file: no next action, no
  overdue date taking the panel over (the dates stay listed in «Mes échéances»), the journey from the trail (W3-D's
  `cases.presenters.journey_with_dates`: the steps it reached behind it, the stop marked, nothing «here»).
- The template already drew a held file once `case` was set: the head's reference, its state's chip (`cases.CaseStatus`)
  and «depuis le», «Dossier» with «Votre dossier», even the suspension notice (dead code until now).
- **The NowPanel's two held variants** (`_held_now`; no CSS: they draw the panel's base card):
  - `suspended` — eyebrow «Votre dossier», title «Dossier suspendu», the reason as text (the pairing the case file's
    header uses, `portal/partials/case_header.html`; the reason in the words of whoever suspended, `dir="auto"` — W3-B's
    own-words rule), primary «Votre dossier» → the file; no questionnaire.
  - `closed` — eyebrow «Votre dossier», title the state's label «Parcours clôturé», the domain's sentence «Un dossier
    clôturé ne se rouvre pas : on en ouvre un nouveau.» (msgid «Un fascicolo concluso non si riapre: se ne apre uno
    nuovo.»), primary «Commencer le questionnaire» (the questionnaire opens the new file), secondary «Votre dossier».
- **The one template change** (`templates/portal/dashboard.html`): the «Dossier» section's suspension notice steps aside
  when the NowPanel draws the reason (`now.variant != "suspended"`), so the reason is drawn once.
- **One click further** (seen on the lane): the closed file's own page still announced «Votre prochaine action —
  Passeport en cours de validité». `cases.services.next_action` now returns None for a read-only file (§4 rule 5): the
  case page falls to its existing empty state, the dossiers' list and the documents register name nothing on it. A
  suspended file keeps naming its obligations (its reason is often one of them). No template change.
- **The other `active_case` callers**, read one by one: `reassess_person` — active files only, on purpose (a closed file
  is never reassessed; a suspended one waits): unchanged. «Ma situation» passes `case` but blanks the case header: inert,
  unchanged. «Mon parcours» (`pathways_page`) draws no journey for a held file — silent, not false; left to the
  secondary pages' family (W3-E) to decide, the rail would need no new word (handed over below).

## 5. Questions for the owner (and the documents)

- **Q1 — the moves the graph declares and §4 does not.** *(Updated in «Review fixes», finding 1: now nobody's.)* REVIEW_REQUIRED → ADMIN_PROCESS, TRAINING → ADMIN_PROCESS,
  TRAINING → ORIENTED, SELECTION → TRAINING, ADMIN_PROCESS → REVIEW_REQUIRED, PRE_DEPARTURE → ADMIN_PROCESS, and
  SUSPENDED → any active state other than the previous one. Rule 2 would refuse them; the graph keeps them, the
  administrator alone may make them (SELECTION → TRAINING also the authorised actor, through `conclude`). Before F-7 a
  person, a professional or an operator could make them all. Either §4 gains these rows with their actors, or the graph
  loses them.
- **Q2 — the training body** (ORIENTED → TRAINING: «operatore, ente formativo»). The object policy gives a training body
  no «change» on the file («sees training data only»); not granted. A path like the authorised actor's (a training
  service), or §4 corrected.
- **Q3 — the authorised actor** (TRAINING → SELECTION, SELECTION → ADMIN_PROCESS): through the selection process only,
  never the case page. Confirm the reading; §4 could say «tramite il processo di selezione».
- **Q4 — «chi ha sospeso, o superiore».** Implemented: the account that suspended, or the administrator. Not
  implemented: an operator lifting a person's own suspension (is the operator «superiore» to the person, against the
  person's choice to pause?), another operator of the same file lifting a colleague's suspension.
- **Q5 — ENTERED → POST_ENTRY, «sistema — automatica».** *(Updated in «Review fixes», finding 1: a declared departure.)* Nothing performs it automatically; before F-7 an operator
  made it by hand, now only the administrator (and the platform's path). Should the platform chain it when the entry is
  recorded, or should §4 name the operator?
- **Q6 — leaving SUSPENDED «con motivazione».** §4's condition column asks a reason for the way back too; the domain
  asks one only to suspend (`resume` passes none). Unchanged.
- **Q7 — the professional** may no longer suspend or close a file (§4 does not name them for either); **Q8 — the
  operator** closes only from POST_ENTRY («qualunque → CLOSED» names the person and the administrator; «per decadenza»
  is the administrator's). Both narrowings follow §4; confirm.
- **Q9 — an administrator who owns a file** acts on it as its owner (the policy's owner branch comes first); kept.
- **Q10 — outside F-7, for the back-office hardening:** *(Done in «Review fixes», finding 2.)* `CaseFileAdmin`'s assignment inline lets an account with the
  model permission `cases.change_*` (role:operator) edit an assignment's role, validity and revocation without
  `services.assign` / `revoke_assignment` (no audit event of the domain, no notification): it changes WHO holds a
  capacity on a file, not its status.
- **Q11 — pre-existing:** a suspended file's owner who takes the questionnaire again opens a second file for the same
  purpose (`case_for_purpose` reads active files only); the dashboard no longer offers it, the questionnaire's own
  entry still does.
- **Q12 — pre-existing:** `selection.services.conclude` revokes only the concluding operator's assignment; a co-operator
  concluding a process another operator opened leaves the opener's AUTHORISED_ACTOR assignment live.

## 6. Words — none invented

Every word drawn by this fix is an existing catalogue entry (fr/ar/en/it): «Votre dossier», «Dossier suspendu», the
state labels («Sospeso», «Percorso concluso»), «Un fascicolo concluso non si riapre: se ne apre uno nuovo.»,
«Commencer le questionnaire», «Transizione non consentita da «%(from)s» a «%(to)s».». Missing — for the owner's copy
packet B1, not written:

1. **The refusal says what, not who.** A refused move reads «Transition non autorisée de « X » à « Y ». »; a sentence
   naming who records that step («Cette étape est enregistrée par l'équipe du projet.» or similar) would be clearer.
2. **Lifting one's own suspension** is offered as the state's label in the case page's select («Orientation terminée»,
   the previous state); a verb («Reprendre le dossier») would say what it does.
3. **The suspended NowPanel** says «Votre dossier» twice (eyebrow and primary); a distinct verb for the primary
   («Ouvrir le dossier») would read better.
4. **The closed file's case page**, with no next action, falls to «Aucune action ne vous est demandée pour l'instant.»;
   «pour l'instant» suggests later — a closed-file sentence would be truer.

## 7. Tests

- New: `apps/cases/tests/test_transition_actors.py` (60 tests: the reproductions; §4 read from the document against
  the data; every role × every state — 13 set-ups, 8 accounts — the page's offer = what `transition` accepts = the
  column; the case page's options = what its view accepts; each role's moves kept; the authorised actor's path open to
  it alone; the platform's path unchanged; audit and notification unchanged; CLOSED read-only for everybody; CR-03
  still binding the administrator; the back office) and `apps/portal/tests/test_held_file.py` (13 tests: both held
  states in fr and ar — presenter and page —, precedence, the empty state kept for a person with no file, the overdue
  date kept in its list, another person's file never drawn, the reassessment unchanged, the closed file's own page).
- Changed: `apps/cases/tests/test_views.py::test_every_transition_is_audited` audited a DRAFT → ORIENTED made by the
  owner — a move §4 gives the system alone, now refused — and audits the owner's suspension instead (actor, from, to,
  reason).
- Results: see §9.

## 8. The lane — what was done

Two synthetic persons created on `ile_v5_l7` by `.work/sec-f7/personas.py` (unusable passwords), their files moved
THROUGH THE DOMAIN: `secf7-suspended` (`6702D178E6`, suspended by its owner, «En attente de la copie du passeport»),
`secf7-closed` (`DC4030348F`, closed by its owner); `qa-person` (`E46E03B461`, oriented) read only. Sessions minted with
`Client.force_login` (`.work/sec-f7/sessions.py`; no password used, typed or stored). Captures with headless Chromium
(Playwright), full page, in `.work/sec-f7/captures/` — all looked at: the two dashboards in fr and ar at 1440 and 390
(the head's chip, the held NowPanel, the journey stopped where the trail stopped, nothing «here», the reason once, the
Arabic mirrored with the French reason in its own direction on the panel's reading edge, the closed panel's
questionnaire and file); the suspended file's case page (fr, ar; 1440, 390: the select offers its previous state and
CLOSED only), the closed file's (no control, and after the `next_action` change no «Votre prochaine action»),
`qa-person`'s (oriented: CLOSED and SUSPENDED only — before F-7 it also offered REVIEW_REQUIRED, TRAINING and
ADMIN_PROCESS). 14 loads: 200, 0 console errors, 0 horizontal overflow. Cleaned at the end (§9).

## 9. Results and hand-over

**Tests** (pytest on `test_ile_v5_l7`, one run at a time, `-p no:randomly`; the machine shared with two other teams'
suites on their own lanes):

| Run | Result |
|---|---|
| the reproductions, before any code changed (`fec37d3`) | 12 failed — F-7 confirmed (`.work/sec-f7/repro_before_fix.txt`) |
| `apps/cases apps/selection apps/portal apps/notifications tests/security tests/test_phase_console.py tests/frontend/test_design_docs.py tests/frontend/test_dashboard_w3_b.py tests/frontend/test_journey_w3_d.py tests/frontend/test_documents_w3_c.py` (portal browser file apart) | **897 passed, 3 skipped** (18 min 31 s; `.work/sec-f7/suite_nonbrowser.log`) |
| `apps/portal/tests/test_browser.py` | **8 passed** |
| `tests/frontend/test_dashboard_browser_w3_b.py` (the dashboard template was touched) | **27 passed** |
| `apps/cases/tests/test_transition_actors.py` after the last comment edit | 60 passed |
| `ruff check .` (what CI runs) · `manage.py makemigrations --check` · `manage.py check` | clean · «No changes detected» · no issue |

**Commits** on `v54-sec-f7` (LF, each ending with the co-author line): the domain fix with its tests
(`0168c4b`); the back office pinned (`ef1d545`); the dashboard of a held file (`290c5ae`); a closed file names no next
action (`045fad3`); CASE_LIFECYCLE.md's one line (`b955215`); these notes.

**The lane, cleaned:** 3 minted sessions revoked on `ile_v5_l7` and the secrets file removed; the 8787 server stopped
(port free); the two synthetic accounts removed (`personas.py remove`: 22 rows cascaded — their files, checklist lines,
notifications and messages; their audit events stay on lane 7 with the actor set null). `personas.py setup` recreates
both in seconds for a reviewer. Never 8780, never `ile_v5`; nothing deployed, no remote touched.

**Handed to:**

- **The steward (at merge)** — the decision-log entry; DS 2026 §11.7 says «Il NowPanel — quattro varianti»: there are
  six now (`suspended`, `closed`: §4 above; no CSS of their own); the ownership of the touched paths
  (`apps/cases/{models,services}.py` and tests, `apps/selection/services.py`, `apps/portal/services.py` and the new test,
  `templates/portal/dashboard.html` — one condition —, `docs/platform/CASE_LIFECYCLE.md` — one line).
- **W3-E (the case file and the secondary pages)** — the case page's transition control now lists only §4's moves (a
  person: suspend, close, and the way back from a suspension they made, labelled with the previous state's name: word 2
  of §6); a closed file's page falls to «Aucune action ne vous est demandée pour l'instant.» (word 4); «Mon parcours»
  draws no journey for a held file — `cases.presenters.journey_with_dates(portal.services.held_case(user))` would draw
  it with no new word, if the family wants it there.
- **The back-office hardening (sec-f5's area) or the owner** — Q10 (the assignment inline).
- **The owner** — Q1–Q12 (§5) and the four missing words (§6, copy packet B1).

## Review fixes

Lane `sec-f7-fix2` (security implementer), 16 October 2026, on top of `9a9bb5c`. The independent review
(`REVIEW.md`, lane `sec-f7-review`, committed with this section) found F-7 closed for the person with nothing
regressed — verdict SHIP_AFTER_FIXES, nothing blocking. It raised two major findings in F-7's own subject, who may move
a file, five minor ones and one observation (CR-03). Both major findings, the four code minors and the observation are
fixed, each with its tests. Finding 7 is words; it goes to the owner's copy packet B1 unchanged. The hard limits held:
nothing deployed, no server or remote touched, no package added, no word added to a catalogue, personas only through
`Client.force_login`, one pytest at a time on `test_ile_v5_l7` with `-p no:randomly`. Scratch and logs:
`C:/tmp/ile_v5_council/.work/sec-f7/fix2/`.

| # | Finding | Commit | Fix | Tests (`apps/cases/tests/test_transition_actors.py` unless named) |
|---|---|---|---|---|
| 1 | major — the administrator on every declared row: from the case page it opened SELECTION and concluded it (CR-03), claimed an orientation (DRAFT → ORIENTED) and a professional review, made the operator's moves, the five rows §4 does not declare and SUSPENDED → any state | `949074b` (`659be72`: a test's name) | `transition_actors` returns the data and adds nobody. Every row names every capacity, the administrator only where §4 names it (`SUSPEND_ACTORS`, `CLOSE_ACTORS`, the new `RESUME_ACTORS`). `BEYOND_SECTION_4` lists the only capacities beyond §4, each with its reason: SELECTION → TRAINING (authorised actor, administrator), ENTERED → POST_ENTRY (administrator) | `test_the_data_says_what_section_4_says` (now with the administrator: every move, out of SUSPENDED towards each state it may have left, equals the union of §4's matching rows plus `BEYOND_SECTION_4`); `test_every_departure_from_section_4_is_declared_with_its_reason`; `test_nobody_is_on_an_undeclared_move_…`; `test_the_administrator_makes_only_the_moves_section_4_names_for_it` and `test_the_administrator_neither_opens_nor_concludes_a_selection_from_the_case_page` (the reviewer's two probes); `…_claims_no_orientation_and_no_professional_review`; `…_still_ends_a_selection_without_an_outcome_and_starts_the_accompaniment`; the matrix and the case-page test (administrator and superuser now explicit) |
| 2 | major — the back office hands out capacities: role:operator made itself a file's owner and closed it, turned its assignment into a professional's and concluded a review, took over another file's assignment and moved that file, rewrote a suspension's reason — no domain event, no notification | `5020315` | `CaseFileAdmin`: `person` and `suspension_reason` read-only, no add form. `AssignmentInline`: shown, never edited. `CaseAssignmentAdmin`: the add form grants through `services.assign`; on a live assignment only «revocato il» is editable, only for an account the assignment's own policy lets change it, and saving it calls `services.revoke_assignment`; a revoked assignment's screen is read-only | `TestTheBackOffice` (8): the reviewer's four probes inverted, through real admin form posts; the operator ends no assignment; the administrator grants and ends one through the domain (one event, one notification each, nothing else changed in the same post) |
| 3 | minor — `suspended_by` took the latest suspension event whatever its date | `83634d4` | only this suspension's event answers: `created_at >= status_since` and `from == previous_status` | `test_does_not_lift_a_suspension_the_trail_does_not_attribute_to_them` (the reviewer's probe, plus an event of the same moment naming another departure state) |
| 4 | minor — a revoked case assignment left a selection that could not be concluded | `fa172e1` | on the selection service's path, the way back to TRAINING no longer needs the assignment standing; the referral and the way in still do | `apps/selection/tests/test_selection_exits.py` (4): the reviewer's probe; the referral refused whole; nobody else uses the way back; the administrator's way out, then the conclusion |
| 5 | minor — `transition` judged and saved the instance it was handed | `f140de6` | `SELECT … FOR NO KEY UPDATE` on the file's row first; every check on that row; the caller's instance told the row's state | `TestTheRowAMoveIsJudgedOn` (3): a stale resume refused, a stale suspension records where the file was, the lock is the move's first statement |
| 6 | minor — the platform's moves inside the person's request were recorded as the person's | `e55d5e6` | `audit.services.record(..., system=True)`: no fallback to the request's user, label «system», the request's trace kept; `transition` passes it when `actor` is None | `test_a_platform_move_made_inside_a_persons_request_is_recorded_as_nobodys` (the reviewer's probe, through `record_assessment` and the timeline); `test_an_act_somebody_makes_inside_a_request_is_still_theirs` |
| obs. | CR-03 counted any assignment carrying a reference | `d5b0ae1` | `CaseFile.has_valid_authorised_actor` counts AUTHORISED_ACTOR assignments only | `test_only_an_authorised_actors_assignment_satisfies_cr_03` (the reviewer's probe) |
| 7 | minor — words of a held file | — | the owner's copy packet B1 (below) | — |

Each new test was run against the code before its fix (the fix stashed, the test kept), and it failed there. There are
three kinds of exception:

- **Finding 1's tests.** The module cannot be imported before the fix, because it imports `BEYOND_SECTION_4`. The
  reviewer's two probes, which these tests keep, fail on `9a9bb5c` (REVIEW.md).
- **`test_an_act_somebody_makes_inside_a_request_is_still_theirs`.** It needs finding 6's new keyword.
- **Properties that held before too.** The referral refused after the assignment ended, nobody else using the way back,
  and the administrator's SELECTION → TRAINING.

**1 — what the administrator makes now.** Any active state → SUSPENDED (a reason required); any state → CLOSED; a
suspension, anybody's, back to the state the file left («o superiore», Q4); and `BEYOND_SECTION_4`'s two moves. A
superuser makes the same moves. Never again: TRAINING → SELECTION or SELECTION → ADMIN_PROCESS (CR-03: «an
administrator is not that actor», `apps/selection/admin.py`), DRAFT → ORIENTED, REVIEW_REQUIRED → ORIENTED / TRAINING,
the operator's moves, the five rows §4 does not declare, SUSPENDED → any other state. The rule read off §4: a move is
open to every capacity that a row matching it names. DRAFT → SUSPENDED («persona, operatore») is also a «qualunque attivo
→ SUSPENDED» move, so it takes the administrator. POST_ENTRY → CLOSED («operatore, persona») is also a «qualunque →
CLOSED» move, so it takes the administrator too. This is the reviewer's strict reading as well.

- **Why these two departures and no more.** SELECTION → TRAINING asserts no outcome. Without it, a selection that can
  no longer be concluded strands the file in SELECTION (finding 4); the reviewer suggested keeping it. ENTERED →
  POST_ENTRY is «sistema — automatica» in §4, and nothing performs it (Q5). Without the administrator nobody could make
  it, and the lifecycle's tail (the operator's POST_ENTRY → CLOSED) would be unreachable. The administrator stands in
  for the missing automation and asserts nothing the recorded entry does not already say.
- **The reviewer's wider option, not taken.** It suggested keeping, as explicit data, more rows for the administrator:
  the operator's and the professional's rows, the five undeclared rows and SUSPENDED → another state. The operator's and
  professional's rows name who records those facts. An administrator who must act on a file there is assigned to it
  (named and dated, as the policy wants) and then acts in that capacity, which `_capacities` already reads. An
  assigned administrator acts in its assignment's capacity only, in the policy's order, which is unchanged. A superuser
  is the administrator whatever it is assigned. For the undeclared rows, rule 2 says refused.
- **Q1, updated.** The five undeclared rows and SUSPENDED → any state other than the one it left are now **nobody's**;
  the platform's own path (`actor=None`) still makes them. Concretely: a file in ADMIN_PROCESS that needs a
  professional review cannot go back to REVIEW_REQUIRED, and a suspended file goes back only to where it was. Either
  §4 gains these rows with their actors, or the graph loses them.
- **Q5, updated.** ENTERED → POST_ENTRY is the administrator's, as a declared departure. The operator still cannot
  make it.
- `CASE_LIFECYCLE.md`'s pointer line now says the administrator appears only where the table names it, and where the
  departures are listed. It is one sentence after the rules, outside the table the test reads.

**2 — the back office.** A file's owner never changes: a new file is opened. The reason is written by the domain with
the move (§4 rules 3 and 4). An assignment's case, assignee, role and validity are the capacity: none of them changes
once granted. Revoke it and grant a new one (`ASSIGNMENT_FIELDS`).

- **Who ends an assignment there.** An account the assignment's own policy lets change it
  (`cases.policies.assignment_policy`, «only administrators create or revoke outside the services»): the administrator
  role, or a superuser. The back office used to ignore that policy and let anyone holding `cases.change_*` edit any
  assignment. role:operator now reads assignment screens and changes nothing on them. role:administrator holds no
  «cases» model permission (`accounts.roles`, unchanged), so today only a superuser grants or ends an assignment in
  the back office. Creating one was already superuser-only; it now goes through the domain.
- **No new word.** The control is the field's own label, «revocato il». Saving it calls `services.revoke_assignment`,
  which records the moment of the save whatever was typed (the class docstring says so). An admin action would have
  needed a new msgid in four catalogues while W3-E works on the same catalogues.
- **The reviewer's alternative, not taken.** It suggested narrowing role:operator's model permissions in
  `ROLE_PERMISSIONS`. The read-only fields stay in this family's app and leave the roles' grants (sec-f5's area) as
  they are.
- **Q10 is done.**
- **Observation for the back-office hardening or the owner, not fixed (outside F-7: nothing moves, no capacity is
  handed out).** `CaseFileAdmin` has no queryset limit. role:operator lists and reads every case file in the back
  office, not only those it is assigned to; `PERMISSION_MODEL.md` §5.1 says «assigned (D)», `readable_by` gives it
  nothing on the platform side. The checklist inline stays editable on any file, and a line's status changed there
  writes no `case.checklist.status` event.

**3 — «chi ha sospeso».** `transition` sets `status_since` before it writes the event, in the same atomic block, so
`created_at >= status_since` holds for the move's own event. The event's `from` is the file's `previous_status`. A
SUSPENDED row that no event of its own explains has no suspender: only the administrator lifts it. This fails closed.
No migration.

**4 — the selection.** The reviewer's first option would let the open process answer both exits. It was taken for the
way back only. A referral («esito positivo della selezione») asserts the reserved act's outcome. After an administrator
has revoked the actor's assignment on the file, cutting that actor off it, the referral is refused in the domain's
words, the conclusion rolls back whole and the process stays open. The operator may still conclude without a referral,
and the administrator may return the file to TRAINING (its declared departure). The domain still requires
role:authorised_actor on that path, and only the selection service passes the flag, after its own `is_operator` check.

**5 — the row.** `FOR NO KEY UPDATE` is the lock a status write takes anyway. Writing a row that references the file,
such as the assignment `open_process` writes a moment before its move, takes `FOR KEY SHARE` on the file. That lock
conflicts with `FOR UPDATE` but not with `FOR NO KEY UPDATE`, so another act on the same file neither waits on a move
nor deadlocks with it. Two moves on one file are serialised; the second is judged on the first's result. `resume`
still computes its target from the caller's instance. `transition` then judges that target on the locked row, so a
stale target is refused, never written.

**6 — the platform's moves.** `system=True` only turns off the fallback: an explicit actor still wins, and every
other caller is unchanged. The timeline already draws an event with no actor without a name, so the orientation's
moves no longer read «Vous» and no word is added. The assessment, which the person did run, stays theirs. The change
touches `apps/audit/services.py`, a path outside this family's slice: one keyword, documented in the function.

**7 — the words, for the owner's copy packet B1 (no code changed).** The review's four join §6's:

- (a) a closed file's «Mes documents» empty state on the dashboard invites an upload and promises a list;
- (b) is §6's word 4;
- (c) a suspended file's own page names a next action while its dashboard panel names none. The notes kept next
  actions on a suspended file on purpose: the reason it waits is often one of them. The owner decides whether the
  panel names it too;
- (d) is §6's word 3.

**The review's other observations stand, unchanged, for the owner.**

- The policies' administrator branch ignores read-only. On a CLOSED file the transition view answers the administrator
  with the domain's refusal and the owner with 403, and the checklist policy lets an administrator change a closed
  file's lines. Neither is a state change.
- Q11 and Q12 are confirmed by the reviewer's reading.
- The lifecycle's tail is answered by finding 1 (Q5).

**Superseded above** (each place marked in the text): §2.1's «the administrator is on every declared row» and its
«nobody beside the administrator» rows (finding 1); §2.2's administrator row (finding 1); §2.3's «only on a file
holding an unrevoked AUTHORISED_ACTOR assignment» (finding 4); §2.4's «the latest event» (finding 3); Q1, Q5 and Q10
(above).

**Runs**, one at a time on lane 7 (`test_ile_v5_l7`) with `-p no:randomly`, all green except where the table says
otherwise:

| Run | Result |
|---|---|
| `apps/cases apps/selection apps/portal apps/notifications apps/audit apps/accounts apps/helpdesk apps/documents apps/academy tests/security tests/backoffice tests/test_phase_console.py tests/frontend/test_design_docs.py tests/frontend/test_dashboard_w3_b.py tests/frontend/test_journey_w3_d.py tests/frontend/test_documents_w3_c.py`, with `-m "not browser"`. This is the builder's list plus every app the fixes reach: the audit helper, the admin, the readers of case assignments | **1 357 passed, 3 skipped** (19 min 16 s; `.work/sec-f7/fix2/suite_targeted.log`) |
| Browser: `apps/portal/tests/test_browser.py`, `tests/frontend/test_dashboard_browser_w3_b.py`, `tests/frontend/test_journey_browser_w3_d.py` | **47 passed** |
| `apps/cases/tests/test_transition_actors.py` and `apps/selection/tests/test_selection_exits.py`, after the last edit | 86 passed |
| The merged tree: design-v5 `f447c28` (sec-f5 merged) plus this branch. `git merge-tree` gives tree `44d37e5`, extracted with `git archive` (no worktree, no commit; the worktree's `.env` copied in). Run: the F-7 module, the selection exits, the held file, sec-f5's `test_backoffice_second_factor.py`, `apps/audit` and `tests/security/test_log_privacy.py` | **206 passed**. The back-office tests also hold on sec-f5's `BackofficeAdminSite` |
| The reviewer's suite (89 tests, `C:/tmp/ile_v5_council/.work/sec-f7/review/`) on the fixed branch | 85 passed. 4 differ by design: the matrix's administrator and superuser rows and the strict probe now see exactly §4's moves plus `BEYOND_SECTION_4`'s two, while their expectation encodes the reading finding 1 removed. The stale-row probe's set-up asks the administrator for SUSPENDED → ENTERED, which is now nobody's move; its scenario is kept, with moves still allowed, in `TestTheRowAMoveIsJudgedOn`. The other nine probes pass |
| `ruff check .` · `manage.py makemigrations --check --dry-run` · `manage.py check` | clean · «No changes detected» · no issue |

A full non-browser run (`-m "not browser"` on every test path) was started and then stopped after about 360 tests,
with no failure. At this machine's pace, shared with three teams' suites, it would have taken over two hours. The
suites above cover every app the fixes reach. The steward's merge regression and CI remain the full runs.

The F-7 module now holds 82 tests (60 before); `apps/selection/tests/test_selection_exits.py` adds 4.

**Handed to:**

- **The steward (at merge).** The paths this lane touched: `apps/cases/{models,services,admin}.py`,
  `apps/cases/tests/test_transition_actors.py`, `apps/selection/tests/test_selection_exits.py` (new),
  `apps/audit/services.py` (new to the family: the `system` keyword), `docs/platform/CASE_LIFECYCLE.md` (the pointer
  line), these notes and `REVIEW.md`. `git merge-tree` against design-v5 `f447c28` (sec-f5 merged): clean. Against
  `v54-w3-e` `504f726`: clean.
- **W3-E (the case file).** The administrator's state control now lists suspend, close, the way back from a
  suspension, SELECTION → TRAINING and ENTERED → POST_ENTRY only. The case timeline names no actor on the
  orientation's moves («sistema»). No template changed.
- **The back-office hardening (sec-f5's area) or the owner.** The observation under 2.
- **The owner.** Q1 and Q5 as updated; `BEYOND_SECTION_4`'s two departures, to confirm (and §4 to gain them) or to
  remove; the words of 7 with §6's (copy packet B1).

## At the merge (the steward, 16 October 2026)

The steward's merge step (`sec-f7-merge`, under `C:/tmp/ile_locks/DESIGN_V5_MERGE_LOCK`, taken at 02:23:38) on lane 7:
`TEST_DATABASE_URL=…/test_ile_v5_l7`, one pytest at a time, `-p no:randomly`; no server started, no persona used.
Nothing deployed, nothing pushed, no production touched. Logs: `C:/tmp/ile_v5_council/evidence/v54/sec-f7/merge/`.

- **The sync** (`fcd4153`). design-v5 had moved from `fec37d3` to `8ab5b89`: 41 commits — the sec-f5 merge and its
  record DL54-130 (the back office's own sign-in signs no one in; a held second factor presented in every session), then
  integration checkpoint 3 (the intfix merge, its rebuild, DL54-131, the changelog line). `git merge --no-ff design-v5`:
  no conflict and no path in common (sec-f5: accounts, settings, documents; intfix: the overlay system's and the
  loader's scripts, the showcase's comment, their tests and the bundles; this branch: the cases domain, the selection
  and audit services, the dashboard's presenter). sec-f5's back office (`BackofficeAdminSite`) and this branch's
  `CaseFileAdmin` / `CaseAssignmentAdmin` meet here for the first time on a committed tree; their tests run together
  below.
- **The bundles.** Both dist trees deleted and rebuilt from clean (`npm run build`; `node_modules` a junction to
  design-v5's): `static/css/dist` byte for byte the committed tree; `static/js/dist` identical once esbuild's chunk
  names are read as one (they follow the worktree: the Motion library is resolved through the junction). design-v5's
  committed tree kept (`git checkout`), so this branch carries design-v5's bundles byte for byte and the merge brings
  none. The family changes no stylesheet and no script: `main.css` 35 483 → 35 483 B (gzip −9) on every page, the
  console page types 44 196 → 44 196 B (V5.8's shared payload unchanged).
- **DS 2026 §11.7** (`25aac85`, the hand-over of §9): «Il NowPanel — sei varianti», the two held variants in the
  catalogue's words, no next action and no takeover on a held file, the reason drawn once. `regen_design_inventory.py`:
  the inventory tables and the counts are current.
- **Ownership** (`a999215`). The family «sec-f7» is registered in `docs/design-v5/OWNERSHIP_V54.json` outside the waves
  (wave 0, as devops, sec-f5 and intfix; no merge tag): 14 entries, 4 whole (the three new test modules and these
  reports) and 10 slices, each with its reason; `tests/test_check_ownership.py` names it among the families outside the
  waves (the checker has accepted `sec-f<n>` since the sec-f5 merge). `check_ownership.py sec-f7 design-v5` before that
  commit: **15 paths, 5 inside, 10 slice → PASS**, each slice read in the diff; after it the steward's two paths join
  (the manifest, steward-only; the checker's test, the steward family's), as at the sec-f5 merge. `--validate`: **29
  families, 698 entries**.
- **Tests on the merged branch** (`a999215`): **1 106 passed, 3 skipped** in 17 min 19 s (`-m "not browser"`) — the
  merge brief's list: `apps/cases` (183, F-7's 82 among them), `apps/portal` (215, the held file's 13 among them),
  `tests/security` (157, the confidential-material guard among them), `tests/test_phase_console.py` (8),
  `apps/notifications` (95), `tests/deployment` (54), `tests/frontend/test_design_docs.py` (40), both bundle-currency
  tests (8); with `apps/selection` (86, the selection exits' 4 among them) and `apps/audit` (8), which the fix reaches,
  `tests/backoffice` (5) and sec-f5's `test_backoffice_second_factor.py` (90: its admin site beside this branch's admin
  screens), the checker's test (57), `tests/test_migration_drift.py` (2), and W3-B's and W3-D's static tests of the
  dashboard and the journey (60 + 41). The three skips are `apps/cases/tests/test_intake.py`'s cases that need a legal
  rule in force (none is). In Chromium, `apps/portal/tests/test_browser.py` and
  `tests/frontend/test_dashboard_browser_w3_b.py` (the dashboard's template and presenter changed): **35 passed** in
  1 min 37 s. `manage.py check`: no issue; `makemigrations --check --dry-run`: no changes; `ruff check .`: clean (`ruff
  format --check` on the family's eleven Python files: ten formatted, and one test signature of `test_views.py`
  unformatted since before the fix).
- **Scan.** The family's 2 747 added lines: loopback only (the documented local test database), `example.test` addresses
  only, no URL, no credential, no production host or droplet name, no live domain.

The merge itself, the table as enforced, the review and the owner's questions are recorded in
`docs/design-v5/DECISION_LOG_V54.md` (DL54-132). main (the V4 line) is the merge brief's next step, after the lock: a
`cherry-pick -x` of Part A's eleven commits, kept only if it applies cleanly and main's `apps/cases` and
`tests/security` pass (`evidence/v54/sec-f7/merge/main_cherry_pick.log`).
