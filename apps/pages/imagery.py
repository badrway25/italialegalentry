"""The V5 photographs' slot registry (V5.12 DECISIONS §6; label v512-c-w2).

One significant image = one primary context (ASSET_USAGE_MATRIX rule 1): a slot names WHERE a frame appears, and a
frame appears in one slot only across the whole site (tests/compliance/test_imagery_v512.py enforces it, together with
the licence, the author, the forbidden-subject vocabulary and the file-name ban).

The files and their provenance come from tools/build_derivatives.py: static/img/v5/<family>/<slug>-<ratio>-<width>.
{avif,webp} and static/img/v5/<family>/PROVENANCE.json (licence, author, Pexels page, crops, redactions, bytes,
sha256). This module reads that file once per process; templates draw a slot with {% photo "<key>" %}
(pages_imagery), which renders templates/components/photo.html.

Art direction. A slot has its ratio on a wide screen (>= 64 rem) and, optionally, another on a narrow one: a 4:5
portrait beside a lead becomes a 3:2 band above it on a phone, where a portrait would push the page's words a whole
screen down.

Loading. `role` decides it: "lcp" — the landing's one LCP image, eager with fetchpriority=high (never more than one per
page: the test holds it); "body" and "band" — lazy, decoding async. Explicit width and height always (CLS 0).

Alt texts are French msgids (the catalogue's source language); lane D translates them. They describe what the frame
shows, never a place or a person it does not need (AUM rule 5): stock is never documentary.
No credit is rendered (V5.24 §2, label v524-px): the Pexels License requires no attribution, and provenance — licence,
author, page — is internal (PROVENANCE.json, `record()`, `provenance()`); the figure's `data-slot` points to it.

V5.22 (SECTION_SYSTEM_V2 §8; label v522-m-build):
- seven new frames, each in one slot: the home's masonry ground (`role="ground"`, decorative, desaturated in the file),
  Le projet's bound volumes (a D panorama: 21:9 from 64 rem, 16:9 from 48 rem — the `mid` ratio — 4:5 below), the
  four Parcours family frames (treatment «select»: black and white at rest, colour when the lane is chosen, hovered or
  focused) and Formation's first station (treatment «develop»);
- a slot may carry named VARIANTS: the same frame drawn by a V2 composition at other ratios and widths (the home
  pilot's full-height 2:3 panels, the ecosystem's 4:3 under its arch). A section adopts one with
  {% photo "<key>" "<class>" variant="<name>" %}; the default rendering stays the one today's page draws, so nothing
  changes on a page before its lane recomposes it;
- {% photo … sizes="…" %} lets a composition state the width it really draws, when it differs from the slot's.

V5.30 §8 (label v530-agami-build): THE PROMOTER'S OWN MARKS (MARKS, at the end) — AGAMI's official logo, framed and
seal forms, from static/brand/agami/PROVENANCE.json (tools/build_derivatives.py --marks). They are not photographs and
not stock: no slot, no crop, no grade, no licence of a third party and no credit; the stock invariants of SLOTS (the
Pexels licence, the author, one frame one slot) do not describe them, their own do
(tests/compliance/test_agami_assets_v530.py: AGAMI's own source, no metadata, no photograph of a person).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, replace
from functools import cache
from pathlib import Path

from django.conf import settings
from django.templatetags.static import static
from django.utils.translation import get_language, override
from django.utils.translation import gettext_lazy as _

V5_DIR = Path(settings.BASE_DIR) / "static" / "img" / "v5"
WIDE_MEDIA = "(min-width: 64rem)"
MID_MEDIA = "(min-width: 48rem)"
#: the Parcours family frames (V5.22, B «il tracciato»): 3/12 at the lane head from 64 rem; below, a 21:9 strip across
#: the page container, whose margins are 40 px from 48 rem, 24 px from 26.875 rem and 20 px below (tokens.css)
FAMILY_SIZES = (
    "(min-width: 64rem) 21vw, (min-width: 48rem) calc(100vw - 5rem), (min-width: 26.875rem) calc(100vw - 3rem), "
    "calc(100vw - 2.5rem)"
)


@dataclass(frozen=True)
class Variant:
    """The same frame, drawn by another composition (V5.22): its ratios and the width it really draws."""

    ratio: str  # from 64 rem
    narrow: str = ""  # below 64 rem (below 48 rem when `mid` is set)
    mid: str = ""  # from 48 to 64 rem
    sizes: str = "100vw"


@dataclass(frozen=True)
class Slot:
    key: str
    family: str
    slug: str
    ratio: str  # the ratio drawn on a wide screen (and everywhere when `narrow` is empty)
    alt: object  # a lazy msgid; "" for a decorative frame (never gettext("") — that is the catalogue's header)
    role: str = "body"  # lcp | head | body | band | ground — «head»: the second half of a head's diptych: eager (the
    # head is never masked, V5.15 round 1) but without fetchpriority (one LCP per page); «ground» (V5.22): a K band's
    # photographic ground, decorative (alt ""), lazy, no credit shown (V5.24 §2)
    narrow: str = ""  # the ratio drawn below 64 rem (below 48 rem when `mid` is set), if different
    sizes: str = "100vw"  # the drawn width, for the browser's choice among the widths
    pair: str = ""  # the slot key of a diptych's other half (both halves render together)
    treatment: str = ""  # "develop": B/W -> colour as it enters (data-grade="bw-scroll"); "bw": colour on
    # hover/focus (data-grade="bw") — lane A's _reveal.css draws both (W2 review M-3); "select" (V5.22 §8): black and
    # white at rest, colour when its lane is chosen, hovered or focused — the Parcours family frames (lane S draws it)
    mid: str = ""  # V5.22: the ratio drawn from 48 to 64 rem, if different (a panorama's 16:9)
    variants: tuple[tuple[str, Variant], ...] = ()  # V5.22: (name, Variant) — the same frame in a V2 composition


SLOTS: tuple[Slot, ...] = (
    # home — «Projet pilote»: the diptych «le même geste» (B/W -> colour as the band enters)
    Slot(
        "home.pilot.cedar",
        "pilote",
        "main-cedre-ciseau",
        "4x5",
        _("Une main guide un ciseau à bois dans une sculpture de cèdre aux motifs géométriques"),
        sizes="(min-width: 64rem) 17rem, 44vw",
        pair="home.pilot.marble",
        treatment="develop",
        # V5.22 §3.1 S4, the D panorama «lo stesso gesto»: a full-height 2:3 panel (about 30 % of the band, 82 vh,
        # drawn by `cover`: 34vw covers 30vw and 82vh x 2/3 from 1280 to 1920) and a 3:2 band on phones
        variants=(("pannello", Variant("2x3", narrow="3x2", sizes="(min-width: 64rem) 34vw, 100vw")),),
    ),
    Slot(
        "home.pilot.marble",
        "pilote",
        "main-marbre-ciseau",
        "4x5",
        _("Une main guide un ciseau sur un bloc de marbre"),
        sizes="(min-width: 64rem) 17rem, 44vw",
        pair="home.pilot.cedar",
        treatment="develop",
        variants=(("pannello", Variant("2x3", narrow="3x2", sizes="(min-width: 64rem) 34vw, 100vw")),),
    ),
    # home — «Un écosystème institutionnel»
    Slot(
        "home.ecosystem",
        "ecosysteme",
        "table-travail-institutions",
        "3x2",
        _("Autour d’une table de travail, des mains, des documents annotés et des micros de séance"),
        sizes="(min-width: 64rem) 36rem, 100vw",
        # V5.22 §3.1 S7, the A «campata, il colophon»: 4:3 under the arch on 7/12 bleeding to the viewport's edge
        # (57vw from 80 rem), 6/12 from 64 rem (the A anatomy), the 3:2 full width below
        variants=(
            (
                "campata",
                Variant("4x3", narrow="3x2", sizes="(min-width: 80rem) 57vw, (min-width: 64rem) 50vw, 100vw"),
            ),
        ),
    ),
    # the four landings: the LCP photograph beside the lead
    Slot(
        "pathways.hero",
        "personnes",
        "personne-fenetre-dos",
        "4x5",
        _("Une personne vue de dos, assise à son bureau devant une grande fenêtre"),
        role="lcp",
        narrow="3x2",
        sizes="(min-width: 80rem) 32rem, (min-width: 64rem) 38vw, 100vw",
    ),
    Slot(
        "companies.hero",
        "entreprises",
        "atelier-mesure-precision",
        "3x2",
        _("Dans un atelier, des mains mesurent une pièce au pied à coulisse"),
        role="lcp",
        sizes="(min-width: 80rem) 38rem, (min-width: 64rem) 46vw, 100vw",
    ),
    Slot(
        "institutions.hero",
        "institutions",
        "table-des-institutions",
        "4x5",
        _("Une table de séance vide : micros, écrans éteints et chevalets sans nom"),
        role="lcp",
        narrow="3x2",
        sizes="(min-width: 80rem) 32rem, (min-width: 64rem) 38vw, 100vw",
    ),
    Slot(
        "universities.hero",
        "universites",
        "bibliotheque-salle-lecture",
        "4x5",
        _("Une salle de lecture : bibliothèques vitrées, tables de bois et lumière des fenêtres"),
        role="lcp",
        narrow="3x2",
        sizes="(min-width: 80rem) 32rem, (min-width: 64rem) 38vw, 100vw",
    ),
    Slot(
        "universities.exchange",
        "universites",
        "etudiants-echange-campus",
        "3x2",
        _(
            "Deux personnes en conversation : l’une accompagne sa parole d’un geste de la main, l’autre tient une "
            "pochette contre elle"
        ),
        # 6/12 of the page container from 64 rem (today's «scambio» and U1's destination panel alike), the container's
        # width below — exact at each container step (tokens.css: the containers 1 440 / 1 320 / 1 176 px and 100 %
        # below 75 rem, the margins 40 px from 48 rem, 24 px from 26.875 rem, 20 px below; 12 columns, 24 px gutters:
        # 6/12 = (container − 80 − 11 × 24) / 2 + 5 × 24). Round 1: the real page's browser test found the 390 px frame
        # drawn 8 px wider than a 3 rem margin said, and 45vw exact only near 1 040 px (8 px short at 1 199), so the
        # phone step and calc(50vw - 3.25rem) are new, and the 1 440 container's track is 41.75 rem, not 42
        sizes=(
            "(min-width: 100rem) 41.75rem, (min-width: 90rem) 38rem, (min-width: 75rem) 33.5rem, "
            "(min-width: 64rem) calc(50vw - 3.25rem), (min-width: 48rem) calc(100vw - 5rem), "
            "(min-width: 26.875rem) calc(100vw - 3rem), calc(100vw - 2.5rem)"
        ),
    ),
    # ---- V5.15 W3 (label v515-c-build): the imagery pass — every important public page has its frame, one slot each.
    # The entrance frames are the page's LCP (one per page); the others are lazy and masked as they enter.
    Slot(
        "training.hero",
        "formation",
        "atelier-soudure-geste",
        "3x2",
        _("Dans un atelier de formation, une main tend la torche de soudage à une autre, au-dessus de l’étau"),
        role="lcp",
        sizes="(min-width: 80rem) 38rem, (min-width: 64rem) 46vw, 100vw",
    ),
    Slot(
        "training.after",
        "formation",
        "microscopes-rangee",
        "3x2",
        _("Une rangée de microscopes sur une paillasse claire"),
        sizes="(min-width: 80rem) 38rem, (min-width: 64rem) 40vw, 100vw",
        treatment="develop",
    ),
    Slot(
        "diplomas.hero",
        "diplomes",
        "classeur-documents-ouvert",
        "3x2",
        _("Un classeur à soufflets ouvert sur une table de bois, rempli de pièces rangées"),
        role="lcp",
        sizes="(min-width: 80rem) 38rem, (min-width: 64rem) 46vw, 100vw",
    ),
    Slot(
        "pilot.plain",
        "pilote",
        "plaine-peupliers-hiver",
        "4x5",
        _("Une rangée de peupliers nus au bord d’une plaine labourée, dans la brume"),
        role="lcp",
        sizes="(min-width: 80rem) 18.5rem, (min-width: 64rem) 22vw, 46vw",
        pair="pilot.fields",
    ),
    Slot(
        "pilot.fields",
        "pilote",
        "champs-montagnes-printemps",
        "4x5",
        _("Des champs en fleurs au pied d’une chaîne de montagnes enneigées"),
        role="head",
        sizes="(min-width: 80rem) 18.5rem, (min-width: 64rem) 22vw, 46vw",
        pair="pilot.plain",
    ),
    Slot(
        "project.hall",
        "projet",
        "grande-salle-etude",
        "3x2",
        _("Une grande salle d’étude vue depuis une galerie : verrières, longues tables, lustres"),
        role="lcp",
        sizes="(min-width: 80rem) 40rem, (min-width: 64rem) 48vw, 120vw",
    ),
    Slot(
        "network.table",
        "reseau",
        "table-commune-vue-haut",
        "3x2",
        _("Une longue table partagée vue d’en haut : ordinateurs, carnets, papiers"),
        role="lcp",
        sizes="(min-width: 80rem) 26rem, (min-width: 64rem) 30vw, 70vw",
    ),
    Slot(
        "living.street",
        "vivre",
        "rue-facades-couleurs",
        "21x9",
        _("Une rue de façades enduites aux couleurs chaudes, volets et balcons fleuris"),
        role="lcp",
        narrow="3x2",
        sizes="100vw",
    ),
    Slot(
        "contact.square",
        "contact",
        "place-civique-palais",
        "3x2",
        _("Une place pavée entre deux palais ; quelques passants s’éloignent"),
        role="lcp",
        sizes="(min-width: 80rem) 28rem, (min-width: 64rem) 33vw, 76vw",
    ),
    Slot(
        "companies.territory",
        "entreprises",
        "serres-plaine-crepuscule",
        "21x9",
        _("Des serres en tunnel à travers une plaine cultivée, au crépuscule"),
        role="band",
        sizes="100vw",
    ),
    Slot(
        "institutions.chamber",
        "institutions",
        "hemicycle-pupitres",
        "3x2",
        _("Les pupitres et les micros d’une salle d’assemblée, sièges vides"),
        sizes="(min-width: 64rem) 32rem, 100vw",
        treatment="develop",
    ),
    # ---- V5.22 (label v522-m-build; SECTION_SYSTEM_V2 §8.1): seven new frames, one slot each, all lazy (no new eager
    # image, §7.3). Their sizes are the V2 compositions' drawn widths (§2); a composition that draws another width
    # says so with {% photo … sizes="…" %}.
    Slot(
        "home.integrity.stone",
        "accueil",
        "pierre-appareillee",
        "21x9",
        "",  # decorative: the integrity band's ground under its 60 % stone veil; no caption (V5.24 §2)
        role="ground",
        narrow="4x5",
        sizes="100vw",
    ),
    Slot(
        "project.volumes",
        "projet",
        "codici-rilegati",
        "21x9",
        _(
            "Des volumes reliés en cuir, alignés sur un rayonnage : nervures et dorures des dos dans une lumière "
            "rasante"
        ),
        role="band",
        mid="16x9",
        narrow="4x5",
        # the D panorama drifts from 48 rem (M22: the image scaled 1.12 inside its full-bleed frame)
        sizes="(min-width: 48rem) 112vw, 100vw",
    ),
    Slot(
        "pathways.family.work",
        "personnes",
        "entrepot-allee-rayonnages",
        "3x2",
        _("Une allée d’entrepôt entre de hauts rayonnages chargés de cartons"),
        narrow="21x9",
        # B «il tracciato»: the frame at the lane head (3/12) from 64 rem; a 21:9 strip across the lane below
        sizes=FAMILY_SIZES,
        treatment="select",
    ),
    Slot(
        "pathways.family.study",
        "personnes",
        # round 1 (v522-m-improve1): at desk level and warm, instead of a second overhead tabletop beside «Famille»
        "notes-cahier-livre",
        "3x2",
        _("À une table de travail, une main prend des notes au stylo dans un cahier, devant un livre ouvert"),
        narrow="21x9",
        sizes=FAMILY_SIZES,
        treatment="select",
    ),
    Slot(
        "pathways.family.family",
        "personnes",
        # round 1 (v522-m-improve1): a shared table on an openwork wooden top, instead of the generic brunch table
        "table-partagee-vue-haut",
        "3x2",
        _(
            "Vue d’en haut, une table partagée : des mains se servent dans des bols d’olives et de tomates, sur un "
            "plateau de bois ajouré"
        ),
        narrow="21x9",
        sizes=FAMILY_SIZES,
        treatment="select",
    ),
    Slot(
        "pathways.family.other",
        "personnes",
        "vignes-brume-aube",
        "3x2",
        _("Des rangées de vignes dans la brume, au pied d’une ligne de collines"),
        narrow="21x9",
        sizes=FAMILY_SIZES,
        treatment="select",
    ),
    Slot(
        "training.before",
        "formation",
        "banc-electrique-mains",
        "4x5",
        _("Des mains câblent des contacteurs sur un tableau électrique, entre des goulottes bleues et des fils rouges"),
        narrow="3x2",
        # I «la traversata»: the first time's frame in its card (V5.30 VARIETY §7: the page passes its own sizes)
        sizes=(
            "(min-width: 90rem) 25rem, (min-width: 64rem) 28vw, (min-width: 48rem) 34rem, "
            "(min-width: 26.875rem) calc(100vw - 3rem), calc(100vw - 2.5rem)"
        ),
        treatment="develop",
    ),
)

BY_KEY = {s.key: s for s in SLOTS}


@cache
def provenance(family: str) -> dict:
    path = V5_DIR / family / "PROVENANCE.json"
    return {p["slug"]: p for p in json.loads(path.read_bytes().decode("utf-8"))["photos"]}


def record(slot: Slot) -> dict:
    """The frame's provenance record (licence, author, Pexels page, files)."""
    return provenance(slot.family)[slot.slug]


