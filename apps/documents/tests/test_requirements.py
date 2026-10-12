"""
The seven states, the derivation that produces them, versions inside a row, and expiry.

These tests are the contract of REQ-DOC-01, REQ-DOC-04 and REQ-DOC-05: what a person reads on the
register, why, and when it changes on its own.
"""

from __future__ import annotations

import datetime as dt

import pytest

from audit.models import AuditEvent
from cases.models import CaseStatus, ResponsibleActor
from cases.services import transition
from core import clock
from documents import services
from documents.models import (
    DocumentKind,
    DocumentRequirement,
    RequirementState,
    ScanStatus,
    VersionDecision,
)
from documents.requirements import REPLACE_WINDOW_DAYS, counts, derive_state, sort_key, state_css
from documents.tests.conftest import upload_file

pytestmark = pytest.mark.django_db

MINIMAL_PDF = (
    b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
    b"2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n"
    b"3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 200 200]>>endobj\n"
    b"trailer<</Root 1 0 R>>\n%%EOF\n"
)


def pdf(name="piece.pdf"):
    return upload_file(name, MINIMAL_PDF, "application/pdf")


# ---------------------------------------------------------------------------------------------
# Declaration
# ---------------------------------------------------------------------------------------------
def test_declare_requirement_is_idempotent_on_its_code(case):
    first = services.declare_requirement(
        case, code="diploma", title="Diplôme", responsible_actor=ResponsibleActor.PERSON
    )
    again = services.declare_requirement(
        case, code="diploma", title="Diplôme ou titre", responsible_actor=ResponsibleActor.PERSON
    )
    assert first.pk == again.pk, "replaying an orientation outcome must not duplicate the register"
    assert DocumentRequirement.objects.filter(case=case).count() == 1
    assert again.title == "Diplôme ou titre"


def test_a_requirement_without_a_responsible_actor_is_invalid(case):
    with pytest.raises(Exception):
        services.declare_requirement(case, code="x", title="Sans responsable", responsible_actor="")


def test_declaration_is_audited(case):
    services.declare_requirement(case, code="passport", title="Passeport", responsible_actor=ResponsibleActor.PERSON)
    assert AuditEvent.objects.filter(action="documents.requirement.declared").exists()


# ---------------------------------------------------------------------------------------------
# The seven states
# ---------------------------------------------------------------------------------------------
def test_nothing_filed_is_missing(requirement):
    assert requirement.display_state == RequirementState.MISSING
    assert state_css(requirement.display_state) == "missing"


def test_filing_makes_it_deposited_not_pending_analysis(requirement, owner):
    version = services.file_version(requirement, owner, pdf())
    requirement.refresh_from_db()
    # The scanner has not run — there is none — and the person's state must NOT borrow the
    # scanner's vocabulary: the piece is DÉPOSÉ, and the antivirus says so separately.
    assert version.document.scan_status == ScanStatus.NOT_CONFIGURED
    assert requirement.display_state == RequirementState.FILED
    assert requirement.state == RequirementState.FILED


def test_review_states(requirement, owner, professional):
    version = services.file_version(requirement, owner, pdf())
    services.set_decision(version, VersionDecision.IN_REVIEW, actor=professional)
    requirement.refresh_from_db()
    assert requirement.display_state == RequirementState.IN_REVIEW

    services.set_decision(version, VersionDecision.ACCEPTED, actor=professional)
    requirement.refresh_from_db()
    assert requirement.display_state == RequirementState.VALID

    services.set_decision(version, VersionDecision.REFUSED, actor=professional, note="Page manquante.")
    requirement.refresh_from_db()
    assert requirement.display_state == RequirementState.INVALID
    assert requirement.state_note == "Page manquante."


def test_a_refusal_must_carry_its_motive(requirement, owner, professional):
    version = services.file_version(requirement, owner, pdf())
    with pytest.raises(services.RequirementRefused):
        services.set_decision(version, VersionDecision.REFUSED, actor=professional, note="   ")


def test_expiry_happens_on_its_own(requirement, owner):
    yesterday = clock.today() - dt.timedelta(days=1)
    services.file_version(requirement, owner, pdf(), expires_on=yesterday)
    requirement.refresh_from_db()
    assert requirement.display_state == RequirementState.EXPIRED


def test_a_piece_expiring_soon_must_be_replaced_before_it_lapses(requirement, owner):
    soon = clock.today() + dt.timedelta(days=REPLACE_WINDOW_DAYS - 1)
    services.file_version(requirement, owner, pdf(), expires_on=soon)
    requirement.refresh_from_db()
    assert requirement.display_state == RequirementState.TO_REPLACE

    far = clock.today() + dt.timedelta(days=REPLACE_WINDOW_DAYS + 5)
    services.file_version(requirement, owner, pdf("autre.pdf"), expires_on=far)
    requirement.refresh_from_db()
    assert requirement.display_state == RequirementState.FILED


