"""
News services: editorial workflow (with permission and audit), public querysets, JSON-LD,
newsletter double opt-in subscription (separate, revocable consent — never linked to other consents).
"""

from __future__ import annotations

import json
import logging
import secrets
from dataclasses import dataclass

from django.conf import settings
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.urls import reverse
from django.utils.translation import gettext as _

from audit.services import record as audit_record
from cms.models import PublicationStatus
from consents.models import ConsentPurpose, NewsletterSubscription
from consents.services import record_consent
from core import clock
from news.models import Article, NewsCategory
from notifications.services import notify_forms_inbox, queue_email

log = logging.getLogger("ile.news")

PUBLISH_PERMISSION = "news.publish_article"


class WorkflowError(ValidationError):
    """Raised when a transition is not allowed from the current status."""


# ---------------------------------------------------------------------------------------------
# Public querysets
# ---------------------------------------------------------------------------------------------


def public_articles(category: NewsCategory | None = None):
    qs = Article.objects.public()
    if category is not None:
        qs = qs.filter(category=category)
    return qs


def category_by_slug(slug: str | None) -> NewsCategory | None:
    if not slug:
        return None
    return NewsCategory.objects.filter(slug=slug).first()


def related_articles(article: Article, limit: int = 3):
    return Article.objects.public().filter(related_to=article)[:limit]


def latest_articles(limit: int = 3):
    """Used by the homepage block (pages app) — live articles only."""
    return Article.objects.public()[:limit]


# ---------------------------------------------------------------------------------------------
# Editorial workflow
# ---------------------------------------------------------------------------------------------


def can_publish(user) -> bool:
    return bool(user and getattr(user, "is_active", False) and (user.is_superuser or user.has_perm(PUBLISH_PERMISSION)))


def _transition(article: Article, allowed: tuple[str, ...], new_status: str, action: str) -> None:
    if article.status not in allowed:
        raise WorkflowError(
            _("Transition « %(action)s » impossible depuis l’état « %(status)s ».")
            % {"action": action, "status": article.get_status_display()}
        )
    article.status = new_status


def submit_for_review(article: Article, user, request=None) -> Article:
    _transition(article, (PublicationStatus.DRAFT,), PublicationStatus.REVIEW, "review")
    article.editor = user if getattr(user, "is_authenticated", False) else article.editor
    article.save()
    audit_record(request, action="news.article.submitted_for_review", target=article, actor=user)
    return article


def publish(article: Article, user, request=None) -> Article:
    """Publish (or schedule when ``publish_at`` is in the future). Requires ``news.publish_article``."""
    if not can_publish(user):
        raise PermissionDenied(_("Seuls les utilisateurs autorisés peuvent publier des articles."))
    allowed = (PublicationStatus.REVIEW, PublicationStatus.SCHEDULED, PublicationStatus.ARCHIVED)
    now = clock.now()
    if article.publish_at and article.publish_at > now:
        _transition(article, allowed, PublicationStatus.SCHEDULED, "publish")
    else:
        _transition(article, allowed, PublicationStatus.PUBLISHED, "publish")
        if article.status == PublicationStatus.PUBLISHED and not article.published_at:
            article.published_at = now
    article.reviewer = user
    article.last_reviewed_at = now
    article.editor = user
    article.save()
    audit_record(
        request,
        action="news.article.published",
        target=article,
        actor=user,
        metadata={"status": article.status, "version": article.version},
    )
    return article


def archive(article: Article, user, request=None) -> Article:
    allowed = (PublicationStatus.PUBLISHED, PublicationStatus.SCHEDULED, PublicationStatus.REVIEW)
    _transition(article, allowed, PublicationStatus.ARCHIVED, "archive")
    article.editor = user if getattr(user, "is_authenticated", False) else article.editor
    article.save()
    audit_record(request, action="news.article.archived", target=article, actor=user)
    return article


def back_to_draft(article: Article, user, request=None) -> Article:
    allowed = (PublicationStatus.REVIEW, PublicationStatus.ARCHIVED)
    _transition(article, allowed, PublicationStatus.DRAFT, "draft")
    article.editor = user if getattr(user, "is_authenticated", False) else article.editor
    article.save()
    audit_record(request, action="news.article.back_to_draft", target=article, actor=user)
    return article


