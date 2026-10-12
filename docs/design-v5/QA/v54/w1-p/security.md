# W1-P · Preview as the live product — independent review, security lens (`w1p-security`)

Italy Legal Entry™ design V5 · V5.4 «EXECUTION MODE» · 5 October 2026 · independent reviewer, lens **security** (the
council's security reviewer for W1-P, plan §3.3 item 3 and §4.4: «passed by the council's security reviewer before it
ships», RTE-M5), label `w1p-security`. I built nothing in this family.

| | |
|---|---|
| **Reviewed** | branch `v54-w1-p`, `v54/base..b3e991c` (5 commits: `1338303`, `aab76d2`, `7bb39e5`, `bb1ba5b`, `b3e991c`), against plan §4 (4.1–4.6), §3.3 item 3, §2.2, §2.7 and DL54-01. Ownership: `scripts/check_ownership.py w1-p v54/base` → 24 inside, 2 slice → PASS. |
| **Server** | My own, `127.0.0.1:8789`, from `C:/tmp/ile_wt/v54-w1-p` at `b3e991c`: `DATABASE_URL=…/ile_v5_l4` (read-only use), `ILE_DESIGN_PREVIEW=1`, `ILE_DESIGN_PREVIEW_PORT=8789`, `ILE_REFERENCE_DATE=2026-10-03`, `DB_CONN_MAX_AGE=0`, `PGAPPNAME=ile-review-w1p-security`, `--noreload`. Not 8785/8786: both were already held by the sibling reviewers of this worktree (accessibility on 8785, UX on 8786); 8789 is the spare lane's port (LANES.json: no worktree, no server). Stopped at the end. |
| **Tests** | `TEST_DATABASE_URL=…/ile_v5_l9` (pytest's `test_ile_v5_l9`), lock-gated. |
| **Browser** | Headless Chromium (Playwright 1.63), own profile `C:/tmp/ile_v5_council/.profiles/w1p-security/`, lock-gated (the gate waited twice for the benchmark lock). Every «attacker» origin (`http://evil.test`, `http://127.0.0.1:8799`, `rebind.test`) was fulfilled inside the browser by Playwright routing or a host-resolver rule: nothing was served on another port. |
| **Untouched** | 8780, 8770–8772, 8782, the engineer's 8784 and the siblings' 8785/8786 were never loaded; Chrome 9222/9223 never used; `ile_qa`, `ile` and `ile_v5` never connected to (the database refusals were proved on an unreachable server, §1). |
| **Credentials** | None used, typed or stored. Authenticated pages only through the persona switch. What my sign-ins wrote on `ile_v5_l4`: 17 persona sign-ins (session rows, `last_login`, the `auth.login`/`auth.logout` audit rows). Every write attempt as a persona was refused before any view (the log shows each refusal); the first write probe targeted a message that does not exist, so even a broken rule could not have changed a persona. |
| **Evidence** | `C:/tmp/ile_v5_council/evidence/v54/w1-p/security/` (index in §7). |

## 0. Verdict

**PASS WITH FIXES: 0 blocking, 1 major, 5 minor.** The security design holds under attack:

- The preview, the persona switch, the frame exception and the read-only rule do not exist under the prod, staging or
  test settings, nor under dev with DEBUG off, even when the environment asks for them. A test proves it (5/5).
- Every listed proxy header (480 requests) and every forged `Host` (195) is refused. DNS rebinding answers 400.
- `ile_qa`, `ile` and every database outside the list are refused before any query (8/8).
- A persona session cannot write: POST, PUT, PATCH, DELETE, unknown methods, a lowercase `post`, a method-override
  header and path tricks are all refused. Only sign-out and the language switch pass, and CSRF still guards them.
- The log line names the persona key and never an e-mail.
- No other origin can frame anything: 6 in-browser framing attacks failed, cross-site, same-site on another port,
  `localhost`↔`127.0.0.1`, and nested through the landing, the index or a proof file.
- Cross-site and same-site login CSRF fail, cookie tossing included: Django's Origin check stops it.
- Both servers listen on 127.0.0.1 only.
- Every old proof-serving guard holds.

**What needs fixing:**

- **M1.** §4.6's «0 CSP violations» fails in redirect and form flows inside the frame. This is the same root cause as
  the UX review's B1. The browser fails closed, so nothing is weakened. I set the security constraints for the fix
  here.
- **Five minors:**
  - the gate's refusal is not the silent 404 the code and the tests claim;
  - log-line forging through the refusal line;
  - dot segments in `?page=`;
  - privileged roles that are not `is_staff` are not refused;
  - the residual exposure to raw port-forwards, which needs documenting.

The re-review needs only the tests named in each fix.

---

## 1. The lens, item by item

| Item | Result | Evidence |
|---|---|---|
| Mounted only with DEBUG and the preview flag; prod and staging refuse it, **proved with a test** | **PASS.** The test sets `ILE_DESIGN_PREVIEW=1`, `DJANGO_DEBUG=1` and `ILE_DESIGN_PREVIEW_PORT=8000`, and runs each configuration in its own interpreter: `config.settings.prod`; staging (= `config.settings.prod` + `docker-compose.staging.yml`'s environment); `config.settings.test`; dev with `DJANGO_DEBUG=0`. Each one has `DEBUG=False`, no flag, no app, no `designpreview.*` middleware, the base cookie names (`sessionid`, `csrftoken`, `ile_language`), no `__design-v5/` mount, `/__design-v5/accedi/qa-person/` unresolvable, and `access.enabled()` false. Positive control: dev + DEBUG + flag mounts all of it, with the chain ceiling → base → frames → read-only. **5 passed.** | `t1_settings_refuse_preview.log`, `scripts/test_w1p_settings_refuse_preview.py` |
| Proxy headers refused | **PASS.** Tested on 15 routes (every page, the archive, the old addresses, `decisioni/`, `stati/429/`, `accedi/`, `esci/`) × the plan's 5 headers + the engineer's 11, each set and each present but empty: **480/480 → 404**, never sealed. Headers outside the list pass: by design a deny-list, see m5. | `p1_gate.json` |
| `Host` pinned to the process port; forged `Host` and `X-Forwarded-*` | **PASS.** Forged hosts `127.0.0.1:8780`, `localhost:8780`, `127.0.0.1:8784`, `127.0.0.1`, `localhost`, `0.0.0.0:8789` (in dev's `ALLOWED_HOSTS`), `testserver`, `LOCALHOST:8789` and `127.0.0.1:08789` → 404. `127.0.0.1:8789.`, `[::1]:8789`, `evil.example:8789` and `127.0.0.1:8789@evil.example` → 400. No `Host` → 400. Total 195 + 15. In the browser, DNS rebinding (`rebind.test:8789` mapped to 127.0.0.1) → **400** on `/__design-v5/` and on `/fr/`. A valid token from a forged `Host`/`X-Forwarded-For` caller → 404 at the gate. | `p1_gate.json`, `p3_…json`, `b-browser/browser_series.json` (5, 5b) |
| `ile_qa` refused | **PASS, before any query.** Real dev settings, preview on, `DATABASE_URL` naming the database on an **unreachable** server (127.0.0.1:1), a POST to `accedi/qa-person/`. `ile_qa`, `ile`, `test_ile`, `ile_v5_perf`, `ILE_V5`, `ile_v5_l10` and `ile_v5x` → 403 «il database «…»», no session cookie, log `refused (database)` with no `@`. Control: `ile_v5` proceeds to the account lookup and fails to connect (500), so the refusal really comes first. The engineer's test monkeypatches `database_name()`; this one does not. **8 passed.** | `t3_database_refusal.log`, `scripts/test_w1p_database_refusal.py` |
| Only the qa-* personas of the preview's database | **PASS.** The allow-list holds the four QA e-mails (dev.py). `accedi/qa-staff/`, `admin/`, `QA-PERSON/`, `qa-person-x/` and `superuser/` → 404, even with a valid token. On `ile_v5_l4` the four accounts are active, not staff, not superuser, with no direct permissions; their groups are `role:person` (×2), `role:company`, and none for qa-fresh-person. The staff and inactive refusals are proved by the engineer's tests, which I re-ran green (the allow-list is not configurable on a live server without editing dev.py). Hardening: m4. | `p3_…json`; suite run below |
| Persona sessions read-only: POST, PUT and DELETE refused | **PASS.** As qa-person, every one of these → **403 refusal**, `text/plain`, `nosniff`, `no-store`, `noindex`: POST to mark-read (non-existent message), Ma situation, login, signup, data export, deletion request, `/documents/` and `/api/`; PUT, PATCH and DELETE on the dashboard; the method `FOO`; a lowercase `post`; a POST carrying `X-HTTP-Method-Override: GET`. `OPTIONS` passes the rule and the view answers 405; no view in `apps/` writes on OPTIONS or on a GET-only branch. Path tricks (`/__design-v5/../fr/…`, `/%5F%5Fdesign-v5/../…`, `//__design-v5/../…`) → 404. The allow-list works and CSRF still guards it: `set_language` → 302 + `ile_v5_language`; `account_logout` → 302, session ended. Without a token, or with a foreign Origin, both → 403 and the persona stays signed in. In the browser, a Ma situation submit inside the frame shows the refusal in the frame. | `p3_…json`, `b10_persona_refusal_in_frame.png` |
| Persona key in the log, never the e-mail | **PASS** (but see m2). The log lines read `persona qa-person signed in (read-only session).`, `… refused (read-only).`, `… refused (database).` and `… signed out.` My server's logs contain no persona e-mail. The only e-mail-shaped strings are my own forged `Host: 127.0.0.1:8789@evil.example` probes, in Django's DisallowedHost lines. | server log (§7) |
| Own language cookie (and session, CSRF) | **PASS.** 8789 sets only `ile_v5_csrftoken`, `ile_v5_sessionid` and `ile_v5_language`; never `sessionid`, `csrftoken` or `ile_language`. | `p3_…json` (`_jar_names`), `browser_series.json` 10a |
| Frame exception only through `_csp_replace` after CSP and XFrameOptions, GET/HEAD only | **PASS.** The effective chain, printed from the running settings, ends `XFrameOptionsMiddleware, CSPMiddleware, BackofficeCSPMiddleware, ExtraSecurityHeadersMiddleware, PreviewFrameMiddleware, PersonaReadOnlyMiddleware`. 32 header cases: relaxed (`frame-ancestors 'self'` + `SAMEORIGIN`, every other directive byte-identical) **only** for GET/HEAD + `Sec-Fetch-Dest: iframe` + `Sec-Fetch-Site: same-origin` + allowed caller. Strict in every other case: same-site, cross-site, `none`, `frame`/`embed`/`object`/`document`, `IFRAME` in capitals, `Sec-Fetch-Dest` alone, POST, PUT, OPTIONS, XFF, `Via`, `Host 0.0.0.0:8789`, `Host 127.0.0.1:8780`, `/backoffice/`, the preview's own pages. A browser-initiated frame navigation (`Sec-Fetch-Site: none`) is refused (`ERR_BLOCKED_BY_RESPONSE`). `Vary: Sec-Fetch-Dest, Sec-Fetch-Site` is on every judged response. One deliberate exception, the read-only refusal to a POST: §4 D1, no objection. | `p4_frame_exception.json`, `browser_series.json` 10a2 |
| No open framing of arbitrary paths | **PASS for security.** No other origin can frame anything: 6 attacks failed, ending at `chrome-error://`. They were: `evil.test` framing `/fr/`; `127.0.0.1:8799` framing `/fr/`; a `localhost:8789` page framing `127.0.0.1:8789/fr/`; and `evil.test` framing the landing, a proof file and the index. `?page=` takes no scheme, no `//` and no other origin (`https://…`, `//evil`, `javascript:` → 400 / `/fr/`), and every reflection is escaped. **Contract gap:** dot segments pass, so the live strip frames research proof pages (m3). | `browser_series.json` 1–4, 9; `b1`/`b2`/`b4`/`b9` PNGs |
| CSRF intact | **PASS** (but see m1). The switch POSTs fail in all of these cases: no token; token without cookie; foreign Origin (`evil.example`, `127.0.0.1:8770`, `localhost:8789`, `null`, `127.0.0.1:8789.evil.example`) → 403. In the browser, `evil.test` auto-submitting «Entrer» → 403 «Origin checking failed», no session. **Cookie tossing** also fails: `127.0.0.1:8799` plants `ile_v5_csrftoken` and submits the matching token → 403 «Origin checking failed - http://127.0.0.1:8799…», no session. The token rotates at sign-in. `CSRF_COOKIE_HTTPONLY` is on. | `p3_…json`, `browser_series.json` 6–7 |
| Nothing reachable from another machine | **PASS.** 8784 (the engineer's) and 8789 listen on `127.0.0.1` only. TCP connects to `10.123.89.19`, `172.21.144.1` and `172.26.240.1` on 8784 and 8789 fail. The gate refuses any non-loopback `REMOTE_ADDR` anyway. Residual: m5. | `n1_bind_and_reachability.txt` |
| Every old proof-serving guard | **PASS.** 49 strings on `research/proof/` and on the old `/proof/`, 18 on `decisioni/`: dotted segments, `..` plain, `%2e%2e`, `%2E%2E%2F`, `..%2f`, double-encoded, overlong UTF-8, `%u002e`, fullwidth dots, backslashes and `%5c`, drive letters `C:` / `C%3a`, `::$DATA`, trailing dot/space, `NUL.html`/`CON`, the 8.3 aliases `ECD~1`, `WORK~1`, `SIGNIN~1.MD`, `INDEX~1.HTM`, `W1-P~1`, `IMPLEM~1.MD`, `.py`/`.pyc`/`.git/config`, directories. Every one refused (404). The old `/proof/` 302s only for strings the first layer accepts, and the target answers them 404 (the redirect is never broader). `decisioni/` serves `.md` only, as `text/plain` + `nosniff`. Three 500s, all NUL-byte paths: pre-existing, not W1-P's (O1). | `p2_proof_guards.json` |
| The W1-P suites (§2.7) | **395 passed, 0 skipped, 0 failed** in 403 s: `tests/frontend/test_design_preview.py` (browser included) + `tests/security`, on `test_ile_v5_l9`. | `t2_w1p_suites_on_l9.log` |

## 2. Plan §4.6: the items this lens reads

| §4.6 item | Result | Note |
|---|---|---|
| absent without the flag (404) | PASS | t1 above; the engineer's tests too. |
| 404 off loopback, with a proxy header, or with a foreign `Host` | **PASS for GET; not for unsafe methods** | A POST/PUT/DELETE from a refused caller meets **CSRF's 403** before the gate (m1). It never opens a session. |
| 405 on GET for `accedi` / `esci` | PASS | GET, HEAD and OPTIONS → 405 `Allow: POST`. PUT/DELETE → CSRF's 403, not the 405 the tests assert (m1). |
| staff, unknown accounts, a database outside the list refused, `ile_qa` included | PASS | t3; the engineer's staff/inactive tests (green). Hardening: m4. |
| distinct session, CSRF and language cookie names | PASS | |
| persona sessions read-only: 403 outside the preview, the allow-list excepted | PASS | |
| the log line carries no e-mail | PASS | Forgeable: m2. |
| frames load real pages only under the narrow condition | PASS | 32 header cases + 6 browser attacks. |
| 0 CSP violations | **PASS at rest; FAIL in flows** | 0 on the landing, the framed home and the index. Violations when a frame's navigation redirects or answers a form (M1). |

---

## 3. Findings

### Blocking

None from the security lens.

### Major

**M1 — In-frame redirects and form answers violate the CSP: §4.6 «0 CSP violations» fails. Same root cause as UX B1;
here, the security constraints on its fix.**

- *Failure scenario (measured independently of UX).* On 8789, `/__design-v5/?page=/fr/../backoffice/`: the frame's
  redirect hop is upgraded to https and refused. The console of the landing reads «Framing 'https://127.0.0.1:8789/'
  violates … "frame-src 'self'"», and the frame ends at `chrome-error://` (`browser_series.json` 9b + console;
  `b9b_page_param_backoffice.png`). UX measured the same mechanism on ordinary flows:
  - a signed-out persona link (302 to the login);
  - the in-frame sign-out (`form-action 'self'`);
  - an in-frame POST answer (`frame-ancestors 'none'`).

  Each one leaves a blank frame (ux.md B1).
- *Cause.* Two mechanisms:
  - The global CSP's `upgrade-insecure-requests` (`config/settings/base.py:360`) makes Chromium upgrade the frame's
    redirect hops on this plain-http loopback server.
  - Plan §4.4 never relaxes a POST answer, so no form answer can be framed.
- *Security reading.* The browser fails **closed**: nothing is exposed or weakened. It is major in this lens only
  because it is a §4.6 gate item, and because its fix edits the frame exception, which this review owns.
- *Fix: UX B1's option 1 is acceptable from the security lens, under these constraints.* I am answering ux.md's
  explicit question here.
  1. Remove `upgrade-insecure-requests` **only**:
     - (i) on the preview's own landing and index, with `@csp_replace({"upgrade-insecure-requests": None})`;
     - (ii) inside `frames.relax()`, i.e. only on a response already relaxed under the narrow condition.

     Never in `base.py`: production needs the directive.
  2. Relaxing a **POST answer** is acceptable under exactly the same condition: `framed_by_this_origin(request)` (DEBUG +
     flag, loopback, no proxy header, own `Host`, `Sec-Fetch-Dest: iframe`, `Sec-Fetch-Site: same-origin`), the same
     excluded prefixes (`/backoffice/`, `/__design-v5/`), and the read-only rule unchanged and first. Why the risk is
     the GET case's:
     - `Sec-Fetch-Site` is set by the browser and cannot be forged by web content;
     - `frame-ancestors 'self'` still demands that every ancestor be this origin;
     - a refused caller stays strict;
     - persona writes are still refused before any view.

     This supersedes the plan's «GET or HEAD» (§4.4): record it as a DL54 entry. It also absorbs D1 below.
  3. Tests, under the dev chain:
     - a relaxed response's CSP differs from the strict one **only** in `frame-ancestors` and
       `upgrade-insecure-requests` (string compare of the remaining directives);
     - cross-site, same-site, `none`, proxy-header and foreign-`Host` POST answers stay strict;
     - in a browser, signed out, `?page=/fr/espace-reserve/` ends on the login rendered in the frame, and the in-product
       sign-out ends on the home rendered in the frame, both with 0 `securitypolicyviolation`.

### Minor

**m1 — The gate's refusal is not the silent 404 the code, the notes and the tests claim.**

- *Failure scenario.*
  1. A refused caller (an `X-Forwarded-For` header, or `Host: 127.0.0.1:8780` / `0.0.0.0:8789`) sending POST without
     a token to `/__design-v5/`, `index/`, `research/` or `accedi/qa-person/` gets **403, «CSRF verification
     failed»**, not 404. `CsrfViewMiddleware.process_view` runs before the view, so before `_guarded`'s gate. A POST
     to a path that does not exist answers 404, so the refused caller can tell a preview route from nothing
     (`p3_…json`; the confirmation run in §7).
  2. An allowed caller's PUT/PATCH/DELETE on `accedi/`, `esci/` and the landing gets 403, not 405.
  3. A refused GET gets Django's **DEBUG technical 404**, which says «Raised by: designpreview.views.persona_enter» and
     lists the `__design-v5/` patterns.
  4. `test_every_route_is_a_404_off_loopback_behind_a_proxy_or_for_another_host` and
     `test_an_allowed_caller_meets_405_for_a_method_a_route_does_not_take` assert 404/405 for these unsafe methods.
     They pass only because Django's default test `Client` does not enforce CSRF.

  The switch never opens a session in any of these cases. The defect is in the claim («a refused caller learns
  nothing, not even that a route exists, whatever its method»: `access.py`, `views.py`, `__init__.py`, notes §4) and in
  tests that do not reflect the real server.
- *Fix.*
  1. In `views._guarded`, answer the refusal with `HttpResponseNotFound("Not Found\n", content_type="text/plain;
     charset=utf-8")` instead of `raise Http404`. Then the DEBUG technical page never names a preview view.
  2. Mark the outer wrapper `csrf_exempt` (`wrapped.csrf_exempt = True` before `transaction.non_atomic_requests`), so
     the gate answers before CSRF.
     - `_persona_only` keeps `csrf_protect` inside, after the gate, and stays CSRF-enforced.
     - `_preview_only` views take GET/HEAD only, so an exempt POST meets `require_http_methods`' 405 and changes
       nothing.
  3. Run both tests with `Client(enforce_csrf_checks=True)`. Assert the refused bodies contain no `designpreview`.
  4. Word the claim as «a refused caller is never served the preview». Under DEBUG, Django's own 404 page for any
     other path still lists the mount.

**m2 — Log forging through the read-only refusal line.**

- *Failure scenario.* As qa-doc-person, `POST /fr/x%0aINFO%20ile.designpreview%20%5Bforged%5D%20Design%20preview:%20persona%20qa-admin%20signed%20in%20(read-only%20session).`
  is refused (403). The server log then holds two lines, the second forged:
  `INFO ile.designpreview [forged] Design preview: persona qa-admin signed in (read-only session). refused (read-only).`
  (server log line 5068). `PersonaReadOnlyMiddleware` logs `request.path` raw. Django 5.2.17 escapes control
  characters in its own request log (the CVE-2025-48432 fix), so this line reintroduces the class. Impact: dev-only,
  and it needs a persona session on this machine. But it falsifies the very log §4.6 relies on («persona key in the
  log»).
- *Fix.*
  1. Log a neutralised path, e.g. `request.path[:200].encode("unicode_escape").decode("ascii")`, or the resolved view
     name and nothing else. Apply the same to the method.
  2. Add a test: with a persona session, POST a path containing `%0a` and `%0d`; the one `ile.designpreview` record's
     `getMessage()` contains no `\n` or `\r`.

**m3 — `?page=` accepts dot segments: the live strip can frame research proof pages, contrary to `page_param`'s
contract.**

- *Failure scenario.*
  - `/__design-v5/?page=/fr/../__design-v5/research/proof/index.html` → 200. The browser resolves the frame to the
    gate-0 proof index «La prova» and renders it **under the live strip, labelled «V4 + fondation»**
    (`b9_page_param_dot_segments.png`).
  - `?page=/fr/../backoffice/`, `/fr/%2e%2e/__design-v5/`, `/ar/../documents/` and `/fr/./` are accepted too.
  - `esci` passes `page=/ar/../__design-v5/` straight into its redirect.

  This contradicts `live.page_param`'s «never the preview itself» and §4.3 (the proof frames leave the main path). A
  crafted link can show the owner an unapproved prototype as the live product. It is not a security breach:
  same-origin only, the back-office and the preview's own pages stay `DENY`.
- *Fix.*
  1. In `page_param`, after `urlsplit`, refuse a path whose percent-decoded form has a `.` or `..` segment, an empty
     segment (`//`), or a character `_UNSAFE` refuses (catches `%2f`, `%5c` and `%00` once decoded).
  2. Test: `/fr/../__design-v5/`, `/fr/%2e%2e/backoffice/`, `/fr/./` and `/ar/..%2f..%2fx` → 400 on the landing and
     `/fr/` after `esci`.

**m4 — Privileged roles that are not `is_staff` are not refused.**

- *Failure scenario.* `personas.enter` refuses only `is_staff` and `is_superuser`. In this codebase, roles are groups
  and independent of `is_staff` (`apps/accounts/roles.py`): `role:operator` («handles case files and the help desk»),
  `role:authorised_actor` (acts on cases for someone else), `role:moderator`, `role:legal_editor`,
  `role:legal_approver` and `role:content_editor`. If an allow-listed QA account ever gained one of them on a preview
  database, «Entrer» would open that privileged session without a password. Today the four accounts hold only
  `role:person`/`role:company`, so this is hardening: §4.1's «a staff persona is never offered» should mean «no
  privileged session, ever».
- *Fix.*
  1. Refuse unless the account's groups ⊆ `{"role:person", "role:company"}` and it has no direct permission (one
     query), with reason `privileged` in the log line.
  2. Test: an allow-listed non-staff account in `role:operator` → 403, no session.
  3. Record it as a DL54 note: it is stricter than §4.4's letter.

**m5 — Residual: a raw port-forward or a header-less reverse proxy with a forged `Host` passes the gate.**

- *Failure scenario (by construction, not exercised: it needs a system-level forward).* The gate trusts loopback
  `REMOTE_ADDR` + no proxy header + `Host`. The client chooses its `Host`, so a non-browser client behind any raw TCP
  forward passes, i.e. a forward that adds no header (`ssh -L`/`-R`, `netsh interface portproxy`, `socat`). For
  example: `curl -H "Host: 127.0.0.1:8780" http://<lan-ip>:<forwarded-port>/`, then fetch the landing for a token,
  then POST `accedi/`, and read the QA personas' pages (read-only). The same holds behind nginx with a bare
  `proxy_pass`: by default nginx sends `Host: $proxy_host` (= `127.0.0.1:<port>`) and adds no `X-Forwarded-*`. The
  deny-list cannot catch either; 150 requests with ten headers outside it passed (`p1_gate.json`, `extra_headers`).
  Impact: low (synthetic QA data, read-only), and it needs someone on this machine to create the forward.
- *Fix.*
  1. State it in the implementation notes' honest limits: the gate cannot detect raw TCP forwards or header-less
     proxies; never forward a preview port; never put a proxy in front of a dev server.
  2. Optional hardening, if the owner ever needs a forward: a per-process launch secret, required once as a cookie
     before `accedi/` answers (the Jupyter model). An example would be a random token written at start-up to a file
     under `C:/tmp/ile_v5_council/.work/` and opened once as `/__design-v5/?chiave=…`.

---

## 4. Deviations from the plan: the security opinion

- **D1: the read-only refusal is frameable although it answers a POST** (notes §6 item 2; `personas.refusal` calls
  `frames.relax`). **No objection.** The response is the preview's own static sentence: `text/plain`, `nosniff`,
  `no-store`, `noindex`, nothing to click. It is relaxed only under `framed_by_this_origin` (verified: cross-site and
  XFF stay `DENY`/`'none'`). M1 item 2 generalises it; one DL54 entry can carry both.
- **D2: the `Host` is pinned on every preview route, eleven proxy headers beyond the plan's five, and `ile` refused
  beside `ile_qa`** (notes §6 items 3–4). **Endorsed**: each is strictly tighter than the plan.
- **D3: `decisioni/` serves the CD decisions** (notes §6 item 6). **No objection.** It uses the proof resolver,
  `.md` only, and serves `text/plain` + `nosniff` under `docs/design-v5/QA/v54/` (18 hostile strings refused).

## 5. Observations (no finding)

- **O1 — NUL bytes answer 500, site-wide, pre-existing.** `%00` anywhere in a path (inside `/__design-v5/` too) makes
  `cms.middleware.LegacyURLMiddleware.lookup_redirect` query PostgreSQL with a NUL byte → `DataError` → 500. Under
  DEBUG, that is the technical 500 page. The preview's own guard raised its 404 first. This is the known «%00 → 500»
  ticket on `cms`; not W1-P's slice.
- **O2 — Proof files share the origin with persona sessions.** The archive serves agent-authored HTML/JS from
  `C:/tmp/ile_v5_council/proof/` on the same origin as the app. A proof script could fetch a CSRF token same-origin
  and sign the browser in or out as a persona: CSRF cannot stop same-origin script. The risk was the same before W1-P
  for any session opened on 8780, and the personas are read-only with synthetic data. Optional: a `sandbox
  allow-scripts` CSP on proof responses, or the archive on its own port.
- **O3 — GET-time writes.** None changes a persona: mark-read, data export and deletion are POST-only (the rule
  refuses them). A sign-in writes the session, `last_login` and an audit row, as the notes say.
- **O4 — XSS.** Every `?page=` reflection is escaped (`src`, `href`, `title`, hidden inputs; JSON through
  `json_script`). The script writes `textContent`/`href` only, from a same-origin, prefix-checked location. There is
  no `innerHTML`.
- **O5 — Fail-closed configuration.** A lane that forgets `ILE_DESIGN_PREVIEW_PORT` gets a 404 on every preview route
  (the gate expects 8780). `0.0.0.0` stays in dev's `ALLOWED_HOSTS`, but the gate refuses it.
- **O6 — Slice note (not security).** `tests/security/test_log_privacy.py` gains a whole test function, while the
  manifest's slice says «the persona line (:57)». The steward checks it at the merge.

## 6. Method and limits

- **Raw HTTP probes.** Written with `http.client`, so that `Host`, headers, methods and un-normalised paths are exactly
  what was sent. Results are JSON files (p1–p4).
- **Browser.** Headless Chromium only: no Firefox, no WebKit, no real device.
- **Port-forwards and proxies.** Not exercised: they need system-level changes. m5 is reasoned from the code and from
  nginx's documented defaults.
- **Staff and inactive refusals.** Proved by the engineer's tests (re-run green), not on the live server. Exercising
  them live would need an edit to dev.py's allow-list or the lane's data, which a read-only reviewer does not make.
- **The «0 CSP violations» flows.** UX measured them on 8786. My own reproduction is the `?page=/fr/../backoffice/`
  redirect (9b).

## 7. Evidence index (E/ = `C:/tmp/ile_v5_council/evidence/v54/w1-p/security/`)

| File | What |
|---|---|
| `E/p1_gate.json` | the gate: 15 routes × 32 header variants, 13 forged hosts, no Host, 10 headers outside the list |
| `E/p2_proof_guards.json` | 49 strings × `research/proof/` and old `/proof/`, 18 × `decisioni/` |
| `E/p3_persona_switch_and_read_only.json` | 56 rows: CSRF, Origin, methods, allow-list, sign-in, read-only refusals, framed refusal, `set_language`, `esci` targets, sign-out |
| `E/p4_frame_exception.json` | 32 header cases, with the full CSP of each, and the landing, index and `/fr/` policies |
| `E/b-browser/browser_series.json` + 7 PNGs | cross-site, same-site and nested framing; DNS rebinding; login CSRF; cookie tossing; the landing (1 frame, 0 violations); dot segments; the persona flow and the in-frame refusal |
| `E/t1_settings_refuse_preview.log` | prod / staging / test / dev-without-DEBUG refuse; dev + flag mounts (5 passed) |
| `E/t2_w1p_suites_on_l9.log` | `test_design_preview` + `tests/security`: 395 passed, 0 skipped |
| `E/t3_database_refusal.log` | `ile_qa`, `ile` and five more refused before any query; control proceeds (8 passed) |
| `E/n1_bind_and_reachability.txt` | listeners on 127.0.0.1 only; LAN and virtual-adapter connects fail |
| `E/scripts/` | every probe, the browser series and the two scratch tests (none in the repository) |
| `C:/tmp/ile_v5_council/.work/servers/srv8789-w1p-security.{err,out}.log` | my server's log: the persona lines, the forged line of m2 (l. 5068), the NUL tracebacks of O1 |
