"""
Forum Permanent — the AUTHENTICATED governance module (docs/platform/FORUM_GOVERNANCE.md).

The public Forum app (``forum.models``) is the PROGRAMME: a date, a venue, a patronage, a
registration form, and after 2 October 2026 an archive. This module is the other half of the same
name: the cooperation workspace where members, commissions, tables, proposals, projects, milestones
and the annual report live. The two never merge — one is readable by anyone, the other is readable
by the people who hold a live mandate — and the bridge between them is a single nullable foreign
key from ``ForumEdition`` to the published ``ForumEvent``.

FORUM_GOVERNANCE §2 says the cycle IS the product: forum → priorities → commissions → tables →
proposals → projects → implementation → monitoring → annual report → the next forum. Four
invariants follow, and each is enforced here rather than drawn on a screen:

1. **A proposal moves only along declared edges.** ``ALLOWED_PROPOSAL_TRANSITIONS`` is the whole
   truth about the lifecycle; anything absent is refused by the domain, whatever entry point asked.

2. **A mandate is dated, and the date is checked when the row is READ.** ``CommissionMember`` has a
   validity window, and ``CommissionMemberQuerySet.live()`` is applied inside every ``readable_by``
   so a lapsed mandate stops listing commissions, tables, proposals and projects the moment it
   lapses — not at the next write. This mirrors ``cases.CaseAssignment.is_live`` deliberately: the
   case file learned the same lesson in its 20 September 2026 security review.

3. **A participant never reaches another participant's personal information.** FORUM_GOVERNANCE §5
   is explicit — «Il Forum non è una rubrica di contatti». ``ForumProfile`` therefore has no field
   for an e-mail address, a telephone number or a personal name: the data is not hidden by a
   template, it is not stored by the model, so no queryset, no serialiser and no future API can
   disclose it. What a member may learn about another member is the organisation they represent,
   their category and the interests they declared.

4. **The annual report is assembled, never typed.** ``forum.governance_services`` builds it from the
   edition, the commissions, the accepted proposals, the projects and the monitoring entries. A
   report that could be written by hand would say whatever its author wanted it to say.

Everything here sits behind the ``virtual_forum`` flag, which is CLOSED (gate G11): the views refuse
before they authenticate. The models are inert while the flag is shut — they simply hold no rows.

The five commissions of FORUM_GOVERNANCE §3 are SEED DATA, not constants in this file (REQ-CFG-03):
adding a sixth commission is a back-office operation, and nothing in this module enumerates them.
"""

from __future__ import annotations

import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.models import TimeStampedModel

# =================================================================================================
# Vocabulary
# =================================================================================================


class EditionStatus(models.TextChoices):
    """Where one annual cycle stands. A closed edition still feeds the next one through its report."""

    PLANNED = "planned", _("Programmée")
    OPEN = "open", _("En cours")
    CLOSED = "closed", _("Clôturée")
    ARCHIVED = "archived", _("Archivée")


class ParticipantCategory(models.TextChoices):
    """WHAT a participant is. Never who they are: the category is an attribute of the organisation."""

    INSTITUTION = "institution", _("Institution")
    ENTERPRISE = "enterprise", _("Entreprise")
    UNIVERSITY = "university", _("Université ou centre de recherche")
    TRAINING_BODY = "training_body", _("Organisme de formation")
    PROFESSIONAL = "professional", _("Professionnel du droit")
    ASSOCIATION = "association", _("Association ou chambre consulaire")
    OTHER = "other", _("Autre participant")


class ForumRole(models.TextChoices):
    """
    The four roles of FORUM_GOVERNANCE §5, held at the level of an EDITION.

    ``SECRETARIAT`` is the only role that reads an edition whole; it is deliberately a role on a
    profile and not a platform-wide group, because the secretariat of the Rovigo edition has no
    business reading the workspace of a later one.

    ``OBSERVER`` reads «secondo il perimetro dell'accordo», and that perimeter is not a sentence in
    a contract here: it is the set of commissions where the observer holds a live mandate. An
    observer with no mandate reads nothing, which is the correct reading of an agreement that has
    not yet named anything.
    """

    PARTICIPANT = "participant", _("Participant")
    SECRETARIAT = "secretariat", _("Secrétariat du Forum")
    OBSERVER = "observer", _("Observateur institutionnel")


class MandateRole(models.TextChoices):
    """The capacity in which a profile sits on ONE commission, for a bounded period."""

    MEMBER = "member", _("Membre")
    REFERENT = "referent", _("Référent")
    OBSERVER = "observer", _("Observateur")


class CommissionStatus(models.TextChoices):
    ACTIVE = "active", _("Active")
    DORMANT = "dormant", _("En veille")
    CLOSED = "closed", _("Clôturée")


class TableStatus(models.TextChoices):
    OPEN = "open", _("Ouvert")
    CONSOLIDATING = "consolidating", _("En consolidation")
    CLOSED = "closed", _("Clôturé")


class ProposalStatus(models.TextChoices):
    """The six states of FORUM_GOVERNANCE §4. The transition table below is the whole lifecycle."""

    DRAFT = "draft", _("Brouillon")
    SUBMITTED = "submitted", _("Déposée")
    UNDER_REVIEW = "under_review", _("En examen")
    ACCEPTED = "accepted", _("Retenue")
    REJECTED = "rejected", _("Écartée")
    WITHDRAWN = "withdrawn", _("Retirée")


