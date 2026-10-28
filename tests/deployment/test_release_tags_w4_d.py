"""
The release, as the deployment documents describe it, held to the repository (W4-D, 16 October 2026).

The owner's directive V5.10 (16 October 2026) fixed what the release is: GitHub's `main` at a3ac318 is preserved by the
tag `pre-v5-main-2026-10`, `main` is fast-forwarded to the validated `design-v5` release snapshot, and one annotated tag
names the release — the platform's own version, «v2.0.0 — Fase 1». The runbook, the checklist and ROLLBACK.md must
say the same thing, the tag must stay the label the footer shows, the rollback's statement about the migrations must
stay true, and CI must keep running the server's major versions (Python 3.12 and PostgreSQL 16, what the runbook
installs on Ubuntu 24.04) beside the development stack.
"""

from __future__ import annotations

import hashlib
import re
import subprocess
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
DEPLOYMENT = ROOT / "docs" / "deployment"
RUNBOOK = (DEPLOYMENT / "PRODUCTION_DEPLOYMENT_RUNBOOK.md").read_text(encoding="utf-8")
CHECKLIST = (DEPLOYMENT / "PRODUCTION_CHECKLIST.md").read_text(encoding="utf-8")
ROLLBACK = (DEPLOYMENT / "ROLLBACK.md").read_text(encoding="utf-8")
DOCUMENTS = {"runbook": RUNBOOK, "checklist": CHECKLIST, "rollback": ROLLBACK}

