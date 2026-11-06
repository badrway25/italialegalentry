# V5.14 privacy lane — build notes (label v514-p-build)

- Branch: `v514-p`, from `design-v5` at `b4e5413`.
- Directive: V5.14 «Privacy is not blocked by Allegato 1» (28 Oct 2026); DECISIONS §13.
- Audit: `docs/compliance/PRIVACY_PROCESSING_AUDIT.md`, the repository-safe copy of the v514-p-audit report.
- Sentence → evidence: `docs/legal/PRIVACY_NOTICE_SOURCES.md`.

## What was built

1. **A — privacy notice** and **B — cookie / technical-storage information**. Both are published legal documents in `apps/legal`'s own model and publication path, built from the verified processing only.
   - **Text files.** The Italian masters and the FR, EN and AR courtesy translations are `apps/legal/content/{privacy,cookies}/{it,fr,en,ar}.txt`.
   - **Translations.** Each one says that the Italian prevails, in its `notice` header. The document metadata flags them `translation_status = pending_legal_review`, which shows in the admin; the page shows that flag in the preview only.
   - **Arabic.** The texts use Western digits and U+200E after ™, as the interface catalogue does.
   - **GDPR content.** Controller, DPO (open), purposes, legal bases as verified, data categories, recipients, retention as configured, transfers (open), rights under arts. 15–22, complaint to the Garante, security measures, cookie and storage register.
2. **Model and service changes** (minimal; migration `legal/0002_verified_processing_documents`).
   - **New fields.** `LegalDocument.translations` (JSON), `translation_status`, `seed_checksum`; `LegalDocumentVersion.translations`, so each published snapshot keeps its translations.
   - **Categories.** `LEGAL_CATEGORY` gives A/B/C/D; `VERIFIED_PROCESSING_KINDS` is privacy and cookies.
   - **Open fields.** `open_fields()` and `open_field_ids()` find them. `is_available` is False when a text still has an open field, unless `ILE_LEGAL_OPEN_FIELDS_ALLOWED` is set.
   - **Checksum.** The translations are included only when present, so the C/D checksums are unchanged.
   - **Publication.** `legal.services.publish` refuses a document with an open field outside a preview. It snapshots the translations, and sets `effective_date` on the first publication of A or B.
   - **New service function.** `legal.services.document_available(kind)` is a per-document gate, cached and invalidated with the others.
   - **Settings.** `ILE_LEGAL_OPEN_FIELDS_ALLOWED`: `False` in `base.py`, `= DEBUG` in `dev.py` (preview), **forced `False` in `prod.py`** (a test loads prod settings with the env var set to 1 and still reads False).
   - **Seed.** `legal.verified_processing_drafts` (order 16, in `apps/legal/drafts.py`) writes A and B as **DRAFTS**. It never publishes, never touches C/D, never overwrites a published text or an editor's change (`seed_checksum`), and is idempotent.
   - **Rendering.** `apps/legal/rendering.py` turns the body into escaped blocks: `##` → h2, `###` → h3, `- ` → list item. An open field becomes `<mark class="legal-open-field">`. The cookie register is h3 + lists because the reading CSS has no table style, and that CSS is not this lane's.
   - **View and template** (`apps/legal/views.py`, `templates/legal/document.html`):
     - /it/ shows the master;
     - /fr/, /en/ and /ar/ show the translation, with its notice in the meta line and a link to the Italian (`hreflang="it"`);
     - the preview adds a notice listing the open OF ids (Italian, `dir="ltr"`);
     - an unpublished draft's title never reaches the page.
   - **Admin.** New columns for category, open-field count and translation status, and a read-only open-field list.
   - **`manage.py legal_publish <kinds> --by <e-mail>`.** It publishes through the same service and refusals as the admin action; the owner can use it on the server through `ile-manage`.
3. **Logging minimisation (LG-1)**, in `config/log_filters.py` and `base.py` `LOGGING`.
   - **What it does.** A filter on the `console` handler, plus redacting `plain` and `structured` formatters, remove e-mail addresses from every log line, message and traceback alike.
   - **What stays.** No logger was removed or lowered. `request_id` stays, as do the outbox pk and the exception class.
   - **Tests.** `tests/security/test_log_minimisation_v514_p.py` covers unit cases plus an end-to-end `deliver()` with `SMTPRecipientsRefused` through the configured handler.
4. **G1 is unchanged and now tested against A/B.** `all_official_pages_published` (G1) already required all five documents, so **no change to `apps/core/gates.py` was needed**. A test publishes A and B and asserts:
   - G1 stays closed;
   - G2 forms, the newsletter (flag on), the Virtual Forum (flag on) and sign-up stay closed;
   - C and D still show their blocked state;
   - A and B answer 200.

## Shared-file slices (outside this lane's whole files)

