"""
The platform's typography contract — V5.24, lane PLAT (FINAL_DELIVERY_V2 §3.7, R8 «the platform is a preserved family:
typography contract and AR's one-line call only»; TYPOGRAPHY_V2 F-3, F-4, F-7, F-8, §4.2, §4.3, §4.5; V5.20's strict rule:
every assertion is the audit's letter or stronger, cited). Static, offline, on the sources and the built dist:

* F-4 — the console's eyebrows are the label role BY NAME: the atrium eyebrow, the ContextHeader's eyebrow, the lattice's
  labels and the identity sheet's facts carry `t-label` (v5/base.css) and the sheets restate only the console's size
  (`--u-eyebrow`, 12/16; 13/20 on phones; 14/20 in Arabic through the tokens) — no capitals, weight or tracking of their own;
* F-8 — the workspace lead's measure is `--measure-small` (29 rem; 83–87 cpl at 15 px before); the atrium's workspace
  title reads `--u-title-lg` (the clamp promoted to the token), its literal leading opens by `--ar-lh-plus` in Arabic and
  its tracking is a token (0 in Arabic);
* F-3 / §4.2 — the figures and step markers are the sans numeral role (`--u-numeral` 28/32, `--w-title`, tabular; the
  smaller markers at `--w-title` tabular at the list's size — 600 in TYPOGRAPHY_V2 §4.2, 500 under V5.29's weight map); the identity sheet's date is in the sans; the references stay in the mono
  (`.ctx__ref`, `.db-ref`, `.reg-ref`, `.ws-case__ref`, `.academy-attendance__ref`) — R8 «refs stay in the mono»;
* F-7 / §4.5 — every Arabic type rule of the platform's sheets is in the SUBJECT form (`.x:lang(ar)`), none descends from
  the page's language, and the NowPanel's Arabic title takes the entry's 20/32;
* T's burn-down (tests/frontend/test_typography_v2.py) emptied for the platform's sheets but the four recorded residues;
* AR's W3.2 call: a checklist line's words go through `documents.services.displayed_text` when it exists — a translated
  line is in the page's language (no lang / dir of its own), an untranslated one keeps the record's;
* budgets (§3.7): every owned dist sheet at or under its measure on design-v5 4e882904 (gzip -9), never raised.
"""

from __future__ import annotations

import gzip
import re
from pathlib import Path

import pytest

from tests.frontend.test_typography_v2 import _TWICE, TYPOGRAPHY_EXCEPTIONS, _rules, _strip, measure

ROOT = Path(__file__).resolve().parents[2]
PORTAL = ROOT / "apps" / "portal" / "static" / "portal"
V5 = PORTAL / "v5"
TEMPLATES = ROOT / "templates"
DIST = ROOT / "static" / "css" / "dist"

pytestmark = pytest.mark.compliance

#: the lane's sheets (FINAL_DELIVERY_V2 §3.7 «Files owned»)
PLAT_SHEETS = (
    *sorted(V5.glob("_*.css")),
    PORTAL / "portal.css",
    ROOT / "apps/academy/static/academy/academy.css",
    ROOT / "apps/documents/static/documents/documents.css",
    ROOT / "apps/companies/static/companies/companies.css",
    ROOT / "apps/helpdesk/static/helpdesk/helpdesk.css",
    ROOT / "apps/selection/static/selection/selection.css",
)
#: the residues of T's burn-down the lane records instead of regressing (PLAT NOTES §4): the lattice label's capitals
#: restated for lane AR's Academy template, the rail's lock-up size (R1), the Academy's attendance reference (lane AR's
#: template). The fourth, the documents workspace's reference, is gone: CLOSING corrected the seat list's name (the
#: audit's `.doc-workspace__ref`, a class no template carries, is `.ws-case__ref`; FINAL_DELIVERY_V2 §3.9 c, PLAT NOTES §4)
RESIDUES = {
    "apps/portal/static/portal/v5/_platform.css": {"uppercase": 1},
    "apps/portal/static/portal/v5/_shell.css": {"literal": 1},
    "apps/academy/static/academy/academy.css": {"mono": 1},
}
#: the owned dist sheets' measures on design-v5 4e882904 (gzip -9), the ceilings — «each ≤ its measure today + 0»
CEILINGS = {
    "portal/console.css": 8032,
    "portal/platform.css": 5014,
    "portal/registers.css": 2984,
    "portal/journey.css": 2728,
    "portal/situation.css": 2243,
    "portal/case.css": 955,
    "portal/organisation.css": 933,
    "portal/portal.css": 1045,
    "academy/academy.css": 192,
    "documents/documents.css": 5564,
    "companies/companies.css": 189,
    "helpdesk/helpdesk.css": 262,
    "selection/selection.css": 463,
}


