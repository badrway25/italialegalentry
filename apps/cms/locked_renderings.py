"""
The Arabic rendering policy of the prescribed texts (V5.27 «ARABIC OWNER DECISION — FINAL», 5 Nov 2026;
FINAL_DELIVERY_V2.md R7′ and §3.8; lane AR, label v524-ar).

The registry (``cms.locked_content``) keeps every prescribed French text byte for byte, with its checksum. This module
holds, BESIDE it, what the Arabic product does with each text — never a change to the text itself:

* **C-UI** — compositional, non-legal copy (titles, entrances, buttons, the pilot's words, the Forum's institutional
  copy, the FAQ questions and its informational answers, the form labels …): a PROVISIONAL professional Arabic
  rendering, served on ``/ar/`` as the page's own text (no ``lang`` attribute), flagged ``STATUS_PROVISIONAL`` here
  and on the dev board — never on the public UI;
* **C-SUBST-FR** — substantive content whose only source is the prescribed French (the FAQ's substantive answers,
  the glossary definitions, the pathways' descriptions, the anti-fraud and diplomas bodies, the persons' intro, the
  consent sentences): on its OWN source page the French stands, isolated (``lang="fr"``) and identified by a caption;
  on every other page that quotes it the French body is HIDDEN until validated and one Arabic line points to the
  source page;
* **C-SUBST-IT** — the legal texts whose authoritative version is Italian (the ``legal.*`` courtesy translations): the
  legal pages show the Italian and identify it (``apps/legal``); the French courtesy is never a fallback on ``/ar/``;
* **C-OFFICIAL** — official titles and proper names kept in the original in every language (the trademark, the Forum's
  name, the e-mail address, the Italian terms of the glossary).

No French text is reworded, machine-translated or moved (V5.12 …); ``locked_content.sha256.json`` is untouched. Italian
and English keep today's behaviour (the French source with ``lang="fr"``): the owner's decision is Arabic (R7′ (1)).

How the policy reaches a page — ONE seam: ``locked_content.get(key, lang)`` asks ``resolve_value`` first, so every
reader of the registry (the ``{% locked %}`` tag, the services, the forms, the menu) gets the rendering, the pointer
line or the French source with the right effective language without a change of its own. The «on its source page» rule
needs the current route: ``request_started`` hands this module the request's path (a context variable), resolved lazily
to a URL name. Outside a request (a shell, a seed, a test calling the registry directly) the French stands, as before.

Sub-keys address one text of a compound value, as the register names them: ``p3.faq.items[0].question``,
``p3.persons.pathways[3].title``, ``p3.pilot.sequence[2]`` — ``locked_content.get()`` accepts them, so a page lane that
composes a compound key part by part (a title in Arabic beside a description kept as source) reads each part with its
own treatment.

Register of every key, with its class and treatment: ``docs/design-v5/QA/v524/ar/LOCKED_BLOCKS_REGISTER.md``.
"""

from __future__ import annotations

import contextvars
import re
from typing import Any

from django.core.signals import request_finished, request_started
from django.urls import Resolver404, resolve
from django.utils.translation import gettext_lazy, pgettext_lazy

# --------------------------------------------------------------------------------------------
# The four treatments (V5.27 §1–§3; R7′ (1)–(4))
# --------------------------------------------------------------------------------------------
C_UI = "C-UI"
C_SUBST_IT = "C-SUBST-IT"
C_SUBST_FR = "C-SUBST-FR"
C_OFFICIAL = "C-OFFICIAL"
TREATMENTS = (C_UI, C_SUBST_IT, C_SUBST_FR, C_OFFICIAL)

#: the status of every C-UI rendering — internal (the dev board, this module); nothing on the public UI says it
STATUS_PROVISIONAL = "PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW"
STATUS_SOURCE = "SOURCE TEXT (FR) — identified on its page, hidden elsewhere until validated"
STATUS_ITALIAN = "ITALIAN AUTHORITATIVE TEXT — shown and identified by the legal pages"
STATUS_ORIGINAL = "ORIGINAL — kept in every language"
STATUS_OF = {
    C_UI: STATUS_PROVISIONAL,
    C_SUBST_FR: STATUS_SOURCE,
    C_SUBST_IT: STATUS_ITALIAN,
    C_OFFICIAL: STATUS_ORIGINAL,
}

#: the one language the renderings are served in (R7′ (1): «the decision is Arabic; it/en keep today's behaviour»)
RENDERED_LANGUAGE = "ar"
SOURCE_LANGUAGE = "fr"

#: a list item in a pattern: ``p3.faq.items[].answer`` stands for every ``p3.faq.items[<n>].answer``
_INDEX = re.compile(r"\[\d+\]")
#: a text leaf's path inside a compound value, as the register writes it: ``[0]``, ``.question``
_STEP = re.compile(r"\[(\d+)\]|\.([a-z_]+)")
#: dict fields that are identifiers, never text (the FAQ's, the pathways' and the terms' ``key``)
IDENTIFIER_FIELDS = frozenset({"key"})

