"""
Catalogue hygiene: files, headers, plural rules, coverage, compiled catalogues, terminology, locked-text
leaks and catalogue ↔ sources synchronisation. No database needed.
"""

from __future__ import annotations

import gettext as gettext_module
import json
import os
import subprocess
import sys

import pytest
from django.utils import translation
from django.utils.translation import gettext, ngettext

from .conftest import ROOT, TRANSLATED

pytestmark = pytest.mark.compliance

EXPECTED_NPLURALS = {"it": 2, "en": 2, "ar": 6, "fr": 2}
#: n → expected plural index, per language (CLDR rules used by gettext).
PLURAL_SAMPLES = {
    "it": {0: 1, 1: 0, 2: 1, 11: 1, 100: 1},
    "en": {0: 1, 1: 0, 2: 1, 11: 1, 100: 1},
    "fr": {0: 0, 1: 0, 2: 1, 11: 1, 100: 1},
    "ar": {0: 0, 1: 1, 2: 2, 3: 3, 10: 3, 11: 4, 99: 4, 100: 5, 101: 5, 102: 5, 103: 3, 111: 4},
}

#: French source → approved rendering. A change here is a terminology decision (docs/I18N_RTL.md §5).
GLOSSARY = {
    "Accueil": {"it": "Pagina iniziale", "en": "Home", "ar": "الرئيسية"},
    "Personnes": {"it": "Persone", "en": "Individuals", "ar": "الأفراد"},
    "Entreprises": {"it": "Imprese", "en": "Enterprises", "ar": "الشركات"},
    "Institutions": {"it": "Istituzioni", "en": "Institutions", "ar": "المؤسسات"},
    "Universités et organismes de formation": {
        "it": "Università e organismi di formazione",
        "en": "Universities and training bodies",
        "ar": "الجامعات وهيئات التكوين",
    },
    "Espace réservé": {"it": "Area riservata", "en": "Reserved area", "ar": "الفضاء الخاص"},
    "Attention aux fraudes": {"it": "Attenzione alle frodi", "en": "Beware of fraud", "ar": "احذروا الاحتيال"},
    "Questionnaire d’orientation": {
        "it": "Questionario di orientamento",
        "en": "Orientation questionnaire",
        "ar": "استبيان التوجيه",
    },
    "Retour à l’accueil": {
        "it": "Torna alla pagina iniziale",
        "en": "Back to the home page",
        "ar": "العودة إلى الصفحة الرئيسية",
    },
    "Aller au contenu principal": {
        "it": "Vai al contenuto principale",
        "en": "Skip to main content",
        "ar": "الانتقال إلى المحتوى الرئيسي",
    },
    "Se connecter": {"it": "Accedi", "en": "Sign in", "ar": "تسجيل الدخول"},
    "Informations légales": {"it": "Informazioni legali", "en": "Legal information", "ar": "المعلومات القانونية"},
}

#: Proper nouns, trademark and document names that stay in the original in every language.
KEPT_VERBATIM = (
    "Italy Legal Entry™",
    "AGAMI — Dialogo Giuridico Interculturale APS",
    "Privacy Policy",
    "Cookie Policy",
    "Vénétie–Maroc",
    "contact@agamieuromed.org",
)

PO_HEADER = (
    'msgid ""\nmsgstr ""\n"Language: {lang}\\n"\n"Content-Type: text/plain; charset=UTF-8\\n"\n'
    '"Plural-Forms: nplurals=2; plural=(n != 1);\\n"\n\n'
)


@pytest.mark.parametrize("lang", TRANSLATED)
def test_po_and_mo_files_exist(audit, lang):
    assert audit.po_path(lang).is_file()
    assert audit.mo_path(lang).is_file()
    assert audit.mo_path(lang).stat().st_size > 10_000


@pytest.mark.parametrize("lang", [*TRANSLATED, "fr"])
def test_headers_and_plural_rule(audit, lang):
    fields = audit.header_fields(audit.parse_po(audit.po_path(lang)))
    assert fields["Language"] == lang
    assert "charset=UTF-8" in fields["Content-Type"]
    assert f"nplurals={EXPECTED_NPLURALS[lang]};" in fields["Plural-Forms"].replace(" ", "")
    expression = fields["Plural-Forms"].split("plural=", 1)[1].rstrip(";")
    plural = gettext_module.c2py(expression)
    for n, index in PLURAL_SAMPLES[lang].items():
        assert plural(n) == index, (lang, n)


