from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"
    verbose_name = "Account & RBAC"

    def ready(self):
        import accounts.checks  # noqa: F401 — registers the deploy-time MFA checks
        from core.public_routes import register_public_paths

        register_public_paths(
            "accounts",
            ["compte/login/", "compte/signup/", "compte/password/reset/", "compte/profil/suppression/confirmee/"],
        )