def _rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def _rule(path: Path, selector: str) -> str:
    """The body of the FIRST rule whose selector list is exactly `selector` (whitespace normalised) — the sheet's own
    declaration, before the media blocks that re-point it on phones."""
    bodies = [body for sel, body in _rules(path.read_text(encoding="utf-8")) if " ".join(sel.split()) == selector]
    assert bodies, selector
    return bodies[0]


def _declaration(body: str, prop: str) -> str | None:
    m = re.search(rf"(?<![\w-]){re.escape(prop)}\s*:\s*([^;]+);", body)
    return " ".join(m.group(1).split()) if m else None


# ---- F-4 · the label role by name -------------------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("template", "markup", "count"),
    [
        ("portal/partials/atrium_eyebrow.html", '<p class="atrium__eyebrow t-label">', 1),
        ("portal/dashboard_organisation.html", '<p class="ctx__eyebrow atrium__eyebrow t-label">', 1),
        ("portal/organisation.html", '<p class="ctx__eyebrow atrium__eyebrow t-label">', 1),
        ("portal/dashboard.html", '<p class="lattice__label t-label">', 2),
        ("portal/dashboard.html", '<div class="org-id__fact"><dt class="t-label">', 5),
        ("portal/dashboard_organisation.html", '<div class="org-id__fact"><dt class="t-label">', 5),
        ("portal/organisation.html", '<div class="org-id__fact"><dt class="t-label">', 6),
    ],
)
def test_the_consoles_eyebrows_and_fact_labels_carry_the_label_role_by_name(template, markup, count):
    """TYPOGRAPHY_V2 F-4 (V5.24 §12): one label role, Host Grotesk at `--w-label` +0.08 em uppercase (no capitals, no tracking in
    Arabic) — by name, so the role's Arabic rule and tokens reach the console's labels; no eyebrow left without it."""
    source = (TEMPLATES / template).read_text(encoding="utf-8")
    assert source.count(markup) == count, (template, markup)
    assert not re.search(r'class="(?:ctx__eyebrow )?atrium__eyebrow"', source), template
    assert '<div class="org-id__fact"><dt>' not in source, template


@pytest.mark.parametrize(
    ("sheet", "selector"),
    [
        # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026: the
        # head's eyebrow left this list for its own, stronger test below (the capitals and the tracking stated off)
        ("_platform.css", ".org-id--lattice .org-id__fact > dt"),
        ("_frame.css", ".ctx__eyebrow"),
    ],
)
def test_the_sheets_restate_only_the_consoles_label_size(sheet, selector):
    """The role owns the capitals, the weight and the tracking (v5/base.css `.t-label`); the console sheet keeps its own
    density — 12/16 through `--u-eyebrow` (13/20 on phones, 14/20 in Arabic in tokens.css) — and nothing else of the type."""
    body = _rule(V5 / sheet, selector)
    assert _declaration(body, "font-size") == "var(--u-eyebrow)"
    assert _declaration(body, "line-height") == "var(--u-eyebrow-lh)"
    for prop in ("text-transform", "letter-spacing", "font-weight"):
        assert _declaration(body, prop) is None, (selector, prop)