# ---------------------------------------------------------------------------------------------
# SEO — JSON-LD (schema.org/Article). Author/publisher is the promoter, never a government body.
# ---------------------------------------------------------------------------------------------

_JSON_ESCAPES = {ord(">"): "\\u003E", ord("<"): "\\u003C", ord("&"): "\\u0026"}


def article_jsonld(article: Article, request, texts=None, language: str | None = None) -> str:
    texts = texts or article.texts(language)
    organisation = {"@type": "Organization", "name": settings.ILE["PROMOTER"]}
    url = request.build_absolute_uri(article.get_absolute_url())
    data = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": texts.title[:110],
        "description": texts.seo_description,
        "inLanguage": texts.language,
        "mainEntityOfPage": {"@type": "WebPage", "@id": url},
        "url": url,
        "author": organisation,
        "publisher": organisation,
        "articleSection": article.category.name(language),
    }
    if article.date_published:
        data["datePublished"] = article.date_published.isoformat()
    if article.date_modified:
        data["dateModified"] = article.date_modified.isoformat()
    image = article.share_image
    if image and image.file:
        data["image"] = [request.build_absolute_uri(image.file.url)]
    return json.dumps(data, ensure_ascii=False).translate(_JSON_ESCAPES)


# ---------------------------------------------------------------------------------------------
# Newsletter — double opt-in (consent purpose NEWSLETTER only, never tied to other consents)
# ---------------------------------------------------------------------------------------------


@dataclass(frozen=True)
class SubscriptionOutcome:
    subscription: NewsletterSubscription
    state: str  # "created" | "pending_resent" | "resubscribed" | "already_active"


def _confirmation_context(request, sub: NewsletterSubscription) -> dict:
    return {
        "confirm_url": request.build_absolute_uri(
            reverse("consents:newsletter_confirm", kwargs={"token": sub.confirm_token})
        ),
        "unsubscribe_url": request.build_absolute_uri(
            reverse("consents:newsletter_unsubscribe", kwargs={"token": sub.unsubscribe_token})
        ),
        "contact_email": settings.ILE["PUBLIC_CONTACT_EMAIL"],
    }


def _queue_confirmation(request, sub: NewsletterSubscription) -> None:
    queue_email(
        to_email=sub.email,
        subject=_("Confirmez votre inscription à la lettre d’information"),
        template="newsletter_confirm",
        context=_confirmation_context(request, sub),
        reference=f"consents.NewsletterSubscription:{sub.pk}",
    )


@transaction.atomic
def subscribe(request, email: str, language: str | None = None) -> SubscriptionOutcome:
    """
    Register a newsletter opt-in request and queue the confirmation e-mail.

    The caller (view) is responsible for the gates (G2 forms, newsletter flag), throttle and the
    honeypot. Nothing personal is written to logs or to the forms inbox notification.
    """
    email = email.lower().strip()
    language = (language or settings.LANGUAGE_CODE).split("-")[0]
    sub = NewsletterSubscription.objects.select_for_update().filter(email=email).first()

    if sub is None:
        consent = record_consent(request, ConsentPurpose.NEWSLETTER, email, language=language)
        sub = NewsletterSubscription.objects.create(email=email, language=language, consent=consent)
        state = "created"
    elif sub.is_active:
        return SubscriptionOutcome(sub, "already_active")
    elif sub.unsubscribed_at is not None:
        consent = record_consent(request, ConsentPurpose.NEWSLETTER, email, language=language)
        sub.consent = consent
        sub.language = language
        sub.unsubscribed_at = None
        sub.confirmed_at = None
        sub.confirm_token = secrets.token_urlsafe(32)
        sub.unsubscribe_token = secrets.token_urlsafe(32)
        sub.save()
        state = "resubscribed"
    else:
        sub.language = language
        sub.save(update_fields=["language", "updated_at"])
        state = "pending_resent"

    _queue_confirmation(request, sub)
    audit_record(request, action=f"newsletter.{state}", target=sub, metadata={"language": language})
    notify_forms_inbox(
        subject=_("Nouvelle demande d’inscription à la lettre d’information"),
        template="newsletter_inbox_notice",
        context={"state": state, "language": language, "requested_at": clock.now()},
        reference=f"consents.NewsletterSubscription:{sub.pk}",
    )
    log.info("newsletter opt-in request (%s)", state)
    return SubscriptionOutcome(sub, state)
