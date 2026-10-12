"""
The entrance «Il varco» — the stage (V5.4 plan §1.13 «Le vie convergono al varco», §1.9 the engage; W2-B, step 1).

On the sources and with Django's client (fast, offline):
* every entrance page — login, signup, password reset and its answers, verification — is served on the layout with
  ONE stage: the owner's door stage as drawn (the photograph, the vector parts, the verbatim key as an HTML layer),
  the four ways in the audience order, the help line; the stage is decorative and never a text carrier;
* the door stage is the loader's L1 host: `door-stage sig` with the id the sign-in's forms name in
  `data-loader-host` — the login and the second factor's code, no other form — and the entrance's form element is the
  product's form element plus that one attribute;
* in the source the focus precedes the stage: after the skip link the next stop is in the form, and the help line's
  address comes after the form's action; the sheet places the two on grid lines and holds the stage's place — its
  column, the band's row — before the stage is parsed, and inside the stage the help line precedes the scene and the
  door the floor;
* the sheets: the entrance imports the door partial and the niche's paints; nothing loops, every animation is one iteration on duration
  tokens with no typed duration and no fill that stays in effect, the keyframes hold no `var()` and move transform
  and opacity only, no `will-change`; the scene and the door are `direction: ltr`; the keyboard rule zeroes the
  transitions; under forced colours no light layer is displayed; the pool at rest is 12 % at most;
* the colours the sheets read are one named block of v5/tokens.css — the door's literals and the five colours the
  stage adds — and nowhere else a literal colour; the stage's gradients are composed from them in the page-only
  partial static/css/v5/_varco.css, which the entrance imports after the door: main.css carries no paint of this page;
* the script writes classes only — no style, no frame loop, no text — asks motion.js's gate, and every state it
  writes is drawn by the sheet; the V1 block name `.entrance` no longer reaches the layout.

In Chromium (``-m browser``):
* the rest: no state, nothing running once the arrival has been said; the arrival runs once after the door is
  painted and is cut by a focus; under the emulated setting there is none and every state is there at once;
* a pointer's focus on the e-mail lights the ways with one pass and leaves nothing running; a valid address holds the
  threshold at the typing pause; a pointer's focus on the password lights the frame; clearing gives the state back;
  from the keyboard the same states arrive with no pass and no running transition;
* on the sign-in's submit the stage's key turns once and holds, with the form's button busy; another entrance form
  engages nothing;
* a refused sign-in's page loads at rest with the kept address's still, and no arrival;
* below 64rem the stage is a band, the floor is not drawn and the frame answers the e-mail field; at 360 × 640 the
  form's action is in the first viewport; under forced colours the lights are not displayed;
* nothing moves when the stage arrives: the form's box is the same without the stage in the document, the help
  line's without the scene (a slow browser paints before the whole page is parsed), and the stage's place is the
  night before the stage is there;
* a password's show / hide control asks for the frame as the field does.
The Arabic page is tests/i18n/test_rtl_browser_entrance.py.
"""

from __future__ import annotations

import os
import re
from pathlib import Path

import pytest

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

ROOT = Path(__file__).resolve().parents[2]
LAYOUT = ROOT / "templates" / "allauth" / "layouts" / "entrance.html"
FORM_ELEMENT = ROOT / "templates" / "allauth" / "elements" / "form.html"
ENTRANCE_FORM = ROOT / "templates" / "allauth" / "elements" / "form__entrance.html"
SHEET = ROOT / "apps" / "accounts" / "static" / "accounts" / "entrance.css"
DOOR = ROOT / "static" / "css" / "v5" / "_door.css"
VARCO = ROOT / "static" / "css" / "v5" / "_varco.css"
TOKENS = ROOT / "static" / "css" / "v5" / "tokens.css"
SCRIPT = ROOT / "static" / "js" / "src" / "entrance.js"
KEY = ROOT / "static" / "brand" / "original" / "key.svg"

HOST = "varco-door"
STATES = ("is-ways", "is-held", "is-frame")
WAYS = ("is-passing-ways", "is-passing-frame", "is-arriving", "is-still")
AUDIENCES = ["persona", "impresa", "istituzione", "universita"]
#: Entrance pages an anonymous visitor reaches (the signup shows its form or its gated message, by the gates).
PAGES = {
    "login": "/{lang}/compte/login/",
    "signup": "/{lang}/compte/signup/",
    "reset": "/{lang}/compte/password/reset/",
    "reset-done": "/{lang}/compte/password/reset/done/",
    "verification-sent": "/{lang}/compte/confirm-email/",
    "inactive": "/{lang}/compte/inactive/",
    "bad-confirmation": "/{lang}/compte/confirm-email/not-a-key/",
    "bad-reset-key": "/{lang}/compte/password/reset/key/1-not-a-key/",
}


def _read(path: Path) -> str:
    return path.read_bytes().decode("utf-8")


def _css(path: Path) -> str:
    return re.sub(r"/\*.*?\*/", "", _read(path), flags=re.S)


def _body(template: Path) -> str:
    """A template without its {% comment %} blocks."""
    return re.sub(r"\{% comment %\}.*?\{% endcomment %\}", "", _read(template), flags=re.S)


def _rules(css: str) -> list[tuple[str, str]]:
    return [(" ".join(selector.split()), body) for selector, body in re.findall(r"([^{}]+)\{([^{}]*)\}", css)]


def _media(css: str, query: str) -> tuple[str, str]:
    """The inside of every block `@media <query> {` of a sheet (braces counted), and the sheet without them."""
    inside, outside, last = [], [], 0
    for match in re.finditer(re.escape(f"@media {query}") + r"\s*\{", css):
        depth, at = 1, match.end()
        while depth:
            depth += {"{": 1, "}": -1}.get(css[at], 0)
            at += 1
        inside.append(css[match.end() : at - 1])
        outside.append(css[last : match.start()])
        last = at
    return "\n".join(inside), "".join(outside) + css[last:]


def _keyframes(css: str) -> dict[str, str]:
    found = {}
    for match in re.finditer(r"@keyframes ([a-z-]+)\s*\{", css):
        depth, i = 1, match.end()
        while depth and i < len(css):
            depth += {"{": 1, "}": -1}.get(css[i], 0)
            i += 1
        found[match.group(1)] = css[match.end() : i - 1]
    return found


# --------------------------------------------------------------------------------------------- the pages


@pytest.mark.django_db
@pytest.mark.parametrize("lang", ["fr", "ar", "it", "en"])
def test_every_entrance_page_is_served_on_the_stage(client, seeded, lang):
    for name, path in PAGES.items():
        response = client.get(path.format(lang=lang))
        html = response.content.decode()
        assert response.status_code == 200, (name, lang, response.status_code)
        assert html.count("data-varco-stage") == 1, (name, lang)
        assert html.count(f'id="{HOST}"') == 1, (name, lang)
        assert 'class="account-page account-page--entrance varco"' in html, (name, lang)
        assert html.count("<h1") == 1, (name, lang)
        assert "css/dist/accounts/entrance.css" in html and "js/dist/entrance.js" in html, (name, lang)
        assert re.findall(r'data-way="([a-z]+)"', html) == AUDIENCES, (name, lang)
        assert "mailto:contact@agamieuromed.org" in html.split("varco__colophon", 1)[1], (name, lang)


