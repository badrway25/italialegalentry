"""
Domain services of the company workspace.

Every state change goes through this module — the views, the admin, the management commands and any
future API call the same functions — so the declared transition table, the authorisation rule of
CR-03 and the audit trail cannot be bypassed by choosing a different entry point.

Nothing in this module returns a person. The only account-shaped object it touches is the actor
answerable for a need, and it is named by organisation or role, never by e-mail address.
"""

from __future__ import annotations

from dataclasses import dataclass

from django.core.exceptions import PermissionDenied, ValidationError
from django.db import models, transaction
from django.urls import NoReverseMatch, reverse
from django.utils import timezone
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _

from accounts import roles
from accounts.models import Membership, MembershipRole, Organisation, OrganisationKind
from accounts.permissions import can, require
from audit.services import record
from companies.models import (
    AGGREGATED_STATUSES,
    REQUIRES_AUTHORISED_ACTOR,
    ActorRole,
    CompanyNeed,
    CompanyProfile,
    NeedAssignment,
    NeedEvent,
    NeedStatus,
    SkillLevel,
    transitions_from,
)
from core import icons

#: Roles allowed to read the territorial / sectoral aggregate. Counts only, never a row.
ANALYSIS_ROLES = (roles.STAFF, roles.ADMINISTRATOR)


class TransitionRefused(ValidationError):
    """A state change the domain does not allow. Never downgraded to a silent no-op."""


def safe_reverse(name: str, *args) -> str:
    """Reverse a route that may not be wired yet; "" rather than a 500 while the include is pending."""
    try:
        return reverse(name, args=args or None)
    except NoReverseMatch:
        return ""


# ---------------------------------------------------------------------------------------------
# The company
# ---------------------------------------------------------------------------------------------
def company_for(user) -> CompanyProfile | None:
    """
    The company this account is responsible for, or None.

    Applied through ``readable_by``, so the answer can never be somebody else's company even if the
    account is a member of several organisations.
    """
    return (
        CompanyProfile.objects.readable_by(user)
        .select_related("organisation", "sector")
        .filter(organisation__memberships__user=user)
        .order_by("legal_name")
        .first()
    )


@transaction.atomic
def declare_company(user, *, data: dict, request=None) -> CompanyProfile:
    """
    Create the organisation, the responsible membership and the company profile in one act, and
    open the verification request that ``accounts`` will decide.

    The account declares; the project verifies. Nothing here grants a role, and nothing here marks
    a company verified: that separation is the whole point of ``accounts.AccountVerification``.
    """
    from accounts import services as account_services
    from accounts.models import AccountType, AccountVerification

    existing = company_for(user)
    if existing is not None:
        raise ValidationError(_("Ce compte est déjà rattaché à une entreprise."))

    # ``accounts.AccountVerification`` holds ONE row per account, recording what that account
    # declared. An account that already declared another type would keep that row, so the company
    # would never be the subject of a verification request — and, if that row were already
    # approved, ``CompanyProfile.verification`` would ignore it (it only reads a row declared as a
    # company) and the entreprise would sit unverifiable for good. Refuse plainly instead of
    # creating a company that cannot be verified.
    declared = AccountVerification.objects.filter(user=user).first()
    if declared is not None and declared.declared_type != AccountType.COMPANY:
        raise ValidationError(
            gettext(
                "Ce compte est déjà enregistré sous un autre type déclaré (%(type)s). La vérification "
                "porte sur un type d’acteur à la fois : écrivez à l’équipe du projet pour faire "
                "rattacher l’entreprise, ou déclarez-la depuis un compte entreprise."
            )
            % {"type": declared.get_declared_type_display()}
        )

    legal_name = (data.get("legal_name") or "").strip()
    organisation = Organisation.objects.create(
        name=(data.get("trade_name") or legal_name).strip(),
        kind=OrganisationKind.COMPANY,
        country=data.get("country") or "IT",
        city=data.get("city") or "",
        website=data.get("website") or "",
        created_by=user,
    )
    Membership.objects.create(user=user, organisation=organisation, role=MembershipRole.OWNER)

    profile = CompanyProfile(organisation=organisation, **data)
    profile.full_clean()
    profile.save()

    account_services.register_declared_account_type(user, AccountType.COMPANY, request=request)
    record(
        request,
        actor=user,
        action="companies.profile.declared",
        target=profile,
        metadata={"organisation_id": organisation.pk},
    )
    return profile


