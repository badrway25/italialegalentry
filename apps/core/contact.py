"""
The site's public telephone channels — V5.19, owner-confirmed on 29 October 2026 (lane v519-k).

Two channels, stored ONCE in the site's settings (``core.models.SiteSettings``: ``freephone_number`` and
``whatsapp_number``; their defaults and the fallback before migrations are ``settings.ILE``), and given to every
template by the context processor (``site.channels``, ``core.context_processors.site``). A template never writes a
number: it reads ``digits``, ``label`` and ``tel_url`` — and, for WhatsApp, ``url`` — from here.

* the Numero Verde, a telephone line: ``800642015`` → «800 642 015», ``tel:800642015`` — a public toll-free number,
  its default written in ``settings.ILE["FREEPHONE_NUMBER"]``;
* WhatsApp, a messaging channel: ``+<digits>`` → «+39 3xx xxx xxxx», ``https://wa.me/<digits>`` (wa.me takes the
  international number with no «+», no space, no punctuation), and ``tel:+<digits>`` where a call is meant. The
  owner-confirmed WhatsApp number is configured outside the repository (V5.19/V5.20, option B): the back office holds
  it, and its default is the environment's ``ILE_WHATSAPP_NUMBER`` (``settings.ILE["WHATSAPP_NUMBER"]``, blank unless
  set; ``default_whatsapp_number``). No file of the repository writes it; the tests use Ofcom's fictional
  +44 7700 900123.

The label is the owner's grouping: a national number in groups of three; an Italian mobile as «+39», then 3-3-4;
another country's number as its code, then groups of three.
A blank value — in the back office, or ``ILE_WHATSAPP_NUMBER`` unset — withdraws the channel: the surfaces then draw
nothing, never an empty link.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

_NATIONAL = re.compile(r"^\d{6,11}$")
_INTERNATIONAL = re.compile(r"^\+\d{8,15}$")
_SEPARATORS = re.compile(r"[\s().-]")


@dataclass(frozen=True)
class Channel:
    """One public channel: what a template needs, and nothing it would have to compute."""

    #: the canonical digits («800642015», «+447700900123»)
    digits: str
    #: the visible grouping («800 642 015», «+44 770 090 0123») — the same in every language
    label: str
    #: the telephone link («tel:800642015», «tel:+447700900123»)
    tel_url: str
    #: the channel's own link: the tel: link for a telephone line, the wa.me link for WhatsApp
    url: str


def canonical(value: str) -> str:
    """The digits of a number as typed in the back office (spaces, dots, dashes, brackets dropped)."""
    return _SEPARATORS.sub("", value or "")


def _groups(digits: str, sizes: tuple[int, ...]) -> list[str]:
    parts, start = [], 0
    for size in sizes:
        if start >= len(digits):
            break
        parts.append(digits[start : start + size])
        start += size
    if start < len(digits):
        parts[-1] += digits[start:]
    return parts


def national_label(digits: str) -> str:
    """«800642015» → «800 642 015»: groups of three, a short tail joining the last group."""
    sizes = (3,) * (len(digits) // 3)
    return " ".join(_groups(digits, sizes or (len(digits),)))


def international_label(number: str) -> str:
    """«+39 3xx xxx xxxx» (Italy: 3-3-4); another country: its code, then groups of three («+447700900123» →
    «+44 770 090 0123»)."""
    if number.startswith("+39"):
        return " ".join(["+39", *_groups(number[3:], (3, 3, 4))])
    body = number[1:]
    code, rest = body[:2], body[2:]
    return " ".join([f"+{code}", national_label(rest)])


def default_whatsapp_number() -> str:
    """
    The default of ``SiteSettings.whatsapp_number`` (V5.20, option B): ``settings.ILE["WHATSAPP_NUMBER"]``, which the
    environment's ``ILE_WHATSAPP_NUMBER`` gives — blank unless configured, never a value written in the repository.
    Read when a row is made (``SiteSettings.load()``, the back office); afterwards the back office holds the number.
    A callable, so that ``makemigrations`` writes its name, never the number of the machine it runs on: migration
    core 0003 names it.
    """
    from django.conf import settings

    return settings.ILE["WHATSAPP_NUMBER"]


def validate_national_number(value: str) -> None:
    if value and not _NATIONAL.match(canonical(value)):
        raise ValidationError(_("Indicare un numero nazionale di 6–11 cifre (es. 800 xxx xxx)."))


def validate_international_number(value: str) -> None:
    if value and not _INTERNATIONAL.match(canonical(value)):
        raise ValidationError(
            _("Indicare il numero in formato internazionale, con il prefisso (es. +39 3xx xxx xxxx).")
        )


def freephone(value: str) -> Channel | None:
    digits = canonical(value)
    if not _NATIONAL.match(digits):
        return None
    tel = f"tel:{digits}"
    return Channel(digits=digits, label=national_label(digits), tel_url=tel, url=tel)


def whatsapp(value: str) -> Channel | None:
    digits = canonical(value)
    if not _INTERNATIONAL.match(digits):
        return None
    return Channel(
        digits=digits,
        label=international_label(digits),
        tel_url=f"tel:{digits}",
        url=f"https://wa.me/{digits[1:]}",
    )


def public_channels(site_settings=None) -> dict[str, Channel | None]:
    """``{"freephone": Channel | None, "whatsapp": Channel | None}`` from the site's settings (or settings.ILE)."""
    from django.conf import settings

    if site_settings is not None:
        freephone_value, whatsapp_value = site_settings.freephone_number, site_settings.whatsapp_number
    else:
        freephone_value, whatsapp_value = settings.ILE["FREEPHONE_NUMBER"], settings.ILE["WHATSAPP_NUMBER"]
    return {"freephone": freephone(freephone_value), "whatsapp": whatsapp(whatsapp_value)}
