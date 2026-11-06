# Preview capability vs production enablement (V5.17 §5)

- Written 28 October 2026 by the privacy lane P3 (label `v517-p3-build`). Directive V5.17 §5: «Clearly distinguish:
  PREVIEW CAPABILITY from PRODUCTION ENABLEMENT. A feature may be visually/functionally complete while remaining
  disabled in production pending a legal gate.»
- **Preview** = the local preview and development settings (`config/settings/dev.py`, DEBUG on), demonstrated with
  fictional data. **Production** = `config/settings/prod.py`, as the server's environment file
  (`docs/deployment/production.env.example`) sets it. A feature that is complete in the preview counts toward
  PRODUCT_COMPLETE; its production enablement waits on its gate and counts toward PRODUCTION_READY (runbook *States*).
- Each row names the switch the code reads and the test that proves the production state. Nothing here deletes a
  feature from the local product.

| Feature | Preview | Production | Gate (what opens it in production) |
|---|---|---|---|
| **Filing a special-category piece** (a requirement that names a medical certificate, a disability or religious certificate, a union card, fingerprints… — `core.special_category.SPECIAL_CATEGORY_TERMS`; SPECIAL_CATEGORY_AUDIT S-02) | available: the Dépôt is offered and files the piece | **not offered**: no Dépôt and no act on the register; the piece's page says, calmly, that the piece is not uploaded to the platform and to write to the Digital helpdesk; the service refuses it whatever the road | an art. 9 condition approved in writing (checklist **A-31**), then `ILE_SPECIAL_CATEGORY_FLOWS_ENABLED=1` **with** `ILE_SPECIAL_CATEGORY_BASIS_REFERENCE` (prod.py refuses the first without the second). Test: `apps/documents/tests/test_special_category_v517.py` |
| **Loose upload, «Autre document»** (S-01) | every kind, «Autre document» pre-selected as before | the named kinds only — identity, diploma, contract —, none pre-selected; «Autre document» refused if posted | as above (A-31) |
| **Loose upload of a named kind**, **pieces that are not special-category documents** (passport, diploma, contract, civil record…) | available | available, with the guidance G-UPLOAD beside the kind | — (the account must exist and have accepted the Conditions) |
| **Helpdesk messages** (S-03), **the case file's reason** (S-05) | available, with the guidance G-FREE | available, with the guidance G-FREE | — |
| **Privacy notice and cookie information with open fields** | shown, every «[DA COMPLETARE …]» highlighted with its class, and the list of open fields | never shown with an open field: the page says it is pending; `legal.services.publish` refuses to publish it | every marker replaced by its verified fact (checklist **A-29**, A-30, A-33). Switch: `ILE_LEGAL_OPEN_FIELDS_ALLOWED` (prod.py forces False). Tests: `apps/legal/tests/test_production_privacy_page_v517.py`, `apps/legal/tests/test_privacy_cookie_v514.py` |
| **Public forms and sign-up** | as G2 decides there (the legal pages of that database, or the audited override `forms_override_without_legal`) | closed while the legal pages are unpublished | G2 (`core.gates.public_forms_enabled`): the five legal pages published (G1), Allegato 1 received |
| **Newsletter** | its flag and G1 | closed while either is | flag `newsletter` **and** G1 |
| **Virtual Forum** | its flag and G1 | closed while either is | flag `virtual_forum` **and** G1 (G11) |
| **The design preview** `/__design-v5/` and its persona switch | `ILE_DESIGN_PREVIEW=1` with DEBUG | **does not exist** (the app is never installed, the routes never mounted) | none: development only (`dev.py`) |
| **Demonstration data** (synthetic accounts, cases, requests) | seeded (`ILE_SEED_DEMONSTRATION_DATA` = DEBUG) | never (prod.py forces False) | none |
| **Phase 3 content** | its flag and the date | closed until both | flag `phase3_public` and the date (G3) |

## The minimisation guidance (UI guidance, not legal content)

Lane P2's sentences ([`SPECIAL_CATEGORY_AUDIT.md`](SPECIAL_CATEGORY_AUDIT.md) §4), served in it/fr/en/ar by
`core.special_category` until the catalogue pass makes them catalogue messages:

- **G-FREE** under free texts: «N’indiquez pas de données sur la santé, l’origine ethnique, les convictions religieuses
  ou philosophiques, les opinions politiques, l’appartenance syndicale, la vie sexuelle ou l’orientation sexuelle :
  elles ne sont pas nécessaires ici.»
- **G-UPLOAD** beside uploads: «Ne déposez que les pièces nécessaires à votre démarche : aucun document médical ni
  aucun document qui révèle la santé, l’origine ethnique, les convictions, les opinions, l’appartenance syndicale, la
  vie sexuelle ou l’orientation sexuelle.»

No universal «explicit consent» checkbox is added anywhere (V5.17 §4; audit T-7).

## Showing the production state locally

`ILE_SPECIAL_CATEGORY_FLOWS_ENABLED=0` in the preview's environment shows the production state of the first two rows;
`DJANGO_DEBUG=0` shows the legal pages as production does.
