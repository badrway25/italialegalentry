from django.apps import AppConfig


class IntegrationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "integrations"
    verbose_name = "Integrazioni (CRM / API)"

    def ready(self):
        from integrations.signals import connect_receivers

        connect_receivers()
