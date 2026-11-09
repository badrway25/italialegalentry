"""
The team's translation rows for the reference data the product reads through ``cms.translation.resolve`` and that the
seeds
create in French only (V5.24 §4–§5; the Arabic completeness audit,
``evidence/v524/arabic/fragments/data_translations.json``,
W2; lane AR, label v524-ar): the five generic stage titles of the eight pathway sheets, the orientation questionnaire
(its
questions, help texts, choices, outcomes and checklist items) and the FAQ's general category.

Every source string here is TEAM text (``apps/pathways/seeds.py`` GENERIC_STEPS_FR, ``apps/orientation/seeds.py``,
``apps/faq/seeds.py``) — no prescribed text of ``cms.locked_content`` is touched. The rows are loaded by
``seed_team_translations`` (idempotent: ``get_or_create`` per ``(master, language)``, defaults on creation only — an
editor's later change is never overwritten), ``status = PUBLISHED``, ``source = SOURCE``.

Arabic: formal institutional register, the plural of courtesy (أنتم), Arabic punctuation, Western digits; the pathway
families named in Arabic (V5.27 hybrid: the pathways' prescribed titles are rendered in provisional Arabic too, so the
result page and its sheet agree). Italian: «Lei» for the person. English: neutral.
"""

from __future__ import annotations

LANGUAGES = ("ar", "it", "en")
SOURCE = "team — v524 (Q3 provisional)"

#: pathways.PathwayStepTranslation — matched by the step's order and its French title, on every pathway
PATHWAY_STEPS: tuple[dict, ...] = (
    {"order": 1, "fr": "S’orienter", "ar": "التوجيه", "it": "Orientarsi", "en": "Getting oriented"},
    {
        "order": 2,
        "fr": "Préparer la documentation généralement requise",
        "ar": "إعداد الوثائق المطلوبة عادةً",
        "it": "Preparare la documentazione generalmente richiesta",
        "en": "Preparing the documents generally required",
    },
    {
        "order": 3,
        "fr": "Suivre la procédure régulière auprès des acteurs compétents",
        "ar": "اتباع المسطرة النظامية لدى الفاعلين المختصين",
        "it": "Seguire la procedura regolare presso i soggetti competenti",
        "en": "Following the regular procedure with the competent actors",
    },
    {
        "order": 4,
        "fr": "Se préparer avant le départ",
        "ar": "الاستعداد قبل المغادرة",
        "it": "Prepararsi prima della partenza",
        "en": "Preparing before departure",
    },
    {
        "order": 5,
        "fr": "Accompagnement après l’arrivée",
        "ar": "المواكبة بعد الوصول",
        "it": "Accompagnamento dopo l’arrivo",
        "en": "Support after arrival",
    },
)

#: faq.FAQCategoryTranslation — matched by slug
FAQ_CATEGORIES: tuple[dict, ...] = (
    {"slug": "general", "fr": "Général", "ar": "عام", "it": "Generale", "en": "General"},
)

