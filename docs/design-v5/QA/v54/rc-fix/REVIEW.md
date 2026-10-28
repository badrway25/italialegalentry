# REVIEW — rc-fix-review: v54-rc-fix against design-v5 4ffc22b

28 Oct 2026. Targeted review of `git diff 4ffc22b..v54-rc-fix` (4 commits: 257e42c, 0013dfb, b220af4, 1533daf; 6 files, +103/−11).
Nothing was written to the repository by the reviewer.

**Verdict: APPROVE_WITH_NITS. No major finding.** The branch can go to the steward's merge step.

## (a) Missing stored file → 404 (b220af4, SMOKE D1)

- Order in `_serve` (`apps/documents/views.py`): `require(user, "download", doc)` → `services.delivery_block` → only
  then `services.open_for_download(doc)` inside `try/except FileNotFoundError`. Both callers (`download`,
  `signed_download`) reach the file only through `_serve`; `open_for_download` has no other caller. A refused account
  therefore never reaches the open: it gets the same 403 whether the file exists or not. No existence leak.
- Anonymous: `login_required` still redirects before `_serve` (test 5).
- Log: `log.warning("documents.file_missing document=%s", doc.pk)` on `ile.documents` — id only, no name, path or
  address; `raise Http404 from None` drops the traceback chain (no path in a chained exception). `Http404` carries no
  message, so the 404 page shows nothing of the document.
- Tests prove ALLOW (owner 404, signed route 404, exactly one record, the record text equals the id-only message and
  contains none of name/path/email, no `documents.downloaded` audit event) and DENY (unrelated account: identical 403
  body before/after loss after normalising the CSRF token and the CSP nonce, no record; infected file: still 403, no
  record; anonymous: still sign-in redirect).
- Only `FileNotFoundError` is caught; other `OSError`s still 500. SMOKE suggested `FileNotFoundError`/`OSError`; the
  narrower catch is deliberate and argued in NOTES §3 (a permission error is a misconfiguration). Accepted.

## (b) Pillow 13.0.0 (0013dfb, gate 12)

- `requirements/base.txt` `Pillow==13.0.0` and `requirements/constraints.txt` `pillow==13.0.0`; `git grep` finds no
  other live pin. No other dependency line changed.
- `.venv`: `PIL.__version__` = 13.0.0.
- Re-run: `pip-audit -r requirements/constraints.txt --no-deps --disable-pip` → **No known vulnerabilities found**.
- Re-run on lane **l7** (`test_ile_v5_l7`, `--create-db`, one pytest): `apps/documents`,
  `tests/security/test_object_permissions.py`, `tests/frontend/test_icons.py`, `tests/frontend/test_favicon.py`,
  `tests/deployment/test_requirements_constraints.py`, `tests/security/test_privilege_escalation.py` → **220 passed**
  (includes the upload/Pillow `verify()` validation tests and the five new download tests).

## (c) test_icons (257e42c, gate 6)

`THINNER_RULES_WITH_AN_OWNER: set[tuple[str, str]] = set()`; the comment no longer names `.entrance__icon` as present
and records where it went. The test stays strict for any new thin rule. Passes in the l7 run.

## (d) PERMISSION_MODEL (1533daf, SECURITY D-4)

- §1.3 row: IMPLEMENTATO, citing §7.1 L-01 and `test_privilege_escalation.py::test_an_administrator_cannot_grant_superuser_to_themselves`
  — the test exists (line 91) and §7.1 row L-01 says closed. Accurate.
- §5.10 «Stato» changed VIOLATO → PARZIALE (scope beyond D-4 but required: the old paragraph contradicted the corrected
  row). Checked against `apps/accounts/admin.py`: `is_superuser` hidden/readonly for non-superusers, `PROTECTED_GROUPS`
  = role:superadmin/role:administrator excluded from choices and restored after m2m save, superuser accounts not
  changeable by non-privileged users, `is_staff` still editable. The Q-1 reference (`docs/design-v5/QA/v54/sec-f8/NOTES.md`
  §6, line 302) exists and says exactly this. Accurate. No residual «VIOLAT» in the file.

## Hygiene

`git diff --check` clean; 0 CR bytes in the diff; no secret, address or personal value in the diff.

## Findings

| Sev | Where | Detail |
|---|---|---|
| nit | `static/brand/v5/PROVENANCE.json:6`, design-v3/v4 specs | Still say «Pillow 12.3(.0)». These are historical build/measurement records (what built those files), so leaving them is correct; mention in the changelog that the derivatives were built with 12.3.0 and not rebuilt. |
| nit | NOTES §2 | The fixer installed into the shared `.venv`, which LANES.json calls read-only; harmless here (task-mandated), but the stale `~il` folder in site-packages should be removed once servers restart, and the steward should record the venv change in the merge entry. |
| nit | process | CI (ubuntu, 3.12/3.13) has not run on Pillow 13; run the full non-browser gate 6 again after merge, as the RC protocol requires. |
