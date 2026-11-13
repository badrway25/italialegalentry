"""
The platform's list toolkit — V5.30, stream C (docs/design-v5/QA/v530/plat/NOTES.md §1, §2, §5; the owner's V5.30 §11–§12:
«one reusable advanced-filter architecture … only filters backed by real data … persistence where architecturally safe»).
Static and in-process (no browser; the drawer's behaviour is test_listing_browser_v530_plat.py's):

* the spec (apps/portal/listing.py): only its own keys are read, each value checked against its whitelist — a choice,
  an ISO day, a sort key —, the search folded and cut at 80, the page's own parameters carried; the chips' links drop
  only their own key, «Tout effacer» keeps only the page's own, the pagination's query never the page; a key repeated
  or reserved is refused at declaration; the same spec narrows a Python list as it narrows a queryset;
* SCOPING (the P0 class of the pass): on each improved list — «Communications», the account's files, «Mes dossiers» — a
  second account's rows NEVER appear, under every combination of search, filter, period and sort, hostile values
  included (an ORM path as a sort, an unknown choice, an impossible date, markup in the search: ignored or escaped);
* the lists: the narrowing is right (state, type, objective, whose file, period, the orders), the count, the chips,
  «Tout effacer», the empty result, the state kept across pages; the bar appears from two rows (or with a narrowing in
  force) and its sheet, the panels' sheet and its module are linked only then;
* the drawer is the overlay system's drawer, from the inline end, with «Filtres» as a link-opener (no-script :target);
* B3 (the V5.29 baseline matrix, assigned to stream C): the console's mono seats render ILE Mono's base subset only;
* budgets: listing.js and listing.css at their measure (new files — V5.20, citing V5.30), main.css and shell.js untouched.
"""

from __future__ import annotations

import datetime as dt
import gzip
import itertools
import re
from pathlib import Path

import pytest
from django.http import QueryDict
from django.utils import timezone

from accounts import roles
from accounts.models import AccountType
from core import clock
from portal.listing import DateRange, Filter, ListSpec, Sort

ROOT = Path(__file__).resolve().parents[2]
TEMPLATES = ROOT / "templates"
JS_DIST = ROOT / "static" / "js" / "dist"
CSS_DIST = ROOT / "static" / "css" / "dist"

MESSAGES_URL = "/fr/espace-reserve/communications/"
FILES_URL = "/fr/espace-reserve/mes-documents/"
CASES_URL = "/fr/espace-reserve/dossiers/"

#: hostile or malformed values the query string may carry: never an error, never a widened list
HOSTILE = [
    {"tri": "-recipient__email"},
    {"tri": "owner__email"},
    {"lecture": "__all__"},
    {"type": "identity' OR 1=1 --"},
    {"statut": "draft,closed"},
    {"du": "2026-13-45", "au": "yesterday"},
    {"q": "<script>alert(1)</script>"},
    {"q": "%"},
    {"q": "x" * 500},
    {"portee": "tous"},
    {"recipient": "1", "owner": "1", "person": "1", "id__gt": "0"},
]


def _q(**params) -> QueryDict:
    query = QueryDict(mutable=True)
    for key, value in params.items():
        query[key] = value
    return query


def _gz(path: Path) -> int:
    return len(gzip.compress(path.read_bytes(), 9))


# ---- the spec, alone ---------------------------------------------------------------------------------------------
SPEC = ListSpec(
    "probe",
    search=lambda rows, q: [r for r in rows if q.lower() in r["name"].lower()],
    search_label="Rechercher",
    filters=(
        Filter(
            "kind",
            "Type",
            (("a", "Alpha"), ("b", "Beta"), ("c", "Gamma")),
            apply=lambda rows, v: [r for r in rows if r["kind"] == v],
            present=lambda rows: {r["kind"] for r in rows},
        ),
    ),
    dates=DateRange(
        "Période", lambda rows, s, e: [r for r in rows if (not s or r["day"] >= s) and (not e or r["day"] <= e)]
    ),
    sorts=(
        Sort("recent", "Récents", lambda rows: sorted(rows, key=lambda r: r["day"], reverse=True)),
        Sort("name", "Nom", lambda rows: sorted(rows, key=lambda r: r["name"])),
    ),
    preserve=("état",),
)
ROWS = [
    {"name": "Passeport", "kind": "a", "day": dt.date(2026, 9, 21)},
    {"name": "Diplôme", "kind": "b", "day": dt.date(2026, 9, 25)},
    {"name": "Contrat", "kind": "b", "day": dt.date(2026, 10, 2)},
]


