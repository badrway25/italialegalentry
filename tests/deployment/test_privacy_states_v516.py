"""
V5.16 §14, as corrected by V5.17 §2 — the status model, written where the owner reads it (the runbook's *States*, the
checklist's §A) and kept apart: PRODUCT_COMPLETE / COMPLIANCE_REVIEW_COMPLETE / PRODUCTION_CONFIG_COMPLETE /
PRODUCTION_READY (V5.17 replaced V5.16's PRIVACY_CONTENT_COMPLETE; no file may keep it as a state).

* the runbook's *States* has one row per state, PRODUCTION_READY needing the three others and the privacy gate;
* the checklist's release gate carries A-29 … A-33, closed and never accepted as open, with the gate «PRIVACY NOTICE =
  VERIFIED AND PUBLIC» and the nginx/Gunicorn/application logging verification of §12 as production configuration;
* the open-field classes the checklist names are the ones the code refuses (``legal.models.OPEN_FIELD_CLASSES``);
* the release notes say what «production-ready» now means.
"""

from __future__ import annotations

import re
from pathlib import Path

from legal.models import OPEN_FIELD_CLASSES

ROOT = Path(__file__).resolve().parents[2]
RUNBOOK = (ROOT / "docs/deployment/PRODUCTION_DEPLOYMENT_RUNBOOK.md").read_bytes().decode("utf-8")
CHECKLIST = (ROOT / "docs/deployment/PRODUCTION_CHECKLIST.md").read_bytes().decode("utf-8")
NOTES = (ROOT / "docs/RELEASE_NOTES_v2.0.0.md").read_bytes().decode("utf-8")
STATES = ("PRODUCT_COMPLETE", "COMPLIANCE_REVIEW_COMPLETE", "PRODUCTION_CONFIG_COMPLETE", "PRODUCTION_READY")


def _flat(text: str) -> str:
    return re.sub(r"\s+", " ", text)


def _section(text: str, heading: str) -> str:
    start = text.index(f"\n{heading}\n")
    end = text.find("\n## ", start + len(heading) + 2)
    return text[start : end if end != -1 else None]


def _row(text: str, key: str) -> str:
    match = re.search(rf"^\| {re.escape(key)} \|(.*)$", text, re.MULTILINE)
    assert match, key
    return match.group(1)


def test_the_runbook_states_carry_the_v517_model_and_keep_them_apart():
    states = _section(RUNBOOK, "## States")
    assert "Do not conflate them." in _flat(states)
    rows = {state: _row(states, f"**{state}**") for state in STATES}
    assert "visually and functionally complete and accepted" in rows["PRODUCT_COMPLETE"]
    assert "**Not blocked by** checklist A-29 … A-33" in rows["PRODUCT_COMPLETE"]
    compliance = rows["COMPLIANCE_REVIEW_COMPLETE"]
    assert "OWNER CONFIRMATION REQUIRED or LEGAL REVIEW REQUIRED" in compliance
    assert "docs/compliance/DPIA.md" in compliance and "OF11_ANNEXE_DEVIATIONS.md" in compliance
    for fact in ("DigitalOcean", "DPA", "SMTP", "backups", "logging", "PRODUCTION CONFIGURATION REQUIRED"):
        assert fact in rows["PRODUCTION_CONFIG_COMPLETE"], fact
    ready = rows["PRODUCTION_READY"]
    assert "PRODUCT_COMPLETE, COMPLIANCE_REVIEW_COMPLETE and PRODUCTION_CONFIG_COMPLETE all hold" in ready
    assert "«PRIVACY NOTICE = VERIFIED AND PUBLIC» (checklist A-29)" in ready
    assert "**A-29 … A-33 closed**" in ready
    # V5.17 §2, §10: compliance and infrastructure block PRODUCTION_READY, not PRODUCT_COMPLETE; the infrastructure
    # values are verified when the server is prepared, never asked of the owner now
    flat = _flat(states)
    assert "do **not** block PRODUCT_COMPLETE; they block PRODUCTION_READY" in flat
    assert "are not questions for the owner now (V5.17 §10)" in flat


def test_the_checklist_gate_carries_a29_to_a33_closed_never_accepted_as_open():
    gate = _section(CHECKLIST, "## A. Release gate")
    intro = _flat(gate[: gate.index("| # |")])
    assert "the bar also needs **A-29 … A-33 closed** — they cannot be accepted as open" in intro
    assert "**None of A-29 … A-33 blocks PRODUCT_COMPLETE**" in intro
    rows = {f"A-{n}": _row(gate, f"A-{n}") for n in range(29, 34)}
    assert "**PRIVACY NOTICE = VERIFIED AND PUBLIC**" in rows["A-29"] and "[DA COMPLETARE" in rows["A-29"]
    config = rows["A-30"]
    for fact in (
        "DigitalOcean region of the droplet",
        "database and storage region",
        "DPA accepted",
        "SMTP provider actually used",
        "contact@agamieuromed.org mailbox",
        "off-server backup provider, location and retention",
        "nginx's log rotation",
        "journald's retention",
        "Gunicorn",
        "Security logging is not weakened blindly",
    ):
        assert fact in config, fact
    assert "PRODUCTION_CONFIG_COMPLETE" in config and "verified when the production server is prepared" in config
    assert "SPECIAL CATEGORY LEGAL BASIS" in rows["A-31"] and "COMPLIANCE_REVIEW_COMPLETE" in rows["A-31"]
    assert "R-SC-1" in rows["A-31"] and "ILE_SPECIAL_CATEGORY_FLOWS_ENABLED" in rows["A-31"]
    assert "DPIA = PRODUCTION GATE" in rows["A-32"] and "docs/compliance/DPIA.md" in rows["A-32"]
    assert (
        "not substituted as controller unless the owner confirms it is a separate legal entity" in rows["A-33"]
        and "DPO STATUS" in rows["A-33"]
    )


def test_the_classes_the_documents_name_are_the_ones_the_code_refuses():
    gate = _flat(_section(CHECKLIST, "## A. Release gate"))
    states = _flat(_section(RUNBOOK, "## States"))
    for label in OPEN_FIELD_CLASSES:
        assert label in gate + states, label


def test_the_release_notes_say_what_production_ready_now_means():
    flat = _flat(NOTES)
    assert "PRODUCT_COMPLETE, COMPLIANCE_REVIEW_COMPLETE, PRODUCTION_CONFIG_COMPLETE and PRODUCTION_READY" in flat
    assert "production refuses to publish the notice while one remains" in flat


def test_the_v516_state_name_is_gone_from_every_living_document():
    """V5.17 §2 replaced PRIVACY_CONTENT_COMPLETE: it may be named only as the name it replaced, never as a state."""
    living = [
        "docs/deployment/PRODUCTION_DEPLOYMENT_RUNBOOK.md",
        "docs/deployment/PRODUCTION_CHECKLIST.md",
        "docs/RELEASE_NOTES_v2.0.0.md",
        *(str(path.relative_to(ROOT)) for path in sorted((ROOT / "docs/compliance").glob("*.md"))),
        "apps/legal/models.py",
    ]
    for name in living:
        text = (ROOT / name).read_bytes().decode("utf-8")
        for line in text.splitlines():
            if "PRIVACY_CONTENT_COMPLETE" in line:
                assert "replac" in line, f"{name}: {line.strip()}"
