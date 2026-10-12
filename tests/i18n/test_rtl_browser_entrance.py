"""
RTL check of the entrance «Il varco» (design V5, V5.4 plan §1.13, §2.5; acceptance L11; W2-B).

What the static guard cannot see (plan §2.5): the stage is a drawing placed in its own units, so its geometry is
measured in a browser. In Arabic as in French —

* the PAGE mirrors: the stage stands at the reading edge (the right in Arabic) and the form at the other end; the
  wall's reveal and the shadow it casts are on the stage's side that touches the form; below 64rem the band's door is
  at the reading edge and the help line beside it; nothing overflows at 1440, 390 or 360 px;
* the DRAWING never mirrors: the door stage is `direction: ltr`, untransformed; the key stands at the same place on
  the door, its bit on the same side; the four ways keep their order from the drawing's left — Persona, Impresa,
  Istituzione, Università — and their angles;
* Latin data stays left-to-right: the help line's address, the e-mail and the password fields;
* a password is typed left to right in Arabic too, and its show / hide control sits at the field's end — the left:
  the room kept for the control is on the control's side, so that neither the placeholder nor the typed password is
  set under it;
* THE FORM mirrors with the page (step 2): the eyebrow's key before its words, the label at the reading edge of its
  row and the «forgotten password» link at the row's end, the primary's key at the inline end — the left — and never
  mirrored itself; the assurance's link stands at the reading edge, and the locked answer is quoted only where the
  registry holds it in the page's language — in Arabic, until a translation is published, the link alone (a French
  paragraph under the action read as a missing translation: the review's m3).

Chromium, on the login. The stage's states and motion are tests/frontend/test_entrance_w2_b.py; the form is
tests/frontend/test_entrance_form_w2_b.py.
"""

from __future__ import annotations

import os

import pytest

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

pytestmark = [pytest.mark.browser, pytest.mark.django_db(transaction=True)]

SIZES = [(1440, 900), (390, 844), (360, 640)]

#: The page's parts and the drawing's parts, measured against the door (so that the two languages compare).
GEOMETRY = r"""() => {
  const r = (el) => el.getBoundingClientRect();
  const stage = document.querySelector('[data-varco-stage]');
  const door = document.getElementById('varco-door');
  const key = door.querySelector('.door-stage__key');
  const svg = key.querySelector('svg');
  const bit = svg.querySelectorAll('rect')[1];
  const shaft = svg.querySelectorAll('rect')[0];
  const d = r(door);
  const rel = (el) => { const b = r(el); return [(b.left - d.left) / d.width, (b.top - d.top) / d.height, b.width / d.width].map((v) => Math.round(v * 1e4) / 1e4); };
  const ways = [...stage.querySelectorAll('.varco__way')].map((way) => {
    const b = r(way);
    return {name: way.dataset.way, centre: Math.round(((b.left + b.right) / 2 - (d.left + d.right) / 2) * 10) / 10, transform: getComputedStyle(way).transform};
  });
  const seam = getComputedStyle(stage, '::after');
  return {
    dir: document.documentElement.dir,
    overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
    stage: {left: r(stage).left, right: r(stage).right},
    focus: {left: r(document.querySelector('.varco__focus')).left, right: r(document.querySelector('.varco__focus')).right},
    door: {direction: getComputedStyle(door).direction, transform: getComputedStyle(door).transform, left: d.left, right: d.right},
    key: rel(key),
    bitRightOfShaft: r(bit).left >= r(shaft).left,
    keyTurn: getComputedStyle(key.querySelector('.sig__turn')).transform,
    floor: getComputedStyle(stage.querySelector('.varco__floor')).display,
    ways,
    seam: {left: seam.left, right: seam.right, display: seam.display},
    help: {left: r(stage.querySelector('.varco__help')).left, right: r(stage.querySelector('.varco__help')).right,
           align: getComputedStyle(stage.querySelector('.varco__help')).textAlign},
    mail: getComputedStyle(stage.querySelector('.varco__help a')).direction,
    fields: ['#id_login', '#id_password'].map((sel) => getComputedStyle(document.querySelector(sel)).direction),
  };
}"""


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


def _measure(browser, url, width, height):
    context = browser.new_context(viewport={"width": width, "height": height}, device_scale_factor=1)
    try:
        page = context.new_page()
        response = page.goto(url, wait_until="networkidle")
        assert response.status == 200
        page.evaluate("async () => { await document.fonts.ready }")
        return page.evaluate(GEOMETRY)
    finally:
        context.close()