def test_the_spec_reads_only_its_keys_and_only_whitelisted_values():
    state = SPEC.read(_q(kind="z", tri="-owner__email", du="2026-02-30", au="demain", other="1", page="2"))
    assert state.values == {} and state.sort == "recent" and state.start is None and state.end is None
    assert not state.narrowed and state.kept == {}
    state = SPEC.read(_q(kind="b", tri="name", du="2026-10-02", au="2026-09-22", état="missing"))
    assert state.values == {"kind": "b"} and state.sort == "name"
    assert (state.start, state.end) == (dt.date(2026, 9, 22), dt.date(2026, 10, 2)), "two days the wrong way round"
    assert state.kept == {"état": "missing"}
    assert SPEC.read(_q(q="  passe \n  port  ")).query == "passe port"
    assert len(SPEC.read(_q(q="y" * 300)).query) == 80
    assert len(SPEC.read(_q(état="w" * 300)).kept["état"]) == 80


def test_the_spec_narrows_a_list_as_it_narrows_a_queryset_and_orders_it():
    state = SPEC.read(_q(kind="b", tri="name"))
    assert [r["name"] for r in SPEC.apply(ROWS, state)] == ["Contrat", "Diplôme"]
    state = SPEC.read(_q(au="2026-09-30"))
    assert [r["name"] for r in SPEC.apply(ROWS, state)] == ["Diplôme", "Passeport"]
    assert SPEC.apply(ROWS, SPEC.read(_q(q="zzz"))) == []


def test_the_chips_drop_only_their_key_and_clear_all_keeps_only_the_pages_own():
    state = SPEC.read(_q(q="con", kind="b", du="2026-09-01", tri="name", état="missing", page="3"))
    ctx = SPEC.context(state, scoped=ROWS, count=1, total=3, path="/x/")
    removes = {chip["label"]: chip["remove"] for chip in ctx["chips"]}
    assert set(removes) == {"Votre recherche", "Type", "Depuis le"}
    assert removes["Type"] == "/x/?%C3%A9tat=missing&q=con&du=2026-09-01&tri=name"
    assert removes["Votre recherche"] == "/x/?%C3%A9tat=missing&kind=b&du=2026-09-01&tri=name"
    assert ctx["clear_url"] == "/x/?%C3%A9tat=missing"
    assert "page" not in ctx["page_query"] and "kind=b" in ctx["page_query"]
    assert ctx["filter_count"] == 2, "the period's bound and the type — the search is the bar's"
    # the drawer offers only what the rows hold (and the choice in force)
    assert [o["value"] for o in ctx["fields"][0]["options"]] == ["a", "b"]
    # the bar carries the drawer's choices, the drawer the bar's search and sort: each submits the whole state
    assert (
        ("kind", "b") in ctx["bar_hidden"]
        and ("q", "con") in ctx["drawer_hidden"]
        and ("tri", "name") in ctx["drawer_hidden"]
    )


def test_the_bar_appears_from_two_rows_or_with_a_narrowing_in_force():
    assert not SPEC.context(SPEC.read(_q()), scoped=ROWS[:1], count=1, total=1, path="/x/")["show"]
    assert SPEC.context(SPEC.read(_q()), scoped=ROWS[:2], count=2, total=2, path="/x/")["show"]
    assert SPEC.context(SPEC.read(_q(q="a")), scoped=ROWS[:1], count=0, total=1, path="/x/")["show"]


def test_a_key_repeated_or_reserved_is_refused_at_declaration():
    noop = lambda rows, v: rows  # noqa: E731
    for keys in (("q",), ("tri",), ("page",), ("x", "x"), ("état",)):
        with pytest.raises(ValueError):
            ListSpec("bad", filters=[Filter(k, k, (("1", "1"),), noop) for k in keys], preserve=("état",))


# ---- fixtures ------------------------------------------------------------------------------------------------------
@pytest.fixture
def staff(user_factory):
    return user_factory("v530.staff@example.test", role=roles.STAFF, is_staff=True)


def _person(user_factory, email, name):
    return user_factory(
        email, role=roles.PERSON, full_name=name, account_type=AccountType.PERSON, terms_accepted_at=clock.now()
    )


