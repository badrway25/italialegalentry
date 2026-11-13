# V5.20 · the WhatsApp number out of the public repository — option B (label v520-wa)

30 October 2026 · branch `v520-wa` from design-v5 `e2098dd` (`v518/green`, DL54-179) · worktree `C:/tmp/ile_wt/v520-wa`
· database lane l6 (`test_ile_v5_l6` for pytest, `ile_v5_l6` for the lane server on 8786) · binding: V5.20 (the strict
test-update rule; the final technical gate), V5.19 (the owner-confirmed channels), the confidential-material policy
(`docs/security/CONFIDENTIAL_MATERIAL_POLICY.md`, `tests/security/test_confidential_material.py`).

**Why.** With the private sentinel table configured (`ILE_CONFIDENTIAL_SENTINELS`), the confidential-material guard
failed on design-v5: the owner-confirmed WhatsApp number is one of the table's rows (a private mobile number), and lane
K had written it in code, a migration, tests and documents. The owner was asked to choose A (publish it in the
repository and update his table) or B (no copy in the repository: database and environment only; the site still
shows it). No answer yet, so B is applied, as the orchestrator ordered.

**Result.** No tracked file holds the number in any form. The site shows exactly what V5.19 asks wherever the number is
configured: the channel, `https://wa.me/` followed by the digits, the label «+39», then 3-3-4, in four languages. In
this note it is «the owner-confirmed WhatsApp number (configured outside the repository, V5.19/V5.20)»; this note and
this branch never write it.

## 1. Where the number lives now