@pytest.mark.parametrize("lang", TRANSLATED)
def test_every_entry_is_translated_and_none_is_fuzzy(catalogues, lang):
    nplurals = EXPECTED_NPLURALS[lang]
    assert len(catalogues[lang]) > 1500
    untranslated = [e.msgid for e in catalogues[lang].values() if not e.is_translated(nplurals)]
    fuzzy = [e.msgid for e in catalogues[lang].values() if e.is_fuzzy]
    assert untranslated == []
    assert fuzzy == []
    for entry in catalogues[lang].values():
        if entry.is_plural:
            assert sorted(entry.msgstr) == list(range(nplurals)), entry.msgid


def test_the_three_catalogues_carry_the_same_msgids(catalogues):
    assert set(catalogues["it"]) == set(catalogues["en"]) == set(catalogues["ar"])


@pytest.mark.parametrize("lang", [*TRANSLATED, "fr"])
def test_compiled_catalogue_matches_its_po(audit, lang):
    assert audit.mo_differences(lang) == []


@pytest.mark.parametrize("lang", TRANSLATED)
def test_glossary_terms_keep_their_approved_translation(catalogues, lang):
    for source, expected in GLOSSARY.items():
        assert catalogues[lang][(None, source)].msgstr[0] == expected[lang], source


@pytest.mark.parametrize("lang", TRANSLATED)
def test_compiled_catalogue_is_loaded_by_django(lang):
    with translation.override(lang):
        for source, expected in GLOSSARY.items():
            assert gettext(source) == expected[lang]


def test_french_stays_the_source_language():
    with translation.override("fr"):
        assert gettext("Accueil") == "Accueil"
        assert gettext("Aller au contenu principal") == "Aller au contenu principal"
        # Back-office strings written in Italian are normalised by the small fr catalogue.
        assert gettext("Nome e cognome") != "Nome e cognome"


def test_arabic_plural_forms_are_selected_by_django(catalogues):
    entry = catalogues["ar"][(None, "%(counter)s résultat pour « %(q)s »")]
    assert len(set(entry.msgstr.values())) >= 5, "the six Arabic forms must not be copies of one another"
    with translation.override("ar"):
        for n, index in PLURAL_SAMPLES["ar"].items():
            got = ngettext("%(counter)s résultat pour « %(q)s »", "%(counter)s résultats pour « %(q)s »", n)
            assert got == entry.msgstr[index], n


@pytest.mark.parametrize("lang", ["it", "en"])
def test_two_form_plurals_are_selected_by_django(catalogues, lang):
    entry = catalogues[lang][(None, "%(n)s fiche")]
    with translation.override(lang):
        assert ngettext("%(n)s fiche", "%(n)s fiches", 1) == entry.msgstr[0]
        assert ngettext("%(n)s fiche", "%(n)s fiches", 2) == entry.msgstr[1]
        assert entry.msgstr[0] != entry.msgstr[1]


@pytest.mark.parametrize("lang", TRANSLATED)
def test_proper_nouns_trademark_and_policy_names_stay_verbatim(catalogues, lang):
    for entry in catalogues[lang].values():
        for kept in KEPT_VERBATIM:
            if kept in entry.msgid:
                for value in entry.msgstr.values():
                    assert kept in value, (lang, entry.msgid)


@pytest.mark.parametrize("lang", TRANSLATED)
def test_no_forbidden_formulation_in_the_translations(catalogues, lang):
    from cms.forbidden import scan

    for entry in catalogues[lang].values():
        for value in entry.msgstr.values():
            assert "®" not in value, entry.msgid
            if not scan(entry.msgid):
                assert not scan(value), (lang, entry.msgid, scan(value))


def test_arabic_catalogue_is_arabic_script_western_digits_no_mojibake(audit, catalogues):
    for entry in catalogues["ar"].values():
        keep = audit.KEEP_AS_IS.match(entry.msgid.strip()) or entry.msgid in audit.KEEP_SOURCE
        for value in entry.msgstr.values():
            assert not audit._ARABIC_INDIC_DIGITS.search(value), entry.msgid
            assert not audit._MOJIBAKE.search(value), entry.msgid
            assert keep or audit._ARABIC.search(value), entry.msgid


