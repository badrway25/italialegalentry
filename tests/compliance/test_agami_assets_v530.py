"""
V5.30 §8 — the AGAMI page from VERIFIED material (the owner's final art direction, 7 Nov 2026; label v530-agami-build).

The page's real image is the promoter's own official logo (pages.imagery.MARKS, static/brand/agami, built by
tools/build_derivatives.py --marks): the framed form in the head's composed seat, the round seal on the identification
plate. What these tests hold:

  * the Q9 identification block is EXACTLY the owner's (V5.23): every field as he gave it, from its one source, and no other
    identifier on the page;
  * no AGAMI image carries metadata — EXIF, XMP, ICC, GPS — in its decoded image nor in its container;
  * no photograph of a person: the only AGAMI assets are the two logo forms from their two recorded sources (the AGAMI
    project's portraits are a third party's personal data; its round-table photographs show identifiable people — neither
    enters, docs/design-v5/QA/v530/agami/PROVENANCE.md), no file the provenance does not list, no portrait-shaped name;
  * the marks drawn whole, never mirrored (in Arabic too: the ribbon's national colours — V5.29, the owner's correction of
    6 Nov 13:12), each under its ceiling, never upscaled;
  * the page draws them as the composition says — the head's one LCP image, the seal lazy and decorative — with the role
    panel's verified facts (each backed by ILE's tracked copy), AGAMI's tagline and motto in the versions AGAMI publishes
    (agamieuromed.org, read 7 Nov 2026 — never a team translation) and the Italy + Morocco ground behind the ways on.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest
from bs4 import BeautifulSoup
from django.conf import settings
from django.utils.translation import gettext, override

from cms import locked_content
from pages import identity, imagery

pytestmark = [pytest.mark.compliance]

ROOT = Path(settings.BASE_DIR)
BRAND = ROOT / "static" / "brand" / "agami"
LANGS = ("fr", "it", "en", "ar")

#: the owner's Q9 decision A (V5.23, 30 Oct 2026), verbatim — the name's dash is typographic (the site's constant, a
#: locked string, sets it as an em dash: compared modulo the dash)
OWNER_Q9 = {
    "name": "AGAMI – Dialogo Giuridico Interculturale APS",
    "legal_form": "Associazione di Promozione Sociale (APS) / Ente del Terzo Settore",
    "tax_code": "91036640240",
    "runts": "Repertorio n. 149809",
    "registration": "Decreto Regione Veneto n. 11118 del 17/09/2025",
    "registered_office": "Via Sandrigo n. 29, 36061 Bassano del Grappa (VI), Italy",
    "operational_office": "Viale Giuseppe Mazzini 142, 00195 Roma, Italy",
    "contact": "contact@agamieuromed.org",
    "website": "agamieuromed.org",
}
#: AGAMI's own published wording (agamieuromed.org, its it/fr/en/ar home pages, 7 Nov 2026): the tagline under the name, the
#: motto over the ways on — the catalogue carries these four versions, never a team translation (the French guillemets
#: with no-break spaces: the same words)
TAGLINE = {
    "fr": "Du dialogue juridique à la coopération internationale",
    "it": "Dal dialogo giuridico alla cooperazione internazionale",
    "en": "From legal dialogue to international cooperation",
    "ar": "من الحوار القانوني إلى التعاون الدولي",
}
MOTTO = {
    "fr": "« Connaître ses racines pour construire des ponts entre les cultures, les ordres juridiques et les "
    "générations. »",
    "it": "«Conoscere le proprie radici per costruire ponti tra culture, ordinamenti e generazioni.»",
    "en": "“Knowing one's roots in order to build bridges between cultures, legal systems and generations.”",
    "ar": "«معرفة الجذور لبناء جسور بين الثقافات والأنظمة القانونية والأجيال.»",
}
#: the two marks, their two sources (inside the AGAMI website project) and their ceilings — held here, never read from the
#: provenance the builder writes (a recipe that raised its own ceiling would otherwise pass)
SOURCES = {
    "agami-insegna": "AGAMI website project, file foto/logo-agami2.png",
    "agami-sigillo": "AGAMI website project, file core/static/core/img/brand/agami-admin-logo.png",
}
CEILINGS = {"agami-insegna": 60 * 1024, "agami-sigillo": 30 * 1024}
LADDERS = {"agami-insegna": (480, 800, 1200, 1600), "agami-sigillo": (176, 264, 353)}
#: honorifics and words that name a portrait or the round table in a file name — the shape of what must never be shipped
PORTRAIT_SHAPES = re.compile(
    r"(^|[-_. ])(avv|dott|dottssa|dott\.ssa|ritratto|portrait|tavola[-_]?rotonda)([-_. ]|$)", re.I
)


def _provenance() -> dict:
    return json.loads((BRAND / "PROVENANCE.json").read_bytes().decode("utf-8"))


def _dash(text: str) -> str:
    return text.replace("—", "-").replace("–", "-")


# ---- the Q9 block: exactly the owner's ---------------------------------------------------------------------------------
def test_the_identification_source_holds_exactly_the_owner_s_fields():
    ident = identity.identification()
    assert set(ident) == {"name", "legal_form", "registers", "offices", "website"}
    assert _dash(ident["name"]) == _dash(OWNER_Q9["name"]) == _dash(settings.ILE["PROMOTER"])
    assert ident["legal_form"] == OWNER_Q9["legal_form"]
    assert [(r["key"], r["value"]) for r in ident["registers"]] == [
        ("tax-code", OWNER_Q9["tax_code"]),
        ("runts", OWNER_Q9["runts"]),
        ("registration", OWNER_Q9["registration"]),
    ]
    lines = []
    for office in ident["offices"]:
        a = office["address"]
        lines.append(
            f"{a['street']}, {a['postcode']} {a['town']}" + (f" ({a['province']})" if a["province"] else "") + ", Italy"
        )
    assert [o["key"] for o in ident["offices"]] == ["registered", "operational"]
    assert lines == [OWNER_Q9["registered_office"], OWNER_Q9["operational_office"]]
    assert ident["website"]["host"] == OWNER_Q9["website"]
    assert settings.ILE["PUBLIC_CONTACT_EMAIL"] == OWNER_Q9["contact"]


@pytest.mark.django_db
@pytest.mark.parametrize("lang", LANGS)
def test_the_plate_shows_the_owner_s_fields_and_no_other_identifier(client, seeded, phase3_open, lang):
    main = _main(client.get(f"/{lang}/agami/").content.decode())
    plate = main.select_one('section.agami-targa[data-ground="night"]')
    # seven labels: the three registers, the two offices, the official contact, the website — nothing else
    assert len(plate.select(".agami-id__voci dt")) == 5 and len(plate.select(".agami-id__contatto dt")) == 2
    values = [dd.get_text() for dd in plate.select(".agami-id__voci dd")]
    assert values[:3] == [OWNER_Q9["tax_code"], OWNER_Q9["runts"], OWNER_Q9["registration"]]
    if lang == "en":  # the owner wrote the offices in English: the English page reads them as he did
        assert values[3:] == [OWNER_Q9["registered_office"], OWNER_Q9["operational_office"]]
    assert _dash(plate.select_one(".agami-id__nome").get_text()) == _dash(OWNER_Q9["name"])
    assert plate.select_one(".agami-id__forma").get_text() == OWNER_Q9["legal_form"]
    assert plate.select_one('a.agami-id__indirizzo[href="mailto:contact@agamieuromed.org"]') is not None
    assert plate.select_one(".agami-id__sito").get_text(strip=True) == OWNER_Q9["website"]
    # «Do not invent or add other identifiers»: no VAT, chamber, certified mail, bank or telephone number on the page,
    # no other long number than the tax code, and every owner's code once (the tax code's own label is the catalogue's
    # «Code fiscal» — «Codice fiscale» on the Italian page)
    text = main.get_text(" ")
    for word in ("P.IVA", "Partita IVA", "VAT", "REA", "PEC", "IBAN"):
        assert not re.search(rf"\b{re.escape(word)}\b", text), word
    assert re.findall(r"\b\d{9,}\b", text) == [OWNER_Q9["tax_code"]]
    assert not re.search(r"\+\d{2}\s?\d|\b800\s?\d{3}\s?\d{3}\b", text), "no telephone number in the page's body"
    for once in (OWNER_Q9["tax_code"], OWNER_Q9["runts"], OWNER_Q9["registration"]):
        assert text.count(once) == 1, once


# ---- the assets: AGAMI's own marks, no metadata, no person ---------------------------------------------------------------
def _webp_chunks(data: bytes) -> list[str]:
    assert data[:4] == b"RIFF" and data[8:12] == b"WEBP"
    chunks, i = [], 12
    while i + 8 <= len(data):
        kind, size = data[i : i + 4].decode("latin-1"), int.from_bytes(data[i + 4 : i + 8], "little")
        chunks.append(kind)
        i += 8 + size + (size & 1)
    return chunks


def _boxes(data: bytes, start: int, end: int):
    i = start
    while i + 8 <= end:
        size, kind, head = int.from_bytes(data[i : i + 4], "big"), data[i + 4 : i + 8], 8
        if size == 1:
            size, head = int.from_bytes(data[i + 8 : i + 16], "big"), 16
        elif size == 0:
            size = end - i
        yield kind, i + head, i + size
        i += size


def _avif_items_and_colours(data: bytes) -> tuple[list[bytes], list[bytes]]:
    """The item types of the AVIF's `meta`/`iinf` (an EXIF block is an «Exif» item, XMP a «mime» item) and the colour types
    of its `iprp`/`ipco`/`colr` boxes (an ICC profile is «prof» or «rICC»; «nclx» is the plain colour description)."""
    items, colours = [], []
    for kind, body, end in _boxes(data, 0, len(data)):
        if kind != b"meta":
            continue
        for sub, sbody, send in _boxes(data, body + 4, end):  # meta is a full box: version + flags
            if sub == b"iinf":
                version = data[sbody]
                first = sbody + 4 + (2 if version == 0 else 4)
                for infe, ibody, _iend in _boxes(data, first, send):
                    if infe == b"infe" and data[ibody] >= 2:
                        id_len = 2 if data[ibody] == 2 else 4
                        at = ibody + 4 + id_len + 2
                        items.append(data[at : at + 4])
            if sub == b"iprp":
                for ipco, pbody, pend in _boxes(data, sbody, send):
                    if ipco == b"ipco":
                        for prop, cbody, _cend in _boxes(data, pbody, pend):
                            if prop == b"colr":
                                colours.append(data[cbody : cbody + 4])
    return items, colours


def test_every_agami_file_is_listed_and_the_listed_files_are_exactly_the_two_logo_forms():
    doc = _provenance()
    marks = {m["slug"]: m for m in doc["marks"]}
    assert set(marks) == set(SOURCES) == {m.slug for m in imagery.MARKS}
    on_disk = {p.name for p in BRAND.iterdir() if p.is_file()} - {"PROVENANCE.json"}
    listed = {f["file"] for m in marks.values() for f in m["files"]}
    assert on_disk == listed, sorted(on_disk ^ listed)
    for slug, record in marks.items():
        # the promoter's own published logo, from its recorded source — never a photograph, never a third party's
        assert record["kind"] == "logo", slug
        assert record["source"] == SOURCES[slug], (slug, record["source"])
        assert record["published"].startswith("https://agamieuromed.org/"), slug
        assert record["rights"].startswith("AGAMI's own published institutional asset"), slug
        assert "foto/" not in record["source"] or record["source"].endswith("foto/logo-agami2.png"), slug


def test_no_portrait_and_no_round_table_photograph_enters_the_static_tree_or_a_template():
    """The AGAMI project's foto/ folder holds the portraits of named professionals (a third party's personal data) and the
    round-table photographs (identifiable people): by shape, no file of the static tree carries such a name, and no template
    points into the project's folders or the people's media."""
    names = [p.name for p in (ROOT / "static").rglob("*") if p.is_file() and "dist" not in p.parts]
    assert not [n for n in names if PORTRAIT_SHAPES.search(Path(n).stem)]
    for template in (ROOT / "templates").rglob("*.html"):
        text = template.read_bytes().decode("utf-8")
        assert "/media/people" not in text and "foto/" not in text, template


@pytest.mark.parametrize("path", imagery.mark_files(), ids=lambda p: p.name)
def test_no_agami_image_carries_exif_xmp_icc_or_gps(path):
    from PIL import Image

    data = path.read_bytes()
    with Image.open(path) as im:
        im.load()
        assert not {"exif", "xmp", "XML:com.adobe.xmp", "icc_profile"} & set(im.info), (path.name, sorted(im.info))
        exif = im.getexif()
        assert len(exif) == 0 and not exif.get_ifd(0x8825), path.name  # no EXIF tag, no GPS IFD
    for marker in (b"Exif\x00\x00", b"<x:xmpmeta", b"http://ns.adobe.com/xap/", b"rdf:RDF"):
        assert marker not in data, (path.name, marker)
    if path.suffix == ".webp":
        assert set(_webp_chunks(data)) <= {"VP8 ", "VP8L", "VP8X", "ALPH"}, (path.name, _webp_chunks(data))
    else:
        items, colours = _avif_items_and_colours(data)
        assert items and b"Exif" not in items and b"mime" not in items, (path.name, items)
        assert not {b"prof", b"rICC"} & set(colours), (path.name, colours)


def test_the_marks_hold_their_ceilings_never_upscaled_and_both_formats_at_every_width():
    for record in _provenance()["marks"]:
        slug, files = record["slug"], record["files"]
        assert record["ceiling"] == CEILINGS[slug], slug
        for fmt in ("avif", "webp"):
            widths = tuple(
                f["width"] for f in sorted((f for f in files if f["format"] == fmt), key=lambda f: f["width"])
            )
            assert widths == LADDERS[slug], (slug, fmt, widths)
        for f in files:
            assert f["bytes"] <= CEILINGS[slug], (f["file"], f["bytes"])
            assert (BRAND / f["file"]).stat().st_size == f["bytes"], f["file"]
            assert f["width"] <= record["original_px"][0], f["file"]


def test_the_marks_are_drawn_whole_and_never_mirrored():
    """A mark is never cropped (its box is the original's ratio at every width) nor mirrored by a sheet: no flip on the seat,
    the plate, the seal or their images, in either direction."""
    for record in _provenance()["marks"]:
        w0, h0 = record["original_px"]
        for f in record["files"]:
            assert abs(f["height"] - round(f["width"] * h0 / w0)) <= 1, f["file"]
    css = re.sub(
        r"/\*.*?\*/", "", (ROOT / "apps/pages/static/pages/css/_agami.css").read_bytes().decode("utf-8"), flags=re.S
    )
    for rule in re.findall(r"([^{}]*agami-(?:insegna|id__sigillo)[^{}]*)\{([^}]*)\}", css):
        body = rule[1]
        assert not re.search(r"scale\s*:\s*-1|scaleX\(\s*-1|scale\(\s*-1|rotateY\(\s*180", body), rule


# ---- the page draws them as the composition says --------------------------------------------------------------------------
def _main(html: str) -> BeautifulSoup:
    return BeautifulSoup(html.split('<main id="main-content"', 1)[1].split("</main>", 1)[0], "html.parser")


@pytest.mark.django_db
@pytest.mark.parametrize("lang", LANGS)
def test_the_head_seat_draws_the_official_logo_as_the_page_s_one_lcp_image(client, seeded, phase3_open, lang):
    main = _main(client.get(f"/{lang}/agami/").content.decode())
    head = main.select_one('header.ingresso[data-compose="name"]')
    seat = head.select_one(".ingresso__aside > .agami-insegna > picture.agami-insegna__logo[data-mark='agami.insegna']")
    assert seat is not None
    sources = seat.select("source")
    assert [s["type"] for s in sources] == ["image/avif", "image/webp"]
    assert all(
        "/static/brand/agami/agami-insegna-" in s["srcset"] and s.get("width") and s.get("height") for s in sources
    )
    img = seat.select_one("img")
    assert (
        img["width"] == "480" and img["height"] == "160" and img["fetchpriority"] == "high" and not img.get("loading")
    )
    assert str(main).count('fetchpriority="high"') == 1
    with override(lang):
        assert img["alt"] == gettext(str(imagery.MARKS_BY_KEY["agami.insegna"].alt)) and img["alt"].strip()
    assert not img.get("lang"), "the alt is translated in every language"
    # the seat composes the head: no library photograph, no figure, and the head's lead is AGAMI's tagline as it publishes it
    assert head.select_one("figure") is None
    assert head.select_one(".ingresso__lead").get_text() == TAGLINE[lang]


@pytest.mark.django_db
@pytest.mark.parametrize("lang", LANGS)
def test_the_identity_band_holds_the_role_panel_of_verified_facts_and_no_drawing(client, seeded, phase3_open, lang):
    main = _main(client.get(f"/{lang}/agami/").content.decode())
    band = main.select_one('section.agami-identita[data-sec="campata"][data-ground="stone"]')
    plate = band.select_one('.agami-identita__lastra[data-verb~="mask"]')
    assert plate is not None and not band.select("svg"), "the drawn colonnade is retired: the band draws nothing"
    entries = plate.select("dl.agami-breve > .agami-breve__voce")
    assert len(entries) == 3
    with override(lang):
        labels = [gettext("Promoteur de"), gettext("Dialogue juridique"), gettext("Active depuis")]
        values = [
            [settings.ILE["PROJECT_NAME"], gettext("Forum Vénétie–Maroc")],
            [f"{gettext('Italie')} – {gettext('Maroc')}"],
            ["2011"],
        ]
    assert [e.select_one("dt").get_text() for e in entries] == labels
    assert [[v.get_text() for v in e.select("dd .agami-breve__valore")] for e in entries] == values
    assert entries[0].select_one("bdi") is not None, "the project's name isolated: its ™ stays at its end in Arabic"
    # each fact is ILE's tracked copy: the prescribed promoter text and FAQ answer say it (French sources)
    who = locked_content.get("p2.forum.who.body", "fr")[0]
    faq = next(i for i in locked_content.get("p3.faq.items", "fr")[0] if i["key"] == "faq_who")["answer"]
    assert "Le Forum est promu par AGAMI" in who and "depuis 2011" in who and "l’Italie et le Maroc" in who
    assert "Le projet est promu par AGAMI" in faq


@pytest.mark.django_db
@pytest.mark.parametrize("lang", LANGS)
def test_the_plate_s_seal_is_decorative_and_lazy_and_the_ways_on_stand_on_the_italy_morocco_ground(
    client, seeded, phase3_open, lang
):
    main = _main(client.get(f"/{lang}/agami/").content.decode())
    seal = main.select_one(
        "section.agami-targa .agami-id__testata > picture.agami-id__sigillo[data-mark='agami.sigillo'] img"
    )
    assert seal is not None and seal["alt"] == "" and seal["loading"] == "lazy" and not seal.get("fetchpriority")
    band = main.select_one('section.agami-approdo[data-sec="approdo"][data-ground="stone"]')
    ground = band.select_one(":scope > .intesa[data-intesa][aria-hidden='true']")
    assert ground is not None and ground.select_one("svg[data-flag='it']") and ground.select_one("svg[data-flag='ma']")
    assert band.select_one(".approdo__fondale") is None, "no drawn bookend: the ground is the band's one motif"
    assert band.select_one(".testa__lead").get_text() == MOTTO[lang]
    hrefs = [a["href"] for a in band.select("a.approdo__link")]
    assert hrefs[:2] == [f"/{lang}/le-projet/", f"/{lang}/reseau/"] and f"/{lang}/forum/" in hrefs, hrefs
