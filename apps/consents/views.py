from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods

from consents.models import NewsletterSubscription
from consents.services import withdraw
from core import clock


@require_http_methods(["GET", "POST"])
def newsletter_confirm(request, token: str):
    sub = get_object_or_404(NewsletterSubscription, confirm_token=token)
    if request.method == "POST" and not sub.confirmed_at:
        sub.confirmed_at = clock.now()
        sub.save(update_fields=["confirmed_at"])
    return render(request, "consents/newsletter_confirm.html", {"subscription": sub})


@require_http_methods(["GET", "POST"])
def newsletter_unsubscribe(request, token: str):
    sub = get_object_or_404(NewsletterSubscription, unsubscribe_token=token)
    if request.method == "POST" and not sub.unsubscribed_at:
        sub.unsubscribed_at = clock.now()
        sub.save(update_fields=["unsubscribed_at"])
        withdraw(sub.consent, note="newsletter unsubscribe link")
    return render(request, "consents/newsletter_unsubscribe.html", {"subscription": sub})
