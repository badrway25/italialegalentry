"""
Navigation template tags (design system) — ``{% load cms_nav %}``.

{% main_menu as menu %}          → tree of NavItem for the header (location "main")
{% footer_menu as items %}       → flat list of NavItem for the footer navigation column
{% brand %}                      → the trademark wordmark, always from the locked registry

Menu rows come from ``cms.MenuItem`` (back-office editable). When no visible row exists for a
location, a static fallback structure is used so the site is navigable from day one. Items are
filtered by publication gates (``requires_gate``) and feature flags (``requires_flag``); items
whose URL name is not (yet) resolvable are hidden, so a menu never links to a missing route.

«Il portico» (docs/design-v5/V5_4_EXECUTION_PLAN.md §1.12, W2-C1): a section whose destination is one of
the four audiences' spaces is a DOOR. ``_portico()`` gives every door what its panel draws, from live
content only — nothing is written here: the door's locked gloss (the door card's own text), its CMS
children or, when it has none, the door card's two live task links, a second line under an entry only
where a short live sentence exists (shown whole, never cut), the door's audience glyph and photograph,
and the anti-fraud foot where the menu carries that page. The IA is the owner's D-U3: four doors, a
hairline, Forum, Projet; «Actualités» moves into the Projet panel.
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
from core.links import public_url

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
    # «Il portico» (_portico below): what a panel draws. All of it is derived, never typed in.
    url_name: str = ""
    audience: str = ""  # person · company · institution · university — a door; "" for a plain panel
    icon: str = ""  # the audience glyph, drawn once on the panel's photograph
    gloss: str = ""  # the panel's lede: the door's locked gloss, or the section's own description
    gloss_lang: str = ""  # its lang attribute when it is not in the page's language
    description_message: object = None  # the gettext source of `description` (the static fallback), so the
    # plain panel's gloss can say in which language it is (an already-translated string cannot)
    photo: dict = field(default_factory=dict)
    foot_url: str = ""  # the anti-fraud page, drawn as the panel's one-line foot
    after_doors: bool = False  # the first item after the doors: the hairline stands before it


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
    # Institutions and Universités have no CMS children: their panels carry the door card's two live task
    # links (_DOOR_TASKS), so every door has a panel with the same anatomy (CD §7, «all or none»).
    (_("Institutions"), "ecosystem:institutions", "phase3_public", "", ()),
    (_("Universités & Formation"), "ecosystem:universities", "phase3_public", "", ()),
    (_("Forum Vénétie–Maroc"), "forum:index", "", "", ()),
    # D-U3: «Actualités» leaves the top row for the Projet panel, until it has a publishing cadence.
    (
        _("Projet"),
        "pages:project",
        "",
        _("Le projet, son promoteur et son réseau."),
        (
            (_("Italy Legal Entry"), "pages:project", ""),
            (_("AGAMI"), "pages:agami", ""),
            (_("Réseau"), "pages:network", ""),
            (_("Actualités"), "news:index", "phase3_public"),
            (_("Contact"), "pages:contact", ""),
        ),
    ),
)

# ---------------------------------------------------------------------------------------------
# «Il portico» — the doors' panels (plan §1.12). Live content only.
# ---------------------------------------------------------------------------------------------
#: A section is a door when it leads to one of the four audiences' spaces (the home's four entrances).
_DOOR_ROUTES = {
    "pathways:index": "person",
    "ecosystem:companies": "company",
    "ecosystem:institutions": "institution",
    "ecosystem:universities": "university",
}
_DOOR_ICONS = {"person": "person", "company": "building", "institution": "institution", "university": "university"}
#: The door card's two live task links: the labels and destinations the door's own page already uses
#: (templates/ecosystem/institutions.html, universities.html). A door without CMS children carries them.
_DOOR_TASKS: dict[str, tuple] = {
    "institution": (
        (_("Proposer une collaboration institutionnelle"), "enquiries:institution_proposal"),
        (_("Le Forum Vénétie–Maroc"), "forum:index"),
    ),
    "university": (
        (_("Proposer un partenariat"), "enquiries:university_proposal"),
        (_("Formation : avant le départ et après l’arrivée"), "pathways:training"),
    ),
}
#: Each door's own audience photograph, in colour, in the V5 grade — the Image Art Director's recorded panel
#: crop of ASSET_USAGE_MATRIX rows 2–5 (Persona: the wide 4:5). static/img/portico/PROVENANCE.json holds the
#: licence, the author, the crop and the redaction of each file.
_DOOR_PHOTOS = {
    "person": "lectrice-bibliotheque-dos-4x5",
    "company": "chai-cuve-chene-4x5",
    "institution": "table-en-seance-4x5",
    "university": "cours-tableau-dos-4x5",
}
#: The anti-fraud page is the panel's foot, not an entry (CD §7: «the anti-fraud entry as one line»).
_FOOT_ROUTE = "pages:antifraud"
#: A second line under an entry: the destination's own live sentence — as its page, or the door's page
#: beside the same link, already says it. Keyed (door audience, url name); "" = in any panel. Kinds:
#: "ui" a gettext string of that page · "ui-first" the first sentence of one · "locked" a locked text ·
#: "locked-first" the first sentence of one. Shown only when short (≤ _SECOND_LINE_MAX, whole, never cut)
#: and in the page's own language: a panel never mixes a French line into an Arabic list.
_SECOND_LINES: dict[tuple[str, str], tuple[str, object]] = {
    ("person", "pathways:index"): ("locked-first", "p3.persons.intro"),
    ("person", "pathways:training"): (
        "ui-first",
        _(
            "Deux temps d’un même parcours : se préparer dans le pays d’origine, puis continuer à se former en "
            "Italie. Les formations ont une finalité d’orientation et de préparation."
        ),
    ),
    ("person", "faq:index"): (
        "ui",
        _(
            "Les réponses aux questions les plus fréquentes sur Italy Legal Entry™ et sur les parcours réguliers "
            "vers l’Italie."
        ),
    ),
    ("person", "glossary:index"): (
        "ui",
        _("Les termes italiens que vous rencontrerez dans les démarches, expliqués en quelques mots."),
    ),
    ("institution", "enquiries:institution_proposal"): (
        "ui",
        _("Présentez votre institution et votre proposition : chaque demande est lue par l’équipe du projet."),
    ),
    ("institution", "forum:index"): ("locked", "p2.forum.header.subtitle"),
    ("university", "enquiries:university_proposal"): (
        "ui",
        _("Présentez votre établissement et votre proposition : chaque demande est lue par l’équipe du projet."),
    ),
    ("university", "pathways:training"): ("ui", _("Deux temps d’un même parcours, dans l’Espace Personnes.")),
    ("", "news:index"): ("locked", "p3.news.body"),
    # the Projet panel: each page's own standfirst (apps/pages/content.py HERO_INTERIM «subtitle», reused by the
    # project page; templates/pages/network.html and contact.html `page_lead`)
    ("", "pages:project"): (
        "ui",
        _("Orientation, formation avant le départ et accompagnement, avec les acteurs compétents."),
    ),
    ("", "pages:network"): ("ui", _("Un projet construit avec les acteurs compétents, chacun dans son rôle.")),
    ("", "pages:contact"): ("ui", _("Une adresse unique pour toutes les demandes relatives au projet.")),
}
_SECOND_LINE_MAX = 160  # cms.MenuItem.description_fr's own limit: a line the back-office could have written

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
                kids.append(NavItem(id=_slug(f"nav-{i}", j), label=str(c_label), url=c_url, url_name=c_url_name))
        if not url and not kids:
            continue
        items.append(
            NavItem(
                id=_slug("nav", i),
                label=str(label),
                url=url,
                description=str(description),
                description_message=description,
                children=kids,
                is_section=bool(kids),
                url_name=url_name,
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
                        url_name=child.url_name,
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
                url_name=row.url_name,
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
        if location == MenuLocation.MAIN:
            _portico(items, lang)
    if path:
        for item in items:
            _mark_current(item, path, lang)
    return items


def _first_sentence(text: str) -> str:
    """The first sentence of a live text, kept whole: up to the first full stop followed by a space."""
    text = " ".join(str(text or "").split())
    for index, char in enumerate(text):
        if char in ".!?" and (index + 1 == len(text) or text[index + 1] == " "):
            return text[: index + 1]
    return text


def _live_line(kind: str, source, lang: str, phase3: bool) -> tuple[str, str]:
    """(text, lang attribute) of a live sentence; ("", "") when it does not exist in a usable form."""
    from pages import services as page_services  # pages imports cms: imported here, not at module load

    if kind.startswith("locked"):
        if str(source).startswith("p3.") and not phase3:
            return "", ""  # a Phase 3 prescribed text never shows before gate G3
        text = page_services.locked(str(source), lang)
    else:
        text = page_services.ui(source)
    value = str(text.value or "")
    if kind.endswith("-first"):
        value = _first_sentence(value)
    return value, text.lang


def _photo(audience: str) -> dict:
    slug = _DOOR_PHOTOS.get(audience)
    if not slug:
        return {}
    small, large = static(f"img/portico/{slug}-640.webp"), static(f"img/portico/{slug}-960.webp")
    return {"src": small, "srcset": f"{small} 640w, {large} 960w", "width": 640, "height": 800}


def _portico(items: list[NavItem], lang: str) -> None:
    """Give every door and every plain panel what «Il portico» draws (plan §1.12). Runs inside the menu's
    ``translation.override(lang)``; reads live texts only and writes none."""
    from pages import services as page_services

    phase3 = gate_open("phase3_public")
    glosses = {e["actor"]: (e["text"], e["text_lang"]) for e in page_services.entrances(lang, phase3)}
    previous_was_door = False
    for item in items:
        item.audience = _DOOR_ROUTES.get(item.url_name, "")
        if item.audience and not item.children:
            for j, (label, url_name) in enumerate(_DOOR_TASKS.get(item.audience, ())):
                url = public_url(url_name)
                if url:
                    item.children.append(
                        NavItem(id=f"{item.id}-task-{j}", label=str(label), url=url, url_name=url_name)
                    )
        # the anti-fraud page is the panel's foot, drawn once, not an entry
        for child in list(item.children):
            if child.url_name == _FOOT_ROUTE:
                item.foot_url = child.url
                item.children.remove(child)
        item.is_section = bool(item.children)
        if item.audience and item.is_section:
            item.icon = _DOOR_ICONS[item.audience]
            item.photo = _photo(item.audience)
            item.gloss, item.gloss_lang = glosses.get(item.audience, ("", ""))
        elif item.is_section and (item.description_message is not None or item.description):
            # a gettext source is translated by the catalogues (its lang attribute says when it was not); a text
            # written in the back-office is French, and says so on the other pages
            text = (
                page_services.ui(item.description_message)
                if item.description_message is not None
                else page_services.editorial(item.description)
            )
            item.gloss, item.gloss_lang = str(text.value), text.lang
        for child in item.children:
            if child.description:  # written in the back-office (French): only on the French page
                if lang == locked_content.FALLBACK_LANGUAGE and len(child.description) <= _SECOND_LINE_MAX:
                    continue
                child.description = ""
            source = _SECOND_LINES.get((item.audience, child.url_name)) or _SECOND_LINES.get(("", child.url_name))
            if not source:
                continue
            text, text_lang = _live_line(source[0], source[1], lang, phase3)
            if text and not text_lang and len(text) <= _SECOND_LINE_MAX:
                child.description = text
        is_door = bool(item.audience and item.is_section)
        item.after_doors = previous_was_door and not is_door
        previous_was_door = is_door


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
