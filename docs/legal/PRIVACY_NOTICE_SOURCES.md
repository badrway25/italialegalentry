# Privacy notice and cookie information — sentence → evidence (V5.14)

- The texts: `apps/legal/content/privacy/it.txt` (A) and `apps/legal/content/cookies/it.txt` (B), the Italian masters.
- `fr.txt`, `en.txt` and `ar.txt` are courtesy translations. They follow the master sentence by sentence, and `apps/legal/tests/test_privacy_cookie_v514.py` holds them to the same sections and the same open fields. Each one says that the Italian prevails, and the document metadata flags them `pending_legal_review`.
- Evidence keys:
  - `file:line` refers to branch `v514-p`;
  - **ANX** is Annexe 1 FR, the approved French courtesy copy of Allegato 1. Its privacy and cookie sections are archived in `apps/cms/locked_content.py` under `legal.privacy.fr_courtesy` and `legal.cookies.fr_courtesy`;
  - **RB** is the production runbook;
  - **AUD** is `docs/compliance/PRIVACY_PROCESSING_AUDIT.md`.
- A statement with no evidence is not in the text. It is an open field, `[DA COMPLETARE — OF-nn — <class>: …]`, and production refuses to publish while one remains (`legal.services.publish`; `legal.models.LegalDocument.is_available`). The class (V5.16) is PRODUCTION CONFIGURATION REQUIRED, OWNER CONFIRMATION REQUIRED or LEGAL REVIEW REQUIRED (`docs/compliance/PRIVACY_PROCESSING_AUDIT.md` §6).

## A — Informativa sul trattamento dei dati personali

