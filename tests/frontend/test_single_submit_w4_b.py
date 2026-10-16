"""
Every guarded form submits through a `.btn` (W4-B; the integration checkpoint's review,
docs/design-v5/QA/v54/intfix/REVIEW.md m2).

main.js's double-submit guard (`form[data-single-submit]`: the form marked `data-submitted`, its submit buttons
`aria-disabled`) is lifted by static/js/src/loader.js — «Réessayer», the 10 s lease, an answer given in the page — or,
when loader.js cannot be loaded, at once by static/js/src/shell.js's catch. Both are reached through shell.js's submit
hook only, and the hook hands a submit to loader.js when its control is a `button.btn` (or its form names a loader
host): a guarded form sent by any other control returns early, and on an answer that does not replace the page its
refusal would stand for ever. So every control that can submit a guarded form is a button of the system:

* the project's own guarded forms: every submit control inside them — in the form or in a template it includes — is a
  `<button>` with the class `btn`; no `<input type="submit">`, no `<input type="image">`;
* every allauth form is guarded (templates/allauth/elements/form.html and form__entrance.html), allauth writes its
  submits through its `button` element, and the project's templates/allauth/elements/button.html (and its layout
  variants, button__<layout>.html) render that element as a `button.btn`; allauth's own templates write no raw `<button>` and no `<input type="submit">`.
"""

from __future__ import annotations

import re
from pathlib import Path

import allauth

ROOT = Path(__file__).resolve().parents[2]
TEMPLATES = ROOT / "templates"
ALLAUTH_TEMPLATES = Path(allauth.__file__).resolve().parent / "templates"

GUARDED_FORM = re.compile(r"<form\b[^>]*\bdata-single-submit\b[^>]*>(.*?)</form>", re.S)
BUTTON = re.compile(r"<button\b([^>]*)>", re.S)
SUBMIT_INPUT = re.compile(r"""<input\b[^>]*\btype=["']?(?:submit|image)\b""", re.S)
INCLUDE = re.compile(r"""\{%\s*include\s+["']([^"']+)["']""")
COMMENT = re.compile(r"\{%\s*comment\s*%\}.*?\{%\s*endcomment\s*%\}|\{#.*?#\}", re.S)


def _read(path: Path) -> str:
    return COMMENT.sub("", path.read_text(encoding="utf-8"))


def _product_templates() -> list[Path]:
    return sorted(p for p in TEMPLATES.rglob("*.html") if "dev" not in p.relative_to(TEMPLATES).parts)


def _submits_through_a_btn(attrs: str) -> bool:
    """A <button>'s attributes: a submit control (no type, or type="submit") must carry the class btn."""
    kind = re.search(r"""\btype=["']?([a-z]+)""", attrs)
    if kind and kind.group(1) in {"button", "reset"}:
        return True
    classes = re.search(r"""\bclass=["']([^"']*)["']""", attrs)
    return bool(classes) and "btn" in classes.group(1).split()


def _guarded_forms() -> list[tuple[Path, str]]:
    found = []
    for path in _product_templates():
        for match in GUARDED_FORM.finditer(_read(path)):
            found.append((path, match.group(1)))
    return found


def test_the_guarded_forms_are_found():
    names = {path.relative_to(TEMPLATES).as_posix() for path, _ in _guarded_forms()}
    assert {
        "accounts/profile.html",
        "accounts/delete_request.html",
        "allauth/elements/form.html",
        "allauth/elements/form__entrance.html",
    } <= names, names


def test_every_submit_control_of_a_guarded_form_is_a_btn():
    for path, body in _guarded_forms():
        sources = [(path, body)]
        for name in INCLUDE.findall(body):
            included = TEMPLATES / name
            if included.is_file():
                sources.append((included, _read(included)))
        for source, text in sources:
            where = f"{path.relative_to(TEMPLATES).as_posix()} (via {source.relative_to(TEMPLATES).as_posix()})"
            assert not SUBMIT_INPUT.search(text), f"{where}: an <input> submits a guarded form — use a button.btn"
            for attrs in BUTTON.findall(text):
                assert _submits_through_a_btn(attrs), f"{where}: <button{attrs}> submits a guarded form without .btn"


def test_allauth_submits_through_its_button_element_which_renders_a_btn():
    folder = TEMPLATES / "allauth" / "elements"
    elements = sorted([folder / "button.html", *folder.glob("button__*.html")])  # the element and its layout variants
    assert elements, "templates/allauth/elements/button.html is gone"
    for element in elements:
        buttons = BUTTON.findall(_read(element))
        assert buttons, f"{element.name} renders no <button>"
        for attrs in buttons:
            assert re.search(r'\bclass="btn\b', attrs), f"{element.name}: allauth's button element must render a .btn"
    assert ALLAUTH_TEMPLATES.is_dir(), ALLAUTH_TEMPLATES
    raw = []
    for path in sorted(ALLAUTH_TEMPLATES.rglob("*.html")):
        text = path.read_text(encoding="utf-8")
        if re.search(r"<button\b", text) or SUBMIT_INPUT.search(text):
            raw.append(path.relative_to(ALLAUTH_TEMPLATES).as_posix())
    assert not raw, f"allauth templates that submit with a raw control (not its button element): {raw}"