- `tests/conftest.py`, fixture `legal_published`: one line, `doc.translations = {}`. The fixture replaces the body with TEST text, and the seeded translations (which carry open fields) must go with it, or the fixture's publication is refused.
- `templates/legal/document.html`: the legal pages' template, here because the publication of A/B needs it. Lane C may touch it for Q2's «never show "in preparation"». My change is confined to the meta line, the body loop, the open-field notice and the Italian link. The `data-gate="legal-blocked"` branch is unchanged.
- `config/settings/dev.py` and `prod.py`: one setting each (`ILE_LEGAL_OPEN_FIELDS_ALLOWED`).
- The ownership manifest was **not** edited (steward's file). This lane's new files:
  - `apps/legal/{drafts,rendering}.py`
  - `apps/legal/content/**`
  - `apps/legal/management/**`
  - `apps/legal/migrations/0002_*`
  - `apps/legal/tests/{conftest,test_privacy_cookie_v514}.py`
  - `config/log_filters.py`
  - `tests/security/test_log_minimisation_v514_p.py`
  - `docs/compliance/PRIVACY_PROCESSING_AUDIT.md`
  - `docs/legal/PRIVACY_NOTICE_SOURCES.md`
  - this file

## Requests to other lanes

- **Lane D (`templates/partials/footer.html`)**
  - Link «Privacy Policy» and «Cookie Policy» only when `legal.services.document_available("privacy")` / `("cookies")` is true.
  - Drop «Mentions légales», «Conditions d'utilisation» and «Avertissement» while their `document_available(kind)` is false (directive §8: absent, not «work in progress").
  - Today `footer.html:19-23` links all five unconditionally (seen in the 1440 px capture).
  - When A is public, the footer is where every page reaches it.
- **Lane C (`apps/core/gates.py`, navigation, Q2 hide gates)**
  - Keep G1 = all five documents. Never reduce it to «privacy published».
  - If unpublished legal pages are to answer 404 (Q2), gate each route on `document_available(kind)`, not on G1. Privacy and cookies must stay reachable once they alone are published.
  - The `register_public_paths("legal", …)` call in `apps/legal/apps.py` can take a per-route gate. Tell this lane if you want it to make that change in `apps/legal`.
- **Whoever owns the orientation templates**
  - The orientation wizard (`templates/orientation/start.html`, `step.html`, `result.html`) is live, stores answers and an IP hash, and has no privacy link. Add one (`{% safe_url 'legal:privacy' %}`) per directive §1.
  - The forms, the login page, the forum note, the community join page and the portal already link it.
- **Runbook owner (R-4)**
  - Add `access_log off;` to the catch-all server block (or the masked `italylegalentry` format).
  - Keep the error log. When applied, drop the matching sentence in A §3.1 (it/fr/en/ar) and re-publish.
- **Whoever opens G2 (the forms)**
  - Before G1 can open, A needs a forms section: the 14 prescribed fields, OF-09 (one legal basis), the 24-month purge, and TG-1 for forum registrations.
  - The text says so (§3.8).

## Owner input (open fields; each blocks A in production)

- **OF-01** confirm the controller's data;
- **OF-02** hosting provider, region, DPA, sub-processors, transfers (CR-08);
- **OF-03** SMTP provider and the mailbox host;
- **OF-04** off-server backups;
- **OF-05** journald retention and confirmation of the 14-day logrotate on the server;
- **OF-06** retention of the security audit trail;
- **OF-07** retention per purpose (inactive accounts, documents, case files, messages, outbox);
- **OF-08** DPO;
- **OF-10** legal basis of the authenticated platform and of backups;
- **OF-12** recipient categories and roles.

Not in the text:

- **OF-09** the forms' basis (forms closed);
- **OF-11(a)** acceptance of the departures from the Annexe, which publishing does;
- **OF-11(b)** confirmation that the presentational sessionStorage keys are technical (non-blocking).

**B (cookies) has no open field: the owner can publish it now** (admin action or `legal_publish cookies --by …`).

## Verification

- **Tests (lane DB `test_ile_v5_l7`), targeted.**
  - `apps/legal/tests` (18), `tests/security/test_log_minimisation_v514_p.py` + `test_log_privacy.py` (14).
  - The regression suites around legal, gates, i18n, security, layout and notifications: see the commit message for the counts.
- **Browser (lane server 8787, `DATABASE_URL …/ile_v5_l7`, preview with A and B published via `legal_publish`; Chromium lock taken and released).**
  - Run: it/fr/en/ar × privacy/cookies × 1440/390.
  - Result:
    - horizontal overflow 0 everywhere;
    - `dir="rtl"` and the article `lang="ar"` on Arabic;
    - 13 highlighted open fields on A, 0 on B;
    - **zero requests to another origin**;
    - `document.cookie` empty (all HttpOnly);
    - no storage key written by these pages.
  - Captures: `C:/tmp/ile_v5_council/evidence/v514-privacy/screens/` (outside the repository).
- **Found and fixed in that pass:** the Italian preview notice was not isolated in RTL, so it now has `dir="ltr"`.

## Fix pass (label v514-p-fix) — the review's seven minors

- **B §3, back-office storage.**
  - `adminTheme` (unfold `app.js:167`, `Alpine.$persist(defaultTheme).as("adminTheme")`; `light`/`dark`/`auto`, until cleared, staff only) is added in it/fr/en/ar.
  - The §3 intro no longer says the values hold no identifier. They stay on the device and are never sent, but `commandHistory` holds what staff typed, for example a name or an e-mail address that was searched for.
  - New test `test_every_back_office_storage_key_of_the_installed_unfold_is_named_in_the_notice`: it reads every `localStorage`/`sessionStorage` key and every `$persist().as()` name from the installed unfold's `app.js` and requires each one in all four languages.
  - AUD §3 has new rows for `adminTheme` and `htmx-history-cache`. `htmx-history-cache` is not written today: htmx writes it only for `hx-push-url`, which unfold uses only in an inline with `per_page`, and no inline sets it. If one ever does, the key must be added to B.
- **A §3.2 and §7, abuse counters.**
  - The counters are also tied to an unsalted SHA-256 of the e-mail address entered (sign-in 5 min, recovery 1 h, address confirmation 10 min), and to the account for password and address changes (1 min).
  - The range is now 1 minute to 1 hour, in all four languages.
  - Evidence: allauth `core/internal/ratelimit.py:145-169` and `base.py:205-212`. AUD P7 and LG-4 are updated.
- **LOGGING, `django` logger.**
  - `LOGGING['loggers']['django'] = {"handlers": [], "level": "INFO", "propagate": True}` detaches Django's `DEFAULT_LOGGING` console and `mail_admins` handlers. Every `django.*` line now goes through the redacting root handler. This is AUD LG-8.
  - Test: `test_a_django_request_line_reaches_no_output_unredacted_under_debug`. It is checked to fail without the line.
  - `django.server` (runserver only) keeps its own handler. It never runs in production.
- **Editing a published text.**
  - `LegalDocument.save()`: if a PUBLISHED row's checksum changes (Italian text, title or translations) outside `publish()`, the row returns to DRAFT. `publish()` marks its own save as the publication.
  - The live text can therefore only change through `publish()`, which brings the permission check, the source check, the open-field check and a `LegalDocumentVersion` snapshot (A §11).
  - The back office warns: «Il testo pubblicato è stato modificato: è tornato in bozza…».
  - This applies to all five kinds, C/D included.
  - Tests: `test_editing_a_published_text_returns_it_to_draft_until_it_is_published_again` and `test_the_back_office_change_form_cannot_change_a_live_text`.
  - Not changed: anyone with change permission can still set `translation_status`. It is metadata and is never shown in production.
- **DENY tests.**
  - The prod-settings subprocess test now fails instead of skipping. It no longer passes the meaningless `ILE_LEGAL_OPEN_FIELDS_ALLOWED` variable, and it asserts `[False, False]` (switch, DEBUG) with `DJANGO_DEBUG=1`.
  - New HTTP test `test_production_serves_the_blocked_notice_for_a_published_row_with_open_fields[it|ar]`: a PUBLISHED row with open fields renders `data-gate="legal-blocked"` in `<main>`, with no «DA COMPLETARE», no OF id and none of the body's headings.
- **csrftoken.** «Quando viene impostato» now adds that, once signed in, the sign-out button is also a form, so the cookie is set on every page (it/fr/en/ar).
- **Requests to other lanes.** See the extension below.

### Requests to other lanes — extension (directive §1: the notice reachable wherever personal data is collected)

Every page that extends `base.html` reaches A through the footer once lane D applies R-1. Directive §1 also asks for a link at the point of collection, in these places:

- **allauth templates (`templates/account/login.html`, `templates/allauth/layouts/entrance.html`)**
  - The sign-in page links A only inside `{% if gates.phase3_public %}` (`login.html:22-26`). It should link it whenever `safe_url 'legal:privacy'` resolves.
  - The password-reset pages (request and from-key, both on the entrance layout) have no link. Add one beside the form.
- **Accounts (`templates/accounts/profile.html`, `delete_request.html`, the export form in `profile.html`, and `allauth/layouts/manage.html`)**
  - Link A from the personal-data paragraph (`profile.html:16`) and from the export and deletion screens.
- **Documents (`templates/documents/partials/depot.html`)**
  - The upload stores the file, its name, type, size, a hash and the IP hash, and may hold identity documents.
  - `base_portal.html:69` has a foot link, but nothing sits by the upload control. Add one.
- **Helpdesk (`templates/helpdesk/open_request.html`)**
  - The request form collects free text. The portal foot link exists (`base_portal.html:69`), but nothing sits by the form. Add one.
- **Gate G1 (lane C), unchanged requirement.** Every form that depends on Allegato 1 (G2 forms, sign-up, newsletter, Virtual Forum) stays closed while A and B alone are public.
  - `test_privacy_and_cookies_public_keep_every_allegato_1_flow_closed` pins this.

### Verification (fix pass, lane l7)

- `apps/legal` passes 24 of 24.
- These suites pass 75 of 75: `tests/security/test_log_minimisation_v514_p.py`, `tests/backoffice/test_backoffice.py`, `tests/compliance/test_gates.py`, `test_public_pages.py`, `test_locked_content.py`, `test_no_personal_data_in_repository.py`, `tests/security/test_production_settings_refuse_to_start.py`.
- No browser pass: the text changes are inside existing sections, and the HTTP tests render B in all four languages.
