"""
The research archive — what the preview was until V5.4, and how it finds what it shows.

Since the owner's directive V5.4 (4 October 2026) ``/__design-v5/`` opens the live V5 product
(designpreview.live); the catalogue below moved, as it was, to ``/__design-v5/research/``, with the
pickers, the compare view and the proof files under it (V5.4 plan §4.2). Its «prototipo di ricerca —
non approvato» labels are kept. One group left it (§4.3): «Baseline V4 (controllo)», which linked
this server's own pages as the V4 control — false the moment V5 enters the templates; the V4
control is on 8771, and the index compares with it there.

Five things live here and nowhere else:

1. **The catalogue** (``catalogue()``): the first screens — the five the hero council examined,
   then H-E, the direction the owner authorised on 2 October, with its measurement pages, and
   the council's record — every other surface of gate 0 «La prova» in the order the owner is
   asked to look at them (proof/index.html, SIGNING_SHEET.md §1.2), then the research
   prototypes of waves 1, 2 and 3 (proof/research/), each with its one-line note and its links.
   A link is a proof file, a proof file with the query string that puts a prototype in one of
   its states, or an entry of a picker or of the compare view; every one that stands on a file
   is resolved against the proof directory **at render time, on every
   request**, so something that is not on disk is shown as «manca» instead of a dead link, and
   becomes a link by itself the moment the file is there. A folder may be announced before it
   is built (``IN_CONSTRUCTION``): H-E was, until its build reached the disk on 4 October 2026;
   none is today. A surface may also name files this server does not serve (``Reference``):
   the council's minutes and sheets, printed as paths.

2. **The hero picker table** (``HERO_VARIANTS``, ``hero_picker()``): which file answers
   ``?variant=h0|ha|hb|hc|hd|he|e1|e2|e3&lang=fr|ar&phase=3|interim``. H-A and H-B exist in
   Arabic only for phase 3; the research directions H-C, H-D and H-E were built for phase 3
   alone, and the three concept frames of H-E (E1–E3) in French only; that absence is a fact of
   the package, and the picker says so in its bar rather than falling back to a different comp.

3. **The type picker table** (``TYPE_SYSTEMS``, ``TYPE_SURFACES``, ``type_picker()``): the same
   for ``?system=v4|a|a2|ap|b|c|d&surface=home|menu|dashboard|documents|case&lang=fr|ar`` — the
   typography research's override sheets on the gate-0 pages. Arabic exists for the home and the
   dashboard only. Both pickers are one builder (``_frame()``) over a table of three choices, so
   they cannot drift apart: the same bar, the same answers to what does not exist.

4. **Proof serving** (``resolve_proof_file()``): a path under the proof directory, served only if
   its **real** path — the name the file system opens, not the string the request carried — is
   inside the root, has no dotted or tilde'd component (``.work``, ``.profiles``, ``.ecd``,
   ``.git-…`` and their NTFS 8.3 aliases ``WORK~1``, ``GIT-ST~1.TXT``; a symbolic link or junction
   is judged by what it points at) and has an extension in ``PROOF_CONTENT_TYPES``. The content
   type is written here, not guessed: ``mimetypes`` on this Windows machine reads the registry,
   and the registry says what some installer last wrote (``.js`` as text/plain breaks an ES
   module; ``.woff2`` is unknown).

5. **The compare view table** (``COMPARISONS``, ``compare_view()``): two proof pages of one
   surface framed side by side at the same phone width, each scrolling on its own — today the
   two phone versions of «Mes pièces» (research consolidation K5). The two are named by their
   authors' roles and stand in the order they arrived, never in an order of preference; their
   pages come from the table, never from the query.

Nothing the preview shows is approved, and the two pickers say so about whatever they frame: the
status of a candidate (``STATUS_GATE0``, ``STATUS_RESEARCH``) is written once, here, and a bar
draws it at every window width — in full from 48 rem, in its closing words (``short_status()``)
below; the compare view writes it in the caption of each frame. Of the first screens the hub
says what each one is and what it asks of the rules; it does not rank one against another — in
its own voice or in the council's (review W2-2): the hub is the page the owner decides O67 on,
and the order the council's chairs gave is three 3–2 comparisons and a fourth place with no
majority. That order stands in the minutes, with its reservations; the hub prints the path to
the minutes, not the order. Nor does it carry a builder's recommendation of one candidate over
another, or an adjective of merit: what a prototype is, what it asks of the rules, who has
looked at it and who decides. Where it offers a prototype's ``?rm=1`` and the prototype leaves
the duration tokens of gate 0 alone, it says that the flag is not yet the reduced-motion state
(research consolidation X-4; MOTION_SYSTEM.md MS7, open in the gate-0 foundation).
"""

from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from django.core.exceptions import SuspiciousFileOperation
from django.http import Http404
from django.urls import reverse
from django.utils._os import safe_join

# ---------------------------------------------------------------------------------------------
# Proof serving
# ---------------------------------------------------------------------------------------------

#: Extension → Content-Type. Anything not listed is not served (404), which covers .py, .pyc,
#: .ps1, .sh, .log, .gz, .jsonl and every other working file of the council's tools.
PROOF_CONTENT_TYPES: dict[str, str] = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "text/javascript; charset=utf-8",
    ".mjs": "text/javascript; charset=utf-8",
    ".svg": "image/svg+xml",
    ".woff2": "font/woff2",
    ".woff": "font/woff",
    ".webp": "image/webp",
    ".avif": "image/avif",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".ico": "image/x-icon",
    ".json": "application/json; charset=utf-8",
    ".md": "text/plain; charset=utf-8",
    ".txt": "text/plain; charset=utf-8",
    ".csv": "text/csv; charset=utf-8",
    ".webm": "video/webm",
    ".mp4": "video/mp4",
}


def resolve_proof_file(root: Path, raw: str) -> tuple[Path, str]:
    """
    The file ``raw`` names under ``root`` — its real path — with its content type, or ``Http404``.

    Two layers, because the string of a request is not the name of a file. The first judges the
    string: no backslash, NUL, empty segment, dotted segment, drive letter or tilde. The second
    (``real_proof_path``) judges what the file system actually opens for that string, which on
    NTFS can be a dotted folder reached through its 8.3 alias, or the target of a link.

    404 for everything refused, never 403: a 403 would confirm that the thing exists, and the
    project's rule (docs/SECURITY.md) is that a caller who may not see something is told nothing.
    """
    segments, suffix, content_type = refuse_proof_string(raw)
    try:
        full = Path(safe_join(str(root), *segments))
    except (SuspiciousFileOperation, ValueError) as exc:
        raise Http404 from exc
    if not full.is_file():
        raise Http404
    return real_proof_path(root, full, suffix), content_type


def refuse_proof_string(raw: str) -> tuple[list[str], str, str]:
    """
    The first layer of ``resolve_proof_file``, on its own: the string of a request judged as a
    string — its segments, its suffix and its content type, or ``Http404``. The archive's old
    ``/proof/…`` addresses are judged by it before they are redirected, so a redirect is never
    broader than the page it names.
    """
    if not raw or "\\" in raw or "\x00" in raw:
        raise Http404
    segments = raw.split("/")
    for segment in segments:
        # "" refuses "//" and a trailing slash (a directory is never listed); "." refuses the
        # dotted working folders and ".." before safe_join even sees them; ":" refuses a Windows
        # drive letter in the middle of a path; "~" refuses an 8.3 alias by its shape (WORK~1,
        # GIT-ST~1.TXT) — no file of the proof package carries a tilde.
        if segment == "" or segment.startswith(".") or ":" in segment or "~" in segment:
            raise Http404
    suffix = PurePosixPath(raw).suffix.lower()
    content_type = PROOF_CONTENT_TYPES.get(suffix)
    if content_type is None:
        raise Http404
    return segments, suffix, content_type


def real_proof_path(root: Path, full: Path, suffix: str) -> Path:
    """
    The real path of the existing file ``full`` — or ``Http404`` unless that real path lies under
    ``root``, has no component starting with a dot or containing a tilde, and ends in ``suffix``.

    ``safe_join`` reasons about strings; the file system does not. On NTFS every long name also
    answers to an 8.3 alias — ``WORK~1`` opens ``.work``, ``GIT-ST~1.TXT`` opens
    ``.git-status-after.txt`` — and a symbolic link or a junction opens whatever it points at, so
    a string with no dot in it can still land in a working folder, or outside the root. The
    answer is to ask the file system for the final, long name (``resolve(strict=True)``) and to
    make every check again on that. The suffix is compared too: the real file is what gets sent,
    so its extension, not the request's, must be the one in ``PROOF_CONTENT_TYPES``.
    """
    try:
        real = full.resolve(strict=True)
        relative = real.relative_to(root.resolve(strict=True))
    except (OSError, ValueError) as exc:
        raise Http404 from exc
    if any(part.startswith(".") or "~" in part for part in relative.parts):
        raise Http404
    if relative.suffix.lower() != suffix:
        raise Http404
    return real


def proof_exists(root: Path, relative: str) -> bool:
    try:
        resolve_proof_file(root, relative)
    except Http404:
        return False
    return True


def proof_url(relative: str) -> str:
    return reverse("designpreview:proof", kwargs={"path": relative})


# ---------------------------------------------------------------------------------------------
# The standalone documents' stylesheets
# ---------------------------------------------------------------------------------------------

#: A layer of main.css a standalone preview document loads: the fonts and the tokens, never a
#: partial (``_legacy-tokens.css`` is the retired system's shim) and never a layer that styles
#: elements — base.css hides every iframe, by policy, and these documents hold frames.
_TOKEN_LAYER = re.compile(r"^(?:[\w-]+/)*(?:fonts|tokens|aliases)\.css$")