#: States before any decision has been taken. WITHDRAWN is reachable from each of them and from
#: nowhere else: a proposal that has been decided is part of the record of the edition, and letting
#: its author withdraw it afterwards would rewrite what a commission actually resolved.
PRE_DECISION_PROPOSAL_STATUSES: frozenset[str] = frozenset(
    {ProposalStatus.DRAFT, ProposalStatus.SUBMITTED, ProposalStatus.UNDER_REVIEW}
)

#: Declared transitions (FORUM_GOVERNANCE §4). Anything absent here is refused by the domain.
#: WITHDRAWN is added programmatically by ``proposal_transitions_from`` for the pre-decision states.
ALLOWED_PROPOSAL_TRANSITIONS: dict[str, frozenset[str]] = {
    ProposalStatus.DRAFT: frozenset({ProposalStatus.SUBMITTED}),
    ProposalStatus.SUBMITTED: frozenset({ProposalStatus.UNDER_REVIEW}),
    ProposalStatus.UNDER_REVIEW: frozenset({ProposalStatus.ACCEPTED, ProposalStatus.REJECTED}),
    ProposalStatus.ACCEPTED: frozenset(),
    ProposalStatus.REJECTED: frozenset(),
    ProposalStatus.WITHDRAWN: frozenset(),
}

#: Decisions a commission takes. Both require a written motivation, so that «écartée» is never a
#: verdict without a reason a proposer can read.
DECISION_PROPOSAL_STATUSES: frozenset[str] = frozenset({ProposalStatus.ACCEPTED, ProposalStatus.REJECTED})


def proposal_transitions_from(status: str) -> frozenset[str]:
    """Every state reachable from ``status``, including the WITHDRAWN exit of the open states."""
    declared = ALLOWED_PROPOSAL_TRANSITIONS.get(status, frozenset())
    if status in PRE_DECISION_PROPOSAL_STATUSES:
        return declared | {ProposalStatus.WITHDRAWN}
    return declared


class ProjectStatus(models.TextChoices):
    """A project exists only because a proposal was accepted; it never starts from nothing."""

    PREPARATION = "preparation", _("En préparation")
    ACTIVE = "active", _("En cours")
    SUSPENDED = "suspended", _("Suspendu")
    COMPLETED = "completed", _("Achevé")
    DISCONTINUED = "discontinued", _("Interrompu")


#: Declared transitions of a project. A suspension returns to the state it came from, which is why
#: ``previous_status`` is recorded rather than guessed.
ALLOWED_PROJECT_TRANSITIONS: dict[str, frozenset[str]] = {
    ProjectStatus.PREPARATION: frozenset({ProjectStatus.ACTIVE, ProjectStatus.SUSPENDED, ProjectStatus.DISCONTINUED}),
    ProjectStatus.ACTIVE: frozenset({ProjectStatus.SUSPENDED, ProjectStatus.COMPLETED, ProjectStatus.DISCONTINUED}),
    ProjectStatus.SUSPENDED: frozenset(
        {ProjectStatus.PREPARATION, ProjectStatus.ACTIVE, ProjectStatus.DISCONTINUED}
    ),
    ProjectStatus.COMPLETED: frozenset(),
    ProjectStatus.DISCONTINUED: frozenset(),
}


def project_transitions_from(status: str) -> frozenset[str]:
    return ALLOWED_PROJECT_TRANSITIONS.get(status, frozenset())


class MilestoneStatus(models.TextChoices):
    PENDING = "pending", _("À faire")
    IN_PROGRESS = "in_progress", _("En cours")
    DONE = "done", _("Réalisée")
    BLOCKED = "blocked", _("Bloquée")
    NOT_APPLICABLE = "not_applicable", _("Sans objet")


#: Milestones that still count in the denominator of « n réalisées sur m ».
OPEN_MILESTONE_STATUSES: frozenset[str] = frozenset(
    {MilestoneStatus.PENDING, MilestoneStatus.IN_PROGRESS, MilestoneStatus.BLOCKED}
)


class ReportStatus(models.TextChoices):
    DRAFT = "draft", _("Projet")
    PUBLISHED = "published", _("Publiée")


#: The design system draws a state as a WORD plus a 2px rule, and it ships exactly eight modifiers
#: (``static/css/register.css``: missing, filed, review, valid, done, invalid, expired, replace).
#: These maps say which existing modifier each domain state borrows, so a template never has to
#: invent a class and the stylesheet never has to grow one. Colour only ever repeats the word.
PROPOSAL_STATE_CLASSES: dict[str, str] = {
    ProposalStatus.DRAFT: "missing",
    ProposalStatus.SUBMITTED: "filed",
    ProposalStatus.UNDER_REVIEW: "review",
    ProposalStatus.ACCEPTED: "done",
    ProposalStatus.REJECTED: "invalid",
    ProposalStatus.WITHDRAWN: "expired",
}
PROJECT_STATE_CLASSES: dict[str, str] = {
    ProjectStatus.PREPARATION: "filed",
    ProjectStatus.ACTIVE: "review",
    ProjectStatus.SUSPENDED: "replace",
    ProjectStatus.COMPLETED: "done",
    ProjectStatus.DISCONTINUED: "expired",
}
MILESTONE_STATE_CLASSES: dict[str, str] = {
    MilestoneStatus.PENDING: "missing",
    MilestoneStatus.IN_PROGRESS: "review",
    MilestoneStatus.DONE: "done",
    MilestoneStatus.BLOCKED: "invalid",
    MilestoneStatus.NOT_APPLICABLE: "expired",
}
COMMISSION_STATE_CLASSES: dict[str, str] = {
    CommissionStatus.ACTIVE: "valid",
    CommissionStatus.DORMANT: "replace",
    CommissionStatus.CLOSED: "expired",
}
TABLE_STATE_CLASSES: dict[str, str] = {
    TableStatus.OPEN: "valid",
    TableStatus.CONSOLIDATING: "review",
    TableStatus.CLOSED: "expired",
}
EDITION_STATE_CLASSES: dict[str, str] = {
    EditionStatus.PLANNED: "filed",
    EditionStatus.OPEN: "valid",
    EditionStatus.CLOSED: "done",
    EditionStatus.ARCHIVED: "expired",
}