def test_the_heads_space_name_keeps_the_label_size_and_drops_the_capitals():
    """RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026 («no
    arbitrary uppercase»; the platform must not read as the public site): the head's space name («Espace Personnes»)
    was the parametrized case above (the sheet restates the size only, the role owns the rest). It keeps the label role
    by name (the templates' `t-label`, F-4 above: its weight, its Arabic rule) and the console's label density, 12/16
    through `--u-eyebrow` — and, stronger, the sheet now states the capitals and the tracking OFF in every language
    (the browser test reads `text-transform: none` in fr, it and ar), and still restates no weight."""
    body = _rule(V5 / "_platform.css", ".atrium__eyebrow, [data-atrium] .ctx__eyebrow")
    assert _declaration(body, "font-size") == "var(--u-eyebrow)"
    assert _declaration(body, "line-height") == "var(--u-eyebrow-lh)"
    assert _declaration(body, "text-transform") == "none"
    assert _declaration(body, "letter-spacing") == "0"
    assert _declaration(body, "font-weight") is None


def test_the_lattice_label_restates_the_role_until_lane_ars_template_carries_it():
    """The recorded residue (R14; PLAT NOTES §4): templates/academy/catalogue.html (lane AR's file) draws `.lattice__label`
    without the role's class, so the sheet keeps the capitals, weight and tracking through the role's tokens — equal to the
    role, deleted by CLOSING when AR's template carries `t-label`."""
    body = _rule(V5 / "_platform.css", ".lattice__label")
    assert _declaration(body, "text-transform") == "uppercase"
    assert _declaration(body, "letter-spacing") == "var(--track-eyebrow)"
    assert _declaration(body, "font-size") == "var(--u-eyebrow)"


# ---- F-8 · the measure; the workspace title's step --------------------------------------------------------------------


def test_the_workspace_lead_reads_29_rem_and_the_atrium_title_the_promoted_step():
    """F-8: `.ws-head__lead` 614 px at 15 px was 83–87 cpl on the needs, the profile and the need form — `--measure-small`
    (29 rem). §4.2: the workspace head's clamp is `--u-title-lg`; its literal leading opens by `--ar-lh-plus` in Arabic
    and its tracking is a token, so an Arabic head carries no tracking (§4.5) and a lang="fr" head keeps the Latin values."""
    lead = _rule(V5 / "_frame.css", ".ws-head__lead")
    assert _declaration(lead, "max-inline-size") == "var(--measure-small)"
    title = _rule(V5 / "_platform.css", "[data-atrium] .ctx__title, [data-atrium] .ws-head__title")
    assert _declaration(title, "font-size") == "var(--u-title-lg)"
    assert _declaration(title, "line-height") == "calc(1.12 + var(--ar-lh-plus))"
    assert _declaration(title, "letter-spacing") == "var(--track-band)"
    assert measure(V5 / "_platform.css")["clamp"] == 0, "no font-size clamp outside tokens.css (F-2)"


# ---- F-3 / §4.2 · the numeral role; the references in the mono -------------------------------------------------------


@pytest.mark.parametrize(
    ("sheet", "selector", "size", "leading"),
    [
        ("_platform.css", ".lattice__figure", "var(--u-numeral)", "var(--u-numeral-lh)"),
        ("_platform.css", ".db-next__day", "var(--u-numeral)", "var(--u-numeral-lh)"),
        ("_platform.css", ".ring-dial__count", "var(--u-small)", "1"),
        # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026:
        # `.org-refs__index` is retired, not restyled — test_the_organisations_tiles_carry_no_numeric_marker below
        ("_registers.css", ".reg-step::before", "var(--u-small)", "var(--u-ui-lh)"),
    ],
)
def test_the_consoles_figures_and_markers_are_the_sans_numeral_role(sheet, selector, size, leading):
    """F-3 (V5.24 §12): step markers and figures in Host Grotesk at `--w-title` tabular, never the mono; the console's figure at the
    scale's numeral step 28/32 (§4.2 «numeral 28/32 600»; the weight through the token, 500 under V5.29), the smaller markers tabular at the list's size."""
    body = _rule(V5 / sheet, selector)
    assert "var(--f-mono)" not in body and "font-family" not in body, selector
    assert _declaration(body, "font-size") == size
    assert _declaration(body, "line-height") == leading
    assert _declaration(body, "font-weight") == "var(--w-title)"
    assert _declaration(body, "font-variant-numeric") == "var(--numeric-data)"
    assert _declaration(body, "letter-spacing") in (None, "0"), selector