def token_stylesheets() -> list[str]:
    """
    The font and token layers of the site, in the order ``static/css/main.css`` imports them, as
    paths for ``{% static %}`` — read from main.css itself, so that when the foundation replaces its
    fonts and tokens (V5.4 W1-A) the picker pages, the compare view, the landing and the index follow
    without an edit. Read on every call: a lane that rebuilds is seen at the next request. Only
    layers that exist are returned.
    """
    from django.contrib.staticfiles import finders

    main = finders.find("css/main.css")
    if not main:
        return []
    text = Path(main).read_bytes().decode("utf-8")
    sheets = []
    for imported in re.findall(r'@import\s+url\("([^"]+)"\)', text):
        name = imported.split("?", 1)[0]
        if _TOKEN_LAYER.match(name) and finders.find(f"css/{name}"):
            sheets.append(f"css/{name}")
    return sheets


# ---------------------------------------------------------------------------------------------
# The two pickers — what they share
# ---------------------------------------------------------------------------------------------

LANGS: dict[str, str] = {"fr": "Français", "ar": "العربية"}
#: The widths the owner is asked to review at (V5.1 §88); a picker draws the frame at one of them.
WIDTHS: tuple[int, ...] = (1440, 1280, 1024, 768, 430, 390, 375, 360)
_WIDTH_OF: dict[str, int] = {str(width): width for width in WIDTHS}

#: What a framed candidate is. Nothing the preview shows is approved; the hub and the bars say it
#: in these words.
STATUS_GATE0 = "maquette del gate 0 — non approvata"
STATUS_RESEARCH = "prototipo di ricerca — non approvato"
STATUS_CONTROL = "controllo — non una proposta"
#: Every /ar/ page of phase 3 carries the locked copy as 8771 serves it: in French (review F4).
NOT_SIGNABLE_AR = "da non firmare come /ar/"
#: The Arabic pages of the package are drawn in provisional faces that no Moroccan reader has read.
ARABIC_FACES = "Caratteri arabi provvisori: manca la lettura di un lettore marocchino (O10)."


def short_status(status: str) -> str:
    """
    A status in its closing words — «non approvata», «non approvato», «non una proposta».

    Below 48 rem the bar has no room for its second line, and the status must still be drawn
    (review W1-2): these are the words it keeps. They are cut from the status itself, so the two
    cannot say different things.
    """
    return status.rpartition(" — ")[2]


#: One choice of a group of the bar: (query value, label, name for the tooltip, key, hreflang).
#: The key is what static/js/dev/designpreview.js listens to; a choice may have none.
Choice = tuple[str, str, str, str, str]
_LANG_CHOICES: list[Choice] = [("fr", "fr", LANGS["fr"], "f", "fr"), ("ar", "ar", LANGS["ar"], "r", "ar")]


class UnknownChoice(ValueError):
    """A query value a picker does not know — answered 400 by the view."""


@dataclass(frozen=True)
class _Table:
    """What makes a picker of three choices: how a combination is named, its file, its link."""

    here: Callable[[str, str, str], str]
    file: Callable[[str, str, str], str]  #: proof-relative, or "" for a combination that was never built
    url: Callable[..., str]  #: (first, second, third, width) → the picker's URL


def _picker_url(name: str, pairs: tuple[tuple[str, str], ...], width: int) -> str:
    query = "&".join(f"{key}={value}" for key, value in pairs)
    if width:
        query += f"&w={width}"
    return f"{reverse(name)}?{query}"


def _option(label: str, url: str, **more) -> dict:
    return {"label": label, "url": url, "key": "", "current": False, "off": False, "title": "", "lang": "", **more}


def _options(
    root: Path, table: _Table, state: tuple[str, str, str], index: int, choices: list[Choice], width: int
) -> list[dict]:
    """
    The links of one group: the current combination with its ``index``-th value replaced by each
    choice in turn. A choice with no file behind it — never built, or not on disk — is ``off``: it
    stays a link and keeps its key, struck through, because the page it opens is the one that
    says what is missing.
    """
    options = []
    for value, label, name, key, lang in choices:
        target = (*state[:index], value, *state[index + 1 :])
        file = table.file(*target)
        off = not (file and proof_exists(root, file))
        title = f"{name} — tasto {key}" if key else name
        if off:
            title += f" · {table.here(*target)} non c’è"
        options.append(
            _option(
                label,
                table.url(*target, width),
                key=key,
                current=value == state[index],
                off=off,
                title=title,
                lang=lang,
            )
        )
    return options


def _frame(
    root: Path,
    table: _Table,
    state: tuple[str, str, str],
    raw_width: str,
    *,
    picker_name: str,
    title: str,
    groups: list[tuple[str, str, str, list[Choice]]],
    code: str,
    name: str,
    status: str,
    absence: str,
    caution: tuple[str, str] = ("", ""),
    dense: bool = False,
    long: bool = False,
) -> dict:
    """
    What frame.html draws for one combination: the bar and the stage.

    ``groups`` are (slot, label, aria-label, choices), in the order of ``state``; the slot is where
    a group goes in the bar of a narrow window (below 48 rem): the ``main`` choice and the ``lang``
    beside the way back, the ``rest`` on the second row. A combination with nothing to frame — not
    in the table (``absence`` says what exists instead), or in the table and not on disk — comes
    back with ``frame_url`` empty, a ``message`` the stage prints in place of the iframe, and the
    same fact said in the bar. ``caution`` is (the sentence, its few words for the narrow bar):
    what the owner must know about a combination that IS framed.

    The bar says the status twice, for two widths: ``status`` in full on its second line, and
    ``status_short`` — always, warning or no warning — in the flag that replaces that line below
    48 rem, followed by the few words of the warning (``flag``) when there is one.

    ``dense`` and ``long`` are what the stylesheet needs to know about the bar below 48 rem:
    ``dense`` — the group of the second row fills it, so the flag is a row of its own (the type
    picker's five surfaces); ``long`` — the ``main`` group does not fit beside the language, so it
    is a row of its own (the hero picker's nine first screens).
    """
    # One of WIDTHS, or 0 (the full window) for anything else: looked up, never converted, so that
    # «²» or five thousand digits are an unknown width and not an exception.
    width = _WIDTH_OF.get(raw_width, 0)
    here = table.here(*state)
    file, message, (warning, flag) = table.file(*state), "", caution
    if not file:
        message = absence
        warning, flag = f"{here}: questa combinazione non esiste.", "combinazione inesistente"
    elif not proof_exists(root, file):
        message = f"Il file {file} non è nella cartella delle prove ({root})."
        warning, flag = f"{here}: il file manca nella cartella delle prove.", "il file manca"
        file = ""
    return {
        "picker_name": picker_name,
        "title": title,
        "frame_url": proof_url(file) if file else "",
        "stage_class": f"dp-stage--w{width}" if width else "",
        "stage_code": here,
        "message": message,
        "bar": {
            "dense": dense,
            "long": long,
            "groups": [
                {
                    "slot": slot,
                    "label": label,
                    "aria": aria,
                    "options": _options(root, table, state, index, choices, width),
                }
                for index, (slot, label, aria, choices) in enumerate(groups)
            ],
            "widths": [
                _option("piena", table.url(*state, 0), current=not width, title="La larghezza della finestra"),
                *(_option(str(w), table.url(*state, w), current=w == width) for w in WIDTHS),
            ],
            "code": code,
            "name": name,
            "status": status,
            "status_short": short_status(status),
            "warning": warning,
            "flag": flag,
        },
    }


# ---------------------------------------------------------------------------------------------
# The hero picker
# ---------------------------------------------------------------------------------------------

PHASES: dict[str, str] = {"3": "fase 3", "interim": "intérim"}
_PHASE_CHOICES: list[Choice] = [("3", "fase 3", "fase 3", "3", ""), ("interim", "intérim", "intérim", "i", "")]


@dataclass(frozen=True)
class HeroVariant:
    key: str
    label: str
    name: str
    shortcut: str
    #: (lang, phase) → proof-relative file. A combination that is not here does not exist.
    files: dict[tuple[str, str], str]
    #: A research direction (proof/research/hero/), not a comp of the gate-0 package.
    research: bool = False

    @property
    def status(self) -> str:
        return STATUS_RESEARCH if self.research else STATUS_GATE0


HERO_VARIANTS: dict[str, HeroVariant] = {
    "h0": HeroVariant(
        "h0",
        "H-0",
        "La maquette attuale",
        "0",
        {
            ("fr", "3"): "home/phase3.html",
            ("ar", "3"): "home/phase3-ar.html",
            ("fr", "interim"): "home/interim.html",
            ("ar", "interim"): "home/interim-ar.html",
        },
    ),
    "ha": HeroVariant(
        "ha",
        "H-A",
        "La porta, piena",
        "a",
        {
            ("fr", "3"): "home/options/ha-phase3.html",
            ("ar", "3"): "home/options/ha-phase3-ar.html",
            ("fr", "interim"): "home/options/ha-interim.html",
        },
    ),
    "hb": HeroVariant(
        "hb",
        "H-B",
        "Il pilastro e la soglia",
        "b",
        {
            ("fr", "3"): "home/options/hb-phase3.html",
            ("ar", "3"): "home/options/hb-phase3-ar.html",
            ("fr", "interim"): "home/options/hb-interim.html",
        },
    ),
    "hc": HeroVariant(
        "hc",
        "H-C",
        "Quattro soglie, una chiave",
        "c",
        {
            ("fr", "3"): "research/hero/hc/index.html",
            ("ar", "3"): "research/hero/hc/ar.html",
        },
        research=True,
    ),
    "hd": HeroVariant(
        "hd",
        "H-D",
        "La porta, di giorno",
        "d",
        {
            ("fr", "3"): "research/hero/hd/index.html",
            ("ar", "3"): "research/hero/hd/ar.html",
        },
        research=True,
    ),
    # H-E, the direction the owner authorised on 2 October 2026, and its three concept frames.
    # They were announced before they were built, until their files reached the disk on 4 October
    # 2026; the currency test now holds those files like every other catalogued file. Like any
    # choice of the bar, until its file is in the proof directory it is struck through and its
    # page says what is missing. The concepts have no key: 1 and 2 are free in this bar, 3 is the
    # phase's, and two keys out of three would be worse than none.
    "he": HeroVariant(
        "he",
        "H-E",
        "Nuova direzione",
        "e",
        {
            ("fr", "3"): "research/hero/he/index.html",
            ("ar", "3"): "research/hero/he/ar.html",
        },
        research=True,
    ),
    **{
        f"e{n}": HeroVariant(
            f"e{n}",
            f"E{n}",
            f"Concetto H-E {n}",
            "",
            {("fr", "3"): f"research/hero/he/concepts/e{n}/index.html"},
            research=True,
        )
        for n in (1, 2, 3)
    },
}

