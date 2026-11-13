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


#: The families a later directive of the owner added outside plan §3's waves: ``devops``, V5.9's production
#: readiness (the devops merge), ``sec-f5``, the fix of the DevOps lane's go-live finding F-5 (the sec-f5 merge),
#: ``intfix``, the steward's integration fixes at integration checkpoint 3 (the intfix merge), ``sec-f7``, the
#: fix of W3-D's review finding F-7, who may move a case file (the sec-f7 merge), and ``sec-f8``, the fix of F-8, the
#: back office granting no more than the platform (the sec-f8 merge; V5.10's release blocker), and ``rc-fix``, the
#: fixes of what the release candidate's validation found (the rc-fix merge). DL54-01's branch and worktree names; no
#: merge tag of their own in the manifest (the checkpoint's tag, v54/checkpoint-3, and the rc-fix merge's v54/rc-fix
#: mark design-v5), and ``v512-a`` … ``v512-d``, the four lanes of the owner's V5.12 remediation (the v512 W1 merge;
#: their branches v512-<lane>-w1 are named in each family's note, the tag v512/w1 marks design-v5), and ``v514-p``,
#: the privacy lane of the owner's V5.14 (the v514-p merge; branch v514-p in its note, the tag v514/privacy marks
#: design-v5), and ``v516-p2``, the privacy classification lane of the owner's V5.16 (the v516-p2 merge; branch
#: v516-p2 in its note, the tag v516/privacy-classification marks design-v5), and ``v517-p3``, the privacy governance
#: correction lane of the owner's V5.17 (the v517-p3 merge; branch v517-p3 in its note, the tag v517/compliance
#: marks design-v5), and ``v515-a``, lane A of the owner's V5.15 visual override, W3 (the v515-a merge; branch v515-a
#: in its note, the tag v515/a marks design-v5), and ``v515-c``, lane C of the same W3 (the v515-c merge; branch v515-c
#: in its note, the tag v515/c marks design-v5), and ``v515-b``, lane B of the same W3 (the v515-b merge; branch v515-b
#: in its note, the tag v515/b marks design-v5), and ``v515-d``, lane D of the same W3 (the v515-d merge; branch v515-d
#: in its note, the tag v515/d marks design-v5), and ``v518-a`` … ``v518-d``, the four lanes of the owner's V5.18
#: stabilisation pass (the v518 stabilisation merge; branches v518-<lane> in each family's note, the tag
#: v518/stabilisation marks design-v5), and ``v519-k``, the contact lane K of the owner's V5.19 (the v519-k merge;
#: branch v519-k in its note, the tag v519/contact marks design-v5), and ``v518g-n``, ``v518g-c`` and ``v518g-p``,
#: groups N, C and P of the owner's V5.18 green suite (the v518g merge; branches v518g-<group> in each family's note,
#: the tag v518/green marks design-v5), and ``v520-wa``, ``v520-css`` and ``v520-fixv``, lanes WA, CSS and FIXV of the
#: owner's V5.20 final technical gate (the v520 merge; branches v520-<lane> in each family's note, the tag v520/gate
#: marks design-v5), and ``v522-m``, the imagery lane M of the owner's V5.22 composition remediation (the v522-m merge;
#: branch v522-m in its note, the tag v522/m marks design-v5), and ``v522-s``, the section-system lane S of the same
#: remediation (the v522-s merge; branch v522-s in its note, the tag v522/s marks design-v5), and ``v522-p1``, the page
#: lane P1 of the same remediation, journeys and spaces (the v522-p1 merge; branch v522-p1 in its note, the tag v522/p1
#: marks design-v5), and ``v522-s2``, the follow-up of lane S of the same remediation, its guards and the page lanes'
#: merge conditions on its modules (the v522-s2 merge; branch v522-s2 in its note, the tag v522/s2 marks design-v5), and
#: ``v522-h``, the homepage lane H of the same remediation, Homepage Composition V2 (the v522-h merge; branch v522-h in
#: its note, the tag v522/h marks design-v5), and ``v522-p2``, the page lane P2 of the same remediation, system, trust
#: and reading (the v522-p2 merge; branch v522-p2 in its note, the tag v522/p2 marks design-v5), and ``v524-px``, the
#: imagery-attribution lane PX of the owner's V5.24 final delivery, first in the Director's merge order
#: (FINAL_DELIVERY_V2.md R11; the v524-px merge; branch v524-px in its note, the tag v524/px marks design-v5), and
#: ``v524-t``, the typography lane T of the same final delivery, second in the Director's merge order
#: (FINAL_DELIVERY_V2.md R1, R11; the v524-t merge; branch v524-t in its note, the tag v524/t marks design-v5), and
#: ``v524-lib``, the library lane LIB of the same final delivery, third in the Director's merge order
#: (FINAL_DELIVERY_V2.md R3, R11, §3.3; the v524-lib merge; branch v524-lib in its note, the tag v524/lib marks
#: design-v5), and ``v524-ar``, the Arabic completeness lane AR of the same final delivery under the owner's Arabic
#: decision V5.27 (FINAL_DELIVERY_V2.md R7', R11, §3.8; the v524-ar merge; branch v524-ar in its note, the tag v524/ar
#: marks design-v5), and ``v524-home``, the homepage lane HOME of the same final delivery (FINAL_DELIVERY_V2.md §3.4,
#: R11; merged through branch v524-sys, no tag of its own), and ``v524-sys``, the owner's V5.29 shared visual system
#: stream (V5.29 §1–§9, §18–§19; the v524-sys merge; branch v524-sys in its note, the tag v524/sys marks design-v5), and
#: ``v524-pub1``, the journeys-and-spaces lane PUB1 of the same final delivery with the owner's V5.29 «l'intesa»
#: (FINAL_DELIVERY_V2.md §3.5, R11; the v524-pub1 merge; branch v524-pub1 in its note, the tag v524/pub1 marks
#: design-v5), and ``v524-pub2``, the system-trust-and-reading lane PUB2 of the same final delivery with the owner's
#: V5.29 FAQ (FINAL_DELIVERY_V2.md §3.6, R11; the v524-pub2 merge; branch v524-pub2 in its note, the tag v524/pub2 marks
#: design-v5), and ``v524-brand``, the owner's V5.29 «small layout & brand refinement» stream (the shell, the forms, the
#: lock-up and its key; the v524-brand merge; branch v524-brand in its note, the tag v524/brand marks design-v5), and
#: ``v524-plat``, the platform lane PLAT of the same final delivery, typography only (FINAL_DELIVERY_V2.md §3.7, R8,
#: R11; the v524-plat merge; branch v524-plat in its note, the tag v524/plat marks design-v5), and ``v524-closing``, the
#: cleanup lane CLOSING of the same final delivery, with the owner's V5.29 closing gate corrections
#: (FINAL_DELIVERY_V2.md §3.9, R11; the v524-closing merge; branch v524-closing in its note, the tag v524/closing marks
#: design-v5).
OUTSIDE_THE_WAVES = {
    "devops", "sec-f5", "intfix", "sec-f7", "sec-f8", "rc-fix", "v512-a", "v512-b", "v512-c", "v512-d", "v514-p",
    "v516-p2", "v517-p3", "v515-a", "v515-c", "v515-b", "v515-d", "v518-a", "v518-b", "v518-c", "v518-d",
    "v519-k", "v518g-n", "v518g-c", "v518g-p",
    "v520-wa", "v520-css", "v520-fixv",
    "v522-m", "v522-s", "v522-p1", "v522-s2", "v522-h", "v522-p2",
    "v524-px", "v524-t", "v524-lib", "v524-cifix", "v524-ar", "v524-home", "v524-sys",
    "v524-pub1", "v524-pub2", "v524-brand", "v524-plat", "v524-closing",
    "v530-agami", "v530-plat", "v530-art", "v530-integ", "v530-mfix", "v530-sys", "v530-cifix", "v530-a", "v530-b",
    "v530-c", "v530-d", "v530-ar",
}


