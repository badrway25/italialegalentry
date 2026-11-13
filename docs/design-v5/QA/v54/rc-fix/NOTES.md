# rc-fix: the release candidate v2.0.0's two gate failures and two P2s

28 Oct 2026. Branch `v54-rc-fix` from design-v5 `4ffc22b`, worktree `C:/tmp/ile_wt/v54-rc-fix` (its `.env` is
design-v5's with DATABASE_URL and TEST_DATABASE_URL set to lane l6; git-ignored). Four commits, one per item. Nothing
merged, no push, no remote, no tag, nothing on main, nothing deployed.

| # | Item | Commit | Proof |
|---|---|---|---|
| 1 | Gate 6: the stale allow-list in `tests/frontend/test_icons.py` | `257e42c` | `THINNER_RULES_WITH_AN_OWNER` is an empty `set[tuple[str, str]]`; the comment says none is left (the last went with components.css §12 in `71fbd90`). `tests/frontend/test_icons.py`: **20 passed** |
| 2 | Gate 12: Pillow 12.3.0 → 13.0.0 | `0013dfb` | see §2 |
| 3 | SMOKE D1: a missing stored file is a 404, not a 500 | `b220af4` | see §3 |
| 4 | SECURITY D-4: PERMISSION_MODEL §1.3 row | `1533daf` | see §4 |

## 2. Pillow 13.0.0

- **The release exists on PyPI** (`--index-url https://pypi.org/simple` only): `pip download pillow==13.0.0 --no-deps
  --only-binary=:all:` got all four wheels: `cp312` and `cp313`, `manylinux_2_27_x86_64.manylinux_2_28_x86_64` and
  `win_amd64` (scratch folder, outside the repository).
- **Release notes, the breaking changes** (pillow.readthedocs.io, 13.0.0): Python 3.10 dropped; I-mode PNG no longer
  clipped to 16 bits; `Image.fromarray(mode=…)` changing the dtype removed; `get_child_images` moved to `ImageFile`;
  `Image._show`, `ImageCms.ImageCmsProfile.product_name/product_info`, `ExifTags.IFD.Makernote` removed; changes in
  behaviour for `ImageColor.getcolor` on RGBa/La, duplicate TIFF tags, and ICO saving without `sizes`. **The code base
  uses none of these.** A grep over every `PIL` import found `apps/documents/services.py` (open + verify of sniffed
  JPEG/PNG), `apps/documents/tests/conftest.py`, `apps/cms/tests/test_media_assets.py`, six test files under
  `tests/frontend/` and three scripts. `scripts/make_favicon_ico.py` passes `sizes=` explicitly, so the ICO change does
  not affect it. `qrcode` is not called with a PIL image factory in `apps/`.
- **The pins:** `requirements/base.txt:9` and `requirements/constraints.txt:20` changed together. Nothing else pins
  Pillow: `dev.txt` does not mention it. The «Pillow 12.3» mentions in `docs/design-v3`/`design-v4` are dated
  measurement records, so they were left alone.
- **Install:** `pip install pillow==13.0.0` in `C:/tmp/italylegalentry/.venv`, the only package change. `pip check`: no
  broken requirements. pip warned that it could not remove the temporary folder `.venv/Lib/site-packages/~il`, because a
  running process (a server on this venv) still holds the old binary. It is harmless. Delete it once those servers have
  restarted. Note: LANES.json calls this venv read-only ("never pip install into it"). The task asked for this install
  explicitly, which is why it was done.
- **pip-audit** `-r requirements/constraints.txt --no-deps --disable-pip`: **No known vulnerabilities found**. The run
  in SECURITY.md found 38.
- **Tests on lane l6** (`test_ile_v5_l6`, `--create-db`):
  - `apps/documents apps/cms apps/core apps/accounts`, plus `tests/frontend/test_depot_w3_c.py`, `test_favicon.py`,
    `test_icons.py`, `tests/deployment/test_requirements_constraints.py`, not browser: **453 passed**
    (`pytest_pillow13_nonbrowser.txt`).
  - The four browser files that import PIL (`test_console_shell_browser_w3_a`, `test_depot_browser_w3_c`,
    `test_documents_browser_w3_c`, `test_loader_w1_d`): **104 passed** (`pytest_pillow13_browser.txt`).
- **CI** (ubuntu-24.04, 3.12 and 3.13) still has to run. The wheels it needs exist.

## 3. A missing stored file

`apps/documents/views.py` `_serve`: the two gates (`require(user, "download", doc)`, `services.delivery_block`) run
first, as before. Only then is the file opened. On `FileNotFoundError` the view logs one warning on `ile.documents`,
`documents.file_missing document=<id>` (no name, no path, no address), and raises `Http404`. No authorisation decision
changed. A `PermissionError` or any other `OSError` still raises a 500, on purpose: that is a server misconfiguration,
not a lost file.

Tests in `apps/documents/tests/test_download.py`:
- the owner gets a 404, exactly one record whose message contains only the id, and no `documents.downloaded` event;
- the signed route also gives a 404;
- an unrelated account gets the same 403 page before and after the file is lost (the per-request CSRF token and CSP
  nonce are normalised before the comparison) and its request writes no record;
- the owner of an infected file still gets a 403, not a 404;
- an anonymous request is still redirected to the sign-in.

Red on the old view: the two 404 tests fail with `FileNotFoundError`. Green on the new one:
`apps/documents` + `tests/security/test_object_permissions.py` **179 passed** (`pytest_missing_file.txt`). Django's
own `Not Found: /documents/<uuid>/` line also logs the path, which carries only the id.

Not in scope, and left as SMOKE reported them: D2 (`private_storage()` creates the root on a read), D3 (the back office
at 390 px), and the 8780 environment (no `private_media` in v5-live).

## 4. PERMISSION_MODEL

- §1.3 row «L'amministratore non può concedersi il superadmin» changed from VIOLATA to **IMPLEMENTATO**. It cites the
  closure in §7.1 L-01 and
  `tests/security/test_privilege_escalation.py::test_an_administrator_cannot_grant_superuser_to_themselves`.
- §5.10's «Stato: VIOLATO oggi … può concedersi il superadmin» paragraph contradicted the corrected row and §7.1. It now
  says **PARZIALE**: the superadmin grant is closed, but the administrator can still set `is_staff` and ordinary groups.
  That gap is left to owner question Q-1 (`QA/v54/sec-f8/NOTES.md` §6), as SECURITY.md D-3 says. This is one step
  beyond the task's wording, taken so the document does not contradict itself. It can be reverted on its own if not
  wanted.
- No test reads the content of PERMISSION_MODEL. The related suites, the doc and compliance guards and the ownership
  test (`test_privilege_escalation`, `test_identity_gaps`, `tests/backoffice/test_screens_follow_the_policies.py`,
  `test_confidential_material`, `tests/compliance`, `tests/deployment`, `test_design_docs`, `test_check_ownership`):
  **378 passed** (`pytest_docs.txt`).

## 5. The end checks

- `ruff check` on the three touched Python files: clean.
- `ruff format`: `views.py` and `test_download.py` are formatted. `test_icons.py` was **not** reformatted: the five
  hunks `ruff format` would change were there before, outside the changed lines, and REGRESSION_NON_BROWSER P2-3 puts
  repository-wide formatting after the release. The changed lines themselves are format-clean.
- `manage.py check`: no issues. `makemigrations --check --dry-run`: no changes.
- `git diff --check`: clean. No CR in the added lines. The diff contains no address, secret or URL.

## 6. For the steward (the merge, DL54-162)

This branch writes no steward file: no OWNERSHIP, decision log, live_status or CHANGELOG. Owners of the touched paths
(`check_ownership.py --owners`), and the slice each needs:

| Path | Current owner | Proposed rc-fix slice |
|---|---|---|
| `tests/frontend/test_icons.py` | w1-b (whole file) | `THINNER_RULES_WITH_AN_OWNER` emptied and its comment (gate 6) |
| `requirements/base.txt` | no owner | the Pillow pin 13.0.0 (gate 12) |
| `requirements/constraints.txt` | devops (whole file) | the pillow pin 13.0.0 (gate 12) |
| `apps/documents/views.py` | w3-c (slice: the Dépôt's JSON answers) | `_serve`: a missing stored file → `documents.file_missing` + 404, after the gates (SMOKE D1) |
| `apps/documents/tests/test_download.py` | no owner | the five missing-file tests and their helpers (SMOKE D1) |
| `docs/security/PERMISSION_MODEL.md` | sec-f5, sec-f8 (slices) | §1.3's superadmin row and §5.10's «Stato» (SECURITY D-4) |

After the merge, re-run the full non-browser suite (gate 6) and pip-audit (gate 12) on the merged design-v5.
