import re

import pytest
from django.utils.html import escape

from cms import locked_content
from cms.models import PublicationStatus
from pathways.models import PATHWAY_KEYS, Pathway, PathwayStep, PathwayWarning
from pathways.tests.conftest import DIPLOMAS_URL, PATHWAY_URL, TRAINING_URL

pytestmark = pytest.mark.django_db

P3_TITLE = escape(locked_content.text("p3.persons.title", "fr"))
P3_INTRO = escape(locked_content.text("p3.persons.intro", "fr"))
P3_HOW = escape(locked_content.text("p3.persons.how_it_works", "fr"))
ANTIFRAUD_TITLE = escape(locked_content.text("p3.antifraud.title", "fr"))
ANTIFRAUD_BODY = escape(locked_content.text("p3.antifraud.body", "fr"))
P1_REPL_1 = escape(locked_content.text("p1.persons.replacement_1", "fr"))
P1_REPL_2 = escape(locked_content.text("p1.persons.replacement_2", "fr"))
DIPLOMAS_TITLE = escape(locked_content.text("p3.diplomas.title", "fr"))
DIPLOMAS_BODY = escape(locked_content.text("p3.diplomas.body", "fr"))
TRAINING_AFTER_TITLE = escape(locked_content.text("p3.training_after.title", "fr"))
TRAINING_AFTER_BODY = escape(locked_content.text("p3.training_after.body", "fr"))
LOCKED_ENTRIES = locked_content.get("p3.persons.pathways", "fr")[0]
ORIGIN_NOTICE = "Parcours en construction avec les acteurs compétents ; aucun canal n’est présenté comme déjà autorisé."
BEFORE_DEPARTURE_NOTICE = (
    "Les formations sont promues avec des organismes partenaires ; "
    "aucune attestation n’a valeur d’approbation administrative."
)


def _html(response) -> str:
    return response.content.decode("utf-8")


def _locked_text(html: str, key: str) -> str:
    """V5.22 (SECTION_SYSTEM_V2 §1 rule 6): a locked text re-composed at render — cut into spans on its own separators —
    is read in its element's text, which is the registry's, character for character."""
    from bs4 import BeautifulSoup

    block = BeautifulSoup(html, "html.parser").select_one(f'[data-locked="{key}"]')
    return block.get_text("") if block else ""


def _how_text(html: str) -> str:
    """The text of «Comment ça marche» as a reader gets it (the stations' words, the hidden arrows between them)."""
    from bs4 import BeautifulSoup

    block = BeautifulSoup(html, "html.parser").select_one('[data-locked="p3.persons.how_it_works"]')
    return " ".join(block.get_text(" ").split()) if block else ""


# ---- interim (gate closed) -----------------------------------------------------------------


class TestInterimIndex:
    def test_renders_200_with_phase1_texts_only(self, client, pathways_seeded, before_phase3):
        r = client.get(PATHWAY_URL)
        assert r.status_code == 200
        html = _html(r)
        assert "page-pathways--interim" in html
        assert html.count("<h1") == 1
        assert "Espace Personnes" in html
        assert P1_REPL_1 in html
        assert P1_REPL_2 in html
        assert "progressivement" in html
        # no Phase 3 prescribed text before the gate
        for text in (P3_TITLE, P3_INTRO, P3_HOW, ANTIFRAUD_TITLE, ANTIFRAUD_BODY):
            assert text not in html
        for entry in LOCKED_ENTRIES:
            assert escape(entry["description"]) not in html
        assert 'data-callout="antifraud"' not in html
        assert 'name="robots" content="noindex' not in html

    def test_interim_has_orientation_cta_block(self, client, pathways_seeded, before_phase3):
        html = _html(client.get(PATHWAY_URL))
        assert 'id="orientation"' in html
        assert "questionnaire d’orientation" in html

    def test_interim_in_every_language_and_rtl(self, client, pathways_seeded, before_phase3):
        for lang in ("it", "fr", "en", "ar"):
            r = client.get(f"/{lang}/parcours/")
            assert r.status_code == 200, lang
        assert '<html lang="ar" dir="rtl"' in _html(client.get("/ar/parcours/"))

    def test_interim_breadcrumbs(self, client, pathways_seeded, before_phase3):
        html = _html(client.get(PATHWAY_URL))
        assert 'class="breadcrumbs' in html
        assert 'aria-current="page"' in html

    @pytest.mark.parametrize("key", PATHWAY_KEYS)
    def test_detail_404_while_gated(self, client, pathways_seeded, before_phase3, key):
        assert client.get(f"{PATHWAY_URL}{key}/").status_code == 404

    def test_diplomas_and_training_404_while_gated(self, client, pathways_seeded, before_phase3):
        assert client.get(DIPLOMAS_URL).status_code == 404
        assert client.get(TRAINING_URL).status_code == 404

    def test_preview_requires_staff(self, client, pathways_seeded, before_phase3, person_user, staff_user):
        assert client.get(f"{PATHWAY_URL}salaried_work/?preview=1").status_code == 404
        client.force_login(person_user)
        assert client.get(f"{PATHWAY_URL}salaried_work/?preview=1").status_code == 404
        client.force_login(staff_user)
        r = client.get(f"{PATHWAY_URL}salaried_work/?preview=1")
        assert r.status_code == 200
        html = _html(r)
        assert 'name="robots" content="noindex' in html
        assert 'data-preview="phase3"' in html
        r = client.get(f"{PATHWAY_URL}?preview=1")
        assert r.status_code == 200 and P3_TITLE in _html(r)
        assert client.get(f"{DIPLOMAS_URL}?preview=1").status_code == 200
        assert client.get(f"{TRAINING_URL}?preview=1").status_code == 200
        # without the flag, staff see the public state
        assert client.get(f"{PATHWAY_URL}salaried_work/").status_code == 404