@pytest.fixture
def alice(user_factory):
    return _person(user_factory, "v530.alice@example.test", "Alice Essai")


@pytest.fixture
def bob(user_factory):
    return _person(user_factory, "v530.bob@example.test", "Bob Essai")


def _message(recipient, staff, subject, *, read=False, days_ago=0):
    from portal.models import Message

    message = Message.objects.create(recipient=recipient, sender=staff, subject=subject, body=f"Corps — {subject}")
    when = timezone.now() - dt.timedelta(days=days_ago)
    fields = {"created_at": when}
    if read:
        fields.update(is_read=True, read_at=when)
    Message.objects.filter(pk=message.pk).update(**fields)
    return message


@pytest.fixture
def inboxes(alice, bob, staff):
    """Alice: three communications (one read); Bob: three with the SAME words — every Bob row is a leak if seen."""
    for owner, tag in ((alice, "ALICE"), (bob, "BOBBY")):
        _message(owner, staff, f"Mise à jour de votre dossier {tag}-1", days_ago=1)
        _message(owner, staff, f"Ouverture d’un dossier {tag}-2", read=True, days_ago=20)
        _message(owner, staff, f"Rappel de pièce {tag}-3", days_ago=5)
    return alice, bob


def _html(client, user, url, **params) -> str:
    client.force_login(user)
    response = client.get(url, params)
    assert response.status_code == 200, (url, params, response.status_code)
    return response.content.decode("utf-8")


# ---- «Communications» --------------------------------------------------------------------------------------------
MESSAGE_COMBINATIONS = [
    dict(zip(("q", "lecture", "du", "tri"), combo, strict=True))
    for combo in itertools.product(
        ("", "dossier", "BOBBY", "ALICE"), ("", "non-lues", "lues"), ("", "2026-01-01"), ("", "anciennes", "non-lues")
    )
]


@pytest.mark.django_db
def test_a_second_accounts_communications_never_appear_under_any_combination(client, inboxes):
    alice, bob = inboxes
    for params in [*MESSAGE_COMBINATIONS, *HOSTILE]:
        clean = {k: v for k, v in params.items() if v}
        # a subject carries its tag and its number («BOBBY-1»); the person's own search echoes the bare word
        assert "BOBBY-" not in _html(client, alice, MESSAGES_URL, **clean), clean
        assert "ALICE-" not in _html(client, bob, MESSAGES_URL, **clean), clean


@pytest.mark.django_db
def test_communications_narrow_by_state_period_and_search_and_keep_their_order(client, inboxes):
    alice, _bob = inboxes
    html = _html(client, alice, MESSAGES_URL, lecture="non-lues")
    assert "ALICE-1" in html and "ALICE-3" in html and "ALICE-2" not in html
    assert '<p class="lst__found" role="status">2 résultats</p>' in html
    assert '<span class="lst__field">État</span> <span class="lst__value" dir="auto">Non lues</span>' in html
    html = _html(client, alice, MESSAGES_URL, lecture="lues")
    assert "ALICE-2" in html and "ALICE-1" not in html
    since = (timezone.localdate() - dt.timedelta(days=7)).isoformat()
    html = _html(client, alice, MESSAGES_URL, du=since)
    assert "ALICE-1" in html and "ALICE-3" in html and "ALICE-2" not in html
    html = _html(client, alice, MESSAGES_URL, q="rappel")
    assert "ALICE-3" in html and "ALICE-1" not in html
    # each subject once, in the page's order (an unread row names it again in its act's label)
    order = lambda page: list(dict.fromkeys(re.findall(r"ALICE-(\d)", page)))  # noqa: E731
    assert order(_html(client, alice, MESSAGES_URL))[:3] == ["1", "3", "2"], "newest first, as before"
    assert order(_html(client, alice, MESSAGES_URL, tri="anciennes"))[:3] == ["2", "3", "1"]
    assert order(_html(client, alice, MESSAGES_URL, tri="non-lues"))[:3] == ["1", "3", "2"]


