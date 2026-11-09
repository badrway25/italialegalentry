"""
Arabic completeness — the rendered product shows no unintended French to an Arabic reader (V5.24 §4–§6, §22; V5.27 §3, §5;
FINAL_DELIVERY_V2.md R7′ (g), §3.8; lane AR, label v524-ar). Non-browser: Django's test client and the suite's fixtures.

What a French run on ``/ar/`` may be, and nothing else:

* a proper name, an acronym or an Italian legal term of the controlled allowlist (``arabic_allowlist``, each with its reason);
* an official title kept in the original (C-OFFICIAL — computed from the registry, R7′ (4)), isolated by its ``lang``;
* a SUBSTANTIVE prescribed text (C-SUBST-FR) on its OWN page, isolated as French and preceded by its identification caption
  — anywhere else that text is hidden behind the pointer line (R7′ (3));
* a prescribed text in ``<title>`` / ``<meta name=description>``, where ``lang`` cannot be set — a substantive or official
  one; a compositional one must read Arabic there too;
* the team's acknowledgement derived from a substantive text (its opening clause), on a form it belongs to, isolated as
  French and preceded by that text's caption (``cms.locked_renderings.DERIVED_ROUTES``).

The burn-down table that tolerated the page lanes' last French runs while their contracts were open
(``ARABIC_BURNDOWN``) is CLOSED and deleted with its mechanism (FINAL_DELIVERY_V2 §3.9; the 6 Nov 21:25 note: «CLOSING
asserts ARABIC_BURNDOWN and KEEP_SOURCE EMPTY and deletes the burn-down mechanism if empty»): nothing French is tolerated
any more but by the policy above, and ``test_the_burn_down_is_closed`` keeps it so.

Everything else that reads French — a team string left French, a compositional prescribed text (C-UI) still in French, a
substantive text quoted off its page, a declared ``lang="fr"`` run that is none of the above — is unintended French and
fails the test: «French must never remain merely because translation work was incomplete» (V5.27 §3).

The detector (T1–T4) scores a run for «obvious French» — stop-words, elisions, accents, endings — on runs of three words or
more, so a name, a code, an e-mail, an Italian citation or a single Latin word never trips it; a run EQUAL to a prescribed
text is recognised whatever its length. T5 guards the data the product reads through its translation tables.
"""

from __future__ import annotations

import html as html_module
import re

import pytest
from django.urls import Resolver404, resolve
from django.utils import translation

from cms import locked_renderings

from .arabic_allowlist import (
    ACRONYMS,
    ITALIAN_LEGAL_TERMS,
    KNOWN_FRENCH,
    LANGUAGE_CODES,
    LANGUAGE_NAMES,
    PROPER_NAMES,
    official_texts,
    rendered_texts,
    source_texts,
)
from .conftest import visible_strings

pytestmark = [pytest.mark.compliance, pytest.mark.django_db]

# ---------------------------------------------------------------------------------------------
# the detector
# ---------------------------------------------------------------------------------------------
_CITATION = re.compile(r"\b(?:D\.?\s?Lgs\.?|D\.P\.R\.|DPR|art\.|artt\.|comma|commi|n\.)\s*[0-9/ ,.a-z-]*", re.I)
_EMAIL = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
_URL = re.compile(r"(?:https?://|www\.)\S+")
#: a code: an upper-case hex reference, a lower-case hex digest of 32 characters or more (the questionnaire result's
#: 64-character code: a random digest whose letter pairs «de», «ce» once scored as French — the steward's fix at the
#: v524-ar merge, the detector's intent unchanged), a UUID, an Italian VAT number, a dashed reference
_CODE = re.compile(
    r"\b[0-9A-F]{8,}\b|\b[0-9a-f]{32,}\b|\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b|\bIT\d{11}\b|\b[A-Z]{2}-\d+\b"
)
_UUID = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")

