"""
Document views (language-neutral, under /documents/).

Thin on purpose: authentication, HTTP method, one authorisation call, one service call, one render.
Every rule about what may be filed, read, reviewed or delivered lives in ``documents.policies`` and
``documents.services``, so a second entry point (an API, a command, the back-office) cannot reach a
different answer.

Two invariants this module defends:

* **Authorisation on EVERY delivery.** A signed link narrows who and for how long; it never stands
  in for the object-level check, which runs again on the way out.
* **One way in, one way out.** Files enter through ``services.store_upload`` (directly, or through
  ``services.file_version``) and leave through ``_serve`` — nowhere else.

The Dépôt (design V5, W3-C — ``templates/documents/partials/depot.html``, ``static/js/src/depot.js``) sends the SAME
form to the SAME two endpoints and asks for its answer as JSON (``DEPOT_HEADER``), so that the server's answer is
composed IN PLACE, in the Dépôt, instead of a page change (DOCUMENT_WORKSPACE.md §11: the eleven answers). The header
changes the form of the answer and nothing else: the validation chain, the size limit, the MIME and antivirus checks,
the storage, the throttle and the permissions run the same lines on both roads.
"""

from __future__ import annotations

import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ValidationError
from django.core.signing import BadSignature, SignatureExpired
from django.http import FileResponse, Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods, require_POST

from accounts.permissions import can, require
from audit.services import record
from core import throttle
from core.views import error_429
from documents import presenters, services
from documents.forms import DocumentUploadForm, RequirementReviewForm, RequirementUploadForm
from documents.models import DocumentRequirement, PrivateDocument

log = logging.getLogger("ile.documents")

UPLOAD_THROTTLE = {"limit": 30, "window_seconds": 3600}
#: A compromised session should not be able to drain a case file in one sweep unnoticed.
DOWNLOAD_THROTTLE = {"limit": 120, "window_seconds": 3600}

#: The Dépôt's request header: its script asks for the answer as JSON. Without it — no script — every view below answers
#: as it always has (a redirect and its message, the 429 page, the Conditions page).
DEPOT_HEADER = "X-ILE-Depot"


# ---------------------------------------------------------------------------------------------
# The Dépôt's answers (design V5, W3-C; DOCUMENT_WORKSPACE.md §11.1)
# ---------------------------------------------------------------------------------------------
def _depot_json(request) -> bool:
    return request.headers.get(DEPOT_HEADER) == "1"


def _depot_answer(answer: str, message, **extra) -> JsonResponse:
    """
    One answer of the Dépôt: its code — the client composes its state from it — and the server's own sentence,
    verbatim, in the reader's language. Always a 200: a refusal, the throttle or the Conditions gate is an ANSWER the
    Dépôt composes, not a failure of the request (the road without script keeps its 403 and 429 pages). Never cached;
    nothing about a file's scan is said beyond what the page says.
    """
    response = JsonResponse({"answer": answer, "message": str(message), **extra})
    response["Cache-Control"] = "no-store"
    return response


def _depot_refusal(form) -> JsonResponse:
    """The first refusal of a bound form, with its field and its code (``empty``, ``too_large``, ``extension``,
    ``content_mismatch``, ``image_invalid``, ``pdf_active_content``, ``required``, ``invalid`` …) — the messages are
    the form's and the validation chain's, untouched."""
    for field, errors in form.errors.as_data().items():
        for error in errors:
            message = next(iter(error), "")
            return _depot_answer(getattr(error, "code", None) or "invalid", message, field=field)
    return _depot_answer("invalid", "")


def _depot_throttled() -> JsonResponse:
    return _depot_answer(
        "throttled",
        _(
            "Vous avez atteint la limite d’envois autorisée. Merci de réessayer dans quelques minutes ; "
            "rien n’a été perdu de votre côté."
        ),
        title=_("Trop de requêtes"),
    )


