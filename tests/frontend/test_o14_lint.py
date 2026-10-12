"""
O14 — no check mark says a state. The lint, as a test (design V5, W1-C; V5.4 plan §1.2 «Standing rulings»).

«VALIDE» is ink and a plain disc. This platform approves nothing — «aucun résultat administratif n'est promis» — so
no colour means «approved» (tests/frontend/test_v5_tokens.py) and no SIGN does either: a tick beside a piece, a
step, a file or a filter reads as a verdict, and it comes back by reflex — every stepper, to-do and timeline of the
kits ends a step with one. The gate-0 lint caught 8 of 11 planted HTML cases, 4 of 5 CSS and 0 of 2 JavaScript (the
research's decision log, A5). This one catches every planted case, and is run on the product:

* HTML — every product template, read as a tree: inside a STATUS CONTEXT (a `{% chip %}`, any element that carries
  `data-register`, a badge, a filter's entry, the health strip, a journey or timeline node, a stepper, a rail, the
  ledger, an actor's disc) no check-bearing symbol of the sprite is drawn, at any depth, and no check character is
  written. A symbol named by a variable must come from a registry map, and the maps are held below.
* CSS — every sheet people write and every bundle that ships: no check character in a `content`, anywhere; and a
  rule that paints a settled state (done · valid · success · completed · conforme) or a status context draws no
  tick — no image of one, no clipped or rotated one.
* JavaScript — no script names a check-bearing symbol or writes a check character: scripts draw no status.
* Python — no producer writes a check character into the page; the one place that does is named, with its reason.

What a check MAY mark is the person's own interface act (apps/core/icons.py CHECK_BEARING): a chosen option card, a
ticked box — drawn by the form sheet — and an account confirmation; and the seal, an authority's act, holds
`badge-check` and nothing else. Those are not status contexts, and the lint leaves them alone (the clean cases).
"""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "apps"))

from core import chips, icons  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE_ROOTS = [ROOT / "templates", *sorted((ROOT / "apps").glob("*/templates"))]

pytestmark = pytest.mark.compliance

# ---- the vocabulary ---------------------------------------------------------------------------------------

#: ✓ ✔ ☑ ✅ 🗸 ⍻ — as characters, and as the escapes of each language.
CHECK_CHARS = re.compile("[✓✔☑✅\U0001f5f8⍻]")
CSS_ESCAPE = re.compile(r"\\0{0,2}(?:2713|2714|2611|2705|1f5f8|237b)(?![0-9a-f])", re.I)
JS_ESCAPE = re.compile(r"\\u(?:2713|2714|2611|2705|237b)|\\u\{0*(?:2713|2714|2611|2705|1f5f8|237b)\}|\\ud83d\\uddf8", re.I)
HTML_ENTITY = re.compile(r"&(?:check|checkmark);|&#0*(?:10003|10004|9745|9989|128504);|&#x0*(?:2713|2714|2611|2705|1f5f8);", re.I)
#: The check stroke as the sprite draws it (ILE `check`; `circle-check` and `badge-check`; Lucide's `m9 12 2 2 4-4`
#: of `vote`) and as Lucide's other ticks do (`M20 6 9 17l-5-5`, `… 3 3L22 4`).
CHECK_STROKE = re.compile(r"4\.5 4\.5L19 7|-5\.5 5\.5L8 12|(?<![\d.])2 2 4-4|M20 6 9 17|3 3L22 4")
#: A name that says tick, for an image or a symbol that is not the sprite's.
CHECK_NAME = re.compile(r"(?<![a-z])(?:check(?!box|ed|list|out|sum|validity|ing)|tick(?!et)|checkmark)", re.I)

#: A status context, by a class token of the element: the chip and what it replaced, the filter, the health strip,
#: the journey, the timelines, the steppers, the rails, the ledger, the meter, an actor's disc, a row's state.
STATUS_CLASS = re.compile(
    r"^(?:chip|badge|state|seg|health|journey|jr|tl|timeline|stepper|wstep|rail|console-bottom|ledger|meter|glyph"
    r"|station|doc-row__state|resp)(?:__[\w-]+|--[\w-]+)?$"
)
#: A variable symbol inside a status context comes from a registry map — and the maps hold no check
#: (test_the_registry_keeps_the_check_out_of_every_status_map).
REGISTRY_FED = re.compile(
    r"^mark$|\|chip_mark\b|^glyph$|\|actor_glyph\b|\|concept:[\"'](?:due|card|actor|nav|company_nav|journey|pathway|audience)[\"']"
    r"|^(?:item|entry|e|step)\.(?:icon|glyph)$"
)

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}


