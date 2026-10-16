"""
The initial legal ruleset.

Provenance, stated plainly because it governs what may be activated:

* The **requirements** come from the previous Italy Legal Entry platform, whose four visa types carry
  genuinely expert document lists (previous-platform audit, part 2 §4, private register — passport
  valid three months beyond the return date with two blank pages, €30 000 insurance, 35×45 mm
  photographs). That is real domain work and it is imported rather than rewritten.
* The **sources** do not come from there, because there are none: the audit records that «Decreto
  Flussi» appears in a sentence of prose, never as a reference. They are supplied here.

So each rule below is one of two kinds, and the difference decides whether it binds anyone:

``ACTIVE`` — the link between the requirement and the provision is not in doubt: the Testo Unico puts
the *nulla osta* for subordinate work at art. 22, family reunification at art. 29 and the annual
quota decree at art. 3(4); the Schengen Borders Code and the Visa Code fix the travel-document
conditions. These enter into force.

``LEGAL_REVIEW`` — the requirement is certainly real, but the precise provision behind it, or the
figure it names, is something a legal referent must confirm. The €30 000 insurance minimum is the
clearest case: the Visa Code states it for SHORT stays, and the previous platform applied it to a
long-stay work file. That may well be right, and it is not for this build to decide. Rules of this
kind are inert: the engine evaluates only what is ACTIVE, so an unreviewed rule cannot reach
anybody's screen. Seeding them
anyway is deliberate — the review queue is where they belong, and an empty queue would misrepresent
how much of this is still to do.

Two provisions are kept out of the seed entirely:

* **art. 23 D.Lgs. 286/1998** (training in the country of origin). CONFLICT_REGISTER CR-07 settles
  it: the article may be cited as a norm of the system, never as the project's own title to operate,
  and any such content passes legal review first. It is not seeded.
* Anything expressing a **timescale or a likelihood of success**. The engine says what a route
  requires; it never says how long it takes or how it will end.
"""

from __future__ import annotations

import datetime as dt

from core.seeds import register_seed
from rules.models import LegalRule, LegalSource, ReviewStatus, RuleEffect, RuleProvenance

#: Provenance note carried by every seeded source. It is not decoration: the legal referent needs to
#: know which references were supplied by the build and therefore still owe a consultation date.
SEED_NOTE = (
    "Riferimento inserito dal seed iniziale del rule engine. "
    "Il referente giuridico deve verificarlo alla fonte ufficiale e registrare la data di consultazione."
)

# `jurisdiction` defaults to IT, and five of these fifteen sources are not Italian: two articles of
# the Visa Code, the Schengen Borders Code, and the Blue Card and student/researcher directives.
# They were all recorded as IT, which matters more than it looks — a rule that rests on a directive
# changes when Brussels moves, not when Rome does, and whoever re-reads the ruleset in a year needs
# to see which of the two they are watching. Found by `rules_pending_review`, which prints the
# jurisdiction next to the reference and made five EU regulations read as Italian law.

#: The fields of a seeded source that the build keeps asserting on every run. The back-office does not
#: offer them (rules/admin.py), so no editorial change can be lost, and the seed has had to correct one
#: before (the five EU sources above). Every other field belongs to the legal referent once the source
#: exists — see `_complete_source`.
BUILD_OWNED_SOURCE_FIELDS = frozenset({"jurisdiction"})

