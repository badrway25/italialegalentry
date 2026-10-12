"""
Navigation template tags (design system) — ``{% load cms_nav %}``.

{% main_menu as menu %}          → tree of NavItem for the header (location "main")
{% footer_menu as items %}       → flat list of NavItem for the footer navigation column
{% brand %}                      → the trademark wordmark, always from the locked registry

Menu rows come from ``cms.MenuItem`` (back-office editable). When no visible row exists for a
location, a static fallback structure is used so the site is navigable from day one. Items are
filtered by publication gates (``requires_gate``) and feature flags (``requires_flag``); items
whose URL name is not (yet) resolvable are hidden, so a menu never links to a missing route.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from django import template
from django.db.utils import DatabaseError, ProgrammingError
from django.templatetags.static import static
from django.urls import NoReverseMatch, reverse
from django.utils import translation
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from cms import locked_content
from cms.models import MenuItem, MenuLocation
from core import flags, gates

register = template.Library()


@dataclass
class NavItem:
    id: str
    label: str
    url: str = ""
    description: str = ""
    children: list[NavItem] = field(default_factory=list)
    new_tab: bool = False
    is_current: bool = False
    is_section: bool = False


# ---------------------------------------------------------------------------------------------
# Gates
# ---------------------------------------------------------------------------------------------
_GATE_FUNCTIONS = {
    "phase3_public": gates.phase3_public,
    "virtual_forum": gates.virtual_forum_enabled,
    "forum_permanent_mode": gates.forum_permanent_mode,
    "forum_banner": gates.forum_banner_visible,
    "newsletter": gates.newsletter_enabled,
    "legal_pages": gates.legal_pages_available,
    "public_forms": lambda: gates.public_forms_enabled().open,
}


def gate_open(name: str) -> bool:
    """True when the named gate is open. Unknown names fall back to the feature-flag registry."""
    if not name:
        return True
    func = _GATE_FUNCTIONS.get(name)
    if func is not None:
        return bool(func())
    return flags.is_enabled(name)


def resolve_url(url_name: str, url: str = "") -> str:
    """Reverse ``url_name`` if possible; otherwise the manual ``url``; "" when nothing resolves."""
    if url_name:
        try:
            return reverse(url_name)
        except NoReverseMatch:
            return ""
    return url or ""


# ---------------------------------------------------------------------------------------------
# Static fallback (French source strings; translated through .po files)
# ---------------------------------------------------------------------------------------------
# (label, url_name, requires_gate, description, children)
_FALLBACK_MAIN: tuple = (
    (
        _("Personnes"),
        "pathways:index",
        "",
        _("Orientation, parcours réguliers et préparation avant le départ."),
        (
            (_("Votre parcours"), "pathways:index", ""),
            (_("Diplômes et titres"), "pathways:diplomas", "phase3_public"),
            (_("Formation"), "pathways:training", "phase3_public"),
            (_("Vivre en Italie"), "living:index", "phase3_public"),
            (_("Attention aux fraudes"), "pages:antifraud", "phase3_public"),
            (_("FAQ"), "faq:index", "phase3_public"),
            (_("Glossaire"), "glossary:index", "phase3_public"),
        ),
    ),
    (
        _("Entreprises"),
        "ecosystem:companies",
        "",
        _("Signalez les besoins professionnels de votre entreprise."),
        (
            (_("Besoins professionnels"), "enquiries:company_needs", ""),
            (_("Projet pilote"), "ecosystem:pilot", "phase3_public"),
        ),
    ),
    (_("Institutions"), "ecosystem:institutions", "phase3_public", "", ()),
    (_("Universités & Formation"), "ecosystem:universities", "phase3_public", "", ()),
    (_("Forum Vénétie–Maroc"), "forum:index", "", "", ()),
    (_("Actualités"), "news:index", "phase3_public", "", ()),
    (
        _("Projet"),
        "pages:project",
        "",
        _("Le projet, son promoteur et son réseau."),
        (
            (_("Italy Legal Entry"), "pages:project", ""),
            (_("AGAMI"), "pages:agami", ""),
            (_("Réseau"), "pages:network", ""),
            (_("Contact"), "pages:contact", ""),
        ),
    ),
)

_FALLBACK_FOOTER: tuple = (
    (_("Personnes"), "pathways:index", ""),
    (_("Entreprises"), "ecosystem:companies", ""),
    (_("Institutions"), "ecosystem:institutions", "phase3_public"),
    (_("Universités & Formation"), "ecosystem:universities", "phase3_public"),
    (_("Forum Vénétie–Maroc"), "forum:index", ""),
    (_("Actualités"), "news:index", "phase3_public"),
    (_("Projet"), "pages:project", ""),
    (_("Contact"), "pages:contact", ""),
)


def _slug(prefix: str, index: int) -> str:
    return f"{prefix}-{index}"


def _mark_current(item: NavItem, path: str, lang: str) -> None:
    home = f"/{lang}/"
    for child in item.children:
        child.is_current = bool(child.url) and child.url == path
    if item.url:
        if item.url == home:
            # A section whose own link is the home page is "current" only on the home page itself —
            # unless one of its children is the page being displayed.
            item.is_current = path == home or any(c.is_current for c in item.children)
        else:
            item.is_current = path == item.url or path.startswith(item.url) or any(c.is_current for c in item.children)
    else:
        item.is_current = any(c.is_current for c in item.children)


def _fallback_main() -> list[NavItem]:
    items: list[NavItem] = []
    for i, (label, url_name, gate, description, children) in enumerate(_FALLBACK_MAIN):
        if not gate_open(gate):
            continue
        url = resolve_url(url_name)
        kids = []
        for j, (c_label, c_url_name, c_gate) in enumerate(children):
            if not gate_open(c_gate):
                continue
            c_url = resolve_url(c_url_name)
            if c_url:
                kids.append(NavItem(id=_slug(f"nav-{i}", j), label=str(c_label), url=c_url))
        if not url and not kids:
            continue
        items.append(
            NavItem(
                id=_slug("nav", i),
                label=str(label),
                url=url,
                description=str(description),
                children=kids,
                is_section=bool(kids),
            )
        )
    return items


def _fallback_footer() -> list[NavItem]:
    items = []
    for i, (label, url_name, gate) in enumerate(_FALLBACK_FOOTER):
        if not gate_open(gate):
            continue
        url = resolve_url(url_name)
        if url:
            items.append(NavItem(id=_slug("footer-nav", i), label=str(label), url=url))
    return items


# ---------------------------------------------------------------------------------------------
# Database rows
# ---------------------------------------------------------------------------------------------
def _row_visible(row: MenuItem) -> bool:
    if not row.is_visible:
        return False
    if row.requires_flag and not flags.is_enabled(row.requires_flag):
        return False
    return gate_open(row.requires_gate)


def _rows(location: str) -> list[MenuItem]:
    try:
        return list(MenuItem.objects.filter(location=location).order_by("order", "id"))
    except (DatabaseError, ProgrammingError):  # pragma: no cover - before migrations
        return []


def _tree_from_rows(rows: list[MenuItem], lang: str, prefix: str) -> list[NavItem]:
    by_parent: dict[int | None, list[MenuItem]] = {}
    for row in rows:
        by_parent.setdefault(row.parent_id, []).append(row)
    items: list[NavItem] = []
    for row in by_parent.get(None, []):
        if not _row_visible(row):
            continue
        url = resolve_url(row.url_name, row.url)
        kids = []
        for child in by_parent.get(row.id, []):
            if not _row_visible(child):
                continue
            c_url = resolve_url(child.url_name, child.url)
            if c_url:
                kids.append(
                    NavItem(
                        id=f"{prefix}-{row.id}-{child.id}",
                        label=child.label(lang),
                        url=c_url,
                        description=child.description_fr,
                        new_tab=child.open_in_new_tab,
                    )
                )
        if not url and not kids:
            continue
        items.append(
            NavItem(
                id=f"{prefix}-{row.id}",
                label=row.label(lang),
                url=url,
                description=row.description_fr,
                children=kids,
                new_tab=row.open_in_new_tab,
                is_section=bool(kids),
            )
        )
    return items


def build_menu(location: str, lang: str | None = None, path: str = "") -> list[NavItem]:
    """
    Public helper (also used by tests): menu tree for a location with gates applied.

    The whole tree is built under ``translation.override(lang)`` so that reversed URLs carry the
    same language prefix as the labels: a menu rendered in Italian must link to ``/it/…``.
    """
    lang = (lang or translation.get_language() or "fr").split("-")[0]
    with translation.override(lang):
        rows = _rows(location)
        if rows:
            items = _tree_from_rows(rows, lang, f"nav-{location}")
        elif location == MenuLocation.MAIN:
            items = _fallback_main()
        elif location in (MenuLocation.FOOTER_1, "footer_nav"):
            items = _fallback_footer()
        else:
            items = []
    if path:
        for item in items:
            _mark_current(item, path, lang)
    return items


# ---------------------------------------------------------------------------------------------
# Tags
# ---------------------------------------------------------------------------------------------
@register.simple_tag(takes_context=True)
def main_menu(context) -> list[NavItem]:
    request = context.get("request")
    path = getattr(request, "path", "") if request else ""
    return build_menu(MenuLocation.MAIN, path=path)


@register.simple_tag(takes_context=True)
def footer_menu(context, location: str = MenuLocation.FOOTER_1) -> list[NavItem]:
    request = context.get("request")
    path = getattr(request, "path", "") if request else ""
    return build_menu(location, path=path)


@register.simple_tag(takes_context=True)
def site_context(context) -> dict:
    """
    The ``site`` dict from ``core.context_processors.site``. Some third-party views (django-allauth)
    put a ``django.contrib.sites.Site`` instance under the same ``site`` name, shadowing the
    processor; base.html re-binds the dict with ``{% site_context as site %}`` before using it.
    """
    current = context.get("site")
    if isinstance(current, dict) and "project_name" in current:
        return current
    from core.context_processors import site as site_processor

    return site_processor(context.get("request"))["site"]


@register.simple_tag
def brand(css_class: str = "brand__wordmark"):
    """The wordmark, sourced from the locked registry (p1.trademark.mark): «Italy Legal Entry™»."""
    mark = locked_content.text("p1.trademark.mark", "fr")
    # dir="ltr": the trademark sign must stay on the right of the name in Arabic pages, whatever class
    # the caller uses (« ™Italy Legal Entry » was rendered in the footer). lang="en": the mark is an
    # English name, and a screen reader on an Arabic page must not read it as Arabic.
    return format_html('<span class="{}" translate="no" dir="ltr" lang="en">{}</span>', css_class, mark)


@register.simple_tag
def brand_lockup(variant: str = "") -> str:
    """
    The official lock-up: the mark, the wordmark, the tagline — as the current site draws them.

    The wordmark is the locked trademark text (p1.trademark.mark), split into its three words only
    so the stylesheet can colour them green / navy / red as the official lock-up does. The text
    content of the element is the locked string, character for character: the spans add colour,
    not words.

    THE TAGLINE IS NOT RENDERED, and that is a decision, not an omission. The current site sets an
    English tagline under the wordmark; the client's own implementation document (p.7 §3.1) orders
    that exact string removed "everywhere, including the logo's alt/ARIA", it is in
    cms.forbidden.FORBIDDEN_PHRASES, and the visual rebase directive §2 states that a redesign does
    not authorise changes to prohibited wording. The addendum of 23 September 2026 restores the
    client's MARK and the doorway IMAGERY; it says nothing about that line of text. So the mark is
    used exactly as drawn and the forbidden line stays out. If the client wants it back, the
    implementation document is what has to change first — and then this docstring.

    `variant="dark"` is the one variant that exists: on a dark surface the mark sits on a paper
    tile and the wordmark goes monochrome, because green and red measure 3.23:1 and 2.90:1 on
    midnight (docs/design-v2/BRAND_ASSETS.md §1). The mark itself is never recoloured.
    """
    mark = str(locked_content.text("p1.trademark.mark", "fr"))
    words = mark.split()
    if len(words) >= 3:
        first, middle, last = words[0], " ".join(words[1:-1]), words[-1]
        tm = ""
        if last.endswith("™"):
            last, tm = last[:-1], "™"
        wordmark = format_html(
            '<span class="lock__w1">{}</span> <span class="lock__w2">{}</span> <span class="lock__w3">{}</span>{}',
            first,
            middle,
            last,
            format_html('<span class="lock__tm">{}</span>', tm) if tm else "",
        )
    else:
        wordmark = format_html("{}", mark)
    css = "lock lock--dark" if variant == "dark" else "lock"
    return format_html(
        '<span class="{css}" translate="no" dir="ltr" lang="en">'
        '<img class="lock__mark" src="{src}" alt="" width="38" height="38" decoding="async">'
        '<span class="lock__text"><span class="lock__wm">{wm}</span></span></span>',
        css=css,
        src=static("brand/original/logo-mark.svg"),
        wm=wordmark,
    )


@register.simple_tag
def brand_words() -> str:
    """Prescribed wording in letters for FR («marque déposée») and IT («marchio depositato»)."""
    lang = (translation.get_language() or "fr").split("-")[0]
    if lang == "fr":
        return locked_content.text("p1.trademark.words_fr", "fr")
    if lang == "it":
        return locked_content.text("p1.trademark.words_it", "fr")
    return mark_safe("")  # noqa: S308 - empty string


@register.filter
def hero_lines(title) -> list[dict]:
    """
    The hero title as lines for the masked reveal — the text unchanged, only the breaks chosen.

    The locked «ITALY LEGAL ENTRY™» breaks before its last word, as the direction draws it; a
    longer interim title breaks near its middle at a space. A trailing ™ is returned apart so the
    template can set it smaller. Never more than two lines: a third would push the doorway down.
    """
    text = str(title or "").strip()
    tm = text.endswith("™")
    if tm:
        text = text[:-1].rstrip()
    words = text.split()
    if len(words) <= 2:
        lines = [text]
    elif len(words) <= 4:
        lines = [" ".join(words[:-1]), words[-1]]
    else:
        half = max(1, round(len(words) / 2))
        lines = [" ".join(words[:half]), " ".join(words[half:])]
    out = [{"text": line, "tm": False} for line in lines if line]
    if out and tm:
        out[-1]["tm"] = True
    return out
