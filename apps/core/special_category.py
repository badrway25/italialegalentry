"""
R-SC-1 — the production safety control for special-category data (art. 9 GDPR). Owner directive V5.17 §4–§5.

No art. 9 condition is approved (``docs/compliance/SPECIAL_CATEGORY_AUDIT.md``). Until one is, production must not
expose a flow that INTENTIONALLY solicits special-category data. One setting decides, and every affected flow asks
this module, never the setting directly:

* ``ILE_SPECIAL_CATEGORY_FLOWS_ENABLED`` — ``False`` in ``base.py`` and in ``prod.py`` (where switching it on needs the
  written approval's reference, ``ILE_SPECIAL_CATEGORY_BASIS_REFERENCE``, or the settings refuse to load); the local
  preview (``dev.py``, DEBUG) and the test suite keep the full product so it can be demonstrated and accepted.

What the switch closes when it is off (S-nn are the audit's rows):

* S-02 — a requirement whose piece, by what it names, is a special-category document (``solicits_special_category``):
  not offered for filing (no form, no act on the register) and refused by ``documents.services.file_version`` whatever
  the road; the person reads a calm sentence (``CLOSED_PIECE_NOTICE``).
* S-01 — the loose upload keeps the named kinds (identity, diploma, contract); the open «Autre document», which
  invites the «just in case» file (V5.16 §6, T-1/T-2), is not offered (``loose_upload_kinds``).

What stays available, with the data-minimisation guidance (lane P2's sentences G-FREE and G-UPLOAD, in it/fr/en/ar):
the help-desk messages (S-03), the case file's free texts (S-05) and the loose upload of the named kinds. Nothing is
deleted from the local product, and no «explicit consent» box is added (V5.17 §4; audit T-7).

The guidance sentences are UI guidance, not legal content. Since the v515-d merge (DL54-174) they are catalogue
messages (``gettext_lazy``), as ``docs/design-v5/QA/v517-p3/NOTES.md`` asked the catalogue owner (lane D): the French
text is the msgid, and the Italian, English and Arabic are lane P3's own renderings, kept below as the reference the
catalogue was filled from (and that the tests read) — never a machine translation.
"""

from __future__ import annotations

import unicodedata

from django.conf import settings
from django.utils.translation import gettext_lazy

SETTING = "ILE_SPECIAL_CATEGORY_FLOWS_ENABLED"
REFUSAL_CODE = "special_category"


def flows_enabled() -> bool:
    """Whether the flows that intentionally solicit special-category data are offered. False unless switched on."""
    return bool(getattr(settings, SETTING, False))


#: G-FREE (SPECIAL_CATEGORY_AUDIT.md §4) — under a free-text field.
G_FREE = {
    "fr": (
        "N’indiquez pas de données sur la santé, l’origine ethnique, les convictions religieuses ou philosophiques, "
        "les opinions politiques, l’appartenance syndicale, la vie sexuelle ou l’orientation sexuelle : elles ne sont "
        "pas nécessaires ici."
    ),
    "it": (
        "Non indicate dati sulla salute, sull’origine etnica, sulle convinzioni religiose o filosofiche, sulle "
        "opinioni politiche, sull’appartenenza sindacale, sulla vita sessuale o sull’orientamento sessuale: qui non "
        "sono necessari."
    ),
    "en": (
        "Do not include information about health, ethnic origin, religious or philosophical beliefs, political "
        "opinions, trade-union membership, sex life or sexual orientation: it is not needed here."
    ),
    "ar": (
        "لا تذكروا هنا بيانات عن الصحة أو الأصل العرقي أو المعتقدات الدينية أو الفلسفية أو الآراء السياسية أو الانتماء "
        "النقابي أو الحياة الجنسية أو التوجه الجنسي: فهي غير ضرورية."
    ),
}

#: G-UPLOAD (SPECIAL_CATEGORY_AUDIT.md §4) — beside an upload.
G_UPLOAD = {
    "fr": (
        "Ne déposez que les pièces nécessaires à votre démarche : aucun document médical ni aucun document qui révèle "
        "la santé, l’origine ethnique, les convictions, les opinions, l’appartenance syndicale, la vie sexuelle ou "
        "l’orientation sexuelle."
    ),
    "it": (
        "Caricate solo i documenti necessari alla vostra pratica: nessun documento medico né alcun documento che "
        "riveli la salute, l’origine etnica, le convinzioni, le opinioni, l’appartenenza sindacale, la vita sessuale "
        "o l’orientamento sessuale."
    ),
    "en": (
        "Upload only the documents your application needs: no medical document, and no document that reveals health, "
        "ethnic origin, beliefs, opinions, trade-union membership, sex life or sexual orientation."
    ),
    "ar": (
        "لا تحمِّلوا إلا الوثائق اللازمة لملفكم: لا وثائق طبية، ولا أي وثيقة تكشف عن الصحة أو الأصل العرقي أو المعتقدات "
        "أو الآراء أو الانتماء النقابي أو الحياة الجنسية أو التوجه الجنسي."
    ),
}

