"""
Orientation wizard views — thin: every decision lives in ``services``/``engine``.

Progressive enhancement: the questionnaire is a plain HTML form (one question per page, POST +
redirect). When the request carries ``HX-Request`` the same fragment is returned for an in-place
swap; a completed questionnaire answers with ``HX-Redirect`` so the result page loads fully.
"""

from __future__ import annotations

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods, require_POST

from core import gates, throttle
from orientation import constants, engine, services
from orientation.forms import AnswerForm, ResumeForm


def _is_htmx(request) -> bool:
    return request.headers.get("HX-Request", "").lower() == "true"


def _too_many(request):
    return render(request, "errors/429.html", status=429)


def _breadcrumbs(*extra: dict) -> list[dict]:
    return [{"label": _("Orientation"), "url": reverse("orientation:start")}, *extra]


@require_http_methods(["GET", "POST"])
def start(request):
    ruleset = services.active_ruleset()
    if request.method == "POST":
        if ruleset is None:
            messages.warning(request, _("Le questionnaire d’orientation n’est pas disponible pour le moment."))
            return redirect("orientation:start")
        if not throttle.allow(
            request,
            constants.THROTTLE_SCOPE_START,
            limit=constants.THROTTLE_START_LIMIT,
            window_seconds=constants.THROTTLE_START_WINDOW_SECONDS,
        ):
            return _too_many(request)
        session = services.start_session(request, ruleset)
        return redirect("orientation:step", session_id=session.id)
    context = {
        "ruleset": ruleset,
        "available": ruleset is not None,
        "disclaimer_locked_key": constants.DISCLAIMER_LOCKED_KEYS[constants.DISCLAIMER_KEY],
        "breadcrumbs": [{"label": _("Orientation"), "url": ""}],
        "phase3_open": gates.phase3_public(),
    }
    return render(request, "orientation/start.html", context)


def _step_context(request, session, step: services.Step, form: AnswerForm | None = None) -> dict:
    question = services.present_question(session.ruleset, step.question)
    error = ""
    if form is not None and form.errors:
        error = " ".join(str(e) for errs in form.errors.values() for e in errs)
    return {
        "session": session,
        "q": question,
        "step_number": step.step_number,
        "progress": step.progress,
        "max_steps": step.max_steps,
        "can_go_back": step.can_go_back,
        "error": error,
        "step_url": reverse("orientation:step", kwargs={"session_id": session.id}),
        "noindex": True,
        "breadcrumbs": _breadcrumbs({"label": _("Questionnaire"), "url": ""}),
    }


@never_cache
@require_http_methods(["GET", "POST"])
def step(request, session_id):
    session = services.get_session_or_404(request, session_id)
    result_url = reverse("orientation:result", kwargs={"session_id": session.id})
    if session.is_completed:
        return _redirect_or_hx(request, result_url)
    current = services.current_step(session)
    if current.result is not None:  # defensive: engine reached an outcome without a stored result
        current = services.complete_session(request, session, current.result)
        return _redirect_or_hx(request, result_url)

    form: AnswerForm | None = None
    if request.method == "POST":
        action = request.POST.get("action", "answer")
        if action == "back":
            services.go_back(session)
            return _redirect_or_hx(request, reverse("orientation:step", kwargs={"session_id": session.id}))
        form = AnswerForm(current.question, request.POST)
        if form.is_valid():
            try:
                nxt = services.submit_answer(
                    request, session, form.cleaned_data["question_key"], form.cleaned_data["answer"]
                )
            except engine.InvalidAnswer:
                nxt = None
            if nxt is not None:
                if nxt.result is not None:
                    return _redirect_or_hx(request, result_url, full_page=True)
                return _redirect_or_hx(request, reverse("orientation:step", kwargs={"session_id": session.id}))
            form.add_error(None, _("La question a changé : merci de répondre à nouveau."))
    context = _step_context(request, session, current, form)
    template = "orientation/_step.html" if _is_htmx(request) else "orientation/step.html"
    return render(request, template, context)