@pytest.mark.django_db
def test_the_sign_in_s_forms_name_the_stage_and_no_other_form_does(client, seeded):
    login = client.get("/fr/compte/login/").content.decode()
    form = re.search(r'<form class="form"[^>]*action="/fr/compte/login/"[^>]*>', login)
    assert form and f'data-loader-host="{HOST}"' in form.group(0), "the login's form names the stage"
    assert "novalidate" in form.group(0) and "data-single-submit" in form.group(0), "…and is the product's form"
    for name in ("signup", "reset"):
        html = client.get(PAGES[name].format(lang="fr")).content.decode()
        assert "data-loader-host" not in html, f"{name}: only a sign-in engages the stage"


def test_the_entrance_s_form_element_is_the_product_s_form_plus_the_host():
    """allauth renders `form__entrance.html` before `form.html` on the entrance layout: the two must stay one form."""
    base = " ".join(_body(FORM_ELEMENT).split())
    entrance = _body(ENTRANCE_FORM)
    host = (
        '{% if not attrs.no_visible_fields %}{% if "login" in attrs.tags or origin == "mfa/authenticate" %}'
        f' data-loader-host="{HOST}"' + "{% endif %}{% endif %}"
    )
    assert entrance.count(host) == 1, "the sign-in's forms — the login, the second factor's code — name the stage"
    assert " ".join(entrance.replace(host, "").split()) == base, "form__entrance.html drifted from form.html"


@pytest.mark.django_db
def test_the_focus_precedes_the_stage_in_the_source(client, seeded):
    html = client.get("/fr/compte/login/").content.decode()
    main = html.split('<main id="main-content"', 1)[1].split("</main>", 1)[0]
    assert main.index('class="varco__focus"') < main.index("data-varco-stage"), "the form first, for the keyboard"
    assert main.index('type="submit"') < main.index("mailto:"), "the help line's address follows the form's action"
    # …and the sheet PLACES the two, with the stage's place held before the stage is parsed: its row below 64rem (the
    # band's own height, from the door's width), its column from 64rem. Never `order`: an item placed by the order of
    # the source moves when the other one arrives (0.446 of layout shift at CPU ×4, measured before this rule).
    sheet = _css(SHEET)
    rules = _rules(sheet)
    assert re.search(
        r"\.varco \{[^}]*grid-template-rows: minmax\(max\(var\(--varco-band-min\), calc\(var\(--door-w\) \* 456 / 368 \+ 2 \* var\(--varco-band-pad\)\)\), auto\) auto;",
        sheet,
    ), "the band's row is reserved at the band's own height"
    assert any(selector == ".varco__stage" and "grid-row: 1;" in body for selector, body in rules)
    assert any(selector == ".varco__focus" and "grid-row: 2;" in body for selector, body in rules)
    assert any(selector == ".varco__stage" and "grid-column: 1;" in body for selector, body in rules)
    assert any(selector == ".varco__focus" and "grid-column: 2;" in body and "grid-row: 1;" in body for selector, body in rules)
    assert not re.search(r"(?<![\w-])order\s*:", sheet), "placed on grid lines, not by `order`"
    # the ground of the stage's place is the page's own box's, there from the first frame: the night, in the stage's
    # cell. Every part therefore names its cell IN FULL in its first rule — column and row, below 64rem too: a part
    # left to auto-placement steps aside from the ground into a column of its own (seen at 390 px: a 242 px sheet).
    first = {}
    for selector, body in rules:
        first.setdefault(selector, body)
    ground = first[".varco::before"]
    assert "grid-column: 1;" in ground and "grid-row: 1;" in ground and "background-color: var(--surface-night);" in ground, ground
    assert "grid-column: 1;" in first[".varco__stage"] and "grid-row: 1;" in first[".varco__stage"], first[".varco__stage"]
    assert "grid-column: 1;" in first[".varco__focus"] and "grid-row: 2;" in first[".varco__focus"], first[".varco__focus"]
    # inside the stage too: the help line is written before the scene, the door before the floor that hangs from it
    stage = main.split("data-varco-stage", 1)[1]
    assert stage.index('class="varco__colophon"') < stage.index('class="varco__scene"')
    assert stage.index('id="varco-door"') < stage.index('class="varco__floor"')
    assert any(selector == ".varco__set" and "grid-template-columns: var(--door-w) minmax(0, 1fr);" in body for selector, body in rules), (
        "the band's door column is the door's width before the door is there"
    )


# --------------------------------------------------------------------------------------------- the stage's markup