#: orientation.QuestionTranslation — matched by the question's key (every ruleset that holds it)
QUESTIONS: tuple[dict, ...] = (
    {
        "key": "objective",
        "ar": {
            "text": "ما الهدف الرئيسي لمشروعكم نحو إيطاليا؟",
            "help": (
                "اختاروا الوضعية التي تصف مشروعكم على أفضل وجه. لا تُطلب أي بيانات شخصية، ويمكنكم الرجوع إلى الخلف في "
                "أي وقت."
            ),
        },
        "it": {
            "text": "Qual è l’obiettivo principale del suo progetto verso l’Italia?",
            "help": (
                "Scelga la situazione che descrive meglio il suo progetto. Non viene richiesto alcun dato personale e "
                "potrà "
                "tornare indietro in qualsiasi momento."
            ),
        },
        "en": {
            "text": "What is the main objective of your project towards Italy?",
            "help": (
                "Choose the situation that best describes your project. No personal data is requested, and you can go "
                "back at any time."
            ),
        },
    },
    {
        "key": "work_profile",
        "ar": {
            "text": "أي وصف يطابق مشروعكم المهني على أفضل وجه؟",
            "help": (
                "يقتصر دور هذا السؤال على تحديد فئة المسارات التي ينبغي الاطلاع عليها؛ وهو لا يشكّل تقييمًا لمؤهلاتكم."
            ),
        },
        "it": {
            "text": "Quale descrizione corrisponde meglio al suo progetto professionale?",
            "help": (
                "Questa domanda serve soltanto a individuare la famiglia di percorsi da consultare; non costituisce "
                "una "
                "valutazione del suo profilo."
            ),
        },
        "en": {
            "text": "Which description best matches your professional project?",
            "help": (
                "This question only serves to identify the family of pathways to consult; it is not an assessment of "
                "your profile."
            ),
        },
    },
    {
        "key": "study_type",
        "ar": {
            "text": "ما نوع مسار الدراسة أو التكوين الذي تعتزمونه؟",
            "help": "يمكن أن تجري الدراسة والتكوين في إيطاليا، أو في بلدكم قبل المغادرة.",
        },
        "it": {
            "text": "Quale tipo di percorso di studio o di formazione intende seguire?",
            "help": (
                "Gli studi e la formazione possono svolgersi in Italia oppure, prima della partenza, nel suo paese."
            ),
        },
        "en": {
            "text": "What type of study or training pathway are you considering?",
            "help": "Studies and training may take place in Italy or, before departure, in your country.",
        },
    },
    {
        "key": "family_member_status",
        "ar": {
            "text": "هل فرد عائلتكم الذي ترغبون في الالتحاق به مقيم بصفة نظامية في إيطاليا؟",
            "help": (
                "أجيبوا بحسب ما تعرفونه اليوم. وفي حال الشك، اختاروا «لا أعرف»: ستُدرس الوضعية مع الفاعلين المختصين."
            ),
        },
        "it": {
            "text": "Il familiare che desidera raggiungere è regolarmente presente in Italia?",
            "help": (
                "Risponda in base a ciò che sa oggi. In caso di dubbio scelga «Non lo so»: la situazione sarà da "
                "esaminare "
                "con i soggetti competenti."
            ),
        },
        "en": {
            "text": "Is the family member you wish to join regularly present in Italy?",
            "help": (
                "Answer according to what you know today. If in doubt, choose “I don’t know”: the situation will need "
                "to be "
                "examined with the competent actors."
            ),
        },
    },
    {
        "key": "training_interest",
        "ar": {
            "text": "هل ترغبون في تلقّي معلومات عن التكوين قبل المغادرة (المهني واللغوي والمدني)؟",
            "help": "التكوين قبل المغادرة وقتٌ للإعداد يُقترح في إطار المشروع؛ وهذا الجواب لا يغيّر التوجيه.",
        },
        "it": {
            "text": (
                "Desidera ricevere informazioni sulla formazione prima della partenza (professionale, linguistica, "
                "civica)?"
            ),
            "help": (
                "La formazione prima della partenza è un tempo di preparazione proposto nell’ambito del progetto; "
                "questa "
                "risposta non modifica l’orientamento."
            ),
        },
        "en": {
            "text": "Would you like to receive information on pre-departure training (vocational, language, civic)?",
            "help": (
                "Pre-departure training is a preparation period offered within the project; this answer does not "
                "change the orientation."
            ),
        },
    },
)

