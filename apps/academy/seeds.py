"""
Academy seeds — a small, realistic, SYNTHETIC catalogue.

Everything here is invented for demonstration. No provider is a real organisation (each one says so
in its ``note``), no text is copied from the previous platform, and no personal data appears
anywhere. The catalogue covers the seven families of the Master Dossier so the domain filter has
something to filter, and one course is left in DRAFT so the "a person never sees an unpublished
course" rule can be seen working as well as tested.

Idempotent: ``get_or_create`` on the stable slug, defaults applied on creation only, so an editor's
corrections are never overwritten by the next deploy.

The demonstration TRAINING PLAN at the end attaches only to accounts in the reserved
``@example.test`` domain (RFC 2606), which can never be a real person: a seed that runs on every
deploy must not be able to write a training plan for a living account.
"""

from __future__ import annotations

from django.contrib.auth import get_user_model
from django.utils import timezone

from academy.models import (
    Competence,
    CompetenceArea,
    CompetenceLevel,
    Course,
    CourseCompetence,
    CourseFormat,
    CourseMaterial,
    CourseModule,
    CourseStatus,
    CourseType,
    MaterialKind,
    ModuleKind,
    PlanOrigin,
    PlanStatus,
    ProviderKind,
    SkillGapLine,
    TrainingPlan,
    TrainingPlanItem,
    TrainingProvider,
)
from core.seeds import demonstration_data_allowed, register_seed

DEMO_NOTE = "Organisme fictif — données de démonstration."

PROVIDERS = (
    {
        "slug": "centre-langue-exemple",
        "name": "Centre de langue italienne (exemple)",
        "kind": ProviderKind.TRAINING_BODY,
        "country": "Italie",
        "city": "Rovigo",
    },
    {
        "slug": "organisme-pro-exemple",
        "name": "Organisme de formation professionnelle (exemple)",
        "kind": ProviderKind.TRAINING_BODY,
        "country": "Maroc",
        "city": "Casablanca",
    },
    {
        "slug": "universite-partenaire-exemple",
        "name": "Université partenaire (exemple)",
        "kind": ProviderKind.UNIVERSITY,
        "country": "Italie",
        "city": "Padoue",
    },
    {
        "slug": "equipe-projet",
        "name": "Équipe du projet Italy Legal Entry",
        "kind": ProviderKind.PROJECT,
        "country": "Italie",
        "city": "",
    },
)

COMPETENCES = (
    ("comprendre-italien-a1", "Comprendre des échanges simples en italien", CompetenceArea.LANGUAGE),
    ("echanger-italien-a2", "Échanger sur des situations de travail en italien", CompetenceArea.LANGUAGE),
    ("identifier-risques", "Identifier les risques d’un poste de travail", CompetenceArea.SAFETY),
    ("connaitre-ses-droits", "Connaître ses droits et ses devoirs au travail", CompetenceArea.CIVIC),
    ("conduire-ses-demarches", "Conduire ses démarches administratives", CompetenceArea.CIVIC),
    ("hygiene-alimentaire", "Appliquer les règles d’hygiène alimentaire", CompetenceArea.TECHNICAL),
    ("travailler-en-equipe", "Travailler dans une équipe organisée", CompetenceArea.WORKPLACE),
)

