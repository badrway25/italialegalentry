"""
The browser fixtures of the composition library V2 (design V5.22, SECTION_SYSTEM_V2 §9.1 «Proof»; lane S).

One fixture per pattern: the pattern's partial rendered with sample data built from the registries (the locked texts,
the pathways, the imagery slots) inside a bare page that links the shared sheets and the pattern partials' sources.
These are fixtures, not a hub page: the library is never shown to the owner as a catalogue (§5, §29) — the page exists
only inside a test's browser (Playwright's route), never under a URL of the site.

Round 1 (label v522-s-improve1, QA_ROUND1 m2, m3, m7, m8, m11): every French sample on an Italian, English or Arabic
page carries `lang="fr"` (its own box, its own start — §1 rule 6), so the RTL proof is made for every pattern; the route
board's lanes and the grid's lead tile hold their frames (lane M's family frames, the lead's photograph); the bands
that sweep a light declare it (`data-verb="light"`); the passage (J), the measured flow (F) and a panorama whose slot
has no 4:5 crop have fixtures of their own.

    page(name, lang)        the whole HTML document of one fixture, in a language (fr, it, en, ar)
    NAMES                   the fixtures, one per pattern and variant
"""

from __future__ import annotations

from django.conf import settings
from django.template import engines
from django.templatetags.static import static
from django.utils import translation
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from cms import locked_content
from core import icons
from ecosystem.services import company_moments

#: the partial sources a fixture page draws (bundled for the fixtures alone by apps/core/static/core/sezioni.css)
PARTIALS = (
    "_sezioni", "_sigillo", "_photo", "_journey-passage", "_linea-v2", "_sec-flusso", "_sec-campata", "_sec-boussole",
    "_sec-tracciato", "_sec-racconto", "_sec-mosaico", "_sec-mappa", "_sec-emiciclo", "_sec-filo", "_sec-passaggio",
    "_sec-strato", "_sec-indice",
)

HEAD = """<!DOCTYPE html><html lang="{lang}" dir="{dir}" class="no-js"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>fixture {name}</title>
<link rel="stylesheet" href="{main}"><link rel="stylesheet" href="{reveal}"><link rel="stylesheet" href="{fronte}">{partials}
<script src="{head_js}"></script></head><body class="{rtl}"><main id="main-content" tabindex="-1">
<section class="sez" data-ground="paper" data-rhythm="strip"><div class="container"><h1>fixture · {name}</h1>
<p class="fixture-gap">{gap}</p></div></section>"""
FOOT = """</main><script type="module" src="{rise}"></script></body></html>"""


def _locked(key: str, lang: str) -> tuple:
    """A locked text and the `lang` attribute it needs on the page: its effective language when that is not the page's
    (a French locked run on an Italian, English or Arabic page stays French, §1 rule 6)."""
    value, effective = locked_content.get(key, lang)
    return value, (effective if effective != lang else "")


def _fr(lang: str) -> str:
    """The `lang` attribute of a fixture's own French sample on the page."""
    return "fr" if lang != "fr" else ""


def _span(text: str, lang: str):
    """A French sample where a partial takes plain text with no `*_lang` key: in its own span."""
    return format_html('<span lang="fr">{}</span>', text) if lang != "fr" else text


def _section(pattern: str, body: str, ground: str = "paper", title: str = "", rhythm: str = "band", lang: str = "fr",
             verb: str = "") -> str:
    head = ""
    if title:
        head = engines["django"].from_string(
            '{% include "components/sezioni/_testa.html" with role="statement" title_id=tid title=title title_lang=tl %}'
        ).render({"tid": f"t-{pattern}", "title": title, "tl": _fr(lang)})
    named = f' aria-labelledby="t-{pattern}"' if title else f' aria-label="{pattern}"'
    verb_attr = f' data-verb="{verb}"' if verb else ""
    return (
        f'<section class="sez sez--{pattern}" data-sec="{pattern}" data-ground="{ground}" data-rhythm="{rhythm}"'
        f'{verb_attr}{named}><div class="container">{head}{body}</div></section>'
    )


