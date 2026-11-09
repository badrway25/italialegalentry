"""Homepage and institutional pages — thin views; every decision lives in ``pages.services``.

V5.22 (SECTION_SYSTEM_V2 §3.2, §3.11, §3.12, §3.17, §3.18; lane P2): the institutional pages' V2 compositions take
plain data built here from the services' context and the content registry, read-only (§9.7: ``services.py`` and
``content.py`` are the homepage lane's) — the story's steps of /le-projet/, the doors, the network map's entries, the
contact page's doors, the promoter's identification. Nothing here holds or retypes a prescribed text: the locked
registry is read through the services' context, and its parts are cut at render (cms.locked_split).
"""

from __future__ import annotations

from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import translation
from django.utils.cache import add_never_cache_headers
from django.utils.html import format_html
from django.utils.translation import gettext as _
from django.views.decorators.http import require_safe

from cms import locked_content
from core import gates, icons
from core.templatetags.ile_core import svg_icon
from pages import content, identity, imagery, services

#: an actor of the ecosystem → its audience accent (static/css/v5/_sezioni.css: --aud)
AUDIENCE_OF = {
    "persons": "person",
    "companies": "company",
    "institutions": "institution",
    "universities": "university",
    "professionals": "professional",
}


def _crumbs(*items: tuple[str, str]) -> list[dict]:
    return [{"label": label, "url": url} for label, url in items]


def _arrow_line(label) -> str:
    """A door's way in: its words and the arrow that extends under the hand (the arrow flips in Arabic)."""
    return format_html("<span>{}</span>{}", label, svg_icon("arrow", "icon icon--sm"))


def _audience_glyph(audience: str) -> str:
    """An actor's glyph from the icon registry (apps/core/icons.py): its audience's (AUDIENCE), the professionals'
    their actor's (ACTOR: `briefcase`) — never a literal in a register (the O14 lint, §4.10)."""
    for domain in ("audience", "actor"):
        try:
            return icons.concept(domain, audience)
        except icons.UnknownIcon:
            continue
    return ""


def _doors(phase3: bool) -> list[dict]:
    """«Le porte» of /le-projet/ (§3.2 LP-4): the four spaces, equal and unranked — the actor's name, its space's way
    in; the actors' sentences stay on /reseau/ (the cross-page repetition, pages1 §5.3)."""
    doors = []
    for actor in content.NETWORK_ACTORS:
        if not actor.entrance:
            continue
        url = services.entrance_url(actor.entrance, phase3)
        if not url:
            continue
        title, label = services.ui(actor.title), services.ui(actor.link_label)
        doors.append(
            {
                "href": url,
                "title": title.value,
                "title_lang": title.lang,
                "line": _arrow_line(label.value),
                "line_lang": label.lang,
                "glyph": _audience_glyph(AUDIENCE_OF[actor.key]),
                "audience": AUDIENCE_OF[actor.key],
            }
        )
    return doors


def _project_story(request, context: dict) -> dict:
    """C «il racconto» (§3.2 LP-1 + LP-2 + LP-3): the three chapters become the steps of one story beside one figure;
    «En bref» only while gate G3 is open (the presentation is a Phase 3 text). Each step's body is its own partial;
    each step keeps its chapter's anchor (its heading is `<id>-title`: #project-why-title still lands on «Pourquoi»)."""
    steps = []
    if context["presentation"]:
        steps.append(
            {
                "id": "project-presentation",
                "heading": _("En bref"),
                "body": render_to_string("pages/partials/projet/_bref.html", context, request),
            }
        )
    steps.append(
        {
            "id": "project-why",
            "heading": context["why_title"].value,
            "heading_lang": context["why_title"].lang,
            "body": render_to_string("pages/partials/projet/_perche.html", context, request),
        }
    )
    steps.append(
        {
            "id": "project-promoter",
            "heading": _("Qui porte le projet"),
            "body": render_to_string("pages/partials/projet/_promotore.html", context, request),
        }
    )
    return {
        "story": steps,
        "fig_nodes": [
            {
                "key": actor.key,
                "glyph": _audience_glyph(AUDIENCE_OF[actor.key]),
                "audience": AUDIENCE_OF[actor.key],
                "label": actor.title,
            }
            for actor in content.NETWORK_ACTORS
        ],
        "doors": _doors(context["phase3"]),
    }


