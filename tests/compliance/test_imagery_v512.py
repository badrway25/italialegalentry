"""
V5.12 §9 / DECISIONS §6 (W2-C): the V5 photographs — one frame, one context; licensed, credited, self-hosted, light.

Every slot of ``pages.imagery`` is checked against its family's PROVENANCE.json (written by
tools/build_derivatives.py): the Pexels licence and author, the forbidden-subject vocabulary and the file-name ban of
docs/IMAGE_LICENSES.md, each frame in ONE slot across the whole site (the hero's and the portico's families included),
the files on disk with their recorded hash, and the weight budget of the files a 1x desktop and a 3x phone take.
The landings draw one LCP image (eager, fetchpriority=high) and nothing else eager; every other frame is lazy.

V5.22 (SECTION_SYSTEM_V2 §7.3, §8; label v522-m-build) adds, for the seven new frames and the four re-crops: each
kind's ceiling on EVERY width it can serve (the largest served AVIF), the ladders' tops, no new eager image, black and
white only where §8 puts it (the hero, «select», «develop») and the ground desaturated in the file, the named
variants and the 48–64 rem band, the full-resolution check's findings held as invariants (every crop clear of the
titles, faces and covers it was cut to avoid), no frame twice anywhere (by id AND by the original's hash), and the
register rows — with no person's name copied into them (§8 «No person's name is copied into any other document»).

V5.24 §2 (2 Nov 2026; FINAL_DELIVERY_V2.md §3.2, lane v524-px): the credit is no longer RENDERED — the Pexels License
requires no attribution and the owner wants no stock label on the product — but it stays RECORDED: the licence,
author and page checks below are unchanged, and the two tests that asserted the caption now assert its absence
(the same invariant on the record, a stronger one on the markup).
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import pytest
from django.conf import settings

from cms.seeds_media import FORBIDDEN_SUBJECT_KEYWORDS
from pages import imagery

pytestmark = [pytest.mark.compliance]

STATIC_IMG = Path(settings.BASE_DIR) / "static" / "img"
NAME_BAN = ("veneto", "rovigo", "regione", "comune", "logo")
LIMITS = {"lcp": 60 * 1024, "body": 45 * 1024, "band": 60 * 1024}


def test_every_slot_is_licensed_and_its_author_recorded():
    """The record of every slot: licence, author, Pexels page (V5.24 §2: recorded, never rendered). The Pexels License
    is the only licence the slot pipeline admits — an attribution-required frame cannot enter it unnoticed
    (IMAGE_LICENSES.md §1.10)."""
    for slot in imagery.SLOTS:
        rec = imagery.record(slot)
        assert rec["license"].startswith("Pexels License"), slot.key
        assert rec["photographer"] and "unavailable" not in rec["photographer"], slot.key
        assert rec["page"].startswith("https://www.pexels.com/photo/"), slot.key
        assert str(rec["pexels_id"]) in rec["page"], slot.key
        assert rec["files"], slot.key


def test_no_forbidden_subject_in_a_slug_or_an_alt():
    for slot in imagery.SLOTS:
        for text in (slot.slug, slot.family, str(slot.alt)):
            hits = [k for k in FORBIDDEN_SUBJECT_KEYWORDS if k in text.lower()]
            assert not hits, (slot.key, text, hits)


def test_no_banned_word_in_a_file_name():
    names = [p.name.lower() for p in (STATIC_IMG / "v5").rglob("*") if p.is_file()]
    assert names
    assert not [n for n in names if any(word in n for word in NAME_BAN)]


def test_each_frame_appears_in_one_slot_across_the_site():
    """A diptych is two frames; a frame is never a second slot's, nor the hero's or the portico's (AUM rule 1)."""
    seen: dict[int, str] = {}
    for slot in imagery.SLOTS:
        pid = imagery.record(slot)["pexels_id"]
        assert pid not in seen, f"frame {pid} in {seen.get(pid)} and {slot.key}"
        seen[pid] = slot.key
    for other in (STATIC_IMG / "photos" / "hero" / "PROVENANCE.json", STATIC_IMG / "portico" / "PROVENANCE.json"):
        doc = json.loads(other.read_bytes().decode("utf-8"))
        for photo in doc.get("photos") or doc.get("files"):
            assert photo["pexels_id"] not in seen, (other.parent.name, photo["pexels_id"], seen.get(photo["pexels_id"]))


