"""Gate G6: a partner's name/logo is public only when authorised in writing AND published."""

import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction

from cms.forbidden import scan
from cms.models import PublicationStatus
from partners.models import Partner, PartnerKind
from partners.services import authorized_partners

pytestmark = [pytest.mark.django_db, pytest.mark.compliance]

URL = "/fr/partenaires/"
REF = "e-mail du référent du 2026-10-05"


def make(name, *, authorized=False, status=PublicationStatus.PUBLISHED, reference="", kind=PartnerKind.COMPANY):
    return Partner.objects.create(
        name=name, kind=kind, authorized=authorized, authorization_reference=reference, status=status
    )


def test_no_page_and_no_link_while_nothing_is_authorised(client, seeded):
    """V5.12 §8: no «partners to come» page — the index answers 404 and nothing links to it until a partner is
    authorised in writing (G6); the home's ecosystem shows the promoter alone."""
    from core import gates
    from partners.sitemaps import PartnersSitemap

    make("Partenaire non autorisé", authorized=False)
    make("Autorisé mais brouillon", authorized=True, reference=REF, status=PublicationStatus.DRAFT)
    assert gates.partners_public() is False
    for lang in ("fr", "it", "en", "ar"):
        assert client.get(f"/{lang}/partenaires/").status_code == 404, lang
    assert PartnersSitemap().items() == []
    for path in ("/fr/", "/fr/reseau/", "/fr/agami/", "/fr/institutions/", "/fr/projet-pilote/"):
        response = client.get(path)
        if response.status_code != 200:  # a Phase 3 page closed in this state
            continue
        html = response.content.decode()
        assert 'href="/fr/partenaires/"' not in html, path
        assert "au fur et à mesure" not in html, path
    home = client.get("/fr/").content.decode()
    assert "home-ecosystem__grid--single" in home and "home-ecosystem__partners" not in home


def test_the_page_and_its_links_appear_with_an_authorised_partner(client, seeded):
    from core import gates
    from partners.sitemaps import PartnersSitemap

    make("Partenaire autorisé", authorized=True, reference=REF)
    assert gates.partners_public() is True
    assert client.get(URL).status_code == 200
    assert PartnersSitemap().items() == ["partners:index"]
    home = client.get("/fr/").content.decode()
    assert 'href="/fr/partenaires/"' in home and "home-ecosystem__grid--single" not in home


def test_authorised_and_published_partner_is_listed(client, seeded):
    make("Partenaire autorisé", authorized=True, reference=REF)
    html = client.get(URL).content.decode()
    assert "Partenaire autorisé" in html
    assert "au fur et à mesure des autorisations" not in html.split("partners__group")[1]


def test_authorised_but_draft_partner_is_hidden(client, seeded):
    make("Brouillon autorisé", authorized=True, reference=REF, status=PublicationStatus.DRAFT)
    html = client.get(URL).content.decode()
    assert "Brouillon autorisé" not in html
    assert list(authorized_partners()) == []


def test_archived_partner_disappears(client, seeded):
    p = make("Ancien partenaire", authorized=True, reference=REF)
    assert "Ancien partenaire" in client.get(URL).content.decode()
    p.status = PublicationStatus.ARCHIVED
    p.save()
    assert "Ancien partenaire" not in client.get(URL).content.decode()


def test_authorisation_requires_written_reference_model_and_db():
    p = Partner(name="X", kind=PartnerKind.COMPANY, authorized=True, authorization_reference="")
    with pytest.raises(ValidationError):
        p.full_clean()
    with pytest.raises(IntegrityError), transaction.atomic():
        Partner.objects.create(name="Y", kind=PartnerKind.COMPANY, authorized=True, authorization_reference="")


def test_authorized_at_is_set_and_cleared():
    p = make("Z", authorized=True, reference=REF)
    assert p.authorized_at is not None
    p.authorized = False
    p.save()
    assert p.authorized_at is None
    assert p.is_public is False


def test_logo_never_rendered_without_authorisation(client, seeded):
    from cms.models import MediaAsset

    asset = MediaAsset.objects.create(title="logo test", file="media/test/logo.png", alt_fr="Logo test")
    p = make("Avec logo", authorized=False)
    p.logo = asset
    p.save()
    html = client.get(URL).content.decode()
    assert "logo.png" not in html
    assert p.logo_public is False
    p.authorized = True
    p.authorization_reference = REF
    p.save()
    assert p.logo_public is True
    html = client.get(URL).content.decode()
    assert "logo.png" in html
    assert 'alt="Logo test"' in html


def test_partners_page_is_compliant(client, seeded):
    make("Partenaire autorisé", authorized=True, reference=REF)
    for lang in ("fr", "it", "en", "ar"):
        html = client.get(f"/{lang}/partenaires/").content.decode()
        assert not scan(html), lang
        assert "Italy Legal Entry™" in html
        assert "®" not in html
        assert "application/ld+json" not in html  # JSON-LD: none by design


def test_seed_creates_only_unauthorised_slots(seeded):
    from partners.seeds import seed_patronage_slots

    first = seed_patronage_slots()
    second = seed_patronage_slots()
    assert "0 patronage slot(s) created" in second or "created" in first
    assert Partner.objects.filter(authorized=True).count() == 0
    assert Partner.objects.filter(name="Commune de Rovigo", status=PublicationStatus.DRAFT).exists()
    assert list(authorized_partners()) == []