# =================================================================================================
# Authorisation helpers — the SAME subqueries feed every ``readable_by``
# =================================================================================================
def _is_unrestricted(user) -> bool:
    """
    Accounts that read the whole module.

    Deliberately narrow: ``role:administrator`` and a superuser, and nothing else. ``role:staff`` is
    absent for the reason the case file records — a standing ability to read every workspace is a
    disclosure, not supervision — and the Forum's own supervision role is ``ForumRole.SECRETARIAT``,
    which is bounded by an edition and by a profile that can be deactivated.
    """
    from accounts import roles

    return bool(getattr(user, "is_superuser", False)) or roles.has_role(user, roles.ADMINISTRATOR)


def _own_profiles(user):
    """The caller's ACTIVE participation profiles. A deactivated profile grants nothing."""
    return ForumProfile.objects.filter(user=user, is_active=True)


def _secretariat_edition_ids(user):
    return _own_profiles(user).filter(role=ForumRole.SECRETARIAT).values("edition_id")


def _mandated_commission_ids(user, at=None):
    """Commissions where the caller holds a LIVE mandate — evaluated at read time, every time."""
    return CommissionMember.objects.live(at).filter(profile__in=_own_profiles(user)).values("commission_id")


def _readable_commission_ids(user, at=None):
    """
    The commission perimeter of ``user``, as a QUERY rather than a Python list.

    Keeping it a queryset is what lets the authorisation live inside the filter of every other
    model: a row the caller may not see never reaches the process, so it cannot leak through a
    count, an autocomplete or a differently worded « not found ».
    """
    return Commission.objects.filter(
        models.Q(edition__in=_secretariat_edition_ids(user)) | models.Q(pk__in=_mandated_commission_ids(user, at))
    ).values("pk")


# =================================================================================================
# Edition
# =================================================================================================
class ForumEditionQuerySet(models.QuerySet):
    def readable_by(self, user) -> ForumEditionQuerySet:
        if not getattr(user, "is_authenticated", False):
            return self.none()
        if _is_unrestricted(user):
            return self
        return self.filter(pk__in=_own_profiles(user).values("edition_id")).distinct()


class ForumEdition(TimeStampedModel):
    """
    One annual cycle of the Forum Permanent. The first is Rovigo 2026 (FORUM_GOVERNANCE §1).

    An edition is not an event: the event is the two hours in the Sala della Gran Guardia, the
    edition is the year of work the event opens. ``event`` links the two when a published page
    exists, and stays null for an edition that has not been announced.
    """

    key = models.SlugField(_("clé"), max_length=64, unique=True)
    year = models.PositiveSmallIntegerField(_("année"))
    title_fr = models.CharField(_("intitulé (FR)"), max_length=200)
    city = models.CharField(_("ville"), max_length=120, blank=True)
    country_code = models.CharField(_("pays (ISO)"), max_length=2, blank=True)
    starts_on = models.DateField(_("ouverture"), null=True, blank=True)
    ends_on = models.DateField(_("clôture"), null=True, blank=True)
    status = models.CharField(
        _("état"), max_length=12, choices=EditionStatus.choices, default=EditionStatus.PLANNED, db_index=True
    )
    event = models.ForeignKey(
        "forum.ForumEvent",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="governance_editions",
        verbose_name=_("page publique de l’édition"),
        help_text=_("Édition publiée sur /forum/, lorsqu’elle existe. Une édition peut exister sans page."),
    )

    class Meta:
        verbose_name = _("édition du Forum permanent")
        verbose_name_plural = _("éditions du Forum permanent")
        ordering = ["-year", "key"]
        indexes = [models.Index(fields=["status", "year"])]

    objects = ForumEditionQuerySet.as_manager()

    def __str__(self) -> str:
        return f"{self.title_fr} ({self.year})"

    def clean(self) -> None:
        if self.starts_on and self.ends_on and self.ends_on < self.starts_on:
            raise ValidationError({"ends_on": _("La clôture ne peut pas précéder l’ouverture.")})

    @property
    def is_open(self) -> bool:
        return self.status == EditionStatus.OPEN

    @property
    def state_class(self) -> str:
        return EDITION_STATE_CLASSES.get(self.status, "filed")