def test_every_workflow_of_waves_1_to_4_has_a_family_with_the_dl54_names():
    """
    Plan §3 lists 24 workflows `v54-<family>`; each is a family here, with DL54-01's branch and tags — beside the
    steward and the families outside the waves, which keep DL54-01's branch and worktree names.
    """
    workflows = re.findall(r"^\*\*\d+\. `v54-(w\d-[0-9a-z]+)`", _section_3(), flags=re.M)
    assert len(workflows) == 24, workflows
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert set(data["families"]) == {"steward", *workflows, *OUTSIDE_THE_WAVES}
    for fid, family in data["families"].items():
        if "branch" in family:
            assert family["branch"] == f"v54-{fid}"
            assert family["worktree"] == f"C:/tmp/ile_wt/v54-{fid}"
            if fid in OUTSIDE_THE_WAVES:
                assert "merge_tag" not in family and "checkpoint_tag" not in family, fid
                continue
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
        (lambda d: d["families"].update(ops=d["families"].pop("w4-a")), "not a family id"),
    ],
)
def test_a_manifest_that_contradicts_itself_does_not_load(tmp_path, damage, complaint):
    data = _small_manifest()
    damage(data)
    path = tmp_path / "manifest.json"
    path.write_bytes(json.dumps(data).encode("utf-8"))
    with pytest.raises(co.ManifestError, match=complaint):
        co.load_manifest(path)


