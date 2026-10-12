"""
i18n audit — translation coverage, catalogue hygiene and locked-text leak detection.

The UI strings of Italy Legal Entry™ are gettext messages with a FRENCH source (ADR-004), translated by
the team into Italian, English and Arabic (``locale/<lang>/LC_MESSAGES/django.po``; the small ``fr``
catalogue only normalises the few msgids that were not written in French and the French plural rule).
Prescribed texts live in ``apps/cms/locked_content.py`` and must NEVER enter a catalogue: a locked text
inside a ``.po`` file would be translated by the team, which the Implementation document forbids.

Usage (from the project root)::

    .venv/Scripts/python scripts/i18n_audit.py              # report; exit 1 when a check fails
    .venv/Scripts/python scripts/i18n_audit.py --json       # same data, machine readable
    .venv/Scripts/python scripts/i18n_audit.py --compile    # write the .mo files in pure Python
                                                            # (fallback when GNU msgfmt is missing)
    .venv/Scripts/python scripts/i18n_audit.py --no-sources # catalogues only, skip the source scan
    .venv/Scripts/python scripts/i18n_audit.py --sync       # pure-Python « makemessages »: add the new
                                                            # msgids (empty msgstr), drop the unused ones

Checks, per language:

* number of msgids / translated / untranslated / fuzzy / obsolete — coverage must be 100 %, no fuzzy;
* ``Language`` and ``Plural-Forms`` headers (it: 2 forms, en: 2, fr: 2, ar: 6) and every plural index filled;
* placeholders (``%(name)s``, ``%s``, ``{name}``) and inline HTML tags identical in msgid and msgstr;
* no forbidden formulation (``cms.forbidden``), no mojibake, no Arabic-Indic digit, Arabic entries really
  written in Arabic script (apart from the documented keep-as-is list), and « ™ » followed by U+200E in
  every Arabic sentence, so that the sign stays on the right of the trademark (bidi);
* no msgid carrying a fragment of a locked text (cross-check against ``cms.locked_content``; six consecutive
  words are enough — every hit is either justified in ``REVIEWED_OVERLAPS`` or frozen in ``KEEP_SOURCE``);
* catalogue ↔ sources synchronisation: every gettext message of the templates and Python modules must be in
  the catalogue (``source_messages`` — pure Python, no GNU xgettext needed; skip with ``--no-sources``);
* the compiled ``.mo`` must match its ``.po`` entry by entry (content comparison, never file dates).
* in the optional ``fr`` catalogue, no Italian-source sentence left identical to its msgid (``--sync`` copies
  a new msgid as its own French text, which is wrong for the few back-office strings written in Italian).

The module has no third-party dependency (the source scan uses Django's own ``templatize``) and does not
need a database; ``parse_po``, ``source_messages`` and ``mo_differences`` are reused by ``tests/i18n``.
"""

from __future__ import annotations

import argparse
import array
import json
import re
import struct
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT / "apps") not in sys.path:
    sys.path.insert(0, str(ROOT / "apps"))

LOCALE_DIR = ROOT / "locale"
DOMAIN = "django"

#: Languages translated by the team, with the number of plural forms gettext expects.
TRANSLATED_LANGUAGES: dict[str, int] = {"it": 2, "en": 2, "ar": 6}
#: Optional catalogues, audited when present (``fr`` = source-language normalisation catalogue).
OPTIONAL_LANGUAGES: dict[str, int] = {"fr": 2}

#: Minimum length (characters, normalised) for a locked string / msgid to count as a "fragment".
FRAGMENT_MIN_CHARS = 40
#: Number of consecutive identical words shared with a locked text that flags a msgid. Six words is the
#: project-wide review rule (« any 6+ word fragment of a prescribed text outside the registry »): every hit
#: must be dispositioned below — REVIEWED_OVERLAPS (translated, justified) or KEEP_SOURCE (never translated).
FRAGMENT_SHINGLE_WORDS = 6