#: every text of the registry, by key, by pattern or by sub-key (a sub-key's own row wins over its pattern's) → its
#: treatment. Total:
#: ``tests/i18n/test_locked_renderings_v524.py``
#: asserts that each string leaf of ``LOCKED_TEXTS["fr"]`` resolves to exactly one class.
TREATMENT: dict[str, str] = {
    # ---- Phase 1 ------------------------------------------------------------------------------------------
    "p1.companies.title": C_UI,
    "p1.companies.intro": C_UI,
    "p1.companies.quote": C_UI,
    "p1.companies.form.fields[]": C_UI,
    "p1.companies.form.consent": C_SUBST_FR,
    "p1.companies.form.button": C_UI,
    "p1.persons.replacement_1": C_UI,
    "p1.persons.replacement_2": C_UI,
    "p1.trademark.mark": C_OFFICIAL,
    "p1.trademark.words_fr": C_UI,
    "p1.trademark.words_it": C_OFFICIAL,
    "p1.email.public_contact": C_OFFICIAL,
    # ---- Phase 2 — the Forum ------------------------------------------------------------------------------
    "p2.forum.header.title": C_OFFICIAL,
    "p2.forum.header.subtitle": C_UI,
    "p2.forum.header.meta": C_UI,
    "p2.forum.header.patronage": C_UI,
    "p2.forum.who.title": C_UI,
    "p2.forum.who.body": C_UI,
    "p2.forum.why.title": C_UI,
    "p2.forum.why.body": C_UI,
    "p2.forum.what.title": C_UI,
    "p2.forum.what.body[]": C_UI,
    "p2.forum.objectives.title": C_UI,
    "p2.forum.objectives.body": C_UI,
    "p2.forum.audience.title": C_UI,
    "p2.forum.audience.body": C_UI,
    "p2.forum.programme.title": C_UI,
    "p2.forum.programme.items[]": C_UI,
    "p2.forum.programme.note": C_UI,
    "p2.forum.speakers.title": C_UI,
    "p2.forum.speakers.body": C_UI,
    "p2.forum.speakers.roles[]": C_UI,
    "p2.forum.registration.title": C_UI,
    "p2.forum.registration.intro": C_UI,
    "p2.forum.registration.fields[]": C_UI,
    "p2.forum.registration.category_label": C_UI,
    "p2.forum.registration.categories[]": C_UI,
    "p2.forum.registration.sector_label": C_UI,
    "p2.forum.registration.consent": C_SUBST_FR,
    "p2.forum.registration.button_primary": C_UI,
    "p2.forum.registration.button_secondary_pilot": C_UI,
    "p2.forum.registration.button_secondary_collab": C_UI,
    "p2.home.banner.title": C_OFFICIAL,
    "p2.home.banner.meta": C_UI,
    "p2.home.banner.quote": C_UI,
    "p2.home.banner.button": C_UI,
    # ---- Phase 3 ------------------------------------------------------------------------------------------
    "p3.hero.title": C_OFFICIAL,  # the trademark itself, the visible H1 (Q1)
    "p3.hero.subtitle": C_UI,
    "p3.hero.body": C_UI,
    "p3.entrances.person.title": C_UI,
    "p3.entrances.person.text": C_UI,
    "p3.entrances.person.button": C_UI,
    "p3.entrances.company.title": C_UI,
    "p3.entrances.company.text": C_UI,
    "p3.entrances.company.button": C_UI,
    "p3.entrances.institution.title": C_UI,
    "p3.entrances.institution.text": C_UI,
    "p3.entrances.institution.button": C_UI,
    "p3.entrances.university.title": C_UI,
    "p3.entrances.university.text": C_UI,
    "p3.entrances.university.button": C_UI,
    "p3.persons.title": C_UI,
    "p3.persons.intro": C_SUBST_FR,
    "p3.persons.pathways[].title": C_UI,
    "p3.persons.pathways[].description": C_SUBST_FR,
    "p3.persons.how_it_works": C_UI,
    "p3.institutions.intro": C_UI,
    "p3.institutions.recipients": C_UI,
    "p3.institutions.button": C_UI,
    "p3.universities.intro": C_UI,
    "p3.universities.button": C_UI,
    "p3.pilot.title": C_UI,
    "p3.pilot.body": C_UI,
    "p3.pilot.sequence[]": C_UI,
    "p3.antifraud.title": C_UI,
    "p3.antifraud.body": C_SUBST_FR,
    "p3.faq.items[].question": C_UI,
    "p3.faq.items[].answer": C_SUBST_FR,
    # the owner's decision of 10 Nov 2026 (DL54-211: «the Arabic FAQ must not normally show French answers»): each
    # answer by what it says — informational or product copy (what the platform does and does not do, who promotes it,
    # the advice against a «guaranteed» visa) reads its professional Arabic; a legal or substantive answer without a
    # validated Arabic translation (no labour intermediation, the decreto flussi as an act, the effect of a prior
    # refusal, the data protection commitment) keeps the pattern's treatment: its French source, identified on its page
    "p3.faq.items[0].answer": C_UI,  # faq_visas
    "p3.faq.items[2].answer": C_UI,  # faq_preassessment_guarantee
    "p3.faq.items[4].answer": C_UI,  # faq_diplomas
    "p3.faq.items[6].answer": C_UI,  # faq_who
    "p3.faq.items[8].answer": C_UI,  # faq_guaranteed_visa_offer
    "p3.glossary.terms[].term": C_OFFICIAL,  # the Italian term, kept Italian in every language (I18N_RTL §9)
    "p3.glossary.terms[].definition": C_SUBST_FR,
    "p3.living.title": C_UI,
    "p3.living.body": C_UI,
    "p3.training_after.title": C_UI,
    "p3.training_after.body": C_SUBST_FR,
    "p3.news.title": C_UI,
    "p3.news.body": C_UI,
    "p3.news.newsletter_label": C_UI,
    "p3.news.newsletter_consent": C_SUBST_FR,
    "p3.virtual_forum.title": C_UI,
    "p3.virtual_forum.body": C_UI,
    "p3.virtual_forum.button": C_UI,
    "p3.diplomas.title": C_UI,
    "p3.diplomas.body": C_SUBST_FR,
    "p3.reserved.title": C_UI,
    "p3.reserved.body": C_UI,
    "p3.reserved.button": C_UI,
    # ---- the legal courtesy translations: the Italian is authoritative (V5.27 §2; apps/legal shows and names it) -----
    "legal.courtesy_notice.fr": C_SUBST_IT,
    "legal.privacy.fr_courtesy": C_SUBST_IT,
    "legal.cookies.fr_courtesy": C_SUBST_IT,
    "legal.notices.fr_courtesy": C_SUBST_IT,
    "legal.terms.fr_courtesy": C_SUBST_IT,
    "legal.disclaimer.fr_courtesy": C_SUBST_IT,
}

#: the prescribed title of the permanent Forum (a catalogue msgid, apps/forum/services.py PERMANENT_TITLE — not a
#: registry key): C-OFFICIAL, kept in French in every language, isolated by the template (register row 131)
OFFICIAL_MSGIDS: dict[str, str] = {
    "FORUM PERMANENT VÉNÉTIE–MAROC": "the prescribed title of the permanent Forum (I18N_RTL §9)"
}

