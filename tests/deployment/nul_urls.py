"""
URLconf of tests/deployment/test_nul_bytes.py: the project's own patterns and handlers, plus two views.

* One reads a form field without a form and looks it up in the database — as the views that store a posted value as
  they receive it do (cases.views.transition and a transition's reason, the selection views and their notes). Django's
  form fields refuse a NUL themselves (ProhibitNullCharactersValidator); a value read straight from request.POST meets no
  such check.
* One is csrf_exempt and reads its raw body, as the integrations API does (integrations.api.api_endpoint; the public
  webhook, integrations.views.inbound_webhook). Once Django has parsed a multipart body from the request's stream, the
  raw body can no longer be read (RawPostDataException).
"""

from django.http import HttpResponse
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from cms.models import Redirect
from config.urls import handler400, handler403, handler404, handler500  # noqa: F401 — the project's handlers
from config.urls import urlpatterns as project_urlpatterns


def looks_the_field_up(request):
    Redirect.objects.filter(old_path=request.POST.get("old_path", "")).exists()
    return HttpResponse(f"looked up; files received: {len(request.FILES)}", content_type="text/plain")


@csrf_exempt
def reads_its_body(request):
    return HttpResponse(f"read its body: {len(request.body)} bytes", content_type="text/plain")


urlpatterns = [
    path("__nul__/lookup/", looks_the_field_up),
    path("__nul__/raw/", reads_its_body),
    *project_urlpatterns,
]
