"""
Seed of ruleset v1 — neutral situational questions mapped to the eight locked pathway keys.

CONTENT_PENDING_LEGAL_REVIEW: no legal criterion is asserted anywhere. The questions ask about the
person's *project* (work, study, family, independent activity, research); the outcomes only say
which pathway family the project corresponds to, that every decision rests with the competent
authorities, and which generic informational steps follow. The locked disclaimer
(``p3.persons.how_it_works``) is rendered by the template, never stored.

Idempotent: v1 is created once; editorial changes made afterwards in the back-office are never
overwritten. It is activated only when no ruleset is active yet.
"""

from __future__ import annotations

from core.seeds import register_seed
from orientation import engine
from orientation.constants import NEEDS_INDIVIDUAL_ANALYSIS

V1_NOTES = (
    "Ruleset initial v1 — questions situationnelles neutres, sans critère légal. "
    "CONTENT_PENDING_LEGAL_REVIEW : à faire relire par la revue légale avant toute modification de fond."
)

STEPS_ITEM = "Consulter la page du parcours dans l’Espace Personnes pour connaître les principales étapes."
DOCS_ITEM = (
    "Vérifier les documents généralement requis auprès des autorités compétentes et rassembler ceux dont vous disposez."
)
AUTH_ITEM = "Identifier les interlocuteurs et les autorités compétents pour votre situation avant toute démarche."
WARN_ITEM = (
    "Méfiez-vous de toute personne qui promet un résultat contre paiement : les décisions relèvent "
    "uniquement des autorités compétentes."
)
TRAINING_ITEM = "Se renseigner sur les parcours de formation avant le départ proposés dans le cadre du projet."


def _generic_checklist(*extra: tuple[str, str]) -> tuple[engine.ChecklistItemSpec, ...]:
    items = [
        engine.ChecklistItemSpec(STEPS_ITEM, "steps", 1),
        engine.ChecklistItemSpec(DOCS_ITEM, "documents", 1),
        engine.ChecklistItemSpec(AUTH_ITEM, "authorities", 1),
        engine.ChecklistItemSpec(WARN_ITEM, "warnings", 1),
    ]
    for i, (category, text) in enumerate(extra, start=2):
        items.append(engine.ChecklistItemSpec(text, category, i))
    return tuple(items)


def _explanation(family: str) -> str:
    return (
        f"D’après vos réponses, votre projet semble correspondre à la famille de parcours « {family} » "
        "présentée dans l’Espace Personnes. Cette pré-évaluation a un caractère purement informatif : "
        "toute décision relève exclusivement des autorités compétentes. Prochaines étapes à caractère "
        "informatif : consulter la page du parcours, préparer la documentation généralement requise et "
        "prendre contact avec les acteurs compétents."
    )