#: a C-SUBST-FR text's OWN page(s), by URL name: there the French stands with its caption; anywhere else it is hidden
SOURCE_ROUTES: dict[str, tuple[str, ...]] = {
    "p1.companies.form.consent": ("enquiries:company_needs", "ecosystem:companies"),
    "p2.forum.registration.consent": ("forum:register",),
    "p3.news.newsletter_consent": ("news:index", "news:newsletter_subscribe"),
    "p3.persons.intro": ("pathways:index",),
    "p3.persons.pathways[].description": ("pathways:detail",),
    "p3.antifraud.body": ("pages:antifraud",),
    "p3.faq.items[].answer": ("faq:index",),
    "p3.glossary.terms[].definition": ("glossary:index", "glossary:term"),
    "p3.training_after.body": ("pathways:training",),
    "p3.diplomas.body": ("pathways:diplomas",),
}

#: a team wording DERIVED from a C-SUBST-FR text (its opening clause, never retyped: consents.services
#: ACKNOWLEDGEMENT_TEXT, the acknowledgement of the notice on the forms of category A, V5.16 §3) → the forms it
#: belongs to: there, on /ar/, it stands in French identified by the source text's caption (V5.27 / R7′ (3);
#: FINAL_DELIVERY_V2 §3.9, AR NOTES §4 «CLOSING»), never translated — the consent record keeps the French it shows
#: V5.32 (lane D, 12 Nov 2026): the contact form also stands on the contact page itself («lo sportello»,
#: templates/enquiries/partials/sportello_form.html — the same enquiries ContactForm, posting to enquiries:contact)
DERIVED_ROUTES: dict[str, tuple[str, ...]] = {
    "p1.companies.form.consent": (
        "enquiries:contact",
        "pages:contact",
        "enquiries:institution_proposal",
        "enquiries:university_proposal",
    ),
}

#: the source page's name, said in the pointer line («the source text is on the page …») — the catalogue's own words
SOURCE_PAGE_NAME: dict[str, Any] = {
    "p1.companies.form.consent": gettext_lazy("Recueil des besoins"),
    "p2.forum.registration.consent": gettext_lazy("Inscription"),
    "p3.news.newsletter_consent": gettext_lazy("Actualités"),
    "p3.persons.intro": gettext_lazy("Espace Personnes"),
    "p3.persons.pathways[].description": gettext_lazy("Consulter la page du parcours"),
    "p3.antifraud.body": gettext_lazy("Attention aux fraudes"),
    "p3.faq.items[].answer": gettext_lazy("Questions fréquentes"),
    "p3.glossary.terms[].definition": gettext_lazy("Glossaire"),
    "p3.training_after.body": gettext_lazy("Formation"),
    "p3.diplomas.body": gettext_lazy("Diplômes et titres"),
}

#: compound keys whose WHOLE value keeps the French on /ar/ although their parts have renderings: their readers compose
#: the parts from a French read of their own (``pathways.models.locked_pathway_entries()`` →
#: ``pathways.services.index_entries()``) and probe this key only for the ``lang`` attribute — a whole-value rendering
#: would untag French titles on the home and on /parcours/. The page lanes read the parts
#: (``p3.persons.pathways[<n>].title`` …) through ``locked_content.get``; the lane that converts the readers removes the
#: key here (QA/v524/ar/NOTES.md §4, the contract items for HOME and PUB1).
DEFERRED_WHOLE: dict[str, str] = {}
#: (empty since lane CLOSING, FINAL_DELIVERY_V2 §3.9: the home's reader, pages.services.build_pathways, reads the
#: pathways' parts by their sub-keys like PUB1's readers — the whole key renders: titles in their provisional Arabic,
#: descriptions as their pointer line off their own page)