def _network_map(context: dict) -> dict:
    """H «la mappa» in the head of /reseau/ (§3.11 RE-0 + RE-1 + RE-2): the ring's five nodes are the map's controls,
    each actor's entry a panel docked in the head's reading column; the hub's entry is «En bref» while gate G3 is open
    (exactly what RE-1 rendered: nothing while it is closed — the map then opens on its first actor)."""
    entries = [
        {**actor, "audience": AUDIENCE_OF[actor["key"]], "glyph": _audience_glyph(AUDIENCE_OF[actor["key"]]), "i": i}
        for i, actor in enumerate(context["actors"])
    ]
    return {"map_entries": entries, "approdo": _approdo(context["links"], partners=bool(context["partners"]))}


def _approdo(links: dict, partners: bool = False, project: bool = False) -> list[dict]:
    """K «l'approdo» (§0.1 «Closing bands», §3.11 RE-3, §3.17 AG-4): the ways on of the project's pages — the Forum's
    tile typographic on its night face (Q4: no photograph stands for the Forum), the others raised paper with their
    glyph; the partners' page only with an authorised partner (gate G6). ``project``: the promoter's page, whose ways
    on are the project and the network (the network's are the Forum and the promoter)."""
    tiles = []
    if project:
        if links.get("project"):
            tiles.append({"href": links["project"], "title": _("Le projet"), "glyph": "ile-arch"})
        if links.get("network"):
            tiles.append({"href": links["network"], "title": _("Le réseau"), "glyph": "waypoints"})
    if links.get("forum"):
        # round 1 (QA_ROUND1 m5): the night tile says what the Forum is — its own prescribed subtitle, whole, in its
        # language (Phase 2, public; French on the other pages, marked); typographic as Q4 wants it, no icon at all
        lang = (translation.get_language() or "fr").split("-")[0]
        subtitle, sub_lang = locked_content.get("p2.forum.header.subtitle", lang)
        tiles.append(
            {
                "href": links["forum"],
                "title": _("Forum Vénétie–Maroc"),
                "line": subtitle,
                "line_lang": "" if sub_lang == lang else sub_lang,
                "forum": True,
            }
        )
    if links.get("agami") and not project:
        tiles.append(
            {
                "href": links["agami"],
                "title": _("Le promoteur"),
                "line": settings.ILE["PROMOTER"],
                "line_lang": "it",
                "glyph": "scale",
            }
        )
    if partners and links.get("partners"):
        tiles.append({"href": links["partners"], "title": _("Voir les partenaires")})
    return tiles


def _dedicated_doors(context: dict) -> list[dict]:
    """«Une demande précise ?» on /contact/ (§3.12 C4): the three dedicated forms as audience doors, their labels the
    existing ones; the glyphs and accents are the audiences' (never one gold)."""
    by_url = {
        services.safe_reverse("enquiries:company_needs"): ("building", "company"),
        services.safe_reverse("enquiries:institution_proposal"): ("institution", "institution"),
        services.safe_reverse("enquiries:university_proposal"): ("university", "university"),
    }
    doors = []
    for item in context["dedicated_forms"]:
        glyph, audience = by_url.get(item["url"], ("briefcase", "professional"))
        label = item["label"]
        doors.append(
            {
                "href": item["url"],
                "title": label.value,
                "title_lang": label.lang,
                "line": svg_icon("arrow", "icon icon--sm"),
                "glyph": glyph,
                "audience": audience,
            }
        )
    return doors


