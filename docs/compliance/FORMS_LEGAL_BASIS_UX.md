# Forms: legal-basis UX (V5.16 §3)

- Written 28 October 2026 by lane P2 (label `v516-p2-build`). An inventory of every public and platform form's
  privacy box or text, read from the code on branch `v516-p2`.
- Directive V5.16 §3 (OF-09):
  - «Do NOT use mandatory "consent to processing" checkboxes for processing that is necessary to provide a service
    requested by the user if the approved lawful basis is Article 6(1)(b).»
  - **A. REQUIRED PROCESSING**: «do not ask for "consent"»; acknowledgement wording such as «I have read the
    Privacy Notice» where useful; «Do NOT present acknowledgement as a GDPR consent.»
  - **B. OPTIONAL PROCESSING**: «separate, optional, specific consent only if such processing actually exists. No
    bundled consent. No pre-ticked boxes. No fake consent used to legitimise mandatory processing.»
- **Locked copy rule.** The implementation document's verbatim texts (`apps/cms/locked_content.py`) are never
  reworded by the team. Where one conflicts with §3, the code keeps it unchanged and marks it **LOCKED COPY — LEGAL
  REVIEW REQUIRED** (`consents.services.LOCKED_COPY_LEGAL_REVIEW_REQUIRED`). §3 below gives the proposed compliant
  wording for the owner and the legal lead. The forms that depend on Allegato 1 stay closed (G2).
- Tests: `tests/compliance/test_forms_legal_basis_v516.py`.

## 1. Inventory

| # | Form | Box / text | Wording source | Class | Status after this lane |
|---|---|---|---|---|---|
| F-01 | **Company needs** (`enquiries.CompanyNeedsForm`; closed by G2) | required box «J’ai lu l’information sur le traitement des données personnelles et je consens au traitement de mes données pour le suivi de la présente demande.» | **prescribed**: IMPL p.2 §1.1, `p1.companies.form.consent` | **A** (6(1)(b), ANX §3) asked as a consent | **LOCKED COPY — LEGAL REVIEW REQUIRED**. Unchanged; proposal P-1 |
| F-02 | **Institution proposal** (`CollaborationProposalForm`; closed by G2) | required box | **team's** (until now a reuse of F-01's sentence, `REUSED_CONSENT_KEYS`, «PENDING_CLIENT», `docs/LEGAL_AND_PUBLICATION_GATES.md` §G2 table) | **A** | **fixed**: acknowledgement «J’ai lu l’information sur le traitement des données personnelles.» (`consents.services.ACKNOWLEDGEMENT_TEXT`), `AcknowledgementBooleanField` (its error never says «consent»). An existing text row of the old reuse is versioned, so earlier records keep what was shown |
| F-03 | **University proposal** (same form, `purpose=university_proposal`; closed by G2) | required box | team's (same reuse) | **A** | **fixed**, as F-02 |
| F-04 | **Contact** (`enquiries.ContactForm`; closed by G2) | required box | team's (same reuse) | **A** | **fixed**, as F-02 |
| F-05 | **Forum registration** (`forum.ForumRegistrationForm`; closed by G2 and `forum_public`) | required box «J’ai lu l’information sur le traitement des données personnelles et je consens au traitement de mes données pour la gestion de l’inscription au Forum.» | **prescribed**: IMPL p.5 §2.1, `p2.forum.registration.consent` | **A** (6(1)(b), ANX §3 «inscriptions aux événements») asked as a consent | **LOCKED COPY — LEGAL REVIEW REQUIRED**. Unchanged; proposal P-2 |
| F-06 | **Newsletter «Restez informés»** (`news.NewsletterForm`; closed by the `newsletter` flag and G1) | required box on a form whose only purpose is the newsletter: «Je souhaite recevoir les communications informatives d’Italy Legal Entry et je consens au traitement de mes données à cette fin (consentement révocable à tout moment).» | **prescribed**: IMPL p.12 §3.8.6, `p3.news.newsletter_consent` («ne jamais précocher la case») | **B** (6(1)(a), ANX §3): a real optional purpose | **compliant as prescribed**: separate form, specific, unticked, revocable, double opt-in |
| F-07 | **Sign-up** (`accounts.SignupForm`; closed by G2) | required box «J’ai lu la Privacy Policy et j’accepte les Conditions d’utilisation.» | **team's** (CONTENT_PENDING_LEGAL_REVIEW; IMPL §3.8.7 asks for acceptance of the terms and the Privacy Policy) | **A**: an acknowledgement of the notice plus acceptance of the terms (a contract), not a consent | **fixed**: `AcknowledgementBooleanField`; the earlier error «Il consenso è obbligatorio per inviare la richiesta.» no longer appears |
| F-08 | **Virtual Forum join** (`community.JoinForm`; closed by its flag and G1) | required box «J’ai lu la Privacy Policy et j’accepte les Conditions d’utilisation du Forum Virtuel.»; **optional** boxes «Afficher mon nom aux autres membres», «Afficher mon organisme aux autres membres» | team's | required box: **A**; visibility choices: **B** (IMPL §3.8.7 «aucune donnée des participants n’est visible publiquement sans leur consentement») | **fixed** (acknowledgement field); the two optional boxes are already separate, not required and unticked (default False) |
| F-09 | **Selection: identity disclosure** (`templates/selection/disclosures.html`) | per request, two buttons «Refuser» / «Communiquer l’identité»; the text «J’autorise la communication de mon identité à l’entreprise nommée ci-dessus, pour la finalité indiquée et pour la durée indiquée. Je peux retirer cette autorisation à tout moment…» (`selection.services`) | team's | **B**: specific consent (6(1)(a)), for a named company, purpose and duration ≤ 180 days; refusal has no consequence | **compliant**: separate, specific, never pre-chosen, withdrawable |
| F-10 | **Document upload** (`documents` forms; live) | no privacy box. Filing is gated by acceptance of the terms (`templates/documents/partials/depot.html:81-82`) | team's | **A** | no box needed. Guidance added (SPECIAL_CATEGORY_AUDIT §4). The notice link by the upload control is lane P's request R-3 |
| F-11 | **Helpdesk request** (`helpdesk.OpenRequestForm`; live) | optional box «Je demande une vérification par un professionnel» | team's | a **service choice**, not a consent | compliant: optional, unticked |
| F-12 | **Orientation questionnaire** (`orientation` forms; live) | no box; `ConsentPurpose.ORIENTATION` is declared but no form records it | — | **A** (6(1)(b), ANX §3) | no box needed. The missing notice link is lane P's request R-3 (orientation owner) |
| F-13 | **Sign-in, password reset, account deletion and export, company profile and needs** | no privacy box | — | **A** | nothing to change. Notice links: lane P's requests (allauth templates, accounts templates) |

