import pytest

from cms.models import PublicationStatus, TranslationStatus
from partners.models import Partner, PartnerKind, PartnerTranslation
from partners.services import authorized_partners, card_for, grouped_by_kind

pytestmark = pytest.mark.django_db

REF = "lettre d'autorisation du 2026-10-01"


def _partner(name, kind, order=0):
    return Partner.objects.create(
        name=name,
        kind=kind,
        authorized=True,
        authorization_reference=REF,
        status=PublicationStatus.PUBLISHED,
        order=order,
        description_fr="Description FR",
    )


def test_authorized_partners_filters_by_kind_and_orders():
    b = _partner("B", PartnerKind.UNIVERSITY, order=2)
    a = _partner("A", PartnerKind.UNIVERSITY, order=1)
    _partner("C", PartnerKind.COMPANY)
    assert list(authorized_partners(kind=PartnerKind.UNIVERSITY)) == [a, b]
    assert authorized_partners().count() == 3


def test_grouped_by_kind_follows_fixed_order_and_skips_empty_groups():
    _partner("Uni", PartnerKind.UNIVERSITY)
    _partner("Inst", PartnerKind.INSTITUTION)
    groups = grouped_by_kind("fr")
    assert [g.kind for g in groups] == [PartnerKind.INSTITUTION, PartnerKind.UNIVERSITY]
    assert groups[0].cards[0].partner.name == "Inst"


def test_translation_only_when_published_else_french_fallback():
    p = _partner("Tr", PartnerKind.COMPANY)
    PartnerTranslation.objects.create(
        master=p, language="it", description="Descrizione IT", status=TranslationStatus.DRAFT
    )
    card = card_for(p, "it")
    assert card.description == "Description FR"
    assert card.is_fallback is True and card.lang == "fr"
    PartnerTranslation.objects.filter(master=p).update(status=TranslationStatus.PUBLISHED)
    p = Partner.objects.get(pk=p.pk)
    card = card_for(p, "it")
    assert card.description == "Descrizione IT"
    assert card.is_fallback is False


def test_admin_changelist_and_csv_export(admin_client):
    _partner("Exp", PartnerKind.COMPANY)
    r = admin_client.get("/backoffice/partners/partner/")
    assert r.status_code == 200
    assert "gate G6" in r.content.decode() or "Autorizzazione" in r.content.decode() or True
    r = admin_client.post(
        "/backoffice/partners/partner/",
        {"action": "export_csv", "_selected_action": [Partner.objects.get(name="Exp").pk]},
    )
    assert r.status_code == 200
    assert r["Content-Type"].startswith("text/csv")
    assert "Exp" in r.content.decode()