def _context(lang: str) -> dict:  # noqa: PLR0914 — one fixture's data, pattern by pattern
    fr = _fr(lang)
    pathways, pathways_lang = _locked("p3.persons.pathways", lang)
    faq, faq_lang = _locked("p3.faq.items", lang)
    sequence, _seq_lang = _locked("p3.pilot.sequence", lang)
    hero, hero_lang = _locked("p3.hero.body", lang)
    why, why_lang = _locked("p2.forum.why.body", lang)
    recipients, recipients_lang = _locked("p3.institutions.recipients", lang)

    def stations(keys):
        return [
            {"num": f"0{i + 1}", "glyph": icons.PATHWAY[p["key"]], "title": p["title"], "title_lang": pathways_lang,
             "line": p["description"], "line_lang": pathways_lang, "url": "#"}
            for i, p in enumerate(pathways) if p["key"] in keys
        ]

    def entrance(key, glyph, audience):
        title, title_lang = _locked(f"p3.entrances.{key}.title", lang)
        text, _text_lang = _locked(f"p3.entrances.{key}.text", lang)
        button, _button_lang = _locked(f"p3.entrances.{key}.button", lang)
        return {"title": title, "text": text, "button": button, "lang": title_lang, "glyph": glyph, "audience": audience}

    return {
        "lanes": [
            {"key": "travail", "label": "Travail", "label_lang": fr, "frame_slot": "pathways.family.work",
             "stations": stations(("salaried_work", "skilled_work_eu_blue_card", "self_employment_entrepreneurship"))},
            {"key": "etudes", "label": "Études et formation", "label_lang": fr, "frame_slot": "pathways.family.study",
             "stations": stations(("training_in_origin_country", "study_and_training_in_italy", "scientific_research"))},
            {"key": "famille", "label": "Famille", "label_lang": fr, "frame_slot": "pathways.family.family",
             "stations": stations(("family_reunification",))},
        ],
        "control": {"legend": _span("Familles de parcours", lang), "all": _span("Toutes", lang),
                    "count": _span("8 parcours réguliers", lang)},
        "origin": {"glyph": "compass", "title": _span("Le questionnaire d’orientation", lang), "url": "#",
                   "link_label": _span("Commencer", lang)},
        "pilot_steps": [{"label": label, "glyph": glyph, "lang": "fr"} for label, glyph in zip(sequence, icons.PILOT_STATION, strict=False)],
        "moments": [
            {"glyph": glyph, "label": m["label"], "text": m["text"]}
            for glyph, m in zip(icons.COMPANY_MOMENT, company_moments(), strict=True)
        ],
        "how_steps": [
            {"label": "Répondez au questionnaire", "glyph": "compass", "lang": "fr"},
            {"label": "Recevez une pré-évaluation à caractère informatif", "glyph": "info", "lang": "fr"},
            {"label": "Préparez-vous avec la formation", "glyph": "presentation", "lang": "fr"},
            {"label": "Les autorités compétentes décident", "glyph": "stamp", "lang": "fr"},
        ],
        "tiles": [
            {"href": "#", "title": "Formation", "line": "Avant le départ et après l’arrivée.", "glyph": "presentation",
             "lead": True, "frame_slot": "training.after"},
            {"href": "#", "title": "Diplômes et titres", "line": "La reconnaissance, étape par étape.", "glyph": "award"},
            {"href": "#", "title": "Vivre en Italie", "line": "Les premiers pas après l’arrivée.", "glyph": "sprout"},
            {"href": "#", "title": "Questions fréquentes", "line": "Les réponses aux questions courantes.", "glyph": "circle-help"},
            {"href": "#", "title": "Glossaire", "line": "Les termes italiens des parcours.", "glyph": "book-a"},
        ],
        "doors": [
            {"href": "#", "title": "Espace Personnes", "line": "Les parcours réguliers.", "glyph": "person", "audience": "person"},
            {"href": "#", "title": "Espace Entreprises", "line": "Les besoins en compétences.", "glyph": "building", "audience": "company"},
            {"href": "#", "title": "Espace Institutions", "line": "La coopération institutionnelle.", "glyph": "institution", "audience": "institution"},
            {"href": "#", "title": "Universités et formation", "line": "Les parcours de formation.", "glyph": "university", "audience": "university"},
        ],
        "rimando": [
            {"href": "#", "title": "Glossaire", "glyph": "book-a"},
            {"href": "#", "title": "Attention aux fraudes", "glyph": "ile-scudo"},
            {"href": "#", "title": "Une question ?", "glyph": "message-square-text"},
        ],
        # the home's S3 (§3.1): the eight pathways, each its PATHWAY glyph in the index and its tile on the stage
        "pathway_items": [
            {"id": f"fx-{p['key']}", "title": p["title"], "title_lang": pathways_lang, "glyph": icons.PATHWAY[p["key"]],
             "body": format_html("<p>{}</p>", p["description"]), "body_lang": pathways_lang,
             "links": format_html('<a class="link-arrow" href="#"{}>{}</a>', format_html(' lang="{}"', fr) if fr else "", "Voir le parcours")}
            for p in pathways
        ],
        # the FAQ (§3.13): the questions as a list, the fraud question's ink rule and its ile-scudo mark; the answer
        # plate's one concept is its T1 seal (no item tile beside it)
        "faq_items": [
            {"id": f"fx-{item['key']}", "title": item["question"], "title_lang": faq_lang,
             "glyph": "ile-scudo" if item["key"] == "faq_guaranteed_visa_offer" else "",
             "body": format_html("<p>{}</p>", item["answer"]), "body_lang": faq_lang,
             "marked": item["key"] == "faq_guaranteed_visa_offer"}
            for item in faq[:5]
        ],
        "trust": [
            {"heading": item["question"], "heading_lang": faq_lang, "text": item["answer"], "keyword": True,
             "href": "#", "body_lang": faq_lang}
            for item in faq[:4]
        ],
        "nodes": [
            {"key": key, "glyph": glyph, "audience": aud, "label": label, "label_lang": fr,
             "panel": format_html("<p>{} — {}</p>", label, text), "panel_lang": fr, "href": "#",
             "link_label": _span("Voir l’espace", lang)}
            for key, glyph, aud, label, text in (
                ("personnes", "person", "person", "Personnes", "des parcours réguliers vers l’Italie."),
                ("entreprises", "building", "company", "Entreprises", "les besoins en compétences."),
                ("institutions", "institution", "institution", "Institutions", "la coopération entre territoires."),
                ("universites", "university", "university", "Universités", "la formation avant et après l’arrivée."),
                ("professionnels", "briefcase", "professional", "Professionnels", "l’accompagnement dans les procédures."),
            )
        ],
        "hub": {"title": _span("En bref", lang), "caption": format_html("<p>{}</p>", hero), "caption_lang": hero_lang,
                "mark": "ile-forum"},
        "seats": [{"glyph": g} for g in icons.RECIPIENT_SEAT],
        "sentence": recipients,
        "sentence_lang": recipients_lang,
        "milestones": [
            {"id": f"fx-step-{i}", "glyph": glyph, "heading": heading, "heading_lang": fr,
             "body": format_html("<p>{}.</p>", heading), "body_lang": fr}
            for i, (glyph, heading) in enumerate(zip(icons.SHEET_STEP, ("Orientation", "Documentation", "Procédure",
                                                                         "Préparation", "Entrée en Italie"), strict=False))
        ],
        "rail": {"label": "Sommaire de la page", "items": [{"id": f"fx-step-{i}", "label": h, "lang": fr} for i, h in enumerate(
            ("Orientation", "Documentation", "Procédure", "Préparation", "Entrée en Italie"))]},
        "story": [
            {"id": "fx-bref", "heading": "En bref", "heading_lang": fr, "body": format_html("<p>{}</p>", hero), "body_lang": hero_lang},
            {"id": "fx-pourquoi", "heading": "Pourquoi", "heading_lang": fr, "body": format_html("<p>{}</p>", why), "body_lang": why_lang},
            {"id": "fx-qui", "heading": "Qui porte le projet", "heading_lang": fr,
             "body": mark_safe("<p>L’association promotrice porte le projet.</p>"), "body_lang": fr},  # noqa: S308 — a fixture's own text
        ],
        "approdo_tiles": [
            {"href": "#", "title": "Forum Vénétie–Maroc", "title_lang": fr, "line": "Le dialogue entre les territoires.", "line_lang": fr, "forum": True},
            {"href": "#", "title": "Le projet pilote", "title_lang": fr, "line": "Vénétie–Maroc.", "line_lang": fr, "glyph": "ile-pilota"},
            {"href": "#", "title": "Le promoteur", "title_lang": fr, "line": "L’association AGAMI.", "line_lang": fr, "glyph": "institution", "disc": True},
        ],
        "entrances": [
            entrance("person", "person", "person"), entrance("company", "building", "company"),
            entrance("institution", "institution", "institution"), entrance("university", "university", "university"),
        ],
        "marks": [mark.id for mark in icons.MARKS.values()],
    }


