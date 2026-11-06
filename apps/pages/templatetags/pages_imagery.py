"""{% photo "<slot key>" [css_class] [variant="<name>"] [sizes="<sizes>"] %} — one V5 photograph, art-directed and
self-hosted (apps/pages/imagery.py).

V5.22: `variant` draws the frame as a V2 composition does (a named rendering of the slot: other ratios, other widths —
imagery.Slot.variants); `sizes` states the width the composition really draws, when it differs from the slot's. Both
are optional: without them the slot renders as it always has."""

from django import template
from django.utils.html import conditional_escape, format_html, format_html_join

from pages import imagery

register = template.Library()


@register.inclusion_tag("components/photo.html")
def photo(key: str, css_class: str = "", variant: str = "", sizes: str = ""):
    return {"p": imagery.picture(key, variant=variant, sizes=sizes), "css_class": css_class}


@register.simple_tag
def foto_scheda(key: str, variant: str = ""):
    """One rendering's data sheet for the imagery specimen board (development only, V5.22 lane M): a <dl> with the
    slot, its sizes, each ratio in art-direction order with its AVIF ladder (width, KB) and its ceiling, and the
    recorded redactions. Rendered here, escaped, so the board needs no partial of its own."""
    slot = imagery.rendering(key, variant)
    rec = imagery.record(slot)
    ceilings = rec.get("ceilings") or {}
    head = format_html(
        "<code>{}</code>{} · Pexels {}{}",
        slot.key,
        format_html(" · variante <code>{}</code>", variant) if variant else "",
        rec["pexels_id"],
        format_html(" · «{}»", slot.treatment) if slot.treatment else "",
    )
    rows = [format_html("<div><dt>slot</dt><dd>{}</dd></div>", head)]
    rows.append(format_html("<div><dt>sizes</dt><dd><code>{}</code></dd></div>", slot.sizes))
    for ratio in dict.fromkeys(r for r in (slot.ratio, slot.mid, slot.narrow) if r):
        avif = sorted(
            (f for f in rec["files"] if f["ratio"] == ratio and f["format"] == "avif"), key=lambda f: f["width"]
        )
        ladder = format_html_join(
            "",
            '<span class="spi-scheda__file">{} w · {} KB</span>',
            ((f["width"], round(f["bytes"] / 1024, 1)) for f in avif),
        )
        cap = (
            format_html(' <span class="spi-scheda__cap">tetto {} KB</span>', round(ceilings[ratio] / 1024))
            if ratio in ceilings
            else ""
        )
        rows.append(format_html("<div><dt>{}</dt><dd>{}{}</dd></div>", ratio.replace("x", ":"), ladder, cap))
    if rec["redactions"]:
        reasons = " · ".join(r["reason"] for r in rec["redactions"])
        rows.append(format_html("<div><dt>oscuramenti</dt><dd>{}</dd></div>", reasons))
    return format_html('<dl class="spi-scheda">{}</dl>', format_html_join("", "{}", ((r,) for r in rows)))


@register.filter
def fronte_name(name) -> str:
    """A name «HEAD — the rest» set in two weights in a head (the promoter on /agami/; round 1 of W3, v515-c-improve1):
    every character of the name is kept, in order — only two spans are added around its parts. The name is the
    association's Italian legal name in every language: each part is tagged lang="it" (WCAG 3.1.2) and isolated
    left-to-right, so on an Arabic page its dash stays before «Dialogo …», never after «APS» (round 2, MJ-2)."""
    text = str(name)
    head, sep, rest = text.partition(" — ")
    if not sep:
        return conditional_escape(text)
    return format_html(
        '<span class="fronte__name" lang="it" dir="ltr">{}</span> '
        '<span class="fronte__name-rest" lang="it" dir="ltr">— {}</span>',
        head,
        rest,
    )
