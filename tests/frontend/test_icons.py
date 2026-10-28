"""
The ILE icon system — design V5 (V5.4 plan §1.7; apps/core/icons.py; the research map ICON_SEMANTIC_MAP.md §8).

One concept, one glyph: the registry IS the sprite; every template literal is a registered symbol and never a
V4 alias, a status mark or the seal; the size floors, the twins, the closed flip list and the check rule hold;
the producers' maps are the registry's; the tag resolves, flips and hashes; the build is current and the sprite
stays under its ceiling; no icon library ships. W1-B's tests (plan §2.7).
"""

from __future__ import annotations

import hashlib
import re
import subprocess
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

import pytest
from django.template import Context, Template

from core import icons

ROOT = Path(__file__).resolve().parents[2]
SPRITE = ROOT / "static" / "img" / "icons.svg"
SOURCES = ROOT / "static" / "icons" / "src"
#: The product's templates: the project tree and every app's; the dev-only pages (the showcase, the preview,
#: the specimen boards) draw the sheet itself and are not the product.
TEMPLATE_ROOTS = [ROOT / "templates", *sorted((ROOT / "apps").glob("*/templates"))]
NS = "{http://www.w3.org/2000/svg}"
#: `{% svg_icon "name" "classes" %}`: a literal name, and the class argument when it is a literal too.
LITERAL = re.compile(r'svg_icon\s+"([a-z0-9-]+)"(?:\s+"([^"]*)")?')
#: Where a check-bearing symbol is never drawn (the check rule, IC §2): a chip, a badge, a journey node or
#: station, the ledger, a rail, an actor disc, a filter chip.
CHECK_FREE = re.compile(r"(chip|badge|glyph|journey|timeline|stepper|rail|ledger|portal_chrome|filter)", re.I)
LIBRARIES = re.compile(r"lucide|phosphor|heroicons|tabler|@radix-ui/react-icons", re.I)

pytestmark = pytest.mark.compliance


def _symbols() -> list[ET.Element]:
    return list(ET.parse(SPRITE).getroot().iter(f"{NS}symbol"))


def _sprite_ids() -> list[str]:
    return [el.get("id", "")[len("icon-") :] for el in _symbols()]


def _templates() -> list[Path]:
    files: list[Path] = []
    for root in TEMPLATE_ROOTS:
        files += sorted(p for p in root.rglob("*.html") if "dev" not in p.relative_to(root).parts)
    assert files
    return files


def _literals() -> list[tuple[Path, str, str]]:
    found = []
    for path in _templates():
        for name, classes in LITERAL.findall(path.read_text(encoding="utf-8")):
            found.append((path, name, classes))
    assert found
    return found


# ---------------------------------------------------------------------------------------------
# The registry and the sprite
# ---------------------------------------------------------------------------------------------
def test_the_registry_is_the_sprite():
    ids = _sprite_ids()
    assert len(ids) == len(set(ids)), "a symbol twice"
    assert ids == [*icons.SYMBOLS, *icons.LEGACY], "the sprite = the registry's symbols in its order, then the V4 aliases"
    assert not set(icons.LEGACY) & set(icons.SYMBOLS)
    assert set(icons.LEGACY.values()) <= set(icons.SYMBOLS)
    # The aliases that still have a producer, and no other (each leaves with its last one): `user` and `key`
    # left with the review's fix pass — an alias nobody emits is not kept «just in case».
    assert icons.LEGACY == {"home": "house", "list": "send", "globe": "languages"}
    assert len(icons.SYMBOLS) == 110


def test_the_sprite_is_strict_xml_clean_and_under_its_ceiling():
    raw = SPRITE.read_bytes()
    assert b"\r" not in raw, "LF bytes"
    assert len(raw) <= icons.SPRITE_MAX_BYTES, (len(raw), icons.SPRITE_MAX_BYTES)
    text = raw.decode("utf-8")
    for comment in re.findall(r"<!--(.*?)-->", text, re.S):
        assert "--" not in comment, "«--» inside an XML comment discards the whole sprite (G-01)"
    markup = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    assert not re.search(r"#[0-9a-fA-F]{3,8}\b", markup), "a literal colour"
    assert "<style" not in markup and "style=" not in markup
    assert "stroke-width" not in markup, "the stroke is the .icon rule's, never the sprite's"
    for el in _symbols():
        assert el.get("viewBox") == "0 0 24 24", el.get("id")
        children = list(el)
        assert children, f"{el.get('id')} is empty"
        for child in children:
            tag = child.tag[len(NS) :]
            if child.get("stroke") == "none":
                assert child.get("fill") == "currentColor", (el.get("id"), tag)
            else:
                assert tag == "path" and child.get("vector-effect") == "non-scaling-stroke", (el.get("id"), tag)


