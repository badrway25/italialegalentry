# Locked blocks register — the Arabic policy (V5.27, FINAL_DELIVERY_V2 R7′ (a); lane AR)

Generated from `apps/cms/locked_renderings.py` (`board_rows()`, `counts()`) on 6 Nov 2026. Keys, classes, counts and reasons
only — no prescribed text, no personal datum (the French texts live in `apps/cms/locked_content.py`, byte-identical,
`locked_content.sha256.json` unchanged). Supersedes the class-C part of `evidence/v524/arabic/03_locked_blocks_register.md`
(«131 class-C keys», option B) wherever the two differ: R7′ prevails.

## 1. The four treatments

| class | treatment | reason |
|---|---|---|
| C-UI | provisional professional Arabic rendering on /ar/ (cms.locked_renderings.AR), no lang attribute; internal status PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW (dev board only) | non-legal compositional copy (V5.27 §1) |
| C-SUBST-IT | the Italian authoritative text shown and identified by the legal pages (apps/legal); the French courtesy never a fallback on /ar/ | legal text whose authoritative version is Italian (V5.27 §2) |
| C-SUBST-FR | French source on its own page, lang="fr" + the Arabic identification caption; elsewhere hidden behind one Arabic pointer line naming the source page | substantive content whose only source is the prescribed French (V5.27 §2) |
| C-OFFICIAL | kept in the original in every language, isolated (lang / bdi) | proper name / official title (V5.27 §3) |

## 2. Counts (texts of the registry + the one prescribed msgid)

| class | texts |
|---|---|
| C-UI | 139 |
| C-SUBST-IT | 59 |
| C-SUBST-FR | 34 |
| C-OFFICIAL | 17 |
| **total** | **249** |

The three figures of V5.27 §8: unintended French fallback on /ar/ **0** (the completeness crawl, with the burn-down
equality of `tests/i18n/arabic_allowlist.py` owned by the page lanes); provisional non-legal Arabic **139** texts;
untranslated authoritative legal blocks **34 C-SUBST-FR** texts (French source, identified on its page, hidden
elsewhere) + **6 C-SUBST-IT keys** (59 texts: titles, sections, paragraphs — the Italian authoritative text shown).

## 3. Key by key