#: Proof folders the catalogue announces before they are complete. A file under one of them may
#: be missing — the hub prints «manca», the bar strikes the choice through — and is linked by
#: itself once it is on disk: every link is resolved on every request. Everything else the
#: catalogue names must exist (tests/frontend/test_design_preview.py holds both halves). H-E's
#: folder stood here from 2 October until its build reached the disk on 4 October 2026: its six
#: files are now held like every other file. Nothing is announced before it is built today.
IN_CONSTRUCTION: tuple[str, ...] = ()


def hero_file(variant: str, lang: str, phase: str) -> str:
    """The proof-relative page of a (variant, lang, phase) — empty for a combination that was never built."""
    return HERO_VARIANTS[variant].files.get((lang, phase), "")


def hero_url(variant: str, lang: str = "fr", phase: str = "3", width: int = 0) -> str:
    return _picker_url("designpreview:hero", (("variant", variant), ("lang", lang), ("phase", phase)), width)


_HERO = _Table(
    here=lambda variant, lang, phase: f"{HERO_VARIANTS[variant].label} · {lang} · {PHASES[phase]}",
    file=hero_file,
    url=hero_url,
)


def hero_picker(root: Path, variant: str, lang: str, phase: str, width: str) -> dict:
    """
    ``?variant=…&lang=…&phase=…&w=…`` resolved into what frame.html draws. Unknown values raise
    ``UnknownChoice``; a known combination that does not exist is answered, and says so.
    """
    if variant not in HERO_VARIANTS:
        raise UnknownChoice(f"variant={variant!r}")
    if lang not in LANGS:
        raise UnknownChoice(f"lang={lang!r}")
    if phase not in PHASES:
        raise UnknownChoice(f"phase={phase!r}")
    chosen = HERO_VARIANTS[variant]
    built = ", ".join(f"{a_lang} · {PHASES[a_phase]}" for a_lang, a_phase in chosen.files)
    if chosen.research:
        absence = (
            f"Questa combinazione non esiste: {chosen.label} è un prototipo di ricerca, costruito soltanto in {built}."
        )
    else:
        absence = f"Questa combinazione non è nel pacchetto del gate 0: {chosen.label} esiste in {built}."
    caution = ("", "")
    if (lang, phase) == ("ar", "3"):
        caution = (
            f"ar · fase 3: la pagina porta la copia bloccata NON tradotta — {NOT_SIGNABLE_AR}.",
            NOT_SIGNABLE_AR,
        )
    return _frame(
        root,
        _HERO,
        (variant, lang, phase),
        width,
        picker_name="Selettore del primo schermo",
        title=f"{chosen.label} — {LANGS[lang]}, {PHASES[phase]}",
        groups=[
            (
                "main",
                "Primo schermo",
                "Variante del primo schermo",
                [(item.key, item.label, item.name, item.shortcut, "") for item in HERO_VARIANTS.values()],
            ),
            ("lang", "Lingua", "Lingua", _LANG_CHOICES),
            ("rest", "Fase", "Fase", _PHASE_CHOICES),
        ],
        code=chosen.label,
        name=chosen.name,
        status=chosen.status,
        absence=absence,
        caution=caution,
        long=True,
    )


# ---------------------------------------------------------------------------------------------
# The type picker
# ---------------------------------------------------------------------------------------------


@dataclass(frozen=True)
class TypeSystem:
    """One override sheet of the typography research (proof/research/type/<folder>/type.css)."""

    key: str
    folder: str
    label: str
    name: str
    faces: str  #: the families, as the bar prints them beside the name
    remark: str  #: what the sheet is, in the research's own words (type/index.html), for the hub
    shortcut: str
    status: str = STATUS_RESEARCH

    @property
    def code(self) -> str:
        """«TYPE A» for the four systems; the bare label for the control, the variant, the experiment."""
        return f"TYPE {self.label}" if self.key in {"a", "b", "c", "d"} else self.label


TYPE_SYSTEMS: dict[str, TypeSystem] = {
    "v4": TypeSystem(
        "v4",
        "V4",
        "V4",
        "Il controllo",
        "Newsreader 300 + IBM Plex Sans",
        "I caratteri di oggi sulle pagine V5: il termine di confronto, non una proposta.",
        "v",
        STATUS_CONTROL,
    ),
    "a": TypeSystem(
        "a",
        "A",
        "A",
        "Fournier e la console",
        "Source Serif 4 + Host Grotesk",
        "Il sistema del gate 0, invariato: un serif da titolo sul portico, un grottesco per tutto il resto.",
        "a",
    ),
    "a2": TypeSystem(
        "a2",
        "A2",
        "A-bis",
        "Variante: il serif del marchio",
        "Newsreader Display + Host Grotesk",
        "TYPE A con il serif del marchio al posto di Source Serif 4. Non è un sistema, e cambia soltanto le "
        "pagine pubbliche.",
        "s",
    ),
    "ap": TypeSystem(
        "ap",
        "Ap",
        "A+",
        "Esperimento: la console un passo più grande",
        "Source Serif 4 + Host Grotesk",
        "TYPE A con il testo della console un passo più grande sotto 48 rem. Non è un sistema: si guarda a "
        "larghezza telefono.",
        "p",
    ),
    "b": TypeSystem(
        "b", "B", "B", "Una voce", "solo Host Grotesk", "Una sola famiglia: l’unico serif della pagina è il nome.", "b"
    ),
    "c": TypeSystem(
        "c",
        "C",
        "C",
        "Vignelli",
        "Bodoni Moda + Hanken Grotesk",
        "Il Bodoni su due righe soltanto, la promessa e il titolo di pagina; tutto il resto in Hanken Grotesk.",
        "c",
    ),
    "d": TypeSystem(
        "d",
        "D",
        "D",
        "La firma",
        "Newsreader Display + Public Sans",
        "Il serif del nome nel suo taglio display, e un sans civico.",
        "d",
    ),
}


@dataclass(frozen=True)
class TypeSurface:
    key: str
    label: str
    shortcut: str
    arabic: bool = False  #: the research built an Arabic page of this surface


TYPE_SURFACES: dict[str, TypeSurface] = {
    "home": TypeSurface("home", "home", "1", arabic=True),
    "menu": TypeSurface("menu", "menu", "2"),
    "dashboard": TypeSurface("dashboard", "cruscotto", "3", arabic=True),
    "documents": TypeSurface("documents", "documenti", "4"),
    "case": TypeSurface("case", "fascicolo", "5"),
}


def type_file(system: str, surface: str, lang: str) -> str:
    """The proof-relative page of a (system, surface, lang) — empty where the research built none."""
    if lang == "ar" and not TYPE_SURFACES[surface].arabic:
        return ""
    suffix = "-ar" if lang == "ar" else ""
    return f"research/type/{TYPE_SYSTEMS[system].folder}/{surface}{suffix}.html"


def type_url(system: str, surface: str = "home", lang: str = "fr", width: int = 0) -> str:
    return _picker_url("designpreview:type", (("system", system), ("surface", surface), ("lang", lang)), width)


_TYPE = _Table(
    here=lambda system, surface, lang: f"{TYPE_SYSTEMS[system].label} · {TYPE_SURFACES[surface].label} · {lang}",
    file=type_file,
    url=type_url,
)


def type_picker(root: Path, system: str, surface: str, lang: str, width: str) -> dict:
    """``?system=…&surface=…&lang=…&w=…`` resolved into what frame.html draws — built like ``hero_picker``."""
    if system not in TYPE_SYSTEMS:
        raise UnknownChoice(f"system={system!r}")
    if surface not in TYPE_SURFACES:
        raise UnknownChoice(f"surface={surface!r}")
    if lang not in LANGS:
        raise UnknownChoice(f"lang={lang!r}")
    chosen = TYPE_SYSTEMS[system]
    caution = ("", "")
    if lang == "ar":
        sentence = ARABIC_FACES
        if surface == "home":
            sentence += " La home araba è quella dell’intérim."
        caution = (sentence, "caratteri arabi provvisori (O10)")
    return _frame(
        root,
        _TYPE,
        (system, surface, lang),
        width,
        picker_name="Selettore tipografico",
        title=f"{chosen.code} — {TYPE_SURFACES[surface].label}, {LANGS[lang]}",
        groups=[
            (
                "main",
                "Sistema",
                "Sistema tipografico",
                [
                    (item.key, item.label, f"{item.code} · {item.name}", item.shortcut, "")
                    for item in TYPE_SYSTEMS.values()
                ],
            ),
            (
                "rest",
                "Superficie",
                "Superficie",
                [(item.key, item.label, item.label, item.shortcut, "") for item in TYPE_SURFACES.values()],
            ),
            ("lang", "Lingua", "Lingua", _LANG_CHOICES),
        ],
        code=chosen.code,
        name=f"{chosen.name} — {chosen.faces}",
        status=chosen.status,
        absence=(
            "Questa combinazione non esiste: la ricerca tipografica ha costruito in arabo soltanto la home e il "
            "cruscotto."
        ),
        caution=caution,
        dense=True,
    )


