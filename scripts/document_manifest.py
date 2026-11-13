"""
Inventory the authoritative document package and extract it to plain text OUTSIDE the repository.

The source documents are confidential (see docs/security/CONFIDENTIAL_MATERIAL_POLICY.md): this
script deliberately writes its output to a working directory that is not part of the repository, and
redacts the personal data contained in the SIAE deposit form.

    python scripts/document_manifest.py --src <package folder> --out <extraction folder>

Both folders are required, and both lie outside the repository: the script refuses an extraction
folder inside it.

Requires PyMuPDF for PDF files (the project venv does not ship it; the system Python does).
DOCX files are read with the standard library only.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import zipfile
from pathlib import Path

# S314: the XML parsed here is the word/document.xml of a DOCX handed to us by the project owner
# and opened from the local disk. It is not network input. defusedxml is not a dependency of this
# project and adding one for a one-shot extraction script would be a worse trade.
from xml.etree import ElementTree as ET  # noqa: S405

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

#: Personal data present in the filled SIAE deposit form. Redacted from the extracted text so that a
#: working copy of the extraction never carries identifiers. The patterns are deliberately generic.
REDACTIONS = [
    (re.compile(r"\b[A-Z]{6}\d{2}[A-Z]\d{2}[A-Z]\d{3}[A-Z]\b"), "[CODICE FISCALE REDACTED]"),
    (re.compile(r"\+\d{2}\s?\d{3}\s?\d{3,4}\s?\d{3,4}"), "[PHONE REDACTED]"),
    (re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"), "[EMAIL REDACTED]"),
    (re.compile(r"\b\d{2}/\d{2}/(19|20)\d{2}\b"), "[DATE REDACTED]"),
]


def paragraph_text(node) -> str:
    parts: list[str] = []
    for child in node.iter():
        if child.tag == W + "t":
            parts.append(child.text or "")
        elif child.tag == W + "tab":
            parts.append("\t")
        elif child.tag in (W + "br", W + "cr"):
            parts.append("\n")
    return "".join(parts)


def docx_to_text(path: Path) -> tuple[str, str]:
    archive = zipfile.ZipFile(path)
    body_lines: list[str] = []

    def walk(container) -> None:
        for child in container:
            if child.tag == W + "p":
                style_node = child.find(f"{W}pPr/{W}pStyle")
                style = style_node.get(W + "val") if style_node is not None else ""
                text = paragraph_text(child)
                if text.strip():
                    heading = re.fullmatch(r"(?:Heading|Titolo|Titre)\s?(\d)", style or "")
                    prefix = "#" * int(heading.group(1)) + " " if heading else ""
                    body_lines.append(prefix + text)
            elif child.tag == W + "tbl":
                for row in child.iter(W + "tr"):
                    cells = [
                        " / ".join(t for p in cell.iter(W + "p") if (t := paragraph_text(p).strip()))
                        for cell in row.findall(W + "tc")
                    ]
                    body_lines.append("| " + " | ".join(cells) + " |")
                body_lines.append("")
            elif child.tag == W + "sdt":
                content = child.find(W + "sdtContent")
                if content is not None:
                    walk(content)

    root = ET.fromstring(archive.read("word/document.xml"))  # noqa: S314 - local DOCX, see module header
    walk(root.find(W + "body"))

    extras: list[str] = []
    for name in archive.namelist():
        if re.match(r"word/(header|footer|footnotes|endnotes|comments)\d*\.xml", name):
            part = ET.fromstring(archive.read(name))  # noqa: S314 - local DOCX, see module header
            texts = [t for p in part.iter(W + "p") if (t := paragraph_text(p).strip())]
            if texts:
                extras.append(f"--- {name} ---\n" + "\n".join(texts))
    return "\n".join(body_lines), "\n".join(extras)


def pdf_to_text(path: Path) -> tuple[str, int]:
    import fitz  # imported lazily: only needed for PDF sources

    document = fitz.open(str(path))
    pages = [f"=== page {index + 1} ===\n" + page.get_text() for index, page in enumerate(document)]
    return "\n\n".join(pages), len(document)


def redact(text: str) -> str:
    for pattern, replacement in REDACTIONS:
        text = pattern.sub(replacement, text)
    return text


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--src", required=True, help="the confidential package folder, outside the repository")
    parser.add_argument("--out", required=True, help="the extraction folder, outside the repository")
    parser.add_argument("--redact-pdf", action="store_true", default=True)
    args = parser.parse_args()

    source = Path(args.src)
    out = Path(args.out)
    if out.resolve().is_relative_to(Path(__file__).resolve().parents[1]):
        raise SystemExit("refusing to extract confidential documents inside the repository")
    out.mkdir(parents=True, exist_ok=True)

    manifest = []
    for path in sorted(source.rglob("*")):
        if not path.is_file():
            continue
        data = path.read_bytes()
        stat = path.stat()
        row = {
            "relative_path": str(path.relative_to(source)),
            "filename": path.name,
            "extension": path.suffix.lower().lstrip("."),
            "size_bytes": stat.st_size,
            "modified": dt.datetime.fromtimestamp(stat.st_mtime).isoformat(timespec="minutes"),
            "sha256": hashlib.sha256(data).hexdigest(),
        }
        if path.suffix.lower() == ".docx":
            body, extras = docx_to_text(path)
            (out / f"{path.stem}.txt").write_text(f"{body}\n\n{extras}", encoding="utf-8")
            row["characters"] = len(body)
        elif path.suffix.lower() == ".pdf":
            body, pages = pdf_to_text(path)
            if args.redact_pdf:
                body = redact(body)
            (out / f"{path.stem}.txt").write_text(body, encoding="utf-8")
            row["characters"] = len(body)
            row["pages"] = pages
        manifest.append(row)

    (out / "manifest.json").write_text(json.dumps(manifest, indent=1, ensure_ascii=False), encoding="utf-8")
    for row in manifest:
        print(f"{row['sha256'][:16]}… {row['size_bytes']:>8}  {row['filename']}")
    print(f"\n{len(manifest)} document(s) -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
