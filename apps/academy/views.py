"""
Academy views — thin: authentication, HTTP method, rendering.

Every rule about WHO may see or do WHAT lives in ``academy.services`` and ``academy.policies``
(deny by default). A view never filters a queryset itself.

All views require an authenticated account — and nothing more. That is not laxity, it is the
requirement: CR-14 and REQ-EDU-04 say a person reaches the Academy without being selected by a
company, so there is deliberately no role test, no case-file test and no selection test on the way
in. They are ``never_cache`` (a personal training record must never sit in a shared cache) and
``noindex``.

Mutations are POST-only with CSRF, and each one calls a service that audits it.
"""

from __future__ import annotations

from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import Truncator
from django.utils.translation import gettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods

from academy import services
from academy.models import CourseModule, CourseType, EnrolmentStatus
from core.links import public_url

CRUMB_MAX_CHARS = 60


def _noindex(response):
    """
    Say "do not index" in the HEADER as well as in the page, as the platform shell does.

    The ``noindex`` meta tag is what a crawler parsing a rendered body reads, and every Academy
    page emits it. The header covers what the meta tag cannot: a HEAD request, the 302 that every
    enrolment and every attendance answers with, and the 503 of the kill switch. A personal
    training record is not somewhere to rely on the sufficient case.
    """
    response.headers.setdefault("X-Robots-Tag", "noindex, nofollow")
    return response


def academy_view(active: str = "academy", methods: tuple[str, ...] = ("GET", "HEAD")):
    """login_required (outermost) → never_cache → allowed methods → platform kill switch."""

    def decorator(view):
        @wraps(view)
        def wrapped(request, *args, **kwargs):
            from portal import services as portal_services

            if not portal_services.reserved_area_enabled() and not request.user.is_staff:
                return _noindex(render(request, "portal/unavailable.html", {"noindex": True}, status=503))
            request.academy_active = active
            return _noindex(view(request, *args, **kwargs))

        return login_required(never_cache(require_http_methods(list(methods))(wrapped)))

    return decorator


def _navigation(user, active: str) -> list[dict]:
    """
    The platform navigation, with the Academy entries added.

    ``portal.services.navigation`` belongs to another lane and does not know about the Academy yet;
    rather than edit it, its result is extended here and the Academy entry is skipped if it appears
    there later, so nothing is ever listed twice.
    """
    from portal import services as portal_services

    items = [dict(item) for item in portal_services.navigation(user, "")]
    known = {item.get("key") for item in items}
    extra = (
        ("academy", _("Academy"), public_url("academy:catalogue")),
        ("academy_mine", _("Mes formations"), public_url("academy:mine")),
    )
    for key, label, url in extra:
        if key not in known and url:
            items.append({"key": key, "label": label, "url": url})
    for item in items:
        item["current"] = item.get("key") == active
    return items


def _crumb(label) -> dict:
    return {"label": Truncator(str(label)).chars(CRUMB_MAX_CHARS), "url": ""}


def _render(request, template: str, context: dict, *crumbs: dict):
    root = {"label": _("Academy"), "url": public_url("academy:catalogue")}
    context.update(
        {
            "portal_nav": _navigation(request.user, getattr(request, "academy_active", "academy")),
            "breadcrumbs": [root, *crumbs] if crumbs else [{**root, "url": ""}],
            "portal_context": _("Academy"),
            "noindex": True,
        }
    )
    return render(request, template, context)


# =================================================================================================
# Catalogue
# =================================================================================================
@academy_view("academy")
def catalogue(request):
    course_type = request.GET.get("domaine", "")
    language = request.GET.get("langue", "")
    search = request.GET.get("q", "")
    courses = services.catalogue(
        request.user,
        course_type=course_type,
        language=language,
        search=search,
    )
    enrolled = set(
        services.enrolments_for(request.user).filter(person=request.user).values_list("course_id", flat=True)
    )
    context = {
        "courses": list(courses),
        "domains": services.catalogue_domains(request.user),
        "selected_domain": course_type if course_type in CourseType.values else "",
        "selected_language": language,
        "search": search,
        "enrolled_ids": enrolled,
        "summary": services.summary(request.user),
    }
    return _render(request, "academy/catalogue.html", context)


@academy_view("academy")
def course_detail(request, slug: str):
    course = services.course_for(request.user, slug)
    enrolment = services.enrolment_of(request.user, course)
    context = {
        "course": course,
        "modules": list(course.modules.all()),
        "materials": list(course.materials.all()),
        "competences": list(course.competences.all()),
        "enrolment": enrolment,
        "can_enrol": services.may(request.user, "enrol", course),
    }
    return _render(request, "academy/course_detail.html", context, _crumb(course.title))