def test_every_source_is_registered_names_its_origin_and_sits_on_the_24_grid():
    stems = {p.stem for p in SOURCES.glob("*.svg")}
    assert stems == set(icons.SYMBOLS), (sorted(stems - set(icons.SYMBOLS)), sorted(set(icons.SYMBOLS) - stems))
    for sid, symbol in icons.SYMBOLS.items():
        raw = (SOURCES / f"{sid}.svg").read_bytes()
        assert b"\r" not in raw, sid
        text = raw.decode("utf-8")
        origin = " ".join(re.findall(r"<!--(.*?)-->", text, re.S))
        if symbol.donor:
            assert f'Lucide "{symbol.donor}" {icons.LUCIDE_VERSION}' in origin, sid
        else:
            assert "ILE drawing" in origin, sid
        assert 'viewBox="0 0 24 24"' in text, sid


def test_the_build_is_current():
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "build_icons.py"), "--check"],
        capture_output=True,
        text=True,
        cwd=ROOT,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_tiers_floors_flip_list_twins_and_check_bearing_are_consistent():
    sizes = set(icons.SIZE_CLASSES.values())
    for sid, symbol in icons.SYMBOLS.items():
        assert symbol.tier in icons.TIERS, sid
        assert symbol.floor in sizes, (sid, symbol.floor)
        assert symbol.meaning, sid
    identity = {sid for sid, s in icons.SYMBOLS.items() if s.tier == icons.IDENTITY}
    status = {sid for sid, s in icons.SYMBOLS.items() if s.tier == icons.STATUS_TIER}
    assert identity == {"ile-arch", "ile-key", "ile-steps", "ile-mark"}
    assert status == {sid for sid in icons.SYMBOLS if sid.startswith("st-")}
    assert icons.FLIP_RTL == {"arrow", "arrow-start", "chevron-end", "logout", "send", "signpost", "panel-left-close"}
    assert not icons.FLIP_RTL & (identity | status), "the identity tier and the marks never mirror"
    assert icons.FLIP_RTL <= set(icons.SYMBOLS)
    for group in icons.TWINS:
        assert len(group) >= 2 and group <= set(icons.SYMBOLS), group
    assert set(icons.CHECK_BEARING) == {"check", "circle-check", "badge-check", "vote"}
    assert icons.MIN_SIZE == {sid: s.floor for sid, s in icons.SYMBOLS.items()}
    for domain, mapping in icons.DOMAINS.items():
        assert set(mapping.values()) <= set(icons.SYMBOLS), domain
    assert set(icons.SHARED) <= set(icons.SYMBOLS)
    grouped = [name for _label, names in icons.GROUPS for name in names]
    assert sorted(grouped) == sorted(icons.SYMBOLS) and len(grouped) == len(set(grouped)), "the sheet's groups"


def test_the_12_percent_tone_sits_on_the_concept_tier_only():
    toned = {el.get("id", "")[5:] for el in _symbols() if any(child.get("fill-opacity") == ".12" for child in el)}
    toned = {icons.LEGACY.get(sid, sid) for sid in toned}  # an alias draws its symbol's geometry, tone included
    assert toned
    # ile-arch: the 12 % tone inside the inner opening is the drawing the review recorded (IC §1).
    wrong = sorted((sid, icons.SYMBOLS[sid].tier) for sid in toned if icons.SYMBOLS[sid].tier != icons.CONCEPT and sid != "ile-arch")
    assert wrong == [], f"toned outside the concept tier: {wrong}"