# =================================================================================================
# Participation profile
# =================================================================================================
#: What one participant may learn about another. The list is short on purpose and it is the whole
#: list: ``governance_services.public_profile`` returns these keys and the templates render nothing
#: else. See ``apps/forum/tests/test_governance_privacy.py``.
PUBLIC_PROFILE_KEYS: tuple[str, ...] = ("organisation", "category", "interests")

#: Field names this model must never acquire. The test that enforces it reads this tuple, so adding
#: a telephone number to a participation profile breaks the build rather than the promise.
FORBIDDEN_PROFILE_FIELDS: tuple[str, ...] = (
    "email",
    "e_mail",
    "mail",
    "phone",
    "telephone",
    "mobile",
    "first_name",
    "last_name",
    "full_name",
    "person_name",
    "address",
    "birth_date",
)


class ForumProfileQuerySet(models.QuerySet):
    def active(self) -> ForumProfileQuerySet:
        return self.filter(is_active=True)

    def readable_by(self, user) -> ForumProfileQuerySet:
        """
        Own profiles, the profiles that sit on a commission with the caller, and — for the
        secretariat — the profiles of its own edition.

        « Sit on a commission with the caller » is checked on both sides with a LIVE mandate: a
        member whose mandate expired last week is no longer listed, and neither is a commission the
        caller left. A membership list that outlives the mandate is a contact directory, and
        FORUM_GOVERNANCE §5 says this is not one.
        """
        if not getattr(user, "is_authenticated", False):
            return self.none()
        if _is_unrestricted(user):
            return self
        shared = CommissionMember.objects.live().filter(commission__in=_mandated_commission_ids(user))
        return self.filter(
            models.Q(user=user)
            | models.Q(edition__in=_secretariat_edition_ids(user))
            | models.Q(pk__in=shared.values("profile_id"))
        ).distinct()


class ForumProfile(TimeStampedModel):
    """
    How one account takes part in one edition — and the model that carries the §5 constraint.

    There is no name here, no e-mail address and no telephone number. That is not an omission to be
    corrected later: the account already holds those, ``accounts.User`` is where they belong, and
    this row exists precisely so that the cooperation workspace can name a participant WITHOUT
    reaching them. ``__str__`` is written the same way, because the audit trail records
    ``str(target)`` and an audit row is read by people who are not members of the commission.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="forum_profiles",
        verbose_name=_("compte"),
    )
    edition = models.ForeignKey(
        ForumEdition, on_delete=models.CASCADE, related_name="profiles", verbose_name=_("édition")
    )
    organisation = models.ForeignKey(
        "accounts.Organisation",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="forum_profiles",
        verbose_name=_("organisation"),
    )
    organisation_label = models.CharField(
        _("organisation représentée"),
        max_length=200,
        blank=True,
        help_text=_("Dénomination publiée dans le Forum. À défaut, celle de l’organisation liée."),
    )
    category = models.CharField(
        _("catégorie"), max_length=20, choices=ParticipantCategory.choices, default=ParticipantCategory.OTHER
    )
    role = models.CharField(
        _("rôle dans le Forum"), max_length=16, choices=ForumRole.choices, default=ForumRole.PARTICIPANT
    )
    declared_interests = models.TextField(
        _("intérêts déclarés"),
        blank=True,
        help_text=_("Thèmes de coopération que le participant souhaite suivre. Jamais de données personnelles."),
    )
    joined_on = models.DateField(_("membre depuis"), default=timezone.localdate)
    is_active = models.BooleanField(_("profil actif"), default=True)

    class Meta:
        verbose_name = _("profil de participation")
        verbose_name_plural = _("profils de participation")
        ordering = ["organisation_label", "id"]
        constraints = [models.UniqueConstraint(fields=["user", "edition"], name="uniq_forum_profile_user_edition")]
        indexes = [models.Index(fields=["edition", "role"])]

    objects = ForumProfileQuerySet.as_manager()

    def __str__(self) -> str:
        # NEVER the account's e-mail: this string is copied into the audit trail.
        return f"{self.display_label} · {self.get_category_display()}"

    @property
    def display_label(self) -> str:
        """The organisation, or an honest placeholder. Never a person's name, never an address."""
        if self.organisation_label.strip():
            return self.organisation_label.strip()
        if self.organisation_id and self.organisation is not None:
            return self.organisation.name
        return str(_("Participant sans organisation déclarée"))

    @property
    def is_secretariat(self) -> bool:
        return self.is_active and self.role == ForumRole.SECRETARIAT

    def live_mandates(self, at=None):
        return self.mandates.live(at).select_related("commission")


# =================================================================================================
# Commissions and their dated mandates
# =================================================================================================
class CommissionQuerySet(models.QuerySet):
    def readable_by(self, user) -> CommissionQuerySet:
        if not getattr(user, "is_authenticated", False):
            return self.none()
        if _is_unrestricted(user):
            return self
        return self.filter(
            models.Q(edition__in=_secretariat_edition_ids(user)) | models.Q(pk__in=_mandated_commission_ids(user))
        ).distinct()