@pytest.mark.django_db
def test_nothing_matching_says_so_with_one_act_and_the_band_still_counts_the_unread(client, inboxes):
    alice, _bob = inboxes
    html = _html(client, alice, MESSAGES_URL, q="introuvable")
    assert '<p class="lst-empty__title">Aucun résultat</p>' in html
    assert f'<p class="lst-empty__act"><a class="btn btn--secondary" href="{MESSAGES_URL}">Tout effacer</a></p>' in html
    assert "2 communications non lues" in html, "the band counts the inbox, whatever the narrowing shows"
    assert "db-tasks reg-rows reg-rows--mail" not in html
    assert '<input type="hidden" name="next" value="list">' not in html


@pytest.mark.django_db
def test_the_markup_escapes_the_search_and_ignores_the_hostile(client, inboxes):
    alice, _bob = inboxes
    html = _html(client, alice, MESSAGES_URL, q="<script>alert(1)</script>")
    assert "<script>alert(1)</script>" not in html and "&lt;script&gt;alert(1)&lt;/script&gt;" in html
    html = _html(client, alice, MESSAGES_URL, tri="-recipient__email", lecture="__all__")
    assert "ALICE-1" in html and "ALICE-2" in html and "ALICE-3" in html, "ignored: the list as it opens"
    assert 'class="lst__state"' not in html


@pytest.mark.django_db
def test_the_state_rides_along_the_pages(client, alice, staff):
    for n in range(12):
        _message(alice, staff, f"Note {n:02d} ALICE", days_ago=n)
    html = _html(client, alice, MESSAGES_URL, q="note", tri="anciennes")
    assert 'href="?page=2&q=note&amp;tri=anciennes"' in html, "the pagination carries the state, never a page twice"
    html = _html(client, alice, MESSAGES_URL, q="note", tri="anciennes", page="2")
    assert "Note 01 ALICE" in html and "Note 00 ALICE" in html and "Note 11 ALICE" not in html


@pytest.mark.django_db
def test_the_bar_its_sheets_and_its_module_come_with_two_rows_and_the_drawer_is_the_systems(client, alice, bob, staff):
    _message(alice, staff, "Seule ALICE")
    html = _html(client, alice, MESSAGES_URL)
    assert "data-listing" not in html and "portal/listing.css" not in html and "js/dist/listing.js" not in html
    assert "core/overlay-panels.css" not in html
    _message(alice, staff, "Deuxième ALICE", read=True)
    html = _html(client, alice, MESSAGES_URL)
    for piece in (
        'href="/static/css/dist/portal/listing.css"',
        'href="/static/css/dist/core/overlay-panels.css"',
        'src="/static/js/dist/listing.js"',
        '<form class="lst__bar" method="get" action="/fr/espace-reserve/communications/" role="search" data-listing-form>',
        '<label class="visually-hidden" for="lst-messages-q">Rechercher dans vos communications</label>',
        '<a class="lst__open" href="#lst-messages-filters" data-overlay-open>',
        '<dialog class="overlay overlay--drawer" id="lst-messages-filters" data-overlay="drawer" aria-labelledby="lst-messages-filters-title">',
        '<form class="lst-form" id="lst-messages-form" method="get" action="/fr/espace-reserve/communications/" data-listing-form>',
        '<button class="btn btn--secondary" type="submit" form="lst-messages-form">Afficher les résultats</button>',
    ):
        assert piece in html, piece
    drawer = html[html.index('id="lst-messages-filters"') :]
    assert 'data-overlay-edge="start"' not in drawer.split(">", 1)[0], "from the inline end: it mirrors in Arabic"
    assert html.index('id="lst-messages-filters"') > html.index('class="reg-page"'), "outside the list it narrows"
    # the one POST of the page keeps its CSRF token
    assert html.count('name="csrfmiddlewaretoken"') >= 1


# ---- the account's files («Mes documents») -------------------------------------------------------------------------
def _file(owner, name, kind="other", days_ago=0, size=1234):
    from documents.models import PrivateDocument, ScanStatus

    doc = PrivateDocument.objects.create(
        owner=owner,
        kind=kind,
        original_name=name,
        stored_name=f"v530-{owner.pk}-{name}",
        content_type="application/pdf",
        size=size,
        sha256=f"{abs(hash((owner.pk, name))):064d}"[:64],
        scan_status=ScanStatus.CLEAN,
    )
    PrivateDocument.objects.filter(pk=doc.pk).update(created_at=timezone.now() - dt.timedelta(days=days_ago))
    return doc