#: orientation.ChoiceTranslation — matched by (question key, choice key); the boolean question has no choice rows
CHOICES: tuple[dict, ...] = (
    {
        "question": "objective",
        "key": "work",
        "ar": "العمل في إيطاليا",
        "it": "Lavorare in Italia",
        "en": "Work in Italy",
    },
    {
        "question": "objective",
        "key": "study",
        "ar": "الدراسة أو متابعة تكوين",
        "it": "Studiare o seguire una formazione",
        "en": "Study or follow a training course",
    },
    {
        "question": "objective",
        "key": "family",
        "ar": "الالتحاق بأحد أفراد عائلتي في إيطاليا",
        "it": "Raggiungere un familiare in Italia",
        "en": "Join a family member in Italy",
    },
    {
        "question": "objective",
        "key": "self_employment",
        "ar": "ممارسة نشاط مستقل أو مقاولاتي",
        "it": "Svolgere un’attività indipendente o imprenditoriale",
        "en": "Carry out a self-employed or entrepreneurial activity",
    },
    {
        "question": "objective",
        "key": "research",
        "ar": "القيام بنشاط بحث علمي",
        "it": "Svolgere un’attività di ricerca scientifica",
        "en": "Carry out scientific research",
    },
    {
        "question": "objective",
        "key": "other",
        "ar": "وضعية أخرى، أو لا أعرف بعد",
        "it": "Altra situazione, o non lo so ancora",
        "en": "Another situation, or I don’t know yet",
    },
    {
        "question": "work_profile",
        "key": "salaried",
        "ar": "عمل مأجور لدى شركة في إيطاليا",
        "it": "Un lavoro subordinato presso un’impresa in Italia",
        "en": "Salaried employment with a company in Italy",
    },
    {
        "question": "work_profile",
        "key": "highly_qualified",
        "ar": "مؤهلات عالية (شهادة تعليم عالٍ أو خبرة مهنية مؤهَّلة)",
        "it": (
            "Un profilo altamente qualificato (titolo di istruzione superiore o esperienza professionale qualificata)"
        ),
        "en": "A highly qualified profile (higher-education degree or qualified professional experience)",
    },
    {
        "question": "work_profile",
        "key": "seasonal",
        "ar": "عمل موسمي أو مؤقت",
        "it": "Un lavoro stagionale o temporaneo",
        "en": "Seasonal or temporary work",
    },
    {
        "question": "work_profile",
        "key": "unsure",
        "ar": "لا أعرف بعد",
        "it": "Non lo so ancora",
        "en": "I don’t know yet",
    },
    {
        "question": "study_type",
        "key": "university",
        "ar": "تسجيل جامعي أو تبادل أكاديمي في إيطاليا",
        "it": "Un’iscrizione universitaria o uno scambio accademico in Italia",
        "en": "University enrolment or an academic exchange in Italy",
    },
    {
        "question": "study_type",
        "key": "vocational_in_italy",
        "ar": "دورة تكوين مهني في إيطاليا",
        "it": "Un corso di formazione professionale in Italia",
        "en": "A vocational training course in Italy",
    },
    {
        "question": "study_type",
        "key": "training_before_departure",
        "ar": "تكوين مهني أو لغوي قبل المغادرة، من بلدي",
        "it": "Una formazione professionale o linguistica prima della partenza, dal mio paese",
        "en": "Vocational or language training before departure, from my country",
    },
    {
        "question": "study_type",
        "key": "unsure",
        "ar": "لا أعرف بعد",
        "it": "Non lo so ancora",
        "en": "I don’t know yet",
    },
    {"question": "family_member_status", "key": "yes", "ar": "نعم", "it": "Sì", "en": "Yes"},
    {"question": "family_member_status", "key": "no", "ar": "لا", "it": "No", "en": "No"},
    {"question": "family_member_status", "key": "unsure", "ar": "لا أعرف", "it": "Non lo so", "en": "I don’t know"},
)