RELEASE_TAG = "v2.0.0"
REFERENCE_TAG = "pre-v5-main-2026-10"
#: GitHub's `main` before the promotion (V5.10: «preserve the current main commit a3ac318»).
REFERENCE_SHA = "a3ac318304beb4504134762bfa6e9c4e4ce600f1"
#: The one bar of PRODUCTION_READY, in the runbook's *States* and the checklist's §A alike.
PRODUCTION_READY_BAR = (
    "A-1 … A-22 ticked with evidence on that commit, and each of A-23 … A-28 closed or accepted in writing by the owner"
    " as open until go-live"
)
#: The numbered migration files and their git blob ids when ROLLBACK.md §7 was written: `design-v5` at 0a8351b — the
#: same 39 files, byte for byte, as the reference tag's a3ac318 (`git ls-tree -r <commit> -- apps`, the two lists
#: identical). A count would miss an edited migration, or one added and one removed (the W4-D review's m3).
MIGRATIONS_WHEN_WRITTEN = {
    "apps/academy/migrations/0001_initial.py": "09ba7b20b05b25bf9fe91587eeb5c162fddb50de",
    "apps/accounts/migrations/0001_initial.py": "12b52b9771fc608bba2c5e881f2ae558d3e297a4",
    "apps/accounts/migrations/0002_initial.py": "b39281fa9c16e19e564afc2e0f2b14063dec55b5",
    "apps/accounts/migrations/0003_accountverification.py": "f17a96137bb029d0b5c4170cc3925593d3869902",
    "apps/accounts/migrations/0004_personprofile_completed_at_and_more.py": "fb9eb496d620130a5e29d75fb72e5dea3cb4c905",
    "apps/audit/migrations/0001_initial.py": "1890995b9ee158bcd5ff4805d452d861b924c09c",
    "apps/cases/migrations/0001_initial.py": "31d8fe9d63f78f5cf9a06382992c5e90ccbdeb30",
    "apps/cms/migrations/0001_initial.py": "4a7e67adabb2909d0968e7e895a4b23d6767d1c7",
    "apps/cms/migrations/0002_mediaasset_caption_ar_mediaasset_caption_date_and_more.py": "3f6193a4f0dc6385bc925a7dac4ca23ccdd91d75",
    "apps/community/migrations/0001_initial.py": "a39bcf50ea581ae9b3a615f6fb72d96f2443a7fd",
    "apps/companies/migrations/0001_initial.py": "8dd3a1e23b2484266ba623d2ac3b2d29208a64f2",
    "apps/companies/migrations/0002_companyneed_motivation.py": "b4f411c465bac52d06448d915f425f1807068898",
    "apps/consents/migrations/0001_initial.py": "fc4c10c4c00a5fab053673f2709f3fe6b96e04fb",
    "apps/core/migrations/0001_initial.py": "70a50aee1b998fb9b4d92daec052d37da8e7fda0",
    "apps/documents/migrations/0001_initial.py": "b483d2f74e9b082c2550599457f08296ad19be95",
    "apps/documents/migrations/0002_alter_privatedocument_scan_status_and_more.py": "9c600ce01737c22ad99281386c583463e6d71c35",
    "apps/ecosystem/migrations/0001_initial.py": "a9e3c66a7cdfc94c0379ff09a7ce719e00de229a",
    "apps/enquiries/migrations/0001_initial.py": "3e3dfdd3363a67e8a6429cac6239881470d86c93",
    "apps/faq/migrations/0001_initial.py": "daf294d65746d738e2bd15175cf325317af7ac10",
    "apps/forum/migrations/0001_initial.py": "224efe00e866f2cb9c58d24e00c6b2d5ba172933",
    "apps/forum/migrations/0002_forumedition_commission_forumprofile_and_more.py": "3d5e68a76fe0ec7d2ad6c39c5a6b918e15068384",
    "apps/glossary/migrations/0001_initial.py": "5372af16bec1e6f3feb40cc6e78ea13cc96c3246",
    "apps/helpdesk/migrations/0001_initial.py": "f6543e83bea0c80c06295de2f77a096b40d089d6",
    "apps/integrations/migrations/0001_initial.py": "db966404d658e054834daa1298ff2943269b950c",
    "apps/legal/migrations/0001_initial.py": "5a53eb1e2cd69d9dd2c34191496f471ed252677b",
    "apps/living/migrations/0001_initial.py": "e1812ef9027ce5a24c144894f19765aa3a75581b",
    "apps/news/migrations/0001_initial.py": "93c7bf65916906779060a2f3f5250ff299f4d1ff",
    "apps/notifications/migrations/0001_initial.py": "95de4a256e3dbdb817059c4081eb018d1e86ea55",
    "apps/notifications/migrations/0002_notificationpreference_notification.py": "b9e514d6e499e1eae475e3f22af5d677ada6690c",
    "apps/orientation/migrations/0001_initial.py": "b5925a1de4199cb41ebac760e46c5a25b45f5c06",
    "apps/pages/migrations/0001_initial.py": "c42fff45b8a73ea7dfae8b1a21592e6adb809616",
    "apps/partners/migrations/0001_initial.py": "af8a5656b060809bd54e0c0c7937175f70ea1adc",
    "apps/pathways/migrations/0001_initial.py": "824cfa946c7110f947f0e3eedf50751a800eadec",
    "apps/portal/migrations/0001_initial.py": "0e8f9498e58b58f9d3dd0301779d6c41829f3cd7",
    "apps/rules/migrations/0001_initial.py": "b8ae3247e3ac01b4877f5117a208a822320a340a",
    "apps/rules/migrations/0002_legalrule_approved_by_label_legalrule_provenance_and_more.py": "5ae0455f909c5fc58b45b7d9a3bb22f0f5d5b6ac",
    "apps/selection/migrations/0001_initial.py": "c97e2dd84d873699efbaa28735bdbf0627182d67",
    "apps/selection/migrations/0002_alter_identityaccess_fields_read_and_more.py": "11b4155f9b2a32d881d00b6ced95e51cd8853442",
    "apps/selection/migrations/0003_alter_selectionprocess_outcome.py": "e860b75adb97ca48f56bca2c834e90c83b4e36fd",
}


def _section(text: str, heading: str) -> str:
    """From ``heading`` to the next heading of level 1 or 2, outside code blocks."""
    lines = text[text.index(heading) :].splitlines(keepends=True)
    kept, fenced = [lines[0]], False
    for line in lines[1:]:
        if line.startswith("```"):
            fenced = not fenced
        elif not fenced and re.match(r"#{1,2} ", line):
            break
        kept.append(line)
    return "".join(kept)


