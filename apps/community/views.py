"""
Forum Virtuel views — thin. Gate order: flag (404) → authentication (login) → membership (403).

Anonymous visitors with the flag on see only the prescribed teaser (``p3.virtual_forum.*``).
"""

from __future__ import annotations

from functools import wraps

from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

from accounts.middleware import require_second_factor
from accounts.permissions import require
from community import conf, services
from community.forms import (
    DiscussionForm,
    DiscussionModerationForm,
    JoinForm,
    PostForm,
    PostModerationForm,
    ReportForm,
)
from community.models import Discussion, MembershipStatus, Post, Room
from core import gates, throttle
from core.views import error_429


def _flag_or_404() -> None:
    if not gates.virtual_forum_enabled():
        raise Http404


def member_required(view):
    """Flag → login → approved membership (moderators pass without membership)."""

    @wraps(view)
    def wrapper(request, *args, **kwargs):
        _flag_or_404()
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())
        membership = services.membership_of(request.user)
        moderator = services.is_moderator(request.user)
        if moderator:
            # a moderator reads hidden and pending posts and moderates: a staff privilege, the second factor first
            require_second_factor(request)
        if not moderator and (membership is None or membership.status != MembershipStatus.APPROVED):
            raise PermissionDenied
        request.community_membership = membership if (membership and membership.is_approved) else None
        request.community_moderator = moderator
        return view(request, *args, **kwargs)

    return wrapper


def _crumbs(*items):
    base = [{"label": _("Forum Virtuel"), "url": reverse("community:index")}]
    return base + [{"label": label, "url": url} for label, url in items]


def index(request):
    _flag_or_404()
    user = request.user
    if not user.is_authenticated:
        return render(request, "community/landing.html", {"state": "anonymous", "breadcrumbs": _crumbs()})
    membership = services.membership_of(user)
    moderator = services.is_moderator(user)
    if moderator:
        require_second_factor(request)
    if not moderator and (membership is None or not membership.is_approved):
        state = "none" if membership is None else membership.status
        return render(
            request,
            "community/landing.html",
            {"state": state, "membership": membership, "breadcrumbs": _crumbs()},
        )
    rooms = services.rooms_for(membership, moderator)
    context = {
        "membership": membership,
        "moderator": moderator,
        "rooms": rooms,
        "calendar": services.upcoming_calendar(membership, moderator)[:5],
        "breadcrumbs": _crumbs(),
    }
    return render(request, "community/index.html", context)


def join(request):
    _flag_or_404()
    if not request.user.is_authenticated:
        return redirect_to_login(request.get_full_path())
    if services.membership_of(request.user) is not None:
        return redirect("community:index")
    crumbs = _crumbs((_("Demande d’accès"), ""))
    gate = gates.public_forms_enabled()
    if not gate.open:
        return render(request, "community/join.html", {"forms_closed": True, "breadcrumbs": crumbs})
    from consents.models import ConsentPurpose
    from consents.services import consent_text_for

    consent_text = consent_text_for(ConsentPurpose.COMMUNITY).text
    if request.method == "POST":
        limits = conf.join_throttle()
        if not throttle.allow(request, "community_join", limits["limit"], limits["window_seconds"]):
            return error_429(request)
        form = JoinForm(request.POST, consent_text=consent_text)
        if form.is_valid():
            services.request_membership(
                request,
                request.user,
                category=form.cleaned_data["category"],
                organisation=form.cleaned_data["organisation"],
                show_name=form.cleaned_data["show_name"],
                show_organisation=form.cleaned_data["show_organisation"],
            )
            messages.success(
                request, _("Votre demande d’accès a été enregistrée. Elle sera examinée par la modération.")
            )
            return redirect("community:index")
    else:
        form = JoinForm(consent_text=consent_text)
    return render(request, "community/join.html", {"form": form, "breadcrumbs": crumbs})


@member_required
def room_detail(request, slug):
    room = get_object_or_404(Room, slug=slug)
    require(request.user, "view", room)
    membership, moderator = request.community_membership, request.community_moderator
    discussions = services.visible_discussions(room, membership, moderator)
    page_obj = Paginator(discussions, 20).get_page(request.GET.get("page"))
    can_post = membership is not None
    if request.method == "POST" and not can_post:
        raise PermissionDenied
    form = None
    if can_post:
        if request.method == "POST":
            limits = conf.post_throttle()
            if not throttle.allow(request, "community_post", limits["limit"], limits["window_seconds"]):
                return error_429(request)
            form = DiscussionForm(request.POST)
            if form.is_valid():
                discussion, post = services.create_discussion(
                    request, room, membership, title=form.cleaned_data["title"], body=form.cleaned_data["body"]
                )
                if post.is_visible:
                    messages.success(request, _("Discussion créée."))
                else:
                    messages.info(request, _("Discussion créée : votre message sera publié après modération."))
                return redirect("community:discussion", pk=discussion.pk)
        else:
            form = DiscussionForm()
    context = {
        "room": room,
        "page_obj": page_obj,
        "form": form,
        "membership": membership,
        "moderator": moderator,
        "breadcrumbs": _crumbs((room.name_fr, "")),
    }
    return render(request, "community/room.html", context)


