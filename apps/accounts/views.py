"""
Self-service account views. Every view acts on ``request.user`` only — there is deliberately no
user id in any URL (no IDOR surface). Business rules live in ``accounts.services``.
"""

from __future__ import annotations

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods, require_POST

from accounts import roles, services
from accounts.profile_forms import DeleteAccountForm, ProfileForm
from audit.services import record
from core import clock, throttle
from core.views import error_429


def _breadcrumbs(current: str) -> list[dict]:
    return [{"label": _("Mon compte"), "url": reverse("accounts:profile")}, {"label": current, "url": ""}]


@login_required
@never_cache
@require_http_methods(["GET", "POST"])
def profile(request):
    user = services.concrete_user(request.user)
    person_profile = services.get_or_create_profile(user)
    if request.method == "POST":
        form = ProfileForm(request.POST, user=user, profile=person_profile)
        if form.is_valid():
            services.update_profile(request, user, form.cleaned_data)
            messages.success(request, _("Votre profil a été mis à jour."))
            return redirect("accounts:profile")
    else:
        form = ProfileForm(user=user, profile=person_profile)
    context = {
        "form": form,
        "person_profile": person_profile,
        "memberships": services.memberships_of(user),
        "roles": roles.role_labels(user),  # translated labels, never the technical « role:* » names
        "has_totp": services.has_active_totp(user),
        "can_delete": services.can_request_deletion(user),
        "breadcrumbs": [{"label": _("Mon compte"), "url": ""}],
        "noindex": True,
    }
    return render(request, "accounts/profile.html", context)


@login_required
@never_cache
@require_POST
def export_data(request):
    user = services.concrete_user(request.user)
    data = services.export_user_data(user)
    record(request, action="account.export", target=user, metadata={"format": "json"})
    response = JsonResponse(
        data,
        encoder=DjangoJSONEncoder,
        json_dumps_params={"ensure_ascii": False, "indent": 2},
    )
    filename = f"italy-legal-entry-donnees-{clock.today():%Y%m%d}.json"
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    response["Cache-Control"] = "private, no-store"
    response["X-Content-Type-Options"] = "nosniff"
    return response


@login_required
@never_cache
@require_http_methods(["GET", "POST"])
def delete_request(request):
    user = services.concrete_user(request.user)
    if not services.can_request_deletion(user):
        raise PermissionDenied
    if request.method == "POST":
        if not throttle.allow(request, "account_delete", limit=5, window_seconds=600):
            return error_429(request)
        form = DeleteAccountForm(request.POST, user=user)
        if form.is_valid():
            services.request_deletion(request, user)
            logout(request)
            return redirect("accounts:delete_done")
    else:
        form = DeleteAccountForm(user=user)
    return render(
        request,
        "accounts/delete_request.html",
        {"form": form, "breadcrumbs": _breadcrumbs(_("Supprimer mon compte")), "noindex": True},
    )


@require_http_methods(["GET"])
def delete_done(request):
    return render(request, "accounts/delete_done.html", {"noindex": True})
