"""
The account pages speak the project's glossary, not django-allauth's defaults (V5.12 D-11; Director's decisions
§9, «Account»: «Mon compte · Créer un compte · Se connecter · Adresse e-mail», overriding «Sign Up», «الاشتراك»,
«Courriel»).

django-allauth renders its pages, its form labels and its messages through ITS English msgids, and so do Django's
password validators under the sign-up's password. The project's catalogues (``LOCALE_PATHS``) come first in Django's
translation lookup, so such a msgid that is ALSO an entry of
``locale/<lang>/LC_MESSAGES/django.po`` is shown in the project's words, in every language — whichever template or
form draws it, the project's overrides (lane B, templates/account/**, templates/allauth/**) included.

This module only declares those msgids to the catalogue tooling: ``gettext_noop`` marks them for extraction
(``scripts/i18n_audit.py`` reads ``gettext_noop`` as ``makemessages`` does), so ``--sync`` keeps them and the audit
requires their translation in it, en, ar and fr. Nothing imports this module at runtime; nothing here is displayed
by it.

The words are the binding glossary's (docs/I18N_RTL.md §5: «Se connecter / Accedi / Sign in / تسجيل الدخول», «Créer un
compte / Crea un account / Create an account / إنشاء حساب», «Adresse e-mail»), the Italian in the institutional register
the glossary sets (§4.2: «Lei», impersonal forms, «account», «password», «e-mail»), sentence case in every language.
The English and Arabic renderings are PROVISIONAL pending the owner and counsel (Q3, accepted 28 Oct 2026 for the
interface terminology only).
"""

from __future__ import annotations

from django.utils.translation import gettext_noop, ngettext_lazy

ALLAUTH_TERMS: tuple[str, ...] = (
    # the entrance: titles, buttons, the line between sign-in and sign-up
    gettext_noop("Sign In"),
    gettext_noop("Sign Up"),
    gettext_noop("Sign Out"),
    gettext_noop("If you have not created an account yet, then please %(link)ssign up%(end_link)s first."),
    gettext_noop("Already have an account? Then please %(link)ssign in%(end_link)s."),
    gettext_noop("Remember Me"),
    # the fields allauth's forms label
    gettext_noop("Email"),
    gettext_noop("Email address"),
    gettext_noop("Email (again)"),
    gettext_noop("Password"),
    gettext_noop("Password (again)"),
    gettext_noop("Current Password"),
    gettext_noop("New Password"),
    gettext_noop("New Password (again)"),
    # the password reset
    gettext_noop("Forgot your password?"),
    gettext_noop("Password Reset"),
    gettext_noop("Reset My Password"),
    gettext_noop(
        "Forgotten your password? Enter your email address below, and we'll send you an email allowing you to reset it."
    ),
    gettext_noop("Please contact us if you have any trouble resetting your password."),
    # the account's own pages
    gettext_noop("Change Password"),
    gettext_noop("Set Password"),
    gettext_noop("Email Addresses"),
    gettext_noop("Two-Factor Authentication"),
    gettext_noop("Activate Authenticator App"),
    # Django's password validators, shown under the sign-up's password: the Italian in «Lei»'s register, never «tu»
    gettext_noop("Your password can’t be too similar to your other personal information."),
    gettext_noop("Your password can’t be a commonly used password."),
    gettext_noop("Your password can’t be entirely numeric."),
    # Django's EmailValidator, the inline error of every e-mail field: the glossary's «Adresse e-mail», never «courriel»
    gettext_noop("Enter a valid email address."),
)

#: Words another lane's source will use, declared here so ``--sync`` keeps them translated until it does (V5.12 review
#: of W2): the profile's phone help without its «Facultatif —», which the field's «facultatif» tag already says
#: (lane B, apps/accounts/profile_forms.py, docs/design-v5/QA/v512/b-w2/NOTES.md).
PENDING_SOURCE_TERMS: tuple[str, ...] = (gettext_noop("Utilisé uniquement pour le suivi de vos demandes."),)

PASSWORD_LENGTH = ngettext_lazy(
    "Your password must contain at least %(min_length)d character.",
    "Your password must contain at least %(min_length)d characters.",
    "min_length",
)