# ---------------------------------------------------------------------------------------------
# Locked texts never enter a catalogue
# ---------------------------------------------------------------------------------------------
def test_locked_index_detects_a_six_word_fragment(audit):
    from cms import locked_content

    index = audit.LockedIndex()
    assert audit.FRAGMENT_SHINGLE_WORDS <= 6
    title = locked_content.text("p1.companies.title", "fr")
    assert index.match(title) == "p1.companies.title"
    words = audit._words(audit.normalise(locked_content.text("p3.persons.intro", "fr")))
    six = " ".join(words[20:26])
    assert index.match(f"Texte d’interface : {six} — fin.") == "p3.persons.intro"
    assert index.match("Texte d’interface : " + " ".join(words[20:25]) + " — fin.") == "", "five words are not a hit"
    assert index.match("Aller au contenu principal") == ""
    assert index.match("Retour à la page précédente du questionnaire, sans perte des réponses déjà saisies.") == ""


@pytest.mark.parametrize("lang", TRANSLATED)
def test_no_unreviewed_locked_fragment_in_the_catalogue(audit, catalogues, lang):
    index = audit.LockedIndex()
    for entry in catalogues[lang].values():
        for source in filter(None, (entry.msgid, entry.msgid_plural)):
            if index.match(source):
                assert entry.msgid in audit.REVIEWED_OVERLAPS or entry.msgid in audit.KEEP_SOURCE, entry.msgid


@pytest.mark.parametrize("lang", TRANSLATED)
def test_locked_derived_msgids_are_never_translated(audit, catalogues, lang):
    for msgid in audit.KEEP_SOURCE:
        entry = catalogues[lang].get((None, msgid))
        if entry is not None:  # the owner may have reworded the template since
            assert entry.msgstr[0] == msgid


def test_every_overlap_decision_is_justified(audit):
    for table in (audit.REVIEWED_OVERLAPS, audit.KEEP_SOURCE):
        for msgid, why in table.items():
            assert len(why) >= 30, msgid


# ---------------------------------------------------------------------------------------------
# Catalogue ↔ sources
# ---------------------------------------------------------------------------------------------
def test_source_scanner_reads_templates_and_python(audit):
    template = (
        '{% load i18n %}<p>{% translate "Bonjour" %}</p>'
        "{% blocktranslate count n=x %}{{ n }} fiche{% plural %}{{ n }} fiches{% endblocktranslate %}"
        '{% translate "Mai" context "mois" %}{{ _("Salut") }}'
    )
    assert audit._messages_in_template(template, "x.html") == [
        (None, "Bonjour", None),
        (None, "%(n)s fiche", "%(n)s fiches"),
        ("mois", "Mai", None),
        (None, "Salut", None),
    ]
    python = (
        "from django.utils.translation import gettext_lazy as _, ngettext, pgettext\n"
        'A = _("Un" " deux")\nB = ngettext("%(n)d jour", "%(n)d jours", 2)\nC = pgettext("ctx", "Mot")\nD = _(A)\n'
    )
    assert audit._messages_in_python(python) == [
        (None, "Un deux", None),
        (None, "%(n)d jour", "%(n)d jours"),
        ("ctx", "Mot", None),
    ]


@pytest.mark.parametrize("lang", TRANSLATED)
def test_every_source_message_is_in_the_catalogue(audit, catalogues, lang):
    """
    A {% translate %} / gettext string added without a catalogue entry would be served in French on the
    Italian, English and Arabic sites. Fix: ``scripts/i18n_audit.py --sync``, translate, ``--compile``.
    """
    missing = sorted(
        f"{msgid!r} ({sorted(message.files)[0]})"
        for (msgctxt, msgid), message in audit.source_messages().items()
        if (msgctxt, msgid) not in catalogues[lang]
    )
    assert missing == [], f"{len(missing)} message(s) missing from locale/{lang}: run scripts/i18n_audit.py --sync"


def test_sync_adds_new_messages_and_drops_unused_ones(audit, tmp_path, monkeypatch):
    target = tmp_path / "locale" / "it" / "LC_MESSAGES"
    target.mkdir(parents=True)
    (target / "django.po").write_text(
        PO_HEADER.format(lang="it")
        + '#: .\\a.py\nmsgid "Garder"\nmsgstr "Tenere"\n\n#: .\\a.py\nmsgid "Retirer"\nmsgstr "Togliere"\n',
        encoding="utf-8",
    )
    monkeypatch.setattr(audit, "LOCALE_DIR", tmp_path / "locale")
    sources = {
        (None, "Garder"): audit.SourceMessage({"a.py"}),
        (None, 'Nouveau "texte"'): audit.SourceMessage({"templates/b.html"}),
        (None, "%(n)s jour"): audit.SourceMessage({"templates/b.html"}, "%(n)s jours"),
    }
    assert audit.sync_catalogue("it", 2, sources) == (2, 1)
    entries = {e.msgid: e for e in audit.parse_po(audit.po_path("it")) if not e.is_header}
    assert set(entries) == {"Garder", 'Nouveau "texte"', "%(n)s jour"}
    assert entries["Garder"].msgstr[0] == "Tenere"
    assert entries['Nouveau "texte"'].msgstr[0] == ""
    assert entries["%(n)s jour"].msgid_plural == "%(n)s jours"
    assert entries["%(n)s jour"].msgstr == {0: "", 1: ""}
    assert audit.sync_catalogue("it", 2, sources) == (0, 0), "sync must be idempotent"
    audit.compile_po("it")
    report = audit.audit_language("it", 2, audit.LockedIndex([]), sources)
    assert not report.ok
    assert report.untranslated == 2
    assert report.missing_from_catalogue == []