FR_STOPWORDS = frozenset(
    "le la les des du de un une et ou à au aux pour dans sur avec vous votre vos nous notre nos ce cette ces qui que "
    "est sont pas ne par en se sa son ses leur leurs être il elle ils elles plus sans sous chez dont où mais si très "
    "tout tous toute toutes peut peuvent doit doivent sera seront été aussi comme entre".split()
)
_ELISION = re.compile(r"^(?:l|d|qu|n|s|j|c)[’']", re.I)
_ACCENT = re.compile(r"[éèêàçùôîâœÉÈÊÀÇ]")
_ENDING = re.compile(r"(?:tion|ment|eur|euse|ique|ité|aire|elle|eau|aux|ais|ées|ée|és|é)$", re.I)
_WORD = re.compile(r"[A-Za-zÀ-ÿœŒ’'-]+")
_ARABIC = re.compile(r"[؀-ۿ]")


def _strip_allowed(text: str) -> str:
    t = _EMAIL.sub(" ", text)
    t = _URL.sub(" ", t)
    t = _CODE.sub(" ", t)
    t = _CITATION.sub(" ", t)
    for table in (PROPER_NAMES, ITALIAN_LEGAL_TERMS, LANGUAGE_NAMES):
        for name in sorted(table, key=len, reverse=True):
            t = t.replace(name, " ")
    return " ".join(
        w
        for w in t.split()
        if w.strip(".,;:!?«»()\"'’") not in ACRONYMS and w.strip(".,;:!?«»()\"'’") not in LANGUAGE_CODES
    )


def french_score(text: str) -> int:
    """0 for anything that is not an obvious French sentence; >= 4 for one (04_test_spec.md §2)."""
    tokens = [w for w in _WORD.findall(_strip_allowed(text)) if len(w.strip("’'-")) > 1]
    if len(tokens) < 3:
        return 0
    lowered = [w.lower().strip("’'-") for w in tokens]
    stop = sum(w in FR_STOPWORDS for w in lowered)
    elision = sum(bool(_ELISION.match(w)) for w in tokens)
    accent = sum(bool(_ACCENT.search(w)) for w in tokens)
    endings = sum(bool(_ENDING.search(w)) for w in lowered)
    score = 2 * stop + 2 * elision + accent + endings
    if score >= 4 and (stop + elision >= 1 or accent >= 2):
        return score
    return 0


def _norm(text: str) -> str:
    return " ".join(html_module.unescape(text).split())


def _locked_match(text: str, table: dict[str, str]) -> str | None:
    """The sub-key of a prescribed text the run equals or contains (a plate's heading, a <title> with a suffix), or None."""
    t = _norm(text)
    if t in table:
        return table[t]
    for value, subkey in table.items():
        if len(value) >= 12 and (value in t or (len(t) >= 12 and t in value)):
            return subkey
    return None


def _fragment_of(text: str, table: dict[str, str]) -> str | None:
    """The sub-key of a prescribed text the run TRUNCATES (its opening clause, a full stop put where the prescribed
    sentence goes on: «Signalez les besoins professionnels de votre entreprise.», «J’ai lu l’information sur le
    traitement des données personnelles.») — computed from the registry, never typed; None under 24 characters."""
    t = _norm(text).rstrip(" .")
    if len(t) < 24:
        return None
    for value, subkey in table.items():
        if value.startswith(t):
            return subkey
    return None


def _route_of(path: str) -> str:
    """The URL name of a page of the Arabic site ("" when it resolves to nothing)."""
    clean = path.split(" ", 1)[-1]  # «POST x» → x
    with translation.override("ar"):
        try:
            return resolve(f"/ar/{clean}").view_name or ""
        except Resolver404:
            return ""


