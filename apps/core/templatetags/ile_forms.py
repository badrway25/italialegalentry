"""
The form system's template tags (V5.12 W2, lane B; DECISIONS §5 «Form system») — ``{% load ile_forms %}``.

{% field_ui field as ui %}   → what components/form_field.html needs to know about a BoundField: its kind (the
                               control it draws), whether it is optional (DECISIONS §5.3: the minority is marked,
                               never the required fields), its leading glyph, its character limit, whether the
                               combobox enhances it, and the server's own messages for the inline check
                               (``data-msg-*``, read by static/js/src/fieldcheck.js: the same words as the server's)
{% form_assets %}            → the field system's page-only sheet and script, ONCE per response: the first field a
                               page renders brings them, so a page without a form loads neither (DECISIONS §5.5:
                               «fieldcheck.js is loaded by form pages only»; budgets: form JS ≤ 6 KB gzip, a
                               page-only sheet ≤ 6 KB gzip; shared CSS only ratchets down). In a fragment
                               fetched by script (DOMParser, innerHTML) the module script is inert: its fields
                               submit and the server judges, but the inline check needs the host to import
                               fieldcheck.js and dispatch `fields:load` on the inserted root (fieldcheck.js head)
{{ field|choice_options }}   → the choices of a radio / checkbox group with the glyph and the description each may
                               carry (``field.field.choice_glyphs`` / ``choice_descriptions``, set by the form)

Nothing here changes what a form accepts: validation stays the server's (the summary and each field's error), the
inline check only says it earlier, in the server's words.
"""

from __future__ import annotations

from django import forms, template
from django.contrib.auth import password_validation
from django.core import validators
from django.templatetags.static import static
from django.utils import translation
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext

register = template.Library()

#: Above this many options a native select is enhanced by the combobox (DECISIONS §5.7; Combobox 34726).
COMBOBOX_MIN_OPTIONS = 16
#: The leading glyph of a field by its input type (DECISIONS §5.2, «a leading glyph slot»): what the value is.
LEADING_GLYPHS = {"email": "at-sign", "tel": "phone"}
#: A stand-in the length messages carry for the count the browser knows and the server does not.
COUNT = 987654321

KIND_HIDDEN = "hidden"
KIND_HONEYPOT = "honeypot"
KIND_CHECKBOX = "checkbox"
KIND_CHOICES = "choices"
KIND_SELECT = "select"
KIND_DATE = "date"
KIND_NUMBER = "number"
KIND_PASSWORD = "password"  # noqa: S105 - a widget kind, not a secret
KIND_TEXTAREA = "textarea"
KIND_FILE = "file"
KIND_TEXT = "text"


def field_kind(bound) -> str:
    field = bound.field
    widget = field.widget
    if bound.is_hidden:
        return KIND_HIDDEN
    if bound.name == "website_url":
        return KIND_HONEYPOT
    if isinstance(widget, (forms.RadioSelect, forms.CheckboxSelectMultiple)):
        return KIND_CHOICES
    input_type = getattr(widget, "input_type", "")
    if input_type == "checkbox":
        return KIND_CHECKBOX
    if isinstance(widget, forms.Select):
        return KIND_SELECT
    if isinstance(field, forms.DateField) or isinstance(widget, forms.DateInput) or input_type == "date":
        return KIND_DATE
    if isinstance(widget, forms.NumberInput) or input_type == "number":
        return KIND_NUMBER
    if input_type == "password":
        return KIND_PASSWORD
    if isinstance(widget, forms.Textarea):
        return KIND_TEXTAREA
    if input_type == "file":
        return KIND_FILE
    return KIND_TEXT


def _limit_message(validator, limit) -> str:
    """A length validator's own message, its limit said and the current count left as ``{n}`` for the script."""
    message = validator.message % {"limit_value": limit, "show_value": COUNT, "value": ""}
    return str(message).replace(f"{COUNT:,}", "{n}").replace(str(COUNT), "{n}")


