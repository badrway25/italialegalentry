"""
Check a V5.4 family's diff against its slice of the ownership manifest (plan §2.2, merge step 1).

    python scripts/check_ownership.py <family> <base-ref> [--head REF] [--working-tree] [--json]
    python scripts/check_ownership.py --list <family>
    python scripts/check_ownership.py --owners <path> [<path> ...]
    python scripts/check_ownership.py --validate

The manifest is docs/design-v5/OWNERSHIP_V54.json (written by W1-0 from the plan's «Owns» lists). For a family
and a base ref — the wave's tag, ``v54/base`` in Wave 1 — the checker lists every path of
``git diff <base>...<head>`` (the family's own changes since it branched; renames counted as a deletion plus an
addition, so a moved file is checked at both ends) and classifies each one:

    inside        the family owns the whole file;
    slice         the family owns a function or a section of a shared file: the file passes, with a warning that
                  names the slice — the steward reads that part of the diff before merging;
    generated     a bundle the steward rebuilds from clean after the merge (static/css/dist, static/js/dist);
    delegated     a Wave-4 family touching a file another family owns: passes, with the owner named;
    OUTSIDE       not in the family's slice (another family's file, or nobody's yet);
    STEWARD-ONLY  package.json, the capture report, live_status.json … — only the steward writes them.

Exit status: 0 when every path passes (warnings may be printed), 1 when at least one is OUTSIDE or STEWARD-ONLY,
2 when the arguments, the refs or the manifest are wrong. ``--working-tree`` checks what is not committed yet as
well (the diff from the merge base to the working tree, plus untracked files): a family can run it before it
asks for the merge.

Function- and section-level slices are checked by file only. That is the honest limit of this tool: it cannot
tell whether a change to static/js/main.js stayed inside ``initTabs``; it says which slice the family holds and
leaves that reading to the steward.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from functools import cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "docs" / "design-v5" / "OWNERSHIP_V54.json"
SCHEMA = "ile-ownership-v54/1"

#: A family id: the steward, a workflow of plan §3's waves (``w<wave>-<name>``), or a family a later directive
#: of the owner added outside the waves — ``devops``, V5.9's production readiness (the devops merge),
#: ``sec-f<n>``, the fix of a go-live security finding F-<n>, named after it (the sec-f5 merge: F-5), and
#: ``intfix``, the steward's integration fixes at an integration checkpoint, V5.5's «full regression only at
#: important integration checkpoints» (the intfix merge: checkpoint 3), and ``rc-fix``, the fixes of what the
#: release candidate's validation found (V5.10's gates; the rc-fix merge: v2.0.0's candidate), and ``v5<nn>-<lane>``,
#: a lane A–D of a later remediation directive (V5.12's four lanes; the v512 W1 merge: v512-a … v512-d; V5.15's
#: visual override, W3: the v515-a, v515-c, v515-b and v515-d merges; V5.18's stabilisation pass, the
#: v518 stabilisation merge: v518-a … v518-d), or its contact lane K (V5.19's owner-confirmed contact
#: channels; the v519-k merge: v519-k), or its
#: privacy lane P (V5.14's privacy and cookie information; the v514-p merge: v514-p), or a later privacy lane
#: P<n> (V5.16's privacy classification; the v516-p2 merge: v516-p2; V5.17's governance correction: v517-p3), and
#: ``v5<nn>g-<group>``, a group of a directive's green suite (V5.18's, under V5.12 §22 «technical tests remain
#: green»: group N the non-browser half and the lint, C the console family, P the public and RTL family; the v518g
#: merge: v518g-n, v518g-c, v518g-p), and ``v5<nn>-wa``, ``v5<nn>-css`` and ``v5<nn>-fixv``, the lanes of a
#: directive's final technical gate (V5.20's, under its strict test-update rule: wa the owner-confirmed WhatsApp
#: number configured outside the repository, css the shared stylesheet back under its budget, fixv the test-change
#: audit's violations fixed in the product; the v520 merge: v520-wa, v520-css, v520-fixv), and ``v5<nn>-s``,
#: ``v5<nn>-m`` and ``v5<nn>-h``, the single-letter lanes of a directive's composition remediation (V5.22's,
#: SECTION_SYSTEM_V2 §9: s the section system's foundation, m the imagery, h the homepage composition; the
#: v522-m merge: v522-m), and ``v5<nn>-p1`` from V5.22 on, the page lane P1 of that remediation (SECTION_SYSTEM_V2
#: §9.4, journeys and spaces; its lane P2 has the privacy lanes' ``v5<nn>-p<n>`` form; below V5.22 ``p1`` stays
#: refused, as no privacy lane was P1; the v522-p1 merge: v522-p1), and ``v5<nn>-s<n>`` (n from 2 to 9) from
#: V5.22 on, a follow-up of that remediation's section-system lane S (its guards and the merge conditions the
#: page lanes set on its modules; lane S itself keeps ``v5<nn>-s``; the v522-s2 merge: v522-s2), and, from V5.24 on,
#: the final-delivery lanes of this file — ``v5<nn>-t``, ``-px``, ``-lib``, ``-home``, ``-pub1``, ``-pub2``, ``-plat``,
#: ``-ar``, ``-closing`` (the Director's FINAL_DELIVERY_V2.md §0 and R11: T typography, PX imagery attribution, LIB the
#: library's material and transitions, HOME, PUB1, PUB2 and PLAT the professional pass per page, AR Arabic completeness,
#: CLOSING the cleanup and the ratchets) and ``-mfix``, the one fix round after the matrix (V5.27 §7); the v524-px
#: merge: v524-px; and ``-cifix``, the steward's fix of the published branch's CI reds (V5.28; the v524-cifix merge);
#: and ``-sys``, the owner's V5.29 shared visual system stream (the ink roles, the weight map, the grounds, the plate,
#: the icon tile, the compact «la protezione»; the v524-sys merge); and ``-brand``, the owner's V5.29 «small layout &
#: brand refinement» stream (the shell's three related widths, the forms, the lock-up and its key; the v524-brand
#: merge).
FAMILY_ID = re.compile(
    r"steward|devops|intfix|rc-fix|sec-f[0-9]+|w[0-9]-[0-9a-z]+|v5[0-9]{2}-(?:[a-dk]|p[2-9]?)|v5[0-9]{2}g-[cnp]"
    r"|v5[0-9]{2}-(?:wa|css|fixv)|v5[0-9]{2}-[hms]|v5(?:2[2-9]|[3-9][0-9])-(?:p1|s[2-9])"
    r"|v5(?:2[4-9]|[3-9][0-9])-(?:t|px|lib|home|pub[12]|plat|ar|closing|mfix|cifix|sys|brand|art|agami|integ|land)"
)
TOP_KEYS = {
    "schema",
    "title",
    "plan",
    "written",
    "writer",
    "checker",
    "naming",
    "rules",
    "generated",
    "steward_only",
    "families",
}
REQUIRED_TOP_KEYS = {"schema", "naming", "generated", "steward_only", "families"}
FAMILY_KEYS = {
    "title",
    "wave",
    "plan",
    "workflow",
    "branch",
    "worktree",
    "merge_tag",
    "checkpoint_tag",
    "after",
    "merges_after",
    "steward",
    "delegated",
    "note",
    "owns",
}
REQUIRED_FAMILY_KEYS = {"title", "wave", "plan", "after", "steward", "delegated", "owns"}
ENTRY_KEYS = {"glob", "except", "slice", "source", "note"}

#: DL54-01: the ref names, per family. A manifest that names a ref otherwise does not load.
NAMING = {
    "branch": "v54-{family}",
    "worktree": "C:/tmp/ile_wt/v54-{family}",
    "merge_tag": "v54/{family}",
    "checkpoint_tag": "v54/{family}-pre-propagation",
}
BASE_TAG = "v54/base"


class ManifestError(Exception):
    """The manifest cannot be read, or contradicts itself."""


# --------------------------------------------------------------------------------------------- globs


def expand_braces(pattern: str) -> list[str]:
    """``a/{b,c}/d`` → ``a/b/d``, ``a/c/d`` (innermost first, so nested braces expand too)."""
    match = re.search(r"\{([^{}]*)\}", pattern)
    if not match:
        return [pattern]
    head, tail = pattern[: match.start()], pattern[match.end() :]
    expanded: list[str] = []
    for option in match.group(1).split(","):
        expanded.extend(expand_braces(head + option + tail))
    return expanded


def _glob_regex(pattern: str) -> str:
    out: list[str] = []
    i = 0
    while i < len(pattern):
        if pattern.startswith("**/", i):
            out.append("(?:[^/]+/)*")  # any number of directories, none included
            i += 3
        elif pattern.startswith("**", i):
            out.append(".*")
            i += 2
        elif pattern[i] == "*":
            out.append("[^/]*")
            i += 1
        elif pattern[i] == "?":
            out.append("[^/]")
            i += 1
        else:
            out.append(re.escape(pattern[i]))
            i += 1
    return "".join(out)


@cache
def compile_glob(pattern: str) -> re.Pattern[str]:
    """A repository glob: POSIX, from the root; ``*`` stays in a directory, ``**`` crosses any number."""
    if not pattern or pattern.startswith("/") or "\\" in pattern or ".." in pattern.split("/"):
        raise ManifestError(f"not a repository glob: {pattern!r}")
    return re.compile("(?:" + "|".join(_glob_regex(p) for p in expand_braces(pattern)) + ")")


def is_literal(pattern: str) -> bool:
    return not any(ch in pattern for ch in "*?{")


# --------------------------------------------------------------------------------------------- the manifest


@dataclass(frozen=True)
class Entry:
    family: str
    glob: str
    excepts: tuple[str, ...] = ()
    slice: str | None = None
    source: str = ""
    note: str | None = None

    def matches(self, path: str) -> bool:
        if not compile_glob(self.glob).fullmatch(path):
            return False
        return not any(compile_glob(pattern).fullmatch(path) for pattern in self.excepts)

    @property
    def whole(self) -> bool:
        return self.slice is None

    def describe(self) -> str:
        return f"{self.family} «{self.slice}»" if self.slice else f"{self.family} (whole file)"


@dataclass
class Family:
    id: str
    title: str
    steward: bool
    delegated: bool
    entries: list[Entry]
    data: dict = field(repr=False)


@dataclass
class Manifest:
    families: dict[str, Family]
    generated: list[Entry]
    steward_only: list[Entry]
    path: Path

    def owners(self, path: str) -> list[Entry]:
        return [entry for family in self.families.values() for entry in family.entries if entry.matches(path)]

    def is_generated(self, path: str) -> bool:
        return any(entry.matches(path) for entry in self.generated)

    def is_steward_only(self, path: str) -> bool:
        return any(entry.matches(path) for entry in self.steward_only)


def _entry_problems(where: str, raw: object) -> list[str]:
    if not isinstance(raw, dict):
        return [f"{where}: an entry must be an object"]
    problems = [f"{where}: unknown key {key!r}" for key in sorted(set(raw) - ENTRY_KEYS)]
    if not isinstance(raw.get("glob"), str) or not raw["glob"]:
        problems.append(f"{where}: «glob» must be a non-empty string")
    if not isinstance(raw.get("source"), str) or not raw["source"]:
        problems.append(f"{where}: «source» must name where the assignment comes from")
    if "slice" in raw and (not isinstance(raw["slice"], str) or not raw["slice"]):
        problems.append(f"{where}: «slice» must be a non-empty string")
    if "except" in raw and (not isinstance(raw["except"], list) or not all(isinstance(x, str) for x in raw["except"])):
        problems.append(f"{where}: «except» must be a list of globs")
    for pattern in [raw.get("glob")] + list(raw.get("except") or []):
        if isinstance(pattern, str) and pattern:
            try:
                compile_glob(pattern)
            except ManifestError as exc:
                problems.append(f"{where}: {exc}")
    return problems


def _entry(family: str, raw: dict) -> Entry:
    return Entry(
        family=family,
        glob=raw["glob"],
        excepts=tuple(raw.get("except") or ()),
        slice=raw.get("slice"),
        source=raw.get("source", ""),
        note=raw.get("note"),
    )


def validate_data(data: object) -> list[str]:
    """Every problem the manifest has, as sentences; an empty list when it is coherent."""
    if not isinstance(data, dict):
        return ["the manifest must be a JSON object"]
    problems = [f"unknown top-level key {key!r}" for key in sorted(set(data) - TOP_KEYS)]
    problems += [f"missing top-level key {key!r}" for key in sorted(REQUIRED_TOP_KEYS - set(data))]
    if problems:
        return problems
    if data["schema"] != SCHEMA:
        problems.append(f"schema is {data['schema']!r}, expected {SCHEMA!r}")
    naming = data["naming"]
    if not isinstance(naming, dict):
        problems.append("«naming» must be an object")
    else:
        for key, form in {**NAMING, "base_tag": BASE_TAG}.items():
            if naming.get(key) != form.replace("{family}", "<family>"):
                problems.append(f"naming.{key} must be {form.replace('{family}', '<family>')!r} (DL54-01)")
    for section in ("generated", "steward_only"):
        if not isinstance(data[section], list) or not data[section]:
            problems.append(f"«{section}» must be a non-empty list of entries")
            continue
        for index, raw in enumerate(data[section]):
            problems += _entry_problems(f"{section}[{index}]", raw)
    families = data["families"]
    if not isinstance(families, dict) or not families:
        return [*problems, "«families» must be a non-empty object"]
    for fid, raw in families.items():
        where = f"families.{fid}"
        if not FAMILY_ID.fullmatch(fid):
            problems.append(
                f"{where}: not a family id "
                "(steward, devops, intfix, rc-fix, sec-f<n>, w<wave>-<name>, v5<nn>-<lane>, v5<nn>g-<group>, "
                "v5<nn>-wa, v5<nn>-css, v5<nn>-fixv, or from V5.24 on a final-delivery lane v5<nn>-t, -px, -lib, "
                "-home, -pub1, -pub2, -plat, -ar, -closing, -mfix, -cifix, -sys, -brand, -art, -agami, -integ, -land)"
            )
        if not isinstance(raw, dict):
            problems.append(f"{where}: must be an object")
            continue
        problems += [f"{where}: unknown key {key!r}" for key in sorted(set(raw) - FAMILY_KEYS)]
        problems += [f"{where}: missing key {key!r}" for key in sorted(REQUIRED_FAMILY_KEYS - set(raw))]
        if not isinstance(raw.get("title"), str) or not raw.get("title"):
            problems.append(f"{where}: «title» must be a non-empty string")
        if not isinstance(raw.get("wave"), int):
            problems.append(f"{where}: «wave» must be an integer")
        for flag in ("steward", "delegated"):
            if not isinstance(raw.get(flag), bool):
                problems.append(f"{where}: «{flag}» must be true or false")
        for key in ("after", "merges_after"):
            value = raw.get(key, [])
            if not isinstance(value, list) or not all(isinstance(x, str) for x in value):
                problems.append(f"{where}: «{key}» must be a list of family ids")
                continue
            problems += [f"{where}: «{key}» names an unknown family {x!r}" for x in value if x not in families]
        for key, form in NAMING.items():
            if key in raw and raw[key] != form.format(family=fid):
                problems.append(f"{where}: «{key}» is {raw[key]!r}, DL54-01 says {form.format(family=fid)!r}")
        owns = raw.get("owns")
        if not isinstance(owns, list) or not owns:
            problems.append(f"{where}: «owns» must be a non-empty list")
            continue
        for index, entry in enumerate(owns):
            problems += _entry_problems(f"{where}.owns[{index}]", entry)
    if problems:
        return problems
    return _conflicts(data)


def _conflicts(data: dict) -> list[str]:
    """
    One writer per file: a literal path owned WHOLE by two families is a contradiction, unless both are the
    steward's (W1-0 and the steward share their tools). Slices may overlap — that is what a serialized file is.
    A family that owns a steward-only path whole contradicts the steward-only list.
    """
    entries = {fid: [_entry(fid, raw) for raw in family["owns"]] for fid, family in data["families"].items()}
    steward = {fid for fid, family in data["families"].items() if family["steward"]}
    steward_only = [_entry("steward_only", raw) for raw in data["steward_only"]]
    problems: list[str] = []
    seen: set[tuple[str, str, str]] = set()
    for fid, own in entries.items():
        for entry in own:
            if not entry.whole:
                continue
            for literal in (p for p in expand_braces(entry.glob) if is_literal(p)):
                if entry.excepts and any(compile_glob(x).fullmatch(literal) for x in entry.excepts):
                    continue
                if fid not in steward and any(other.matches(literal) for other in steward_only):
                    problems.append(f"{literal}: owned whole by {fid}, but the manifest says steward only")
                for other_id, other_entries in entries.items():
                    if other_id == fid or (fid in steward and other_id in steward):
                        continue
                    for other in other_entries:
                        if other.whole and other.matches(literal):
                            key = (literal, *sorted((fid, other_id)))
                            if key not in seen:
                                seen.add(key)
                                problems.append(f"{literal}: owned whole by both {fid} and {other_id}")
    return problems


def load_manifest(path: Path = MANIFEST) -> Manifest:
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ManifestError(f"{path}: {exc}") from exc
    problems = validate_data(data)
    if problems:
        raise ManifestError(f"{path}:\n  " + "\n  ".join(problems))
    families = {
        fid: Family(
            id=fid,
            title=raw["title"],
            steward=raw["steward"],
            delegated=raw["delegated"],
            entries=[_entry(fid, entry) for entry in raw["owns"]],
            data=raw,
        )
        for fid, raw in data["families"].items()
    }
    return Manifest(
        families=families,
        generated=[_entry("generated", raw) for raw in data["generated"]],
        steward_only=[_entry("steward_only", raw) for raw in data["steward_only"]],
        path=Path(path),
    )


# --------------------------------------------------------------------------------------------- the check


@dataclass
class Verdict:
    status: str  # the git status letter (A, M, D, T, …; ? for an untracked file)
    path: str
    kind: str  # inside · slice · generated · delegated · outside · steward-only
    detail: str
    others: list[str]

    @property
    def fails(self) -> bool:
        return self.kind in {"outside", "steward-only"}

    @property
    def warns(self) -> bool:
        return self.kind in {"slice", "delegated"}


def _grouped(entries: list[Entry]) -> list[str]:
    """Other owners, one line per slice: «w1-a, w1-b and 20 more «append-only: …»», «w3-a (whole file)»."""
    groups: dict[str | None, list[str]] = {}
    for entry in entries:
        names = groups.setdefault(entry.slice, [])
        if entry.family not in names:
            names.append(entry.family)
    described = []
    for slice_, names in groups.items():
        who = ", ".join(names) if len(names) <= 3 else f"{', '.join(names[:2])} and {len(names) - 2} more"
        described.append(f"{who} «{slice_}»" if slice_ else f"{who} (whole file)")
    return described


def classify(manifest: Manifest, family_id: str, changes: list[tuple[str, str]]) -> list[Verdict]:
    family = manifest.families[family_id]
    verdicts: list[Verdict] = []
    for status, path in changes:
        owners = manifest.owners(path)
        own = [entry for entry in owners if entry.family == family_id]
        others = _grouped([entry for entry in owners if entry.family != family_id])
        if manifest.is_generated(path):
            verdicts.append(
                Verdict(status, path, "generated", "rebuilt from clean by the steward after the merge", others)
            )
        elif manifest.is_steward_only(path) and not family.steward:
            verdicts.append(Verdict(status, path, "steward-only", "only the steward writes this file", others))
        elif any(entry.whole for entry in own):
            verdicts.append(Verdict(status, path, "inside", "", others))
        elif own:
            slices = "; ".join(f"«{entry.slice}»" for entry in own)
            detail = f"shared file: {family_id} owns only {slices} — the steward checks the diff stays inside it"
            verdicts.append(Verdict(status, path, "slice", detail, others))
        elif family.delegated and owners:
            detail = f"owned by {', '.join(others)}; {family_id} is delegated: the fix lands through the steward"
            verdicts.append(Verdict(status, path, "delegated", detail, others))
        elif owners:
            verdicts.append(Verdict(status, path, "outside", f"not in {family_id}'s slice", others))
        else:
            detail = "in no family's slice: the steward assigns it in the manifest before the merge"
            verdicts.append(Verdict(status, path, "outside", detail, others))
    return verdicts


def _git(repo: Path, *args: str) -> bytes:
    result = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, check=False)  # noqa: S603, S607
    if result.returncode != 0:
        message = result.stderr.decode("utf-8", "replace").strip() or f"git {' '.join(args)} failed"
        raise ManifestError(message)
    return result.stdout


def _resolve(repo: Path, ref: str) -> str:
    return _git(repo, "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}").decode().strip()


def _name_status(raw: bytes) -> list[tuple[str, str]]:
    items = raw.split(b"\0")
    changes = []
    for status, path in zip(items[0::2], items[1::2], strict=False):
        if status and path:
            changes.append((status.decode()[0], path.decode("utf-8")))
    return changes


def diff_paths(
    repo: Path, base: str, head: str = "HEAD", working_tree: bool = False
) -> tuple[str, list[tuple[str, str]]]:
    """The family's own changes: from the merge base of ``base`` and ``head`` to ``head`` (or the working tree)."""
    base_commit = _resolve(repo, base)
    head_commit = _resolve(repo, head)
    merge_base = _git(repo, "merge-base", base_commit, head_commit).decode().strip()
    if working_tree:
        changes = _name_status(_git(repo, "diff", "--name-status", "--no-renames", "-z", merge_base))
        untracked = _git(repo, "ls-files", "--others", "--exclude-standard", "-z").split(b"\0")
        changes += [("?", path.decode("utf-8")) for path in untracked if path]
    else:
        changes = _name_status(
            _git(repo, "diff", "--name-status", "--no-renames", "-z", f"{merge_base}..{head_commit}")
        )
    return merge_base, sorted(set(changes), key=lambda change: (change[1], change[0]))