def test_pure_python_compiler_round_trips(audit, tmp_path, monkeypatch):
    source = audit.po_path("ar").read_text(encoding="utf-8")
    target = tmp_path / "locale" / "ar" / "LC_MESSAGES"
    target.mkdir(parents=True)
    (target / "django.po").write_text(source, encoding="utf-8")
    monkeypatch.setattr(audit, "LOCALE_DIR", tmp_path / "locale")
    compiled = audit.compile_po("ar")
    with compiled.open("rb") as handle:
        catalogue = gettext_module.GNUTranslations(handle)
    assert catalogue.gettext("Accueil") == GLOSSARY["Accueil"]["ar"]
    assert catalogue.ngettext("%(n)s fiche", "%(n)s fiches", 2) != "%(n)s fiches"
    assert audit.mo_differences("ar") == []
    # …and a stale .mo is detected by content, whatever the file dates say.
    stale = source.replace('msgstr "' + GLOSSARY["Accueil"]["ar"] + '"', 'msgstr "البداية"')
    assert stale != source
    (target / "django.po").write_text(stale, encoding="utf-8")
    assert "Accueil" in audit.mo_differences("ar")


# ---------------------------------------------------------------------------------------------
# The audit script itself (coverage gate)
# ---------------------------------------------------------------------------------------------
def test_audit_script_succeeds_with_full_coverage():
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "i18n_audit.py"), "--json"],
        capture_output=True,
        cwd=ROOT,
        env=env,
        timeout=300,
    )
    assert result.returncode == 0, result.stdout.decode("utf-8", "replace")[-3000:]
    payload = json.loads(result.stdout.decode("utf-8"))
    assert payload["ok"] is True
    by_lang = {row["language"]: row for row in payload["languages"]}
    assert set(TRANSLATED) <= set(by_lang)
    for lang in TRANSLATED:
        row = by_lang[lang]
        assert row["coverage"] == 100.0
        assert row["untranslated"] == row["fuzzy"] == 0
        assert row["locked_fragments"] == []
        assert row["missing_from_catalogue"] == []
        assert row["nplurals"] == EXPECTED_NPLURALS[lang]


def test_audit_fails_on_an_untranslated_or_locked_msgid(audit, tmp_path, monkeypatch):
    from cms import locked_content

    locked = locked_content.text("p1.companies.title", "fr")
    target = tmp_path / "locale" / "en" / "LC_MESSAGES"
    target.mkdir(parents=True)
    (target / "django.po").write_text(
        PO_HEADER.format(lang="en")
        + f'msgid "Bonjour"\nmsgstr ""\n\nmsgid "{locked}"\nmsgstr "Which profiles does your company need?"\n',
        encoding="utf-8",
    )
    monkeypatch.setattr(audit, "LOCALE_DIR", tmp_path / "locale")
    audit.compile_po("en")
    report = audit.audit_language("en", 2, audit.LockedIndex())
    assert report.ok is False
    assert report.untranslated_msgids == ["Bonjour"]
    assert [item["locked_key"] for item in report.locked_fragments] == ["p1.companies.title"]


# ---------------------------------------------------------------------------------------------
# Bidi: the trademark sign inside Arabic sentences
# ---------------------------------------------------------------------------------------------
def test_arabic_trademark_sign_is_anchored_by_a_left_to_right_mark(audit, catalogues):
    """« ™ » is bidi-neutral: without U+200E after it, an Arabic sentence shows « ™Italy Legal Entry »."""
    carrying = 0
    for entry in catalogues["ar"].values():
        for value in entry.msgstr.values():
            if "™" not in value or not audit._ARABIC.search(value):
                continue
            carrying += 1
            assert not audit._TRADEMARK_WITHOUT_LRM.search(value), entry.msgid
            for placeholder in audit.BRAND_PLACEHOLDERS:
                assert placeholder not in value or placeholder + audit.LRM in value, entry.msgid
    assert carrying >= 10
    # The mark is a rendering aid of the right-to-left catalogue only.
    for lang in ("it", "en"):
        assert not any(audit.LRM in value for e in catalogues[lang].values() for value in e.msgstr.values()), lang


