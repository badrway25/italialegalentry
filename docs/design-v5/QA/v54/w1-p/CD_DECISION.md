# W1-P · Preview as the live product — the Creative Director's decision

Italy Legal Entry™ design V5 · V5.4 «EXECUTION MODE» · 5 October 2026, 13:40–14:30 · Executive Creative Director, label
`w1p-cd`, with the UX lead's evidence. I built nothing in this family and reviewed nothing in it before this sitting.

- **Branch:** `v54-w1-p` at `8f12192` (`v54/base` = `f11d131`; 12 commits, 33 files). Plan
  `docs/design-v5/V5_4_EXECUTION_PLAN.md` §4 (4.1–4.6), §3.3 item 3, §2.2, §2.7; DL54-01, DL54-17, DL54-18.
- **Read:** the four re-checks of round 2 — `ux_r2.md` (the council lead), `security_r2.md`, `a11y_r2.md`,
  `performance_r2.md` — against their round-1 baselines, and `IMPLEMENTATION_NOTES.md` (both rounds).
- **Seen and measured myself:**
  - **Server:** my own, `127.0.0.1:8785`, from `C:/tmp/ile_wt/v54-w1-p` at `8f12192`, on `ile_v5_l4` (read-only use).
    Environment: `ILE_DESIGN_PREVIEW=1`, `ILE_DESIGN_PREVIEW_PORT=8785`, `ILE_REFERENCE_DATE=2026-10-03`,
    `DB_CONN_MAX_AGE=0`, `PGAPPNAME=ile-lane-4-cd`, `--noreload`.
  - **Browser:** headless Chromium (Playwright 1.63), profile `C:/tmp/ile_v5_council/.profiles/w1p-cd/`. Every series
    and the suite run were lock-gated; they waited 455 s, 50 s and 620 s.
  - **Never touched:** 8780, 8770–8772, 8782, the engineer's 8784, Chrome 9222/9223.
  - **No password** was used, typed or stored. Writes on `ile_v5_l4`: three persona sign-ins and their three
    sign-outs. Five write attempts as a persona were refused before any view.
- **Evidence:** `C:/tmp/ile_v5_council/evidence/v54/w1-p/cd/` (index in §7).

## Decision: **PASSES_WITH_CONDITIONS**

`/__design-v5/` does what the owner asked for in V5.4. It opens on the live product: the real home, full window, in one
frame, under a quiet 40 px bar. The index is one click away, and the old catalogue sits in an archive that says what it
is. Every authenticated page is two clicks away, without a password, read-only.

- **Plan §4.6 is met, item by item** (§1). The one item left is the steward's and the orchestrator's, after the merge:
  v5-live at the tag and 8780 restarted.
- **The council is clear.** All four lenses re-checked the fixes: 0 blocking, 0 major. Round 1 had 2 blocking and 9
  major.
- **My own captures and probes agree with them** (§1, §2).

It does not pass clean: nine conditions, all minor, all inside W1-P's slice, each a few lines with its test. Four of them
are things the owner would meet on 8780:
- the index promises a loader that does not exist yet;
- its «404» shows Django's technical page;
- its two sign-in states show the dashboard while a persona is inside;
- the product's own way in ends on a password form, with nothing pointing to «Personas».

The other five keep the security reviewer's contract, keep the code honest with its comments, and finish the names and
words the owner and assistive technology read.

**The merge rule:**
- **C1–C9 land before the merge,** in one fix pass on the branch.
- **The steward verifies them at the merge,** with no new council sitting (UX: «I don't need to see this again»;
  security: «No further review round is needed»). The steward checks three things:
  - the named tests exist and pass in the W1-P suites, with 0 skipped;
  - the fix pass's width series shows 0 bad rows;
  - one look at the index's «Stati senza credenziali» and «Le pagine d'errore».
- **A condition the fix pass cannot meet as written comes back to the CD,** with its reason in the notes. It is never
  dropped silently.