# --------------------------------------------------------------------------------------------
# The provisional professional Arabic renderings of the C-UI texts (native reader's second pass, 6 Nov 2026). Register:
# formal institutional Arabic, the plural of courtesy (أنتم), Arabic punctuation «، ؛ ؟», Western digits, a Latin run
# that ends a clause followed by U+200E (LRM) so the Arabic punctuation stays in place; the brand «Italy Legal Entry»
# and the proper name «Vénétie–Maroc» as the catalogue already writes them; the pilot «المشروع التجريبي» and the
# anti-fraud «احذروا الاحتيال» as the catalogue already says them. A rendering shaped by a cut (the «Comment ça marche»
# route, the Forum's objectives and audience) keeps the separators the cut reads.
# --------------------------------------------------------------------------------------------
LRM = "‎"
AR: dict[str, str] = {
    # ---- Phase 1 — Espace Entreprises ----------------------------------------------------------------------
    "p1.companies.title": "ما الملامح المهنية التي تحتاجها شركتكم؟",
    "p1.companies.intro": (
        "تجمع Italy Legal Entry‎ الاحتياجات المهنية للشركات الإيطالية لبناء مسارات نظامية للتكوين والتنقل بالتعاون "
        "مع الفاعلين المختصين. أعلِمونا باحتياجات شركتكم: سيُعاد الاتصال بكم لتعميق أوجه التعاون الممكنة في إطار "
        "المشروع."
    ),
    "p1.companies.quote": (
        "«ننطلق من الاحتياجات الفعلية للشركات الإيطالية، ونبني مع الفاعلين المختصين مسارات نظامية للتكوين والتنقل.»"
    ),
    "p1.companies.form.fields[0]": "الاسم القانوني للشركة",
    "p1.companies.form.fields[1]": "قطاع النشاط",
    "p1.companies.form.fields[2]": "المقر (البلدية والمقاطعة)",
    "p1.companies.form.fields[3]": "اسم الشخص المرجعي ووظيفته",
    "p1.companies.form.fields[4]": "البريد الإلكتروني",
    "p1.companies.form.fields[5]": "الهاتف",
    "p1.companies.form.fields[6]": "الملامح المهنية التي تحتاجها الشركة",
    "p1.companies.form.fields[7]": "العدد التقريبي للأشخاص",
    "p1.companies.form.fields[8]": "المؤهلات والكفاءات المطلوبة",
    "p1.companies.form.fields[9]": "الخبرة المطلوبة",
    "p1.companies.form.fields[10]": "المتطلبات اللغوية",
    "p1.companies.form.fields[11]": "احتياجات التكوين",
    "p1.companies.form.fields[12]": "الجدول الزمني التقريبي",
    "p1.companies.form.fields[13]": "ملاحظات (حقل حر)",
    "p1.companies.form.button": "أعربوا عن اهتمامكم بالمشروع",
    "p1.persons.replacement_1": "التوجيه نحو مسارات للتكوين والتنقل النظامي، مبنية مع الفاعلين المختصين",
    "p1.persons.replacement_2": "جمع احتياجات الشركات وبناء مسارات نظامية للتكوين والتنقل",
    "p1.trademark.words_fr": "علامة مسجَّلة",
    # ---- Phase 2 — the Forum --------------------------------------------------------------------------------
    "p2.forum.header.subtitle": "حوار قانوني وتعاون اقتصادي وتنقل نظامي",
    "p2.forum.header.meta": "روفيغو — 2 أكتوبر 2026 — Sala della Gran Guardia‎ — من 15:00 إلى 18:00",
    "p2.forum.header.patronage": "تحت رعاية منطقة فينيتو وبلدية روفيغو",
    "p2.forum.who.title": "من نحن",
    "p2.forum.who.body": (
        "ينظَّم المنتدى بمبادرة من جمعية AGAMI — Dialogo Giuridico Interculturale APS‎، وهي جمعية حقوقيين تعمل منذ "
        "2011 "
        "في مجال الحوار القانوني بين إيطاليا والمغرب، في إطار مشروع Italy Legal Entry™‎: منظومة مخصصة للتوجيه والتكوين "
        "قبل المغادرة ومواكبة المسارات النظامية نحو إيطاليا، بُنيت بمساهمة مهنيين وشركات ومؤسسات وجامعات وهيئات تكوين."
    ),
    "p2.forum.why.title": "لماذا Italy Legal Entry‎",
    "p2.forum.why.body": (
        "كثيرًا ما يُترك التنقل نحو إيطاليا لقنوات عشوائية وللتضليل ولوسطاء غير مؤهلين. وقد نشأت Italy Legal Entry‎ "
        "لتقديم البديل: مسارات نظامية ومنظَّمة وشفافة، تنطلق من الاحتياجات الفعلية للشركات الإيطالية وتقوم على التوجيه "
        "والتكوين في بلد المنشأ والمواكبة المهنية، في احترام تام للتشريعات الإيطالية والأوروبية. فالشرعية ليست قيدًا: "
        "بل هي الطريق الأكثر أمانًا وفعالية للأشخاص والشركات والأقاليم."
    ),
    "p2.forum.what.title": "ما هو المنتدى",
    "p2.forum.what.body[0]": (
        "ينشأ منتدى Vénétie–Maroc‎ فضاءً دائمًا للحوار والتعاون بين إيطاليا والمغرب، مع اهتمام خاص بالعلاقات بين "
        "فينيتو والأقاليم المغربية."
    ),
    "p2.forum.what.body[1]": (
        "تهدف المبادرة إلى جمع المؤسسات والممثليات الاقتصادية والشركات والمهنيين والجامعات وهيئات التكوين وسائر "
        "الفاعلين المهتمين بتنمية علاقات مُهيكلة بين البلدين."
    ),
    "p2.forum.what.body[2]": (
        "الهدف هو تحويل الحوار إلى مشاريع ملموسة في مجالات التعاون الاقتصادي والتكوين والتنقل النظامي والعلاقات "
        "المؤسسية. وسيُقدَّم خلال المنتدى أيضًا مشروع Italy Legal Entry‎ والمشروع التجريبي Vénétie–Maroc‎."
    ),
    "p2.forum.objectives.title": "الأهداف",
    # eight clauses on the sentence's own «؛ » — the Forum cuts them into its eight stations (forum_v2.forum_clauses)
    "p2.forum.objectives.body": (
        "تعزيز الحوار المؤسسي Vénétie–Maroc‎؛ تنمية العلاقات بين الشركات؛ تحديد الاحتياجات المهنية؛ تطوير التكوين قبل "
        "المغادرة؛ النهوض بمسارات التنقل النظامي؛ تشجيع التعاون الجامعي؛ إقامة شراكات اقتصادية ومهنية؛ ضمان استمرارية "
        "العلاقات من خلال المنتدى الدائم Vénétie–Maroc‎."
    ),
    "p2.forum.audience.title": "لمن يتوجه المنتدى",
    # nine actors on the sentence's own «، », in the prescribed order — the ring's seats (forum_v2.forum_actors: the
    # institutions 1, the companies 2, the universities 5, the training bodies 6)
    "p2.forum.audience.body": (
        "المؤسسات الإيطالية والمغربية، الشركات، الجمعيات المهنية، غرف التجارة، الجامعات، هيئات التكوين، المهنيون، "
        "هيئات الشغل، والممثليات الدبلوماسية والقنصلية."
    ),
    "p2.forum.programme.title": "البرنامج",
    "p2.forum.programme.items[0]": "15:00 — الاستقبال والتسجيل",
    "p2.forum.programme.items[1]": "كلمات مؤسسية",
    "p2.forum.programme.items[2]": "تقديم المنتدى الدائم Vénétie–Maroc‎",
    "p2.forum.programme.items[3]": "تقديم Italy Legal Entry‎",
    "p2.forum.programme.items[4]": "تقديم المشروع التجريبي Vénétie–Maroc‎",
    "p2.forum.programme.items[5]": "مداخلات مؤسسية واقتصادية",
    "p2.forum.programme.items[6]": "حوار مع الشركات والجامعات والشركاء",
    "p2.forum.programme.items[7]": "الخلاصات والخطوات المقبلة",
    "p2.forum.programme.note": "البرنامج المفصّل للمداخلات في طور الإعداد وسيُحدَّث على هذه الصفحة.",
    "p2.forum.speakers.title": "المتدخلون",
    "p2.forum.speakers.body": (
        "من المرتقب، في جملة أمور، مداخلات عضو في مجلس الشيوخ الإيطالي، ومستشار وزير الشركات والصناعة الإيطالية "
        "(Made in Italy‎)، وعمدة روفيغو، ومحافظ روفيغو. وستُنشر أسماء المتدخلين مع البرنامج النهائي."
    ),
    "p2.forum.speakers.roles[0]": "عضو مجلس الشيوخ الإيطالي",
    "p2.forum.speakers.roles[1]": "مستشار وزير الشركات والصناعة الإيطالية (Made in Italy‎)",
    "p2.forum.speakers.roles[2]": "عمدة روفيغو",
    "p2.forum.speakers.roles[3]": "محافظ روفيغو",
    "p2.forum.registration.title": "التسجيل",
    "p2.forum.registration.intro": "المشاركة مجانية، بتسجيل مسبق.",
    "p2.forum.registration.fields[0]": "الاسم الشخصي",
    "p2.forum.registration.fields[1]": "الاسم العائلي",
    "p2.forum.registration.fields[2]": "الهيئة / الشركة",
    "p2.forum.registration.fields[3]": "الوظيفة",
    "p2.forum.registration.fields[4]": "البريد الإلكتروني",
    "p2.forum.registration.fields[5]": "الهاتف",
    "p2.forum.registration.fields[6]": "البلد",
    "p2.forum.registration.category_label": "الفئة",
    "p2.forum.registration.categories[0]": "مؤسسة",
    "p2.forum.registration.categories[1]": "شركة",
    "p2.forum.registration.categories[2]": "جمعية مهنية / غرفة تجارة",
    "p2.forum.registration.categories[3]": "جامعة / هيئة تكوين",
    "p2.forum.registration.categories[4]": "مهني",
    "p2.forum.registration.categories[5]": "هيئة شغل",
    "p2.forum.registration.categories[6]": "ممثلية دبلوماسية أو قنصلية",
    "p2.forum.registration.categories[7]": "أخرى",
    "p2.forum.registration.sector_label": "قطاع الاهتمام",
    "p2.forum.registration.button_primary": "شاركوا في المنتدى",
    "p2.forum.registration.button_secondary_pilot": "أعربوا عن اهتمامكم بالمشروع التجريبي",
    "p2.forum.registration.button_secondary_collab": "اقترحوا تعاونًا",
    "p2.home.banner.meta": "روفيغو | 2 أكتوبر 2026 | 15:00–18:00",
    "p2.home.banner.quote": "«مؤسسات وشركات وجامعات ومهنيون لبناء علاقات جديدة بين فينيتو والمغرب.»",
    "p2.home.banner.button": "اكتشفوا المنتدى",
    # ---- Phase 3 — the hero, the four entrances ----------------------------------------------------------
    "p3.hero.subtitle": "المسار النظامي نحو إيطاليا، من التوجيه إلى الإدماج.",
    "p3.hero.body": (
        "Italy Legal Entry‎ منظومة رقمية إيطالية مخصصة للتوجيه والتكوين ومواكبة المسارات النظامية نحو إيطاليا، "
        "طُوِّرت من خلال التعاون بين الأفراد والشركات والمؤسسات والجامعات وهيئات التكوين والمهنيين."
    ),
    "p3.entrances.person.title": "هل أنتم من الأفراد؟",
    "p3.entrances.person.text": "حدِّدوا المسار النظامي الأنسب لوضعيتكم واكتشفوا مراحله الرئيسية.",
    "p3.entrances.person.button": "اكتشفوا مساركم",
    "p3.entrances.company.title": "هل أنتم شركة؟",
    "p3.entrances.company.text": "أعلِمونا بالاحتياجات المهنية لشركتكم واكتشفوا مسارات التكوين والتنقل النظامي.",
    "p3.entrances.company.button": "أعربوا عن اهتمامكم",
    "p3.entrances.institution.title": "هل أنتم مؤسسة؟",
    "p3.entrances.institution.text": "لنبنِ معًا برامج وشراكات للتنقل النظامي والتكوين والتعاون الدولي.",
    "p3.entrances.institution.button": "اقترحوا تعاونًا",
    "p3.entrances.university.title": "هل أنتم جامعة أو هيئة تكوين؟",
    "p3.entrances.university.text": "التكوين والتنقل والتدريب والتبادل والتعاون الدولي.",
    "p3.entrances.university.button": "تعاونوا معنا",
    # ---- Phase 3 — Espace Personnes ------------------------------------------------------------------------
    "p3.persons.title": "مساركم النظامي نحو إيطاليا",
    "p3.persons.pathways[0].title": "العمل المأجور",
    "p3.persons.pathways[1].title": "العمل المؤهَّل — البطاقة الزرقاء الأوروبية",
    "p3.persons.pathways[2].title": "التكوين في بلد المنشأ",
    "p3.persons.pathways[3].title": "الدراسة والتكوين في إيطاليا",
    "p3.persons.pathways[4].title": "التجمع العائلي",
    "p3.persons.pathways[5].title": "العمل المستقل والمقاولة",
    "p3.persons.pathways[6].title": "البحث العلمي",
    "p3.persons.pathways[7].title": "السبل النظامية الأخرى",
    # the route's shape kept — «: », three « → », the caveat after the first «. » (pathways.services.how_it_works)
    "p3.persons.how_it_works": (
        "كيف يعمل: أجيبوا عن أسئلة التوجيه → تتلقّون تقييمًا أوليًا ذا طابع إعلامي → استعدّوا بالتكوين قبل المغادرة → "
        "اتبعوا المسطرة النظامية مع الفاعلين المختصين. لا يُوعَد بأي نتيجة إدارية ولا تُضمَن."
    ),
    # ---- Phase 3 — the institutions, the universities, the pilot ----------------------------------------
    "p3.institutions.intro": (
        "تنهض Italy Legal Entry‎ بنماذج للتعاون المؤسسي تهدف إلى بناء مسارات نظامية وشفافة ومنظَّمة للتنقل والتكوين."
    ),
    "p3.institutions.recipients": (
        "الجهات المعنية: الجهات، والجماعات، والهيئات العمومية، وغرف التجارة، وهيئات الشغل، والممثليات "
        "الدبلوماسية والقنصلية ومؤسسات البلدان الشريكة."
    ),
    "p3.institutions.button": "اقترحوا تعاونًا مؤسسيًا",
    "p3.universities.intro": (
        "الجامعات وهيئات التكوين والمعاهد ومراكز البحث: التكوين، والتدريب، والتنقل الدولي، وتبادل الطلبة، والبرامج "
        "المشتركة، والتعاون الأكاديمي، والتكوين قبل المغادرة، وتثمين الكفاءات."
    ),
    "p3.universities.button": "اقترحوا شراكة",
    "p3.pilot.title": "المشروع التجريبي Vénétie–Maroc‎",
    "p3.pilot.body": (
        "تعتزم Italy Legal Entry‎ الانطلاق من مشروع تجريبي بين فينيتو والمغرب، مبني على احتياجات الشركات وعلى "
        "التعاون مع مخاطَبين مؤسسيين وتكوينيين. والنموذج قابل للتكرار مع أقاليم وبلدان أخرى."
    ),
    "p3.pilot.sequence[0]": "احتياجات الشركات",
    "p3.pilot.sequence[1]": "الملامح والكفاءات",
    "p3.pilot.sequence[2]": "التكوين في بلد المنشأ",
    "p3.pilot.sequence[3]": "الإعداد قبل المغادرة",
    "p3.pilot.sequence[4]": "المساطر النظامية",
    "p3.pilot.sequence[5]": "الدخول إلى إيطاليا",
    "p3.pilot.sequence[6]": "المواكبة",
    "p3.pilot.sequence[7]": "المتابعة",
    # ---- Phase 3 — the anti-fraud title, the FAQ questions and informational answers ----------------------
    "p3.antifraud.title": "احذروا الاحتيال",
    "p3.faq.items[0].question": "هل تمنح Italy Legal Entry‎ تأشيرات؟",
    "p3.faq.items[1].question": "هل Italy Legal Entry‎ وكالة توظيف؟",
    "p3.faq.items[2].question": "هل يضمن التقييم الأولي الدخول إلى إيطاليا؟",
    "p3.faq.items[3].question": "ما هو «decreto flussi‎»؟",
    "p3.faq.items[4].question": "هل تعترف Italy Legal Entry‎ بالشهادات الأجنبية؟",
    "p3.faq.items[5].question": "هل يمنع رفض سابق أي طلب مستقبلي؟",
    "p3.faq.items[6].question": "من يقف وراء Italy Legal Entry‎؟",
    "p3.faq.items[7].question": "هل بياناتي محمية؟",
    "p3.faq.items[8].question": "يعرض عليّ شخص تأشيرة مضمونة مقابل مبلغ مالي. ماذا أفعل؟",
    # the informational answers (DL54-211), in the catalogue's own words where it already says them («من اختصاص
    # السلطات المختصة», «السبيل النظامي», «التصديق أو الأبوستيل», «احذروا الاحتيال»), the promoter as the Forum says it
    "p3.faq.items[0].answer": (
        "لا. فالتأشيرات وتصاريح الإقامة والتراخيص من اختصاص السلطات المختصة حصرًا. وتوجّهكم المنصة نحو السبيل "
        "النظامي الأنسب وتساعدكم على الاستعداد."
    ),
    "p3.faq.items[2].answer": (
        "لا. فهو توجيه ذو طابع إعلامي، يستند إلى المعلومات التي تقدّمونها. ويعود كل قرار إلى السلطات."
    ),
    "p3.faq.items[4].answer": (
        "لا. فالاعتراف من اختصاص السلطات والهيئات المختصة؛ وتوجّهكم المنصة بشأن الوثائق والترجمات والتصديق أو "
        "الأبوستيل والإجراءات الواجب اتباعها."
    ),
    "p3.faq.items[6].answer": (
        "المشروع مبادرة من جمعية AGAMI — Dialogo Giuridico Interculturale APS‎، وهي جمعية حقوقيين تعمل منذ 2011 في "
        "مجال الحوار القانوني بين إيطاليا والمغرب، ويُنجَز بمساهمة مهنيين وشركات ومؤسسات وهيئات تكوين."
    ),
    "p3.faq.items[8].answer": (
        "ارفضوا. فلا يمكن ضمان أي نتيجة، ولا يمكن لأي وسيط أن يمنح تأشيرة. اطّلعوا على قسم «احذروا الاحتيال»."
    ),
    # ---- Phase 3 — living, training, news, the virtual Forum, diplomas, the reserved area ---------------
    "p3.living.title": "العيش في إيطاليا",
    "p3.living.body": (
        "الاستعداد للوصول يعني أيضًا معرفة الحياة اليومية: اللغة الإيطالية، والسكن، والصحة والتسجيل في الخدمة الصحية، "
        "والمدرسة والتربية المدنية، والحقوق والواجبات، والسلامة في العمل، والضرائب الأساسية، والخدمات العمومية. ويجمع "
        "هذا القسم معلومات عملية وأدلة، تُغنى تدريجيًا، لمواكبة الإدماج بعد الدخول النظامي."
    ),
    "p3.training_after.title": "التكوين بعد الوصول",
    "p3.news.title": "الأخبار",
    "p3.news.body": "المستجدات التنظيمية، والآجال الرسمية، ومبادرات المنتدى الدائم Vénétie–Maroc‎، وأنشطة المنظومة.",
    "p3.news.newsletter_label": "ابقوا على اطلاع",
    "p3.virtual_forum.title": "المنتدى الافتراضي",
    "p3.virtual_forum.body": (
        "لا يتوقف المنتدى عند الحدث. فالمنتدى الافتراضي هو فضاء الحوار والتواصل في الموقع، المخصص للمشاركين — من "
        "مؤسسات "
        "وشركات وجامعات وهيئات تكوين ومهنيين — لمواصلة التبادل، ومشاركة الوثائق والمبادرات، واقتراح أوجه التعاون، "
        "ومتابعة المشاريع المنبثقة عن المنتدى. ويكون الدخول بالتسجيل."
    ),
    "p3.virtual_forum.button": "ادخلوا إلى المنتدى الافتراضي",
    "p3.diplomas.title": "الشهادات والمؤهلات الأجنبية",
    "p3.reserved.title": "الفضاء الخاص",
    "p3.reserved.body": "ادخلوا إلى فضائكم الشخصي لمتابعة طلباتكم ومساراتكم ومراسلاتكم.",
    "p3.reserved.button": "تسجيل الدخول",
}

