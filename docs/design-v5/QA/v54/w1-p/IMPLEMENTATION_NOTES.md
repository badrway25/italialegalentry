# W1-P · Preview as the live product — implementation notes

Italy Legal Entry™ design V5 · V5.4 «EXECUTION MODE» · 5 October 2026 · the Preview Engineer (label
`w1p-engineer`) · plan `docs/design-v5/V5_4_EXECUTION_PLAN.md` §4 (4.1–4.6), §3.3 item 3, §2.2, §2.7 ·
DL54-01 (branch `v54-w1-p`, merge tag `v54/w1-p`).

Branch `v54-w1-p` from `v54/base` (`f11d131`), worktree `C:/tmp/ile_wt/v54-w1-p`, lane 4 (server
`127.0.0.1:8784`, database `ile_v5_l4`, tests on `test_ile_v5_l4`). Not merged into design-v5. Every
path written is inside W1-P's slice of `docs/design-v5/OWNERSHIP_V54.json`:
`scripts/check_ownership.py w1-p v54/base` → **23 inside, 2 slice → PASS** (the two slices: the
preview block of `config/settings/dev.py`, and the persona line of `tests/security/test_log_privacy.py`).

| Commit | What |
|---|---|
| `1338303` | the shared gate (`access.py`), the frame exception (`frames.py`), the persona switch and the read-only rule (`personas.py`), the preview block of `dev.py` |
| `aab76d2` | the live product — landing, strip, index (`live.py`, views, urls, templates, sheet, script); the hub moved to `/research/`, with redirects |
| `7bb39e5` | `tests/frontend/test_design_preview.py` rewritten, under the dev middleware chain |
| `bb1ba5b` | the persona line of `tests/security/test_log_privacy.py` |

This file is the fifth commit, on its own.

---

## 1. What `/__design-v5/` is now (plan §4.1)

**The landing** (`views.landing`, `templates/dev/designpreview/landing.html`). The real `/fr/` page of
this server, full window, in **exactly one** same-origin frame, under a **40 px strip** that sits outside
the page. `?page=` frames another page of this site — a path under `/fr/`, `/ar/`, `/it/` or `/en/` of
this server, nothing else (`live.page_param`: no scheme, no other origin, no `//`, no backslash or control
character, not the preview itself; a refused value is a 400 with the way back, never framed). `?frame=phone`
draws the page in a phone of 390 CSS px (up to 844 px tall); without it the frame is the window.

**The strip** (`_strip.html`), from the start of the row to its end:
- **the name** — «Italy Legal Entry™ — V5, la migliore di oggi» (the claim from 90 rem; below 48 rem the
  mark and «V5»; at 320 px the mark);
