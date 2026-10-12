from __future__ import annotations

import logging

from audit.models import AuditEvent
from core.privacy import hashed_client_ip

log = logging.getLogger("ile.audit")


def _label(obj) -> str:
    """
    Readable label for the audit row, pseudonymised when the account has been anonymised.

    ``anonymise_user`` rewrites the labels of existing rows, but events keep arriving afterwards —
    the logout that follows a self-service deletion, a background job, a late signal. Labelling them
    here rather than scrubbing afterwards means the invariant holds for every event, whenever it is
    written, instead of only for those that existed at the moment of anonymisation.

    Two narrownesses that were not here at first, and each fixes something real:

    * **Only a User is pseudonymised.** ``anonymise_user`` rewrites the anonymised address onto the
      person's consents and newsletter subscriptions as well, so the old test — "does this object's
      e-mail end with the anonymised domain" — matched a ``ConsentRecord`` too and labelled the row
      ``user:<consent id> (anonymised)``. A wrong user id inside an audit trail is worse than no
      label at all, because it reads as a fact.

    * **``email`` is only treated as an address when it IS one.** A model whose ``email`` is a
      foreign key would make ``.endswith`` raise, and a failure in ``record()`` takes down the
      operation it was meant to witness. The audit trail must never be the thing that breaks.
    """
    from django.contrib.auth import get_user_model

    from accounts.services import ANONYMISED_DOMAIN, anonymised_label_for

    if isinstance(obj, get_user_model()):
        email = getattr(obj, "email", "")
        if isinstance(email, str) and email.endswith("@" + ANONYMISED_DOMAIN):
            return anonymised_label_for(obj.pk)
    return str(obj)


def record(request=None, *, action: str, target=None, metadata: dict | None = None, actor=None) -> AuditEvent:
    actor = actor or (getattr(request, "user", None) if request is not None else None)
    if actor is not None and not getattr(actor, "is_authenticated", False):
        actor = None
    event = AuditEvent.objects.create(
        actor=actor,
        actor_label=_label(actor) if actor else "anonymous",
        action=action,
        target_type=type(target).__name__ if target is not None else "",
        target_id=str(getattr(target, "pk", "") or "") if target is not None else "",
        target_repr=_label(target)[:200] if target is not None else "",
        metadata=metadata or {},
        ip_hash=hashed_client_ip(request) if request is not None else "",
        request_id=getattr(request, "request_id", "") if request is not None else "",
    )
    # The DATABASE row keeps the readable label and repr: it is the audit trail, it is access
    # controlled, and an auditor needs to read it. The LOG STREAM does not: it is shipped, copied,
    # retained by other systems and often read by people with no business seeing personal data.
    # ``actor_label`` is the account's e-mail address and ``target_repr`` is, for a document, the
    # uploaded file name — both personal data. Only identifiers go to the stream, so a reader who
    # needs the detail must go through the audit trail and be authorised for it.
    log.info(
        "audit %s",
        action,
        extra={
            "event": action,
            "actor": f"user:{actor.pk}" if actor is not None else "anonymous",
            "target": f"{event.target_type}:{event.target_id}" if event.target_type else "-",
        },
    )
    return event
