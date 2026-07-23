#!/usr/bin/env python3
"""Original PDF helper covering common deterministic operations."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pdfplumber
from pypdf import PdfReader, PdfWriter
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


def page_numbers(spec: str, total: int) -> list[int]:
    result: list[int] = []
    for chunk in spec.split(","):
        part = chunk.strip()
        if not part:
            continue
        if "-" in part:
            start_text, end_text = part.split("-", 1)
            start, end = int(start_text), int(end_text)
            result.extend(range(start, end + 1))
        else:
            result.append(int(part))
    if not result or any(number < 1 or number > total for number in result):
        raise SystemExit(f"Invalid page selection for a {total}-page PDF: {spec}")
    return result


def write_pdf(writer: PdfWriter, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("wb") as handle:
        writer.write(handle)
    print(json.dumps({"output": str(output.resolve()), "pages": len(writer.pages)}, ensure_ascii=False))


def info(path: Path) -> None:
    reader = PdfReader(path)
    sizes = []
    for index, page in enumerate(reader.pages, start=1):
        sizes.append(
            {
                "page": index,
                "width_points": round(float(page.mediabox.width), 2),
                "height_points": round(float(page.mediabox.height), 2),
                "rotation": int(page.rotation or 0),
            }
        )
    metadata = {str(key): str(value) for key, value in (reader.metadata or {}).items()}
    report = {
        "file": str(path.resolve()),
        "pages": len(reader.pages),
        "encrypted": reader.is_encrypted,
        "metadata": metadata,
        "page_sizes": sizes,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))


def extract(path: Path, output: Path) -> None:
    pages = []
    with pdfplumber.open(path) as document:
        for index, page in enumerate(document.pages, start=1):
            pages.append(f"===== Page {index} =====\n{page.extract_text() or ''}".rstrip())
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n\n".join(pages) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.resolve()), "pages": len(pages)}, ensure_ascii=False))


def merge(inputs: list[Path], output: Path) -> None:
    writer = PdfWriter()
    for path in inputs:
        reader = PdfReader(path)
        for page in reader.pages:
            writer.add_page(page)
    write_pdf(writer, output)


def split(source: Path, selection: str, output: Path) -> None:
    reader = PdfReader(source)
    writer = PdfWriter()
    for number in page_numbers(selection, len(reader.pages)):
        writer.add_page(reader.pages[number - 1])
    write_pdf(writer, output)


def rotate(source: Path, degrees: int, output: Path) -> None:
    if degrees not in {90, 180, 270}:
        raise SystemExit("Rotation must be 90, 180, or 270 degrees.")
    reader = PdfReader(source)
    writer = PdfWriter()
    for page in reader.pages:
        page.rotate(degrees)
        writer.add_page(page)
    write_pdf(writer, output)


def create_text(input_path: Path, output: Path, title: str | None) -> None:
    registerFont(UnicodeCIDFont("STSong-Light"))
    styles = getSampleStyleSheet()
    body = ParagraphStyle(
        "ChineseBody",
        parent=styles["BodyText"],
        fontName="STSong-Light",
        fontSize=10.5,
        leading=16,
        alignment=TA_LEFT,
        spaceAfter=8,
    )
    heading = ParagraphStyle(
        "ChineseTitle",
        parent=body,
        fontSize=20,
        leading=26,
        spaceAfter=18,
    )
    story = []
    if title:
        story.append(Paragraph(title.replace("&", "&amp;"), heading))
    for block in input_path.read_text(encoding="utf-8").split("\n\n"):
        value = block.strip()
        if value:
            escaped = value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            story.append(Paragraph(escaped.replace("\n", "<br/>"), body))
            story.append(Spacer(1, 4))
    output.parent.mkdir(parents=True, exist_ok=True)
    document = SimpleDocTemplate(str(output), pagesize=A4, leftMargin=54, rightMargin=54, topMargin=54, bottomMargin=54)
    document.build(story)
    info(output)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    info_cmd = sub.add_parser("info")
    info_cmd.add_argument("input", type=Path)
    extract_cmd = sub.add_parser("extract")
    extract_cmd.add_argument("input", type=Path)
    extract_cmd.add_argument("--output", required=True, type=Path)
    merge_cmd = sub.add_parser("merge")
    merge_cmd.add_argument("inputs", nargs="+", type=Path)
    merge_cmd.add_argument("--output", required=True, type=Path)
    split_cmd = sub.add_parser("split")
    split_cmd.add_argument("input", type=Path)
    split_cmd.add_argument("--pages", required=True)
    split_cmd.add_argument("--output", required=True, type=Path)
    rotate_cmd = sub.add_parser("rotate")
    rotate_cmd.add_argument("input", type=Path)
    rotate_cmd.add_argument("--degrees", required=True, type=int)
    rotate_cmd.add_argument("--output", required=True, type=Path)
    create_cmd = sub.add_parser("create-text")
    create_cmd.add_argument("--input", required=True, type=Path)
    create_cmd.add_argument("--output", required=True, type=Path)
    create_cmd.add_argument("--title")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "info":
        info(args.input)
    elif args.command == "extract":
        extract(args.input, args.output)
    elif args.command == "merge":
        merge(args.inputs, args.output)
    elif args.command == "split":
        split(args.input, args.pages, args.output)
    elif args.command == "rotate":
        rotate(args.input, args.degrees, args.output)
    elif args.command == "create-text":
        create_text(args.input, args.output, args.title)


if __name__ == "__main__":
    main()