def test_every_slot_key_is_unique_and_pairs_point_both_ways():
    keys = [s.key for s in imagery.SLOTS]
    assert len(keys) == len(set(keys))
    for slot in imagery.SLOTS:
        if slot.pair:
            assert imagery.BY_KEY[slot.pair].pair == slot.key


def test_the_files_exist_with_their_recorded_hash():
    for slot in imagery.SLOTS:
        for f in imagery.record(slot)["files"]:
            path = imagery.V5_DIR / slot.family / f["file"]
            assert path.exists(), path
            assert hashlib.sha256(path.read_bytes()).hexdigest() == f["sha256"], path


#: V5.20 strict rule, cited (QA round 1, M1; label v522-m-improve1). The ONLY renderings that leave DECISIONS §6's
#: assertions in test_the_weights_hold_their_budget, and only for the ONE assertion that their kind, as SECTION_SYSTEM_V2
#: §7.3 (an approved product decision, V5.22) sets it, contradicts. Each is held on EVERY width, AVIF and WebP alike
#: (the same ceiling, no allowance), by test_v522_every_new_frame_holds_its_kind_ceiling_on_every_width.
#: (slug, ratio) -> the §7.3 kind and why the V5.12 assertion cannot describe it
OWN_CEILING_V522 = {
    ("main-cedre-ciseau", "2x3"): "§7.3 «2:3 pilot panel ≤ 60 KB at 1 600 w», above the body's 45 KB",
    ("main-marbre-ciseau", "2x3"): "§7.3 «2:3 pilot panel ≤ 60 KB at 1 600 w», above the body's 45 KB",
    ("pierre-appareillee", "4x5"): "§7.3 «Ground (K) ≤ 40 KB (4:5 at 800 w)», a role DECISIONS §6 has no limit for",
}
OWN_LADDER_V522 = {
    (slug, ratio): "§7.3 «Family frame (B) ≤ 30 KB at 720 w»: the ladder ends at 720 w (the 21:9 strip at 1 200 w)"
    for slug in ("entrepot-allee-rayonnages", "notes-cahier-livre", "table-partagee-vue-haut", "vignes-brume-aube")
    for ratio in ("3x2", "21x9")
}


def test_the_weights_hold_their_budget():
    """DECISIONS §6: LCP <= 60 KB, body <= 45 KB, 21:9 band <= 60 KB, on the widths a 1x desktop and a 3x phone take.

    V5.20 strict rule, cited (V5.22, SECTION_SYSTEM_V2 §7.3; QA round 1 M1, label v522-m-improve1): the assertions are
    the V5.12 ones, unchanged. A rendering leaves ONE of them only when it is listed in OWN_CEILING_V522 (its §7.3 kind
    sets another limit: the 2:3 pilot panel, the ground's 4:5) or OWN_LADDER_V522 (its §7.3 kind ends its ladder at
    720 w: the family frames) — and is then held on every width, AVIF and WebP alike, by
    test_v522_every_new_frame_holds_its_kind_ceiling_on_every_width. Every other file is held here exactly as before,
    in both formats: every V5.12 and V5.15 file, universities.exchange's re-cut 3:2 (a V5.12 slot and ratio) included,
    and every other V5.22 rendering (the bench, the volumes, the stone's 21:9, the ecosystem's 4:3, the cedar's and the
    marble's 3:2)."""
    for slot in imagery.SLOTS:
        rec = imagery.record(slot)
        for f in rec["files"]:
            if f["budget"] and (rec["slug"], f["ratio"]) not in OWN_CEILING_V522:
                limit = LIMITS["band"] if f["ratio"] == "21x9" else LIMITS[rec["role"]]
                assert f["bytes"] <= limit, (f["file"], f["bytes"], limit)
        # the AVIF and WebP a 1x desktop takes (the 480 and the 800 of each ratio) are always budgeted — for a 21:9
        # band, drawn full width, the 1200 and the 1600 (V5.15 W3: the first 21:9 slots; a phone takes its narrow
        # ratio, or the 1200 at 3x)
        budgeted = {(f["ratio"], f["width"]) for f in rec["files"] if f["budget"]}
        for ratio in {f["ratio"] for f in rec["files"]}:
            if (rec["slug"], ratio) in OWN_LADDER_V522:
                continue
            widths = (1200, 1600) if ratio == "21x9" else (480, 800)
            assert all((ratio, w) in budgeted for w in widths), (slot.key, ratio)


