"""
V5 live preview — DEVELOPMENT ONLY (Design V5.2, stream B; owner's directives V5.1 §2–§5, §80,
V5.2 §7, §40 and V5.4 «EXECUTION MODE»).

Since V5.4 (4 October 2026; docs/design-v5/V5_4_EXECUTION_PLAN.md §4) the preview is the LIVE V5
PRODUCT, not a catalogue of options:

* ``/__design-v5/`` opens the current best V5 — the real ``/fr/`` page of this server, full window,
  in one same-origin frame — under a slim strip outside the page: the build, the state of the page
  («V5 — council-passed» or «V4 + fondation», from the steward's ``live_status.json``), its
  languages, the frame (the window or a phone of 390), the personas, the steward's changelog, the
  index and the page alone (designpreview.live);
* ``/__design-v5/index/`` lists every live surface, public and authenticated, in fr and ar, with
  frames on demand — one pair at a time — the families' state, the foundation's specimen boards
  and the V4 control on 8771;
* ``POST /__design-v5/accedi/<persona>/`` and ``POST /__design-v5/esci/`` sign this browser in and
  out as one of the preview database's four QA accounts, read-only, without a password
  (designpreview.personas);
* ``/__design-v5/research/`` is the research archive: the gate-0 comps of
  ``C:/tmp/ile_v5_council/proof`` and the research prototypes, with the hero and type pickers, the
  compare view and the proof files, as they were — every candidate labelled «prototipo di ricerca —
  non approvato» (designpreview.services). The old addresses redirect.

It exists in a process only when BOTH hold:

* ``settings.DEBUG`` is true, and
* the environment variable ``ILE_DESIGN_PREVIEW=1`` is set (read by ``config/settings/dev.py``).

and it answers only a loopback caller with no proxy header, on this process's own ``Host``
(designpreview.access).

Removal footprint — six things, nothing else in the repository knows about the preview:
``apps/designpreview/``, ``templates/dev/designpreview/``, ``static/css/dev/designpreview.css``,
``static/js/dev/designpreview.js``, the ``ILE_DESIGN_PREVIEW*`` block in ``config/settings/dev.py``
(with the middleware it adds and the distinct cookie names) and the conditional mount in
``config/urls.py`` (inside the existing ``if settings.DEBUG:`` block).

Nothing here changes production: the global Content-Security-Policy is untouched (the directives the
preview's pages need are applied per view, with django-csp's decorators, and a real page is framed
only through ``designpreview.frames``, under its narrow condition), the production cascade does not
import the dev stylesheet, and everything the preview answers an allowed caller with says
``X-Robots-Tag: noindex, nofollow`` and ``Cache-Control: no-store``. A caller who is not allowed
meets Django's own 404, which carries nothing of the preview.
"""
