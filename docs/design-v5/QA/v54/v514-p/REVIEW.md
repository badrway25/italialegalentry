# V5.14 privacy lane: review (label v514-p-review)

- **Branch:** `v514-p` @ `9156611` (worktree `C:/tmp/ile_wt/v514-p`). **Base:** `b4e5413` (design-v5 HEAD at branch time).
- **Reviewer:** privacy review, 28 Oct 2026.
- **Verdict: APPROVE_WITH_FIXES.** Nothing here is a major finding, and no tracking blocker was found. Seven minor findings: two are text accuracy (one in B, one in A), and the rest are hardening and test strength. B must take its fix before the owner publishes it. A cannot be published in production anyway until the 10 open fields are answered.

## What was checked, and how

- **Directive.** V5.14 was read in full. Each requirement was checked against the code at `9156611`, not against the builder's summary.
- **Privacy notice, sentence by sentence.** Each sentence of `apps/legal/content/privacy/it.txt` was checked against the evidence cited in `docs/legal/PRIVACY_NOTICE_SOURCES.md`, with the source file opened each time:
  - settings `base.py` / `prod.py` / `test.py`;
  - runbook §10, §11 (nginx `map`, `log_format`, catch-all), §13;
  - `core/privacy.py`, `core/logging.py`, `core/middleware.py`;
  - `audit/receivers.py`, the audit action names, `accounts/models.py` / `urls.py` / `services.anonymise_user`;
  - `documents/services.py` (`DOWNLOAD_LINK_TTL = 600`);
  - the allauth 65 `core/internal/ratelimit.py` source.
- **Cookie and storage register.** Checked against the settings and middleware, and against every `localStorage` / `sessionStorage` / `document.cookie` call. The search covered `static/js` (src and dist), `apps/*/static`, the templates and the installed django-unfold package.
- **External requests.** No absolute third-party URL appears in the templates. The CSP is `'self'`-only. htmx is not loaded on the public site: `orientation/_step.html` has inert `hx-*` attributes. **No PRIVACY TRACKING BLOCKER.**
- **Translations.** EN was compared with the IT master section by section and is faithful. FR, EN and AR carry the «Italian prevails» notice and the link to the Italian, and the test pins the same open-field ids in every language.
- **Tests run** (lane l7, `test_ile_v5_l7`):
  - `apps/legal` + `tests/security/test_log_minimisation_v514_p.py` + `test_log_privacy.py`: **32 passed** (the prod-settings subprocess test ran; it did not skip);
  - `tests/compliance/{test_gates, test_gate_dependencies_w4_d, test_locked_content, test_no_links_to_gated_pages, test_no_personal_data_in_repository, test_public_pages}` + `tests/backoffice/test_backoffice.py` + `tests/security`: **224 passed, 1 skipped** (the confidential-sentinel table is not configured here, which is expected).
- **HTTP-level DENY check, by hand** (lane DB, where privacy is published with 10 open fields):
  - with `ILE_LEGAL_OPEN_FIELDS_ALLOWED=False`, `/it/` and `/ar/privacy-policy/` render the `legal-blocked` page and no «DA COMPLETARE» text;
  - `/en/cookie-policy/` renders the text;
  - with `True`, the privacy text is shown with its markers;
  - the only cookie set is `ile_language`.
- **Diff hygiene.**
  - No CRLF.
  - No secret: the prod-settings test uses throwaway values.
  - No personal data of a natural person: the controller is a legal person, as in the Annexe.
  - No server identity: no IP, droplet name or region. «DigitalOcean» appears only as a forbidden string in a test; the runbook already names the provider.
  - No confidential-material location in the repository.

## Confirmed correct

- **Controller and contact.** They match the Annexe §1.1 and `ILE["PROMOTER"]` / `PUBLIC_CONTACT_EMAIL`, and OF-01 asks for confirmation that they are current.
- **Nothing invented.** The DPO (OF-08), hosting region and transfers (OF-02), the SMTP provider (OF-03), the off-server backups (OF-04), journald retention (OF-05), audit retention (OF-06), platform retention (OF-07), the platform's legal basis (OF-10) and the recipients' roles (OF-12) are all open fields.
- **The nginx facts match RB §11 exactly:**
  - masked IPv4 `.0` and IPv6 first three groups;
  - `$uri`, not `$request_uri`;
  - no user agent or referer;
  - the error log at `warn`, which holds the raw IP and query;
  - the catch-all `return 444` with no `access_log`, so on port 80 the distribution's `combined` log applies.