COURSES = (
    {
        "slug": "italien-a1",
        "title": "Italien A1 — premiers échanges",
        "summary": "Comprendre et produire des énoncés simples de la vie quotidienne et du travail.",
        "description": (
            "Un premier parcours de langue italienne, pensé pour une personne qui part de zéro. "
            "Les séances alternent écoute, prise de parole et écrits courts. Le cours atteste la "
            "participation aux séances ; il ne délivre aucun titre et ne certifie aucun niveau "
            "officiel."
        ),
        "course_type": CourseType.ITALIAN_LANGUAGE,
        "provider": "centre-langue-exemple",
        "language": "it",
        "course_format": CourseFormat.BLENDED,
        "duration_hours": 60,
        "modules": (
            ("Se présenter et présenter quelqu’un", ModuleKind.LESSON, 90),
            ("Les lieux du quotidien : demander et comprendre un chemin", ModuleKind.LESSON, 90),
            ("Le vocabulaire du travail : outils, gestes, consignes", ModuleKind.LESSON, 120),
            ("Atelier : un échange au guichet", ModuleKind.PRACTICE, 90),
            ("Révision et auto-évaluation", ModuleKind.REVIEW, 60),
        ),
        "materials": (
            ("Livret de séances A1", MaterialKind.DOCUMENT, "Centre de langue italienne (exemple)", "Livret v1"),
            ("Enregistrements des dialogues", MaterialKind.RECORDING, "", ""),
        ),
        "competences": (
            ("comprendre-italien-a1", CompetenceLevel.BASIC, "Comprendre une consigne simple et y répondre."),
        ),
    },
    {
        "slug": "droits-et-devoirs",
        "title": "Droits et devoirs de la personne qui travaille en Italie",
        "summary": "Ce que dit le contrat, ce que garantit la loi, à qui s’adresser en cas de difficulté.",
        "description": (
            "Le cours présente le cadre général : contrat, rémunération, temps de travail, congés, "
            "représentation, voies de recours. Il ne remplace ni un conseil juridique individuel ni "
            "l’examen d’une situation particulière par un professionnel."
        ),
        "course_type": CourseType.RIGHTS_AND_DUTIES,
        "provider": "equipe-projet",
        "language": "fr",
        "course_format": CourseFormat.ONLINE,
        "duration_hours": 12,
        "modules": (
            ("Le contrat de travail : ce qu’il contient", ModuleKind.LESSON, 90),
            ("Temps de travail, repos, congés", ModuleKind.LESSON, 90),
            ("Rémunération et fiche de paie", ModuleKind.LESSON, 90),
            ("Que faire en cas de difficulté : interlocuteurs et recours", ModuleKind.LESSON, 90),
        ),
        "materials": (
            (
                "Repères sur le contrat de travail",
                MaterialKind.READING,
                "Portail institutionnel italien du travail",
                "Fiche d’information générale",
            ),
        ),
        "competences": (
            ("connaitre-ses-droits", CompetenceLevel.INTERMEDIATE, "Lire un contrat et repérer ce qui manque."),
        ),
    },
    {
        "slug": "education-civique",
        "title": "Éducation civique : institutions et vie quotidienne",
        "summary": "Comment sont organisées les institutions, et où s’adresser pour quelle démarche.",
        "description": (
            "Communes, régions, État : qui fait quoi, et quelle administration traite quelle demande. "
            "Le cours donne des repères ; il ne traite aucun dossier individuel."
        ),
        "course_type": CourseType.CIVIC_EDUCATION,
        "provider": "universite-partenaire-exemple",
        "language": "it",
        "course_format": CourseFormat.ONLINE,
        "duration_hours": 10,
        "modules": (
            ("L’organisation des institutions", ModuleKind.LESSON, 90),
            ("Les administrations du quotidien", ModuleKind.LESSON, 90),
            ("Lecture : une démarche, étape par étape", ModuleKind.READING, 60),
        ),
        "materials": (),
        "competences": (("conduire-ses-demarches", CompetenceLevel.BASIC, "Identifier l’administration compétente."),),
    },
    {
        "slug": "securite-au-travail",
        "title": "Sécurité au travail — repères généraux",
        "summary": "Reconnaître les risques, comprendre les consignes, savoir à qui signaler.",
        "description": (
            "Repères généraux de prévention : risques courants, équipements, signalisation, conduite "
            "à tenir. Le cours ne remplace pas la formation obligatoire que l’employeur doit "
            "dispenser, qui relève de lui seul."
        ),
        "course_type": CourseType.WORKPLACE_SAFETY,
        "provider": "organisme-pro-exemple",
        "language": "fr",
        "course_format": CourseFormat.BLENDED,
        "duration_hours": 8,
        "access_note": "Ce cours ne remplace pas la formation obligatoire dispensée par l’employeur.",
        "modules": (
            ("Les risques les plus fréquents", ModuleKind.LESSON, 90),
            ("Équipements de protection et signalisation", ModuleKind.LESSON, 90),
            ("Atelier : repérer les risques d’un poste", ModuleKind.PRACTICE, 120),
        ),
        "materials": (
            ("Affiches de signalisation commentées", MaterialKind.DOCUMENT, "Organisme de formation (exemple)", ""),
        ),
        "competences": (
            ("identifier-risques", CompetenceLevel.INTERMEDIATE, "Repérer et signaler un risque sur son poste."),
        ),
    },
    {
        "slug": "culture-du-travail",
        "title": "Culture du travail et organisation de l’entreprise",
        "summary": "Horaires, hiérarchie, réunions, écrits professionnels : les usages et leurs raisons.",
        "description": (
            "Un parcours court sur les usages du travail en Italie et sur ce qui, dans une "
            "organisation, est attendu sans être toujours dit."
        ),
        "course_type": CourseType.WORK_CULTURE,
        "provider": "equipe-projet",
        "language": "fr",
        "course_format": CourseFormat.ONLINE,
        "duration_hours": 6,
        "modules": (
            ("Le temps : horaires, ponctualité, absences", ModuleKind.LESSON, 60),
            ("L’équipe : rôles, consignes, retours", ModuleKind.LESSON, 60),
            ("Écrire au travail : messages courts et comptes rendus", ModuleKind.PRACTICE, 90),
        ),
        "materials": (),
        "competences": (
            ("travailler-en-equipe", CompetenceLevel.INTERMEDIATE, "Rendre compte de son travail à son équipe."),
        ),
    },
    {
        "slug": "metiers-agroalimentaire",
        "title": "Fondamentaux des métiers de l’agroalimentaire",
        "summary": "Hygiène, chaîne du froid, traçabilité et gestes techniques de base.",
        "description": (
            "Un parcours technique d’initiation, construit à partir des besoins de compétences "
            "recensés sur le territoire. Le suivi du cours atteste une participation ; il ne vaut "
            "ni habilitation ni qualification reconnue."
        ),
        "course_type": CourseType.PROFESSIONAL_TRAINING,
        "provider": "organisme-pro-exemple",
        "language": "fr",
        "course_format": CourseFormat.IN_PERSON,
        "duration_hours": 40,
        "modules": (
            ("Hygiène et règles de base", ModuleKind.LESSON, 120),
            ("La chaîne du froid", ModuleKind.LESSON, 120),
            ("Traçabilité et étiquetage", ModuleKind.LESSON, 120),
            ("Atelier technique encadré", ModuleKind.PRACTICE, 180),
            ("Révision", ModuleKind.REVIEW, 60),
        ),
        "materials": (
            ("Fiches d’hygiène en atelier", MaterialKind.DOCUMENT, "Organisme de formation (exemple)", "Fiches v2"),
            ("Exercices de traçabilité", MaterialKind.EXERCISE, "", ""),
        ),
        "competences": (
            ("hygiene-alimentaire", CompetenceLevel.INTERMEDIATE, "Appliquer un protocole d’hygiène en atelier."),
            ("identifier-risques", CompetenceLevel.BASIC, "Reconnaître un risque en atelier."),
        ),
    },
    {
        "slug": "preparation-au-depart",
        "title": "Préparation au départ : démarches, arrivée, premiers jours",
        "summary": "Ce qu’il faut préparer avant de partir et ce qui attend à l’arrivée.",
        "description": (
            "Un parcours d’orientation pratique : documents à rassembler, déroulé de l’arrivée, "
            "premières démarches, interlocuteurs. Le cours n’engage aucune autorité et ne promet "
            "aucun résultat."
        ),
        "course_type": CourseType.PRE_DEPARTURE,
        "provider": "equipe-projet",
        "language": "fr",
        "course_format": CourseFormat.ONLINE,
        "duration_hours": 6,
        "modules": (
            ("Rassembler ses documents", ModuleKind.LESSON, 60),
            ("L’arrivée : les premiers jours", ModuleKind.LESSON, 60),
            ("Lecture : à qui s’adresser, pour quoi", ModuleKind.READING, 45),
        ),
        "materials": (),
        "competences": (
            ("conduire-ses-demarches", CompetenceLevel.INTERMEDIATE, "Préparer un dossier complet avant le départ."),
        ),
    },
    {
        "slug": "italien-a2-preparation",
        "title": "Italien A2 — en préparation",
        "summary": "Suite du parcours de langue. Le contenu est en cours de relecture pédagogique.",
        "description": "",
        "course_type": CourseType.ITALIAN_LANGUAGE,
        "provider": "centre-langue-exemple",
        "language": "it",
        "course_format": CourseFormat.BLENDED,
        "duration_hours": 60,
        "status": CourseStatus.DRAFT,
        "modules": (("Séance d’ouverture", ModuleKind.LESSON, 90),),
        "materials": (),
        "competences": (),
    },
)