SOURCES: tuple[dict, ...] = (
    {
        "key": "tui-286-1998",
        "title_fr": "Texte unique sur l’immigration",
        "title_it": "Testo unico delle disposizioni concernenti la disciplina dell’immigrazione",
        "reference": "D.Lgs. 25 luglio 1998, n. 286",
        "authority": "Repubblica Italiana",
    },
    {
        "key": "tui-286-1998-art-3-4",
        "title_fr": "Décret fixant les quotas annuels d’entrée",
        "title_it": "Decreto di programmazione dei flussi di ingresso",
        "reference": "D.Lgs. 286/1998, art. 3, comma 4",
        "authority": "Repubblica Italiana",
    },
    {
        "key": "tui-286-1998-art-22",
        "title_fr": "Travail salarié à durée déterminée et indéterminée",
        "title_it": "Lavoro subordinato a tempo determinato e indeterminato",
        "reference": "D.Lgs. 286/1998, art. 22",
        "authority": "Repubblica Italiana",
    },
    {
        "key": "tui-286-1998-art-24",
        "title_fr": "Travail saisonnier",
        "title_it": "Lavoro stagionale",
        "reference": "D.Lgs. 286/1998, art. 24",
        "authority": "Repubblica Italiana",
    },
    {
        "key": "tui-286-1998-art-26",
        "title_fr": "Entrée et séjour pour travail indépendant",
        "title_it": "Ingresso e soggiorno per lavoro autonomo",
        "reference": "D.Lgs. 286/1998, art. 26",
        "authority": "Repubblica Italiana",
    },
    {
        "key": "tui-286-1998-art-27-ter",
        "title_fr": "Entrée et séjour pour recherche scientifique",
        "title_it": "Ingresso e soggiorno per ricerca",
        "reference": "D.Lgs. 286/1998, art. 27-ter",
        "authority": "Repubblica Italiana",
    },
    {
        "key": "tui-286-1998-art-27-quater",
        "title_fr": "Carte bleue européenne — travailleurs hautement qualifiés",
        "title_it": "Carta blu UE — lavoratori altamente qualificati",
        "reference": "D.Lgs. 286/1998, art. 27-quater",
        "authority": "Repubblica Italiana",
    },
    {
        "key": "tui-286-1998-art-29",
        "title_fr": "Regroupement familial",
        "title_it": "Ricongiungimento familiare",
        "reference": "D.Lgs. 286/1998, art. 29",
        "authority": "Repubblica Italiana",
    },
    {
        "key": "tui-286-1998-art-39",
        "title_fr": "Accès à l’enseignement universitaire",
        "title_it": "Accesso ai corsi universitari",
        "reference": "D.Lgs. 286/1998, art. 39",
        "authority": "Repubblica Italiana",
    },
    {
        "key": "dpr-394-1999",
        "title_fr": "Règlement d’application du texte unique",
        "title_it": "Regolamento di attuazione del testo unico",
        "reference": "D.P.R. 31 agosto 1999, n. 394",
        "authority": "Repubblica Italiana",
    },
    {
        "key": "visa-code-810-2009-art-15",
        "jurisdiction": "EU",
        "title_fr": "Assurance médicale de voyage",
        "title_it": "Assicurazione sanitaria di viaggio",
        "reference": "Reg. (CE) n. 810/2009 (codice dei visti), art. 15",
        "authority": "Unione europea",
    },
    {
        "key": "visa-code-810-2009-art-12",
        "jurisdiction": "EU",
        "title_fr": "Document de voyage",
        "title_it": "Documento di viaggio",
        "reference": "Reg. (CE) n. 810/2009 (codice dei visti), art. 12",
        "authority": "Unione europea",
    },
    {
        "key": "schengen-borders-2016-399-art-6",
        "jurisdiction": "EU",
        "title_fr": "Conditions d’entrée pour un séjour de courte durée",
        "title_it": "Condizioni d’ingresso per soggiorni di breve durata",
        "reference": "Reg. (UE) 2016/399 (codice frontiere Schengen), art. 6",
        "authority": "Unione europea",
    },
    {
        "key": "directive-2021-1883",
        "jurisdiction": "EU",
        "title_fr": "Directive « carte bleue européenne »",
        "title_it": "Direttiva «carta blu UE»",
        "reference": "Direttiva (UE) 2021/1883",
        "authority": "Unione europea",
    },
    {
        "key": "directive-2016-801",
        "jurisdiction": "EU",
        "title_fr": "Directive « étudiants et chercheurs »",
        "title_it": "Direttiva «studenti e ricercatori»",
        "reference": "Direttiva (UE) 2016/801",
        "authority": "Unione europea",
    },
)

