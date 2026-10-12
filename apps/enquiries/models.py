"""
Public form submissions (enquiries).

Three concrete models share the abstract ``PublicSubmission`` base:

* ``CompanyNeedsRequest`` — Phase 1 « Recueil des besoins » (14 prescribed fields, §1.1);
* ``CollaborationProposal`` — institutions / universities collaboration proposals (Phase 2/3);
* ``ContactRequest`` — generic contact form.

Privacy by design: only the prescribed/minimal fields are stored, the IP address is hashed,
consent is linked to the exact text version shown, duplicates are suppressed for 24 hours,
records can be anonymised (GDPR erasure) and purged after the retention period
(``settings.ILE["RETENTION_MONTHS_FORMS"]``, 24 months from the legal texts — never invented).
"""

from __future__ import annotations

import hashlib
import re

from django.conf import settings
from django.db import models
from django.utils.functional import lazy
from django.utils.translation import gettext_lazy as _

from cms import locked_content
from core.models import TimeStampedModel

ANONYMISED = "[anonymised]"
_WS = re.compile(r"\s+")


def _locked_company_label(index: int):
    """Lazy label from the prescribed list ``p1.companies.form.fields`` (never hand-copied)."""

    def resolve() -> str:
        return locked_content.get("p1.companies.form.fields", "fr")[0][index]

    return lazy(resolve, str)()


def normalise_for_hash(value: object) -> str:
    return _WS.sub(" ", str(value or "")).strip().casefold()


def compute_duplicate_hash(model_label: str, values: dict[str, object]) -> str:
    """sha256 over the model label + normalised key fields (e-mail always included)."""
    parts = [model_label] + [f"{k}={normalise_for_hash(v)}" for k, v in sorted(values.items())]
    return hashlib.sha256("\x1f".join(parts).encode("utf-8")).hexdigest()


class SubmissionStatus(models.TextChoices):
    NEW = "new", _("Nouvelle")
    IN_PROGRESS = "in_progress", _("En cours de traitement")
    HANDLED = "handled", _("Traitée")
    ARCHIVED = "archived", _("Archivée")