def test_the_stage_is_the_door_as_drawn_and_the_loader_s_host():
    body = _body(LAYOUT)
    stage = body.split('<div class="varco__stage chapter--dark" data-varco-stage>', 1)[1]
    host = re.search(r'<div class="door-stage sig varco__door" id="varco-door" aria-hidden="true">', stage)
    assert host, "the door stage is the L1 host: door-stage + sig, with the id the forms name, decorative"
    door = stage[host.end() :]
    # the door as drawn: the arch, the inner door, the three steps, the outline, in stage units
    assert 'viewBox="264 64 368 456"' in door
    for shape in (
        '<path class="doorway__arch-inset" d="M304 507V240a144 144 0 0 1 288 0v267"/>',
        '<path class="doorway__inner" d="M365 397V222a83 83 0 0 1 166 0v175z"/>',
        '<rect x="342.5" y="477" width="211" height="6" rx="2"/>',
        '<rect x="320" y="486" width="256" height="6" rx="2"/>',
        '<rect x="297.5" y="495" width="301" height="6" rx="2"/>',
        '<path class="doorway__arch" d="M288 507V240a160 160 0 0 1 320 0v267"/>',
    ):
        assert shape in door, shape
    # the photograph: the owner's, the home's derivatives (static/brand/v5, AVIF and WebP, 400 to 1200 px) in a
    # <picture> the browser can prioritise and never announces; the page preloads the AVIF set with the same sizes,
    # character for character, so the one file the picture chooses is the one fetched (review M1, the check's F1)
    photo = re.search(r'<picture class="door-stage__photo">(.*?)</picture>', door, re.S)
    assert photo, "the photograph is a <picture> in the arch's box"
    avif = re.search(r'<source type="image/avif" srcset="([^"]+)" sizes="([^"]+)">', photo.group(1))
    webp = re.search(r'<source type="image/webp" srcset="([^"]+)" sizes="([^"]+)">', photo.group(1))
    img = re.search(r"<img ([^>]*)>", photo.group(1))
    assert avif and webp and img, photo.group(1)
    widths = re.findall(r"brand/v5/doorway-arch-(\d+)\.avif' %\} (\d+)w", avif.group(1))
    assert widths == [(w, w) for w in ("400", "576", "800", "960", "1200")], widths
    widths = re.findall(r"brand/v5/doorway-arch-(\d+)\.webp' %\} (\d+)w", webp.group(1))
    assert widths == [(w, w) for w in ("400", "576", "800", "960")], widths
    assert avif.group(2) == webp.group(2), "one sizes for the two sources"
    assert 'alt=""' in img.group(1) and 'fetchpriority="high"' in img.group(1) and 'decoding="async"' in img.group(1)
    assert 'width="400" height="533"' in img.group(1) and "brand/v5/doorway-arch-400.webp" in img.group(1)
    assert "brand/v2/" not in body, "V4's single 400 px file is gone from the entrance"
    preloads = re.findall(r'<link rel="preload"[^>]*>', body)
    assert preloads == [
        f'<link rel="preload" as="image" type="image/avif" fetchpriority="high" imagesrcset="{avif.group(1)}" imagesizes="{avif.group(2)}">'
    ], preloads
    # the key: the loader's key-turn primitive, with the verbatim key inside
    key = re.search(r'<span class="sig__l sig__key door-stage__key"><span class="sig__turn"><svg viewBox="10 11 40 94" focusable="false">(.*?)</svg>', door)
    assert key, "the key is a `.sig__l.sig__key` layer with a `.sig__turn`: loader.css turns it on `.sig.is-engaged`"
    original = _read(KEY)
    drawn = re.sub(r' class="[^"]*"', "", key.group(1))
    for shape in re.findall(r"<(?:circle|rect)[^>]*?/>", re.sub(r' fill="[^"]*"', "", original)):
        assert shape in drawn, f"the stage's key lost a shape of key.svg: {shape}"
    assert len(re.findall(r"<(?:circle|rect)", drawn)) == 5, "five shapes, as key.svg"
    # the lights are layers of the stage, never text
    assert door.count('class="sig__l door-stage__step door-stage__step--') == 3
    assert '<span class="door-stage__frame"><span class="door-stage__frame-wipe"><svg class="door-stage__frame-light"' in door
    floor = stage.split('<div class="varco__floor" aria-hidden="true">', 1)[1].split("</div>", 1)[0]
    assert re.findall(r'data-way="([a-z]+)"', floor) == AUDIENCES
    assert not re.sub(r"<[^>]+>", "", floor).strip(), "the floor carries no text"
    assert not re.search(r"\sstyle=|<style|<script(?![^>]*src=)", body), "no inline style, no inline script"
    names = {name for value in re.findall(r'class="([^"]*)"', body) for name in value.split()}
    assert not [name for name in names if name == "entrance" or name.startswith("entrance__")], (
        "V1's .entrance (the four entrances, components.css §12) no longer reaches the layout"
    )
    assert ".account-page--entrance" not in _css(ROOT / "static" / "css" / "components.css"), "§27's entrance rule is gone"


def test_the_stage_host_is_named_in_one_place_only():
    carriers = []
    for folder in (ROOT / "templates", *(ROOT / "apps").glob("*/templates")):
        for path in folder.rglob("*.html"):
            if f'id="{HOST}"' in _read(path):
                carriers.append(path.relative_to(ROOT).as_posix())
    assert carriers == ["templates/allauth/layouts/entrance.html"], carriers


# --------------------------------------------------------------------------------------------- the sheets


def test_the_entrance_imports_the_door_and_nothing_loops():
    sheet, door, paints = _css(SHEET), _css(DOOR), _css(VARCO)
    assert sheet.strip().startswith(
        '@import url("../css/v5/_door.css");\n@import url("../css/v5/_varco.css");'
    ), "the two partials are imported before every rule: the door, then the niche's paints"
    # the paints' partial paints: it moves nothing and places nothing
    assert not re.search(r"(?<![\w-])(?:animation|transition|transform|opacity|display|position|inset[a-z-]*|grid[a-z-]*)\s*:", paints), "_varco.css paints only"
    assert "@keyframes" not in paints
    for name, css in (("entrance.css", sheet), ("_door.css", door), ("_varco.css", paints)):
        assert "infinite" not in css and "alternate" not in css, f"{name}: nothing loops"
        assert "will-change" not in css, f"{name}: no will-change (plan §1.5)"
        for value in re.findall(r"(?<![\w-])animation\s*:\s*([^;]+);", css):
            for part in (part.strip() for part in value.split(",")):
                assert re.search(r"var\(--motion-[a-z-]+\)", part), f"{name}: an animation off the duration tokens: {part}"
                assert not re.search(r"(?<![\w.-])\d*\.?\d+m?s\b", part), f"{name}: a typed duration: {part}"
                assert re.search(r"\s1\s+backwards$", part), f"{name}: one iteration, and no fill that stays in effect: {part}"
        for value in re.findall(r"(?<![\w-])transition\s*:\s*([^;]+);", css):
            if value.strip() == "none":
                continue
            assert "var(--motion-" in value and not re.search(r"(?<![\w.-])\d*\.?\d+m?s\b", value), f"{name}: {value}"
        for name_, body in _keyframes(css).items():
            assert "var(" not in body, f"{name_}: var() inside @keyframes does not animate"
            properties = set(re.findall(r"([a-z-]+)\s*:", re.sub(r"[\d.]+%|from|to", "", body)))
            assert properties <= {"transform", "opacity"}, f"{name_} moves {sorted(properties)}"
    # a pass ends on the element's own state: its keyframes have a `from` only
    for name in ("varco-draw", "varco-run", "varco-out", "door-frame-rise", "door-frame-hold"):
        body = {**_keyframes(sheet), **_keyframes(door)}[name]
        assert re.fullmatch(r"\s*from\s*\{[^}]*\}\s*", body), f"{name} must end on the element's own state"