@pytest.mark.parametrize("size", SIZES)
def test_the_page_mirrors_and_the_drawing_does_not(browser, live_server, seeded, size):
    width, height = size
    fr = _measure(browser, f"{live_server.url}/fr/compte/login/", width, height)
    ar = _measure(browser, f"{live_server.url}/ar/compte/login/", width, height)
    assert (fr["dir"], ar["dir"]) == ("ltr", "rtl")
    assert fr["overflow"] <= 0 and ar["overflow"] <= 0, (width, fr["overflow"], ar["overflow"])

    # the drawing: the same door, the same key at the same place, never mirrored
    for page in (fr, ar):
        assert page["door"]["direction"] == "ltr" and page["door"]["transform"] == "none", page["door"]
        assert page["keyTurn"] == "none", "at rest the key is the verbatim key: no transform holds it"
        assert page["bitRightOfShaft"], "the key's bit stays on its own side"
        assert page["mail"] == "ltr" and page["fields"] == ["ltr", "ltr"], "Latin data reads left to right"
    assert ar["key"] == pytest.approx(fr["key"], abs=0.002), f"the key moved on the door: {fr['key']} → {ar['key']}"

    if width >= 1024:
        # the page: the stage at the reading edge, the form at the other end
        assert fr["stage"]["right"] <= fr["focus"]["left"] + 1 and ar["stage"]["left"] >= ar["focus"]["right"] - 1
        # the wall's reveal on the side that touches the form
        assert fr["seam"]["right"] == "0px" and ar["seam"]["left"] == "0px", (fr["seam"], ar["seam"])
        # the ways: one fan, in the drawing's order and with the drawing's angles, in both languages
        assert [way["name"] for way in ar["ways"]] == ["persona", "impresa", "istituzione", "universita"]
        assert [way["centre"] for way in ar["ways"]] == pytest.approx([way["centre"] for way in fr["ways"]], abs=0.6), "the fan moved"
        assert [way["transform"] for way in ar["ways"]] == [way["transform"] for way in fr["ways"]], "an angle mirrored"
        centres = [way["centre"] for way in fr["ways"]]
        assert centres == sorted(centres) and centres[0] < 0 < centres[-1], f"Persona on the drawing's left, Università on its right: {centres}"
        # the help line starts on the page's reading edge
        assert fr["help"]["align"] in ("start", "left") and ar["help"]["align"] in ("start", "right")
        assert ar["help"]["right"] > ar["door"]["left"], "the Arabic help line is set from the right"
    else:
        # the band: the door at the reading edge, the help line beside it; no floor
        assert fr["floor"] == "none" and ar["floor"] == "none"
        assert fr["door"]["right"] <= fr["help"]["left"] and ar["door"]["left"] >= ar["help"]["right"], (fr["door"], fr["help"], ar["door"], ar["help"])


def test_the_arabic_stage_answers_as_the_french_one(browser, live_server, seeded):
    """The states are the same picture in both directions: the lit ways and the lit frame sit where the drawing has them."""
    probe = r"""() => {
      const stage = document.querySelector('[data-varco-stage]');
      const door = document.getElementById('varco-door').getBoundingClientRect();
      const box = (sel) => { const b = stage.querySelector(sel).getBoundingClientRect(); return [b.left - door.left, b.top - door.top, b.width, b.height].map((v) => Math.round(v * 10) / 10); };
      return {classes: [...stage.classList].filter((c) => c.startsWith('is-')).sort(), frame: box('.door-stage__frame'), threshold: box('.varco__threshold--lit'),
              ways: Number(getComputedStyle(stage.querySelector('.varco__way-lit')).opacity), lit: Number(getComputedStyle(stage.querySelector('.door-stage__frame')).opacity)};
    }"""
    seen = {}
    for lang in ("fr", "ar"):
        context = browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1, reduced_motion="reduce")
        try:
            page = context.new_page()
            page.goto(f"{live_server.url}/{lang}/compte/login/", wait_until="networkidle")
            page.fill("#id_login", "prenom.nom@example.com")
            page.focus("#id_password")
            page.wait_for_timeout(600)
            seen[lang] = page.evaluate(probe)
        finally:
            context.close()
    assert seen["fr"]["classes"] == seen["ar"]["classes"] == ["is-frame", "is-held", "is-ways"], seen
    assert seen["ar"]["frame"] == pytest.approx(seen["fr"]["frame"], abs=0.6), seen
    assert seen["ar"]["threshold"] == pytest.approx(seen["fr"]["threshold"], abs=0.6), seen
    assert seen["ar"]["ways"] == seen["fr"]["ways"] == 1 and seen["ar"]["lit"] == seen["fr"]["lit"] == 1