#: the explanation every family's outcome shares (apps/orientation/seeds.py ``_explanation``), per language
EXPLANATION: dict[str, str] = {
    "ar": (
        "بحسب أجوبتكم، يبدو أن مشروعكم يندرج ضمن فئة المسارات «{family}» المعروضة في فضاء الأفراد. ولهذا التقييم "
        "الأولي "
        "طابع إعلامي محض: فكل قرار يعود حصريًا إلى السلطات المختصة. الخطوات الموالية، ذات الطابع الإعلامي: الاطلاع على "
        "صفحة المسار، وإعداد الوثائق المطلوبة عادةً، والاتصال بالفاعلين المختصين."
    ),
    "it": (
        "In base alle sue risposte, il suo progetto sembra corrispondere alla famiglia di percorsi «{family}» "
        "presentata "
        "nell’Area Persone. Questa prevalutazione ha carattere puramente informativo: ogni decisione spetta "
        "esclusivamente "
        "alle autorità competenti. Prossimi passi, a carattere informativo: consultare la pagina del percorso, "
        "preparare la "
        "documentazione generalmente richiesta e prendere contatto con i soggetti competenti."
    ),
    "en": (
        "Based on your answers, your project appears to correspond to the “{family}” family of pathways presented in "
        "the "
        "Individuals Area. This preliminary assessment is purely informative: every decision rests exclusively with "
        "the "
        "competent authorities. Next steps, for information: consult the pathway page, prepare the documents generally "
        "required and contact the competent actors."
    ),
}

#: orientation.OutcomeTranslation — matched by the outcome's pathway_key (one outcome per family per ruleset)
OUTCOMES: tuple[dict, ...] = (
    {
        "pathway_key": "salaried_work",
        "ar": {"title": "توجيه نحو مسار العمل المأجور", "family": "العمل المأجور"},
        "it": {"title": "Orientamento verso un percorso di lavoro subordinato", "family": "lavoro subordinato"},
        "en": {"title": "Orientation towards a salaried work pathway", "family": "salaried work"},
    },
    {
        "pathway_key": "skilled_work_eu_blue_card",
        "ar": {"title": "توجيه نحو مسار العمل المؤهَّل", "family": "العمل المؤهَّل"},
        "it": {"title": "Orientamento verso un percorso di lavoro qualificato", "family": "lavoro qualificato"},
        "en": {"title": "Orientation towards a skilled work pathway", "family": "skilled work"},
    },
    {
        "pathway_key": "training_in_origin_country",
        "ar": {"title": "توجيه نحو مسار التكوين قبل المغادرة", "family": "التكوين في بلد المنشأ"},
        "it": {
            "title": "Orientamento verso un percorso di formazione prima della partenza",
            "family": "formazione nel paese d’origine",
        },
        "en": {
            "title": "Orientation towards a pre-departure training pathway",
            "family": "training in the country of origin",
        },
    },
    {
        "pathway_key": "study_and_training_in_italy",
        "ar": {"title": "توجيه نحو مسار الدراسة أو التكوين في إيطاليا", "family": "الدراسة والتكوين في إيطاليا"},
        "it": {
            "title": "Orientamento verso un percorso di studio o di formazione in Italia",
            "family": "studio e formazione in Italia",
        },
        "en": {
            "title": "Orientation towards a study or training pathway in Italy",
            "family": "study and training in Italy",
        },
    },
    {
        "pathway_key": "family_reunification",
        "ar": {"title": "توجيه نحو مسار التجمع العائلي", "family": "التجمع العائلي"},
        "it": {
            "title": "Orientamento verso un percorso di ricongiungimento familiare",
            "family": "ricongiungimento familiare",
        },
        "en": {"title": "Orientation towards a family reunification pathway", "family": "family reunification"},
    },
    {
        "pathway_key": "self_employment_entrepreneurship",
        "ar": {"title": "توجيه نحو مسار العمل المستقل أو المقاولة", "family": "العمل المستقل والمقاولة"},
        "it": {
            "title": "Orientamento verso un percorso di lavoro autonomo o di imprenditoria",
            "family": "lavoro autonomo e imprenditoria",
        },
        "en": {
            "title": "Orientation towards a self-employment or entrepreneurship pathway",
            "family": "self-employment and entrepreneurship",
        },
    },
    {
        "pathway_key": "scientific_research",
        "ar": {"title": "توجيه نحو مسار البحث العلمي", "family": "البحث العلمي"},
        "it": {"title": "Orientamento verso un percorso di ricerca scientifica", "family": "ricerca scientifica"},
        "en": {"title": "Orientation towards a scientific research pathway", "family": "scientific research"},
    },
    {
        "pathway_key": "other_regular_routes",
        "ar": {"title": "توجيه نحو السبل النظامية الأخرى", "family": "السبل النظامية الأخرى"},
        "it": {"title": "Orientamento verso le altre vie regolari", "family": "altre vie regolari"},
        "en": {"title": "Orientation towards the other regular routes", "family": "other regular routes"},
    },
    {
        "pathway_key": "needs_individual_analysis",
        "ar": {
            "title": "وضعية تستوجب دراسة فردية",
            "explanation": (
                "لا تسمح أجوبتكم بتحديد فئة مسارات واحدة. ولهذا التقييم الأولي طابع إعلامي محض: فكل قرار يعود حصريًا "
                "إلى "
                "السلطات المختصة. الخطوات الموالية، ذات الطابع الإعلامي: الاطلاع على عرض المسارات النظامية في فضاء "
                "الأفراد، "
                "والاتصال بالفاعلين المختصين لدراسة وضعيتكم دراسةً فردية."
            ),
        },
        "it": {
            "title": "Situazione da esaminare individualmente",
            "explanation": (
                "Le sue risposte non consentono di individuare un’unica famiglia di percorsi. Questa prevalutazione ha "
                "carattere puramente informativo: ogni decisione spetta esclusivamente alle autorità competenti. "
                "Prossimi "
                "passi, a carattere informativo: consultare la presentazione dei percorsi regolari nell’Area Persone e "
                "prendere contatto con i soggetti competenti per un esame individuale della sua situazione."
            ),
        },
        "en": {
            "title": "Situation to be examined individually",
            "explanation": (
                "Your answers do not make it possible to identify a single family of pathways. This preliminary "
                "assessment is "
                "purely informative: every decision rests exclusively with the competent authorities. Next steps, for "
                "information: consult the presentation of the regular pathways in the Individuals Area and contact the "
                "competent actors for an individual examination of your situation."
            ),
        },
    },
)