- **The follow-ups F1–F6 (§5) are not conditions of this merge.** The steward schedules them before the first report to
  the owner (plan §6), when the owner starts to use the preview to judge a flagship.

---

## 1. Plan §4.6, item by item

| §4.6 item | Verdict | The council's evidence | My own check at `8f12192` |
|---|---|---|---|
| absent without the flag (404) | **PASS** | security t1: prod, staging, test and dev-without-DEBUG refuse it under a hostile environment (5 passed); the engineer's tests | in my suite run (below) |
| 404 off loopback, with a proxy header, or with a foreign `Host` | **PASS** | security: 4,704 refused requests (16 routes × 42 callers × 7 methods), plain `404 Not Found`, naming nothing | `X-Forwarded-For` set, `Forwarded` empty, `Host: 127.0.0.1:8780` → 404 «Not Found»; `localhost:8785` → 200. A NUL byte is the pre-existing site-wide edge (S1) |
| 405 on GET for `accedi` / `esci` | **PASS** | security: GET, HEAD and OPTIONS → 405 `Allow: POST` | GET `accedi/qa-doc-person/` and `esci/` → 405 `Allow: POST`; POST without the token → 403 |
| staff, unknown accounts and a database outside the allow-list refused, `ile_qa` included | **PASS** | security t3: `ile_qa`, `ile` and five more refused before any query (8 passed); the privileged roles of DL54-18 | an unknown persona → 404. Code read: `V4_CONTROL_DATABASES = {"ile", "ile_qa"}`, refused even if a setting names them |
| distinct session, CSRF and language cookie names | **PASS** | security: only `ile_v5_*` names set | «Entrer» sets `ile_v5_sessionid`. Every cookie set in my runs has an `ile_v5_*` name (`ile_v5_csrftoken`, `ile_v5_sessionid`, `ile_v5_language`); none has a V4 name |
| persona sessions read-only: 403 on unsafe methods outside the preview, the allow-list excepted | **PASS** | security: 34 write attempts refused before any view; sign-out and the language switch keep their CSRF check | as `qa-doc-person`: POST `/fr/contact/` and DELETE → 403 «Anteprima V5 — sola lettura.»; «Sortir» → 302, and the dashboard then sends to the sign-in |
| the log line carries no e-mail | **PASS** (C6 closes the ceiling's line) | security: the persona line escaped against LF, CR, U+2028, NEL, ESC; **m7**: the ceiling's 503 line still writes the path raw | 11 `ile.designpreview` lines in my server's log, each with the persona key. 0 «@» in the whole log |
| frames load real pages only under the narrow condition | **PASS** (C5 closes the method gap) | security: 47 header cases and 8 framing attacks from other origins; performance: 400 of 400 frame documents relaxed, nothing else; **m6**: the read-only refusal is relaxed whatever the method | `/fr/` framed by this origin → `SAMEORIGIN`, `frame-ancestors 'self'`, no `upgrade-insecure-requests`. Top-level, cross-site, proxy header, back-office → `DENY`, `'none'`. Persona POST framed → relaxed (DL54-17). **m6 reproduced:** persona PUT framed → relaxed too |
| at most one frame pair at a time, enforced by the hub's script | **PASS** (C7) | performance: ten addresses × pair → exactly 2 frame documents, 0 broken pipes; UX and accessibility by pointer and keyboard; **P-4**: every first open waits 150 ms, against the code's own comment | my count in the viewer: 1 → 2 → 1 (another address unloads the pair) → 2 after thirty scripted clicks → 0 after Escape. The pair is side by side at 1440 (`23_…`) |
| the strip paints in ≤ 1 s, and the landing loads exactly one frame | **PASS** | performance: FCP warm 68 ms, cold 128–176 ms, cold at CPU ×4 412 ms (max 652); one frame, 0 nested | landing FCP **36–652 ms** (652 ms on the first request after an idle server, 36–164 ms after). **15 of 15** landing loads hold exactly one frame and 0 nested frames. The strip is 40 px at every capture, with 0 horizontal overflow |
| 0 CSP violations | **PASS** | 0 in every lens's series. The only violation anyone met is Django's default CSRF failure page (S2), product-wide | **0** `securitypolicyviolation` events over 21 steps, in the top document and every frame: signed out, the persona's pages, ar, the sign-in in the frame, the 404. The only console errors are my deliberate 403 probe and the 404 page |
| the research archive's tests keep passing at their new paths | **PASS** | the engineer's 480 passed; security 428; accessibility 15 browser tests | **W1-P suites: 428 passed, 0 skipped, 0 failed in 448 s** (`test_design_preview` with its browser tests, and `tests/security`), on `test_ile_v5_l9`. `/hero/`, `/type/?system=b`, `/compare/` and `/proof/index.html` → 302 to `research/…`, query kept |
| v5-live is checked out at the tag, and the orchestrator restarts 8780 after the merge | **PENDING — after the merge** | — | The steward checks the tag out: `git -C C:/tmp/ile_wt/v5-live checkout --detach v54/w1-p`. The orchestrator restarts 8780 with the unchanged command of `evidence/v54/SERVERS.md`; `ILE_DESIGN_PREVIEW_PORT` defaults to 8780. The steward's `live_status.json` and `CHANGELOG_V54.md` must be committed before the tag, because 8780 reads them from the checkout it serves |

**The rest of §4, at a glance:**
- **§4.1:**
  - the strip carries every element the plan lists — the tag, commit and date and the changelog in «Novità» at 1440;
  - «Superfici V5» is drawn only once a surface has passed;
  - the index has the public pages, the four persona cards with no staff persona, the family board, the specimen boards
    and the comparison on 8771.
- **§4.2:** the archive holds the hub as it was, keeps its «non approvato» tags, and redirects the old addresses.
- **§4.3:** the pickers, the banners, the proof frames and the «Baseline V4 (controllo)» group have left the main path.
- **§4.4:** hardened as written, and stricter where DL54-18 and DL54-19 say.
- **§4.5:** the entry points are there. The behaviours belong to W1-D and W2-B, and the index must say so (C2).

**Branch hygiene:**
- `scripts/check_ownership.py w1-p v54/base` → 30 inside, 3 slice → PASS. The three slices:
  - `dev.py`: the diff stays inside the preview block;
  - `test_log_privacy.py`: one new function, no existing line changed;
  - DL54: entries appended.
- `regen_design_inventory.py` (check mode) → «current». W1-P changes no inventoried figure.
- `static/css/dev/` and `static/js/dev/` are not build entries, so `dist/` does not change.

## 2. What I saw

I looked at every capture (§7). As the owner will meet it:

- **The landing — fr and ar, 1440 and 390, and the phone frame at 1440.**
  - Nothing stands between the owner and the page but a dark 40 px bar outside it. It names the product, says
    «pagina: V4 + fondation», and holds the languages, the frame, «Personas», «Novità», «Indice» and «Apri a parte».
  - At 390 it keeps its row: the mark, the state, «Personas», «Altro».
  - The frame holds the real `/fr/` (`lang="fr"`, ltr) or `/ar/` (`lang="ar"`, rtl), and the page never knows the bar
    is there.
  - It is quiet, it does not compete with the door stage, and it reads as a tool, not as a second navbar. That is the
    right register for it.
- **«Personas» → «Entrer» → «Tableau de bord»** (`qa-doc-person`, `EE167596D4`), fr and ar, 1440 and 390.
  - The console renders whole in the frame, with its rail mirrored in ar.
  - The bar says who is inside («Personas ● Personne avec dos…»).
  - «Sortir» returns to the public home with nobody inside.
  - From the index, «ar» of «Mes échéances» opens that page as that persona in one click: two from the landing.
- **The index.**
  - A complete, sober map: 41 public page types and the four persona cards, each listing its pages in fr and ar.
  - It is long by necessity.
  - The one visual noise is the «● V4 + fondation» chip repeated on all 41 rows under a fold that already says it. Some
    chips wrap under their titles (C9).
- **The viewer.** The desktop frame and the phone frame stand side by side at 1440, the desktop scaled to fit. The phone
  runs 10 px past the window (F3).
- **The archive.** «Archivio della ricerca», an archival lead, the historical notice, the old notes kept as written. It is
  clearly secondary.
- **Where it falls short — the owner would see these:**
  - **«La 404»:** the frame shows Django's yellow technical page. It is in English and lists the URL patterns, under a
    strip that calls it «La pagina 404» (`21_…`) — C1.
  - **«Stati senza credenziali»:** the index says «la chiave gira una volta e si ferma», «accende la porta del marchio»
    and «la scena risponde a ogni passo». None of it is built yet: no `static/js/src/loader.js`, no
    `templates/components/loader.html`, no `user_logged_in` receiver in `apps/accounts/signals.py` — C2. V5.4 shows
    the owner the working result, never a promise worded as a fact.
  - **Signed out:** the product's own «Espace réservé» ends on the real password form (`22_…`), and nothing points to
    «Personas» — C4.

## 3. The deviations from the plan's letter — ratified

- **DL54-17 — a form's answer framed under the narrow condition; framed pages and the landing drop
  `upgrade-insecure-requests`. Ratified.**
  - UX measured the failure it cures: a blank frame in every natural flow — the sign-in, its error, the product's own
    sign-out, every public form. Without the change, §4.6's «0 CSP violations» fails.
  - The security reviewer endorsed it: the condition is the GET condition, the global policy is untouched, and the
    read-only rule comes first.
  - Its wording is accurate once C5 puts the method in the one predicate.
- **DL54-18 — no privileged persona. Ratified.** It is stricter than §4.4's letter, and it is how this codebase grants
  privileges (groups, not `is_staff`).
- **The implementation notes' build decisions (§6, items 1 and 3–8). Ratified and recorded as DL54-19:**
  - Italian working strings, with the plan's proper names verbatim;
  - one gate for every route, with sixteen proxy headers, and `ile` refused beside `ile_qa`;
  - the states the product's DEBUG routes cannot show in its own words live in the app;
  - the CD decisions served as text;
  - the preview's documents follow `main.css`'s font and token layers;
  - the steward's two files live in `docs/design-v5/`.

## 4. Conditions before the merge (C1–C9)

All minor, all inside W1-P's slice. The fix pass must also:
- **re-measure the strip's width series:** 17 widths × signed out and `qa-person` × 0, 2, 6 and 12 surfaces, with and
  without the 1.4.12 override, 0 bad rows;
- **re-run the W1-P suites:** 0 failed, 0 skipped;
- **re-capture and look at** the landing, the index, the archive and one persona page, fr and ar, 1440 and 390;
- **append «Review fixes — round 2»** to the notes.

| # | Source | What must hold | The test that holds it |
|---|---|---|---|
| **C1** | UX r2 n1 | «La 404» and the closed virtual forum show the product's 404, not Django's technical page. Add «404» to `views.STATES` and render `core.views.error_404` under `translation.override(lang)`, as the 429 is rendered. The index links «La 404» to `stati/404/?lang=fr` and `?lang=ar`. The forum row says what it shows | the index's 404 links answer 404 with `errors/404.html`, in fr and in ar |
| **C2** | UX r2 n4 | The three states that need W1-D or W2-B say so: «— in arrivo con W1-D (il caricatore «Lume»): oggi la pagina non lo mostra ancora», and likewise «W1-D + W2-B» and «W2-B». The note goes once that family is `"v5"` in `live_status.json`. The index never words a promise as a fact | without the file, the three items say «in arrivo»; with the family at `"v5"`, the note goes |
| **C3** | UX r2 n3 | While a persona is inside, the two sign-in states («Dopo l'invio, sull'accesso», «La scena dell'accesso») are a small POST to `esci/` with `page=/fr/compte/login/`, labelled «Esci dalla persona e apri l'accesso». Signed out, they stay links | as a persona, the two items are forms to `esci/` with that page; signed out, links |
| **C4** | UX r2 n2 | When the framed page is the sign-in and nobody is inside, one muted line beside the state reads «Per entrare senza password: «Personas»». Draw it in `live.strip()` and in `follow()`. Each «Entrer» form carries the sign-in's `next` as `page`; `_next` honours it only when it is that persona's own page | signed out, `?page=/fr/espace-reserve/mes-echeances/` shows the line, and «Entrer» as `qa-doc-person` lands on «Mes échéances» |
| **C5** | security r2 m6 | The method belongs to the one predicate: `frames.framed_by_this_origin` starts with `request.method in FRAMED_METHODS`. `PreviewFrameMiddleware` relaxes on that predicate alone, and `personas.refusal()` inherits it | extend `test_a_frame_of_this_origin_may_show_the_refusal_and_nothing_else_may`: a persona's framed PUT, PATCH and DELETE → `DENY` and `'none'`; POST → `SAMEORIGIN` and `'self'` |
| **C6** | security r2 m7 | Every line the preview logs escapes what a request chose. One helper, e.g. `designpreview.access.loggable()`, used by the read-only line and by `ConnectionCeilingMiddleware.busy()`, which logs `loggable(request.path)` | `busy()` on a path holding `%0a` and `%0d` → exactly one `ile.designpreview` record, with no `\n` and no `\r` |
| **C7** | performance r2 P-4 | Either `unload()` stamps `lastUnload` only when a frame was really removed — measured: a first open drops from 169 ms to 24 ms, the bursts stay bounded — or the comment, the part-3 header and the notes stop promising «a person's click is not delayed». The CD prefers the fix | after the first click, the desktop frame gets its `src` less than 100 ms after the click's `timeStamp` (or, if the words are corrected, the test asserts what the words say) |
| **C8** | accessibility r2 n1, n2, n3, n4, m6′ | The names and states the owner and assistive technology read: (a) the home link keeps «Italy Legal Entry™ — V5» from 48 to 90 rem, the words visually hidden, not `display: none`; (b) «1:1» named «1:1 — misura vera della cornice desktop», disabled while there is no desktop frame; (c) under forced colours the pressed toggles draw `Highlight` / `HighlightText`; (d) «Superfici V5: n pagine»; (e) `lang="fr"` on «V4 + fondation» in the rows, the family chips, the strip's state and `follow()` | at 1024 × 768 the strip has a link named «Italy Legal Entry™ — V5»; «1:1» is disabled without a desktop frame; the template tests for (d) and (e) |
| **C9** | UX r2 n8, n9 | The index's words: «1 famiglia» and «1 pagina pubblica» (`pluralize`); dates printed «5 ottobre 2026», with the ISO value in `datetime`; inside the «V4 + fondation» fold, a row prints its chip only when its state is `"v5"`. Also `.dp-index__text code { overflow-wrap: anywhere; }` (a11y O8) | the plural and the date in a template test; no `dp-state` chip on a V4 row inside the fold |

## 5. Follow-ups after the merge, and the steward's items

**W1-P follow-ups (F1–F6):** minor, not conditions of this merge, due before the first report to the owner (plan §6).
Each is in the preview's own files; the steward assigns the writer.

| # | Source | What |
|---|---|---|
| **F1** | UX n5, a11y n5 | Tier the strip by what the row holds, not by the worst case, so that the build shows at the owner's 1440: 404 px stand empty there today. The build yields before the state (`flex-shrink`), so «V5 — council-passed» is never cut under the 1.4.12 override. Then re-measure the width series with «V5 — council-passed» in the frame |
| **F2** | UX n6 | The read-only refusal shown in the stage's message box, with «Torna alla pagina di prima». The response stays `text/plain`, as the security review accepted |
| **F3** | UX n7 | The viewer's phone frame scaled to the window's height: `min(1, available / 846)` |
| **F4** | UX n10 | «V5 dal vivo» on the index returns to the page the owner left (`?da=`) |
| **F5** | performance P-3 | A multipart body announced above `DATA_UPLOAD_MAX_MEMORY_SIZE` and withheld still takes a slot: parse it before the slot, as the reviewer wrote, with the test beside the existing withheld-body test |
| **F6** | performance O-5 | The index's weight (176 KB, 102 forms): one form per persona card, with `<button name="page" value="…">` per page. Roughly −40 KB and several hundred elements. The index's UX is unchanged |

**For the steward, outside W1-P's slice:**
- **S1 (security O1): a NUL byte in any path turns the answer into Django's DEBUG technical 500.** Pre-existing and
  site-wide; it shows `DATABASE_URL` with the development password.
  - `cms.middleware.LegacyURLMiddleware.lookup_redirect` queries with the NUL. The fix belongs to its owner: no lookup
    for a path holding `\x00`, or catch `DataError`.
  - Optionally, a dev exception-reporter filter that also hides `URL|DSN|DATABASE`.
  - It is the «%00 → 500» ticket already known. It is loopback-only, and it exists on every DEBUG server, the V4
    control included.
- **S2 (security O9): Django's default CSRF failure page carries an inline `<style>`,** which `style-src 'self'`
  refuses everywhere. A project `403_csrf.html` without inline style would make it CSP-clean.
- **S3 (performance O-7):** three persona sessions left open on `ile_v5_l4` by an earlier run. They are harmless and
  expire in 8 h. Clear them if the lane is reused.

## 6. What this decision does not cover

- **The bar and the index are scored against §4.6, not against the six scales of §3.1.** W1-P is a development tool, and
  its gate is §4.6 (§3.3 item 3). No surface of the product changes in this family. Every page in the frame is V4 until a
  V5 family merges, and the strip says «V4 + fondation» for all of them.
- **Browsers:** Chromium only, headless, on Windows. No WebKit, no Firefox, no real phone, no screen reader. The
  reviewers are under the same limit.
- **Suites:** I ran the W1-P suites (§2.7), not the full suite. The steward runs everything at the merge. The 27 failures
  and 2 browser skips of `v54/base` are the clock's, not W1-P's. design-v5 holds no clock-fix commit yet, so nothing was
  merged into the branch.

## 7. Evidence (E/ = `C:/tmp/ile_v5_council/evidence/v54/w1-p/cd/`)

- **The captures** (`cd_capture.json` holds every measure):
  - `01`–`05`: the landing, fr and ar, 1440 and 390, and the phone frame;
  - `06`–`09`: the index and the archive, 1440 and 390, with full-page captures;
  - `11`: «Personas»;
  - `12`–`15`: the persona's «Tableau de bord», fr and ar, 1440 and 390;
  - `16`: the index with the persona inside;
  - `18`: after «Sortir»;
  - `20`: the index's one-click «ar» of «Mes échéances»;
  - `21`: «La 404» today;
  - `22`: a reserved page, signed out;
  - `23`: the viewer's pair;
  - `24`: «Altro» at 390.
- **The guards and the frame policy:** `cd_probes.json`.
- **The frame cap:** `cd_framecap.json`.
- **The W1-P suites:** `s1_w1p_suites_cd.log`.
- **My server's log:** `srv8785_w1p_cd.log`.
- **The scripts:** `scripts/` (`cd_capture.py`, `cd_probes.py`, `cd_framecap.py`).