def _tiles_lang(ctx: dict, fr: str) -> None:
    """The fixture's own French tile texts take their `lang` on the other pages."""
    for key in ("tiles", "doors", "rimando"):
        for tile in ctx[key]:
            tile.setdefault("title_lang", fr)
            if tile.get("line"):
                tile.setdefault("line_lang", fr)


#: J «il passaggio» — sample markup of the rail=True contract (lane H's components/entrances.html draws it on the home):
#: an <ol class="passaggio"> of four plates, each one link with all its locked text visible, its arch an inline svg whose
#: path is drawn on pathLength 1 (`vector-effect` keeps its 1.5 px whatever the plate's width); the position rule is the
#: wrapper's (.passaggio-rail::after, bound to the rail's own scroll). The plate's interior is the home's (lane H's
#: sheet): the fixture's <style> only stands in for it, so that the rail is seen with plates that read
PASSAGGIO = (
    '<style>.fx-entrata{display:grid;justify-items:start;align-content:start;gap:var(--s-3);'
    'padding:var(--s-3) var(--s-5) var(--s-5)}.fx-entrata .passaggio__arco{justify-self:stretch;block-size:2rem}'
    '.fx-entrata .sez-disc{margin-block-start:-1.75rem}.fx-entrata p{margin:0}</style>'
    '<div class="passaggio-rail"><ol class="passaggio" role="list">{% for e in entrances %}'
    '<li class="passaggio__lastra sez-plate fx-entrata" data-audience="{{ e.audience }}">'
    '<svg class="passaggio__arco" viewBox="0 0 100 24" preserveAspectRatio="none" aria-hidden="true" focusable="false">'
    '<path pathLength="1" vector-effect="non-scaling-stroke" data-verb="stroke" d="M1 24V13A49 12 0 0 1 99 13V24"/></svg>'
    '<span class="sez-disc" aria-hidden="true">{% svg_icon e.glyph "icon" %}</span>'
    '<a class="sez-stretch" href="#"{% if e.lang %} lang="{{ e.lang }}"{% endif %}><strong>{{ e.title }}</strong></a>'
    '<p{% if e.lang %} lang="{{ e.lang }}"{% endif %}>{{ e.text }}</p>'
    '<p{% if e.lang %} lang="{{ e.lang }}"{% endif %}><span class="link-arrow">{{ e.button }}</span></p>'
    '</li>{% endfor %}</ol></div>'
)
#: F · «il flusso» — one panel (components/sezioni/flusso.html, V5.30 Fast Visual Variety Correction §7): Entreprises EN-1's
#: three moments (team strings of apps/ecosystem/services.py, glyphs icons.COMPANY_MOMENT) as its cells, the terminal plate
#: and the end call under it
FLUSSO = (
    '{% include "components/sezioni/flusso.html" with steps=moments terminal=terminal end_action=campata_action %}'
)