class Commission(TimeStampedModel):
    """
    A mixed commission: one priority of the edition, entrusted to a standing working body.

    REQ-CFG-03 — the five commissions of FORUM_GOVERNANCE §3 are seed data. Nothing in this module
    enumerates them, nothing branches on their keys, and adding a sixth is a back-office operation.
    """

    edition = models.ForeignKey(
        ForumEdition, on_delete=models.CASCADE, related_name="commissions", verbose_name=_("édition")
    )
    key = models.SlugField(_("clé"), max_length=64)
    name_fr = models.CharField(_("intitulé (FR)"), max_length=200)
    scope_fr = models.TextField(_("champ (FR)"), blank=True)
    governance_fr = models.TextField(
        _("gouvernance (FR)"),
        blank=True,
        help_text=_("Composition, présidence, rythme des réunions. Jamais de noms de personnes physiques."),
    )
    status = models.CharField(
        _("état"), max_length=10, choices=CommissionStatus.choices, default=CommissionStatus.ACTIVE, db_index=True
    )
    order = models.PositiveSmallIntegerField(_("ordre"), default=0)

    class Meta:
        verbose_name = _("commission mixte")
        verbose_name_plural = _("commissions mixtes")
        ordering = ["edition", "order", "key"]
        constraints = [models.UniqueConstraint(fields=["edition", "key"], name="uniq_forum_commission_key")]

    objects = CommissionQuerySet.as_manager()

    def __str__(self) -> str:
        return self.name_fr

    def live_members(self, at=None):
        return self.members.live(at).select_related("profile", "profile__organisation")

    @property
    def state_class(self) -> str:
        return COMMISSION_STATE_CLASSES.get(self.status, "filed")


class CommissionMemberQuerySet(models.QuerySet):
    def live(self, at=None) -> CommissionMemberQuerySet:
        """
        Mandates in force on ``at`` (today by default).

        This is the read-time half of the dated mandate, and it is the half that matters. Checking
        the window only when a mandate is written means an expired mandate keeps opening commissions,
        tables, proposals and projects until somebody notices — which is precisely the boundary a
        dated authorisation exists to draw.
        """
        today = at or timezone.localdate()
        return self.filter(revoked_at__isnull=True, valid_from__lte=today).filter(
            models.Q(valid_until__isnull=True) | models.Q(valid_until__gte=today)
        )

    def readable_by(self, user) -> CommissionMemberQuerySet:
        """
        Mandates inside a readable commission — PLUS the caller's own, live or not.

        Reading your own lapsed mandate is not a disclosure, it is the answer to « why can I no
        longer open this commission », and « Ma participation » shows exactly that. The policy in
        ``forum.governance_policies`` says the same thing, and a test runs both to make sure they
        keep saying it.
        """
        if not getattr(user, "is_authenticated", False):
            return self.none()
        if _is_unrestricted(user):
            return self
        return self.filter(
            models.Q(profile__user=user) | models.Q(commission__in=_readable_commission_ids(user))
        ).distinct()


class CommissionMember(TimeStampedModel):
    """
    A mandate: WHO sits on WHICH commission, in WHAT capacity, FROM when TO when.

    ``is_live`` and ``CommissionMemberQuerySet.live()`` must always answer the same question the
    same way — one for a row in hand, one for a filter — and a test asserts that they do.
    """

    commission = models.ForeignKey(
        Commission, on_delete=models.CASCADE, related_name="members", verbose_name=_("commission")
    )
    profile = models.ForeignKey(
        ForumProfile, on_delete=models.CASCADE, related_name="mandates", verbose_name=_("profil")
    )
    role = models.CharField(_("qualité"), max_length=10, choices=MandateRole.choices, default=MandateRole.MEMBER)
    mandate_reference = models.CharField(
        _("référence du mandat"),
        max_length=200,
        blank=True,
        help_text=_("Acte de désignation : délibération, lettre de mission, accord de coopération."),
    )
    valid_from = models.DateField(_("mandat à compter du"), default=timezone.localdate)
    valid_until = models.DateField(
        _("mandat jusqu’au"),
        null=True,
        blank=True,
        help_text=_("Vide = sans échéance. Un mandat échu ne donne plus aucun accès, dès le lendemain."),
    )
    revoked_at = models.DateTimeField(_("révoqué le"), null=True, blank=True)

    class Meta:
        verbose_name = _("mandat en commission")
        verbose_name_plural = _("mandats en commission")
        ordering = ["commission", "-valid_from", "id"]
        indexes = [
            models.Index(fields=["commission", "revoked_at"]),
            models.Index(fields=["profile", "valid_until"]),
        ]

    objects = CommissionMemberQuerySet.as_manager()

    def __str__(self) -> str:
        return f"{self.get_role_display()} · {self.commission.name_fr}"

    @property
    def is_live(self) -> bool:
        if self.revoked_at is not None:
            return False
        today = timezone.localdate()
        if self.valid_from and self.valid_from > today:
            return False
        return not (self.valid_until and self.valid_until < today)

    def clean(self) -> None:
        if self.valid_until and self.valid_from and self.valid_until < self.valid_from:
            raise ValidationError({"valid_until": _("La fin du mandat ne peut pas précéder son début.")})
        if self.profile_id and self.commission_id and self.profile.edition_id != self.commission.edition_id:
            raise ValidationError(
                {"profile": _("Le profil et la commission doivent appartenir à la même édition du Forum.")}
            )


# =================================================================================================
# Digital tables
# =================================================================================================
class TableQuerySet(models.QuerySet):
    def readable_by(self, user) -> TableQuerySet:
        if not getattr(user, "is_authenticated", False):
            return self.none()
        if _is_unrestricted(user):
            return self
        return self.filter(commission__in=_readable_commission_ids(user)).distinct()