@pytest.fixture
def files(alice, bob):
    _file(alice, "alice-passeport.pdf", kind="identity", days_ago=2, size=900)
    _file(alice, "alice-diplome.pdf", kind="diploma", days_ago=10, size=5000)
    _file(alice, "alice-contrat.pdf", kind="contract", days_ago=30, size=2000)
    _file(bob, "bobby-passeport.pdf", kind="identity", days_ago=1)
    _file(bob, "bobby-contrat.pdf", kind="contract", days_ago=3)
    return alice, bob


FILE_COMBINATIONS = [
    dict(zip(("q", "type", "au", "tri"), combo, strict=True))
    for combo in itertools.product(
        ("", "passeport", "bobby", "pdf"),
        ("", "identity", "contract"),
        ("", "2027-01-01"),
        ("", "nom", "taille", "anciens"),
    )
]


@pytest.mark.django_db
def test_a_second_accounts_files_never_appear_under_any_combination(client, files):
    alice, bob = files
    for params in [*FILE_COMBINATIONS, *HOSTILE, {"état": "missing", "q": "bobby"}]:
        clean = {k: v for k, v in params.items() if v}
        assert "bobby-" not in _html(client, alice, FILES_URL, **clean), clean
        assert "alice-" not in _html(client, bob, FILES_URL, **clean), clean


@pytest.mark.django_db
def test_files_narrow_by_type_search_period_and_order_and_carry_the_registers_state(client, files):
    alice, _bob = files
    html = _html(client, alice, FILES_URL, type="identity")
    assert "alice-passeport.pdf" in html and "alice-diplome.pdf" not in html
    assert '<p class="lst__found" role="status">1 résultat</p>' in html
    names = lambda page: re.findall(r"(alice-[a-z]+)\.pdf</a>", page)  # noqa: E731
    assert names(_html(client, alice, FILES_URL)) == ["alice-passeport", "alice-diplome", "alice-contrat"]
    assert names(_html(client, alice, FILES_URL, tri="nom")) == ["alice-contrat", "alice-diplome", "alice-passeport"]
    assert names(_html(client, alice, FILES_URL, tri="taille")) == ["alice-diplome", "alice-contrat", "alice-passeport"]
    since = (timezone.localdate() - dt.timedelta(days=15)).isoformat()
    assert names(_html(client, alice, FILES_URL, du=since)) == ["alice-passeport", "alice-diplome"]
    html = _html(client, alice, FILES_URL, état="missing", type="contract")
    assert '<input type="hidden" name="état" value="missing">' in html
    assert 'href="/fr/espace-reserve/mes-documents/?%C3%A9tat=missing"' in html, "«Tout effacer» keeps the register's"
    # the drawer offers only the types the account holds
    drawer = html[html.index('id="lst-files-form"') :]
    assert 'value="identity"' in drawer and 'value="diploma"' in drawer and 'value="other"' not in drawer


# ---- «Mes dossiers» ----------------------------------------------------------------------------------------------
@pytest.fixture
def mandates(user_factory, alice, bob):
    """A professional holding live mandates on Alice's and Bob's files and a file of his own; a second professional on
    a third person's file — every one of whose rows is a leak if the first professional sees it."""
    from cases import services
    from cases.models import AssignmentRole, CasePurpose

    pro = _person(user_factory, "v530.pro@example.test", "Pro Mandataire")
    roles.assign_role(pro, roles.PROFESSIONAL)
    other = user_factory("v530.other-pro@example.test", role=roles.PROFESSIONAL, full_name="Autre Pro")
    carol = _person(user_factory, "v530.carol@example.test", "Carol Secret")
    cases = {
        "alice": services.open_case(alice, purpose=CasePurpose.WORK, pathway_key="salaried_work"),
        "bob": services.open_case(bob, purpose=CasePurpose.STUDY, pathway_key="salaried_work"),
        "pro": services.open_case(pro, purpose=CasePurpose.WORK, pathway_key="salaried_work"),
        "carol": services.open_case(carol, purpose=CasePurpose.STUDY, pathway_key="salaried_work"),
    }
    valid = clock.today() + dt.timedelta(days=30)
    for key in ("alice", "bob"):
        services.assign(
            cases[key],
            pro,
            role=AssignmentRole.PROFESSIONAL,
            authorisation_reference="SYNTH-1",
            authorisation_valid_until=valid,
        )
    services.assign(
        cases["carol"],
        other,
        role=AssignmentRole.PROFESSIONAL,
        authorisation_reference="SYNTH-2",
        authorisation_valid_until=valid,
    )
    return pro, other, cases