def test_a_symbol_under_two_concept_keys_is_a_reviewed_shared_one():
    uses: dict[str, set[tuple[str, str]]] = {}
    for domain, mapping in icons.DOMAINS.items():
        for key, sid in mapping.items():
            uses.setdefault(sid, set()).add((domain, key))
    multi = {sid for sid, where in uses.items() if len(where) > 1}
    assert multi <= set(icons.SHARED), sorted(multi - set(icons.SHARED))


def test_twins_never_meet_inside_one_list_domain():
    for domain in icons.LIST_DOMAINS:
        values = set(icons.DOMAINS[domain].values())
        for group in icons.TWINS:
            assert len(values & group) <= 1, (domain, sorted(values & group))


# ---------------------------------------------------------------------------------------------
# The templates
# ---------------------------------------------------------------------------------------------
def test_template_literals_are_symbols_never_aliases_marks_or_the_seal():
    for path, name, _classes in _literals():
        assert name in icons.SYMBOLS, f"{path}: {name!r} is not a symbol (a V4 alias goes through the registry)"
        assert icons.SYMBOLS[name].tier != icons.STATUS_TIER, f"{path}: a status mark is the chip's, never a literal"
        assert name not in ("badge-check", "badge-dot"), f"{path}: the seal and the actor go through the registry"


def test_check_bearing_symbols_stay_out_of_chips_nodes_rails_and_discs():
    names = set()
    for path, name, _classes in _literals():
        names.add(name)
        if name in icons.CHECK_BEARING:
            assert not CHECK_FREE.search(path.name), f"{path}: {name} drawn in {path.name}"
    assert "vote" not in names, "vote is the civic-education topic's, through LIVING, on its own page"
    assert "badge-check" not in names


def test_no_literal_renders_a_symbol_below_its_floor():
    for path, name, classes in _literals():
        below = icons.floor_violation(name, classes)
        assert below is None, f"{path}: {name} at {below} px, floor {icons.MIN_SIZE[name]} px"


def test_the_producers_maps_are_the_registrys():
    from cases.models import ResponsibleActor
    from cms.templatetags.cms_nav import _DOOR_ICONS
    from core import chips
    from documents.requirements import ACTOR_GLYPHS
    from living.catalogue import TOPIC_SLUGS
    from pages.content import ENTRANCES
    from pathways.services import DEFAULT_ICONS
    from portal.services import NAV_GLYPHS

    assert ACTOR_GLYPHS == icons.ACTOR
    assert set(icons.ACTOR) == set(ResponsibleActor.values)
    assert set(icons.AUDIENCE) == {entrance.actor for entrance in ENTRANCES}
    assert _DOOR_ICONS == icons.AUDIENCE, "the navbar's door panels draw the four audiences' glyphs («Il portico»)"
    assert set(icons.PATHWAY) == set(DEFAULT_ICONS)
    assert set(icons.LIVING) == set(TOPIC_SLUGS)
    assert NAV_GLYPHS == icons.NAV, "the rail, its bottom bar and its drawer draw the registry's map (review M1)"
    assert set(icons.CARD) == {"requests", "orientation", "documents", "deadlines", "messages", "organisation"}
    assert set(chips.REGISTERS) <= set(icons.STATUS)
    assert icons.STATUS["conforme"] not in icons.CHECK_BEARING, "conforme is a plain disc, never a check"
    assert set(icons.DUE) == {"", "upcoming", "soon", "overdue"}, "documents.requirements.due_urgency's values"
    assert set(icons.ALERT) == {"debug", "info", "success", "warning", "error"}
    assert {"info", "warning", "error", "pending", "unavailable", "institutional"} <= set(icons.NOTICE)