#: Overlaps with the locked registry that were REVIEWED and judged NOT to be prescribed text. They are
#: translated like any other UI string. Every entry needs a written justification; the audit prints the
#: list on each run so the decision stays visible. Any overlap that is not listed here FAILS the audit.
REVIEWED_OVERLAPS: dict[str, str] = {
    "Les logos de la Région de la Vénétie et de la Commune de Rovigo seront transmis avec leurs autorisations : "
    "ne jamais télécharger ni inventer un logo. Un partenaire non autorisé n’est jamais affiché publiquement.": (
        "back-office help text; the only shared words are the names of the two patron institutions"
    ),
    "Personnes, entreprises, institutions, universités, organismes de formation et professionnels : "
    "les acteurs de l’écosystème Italy Legal Entry™.": (
        "meta description; shares only the generic enumeration of stakeholder categories with p3.hero.body"
    ),
    "Institutions, entreprises, universités, organismes de formation et professionnels qui participent au projet "
    "Italy Legal Entry™.": (
        "meta description; shares only the generic enumeration of stakeholder categories with p3.virtual_forum.body"
    ),
    "Représentations diplomatiques et consulaires": (
        "partner category label (four common nouns that also occur in the Forum audience list)"
    ),
    "Institutions, universités et organismes de formation : présentez votre proposition de collaboration dans le "
    "cadre du projet Italy Legal Entry™. Elle sera examinée par l’équipe du projet, qui vous recontactera si "
    "nécessaire.": "form introduction; shares only the generic phrase « dans le cadre du projet Italy Legal Entry™ »",
    "Consulter l’information sur le traitement des données personnelles (Privacy Policy)": (
        "link label that names the privacy notice; the notice itself is a legal page and is never translated"
    ),
    # --- six-word overlaps (independent review, 2026-09-20): the shared span is a noun phrase or a mandated
    # --- designation, never a clause of the prescribed sentence; the sentence itself is team-written UI copy.
    "Point de départ de la durée de conservation (24 mois à compter du dernier contact).": (
        "back-office help text stating the retention period as a fact; shares only the span « mois à compter du "
        "dernier contact » with the courtesy privacy text"
    ),
    "Faire connaître les besoins professionnels de votre entreprise dans le cadre du projet.": (
        "team-written card text; shares only the noun phrase « les besoins professionnels de votre entreprise »"
    ),
    "Ce formulaire sera activé dès la publication des informations sur le traitement des données personnelles. "
    "Vous pouvez nous écrire à l’adresse ci-dessous.": (
        "gate G2 notice; shares only the generic GDPR noun phrase « sur le traitement des données personnelles »"
    ),
    "L’information sur le traitement des données personnelles est disponible sur la page": (
        "link introduction; shares only the generic GDPR noun phrase that names the privacy notice"
    ),
    "Les informations sur le traitement des données personnelles figurent dans la Privacy Policy.": (
        "link introduction; shares only the generic GDPR noun phrase that names the privacy notice"
    ),
    "Vos données sont traitées pour la gestion de l’inscription au Forum, conformément à l’information sur le "
    "traitement des données personnelles publiée sur le site.": (
        "acknowledgement e-mail; shares only the purpose label « la gestion de l’inscription au Forum », not the "
        "consent sentence (which is rendered from the registry on the form)"
    ),
    "Vous avez demandé à recevoir les communications informatives d’Italy Legal Entry™. Pour confirmer votre "
    "inscription, ouvrez le lien suivant :": (
        "double opt-in e-mail; shares only the name of the service the visitor subscribed to, not the consent sentence"
    ),
    "Répondez à quelques questions sur votre situation et recevez une pré-évaluation à caractère informatif sur la "
    "famille de parcours régulier vers l’Italie qui correspond à votre projet.": (
        "questionnaire introduction; shares the mandated designation « pré-évaluation à caractère informatif » "
        "(the result must always be named so) and its verb"
    ),
    "Répondez à quelques questions pour identifier les voies régulières à explorer, avec les étapes et la "
    "documentation généralement requises.": (
        "interim page introduction; shares only the noun phrase « les étapes et la documentation généralement "
        "requises » — rewording requested from the pathways owner to remove the echo of p3.persons.intro"
    ),
    "Avant le départ, des parcours de formation professionnelle et civico-linguistique peuvent être organisés dans le "
    "pays d’origine avec des organismes partenaires : langue italienne, connaissance de la vie en Italie, compétences "
    "utiles au parcours envisagé.": (
        "training page card; shares only the noun phrase « parcours de formation professionnelle et "
        "civico-linguistique » — rewording requested from the pathways owner"
    ),
}

#: Locked-derived wording found in a source file that this catalogue does not own. Until the owner removes
#: it from the template, the msgstr MUST stay identical to the French msgid in every language, so that the
#: team never translates a fragment of a prescribed text (the audit enforces msgstr == msgid).
KEEP_SOURCE: dict[str, str] = {
    "Espace permanent de dialogue et de coopération": (
        "templates/forum/partials/hero.html — eyebrow lifted from p2.forum.what.body[0]; change requested: "
        "render it from the locked registry or reword it"
    ),
    "Signalez les besoins professionnels de votre entreprise.": (
        "apps/cms/templatetags/cms_nav.py — mega-menu description that truncates p3.entrances.company.text (its "
        "opening clause, verb included); change requested: reword the description so it no longer abbreviates a "
        "prescribed sentence"
    ),
    "Vivre en Italie — %(topic)s : fiches pratiques pour accompagner l’intégration après l’entrée régulière.": (
        "templates/living/topic.html — meta description ending with the closing clause of p3.living.body; change "
        "requested: reword it or build it from the locked registry"
    ),
}

#: msgids that legitimately stay identical in every language (trademark, proper nouns, document names
#: kept in the original as on the site, technical acronyms). Anything else left without Arabic script in
#: the Arabic catalogue is reported.
KEEP_AS_IS = re.compile(
    r"^(?:Italy Legal Entry(?:\u2122)?|AGAMI(?: \u2014 Dialogo Giuridico Interculturale APS)?|Privacy Policy|"
    r"Cookie Policy|FAQ|CSV|PDF|URL|IP|ID|SEO|API|CRM|MFA|TOTP|JSON|HTML|SHA-256|UUID|E-mail|RBAC|"
    r"[A-Z][A-Z0-9_]{2,}|[\W\d_]*|%\([a-z_]+\)s|\{[a-z_]+\})$"
)

#: Bidi rule of the Arabic catalogue. « ™ » is a neutral character: at the end of a Latin run inside a
#: right-to-left sentence it takes the paragraph direction and is painted on the LEFT of the name
#: (« ™Italy Legal Entry »). A LEFT-TO-RIGHT MARK (U+200E) right after it keeps the sign attached to the
#: trademark. The same holds for the placeholders that receive the trademark (``site.project_name``).
LRM = "\u200e"
_TRADEMARK_WITHOUT_LRM = re.compile("\u2122(?!\u200e)")
BRAND_PLACEHOLDERS: tuple[str, ...] = ("%(project)s",)

