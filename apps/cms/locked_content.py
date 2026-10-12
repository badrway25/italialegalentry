"""
LOCKED CONTENT REGISTRY — Italy Legal Entry™

Every text below is prescribed by the source documents and must be reproduced EXACTLY
(« À INSÉRER — copier tel quel »). Do NOT rewrite, improve, abbreviate, paraphrase or translate.

Sources
-------
* ILE_Document_Implementation_FR.pdf (14 Sept 2026, Avv. Kaoutar Badrane) — Priority 1.
  Keys ``p1.*`` (Phase 1), ``p2.*`` (Phase 2), ``p3.*`` (Phase 3).
* ILE_Annexe_1_Textes_Juridiques_FR.pdf — courtesy French translation of the legal texts.
  Keys ``legal.*.fr_courtesy``. The official Italian « Allegato 1 — Testi legali » is NOT available:
  legal pages are BLOCKED_BY_MISSING_OFFICIAL_SOURCE (see docs/LEGAL_AND_PUBLICATION_GATES.md).

Integrity
---------
``locked_content.sha256.json`` stores a checksum for every key. ``tests/compliance`` fails if any
locked text changes without regenerating the checksums through ``scripts/lock_content.py``
(which is a deliberate, reviewed act recorded in git history).

Languages
---------
Only French versions were supplied. Other languages fall back to French; the template tag
marks fallback text with ``lang="fr"`` so assistive technologies pronounce it correctly.
Official IT/EN/AR versions will be added under ``LOCKED_TEXTS["it"]`` etc. when transmitted.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any

LockClass = str
LOCKED_IMPLEMENTATION_CONTENT: LockClass = "LOCKED_IMPLEMENTATION_CONTENT"
LOCKED_LEGAL_CONTENT: LockClass = "LOCKED_LEGAL_CONTENT"

FALLBACK_LANGUAGE = "fr"

# --------------------------------------------------------------------------------------------
# French texts — Implementation document (Priority 1)
# --------------------------------------------------------------------------------------------
_FR: dict[str, Any] = {
    # ---- PHASE 1 — §1.1 Espace Entreprises --------------------------------------------------
    "p1.companies.title": "DE QUELS PROFILS PROFESSIONNELS VOTRE ENTREPRISE A-T-ELLE BESOIN ?",
    "p1.companies.intro": (
        "Italy Legal Entry recueille les besoins professionnels des entreprises italiennes pour "
        "construire, avec les acteurs compétents, des parcours réguliers de formation et de "
        "mobilité. Signalez les besoins de votre entreprise : vous serez recontactés pour "
        "approfondir les collaborations possibles dans le cadre du projet."
    ),
    "p1.companies.quote": (
        "« Nous partons des besoins réels des entreprises italiennes et nous construisons, "
        "avec les acteurs compétents, des parcours réguliers de formation et de mobilité. »"
    ),
    "p1.companies.form.fields": [
        "Raison sociale de l’entreprise",
        "Secteur d’activité",
        "Siège (commune et province)",
        "Nom et fonction du référent",
        "E-mail",
        "Téléphone",
        "Profils professionnels dont l’entreprise a besoin",
        "Nombre indicatif de personnes",
        "Qualifications et compétences requises",
        "Expérience requise",
        "Exigences linguistiques",
        "Besoins de formation",
        "Calendrier indicatif",
        "Notes (champ libre)",
    ],
    "p1.companies.form.consent": (
        "J’ai lu l’information sur le traitement des données personnelles et je consens au "
        "traitement de mes données pour le suivi de la présente demande."
    ),
    "p1.companies.form.button": "MANIFESTEZ VOTRE INTÉRÊT POUR LE PROJET",
    # ---- PHASE 1 — §1.2 Parcours individuels ------------------------------------------------
    "p1.persons.replacement_1": (
        "orientation vers des parcours de formation et de mobilité régulière, construits avec les acteurs compétents"
    ),
    "p1.persons.replacement_2": (
        "recueil des besoins des entreprises et construction de parcours réguliers de formation et de mobilité"
    ),
    # ---- PHASE 1 — §1.3 Marque --------------------------------------------------------------
    "p1.trademark.mark": "Italy Legal Entry™",
    "p1.trademark.words_fr": "marque déposée",
    "p1.trademark.words_it": "marchio depositato",
    # ---- PHASE 1 — §1.1 note: unique destination of all forms --------------------------------
    "p1.email.public_contact": "contact@agamieuromed.org",
    # ---- PHASE 2 — §2.1 Forum Vénétie–Maroc -------------------------------------------------
    "p2.forum.header.title": "FORUM VÉNÉTIE–MAROC",
    "p2.forum.header.subtitle": "Dialogue juridique, coopération économique et mobilité régulière",
    "p2.forum.header.meta": "Rovigo — 2 octobre 2026 — Sala della Gran Guardia — 15h00–18h00",
    "p2.forum.header.patronage": "Sous le patronage de la Région de la Vénétie et de la Commune de Rovigo",
    "p2.forum.who.title": "QUI SOMMES-NOUS",
    "p2.forum.who.body": (
        "Le Forum est promu par AGAMI — Dialogo Giuridico Interculturale APS, association de "
        "juristes active depuis 2011 dans le dialogue juridique entre l’Italie et le Maroc, dans le "
        "cadre du projet Italy Legal Entry™ : un écosystème dédié à l’orientation, à la formation "
        "avant le départ et à l’accompagnement des parcours réguliers vers l’Italie, construit avec "
        "le concours de professionnels, d’entreprises, d’institutions, d’universités et d’organismes "
        "de formation."
    ),
    "p2.forum.why.title": "POURQUOI ITALY LEGAL ENTRY",
    "p2.forum.why.body": (
        "La mobilité vers l’Italie est trop souvent confiée à des canaux improvisés, à la "
        "désinformation et à des intermédiaires non qualifiés. Italy Legal Entry naît pour offrir "
        "l’alternative : des parcours réguliers, organisés et transparents, construits à partir des "
        "besoins réels des entreprises italiennes et fondés sur l’orientation, la formation dans le "
        "pays d’origine et l’accompagnement professionnel, dans le plein respect de la "
        "réglementation italienne et européenne. La légalité n’est pas une contrainte : c’est la voie "
        "la plus sûre et la plus efficace pour les personnes, les entreprises et les territoires."
    ),
    "p2.forum.what.title": "QU’EST-CE QUE LE FORUM",
    "p2.forum.what.body": [
        (
            "Le Forum Vénétie–Maroc naît comme espace permanent de dialogue et de coopération "
            "entre l’Italie et le Maroc, avec une attention particulière aux relations entre la Vénétie et "
            "les territoires marocains."
        ),
        (
            "L’initiative entend réunir institutions, représentations économiques, entreprises, "
            "professionnels, universités, organismes de formation et autres acteurs intéressés au "
            "développement de relations structurées entre les deux pays."
        ),
        (
            "L’objectif est de transformer le dialogue en projets concrets dans les domaines de la "
            "coopération économique, de la formation, de la mobilité régulière et des relations "
            "institutionnelles. Au cours du Forum seront également présentés Italy Legal Entry et le "
            "projet pilote Vénétie–Maroc."
        ),
    ],
    "p2.forum.objectives.title": "OBJECTIFS",
    "p2.forum.objectives.body": (
        "Favoriser le dialogue institutionnel Vénétie–Maroc ; développer les relations entre "
        "entreprises ; identifier les besoins professionnels ; développer la formation avant le "
        "départ ; promouvoir des parcours de mobilité régulière ; favoriser les collaborations "
        "universitaires ; créer des partenariats économiques et professionnels ; donner une "
        "continuité aux relations à travers le Forum Permanent Vénétie–Maroc."
    ),
    "p2.forum.audience.title": "À QUI S’ADRESSE-T-IL",
    "p2.forum.audience.body": (
        "Institutions italiennes et marocaines, entreprises, associations professionnelles, "
        "Chambres de Commerce, universités, organismes de formation, professionnels, "
        "organismes du travail et représentations diplomatiques et consulaires."
    ),
    "p2.forum.programme.title": "PROGRAMME",
    "p2.forum.programme.items": [
        "15h00 — Accueil et enregistrement",
        "Allocutions institutionnelles",
        "Présentation du Forum Permanent Vénétie–Maroc",
        "Présentation d’Italy Legal Entry",
        "Présentation du projet pilote Vénétie–Maroc",
        "Interventions institutionnelles et économiques",
        "Dialogue avec les entreprises, les universités et les partenaires",
        "Conclusions et prochaines étapes",
    ],
    "p2.forum.programme.note": (
        "Le programme détaillé des interventions est en cours de définition et sera mis à jour sur cette page."
    ),
    "p2.forum.speakers.title": "INTERVIENNENT",
    "p2.forum.speakers.body": (
        "Sont prévues, entre autres, les interventions d’un Sénateur de la République, du "
        "Conseiller du Ministre des Entreprises et du Made in Italy, du Maire de Rovigo et du "
        "Préfet de Rovigo. Les noms des intervenants seront publiés avec le programme définitif."
    ),
    "p2.forum.speakers.roles": [
        "Sénateur de la République",
        "Conseiller du Ministre des Entreprises et du Made in Italy",
        "Maire de Rovigo",
        "Préfet de Rovigo",
    ],
    "p2.forum.registration.title": "INSCRIPTION",
    "p2.forum.registration.intro": "La participation est gratuite, sur inscription préalable.",
    "p2.forum.registration.fields": [
        "Prénom",
        "Nom",
        "Organisme / Entreprise",
        "Fonction",
        "E-mail",
        "Téléphone",
        "Pays",
    ],
    "p2.forum.registration.category_label": "Catégorie",
    "p2.forum.registration.categories": [
        "Institution",
        "Entreprise",
        "Association professionnelle / Chambre de Commerce",
        "Université / Organisme de formation",
        "Professionnel",
        "Organisme du travail",
        "Représentation diplomatique ou consulaire",
        "Autre",
    ],
    "p2.forum.registration.sector_label": "Secteur d’intérêt",
    "p2.forum.registration.consent": (
        "J’ai lu l’information sur le traitement des données personnelles et je consens au "
        "traitement de mes données pour la gestion de l’inscription au Forum."
    ),
    "p2.forum.registration.button_primary": "PARTICIPEZ AU FORUM",
    "p2.forum.registration.button_secondary_pilot": "MANIFESTEZ VOTRE INTÉRÊT POUR LE PROJET PILOTE",
    "p2.forum.registration.button_secondary_collab": "PROPOSEZ UNE COLLABORATION",
    # ---- PHASE 2 — §2.2 Homepage banner ------------------------------------------------------
    "p2.home.banner.title": "FORUM VÉNÉTIE–MAROC",
    "p2.home.banner.meta": "Rovigo | 2 octobre 2026 | 15h00–18h00",
    "p2.home.banner.quote": (
        "« Institutions, entreprises, universités et professionnels pour construire de nouvelles "
        "relations entre la Vénétie et le Maroc. »"
    ),
    "p2.home.banner.button": "DÉCOUVREZ LE FORUM",
    # ---- PHASE 3 — §3.1 Hero ---------------------------------------------------------------
    "p3.hero.title": "ITALY LEGAL ENTRY™",
    "p3.hero.subtitle": "Le parcours régulier vers l’Italie, de l’orientation à l’intégration.",
    "p3.hero.body": (
        "Italy Legal Entry est un écosystème numérique italien dédié à l’orientation, à la formation "
        "et à l’accompagnement des parcours réguliers vers l’Italie, développé à travers la "
        "collaboration entre personnes, entreprises, institutions, universités, organismes de "
        "formation et professionnels."
    ),
    # ---- PHASE 3 — §3.2 Four entrances ------------------------------------------------------
    "p3.entrances.person.title": "ÊTES-VOUS UNE PERSONNE ?",
    "p3.entrances.person.text": (
        "Identifiez le parcours régulier le plus adapté à votre situation et découvrez les principales étapes."
    ),
    "p3.entrances.person.button": "DÉCOUVREZ VOTRE PARCOURS",
    "p3.entrances.company.title": "ÊTES-VOUS UNE ENTREPRISE ?",
    "p3.entrances.company.text": (
        "Signalez les besoins professionnels de votre entreprise et découvrez les parcours de "
        "formation et de mobilité régulière."
    ),
    "p3.entrances.company.button": "MANIFESTEZ VOTRE INTÉRÊT",
    "p3.entrances.institution.title": "ÊTES-VOUS UNE INSTITUTION ?",
    "p3.entrances.institution.text": (
        "Construisons ensemble des programmes et des partenariats de mobilité régulière, de "
        "formation et de coopération internationale."
    ),
    "p3.entrances.institution.button": "PROPOSEZ UNE COLLABORATION",
    "p3.entrances.university.title": "ÊTES-VOUS UNE UNIVERSITÉ OU UN ORGANISME DE FORMATION ?",
    "p3.entrances.university.text": "Formation, mobilité, stages, échanges et coopération internationale.",
    "p3.entrances.university.button": "COLLABOREZ AVEC NOUS",
    # ---- PHASE 3 — §3.3 Espace Personnes ----------------------------------------------------
    "p3.persons.title": "VOTRE PARCOURS RÉGULIER VERS L’ITALIE",
    "p3.persons.intro": (
        "Italy Legal Entry ne délivre pas de visas, de permis de séjour ni d’autorisations : ces "
        "décisions relèvent exclusivement des autorités compétentes. La plateforme vous oriente, à "
        "travers des questions progressives, vers la voie d’entrée régulière la plus adaptée à votre "
        "situation, et vous indique les étapes et la documentation généralement requises, de "
        "l’orientation à la formation avant le départ jusqu’à l’accompagnement en Italie."
    ),
    "p3.persons.pathways": [
        {
            "key": "salaried_work",
            "title": "Travail salarié",
            "description": (
                "entrées pour travail dans le cadre des quotas annuels (décret flux) et des "
                "procédures prévues par la loi."
            ),
        },
        {
            "key": "skilled_work_eu_blue_card",
            "title": "Travail qualifié — Carte bleue européenne",
            "description": (
                "pour les profils hautement qualifiés, sur la base d’un titre ou d’une expérience "
                "professionnelle reconnue."
            ),
        },
        {
            "key": "training_in_origin_country",
            "title": "Formation dans le pays d’origine",
            "description": (
                "parcours de formation professionnelle et civico-linguistique organisés avant le "
                "départ, dans le cadre prévu par la réglementation italienne."
            ),
        },
        {
            "key": "study_and_training_in_italy",
            "title": "Études et formation en Italie",
            "description": "inscription universitaire, cours de formation, échanges et mobilité académique.",
        },
        {
            "key": "family_reunification",
            "title": "Regroupement familial",
            "description": "pour les membres de famille de personnes régulièrement présentes en Italie.",
        },
        {
            "key": "self_employment_entrepreneurship",
            "title": "Travail indépendant et entrepreneuriat",
            "description": (
                "activités indépendantes, professionnelles et entrepreneuriales, dans les limites prévues par la loi."
            ),
        },
        {
            "key": "scientific_research",
            "title": "Recherche scientifique",
            "description": "chercheurs et personnel académique accueillis par des organismes agréés.",
        },
        {
            "key": "other_regular_routes",
            "title": "Autres voies régulières",
            "description": (
                "travail saisonnier et autres hypothèses prévues par la réglementation, à vérifier au cas par cas."
            ),
        },
    ],
    "p3.persons.how_it_works": (
        "Comment ça marche : répondez aux questions d’orientation → recevez une pré-évaluation "
        "à caractère informatif → préparez-vous avec la formation avant le départ → suivez la "
        "procédure régulière avec les acteurs compétents. Aucun résultat administratif n’est promis "
        "ni garanti."
    ),
    # ---- PHASE 3 — §3.4 Espace Institutions -------------------------------------------------
    "p3.institutions.intro": (
        "Italy Legal Entry promeut des modèles de coopération institutionnelle destinés à la "
        "construction de parcours réguliers, transparents et organisés de mobilité et de formation."
    ),
    "p3.institutions.recipients": (
        "Destinataires : Régions, Communes, organismes publics, Chambres de Commerce, "
        "organismes du travail, représentations diplomatiques et consulaires et institutions des "
        "pays partenaires."
    ),
    "p3.institutions.button": "PROPOSEZ UNE COLLABORATION INSTITUTIONNELLE",
    # ---- PHASE 3 — §3.5 Espace Universités et Formation ------------------------------------
    "p3.universities.intro": (
        "Universités, organismes de formation, instituts et centres de recherche : formation, "
        "stages, mobilité internationale, échanges d’étudiants, programmes conjoints, "
        "coopération académique, formation avant le départ et valorisation des compétences."
    ),
    "p3.universities.button": "PROPOSEZ UN PARTENARIAT",
    # ---- PHASE 3 — §3.6 Projet Pilote -------------------------------------------------------
    "p3.pilot.title": "PROJET PILOTE VÉNÉTIE–MAROC",
    "p3.pilot.body": (
        "Italy Legal Entry entend partir d’un projet pilote entre la Vénétie et le Maroc, construit sur "
        "les besoins des entreprises et sur la coopération avec des interlocuteurs institutionnels et "
        "de formation. Le modèle est reproductible avec d’autres territoires et d’autres pays."
    ),
    "p3.pilot.sequence": [
        "BESOINS DES ENTREPRISES",
        "PROFILS ET COMPÉTENCES",
        "FORMATION DANS LE PAYS D’ORIGINE",
        "PRÉPARATION AVANT LE DÉPART",
        "PROCÉDURES RÉGULIÈRES",
        "ENTRÉE EN ITALIE",
        "ACCOMPAGNEMENT",
        "SUIVI",
    ],
    # ---- PHASE 3 — §3.8.1 Attention aux fraudes ---------------------------------------------
    "p3.antifraud.title": "ATTENTION AUX FRAUDES",
    "p3.antifraud.body": (
        "Personne ne peut vous « vendre » un visa, un contrat de travail garanti ou une entrée "
        "assurée en Italie. Les visas et les permis sont délivrés exclusivement par les autorités "
        "compétentes, selon les procédures prévues par la loi. Méfiez-vous de quiconque "
        "demande de l’argent en échange d’un résultat garanti, propose des documents falsifiés "
        "ou des « voies rapides » en dehors des procédures officielles : ce sont des pratiques "
        "illégales qui peuvent compromettre définitivement votre parcours. Italy Legal Entry ne "
        "promet aucun résultat, n’accélère aucune procédure et travaille uniquement dans la "
        "légalité : c’est votre meilleure protection."
    ),
    # ---- PHASE 3 — §3.8.2 FAQ ---------------------------------------------------------------
    "p3.faq.items": [
        {
            "key": "faq_visas",
            "question": "Italy Legal Entry délivre-t-elle des visas ?",
            "answer": (
                "Non. Les visas, permis de séjour et autorisations relèvent exclusivement des autorités "
                "compétentes. La plateforme vous oriente vers la voie régulière la plus adaptée et vous "
                "aide à vous préparer."
            ),
        },
        {
            "key": "faq_recruitment_agency",
            "question": "Italy Legal Entry est-elle une agence de recrutement ?",
            "answer": (
                "Non. La plateforme ne sélectionne pas de candidats et n’exerce aucune intermédiation "
                "de main-d’œuvre : elle recueille les besoins des entreprises et promeut des parcours "
                "réguliers de formation et de mobilité avec les acteurs compétents."
            ),
        },
        {
            "key": "faq_preassessment_guarantee",
            "question": "La pré-évaluation garantit-elle l’entrée en Italie ?",
            "answer": (
                "Non. Il s’agit d’une orientation à caractère informatif, fondée sur les informations "
                "que vous fournissez. Chaque décision appartient aux autorités."
            ),
        },
        {
            "key": "faq_decreto_flussi",
            "question": "Qu’est-ce que le « decreto flussi » ?",
            "answer": (
                "C’est l’acte par lequel l’Italie fixe périodiquement les quotas d’entrées pour travail. "
                "Les demandes suivent des procédures et des délais officiels, publiés par les autorités."
            ),
        },
        {
            "key": "faq_diplomas",
            "question": "Italy Legal Entry reconnaît-elle les diplômes étrangers ?",
            "answer": (
                "Non. La reconnaissance relève des autorités et organismes compétents ; la plateforme "
                "vous oriente sur la documentation, les traductions, la légalisation ou l’apostille et "
                "les procédures à suivre."
            ),
        },
        {
            "key": "faq_prior_refusal",
            "question": "Un refus passé empêche-t-il toute demande future ?",
            "answer": (
                "Non. Un refus antérieur n’entraîne jamais un rejet automatique : chaque situation "
                "demande une analyse individuelle par les acteurs compétents."
            ),
        },
        {
            "key": "faq_who",
            "question": "Qui est derrière Italy Legal Entry ?",
            "answer": (
                "Le projet est promu par AGAMI — Dialogo Giuridico Interculturale APS, association de "
                "juristes active depuis 2011 dans le dialogue juridique Italie–Maroc, avec le concours "
                "de professionnels, d’entreprises, d’institutions et d’organismes de formation."
            ),
        },
        {
            "key": "faq_data_protection",
            "question": "Mes données sont-elles protégées ?",
            "answer": (
                "Oui. Les données sont traitées conformément au RGPD, conservées sur des serveurs "
                "dans l’Union européenne et ne sont jamais cédées à des tiers sans votre consentement. "
                "Voir la Privacy Policy."
            ),
        },
        {
            "key": "faq_guaranteed_visa_offer",
            "question": "Quelqu’un me propose un visa garanti contre paiement. Que faire ?",
            "answer": (
                "Refusez. Aucun résultat ne peut être garanti et aucun intermédiaire ne peut délivrer de "
                "visa. Consultez la section « Attention aux fraudes »."
            ),
        },
    ],
    # ---- PHASE 3 — §3.8.3 Glossaire ---------------------------------------------------------
    "p3.glossary.terms": [
        {
            "key": "visto_ingresso",
            "term": "Visto d’ingresso",
            "definition": "visa d’entrée délivré par les représentations diplomatiques et consulaires italiennes.",
        },
        {
            "key": "permesso_di_soggiorno",
            "term": "Permesso di soggiorno",
            "definition": "permis de séjour délivré en Italie après l’entrée, auprès de la Questura compétente.",
        },
        {
            "key": "nulla_osta",
            "term": "Nulla osta",
            "definition": (
                "autorisation préalable délivrée par le Sportello Unico per l’Immigrazione, nécessaire "
                "pour certaines entrées pour travail ou regroupement familial."
            ),
        },
        {
            "key": "decreto_flussi",
            "term": "Decreto flussi",
            "definition": "acte fixant périodiquement les quotas d’entrées régulières pour travail.",
        },
        {
            "key": "carta_blu_ue",
            "term": "Carta blu UE",
            "definition": "titre de séjour pour travailleurs hautement qualifiés.",
        },
        {
            "key": "ricongiungimento_familiare",
            "term": "Ricongiungimento familiare",
            "definition": "regroupement familial avec un proche régulièrement présent en Italie.",
        },
        {
            "key": "legalizzazione_apostille",
            "term": "Legalizzazione / Apostille",
            "definition": (
                "formalités attestant l’authenticité des documents étrangers destinés à être utilisés en Italie."
            ),
        },
        {
            "key": "dichiarazione_di_valore",
            "term": "Dichiarazione di valore",
            "definition": "document consulaire décrivant la valeur d’un titre d’études étranger.",
        },
        {
            "key": "questura_prefettura",
            "term": "Questura / Prefettura",
            "definition": (
                "autorités compétentes au niveau provincial pour les titres de séjour et certaines procédures."
            ),
        },
        {
            "key": "codice_fiscale",
            "term": "Codice fiscale",
            "definition": "identifiant fiscal italien, nécessaire pour la plupart des démarches en Italie.",
        },
    ],
    # ---- PHASE 3 — §3.8.4 Vivre en Italie ---------------------------------------------------
    "p3.living.title": "VIVRE EN ITALIE",
    "p3.living.body": (
        "Se préparer à l’arrivée, c’est aussi connaître la vie quotidienne : langue italienne, "
        "logement, santé et inscription au service sanitaire, école et éducation civique, droits et "
        "devoirs, sécurité au travail, fiscalité de base et services publics. Cette section rassemble "
        "des informations pratiques et des guides, progressivement enrichis, pour accompagner "
        "l’intégration après l’entrée régulière."
    ),
    # ---- PHASE 3 — §3.8.5 Formation après l’arrivée ----------------------------------------
    "p3.training_after.title": "FORMATION APRÈS L’ARRIVÉE",
    "p3.training_after.body": (
        "L’accompagnement ne s’arrête pas à l’entrée en Italie. Italy Legal Entry promeut, avec "
        "les organismes de formation partenaires, des parcours de formation après l’arrivée : "
        "langue italienne, éducation civique et connaissance de la vie en Italie, sécurité au travail, "
        "mise à niveau et qualification professionnelle, orientation vers les services du territoire. "
        "La formation continue est la clé d’une intégration réussie — pour les personnes comme "
        "pour les entreprises qui les accueillent."
    ),
    # ---- PHASE 3 — §3.8.6 Actualités & newsletter -------------------------------------------
    "p3.news.title": "ACTUALITÉS",
    "p3.news.body": (
        "Nouveautés normatives, échéances officielles, initiatives du Forum Permanent Vénétie–Maroc "
        "et activités de l’écosystème."
    ),
    "p3.news.newsletter_label": "Restez informés",
    "p3.news.newsletter_consent": (
        "Je souhaite recevoir les communications informatives d’Italy Legal Entry et je consens au "
        "traitement de mes données à cette fin (consentement révocable à tout moment)."
    ),
    # ---- PHASE 3 — §3.8.7 Forum Virtuel -----------------------------------------------------
    "p3.virtual_forum.title": "FORUM VIRTUEL",
    "p3.virtual_forum.body": (
        "Le Forum ne s’arrête pas à l’événement. Le Forum Virtuel est l’espace de dialogue et de "
        "communication du site, réservé aux participants — institutions, entreprises, universités, "
        "organismes de formation et professionnels — pour poursuivre les échanges, partager "
        "documents et initiatives, proposer des collaborations et suivre les projets nés du Forum. "
        "L’accès se fait sur inscription."
    ),
    "p3.virtual_forum.button": "ACCÉDEZ AU FORUM VIRTUEL",
    # ---- PHASE 3 — §3.9 Diplômes ------------------------------------------------------------
    "p3.diplomas.title": "DIPLÔMES ET TITRES ÉTRANGERS",
    "p3.diplomas.body": (
        "Faire valoir en Italie un diplôme ou une qualification obtenus à l’étranger demande des "
        "démarches précises : documentation, traductions, légalisation ou apostille lorsque "
        "nécessaire, déclaration de valeur, procédures de reconnaissance auprès des autorités "
        "compétentes. Italy Legal Entry ne reconnaît pas directement les diplômes : la plateforme "
        "vous oriente sur les étapes, les documents généralement requis et les autorités "
        "auxquelles vous adresser, pour que vos compétences soient valorisées par la voie "
        "régulière."
    ),
    # ---- PHASE 3 — §3.10 Espace réservé -----------------------------------------------------
    "p3.reserved.title": "ESPACE RÉSERVÉ",
    "p3.reserved.body": (
        "Accédez à votre espace personnel pour suivre vos demandes, vos parcours et vos communications."
    ),
    "p3.reserved.button": "CONNEXION",
}

# --------------------------------------------------------------------------------------------
# Legal texts — courtesy French translation (Annexe 1). NOT the official version.
# Publication of these FR texts requires written confirmation by Avv. Badrane.
# The internal operational note of the Cookie Policy is intentionally NOT included.
# --------------------------------------------------------------------------------------------
_FR_LEGAL: dict[str, Any] = {
    "legal.courtesy_notice.fr": "Traduction de courtoisie — la version italienne fait foi",
    "legal.privacy.fr_courtesy": {
        "title": "Information sur le traitement des données personnelles (Privacy Policy)",
        "intro": (
            "Information fournie au sens des art. 13 et 14 du Règlement (UE) 2016/679 (« RGPD ») et du "
            "D.Lgs. 196/2003, tel que modifié par le D.Lgs. 101/2018, aux utilisateurs du site "
            "legalitalentry.it et de la plateforme Italy Legal Entry."
        ),
        "sections": [
            {
                "heading": "1. Responsable du traitement",
                "body": (
                    "Le responsable du traitement est AGAMI — Dialogo Giuridico Interculturale APS, "
                    "association de promotion sociale inscrite au RUNTS (Rep. n° 149809), code fiscal "
                    "91036640240, siège social Via Sandrigo 29, 36061 Bassano del Grappa (VI), siège "
                    "opérationnel Viale Giuseppe Mazzini 142, 00195 Rome. Le responsable peut être contacté à "
                    "l’adresse contact@agamieuromed.org. L’activation d’une adresse dédiée du domaine "
                    "legalitalentry.it sera communiquée par mise à jour de la présente information."
                ),
            },
            {
                "heading": "2. Catégories de données traitées",
                "body": (
                    "Sont traitées à travers le site : les données de navigation acquises automatiquement par les "
                    "systèmes informatiques (adresses IP, journaux d’accès, données techniques de l’appareil), "
                    "nécessaires au fonctionnement et à la sécurité du site ; les données fournies volontairement "
                    "par les utilisateurs via les formulaires disponibles, en particulier les données d’identification "
                    "et de contact, les informations relatives à la situation personnelle pertinente pour l’orientation "
                    "demandée (objectif du parcours, niveau linguistique, titres et qualifications), les données "
                    "relatives à l’entreprise et aux besoins professionnels indiqués dans le formulaire dédié aux "
                    "entreprises, ainsi que les données d’inscription aux événements promus par la plateforme. "
                    "L’utilisateur est invité à ne pas insérer dans les champs libres des catégories particulières de "
                    "données au sens de l’art. 9 du RGPD, non requises pour les finalités du service."
                ),
            },
            {
                "heading": "3. Finalités et bases juridiques",
                "body": (
                    "Les données sont traitées pour les finalités suivantes : répondre aux demandes d’orientation "
                    "et d’information des utilisateurs et gérer les parcours informatifs de la plateforme, sur la base "
                    "de l’exécution de mesures précontractuelles prises à la demande de la personne concernée "
                    "(art. 6, par. 1, lett. b, RGPD) ; recueillir et gérer les manifestations d’intérêt des entreprises et "
                    "les inscriptions aux événements, sur la même base juridique ; respecter les obligations "
                    "légales du responsable (art. 6, par. 1, lett. c, RGPD) ; garantir la sécurité du site et prévenir "
                    "les abus, sur la base de l’intérêt légitime du responsable (art. 6, par. 1, lett. f, RGPD). L’envoi "
                    "d’éventuelles communications informatives périodiques n’aura lieu qu’avec le consentement "
                    "exprès et révocable de la personne concernée (art. 6, par. 1, lett. a, RGPD)."
                ),
            },
            {
                "heading": "4. Caractère du recueil et processus décisionnels",
                "body": (
                    "La communication des données demandées dans les formulaires est facultative, mais "
                    "l’absence des données indiquées comme nécessaires empêche de répondre à la demande. "
                    "Les résultats restitués par la plateforme constituent des pré-évaluations à caractère "
                    "exclusivement informatif : aucun traitement ne donne lieu à des décisions fondées "
                    "uniquement sur des processus automatisés produisant des effets juridiques sur la personne "
                    "concernée au sens de l’art. 22 du RGPD, et toute décision administrative relève "
                    "exclusivement des autorités publiques."
                ),
            },
            {
                "heading": "5. Destinataires des données",
                "body": (
                    "Les données peuvent être traitées, pour le compte du responsable et sur la base d’actes de "
                    "désignation au sens de l’art. 28 du RGPD, par les prestataires assurant la gestion technique "
                    "et l’hébergement du site et de la plateforme. Les données des entreprises et des personnes "
                    "concernées ne sont ni communiquées à des tiers ni mises en relation entre elles sans le "
                    "consentement exprès de la personne concernée. Les données ne sont en aucun cas "
                    "diffusées."
                ),
            },
            {
                "heading": "6. Lieu du traitement et transferts",
                "body": (
                    "Les données sont conservées sur des serveurs situés dans l’Union européenne et ne sont "
                    "pas transférées vers des pays tiers. Si, pour le développement de projets de coopération "
                    "spécifiques, un transfert vers des pays tiers devenait nécessaire, il n’interviendrait que dans "
                    "le respect des conditions et garanties prévues par les art. 44 et suivants du RGPD, avec mise "
                    "à jour préalable de la présente information. Les utilisateurs accédant depuis le Royaume du "
                    "Maroc bénéficient également, en tant que de besoin, des protections prévues par la loi "
                    "marocaine n° 09-08 relative à la protection des personnes physiques à l’égard du traitement "
                    "des données à caractère personnel."
                ),
            },
            {
                "heading": "7. Durées de conservation",
                "body": (
                    "Les données recueillies via les formulaires sont conservées le temps nécessaire pour "
                    "répondre à la demande et, en tout état de cause, pour une durée n’excédant pas vingt-quatre "
                    "mois à compter du dernier contact, sous réserve des obligations légales de conservation et "
                    "de la protection des droits du responsable. Les données de navigation sont conservées pour "
                    "les seules durées techniques strictement nécessaires."
                ),
            },
            {
                "heading": "8. Droits des personnes concernées",
                "body": (
                    "Les personnes concernées peuvent exercer à tout moment les droits reconnus par les art. 15 "
                    "à 22 du RGPD — accès, rectification, effacement, limitation du traitement, portabilité et "
                    "opposition — en écrivant à contact@agamieuromed.org. Reste sauf le droit d’introduire une "
                    "réclamation auprès du Garante per la protezione dei dati personali au sens de l’art. 77 du "
                    "RGPD (www.garanteprivacy.it)."
                ),
            },
        ],
    },
    "legal.cookies.fr_courtesy": {
        "title": "Politique des cookies (Cookie Policy)",
        "intro": (
            "La présente information est fournie conformément à la décision du Garante per la protezione "
            "dei dati personali du 10 juin 2021 (« Lignes directrices cookies et autres outils de traçage »), "
            "à l’art. 122 du D.Lgs. 196/2003 et à l’art. 13 du RGPD."
        ),
        "sections": [
            {
                "heading": "",
                "body": (
                    "Le site legalitalentry.it utilise exclusivement des cookies techniques, nécessaires au "
                    "fonctionnement du site, à la mémorisation de la langue sélectionnée et à la sécurité de la "
                    "navigation. Ces cookies ne requièrent pas le consentement de l’utilisateur. Le site n’utilise "
                    "pas de cookies de profilage, ni propres ni de tiers, et n’emploie pas d’outils d’analyse "
                    "comportant le traçage des utilisateurs."
                ),
            },
            {
                "heading": "",
                "body": (
                    "Certaines pages peuvent intégrer des contenus techniques hébergés par des fournisseurs "
                    "externes (images ou ressources graphiques) : ces fournisseurs peuvent connaître l’adresse "
                    "IP de l’utilisateur aux seules fins de la fourniture du contenu demandé. Si des cookies "
                    "analytiques ou de tiers étaient introduits à l’avenir, le site adopterait préalablement un "
                    "bandeau de recueil du consentement conforme aux Lignes directrices du Garante et la "
                    "présente information serait mise à jour, avec indication de la date de dernière révision."
                ),
            },
            {
                "heading": "",
                "body": (
                    "L’utilisateur peut en tout état de cause gérer ou désactiver les cookies via les paramètres de "
                    "son navigateur ; la désactivation des cookies techniques peut toutefois compromettre "
                    "certaines fonctionnalités du site."
                ),
            },
        ],
    },
    "legal.notices.fr_courtesy": {
        "title": "Mentions légales",
        "intro": "",
        "sections": [
            {
                "heading": "",
                "body": (
                    "Le site legalitalentry.it et la plateforme Italy Legal Entry sont promus par AGAMI — Dialogo "
                    "Giuridico Interculturale APS, association de promotion sociale constituée au sens du "
                    "D.Lgs. 117/2017, inscrite au Registre unique national du Tiers secteur (Rep. n° 149809), "
                    "code fiscal 91036640240, siège social Via Sandrigo 29, 36061 Bassano del Grappa (VI), "
                    "siège opérationnel Viale Giuseppe Mazzini 142, 00195 Rome — e-mail : "
                    "contact@agamieuromed.org."
                ),
            },
            {
                "heading": "",
                "body": (
                    "« Italy Legal Entry » est une marque déposée : demande de marque de l’Union européenne "
                    "n° 019405072, déposée auprès de l’EUIPO le 4 août 2026 pour les classes 35, 42 et 45, et "
                    "enregistrement auprès de l’OMPIC (Royaume du Maroc) n° PR-261439. Les marques "
                    "appartiennent à Me Kaoutar Badrane et sont utilisées par la plateforme avec le "
                    "consentement de leur titulaire. Tout usage non autorisé des marques, signes distinctifs et de "
                    "l’identité visuelle de la plateforme est interdit."
                ),
            },
            {
                "heading": "",
                "body": (
                    "Tous les contenus du site — textes, élaborations, architecture informative, matériels "
                    "graphiques originaux — sont protégés par la loi italienne n° 633 du 22 avril 1941 et par les "
                    "conventions internationales en matière de droit d’auteur. Leur reproduction, extraction ou "
                    "réutilisation, totale ou partielle, sans autorisation écrite est interdite. Les images de banque "
                    "sont utilisées dans les limites de leurs licences respectives."
                ),
            },
            {
                "heading": "",
                "body": (
                    "Les contenus du site ont une nature informative et d’orientation générale ; ils sont mis à jour "
                    "avec la diligence professionnelle requise mais ne constituent ni un conseil juridique individuel "
                    "ni une source officielle des normes citées, pour lesquelles seuls font foi les textes publiés "
                    "dans les sources officielles."
                ),
            },
        ],
    },
    "legal.terms.fr_courtesy": {
        "title": "Conditions d’utilisation",
        "intro": (
            "L’accès au site legalitalentry.it et l’utilisation de la plateforme Italy Legal Entry emportent "
            "acceptation des présentes conditions d’utilisation."
        ),
        "sections": [
            {
                "heading": "Art. 1 — Nature du service",
                "body": (
                    "La plateforme fournit des services d’information, d’orientation, de préparation documentaire "
                    "et de formation préparatoire en matière de parcours réguliers de mobilité vers l’Italie. La "
                    "plateforme n’est pas une agence pour l’emploi, n’exerce pas d’activité d’intermédiation entre "
                    "l’offre et la demande de travail au sens de l’art. 4 du D.Lgs. 276/2003, ne délivre ni visas, ni "
                    "permis de séjour, ni autorisations, ni reconnaissances de titres, ne garantit ni résultats "
                    "administratifs ni délais des procédures, et n’intervient pas auprès des autorités publiques au "
                    "nom ou pour le compte des utilisateurs. Toute décision relève exclusivement des autorités "
                    "publiques italiennes, européennes et des pays partenaires."
                ),
            },
            {
                "heading": "Art. 2 — Résultats informatifs",
                "body": (
                    "Les orientations, listes de contrôle et résultats restitués par la plateforme constituent des pré-"
                    "évaluations à caractère informatif, élaborées sur la base des informations fournies par "
                    "l’utilisateur. Ils ne constituent ni actes administratifs ni conseil juridique individuel, lequel ne "
                    "peut être rendu que par des professionnels habilités après examen du cas concret."
                ),
            },
            {
                "heading": "Art. 3 — Obligations de l’utilisateur",
                "body": (
                    "L’utilisateur s’engage à fournir des informations véridiques, complètes et à jour, à ne pas "
                    "téléverser de documents faux, contrefaits ou altérés, et à ne pas utiliser la plateforme à des "
                    "fins illicites ou de contournement de la réglementation en matière d’immigration. La "
                    "plateforme se réserve de ne pas donner suite aux demandes fondées sur des déclarations "
                    "inexactes ou des documents non véridiques."
                ),
            },
            {
                "heading": "Art. 4 — Propriété intellectuelle",
                "body": (
                    "Les marques, contenus et matériels de la plateforme sont protégés conformément aux "
                    "Mentions légales, qui font partie intégrante des présentes conditions."
                ),
            },
            {
                "heading": "Art. 5 — Responsabilité",
                "body": (
                    "Sous réserve des limites impératives de la loi, le gestionnaire de la plateforme ne répond ni "
                    "des décisions prises par les autorités compétentes, ni des conséquences d’informations "
                    "inexactes ou incomplètes fournies par l’utilisateur, ni des interruptions techniques du service "
                    "dues à des causes non imputables. Rien dans les présentes conditions ne limite la "
                    "responsabilité pour dol ou faute lourde ni les droits impérativement reconnus aux "
                    "consommateurs par le D.Lgs. 206/2005."
                ),
            },
            {
                "heading": "Art. 6 — Loi applicable et juridiction",
                "body": (
                    "Les présentes conditions sont régies par la loi italienne. Tout litige relève du tribunal de "
                    "Vicence, sous réserve, pour les utilisateurs ayant la qualité de consommateurs, de la "
                    "compétence impérative du tribunal du lieu de résidence ou de domicile du consommateur au "
                    "sens du D.Lgs. 206/2005."
                ),
            },
        ],
    },
    "legal.disclaimer.fr_courtesy": {
        "title": "Avertissement (Disclaimer)",
        "intro": "",
        "sections": [
            {
                "heading": "",
                "body": (
                    "Italy Legal Entry fournit une orientation informative et un accompagnement préparatoire. "
                    "Toutes les décisions en matière de visas, d’entrées, de séjours et de reconnaissances "
                    "relèvent exclusivement des autorités publiques. Les résultats générés par la plateforme sont "
                    "des pré-évaluations informatives : ils ne constituent ni actes administratifs ni conseil juridique "
                    "individualisé."
                ),
            },
            {
                "heading": "",
                "body": (
                    "Les parcours de formation promus par la plateforme et ses partenaires ont une nature "
                    "d’orientation et de préparation et sont distincts des programmes de formation professionnelle "
                    "et civico-linguistique approuvés au sens de l’art. 23 du D.Lgs. 286/1998. Une attestation "
                    "délivrée par la plateforme ne constitue en aucun cas une approbation ministérielle. Les "
                    "initiatives présentées sur le site, y compris le projet pilote Vénétie–Maroc, sont décrites dans "
                    "leur état réel d’avancement et n’impliquent pas l’existence de canaux d’entrée déjà autorisés "
                    "ou opérationnels, jusqu’à l’achèvement des parcours institutionnels correspondants."
                ),
            },
            {
                "heading": "",
                "body": (
                    "Un refus antérieur n’entraîne jamais un rejet automatique des demandes futures : chaque "
                    "situation exige une analyse individuelle par les acteurs compétents."
                ),
            },
        ],
    },
}

LOCKED_TEXTS: dict[str, dict[str, Any]] = {
    "fr": {**_FR, **_FR_LEGAL},
    # "it": {...}  — to be added ONLY from officially transmitted texts (never machine-translated)
    # "en": {...}
    # "ar": {...}
}

LOCK_CLASS: dict[str, LockClass] = {
    **dict.fromkeys(_FR, LOCKED_IMPLEMENTATION_CONTENT),
    **dict.fromkeys(_FR_LEGAL, LOCKED_LEGAL_CONTENT),
}


class LockedContentMissing(KeyError):
    pass


def keys() -> list[str]:
    return sorted(LOCKED_TEXTS["fr"])


def get(key: str, language: str | None = None) -> tuple[Any, str]:
    """
    Return ``(value, effective_language)``. Falls back to French when the requested language
    has no *official* locked version. Raises LockedContentMissing for unknown keys.
    """
    if key not in LOCKED_TEXTS["fr"]:
        raise LockedContentMissing(key)
    lang = (language or FALLBACK_LANGUAGE).split("-")[0]
    if lang in LOCKED_TEXTS and key in LOCKED_TEXTS[lang]:
        return LOCKED_TEXTS[lang][key], lang
    return LOCKED_TEXTS["fr"][key], "fr"


class LockedText(str):
    """
    A prescribed text that remembers the language it is written in.

    ``fallback_lang`` is set when that language differs from the one that was requested (today: every
    non-French page shows the French text). Components read it to emit ``<span lang="fr">`` — right
    screen-reader voice (WCAG 3.1.2) and left-to-right isolation inside Arabic pages — without every
    view having to pass the language around. It behaves as a plain ``str`` everywhere else.
    """

    lang: str = ""
    fallback_lang: str = ""

    def __new__(cls, value: str, lang: str = "", requested: str = ""):
        obj = super().__new__(cls, value)
        obj.lang = lang
        obj.fallback_lang = lang if lang and lang != requested else ""
        return obj


def text(key: str, language: str | None = None) -> LockedText:
    value, effective = get(key, language)
    if not isinstance(value, str):
        raise TypeError(f"Locked key {key!r} is not a plain string")
    requested = (language or FALLBACK_LANGUAGE).split("-")[0]
    return LockedText(value, effective, requested)


def available_languages(key: str) -> list[str]:
    return [lang for lang, table in LOCKED_TEXTS.items() if key in table]


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def checksum(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def checksums(language: str = "fr") -> dict[str, str]:
    return {k: checksum(v) for k, v in sorted(LOCKED_TEXTS[language].items())}