def test_the_rails_emit_the_registrys_symbol_for_every_entry(monkeypatch):
    """Review M1: the console rail, the bottom bar and the drawer said V4 meanings with the V5 drawings —
    `handshake` for the help desk, `briefcase` for the cases, `map-pin` for the journey, the mortarboard for the
    Academy. Every entry of both navigations now carries the registry's symbol, and never a V4 alias."""
    from django.urls import reverse

    from companies import services as company_services
    from portal import services as portal_services

    monkeypatch.setattr(portal_services, "unread_count", lambda user: 0)
    monkeypatch.setattr(
        portal_services,
        "_role_entries",
        lambda user: [
            (key, portal_services.ROLE_SURFACE_LABELS[key], reverse(route))
            for _role, key, route in portal_services.ROLE_SURFACES
        ],
    )
    # «Communications d’identité» is a row for the account somebody has asked (W3-A): the stand-in is handed it
    monkeypatch.setattr(
        portal_services,
        "_identity_panel",
        lambda user: ("disclosures", "Communications d’identité", reverse("selection:disclosures")),
    )
    rail = portal_services.navigation(object())
    assert {entry["key"] for entry in rail} == set(icons.NAV), "every key of the rail is in the registry, and back"
    for entry in rail:
        assert entry["icon"] == icons.NAV[entry["key"]], entry["key"]

    monkeypatch.setattr(company_services, "may_read_analysis", lambda user: True)
    company_rail = company_services.navigation(object(), company=object())
    assert {entry["key"] for entry in company_rail} == set(icons.COMPANY_NAV)
    for entry in company_rail:
        assert entry["icon"] == icons.COMPANY_NAV[entry["key"]], entry["key"]

    drawn = {entry["icon"] for entry in (*rail, *company_rail)}
    assert drawn <= set(icons.SYMBOLS), "a symbol, never a V4 alias"
    # the symbols the review named keep the one meaning they have everywhere else: the rails do not draw them
    assert not drawn & {"handshake", "briefcase", "map-pin", "university", "calendar", "check"}, drawn
    # the rail and the bottom bar draw 20 px (console.css): no entry asks for more
    assert max(icons.MIN_SIZE[symbol] for symbol in drawn) <= 20


# ---------------------------------------------------------------------------------------------
# The empty state, the one hand, forced colours (the review's fix pass)
# ---------------------------------------------------------------------------------------------
EMPTY_INCLUDE = re.compile(r'{%\s*include\s+"components/empty_state\.html"([^%]*)%}')


def test_the_empty_state_draws_its_space_or_the_neutral_mark_never_document_by_default():
    """Review M3: the partial defaulted to `document` — the glyph of «Mes pièces» — and 22 of its 28 callers passed
    none, so `document` meant «nothing here yet» on ten public pages. The default is the neutral mark; a caller that
    names a glyph names a symbol its 24 px seat can draw; nobody draws the neutral mark for anything else."""
    assert icons.EMPTY_STATE == "empty" and icons.SYMBOLS["empty"].tier == icons.UTILITY
    partial = (ROOT / "templates" / "components" / "empty_state.html").read_text(encoding="utf-8")
    assert '{% svg_icon icon|default:"empty" "icon empty-state__icon" %}' in partial
    assert 'default:"document"' not in partial

    def render(**context) -> str:
        return Template('{% include "components/empty_state.html" %}').render(Context({"title": "Titre", **context}))

    assert "#icon-empty" in render() and "#icon-document" not in render()
    assert "#icon-empty" in render(icon=""), "a caller whose registry key gives nothing gets the neutral mark"
    assert "#icon-newspaper" in render(icon="newspaper") and "#icon-empty" not in render(icon="newspaper")

    callers = 0
    for path in _templates():
        text = path.read_text(encoding="utf-8")
        assert 'svg_icon "empty"' not in text, f"{path}: the neutral mark is the empty state's default and nothing else"
        for arguments in EMPTY_INCLUDE.findall(text):
            callers += 1
            literal = re.search(r'\bicon="([a-z0-9-]*)"', arguments)
            if literal is None:
                continue
            name = literal.group(1)
            assert name in icons.SYMBOLS, f"{path}: {name!r}"
            assert name != "empty", f"{path}: the neutral mark is the default — pass nothing"
            assert icons.SYMBOLS[name].tier in (icons.CONCEPT, icons.IDENTITY), f"{path}: {name} is not a space's glyph"
            assert icons.MIN_SIZE[name] <= 24, f"{path}: {name} needs more than the empty state's 24 px seat"
    # 21 + the Forum's two: the pathway sheet's four sections being verified say so in words on the «attesa» edge since
    # W3-F1 (11 Oct 2026; a glyph in each would break the six-icon ceiling of its editorial body, DL54-29 item 1)
    assert callers >= 21, callers
    # the pages the review named: each says which space is empty
    for template, symbol in (
        ("faq/index.html", "circle-help"),
        ("glossary/index.html", "book-a"),
        ("news/index.html", "newspaper"),
        ("pages/home/_news.html", "newspaper"),
        ("forum/index.html", "handshake"),
        ("forum/register.html", "handshake"),
        ("living/index.html", "sprout"),
    ):
        text = (ROOT / "templates" / template).read_text(encoding="utf-8")
        found = [re.search(r'\bicon="([a-z0-9-]*)"', a) for a in EMPTY_INCLUDE.findall(text)]
        assert found and all(m is not None and m.group(1) == symbol for m in found), (template, symbol)