@pytest.mark.parametrize(
    ("fid", "valid"),
    [
        ("steward", True),
        ("w3-f2", True),
        ("devops", True),
        ("sec-f5", True),
        ("sec-f7", True),
        ("intfix", True),
        ("rc-fix", True),
        ("v512-a", True),
        ("v512-d", True),
        ("v514-p", True),
        ("v516-p2", True),
        ("v517-p3", True),
        ("v515-a", True),
        ("v515-c", True),
        ("v515-b", True),
        ("v515-d", True),
        ("v518-a", True),
        ("v518-b", True),
        ("v518-c", True),
        ("v518-d", True),
        ("v519-k", True),
        ("v518g-n", True),
        ("v518g-c", True),
        ("v518g-p", True),
        ("v520-wa", True),
        ("v520-css", True),
        ("v520-fixv", True),
        ("v522-s", True),
        ("v522-m", True),
        ("v522-h", True),
        ("v522-p1", True),
        ("v522-p2", True),
        ("v522-s2", True),
        # V5.24 final delivery (FINAL_DELIVERY_V2.md R11; V5.20 cited: cases added, none changed): the nine lanes and
        # the one fix round, from V5.24 on
        ("v524-t", True),
        ("v524-px", True),
        ("v524-lib", True),
        ("v524-home", True),
        ("v524-pub1", True),
        ("v524-pub2", True),
        ("v524-plat", True),
        ("v524-ar", True),
        ("v524-closing", True),
        ("v524-mfix", True),
        ("v529-px", True),
        ("v530-closing", True),
        # the v524-cifix merge (V5.20 cited: cases added, none changed): the CI fix of the published branch, and its
        # near-misses
        ("v524-cifix", True),
        ("v531-cifix", True),
        # the v524-sys merge (V5.20 cited: cases added, none changed; V5.29, the owner's shared visual system stream):
        # the stream's id, and its near-misses
        ("v524-sys", True),
        ("v529-sys", True),
        # the v524-brand merge (V5.20 cited: cases added, none changed; V5.29, the owner's layout & brand refinement): the
        # stream's id, and its near-misses
        ("v524-brand", True),
        ("v529-brand", True),
        # the V5.30 streams (V5.20 cited: cases added, none changed; V5.30, the owner's final art direction + platform
        # pass): public art direction, AGAMI, the one integration round, the landing on design-v5, and their near-misses
        ("v530-art", True),
        ("v530-agami", True),
        ("v530-integ", True),
        ("v530-land", True),
        ("v530-artx", False),
        ("v530-agam", False),
        ("ops", False),
        ("w3f2", False),
        ("devops-2", False),
        ("sec-f", False),
        ("sec-5", False),
        ("sec-f5a", False),
        ("intfix-2", False),
        ("intfix3", False),
        ("rc-fix-2", False),
        ("rcfix", False),
        ("v512-e", False),
        ("v512-a-w1", False),
        ("v512a", False),
        ("v514-q", False),
        ("v514-pp", False),
        ("v516-p1", False),
        ("v516-p22", False),
        ("v516-q2", False),
        ("v519-j", False),
        ("v519-kk", False),
        ("v518g-a", False),
        ("v518g-nn", False),
        ("v518g", False),
        ("v518gg-n", False),
        ("v518-n", False),
        ("v520-w", False),
        ("v520-waa", False),
        ("v520-cs", False),
        ("v520-fix", False),
        ("v520-fixvv", False),
        ("v520-audit", False),
        ("v520-merge", False),
        ("v520wa", False),
        ("v520g-wa", False),
        ("v522-mm", False),
        ("v522-m1", False),
        ("v522-sh", False),
        ("v522m", False),
        ("v522g-m", False),
        ("v522-merge", False),
        ("v522-director", False),
        ("v522-audit", False),
        ("v521-p1", False),
        ("v522-p0", False),
        ("v522-p11", False),
        ("v522-p1a", False),
        ("v522p1", False),
        ("v522-pp1", False),
        ("v522g-p1", False),
        ("v522-p1-merge", False),
        ("v521-s2", False),
        ("v522-s0", False),
        ("v522-s1", False),
        ("v522-s22", False),
        ("v522-s2a", False),
        ("v522s2", False),
        ("v522-ss2", False),
        ("v522g-s2", False),
        ("v522-s2-merge", False),
        ("v523-px", False),
        ("v522-closing", False),
        ("v524-pub", False),
        ("v524-pub3", False),
        ("v524-pub12", False),
        ("v524-x", False),
        ("v524-home2", False),
        ("v524-t1", False),
        ("v524px", False),
        ("v524g-px", False),
        ("v524-px-merge", False),
        ("v524-closing-2", False),
        ("v524-mfix2", False),
        ("v524-director", False),
        ("v524-matrix", False),
        ("v524-gate", False),
        ("v523-cifix", False),
        ("v524-cifix2", False),
        ("v524cifix", False),
        ("v524-ci", False),
        ("v524g-cifix", False),
        ("v523-sys", False),
        ("v524-sys2", False),
        ("v524-system", False),
        ("v524-sy", False),
        ("v524sys", False),
        ("v523-brand", False),
        ("v524-brand2", False),
        ("v524-branding", False),
        ("v524-bran", False),
        ("v524brand", False),
    ],
)
def test_a_family_id_is_the_steward_a_wave_s_workflow_or_a_family_outside_the_waves(fid, valid):
    """
    Every form the checker's docstring names, and its near-misses. From V5.24 on the final-delivery lanes of
    FINAL_DELIVERY_V2.md (R11: v5<nn>-t, -px, -lib, -home, -pub1, -pub2, -plat, -ar, -closing, and -mfix for the one
    fix round of V5.27 §7) are admitted — the cases were added at the v524-px merge under V5.20's strict rule: no
    existing case changed, the new ids asserted admitted and their near-misses (a lower directive number, a third
    page lane, a suffix, a label) refused.
    """
    assert bool(co.FAMILY_ID.fullmatch(fid)) is valid


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