def test_audit_fails_on_an_arabic_trademark_without_the_left_to_right_mark(audit, tmp_path, monkeypatch):
    target = tmp_path / "locale" / "ar" / "LC_MESSAGES"
    target.mkdir(parents=True)
    header = PO_HEADER.format(lang="ar").replace(
        "nplurals=2; plural=(n != 1);",
        "nplurals=6; plural=n==0 ? 0 : n==1 ? 1 : n==2 ? 2 : n%100>=3 && n%100<=10 ? 3 : n%100>=11 ? 4 : 5;",
    )
    body = (
        'msgid "Italy Legal Entry™ pour les personnes"\nmsgstr "Italy Legal Entry™{mark} للأفراد"\n\n'
        'msgid "%(project)s est promu par %(promoter)s."\nmsgstr "%(project)s{mark} مشروع تروّج له %(promoter)s."\n'
    )
    monkeypatch.setattr(audit, "LOCALE_DIR", tmp_path / "locale")
    (target / "django.po").write_text(header + body.format(mark=""), encoding="utf-8")
    audit.compile_po("ar")
    report = audit.audit_language("ar", 6, audit.LockedIndex([]))
    assert report.ok is False
    assert sum("U+200E" in error for error in report.errors) == 2, report.errors
    (target / "django.po").write_text(header + body.format(mark=audit.LRM), encoding="utf-8")
    audit.compile_po("ar")
    assert audit.audit_language("ar", 6, audit.LockedIndex([])).ok is True


# ---------------------------------------------------------------------------------------------
# The source-language catalogue normalises the Italian back-office strings
# ---------------------------------------------------------------------------------------------
def test_french_catalogue_leaves_no_italian_sentence_untranslated(audit):
    assert audit.unnormalised_source_msgids(audit.parse_po(audit.po_path("fr"))) == []


def test_audit_fails_on_an_italian_msgid_copied_into_the_french_catalogue(audit, tmp_path, monkeypatch):
    italian_source = "Stato dei gate di pubblicazione"
    french_source = "Retour à la page précédente"
    for lang, second in (("it", "Torna alla pagina precedente"), ("fr", french_source)):
        target = tmp_path / "locale" / lang / "LC_MESSAGES"
        target.mkdir(parents=True)
        plural = "(n != 1)" if lang == "it" else "(n > 1)"
        (target / "django.po").write_text(
            PO_HEADER.format(lang=lang).replace("(n != 1)", plural)
            + f'msgid "{italian_source}"\nmsgstr "{italian_source}"\n\n'
            + f'msgid "{french_source}"\nmsgstr "{second}"\n\nmsgid "Menu"\nmsgstr "Menu"\n',
            encoding="utf-8",
        )
    monkeypatch.setattr(audit, "LOCALE_DIR", tmp_path / "locale")
    audit.compile_po("fr")
    report = audit.audit_language("fr", 2, audit.LockedIndex([]))
    assert report.ok is False
    assert [error for error in report.errors if "Italian-source" in error and italian_source in error]
    assert not [error for error in report.errors if french_source in error or "« Menu »" in error]
    fixed = (
        audit.po_path("fr")
        .read_text(encoding="utf-8")
        .replace(f'msgstr "{italian_source}"', 'msgstr "État des gates de publication"')
    )
    audit.po_path("fr").write_text(fixed, encoding="utf-8")
    audit.compile_po("fr")
    assert audit.audit_language("fr", 2, audit.LockedIndex([])).ok is True


def test_audit_fails_on_a_duplicate_msgid(audit, tmp_path, monkeypatch):
    """GNU msgfmt refuses duplicates; the pure-Python compiler would keep the last one without a word."""
    target = tmp_path / "locale" / "en" / "LC_MESSAGES"
    target.mkdir(parents=True)
    (target / "django.po").write_text(
        PO_HEADER.format(lang="en") + 'msgid "Bonjour"\nmsgstr "Hello"\n\nmsgid "Bonjour"\nmsgstr "Good morning"\n',
        encoding="utf-8",
    )
    monkeypatch.setattr(audit, "LOCALE_DIR", tmp_path / "locale")
    audit.compile_po("en")
    report = audit.audit_language("en", 2, audit.LockedIndex([]))
    assert report.ok is False
    assert any("duplicate msgid" in error for error in report.errors), report.errors
