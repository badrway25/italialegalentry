"""
Every status chip in the templates is drawn by the `{% chip %}` pair, with a register that is one of eight and the
mark of that register.

Phase 1b of the status chip (24 September 2026) put a `data-register` on 63 hand-written `.state` elements in 32
templates. Design V5 (W1-C, V5.4 plan §1.2) gives every chip its mark — «i cerchi», the sign that says the state
without colour — and a mark cannot be asked of eighty hand-written elements one by one. So the element has ONE
producer: `{% chip MEMBER "app.Enum" %}word{% endchip %}` (apps/core/templatetags/ile_core.py), which renders
templates/components/chip.html with the member's register and the register's mark, both from apps/core/chips.py.
«A chip is never drawn without its mark» is then true by construction, and this file holds the construction:

* no product template writes a chip, a `.state` or a `.badge` element by hand, and none includes the partial;
* every call names a producer that chips.py knows, or a register that is one of the eight; a register computed
  elsewhere is on a short list, each entry with its reason;
* rendered, every member of every producer comes out as one element with its register, its mark from the sprite and
  its word — the case statuses with their gauge; an unknown value is drawn without a register, and logged;
* the two places that speak the registers without being chips — the health strip, the filter's legend — take
  theirs from Python too, and the filter draws the chip's own mark.

The check of the call sites is on the SOURCE, call by call, because the templates render behind sessions and
fixtures that no single test can set up for all of them; the rendering is checked through the tag itself, member by
member, which is what every one of those sites runs.
"""

from __future__ import annotations

import logging
import re
import sys
from pathlib import Path

import pytest
from django.template import Context, Template

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "apps"))

from core import chips, icons  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
#: The product's templates: the project tree and every app's. The dev-only pages (the showcase, the preview, the
#: specimen boards) draw the chip to show it, unknown values included, and label their own pages with `dp-state`.
TEMPLATE_ROOTS = [ROOT / "templates", *sorted((ROOT / "apps").glob("*/templates"))]
PARTIAL = "templates/components/chip.html"

#: `{% chip … %}` — the opening tag and its arguments.
CALL = re.compile(r"\{%\s*chip\s(?P<args>[^%]*?)\s*%\}")
END = re.compile(r"\{%\s*endchip\s*%\}")
#: An element whose class list holds `chip`, `state` or `badge` as a whole word: a chip written by hand. (A dot on
#: either side is a template variable inside the attribute — `{% if step.state == … %}` — not a class.)
HAND = re.compile(r'<[a-z][a-z0-9]*\b[^>]*\bclass="[^"]*(?<![\w.-])(?:chip|state|badge)(?![\w.-])[^"]*"[^>]*>', re.I)
ARG = re.compile(r"""(?:(?P<key>\w+)=)?(?P<value>"[^"]*"|'[^']*'|[^\s"']+)""")
KWARGS = {"register", "size", "css_class", "role", "lang", "title"}
#: A class the caller may pass: it PLACES the chip in its page. A word that used to paint — or pretended to — is not one.
PAINT = re.compile(r"(?<![\w-])(?:state|chip)(?:--[\w-]+)?(?![\w-])|badge--")
#: The calls whose register is computed elsewhere, each with its reason. Everything else is a literal or a producer.
COMPUTED = {
    ("templates/components/badge.html", "kind|badge_register"): "the legacy `kind`, translated by chips.KIND_REGISTER",
    (
        "templates/components/case_timeline.html",
        "row.chip_register",
    ): "cases.presenters.timeline reads the audit event's member",
}
#: Where `data-register` may be written in a template: the partial, and the two elements that speak the registers
#: without being chips.
NOT_CHIPS = {
    "templates/components/health_strip.html": "health__segment",
    # the state filter's entries, drawn in the register's flow and in its sheet from one partial (W3-C)
    "templates/documents/partials/state_filter.html": "seg__dot",
}


def _templates() -> list[Path]:
    files: list[Path] = []
    for root in TEMPLATE_ROOTS:
        files += sorted(p for p in root.rglob("*.html") if "dev" not in p.relative_to(root).parts)
    assert files
    return files


def _rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def _source(path: Path) -> str:
    """A template without its comment blocks: a contract may name the pair, or quote the markup it replaced."""
    return re.sub(r"\{% comment %\}.*?\{% endcomment %\}", "", path.read_text(encoding="utf-8"), flags=re.S)


def _calls() -> list[tuple[str, str]]:
    found = []
    for path in _templates():
        for match in CALL.finditer(_source(path)):
            found.append((_rel(path), match.group("args")))
    return found


def _parse(args: str) -> tuple[list[str], dict[str, str]]:
    positional, keyword = [], {}
    for match in ARG.finditer(args):
        if match.group("key"):
            keyword[match.group("key")] = match.group("value")
        else:
            positional.append(match.group("value"))
    return positional, keyword


def _literal(value: str) -> str | None:
    return value[1:-1] if value[:1] in "\"'" and value[-1:] == value[:1] else None


CALLS = _calls()


def _render(source: str, **context) -> str:
    return Template(source).render(Context(context))