class Leaks:
    """The findings of one crawl: the unintended French runs."""

    def __init__(self) -> None:
        self.found: dict[str, list[tuple[str, str, str]]] = {}
        self.officials = official_texts()
        self.sources = source_texts()
        self.rendered = rendered_texts()
        self.taxonomy = taxonomy_sources()

    def add(self, path: str, kind: str, text: str, why: str) -> None:
        self.found.setdefault(path, []).append((kind, text[:110], why))

    def page(self, path: str, html: str) -> None:
        route = _route_of(path)
        captions = {locked_renderings.pattern(key) for key in re.findall(r'data-locked-caption="([^"]+)"', html)}
        for effective, kind, text in visible_strings(html, "ar"):
            if _ARABIC.search(text) or not _WORD.search(text):
                continue
            if not _WORD.search(_strip_allowed(text)):
                continue  # a run made only of allowlisted names, endonyms, acronyms, codes (the promoter, «Français»)
            if any(re.search(pattern, text) for pattern, _why in KNOWN_FRENCH.values()):
                continue
            in_head = kind in ("title", "@description")
            if effective in ("it", "en"):
                continue  # a declared Italian or English run: the glossary's terms, «Privacy Policy» — not French
            if kind == "option" and text in self.taxonomy:
                # a select's option is often one word («Vénétie»), below the detector's three: an option that
                # prints a catalogue taxonomy label's French source is a leak whatever its length (v524-ar-fix B2)
                self.add(
                    path, kind, text, "an option in its French source (the catalogue's rendering did not reach it)"
                )
                continue
            # --- a prescribed text, by its value ---------------------------------------------------------------
            if _locked_match(text, self.officials):
                continue  # an official title kept in the original (C-OFFICIAL)
            subkey = _locked_match(text, self.rendered)
            if subkey:  # a compositional text that should read Arabic
                self.add(path, kind, text, f"C-UI {subkey} in French (its rendering did not reach the page)")
                continue
            subkey = _locked_match(text, self.sources)
            if subkey:  # a substantive text: French on its own page, with its caption; hidden elsewhere
                if in_head:
                    continue  # <title> / meta cannot carry lang: the source text is admitted there (R7′)
                on_route = route in locked_renderings.source_routes(subkey)
                if on_route and effective == "fr" and locked_renderings.pattern(subkey) in captions:
                    continue
                why = (
                    "off its source page"
                    if not on_route
                    else ("without lang=fr" if effective != "fr" else "without its caption")
                )
                self.add(path, kind, text, f"C-SUBST-FR {subkey} {why}")
                continue
            # --- anything else -----------------------------------------------------------------------------------
            subkey = _fragment_of(text, {**self.rendered, **self.sources})
            if subkey:  # a literal that truncates a prescribed text (a KEEP_SOURCE msgid, a derived acknowledgement)
                # the team's acknowledgement derived from a substantive text, on a form it belongs to, in French AND
                # identified by that text's caption (R7′ (3) as for the source on its page; cms.locked_renderings
                # DERIVED_ROUTES; FINAL_DELIVERY_V2 §3.9 — the burn-down's five consent rows answered, V5.20: the rows
                # tolerated the run with no caption, this admits it only identified, on its own forms)
                on_form = route in locked_renderings.derived_routes(subkey)
                if on_form and effective == "fr" and locked_renderings.pattern(subkey) in captions:
                    continue
                self.add(path, kind, text, f"a truncation of {subkey} in French")
                continue
            if effective == "fr":
                self.add(path, kind, text, "declared French that is no prescribed text kept by the policy")
                continue
            score = french_score(text)
            if score:
                self.add(path, kind, text, f"French in the page's language (score {score})")

    def report(self) -> str:
        return "\n".join(f"{p} · {k} · {t} · {w}" for p, hits in self.found.items() for k, t, w in hits)


# ---------------------------------------------------------------------------------------------
# fixtures
# ---------------------------------------------------------------------------------------------
def taxonomy_sources() -> frozenset[str]:
    """The French sources of the companies' taxonomy (sectors, territories) the catalogue renders."""
    from companies.models import TAXONOMY_LABELS

    with translation.override(None):
        return frozenset(str(label) for label in TAXONOMY_LABELS)