_ARABIC = re.compile(r"[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]")
_ARABIC_INDIC_DIGITS = re.compile(r"[\u0660-\u0669\u06F0-\u06F9]")
# UTF-8 read as Latin-1/CP1252: "Ã" + continuation byte, "â€" (punctuation), "Ø"/"Ù" + byte (Arabic).
_MOJIBAKE = re.compile(r"\u00c3[\u0080-\u00bf]|\u00e2\u20ac|[\u00d8\u00d9][\u0080-\u00bf]|\ufffd")
_PERCENT = re.compile(r"%(?:\([A-Za-z_][A-Za-z0-9_]*\))?[#0\- +]?\d*(?:\.\d+)?[sdifgrxu]|%%")
_BRACE = re.compile(r"\{[A-Za-z_][A-Za-z0-9_.]*(?:![rsa])?(?::[^{}]*)?\}")
_HTML_TAG = re.compile(r"</?(?:a|abbr|b|br|code|em|i|p|span|strong|sub|sup|u)\b")
_KEYWORD = re.compile(r'^(msgctxt|msgid_plural|msgid|msgstr)(?:\[(\d+)\])?\s+(".*")\s*$')
_ESCAPES = {"n": "\n", "t": "\t", "r": "\r", '"': '"', "\\": "\\"}


# ---------------------------------------------------------------------------------------------
# PO parsing
# ---------------------------------------------------------------------------------------------
@dataclass
class Entry:
    msgid: str = ""
    msgctxt: str | None = None
    msgid_plural: str | None = None
    msgstr: dict[int, str] = field(default_factory=dict)
    comments: list[str] = field(default_factory=list)
    obsolete: bool = False

    @property
    def flags(self) -> set[str]:
        found: set[str] = set()
        for line in self.comments:
            if line.startswith("#,"):
                found.update(part.strip() for part in line[2:].split(",") if part.strip())
        return found

    @property
    def references(self) -> list[str]:
        refs: list[str] = []
        for line in self.comments:
            if line.startswith("#:"):
                refs.extend(line[2:].split())
        return refs

    @property
    def is_header(self) -> bool:
        return self.msgid == "" and self.msgctxt is None

    @property
    def is_fuzzy(self) -> bool:
        return "fuzzy" in self.flags

    @property
    def is_plural(self) -> bool:
        return self.msgid_plural is not None

    def is_translated(self, nplurals: int = 1) -> bool:
        if self.is_plural:
            return all(self.msgstr.get(i, "") != "" for i in range(nplurals))
        return self.msgstr.get(0, "") != ""


def _unquote(token: str) -> str:
    body = token[1:-1]
    out: list[str] = []
    i = 0
    while i < len(body):
        char = body[i]
        if char == "\\" and i + 1 < len(body):
            out.append(_ESCAPES.get(body[i + 1], "\\" + body[i + 1]))
            i += 2
        else:
            out.append(char)
            i += 1
    return "".join(out)


def parse_po(path: Path | str) -> list[Entry]:
    """Parse a ``.po`` file into entries (header included, obsolete entries flagged)."""
    return parse_po_text(Path(path).read_text(encoding="utf-8"), str(path))


def parse_po_text(text: str, path: str = "<string>") -> list[Entry]:
    """Parse the text of a ``.po`` file (or of a single blank-line separated block)."""
    entries: list[Entry] = []
    blocks = re.split(r"\n\s*\n", text.replace("\r\n", "\n"))
    for block in blocks:
        lines = [line for line in block.split("\n") if line.strip()]
        if not lines:
            continue
        entry = Entry()
        target: tuple[str, int] | None = None
        has_message = False
        for line in lines:
            if line.startswith("#~"):
                entry.obsolete = True
                continue
            if line.startswith("#"):
                entry.comments.append(line)
                continue
            match = _KEYWORD.match(line)
            if match:
                keyword, index, token = match.group(1), match.group(2), match.group(3)
                value = _unquote(token)
                has_message = True
                if keyword == "msgctxt":
                    entry.msgctxt = value
                elif keyword == "msgid":
                    entry.msgid = value
                elif keyword == "msgid_plural":
                    entry.msgid_plural = value
                else:
                    entry.msgstr[int(index or 0)] = value
                target = (keyword, int(index or 0))
            elif line.lstrip().startswith('"') and target is not None:
                value = _unquote(line.strip())
                keyword, position = target
                if keyword == "msgctxt":
                    entry.msgctxt = (entry.msgctxt or "") + value
                elif keyword == "msgid":
                    entry.msgid += value
                elif keyword == "msgid_plural":
                    entry.msgid_plural = (entry.msgid_plural or "") + value
                else:
                    entry.msgstr[position] = entry.msgstr.get(position, "") + value
            else:
                raise ValueError(f"{path}: unparsable line: {line!r}")
        if has_message or entry.obsolete:
            entries.append(entry)
    return entries


def po_path(language: str) -> Path:
    return LOCALE_DIR / language / "LC_MESSAGES" / f"{DOMAIN}.po"


def mo_path(language: str) -> Path:
    return LOCALE_DIR / language / "LC_MESSAGES" / f"{DOMAIN}.mo"


def header_fields(entries: list[Entry]) -> dict[str, str]:
    for entry in entries:
        if entry.is_header and not entry.obsolete:
            fields: dict[str, str] = {}
            for line in entry.msgstr.get(0, "").split("\n"):
                if ":" in line:
                    name, _, value = line.partition(":")
                    fields[name.strip()] = value.strip()
            return fields
    return {}


