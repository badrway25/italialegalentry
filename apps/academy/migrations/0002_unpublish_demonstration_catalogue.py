"""
V5.12 §8 (Director's decisions: the Academy demonstration catalogue is HIDDEN). Until this release ``academy.catalogue``
seeded seven invented courses in every environment, production included, and every account saw them. The seed is now
gated by ``core.seeds.demonstration_data_allowed()``; this data step takes back what an earlier deploy wrote — on an
environment where demonstration data is NOT allowed, the seeded courses (their slugs, frozen here) leave the catalogue:
published becomes draft. Nothing is deleted: an enrolment keeps its course, and the back office can still read it.
Where demonstration data is allowed (development, the design preview), nothing changes.
"""

from django.db import migrations

#: The slugs ``academy.seeds.COURSES`` wrote, as of this release.
SEEDED_COURSES = (
    "italien-a1",
    "droits-et-devoirs",
    "education-civique",
    "securite-au-travail",
    "culture-du-travail",
    "metiers-agroalimentaire",
    "preparation-au-depart",
    "italien-a2-preparation",
)


def unpublish_where_not_allowed(apps, schema_editor):
    from core.seeds import demonstration_data_allowed

    if demonstration_data_allowed():
        return
    Course = apps.get_model("academy", "Course")
    Course.objects.filter(slug__in=SEEDED_COURSES, status="published").update(status="draft")


class Migration(migrations.Migration):
    dependencies = [("academy", "0001_initial")]

    operations = [migrations.RunPython(unpublish_where_not_allowed, migrations.RunPython.noop)]
