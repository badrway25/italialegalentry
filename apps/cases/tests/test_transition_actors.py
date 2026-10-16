"""
WHO may move a case file — the «Chi può» column of docs/platform/CASE_LIFECYCLE.md §4 (finding F-7, sec-f7).

§4's rule 2: «Una transizione non dichiarata in questa tabella è rifiutata dal dominio, non solo nascosta
nell'interfaccia». The table declares WHO as well as WHAT, and until F-7 the domain read only the WHAT: a person whose
file was active held «change» on it (``cases.policies``) and could therefore make every declared move — announce their
own administrative procedure, their own entry into Italy, open the selection phase (a reserved activity, CR-03) — which
the journey «La soglia» then drew as a fact.

These tests reproduce that, then hold the fix: the column is data (``cases.models.TRANSITION_ACTORS``), enforced inside
``cases.services.transition`` whenever an actor is given, and the case page's controls are computed from the same
table — so the interface never offers a move the domain refuses, for any role in any state. The effective right is the
object policy AND the column: nobody gains a move; the training body and the authorised actor, whom the column names
and the policy refuses «change», get nothing on the case's own path (the authorised actor keeps the selection
service's). The administrator makes the moves §4 names it for — suspend, close, lift a suspension as «superiore» —
and the two ``BEYOND_SECTION_4`` declares with their reason, never a reserved activity's (sec-f7 REVIEW, finding 1).
"""

from __future__ import annotations

import datetime as dt
from html.parser import HTMLParser
from pathlib import Path

import pytest
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.utils import translation

from accounts import roles
from audit.models import AuditEvent
from audit.services import record
from cases import services
from cases.models import (
    ACTIVE_STATUSES,
    ALLOWED_TRANSITIONS,
    BEYOND_SECTION_4,
    TRANSITION_ACTORS,
    AssessmentOutcome,
    AssignmentRole,
    CaseFile,
    CasePurpose,
    CaseStatus,
    TransitionActor,
    transition_actors,
    transitions_from,
)
from core import clock

pytestmark = pytest.mark.django_db

ROOT = Path(__file__).resolve().parents[3]
LIFECYCLE = ROOT / "docs" / "platform" / "CASE_LIFECYCLE.md"
INDEX = "/fr/espace-reserve/dossiers/"
S = CaseStatus
WHO = TransitionActor


def _transition_url(case) -> str:
    return f"{INDEX}{case.reference}/etat/"


def _put(case, status, *, previous=""):
    """Test set-up only: place the file in ``status`` without walking the graph (W3-D's ``_status`` does the same)."""
    CaseFile.objects.filter(pk=case.pk).update(
        status=status,
        status_since=clock.now(),
        previous_status=previous,
        suspension_reason="Motif de test" if status == S.SUSPENDED else "",
    )
    case.refresh_from_db()
    return case


def _suspended_by(case, user, *, previous=S.ORIENTED):
    """A file suspended by ``user`` (None: by the platform), as the trail records a suspension."""
    _put(case, S.SUSPENDED, previous=previous)
    record(
        actor=user,
        action="case.transition",
        target=case,
        metadata={"from": str(previous), "to": str(S.SUSPENDED), "reason": "Motif de test"},
    )
    return case


def _moves_to(case, target) -> bool:
    return AuditEvent.objects.filter(
        action="case.transition", target_id=str(case.pk), metadata__to=str(target)
    ).exists()


def _accepts(case, target, user) -> bool:
    """Whether ``services.transition`` makes the move for ``user`` — tried inside a savepoint, then undone."""
    point = transaction.savepoint()
    try:
        services.transition(case, target, actor=user, reason="Motif de test")
    except ValidationError:
        return False
    else:
        return True
    finally:
        transaction.savepoint_rollback(point)
        case.refresh_from_db()


def _offered(case, user) -> set[str]:
    return {str(target) for target, _label in services.transitions_available(case, user)}


def _moves_on_the_page(body: str) -> set[str]:
    """
    The moves the case page offers: the choices of the file's state dialog (design V5, W3-E —
    templates/cases/partials/state_dialog.html: radios named ``status`` in ``#file-state-form``), where the V4 page
    drew a select's options. Read in that form only: a checklist line's dialog names its radios ``status`` too.
    """
    if 'id="file-state-form"' not in body:
        return set()
    form = body.split('id="file-state-form"', 1)[1].split("</form>", 1)[0]
    return {value for value in CaseStatus.values if f'name="status" value="{value}"' in form}


@pytest.fixture
def owner(django_user_model):
    # no ``roles.ensure_roles()``: ``assign_role`` creates the group it needs, and the policies read no model permission
    user = django_user_model.objects.create_user(email="f7.owner@example.test", password="x")
    roles.assign_role(user, roles.PERSON)
    return user


@pytest.fixture
def case(owner):
    return services.open_case(owner, purpose=CasePurpose.WORK, pathway_key="salaried_work")


@pytest.fixture
def authorised(django_user_model, case):
    """An authorised actor, assigned with a reference and a validity: CR-03 is satisfied on this file."""
    user = django_user_model.objects.create_user(email="f7.authorised@example.test", password="x")
    roles.assign_role(user, roles.AUTHORISED_ACTOR)
    services.assign(
        case,
        user,
        role=AssignmentRole.AUTHORISED_ACTOR,
        authorisation_reference="SYNTH-AUT-F7",
        authorisation_valid_until=clock.today() + dt.timedelta(days=90),
    )
    return user


@pytest.fixture
def cast(django_user_model, case, owner, authorised):
    """Every capacity the column names, on one file — each assignee live, the authorised actor's mandate valid."""

    def make(email, role=None, **extra):
        user = django_user_model.objects.create_user(email=email, password="x", **extra)
        if role:
            roles.assign_role(user, role)
        return user

    people = {"owner": owner, "authorised": authorised}
    for key, role, assignment in (
        ("operator", roles.OPERATOR, AssignmentRole.OPERATOR),
        ("professional", roles.PROFESSIONAL, AssignmentRole.PROFESSIONAL),
        ("training_body", roles.TRAINING_PROVIDER, AssignmentRole.TRAINING_BODY),
    ):
        people[key] = make(f"f7.{key}@example.test", role)
        services.assign(case, people[key], role=assignment)
    people["administrator"] = make("f7.administrator@example.test", roles.ADMINISTRATOR, is_staff=True)
    people["superuser"] = django_user_model.objects.create_superuser(email="f7.super@example.test", password="x")
    people["stranger"] = make("f7.stranger@example.test", roles.PERSON)
    return people


