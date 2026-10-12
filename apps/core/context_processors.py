from __future__ import annotations

from django.conf import settings
from django.urls import translate_url
from django.utils import translation

from core import gates
from core.models import SiteSettings


def _language_links(request):
    current = translation.get_language() or settings.LANGUAGE_CODE
    path = request.get_full_path()
    links = []
    for code, name in settings.LANGUAGES:
        try:
            url = translate_url(path, code)
        except Exception:  # pragma: no cover - defensive
            url = f"/{code}/"
        links.append(
            {
                "code": code,
                "name": name,
                "url": url,
                "active": code == current,
                "dir": "rtl" if code in settings.RTL_LANGUAGES else "ltr",
            }
        )
    return links


def site(request):
    lang = translation.get_language() or settings.LANGUAGE_CODE
    try:
        site_settings = SiteSettings.load()
    except Exception:  # pragma: no cover - before migrations
        site_settings = None
    return {
        "site": {
            "project_name": settings.ILE["PROJECT_NAME"],
            "promoter": settings.ILE["PROMOTER"],
            "contact_email": (
                site_settings.public_contact_email if site_settings else settings.ILE["PUBLIC_CONTACT_EMAIL"]
            ),
            "version_label": (site_settings.version_label if site_settings else settings.ILE["VERSION_LABEL"]),
            "content_verified_on": (site_settings.content_verified_on if site_settings else None),
            "settings": site_settings,
            "lang": lang,
            "dir": "rtl" if lang in settings.RTL_LANGUAGES else "ltr",
            "is_rtl": lang in settings.RTL_LANGUAGES,
            "languages": _language_links(request),
            "fallback_language": settings.CONTENT_FALLBACK_LANGUAGE,
        },
        "gates": gates.snapshot(),
    }