def test_the_picture_carries_both_formats_and_explicit_dimensions():
    for slot in imagery.SLOTS:
        pic = imagery.picture(slot.key)
        assert pic.width and pic.height
        types = [s["type"] for s in pic.sources]
        assert "image/avif" in types
        assert pic.srcset.count(".webp") >= 2
        if slot.narrow:
            assert any(s["media"] for s in pic.sources), slot.key
        assert pic.eager == (slot.role == "lcp")


@pytest.mark.django_db
@pytest.mark.parametrize(
    "path, slot",
    [
        ("/fr/institutions/", "institutions.hero"),
        ("/fr/universites-et-formation/", "universities.hero"),
        ("/fr/entreprises/", "companies.hero"),
        # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026: the person
        # door's head draws no photograph (lane B: its seat is the questionnaire's panel; the frame it drew is the
        # qualified-work pathway's, shown by the explorer) — no LCP image there at all, every image of the page lazy
        # and sized (its LCP is its words)
        ("/fr/parcours/", None),
    ],
)
def test_a_landing_draws_one_lcp_image_and_lazy_others(client, seeded, phase3_open, path, slot):
    response = client.get(path)
    assert response.status_code == 200
    main = response.content.decode().split('<main id="main-content"', 1)[1].split("</main>", 1)[0]
    if slot is None:
        images = re.findall(r"<img [^>]*>", main)
        assert images and 'fetchpriority="high"' not in main
        assert all('loading="lazy"' in img and re.search(r'width="\d+" height="\d+"', img) for img in images)
        assert "images.pexels.com" not in main
        return
    assert f'data-slot="{slot}"' in main
    assert main.count('fetchpriority="high"') == 1
    figures = re.findall(r'<figure class="foto[^"]*"[^>]*>.*?</figure>', main, flags=re.S)
    assert figures
    for fig in figures:
        assert re.search(r'<img [^>]*width="\d+" height="\d+"', fig), fig[:200]
        if f'data-slot="{slot}"' not in fig:
            assert 'loading="lazy"' in fig
    # self-hosted only
    assert "images.pexels.com" not in main


@pytest.mark.django_db
def test_the_home_draws_the_diptych_and_the_ecosystem_frame_lazily(client, seeded, phase3_open):
    html = client.get("/fr/").content.decode()
    for slot in ("home.pilot.cedar", "home.pilot.marble", "home.ecosystem"):
        fig = re.search(rf'<figure [^>]*data-slot="{re.escape(slot)}".*?</figure>', html, flags=re.S)
        assert fig, slot
        assert 'loading="lazy"' in fig.group(0) and 'fetchpriority="high"' not in fig.group(0)
    # one B/W mechanism (lane A's data-grade, the W2 review's M-3): the diptych alone; every body frame is masked
    assert html.count('data-grade="bw-scroll"') == 2
    assert "foto--develop" not in html


# --------------------------------------------------------------------------------------------- V5.22 (lane M)