#: Values of ``cases.ResponsibleActor``. Repeated as literals so the seed does not import the case
#: app; ``LegalRule.clean()`` checks them against the real enumeration, so a typo here fails loudly.
PERSON = "person"
AUTHORITY = "authority"
COMPANY = "company"
PROJECT_TEAM = "project_team"

IN_FORCE_FROM = dt.date(2026, 1, 1)


def _rule(**kwargs) -> dict:
    kwargs.setdefault("jurisdiction", "IT")
    kwargs.setdefault("valid_from", IN_FORCE_FROM)
    kwargs.setdefault("version", 1)
    kwargs.setdefault("responsible_actor", PERSON)
    kwargs.setdefault("requirement_fr", "")
    return kwargs


#: Rules that enter into force. Each one names a provision that says what the rule says.
ACTIVE_RULES: tuple[dict, ...] = (
    # ---- Cross-cutting: the travel document ------------------------------------------------
    _rule(
        rule_id="R-DOC-001",
        pathway="salaried_work",
        condition={},
        effect=RuleEffect.MISSING_REQUIREMENT,
        message_key="rules.doc.passport",
        message_fr="Un document de voyage en cours de validité est exigé.",
        requirement_fr=(
            "Passeport valable au moins trois mois après la date prévue de sortie de l’espace "
            "Schengen, délivré depuis moins de dix ans, avec au moins deux pages vierges."
        ),
        sources=("visa-code-810-2009-art-12", "schengen-borders-2016-399-art-6"),
    ),
    # ---- Salaried work ---------------------------------------------------------------------
    _rule(
        rule_id="R-WORK-001",
        pathway="salaried_work",
        condition={},
        effect=RuleEffect.WARNING,
        message_key="rules.work.quota",
        message_fr=(
            "L’entrée pour travail salarié s’inscrit dans les quotas fixés périodiquement par décret. "
            "Les demandes suivent les délais officiels publiés par les autorités."
        ),
        responsible_actor=AUTHORITY,
        sources=("tui-286-1998-art-3-4", "tui-286-1998-art-22"),
    ),
    _rule(
        rule_id="R-WORK-002",
        pathway="salaried_work",
        condition={},
        effect=RuleEffect.MISSING_REQUIREMENT,
        message_key="rules.work.nulla_osta",
        message_fr="L’autorisation de travail (nulla osta) est délivrée par le guichet unique pour l’immigration.",
        requirement_fr=(
            "Nulla osta al lavoro délivré par le Sportello Unico per l’immigrazione compétent, "
            "demandé par l’employeur en Italie."
        ),
        responsible_actor=COMPANY,
        sources=("tui-286-1998-art-22", "dpr-394-1999"),
    ),
    _rule(
        rule_id="R-WORK-003",
        pathway="salaried_work",
        condition={"field": "has_job_offer", "op": "is_false"},
        effect=RuleEffect.MISSING_REQUIREMENT,
        message_key="rules.work.offer",
        message_fr="La procédure pour travail salarié suppose un employeur identifié en Italie.",
        requirement_fr=(
            "Proposition de contrat de travail d’un employeur établi en Italie. Sans employeur "
            "demandeur, la procédure de nulla osta ne peut pas être engagée."
        ),
        responsible_actor=COMPANY,
        sources=("tui-286-1998-art-22",),
    ),
    # ---- Family reunification --------------------------------------------------------------
    _rule(
        rule_id="R-FAM-001",
        pathway="family_reunification",
        condition={},
        effect=RuleEffect.MISSING_REQUIREMENT,
        message_key="rules.family.nulla_osta",
        message_fr="Le regroupement familial est engagé par la personne déjà présente régulièrement en Italie.",
        requirement_fr=(
            "Nulla osta al ricongiungimento familiare demandé au Sportello Unico per l’immigrazione "
            "par le membre de famille résidant régulièrement en Italie."
        ),
        responsible_actor=AUTHORITY,
        sources=("tui-286-1998-art-29", "dpr-394-1999"),
    ),
    _rule(
        rule_id="R-FAM-002",
        pathway="family_reunification",
        condition={},
        effect=RuleEffect.MISSING_REQUIREMENT,
        message_key="rules.family.accommodation",
        message_fr="Un logement et des ressources conformes aux seuils fixés par la loi sont exigés.",
        requirement_fr=(
            "Justificatif de logement et de ressources du demandeur, dans les conditions prévues par "
            "l’art. 29 du texte unique. Les seuils sont fixés par la réglementation en vigueur."
        ),
        sources=("tui-286-1998-art-29",),
    ),
    # ---- Study ------------------------------------------------------------------------------
    _rule(
        rule_id="R-STU-001",
        pathway="study_and_training_in_italy",
        condition={},
        effect=RuleEffect.MISSING_REQUIREMENT,
        message_key="rules.study.admission",
        message_fr="L’accès aux cours universitaires suppose une admission auprès de l’établissement.",
        requirement_fr=(
            "Document d’admission ou de préinscription délivré par l’établissement d’enseignement "
            "italien, selon la procédure annuelle publiée par les autorités."
        ),
        sources=("tui-286-1998-art-39", "directive-2016-801"),
    ),
    # ---- EU Blue Card ------------------------------------------------------------------------
    _rule(
        rule_id="R-BLUE-001",
        pathway="skilled_work_eu_blue_card",
        condition={},
        effect=RuleEffect.MISSING_REQUIREMENT,
        message_key="rules.blue.offer",
        message_fr="La carte bleue européenne suppose un contrat ou une offre ferme d’emploi hautement qualifié.",
        requirement_fr=(
            "Contrat de travail ou offre ferme portant sur un emploi hautement qualifié, dans les "
            "conditions prévues par l’art. 27-quater du texte unique."
        ),
        responsible_actor=COMPANY,
        sources=("tui-286-1998-art-27-quater", "directive-2021-1883"),
    ),
    # ---- Research ----------------------------------------------------------------------------
    _rule(
        rule_id="R-RES-001",
        pathway="scientific_research",
        condition={},
        effect=RuleEffect.MISSING_REQUIREMENT,
        message_key="rules.research.host",
        message_fr="L’entrée pour recherche suppose une convention d’accueil avec un organisme agréé.",
        requirement_fr=(
            "Convention d’accueil signée avec un organisme de recherche inscrit sur la liste prévue "
            "par la réglementation."
        ),
        responsible_actor=AUTHORITY,
        sources=("tui-286-1998-art-27-ter", "directive-2016-801"),
    ),
    # ---- Self-employment ---------------------------------------------------------------------
    _rule(
        rule_id="R-SELF-001",
        pathway="self_employment_entrepreneurship",
        condition={},
        effect=RuleEffect.MISSING_REQUIREMENT,
        message_key="rules.self.nulla_osta",
        message_fr="Le travail indépendant suppose une attestation des conditions requises pour l’activité.",
        requirement_fr=(
            "Attestation délivrée par l’autorité compétente confirmant que les conditions requises "
            "pour exercer l’activité indépendante envisagée sont réunies."
        ),
        responsible_actor=AUTHORITY,
        sources=("tui-286-1998-art-26", "dpr-394-1999"),
    ),
    # ---- Seasonal and other regular routes ----------------------------------------------------
    _rule(
        rule_id="R-OTH-001",
        pathway="other_regular_routes",
        condition={},
        effect=RuleEffect.REVIEW_REQUIRED,
        message_key="rules.other.individual",
        message_fr=(
            "Les hypothèses regroupées ici (travail saisonnier et autres voies prévues par la "
            "réglementation) demandent un examen au cas par cas."
        ),
        responsible_actor=PROJECT_TEAM,
        sources=("tui-286-1998-art-24", "tui-286-1998"),
    ),
)