#: The closed state of a special-category piece (production, switch off): a finished sentence, never «en cours».
CLOSED_PIECE = {
    "fr": (
        "Cette pièce ne se dépose pas sur la plateforme : elle relève des catégories particulières de données, que la "
        "plateforme ne reçoit pas. Pour savoir comment la transmettre, écrivez au Guichet numérique."
    ),
    "it": (
        "Questo documento non si carica sulla piattaforma: rientra nelle categorie particolari di dati, che la "
        "piattaforma non riceve. Per sapere come trasmetterlo, scrivete allo Sportello digitale."
    ),
    "en": (
        "This document is not uploaded to the platform: it falls within the special categories of data, which the "
        "platform does not receive. To find out how to send it, write to the Digital helpdesk."
    ),
    "ar": (
        "لا تُحمَّل هذه الوثيقة على المنصة: فهي من الفئات الخاصة من البيانات التي لا تتلقاها المنصة. لمعرفة طريقة "
        "إرسالها، راسلوا الشباك الرقمي."
    ),
}

#: The three catalogue messages (msgid = the French text above; it/en/ar in locale/, from the dictionaries above).
FREE_TEXT_GUIDANCE = gettext_lazy(
    "N’indiquez pas de données sur la santé, l’origine ethnique, les convictions religieuses ou philosophiques, "
    "les opinions politiques, l’appartenance syndicale, la vie sexuelle ou l’orientation sexuelle : elles ne sont "
    "pas nécessaires ici."
)
UPLOAD_GUIDANCE = gettext_lazy(
    "Ne déposez que les pièces nécessaires à votre démarche : aucun document médical ni aucun document qui révèle "
    "la santé, l’origine ethnique, les convictions, les opinions, l’appartenance syndicale, la vie sexuelle ou "
    "l’orientation sexuelle."
)
CLOSED_PIECE_NOTICE = gettext_lazy(
    "Cette pièce ne se dépose pas sur la plateforme : elle relève des catégories particulières de données, que la "
    "plateforme ne reçoit pas. Pour savoir comment la transmettre, écrivez au Guichet numérique."
)

#: What a requirement's code or title must name for the piece to be a special-category document. Words that
#: name the DOCUMENT, never a field of life («assurance médicale de voyage» is an insurance contract and stays open).
#: Accents and case are ignored. Extending this list closes more pieces in production; it never opens one.
SPECIAL_CATEGORY_TERMS = (
    # health
    "certificat medical",
    "certificats medicaux",
    "dossier medical",
    "rapport medical",
    "attestation medicale",
    "certificato medico",
    "certificati medici",
    "certificazione medica",
    "cartella clinica",
    "referto",
    "medical certificate",
    "medical record",
    "medical report",
    "health certificate",
    "certificato sanitario",
    "certificat de sante",
    "etat de sante",
    "stato di salute",
    "health status",
    "handicap",
    "disabilit",
    "invalidit",
    "vaccin",
    "grossesse",
    "gravidanza",
    "pregnan",
    # beliefs, union, origin, sex life, genetic and biometric data
    "religi",
    "confession",
    "syndica",
    "sindacal",
    "trade union",
    "origine ethnique",
    "origine etnica",
    "ethnic origin",
    "orientation sexuelle",
    "orientamento sessuale",
    "sexual orientation",
    "genetique",
    "genetic",
    # biometric DATA, never a biometric document: a photo is biometric data only when processed for unique
    # identification (recital 51), so «Passeport biométrique» and «Photo d'identité biométrique» stay open
    "donnees biometriques",
    "dati biometrici",
    "biometric data",
    "empreintes digitales",
    "impronte digitali",
    "fingerprint",
)


def _fold(value: str) -> str:
    decomposed = unicodedata.normalize("NFKD", value or "")
    plain = "".join(char for char in decomposed if not unicodedata.combining(char))
    return " ".join(plain.casefold().replace("_", " ").replace("-", " ").split())


def solicits_special_category(requirement) -> bool:
    """Whether the piece a requirement asks for is, by what it names, a special-category document.

    Code and title only, never ``detail``: a detail often says what NOT to send («sans mention religieuse», «no health
    data»), and reading it would close an ordinary piece (review of lane P3, recorded in the audit §3.1).
    """
    words = _fold(" ".join((requirement.code or "", requirement.title or "")))
    return any(term in words for term in SPECIAL_CATEGORY_TERMS)


def piece_closed(requirement) -> bool:
    """Whether filing this requirement is closed here: switch off AND a special-category piece."""
    return not flows_enabled() and solicits_special_category(requirement)


def loose_upload_kinds(choices):
    """The kinds the loose upload offers: all of them with the switch on, the named ones only with it off (S-01)."""
    from documents.models import DocumentKind

    if flows_enabled():
        return list(choices)
    return [(value, label) for value, label in choices if value != DocumentKind.OTHER]
