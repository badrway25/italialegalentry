# DevOps second pass — independent review (`devops2-review`)

Reviewer `devops2-review`, 16 October 2026. I built nothing on this branch.

Reviewed: `design-v5...v54-devops-2`, the eight commits `d62d256` … `6010a5c` on base `8ab5b89`, 14 files, +1 088 / −8.
Read in full: directive V5.9; the runbook, the checklist and `ROLLBACK.md`; the family's `NOTES.md` (both passes); every
changed file. Read in the pinned sources: Django 5.2.17 (`contrib/staticfiles/storage.py` — `HashedFilesMixin`'s passes
and the four module patterns; `http/request.py` — `_load_post_and_files`, `body`; `core/handlers/exception.py`),
WhiteNoise 6.12.0 (`middleware.py` `immutable_file_test`, `storage.py` compression and deletion), pytest-django 4.14.0
(`LiveServer`), Gunicorn 26.2.0 (`http/message.py`, header values).

Every probe ran in `C:/tmp/ile_v5_council/.work/devops-2/review/`, never in the repository: copies of the tree at
`8ab5b89` and at `6010a5c`, scratch settings, a scratch harness. The lane server listened on 127.0.0.1:8789 against
`ile_v5_l9` only and is stopped. Tests ran on `test_ile_v5_l9`, one pytest at a time, `-p no:randomly`, never the full
suite. Nothing was deployed and no server was contacted.

## Verdict: SHIP_AFTER_FIXES

Three of the four fixes hold under every attack I could build. The fourth, the NUL guard, fixes what it set out to fix
and opens a new 500 along the way.

1. **Stale modules after a release: fixed, at the root.** I simulated a release as the runbook does it: collect, change a
   module, collect again into the same `STATIC_ROOT`, never `--clear`. I ran it under the merge base's storage, then
   under the branch's.
   - Before: a browser coming back 30 s, an hour or 30 days after the release runs the old `loader.js` with the new
     pages, and a page opened before the release imports the new one.
   - After: no old module runs, no file outside the new graph is loaded, and the old graph stays intact, byte for
     byte.
   - Chromium imports every rewritten module. nginx 1.24 passes WhiteNoise's headers through unchanged. No page loads
     more files, or loads them later, than before.
2. **NUL bytes: every NUL that reaches Django now gets the project's 400 page and one WARNING.** On the merge base, 7
   of my 34 vectors were 500s with a traceback. **But the guard reads the body of every POST**, `csrf_exempt` views
   included. The public webhook `/api/v1/webhooks/<system>/` (no API key) can no longer read its own body. Any
   multipart POST to it is now a 500 with a traceback, and no NUL is needed (**M1**). The request gets through nginx
   too: I checked with Ubuntu 24.04's nginx.
3. **`check --deploy`: byte-identical to the merge base.** W005 and W021 with the template's HSTS values; no issue with
   both on.
4. **Live-server port: never a port Chromium refuses, and two sessions never share one.** I forced six concurrent
   sessions onto three ports: three bound, three failed cleanly. One fixture belonging to another family still binds
   port 0 and opens it in Chromium (m4).

**M1 is a few lines of code.** The form-field check moves into `process_view` and skips `csrf_exempt` views. I
prototyped it and ran it; nothing else holds the merge.

## What I ran

