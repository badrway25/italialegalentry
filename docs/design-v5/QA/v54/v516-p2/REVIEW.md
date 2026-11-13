# v516-p2 — privacy / legal-engineering review (label v516-p2-review)

- Branch `v516-p2`, head `c5f7dea` (one commit on `design-v5` 4d9ada5), worktree `C:/tmp/ile_wt/v516-p2`.
- Read: directive V5.16 (in full), the whole diff (34 files), the six new `docs/compliance/*.md`, the checklist /
  runbook / release-notes slices, the four-language notice markers, the code slices and the three new test files.
- Re-run on lane l9: `apps/legal`, `tests/compliance/test_forms_legal_basis_v516.py`,
  `tests/deployment/test_privacy_states_v516.py`, `apps/consents`, `apps/enquiries`,
  `apps/community/tests/test_join.py`, `tests/i18n/test_catalogues.py` → **184 passed**.

## Verdict: APPROVE_WITH_FIXES

The checks the task asked for hold:
- **Nothing invented** in the matrix, art. 9 audit, DPO, DPIA or roles matrix. Every basis is either cited from ANX
  §3 or marked LEGAL REVIEW REQUIRED. Retention is classed CONFIGURED (with file:line) / APPROVED POLICY / PROPOSED /
  UNRESOLVED. The Garante list item numbers (provv. 467/2018 items 1, 6, 8, 9, 10) and the WP248 criteria are
  correct, and both documents say the legal review must check them. There is one exception, finding 1.
- **6(1)(b) is never applied mechanically.** Security logs, abuse prevention, the audit trail, legal compliance,
  internal helpdesk notes, Academy plans and selection each get their own assessment.
- **Art. 9.** No universal explicit-consent box. The flows where art. 9 data is realistic are marked SPECIAL
  CATEGORY LEGAL BASIS REQUIRED. The public forms and the Virtual Forum are closed in code (G2, the flag and G1).
  The reserved-area flows are not closed in code; the builder states this openly and records it in R-SC-1 and the
  closed-only checklist item A-31 (see finding 3).
- **Acknowledgement is never a consent.** `AcknowledgementBooleanField` uses Django's required message. No bundled
  consent, no pre-ticked box, and the optional visibility choices and the selection disclosure are separate.
  Tests pin all of this.
- **Locked copy is untouched.** `p1.companies.form.consent` and `p2.forum.registration.consent` are verbatim and
  marked LOCKED COPY — LEGAL REVIEW REQUIRED, with proposals P-1/P-2 and both forms closed by G2. The newsletter is
  correctly classed B (a real optional purpose).
- **Marker classes are correct in all four languages.** OF-02…05 are PRODUCTION CONFIGURATION REQUIRED, OF-01 is
  OWNER CONFIRMATION REQUIRED (AGAMI APS as the candidate), and OF-06/07/08/10/12/13 are LEGAL REVIEW REQUIRED.
  DigitalOcean is named once as the intended provider, with no region, DPA state or transfer stated.
- **The production guard still refuses** a marker of every class (tested per class) and an unclassified one.
- **The status model is consistent** across the runbook *States*, checklist A-29…A-33 (closed, never accepted as
  open) and the release notes. It does not conflict with W4-D's rows.
- **No secret, real personal data or server identity** in the diff. The AGAMI identifiers are the organisation's,
  already in the repo from ANX.
- **Lane boundaries are respected.** The only template touched is the preview notice in `templates/legal/document.html`
  (lane P's file). Footer, base, header, gates.py, static and `locale/` are untouched.

## Findings

1. **[major] An unsourced legal fact.** `docs/compliance/DPO_ASSESSMENT.md:10` says «Italy Legal Entry is a project
   and a platform, not a legal entity», and `docs/compliance/PRIVACY_PROCESSING_AUDIT.md:129` (the OF-01 row) says
   «never Italy Legal Entry itself, which is not a legal entity».
   - No approved material states this. V5.16 §2 makes it conditional: «Do not substitute Italy Legal Entry itself
     unless it is a separate legal entity».
   - Fix: «Italy Legal Entry is not to be substituted as controller unless the owner confirms it is a separate legal
     entity (OF-01)». Make the same change to «never» in checklist A-33 and in the v516 test docstring.
2. **[minor] Version switch only through seeds.** In `apps/consents/services.py`, the switch from the old reused text
   to the acknowledgement happens only in `ensure_consent_text`.
   - `record_consent` calls `consent_text_for`, which returns any current row directly. On a database that still
     holds the v1 «je consens» row, a submission made before `seed_all` runs records the old consent sentence while
     the form shows the acknowledgement.
   - This affects dev and preview databases, and the window between `migrate` and `seed_all`. G2 limits the
     production impact.
   - Fix: apply the retired-key check in `consent_text_for` for `ACKNOWLEDGEMENT_PURPOSES`, or route those purposes
     through `ensure_consent_text`. Add a test that goes through `record_consent` with a v1 reused row present. Name
     the seed's re-versioning in the release handoff, since `seed_all` otherwise «never rewrites».
3. **[minor] The art. 9 audit's status column overstates what is enforced.** In
   `docs/compliance/SPECIAL_CATEGORY_AUDIT.md` §1, the status column for S-01…S-03 says «production flow stays
   closed», but the closed-by column says «nothing».
   - Reword to «MUST stay closed — not enforced in code until R-SC-1; manual gate A-31».
   - The steward/director should track R-SC-1 as a PRODUCTION_READY blocker, not a nice-to-have.
4. **[minor] Back-office wording.** The consents admin still offers «Registra la revoca del consenso» on every
   `ConsentRecord`, now including the acknowledgements (institution, university, contact, sign-up, Virtual Forum).
   - Staff could «withdraw» an acknowledgement as if it were a consent, which implies that a 6(1)(b) processing
     stops.
   - Fix (or a request to the consents/back-office owner): limit the action to the category-B purposes, or label
     acknowledgement records as such.
5. **[minor] Count error.** `docs/compliance/DPIA_NECESSITY.md` §4 says «At least three WP248 criteria» and then
   lists four (1, 4, 6, 7). Change it to «four».

None of these needs a browser run. Findings 1, 3 and 5 are document edits; finding 2 is a code change plus a test.