def test_the_bands_figure_and_the_identity_sheets_date_follow_the_weight_map_and_the_sans():
    """§4.3: the title weight intitles (`--w-title`) — the register band's count takes the numeral's weight (its size stays the band's 20/28); the
    identity sheet's date is not a reference: the sans with tabular figures, never split (`white-space: nowrap`)."""
    band = _rule(V5 / "_registers.css", ".reg-band__n")
    assert _declaration(band, "font-weight") == "var(--w-title)"
    assert _declaration(band, "font-size") == "var(--u-section)"
    time = _rule(V5 / "_platform.css", ".org-id__fact time")
    assert "var(--f-mono)" not in time
    assert _declaration(time, "font-variant-numeric") == "var(--numeric-data)"
    assert _declaration(time, "white-space") == "nowrap"


@pytest.mark.parametrize(
    ("sheet", "selector"),
    [
        (V5 / "_frame.css", ".ctx__ref"),
        (V5 / "_dashboard.css", ".db-ref"),
        (V5 / "_registers.css", ".reg-ref"),
        (V5 / "_workspace.css", ".ws-case__ref"),
        (ROOT / "apps/academy/static/academy/academy.css", ".academy-attendance__ref"),
    ],
)
def test_the_references_stay_in_the_mono(sheet, selector):
    """R8 «refs stay in the mono» (TYPOGRAPHY_V2 F-3: the ledger's hand for references, hashes, rule versions)."""
    assert _declaration(_rule(sheet, selector), "font-family") == "var(--f-mono)"


def test_no_other_mono_seat_in_the_platforms_sheets():
    """Outside the five reference classes no rule of the platform's sheets draws ILE Mono (F-3): the audit's five seats of
    _platform.css and the registers' step counter are the sans now."""
    refs = {".ctx__ref", ".db-ref", ".reg-ref", ".ws-case__ref", ".academy-attendance__ref"}
    for sheet in PLAT_SHEETS:
        for selector, body in _rules(sheet.read_text(encoding="utf-8")):
            if "var(--f-mono)" in body:
                assert " ".join(selector.split()) in refs, (_rel(sheet), selector)


# ---- F-7 / §4.5 · the Arabic rules ------------------------------------------------------------------------------------


def test_every_arabic_type_rule_of_the_platform_is_in_the_subject_form():
    """F-7: a `lang="fr"` element on an Arabic page keeps its Latin type — no `:lang(ar) <descendant>` rule writes a type
    property in any of the platform's sheets; the ones that stay are `.x:lang(ar)`."""
    for sheet in PLAT_SHEETS:
        assert measure(sheet)["ar_descendant"] == 0, _rel(sheet)
    shell = _strip((V5 / "_shell.css").read_text(encoding="utf-8"))
    assert ".rail__space:lang(ar)" in shell and ".console-bottom__item:lang(ar)" in shell
    assert ":lang(ar) .console .page-header__title" not in shell, "dead: the tokens zero --track-band in Arabic"
    rail = _strip((V5 / "_journey-rail.css").read_text(encoding="utf-8"))
    assert ":is(.journey__shore, .journey__gate):lang(ar)" in rail


def test_the_now_panels_arabic_title_takes_the_entrys_leading():
    """§4.5: entry titles 20/32 in Arabic (T's probe found the company dashboard's `h2.db-now__title` at 20/25 on two lines,
    under Readex Pro's 1.25 em content area — «tight»); the rule in the subject form, the dead tracking zero gone."""
    body = _rule(V5 / "_dashboard.css", ".db-now__title:lang(ar)")
    assert _declaration(body, "line-height") == "2rem"
    assert _declaration(body, "letter-spacing") is None
    assert ":lang(ar) .db-now__title" not in _strip((V5 / "_dashboard.css").read_text(encoding="utf-8"))