**Pre-ticked boxes**: none. Every `BooleanField` on these forms has `initial=False` and renders without `checked`
(test `test_no_box_on_any_form_is_pre_ticked`).

**Bundling**: no team label joins a consent to another purpose
(`test_a_bundled_consent_is_not_offered_anywhere`). F-07 and F-08 join an acknowledgement and a terms acceptance.
Neither is a consent; whether the legal lead wants them split into two boxes is noted in §3.

## 2. What changed in the code (minimal, recorded)

- `apps/core/forms.py`: `AcknowledgementBooleanField` — required, never pre-ticked, the CSS hook `consent-checkbox`
  kept (the form-field component keys on it), Django's own required message. `ConsentBooleanField` is unchanged and
  now serves the three prescribed sentences only.
- `apps/consents/services.py`:
  - `REUSED_CONSENT_KEYS` is empty;
  - `ACKNOWLEDGEMENT_TEXT` / `ACKNOWLEDGEMENT_PURPOSES` (F-02 to F-04, and the unused `orientation` purpose);
  - `ensure_consent_text` creates a **new version** when the current row is the old reuse;
  - `LOCKED_COPY_LEGAL_REVIEW_REQUIRED` marks F-01 and F-05.
- `apps/enquiries/forms.py`: the label and the field type follow the purpose (prescribed → locked consent sentence;
  team → acknowledgement).
- `apps/accounts/forms.py`, `apps/community/forms.py`: the acknowledgement field.
- **No new catalogue message.** The acknowledgement «J’ai lu l’information sur le traitement des données
  personnelles.» is the first half of a locked sentence, and the catalogue's locked-fragment rule
  (`tests/i18n/test_catalogues.py`) keeps such text out of the `.po` files without a reviewed decision. So it is
  shown in French with `lang="fr"` on /it/, /en/ and /ar/, exactly as the prescribed sentences beside it are today.
  Its translations are requested from lane D together with P-1/P-2 once the legal lead approves them.

## 3. LOCKED COPY — LEGAL REVIEW REQUIRED: proposed compliant wording (for the owner and the legal lead)

The team does not apply these proposals. Each one needs the owner's and the legal lead's written approval, and the
Italian Allegato 1 prevails.

- **P-1 (F-01, company needs; replaces `p1.companies.form.consent`)**
  - Acknowledgement, required (category A): «J’ai lu l’information sur le traitement des données personnelles
    (Privacy Policy).»
  - No consent is needed for handling the request: ANX §3 founds it on art. 6(1)(b).
  - If the controller wants to keep the company's details for later projects beyond the request, that is a
    separate optional purpose (category B). It would need its own box, unticked: «J’accepte d’être recontacté(e)
    pour d’autres projets de coopération d’Italy Legal Entry (facultatif, révocable à tout moment).» Only if that
    purpose exists.
- **P-2 (F-05, Forum registration; replaces `p2.forum.registration.consent`)**
  - Acknowledgement, required (category A): «J’ai lu l’information sur le traitement des données personnelles
    (Privacy Policy).»
  - Any optional use, such as photographs at the event or publishing the participant's name, would need its own
    separate, unticked consent, and only if that use exists.
- **P-3 (F-07, F-08; team wording, optional refinement)**
  - The legal lead may prefer two boxes: «J’ai lu la Privacy Policy.» and «J’accepte les Conditions d’utilisation.»
  - Neither is a consent. The team keeps one box until the legal lead decides, because IMPL §3.8.7 prescribes the
    acceptance of the terms and the notice together.
- **OF-09** is answered by P-1 and P-2 once approved: one basis (6(1)(b)) for the form processing, stated in the
  notice's forms section before G2 opens.

## 4. Requests

- **Owner of `templates/pages/contact.html`**: its comment says «The sentence about data processing is prescribed
  wording (consent texts)». For the contact form that is no longer true: the box is the team's acknowledgement
  (F-04). It is a comment only.
- **Lane D (catalogue)**: after the legal lead's decision on P-1/P-2, add the acknowledgement (§2) with its it/en/ar
  translations and an overlap decision for the locked fragment.
