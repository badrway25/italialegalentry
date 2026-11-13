# OF-11 — the two deviations from Annexe 1, for the owner's acceptance (V5.17 §7)

- Written 28 October 2026 by the privacy lane P3 (label `v517-p3-build`). Directive V5.17 §7: «Do NOT auto-close
  OF-11 yet.» Before owner acceptance, both deviations are listed in full, one sentence each: ANNEXE 1 SAYS → VERIFIED
  PRODUCT REALITY → PROPOSED NOTICE. «No legal essay.»
- **OF-11 is OPEN — OWNER CONFIRMATION REQUIRED.** Publishing the cookie information is **not** the acceptance; the
  owner (or the legal lead) accepts both rows below in writing, with the date, before it is published. The locked
  source text (`apps/cms/locked_content.py`, `legal.cookies.fr_courtesy`) stays unchanged.
- Annexe 1 = the legal lead's French courtesy copy of Allegato 1 (14 Sept 2026), cookie section, archived in
  `apps/cms/locked_content.py` under `legal.cookies.fr_courtesy`. The proposed wording is the one already drafted in
  `apps/legal/content/cookies/{it,fr,en,ar}.txt` (§1 and §3).

| # | ANNEXE 1 SAYS | VERIFIED PRODUCT REALITY (evidence) | PROPOSED NOTICE |
|---|---|---|---|
| D-1 | Some pages may embed technical content hosted by external providers (images or graphic resources), and those providers may learn the user's IP address («Certaines pages peuvent intégrer des contenus techniques hébergés par des fournisseurs externes … ces fournisseurs peuvent connaître l’adresse IP de l’utilisateur»). | No page loads anything from another origin: the Content-Security-Policy allows `'self'` only (`config/settings/base.py`), fonts and images are self-hosted (`static/fonts/`, `static/img/`), `apps/cms/forbidden.py` refuses third-party hotlinks, and the privacy and cookie pages in it/fr/en/ar at 1440 and 390 px made zero requests to another origin (measured 28 Oct 2026, `PRIVACY_PROCESSING_AUDIT.md` §0). | The notice says that the pages load no fonts, scripts, images, maps or videos from other sites, so that no third party receives the visitor's IP address through them (`cookies/fr.txt` §1: «Les pages ne chargent ni polices, ni scripts, ni images, ni cartes, ni vidéos depuis d’autres sites : aucun tiers ne reçoit l’adresse IP des personnes qui les consultent.»). |
| D-2 | The site uses only technical cookies, and the information describes cookies alone, with no word on any other storage in the browser («Le site … utilise exclusivement des cookies techniques …»). | Besides its cookies, the site keeps first-party interface state in the browser, never sent to the server: localStorage `ile.rail`; sessionStorage `ile.lume`, `ile.hero.discovered`, `ile.dismissed.<id>`; and, for staff in the back office only, localStorage `adminTheme`, `sidebarOpen`, `sidebarWidth`, `commandHistory` (`PRIVACY_PROCESSING_AUDIT.md` §3; `static/js/src/*`; django-unfold `app.js`; pinned by `apps/legal/tests/test_privacy_cookie_v514.py`). | The notice names the browser storage beside the cookies — each key with its purpose and duration, as a technical tool that needs no consent — in its own section (`cookies/fr.txt` §3 «Stockage local du navigateur»). |

OF-11(b) — that the presentational sessionStorage keys count as technical — rides on D-2's acceptance and does not
block on its own (`PRIVACY_PROCESSING_AUDIT.md` §6).

| Accepted by | Date | Rows |
|---|---|---|
| — | — | — |
