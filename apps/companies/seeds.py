"""
Seeds of the company workspace — CONFIGURATION ONLY.

Technical Blueprint §20 puts professional, sectoral and territorial taxonomies outside the code, so
they are rows an administrator can edit, not a Python list an administrator cannot reach. This seed
creates them and never overwrites an editorial change: it matches on the stable ``code`` and only
fills defaults on creation.

The demonstration company (a synthetic one, never real data and never data copied from the previous
platform) is NOT seeded: it is created on demand by ``manage.py companies_demo``, so a deployment
that runs ``seed_all`` never invents an entreprise that does not exist.
"""

from __future__ import annotations

from core.seeds import register_seed

#: Sector taxonomy — the activity families the project's Phase 1 needs collection actually met.
SECTORS: tuple[tuple[str, str, str], ...] = (
    ("agroalimentaire", "Agroalimentaire et transformation", "Agroalimentare e trasformazione"),
    ("agriculture", "Agriculture et travaux saisonniers", "Agricoltura e lavori stagionali"),
    ("batiment", "Bâtiment et travaux publics", "Edilizia e opere pubbliche"),
    ("metallurgie", "Métallurgie et mécanique", "Metallurgia e meccanica"),
    ("logistique", "Logistique et transport", "Logistica e trasporti"),
    ("tourisme", "Hôtellerie, restauration et tourisme", "Turismo, alberghi e ristorazione"),
    ("sante-social", "Santé et services à la personne", "Sanità e servizi alla persona"),
    ("textile", "Textile et cuir", "Tessile e pelletteria"),
    ("energie", "Énergie et environnement", "Energia e ambiente"),
    ("numerique", "Numérique et services", "Digitale e servizi"),
    ("artisanat", "Artisanat", "Artigianato"),
    ("autre", "Autre secteur", "Altro settore"),
)

#: Territory taxonomy — the Italian regions of the cooperation, then the wider national perimeter.
#: A region, not a municipality: a need is expressed for a territory, and a finer grain would say
#: more about the company than the analysis requires.
TERRITORIES: tuple[tuple[str, str, str], ...] = (
    ("veneto", "Vénétie", "Veneto"),
    ("lombardia", "Lombardie", "Lombardia"),
    ("emilia-romagna", "Émilie-Romagne", "Emilia-Romagna"),
    ("piemonte", "Piémont", "Piemonte"),
    ("friuli-venezia-giulia", "Frioul-Vénétie Julienne", "Friuli-Venezia Giulia"),
    ("trentino-alto-adige", "Trentin-Haut-Adige", "Trentino-Alto Adige"),
    ("toscana", "Toscane", "Toscana"),
    ("marche", "Marches", "Marche"),
    ("lazio", "Latium", "Lazio"),
    ("campania", "Campanie", "Campania"),
    ("puglia", "Pouilles", "Puglia"),
    ("sicilia", "Sicile", "Sicilia"),
    ("autre-region", "Autre région italienne", "Altra regione italiana"),
)


@register_seed("companies.taxonomy", order=40)
def seed_taxonomy() -> str:
    from companies.models import Sector, Territory

    created_sectors = 0
    for order, (code, label_fr, label_it) in enumerate(SECTORS, start=1):
        _row, created = Sector.objects.get_or_create(
            code=code, defaults={"label_fr": label_fr, "label_it": label_it, "order": order * 10}
        )
        created_sectors += int(created)

    created_territories = 0
    for order, (code, label_fr, label_it) in enumerate(TERRITORIES, start=1):
        _row, created = Territory.objects.get_or_create(
            code=code,
            defaults={"label_fr": label_fr, "label_it": label_it, "country": "IT", "order": order * 10},
        )
        created_territories += int(created)

    return f"{created_sectors} sectors and {created_territories} territories created"
