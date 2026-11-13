"""
``manage.py legal_publish privacy cookies --by <e-mail>`` — publish legal documents through ``legal.services.publish``.

The same rules as the back office's «Pubblica testo ufficiale» action: the account must hold the publication
permission, the text must exist and name its source, and — outside a preview — no open field «[DA COMPLETARE …]»
may remain (V5.14). Publishing the privacy and cookie information this way opens no form: gate G1 waits for all
five documents.
"""

from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied, ValidationError
from django.core.management.base import BaseCommand, CommandError

from legal.models import LegalKind
from legal.services import get_document, publish


class Command(BaseCommand):
    help = "Publish legal documents (privacy, cookies, notices, terms, disclaimer) as the given account."

    def add_arguments(self, parser):
        parser.add_argument("kinds", nargs="+", choices=LegalKind.values)
        parser.add_argument("--by", required=True, help="E-mail of an account allowed to publish legal documents.")

    def handle(self, *args, **options):
        user = get_user_model().objects.filter(email__iexact=options["by"]).first()
        if user is None:
            raise CommandError("No account with that e-mail address.")
        failed = False
        for kind in options["kinds"]:
            document = get_document(kind)
            try:
                publish(document, user)
            except PermissionDenied:
                raise CommandError("This account may not publish legal documents.") from None
            except ValidationError as exc:
                failed = True
                self.stderr.write(f"{kind}: NOT published — {'; '.join(exc.messages)}")
                continue
            self.stdout.write(f"{kind}: published, v{document.version}")
        if failed:
            raise CommandError("At least one document was not published.")