def test_replacement_request_moves_the_row_and_needs_a_reason(requirement, owner, professional):
    services.file_version(requirement, owner, pdf())
    with pytest.raises(services.RequirementRefused):
        services.request_replacement(requirement, actor=professional, reason="")
    services.request_replacement(requirement, actor=professional, reason="Scan illisible.")
    requirement.refresh_from_db()
    assert requirement.display_state == RequirementState.TO_REPLACE
    assert requirement.state_note == "Scan illisible."


def test_filing_again_answers_an_outstanding_replacement_request(requirement, owner, professional):
    services.file_version(requirement, owner, pdf())
    services.request_replacement(requirement, actor=professional, reason="Scan illisible.")
    services.file_version(requirement, owner, pdf("net.pdf"))
    requirement.refresh_from_db()
    assert requirement.replacement_requested_at is None
    assert requirement.display_state == RequirementState.FILED


def test_an_infected_file_makes_the_piece_invalid_not_merely_unscanned(requirement, owner):
    version = services.file_version(requirement, owner, pdf())
    services.apply_scan_result(version.document, ScanStatus.INFECTED, note="test")
    version.refresh_from_db()
    requirement.refresh_from_db()
    assert requirement.derived_state() == RequirementState.INVALID


def test_a_purged_file_puts_the_requirement_back_to_missing(requirement, owner):
    version = services.file_version(requirement, owner, pdf())
    services.purge_document(version.document, reason="test")
    version.refresh_from_db()
    requirement.refresh_from_db()
    assert requirement.derived_state() == RequirementState.MISSING


def test_every_state_has_a_css_word_and_they_are_all_distinct():
    css = {state_css(value) for value in RequirementState.values}
    assert len(css) == 7, "each of the seven states carries its own word and rule, never a shared colour"


# ---------------------------------------------------------------------------------------------
# Versions inside the row
# ---------------------------------------------------------------------------------------------
def test_versions_live_inside_the_row_and_the_history_is_kept(requirement, owner):
    first = services.file_version(requirement, owner, pdf("v1.pdf"))
    second = services.file_version(requirement, owner, pdf("v2.pdf"))
    first.refresh_from_db()
    assert requirement.versions.count() == 2
    assert second.number == 2 and second.is_current
    assert not first.is_current and first.superseded_at is not None
    assert first.document is not None, "the previous deposit is kept, not deleted"
    assert requirement.current_version.pk == second.pk


def test_only_one_version_is_ever_current(requirement, owner):
    services.file_version(requirement, owner, pdf("v1.pdf"))
    services.file_version(requirement, owner, pdf("v2.pdf"))
    services.file_version(requirement, owner, pdf("v3.pdf"))
    assert requirement.versions.filter(is_current=True).count() == 1


def test_only_the_version_in_force_can_be_reviewed(requirement, owner, professional):
    first = services.file_version(requirement, owner, pdf("v1.pdf"))
    services.file_version(requirement, owner, pdf("v2.pdf"))
    first.refresh_from_db()
    with pytest.raises(services.RequirementRefused):
        services.set_decision(first, VersionDecision.ACCEPTED, actor=professional)


def test_filing_is_refused_on_a_closed_case(requirement, owner):
    transition(requirement.case, CaseStatus.CLOSED)
    requirement.case.refresh_from_db()
    requirement = DocumentRequirement.objects.get(pk=requirement.pk)
    with pytest.raises(services.RequirementRefused):
        services.file_version(requirement, owner, pdf())


def test_filing_goes_through_the_same_validation_chain(requirement, owner):
    from documents.services import UploadRejected

    with pytest.raises(UploadRejected):
        services.file_version(requirement, owner, upload_file("piege.svg", b"<svg><script/></svg>", "image/svg+xml"))
    assert requirement.versions.count() == 0


def test_filing_is_audited_with_the_version_it_created(requirement, owner):
    services.file_version(requirement, owner, pdf())
    event = AuditEvent.objects.filter(action="documents.requirement.filed").first()
    assert event is not None and event.metadata["version"] == 1
    assert event.metadata["code"] == requirement.code


# ---------------------------------------------------------------------------------------------
# Reconciliation and ordering
# ---------------------------------------------------------------------------------------------
def test_refresh_reconciles_the_stored_state_and_audits_the_move(requirement, owner):
    version = services.file_version(requirement, owner, pdf(), expires_on=clock.today() + dt.timedelta(days=2))
    requirement.refresh_from_db()
    assert requirement.state == RequirementState.TO_REPLACE

    # The piece lapses while nobody is looking.
    version.expires_on = clock.today() - dt.timedelta(days=1)
    version.save(update_fields=["expires_on"])
    changed = services.refresh_all_states()
    requirement.refresh_from_db()
    assert requirement.state == RequirementState.EXPIRED
    assert changed == {"to_replace->expired": 1}
    assert AuditEvent.objects.filter(action="documents.requirement.state").exists()