#: Rules that are certainly real requirements but whose precise provision, or whose figure, a legal
#: referent must confirm before they bind anyone. They sit in the review queue and change nothing.
REVIEW_RULES: tuple[dict, ...] = (
    _rule(
        rule_id="R-DOC-002",
        pathway="salaried_work",
        condition={},
        effect=RuleEffect.MISSING_REQUIREMENT,
        message_key="rules.doc.insurance",
        message_fr="Une assurance médicale de voyage est exigée.",
        requirement_fr=(
            "Assurance médicale de voyage couvrant les frais de rapatriement et les soins urgents, "
            "à hauteur d’au moins 30 000 €."
        ),
        sources=("visa-code-810-2009-art-15",),
        note=(
            "Le seuil de 30 000 € est celui du code des visas pour les séjours de courte durée. "
            "Son application au parcours « travail salarié » (séjour de longue durée) doit être "
            "confirmée par le référent juridique avant mise en vigueur."
        ),
    ),
    _rule(
        rule_id="R-STU-002",
        pathway="study_and_training_in_italy",
        condition={},
        effect=RuleEffect.MISSING_REQUIREMENT,
        message_key="rules.study.means",
        message_fr="Des moyens de subsistance suffisants pour la durée des études sont exigés.",
        requirement_fr=(
            "Justificatif de moyens de subsistance pour la durée du séjour. Le montant est fixé "
            "chaque année par les autorités."
        ),
        sources=("tui-286-1998-art-39",),
        note=(
            "La vecchia piattaforma indicava «circa 6 000 € l’anno con estratti conto degli ultimi "
            "tre mesi». L’importo è aggiornato periodicamente: va confermato e datato prima di "
            "entrare in vigore, altrimenti la regola invecchia senza che nessuno se ne accorga."
        ),
    ),
    _rule(
        rule_id="R-STU-003",
        pathway="study_and_training_in_italy",
        condition={},
        effect=RuleEffect.MISSING_REQUIREMENT,
        message_key="rules.study.qualification",
        message_fr="Le titre d’études étranger doit être accompagné des documents prévus par la procédure.",
        requirement_fr=(
            "Titre d’études traduit et légalisé, accompagné des documents demandés par "
            "l’établissement et par la représentation diplomatique."
        ),
        responsible_actor=AUTHORITY,
        sources=("tui-286-1998-art-39",),
        note=(
            "Formulation à valider : la plateforme n’a aucun rôle dans la reconnaissance des "
            "diplômes et ne doit pas donner à penser le contraire."
        ),
    ),
    _rule(
        rule_id="R-FAM-003",
        pathway="family_reunification",
        condition={},
        effect=RuleEffect.MISSING_REQUIREMENT,
        message_key="rules.family.civil_status",
        message_fr="Les actes d’état civil établissant le lien familial sont exigés.",
        requirement_fr=(
            "Actes d’état civil établissant le lien familial, traduits et légalisés selon la "
            "procédure applicable au pays d’origine."
        ),
        sources=("tui-286-1998-art-29",),
        note=(
            "La vecchia piattaforma esigeva un atto di matrimonio «di meno di sei mesi». "
            "Il termine va verificato: se non è previsto dalla norma, non deve essere richiesto."
        ),
    ),
    _rule(
        rule_id="R-TRAIN-001",
        pathway="training_in_origin_country",
        condition={},
        effect=RuleEffect.REVIEW_REQUIRED,
        message_key="rules.training.individual",
        message_fr=(
            "Les parcours de formation organisés avant le départ demandent un examen au cas par cas "
            "avec les acteurs compétents."
        ),
        responsible_actor=PROJECT_TEAM,
        sources=("tui-286-1998",),
        note=(
            "CONFLICT_REGISTER CR-07 : l’art. 23 du texte unique ne peut pas être cité comme titre "
            "du projet. Toute rédaction citant cette disposition passe par la revue juridique."
        ),
    ),
)


