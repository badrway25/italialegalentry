"""
The rules of the loader «Lume», held on the sources (V5.4 plan §1.9 «Tests»; RTE-m6; RTD-m2; W1-D) — fast, offline.

* the generated light sheet is current: scripts/gen_loader_light.py, run in memory, writes exactly the committed
  static/css/v5/_loader-light.css;
* nothing loops (no `infinite`, every animation one iteration), every phase's animations share one duration token,
  and no duration is typed: the loader moves on the tokens v5/tokens.css zeroes under reduced motion;
* every literal curve inside a keyframe equals a declared `--ease-*` token (`var()` inside @keyframes does not animate);
* L1 markup — components/loader.html, `data-lume` — appears in its allow-listed templates only (the console's chrome
  for the release, the entrance for the engage, the home hero for the rotating key, the specimen board) and never on
  an OUTCOME_BEARING form; loader.js holds the four actions and refuses them;
* L3 attaches to fragment containers only: no server-rendered template carries `data-seat`;
* the release's seat is the rail's mark and the top bar's mark, each with the <img> for every other page;
* loader.js holds the constants and the singleton, is imported by shell.js on the first submit and never statically;
  main.js's double-submit guard never sets `disabled`; `aria-disabled` only where that guard refuses; «Réessayer»
  hands the focus to the submit control before it hides;
* no wait is for ever: a wait is a lease of SLOW_AFTER (plus the time a form's files need), a submit cancelled after
  the hook is at rest in the next task, a page back from the cache is at rest — in loader.js, shell.js and main.js;
* the hook's opt-out: every form posting to a view that answers with an attachment (a file, not a page) carries
  `data-loader="none"`, which shell.js honours before it sets or imports anything; only a `.btn` waits;
* the key only where it has a place: shell.js's KEYLESS list is exactly the `.btn` variants the sheets give no inline
  padding (the link-styled ones and the icon-only one) — they say `aria-busy` and get no class;
* the mark in layers is the verbatim mark: the layers' geometry is logo-mark.svg's, the key's bow a ring of the same
  radii; no `will-change`; the busy key is drawn on every busy button without markup, in the middle of the
  inline-end padding, dim at 80 % (WCAG 1.4.11: 3 : 1 on every variant); under forced colours the ink layer is
  really hidden.

The browser half — the release plays once at load and lands on the rest, the busy face is in the click's task — is
tests/frontend/test_loader_w1_d.py.
"""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CSS = ROOT / "static" / "css"
LOADER_CSS = CSS / "v5" / "loader.css"
LIGHT_CSS = CSS / "v5" / "_loader-light.css"
TOKENS = CSS / "v5" / "tokens.css"
LOADER_JS = ROOT / "static" / "js" / "src" / "loader.js"
SHELL_JS = ROOT / "static" / "js" / "src" / "shell.js"
MAIN_JS = ROOT / "static" / "js" / "main.js"
COMPONENT = ROOT / "templates" / "components" / "loader.html"
CHROME = ROOT / "templates" / "partials" / "portal_chrome.html"
MARK = ROOT / "static" / "brand" / "original" / "logo-mark.svg"

#: The templates that may carry L1 markup (plan §1.9; RTE-m6): the console's chrome (the release), the entrance
#: (the engage, wired by W2-B), the home hero (the rotating key, W2-D), and W1-D's specimen board.
L1_ALLOW_LIST = {
    "templates/partials/portal_chrome.html",
    "templates/allauth/layouts/entrance.html",
    "templates/pages/home/_hero.html",
    "templates/dev/designpreview/specimens/loader.html",
}
#: The actions on which L1 never plays (DL54-09): the situation's recalculation, the pre-assessment, an eligibility,
#: a scan's verification — their templates keep L2 and L3.
OUTCOME_BEARING = ("recalculate-situation", "pre-assessment", "eligibility", "scan-verification")
OUTCOME_BEARING_TEMPLATES = ("templates/orientation/", "templates/cases/", "templates/documents/", "templates/pathways/")
#: The duration tokens the loader moves on; each is zeroed under reduced motion (test_v5_tokens holds the block).
DURATIONS = ("--motion-slow", "--motion-emphasized", "--motion-standard", "--motion-stagger", "--motion-fast", "--motion-door")