# ---- Phase 3 open ---------------------------------------------------------------------------


class TestPhase3Index:
    def test_header_and_locked_texts(self, client, pathways_seeded, phase3_open):
        r = client.get(PATHWAY_URL)
        assert r.status_code == 200
        html = _html(r)
        assert "page-pathways--index" in html
        assert html.count("<h1") == 1
        assert P3_TITLE in html
        assert P3_INTRO in html
        # cut on its own arrows into four stations of «la linea» (CREATIVE_DIRECTION_V5 law 8, D-U4): joined back,
        # the words are the registry's sentence, character for character
        assert _how_text(html) == locked_content.text("p3.persons.how_it_works", "fr")
        assert 'data-callout="how-it-works"' in html
        assert 'name="robots" content="noindex' not in html

    def test_eight_pathways_in_prescribed_order_with_exact_texts(self, client, pathways_seeded, phase3_open):
        html = _html(client.get(PATHWAY_URL))
        assert 'data-pathways="8"' in html
        keys = re.findall(r'data-pathway="([a-z_]+)"', html)
        # V5.22 (SECTION_SYSTEM_V2 §3.4 PA-1 «il tracciato delle famiglie», an approved owner/product decision; V5.20
        # strict rule): the eight stand on their family's lane — «the prescribed order shows in the numerals». Each
        # pathway once, each numeral its prescribed rank, the words exact (a stronger check than the document order)
        assert sorted(keys) == sorted(PATHWAY_KEYS) and len(keys) == 8
        # V5.24 (FINAL_DELIVERY_V2 §3.5, TYPOGRAPHY_V2 §4.2; V5.20): the numeral also carries the numeral role by name
        # (`t-numeral`) — the class read as the numeral's own first class, the same invariant
        numerals = dict(
            re.findall(
                r'data-pathway="([a-z_]+)"[^>]*>.*?<span class="tracciato__num(?: t-numeral)?"[^>]*>(\d\d)<', html
            )
        )
        assert numerals == {key: f"{rank:02d}" for rank, key in enumerate(PATHWAY_KEYS, start=1)}
        for entry in LOCKED_ENTRIES:
            assert escape(entry["title"]) in html
            assert escape(entry["description"]) in html
            assert f'href="/fr/parcours/{entry["key"]}/"' in html

    def test_the_families_come_from_the_registry_and_the_count_line_says_each(
        self, client, pathways_seeded, phase3_open
    ):
        """V5.12 W2 review (lane C, minor): each row's family is the services' tuple, not a substring test in the
        template, every pathway has one, and the polite status line carries one count per family (all = 8)."""
        from pathways.services import FAMILY_OF, PATHWAY_FAMILIES

        assert sorted(FAMILY_OF) == sorted(PATHWAY_KEYS)
        assert [f for f, _k in PATHWAY_FAMILIES] == ["work", "study", "family", "other"]
        html = _html(client.get(PATHWAY_URL))
        rows = dict(re.findall(r'data-pathway="([a-z_]+)" data-family="([a-z]+)"', html))
        assert rows == FAMILY_OF
        # V5.22 (SECTION_SYSTEM_V2 §3.4 PA-1; strict rule): the route board's count line, the same polite status
        assert re.search(r'class="tracciato__conto percorsi-conto" role="status" aria-live="polite"', html)
        counts = dict(re.findall(r'data-count="([a-z]+)">(\d+) parcours affichés?<', html))
        expected = {f: str(len(k)) for f, k in PATHWAY_FAMILIES}
        assert counts == {"all": "8", **expected}

    def test_antifraud_callout_present(self, client, pathways_seeded, phase3_open):
        html = _html(client.get(PATHWAY_URL))
        assert 'data-callout="antifraud"' in html
        assert ANTIFRAUD_TITLE in html
        # V5.22 (SECTION_SYSTEM_V2 §0.1 «one component, la protezione», §3.4; strict rule): the anti-fraud plate in its
        # own band — its body cut on its own full stops into three levels, read whole in its element; its mark the
        # protection's T1 seal (ile-scudo), never the alarm's amber
        assert _locked_text(html, "p3.antifraud.body") == locked_content.text("p3.antifraud.body", "fr")
        assert 'data-mark="ile-scudo"' in html

    def test_side_links_and_cta(self, client, pathways_seeded, phase3_open):
        html = _html(client.get(PATHWAY_URL))
        assert 'href="/fr/formation/"' in html
        assert 'href="/fr/diplomes-et-titres/"' in html
        assert 'id="orientation"' in html

    def test_unpublished_pathway_has_no_link(self, client, pathways_seeded, phase3_open):
        p = Pathway.objects.get(key="scientific_research")
        p.status = PublicationStatus.DRAFT
        p.save()
        html = _html(client.get(PATHWAY_URL))
        assert 'href="/fr/parcours/scientific_research/"' not in html
        assert escape(p.title) in html  # still listed: the eight are prescribed
        assert "en préparation" not in html  # V5.12 §8: listed without a link, never «in preparation»
        assert client.get(f"{PATHWAY_URL}scientific_research/").status_code == 404

    def test_languages_and_rtl(self, client, pathways_seeded, phase3_open):
        for lang in ("it", "fr", "en", "ar"):
            r = client.get(f"/{lang}/parcours/")
            assert r.status_code == 200, lang
            assert 'lang="fr"' in _html(r) if lang != "fr" else True
        assert '<html lang="ar" dir="rtl"' in _html(client.get("/ar/parcours/"))

    def test_post_not_allowed(self, client, pathways_seeded, phase3_open):
        assert client.post(PATHWAY_URL).status_code == 405


