# W3-F2 — Content, legal, error and account pages · NOTES

Family W3-F2 (plan `docs/design-v5/V5_4_EXECUTION_PLAN.md` §3.5 item 2), branch `v54-w3-f2`, worktree
`C:/tmp/ile_wt/v54-w3-f2`, from design-v5 at `7d4ce79`. Delivery mode (V5.5): implement → review once → fix → ship.
Lane: 127.0.0.1:8784 on `ile_v5_l4` (`ILE_REFERENCE_DATE=2026-10-03`, `DB_CONN_MAX_AGE=0`, `--noreload`), tests on
`test_ile_v5_l4`. Evidence: `C:/tmp/ile_v5_council/evidence/v54/w3-f2/` (outside every repository).

---

## Step 1 — the content and legal pages (implementer w3-f2-impl-1, 11 October 2026)

### What was built

**One grammar, one sheet.** The pages a person reads and consults are drawn by one page partial,
`static/css/v5/_lettura.css` («la lettura»), loaded by one page sheet, `apps/cms/static/cms/lettura.css` (built to
`static/css/dist/cms/lettura.css`), in `extra_head` after `main.css`. One entry for every content page, not one per
app: a reader going from the FAQ to the glossary to a legal page downloads it once (cached). Every page of the area
says `lettura` in its body class; the partial's re-drawings of main.css's components (the trail, the page header, the
search form, the pagination, the empty state) are scoped by it, the pages' own blocks by their names.

The grammar is the public interior's, value for value with the home's chapters (W2-D, `pages.css` §2) and with what
W3-F1 is building for the doors (its `_interior.css`, read, not imported — it is not on design-v5):
1. the trail — breadcrumbs 13/20, current page in ink, links 24 px targets;
2. the head — the space's name as a label, the h1 at 28/36 then 36/44 (48rem), the lead 17/28 then 20/28, verbatim; no
   rule under it; the FAQ's and the glossary's search in the head's **end seat** from 64rem (7 | 5 columns), under the
   lead below;
3. the chapters — one section device at the reading edge (`ile-steps` + the title), head 4 | body 8 and sticky from
   75rem; full-bleed hairlines between bands; a page's foot is a **quiet chapter** (a label, not a title, no device):
   dense, then quiet;
4. the register (`.registro`) — rows on shared hairlines, the whole row the target where it has one destination
   (`registro--links`), no glyph, no arrow;
5. the tools — the search, the glossary's **letter index** (a band that sticks under the letterhead from 48rem, PX25;
   a letter reached from it lands under it), the news' **category filter** (links on one hairline, the current one
   under the tabs' indicator), the pagination (V5 on these pages), the **empty page** (DS V5 §10.8: the domain's glyph
   on its 40 px disc, title 20/28, one sentence, one action — no dashed box: on V5 a broken edge is «attesa», what is
   due, and an empty list owes nothing);