# ---------------------------------------------------------------------------------------------
# Locked-text cross-check
# ---------------------------------------------------------------------------------------------
def normalise(text: str) -> str:
    text = text.replace("\u2019", "'").replace("\u2018", "'").replace("\u00a0", " ").replace("\u202f", " ")
    return re.sub(r"\s+", " ", text).strip().casefold()


def _flatten(value, prefix: str):
    if isinstance(value, str):
        yield prefix, value
    elif isinstance(value, dict):
        for key, item in value.items():
            yield from _flatten(item, f"{prefix}.{key}")
    elif isinstance(value, (list, tuple)):
        for index, item in enumerate(value):
            yield from _flatten(item, f"{prefix}[{index}]")


def locked_strings() -> list[tuple[str, str]]:
    """Every string of the locked registry, flattened: ``[(key path, normalised text), …]``."""
    from cms import locked_content

    found: list[tuple[str, str]] = []
    for table in locked_content.LOCKED_TEXTS.values():
        for key, value in table.items():
            found.extend((path, normalise(text)) for path, text in _flatten(value, key))
    return found


def _words(text: str) -> list[str]:
    return re.findall(r"[\w'-]+", text)


class LockedIndex:
    """Lookup structure answering « does this msgid carry a fragment of a locked text? »."""

    def __init__(self, strings: list[tuple[str, str]] | None = None) -> None:
        self.strings = strings if strings is not None else locked_strings()
        self.shingles: dict[tuple[str, ...], str] = {}
        for key, text in self.strings:
            words = _words(text)
            for start in range(len(words) - FRAGMENT_SHINGLE_WORDS + 1):
                self.shingles.setdefault(tuple(words[start : start + FRAGMENT_SHINGLE_WORDS]), key)

    def match(self, msgid: str) -> str:
        """Return the locked key a msgid overlaps with, or "" when the msgid is clean."""
        candidate = normalise(msgid)
        if len(candidate) >= FRAGMENT_MIN_CHARS:
            for key, text in self.strings:
                if candidate in text:
                    return key
        for key, text in self.strings:
            if len(text) >= FRAGMENT_MIN_CHARS and text in candidate:
                return key
        words = _words(candidate)
        for start in range(len(words) - FRAGMENT_SHINGLE_WORDS + 1):
            key = self.shingles.get(tuple(words[start : start + FRAGMENT_SHINGLE_WORDS]))
            if key:
                return key
        return ""


# ---------------------------------------------------------------------------------------------
# Audit
# ---------------------------------------------------------------------------------------------
@dataclass
class LanguageReport:
    language: str
    present: bool = True
    total: int = 0
    translated: int = 0
    untranslated: int = 0
    fuzzy: int = 0
    obsolete: int = 0
    plural_entries: int = 0
    nplurals: int = 0
    mo_exists: bool = False
    mo_stale: bool = False
    locked_fragments: list[dict[str, str]] = field(default_factory=list)
    reviewed_overlaps: list[dict[str, str]] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    untranslated_msgids: list[str] = field(default_factory=list)
    missing_from_catalogue: list[dict[str, str]] = field(default_factory=list)
    stale_msgids: list[str] = field(default_factory=list)

    @property
    def coverage(self) -> float:
        return 100.0 if not self.total else round(100.0 * self.translated / self.total, 2)

    @property
    def ok(self) -> bool:
        return (
            self.present
            and self.untranslated == 0
            and self.fuzzy == 0
            and not self.locked_fragments
            and not self.errors
            and self.mo_exists
            and not self.mo_stale
        )

    def as_dict(self) -> dict:
        return {
            "language": self.language,
            "present": self.present,
            "msgids": self.total,
            "translated": self.translated,
            "untranslated": self.untranslated,
            "fuzzy": self.fuzzy,
            "obsolete": self.obsolete,
            "plural_entries": self.plural_entries,
            "nplurals": self.nplurals,
            "coverage": self.coverage,
            "mo_exists": self.mo_exists,
            "mo_stale": self.mo_stale,
            "locked_fragments": self.locked_fragments,
            "reviewed_overlaps": self.reviewed_overlaps,
            "errors": self.errors,
            "untranslated_msgids": self.untranslated_msgids[:50],
            "missing_from_catalogue": self.missing_from_catalogue[:50],
            "stale_msgids": self.stale_msgids[:50],
            "ok": self.ok,
        }


def _placeholders(text: str) -> list[str]:
    return sorted(p for p in _PERCENT.findall(text) if p != "%%") + sorted(_BRACE.findall(text))