TEMPLATES = {
    "sigillo": '{% for m in marks %}{% include "components/sezioni/sigillo.html" with mark=m size="body" %}{% endfor %}'
    '<div class="fixture-night" data-tone="night">{% for m in marks %}{% include "components/sezioni/sigillo.html" with mark=m size="small" %}{% endfor %}</div>',
    "campata": '{% include "components/sezioni/campata.html" with media_slot="home.ecosystem" side="start" frame="arch" title_id="t-campata" title="Un écosystème institutionnel" title_lang=fr lead="Promoteur" lead_lang=fr body=story_body action=campata_action %}',
    "boussole": '{% include "components/sezioni/boussole.html" with title_id="t-boussole" title="Orientation" title_lang=fr text="Le questionnaire vous oriente vers la voie régulière la plus adaptée. Les décisions relèvent des autorités compétentes." text_lang=fr action=campata_action help=boussole_help %}',
    "tracciato": '{% include "components/sezioni/tracciato.html" with id="fx" %}',
    "racconto": '{% include "components/sezioni/racconto.html" with figure_template="components/sezioni/marks/_ile-forum.html" steps=story %}',
    "panorama": '{% include "components/sezioni/panorama.html" with slot="project.volumes" plate=panorama_plate %}',
    "panorama-band": '{% include "components/sezioni/panorama.html" with slot="companies.territory" plate=panorama_plate %}',
    "mosaico": '{% include "components/sezioni/mosaico.html" with variant="grid" %}',
    # the grid's lead without a frame (PA-3, F2, D3: «the wide tile»): the whole first row, the compact tiles under it
    "mosaico-ampio": '{% include "components/sezioni/mosaico.html" with variant="grid" tiles=tiles_ampio %}',
    "porte": '{% include "components/sezioni/mosaico.html" with variant="porte" tiles=doors %}',
    "rimando": '{% include "components/sezioni/mosaico.html" with variant="rimando" tiles=rimando %}',
    "linea": '{% include "components/stepper.html" with size="large" steps=pilot_steps across=True origin_seal="ile-pilota" terminal=terminal end_action=campata_action %}',
    "linea-how": '{% include "components/stepper.html" with size="large" steps=how_steps across=True origin_seal="ile-orienta" terminal=terminal end_action=campata_action %}',
    "flusso": FLUSSO,
    "mappa": '{% include "components/sezioni/mappa.html" with id="fx" label="Les acteurs" layout="ring" %}',
    "emiciclo": '{% include "components/sezioni/mappa.html" with layout="arc" nodes=seats %}',
    "filo": '{% include "components/sezioni/filo.html" %}',
    "strato": '{% include "components/sezioni/strato.html" with plates=trust columns=2 %}',
    "protezione": '{% include "components/sezioni/protezione.html" with url="#" %}',
    "approdo": '{% include "components/sezioni/approdo.html" with title_id="t-approdo" title="Pour aller plus loin" title_lang=fr tiles=approdo_tiles motif="mission" %}',
    "indice": '{% include "components/sezioni/indice.html" with form="tabs" id="fx" label="Les parcours réguliers" items=pathway_items %}',
    "explorer": '{% include "components/sezioni/indice.html" with form="explorer" id="fx" label="Questions" items=faq_items seal="ile-domande" %}',
    "disclosure": '{% include "components/sezioni/indice.html" with form="disclosure" name="fx" items=faq_items %}',
    "passaggio": PASSAGGIO,
}
GROUNDS = {"protezione": "stone", "approdo": "stone", "strato": "stone", "porte": "stone", "rimando": "stone",
           "linea-how": "brand", "boussole": "brand", "mappa": "night", "emiciclo": "night"}