KB = 1024
#: SECTION_SYSTEM_V2 §7.3: each kind's ceiling on the largest served AVIF — held here, never read from the provenance
#: the builder writes (a recipe that raised its own ceiling would otherwise pass). (slot, variant) -> {ratio: bytes}
CEILINGS_V522 = {
    ("home.integrity.stone", ""): {"21x9": 60 * KB, "4x5": 40 * KB},
    ("project.volumes", ""): {"21x9": 60 * KB, "16x9": 60 * KB, "4x5": 45 * KB},
    ("pathways.family.work", ""): {"3x2": 30 * KB, "21x9": 30 * KB},
    ("pathways.family.study", ""): {"3x2": 30 * KB, "21x9": 30 * KB},
    ("pathways.family.family", ""): {"3x2": 30 * KB, "21x9": 30 * KB},
    ("pathways.family.other", ""): {"3x2": 30 * KB, "21x9": 30 * KB},
    ("training.before", ""): {"4x5": 45 * KB, "3x2": 45 * KB},
    ("home.pilot.cedar", "pannello"): {"2x3": 60 * KB, "3x2": 45 * KB},
    ("home.pilot.marble", "pannello"): {"2x3": 60 * KB, "3x2": 45 * KB},
    ("home.ecosystem", "campata"): {"4x3": 45 * KB},
    ("universities.exchange", ""): {"3x2": 45 * KB},
}
#: the tops of the ladders §7.3 names: the family frame at 720 w (its 21:9 strip at 1 200 w for 3x phones and tablets,
#: under the same 30 KB), the ground's 4:5 at 800 w, the pilot panel at 1 600 w, a band or panorama at 1 920 w
LADDER_TOPS = {
    ("home.integrity.stone", "21x9"): 1920,
    ("home.integrity.stone", "4x5"): 800,
    ("project.volumes", "21x9"): 1920,
    ("pathways.family.work", "3x2"): 720,
    ("pathways.family.study", "3x2"): 720,
    ("pathways.family.family", "3x2"): 720,
    ("pathways.family.other", "3x2"): 720,
    ("home.pilot.cedar", "2x3"): 1600,
    ("home.pilot.marble", "2x3"): 1600,
}
NEW_V522 = (
    "home.integrity.stone",
    "project.volumes",
    "pathways.family.work",
    "pathways.family.study",
    "pathways.family.family",
    "pathways.family.other",
    "training.before",
)
VARIANTS_V522 = (("home.pilot.cedar", "pannello"), ("home.pilot.marble", "pannello"), ("home.ecosystem", "campata"))


def _v522_files(key: str, variant: str) -> dict[str, list[dict]]:
    slot = imagery.rendering(key, variant)
    rec = imagery.record(slot)
    ratios = {slot.ratio, slot.narrow or slot.ratio} | ({slot.mid} if slot.mid else set())
    return {r: [f for f in rec["files"] if f["ratio"] == r] for r in ratios}


def test_v522_every_new_frame_holds_its_kind_ceiling_on_every_width():
    """§7.3 «Ceiling (largest served AVIF)»: every AVIF a V5.22 rendering can serve is under its kind's ceiling, and
    every WebP fallback under the SAME ceiling (QA round 1, M1: §7.3 records no allowance for the fallback, so none is
    granted; a WebP width that cannot fit at q 40 is not built and is listed in `webp_not_built`). The provenance
    records the same ceilings (none raised silently) and no allowance."""
    for (key, variant), ceilings in CEILINGS_V522.items():
        files = _v522_files(key, variant)
        # a new slot is governed whole; a variant may keep a V5.12 ratio (the ecosystem's 3:2, test above)
        assert set(ceilings) <= set(files), (key, variant, set(files), set(ceilings))
        if key in NEW_V522:
            assert set(files) == set(ceilings), (key, set(files), set(ceilings))
        for ratio, ceiling in ceilings.items():
            avif = [f for f in files[ratio] if f["format"] == "avif"]
            webp = [f for f in files[ratio] if f["format"] == "webp"]
            assert len(avif) >= 2 and webp, (key, ratio)
            assert {f["width"] for f in webp} <= {f["width"] for f in avif}, (key, ratio)
            for f in avif:
                assert f["bytes"] <= ceiling, (f["file"], f["bytes"], ceiling)
            for f in webp:
                assert f["bytes"] <= ceiling, (f["file"], f["bytes"], ceiling)
        rec = imagery.record(imagery.BY_KEY[key])
        recorded = rec.get("ceilings", {})
        for ratio, ceiling in ceilings.items():
            assert recorded.get(ratio) == ceiling, (key, ratio, recorded.get(ratio), ceiling)
        assert "webp_allowance" not in rec, key
        # a WebP width left out is recorded, and its AVIF width still exists
        for name in rec.get("webp_not_built", []):
            assert name.endswith(".webp") and any(f["file"] == name[:-5] + ".avif" for f in rec["files"]), name


