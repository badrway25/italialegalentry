from core.seeds import register_seed
from legal.drafts import load_drafts
from legal.services import ensure_documents, invalidate


@register_seed("legal.documents", order=15)
def seed_legal_documents():
    created = ensure_documents()
    return f"{created} legal document row(s) created (status BLOCKED until official Italian text is supplied)"


@register_seed("legal.verified_processing_drafts", order=16)
def seed_privacy_and_cookie_drafts():
    """V5.14: the privacy and cookie information as DRAFTS (never published by a seed)."""
    updated = load_drafts()
    invalidate()
    return f"{updated} privacy/cookie draft(s) written from the verified processing (unpublished)"
