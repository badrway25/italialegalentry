"""Thin views — logic lives in ``news.services``."""

from __future__ import annotations

from urllib.parse import urlencode

from django.contrib import messages
from django.core.paginator import Paginator
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import translation
from django.utils.translation import gettext as _
from django.views.decorators.http import require_http_methods, require_POST

from accounts.middleware import require_second_factor
from core import gates, throttle
from news import services
from news.editorial import blocks
from news.forms import NewsletterForm
from news.models import Article, NewsCategory

PAGE_SIZE = 10
THROTTLE_SCOPE = "newsletter"


def _current_language() -> str:
    return (translation.get_language() or "fr").split("-")[0]


def _newsletter_context(request, form: NewsletterForm | None = None) -> dict:
    enabled = gates.newsletter_enabled()
    forms_gate = gates.public_forms_enabled()
    return {
        "newsletter_enabled": enabled,
        "newsletter_forms_open": enabled and forms_gate.open,
        "newsletter_form": (form or NewsletterForm()) if enabled and forms_gate.open else None,
    }


def _index_context(request, form: NewsletterForm | None = None) -> dict:
    lang = _current_language()
    category = services.category_by_slug(request.GET.get("categorie"))
    articles = services.public_articles(category)
    paginator = Paginator(articles, PAGE_SIZE)
    page_obj = paginator.get_page(request.GET.get("page"))
    context = {
        "phase3": gates.phase3_public(),
        "category": category,
        "categories": list(NewsCategory.objects.all()),
        "page_obj": page_obj,
        "articles": [(article, article.texts(lang)) for article in page_obj.object_list],
        "query": urlencode({"categorie": category.slug}) if category else "",
        "breadcrumbs": [{"label": _("Actualités"), "url": ""}],
        "lang": lang,
    }
    context.update(_newsletter_context(request, form))
    return context


@require_http_methods(["GET"])
def index(request):
    return render(request, "news/index.html", _index_context(request))


@require_http_methods(["GET"])
def detail(request, slug: str):
    lang = _current_language()
    article = (
        Article.objects.with_dates()
        .select_related("category", "hero_image", "og_image", "editor")
        .prefetch_related("translations")
        .filter(slug=slug)
        .first()
    )
    if article is None:
        raise Http404
    preview = False
    if not article.is_live():
        user = request.user
        if not (user.is_authenticated and user.is_staff and user.has_perm("news.view_article")):
            raise Http404
        # a staff preview of an unpublished article: the second-factor policy first (accounts.middleware)
        require_second_factor(request)
        preview = True
    texts = article.texts(lang)
    context = {
        "article": article,
        "texts": texts,
        "blocks": blocks(texts.body),
        "sources": article.source_links or [],
        "related": [(rel, rel.texts(lang)) for rel in services.related_articles(article)],
        "jsonld": services.article_jsonld(article, request, texts, lang),
        "share_image": article.share_image,
        "share_alt": article.share_image.alt(lang) if article.share_image else "",
        "hero_alt": "" if not article.hero_image or article.hero_image.is_decorative else article.hero_image.alt(lang),
        "preview": preview,
        "noindex": preview,
        "phase3": gates.phase3_public(),
        "breadcrumbs": [
            {"label": _("Actualités"), "url": reverse("news:index")},
            {"label": texts.title, "url": ""},
        ],
        "lang": lang,
    }
    return render(request, "news/detail.html", context)


@require_POST
def newsletter_subscribe(request):
    if not gates.newsletter_enabled():
        raise Http404
    if not gates.public_forms_enabled().open:
        # Gate G2 closed: nothing is persisted, nothing is sent (docs/LEGAL_AND_PUBLICATION_GATES.md).
        return render(request, "news/index.html", _index_context(request), status=403)
    if not throttle.allow(request, THROTTLE_SCOPE):
        return render(request, "errors/429.html", status=429)
    form = NewsletterForm(request.POST)
    success_url = reverse("news:index") + "#newsletter"
    if form.is_spam:
        # Honeypot / timing failure: behave exactly like a success without saving anything.
        messages.success(request, _("Merci. Si l’adresse est valide, un e-mail de confirmation vous a été envoyé."))
        return HttpResponseRedirect(success_url)
    if not form.is_valid():
        # Django 5.2 marks invalid controls with aria-invalid / aria-describedby automatically.
        return render(request, "news/index.html", _index_context(request, form), status=200)
    services.subscribe(request, form.cleaned_data["email"], _current_language())
    messages.success(request, _("Merci. Si l’adresse est valide, un e-mail de confirmation vous a été envoyé."))
    return HttpResponseRedirect(success_url)
