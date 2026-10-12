"""
scripts/regen_design_inventory.py — the steward's regeneration of the DS 2026 inventory tables and the A11Y
counts after every V5.4 merge (plan §2.2, merge step 3).

A synthetic tree carries every kind of staleness the script rewrites (a weight, a row order, a row for a file
that is gone, a count, a total, a summary, a gap range) and every kind of gap it must NOT fill (a sheet, a font,
a component, an icon, a keyframe, a script and an init function nobody has described): the first are
rewritten, the second are reported as «needs a writer» — the script never invents prose. Then the real
documents: every anchor the script reads is there.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "regen_design_inventory.py"


def _load_script():
    spec = importlib.util.spec_from_file_location("ile_regen_design_inventory", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module  # dataclasses look their module up by name
    spec.loader.exec_module(module)
    return module


regen = _load_script()

DESIGN = """# DS

| Documento gemello | `docs/ACCESSIBILITY.md` (lacune **G-01 … G-01**) |

## 2. Architettura CSS

| Ordine | File | Peso | Contenuto |
|---|---|---|---|
| 1 | `components.css` | 9.9 KB | 7 sezioni numerate: the components, described
over two lines |
| 2 | `gone.css` | 1.0 KB | a sheet main.css no longer imports |
| 3 | `fonts.css` | ≈ 1.5 KB | the faces |

Convenzioni.

### 2.1 Fogli delle app

### 6.2 File self-hosted (`static/fonts/`, 9 file woff2, ≈ 99 KB in totale)

| File | Famiglia | Peso · stile | Sottoinsieme | KB |
|---|---|---|---|---|
| `a.woff2` | A | 400 · tondo | latin | 0.5 |
| `gone.woff2` | G | 400 · tondo | latin | 3.0 |

### 6.3 Licenza

## 10. Catalogo componenti (`templates/components/`)

3 file. Each component is an include.

#### `x.html`

- **Scopo**: x.

### 10.1 Pattern

## 12. Motion

The keyframe `other` lives elsewhere.

## 13. Iconografia

<!-- icon-list:start -->
9 icone.

| Gruppo | Icone |
|---|---|
| Tutte | `a`, `c` |
<!-- icon-list:end -->

> verified: **1 icone disposte**
> sulle 1 catture, 0 vuote.

## 14. Illustrazioni

## 16. Moduli JS

Tre file, ≈ 0.1 KB non compressi in totale.

| File | Caricamento | Ruolo |
|---|---|---|
| `static/js/main.js` | module | init |

| Funzione | Hook |
|---|---|
| `initA` | data-a |
| `initC` | data-c |

## 17. Lo shim

## 19. Screenshot QA (`docs/qa/design/`)

The report: **5 catture**, all fine.

## 20. Controlli automatici

L'elenco è in `docs/ACCESSIBILITY.md` §13 (**G-01 … G-01**).
"""

A11Y = """# A11Y

Lacune (**G-01 … G-01**).

<!-- wcag-checklist:start -->
| N | Criterio | Livello | Stato | Implementazione |
|---|---|---|---|---|
| 1.1.1 | Contenuti non testuali | A | Conforme | alt text everywhere, checked |
| 1.3.1 | Informazioni e relazioni | A | Conforme | headings and landmarks everywhere |
| 2.4.7 | Focus visibile | AA | Parziale (G-02) | the ring is missing in one place |
<!-- wcag-checklist:end -->

Riepilogo: 9 criteri — 9 conformi, 0 parziali, 0 da confermare in QA, 0 non applicabili.

## 13. Lacune note

