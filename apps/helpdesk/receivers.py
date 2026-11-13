"""
The escalation seam, wired as a signal.

When the rule engine freezes an outcome of ``REVIEW_REQUIRED`` onto a case file, a request is opened
at the help desk. That is the whole promise of Technical Blueprint §13 — «escalation dall'orientamento
automatico al supporto umano» — and it has to happen in the domain rather than in one view, or the
promise would hold only for whichever screen remembered to call it.

It is a receiver rather than a call inside ``cases.services.record_assessment`` because the case file
is not this module's to edit, and because the coupling belongs on this side: the case file must keep
working with the help desk absent, which it does — nothing in ``cases`` imports ``helpdesk``.

The receiver is deliberately narrow: creation only, ``REVIEW_REQUIRED`` only, idempotent through the
unique constraint on the assessment. It writes no answer and notifies no third party.
"""

from __future__ import annotations

import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

log = logging.getLogger("ile.helpdesk")


@receiver(post_save, dispatch_uid="helpdesk.escalate_review_required")
def escalate_review_required(sender, instance, created, **kwargs):
    from cases.models import AssessmentOutcome, PathwayAssessment

    if sender is not PathwayAssessment or not created:
        return
    if instance.outcome != AssessmentOutcome.REVIEW_REQUIRED:
        return

    from helpdesk import services

    ticket = services.open_from_assessment(instance)
    if ticket is not None:
        log.info(
            "helpdesk escalation opened",
            extra={"event": "helpdesk.escalation", "target": f"HelpdeskTicket:{ticket.pk}"},
        )