def _sheets() -> list[Path]:
    """The stylesheets people write: the cascade, the page sheets, the console's — not the bundles, not the dev boards."""
    sheets = [p for p in (ROOT / "static" / "css").rglob("*.css") if not {"dist", "dev"} & set(p.relative_to(ROOT).parts)]
    sheets += list((ROOT / "apps").glob("*/static/**/*.css"))
    assert len(sheets) > 20
    return sorted(sheets)


#: A rule that would draw a glyph thinner than the hand, kept visible here with its owner until it goes. None is
#: left: the last one went with its section (W4-D part 2, 71fbd90). A new entry needs an owner and a date to go.
THINNER_RULES_WITH_AN_OWNER: set[tuple[str, str]] = set()


def test_no_sheet_draws_a_glyph_with_a_thinner_hand_than_the_icon_rule():
    """Review M2: every stroke of the sprite is non-scaling, so a `stroke-width` a component wrote for the old
    scaling sprite is CSS px now — `.empty-state__icon { stroke-width: 1.25 }` drew the empty states lighter than
    every other glyph of their page. The .icon rule is the one hand; nothing on a glyph goes below its 1.5 px."""
    components = (ROOT / "static" / "css" / "components.css").read_text(encoding="utf-8")
    icon_rule = re.search(r"\n\.icon \{([^}]*)\}", components).group(1)
    assert "stroke-width: 1.5;" in icon_rule and "stroke-linecap: square;" in icon_rule and "stroke-linejoin: miter;" in icon_rule
    empty = re.search(r"\n\.empty-state__icon \{([^}]*)\}", components).group(1)
    assert "stroke-width" not in empty
    thinner = set()
    for path in _sheets():
        css = re.sub(r"/\*.*?\*/", "", path.read_text(encoding="utf-8"), flags=re.S)
        for selector, body in re.findall(r"([^{}]+)\{([^{}]*)\}", css):
            if not re.search(r"icon|glyph|chip__g", selector):
                continue
            for value in re.findall(r"(?<![-\w])stroke-width:\s*([0-9.]+)", body):
                if float(value) < 1.5:
                    thinner.add((path.relative_to(ROOT).as_posix(), selector.strip()))
    assert thinner == THINNER_RULES_WITH_AN_OWNER, sorted(thinner ^ THINNER_RULES_WITH_AN_OWNER)


def test_under_forced_colours_an_icon_inherits_its_ink_and_paints_no_ground():
    """The a11y check of «Il portico», finding 7 (handed to the icon system): a browser's <svg> follows the forced
    palette only while its own `color` is inherited, so a glyph coloured by its component kept its authored hex.
    components.css §2 makes every icon inherit again under forced colours — and drop a ground of its own, which
    would stay light under an ink turned white. tests/frontend/test_browser_w1_b.py reads it in the browser."""
    components = (ROOT / "static" / "css" / "components.css").read_text(encoding="utf-8")
    # §2 runs to the next numbered section — §3 «Badges» left with the chip (v5/chip.css, W1-C), so its number is not named
    start = components.index("   2. Icons")
    section = components[start : start + re.search(r"\n   \d+\. ", components[start + 1 :]).start() + 1]
    block = re.search(r"@media \(forced-colors: active\) \{\s*\.icon \{([^}]*)\}\s*\}", section)
    assert block, "the forced-colours rule of the icon section"
    assert "color: inherit !important;" in block.group(1) and "background: none !important;" in block.group(1)
    bundle = (ROOT / "static" / "css" / "dist" / "main.css").read_text(encoding="utf-8")
    assert "@media(forced-colors:active){.icon{color:inherit!important;background:none!important}}" in bundle