@pytest.fixture
def open_site(client, seeded, legal_published, phase3_open):
    """Every gate open, so that each registered route renders its real content (forms included)."""
    return client


def _public_pages(client):
    from core.public_routes import all_routes

    for route in all_routes():
        response = client.get(f"/ar/{route.path}")
        if response.status_code == 200:
            yield route.path, response.content.decode()


# ---------------------------------------------------------------------------------------------
# T5 — data completeness (fast, before any page)
# ---------------------------------------------------------------------------------------------
def test_every_seeded_reference_row_has_a_published_arabic_translation(seeded):
    from cms.models import TranslationStatus
    from faq.models import FAQCategory
    from glossary.models import Term
    from orientation.models import ChecklistItem, Choice, Outcome, Question, Ruleset
    from pathways.models import Pathway, PathwayStep

    def missing(rows, label):
        return [
            f"{label}:{r.pk}"
            for r in rows
            if not r.translations.filter(language="ar", status=TranslationStatus.PUBLISHED).exists()
        ]

    gaps = []
    gaps += missing(PathwayStep.objects.filter(pathway__in=Pathway.objects.all()), "pathway step")
    active = Ruleset.objects.filter(status="active").first() or Ruleset.objects.order_by("-version").first()
    assert active is not None, "the orientation ruleset v1 is seeded"
    gaps += missing(Question.objects.filter(ruleset=active), "question")
    gaps += missing(Choice.objects.filter(question__ruleset=active), "choice")
    gaps += missing(Outcome.objects.filter(ruleset=active), "outcome")
    gaps += missing(ChecklistItem.objects.filter(outcome__ruleset=active), "checklist item")
    gaps += missing(FAQCategory.objects.all(), "faq category")
    assert gaps == [], gaps
    # the glossary's terms: the Italian term is kept in every language and its definition is a prescribed text (C-SUBST-FR):
    # no team row is expected, the registry's seam carries the policy
    assert Term.objects.count() >= 10


def test_the_team_translation_seed_is_idempotent(seeded):
    from io import StringIO

    from django.core.management import call_command

    from orientation.models import ChoiceTranslation, OutcomeTranslation, QuestionTranslation
    from pathways.models import PathwayStepTranslation

    before = (
        PathwayStepTranslation.objects.count(),
        QuestionTranslation.objects.count(),
        ChoiceTranslation.objects.count(),
        OutcomeTranslation.objects.count(),
    )
    out = StringIO()
    call_command("seed_team_translations", stdout=out)
    assert "0 team translation row(s) created" in out.getvalue()
    assert (
        PathwayStepTranslation.objects.count(),
        QuestionTranslation.objects.count(),
        ChoiceTranslation.objects.count(),
        OutcomeTranslation.objects.count(),
    ) == before
    assert PathwayStepTranslation.objects.filter(language="ar").count() == 8 * 5
    assert QuestionTranslation.objects.filter(language="ar").count() == 5
    assert ChoiceTranslation.objects.filter(language="ar").count() == 17
    assert OutcomeTranslation.objects.filter(language="ar").count() == 9


# ---------------------------------------------------------------------------------------------
# T1 — public routes, error pages, the forms' error state  ·  T4 — readable attributes (visible_strings carries them)
# ---------------------------------------------------------------------------------------------
FORM_PATHS = (
    "contact/formulaire/",
    "entreprises/recueil-des-besoins/",
    "collaboration/institutions/",
    "collaboration/universites-formation/",
    "forum/inscription/",
    "compte/login/",
    "compte/signup/",
)