def _chip(register: str, mark: str, word: str, *, classes: str = "chip", extra: str = "") -> str:
    """The one markup of a chip, as the partial writes it."""
    attr = f' data-register="{register}"' if register else ""
    return (
        rf'<span class="{classes}"{attr}{extra}><svg class="icon chip__g" aria-hidden="true" focusable="false">'
        rf'<use href="[^"#]*/img/icons\.svg(?:\?v=[0-9a-f]+)?#icon-{mark}"></use></svg>'
        rf'<span class="chip__w">{word}</span>'
    )


# ---- the call sites --------------------------------------------------------------------------------------


def test_the_scan_sees_the_converted_sites():
    """A regex that matches nothing would pass every other test here for the wrong reason."""
    assert len(CALLS) >= 75, len(CALLS)
    assert len({path for path, _ in CALLS}) >= 40


def test_no_template_writes_a_chip_by_hand():
    """A hand-written element has no mark, and nothing would notice. The partial is the only place the element is
    written; a page that needs a state asks the tag for it."""
    by_hand = []
    for path in _templates():
        if _rel(path) == PARTIAL:
            continue
        for match in HAND.finditer(_source(path)):
            by_hand.append((_rel(path), match.group(0)[:110]))
    assert not by_hand, by_hand
    assert len(HAND.findall(_source(ROOT / PARTIAL))) == 1, "the partial writes ONE element"


def test_the_partial_is_rendered_by_the_tag_alone():
    for path in _templates():
        assert "components/chip.html" not in _source(path), f"{_rel(path)} includes the partial"


