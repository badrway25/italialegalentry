# DPO assessment — art. 37 GDPR (V5.16 §7)

- Written 28 October 2026 by lane P2 (label `v516-p2-build`). An assessment of the triggers against the processing
  the software performs ([`PROCESSING_PURPOSE_MATRIX.md`](PROCESSING_PURPOSE_MATRIX.md)). It is not the controller's
  decision, and it designates nobody.
- Directive V5.16 §7: «Do NOT invent a DPO. Italy Legal Entry must not be treated as a public authority. A DPO is not
  automatically required merely because the platform processes personal data … Until that assessment is completed:
  DPO STATUS = TO BE CONFIRMED.»
- The assessment is the **controller's**. The candidate controller is AGAMI — Dialogo Giuridico Interculturale APS
  (OF-01, OWNER CONFIRMATION REQUIRED). Italy Legal Entry is not substituted as controller unless the owner confirms
  it is a separate legal entity (OF-01); until then the assessment is addressed to the candidate controller.
- Sources: art. 37(1) and (4) GDPR; the Article 29 Working Party guidelines on DPOs (WP243 rev.01), endorsed by the
  EDPB, which define «core activities», «large scale» and «regular and systematic monitoring». The legal review
  should check these references.

## 1. The three triggers of art. 37(1)

| Trigger | Assessment against the actual processing | What decides it | Today |
|---|---|---|---|
| **(a)** processing carried out by a **public authority or body** | AGAMI APS is an association of social promotion registered in RUNTS (ANX §1.1), a private body. Institutions that use the platform are users or recipients, not the controller ([`RECIPIENT_ROLES_MATRIX.md`](RECIPIENT_ROLES_MATRIX.md)). Directive: ILE «must not be treated as a public authority» | the controller's legal form (OF-01) | **not met** |
| **(b)** core activities consisting of processing that requires **regular and systematic monitoring** of data subjects **on a large scale** | Partly relevant. The platform follows a person's pathway over time: the case file with its status history, checklist, deadlines, the training plan and attendance, the selection stages (M-07 to M-12). WP243 counts «regular and systematic» as ongoing, according to a system and planned; case-file follow-up could qualify. There is no online tracking or profiling (lane P audit §0, §2.3: no analytics, no behavioural profiling), and the orientation result is informational (ANX §4). **Large scale is unknown before launch** | whether the platform is AGAMI's **core activity** (the APS's purpose and its share of the APS's activities); the **number of data subjects** expected with an active case file per year; the **duration** of the follow-up; the **geographical extent** (Italy and Morocco; the Forum's two countries) | **TO BE CONFIRMED** |
| **(c)** core activities consisting of **large-scale** processing of **special categories** (art. 9) or criminal data (art. 10) | The design does not intend art. 9 data, but uploads and free texts can carry them ([`SPECIAL_CATEGORY_AUDIT.md`](SPECIAL_CATEGORY_AUDIT.md) S-01 to S-07). If the legal review approves an art. 9 condition and those flows open, this trigger must be re-assessed with the scale. Art. 10: no model field and no orientation question asks for criminal convictions or offences (grep of `apps/*/models.py` and `apps/orientation/seeds.py`); free texts could still carry them, which the same gate covers | whether art. 9 flows open in production (A-31), and at what scale | **not met while the art. 9 flows stay closed; TO BE CONFIRMED otherwise** |

## 2. Art. 37(4): Union or Member State law

- No Italian provision found by this lane makes a DPO mandatory for a private association beyond art. 37(1). The
  Codice privacy (D.Lgs. 196/2003 as amended by D.Lgs. 101/2018) adds no general obligation for private bodies.
- This is to be confirmed by the legal review, which is not this lane's role.

## 3. Conclusion

**DPO STATUS = TO BE CONFIRMED.**

- Trigger (a) is not met.
- Trigger (b) depends on facts that do not exist before launch: the core-activity question and the scale.
- Trigger (c) is not met while the art. 9 flows stay closed (A-31).

The facts that decide it, for the owner:
1. The expected number of persons with a case file in the first year, and their geographical spread.
2. Whether operating the platform is a core activity of AGAMI APS, or ancillary to its other activities.
3. Whether any art. 9 flow will open in production (the legal review's answer to SPECIAL CATEGORY LEGAL BASIS
   REQUIRED).
4. The duration of a pathway's follow-up (case files, training, selection).

Outcomes:
- If the controller concludes that no trigger applies, the privacy notice says so in OF-08 and keeps the record of
  the assessment (accountability, art. 5(2)).
- If a trigger applies, the controller designates a DPO (art. 37(5)–(7)), publishes the contact details and tells
  the Garante. The notice then names the DPO.
- A voluntary designation is also possible.

The privacy notice's marker **OF-08 — LEGAL REVIEW REQUIRED: DPO STATUS = TO BE CONFIRMED** stays until then. The
production publication guard refuses the notice while it is there.