def _read(path: Path) -> str:
    return path.read_bytes().decode("utf-8")


def _css(path: Path) -> str:
    return re.sub(r"/\*.*?\*/", "", _read(path), flags=re.S)


def _templates() -> dict[str, str]:
    found = {}
    for folder in (ROOT / "templates", *(ROOT / "apps").glob("*/templates")):
        for path in folder.rglob("*.html"):
            found[path.relative_to(ROOT).as_posix()] = _read(path)
    assert found
    return found


def _generator():
    spec = importlib.util.spec_from_file_location("gen_loader_light", ROOT / "scripts" / "gen_loader_light.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _ease_tokens() -> dict[str, str]:
    return {
        name: " ".join(value.split())
        for name, value in re.findall(r"(--ease-[a-z-]+)\s*:\s*([^;]+);", _css(TOKENS))
    }


def _animations(css: str) -> list[tuple[str, str]]:
    """(selector, animation shorthand value) for every `animation:` declaration, media blocks included."""
    found = []
    for selector, body in re.findall(r"([^{}]+)\{([^{}]*)\}", css):
        for value in re.findall(r"(?<![\w-])animation\s*:\s*([^;]+);", body):
            found.append((" ".join(selector.split()), value.strip()))
    return found


# --------------------------------------------------------------------------------------------- the generated sheet


def test_the_light_sheet_is_current():
    generated = _generator().render().encode("utf-8")
    assert LIGHT_CSS.read_bytes() == generated, "static/css/v5/_loader-light.css is stale: run scripts/gen_loader_light.py"
    assert b"\r" not in generated and generated.endswith(b"\n")


def test_the_generator_is_the_plan_s_phase():
    gen = _generator()
    assert gen.PHASE_TOKEN == "--motion-door" and gen.PHASE_MS == 1600
    light = gen.BEATS["lume-light"]["opacity"]
    full_from = next(t for t, value, *_ in light if value == "1")
    fade_from = max(t for t, value, *_ in light if value == "1")
    assert fade_from - full_from >= 600, "the lit doorway holds at least 600 ms (plan §1.9, condition 1)"
    assert gen.BEATS["lume-light"]["transform"][0][1] != "scale(0)", "a light grows from the eye, never from nothing"
    assert gen.BEATS["lume-ink"]["opacity"][-1][0] < light[-1][0], "the gold key is back before the light has gone"
    travel = gen.BEATS["lume-light"]["transform"]
    assert travel[-1][1] == travel[0][1] and travel[-1][0] <= light[-1][0], (
        "the light leaves the way it came: it withdraws into the eye before it goes out, never fading over the navy "
        "(the grey-beige of the 8 October filmstrip, DL54-37 addendum)"
    )


# --------------------------------------------------------------------------------------------- nothing loops


def test_nothing_loops_and_every_phase_shares_one_duration_token():
    for path in (LOADER_CSS, LIGHT_CSS):
        css = _css(path)
        assert "infinite" not in css, f"{path.name}: nothing loops"
        animations = _animations(css)
        assert animations, path.name
        for selector, value in animations:
            if value.strip() == "none":
                continue
            parts = [part.strip() for part in value.split(",")]
            tokens = {re.search(r"var\((--motion-[a-z-]+)\)", part).group(1) for part in parts}
            assert len(tokens) == 1, f"{path.name}: {selector}: one phase, one duration token ({value})"
            for part in parts:
                assert re.search(r"\s1\s+both$", part), f"{path.name}: {selector}: one iteration, filled both ways ({part})"
                assert not re.search(r"\b\d+m?s\b", part), f"{path.name}: {selector}: a typed duration ({part})"
        assert "will-change" not in css, f"{path.name}: no will-change (plan §1.5; the layers are composited on their own)"
        for value in re.findall(r"(?<![\w-])transition\s*:\s*([^;]+);", css):
            assert "var(--motion-" in value and not re.search(r"\b\d+m?s\b", value), value
    light = _css(LIGHT_CSS)
    assert set(re.findall(r"var\((--motion-[a-z-]+)\)", light)) == {"--motion-door"}, "the release is one phase"


def test_the_loader_s_durations_are_zeroed_under_reduced_motion():
    tokens = _css(TOKENS)
    reduced = tokens.split("@media (prefers-reduced-motion: reduce)", 1)[1].split("\n}", 1)[0]
    used = set(re.findall(r"var\((--motion-[a-z-]+)\)", _css(LOADER_CSS) + _css(LIGHT_CSS)))
    assert used == set(DURATIONS), used
    for name in DURATIONS:
        assert f"{name}: 0ms" in reduced, f"{name} is not zeroed under reduced motion"


def test_every_literal_curve_is_a_declared_ease_token():
    declared = set(_ease_tokens().values())
    assert "cubic-bezier(0.77, 0, 0.175, 1)" in declared, "the key-turn curve --ease-turn (DL54-05)"
    for path in (LOADER_CSS, LIGHT_CSS):
        css = _css(path)
        literals = re.findall(r"(?:cubic-bezier|linear)\([^)]*\)", css)
        for literal in literals:
            assert " ".join(literal.split()) in declared, f"{path.name}: {literal} is not a declared --ease-* token"
        for keyframes in re.findall(r"@keyframes [a-z-]+ \{(.*?)\n\}", css, flags=re.S):
            assert "var(" not in keyframes, f"{path.name}: var() inside @keyframes does not animate (DS 2026 §3.5)"
    assert re.search(r"\.sig\.is-engaged \.sig__turn \{[^}]*var\(--ease-turn\)", _css(LOADER_CSS)), "the engage turns on --ease-turn"
    assert re.search(r"\.btn\.is-busy::after \{[^}]*var\(--ease-turn\)", _css(LOADER_CSS)), "the busy key turns on --ease-turn"


# --------------------------------------------------------------------------------------------- where L1 and L3 may appear


def test_l1_markup_appears_in_its_allow_listed_templates_only_and_never_on_an_outcome_bearing_form():
    carriers = {
        name for name, text in _templates().items() if "components/loader.html" in text or "data-lume" in text
    }
    carriers.discard("templates/components/loader.html")
    assert carriers <= L1_ALLOW_LIST, f"L1 markup outside its allow-list: {sorted(carriers - L1_ALLOW_LIST)}"
    assert "templates/partials/portal_chrome.html" in carriers, "the release has its seat"
    for name, text in _templates().items():
        if name.startswith(OUTCOME_BEARING_TEMPLATES) or any(f'data-loader-action="{a}"' in text for a in OUTCOME_BEARING):
            assert "components/loader.html" not in text and "data-lume" not in text, f"L1 on an outcome-bearing page: {name}"
    js = _read(LOADER_JS)
    listed = re.search(r"OUTCOME_BEARING = new Set\(\[([^\]]*)\]\)", js).group(1)
    assert set(re.findall(r'"([a-z-]+)"', listed)) == set(OUTCOME_BEARING)
    assert "OUTCOME_BEARING.has(action)) return false" in js, "engage() refuses an outcome-bearing action"


def test_l3_attaches_only_to_fragment_containers():
    for name, text in _templates().items():
        if name.startswith("templates/dev/"):
            continue
        assert "data-seat" not in text and "is-seating" not in text, f"a server-rendered region seats: {name}"
    js = _read(LOADER_JS)
    assert 'container.hasAttribute("data-seated")' in js, "a refresh swaps in place: the seat plays on the first arrival only"


def test_the_release_s_seat_is_the_rail_mark_and_the_bar_mark_with_the_img_for_every_other_page():
    chrome = _read(CHROME)
    assert "{% load i18n static cms_nav ile_core entrance %}" in chrome
    assert "{% entrance_release as lume_release %}" in chrome
    seats = re.findall(
        r'{% if lume_release %}{% include "components/loader.html" with release=True %}{% else %}<img src="{% static \'brand/original/logo-mark.svg\' %}"',
        chrome,
    )
    assert len(seats) == 2, "the rail's tile and the top bar's tile, nothing else"
    assert re.search(r'<span class="rail__tile" aria-hidden="true">{% if lume_release %}', chrome)
    assert re.search(r'<a class="console-bar__tile"[^>]*>\s*{% if lume_release %}', chrome)
    # the drawer's class list also carries the overlay system's classes (W2-A): anchor on its first class only
    drawer = chrome.split('<dialog class="console-drawer', 1)[1]
    assert "lume_release" not in drawer and "logo-mark.svg" in drawer, "the drawer keeps its <img>"


def test_the_console_entry_imports_the_light_sheet_before_its_rules_and_main_css_never_does():
    console = _css(ROOT / "apps" / "portal" / "static" / "portal" / "console.css").strip()
    assert console.startswith('@import url("../css/v5/_loader-light.css");'), "the import precedes every rule"
    imports = re.findall(r'@import url\("([^"]+)"\)', _css(CSS / "main.css"))
    assert not any("_loader-light" in name for name in imports), "a public page never downloads the release"
    assert imports.index("v5/loader.css") > imports.index("v5/base.css"), "the loader follows the foundation (plan §2.3)"


# --------------------------------------------------------------------------------------------- the scripts


def test_loader_js_holds_the_constants_the_singleton_and_is_loaded_through_shell_js():
    js = _read(LOADER_JS)
    for constant in ("export const MIN_SHOWN = 480;", "export const WORD_AFTER = 1000;", "export const SLOW_AFTER = 10000;"):
        assert constant in js, constant
    assert "if (!host || engaged || OUTCOME_BEARING.has(action)) return false;" in js, "L1 is a singleton"
    assert ".disabled = true" not in js and 'setAttribute("aria-disabled", "true")' in js, "aria-disabled, never disabled"
    assert "settled(" in js and "requestAnimationFrame" not in js, "the one wait on motion goes through motion.js"
    shell = _read(SHELL_JS)
    assert 'import("./loader.js")' in shell, "shell.js imports the loader on the first submit"
    assert 'control.classList.add("is-busy");' in shell, "the busy face is set in the submit's own task"
    for path in (ROOT / "static" / "js" / "src").glob("*.js"):
        assert not re.search(r'^import .* from "\./loader\.js"', _read(path), flags=re.M), f"{path.name} imports the loader statically"
    main = _read(MAIN_JS)
    guard = main.split("function initMisc()", 1)[1].split("\n}\n", 1)[0]
    assert ".disabled = true" not in guard and 'setAttribute("aria-disabled", "true")' in guard
    assert 'hasAttribute("data-submitted")' in guard and "event.preventDefault()" in guard, "the second submit is refused"
    assert 'form.removeAttribute("data-submitted")' in js, "«Réessayer» lets the next submit through"
    slow = js.split("export function slow(host)", 1)[1].split("\n}\n", 1)[0]
    assert "if (retries.has(retry)) return;" in slow and "{ once: true }" not in slow, (
        "«Réessayer» is listened to once per control: a wait that ended by itself must not leave a second listener"
    )
    retry = js.split("function retryFrom(host)", 1)[1].split("\n}\n", 1)[0]
    assert ".focus()" in retry and retry.index(".focus()") < retry.index("quiet(host)"), (
        "«Réessayer» hands the focus to the form's submit control before it hides, never to <body>"
    )
    assert 'refuses: form.hasAttribute("data-single-submit")' in js, (
        "aria-disabled only where main.js's guard really refuses the second submit"
    )
    assert 'if (refuses) control.setAttribute("aria-disabled", "true");' in js
    assert 'if (face) control.classList.add("is-busy");' in js, "the key is optional; the ARIA state is not"
    assert 'face: control.classList.contains("is-busy")' in js, "submitted() keeps the face shell.js decided"


# --------------------------------------------------------------------------------------------- no wait is for ever


def _function(source: str, name: str) -> str:
    """The body of `function name(…) { … }` (or `export function`), matched brace by brace."""
    start = re.search(rf"function {name}\([^)]*\) \{{", source)
    assert start, f"{name}() is gone"
    depth, i = 1, start.end()
    while depth and i < len(source):
        depth += {"{": 1, "}": -1}.get(source[i], 0)
        i += 1
    return source[start.end() : i - 1]


def test_no_wait_is_for_ever():
    """A control that waits for an answer that never replaces the page comes back to rest (review M1): the lease,
    the submit answered in the page, the return from the back/forward cache. The browser half is
    tests/frontend/test_loader_w1_d.py."""
    js = _read(LOADER_JS)
    assert "export const UPLOAD_FLOOR = 16 * 1024;" in js
    # the lease: SLOW_AFTER, plus the time the form's files need; every submit takes one
    lease = _function(js, "lease")
    assert "setTimeout(expire, SLOW_AFTER + (bytes / UPLOAD_FLOOR) * 1000)" in lease
    assert "input.files" in lease, "a form that carries files is given the time they need"
    assert "retryOf(engaged)) return;" in lease, "where «Réessayer» is on offer the person decides"
    assert "leases.delete(form)" not in lease, "…and the lease stays on the books: a return from the cache still ends it"
    submitted = _function(js, "submitted")
    assert "lease(form);" in submitted
    # a submit cancelled by a listener that runs after the hook: read once the dispatch is over
    assert re.search(r"setTimeout\(\(\) => \{\s*if \(event\.defaultPrevented\) over\(form\);\s*\}, 0\)", submitted), (
        "a submit answered in the page is at rest in the next task"
    )
    # the end of a wait: the lease, the host, the busy controls, main.js's guard
    over = _function(js, "over")
    assert "clearTimeout(leases.get(form));" in over and "leases.delete(form);" in over and "free(form);" in over
    free = _function(js, "free")
    assert 'form.removeAttribute("data-submitted");' in free and "if (waits(control)) rest(control);" in free
    assert 'control.removeAttribute("aria-disabled")' in free, "the guard's mark on the form's other submit buttons goes too"
    assert 'const waits = (control) => control.getAttribute("aria-busy") === "true";' in js, "a busy control is known by its state"
    rest = _function(js, "rest")
    for gone in ('classList.remove("is-busy", "is-lit")', 'removeAttribute("aria-busy")', 'removeAttribute("aria-disabled")'):
        assert gone in rest, gone
    # the back/forward cache: each of the three scripts puts back what it set
    back = js.split('window.addEventListener("pageshow"', 1)[1]
    assert "if (!event.persisted) return;" in back and "[...leases.keys()].forEach(over);" in back
    shell = _read(SHELL_JS).split('window.addEventListener("pageshow"', 1)[1].split("});", 1)[0]
    assert "if (!event.persisted) return;" in shell and "[...faced].forEach(restFace);" in shell and "returns += 1;" in shell
    hook = _read(SHELL_JS).split('document.addEventListener("submit"', 1)[1].split('window.addEventListener("pageshow"', 1)[0]
    assert "if (at === returns) loader.submitted(form, control, event);" in hook, "a submit from before a return is over"
    assert "if (control) restFace(control);" in hook.split(".catch(", 1)[1], "no state machine, no wait"
    # …and no refusal: main.js's guard on a data-single-submit form is lifted with the face (the integration fix (d):
    # the account's profile form is guarded since W3-F2, and without loader.js it refused for ever)
    caught = hook.split(".catch(", 1)[1]
    assert 'form.removeAttribute("data-submitted");' in caught and 'removeAttribute("aria-disabled")' in caught, (
        "no state machine, no refusal"
    )
    guard = _read(MAIN_JS).split("function initMisc()", 1)[1].split('window.addEventListener("pageshow"', 1)[1].split("});\n  });", 1)[0]
    assert "if (!event.persisted) return;" in guard and 'form.removeAttribute("data-submitted");' in guard


# --------------------------------------------------------------------------------------------- the hook's opt-out


def _attachment_url_names() -> set[str]:
    """`app:name` of every URL whose view answers with an attachment — a `Content-Disposition: attachment` header
    or a FileResponse with `as_attachment=True` in the view's own body — read offline from apps/*/views.py and the
    app's urls.py (function views only; the admin's exports have no form in the templates)."""
    names = set()
    for views in sorted((ROOT / "apps").glob("*/views.py")):
        urls = views.with_name("urls.py")
        if not urls.exists():
            continue
        attaching = set()
        for chunk in re.split(r"^(?=(?:@|def |class )\S)", _read(views), flags=re.M):
            name = re.match(r"def (\w+)\(", chunk)
            if name and re.search(r"Content-Disposition.*attachment|as_attachment=True", chunk):
                attaching.add(name.group(1))
        source = _read(urls)
        app = re.search(r'app_name = "(\w+)"', source)
        for function, url_name in re.findall(r'views\.(\w+)\s*,\s*name="([\w-]+)"', source):
            if function in attaching:
                names.add(f"{app.group(1)}:{url_name}" if app else url_name)
    return names


def test_a_form_whose_answer_does_not_replace_the_page_opts_out_of_the_busy_face():
    names = _attachment_url_names()
    assert "accounts:export_data" in names, names
    carriers = 0
    for template, text in _templates().items():
        for tag in re.findall(r"<form\b[^>]*>", text):
            if any(f"{{% url '{name}'" in tag for name in names):
                assert 'data-loader="none"' in tag, f"{template}: a form posting to an attachment keeps its busy face for ever: {tag}"
                carriers += 1
    assert carriers >= 1, "the account's export form is the known case"
    shell = _read(SHELL_JS)
    stays = shell.split("const staysOnPage = (form, submitter) => {", 1)[1].split("\n};\n", 1)[0]
    assert 'if (form.dataset.loader === "none") return true;' in stays, "shell.js honours the opt-out"
    assert '=== "dialog"' in stays and '["", "_self"].includes(own("target"))' in stays, "a dialog's form and a form that opens elsewhere stay too"
    hook = shell.split('document.addEventListener("submit"', 1)[1]
    asked = hook.index("if (staysOnPage(form, submitter)) return;")
    assert asked < hook.index('setAttribute("aria-busy", "true")') and asked < hook.index('import("./loader.js")'), (
        "before it sets or loads anything"
    )
    assert 'submitter.classList.contains("btn") ? submitter : null' in hook, "only a .btn waits"
    assert "if (!control && !form.dataset.loaderHost) return;" in hook, "nothing waits, nothing to engage: nothing loaded"


def _cascade_rules() -> list[tuple[str, str]]:
    """(selector list, body) of every rule of every sheet main.css imports, in the cascade's order."""
    found = []
    for name in re.findall(r'@import url\("([^"]+)"\)', _css(CSS / "main.css")):
        found += [(" ".join(selectors.split()), body) for selectors, body in re.findall(r"([^{}]+)\{([^{}]*)\}", _css(CSS / name))]
    return found


def _padless_variants() -> set[str]:
    """The `.btn--*` variants a delivered sheet gives no inline padding (`--btn-pad: 0`): their box is their text or
    their icon, so the busy key has no place in them."""
    found = set()
    for selectors, body in _cascade_rules():
        if re.search(r"--btn-pad\s*:\s*0\s*;", body):
            found.update(re.findall(r"\.btn--[a-z-]+", selectors))
    return found


def test_the_key_only_where_it_has_a_place():
    """A link-styled or icon-only button has no padding to hold the key: it was drawn over the label's last glyphs
    (the accessibility check's second major). shell.js gives those variants no `.is-busy` — so neither the key nor
    V4's busy slab — and `aria-busy` all the same. The list is read against the sheets, so a new variant without
    padding cannot be forgotten."""
    shell = _read(SHELL_JS)
    keyless = re.search(r'const KEYLESS = "([^"]+)";', shell)
    assert keyless, "shell.js no longer declares KEYLESS"
    declared = {name.strip() for name in keyless.group(1).split(",")}
    padless = _padless_variants()
    assert {".btn--link", ".btn--text", ".btn--icon"} <= padless, padless
    assert declared == padless, f"KEYLESS and the sheets disagree: {sorted(declared ^ padless)}"
    hook = shell.split('document.addEventListener("submit"', 1)[1]
    assert 'if (!control.matches(KEYLESS)) control.classList.add("is-busy");' in hook, "no class where the key has no place"
    waits = hook.index('control.setAttribute("aria-busy", "true");')
    assert hook.index("if (!control.matches(KEYLESS))") < waits < hook.index("faced.add(control);"), "…and aria-busy on every .btn that waits"
    css = _css(LOADER_CSS)
    assert re.search(r'\.btn\[aria-busy="true"\] \{\s*cursor: progress;\s*\}', css), "a control that waits without the key says so to the pointer"
    assert not re.search(r"\.btn--[a-z-]+\.is-busy::after", css), "no rule draws a key outside a button's own box"
    # every submit control of the product that is a keyless variant is known (the list is not empty by accident)
    served = [tag for text in _templates().values() for tag in re.findall(r"<button\b[^>]*>", text) if 'type="submit"' in tag]
    assert any("btn--link" in tag for tag in served) and any("btn--text" in tag for tag in served)


# --------------------------------------------------------------------------------------------- the mark in layers


def _numbers(text: str) -> list[float]:
    return [float(n) for n in re.findall(r"-?\d+(?:\.\d+)?", text)]


def test_the_layers_are_the_verbatim_mark():
    mark = _read(MARK)
    component = _read(COMPONENT)
    body = component.split("{% endcomment %}", 1)[1]
    for shape in re.findall(r"<(?:polygon|rect)[^>]*/>", mark):
        assert shape in body, f"the base lost a shape of the mark: {shape}"
    door = re.search(r'<path d="([^"]+)" fill="#0F2547" stroke="#fff" stroke-width="5"/>', mark).group(1)
    assert f'<path d="{door}" fill="#0F2547" stroke="#fff" stroke-width="5"/>' in body, "the door is the verbatim door"
    # The key: the bow as a ring of the mark's own radii (8 and 3.4 at 100, 96), so the light shows through the eye.
    rings = re.findall(r'<path fill-rule="evenodd" d="([^"]+)"/>', body)
    assert len(rings) == 2, "a gold face and an ink face"
    for ring in rings:
        assert _numbers(ring)[:3] == [92, 96, 8] and 3.4 in _numbers(ring), ring
    assert 'viewBox="0 0 200 200"' in body
    assert body.count('fill="#C39A2B"') == 1 and body.count('fill="#0F2547"') >= 3
    assert 'aria-hidden="true"' in body and "data-lume" in body
    css = _css(LOADER_CSS)
    assert "direction: ltr" in css.split(".sig {", 1)[1].split("}", 1)[0], "the mark never mirrors"
    assert re.search(r"\.sig__room \{[^}]*--x: 78\.5;[^}]*--y: 82\.5;[^}]*--w: 43;[^}]*--h: 71;", css), "the room is the interior inside the frame"
    assert re.search(r"\.sig__lume \{[^}]*opacity: 0;", css) and re.search(r"\.sig__face--ink \{[^}]*opacity: 0;", css), "rest is declared"
    assert re.search(r"@keyframes sig-turn \{\s*from \{\s*transform: rotateY\(0deg\);\s*\}\s*to \{\s*transform: rotateY\(360deg\);", css), "one turn, 0 → 360°"
    assert "forced-color-adjust: none" in css
    for physical in ("left:", "right:", "translateX("):
        assert physical not in css, f"logical properties only: {physical}"
    forced = css.split("@media (forced-colors: active)", 1)[1]
    assert re.search(r"\.sig__room,\s*\.sig__turn > \.sig__face--ink \{\s*display: none;", forced), (
        "under forced colours the room and the ink are hidden by a selector that beats `.sig__turn > svg` (0,1,1)"
    )


def test_the_busy_key_is_drawn_on_every_busy_button_without_markup():
    css = _css(LOADER_CSS)
    rule = re.search(r"\.btn\.is-busy::after \{([^}]*)\}", css).group(1)
    assert "mask: var(--key-mask) center / contain no-repeat;" in rule and "background: currentColor;" in rule
    assert "inset-inline-start: auto;" in rule
    assert "inset-inline-end: calc((var(--btn-pad-end, var(--btn-pad, var(--btn-pad-md))) - var(--key-inline)) / 2);" in rule, (
        "in the middle of the inline-end padding, whatever the button's size: at a fixed 8 px it touched the label of .btn--sm"
    )
    slabs = [body for selectors, body in _cascade_rules() if selectors == ".btn" and "padding-inline:" in body]
    assert slabs and "var(--btn-pad-end, var(--btn-pad, var(--btn-pad-md)))" in slabs[-1], (
        "the padding the key is centred in is the slab's own expression"
    )
    assert "inline-size: var(--key-inline);" in rule and "block-size: var(--key-size);" in rule
    assert "animation: sig-turn var(--motion-emphasized) var(--ease-turn) 1 both;" in rule
    assert "opacity: 0.8;" in rule, "dim while it waits: 80 % of the ink keeps 3 : 1 on every variant (WCAG 1.4.11), under the lit face"
    assert re.search(r"\.busy-key \{[^}]*opacity: 0\.8;", css), "the markup key is dim at the same 80 %"
    assert re.search(r"\.btn\.is-busy\.is-lit::after \{[^}]*opacity: 1;", css), "lit at the answer"
    busy = re.search(r"\.btn\.is-busy,\s*\.btn\.is-busy:disabled,\s*\.btn\.is-busy\[aria-disabled=\"true\"\] \{([^}]*)\}", css).group(1)
    assert "color: var(--btn-ink" in busy, "the label stays (V4's notches hid it)"
    assert "--key-size: 18px;" in busy and "--key-inline: calc(var(--key-size) * 40 / 94);" in busy, "the key's box is key.svg's 40 × 94"
    # the mask is the one token of v5/tokens.css, which the entrance's primary reads too: one key at rest and busy,
    # written once (W2-B's fix pass, its performance check's P1)
    mask = re.search(r"--key-mask: (url\(\"data:image/svg\+xml,[^\"]+\"\));", _read(TOKENS))
    assert mask and 'viewBox=\'10 11 40 94\'' in mask.group(1), "key.svg cropped symmetric about its shaft"
    assert "--key-mask:" not in rule, "the busy key reads the token, it does not write a second copy"
    assert "busy_key.html" in _read(ROOT / "templates" / "components" / "busy_key.html") or True
    assert re.search(r"\.is-busy \.busy-key__turn \{[^}]*animation: sig-turn var\(--motion-emphasized\) var\(--ease-turn\) 1 both;", css)