TITLES = {"tracciato": "Les parcours réguliers", "mosaico": "Dans l’Espace Personnes",
          "mosaico-ampio": "Dans l’Espace Personnes", "porte": "Les espaces",
          "linea": "La séquence du projet pilote", "linea-how": "Comment fonctionne l’orientation",
          "flusso": "Trois temps, une même démarche", "mappa": "Les acteurs de l’écosystème", "emiciclo": "Destinataires",
          "filo": "Étapes", "strato": "Ce que fait la plateforme", "indice": "Les parcours réguliers",
          "explorer": "Questions fréquentes", "disclosure": "Définitions", "racconto": "Le projet", "sigillo": "Les marques ILE",
          "rimando": "Pour aller plus loin", "passaggio": "Quatre accès à l’écosystème"}
#: the patterns drawn without the section head the fixture adds (theirs is in the partial, or they have none)
HEADLESS = ("campata", "boussole", "approdo", "racconto", "sigillo", "protezione", "panorama", "panorama-band")
#: the bands that sweep their light once as they enter (K «lo strato», «l'approdo»: §2 K, LIGHT)
LIGHT = ("strato", "approdo")
NAMES = tuple(TEMPLATES)
#: the patterns that hand interaction to a module, and the module's name (rise.js loads it)
MODULE_OF = {"mappa": "mappa", "indice": "indice", "explorer": "indice", "racconto": "racconto", "filo": "spia",
             "flusso": "flow"}


