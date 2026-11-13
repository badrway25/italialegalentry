from accounts.roles import ensure_roles
from core.seeds import register_seed


@register_seed("accounts.roles", order=10)
def seed_roles():
    created = ensure_roles()
    return f"{created} role group(s) created; permissions synchronised"