def _check_entry(entry: Entry, language: str, report: LanguageReport) -> None:
    from cms import forbidden

    label = entry.msgid[:60].replace("\n", " ")
    sources = [entry.msgid] + ([entry.msgid_plural] if entry.msgid_plural else [])
    allowed_in_plural = set(_placeholders(" ".join(sources)))
    for index, value in sorted(entry.msgstr.items()):
        if not value:
            continue
        got = _placeholders(value)
        if entry.is_plural:
            # A plural form may legitimately drop the number (Arabic « one » / « two » forms).
            if not set(got) <= allowed_in_plural:
                report.errors.append(f"placeholder mismatch in plural [{index}] of « {label} »: {got}")
        else:
            expected = _placeholders(entry.msgid)
            if expected != got:
                report.errors.append(f"placeholder mismatch in « {label} »: expected {expected}, got {got}")
            if sorted(_HTML_TAG.findall(entry.msgid)) != sorted(_HTML_TAG.findall(value)):
                report.errors.append(f"inline HTML differs in « {label} »")
        if _MOJIBAKE.search(value):
            report.errors.append(f"mojibake in the translation of « {label} »")
        if not forbidden.scan(entry.msgid):
            for violation in forbidden.scan(value):
                report.errors.append(f"forbidden formulation ({violation.label}) in the translation of « {label} »")
        if value.endswith("\n") != entry.msgid.endswith("\n") or value.startswith("\n") != entry.msgid.startswith("\n"):
            report.errors.append(f"leading/trailing newline differs in « {label} »")
        if language == "ar":
            if _ARABIC_INDIC_DIGITS.search(value):
                report.errors.append(f"Arabic-Indic digit in « {label} » (the site uses Western digits)")
            keep = KEEP_AS_IS.match(entry.msgid.strip()) or entry.msgid in KEEP_SOURCE
            if not _ARABIC.search(value) and not keep:
                report.errors.append(f"Arabic translation of « {label} » contains no Arabic script")
            if _ARABIC.search(value):  # entries kept in Latin script are rendered by a left-to-right element
                if _TRADEMARK_WITHOUT_LRM.search(value):
                    report.errors.append(f"« ™ » is not followed by U+200E (LRM) in the Arabic « {label} »")
                for placeholder in BRAND_PLACEHOLDERS:
                    if re.search(re.escape(placeholder) + "(?!" + LRM + ")", value):
                        report.errors.append(f"{placeholder} is not followed by U+200E (LRM) in the Arabic « {label} »")


def audit_language(
    language: str,
    nplurals: int,
    index: LockedIndex,
    sources: dict | None = None,
) -> LanguageReport:
    report = LanguageReport(language=language)
    path = po_path(language)
    if not path.exists():
        report.present = False
        report.errors.append(f"missing catalogue {path.relative_to(ROOT)}")
        return report
    entries = parse_po(path)
    fields = header_fields(entries)
    plural_forms = fields.get("Plural-Forms", "")
    match = re.search(r"nplurals\s*=\s*(\d+)", plural_forms)
    report.nplurals = int(match.group(1)) if match else 0
    if report.nplurals != nplurals:
        report.errors.append(f"Plural-Forms declares {report.nplurals} forms, expected {nplurals}")
    if "plural=" not in plural_forms.replace(" ", ""):
        report.errors.append("Plural-Forms header has no plural expression")
    if fields.get("Language", "") != language:
        report.errors.append(f"Language header is {fields.get('Language', '')!r}, expected {language!r}")
    if "charset=UTF-8" not in fields.get("Content-Type", ""):
        report.errors.append("Content-Type charset must be UTF-8")
    seen: set[tuple[str | None, str]] = set()
    for entry in entries:
        if entry.obsolete:
            report.obsolete += 1
            continue
        if entry.is_header:
            if entry.is_fuzzy:
                report.errors.append("the header entry is still flagged fuzzy")
            continue
        report.total += 1
        if (entry.msgctxt, entry.msgid) in seen:
            # GNU msgfmt refuses a duplicate; the pure-Python compiler would silently keep the last one.
            report.errors.append(f"duplicate msgid « {entry.msgid[:60]} »")
        seen.add((entry.msgctxt, entry.msgid))
        if entry.is_plural:
            report.plural_entries += 1
            if set(entry.msgstr) != set(range(nplurals)):
                report.errors.append(f"plural entry « {entry.msgid[:60]} » has indexes {sorted(entry.msgstr)}")
        if entry.is_fuzzy:
            report.fuzzy += 1
        elif entry.is_translated(nplurals):
            report.translated += 1
        else:
            report.untranslated += 1
            report.untranslated_msgids.append(entry.msgid)
        for source in filter(None, (entry.msgid, entry.msgid_plural)):
            key = index.match(source)
            if key:
                item = {"msgid": source, "locked_key": key, "refs": " ".join(entry.references)}
                if entry.msgid in KEEP_SOURCE:
                    expected = [entry.msgid] + [entry.msgid_plural or entry.msgid] * (nplurals - 1)
                    got = [entry.msgstr.get(i, "") for i in range(nplurals if entry.is_plural else 1)]
                    if got != expected[: len(got)]:
                        report.errors.append(f"« {entry.msgid[:60]} » is locked-derived and must keep its French text")
                    report.reviewed_overlaps.append(
                        {**item, "decision": "keep-source", "why": KEEP_SOURCE[entry.msgid]}
                    )
                elif entry.msgid in REVIEWED_OVERLAPS:
                    why = REVIEWED_OVERLAPS[entry.msgid]
                    report.reviewed_overlaps.append({**item, "decision": "reviewed", "why": why})
                else:
                    report.locked_fragments.append(item)
                break
        _check_entry(entry, language, report)
    if language in OPTIONAL_LANGUAGES:
        for msgid in unnormalised_source_msgids(entries):
            report.errors.append(
                f"« {msgid[:60]} » is an Italian-source msgid left untranslated in locale/{language}: "
                "write its French text (the French site would show Italian)"
            )
    compiled = mo_path(language)
    report.mo_exists = compiled.exists()
    if not report.mo_exists:
        report.errors.append(f"missing compiled catalogue {compiled.relative_to(ROOT)}")
    else:
        # Compare CONTENT, not modification times: a fresh checkout gives every file an arbitrary mtime.
        differences = mo_differences(language, entries)
        report.mo_stale = bool(differences)
        if differences:
            report.errors.append(
                f"{compiled.relative_to(ROOT)} does not match its .po ({len(differences)} entries, e.g. "
                f"« {differences[0][:60]} ») — recompile: scripts/i18n_audit.py --compile"
            )
    if sources is not None:
        catalogue = {(e.msgctxt, e.msgid) for e in entries if not e.obsolete and not e.is_header}
        for key in sorted(set(sources) - catalogue, key=lambda k: k[1]):
            origin = sorted(sources[key].files)[0]
            report.missing_from_catalogue.append({"msgid": key[1], "msgctxt": key[0] or "", "source": origin})
        report.stale_msgids = sorted(key[1] for key in catalogue - set(sources))
        if report.missing_from_catalogue:
            first = report.missing_from_catalogue[0]
            report.errors.append(
                f"{len(report.missing_from_catalogue)} source msgid(s) missing from the catalogue, e.g. "
                f"« {first['msgid'][:60]} » ({first['source']}) — add and translate them"
            )
    return report