def test_the_passes_are_one_tier_two_sequence_on_the_tokens():
    sheet = _css(SHEET)
    ways = re.search(r"\.varco__stage\.is-passing-ways \.varco__way-light \{([^}]*)\}", sheet).group(1)
    assert "varco-run var(--motion-slow) var(--ease-sine) 1 backwards" in ways
    assert "varco-out var(--motion-fast) var(--ease-sine) var(--motion-slow) 1 backwards" in ways, (
        "the bead goes out where it arrives, after the run: --motion-slow + --motion-fast, the plan's 600 ms"
    )
    assert re.search(r"\.varco__stage\.is-passing-ways \.varco__way-lit \{[^}]*varco-draw var\(--motion-slow\)", sheet)
    for part in ("frame-wipe", "frame-light"):
        assert re.search(rf"\.varco__stage\.is-passing-frame \.door-stage__{part} \{{[^}}]*var\(--motion-slow\) var\(--ease-sine\) 1 backwards", sheet)
    arrival = re.search(r"\.varco__stage\.is-arriving \.varco__way-light \{([^}]*)\}", sheet).group(1)
    assert arrival.count("var(--motion-route-light)") == 2 and arrival.count("calc(var(--motion-route-stagger) * var(--way-n))") == 2
    # each way is lit behind its light — drawn as the light runs, given back as it arrives — on the light's own clock
    lit = re.search(r"\.varco__stage\.is-arriving \.varco__way-lit \{([^}]*)\}", sheet).group(1)
    for name in ("varco-draw", "varco-glint"):
        assert f"{name} var(--motion-route-light) var(--ease-sine) calc(var(--motion-route-stagger) * var(--way-n)) 1 backwards" in lit, name
    tokens = _css(TOKENS)
    reduced = tokens.split("@media (prefers-reduced-motion: reduce)", 1)[1].split("\n}", 1)[0]
    used = set(re.findall(r"var\((--motion-[a-z-]+)\)", sheet + _css(DOOR)))
    assert used == {"--motion-fast", "--motion-standard", "--motion-slow", "--motion-stagger", "--motion-route-light", "--motion-route-stagger"}, used
    for name in used:
        assert f"{name}: 0ms" in reduced, f"{name} is not zeroed under reduced motion"


def test_every_state_the_script_writes_is_drawn_and_the_keyboard_never_animates():
    sheet, door, script = _css(SHEET), _css(DOOR), _read(SCRIPT)
    assert re.search(r"\.varco__stage\.is-ways \.varco__way-lit \{\s*opacity: 1;", sheet)
    assert re.search(r"\.varco__stage\.is-held \.varco__pool--lit,\s*\.varco__stage\.is-held \.varco__threshold--lit \{\s*opacity: 1;", sheet)
    # each of the door's two switches is set ON THE LAYER IT LIGHTS: a switch set on the stage's root is inherited by
    # every element of the stage, and each state restyled all of them (the performance check's P3: 206 elements for the
    # Tab, 128 with the stage held still)
    assert re.search(r"\.varco__stage\.is-frame \.door-stage__frame \{\s*--door-frame: 1;\s*\}", sheet)
    assert re.search(r"\.varco__stage\.is-held \.door-stage__step \{\s*--door-steps: 1;\s*\}", sheet)
    assert not re.search(r"\.varco__stage(?:\.[a-z-]+)+\s*\{[^}]*--door-(?:frame|steps)\s*:", sheet), "no switch on the stage's root"
    # _door.css draws the lights from its switches (each step's own opacity, the order, the stagger)
    assert re.search(r"\.door-stage__frame \{[^}]*opacity: var\(--door-frame, 0\);", door), "the frame's light is switched, transparent at rest"
    assert re.search(r"\.door-stage__step \{[^}]*opacity: calc\(var\(--door-steps, 0\) \* var\(--step-lit\)\);", door)
    for cls in (*STATES, *WAYS):
        assert f".varco__stage.{cls}" in sheet, f"{cls} is written by the script and drawn nowhere"
    assert 'const STATES = ["ways", "held", "frame"];' in script and "`is-${name}`" in script and "`is-passing-${name}`" in script
    for cls in ("is-arriving", "is-still"):
        assert f'"{cls}"' in script, cls
    keyboard = re.search(r'html\[data-input="key"\] \.varco__stage :is\(([^)]*)\) \{([^}]*)\}', sheet)
    assert keyboard and "transition-duration: 0ms;" in keyboard.group(2) and "transition-delay: 0ms;" in keyboard.group(2)
    for layer in (".door-stage__frame", ".door-stage__step", ".varco__way-lit", ".varco__pool--lit", ".varco__threshold--lit"):
        assert layer in keyboard.group(1), f"{layer} would fade under the keyboard"
    still = re.search(r"((?:\.varco__stage\.is-still [^{]*)+)\{\s*transition: none;", sheet)
    assert still and all(layer in still.group(1) for layer in (".door-stage__frame", ".door-stage__step", ".varco__way-lit"))


def test_the_scene_never_mirrors_and_forced_colours_take_no_light():
    sheet, door = _css(SHEET), _css(DOOR)
    assert "direction: ltr;" in re.search(r"\.door-stage \{([^}]*)\}", door).group(1), "the door, the key: drawn, never mirrored"
    assert "direction: ltr;" in re.search(r"\.varco__scene \{([^}]*)\}", sheet).group(1), "the ways too"
    paints = _css(VARCO)
    for css in (sheet, door, paints):
        assert not re.search(r"(?<![\w-])(?:left|right|margin-left|margin-right|padding-left|padding-right)\s*:", css)
    rtl = [selector for selector, _ in _rules(sheet) + _rules(paints) if '[dir="rtl"]' in selector]
    assert any(".varco__stage::after" in s for s in rtl), "the wall's seam has its twin: it is on the side that touches the form"
    assert rtl and all(".door-stage" not in s and ".varco__way" not in s and ".varco__floor" not in s for s in rtl), (
        "the reading direction moves the page's parts — the band's pool, the wall's seam — never the drawing"
    )
    forced_sheet = sheet.split("@media (forced-colors: active)", 1)[1]
    hidden = re.search(r"((?:\.[a-z_:-]+,?\s*)+)\{\s*display: none;", forced_sheet).group(1)
    for layer in (".varco__way-lit", ".varco__way-light", ".varco__threshold--lit", ".varco__pool", ".varco__stage::after"):
        assert layer in hidden, f"{layer} is displayed under forced colours"
    assert re.search(r"\.varco__threshold,\s*\.varco__way-line \{[^}]*background: CanvasText;", forced_sheet), "the ways in the system's ink"
    forced_door = door.split("@media (forced-colors: active)", 1)[1]
    assert re.search(r"\.door-stage__frame,\s*\.door-stage__step \{\s*display: none;", forced_door)
    for layer in (".varco__floor", ".varco__way", ".door-stage__frame"):
        bodies = [body for selector, body in _rules(sheet if layer.startswith(".varco") else door) if selector == layer]
        assert any(re.search(r"contain: (?:strict|layout paint)", body) for body in bodies), f"{layer} is not contained"


def test_the_grain_is_the_niche_s_and_the_niche_meets_the_footer():
    """The 3 % grain is drawn on the niche only, from 64rem: on the band it is not seen, and its 246 B file over a
    phone's small band was the page's largest contentful paint (the performance check's P2; acceptance L9: «the door,
    not the grain»). From 64rem the niche meets the night footer: no band of light wall between two nights (m1)."""
    sheet = _css(SHEET)
    desktop, below = _media(sheet, "(min-width: 64rem)")
    assert sheet.count("grain.svg") == 1 and "grain.svg" in desktop, "the grain only where the stage is a niche"
    grain = re.search(r"\.varco__stage::before \{([^}]*)\}", desktop).group(1)
    assert "opacity: 0.03;" in grain and "mix-blend-mode: multiply;" in grain and "pointer-events: none;" in grain
    assert "grain" not in below, "no grain on the band"
    assert re.search(r"\.page-entrance \.site-footer \{\s*margin-block-start: 0;\s*\}", desktop), "the niche meets the footer from 64rem"
    assert ".site-footer" not in below, "below 64rem the footer keeps its air: the form is on paper"