| G-01 | chiusa | the first |
| G-02 | aperta | the second |
"""


def _write(path: Path, data: str | bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data if isinstance(data, bytes) else data.encode("utf-8"))


@pytest.fixture
def tree(tmp_path, monkeypatch):
    static = tmp_path / "static"
    _write(
        static / "css" / "main.css",
        '@import url("fonts.css");\n@import url("components.css");\n@import url("v2/new.css");\n',
    )
    _write(static / "css" / "fonts.css", "/* faces */\n" + "x" * (2048 - 12))
    _write(
        static / "css" / "components.css",
        "/*\n   1. Controls\n   2. Feedback\n*/\n@keyframes spin { to { opacity: 1; } }\n",
    )
    _write(static / "css" / "v2" / "new.css", ".new {}\n")
    _write(static / "fonts" / "a.woff2", b"\0" * 1024)
    _write(static / "fonts" / "b.woff2", b"\0" * 512)
    _write(static / "img" / "icons.svg", '<svg><symbol id="icon-a"/><symbol id="icon-b"/></svg>\n')
    _write(static / "js" / "main.js", "function initA() {}\nfunction initB() {}\n")
    _write(static / "js" / "head.js", "document.documentElement.className = 'js';\n")
    _write(tmp_path / "templates" / "components" / "x.html", "<p>x</p>\n")
    _write(tmp_path / "templates" / "components" / "y.html", "<p>y</p>\n")
    _write(tmp_path / "capture-report.json", json.dumps({"home-fr-390": {"icons": 3}, "home-ar-390": {"icons": 4}}))
    _write(tmp_path / "DS.md", DESIGN)
    _write(tmp_path / "A11Y.md", A11Y)
    monkeypatch.setattr(regen, "STATIC", static)
    monkeypatch.setattr(regen, "COMPONENTS", tmp_path / "templates" / "components")
    monkeypatch.setattr(regen, "CAPTURE_REPORT", tmp_path / "capture-report.json")
    monkeypatch.setattr(regen, "DESIGN_DOC", tmp_path / "DS.md")
    monkeypatch.setattr(regen, "A11Y_DOC", tmp_path / "A11Y.md")
    return tmp_path


def test_what_can_be_computed_is_rewritten(tree, capsys):
    assert regen.main([]) == 2, "check mode: stale figures AND things that need a writer"
    assert (tree / "DS.md").read_bytes().decode("utf-8") == DESIGN, "check mode changes nothing"
    capsys.readouterr()
    assert regen.main(["--write"]) == 2, "the prose is still missing after the rewrite"
    design = (tree / "DS.md").read_bytes().decode("utf-8")
    a11y = (tree / "A11Y.md").read_bytes().decode("utf-8")
    assert b"\r" not in (tree / "DS.md").read_bytes() and b"\r" not in (tree / "A11Y.md").read_bytes()
    # §2: main.css's order, numbered 1…n, exact weights, the multi-line row whole, the dead row gone
    architecture = design.split("## 2. Architettura CSS", 1)[1].split("### 2.1 ", 1)[0]
    assert "| 1 | `fonts.css` | ≈ 2.0 KB | the faces |" in architecture
    components_kb = regen._kb((tree / "static" / "css" / "components.css").stat().st_size)
    assert (
        f"| 2 | `components.css` | {components_kb} KB | 2 sezioni numerate: the components, described\nover two lines |"
        in architecture
    )
    assert "gone.css" not in architecture
    assert architecture.index("fonts.css") < architecture.index("components.css")
    # §6.2: the heading's count and total, each row's KB, the dead row gone
    assert "### 6.2 File self-hosted (`static/fonts/`, 2 file woff2, ≈ 2 KB in totale)" in design
    assert "| `a.woff2` | A | 400 · tondo | latin | 1.0 |" in design
    assert "gone.woff2" not in design
    # §10, §13, §16, §19 and the gap range
    assert "\n2 file. Each component is an include." in design
    assert "<!-- icon-list:start -->\n2 icone." in design
    assert "**7 icone disposte**\n> sulle 2 catture" in design
    assert "Tre file, ≈ 0.1 KB non compressi in totale." in design
    assert "**2 catture**" in design
    assert design.count("G-01 … G-02") == 2 and "G-01 … G-01" not in design
    # ACCESSIBILITY.md: the summary recounted from the table, the gap range
    assert "Riepilogo: 3 criteri — 2 conformi, 1 parziali, 0 da confermare in QA, 0 non applicabili." in a11y
    assert "G-01 … G-02" in a11y


def test_what_needs_prose_is_reported_never_invented(tree, capsys):
    regen.main(["--write"])
    out = capsys.readouterr().out
    for complaint in (
        "main.css imports `v2/new.css` and the table has no row for it",
        "`static/fonts/b.woff2` has no row",
        "`templates/components/y.html` has no section",
        "the keyframe `spin` is in the cascade and §12 does not name it",
        "the sprite's `icon-b` is not in the grouped list",
        "`c` is listed and is not in the sprite",
        "`static/js/head.js` is not in the table",
        "main.js's `initB` has no row",
        "`initC` is documented and main.js no longer has it",
    ):
        assert "needs a writer: DS 2026 §" in out and complaint in out, complaint
    design = (tree / "DS.md").read_bytes().decode("utf-8")
    assert "v2/new.css" not in design and "b.woff2" not in design and "y.html" not in design


def test_a_second_run_finds_nothing_stale(tree, capsys):
    regen.main(["--write"])
    capsys.readouterr()
    regen.main([])
    out = capsys.readouterr().out
    assert "stale:" not in out and "rewrote:" not in out
    assert "needs a writer:" in out


def test_a_document_that_lost_an_anchor_stops_the_script(tree, capsys):
    _write(tree / "DS.md", DESIGN.replace("### 6.3 Licenza", "### Licenza"))
    assert regen.main(["--write"]) == 2
    assert "a section this script reads is gone: ### 6.3" in capsys.readouterr().err
    assert (tree / "DS.md").read_bytes().decode("utf-8") == DESIGN.replace("### 6.3 Licenza", "### Licenza")


def test_a_current_inventory_answers_0(tree, capsys):
    """Once the prose exists, the documents are current and the script says so."""
    regen.main(["--write"])
    (tree / "static" / "css" / "main.css").write_bytes(b'@import url("fonts.css");\n@import url("components.css");\n')
    (tree / "static" / "fonts" / "b.woff2").unlink()
    (tree / "templates" / "components" / "y.html").unlink()
    (tree / "static" / "js" / "head.js").unlink()
    (tree / "static" / "js" / "main.js").write_bytes(b"function initA() {}\nfunction initC() {}\n")
    (tree / "static" / "img" / "icons.svg").write_bytes(b'<svg><symbol id="icon-a"/><symbol id="icon-c"/></svg>\n')
    (tree / "static" / "css" / "components.css").write_bytes(b"/*\n   1. Controls\n   2. Feedback\n*/\n")
    capsys.readouterr()
    assert regen.main(["--write"]) == 0
    capsys.readouterr()
    assert regen.main([]) == 0
    assert "the inventory tables and the counts are current" in capsys.readouterr().out


def test_every_anchor_the_script_reads_is_in_the_real_documents():
    """The real DS 2026 and ACCESSIBILITY.md carry every heading, marker and phrase the script rewrites."""
    documents, _result = regen.regenerate()
    assert set(documents) == {regen.DESIGN_DOC, regen.A11Y_DOC}
    for before, after in documents.values():
        assert "\r" not in before and "\r" not in after