@transaction.atomic
def update_company(profile: CompanyProfile, *, data: dict, actor=None, request=None) -> CompanyProfile:
    """Update the identity of the company. Never its verification state — accounts decides that."""
    require(actor, "change", profile)
    # Compared against the STORED row, not against the object in hand: a ModelForm has already
    # written the submitted values onto its instance by the time it validates, so diffing the
    # in-memory object would find nothing changed and would silently save nothing.
    stored = CompanyProfile.objects.get(pk=profile.pk)
    changed = [field for field, value in data.items() if getattr(stored, field, None) != value]
    for field, value in data.items():
        setattr(profile, field, value)
    if not changed:
        return profile
    profile.full_clean()
    profile.save()
    # Metadata carries the FIELD NAMES only: an audit row must say what changed without copying the
    # personal data it changed.
    record(request, actor=actor, action="companies.profile.updated", target=profile, metadata={"fields": changed})
    return profile


# ---------------------------------------------------------------------------------------------
# Needs
# ---------------------------------------------------------------------------------------------
def needs_of(company: CompanyProfile):
    return (
        CompanyNeed.objects.filter(company=company)
        .select_related("territory", "sector")
        .prefetch_related("assignments__organisation", "skills")
        .order_by("-created_at")
    )


def get_own_need(user, reference: str) -> CompanyNeed:
    """
    The single door to a need detail page.

    The lookup runs through ``readable_by``, so an unauthorised reference is indistinguishable from
    a reference that does not exist: 404 in both cases, never a differently worded refusal.
    """
    from django.http import Http404

    need = (
        CompanyNeed.objects.readable_by(user)
        .select_related("company__organisation", "territory", "sector")
        .prefetch_related("skills", "assignments__organisation", "events")
        .filter(reference=reference)
        .first()
    )
    if need is None:
        raise Http404
    if not can(user, "view", need):
        raise Http404
    return need


@transaction.atomic
def create_need(company: CompanyProfile, *, data: dict, actor=None, request=None) -> CompanyNeed:
    """Open a need in DRAFT. A company creates and manages SEVERAL needs (REQ-B2B-04)."""
    need = CompanyNeed(company=company, status=NeedStatus.DRAFT, **data)
    need.full_clean(exclude=["reference"])
    need.save()
    NeedEvent.objects.create(
        need=need,
        from_status="",
        to_status=NeedStatus.DRAFT,
        note=str(_("Besoin créé.")),
        responsible_label=company.legal_name,
    )
    record(
        request,
        actor=actor,
        action="companies.need.created",
        target=need,
        metadata={"company_id": company.pk, "territory": data.get("territory") and str(data["territory"])},
    )
    return need


@transaction.atomic
def update_need(need: CompanyNeed, *, data: dict, actor=None, request=None) -> CompanyNeed:
    require(actor, "change", need)
    # Same reasoning as ``update_company``: the comparison is against the stored row.
    stored = CompanyNeed.objects.get(pk=need.pk)
    changed = [field for field, value in data.items() if getattr(stored, field, None) != value]
    for field, value in data.items():
        setattr(need, field, value)
    if not changed:
        return need
    need.full_clean(exclude=["reference"])
    need.save()
    record(request, actor=actor, action="companies.need.updated", target=need, metadata={"fields": changed})
    return need