def test_every_chip_is_closed_and_none_is_nested():
    for path in _templates():
        text = _source(path)
        events = sorted(
            [(m.start(), "open") for m in CALL.finditer(text)] + [(m.start(), "close") for m in END.finditer(text)]
        )
        kinds = [kind for _, kind in events]
        assert kinds == ["open", "close"] * (len(kinds) // 2), f"{_rel(path)}: {kinds}"


@pytest.mark.parametrize(("path", "args"), CALLS, ids=[f"{p}:{i}" for i, (p, _) in enumerate(CALLS)])
def test_every_chip_call_names_a_known_producer_or_one_of_the_eight_registers(path, args):
    positional, keyword = _parse(args)
    assert set(keyword) <= KWARGS, f"{path}: {sorted(set(keyword) - KWARGS)}"
    if positional:
        assert len(positional) == 2 and "register" not in keyword, f"{path}: {args}"
        producer = _literal(positional[1])
        assert producer in chips.REGISTER, f"{path}: unknown producer {positional[1]} — the chip would be unmapped"
        assert _literal(positional[0]) is None, f"{path}: the member is the object's, not a literal"
    else:
        assert "register" in keyword, f"{path}: a chip without a producer and without a register — {args}"
        word = _literal(keyword["register"])
        if word is None:
            assert (path, keyword["register"]) in COMPUTED, f"{path}: register={keyword['register']} is not on the list"
        else:
            assert word in chips.REGISTERS, f"{path}: {word!r} is not a register"
    if "size" in keyword:
        assert _literal(keyword["size"]) in ("s", "l"), f"{path}: {keyword['size']}"
    placed = _literal(keyword.get("css_class", '""'))
    assert placed is not None and not PAINT.search(placed), f"{path}: css_class places a chip, it never paints one"


def test_the_computed_registers_are_all_used():
    used = {(path, _parse(args)[1].get("register", "")) for path, args in CALLS}
    assert set(COMPUTED) <= used, sorted(set(COMPUTED) - used)


# ---- what the tag renders ------------------------------------------------------------------------------------


@pytest.mark.parametrize("producer", sorted(chips.REGISTER))
def test_every_member_is_rendered_with_its_register_its_mark_and_its_word(producer):
    for member, register in chips.REGISTER[producer].items():
        html = _render("{% chip value producer %}Mot{% endchip %}", value=member, producer=producer)
        mark = chips.mark_for(register, producer, member)
        assert mark in icons.SYMBOLS and mark not in icons.CHECK_BEARING
        match = re.fullmatch(_chip(register, mark, "Mot") + r"(?P<meter>.*)</span>", html)
        assert match, f"{producer}.{member}: {html}"
        stage = chips.STAGE.get(member) if producer == chips.STAGE_PRODUCER else None
        if stage:
            notches = "".join('<span class="is-on"></span>' if n <= stage else "<span></span>" for n in (1, 2, 3))
            assert match.group("meter") == f'<span class="chip__meter" aria-hidden="true">{notches}</span>'
        else:
            assert match.group("meter") == "", f"{producer}.{member}: {match.group('meter')}"


@pytest.mark.parametrize("register", chips.REGISTERS)
def test_a_register_the_template_knows_is_rendered_the_same_way(register):
    html = _render(
        '{% chip register=word css_class="entry__actor" size="s" role="status" lang="it" %}Mot{% endchip %}',
        word=register,
    )
    assert re.fullmatch(
        _chip(
            register,
            icons.STATUS[register],
            "Mot",
            classes="entry__actor chip chip--s",
            extra=' role="status" lang="it"',
        )
        + "</span>",
        html,
    ), html


def test_the_word_is_the_block_already_rendered_and_never_escaped_twice():
    html = _render(
        '{% load i18n %}{% chip register="azione" %}\n  {% blocktranslate count n=n %}{{ n }} en retard{% plural %}'
        '{{ n }} en retard{% endblocktranslate %}\n{% endchip %}|{% chip register="neutro" %}{{ label }}{% endchip %}',
        n=3,
        label="R&D <b>",
    )
    late, escaped = html.split("|")
    assert '<span class="chip__w">3 en retard</span>' in late, late
    assert '<span class="chip__w">R&amp;D &lt;b&gt;</span>' in escaped, escaped


def test_an_unknown_value_is_drawn_without_a_register_and_said_in_the_log(caplog):
    with caplog.at_level(logging.WARNING, logger="core.templatetags.ile_core"):
        unknown = _render('{% chip "no-such-member" "cases.CaseStatus" %}Mot{% endchip %}')
        not_a_register = _render('{% chip register="verde" %}Mot{% endchip %}')
    for html in (unknown, not_a_register):
        assert re.fullmatch(_chip("", icons.STATUS["neutro"], "Mot") + "</span>", html), html
        assert "data-register" not in html
    assert len(caplog.records) == 2 and "no register" in caplog.records[0].getMessage()
    assert "is not a register" in caplog.records[1].getMessage()


def test_a_chip_without_a_word_is_not_drawn():
    assert _render('[{% chip register="neutro" %}  {{ nothing }}  {% endchip %}]') == "[]"


def test_the_partial_draws_the_mark_the_tag_gives_it_never_a_literal():
    partial = _source(ROOT / PARTIAL)
    assert '{% svg_icon mark "icon chip__g" %}' in partial and partial.count("svg_icon") == 1
    assert '{% if register %} data-register="{{ register }}"{% endif %}' in partial
    assert '<span class="chip__w">{{ label }}</span>' in partial
    assert not re.search(r"icon-|st-[a-z]", partial), "no symbol is named here: the registry decides"


def test_the_badge_component_is_a_chip_for_every_kind():
    for kind, register in chips.KIND_REGISTER.items():
        html = _render('{% include "components/badge.html" with label="Mot" kind=kind only %}', kind=kind).strip()
        assert re.fullmatch(_chip(register, icons.STATUS[register], "Mot", classes="badge chip") + "</span>", html), (
            html
        )
    assert "badge--" not in _source(ROOT / "templates" / "components" / "badge.html")


# ---- the elements that speak the registers without being chips ---------------------------------------------


def test_data_register_is_written_by_the_partial_and_by_two_legends_only():
    for path in _templates():
        text = _source(path)
        if "data-register" not in text:
            continue
        rel = _rel(path)
        assert rel == PARTIAL or rel in NOT_CHIPS, f"{rel} writes data-register by hand"
        if rel in NOT_CHIPS:
            tags = re.findall(r"<[a-z]+\b[^>]*data-register=[^>]*>", text)
            assert tags and all(NOT_CHIPS[rel] in tag and 'data-register="{{ f.register }}"' in tag for tag in tags), (
                rel,
                tags,
            )


def test_the_filters_legend_draws_the_chips_own_mark():
    """Icon review m4: «Manquant» and «À remplacer» shared one V4 dot. The filter's entry draws the member's mark
    from the same registry as the chip — two marks for the one register — on the element that carries the register."""
    text = _source(ROOT / "templates" / "documents" / "partials" / "state_filter.html")
    assert (
        '<span class="seg__dot" data-register="{{ f.register }}" aria-hidden="true">'
        '{% svg_icon f.value|chip_mark:"documents.RequirementState" "icon chip__g" %}</span>'
    ) in text
    drawn = {
        member: _render('{{ m|chip_mark:"documents.RequirementState" }}', m=member)
        for member in chips.REGISTER["documents.RequirementState"]
    }
    assert drawn["missing"] == "st-attesa" and drawn["to_replace"] == "st-attesa-replace"
    assert len(set(drawn.values())) == len(drawn), "one mark per state of a piece"
    assert _render('{{ "blocco"|chip_mark }}|{{ ""|chip_mark }}') == "lock|st-neutro"


def test_a_tag_is_a_term_and_carries_neither_a_register_nor_a_mark():
    """static/css/v5/chip.css §4: the glossary's words under a pathway, the level asked of a competence, the kind of
    a message — terms, not states. They are written by hand, and say nothing a register says."""
    found = []
    for path in _templates():
        for match in re.finditer(r'<(a|span)\b[^>]*\bclass="tag"[^>]*>(.*?)</\1>', _source(path), flags=re.S):
            found.append(_rel(path))
            assert "data-register" not in match.group(0) and "svg_icon" not in match.group(0), _rel(path)
    assert len(found) >= 9 and {"templates/pathways/detail.html", "templates/companies/need_detail.html"} <= set(found)
