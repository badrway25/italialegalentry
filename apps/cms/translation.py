"""
Translation resolution for CMS content (gate G10).

``resolve(obj, lang)`` returns ``(translation_row, effective_language, is_fallback)`` choosing the
PUBLISHED row for the requested language, else the PUBLISHED row of the fallback language, else
None. Unapproved translations are never rendered publicly.
"""

from __future__ import annotations

from django.conf import settings

from cms.models import TranslationStatus


def resolve(obj, lang: str, related_name: str = "translations", public_only: bool = True):
    lang = (lang or settings.LANGUAGE_CODE).split("-")[0]
    fallback = settings.CONTENT_FALLBACK_LANGUAGE
    rows = list(getattr(obj, related_name).all())
    if public_only:
        rows = [r for r in rows if r.status == TranslationStatus.PUBLISHED]
    by_lang = {r.language: r for r in rows}
    if lang in by_lang:
        return by_lang[lang], lang, False
    if fallback in by_lang:
        return by_lang[fallback], fallback, True
    return None, lang, False


def translation_matrix(obj, related_name: str = "translations") -> dict[str, str]:
    """{lang: status} for the admin overview, MISSING where no row exists."""
    rows = {r.language: r.status for r in getattr(obj, related_name).all()}
    return {code: rows.get(code, TranslationStatus.MISSING) for code, _ in settings.LANGUAGES}