@transaction.atomic
def set_skills(need: CompanyNeed, *, mandatory: list[str], preferred: list[str], actor=None, request=None) -> None:
    """
    Replace the skill matrix of a need.

    A matrix of rows, not a paragraph: the Academy's skill gap is « required → held → gap → module »,
    and a paragraph cannot take part in that.
    """
    require(actor, "change", need)
    from companies.models import NeedSkill

    wanted: list[tuple[str, str, int]] = []
    seen: set[tuple[str, str]] = set()
    for level, labels in ((SkillLevel.MANDATORY, mandatory), (SkillLevel.PREFERRED, preferred)):
        for order, label in enumerate(labels):
            cleaned = (label or "").strip()
            if cleaned and (cleaned, level) not in seen:
                seen.add((cleaned, level))
                wanted.append((cleaned, level, order))

    need.skills.all().delete()
    rows = []
    for cleaned, level, order in wanted:
        row = NeedSkill(need=need, label=cleaned, level=level, order=order)
        row.full_clean(exclude=["need"])
        rows.append(row)
    NeedSkill.objects.bulk_create(rows)
    record(
        request,
        actor=actor,
        action="companies.need.skills_set",
        target=need,
        metadata={"mandatory": len(mandatory), "preferred": len(preferred)},
    )


# ---------------------------------------------------------------------------------------------
# Transitions
# ---------------------------------------------------------------------------------------------
@transaction.atomic
def transition(
    need: CompanyNeed, target: str, *, actor=None, note: str = "", responsible_label: str = "", request=None
) -> CompanyNeed:
    """
    Move ``need`` to ``target``, or refuse.

    Refusals are exceptions, not return values: a silently ignored transition would leave the
    interface showing a state the domain never reached.
    """
    if target not in NeedStatus.values:
        raise TransitionRefused(_("État non reconnu."))
    if target == need.status:
        return need
    if target not in transitions_from(need.status):
        raise TransitionRefused(
            gettext("Transition non autorisée de « %(from)s » vers « %(to)s ».")
            % {"from": need.get_status_display(), "to": dict(NeedStatus.choices)[target]}
        )
    if target in {NeedStatus.SUBMITTED} and not need.company.is_verified:
        raise TransitionRefused(_("Un besoin n’est transmis qu’une fois l’entreprise vérifiée par l’équipe du projet."))
    if target in {NeedStatus.SUBMITTED} and not need.is_complete:
        raise TransitionRefused(
            gettext("Le besoin est incomplet : il manque %(items)s.")
            % {"items": ", ".join(need.missing_for_submission())}
        )
    if target in REQUIRES_AUTHORISED_ACTOR and not need.has_live_authorised_actor():
        # CR-03: a reserved activity belongs to an authorised party. No live authorisation, no
        # taking in charge — the same rule the case file applies to SELECTION.
        raise TransitionRefused(
            _("La prise en charge exige un acteur autorisé assigné, avec une autorisation en cours de validité.")
        )
    if target == NeedStatus.ON_HOLD and not note.strip():
        raise TransitionRefused(_("Une mise en attente doit être motivée."))

    previous = need.status
    need.status = target
    need.status_since = timezone.now()
    if target == NeedStatus.ON_HOLD:
        need.hold_reason = note.strip()[:300]
    elif previous == NeedStatus.ON_HOLD:
        need.hold_reason = ""
    if target == NeedStatus.SUBMITTED and need.submitted_at is None:
        need.submitted_at = timezone.now()
    if target in {NeedStatus.CLOSED, NeedStatus.WITHDRAWN}:
        need.closed_at = timezone.now()
    need.save(update_fields=["status", "status_since", "hold_reason", "submitted_at", "closed_at", "updated_at"])

    NeedEvent.objects.create(
        need=need,
        from_status=previous,
        to_status=target,
        note=note.strip()[:300],
        responsible_label=responsible_label or _default_responsible_label(need, actor),
    )
    record(
        request,
        actor=actor,
        action="companies.need.transition",
        target=need,
        metadata={"from": previous, "to": target, "note": note[:300]},
    )
    return need