#: orientation.ChecklistItemTranslation — matched by the item's French text, under every outcome that holds it
CHECKLIST_ITEMS: tuple[dict, ...] = (
    {
        "fr": "Consulter la page du parcours dans l’Espace Personnes pour connaître les principales étapes.",
        "ar": "الاطلاع على صفحة المسار في فضاء الأفراد للتعرف على المراحل الرئيسية.",
        "it": "Consultare la pagina del percorso nell’Area Persone per conoscere le tappe principali.",
        "en": "Consult the pathway page in the Individuals Area to learn the main steps.",
    },
    {
        "fr": (
            "Vérifier les documents généralement requis auprès des autorités compétentes et rassembler ceux dont vous "
            "disposez."
        ),
        "ar": "التحقق من الوثائق المطلوبة عادةً لدى السلطات المختصة وجمع ما تتوفرون عليه منها.",
        "it": (
            "Verificare i documenti generalmente richiesti presso le autorità competenti e raccogliere quelli di cui "
            "dispone."
        ),
        "en": "Check the documents generally required with the competent authorities and gather those you have.",
    },
    {
        "fr": "Identifier les interlocuteurs et les autorités compétents pour votre situation avant toute démarche.",
        "ar": "تحديد المخاطَبين والسلطات المختصة بوضعيتكم قبل أي إجراء.",
        "it": "Individuare gli interlocutori e le autorità competenti per la sua situazione prima di qualsiasi passo.",
        "en": "Identify the contacts and authorities competent for your situation before taking any step.",
    },
    {
        "fr": (
            "Méfiez-vous de toute personne qui promet un résultat contre paiement : les décisions relèvent uniquement "
            "des "
            "autorités compétentes."
        ),
        "ar": "احذروا كل من يعدكم بنتيجة مقابل أداء مالي: فالقرارات من اختصاص السلطات المختصة وحدها.",
        "it": (
            "Diffidi di chiunque prometta un risultato dietro pagamento: le decisioni spettano unicamente alle "
            "autorità competenti."
        ),
        "en": (
            "Beware of anyone who promises a result in exchange for payment: decisions rest solely with the competent "
            "authorities."
        ),
    },
    {
        "fr": "Se renseigner sur les parcours de formation avant le départ proposés dans le cadre du projet.",
        "ar": "الاستعلام عن مسارات التكوين قبل المغادرة المقترحة في إطار المشروع.",
        "it": "Informarsi sui percorsi di formazione prima della partenza proposti nell’ambito del progetto.",
        "en": "Find out about the pre-departure training pathways offered within the project.",
    },
    {
        "fr": "Réunir les titres d’études et les attestations d’expérience professionnelle dont vous disposez.",
        "ar": "جمع ما تتوفرون عليه من شهادات دراسية وإثباتات للخبرة المهنية.",
        "it": "Raccogliere i titoli di studio e gli attestati di esperienza professionale di cui dispone.",
        "en": "Gather the educational qualifications and certificates of professional experience you have.",
    },
    {
        "fr": "Réunir les titres d’études dont vous disposez et vous renseigner sur leur présentation en Italie.",
        "ar": "جمع ما تتوفرون عليه من شهادات دراسية والاستعلام عن كيفية تقديمها في إيطاليا.",
        "it": "Raccogliere i titoli di studio di cui dispone e informarsi sulla loro presentazione in Italia.",
        "en": "Gather the educational qualifications you have and find out how they are presented in Italy.",
    },
    {
        "fr": "Réunir les documents relatifs au lien familial dont vous disposez.",
        "ar": "جمع ما تتوفرون عليه من وثائق تثبت الرابطة العائلية.",
        "it": "Raccogliere i documenti relativi al legame familiare di cui dispone.",
        "en": "Gather the documents you have concerning the family relationship.",
    },
    {
        "fr": "Décrire votre projet d’activité pour en parler avec les interlocuteurs compétents.",
        "ar": "وصف مشروع نشاطكم للتحدث عنه مع المخاطَبين المختصين.",
        "it": "Descrivere il suo progetto di attività per parlarne con gli interlocutori competenti.",
        "en": "Describe your business project in order to discuss it with the competent contacts.",
    },
    {
        "fr": "Prendre contact avec l’organisme de recherche ou l’université qui pourrait vous accueillir.",
        "ar": "الاتصال بهيئة البحث أو الجامعة التي يمكن أن تستقبلكم.",
        "it": "Prendere contatto con l’ente di ricerca o l’università che potrebbe accoglierla.",
        "en": "Contact the research body or university that could host you.",
    },
    {
        "fr": "Consulter la présentation des parcours réguliers dans l’Espace Personnes.",
        "ar": "الاطلاع على عرض المسارات النظامية في فضاء الأفراد.",
        "it": "Consultare la presentazione dei percorsi regolari nell’Area Persone.",
        "en": "Consult the presentation of the regular pathways in the Individuals Area.",
    },
)


def outcome_explanation(row: dict, language: str) -> str:
    """The outcome's explanation in ``language``: the family's shared sentence with its name, or the row's own text."""
    texts = row[language]
    if "explanation" in texts:
        return texts["explanation"]
    return EXPLANATION[language].format(family=texts["family"])


def row_count() -> int:
    """The number of translation rows the seed writes per language (50: 5 + 1 + 5 + 17 + 9 + 11 ... per master
    found)."""
    return (
        len(PATHWAY_STEPS) + len(FAQ_CATEGORIES) + len(QUESTIONS) + len(CHOICES) + len(OUTCOMES) + len(CHECKLIST_ITEMS)
    )