def _check_symbols() -> set[str]:
    """The check-bearing symbols: the registry's four, and any source of the sprite that draws the stroke."""
    found = set(icons.CHECK_BEARING)
    for path in (ROOT / "static" / "icons" / "src").glob("*.svg"):
        if CHECK_STROKE.search(path.read_text(encoding="utf-8")):
            found.add(path.stem)
    return found


CHECKS = _check_symbols()


# ---- HTML ---------------------------------------------------------------------------------------------------


def _prepare(source: str) -> str:
    """A Django template as something an HTML parser can walk: the chip pair is a status element, an icon is a
    <use>; every other tag and variable leaves, the words of the attributes stay."""
    s = re.sub(r"\{% comment %\}.*?\{% endcomment %\}", "", source, flags=re.S)
    s = re.sub(r"\{#.*?#\}", "", s)
    s = re.sub(r"\{%\s*chip\s[^%]*%\}", '<span class="chip" data-register="">', s)
    s = re.sub(r"\{%\s*endchip\s*%\}", "</span>", s)
    s = re.sub(r"""\{%\s*svg_icon\s+["']([a-z0-9-]*)["'][^%]*%\}""", r'<use href="#icon-\1"></use>', s)
    s = re.sub(r"\{%\s*svg_icon\s+([^\s%]+)[^%]*%\}", lambda m: f'<use data-var="{m.group(1).replace(chr(34), chr(39))}"></use>', s)
    s = re.sub(r"\{%.*?%\}", " ", s, flags=re.S)
    return re.sub(r"\{\{.*?\}\}", " ", s, flags=re.S)