LABELS = {
    "inside": "inside",
    "slice": "slice",
    "generated": "generated",
    "delegated": "delegated",
    "outside": "OUTSIDE",
    "steward-only": "STEWARD-ONLY",
}


def report(family: Family, base: str, head: str, merge_base: str, verdicts: list[Verdict]) -> str:
    lines = [
        f"check_ownership: {family.id} — {family.title}",
        f"diff {base}...{head} (merge base {merge_base[:12]}): {len(verdicts)} path(s)",
    ]
    for verdict in verdicts:
        line = f"  {LABELS[verdict.kind]:<13} {verdict.status} {verdict.path}"
        if verdict.detail:
            line += f" — {verdict.detail}"
        if verdict.others and verdict.kind in {"slice", "outside"}:
            line += f" [also: {', '.join(verdict.others)}]"
        lines.append(line)
    counts = {kind: sum(1 for v in verdicts if v.kind == kind) for kind in LABELS}
    failed = counts["outside"] + counts["steward-only"]
    lines.append(
        "summary: "
        + ", ".join(f"{counts[kind]} {LABELS[kind].lower()}" for kind in LABELS if counts[kind])
        + (f" -> FAIL ({failed} path(s) outside {family.id}'s slice)" if failed else " -> PASS")
        + (
            " — read the slice warnings before merging"
            if not failed and (counts["slice"] or counts["delegated"])
            else ""
        )
    )
    return "\n".join(lines)