def _files(slot: Slot, ratio: str, fmt: str) -> list[dict]:
    return sorted(
        (f for f in record(slot)["files"] if f["ratio"] == ratio and f["format"] == fmt), key=lambda f: f["width"]
    )


def _srcset(slot: Slot, ratio: str, fmt: str) -> str:
    return ", ".join(
        f"{static('img/v5/' + slot.family + '/' + f['file'])} {f['width']:d}w" for f in _files(slot, ratio, fmt)
    )


def _box(slot: Slot, ratio: str) -> tuple[int, int]:
    first = (_files(slot, ratio, "webp") or _files(slot, ratio, "avif"))[0]
    return first["width"], first["height"]


@dataclass
class Picture:
    slot: Slot
    alt: str
    sources: list[dict] = field(default_factory=list)
    src: str = ""
    srcset: str = ""
    width: int = 0
    height: int = 0
    ratio: str = ""
    eager: bool = False
    head: bool = False  # a head's second frame: eager, never masked, no fetchpriority
    alt_lang: str = ""  # "fr" while the page's catalogue has no translation of the alt yet (WCAG 3.1.2)
    variant: str = ""  # V5.22: the named rendering a composition asked for ("" = the slot's default)


def rendering(key: str, variant: str = "", sizes: str = "") -> Slot:
    """The slot as a composition draws it: its default rendering, or a named variant (V5.22), with the width the
    composition really draws when it states one. An unknown variant is a KeyError: a template typo fails loudly."""
    slot = BY_KEY[key]
    if variant:
        v = dict(slot.variants)[variant]
        slot = replace(slot, ratio=v.ratio, narrow=v.narrow, mid=v.mid, sizes=v.sizes)
    if sizes:
        slot = replace(slot, sizes=sizes)
    return slot