#: Every password field of the page with its show / hide control: the box the typed text and the placeholder are
#: set in (the input's content box), and the control's box.
ROOM = r"""() => [...document.querySelectorAll('.varco .form-field__control--password')].map((control) => {
  const input = control.querySelector('input');
  const toggle = control.querySelector('[data-password-toggle]');
  const i = input.getBoundingClientRect(), t = toggle.getBoundingClientRect(), cs = getComputedStyle(input);
  return {
    id: input.id,
    direction: cs.direction,
    text: [i.left + parseFloat(cs.borderLeftWidth) + parseFloat(cs.paddingLeft), i.right - parseFloat(cs.borderRightWidth) - parseFloat(cs.paddingRight)],
    toggle: [t.left, t.right],
    field: [i.left, i.right],
  };
})"""


@pytest.mark.parametrize("lang", ["fr", "ar"])
@pytest.mark.parametrize("size", SIZES)
def test_a_password_is_never_set_under_its_control(browser, live_server, seeded, lang, size):
    """In Arabic the password field is `direction: ltr` (static/css/base.css) while its control stays at the field's
    end, the left: `padding-inline-end` alone kept the room on the right, and at 390 px the placeholder and the typed
    password ran under «إظهار كلمة المرور» — on V4 as on V5. The room is on the control's side in both directions."""
    width, height = size
    seen = 0
    for path in ("login", "signup"):
        context = browser.new_context(viewport={"width": width, "height": height}, device_scale_factor=1)
        try:
            page = context.new_page()
            response = page.goto(f"{live_server.url}/{lang}/compte/{path}/", wait_until="networkidle")
            assert response.status == 200
            page.evaluate("async () => { await document.fonts.ready }")
            rooms = page.evaluate(ROOM)
        finally:
            context.close()
        for room in rooms:
            seen += 1
            (text_left, text_right), (toggle_left, toggle_right) = room["text"], room["toggle"]
            assert room["direction"] == "ltr", room
            assert text_right <= toggle_left + 0.5 or text_left >= toggle_right - 0.5, f"{lang} {width} {path}: the text box {room['text']} runs under the control {room['toggle']}"
            assert text_right - text_left >= 80, f"{lang} {width} {path}: {text_right - text_left:.0f} px left for the password"
            # the control at the field's end: the left in Arabic, the right in French
            field_left, field_right = room["field"]
            at_the_left = toggle_left - field_left < field_right - toggle_right
            assert at_the_left == (lang == "ar"), room
    assert seen, "the login has a password field with its control"


#: The form's parts, measured against the column they stand in (so that the two languages compare).
FORM = r"""() => {
  const r = (el) => el.getBoundingClientRect();
  const q = (sel) => document.querySelector(sel);
  const sheet = r(q('.varco__sheet'));
  const side = (el) => { const b = r(el); return {start: Math.round((b.left - sheet.left) * 10) / 10, end: Math.round((sheet.right - b.right) * 10) / 10, mid: (b.left + b.right) / 2}; };
  const submit = q('.varco .form__actions .btn--primary');
  const key = getComputedStyle(submit, '::after');
  const s = r(submit);
  const inlineEnd = parseFloat(key.insetInlineEnd), w = parseFloat(key.width);
  const assurance = q('.varco__assurance-a');
  return {
    eyebrow: {key: side(q('.varco__eyebrow-key')), words: side(q('.varco__eyebrow span'))},
    label: side(q('label[for=id_password]')),
    reset: side(q('.form-field__aside a')),
    field: side(q('#id_password')),
    toggle: side(q('[data-password-toggle]')),
    row: Math.abs((r(q('label[for=id_password]')).top + r(q('label[for=id_password]')).bottom) - (r(q('.form-field__aside a')).top + r(q('.form-field__aside a')).bottom)) / 2,
    key: {left: key.left, right: key.right, end: inlineEnd, w, transform: key.transform, scale: key.scale, mask: key.maskImage || key.webkitMaskImage, pad: [parseFloat(getComputedStyle(submit).paddingLeft), parseFloat(getComputedStyle(submit).paddingRight)]},
    labelMid: (() => { const range = document.createRange(); range.selectNodeContents(submit); const b = range.getBoundingClientRect(); return (b.left + b.right) / 2 - (s.left + s.right) / 2; })(),
    assurance: assurance ? {dir: getComputedStyle(assurance).direction, align: getComputedStyle(assurance).textAlign, lang: assurance.getAttribute('lang')} : null,
    more: q('.varco__assurance-more a') ? side(q('.varco__assurance-more a')) : null,
    typed: ['#id_login', '#id_password'].map((sel) => getComputedStyle(q(sel)).fontSize),
  };
}"""


