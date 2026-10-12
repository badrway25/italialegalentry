"""Small helpers referenced by settings (kept import-light: no model import at module level)."""

from __future__ import annotations


def user_display(user) -> str:
    """How a user is named in account messages (ACCOUNT_USER_DISPLAY): full name, else e-mail."""
    return (getattr(user, "full_name", "") or "").strip() or getattr(user, "email", "") or str(user)
