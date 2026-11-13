"""
The controlled allowlist of the Arabic completeness test (V5.24 §22; V5.27 §3, §5; FINAL_DELIVERY_V2 R7′ (g); lane AR).

Four tables, each entry with a one-line reason (``test_every_allowlist_entry_is_justified``): the proper names and
official titles kept in the original in every language, the acronyms, the Italian legal terms the glossary keeps Italian,
and the prescribed texts kept in their original by the owner's policy — the last table COMPUTED from the registry and
``cms.locked_renderings`` (the C-OFFICIAL class and the C-SUBST-FR texts, which the test admits only on their own page
and with their caption), nothing typed. A fifth table, ``KNOWN_FRENCH``, holds accepted exceptions under the §9 protocol
of docs/I18N_RTL.md and is EMPTY at merge (R7′: «KNOWN_FRENCH = {} stays»).

The burn-down table that stood here while the page lanes' contracts were open (``ARABIC_BURNDOWN``) reached zero and was
deleted with its mechanism by lane CLOSING (FINAL_DELIVERY_V2 §3.9; test_arabic_completeness.test_the_burn_down_is_closed).
"""

from __future__ import annotations

from cms import locked_renderings

PROPER_NAMES: dict[str, str] = {
    "Italy Legal Entry": "the brand (™ + LRM, isolated by {% brand %} / bdi)",
    "AGAMI — Dialogo Giuridico Interculturale APS": "the promoter's legal name (V5.23 Q9)",
    "Dialogo Giuridico Interculturale APS": "the promoter's legal name, after its acronym",
    "AGAMI": "the promoter",
    "Vénétie–Maroc": "the Forum's and the pilot's proper name, kept in every language (I18N_RTL §5)",
    "Forum Permanente Vénétie–Maroc": "the permanent Forum's Italian name, as the back-office writes it",
    "Numero Verde": "the toll-free line's Italian name, kept in every language",
    "Privacy Policy": "kept in the original in every language, as on the site",
    "Cookie Policy": "kept in the original in every language, as on the site",
    "Sala della Gran Guardia": "the Forum's venue, a proper name",
    "Made in Italy": "the ministry's name, kept in the original",
    "Rovigo": "a place name",
    "Comune di Valfiorita": "fictional preview organisation",
    "Istituto di formazione Collina Verde": "fictional preview organisation",
    "Università Collina Verde": "fictional preview organisation",
    "Centro linguistico Valfiorita": "fictional preview organisation",
    "Institut des métiers Oued Lakhdar": "fictional preview organisation",
    "DigitalOcean": "the hosting provider named in the privacy policy",
    "Google Authenticator": "product name",
    "Microsoft Authenticator": "product name",
    "Host Grotesk": "a typeface's name (the dev board's type sheet)",
    "Readex Pro": "a typeface's name (the dev board's type sheet)",
}

ACRONYMS: dict[str, str] = {
    "TOTP": "two-factor authentication (the code app)",
    "OTP": "one-time password (two-factor authentication)",
    "QR": "the QR code of the two-factor set-up",
    "PDF": "file type",
    "UE": "Union européenne",
    "EU": "European Union",
    "SMS": "channel",
    "CSV": "file type",
    "RUNTS": "Registro Unico Nazionale del Terzo Settore",
    "CF": "codice fiscale",
    "IBAN": "banking",
    "PEC": "posta elettronica certificata",
    "SPID": "Italian digital identity",
    "CIE": "carta d'identità elettronica",
    "CEFR": "language levels",
    "QCER": "language levels (it)",
    "TIG": "welding",
    "MIG": "welding",
    "HTTPS": "protocol",
    "CSRF": "security",
    "GDPR": "regulation",
    "RGPD": "regulation",
    "DPO": "data protection officer",
    "APS": "legal form",
    "ETS": "legal form",
    "ONLUS": "legal form",
    "ID": "identifier",
    "URL": "address",
    "IP": "address",
    "WhatsApp": "channel",
    "ILE": "the project's acronym",
    "FAQ": "the page's name, kept in every language",
}