def _redirect_or_hx(request, url: str, full_page: bool = False):
    if not _is_htmx(request):
        return HttpResponseRedirect(url)
    if full_page:
        response = HttpResponse(status=200)
        response["HX-Redirect"] = url
        return response
    # Render the fragment for the new state directly and tell HTMX the canonical URL.
    session_id = request.resolver_match.kwargs.get("session_id")
    session = services.get_session_or_404(request, session_id)
    if session.is_completed:
        response = HttpResponse(status=200)
        response["HX-Redirect"] = reverse("orientation:result", kwargs={"session_id": session.id})
        return response
    current = services.current_step(session)
    response = render(request, "orientation/_step.html", _step_context(request, session, current))
    response["HX-Push-Url"] = url
    return response


@never_cache
@require_http_methods(["GET"])
def result(request, session_id):
    session = services.get_session_or_404(request, session_id)
    if not session.is_completed or not hasattr(session, "result"):
        return redirect("orientation:step", session_id=session.id)
    res = session.result
    presentation = services.present_result(res)
    forms_gate = gates.public_forms_enabled()
    context = {
        "session": session,
        "result": res,
        "r": presentation,
        "reveal_token": services.pop_reveal_token(request, session),
        "can_save": request.user.is_authenticated and session.user_id is None,
        "is_saved": bool(session.user_id) and request.user.is_authenticated and session.user_id == request.user.id,
        "forms_enabled": forms_gate.open,
        "phase3_open": gates.phase3_public(),
        "disclaimer_version": res.disclaimer_version,
        "resume_url": request.build_absolute_uri(reverse("orientation:resume")),
        "noindex": True,
        "breadcrumbs": _breadcrumbs({"label": _("Pré-évaluation"), "url": ""}),
    }
    return render(request, "orientation/result.html", context)


@never_cache
@require_http_methods(["GET", "POST"])
def resume(request):
    form = ResumeForm(request.POST or None)
    if request.method == "POST":
        if not throttle.allow(
            request,
            constants.THROTTLE_SCOPE_RESUME,
            limit=constants.THROTTLE_RESUME_LIMIT,
            window_seconds=constants.THROTTLE_RESUME_WINDOW_SECONDS,
        ):
            return _too_many(request)
        if form.is_valid():
            session = services.resume_by_token(request, form.cleaned_data["token"])
            if session is not None:
                if session.is_completed:
                    return redirect("orientation:result", session_id=session.id)
                return redirect("orientation:step", session_id=session.id)
            form.add_error("token", _("Aucune pré-évaluation ne correspond à ce code, ou elle a expiré."))
    context = {"form": form, "noindex": False, "breadcrumbs": _breadcrumbs({"label": _("Reprendre"), "url": ""})}
    return render(request, "orientation/resume.html", context)


@login_required
@require_POST
def save(request, session_id):
    """Attach an anonymous session to the signed-in account. Public-form gate G2 applies."""
    session = services.get_session_or_404(request, session_id)
    gate = gates.public_forms_enabled()
    if not gate.open:
        return render(request, "orientation/save_unavailable.html", {"session": session, "noindex": True}, status=200)
    if session.user_id is None:
        services.attach_to_user(request, session, request.user)
        messages.success(request, _("Votre pré-évaluation a été enregistrée dans votre espace."))
    return redirect("orientation:result", session_id=session.id)


@require_POST
def restart(request, session_id):
    session = services.get_session_or_404(request, session_id)
    if not throttle.allow(
        request,
        constants.THROTTLE_SCOPE_START,
        limit=constants.THROTTLE_START_LIMIT,
        window_seconds=constants.THROTTLE_START_WINDOW_SECONDS,
    ):
        return _too_many(request)
    try:
        new_session = services.restart(request, session)
    except services.NoActiveRuleset:
        messages.warning(request, _("Le questionnaire d’orientation n’est pas disponible pour le moment."))
        return redirect("orientation:start")
    return redirect("orientation:step", session_id=new_session.id)