# ---------------------------------------------------------------------------------------------
# The tag
# ---------------------------------------------------------------------------------------------
def test_the_tag_resolves_aliases_enforces_the_flip_list_and_hashes_the_sprite():
    html = Template(
        '{% svg_icon "home" %}|{% svg_icon "arrow" "icon" %}|{% svg_icon "arrow-up-right" "icon icon--flip-rtl" %}|'
        '{% svg_icon "" %}|{% svg_icon "ile-steps" "icon" %}|{% svg_icon "no-such-icon" %}|'
        '{{ "requests"|concept:"card" }}|{{ "authority"|actor_glyph }}|{{ "nobody"|actor_glyph }}|'
        '{{ "soon"|concept:"due" }}|{{ "x"|concept:"no-such-domain" }}|{% svg_icon "close" "icon" "Fermer" %}'
    ).render(Context({}))
    parts = html.split("|")
    digest = hashlib.sha256(SPRITE.read_bytes()).hexdigest()[:12]
    assert parts[0] == (
        f'<svg class="icon" aria-hidden="true" focusable="false"><use href="/static/img/icons.svg?v={digest}#icon-house">'
        "</use></svg>"
    ), "a V4 alias draws its V5 symbol (`home` is a house, as it always was), from the content-hashed sprite"
    assert 'class="icon icon--flip-rtl"' in parts[1], "a flip-list symbol carries the class"
    assert 'class="icon"' in parts[2] and "flip" not in parts[2], "and no other symbol does, whatever the call wrote"
    assert parts[3] == "" and parts[5] == "", "an empty or unknown name draws nothing"
    assert 'class="icon"' in parts[4] and "flip" not in parts[4], "ile-steps never mirrors (Q8)"
    assert parts[6] == "send" and parts[7] == "stamp" and parts[8] == "" and parts[9] == "clock" and parts[10] == ""
    assert 'role="img" aria-label="Fermer"' in parts[11] and "aria-hidden" not in parts[11]


def test_no_python_producer_and_no_dev_list_emits_a_retired_v4_id():
    """`user` and `key` are gone from the registry and from the sprite: nothing may still name them as an icon —
    the tag would draw nothing. The dev showcase's list names symbols only (an alias there showed a V4 name under a
    V5 drawing), and every `icon="…"` / `"icon": "…"` literal of the apps resolves."""
    from core import dev

    assert set(dev.ICONS) <= set(icons.SYMBOLS), sorted(set(dev.ICONS) - set(icons.SYMBOLS))
    literal = re.compile(r"""(?:\bicon\s*=\s*|["']icon["']\s*:\s*)["']([a-z0-9-]+)["']""")
    for path in sorted((ROOT / "apps").rglob("*.py")):
        if "migrations" in path.parts or "tests" in path.parts:
            continue
        for name in literal.findall(path.read_text(encoding="utf-8")):
            assert name in icons.SYMBOLS or name in icons.LEGACY, f"{path}: icon {name!r} is neither a symbol nor an alias"


# ---------------------------------------------------------------------------------------------
# The product ships no icon library; the licences name every donor
# ---------------------------------------------------------------------------------------------
def test_no_icon_library_in_the_product():
    assert not LIBRARIES.search((ROOT / "package.json").read_text(encoding="utf-8"))
    for path in (ROOT / "static" / "js").rglob("*.js"):
        if "dist" in path.parts or "vendor" in path.parts:
            continue
        assert not LIBRARIES.search(path.read_text(encoding="utf-8")), path
    for path in _templates():
        assert not LIBRARIES.search(path.read_text(encoding="utf-8")), path


def test_the_licences_file_names_every_donor_with_both_notices():
    text = (ROOT / "docs" / "design-v5" / "ICON_LICENSES.md").read_text(encoding="utf-8")
    assert "ISC License" in text and "The MIT License (MIT)" in text and icons.LUCIDE_VERSION in text
    for sid, symbol in icons.SYMBOLS.items():
        if symbol.donor:
            assert f"| `{sid}` | `{symbol.donor}` |" in text, sid