ITALIAN_LEGAL_TERMS: dict[str, str] = dict.fromkeys(
    (
        "Questura",
        "Prefettura",
        "Nulla osta",
        "Nulla Osta",
        "Permesso di soggiorno",
        "Carta blu UE",
        "Carta Blu UE",
        "Codice fiscale",
        "Decreto flussi",
        "Decreto Flussi",
        "decreto flussi",
        "Dichiarazione di valore",
        "Legalizzazione",
        "Apostille",
        "Ricongiungimento familiare",
        "Visto d’ingresso",
        "Visto d'ingresso",
        "Sportello Unico per l’Immigrazione",
        "Sportello Unico",
        "Sportello unico",
        "Testo Unico sull’Immigrazione",
        "Testo unico sull’immigrazione",
        "Testo unico sull'immigrazione",
        "Comune",
        "Regione",
        "Ministero",
        "Consolato",
        "Ambasciata",
        "Decreto Regione Veneto",
        "Repertorio",
        "Associazione di Promozione Sociale",
        "Ente del Terzo Settore",
        "Partita IVA",
        "Registro delle Imprese",
        "Convention de La Haye du 5 octobre 1961",
        "Quadro comune europeo di riferimento per le lingue",
        "soggetti autorizzati",
    ),
    "Italian legal term kept in Italian in every language (docs/I18N_RTL.md §9)",
)


def _language_names(kind: str) -> dict[str, str]:
    """The language switcher's words, written in their own language on every page — each configured language's
    endonym («Français») or its code («fr») — computed from ``settings.LANGUAGES`` and Django's locale table, never
    typed."""
    from django.conf import settings
    from django.conf.locale import LANG_INFO

    out: dict[str, str] = {}
    for code, _name in settings.LANGUAGES:
        if kind == "code":
            out[code] = f"the language switcher's code of {code}"
        elif LANG_INFO.get(code, {}).get("name_local"):
            local = LANG_INFO[code]["name_local"]
            for form in (local, local[:1].upper() + local[1:]):  # Django's «français», the switcher's «Français»
                out[form] = f"the language switcher's endonym of {code}"
    return out


#: the language switcher's endonyms (computed; matched as phrases, like the proper names)
LANGUAGE_NAMES: dict[str, str] = _language_names("endonym")
#: the language switcher's codes (computed; matched as whole words, like the acronyms)
LANGUAGE_CODES: dict[str, str] = _language_names("code")

#: accepted exceptions (I18N_RTL §9 protocol): {"ID": ("regex", "reason")} — EMPTY at merge (R7′)
KNOWN_FRENCH: dict[str, tuple[str, str]] = {}


def official_texts() -> dict[str, str]:
    """The C-OFFICIAL texts of the registry and the prescribed Forum title — computed, never typed: a run that equals one
    of them is kept in its original on every page (R7′ (4))."""
    out: dict[str, str] = {}
    for subkey, french in locked_renderings.leaves():
        if locked_renderings.treatment(subkey) == locked_renderings.C_OFFICIAL and len(french) >= 3:
            out[" ".join(french.split())] = f"C-OFFICIAL {subkey}"
    for msgid, why in locked_renderings.OFFICIAL_MSGIDS.items():
        out[msgid] = why
    return out


def source_texts() -> dict[str, str]:
    """The C-SUBST-FR texts (the substantive blocks whose only source is the prescribed French), by their normalised
    value → sub-key: on their own page they stand in French, isolated and captioned; anywhere else they are hidden."""
    return {
        " ".join(french.split()): subkey
        for subkey, french in locked_renderings.leaves()
        if locked_renderings.treatment(subkey) == locked_renderings.C_SUBST_FR
    }


def rendered_texts() -> dict[str, str]:
    """The C-UI texts (French → sub-key): a French run equal to one of them on /ar/ is a rendering that did not reach the
    page — unintended French (R7′: «every (1) key renders Arabic with no French word»)."""
    return {
        " ".join(french.split()): subkey
        for subkey, french in locked_renderings.leaves()
        if locked_renderings.treatment(subkey) == locked_renderings.C_UI
    }