def unnormalised_source_msgids(entries: list[Entry]) -> list[str]:
    """
    Sentences of the source-language catalogue (``fr``) that were NOT written in French.

    A few back-office strings have an Italian msgid; ``locale/fr`` gives them their French text. ``--sync``
    can only copy a new msgid into ``locale/fr``, so an Italian newcomer would be served in Italian on the
    French site without anybody noticing. Heuristic: a sentence (four words or more) that is identical in the
    French AND in the Italian catalogue was written in Italian — a French sentence never survives the Italian
    translation unchanged. Proper nouns, acronyms and the frozen ``KEEP_SOURCE`` texts are exempt.
    """
    italian_path = po_path("it")
    if not italian_path.exists():
        return []
    italian = {(e.msgctxt, e.msgid): e for e in parse_po(italian_path) if not e.obsolete and not e.is_header}
    found = []
    for entry in entries:
        if entry.obsolete or entry.is_header or entry.msgid in KEEP_SOURCE or KEEP_AS_IS.match(entry.msgid.strip()):
            continue
        twin = italian.get((entry.msgctxt, entry.msgid))
        if twin is None or len(_words(entry.msgid)) < 4:
            continue
        if entry.msgstr.get(0) == entry.msgid == twin.msgstr.get(0):
            found.append(entry.msgid)
    return found


def mo_differences(language: str, entries: list[Entry] | None = None) -> list[str]:
    """msgids whose compiled translation differs from the ``.po`` (empty list = the ``.mo`` is up to date)."""
    import gettext as gettext_module

    entries = entries if entries is not None else parse_po(po_path(language))
    with mo_path(language).open("rb") as handle:
        compiled = gettext_module.GNUTranslations(handle)
    catalogue = compiled._catalog  # noqa: SLF001 - the public API cannot enumerate a catalogue
    expected: dict = {}
    for entry in entries:
        if entry.obsolete or entry.is_header or entry.is_fuzzy or not all(entry.msgstr.values()):
            continue
        msgid = entry.msgid if entry.msgctxt is None else f"{entry.msgctxt}\x04{entry.msgid}"
        if entry.is_plural:
            for index, value in entry.msgstr.items():
                expected[(msgid, index)] = value
        else:
            expected[msgid] = entry.msgstr[0]
    actual = {key: value for key, value in catalogue.items() if key != ""}
    differing = [key for key in expected if actual.get(key) != expected[key]]
    differing += [key for key in actual if key not in expected]
    return [key[0] if isinstance(key, tuple) else key for key in differing]


# ---------------------------------------------------------------------------------------------
# Source extraction (pure Python — GNU xgettext is not required)
# ---------------------------------------------------------------------------------------------
_SOURCE_SKIP_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    "docs",
    "locale",
    "media",
    "node_modules",
    "staticfiles",
    "tests",
    "tmp",
}
_GETTEXT_SINGLE = {"_", "gettext", "gettext_lazy", "gettext_noop"}
_GETTEXT_PLURAL = {"ngettext", "ngettext_lazy"}
_GETTEXT_CONTEXT = {"pgettext", "pgettext_lazy"}
_GETTEXT_CONTEXT_PLURAL = {"npgettext", "npgettext_lazy"}
_PY_STRING = r"""(?:u?'(?:[^'\\]|\\.)*'|u?"(?:[^"\\]|\\.)*")"""
_TEMPLATE_CALL = re.compile(
    r"\b(npgettext|pgettext|ngettext|gettext|_)\(\s*(" + _PY_STRING + r")"
    r"(?:\s*,\s*(" + _PY_STRING + r"))?(?:\s*,\s*(" + _PY_STRING + r"))?"
)


def _constant(node) -> str | None:
    import ast

    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        left, right = _constant(node.left), _constant(node.right)
        if left is not None and right is not None:
            return left + right
    return None


@dataclass
class SourceMessage:
    """A gettext message found in the sources: where it occurs and, for plural calls, its plural msgid."""

    files: set[str] = field(default_factory=set)
    plural: str | None = None


#: ``(msgctxt, msgid, msgid_plural)`` as found in one source file.
_Found = tuple[str | None, str, str | None]


def _messages_in_python(source: str) -> list[_Found]:
    import ast

    found: list[_Found] = []
    for node in ast.walk(ast.parse(source)):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        name = func.id if isinstance(func, ast.Name) else func.attr if isinstance(func, ast.Attribute) else ""
        args = [_constant(arg) for arg in node.args]
        if name in _GETTEXT_SINGLE and args and args[0] is not None:
            found.append((None, args[0], None))
        elif name in _GETTEXT_PLURAL and len(args) >= 2 and None not in args[:2]:
            found.append((None, args[0], args[1]))
        elif name in _GETTEXT_CONTEXT and len(args) >= 2 and None not in args[:2]:
            found.append((args[0], args[1], None))
        elif name in _GETTEXT_CONTEXT_PLURAL and len(args) >= 3 and None not in args[:3]:
            found.append((args[0], args[1], args[2]))
    return found