# ---------------------------------------------------------------------------------------------
# F-7, reproduced: the person's own file, moved by the person
# ---------------------------------------------------------------------------------------------
class TestTheFindingReproduced:
    def test_a_person_cannot_announce_their_own_administrative_procedure(self, client, owner, case):
        _put(case, S.ORIENTED)
        client.force_login(owner)
        response = client.post(_transition_url(case), {"status": S.ADMIN_PROCESS}, follow=True)
        case.refresh_from_db()
        assert case.status == S.ORIENTED
        assert not _moves_to(case, S.ADMIN_PROCESS)
        # refused in the domain's own words, already translated — no new sentence
        notes = [str(message) for message in response.context["messages"]]
        assert notes == [
            "Transition non autorisée de « Orientation terminée » à « Procédure administrative en cours »."
        ]

    def test_a_person_cannot_move_their_file_on_to_the_departure(self, client, owner, case):
        _put(case, S.ADMIN_PROCESS)
        client.force_login(owner)
        client.post(_transition_url(case), {"status": S.PRE_DEPARTURE})
        case.refresh_from_db()
        assert case.status == S.ADMIN_PROCESS

    def test_a_person_cannot_record_their_own_entry_into_italy(self, client, owner, case):
        _put(case, S.PRE_DEPARTURE)
        client.force_login(owner)
        client.post(_transition_url(case), {"status": S.ENTERED})
        case.refresh_from_db()
        assert case.status == S.PRE_DEPARTURE
        assert not _moves_to(case, S.ENTERED)

    def test_a_person_cannot_open_the_selection_phase_even_with_an_authorised_actor_assigned(
        self, client, owner, case, authorised
    ):
        """CR-03's own check passes here — a valid authorised actor IS assigned —, so only WHO can refuse it."""
        _put(case, S.TRAINING)
        assert case.has_valid_authorised_actor()
        client.force_login(owner)
        client.post(_transition_url(case), {"status": S.SELECTION})
        case.refresh_from_db()
        assert case.status == S.TRAINING
        assert not _moves_to(case, S.SELECTION)

    @pytest.mark.parametrize(
        ("status", "target"),
        [
            (S.ORIENTED, S.ADMIN_PROCESS),
            (S.ORIENTED, S.TRAINING),
            (S.ADMIN_PROCESS, S.PRE_DEPARTURE),
            (S.PRE_DEPARTURE, S.ENTERED),
            (S.TRAINING, S.SELECTION),
        ],
    )
    def test_the_person_is_never_offered_those_moves(self, owner, case, authorised, status, target):
        _put(case, status)
        assert target not in dict(services.transitions_available(case, owner))

    @pytest.mark.parametrize(
        ("status", "target"),
        [
            (S.ORIENTED, S.ADMIN_PROCESS),
            (S.PRE_DEPARTURE, S.ENTERED),
            (S.TRAINING, S.SELECTION),
        ],
    )
    def test_the_domain_refuses_them_whatever_the_entry_point(self, owner, case, authorised, status, target):
        _put(case, status)
        with pytest.raises(services.TransitionNotPermitted):
            services.transition(case, target, actor=owner)
        case.refresh_from_db()
        assert case.status == status


# ---------------------------------------------------------------------------------------------
# The column as data, and the data as §4 states it
# ---------------------------------------------------------------------------------------------
_NAMES = {
    "persona": WHO.PERSON,
    "operatore": WHO.OPERATOR,
    "professionista": WHO.PROFESSIONAL,
    "ente formativo": WHO.TRAINING_BODY,
    "soggetto autorizzato": WHO.AUTHORISED_ACTOR,
    "amministratore": WHO.ADMINISTRATOR,
    "sistema": WHO.SYSTEM,
}