@pytest.mark.parametrize(
    ("sheet", "selector"),
    [
        ("_table.css", ".doc-files__title"),
        ("_workspace.css", ".ws-case__title"),
        ("_workspace.css", ".reg__next-title"),
        ("_depot.css", ".doc-piece__h2"),
        ("_registers.css", ".reg-result__title"),
    ],
)
def test_the_titles_whose_arabic_zero_left_read_the_tracking_token(sheet, selector):
    """The four `:lang(ar) .title { letter-spacing: 0 }` rules were dead: each title tracks `--track-entry`, which tokens.css
    zeroes under `:lang(ar)` and restores inside a Latin run (F-7) — the title must keep reading the token."""
    assert _declaration(_rule(V5 / sheet, selector), "letter-spacing") == "var(--track-entry)"
    assert f":lang(ar) {selector}" not in _strip((V5 / sheet).read_text(encoding="utf-8"))


# ---- T's burn-down for the platform ------------------------------------------------------------------------------------


def test_ts_burn_down_is_emptied_for_the_platforms_sheets_but_the_recorded_residues():
    """FINAL_DELIVERY_V2 §3.7 «T's burn-down emptied for the portal sheets»: every count 0, except the residues each
    recorded with its reason (RESIDUES; PLAT NOTES §4) — and the table's rows equal them (no residue unrecorded)."""
    for sheet in PLAT_SHEETS:
        measured = {k: v for k, v in measure(sheet).items() if v}
        assert measured == RESIDUES.get(_rel(sheet), {}), _rel(sheet)
        # T's burn-down table is closed (FINAL_DELIVERY_V2 §3.9 c; V5.20: the same equality, read on its successor):
        # the closed exception register counts, per discipline, exactly the recorded residues
        registered: dict[str, int] = {}
        for kind, selector in TYPOGRAPHY_EXCEPTIONS.get(_rel(sheet), {}):
            registered[kind] = registered.get(kind, 0) + _TWICE.get((_rel(sheet), (kind, selector)), 1)
        assert registered == RESIDUES.get(_rel(sheet), {}), _rel(sheet)
    assert measure(PORTAL / "portal.css") == {"clamp": 0, "literal": 0, "mono": 0, "ar_descendant": 0, "uppercase": 0}
    portal = _strip((PORTAL / "portal.css").read_text(encoding="utf-8"))
    assert "var(--font-size-small)" not in portal and "var(--u-ui)" in portal


# ---- budgets -------------------------------------------------------------------------------------------------------------


@pytest.mark.parametrize(("sheet", "ceiling"), sorted(CEILINGS.items()))
def test_every_owned_dist_sheet_holds_its_measure(sheet, ceiling):
    """§3.7 Budgets: «each ≤ its measure today + 0 (type conversions only shrink or hold; measured)» — gzip -9 of the built
    dist against the measure on design-v5 4e882904; never raised (R4)."""
    size = len(gzip.compress((DIST / sheet).read_bytes(), 9))
    assert size <= ceiling, (sheet, size, ceiling)


# ---- lane AR's W3.2 call -------------------------------------------------------------------------------------------------


@pytest.fixture
def case_with_a_line(db, user_factory):
    from accounts import roles
    from accounts.models import AccountType
    from cases.models import CasePurpose, ResponsibleActor
    from cases.services import add_checklist_item, open_case
    from core import clock

    user = user_factory(
        "plat.lines@example.test",
        role=roles.PERSON,
        full_name="Personne PLAT",
        account_type=AccountType.PERSON,
        terms_accepted_at=clock.now(),
    )
    case = open_case(user, purpose=CasePurpose.WORK, pathway_key="salaried_work")
    item = add_checklist_item(
        case,
        requirement="Passeport en cours de validité",
        responsible_actor=ResponsibleActor.PERSON,
        detail="Pages d’identité uniquement. La validité doit couvrir la durée du séjour envisagé.",
        source_title="Testo unico",
        source_ref="art. 4",
    )
    return user, case, item