def describe_family(family: Family) -> str:
    data = family.data
    lines = [f"{family.id} — {family.title} (wave {data['wave']}; plan {data['plan']})"]
    for key in ("branch", "worktree", "merge_tag", "checkpoint_tag"):
        if key in data:
            lines.append(f"  {key}: {data[key]}")
    if data.get("after"):
        lines.append(f"  after: {', '.join(data['after'])}")
    if data.get("merges_after"):
        lines.append(f"  merges after: {', '.join(data['merges_after'])}")
    flags = [name for name in ("steward", "delegated") if data.get(name)]
    if flags:
        lines.append(f"  flags: {', '.join(flags)}")
    if data.get("note"):
        lines.append(f"  note: {data['note']}")
    for entry in family.entries:
        line = f"  - {entry.glob}"
        if entry.excepts:
            line += f" (except {', '.join(entry.excepts)})"
        if entry.slice:
            line += f" — slice: {entry.slice}"
        lines.append(line + f"   [{entry.source}]")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check a V5.4 family's diff against its slice of docs/design-v5/OWNERSHIP_V54.json."
    )
    parser.add_argument("family", nargs="?", help="the family id, e.g. w1-a")
    parser.add_argument("base", nargs="?", help="the base ref: the wave's tag (v54/base in Wave 1)")
    parser.add_argument("--head", default="HEAD", help="the family's branch or commit (default: HEAD)")
    parser.add_argument("--working-tree", action="store_true", help="also check uncommitted and untracked files")
    parser.add_argument("--json", action="store_true", help="print the verdicts as JSON")
    parser.add_argument("--manifest", type=Path, default=MANIFEST, help=argparse.SUPPRESS)
    parser.add_argument("--repo", type=Path, default=ROOT, help=argparse.SUPPRESS)
    parser.add_argument("--list", metavar="FAMILY", help="print a family's slice")
    parser.add_argument("--owners", nargs="+", metavar="PATH", help="print who owns each path")
    parser.add_argument("--validate", action="store_true", help="check that the manifest parses and is coherent")
    args = parser.parse_args(argv)
    for stream in (sys.stdout, sys.stderr):
        # A Windows console's code page cannot print every character of the manifest («→»): replace, never crash.
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="replace")

    try:
        manifest = load_manifest(args.manifest)
    except ManifestError as exc:
        print(f"check_ownership: the manifest does not load: {exc}", file=sys.stderr)
        return 2

    if args.validate:
        entries = sum(len(family.entries) for family in manifest.families.values())
        print(
            f"check_ownership: {manifest.path.name} is coherent: {len(manifest.families)} families, {entries} entries"
        )
        return 0
    if args.list:
        if args.list not in manifest.families:
            print(
                f"check_ownership: unknown family {args.list!r}; known: {', '.join(manifest.families)}", file=sys.stderr
            )
            return 2
        print(describe_family(manifest.families[args.list]))
        return 0
    if args.owners:
        for path in args.owners:
            path = path.replace("\\", "/").removeprefix("./")
            owners = manifest.owners(path)
            tags = [
                tag
                for tag, hit in (
                    ("generated", manifest.is_generated(path)),
                    ("steward only", manifest.is_steward_only(path)),
                )
                if hit
            ]
            print(f"{path}: " + (", ".join([entry.describe() for entry in owners] + tags) or "no owner"))
        return 0
    if not args.family or not args.base:
        parser.print_usage(sys.stderr)
        print("check_ownership: give a family and a base ref, or --list / --owners / --validate", file=sys.stderr)
        return 2
    if args.family not in manifest.families:
        print(
            f"check_ownership: unknown family {args.family!r}; known: {', '.join(manifest.families)}", file=sys.stderr
        )
        return 2
    try:
        merge_base, changes = diff_paths(args.repo, args.base, args.head, args.working_tree)
    except ManifestError as exc:
        print(f"check_ownership: git: {exc}", file=sys.stderr)
        return 2
    verdicts = classify(manifest, args.family, changes)
    if args.json:
        print(
            json.dumps(
                {
                    "family": args.family,
                    "base": args.base,
                    "head": args.head,
                    "merge_base": merge_base,
                    "pass": not any(v.fails for v in verdicts),
                    "verdicts": [v.__dict__ for v in verdicts],
                },
                indent=1,
            )
        )
    else:
        print(report(manifest.families[args.family], args.base, args.head, merge_base, verdicts))
    return 1 if any(v.fails for v in verdicts) else 0


if __name__ == "__main__":
    raise SystemExit(main())