def build_v1_spec() -> engine.RulesetSpec:
    questions = (
        engine.QuestionSpec(
            key="objective",
            order=1,
            is_entry=True,
            text_fr="Quel est l’objectif principal de votre projet vers l’Italie ?",
            help_fr=(
                "Choisissez la situation qui décrit le mieux votre projet. Aucune donnée personnelle n’est "
                "demandée et vous pourrez revenir en arrière à tout moment."
            ),
            choices=(
                engine.ChoiceSpec("work", "Travailler en Italie", 1),
                engine.ChoiceSpec("study", "Étudier ou suivre une formation", 2),
                engine.ChoiceSpec("family", "Rejoindre un membre de ma famille en Italie", 3),
                engine.ChoiceSpec("self_employment", "Exercer une activité indépendante ou entrepreneuriale", 4),
                engine.ChoiceSpec("research", "Mener une activité de recherche scientifique", 5),
                engine.ChoiceSpec("other", "Autre situation, ou je ne sais pas encore", 6),
            ),
        ),
        engine.QuestionSpec(
            key="work_profile",
            order=2,
            text_fr="Quelle description correspond le mieux à votre projet professionnel ?",
            help_fr=(
                "Cette question sert uniquement à identifier la famille de parcours à consulter ; elle ne "
                "constitue pas une évaluation de votre profil."
            ),
            choices=(
                engine.ChoiceSpec("salaried", "Un emploi salarié auprès d’une entreprise en Italie", 1),
                engine.ChoiceSpec(
                    "highly_qualified",
                    "Un profil hautement qualifié (diplôme de l’enseignement supérieur ou expérience "
                    "professionnelle qualifiée)",
                    2,
                ),
                engine.ChoiceSpec("seasonal", "Un travail saisonnier ou temporaire", 3),
                engine.ChoiceSpec("unsure", "Je ne sais pas encore", 4),
            ),
        ),
        engine.QuestionSpec(
            key="study_type",
            order=3,
            text_fr="Quel type de parcours d’études ou de formation envisagez-vous ?",
            help_fr="Les études et la formation peuvent se dérouler en Italie ou, avant le départ, dans votre pays.",
            choices=(
                engine.ChoiceSpec("university", "Une inscription universitaire ou un échange académique en Italie", 1),
                engine.ChoiceSpec("vocational_in_italy", "Un cours de formation professionnelle en Italie", 2),
                engine.ChoiceSpec(
                    "training_before_departure",
                    "Une formation professionnelle ou linguistique avant le départ, depuis mon pays",
                    3,
                ),
                engine.ChoiceSpec("unsure", "Je ne sais pas encore", 4),
            ),
        ),
        engine.QuestionSpec(
            key="family_member_status",
            order=4,
            text_fr="Le membre de votre famille que vous souhaitez rejoindre est-il régulièrement présent en Italie ?",
            help_fr=(
                "Répondez selon ce que vous savez aujourd’hui. En cas de doute, choisissez « Je ne sais pas » : "
                "la situation sera à examiner avec les acteurs compétents."
            ),
            choices=(
                engine.ChoiceSpec("yes", "Oui", 1),
                engine.ChoiceSpec("no", "Non", 2),
                engine.ChoiceSpec("unsure", "Je ne sais pas", 3),
            ),
        ),
        engine.QuestionSpec(
            key="training_interest",
            order=5,
            type="boolean",
            text_fr=(
                "Souhaitez-vous recevoir des informations sur la formation avant le départ "
                "(professionnelle, linguistique, civique) ?"
            ),
            help_fr=(
                "La formation avant le départ est un temps de préparation proposé dans le cadre du projet ; "
                "cette réponse ne modifie pas l’orientation."
            ),
        ),
    )
    outcomes = (
        engine.OutcomeSpec(
            key="salaried_work",
            pathway_key="salaried_work",
            title_fr="Orientation vers un parcours de travail salarié",
            explanation_fr=_explanation("travail salarié"),
            checklist=_generic_checklist(("steps", TRAINING_ITEM)),
        ),
        engine.OutcomeSpec(
            key="skilled_work",
            pathway_key="skilled_work_eu_blue_card",
            title_fr="Orientation vers un parcours de travail qualifié",
            explanation_fr=_explanation("travail qualifié"),
            checklist=_generic_checklist(
                (
                    "documents",
                    "Réunir les titres d’études et les attestations d’expérience professionnelle dont vous disposez.",
                ),
                ("steps", TRAINING_ITEM),
            ),
        ),
        engine.OutcomeSpec(
            key="training_origin",
            pathway_key="training_in_origin_country",
            title_fr="Orientation vers un parcours de formation avant le départ",
            explanation_fr=_explanation("formation dans le pays d’origine"),
            checklist=_generic_checklist(("steps", TRAINING_ITEM)),
        ),
        engine.OutcomeSpec(
            key="study_italy",
            pathway_key="study_and_training_in_italy",
            title_fr="Orientation vers un parcours d’études ou de formation en Italie",
            explanation_fr=_explanation("études et formation en Italie"),
            checklist=_generic_checklist(
                (
                    "documents",
                    "Réunir les titres d’études dont vous disposez et vous renseigner sur leur présentation en Italie.",
                ),
            ),
        ),
        engine.OutcomeSpec(
            key="family",
            pathway_key="family_reunification",
            title_fr="Orientation vers un parcours de regroupement familial",
            explanation_fr=_explanation("regroupement familial"),
            checklist=_generic_checklist(
                ("documents", "Réunir les documents relatifs au lien familial dont vous disposez."),
            ),
        ),
        engine.OutcomeSpec(
            key="self_employment",
            pathway_key="self_employment_entrepreneurship",
            title_fr="Orientation vers un parcours de travail indépendant ou d’entrepreneuriat",
            explanation_fr=_explanation("travail indépendant et entrepreneuriat"),
            checklist=_generic_checklist(
                ("steps", "Décrire votre projet d’activité pour en parler avec les interlocuteurs compétents."),
            ),
        ),
        engine.OutcomeSpec(
            key="research",
            pathway_key="scientific_research",
            title_fr="Orientation vers un parcours de recherche scientifique",
            explanation_fr=_explanation("recherche scientifique"),
            checklist=_generic_checklist(
                (
                    "authorities",
                    "Prendre contact avec l’organisme de recherche ou l’université qui pourrait vous accueillir.",
                ),
            ),
        ),
        engine.OutcomeSpec(
            key="other_routes",
            pathway_key="other_regular_routes",
            title_fr="Orientation vers les autres voies régulières",
            explanation_fr=_explanation("autres voies régulières"),
            checklist=_generic_checklist(("steps", TRAINING_ITEM)),
        ),
        engine.OutcomeSpec(
            key="individual_analysis",
            pathway_key=NEEDS_INDIVIDUAL_ANALYSIS,
            title_fr="Situation à examiner individuellement",
            explanation_fr=(
                "Vos réponses ne permettent pas d’identifier une famille de parcours unique. Cette pré-évaluation "
                "a un caractère purement informatif : toute décision relève exclusivement des autorités "
                "compétentes. Prochaines étapes à caractère informatif : consulter la présentation des parcours "
                "réguliers dans l’Espace Personnes et prendre contact avec les acteurs compétents pour un examen "
                "individuel de votre situation."
            ),
            checklist=(
                engine.ChecklistItemSpec(
                    "Consulter la présentation des parcours réguliers dans l’Espace Personnes.", "steps", 1
                ),
                engine.ChecklistItemSpec(AUTH_ITEM, "authorities", 1),
                engine.ChecklistItemSpec(WARN_ITEM, "warnings", 1),
            ),
        ),
    )

    def eq(key: str, value):
        return {"question_key": key, "op": "eq", "value": value}

    rules = (
        # --- work branch ------------------------------------------------------------------
        engine.RuleSpec(
            "Travail → profil professionnel", eq("objective", "work"), next_question="work_profile", order=10
        ),
        engine.RuleSpec(
            "Travail (profil connu) → intérêt formation avant le départ",
            {
                "all": [
                    eq("objective", "work"),
                    {"question_key": "work_profile", "op": "in", "value": ["salaried", "highly_qualified", "seasonal"]},
                ]
            },
            next_question="training_interest",
            order=20,
        ),
        engine.RuleSpec(
            "Travail salarié",
            {"all": [eq("objective", "work"), eq("work_profile", "salaried")]},
            outcome="salaried_work",
            order=30,
        ),
        engine.RuleSpec(
            "Travail qualifié",
            {"all": [eq("objective", "work"), eq("work_profile", "highly_qualified")]},
            outcome="skilled_work",
            order=31,
        ),
        engine.RuleSpec(
            "Travail saisonnier → autres voies",
            {"all": [eq("objective", "work"), eq("work_profile", "seasonal")]},
            outcome="other_routes",
            order=32,
        ),
        engine.RuleSpec(
            "Travail (profil inconnu) → examen individuel",
            {"all": [eq("objective", "work"), eq("work_profile", "unsure")]},
            outcome="individual_analysis",
            order=33,
        ),
        # --- study branch -----------------------------------------------------------------
        engine.RuleSpec("Études → type de parcours", eq("objective", "study"), next_question="study_type", order=40),
        engine.RuleSpec(
            "Études en Italie",
            {
                "all": [
                    eq("objective", "study"),
                    {
                        "question_key": "study_type",
                        "op": "in",
                        "value": ["university", "vocational_in_italy", "unsure"],
                    },
                ]
            },
            outcome="study_italy",
            order=41,
        ),
        engine.RuleSpec(
            "Formation avant le départ",
            {"all": [eq("objective", "study"), eq("study_type", "training_before_departure")]},
            outcome="training_origin",
            order=42,
        ),
        # --- family branch ----------------------------------------------------------------
        engine.RuleSpec(
            "Famille → présence régulière", eq("objective", "family"), next_question="family_member_status", order=50
        ),
        engine.RuleSpec(
            "Regroupement familial",
            {"all": [eq("objective", "family"), eq("family_member_status", "yes")]},
            outcome="family",
            order=51,
        ),
        engine.RuleSpec(
            "Famille (situation à examiner)",
            {
                "all": [
                    eq("objective", "family"),
                    {"question_key": "family_member_status", "op": "in", "value": ["no", "unsure"]},
                ]
            },
            outcome="individual_analysis",
            order=52,
        ),
        # --- direct outcomes --------------------------------------------------------------
        engine.RuleSpec(
            "Activité indépendante", eq("objective", "self_employment"), outcome="self_employment", order=60
        ),
        engine.RuleSpec("Recherche scientifique", eq("objective", "research"), outcome="research", order=70),
        engine.RuleSpec(
            "Autre situation → examen individuel", eq("objective", "other"), outcome="individual_analysis", order=80
        ),
    )
    return engine.RulesetSpec(version=1, questions=questions, outcomes=outcomes, rules=rules, notes=V1_NOTES)


@register_seed("orientation.ruleset_v1", order=60)
def seed_ruleset_v1() -> str:
    from orientation.models import Ruleset, RulesetStatus
    from orientation.services import activate_ruleset, materialise_spec

    spec = build_v1_spec()
    report = engine.validate(spec)
    if not report.ok:  # pragma: no cover - guarded by tests
        raise RuntimeError("ruleset v1 seed is invalid: " + "; ".join(report.errors))
    ruleset, created = Ruleset.objects.get_or_create(version=1, defaults={"notes": V1_NOTES})
    if created:
        materialise_spec(ruleset, spec)
    if not Ruleset.objects.filter(status=RulesetStatus.ACTIVE).exists() and ruleset.status == RulesetStatus.DRAFT:
        activate_ruleset(ruleset)
        return "ruleset v1 created and activated" if created else "ruleset v1 activated"
    return "ruleset v1 created" if created else "ruleset v1 present"