| key | class | status | source page (route) |
|---|---|---|---|
| `legal.cookies.fr_courtesy.title` | C-SUBST-IT | ITALIAN AUTHORITATIVE TEXT — shown and identified by the legal pages | — |
| `legal.cookies.fr_courtesy.intro` | C-SUBST-IT | ITALIAN AUTHORITATIVE TEXT — shown and identified by the legal pages | — |
| `legal.cookies.fr_courtesy.sections[0].heading` | C-SUBST-IT | ITALIAN AUTHORITATIVE TEXT — shown and identified by the legal pages | — |
| `legal.cookies.fr_courtesy.sections[0].body` | C-SUBST-IT | ITALIAN AUTHORITATIVE TEXT — shown and identified by the legal pages | — |
| `legal.cookies.fr_courtesy.sections[1].heading` | C-SUBST-IT | ITALIAN AUTHORITATIVE TEXT — shown and identified by the legal pages | — |
| `legal.cookies.fr_courtesy.sections[1].body` | C-SUBST-IT | ITALIAN AUTHORITATIVE TEXT — shown and identified by the legal pages | — |
| `legal.cookies.fr_courtesy.sections[2].heading` | C-SUBST-IT | ITALIAN AUTHORITATIVE TEXT — shown and identified by the legal pages | — |
| `legal.cookies.fr_courtesy.sections[2].body` | C-SUBST-IT | ITALIAN AUTHORITATIVE TEXT — shown and identified by the legal pages | — |
| `legal.courtesy_notice.fr` | C-SUBST-IT | ITALIAN AUTHORITATIVE TEXT — shown and identified by the legal pages | — |
| `legal.disclaimer.fr_courtesy.title` | C-SUBST-IT | ITALIAN AUTHORITATIVE TEXT — shown and identified by the legal pages | — |
| `legal.disclaimer.fr_courtesy.intro` | C-SUBST-IT | ITALIAN AUTHORITATIVE TEXT — shown and identified by the legal pages | — |
| `legal.disclaimer.fr_courtesy.sections[0].heading` | C-SUBST-IT | ITALIAN AUTHORITATIVE TEXT — shown and identified by the legal pages | — |
| `legal.disclaimer.fr_courtesy.sections[0].body` | C-SUBST-IT | ITALIAN AUTHORITATIVE TEXT — shown and identified by the legal pages | — |
| `legal.disclaimer.fr_courtesy.sections[1].heading` | C-SUBST-IT | ITALIAN AUTHORITATIVE TEXT — shown and identified by the legal pages | — |
| `legal.disclaimer.fr_courtesy.sections[1].body` | C-SUBST-IT | ITALIAN AUTHORITATIVE TEXT — shown and identified by the legal pages | — |
| `legal.disclaimer.fr_courtesy.sections[2].heading` | C-SUBST-IT | ITALIAN AUTHORITATIVE TEXT — shown and identified by the legal pages | — |
| `legal.disclaimer.fr_courtesy.sections[2].body` | C-SUBST-IT | ITALIAN AUTHORITATIVE TEXT — shown and identified by the legal pages | — |
| `legal.notices.fr_courtesy.title` | C-SUBST-IT | ITALIAN AUTHORITATIVE TEXT — shown and identified by the legal pages | — |
| `legal.notices.fr_courtesy.intro` | C-SUBST-IT | ITALIAN AUTHORITATIVE TEXT — shown and identified by the legal pages | — |
| `legal.notices.fr_courtesy.sections[0].heading` | C-SUBST-IT | ITALIAN AUTHORITATIVE TEXT — shown and identified by the legal pages | — |
| `legal.notices.fr_courtesy.sections[0].body` | C-SUBST-IT | ITALIAN AUTHORITATIVE TEXT — shown and identified by the legal pages | — |
| `legal.notices.fr_courtesy.sections[1].heading` | C-SUBST-IT | ITALIAN AUTHORITATIVE TEXT — shown and identified by the legal pages | — |
| `legal.notices.fr_courtesy.sections[1].body` | C-SUBST-IT | ITALIAN AUTHORITATIVE TEXT — shown and identified by the legal pages | — |
| `legal.notices.fr_courtesy.sections[2].heading` | C-SUBST-IT | ITALIAN AUTHORITATIVE TEXT — shown and identified by the legal pages | — |
| `legal.notices.fr_courtesy.sections[2].body` | C-SUBST-IT | ITALIAN AUTHORITATIVE TEXT — shown and identified by the legal pages | — |
| `legal.notices.fr_courtesy.sections[3].heading` | C-SUBST-IT | ITALIAN AUTHORITATIVE TEXT — shown and identified by the legal pages | — |
| `legal.notices.fr_courtesy.sections[3].body` | C-SUBST-IT | ITALIAN AUTHORITATIVE TEXT — shown and identified by the legal pages | — |
| `legal.privacy.fr_courtesy.title` | C-SUBST-IT | ITALIAN AUTHORITATIVE TEXT — shown and identified by the legal pages | — |
| `legal.privacy.fr_courtesy.intro` | C-SUBST-IT | ITALIAN AUTHORITATIVE TEXT — shown and identified by the legal pages | — |
| `legal.privacy.fr_courtesy.sections[0].heading` | C-SUBST-IT | ITALIAN AUTHORITATIVE TEXT — shown and identified by the legal pages | — |
| `legal.privacy.fr_courtesy.sections[0].body` | C-SUBST-IT | ITALIAN AUTHORITATIVE TEXT — shown and identified by the legal pages | — |
| `legal.privacy.fr_courtesy.sections[1].heading` | C-SUBST-IT | ITALIAN AUTHORITATIVE TEXT — shown and identified by the legal pages | — |
| `legal.privacy.fr_courtesy.sections[1].body` | C-SUBST-IT | ITALIAN AUTHORITATIVE TEXT — shown and identified by the legal pages | — |
| `legal.privacy.fr_courtesy.sections[2].heading` | C-SUBST-IT | ITALIAN AUTHORITATIVE TEXT — shown and identified by the legal pages | — |
| `legal.privacy.fr_courtesy.sections[2].body` | C-SUBST-IT | ITALIAN AUTHORITATIVE TEXT — shown and identified by the legal pages | — |
| `legal.privacy.fr_courtesy.sections[3].heading` | C-SUBST-IT | ITALIAN AUTHORITATIVE TEXT — shown and identified by the legal pages | — |
| `legal.privacy.fr_courtesy.sections[3].body` | C-SUBST-IT | ITALIAN AUTHORITATIVE TEXT — shown and identified by the legal pages | — |
| `legal.privacy.fr_courtesy.sections[4].heading` | C-SUBST-IT | ITALIAN AUTHORITATIVE TEXT — shown and identified by the legal pages | — |
| `legal.privacy.fr_courtesy.sections[4].body` | C-SUBST-IT | ITALIAN AUTHORITATIVE TEXT — shown and identified by the legal pages | — |
| `legal.privacy.fr_courtesy.sections[5].heading` | C-SUBST-IT | ITALIAN AUTHORITATIVE TEXT — shown and identified by the legal pages | — |
| `legal.privacy.fr_courtesy.sections[5].body` | C-SUBST-IT | ITALIAN AUTHORITATIVE TEXT — shown and identified by the legal pages | — |
| `legal.privacy.fr_courtesy.sections[6].heading` | C-SUBST-IT | ITALIAN AUTHORITATIVE TEXT — shown and identified by the legal pages | — |
| `legal.privacy.fr_courtesy.sections[6].body` | C-SUBST-IT | ITALIAN AUTHORITATIVE TEXT — shown and identified by the legal pages | — |
| `legal.privacy.fr_courtesy.sections[7].heading` | C-SUBST-IT | ITALIAN AUTHORITATIVE TEXT — shown and identified by the legal pages | — |
| `legal.privacy.fr_courtesy.sections[7].body` | C-SUBST-IT | ITALIAN AUTHORITATIVE TEXT — shown and identified by the legal pages | — |
| `legal.terms.fr_courtesy.title` | C-SUBST-IT | ITALIAN AUTHORITATIVE TEXT — shown and identified by the legal pages | — |
| `legal.terms.fr_courtesy.intro` | C-SUBST-IT | ITALIAN AUTHORITATIVE TEXT — shown and identified by the legal pages | — |
| `legal.terms.fr_courtesy.sections[0].heading` | C-SUBST-IT | ITALIAN AUTHORITATIVE TEXT — shown and identified by the legal pages | — |
| `legal.terms.fr_courtesy.sections[0].body` | C-SUBST-IT | ITALIAN AUTHORITATIVE TEXT — shown and identified by the legal pages | — |
| `legal.terms.fr_courtesy.sections[1].heading` | C-SUBST-IT | ITALIAN AUTHORITATIVE TEXT — shown and identified by the legal pages | — |
| `legal.terms.fr_courtesy.sections[1].body` | C-SUBST-IT | ITALIAN AUTHORITATIVE TEXT — shown and identified by the legal pages | — |
| `legal.terms.fr_courtesy.sections[2].heading` | C-SUBST-IT | ITALIAN AUTHORITATIVE TEXT — shown and identified by the legal pages | — |
| `legal.terms.fr_courtesy.sections[2].body` | C-SUBST-IT | ITALIAN AUTHORITATIVE TEXT — shown and identified by the legal pages | — |
| `legal.terms.fr_courtesy.sections[3].heading` | C-SUBST-IT | ITALIAN AUTHORITATIVE TEXT — shown and identified by the legal pages | — |
| `legal.terms.fr_courtesy.sections[3].body` | C-SUBST-IT | ITALIAN AUTHORITATIVE TEXT — shown and identified by the legal pages | — |
| `legal.terms.fr_courtesy.sections[4].heading` | C-SUBST-IT | ITALIAN AUTHORITATIVE TEXT — shown and identified by the legal pages | — |
| `legal.terms.fr_courtesy.sections[4].body` | C-SUBST-IT | ITALIAN AUTHORITATIVE TEXT — shown and identified by the legal pages | — |
| `legal.terms.fr_courtesy.sections[5].heading` | C-SUBST-IT | ITALIAN AUTHORITATIVE TEXT — shown and identified by the legal pages | — |
| `legal.terms.fr_courtesy.sections[5].body` | C-SUBST-IT | ITALIAN AUTHORITATIVE TEXT — shown and identified by the legal pages | — |
| `p1.companies.form.button` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p1.companies.form.consent` | C-SUBST-FR | SOURCE TEXT (FR) — identified on its page, hidden elsewhere until validated | enquiries:company_needs, ecosystem:companies |
| `p1.companies.form.fields[0]` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p1.companies.form.fields[1]` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p1.companies.form.fields[2]` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p1.companies.form.fields[3]` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p1.companies.form.fields[4]` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p1.companies.form.fields[5]` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p1.companies.form.fields[6]` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p1.companies.form.fields[7]` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p1.companies.form.fields[8]` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p1.companies.form.fields[9]` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p1.companies.form.fields[10]` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p1.companies.form.fields[11]` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p1.companies.form.fields[12]` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p1.companies.form.fields[13]` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p1.companies.intro` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p1.companies.quote` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p1.companies.title` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p1.email.public_contact` | C-OFFICIAL | ORIGINAL — kept in every language | — |
| `p1.persons.replacement_1` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p1.persons.replacement_2` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p1.trademark.mark` | C-OFFICIAL | ORIGINAL — kept in every language | — |
| `p1.trademark.words_fr` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p1.trademark.words_it` | C-OFFICIAL | ORIGINAL — kept in every language | — |
| `p2.forum.audience.body` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p2.forum.audience.title` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p2.forum.header.meta` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p2.forum.header.patronage` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p2.forum.header.subtitle` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p2.forum.header.title` | C-OFFICIAL | ORIGINAL — kept in every language | — |
| `p2.forum.objectives.body` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p2.forum.objectives.title` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p2.forum.programme.items[0]` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p2.forum.programme.items[1]` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p2.forum.programme.items[2]` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p2.forum.programme.items[3]` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p2.forum.programme.items[4]` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p2.forum.programme.items[5]` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p2.forum.programme.items[6]` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p2.forum.programme.items[7]` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p2.forum.programme.note` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p2.forum.programme.title` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p2.forum.registration.button_primary` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p2.forum.registration.button_secondary_collab` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p2.forum.registration.button_secondary_pilot` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p2.forum.registration.categories[0]` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p2.forum.registration.categories[1]` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p2.forum.registration.categories[2]` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p2.forum.registration.categories[3]` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p2.forum.registration.categories[4]` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p2.forum.registration.categories[5]` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p2.forum.registration.categories[6]` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p2.forum.registration.categories[7]` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p2.forum.registration.category_label` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p2.forum.registration.consent` | C-SUBST-FR | SOURCE TEXT (FR) — identified on its page, hidden elsewhere until validated | forum:register |
| `p2.forum.registration.fields[0]` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p2.forum.registration.fields[1]` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p2.forum.registration.fields[2]` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p2.forum.registration.fields[3]` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p2.forum.registration.fields[4]` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p2.forum.registration.fields[5]` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p2.forum.registration.fields[6]` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p2.forum.registration.intro` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p2.forum.registration.sector_label` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p2.forum.registration.title` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p2.forum.speakers.body` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p2.forum.speakers.roles[0]` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p2.forum.speakers.roles[1]` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p2.forum.speakers.roles[2]` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p2.forum.speakers.roles[3]` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p2.forum.speakers.title` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p2.forum.what.body[0]` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p2.forum.what.body[1]` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p2.forum.what.body[2]` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p2.forum.what.title` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p2.forum.who.body` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p2.forum.who.title` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p2.forum.why.body` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p2.forum.why.title` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p2.home.banner.button` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p2.home.banner.meta` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p2.home.banner.quote` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p2.home.banner.title` | C-OFFICIAL | ORIGINAL — kept in every language | — |
| `p3.antifraud.body` | C-SUBST-FR | SOURCE TEXT (FR) — identified on its page, hidden elsewhere until validated | pages:antifraud |
| `p3.antifraud.title` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.diplomas.body` | C-SUBST-FR | SOURCE TEXT (FR) — identified on its page, hidden elsewhere until validated | pathways:diplomas |
| `p3.diplomas.title` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.entrances.company.button` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.entrances.company.text` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.entrances.company.title` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.entrances.institution.button` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.entrances.institution.text` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.entrances.institution.title` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.entrances.person.button` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.entrances.person.text` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.entrances.person.title` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.entrances.university.button` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.entrances.university.text` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.entrances.university.title` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.faq.items[0].question` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.faq.items[0].answer` | C-SUBST-FR | SOURCE TEXT (FR) — identified on its page, hidden elsewhere until validated | faq:index |
| `p3.faq.items[1].question` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.faq.items[1].answer` | C-SUBST-FR | SOURCE TEXT (FR) — identified on its page, hidden elsewhere until validated | faq:index |
| `p3.faq.items[2].question` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.faq.items[2].answer` | C-SUBST-FR | SOURCE TEXT (FR) — identified on its page, hidden elsewhere until validated | faq:index |
| `p3.faq.items[3].question` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.faq.items[3].answer` | C-SUBST-FR | SOURCE TEXT (FR) — identified on its page, hidden elsewhere until validated | faq:index |
| `p3.faq.items[4].question` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.faq.items[4].answer` | C-SUBST-FR | SOURCE TEXT (FR) — identified on its page, hidden elsewhere until validated | faq:index |
| `p3.faq.items[5].question` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.faq.items[5].answer` | C-SUBST-FR | SOURCE TEXT (FR) — identified on its page, hidden elsewhere until validated | faq:index |
| `p3.faq.items[6].question` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.faq.items[6].answer` | C-SUBST-FR | SOURCE TEXT (FR) — identified on its page, hidden elsewhere until validated | faq:index |
| `p3.faq.items[7].question` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.faq.items[7].answer` | C-SUBST-FR | SOURCE TEXT (FR) — identified on its page, hidden elsewhere until validated | faq:index |
| `p3.faq.items[8].question` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.faq.items[8].answer` | C-SUBST-FR | SOURCE TEXT (FR) — identified on its page, hidden elsewhere until validated | faq:index |
| `p3.glossary.terms[0].term` | C-OFFICIAL | ORIGINAL — kept in every language | — |
| `p3.glossary.terms[0].definition` | C-SUBST-FR | SOURCE TEXT (FR) — identified on its page, hidden elsewhere until validated | glossary:index, glossary:term |
| `p3.glossary.terms[1].term` | C-OFFICIAL | ORIGINAL — kept in every language | — |
| `p3.glossary.terms[1].definition` | C-SUBST-FR | SOURCE TEXT (FR) — identified on its page, hidden elsewhere until validated | glossary:index, glossary:term |
| `p3.glossary.terms[2].term` | C-OFFICIAL | ORIGINAL — kept in every language | — |
| `p3.glossary.terms[2].definition` | C-SUBST-FR | SOURCE TEXT (FR) — identified on its page, hidden elsewhere until validated | glossary:index, glossary:term |
| `p3.glossary.terms[3].term` | C-OFFICIAL | ORIGINAL — kept in every language | — |
| `p3.glossary.terms[3].definition` | C-SUBST-FR | SOURCE TEXT (FR) — identified on its page, hidden elsewhere until validated | glossary:index, glossary:term |
| `p3.glossary.terms[4].term` | C-OFFICIAL | ORIGINAL — kept in every language | — |
| `p3.glossary.terms[4].definition` | C-SUBST-FR | SOURCE TEXT (FR) — identified on its page, hidden elsewhere until validated | glossary:index, glossary:term |
| `p3.glossary.terms[5].term` | C-OFFICIAL | ORIGINAL — kept in every language | — |
| `p3.glossary.terms[5].definition` | C-SUBST-FR | SOURCE TEXT (FR) — identified on its page, hidden elsewhere until validated | glossary:index, glossary:term |
| `p3.glossary.terms[6].term` | C-OFFICIAL | ORIGINAL — kept in every language | — |
| `p3.glossary.terms[6].definition` | C-SUBST-FR | SOURCE TEXT (FR) — identified on its page, hidden elsewhere until validated | glossary:index, glossary:term |
| `p3.glossary.terms[7].term` | C-OFFICIAL | ORIGINAL — kept in every language | — |
| `p3.glossary.terms[7].definition` | C-SUBST-FR | SOURCE TEXT (FR) — identified on its page, hidden elsewhere until validated | glossary:index, glossary:term |
| `p3.glossary.terms[8].term` | C-OFFICIAL | ORIGINAL — kept in every language | — |
| `p3.glossary.terms[8].definition` | C-SUBST-FR | SOURCE TEXT (FR) — identified on its page, hidden elsewhere until validated | glossary:index, glossary:term |
| `p3.glossary.terms[9].term` | C-OFFICIAL | ORIGINAL — kept in every language | — |
| `p3.glossary.terms[9].definition` | C-SUBST-FR | SOURCE TEXT (FR) — identified on its page, hidden elsewhere until validated | glossary:index, glossary:term |
| `p3.hero.body` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.hero.subtitle` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.hero.title` | C-OFFICIAL | ORIGINAL — kept in every language | — |
| `p3.institutions.button` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.institutions.intro` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.institutions.recipients` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.living.body` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.living.title` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.news.body` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.news.newsletter_consent` | C-SUBST-FR | SOURCE TEXT (FR) — identified on its page, hidden elsewhere until validated | news:index |
| `p3.news.newsletter_label` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.news.title` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.persons.how_it_works` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.persons.intro` | C-SUBST-FR | SOURCE TEXT (FR) — identified on its page, hidden elsewhere until validated | pathways:index |
| `p3.persons.pathways[0].title` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.persons.pathways[0].description` | C-SUBST-FR | SOURCE TEXT (FR) — identified on its page, hidden elsewhere until validated | pathways:detail |
| `p3.persons.pathways[1].title` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.persons.pathways[1].description` | C-SUBST-FR | SOURCE TEXT (FR) — identified on its page, hidden elsewhere until validated | pathways:detail |
| `p3.persons.pathways[2].title` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.persons.pathways[2].description` | C-SUBST-FR | SOURCE TEXT (FR) — identified on its page, hidden elsewhere until validated | pathways:detail |
| `p3.persons.pathways[3].title` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.persons.pathways[3].description` | C-SUBST-FR | SOURCE TEXT (FR) — identified on its page, hidden elsewhere until validated | pathways:detail |
| `p3.persons.pathways[4].title` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.persons.pathways[4].description` | C-SUBST-FR | SOURCE TEXT (FR) — identified on its page, hidden elsewhere until validated | pathways:detail |
| `p3.persons.pathways[5].title` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.persons.pathways[5].description` | C-SUBST-FR | SOURCE TEXT (FR) — identified on its page, hidden elsewhere until validated | pathways:detail |
| `p3.persons.pathways[6].title` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.persons.pathways[6].description` | C-SUBST-FR | SOURCE TEXT (FR) — identified on its page, hidden elsewhere until validated | pathways:detail |
| `p3.persons.pathways[7].title` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.persons.pathways[7].description` | C-SUBST-FR | SOURCE TEXT (FR) — identified on its page, hidden elsewhere until validated | pathways:detail |
| `p3.persons.title` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.pilot.body` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.pilot.sequence[0]` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.pilot.sequence[1]` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.pilot.sequence[2]` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.pilot.sequence[3]` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.pilot.sequence[4]` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.pilot.sequence[5]` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.pilot.sequence[6]` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.pilot.sequence[7]` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.pilot.title` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.reserved.body` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.reserved.button` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.reserved.title` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.training_after.body` | C-SUBST-FR | SOURCE TEXT (FR) — identified on its page, hidden elsewhere until validated | pathways:training |
| `p3.training_after.title` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.universities.button` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.universities.intro` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.virtual_forum.body` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.virtual_forum.button` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `p3.virtual_forum.title` | C-UI | PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW | — |
| `FORUM PERMANENT VÉNÉTIE–MAROC` | C-OFFICIAL | ORIGINAL — kept in every language | the prescribed title of the permanent Forum (I18N_RTL §9) |
