"""
Personal-data hooks of the company workspace.

``companies_export_section`` — GDPR art. 15/20. A company profile holds the personal data of ONE
natural person, the named contact with their function; the needs hold none. The export therefore
returns the company identity as held, and the needs as a summary, for the account that is a member
of the organisation — and for nobody else, since it is reached through ``readable_by``.

There is no anonymisation receiver that deletes a company: an organisation is a legal person, its
needs are its own records, and erasing an account does not erase the company's file. What the
anonymisation of an account must not leave behind is the contact's personal data — so the contact
fields are scrubbed instead, and the company stays, which is the honest outcome.
"""

from __future__ import annotations

from companies.models import CompanyNeed, CompanyProfile


def companies_export_section(user) -> dict:
    profiles = CompanyProfile.objects.readable_by(user).filter(organisation__memberships__user=user).distinct()
    return {
        "companies": [
            {
                "legal_name": profile.legal_name,
                "trade_name": profile.trade_name,
                "registration_number": profile.registration_number,
                "vat_number": profile.vat_number,
                "sector": profile.sector.label_fr if profile.sector_id else "",
                "size": profile.size,
                "year_founded": profile.year_founded,
                "contact_name": profile.contact_name,
                "contact_function": profile.contact_function,
                "contact_email": profile.contact_email,
                "contact_phone": profile.contact_phone,
                "address": profile.display_address,
                "verification_status": profile.verification_status,
                "created_at": profile.created_at,
            }
            for profile in profiles
        ],
        "needs": [
            {
                "reference": need.reference,
                "title": need.title,
                "territory": need.territory.label_fr if need.territory_id else "",
                "sector": need.sector.label_fr if need.sector_id else "",
                "professional_profile": need.professional_profile,
                "headcount": need.headcount,
                "status": need.status,
                "created_at": need.created_at,
                "submitted_at": need.submitted_at,
            }
            for need in CompanyNeed.objects.filter(company__in=profiles).order_by("-created_at")
        ],
    }