def _messages(bound, kind: str) -> dict[str, str]:
    field = bound.field
    out: dict[str, str] = {}
    if field.required:
        out["required"] = str(field.error_messages.get("required", ""))
    for validator in field.validators:
        if isinstance(validator, validators.EmailValidator | validators.URLValidator):
            out["type"] = str(validator.message)
        elif isinstance(validator, validators.MaxLengthValidator):
            out["max"] = _limit_message(validator, validator.limit_value)
        elif isinstance(validator, validators.MinLengthValidator):
            out["min"] = _limit_message(validator, validator.limit_value)
        elif isinstance(validator, validators.MinValueValidator):
            out["low"] = str(validator.message % {"limit_value": validator.limit_value})
        elif isinstance(validator, validators.MaxValueValidator):
            out["high"] = str(validator.message % {"limit_value": validator.limit_value})
    invalid = field.error_messages.get("invalid")
    if invalid and kind in (KIND_DATE, KIND_NUMBER, KIND_TEXT):
        out.setdefault("type", str(invalid))
    return {k: v for k, v in out.items() if v}


#: The password rules the browser can verify as the person types (V5.15 W3, lane B; DECISIONS §5.11): the validator's
#: class name → the rule static/js/src/fieldcheck.js applies. The others (too similar to the person's details, too
#: common) are the server's alone: they are listed, and stay neutral until the server answers.
_LIVE_PASSWORD_RULES = {
    "MinimumLengthValidator": lambda v: f"min:{v.min_length}",
    "NumericPasswordValidator": lambda v: "notnumeric",
}


def password_rules(bound) -> list[dict]:
    """
    The live checklist of a NEW password (the field the person creates: ``autocomplete="new-password"``, and not its
    confirmation): each rule of AUTH_PASSWORD_VALIDATORS in the validators' own words (their help texts, as the
    server says them), with the rule the script can check live, or "" for a rule only the server can judge.
    """
    widget = bound.field.widget
    if widget.attrs.get("autocomplete") != "new-password" or bound.name.endswith("2"):
        return []
    out = []
    for validator in password_validation.get_default_password_validators():
        text = validator.get_help_text()
        make = _LIVE_PASSWORD_RULES.get(type(validator).__name__)
        out.append({"text": text, "rule": make(validator) if make else ""})
    return out


@register.simple_tag
def field_ui(bound) -> dict:
    field = bound.field
    widget = field.widget
    kind = field_kind(bound)
    attrs = widget.attrs
    options = len(list(getattr(widget, "choices", None) or [])) if kind == KIND_SELECT else 0
    max_length = getattr(field, "max_length", None) if kind == KIND_TEXTAREA else None
    match = ""
    if kind == KIND_PASSWORD and bound.name.endswith("2") and f"{bound.name[:-1]}1" in bound.form.fields:
        match = bound.form[f"{bound.name[:-1]}1"].auto_id
    return {
        "rules": (rules := password_rules(bound) if kind == KIND_PASSWORD else []),
        # round 1: the rules the browser verifies are the checklist; the ones the server alone judges are one quiet
        # note under it, without marks (a mark that never fills read as a requirement not met)
        "rules_live": [r for r in rules if r["rule"]],
        "rules_note": " ".join(str(r["text"]) for r in rules if not r["rule"]),
        "kind": kind,
        "optional": not field.required and kind not in (KIND_HIDDEN, KIND_HONEYPOT),
        "glyph": getattr(field, "glyph", None) or LEADING_GLYPHS.get(getattr(widget, "input_type", ""), ""),
        "readonly": bool(attrs.get("readonly")),
        "disabled": bool(field.disabled or attrs.get("disabled")),
        "count": max_length or 0,
        "combobox": options >= COMBOBOX_MIN_OPTIONS and not getattr(widget, "allow_multiple_selected", False),
        "messages": _messages(bound, kind),
        "match": match,
        "label_lang": getattr(field, "label_lang", ""),
    }