def _default_responsible_label(need: CompanyNeed, actor) -> str:
    """Who is answerable for the step — an organisation or a role, never an e-mail address."""
    if actor is not None and need.company.organisation.memberships.filter(user=actor).exists():
        return need.company.legal_name
    live = need.live_assignments()
    if live:
        return live[0].display_name
    return str(_("Équipe du projet"))


def submit(need: CompanyNeed, *, actor, request=None) -> CompanyNeed:
    """The company transmits its need to the project. Requires a verified company (REQ-B2B-01)."""
    require(actor, "submit", need)
    return transition(need, NeedStatus.SUBMITTED, actor=actor, request=request)


def withdraw(need: CompanyNeed, *, actor, reason: str = "", request=None) -> CompanyNeed:
    require(actor, "withdraw", need)
    return transition(need, NeedStatus.WITHDRAWN, actor=actor, note=reason, request=request)


# ---------------------------------------------------------------------------------------------
# Actors answerable for a need (first link of the chain of CR-03)
# ---------------------------------------------------------------------------------------------
@transaction.atomic
def assign_actor(
    need: CompanyNeed,
    *,
    assignee,
    role: str,
    organisation=None,
    authorisation_reference: str = "",
    authorisation_jurisdiction: str = "",
    authorisation_valid_until=None,
    mandate_note: str = "",
    actor=None,
    request=None,
) -> NeedAssignment:
    """
    Name the party answerable for a need.

    Only an administrator may do this: an assignment a company could write for itself would be a
    self-issued authorisation, which is exactly what CR-03 forbids.
    """
    if actor is not None and not roles.has_role(actor, roles.ADMINISTRATOR):
        raise PermissionDenied
    assignment = NeedAssignment(
        need=need,
        assignee=assignee,
        role=role,
        organisation=organisation,
        authorisation_reference=authorisation_reference,
        authorisation_jurisdiction=authorisation_jurisdiction,
        authorisation_valid_until=authorisation_valid_until,
        mandate_note=mandate_note,
    )
    assignment.full_clean(exclude=["need", "assignee"])
    assignment.save()
    record(
        request,
        actor=actor,
        action="companies.need.actor_assigned",
        target=need,
        metadata={
            "role": role,
            "assignment_id": assignment.pk,
            "has_authorisation": bool(authorisation_reference),
            "valid_until": str(authorisation_valid_until or ""),
        },
    )
    return assignment


@transaction.atomic
def revoke_actor(assignment: NeedAssignment, *, actor=None, request=None) -> NeedAssignment:
    if actor is not None and not roles.has_role(actor, roles.ADMINISTRATOR):
        raise PermissionDenied
    if assignment.revoked_at is None:
        assignment.revoked_at = timezone.now()
        assignment.save(update_fields=["revoked_at", "updated_at"])
        record(
            request,
            actor=actor,
            action="companies.need.actor_revoked",
            target=assignment.need,
            metadata={"assignment_id": assignment.pk, "role": assignment.role},
        )
    return assignment


def responsible_for(need: CompanyNeed) -> list[dict]:
    """The named, live actors of a need — organisation or role, never an e-mail address."""
    return [
        {
            "name": row.display_name,
            "role_label": row.get_role_display(),
            "authorisation": row.authorisation_reference,
            "valid_until": row.authorisation_valid_until,
            "is_authorised_actor": row.role == ActorRole.AUTHORISED_ACTOR,
        }
        for row in need.assignments.all()
        if row.is_live
    ]


