"""
V5.19 (owner-confirmed, 29 October 2026; lane v519-k): the site's two public telephone channels join its settings —
the Numero Verde 800 642 015 and WhatsApp (core.contact). AddField writes the Numero Verde into the existing
singleton through its default; the data step states it for a row that would hold none.

V5.20 (option B): the owner-confirmed WhatsApp number is configured outside the repository (V5.19/V5.20) — no file of
the repository writes it, this one included. AddField leaves it blank; the data step copies the environment's value
(settings.ILE["WHATSAPP_NUMBER"], from ILE_WHATSAPP_NUMBER) into a singleton that holds none, when one is configured;
then the field takes its default from the environment for every row made later (core.contact.default_whatsapp_number:
a name, never a number).
"""

import core.contact
from django.conf import settings
from django.db import migrations, models

FREEPHONE = "800642015"


def set_the_confirmed_numbers(apps, schema_editor):
    SiteSettings = apps.get_model("core", "SiteSettings")
    SiteSettings.objects.filter(freephone_number="").update(freephone_number=FREEPHONE)
    whatsapp = settings.ILE["WHATSAPP_NUMBER"]
    if whatsapp:
        SiteSettings.objects.filter(whatsapp_number="").update(whatsapp_number=whatsapp)


class Migration(migrations.Migration):
    dependencies = [("core", "0002_version_label_blank")]

    operations = [
        migrations.AddField(
            model_name="sitesettings",
            name="freephone_number",
            field=models.CharField(
                blank=True,
                default=FREEPHONE,
                help_text="Le sole cifre o con spazi: 800 xxx xxx. Il sito lo mostra come «800 xxx xxx».",
                max_length=20,
                validators=[core.contact.validate_national_number],
                verbose_name="numero verde",
            ),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="whatsapp_number",
            field=models.CharField(
                blank=True,
                default="",
                help_text="In formato internazionale: +39 3xx xxx xxxx. Il link aperto è https://wa.me/ seguito dalle cifre.",
                max_length=20,
                validators=[core.contact.validate_international_number],
                verbose_name="numero WhatsApp",
            ),
        ),
        migrations.RunPython(set_the_confirmed_numbers, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="sitesettings",
            name="whatsapp_number",
            field=models.CharField(
                blank=True,
                default=core.contact.default_whatsapp_number,
                help_text="In formato internazionale: +39 3xx xxx xxxx. Il link aperto è https://wa.me/ seguito dalle cifre.",
                max_length=20,
                validators=[core.contact.validate_international_number],
                verbose_name="numero WhatsApp",
            ),
        ),
    ]