# ---------------------------------------------------------------------------------------------
# The compare view
# ---------------------------------------------------------------------------------------------


@dataclass(frozen=True)
class Side:
    """One of the two prototypes a comparison frames."""

    author: str  #: who made it, by role — the words of its frame's caption
    wave: str  #: when it reached the hub: the one reason for its place, first or second
    files: dict[str, str]  #: lang → proof-relative page, for every language of LANGS (a test holds it)


@dataclass(frozen=True)
class Comparison:
    """
    Two proof pages of one surface framed at the same width — ``width`` CSS pixels, drawn by the
    stylesheet: side by side from 54 rem, one under the other below — each in a frame of its own,
    and so with a scroll of its own.

    ``sides`` stand in the order the two reached the hub, and the view says so: an order of
    arrival, never one of preference. Nothing here says which one is the candidate.
    """

    key: str
    code: str  #: the entry of the research consolidation it answers
    title: str
    width: int
    sides: tuple[Side, Side]


COMPARISONS: dict[str, Comparison] = {
    # Research consolidation K5 (RESEARCH_SYNTHESIS_V52.md §3): «Mes pièces» on a phone, twice —
    # the platform audit's proposal, on the hub since wave 2, and the documents lane's, wave 3.
    "mes-pieces": Comparison(
        "mes-pieces",
        "K5",
        "«Mes pièces» su telefono",
        390,
        (
            Side(
                "La proposta dell’audit UI-UX-Pro-Max della piattaforma",
                "seconda ondata",
                {"fr": "research/uiux-platform/proto/docs-fr.html", "ar": "research/uiux-platform/proto/docs-ar.html"},
            ),
            Side(
                "La proposta dello specialista dello spazio documenti",
                "terza ondata",
                {"fr": "research/documents/index.html", "ar": "research/documents/ar.html"},
            ),
        ),
    ),
}


def compare_url(pair: str, lang: str = "fr") -> str:
    return _picker_url("designpreview:compare", (("pair", pair), ("lang", lang)), 0)


def compare_files(pair: str, lang: str) -> tuple[str, ...]:
    """The proof-relative pages a comparison frames in ``lang``, from left to right."""
    return tuple(side.files[lang] for side in COMPARISONS[pair].sides)


def compare_view(root: Path, pair: str, lang: str) -> dict:
    """
    ``?pair=…&lang=…`` resolved into what compare.html draws: the bar — the way back, the language
    (a choice whose two pages are not both on disk is struck through, and still a link), the line
    that says what is compared and in what order — and one frame per side, or, where its page is
    not on disk, the sentence that says so. Unknown values raise ``UnknownChoice``: the pages come
    from ``COMPARISONS`` alone, never from the query, so no value can lead anywhere else.
    """
    if pair not in COMPARISONS:
        raise UnknownChoice(f"pair={pair!r}")
    if lang not in LANGS:
        raise UnknownChoice(f"lang={lang!r}")
    comparison = COMPARISONS[pair]
    frames = []
    for side in comparison.sides:
        file = side.files[lang]
        present = proof_exists(root, file)
        frames.append(
            {
                "author": side.author,
                "wave": side.wave,
                "url": proof_url(file) if present else "",
                "message": "" if present else f"Il file {file} non è nella cartella delle prove ({root}).",
            }
        )
    options = []
    for value, label, name, key, hreflang in _LANG_CHOICES:
        off = not all(proof_exists(root, file) for file in compare_files(pair, value))
        title = f"{name} — tasto {key}"
        if off:
            title += f" · {comparison.title} · {value}: una delle due pagine non c’è"
        options.append(
            _option(
                label, compare_url(pair, value), key=key, current=value == lang, off=off, title=title, lang=hreflang
            )
        )
    first, second = comparison.sides
    return {
        "title": f"{comparison.title} — {LANGS[lang]}",
        "code": comparison.code,
        "name": comparison.title,
        "status": STATUS_RESEARCH,
        # Drawn from 48 rem, where each page is ``width`` px wide — side by side from 54 rem, one under
        # the other below: «first» and «then» are true in both, «left» and «right» in one (review HC-2).
        "order": (
            f"Le due pagine a {comparison.width} px, ciascuna con il suo scorrimento; in ordine d’arrivo — prima la "
            f"{first.wave}, poi la {second.wave} — e non di preferenza: decide il proprietario."
        ),
        "warning": ARABIC_FACES if lang == "ar" else "",
        "lang_group": {"slot": "lang", "label": "Lingua", "aria": "Lingua", "options": options},
        "frames": frames,
    }


# ---------------------------------------------------------------------------------------------
# The catalogue
# ---------------------------------------------------------------------------------------------


@dataclass(frozen=True)
class Link:
    """One link of a surface: a proof file (in one of its states, or not), a picker entry or a comparison."""

    label: str
    path: str = ""  #: proof-relative; resolved at render time
    query: str = ""  #: appended to a proof link — the flag that opens a prototype in one of its states
    hero_entry: tuple[str, str, str] = ()  #: (variant, lang, phase) of the hero picker
    type_entry: tuple[str, str, str] = ()  #: (system, surface, lang) of the type picker
    compare_entry: tuple[str, str] = ()  #: (pair, lang) of the compare view
    width: int = 0  #: a picker entry opened at one of ``WIDTHS``
    lang: str = ""
    note: str = ""  #: a short warning printed after the label, e.g. «da non firmare come /ar/»


@dataclass(frozen=True)
class Reference:
    """
    A file a surface names and this server does not serve — the council's minutes, its sheets.

    Printed as a path, never a link: it lives outside the proof directory, in another stream's
    folder, and is neither copied nor exposed. Whether it is on disk is looked up when the hub is
    drawn, like everything else, and said in the same word.
    """

    label: str
    path: str  #: absolute


@dataclass(frozen=True)
class Surface:
    title: str
    note: str
    links: tuple[Link, ...] = ()
    pending: str = ""  #: «non ancora disponibile» for a surface that has no comp yet
    code: str = ""  #: H-0 … H-E, N-A, TYPE A …, printed as a folio
    tag: str = ""  #: the status of a candidate that sits among others (H-C, H-D)
    references: tuple[Reference, ...] = ()


@dataclass(frozen=True)
class Group:
    key: str
    title: str
    lead: str
    surfaces: tuple[Surface, ...]
    tag: str = ""  #: the status every surface of the group shares («prototipo di ricerca — non approvato»)


def _proof(label: str, path: str, lang: str = "", note: str = "", query: str = "") -> Link:
    """A proof file. With ``query`` — the flag that opens a prototype in one of its states — the label shows it."""
    return Link(label=f"{label} · ?{query}" if query else label, path=path, lang=lang, note=note, query=query)


def _hero(variant: str, lang: str = "fr", phase: str = "3", label: str = "") -> Link:
    return Link(label=label or f"selettore · {lang} · {PHASES[phase]}", hero_entry=(variant, lang, phase), lang=lang)


def _type(system: str, surface: str, width: int = 0) -> Link:
    label = f"selettore · {TYPE_SURFACES[surface].label}"
    if width:
        label += f" · {width}"
    return Link(label=label, type_entry=(system, surface, "fr"), width=width, lang="fr")


def _compare(pair: str, lang: str) -> Link:
    return Link(label=f"confronto · {lang}", compare_entry=(pair, lang), lang=lang)


def _pair(folder: str, name: str, query: str = "", pages: tuple[str, str] = ("", "")) -> tuple[Link, Link]:
    """
    The French and the Arabic page of one state of a prototype. ``name`` says where the language
    goes (``public-{lang}-open``); a prototype that names its two pages otherwise — ``index`` and
    ``ar``, ``stage`` and ``stage-ar`` — hands them over as ``pages``, for ``{page}``.
    """
    return tuple(
        _proof(lang, f"{folder}/{name.replace('{lang}', lang).replace('{page}', page)}.html", lang, query=query)
        for lang, page in zip(("fr", "ar"), pages, strict=True)
    )


def _type_group() -> Group:
    """One row per override sheet, written from ``TYPE_SYSTEMS`` so the hub and the bar cannot disagree."""
    entries = {
        "a2": (_type("a2", "home"), _type("a2", "menu")),
        "ap": (_type("ap", "dashboard", 390), _type("ap", "documents", 390)),
    }
    rows = [
        Surface(
            "La pagina della ricerca",
            "Ogni sistema con le sue pagine, le tavole affiancate e le misure (peso dei font, fallback, "
            "spostamento al cambio). In inglese.",
            (_proof("indice della ricerca", "research/type/index.html", "en"),),
        )
    ]
    rows += [
        Surface(
            system.name,
            f"{system.faces[0].upper()}{system.faces[1:]}. {system.remark}",
            entries.get(system.key, (_type(system.key, "home"), _type(system.key, "dashboard"))),
            code=system.code,
            tag=system.status if system.status != STATUS_RESEARCH else "",
        )
        for system in TYPE_SYSTEMS.values()
    ]
    return Group(
        "type",
        "Ricerca — sistemi tipografici TYPE A / B / C / D",
        "Quattro sistemi, una variante, un esperimento e il controllo V4, come fogli di override sulle pagine del "
        "gate 0: home, menu, cruscotto, documenti, fascicolo — in arabo soltanto home e cruscotto, con caratteri "
        "provvisori (O10). Manca ancora la lettura del direttore tipografico, e la scelta è del proprietario.",
        tuple(rows),
        tag=STATUS_RESEARCH,
    )


