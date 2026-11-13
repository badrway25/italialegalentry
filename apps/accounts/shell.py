"""
The account pages inside the console (V5.12 W2, lane B; DECISIONS «Lane B», scope: «the account area in the console
shell: allauth/layouts/manage.html extends the console base for signed-in users with a space»).

«Mon compte» — the profile, the e-mail addresses, the password, the second factor, the deletion request — used to open
in the PUBLIC shell (the header, the public footer), so a signed-in person left their console to change a password and
had no way back but the account menu. For a signed-in account whose reserved area is open, the account pages now draw
the console's frame: the space's rail (the person's, or the company's for a company account), the context bar with
the trail «<space> › Mon compte», the console foot. An anonymous visitor (a password reset by e-mail link) and an
account while the reserved area is switched off keep the public frame, as before.

``frame(request)`` → the layout template manage.html extends; ``console_context(request)`` → the rail and the trail
the console's chrome reads (portal/base_portal.html's contract: ``portal_nav``, ``breadcrumbs``).
"""

from __future__ import annotations

from typing import Any

from django.urls import NoReverseMatch, reverse
from django.utils.translation import gettext as _

PUBLIC_FRAME = "allauth/layouts/base.html"
CONSOLE_FRAME = "allauth/layouts/_console.html"


def in_console(request) -> bool:
    user = getattr(request, "user", None)
    if user is None or not user.is_authenticated:
        return False
    from portal import services as portal_services

    return bool(user.is_staff or portal_services.reserved_area_enabled())


def frame(request) -> str:
    return CONSOLE_FRAME if in_console(request) else PUBLIC_FRAME


def _profile_url() -> str:
    try:
        return reverse("accounts:profile")
    except NoReverseMatch:
        return ""


def console_context(request) -> dict[str, Any]:
    """The rail of the account's own space and the trail of an account page: «<space> › Mon compte»."""
    from accounts import roles
    from portal import services as portal_services

    user = request.user
    company = None
    space = portal_services.SPACE_PERSON
    if roles.audience_role(user) == roles.COMPANY:
        from companies import services as company_services

        company = company_services.company_for(user)
        space = portal_services.SPACE_COMPANY
    nav = portal_services.shell_navigation(user, space, "", company=company)
    head = nav[0]["space"] if nav and nav[0].get("space") else portal_services.shell_space(user, space)
    profile = _profile_url()
    crumbs = [
        {"label": head["label"], "url": head.get("url", "")},
        {"label": _("Mon compte"), "url": "" if request.path == profile else profile},
    ]
    page = _page_label(request)
    if page and request.path != profile:
        crumbs.append({"label": page, "url": ""})
    return {"portal_nav": nav, "breadcrumbs": crumbs}


def _page_label(request) -> str:
    """
    The trail's current crumb: the account section a page belongs to, in the words of
    accounts/partials/account_nav.html — or, for the two pages that are no section of their own, the page
    itself in its heading's words: the deletion request and the sign-out. The trail's last item is the current
    page (templates/components/breadcrumbs.html), so «Mon compte» names the profile alone (V5.20: the trail of
    those two pages had become «Mon compte» in the console frame).
    """
    match = getattr(request, "resolver_match", None)
    name = (match.view_name if match else "") or ""
    if name in ("account_email",):
        return _("Adresses e-mail")
    if name in ("account_change_password", "account_set_password"):
        return _("Mot de passe")
    if name.startswith("mfa_"):
        return _("Authentification à deux facteurs")
    if name == "accounts:delete_request":
        return _("Supprimer mon compte")
    if name == "account_logout":
        return _("Se déconnecter")
    return ""