def _crawl_public(client) -> Leaks:
    leaks = Leaks()
    pages = 0
    for path, page in _public_pages(client):
        pages += 1
        leaks.page(path, page)
    # the 57 registered public routes, three of them behind a feature flag that is off here (the virtual Forum, the news,
    # the partners): every other one renders
    assert pages >= 54, pages
    for code in (400, 403, 404, 500):
        response = client.get(f"/_errors/{code}/", HTTP_ACCEPT_LANGUAGE="ar")
        if response.status_code in (200, code):
            leaks.page(f"_errors/{code}/", response.content.decode())
    for path in FORM_PATHS:
        client.get(f"/ar/{path}")
        response = client.post(f"/ar/{path}", {}, follow=True)
        if response.status_code == 200:
            leaks.page(f"POST {path}", response.content.decode())
    return leaks


def test_no_unintended_french_on_the_arabic_public_site(open_site):
    leaks = _crawl_public(open_site)
    assert leaks.found == {}, leaks.report()


def test_the_burn_down_is_closed(audit):
    """FINAL_DELIVERY_V2 §3.9 and the 6 Nov 21:25 note: the Arabic burn-down table and the catalogue's KEEP_SOURCE are
    EMPTY, and the burn-down mechanism is gone — the allowlist module no longer holds the table, so no lane can tolerate a
    French run by a row again (V5.20: the equality the deleted test held, with the table at zero, is this assertion)."""
    from . import arabic_allowlist

    assert not hasattr(arabic_allowlist, "ARABIC_BURNDOWN")
    assert audit.KEEP_SOURCE == {}
    assert not locked_renderings.DEFERRED_WHOLE


# ---------------------------------------------------------------------------------------------
# T2 — the questionnaire walk (every choice of every question once; every outcome)
# ---------------------------------------------------------------------------------------------
def test_no_unintended_french_on_the_arabic_questionnaire(open_site):
    """The wizard keeps ONE session URL for every question (the state is the session's), so the walk replays answer
    sequences on fresh sessions: every choice of every question is taken once, each branch to its end."""
    leaks = Leaks()
    explored: set[tuple[str, str]] = set()
    queue: list[list[tuple[str, str]]] = [[]]
    results = 0
    walks = 0
    while queue and walks < 80:
        answers = queue.pop(0)
        walks += 1
        response = open_site.post("/ar/orientation/", {}, follow=True)
        assert response.status_code == 200
        for key, value in answers:
            response = open_site.post(
                response.request["PATH_INFO"], {"action": "answer", "question_key": key, "answer": value}, follow=True
            )
            assert response.status_code == 200, (answers, key, value)
        path = response.request["PATH_INFO"]
        page = response.content.decode()
        leaks.page(path.removeprefix("/ar/"), page)
        if "/resultat/" in path:
            results += 1
            continue
        question = re.search(r'name="question_key" value="([^"]+)"', page)
        if not question:
            continue
        for value in dict.fromkeys(re.findall(r'name="answer" value="([^"]+)"', page)):
            if (question.group(1), value) not in explored:
                explored.add((question.group(1), value))
                queue.append([*answers, (question.group(1), value)])
    assert results >= 1, "the walk reaches a result page"
    assert leaks.found == {}, leaks.report()


# ---------------------------------------------------------------------------------------------
# T3 — the reserved area for the four audiences
# ---------------------------------------------------------------------------------------------
RESERVED_PERSON = (
    "espace-reserve/",
    "espace-reserve/mes-demandes/",
    "espace-reserve/mon-parcours/",
    "espace-reserve/mes-documents/",
    "espace-reserve/mes-echeances/",
    "espace-reserve/communications/",
    "compte/profil/",
    "compte/email/",
    "compte/password/change/",
    "compte/2fa/",
)
RESERVED_COMPANY = (
    "espace-reserve/",
    "espace-reserve/entreprise/",
    "espace-reserve/entreprise/mes-besoins/",
    "espace-reserve/entreprise/mes-besoins/nouveau/",
    "espace-reserve/entreprise/mon-entreprise/",
)
RESERVED_ORGANISATION = ("espace-reserve/", "espace-reserve/mon-organisation/")


