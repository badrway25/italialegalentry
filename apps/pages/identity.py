"""
The promoter's public identification — ONE canonical source (the owner's Q9 decision A, V5.23, 30 October 2026;
SECTION_SYSTEM_V2 §11.1 and §3.17 AG-3; lane P2).

«The AGAMI page should show the association's verified public institutional identification directly […] Use only
verified public data […] Do not invent or add other identifiers.» The values below are the owner's, as he gave them,
held once and read by the AGAMI page's identification plate alone (templates/pages/agami.html); no other template
retypes them. The association's name and its official address are not repeated here: they are the site's own constants
(``settings.ILE["PROMOTER"]``, the address of ``site.contact_email``, the locked ``p1.email.public_contact``), so each
fact keeps its one home. An address is held as its fields (the street, the postal code, the town, the province) and set
as two lines, the country in the page's language by the template; the registers' designations are Italian and are
rendered with ``lang="it"``.

The official legal notices («Mentions légales») stay unpublished under Q2: the plate is understandable on its own and
links to them only once they are published (``links.notices``, empty while the route is gated).
"""

from __future__ import annotations

from django.conf import settings
from django.utils.translation import gettext_lazy as _

#: the owner's verified fields (V5.23), in his order — the name and the contact are the site's constants (above)
LEGAL_FORM = "Associazione di Promozione Sociale (APS) / Ente del Terzo Settore"
TAX_CODE = "91036640240"
RUNTS = "Repertorio n. 149809"
REGISTRATION = "Decreto Regione Veneto n. 11118 del 17/09/2025"
#: an office as its address's fields (the street; the postal code, the town and its province) — the template sets them
REGISTERED_OFFICE = {
    "street": "Via Sandrigo n. 29",
    "postcode": "36061",
    "town": "Bassano del Grappa",
    "province": "VI",
}
OPERATIONAL_OFFICE = {"street": "Viale Giuseppe Mazzini 142", "postcode": "00195", "town": "Roma", "province": ""}
WEBSITE = "agamieuromed.org"


def identification() -> dict:
    """The plate's data: the name, its legal form, the registers, the two offices and the official website, each with
    its label (a catalogue string) and the language of its value."""
    return {
        "name": settings.ILE["PROMOTER"],
        "legal_form": LEGAL_FORM,
        "registers": [
            {"key": "tax-code", "label": _("Code fiscal"), "value": TAX_CODE, "lang": ""},
            {"key": "runts", "label": "RUNTS", "label_lang": "it", "value": RUNTS, "lang": "it"},
            {"key": "registration", "label": _("Inscription"), "value": REGISTRATION, "lang": "it"},
        ],
        "offices": [
            {"key": "registered", "label": _("Siège social"), "address": REGISTERED_OFFICE},
            {"key": "operational", "label": _("Siège opérationnel"), "address": OPERATIONAL_OFFICE},
        ],
        # the website as the owner gave it, a fact of the identification — not a link: the site's one outbound link is
        # the WhatsApp channel the owner ordered (V5.19 §7; tests/compliance/test_public_pages.py)
        "website": {"label": _("Site officiel"), "host": WEBSITE},
    }
