# W1-P · Preview as the live product — security re-check after fix round 1 (`w1p-security-r2`)

Italy Legal Entry™ design V5 · V5.4 «EXECUTION MODE» · 5 October 2026 · independent reviewer, lens **security**,
label `w1p-security-r2`. I built nothing in this family. This is the re-check of my round-1 review
(`security.md`, the baseline) after the engineer's fix round (`IMPLEMENTATION_NOTES.md` § «Review fixes — round 1»,
DL54-17, DL54-18). Plan §4.4: the persona switch and the frames are «passed by the council's security reviewer before
it ships» (RTE-M5).

| | |
|---|---|
| **Reviewed** | branch `v54-w1-p` at `8f12192`, `v54/base..HEAD` (12 commits). The fix round is `23ca9b6`, `1ea7d06`, `f7555d1`, `2a05390`, `60196ec` and `8f12192`, on top of round 1's `b3e991c` + `0dedb7e`. Read against plan §4 (4.1–4.6), §3.3 item 3, §2.2, §2.7, DL54-01, DL54-17 and DL54-18. Ownership: `scripts/check_ownership.py w1-p v54/base` → 30 inside, 3 slice → **PASS**. The worktree was clean at `8f12192`. |
| **Server** | My own, `127.0.0.1:8789`, from `C:/tmp/ile_wt/v54-w1-p` at `8f12192`: `DATABASE_URL=…/ile_v5_l4` (read-only use), `ILE_DESIGN_PREVIEW=1`, `ILE_DESIGN_PREVIEW_PORT=8789`, `ILE_REFERENCE_DATE=2026-10-03`, `DB_CONN_MAX_AGE=0`, `PGAPPNAME=ile-review-w1p-security-r2`, `--noreload`. Not 8785/8786: both were already held by sibling reviewers of this worktree (their server logs name the accessibility and UX reviews). 8789 is the spare lane's port (LANES.json: no worktree, no server), as in round 1. Stopped at the end. |
| **Tests** | `TEST_DATABASE_URL=…/ile_v5_l9` (pytest's `test_ile_v5_l9`), nobody else connected to it, lock-gated. A first attempt that started in a 30-second gap between two benchmark windows was stopped by me when the lock came back. The run reported in §2 waited for 90 seconds without the lock. |
| **Browser** | Headless Chromium (Playwright), own profile `C:/tmp/ile_v5_council/.profiles/w1p-security-r2/`, lock-gated. Every «attacker» origin (`http://evil.test`, `http://127.0.0.1:8799`, `rebind.test`) was fulfilled inside the browser by Playwright routing or a host-resolver rule. Nothing was served on another port. |
| **Untouched** | 8780, 8770–8772, 8782, 8785/8786 and 8791/8792 were never loaded. 8784 (the engineer's) got only TCP connect attempts on non-loopback addresses, never an HTTP request. Chrome 9222/9223 never used. `ile_qa`, `ile` and `ile_v5` never connected to: the database refusals were proved on an unreachable server, as in round 1. |
| **Credentials** | None used, typed or stored. Authenticated pages only through the persona switch. Writes on `ile_v5_l4`: 26 persona sign-ins (session rows, `last_login`, the `auth.login` audit rows) and 12 sign-outs (10 through «Sortir», 2 through the product's own sign-out: the `auth.logout` audit rows). No sign-in form was submitted with its token, because a failed sign-in writes an `auth.login_failed` audit row. Every write attempt as a persona was refused before any view. |
| **Evidence** | `C:/tmp/ile_v5_council/evidence/v54/w1-p/security-r2/` (index in §8). |

## 0. Verdict

**PASS WITH FIXES: 0 blocking, 0 major, 2 minor (both new and small).** Every round-1 finding is closed. M1, m1, m2
(on the line it named), m3 and m4 are fixed and held by tests. m5 is documented, which round 1 allowed.

- **The preview exists only under dev + DEBUG + the flag.** Prod, staging, test and dev-without-DEBUG refuse it even
  when the environment asks for it (5/5, re-run on `8f12192`).
- **The gate answers first, whatever the method** (round-1 m1).
  - 4,704 refused requests got a plain `404 Not Found` (`text/plain`), unsealed, naming nothing of the preview:
    16 routes × 16 proxy headers set and empty, plus 10 forged `Host` values, × 7 methods (GET, HEAD, POST, PUT,
    PATCH, DELETE, OPTIONS).
  - No CSRF 403 and no technical page any more.
  - 240 requests to names outside `ALLOWED_HOSTS`, and every request without a `Host`, → 400.
- **CSRF is intact on the switch.** The switch is `csrf_exempt` at the middleware and `csrf_protect` inside, after the
  gate.
  - With no token, a wrong cookie, no cookie, or any foreign `Origin` → 403.
  - In the browser, cross-site auto-submit and same-site cookie tossing fail. An `evil.test` page auto-submitting «Entrer» or «Sortir» gets 403 «Origin checking failed», no session; so does `127.0.0.1:8799` planting `ile_v5_csrftoken` and submitting the matching token (`browser_series_r2.json` 6, 7, 7b).
- **Only the four `qa-*` personas, only on the lane's database.** `ile_qa`, `ile` and five more names are refused
  before any query (8/8). Privileged roles are refused (DL54-18; the four accounts on `ile_v5_l4` hold only
  `role:person` ×2 and `role:company`, plus one with no group).
- **Persona sessions are read-only.** 34 write attempts (POST, PUT, PATCH, DELETE, TRACE, `FOO`, a lowercase `post`,
  a method-override header, path tricks) were refused before any view. Sign-out and the language switch pass, and CSRF
  still guards both.
- **Persona key in the log, never an e-mail.** The m2 forging vectors (LF, CR, U+2028, NEL, ESC) reach the read-only
  line escaped.
- **The frame exception follows DL54-17.** A relaxed answer differs from the strict one in `frame-ancestors` and
  `upgrade-insecure-requests` only. Every same-site, cross-site, `none`, `document`, proxy, foreign-`Host`,
  PUT/PATCH/DELETE/OPTIONS case stays strict (47 header cases). In the browser, 8 framing attacks from other origins end at `chrome-error://`, including a cross-site form POSTed into its own frame. The landing, the in-frame redirect to the sign-in, the persona's pages, the in-frame refusal and the product's own sign-out show 0 `securitypolicyviolation`.
- **`?page=` no longer frames dot segments** (round-1 m3): 400, written or encoded. «Entrer» and «Sortir» fall back to
  safe pages.
- **127.0.0.1 only.** The engineer's 8784 and my 8789 listen on loopback only; connections from the LAN and virtual
  adapters fail.
- **Every old proof-serving guard holds.** 49 + 49 + 18 hostile strings.

**The two minors:**

- **m6.** The read-only refusal is relaxed for framing **whatever the method**: PUT, PATCH, DELETE, TRACE, `FOO`.
  DL54-17 says GET, HEAD or POST, and `frames.py` says «a PUT … the normal policy, unchanged». No browser can exploit
  it, because a frame is never navigated with those methods. It breaks the contract this lens set, and its fix is two
  lines.
- **m7.** m2 is incomplete: the ceiling's 503 line, in the same `ile.designpreview` logger, still writes
  `request.path` raw. Demonstrated: a loopback client with no persona forged a «persona qa-admin signed in» line.

**For the steward, outside W1-P's slice (O1, pre-existing, site-wide):** a NUL byte in any path turns the answer into
Django's DEBUG technical 500, the gate's plain 404 included. That page shows `DATABASE_URL` with the development
database password in clear. The fix belongs in `cms.middleware.LegacyURLMiddleware.lookup_redirect`.

**The re-check needs only the two tests named in §4.** No further review round is needed.

---

## 1. Round-1 findings: what was done and what I measured

| Round 1 | Fix (engineer) | Re-test on 8789 at `8f12192` | Status |
|---|---|---|---|
| **M1:** in-frame redirects and form answers violated the CSP (§4.6 «0 CSP violations») | (1) `upgrade-insecure-requests` dropped on the landing and the index (`@csp_replace(NO_UPGRADE)`) and inside `frames.relax()` only; `base.py` untouched. (2) A POST answer is relaxed under exactly `framed_by_this_origin`, same excluded prefixes, read-only rule still first. Recorded as **DL54-17**. (3) The three tests I asked for. | (1) The landing and the index differ from `/fr/`'s policy in `frame-src 'self'` (added) and `upgrade-insecure-requests` (removed), nothing else. Every relaxed answer differs from the strict one in exactly `frame-ancestors` and `upgrade-insecure-requests` (`p4`). (2) POST answers are relaxed only for iframe + same-origin + the gate's caller. Same-site, cross-site, `none`, `document`, `X-Forwarded-For`, `Forwarded`, `Host 127.0.0.1:8780`, `Host 0.0.0.0:8789` and `/backoffice/login/` stay strict (`p4`). (3) The tests exist and pass (§2). In the browser, signed out, `?page=/fr/espace-reserve/` ends on the sign-in rendered in the frame. The persona's first page, the in-frame refusal and the product's own sign-out render too. Every one of these steps shows 0 `securitypolicyviolation` (`browser_series_r2.json` 8, 9c, 10a–10c). The one violation of the series (9d) is the inline `<style>` of Django's default CSRF failure page, which the site's `style-src 'self'` refuses top-level too (O9). | **Fixed.** One gap left: the read-only refusal skips the method condition (m6). |
| **m1:** the gate's refusal was not the silent 404 claimed (CSRF 403 first; DEBUG technical 404 naming the view; 403 instead of 405) | `_not_found()` (plain `HttpResponseNotFound`) instead of `raise Http404`. Every route `csrf_exempt`, with `csrf_protect` inside the switch after the gate. The two tests use `Client(enforce_csrf_checks=True)` and assert that refused bodies name nothing. Docstrings reworded. | 4,704 refused requests across 7 methods → `404`, body exactly `Not Found\n`, `text/plain`, no seal, no «designpreview», «__design-v5», «CSRF» or «Raised by» (`p1`). An allowed caller's PUT, PATCH, DELETE and `FOO` on `accedi/` and `esci/` → **405**. GET, HEAD and OPTIONS → 405 `Allow: POST` (`p3`). A refused POST to a route and a POST to nothing are both 404. Only the body format differs, and Django's own DEBUG 404 lists the mount anyway, as the notes say. One edge remains, outside the slice: a NUL byte (O1). | **Fixed** |
| **m2:** log forging through the read-only refusal line | `_loggable()`: `unicode_escape`, 200 characters, applied to the persona, the method and the path. | LF, CR, U+2028, NEL and ESC paths as `qa-person`: one record each, escaped (`\n`, `\r`, `\u2028`, `\x85`, `\x1b`). The log slice holds no forged line and no `@` (`p3_server_log_slice.txt`). | **Fixed for that line.** The same class remains in the ceiling's 503 line (m7). |
| **m3:** dot segments in `?page=` | `_clean_path()`: no `.`, `..` or empty segment, as written and percent-decoded until stable (at most 4 rounds, then refused); `_UNSAFE` applied at each round. | `/fr/../__design-v5/research/proof/index.html`, `/fr/../backoffice/`, `/fr/%2e%2e/backoffice/` and `/fr/.%2E/__design-v5/` → **400**, no frame (in the browser too: `b9_page_param_dot_segments_400.png`). «Sortir» with 8 hostile values → `?page=/fr/`. «Entrer» with 7 hostile values → the persona's first page (`p3`). Every reflection escaped, including `?frame=` and `?lang=` (`p6`). | **Fixed** |
| **m4:** privileged roles that are not `is_staff` | The switch refuses any group but `role:person` / `role:company`, and any direct permission: `refused (privileged)`. Recorded as **DL54-18**. | Code read (`personas.enter`, `PERSONA_ROLES`); in this codebase privileges are groups (`accounts.roles`, `is_superadmin`). The engineer's test covers `role:operator` and a direct permission (green, §2). On `ile_v5_l4` today (read-only query): qa-doc-person and qa-person `role:person`, qa-company `role:company`, qa-fresh-person no group; none staff, none superuser, 0 direct permissions. | **Fixed** |
| **m5:** raw port-forwards and header-less proxies pass the gate | Stated in the notes' honest limits: «Never forward a preview port; never put a proxy in front of a dev server». The optional launch secret is not built. | Text read (notes, «Honest limits (added)»). A deny-list by design: 80 requests with five headers outside the list still pass (`p1`, `extra_headers_not_listed`). See also O1: behind such a forward, a NUL path would show the forward's users the DEBUG 500 page. | **Addressed as allowed** (documentation) |
| **D1:** the read-only refusal framed although it answers a POST | Absorbed into DL54-17. | POST → relaxed only under the narrow condition; same-site, cross-site and `none` stay strict (`p3`). But PUT, PATCH, DELETE, TRACE and `FOO` are relaxed too (`p7`). | See m6 |

## 2. The lens, item by item

| Item | Result | Evidence |
|---|---|---|
| Mounted only with DEBUG and the preview flag; prod and staging refuse it, **proved with a test** | **PASS.** My round-1 test re-run on `8f12192`, each configuration in its own interpreter with a hostile environment (`ILE_DESIGN_PREVIEW=1`, `DJANGO_DEBUG=1`, `ILE_DESIGN_PREVIEW_PORT=8000`). Prod; staging (= `config.settings.prod` + `docker-compose.staging.yml`'s environment); test; and dev with `DJANGO_DEBUG=0` all have `DEBUG=False`, no app, no `designpreview.*` middleware, the base cookie names and no mount, and `access.enabled()` is false. Positive control: dev + DEBUG + flag mounts the chain ceiling → base → frames → read-only. **5 passed.** | `t1_settings_refuse_preview_r2.log` |
| Proxy headers refused | **PASS, every method.** 16 routes × (the plan's 5 + the engineer's 11 headers, each set and each present but empty) × 7 methods → 404 plain (part of the 4,704). Deny-list by design (m5). | `p1_gate_r2.json` |
| `Host` pinned to the process port; forged `Host` and `X-Forwarded-*` | **PASS.** `127.0.0.1:8780`, `localhost:8780`, `127.0.0.1:8784`, `127.0.0.1:8785`, `127.0.0.1`, `localhost`, `0.0.0.0:8789`, `testserver`, `LOCALHOST:8789`, `127.0.0.1:08789` → 404, every method. `localhost.:8789` and `127.0.0.1.:8789` (trailing dot, which Django's host check accepts) → 404 at the gate. `127.0.0.1:8789.`, `[::1]:8789`, `evil.example:8789`, `127.0.0.1:8789@evil.example`, `rebind.test:8789` and `127.0.0.1:8789,evil.example` → 400. No `Host` → 400. A valid token from an `X-Forwarded-For` caller or from `Host 0.0.0.0:8789` → 404, before CSRF. In the browser, DNS rebinding (`rebind.test:8789` → 127.0.0.1) → 400 on `/__design-v5/` and on `/fr/`. | `p1`, `p3`, `p6` |
| `ile_qa` refused | **PASS, before any query.** Real dev settings, preview on, `DATABASE_URL` naming the database on an unreachable server (127.0.0.1:1). `ile_qa`, `ile`, `test_ile`, `ile_v5_perf`, `ILE_V5`, `ile_v5_l10` and `ile_v5x` → 403 «il database «…»», no session cookie, log `refused (database)` with no `@`. Control: `ile_v5` proceeds to the account lookup and fails to connect (500). **8 passed.** | `t3_database_refusal_r2.log` |
| Only the qa-* personas of the preview database | **PASS.** `qa-staff`, `admin`, `QA-PERSON`, `qa-person-x`, `superuser` and `qa-admin` → 404 with a valid token, no session. The allow-list is the four QA e-mails (dev.py). DL54-18 refuses any other role (§1). | `p3` |
| Persona sessions read-only: POST, PUT and DELETE refused | **PASS.** As `qa-person`, 34 write attempts → 403, the refusal in plain words (`text/plain`, `nosniff`, `no-store`, `noindex`), before any view: POST to mark-read (non-existent message), Ma situation, login, signup, data export, deletion request, password change, e-mail, `/documents/`, `/api/`, `/fr/consentements/`, `/backoffice/login/`, `/ar/espace-reserve/mes-documents/` and `/fr/contact/`; PUT, PATCH and DELETE on the dashboard; TRACE; `FOO`; a lowercase `post`; `X-HTTP-Method-Override: GET`; `/__DESIGN-V5/…`; `/__design-v5` (no slash). The forged-log paths are refused too. `OPTIONS` passes the rule and the view answers 405. Paths under `/__design-v5/` that resolve nowhere (`/__design-v5/../fr/…`, `/%5F%5Fdesign-v5/../…`, `/__design-v5/%2e%2e/…`, `/__design-v5/nowhere/`) → 404; preview pages → 405. No catch-all route exists that could take them elsewhere (`config/urls.py`). The two allowed writes keep their CSRF check. `set_language` without a token or with a foreign Origin → 403; with its token → 302, `next=https://evil.example/` falls back to `/`. `account_logout` without a token → 403, persona still in; with its token → 302, session ended. The census pages added in the fix round (academy, helpdesk, documents, companies, requests) write only behind POST (O3). | `p3`, server log |
| Persona key in the log, never the e-mail | **PASS.** Lines read `persona qa-person signed in (read-only session).`, `persona qa-person, POST /fr/… refused (read-only).`, `persona qa-company signed out.`. No persona e-mail anywhere in my server log: its only `@` are my own forged
`Host: 127.0.0.1:8789@evil.example` probes, in Django's DisallowedHost lines. m2's vectors reach the line escaped. **But:** the ceiling's 503 line can still be forged (m7). | `p3_server_log_slice.txt`, `p5_ceiling_log_slice.txt` |
| Own language cookie (and session, CSRF) | **PASS.** 8789 set only `ile_v5_csrftoken`, `ile_v5_sessionid` and `ile_v5_language`; never `sessionid`, `csrftoken` or `ile_language`. The landing's new `?lang=` sets `ile_v5_language` only for a page without a prefix and only to `fr`/`ar`/`it`/`en`. A hostile value is ignored and escaped. | `p3` (`_jar_names`), `p6` |
| Frame exception only through `_csp_replace` after CSP and XFrameOptions, GET/HEAD (+ POST, DL54-17) only | **PASS, except m6.** The chain ends `XFrameOptionsMiddleware, CSPMiddleware, BackofficeCSPMiddleware, ExtraSecurityHeadersMiddleware, PreviewFrameMiddleware, PersonaReadOnlyMiddleware` (t1's control; the engineer's chain test). Of the 47 header cases, 8 are relaxed, and only these: GET, HEAD and POST answers with iframe + same-origin from the gate's caller (`127.0.0.1:8789` or `localhost:8789`), the `/ar/espace-reserve/` → login redirect, `/documents/`, and the proof file by its own view. Strict in every other case: same-site, cross-site, `none`, `frame`, `embed`, `object`, `document`, `IFRAME` in capitals, `Sec-Fetch-Dest` alone, PUT, PATCH, DELETE, OPTIONS, `FOO`, XFF, `Via`, `Forwarded`, `Host 0.0.0.0:8789`, `Host 127.0.0.1:8780`, `/backoffice/` (also percent-encoded), and the preview's own pages (also percent-encoded). `/_errors/500/` framed by this origin gets `SAMEORIGIN` and no
policy at all, because django-csp sends none on a DEBUG 500; that is the library's DEBUG behaviour, not the
exception's. `Vary: Sec-Fetch-Dest, Sec-Fetch-Site` is on every judged response. **m6:** the read-only refusal is relaxed for PUT, PATCH, DELETE, TRACE and `FOO` too. | `p4_frame_exception_r2.json`, `p7_refusal_relaxed_by_method.txt` |
| No open framing of arbitrary paths | **PASS.** `?page=` takes a path under `/fr/`, `/ar/`, `/it/`, `/en/` or `/documents/` only. No scheme, no `//`, no backslash or control character, no dot or empty segment, written or encoded → 400 without a frame. Reflections are escaped (`p6`). Other origins cannot frame anything. Eight in-browser attacks end at `chrome-error://`: `evil.test` framing `/fr/`, the landing, a proof file, the index and the login; `127.0.0.1:8799` framing `/fr/`; a `localhost:8789` page framing `127.0.0.1:8789/fr/`; and `evil.test` POSTing a form into its own frame. A frame of the landing that navigates to `/backoffice/` is refused, and the stage says so instead of a blank frame (`b9e_backoffice_refused_stage.png`). A browser-initiated frame navigation (`Sec-Fetch-Site: none`) → `ERR_BLOCKED_BY_RESPONSE`. The index frames only server-built same-origin URLs (`data-dp-pair`). | `p6`, `b-browser/` |
| CSRF intact | **PASS.** The switch POSTs fail in all of these cases: no token; token without cookie; token with a wrong cookie; foreign Origin (`evil.example`, `127.0.0.1:8770`, `127.0.0.1:8784`, `localhost:8789`, `null`, `127.0.0.1:8789.evil.example`, `https://127.0.0.1:8789`) → 403. The token rotates at sign-in. `esci` without a token → 403. Why the `csrf_exempt` change is safe: Django's middleware skips an exempt view *without* marking the request as processed. The inner `csrf_protect` then runs the full check on the raw view, which carries no exempt flag. In the browser, cross-site auto-submit of «Entrer» and of «Sortir», and same-site cookie tossing from `127.0.0.1:8799`, → 403 «Origin checking failed», no session. | `p3`, `b-browser/` |
| Nothing reachable from another machine | **PASS.** 8784, 8789 and PostgreSQL 5439 listen on `127.0.0.1` only. TCP connects to `10.123.89.19`, `172.21.144.1` and `172.26.240.1` on 8784 and 8789 time out. The gate refuses any non-loopback `REMOTE_ADDR` anyway. | `n1_bind_and_reachability_r2.txt` |
| Every old proof-serving guard | **PASS.** The round-1 49 strings on `research/proof/` and on the old `/proof/`, and 18 on `decisioni/`. Each one is refused (404), or, for the old `/proof/`, 302-redirected only to a target that answers it 404, as in round 1. The cases: dotted segments, `..` plain and encoded, double-encoded, overlong UTF-8, `%u002e`, fullwidth dots, backslashes and `%5c`, drive letters, `::$DATA`, trailing dot/space, device names, the 8.3 aliases `ECD~1`, `WORK~1`, `SIGNIN~1.MD`, `INDEX~1.HTM`, `W1-P~1`, `IMPLEM~1.MD`, `.py`/`.pyc`/`.git/config`, and directories. The three 500s are the NUL-byte paths of the pre-existing `cms` issue (O1). | `p2_proof_guards_r2.json` |
| The W1-P suites (§2.7) | **428 passed, 0 skipped, 0 failed** in 554 s: `tests/frontend/test_design_preview.py` (browser tests included) + `tests/security`, on `test_ile_v5_l9`, at `8f12192`. The same item count as the engineer's run 1 of these two suites. The tests the notes name for each round-1 fix are among them. | `t2_w1p_suites_on_l9_r2.log` |

## 3. Plan §4.6: the items this lens reads

| §4.6 item | Result | Note |
|---|---|---|
| absent without the flag (404) | PASS | t1; the engineer's tests. |
| 404 off loopback, with a proxy header, or with a foreign `Host` | **PASS, every method** | Round-1 m1 closed: 4,704 requests. NUL-byte edge outside the slice (O1). |
| 405 on GET for `accedi` / `esci` | PASS | GET, HEAD and OPTIONS → 405 `Allow: POST`; PUT, PATCH, DELETE and `FOO` → 405 too. |
| staff, unknown accounts, a database outside the list refused, `ile_qa` included | PASS | t3; the engineer's tests; plus privileged roles (DL54-18). |
| distinct session, CSRF and language cookie names | PASS | |
| persona sessions read-only: 403 outside the preview, the allow-list excepted | PASS | 34 attempts; the allow-list keeps CSRF. |
| the log line carries no e-mail | PASS | The persona line can no longer be forged; the ceiling line still can (m7). |
| frames load real pages only under the narrow condition | **PASS with m6** | 47 header cases + 8 browser attacks; the refusal skips the method condition. |
| 0 CSP violations | **PASS** | 0 on the landing, the in-frame redirect to the sign-in, the persona's first page, the in-frame refusal and the product's own sign-out (browser series 8, 9c, 10a–10c). The engineer's browser tests that count `securitypolicyviolation` pass in my run. The one violation I saw (9d) is the inline `<style>` of Django's default CSRF failure page, product-wide and not the frame's (O9). |

---

## 4. Findings

### Blocking

None from the security lens.

### Major

None.

### Minor

**m6: The read-only refusal is relaxed for framing whatever the method. DL54-17 limits the exception to GET, HEAD
and POST.**

- *Failure scenario (measured, `p7_refusal_relaxed_by_method.txt`).*
  - As `qa-person`, with `Sec-Fetch-Dest: iframe` and `Sec-Fetch-Site: same-origin`, a PUT, PATCH, DELETE, TRACE or
    `FOO` to `/fr/espace-reserve/ma-situation/` is answered 403 with `X-Frame-Options: SAMEORIGIN` and
    `frame-ancestors 'self'`. The same PUT or DELETE without a persona stays `DENY` / `'none'`.
  - The cause: `personas.refusal()` (`apps/designpreview/personas.py:220–221`) calls `frames.relax()` whenever
    `frames.framed_by_this_origin(request)` holds. That predicate (`frames.py:62`) has no method in it; only the
    middleware adds `request.method in FRAMED_METHODS` (`frames.py:91`).
  - This contradicts DL54-17 («when it answers **GET, HEAD or POST**», `DECISION_LOG_V54.md:224`) and the module's
    own «a PUT … the normal policy, unchanged» (`frames.py:42`). The engineer's tests check a framed PUT for an
    anonymous caller only (`test_a_real_page_is_framed_by_this_origin_only_when_every_condition_holds`), never through
    the persona path.
- *Security reading.* No browser can exploit it. A frame is only ever navigated with GET or POST, so a PUT carrying
  `Sec-Fetch-Dest: iframe` comes from a non-browser client, for whom framing headers mean nothing. The response is the
  preview's static sentence. It is minor because it breaks the contract this lens set for the exception (round-1 M1:
  «exactly the same condition») and leaves two predicates that can drift apart.
- *Fix.*
  1. Put the method in the one predicate: in `frames.framed_by_this_origin`, start with
     `request.method in FRAMED_METHODS and access.allowed(request) and …`.
  2. Simplify `PreviewFrameMiddleware` to `if framed_by_this_origin(request): relax(response)`. `personas.refusal()`
     then inherits the condition unchanged.
  3. Test, under the dev chain: as a persona with `FRAMED` headers, PUT, PATCH and DELETE → 403 refusal with `DENY` and
    `frame-ancestors 'none'`, and POST → `SAMEORIGIN` and `'self'` (unchanged). Extend
    `test_a_frame_of_this_origin_may_show_the_refusal_and_nothing_else_may`.

**m7: m2 is incomplete. The ceiling's 503 line, in the same `ile.designpreview` logger, still writes the request's
path raw, and a loopback client with no persona can forge a line.**

- *Failure scenario (demonstrated on my own server, `p5_ceiling_log_probe.txt`, `p5_ceiling_log_slice.txt`).*
  1. Eight loopback connections each announce a multipart body of 6,000,000 bytes, above `DATA_UPLOAD_MAX_MEMORY_SIZE`
     (5 MB), carry a well-formed `ile_v5_csrftoken` cookie, and send only the first boundary line.
     `_read_a_small_body` skips them (too large), each takes a slot, and the CSRF check blocks reading the body inside
     the slot.
  2. A ninth request, `GET /fr/x%0aWARNING%20ile.designpreview%20[forged]%20Design%20preview:%20persona%20qa-admin%20signed%20in%20(read-only%20session).`,
     waits 20 s and gets the 503.
  3. `ConnectionCeilingMiddleware.busy()` logs `request.path` raw (`apps/designpreview/middleware.py:178`), so the
     server log reads, on two lines:

     ```
     WARNING ile.designpreview [-] Design preview: the 8 database slots stayed taken for 20 s — /fr/x
     WARNING ile.designpreview [forged] Design preview: persona qa-admin signed in (read-only session). answered 503.
     ```

     Django's own `django.request` line for the same request is escaped (`/fr/x\nWARNING …`). An attacker would put a
     plausible 32-hex request id in place of `[forged]`.
- *Security reading.* The line predates W1-P (`busy()` logged `request.path` at `v54/base`). But it sits in W1-P's
  slice (`apps/designpreview/**`) and in the logger §4.6 relies on («persona key in the log»). The m2 fix says
  «Whatever a request chose — its method, its path — reaches a log line escaped» (`personas.py:27–28`, notes), which is
  true of one module only. The precondition is performance P-1's residual, which the middleware's docstring states:
  bodies too large to read into memory still hold slots (O7). Impact: dev-only and loopback-only, but the result is
  a falsified preview log.
- *Fix.*
  1. Move the escaping helper where both modules can import it without a cycle, e.g.
     `designpreview.access.loggable(value)` (the same `str(value)[:200].encode("unicode_escape").decode("ascii")`). Use
     it in `personas.PersonaReadOnlyMiddleware` and in `ConnectionCeilingMiddleware.busy()`:
     `loggable(request.path)`.
  2. Test: `ConnectionCeilingMiddleware(lambda r: HttpResponse()).busy(RequestFactory().get("/fr/x%0aINFO%20forged%0d"))`
     → exactly one `ile.designpreview` record, whose `getMessage()` contains neither `\n` nor `\r`.

---

## 5. Deviations from the plan: the security opinion

- **DL54-17: a form's answer is framed under the narrow condition; a framed page and the landing/index drop
  `upgrade-insecure-requests`.** **Endorsed.** It implements exactly the constraints of my round-1 M1:
  - the global policy is untouched;
  - only the landing, the index and relaxed answers drop the directive;
  - the POST condition is the GET condition;
  - the excluded prefixes are unchanged;
  - the read-only rule comes first;
  - the three tests exist.

  The one gap is m6. The entry's wording is accurate once m6 is fixed.
- **DL54-18: no privileged persona.** **Endorsed.** It is stricter than §4.4's letter and matches how this codebase
  grants privileges (groups; `is_superadmin` = `is_superuser` or `role:superadmin`; object rights deny by default). The
  four accounts pass it today.
- **D2** (Host pinned on every route, sixteen proxy headers, `ile` refused) and **D3** (`decisioni/` serves the CD
  decisions): unchanged, still endorsed.

## 6. Observations (no finding against W1-P)

- **O1 (updated): a NUL byte still answers 500, and it now also defeats m1's plain 404.** This is pre-existing and
  site-wide; the fix belongs to the `cms` owner or the steward.
  - `%00` anywhere in a path makes `cms.middleware.LegacyURLMiddleware.lookup_redirect` query PostgreSQL with a NUL
    byte. The resulting `DataError` → 500.
  - For a refused caller on a preview route (e.g. `GET /__design-v5/research/proof/x%00` with `X-Forwarded-For`), the
    gate's plain 404 is turned into Django's DEBUG technical 500. That page says «Raised during:
    designpreview.views.proof».
  - On every DEBUG path it also lists `request.META`, which under `runserver` holds the whole process environment.
    That includes `DATABASE_URL` with the shared development database password, in clear: Django's
    `SafeExceptionReporterFilter` masks only names matching `API|TOKEN|KEY|SECRET|PASS|SIGNATURE|HTTP_COOKIE`
    (`ILE_QA_PASSWORD` is masked, `DATABASE_URL` is not) (`p8_nul_technical_500.txt`, password redacted there;
    control: the same refused request without the NUL is the plain 404).
  - Loopback-only today, and PostgreSQL listens on 127.0.0.1. Behind the raw forward m5 warns against, though, it would
    show the forward's users the database URL.
  - *Fix, outside W1-P's slice:*
    1. `lookup_redirect` returns no redirect for a path containing `\x00` (or catches `DataError`).
    2. Optionally, dev settings use an exception-reporter filter whose `hidden_settings` also matches
       `URL|DSN|DATABASE`.
- **O2 (unchanged): proof files share the origin with persona sessions.** Same-origin script can do what a persona
  can, read-only. Optional: `sandbox allow-scripts` on proof responses, or the archive on its own port.
- **O3 (re-verified): GET-time writes.** The census pages the fix round added write only behind POST, which the
  read-only rule refuses:
  - the Academy: `enrol` and module changes POST-only;
  - the helpdesk: ticket opening and messages behind `request.method == "POST"`;
  - documents: upload, decide and delete POST-only; the download only reads;
  - companies: needs and profile behind POST;
  - messages: mark-read POST-only.

  A sign-in writes the session, `last_login` and an audit row, as the notes say.
- **O4 (re-verified): XSS.** No raw reflection of `?page=`, `?frame=` or `?lang=` (`p6`). Templates are autoescaped,
  the map goes through `json_script`, and the script writes `textContent` / `href` only. One hardening note:
  - The landing's script copies any clicked link inside the frame into `pendingHref`, which can become the href of
    «Apri la pagina da sola» when the frame is refused, whatever the scheme.
  - No product template has a `javascript:` link, and the landing's `script-src 'self'` blocks `javascript:`
    execution, so it is not exploitable.
  - Optional: accept only `http:` and `https:` (`/^https?:$/.test(new URL(link.href).protocol)`).
- **O5 (unchanged): fail-closed configuration.** A lane that forgets `ILE_DESIGN_PREVIEW_PORT` gets 404 everywhere.
- **O6 (round 1, the slice of `test_log_privacy.py`): closed.** `check_ownership.py w1-p v54/base` passes (30 inside,
  3 slice); the steward reads the slice warnings at the merge, as for every family.
- **O7 (new; performance's lens): P-1's residual is reachable from loopback.** Eight withheld bodies larger than 5 MB
  still take all eight slots, and every page of the preview answers 503 after 20 s for as long as the client keeps the
  sockets open. Measured in m7's run; the landing answered 200 again at once after release. The middleware's
  docstring states this residual («A body too large to be read into memory, or one sent without a length, is read
  where it always was»). It is the precondition of m7 and nothing more for this lens.
- **O8 (the steward's F1, still open): an allowed caller's `Http404` reaches Django's DEBUG technical 404**, unsealed:
  an unknown persona key, a missing specimen board, a refused proof path. It names the view, for the owner only. No
  security impact. The steward's follow-up list already carries it.
- **O9 (new; pre-existing, product-wide): Django's default CSRF failure page breaks the site's own policy.** It
  carries an inline `<style>`, which `style-src 'self'` refuses top-level and in a frame alike. The page renders
  unstyled, and the browser fails closed. My series met it top-level (6, 7, 7b) and in the frame (9d, a form whose
  token I removed). It is the only `securitypolicyviolation` of the series. The repository sets no
  `CSRF_FAILURE_VIEW` and ships no `403_csrf.html`. Not W1-P's: a project template without inline style would make
  it CSP-clean.

## 7. Method and limits

- **Raw HTTP probes.** Written with `http.client` and raw sockets, so that `Host`, headers, methods, un-normalised
  paths and withheld bodies are exactly what was sent. Results are JSON or text files (p1–p8).
- **Browser.** Headless Chromium only: no Firefox, no WebKit, no real device.
- **Port-forwards and proxies.** Not exercised; m5 stands as documented.
- **Staff, inactive and privileged refusals.** Proved by the engineer's tests (green, §2) and by reading the code, not
  live. Exercising them live would need edits to dev.py's allow-list or the lane's data, which a read-only reviewer
  does not make. The live data was checked with a read-only query.
- **m6 and m7.** Each was measured on my own server only. m7's slot exhaustion lasted about 22 s and touched no other
  server.
- **Step 10c of the browser series.** The product's sign-out was submitted by script (`form.submit()`), which
  fires no `submit` event. So the landing's script did not reload the strip, and the strip still named the persona.
  The session itself ended (the dashboard then answers 302 to the sign-in). The engineer's browser test, which
  clicks, covers the strip (UX's lens).
- **Not this lens.** «At most one frame pair» and «the strip paints in ≤ 1 s» belong to the performance and UX
  reviewers. The engineer's browser tests for them ran inside my suite run.

## 8. Evidence index (E/ = `C:/tmp/ile_v5_council/evidence/v54/w1-p/security-r2/`)

| File | What |
|---|---|
| `E/p1_gate_r2.json` | the gate: 16 routes × 42 refused callers × 7 methods (4,704, all plain 404); 240 names outside `ALLOWED_HOSTS`; no `Host`; 80 with headers outside the list |
| `E/p2_proof_guards_r2.json` | 49 strings × `research/proof/` and old `/proof/`, 18 × `decisioni/` |
| `E/p3_persona_switch_and_read_only_r2.json` + `E/p3_server_log_slice.txt` | 101 rows: CSRF, Origin, the gate before CSRF, methods, allow-list, hostile `page` on «Entrer» and «Sortir», 34 refused writes, forged-log paths, framed refusals, `set_language`, `account_logout`; the server log of that run |
| `E/p4_frame_exception_r2.json` | 47 header cases with each full CSP and the directive diff; the landing, index and hub policies against `/fr/` |
| `E/p5_ceiling_log_probe.txt` + `E/p5_ceiling_log_slice.txt` | m7: eight withheld bodies, the 503 after 20 s, the forged line |
| `E/p6_misc_r2.txt` | reflections (`?page=`, `?frame=`, `?lang=`), five more `Host` variants, the DEBUG 404 listing the mount |
| `E/p7_refusal_relaxed_by_method.txt` | m6: the refusal relaxed for POST, PUT, PATCH, DELETE, `FOO` and TRACE; anonymous PUT/DELETE strict |
| `E/p8_nul_technical_500.txt` | O1: a NUL byte turns the gate's 404 into the DEBUG technical 500 (view named, `DATABASE_URL` in META — redacted in the file); control without the NUL |
| `E/b-browser/browser_series_r2.json` + PNGs | the browser series: 8 framing attacks from other origins, DNS rebinding, login CSRF and cookie tossing, the landing (1 frame, 0 violations), dot segments (400), the in-frame redirect and form answer, the refused back-office frame, the persona flow with the in-frame refusal, the product's own sign-out and «Sortir»; `run.log` |
| `E/t1_settings_refuse_preview_r2.log` | prod / staging / test / dev-without-DEBUG refuse; dev + flag mounts (5 passed) |
| `E/t2_w1p_suites_on_l9_r2.log` | `test_design_preview` + `tests/security` on `test_ile_v5_l9` |
| `E/t3_database_refusal_r2.log` | `ile_qa`, `ile` and five more refused before any query; control proceeds (8 passed) |
| `E/n1_bind_and_reachability_r2.txt` | listeners on 127.0.0.1 only; LAN and virtual-adapter connects fail |
| `E/scripts/` | every probe, the browser series, the quiet-period gate and the two scratch tests (none in the repository) |
| `C:/tmp/ile_v5_council/.work/servers/srv8789-w1p-security-r2.{err,out}.log` | my server's log: the persona lines, m2's escaped vectors, m7's forged line, the NUL tracebacks of O1 |