class Table(TimeStampedModel):
    """
    A digital table: the place inside a commission where proposals are worked on.

    ``referent`` points at a MANDATE rather than at a profile, so «qui modère cette table» and
    «jusqu'à quand» are the same fact. A referent whose mandate lapses stops being displayed as the
    referent, because the mandate is what made them one.
    """

    commission = models.ForeignKey(
        Commission, on_delete=models.CASCADE, related_name="tables", verbose_name=_("commission")
    )
    key = models.SlugField(_("clé"), max_length=64)
    title_fr = models.CharField(_("intitulé (FR)"), max_length=200)
    topic_fr = models.TextField(_("thème (FR)"), blank=True)
    status = models.CharField(
        _("état"), max_length=14, choices=TableStatus.choices, default=TableStatus.OPEN, db_index=True
    )
    referent = models.ForeignKey(
        CommissionMember,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tables_led",
        verbose_name=_("référent"),
    )
    opened_on = models.DateField(_("ouvert le"), default=timezone.localdate)
    closed_on = models.DateField(_("clôturé le"), null=True, blank=True)

    class Meta:
        verbose_name = _("table thématique")
        verbose_name_plural = _("tables thématiques")
        ordering = ["commission", "title_fr"]
        constraints = [models.UniqueConstraint(fields=["commission", "key"], name="uniq_forum_table_key")]

    objects = TableQuerySet.as_manager()

    def __str__(self) -> str:
        return self.title_fr

    def clean(self) -> None:
        if self.referent_id and self.referent is not None and self.referent.commission_id != self.commission_id:
            raise ValidationError({"referent": _("Le référent doit détenir un mandat dans cette commission.")})

    @property
    def live_referent(self) -> CommissionMember | None:
        """The referent, only while their mandate is in force. Otherwise the table has none."""
        if self.referent_id and self.referent is not None and self.referent.is_live:
            return self.referent
        return None

    @property
    def is_open(self) -> bool:
        return self.status in {TableStatus.OPEN, TableStatus.CONSOLIDATING}

    @property
    def state_class(self) -> str:
        return TABLE_STATE_CLASSES.get(self.status, "filed")


# =================================================================================================
# Proposals
# =================================================================================================
class ForumProposalQuerySet(models.QuerySet):
    def readable_by(self, user) -> ForumProposalQuerySet:
        """
        Own proposals always; other people's only once they have left the drafting stage.

        A DRAFT belongs to the person writing it. Showing an unfinished proposal to the rest of the
        commission would make the drafting stage useless and would put half-formed positions of one
        organisation in front of another — which is a different product from the one §2 describes.
        """
        if not getattr(user, "is_authenticated", False):
            return self.none()
        if _is_unrestricted(user):
            return self
        shared = models.Q(commission__in=_readable_commission_ids(user)) & ~models.Q(status=ProposalStatus.DRAFT)
        return self.filter(models.Q(proposer__user=user) | shared).distinct()

    def decided(self) -> ForumProposalQuerySet:
        return self.filter(status__in=DECISION_PROPOSAL_STATUSES)

    def accepted(self) -> ForumProposalQuerySet:
        return self.filter(status=ProposalStatus.ACCEPTED)


class ForumProposal(TimeStampedModel):
    """
    A proposal elaborated at a table and decided by its commission.

    The state is NEVER written from a view. ``governance_services.transition_proposal`` is the only
    door: it checks the declared table, refuses out loud rather than no-opping, and writes an
    ``AuditEvent``. A refusal that returns silently leaves the interface showing a state the domain
    never reached, which is worse than an error because it looks like success.
    """

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    reference = models.CharField(_("référence"), max_length=16, unique=True, editable=False)
    proposer = models.ForeignKey(
        ForumProfile, on_delete=models.PROTECT, related_name="proposals", verbose_name=_("proposant")
    )
    commission = models.ForeignKey(
        Commission, on_delete=models.CASCADE, related_name="proposals", verbose_name=_("commission")
    )
    table = models.ForeignKey(
        Table,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="proposals",
        verbose_name=_("table"),
    )
    title_fr = models.CharField(_("intitulé (FR)"), max_length=200)
    body_fr = models.TextField(_("texte (FR)"))
    status = models.CharField(
        _("état"), max_length=14, choices=ProposalStatus.choices, default=ProposalStatus.DRAFT, db_index=True
    )
    status_since = models.DateTimeField(_("dans cet état depuis"), default=timezone.now, editable=False)
    previous_status = models.CharField(
        _("état précédent"), max_length=14, choices=ProposalStatus.choices, blank=True, editable=False
    )
    decision_note_fr = models.TextField(
        _("motivation de la décision (FR)"),
        blank=True,
        help_text=_("Obligatoire pour retenir ou écarter une proposition : une décision sans motif n’en est pas une."),
    )
    decided_at = models.DateTimeField(_("décidée le"), null=True, blank=True, editable=False)

    class Meta:
        verbose_name = _("proposition")
        verbose_name_plural = _("propositions")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["commission", "status"]),
            models.Index(fields=["status", "status_since"]),
        ]

    objects = ForumProposalQuerySet.as_manager()

    def __str__(self) -> str:
        return f"{self.reference} · {self.title_fr}"

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = self._new_reference()
        super().save(*args, **kwargs)

    @staticmethod
    def _new_reference() -> str:
        """Short and non-sequential: a running number would publish how many proposals exist."""
        for _attempt in range(12):
            candidate = "P" + uuid.uuid4().hex[:9].upper()
            if not ForumProposal.objects.filter(reference=candidate).exists():
                return candidate
        raise RuntimeError("could not allocate a unique proposal reference")

    def allowed_transitions(self) -> frozenset[str]:
        return proposal_transitions_from(self.status)

    def can_transition_to(self, target: str) -> bool:
        return target in self.allowed_transitions()

    @property
    def is_decided(self) -> bool:
        return self.status in DECISION_PROPOSAL_STATUSES

    @property
    def is_editable(self) -> bool:
        return self.status == ProposalStatus.DRAFT

    @property
    def state_class(self) -> str:
        return PROPOSAL_STATE_CLASSES.get(self.status, "filed")

    def clean(self) -> None:
        if self.table_id and self.table is not None and self.table.commission_id != self.commission_id:
            raise ValidationError({"table": _("La table choisie n’appartient pas à cette commission.")})
        if self.proposer_id and self.commission_id and self.proposer.edition_id != self.commission.edition_id:
            raise ValidationError({"commission": _("La commission relève d’une autre édition que le proposant.")})