CASE_COMBINATIONS = [
    dict(zip(("q", "statut", "objectif", "portee", "tri"), combo, strict=True))
    for combo in itertools.product(
        ("", "Carol", "Essai"),
        ("", "draft"),
        ("", "study", "work"),
        ("", "miens", "confies"),
        ("", "reference", "ouverture"),
    )
]


@pytest.mark.django_db
def test_a_file_outside_the_mandates_never_appears_under_any_combination(client, mandates):
    pro, other, cases = mandates
    secret = cases["carol"].reference
    for params in [*CASE_COMBINATIONS, *HOSTILE, {"q": secret}]:
        clean = {k: v for k, v in params.items() if v}
        # a row is its link to the file; the professional's own typed search may echo a reference, never a row
        page = _html(client, pro, CASES_URL, **clean)
        assert f"/dossiers/{secret}/" not in page and "Carol Secret" not in page, clean
        page = _html(client, other, CASES_URL, **clean)
        for key in ("alice", "bob", "pro"):
            assert f"/dossiers/{cases[key].reference}/" not in page, (clean, key)


@pytest.mark.django_db
def test_files_narrow_by_whose_objective_and_search_and_a_single_file_draws_no_bar(client, mandates, alice):
    pro, _other, cases = mandates
    refs = lambda page: {key for key, case in cases.items() if f">{case.reference}</span>" in page}  # noqa: E731
    assert refs(_html(client, pro, CASES_URL)) == {"alice", "bob", "pro"}
    assert refs(_html(client, pro, CASES_URL, portee="miens")) == {"pro"}
    assert refs(_html(client, pro, CASES_URL, portee="confies")) == {"alice", "bob"}
    assert refs(_html(client, pro, CASES_URL, objectif="study")) == {"bob"}
    assert refs(_html(client, pro, CASES_URL, q="alice")) == {"alice"}
    assert refs(_html(client, pro, CASES_URL, q=cases["bob"].reference.lower())) == {"bob"}
    html = _html(client, pro, CASES_URL, objectif="family")
    assert '<p class="lst-empty__title">Aucun résultat</p>' in html
    assert "Cette liste contient des dossiers qui ne sont pas les vôtres" in html, "the clause speaks for the list"
    html = _html(client, alice, CASES_URL)
    assert "data-listing" not in html and "lst-cases-filters" not in html, "one file: nothing to narrow"


# ---- B3 · the mono seats keep to ILE Mono's base subset -----------------------------------------------------------
BASE_SUBSET = re.compile(r"^[ #+,\-./0-9:A-Z_ ]*$")
MONO_SEAT = re.compile(
    r'<(span|dd|code)[^>]*class="(?:[^"]* )?(?:db-ref|reg-ref|ctx__ref|ws-case__ref|t-ref)(?: [^"]*)?"[^>]*>([^<]*)<'
)


def test_the_separator_of_a_meta_row_reads_the_sans():
    css = (ROOT / "apps/portal/static/portal/v5/_registers.css").read_text(encoding="utf-8")
    body = re.search(r"\.reg-row__meta > \*::before,\s*\.reg-step__meta > \*::before \{([^}]*)\}", css).group(1)
    assert 'content: "·"' in body and "font-family: var(--f-sans)" in body


def test_the_templates_keep_letters_and_citations_off_the_mono():
    read = lambda name: (TEMPLATES / name).read_text(encoding="utf-8")  # noqa: E731
    for name in ("portal/dashboard.html", "cases/detail.html", "cases/assessment.html"):
        assert '<span class="db-ref">v{{' not in read(name), name
    assert '<span class="reg-ref">{{ line.source_ref }}</span>' not in read("cases/detail.html")
    assert '<span class="db-ref">{{ now.source.ref }}</span>' not in read("portal/partials/now_panel.html")
    assert "{{ item.reference|upper }}" in read("portal/requests.html")
    assert "{{ item.reference|upper }}" in read("portal/request_detail.html")
    assert "{{ version.sha256_short|upper }}" in read("documents/requirement_detail.html")
    for name in ("academy/mine.html", "academy/plan_detail.html"):
        assert '<span class="reg-ref">{{ plan.origin_reference }}</span>' not in read(name), name


