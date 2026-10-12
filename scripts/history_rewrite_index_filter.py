"""
`git filter-branch --index-filter` body: drop paths and redact values across every commit.

    ILE_REDACTION_TABLE=C:/altrove/redaction.json \
    git filter-branch --index-filter \
        "'.../python.exe' 'scripts/history_rewrite_index_filter.py'" --prune-empty -- --all

**The table of values to redact lives outside the repository, and that is the point.** The first
version of this script hardcoded them. It ran correctly, and afterwards the values were gone from
every file in history except one: this one. A tool that carries the secret it removes re-introduces
the secret, and it does so in the file least likely to be re-read.

The same mistake, in the same session, had already been made by the test that guards the
redaction — which searched for the value it guarded as a literal and so matched itself. Twice is
a pattern: **a redaction tool never names what it redacts.**

Table format, a JSON object:

    {
      "remove_paths": ["docs/source/whatever.pdf", "stray.png"],
      "replacements": [["value to remove", "[REDACTED]"], ...],
      "skip_suffixes": [".png", ".woff2"]
    }

`replacements` is applied IN ORDER, so list the longest form of a value first. A digest that exists
in history at 64, 33 and 14 characters needs all three, longest first: replacing the short form
first consumes the head of the long one and strands the rest of the hex in place. That is not
hypothetical — it is what a trial run on a throwaway clone found.

`skip_suffixes` excludes files from the *text* replacement only. A byte replacement cannot redact
an address that is visible in the pixels of a screenshot, so running it over images buys nothing
and costs the whole image through a pipe once per commit. Images that must go are removed by path,
which `skip_suffixes` does not affect.

Runs once per commit against $GIT_INDEX_FILE and never checks a tree out. Three git processes per
commit — a listing, one batched read of every blob, one batched write — rather than two per file:
the per-file version was still accelerating past twenty minutes on 68 commits.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

TABLE_ENV = "ILE_REDACTION_TABLE"

#: Used only when the table does not say. Media whose bytes a UTF-8 needle cannot meaningfully hit.
DEFAULT_SKIP_SUFFIXES = (
    ".png", ".jpg", ".jpeg", ".webp", ".gif", ".ico", ".pdf",
    ".woff", ".woff2", ".ttf", ".otf", ".eot",
    ".zip", ".gz", ".tar", ".mo", ".pyc",
)


def load_table() -> tuple[list[str], list[tuple[bytes, bytes]], tuple[str, ...]]:
    """
    Read the table, or stop.

    Refusing loudly matters more here than anywhere else: a missing table would make every commit a
    no-op, `filter-branch` would report success on all of them, and the result would be an
    untouched history that everybody believes has been cleaned.
    """
    location = os.environ.get(TABLE_ENV)
    if not location:
        sys.exit(
            f"{TABLE_ENV} is not set. It must point at a JSON redaction table kept OUTSIDE this "
            f"repository. Refusing to run: a silent no-op here looks exactly like a clean rewrite."
        )
    path = Path(location)
    if not path.is_file():
        sys.exit(f"{TABLE_ENV} points at {path}, which is not a file. Refusing to run.")

    data = json.loads(path.read_text(encoding="utf-8"))
    remove_paths = list(data.get("remove_paths", []))
    replacements = [(a.encode("utf-8"), b.encode("utf-8")) for a, b in data.get("replacements", [])]
    skip = tuple(data.get("skip_suffixes", DEFAULT_SKIP_SUFFIXES))
    if not remove_paths and not replacements:
        sys.exit(f"{TABLE_ENV} at {path} asks for nothing to be removed. Refusing to run.")
    return remove_paths, replacements, skip


def git(*args: str, stdin: bytes | None = None, capture: bool = True) -> bytes:
    proc = subprocess.run(
        ["git", *args],
        input=stdin,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0 and b"did not match" not in (proc.stderr or b""):
        sys.stderr.write(f"git {' '.join(args)} -> {proc.returncode}: {proc.stderr!r}\n")
    return proc.stdout or b""


def read_blobs(shas: list[str]) -> dict[str, bytes]:
    """Every blob in one `git cat-file --batch`, instead of one process per file."""
    if not shas:
        return {}
    proc = subprocess.run(
        ["git", "cat-file", "--batch"],
        input=("\n".join(shas) + "\n").encode(),
        capture_output=True,
        check=False,
    )
    out, pos, blobs = proc.stdout, 0, {}
    while pos < len(out):
        newline = out.find(b"\n", pos)
        if newline == -1:
            break
        header = out[pos:newline].split()
        pos = newline + 1
        if len(header) != 3:  # "<sha> missing" and anything unexpected
            continue
        sha, _kind, size = header[0].decode(), header[1], int(header[2])
        blobs[sha] = out[pos : pos + size]
        pos += size + 1  # the trailing newline git adds after the content
    return blobs


def main() -> int:
    remove_paths, replacements, skip_suffixes = load_table()

    if remove_paths:
        git("rm", "--cached", "--ignore-unmatch", "--quiet", "-r", "--", *remove_paths, capture=False)

    if not replacements:
        return 0

    # Every tracked file is a candidate: naming the files that carry a value is the same mistake as
    # naming the value, one step removed.
    entries = []
    for entry in git("ls-files", "-s", "-z").split(b"\0"):
        if not entry:
            continue
        meta, _, path = entry.partition(b"\t")
        mode, sha, _stage = meta.split()
        if path.decode(errors="replace").lower().endswith(skip_suffixes):
            continue
        entries.append((mode.decode(), sha.decode(), path.decode()))

    blobs = read_blobs([sha for _mode, sha, _path in entries])

    updates = []
    for mode, sha, path in entries:
        blob = blobs.get(sha)
        if blob is None:
            continue
        new = blob
        for needle, replacement in replacements:
            new = new.replace(needle, replacement)
        if new == blob:
            continue
        new_sha = git("hash-object", "-w", "--stdin", stdin=new).strip().decode()
        updates.append(f"{mode} {new_sha}\t{path}")

    if updates:
        git("update-index", "--index-info", stdin=("\n".join(updates) + "\n").encode(), capture=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