6. the pages' own blocks — FAQ answers (17/28, PX18: the question never smaller than its answer), the glossary
   register (term | definition from 48rem, one band for all letters, groups 40 px apart), news records (`card--flat`,
   a cover only when the article has one — PX17), «Vivre en Italie» (the ten topics typographic, two columns; a
   topic's glyph once, on its own page), partners (records in two columns, the logo only when public), the Forum
   Virtuel (rooms, calendar, initiatives, threads as registers; chips through `{% chip %}`), the forms;
7. D26's slots and long-form prose (PX24) — see below;
8. Arabic, forced colours, print.

Corners: 4 (buttons, fields, notices), full (chips, discs), and 6 for a cover or a figure — the targa's value — so a
screen keeps three (§1.3). Shadows: none at rest (hairlines before boxes, SH-2). Glyphs in an editorial body: at most
three on any page of the area (the topic page: its eyebrow glyph, the chapter mark, the empty mark) — the browser test
holds ≤ 6. Line-heights on the 4 px line (RH-1, tested). Tokens only; logical properties only (tested).

**D26 «the grammar of a legal page», as layout slots** (headings verbatim):
- **verification line** (`.verifica`) — only where a date exists: the legal pages' «Version officielle en italien · en
  vigueur depuis le … · vN», a sheet's «Dernière vérification» / «Publiée le», a term's «Source» / «Dernière
  vérification», an article's «Publié le» / «Mis à jour le» / «Rédaction»; no new commitment;
- **one inset** — the condition nobody may miss: on a sheet, «Informations pratiques à caractère général : elles ne
  remplacent pas les indications des autorités compétentes.» (`.inset`, the institutional notice's paper and gold
  rule); on a legal page, the courtesy translation with its notice, or — while the text is awaited — the pending
  notice (now with its mark and title: the kind said three times, DL54-47); on the companies' form page, the
  prescribed quote;
- **one action** — the page's one primary (the search, the form's submit, the newsletter's «S’inscrire»); no page of
  the area needed the raised action card;
- **an authority's host** (`.autorita__host`) beside each official source of a sheet and of an article
  (`{{ url|host }}`: «salute.gov.it»);
- **a caption and a credit under the photograph** of an article (`figura`): its caption (the article's, else the
  asset's French one, marked `lang`), place, date, «Photo : credit» — always a figcaption when the apparatus has one;
- **«who can help me»** (`.aiuto`) in LIVE words only: «Vous n’avez pas trouvé de réponse ? Contactez-nous» (the FAQ's
  own), «Besoin d’aide ? Écrivez-nous :» + the one address (the account pages' and the login's own string; translated
  in the four catalogues) at the foot of a legal page and of a sheet; inside the pending notice the address itself.

**Pages** (each with its ar twin): `/fr/faq/` (+ search, + empty search), `/fr/glossaire/` (+ search) and a term
page, `/fr/partenaires/`, `/fr/actualites/` (+ category, + empty) and an article, `/fr/vivre-en-italie/`, a topic and
a sheet, `/fr/forum-virtuel/` (anonymous landing; member: rooms, a room, a thread, calendar, initiatives, the request
for access, edit, report), the enquiry forms (`/fr/contact/formulaire/`, `/fr/entreprises/recueil-des-besoins/`, the
two collaboration proposals) and `/fr/demande-transmise/`, the five legal pages, the newsletter's confirmation and
unsubscription. `/fr/contact/` itself is `templates/pages/contact.html` — W3-F1's file (`templates/pages/**`): not
touched; its form page is this family's.

**Forms.** The contact form, the three other enquiry forms and the newsletter: fields at 16 px (v5/base.css), labels
above, one primary; errors said by the 2 px edge, the drawn mark and the words, wired by Django 5.2's
`aria-describedby` (`_error`, `_helptext`) and `aria-invalid` — measured on the lane, fr and ar, 1440 and 390: every
control described by an element that exists, the summary at the top. The newsletter consent's error list is now the
component's pattern (`div[role=alert] > ul`, no `role` on the `ul` — the axe `listitem` defect W1-C fixed in the
component). The Forum's forms show the system's error summary (`components/form_errors.html`) instead of the bare
non-field list. Processing, CSRF, honeypot, timing, throttles and recipients untouched.

**Prescribed titles in capitals are tracked** (TR rule 6) — `{% locked_title %}` (`apps/cms/templatetags/lettura.py`)
renders the h1 whole, with `page-header__title--caps` when the words are capitals and the `lang` of a fallback: news,
«Vivre en Italie», the Forum Virtuel, the companies' form page.

**RTL.** Every French or Italian run on an Arabic page keeps its own direction (punctuation in place) and, in a head,
ends on the reading edge (written `text-align: right` under `[dir="rtl"]`: the run is left to right, so its «end» is
the page's right — the value `tests/i18n/test_rtl_browser.py` reads off the h1); a body in French reads left to right
from the page's start of line; a French quote's box stands on the reading edge with its rule at the start of its words. The fallback `lang` moved from the containers (an article, a sheet, a topic's header, a
record) to the texts that hold the fallback content, so the interface's own words inside them keep the page's language
and a French body reads left to right. The Forum's rooms exist in French only (`name_fr`): marked `lang="fr"` on other
pages.

### Defect found and fixed on the way (older than this family)

On the Arabic (and any non-French) Forum Virtuel pages the prescribed title and text are French fallbacks, which the
`locked` tag wraps in `<span lang="fr">`: written into `<title>` and into the description's `content=""`, the markup
ended the attribute and **the whole prescribed text spilled onto the top of the page, above the letterhead**
(`r5/forum-virtuel_ar_360.png`). They now go in as text (`as` + `striptags`, the news' and «Vivre en Italie»'s
pattern); a test holds it (`test_a_prescribed_text_in_the_title_or_the_description_stays_text`).

### Retired (W3-F2's rows of the deletion map, plan §2.3)

- `components.css` **§20** whole — what was left after W1-C: the search form, the alphabetical index, the FAQ's link
  list, the related links, the glossary term's target (only the FAQ and the glossary drew them);
- `components.css` **§28** whole — the legal page (only `legal/document.html`) and the dead `.dev-placeholder`;
- `components.css` **§22**: the two dead `.pagination__icon-prev` rules (W1-B's hand-over); the pagination itself stays
  — the console's lists draw it.
- DS 2026 §2: the two figures `scripts/regen_design_inventory.py --write` computes for components.css (39.7 → 35.0 KB,
  19 → 17 sections — the slice's «section count in the merge that deletes sections») and the row's prose.

**Left, and why** (rows «by page» whose other consumers still draw them): §9 breadcrumbs and §10 page header (W3-F1's
pages — orientation, pathways, the doors — and the shared `page_header.html` / `breadcrumbs.html` components; these
pages re-draw them under `.lettura`); §18, §19, §24 (W3-F1's pages, the manage layout); §26 errors and §27 manage pages
(step 2); `register.css`'s folio, sources, outcome … (the console's pages and W3-F1's: none of this family's pages
draws them any more — the area's list of sources is `.fonti`, because `register.css` owns `.sources` in main.css);
V1 `layout.css`'s editorial parts (`.container`, `.section`, `.prose` … on most pages of the site).

### Measures

- **Smoke**, lane, fr and ar, at 1440, 1024, 390 and 360 (`r1` … `r5`, `flows`, `interact`): every page 200, no
  horizontal overflow, corners {4, full} (+ the targa's 6), no shadow at rest, ≤ 3 glyphs, no Latin text under 12 px,
  no Arabic under 14 px, typed text 16 px. Captures looked at, page by page.
- **Browser test** with TEST-ONLY content (two articles, two sheets, two partners, a member's Forum) — every page, fr
  and ar, 1440 and 390, member and anonymous: the same assertions pass (`browser-test/`, 80 captures).
- **Keyboard**: the FAQ's disclosure opens on Enter and closes on Space (fr, ar); the glossary's index sticks flush
  under the letterhead at 1440 and 1024 (top 57 = header bottom 57) and a letter lands 25 px under it; on a phone the
  index is a block of its own. On the glossary the page's scroll padding is the letterhead plus the index, so a focus
  moved by the keyboard is never hidden behind the sticky band (WCAG 2.4.11).
- **Targets**: 24 px at least everywhere (the trail's links, the rows of links); under a coarse pointer the links that
  stand alone (rows of links, the FAQ's links, the reset, «who can help me», the head's address) answer on 44 px by an
  invisible extension, the rows opened to 20 px so that no two targets overlap (SP-8); the letter index, the category
  filter and the pagination are 44 px by construction.
- **Forms on the lane** (console e-mail backend checked: `django.core.mail.backends.console.EmailBackend`): the contact
  form sent empty (summary + five fields described), then sent filled → `/fr/demande-transmise/?k=contact`; the
  newsletter without consent (its error), then with → «Merci. Si l’adresse est valide…»; the console mail's two links
  → the confirmation and the unsubscription pages, both submitted.
- **CSS weight** (gzip -9): `dist/main.css` 42 463 → **42 141 B** (−322 B on every page); `dist/cms/lettura.css`
  **3 724 B** (19.5 KB minified) on the content pages only. An interior page: 42 463 → 45 865 B — **1 379 B over the
  Wave-1 interior ceiling (44 486 B)**. Bust rule steps 1 and 2 done (the legacy deleted, the rules in a page partial).
  Measured A/B on the lane (slow 4G 150 ms / 1.6 Mbps, CPU ×4, cold, n = 3 interleaved; arm B = the same page with
  the page sheet's request blocked; the dev server serves the sheet uncompressed, 19 KB, so this is an upper bound):
  FAQ 1440 LCP 2 052 vs 1 968 ms, FAQ 390 2 040 vs 1 936, contact 1440 2 048 vs 2 004, contact 390 2 068 vs 1 968;
  CLS 0 · 0.0006; longest task ≤ 114 ms; every LCP under the 2.5 s budget (`perf/perf.json`). For the steward's record
  (as DL54-44, -73, -76).

Evidence folders (`C:/tmp/ile_v5_council/evidence/v54/w3-f2/`): `before/` (the pages as design-v5 left them), `r1/` …
`r5/` (the rounds, 1440 · 1024 · 390 · 360, fr and ar), `flows/` (the forms on the lane), `interact/` (keyboard, the
sticky index), `perf/perf.json`, `browser-test/` (the TEST-ONLY content pages), `final/`, `final2/`, `final3/`.

### Tests

- New: `tests/frontend/test_content_pages_w3_f2.py` (40: every page loads the sheet and says `lettura`; the partial is
  page-only, tokens only, logical, on the 4 px line, every token it reads exists; the retired rules are gone; `host`;
  `locked_title`; the title/description leak) and `tests/frontend/test_content_pages_browser_w3_f2.py` (6, browser).
- **Targeted suites, all green on the branch's head** (`TEST_DATABASE_URL=…/test_ile_v5_l4`, one run at a time):
  - not browser — `tests/compliance`, `tests/security`, `tests/i18n`, `apps/accounts`, `tests/frontend/test_layout.py`,
    `test_design_docs.py`, `test_css_bundle_is_current.py`, `test_frontend_bundle_is_current.py`,
    `test_static_pipeline.py`, `test_o14_lint.py`, `test_state_chips_carry_a_register.py`, `test_icons.py`,
    `test_429_w2_b.py` (the 429 page), `test_v5_tokens.py`, `test_chips_registry.py`, `test_static_assets.py`,
    `test_legacy_token_shim.py`, `test_css_tokens_exist.py`, `test_components_w1_c.py`,
    `test_template_comments_do_not_leak.py`, `tests/test_check_ownership.py`, `tests/test_regen_design_inventory.py`:
    1 569 passed, 1 xfailed — after four fixes of this family's own making, all re-run green: the FAQ's answer count
    keeps the heading markup `test_ui_translations` reads (×3), and the two notices' marks no longer read as a literal
    `svg_icon` name (`test_icons`);
  - the content apps (`apps/faq glossary news living partners community enquiries`) with the two new files and
    `test_icons`, `test_css_bundle_is_current`: 392 passed;
  - browser — `tests/i18n` (all three RTL files), `tests/frontend/test_browser.py`, `test_browser_w1_b.py`,
    `test_browser_w1_c.py`, `test_content_pages_browser_w3_f2.py`: 68 passed, 1 failed — `test_rtl_browser`'s h1
    alignment on the Arabic companies' form page read `end` (fixed: `right`, see «RTL»), then
    `test_rtl_browser.py` + the family's browser file re-run: 29 passed. No skip, no crash.
  - The error pages in four languages (`test_ui_translations`, `test_layout`, `test_429_w2_b`) are green; their
    redesign is step 2.

### Lane state left behind (ile_v5_l4 only)

- The flag `virtual_forum` was switched on for the Forum Virtuel's smoke — **restored** (row deleted, the default off
  applies again) at the end of step 1.
- Rows written by the flows, all `@example.invalid`: one contact enquiry («Lane W3-F2 smoke»), one newsletter
  subscription (confirmed, then unsubscribed) with its consent record. Left in the lane database (consent records are
  an append-only trail).

### Ownership — paths outside the slice, for the merge step (to write into the manifest, not to ignore)

`scripts/check_ownership.py w3-f2 design-v5` lists them. Justified:
- `static/css/v5/_lettura.css` — the area's page partial (plan §2.3: page-only CSS is a `_` partial of static/css/v5);
- `apps/cms/static/cms/lettura.css` — its one entry (plan §2.3: page sheets are app entries); `static/css/dist/**` is
  generated;
- `apps/cms/templatetags/lettura.py` — the `host` filter (D26) and the `locked_title` tag;
- `apps/living/catalogue.py` — W1-B's hand-over: the seed's glyphs are the registry's LIVING map;
- `docs/design/DESIGN_SYSTEM_2026.md` §2 — the two regenerated figures and the components.css row's prose (the slice
  names §10 prose and the section count);
- `templates/glossary/_entry.html` and the two test files are inside the slice's globs.

### Handed to W3-F2 — answers

| From | Item | Answer |
|---|---|---|
| W1-B NOTES l.165, SHIPPED | the arrow density of the public editorial body (six-icon ceiling, DL54-23 item 1) | **Done** for this area: no `link-arrow` and no row arrow on any page; the pagination keeps its two direction marks; ≤ 3 glyphs per page, ≤ 6 held by the browser test |
| W1-B NOTES l.165, l.339 | `pagination__icon-prev` is dead CSS in §22 | **Done**: both rules removed |
| W1-B NOTES l.339, SHIPPED | `living.catalogue`'s icons (`home`, `globe`, …) | **Done**: `apps/living/catalogue.py` seeds the registry's LIVING symbols. Rows already seeded keep their V4 ids — never read for these ten slugs (`living/topic.html` asks the registry first); no data migration. With `pathways.services.DEFAULT_ICONS` (W3-F1, still `globe`) the aliases can then leave `icons.LEGACY` |
| W1-B NOTES l.339 | the model's help text («ex. « home »») | **Not done**: it is a msgid of the four catalogues (the Arabic is the owner's translators'), an admin-only string, and `home` resolves while the alias exists. Whoever removes the alias changes the example in the same translators' batch |
| W1-C NOTES (to W3-F1, the FAQ is W3-F2's) | «Pour aller plus loin» 6 px under the FAQ's last row | **Done**: the foot is a quiet chapter of its own, a band below the last question (hairline + 40/64 px) |
| W1-C NOTES l.260 | the account pages' links box floats over the title (W2-A / W3-F2) | **Step 2** (account pages) |
| W1-C NOTES l.596 | «Supprimer mon compte»: the links box covers the warning's first line | **Step 2** |
| W1-D NOTES l.469, l.488, SHIPPED | `accounts/profile.html`: the export form's `data-loader="none"` must survive | **Step 2**; the file is untouched here |
| W2-B NOTES l.164 | `allauth/elements/form.html` (the manage pages) untouched by W2-B | **Step 2** |
| W2-B NOTES l.569 | the show / hide control drawn as its words says its state twice (account pages) | **Step 2** |

### B1 item 7 — question headings and «who can help me», PROPOSED (never written in a template)

Copy for the owner's packet; the templates keep today's live strings until it is signed. The official Italian
headings of the legal pages and the courtesy translations' headings (locked) are not ours to recast.
- «Pour aller plus loin» → «Que lire ensuite ?»
- «Sources officielles» / «Sources» → «Où vérifier ces informations ?»
- «Fiches pratiques» → «Que faut-il savoir ?»
- «Termes liés» → «Quels termes vont avec celui-ci ?»
- «À lire aussi» → «Que lire d’autre ?»
- «Votre message» → «Que souhaitez-vous nous demander ?»; «Votre proposition» → «Que proposez-vous ?»
- «Données personnelles» → «Que devient ce que vous nous écrivez ?» (with counsel)
- the «who can help me» slot: a label «Qui peut m’aider ?» above today's live sentence.

### Left for step 2 and for others

- Step 2 (this family): the 400 / 403 / 404 / 410 / 429 / 500 errors (§26), the profile and account-management pages
  and allauth's manage layout (§27), with the hand-overs above. The partial is ready to be imported by their sheet.
- W3-F1 / W4: the two interior partials (`_interior.css`, `_lettura.css`) share the chapter, register and D26 class
  names and values on purpose — one of them can import the other's common part once both are on design-v5.
- W3-E: the component `empty_state.html` keeps V4's dashed box elsewhere; these pages draw the V5 empty page under
  `.lettura` — the same drawing can move into the component's rebuild.

---

## Step 2 — the error pages and the account pages (implementer w3-f2-impl-2, 11 October 2026)

### What was built

**One page partial, one entry, for the pages of service.** `static/css/v5/_servizio.css` («le pagine di servizio»),
loaded by one page sheet, `apps/cms/static/cms/servizio.css` (built to `static/css/dist/cms/servizio.css`), after
`main.css`, on the error pages and the account pages — and on nothing else. Self-contained on purpose: the trail, the
head and the empty state are restated at lettura's values (one grammar), so a page of service carries neither the
content pages' 3.7 KB sheet nor this one's rules elsewhere. Every page says `servizio` in its body class.

**The errors 400 / 403 / 404 / 410 / 429 / 500** are one quiet page in the interior's grammar, the same for every
status (templates/errors/**): *what happened* — the status as the head's label («Erreur 404», the document title's
words, decorative), the title and the sentence verbatim; *what to do* — one primary (the home) and the way back
(«Page précédente», with script only, `.js-only`); *the way on* — the recovery navigation as a quiet chapter (a label,
not a title, the spaces as links); *«who can help me»* — «Besoin d’aide ? Écrivez-nous :» and the one address (the
account pages' live line, D26). The V4 numeral at 7rem and the at-sign button are gone; the one forward arrow stays
on the primary — the action that goes on (`icon--flip-rtl`, test_rtl_browser reads its mirror on the 404) —, the way
back has none. Nothing is revealed:
no stack, no path (a test asks a 404 for a made-up address and finds it nowhere in `<main>`), no account detail; the
500 shows the request's correlation id. The 403 offers the sign-in as its primary to a person who is not signed in —
its sentence asks for it —, the home and the way back otherwise.

- **400 and 500 are self-sufficient** (`apps/core/views.py`): rendered WITHOUT the request — no context processor, no
  database, no session —, as Django's own `bad_request` and `server_error` are, in a frame of their own
  (`templates/errors/standalone.html`: the letterhead's lock-up on paper and nothing that reads the database, the faces'
  preloads, `main.css` + the page sheet, `head.js` and `main.js` for the back link). The project's name and the public
  address come from settings, the language is the one LocaleMiddleware set. If even the template fails (a static
  manifest that lost an entry), the view answers a bare page of the same catalogue words, naming nothing. Proved by
  tests with no `django_db` mark (a query would raise) under a context processor that explodes, and in a browser: a
  view that raises reaches the page through every middleware, CSP included.
- **403, 404, 410, 429 stay in the public shell** (`templates/errors/base_error.html`): they answer a visit, and the
  site's navigation is the way on. W2-B's root `templates/429.html` keeps putting the page's content in a signed-in
  person's way — untouched, its test green.

**The account pages** — the profile, allauth's management pages (the e-mail addresses, the password change and set,
the second factor and the authenticator's set-up, the sign-out's confirmation) and the deletion request — stand in one
frame on the public shell (they sat in neither the console nor the entrance): `allauth/layouts/base.html` →
`manage.html`, which `accounts/profile.html` and `accounts/delete_request.html` extend too.
1. the trail — «Accueil › Espace réservé › Mon compte › the section», read from the address (allauth's views give
   none; `accounts/partials/trail.html`, the breadcrumbs component's markup and classes);
2. the account's sections (`accounts/partials/account_nav.html`) — from 64rem in the chapter head's seat at the reading
   edge (three columns of twelve, sticky from 75rem), a list on a rule with the current section on the tabs' indicator;
   below 64rem a band of links on one hairline (the news' categories), its first word on the reading edge. The current
   section says `aria-current="page"` on its own page, `"true"` on one of its pages (the deletion request, the
   authenticator's set-up). Profil · Adresses e-mail · Mot de passe · Authentification à deux facteurs: the way to the
   reserved area and the sign-out stay the letterhead's account menu; «Mes documents» moved to the person's data;
3. the page in the body's eight columns: its title (28/36 → 36/44) and its sentence (the lead, 17/28 → 20/28), its
   sections on hairlines (20/28 titles), the profile's facts as a register (label 14/20 over its value, side by side
   from 48rem), the security as rows whose whole row is the target (the second factor's state as its chip), the
   organisations as a table on hairlines or the V5 empty state (glyph disc, title, sentence — no dashed box), forms at
   the reading measure (16 px typed text, 52 px plates, one primary after a hairline), the person's data (the export —
   `data-loader="none"` kept —, «Mes documents», then under a hairline of its own the system's danger button), and
   «who can help me» at the foot;
4. allauth's elements keep their class names (`account-page__title`, `account-page__text`, `account-panel`…) and the
   product's two pages use the same names: one drawing under `.conto` for both. The entrance's elements are untouched;
   one management variant only, `templates/allauth/elements/button__manage.html`, so that a page has one primary
   («Rendre principale» beside «Ajouter un e-mail», «Générer de nouveaux codes» beside «Télécharger les codes» become
   secondaries);
5. **the danger action**: W2-A's tag `v54/w2-a` is NOT on design-v5 (only `v54/w2-a-pre-propagation`), so the deletion
   keeps today's mechanism — the profile's danger button (the garnet outline) leads to its own confirmation page, where
   the warning notice is the one inset, the password and the mandatory box confirm, and the answers are «Annuler» first,
   «Confirmer la suppression» (danger) last. allauth's own confirmations (an address's removal through allauth's
   `confirm()`, the authenticator's deactivation page, new recovery codes) are allauth's. Once W2-A merges, the deletion
   can confirm on overlay.js's alertdialog: a change of `accounts/delete_request.html` and the profile's button only;
6. the deletion's answer (`accounts/delete_done.html`, the person signed out) is a quiet page of the frame (`conto--solo`):
   no trail, no sections, the title and its sentence, one primary, the page's own «who can help me»;
7. every account page is kept out of the index (`noindex` where the view has not set it; robots.txt already disallows
   `/*/compte/`).

Corners: 4 (buttons, fields, notices, the QR code's tile), full (chips, the empty state's disc) and the letterhead's 6
— three a screen. Shadows: none at rest. Glyphs in `<main>`: ≤ 3 on every page of the area. Line-heights on the 4 px
line, tokens only, logical properties only (tested).

### Defect found and fixed on the way (step 1's, this family's)

`tests/i18n/test_rtl_static.py::test_stylesheet_uses_logical_properties_only[static/css/v5/_lettura.css]` failed on the
branch: step 1's last commit had written `text-align: right` for a French run in an Arabic head (what
`test_rtl_browser` reads off the companies' h1 — `start`, `right` or `center` — after `end` had failed it). Both tests
now pass without a physical property: a French or Italian run in a head ends on the reading edge with
`text-align: end` (its own direction is left to right), and a prescribed h1 shown in another language than the
page's (`{% locked_title %}`, `apps/cms/templatetags/lettura.py`) holds its words as a run of their own —
`<h1 class=…><span dir="ltr" lang="fr">…</span></h1>` — so the h1 keeps the page's direction and `start` while the run
keeps its punctuation; the capitals' tracking follows the run. The heads look as they did (`final-s2b/`, looked at).

### Retired (W3-F2's rows of the deletion map, plan §2.3) — main.css gzip 42 141 → 41 814 B (−327 B, every page)

- `components.css` **§26** whole — the error page (`.error-page*`) and `html.no-js .js-only` (now the partial's: only
  the error pages use it);
- `components.css` **§27**: the account pages' frame, card and panels — `.account-page`, `.account-page__card` (and its
  `h1`), `.account-page__aside`, `.account-page--manage .account-page__card`, `.account-panel`,
  `.account-panel:first-of-type`, `.account-panel__actions`, `.account-page .form-field`. **Kept, and why:**
  `.account-panel__title` — the entrance «Il varco» (W2-B) draws allauth's second title through it («Options
  alternatives» on the reauthentication and the second factor's sign-in); `.account-table` — the console's requests
  list (`templates/portal/requests.html`, W3-E) and the design showcase draw it. The section stays as «27. Account
  pages — what the entrance and the console still read»;
- `templates/accounts/partials/account_menu.html` — deleted (its two includers rewritten);
- DS 2026 §2: the two figures `regen_design_inventory.py --write` computes for components.css (35.0 → 33.0 KB,
  17 → 16 sections) and the row's prose; §2.1: the rows of the two page sheets (`cms/lettura.css`, step 1's, was
  missing; `cms/servizio.css`); §10: the entries that cited the rewritten templates (`breadcrumbs.html`,
  `local_nav.html`, `page_header.html` — their «Usato in» and examples now name templates that use them); §10.1: the
  error and account rows as V5 draws them.

The login family is unchanged by the deletions: `/compte/login/`, `/compte/signup/`, `/compte/password/reset/` and
`/compte/reauthenticate/`, fr and ar, 1440 and 390, captured with the step-1 `main.css` and with this one — **16 / 16
pixel-identical** (`entrance-before/`, `entrance-after/`). Taken with a cold HTTP cache and the swapped sheet checked
on the wire (the step-1 bundle served during the «before» run): a first comparison, run seconds after the swap, had
reused the cached bundle (the dev server sends no Cache-Control) and proved nothing — redone; every lane script now
empties the profile's HTTP cache at launch.

### Measures

- **The whole area together** (step 1's pages and step 2's: 39 pages — the FAQ with and without results, the
  glossary, a term, the partners, the news, «Vivre en Italie» and a topic, the Forum Virtuel's landing and its request
  for access (flag on for the run, then restored), the four enquiry forms and their answer, the five legal pages, the
  newsletter's two answers (lane tokens, GET only), 400 / 403 / 404 / 410 / 500, the 403 of a signed-in superuser, the
  profile of a person and of a company member, the e-mail addresses with and without an address, the password, the
  second factor, the deletion request and its answer, the sign-out's confirmation) on the lane:
  - **1440 and 390, fr and ar** (`final-s2/`, 156 full-page captures): every page answers its status; one h1; **≤ 3
    corner values a screen** (chrome included, a pill counted as `full`); **0 shadow of level ≥ 3 at rest**; **0 CSP
    report, 0 console error** (an error page's own 4xx / 5xx status line excepted); no Latin text under 12 px, no
    Arabic under 14 px; typed text 16 px; ≤ 3 glyphs in `<main>`;
  - **320, 340, 360, 375, 390, 412, 430, fr and ar** (`area-sweep/`, 546 loads): **0 px of horizontal overflow**, and
    the same corner, shadow, CSP, console, type and field results;
  - after the last two fixes (the error page's arrow, the logical French run in an Arabic head — below), the error
    pages, the 403 of a signed-in superuser and the four pages with a prescribed title (the companies' form, the news,
    «Vivre en Italie», the Forum Virtuel) re-measured at 1440 / 390 (`final-s2b/`, 40 captures) and at the seven phone
    widths (`area-sweep-b/`, 140 loads): the same results; every run above started from an empty HTTP cache;
  - the product's **429** reached through a real throttle (the account deletion's, 5 posts in 10 minutes, the form
    posted empty — nothing deleted): fr and ar at the seven phone widths and 1440, 16 loads, the same results
    (`s2r4/`, `area-sweep-429.log`); the **authenticator's set-up** (a session holding a fresh sign-in record: no
    password involved) at the eight widths, fr and ar, the same (`area-sweep-totp/`).
- **Looked at**, page by page, fr and ar, 1440 and 390 (`s2r1/` … `s2r5/`, `final-s2/`, `final-s2b/`; 1024 and 768 in
  `s2-mid/`): the defects found by
  eye and fixed — the 500's page hidden under its own letterhead's paper layer (a static header handed its `::before`
  to the whole page), allauth's bare second title glued to the e-mail form (a later rule zeroed its margin), two
  hairlines between the address list and its actions, the band's first word 12 px off the reading edge, buttons outside
  a form's actions at 44 instead of 52 px, the deletion's answer tight under the letterhead, the QR code touching its
  secret's label, a hairline above the sign-out's lone button (a form with no field to fill is its answer alone).
- **Keyboard** (`/compte/email/`, fr, 1440): skip link → languages → letterhead → the trail → the four sections → the
  address → its three actions → the new address → the primary → «who can help me» → the footer; every stop draws the
  system's ring; nothing focused hides under the sticky letterhead.
- **Browser test** (`tests/frontend/test_service_pages_browser_w3_f2.py`, live server, Chromium): every service page
  fr and ar at 1440, 390, 320 and 430 — status, language, overflow, one h1, ≤ 3 corners, no level-3 shadow, no CSP, no
  console error, type floors, 16 px fields; a real failure and a suspicious request through every middleware; the
  current section on the reading edge (the right one in Arabic) and under its words below 64rem (`browser-test-s2/`,
  48 captures).
- **CSS weight** (gzip -9): `dist/main.css` 42 141 → **41 814 B**; `dist/cms/servizio.css` **2 353 B** (11.7 KB
  minified) on the service pages only. An error or account page: 41 814 + 2 353 = **44 167 B, under the interior
  ceiling (44 486 B)**. Nothing animates on these pages but the system's colour changes (0 ms under reduced motion).

Evidence (`C:/tmp/ile_v5_council/evidence/v54/w3-f2/`): `before2/` (the pages as step 1 left them), `s2r1/` … `s2r5/`,
`s2-mid/`, `final-s2/`, `final-s2b/`, `area-sweep/`, `area-sweep-b/`, `area-sweep-totp/` (the 429 sweep's log in the
scratch folder, `C:/tmp/ile_v5_council/.work/w3-f2/w3-f2-impl-2/`), `entrance-before/`, `entrance-after/`,
`browser-test-s2/`.

### Tests

- New: `tests/frontend/test_service_pages_w3_f2.py` (45: the self-sufficient 400 / 500 and their bare fallback; every
  error page in four languages; the 403's primary; the error family's templates; the account frame on six pages; the
  profile's contract — `data-loader="none"`, the danger button, «Mes documents»; the deletion's order of answers;
  allauth's second primary; the management button's mapping, the entrance's kept; the authenticator's set-up in the
  frame; the page sheet; the partial's rules; the retired rules) and `tests/frontend/test_service_pages_browser_w3_f2.py`
  (3, browser).
- Targeted suites (one run at a time, `TEST_DATABASE_URL=…/test_ile_v5_l4`):
  - **not browser** — `tests/i18n`, `tests/compliance`, `tests/security`, `apps/accounts`, `apps/enquiries`,
    `apps/consents`, `apps/faq`, `apps/glossary`, `apps/news`, `apps/living`, `apps/partners`, `apps/community`,
    `tests/frontend/test_layout.py`, `test_design_docs.py`, `test_css_bundle_is_current.py`,
    `test_frontend_bundle_is_current.py`, `test_static_pipeline.py`, `test_o14_lint.py`,
    `test_state_chips_carry_a_register.py`, `test_429_w2_b.py`, the two new files' unit half, `test_content_pages_w3_f2.py`,
    `test_loader_rules.py`, `test_icons.py`, `test_template_comments_do_not_leak.py`, `test_components_w1_c.py`,
    `test_design_showcase.py`, `test_entrance_w2_b.py`, `test_entrance_form_w2_b.py`, `test_v5_tokens.py`,
    `test_css_tokens_exist.py`, `test_legacy_token_shim.py`, `test_static_assets.py`, `test_chips_registry.py`,
    `tests/test_check_ownership.py`, `tests/test_regen_design_inventory.py`: **2 013 passed, 1 failed, 2 xfailed** — the
    failure step 1's (`test_rtl_static` on `_lettura.css`'s `text-align: right`, «Defect found and fixed» above);
  - **browser** — `tests/i18n` (`test_rtl_browser.py`, `test_rtl_browser_entrance.py`, `test_rtl_browser_nav.py`),
    `test_service_pages_browser_w3_f2.py`, `test_content_pages_browser_w3_f2.py`, `test_entrance_w2_b.py`,
    `test_entrance_form_w2_b.py`: **102 passed, 0 skipped, 0 failed** (after the fixes);
  - **after the last fixes** (the arrow, the logical run), the suites they touch again — `tests/i18n`,
    `tests/compliance`, `apps/community`, `apps/enquiries`, `apps/living`, `apps/news`, `apps/accounts`, `test_layout.py`,
    `test_429_w2_b.py`, both families' unit files, `test_icons.py`, `test_design_docs.py`, the bundle and pipeline tests,
    `test_o14_lint.py`, `test_state_chips_carry_a_register.py`, `test_loader_rules.py`,
    `test_template_comments_do_not_leak.py`: 995 passed, 3 failed — `apps/enquiries`' compliance test reads
    `lang="fr">TITLE`, the run wrote `lang` before `dir`: the order turned (`46927fb`), then the files it touches
    (`apps/enquiries/tests/test_compliance.py`, `test_content_pages_w3_f2.py`, `test_locked_texts.py`,
    `test_page_integrity.py`): **94 passed**. The browser run above was taken before that attribute's order changed (the
    same rendering).
- Not run: the full suite (V5.5: integration checkpoints run it); `tests/frontend/test_design_preview.py` (its error-page
  states read the template's name, the language and the title, all kept).

### Lane state left behind (ile_v5_l4 only)

- The flag `virtual_forum` was switched on twice for the area's runs — **restored** each time (row deleted, the default
  off applies).
- Sessions minted with `force_login` for qa-person, seed-company, qa-fresh-person, qa-admin (and qa-person with a fresh
  sign-in record) — **revoked** at the end (rows deleted, the secrets file removed).
- No row written by this step: the throttle's counter lives in the lane server's memory (10 minutes), the
  authenticator's set-up keeps its pending secret in the (revoked) session; nothing was deleted, activated or sent.

### Ownership — paths outside the slice, for the merge step (to write into the manifest, not to ignore)

`scripts/check_ownership.py w3-f2 design-v5` lists them. Justified:
- `static/css/v5/_servizio.css` — the service pages' page partial (plan §2.3);
- `apps/cms/static/cms/servizio.css` — its one entry, beside step 1's `cms/lettura.css`; `static/css/dist/**` generated;
- `apps/core/views.py` — `error_400` and `error_500` render without the request (the self-sufficient page), with the
  bare fallback; unowned in the manifest;
- `docs/design/DESIGN_SYSTEM_2026.md` — §2 (the two regenerated figures, the components row's prose, the two page
  sheets' rows of §2.1) and §10 (the entries whose «Usato in» or example cited the rewritten templates; §10.1's two
  rows); `docs/design-v5/DECISION_LOG_V54.md` — DL54-78 (to renumber: design-v5 has its own DL54-77 … since);
- `templates/errors/{standalone,_actions,_way_on}.html`, `templates/accounts/partials/{trail,account_nav}.html`,
  `templates/allauth/elements/button__manage.html` and the two test files are inside the slice's globs.

### Handed to W3-F2 — answers (step 1's table, the rows left for step 2)

| From | Item | Answer |
|---|---|---|
| W1-C NOTES l.260 | the account pages' links box floats over the title | **Done**: the profile's list wore the header dropdown's class names (`account-menu__list`: absolute, shadow 3); the account pages now have their own list (`conto-nav`), in the frame's seat |
| W1-C NOTES l.596 | «Supprimer mon compte»: the links box covers the warning's first line | **Done** (same cause, same fix); the page's answers are now «Annuler» then the danger button (m3: in `.form__actions`, no inline white space) |
| W1-D NOTES l.469, l.488 | `accounts/profile.html`: the export form's `data-loader="none"` must survive | **Done**: kept, and tested here as well as in `test_loader_rules` |
| W2-B NOTES l.164 | `allauth/elements/form.html` (the manage pages) untouched by W2-B | **Kept untouched**: the management layout draws it under `.conto`; only the button needed a management variant |
| W2-B NOTES l.569 | the show / hide control drawn as its words says its state twice (account pages) | **Already resolved** by W1-C's component (one constant name, `aria-pressed` the one channel, the eye glyph): seen on the password change and the deletion request, fr and ar |

### Left, and for others

- **The CSRF failure page** (`templates/403_csrf.html`, a root template): Django's English page answers an expired
  form today. Not built: no live sentence fits (the generic 403's «vous n’avez pas les droits…» would mislead) — a new
  sentence is B1 copy (with the owner's translators for ar). Then the page is the self-sufficient frame (Django renders
  it without the request).
- **Sessions**: `allauth.usersessions` is not installed — there is no page of sessions to draw.
- **W2-A**: once `v54/w2-a` is on design-v5, the deletion's confirmation can move onto overlay.js's alertdialog (the
  page stays as the no-script fallback); the header's account menu (`components/account_menu.html`, §8) is W2-A's.
- **W4-D**: `.account-panel__title` and `.account-table` are the last rules of §27 — they leave with their readers'
  families (W2-B's next pass, W3-E's console tables).
- **B1 item 7**: «Qui peut m’aider ?» above the live line (step 1's proposal) applies to these pages too.

---

## Review fixes (implementer w3-f2-fix, 12 October 2026)

The fix pass on `REVIEW.md` (`w3-f2-review`: three majors, twelve minors, the notes for the steward) and `A11Y_PERF.md`
(`w3-f2-a11y-perf`: A1 … A4, P1, O1). V5.5: implement → review once → fix → ship — no new review round. Lane 8784 on
`ile_v5_l4` as before; headless Chromium with its own profiles (`.profiles/w3-f2-fix/`), one browser and one pytest at a
time; no run crashed. Evidence: `C:/tmp/ile_v5_council/evidence/v54/w3-f2/fix/` (`before/`, `door1/` … `door6/`, `r1/`,
`probe/` with `probe_fix.json`, `forced/`, `browser-test/` — the family's browser tests' captures on TEST content —
and the `c_*.png` crops); scratch scripts: `C:/tmp/ile_v5_council/.work/w3-f2/w3-f2-fix/`.

### The majors

| Item | Fix | Seen and measured on the lane |
|---|---|---|
| **M1** the error pages carry nothing of ILE | **The door at rest** on every error page (CD §0 item 2, brand act 1, §1.4 law 5, §20; DS V5 PX21). `templates/errors/_door.html` draws the entrance's stage — the arch, the owner's photograph as served (`static/brand/v5`, AVIF and WebP), the solid navy inner door, the three steps, the outline — with **the key out of the lock**: the verbatim key set down on its side on the top step (bow at the door's right, bit down). No glow at the keyhole, no lit frame, no lit steps, nothing moves (reduced motion is the same picture), never mirrored (the stage stays `direction: ltr`; the `sig` host keeps the image's colours under forced colours); decorative (`aria-hidden`, nothing focusable). Included first in the page by `errors/base_error.html` and `errors/standalone.html`, static files only: the 400 and the 500 stay self-sufficient and their bare fallback stays text. **Seat:** compact above the label below 64rem, at the reading edge (5rem on a phone, 7rem from 48rem); from 64rem one grid row — what happened and what to do (`.error-page__body`, one block, so that the buttons never stretch) in seven columns, the door (14rem) in the end seat (the left of an Arabic page), its threshold on the actions' line when the words are the taller; the arch, not its box, on the edge (the stage's 24 / 368 margin pulled out); no drop shadow on paper; hidden in print. **Paint:** W2-B's `_door.css`, imported by a page sheet of the error pages, `apps/cms/static/cms/errori.css` (the door stage + `_servizio.css` + the door's seat), which the two error frames load instead of `cms/servizio.css` — the account pages keep theirs without the door (V5.8: a surface's CSS where it is used). The message and the three ways back unchanged. | fr / ar × 1440 / 1024 / 834 / 390 (`door2/` … `door6/`): end seat at 1440 and 1024 (arch on the container's edge), above the label at 834 and 390, the key's bow on the door's right in both directions; the real 500 through every middleware and the signed-in 403 in the browser test (`browser-test/__w3f2___500_*`, `compte_profil_suppression_admin_*`); forced colours light and dark (`forced/`): the image kept, lines and steps in the system's ink; reduced motion: 0 animations; 0 overflow, 0 CSP report, 0 console error; ≤ 2 corner values. |
| **M2** Latin runs off the reading edge on the Arabic pages | `_lettura.css`: **every head of the area ends on its cell's reading edge** — the head rule (the h1 and h2 of `.page-header` / `.chapter__head`) extended to `.glossary-entry__term`, `.faq-item__question` and `.registro__title` (`text-align: end`, the run keeping its `ltr`); bodies keep their own start. | `probe/probe_fix.json`, ar at 1440 and 390: 10 Italian terms and 9 French questions, **worst gap 0 px** (were 100–140 px off for the terms; the questions zig-zagged); the Forum's rooms in the browser test (a member, TEST content). New browser assertion (below). |
| **M3 / A1** a refused newsletter is invisible | `news/_newsletter.html` opens its form with **the system's summary** (`components/form_errors.html`, `#form-errors`: the non-field errors and a link to each field in error) — the old non-field `div` is in it now; the field keeps its own error. `apps/news/forms.py`: the consent's `label_lang`, as the enquiry forms set it, so the summary marks the consent's French label on the Arabic page. | Sent after the 3 s floor without the consent: **focus on `#form-errors`**, inside `#newsletter`, in the viewport (fr 1440: 408–572 of 900 px; ar 390: 334–582 of 844), its link `#id_consent` with `lang="fr"` in Arabic, `aria-invalid` and the field's error kept (`probe/newsletter-refused_*.png`). Nothing stored. |
| **A2** the profile's personal fields carry no input purpose | `apps/accounts/profile_forms.py`: `full_name` `autocomplete="name"`; `phone` `type="tel"`, `autocomplete="tel"`, `inputmode="tel"`; `country_of_residence` `autocomplete="country-name"`; `preferred_language` `autocomplete="language"` — widgets declared on the fields, so `type` is the input's type, not a second attribute; the validation unchanged. | Rendered as listed, fr and ar. |

### The minors

- **m1** the letter band is a row of equal cells — `grid`, `repeat(auto-fill, minmax(44px, 1fr))`, no gap — that takes
  the gutter's first 16 px on both sides, so a letter centred in its cell stands on the reading edge with its drawing:
  **one line at 1440, 390 and 360** (cells 45.4 / 47.8 / 44 px), two at 320 by design. (The review's «358 px» is 350 px
  of band at 390: the gutter is 20 px below 430.)
- **m2** a row that is a link says so at rest: a register's title link (`.registro__title a` — «Vivre en Italie»'s
  topics, a topic's sheets, the Forum's rooms and threads) and the account's «Sécurité» rows in the link's colour
  (`--accent-text`); the underline and `--accent-text-hover` come under the pointer; no glyph.
- **m3** the legal pages have **the trail** (the breadcrumbs component's markup, Accueil › the page: the view gives
  none) and the verification line drawn as a `.verifica` in a head — 24 px under the title, 13/20, the quiet ink,
  tabular figures — by CSS (the i18n tests pin `<p class="legal-page__meta" lang>`). «Sur cette page» waits for the
  official texts (PX24: none on the lane).
- **m4** the newsletter's two answers lead on: once answered, «Retour à l’accueil» (the one primary, with the error
  pages' arrow) and «who can help me», both in live words.
- **m5** **one rule between two groups**: a glossary group's last term and the profile's last «Sécurité» row leave
  their closing hairline to the next group's rule; the address list (`/compte/email/`) takes the body's width, so
  «Rendre principale», «Renvoyer la vérification» and «Enlever» hold one row at 1440.
- **m6** an enquiry form's first legend under its chapter's title is visually hidden — still the fieldset's name; the
  consent's legend stays — on the contact, company-needs and collaboration forms (the same pair of titles on each).
- **m7** the news' filter is drawn only where it filters (over articles, or over a category's empty answer: its way
  back); an empty state first in a chapter without a head draws no second hairline under the chapter's rule.
- **m8** **one rule for a head's Latin paragraph on the Arabic page** (a lead, an eyebrow, a chapter's lead, a topic's
  introduction): a box the width of its words pushed onto the reading edge — one line ends there as a heading does, a
  longer text reads from its own start as a body does (`inline-size: fit-content; margin-inline-start: auto` on the
  `ltr` run); headings keep `end`. «Vivre en Italie»'s seven-line lead now reads from its start at 1440 and 390. The
  rule for W3-F1 (its review's m7) is in «For the merge».
- **m9** the anonymous 403's «Se connecter» carries **`?next=`** the refused address
  (`request.get_full_path|urlencode`; allauth refuses a `next` that is not of this site).
- **m10** a topic's glyph stands **with its title** — on the h1's first line at the reading edge, 24 px with the 28 px
  title and 32 px with the 36 px one, in ink; a fallback title is a run of its own (`<span lang dir="ltr">`), so the
  glyph keeps its seat in Arabic.
- **A3** under a coarse pointer the trail's links, the glossary's terms, the FAQ's links and permalink, the consent's
  privacy link and the password's help link joined the 44 px extension, and a word narrower than 44 px is widened about
  its middle (`inset-inline: min(0px, calc((100% − 44px) / 2))`: «Gérer», «إدارة», «وثائقي»); the bare inline links became
  24 px boxes (`inline-block`; + 2 px on a 20 px line), which holds SP-8's floor under a fine pointer too (the FAQ's
  help line, the privacy link); the trail's wrapped rows and the FAQ's line of facts open so that targets meet without
  overlapping. **Probe** (390, touch, fr and ar, eight pages): 0 target under 44 × 44, 0 overlap.
- **A4** «Privacy Policy» says it is English: `lang="en"` in the error pages' way on; on the legal page the title is a
  run of its own — `<span lang="en" dir="ltr">` in the h1 and `lang="en"` in the trail (an `h1 lang="en"` would have
  left the Arabic page's reading edge) — and the official Italian title the same way (`lang="it"`).

**Found on the way, fixed (this family's).** The official Italian legal text read right to left on the Arabic page
(step 1's `browser-test/privacy-policy_ar_1440.png`: «.uno», «.Paragrafo due»; now `fix/browser-test/`, the same page
in order): its `lang` is the article's, and the rules that
keep a foreign text `ltr` read each element's own attribute. `[dir="rtl"] .lettura .legal-page[lang="it"]
.legal-page__body { direction: ltr; text-align: start }`; the courtesy translation (`aside lang="fr"`) stands as a
French quote's box — on the reading edge, its rule at its words' start.

### Not fixed, and why

- **m11** (one interior grammar for three partials): W3-F1's `_interior.css` is not on design-v5 (`1c03e3b`, W3-B the
  last merge) — the extraction waits for it, as the builder planned; the V5 empty state is W3-E's component to take.
- **m12** the CSRF failure stays Django's page: its sentence is B1 copy (the owner's packet); the frame is ready (the
  self-sufficient page).
- The letterhead footer's «Privacy Policy» / «Cookie Policy» (A4) and the signed-in letterhead's shift at 1440 (O1):
  W2-C1's, and the W4 performance sweep's.
- P1 and the steward's notes: the merge step's — below.

### For the merge (the steward)

- **DECISION_LOG:** this family's entries are DL54-77 (step 1), DL54-78 (step 2) and DL54-79 (this pass); design-v5 has
  its own DL54-78 … DL54-87 — renumber all three (DL54-78 had no row in the index; it has one now, beside DL54-79's).
  `dist/**` conflicts as binary: rebuild from clean.
- **Paths outside the slice** (`check_ownership.py w3-f2 design-v5`): step 1's and step 2's seven, and three of this
  pass — `apps/cms/static/cms/errori.css` (the error pages' sheet; page sheets are app entries, plan §2.3; its `dist`
  output generated), `apps/accounts/profile_forms.py` (A2: three widgets, no logic), `apps/news/forms.py` (one line:
  the consent's `label_lang` for the summary). `apps/core/views.py` to assign knowingly (the 400 / 500 render).
- **Weights** (gzip -9 from stdin, the review's measure): `dist/main.css` and the console bundles untouched by this
  pass (41 805 B on the branch, 41 155 B on the review's merged tree — the shared payload does not grow);
  `cms/lettura.css` 3 718 → **4 056 B**; `cms/servizio.css` 2 340 → **2 426 B**; `cms/errori.css` **3 619 B** (new: the
  error pages load it instead of servizio.css). Page types on the merged tree: a content page 41 155 + 4 056 =
  **45 211 B** (725 over the Wave-1 interior figure, 44 486 B), an error page **44 774 B** (288 over), an account page
  **43 581 B** (under). Page-only sheets are where V5.8 wants this CSS: record the page types as DL54-44, -73 and -76
  did (A11Y_PERF P1 has the timing on the twin; the door adds an image of 33–47 KB to the error pages' first screen,
  sized in its box from the first frame — no layout shift).
- **m8's rule for W3-F1** (its review's m7), as written here: `[dir="rtl"] :is(.page-header, .chapter__head) :is(p,
  div.page-header__lead):is([lang="fr"], [lang="it"]) { inline-size: fit-content; margin-inline-start: auto; }` —
  headings keep `text-align: end`.
- **Hand-offs:** W2-C1 (the footer's two policy names in English, `lang="en"`; O1), W4 (O1), W3-E (the empty state),
  B1 (the CSRF sentence; «Qui peut m’aider ?» above the live line).

### Tests (V5.5: smoke while building, targeted for the modules changed)

- **The family's unit files** — `tests/frontend/test_service_pages_w3_f2.py` 47 passed, `test_content_pages_w3_f2.py`
  50 passed. New or extended: the door at rest in every error page in four languages and in both frames (first in
  the page, the photograph's static files, the three steps, the key out of the lock, no light, nothing to reach), the
  two sheets' imports (the door on the error pages only, never in `main.css`), the door's rules (the key's box and
  turn, no motion, the end seat, logical properties, tokens only), the 403's `next` (encoded), «Privacy Policy»
  `lang="en"`, the profile's input purposes; the refused newsletter's summary inside `#newsletter` (fr, ar; the
  consent's `lang` in it), the news' filter, the legal trail and title runs, the official text's direction and the
  `.verifica` spacing, the newsletter's answers' way on and help line, a topic's glyph in its h1, the partial's new
  rules (M2, m8, m1, m6, m2).
- **Targeted, not browser** (one run, `TEST_DATABASE_URL=…/test_ile_v5_l4`): `tests/i18n/test_rtl_static.py`,
  `test_locked_texts.py`, `test_ui_translations.py`, `test_page_integrity.py`, `apps/news`, `apps/accounts`
  (`test_profile.py`, `test_privacy_workflows.py`), `apps/legal`, `apps/consents`, `apps/living`,
  `tests/compliance/test_public_pages.py`, `tests/frontend/test_layout.py`, `test_design_docs.py`,
  `test_css_bundle_is_current.py`, `test_static_pipeline.py`, `test_429_w2_b.py`, `test_icons.py`,
  `test_template_comments_do_not_leak.py`, `test_loader_rules.py`, `tests/test_check_ownership.py`: **434 passed**.
- **Browser** (one run, Chromium on the live server, `W3F2_SHOTS` → `fix/browser-test/`, 128 captures):
  `tests/frontend/test_service_pages_browser_w3_f2.py` (with the new door test: fr and ar, 1440 and 390, the 404 and
  the real 500), `test_content_pages_browser_w3_f2.py` (with the new tests: the Latin heads on the Arabic reading edge
  at 1440 and 390, the band on one line at 390 and 360, the hidden legend), `tests/i18n/test_rtl_browser.py`:
  **39 passed** in 6 min 35 s — no skip, no crash.
- `ruff check` clean on the changed Python (CI's lint); `ruff format` applied to the changed files.
- Not run: the full suite (V5.5: the integration checkpoint's).

### Lane state left behind (ile_v5_l4 only)

- Sessions minted with `Client.force_login` for qa-person and seed-company — **revoked** (2 rows deleted, the secrets
  file removed). The newsletter answers' two paths were read from a lane row (`@example.invalid`) into a file outside
  every repository and deleted after use; no evidence name or metrics line carries a token.
- No row written: the newsletter refusals stored nothing (no consent), the throttle counts in the server's memory.
  The lane server is stopped (8784 free); this pass's browser profiles removed.

---

## Merge step — the steward's note on numbering (12 October 2026; label w3-f2-merge)

The static pipeline's record (DL54-77), W3-B's entries with their merge's record (DL54-78 … DL54-87) and W2-A's
entries with theirs (DL54-88 … DL54-95) reached design-v5 first, so at the family's merge its three entries became
**DL54-96 … DL54-98** — the same order, add 19 —, their content unchanged: no entry cites another of the three, so only
the headings and the index's row numbers moved (the pre-merge sync, `f4f344e`). The steward's own record of the merge
is **DL54-99**. The code and DS 2026 cite none of the moved numbers.

How to read the numbers written before the merge — in this file, `REVIEW.md` and `A11Y_PERF.md` alike:

| Written | Read | The entry |
|---|---|---|
| DL54-77 | **DL54-96** | step 1: the content and legal pages as built — «la lettura» |
| DL54-78 | **DL54-97** | step 2: the error and account pages as built — «le pagine di servizio» |
| DL54-79 | **DL54-98** | the fix pass: the door at rest, the Latin heads of the Arabic pages, the refused newsletter |

The exceptions are design-v5's own numbers, unchanged: «design-v5 has its own DL54-77 …» (step 2's ownership list),
«its own DL54-78 … DL54-87» («For the merge») and «W3-B's DL54-78 … 87» (`REVIEW.md`, its notes for the steward);
every DL54-23, DL54-44 and DL54-47 is design-v5's.