def test_v522_only_section_7_3_kinds_leave_the_v512_budget():
    """QA round 1, M1: the exemptions from DECISIONS §6 are exactly the §7.3 kinds that contradict it, each held by
    CEILINGS_V522 — never a V5.12 slot's own ratio (universities.exchange's 3:2, the ecosystem's 3:2, the pilot's 4:5)."""
    governed = {
        (imagery.record(imagery.BY_KEY[key])["slug"], ratio)
        for (key, _variant), ceilings in CEILINGS_V522.items()
        for ratio in ceilings
    }
    assert set(OWN_CEILING_V522) <= governed and set(OWN_LADDER_V522) <= governed
    v512 = {
        ("etudiants-echange-campus", "3x2"),
        ("table-travail-institutions", "3x2"),
        ("main-cedre-ciseau", "4x5"),
        ("main-marbre-ciseau", "4x5"),
    }
    assert not v512 & (set(OWN_CEILING_V522) | set(OWN_LADDER_V522))
    # the 2:3 panels' and the ground's exemption is from the limit only: their ladders keep the 480 and the 800
    for slug, ratio in OWN_CEILING_V522:
        key = next(s.key for s in imagery.SLOTS if s.slug == slug)
        widths = {f["width"] for f in imagery.record(imagery.BY_KEY[key])["files"] if f["ratio"] == ratio}
        assert {480, 800} <= widths, (slug, ratio, sorted(widths))


def test_v522_the_ladders_reach_what_each_kind_serves_and_no_further():
    for (key, ratio), top in LADDER_TOPS.items():
        widths = {f["width"] for f in imagery.record(imagery.BY_KEY[key])["files"] if f["ratio"] == ratio}
        assert max(widths) == top, (key, ratio, sorted(widths))


def test_v522_no_new_eager_image_anywhere():
    """§7.3 «No new eager image anywhere»: the eager slots are the landings' LCPs and the pilot head's second frame,
    exactly as before V5.22; every new slot and every variant is lazy."""
    eager = {s.key for s in imagery.SLOTS if s.role in ("lcp", "head")}
    assert eager == {
        "pathways.hero",
        "companies.hero",
        "institutions.hero",
        "universities.hero",
        "training.hero",
        "diplomas.hero",
        "pilot.plain",
        "pilot.fields",
        "project.hall",
        "network.table",
        "living.street",
        "contact.square",
    }, eager
    for key in NEW_V522:
        pic = imagery.picture(key)
        assert not pic.eager and not pic.head, key
    for key, variant in VARIANTS_V522:
        pic = imagery.picture(key, variant=variant)
        assert not pic.eager and not pic.head, (key, variant)


def test_v522_black_and_white_rests_only_where_section_8_puts_it():
    """§8 «Treatments»: black and white rests only in the hero, plus «select» (the four Parcours family frames) and
    «develop» (the pilot's two panels, the two V5.15 developing frames and Formation's first station); the home's
    masonry ground is desaturated IN THE FILE, never by a CSS grayscale."""
    treated = {s.key: s.treatment for s in imagery.SLOTS if s.treatment}
    assert treated == {
        "home.pilot.cedar": "develop",
        "home.pilot.marble": "develop",
        "training.after": "develop",
        "institutions.chamber": "develop",
        "pathways.family.work": "select",
        "pathways.family.study": "select",
        "pathways.family.family": "select",
        "pathways.family.other": "select",
        "training.before": "develop",
    }, treated
    stone = imagery.record(imagery.BY_KEY["home.integrity.stone"])
    assert "-35 % saturation in the file" in stone["treatment"], stone["treatment"]