def picture(key: str, variant: str = "", sizes: str = "") -> Picture:
    """Everything photo.html needs: the art-directed <source>s (AVIF then WebP; wide, then the 48–64 rem band when
    the slot has one, then narrow), the WebP <img>."""
    slot = rendering(key, variant, sizes)
    narrow = slot.narrow or slot.ratio
    sources = []
    bands = []
    if slot.narrow or slot.mid:
        bands.append((WIDE_MEDIA, slot.ratio))
        if slot.mid:
            bands.append((MID_MEDIA, slot.mid))
    for media, ratio in bands:
        w, h = _box(slot, ratio)
        sources += [
            {"type": "image/avif", "media": media, "srcset": _srcset(slot, ratio, "avif"), "width": w, "height": h},
            {"type": "image/webp", "media": media, "srcset": _srcset(slot, ratio, "webp"), "width": w, "height": h},
        ]
    w, h = _box(slot, narrow)
    sources.append(
        {"type": "image/avif", "media": "", "srcset": _srcset(slot, narrow, "avif"), "width": w, "height": h}
    )
    middle = next((f for f in _files(slot, narrow, "webp") if f["width"] >= 800), _files(slot, narrow, "webp")[-1])
    alt = str(slot.alt)
    # an alt the catalogue does not translate yet is the French source: it says so, so a screen reader reads it in
    # French and Arabic isolates it (the same rule as every other fallback text; D's catalogue pass removes it)
    alt_lang = ""
    if alt and get_language() not in (None, "fr"):
        with override("fr"):
            alt_lang = "fr" if alt == str(slot.alt) else ""
    return Picture(
        slot=slot,
        alt=alt,
        alt_lang=alt_lang,
        sources=sources,
        src=static(f"img/v5/{slot.family}/{middle['file']}"),
        srcset=_srcset(slot, narrow, "webp"),
        width=w,
        height=h,
        ratio=slot.ratio,
        eager=slot.role == "lcp",
        head=slot.role == "head",
        variant=variant,
    )