_NAV = "research/navigation"
_DRAWER = "research/emil/prototype/drawer"
_HE = "research/hero/he"
_UIUX_PUBLIC = "research/uiux-public/proto"
_UIUX_PLATFORM = "research/uiux-platform/proto"
_HE_21ST = "research/hero/he-21st"
_DOOR_MASTER = "research/hero/door-master"
_DOCUMENTS = "research/documents"
_JOURNEY = "research/journey"
_ICONS = "research/icons"
_IMAGES = "research/images/proto"
#: The hero council's record, in the folders of the stream that wrote it — named, not served.
_COUNCIL_MINUTES = "C:/tmp/ile_wt/qa-v5/docs/design-v5/QA/HERO_COUNCIL_REVIEW.md"
_COUNCIL_SHEETS = "C:/tmp/ile_v5_council/.work/hero-council/design"

GROUPS: tuple[Group, ...] = (
    Group(
        "home",
        "La home — il primo schermo (O67)",
        "Cinque primi schermi dello stesso sito, da guardare dal vivo prima di decidere: tre del gate 0 (H-0, H-A, "
        "H-B) e due prototipi di ricerca (H-C, H-D), costruiti per la sola fase 3. Nessuno è approvato. Sotto i "
        "1024 px telefono e tablet sono la maquette attuale nelle tre opzioni del gate 0. Il sesto, H-E, è il "
        "gruppo che segue.",
        (
            Surface(
                "La maquette attuale",
                "Testo a sinistra, la legenda-carta al centro, la porta 392 × 523 a 1440. Il verificatore R3B la "
                "indica come da non firmare; resta il termine di confronto.",
                (
                    _proof("fr · fase 3", "home/phase3.html", "fr"),
                    _proof("ar · fase 3", "home/phase3-ar.html", "ar", NOT_SIGNABLE_AR),
                    _proof("fr · intérim", "home/interim.html", "fr"),
                    _proof("ar · intérim", "home/interim-ar.html", "ar"),
                    _hero("h0"),
                ),
                code="H-0",
            ),
            Surface(
                "La porta, piena",
                "La correzione M1 del revisore per intero: la porta come in H-B, l’arco 60 px sotto la testata, i "
                "gradini sul pavimento; da 1280 px, sotto ricade su H-0.",
                (
                    _proof("fr · fase 3", "home/options/ha-phase3.html", "fr"),
                    _proof("ar · fase 3", "home/options/ha-phase3-ar.html", "ar", NOT_SIGNABLE_AR),
                    _proof("fr · intérim", "home/options/ha-interim.html", "fr"),
                    _hero("ha"),
                ),
                code="H-A",
            ),
            Surface(
                "Il pilastro e la soglia",
                "La porta a tutta altezza e i quattro accessi come soglia; da 1280 px e con una sua composizione "
                "da 1024 px. Raccomandata al gate 0 dal verificatore di design (R3B) e dal reparto composizione, "
                "che avevano davanti le sole H-0, H-A e H-B; non approvata: la decisione è del proprietario.",
                (
                    _proof("fr · fase 3", "home/options/hb-phase3.html", "fr"),
                    _proof("ar · fase 3", "home/options/hb-phase3-ar.html", "ar", NOT_SIGNABLE_AR),
                    _proof("fr · intérim", "home/options/hb-interim.html", "fr"),
                    _hero("hb"),
                ),
                code="H-B",
            ),
            Surface(
                "Quattro soglie, una chiave",
                "Quattro stanze uguali su una linea di pavimento — parola, glifo, fotografia e rotta per ogni "
                "accesso, fino alla chiave; da 1024 px, sotto non cambia nulla. Chiede due emendamenti alla "
                "Direzione creativa e poggia su fotografie provvisorie. Il consiglio sull’hero l’ha esaminata il "
                "2 ottobre: il verbale è nel gruppo «Consiglio sull’hero». Decide il proprietario (O67).",
                (
                    _proof("fr · fase 3", "research/hero/hc/index.html", "fr"),
                    _proof("ar · fase 3", "research/hero/hc/ar.html", "ar", NOT_SIGNABLE_AR),
                    _hero("hc"),
                    _proof("esplorazione · tre varianti", "research/hero/hc/explore.html", "fr"),
                ),
                code="H-C",
                tag=STATUS_RESEARCH,
            ),
            Surface(
                "La porta, di giorno",
                "Le parole di giorno, su carta; la porta nella notte, in una nicchia; i quattro accessi come indice "
                "leggibile a riposo — fotografia, parola, frase; sotto i 1024 px è la soluzione A in tono di carta. "
                "Il primo schermo non è più notturno, e il §9 della Direzione creativa andrebbe emendato. Il "
                "consiglio sull’hero l’ha esaminata il 2 ottobre: il verbale è nel gruppo «Consiglio sull’hero». "
                "Decide il proprietario (O67).",
                (
                    _proof("fr · fase 3", "research/hero/hd/index.html", "fr"),
                    _proof("ar · fase 3", "research/hero/hd/ar.html", "ar", NOT_SIGNABLE_AR),
                    _hero("hd"),
                    _proof("esplorazione · La rete", "research/hero/hd/explore/rete.html", "fr"),
                    _proof("esplorazione · Due rive", "research/hero/hd/explore/due-rive.html", "fr"),
                    _proof("esplorazione · La loggia", "research/hero/hd/explore/loggia.html", "fr"),
                ),
                code="H-D",
                tag=STATUS_RESEARCH,
            ),
        ),
    ),
    Group(
        "he",
        "H-E — nuova direzione",
        "Direzione nuova autorizzata dal proprietario il 2 ottobre. Al 4 ottobre la pagina è costruita, come prova "
        "provvisoria, e la sua revisione indipendente non è conclusa; decide il proprietario — O67. In fondo al "
        "gruppo, tre pagine di misura: ciascuna dice che cosa è e che cosa non è.",
        (
            Surface(
                "La pagina costruita",
                "Il primo schermo di H-E, costruito per la sola fase 3, in francese e in arabo.",
                (
                    _proof("fr · fase 3", f"{_HE}/index.html", "fr"),
                    _proof("ar · fase 3", f"{_HE}/ar.html", "ar", NOT_SIGNABLE_AR),
                    _hero("he"),
                ),
                code="H-E",
            ),
            Surface(
                "I tre concetti",
                "I tre quadri di concetto di H-E, in francese soltanto: nel selettore sono le scelte E1, E2 ed E3, "
                "senza tasto.",
                tuple(_hero(f"e{n}", label=f"selettore · concetto {n}") for n in (1, 2, 3)),
                code="E1–E3",
            ),
            Surface(
                "CTA-A / CTA-B",
                "Il campione delle due candidate per la CTA primaria dell’eroe: CTA-A e CTA-B.",
                (_proof("campione", f"{_HE}/cta/index.html", "fr"),),
            ),
            Surface(
                "Il banco del primo movimento",
                "Il primo movimento di H-E misurato su una geometria di sostituzione: un diagramma dei tempi — si "
                "giudicano i tempi, non il disegno.",
                (_proof("banco", "research/hero/he-motion/index.html", "fr"),),
            ),
            Surface(
                "Le due CTA sul loro banco",
                "CTA-A e CTA-B accanto a T0, il riferimento: i loro stati, e un primo schermo di sostituzione, il "
                "palco. Sul palco una CTA alla volta: il parametro cta sceglie T0, CTA-A o CTA-B. È un banco di "
                "prova, non un eroe e non una proposta: i suoi numeri vanno ripresi su H-E.",
                (
                    _proof("stati · fr", f"{_HE_21ST}/states.html", "fr"),
                    _proof("stati · ar", f"{_HE_21ST}/states-ar.html", "ar"),
                    # The stand-in first screen draws ONE primary, the one ?cta= names, and T0 when the
                    # query says nothing (bench.js): one link per primary and per language, none bare.
                    _proof("palco · fr · T0", f"{_HE_21ST}/stage.html", "fr", query="cta=t0"),
                    _proof("palco · fr · CTA-A", f"{_HE_21ST}/stage.html", "fr", query="cta=a"),
                    _proof("palco · fr · CTA-B", f"{_HE_21ST}/stage.html", "fr", query="cta=b"),
                    _proof("palco · ar · T0", f"{_HE_21ST}/stage-ar.html", "ar", query="cta=t0"),
                    _proof("palco · ar · CTA-A", f"{_HE_21ST}/stage-ar.html", "ar", query="cta=a"),
                    _proof("palco · ar · CTA-B", f"{_HE_21ST}/stage-ar.html", "ar", query="cta=b"),
                ),
            ),
            Surface(
                "La porta dal suo master",
                "La fotografia della porta servita dal suo master, in più larghezze e precaricata: un frammento da "
                "copiare in una pagina, non una pagina — aperto da solo mostra la fotografia, senza la porta "
                "disegnata. La pagina di verifica mette la porta di oggi accanto a quella del frammento, così com’è "
                "scritto: una verifica, non una maquette.",
                (
                    _proof("frammento", f"{_DOOR_MASTER}/snippet.html", "fr"),
                    _proof("verifica · oggi e il frammento", f"{_DOOR_MASTER}/check/door-snippet.html", "fr"),
                ),
            ),
        ),
        tag=STATUS_RESEARCH,
    ),
    Group(
        "council",
        "Consiglio sull’hero",
        "Cinque seggi su cinque: nessuno tra H-0, H-A, H-B, H-C e H-D raggiunge, così com’è costruito, il livello "
        "richiesto. Il consiglio non approva nulla e non impone un vincitore: decide il proprietario (O67). "
        "L’ordine di preferenza dei seggi sta nel verbale, con le sue riserve, e non in questa pagina. Il verbale "
        "e le tavole non sono serviti da questo server: qui sotto ci sono i loro percorsi, come testo.",
        (
            Surface(
                "Il verbale",
                "Il verbale del segretario per il proprietario, in inglese: l’esito, ogni punteggio, gli accordi e le "
                "contraddizioni fra i cinque seggi, ciò che non è stato esaminato.",
                references=(Reference("verbale", _COUNCIL_MINUTES),),
            ),
            Surface(
                "Le tavole prima/dopo",
                "Le due tavole del seggio «design», alle due larghezze a cui il consiglio ha guardato.",
                references=(
                    Reference("1440 × 900", f"{_COUNCIL_SHEETS}/BEFORE_AFTER_1440x900.png"),
                    Reference("390 × 844", f"{_COUNCIL_SHEETS}/BEFORE_AFTER_390x844.png"),
                ),
            ),
        ),
    ),
    Group(
        "navbar",
        "Navbar e mega-menu",
        "La testata pubblica con il pannello aperto: quattro stati catturati, fase 3 e intérim, fr e ar.",
        (
            Surface(
                "Fase 3 — menu aperto",
                "La testata della fase 3 con il pannello «Personnes» aperto: la fotografia Persona si firma qui (O59).",
                (
                    _proof("fr", "home/phase3-menu.html", "fr"),
                    _proof("ar", "home/phase3-menu-ar.html", "ar", NOT_SIGNABLE_AR),
                ),
            ),
            Surface(
                "Intérim — menu aperto",
                "Lo stesso pannello su ciò che il pubblico vede oggi (8770).",
                (
                    _proof("fr", "home/interim-menu.html", "fr"),
                    _proof("ar", "home/interim-menu-ar.html", "ar"),
                ),
            ),
        ),
    ),
    Group(
        "login",
        "Accesso «Il varco»",
        "Solo la porta, il modulo sulla carta; la chiave gira una volta all’ingresso, i piani non si muovono mai (O1).",
        (
            Surface(
                "Il varco",
                "Stato di riposo, stato d’errore, e le due pagine arabe.",
                (
                    _proof("fr · riposo", "login/index.html", "fr"),
                    _proof("fr · errore", "login/error.html", "fr"),
                    _proof("ar · riposo", "login/ar.html", "ar"),
                    _proof("ar · errore", "login/error-ar.html", "ar"),
                ),
            ),
        ),
    ),
    Group(
        "shell",
        "Guscio della piattaforma e cruscotto della persona",
        "La console un passo più chiara (O13), la barra di contesto nella grammatica ILE, il NowPanel con la sua "
        "azione, il binario «la soglia».",
        (
            Surface(
                "Cruscotto a metà percorso",
                "Il guscio della console (rail etichettato, barra di contesto, spazio di lavoro) attorno al cruscotto "
                "di una persona a metà percorso.",
                (
                    _proof("fr", "shell-dashboard/index.html", "fr"),
                    _proof("ar", "shell-dashboard/ar.html", "ar"),
                ),
            ),
        ),
    ),
    Group(
        "documents",
        "Spazio documenti",
        "VALIDE in inchiostro, nessuna spunta da nessuna parte — nemmeno sul filtro scelto (O14); «Il registro»; il "
        "Dépôt con i campi etichettati.",
        (
            Surface(
                "«Mes pièces»",
                "L’elenco delle pièces, la striscia di salute, «Il registro».",
                (
                    _proof("fr", "documents/index.html", "fr"),
                    _proof("ar", "documents/ar.html", "ar"),
                ),
            ),
            Surface(
                "Tavola degli stati",
                "Otto registri, «conforme» in inchiostro senza spunta, su pietra, foglio della console e notte, "
                "fr e ar.",
                (_proof("fr", "documents/chips.html", "fr"),),
            ),
            Surface(
                "Dépôt",
                "Il caricamento di una pièce in ciascuno dei suoi stati, alla larghezza del cassetto.",
                (
                    _proof("fr", "documents/depot.html", "fr"),
                    _proof("ar", "documents/depot-ar.html", "ar"),
                ),
            ),
        ),
    ),
    Group(
        "journey",
        "Il passaggio «La soglia» e il prototipo delle luci",
        "La linea in piano: sette stazioni, il passaggio d’orientamento, poi la console — gli stessi componenti "
        "della home e del cruscotto.",
        (
            Surface(
                "Il passaggio — pubblico e console",
                "Geometria in piano, LTR e RTL, movimento ridotto.",
                (
                    _proof("fr", "journey/index.html", "fr"),
                    _proof("ar", "journey/ar.html", "ar"),
                ),
            ),
            Surface(
                "Luci delle rotte (prototipo)",
                "La prima respirazione dell’eroe «La porta»: la luce dell’arco poi le quattro luci delle rotte, "
                "campionate a runtime (O29) — misura, non maquette da firmare.",
                (
                    _proof("fr", "journey/hero-lights.html", "fr"),
                    _proof("ar", "journey/hero-lights-ar.html", "ar"),
                ),
            ),
        ),
    ),
    Group(
        "phone",
        "Tavola telefono (misura)",
        "L’eroe intérim su telefono misurato su 8770: solo geometria, il disegno da firmare è quello della home.",
        (
            Surface(
                "Tavola delle misure",
                "La soluzione A «Una schermata», misurata sulla home realmente servita (8770) prima e dopo il "
                "foglio del prototipo.",
                (_proof("tavola", "phone-hero/index.html", "fr"),),
            ),
        ),
    ),
    Group(
        "loader",
        "Il caricatore di firma",
        "La chiave che gira nella porta del marchio: gli stati del caricatore e il movimento ridotto.",
        (
            Surface(
                "Caricatore",
                "La chiave che gira: L1 all’ingresso, L2, L3, il filo, e la scena della porta — anche con «riduci "
                "movimento» attivo.",
                (_proof("caricatore", "smoke/loader.html", "fr"),),
            ),
        ),
    ),
    Group(
        "components",
        "Vetrina dei componenti (fondazione)",
        "Font, token, lo sprite provvisorio e i glifi d’identità ridisegnati per le piccole dimensioni.",
        (
            Surface(
                "Fondazione",
                "Il controllo (font, token, bottoni, chip, icone), il guscio della console, il chrome pubblico "
                "(barra utilitaria, testata, portico), lo sprite, ile-arch e ile-mark a 14–20 px.",
                (
                    _proof("controllo", "smoke/index.html", "fr"),
                    _proof("guscio console", "smoke/console.html", "fr"),
                    _proof("chrome pubblico", "smoke/chrome.html", "fr"),
                    _proof("sprite", "smoke/icons.html", "fr"),
                    _proof("glifi d’identità", "smoke/identity-small.html", "fr"),
                ),
            ),
        ),
    ),
    Group(
        "package",
        "Il pacchetto di firma",
        "L’indice delle prove e la scheda di firma: i verdetti alla lettera, l’ordine di firma, ciò che è ancora "
        "aperto.",
        (
            Surface(
                "Gate 0 «La prova»",
                "L’indice generato da tools/build_index.py e la scheda SIGNING_SHEET.md (servita come testo).",
                (
                    _proof("indice delle prove", "index.html", "it"),
                    _proof("SIGNING_SHEET.md", "SIGNING_SHEET.md", "it"),
                ),
            ),
        ),
    ),
    _type_group(),
    Group(
        "research-loader",
        "Ricerca — il caricatore di firma, tre candidati",
        "Un candidato per ciascuna parola del brief «porta / luce / percorso». Tutti e tre sono una macchina a "
        "stati — riposo, ingaggio, apertura — e niente gira in ciclo: durante l’attesa il caricatore sta fermo. "
        "Nessuno ha ancora guardato il movimento a velocità reale, e la scelta è del proprietario. Il link "
        "«movimento ridotto · ?rm=1» non è ancora lo stato di movimento ridotto: ferma il caricatore, ma i token di "
        "durata del gate 0 restano (MS7).",
        (
            Surface(
                "I tre candidati a confronto",
                "La pagina di confronto: i tre candidati, il controllo del gate 0 e le tre tavole a 1×.",
                (_proof("confronto", "research/loader/index.html", "fr"),),
            ),
            Surface(
                "«Mandata» — risponde la porta",
                "La chiave entra, mezzo giro, si assesta; tiene; mezzo giro, e una luce sale nel telaio della porta. "
                "È il solo candidato che non chiede di cambiare una regola.",
                (
                    _proof("tavole fr e ar", "research/loader/mandata/index.html", "fr"),
                    _proof("movimento ridotto", "research/loader/mandata/index.html", "fr", query="rm=1"),
                ),
                code="A",
            ),
            Surface(
                "«Lume» — risponde la luce",
                "Un giro morbido; tiene; la stanza dietro la porta si riempie di luce dall’occhio della chiave. "
                "Chiede al proprietario di emendare la regola M10.",
                (
                    _proof("tavole fr e ar", "research/loader/lume/index.html", "fr"),
                    _proof("movimento ridotto", "research/loader/lume/index.html", "fr", query="rm=1"),
                ),
                code="B",
            ),
            Surface(
                "«Passo» — risponde il percorso",
                "Un giro rapido; tiene; i tre gradini prendono la luce e un filo corre dalla linea di terra al "
                "contenuto. Il solo il cui movimento ha un verso — corre nel senso della lettura e in arabo si "
                "specchia — e il solo che esce dal marchio: gli serve spazio accanto.",
                (
                    _proof("tavole fr e ar", "research/loader/passo/index.html", "fr"),
                    _proof("movimento ridotto", "research/loader/passo/index.html", "fr", query="rm=1"),
                ),
                code="C",
            ),
        ),
        tag=STATUS_RESEARCH,
    ),
    Group(
        "research-navigation",
        "Ricerca — navigazione pubblica e di console",
        "Due proposte sulla fondazione del gate 0: N-A «Il sommario» per la testata pubblica (fotografia, indice, "
        "riquadro di lettura) e P-A «Tre livelli» per la console (il binario, la fascia di contesto, le azioni). "
        "Nessuno ha ancora guardato il movimento, i caratteri arabi sono provvisori (O10) e dieci decisioni — "
        "N1–N10 — restano del proprietario.",
        (
            Surface(
                "L’indice dei prototipi",
                "La tavola degli stati, in francese e in arabo, com’è scritta dalla ricerca (in inglese).",
                (_proof("indice", f"{_NAV}/index.html", "en"),),
            ),
            Surface(
                "Pubblico — la testata chiusa",
                "La testata in cima a «Espace Personnes».",
                _pair(_NAV, "public-{lang}"),
                code="N-A",
            ),
            Surface(
                "Pubblico — «Personnes» aperto con un clic",
                "La glossa della porta nel riquadro di lettura; lo scrim compare solo per un clic o per la tastiera.",
                _pair(_NAV, "public-{lang}-open"),
                code="N-A",
            ),
            Surface(
                "Pubblico — aperto al passaggio del puntatore",
                "«Formation» sotto il puntatore: il suo testo d’apertura, intero, nel riquadro di lettura.",
                _pair(_NAV, "public-{lang}-item"),
                code="N-A",
            ),
            Surface(
                "Pubblico — «Entreprises»",
                "Una porta con due sole voci: il caso rado.",
                _pair(_NAV, "public-{lang}-entreprises"),
                code="N-A",
            ),
            Surface(
                "Pubblico — «Projet»",
                "Il pannello semplice, appeso alla fine della barra.",
                _pair(_NAV, "public-{lang}-projet"),
                code="N-A",
            ),
            Surface(
                "Pubblico — dopo lo scorrimento",
                "La barra a 56 px, in vetro: solo con un puntatore fine e nessun pannello aperto.",
                _pair(_NAV, "public-{lang}-scrolled"),
                code="N-A",
            ),
            Surface(
                "Pubblico — il foglio su telefono",
                "La testata che occupa lo schermo, «Personnes» aperto sul posto. Da guardare a 390 px: il parametro "
                "drawer=1 apre il foglio al caricamento.",
                _pair(_NAV, "public-{lang}-sheet", "drawer=1"),
                code="N-A",
            ),
            Surface(
                "Console — il fascicolo, binario aperto",
                "I tre livelli sulla pagina del fascicolo: il binario (248 px), la fascia con l’identità e l’indice "
                "di sezione, l’azione primaria. A 390 px: la barra superiore e la barra d’azione.",
                _pair(_NAV, "app-{lang}"),
                code="P-A",
            ),
            Surface(
                "Console — il binario compatto",
                "80 px, con le etichette brevi: mai di soli glifi.",
                _pair(_NAV, "app-{lang}-compact"),
                code="P-A",
            ),
            Surface(
                "Console — dopo lo scorrimento",
                "L’indice di sezione agganciato, con l’identità condensata e l’azione primaria.",
                _pair(_NAV, "app-{lang}-stuck"),
                code="P-A",
            ),
            Surface(
                "Console — il cassetto su telefono",
                "Il binario intero in un cassetto. Da guardare a 390 px: il parametro drawer=1 lo apre al caricamento.",
                _pair(_NAV, "app-{lang}", "drawer=1"),
                code="P-A",
            ),
        ),
        tag=STATUS_RESEARCH,
    ),
    Group(
        "research-drawer",
        "Ricerca — il cassetto della console, il movimento",
        "Come entra e come esce il menu della console su telefono: quattro posizioni dietro un selettore, sul "
        "cruscotto del gate 0. Nessuno ha ancora guardato il movimento: i tempi vengono dal codice e da fotogrammi. "
        "La scelta è del proprietario.",
        (
            Surface(
                "Gate 0 · Slide · Quiet · Sheet",
                "In una finestra più stretta di 1024 px: i tasti 1–4 o ← → cambiano posizione e rigiocano l’ingresso, "
                "R lo rigioca. Gate 0 è il controllo; il parametro exit=out prova l’altra curva d’uscita. Il "
                "parametro rm=1 non è ancora lo stato di movimento ridotto: cambia il cassetto, ma i token di durata "
                "del gate 0 restano (MS7).",
                (
                    _proof("fr", f"{_DRAWER}/index.html", "fr"),
                    _proof("ar", f"{_DRAWER}/ar.html", "ar"),
                    _proof("fr · altra curva d’uscita", f"{_DRAWER}/index.html", "fr", query="exit=out"),
                    _proof("fr · movimento ridotto", f"{_DRAWER}/index.html", "fr", query="rm=1"),
                ),
            ),
        ),
        tag=STATUS_RESEARCH,
    ),
    Group(
        "research-cta",
        "Ricerca — la CTA di firma",
        "Il bottone primario dell’eroe due volte sulla notte: T0 «Bordo d’oro» e T2, l’anello fatto in casa. "
        "Misurato soltanto su un renderer software, mai dentro la home vera; oltre a chi l’ha costruito non l’ha "
        "guardato nessuno.",
        (
            Surface(
                "T0 «Bordo d’oro» e T2, l’anello",
                "Riposo, hover, focus da tastiera, pressione. Da guardare su un desktop con il mouse: su telefono "
                "la pagina mostra T0 due volte, per costruzione.",
                (
                    _proof("fr", "research/21st-group1/signature-cta/index.html", "fr"),
                    _proof("ar", "research/21st-group1/signature-cta/ar.html", "ar"),
                ),
            ),
        ),
        tag=STATUS_RESEARCH,
    ),
    Group(
        "research-21st",
        "Ricerca, seconda ondata — tre componenti dalla rassegna 21st",
        "Tre meccanismi presi dalla rassegna dei componenti 21st e rifatti sulla fondazione del gate 0, con le "
        "stringhe vere del prodotto: ciascuno mostra un meccanismo, non una pagina. Portano il giudizio di chi li "
        "ha costruiti: la revisione indipendente è in attesa.",
        (
            Surface(
                "Il codice di verifica — un campo, sei caselle",
                "Il secondo passaggio dell’accesso: un solo campo vero sotto sei caselle disegnate — vuoto, "
                "compilato, rifiutato dal server. Niente viene inviato; la riga d’aiuto sotto il campo è una "
                "proposta, il resto sono le stringhe di oggi.",
                _pair("research/21st-group2/code-field", "{page}", pages=("index", "ar")),
            ),
            Surface(
                "Il suggerimento e la definizione",
                "Il nome di un controllo come suggerimento — il primo attende 400 ms, i vicini compaiono subito — "
                "e un termine del glossario che apre la sua definizione là dove lo si legge. Senza script.",
                _pair("research/21st-group4/proto", "{page}", pages=("overlays", "overlays-ar")),
            ),
            Surface(
                "La scelta guida l’immagine",
                "Un solo palco per l’immagine e quattro voci: il puntatore o la tastiera la cambiano, un tocco "
                "segue il link; sotto 48 rem ogni voce tiene la sua fotografia. Un campione di ricerca, non un "
                "sostituto delle «Quattro porte».",
                _pair("research/21st-group4/proto", "{page}", pages=("stage", "stage-ar")),
            ),
        ),
        tag=STATUS_RESEARCH,
    ),
    Group(
        "research-motion",
        "Ricerca, seconda ondata — il banco di prova del movimento",
        "I cinque livelli del movimento sui controlli veri di ILE: dal livello 0 — ciò che si apre da tastiera "
        "non si muove — al riscontro di un gesto, alle transizioni di stato, fino ai movimenti di firma. È una "
        "pagina di misura, non una maquette: la revisione indipendente è in attesa.",
        (
            Surface(
                "Il banco",
                "Ogni livello con i suoi controlli e la regola che lo governa. I parametri rigiocano la pagina: "
                "rm=1 con il movimento ridotto, slow=5 con ogni orologio cinque volte più lento.",
                (
                    *_pair("research/motion/bench", "{page}", pages=("index", "ar")),
                    _proof("fr · movimento ridotto", "research/motion/bench/index.html", "fr", query="rm=1"),
                    _proof("fr · al rallentatore", "research/motion/bench/index.html", "fr", query="slow=5"),
                ),
            ),
        ),
        tag=STATUS_RESEARCH,
    ),
    Group(
        "research-uiux",
        "Ricerca, seconda ondata — le proposte dei due audit UI-UX-Pro-Max",
        "Copie delle maquette del gate 0 con le correzioni proposte dai due audit, quello delle pagine pubbliche e "
        "quello della piattaforma: le maquette originali sono lette, mai modificate, e nessuna parola cambia. "
        "Sono proposte di chi ha condotto gli audit: la revisione indipendente è in attesa.",
        (
            Surface(
                "Pubblico — la home",
                "La promessa in due blocchi, l’avviso frase per frase, gli spazi e i trattini della tipografia "
                "francese — su H-0 e su H-B.",
                (
                    _proof("H-0 · fr", f"{_UIUX_PUBLIC}/home-h0.html", "fr"),
                    _proof("H-B · fr", f"{_UIUX_PUBLIC}/home-hb.html", "fr"),
                    _proof("H-B · ar", f"{_UIUX_PUBLIC}/home-hb-ar.html", "ar", NOT_SIGNABLE_AR),
                ),
            ),
            Surface(
                "Pubblico — il menu aperto",
                "Le stesse correzioni sulla testata della fase 3 con il pannello aperto.",
                (_proof("fr", f"{_UIUX_PUBLIC}/menu.html", "fr"),),
            ),
            Surface(
                "Pubblico — l’accesso",
                "Il bottone che mostra la password porta un’etichetta visibile, i due campi non hanno più un "
                "segnaposto, e nella pagina d’errore ciascun campo è legato al suo messaggio.",
                (
                    _proof("fr · riposo", f"{_UIUX_PUBLIC}/login.html", "fr"),
                    _proof("fr · errore", f"{_UIUX_PUBLIC}/login-error.html", "fr"),
                    _proof("ar · riposo", f"{_UIUX_PUBLIC}/login-ar.html", "ar"),
                ),
            ),
            Surface(
                "Piattaforma — il guscio e il cruscotto",
                "Il piede del binario resta in vista mentre l’elenco scorre, un secondo link di salto porta al "
                "controllo «Menu», un pannello si chiude quando il fuoco della tastiera lo lascia.",
                _pair(_UIUX_PLATFORM, "shell-{lang}"),
            ),
            Surface(
                "Piattaforma — «Mes pièces»",
                "Su telefono una riga di pièce già nel primo schermo e il filtro in un foglio; ogni controllo "
                "ripetuto nomina la sua pièce; 16 px in ogni campo di testo su un puntatore grossolano.",
                _pair(_UIUX_PLATFORM, "docs-{lang}"),
            ),
        ),
        tag=STATUS_RESEARCH,
    ),
    Group(
        "research-documents",
        "Ricerca, terza ondata — «Mes pièces» V5.2",
        "La proposta dello specialista dello spazio documenti, sulla fondazione del gate 0, che resta com’è e fa da "
        "riferimento: la riga in sei zone con il suo piede, la riga intera come link, la striscia del registro con "
        "l’azione primaria della pagina, tre gruppi sotto le parole «À vous · En cours · Réglées». Porta il giudizio "
        "di chi l’ha costruita: la revisione indipendente è in attesa.",
        (
            Surface(
                "La pagina",
                "«Mes pièces» com’è proposta: la striscia del registro e l’elenco delle pièces nei suoi tre gruppi.",
                (
                    _proof("fr", f"{_DOCUMENTS}/index.html", "fr"),
                    _proof("ar", f"{_DOCUMENTS}/ar.html", "ar"),
                ),
            ),
            Surface(
                "La tavola annotata",
                "La riga in sei zone e i suoi nove casi, la striscia del registro, gli otto stati, le scadenze, la "
                "carta, il deposito, l’anteprima, la variante B della striscia e le due misure del conteggio, "
                "disegnati uno per uno; le annotazioni sono in inglese.",
                (_proof("tavola", f"{_DOCUMENTS}/anatomy.html", "fr"),),
            ),
            Surface(
                "Due telefoni a confronto",
                "Le due versioni di «Mes pièces» per il telefono, ciascuna con il suo scorrimento: la proposta "
                "dell’audit della piattaforma (seconda ondata, qui sopra) e quella dello specialista dello spazio "
                "documenti, in ordine d’arrivo. Alla stessa larghezza: 390 px, affiancate, da 864 px di finestra; "
                "sotto, una sotto l’altra, larghe quanto la finestra permette, fino a 390 px. Il confronto non ne "
                "indica una: decide il proprietario.",
                (_compare("mes-pieces", "fr"), _compare("mes-pieces", "ar")),
                code="K5",
            ),
        ),
        tag=STATUS_RESEARCH,
    ),
    Group(
        "research-journey",
        "Ricerca, terza ondata — «La soglia» V5.2",
        "Il percorso Marocco → Italia come componente di firma: una linea in piano, tre registri — le tappe, chi "
        "tiene ogni tratto, le pièces — e le due soglie, nel passaggio pubblico, nel cruscotto e nel fascicolo. "
        "Porta il giudizio di chi l’ha costruito: la revisione indipendente è in attesa.",
        (
            Surface(
                "Il passaggio, il binario, il fascicolo",
                "Il passaggio pubblico, il binario del cruscotto, il fascicolo e il formato compatto, con gli stati, "
                "sulla stessa pagina.",
                (
                    _proof("fr", f"{_JOURNEY}/index.html", "fr"),
                    _proof("ar", f"{_JOURNEY}/ar.html", "ar"),
                ),
            ),
        ),
        tag=STATUS_RESEARCH,
    ),
    Group(
        "research-colour",
        "Ricerca, terza ondata — i colori della piattaforma",
        "Il sistema dei colori del gate 0 rimisurato, con le correzioni proposte accanto ai token di oggi: un rilievo "
        "e delle proposte, nessun token cambiato. Porta il giudizio di chi l’ha costruito: la revisione indipendente "
        "è in attesa.",
        (
            Surface(
                "Il campione",
                "Oggi e la proposta, affiancati, con le stringhe vere del prodotto in francese e in arabo.",
                (_proof("campione", "research/colour/specimen.html", "fr"),),
            ),
        ),
        tag=STATUS_RESEARCH,
    ),
    Group(
        "research-icons",
        "Ricerca, terza ondata — le icone",
        "Lo sprite del gate 0 misurato contro la mappa semantica delle icone: le dimensioni minime, i quasi gemelli, "
        "i quattro pubblici, i glifi da sostituire. I candidati sono schizzi, non disegni di produzione. Porta il "
        "giudizio di chi l’ha costruito: la revisione indipendente è in attesa.",
        (
            Surface(
                "La tavola semantica",
                "I quattro pubblici, i domini, il percorso, le responsabilità, «i cerchi», i momenti su misura, gli "
                "emendamenti del gate 0 e le proposte, alle dimensioni dello sprite; il commento è in inglese.",
                (
                    _proof("fr", f"{_ICONS}/sheet.html", "fr"),
                    _proof("ar", f"{_ICONS}/sheet-ar.html", "ar"),
                ),
            ),
            Surface(
                "Le famiglie",
                "Dodici famiglie di icone, l’una accanto all’altra; in inglese.",
                (_proof("famiglie", f"{_ICONS}/families.html", "en"),),
            ),
            Surface(
                "I candidati",
                "Ogni candidato, su carta e su notte; in inglese.",
                (_proof("candidati", f"{_ICONS}/candidates.html", "en"),),
            ),
        ),
        tag=STATUS_RESEARCH,
    ),
    Group(
        "research-images",
        "Ricerca, terza ondata — la fila delle porte",
        "La fila delle porte della home del gate 0, con le sue parole, quattro volte: le fotografie di oggi, quelle "
        "proposte in due tagli, le alternative. Porta il giudizio di chi l’ha costruita: la revisione indipendente è "
        "in attesa.",
        (
            Surface(
                "La fila, quattro volte",
                "Mostra fotografie stock (Pexels), provvisorie finché il proprietario non risponde a O54 e O55 e non "
                "decide O81; fra le alternative, una è trattenuta per O55. È una pagina soltanto locale, da non "
                "pubblicare.",
                (
                    _proof("fr", f"{_IMAGES}/doors.html", "fr"),
                    _proof("ar", f"{_IMAGES}/doors-ar.html", "ar"),
                ),
            ),
        ),
        tag=STATUS_RESEARCH,
    ),
    Group(
        "upcoming",
        "In arrivo (V5.2 §7.2)",
        "Le superfici che l’hub mostrerà man mano che le famiglie arrivano; nessuna ha ancora una maquette.",
        (
            Surface(
                "Fascicolo",
                "La pagina del fascicolo e la sua cronologia. Per ora esistono soltanto campioni di ricerca: la "
                "tipografia, la navigazione e il registro del percorso nel fascicolo («La soglia» V5.2), qui sopra.",
                pending="non ancora disponibile",
            ),
            Surface(
                "Cruscotto impresa",
                "Lo spazio dell’impresa e la tabella dei bisogni.",
                pending="non ancora disponibile",
            ),
            Surface("Academy", "La formazione collegata.", pending="non ancora disponibile"),
            Surface("Forum", "Il Forum permanente Veneto–Marocco.", pending="non ancora disponibile"),
        ),
    ),
)


