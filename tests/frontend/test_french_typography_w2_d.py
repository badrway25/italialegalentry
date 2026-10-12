"""
The French-spacing filter of the home's chapters (design V5.4, plan §1.1 «French spacing — never inside locked
copy»; W2-D step 3): ``{{ text|typo }}`` in ``apps/pages/templatetags/pages_typo.py``.

Two promises, both held here. Team-authored strings — the catalogue's interface strings, the editorial columns of
the back office — get a no-break space beside French high punctuation, so that a line never starts with a colon
or ends on an opening guillemet. A prescribed text never changes by a character: the filter is not applied to
locked variables, and if it were it would hand them back untouched.
"""

from __future__ import annotations

import pytest
from django.utils.html import escape
from django.utils.safestring import SafeString, mark_safe

from cms import locked_content
from pages.templatetags.pages_typo import NBSP, is_prescribed, typo


def _registry_strings() -> list[str]:
    found: list[str] = []

    def walk(value) -> None:
        if isinstance(value, str):
            found.append(value)
        elif isinstance(value, dict):
            for item in value.values():
                walk(item)
        elif isinstance(value, (list, tuple)):
            for item in value:
                walk(item)

    for table in locked_content.LOCKED_TEXTS.values():
        walk(table)
    return found


def test_the_no_break_space_is_u00a0_and_written_as_an_escape():
    """Host Grotesk carries no U+202F (plan §1.1): French uses U+00A0. In the source it is an escape — a literal
    no-break space is invisible, and the next editor's tool would turn it into a space."""
    from pathlib import Path

    assert NBSP == "\u00a0"
    source = (Path(__file__).resolve().parents[2] / "apps" / "pages" / "templatetags" / "pages_typo.py").read_bytes()
    assert b"\xc2\xa0" not in source and b'NBSP = "\\u00a0"' in source


@pytest.mark.parametrize(
    "written, drawn",
    [
        (
            "Des besoins au suivi : la séquence, étape par étape.",
            "Des besoins au suivi\u00a0: la séquence, étape par étape.",
        ),
        ("Lire la page « Attention aux fraudes »", "Lire la page «\u00a0Attention aux fraudes\u00a0»"),
        ("Qui ? Quoi ! Où ; ici", "Qui\u00a0? Quoi\u00a0! Où\u00a0; ici"),
        ("Actualités", "Actualités"),
        ("Voir l’Espace Personnes", "Voir l’Espace Personnes"),
        # the other languages set no space there: nothing to change
        ("Dalle esigenze delle imprese al seguito: la sequenza, passo dopo passo.", None),
        ("From companies' needs to follow-up: the sequence, step by step.", None),
        ("من احتياجات الشركات إلى المتابعة: تسلسل المشروع التجريبي، مرحلة بمرحلة.", None),
    ],
)
def test_a_team_authored_string_gets_its_no_break_spaces(written, drawn):
    assert typo(written) == (written if drawn is None else drawn)
    assert typo(typo(written)) == typo(written), "applied twice, it changes nothing more"
    # no word, no other space and no hyphen moves: the string is the same but for the spaces it replaced
    assert typo(written).replace(NBSP, " ") == written


def test_a_prescribed_text_is_handed_back_byte_for_byte():
    """Every string of the registry, the short labels included (they carry no six-word run), in every language."""
    strings = _registry_strings()
    assert len(strings) > 200
    spaced = [s for s in strings if " ?" in s or " :" in s or "« " in s or " »" in s or " !" in s or " ;" in s]
    assert len(spaced) >= 20, "the registry does hold French high punctuation: the guard is not idle"
    for string in strings:
        assert is_prescribed(string) or " " not in string
        assert typo(string) == string, string[:80]


def test_escaping_is_left_to_the_template():
    """A plain string comes back plain (the template escapes it), a safe one comes back safe: no markup is added."""
    plain = typo("Fish & chips : oui")
    assert not isinstance(plain, SafeString) and plain == "Fish & chips\u00a0: oui"
    safe = typo(mark_safe("Fish &amp; chips : oui"))
    assert isinstance(safe, SafeString) and safe == "Fish &amp; chips\u00a0: oui"
    assert typo(None) == "" and typo("") == ""


@pytest.mark.django_db
def test_the_home_draws_its_own_strings_with_the_spaces_and_the_locked_copy_as_written(client, seeded, phase3_open):
    html = client.get("/fr/").content.decode("utf-8")
    main = html.split('<main id="main-content"', 1)[1].split("</main>", 1)[0]
    # team-authored: the pilot's sentence (a section intro) and the anti-fraud link (an interface string)
    assert "au suivi\u00a0: la séquence du projet pilote" in main
    assert "Lire la page «\u00a0Attention aux fraudes\u00a0»" in main
    # prescribed: whole, with their ordinary spaces — the questions of the trust chapter, the warning, the sentence
    # of the orientation chapter
    faq = {item["key"]: item for item in locked_content.get("p3.faq.items", "fr")[0]}
    for key in ("faq_visas", "faq_recruitment_agency", "faq_preassessment_guarantee", "faq_diplomas"):
        assert " ?" in faq[key]["question"]
        assert escape(faq[key]["question"]) in main, key
        assert escape(faq[key]["answer"]) in main, key
    for key in ("p3.antifraud.body", "p3.persons.how_it_works", "p3.hero.body"):
        assert str(escape(locked_content.text(key, "fr"))) in main, key
    # and no locked element of the page carries a no-break space the registry does not hold
    registry = "".join(_registry_strings())
    assert NBSP not in registry
    assert main.count(NBSP) == main.count("\u00a0: ") + main.count("«\u00a0") + main.count("\u00a0»") + main.count(
        "\u00a0? "
    ) + main.count("\u00a0; ") + main.count("\u00a0! "), "every no-break space of the page is one the filter wrote"


@pytest.mark.django_db
def test_the_interim_home_keeps_a_colon_with_its_sentence(client, seeded):
    """Gate G3 closed — what the site shows today: « … ou autorisation : ces décisions … » broke before its colon
    on a phone."""
    html = client.get("/fr/").content.decode("utf-8")
    block = html.split('data-section="trust"', 1)[1].split("</section>", 1)[0]
    assert "permis ou autorisation\u00a0: ces décisions" in block
    assert str(escape(locked_content.text("p1.persons.replacement_2", "fr"))) in block
