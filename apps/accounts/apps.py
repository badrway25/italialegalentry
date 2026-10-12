from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"
    verbose_name = "Account & RBAC"

    def ready(self):
        from django.contrib.auth.signals import user_logged_in

        import accounts.checks  # noqa: F401 — registers the deploy-time MFA checks
        from accounts import signals
        from core.public_routes import register_public_paths

        # The entrance release of the loader «Lume» (V5.4 plan §1.9, W1-D): a successful sign-in leaves the flag
        # the first console page consumes (accounts.signals). Connected here, as the audit trail connects its own.
        user_logged_in.connect(signals.mark_entrance_release, dispatch_uid="accounts.entrance_release")

        register_public_paths(
            "accounts",
            ["compte/login/", "compte/signup/", "compte/password/reset/", "compte/profil/suppression/confirmee/"],
        )