# =================================================================================================
# Projects, milestones, monitoring
# =================================================================================================
class ForumProjectQuerySet(models.QuerySet):
    def readable_by(self, user) -> ForumProjectQuerySet:
        if not getattr(user, "is_authenticated", False):
            return self.none()
        if _is_unrestricted(user):
            return self
        return self.filter(commission__in=_readable_commission_ids(user)).distinct()

    def running(self) -> ForumProjectQuerySet:
        return self.filter(status__in=[ProjectStatus.PREPARATION, ProjectStatus.ACTIVE])


class ForumProject(TimeStampedModel):
    """
    What an accepted proposal became. ``origin`` is not optional and never null: FORUM_GOVERNANCE §2
    says a proposal that cannot become a project is a discussion table, and a project with no origin
    is a project nobody proposed.
    """

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    origin = models.OneToOneField(
        ForumProposal, on_delete=models.PROTECT, related_name="project", verbose_name=_("proposition d’origine")
    )
    commission = models.ForeignKey(
        Commission, on_delete=models.CASCADE, related_name="projects", verbose_name=_("commission")
    )
    title_fr = models.CharField(_("intitulé (FR)"), max_length=200)
    summary_fr = models.TextField(_("objet (FR)"), blank=True)
    lead = models.ForeignKey(
        ForumProfile,
        on_delete=models.PROTECT,
        related_name="projects_led",
        verbose_name=_("responsable"),
        help_text=_("Organisation responsable de la mise en œuvre. « Qui est responsable » est obligatoire."),
    )
    partners_fr = models.TextField(
        _("partenaires (FR)"),
        blank=True,
        help_text=_("Organisations associées, une par ligne. Jamais de personnes physiques."),
    )
    status = models.CharField(
        _("état"), max_length=14, choices=ProjectStatus.choices, default=ProjectStatus.PREPARATION, db_index=True
    )
    status_since = models.DateTimeField(_("dans cet état depuis"), default=timezone.now, editable=False)
    previous_status = models.CharField(
        _("état précédent"), max_length=14, choices=ProjectStatus.choices, blank=True, editable=False
    )
    started_on = models.DateField(_("démarrage"), null=True, blank=True)
    ends_on = models.DateField(_("échéance"), null=True, blank=True)

    class Meta:
        verbose_name = _("projet du Forum")
        verbose_name_plural = _("projets du Forum")
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["commission", "status"])]

    objects = ForumProjectQuerySet.as_manager()

    def __str__(self) -> str:
        return self.title_fr

    def allowed_transitions(self) -> frozenset[str]:
        return project_transitions_from(self.status)

    def can_transition_to(self, target: str) -> bool:
        return target in self.allowed_transitions()

    @property
    def partner_lines(self) -> list[str]:
        return [line.strip() for line in self.partners_fr.splitlines() if line.strip()]

    @property
    def state_class(self) -> str:
        return PROJECT_STATE_CLASSES.get(self.status, "filed")

    def milestone_counts(self) -> dict[str, int]:
        """Counts, never a percentage: « 4 jalons réalisés sur 11 » is verifiable, « 62 % » is not."""
        rows = list(self.milestones.all())
        applicable = [row for row in rows if row.status != MilestoneStatus.NOT_APPLICABLE]
        done = [row for row in applicable if row.status == MilestoneStatus.DONE]
        return {
            "total": len(applicable),
            "done": len(done),
            "open": len(applicable) - len(done),
            "overdue": len([row for row in applicable if row.is_overdue]),
        }