def all_files() -> list[Path]:
    """Every derivative a slot can serve (for the tests)."""
    out = []
    for slot in SLOTS:
        out += [V5_DIR / slot.family / f["file"] for f in record(slot)["files"]]
    return out


# ---- V5.30 §8 (label v530-agami-build): the promoter's own marks ----------------------------------------------------
BRAND_DIR = Path(settings.BASE_DIR) / "static" / "brand" / "agami"
#: the head's composed seat: the 6/12 track of the page container from 64 rem (the computation universities.exchange
#: used until V5.30, exact at each container step), the container's width below — the plate capped at 34 rem everywhere
#: (_agami.css)
SEAT_SIZES = (
    "(min-width: 90rem) 34rem, (min-width: 75rem) 33.5rem, (min-width: 64rem) calc(50vw - 3.25rem), "
    "(min-width: 39rem) 34rem, (min-width: 26.875rem) calc(100vw - 3rem), calc(100vw - 2.5rem)"
)


@dataclass(frozen=True)
class Mark:
    """One of AGAMI's marks as the page draws it: drawn whole (never cropped, graded, recoloured or mirrored)."""

    key: str
    slug: str
    alt: object  # a lazy msgid; "" for a mark set beside the words that already say it (decorative)
    sizes: str
    eager: bool = False  # the head's frame, the page's LCP candidate: eager with fetchpriority=high (one per page)


