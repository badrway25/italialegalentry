"""Build the V5 photographs' derivatives from the Pexels originals (V5.12 DECISIONS §6; label v512-c-w2).

    python tools/build_derivatives.py --originals <dir> [--only <slug> ...] [--check]

The originals stay OUTSIDE the repository (the Image Art Director's cache: C:/tmp/ile_v5_council/proof/.work/photos/
originals, proof/research/images/originals, .work/v512-c-w2/originals — one <pexels id>.jpg each, fetched once from
the Pexels CDN; the API key, needed only for the author lookup, is read from PEXELS_API_KEY by the fetch step and never
by this script). Pass every directory that holds one with --originals (repeatable).

Pipeline (the one V5 grade of gate 0, as the hero's and the portico's families were cut — proof/research/images/tools/
build_derivs.py, re-implemented here so the repository carries its own recipe):
    crop (the recorded box, snapped to the ratio) -> redact (feathered Gaussian blur on the recorded boxes) -> the V5
    grade (contrast +8 %, saturation -15 %, soft S-curve a = 0.08, blacks lifted toward notte-900 #0b1a33, highlights
    +4 % warm) -> optional extra desaturation of one hue (the recorded `desat_red`) -> Lanczos to each width (never
    upscaled) -> unsharp 0.5 -> AVIF + WebP, metadata and ICC stripped.

Weights (DECISIONS §6): a landing page's LCP image <= 60 KB, a body image <= 45 KB, a 21:9 band <= 60 KB, in the
format and at the width the browser picks at 1440 px (1x) and at 390 px (3x). The script steps the quality down until
the file fits its family's budget, and fails if it cannot within the floor (AVIF q 30, WebP q 50).

Writes static/img/v5/<family>/<slug>-<ratio>-<width>.{avif,webp} and static/img/v5/<family>/PROVENANCE.json
(licence, author, page, crops, redactions, files with bytes and sha256). apps/pages/imagery.py reads that file.
--check rebuilds nothing: it verifies that every file the provenance lists exists with its recorded size and hash.

V5.22 (SECTION_SYSTEM_V2 §7.3, §8; label v522-m-build). A recipe may carry:
    "ceilings"  {ratio: bytes} — the file ceiling of its kind (body 45 KB, band and panorama 60 KB, the 2:3 pilot
                panel 60 KB, the family frame 30 KB, the K ground 60 KB at 21:9 and 40 KB at 4:5). It binds EVERY
                width of that ratio, AVIF and WebP alike, so the largest file a browser can be served stays under it
                (round 1, label v522-m-improve1: no allowance of any kind for the WebP fallback — SECTION_SYSTEM_V2
                §7.3 records none). A WebP width that cannot fit at q 40 is not built and is listed in the provenance
                (`webp_not_built`); a browser without AVIF then takes the next WebP width down. Every AVIF width stays;
    "widths"    {ratio: (w, ...)} — a ladder of its own (the family frames stop at 720 / 1200);
    "desat"     a fraction of saturation removed from the whole frame after the grade, IN THE FILE (the home's
                masonry ground: −35 %, never a CSS grayscale);
    "tone"      "cool" — the grade's warm highlights turned slightly cool (Le projet's bound volumes);
    "keep"      ratios already built and committed that a rebuild must leave byte-identical (a re-crop adds a
                ratio to an existing slug: --only <slug> rebuilds the other ratios only).
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

Image.MAX_IMAGE_PIXELS = None
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "static" / "img" / "v5"
NOTTE_900 = (0x0B, 0x1A, 0x33)
LICENSE = "Pexels License (https://www.pexels.com/license/)"
RATIOS = {
    "4x5": (4, 5),
    "3x2": (3, 2),
    "21x9": (21, 9),
    "1x1": (1, 1),
    # V5.22 (SECTION_SYSTEM_V2 §8): the pilot's full-height panels, the ecosystem's arched frame, the panorama's tablet
    # ratio (§2 D: 21:9 from 64 rem, 16:9 from 48 rem, 4:5 below)
    "2x3": (2, 3),
    "4x3": (4, 3),
    "16x9": (16, 9),
}
# width ladders (DECISIONS §6: 480 / 800 / 1200 / 1600, 1920 for 21:9) — a width the cropped master cannot give is
# skipped
WIDTHS = {
    "4x5": (480, 800, 1200, 1600),
    "3x2": (480, 800, 1200, 1600),
    "21x9": (800, 1200, 1600, 1920),
    "1x1": (480, 800),
    "2x3": (480, 800, 1200, 1600),
    "4x3": (480, 800, 1200, 1600),
    "16x9": (480, 800, 1200, 1600),
}
BUDGET = {"lcp": 60 * 1024, "body": 45 * 1024, "band": 60 * 1024}
# the files a budget binds: the widths a 1x desktop and a 3x phone actually take for each role (imagery.py's sizes)
BUDGET_WIDTHS = {"4x5": (480, 800), "3x2": (480, 800, 1200), "21x9": (1600, 1200), "1x1": (480,)}
AVIF_Q, AVIF_FLOOR, WEBP_Q, WEBP_FLOOR = 52, 30, 74, 50
#: V5.22: under a kind's ceiling the WebP fallback goes down to this quality before a width is left out (round 1: the
#: fallback is held to the same ceiling as the AVIF, SECTION_SYSTEM_V2 §7.3; the 1.4x allowance of the first build is
#: gone)
WEBP_FLOOR_V522 = 40

# boxes are FRACTIONS of the original frame; a redaction is (x0, y0, x1, y1, blur radius at full size, reason)
RECIPES: list[dict] = [
    {
        "family": "pilote",
        "slug": "main-cedre-ciseau",
        "pexels_id": 30563520,
        "role": "body",
        # V5.22 re-crop (SECTION_SYSTEM_V2 §8.2, the home's D panorama «lo stesso gesto»): a 2:3 full-height panel
        # (2 023 × 3 035) and a 3:2 band for phones; the 4:5 of the V5.12 diptych stays as committed
        "crops": {"4x5": (0.30, 0.0, 0.76, 1.0), "2x3": (0.31, 0.0, 0.755, 1.0), "3x2": (0.02, 0.18, 0.80, 1.0)},
        "keep": ("4x5",),
        "ceilings": {"2x3": 60 * 1024, "3x2": 45 * 1024},
        "widths": {"3x2": (480, 800, 1200)},
        "redact": [],
        "label": "v522-m-build",
        "note": "the hand guiding the chisel through the cedar carving; the face and the shirt's pocket stay out "
        "(the 2:3 panel holds the chisel hand, the ringed hand and the carving; the 3:2 band stops before the pocket)",
    },
    {
        "family": "pilote",
        "slug": "main-marbre-ciseau",
        "pexels_id": 6713855,
        "role": "body",
        # V5.22 re-crop: the 2:3 panel (2 667 × 4 000) and the whole frame as the phone's 3:2 band. Round 1
        # (v522-m-improve1, QA M2): the panel starts at x 0.31 and trims the thumb, never the blade. The blade's outer
        # corner (x 0.672) sits at 0.814 of the panel, so under the home's cover (~30 % × 82 vh, centred) the blade on
        # the stone stays >= 7 % inside the drawn edge at 1024 x 768 and >= 14 % from 1280 x 800
        "crops": {"4x5": (0.17, 0.0, 0.64, 1.0), "2x3": (0.31, 0.0, 0.7545, 1.0), "3x2": (0.0, 0.0, 1.0, 1.0)},
        "keep": ("4x5",),
        "ceilings": {"2x3": 60 * 1024, "3x2": 45 * 1024},
        "widths": {"3x2": (480, 800, 1200)},
        "redact": [],
        "label": "v522-m-improve1",
        "note": "the hand and the chisel on marble; the block is not a recognisable work (the 3:2 band shows the "
        "whole frame: hands, chisel, block, sleeves; no face); the 2:3 panel holds the fist, the whole blade and its "
        "contact with the stone (the blade's corner at 0.814 of the panel), the thumb trimmed",
    },
    {
        "family": "ecosysteme",
        "slug": "table-travail-institutions",
        "pexels_id": 33543226,
        "role": "body",
        # V5.22 re-crop: the 4:3 under the home's arched frame (6 869 × 5 152; the red wall at the start edge leaves);
        # the 3:2 of V5.12 stays as committed and serves the phones
        "crops": {"3x2": (0.0, 0.0, 1.0, 1.0), "4x3": (0.111, 0.0, 1.0, 1.0)},
        "keep": ("3x2",),
        "ceilings": {"4x3": 45 * 1024},
        "redact": [
            (0.625, 0.395, 0.680, 0.505, 40, "the lanyard badge (mark and name)"),
            (0.655, 0.000, 0.740, 0.420, 40, "the lanyard's printed strap"),
            (0.040, 0.520, 0.480, 0.680, 22, "legible handwriting on the papers"),
        ],
        "label": "v522-m-build",
        "note": "hands and documents around a working table; no face in the frame",
    },
    {
        "family": "personnes",
        "slug": "personne-fenetre-dos",
        "pexels_id": 7594198,
        "role": "lcp",
        "crops": {"4x5": (0.235, 0.0, 0.765, 1.0), "3x2": (0.05, 0.10, 0.95, 1.0)},
        "redact": [],
        "note": "a man at a desk by a window, seen from behind; nothing legible on the desk",
    },
    {
        "family": "entreprises",
        "slug": "atelier-mesure-precision",
        "pexels_id": 7180823,
        "role": "lcp",
        "crops": {"3x2": (0.08, 0.215, 0.92, 0.90)},
        "redact": [(0.425, 0.470, 0.535, 0.565, 12, "the caliper's maker's mark and scale lettering")],
        "desat_red": 0.15,
        "note": "the craftsman's hands, the caliper and the piece; the crop stops under the chin (O55); red sweater "
        "-15 % sat.; "
        "3:2 only: the gesture is horizontal and a 4:5 cut loses either the hand or the piece",
    },
    {
        "family": "institutions",
        "slug": "table-des-institutions",
        "pexels_id": 6949366,
        "role": "lcp",
        "crops": {"4x5": (0.33, 0.03, 0.87, 0.97), "3x2": (0.05, 0.15, 1.0, 0.95)},
        "redact": [],
        "note": "an empty council table: microphones, screens off, blank name cards; no emblem",
    },
    {
        "family": "universites",
        "slug": "bibliotheque-salle-lecture",
        "pexels_id": 9489906,
        "role": "lcp",
        "crops": {"4x5": (0.715, 0.30, 1.0, 0.83), "3x2": (0.70, 0.40, 1.0, 0.70)},
        "redact": [],
        "note": "the reading room's end bay: bookcases, a lamp, the long tables by the windows; the two readers and "
        "the spiral "
        "stair stay out of the crop (O55, O54)",
    },
    {
        "family": "universites",
        "slug": "etudiants-echange-campus",
        "pexels_id": 31367507,
        "role": "body",
        # V5.22 re-crop (SECTION_SYSTEM_V2 §8.2): at 768 the two blurred covers read as censored objects
        # (evidence/v522/pages2/p1_universites_fr_768.jpg); the new 3:2 starts after the book's edge (x 0.555) and
        # below every face, so nothing needs a redaction: the folder is a tablet's plain folio case
        "crops": {"3x2": (0.58, 0.44, 1.0, 0.86)},
        "ceilings": {"3x2": 45 * 1024},
        "redact": [],
        "label": "v522-m-build",
        "note": "the exchange told by hands: one student's explaining gesture, the other's folio case held against "
        "her; the book and its cover, the second book and every face are outside the crop (O55), so no redaction",
    },
    # ---- V5.15 W3 (label v515-c-build): the imagery pass — the remaining pages' frames, each in ONE slot
    {
        "family": "formation",
        "slug": "atelier-soudure-geste",
        "pexels_id": 5265332,
        "role": "lcp",
        "crops": {"3x2": (0.22, 0.38, 0.84, 1.0)},
        "redact": [(0.425, 0.525, 0.470, 0.570, 18, "the jacket's brand mark")],
        "note": "a trainee hands the torch to another over the vice; the one face in the full frame (right, in "
        "profile) is above the "
        "crop (O55); the helmets' decals are outside it; 3:2 only (a 4:5 cut brings the profile back)",
    },
    {
        "family": "formation",
        "slug": "microscopes-rangee",
        "pexels_id": 15290006,
        "role": "body",
        "crops": {"3x2": (0.0, 0.0, 1.0, 1.0)},
        "redact": [],
        "note": "a row of microscopes on a pale bench: structured learning, nobody in the frame",
    },
    {
        "family": "diplomes",
        "slug": "classeur-documents-ouvert",
        "pexels_id": 4792286,
        "role": "lcp",
        "crops": {"3x2": (0.0, 0.0, 1.0, 1.0)},
        "redact": [],
        "note": "an open accordion case of papers on a wooden table, from above; nothing legible on the papers",
    },
    {
        "family": "pilote",
        "slug": "plaine-peupliers-hiver",
        "pexels_id": 11010756,
        "role": "lcp",
        "crops": {"4x5": (0.0, 0.0, 0.6, 1.0)},
        "redact": [],
        "soft": 0.7,
        "note": "a row of bare poplars over a ploughed plain in the mist; the alt names no place (stock is never "
        "documentary)",
    },
    {
        "family": "pilote",
        "slug": "champs-montagnes-printemps",
        "pexels_id": 36909829,
        "role": "body",
        "crops": {"4x5": (0.0, 0.0, 0.55, 1.0)},
        "redact": [],
        "soft": 0.8,
        "note": "flowering fields under a snow-capped range; the alt names no place",
    },
    {
        "family": "projet",
        "slug": "grande-salle-etude",
        "pexels_id": 10323211,
        "role": "lcp",
        "crops": {"3x2": (0.0, 0.16, 1.0, 0.66)},
        "redact": [],
        "note": "a great study hall seen from a gallery: glazed walls, long tables; the people are small, seen from "
        "above, none "
        "turned to the camera; the near readers of the full frame's foot are below the crop (O55)",
    },
    {
        "family": "reseau",
        "slug": "table-commune-vue-haut",
        "pexels_id": 34632581,
        "role": "lcp",
        "crops": {"3x2": (0.0, 0.0, 1.0, 1.0)},
        "redact": [],
        "soft": 0.6,
        "note": "one long shared table from straight above: laptops, papers, the tops of heads — no face (O55)",
    },
    {
        "family": "vivre",
        "slug": "rue-facades-couleurs",
        "pexels_id": 12900263,
        "role": "lcp",
        "crops": {"21x9": (0.0, 0.03, 1.0, 0.69), "3x2": (0.0, 0.0, 0.62, 0.62)},
        "soft": 1.0,
        "redact": [(0.080, 0.650, 0.105, 0.680, 10, "the house number")],
        "note": "a street of stucco façades, shutters and balconies; the parked cars, their plates and the cyclist "
        "stay below the "
        "crop; the alt names no city",
    },
    {
        "family": "contact",
        "slug": "place-civique-palais",
        "pexels_id": 14581980,
        "role": "lcp",
        "crops": {"3x2": (0.0, 0.0, 1.0, 1.0)},
        "soft": 0.6,
        "redact": [],
        "note": "a civic square between two palazzi; five passers-by seen from behind, small, none identifiable "
        "(O55); the "
        "square, not a doorway, is the subject (O54); the alt names no city",
    },
    {
        "family": "entreprises",
        "slug": "serres-plaine-crepuscule",
        "pexels_id": 5906831,
        "role": "body",
        "crops": {"21x9": (0.0, 0.18, 1.0, 0.82)},
        "redact": [],
        "soft": 0.6,
        "note": "greenhouse tunnels across a cultivated plain at dusk: the productive territory; nobody in the frame; "
        "the alt "
        "names no place",
    },
    {
        "family": "institutions",
        "slug": "hemicycle-pupitres",
        "pexels_id": 32266781,
        "role": "body",
        "crops": {"3x2": (0.0, 0.22, 0.77, 1.0)},
        "redact": [(0.490, 0.520, 1.000, 0.760, 30, "the printed sheet on the desk")],
        "note": "the desks and microphones of an assembly hall; the flags and coats of arms under the windows are "
        "above the crop; "
        "the chamber is not recognisable in the crop",
    },
    # ---- V5.22 (label v522-m-build; SECTION_SYSTEM_V2 §8.1): seven new frames, each in ONE slot, every width under
    # its kind's ceiling (§7.3). Nobody identifiable (O55), no arch, step, vault, door or gridded window as the subject
    # (O54), no cliché, no readable text or brand (redacted where the crop keeps it), Q4 and Q5 untouched.
    {
        "family": "accueil",
        "slug": "pierre-appareillee",
        "pexels_id": 11499083,
        "role": "ground",
        # the home's integrity band (S5 + S6, «lo strato»): the ground under a 60 % stone veil — 21:9 from 64 rem, 4:5
        # below; desaturated in the file (never a CSS grayscale), decorative
        "crops": {"21x9": (0.0, 0.20, 1.0, 0.77), "4x5": (0.22, 0.0, 0.82, 1.0)},
        # round 1: a 640 step, because the 800 w WebP cannot fit 40 KB at q 40 (the fallback keeps two widths)
        "widths": {"4x5": (480, 640, 800)},
        "ceilings": {"21x9": 60 * 1024, "4x5": 40 * 1024},
        "desat": 0.35,
        # the faces' grain is softened (the courses, joints and raking light carry the ground under its veil; the
        # grain was 2.5x the 21:9 ceiling)
        "soft": 1.6,
        "redact": [],
        "label": "v522-m-build",
        "note": "dressed stone courses in raking light, close and frontal: block faces, joints and their shadows; no "
        "opening of any kind, no mark, no lettering, nobody; the 21:9 keeps the full width, the 4:5 the frame's centre",
    },
    {
        "family": "projet",
        "slug": "codici-rilegati",
        "pexels_id": 29976379,
        "role": "band",
        # Le projet's D panorama (after «il racconto»): 21:9 from 64 rem, 16:9 from 48 rem, 4:5 below (§2 D)
        "crops": {"21x9": (0.0, 0.37, 1.0, 1.0), "16x9": (0.12, 0.37, 0.87, 1.0), "4x5": (0.0, 0.37, 0.34, 1.0)},
        # the 4:5 serves phones only (< 48 rem, full width): 800 w covers a 2x phone; a 1 200 w could not keep 45 KB.
        # Round 1: a 640 step, because the 800 w WebP cannot fit 45 KB at q 40 (the fallback keeps two widths)
        "widths": {"4x5": (480, 640, 800)},
        "ceilings": {"21x9": 60 * 1024, "16x9": 60 * 1024, "4x5": 45 * 1024},
        "tone": "cool",
        # the 1 920 w 21:9 fits its 60 KB at q 31 (at 0 it needed q < 30); the phone-only 4:5 a little softer, so its
        # 800 w WebP fallback fits too (at 0.6 it did not, even at q 40)
        "soft": {"21x9": 0.6, "16x9": 0.6, "4x5": 1.0},
        "redact": [],
        "label": "v522-m-build",
        "note": "leather-bound volumes on a shelf, raised bands and gilt tooling in raking light; every crop starts "
        "under the spines' title labels (y 0.37 of the frame; the lowest label ends at 0.35), so no title is in any "
        "crop and nothing needs a redaction; nobody; a different scale and subject from the Universités reading room",
    },
    {
        "family": "personnes",
        "slug": "entrepot-allee-rayonnages",
        "pexels_id": 29454379,
        "role": "body",
        # Parcours PA-1, the lane «Travail» (B «il tracciato»): 3:2 at the lane head from 64 rem, a 21:9 strip below;
        # treatment «select» (black and white at rest, colour when its lane is chosen, hovered or focused)
        "crops": {"3x2": (0.0, 0.30, 1.0, 0.80), "21x9": (0.0, 0.44, 1.0, 0.76)},
        "widths": {"3x2": (480, 720), "21x9": (480, 720, 1200)},
        "ceilings": {"3x2": 30 * 1024, "21x9": 30 * 1024},
        "soft": 0.4,
        "redact": [],
        "label": "v522-m-build",
        "note": "a logistics warehouse aisle in perspective between high pallet racking, empty; the cartons' printed "
        "labels are a few pixels high at every served width (720 / 1200 w), so nothing is legible; nobody",
    },
    {
        "family": "personnes",
        "slug": "notes-cahier-livre",
        "pexels_id": 6334273,
        "role": "body",
        # Parcours PA-1, the lane «Études et formation». Round 1 (v522-m-improve1, QA m1): replaces 6549915, an overhead
        # tabletop beside «Famille», nearly neutral (mean saturation 27–29, so «select» barely changed it) and with a
        # redaction seam across its dictionary. This frame is at desk level and warm (brown tweed, pink shirt, pale
        # wood: mean saturation 52–55 after the grade); the open book stands behind the writing hand
        "crops": {"3x2": (0.10, 0.14, 0.90, 0.94), "21x9": (0.02, 0.29, 0.98, 0.88)},
        "widths": {"3x2": (480, 720), "21x9": (480, 720, 1200)},
        "ceilings": {"3x2": 30 * 1024, "21x9": 30 * 1024},
        # the handwritten figures and words beyond the pen are softened by ONE box (two boxes that abut leave a seam
        # of crisp strokes between their feathers, QA round 1 m1), where the page already falls out of focus, so the
        # softening reads as depth of field; the pen's own line and the drawn arrows beside it (x < 0.652) are shapes,
        # not words, and stay sharp
        "redact": [
            (0.655, 0.655, 0.870, 0.850, 12, "the handwritten figures and words on the notebook beyond the pen"),
        ],
        "label": "v522-m-improve1",
        "note": "at desk level: a hand writes in a ruled notebook with a white pen, an open book behind it, a second "
        "book at the edge; the face is above the frame (the collar at its top edge is above both crops, which start at "
        "y 0.14 and 0.29); the books' pages and covers carry nothing legible; the far handwriting is softened",
    },
    {
        "family": "personnes",
        "slug": "table-partagee-vue-haut",
        "pexels_id": 27177298,
        "role": "body",
        # Parcours PA-1, the lane «Famille» (seen from above, §8.1). Round 1 (v522-m-improve1): replaces 3184192, the
        # generic brunch table (QA round 1: 3 / 5); a shared table on an openwork wooden top, two hands serving each
        # other. Both crops stop at x 0.81, before the bread board (a filled loaf), and start under the glasses at the
        # frame's top edge (y < 0.13) and the third hand there
        "crops": {"3x2": (0.0, 0.17, 0.81, 1.0), "21x9": (0.0, 0.20, 0.81, 0.733)},
        "widths": {"3x2": (480, 720), "21x9": (480, 720, 1200)},
        "ceilings": {"3x2": 30 * 1024, "21x9": 30 * 1024},
        "soft": 0.4,
        "redact": [],
        "label": "v522-m-improve1",
        "note": "a shared table from straight above: bowls of olives, tomatoes, a dip and peanuts on an openwork "
        "wooden top; one hand holds out a spoon, the other holds the olive bowl; no face (the arms enter from the "
        "edges), no lettering, no brand; the glasses at the frame's top edge, the third hand there and the bread board "
        "at its right are outside both crops",
    },
    {
        "family": "personnes",
        "slug": "vignes-brume-aube",
        "pexels_id": 9250930,
        "role": "body",
        # Parcours PA-1, the lane «Autres voies» (seasonal work); distinct from the Entreprises greenhouses at dusk
        "crops": {"3x2": (0.0, 0.0, 1.0, 1.0), "21x9": (0.0, 0.24, 1.0, 0.887)},
        "widths": {"3x2": (480, 720), "21x9": (480, 720, 1200)},
        "ceilings": {"3x2": 30 * 1024, "21x9": 30 * 1024},
        "soft": 0.6,
        "redact": [],
        "label": "v522-m-build",
        "note": "netted vine rows running into a misty plain, a line of trees and hills behind; no person; a car and "
        "a mast lost in the haze are a few pixels wide; the alt names no place (stock is never documentary)",
    },
    {
        "family": "formation",
        "slug": "banc-electrique-mains",
        "pexels_id": 34526423,
        "role": "body",
        # Formation F1 «la traversata», station 1 (before departure): 4:5 from 64 rem, 3:2 below; treatment
        # «develop» (bw-scroll), allowed for /formation/'s two times. Both crops start at x 0.30: the face (x 0.17–0.27,
        # y 0.20–0.44) is outside every crop (O55); only the hands, the contactors and the wire ducts remain
        "crops": {"4x5": (0.30, 0.28, 0.56, 0.77), "3x2": (0.30, 0.40, 0.56, 0.66)},
        "widths": {"4x5": (480, 800, 1200), "3x2": (480, 800, 1200)},
        "ceilings": {"4x5": 45 * 1024, "3x2": 45 * 1024},
        # the median mode erases the printed strokes and keeps every shape crisp: a blur read as patches in focus
        "redact": [
            (0.360, 0.428, 0.399, 0.475, 9, "a motor-protection breaker's maker's logo and printed label", "median"),
            (0.430, 0.400, 0.462, 0.462, 9, "a miniature breaker's printed markings", "median"),
            (0.431, 0.583, 0.498, 0.640, 9, "the control relays' model codes and terminal numbers", "median"),
            (0.383, 0.612, 0.408, 0.636, 9, "a module's CE label", "median"),
        ],
        "label": "v522-m-build",
        "note": "hands wiring control relays on an electrical training bench, between blue wire ducts and red leads; "
        "the face (x 0.17–0.27) is outside both crops, which start at x 0.30 (O55); the breaker's maker's logo and "
        "label, the relays' model codes and terminal numbers and a CE label are erased by a median filter (the shapes "
        "stay crisp, so nothing reads as a blurred patch); the supply panel's "
        "lettering and the louvred window stay outside the crops; distinct from the welding head and the companies' "
        "calliper. Chosen over 34938452 (the same subject on a workbench), whose Pexels author is a company account: "
        "the caption would have printed a commercial brand under the frame",
    },
]


# ------------------------------------------------------------------ the one V5 grade
def _lut(fn) -> list[int]:
    return [max(0, min(255, round(fn(i)))) for i in range(256)]


def _s_curve(a: float = 0.08):
    return lambda i: 255 * ((i / 255) - (a / (2 * math.pi)) * math.sin(2 * math.pi * i / 255))


def _lift(target: int, t: float = 0.8):
    return lambda i: i + t * target * (1 - i / 255) ** 4


def _warm(pct: float):
    def fn(i: int) -> float:
        x = i / 255
        w = ((x - 0.6) / 0.4) ** 2 if x > 0.6 else 0.0
        return i + pct * 255 * w

    return fn


#: the highlight shift of the one V5 grade (r, g, b), and its cool reading for a frame that must not warm (V5.22 §8:
#: Le projet's bound volumes, «colour, cool grade», so the leather reads institutional and never as the reading room)
HIGHLIGHT_SHIFT = {"": (0.04, 0.015, -0.02), "cool": (-0.015, 0.0, 0.025)}


def grade(img: Image.Image, tone: str = "") -> Image.Image:
    img = ImageEnhance.Contrast(img).enhance(1.08)
    img = ImageEnhance.Color(img).enhance(0.85)
    img = img.point(_lut(_s_curve()) * 3)
    r, g, b = img.split()
    sr, sg, sb = HIGHLIGHT_SHIFT[tone]
    r = r.point(_lut(_lift(NOTTE_900[0]))).point(_lut(_warm(sr)))
    g = g.point(_lut(_lift(NOTTE_900[1]))).point(_lut(_warm(sg)))
    b = b.point(_lut(_lift(NOTTE_900[2]))).point(_lut(_warm(sb)))
    return Image.merge("RGB", (r, g, b))


def desaturate_reds(img: Image.Image, amount: float) -> Image.Image:
    """Lower the saturation of the red hues only (the workshop's sweater): HSV, hue within ±25° of red."""
    h, s, v = img.convert("HSV").split()
    reds = h.point(lambda hv: 255 if hv < 18 or hv > 237 else 0).filter(ImageFilter.GaussianBlur(2))
    s = Image.composite(s.point(lambda sv: round(sv * (1 - amount))), s, reds)
    return Image.merge("HSV", (h, s, v)).convert("RGB")


def snap(box, ratio, size):
    wpx, hpx = size
    x0, y0, x1, y1 = box[0] * wpx, box[1] * hpx, box[2] * wpx, box[3] * hpx
    bw, bh = x1 - x0, y1 - y0
    rw, rh = ratio
    if bw / bh > rw / rh:
        nbw = bh * rw / rh
        cx = (x0 + x1) / 2
        x0, x1 = cx - nbw / 2, cx + nbw / 2
    else:
        nbh = bw * rh / rw
        cy = (y0 + y1) / 2
        y0, y1 = cy - nbh / 2, cy + nbh / 2
    x0, y0 = max(0, round(x0)), max(0, round(y0))
    w = min(wpx - x0, round(x1 - x0))
    h = round(w * rh / rw)
    if y0 + h > hpx:
        y0 = max(0, hpx - h)
        if y0 + h > hpx:
            h = hpx - y0
            w = round(h * rw / rh)
    return (x0, y0, x0 + w, y0 + h)


def redact(img: Image.Image, boxes) -> Image.Image:
    """A box is (x0, y0, x1, y1, radius, reason[, mode]). Mode «blur» (the default): a feathered Gaussian blur.
    Mode «median» (V5.22): a median filter of `radius` px — it erases thin printed strokes (labels, model codes) and
    keeps the edges of the larger shapes crisp, so an in-focus label reads as blank, never as a blurred patch."""
    W, H = img.size
    for box in boxes:
        fx0, fy0, fx1, fy1, rad, _why = box[:6]
        mode = box[6] if len(box) > 6 else "blur"
        left, u, r, lo = int(fx0 * W), int(fy0 * H), int(fx1 * W), int(fy1 * H)
        pad = rad * 3
        pl, pu, pr, plo = max(0, left - pad), max(0, u - pad), min(W, r + pad), min(H, lo + pad)
        region = img.crop((pl, pu, pr, plo))
        if mode == "median":
            size = rad if rad % 2 else rad + 1
            treated = region.filter(ImageFilter.MedianFilter(size))
            feather = 3
        else:
            treated = region.filter(ImageFilter.GaussianBlur(rad))
            feather = max(4, rad)
        mask = Image.new("L", region.size, 0)
        ImageDraw.Draw(mask).rectangle((left - pl, u - pu, r - pl - 1, lo - pu - 1), fill=255)
        mask = mask.filter(ImageFilter.GaussianBlur(feather))
        img.paste(treated, (pl, pu), mask)
    return img


def _clean(img: Image.Image) -> Image.Image:
    out = Image.new("RGB", img.size)
    out.paste(img)
    return out


def encode(img: Image.Image, fmt: str, q: int) -> bytes:
    buf = io.BytesIO()
    if fmt == "avif":
        _clean(img).save(buf, "AVIF", quality=q, speed=4, subsampling="4:2:0")
    else:
        _clean(img).save(buf, "WEBP", quality=q, method=6)
    return buf.getvalue()


def fit(img: Image.Image, fmt: str, limit: int | None, floor: int | None = None) -> tuple[bytes, int]:
    q, default_floor = (AVIF_Q, AVIF_FLOOR) if fmt == "avif" else (WEBP_Q, WEBP_FLOOR)
    floor = floor or default_floor
    data = encode(img, fmt, q)
    while limit and len(data) > limit:
        q -= 3
        if q < floor:
            raise SystemExit(f"cannot fit {img.size} {fmt} under {limit} B above q{floor}")
        data = encode(img, fmt, q)
    return data, q


def find_original(pid: int, dirs: list[Path]) -> Path:
    for d in dirs:
        p = d / f"{pid}.jpg"
        if p.exists():
            return p
    raise SystemExit(f"original {pid}.jpg not found in {', '.join(map(str, dirs))}")


def find_meta(pid: int, dirs: list[Path]) -> dict:
    for d in dirs:
        for p in (d / f"{pid}.json", d.parent / "meta" / f"{pid}.json"):
            if p.exists():
                return json.loads(p.read_bytes().decode("utf-8"))
    raise SystemExit(f"metadata {pid}.json not found (the fetch step writes it next to the original)")


def build(recipe: dict, dirs: list[Path]) -> dict:
    pid = recipe["pexels_id"]
    src = find_original(pid, dirs)
    meta = find_meta(pid, dirs)
    original = Image.open(src)
    original.load()
    original = original.convert("RGB")
    W, H = original.size
    worked = redact(original.copy(), recipe["redact"])
    family_dir = OUT / recipe["family"]
    family_dir.mkdir(parents=True, exist_ok=True)
    files = []
    skipped: list[str] = []
    keep = set(recipe.get("keep", ()))
    ceilings = recipe.get("ceilings") or {}
    for ratio, box in recipe["crops"].items():
        if ratio in keep:
            continue  # a ratio already built and committed: its files stay byte-identical (write_provenance merges)
        px = snap(box, RATIOS[ratio], (W, H))
        master = grade(worked.crop(px), recipe.get("tone", ""))
        if recipe.get("desat_red"):
            master = desaturate_reds(master, recipe["desat_red"])
        if recipe.get("desat"):
            master = ImageEnhance.Color(master).enhance(1 - recipe["desat"])
        role = "band" if ratio == "21x9" else recipe["role"]
        for width in recipe.get("widths", {}).get(ratio, WIDTHS[ratio]):
            if width > master.width:
                continue
            height = round(width * RATIOS[ratio][1] / RATIOS[ratio][0])
            d = master.resize((width, height), Image.LANCZOS)
            # `soft`: a frame of fine, even texture (mist over furrows) is softened instead of sharpened, so it fits its
            # budget without blocking (V5.15 W3); every other frame gets the unsharp 0.5. V5.22: a {ratio: radius} map
            # softens one crop more than another (a phone-only crop whose fallback must still fit)
            soft = recipe.get("soft")
            soft = soft.get(ratio) if isinstance(soft, dict) else soft
            d = (
                d.filter(ImageFilter.GaussianBlur(soft))
                if soft
                else d.filter(ImageFilter.UnsharpMask(radius=0.5, percent=60, threshold=2))
            )
            for fmt in ("avif", "webp"):
                # V5.22: the kind's ceiling binds every width the slot can serve (§7.3 «largest served AVIF»), and the
                # WebP fallback under the same ceiling (round 1, v522-m-improve1: no allowance); a V5.12 recipe keeps
                # DECISIONS §6's budgets on the widths they bind
                limit = ceilings[ratio] if ceilings else (BUDGET[role] if width in BUDGET_WIDTHS[ratio] else None)
                try:
                    data, q = fit(d, fmt, limit, WEBP_FLOOR_V522 if (ceilings and fmt == "webp") else None)
                except SystemExit:
                    if not (ceilings and fmt == "webp"):
                        raise
                    # V5.22: the WebP fallback stops at the widths it can serve under the ceiling (a browser without
                    # AVIF then takes the next width down); every AVIF width stays, under its ceiling
                    skipped.append(f"{recipe['slug']}-{ratio}-{width}.webp")
                    print(f"  {recipe['slug']}-{ratio}-{width}.webp skipped: over {limit} B above q{WEBP_FLOOR_V522}")
                    continue
                name = f"{recipe['slug']}-{ratio}-{width}.{fmt}"
                (family_dir / name).write_bytes(data)
                files.append(
                    {
                        "file": name,
                        "ratio": ratio,
                        "width": width,
                        "height": height,
                        "format": fmt,
                        "quality": q,
                        "bytes": len(data),
                        "budget": limit,
                        "sha256": hashlib.sha256(data).hexdigest(),
                    }
                )
                print(f"  {name:<52} {len(data):>7} B  q{q}{f'  (budget {limit})' if limit else ''}")
        files_crop = {
            "ratio": ratio,
            "crop_fraction": list(box),
            "crop_px": list(px),
            "master_px": [px[2] - px[0], px[3] - px[1]],
        }
        recipe.setdefault("_crops", []).append(files_crop)
    out = {
        "slug": recipe["slug"],
        "pexels_id": pid,
        "photographer": meta.get("photographer"),
        "photographer_url": meta.get("photographer_url"),
        "page": meta.get("url") or meta.get("page"),
        "license": LICENSE,
        "pexels_alt": meta.get("alt"),
        "original_px": [W, H],
        "original_sha256": hashlib.sha256(src.read_bytes()).hexdigest(),
        "role": recipe["role"],
        "crops": recipe.pop("_crops", []),
        "redactions": [
            {"box_fraction": list(r[:4]), "radius_px": r[4], "reason": r[5], **({"mode": r[6]} if len(r) > 6 else {})}
            for r in recipe["redact"]
        ],
        "treatment": "the one V5 grade (contrast +8 %, saturation -15 %, S-curve a = 0.08, blacks toward notte-900, "
        + ("highlights turned cool: r -1.5 %, b +2.5 %" if recipe.get("tone") == "cool" else "highlights +4 % warm")
        + ")"
        + (f"; reds -{int(recipe['desat_red'] * 100)} % saturation" if recipe.get("desat_red") else "")
        + (f"; the whole frame -{round(recipe['desat'] * 100)} % saturation in the file" if recipe.get("desat") else "")
        + "; Lanczos; "
        + (f"soft {recipe['soft']}" if recipe.get("soft") else "unsharp 0.5").replace("'", "")
        + "; AVIF (speed 4, 4:2:0) + WebP (method 6); metadata and ICC stripped",
        "note": recipe["note"],
        "files": files,
    }
    if ceilings:
        out["ceilings"] = dict(ceilings)
        out["webp_floor"] = WEBP_FLOOR_V522
        out["webp_not_built"] = skipped
    if recipe.get("label"):
        out["label"] = recipe["label"]
    out["_keep"] = sorted(set(recipe.get("keep", ())))
    return out


def write_provenance(family: str, photos: list[dict]) -> None:
    path = OUT / family / "PROVENANCE.json"
    existing = {}
    if path.exists():
        existing = {p["slug"]: p for p in json.loads(path.read_bytes().decode("utf-8"))["photos"]}
    for p in photos:
        keep = set(p.pop("_keep", ()))
        old = existing.get(p["slug"])
        if old and keep:
            # a re-crop (V5.22): the kept ratios' files and crops stay as committed, the new ones join them
            p["files"] = [f for f in old["files"] if f["ratio"] in keep] + p["files"]
            p["crops"] = [c for c in old.get("crops", []) if c["ratio"] in keep] + p["crops"]
            for k in ("ceilings",):
                if k in old and k in p:
                    p[k] = {**old[k], **p[k]}
        existing[p["slug"]] = p
    doc = {
        "what": f"V5 photographs, family «{family}» (V5.12 DECISIONS §6; V5.22 SECTION_SYSTEM_V2 §8): one frame, one "
        f"context; slots in apps/pages/imagery.py.",
        "builder": "tools/build_derivatives.py (originals outside the repository; never hotlinked)",
        "policy": "Self-hosted only. Pexels License: free use and modification, no endorsement implied; the author is "
        "recorded anyway. "
        "Nobody identifiable (O55); no arcade, step, vault, door or gridded window as the subject (O54); stock is "
        "never documentary.",
        "photos": [existing[k] for k in sorted(existing)],
    }
    path.write_bytes((json.dumps(doc, indent=1, ensure_ascii=False) + "\n").encode("utf-8"))


def check() -> int:
    bad = 0
    for prov in sorted(OUT.glob("*/PROVENANCE.json")):
        for photo in json.loads(prov.read_bytes().decode("utf-8"))["photos"]:
            for f in photo["files"]:
                p = prov.parent / f["file"]
                if not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest() != f["sha256"]:
                    print("MISMATCH", p)
                    bad += 1
    print("check:", "ok" if not bad else f"{bad} problem(s)")
    return 1 if bad else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--originals", action="append", default=[], help="a directory holding <pexels id>.jpg (+ .json)")
    ap.add_argument("--only", nargs="*", help="only these slugs")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    if a.check:
        return check()
    dirs = [Path(d) for d in a.originals]
    if not dirs:
        ap.error("--originals is required")
    for recipe in RECIPES:
        if a.only and recipe["slug"] not in a.only:
            continue
        print(recipe["family"], recipe["slug"], flush=True)
        # written after each frame (V5.22): a later frame that cannot fit its ceiling leaves the earlier ones recorded
        write_provenance(recipe["family"], [build(dict(recipe), dirs)])
    return 0


if __name__ == "__main__":
    sys.exit(main())