# ---------------------------------------------------------------------------------------------
# Shell
# ---------------------------------------------------------------------------------------------
def _portal_shell(request, context: dict, *crumbs: dict) -> dict:
    """
    Put a page on the PLATFORM shell, never on the public one.

    ``portal.services.navigation`` is imported lazily and defensively: this app must keep working
    if the reserved area is switched off, and a register of what a case still needs is exactly the
    page that must not disappear because a sibling app is unavailable.
    """
    root = {"label": _("Espace réservé"), "url": ""}
    nav = []
    try:
        from django.urls import reverse as _reverse

        from portal import services as portal_services

        nav = portal_services.navigation(request.user, "documents")
        root = {"label": _("Espace réservé"), "url": _reverse("portal:dashboard")}
    except Exception:  # noqa: BLE001 — the page stands on its own without the reserved-area shell
        nav = []
    context.update(
        {
            "portal_nav": nav,
            "breadcrumbs": [root, *crumbs] if crumbs else [{**root, "url": ""}],
            "noindex": True,
        }
    )
    return context


# ---------------------------------------------------------------------------------------------
# The register
# ---------------------------------------------------------------------------------------------
@login_required
@never_cache
@require_http_methods(["GET"])
def index(request):
    """
    The register of what each of the account's case files still needs.

    NOT a file browser: the question is "what is missing, who is waiting for it, and what happens
    next", and a list of filenames answers none of it. The loose files below the register are the
    ones attached to no requirement — they keep their place so nothing becomes unreachable.
    """
    context = {
        "register": presenters.register_context(
            request.user, state_filter=request.GET.get("état") or request.GET.get("etat") or ""
        ),
        "loose_documents": _loose_documents(request.user),
        "may_upload": services.user_may_upload(request.user),
    }
    return render(request, "documents/index.html", _portal_shell(request, context))


def _loose_documents(user):
    """The account's own files that answer no requirement — legacy uploads, personal copies."""
    return (
        PrivateDocument.objects.for_owner(user)
        .filter(requirement_versions__isnull=True)
        .select_related("organisation")
        .order_by("-created_at")[:50]
    )


@login_required
@never_cache
@require_http_methods(["GET"])
def requirement_detail(request, pk):
    requirement = _get_requirement(request.user, pk)
    row = presenters.present_requirement(requirement, user=request.user, with_versions=True)
    context = {
        "row": row,
        "case": requirement.case,
        "responsible": [item for item in requirement.case.assignments.select_related("organisation") if item.is_live],
        "upload_form": RequirementUploadForm(requirement=requirement, user=request.user) if row["may_file"] else None,
        "review_form": RequirementReviewForm() if row["may_review"] else None,
        "link_minutes": services.DOWNLOAD_LINK_MINUTES,
    }
    return render(
        request,
        "documents/requirement_detail.html",
        _portal_shell(
            request,
            context,
            {"label": _("Mes pièces"), "url": reverse("documents:index")},
            {"label": requirement.title, "url": ""},
        ),
    )


def _get_requirement(user, pk) -> DocumentRequirement:
    """
    Fetch a requirement the account may read, or 404.

    Authorisation is applied IN THE QUERYSET, so an account that may not read this row cannot tell
    it apart from one that does not exist — no count, no differently worded error, no timing tell.
    """
    requirement = (
        DocumentRequirement.objects.readable_by(user).select_related("case", "checklist_item").filter(pk=pk).first()
    )
    if requirement is None:
        raise Http404
    return requirement


# ---------------------------------------------------------------------------------------------
# Filing and reviewing
# ---------------------------------------------------------------------------------------------
@login_required
@never_cache
@require_POST
def requirement_file(request, pk):
    requirement = _get_requirement(request.user, pk)
    require(request.user, "file", requirement)
    as_json = _depot_json(request)
    if not services.user_may_upload(request.user):
        if as_json:
            return _depot_answer(
                "terms", _("Le dépôt d’une pièce nécessite l’acceptation des Conditions d’utilisation.")
            )
        return render(
            request,
            "documents/terms_required.html",
            _portal_shell(request, {}, {"label": _("Mes pièces"), "url": reverse("documents:index")}),
            status=403,
        )
    if not throttle.allow(request, "documents_upload", **UPLOAD_THROTTLE):
        return _depot_throttled() if as_json else error_429(request)

    form = RequirementUploadForm(request.POST, request.FILES, requirement=requirement, user=request.user)
    if form.is_valid():
        try:
            version = services.file_version(
                requirement,
                request.user,
                form.cleaned_data["file"],
                expires_on=form.cleaned_data.get("expires_on"),
                request=request,
            )
        except ValidationError as exc:
            if as_json:
                return _depot_answer(getattr(exc, "code", None) or "refused", " ".join(exc.messages))
            for message in exc.messages:
                messages.error(request, message)
        else:
            if version.document is not None and version.document.is_infected:
                infected = _("Le fichier a été signalé par l’analyse antivirus : il n’a pas été conservé.")
                if as_json:
                    # The deposit is recorded and the file is gone: the piece's state changed (NON VALIDE), so the
                    # Dépôt reads the piece again — `version` says a version was written.
                    return _depot_answer("infected", infected, version=version.number)
                messages.error(request, infected)
            else:
                filed = _("Pièce déposée (version %(n)d). Elle sera examinée par un intervenant du dossier.") % {
                    "n": version.number
                }
                if as_json:
                    return _depot_answer("filed", filed, version=version.number)
                messages.success(request, filed)
            return redirect("documents:requirement", pk=requirement.pk)
    else:
        if as_json:
            return _depot_refusal(form)
        for field_errors in form.errors.values():
            for message in field_errors:
                messages.error(request, message)
    return redirect("documents:requirement", pk=requirement.pk)