def _antifraud_routes(context: dict) -> list[dict]:
    """A «segnalare · informarsi» on /attention-aux-fraudes/ (§3.18 AF2): the three ways to read about the regular
    routes as route tiles — the FAQ's carrying the prescribed question itself (never a paraphrase of it), the Personnes
    space, the glossary. Internal links only: no authority, police, embassy or portal link is authorised.
    Round 2 (QA_ROUND2 M7): when the prescribed answer exists, the FAQ's way is the page's own disclosure instead — the
    question opens its answer in place (§1 rule 7: FAQ answers may stand behind a disclosure; printed once on the page,
    whole, the FAQ's permalink under it) — and the tiles are the two others."""
    links, question = context["links"], context["faq_question"]
    tiles = []
    if links.get("faq") and not (question and question.get("answer")):
        tiles.append(
            {
                "href": links["faq"],
                "title": _("Questions fréquentes"),
                "line": question["question"] if question else "",
                "line_lang": question["lang"] if question else "",
                "glyph": "circle-help",
            }
        )
    if links.get("pathways"):
        tiles.append(
            {"href": links["pathways"], "title": _("Espace Personnes : les parcours réguliers"), "glyph": "signpost"}
        )
    if links.get("glossary"):
        tiles.append({"href": links["glossary"], "title": _("Glossaire des termes officiels"), "glyph": "book-a"})
    return tiles


@require_safe
def home(request):
    return render(request, "pages/home.html", services.home_context(request))


@require_safe
def project(request):
    context = services.project_context(request)
    context["breadcrumbs"] = _crumbs((_("Le projet"), ""))
    context.update(_project_story(request, context))
    return render(request, "pages/project.html", context)


@require_safe
def agami(request):
    context = services.agami_context(request)
    context["breadcrumbs"] = _crumbs((_("Le projet"), services.safe_reverse("pages:project")), (_("AGAMI"), ""))
    context.update(
        {
            # §3.17 AG-3, V5.23: the promoter's public identification, from its one canonical source
            "identification": identity.identification(),
            # §3.17 AG-1: «depuis 2011» and «Italie–Maroc» (the text's own «l’Italie et le Maroc») set in place in the
            # prescribed text (emphasis, never a cut: a needle not in the text is ignored — cms.locked_split.emphasize)
            "who_emphasis": "depuis 2011|l’Italie et le Maroc",
            "approdo": _approdo(context["links"], partners=True, project=True),
            # V5.30 §8: the promoter's own marks (pages.imagery.MARKS) — the head's framed logo, the plate's seal
            "insegna": imagery.mark("agami.insegna"),
            "sigillo": imagery.mark("agami.sigillo"),
        }
    )
    return render(request, "pages/agami.html", context)


@require_safe
def network(request):
    context = services.network_context(request)
    context["breadcrumbs"] = _crumbs((_("Le projet"), services.safe_reverse("pages:project")), (_("Le réseau"), ""))
    context.update(_network_map(context))
    return render(request, "pages/network.html", context)


@require_safe
def contact(request):
    context = services.contact_context(request)
    context["breadcrumbs"] = _crumbs((_("Contact"), ""))
    context["dedicated_doors"] = _dedicated_doors(context)
    return render(request, "pages/contact.html", context)


@require_safe
def antifraud(request):
    """Phase 3 page: 404 (never « coming soon ») while gate G3 is closed; staff preview is noindex."""
    is_preview = False
    if not gates.phase3_public():
        if not services.can_preview(request):
            raise Http404
        is_preview = True
    context = services.antifraud_context(request, is_preview=is_preview)
    context["route_tiles"] = _antifraud_routes(context)
    # the page belongs to the Personnes space (its folio, its nav section): the trail says so (round 2 of W3, m-6)
    context["breadcrumbs"] = _crumbs(
        (_("Espace Personnes"), reverse("pathways:index")), (_("Attention aux fraudes"), "")
    )
    response = render(request, "pages/antifraud.html", context)
    if is_preview:
        # A back-office preview of gated Phase 3 content must never be stored by a shared cache.
        add_never_cache_headers(response)
    return response