def test_the_register_puts_the_blocking_rows_first(case, owner, professional):
    from cases.models import ResponsibleActor as RA

    expired = services.declare_requirement(case, code="a", title="A", responsible_actor=RA.PERSON, order=9)
    services.file_version(expired, owner, pdf("a.pdf"), expires_on=clock.today() - dt.timedelta(days=1))
    valid = services.declare_requirement(case, code="b", title="B", responsible_actor=RA.PERSON, order=0)
    version = services.file_version(valid, owner, pdf("b.pdf"))
    services.set_decision(version, VersionDecision.ACCEPTED, actor=professional)
    missing = services.declare_requirement(case, code="c", title="C", responsible_actor=RA.AUTHORITY, order=1)

    rows = sorted(DocumentRequirement.objects.filter(case=case), key=sort_key)
    assert [row.code for row in rows] == ["a", "c", "b"], "expired, then missing, then valid"
    assert [expired.pk, missing.pk, valid.pk] == [row.pk for row in rows]


def test_counts_are_counts_and_never_a_percentage(case, owner, professional):
    from cases.models import ResponsibleActor as RA

    one = services.declare_requirement(case, code="a", title="A", responsible_actor=RA.PERSON)
    services.declare_requirement(case, code="b", title="B", responsible_actor=RA.AUTHORITY)
    version = services.file_version(one, owner, pdf())
    services.set_decision(version, VersionDecision.ACCEPTED, actor=professional)

    summary = counts(DocumentRequirement.objects.filter(case=case))
    assert summary["total"] == 2 and summary["valid"] == 1 and summary["missing"] == 1
    assert "percent" not in summary and "progress" not in summary


def test_derive_state_is_pure_and_takes_the_day_as_an_argument(requirement, owner):
    version = services.file_version(requirement, owner, pdf(), expires_on=clock.today() + dt.timedelta(days=200))
    assert derive_state(requirement, version) == RequirementState.FILED
    later = clock.today() + dt.timedelta(days=201)
    assert derive_state(requirement, version, today=later) == RequirementState.EXPIRED


def test_the_kind_of_the_requirement_is_carried_to_the_stored_file(case, owner):
    requirement = services.declare_requirement(
        case,
        code="id",
        title="Passeport",
        responsible_actor=ResponsibleActor.PERSON,
        kind=DocumentKind.IDENTITY,
    )
    version = services.file_version(requirement, owner, pdf())
    assert version.document.kind == DocumentKind.IDENTITY


# ---------------------------------------------------------------------------------------------
# The command and the seed
# ---------------------------------------------------------------------------------------------
def test_refresh_command_reports_what_moved(requirement, owner, capsys):
    from io import StringIO

    from django.core.management import call_command

    version = services.file_version(requirement, owner, pdf())
    version.expires_on = clock.today() - dt.timedelta(days=1)
    version.save(update_fields=["expires_on"])
    out = StringIO()
    call_command("documents_refresh_requirements", stdout=out)
    assert "filed->expired: 1" in out.getvalue()
    requirement.refresh_from_db()
    assert requirement.state == RequirementState.EXPIRED

    out = StringIO()
    call_command("documents_refresh_requirements", stdout=out)
    assert "No requirement changed state." in out.getvalue(), "the command is idempotent"


def test_the_seed_puts_all_seven_words_on_one_screen(case, superuser):
    """A feature nobody can see working is a feature nobody can check."""
    from documents.seeds import seed_document_register

    message = seed_document_register()
    assert "requirement(s) declared" in message
    states = {row.display_state for row in DocumentRequirement.objects.filter(case=case)}
    assert states == set(RequirementState.values), states
    assert seed_document_register() == "document register already seeded", "idempotent"


def test_the_seed_does_nothing_without_a_case(db):
    from documents.seeds import seed_document_register

    assert seed_document_register() == "no case file: nothing seeded"


# ---------------------------------------------------------------------------------------------
# The rule engine asks this app what a case has obtained
# ---------------------------------------------------------------------------------------------
def test_valid_document_codes_names_only_the_pieces_actually_obtained(case, owner, professional):
    from cases.models import ResponsibleActor as RA

    accepted = services.declare_requirement(case, code="passport", title="P", responsible_actor=RA.PERSON)
    version = services.file_version(accepted, owner, pdf("p.pdf"))
    services.set_decision(version, VersionDecision.ACCEPTED, actor=professional)

    services.declare_requirement(case, code="nulla_osta", title="N", responsible_actor=RA.AUTHORITY)
    merely_filed = services.declare_requirement(case, code="diploma", title="D", responsible_actor=RA.PERSON)
    services.file_version(merely_filed, owner, pdf("d.pdf"))

    assert services.valid_document_codes(case) == ["passport"]


def test_valid_document_codes_drops_a_piece_the_day_it_lapses(case, owner, professional):
    from cases.models import ResponsibleActor as RA

    requirement = services.declare_requirement(case, code="passport", title="P", responsible_actor=RA.PERSON)
    version = services.file_version(requirement, owner, pdf("p.pdf"), expires_on=clock.today() + dt.timedelta(days=200))
    services.set_decision(version, VersionDecision.ACCEPTED, actor=professional)
    assert services.valid_document_codes(case) == ["passport"]

    # The derived state is used, so the answer changes without any command having run.
    version.expires_on = clock.today() - dt.timedelta(days=1)
    version.save(update_fields=["expires_on"])
    assert services.valid_document_codes(case) == []