#: the identification caption before a C-SUBST-FR block on its own page, and before an Italian authoritative text —
#: UI strings, in the label role, translated by the catalogue (it/en/ar; the Arabic reviewed)
CAPTION_SOURCE_FR = pgettext_lazy(
    "locked caption", "Texte source en français — traduction arabe en cours de validation."
)
CAPTION_SOURCE_IT = pgettext_lazy(
    "locked caption", "Texte italien faisant foi — traduction arabe en cours de validation."
)
#: the hidden form's one line, on a page that quotes a C-SUBST-FR block it does not own
POINTER_LINE = pgettext_lazy(
    "locked caption", "Texte source en français sur la page « %(page)s » — traduction arabe en cours de validation."
)


# --------------------------------------------------------------------------------------------
# The request's route (the «on its source page» rule)
# --------------------------------------------------------------------------------------------
_PATH: contextvars.ContextVar[str | None] = contextvars.ContextVar("ile_locked_request_path", default=None)
_ROUTE: contextvars.ContextVar[str | None] = contextvars.ContextVar("ile_locked_request_route", default=None)
_UNRESOLVED = ""


def _on_request_started(sender=None, environ=None, scope=None, **_kwargs) -> None:
    path = ""
    if environ:
        path = environ.get("PATH_INFO") or ""
    elif scope:
        path = scope.get("path") or ""
    _PATH.set(path or _UNRESOLVED)
    _ROUTE.set(None)