def _resolved_link(link: Link, root: Path) -> dict:
    """
    A link as the hub draws it. Whatever stands on a proof file — the file itself, or the picker
    entry that frames it — is ``available`` only if that file can be served; the hub then prints
    «manca» in place of a link.
    """
    resolved = {"label": link.label, "lang": link.lang, "note": link.note}
    if link.hero_entry:
        paths = (hero_file(*link.hero_entry),)
        url, kind = hero_url(*link.hero_entry, link.width), "picker"
    elif link.type_entry:
        paths = (type_file(*link.type_entry),)
        url, kind = type_url(*link.type_entry, link.width), "picker"
    elif link.compare_entry:
        # Both pages, or «manca»: a comparison with one side missing is not the comparison.
        paths = compare_files(*link.compare_entry)
        url, kind = compare_url(*link.compare_entry), "compare"
    else:
        paths = (link.path,)
        url, kind = proof_url(link.path) + (f"?{link.query}" if link.query else ""), "proof"
    available = all(path and proof_exists(root, path) for path in paths)
    return {
        **resolved,
        "url": url if available else "",
        "kind": kind,
        "available": available,
        "path": " · ".join(paths),
    }


def catalogue(root: Path) -> list[dict]:
    """
    The groups with every link resolved against ``root`` — template-ready dictionaries.

    Resolved here and now, on every call: nothing about what is on disk is remembered from one
    request to the next, so a file that arrives is linked at the next reload and one that goes is
    «manca» again.
    """
    groups = []
    for group in GROUPS:
        surfaces = [
            {
                "title": surface.title,
                "note": surface.note,
                "code": surface.code,
                "tag": surface.tag,
                "links": [_resolved_link(link, root) for link in surface.links],
                "references": [
                    {"label": reference.label, "path": reference.path, "present": Path(reference.path).is_file()}
                    for reference in surface.references
                ],
                "pending": surface.pending,
            }
            for surface in group.surfaces
        ]
        groups.append(
            {"key": group.key, "title": group.title, "lead": group.lead, "tag": group.tag, "surfaces": surfaces}
        )
    return groups


def catalogued_proof_paths() -> list[str]:
    """Every proof file the hub, the two pickers and the compare view point at — what the currency test checks."""
    paths = [link.path for group in GROUPS for surface in group.surfaces for link in surface.links if link.path]
    paths += [file for variant in HERO_VARIANTS.values() for file in variant.files.values()]
    paths += [file for comparison in COMPARISONS.values() for side in comparison.sides for file in side.files.values()]
    paths += [
        type_file(system, surface, lang)
        for system in TYPE_SYSTEMS
        for surface in TYPE_SURFACES
        for lang in LANGS
        if type_file(system, surface, lang)
    ]
    return sorted(set(paths))
