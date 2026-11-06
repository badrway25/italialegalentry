"""
``manage.py preview_data_clean [--apply]`` — the preview's rows made fit for the owner's acceptance
(designpreview.preview_data; V5.12 §11–§13). DEVELOPMENT ONLY: the command exists only where the preview is installed
(dev.py, ``ILE_DESIGN_PREVIEW=1``), and refuses any database that is not a preview's (``ile_v5`` and its lane clones —
never ``ile`` or ``ile_qa``, the V4 control's). Without ``--apply`` it lists what it would change and changes nothing.
"""

from __future__ import annotations

from django.core.management.base import BaseCommand, CommandError

from designpreview import personas, preview_data
from designpreview.live import _TICKET


class Command(BaseCommand):
    help = "Rewrite the preview database's fixture names and test rows as a finished product shows them (dev only)."

    def add_arguments(self, parser):
        parser.add_argument("--apply", action="store_true", help="make the changes (default: list them only)")

    def handle(self, *args, apply: bool = False, **options):
        name = personas.database_name()
        if not personas.database_allowed(name):
            raise CommandError(f"refused: «{name}» is not a preview database (ILE_DESIGN_PREVIEW_ALLOWED_DATABASES)")
        report = preview_data.clean(apply=apply, keep_ticket=_TICKET)
        for line in report.changes:
            self.stdout.write(line)
        verb = "changed" if apply else "would change (dry run; --apply to make them)"
        self.stdout.write(f"{len(report.changes)} value(s) {verb} on {name}")