def _messages_in_template(source: str, origin: str) -> list[_Found]:
    import ast

    from django.utils.translation.template import templatize

    found: list[_Found] = []
    for match in _TEMPLATE_CALL.finditer(templatize(source, origin=origin)):
        args = [ast.literal_eval(token.lstrip("u")) for token in match.groups()[1:] if token]
        name = match.group(1)
        if name == "npgettext":
            found.append((args[0], args[1], args[2]))
        elif name == "pgettext":
            found.append((args[0], args[1], None))
        elif name == "ngettext":
            found.append((None, args[0], args[1]))
        else:
            found.append((None, args[0], None))
    return found


def source_messages(root: Path = ROOT) -> dict[tuple[str | None, str], SourceMessage]:
    """
    Every gettext message of the project sources: ``{(msgctxt, msgid): SourceMessage(files, plural)}``.

    Python files are read with ``ast`` (``_``, ``gettext[_lazy|_noop]``, ``ngettext[_lazy]``, ``pgettext…``);
    templates (``.html`` / ``.txt``) go through Django's own ``templatize`` — the function ``makemessages``
    feeds to xgettext — so ``{% translate %}``, ``{% blocktranslate %}`` (``trimmed``, ``count``, ``context``)
    and ``_("…")`` in variables are recognised exactly as Django recognises them. Messages whose argument is
    not a string literal (``_(CONSTANT)``) cannot be extracted — by xgettext either.
    """
    import os

    found: dict[tuple[str | None, str], SourceMessage] = {}
    for base, dirs, files in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in _SOURCE_SKIP_DIRS)
        for name in sorted(files):
            path = Path(base) / name
            origin = path.relative_to(root).as_posix()
            if name.endswith(".py"):
                messages = _messages_in_python(path.read_text(encoding="utf-8"))
            elif name.endswith((".html", ".txt")) and "templates" in path.parts:
                messages = _messages_in_template(path.read_text(encoding="utf-8"), origin)
            else:
                continue
            for msgctxt, msgid, plural in messages:
                message = found.setdefault((msgctxt, msgid), SourceMessage())
                message.files.add(origin)
                message.plural = message.plural or plural
    return found


def run_audit(check_sources: bool = True) -> list[LanguageReport]:
    index = LockedIndex()
    sources = source_messages() if check_sources else None
    languages = dict(TRANSLATED_LANGUAGES)
    languages.update({lang: n for lang, n in OPTIONAL_LANGUAGES.items() if po_path(lang).exists()})
    return [audit_language(lang, n, index, sources) for lang, n in languages.items()]


# ---------------------------------------------------------------------------------------------
# Catalogue synchronisation (pure-Python stand-in for « makemessages » when GNU gettext is missing)
# ---------------------------------------------------------------------------------------------
def _quote(text: str) -> str:
    escaped = text.replace("\\", "\\\\").replace('"', '\\"').replace("\t", "\\t").replace("\r", "\\r")
    return '"' + escaped.replace("\n", "\\n") + '"'


def _block_key(block: str) -> tuple[str | None, str] | None:
    """``(msgctxt, msgid)`` of one blank-line separated ``.po`` block (None for the header / comments)."""
    parsed = parse_po_text(block)
    if not parsed or parsed[0].is_header or parsed[0].obsolete:
        return None
    return parsed[0].msgctxt, parsed[0].msgid


def sync_catalogue(language: str, nplurals: int, sources: dict | None = None) -> tuple[int, int]:
    """
    Bring ``locale/<language>/…/django.po`` in line with the sources; returns ``(added, removed)``.

    * messages that no longer occur in the sources are dropped (``makemessages`` would mark them obsolete);
    * new messages are appended with their file reference and an EMPTY msgstr — the translator fills them,
      and the audit keeps failing until they do. In the optional ``fr`` catalogue a new message is a French
      source string, so it is its own translation.

    Existing translations are never touched.
    """
    sources = sources if sources is not None else source_messages()
    path = po_path(language)
    blocks = re.split(r"\n\s*\n", path.read_text(encoding="utf-8").replace("\r\n", "\n").strip("\n"))
    kept: list[str] = []
    present: set[tuple[str | None, str]] = set()
    removed = 0
    for block in blocks:
        key = _block_key(block)
        if key is not None and key not in sources:
            removed += 1
            continue
        if key is not None:
            present.add(key)
        kept.append(block)
    added = 0
    for key in sorted(set(sources) - present, key=lambda k: (sorted(sources[k].files)[0], k[1])):
        msgctxt, msgid = key
        message = sources[key]
        lines = ["#: " + " ".join(".\\" + name.replace("/", "\\") for name in sorted(message.files))]
        if msgctxt is not None:
            lines.append(f"msgctxt {_quote(msgctxt)}")
        lines.append(f"msgid {_quote(msgid)}")
        own = language in OPTIONAL_LANGUAGES
        if message.plural is not None:
            lines.append(f"msgid_plural {_quote(message.plural)}")
            for index in range(nplurals):
                value = (msgid if index == 0 else message.plural) if own else ""
                lines.append(f"msgstr[{index}] {_quote(value)}")
        else:
            lines.append(f"msgstr {_quote(msgid if own else '')}")
        kept.append("\n".join(lines))
        added += 1
    if added or removed:
        path.write_text("\n\n".join(kept) + "\n", encoding="utf-8", newline="\n")
    return added, removed