@member_required
def discussion_detail(request, pk):
    discussion = get_object_or_404(Discussion.objects.select_related("room"), pk=pk)
    require(request.user, "view", discussion)
    membership, moderator = request.community_membership, request.community_moderator
    posts = services.visible_posts(discussion, membership, moderator)
    can_reply = membership is not None and discussion.is_open
    if request.method == "POST" and not can_reply:
        raise PermissionDenied
    form = None
    if can_reply:
        if request.method == "POST":
            limits = conf.post_throttle()
            if not throttle.allow(request, "community_post", limits["limit"], limits["window_seconds"]):
                return error_429(request)
            form = PostForm(request.POST)
            if form.is_valid():
                post = services.create_post(request, discussion, membership, body=form.cleaned_data["body"])
                if post.is_visible:
                    messages.success(request, _("Réponse publiée."))
                else:
                    messages.info(request, _("Votre réponse sera publiée après modération."))
                return redirect("community:discussion", pk=discussion.pk)
        else:
            form = PostForm()
    context = {
        "discussion": discussion,
        "room": discussion.room,
        "posts": posts,
        "form": form,
        "membership": membership,
        "moderator": moderator,
        "moderation_form": DiscussionModerationForm() if moderator else None,
        "post_moderation_form": PostModerationForm() if moderator else None,
        "breadcrumbs": _crumbs(
            (discussion.room.name_fr, reverse("community:room", kwargs={"slug": discussion.room.slug})),
            (discussion.title, ""),
        ),
    }
    return render(request, "community/discussion.html", context)


@member_required
def post_edit(request, pk):
    post = get_object_or_404(Post.objects.select_related("discussion__room"), pk=pk)
    require(request.user, "edit", post)
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            services.edit_post(request, post, body=form.cleaned_data["body"])
            messages.success(request, _("Message modifié."))
            return redirect("community:discussion", pk=post.discussion_id)
    else:
        form = PostForm(initial={"body": post.body})
    context = {
        "form": form,
        "post": post,
        "breadcrumbs": _crumbs(
            (post.discussion.title, reverse("community:discussion", kwargs={"pk": post.discussion_id})),
            (_("Modifier le message"), ""),
        ),
    }
    return render(request, "community/post_edit.html", context)


@member_required
def post_report(request, pk):
    post = get_object_or_404(Post.objects.select_related("discussion__room"), pk=pk)
    require(request.user, "report", post)
    if request.method == "POST":
        limits = conf.report_throttle()
        if not throttle.allow(request, "community_report", limits["limit"], limits["window_seconds"]):
            return error_429(request)
        form = ReportForm(request.POST)
        if form.is_valid():
            services.report_post(request, post, request.community_membership, reason=form.cleaned_data["reason"])
            messages.success(request, _("Merci, votre signalement a été transmis à la modération."))
            return redirect("community:discussion", pk=post.discussion_id)
    else:
        form = ReportForm()
    context = {
        "form": form,
        "post": post,
        "breadcrumbs": _crumbs(
            (post.discussion.title, reverse("community:discussion", kwargs={"pk": post.discussion_id})),
            (_("Signaler un message"), ""),
        ),
    }
    return render(request, "community/report.html", context)


@member_required
@require_POST
def post_moderate(request, pk):
    post = get_object_or_404(Post.objects.select_related("discussion"), pk=pk)
    require(request.user, "moderate", post)
    form = PostModerationForm(request.POST)
    if form.is_valid():
        services.moderate_post(
            post, request.user, form.cleaned_data["action"], form.cleaned_data["note"], request=request
        )
        messages.success(request, _("Action de modération enregistrée."))
    else:
        messages.error(request, _("Action de modération invalide."))
    return redirect("community:discussion", pk=post.discussion_id)


@member_required
@require_POST
def discussion_moderate(request, pk):
    discussion = get_object_or_404(Discussion, pk=pk)
    require(request.user, "moderate", discussion)
    form = DiscussionModerationForm(request.POST)
    if form.is_valid():
        services.moderate_discussion(
            discussion, request.user, form.cleaned_data["action"], form.cleaned_data["note"], request=request
        )
        messages.success(request, _("Action de modération enregistrée."))
    else:
        messages.error(request, _("Action de modération invalide."))
    return redirect("community:discussion", pk=discussion.pk)


@member_required
def calendar(request):
    entries = services.upcoming_calendar(request.community_membership, request.community_moderator)
    return render(
        request, "community/calendar.html", {"entries": entries, "breadcrumbs": _crumbs((_("Calendrier"), ""))}
    )


@member_required
def initiatives(request):
    items = services.initiatives_for(request.community_membership, request.community_moderator)
    return render(
        request, "community/initiatives.html", {"initiatives": items, "breadcrumbs": _crumbs((_("Initiatives"), ""))}
    )
