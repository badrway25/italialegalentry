# V5.12 lane D, wave W2 (label `v512-d-w2`): notes

- **Branch:** `v512-d-w2`, built on `design-v5` at `6251475` (v512 W1 merged).
- **Worktree:** `C:/tmp/ile_wt/v512-d`. **Database lane:** l6. **Lane server:** 8786 (stopped at the end).
- **Scope:** the lane D items of the W2 row in DECISIONS.md — the organisation rails and the organisation space (Q7),
  the console foot, the empty-wall collapse, the allauth string catalogues — plus §14's carry-over (the two failing
  browser tests of `test_design_preview.py`) and §13's footer work (the privacy notice and the cookie information
  linked once published, the unpublished legal pages absent).
- **Owner answers.** DECISIONS §12–§13 hold the owner's binding answers to Q1–Q8 (28 Oct, 11:35) and the privacy
  correction (14:42); they replace the defaults the task text quoted. This wave applies them: **Q7's default is
  rejected**, so the organisations get a designed space, not a minimal bridge; Q2/§13 for the footer; Q3 for the
  EN/AR labels (provisional, flagged in `docs/I18N_RTL.md` §5).

## What changed, and what the owner sees

### Q7 · The organisation space (institution, university, training body)

An institution, a university or a training body now has its **own space**, not the person's console with modules
removed. Who counts is `accounts.roles.audience_role` (the project's team first, then the roles, then the type):
`portal.services.organisation_audience()` → `institution` / `university` (a training body works in the universities'
space, S1 §3.5).

| Where | What the owner sees |
|---|---|
| Rail head | «Espace Institutions / Area Istituzioni / Institutions Area / فضاء المؤسسات», «Espace Universités et Formation / Area Università e Formazione / Universities and Training Area / فضاء الجامعات والتكوين» — the public spaces' own names (S1 §3.4, §3.5), already in the four catalogues |
| Rail | «Tableau de bord» (the ungrouped first row) · **Coopération**: «Mon organisation», «Mes demandes», «Mes échéances» (only once the team has set a date for the account) · **Échanges**: «Communications». No «Ma situation», «Mon parcours», «Mes dossiers», «Mes documents», «Guichet numérique», Academy |
| Bottom bar (phone) | dashboard, organisation, requests, communications; «Mon organisation» is the one that leaves first where four words and «Menu» do not hold |
| Dashboard | eyebrow = the space; title «Tableau de bord»; the organisation's name; the space's **locked** presentation (`p3.institutions.intro` / `p3.universities.intro`, through `{% locked %}`, French fallback marked `lang="fr"`). Main column: the registers that have rows only (dates, communications, requests); with none, one calm sentence («Aucune action ne vous est demandée pour l’instant.», an existing msgid) and — **only while the public form is open (G2)** — the approved CTA «PROPOSEZ UNE COLLABORATION» / «COLLABOREZ AVEC NOUS» (locked `p3.entrances.*.button`). Then **«Le projet»**: the public pages the role works with (its own public space, the training for a university, the pilot project, the regular pathways, the Forum), each only while its page is public (`core.links.public_url`), two columns from 48 rem, glyph on a disc that takes the accent on hover/focus. Side: the **identity sheet** — the organisation's audience on a disc, its name, nature, city, country, the account's role, since when |
| «Mon organisation» (`/espace-reserve/mon-organisation/`, new) | the identity sheet of each organisation (with its website when it has one), the documents its members filed for it (for its responsible only: `organisation_documents_for`), «Le projet», the account's links |
| Person's pages | «Ma situation», «Mon parcours», «Dossiers» redirect to the dashboard; «Mes documents» redirects to «Mon organisation». An institution is never asked its date of birth |
| Loader | the space has its own key, `organisation`: its first console page lights once (lane A's request, §14; no template change) |

No CTA or promise for a capability that is not implemented: no convention workspace, no Forum governance (gated by
the virtual Forum, Q6), no collaboration CTA while G2 is closed. Page-only sheet: `apps/portal/static/portal/organisation.css`
→ `static/css/dist/portal/organisation.css` (**3.7 KB min**), linked by the two organisation pages only.

### D-08 / D-09 / D-22 · A company's «Espace réservé»

- The company's rail in «Espace réservé» no longer offers «Ma situation», «Mon parcours», «Mes dossiers»; those routes
  send it to its dashboard. «Tableau de bord» is the ungrouped first row (the «Parcours» section would hold it alone).
- An account named by the company's role is no longer a «person» for the dashboard (`is_person_account`), whatever its
  type defaults to: the preview's company account (typed person) no longer gets the person's NowPanel «Commencer
  l’orientation». It gets the bridge, headed by its way to «Espace entreprise».

### §8 · The Academy entry

`portal.services.academy_open()`: the Academy is a page of the rail only while a course is published, or when the
account already holds an enrolment. Where demonstration data is off (production) and nothing reviewed is published,
the entry is absent. The preview (demonstration data on) is unchanged.

### D-20 · The empty-state wall

The bridge (company, professional) draws a register only with rows, an action of its own (the orientation's start
for a professional), or when it cannot be read; the organisation card always stands. With nothing under way: one calm
sentence. No heading over «… apparaîtront ici» remains on any dashboard.

### D-16 · The console foot (new partial, include by lane A)

`templates/portal/partials/console_foot.html`: the promoter line «AGAMI — Dialogo Giuridico Interculturale APS —
promoteur du projet», the **locked** statement «Italy Legal Entry ne délivre pas de visas, de permis de séjour ni
d’autorisations : ces décisions relèvent exclusivement des autorités compétentes.» (the first sentence of
`p3.persons.intro`, cut at its first full stop by `portal.templatetags.console_foot.locked_sentence`, never retyped;
`lang="fr"` outside French), the **published** legal pages only, and the contact address as a mail link. It is the
whole `<footer>`; it shows once lane A replaces the inline footer of `portal/base_portal.html` (see requests).

### Q2 / V5.14 §13 / D-24 · The public footer

- «Informations légales» lists only the legal pages that are **published** (`legal.templatetags.legal_links`): the
  privacy notice and the cookie information as soon as lane P's documents are published, the official notices, terms
  and disclaimer only with their verified Italian source. Lane P's per-document gate
  `legal.services.document_available` is used where it exists; until it is merged, one cached query (dropped on every
  save/delete of a legal document). With no published page the column leaves (`site-footer__inner--three`).
- The fraud link says the glossary's word, «Attention aux fraudes / Attenzione alle frodi / Beware of fraud /
  احذروا الاحتيال»; the locked heading stays on the section itself.

### D-11 · The account pages speak the glossary (allauth string catalogues)

`apps/accounts/allauth_terms.py` declares, with `gettext_noop`, the allauth msgids the entrance and the account pages
show (and Django's four password-validator sentences); the project catalogues translate them, and `LOCALE_PATHS` wins
over allauth's and Django's catalogues. Measured on 8786:

| Page | Before (fr / it / en / ar) | After |
|---|---|---|
| Login title / button | Connexion · Accedi · Sign In · تسجيل الدخول | **Se connecter** · Accedi · **Sign in** · تسجيل الدخول |
| Login → sign-up line | «Si vous n'avez pas encore créé de compte, merci de vous enregistrer au préalable.» | «Vous n’avez pas encore de compte ? **Créer un compte**» · «Non ha ancora un account? Crea un account» · «No account yet? Create an account» · «ليس لديكم حساب بعد؟ إنشاء حساب» |
| Sign-up title | Création de compte · Registrazione · **Sign Up** · **الاشتراك** | **Créer un compte · Crea un account · Create an account · إنشاء حساب** |
| E-mail field | **Courriel** · Email · Email · بريد إلكتروني | **Adresse e-mail · Indirizzo e-mail · E-mail address · البريد الإلكتروني** |
| Password rules (it) | «La **tua** password …» | «La password non deve …» (Lei's register) |
| Reset page | «Reset My Password», «Password Reset» | «Réinitialiser le mot de passe», «Reset the password», «Password reset» … |

Lane B overrides the allauth templates with project msgids in W2 (DECISIONS lane B); these catalogue entries cover
whatever allauth still draws (form labels, messages, the account pages B does not rewrite). The en/ar msgstr of
«Adresse e-mail» moved to the binding «E-mail address» / «البريد الإلكتروني» (DECISIONS §9).

### Carry-over (§14) · The two failing browser tests of `test_design_preview.py`

Root cause: W1's rename was half done. `static/js/dev/designpreview.js` still titled the window «… · V5 dal vivo ·
…», and the strip's «di accettazione» was `display: none` below 120 rem, so the home link's accessible name read
«Italy Legal Entry™ — Anteprima» between 48 and 120 rem. Fix: the JS title says «Anteprima di accettazione»; the claim
leaves the eye the way «Italy Legal Entry™ — » does (a 1 px clipped box), never the link's name. The test now asks for
the full name «Italy Legal Entry™ — Anteprima di accettazione» (the guard is unchanged: the words leave the eye, never
the name). Dev-only sheet: +0.2 KB in `static/css/dev/designpreview.css`.

## Checked on 8786 (lane DB `ile_v5_l6`)

- Two synthetic organisation accounts were added to the **lane** database by a script outside the repository
  (`C:/tmp/ile_v5_council/.work/v512-d-w2/seed_l6_orgs.py`: qa-institution, qa-university, each with an owner
  membership; one team message for the university), and the two personas were added to the switch at runtime by the
  lane launcher (`.work/v512-d-w2/srv/run_8786.py`, as `run_8780.py` does). Nothing in the repository.
- **HTTP crawl** (`.work/v512-d-w2/crawl.py`): 5 accounts × 4 languages × 8 console pages. Organisation rails exactly
  `dashboard, organisation, requests, messages`; the space names in the four languages; the person's pages redirect;
  0 non-200 answers. The only «fixture» word left is the `qa-…@example.test` address in the account line (the
  switch's allow-list, known since W1).
- **Chromium** (lock taken and released each time), shots in `C:/tmp/ile_v5_council/.work/v512-d-w2/shots/`:
  institution / university dashboards fr+it 1440, ar+fr 390 with reduced motion; «Mon organisation» fr 1440 and ar
  390; company dashboard fr+it 1440; login fr; footer fr 1440 and ar 390; sign-up ar 390; the hub strip at 1280 and
  900. **Horizontal overflow at 390: 0 px** on every organisation page in ar and fr and on the Arabic sign-up.
- The account line's e-mail address is now isolated LTR (`class="email" dir="ltr"`): in Arabic it read «qa- · …».

## Budgets

- Shared CSS/JS: **unchanged** (`main.css`, `console.css`, `shell.js` untouched). `npm run build:css` rewrote no other
  dist file.
- Page-only: `css/dist/portal/organisation.css` **3.7 KB** (2 pages).
- Dev-only: `static/css/dev/designpreview.css` +0.2 KB.
- No new npm dependency, no JS added to the product.

## Tests (targeted, `TEST_DATABASE_URL=…/test_ile_v5_l6`)

- **New:** `tests/frontend/test_organisation_space_v512_d.py`, **46 tests**, all pass — the organisation space in four
  languages (space name, rail, no person's key), the space key, the dates entry, the redirects, the composed
  dashboard (locked lead, no person's words, the identity sheet, the calm line), the CTA closed with G2 and shown with
  it, a register drawn only with rows, the public references, «Mon organisation», the company's rail and redirects,
  the bridge without the wall, the Academy gate both ways, the console foot (promoter, the locked sentence cut from the
  locked text, published links only), the footer's legal links both ways and per document, the fraud link's word in
  four languages, the entrance in the glossary's words in four languages, every allauth term translated.
- **Stale tests brought to the new behaviour, same guards:**
  - `test_design_preview` (carry-over: the home link's full name);
  - `apps/portal/tests/test_navigation_reaches_every_surface.py`, `tests/frontend/test_console_shell_w3_a.py`,
    `tests/frontend/test_icons.py` — read the rail with a published course (`academy_open` patched to True, the
    other side is in the new file); the company's rail without the person's pages and their redirects;
  - `apps/portal/tests/test_security.py` — the new route `organisation` in the anonymous sample;
  - `tests/frontend/test_dashboard_w3_b.py` — the bridge keeps a register only with rows; the institution's own
    dashboard; the empty university says one calm line, never «… apparaîtront ici»;
  - `tests/frontend/test_layout.py`, `tests/i18n/test_ui_translations.py`, `tests/compliance/test_public_pages.py` —
    the five legal links are asserted with the five pages published (`legal_published`);
  - `apps/accounts/tests/test_login_form_w2_b.py` — «Se connecter» in the title, «Adresse e-mail» in the summary;
  - `tests/frontend/test_console_phone_browser_w3_a.py` (browser) — the long-name drawer test gives the account a
    long NAME (W1: an account without a name reads «Mon compte», never its e-mail).
- **Runs** (one pytest at a time on l6; browser runs under the Chromium lock):
  - Ring 1, non-browser: `apps/{portal,cases,accounts,legal,companies,academy,designpreview}`, `tests/i18n`,
    `test_console_shell_w3_a`, `test_icons`, `test_o14_lint`, `test_layout`, `test_terminology_v512_d`,
    `test_dashboard_w3_b`, `test_overlays`, `test_static_pipeline`, `test_console_shell_stylesheets`,
    `test_loader_rules`, `test_lume_v512_a`: first **1385 passed, 23 failed** (the stale tests above), then the
    failing files + the new file: **431 passed, 2 failed** → the last two fixed: **8 passed**.
  - Ring 2, non-browser: `tests/compliance`, `test_entrance_form_w2_b`, `test_entrance_w2_b`,
    `test_content_pages_w3_f2`, `test_cms_nav`, `test_mobile_rtl_w4_a`, `test_overlays_console_w2_a`,
    `test_documents_w3_c`, `test_case_file_w3_e`, `apps/{helpdesk,selection,documents,enquiries,core}`:
    **664 passed, 3 failed** → `test_public_pages` fixed (9 passed on a fresh test database); the other two fail
    identically on `design-v5` HEAD without this branch (see «Not mine» below).
  - Browser: `test_design_preview.py` + `test_console_phone_browser_w3_a.py`: **43 passed, 3 failed** → the two
    long-name tests fixed (**2 passed**); the third fails on the base (below). The two §14 carry-over tests: **2 passed**.
- **Other checks:** `scripts/i18n_audit.py` OK, 100 % in it/en/ar/fr; `ruff check` and `ruff format --check` clean on
  every touched Python file; no model change (no migration).
- **Not mine, failing on `design-v5` HEAD `6251475` as well** (run there on l6, unchanged):
  `tests/frontend/test_cms_nav.py::test_portico_gives_every_door_its_panel_from_live_content` (expects «Actualités»,
  which C's W1 news gate hides), `tests/frontend/test_mobile_rtl_w4_a.py::test_the_500_keeps_its_semicolon_with_its_words`
  (the 500 page renders its bare fallback without a database) and the browser
  `test_console_phone_browser_w3_a.py::test_arabic_mirrors_the_chrome_and_never_the_mark` (`.console-bar__tile img`
  is gone since A's W1 loader). For the steward's W2 merge (§14).
- **Note for the steward:** midway, the test database `test_ile_v5_l6` held a column of lane P's legal migration
  (`seed_checksum`), so a reused database failed with `IntegrityError`; `--create-db` cleared it. Another run may have
  used l6's test database.

## New msgids (lane D's catalogue pass, done in this branch)

| msgid | it | en | ar |
|---|---|---|---|
| Coopération | Cooperazione | Cooperation | التعاون |
| 24 allauth / Django msgids (`apps/accounts/allauth_terms.py`) | see the table above | | |

Changed msgstr: «Adresse e-mail» en «E-mail address», ar «البريد الإلكتروني». Glossary rows added (§5, provisional
note): «Adresse e-mail», «Mot de passe», «Espace Institutions», «Coopération». `scripts/i18n_audit.py`: OK, 100 % in
the four languages; the `.mo` recompiled.

## Requests to other lanes and the orchestrator

- **A** (`templates/portal/base_portal.html`): replace the inline `<footer class="portal-footer console__footer">…</footer>`
  of `{% block site_footer %}` with `{% include "portal/partials/console_foot.html" %}`. Until then the console foot
  still links the unpublished Privacy / Conditions / Avertissement pages. Optional: a rule giving
  `.portal-footer__statement` its own row (`flex-basis: 100%`) — it already wraps on its own at every width measured.
- **A / steward** (`static/css/v5/chrome.css`, shared): `@media (min-width: 64rem) { .site-footer__inner--three {
  grid-template-columns: 1.4fr 1fr 1fr; } }` — while no legal page is published the footer has three columns, and the
  fourth track of `1.4fr 1fr 1fr 1.2fr` stays empty. (+≈70 bytes to a shared sheet; I did not touch it.)
- **B** (`apps/core/icons.py`, registry): register `ORGANISATION_NAV` = `{"dashboard": "layout-dashboard",
  "organisation": AUDIENCE[audience], "requests": "send", "deadlines": "calendar-clock", "messages": "mail"}` and the
  «Le projet» glyphs (CHAPTER institutions/universities/training/italy/pathways, `handshake` for the Forum, drawn at
  24 px). Today `portal.services.organisation_nav_glyph` composes them from the registry's own maps.
- **B** (`templates/account/**`, `templates/allauth/**`): keep using the glossary words; any new project msgid for the
  account pages comes to D's catalogue pass.
- **C** (`templates/legal/document.html`, `apps/core/gates.py`, lane P): Q2 — an unpublished legal page should answer
  404 per document (`document_available`), not G1; `templates/errors/_way_on.html`, `templates/enquiries/partials/
  form_shell.html` and `templates/community/join.html` still link `legal:privacy` / `legal:terms` unconditionally —
  `{% legal_links "privacy" as … %}` from `legal_links` does it in one tag.
- **Orchestrator** (8780 launcher, outside the repository): add `Page("organisation", "Mon organisation",
  "portal:organisation", key="organisation")` to `_org_pages()`, so the hub names the new page. Optionally seed one
  team message for `qa-university` on `ile_v5` to show a register with rows (the preview's organisations otherwise show
  the calm state, which is also correct).

## Not done in W2, or left for W3

- The person rail's «Tableau de bord» as an ungrouped first row (D-22) is done for the company only: for the person it
  changes the section layout that dozens of W3-A tests pin; it belongs to W3's dashboard lattice.
- `AUDIENCE_SPACE_LABELS` still mixes a space name («Espace Personnes») with identity words («Institution»): the rail
  head now carries the organisation's space name, the foot its identity word — consistent on screen; a full harmonisation
  is W3's final catalogue pass.
- The list pages «Mes demandes» and «Communications» keep their one-sentence empty state («… apparaîtront ici») when
  opened directly: a page whose subject is the register says so in one line (not a wall).

## Fixes after review (v512-d-fix-w2)

Base: `design-v5` HEAD `4d9ada5` merged into `v512-d-w2` first (lane P's legal publication path, `document_available`,
`invalidate()`, `publish()`); the fixes on top.

| Finding | Severity | Fix |
|---|---|---|
| D-20 applied only on the bridge: the person's dashboard still drew «Mes échéances … apparaîtront ici» and «Communications … apparaîtront ici» | major | `portal.services.dashboard_context` reads the dates and the communications through `_rows_and_availability` (rows + whether the register could be read; `_safe_rows` is its first half). The person's side column draws each register only **with rows** or when it **cannot be read** (the card's own notice «Cette rubrique est momentanément indisponible. Vos données ne sont pas affectées.»); with neither, one calm sentence «Aucune échéance ni communication pour l’instant.» (it/en/ar translated; EN/AR provisional, Q3). When the NowPanel took the only date over, no calm sentence (the date is on the page). The D-22 rail layout stays in W3. |
| `legal_links` through lane P's per-kind cache, which D's save signal did not clear | minor | `_forget()` calls `legal.services.invalidate()`; the fallback query and its cache key are dropped (P is merged). The test publishes through `services.publish()` (P's rule: a published text saved outside `publish()` returns to draft). |
| Catalogues stale | minor | `i18n_audit --sync`, then translated and `--compile`: 3605 msgids, 100 % in it, en, ar, fr. **Re-run after the A → B → C W2 merges** (their new msgids, C's photographs' alt texts, the asterisk msgid «Les champs marqués d’un astérisque (*) sont obligatoires.», which `--sync` drops once B's field system is merged — it is still used on this tree). |
| `.site-footer__inner--three` has no CSS rule | minor | **Not mine** (`static/css/v5/chrome.css` is lane A's, DECISIONS §10.0): request repeated below. |
| The e-mail error said «courriel»; the phone help repeated «Facultatif —» | minor | Django's `Enter a valid email address.` declared in `apps/accounts/allauth_terms.py` and overridden in the four catalogues: fr «Saisissez une adresse e-mail valide.», it «Inserisca un indirizzo e-mail valido.» (Lei), en «Enter a valid e-mail address.», ar «يُرجى إدخال عنوان بريد إلكتروني صالح.». The shorter phone help B asked for, «Utilisé uniquement pour le suivi de vos demandes.», is declared (`PENDING_SOURCE_TERMS`, so `--sync` keeps it) and translated; `profile_forms.py` is B's — B swaps the msgid. |
| The identity sheet showed the raw stored country («Italia») on fr and ar; the trail root said «Espace réservé» under «Espace Institutions» | minor | `portal.services.country_label()` reads the stored value (an ISO code or a name in any of the four languages) through lane B's `core.countries` (`match` → `name` in the reader's language), the stored word when the table does not know it, or before B is merged. Used by the identity sheet and `organisations_for`'s place. `portal.views._render` starts the trail with `shell_space(user)["label"]` — the rail head's word: «Espace Institutions» / «Espace Universités et Formation» for an organisation, unchanged «Espace réservé» for everyone else. |

Tests added to `tests/frontend/test_organisation_space_v512_d.py`: the person's side column without the wall (4 languages,
the calm sentence translated), a register with rows drawn and the other not, an unreadable register says so, the country
in the reader's language (4 languages; skips until `core.countries` is merged), an unknown country shown as stored, the
trail's root is the space's name (institution, university); `test_a_single_published_page_is_linked_alone` publishes
through `publish()`.

Requests (unchanged owners):
- **A** (`static/css/v5/chrome.css`): `@media (min-width: 64rem) { .site-footer__inner--three { grid-template-columns:
  1.4fr 1fr 1fr; } }`.
- **B** (`apps/accounts/profile_forms.py`): the phone's `help_text` → `_("Utilisé uniquement pour le suivi de vos
  demandes.")` (translated in the four catalogues by this pass).
- **Orchestrator / steward**: after the A → B → C W2 merges, run D's catalogue pass on the merged tree
  (`scripts/i18n_audit.py --sync`, translate the new msgids, `--compile`) and re-run `tests/i18n` and the country test of the new file
  (it stops skipping once `core.countries` exists).