| | Result |
|---|---|
| `pytest tests/deployment apps/cms tests/frontend/test_static_pipeline.py tests/frontend/test_css_bundle_is_current.py tests/frontend/test_frontend_bundle_is_current.py tests/test_env_example_is_complete.py tests/test_live_server.py -p no:randomly` | **153 passed** — the NOTES' set (live server on a drawn port, 20453) |
| `pytest tests/security -p no:randomly` | **157 passed** |
| `pytest apps/integrations apps/core tests/backoffice/test_backoffice.py tests/compliance/test_public_pages.py apps/documents/tests/test_download.py` | **71 passed** |
| NUL probe, 34 vectors (`review/test_nul_review.py`), on the merge base / the branch / the proposed guard | **7 × 500** / **1 × 500 and 1 ERROR** (M1, m1) / **0** |
| Simulated release, two storages × two scenarios (`review/release/run_release.py`) | §1 |
| Chromium on the lane server (production settings, the branch's storage) | §1 |
| W4-B's `static/js` (the next merge) collected with the branch's storage | exit 0; 15 dist modules, 36 imports, all rewritten |
| An acyclic chain of 7 modules (`review/chain/chain.py`) | «Max post-process passes exceeded» in one directory order, success in the other (m3) |
| nginx 1.24 (WSL Ubuntu 24.04, as the user, under the scratch directory, in front of an echo upstream) | §1 and n1 |
| `check --deploy --fail-level WARNING`, merge base and branch, template HSTS and HSTS on | identical (§3) |
| Concurrent live-server sessions (`review/ports/`) | §4 |
| `ruff check`, `ruff format --check` on the changed Python files | clean |
| Added lines scanned for secrets and for the production server's address and name | 0 hits |
| `git diff --stat design-v5...HEAD -- static/ templates/ apps/cases apps/portal` | empty: no file of W3-E, W4-B or sec-f7 touched |
| `scripts/check_ownership.py devops design-v5` | 14 paths: 7 inside, 2 slice, 5 outside → FAIL until the steward assigns them (NOTES) |

## The brief's questions, answered

### 1. A release, then a browser that follows the cache headers

**Setup.** Release N is the branch's `static/`. Release N+1 is collected into the same `STATIC_ROOT` without `--clear`,
under `config.settings.prod`. The harness gives every file the release changes a new mtime, as a git checkout does:
collectstatic skips a source file that is not newer than its collected copy. Two scenarios:

- **A — an entry changed in place:** `js/dist/loader.js` changes, and its name and its importers' esbuild output stay
  the same. This is the original bug.
- **B — a real esbuild rebuild:** after a change to `static/js/src/overlay.js`, the chunk names change and 17 dist
  names change.

The graph is walked from every `{% static %}` entry of the templates through the collected tree. WhiteNoise is probed
in a fresh process after each collect, as a restart would have it. The browser model fetched the N graph at t = 0 with
N's headers. It then loads N+1's pages at t = 30 s, 1 h and 30 days, and uses its cached copy of a file whenever the
headers still allow it.

| | merge base's storage, A | merge base's storage, B | branch, A | branch, B |
|---|---|---|---|---|
| Plain names in N+1's graph (`max-age=31536000`) | 10 | 12 | **0** | **0** |
| Old modules run by a returning browser (30 s / 1 h / 30 d) | `loader.js` | `depot.js`, `loader.js`, `piece-drawer.js`, plus 3 old chunks outside N+1's graph | **0** | **0** |
| A page opened under N imports on demand after the release | gets N+1's `loader.js` | N+1's three entries | **its own release's files, byte for byte, `.gz` included** | **same** |
| Names the release changes | `loader.js` only | 17 | 6: `loader`, then its importers `chunk-T6TU3QHP`, `depot`, `piece-drawer`, `shell`, `console` | 17 |
| N+1's graph: not 200 / not `immutable` | 0 / 10 | 0 / 12 | **0 / 0** | **0 / 0** |

**Are hashed files still immutable?** Yes, every name in the current manifest is `max-age=315360000, public, immutable`,
and a plain name is `max-age=60, public`. One nuance: WhiteNoise compares a name against the *current* manifest, so
after a release the previous release's hashed files get `max-age=60, public` (n2). They are still collected and still
serve the right bytes, so this is harmless.

**Does the runbook's nginx block agree with WhiteNoise?** Yes. It has no `location /static/` (a test holds that), and
it proxies everything to Gunicorn. Run in front of an upstream that answers as WhiteNoise does, nginx 1.24:

- keeps `Cache-Control: max-age=315360000, public, immutable` unchanged;
- keeps the upstream's `Content-Encoding: gzip` and `Vary` (its own `gzip on` does not compress twice);
- passes a multipart body through untouched (this is how M1 reaches Django in production).

**Is any page's first render slower?** No:

- **Same files:** Chromium on the lane server loads the same 9 scripts on `/fr/` under both storages, at the same
  waterfall depth.
- **Compression kept:** every rewritten file has its `.gz`; 38 of 38 scripts were served gzip-encoded.
- **No preload lost:** the templates preload only fonts and the hero image, through `{% static %}`, unchanged by the
  fix, and no module preload exists.
- **Text unchanged except the names:** a diff shows only the `} from "` spacing and the hashes differ.
- **Clean pages:** on `/fr/` (18 static requests), `/ar/` (19) and `/fr/compte/login/` (20), every static request is a
  hashed name answered 200 and `immutable`, with no console error.
- **Fewer revalidations:** under the merge base's storage the same pages loaded 5, 5 and 4 chunks by plain name with a
  year of cache and no `immutable`, which Firefox revalidates on reload.
- **Every module still runs:** `import()` of each of the 19 hashed dist modules from the page succeeds.

**What else the rewriting touches.** Collecting the same tree with both storages, 29 of 615 names differ: 18 in
`js/dist` and 11 in `js/src`. No non-JS file and no third-party file changes, as the NOTES say. **W4-B's `static/js`**
collects with exit 0, and all 36 of its imports become the hashed names; it has no cycle and no computed `import()`.

### 2. NUL bytes wherever a request carries text

Results through the test client, DEBUG off; the before column is the merge base `8ab5b89`. Every 400 below is the
project's own page (`Erreur 400 · Italy Legal Entry™`; `/ar/` answers `lang="ar" dir="rtl"`) with one WARNING line
whose path is escaped (`Bad Request: /fr/nothing\x00here/`).

| Vector | Before | Branch | Proposed (M1 + m2) |
|---|---|---|---|
| Path: `/fr/…%00…`, `/documents/%00/`, `/api/v1/webhooks/a%00b/`, `/fr/glossaire/a%00b/`, HEAD | 500 + ERROR | 400 | 400 |
| Path: `/backoffice/%00/` | 302 | 400 | 400 |
| Query: `?categorie=%00` | 500 + ERROR | 400 | 400 |
| Query: `?next=%00`, `/healthz/?x=%00`, `/api/v1/events/?after=%00` | 200 / 200 / 401 | 400 | 400 |
| Form, urlencoded and multipart (sign-in), NUL in a value | 200 (the form's message) | 400 | 400 |
| Form field sent to a `csrf_exempt` view (scratch echo view, `name*=UTF-8''o%00p`) | 200 | 400 | 200 (left to the view, as on `design-v5`) |
| Session cookie `"\000…"` | 500 + ERROR | 400 | 400 |
| CSRF cookie with NUL, on a POST | 403 | 403 | 403 |
| Language cookie (`ile_language`), unknown cookie | 200 | 200 | 200 |
| Multipart filename with a raw NUL, or `filename*=UTF-8''a%00b.pdf` | 200; Django strips it (`ab.pdf`) | same | same |
| A file whose bytes hold NUL | 200 | 200 | 200 |
| Header (test client only: Gunicorn's RFC 9110 check and nginx refuse a raw NUL in a header) | 200 | 200 | 200 |
| **Webhook, multipart body, no NUL at all** | 401 | **500 + ERROR** (M1) | 401 |
| **Webhook, urlencoded body of 250 fields, no NUL** | 401 | **400 + ERROR** (m1) | 401 |
| Webhook, JSON body with `\u0000` | 401 | 401 | 401 |

On the branch, the guard's 400 has no `Content-Security-Policy`, no `X-Frame-Options` and no `Permissions-Policy` (m2).
In the proposed column, every 400 carries all three.

### 3. `check --deploy`

`manage.py check --deploy --fail-level WARNING` under `config.settings.prod` with the runbook's placeholders and
`DATABASE_URL` on `ile_v5_l9`. I ran it on the merge base and on the branch, once with the template's HSTS values and
once with both directives on. The two outputs are byte-identical:

- W005 and W021, exit 1, with the template's values;
- «System check identified no issues», exit 0, with both on.

### 4. The live server's port

- **Unsafe ports and concurrency:** four sessions started at once on drawn ports got four distinct ports (28049, 32123,
  26576, 23381) and Chromium answered 200 on each. Six sessions forced onto three ports: three bound distinct ports and
  three raised a clean `OSError 10048`. A port is never shared and never refused by Chromium.
- **Windows exclusions:** a Hyper-V exclusion lies inside the range (29992–30091). A bind there raises `OSError 10013`,
  which the loop skips (n3).
- **Address given:** a `--liveserver` or `DJANGO_LIVE_TEST_SERVER_ADDRESS` that names a port is honoured exactly, as in
  pytest-django.
- **The fixture is still pytest-django's:** the override yields pytest-django's own `LiveServer`, so
  `_live_server_helper` keeps its database and `ALLOWED_HOSTS` handling.

### Nothing else regressed

- **Security headers:** CSP, `X-Frame-Options`, `Permissions-Policy`, `nosniff`, `Referrer-Policy`, COOP and CORP are
  unchanged on every normal response: `/fr/`, `/ar/`, the sign-in page and a 404, in Chromium and through the test
  client. The guard's own 400 is the only exception (m2).
- **Static pipeline and bundles:** the CSS import-convention test, the collectstatic run and the two bundle-currency
  tests pass (part of the 153).

## Major finding — fix before the merge

### M1 — The guard reads every POST body, and the public webhook can no longer read its own

**Failure.** On the server, this returns 500; on `design-v5` it returns 401. No NUL is needed:

```bash
curl -s -o /dev/null -w '%{http_code}\n' -F event=ping "https://<host>/api/v1/webhooks/anything/"
```

Each such request writes `ERROR django.request Internal Server Error: /api/v1/webhooks/anything/` to the journal, with a
traceback ending in `RawPostDataException: You cannot access body after reading from request's data stream` at
`apps/integrations/views.py:86` (`body = request.body`). The endpoint is `auth=False`, so anyone can trigger it, and
this is the same class of problem as N-4, which the pass was meant to remove. Legitimate senders post JSON, which is
never parsed as a form, so they are unaffected.

**Cause.** `NulByteMiddleware.carries_nul` (`apps/cms/middleware.py:138–147`) evaluates `request.POST` for every POST.
For `multipart/form-data`, Django parses the request stream itself (`_load_post_and_files`). After that, `request.body`
raises. Before this branch only `CsrfViewMiddleware` parsed a POST, and it never does so for a `csrf_exempt` view. The
integrations API is `csrf_exempt` (`apps/integrations/api.py:63`). It is the only production code that reads a raw body.

**Fix.** Prototyped in `review/review_mw.py`.

- Keep the checks of the path, the query string and the session cookie in `__call__`, before every reader, as now.
- Move the form-field check into `process_view`, and return `None` when `getattr(view_func, "csrf_exempt", False)`.

That is exactly the set of requests whose body `CsrfViewMiddleware.process_view` parses anyway, a few steps on. Nothing
new is read, and a view that reads its raw body keeps it. A `csrf_exempt` view that stores posted fields would have to
guard itself; there is none today.

With the prototype in place:

- my 34 vectors pass, and the webhook answers 401 again;
- the branch's `test_nul_bytes.py` passes 16 of 17 (the 17th looks the class up by its dotted path);
- a form's 400 now leaves through the whole chain, so it carries CSP and `X-Frame-Options` too.

**Tests to add** (in `tests/deployment/test_nul_bytes.py`): a multipart POST and a 250-field urlencoded POST to
`/api/v1/webhooks/<x>/` both answer 401, with no ERROR record.

## Minor findings

### m1 — TooManyFieldsSent on the webhook: an ERROR line with its traceback, for anyone

This has the same cause as M1. An urlencoded POST of more than `DATA_UPLOAD_MAX_NUMBER_FIELDS` (200) fields to the
webhook is parsed by the guard. Django raises `TooManyFieldsSent`, a SuspiciousOperation, which
`django.security.TooManyFieldsSent` logs at **ERROR** with its traceback, and answers 400. On the merge base the same
request was 401 with no ERROR, because nobody parsed it. M1's fix removes this as well, as measured.

### m2 — The guard's 400 carries no CSP, no X-Frame-Options and no Permissions-Policy

`XFrameOptionsMiddleware`, `CSPMiddleware`, `BackofficeCSPMiddleware` and `ExtraSecurityHeadersMiddleware` sit below the
guard (`config/settings/base.py:127–131`, guard at `:116`). A response the guard returns never passes through them. It
gets only `SecurityMiddleware`'s headers (`nosniff`, `Referrer-Policy`, COOP), measured in Chromium and through the test
client. On the merge base the query and cookie vectors were 500s that did carry CSP and `X-Frame-Options`.

**Impact:** practically nil, because the page is static and reflects nothing. It is inconsistent with every other page
the site draws.

**Fix (prototyped):** list the four middlewares right after `TextGZipMiddleware`, keeping their relative order
(`test_html_compression.py` requires CSP below the gzip layer). Every 400 of the 34 vectors then carries CSP,
`X-Frame-Options`, `Permissions-Policy` and CORP. 161 tests pass with that order and M1's guard, across
html_compression, layout, overlays, back office, public pages, downloads, `apps/core`, error pages, NUL bytes and
integrations; the one failure is the dotted-path lookup again. If the steward prefers not to reorder, A-21 should say
that this 400 has none of those headers.

### m3 — «Max post-process passes exceeded» does not only mean a cycle, and the pass count follows the directory order

`apps/core/storage.py:26–27` and the runbook (`:355`, `:1336`) explain that error by a cycle between two bundles. A cycle
does cause it, but so does an **acyclic** chain longer than Django's five extra passes, depending on the order Django
processes the files. That order is by depth, then by **directory listing order**: sorted on NTFS, hash order on ext4.

- **Demonstrated** (`review/chain/chain.py`): seven modules `a→b→…→g`, with no cycle, added to the real tree. In the
  order where each module is listed before the one it imports, collectstatic exits 1 with «Max post-process passes
  exceeded.». In the reverse order it exits 0.
- **Consequence:** a dist that collects on this workstation and in CI can still fail during the server's release
  window, or the reverse.
- **Today's margin** (`review/chain/worst_case.py`; the model predicts the chain's failure: Django allows p ≤ 4): the
  worst case over every order is **p = 3** for the branch and for W4-B's tree. So it is safe today, with one pass of
  margin.
- **Where the margin goes:** the worst case is `js/src/console.js → piece-drawer → depot → loader`. Those are sources
  that no page loads; the dist alone needs at most p = 2.

**Fix:** apply the module rewriting to `js/dist` only. Mind that the post-processed path is built with `os.path.join`,
so a `js/dist/*.js` pattern would not match on Windows. Alternatively, stop collecting `js/src`, or add the worst-case
computation to `test_static_caching.py`, which needs no collectstatic and takes milliseconds. Either way, correct the
three sentences.

### m4 — The design preview's `dev_server` still lets the operating system choose the port Chromium opens

`tests/frontend/test_design_preview.py:2486` binds `("127.0.0.1", 0)`. Its `dev_server` fixture (`:412`) is opened in
Chromium by six browser tests (`:5506`–`:5840`). That is the mechanism of the W3-A flake (`ERR_UNSAFE_PORT`) that item 4
fixed for `live_server`, and it remains here. The file belongs to another family. A helper exported from
`tests/live_server.py` (draw, bind, retry) would serve both; the steward should coordinate.

### m5 — No test collects twice into the same `STATIC_ROOT`

The runbook's release (step 15.8: collectstatic, never `--clear`) is the scenario item 1 is about.
`test_static_caching.py` proves only a collect into an empty root; my harness proved the second collect. Suggested
test:

- collect;
- change `loader.js` in a copy of the source, giving it a new mtime;
- collect again;
- check that its importers' names changed, that N's files survive byte for byte, and that N+1's graph holds no plain
  name.

### m6 — The rewriting reads every collected script, third-party ones included

Django's module patterns run on every collected `.js`. Suppose a script holds a literal specifier, or text in a comment
or a string that looks like one, and it resolves to no file. Then collectstatic stops, with ValueError surfacing as
`MissingFileError`, inside the release window. Today no third-party file is touched (29 names change, all ours), but a
dependency update could stop a deployment. m3's restriction to `js/dist` removes the exposure. Without it, a fast
static check modelled on `test_static_pipeline.py`'s CSS convention test, run over every collected script, would catch
it before the server does.

## Nits

- **n1 — Behind nginx, `%00` in the path never reaches Django.** I measured this with nginx 1.24, the Ubuntu 24.04
  package:
  - `%00` in the path gets nginx's own bare 400;
  - a raw NUL in the path or in a header also gets nginx's 400;
  - `?q=%00` and an octal-escaped cookie pass through untouched.

  So on the server the guard answers the query string, the cookie and the form. Checklist D-10's first `curl` proves
  nginx rather than the guard, and the runbook's known limit reads as if the project's page answered the path. D-10
  could add `curl -s "$H/fr/?q=%00" | grep -c 'class="container error-page"'`, expecting 1.
- **n2 — After a release, the previous release's hashed files are served `max-age=60, public`** (measured in A and B).
  Step 11's «a hashed name ten years» and the static table could say «a name of the current release».
- **n3 — NOTES §4 says «outside this machine's Hyper-V exclusions today».** `netsh int ipv4 show excludedportrange
  protocol=tcp` lists 29992–30091, which is inside 20000–32767. The code already skips that case; the sentence is wrong.
- **n4 — NOTES «For the steward» says 13 paths, 6 inside.** `check_ownership.py` now reports 14 paths, 7 inside; the
  five outside are the same.

## Verified correct — leave as is

- **`core.storage.CompressedManifestModulesStorage`:**
  - it is one attribute on WhiteNoise's storage, using Django 5.2.17's four module patterns;
  - every import of the dist is rewritten, on the branch and on W4-B's dist;
  - the rewritten modules are valid and resolve: Chromium imports 19 of 19;
  - the hashes chain transitively, so a change to `loader.js` renames each of its importers.
- **`WHITENOISE_MAX_AGE = 60`:** it applies only to names that are not in the manifest.
- **Never `--clear` (step 8, step 15, ROLLBACK §1):** an old graph and its `.gz` files survive a release. A failed
  post-process leaves the previous manifest in place, and every file it names still exists (measured:
  `review/chain/failed_release.py`), so the rollback re-collect works.
- **nginx step 11:** it has no `/static/` location and passes WhiteNoise's headers and compression through.
- **The NUL guard's placement and answer:**
  - it runs after RequestID and Locale, so the page carries the request id and the language;
  - it runs before every reader;
  - the 400 is returned rather than raised, so it is a WARNING with the path escaped, never an ERROR;
  - a file's bytes are never read;
  - `lookup_redirect`'s second layer sends 0 queries.
- **`check --deploy`:** unchanged.
- **The live-server fixture:**
  - it keeps pytest-django's object and settings handling, and honours an address that names a port;
  - it draws with `SystemRandom`, and the bind itself is the test of freedom;
  - it prints a summary line, and `.env.example` documents the variable (the env-example test passes).

## For the steward

- Assign the five paths outside the family, as the NOTES list them.
- Extend the family's slice of `base.py` to `STORAGES["staticfiles"]`, `WHITENOISE_MAX_AGE` and the guard's
  `MIDDLEWARE` entry, plus the four header middlewares if m2 is taken.
- M1 touches only `apps/cms/middleware.py` and `tests/deployment/test_nul_bytes.py`.
- m4 is in the design preview's file.

## Scratch files (outside the repository)

`C:/tmp/ile_v5_council/.work/devops-2/review/`:

| File | Purpose |
|---|---|
| `test_nul_review.py`, `review_urls.py`, `conftest.py`, `pytest.ini` | The NUL probe, with results in `nul_before.json`, `nul_after.json`, `nul_proposed*.json` |
| `review_mw.py`, `review_plugin.py`, `review_plugin_headers.py` | The proposed guard and chain |
| `release/run_release.py`, `settings_rel.py`, `probe.py` | The simulated releases (`release_report.json`, `run_release.log`) |
| `release/chromium_check.py`, `lane_settings.py` | The browser check |
| `release/third_party.py`, `w4b_check.py` | The third-party diff and W4-B's dist |
| `chain/chain.py`, `worst_case.py`, `failed_release.py` | The acyclic chain, the worst case over directory orders, a failed collect into a good root |
| `deploy/check_deploy.sh` | The four `check --deploy` outputs |
| `ports/one_server.py`, `run_sessions.py` | Concurrent live-server sessions |
| `nginx/nginx.conf`, `echo_upstream.py`, `run_check.sh` | The nginx check |
| `base/`, `rel/` | The tree at `8ab5b89`, and the branch's tree with the rebuilt dist |

Not run: Gunicorn (Unix only; its header check was read in `http/message.py`), a server, the full suite, the browser
suite as a whole (the brief), Firefox and WebKit.