def _flat(text: str) -> str:
    """Prose reflows: compare words, not line breaks."""
    return re.sub(r"\s+", " ", text)


def _blob_id(data: bytes) -> str:
    """git's object id of a file's bytes (`git hash-object`): the checkout is LF (.gitattributes), as git stores it."""
    return hashlib.sha1(b"blob %d\0" % len(data) + data, usedforsecurity=False).hexdigest()


def test_the_release_tag_is_the_version_the_platform_declares():
    """The footer's label and the tag say the same thing: change one, and this test asks for the other."""
    from core.models import SiteSettings

    base = (ROOT / "config" / "settings" / "base.py").read_text(encoding="utf-8")
    setting = re.search(r'"VERSION_LABEL": env\("ILE_VERSION_LABEL", default="([^"]+)"\)', base).group(1)
    model = SiteSettings._meta.get_field("version_label").default
    assert setting == model, (setting, model)
    assert setting.split()[0] == RELEASE_TAG, setting
    assert f"export ILE_TAG={RELEASE_TAG} " in RUNBOOK
    release_tags = _section(RUNBOOK, "## RELEASE TAGS")
    assert f"The release is **`{RELEASE_TAG}`**, an **annotated** tag" in release_tags


def test_the_three_documents_name_the_same_release_and_reference():
    for name, text in DOCUMENTS.items():
        assert REFERENCE_TAG in text, f"{name} does not name the pre-V5 reference tag"
        assert REFERENCE_SHA in text, f"{name} does not give the reference tag's commit"
        assert RELEASE_TAG in text, f"{name} does not name the release tag"
        # No other 40-hex commit is offered as a reference point of the release.
        assert set(re.findall(r"\b[0-9a-f]{40}\b", text)) <= {REFERENCE_SHA, "0" * 40}, name
    assert REFERENCE_SHA in _section(RUNBOOK, "## RELEASE TAGS")
    assert REFERENCE_SHA in _section(ROLLBACK, "## 7. The pre-V5 platform")
    assert '"refs/tags/v2.0.0^{}"' in CHECKLIST and '"refs/tags/pre-v5-main-2026-10^{}"' in CHECKLIST


def test_no_candidate_tag_is_deployed_or_rolled_back_to():
    """V5.10: «one meaningful final release tag» — the candidate is named by its SHA, never by a tag."""
    for name, text in DOCUMENTS.items():
        assert not re.search(r"(?:ILE_TAG|PREVIOUS_TAG)=v5-release-candidate", text), name
        mentions = re.findall(r"[^\n]*v5-release-candidate[^\n]*", text)
        assert all("there is no `v5-release-candidate` tag" in line for line in mentions), (name, mentions)
    assert "PREVIOUS_TAG=v2.0.0 " in ROLLBACK


def test_the_states_are_the_owners_three():
    states = _section(RUNBOOK, "## States")
    rows = {
        state: re.search(rf"^\| \*\*{state}\*\* \|(.*)$", states, re.MULTILINE)
        for state in (
            "DEVELOPMENT_COMPLETE",
            "RELEASE_CANDIDATE",
            "PRODUCTION_READY",
        )
    }
    assert all(rows.values()), rows
    assert "named by its SHA" in rows["RELEASE_CANDIDATE"].group(1)
    ready = rows["PRODUCTION_READY"].group(1)
    for fact in ("fast-forward", REFERENCE_TAG, f"`{RELEASE_TAG}`", PRODUCTION_READY_BAR, "V5.9 §17"):
        assert fact in ready, fact
    assert "«GitHub pushed» is none of these." in states