def test_v522_every_new_alt_is_a_concrete_french_sentence():
    for key in (*NEW_V522[1:], "universities.exchange"):
        alt = str(imagery.BY_KEY[key].alt)
        assert 30 <= len(alt) <= 200, (key, alt)
        assert alt[0].isupper() and not alt.endswith("."), (key, alt)


def test_v522_variants_draw_their_own_crops_and_widths_and_leave_the_default_alone():
    """A V2 composition adopts a re-crop by its variant; the default rendering — the one today's page draws — is
    unchanged, so no page moves before its lane recomposes it."""
    default = imagery.picture("home.pilot.cedar")
    assert default.ratio == "4x5" and default.slot.sizes == "(min-width: 64rem) 17rem, 44vw" and not default.slot.narrow
    panel = imagery.picture("home.pilot.cedar", variant="pannello")
    assert panel.variant == "pannello" and panel.ratio == "2x3" and panel.slot.narrow == "3x2"
    assert panel.slot.sizes == "(min-width: 64rem) 34vw, 100vw"
    wide = [s for s in panel.sources if s["media"] == imagery.WIDE_MEDIA]
    assert {s["type"] for s in wide} == {"image/avif", "image/webp"}
    assert all("-2x3-" in s["srcset"] and s["height"] * 2 == s["width"] * 3 for s in wide)
    assert "-3x2-" in panel.srcset and panel.width * 2 == panel.height * 3
    arch = imagery.picture("home.ecosystem", variant="campata")
    assert arch.ratio == "4x3" and arch.slot.narrow == "3x2" and "57vw" in arch.slot.sizes
    assert imagery.picture("home.ecosystem").ratio == "3x2"
    with pytest.raises(KeyError):
        imagery.picture("home.ecosystem", variant="arco")


def test_v522_a_composition_may_state_the_width_it_draws():
    pic = imagery.picture("training.before", sizes="(min-width: 64rem) 30rem, 100vw")
    assert pic.slot.sizes == "(min-width: 64rem) 30rem, 100vw"
    assert imagery.BY_KEY["training.before"].sizes != pic.slot.sizes


def test_v522_the_panorama_has_its_three_bands():
    """§2 D: 21:9 from 64 rem, 16:9 from 48 rem, 4:5 below — the sources in that order, each with its own box."""
    pic = imagery.picture("project.volumes")
    assert [(s["media"], s["type"]) for s in pic.sources] == [
        (imagery.WIDE_MEDIA, "image/avif"),
        (imagery.WIDE_MEDIA, "image/webp"),
        (imagery.MID_MEDIA, "image/avif"),
        (imagery.MID_MEDIA, "image/webp"),
        ("", "image/avif"),
    ]
    ratios = {"21x9": (21, 9), "16x9": (16, 9), "4x5": (4, 5)}
    for source, expected in zip(pic.sources, ("21x9", "21x9", "16x9", "16x9", "4x5"), strict=True):
        assert f"-{expected}-" in source["srcset"], (expected, source["srcset"][:80])
        rw, rh = ratios[expected]
        assert abs(source["width"] * rh - source["height"] * rw) <= rw + rh, (expected, source)
    assert "-4x5-" in pic.srcset


#: renderings no product page draws any more, only the dev specimen bench (V5.31 golden home: the trust band lost its
#: stone ground, the pilot draws «riva» where «pannello» was)
NOT_DRAWN_V531 = {("home.integrity.stone", ""), ("home.pilot.cedar", "pannello"), ("home.pilot.marble", "pannello")}