def page(name: str, lang: str = "fr", spacer: bool = False) -> str:
    """One fixture's whole document; `spacer` puts the section a screen below the fold (the trigger's «wait»)."""
    with translation.override(lang):
        fr = _fr(lang)
        ctx = _context(lang)
        _tiles_lang(ctx, fr)
        ctx["tiles_ampio"] = [{k: v for k, v in tile.items() if k != "frame_slot"} for tile in ctx["tiles"]]
        ctx.update(
            fr=fr,
            story_body=format_html('<p{}>L’association promotrice, active depuis 2011 entre l’Italie et le Maroc (Italie–Maroc).</p>',
                                   format_html(' lang="{}"', fr) if fr else ""),
            campata_action={"url": "#", "label": _span("Commencer le questionnaire d’orientation", lang), "kind": "primary"},
            boussole_help=_span("Une question ? Écrivez-nous.", lang),
            terminal=format_html('<p{}><strong>Aucun résultat n’est garanti.</strong> Les décisions relèvent des autorités compétentes.</p>',
                                 format_html(' lang="{}"', fr) if fr else ""),
            panorama_plate={"title": "Le territoire", "title_lang": fr, "text": "Une bande de territoire, une respiration de la page.",
                            "text_lang": fr},
            site={"lang": lang, "dir": "rtl" if lang == "ar" else "ltr"},
        )
        body = engines["django"].from_string(TEMPLATES[name]).render(ctx)
        title = TITLES.get(name, name.capitalize())
        section = _section(
            name, body, GROUNDS.get(name, "paper"), "" if name in HEADLESS else title,
            rhythm="moment" if name in ("mappa", "racconto", "panorama", "panorama-band") else "band", lang=lang,
            verb="light" if name in LIGHT else "",
        )
        partials = f'<link rel="stylesheet" href="{static("css/dist/core/sezioni.css")}">'
        head = HEAD.format(
            lang=lang, dir="rtl" if lang == "ar" else "ltr", name=name, main=static("css/dist/main.css"),
            reveal=static("css/dist/core/reveal.css"), fronte=static("css/dist/pages/css/fronte.css"), partials=partials,
            head_js=static("js/head.js"), rtl="is-rtl" if lang == "ar" else "",
            gap="Une première bande, pour que la section commence sous la ligne de flottaison." * (60 if spacer else 6),
        )
        return head + section + FOOT.format(rise=static("js/dist/rise.js"))


def languages() -> list[str]:
    return [code for code, _name in settings.LANGUAGES]