def test_the_runbook_and_the_checklist_set_one_bar_for_production_ready():
    """PRODUCTION_READY is what the owner is told (V5.9 §16: «do not declare ready too early»): the runbook's *States*
    and the checklist's release gate state the same bar, in the same words (the W4-D review's M2). The owner's items
    A-23 … A-28 cannot all close before the deployment — SMTP from the droplet, the backups running — so each one is
    closed or accepted by him in writing, as the go-live blockers were before."""
    gate = _section(CHECKLIST, "## A. Release gate")
    gate_intro = _flat(gate[: gate.index("| # |")])
    assert PRODUCTION_READY_BAR in gate_intro, gate_intro
    assert "every line is ticked" not in _flat(CHECKLIST)
    before = _flat(_section(CHECKLIST, "## B. Before the deployment"))
    assert "The release gate's bar (§A) holds on that SHA" in before
    assert "every open line is accepted" not in before


def test_a_downgrade_is_a_restore_never_a_migrate_backwards():
    section_7 = _flat(_section(ROLLBACK, "## 7. The pre-V5 platform"))
    assert "never a rollback target of this server" in section_7
    assert "**a downgrade is never a `migrate` backwards on live data.**" in section_7
    assert "git diff --name-status pre-v5-main-2026-10 v2.0.0 -- 'apps/*/migrations/*.py'" in section_7
    assert "ROLLBACK.md`](ROLLBACK.md) §7" in _flat(_section(RUNBOOK, "## RELEASE TAGS"))


def test_every_migration_pattern_the_documents_give_lists_the_migrations():
    """git matches a pattern that holds a wildcard against the whole path, so `'apps/*/migrations/'` names no file — a
    path never ends in a slash — and a check written with it prints nothing whatever the release changed (the W4-D
    review's M1: ROLLBACK.md §7's re-check, the runbook's step 15). Each pattern the three documents give for the
    migrations must list every migration file of the tree, as `git ls-files` reads it."""

    def ls_files(pathspec: str) -> set[str]:
        out = subprocess.run(
            ["git", "ls-files", "--", pathspec], cwd=ROOT, capture_output=True, text=True, check=True, encoding="utf-8"
        )
        return {line for line in out.stdout.splitlines() if line}

    migrations = {path for path in ls_files("apps") if re.fullmatch(r"apps/[^/]+/migrations/\d{4}_[^/]+\.py", path)}
    assert len(migrations) >= len(MIGRATIONS_WHEN_WRITTEN), len(migrations)
    patterns = {pattern for text in DOCUMENTS.values() for pattern in re.findall(r"'(apps/\*/migrations/[^']*)'", text)}
    assert patterns, "no migration pattern found in the deployment documents"
    for pattern in sorted(patterns):
        missing = sorted(migrations - ls_files(pattern))
        assert not missing, f"{pattern!r} does not list {len(missing)} migration file(s), e.g. {missing[:2]}"


def _migrations_in_the_checkout() -> dict[str, str]:
    return {
        path.relative_to(ROOT).as_posix(): _blob_id(path.read_bytes())
        for path in (ROOT / "apps").glob("*/migrations/[0-9][0-9][0-9][0-9]_*.py")
    }


def _released_migration_changes(current: dict[str, str]) -> dict[str, list[str]]:
    """What ``current`` changed in the released migrations — the files ROLLBACK.md §7 speaks for."""
    written = MIGRATIONS_WHEN_WRITTEN
    return {
        "added": sorted(current.keys() - written.keys()),
        "removed": sorted(written.keys() - current.keys()),
        "edited": sorted(path for path in current.keys() & written.keys() if current[path] != written[path]),
    }


def test_the_rollback_statement_about_the_migrations_is_still_true():
    """ROLLBACK.md §7 says no migration differs between the reference tag and the release, `v2.0.0`: the same files,
    byte for byte. A released migration edited or removed since makes that false: say in §7 what it changes for a
    return to `pre-v5-main-2026-10` (section 1's list decides whether it is code-rollback-safe), then update the table
    above and the count in the section."""
    changes = _released_migration_changes(_migrations_in_the_checkout())
    broken = {kind: paths for kind, paths in changes.items() if kind != "added" and paths}
    assert not broken, f"ROLLBACK.md §7 was written for other migration files: {broken}"
    assert f"the {len(MIGRATIONS_WHEN_WRITTEN)} migration files of `pre-v5-main-2026-10`" in _flat(ROLLBACK)


