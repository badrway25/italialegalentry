"""
requirements/base.txt pins the nine packages the project names; the ten others its dependencies pull in (asgiref,
cryptography, cffi, fido2, …) were resolved against lower bounds on the day of the install, so a server could get
versions no test ever ran, and a rollback's `pip install -r` did not restore the previous set (DevOps verification,
finding 13). requirements/constraints.txt pins the whole closure for the server — Linux, CPython 3.12 — and the
runbook and the rollback install with it. These tests keep it complete and in step with base.txt.
"""

from __future__ import annotations

import re
from importlib import metadata
from pathlib import Path

from packaging.markers import default_environment
from packaging.requirements import Requirement
from packaging.utils import canonicalize_name

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "requirements" / "base.txt"
CONSTRAINTS = ROOT / "requirements" / "constraints.txt"

#: The production server's interpreter and platform (runbook, step 0): markers are evaluated for it, not for the
#: machine running the tests (typing-extensions, for one, is needed by psycopg below Python 3.13 only).
SERVER = {
    **default_environment(),
    "python_version": "3.12",
    "python_full_version": "3.12.3",
    "sys_platform": "linux",
    "platform_system": "Linux",
    "os_name": "posix",
    "platform_machine": "x86_64",
    "implementation_name": "cpython",
    "platform_python_implementation": "CPython",
}


def _requirements(path: Path) -> list[Requirement]:
    lines = (line.split("#", 1)[0].strip() for line in path.read_text(encoding="utf-8").splitlines())
    return [Requirement(line) for line in lines if line]


def _pins(path: Path) -> dict[str, str]:
    pins = {}
    for requirement in _requirements(path):
        (specifier,) = requirement.specifier  # one exact pin per line
        assert specifier.operator == "==", f"{path.name}: {requirement} is not an exact pin"
        pins[canonicalize_name(requirement.name)] = specifier.version
    return pins


def _applies(requirement: Requirement, extras: set[str]) -> bool:
    if requirement.marker is None:
        return True
    return any(requirement.marker.evaluate({**SERVER, "extra": extra}) for extra in extras | {""})


def _closure() -> set[str]:
    """Every distribution base.txt brings onto the server, walked through the installed metadata. A dependency the
    test machine does not have installed is counted by name (its own dependencies cannot be read from here)."""
    names: set[str] = set()
    walked: set[tuple[str, frozenset[str]]] = set()
    todo = [(requirement, set(requirement.extras)) for requirement in _requirements(BASE)]
    while todo:
        requirement, extras = todo.pop()
        name = canonicalize_name(requirement.name)
        if (name, frozenset(extras)) in walked:
            continue
        walked.add((name, frozenset(extras)))
        names.add(name)
        try:
            requires = metadata.distribution(requirement.name).requires or []
        except metadata.PackageNotFoundError:
            continue
        for spec in requires:
            dependency = Requirement(spec)
            if _applies(dependency, extras):
                todo.append((dependency, set(dependency.extras)))
    return names


def test_the_constraints_repeat_every_direct_pin_of_base_txt():
    constraints = _pins(CONSTRAINTS)
    for name, version in _pins(BASE).items():
        assert constraints.get(name) == version, (
            f"constraints.txt pins {name}=={constraints.get(name)}, base.txt {version}"
        )


def test_the_constraints_cover_the_dependency_closure_and_nothing_else():
    constraints, closure = set(_pins(CONSTRAINTS)), _closure()
    assert not closure - constraints, f"not pinned in constraints.txt: {sorted(closure - constraints)}"
    assert not constraints - closure, f"pinned but no longer needed: {sorted(constraints - closure)}"


def test_the_pinned_set_satisfies_its_own_requirements():
    """What `pip check` will say on the server: every requirement of a pinned distribution (under the server's markers)
    accepts the pinned version of its dependency. Read from the installed metadata wherever the installed version is
    the pinned one."""
    constraints = _pins(CONSTRAINTS)
    checked = 0
    for name, version in constraints.items():
        try:
            distribution = metadata.distribution(name)
        except metadata.PackageNotFoundError:
            continue
        if distribution.version != version:
            continue
        checked += 1
        for spec in distribution.requires or []:
            dependency = Requirement(spec)
            pinned = constraints.get(canonicalize_name(dependency.name))
            if pinned and _applies(dependency, set()):
                assert dependency.specifier.contains(pinned, prereleases=True), f"{name} {version} needs {dependency}"
    assert checked, "no pinned distribution is installed at its pinned version here"


def test_the_server_installs_with_the_constraints():
    deployment = ROOT / "docs" / "deployment"
    installs = [
        (path.name, line)
        for path in (deployment / "PRODUCTION_DEPLOYMENT_RUNBOOK.md", deployment / "ROLLBACK.md")
        for line in path.read_text(encoding="utf-8").splitlines()
        if re.search(r"pip install .*-r ", line)
    ]
    assert len(installs) >= 3, installs  # runbook steps 4 and 15, rollback section 1
    for name, line in installs:
        assert "-c /srv/italylegalentry/app/requirements/constraints.txt" in line, f"{name}: {line.strip()}"