- **Application log.** It holds identifiers only; `django.request` logs `request.path`; no raw IP is logged anywhere (`client_ip` is only ever hashed); Gunicorn writes no access log (RB §9).
- **Sessions:**
  - `SESSION_COOKIE_AGE` 8 h;
  - database backend;
  - `ACCOUNT_SESSION_REMEMBER=False`, so the cookie lasts for the browser session after sign-in;
  - `clearsessions` runs daily (RB §10).
- **Other cookies:**
  - `csrftoken`: Django's default 52 weeks; HttpOnly, Lax, and Secure in prod;
  - `ile_language`: 365 days; HttpOnly, Lax, Secure;
  - `mfa_trusted` is not set.
- **Front-end storage.** `ile.lume` is read within 5 s and removed; `ile.rail`, `ile.hero.discovered` and `ile.dismissed.<id>` exist. The other sessionStorage key is a feature probe, set and removed at once.
- **Orientation questionnaire.** 30 days (`ANONYMOUS_SESSION_TTL_DAYS`), purged daily, basis 6(1)(b) from the Annexe §3.
- **Audit trail:**
  - a failed sign-in is recorded without the submitted address (`receivers.py:33-35`);
  - `auth.role_granted`, `documents.downloaded` and `case.viewed` exist, as the text says;
  - `ip_hash` is a keyed SHA-256 and is correctly described as pseudonymised, not anonymous.
- **Documents.** Private root, signed link valid 10 min, `uploaded_ip_hash`.
- **Departures from the Annexe.** The Annexe's false «external providers may learn the IP» is dropped, and the departures are listed for the owner as OF-11.
- **Publication:**
  - A and B are published one by one through `legal.services.publish`;
  - `document_available(kind)` is cached and invalidated;
  - production refuses to publish a text with a marker (in the IT text or any translation), and even a row forced to PUBLISHED is not shown;
  - `prod.py` hard-codes `ILE_LEGAL_OPEN_FIELDS_ALLOWED = False`;
  - the seed writes drafts only, never publishes and never overwrites an editor's change or a published text;
  - C and D stay BLOCKED and are never drafted.
- **G1.** `all_official_pages_published` still needs all five documents. The test publishes A and B, turns on the newsletter and Virtual Forum flags, and confirms that G1, the public forms, the newsletter, the Virtual Forum and sign-up all stay closed. A and B answer 200.
- **LG-1 logging fix.**
  - The filter sits on the `console` handler together with the redacting formatters, so the plain format, the JSON format and tracebacks are all redacted.
  - `request_id` is kept. `django.security` stays at WARNING and `ile.security` / `ile.audit` at INFO.
  - The address of a failed delivery stays in `EmailOutbox.last_error`.
  - The end-to-end test with `SMTPRecipientsRefused` passes.
  - Verified by hand: under the prod-like path (DEBUG False), the root handler is the only one that writes.
- **Rendering.** The text is escaped by blocks and only `<mark>` is added, so no raw HTML comes from the database.

## Findings (all minor)

1. **B §3 misses a back-office storage key and contradicts itself.**
   - **Where:** `apps/legal/content/cookies/*.txt` §3.
   - **Missing key:** django-unfold also persists the staff theme in `localStorage` key `adminTheme`, through `Alpine.$persist(defaultTheme).as("adminTheme")` in `unfold/static/unfold/js/app.js:167`.
   - **Contradiction:** the §3 intro says the values «non contengono identificativi», but `commandHistory` holds the staff member's search texts, which can include names or e-mail addresses.
   - **Fix:** add `adminTheme` (value light/dark/auto, kept until cleared, staff only) to the back-office entry in it/fr/en/ar. Reword the intro along the lines of «non sono inviati al server e restano sul dispositivo; le ricerche del personale possono contenere dati che il personale ha digitato». Extend `test_every_storage_key_named_in_the_notice_exists_in_the_front_end` to the unfold keys, read from the installed package.
   - **Not an issue:** `htmx-history-cache` would only appear with unfold inline pagination (`hx-push-url`), and no inline sets `per_page`. Note this in AUD §3 so that a future `per_page` inline triggers a register update.
2. **A §3.2 understates the abuse counters.**
   - **Where:** `apps/legal/content/privacy/*.txt` §3.2 and §7; AUD P7.
   - **What the text says:** the sign-in, sign-up and recovery counters are «associati all'indirizzo IP» and last «tra 5 minuti e 1 ora».
   - **What allauth does** (`ACCOUNT_RATE_LIMITS`, and `get_cache_key` in allauth 65):
     - it also keys `login_failed` (5 min), `reset_password` (1 h) and `confirm_email` (10 min) on an **unsalted SHA-256 of the e-mail address entered**;
     - it keys `change_password` and `manage_email` on the account id for **1 minute**.
   - **Fix:** say «associati all'indirizzo IP e, per l'accesso, il recupero della password e la conferma dell'indirizzo, a un'impronta dell'indirizzo e-mail digitato; per le modifiche della password e dell'indirizzo, all'account» and «tra 1 minuto e 1 ora». Update §7, FR/EN/AR and AUD P7.