@register_seed("academy.catalogue", order=70)
def seed_catalogue() -> str:
    providers: dict[str, TrainingProvider] = {}
    for row in PROVIDERS:
        provider, _created = TrainingProvider.objects.get_or_create(
            slug=row["slug"],
            defaults={
                "name": row["name"],
                "kind": row["kind"],
                "country": row["country"],
                "city": row["city"],
                "note": "" if row["kind"] == ProviderKind.PROJECT else DEMO_NOTE,
            },
        )
        providers[row["slug"]] = provider

    competences: dict[str, Competence] = {}
    for code, label, area in COMPETENCES:
        competence, _created = Competence.objects.get_or_create(code=code, defaults={"label": label, "area": area})
        competences[code] = competence

    created_courses = 0
    for spec in COURSES:
        status = spec.get("status", CourseStatus.PUBLISHED)
        course, created = Course.objects.get_or_create(
            slug=spec["slug"],
            defaults={
                "title": spec["title"],
                "summary": spec["summary"],
                "description": spec["description"],
                "course_type": spec["course_type"],
                "provider": providers[spec["provider"]],
                "language": spec["language"],
                "course_format": spec["course_format"],
                "duration_hours": spec["duration_hours"],
                "access_note": spec.get("access_note", ""),
                "status": status,
                "published_at": timezone.now() if status == CourseStatus.PUBLISHED else None,
            },
        )
        created_courses += int(created)
        if not created:
            continue
        for order, (title, kind, minutes) in enumerate(spec["modules"], start=1):
            CourseModule.objects.get_or_create(
                course=course,
                order=order,
                defaults={"title": title, "kind": kind, "duration_minutes": minutes},
            )
        for order, (title, kind, source_title, source_ref) in enumerate(spec["materials"], start=1):
            CourseMaterial.objects.get_or_create(
                course=course,
                title=title,
                defaults={"order": order, "kind": kind, "source_title": source_title, "source_ref": source_ref},
            )
        for code, level, outcome in spec["competences"]:
            CourseCompetence.objects.get_or_create(
                course=course,
                competence=competences[code],
                defaults={"level_reached": level, "expected_outcome": outcome},
            )
    return f"{created_courses} courses created ({Course.objects.published().count()} published in catalogue)"