def test_a_new_migration_does_not_trip_the_rollback_statement_an_edited_or_removed_one_does():
    """§7 speaks for the 39 released files (W4-D part 2, A6): a later migration is the next release's business
    (section 1), so it must not fail the tripwire; an edited or a removed released file must, each by its name."""
    released = dict(MIGRATIONS_WHEN_WRITTEN)
    added = {**released, "apps/cases/migrations/0002_a_later_release.py": "0" * 40}
    later = _released_migration_changes(added)
    assert later["added"] == ["apps/cases/migrations/0002_a_later_release.py"]
    assert not later["edited"] and not later["removed"], later
    name = "apps/rules/migrations/0002_legalrule_approved_by_label_legalrule_provenance_and_more.py"
    edited = {**released, name: _blob_id(b"# edited\n")}
    assert _released_migration_changes(edited)["edited"] == [name]
    removed = {path: blob for path, blob in released.items() if path != name}
    assert _released_migration_changes(removed)["removed"] == [name]
    renamed = {**removed, name.replace("0002_", "0002_renamed_"): released[name]}
    assert _released_migration_changes(renamed)["removed"] == [name]
    assert len(MIGRATIONS_WHEN_WRITTEN) == 39


def test_the_rollback_statement_speaks_at_the_release():
    """§7 states the migrations' identity at the release this candidate becomes — «at `v2.0.0`» —, not «today»."""
    section_7 = _flat(_section(ROLLBACK, "## 7. The pre-V5 platform"))
    assert "No migration differs between the two at `v2.0.0`" in section_7, section_7
    assert "No migration differs between the two today" not in section_7


def test_ci_runs_the_production_target_beside_the_development_stack():
    """The runbook installs Ubuntu 24.04's Python 3.12 and PostgreSQL 16 with the pinned closure; CI runs the same
    major versions with the same closure — setup-python's CPython 3.12.x and the Alpine image of PostgreSQL 16, not
    Ubuntu's own builds (the W4-D review's m2) —, on that release of Ubuntu, beside the development stack (Python 3.13,
    PostgreSQL 17). One step makes the job's name true: it asserts the interpreter's and the database's versions."""
    workflow = yaml.safe_load((ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8"))
    job = workflow["jobs"]["test"]
    assert job["runs-on"] == "ubuntu-24.04", job["runs-on"]
    assert job["strategy"]["fail-fast"] is False
    runs = {(entry["python"], entry["postgres"]) for entry in job["strategy"]["matrix"]["include"]}
    assert runs == {("3.12", "16"), ("3.13", "17")}, runs
    assert job["services"]["postgres"]["image"] == "postgres:${{ matrix.postgres }}-alpine"
    install = next(step["run"] for step in job["steps"] if step.get("name") == "Install dependencies")
    assert install == "python -m pip install -r requirements/dev.txt -c requirements/constraints.txt", install
    versions = next(
        step for step in job["steps"] if step.get("name") == "The interpreter and the database are the matrix's"
    )
    assert versions["env"] == {"PY_VERSION": "${{ matrix.python }}", "PG_MAJOR": "${{ matrix.postgres }}"}
    # Written as patterns: tests/test_env_example_is_complete.py counts every literal environment read of a .py file
    # as a variable the application reads, and these two are the workflow's, not the application's.
    assert re.search(r"assert v == os\.environ\['PY_VERSION'\]", versions["run"]), versions["run"]
    assert re.search(r"assert str\(v\) == os\.environ\['PG_MAJOR'\]", versions["run"]), versions["run"]
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    floor = re.search(r'requires-python = ">=(\d+\.\d+)"', pyproject).group(1)
    assert floor == min(python for python, _ in runs), "CI must run the oldest Python the project declares"
    assert "Python 3.12 with PostgreSQL 16" in _flat(RUNBOOK)
    assert "Python 3.12 with PostgreSQL 16" in _flat(CHECKLIST)