@pytest.mark.parametrize(
    "role, routes",
    [
        ("person", RESERVED_PERSON),
        ("company", RESERVED_COMPANY),
        ("institution", RESERVED_ORGANISATION),
        ("university", RESERVED_ORGANISATION),
    ],
)
def test_no_unintended_french_in_the_arabic_reserved_area(open_site, user_factory, role, routes):
    from accounts import roles as role_names

    user = user_factory(f"{role}-ar@example.test", role=getattr(role_names, role.upper()), preferred_language="ar")
    open_site.force_login(user)
    leaks = Leaks()
    pages = 0
    for path in routes:
        response = open_site.get(f"/ar/{path}")
        if response.status_code != 200:
            continue  # a space the account does not have answers 403 / 404 or redirects
        pages += 1
        leaks.page(path, response.content.decode())
    assert pages >= 1, role
    assert leaks.found == {}, leaks.report()


def test_no_unintended_french_in_the_arabic_company_workspace_with_its_need_form(open_site, user_factory):
    """The company crawl above has no company profile, so the need form is never served to it: here a company with
    its profile reaches /ar/espace-reserve/entreprise/mes-besoins/nouveau/, whose sector and territory selects
    printed «Vénétie» and «Agroalimentaire et transformation» (v524-ar-fix B2). The company's own data are Italian."""
    from accounts import roles as role_names
    from accounts.models import AccountType, Membership, MembershipRole, Organisation, OrganisationKind
    from companies.models import CompanyProfile, Sector

    user = user_factory("company-form-ar@example.test", role=role_names.COMPANY, preferred_language="ar")
    user.account_type = AccountType.COMPANY
    user.save(update_fields=["account_type"])
    organisation = Organisation.objects.create(
        name="Alfa Meccanica", kind=OrganisationKind.COMPANY, country="IT", city="Rovigo"
    )
    Membership.objects.create(user=user, organisation=organisation, role=MembershipRole.OWNER)
    CompanyProfile.objects.create(
        organisation=organisation,
        legal_name="Alfa Meccanica S.r.l.",
        registration_number="RO-ALFA-01",
        sector=Sector.objects.active().ordered().first(),
        contact_name="Giulia Rossi",
        contact_function="HR",
        contact_email="hr-alfa@example.test",
        city="Rovigo",
        country="IT",
    )
    open_site.force_login(user)
    response = open_site.get("/ar/espace-reserve/entreprise/mes-besoins/nouveau/")
    assert response.status_code == 200
    html = response.content.decode()
    options = [text for _lang, kind, text in visible_strings(html, "ar") if kind == "option"]
    assert len(options) > len(taxonomy_sources()) // 2, "the need form serves its sector and territory options"
    leaks = Leaks()
    leaks.page("espace-reserve/entreprise/mes-besoins/nouveau/", html)
    assert leaks.found == {}, leaks.report()


