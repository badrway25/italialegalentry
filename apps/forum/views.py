"""Public views of the Forum Vénétie–Maroc — thin: gates, throttle, delegation to services."""

from __future__ import annotations

from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.decorators.http import require_http_methods

from audit.services import record as audit_record
from core import throttle
from forum import services
from forum.forms import ForumRegistrationForm

THROTTLE_SCOPE = "forum_register"


def _breadcrumbs(page_title: str, extra: list[dict] | None = None) -> list[dict]:
    crumbs = [{"label": page_title, "url": reverse("forum:index")}]
    if extra:
        crumbs.extend(extra)
    return crumbs


def _base_context(request, event):
    ctx = services.page_context(request, event)
    ctx["breadcrumbs"] = _breadcrumbs(ctx["page_title"])
    ctx["index_url"] = reverse("forum:index")
    return ctx


@require_http_methods(["GET", "HEAD"])
def index(request):
    event = services.current_event()
    ctx = _base_context(request, event)
    if event is not None and ctx["registration_open"] and ctx["forms_enabled"]:
        ctx["form"] = ForumRegistrationForm()
    return render(request, "forum/index.html", ctx)


@require_http_methods(["GET", "HEAD", "POST"])
def register(request):
    event = services.current_event()
    ctx = _base_context(request, event)
    ctx["breadcrumbs"] = _breadcrumbs(ctx["page_title"], [{"label": _("Inscription"), "url": ""}])
    ctx["standalone"] = True
    if event is None or not ctx["registration_open"]:
        if request.method == "POST":
            return render(request, "forum/register.html", ctx, status=403)
        return render(request, "forum/register.html", ctx)
    if not ctx["forms_enabled"]:
        # Gate G2 closed: GET shows the "form unavailable" notice, POST is refused and stores nothing.
        return render(request, "forum/register.html", ctx, status=403 if request.method == "POST" else 200)
    if request.method == "POST":
        if not throttle.allow(request, THROTTLE_SCOPE):
            audit_record(request, action="forum.registration.throttled")
            return render(request, "errors/429.html", status=429)
        form = ForumRegistrationForm(request.POST)
        if form.is_spam:
            # Honeypot / timing failure: bots get a success page, nothing is stored or sent.
            audit_record(request, action="forum.registration.spam_rejected", metadata={"event": event.slug})
            return redirect("forum:register_done")
        if form.is_valid():
            services.create_registration(request, event, form.cleaned_data)
            return redirect("forum:register_done")
        ctx["form"] = form
        return render(request, "forum/register.html", ctx, status=400)
    ctx["form"] = ForumRegistrationForm()
    return render(request, "forum/register.html", ctx)


@require_http_methods(["GET", "HEAD"])
def register_done(request):
    event = services.current_event()
    ctx = _base_context(request, event)
    ctx["breadcrumbs"] = _breadcrumbs(ctx["page_title"], [{"label": _("Inscription enregistrée"), "url": ""}])
    return render(request, "forum/register_done.html", ctx)