MARKS: tuple[Mark, ...] = (
    # the head's composed seat «l'insegna»: the official logo, framed, beside the promoter's name
    Mark(
        "agami.insegna",
        "agami-insegna",
        _(
            "Logo officiel d’AGAMI Research Center : une balance de la justice traversée par un ruban aux couleurs "
            "de l’Italie et du Maroc"
        ),
        sizes=SEAT_SIZES,
        eager=True,
    ),
    # the identification plate's seal: decorative, the plate's words name the association
    Mark("agami.sigillo", "agami-sigillo", "", sizes="5.5rem"),
)
MARKS_BY_KEY = {m.key: m for m in MARKS}


@cache
def mark_provenance() -> dict:
    path = BRAND_DIR / "PROVENANCE.json"
    return {m["slug"]: m for m in json.loads(path.read_bytes().decode("utf-8"))["marks"]}


def mark(key: str) -> dict:
    """Everything the page's mark partial needs: the AVIF and WebP sets, the WebP <img> (its middle width), the box, the
    alt in the page's language (marked French while the catalogue lacks it, as picture() does)."""
    m = MARKS_BY_KEY[key]
    files = mark_provenance()[m.slug]["files"]

    def srcset(fmt: str) -> str:
        chosen = sorted((f for f in files if f["format"] == fmt), key=lambda f: f["width"])
        return ", ".join(f"{static('brand/agami/' + f['file'])} {f['width']:d}w" for f in chosen)

    webp = sorted((f for f in files if f["format"] == "webp"), key=lambda f: f["width"])
    first = webp[0]
    middle = next((f for f in webp if f["width"] >= 800), webp[-1])
    alt = str(m.alt)
    alt_lang = ""
    if alt and get_language() not in (None, "fr"):
        with override("fr"):
            alt_lang = "fr" if alt == str(m.alt) else ""
    return {
        "key": m.key,
        "alt": alt,
        "alt_lang": alt_lang,
        "avif": srcset("avif"),
        "webp": srcset("webp"),
        "src": static(f"brand/agami/{middle['file']}"),
        "width": first["width"],
        "height": first["height"],
        "sizes": m.sizes,
        "eager": m.eager,
    }


def mark_files() -> list[Path]:
    """Every file a mark can serve (for the tests)."""
    return [BRAND_DIR / f["file"] for record in mark_provenance().values() for f in record["files"]]