@login_required
@never_cache
@require_POST
def requirement_review(request, pk):
    requirement = _get_requirement(request.user, pk)
    require(request.user, "review", requirement)
    version = requirement.current_version
    if version is None:
        raise Http404

    form = RequirementReviewForm(request.POST)
    if not form.is_valid():
        for field_errors in form.errors.values():
            for message in field_errors:
                messages.error(request, message)
        return redirect("documents:requirement", pk=requirement.pk)

    decision = form.cleaned_data["decision"]
    note = form.cleaned_data.get("note", "")
    try:
        if decision == RequirementReviewForm.REPLACE:
            services.request_replacement(requirement, actor=request.user, reason=note, request=request)
        else:
            from documents.models import VersionDecision

            mapping = {
                RequirementReviewForm.ACCEPT: VersionDecision.ACCEPTED,
                RequirementReviewForm.REFUSE: VersionDecision.REFUSED,
                RequirementReviewForm.REVIEW: VersionDecision.IN_REVIEW,
            }
            services.set_decision(version, mapping[decision], actor=request.user, note=note, request=request)
    except ValidationError as exc:
        for message in exc.messages:
            messages.error(request, message)
    else:
        messages.success(request, _("Examen enregistré."))
    return redirect("documents:requirement", pk=requirement.pk)


# ---------------------------------------------------------------------------------------------
# Delivery
# ---------------------------------------------------------------------------------------------
def _serve(request, doc: PrivateDocument, *, via: str) -> FileResponse:
    """
    The single exit. Authorisation has already been checked by the caller and is checked again here.

    A refusal is a 403 whatever its reason, and nothing about the reason reaches the client: an
    account must not be able to learn a file's scan status by comparing error messages.

    A row whose stored file is gone is a 404 for an account both gates let through (a lost file is
    not a server error), logged once as ``documents.file_missing`` with the document's id and
    nothing else — never its name or its path. The file is opened only AFTER both gates, so an
    account they refuse still gets its 403 and cannot learn whether the file exists.
    """
    require(request.user, "download", doc)
    # The second gate: a file may be readable to this account and still not be deliverable to it.
    # ``services.delivery_block`` is the single statement of that rule, consulted here and by
    # ``presenters.present_version`` — so the page never draws a link this view would refuse.
    if services.delivery_block(doc, request.user):
        raise PermissionDenied
    try:
        stored = services.open_for_download(doc)
    except FileNotFoundError:
        log.warning("documents.file_missing document=%s", doc.pk)
        raise Http404 from None
    response = FileResponse(
        stored,
        as_attachment=True,
        filename=doc.original_name,
        content_type=doc.content_type,
    )
    response["X-Content-Type-Options"] = "nosniff"
    response["Cache-Control"] = "private, no-store"
    response["Content-Security-Policy"] = "default-src 'none'; sandbox"
    record(
        request,
        action="documents.downloaded",
        target=doc,
        metadata={"scan_status": doc.scan_status, "via": via},
    )
    return response


@login_required
@never_cache
@require_http_methods(["GET", "HEAD"])
def download(request, pk):
    # The same rate bound as the signed route. Without it the throttle below was decorative: a
    # compromised session that wanted to drain a case file simply used this URL instead.
    if not throttle.allow(request, "documents_download", **DOWNLOAD_THROTTLE):
        return error_429(request)
    doc = get_object_or_404(PrivateDocument.objects.alive().select_related("owner"), pk=pk)
    return _serve(request, doc, via="direct")


