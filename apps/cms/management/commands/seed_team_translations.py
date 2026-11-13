"""
``manage.py seed_team_translations`` — the team's translation rows for the reference data the seeds create in French
only
(V5.24 §4–§5, the Arabic completeness audit's W2; lane AR): the pathway sheets' five generic stages, the orientation
questionnaire, the FAQ's general category — in Arabic, Italian and English (``cms.team_translations``).

Idempotent: one ``get_or_create`` per ``(master, language)``, defaults on creation only — a row an editor changed is
never
overwritten (``core.seeds``: «never overwrite editorial changes to non-locked fields»). Registered as the seed
``cms.team_translations`` (order 99, after the masters' seeds), so ``seed_all`` — the preview's and the tests' — loads
it on
every environment.
"""

from __future__ import annotations

from django.core.management.base import BaseCommand

from cms import team_translations as data
from cms.models import TranslationStatus


def _ensure(model, master, language: str, **fields) -> bool:
    _row, created = model.objects.get_or_create(
        master=master,
        language=language,
        defaults={**fields, "status": TranslationStatus.PUBLISHED, "source": data.SOURCE},
    )
    return created


def seed() -> str:
    """Load the rows; returns a one-line summary («n created, m present»)."""
    from faq.models import FAQCategory, FAQCategoryTranslation
    from orientation.models import (
        ChecklistItem,
        ChecklistItemTranslation,
        Choice,
        ChoiceTranslation,
        Outcome,
        OutcomeTranslation,
        Question,
        QuestionTranslation,
    )
    from pathways.models import PathwayStep, PathwayStepTranslation

    created = present = 0

    def count(made: bool) -> None:
        nonlocal created, present
        created += int(made)
        present += int(not made)

    for row in data.PATHWAY_STEPS:
        for step in PathwayStep.objects.filter(order=row["order"], title_fr=row["fr"]):
            for language in data.LANGUAGES:
                count(_ensure(PathwayStepTranslation, step, language, title=row[language], text=""))
    for row in data.FAQ_CATEGORIES:
        for category in FAQCategory.objects.filter(slug=row["slug"]):
            for language in data.LANGUAGES:
                count(_ensure(FAQCategoryTranslation, category, language, name=row[language]))
    for row in data.QUESTIONS:
        for question in Question.objects.filter(key=row["key"]):
            for language in data.LANGUAGES:
                texts = row[language]
                count(_ensure(QuestionTranslation, question, language, text=texts["text"], help=texts["help"]))
    for row in data.CHOICES:
        for choice in Choice.objects.filter(question__key=row["question"], key=row["key"]):
            for language in data.LANGUAGES:
                count(_ensure(ChoiceTranslation, choice, language, label=row[language]))
    for row in data.OUTCOMES:
        for outcome in Outcome.objects.filter(pathway_key=row["pathway_key"]):
            for language in data.LANGUAGES:
                title = row[language]["title"]
                explanation = data.outcome_explanation(row, language)
                count(_ensure(OutcomeTranslation, outcome, language, title=title, explanation=explanation))
    for row in data.CHECKLIST_ITEMS:
        for item in ChecklistItem.objects.filter(text_fr=row["fr"]):
            for language in data.LANGUAGES:
                count(_ensure(ChecklistItemTranslation, item, language, text=row[language]))
    return f"{created} team translation row(s) created, {present} already present"


class Command(BaseCommand):
    help = "Load the team's it/en/ar translation rows for the seeded reference data (idempotent; V5.24 W2)."

    def handle(self, *args, **options):
        self.stdout.write(seed())