@pytest.fixture
def phase3_live(set_flag, monkeypatch):
    """Gate G3 open for the live server, without freezegun (a frozen ``time.monotonic`` stalls Playwright's event
    loop): every publication decision goes through ``core.clock.now()`` — the fixture of tests/i18n/test_rtl_browser.py."""
    import datetime as dt

    from core import clock, flags

    fixed = dt.datetime(2026, 10, 3, 10, 0, tzinfo=dt.UTC)
    monkeypatch.setattr(clock, "now", lambda: fixed)
    set_flag("phase3_public", True, enabled_from=dt.datetime(2026, 10, 2, tzinfo=dt.UTC))
    flags.invalidate()
    yield
    flags.invalidate()


@pytest.mark.parametrize("size", [(1440, 900), (390, 844)])
def test_the_form_mirrors_and_its_key_does_not(browser, live_server, seeded, phase3_live, size):
    width, height = size
    seen = {}
    for lang in ("fr", "ar"):
        context = browser.new_context(viewport={"width": width, "height": height}, device_scale_factor=1)
        try:
            page = context.new_page()
            response = page.goto(f"{live_server.url}/{lang}/compte/login/", wait_until="networkidle")
            assert response.status == 200
            page.evaluate("async () => { await document.fonts.ready }")
            seen[lang] = page.evaluate(FORM)
        finally:
            context.close()
    fr, ar = seen["fr"], seen["ar"]
    for page in (fr, ar):
        assert page["typed"] == ["16px", "16px"], page["typed"]
        assert page["row"] <= 2, f"the label and the link share one row: {page['row']}"
        assert page["key"]["transform"] == "none" and page["key"]["scale"] == "none", "the key is drawn, never mirrored"
        assert abs(page["labelMid"]) < 1, "the label is centred on the plate in both directions"
    assert fr["key"]["mask"] == ar["key"]["mask"], "one drawing of the key"
    # the eyebrow: the key before its words
    assert fr["eyebrow"]["key"]["mid"] < fr["eyebrow"]["words"]["mid"] and ar["eyebrow"]["key"]["mid"] > ar["eyebrow"]["words"]["mid"]
    assert fr["eyebrow"]["key"]["start"] == pytest.approx(ar["eyebrow"]["key"]["end"], abs=1)
    # the label's row: the label at the reading edge, the link at the row's end; the control at the field's end
    assert fr["label"]["start"] == pytest.approx(0, abs=1) and ar["label"]["end"] == pytest.approx(0, abs=1)
    assert fr["reset"]["end"] == pytest.approx(0, abs=1) and ar["reset"]["start"] == pytest.approx(0, abs=1)
    assert fr["toggle"]["end"] == pytest.approx(ar["toggle"]["start"], abs=1) and fr["toggle"]["end"] < fr["toggle"]["start"]
    # the primary's key: at the inline end — the right in French, the left in Arabic — in the middle of the end pad
    for page in (fr, ar):
        assert page["key"]["end"] == pytest.approx((52 - page["key"]["w"]) / 2, abs=0.6), page["key"]
        assert page["key"]["pad"] == [52, 52], "the two pads are the plate's height in both directions"
    assert float(ar["key"]["left"].replace("px", "")) == pytest.approx(ar["key"]["end"], abs=0.6), "in Arabic the inline end is the left"
    assert float(fr["key"]["right"].replace("px", "")) == pytest.approx(fr["key"]["end"], abs=0.6), "in French, the right"
    # the assurance: the locked answer where the registry holds the page's language (French), the link alone on the
    # Arabic page until a translation is published — and the link starts at the reading edge in both
    assert fr["assurance"] and fr["assurance"]["lang"] is None, "Phase 3 is open in this test: the assurance is on the page"
    assert ar["assurance"] is None, "no French paragraph under the action of the Arabic page (review m3)"
    assert fr["more"] and ar["more"], "the Privacy Policy link, in every language"
    assert fr["more"]["start"] == pytest.approx(0, abs=1) and ar["more"]["end"] == pytest.approx(0, abs=1), (
        "the page's own link starts at the reading edge"
    )