DEMO_PLAN_TITLE = "Parcours de formation recommandé — agroalimentaire"
DEMO_ACCOUNT = "qa-person@example.test"


@register_seed("academy.demo_plan", order=71)
def seed_demo_plan() -> str:
    """
    One training plan, for the reserved QA account only.

    The guard is the point: a seed runs on every deploy, and a training plan is personal data. The
    ``@example.test`` domain is reserved by RFC 2606 and can never belong to a real person, so this
    seed cannot write a plan for anybody real even if it runs in production by accident.
    """
    if not demonstration_data_allowed():
        # A training plan belongs to a person. Inventing one is inventing a person's record.
        return "academy demonstration plan skipped (synthetic data is not allowed here)"
    if not DEMO_ACCOUNT.endswith("@example.test"):  # pragma: no cover - defensive
        return "skipped: demo account is not in the reserved domain"
    person = get_user_model().objects.filter(email=DEMO_ACCOUNT).first()
    if person is None:
        return "skipped: no reserved demonstration account on this instance"

    plan, created = TrainingPlan.objects.get_or_create(
        person=person,
        title=DEMO_PLAN_TITLE,
        defaults={
            "origin": PlanOrigin.COMPANY_NEED,
            "origin_reference": "Besoin territorial FB-2026-014 (exemple)",
            "status": PlanStatus.ACTIVE,
            "note": (
                "Ce plan est un parcours conseillé, établi à partir d’un besoin de compétences "
                "exprimé sur le territoire. Il ne conditionne en rien l’accès aux cours : tous les "
                "cours qu’il cite sont ouverts à toute personne inscrite, sans sélection préalable."
            ),
        },
    )
    if not created:
        return "demonstration plan already present"

    courses = {
        course.slug: course
        for course in Course.objects.filter(slug__in=("metiers-agroalimentaire", "securite-au-travail", "italien-a1"))
    }
    competences = {row.code: row for row in Competence.objects.all()}
    ordered = (
        (
            "italien-a1",
            "La communication en atelier suppose des échanges simples en italien.",
            "Comprendre une consigne orale.",
        ),
        (
            "securite-au-travail",
            "Le poste comporte des risques courants à reconnaître.",
            "Repérer et signaler un risque.",
        ),
        ("metiers-agroalimentaire", "Cœur technique du besoin recensé.", "Appliquer un protocole d’hygiène."),
    )
    for order, (slug, rationale, outcome) in enumerate(ordered, start=1):
        course = courses.get(slug)
        if course is not None:
            TrainingPlanItem.objects.get_or_create(
                plan=plan,
                course=course,
                defaults={"order": order, "rationale": rationale, "expected_outcome": outcome},
            )

    gap_rows = (
        (
            "comprendre-italien-a1",
            CompetenceLevel.BASIC,
            CompetenceLevel.NONE,
            "italien-a1",
            "Comprendre une consigne simple.",
        ),
        (
            "identifier-risques",
            CompetenceLevel.INTERMEDIATE,
            CompetenceLevel.BASIC,
            "securite-au-travail",
            "Signaler un risque à son responsable.",
        ),
        (
            "hygiene-alimentaire",
            CompetenceLevel.INTERMEDIATE,
            CompetenceLevel.NONE,
            "metiers-agroalimentaire",
            "Appliquer un protocole d’hygiène en atelier.",
        ),
        (
            "travailler-en-equipe",
            CompetenceLevel.BASIC,
            CompetenceLevel.BASIC,
            "",
            "Aucun écart : compétence déjà acquise.",
        ),
    )
    for order, (code, required, current, course_slug, outcome) in enumerate(gap_rows, start=1):
        competence = competences.get(code)
        if competence is None:
            continue
        SkillGapLine.objects.get_or_create(
            plan=plan,
            competence=competence,
            defaults={
                "order": order,
                "required_level": required,
                "current_level": current,
                "course": courses.get(course_slug),
                "expected_outcome": outcome,
                "source_note": "Besoin territorial FB-2026-014 (exemple)",
            },
        )
    return "demonstration training plan created for the reserved QA account"