@register_seed("rules.legal_ruleset", order=45)
def seed() -> dict[str, int]:
    """
    Create the sources and the rules, idempotently. **Nothing is put in force.** A source or a rule that
    already exists keeps what staff made of it: rules are created only when missing, and an existing source
    is only completed where a field is empty (`_complete_source`).

    This used to seed eleven rules straight to ``ACTIVE`` so that the engine could be seen working
    before the legal review had happened, with ``approved_by`` left empty on purpose and a command
    that listed them. That was honest but it was the wrong shape: the rules bound people, the list
    was a thing somebody had to remember to read, and the database happily held a rule in force
    that nobody had approved.

    Now the seed writes candidates. A rule drafted from the norm starts at ``DRAFT``; content taken
    from the previous platform starts at ``LEGACY_CANDIDATE``. Neither is in force, so
    ``rules_in_force()`` returns nothing until a jurist has actually walked the chain.

    To see the engine work locally, ``manage.py rules_activate_demonstration`` does it explicitly,
    refuses to run where demonstration data is not allowed, and stamps every rule with an approver
    label that says in words that no jurist approved it.
    """
    counts = {"sources": 0, "drafted": 0, "legacy_candidates": 0}

    by_key: dict[str, LegalSource] = {}
    for spec in SOURCES:
        values = {k: v for k, v in spec.items() if k != "key"}
        source, created = LegalSource.objects.get_or_create(key=spec["key"], defaults={**values, "note": SEED_NOTE})
        if not created:
            _complete_source(source, values)
        by_key[source.key] = source
        counts["sources"] += int(created)

    for spec in ACTIVE_RULES:
        if _write(spec, by_key, ReviewStatus.DRAFT, RuleProvenance.DRAFTED_FROM_SOURCE):
            counts["drafted"] += 1

    for spec in REVIEW_RULES:
        if _write(spec, by_key, ReviewStatus.LEGACY_CANDIDATE, RuleProvenance.LEGACY_DERIVED):
            counts["legacy_candidates"] += 1

    return counts


