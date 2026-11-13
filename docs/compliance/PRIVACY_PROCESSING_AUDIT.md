# Privacy processing audit — what the software really does (V5.14)

- Owner directive V5.14 (28 Oct 2026): the privacy notice (category **A**) and the cookie / technical-storage information (**B**) are written from the processing this application **actually** performs, and they do not wait for Allegato 1. Substantive content (**C**) and governance documents (**D**) still do.
- Audit date: 28 October 2026, on branch `design-v5` at `b4e5413`. This repository copy was re-checked on branch `v514-p`, and its `file:line` references point at that tree.
- The texts built from it are in `apps/legal/content/{privacy,cookies}/{it,fr,en,ar}.txt`. Sentence-by-sentence evidence is in `docs/legal/PRIVACY_NOTICE_SOURCES.md`.
- This file is repository-safe. It holds no secret, no personal data of a real person and no server identity. Approved project documents held outside the repository are cited by name only:
  - **ANX**: Annexe 1 FR, the legal lead's French courtesy copy of Allegato 1, dated 14 Sept 2026. Its privacy and cookie sections are archived in `apps/cms/locked_content.py`, keys `legal.privacy.fr_courtesy` and `legal.cookies.fr_courtesy`.
  - **IMPL**: the implementation document.
  - **RB**: `docs/deployment/PRODUCTION_DEPLOYMENT_RUNBOOK.md`.
- Nothing here was observed on a server. We never touch production, so the reverse proxy, logrotate and journald facts are **as configured by the runbook**, not as measured.

## 0. Verdict

- **No PRIVACY TRACKING BLOCKER.** There is no analytics, profiling, marketing, third-party cookie or external request that would hand a visitor's IP address to a third party.
  - The CSP is `'self'`-only (`config/settings/base.py:383-399`).
  - Fonts are self-hosted (`static/fonts/`).
  - `apps/cms/forbidden.py` refuses GA/gtag, pixels and Google Fonts hotlinks.
  - The `analytics` flag is `False` (`base.py:364`) and nothing reads it.
  - **Measured on the lane server, 28 Oct 2026:** the A and B pages in it/fr/en/ar at 1440 and 390 px made zero requests to any other origin. `document.cookie` was empty, because every cookie is HttpOnly.
- **Only technical cookies** are set, plus first-party browser storage for interface state. **No consent banner** (directive §4).
- **B (cookies)** has no open field. **OF-11 stays open** (V5.17 §7): the owner accepts in writing the two deviations from ANX listed in [`OF11_ANNEXE_DEVIATIONS.md`](OF11_ANNEXE_DEVIATIONS.md) before B is published; publishing is not that acceptance.
- **A (privacy)** is complete in structure, but it carries **10 open fields** (§6). Production refuses to publish it until each one is replaced by a verified fact.

## 1. Controller

| Fact | Value | Evidence |
|---|---|---|
| Controller | AGAMI — Dialogo Giuridico Interculturale APS, APS in RUNTS (Rep. n. 149809), C.F. 91036640240 | ANX §1.1 (`locked_content.py`, `legal.privacy.fr_courtesy`); `base.py` `ILE["PROMOTER"]` |
| Offices | Via Sandrigo 29, 36061 Bassano del Grappa (VI) (registered); Viale Giuseppe Mazzini 142, 00195 Roma (operational) | ANX §1.1 |
| Contact | contact@agamieuromed.org | ANX §1.1, §8; IMPL (all forms go there only); `base.py` `ILE["PUBLIC_CONTACT_EMAIL"]`, `ILE["FORMS_DESTINATION_EMAIL"]` |
| DPO | none named in any approved document | → **OF-08** |
| Supervisory authority | Garante per la protezione dei dati personali, art. 77 GDPR | ANX §8 |
| Moroccan users | law n° 09-08 «en tant que de besoin» | ANX §6 |

## 2. Processing that runs today (G1 closed)