# ---------------------------------------------------------------------------------------------
# The next action — one priority, never a list of five
# ---------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class NextAction:
    """Shape compatible with ``portal/partials/next_action.html``, which the shell renders."""

    label: str
    url: str = ""
    detail: str = ""
    urgency: str = "normal"  # normal | soon | overdue | blocked
    responsible_actor: str = ""
    cta_label: str = ""

    @property
    def is_for_someone_else(self) -> bool:
        return self.responsible_actor not in ("", "company")

    def get_responsible_display(self) -> str:
        return {
            "project_team": str(_("L’équipe du projet")),
            "authorised_actor": str(_("Le soggetto autorizzato / acteur autorisé")),
        }.get(self.responsible_actor, self.responsible_actor)


def next_action(company: CompanyProfile | None, needs=None) -> NextAction | None:
    """
    The single thing this company should do next. One priority, in the order that matters.

    It is allowed to answer « nothing, and here is who it depends on »: a company waiting for its own
    verification is not late, and telling it otherwise would be a small lie that wastes its time.
    """
    if company is None:
        return NextAction(
            label=str(_("Déclarez votre entreprise pour ouvrir votre espace")),
            url=safe_reverse("companies:profile_create"),
            detail=str(_("L’équipe vérifie ensuite l’entreprise avant toute transmission de besoin.")),
            responsible_actor="company",
            cta_label=str(_("Déclarer mon entreprise")),
        )
    rows = list(needs if needs is not None else needs_of(company))
    if not company.is_verified:
        return NextAction(
            label=str(_("Votre entreprise est en cours de vérification")),
            detail=str(
                _(
                    "Vous pouvez préparer vos besoins dès maintenant ; leur transmission sera possible "
                    "une fois la vérification prononcée."
                )
            ),
            urgency="blocked",
            responsible_actor="project_team",
        )
    drafts = [row for row in rows if row.status == NeedStatus.DRAFT]
    incomplete = [row for row in drafts if not row.is_complete]
    if incomplete:
        need = incomplete[0]
        return NextAction(
            label=gettext("Complétez le besoin « %(title)s »") % {"title": need.title},
            url=safe_reverse("companies:need_edit", need.reference),
            detail=gettext("Il manque %(items)s.") % {"items": ", ".join(need.missing_for_submission())},
            urgency="soon",
            responsible_actor="company",
            cta_label=str(_("Compléter le besoin")),
        )
    if drafts:
        need = drafts[0]
        return NextAction(
            label=gettext("Transmettez le besoin « %(title)s » au projet") % {"title": need.title},
            url=safe_reverse("companies:need_detail", need.reference),
            detail=str(_("Le besoin est complet : il peut être transmis pour examen.")),
            responsible_actor="company",
            cta_label=str(_("Ouvrir le besoin")),
        )
    waiting = [row for row in rows if row.status in {NeedStatus.SUBMITTED, NeedStatus.UNDER_REVIEW}]
    if waiting:
        return NextAction(
            label=str(_("Vos besoins transmis sont en cours d’examen")),
            detail=str(_("Vous serez informé dès qu’un acteur responsable sera désigné.")),
            responsible_actor="project_team",
        )
    if not rows:
        return NextAction(
            label=str(_("Exprimez votre premier besoin en compétences")),
            url=safe_reverse("companies:need_create"),
            detail=str(_("Un besoin décrit un poste : territoire, métier, tâches, compétences, langue, calendrier.")),
            responsible_actor="company",
            cta_label=str(_("Créer un besoin")),
        )
    return None


# ---------------------------------------------------------------------------------------------
# Aggregation — counts only (REQ-B2B-05)
# ---------------------------------------------------------------------------------------------
def may_read_analysis(user) -> bool:
    return bool(getattr(user, "is_superuser", False)) or roles.has_role(user, *ANALYSIS_ROLES)


