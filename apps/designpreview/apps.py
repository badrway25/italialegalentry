from django.apps import AppConfig


class DesignPreviewConfig(AppConfig):
    """Registered by config/settings/dev.py only when DEBUG is on and ILE_DESIGN_PREVIEW=1."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "designpreview"
    verbose_name = "Anteprima V5 (sviluppo)"