@pytest.mark.parametrize(
    "key, variant",
    [
        case
        for case in [(k, "") for k in NEW_V522] + list(VARIANTS_V522) + [("universities.exchange", "")]
        if case not in NOT_DRAWN_V531
    ],
)
def test_v522_the_tag_draws_a_lazy_figure_with_explicit_boxes_and_its_sizes(key, variant):
    from django.template import Context, Template

    html = Template('{% load pages_imagery %}{% photo key "x" variant=variant %}').render(
        Context({"key": key, "variant": variant})
    )
    slot = imagery.rendering(key, variant)
    img = re.search(r"<img [^>]*>", html).group(0)
    assert 'loading="lazy"' in img and 'decoding="async"' in img and "fetchpriority" not in html
    assert re.search(r'width="\d+" height="\d+"', img), img
    for source in re.findall(r"<source [^>]*>", html):
        assert re.search(r'width="\d+" height="\d+"', source), source
        assert f'sizes="{slot.sizes}"' in source, source
    assert f'sizes="{slot.sizes}"' in img
    assert f'data-slot="{key}"' in html and "images.pexels.com" not in html
    # V5.24 §2 (FINAL_DELIVERY_V2.md §3.2 D6): no caption, no stock label on the frame
    assert "<figcaption" not in html and "Pexels" not in html


def test_v522_the_full_resolution_check_holds_in_the_crops():
    """ASSET_USAGE_MATRIX §11: what the full-resolution check found is kept by the crops themselves."""

    def crop(key: str, ratio: str):
        rec = imagery.record(imagery.BY_KEY[key])
        return next(c["crop_px"] for c in rec["crops"] if c["ratio"] == ratio), rec["original_px"]

    # Le projet's volumes: every crop starts under the spines' title labels (the lowest ends at 0.35 of the height)
    for ratio in ("21x9", "16x9", "4x5"):
        box, (w, h) = crop("project.volumes", ratio)
        assert box[1] >= 0.36 * h, (ratio, box)
    # the family table (round 1, v522-m-improve1): both crops start under the glasses and the third hand at the frame's
    # top edge (y < 0.13) and stop before the bread board at its right (x > 0.82)
    for ratio in ("3x2", "21x9"):
        box, (w, h) = crop("pathways.family.family", ratio)
        assert box[1] >= 0.15 * h and box[2] <= 0.815 * w, (ratio, box)
    # the campus re-crop: right of the book (its edge at x 0.555) and under every face (the lowest chin at y 0.40)
    box, (w, h) = crop("universities.exchange", "3x2")
    assert box[0] >= 0.556 * w and box[1] >= 0.42 * h, box
    assert imagery.record(imagery.BY_KEY["universities.exchange"])["redactions"] == []
    # the cedar's phone band stops before the shirt pocket (x 0.82); its 2:3 panel too
    for ratio in ("2x3", "3x2"):
        box, (w, h) = crop("home.pilot.cedar", ratio)
        assert box[2] <= 0.81 * w, (ratio, box)
    # Formation's first station: the face (x 0.17–0.27 of the frame) is outside both crops, which start at x 0.30; the
    # printed marks the crops keep are erased by the median mode (in focus, a blur read as a patch)
    for ratio in ("4x5", "3x2"):
        box, (w, h) = crop("training.before", ratio)
        assert box[0] >= 0.29 * w, (ratio, box)
    marks = imagery.record(imagery.BY_KEY["training.before"])["redactions"]
    assert any("maker" in r["reason"] for r in marks) and any("model codes" in r["reason"] for r in marks), marks
    assert {r.get("mode") for r in marks} == {"median"}, marks
    # the study frame (round 1, v522-m-improve1; QA m1): the face is above the frame (both crops start under the collar
    # at its top edge); the handwriting beyond the pen is softened by ONE box — two boxes that abut leave a seam of
    # crisp strokes between their feathers — clear of the pen's line and the drawn arrows (x < 0.652)
    for ratio in ("3x2", "21x9"):
        box, (w, h) = crop("pathways.family.study", ratio)
        assert box[1] >= 0.13 * h, (ratio, box)
    marks = imagery.record(imagery.BY_KEY["pathways.family.study"])["redactions"]
    assert len(marks) == 1 and "handwritten" in marks[0]["reason"], marks
    assert marks[0]["box_fraction"][0] >= 0.652, marks
    # the marble's 2:3 panel (QA round 1, M2): it trims the thumb, never the blade — the blade's outer corner (x 0.672 of
    # the frame) sits at <= 0.82 of the panel, so the home's ~30 % x 82 vh cover keeps the blade on the stone >= 4 %
    # inside the drawn edge from 1024 x 768 (evidence/v522/m/imp1_pilot_panels_cover_sim.json)
    box, (w, h) = crop("home.pilot.marble", "2x3")
    assert (0.672 * w - box[0]) / (box[2] - box[0]) <= 0.82 and box[3] - box[1] == h, box