@login_required
@never_cache
@require_http_methods(["GET", "HEAD"])
def signed_download(request, token: str):
    """
    Deliver a file through a signed, time-limited, account-bound link (REQ-DOC-02).

    The link adds three constraints and removes none: it expires, it cannot be forged, and it is
    inert in anybody else's browser. The object-level policy still runs in ``_serve``, so a link
    that leaks into an e-mail thread or a proxy log grants nothing at all.
    """
    if not throttle.allow(request, "documents_download", **DOWNLOAD_THROTTLE):
        return error_429(request)
    try:
        doc = services.resolve_download_token(token, request.user)
    except SignatureExpired:
        # Say so plainly and send the reader back where a fresh link is waiting. Showing "not
        # found" for a document that exists would be a lie a user cannot act on.
        messages.error(
            request,
            _("Ce lien temporaire a expiré (validité %(n)d minutes). En voici un nouveau.")
            % {"n": services.DOWNLOAD_LINK_MINUTES},
        )
        return redirect(_expired_link_target(request.user, token))
    except BadSignature:
        raise Http404 from None
    return _serve(request, doc, via="signed_link")


def _expired_link_target(user, token: str) -> str:
    document_id = services.peek_expired_token(token)
    if document_id:
        requirement = DocumentRequirement.objects.readable_by(user).filter(versions__document_id=document_id).first()
        if requirement is not None:
            return reverse("documents:requirement", args=[requirement.pk])
    return reverse("documents:index")


# ---------------------------------------------------------------------------------------------
# Loose personal files (kept: nothing already uploaded may become unreachable)
# ---------------------------------------------------------------------------------------------
def _breadcrumb_register() -> dict:
    return {"label": _("Mes pièces"), "url": reverse("documents:index")}


@login_required
@never_cache
@require_http_methods(["GET", "POST"])
def upload(request):
    as_json = request.method == "POST" and _depot_json(request)
    if not services.user_may_upload(request.user):
        if as_json:
            return _depot_answer(
                "terms",
                _(
                    "Le dépôt de pièces est réservé aux comptes ayant accepté les Conditions d’utilisation et la "
                    "Privacy Policy."
                ),
            )
        return render(
            request,
            "documents/terms_required.html",
            _portal_shell(request, {}, _breadcrumb_register()),
            status=403,
        )
    if request.method == "POST":
        if not throttle.allow(request, "documents_upload", **UPLOAD_THROTTLE):
            return _depot_throttled() if as_json else error_429(request)
        form = DocumentUploadForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            doc = services.store_upload(
                request.user,
                form.cleaned_data["file"],
                form.cleaned_data["kind"],
                form.cleaned_data.get("description", ""),
                organisation=form.cleaned_data.get("organisation"),
                request=request,
            )
            if doc.is_infected:
                blocked = _("Le fichier a été bloqué par l’analyse antivirus et n’a pas été conservé.")
                if as_json:
                    return _depot_answer("infected", blocked)
                messages.error(request, blocked)
            else:
                if as_json:
                    return _depot_answer("filed", _("Document téléversé."), next=reverse("documents:index"))
                messages.success(request, _("Document téléversé."))
            return redirect("documents:index")
        if as_json:
            return _depot_refusal(form)
    else:
        form = DocumentUploadForm(user=request.user)
    return render(
        request,
        "documents/upload.html",
        _portal_shell(request, {"form": form}, _breadcrumb_register(), {"label": _("Téléverser"), "url": ""}),
    )


@login_required
@require_POST
def delete(request, pk):
    doc = get_object_or_404(PrivateDocument.objects.alive(), pk=pk)
    # The policy refuses a file that answers a requirement: evidence in a case file is superseded
    # by a new version or purged by retention, never quietly removed by its uploader.
    require(request.user, "delete", doc)
    services.soft_delete(doc, request=request)
    messages.success(request, _("Document supprimé."))
    return redirect("documents:index")


def may_download(user, doc) -> bool:
    """Small helper for sibling apps that need to know before they draw a link."""
    return can(user, "download", doc)