@pytest.mark.django_db
def test_the_case_file_and_the_dashboard_render_only_base_subset_text_in_their_mono_seats(client, alice):
    from cases import services
    from cases.models import CasePurpose, ResponsibleActor

    case = services.open_case(alice, purpose=CasePurpose.WORK, pathway_key="salaried_work")
    services.add_checklist_item(
        case,
        requirement="Passeport",
        responsible_actor=ResponsibleActor.PERSON,
        source_title="Code",
        source_ref="art. 22",
    )
    for url in ("/fr/espace-reserve/", f"/fr/espace-reserve/dossiers/{case.reference}/", "/ar/espace-reserve/"):
        html = _html(client, alice, url)
        seats = [text for _tag, text in MONO_SEAT.findall(html) if text.strip()]
        assert seats, url
        for text in seats:
            assert BASE_SUBSET.match(text.replace("&#x27;", "'")), (url, text)
        assert "art. 22" not in "".join(seats)


# ---- budgets -----------------------------------------------------------------------------------------------------
def test_the_toolkits_files_hold_their_measure_and_the_shared_ceilings_are_untouched():
    # V5.20, citing V5.30 (the orchestrator's rule: «a NEW platform JS module gets its own ceiling recorded at its
    # measure … a new file, not a raise»): listing.js and the page sheet portal/listing.css are new files, recorded at
    # their measure on the stream's head; main.css and shell.js stay under their hard ceilings, unchanged
    assert _gz(JS_DIST / "listing.js") <= 343, _gz(JS_DIST / "listing.js")
    assert _gz(CSS_DIST / "portal" / "listing.css") <= 1_258, _gz(CSS_DIST / "portal" / "listing.css")
    assert _gz(CSS_DIST / "main.css") <= 32_105
    assert _gz(JS_DIST / "shell.js") <= 4_700
    source = (ROOT / "static/js/src/listing.js").read_text(encoding="utf-8")
    for unsafe in ("innerHTML", "outerHTML", "insertAdjacentHTML", "eval(", "new Function", ".style."):
        assert unsafe not in source, unsafe


# ---- the destructive confirm: a need's withdrawal -----------------------------------------------------------------
def _company(user_factory, slug):
    from accounts.models import (
        AccountVerification,
        Membership,
        MembershipRole,
        Organisation,
        OrganisationKind,
        VerificationStatus,
    )
    from companies.models import CompanyProfile, Sector

    user = user_factory(f"v530.{slug}@example.test", role=roles.COMPANY, account_type=AccountType.COMPANY)
    organisation = Organisation.objects.create(
        name=f"Organisation {slug}", kind=OrganisationKind.COMPANY, country="IT", city="Rovigo"
    )
    Membership.objects.create(user=user, organisation=organisation, role=MembershipRole.OWNER)
    AccountVerification.objects.create(
        user=user, declared_type=AccountType.COMPANY, status=VerificationStatus.APPROVED, decided_at=timezone.now()
    )
    sector, _created = Sector.objects.get_or_create(
        code="batiment", defaults={"label_fr": "Bâtiment et travaux publics", "order": 10}
    )
    profile = CompanyProfile.objects.create(
        organisation=organisation,
        legal_name=f"Société {slug} S.r.l.",
        registration_number=f"RM-{slug.upper()}-01",
        sector=sector,
        contact_name="Référent",
        contact_function="RH",
        contact_email=f"referent-{slug}@example.test",
        city="Rovigo",
        country="IT",
    )
    return profile, user


def _need(profile, title):
    from companies.models import CompanyNeed

    return CompanyNeed.objects.create(company=profile, title=title, headcount=1, status="draft")


@pytest.fixture
def companies(user_factory):
    from companies.models import NeedEvent

    alpha, alpha_user = _company(user_factory, "alpha")
    gamma, gamma_user = _company(user_factory, "gamma")
    for profile, tag in ((alpha, "ALPHA"), (gamma, "GAMMA")):
        for n in range(2):
            need = _need(profile, f"Besoin {tag}-{n}")
            NeedEvent.objects.create(need=need, from_status="", to_status="draft", responsible_label="Votre entreprise")
    return (alpha, alpha_user), (gamma, gamma_user)