class TestPhase3Detail:
    @pytest.mark.parametrize("entry", LOCKED_ENTRIES, ids=[e["key"] for e in LOCKED_ENTRIES])
    def test_each_pathway_renders_locked_title_and_description(self, client, pathways_seeded, phase3_open, entry):
        r = client.get(f"{PATHWAY_URL}{entry['key']}/")
        assert r.status_code == 200
        html = _html(r)
        assert html.count("<h1") == 1
        assert re.search(rf'<h1 class="ingresso__title[^"]*">{re.escape(escape(entry["title"]))}</h1>', html)
        assert escape(entry["description"]) in html
        assert f'data-pathway="{entry["key"]}"' in html
        assert 'data-callout="antifraud"' in html
        # V5.22 (SECTION_SYSTEM_V2 §3.5 PS-3; strict rule): «la protezione», the body read whole in its element
        assert _locked_text(html, "p3.antifraud.body") == locked_content.text("p3.antifraud.body", "fr")
        assert 'data-metadata="pathway"' in html
        assert "Contenu informatif — les décisions relèvent des autorités compétentes" in html
        # V5.12 §8: the index names exactly the chapters drawn; one never stands empty or «being verified»
        for anchor in ("apercu", "etapes", "documentation", "autorites", "avertissements", "ressources", "orientation"):
            assert (f'href="#{anchor}"' in html) == (f'id="{anchor}"' in html), anchor
        for anchor in ("avertissements", "ressources", "orientation"):
            assert f'id="{anchor}"' in html
        for words in ("en cours de vérification", "en préparation", "au fur et à mesure", "en cours d’identification"):
            assert words not in html, words
        if entry["key"] == "training_in_origin_country":
            assert ORIGIN_NOTICE in html
        else:
            assert ORIGIN_NOTICE not in html

    def test_timeline_skeleton_headings_only(self, client, pathways_seeded, phase3_open):
        html = _html(client.get(f"{PATHWAY_URL}salaried_work/"))
        assert 'data-steps="5"' in html
        assert "S’orienter" in html
        assert "Accompagnement après l’arrivée" in html
        # V5.22 (SECTION_SYSTEM_V2 §3.5 PS-1 «il filo»; strict rule): the milestones still say they are being verified
        # (their node's dashed edge), headings only
        assert "filo__tappa--attesa" in html
        assert "au fur et à mesure" not in html
        assert "Sportello Unico per l’Immigrazione" in html
        assert 'data-glossary="' in html

    def test_reviewed_step_text_is_rendered_pending_text_is_not(self, client, pathways_seeded, phase3_open):
        p = Pathway.objects.get(key="salaried_work")
        step = p.steps.get(order=1)
        step.text_fr = "TEXTE PENDING NE DOIT PAS APPARAITRE"
        step.save()
        html = _html(client.get(f"{PATHWAY_URL}salaried_work/"))
        assert "TEXTE PENDING NE DOIT PAS APPARAITRE" not in html
        step.pending_legal_review = False
        step.text_fr = "Texte vérifié visible"
        step.save()
        html = _html(client.get(f"{PATHWAY_URL}salaried_work/"))
        assert "Texte vérifié visible" in html

    def test_reviewed_warning_rendered(self, client, pathways_seeded, phase3_open):
        p = Pathway.objects.get(key="salaried_work")
        PathwayWarning.objects.create(pathway=p, order=1, text_fr="Avertissement vérifié", pending_legal_review=False)
        PathwayWarning.objects.create(pathway=p, order=2, text_fr="Avertissement caché", pending_legal_review=True)
        html = _html(client.get(f"{PATHWAY_URL}salaried_work/"))
        assert "Avertissement vérifié" in html
        assert "Avertissement caché" not in html

    def test_breadcrumbs(self, client, pathways_seeded, phase3_open):
        html = _html(client.get(f"{PATHWAY_URL}family_reunification/"))
        assert 'href="/fr/parcours/">Espace Personnes</a>' in html
        assert 'aria-current="page"' in html
        assert "Regroupement familial" in html

    def test_metadata_row_shows_last_reviewed_date(self, client, pathways_seeded, phase3_open):
        import datetime as dt

        p = Pathway.objects.get(key="salaried_work")
        p.last_reviewed_at = dt.datetime(2026, 10, 1, 9, 0, tzinfo=dt.UTC)
        p.save()
        html = _html(client.get(f"{PATHWAY_URL}salaried_work/"))
        assert "01.10.2026" in html
        assert "<time" in html

    def test_unknown_key_404(self, client, pathways_seeded, phase3_open):
        assert client.get(f"{PATHWAY_URL}tourism/").status_code == 404

    def test_detail_rtl(self, client, pathways_seeded, phase3_open):
        r = client.get("/ar/parcours/salaried_work/")
        assert r.status_code == 200
        assert '<html lang="ar" dir="rtl"' in _html(r)

    def test_empty_chapters_are_not_drawn(self, client, pathways_seeded, phase3_open):
        """V5.12 §8: without steps, documents, authorities or context, those chapters and their index entries go."""
        p = Pathway.objects.get(key="salaried_work")
        PathwayStep.objects.filter(pathway=p).delete()
        p.authorities = []
        p.save()
        html = _html(client.get(f"{PATHWAY_URL}salaried_work/"))
        for anchor in ("apercu", "etapes", "documentation", "autorites"):
            assert f'id="{anchor}"' not in html and f'href="#{anchor}"' not in html, anchor
        assert "Étapes en préparation" not in html and "Contexte en cours de vérification" not in html
        assert "Liste en cours de vérification" not in html and "Acteurs en cours d’identification" not in html
        assert 'id="avertissements"' in html and 'data-callout="antifraud"' in html

    def test_the_origin_country_notice_keeps_the_overview(self, client, pathways_seeded, phase3_open):
        html = _html(client.get(f"{PATHWAY_URL}training_in_origin_country/"))
        assert 'id="apercu"' in html and 'href="#apercu"' in html
        assert 'data-notice="training-in-origin-country"' in html

    def test_metadata_row_without_a_review_date_is_the_nature_alone(self, client, pathways_seeded, phase3_open):
        html = _html(client.get(f"{PATHWAY_URL}salaried_work/"))
        assert "Contenu informatif — les décisions relèvent des autorités compétentes" in html
        assert "Dernière vérification" not in html and "contenus détaillés en cours de vérification" not in html