def test_the_colours_are_one_token_block_and_the_paints_one_page_only_partial():
    """The door's literals and the five colours the stage adds are one named block of v5/tokens.css; the stage's
    gradients are composed from them in the page-only partial the entrance imports — never as tokens of main.css,
    where every page of the site carried one page's picture (579 B gzip, measured; DL54-15's bust rule: «moves
    page-specific rules into page partials»). The page sheet reads tokens and writes no gradient."""
    tokens = _read(TOKENS)
    block = re.sub(r"/\*.*?\*/", "", tokens.split("§4.3 THE DOOR STAGE AND THE ENTRANCE «IL VARCO»", 1)[1], flags=re.S)
    values = dict(re.findall(r"^\s*(--(?:door|varco)-[a-z-]+)\s*:\s*([^;]+);", block, flags=re.M))
    declared = set(values)
    sheet, door, paints = _css(SHEET), _css(DOOR), _css(VARCO)
    used = set(re.findall(r"var\((--(?:door|varco)-[a-z-]+)", sheet + door + paints))
    local = set(re.findall(r"(?<![\w-])(--(?:door|varco)-[a-z-]+)\s*:", sheet + door))  # the sheets' own lengths and switches
    assert local == {"--door-w", "--door-frame", "--door-steps", "--varco-band", "--varco-band-min", "--varco-band-pad", "--varco-reveal"}, local
    switches = {"--door-frame", "--door-steps"}  # _door.css's API: read with a default, set by the consumer on the layers
    for name in switches:
        assert f"var({name}, 0)" in door, name
    assert used - local - switches <= declared, f"read and not declared: {sorted(used - local - switches - declared)}"
    assert declared <= used, f"declared and never read: {sorted(declared - used)}"
    # main.css carries colours, not the entrance's picture: every --varco-* token is one plain colour
    stage = {name: value.strip() for name, value in values.items() if name.startswith("--varco-")}
    assert stage and all(re.fullmatch(r"#[0-9a-f]{6}", value) for value in stage.values()), stage
    assert not re.search(r"(?<![\w-])--varco-[a-z-]+\s*:", paints), "the partial paints: it declares no custom property"
    for name, css in (("entrance.css", sheet), ("_door.css", door), ("_varco.css", paints)):
        assert not re.search(r"#[0-9a-fA-F]{3,8}\b|\brgba?\(|\bhsla?\(", css), f"{name}: a literal colour outside the token sheet"
    assert "gradient(" not in sheet, "an app sheet writes no gradient: the stage's are _varco.css's"
    assert paints.count("gradient(") >= 12 and "var(--varco-reveal)" in paints and "var(--varco-reveal)" in sheet
    # an alpha is a mix with transparent, in srgb: the same colour stop a literal rgba() gave
    assert set(re.findall(r"color-mix\(in ([a-z]+),", paints)) == {"srgb"}
    pool = re.search(r"\.varco__pool \{([^}]*)\}", paints).group(1)
    alphas = [float(a) for a in re.findall(r"var\(--identity-light-night\) ([0-9.]+)%", pool)]
    assert alphas and max(alphas) <= 12, f"the pool at rest is 12 % at most (plan §1.13): {alphas}"
    assert not re.search(r"\bmatching\b", _read(SHEET) + _read(DOOR) + _read(SCRIPT) + _read(LAYOUT), flags=re.I)


def test_the_script_writes_classes_only_and_asks_the_gate():
    script = _read(SCRIPT)
    code = re.sub(r"/\*.*?\*/|//[^\n]*", "", script, flags=re.S)
    assert 'import { afterPaint, durationToken, reducedMotion, settled } from "./motion.js";' in script
    for refused in (".style", "setAttribute(\"style\"", ".animate(", "requestAnimationFrame", "innerHTML", "textContent", "matchMedia"):
        assert refused not in code, f"entrance.js: {refused}"
    assert "reducedMotion()" in code and "settled(stage" in code
    assert 'document.documentElement.dataset.input === "pointer"' in code, "a pass only when a pointer asked"
    assert 'getPropertyValue("--varco-band")' in code, "the band is the sheet's to declare"
    assert 'durationToken("--motion-wait", 400)' in code, "an address being typed is read at the pause"
    assert 'document.getElementById("form-errors")' in code and "fromInside()" in code and "fromHistory()" in code
    assert "largest-contentful-paint" in code and ".decode()" in code, "the arrival waits for the door's paint"
    assert re.search(r"if \(stage\.classList\.contains\(cls\) !== on\) stage\.classList\.toggle\(cls, on\);", code), (
        "a class is written only when it changes"
    )
    assert code.count("classList.") == 2, "…and through that one function"


# ---------------------------------------------------------------------------------------------- in Chromium


@pytest.fixture(scope="module")
def browser():
    playwright = pytest.importorskip("playwright.sync_api")
    with playwright.sync_playwright() as p:
        try:
            instance = p.chromium.launch()
        except Exception as exc:  # pragma: no cover - browser not installed
            pytest.skip(f"Chromium not available: {exc}")
        yield instance
        instance.close()


STAGE = r"""() => {
  const s = document.querySelector('[data-varco-stage]');
  const opacity = (sel) => { const el = s.querySelector(sel); return el ? Number(getComputedStyle(el).opacity) : null; };
  return {
    classes: [...s.classList].filter((c) => c.startsWith('is-')).sort(),
    running: document.getAnimations().filter((a) => a.playState === 'running').map((a) => a.animationName || a.transitionProperty),
    stage: s.getAnimations({subtree: true}).map((a) => a.animationName || ('t:' + a.transitionProperty)),
    ways: opacity('.varco__way-lit'), threshold: opacity('.varco__threshold--lit'), pool: opacity('.varco__pool--lit'),
    frame: opacity('.door-stage__frame'), step: opacity('.door-stage__step--low'),
    input: document.documentElement.dataset.input || null,
    floor: getComputedStyle(s.querySelector('.varco__floor')).display,
    engaged: document.getElementById('varco-door').classList.contains('is-engaged'),
  };
}"""


def _page(browser, motion="no-preference", width=1440, height=900, forced="none"):
    context = browser.new_context(
        viewport={"width": width, "height": height}, reduced_motion=motion, forced_colors=forced, device_scale_factor=1
    )
    return context, context.new_page()


def _click(page, selector):
    """A real pointer press in the field's start, where no control sits."""
    box = page.locator(selector).first.bounding_box()
    page.mouse.click(box["x"] + 40, box["y"] + box["height"] / 2)


def _eventually(page, check, timeout=6.0):
    import time

    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if check():
            return True
        page.wait_for_timeout(50)
    return bool(check())