| § | Statement (it master) | Evidence |
|---|---|---|
| intro | arts. 13–14 GDPR, D.Lgs. 196/2003 as amended by D.Lgs. 101/2018; site and platform users | ANX §1 heading |
| intro | describes the processing in the current configuration | directive V5.14 §2; AUD |
| 1 | controller identity, RUNTS, C.F., offices, contact | ANX §1.1; `base.py` `ILE["PROMOTER"]`, `ILE["PUBLIC_CONTACT_EMAIL"]`. Currency → **OF-01** |
| 2 | DPO | not in any approved document → **OF-08** |
| 3.1 | access log fields, IPv4 last part zeroed, IPv6 first three groups, path without parameters, no UA or referer | RB §11 `map $remote_addr $italylegalentry_client`, `log_format italylegalentry` (`$uri`, not `$request_uri`) |
| 3.1 | error log: full IP and full request | RB §11 `error_log … warn`; nginx's fixed error format (AUD LG-2) |
| 3.1 | other host names refused, standard log with full IP, request, UA, referer | RB §11 catch-all block (`return 444`, no `access_log`; `ssl_reject_handshake on` on 443) (AUD P3) |
| 3.1 | application log: internal identifiers, never the e-mail; path without parameters on error; no IP, no form content | `apps/core/logging.py:16-38`; `apps/audit/services.py` (`user:<pk>`); Django `django.request` logs `request.path`; `config/log_filters.py` (e-mail redaction); `tests/security/test_log_privacy.py`, `test_log_minimisation_v514_p.py` |
| 3.1 | purposes; basis 6(1)(f) | ANX §3 («garantir la sécurité du site et prévenir les abus … art. 6.1.f») |
| 3.1 | daily rotation, 14 days | RB §13 log table («rotated daily, 14 days (`/etc/logrotate.d/nginx`)»). Server confirmation and journald → **OF-05** |
| 3.2 | IP not stored in clear; SHA-256 with secret key; pseudonymised, not anonymous | `apps/core/privacy.py:19-23`; `prod.py` `IP_HASH_SALT` mandatory |
| 3.2 | security log contents; failed sign-in without the address | `apps/audit/models.py`; `apps/audit/receivers.py:33-35`; `docs/security/AUDIT_MODEL.md` |
| 3.2 | counters: sign-in, sign-up and reset by IP, 5 min – 1 h; public forms by IP hash, 10 min; memory only | `base.py:205` `ACCOUNT_RATE_LIMITS`; allauth 65.19 `core/internal/ratelimit.py` (IP in the key); `apps/core/throttle.py`; LocMemCache `base.py:177` (no `REDIS_URL` in `production.env.example`) |
| 3.2 | basis 6(1)(f) | ANX §3 |
| 3.2 | retention of the security log | not configured, never purged (AUDIT_MODEL §6) → **OF-06** |
| 3.3 | account fields, profile, organisation, verification | `apps/accounts/models.py` (`User`, `PersonProfile`, `Membership`, `AccountVerification`) |
| 3.3 | password as a non-reversible hash | `base.py:238` `PASSWORD_HASHERS` (PBKDF2) |
| 3.3 | second factor TOTP + recovery codes; mandatory for staff and roles reading others' data | `base.py:226` `MFA_SUPPORTED_TYPES`; `accounts/services.py` `MFA_REQUIRED_ROLES`, `reads_other_peoples_data`; `prod.py:87` `BACKOFFICE_MFA_ENFORCED=True` |
| 3.3 | session in the DB, 8 h after the last update, expired sessions deleted daily | `base.py:376`; no `SESSION_ENGINE` (DB); RB §10 `clearsessions` daily 03:40 |
| 3.3 | legal basis of the reserved area | ANX does not name the platform → **OF-10** |
| 3.3 | kept until deletion; self-service deletion from the profile; deletion anonymises | `accounts/urls.py:10` (`profil/suppression/`); `accounts/services.py:205` `anonymise_user`. Inactivity → **OF-07** |
| 3.4 | questionnaire without account; answers as predefined choices, language, IP hash, resume-token hash, result with rule versions | `apps/orientation/models.py` (`OrientationSession`, `OrientationResult`); views ungated (`orientation/views.py`) |
| 3.4 | basis 6(1)(b) | ANX §3 («répondre aux demandes d'orientation … art. 6.1.b») |
| 3.4 | 30 days without account, then automatic deletion | `orientation/constants.py:32` `ANONYMOUS_SESSION_TTL_DAYS = 30`; RB §10 `purge-orientation-sessions` daily |
| 3.5 | upload PDF/JPEG/PNG incl. identity documents; platform modules | `apps/documents`; `docs/DEPLOYMENT_READINESS.md` §3; `config/urls.py` routes (cases, portal, helpdesk, academy, selection) |
| 3.5 | stored fields per document | `documents/models.py` (`PrivateDocument`: file, original name, kind, size, sha256, description, `uploaded_ip_hash`) |
| 3.5 | outside every web-served directory; download from the reserved area, personal link valid 10 min | `base.py:274` `PRIVATE_MEDIA_ROOT`; `prod.py` overlap guard; `documents/services.py` signed link (10 min) |
| 3.5 | who accesses: user, organisation contact, authorised staff | `documents/policies.py`; DATA_CLASSIFICATION P-12 |
| 3.5 | art. 9 advice for free fields | ANX §2 (last sentence) |
| 3.5 | art. 9 condition | none approved → **OF-13** (LEGAL REVIEW REQUIRED; `docs/compliance/SPECIAL_CATEGORY_AUDIT.md`) |
| 3.5 | retention | not configured → **OF-07** |
| 3.6 | service e-mails; outbox copy (recipient, subject, text) | `notifications/models.py` `EmailOutbox`; `notifications/services.py` |
| 3.6 | provider; mailbox host | `production.env.example` `EMAIL_HOST=<smtp-host>` (placeholder) → **OF-03**; copy retention never purged → **OF-07** |
| 3.7 | nightly encrypted backup of DB and documents; 7 days on the server; off-server copy planned | RB §10 «The nightly backup» (`gpg`, `KEEP_LOCAL_DAYS=7`, off-server location undecided) → **OF-04** |
| 3.8 | forms, event registration, sign-up, newsletter, Virtual Forum not active; CRM integration not active | `core/gates.py` G1/G2, `newsletter_enabled`, `virtual_forum_enabled`; `accounts/adapters.py` (sign-up); `base.py:418` `LoggingTransport` (no socket) |
| 4 | optional provision; informational pre-assessments; no art. 22 decision | ANX §4; `docs/PRIVACY_BY_DESIGN.md` §8 |
| 5 | recipients: staff and authorised persons; hosting provider as processor; SMTP; off-site backup provider | ANX §5 («prestataires … hébergement … art. 28»); RB. Categories and roles → **OF-12**; DPA and sub-processors → **OF-02** |
| 5 | «intended provider: DigitalOcean» | directive V5.16 §10 («DigitalOcean may be documented as the intended hosting provider»); RB §1 (DigitalOcean droplet). Region, DPA state and transfers are not stated → **OF-02** |
| 5 | not disseminated; no third-party resources or analytics on the pages | ANX §5 («ne sont en aucun cas diffusées»); AUD §0 and §2 (CSP `base.py:383`, measured zero external requests) |
| 6 | location and transfers | ANX §6 is unverified (CR-08) → **OF-02** (with OF-03, OF-04) |
| 6 | Moroccan law 09-08 | ANX §6 |
| 7 | summary figures | as 3.1–3.7 |
| 8 | rights arts. 15–22, contact; self-service deletion; complaint to the Garante, art. 77 | ANX §8; `accounts/urls.py:10` |
| 9 | HTTPS only; second factor; IP fingerprints; encrypted backups; documents never served directly | `prod.py` (`SECURE_SSL_REDIRECT`, HSTS checks); `MFA_REQUIRED_ROLES`; `core/privacy.py`; RB §10 (gpg); `tests/deployment/test_private_documents_are_never_served.py` |
| 10 | cookies and storage summary | text B |
| 11 | updated when processing changes; version shown; each published version kept | `legal.services.publish` (`LegalDocumentVersion` snapshot, `effective_date` on first publication); `templates/legal/document.html` meta line |

## B — Informativa sui cookie e sulle tecnologie di memorizzazione

| § | Statement | Evidence |
|---|---|---|
| intro | Garante guidelines of 10 June 2021; art. 122 Codice; art. 13 GDPR | ANX cookie section heading |
| 1 | only first-party technical cookies and browser storage; no profiling, marketing, analytics or tracking | AUD §0, §3; `base.py:364` (analytics off); `cms/forbidden.py` |
| 1 | no third-party fonts, scripts, images, maps or videos; no third party receives the IP | CSP `base.py:383-399` (`'self'`); `static/fonts/`; measured: zero external requests (AUD §0) |
| 1 | no consent needed; no banner | Garante guidelines (technical cookies), as ANX's cookie section states; directive V5.14 §4 |
| 2 `sessionid` | purpose; set only when the session is written; 8 h anonymous / browser session after sign-in / server 8 h; random identifier; HttpOnly, Lax, Secure | Django sessions; `base.py:200,376-377`; allauth `set_expiry(0)` with `ACCOUNT_SESSION_REMEMBER=False`; `prod.py:65` |
| 2 `csrftoken` | CSRF; set with a form; 52 weeks; HttpOnly, Lax, Secure | Django `CSRF_COOKIE_AGE` default (not overridden); `base.py:378-379`; `prod.py` |
| 2 `ile_language` | language; on a language-prefixed page; 365 days; two-letter code; HttpOnly, Lax, Secure | `core/middleware.py:95,110` (`LanguageCookieMiddleware`); `base.py:259-261`; `prod.py` |
| 3 | storage values carry no identifier, stay on the device and are never sent | AUD §3; the scripts set and read them locally only |
| 3 `ile.rail` | rail open or closed; until cleared; «open»/«closed» | `static/js/rail-pref.js`; `static/js/src/console.js` |
| 3 `ile.lume` | transition mark, read within 5 s then removed | `static/js/src/head/head.js:44-80` |
| 3 `ile.hero.discovered` | home opening once per tab; «1» | `static/js/src/hero.js` |
| 3 `ile.dismissed.<id>` | dismissed notice per tab; «1» | `static/js/src/home.js`; `templates/pages/home/_banner.html` |
| 3 back office | `sidebarOpen`, `sidebarWidth`, `commandHistory` | django-unfold `static/unfold/js/app.js` (installed package) |
| 4 | browser settings; disabling technical cookies may impair features | ANX cookie section, last paragraph |
| 5 | banner first if analytics or third-party cookies are ever introduced | ANX cookie section (third paragraph, second sentence) |

Not taken from ANX, on purpose (AUD §5): the sentence on external providers that «may learn the IP», which is false for this software. The developer's operational note is not to be published (ANX itself says so).
