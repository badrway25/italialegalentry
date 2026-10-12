from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse

from core import gates


class AccountAdapter(DefaultAccountAdapter):
    """Registration is a public form that requires the privacy information: gated by G2."""

    def is_open_for_signup(self, request) -> bool:
        return gates.public_forms_enabled().open

    def get_login_redirect_url(self, request):
        """
        Send each account to the surface it actually works in (L-09, REQ-IAM-09).

        Everyone landing on the person's dashboard was not a neutral default: a company saw a page
        built around a case file it does not have, and an authorised actor had to navigate to the
        one screen their role exists for. The order below is by specificity, and the person's
        dashboard remains the fallback because it is the only surface every account can use.
        """
        from django.urls import NoReverseMatch

        from accounts import roles

        user = getattr(request, "user", None)
        if user is None or not getattr(user, "is_authenticated", False):
            return reverse("portal:dashboard")

        for role, route in (
            (roles.AUTHORISED_ACTOR, "selection:workspace"),
            (roles.PROFESSIONAL, "helpdesk:queue"),
            (roles.COMPANY, "companies:dashboard"),
            (roles.TRAINING_PROVIDER, "academy:catalogue"),
        ):
            if roles.has_role(user, role):
                # A deployment without one of these modules must land on the dashboard rather than
                # raise at login: a routing preference is not worth an unusable sign-in.
                try:
                    return reverse(route)
                except NoReverseMatch:
                    continue
        return reverse("portal:dashboard")

    def get_email_verification_redirect_url(self, email_address):
        return reverse("account_login")

    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit=False)
        user.full_name = form.cleaned_data.get("full_name", "")
        user.account_type = form.cleaned_data.get("account_type") or user.account_type
        user.preferred_language = (request.LANGUAGE_CODE or "fr")[:2] if hasattr(request, "LANGUAGE_CODE") else "fr"
        if commit:
            user.save()
        return user