def needs_aggregate(user) -> dict:
    """
    Expressed needs counted by territory, by sector and by state.

    COUNTS ONLY: no company name, no need title, no identifier, nothing that could be turned back
    into a row. Drafts and withdrawn needs are excluded — a draft is a private working document and
    a withdrawn need is not a need.
    """
    if not may_read_analysis(user):
        raise PermissionDenied
    base = CompanyNeed.objects.aggregated()

    def _count(field: str, label_field: str) -> list[dict]:
        return [
            {
                "label": row[label_field] or str(_("Non précisé")),
                "needs": row["needs"],
                "headcount": row["headcount"] or 0,
            }
            for row in base.values(label_field)
            .annotate(needs=models.Count("id"), headcount=models.Sum("headcount"))
            .order_by("-needs", label_field)
        ]

    status_labels = dict(NeedStatus.choices)
    return {
        "total_needs": base.count(),
        "total_headcount": base.aggregate(total=models.Sum("headcount"))["total"] or 0,
        "by_territory": _count("territory", "territory__label_fr"),
        "by_sector": _count("sector", "sector__label_fr"),
        "by_status": [
            {"label": str(status_labels.get(row["status"], row["status"])), "needs": row["needs"]}
            for row in base.values("status").annotate(needs=models.Count("id")).order_by("-needs")
        ],
        "counted_states": [str(status_labels[state]) for state in NeedStatus.values if state in AGGREGATED_STATUSES],
    }


# ---------------------------------------------------------------------------------------------
# The workspace shell
# ---------------------------------------------------------------------------------------------
def navigation(user, active: str = "", company: CompanyProfile | None = None) -> list[dict]:
    """
    The company workspace navigation. A module a role cannot use is NOT shown merely because it
    exists in the code (PLATFORM_REQUIREMENTS_V2 §3).

    « Mes besoins » and « Mon entreprise » belong to an account that HAS a company: offered to one
    that has none they lead to the declaration form, so a project reader consulting the aggregate
    was being invited to declare an entreprise. The workspace root stays for an account that could
    still declare one — it is where the declaration is offered — and disappears for a project
    reader, who has nothing to do there.
    """
    is_project_reader = may_read_analysis(user)
    entries = []
    if company is not None or not is_project_reader:
        entries.append(("dashboard", _("Tableau de bord"), safe_reverse("companies:dashboard")))
    if company is not None:
        entries.append(("needs", _("Mes besoins"), safe_reverse("companies:needs")))
        entries.append(("profile", _("Mon entreprise"), safe_reverse("companies:profile")))
    if is_project_reader:
        entries.append(("analysis", _("Analyse territoriale"), safe_reverse("companies:analysis")))
    portal_messages = safe_reverse("portal:messages")
    if portal_messages:
        entries.append(("messages", _("Communications"), portal_messages))
    # The rail draws a glyph per entry and a title per group (rail_nav.html). The glyph is the icon
    # registry's (apps/core/icons.py COMPANY_NAV; design V5, V5.4 plan §1.7): one concept, one glyph —
    # the needs are a wrench, the analysis a map; `briefcase` and `map-pin` keep the meaning they have
    # everywhere else (the professional, a place). tests/frontend/test_icons.py holds every entry to it.
    group = str(_("Espace entreprise"))
    # The phone's bottom bar (CD §3.9): the four entries of the workspace, then «Menu».
    bottom = {"dashboard", "needs", "profile", "messages"}
    return [
        {
            "key": key,
            "label": label,
            "url": url,
            "current": key == active,
            "icon": icons.COMPANY_NAV[key],
            "group": group,
            "bottom": key in bottom,
        }
        for key, label, url in entries
        if url
    ]


def communications(user, limit: int = 5) -> list[dict]:
    """
    The account's own communications. Read through ``portal``'s own queryset, which filters by
    recipient — this app never widens it.
    """
    try:
        from portal.models import Message
    except ImportError:  # pragma: no cover - portal is always installed
        return []
    rows = []
    for message in Message.objects.inbox(user)[:limit]:
        rows.append(
            {
                "subject": message.subject,
                "date": message.created_at,
                "is_unread": not message.is_read,
                "url": safe_reverse("portal:message_detail", message.pk),
            }
        )
    return rows
