"""
scripts/check_ownership.py — the first step of every V5.4 merge (plan §2.2) — and the manifest it reads.

The manifest, docs/design-v5/OWNERSHIP_V54.json, must load (one writer per whole file, every entry with its
source, the ref names of DL54-01) and cover every file plan §3 assigns: the coverage test reads §3's «Owns»
lists from the plan itself, so neither can drift from the other unnoticed. The checker must classify a
family's diff the way the plan says — inside, by slice with a warning, generated, delegated, outside,
steward-only — and on a real git history it must take the family's own commits only (the base's later commits
are not the family's) and see a renamed file at both ends.
"""

from __future__ import annotations

import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_ownership.py"
MANIFEST = ROOT / "docs" / "design-v5" / "OWNERSHIP_V54.json"
PLAN = ROOT / "docs" / "design-v5" / "V5_4_EXECUTION_PLAN.md"


def _load_script():
    spec = importlib.util.spec_from_file_location("ile_check_ownership", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module  # dataclasses look their module up by name
    spec.loader.exec_module(module)
    return module


co = _load_script()


# --------------------------------------------------------------------------------------------- globs


@pytest.mark.parametrize(
    ("pattern", "path", "expected"),
    [
        ("static/css/dist/**", "static/css/dist/main.css", True),
        ("static/css/dist/**", "static/css/dist/pages/css/pages.css", True),
        ("static/css/dist/**", "static/css/main.css", False),
        ("templates/*.html", "templates/base.html", True),
        ("templates/*.html", "templates/pages/home.html", False),
        ("tests/**/test_*_w1_a.py", "tests/test_x_w1_a.py", True),
        ("tests/**/test_*_w1_a.py", "tests/frontend/test_layout_w1_a.py", True),
        ("tests/**/test_*_w1_a.py", "tests/frontend/test_layout_w1_b.py", False),
        ("static/css/v5/{fonts,tokens}.css", "static/css/v5/tokens.css", True),
        ("static/css/v5/{fonts,tokens}.css", "static/css/v5/base.css", False),
        ("**/live_status.json", "live_status.json", True),
        ("**/live_status.json", "apps/designpreview/live_status.json", True),
        ("apps/*/static/**/*.css", "apps/pages/static/pages/css/pages.css", True),
        ("apps/*/static/**/*.css", "apps/pages/static/pages/js/home.js", False),
        ("static/fonts/v5-*", "static/fonts/v5-host-roman.woff2", True),
        ("static/fonts/v5-*", "static/fonts/licenses/OFL.txt", False),
    ],
)
def test_a_glob_means_what_the_manifest_says(pattern, path, expected):
    assert bool(co.compile_glob(pattern).fullmatch(path)) is expected


def test_an_entry_leaves_out_what_it_excepts():
    entry = co.Entry(
        "w3-f1", "templates/pages/**", ("templates/pages/home.html", "templates/pages/home/**"), source="§3.5"
    )
    assert entry.matches("templates/pages/agami.html")
    assert not entry.matches("templates/pages/home.html")
    assert not entry.matches("templates/pages/home/_hero.html")


@pytest.mark.parametrize("pattern", ["", "/etc/passwd", "templates\\base.html", "../outside/file", "a/../b"])
def test_a_glob_that_is_not_a_repository_path_is_refused(pattern):
    with pytest.raises(co.ManifestError):
        co.compile_glob(pattern)


# --------------------------------------------------------------------------------------------- the real manifest


def _section_3() -> str:
    text = PLAN.read_text(encoding="utf-8")
    return text.split("## 3. FAMILY ORDER AND WAVES", 1)[1].split("## 4. PREVIEW AS LIVE PRODUCT", 1)[0]


def test_the_real_manifest_loads_and_is_written_in_lf():
    manifest = co.load_manifest(MANIFEST)
    assert {"steward", "w1-0"} <= set(manifest.families)
    assert b"\r" not in MANIFEST.read_bytes()
    assert co.main(["--validate"]) == 0


def test_every_workflow_of_waves_1_to_4_has_a_family_with_the_dl54_names():
    """Plan §3 lists 24 workflows `v54-<family>`; each is a family here, with DL54-01's branch and tags."""
    workflows = re.findall(r"^\*\*\d+\. `v54-(w\d-[0-9a-z]+)`", _section_3(), flags=re.M)
    assert len(workflows) == 24, workflows
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert set(data["families"]) == {"steward", *workflows}
    for fid, family in data["families"].items():
        if "branch" in family:
            assert family["branch"] == f"v54-{fid}"
            assert family["worktree"] == f"C:/tmp/ile_wt/v54-{fid}"
            assert family["merge_tag"] == f"v54/{fid}"
            assert family["checkpoint_tag"] == f"v54/{fid}-pre-propagation"
    text = MANIFEST.read_text(encoding="utf-8")
    assert "/pre-propagation" not in text, "DL54-01: the checkpoint tag is v54/<family>-pre-propagation"
    assert data["naming"]["base_tag"] == "v54/base"


#: Files an «Owns» list names as what the family's change REFERS to, not as files it writes: W2-C2 and W3-C wire
#: their surfaces onto overlay.js (W2-A's), and W3-A's console.css imports _loader-light.css (W1-D's).
MENTIONS = {("w2-c2", "overlay.js"), ("w3-c", "overlay.js"), ("w3-a", "_loader-light.css")}
PATH_LIKE = re.compile(r"[\w./{}*,-]+")
FILE_SUFFIX = re.compile(r"\.(py|css|js|mjs|html|json|md|svg|txt|woff2)$")


def _owns_lists() -> dict[str, str]:
    lists = {}
    for block in re.split(r"(?=^\*\*\d+\. `v54-w\d-)", _section_3(), flags=re.M):
        header = re.match(r"\*\*\d+\. `v54-(w\d-[0-9a-z]+)`", block)
        owns = re.search(r"^- \*\*Owns:\*\*(.*?)(?=^- \*\*|\Z)", block, flags=re.M | re.S)
        if header and owns:
            lists[header.group(1)] = owns.group(1)
    return lists


def _excluded(owns: str) -> set[str]:
    """The paths an «Owns» list leaves out: «… except `a` and `b`», «(not `c`: …)»."""
    excluded = set()
    for clause in re.finditer(r"\b(?:except|not)\s+((?:`[^`]+`(?:\s*(?:and|,)\s*)?)+)", owns):
        excluded |= set(re.findall(r"`([^`]+)`", clause.group(1)))
    return excluded


def _named_paths(owns: str) -> list[str]:
    named = []
    excluded = _excluded(owns)
    for raw in re.findall(r"`([^`]+)`", owns):
        token = re.sub(r":[0-9][0-9,–\- ]*$", "", raw)  # «test_static_assets.py:133–171» → the file
        if raw in excluded or not PATH_LIKE.fullmatch(token):
            continue
        if "/" in token or FILE_SUFFIX.search(token) or token.startswith("."):
            named.extend(co.expand_braces(token))
    return named


def _covered(token: str, globs: list[str]) -> bool:
    sample = token.replace("**", "x/y").replace("*", "x")
    for glob in globs:
        for pattern in co.expand_braces(glob):
            if pattern == token or pattern.endswith("/" + token):
                return True
            if token.endswith("/") and pattern.startswith(token):
                return True
            if co.compile_glob(pattern).fullmatch(sample if "*" in token else token):
                return True
    return False


def test_the_manifest_covers_every_file_plan_section_3_assigns():
    """
    Every path named in a family's «Owns» list (plan §3.3–§3.5) is in that family's slice of the manifest —
    full paths, globs, brace groups, and the bare names §3 uses for shared files (`components.css`,
    `test_layout.py`) and for tests (`test_v5_tokens.py`) — except what the list itself leaves out.
    """
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    lists = _owns_lists()
    assert {"w1-0", "w1-a", "w1-p", "w2-a", "w2-c2", "w3-e"} <= set(lists), sorted(lists)
    missing = []
    for fid, owns in lists.items():
        globs = [entry["glob"] for entry in data["families"][fid]["owns"]]
        for token in _named_paths(owns):
            if (fid, token) not in MENTIONS and not _covered(token, globs):
                missing.append(f"{fid}: {token}")
    assert not missing, "named in plan §3 but not in the family's slice:\n" + "\n".join(missing)


def test_the_serialized_files_of_section_2_2_are_sliced_not_owned_twice():
    """The files §2.2 serializes have one whole owner at most; everyone else holds a named slice."""
    manifest = co.load_manifest(MANIFEST)
    for path in (
        "static/js/main.js",
        "templates/base.html",
        "static/css/v5/tokens.css",
        "templates/partials/portal_chrome.html",
        "apps/portal/static/portal/console.css",
        "templates/components/form_field.html",
        "tests/frontend/test_layout.py",
        "tests/i18n/test_rtl_browser.py",
        "apps/portal/services.py",
        "apps/cases/services.py",
        "config/settings/dev.py",
    ):
        owners = manifest.owners(path)
        assert len(owners) >= 2, (path, owners)
        whole = {entry.family for entry in owners if entry.whole}
        assert len(whole - {"steward", "w1-0"}) <= 1, (path, whole)
        assert all(entry.slice for entry in owners if entry.family not in whole), path
    assert {e.family for e in manifest.owners("static/js/main.js")} >= {"w1-c", "w1-d", "w2-a", "w2-c1", "w4-b"}
    assert manifest.is_steward_only("package.json") and manifest.is_steward_only("package-lock.json")
    assert manifest.is_generated("static/css/dist/main.css") and manifest.is_generated("static/js/dist/shell.js")


# --------------------------------------------------------------------------------------------- the check


def _small_manifest() -> dict:
    naming = {
        "branch": "v54-<family>",
        "worktree": "C:/tmp/ile_wt/v54-<family>",
        "merge_tag": "v54/<family>",
        "checkpoint_tag": "v54/<family>-pre-propagation",
        "base_tag": "v54/base",
    }

    def family(fid, wave, owns, *, steward=False, delegated=False):
        return {
            "title": fid,
            "wave": wave,
            "plan": "test",
            "branch": f"v54-{fid}",
            "merge_tag": f"v54/{fid}",
            "after": [],
            "steward": steward,
            "delegated": delegated,
            "owns": owns,
        }

    return {
        "schema": "ile-ownership-v54/1",
        "naming": naming,
        "generated": [{"glob": "static/css/dist/**", "source": "test"}],
        "steward_only": [{"glob": "package.json", "source": "test"}],
        "families": {
            "steward": family("steward", 0, [{"glob": "package.json", "source": "test"}], steward=True),
            "w1-a": family(
                "w1-a",
                1,
                [
                    {"glob": "static/css/v5/**", "source": "test"},
                    {"glob": "static/js/main.js", "slice": "initTabs", "source": "test"},
                ],
            ),
            "w2-a": family(
                "w2-a",
                2,
                [
                    {"glob": "static/js/src/overlay.js", "source": "test"},
                    {"glob": "static/js/main.js", "slice": "initDialogs", "source": "test"},
                ],
            ),
            "w4-a": family("w4-a", 4, [{"glob": "docs/qa/w4-a/**", "source": "test"}], delegated=True),
        },
    }


@pytest.fixture
def small(tmp_path):
    path = tmp_path / "manifest.json"
    path.write_bytes(json.dumps(_small_manifest()).encode("utf-8"))
    return co.load_manifest(path)


def test_each_path_of_a_diff_gets_the_verdict_the_plan_gives_it(small):
    changes = [
        ("M", "static/css/v5/tokens.css"),
        ("M", "static/js/main.js"),
        ("M", "static/css/dist/main.css"),
        ("M", "static/js/src/overlay.js"),
        ("A", "nowhere/new.txt"),
        ("M", "package.json"),
    ]
    verdicts = {v.path: v for v in co.classify(small, "w1-a", changes)}
    assert verdicts["static/css/v5/tokens.css"].kind == "inside"
    assert verdicts["static/js/main.js"].kind == "slice"
    assert "«initTabs»" in verdicts["static/js/main.js"].detail
    assert verdicts["static/js/main.js"].others == ["w2-a «initDialogs»"]
    assert verdicts["static/css/dist/main.css"].kind == "generated"
    assert verdicts["static/js/src/overlay.js"].kind == "outside"
    assert verdicts["static/js/src/overlay.js"].others == ["w2-a (whole file)"]
    assert verdicts["nowhere/new.txt"].kind == "outside" and "no family" in verdicts["nowhere/new.txt"].detail
    assert verdicts["package.json"].kind == "steward-only"
    assert [v.path for v in verdicts.values() if v.fails] == [
        "static/js/src/overlay.js",
        "nowhere/new.txt",
        "package.json",
    ]


def test_a_delegated_family_passes_another_family_s_file_and_nothing_else(small):
    changes = [("M", "static/js/src/overlay.js"), ("A", "nowhere/new.txt"), ("M", "package.json")]
    kinds = {v.path: v.kind for v in co.classify(small, "w4-a", changes)}
    assert kinds == {
        "static/js/src/overlay.js": "delegated",
        "nowhere/new.txt": "outside",
        "package.json": "steward-only",
    }
    assert [v.kind for v in co.classify(small, "steward", [("M", "package.json")])] == ["inside"]


@pytest.mark.parametrize(
    ("damage", "complaint"),
    [
        (
            lambda d: d["families"]["w2-a"]["owns"].append({"glob": "static/css/v5/tokens.css", "source": "t"}),
            "owned whole by both",
        ),
        (lambda d: d["families"]["w1-a"].update(branch="v54/w1-a"), "DL54-01"),
        (lambda d: d["naming"].update(checkpoint_tag="v54/<family>/pre-propagation"), "DL54-01"),
        (lambda d: d["families"]["w1-a"]["owns"].append({"glob": "x.py"}), "source"),
        (lambda d: d["families"]["w1-a"]["owns"].append({"glob": "x.py", "source": "t", "owner": "me"}), "unknown key"),
        (lambda d: d["families"]["w1-a"]["owns"].append({"glob": "../x.py", "source": "t"}), "not a repository glob"),
        (lambda d: d["families"]["w1-a"].update(after=["w9-z"]), "unknown family"),
        (lambda d: d["families"]["w1-a"]["owns"].append({"glob": "package.json", "source": "t"}), "steward only"),
        (lambda d: d.update(schema="other"), "schema"),
    ],
)
def test_a_manifest_that_contradicts_itself_does_not_load(tmp_path, damage, complaint):
    data = _small_manifest()
    damage(data)
    path = tmp_path / "manifest.json"
    path.write_bytes(json.dumps(data).encode("utf-8"))
    with pytest.raises(co.ManifestError, match=complaint):
        co.load_manifest(path)


# --------------------------------------------------------------------------------------------- on a real history


def _git(repo: Path, *args: str) -> str:
    """git in a throwaway repository, isolated from this machine's configuration."""
    config = repo.parent / "isolated.gitconfig"
    config.touch()
    env = {
        **os.environ,
        "GIT_CONFIG_GLOBAL": str(config),
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_AUTHOR_NAME": "Test",
        "GIT_AUTHOR_EMAIL": "test@example.test",
        "GIT_COMMITTER_NAME": "Test",
        "GIT_COMMITTER_EMAIL": "test@example.test",
    }
    return subprocess.run(["git", "-C", str(repo), *args], env=env, capture_output=True, text=True, check=True).stdout


def _write(repo: Path, relative: str, text: str) -> None:
    target = repo / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(text.encode("utf-8"))


@pytest.fixture
def history(tmp_path):
    """A base tagged v54/base, a family branch v54-w1-a, and a later commit on the base the family never made."""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q", "-b", "main")
    _write(repo, "manifest.json", json.dumps(_small_manifest()))
    for relative in ("static/css/v5/tokens.css", "static/js/main.js", "static/js/src/overlay.js", "keep.txt"):
        _write(repo, relative, f"{relative}\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "base")
    _git(repo, "tag", "v54/base")
    _git(repo, "checkout", "-q", "-b", "v54-w1-a")
    _write(repo, "static/css/v5/tokens.css", ":root{--x:1}\n")
    _write(repo, "static/js/main.js", "function initTabs() {}\n")
    _write(repo, "static/css/dist/main.css", ":root{--x:1}\n")
    _git(repo, "mv", "keep.txt", "moved.txt")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "family work")
    _git(repo, "checkout", "-q", "main")
    _write(repo, "static/js/src/overlay.js", "export const later = 1;\n")
    _git(repo, "commit", "-q", "-am", "a later commit on the base")
    _git(repo, "checkout", "-q", "v54-w1-a")
    return repo


def _check(repo: Path, *extra: str) -> int:
    return co.main(["w1-a", "v54/base", "--repo", str(repo), "--manifest", str(repo / "manifest.json"), *extra])


def test_on_a_real_history_the_family_s_own_commits_are_checked_and_a_move_counts_twice(history, capsys):
    assert _check(history, "--head", "v54-w1-a") == 1
    out = capsys.readouterr().out
    assert re.search(r"inside +M static/css/v5/tokens\.css", out)
    assert re.search(r"slice +M static/js/main\.js — shared file: w1-a owns only «initTabs»", out)
    assert re.search(r"generated +A static/css/dist/main\.css", out)
    assert re.search(r"OUTSIDE +D keep\.txt", out) and re.search(r"OUTSIDE +A moved\.txt", out)
    assert "overlay.js" not in out, "the base's later commit is not the family's"
    assert "-> FAIL (2 path(s) outside w1-a's slice)" in out

    _git(history, "mv", "moved.txt", "keep.txt")
    _git(history, "commit", "-q", "-m", "put the file back")
    assert _check(history) == 0
    out = capsys.readouterr().out
    assert "-> PASS — read the slice warnings before merging" in out


def test_the_working_tree_mode_sees_what_is_not_committed(history, capsys):
    _git(history, "mv", "moved.txt", "keep.txt")
    _git(history, "commit", "-q", "-m", "put the file back")
    _write(history, "static/css/v5/fonts.css", "/* not committed yet */\n")
    _write(history, "scratch.txt", "untracked\n")
    assert _check(history) == 0, "committed work only, by default"
    capsys.readouterr()
    assert _check(history, "--working-tree") == 1
    out = capsys.readouterr().out
    assert re.search(r"inside +\? static/css/v5/fonts\.css", out)
    assert re.search(r"OUTSIDE +\? scratch\.txt", out)


def test_the_json_report_carries_every_verdict(history, capsys):
    assert _check(history, "--json") == 1
    report = json.loads(capsys.readouterr().out)
    assert report["pass"] is False and report["family"] == "w1-a"
    assert {v["path"]: v["kind"] for v in report["verdicts"]}["moved.txt"] == "outside"


def test_wrong_arguments_answer_2(history, tmp_path, capsys):
    assert co.main(["w1-z", "v54/base", "--repo", str(history), "--manifest", str(history / "manifest.json")]) == 2
    assert _check(history, "--head", "no-such-branch") == 2
    assert co.main(["w1-a", "no-such-tag", "--repo", str(history), "--manifest", str(history / "manifest.json")]) == 2
    broken = tmp_path / "broken.json"
    broken.write_bytes(b"{ not json")
    assert co.main(["--validate", "--manifest", str(broken)]) == 2
    assert co.main(["--manifest", str(history / "manifest.json")]) == 2, "a family and a base, or a mode"
    capsys.readouterr()


def test_list_and_owners_describe_the_real_manifest(capsys):
    assert co.main(["--list", "w1-a"]) == 0
    listing = capsys.readouterr().out
    assert "branch: v54-w1-a" in listing and "checkpoint_tag: v54/w1-a-pre-propagation" in listing
    assert "static/css/v5/{fonts,tokens,aliases,base}.css" in listing
    assert co.main(["--owners", "static/js/main.js", "package.json", "nowhere/at/all.txt"]) == 0
    owners = capsys.readouterr().out
    assert "w1-c «initTabs and initAccordions»" in owners
    assert "package.json: steward (whole file), steward only" in owners
    assert "nowhere/at/all.txt: no owner" in owners