@academy_view("academy", methods=("POST",))
def enrol(request, slug: str):
    course = services.course_for(request.user, slug)
    services.require_can(request.user, "enrol", course)
    enrolment = services.enrol(request.user, course, request=request)
    messages.success(
        request,
        _("Inscription enregistrée. Vous pouvez suivre les modules quand vous le souhaitez."),
    )
    url = public_url("academy:enrolment", enrolment.uuid)
    return redirect(url or public_url("academy:mine") or "/")


# =================================================================================================
# My trainings
# =================================================================================================
@academy_view("academy_mine")
def mine(request):
    rows = list(services.enrolments_for(request.user).filter(person=request.user))
    # A professional or an operator holding a live assignment legitimately READS the training plan
    # of the person they follow — but that plan is not theirs, and a page headed "Mes formations"
    # that lists it among their own says something false about whose record it is. The two are
    # separated here and the second register states the mandate it is read under.
    plans = list(services.plans_for(request.user))
    context = {
        "ongoing": [row for row in rows if row.is_open],
        "completed": [row for row in rows if row.is_completed],
        "withdrawn": [row for row in rows if row.status == EnrolmentStatus.WITHDRAWN],
        "plans": [plan for plan in plans if plan.person_id == request.user.id],
        "mandated_plans": [plan for plan in plans if plan.person_id != request.user.id],
        "summary": services.summary(request.user),
    }
    return _render(request, "academy/mine.html", context, {"label": _("Mes formations"), "url": ""})


@academy_view("academy_mine")
def enrolment_detail(request, uuid):
    enrolment = services.enrolment_for(request.user, uuid)
    services.require_can(request.user, "view", enrolment)
    context = {
        "enrolment": enrolment,
        "course": enrolment.course,
        "rows": services.module_rows(enrolment),
        "progress": services.progress(enrolment),
        "next_module": services.next_module(enrolment),
        "materials": list(enrolment.course.materials.all()),
        "can_change": services.may(request.user, "change", enrolment),
    }
    return _render(
        request,
        "academy/enrolment_detail.html",
        context,
        {"label": _("Mes formations"), "url": public_url("academy:mine")},
        _crumb(enrolment.course.title),
    )


@academy_view("academy_mine", methods=("POST",))
def attend(request, uuid, module_pk: int):
    enrolment = services.enrolment_for(request.user, uuid)
    services.require_can(request.user, "change", enrolment)
    module = get_object_or_404(CourseModule, pk=module_pk, course_id=enrolment.course_id)
    services.record_attendance(enrolment, module, actor=request.user, request=request)
    if enrolment.is_completed:
        messages.success(
            request,
            _("Tous les modules ont été suivis. Une attestation de suivi est enregistrée dans votre compte."),
        )
    else:
        messages.success(request, _("Module enregistré comme suivi."))
    return redirect(public_url("academy:enrolment", enrolment.uuid) or "/")


@academy_view("academy_mine", methods=("POST",))
def withdraw(request, uuid):
    enrolment = services.enrolment_for(request.user, uuid)
    services.require_can(request.user, "change", enrolment)
    services.withdraw(enrolment, actor=request.user, request=request)
    messages.info(request, _("Formation interrompue. Vous pourrez la reprendre à tout moment."))
    return redirect(public_url("academy:enrolment", enrolment.uuid) or "/")


@academy_view("academy_mine", methods=("POST",))
def resume(request, uuid):
    enrolment = services.enrolment_for(request.user, uuid)
    services.require_can(request.user, "change", enrolment)
    services.resume(enrolment, request=request)
    messages.success(request, _("Formation reprise."))
    return redirect(public_url("academy:enrolment", enrolment.uuid) or "/")


# =================================================================================================
# Training plan
# =================================================================================================
@academy_view("academy_mine")
def plan_detail(request, uuid):
    plan = services.plan_for(request.user, uuid)
    services.require_can(request.user, "view", plan)
    context = {
        "plan": plan,
        "items": services.plan_item_rows(plan, request.user),
        "gap_rows": services.plan_rows(plan, viewer=request.user),
        "is_own": plan.person_id == request.user.id,
    }
    # Read under a mandate: the reader must be told so, and told which mandate, on the page itself.
    # A plan opened by a professional looks exactly like their own otherwise.
    return _render(
        request,
        "academy/plan_detail.html",
        context,
        {"label": _("Mes formations"), "url": public_url("academy:mine")},
        _crumb(plan.title),
    )