@pytest.mark.django_db
def test_a_checklist_line_goes_through_the_documents_catalogue_helper(case_with_a_line):
    """Lane AR's W3.2 (arabic/02_class_b_wraps.md; FINAL_DELIVERY_V2 §3.7, §3.8): `documents.services.displayed_text` —
    the catalogue's pgettext("document requirement", …) — gives a catalogued line its words in the reader's language, and
    the row is then the page's (no lang / dir of its own); on a French page the record's French, no span."""
    from django.utils import translation

    from portal import services

    user, case, item = case_with_a_line
    with translation.override("ar"):
        [row] = services.case_lines(user, case, [item])
    assert row["title"] == "جواز سفر ساري الصلاحية"
    assert row["detail"] == "صفحات الهوية فقط. ويجب أن تغطي الصلاحية مدة الإقامة المزمعة."
    assert row["words"] == {"lang": "", "dir": ""}, "a translated line is the page's: no lang / dir span"

    with translation.override("fr"):
        [row] = services.case_lines(user, case, [item])
    assert row["title"] == "Passeport en cours de validité"
    assert row["words"] == {"lang": "", "dir": ""}, "French page, French record: no span"


@pytest.mark.django_db
def test_an_uncatalogued_line_keeps_the_records_words_isolated(case_with_a_line):
    """A line the catalogue does not carry keeps the record's words in the record's language, isolated (gate-0 A6); a line
    whose title is catalogued but whose detail is not keeps BOTH in the record's words — the templates give the title and
    the detail one lang / dir, so a mixed row would put French under the page's Arabic direction; an empty detail stays
    empty."""
    from django.utils import translation

    from portal import services

    user, case, item = case_with_a_line
    item.requirement, item.detail = "Pièce rédigée par le dossier", ""
    with translation.override("ar"):
        [row] = services.case_lines(user, case, [item])
    assert row["title"] == "Pièce rédigée par le dossier" and row["detail"] == ""
    assert row["words"] == {"lang": "fr", "dir": "ltr"}, "an untranslated line keeps the record's language, isolated"

    item.requirement, item.detail = "Passeport en cours de validité", "Détail propre à ce dossier."
    with translation.override("ar"):
        [row] = services.case_lines(user, case, [item])
    assert (row["title"], row["detail"]) == ("Passeport en cours de validité", "Détail propre à ce dossier.")
    assert row["words"] == {"lang": "fr", "dir": "ltr"}, "a half-catalogued line stays whole in the record's words"


# ---- V5.29: the platform inherits the weight map and the ink roles -----------------------------------------------------

V529_SHEETS = sorted((ROOT / "apps/portal/static/portal").rglob("*.css")) + [
    ROOT / "apps/documents/static/documents/documents.css",
    ROOT / "apps/companies/static/companies/companies.css",
    ROOT / "apps/academy/static/academy/academy.css",
]


@pytest.mark.parametrize("sheet", V529_SHEETS, ids=lambda p: p.name)
def test_the_platform_writes_no_literal_title_weight_and_no_v1_ink(sheet):
    """V5.29 §5–§6 (owner, 6 Nov 2026: «too much black, heavy bold … not bold hierarchy»; stream SYS's contract item for
    PLAT, QA/v529/sys/NOTES.md §3): no platform sheet writes a literal weight above the body's 400 — titles, labels,
    controls and figures read `--w-title` / `--w-label` / `--w-control`, so the map's one step down reaches the console —
    and no sheet paints with V1's `--ink*` aliases: the text roles by name (`--text-1/-2/-3`, `--text-primary` …)."""
    css = re.sub(r"/\*.*?\*/", "", sheet.read_text(encoding="utf-8"), flags=re.S)
    assert not re.findall(r"font-weight:\s*(?:[5-9]00|bold|bolder)\s*[;}]", css), sheet
    assert not re.findall(r"var\(--ink(?:-\d)?\)", css), sheet