@register.simple_tag(takes_context=True)
def form_assets(context) -> str:
    """The sheet and the module of the field system, the first time a response asks for them; "" after."""
    request = context.get("request")
    if request is None or getattr(request, "_ile_form_assets", False):
        return ""
    request._ile_form_assets = True
    return format_html(
        '<link rel="stylesheet" href="{}"><script type="module" src="{}"></script>',
        static("css/dist/core/forms.css"),
        static("js/dist/fieldcheck.js"),
    )


@register.simple_tag(takes_context=True)
def steps_assets(context) -> str:
    """The steps' page-only sheet (core/steps.css: v5/_steps.css — the rails, the review, the navigation), once per
    response, from components/form_steps.html: only a form in steps carries it (V5.15 W3 round 2)."""
    request = context.get("request")
    if request is not None:
        if getattr(request, "_ile_steps_assets", False):
            return ""
        request._ile_steps_assets = True
    return format_html('<link rel="stylesheet" href="{}">', static("css/dist/core/steps.css"))


@register.simple_tag(takes_context=True)
def glyph_assets(context) -> str:
    """The glyph tile's page-only sheet (core/glyph.css: v5/_glyph.css, the empty state's tile and surface), once per
    response and never where the form system's sheet already carries it (V5.15 W3 round 1: out of main.css)."""
    request = context.get("request")
    if request is not None:
        if getattr(request, "_ile_glyph_assets", False) or getattr(request, "_ile_form_assets", False):
            return ""
        request._ile_glyph_assets = True
    return format_html('<link rel="stylesheet" href="{}">', static("css/dist/core/glyph.css"))


@register.filter
def choice_options(bound) -> list[dict]:
    """The group's options for components/choice_cards.html: the native subwidget, its glyph, its description."""
    glyphs = getattr(bound.field, "choice_glyphs", None) or {}
    descriptions = getattr(bound.field, "choice_descriptions", None) or {}
    out = []
    for sub in bound:
        value = str(sub.data.get("value", ""))
        out.append({"sub": sub, "glyph": glyphs.get(value, ""), "description": descriptions.get(value, "")})
    return out


def _fallback(text) -> str:
    """ "fr" when a team string is still its French source on a page in another language — the fallback says its
    language (WCAG 3.1.2; tests/i18n/test_page_integrity.py), as «facultatif» does — else ""."""
    if (translation.get_language() or "fr")[:2] == "fr":
        return ""
    with translation.override("fr"):
        source = str(text)
    return "fr" if str(text) == source else ""


def untranslated(msgid: str) -> bool:
    """True when ``msgid`` has no translation in the page's language (and the page is not French): its words on the
    page are the French source. ``gettext`` answers the msgid itself exactly when the catalogue has nothing for it
    (V5.15 W3 round 1: comparing the translated text with itself under French — as ``_fallback`` does for a lazy
    label — always said «fr», and an Arabic «بياناتكم» was laid out as French)."""
    if (translation.get_language() or "fr")[:2] == "fr":
        return False
    return gettext(msgid) == msgid


@register.simple_tag
def ui_lang(msgid: str) -> str:
    """`` lang="fr"`` for an element whose words are ``{% translate msgid %}`` while that msgid has no translation in
    the page's language (V5.15 W3, lane B: the formwork's new words, until lane D's catalogue pass); "" otherwise."""
    return mark_safe(' lang="fr"') if untranslated(msgid) else ""


@register.simple_tag
def msg_lang(name: str, msgid: str) -> str:
    """`` data-msg-<name>-lang="fr"`` beside a script's word (``data-msg-<name>``) still in its French source: the
    script writes the word and gives its node that language (static/js/src/steps.js); "" when it is translated."""
    return format_html(' data-msg-{}-lang="fr"', name) if untranslated(msgid) else ""