def _on_request_finished(sender=None, **_kwargs) -> None:
    _PATH.set(None)
    _ROUTE.set(None)


request_started.connect(_on_request_started, dispatch_uid="cms.locked_renderings.request_started", weak=False)
request_finished.connect(_on_request_finished, dispatch_uid="cms.locked_renderings.request_finished", weak=False)


def current_route() -> str | None:
    """The URL name (``namespace:name``) of the request being served, resolved once per request; "" when the path
    resolves to nothing; None outside a request."""
    path = _PATH.get()
    if path is None:
        return None
    route = _ROUTE.get()
    if route is None:
        try:
            match = resolve(path)
            route = match.view_name or _UNRESOLVED
        except Resolver404:
            route = _UNRESOLVED
        _ROUTE.set(route)
    return route


def set_route_for_tests(route: str | None) -> None:
    """Pin the route (a URL name, "" for none, None for «outside a request») — for a test that renders without
    a request."""
    _PATH.set(None if route is None else "/")
    _ROUTE.set(route)


# --------------------------------------------------------------------------------------------
# The policy, key by key
# --------------------------------------------------------------------------------------------
def pattern(subkey: str) -> str:
    """``p3.faq.items[4].answer`` → ``p3.faq.items[].answer`` (the register's row pattern)."""
    return _INDEX.sub("[]", subkey)