class _Scan(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.stack: list[tuple[str, str | None, bool]] = []
        self.findings: list[str] = []

    def _context(self) -> tuple[str | None, bool]:
        label, in_seal = None, False
        for _tag, own, seal in self.stack:
            in_seal = in_seal or seal
            label = label or own
        return label, in_seal

    def _open(self, tag: str, attrs: list[tuple[str, str | None]], push: bool) -> None:
        a = {key: value or "" for key, value in attrs}
        classes = a.get("class", "").split()
        own = None
        if "data-register" in a:
            own = f"{tag}[data-register]"
        else:
            hit = next((c for c in classes if STATUS_CLASS.match(c)), None)
            own = f"{tag}.{hit}" if hit else None
        context, in_seal = self._context()
        context = context or own
        if tag in ("use", "image", "img") and context:
            href = a.get("href") or a.get("xlink:href") or a.get("src") or ""
            symbol = re.search(r"#icon-([\w-]+)\s*$", href)
            name = symbol.group(1) if symbol else ""
            if name in CHECKS and not (in_seal and name == "badge-check"):
                self.findings.append(f"icon-{name} inside {context}")
            elif not symbol and href and CHECK_NAME.search(href):
                self.findings.append(f"an image named {href[-40:]!r} inside {context}")
            variable = a.get("data-var")
            if variable and not REGISTRY_FED.search(variable):
                self.findings.append(f"a symbol chosen by `{variable}` inside {context}: not a registry map")
        if push and tag not in VOID:
            self.stack.append((tag, own, "seal" in classes))

    def handle_starttag(self, tag, attrs):
        self._open(tag, attrs, True)

    def handle_startendtag(self, tag, attrs):
        self._open(tag, attrs, False)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break

    def _text(self, data: str) -> None:
        context, _ = self._context()
        hit = CHECK_CHARS.search(data) or HTML_ENTITY.search(data)
        if context and hit:
            self.findings.append(f"the check character {hit.group(0)!r} inside {context}")

    def handle_data(self, data):
        self._text(data)

    def handle_entityref(self, name):
        self._text(f"&{name};")

    def handle_charref(self, name):
        self._text(f"&#{name};")


def html_findings(source: str) -> list[str]:
    scan = _Scan()
    scan.feed(_prepare(source))
    scan.close()
    return scan.findings


# ---- CSS ----------------------------------------------------------------------------------------------------

#: A selector that paints a settled state, or a status context.
SETTLED = re.compile(
    r"conforme|--(?:done|valid|success|completed?|approved|verified)(?![\w-])|\.is-(?:done|valid|complete|approved)(?![\w-])"
    r"|\[aria-checked|\.(?:chip|badge|state|seg|health|journey|tl|timeline|stepper|wstep|rail|ledger|meter|glyph)(?:__|--|[^\w-]|$)"
    r"|\[data-register"
)
#: The person's own act, drawn by the form sheet: a native control's tick is not a state.
OWN_ACT = re.compile(r"input\[type=|:checked|\.opt(?:__|\b)|\.form-field|\.wizard__")


def _rules(css: str) -> list[tuple[str, str]]:
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    return [(" ".join(s.split()), b) for s, b in re.findall(r"([^{}]+)\{([^{}]*)\}", css) if s.strip()]


def css_findings(css: str) -> list[str]:
    found = []
    for selector, body in _rules(css):
        for value in re.findall(r"(?<![\w-])content\s*:\s*([^;}]+)", body):
            if CHECK_CHARS.search(value) or CSS_ESCAPE.search(value):
                found.append(f"{selector}: a check character in `content`")
        if not SETTLED.search(selector) or OWN_ACT.search(selector):
            continue
        for url in re.findall(r"url\(\s*([^)]*)\)", body):
            if CHECK_NAME.search(url) or CHECK_STROKE.search(url) or CHECK_CHARS.search(url):
                found.append(f"{selector}: an image of a check")
        if re.search(r"(?<![\w-])clip-path\s*:\s*polygon\(", body):
            found.append(f"{selector}: a clipped tick")
        turned = re.search(r"rotate\(\s*-?(?:4[0-9]|5[0-5]|13[0-9])deg\s*\)|(?<![\w-])rotate\s*:\s*-?(?:4[0-9]|5[0-5])deg", body)
        two_edges = re.search(r"border-width\s*:\s*0\s+\S+\s+\S+\s+0|border-(?:inline-end|right)[\w-]*\s*:[^;]+;[^}]*border-(?:block-end|bottom)[\w-]*\s*:", body)
        if turned and two_edges:
            found.append(f"{selector}: a tick drawn with two edges and a turn")
    return found


# ---- JavaScript and Python -----------------------------------------------------------------------------------

_CHECK_NAMES = "|".join(sorted(map(re.escape, icons.CHECK_BEARING), key=len, reverse=True))
JS_SYMBOL = re.compile(r"icon-(?:" + _CHECK_NAMES + r")(?![\w-])")
JS_NAME = re.compile(r"""["'`](?:check|circle-check|badge-check|check-circle|checkmark|tick)["'`]""")


def js_findings(source: str, *, names: bool = True) -> list[str]:
    """`names`: also refuse a bare symbol name as a string — for the sources people write; a bundle is read for the
    characters and the sprite ids only (a library's own strings are not ours to lint)."""
    code = re.sub(r"/\*.*?\*/", "", source, flags=re.S)
    code = re.sub(r"(?m)(?<![:\"'`\\])//[^\n]*$", "", code)
    found = []
    for pattern, what in ((CHECK_CHARS, "a check character"), (JS_ESCAPE, "an escaped check character"), (HTML_ENTITY, "a check entity"), (JS_SYMBOL, "a check-bearing symbol of the sprite")):
        hit = pattern.search(code)
        if hit:
            found.append(f"{what}: {hit.group(0)!r}")
    if names:
        hit = JS_NAME.search(code)
        if hit:
            found.append(f"a check named as a symbol: {hit.group(0)}")
    return found


def python_findings(source: str) -> list[str]:
    found = []
    for pattern, what in ((CHECK_CHARS, "a check character"), (JS_ESCAPE, "an escaped check character"), (HTML_ENTITY, "a check entity")):
        hit = pattern.search(source)
        if hit:
            found.append(f"{what}: {hit.group(0)!r}")
    hit = re.search(r"""(?:\bicon\s*=\s*|["']icon["']\s*:\s*)["'](?:""" + _CHECK_NAMES + r""")["']""", source)
    if hit:
        found.append(f"a producer names a check-bearing symbol: {hit.group(0)}")
    return found


# ---- the planted cases: the lint catches every one, and leaves the clean ones alone ---------------------------

PLANTED_HTML = {
    "a check in a chip": '<span class="chip" data-register="conforme"><svg class="icon chip__g"><use href="/static/img/icons.svg#icon-check"></use></svg><span class="chip__w">Valide</span></span>',
    "a check in the chip tag's block": '{% chip row.state "documents.RequirementState" %}{% svg_icon "check" "icon" %} Valide{% endchip %}',
    "circle-check beside a state, by the tag": '<span data-register="conforme">{% svg_icon "circle-check" "icon icon--sm" %}Validée</span>',
    "a check character in a chip": '{% chip register="conforme" %}✓ Valide{% endchip %}',
    "a heavy check in a legacy state": '<span class="state state--valid">✔ Validé</span>',
    "a check entity in a badge": '<span class="badge badge--success">&check; Validé</span>',
    "a numeric entity in a chip": '{% chip register="conforme" %}&#10003; Valide{% endchip %}',
    "a check 6 levels deep in a journey node": '<ol class="journey"><li class="journey__step journey__step--done"><div><div><div><span class="journey__node"><svg><use xlink:href="#icon-circle-check"/></svg></span></div></div></div></li></ol>',
    "a check in the chosen filter": '<a class="seg__link" aria-current="true"><svg><use href="#icon-check"></use></svg>Valide</a>',
    "vote in a rail": '<nav class="rail"><ul><li><a class="rail__item" href="#"><svg><use href="#icon-vote"></use></svg>Mes documents</a></li></ul></nav>',
    "badge-check in an actor's disc": '<span class="glyph glyph--sm"><svg><use href="x.svg#icon-badge-check"/></svg></span>',
    "a check in a row's state": '<div class="doc-row"><div class="doc-row__state"><svg><use href="../img/icons.svg#icon-check"/></svg></div></div>',
    "a check on a timeline node": '<ol class="tl"><li class="tl__row"><span class="tl__node"><use href="#icon-check"></use></span></li></ol>',
    "a check in a stepper": '<li class="stepper__item stepper__item--done"><span class="stepper__marker">&#x2713;</span></li>',
    "an image of a tick in a chip": '<span class="chip" data-register="conforme"><img src="/static/img/tick.png" alt="">Valide</span>',
    "a symbol chosen by a free variable in a chip": '{% chip register="conforme" %}{% svg_icon row.icon "icon" %}Valide{% endchip %}',
    "circle-check in a seal": '<span class="chip" data-register="conforme"><span class="seal"><use href="#icon-circle-check"></use></span>Acte</span>',
}
CLEAN_HTML = {
    "a chosen option card": '<label class="opt" for="a"><input type="radio" id="a"><span class="opt__mark" aria-hidden="true">{% svg_icon "check" "icon" %}</span><span class="opt__title">Travail</span></label>',
    "a ticked box's label": '<label class="form-field__check"><input type="checkbox"> ✓ Se souvenir de moi</label>',
    "an account confirmation": '<div class="alert alert--success" role="status">{% svg_icon "circle-check" "icon" %}<p>E-mail confirmé</p></div>',
    "the seal holds badge-check": '<span class="chip" data-register="conforme"><span class="seal"><svg><use href="#icon-badge-check"></use></svg></span>Acte</span>',
    "a chip with its mark": '{% chip row.state "documents.RequirementState" %}{{ row.state_label }}{% endchip %}',
    "the partial's own mark": '<span class="chip" data-register="{{ register }}">{% svg_icon mark "icon chip__g" %}<span class="chip__w">{{ label }}</span></span>',
    "a rail entry from the registry": '<nav class="rail"><a class="rail__item" href="{{ item.url }}">{% svg_icon item.icon "icon" %}{{ item.label }}</a></nav>',
    "a check after a chip has closed": '{% chip register="neutro" %}Déposé{% endchip %}<label class="opt"><span class="opt__mark">{% svg_icon "check" "icon" %}</span></label>',
}
PLANTED_CSS = {
    "a check in content": '.x::before { content: "✓"; }',
    "an escaped check on a done step": '.stepper__item--done .stepper__marker::before { content: "\\2713"; }',
    "a heavy check, escaped and padded": '.list li::marker { content: "\\002714 "; }',
    "an image of a check on a register": '[data-register="conforme"]::before { background: url("../img/check.svg") no-repeat; }',
    "a data URI that draws the stroke": '.chip--valid::after { mask-image: url("data:image/svg+xml,%3Csvg%3E%3Cpath d=\'M20 6 9 17l-5-5\'/%3E%3C/svg%3E"); }',
    "a clipped tick on a valid state": '.state--valid::before { clip-path: polygon(11% 53%, 42% 83%, 91% 26%, 82% 19%, 42% 67%, 19% 45%); background: currentColor; }',
    "the two-edge tick": '.journey__step--done .journey__node::after { content: ""; border: solid currentColor; border-width: 0 2px 2px 0; transform: rotate(45deg); }',
    "the two-edge tick, logical": '.tl__node.is-done::after { border-inline-end: 2px solid; border-block-end: 2px solid; rotate: 45deg; }',
}
CLEAN_CSS = {
    "the checkbox's own tick": ':where(input[type="checkbox"], input[type="radio"])::before { clip-path: polygon(11.2% 53.2%, 42.4% 83%, 90.8% 26.4%, 82.4% 19.2%, 41.6% 67%, 18.8% 45.2%); }',
    "a chosen option card": '.opt:has(input:checked) .opt__mark .icon { opacity: 1; }',
    "the disclosure's chevron": '.accordion__summary::after { border: solid currentColor; border-width: 0 1.5px 1.5px 0; transform: rotate(45deg); }',
    "a done node, filled": '.journey__step--done .journey__node { border-color: var(--accent); background: var(--accent); }',
    "a counter": '.stepper__marker::before { counter-increment: step; content: counter(step); }',
    "the chip's mark": '.chip__g { inline-size: var(--chip-mark-size); color: var(--chip-mark); }',
}
PLANTED_JS = {
    "a check drawn into a chip": "chip.innerHTML = '<svg class=\"icon\"><use href=\"/static/img/icons.svg#icon-check\"></use></svg>' + label;",
    "an escaped check as text": 'node.textContent = "\\u2713 Validé";',
    "a check character": 'row.insertAdjacentHTML("beforeend", "✔");',
    "a symbol by name": 'use.setAttribute("href", sprite + "#icon-" + (done ? "circle-check" : "st-attesa"));',
    "a code point escape": "state.dataset.mark = `\\u{2713}`;",
}
CLEAN_JS = {
    "a native control": 'input.checked = true; if (!form.checkValidity()) return; // check the box\nconst boxes = form.querySelectorAll("input[type=checkbox]");',
    "a status mark": 'use.setAttribute("href", sprite + "#icon-st-conforme");',
}


@pytest.mark.parametrize("case", sorted(PLANTED_HTML))
def test_the_lint_catches_the_planted_html(case):
    assert html_findings(PLANTED_HTML[case]), case


@pytest.mark.parametrize("case", sorted(CLEAN_HTML))
def test_the_lint_leaves_the_persons_own_act_alone_in_html(case):
    assert html_findings(CLEAN_HTML[case]) == [], case


@pytest.mark.parametrize("case", sorted(PLANTED_CSS))
def test_the_lint_catches_the_planted_css(case):
    assert css_findings(PLANTED_CSS[case]), case


@pytest.mark.parametrize("case", sorted(CLEAN_CSS))
def test_the_lint_leaves_the_clean_css_alone(case):
    assert css_findings(CLEAN_CSS[case]) == [], case


@pytest.mark.parametrize("case", sorted(PLANTED_JS))
def test_the_lint_catches_the_planted_javascript(case):
    assert js_findings(PLANTED_JS[case]), case


@pytest.mark.parametrize("case", sorted(CLEAN_JS))
def test_the_lint_leaves_the_clean_javascript_alone(case):
    assert js_findings(CLEAN_JS[case]) == [], case


# ---- the product ------------------------------------------------------------------------------------------------


def _templates() -> list[Path]:
    files: list[Path] = []
    for root in TEMPLATE_ROOTS:
        files += sorted(p for p in root.rglob("*.html") if "dev" not in p.relative_to(root).parts)
    assert len(files) > 150
    return files


def test_no_template_draws_a_check_in_a_status_context():
    found = {}
    for path in _templates():
        hits = html_findings(path.read_text(encoding="utf-8"))
        if hits:
            found[path.relative_to(ROOT).as_posix()] = hits
    assert not found, found


def test_the_one_check_of_the_templates_is_the_persons_own_choice():
    """Where the sprite's `check` IS drawn by a template: the chosen option card, and nowhere else."""
    literal = re.compile(r"""svg_icon\s+["'](""" + "|".join(sorted(CHECKS)) + r""")["']""")
    drawn = {}
    for path in _templates():
        for name in literal.findall(path.read_text(encoding="utf-8")):
            drawn.setdefault(path.relative_to(ROOT).as_posix(), set()).add(name)
    assert drawn == {"templates/components/option_cards.html": {"check"}}, drawn


def _sheets(*, bundles: bool) -> list[Path]:
    css = ROOT / "static" / "css"
    sheets = [p for p in css.rglob("*.css") if ("dist" in p.relative_to(css).parts) == bundles and "dev" not in p.relative_to(css).parts]
    if not bundles:
        sheets += list((ROOT / "apps").glob("*/static/**/*.css"))
    assert sheets
    return sorted(sheets)


@pytest.mark.parametrize("bundles", [False, True], ids=["sources", "bundles"])
def test_no_stylesheet_draws_a_check_for_a_state(bundles):
    found = {}
    for path in _sheets(bundles=bundles):
        hits = css_findings(path.read_text(encoding="utf-8"))
        if hits:
            found[path.relative_to(ROOT).as_posix()] = hits
    assert not found, found


def test_no_script_draws_a_check():
    js = ROOT / "static" / "js"
    found = {}
    for path in sorted(js.rglob("*.js")):
        parts = path.relative_to(js).parts
        if "dev" in parts or "vendor" in parts:
            continue
        hits = js_findings(path.read_text(encoding="utf-8"), names="dist" not in parts)
        if hits:
            found[path.relative_to(ROOT).as_posix()] = hits
    assert not found, found


#: The one producer that writes a check character, and why it may: the back-office's summary of a Forum event's
#: gates says whether a technical switch is open or shut, to staff, in the admin — not a state of a person, a piece
#: or a file, and no page of the product.
PYTHON_EXCEPTIONS = {"apps/forum/admin.py"}
#: The registry itself, and the list the dev showcase draws its icon sheet from, name every symbol.
PYTHON_REGISTRIES = {"apps/core/icons.py", "apps/core/dev.py"}


def test_no_python_producer_writes_a_check_into_the_page():
    found = {}
    for path in sorted((ROOT / "apps").rglob("*.py")):
        rel = path.relative_to(ROOT).as_posix()
        if "migrations" in path.parts or "tests" in path.parts or rel in PYTHON_REGISTRIES:
            continue
        hits = python_findings(path.read_text(encoding="utf-8"))
        if hits:
            found[rel] = hits
    assert set(found) == PYTHON_EXCEPTIONS, found


def test_the_registry_keeps_the_check_out_of_every_status_map():
    """The symbols a status context draws by variable come from these maps (REGISTRY_FED): none holds a check. The
    seal is the one entry that does, and it is an authority's act, drawn in its own element. The check-bearing set
    is the registry's — a new drawing of the stroke cannot enter the sprite unnamed."""
    assert CHECKS == set(icons.CHECK_BEARING), sorted(CHECKS ^ set(icons.CHECK_BEARING))
    for domain in ("status", "journey", "actor", "nav", "company_nav", "card", "due", "audience", "pathway"):
        for key, symbol in icons.DOMAINS[domain].items():
            if (domain, key) == ("status", "seal"):
                assert symbol == "badge-check"
                continue
            assert symbol not in CHECKS, f"{domain}.{key} draws {symbol}"
    for register in chips.REGISTERS:
        assert chips.mark_for(register) not in CHECKS
    assert all(mark not in CHECKS for mark in chips.MEMBER_MARK.values())
    assert "seal" not in chips.REGISTERS, "the seal is not a register: no chip is born with a check"