| Place | What it holds | Tracked? |
|---|---|---|
| `core.models.SiteSettings.whatsapp_number` (database, back office «Contatti e versione») | the canonical value, as before | no (data) |
| `settings.ILE["WHATSAPP_NUMBER"]` = `env("ILE_WHATSAPP_NUMBER", default="")` (`config/settings/base.py`) | the default of a new settings row, and the fallback before migrations; blank unless the environment sets it | the line, not a value |
| `core.contact.default_whatsapp_number()` | the field's default, a callable that reads the setting when a row is made | code, no value |
| migration `core/0003_public_telephone_channels` | AddField with `default=""`, then the data step copies `settings.ILE["WHATSAPP_NUMBER"]` into a row holding none **when it is set**, then AlterField to the callable default | code, no value |
| the server's environment file (`ILE_WHATSAPP_NUMBER=`, `docs/deployment/production.env.example`) | filled by the owner, on the server | the template line, empty |
| `C:/tmp/ile_wt/v5-live/.env` (the preview's; gitignored, untracked — checked with `git check-ignore`) | the value, canonical form (+39 then the digits), written in-process from the V5.19 directive | no |
| `ile_v5` (the preview's database) | the value, already there since the v519-k merge — left as it is | no |

**One deviation from the letter, and why.** The order said the migration's WhatsApp default «becomes ""». It does, in
the AddField. But the model's default has to come from the environment, and Django compares the model with the
migration state: a model default read from the environment at import (lane K's `default=settings.ILE[…]`) would make
`makemigrations --check` dirty on every machine where `ILE_WHATSAPP_NUMBER` is set, and a `makemigrations` run there
would write the number into a new migration file. So the field's default is the callable `default_whatsapp_number`,
and 0003 ends with an AlterField to that same callable. `sqlmigrate core 0003` shows the AlterField as a no-op. The
migration is still local and unpublished, so 0003 was edited in place: `ile_v5` (0003 applied, the value in its row)
is untouched, and a database that has not applied 0003 yet (`ile_v5_l6`) took the value from the environment through
the data step.

**The Numero Verde** 800 642 015 is a public toll-free business number and is not in the private table. It stays as
configured: `settings.ILE["FREEPHONE_NUMBER"]`, the field's literal default, the migration's literal.

## 2. One template line — the channel is not announced when it is withdrawn

With nothing configured (a fresh clone, CI, a server before the owner sets the number), the WhatsApp channel is
withdrawn. But the contact page's chapter would still have been titled «Par téléphone et WhatsApp». The title now
names the channels the settings hold (`templates/pages/contact.html`):

- both channels: «Par téléphone et WhatsApp»;
- the Numero Verde alone: «Téléphone»;
- WhatsApp alone: «WhatsApp».

Only existing catalogue messages are used, so there is no new msgid and no translation. «Téléphone» is already
translated in the four catalogues (Telefono / Telephone / الهاتف). The chapter's mark is chosen by its anchor, which is
unchanged. When the number is configured, as in the preview, nothing on the page changes.

## 3. Tests — each change under the V5.20 rule

The rule's four conditions hold for every change below:

1. The old expectations spelt the owner's number, which conflicts with the owner's standing rule that the depositant's
   private identifiers enter no tracked file (the confidential-material policy, and the private table that implements
   it). Option B is applied while the owner's answer is awaited.
2. The new behaviour is implemented on purpose: the number comes from the environment and the back office.
3. Each test protects the same invariant or a stronger one.
4. The reason is cited in each test's docstring or comment.

The fictional number is Ofcom's drama-reserved UK mobile **+44 7700 900123**. The range 07700 900000–900999 is never
assigned to a subscriber. Its label, «+44 770 090 0123», has 16 characters, as the owner's has, so the layout tests
measure the same line length.

| Test | Before | Now |
|---|---|---|
| `tests/conftest.py` — new fixture `whatsapp_channel` | — | Configures the fictional number in both places the site reads: `settings.ILE` and the SiteSettings row, whatever the machine's environment holds. Returns core.contact's channel. |
| `tests/conftest.py::whatsapp_link_set_aside` (a071a9b) | read `public_channels()` (the settings) | Reads the **configured** channel, `public_channels(SiteSettings.load())`, which is what the context processor draws. Still only `<a href>` to exactly that URL; the same URL as a source, and any other external URL, still fail. With nothing configured, nothing is set aside. |
| `test_contact_channels_v519.py` — canonical values, separators, malformed input, four-language names, footer and sheet, Arabic order, obsolete numbers, blank withdraws | the owner's number | The same assertions on the fictional number. `test_the_canonical_channels` also checks the settings fallback. `test_a_blank_setting_withdraws_its_channel` first proves the channel is drawn, then that the back office's blank wins over the environment's default (stronger). |
| `…::test_an_italian_mobile_reads_plus_39_then_three_three_four` (new) | the Italian 3-3-4 rule was proved only through the owner's number | The rule is proved on digits that no numbering plan assigns: «+39 000 000 0000». |
| `…::test_the_settings_hold_the_configured_numbers` (was `…_confirmed_numbers`) | the row held the owner's number | A new row takes the Numero Verde and the environment's number. With the environment blank, it takes none and the channel is withdrawn. Two cases. |
| `…::test_no_whatsapp_number_is_written_in_the_settings_or_the_migration` (new) | — | `settings.ILE["WHATSAPP_NUMBER"]` equals the environment's value (blank when unset). Neither `base.py` nor migration 0003 writes an international number or a `wa.me/<digits>` link. |
| `…::test_the_migration_copies_the_environments_number_into_a_blank_row` (new) | — | The data step leaves a blank row blank when nothing is configured. It copies the configured number into a blank row. It never overwrites a number held in the back office. |
| `…::test_no_template_writes_a_number` | looked for the freephone forms, the owner's number and `wa.me/39` | Looks for the freephone forms, any `wa.me/`, any `tel:+` and any international number in any grouping (a `+`, then at least nine digits and separators: spaces, NBSP, dots, brackets, slashes or dashes). This is stronger: it covers the owner's number in every form, and any other. |
| `…::test_the_guards_set_aside_the_configured_whatsapp_link_only_as_a_link` (new) | — | The helper sets aside the link and nothing else: not the same URL as an image source, not another wa.me number. With the row blank, nothing is set aside. |
| `…::test_with_nothing_configured_the_whatsapp_channel_is_absent_everywhere` (new, ×4 languages) | — | `ILE_WHATSAPP_NUMBER` blank and the row blank. On `/`, `/contact/`, `/le-projet/` and `/agami/`, every page answers 200 and **is never skipped**. No page has a `wa.me` link, a `tel:+` link, the glyph, the plate or the word «WhatsApp». The Numero Verde stays in the footer and the sheet, and the chapter is titled «Téléphone» in that language. |
| `…::test_the_configured_whatsapp_number_is_the_one_the_contact_page_links` (new, environment-bound) | — | Modelled on `test_the_depositants_private_identifiers_are_checked`. It reads `ILE_WHATSAPP_NUMBER` and asserts that `/fr/contact/` and `/ar/contact/` link exactly `https://wa.me/<its digits>`, once in the page body, that the label has the owner's grouping inside the LTR isolate, and that the accessible name is the channel's. It also checks that a new settings row holds the environment's value. **SKIPPED with its reason only where the variable is unset.** A set but malformed value FAILS. No assertion message prints the number. |
| `test_institutional.py::test_contact_page_single_address_…` | the owner's URL and label | The configured channel's URL and label. Still no other number on the page. |
| `tests/frontend/test_layout.py::_external_urls` | admitted the owner's URL **in any attribute** (src, href, content, action) | Uses the conftest helper, which admits it only as `<a href>`. This is stronger. `test_no_external_resources_or_inline_styles` runs with the channel configured, so the rule is exercised. |
| `tests/compliance/test_public_pages.py::test_no_external_scripts_fonts_or_images` | read the settings' channel | Uses the same helper on the configured fictional channel, so the link is drawn and set aside wherever the suite runs. |
| `tests/frontend/test_browser_contact_channels_v519.py` | `HREFS` named the owner's URL | The hrefs come from the configured channel. The 44 px targets, one line, LTR order and 390/360 × fr/ar measures are unchanged. |

Skips: the environment-bound test above is skipped in CI and on a fresh clone, as the private-table test is. That is
genuinely environment-bound, and the skip states its reason. The four `/xx/faq/` cases of
`test_no_obsolete_number_on_a_public_page` (FAQ gated in the test database) were left as they were. They are item 5 of
the gate, not this lane's.

## 4. The repository's documents

The sentences that wrote the number now say «the owner-confirmed WhatsApp number (configured outside the repository,
V5.19/V5.20)», or «il numero … confermato dal proprietario (configurato fuori dal repository, V5.19/V5.20)» in the
Italian files:

- `DECISION_LOG_V54.md`: DL54-176's index row and item 1. Item 2 now says the review copy was redacted at V5.20.
- `CHANGELOG_V54.md`: v519/contact.
- `live_status.json`: the v519-k title.
- `OWNERSHIP_V54.json`: v519-k's title and its 37 identical slice descriptions.
- `QA/v519-k/NOTES.md` and `QA/v54/v519-k/REVIEW.md`: each now opens with a one-line redaction note. The review is
  still byte for byte the original, except its three sentences that quoted the number.

`QA/v518g/*` holds no form of the number (scanned), so it was not changed.

Three of these files are steward-only in the ownership manifest: `live_status.json`, `CHANGELOG_V54.md` and
`OWNERSHIP_V54.json`. They were edited here by the orchestrator's explicit order, and only to redact the number. At the
merge, `check_ownership.py` will report them as STEWARD-ONLY, and the steward reads and accepts those lines. No family
entry was added for `v520-wa`: that is the steward's to record.

Deployment:

- `.env.example` declares `ILE_WHATSAPP_NUMBER=` (empty, its default) with the comment the completeness test asks for.
- `docs/deployment/production.env.example` declares the same, under a new «public contact channels» section, filled
  on the server.
- Checklist A-30 (PRODUCTION_CONFIG_COMPLETE) has one clause, plus one evidence command:
  `curl … /it/contact/ | grep -o 'https://wa.me/[0-9]*'`.
- The runbook's PRODUCTION_CONFIG_COMPLETE state has one clause.

## 5. Verification

All on lane l6. The separator-tolerant scan reads the values in-process from the private table and from the V5.19
directive, and prints counts only.

- **Separator-tolerant scan, every tracked file** (and every untracked file that is not ignored). It looks for the
  digits of each value of the private table, with any run of separators between them (spaces, NBSP, dots, dashes,
  brackets, slashes, plus); with and without the country code; each row's pattern as a regular expression and as
  literal source text.
  - Result: **0 hits** for every row.
  - Partial runs: no 6-digit or longer run of the number's digits in any file.
- **`tests/security/test_confidential_material.py`** with `ILE_CONFIDENTIAL_SENTINELS` naming the private table:
  **17 passed, 0 failed, 0 skipped**. That includes `test_no_sentinel_text_in_tracked_files` and
  `test_the_depositants_private_identifiers_are_checked`. Before this branch, the guard failed on the number.
- **`makemigrations --check`**: «No changes detected», both with `ILE_WHATSAPP_NUMBER` unset and with it set to the
  fictional number.
- **`sqlmigrate core 0003`**: the AlterField is a no-op.
- **`manage.py check`**: no issues.
- **`ruff check .`**: all checks passed.
- **Targeted pytest** (`test_contact_channels_v519`, `test_institutional`, `test_layout`, `tests/compliance/test_public_pages`):
  - unset: 133 passed, 5 skipped (4 `/xx/faq/`, plus the environment-bound test, with its reason);
  - with `ILE_WHATSAPP_NUMBER` set in-process to the owner's value: `test_contact_channels_v519` 51 passed, 4 skipped
    (`/xx/faq/`), so the environment-bound test ran and passed;
  - with a malformed value: the environment-bound test FAILS («is set but is not an international number»);
  - with the fictional value: it passes (the other-country grouping).
- `tests/test_env_example_is_complete.py`, `tests/deployment/test_runbook_matches_the_code.py`,
  `tests/test_check_ownership.py`, `tests/frontend/test_design_docs.py` and the confidential guard: **190 passed**.
- **The preview path.** The lane server on 127.0.0.1:8786 was started from this worktree on `ile_v5_l6`, with
  `ILE_WHATSAPP_NUMBER` set in-process. `migrate` applied 0003 there, and the row took the owner's value through the
  data step. On `/fr/contact/`, `/fr/`, `/ar/contact/` and `/ar/`:
  - every page answered 200;
  - the only wa.me link on each page is the owner's exact URL;
  - the footer and the sheet draw both channels;
  - the contact page draws each plate once, with the owner's grouping inside `<bdi dir="ltr">`;
  - the Arabic pages are `dir="rtl"`.
  - Result: **PASS**.
  - Headless Chromium on the same server, holding `CHROMIUM_LOCK` (label `v520-wa`, 07:02–07:27), at 390 and 360 px
    in fr and ar, on the contact page's plates, the footer's links and the phone sheet's plates. Each link has exactly
    the two hrefs (`tel:800642015` and the owner's wa.me URL) and is at least 44 × 44 px. Each number is on one line,
    with computed `direction: ltr`, its first character drawn left of its last, and the owner's grouping. No page
    scrolls horizontally. Result: **PASS** in all four cases.
- **Browser files** (same lock, `test_ile_v5_l6`, `-p no:randomly`):
  - `test_browser_contact_channels_v519` (on the fictional channel), `test_browser_w2_c2` (the sheet),
    `tests/i18n/test_rtl_browser_w2_c2` and `test_mobile_rtl_w4_a`: **80 passed**;
  - the contact and footer pages' browser files — `apps/pages/tests/test_browser`, `test_content_pages_browser_w3_f2`,
    `tests/i18n/test_rtl_browser` and `test_browser_w1_c`: **73 passed**.
  - With WhatsApp unconfigured by default, the sheet and the footer hold one channel less. None of these files
    depended on the second one.
- `scripts/i18n_audit.py` (report): exit 0. The template's new use of «Téléphone» is an existing, translated msgid.
- **Full non-browser suite** on `1f600d7` (`-m "not browser" -p no:randomly --create-db`, `test_ile_v5_l6`, the
  private table configured, `ILE_WHATSAPP_NUMBER` unset; 07:27–08:46): **6 425 passed, 0 failed, 0 errors,
  8 skipped, 2 xfailed** (640 browser tests deselected).
  - The 8 skips: the 3 intake «no rule in force» skips and the 4 `/xx/faq/` skips, both gate item 5 and unchanged;
    and the environment-bound WhatsApp test, with its reason.
  - The private-table test is no longer among the skips: it ran and passed.
  - The log and the junit record hold no form of the number.
- After the follow-up commit (the template guard widened to any international number, line wraps in the redacted
  documents), the channel tests, the confidential guard, the design-docs, ownership, env-example and runbook tests
  were re-run on the final tree: **240 passed, 5 skipped** (the 4 `/xx/faq/` and the environment-bound test).

## 6. Left for others, and the history

- **The owner's answer (A or B) is still open.** Under A, the number would go back into the repository, and the owner
  would update his table: restore the setting's literal and the tests' constants. Nothing else here depends on B.
- **Production.** The owner sets `ILE_WHATSAPP_NUMBER` in the server's environment file before the first request, or
  types the number in the back office (checklist A-30). Until then, the site shows the Numero Verde alone, under
  «Téléphone».
- **History.** The local history still holds the number in lane K's commits on design-v5: four diffs, from 9dc75f6 to
  the v519-k merge record, and two commit messages. None of them was ever published:
  - GitHub's design-v5 is the 28 October snapshot `0a9373e`; main is `a3ac318`. Both were scanned the same way:
    **0 hits**.
  - Publication goes by a snapshot of a tree (`git commit-tree`), so a snapshot of this branch's tree carries none of
    the number.
  - The standing rule holds: the local history is never pushed.
