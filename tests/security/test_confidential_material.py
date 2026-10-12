"""
The confidential document package must never enter the repository.

Policy: docs/security/CONFIDENTIAL_MATERIAL_POLICY.md. The 20 September 2026 package (Master
Dossier v2.0, Technical Blueprint v1.0, Relazione Tecnica, SIAE dossier, Mod. 350 guidance sheet and
the filled Mod. 350 deposit form) is confidential, is the subject of an unpublished-work deposit, and
the deposit form carries the personal data of a natural person.

These tests fail if any of that material — or a sentinel drawn from it — is found in a tracked file.
They are deliberately cheap and deliberately paranoid: the cost of a false positive is renaming a
variable, the cost of a false negative is publishing an unpublished work and a person's identifiers.

The sentinels come from two tables. The public one, below, holds only what a public repository may
name: the confidentiality markings and the public references printed on the deposit form. The
depositant's private identifiers may not be written here, nor anywhere else in the repository — a
guard that spells out the value it guards publishes it. They live in a private table outside the
repository: a JSON list of [pattern, label] pairs, named by the environment variable
ILE_CONFIDENTIAL_SENTINELS (the local, untracked .env, or the shell).

- Variable unset, as in CI: a dedicated test is SKIPPED and says why, so the gap shows in every run
  summary instead of hiding behind a green tick.
- Variable set, but the table missing, unreadable, empty or malformed: the tests FAIL. A missing
  table must never look like a pass — the lesson of the history filter, which refuses to start
  without its own table (docs/security/HISTORY_REWRITE_2026-09-21.md §5.1).
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]

#: SHA-256 of each document in the confidential package (docs/source-of-truth/DOCUMENT_MANIFEST.md).
#: A tracked file with one of these digests is the document itself, whatever it is called.
CONFIDENTIAL_DIGESTS = {
    "2dd30a10568666789ba16e99b784b96dd94b4b666008a54733ab3d967fd2a044": "Master Dossier v2.0",
    "10e63363e8b45f05ba46728d9c7b3f2b7c74acd7402d9d6e987d6b6a4e32d04f": "Technical Blueprint v1.0",
    "e6c50841f12b044306bd96c4b04c8bb82f734de58d289f5033cda66630dd6aa1": "Relazione Tecnica v1.0",
    "cccc74cd4ab616cf64176e57f28fe967cff8fb056cdf815d88f6da1ec44284b1": "Dossier SIAE v1.0",
    "39c2f12075195f8da64b38f621c1b93c0fbd678b3a4a6a49219f78b2dd679781": "Scheda Mod. 350",
    "8f8077c0e5a65878ced9047dd2bbda4b607e87cf523389594789125d03661280": "Mod. 350 compilato",
}

#: Filenames from the package. Tracking a file with one of these names is a mistake even if the
#: content differs (it would be a copy, an export or a rename).
CONFIDENTIAL_FILENAMES = {
    "italy_legal_entry_master_dossier_v2_0_20-09-2026.docx",
    "italy_legal_entry_technical_blueprint_v1_0_20-09-2026.docx",
    "relazione_tecnica_italy_legal_entry_v1.docx",
    "dossier_siae_italy_legal_entry_v1.docx",
    "scheda_compilazione_mod350_italy_legal_entry.docx",
    "mod_350_deposito_italy_legal_entry_compilato.pdf",
}

#: Public sentinels: text that must not appear in any tracked file outside ALLOWED.
#: - the confidentiality markings, which would mean a confidential document was pasted in;
#: - the deposit form's heading and the SIAE address printed on it, which would mean the form was.
#: The depositant's private identifiers are deliberately absent: see PRIVATE_SENTINELS_VARIABLE.
SENTINEL_PATTERNS: tuple[tuple[str, str], ...] = (
    (r"RISERVATO\s*[-—–]\s*NON DESTINATO ALLA DIFFUSIONE", "Master Dossier confidentiality marking"),
    (r"SPECIFICA TECNICA RISERVATA", "Technical Blueprint confidentiality marking"),
    (r"DEPOSITO OPERA INEDITA", "SIAE deposit form heading"),
    (r"Viale della Letteratura,?\s*30", "SIAE address from the deposit form"),
)

#: Names the private sentinel table: a JSON file OUTSIDE the repository holding a list of
#: [pattern, label] pairs, the depositant's private identifiers. Those patterns are searched in every
#: tracked file, ALLOWED included: no file has a reason to hold them.
PRIVATE_SENTINELS_VARIABLE = "ILE_CONFIDENTIAL_SENTINELS"

#: Files allowed to mention the public sentinels, because their job is to name what must not appear.
ALLOWED = {
    "tests/security/test_confidential_material.py",
    "docs/security/CONFIDENTIAL_MATERIAL_POLICY.md",
    "docs/source-of-truth/CONFIDENTIALITY_REGISTER.md",
    "scripts/document_manifest.py",
}

#: Extensions that never contain prose worth scanning and can be large.
BINARY_SUFFIXES = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".avif",
    ".gif",
    ".ico",
    ".woff",
    ".woff2",
    ".ttf",
    ".otf",
    ".mo",
    ".gz",
    ".zip",
    ".pdf",
}


def tracked_files() -> list[Path]:
    out = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=True,
    )
    return [REPO / name for name in out.stdout.split("\0") if name]


def tracked_text(files: list[Path]):
    """(relative path, text) of every tracked file worth scanning."""
    for path in files:
        if path.suffix.lower() in BINARY_SUFFIXES or not path.is_file():
            continue
        try:
            yield path.relative_to(REPO).as_posix(), path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue


def private_sentinel_patterns() -> tuple[tuple[str, str], ...] | None:
    """
    The private sentinel table, or None when ILE_CONFIDENTIAL_SENTINELS is unset.

    A table that is named but unusable fails the calling test; it never degrades into a skip or a
    pass. Unusable means: no such file, unreadable, not UTF-8 JSON, empty, a row that is not a
    [pattern, label] pair of non-empty strings, a pattern that does not compile, or a file inside the
    repository, where it would be one `git add` away from publication. The messages name the
    variable and the row number, never a pattern.
    """
    location = os.environ.get(PRIVATE_SENTINELS_VARIABLE, "").strip()
    if not location:
        return None
    where = f"{PRIVATE_SENTINELS_VARIABLE} ({location})"
    table = Path(location).expanduser()
    if table.resolve().is_relative_to(REPO):
        pytest.fail(f"{where}: the private sentinel table must live outside the repository")
    try:
        data = table.read_bytes()
    except FileNotFoundError:
        pytest.fail(f"{where}: no such file; a missing table must never look like a pass")
    except OSError as error:
        pytest.fail(f"{where}: unreadable ({type(error).__name__})")
    try:
        rows = json.loads(data.decode("utf-8-sig")) if data.strip() else []
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        pytest.fail(f"{where}: not a UTF-8 JSON document ({type(error).__name__})")
    if not isinstance(rows, list) or not rows:
        pytest.fail(f"{where}: empty, or not a list of [pattern, label] pairs")
    patterns: list[tuple[str, str]] = []
    for number, row in enumerate(rows, start=1):
        if not (
            isinstance(row, list) and len(row) == 2 and all(isinstance(cell, str) and cell.strip() for cell in row)
        ):
            pytest.fail(f"{where}: row {number} is not a [pattern, label] pair of non-empty strings")
        pattern, label = row
        try:
            re.compile(pattern)
        except re.error:
            pytest.fail(f"{where}: row {number} ({label}) is not a valid regular expression")
        patterns.append((pattern, label))
    return tuple(patterns)


@pytest.fixture(scope="module")
def files() -> list[Path]:
    rows = tracked_files()
    assert rows, "git ls-files returned nothing: the test cannot protect an untracked tree"
    return rows


def test_no_confidential_document_is_tracked(files: list[Path]) -> None:
    """No tracked file has the digest of a document from the confidential package."""
    offenders = []
    for path in files:
        if not path.is_file():
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest in CONFIDENTIAL_DIGESTS:
            offenders.append(f"{path.relative_to(REPO)} is {CONFIDENTIAL_DIGESTS[digest]}")
    assert offenders == [], offenders


def test_no_confidential_filename_is_tracked(files: list[Path]) -> None:
    offenders = [str(path.relative_to(REPO)) for path in files if path.name.lower() in CONFIDENTIAL_FILENAMES]
    assert offenders == [], offenders


def test_no_sentinel_text_in_tracked_files(files: list[Path]) -> None:
    """
    No tracked file quotes a confidentiality marking or a personal identifier from the package.

    The public sentinels are searched outside ALLOWED. The private ones, where the private table is
    configured, are searched in every tracked file; elsewhere the next test reports the gap.
    """
    public = [(re.compile(pattern), label) for pattern, label in SENTINEL_PATTERNS]
    private = [(re.compile(pattern), label) for pattern, label in private_sentinel_patterns() or ()]
    offenders = []
    for relative, text in tracked_text(files):
        for pattern, label in private if relative in ALLOWED else public + private:
            if pattern.search(text):
                offenders.append(f"{relative}: {label}")
    assert offenders == [], offenders


def test_the_depositants_private_identifiers_are_checked(files: list[Path]) -> None:
    """
    The private sentinel table is configured and usable here, or the gap is reported, not hidden.

    Without ILE_CONFIDENTIAL_SENTINELS (CI, a fresh clone) the test above searches the public
    sentinels only. This test is then SKIPPED, with the reason in the run summary, so a green run
    never reads as «the depositant's identifiers were checked». With the table, it adds what a regular
    expression does not always catch: a pattern's own source text, pasted back into a tracked file.
    """
    patterns = private_sentinel_patterns()
    if patterns is None:
        pytest.skip(
            f"{PRIVATE_SENTINELS_VARIABLE} is not set: the depositant's private identifiers are checked only "
            "where the private sentinel table (a JSON file outside the repository) is configured"
        )
    offenders = [
        f"{relative}: {label}"
        for relative, text in tracked_text(files)
        for pattern, label in patterns
        if pattern in text
    ]
    assert offenders == [], offenders


#: Tables that are named but cannot be used. Each one must fail, never skip and never pass.
UNUSABLE_TABLES = {
    "no such file": None,
    "a directory": "directory",
    "empty file": b"",
    "empty list": b"[]",
    "not a list": b'{"pattern": "label"}',
    "not JSON": b"[[",
    "not UTF-8": b"\xff\xfe[]",
    "short row": b'[["pattern only"]]',
    "empty pattern": b'[["", "label"]]',
    "invalid regular expression": b'[["(", "label"]]',
}


@pytest.mark.parametrize("content", list(UNUSABLE_TABLES.values()), ids=list(UNUSABLE_TABLES))
def test_a_named_but_unusable_private_table_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, content: bytes | str | None
) -> None:
    table = tmp_path / "confidential_sentinels.json"
    if content == "directory":
        table.mkdir()
    elif content is not None:
        table.write_bytes(content)
    monkeypatch.setenv(PRIVATE_SENTINELS_VARIABLE, str(table))
    with pytest.raises(pytest.fail.Exception):
        private_sentinel_patterns()


def test_a_private_table_inside_the_repository_is_refused(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(PRIVATE_SENTINELS_VARIABLE, str(REPO / "confidential_sentinels.json"))
    with pytest.raises(pytest.fail.Exception):
        private_sentinel_patterns()


def test_a_usable_private_table_is_read_and_an_unset_variable_reads_as_none(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    table = tmp_path / "confidential_sentinels.json"
    table.write_bytes(json.dumps([[r"\bnot-an-identifier\b", "probe"]]).encode("utf-8"))
    monkeypatch.setenv(PRIVATE_SENTINELS_VARIABLE, str(table))
    assert private_sentinel_patterns() == ((r"\bnot-an-identifier\b", "probe"),)
    monkeypatch.delenv(PRIVATE_SENTINELS_VARIABLE)
    assert private_sentinel_patterns() is None


def test_extraction_directory_is_outside_the_repository() -> None:
    """The working extraction of the confidential documents must not live inside the repository."""
    strays = [
        str(path.relative_to(REPO))
        for path in REPO.rglob("docItaly*")
        if ".venv" not in path.parts and ".git" not in path.parts
    ]
    assert strays == [], strays