| # | Processing | Data | Where | Retention as configured | Basis |
|---|---|---|---|---|---|
| P1 | Reverse-proxy access log | IP **masked** (IPv4 `.0`, IPv6 first 3 groups), time, method, **path without query string**, protocol, status, bytes, time, Host, request id. No UA, no referer | RB §11 (`map $remote_addr`, `log_format italylegalentry`) | daily rotation, **14 days** (RB §13 table, `/etc/logrotate.d/nginx`) | 6(1)(f), ANX §3 |
| P2 | Reverse-proxy error log | **raw IP** and the full request line, query string included (nginx's fixed format) | RB §11 `error_log … warn` | 14 days (same rule) | 6(1)(f) |
| P3 | Catch-all server, unknown Host on port 80 | nginx's default `combined` log: raw IP, request with query, UA, referer. On 443 the handshake is rejected, so nothing is logged | RB §11 catch-all block (no `access_log`) | 14 days (distribution default) | 6(1)(f). Request R-4 below |
| P4 | Application log (Django/Gunicorn → journald) | JSON lines: level, logger, request id, message, identifier extras (`user:<pk>`). `django.request` logs the path only. **No Gunicorn access log**. **No e-mail address** since V5.14 (§4) | `core/logging.py`; `base.py:456+` `LOGGING`; `config/log_filters.py` | **not configured** (RB §13: «journald's retention is the owner's policy») | → **OF-05** |
| P5 | Security audit trail | `AuditEvent`: actor + e-mail label, action, target, metadata, **`ip_hash`**, request id. Failed sign-in **without** the submitted address | `apps/audit/models.py`, `services.py`, `receivers.py:33-35` | **never purged** (`docs/security/AUDIT_MODEL.md` §6) | 6(1)(f) → **OF-06** |
| P6 | IP pseudonymisation | `hash_ip`: SHA-256 of `IP_HASH_SALT:ip`, 32 hex. The salt is mandatory in production | `core/privacy.py:19`; `prod.py` | as the record | pseudonymised, **not anonymised** |
| P7 | Abuse throttles (process memory) | public forms: `ip_hash`, 600 s; allauth: **raw IP** in the cache key for `login_failed` (5 min), `signup` (1 h), `reset_password` (1 h); an **unsalted SHA-256 of the e-mail address entered** (`/key`) for `login_failed` (5 min), `reset_password` (1 h), `confirm_email` (10 min); the **account id** (`/user`) for `change_password` and `manage_email` (1 min) | `core/throttle.py`; `base.py:205-212` `ACCOUNT_RATE_LIMITS`; allauth `core/internal/ratelimit.py:145-169` `get_cache_key`; LocMemCache `base.py:177` | 1 min to 1 h (public forms 10 min), memory only | 6(1)(f) |
| P8 | Sessions | DB session: auth id, allauth/MFA stage, flash messages, orientation pointers | `base.py:376-377`, `:486` | **8 h** after the last write; `clearsessions` daily (RB §10) | service + 6(1)(f) |
| P9 | Accounts, credentials, MFA | e-mail, name, language, account type, dates, terms acceptance, country, phone, organisation, verification data; PBKDF2 hash; TOTP + recovery codes | `apps/accounts/*`; `base.py:226,238` | until deletion/anonymisation, self-service (`accounts/urls.py:10`, `services.py:205`) | → **OF-10**; inactivity → **OF-07** |
| P10 | Orientation wizard (anonymous, live) | answers as choice keys, language, `ip_hash`, token hash, result + rule versions | `apps/orientation/*` | **30 days** (`orientation/constants.py:32`), purged daily | 6(1)(b), ANX §3 |
| P11 | Private documents | file, original name, kind, size, sha256, description, `uploaded_ip_hash` | `apps/documents/*`; `PRIVATE_MEDIA_ROOT` outside served directories; signed 10-min link | `retention_until` set by hand only, so a NULL value never expires | → **OF-07**, **OF-10**; art. 9 risk |
| P12 | Case files, checklists, messages, deadlines, help desk, academy, selection | per `docs/security/DATA_CLASSIFICATION.md` | `apps/cases`, `portal`, `helpdesk`, `academy`, `selection`, `companies` | **not configured** | → **OF-07**, **OF-10** |
| P13 | E-mail outbox | recipient, subject, **full text/HTML body**, reply-to, status, last error | `apps/notifications/models.py`, `services.py` | **never purged** | → **OF-07** (TG-3) |
| P-MAIL | SMTP relay | every outgoing e-mail | `prod.py:89`; `production.env.example` `EMAIL_HOST` placeholder | the provider's | provider unnamed → **OF-03** |
| P-HOST | Hosting | everything above | RB §1 (cloud firewall), Known limits | — | region, DPA, sub-processors unconfirmed (CR-08) → **OF-02** |
| P-BACKUP | Backups | `pg_dump`, private and public media, configuration; gpg-encrypted to the owner's key | RB §10 «The nightly backup» | **7 days local** (`KEEP_LOCAL_DAYS=7`); off-site undecided | → **OF-04** |
| P-CRM | CRM integration | ids and codes only | `INTEGRATIONS_TRANSPORT=LoggingTransport` (`base.py:418`): no socket | none today | n/a |

Closed by G1/G2 or a flag (not described as active in the notice; it says they will be added before activation):

- public forms (P14);
- forum registration (P15, outside the 24-month purge: TG-1);
- consent proofs (P16);
- the newsletter (P17);
- sign-up (P18);
- the Virtual Forum (P19).

Verified absent:

- analytics, tag managers and pixels;
- embeds, maps and social widgets;
- third-party fonts and CDNs;
- error-tracking SaaS;
- captcha;
- art. 22 decisions;
- transfers performed by the code.

## 3. Cookies and browser storage (production settings)

| Name | Purpose | Duration | Flags | Evidence |
|---|---|---|---|---|
| `sessionid` | session: sign-in, MFA stage, wizard, flash messages | anonymous: 8 h; after sign-in: browser session (`ACCOUNT_SESSION_REMEMBER=False`); server-side 8 h | HttpOnly, Lax, Secure | `base.py:200,376-377`; `prod.py:65` |
| `csrftoken` | CSRF protection | Django default `CSRF_COOKIE_AGE` = 52 weeks (not overridden) | HttpOnly, Lax, Secure | `base.py:378-379`; `prod.py` |
| `ile_language` | reading language | 365 days | HttpOnly, Lax, Secure | `core/middleware.py:95,110`; `base.py:259-261` |
| `mfa_trusted` | — | **not set** (`MFA_TRUST_ENABLED` defaults to False) | — | allauth `mfa/app_settings.py` |
| localStorage `ile.rail` | console rail open or closed | until cleared | never sent | `static/js/rail-pref.js`, `static/js/src/console.js` |
| sessionStorage `ile.lume` | page-transition mark, read within 5 s then removed | tab | never sent | `static/js/src/head/head.js:44-80` |
| sessionStorage `ile.hero.discovered` | home hero plays once per tab | tab | never sent | `static/js/src/hero.js` |
| sessionStorage `ile.dismissed.<id>` | dismissed institutional notice | tab | never sent | `static/js/src/home.js` |
| localStorage `adminTheme` (back office) | staff display theme: `light`, `dark` or `auto` (Alpine `$persist`) | until cleared | never sent | django-unfold `static/unfold/js/app.js:167` |
| localStorage `sidebarOpen`, `sidebarWidth`, `commandHistory` (back office) | staff UI state and staff search history on the staff device; `commandHistory` holds the text staff typed, which can be a name or an e-mail address (the notice's §3 intro says so) | until cleared | never sent | django-unfold `static/unfold/js/app.js:139-156,395,524-536` |
| localStorage `htmx-history-cache` (back office) | **not written today.** htmx keeps it only for `hx-push-url` navigation, which unfold uses in paginated inlines (`unfold/helpers/pagination_inline.html:19`, only when an inline sets `per_page`). No inline in this project sets `per_page`. If one ever does, this key (a copy of the page's HTML on the staff device) must be added to the notice | — | — | unfold templates |

`apps/legal/tests/test_privacy_cookie_v514.py::test_the_cookie_register_matches_the_configuration` fails if a name or a duration in the settings drifts from the text. `…::test_every_storage_key_named_in_the_notice_exists_in_the_front_end` checks the storage keys the same way, and `…::test_every_back_office_storage_key_of_the_installed_unfold_is_named_in_the_notice` reads every `localStorage`/`sessionStorage` key and every `$persist(...).as(...)` name from the installed unfold's `app.js` and requires it in the notice in all four languages.

## 4. Logging minimisation (directive §5)

| ID | Finding | Action |
|---|---|---|
| LG-1 | `notifications.deliver` logged the SMTP exception text. With `SMTPRecipientsRefused`, that text holds the recipient's address | **Fixed in this lane.** `config/log_filters.py` puts a redaction filter and redacting formatters on the `console` handler, covering message and traceback. The outbox pk and the exception class stay, and the DB copy in `EmailOutbox.last_error` stays (access-controlled). Tests: `tests/security/test_log_minimisation_v514_p.py`, end to end through the configured handler |
| LG-2 | The nginx error log keeps the raw IP and the query string (fixed format) | kept, because operations need it. The notice describes it (§3.1). Request R-4 |
| LG-3 | The catch-all server writes nginx's `combined` log (raw IP, query, UA, referer) for unknown hosts | Request R-4: `access_log off;` in the catch-all block. The notice describes the current configuration; drop that sentence when R-4 is applied |
| LG-4 | allauth rate-limit keys hold the raw IP, an unsalted SHA-256 of the e-mail address entered, or the account id, for 1 min to 1 h in memory | kept, because brute-force protection needs it. Stated in the notice (§3.2, §7; P7) |
| LG-8 | `LOGGING` did not configure the `django` logger, so Django's `DEFAULT_LOGGING` handlers stayed on it. Under DEBUG (preview, dev) its console handler printed `django.request`/`django.security` lines a second time, unredacted (production unaffected: `RequireDebugTrue`; `mail_admins` with no `ADMINS`) | **Fixed (v514-p-fix).** `base.py` `LOGGING['loggers']['django'] = {handlers: [], level: INFO, propagate: True}` detaches them; every line now goes through the redacting root `console` handler. Test: `apps/legal/tests/test_privacy_cookie_v514.py::test_a_django_request_line_reaches_no_output_unredacted_under_debug` (fails without the line). `django.server` (runserver only) keeps Django's own handler and logs request lines with their query strings; it never runs in production (gunicorn) |
| LG-5 | paths with tokens (download 10 min, reset and confirmation links) appear in access and request logs | kept. Logs are root/`adm` only, and the retention is short (journald: OF-05) |
| LG-6 | `client_ip` takes the left-most X-Forwarded-For entry | correct behind RB's nginx, which overwrites XFF |
| LG-7 | journald retention is unset | **OF-05** |

Not changed, on purpose: no security logger was removed or lowered. `django.security` stays at WARNING and `ile.security`/`ile.audit` at INFO; the request id filter stays. The application never logs a raw IP, so IP redaction in Django logs would only hide server addresses that operations need.

## 5. Where ANX does not match the software (OF-11, open: [`OF11_ANNEXE_DEVIATIONS.md`](OF11_ANNEXE_DEVIATIONS.md))

1. ANX's cookie section says external providers may learn the visitor's IP. That is **false** here, so the notice says that no third party receives it.
2. ANX does not mention browser storage. The notice lists it.
3. ANX does not cover the authenticated platform (accounts, MFA, documents, case files). The notice describes it, and its legal basis is **OF-10**.
4. ANX's «durées techniques strictement nécessaires» is replaced by the configured figures.
5. ANX's «serveurs dans l'UE, pas de transfert» is **not verified**, so it becomes open field **OF-02**.
6. Consent wording vs 6(1)(b) for the forms: **OF-09**. The forms are closed, so the notice does not describe them yet.
7. The IP hash is described as pseudonymisation.

## 6. Open fields (owner input; each `[DA COMPLETARE — OF-nn — <class>: …]` in the text blocks publication in production)

Since V5.16 (28 October 2026, lane P2) every marker carries **one class**, in English in every language, after its id:
**PRODUCTION CONFIGURATION REQUIRED** (the real infrastructure: it blocks PRODUCTION_CONFIG_COMPLETE, not
PRODUCT_COMPLETE), **OWNER CONFIRMATION REQUIRED** (OF-01) or **LEGAL REVIEW REQUIRED** (bases, art. 9, roles, DPO
status, retention policies: COMPLIANCE_REVIEW_COMPLETE, V5.17 §2). Production refuses the text while any marker of
any class remains (`legal.models.OPEN_FIELD_CLASSES`; `apps/legal/tests/test_open_field_classes_v516.py`). None of
them blocks PRODUCT_COMPLETE. The PRODUCTION CONFIGURATION REQUIRED rows are not questions for the owner now (V5.17
§10): they are verified when the production server is prepared, as checklist A-30's items.

| ID | Class | Question | In the text |
|---|---|---|---|
| OF-01 | OWNER CONFIRMATION REQUIRED | AGAMI APS is the **candidate** controller: the owner confirms in writing that it is the controller for Italy Legal Entry (Italy Legal Entry is not substituted as controller unless the owner confirms it is a separate legal entity), and that its name, offices and contact are current (V5.16 §2) | A §1 |
| OF-02 | PRODUCTION CONFIGURATION REQUIRED | Hosting: DigitalOcean is the **intended** provider (V5.16 §10, named in A §5). To verify on the production infrastructure: the region of the server, DB and volumes, DigitalOcean's art. 28 DPA accepted, sub-processors, any transfer and its safeguard (CR-08) | A §5, §6 |
| OF-03 | PRODUCTION CONFIGURATION REQUIRED | SMTP provider actually used in production (name, seat, DPA, region); mail host of the contact@agamieuromed.org mailbox | A §3.6 (and §6) |
| OF-04 | PRODUCTION CONFIGURATION REQUIRED | Off-server backups: location, provider, region, who can access them, retention | A §3.7 (and §6) |
| OF-05 | PRODUCTION CONFIGURATION REQUIRED | journald retention; the 14-day logrotate on the real server | A §3.1 |
| OF-06 | LEGAL REVIEW REQUIRED | Retention of the security audit trail (policy) | A §3.2 |
| OF-07 | LEGAL REVIEW REQUIRED | Retention policies: inactive accounts; documents, case files, messages, deadlines, help desk, academy, selection; e-mail outbox copies | A §3.3, §3.5, §3.6 |
| OF-08 | LEGAL REVIEW REQUIRED | DPO STATUS = TO BE CONFIRMED (`DPO_ASSESSMENT.md`) | A §2 |
| OF-10 | LEGAL REVIEW REQUIRED | Legal basis of the authenticated platform and of backups (`PROCESSING_PURPOSE_MATRIX.md`) | A §3.3 |
| OF-12 | LEGAL REVIEW REQUIRED | The role of each recipient category: processor, independent controller or joint controller (`RECIPIENT_ROLES_MATRIX.md`) | A §5 |
| OF-13 | LEGAL REVIEW REQUIRED | SPECIAL CATEGORY LEGAL BASIS REQUIRED: the art. 9 condition for special-category data in uploads and free texts (`SPECIAL_CATEGORY_AUDIT.md`); new with V5.16 §5 | A §3.5 |
| OF-09 | LEGAL REVIEW REQUIRED (locked copy) | One basis for the forms (6(1)(b) or consent): the team's forms now ask an acknowledgement; the two prescribed sentences are LOCKED COPY — LEGAL REVIEW REQUIRED (`FORMS_LEGAL_BASIS_UX.md`) | not in the text: the forms are closed. It must be answered before G2 opens, when A gets its forms section |
| OF-11 | OWNER CONFIRMATION REQUIRED | (a) accept in writing the two deviations of §5 items 1–2 from ANX, as listed in `OF11_ANNEXE_DEVIATIONS.md` — open, not closed by publishing (V5.17 §7); (b) confirm that the presentational sessionStorage keys are technical (non-blocking) | — |

## 7. Technical gaps (for their owners; not this lane's code)

- **TG-1**: `ForumRegistration` is outside the 24-month purge (`enquiries/models.py` `SUBMISSION_MODELS`).
- **TG-2**: `PrivateDocument.retention_until` is never set by code (OF-07).
- **TG-3**: `EmailOutbox` keeps full bodies with no purge, and `anonymise_user` does not clear them (OF-07).
- **TG-4**: LG-1, now fixed by the log filter. The address remains in `last_error` by design.

## 8. Requests to other owners

- **R-1** (footer, lane D): link Privacy and Cookie information as soon as they are public. Omit the unpublished C/D links (`legal.services.document_available(kind)`).
- **R-2** (gates, lane C): keep G1 = all five pages (`legal.services.all_official_pages_published`). It already is, and it is tested.
- **R-3** (orientation templates): link the privacy notice from the orientation wizard, which is live and collects data.
- **R-4** (runbook): `access_log off;` in the catch-all server; keep and document the error log.
