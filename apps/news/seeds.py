"""
News seeds — idempotent. Only the initial category set is created; NO article is seeded
(the CMS starts empty, workflow DRAFT → REVIEW → PUBLISHED → ARCHIVED — docs/CONTENT_SOURCE_MAP.md §6).
"""

from __future__ import annotations

from django.conf import settings
from django.contrib.auth.models import Group, Permission

from core.models import FeatureFlag
from core.seeds import register_seed
from news.models import NewsCategory

# (slug, order, {lang: label}) — category labels are editorial UI content (not prescribed texts), so
# they are provided in the four languages; editors can change them in the back-office.
CATEGORIES: tuple[tuple[str, int, dict[str, str]], ...] = (
    ("normativa", 10, {"fr": "Normativa", "it": "Normativa", "en": "Legislation", "ar": "المستجدات القانونية"}),
    ("echeances", 20, {"fr": "Échéances", "it": "Scadenze", "en": "Deadlines", "ar": "المواعيد الرسمية"}),
    ("forum", 30, {"fr": "Forum", "it": "Forum", "en": "Forum", "ar": "المنتدى"}),
    ("ecosysteme", 40, {"fr": "Écosystème", "it": "Ecosistema", "en": "Ecosystem", "ar": "المنظومة"}),
)


@register_seed("news.categories", order=40)
def seed_categories() -> str:
    created = 0
    for slug, order, names in CATEGORIES:
        obj, was_created = NewsCategory.objects.get_or_create(
            slug=slug, defaults={"name_fr": names["fr"], "order": order}
        )
        created += int(was_created)
        # Fill only the labels an editor has not written yet (never overwrite editorial changes).
        missing = [lang for lang in ("it", "en", "ar") if not getattr(obj, f"name_{lang}")]
        for lang in missing:
            setattr(obj, f"name_{lang}", names[lang])
        if missing:
            obj.save(update_fields=[f"name_{lang}" for lang in missing])
    return f"{created} category(ies) created, {len(CATEGORIES)} ensured; no article seeded"


@register_seed("news.newsletter_flag", order=41)
def seed_newsletter_flag() -> str:
    """Ensure the newsletter flag row exists, inactive and date-bound to Phase 3 (G3) by default."""
    _row, created = FeatureFlag.objects.get_or_create(
        key="newsletter",
        defaults={
            "enabled": False,
            "enabled_from": settings.ILE["PHASE3_DATE"],
            "note": "Newsletter « Restez informés » — Phase 3 (§3.8.6): activer uniquement à partir du 2 octobre 2026",
        },
    )
    return "newsletter flag row created (disabled, from 2026-10-02)" if created else "newsletter flag row present"


@register_seed("news.publish_permission", order=42)
def seed_publish_permission() -> str:
    """Grant ``news.publish_article`` to the administrator role (idempotent, additive)."""
    perm = Permission.objects.filter(content_type__app_label="news", codename="publish_article").first()
    if perm is None:
        return "publish_article permission not yet available"
    group, _created = Group.objects.get_or_create(name="role:administrator")
    group.permissions.add(perm)
    return "news.publish_article granted to role:administrator"
