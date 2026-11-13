"""
V5.12 (Director's decisions §8, D-17): the footer's version label leaves the public footer — its default is emptied,
and a row still holding the old default is blanked. A label somebody wrote in the back office is kept.
"""

from django.db import migrations, models

OLD_DEFAULT = "v2.0.0 — Fase 1"


def blank_the_old_default(apps, schema_editor):
    SiteSettings = apps.get_model("core", "SiteSettings")
    SiteSettings.objects.filter(version_label=OLD_DEFAULT).update(version_label="")


def restore_the_old_default(apps, schema_editor):
    SiteSettings = apps.get_model("core", "SiteSettings")
    SiteSettings.objects.filter(version_label="").update(version_label=OLD_DEFAULT)


class Migration(migrations.Migration):
    dependencies = [("core", "0001_initial")]

    operations = [
        migrations.AlterField(
            model_name="sitesettings",
            name="version_label",
            field=models.CharField(
                blank=True, default="", max_length=60, verbose_name="indicazione di versione (footer)"
            ),
        ),
        migrations.RunPython(blank_the_old_default, restore_the_old_default),
    ]