- **the build** — the tag this worktree is checked out at (on 8780: v5-live's tag), its commit, and its
  date in the tooltip and in the menus (`live.identity`: git, asked once per process — 8780 is restarted
  after every checkout). On a lane it reads «ramo v54-w1-p · aab76d2»;
- **the state of the page in the frame** — «V5 — council-passed» **only** where the steward's
  `live_status.json` says `"v5"` for that surface; «V4 + fondation» everywhere else, and everywhere when
  the file is absent, unreadable or silent (§3 below);
- **the page's languages** — fr and ar everywhere; it and en as well for the home and the login;
- **the frame** — «Desktop» / «Telefono 390», changed without reloading the page the frame holds;
- **the council-passed surfaces** as quick links (none today: the group is not drawn while it is empty);
- **«Personas»** — the four QA personas, «Entrer» (a POST with its CSRF token) and, when one is in, a dot,
  its name and «Sortir»;
- **«Novità»** — «Cambiato dall’ultimo rapporto»: three lines of the steward's
  `docs/design-v5/CHANGELOG_V54.md`, opened on demand (absent today: it says so);
- **«Indice»**, and **«Apri da sola»** (the page alone, in a new tab; the full sentence is its tooltip).

From 80 rem everything stands on one row; below, the name, the state, «Personas» and «Indice» stay and
the rest is in «Altro»; below 48 rem «Indice» joins it. The menus are `<details>` (no script needed); the
script closes them on Escape, on a click elsewhere and when the focus steps into the frame, one open at a
time. When the page in the frame navigates, the script moves the strip with it — its state, its
languages, «Apri da sola», the frame links, the persona forms — and keeps it in the address bar
(`?page=`), so a reload frames it again.

**The index** (`views.index`, `index.html`), one click away: every public page (33 rows, from the URL
names in `live.PUBLIC_PAGES` — a path that changes later changes here by itself) in fr and ar (it and en
for the home and the login), each URL opened in the landing's frame, each with «Desktop 1440» and
«Telefono 390» and its twin on the V4 control (`http://127.0.0.1:8771…`, never this server); the «V4 +
fondation» pages **grouped apart, collapsed**, the council-passed ones above them; the four persona cards
with their pages in fr and ar; the states without credentials (§4.5); the families' status board; the
foundation's specimen boards; the V4 comparison; the research archive.

**At most one frame pair at a time** (RTE-m9). The index's markup holds no frame. Its script
(`static/js/dev/designpreview.js`, part 3) opens frames in a modal viewer: a *pair* is the desktop frame
and the phone frame of **one** address. Opening a frame of another address first unloads the pair it
holds — each frame emptied (`about:blank`) and removed — then loads the next; closing the viewer
(button or Escape) unloads it; a frame of the pair is never doubled (`MAX_FRAMES = 2`). Without the
script the two links open the landing, which holds one frame.

## 2. The research archive (plan §4.2, §4.3)

The hub, the hero and type pickers, the compare view and the proof files, **as they were**, under
`/__design-v5/research/` (`research/`, `research/hero/`, `research/type/`, `research/compare/`,
`research/proof/<path>`). The URL names did not change, so every link the catalogue builds moved by
itself; the «prototipo di ricerca — non approvato» labels are kept. The old addresses —
`/__design-v5/hero/`, `/type/`, `/compare/`, `/proof/…` — answer **302** to their equivalents, query
string kept; an old proof path is judged by its string first (`services.refuse_proof_string`, the
resolver's first layer on its own), so a redirect is never broader than its target. An old link to an
anchor of the hub (`/__design-v5/#g-he`) is sent on by the landing's script to `research/#g-he` — a
fragment never reaches the server; every other fragment is left alone.

What left the main path (§4.3): the pickers, the A/B/C pages, the «non approvato» banners and the proof
frames are in the archive only; the index of frames is one click away, not the landing. **The «Baseline V4
(controllo)» group left the archive too**: it linked this server's own pages as V4, which they stop being
the moment V5 enters the templates; the V4 control is compared on 8771, in the index. «In arrivo (V5.2
§7.2)» stays, as the archive was. The archive says what it is in its masthead and under its title, with
the way to the live product and its index.

## 3. What the preview reads and never writes — for the steward

**`docs/design-v5/live_status.json`** (path: `ILE_DESIGN_PREVIEW_LIVE_STATUS`, dev.py). Written by the
steward only (`steward_only` in the manifest); read on every request. Schema `ile-live-status-v54/1`:

```json
{
  "schema": "ile-live-status-v54/1",
  "updated": "2026-10-06",
  "families": [
    {"key": "w1-a", "title": "Fondazione: token, tipo, colore, angoli", "state": "v5",
     "scores": {"visual": 4, "premium": 4, "originality": 4, "ux": 4, "mobile": 4, "coherence": 4},
     "decision": "w1-a/CD_DECISION.md", "tag": "v54/w1-a", "date": "2026-10-06"}
  ],
  "surfaces": {"home": "v4-fondation", "login": "v5"}
}
```

- A state is the word `"v5"` (or an object whose `state` is `"v5"`) or anything else, which reads as
  «V4 + fondation». `"V5"`, `"passed"`, a missing key, a malformed file: «V4 + fondation».
- `surfaces` is keyed by the page keys the index lists under «Le chiavi delle superfici, per lo steward»
  (`live.surface_keys()`): `home`, `login`, `signup`, `password-reset`, `companies`, `institutions`,
  `universities`, `pilot`, `pathways`, `diplomas`, `training`, `orientation`, `project`, `agami`,
  `network`, `antifraud`, `contact`, `company-needs`, `institution-proposal`, `university-proposal`,
  `contact-form`, `forum`, `community`, `news`, `faq`, `glossary`, `living`, `partners`, `privacy`,
  `cookies`, `notices`, `terms`, `disclaimer`, and the persona pages `dashboard`, `case`, `documents`,
  `situation`, `requests`, `journey`, `deadlines`, `messages`, `profile`, `company`, `company-profile`,
  `company-needs-list`, `company-analysis`.
- `families` feeds the status board: six scores (other keys ignored), the CD decision — a Markdown file
  relative to `docs/design-v5/QA/v54/`, served as text by `/__design-v5/decisioni/<path>` through the
  proof server's resolver (`.md` only; dotted segments, traversal, 8.3 aliases, links refused) — the tag,
  the date. «V4 + fondation» families are grouped apart, collapsed.

**`docs/design-v5/CHANGELOG_V54.md`** (`ILE_DESIGN_PREVIEW_CHANGELOG`): the strip shows its first three
list items (`- ` or `* `), newest first as written; `**` and backticks are dropped.

## 4. How the authenticated pages are reached (plan §4.4)

**One gate for every route** (`apps/designpreview/access.py`), checked by every view before the method:
DEBUG and `ILE_DESIGN_PREVIEW=1`; `REMOTE_ADDR` on loopback **and no proxy header** — the plan's five
(`X-Forwarded-For`, `Forwarded`, `X-Real-IP`, `X-Forwarded-Host`, `CF-Connecting-IP`) and eleven more that
tunnels and port-forwards add (`X-Forwarded-Proto`, `-Port`, `-Server`, `X-Original-Forwarded-For`,
`Via`, `True-Client-IP`, `X-Client-IP`, `X-Cluster-Client-IP`, `Fastly-Client-IP`, `CF-Ray`, `CDN-Loop`),
present at all, even empty; `Host` exactly `127.0.0.1:<port>` or `localhost:<port>` for
`ILE_DESIGN_PREVIEW_PORT` (8780; each lane exports its own — LANES.json's commands already do). Refused:
Django's 404, before any 405, without the preview's seals. A name outside `ALLOWED_HOSTS` never reaches
it (400).

**The switch** — `POST /__design-v5/accedi/<persona>/`, `POST /__design-v5/esci/` (`personas.py`,
`views.persona_enter`, `views.persona_exit`). POST only (405 otherwise, `Allow: POST`), CSRF enforced by
the view's own decorator. The allow-list: the four QA accounts by e-mail in dev.py
(`ILE_DESIGN_PREVIEW_PERSONAS`; their names and pages are in `personas.PERSONAS` and
`live.PERSONA_PAGES`). Refused with a sentence and 403: a staff or superuser account (whatever the
allow-list maps the key to), an absent or inactive account, any database not in
`ILE_DESIGN_PREVIEW_ALLOWED_DATABASES` (`ile_v5`, `ile_v5_l3` … `ile_v5_l9`) — and **`ile_qa` and `ile`
always**, even if a setting names them (`ile` is the V4 control's on 8770 and 8772). An unknown persona key
is a 404. The sign-in is `auth.login(request, user, backend=ModelBackend)`: `user_logged_in` is sent (the
audit trail records `auth.login`; W1-D's release flag will ride on it), the session key is rotated, and
the session carries `ile_design_preview_persona`. **One log line** per event, with the persona key, never
the e-mail: `Design preview: persona qa-doc-person signed in (read-only session).` — and `… refused
(staff|unknown|database).`, `… signed out.`. After «Entrer» the browser lands on the landing framing the
persona's first page (the console dashboard, or the company's space), so the release plays there; after
«Sortir», on the public page it came from (a reserved page needs a session: its language's home).

**Read-only personas** (`PersonaReadOnlyMiddleware`, last in the chain): while the flag is set, every
method but GET, HEAD and OPTIONS outside `/__design-v5/` is answered **403** in plain words («Anteprima V5
— persona in sola lettura … non è stato eseguito, e niente è cambiato … Per uscire: «Sortir»»), sealed,
before any view — except `account_logout` and `set_language`. The personas never drift. Measured on
lane 4: as `qa-person`, the «Ma situation» form submitted inside the frame shows the refusal in the
frame (`c1-final/08_…png`).

**Distinct cookies** (dev.py's preview block): `ile_v5_sessionid`, `ile_v5_csrftoken`, `ile_v5_language`.

**Frames** (`frames.py`, `PreviewFrameMiddleware`, listed after `CSPMiddleware` and
`XFrameOptionsMiddleware`): the codebase's own `_csp_replace` pattern — `frame-ancestors 'self'`, merged
into whatever a view replaced, and `X-Frame-Options: SAMEORIGIN`, which XFrameOptions keeps — only for
GET or HEAD, `Sec-Fetch-Dest: iframe`, `Sec-Fetch-Site: same-origin`, the gate's caller, outside
`/backoffice/` and `/__design-v5/`; `Vary: Sec-Fetch-Dest, Sec-Fetch-Site` on every response it judges.
Everything else keeps `frame-ancestors 'none'` and `DENY`. Absent under the test and production settings.

**The chain** in dev.py: `ConnectionCeilingMiddleware` first, the base chain unchanged, then
`PreviewFrameMiddleware`, then `PersonaReadOnlyMiddleware`.

No password is used, typed or stored anywhere: the QA accounts' e-mails are the allow-list, the session is
minted for the account the preview's own database holds.

## 5. The loader and the states, without credentials (plan §4.5)

The index's «Stati senza credenziali»: **the engage** — the login, opened alone (its error page is the
answer to a POST, which no frame may show: the plan's GET-or-HEAD rule), «Un indirizzo qualunque e una
password sbagliata»; **the release** — «Entrer» as a persona; **the stage's states** — the login in the
frame; **the 429 page** — `/__design-v5/stati/429/`, the site's own `errors/429.html` with status 429
(the preview's own DEBUG state route: `config/urls.py` has no owner in the manifest, so the route lives in
the app); and the DEBUG error pages `/_errors/400|403|404|500/`.

## 6. Decisions met during the build — for the council and the CD to ratify (proposed DL54 entries)

1. **The strip and the index speak Italian**, as the preview always has (the reviews of the hub checked
   «etichette italiane»), and keep verbatim the plan's proper names: «V5 — council-passed», «V4 +
   fondation», «Personas», «Entrer», «Sortir», the persona names. «Index» → «Indice»; «Changed since the last
   report» → «Cambiato dall’ultimo rapporto» (under «Novità»); «Open the page alone» → «Apri da sola» (the
   full sentence is the tooltip and the «Altro» link).
2. **The read-only refusal may be shown by a same-origin frame** although it answers a POST. The plan
   relaxes GET and HEAD only, for real pages; the refusal is the preview's own sentence in `text/plain` —
   no page, no form, nothing to click — and without the exception the owner sees «refused to connect» in
   the frame instead of what was not done. Same conditions as the frames otherwise (the gate's caller,
   `Sec-Fetch-Dest: iframe`, same-origin).
3. **The gate pins the Host on every preview route**, not only on the switch (§4.6 lists «404 with a
   foreign Host» among the guards); a refused caller meets 404 before any 405.
4. **Eleven proxy headers beyond the plan's five**; **`ile` refused beside `ile_qa`**.
5. **The 429 state route lives in the app** (`/__design-v5/stati/429/`): `config/urls.py` has no owner.
   When W2-B or the steward adds `/_errors/429/` there, the index can point at it.
6. **The CD decision is served** (as text, `.md` only, through the proof resolver) so that the status
   board's «link to the CD decision» is a link.
7. **Every standalone preview document loads the font and token layers listed by `static/css/main.css`**
   (`services.token_stylesheets`, `_stylesheets.html`) instead of naming `css/fonts.css` and the token
   files: W1-A removes `fonts.css` and adds `v5/fonts.css` and `v5/tokens.css`; the pickers, the compare
   view, the landing and the index follow without an edit. At `v54/base` they resolve to exactly the four
   files frame.html named before. (They never load `dist/main.css`: `base.css` hides every iframe.)
8. **live_status.json and the changelog** live in `docs/design-v5/` beside the plan (§3 above); the
   preview never claims a pass the steward has not written.

## 7. Acceptance (plan §4.6) — where each item is proved

| Item | Proof |
|---|---|
| absent without the flag (404) | `test_absent_without_the_flag`, `test_answers_404_without_the_flag`, `test_the_views_refuse_even_if_someone_wires_them_up`, `test_dev_settings_read_the_flag_from_the_environment` |
| 404 off loopback, with a proxy header, with a foreign Host | `test_every_route_is_a_404_off_loopback_behind_a_proxy_or_for_another_host` (14 routes × 2 addresses, 16 headers set, 5 present-but-empty, 5 hosts; GET and POST), `test_the_gate_answers_the_port_of_its_own_process` |
| 405 on GET for accedi / esci | `test_an_allowed_caller_meets_405_for_a_method_a_route_does_not_take` |
| staff, unknown accounts, a database outside the list — `ile_qa` included — refused | `test_the_switch_never_opens_a_staff_session_whatever_the_allow_list_says`, `test_the_switch_refuses_an_unknown_persona_and_an_absent_or_inactive_account`, `test_the_switch_refuses_any_database_outside_its_list_and_the_v4_control_s_always` |
| distinct session, CSRF and language cookie names | `test_dev_settings_read_the_flag_from_the_environment`; `ile_v5_sessionid` set by the switch (client test and browser test) |
| persona sessions read-only: 403 outside the preview, the allow-list excepted | `test_a_persona_session_cannot_write_outside_the_preview`, `test_a_session_that_is_not_a_persona_s_is_not_touched_by_the_rule`, `test_the_read_only_rule_and_the_frame_exception_do_nothing_outside_the_preview_s_condition` |
| the log line carries no e-mail | `test_the_switch_signs_a_persona_in_read_only_and_logs_its_key_never_its_e_mail`; `tests/security/test_log_privacy.py::test_the_persona_switch_logs_a_persona_key_never_an_e_mail` |
| frames load real pages only under the narrow condition | `test_a_real_page_is_framed_by_this_origin_only_when_every_condition_holds` (13 failing conditions, POST, back-office, preview pages, flag off, DEBUG off), `test_the_frame_exception_merges_into_what_a_view_has_replaced`, `test_the_dev_chain_puts_the_ceiling_first_the_frame_exception_after_csp_and_the_read_only_rule_last`, `test_a_frame_of_this_origin_may_show_the_refusal_and_nothing_else_may` |
| at most one frame pair at a time, enforced by the hub's script | browser: `test_the_index_never_holds_more_than_one_pair_of_frames` (an observer counts every frame, most = 2); static: `test_the_templates_are_clean` (no frame in the index's markup, one in the landing's) |
| the strip paints in ≤ 1 s, the landing loads exactly one frame | browser: `test_the_landing_draws_one_frame_of_the_real_home_under_a_strip_of_40_px` (1440 × 900 and 390 × 844, fr and ar: FCP ≤ 1000 ms, one frame, strip 40 px); captures: FCP 36–92 ms warm, 708 ms on the first request after a server start |
| 0 CSP violations | the two browser tests above collect `securitypolicyviolation` in the landing, the framed page and the index's frames, and the console's «Content Security Policy» / «Refused to» lines: 0; the capture series: 0 |
| the research archive's tests keep passing at their new paths | every archive test of `v54/base` kept (paths moved to `research/`), plus `test_the_archive_s_old_addresses_redirect_to_their_research_equivalents`, `test_an_old_proof_address_is_judged_before_it_is_redirected`, `test_the_archive_says_what_it_is_and_has_left_the_baseline_group`, `test_an_old_anchor_of_the_hub_opens_the_archive_at_that_anchor` |
| v5-live checked out at the tag, 8780 restarted after the merge | the steward's and the orchestrator's (not this lane's) |

## 8. Tests and suites (plan §2.7, W1-P)

`tests/frontend/test_design_preview.py` — rewritten for the new shape: 130 test functions, 271 items
(87 and 182 at `v54/base`). Every preview test runs with the preview block of `config/settings/dev.py`
installed **as the owner's server reads it** — its middleware chain, cookie names, port and personas,
imported from the module itself once per session (`dev_preview`, `_dev_settings`, base settings put back)
— and the test client calling from 127.0.0.1 on `127.0.0.1:8780`. The test database is not among the
databases a persona may be opened on unless a test says so (`this_database`). Every old guard kept:
dotted segments, traversal (plain and percent-encoded), 8.3 short names and links, extensions and content
types, the policies (proof files, every other page, the global settings untouched), the seals, the ceiling
and its bursts at the `runserver` class (which now answers the port it binds), the catalogue against the
real package. Browser tests: 3 of the archive (on `live_server`, whose port the gate is told) and 5 of the
live product (on the `runserver` class with the dev chain and the static handler — `live_server`'s chain
was built before the test and has no frame exception).

Runs on lane 4 (`TEST_DATABASE_URL=…/ile_v5_l4` → `test_ile_v5_l4`), lock-gated:

| Run | Result | Log |
|---|---|---|
| baseline at `v54/base` (the three new modules already on disk) | 305 passed, 1 failed (the LF test counting those modules) | `E/w1-p/a0_baseline_w1p_suites_v54base.log` |
| W1-P suites, run 1 — `test_design_preview` (browser included) + `tests/security` | **395 passed, 0 skipped, 0 failed** (308 s) | `E/w1-p/b1_w1p_suites_r1.log` |
| W1-P suites, run 2 — on the committed code | **395 passed, 0 skipped, 0 failed** (389 s) | `E/w1-p/b2_w1p_suites_r2.log` |
| adjacent suites — the dev-settings lifetime test, env example, ownership, the QA password, template comments, design docs, static assets, V4 tokens, the shim, CSS tokens, `tests/i18n`, `tests/compliance` (not browser) | 506 passed, 1 xfailed, **4 failed, none of them W1-P's**: `test_form_unavailable_notice_is_translated_on_every_public_form` (`[it]`, `[en]`, `[ar]`) are three of the 27 failures of `v54/base` (W1-0's `h1_not_browser.log`); `test_cited_paths_exist` is the worktree's — `docs/I18N_RTL.md` cites `docs/qa/rtl/`, an untracked folder present in design-v5's worktree and absent from a fresh one | `E/w1-p/b3_adjacent_suites.log` |

(E/ = `C:/tmp/ile_v5_council/evidence/v54/`.) The full `pytest -m "not browser"` (75 min at `v54/base`,
27 known failures there) was not re-run by this lane: W1-P changes nothing outside the preview's own
files, the preview block of dev.py and one test of `tests/security`; the steward runs everything at the
merge. ruff check and ruff format: clean on every Python file touched.

## 9. Captures — looked at, one by one

Lane 4, headless Chromium with its own profile (`C:/tmp/ile_v5_council/.profiles/w1p-engineer`), no
password (the persona switch). Final series: `E/w1-p/c1-final/` (16 shots and `report.json`):
`01_landing_{fr,ar}_{1440x900,390x844}`, `02_landing_fr_phone_frame_1440x900`,
`03_landing_novita_1440x900`, `03_landing_altro_390x844`, `03_landing_personas_390x844`,
`04_index_1440x900`, `04_index_1440_full`, `04_index_390_full`, `05_index_viewer_pair_1440x900`,
`06_research_archive_1440x900`, `06_research_old_address_redirected_1440x900`,
`07_persona_doc_person_dashboard_{1440x900,ar_1440x900}`, `07_persona_doc_person_case_390x844`,
`08_persona_read_only_refusal_in_frame_1440x900`. In every one: the strip 40 px; one frame on the landing,
holding the real page (its path and `lang` read from inside the frame); no horizontal overflow; no
policy violation; no failed request but the intended 403 of the read-only refusal.

What looking found, and what was fixed before the commits:
- first series (`E/w1-p/r1/`): the strip ran edge to edge at 1440 («Indice» touching «Apri…»), **overflowed
  by 23 px at 390** and **by 42 px at 1440 with a persona's name** — «Personas : …» even carried a stray
  space. Fixed: the wordmark left the strip (the page's own header carries it right below), the build
  shows its tag and commit, the controls stand at the end after a hairline, the persona's name is capped
  (11 rem; below 90 rem 8 rem; on a phone a dot, the name kept for screen readers), «Indice» joins
  «Altro» below 48 rem, the narrow layout starts at 80 rem.
- the geometry was then measured, not guessed (`E/w1-p/r2-widths` … `r5-widths`, `strip_widths.json`):
  14 widths from 320 to 1920, signed out and as `qa-company`, plus the index at 1440 and 390 — 40 px
  everywhere, 0 overflow, 0 overlap, nothing outside the window, no target under 24 px (r5).
- the current language and frame were filled pills that read as primary buttons: now a quiet tile.
- a lane server runs `--noreload`, and the cached template loader kept serving the old strip after a
  template change: the server is restarted after every template or Python change before a capture.

## 10. For the other lanes and the steward

- **A preview server must export `ILE_DESIGN_PREVIEW_PORT`** (its own port). Without it the gate expects
  8780 and every preview route is a 404 on another port — closed, by design. The LANES.json commands
  already export it.
- **Sessions minted for a preview server** are read from `ile_v5_sessionid`: a script that mints with
  `settings.SESSION_COOKIE_NAME` under the dev settings with `ILE_DESIGN_PREVIEW=1` is right by itself; one
  that hard-codes `sessionid`, or mints without the flag, must hand the cookie over under the new name.
  8782 (no preview flag) is unaffected.
- **W1-A** removes `css/fonts.css`: nothing to do in the preview's documents (they follow main.css's
  import list); the archive's hub extends `base.html`.
- **W1-D**: the release flag rides on `user_logged_in`, which the switch sends.
- **The steward**: `live_status.json` and `CHANGELOG_V54.md` as in §3; `config/urls.py` needs nothing (the
  mount is unchanged; the new routes are inside the app).

## 11. Honest limits

- Chromium on Windows only (headless Playwright); no WebKit, no Firefox, no real phone, no screen reader.
- The strip is a development tool: its look has not been scored by the council (UX lead, security,
  accessibility, performance, CD — plan §3.3 item 3). The security reviewer should read §4 and §6 items 2–4
  first.
- The index's «Desktop 1440» frame is drawn at its true size: in a 1440 window the phone frame of the pair
  is beside it, past the right edge (the viewer scrolls). Nothing is scaled.
- The read-only refusal is plain text in the browser's default face.
- The persona switch needs the four QA accounts on the preview's database (counted on `ile_v5` by W1-0;
  present on `ile_v5_l4`). A sign-in writes what a sign-in writes — the audit row and `last_login` — and
  nothing of the persona's dossier.
- `Sec-Fetch-*` decides the frame exception: a browser without it (none current) would meet the strict
  policy and an empty frame, never a looser one.


---

## Review fixes — round 1

5 October 2026 · the Preview Engineer, fix round 1 (label `w1p-fix-1`) · the four council reviews of round 1,
committed as they were written: `docs/design-v5/QA/v54/w1-p/{ux,security,a11y,performance}.md` (`0dedb7e`) — UX
FAIL (1 blocking, 6 major, 11 minor), security PASS WITH FIXES (1 major, 5 minor), accessibility FAIL (1 blocking,
2 major, 9 minor), performance PASS_WITH_FIXES (2 minor). Same branch, worktree, lane and databases as above; no merge
into design-v5; design-v5 holds no clock-fix commit yet (its one new commit, `76c6795`, is W1-K's QA folder), so
nothing was merged in. `scripts/check_ownership.py w1-p v54/base` → **30 inside, 3 slice → PASS** (the slices: the
preview block of `config/settings/dev.py`, the persona line of `tests/security/test_log_privacy.py`, W1-P's
append-only entries of DL54).

| Commit | What |
|---|---|
| `0dedb7e` | the four reviews, as their authors left them in the family's QA folder |
| `23ca9b6` | the persona switch (privileged roles, escaped log line, the refusal's words) and the ceiling (a small body read before the slot) |
| `1ea7d06` | the frame exception (a form's answer, no `upgrade-insecure-requests`), the gate before CSRF, `page_param`, the census in `live.py`, the switch's page, the surfaces' data, dev.py's scratch copies |
| `f7555d1` | the templates, the sheet and the script — what the owner sees |
| `2a05390` | the tests |
| `60196ec` | DL54-17 and DL54-18 |

This section is the seventh commit, on its own.

### Every blocking and major finding

| Finding | What was done | Held by |
|---|---|---|
| **UX B1 / security M1** — a redirect or a form's answer in the frame left a blank frame and policy violations (§4.6 «0 CSP violations») | The landing and the index drop `upgrade-insecure-requests` (`@csp_replace(NO_UPGRADE)`, django-csp omits a directive replaced by `None`), and so does a page framed under the narrow condition (`frames.RELAXED`): a frame inherits its parent's insecure-requests policy, and Chromium upgraded the frame's redirect hops to https on this plain-http server. A form's answer (POST) inside the frame is relaxed under **exactly** `framed_by_this_origin` — the same excluded prefixes, the read-only rule still first — as the security reviewer allowed: **DL54-17**, superseding §4.4's «GET or HEAD». A page that can never be framed (the back-office, the preview's own pages, another site) now shows the stage's message — «Questa pagina non si apre nella cornice», with «Apri la pagina da sola» at the address the link asked for and «Torna alla pagina di prima» — never a blank frame. The global policy is untouched (`base.py` keeps both directives). | `test_a_real_page_is_framed_by_this_origin_only_when_every_condition_holds` (cross-site, same-site, `none`, `document`, proxy header, foreign Host, off-loopback POST answers stay strict; PUT never relaxed), `test_a_relaxed_policy_differs_from_the_strict_one_in_two_directives_and_nothing_else`, `test_the_global_policy_is_not_edited_by_the_app`; browser: `test_a_redirect_and_a_form_s_answer_render_in_the_frame_without_a_policy_violation` (signed out, `?page=/fr/espace-reserve/` ends on the sign-in rendered; its empty submission renders), `test_the_product_s_own_sign_out_in_the_frame_ends_on_the_home_and_the_strip_follows`, `test_a_page_the_frame_cannot_hold_is_said_never_a_blank_frame` — each with 0 `securitypolicyviolation` |
| **UX M1** — the index's pair was never visible as a pair at 1440 | The desktop frame still lays its page out at 1440 CSS px and is drawn scaled to fit beside the phone (a box of the scaled size, `transform: scale(var(--dp-scale))`, the scale computed by the viewer's script from the window on open and on resize); «1:1» draws it at its true size. Measured: at 1440 × 900 the desktop frame 991 × 620 at x 16–1007, the phone 392 at x 1031–1423; at 1280 × 800, 831 × 520 and 871–1263. | browser: `test_the_viewer_shows_both_frames_of_the_pair_at_the_owner_s_widths` (both inside the window, side by side, the desktop laid out at 1440 and the phone at 390, «1:1» 1442 px) |
| **UX M2** — the index exposed 47 of the census's 79 page types; `/documents/` refused | `live.PUBLIC_PAGES` / `PERSONA_PAGES` mirror W1-0's census (`C:/tmp/ile_v5_council/evidence/v54/w1-0/before/PAGE_TYPES.json`) one row per page type, under the persona the census captured it with, detail pages by the census's own example ids (present, identical, on `ile_v5` and the lane clones): the Guichet numérique, the Academy, the documents app, the request detail, «Mes dossiers», the new-need form, the account pages, the pathway, glossary and living detail pages, the success and state pages; the census's states under «Stati senza credenziali» (the open menu, a step of the questionnaire, the 404, the 410, the 403); the four role-account types «fuori dall’anteprima». **A surface key is now a census id** (`home`, `door-persons`, `legal-document` for the five legal texts, `dashboard-person` …): the steward marks a page type and every page of that type follows; a detail page is matched by the pattern of its address, so any case of a marked type says so. `page_param` accepts `/documents/`; `?lang=` gives a page of the documents app its language — the landing sets the language cookie, as `core.middleware.LanguageCookieMiddleware` does for a prefixed page — and the script follows every page the landing may frame (`map.follow`: a language prefix or `/documents/`, the one rule `page_param` applies, so that a reload frames what the strip names — narrower than the review's «any same-origin path outside …» only by the technical addresses `/healthz/`, `/robots.txt`, `/sitemap.xml`, `/wp-login.php`, which are no page to follow). | `test_the_index_covers_every_page_type_of_w1_0_s_census` (against a copy of the census in the test), `test_the_census_the_index_mirrors_is_w1_0_s` (the copy against the file, where it is on disk), `test_the_index_lists_every_public_page_in_fr_and_ar_with_its_frames_and_its_v4_twin`, `test_a_page_of_the_documents_app_is_framed_in_the_language_it_was_asked_for`, `test_the_landing_frames_a_page_of_this_site` (`/documents/…`) |
| **UX M3** — only a persona's first page was two clicks away; its page links were a trap | While a persona is not inside, each of its pages is a small POST form to `accedi/<persona>/` per language («fr», «ar»), carrying `page` and `lang`; the switch honours `page` only when it is one of **that persona's own** pages in any of its languages (`live.persona_urls`), its first page otherwise. Every listed authenticated page is «Indice» → «fr»/«ar»: two clicks. The persona inside keeps links. | `test_one_click_enters_a_persona_and_opens_its_page_only_if_the_page_is_its_own` (another persona's page, a public page, another origin, a dot segment, an extra query: the first page), `test_a_persona_s_pages_are_links_once_it_is_inside_and_forms_for_the_others`, `test_the_index_offers_the_four_personas_and_never_a_staff_one` |
| **UX M4 / a11y m8** — folds that did not look like folds; the public pages hidden | `.dp-index__summary::after`, the strip's chevron, turning under `[open]` (its transition only under `prefers-reduced-motion: no-preference`); the public fold is open while nothing has passed (`{% if not passed %} open`), collapsed once a page has. | `test_the_index_groups_the_v4_fondation_pages_apart_open_until_one_passes` |
| **UX M5 / a11y M2** — the quick links outgrew the strip | One menu, «Superfici V5 · n», drawn only when n > 0, public pages then each persona's (a persona's page is a POST that enters it when it is not inside); below 80 rem the same list stands in «Altro». The row's tiers were then measured in the worst case — the longest persona name, every language, «V5 — council-passed» and the menu: the claim from 120 rem, the build from 100 rem, «Italy Legal Entry™ — » from 90 rem (the build and the claim stay in «Novità» and «Altro»). The state's words may shrink with an ellipsis before anything leaves the window. Measured (`E/w1-p/fix-1/widths-r3/`): 17 widths × signed out and `qa-person` × 0, 2, 6, 12 passed surfaces = 136 rows, **0** with a strip ≠ 40 px, a horizontal scroll, an overlap, a control outside the window or under 24 px; the words shrink only for «V5 — council-passed» at 320 (and 360 with a persona inside). | `test_the_strip_never_outgrows_its_row_with_council_passed_surfaces` (2, 6, 12 at 1280 and 1440, signed out and as `qa-person`; the list in «Altro» at 1024), `test_the_strip_says_v5_only_where_the_steward_s_live_status_says_so` |
| **UX M6** — the archive still handed the owner decisions V5.4 closed | Its framing only (plan §4.2: the notes as they were): H1 «Archivio della ricerca»; an archival lead («conservati come erano, per tracciabilità»); the warning replaced by one historical notice — the notes date from before 4 October 2026; where they say «decide il proprietario», the council decides now and a family that passes propagates without waiting; nothing shown is approved; the live product is the landing. The reviewers' status sentence of the time is kept in it. Every «non approvato» tag kept. | `test_the_archive_says_what_it_is_and_has_left_the_baseline_group`, `test_the_hub_says_that_a_research_prototype_is_not_approved_wherever_one_stands` |
| **a11y B1** — the index's sticky strip hid the focus (WCAG 2.4.11, plan §1.6) | `scroll-padding-block-start: 56px` on `.dp-live-root`; the sections' `scroll-margin-block-start` removed. | browser: `test_no_focused_control_of_the_index_hides_under_its_sticky_strip` — Shift+Tab from the index's last control to the strip at 390 × 844 and 1440 × 900, no focused box meets the strip's; **checked to fail without the fix** (at 390, focused persona forms and links under the strip) |
| **a11y M1** — choosing the frame in «Altro» dropped the focus to `<body>` | The script gives the focus back to «Altro»'s summary when it closes the menu. | browser: `test_choosing_the_frame_from_altro_keeps_the_focus_on_altro` (1024 × 768, by keyboard) |

### The minors

**Applied:**
- **UX m1** — the table's plain words: «Versione in uso», «Ogni invio che cambierebbe dei dati viene fermato», «Ancora
  nessuna novità registrata.», «Nessuna superficie ha ancora passato il consiglio: per ora ogni pagina è «V4 +
  fondation».», «… soltanto quando il consiglio l’ha approvata», «Dopo l’invio, sull’accesso», «L’ingresso, dopo
  «Entrer»», «La scena dell’accesso, mentre si compila», «la porta del marchio, nella colonna di sinistra», «(il sito di
  oggi)», «Entrare qui non vi fa uscire di là, e viceversa.», «chiedono di accettare le condizioni», «riquadro vuoto»,
  «Apri a parte» (the full sentence is its tooltip), the 400's «una pagina in /fr/, /ar/, /it/, /en/ o /documents/».
  File paths moved into `title` attributes and the steward's fold. The plan's proper names kept verbatim.
- **UX m2** (wording) — the refusal: «Anteprima V5 — sola lettura. Questa azione non è stata eseguita, e nulla è
  cambiato: «‹persona›» resta uguale per chi guarda dopo. Per tornare alla pagina: «Indietro» del browser. Per uscire
  dalla persona: «Sortir», nella barra in alto.» — no method, no path, no «cantieri», no «?état=».
- **UX m3** — «Analyse territoriale — 403 per questa impresa: la pagina d’errore».
- **UX m4 / a11y m1** — the frame and the window are named after the page: «La home — V4 + fondation», «La home · V5 dal
  vivo · Italy Legal Entry™», served so and kept so by the script (the strip's data carries each page's title; the framed
  document's own title otherwise).
- **UX m5** — a muted «pagina:» inside the state chip. Below 48 rem the strip shows the mark alone (no «V5» beside it),
  so the contradiction cannot arise and the chip drops the prefix to keep the row.
- **UX m6 / a11y m9** — «dentro» in place of «Entrer» on the persona inside; the summary's hidden words « — dentro come ».
- **UX m7** — «apre il suo Tableau de bord» / «apre il suo Espace entreprise», in the strip's list and on the cards.
- **UX m8** — the languages stay on the row down to 64 rem; below 48 rem «Indice» is in «Altro» (two clicks): a
  loopback desktop tool, said here.
- **UX m9** — after the product's own «Se déconnecter» inside the frame, the landing is served again: the strip names
  nobody.
- **UX m10** — «(senza inviare)». **UX m11** — solved by M3's per-language forms.
- **Security m1** — a refused caller meets `HttpResponseNotFound` («Not Found», `text/plain`), never `Http404` (the DEBUG
  page named the view); every preview route is `csrf_exempt` so the gate answers before `CsrfViewMiddleware`, and the
  switch keeps `csrf_protect` inside, after the gate. The two tests now run with `Client(enforce_csrf_checks=True)` and
  assert that refused bodies name nothing of the preview. The docstrings say «a refused caller is never served the
  preview»; Django's own DEBUG 404 page for any other path still lists the mount.
- **Security m2** — the read-only refusal's log line writes the persona, the method and the path escaped
  (`unicode_escape`, 200 characters): `test_a_persona_cannot_forge_a_line_of_the_preview_s_log` (`%0a`, `%0d`: one
  record, no newline).
- **Security m3** — `page_param` refuses a dot segment or an empty one, as written and percent-decoded until stable
  (the URL standard reads `%2e%2e` as `..`): `/fr/../__design-v5/`, `/fr/%2e%2e/backoffice/`, `/fr/./`, `/ar/..%2f..%2fx`,
  `/fr//x/`, `/fr/%252e%252e/` → 400; «Sortir» with such a page → the home (`test_sortir_never_frames_a_dot_segment`).
- **Security m4** — the switch refuses an allow-listed account holding any group but `role:person` / `role:company`, or
  any permission of its own (`refused (privileged)`): **DL54-18**, stricter than §4.4's letter.
- **Security m5** — documented below (honest limits); the optional launch secret is not built.
- **a11y m2** — a menu closes when the keyboard leaves it (`focusout` with a related target outside); Escape moves the
  focus back to the summary only when the focus was inside the menu.
- **a11y m3** — under `forced-colors: active` the persona's dot and the states' dots keep `CanvasText`, and the current
  language or frame is underlined (`E/w1-p/fix-1/c2-final/16_forced_colours_company_inside_390.png`).
- **a11y m4** — the build and the state are `<span>` elements; the row has headroom (the tiers above); under the WCAG
  1.4.12 override the strip keeps one row of 40 px at every width, nothing outside the window
  (`E/w1-p/fix-1/widths-r3/strip_widths_spacing.json`, 136 rows, 0 bad) — the state's words shrink with an ellipsis
  where the override leaves no room (with «V4 + fondation», only at 375 px and less).
- **a11y m5** — a pressed «Desktop 1440» / «Telefono 390» releases its own frame (about:blank, then removed); within the
  one-pair cap.
- **a11y m6** — `lang="fr"` on the persona names, «Entrer», «Sortir», the persona pages' titles and «V4 + fondation» in
  the index; the language tooltips in Italian (`LANG_NAMES`: «Francese», «Arabo», «Italiano», «Inglese»).
- **a11y m7** — `.dp-hidden` words: «Stato della pagina nella cornice: » before the state, « — francese» after «fr» (and
  the others), « (nuova scheda)» inside every link that opens a new tab.
- **Performance P-1** — `ConnectionCeilingMiddleware` reads an announced body of a known length up to
  `DATA_UPLOAD_MAX_MEMORY_SIZE` before it takes a slot: `test_a_client_that_withholds_its_body_costs_a_thread_never_a_slot`
  (ceiling 2, three withheld bodies to the switch with its CSRF cookie: the landing 200 at once; nothing left behind).
  One behaviour changes, as the reviewer said: a POST without a CSRF cookie that withholds its body now waits for its
  body before its 403 — on a thread, never on a slot.
- **Performance P-2** — a frame of the index gets its address from one pending timer that an unload cancels (the next
  task when nothing was unloaded in the last 300 ms, 150 ms otherwise): ten addresses × pair opened back to back by
  script cost at most two frame documents (`test_the_index_never_holds_more_than_one_pair_of_frames`).
- Observation **performance O-1** — the virtual forum's row says «404 finché il forum virtuale è chiuso».

**Left, and why:**
- **UX m2, the HTML refusal** — «if security agrees, serve minimal HTML with a «Torna alla pagina» link built from a
  same-origin Referer». The security review did not rule on it, and its D1 accepted the refusal's framing because it is
  `text/plain` with nothing to click: the words changed, the format did not.
- **a11y m3, the optional under-bar** for the current item outside forced colours (the 1.30 : 1 tile) — the reviewer
  called it a design call; the current item keeps its weight and lighter text; forced colours underline it.
- **Security m5, the optional launch secret** — only needed if a preview port is ever forwarded; the limit is stated
  below instead.
- **a11y O2 (a skip link), O3 (the dev sheet's rings on W1-A's focus tokens)** — observations, not findings: the tokens
  do not exist yet, and the sheet's test requires every custom property it uses to be declared.
- **Security O2 (proof scripts share the origin with persona sessions)** and **O1 (NUL bytes → 500 in `cms`)** —
  observations; O1 is the known `cms` ticket, outside W1-P's slice.

### Captures — looked at, one by one

Lane 4, headless Chromium, profile `C:/tmp/ile_v5_council/.profiles/w1p-fix-1/` (emptied before the final series),
no password. Final series `E/w1-p/fix-1/c2-final/` (`look.json`): the landing; signed out, a reserved page → the sign-in
rendered in the frame (`02_…`), its empty submission rendered (`03_…`); the back-office refused → the stage's message
(`04_…`); the index (top, personas, states, full page); one click on «ar» of «Mes échéances» → `qa-doc-person` inside,
that page framed (`06_…`); the documents app in ar and fr (`07_…`); the persona menu with «dentro» (`08_…`); the
read-only refusal in the frame (`09_…`); the product's own sign-out → the home, the strip naming nobody (`10_…`); the
viewer's pair at 1440 and 1280 (`11_…`); «Superfici V5 · 4» at 1440 and in «Altro» at 1024 (`12_…`, a scratch status
file the lane server read through `ILE_DESIGN_PREVIEW_LIVE_STATUS`, removed after); the archive (`13_…`); 390 × 844 with
«Altro» (`14_…`); the index at 390 (`15_…`); forced colours with `qa-company` inside at 390 (`16_…`). In every step: the
strip 40 px, no horizontal overflow, **0 `securitypolicyviolation`**; the one CSP console line of the series is step 04's
own — the browser refusing the back-office, which is what that step shows. Width series: `E/w1-p/fix-1/widths-r1`
(before the tiers: 44 of 136 rows overflowed), `widths-r2`, `widths-r3` (with and without the 1.4.12 override: 0 of 136).

What looking found, and what was fixed before the commits: the first width series overflowed (the «pagina:» prefix at
390 and below; «Superfici V5» with a persona inside at 1280 and 1600) — the tiers above; a persona page's «ar» wrapped
alone under a long title — the languages of a page now wrap together.

### Tests and suites (lane 4, `test_ile_v5_l4`, lock-gated)

`tests/frontend/test_design_preview.py`: 147 test functions (130 before the round). New: the CSRF-enforced gate, the
privileged roles, the forged log line, the dot segments («Sortir»), the documents app's language, the census (two),
the persona forms, the one-click switch, the two-directive policy comparison, the withheld bodies, and six browser
tests (the redirect and the form's answer in the frame, the in-product sign-out, the refused frame, the viewer's pair,
the focus walk, the focus back on «Altro», the strip with 2/6/12 surfaces). The strip-paint test now warms the server
with one request first: the first request after a server starts pays Django's one-time costs, which belong to no page —
on this loaded machine they alone took the first measurement past the second (1092 ms) in run 1.

| Run | Result | Log |
|---|---|---|
| W1-P suites, run 1 — `test_design_preview` (browser included) + `tests/security` | 427 passed, 1 failed (the strip-paint test's first, cold measurement: 1092 ms; see above) | `E/w1-p/fix-1/s1_w1p_suites_r1.log` |
| W1-P suites, run 2 — on the committed code, + `test_check_ownership`, `test_dev_database_connection_lifetime`, `test_qa_password_comes_from_the_environment` | **480 passed, 0 skipped, 0 failed** (563 s) | `E/w1-p/fix-1/s2_w1p_suites_r2.log` |

ruff check and ruff format: clean on every Python file touched. Every file of the footprint is LF.

### For the steward

- **Surface keys are W1-0's census ids** now (the index's «Le chiavi delle superfici, per lo steward» lists them):
  `live_status.json`'s `surfaces` names page types, not rows — §3's example keys above read `home`, `login`,
  `dashboard-person`, `legal-document` … The file does not exist yet, so nothing has to be migrated.
- `ILE_DESIGN_PREVIEW_LIVE_STATUS` and `ILE_DESIGN_PREVIEW_CHANGELOG` may be set in a lane's environment to a scratch
  copy, so that a state is measured without touching the steward's files (dev.py's preview block).
- DL54-17 and DL54-18 are numbered on W1-P's branch: renumber them at the merge if another family's entries land first.

### Honest limits (added)

- **Raw port-forwards and header-less proxies** (security m5): the gate trusts a loopback `REMOTE_ADDR`, the absence of
  a proxy header and the `Host`, and the client chooses its `Host`. A raw TCP forward (`ssh -L/-R`, `netsh interface
  portproxy`, `socat`) or a reverse proxy that adds no header (nginx's bare `proxy_pass` sends `Host: $proxy_host`) cannot
  be told from the owner's browser: a non-browser client behind one could mint a read-only persona session over
  synthetic QA data. **Never forward a preview port; never put a proxy in front of a dev server.** Should a forward ever
  be needed, a per-process launch secret (a random token written at start-up under `C:/tmp/ile_v5_council/.work/`,
  presented once as a cookie before `accedi/` answers) is the hardening — not built.
- The census in the test is a copy; its comparison with the file runs only where the evidence folder is on disk.
- A detail page other than the census's example is matched by the pattern of its address; a page type the census does
  not hold (a living sheet, a news article — none published on the clones) reads «V4 + fondation» until it is added.
- The state's words shrink with an ellipsis in the cramped cases above; the full words stay in the chip's tooltip and in
  its accessible name.
- The build is shown on the strip from 100 rem (1600 px); at the owner's 1440 it is one click away in «Novità».
- The read-only refusal is still plain text in the browser's default face (UX m2's HTML variant is left).
- Chromium on Windows only, headless; no WebKit, no Firefox, no real phone, no screen reader.