3. **Outside production, `django.*` log lines are printed unredacted a second time.**
   - **Where:** `config/settings/base.py` `LOGGING`.
   - **Cause:** Django's `DEFAULT_LOGGING` handlers stay attached to the `django` logger, because `LOGGING` does not configure that logger.
   - **Effect:** under DEBUG (preview and dev), Django's own console handler prints `django.request` / `django.security` lines **unredacted**, alongside the redacted root line. Reproduced: `logging.getLogger('django.request').error('… a.b@example.org')` prints the address once in clear.
   - **Production:** not affected. The handler is `RequireDebugTrue`, and `AdminEmailHandler` has no `ADMINS`. Even so, the docstring's «every line» is not true for the preview.
   - **Fix:** add `"django": {"handlers": [], "level": "INFO", "propagate": True}` to `LOGGING["loggers"]`, which detaches the default handlers so everything flows through the redacting root handler. Then add a test that logs an address on `django.request` under DEBUG=True and finds it nowhere.
4. **An edit to a published A/B text in the back office goes live without the publication rules.**
   - **Where:** `apps/legal/admin.py` `save_model`, `models.LegalDocument.save`.
   - **Effect:** `body_it` and the new editable `translations` JSON change the live text at once. There is no publish-permission check, no source check and no `LegalDocumentVersion` snapshot, and `translation_status` can be switched to «reviewed» by anyone with change permission. A §11 promises «il titolare conserva ogni versione pubblicata», which this path breaks.
   - **Mitigation:** production would still hide a text that regains a marker. The behaviour itself predates this branch for C/D.
   - **Fix (inside apps/legal):** when a PUBLISHED document's checksum changes in `save_model`, return it to DRAFT, or snapshot it through `publish()`. Add a test.
5. **The production-settings DENY test is weaker than it looks.**
   - **Where:** `apps/legal/tests/test_privacy_cookie_v514.py::test_production_settings_force_open_fields_off`.
   - **Problem 1:** no settings module reads an environment variable `ILE_LEGAL_OPEN_FIELDS_ALLOWED`, so passing `"1"` proves nothing.
   - **Problem 2:** the test `pytest.skip`s silently whenever prod settings fail to load.
   - **Problem 3:** the HTTP-level DENY (a published row with markers renders `legal-blocked`, without the text, in it and ar) is not a test; I checked it by hand only.
   - **Fix:** keep the subprocess but `fail` instead of `skip`. Add a test that `/it/privacy-policy/` and `/ar/privacy-policy/` render `data-gate="legal-blocked"` and contain neither «DA COMPLETARE» nor the body when the row is PUBLISHED and open fields are not allowed. This makes the DENY as strong as the ALLOW test.
6. **The request for privacy links is incomplete.**
   - **Where:** `docs/design-v5/QA/v514-p/NOTES.md`, «Requests to other lanes».
   - **Gap:** directive §1 says «wherever personal data is collected». The notes ask only for the orientation wizard.
   - **Fix:** also ask for links on the sign-in and password-reset pages (allauth templates), the profile and its export and deletion pages, the document upload (`documents/partials/depot.html`) and the help-desk request form.
7. **A cookie text detail.**
   - **Where:** `cookies/*.txt` `csrftoken`, «Quando viene impostato».
   - **Gap:** for a signed-in user, every page has a form (the logout form in `components/account_menu.html`). The sentence is true but could surprise a reader.
   - **Fix:** optionally say «… anche il pulsante di uscita dell'area riservata».

## Requests carried to other lanes (unchanged, endorsed)

- **Lane D (footer):** link to Privacy and Cookie information through `document_available(kind)`, and drop the unpublished C/D links.
- **Lane C (hide gates):**
  - gate the legal routes per document, not on G1;
  - keep G1 at all five documents;
  - the production «privacy blocked» page must not read as «work in progress» (§8).
- **Runbook owner:** R-4, `access_log off;` in the catch-all server.

## Owner's open fields (release blockers for A; unchanged)

- **Release blockers:** OF-01, OF-02, OF-03, OF-04, OF-05, OF-06, OF-07, OF-08, OF-10, OF-12, as listed in AUD §6.
- **OF-09:** must be answered before G2.
- **OF-11:** publishing B or A counts as acceptance.
- **B** becomes publishable once finding 1 is fixed.