def _section_4_rows() -> list[tuple[str, str, frozenset[str] | str]]:
    """(Da, A, Chi può) of every row of §4's table, read from the approved document itself."""
    text = LIFECYCLE.read_bytes().decode("utf-8")
    section = text.split("## 4. Tabella delle transizioni", 1)[1].split("**Regole invalicabili:**", 1)[0]
    rows = []
    for line in section.splitlines():
        cells = [cell.strip().strip("*").strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 5 or cells[0] == "Da" or set(cells[0]) <= {"-"}:
            continue
        who = cells[2]
        names = who if who.startswith("chi ") else frozenset(_NAMES[name.strip()] for name in who.split(","))
        rows.append((cells[0], cells[1], names))
    return rows


#: «chi ha sospeso, o superiore»: the superior is the administrator (sec-f7 NOTES, Q4); who suspended is the trail's.
_SUPERIOR = frozenset({WHO.ADMINISTRATOR})


def _section_4_says(status: str, target: str, previous: str = "") -> frozenset[str]:
    """Every capacity a row of §4 matching the move names — a move is open to all of them («qualunque attivo →
    SUSPENDED» and «DRAFT → SUSPENDED» both match DRAFT → SUSPENDED). ``previous``: the state a SUSPENDED file left."""
    names: set[str] = set()
    for source, to, who in _section_4_rows():
        if source == "—":  # the creation (open_case), not a transition
            continue
        if to == "stato precedente":
            assert source == "SUSPENDED" and who == "chi ha sospeso, o superiore"
            if status == S.SUSPENDED and previous and target == previous:
                names |= _SUPERIOR
            continue
        if S[to] != target:
            continue
        if source == "qualunque attivo":
            matches = status in ACTIVE_STATUSES
        elif source == "qualunque":
            matches = target in transitions_from(status)
        else:
            matches = S[source] == status
        if matches:
            names |= who
    return frozenset(names)


def test_the_column_names_every_declared_transition_and_nothing_else():
    declared = {(source, target) for source, targets in ALLOWED_TRANSITIONS.items() for target in targets}
    assert set(TRANSITION_ACTORS) == declared


def test_an_assignee_acts_in_the_capacity_of_its_assignment_role():
    assignees = {WHO.PROFESSIONAL, WHO.AUTHORISED_ACTOR, WHO.TRAINING_BODY, WHO.OPERATOR}
    assert assignees == set(AssignmentRole.values)


def test_the_data_says_what_section_4_says():
    """§4's table, read from the approved document, against the data — the administrator included (sec-f7 REVIEW,
    finding 1: it used to be added to every row, which this test could not see). Every declared move, from every
    state — and out of SUSPENDED towards each state it may have left — carries exactly the capacities §4's matching
    rows name, plus what ``BEYOND_SECTION_4`` declares with its reason. A row the graph has and §4 does not is nobody's
    (rule 2) unless declared there."""
    assert len(_section_4_rows()) == 17, "§4's table changed: change TRANSITION_ACTORS with it"
    beyond = {row: names for row, (names, _why) in BEYOND_SECTION_4.items()}
    for status in CaseStatus.values:
        for previous in sorted(ACTIVE_STATUSES) if status == S.SUSPENDED else [""]:
            for target in transitions_from(status):
                expected = _section_4_says(status, target, previous) | beyond.get((status, target), frozenset())
                assert transition_actors(status, target, previous=previous) == expected, (status, target, previous)


def test_every_departure_from_section_4_is_declared_with_its_reason():
    for (status, target), (names, why) in BEYOND_SECTION_4.items():
        assert target in transitions_from(status), (status, target)
        assert names and not names & _section_4_says(status, target), "§4 already names them: not a departure"
        assert len(why) >= 60, (status, target)
    # never a reserved activity's row, nor a claim of an orientation or of a review nobody ran
    for row in ((S.TRAINING, S.SELECTION), (S.SELECTION, S.ADMIN_PROCESS), (S.DRAFT, S.ORIENTED)):
        assert row not in BEYOND_SECTION_4, row
    assert set(BEYOND_SECTION_4) == {(S.SELECTION, S.TRAINING), (S.ENTERED, S.POST_ENTRY)}


def test_nobody_is_on_an_undeclared_move_and_out_of_suspended_only_the_way_back_is_open():
    for status in CaseStatus.values:
        for target in CaseStatus.values:
            if target not in transitions_from(status):
                assert transition_actors(status, target) == frozenset(), (status, target)
    for previous in ACTIVE_STATUSES:
        for target in ACTIVE_STATUSES:
            names = transition_actors(S.SUSPENDED, target, previous=previous)
            assert names == (_SUPERIOR if target == previous else frozenset()), (previous, target)
        assert transition_actors(S.SUSPENDED, previous) == frozenset(), "the state it left unknown: nobody"


def test_the_administrator_makes_only_the_moves_section_4_names_for_it():
    """sec-f7 REVIEW, finding 1 (the reviewer's probe, kept): §4 names the administrator on «qualunque attivo →
    SUSPENDED», «qualunque → CLOSED» and, as «superiore», the way back from a suspension — and on nothing else; the
    data adds exactly ``BEYOND_SECTION_4``'s two moves, neither of them a reserved activity's."""
    extra = {(S.SELECTION, S.TRAINING), (S.ENTERED, S.POST_ENTRY)}
    for status in ACTIVE_STATUSES:
        moves = {
            target for target in transitions_from(status) if WHO.ADMINISTRATOR in transition_actors(status, target)
        }
        assert moves == {S.SUSPENDED, S.CLOSED} | {target for source, target in extra if source == status}, status
    for previous in ACTIVE_STATUSES:
        moves = {
            target
            for target in transitions_from(S.SUSPENDED)
            if WHO.ADMINISTRATOR in transition_actors(S.SUSPENDED, target, previous=previous)
        }
        assert moves == {previous, S.CLOSED}, previous


# ---------------------------------------------------------------------------------------------
# Every role in every state: what the page offers is exactly what the domain accepts
# ---------------------------------------------------------------------------------------------
#: The column as the domain applies it on this file (an authorised actor assigned, so CR-03 never blocks SELECTION),
#: per role, per state; a role or a state absent here: nothing. The administrator and the superuser make the moves §4
#: names them for, and ``BEYOND_SECTION_4``'s two — never SELECTION, whoever is assigned (sec-f7 REVIEW, finding 1).
_ACTIVE_EXITS = {S.SUSPENDED, S.CLOSED}
_ADMINISTRATOR_MOVES = {
    **{status: {S.SUSPENDED, S.CLOSED} for status in ACTIVE_STATUSES},
    S.SELECTION: {S.TRAINING, S.SUSPENDED, S.CLOSED},
    S.ENTERED: {S.POST_ENTRY, S.SUSPENDED, S.CLOSED},
    "suspended:owner": {S.ORIENTED, S.CLOSED},
    "suspended:operator": {S.ORIENTED, S.CLOSED},
    "suspended:platform": {S.ORIENTED, S.CLOSED},
    S.CLOSED: set(),
}
EXPECTED: dict[str, dict[str, set[str]]] = {
    "administrator": _ADMINISTRATOR_MOVES,
    "superuser": _ADMINISTRATOR_MOVES,
    "owner": {
        **{status: {S.SUSPENDED, S.CLOSED} for status in ACTIVE_STATUSES},
        "suspended:owner": {S.ORIENTED, S.CLOSED},
        "suspended:operator": {S.CLOSED},
        "suspended:platform": {S.CLOSED},
        S.CLOSED: set(),
    },
    "operator": {
        **{status: {S.SUSPENDED} for status in ACTIVE_STATUSES},
        S.ORIENTED: {S.REVIEW_REQUIRED, S.TRAINING, S.ADMIN_PROCESS, S.SUSPENDED},
        S.ADMIN_PROCESS: {S.PRE_DEPARTURE, S.SUSPENDED},
        S.PRE_DEPARTURE: {S.ENTERED, S.SUSPENDED},
        S.POST_ENTRY: {S.SUSPENDED, S.CLOSED},
        "suspended:owner": set(),
        "suspended:operator": {S.ORIENTED},
        "suspended:platform": set(),
        S.CLOSED: set(),
    },
    "professional": {S.REVIEW_REQUIRED: {S.ORIENTED, S.TRAINING}},
}
_SETUPS = [status for status in CaseStatus.values if status != S.SUSPENDED] + [
    "suspended:owner",
    "suspended:operator",
    "suspended:platform",
]


def _expected(role: str, setup: str) -> set[str]:
    return {str(target) for target in EXPECTED.get(role, {}).get(setup, set())}


def _set_up(case, cast, setup):
    if setup.startswith("suspended:"):
        by = setup.split(":", 1)[1]
        return _suspended_by(case, None if by == "platform" else cast[by])
    return _put(case, setup)


@pytest.mark.parametrize("setup", _SETUPS)
def test_every_role_is_offered_exactly_what_the_domain_accepts(case, cast, setup):
    """The table-driven test: for each account the column can name, in each state (a suspension made by the person, by
    the operator or by the platform), the case page's controls equal the moves ``transition`` accepts — and both equal
    the column as §4 states it."""
    _set_up(case, cast, setup)
    status = str(case.status)
    for role, user in cast.items():
        offered = _offered(case, user)
        accepted = {target for target in CaseStatus.values if target != status and _accepts(case, target, user)}
        assert offered == accepted, (role, setup)
        assert offered == _expected(role, setup), (role, setup)


@pytest.mark.parametrize(
    ("role", "status"),
    [
        ("owner", S.ORIENTED),
        ("owner", S.PRE_DEPARTURE),
        ("owner", "suspended:owner"),
        ("operator", S.ORIENTED),
        ("operator", S.POST_ENTRY),
        ("professional", S.REVIEW_REQUIRED),
        ("authorised", S.TRAINING),
        ("training_body", S.ORIENTED),
        ("administrator", S.TRAINING),
        ("administrator", S.SELECTION),
        ("administrator", "suspended:owner"),
        ("superuser", S.DRAFT),
    ],
)
def test_the_case_page_offers_exactly_what_its_view_accepts(client, case, cast, role, status):
    """Through the interface itself: the page's options, then a POST of every state to the transition view."""
    _set_up(case, cast, status)
    before = str(case.status)
    user = cast[role]
    client.force_login(user)
    body = client.get(f"{INDEX}{case.reference}/").content.decode("utf-8")
    shown = _moves_on_the_page(body)
    accepted = set()
    for target in CaseStatus.values:
        if target == before:
            continue
        response = client.post(_transition_url(case), {"status": target, "reason": "Motif de test"})
        case.refresh_from_db()
        if case.status != before:
            accepted.add(target)
            _set_up(case, cast, status)
        else:
            assert response.status_code in (302, 403), (role, target)
    assert shown == accepted == _expected(role, status), role


# ---------------------------------------------------------------------------------------------
# What §4 gives each one, kept
# ---------------------------------------------------------------------------------------------
class TestThePerson:
    def test_suspends_their_file_with_a_reason_and_only_with_one(self, owner, case):
        _put(case, S.ADMIN_PROCESS)
        with pytest.raises(services.TransitionRefused):
            services.transition(case, S.SUSPENDED, actor=owner, reason="  ")
        services.transition(case, S.SUSPENDED, actor=owner, reason="Je pars en mission deux mois")
        case.refresh_from_db()
        assert case.status == S.SUSPENDED and case.suspension_reason == "Je pars en mission deux mois"

    def test_lifts_a_suspension_they_made_back_to_where_the_file_was(self, owner, case):
        _put(case, S.ADMIN_PROCESS)
        services.transition(case, S.SUSPENDED, actor=owner, reason="Pause")
        assert services.suspended_by(case) == owner.pk
        services.resume(case, actor=owner)
        case.refresh_from_db()
        assert case.status == S.ADMIN_PROCESS and case.suspension_reason == ""

    def test_does_not_lift_a_suspension_somebody_else_made(self, owner, case, cast):
        _put(case, S.ADMIN_PROCESS)
        services.transition(case, S.SUSPENDED, actor=cast["operator"], reason="Pièce d’identité à vérifier")
        with pytest.raises(services.TransitionNotPermitted):
            services.resume(case, actor=owner)
        assert dict(services.transitions_available(case, owner)) == {S.CLOSED: "Parcours clôturé"}

    def test_does_not_lift_a_suspension_the_trail_does_not_attribute_to_them(self, owner, case, cast):
        """sec-f7 REVIEW, finding 3 (the reviewer's probe, kept): «chi ha sospeso» is read from THIS suspension's
        event — written since the file entered SUSPENDED, from the state it left — never from an older one. A file
        set SUSPENDED by a path that wrote no event (a restore, a data fix) is the administrator's to lift."""
        _put(case, S.ORIENTED)
        services.transition(case, S.SUSPENDED, actor=owner, reason="Pause")
        services.resume(case, actor=owner)
        _put(case, S.SUSPENDED, previous=S.PRE_DEPARTURE)  # no event of its own: a restored row
        assert services.suspended_by(case) is None
        assert not _accepts(case, S.PRE_DEPARTURE, owner)
        assert _accepts(case, S.PRE_DEPARTURE, cast["administrator"])
        # an event of this moment that names another departure state is not this suspension's either
        record(actor=owner, action="case.transition", target=case, metadata={"from": S.ORIENTED, "to": S.SUSPENDED})
        assert services.suspended_by(case) is None
        assert not _accepts(case, S.PRE_DEPARTURE, owner)

    def test_closes_their_file_from_any_state_on_request(self, owner, case):
        for status in (*ACTIVE_STATUSES, S.SUSPENDED):
            _put(case, status, previous=S.ORIENTED if status == S.SUSPENDED else "")
            assert _accepts(case, S.CLOSED, owner), status

    def test_never_moves_their_file_along_the_pathway(self, owner, case, authorised):
        for status in ACTIVE_STATUSES:
            _put(case, status)
            onward = transitions_from(status) - _ACTIVE_EXITS
            assert not any(_accepts(case, target, owner) for target in onward), status


class TestTheOperatorAndTheProfessional:
    def test_the_operator_makes_the_operators_moves(self, case, cast):
        operator = cast["operator"]
        for status, target in (
            (S.ORIENTED, S.REVIEW_REQUIRED),
            (S.ORIENTED, S.TRAINING),
            (S.ORIENTED, S.ADMIN_PROCESS),
            (S.ADMIN_PROCESS, S.PRE_DEPARTURE),
            (S.PRE_DEPARTURE, S.ENTERED),
            (S.POST_ENTRY, S.CLOSED),
        ):
            _put(case, status)
            assert _accepts(case, target, operator), (status, target)

    def test_the_operator_does_not_make_the_authorised_actors_or_the_platforms_moves(self, case, cast):
        operator = cast["operator"]
        for status, target in ((S.TRAINING, S.SELECTION), (S.ENTERED, S.POST_ENTRY), (S.ORIENTED, S.CLOSED)):
            _put(case, status)
            assert not _accepts(case, target, operator), (status, target)

    def test_the_operator_lifts_its_own_suspension_and_not_the_persons(self, case, cast, owner):
        operator = cast["operator"]
        _suspended_by(case, operator, previous=S.PRE_DEPARTURE)
        assert _accepts(case, S.PRE_DEPARTURE, operator)
        _suspended_by(case, owner, previous=S.PRE_DEPARTURE)
        assert not _accepts(case, S.PRE_DEPARTURE, operator)

    def test_the_professional_concludes_a_review_and_does_nothing_else(self, case, cast):
        professional = cast["professional"]
        _put(case, S.REVIEW_REQUIRED)
        assert _accepts(case, S.ORIENTED, professional) and _accepts(case, S.TRAINING, professional)
        assert not _accepts(case, S.SUSPENDED, professional) and not _accepts(case, S.CLOSED, professional)


class TestTheAdministratorAndThePlatform:
    def test_the_administrator_suspends_closes_lifts_any_suspension_and_moves_along_only_where_declared(
        self, case, cast
    ):
        administrator = cast["administrator"]
        for status in ACTIVE_STATUSES:
            _put(case, status)
            assert _accepts(case, S.SUSPENDED, administrator) and _accepts(case, S.CLOSED, administrator), status
            onward = transitions_from(status) - _ACTIVE_EXITS
            accepted = {target for target in onward if _accepts(case, target, administrator)}
            assert accepted == set(_ADMINISTRATOR_MOVES[status]) - _ACTIVE_EXITS, status
        _suspended_by(case, cast["owner"])
        assert _accepts(case, S.ORIENTED, administrator)
        assert not any(_accepts(case, target, administrator) for target in ACTIVE_STATUSES - {S.ORIENTED})

    def test_the_administrator_neither_opens_nor_concludes_a_selection_from_the_case_page(self, client, case, cast):
        """sec-f7 REVIEW, finding 1 (the reviewer's probe, kept): with an authorised actor merely ASSIGNED, the
        administrator used to move the file into SELECTION and on to ADMIN_PROCESS («esito positivo della selezione»)
        with no mandate, no selection process and no act of the authorised actor — CR-03's reserved activity, drawn
        by the journey as a fact. Neither is offered, and the view refuses both in the domain's words."""
        from selection.models import SelectionProcess

        assert case.has_valid_authorised_actor()
        client.force_login(cast["administrator"])
        for status, target in ((S.TRAINING, S.SELECTION), (S.SELECTION, S.ADMIN_PROCESS)):
            _put(case, status)
            page = client.get(f"{INDEX}{case.reference}/").content.decode("utf-8")
            moves = _moves_on_the_page(page)
            assert S.CLOSED in moves and target not in moves, (status, target, moves)
            response = client.post(_transition_url(case), {"status": target}, follow=True)
            case.refresh_from_db()
            assert case.status == status and not _moves_to(case, target), (status, target)
            with translation.override("fr"):
                refusal = f"Transition non autorisée de « {S(status).label} » à « {S(target).label} »."
            assert [str(message) for message in response.context["messages"]] == [refusal]
        assert not SelectionProcess.objects.filter(case=case).exists()

    def test_the_administrator_claims_no_orientation_and_no_professional_review(self, case, cast):
        for user in (cast["administrator"], cast["superuser"]):
            _put(case, S.DRAFT)
            assert not _accepts(case, S.ORIENTED, user), "an orientation nobody ran"
            _put(case, S.REVIEW_REQUIRED)
            assert not _accepts(case, S.ORIENTED, user) and not _accepts(case, S.TRAINING, user), "a review nobody made"

    def test_a_platform_move_made_inside_a_persons_request_is_recorded_as_nobodys(self, owner, case, rf):
        """sec-f7 REVIEW, finding 6 (the reviewer's probe, kept): ``audit.services.record`` falls back to the request's
        user when no actor is given, so the orientation service's moves (§4: «sistema»), made inside the person's
        request, were recorded with the PERSON as their actor and the timeline said «Vous». The platform's path now
        records no actor — the request's trace kept — and the timeline names nobody; the assessment, which the person
        did run, stays theirs."""
        from cases import presenters

        request = rf.post("/fr/orientation/")
        request.user, request.request_id = owner, "f7-platform-move"
        services.record_assessment(
            case,
            outcome=AssessmentOutcome.REVIEW_REQUIRED,
            ruleset_version=1,
            ruleset_snapshot={"format": "test", "rules": []},
            answers={},
            request=request,
        )
        moves = AuditEvent.objects.filter(action="case.transition", target_id=str(case.pk)).order_by("created_at", "id")
        assert [(move.metadata["from"], move.metadata["to"]) for move in moves] == [
            (S.DRAFT, S.ORIENTED),
            (S.ORIENTED, S.REVIEW_REQUIRED),
        ]
        for move in moves:
            assert (move.actor_id, move.actor_label, move.request_id) == (None, "system", "f7-platform-move")
            assert move.ip_hash, "the request's trace is kept"
        assert AuditEvent.objects.get(action="case.assessment", target_id=str(case.pk)).actor_id == owner.pk
        drawn = [row["actor"] for row in presenters.timeline(case) if row["chip_label"]]
        assert drawn == ["", ""]

    def test_an_act_somebody_makes_inside_a_request_is_still_theirs(self, owner, case, rf):
        """The fallback itself is unchanged for every other act: no actor given, the request's user is the actor."""
        request = rf.post("/fr/espace-reserve/")
        request.user = owner
        assert record(request, action="case.viewed", target=case).actor_id == owner.pk
        assert record(request, action="case.viewed", target=case, actor=owner, system=True).actor_id == owner.pk

    def test_the_administrator_still_ends_a_selection_without_an_outcome_and_starts_the_accompaniment(self, case, cast):
        """``BEYOND_SECTION_4``'s two moves: the way out of a selection that can no longer be concluded (it asserts
        no outcome), and ENTERED → POST_ENTRY, whose performer «sistema — automatica» does not exist (Q5)."""
        administrator = cast["administrator"]
        _put(case, S.SELECTION)
        assert _accepts(case, S.TRAINING, administrator)
        _put(case, S.ENTERED)
        assert _accepts(case, S.POST_ENTRY, administrator)

    def test_a_suspension_nobody_can_attribute_is_lifted_by_the_administrator_alone(self, case, cast):
        _suspended_by(case, None)
        assert services.suspended_by(case) is None
        assert [role for role, user in cast.items() if _accepts(case, S.ORIENTED, user)] == [
            "administrator",
            "superuser",
        ]

    def test_the_platforms_own_path_is_unchanged(self, owner, case):
        """actor=None: the orientation service moves DRAFT → ORIENTED → REVIEW_REQUIRED, and ENTERED → POST_ENTRY
        stays open to the platform (§4: «sistema — automatica»)."""
        services.record_assessment(
            case,
            outcome=AssessmentOutcome.REVIEW_REQUIRED,
            ruleset_version=1,
            ruleset_snapshot={"format": "test", "rules": []},
            answers={},
        )
        case.refresh_from_db()
        assert case.status == S.REVIEW_REQUIRED
        _put(case, S.ENTERED)
        services.transition(case, S.POST_ENTRY)
        case.refresh_from_db()
        assert case.status == S.POST_ENTRY


class TestTheCapacitiesThePolicyRefuses:
    def test_the_training_body_gets_nothing_though_the_column_names_it(self, case, cast):
        """ORIENTED → TRAINING: «operatore, ente formativo» — but the object policy gives a training body no «change»
        on the file, and this fix widens nobody's access (sec-f7 NOTES: a question for the owner)."""
        _put(case, S.ORIENTED)
        assert WHO.TRAINING_BODY in transition_actors(S.ORIENTED, S.TRAINING)
        assert not _accepts(case, S.TRAINING, cast["training_body"])
        assert services.transitions_available(case, cast["training_body"]) == []

    def test_the_authorised_actor_does_not_move_the_file_through_the_case(self, client, case, cast):
        _put(case, S.TRAINING)
        authorised = cast["authorised"]
        assert not _accepts(case, S.SELECTION, authorised)
        client.force_login(authorised)
        assert client.post(_transition_url(case), {"status": S.SELECTION}).status_code == 403

    def test_the_selection_services_path_makes_the_authorised_actors_moves_and_no_other(self, case, cast):
        authorised = cast["authorised"]
        _put(case, S.TRAINING)
        with pytest.raises(services.TransitionNotPermitted):
            services.transition(case, S.ADMIN_PROCESS, actor=authorised, as_authorised_actor=True)
        services.transition(case, S.SELECTION, actor=authorised, as_authorised_actor=True)
        for target in (S.ADMIN_PROCESS, S.TRAINING):
            _put(case, S.SELECTION)
            services.transition(case, target, actor=authorised, as_authorised_actor=True)
            case.refresh_from_db()
            assert case.status == target
        _put(case, S.SELECTION)
        with pytest.raises(services.TransitionNotPermitted):
            services.transition(case, S.SUSPENDED, actor=authorised, reason="x", as_authorised_actor=True)

    def test_the_selection_services_path_is_closed_to_anybody_else_and_without_a_mandate(self, case, cast):
        _put(case, S.TRAINING)
        for role in ("owner", "operator", "professional", "training_body", "stranger"):
            with pytest.raises(services.TransitionNotPermitted):
                services.transition(case, S.SELECTION, actor=cast[role], as_authorised_actor=True)
        with pytest.raises(services.TransitionNotPermitted):
            services.transition(case, S.SELECTION, actor=None, as_authorised_actor=True)
        for assignment in case.assignments.filter(role=AssignmentRole.AUTHORISED_ACTOR):
            services.revoke_assignment(assignment)
        with pytest.raises(services.TransitionNotPermitted):
            services.transition(case, S.SELECTION, actor=cast["authorised"], as_authorised_actor=True)


# ---------------------------------------------------------------------------------------------
# Every other way a status could change
# ---------------------------------------------------------------------------------------------
BACKOFFICE = "/backoffice/cases/"


class _AdminForm(HTMLParser):
    """An admin change form's fields as a browser submits them: inputs, checked boxes, selects, textareas."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.data: dict[str, list[str]] = {}
        self._inside = False
        self._select: str | None = None
        self._chosen: list[str] = []
        self._textarea: str | None = None
        self._text = ""

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "form" and (attributes.get("id") or "").endswith("_form"):
            self._inside = True
        name = attributes.get("name")
        if not self._inside or (tag != "option" and not name):
            return
        if tag == "input":
            kind = (attributes.get("type") or "text").lower()
            if kind in ("submit", "button", "image", "file", "reset"):
                return
            if kind in ("checkbox", "radio") and "checked" not in attributes:
                return
            self.data.setdefault(name, []).append(attributes.get("value") or ("on" if kind == "checkbox" else ""))
        elif tag == "select":
            self._select, self._chosen = name, []
        elif tag == "option" and self._select is not None and "selected" in attributes:
            self._chosen.append(attributes.get("value") or "")
        elif tag == "textarea":
            self._textarea, self._text = name, ""

    def handle_data(self, data):
        if self._textarea is not None:
            self._text += data

    def handle_endtag(self, tag):
        if tag == "select" and self._select is not None:
            self.data[self._select] = self._chosen or [""]
            self._select = None
        elif tag == "textarea" and self._textarea is not None:
            self.data.setdefault(self._textarea, []).append(self._text.lstrip("\n"))
            self._textarea = None
        elif tag == "form":
            self._inside = False


def _admin_post(client, path: str, changes: dict):
    """Fetch an admin change form, change some of its fields as a browser would, post it back."""
    page = client.get(path)
    assert page.status_code == 200, (path, page.status_code)
    form = _AdminForm()
    form.feed(page.content.decode("utf-8"))
    data = {name: values if len(values) != 1 else values[0] for name, values in form.data.items()}
    data.update(changes)
    data["_save"] = "Save"
    return client.post(path, data)


def _move(client, case, target) -> str:
    client.post(_transition_url(case), {"status": target, "reason": "Motif de test"})
    case.refresh_from_db()
    return str(case.status)


@pytest.fixture
def back_office(django_user_model, case, cast):
    """The back office as production seeds it: the roles carry their MODEL permissions (role:operator: «cases» view and
    change), the operator — assigned to ``case`` — reaches it with the staff flag; another person's file carries a
    training body's assignment the operator has nothing to do with."""
    roles.ensure_roles()
    operator = cast["operator"]
    operator.is_staff = True
    operator.save(update_fields=["is_staff"])
    stranger = django_user_model.objects.create_user(email="f7.other.owner@example.test", password="x")
    roles.assign_role(stranger, roles.PERSON)
    other = services.open_case(stranger, purpose=CasePurpose.WORK, pathway_key="salaried_work")
    return {
        "operator": operator,
        "owner": cast["owner"],
        "superuser": cast["superuser"],
        "trainer": cast["training_body"],
        "own_assignment": case.assignments.get(assignee=operator),
        "other": other,
        "foreign_assignment": services.assign(other, cast["training_body"], role=AssignmentRole.TRAINING_BODY),
    }


class TestTheBackOffice:
    """
    The one screen that edits a file outside its services (no management command, signal, form or API writes a
    status: sec-f7 NOTES, «every path checked»). It cannot move a file — ``status`` and its trace are not in its form,
    and it declares no action of its own. And since WHO may move a file is read from the capacity an account holds on
    it, it hands out no capacity either (sec-f7 REVIEW, finding 2 — the reviewer's four probes, kept): a file's owner
    and its suspension's reason are read-only, an assignment is granted and ended through the domain and nothing else
    of it is editable. Every step goes through the back office's own pages with a minted session.
    """

    @staticmethod
    def _form(rf, user, case):
        from django.contrib import admin

        model_admin = admin.site._registry[CaseFile]
        request = rf.get("/backoffice/cases/casefile/")
        request.user = user
        return model_admin, request, model_admin.get_form(request, case)

    def test_the_case_files_form_holds_no_status_no_owner_no_reason_and_no_action_moves_one(self, rf, case, cast):
        model_admin, request, form = self._form(rf, cast["superuser"], case)
        held_back = {"status", "previous_status", "status_since", "closed_at", "person", "suspension_reason"}
        assert not held_back & set(form.base_fields)
        assert set(model_admin.get_actions(request)) <= {"delete_selected"}
        assert not model_admin.has_add_permission(request), "a file is opened by services.open_case"

    def test_the_operator_cannot_make_itself_a_files_owner_and_close_it(self, client, case, back_office):
        operator = back_office["operator"]
        _put(case, S.ORIENTED)
        client.force_login(operator)
        assert _move(client, case, S.CLOSED) == S.ORIENTED, "§4: the operator closes from POST_ENTRY only"
        _admin_post(client, f"{BACKOFFICE}casefile/{case.pk}/change/", {"person": str(operator.pk)})
        case.refresh_from_db()
        assert case.person_id == back_office["owner"].pk
        assert _move(client, case, S.CLOSED) == S.ORIENTED

    def test_the_operator_cannot_turn_its_assignment_into_a_professionals_and_conclude_a_review(
        self, client, case, back_office
    ):
        operator, row = back_office["operator"], back_office["own_assignment"]
        _put(case, S.REVIEW_REQUIRED)
        client.force_login(operator)
        assert _move(client, case, S.ORIENTED) == S.REVIEW_REQUIRED, "§4: the professional's alone"
        change = f"{BACKOFFICE}caseassignment/{row.pk}/change/"
        assert _admin_post(client, change, {"role": AssignmentRole.PROFESSIONAL}).status_code == 403
        # nor through the file's own form: its inline shows the assignment and edits nothing
        inline = {"assignments-0-role": AssignmentRole.PROFESSIONAL}
        _admin_post(client, f"{BACKOFFICE}casefile/{case.pk}/change/", inline)
        row.refresh_from_db()
        assert row.role == AssignmentRole.OPERATOR
        assert _move(client, case, S.ORIENTED) == S.REVIEW_REQUIRED

    def test_the_operator_cannot_take_over_another_files_assignment_and_move_that_file(self, client, back_office):
        other, operator, row = back_office["other"], back_office["operator"], back_office["foreign_assignment"]
        _put(other, S.ORIENTED)
        client.force_login(operator)
        assert client.get(f"{INDEX}{other.reference}/").status_code == 404, "not its file"
        change = f"{BACKOFFICE}caseassignment/{row.pk}/change/"
        response = _admin_post(client, change, {"assignee": str(operator.pk), "role": AssignmentRole.OPERATOR})
        assert response.status_code == 403
        row.refresh_from_db()
        assert (row.assignee_id, row.role) == (back_office["trainer"].pk, AssignmentRole.TRAINING_BODY)
        assert client.get(f"{INDEX}{other.reference}/").status_code == 404
        assert _move(client, other, S.ADMIN_PROCESS) == S.ORIENTED

    def test_a_suspended_files_reason_is_not_rewritten_there(self, client, case, back_office):
        """The reason the person reads on the dashboard's NowPanel is written by the domain with the move (§4 rules 3
        and 4) — never rewritten in the back office without a domain event."""
        _put(case, S.ORIENTED)
        services.transition(case, S.SUSPENDED, actor=back_office["owner"], reason="En attente du passeport")
        client.force_login(back_office["operator"])
        _admin_post(client, f"{BACKOFFICE}casefile/{case.pk}/change/", {"suspension_reason": "Texte réécrit"})
        case.refresh_from_db()
        assert case.suspension_reason == "En attente du passeport"

    def test_the_operator_ends_no_assignment_there(self, client, back_office):
        """«Only administrators create or revoke outside the services» (``cases.policies``): the operator reads an
        assignment's screen and changes nothing on it — not even its end."""
        row = back_office["foreign_assignment"]
        client.force_login(back_office["operator"])
        change = f"{BACKOFFICE}caseassignment/{row.pk}/change/"
        assert 'name="revoked_at_0"' not in client.get(change).content.decode("utf-8")
        assert client.post(change, {"revoked_at_0": "2026-10-16", "revoked_at_1": "10:00:00"}).status_code == 403
        row.refresh_from_db()
        assert row.revoked_at is None

    def test_the_administrator_grants_an_assignment_through_the_domain(
        self, client, case, back_office, django_user_model
    ):
        from notifications.events import ASSIGNMENT_GRANTED
        from notifications.models import Notification

        newcomer = django_user_model.objects.create_user(email="f7.newcomer@example.test", password="x")
        roles.assign_role(newcomer, roles.PROFESSIONAL)
        client.force_login(back_office["superuser"])
        response = client.post(
            f"{BACKOFFICE}caseassignment/add/",
            {
                "case": case.pk,
                "assignee": newcomer.pk,
                "role": AssignmentRole.PROFESSIONAL,
                "organisation": "",
                "authorisation_reference": "",
                "authorisation_jurisdiction": "",
                "authorisation_valid_until": "",
                "mandate_note": "",
                "_save": "Save",
            },
        )
        assert response.status_code == 302
        assert case.assignments.filter(assignee=newcomer, role=AssignmentRole.PROFESSIONAL).count() == 1
        event = AuditEvent.objects.get(action="case.assigned", target_id=str(case.pk), metadata__assignee=newcomer.pk)
        assert event.actor_id == back_office["superuser"].pk and event.metadata["role"] == AssignmentRole.PROFESSIONAL
        assert Notification.objects.filter(recipient=newcomer, event=ASSIGNMENT_GRANTED).count() == 1

    def test_the_administrator_ends_an_assignment_through_the_domain_and_changes_nothing_else(
        self, client, back_office
    ):
        from notifications.events import ASSIGNMENT_REVOKED
        from notifications.models import Notification

        row, operator, superuser = back_office["own_assignment"], back_office["operator"], back_office["superuser"]
        client.force_login(superuser)
        change = f"{BACKOFFICE}caseassignment/{row.pk}/change/"
        response = _admin_post(
            client,
            change,
            {
                "revoked_at_0": "2026-10-16",
                "revoked_at_1": "10:00:00",
                "role": AssignmentRole.PROFESSIONAL,
                "assignee": str(superuser.pk),
                "authorisation_valid_until": "2099-12-31",
            },
        )
        assert response.status_code == 302
        row.refresh_from_db()
        assert row.revoked_at is not None
        assert (row.role, row.assignee_id) == (AssignmentRole.OPERATOR, operator.pk)
        assert row.authorisation_valid_until is None
        event = AuditEvent.objects.get(action="case.assignment.revoked", metadata__assignment=row.pk)
        assert event.actor_id == superuser.pk
        assert Notification.objects.filter(recipient=operator, event=ASSIGNMENT_REVOKED).count() == 1
        # and an assignment that ended is never revived there: its screen is read-only, a new one is granted instead
        assert _admin_post(client, change, {"revoked_at_0": "", "revoked_at_1": ""}).status_code == 403
        row.refresh_from_db()
        assert row.revoked_at is not None


# ---------------------------------------------------------------------------------------------
# The row a move is judged on
# ---------------------------------------------------------------------------------------------
class TestTheRowAMoveIsJudgedOn:
    """sec-f7 REVIEW, finding 5: ``transition`` re-reads the file's row and locks it before it judges a move, so a
    request that loaded the file before another account moved it is judged on where the file IS — WHO may move a file
    depends on that — and never writes its stale state over a newer one."""

    def test_a_move_computed_on_a_stale_row_does_not_overwrite_a_newer_state(self, owner, case, cast):
        _put(case, S.ORIENTED)
        services.transition(case, S.SUSPENDED, actor=owner, reason="Pause")
        stale = CaseFile.objects.get(pk=case.pk)  # the person's page loaded it: «suspended by me, from ORIENTED»
        services.resume(CaseFile.objects.get(pk=case.pk), actor=cast["administrator"])  # meanwhile: lifted…
        services.transition(CaseFile.objects.get(pk=case.pk), S.ADMIN_PROCESS, actor=cast["operator"])  # …moved on
        with pytest.raises(services.TransitionRefused):
            services.transition(stale, S.ORIENTED, actor=owner)
        case.refresh_from_db()
        assert case.status == S.ADMIN_PROCESS, "ADMIN_PROCESS → ORIENTED is nobody's move"
        assert stale.status == S.ADMIN_PROCESS, "the caller's instance is told where the file is"

    def test_a_suspension_computed_on_a_stale_row_records_where_the_file_really_was(self, owner, case, cast):
        _put(case, S.ORIENTED)
        stale = CaseFile.objects.get(pk=case.pk)  # ORIENTED, as the person's page showed it
        services.transition(CaseFile.objects.get(pk=case.pk), S.ADMIN_PROCESS, actor=cast["operator"])
        services.transition(stale, S.SUSPENDED, actor=owner, reason="Pause")
        case.refresh_from_db()
        assert (case.status, case.previous_status) == (S.SUSPENDED, S.ADMIN_PROCESS)
        assert (stale.status, stale.previous_status) == (S.SUSPENDED, S.ADMIN_PROCESS)
        services.resume(case, actor=owner)
        case.refresh_from_db()
        assert case.status == S.ADMIN_PROCESS, "suspending and resuming never undoes somebody else's move"

    def test_the_row_is_locked_before_the_move_is_judged(self, owner, case):
        from django.db import connection
        from django.test.utils import CaptureQueriesContext

        _put(case, S.ORIENTED)
        with CaptureQueriesContext(connection) as queries:
            services.transition(case, S.SUSPENDED, actor=owner, reason="Pause")
        statements = [query["sql"] for query in queries.captured_queries]
        statements = [sql for sql in statements if not sql.startswith(("SAVEPOINT", "RELEASE SAVEPOINT"))]
        assert '"cases_casefile"' in statements[0] and statements[0].endswith("FOR NO KEY UPDATE")
        assert sum("FOR NO KEY UPDATE" in sql for sql in statements) == 1


# ---------------------------------------------------------------------------------------------
# What did not change
# ---------------------------------------------------------------------------------------------
def test_a_permitted_move_is_audited_as_before_and_a_refused_one_leaves_nothing(case, cast, owner):
    from notifications.models import Notification

    _put(case, S.ORIENTED)
    sent = Notification.objects.count()
    with pytest.raises(services.TransitionNotPermitted):
        services.transition(case, S.ADMIN_PROCESS, actor=owner)
    assert not _moves_to(case, S.ADMIN_PROCESS) and Notification.objects.count() == sent
    services.transition(case, S.ADMIN_PROCESS, actor=cast["operator"], reason="Dossier complet")
    event = AuditEvent.objects.get(action="case.transition", target_id=str(case.pk))
    assert event.actor_id == cast["operator"].pk
    assert event.metadata == {"from": S.ORIENTED, "to": S.ADMIN_PROCESS, "reason": "Dossier complet"}
    assert Notification.objects.count() == sent + 1, "the person is told, as before"


def test_a_closed_file_stays_read_only_for_everybody(case, cast):
    _put(case, S.CLOSED)
    for role, user in cast.items():
        assert services.transitions_available(case, user) == [], role
        with pytest.raises(services.TransitionRefused):
            services.transition(case, S.ORIENTED, actor=user)


def test_selection_still_needs_a_valid_authorised_actor_on_every_path(case, cast):
    """CR-03 (§4 rule 1), unchanged: without a valid authorised actor assigned, neither the platform's own path nor the
    selection service's reaches SELECTION — and the administrator, who never makes that move, is refused as well."""
    for assignment in case.assignments.filter(role=AssignmentRole.AUTHORISED_ACTOR):
        services.revoke_assignment(assignment)
    _put(case, S.TRAINING)
    assert S.SELECTION not in dict(services.transitions_available(case, cast["administrator"]))
    for actor, as_authorised_actor in ((cast["administrator"], False), (None, False), (cast["authorised"], True)):
        with pytest.raises(services.TransitionRefused):
            services.transition(case, S.SELECTION, actor=actor, as_authorised_actor=as_authorised_actor)
        case.refresh_from_db()
        assert case.status == S.TRAINING


def test_only_an_authorised_actors_assignment_satisfies_cr_03(owner, django_user_model):
    """sec-f7 REVIEW, the CR-03 observation (the reviewer's probe, kept): an operator's or a professional's assignment
    that carries an authorisation reference and a validity is not «un AuthorizedActor valido, non scaduto e assegnato»
    (§4 rule 1) — SELECTION stays out of reach, on the platform's own path too."""
    case = services.open_case(owner, purpose=CasePurpose.WORK, pathway_key="salaried_work")
    _put(case, S.TRAINING)
    for index, role in enumerate((AssignmentRole.OPERATOR, AssignmentRole.PROFESSIONAL, AssignmentRole.TRAINING_BODY)):
        assignee = django_user_model.objects.create_user(email=f"f7.cr03.{index}@example.test", password="x")
        services.assign(
            case,
            assignee,
            role=role,
            authorisation_reference="NOT-AN-AUTHORISATION",
            authorisation_valid_until=clock.today() + dt.timedelta(days=30),
        )
    assert not case.has_valid_authorised_actor()
    with pytest.raises(services.TransitionRefused):
        services.transition(case, S.SELECTION)
    case.refresh_from_db()
    assert case.status == S.TRAINING


def test_the_view_still_answers_403_where_the_policy_refuses_and_404_to_a_stranger(client, case, cast):
    _put(case, S.ORIENTED)
    client.force_login(cast["training_body"])
    assert client.post(_transition_url(case), {"status": S.TRAINING}).status_code == 403
    client.force_login(cast["stranger"])
    assert client.post(_transition_url(case), {"status": S.SUSPENDED, "reason": "x"}).status_code == 404


def test_permission_denied_is_never_the_domains_answer(case, cast):
    """A refusal of WHO is a domain refusal (a ``ValidationError`` the view turns into a message), never a 403 raised
    from the service: the 403 stays the object policy's, in the view."""
    _put(case, S.ORIENTED)
    with pytest.raises(services.TransitionNotPermitted) as refused:
        services.transition(case, S.ADMIN_PROCESS, actor=cast["owner"])
    assert isinstance(refused.value, ValidationError) and not isinstance(refused.value, PermissionDenied)