def treatment(subkey: str) -> str | None:
    """The class of a text (a key or a sub-key), or None when the policy does not know it: the sub-key itself, its
    pattern (``[]`` for any item), then the compound key it belongs to — a value classified whole (the legal texts)
    classifies every text inside it."""
    found = TREATMENT.get(subkey) or TREATMENT.get(pattern(subkey))
    path = subkey
    while found is None and ("[" in path or "." in path):
        path = re.sub(r"(?:\[\d*\]|\.[a-z_]+)$", "", path)
        if not path or path == subkey:
            break
        found = TREATMENT.get(path)
    return found


def rendering(subkey: str) -> str | None:
    """The provisional Arabic rendering of a C-UI text, or None."""
    return AR.get(subkey)


def source_routes(subkey: str) -> tuple[str, ...]:
    return SOURCE_ROUTES.get(subkey) or SOURCE_ROUTES.get(pattern(subkey)) or ()


def derived_routes(subkey: str) -> tuple[str, ...]:
    """The forms where a team wording derived from ``subkey`` stands identified by its caption (``DERIVED_ROUTES``)."""
    return DERIVED_ROUTES.get(subkey) or DERIVED_ROUTES.get(pattern(subkey)) or ()


def on_source_route(subkey: str) -> bool | None:
    """True on the text's own page, False on another page of the site, None outside a request (the French stands)."""
    route = current_route()
    if route is None:
        return None
    return route in source_routes(subkey)


def is_hidden(subkey: str, lang: str) -> bool:
    """Whether a text is in its hidden form on the page being served: a C-SUBST-FR text quoted off its own page, in
    Arabic."""
    lang = (lang or SOURCE_LANGUAGE).split("-")[0]
    return lang == RENDERED_LANGUAGE and treatment(subkey) == C_SUBST_FR and on_source_route(subkey) is False


def menu_notice_allowed(subkey: str, lang: str) -> bool:
    """The mega-menu's legal notice line (cms_nav): a substantive block pending validation is not said in the menu of an
    Arabic page at all — its own page carries it, identified (V5.27 §2: hiding is preferable to mixed-language
    content)."""
    lang = (lang or SOURCE_LANGUAGE).split("-")[0]
    return not (lang == RENDERED_LANGUAGE and treatment(subkey) == C_SUBST_FR)