def _quiet(page):
    """Nothing of the stage is running or in effect any more."""
    return _eventually(page, lambda: page.evaluate(STAGE)["stage"] == [])


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
def test_the_arrival_is_said_once_and_a_focus_cuts_it(browser, live_server, seeded):
    context, page = _page(browser)
    try:
        page.goto(live_server.url + "/fr/compte/login/", wait_until="load")
        assert _eventually(page, lambda: "is-arriving" in page.evaluate(STAGE)["classes"]), "the arrival starts once the door is painted"
        state = page.evaluate(STAGE)
        # four lights, each with its way lit behind it (review m2): run and glint on the light, draw and glint on the way
        assert set(state["stage"]) == {"varco-run", "varco-glint", "varco-draw"} and len(state["stage"]) == 16, state["stage"]
        page.focus("#id_login")
        state = page.evaluate(STAGE)
        assert "is-arriving" not in state["classes"] and "varco-run" not in state["stage"], "any focus cuts it to the rest"
        page.evaluate("document.activeElement.blur()")
        page.wait_for_timeout(3000)
        assert page.evaluate(STAGE)["classes"] == [], "…and it is never said again"
        # left alone, the sentence ends by itself and leaves nothing behind
        page.goto(live_server.url + "/fr/compte/login/", wait_until="load")
        assert _eventually(page, lambda: "is-arriving" in page.evaluate(STAGE)["classes"])
        assert _eventually(page, lambda: page.evaluate(STAGE)["classes"] == [], timeout=8.0)
        rest = page.evaluate(STAGE)
        assert rest["stage"] == [] and rest["ways"] == 0 and rest["frame"] == 0 and rest["step"] == 0, rest
    finally:
        context.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
def test_the_stage_answers_a_pointer_with_one_pass_each(browser, live_server, seeded):
    context, page = _page(browser)
    try:
        page.goto(live_server.url + "/fr/compte/login/", wait_until="networkidle")
        _click(page, "#id_login")
        state = page.evaluate(STAGE)
        assert state["input"] == "pointer" and state["classes"] == ["is-passing-ways", "is-ways"], state
        assert {"varco-draw", "varco-run", "varco-out"} <= set(state["stage"]), "one pass: the ways drawn behind their lights"
        assert _quiet(page), "nothing stays in effect after the pass"
        state = page.evaluate(STAGE)
        assert state["classes"] == ["is-ways"] and state["ways"] == 1 and state["threshold"] == 0, state

        page.evaluate(
            """() => { window.__typed = {last: 0, held: []};
                 document.getElementById('id_login').addEventListener('input', () => { window.__typed.last = performance.now(); });
                 const s = document.querySelector('[data-varco-stage]');
                 new MutationObserver(() => { if (s.classList.contains('is-held')) window.__typed.held.push(performance.now()); })
                   .observe(s, {attributes: true, attributeFilter: ['class']}); }"""
        )
        page.keyboard.type("prenom.nom@example.com", delay=10)
        assert _eventually(page, lambda: "is-held" in page.evaluate(STAGE)["classes"])
        typed = page.evaluate("window.__typed")
        assert len(typed["held"]) == 1 and typed["held"][0] - typed["last"] >= 350, (
            f"an address being typed is read once, at the pause — «a@b» is valid, «a@b.» is not: {typed}"
        )
        assert _quiet(page)
        state = page.evaluate(STAGE)
        assert state["threshold"] == 1 and state["pool"] == 1 and state["step"] > 0.5, state

        _click(page, "#id_password")
        state = page.evaluate(STAGE)
        assert state["classes"] == ["is-frame", "is-held", "is-passing-frame", "is-ways"], state
        assert {"door-frame-rise", "door-frame-hold"} <= set(state["stage"])
        assert _quiet(page)
        state = page.evaluate(STAGE)
        assert state["classes"] == ["is-frame", "is-held", "is-ways"] and state["frame"] == 1, "three states, held"

        # the password's own control keeps the frame; leaving an empty password gives it back
        page.locator("[data-password-toggle]").first.focus()
        assert "is-frame" in page.evaluate(STAGE)["classes"]
        page.locator(".varco .form__actions .btn").first.focus()
        assert _quiet(page)
        state = page.evaluate(STAGE)
        assert state["classes"] == ["is-held", "is-ways"] and state["frame"] == 0, "the form holds an address, and no password"

        # clearing the address gives back the rest
        page.fill("#id_login", "")
        page.locator(".varco .form__actions .btn").first.focus()
        assert _quiet(page)
        state = page.evaluate(STAGE)
        assert state["classes"] == [] and state["ways"] == 0 and state["threshold"] == 0 and state["step"] == 0, state
    finally:
        context.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
def test_a_password_s_own_control_asks_for_the_frame_as_the_field_does(browser, live_server, seeded):
    """The show / hide control is the password's: a pointer's press on it asks for the frame, with its pass, and the
    focus it hands back to the field asks for nothing more."""
    context, page = _page(browser)
    try:
        page.goto(live_server.url + "/fr/compte/login/", wait_until="networkidle")
        page.wait_for_timeout(2800)  # the arrival has been said
        # from the e-mail field, as a person does: the field that loses the focus must not take the pass away
        _click(page, "#id_login")
        assert _quiet(page)
        box = page.locator("[data-password-toggle]").first.bounding_box()
        page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
        page.mouse.down()
        state = page.evaluate(STAGE)
        assert state["classes"] == ["is-frame", "is-passing-frame"], state
        page.mouse.up()  # the click: shell.js shows the password and gives the focus back to the field
        assert page.evaluate("document.activeElement.id") == "id_password"
        assert _quiet(page)
        state = page.evaluate(STAGE)
        assert state["classes"] == ["is-frame"] and state["frame"] == 1 and state["ways"] == 0, state
    finally:
        context.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
def test_from_the_keyboard_the_states_are_there_at_once(browser, live_server, seeded):
    context, page = _page(browser)
    try:
        page.goto(live_server.url + "/fr/compte/login/", wait_until="networkidle")
        page.wait_for_timeout(2800)  # the arrival has been said
        page.focus("body")
        for _ in range(60):
            page.keyboard.press("Tab")
            if page.evaluate("document.activeElement.id") == "id_login":
                break
        state = page.evaluate(STAGE)
        assert state["input"] == "key" and state["classes"] == ["is-ways"], state
        assert state["stage"] == [] and state["ways"] == 1, "no pass, no transition: tier 0"
        page.keyboard.type("prenom.nom@example.com", delay=10)
        assert _eventually(page, lambda: "is-held" in page.evaluate(STAGE)["classes"])
        state = page.evaluate(STAGE)
        assert state["stage"] == [] and state["threshold"] == 1 and state["step"] > 0.5, state
        page.keyboard.press("Tab")
        state = page.evaluate(STAGE)
        assert state["classes"] == ["is-frame", "is-held", "is-ways"] and state["stage"] == [] and state["frame"] == 1, state
    finally:
        context.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
