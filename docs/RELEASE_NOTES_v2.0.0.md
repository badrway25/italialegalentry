# Italy Legal Entry™ v2.0.0 — release notes

> **Draft of 16 October 2026** (W4-D, part 1 — release engineering, corrected the same day after its review), written
> from `design-v5` at `0a8351b` for the owner and for whoever deploys; **completed on 27 October 2026** (W4-D, part 2 —
> integration readiness) with F-8, W4-A, W4-B and W4-C as merged, part 2's fixes and the weights after it. The
> release-candidate validation completes the rest: the *Release gates* table (§7) and the final test counts and
> weights. **Validated on 28 October 2026**: the release-candidate validation ran on 27–28 October, its two failures
> were fixed (§2, *Release-candidate fixes*) and §7 records every gate's result. Nothing here is a secret, and no server
> is named.

## 1. What v2.0.0 is

**The release.** `v2.0.0` is the version the platform already declares — the footer's label «v2.0.0 — Fase 1»
(`ILE_VERSION_LABEL`, `SiteSettings.version_label`). Following the owner's directive V5.10 (16 October 2026), once the
release gates pass on one commit: GitHub's `main` at `a3ac318` is preserved by the tag **`pre-v5-main-2026-10`**,
`main` is fast-forwarded to the validated `design-v5` release snapshot, and that commit receives the annotated tag
**`v2.0.0`** — the only release tag. The server checks out that tag; the handoff gives its commit SHA
(`docs/deployment/PRODUCTION_DEPLOYMENT_RUNBOOK.md`, *RELEASE TAGS* and *States*).

**The product.** v2.0.0 is the V5 redesign of the whole platform — every public page, every page of the reserved area,
the sign-in and the entrance pages — on the same Django 5.2 LTS back end, with the same rules, gates, locked texts and
data model: **no migration was added** since the pre-V5 platform (the 39 migration files are identical,
`docs/deployment/ROLLBACK.md` §7). The 75 page surfaces the programme tracks are all in V5
(`docs/design-v5/live_status.json`).

