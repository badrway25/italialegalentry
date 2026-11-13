# DPIA necessity assessment — art. 35 GDPR (V5.16 §8)

- Written 28 October 2026 by lane P2 (label `v516-p2-build`). This is a focused necessity assessment, not a DPIA.
- Conclusion corrected the same day by lane P3 (label `v517-p3-build`), directive V5.17 §3: «proceed on the
  assumption that a DPIA should be prepared unless the legal/privacy review produces a documented reasoned conclusion
  that it is not required. Do not merely write: "probably required".» The DPIA is in preparation:
  [`DPIA.md`](DPIA.md).
- Directive V5.16 §8: «perform a focused DPIA-necessity assessment before production. Do not claim that a DPIA is
  mandatory or unnecessary without the assessment. If required, it becomes a production gate.»
- References, to be checked by the legal review:
  - art. 35(1) and (3) GDPR;
  - the Garante's list of processing subject to a DPIA (provvedimento n. 467 of 11 October 2018, under art. 35(4));
  - the Article 29 Working Party guidelines on DPIA (WP248 rev.01), endorsed by the EDPB. They set nine criteria and
    say that processing meeting **two or more** will in most cases require a DPIA.

## 1. The processing assessed

| Processing | Where |
|---|---|
| **identity documents** and other pathway documents uploaded by the person | M-08, S-01/S-02 |
| **case files**: status history, checklists, deadlines, messages, assessments | M-07, M-09 |
| possible **special-category data** in uploads and free texts | [`SPECIAL_CATEGORY_AUDIT.md`](SPECIAL_CATEGORY_AUDIT.md) |
| **orientation and eligibility pre-assessments**: the questionnaire, the rule engine, `PathwayAssessment` | M-06, M-07 |
| **multiple institutional actors**: professionals, operators, authorised actors, training providers, companies (through identity disclosure), institutions | [`RECIPIENT_ROLES_MATRIX.md`](RECIPIENT_ROLES_MATRIX.md) |

## 2. The EDPB criteria (WP248)

| # | Criterion | Applied | Met? |
|---|---|---|---|
| 1 | Evaluation or scoring, including profiling and predicting | the orientation questionnaire and the rule engine evaluate a person's situation against the pathways' conditions; `PathwayAssessment` records an outcome per pathway. They are informational, never a decision (ANX §4), but they are an evaluation of personal aspects | **likely yes** |
| 2 | Automated decision with legal or similar significant effect | none: ANX §4; every administrative decision is the authorities'. The selection outcomes describe the process, not the person (`apps/selection/models.py:27-30`) | **no** |
| 3 | Systematic monitoring | follow-up of a case file over time; there is no observation of public spaces and no online tracking | **unclear**: depends on DPO_ASSESSMENT (b) |
| 4 | Sensitive data or data of a highly personal nature | identity documents of third-country nationals; their migration situation; possible art. 9 data in uploads and free text | **likely yes** |
| 5 | Data processed on a large scale | unknown before launch (the DPO assessment's facts 1, 2, 4) | **unknown** |
| 6 | Matching or combining datasets | the selection chain: a company's need, an authorised actor's mandate, the person's competences and evidence, the case file (`apps/selection/models.py:8`); the identity disclosure to a company | **likely yes** |
| 7 | Data concerning vulnerable data subjects | WP248 cites a power imbalance and names asylum seekers among others. Persons preparing a regular entry, dependent on documents and on the actors around them, plausibly fall in this class | **likely yes** |
| 8 | Innovative use or new technological solutions | none: no AI, no biometrics, no IoT. The rule engine is a deterministic, reviewed rule set | **no** |
| 9 | Processing that prevents data subjects from exercising a right or using a service | the pre-assessment does not refuse a service; the platform is not the gate to a visa | **no** |

## 3. The Garante's list (provv. 467/2018), items that touch this processing

- **Evaluation or scoring on a large scale** (item 1): relevant to the orientation and assessments **if** the scale is
  large → unknown.
- **Non-occasional processing of data of vulnerable persons** (item 6, which names asylum seekers among others):
  relevant if the data subjects are treated as vulnerable (criterion 7) → likely.
- **Large-scale exchange of data between different controllers by telematic means** (item 8): professionals,
  authorised actors, training providers and companies may be independent controllers (RECIPIENT_ROLES_MATRIX) → the
  scale decides.
- **Interconnection, combination or comparison of information** (item 9): the selection chain → likely.
- **Special categories interconnected with other data collected for other purposes** (item 10): only if art. 9 flows
  open → closed in production by R-SC-1 (A-31; `core.special_category`).

## 4. Conclusion

**DPIA to be prepared (in progress: [`DPIA.md`](DPIA.md)) unless legal review documents a reasoned conclusion that
it is not required. DPIA = PRODUCTION GATE** (checklist A-32; it blocks PRODUCTION_READY, not PRODUCT_COMPLETE).

The evidence that leads there:

- At least four WP248 criteria are likely met independently of the scale: 1 evaluation, 4 highly personal data,
  6 matching, and 7 vulnerable data subjects. The threshold of two is likely reached even before the scale is known.
- Two items of the Garante's list are likely relevant (6, 9).

This is an assessment, not a legal determination. It becomes a determination only when the controller, with the
legal review (and the DPO if one is designated, art. 35(2)), confirms or rejects it in writing.

The facts that could reverse it are, for the controller:
- whether the data subjects are vulnerable in the WP248 sense;
- the expected scale;
- whether the selection chain and the assessments open in production.

Until then the production checklist carries **A-32 DPIA** as a gate: the DPIA of [`DPIA.md`](DPIA.md) is completed
and signed and its measures are applied, unless the legal review's reasoned written conclusion that none is required
is on file.

The DPIA covers at least (all present in [`DPIA.md`](DPIA.md)):
- the processing of §1;
- the recipients and their roles;
- the retention policies (OF-06, OF-07);
- the hosting region and transfers (OF-02 to OF-04);
- the measures already in the code: pseudonymised IP, MFA for every role that reads others' data, signed 10-minute
  download links, private storage outside served directories, the identity disclosure's consent, purpose and expiry,
  the audit trail of every access.