def test_under_the_setting_every_state_is_a_still(browser, live_server, seeded):
    context, page = _page(browser, motion="reduce")
    try:
        page.goto(live_server.url + "/fr/compte/login/", wait_until="networkidle")
        page.wait_for_timeout(600)
        rest = page.evaluate(STAGE)
        assert rest["classes"] == [] and rest["stage"] == [], "no arrival under reduced motion"
        _click(page, "#id_login")
        state = page.evaluate(STAGE)
        assert state["classes"] == ["is-ways"] and state["stage"] == [] and state["ways"] == 1, "the end, without travel"
        page.keyboard.type("prenom.nom@example.com", delay=5)
        _click(page, "#id_password")
        state = page.evaluate(STAGE)
        assert state["classes"] == ["is-frame", "is-held", "is-ways"] and state["stage"] == [], state
        assert state["frame"] == 1 and state["threshold"] == 1 and state["step"] > 0.5, state
    finally:
        context.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
def test_on_the_sign_in_s_submit_the_stage_s_key_turns_once_and_holds(browser, live_server, seeded):
    context, page = _page(browser)
    try:
        # the answer is given at the network, never by a view: 204, so the page stays and the hold can be read
        page.route("**/*", lambda route: route.fulfill(status=204, body="") if route.request.method == "POST" else route.continue_())
        page.goto(live_server.url + "/fr/compte/login/", wait_until="networkidle")
        _click(page, "#id_login")
        page.keyboard.type("prenom.nom@example.com", delay=5)
        _click(page, "#id_password")
        page.keyboard.type("not-a-password", delay=5)
        page.locator(".varco .form__actions .btn--primary").click()
        assert _eventually(page, lambda: page.evaluate(STAGE)["engaged"]), "the form names the stage, the loader engages it"
        turn = page.evaluate(
            """() => { const t = document.querySelector('#varco-door .sig__turn'); const a = t.getAnimations()[0];
                 return {name: a && a.animationName, iterations: getComputedStyle(t).animationIterationCount,
                         duration: getComputedStyle(t).animationDuration, busy: document.querySelector('.varco .form__actions .btn').getAttribute('aria-busy')}; }"""
        )
        assert turn == {"name": "sig-turn", "iterations": "1", "duration": "0.48s", "busy": "true"}, turn
        page.wait_for_timeout(900)
        held = page.evaluate(
            """() => { const t = document.querySelector('#varco-door .sig__turn'); const a = t.getAnimations()[0];
                 return {state: a && a.playState, matrix: getComputedStyle(t).transform, classes: [...document.querySelector('[data-varco-stage]').classList].filter((c) => c.startsWith('is-')).sort()}; }"""
        )
        assert held["state"] == "finished", "one turn, then the hold"
        values = [float(n) for n in re.findall(r"-?[\d.]+(?:e-?\d+)?", held["matrix"].split("(", 1)[1])]
        assert values[0] == pytest.approx(1, abs=1e-6), f"the key holds on the verbatim key, never mirrored: {held['matrix']}"
        assert held["classes"] == ["is-frame", "is-held", "is-ways"], "the lights stay as the form left them"

        # another entrance form engages nothing
        page.goto(live_server.url + "/fr/compte/password/reset/", wait_until="networkidle")
        _click(page, "#id_email")
        page.keyboard.type("prenom.nom@example.com", delay=5)
        page.locator(".varco .form__actions .btn--primary").click()
        page.wait_for_timeout(700)
        state = page.evaluate(STAGE)
        assert not state["engaged"] and "is-ways" in state["classes"], state
    finally:
        context.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
def test_a_refused_sign_in_s_page_loads_at_rest_with_the_kept_address(browser, live_server, seeded):
    context, page = _page(browser)
    try:
        page.add_init_script(
            """window.__seen = []; document.addEventListener('DOMContentLoaded', () => { const s = document.querySelector('[data-varco-stage]');
               if (s) new MutationObserver(() => window.__seen.push(s.className)).observe(s, {attributes: true, attributeFilter: ['class']}); });"""
        )
        page.goto(live_server.url + "/fr/compte/login/", wait_until="networkidle")
        page.fill("#id_login", "personne.inconnue@example.com")
        page.fill("#id_password", "not-a-password")
        with page.expect_navigation(wait_until="load"):
            page.locator("#id_password").press("Enter")
        page.wait_for_timeout(3200)
        state = page.evaluate(STAGE)
        assert page.locator("#form-errors").count() == 1 and page.input_value("#id_login") == "personne.inconnue@example.com"
        assert state["classes"] == ["is-held", "is-ways"] and state["stage"] == [], "the still of the kept address"
        assert state["ways"] == 1 and state["threshold"] == 1 and state["frame"] == 0, state
        seen = " ".join(page.evaluate("window.__seen"))
        assert "is-arriving" not in seen and "is-passing" not in seen, "no arrival and no travel on a refused sign-in's page"
    finally:
        context.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("size", [(390, 844), (360, 640)])
def test_below_64rem_the_stage_is_a_band_and_the_frame_answers(browser, live_server, seeded, size):
    width, height = size
    context, page = _page(browser, width=width, height=height)
    try:
        page.goto(live_server.url + "/fr/compte/login/", wait_until="networkidle")
        page.wait_for_timeout(500)
        geometry = page.evaluate(
            """() => { const r = (sel) => document.querySelector(sel).getBoundingClientRect();
                 return {stage: r('[data-varco-stage]'), focus: r('.varco__focus'), sheet: r('.varco__sheet'), submit: r('.varco .form__actions .btn--primary'),
                         overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth}; }"""
        )
        rest = page.evaluate(STAGE)
        assert rest["floor"] == "none" and rest["classes"] == [], "the band keeps the door alone, and says no arrival"
        grain = page.evaluate("(() => { const cs = getComputedStyle(document.querySelector('[data-varco-stage]'), '::before'); return [cs.content, cs.backgroundImage]; })()")
        assert grain == ["none", "none"], f"no grain on the band: {grain}"
        assert geometry["overflow"] <= 0
        assert geometry["stage"]["width"] == width and geometry["focus"]["width"] == width, "one column: both parts span the page"
        assert geometry["stage"]["bottom"] <= geometry["sheet"]["top"], "the band above the form"
        assert geometry["stage"]["height"] <= (124 if height > 704 else 76), geometry["stage"]["height"]
        assert geometry["submit"]["bottom"] <= height, "the form's action is in the first viewport"
        _click(page, "#id_login")
        state = page.evaluate(STAGE)
        assert "is-frame" in state["classes"] and "is-ways" not in state["classes"], "on the band the frame answers the e-mail field"
        assert _quiet(page) and page.evaluate(STAGE)["frame"] == 1
    finally:
        context.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("lang", ["fr", "ar"])