class ProjectMilestone(TimeStampedModel):
    """A dated step of a project, with the party answerable for it. Never anonymous."""

    project = models.ForeignKey(
        ForumProject, on_delete=models.CASCADE, related_name="milestones", verbose_name=_("projet")
    )
    order = models.PositiveSmallIntegerField(_("ordre"), default=0)
    title_fr = models.CharField(_("intitulé (FR)"), max_length=200)
    detail_fr = models.TextField(_("précisions (FR)"), blank=True)
    due_on = models.DateField(_("échéance"), null=True, blank=True)
    status = models.CharField(
        _("état"), max_length=16, choices=MilestoneStatus.choices, default=MilestoneStatus.PENDING, db_index=True
    )
    responsible = models.ForeignKey(
        ForumProfile,
        on_delete=models.PROTECT,
        related_name="milestones",
        verbose_name=_("responsable"),
    )
    responsible_note = models.CharField(
        _("précision sur le responsable"),
        max_length=200,
        blank=True,
        help_text=_("Par exemple la direction concernée, sans jamais nommer une personne physique."),
    )

    class Meta:
        verbose_name = _("jalon")
        verbose_name_plural = _("jalons")
        ordering = ["project", "order", "id"]
        indexes = [models.Index(fields=["project", "status"])]

    def __str__(self) -> str:
        return self.title_fr

    @property
    def is_open(self) -> bool:
        return self.status in OPEN_MILESTONE_STATUSES

    @property
    def is_overdue(self) -> bool:
        return bool(self.due_on and self.is_open and self.due_on < timezone.localdate())

    @property
    def state_class(self) -> str:
        return MILESTONE_STATE_CLASSES.get(self.status, "missing")


class MonitoringEntry(TimeStampedModel):
    """
    One monitoring period of one project. ``indicators`` is a flat mapping of declared measures.

    Nothing computes a score out of it. The annual report adds up what the commissions recorded and
    says which period it covers; it never invents an index, because an index nobody defined is a
    judgement dressed as a number.
    """

    project = models.ForeignKey(
        ForumProject, on_delete=models.CASCADE, related_name="monitoring", verbose_name=_("projet")
    )
    period_start = models.DateField(_("période du"))
    period_end = models.DateField(_("période au"))
    indicators = models.JSONField(
        _("indicateurs"),
        default=dict,
        blank=True,
        help_text=_("Mesures déclarées par la commission : {clé: valeur}. Aucune donnée personnelle."),
    )
    note_fr = models.TextField(_("observations (FR)"), blank=True)
    recorded_by = models.ForeignKey(
        ForumProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="monitoring_entries",
        verbose_name=_("consigné par"),
    )

    class Meta:
        verbose_name = _("relevé de suivi")
        verbose_name_plural = _("relevés de suivi")
        ordering = ["-period_end", "id"]
        indexes = [models.Index(fields=["project", "period_end"])]

    def __str__(self) -> str:
        return f"{self.project.title_fr} · {self.period_start:%d.%m.%Y}–{self.period_end:%d.%m.%Y}"

    def clean(self) -> None:
        if self.period_start and self.period_end and self.period_end < self.period_start:
            raise ValidationError({"period_end": _("La fin de la période ne peut pas précéder son début.")})
        if self.indicators and not isinstance(self.indicators, dict):
            raise ValidationError({"indicators": _("Les indicateurs doivent être un objet {clé: valeur}.")})


# =================================================================================================
# Annual report
# =================================================================================================
class AnnualReportQuerySet(models.QuerySet):
    def readable_by(self, user) -> AnnualReportQuerySet:
        """
        A published report is readable by everyone who takes part in the edition; a draft is not.

        The secretariat is the only role that reads a report before it is published, because until
        then it is a working document that still changes every time it is regenerated.
        """
        if not getattr(user, "is_authenticated", False):
            return self.none()
        if _is_unrestricted(user):
            return self
        editions = _own_profiles(user).values("edition_id")
        return self.filter(
            models.Q(edition__in=_secretariat_edition_ids(user))
            | (models.Q(edition__in=editions) & models.Q(status=ReportStatus.PUBLISHED))
        ).distinct()


class AnnualReport(TimeStampedModel):
    """
    The relation that closes one cycle and opens the next (FORUM_GOVERNANCE §2).

    ``sections`` is GENERATED by ``governance_services.build_report_sections`` from the edition, its
    commissions, the accepted proposals, the projects and the monitoring entries. It is stored
    rather than recomputed on every read so that a published report keeps saying what it said on the
    day it was published, even after the data moves on — the same reasoning as the frozen ruleset
    snapshot on a case assessment.
    """

    edition = models.OneToOneField(
        ForumEdition, on_delete=models.CASCADE, related_name="annual_report", verbose_name=_("édition")
    )
    status = models.CharField(
        _("état"), max_length=10, choices=ReportStatus.choices, default=ReportStatus.DRAFT, db_index=True
    )
    sections = models.JSONField(_("sections"), default=list, blank=True, editable=False)
    generated_at = models.DateTimeField(_("assemblée le"), null=True, blank=True, editable=False)
    generated_by = models.ForeignKey(
        ForumProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reports_generated",
        verbose_name=_("assemblée par"),
    )
    published_at = models.DateTimeField(_("publiée le"), null=True, blank=True, editable=False)

    class Meta:
        verbose_name = _("relation annuelle")
        verbose_name_plural = _("relations annuelles")
        ordering = ["-edition__year"]

    objects = AnnualReportQuerySet.as_manager()

    def __str__(self) -> str:
        return f"{_('Relation annuelle')} {self.edition.year}"

    @property
    def is_published(self) -> bool:
        return self.status == ReportStatus.PUBLISHED