def test_no_unintended_french_on_the_arabic_case_file_and_documents(open_site, user_factory):
    """A person with a case file and the seven requested pieces (the documents' seed): the dashboard's «now» card, the
    case file, «Mes documents» and one piece's page name every piece in Arabic (W3.2)."""
    from accounts import roles as role_names
    from cases import services as cases
    from cases.models import CasePurpose
    from documents.models import DocumentRequirement

    user = user_factory("person-case-ar@example.test", role=role_names.PERSON, preferred_language="ar")
    case = cases.open_case(user, purpose=CasePurpose.WORK)
    from documents import seeds as document_seeds
    from documents import services as documents

    for order, (code, title, actor, kind, source_title, source_ref, access, detail) in enumerate(
        document_seeds.REQUIREMENTS
    ):
        documents.declare_requirement(
            case,
            code=code,
            title=title,
            detail=detail,
            responsible_actor=actor,
            kind=kind,
            source_title=source_title,
            source_ref=source_ref,
            access_class=access,
            order=order,
        )
    assert DocumentRequirement.objects.filter(case=case).count() == len(document_seeds.REQUIREMENTS)
    open_site.force_login(user)
    leaks = Leaks()
    piece = DocumentRequirement.objects.filter(case=case).order_by("order").first()
    paths = [
        "espace-reserve/",
        "espace-reserve/mes-documents/",
        f"espace-reserve/mes-demandes/{case.reference}/",
    ]
    pages = 0
    for path in paths:
        response = open_site.get(f"/ar/{path}")
        if response.status_code == 200:
            pages += 1
            leaks.page(path, response.content.decode())
    response = open_site.get(f"/documents/pieces/{piece.pk}/", HTTP_ACCEPT_LANGUAGE="ar")
    if response.status_code == 200:
        pages += 1
        leaks.page(f"documents/pieces/{piece.pk}/", response.content.decode())
    assert pages >= 2
    assert leaks.found == {}, leaks.report()


# ---------------------------------------------------------------------------------------------
# the detector's own calibration — fixed strings from the audit's corpus
# ---------------------------------------------------------------------------------------------
@pytest.mark.parametrize(
    "text",
    [
        "Signalez les besoins professionnels de votre entreprise.",
        "Préparer la documentation généralement requise",
        "Quel est l’objectif principal de votre projet vers l’Italie ?",
        "Délivré par le Sportello unico. Cette pièce ne dépend pas de vous.",
        "Vérifier les documents généralement requis auprès des autorités compétentes et rassembler ceux dont vous disposez.",
        "Espace permanent de dialogue et de coopération",
    ],
)
def test_the_detector_sees_a_french_sentence(text):
    assert french_score(text) >= 4


@pytest.mark.parametrize(
    "text",
    [
        "D.lgs. 25 luglio 1998, n. 286 — Testo unico sull’immigrazione — art. 4, comma 1",
        "Carta blu UE",
        "AGAMI — Dialogo Giuridico Interculturale APS",
        "Institut des métiers Oued Lakhdar — Casablanca",
        "Nadia Benali-Essai",
        "Italy Legal Entry™",
        "IT00000000000",
        "Decreto Regione Veneto n. 11118 del 17/09/2025",
        "Associazione di Promozione Sociale (APS) / Ente del Terzo Settore",
        "Agenzia per il lavoro autorizzata",
        "Via Sandrigo n. 29",
        "Rovigo — 2 ottobre 2026 — Sala della Gran Guardia",
        "9c0d3b1884a5f1ba8e2de8ce779399aa36f6f5220a8933d4f2c246390ea88aa9",
        "de0ce0fa" * 8,
    ],
)
def test_the_detector_ignores_names_codes_acronyms_and_italian_terms(text):
    assert french_score(text) == 0


def test_a_prescribed_text_is_recognised_whatever_its_length():
    leaks = Leaks()
    assert leaks.rendered["SUIVI"] == "p3.pilot.sequence[7]"
    assert leaks.officials["Italy Legal Entry™"].startswith("C-OFFICIAL")
    assert "FORUM PERMANENT VÉNÉTIE–MAROC" in leaks.officials
    assert _locked_match("ATTENTION AUX FRAUDES · Italy Legal Entry™", leaks.rendered) == "p3.antifraud.title"


def test_every_allowlist_entry_is_justified():
    for table in (PROPER_NAMES, ACRONYMS, ITALIAN_LEGAL_TERMS, LANGUAGE_NAMES, LANGUAGE_CODES):
        for key, why in table.items():
            assert len(why) >= 4, key
    for ident, (_pattern, why) in KNOWN_FRENCH.items():
        assert len(why) >= 30, ident
    assert KNOWN_FRENCH == {}, "accepted exceptions are not part of this candidate (R7′)"