def _complete_source(source: LegalSource, values: dict) -> list[str]:
    """
    Bring an existing source up to the seed WITHOUT undoing the legal referent's work.

    The referent corrects a source's titles, reference, authority and note in the back-office
    (rules/admin.py), and `seed_all` runs at every deployment. Until 12 October 2026 this seed wrote every
    seeded field back with `update_or_create`, so a corrected citation silently returned to the build's
    text at the next release (DevOps review, finding M9) — the one seed that broke the contract of
    core.seeds («never overwrite editorial changes»). Now only an EMPTY field is completed from the seed,
    and the build-owned fields (`BUILD_OWNED_SOURCE_FIELDS`) follow it. Returns the fields written.
    """
    changed = [
        name
        for name, value in values.items()
        if (
            getattr(source, name) != value if name in BUILD_OWNED_SOURCE_FIELDS else value and not getattr(source, name)
        )
    ]
    for name in changed:
        setattr(source, name, values[name])
    if changed:
        source.save(update_fields=[*changed, "updated_at"])
    return changed


def _write(spec: dict, by_key: dict[str, LegalSource], status: str, provenance: str) -> bool:
    payload = {k: v for k, v in spec.items() if k != "sources"}
    source_keys = spec.get("sources", ())
    rule, created = LegalRule.objects.get_or_create(
        rule_id=payload["rule_id"],
        version=payload["version"],
        defaults={**payload, "review_status": status, "provenance": provenance},
    )
    if created:
        rule.sources.set([by_key[key] for key in source_keys])
        # `approved_by`, `approved_by_label` and `approved_at` stay empty, and now the database
        # agrees: a check constraint refuses an approved or active rule whose approver label is
        # blank, so this cannot drift back by somebody writing the status column directly.
    return created
