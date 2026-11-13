from __future__ import annotations

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import TimeStampedModel


class AccountType(models.TextChoices):
    PERSON = "person", _("Persona")
    COMPANY = "company", _("Impresa")
    INSTITUTION = "institution", _("Istituzione")
    UNIVERSITY = "university", _("Università / organismo di formazione")
    PROFESSIONAL = "professional", _("Professionista")
    STAFF = "staff", _("Staff")


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create(self, email: str, password: str | None, **extra):
        if not email:
            raise ValueError("E-mail is required")
        email = self.normalize_email(email).lower()
        user = self.model(email=email, **extra)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password: str | None = None, **extra):
        extra.setdefault("is_staff", False)
        extra.setdefault("is_superuser", False)
        return self._create(email, password, **extra)

    def create_superuser(self, email: str, password: str | None = None, **extra):
        extra.update(is_staff=True, is_superuser=True, is_active=True, account_type=AccountType.STAFF)
        return self._create(email, password, **extra)


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    """
    E-mail based user. Authorisation is role-based (accounts.roles / Django groups) plus
    object-level policies (accounts.permissions) — ``is_staff`` only opens the back-office door.
    """

    email = models.EmailField(_("e-mail"), unique=True)
    full_name = models.CharField(_("nome e cognome"), max_length=160, blank=True)
    preferred_language = models.CharField(_("lingua preferita"), max_length=5, choices=settings.LANGUAGES, default="fr")
    account_type = models.CharField(
        _("tipo di account"), max_length=16, choices=AccountType.choices, default=AccountType.PERSON, db_index=True
    )
    is_active = models.BooleanField(_("attivo"), default=True)
    is_staff = models.BooleanField(_("accesso al back-office"), default=False)
    date_joined = models.DateTimeField(_("registrato il"), auto_now_add=True)
    terms_accepted_at = models.DateTimeField(_("condizioni accettate il"), null=True, blank=True)
    terms_consent = models.ForeignKey(
        "consents.ConsentRecord", on_delete=models.SET_NULL, null=True, blank=True, related_name="+"
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = []

    class Meta:
        verbose_name = _("utente")
        verbose_name_plural = _("utenti")
        ordering = ["email"]

    def __str__(self) -> str:
        return self.email

    def get_full_name(self) -> str:
        return self.full_name or self.email

    def get_short_name(self) -> str:
        return (self.full_name or self.email).split(" ")[0]

    @property
    def organisations(self):
        return Organisation.objects.filter(memberships__user=self).distinct()


class VerificationStatus(models.TextChoices):
    """
    Whether a self-declared account type has been checked by a human.

    Anyone can tick "Institution" on a public signup form. Until 20 September 2026 that declaration
    was enough to be granted ``role:institution`` on the spot. The roles carried no model permissions
    yet, so nothing was exposed — but the role workspaces of phase P1 give each of those roles a real
    perimeter, and a self-declared role would then be an escalation that needs no exploit, only a
    dropdown. The declaration and the grant are therefore separated here: the account type is what
    the visitor says, the role is what the project has verified.
    """

    NOT_REQUIRED = "not_required", _("Non necessaria")
    PENDING = "pending", _("In attesa di verifica")
    APPROVED = "approved", _("Verificata")
    REJECTED = "rejected", _("Respinta")


#: Account types a visitor may claim but that must be verified before the matching role is granted.
#: A person claiming to be a person is claiming nothing.
VERIFIED_ACCOUNT_TYPES: tuple[str, ...] = (
    AccountType.COMPANY,
    AccountType.INSTITUTION,
    AccountType.UNIVERSITY,
    AccountType.PROFESSIONAL,
)


class AccountVerification(TimeStampedModel):
    """One request to have a declared account type verified, and its outcome."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="verification",
        verbose_name=_("utente"),
    )
    declared_type = models.CharField(_("tipo dichiarato"), max_length=20, choices=AccountType.choices)
    declared_organisation = models.CharField(_("organizzazione dichiarata"), max_length=200, blank=True)
    status = models.CharField(
        _("stato"),
        max_length=16,
        choices=VerificationStatus.choices,
        default=VerificationStatus.PENDING,
        db_index=True,
    )
    evidence_note = models.TextField(
        _("elementi forniti"),
        blank=True,
        help_text=_("Che cosa ha dichiarato o trasmesso la persona a sostegno della richiesta."),
    )
    decision_note = models.TextField(_("motivazione della decisione"), blank=True)
    decided_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name=_("deciso da"),
    )
    decided_at = models.DateTimeField(_("deciso il"), null=True, blank=True)

    class Meta:
        verbose_name = _("verifica dell'account")
        verbose_name_plural = _("verifiche degli account")
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.user_id} · {self.get_declared_type_display()} · {self.get_status_display()}"

    @property
    def is_pending(self) -> bool:
        return self.status == VerificationStatus.PENDING


class OrganisationKind(models.TextChoices):
    COMPANY = "company", _("Impresa")
    INSTITUTION = "institution", _("Istituzione")
    UNIVERSITY = "university", _("Università")
    TRAINING_BODY = "training_body", _("Organismo di formazione")
    ASSOCIATION = "association", _("Associazione / Camera di Commercio")
    PROFESSIONAL_FIRM = "professional_firm", _("Studio professionale")
    OTHER = "other", _("Altro")


class Organisation(TimeStampedModel):
    name = models.CharField(_("denominazione"), max_length=200)
    kind = models.CharField(_("tipo"), max_length=20, choices=OrganisationKind.choices)
    country = models.CharField(_("paese"), max_length=80, blank=True)
    city = models.CharField(_("città"), max_length=120, blank=True)
    website = models.URLField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="+")
    external_reference = models.CharField(max_length=80, blank=True, help_text=_("ID CRM esterno (integrations)"))

    class Meta:
        verbose_name = _("organizzazione")
        verbose_name_plural = _("organizzazioni")
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class MembershipRole(models.TextChoices):
    OWNER = "owner", _("Responsabile")
    MEMBER = "member", _("Membro")


class Membership(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="memberships")
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name="memberships")
    role = models.CharField(max_length=10, choices=MembershipRole.choices, default=MembershipRole.MEMBER)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "organisation"], name="uniq_membership")]
        verbose_name = _("appartenenza")
        verbose_name_plural = _("appartenenze")

    def __str__(self) -> str:
        return f"{self.user} @ {self.organisation} ({self.role})"


class EducationLevel(models.TextChoices):
    """
    Declared level of education. Deliberately coarse.

    The platform has no role in recognising qualifications and must not give a person the impression
    that it does, so the profile records a level, never a diploma, an institution or a grade. Four
    bands are enough for a rule to say "this route expects a higher-education qualification" and not
    enough to look like an assessment of anybody's worth.
    """

    NONE = "none", _("Nessun titolo dichiarato")
    SECONDARY = "secondary", _("Istruzione secondaria")
    HIGHER = "higher", _("Istruzione superiore (laurea o equivalente)")
    POSTGRADUATE = "postgraduate", _("Post-laurea")


class PersonProfile(TimeStampedModel):
    """
    What a person tells us about their situation, and nothing else.

    Each field earns its place by being read by something: the versioned rule engine declares the
    facts a legal rule may consult (``rules.engine.ALLOWED_FIELDS``) and this is where most of them
    come from. A field nothing reads is personal data held for no reason, which is the definition of
    what data minimisation forbids — so the rule for adding one here is that a rule, a checklist or a
    screen must already need it.

    Three absences are deliberate:

    * **No diploma, institution or grade.** The platform does not recognise qualifications and must
      not look as though it does. ``education_level`` is a band; ``has_qualification_recognition``
      records only whether a procedure has been COMPLETED ELSEWHERE.
    * **No employer name.** ``has_job_offer`` is a yes or no. Which company it is belongs to the case
      file, where it is access-controlled, not to a profile that widens with every login.
    * **No document numbers.** A passport number is never a fact a rule needs; its expiry might be,
      and that lives on the document itself.

    Everything is optional. A person who answers nothing still gets an orientation — it will simply
    be the one that can be given without knowing anything, which is the honest result.
    """

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="person_profile")
    country_of_residence = models.CharField(_("paese di residenza"), max_length=80, blank=True)
    phone = models.CharField(_("telefono"), max_length=40, blank=True)

    date_of_birth = models.DateField(
        _("data di nascita"),
        null=True,
        blank=True,
        help_text=_("Alcune condizioni d'ingresso dipendono dall'età. Le regole leggono l'età, mai la data."),
    )
    nationality = models.CharField(
        _("cittadinanza"),
        max_length=80,
        blank=True,
        help_text=_("Le condizioni d'ingresso dipendono dalla cittadinanza dichiarata."),
    )
    education_level = models.CharField(
        _("livello di studi"),
        max_length=16,
        choices=EducationLevel.choices,
        blank=True,
        help_text=_("Serve a distinguere i percorsi che presuppongono un titolo superiore. Non è una valutazione."),
    )
    years_of_experience = models.PositiveSmallIntegerField(
        _("anni di esperienza professionale"),
        null=True,
        blank=True,
        help_text=_("Dichiarati dalla persona. La piattaforma non li verifica e non li certifica."),
    )
    languages = models.JSONField(
        _("lingue dichiarate"),
        default=list,
        blank=True,
        help_text=_("Codici di lingua, es. [\"fr\", \"ar\"]. Dichiarati, mai certificati."),
    )
    has_job_offer = models.BooleanField(
        _("proposta di lavoro in Italia"),
        null=True,
        blank=True,
        help_text=_("Sì o no. Il nome dell'impresa non è richiesto qui."),
    )
    has_qualification_recognition = models.BooleanField(
        _("riconoscimento del titolo già ottenuto"),
        null=True,
        blank=True,
        help_text=_("Riguarda una procedura conclusa presso le autorità competenti, non presso questa piattaforma."),
    )
    completed_at = models.DateTimeField(_("profilo completato il"), null=True, blank=True, editable=False)

    class Meta:
        verbose_name = _("profilo persona")
        verbose_name_plural = _("profili persona")

    def __str__(self) -> str:
        return f"Profilo {self.user}"

    #: Fields the orientation and the rule engine actually read. ``completeness`` is measured against
    #: this list rather than against every column, so adding an administrative field does not make
    #: every existing profile look unfinished.
    PROFILE_FIELDS = (
        "date_of_birth",
        "nationality",
        "country_of_residence",
        "education_level",
        "years_of_experience",
        "languages",
        "has_job_offer",
    )

    def answered(self) -> list[str]:
        """The profile fields the person has actually answered. ``False`` is an answer; ``None`` is not."""
        given = []
        for name in self.PROFILE_FIELDS:
            value = getattr(self, name)
            if value is None or value == "" or value == []:
                continue
            given.append(name)
        return given

    @property
    def completeness(self) -> int:
        """Answered fields out of the ones that are read. A count, never a score about the person."""
        return len(self.answered())

    @property
    def is_complete(self) -> bool:
        return self.completeness == len(self.PROFILE_FIELDS)