@pytest.mark.django_db
def test_the_withdrawal_asks_first_in_the_systems_alert_dialog_and_still_posts_without_script(client, companies):
    (alpha, user), _gamma = companies
    need = alpha.needs.first()
    url = f"/fr/espace-reserve/entreprise/mes-besoins/{need.reference}/"
    html = _html(client, user, url)
    opener = '<a class="btn btn--danger" href="#need-withdraw-dialog" data-overlay-open>Retirer le besoin</a>'
    assert opener in html, "the opener, styled as what it is; a link to the dialog without script (:target)"
    dialog = html[html.index('id="need-withdraw-dialog"') - 200 :]
    assert 'class="overlay overlay--dialog overlay--alert"' in dialog and 'data-overlay="alert"' in dialog
    assert 'role="alertdialog"' in dialog and 'aria-describedby="need-withdraw-text"' in dialog
    body = dialog[dialog.index('<form class="form reg-dialog" id="need-withdraw-form" method="post"') :]
    assert 'name="csrfmiddlewaretoken"' in body.split("</form>", 1)[0], "CSRF on the POST"
    assert 'name="reason"' in body.split("</form>", 1)[0], "the reason in view, inside the confirmation"
    assert "Un besoin retiré n’est pas rouvert : un nouveau besoin peut être créé." in body
    foot = body.split("</form>", 1)[1]
    assert foot.index("data-overlay-safe") < foot.index(
        'class="btn btn--danger" type="submit" form="need-withdraw-form"'
    ), "«Annuler» the safe answer first, the garnet outline last"
    assert "css/dist/core/overlay-panels.css" in html
    # the act itself is unchanged: the same POST withdraws, through the policy and the service
    client.force_login(user)
    response = client.post(
        f"/fr/espace-reserve/entreprise/mes-besoins/{need.reference}/retirer/", {"reason": "Poste pourvu"}
    )
    assert response.status_code == 302
    need.refresh_from_db()
    assert need.status == "withdrawn"
    assert "need-withdraw-dialog" not in _html(client, user, url), "a withdrawn need offers no withdrawal"


@pytest.mark.django_db
def test_the_company_dashboards_recent_activity_is_its_own_needs_history_only(client, companies):
    (_alpha, alpha_user), (_gamma, gamma_user) = companies
    html = _html(client, alpha_user, "/fr/espace-reserve/entreprise/")
    activity = html[html.index('id="db-activity-title"') :].split("</section>", 1)[0]
    assert "Activité récente" in activity and activity.count('class="db-list__row"') == 2
    assert "Besoin ALPHA-" in activity and "GAMMA" not in html.replace("Société gamma", "")
    assert "GAMMA-" not in html and "ALPHA-" not in _html(client, gamma_user, "/fr/espace-reserve/entreprise/")


@pytest.mark.django_db
def test_the_persons_dashboard_reads_its_recent_activity_from_the_case_files_presenter(client, alice, bob):
    from cases import services
    from cases.models import CasePurpose

    services.open_case(alice, purpose=CasePurpose.WORK, pathway_key="salaried_work")
    services.open_case(bob, purpose=CasePurpose.STUDY, pathway_key="salaried_work")
    html = _html(client, alice, "/fr/espace-reserve/")
    section = html[html.index('id="db-activity-title"') :].split("</section>", 1)[0]
    assert '<ol class="tl" role="list" aria-label="Activité récente">' in section
    assert "#history-title" in section and "Tout l’historique" in section
    assert 'class="db-side db-side--lattice db-side--tall"' in html, "the side spans the activity's row too"
    assert "Bob Essai" not in html, "the actor is a type, never a name"
    assert "portal/journey.css" in html, "the timeline's drawing comes with it"


@pytest.mark.django_db
def test_the_calm_panel_draws_the_spaces_glyph_never_the_porticoes(client, alice):
    html = _html(client, alice, MESSAGES_URL)
    calm = html[html.index('<div class="org-calm reg-calm"') :].split("</div>", 1)[0]
    assert '<span class="org-calm__art" aria-hidden="true">' in calm and "#icon-mail" in calm
    for template in ("portal/partials/calm_art.html",):
        text = (TEMPLATES / template).read_text(encoding="utf-8")
        assert "org-calm__arch" not in text and "org-calm__route" not in text and "<svg" not in text
    css = (ROOT / "apps/portal/static/portal/v5/_platform.css").read_text(encoding="utf-8")
    assert ".org-calm__arch" not in css and ".org-calm__route" not in css, "the drawing's rules left with it"