class TestDiplomas:
    def test_locked_texts_and_skeleton(self, client, pathways_seeded, phase3_open):
        r = client.get(DIPLOMAS_URL)
        assert r.status_code == 200
        html = _html(r)
        assert html.count("<h1") == 1
        assert DIPLOMAS_TITLE in html
        assert DIPLOMAS_BODY in html
        assert 'data-steps="5"' in html
        assert "Légalisation ou apostille" in html
        assert "Déclaration de valeur" in html
        assert "Dichiarazione di valore" in html
        assert 'data-callout="antifraud"' in html
        assert 'href="/fr/parcours/">Espace Personnes</a>' in html

    def test_no_recognition_claim_outside_locked_text(
        self, client, pathways_seeded, phase3_open, strip_locked_fn, visible_text_fn
    ):
        html = _html(client.get(DIPLOMAS_URL))
        remaining = visible_text_fn(strip_locked_fn(html)).lower()
        for token in ("reconnaît", "reconnaissons", "riconosce", "recognises", "recognizes", "omologa", "equivalenze"):
            assert token not in remaining, token

    def test_rtl(self, client, pathways_seeded, phase3_open):
        assert client.get("/ar/diplomes-et-titres/").status_code == 200


class TestTraining:
    def test_two_phases_before_and_after(self, client, pathways_seeded, phase3_open):
        r = client.get(TRAINING_URL)
        assert r.status_code == 200
        html = _html(r)
        assert html.count("<h1") == 1
        assert 'data-phases="2"' in html
        assert 'id="avant-le-depart"' in html
        assert 'id="apres-l-arrivee"' in html
        assert html.index('id="avant-le-depart"') < html.index('id="apres-l-arrivee"')
        assert "Formation avant le départ" in html
        assert TRAINING_AFTER_TITLE in html
        # V5.22 (SECTION_SYSTEM_V2 §3.9 F1; strict rule): the body whole, its first sentence set larger in place
        assert _locked_text(html, "p3.training_after.body") == locked_content.text("p3.training_after.body", "fr")
        assert BEFORE_DEPARTURE_NOTICE in html
        assert 'href="/fr/parcours/training_in_origin_country/"' in html
        assert 'data-callout="antifraud"' in html

    def test_no_ministerial_approval_claim(
        self, client, pathways_seeded, phase3_open, strip_locked_fn, visible_text_fn
    ):
        text = visible_text_fn(strip_locked_fn(_html(client.get(TRAINING_URL)))).lower()
        for token in (
            "approbation ministérielle",
            "approvazione ministeriale",
            "attestation ministérielle",
            "canal actif",
            "corridoio operativo",
        ):
            assert token not in text, token

    def test_rtl(self, client, pathways_seeded, phase3_open):
        assert client.get("/ar/formation/").status_code == 200


