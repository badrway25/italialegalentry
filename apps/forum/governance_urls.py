"""
URLs of the Forum Permanent governance module (FORUM_GOVERNANCE §7).

Every route requires an authenticated account AND an open ``virtual_forum`` gate, so none of them
is registered in ``core.public_routes``: nothing here must ever answer 200 to an anonymous crawler.

The include belongs to ``config/urls.py``, which this lane does not own. It is requested in the
result as a shared-file change, to be inserted INSIDE ``i18n_patterns`` and BEFORE the portal's own
catch-all mount, exactly as the other platform modules are::

    path("espace-reserve/forum-permanent/", include("forum.governance_urls", namespace="forum_governance")),

Until that line exists the module is simply unreachable — ``core.links.public_url`` returns "" for
every name below, so no template renders a dead link — and the test suite mounts it through
``apps/forum/tests/governance_urlconf.py``.

The path segments are French because French is the source language of the platform; the state names
in the URLs are not, and are not meant to be: ``/propositions/<uuid>/etat/`` takes the target state
in the POST body, so a bookmark can never carry a transition.
"""

from django.urls import path

from forum import governance_views as views

app_name = "forum_governance"

urlpatterns = [
    path("", views.participation, name="participation"),
    path("commissions/", views.commissions, name="commissions"),
    path("commissions/<slug:key>/", views.commission_detail, name="commission_detail"),
    path("commissions/<slug:key>/proposer/", views.proposal_create, name="proposal_create"),
    path("commissions/<slug:key>/tables/<slug:table_key>/", views.table_detail, name="table_detail"),
    path("propositions/", views.proposals, name="proposals"),
    path("propositions/<uuid:uuid>/", views.proposal_detail, name="proposal_detail"),
    path("propositions/<uuid:uuid>/etat/", views.proposal_transition, name="proposal_transition"),
    path("projets/", views.projects, name="projects"),
    path("projets/<uuid:uuid>/", views.project_detail, name="project_detail"),
    path("relation-annuelle/", views.annual_report, name="annual_report"),
    path("relation-annuelle/<int:year>/", views.annual_report, name="annual_report_year"),
]
