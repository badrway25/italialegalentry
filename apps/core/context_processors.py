from __future__ import annotations

from django.conf import settings
from django.urls import translate_url
from django.utils import translation

from core import contact, gates
from core.models import SiteSettings

#: The language control's flag for each language — the ONE place to change it (static/img/flags/PROVENANCE.md).
#: English is drawn with the United Kingdom's flag: its catalogue is written in British spelling (docs/I18N_RTL.md
#: §4.2, «britannico istituzionale»: organisation, authorised). Arabic is NOT a country: the locale is the generic `ar`
#: (no region), named «العربية», written in Modern Standard Arabic (§4.2) — so it draws a neutral language mark, the
#: letter ع on a mineral plate in the flags' own 3:2 frame (ar.svg), never Morocco's flag (V5.31 art pass, 11 Nov
#: 2026, B6; the evidence is in static/img/flags/PROVENANCE.md).
LANGUAGE_FLAGS = {"it": "it", "fr": "fr", "en": "gb", "ar": "ar"}


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
                "flag": f"img/flags/{LANGUAGE_FLAGS[code]}.svg" if code in LANGUAGE_FLAGS else "",
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
            # V5.19: the public telephone channels — {"freephone", "whatsapp"}: digits, label, tel_url, url
            # (core.contact)
            "channels": contact.public_channels(site_settings),
            # the release, for the page's metadata (`<meta name="generator">`) — never the footer, which says the phase
            "version_label": ((site_settings.version_label if site_settings else "") or settings.ILE["VERSION_LABEL"]),
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