def page_name(subkey: str) -> str:
    """The name of the text's own page, in the page's language: a pathway description names its sheet by the sheet's
    title (its rendering), every other block the catalogue's name of its page."""
    if pattern(subkey) == "p3.persons.pathways[].description":
        title_key = subkey.rsplit(".", 1)[0] + ".title"
        found = rendering(title_key)
        if found:
            return found
        from cms import locked_content

        return str(locked_content.get(title_key, SOURCE_LANGUAGE)[0])
    name = SOURCE_PAGE_NAME.get(subkey) or SOURCE_PAGE_NAME.get(pattern(subkey))
    return str(name) if name is not None else ""


def pointer_line(subkey: str) -> str:
    """The hidden form: one line, in the page's language, naming the source page."""
    return str(POINTER_LINE) % {"page": page_name(subkey)}


def caption_text(subkey: str, lang: str) -> str:
    """The identification caption of a block shown in its source language on a page of another language, "" when the
    block needs none (a C-UI rendering, a C-OFFICIAL name, a French page)."""
    lang = (lang or SOURCE_LANGUAGE).split("-")[0]
    if lang != RENDERED_LANGUAGE:
        return ""  # the decision is Arabic: Italian and English keep today's rendering, caption included
    kind = treatment(subkey)
    if kind == C_SUBST_FR:
        return str(CAPTION_SOURCE_FR)
    if kind == C_SUBST_IT:
        return str(CAPTION_SOURCE_IT)
    return ""


def _resolve_leaf(subkey: str, lang: str) -> tuple[str, str] | None:
    kind = treatment(subkey)
    if kind == C_UI:
        found = rendering(subkey)
        return (found, lang) if found else None
    if kind == C_SUBST_FR and on_source_route(subkey) is False:
        return pointer_line(subkey), lang
    return None


def resolve_value(subkey: str, french: Any, lang: str | None) -> tuple[Any, str] | None:
    """
    The value the Arabic product shows for the registry's ``french`` at ``subkey`` — ``(value, effective_language)`` —
    or None when the French stands (``locked_content.get`` then answers ``(french, "fr")`` as it always did).

    A compound value (a list, a dict, a list of dicts) is rebuilt leaf by leaf: C-UI leaves take their rendering,
    C-SUBST-FR leaves quoted off their page take the pointer line, identifiers and C-OFFICIAL leaves stay as written;
    when a leaf must stay French on this page (a C-SUBST-FR on its source route, a C-SUBST-IT) the WHOLE value stays
    French — a compound value carries one language, and a page lane that needs a mixed composition reads the parts by
    their sub-keys.
    """
    lang = (lang or SOURCE_LANGUAGE).split("-")[0]
    if lang != RENDERED_LANGUAGE or subkey in DEFERRED_WHOLE:
        return None
    changed = False
    french_left = False

    def walk(path: str, value: Any, field: str = "") -> Any:
        nonlocal changed, french_left
        if isinstance(value, str):
            if field in IDENTIFIER_FIELDS:
                return value
            kind = treatment(path)
            if kind == C_OFFICIAL:
                return value
            found = _resolve_leaf(path, lang)
            if found is None:
                french_left = True
                return value
            changed = True
            return found[0]
        if isinstance(value, list):
            return [walk(f"{path}[{i}]", item) for i, item in enumerate(value)]
        if isinstance(value, dict):
            return {name: walk(f"{path}.{name}", item, name) for name, item in value.items()}
        return value

    built = walk(subkey, french)
    if not changed or french_left:
        return None
    return built, lang


# --------------------------------------------------------------------------------------------
# The register (the dev board, the counts of the report, the tests)
# --------------------------------------------------------------------------------------------
def leaves() -> list[tuple[str, str]]:
    """Every text of the registry as ``(sub-key, French)``, identifiers left out — the register's rows."""
    from cms import locked_content

    out: list[tuple[str, str]] = []

    def walk(path: str, value: Any, field: str = "") -> None:
        if isinstance(value, str):
            if field not in IDENTIFIER_FIELDS:
                out.append((path, value))
        elif isinstance(value, list):
            for i, item in enumerate(value):
                walk(f"{path}[{i}]", item)
        elif isinstance(value, dict):
            for name, item in value.items():
                walk(f"{path}.{name}", item, name)

    for key in locked_content.keys():  # noqa: SIM118 — a module's function, not a dict
        walk(key, locked_content.LOCKED_TEXTS[SOURCE_LANGUAGE][key])
    return out


def board_rows() -> list[dict[str, Any]]:
    """One row per text: key, class, status, source routes, whether a rendering exists — for ``/__design-v5/``."""
    rows = []
    for subkey, french in leaves():
        kind = treatment(subkey)
        rows.append(
            {
                "key": subkey,
                "treatment": kind or "—",
                "status": STATUS_OF.get(kind or "", "UNCLASSIFIED"),
                "routes": ", ".join(source_routes(subkey)) if kind == C_SUBST_FR else "",
                "rendered": subkey in AR,
                "words": len(french.split()),
            }
        )
    for msgid, why in OFFICIAL_MSGIDS.items():
        rows.append(
            {
                "key": msgid,
                "treatment": C_OFFICIAL,
                "status": STATUS_ORIGINAL,
                "routes": why,
                "rendered": False,
                "words": len(msgid.split()),
            }
        )
    return rows


def counts() -> dict[str, int]:
    """The three figures of the report (V5.27 §8): the provisional non-legal Arabic (C-UI), the untranslated
    authoritative blocks (C-SUBST-FR + C-SUBST-IT) with their split, the originals — counted over the register's
    texts."""
    totals = dict.fromkeys(TREATMENTS, 0)
    for subkey, _french in leaves():
        kind = treatment(subkey)
        if kind:
            totals[kind] += 1
    totals[C_OFFICIAL] += len(OFFICIAL_MSGIDS)
    return totals


def template_counts() -> dict[str, int]:
    """counts() with keys a Django template can read (c_ui, c_subst_it, c_subst_fr, c_official): a hyphenated key
    such as `locked_counts.C-UI` does not parse (v524-ar-fix B1)."""
    return {kind.lower().replace("-", "_"): figure for kind, figure in counts().items()}