@register.simple_tag
def script_word(attr: str, msgid: str) -> str:
    """`` <attr>="<the word>"`` (and `` <attr>-lang="fr"`` while the word is still its French source) for a word a
    script writes (V5.15 W3, round 2). The word is ``gettext(msgid)`` itself, never ``{% translate %}``: the tag escapes
    ``%`` before its lookup, so a msgid with a placeholder («Étape %(n)s sur %(total)s») rendered its French source in
    every language while ``untranslated()`` (gettext) said «translated» and no lang was given (WCAG 3.1.2). One call
    answers the value and its language, so they can never disagree."""
    word = gettext(msgid)
    if untranslated(msgid):
        return format_html(' {}="{}" {}-lang="fr"', attr, word, attr)
    return format_html(' {}="{}"', attr, word)


@register.simple_tag
def form_steps(form) -> list[dict]:
    """
    The steps of a multi-step form (V5.15 W3, lane B; DECISIONS §5.12) — ``{% form_steps form as steps %}``.

    A form says its steps as ``steps = ((key, label, glyph, (field names…)), …)``, in the order it asks them; every
    visible field it does not name joins the last step, so no field is ever lost. Each step: ``key`` (the anchor,
    ``etape-<key>``), ``n`` (1-based), ``label``, ``lang`` ("fr" while the label is its French fallback), ``glyph``
    (a registry symbol or ""), ``fields`` (its BoundFields,
    in the form's own order) and ``errors`` (True when one of them came back with an error: the script opens the
    first such step) and ``minority`` ("required" when the step marks its required fields instead of its optional
    ones). With no ``steps`` the form has one step and the tag returns []. ALL the fields stay in the
    page: without script every step is a fieldset in sequence and the form is the same form (static/js/src/steps.js).
    """
    spec = getattr(form, "steps", None)
    if not spec:
        return []
    named: dict[str, int] = {}
    out = []
    for index, (key, label, glyph, names) in enumerate(spec):
        out.append(
            {
                "key": key,
                "n": index + 1,
                "label": label,
                "lang": _fallback(label),
                "glyph": glyph,
                "fields": [],
                "errors": False,
            }
        )
        for name in names:
            named[name] = index
    for bound in form.visible_fields():
        if field_kind(bound) == KIND_HONEYPOT:
            continue
        step = out[named.get(bound.name, len(out) - 1)]
        step["fields"].append(bound)
        step["errors"] = step["errors"] or bool(bound.errors)
    # the minority is marked PER STEP (DECISIONS §5.3; V5.15 W3 round 1): a step where the optional fields outnumber
    # the required ones tags its required fields («obligatoire») and leaves «facultatif» out — «Le besoin» of the
    # public form says its one required field, not its seven optional ones
    for step in out:
        asked = [b for b in step["fields"] if field_kind(b) not in (KIND_HIDDEN, KIND_CHECKBOX)]
        required = sum(1 for b in asked if b.field.required)
        step["minority"] = "required" if required and len(asked) - required > required else ""
    # round 2 (the composition): the fields as ROWS — two short fields the form pairs by meaning (``steps_pairs``,
    # only when they are next to each other in the prescribed order: a pair never reorders) share a row from a
    # measure wide enough; and a step the form names in ``steps_more`` gathers its trailing optional fields under a
    # quiet sub-head («Le besoin»: the one required field, then the seven details), never reordered either
    pairs = {frozenset(pair) for pair in getattr(form, "steps_pairs", ())}
    more = dict(getattr(form, "steps_more", {}))
    for step in out:
        rows: list[list] = []
        for bound in step["fields"]:
            if rows and len(rows[-1]) == 1 and frozenset((rows[-1][0].name, bound.name)) in pairs:
                rows[-1].append(bound)
            else:
                rows.append([bound])
        step["more"], step["more_label"], step["more_lang"] = [], "", ""
        if step["key"] in more:
            cut = len(rows)
            while cut > 0 and all(not b.field.required for b in rows[cut - 1]):
                cut -= 1
            if 0 < cut < len(rows) and len(rows) - cut >= 3:
                step["more"], rows = rows[cut:], rows[:cut]
                step["more_label"] = more[step["key"]]
                step["more_lang"] = _fallback(step["more_label"])
        step["rows"] = rows
    return out