| Family | What it shipped | Merged |
|---|---|---|
| W1-A — foundation | one type voice (Host Grotesk; the wordmark in ILE Wordmark, references in ILE Mono, Arabic in Vazirmatn), the V5 tokens and colour register, the corners, one focus ring | 9 Oct |
| W1-B — icons | one sprite drawn by one hand and a registry that gives each concept its own sign (110 symbols; person ≠ company ≠ institution ≠ university) | 9 Oct |
| W1-D — motion and the loader «Lume» | the brand's key turning once at every form submission (no wait lasts for ever: the form comes back after 10 s); reduced motion as a state | 9 Oct |
| W2-C1, W2-C2 — the navigation «Il portico» | the institutional bar with the four languages, the header with the four doors and their panels; the phone and tablet sheet on the overlay system | 9 and 12 Oct |
| W2-D — the hero and the home | the definitive hero (the path from Morocco to the door, the four entrances readable at rest, the phones' own first screen) and the home's chapters around it (W2-E folded in) | 10 Oct |
| W1-C — core components | flat buttons, the «lastra» fields, state pills with one producer, cards by function, notices, tabs and disclosures | 11 Oct |
| W2-B — the sign-in «Il varco» | the sign-in and every entrance page (sign-up, password reset, e-mail verification, second factor, «too many requests») | 11 Oct |
| W3-A — the console «Tre livelli» | the reserved area's chrome: the night rail in three levels, the current page lit, one rail per space | 11 Oct |
| W3-B — dashboards | the person's, the company's and the organisations' bridge; the NowPanel — the one raised surface with the one primary action | 11 Oct |
| W2-A — overlays | one overlay system on native elements: the console's drawer, the account popover, the rows' menus, the phones' bottom sheets | 12 Oct |
| W3-F1 — doors, project pages, orientation | the four doors, the Forum and its registration, the project, the pilot project, AGAMI, the network, contact, anti-fraud, the pathways, the questionnaire | 12 Oct |
| W3-F2 — content, legal, error and account pages | FAQ, glossary, partners, news, «Vivre en Italie», the legal pages, the error pages, the account pages | 12 Oct |
| W3-C — documents | «Mes pièces»: the register by who must act, one piece per row, the piece's page, the upload, the Conditions gate | 12 Oct |
| W3-D — the journey «La soglia» | one drawing of the public passage and one of the console's rail, between «Maroc» and «Italie» | 15 Oct |
| W3-E — the case file and the console's other pages | requests, communications, deadlines, files, pre-assessments, «Mon parcours», «Ma situation»; the company beyond its dashboard; the Academy; the help desk; the selection; the Forum's governance; the case file | 16 Oct |
| W4-B — motion audit | the Motion library removed (see §3); every animation through one gate; a still page under reduced motion; nothing animated from the keyboard | 16 Oct |
| W4-A — mobile and RTL | every page on a phone and in Arabic: 106 page states × fr, ar × eight phone viewports and 320 px; twenty-two defects, twenty-one fixed where they live (one major: a phone number laid out right to left); the phone's chrome within 120 px, no page wider than the phone, every isolated target 44 × 44 under a finger and 24 under a mouse; in Arabic the company's phone and e-mail left to right and a name in the other direction kept on the page's reading edge | 17 Oct |
| W4-C — performance and accessibility | the production-like measures of every page type and a WCAG 2.2 AA sweep (§6), `docs/design-v5/QA/v54/w4-c/` | 27 Oct |
| W4-D — integration readiness | the release engineering (CI, the deployment documents, the go-live phase, these notes — part 1), then the fixes of §2 and the last legacy layers of §3 (part 2) | 16 Oct (part 1) |

The design preview of the programme (`/__design-v5/`, W1-P) is a development tool: it exists only with DEBUG on and
`ILE_DESIGN_PREVIEW=1`, never under the production settings (checklist A-8).

## 2. Security and robustness

- **F-5 — the back office's second factor** (fixed, 15 October 2026): Django's own admin sign-in signs no one in and
  sends staff to allauth's sign-in, which asks the code; an account that holds a second factor presents it in every
  session before the back office, the reserved area, a private document or the pages that manage the factor
  (`docs/design-v5/QA/v54/sec-f5/NOTES.md`; checklist A-13).
- **F-7 — who may move a case file** (fixed, 16 October 2026): the lifecycle's «Chi può» column
  (`CASE_LIFECYCLE.md` §4) is data beside the graph and enforced by the domain on the file's locked row; a person can
  no longer move their own file into operator states; nobody's access was widened; a person whose latest file is
  suspended or closed is told so on the dashboard (`docs/design-v5/QA/v54/sec-f7/NOTES.md`).
- **F-8 — the back office's object permissions** (fixed, 16 October 2026; `docs/design-v5/QA/v54/sec-f8/NOTES.md`):
  the back office grants no more than the platform — every screen with personal or case data asks the model
  permission, the platform policy's roles, the domain's readable rows and the object policy —, so an operator reads in
  the back office only the case files it holds a live assignment on, and every other screen with personal data
  (documents, the help desk, public submissions, the Virtual Forum, the Forum's governance, notifications and mail,
  consents, the audit trail, orientation, integrations, the legal rules' workflow) follows its platform policy. A
  CLOSED file is read-only for everybody; a checklist line's status changes through the domain, with its audit event;
  a view-only grant never writes; a hidden field is no filter, and no account list is offered to a role that may not
  read accounts. A staff privilege on a public page (moderation, previews of unpublished content) meets the second
  factor. The integrations API answers NUL bytes and other unexpected input with a controlled 4xx, never a 500.
  Nobody's access was widened. The owner's questions are in §5.
- **W4-D part 2 — four defects fixed** (27 October 2026; `docs/design-v5/QA/v54/w4-d/NOTES.md`, «Part 2»):
  - *The pre-assessment lost its pathway's sources.* The questionnaire's assessment read the pathway's recorded
    sources through fields the model does not have, and a guard that only logged hid the error on every assessment: an
    outcome founded on rules in force now cites, after the rules' own sources, the pathway's primary sources (title,
    link and consultation date, the publisher kept in the record — never the editor's internal note), on the first
    assessment and on every reassessment. An outcome with no rule in force still cites no source, as its page says.
  - *The Virtual Forum and the newsletter* opened on their own flags before the legal pages were published, although
    the phase console declares that dependency; both now also require the legal pages (GO_LIVE_PHASE F-3).
  - *The sign-in invited to a closed sign-up*: the invitation is no longer drawn while the sign-up is closed (gate G2),
    and returns with it (F-4).
  - *A CLOSED case file accepted a new assignment* — a grant to read a file nobody may work on any more: the domain and
    the back office's form now refuse it (CASE_LIFECYCLE §4 rule 5 — F-8's Q-8, answered by the rule; reversible if the
    owner decides otherwise). Ending an assignment on a closed file stays possible.
- **Release-candidate fixes** (28 October 2026; `docs/design-v5/QA/v54/rc-fix/NOTES.md`, DL54-162): the validation
  found two gate failures and both are fixed. *Pillow* 12.3.0 → **13.0.0**: `pip-audit` reported 38 known advisories
  against the pinned image library (decoder overflows, decompression-bomb bypasses), all fixed in 13.0.0; reach was
  limited (a person's upload reaches Pillow only as JPEG or PNG, the CMS images only from staff behind the second
  factor), the pin moved anyway, and `pip-audit` on `requirements/constraints.txt` now reports none. *A stale test*: an
  icon test still allowed a rule part 2 had deleted. With them: a document whose stored file is missing answers 404
  after the permission checks — never a 500 — and is logged by its id only; a refused account gets the same 403
  whether or not the file exists.
- **The NUL-byte guard** (16 October 2026): a NUL byte in the query string, a form field or the session cookie is
  answered with the project's 400 page — with the security headers of every page — instead of a 500 with a traceback;
  behind nginx a NUL in the path gets nginx's own 400 (`cms.middleware.NulByteMiddleware`; checklist A-21, D-10).
- **Release hardening.** The production settings refuse to start on a weakened configuration — missing mandatory
  variables, a wildcard host, a short or published salt, a mail backend that does not deliver, an unfilled placeholder,
  private documents inside a served directory (`config/settings/prod.py`, checks `core.E001`, `core.W001`–`W003`);
  `/healthz/` checks the database; private documents leave only through the authorised download view, never through
  a web-server alias; the 400 and 500 pages are drawn without the request; every static file a page loads — the ES
  modules' imports included — is a hashed, immutable name, a plain name revalidated after 60 seconds; the server
  installs the dependency closure pinned in `requirements/constraints.txt`.
- **CI** runs every push twice on Ubuntu 24.04: Python 3.12 with PostgreSQL 16 — the server's major versions — and
  Python 3.13 with PostgreSQL 17 — the development stack —, each with the pinned closure (`.github/workflows/ci.yml`).
  The browser suite (Chromium) runs locally.
- **Integration checkpoint 3** (16 October 2026, the full suite on `design-v5`: 5 108 non-browser and 519 Chromium tests
  passed) fixed at their root a console drawer that lost its focus trap when reopened within one frame, a
  double-submission guard that could stay on for ever without the loader, and an overlay frame request outside the
  motion gate.

## 3. Weights, before → after

Gzip bytes. **Before**: the V4 platform as V5 found it — the W1-0 baseline of 5 October 2026, measured on the wire in
the capture loads (Resource Timing). **After**: `design-v5` at `0a8351b`, after W4-B — the steward's measure at the
W4-B merge (DL54-154: the bundles rebuilt from a clean tree, `gzip.compress(data, 9)`, each page type with the sheets
and scripts its templates load). Two methods of one quantity: compare the orders of magnitude, not single bytes.

**After W4-A and W4-D's part 2** (the same measure, 27 October 2026): W4-A's sweep and part 2's deletions — the
entrances' rules no template drew, four legacy names read by nothing, a guard for a class that no longer exists —
took `main.css` from 31 799 to **31 244 B** on every page, the console's page types from 39 978 to **39 405 B**, the
sign-in to **36 105 B** and the home to **45 591 B**; every other row is lighter by at least `main.css`'s 555 B. W4-C's
merge left the shared sheets as they were (`documents.css` 2 B lighter) and changed one script: the console's shared
chunk, 3 702 → 3 751 B (the Dépôt never silent when its module is late). These are the final figures: the release-candidate
fixes changed no sheet and no script.

| CSS | Before (V4) | After (V5) | Change |
|---|---|---|---|
| `main.css` — every page | 36 294 | 31 799 | −4 495 (−12 %) |
| an interior page with no sheet of its own | 36 294 | 31 799 | −4 495 |
| the doors | 36 294 | 35 226 | −1 068 |
| the sign-in | 37 502 | 36 660 | −842 |
| a console page (the dashboard) | 41 668 | 39 978 | −1 690 |
| the home | 39 114 | 46 160 | +7 046 (the V5 hero's own sheet) |
| the case file (where it draws its dialogs) | 41 668 | 46 229 (48 289) | +4 561 |
| «Mes pièces» and the documents' registers (with their panels) | 42 839 | 47 535 | +4 696 |

| JavaScript | Before (V4) | After (V5) | Change |
|---|---|---|---|
| the home | 36 892 · 8 requests | 24 138 · 7 requests | −12 754 |
| a public page | 34 488 · 6 | 16 781 · 6 | −17 707 |
| the sign-in | 34 488 · 6 | 18 462 · 7 | −16 026 |
| a console page | 36 706 · 8 | 19 168 · 8 | −17 538 |
| «Ma situation» | 37 902 · 9 | 20 537 · 9 | −17 365 |

Within V5 both shared bundles first grew, then ratcheted down under the owner's V5.8 rule (shared bundles never rise;
a surface's own CSS loads only where it is drawn): `main.css` peaked at 43 933 B (9 October) and the console's page
types at a ceiling of 50 927 B (11 October); the home's script reached 51 249 B before W4-B removed the Motion
library. The plan's milestone `dist/main.css` ≤ 36 KB is met.

## 4. How to deploy

The owner deploys; the team never touches a server, DNS, a domain or a certificate.

- [`docs/deployment/PRODUCTION_DEPLOYMENT_RUNBOOK.md`](deployment/PRODUCTION_DEPLOYMENT_RUNBOOK.md) — Ubuntu 24.04
  LTS, Python 3.12, PostgreSQL 16, Gunicorn under systemd, nginx, certbot: steps 1–15 from the release tag
  (`export ILE_TAG=v2.0.0` and the SHA of the handoff), static files vs public media vs private documents, TLS, the
  difference between a registrar transfer and a DNS cutover, the cutover sequence, the release tags and the states.
- [`docs/deployment/PRODUCTION_CHECKLIST.md`](deployment/PRODUCTION_CHECKLIST.md) — §A the release gate with the
  evidence each line needs, §B before the deployment, §C the backup before the cutover with its restore check, §D the
  smoke test.
- [`docs/deployment/ROLLBACK.md`](deployment/ROLLBACK.md) — the DNS rollback at the first cutover, a previous tag,
  forward-only migrations and the verified dump, storage restored with its database, and (§7) why
  `pre-v5-main-2026-10` is a reference, not a rollback target.
- [`docs/deployment/production.env.example`](deployment/production.env.example) — the template of the server's
  environment file; the runbook's step 5 generates the secrets on the server. [`.env.example`](../.env.example) lists
  every variable the code reads.
- **The first deployment** starts from an empty database: `migrate`, then `seed_all`. Nothing of the legacy platform is
  imported. At the deployment, set the phase flags in the back-office's phase console: the Forum's permanent mode
  (recommended, `docs/design-v5/QA/v54/w4-d/GO_LIVE_PHASE.md` F-2), Phase 3 as authorised; never
  `forms_override_without_legal`. The Virtual Forum and the newsletter stay closed until the legal pages are
  published, whatever their flags (F-3, enforced since part 2).

## 5. The owner's open decisions

**From F-5** (`docs/design-v5/QA/v54/sec-f5/NOTES.md`, «For the owner»):
1. How long the second factor's proof lasts — today the session: 8 hours after its last activity, and the browser's
   closing. A shorter life for back-office sessions is a policy decision.
2. One password-change path for staff: the back office's own form does not apply allauth's rate limit nor the
   sign-out after a change; sending staff to allauth's page would leave one path.
3. Rate limits counted per Gunicorn worker (local-memory cache: up to three times the figure) — accept, or add Redis
   and its client library (a new dependency).
And on the server, after the deployment: checklist D-12 — the sign-in asks the code before the back office opens.

**From F-7** (`docs/design-v5/QA/v54/sec-f7/NOTES.md` §5, Q1–Q12): the moves the lifecycle graph declares and §4
does not (now the administrator's alone: keep them in §4 with their actors, or remove them from the graph — Q1); the
training body's step (Q2); the authorised actor acting through the selection process only (Q3); who may lift a
suspension — an operator lifting a person's own pause? (Q4); ENTERED → POST_ENTRY, «automatic» in §4 but performed by
nobody automatically (Q5); a reason to leave SUSPENDED (Q6); the narrowings that follow §4 — the professional no longer
suspends or closes, the operator closes only from POST_ENTRY (Q7, Q8); an administrator who owns a file acts as its
owner (Q9); the back office's assignment inline (Q10, fixed in F-7's review); a second file opened after the
questionnaire on a suspended file (Q11); a co-operator's conclusion of a selection leaving the opener's assignment live
(Q12).

**From F-8** (`docs/design-v5/QA/v54/sec-f8/NOTES.md` §6, Q-1…Q-9; Q-8 is answered by CASE_LIFECYCLE §4 rule 5 —
§2): whether the administrator keeps making staff accounts and setting other accounts' passwords (Q-1); the grants
now inert in the back office — give the policies those roles or remove the grants (Q-2); who supervises deleted
documents' retention (Q-3); a domain service to hand a checklist line to another actor (Q-4); the case screens for the
administrator role (Q-5); mail bodies hidden from staff (Q-6); a person's e-mail switches editable by the administrator
(Q-7); staff reading every consent record (Q-9).

**The copy packet B1** — the words no family wrote, collected in each family's notes (none of them is shipped; every
word on the pages is live copy or an existing catalogue string): the sign-in's Caps Lock hint, session-ended line,
long-wait words and second-factor hints (W2-B); the compact rail's labels and «Changer d'espace» (W3-A); the
dashboards' and documents' group words («À vous · En cours · Réglées»), «Sans échéance», a deadline's distance in words
(W3-B, W3-C, W3-D, W3-E); the question headings of the doors and content pages (W3-F1, W3-F2); the CSRF failure page's
sentence (W3-F2); French typography on locked copy (item 8, with counsel); four words of F-7 (a refusal that says who
records a step, a verb to resume a suspended file, the suspended NowPanel's primary, a closed file's sentence); and the
Forum after its event — three prescribed sentences still in the future tense (`GO_LIVE_PHASE.md` F-1). Part 2 added
none: the sign-in's invitation is withheld with allauth's own words, and the closed file's refusal is the lifecycle's
existing sentence.

**GitHub settings** (read on 16 October 2026): the repository is public; its wiki is enabled and unused; Dependabot
alerts and security updates are off; secret scanning and push protection are on. Turning the wiki off and Dependabot
on are the owner's choices.

**The deployment's own questions** (`docs/design-v5/QA/v54/devops/NOTES.md`, still open): the host names (apex, `www`,
the canonical one; a temporary validation host); who inventories the subdomains before HSTS `includeSubDomains`; the
database — PostgreSQL 16 on the droplet or a managed cluster in an EU region; the SMTP provider, the sender domain's
SPF and DKIM, and an open outbound port; Redis (above); the backups' off-server EU location, key holder and retention;
raw client addresses in the access logs or not; a wider health endpoint or not; who owns nginx's default server and
the firewall if the designated server already hosts other sites; the written confirmation of EU hosting for the
server, the database and the backups (CR-08).

**The go-live phase** (`GO_LIVE_PHASE.md`): the authorisation of Phase 3; the Forum's permanent mode (F-2) and its
words after the event (F-1).

## 6. Known limits

- **Browsers and devices.** The browser suite and every family's checks ran in Chromium (headless). Safari/WebKit and
  Firefox were never run, nor a real phone (touch was synthesised, phone widths emulated), nor a real Windows
  contrast theme (forced colours were Chromium's emulation). W4-C's sweep and measures ran in Chromium too: no WebKit
  or Firefox build is on the measuring machine.
- **No screen reader by a person** (`docs/HUMAN_QA_CHECKLIST.md`; checklist A-9, A-23). The Arabic pages have had no
  Moroccan reader yet (B2).
- **No legal rule is in force.** The seed writes 16 candidates — 11 drafted from the norm, 5 taken from the previous
  platform — and none is active before a jurist's review and the verification of the fifteen sources (checklist A-16,
  A-23).
- **The official Italian legal texts are not received** (gate G1): every public form and the sign-up stay closed until
  they are published; translations wait for a human review (gate G10; pages fall back to French, marked).
- **Performance** (W4-C, `docs/design-v5/QA/v54/w4-c/PERF.md`: the compressed twin, 78 page types × fr, ar × 1440,
  390, slow 4G and CPU × 4, five cold loads a cell): LCP ≤ 2.5 s on every page type (slowest median 1.5 s), CLS within
  its budget everywhere (the upload page's 0.04–0.07 fixed to 0.000), every overlay's cold open ≤ 120 ms at p90. Four
  budget letters are **accepted exceptions**, none with a measured cost: the overlay core is 6.5 KB against 4 KB per
  module; Arabic console pages that use the monospaced face load 63 KB of fonts against the 56 KB Arabic budget; the
  sign-in pages make one script request more than V4 (a 394-byte helpers chunk); the work after the first paint is
  read as the rest of the first render. The public letterhead still moves slightly after the first paint on most
  desktop loads (0.01–0.02, rarely above 0.03; every median within budget), left to W4-D.
- **Uploads are not scanned** by an antivirus: they stay «not analysed», which the delivery rule says.
- **Rate limits per worker**, the **session-long second factor** and **one or two password-change paths**: §5.
- **The Forum after its event** shows the launch meeting with sentences written before it (F-1, `GO_LIVE_PHASE.md`).
- **The letterhead's small shift** above (W4-C) was not fixed by W4-D's part 2: its cause is diagnosed (the menu's
  inline place, not its height) but the fix touches the navigation's layout and needs its own measure; it is the
  first item after the release.
- **Typography of team-written French strings**: 149 French strings written in the templates beside « » : ; ? !
  are not yet passed through the typography filter that locked copy uses (a no-break space before the mark); a
  change of rendering on many pages, measured page by page after the release.
- **The legacy token layer** (`static/css/_legacy-tokens.css`: 138 old names and two classes mapped onto V5) remains a
  debt the tests count down; it only shrinks.
- **WebAuthn** is not enabled (TOTP only).
- **CI** runs the non-browser suite; the browser suite needs Chromium and runs locally (checklist A-3).

## 7. Release gates

The fourteen gates of the owner's directive V5.10, «before main moves». The result column is filled by the
release-candidate validation, on one commit, with its evidence; the middle column says only where things stood when
this draft was written. The validation ran on `4ffc22b` (27 October 2026) and, after its fixes, on `528bc5c` (28
October); the commits after it add only these notes and a timing correction to two tests (GitHub's first CI run on
the candidate counted, on one of its two jobs, a database backend that was leaving — the test now waits for it).

| # | Gate (V5.10) | At this draft (16 October 2026; part 2, 27 October) | Result |
|---|---|---|---|
| 1 | W4-A Mobile/RTL complete | in flight; merged on `design-v5` (17 October) | **PASS** — merged (tag `v54/w4-a`, DL54-157/158); its browser and RTL tests inside gate 6's 573 |
| 2 | W4-B Motion complete | merged on `design-v5` (16 October) | **PASS** — merged (tag `v54/w4-b`); the Motion library removed, the home's JavaScript 51 249 → 24 138 B |
| 3 | F-8 complete and merged | in flight; merged on `design-v5` (16 October) | **PASS** — merged (DL54-156); every item of the V5.10 list has DENY and ALLOW tests: 431 passed, none missing |
| 4 | F-5/F-7/NUL/API fixes present in the release candidate | F-5, F-7 and the NUL guard on `design-v5`; the API's input handling with F-8, merged | **PASS** — present in the candidate's code; their six test files: 272 passed |
| 5 | GitHub CI green | both runs of the matrix on the candidate's SHA (checklist A-2, A-26) | **Required on the release snapshot itself** (the commit that carries these notes): both matrix runs green before `main` moves; the run is linked from the GitHub release `v2.0.0` |
| 6 | Full regression green | non-browser and browser suites, 0 failed (checklist A-3) | **PASS** — fresh clone of `528bc5c`: 5 703 non-browser passed (4 skipped: no rule in force, the private table unset; 2 expected failures, declared debts) and 573 Chromium passed, 0 failed. A first run found 1 failure (the stale icon test), fixed |
| 7 | Django migration check clean | checklist A-4 | **PASS** — 71 migrations applied from an empty database under the development and the production settings; `makemigrations --check`: no changes |
| 8 | Django production/deploy checks reviewed | checklist A-5 | **PASS** — `check --deploy` under the production settings: only `security.W005`/`W021` (HSTS subdomains and preload off by design until the subdomains are inventoried, §5), 0 with them on; `collectstatic`: 617 files, manifest storage |
| 9 | Secret scan clean | checklist A-6 | **PASS** — every object of the candidate's tree: 0 for every known secret value in every encoding; the documented development values only |
| 10 | PII/confidential-artifact scan clean | checklist A-7 | **PASS** — no real personal data, no confidential artefact, no server identifier, no forbidden file |
| 11 | Working tree clean | checklist A-1 | **PASS** — the release branch's working tree clean; the snapshot is built from its commit |
| 12 | No known P0/P1 security defect | the release-candidate report's outstanding list | **PASS** — no open P0/P1 in the code or the reviews; the one P1 found (Pillow's 38 advisories) fixed in 13.0.0; P2s open: §5, §6 |
| 13 | Core product flows smoke-tested | checklist A-12 to A-20 | **PASS** — 393 page visits on the preview, French and Arabic, 1440 and 390: every expected status, no console error, RTL on every Arabic page, NUL → 400; questionnaire, case file, protected download (owner 200, others 403, anonymous to the sign-in), closed-file assignment refused, second factor when enforced |
| 14 | Preview reflects the actual candidate being released | the preview serving the candidate's commit (the plan runs it with a reference date of 3 October 2026, whose gate states are those of the whole release window — `GO_LIVE_PHASE.md` §1; the validation records the date the running preview uses) | **PASS** — the preview serves the candidate's commit, with the reference date of 3 October 2026 |