# ---------------------------------------------------------------------------------------------
# Pure-Python .mo writer (fallback for machines without GNU gettext)
# ---------------------------------------------------------------------------------------------
def compile_po(language: str) -> Path:
    """Write ``django.mo`` next to ``django.po`` (same binary layout as GNU msgfmt, no hash table)."""
    messages: dict[bytes, bytes] = {}
    for entry in parse_po(po_path(language)):
        if entry.obsolete or (entry.is_fuzzy and not entry.is_header):
            continue
        if not entry.is_header and not all(entry.msgstr.values()):
            continue
        key = entry.msgid
        if entry.msgid_plural is not None:
            key += "\x00" + entry.msgid_plural
        if entry.msgctxt is not None:
            key = entry.msgctxt + "\x04" + key
        value = "\x00".join(entry.msgstr[i] for i in sorted(entry.msgstr))
        messages[key.encode("utf-8")] = value.encode("utf-8")
    keys = sorted(messages)
    offsets: list[tuple[int, int, int, int]] = []
    ids = strs = b""
    for key in keys:
        offsets.append((len(ids), len(key), len(strs), len(messages[key])))
        ids += key + b"\x00"
        strs += messages[key] + b"\x00"
    keystart = 7 * 4 + 16 * len(keys)
    valuestart = keystart + len(ids)
    koffsets: list[int] = []
    voffsets: list[int] = []
    for o1, l1, o2, l2 in offsets:
        koffsets += [l1, o1 + keystart]
        voffsets += [l2, o2 + valuestart]
    output = struct.pack("Iiiiiii", 0x950412DE, 0, len(keys), 7 * 4, 7 * 4 + len(keys) * 8, 0, 0)
    output += array.array("i", koffsets + voffsets).tobytes() + ids + strs
    target = mo_path(language)
    target.write_bytes(output)
    return target


# ---------------------------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------------------------
def _print_report(reports: list[LanguageReport]) -> None:
    print("i18n audit — locale/<lang>/LC_MESSAGES/django.po")
    print(
        f"{'lang':<5}{'msgids':>8}{'translated':>12}{'untranslated':>14}{'fuzzy':>7}{'obsolete':>10}"
        f"{'plural':>8}{'nplurals':>10}{'coverage':>10}  status"
    )
    for r in reports:
        print(
            f"{r.language:<5}{r.total:>8}{r.translated:>12}{r.untranslated:>14}{r.fuzzy:>7}{r.obsolete:>10}"
            f"{r.plural_entries:>8}{r.nplurals:>10}{r.coverage:>9}%  {'OK' if r.ok else 'FAIL'}"
        )
    for r in reports:
        for item in r.locked_fragments:
            print(f"[{r.language}] LOCKED FRAGMENT ({item['locked_key']}): {item['msgid'][:90]!r}  {item['refs']}")
        for error in r.errors:
            print(f"[{r.language}] ERROR: {error}")
        if r is reports[0]:
            for item in r.reviewed_overlaps:
                print(
                    f"[all] {item['decision']} overlap ({item['locked_key']}): {item['msgid'][:70]!r} — {item['why']}"
                )
        for msgid in r.untranslated_msgids[:20]:
            print(f"[{r.language}] UNTRANSLATED: {msgid[:90]!r}")
        if len(r.untranslated_msgids) > 20:
            print(f"[{r.language}] … and {len(r.untranslated_msgids) - 20} more untranslated msgids")
        if r is reports[0]:
            for item in r.missing_from_catalogue[:40]:
                print(f"[all] MISSING FROM CATALOGUE: {item['msgid'][:90]!r}  {item['source']}")
            if r.stale_msgids:
                print(
                    f"[all] note: {len(r.stale_msgids)} catalogue msgid(s) no longer occur in the sources "
                    f"(harmless; e.g. {r.stale_msgids[0][:60]!r})"
                )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit the gettext catalogues of Italy Legal Entry.")
    parser.add_argument("--json", action="store_true", help="print the report as JSON")
    parser.add_argument("--compile", action="store_true", help="write the .mo files in pure Python, then audit")
    parser.add_argument(
        "--sync",
        action="store_true",
        help="add the source messages missing from the catalogues (empty msgstr) and drop the unused ones",
    )
    parser.add_argument(
        "--no-sources",
        action="store_true",
        help="skip the source scan (catalogue ↔ templates/Python synchronisation check)",
    )
    args = parser.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if args.sync:
        sources = source_messages()
        for language, nplurals in {**TRANSLATED_LANGUAGES, **OPTIONAL_LANGUAGES}.items():
            if po_path(language).exists():
                added, removed = sync_catalogue(language, nplurals, sources)
                print(f"synchronised {po_path(language).relative_to(ROOT)}: +{added} -{removed}", file=sys.stderr)
    if args.compile:
        for language in [*TRANSLATED_LANGUAGES, *OPTIONAL_LANGUAGES]:
            if po_path(language).exists():
                print(f"compiled {compile_po(language).relative_to(ROOT)}", file=sys.stderr)
    reports = run_audit(check_sources=not args.no_sources)
    if args.json:
        payload = {"ok": all(r.ok for r in reports), "languages": [r.as_dict() for r in reports]}
        print(json.dumps(payload, ensure_ascii=False, indent=1))
    else:
        _print_report(reports)
    return 0 if all(r.ok for r in reports) else 1


if __name__ == "__main__":
    raise SystemExit(main())