# ---- sitemap --------------------------------------------------------------------------------


class TestSitemap:
    def test_sitemap_lists_only_index_while_gated(self, client, pathways_seeded, before_phase3):
        r = client.get("/sitemap.xml")
        assert r.status_code == 200
        xml = _html(r)
        assert "/fr/parcours/</loc>" in xml
        assert "/fr/parcours/salaried_work/" not in xml
        assert "/fr/diplomes-et-titres/" not in xml
        assert "/fr/formation/" not in xml

    def test_sitemap_lists_gated_pages_when_open(self, client, pathways_seeded, phase3_open):
        xml = _html(client.get("/sitemap.xml"))
        assert "/fr/parcours/</loc>" in xml
        for key in PATHWAY_KEYS:
            assert f"/fr/parcours/{key}/</loc>" in xml
        assert "/ar/parcours/salaried_work/</loc>" in xml
        assert "/fr/diplomes-et-titres/</loc>" in xml
        assert "/fr/formation/</loc>" in xml

    def test_sitemap_skips_unpublished_pathway(self, client, pathways_seeded, phase3_open):
        p = Pathway.objects.get(key="other_regular_routes")
        p.status = PublicationStatus.DRAFT
        p.save()
        xml = _html(client.get("/sitemap.xml"))
        assert "/fr/parcours/other_regular_routes/" not in xml
        assert "/fr/parcours/salaried_work/</loc>" in xml
