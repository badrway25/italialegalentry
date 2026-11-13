"""
Partner seeds — NOTHING is authorised by the seed (gate G6).

The two patronage bodies of the Rovigo Forum are created as *draft, unauthorised* rows so the
back-office already has the slot ready for the logos and written authorisations that will be
transmitted separately (document §2.1 note). Editorial changes are never overwritten.
"""

from core.seeds import register_seed
from partners.models import Partner, PartnerKind

PATRONAGE_SLOTS = (
    ("Région de la Vénétie", PartnerKind.INSTITUTION, "Italie", "Venise", 1),
    ("Commune de Rovigo", PartnerKind.INSTITUTION, "Italie", "Rovigo", 2),
)


@register_seed("partners.patronage_slots", order=60)
def seed_patronage_slots():
    created = 0
    for name, kind, country, city, order in PATRONAGE_SLOTS:
        _obj, was_created = Partner.objects.get_or_create(
            name=name,
            defaults={
                "kind": kind,
                "country": country,
                "city": city,
                "order": order,
                "authorized": False,
                "editorial_note": "Slot logo — in attesa di trasmissione e autorizzazione scritta (G6)",
            },
        )
        created += int(was_created)
    return f"{created} patronage slot(s) created (all unauthorised, draft)"