class PublicSubmission(TimeStampedModel):
    """Abstract base for every public form submission (back-office workflow + privacy metadata)."""

    #: Fields containing personal data — replaced by ``ANONYMISED`` on erasure.
    PERSONAL_FIELDS: tuple[str, ...] = ()
    #: Fields hashed (with the e-mail) to detect a duplicate submission within 24 hours.
    DUPLICATE_KEY_FIELDS: tuple[str, ...] = ()
    #: Fields shown in the notification e-mail / exports, in order.
    DATA_FIELDS: tuple[str, ...] = ()
    #: ``consents.ConsentPurpose`` value used when recording consent.
    CONSENT_PURPOSE: str = ""

    status = models.CharField(
        _("statut"), max_length=12, choices=SubmissionStatus.choices, default=SubmissionStatus.NEW, db_index=True
    )
    admin_notes = models.TextField(_("notes internes"), blank=True)
    consent = models.ForeignKey(
        "consents.ConsentRecord",
        on_delete=models.PROTECT,
        related_name="%(class)s_submissions",
        verbose_name=_("consentement"),
    )
    language = models.CharField(_("langue"), max_length=5, choices=settings.LANGUAGES, default="fr")
    source_path = models.CharField(_("page d’origine"), max_length=300, blank=True)
    ip_hash = models.CharField(_("empreinte IP (hachée)"), max_length=32, blank=True)
    user_agent = models.CharField(_("navigateur"), max_length=160, blank=True)
    duplicate_hash = models.CharField(_("empreinte de doublon"), max_length=64, blank=True, db_index=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_submissions",
        verbose_name=_("compte associé"),
        help_text=_("Renseigné uniquement lorsque la personne était connectée au moment de l’envoi."),
    )
    external_reference = models.CharField(
        _("référence externe (CRM)"), max_length=80, blank=True, help_text=_("Identifiant dans l’outil CRM externe.")
    )
    handled_at = models.DateTimeField(_("traitée le"), null=True, blank=True)
    handled_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name=_("traitée par"),
    )
    last_contact_at = models.DateTimeField(
        _("dernier contact"),
        null=True,
        blank=True,
        help_text=_("Point de départ de la durée de conservation (24 mois à compter du dernier contact)."),
    )
    anonymised_at = models.DateTimeField(_("anonymisée le"), null=True, blank=True, editable=False)

    class Meta:
        abstract = True
        ordering = ["-created_at"]

    @property
    def is_anonymised(self) -> bool:
        return self.anonymised_at is not None

    @property
    def retention_reference(self):
        """Timestamp from which the retention period is counted (last contact, else creation)."""
        return self.last_contact_at or self.handled_at or self.created_at

    @classmethod
    def kind_label(cls) -> str:
        return str(cls._meta.verbose_name)

    def duplicate_key_values(self) -> dict[str, object]:
        return {name: getattr(self, name) for name in ("email", *self.DUPLICATE_KEY_FIELDS)}

    def compute_duplicate_hash(self) -> str:
        return compute_duplicate_hash(self._meta.label_lower, self.duplicate_key_values())

    def data_rows(self) -> list[tuple[str, str]]:
        """[(verbose label, value)] for e-mails and exports — labels come from the model fields."""
        rows = []
        for name in self.DATA_FIELDS:
            field = self._meta.get_field(name)
            value = getattr(self, name)
            if getattr(field, "choices", None):
                value = getattr(self, f"get_{name}_display")()
            rows.append((str(field.verbose_name), "" if value is None else str(value)))
        return rows

    def anonymise_fields(self) -> None:
        """Replace personal data in memory (persisted by ``enquiries.services.anonymise``)."""
        for name in self.PERSONAL_FIELDS:
            setattr(self, name, ANONYMISED)
        self.ip_hash = ""
        self.user_agent = ""
        self.duplicate_hash = ""
        self.owner = None


class CompanyNeedsRequest(PublicSubmission):
    """
    Phase 1 « Recueil des besoins » — the 14 prescribed fields, in the prescribed order
    (``p1.companies.form.fields``). Field 8 is intentionally a short free text so that companies
    may write « une dizaine » or « 5–10 » without being forced into a number.
    No field ever asks for candidates or profiles to recruit (F07).
    """

    PERSONAL_FIELDS = ("contact_name_and_role", "email", "phone", "notes")
    DUPLICATE_KEY_FIELDS = ("company_name", "profiles_needed")
    DATA_FIELDS = (
        "company_name",
        "sector",
        "headquarters",
        "contact_name_and_role",
        "email",
        "phone",
        "profiles_needed",
        "indicative_headcount",
        "qualifications_required",
        "experience_required",
        "language_requirements",
        "training_needs",
        "indicative_timeline",
        "notes",
    )
    CONSENT_PURPOSE = "company_needs"

    company_name = models.CharField(_locked_company_label(0), max_length=200)
    sector = models.CharField(_locked_company_label(1), max_length=160)
    headquarters = models.CharField(_locked_company_label(2), max_length=200)
    contact_name_and_role = models.CharField(_locked_company_label(3), max_length=200)
    email = models.EmailField(_locked_company_label(4), max_length=254)
    phone = models.CharField(_locked_company_label(5), max_length=40, blank=True)
    profiles_needed = models.TextField(_locked_company_label(6))
    indicative_headcount = models.CharField(_locked_company_label(7), max_length=60, blank=True)
    qualifications_required = models.TextField(_locked_company_label(8), blank=True)
    experience_required = models.TextField(_locked_company_label(9), blank=True)
    language_requirements = models.TextField(_locked_company_label(10), blank=True)
    training_needs = models.TextField(_locked_company_label(11), blank=True)
    indicative_timeline = models.CharField(_locked_company_label(12), max_length=200, blank=True)
    notes = models.TextField(_locked_company_label(13), blank=True)

    class Meta(PublicSubmission.Meta):
        verbose_name = _("Recueil des besoins — entreprise")
        verbose_name_plural = _("Recueil des besoins — entreprises")
        indexes = [models.Index(fields=["duplicate_hash", "created_at"], name="enq_company_dup_idx")]

    def __str__(self) -> str:
        return f"{self.company_name} ({self.created_at:%Y-%m-%d})" if self.created_at else self.company_name