#: the «select» treatment turns a black-and-white frame to colour when its lane is chosen (§8, B): a frame that is
#: nearly neutral in colour barely changes (QA round 1, m1: the first study frame measured 27–29). Every «select» frame
#: carries colour for the select to reveal — mean HSV saturation (0–255) of every derivative at or above this line
#: (round 1 measures, AVIF and WebP: work 66.5–69.8, study 49.4–54.2, family 84.8–96.6, other 60.9–70.0)
SELECT_MIN_SATURATION = 45.0


def test_v522_a_select_frame_carries_colour_for_the_select_to_reveal():
    from PIL import Image

    for slot in imagery.SLOTS:
        if slot.treatment != "select":
            continue
        for f in imagery.record(slot)["files"]:
            with Image.open(imagery.V5_DIR / slot.family / f["file"]) as im:
                sat = im.convert("HSV").getchannel("S")
                mean = sum(i * n for i, n in enumerate(sat.histogram())) / (sat.width * sat.height)
            assert mean >= SELECT_MIN_SATURATION, (f["file"], round(mean, 1))


def test_v522_no_frame_appears_twice_anywhere_by_id_or_by_its_original():
    """«No frame repeats anywhere» (V5.22 §14, §8): one slot per Pexels id across the V5 families, the hero and the
    portico (test_each_frame_appears_in_one_slot_across_the_site) — and one slot per ORIGINAL, by its sha256, so the
    same picture downloaded twice or under another id is caught too."""
    by_hash: dict[str, str] = {}
    for slot in imagery.SLOTS:
        digest = imagery.record(slot)["original_sha256"]
        assert digest not in by_hash, f"{slot.key} and {by_hash.get(digest)} share an original"
        by_hash[digest] = slot.key
    hero = json.loads((STATIC_IMG / "photos" / "hero" / "PROVENANCE.json").read_bytes().decode("utf-8"))
    for photo in hero["photos"]:
        assert photo["original_sha256"] not in by_hash, (photo["slug"], by_hash.get(photo["original_sha256"]))


def test_v522_the_registers_hold_a_row_per_frame_and_no_person_s_name():
    """IMAGE_LICENSES.md §3.4 and ASSET_USAGE_MATRIX.md §11 carry a row per V5.22 frame (its Pexels id and slot) —
    and, per §8, no photographer's name: the credit lives in PROVENANCE.json and in the caption only."""
    root = Path(settings.BASE_DIR) / "docs"
    licences = (root / "IMAGE_LICENSES.md").read_bytes().decode("utf-8")
    matrix = (root / "design-v5" / "ASSET_USAGE_MATRIX.md").read_bytes().decode("utf-8")
    section_l = licences.split("### 3.4", 1)[1].split("\n## ", 1)[0]
    section_m = matrix.split("## 11.", 1)[1]
    for key in (*NEW_V522, "home.pilot.cedar", "home.pilot.marble", "home.ecosystem", "universities.exchange"):
        rec = imagery.record(imagery.BY_KEY[key])
        for section in (section_l, section_m):
            assert f"`{key}`" in section, key
            assert f"Pexels {rec['pexels_id']}" in section, (key, rec["pexels_id"])
            assert rec["photographer"].strip() not in section, key
