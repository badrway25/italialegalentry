from django.apps import AppConfig


class AuditConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "audit"
    verbose_name = "Audit trail"

    def ready(self):
        from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed

        from audit import receivers, signals  # noqa: F401

        # Authentication events: REQ-SEC-06 lists them first and coverage was zero until 20/09/2026.
        user_logged_in.connect(receivers.on_user_logged_in, dispatch_uid="audit.login")
        user_logged_out.connect(receivers.on_user_logged_out, dispatch_uid="audit.logout")
        user_login_failed.connect(receivers.on_user_login_failed, dispatch_uid="audit.login_failed")
