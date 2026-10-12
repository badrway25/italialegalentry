from consents.models import ConsentPurpose
from consents.services import ensure_consent_text
from core.seeds import register_seed


@register_seed("consents.texts", order=20)
def seed_consent_texts():
    for purpose in ConsentPurpose.values:
        ensure_consent_text(purpose)
    return f"{len(ConsentPurpose.values)} consent purposes ensured"