@pytest.mark.parametrize("size", [(1440, 900), (1024, 768), (390, 844), (360, 640)])
def test_nothing_moves_when_the_stage_arrives(browser, live_server, seeded, lang, size):
    """In the source the focus precedes the stage, and a slow browser paints before the stage has been parsed: the
    form's box is the same with and without the stage in the document, and the help line's with and without the
    scene — every part's place is held before the part is there — and the stage's place is already the night: the
    ground is the page's own box's, in the stage's cell, at the stage's size."""
    width, height = size
    context, page = _page(browser, width=width, height=height)
    box = "(sel) => { const b = document.querySelector(sel).getBoundingClientRect(); return [b.left, b.top, b.width, b.height].map((v) => Math.round(v * 10) / 10); }"
    ground = "() => { const cs = getComputedStyle(document.querySelector('.varco'), '::before'); return {colour: cs.backgroundColor, size: [cs.width, cs.height].map((v) => Math.round(parseFloat(v) * 10) / 10)}; }"
    try:
        page.goto(f"{live_server.url}/{lang}/compte/login/", wait_until="networkidle")
        sheet, focus, help_line, stage = (page.evaluate(box, sel) for sel in (".varco__sheet", ".varco__focus", ".varco__help", "[data-varco-stage]"))
        night = page.evaluate("getComputedStyle(document.querySelector('[data-varco-stage]')).backgroundColor")
        page.evaluate("document.querySelector('.varco__scene').remove()")
        assert page.evaluate(box, ".varco__help") == help_line, "the help line moved when the scene arrived"
        page.evaluate("document.querySelector('[data-varco-stage]').remove()")
        assert page.evaluate(box, ".varco__focus") == focus and page.evaluate(box, ".varco__sheet") == sheet, (
            "the form moved when the stage arrived"
        )
        before = page.evaluate(ground)
        assert before["colour"] == night and before["size"] == stage[2:], f"the stage's place is not the night before the stage: {before}, {night}, {stage}"
    finally:
        context.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
def test_under_forced_colours_the_stage_takes_no_light(browser, live_server, seeded):
    context, page = _page(browser, forced="active")
    try:
        page.goto(live_server.url + "/fr/compte/login/", wait_until="networkidle")
        _click(page, "#id_login")
        page.keyboard.type("prenom.nom@example.com", delay=5)
        _click(page, "#id_password")
        page.wait_for_timeout(700)
        shown = page.evaluate(
            """() => Object.fromEntries(['.varco__way-lit', '.varco__way-light', '.varco__threshold--lit', '.varco__pool--lit', '.door-stage__frame', '.door-stage__step']
                 .map((sel) => [sel, getComputedStyle(document.querySelector(sel)).display]))"""
        )
        assert set(shown.values()) == {"none"}, shown
        assert page.evaluate("getComputedStyle(document.querySelector('.varco__way-line')).display") != "none", "the ways stay, drawn"
    finally:
        context.close()


#: The photograph's box and what its `sizes` tells the browser, in CSS px: the first entry whose condition holds,
#: measured as a length on the page (the sizes' lengths are the sheet's, in rem and vw).
PHOTO = r"""() => {
  const picture = document.querySelector('#varco-door .door-stage__photo');
  const source = picture.querySelector('source[type="image/avif"]');
  let told = null;
  for (const entry of source.getAttribute('sizes').split(/,\s*/)) {
    const parts = entry.trim().match(/^(\(.*\))\s+(\S+)$/);
    const [condition, length] = parts ? [parts[1], parts[2]] : [null, entry.trim()];
    if (condition && !matchMedia(condition).matches) continue;
    const probe = document.createElement('div');
    probe.style.position = 'absolute';
    probe.style.width = length;
    document.body.append(probe);
    told = probe.getBoundingClientRect().width;
    probe.remove();
    break;
  }
  const img = picture.querySelector('img');
  return {box: picture.getBoundingClientRect().width, told, file: img.currentSrc.split('/').pop(), natural: img.naturalWidth};
}"""


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
def test_the_photograph_s_sizes_follow_its_box_and_one_file_is_fetched(browser, live_server, seeded):
    """Review M1 and the check's F1: the photograph is told the WIDEST it is drawn in each range of windows, never less
    (told less, the browser takes a file too small and stretches it) and never much more; at a device scale of 2 the
    chosen file covers the box's device pixels; the preload and the picture choose the same file, so one is fetched.
    The cases cross every line of the sizes: the short desktop's three, the desktop's three, the short band, the band
    from 48rem and the phone's."""
    cases = [
        (1440, 900), (1920, 1080), (2560, 1440), (1600, 1000), (1100, 900), (1366, 768), (1600, 800), (1024, 768),
        (768, 1024), (390, 844), (360, 640), (800, 600),
    ]
    for width, height in cases:
        context = browser.new_context(viewport={"width": width, "height": height}, device_scale_factor=1)
        page = context.new_page()
        try:
            page.goto(live_server.url + "/fr/compte/login/", wait_until="load")
            photo = page.evaluate(PHOTO)
            assert photo["told"] >= photo["box"] - 0.5, f"{width} × {height}: told {photo['told']:.1f} px for a box of {photo['box']:.1f}"
            assert photo["told"] <= photo["box"] * 1.02 + 1, f"{width} × {height}: told {photo['told']:.1f} px for a box of {photo['box']:.1f}"
        finally:
            context.close()
    for width, height, file in ((1440, 900, "576"), (1920, 1080, "800"), (390, 844, "400")):
        context = browser.new_context(viewport={"width": width, "height": height}, device_scale_factor=2)
        page = context.new_page()
        fetched = []
        page.on("request", lambda request: fetched.append(request.url) if "doorway-arch" in request.url else None)
        try:
            page.goto(live_server.url + "/fr/compte/login/", wait_until="load")
            page.wait_for_timeout(300)
            photo = page.evaluate(PHOTO)
            assert photo["file"].startswith(f"doorway-arch-{file}."), (width, photo)
            # the candidate's own width (an image from a srcset reports a density-corrected naturalWidth: the box's)
            chosen = int(photo["file"].split("-")[2].split(".")[0])
            assert chosen >= photo["box"] * 2 or chosen == 400, f"{width} px at 2×: {chosen} px for {photo['box'] * 2:.0f} device px"
            assert len(fetched) == 1 and fetched[0].endswith(photo["file"]), f"one photograph fetched: {fetched}"
        finally:
            context.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
def test_from_64rem_the_niche_meets_the_footer(browser, live_server, seeded):
    """Review m1: from 64rem the night niche runs down to the night footer — no band of light wall between the two."""
    for width, height in ((1440, 900), (1024, 768)):
        context, page = _page(browser, width=width, height=height)
        try:
            page.goto(live_server.url + "/fr/compte/login/", wait_until="networkidle")
            edges = page.evaluate(
                "() => [document.querySelector('[data-varco-stage]').getBoundingClientRect().bottom, document.querySelector('.site-footer').getBoundingClientRect().top]"
            )
            assert abs(edges[1] - edges[0]) < 1, f"{width}: the stage ends at {edges[0]:.1f}, the footer begins at {edges[1]:.1f}"
        finally:
            context.close()
