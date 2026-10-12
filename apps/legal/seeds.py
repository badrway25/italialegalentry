from core.seeds import register_seed
from legal.services import ensure_documents


@register_seed("legal.documents", order=15)
def seed_legal_documents():
    created = ensure_documents()
    return f"{created} legal document row(s) created (status BLOCKED until official Italian text is supplied)"
