# Review — lane P3 (label v517-p3-review), branch v517-p3 @ 52b9e08 (base design-v5 e580b41)

Verdict: **APPROVE_WITH_FIXES** — nothing blocks the merge; the fixes below are minor and can ride a follow-up.
No file was changed by the review.

## What was checked

- Directive V5.17 read in full; the diff (28 files) read in full.
- Targeted pytest on lane l9 (apps/documents, apps/helpdesk, apps/legal, apps/cases, tests/deployment):
  **632 passed, 3 skipped, 0 failed** (10 min 37 s).
- LF only in every changed file. No secret, personal datum or server identity added (the prod-settings subprocess
  test uses obviously fake keys and example.com).

## Findings by point

1. **Status names** — exact and consistent. The runbook *States* quotes V5.17 §2 verbatim; checklist §A, release
   notes §5, `apps/legal/models.py`, PRIVACY_PROCESSING_AUDIT §6 use COMPLIANCE_REVIEW_COMPLETE. PRIVACY_CONTENT_COMPLETE
   survives only as «the name it replaced» and in historical records (OWNERSHIP_V54.json title, P2 notes, decision
   log). A new test pins this. **Nothing compliance-related blocks PRODUCT_COMPLETE** in any doc or test (grep).
2. **DPIA** — art. 35(7) structure complete. Spot-checked citations all resolve (MFA_REQUIRED_ROLES,
   DOWNLOAD_LINK_MINUTES, validate_upload, SESSION_COOKIE_AGE = 8 h, ANONYMOUS_SESSION_TTL_DAYS = 30,
   MAX_DISCLOSURE_DAYS = 180, the selection model's no-age/nationality rule, account deletion routes,
   ILE["PROMOTER"], log_filters, test files). Open facts D-1…D-10 are genuinely unknown; no invented basis,
   retention, controller or DPO. Ratings labelled preliminary. DPIA_NECESSITY conclusion matches §3 wording.
3. **R-SC-1** — real control: base False, prod.py False and refuses True without the basis reference (proved in a
   subprocess, with DJANGO_DEBUG=1 so the preview's switch cannot leak); presenter, view, service (any road) and the
   loose-upload form all ask the guard. DENY tests read the real roads (page, register, form post, Dépôt JSON,
   service, DB counts) and ALLOW tests mirror them. No consent box, nothing deleted. The closed sentence is finished,
   calm, in the catalogue's helpdesk names.
4. **OF-11** — stays OPEN; the two rows match the lane P audit's §6 items 1–2 (external-provider IP; browser storage)
   and the repo audit §5 items 1–2. Quotes verified in `apps/cms/locked_content.py` (legal.cookies.fr_courtesy) and
   `apps/legal/content/cookies/fr.txt` (§1 sentence, §3 heading); storage keys verified in static/js/src. Acceptance
   row empty. The other ANX departures (§5 items 3–7) are correctly left to their own OFs.
5. **Production privacy page test** — meaningful: whole page, four languages, both a published row with markers and a
   fully filled body (asserts the body really renders), forbidden list built from OPEN_FIELD_CLASSES plus an OF-id
   regex.
6. **Visual lanes' files** — none touched (no base/header/footer/gates.py/portal templates/static). One recorded slice
   in `templates/cases/partials/state_dialog.html` (w3-e), one line, listed in NOTES with request R-P3-1.

## Minor fixes (list, not applied)

- M-1 `apps/core/special_category.py` SPECIAL_CATEGORY_TERMS: the bare stem `biometri` would close an ordinary piece
  such as «Passeport biométrique» or «Photo d’identité biométrique» (a photo is biometric data only when processed
  for unique identification, recital 51). No current requirement triggers it. Fix: replace with «donnees
  biometriques», «dati biometrici», «biometric data» (fingerprints already listed) and add both titles to
  `test_an_ordinary_piece_is_not_closed`.
- M-2 Same function reads `requirement.detail`: a detail that says what NOT to send («sans mention religieuse»,
  «no health data») would close an ordinary piece. Fix: match on code + title only, or document the choice.
- M-3 The control is name-based: staff can still declare a piece that solicits art. 9 data under a neutral title.
  Fix (follow-up): `documents.services.declare_requirement` refuses, or warns, when the switch is off and the
  declared piece is special-category; and record the residual in SPECIAL_CATEGORY_AUDIT §3.1 / DPIA RK-2.
- M-4 `test_production_privacy_page_v517.py` runs under test.py with the production switches (DEBUG False,
  ILE_LEGAL_OPEN_FIELDS_ALLOWED False), not under prod.py; the docstring and the builder summary say «production
  settings». Fix: reword to «the production switches» (or note it).
- M-5 The requirement Dépôt keeps its own note («Ne déposez que la pièce demandée ici.»), not G-UPLOAD; the summary's
  «uploads that stay open show G-UPLOAD» is true for the loose upload only. Already consistent with the audit table
  («the depot note stays») — just state it in NOTES §3.
- M-6 (cosmetic) A forged POST on a closed piece flashes the closed sentence twice (error from the service, info
  from the detail page after the redirect). Unreachable from the UI in production.
- M-7 In production a closed special-category piece still counts as «missing» on the case checklist with no act;
  the page explains it, but the checklist row may read as blocking. Product decision for the documents owner.