class ProposalKind(models.TextChoices):
    INSTITUTION = "institution", _("Institution")
    UNIVERSITY = "university", _("Université / organisme de formation")
    OTHER_BODY = "other_body", _("Autre organisme")


class CollaborationProposal(PublicSubmission):
    """
    Collaboration proposal from an institution, a university/training body or another body.
    CONTENT_PENDING_LEGAL_REVIEW: the field set and labels are NOT prescribed by the implementation
    document — kept minimal (organisation, contact, proposal) pending confirmation.
    """

    PERSONAL_FIELDS = ("contact_name_and_role", "email", "phone", "proposal")
    DUPLICATE_KEY_FIELDS = ("kind", "organisation_name", "proposal")
    DATA_FIELDS = (
        "kind",
        "organisation_name",
        "organisation_type",
        "contact_name_and_role",
        "email",
        "phone",
        "country",
        "proposal",
    )
    CONSENT_PURPOSE = "institution_proposal"

    kind = models.CharField(_("type d’organisme"), max_length=12, choices=ProposalKind.choices, db_index=True)
    organisation_name = models.CharField(_("Nom de l’organisme"), max_length=200)
    organisation_type = models.CharField(
        _("Nature de l’organisme"),
        max_length=120,
        blank=True,
        help_text=_("Par exemple : Région, Commune, Chambre de Commerce, université, centre de formation."),
    )
    contact_name_and_role = models.CharField(_("Nom et fonction du référent"), max_length=200)
    email = models.EmailField(_("E-mail"), max_length=254)
    phone = models.CharField(_("Téléphone"), max_length=40, blank=True)
    country = models.CharField(_("Pays"), max_length=80)
    proposal = models.TextField(_("Proposition de collaboration"))

    class Meta(PublicSubmission.Meta):
        verbose_name = _("Proposition de collaboration")
        verbose_name_plural = _("Propositions de collaboration")
        indexes = [models.Index(fields=["duplicate_hash", "created_at"], name="enq_proposal_dup_idx")]

    def __str__(self) -> str:
        return f"{self.organisation_name} — {self.get_kind_display()}"

    @property
    def consent_purpose(self) -> str:
        return "university_proposal" if self.kind == ProposalKind.UNIVERSITY else "institution_proposal"


class ContactRequest(PublicSubmission):
    """Generic contact request (name, e-mail, subject, message)."""

    PERSONAL_FIELDS = ("name", "email", "subject", "message")
    DUPLICATE_KEY_FIELDS = ("subject", "message")
    DATA_FIELDS = ("name", "email", "subject", "message")
    CONSENT_PURPOSE = "contact"

    name = models.CharField(_("Nom et prénom"), max_length=160)
    email = models.EmailField(_("E-mail"), max_length=254)
    subject = models.CharField(_("Objet"), max_length=200)
    message = models.TextField(_("Message"))

    class Meta(PublicSubmission.Meta):
        verbose_name = _("Demande de contact")
        verbose_name_plural = _("Demandes de contact")
        indexes = [models.Index(fields=["duplicate_hash", "created_at"], name="enq_contact_dup_idx")]

    def __str__(self) -> str:
        return f"{self.subject} ({self.email})"


SUBMISSION_MODELS: tuple[type[PublicSubmission], ...] = (CompanyNeedsRequest, CollaborationProposal, ContactRequest)
