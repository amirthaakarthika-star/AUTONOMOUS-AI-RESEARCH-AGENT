from pathlib import Path
from io import BytesIO
import re

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.enums import TA_CENTER

from src.utils import build_timestamped_filename, ensure_output_dir


def markdown_to_pdf_bytes(report: str, topic: str) -> bytes:
    """Convert markdown report text to PDF bytes using reportlab."""
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Title"],
        fontSize=22,
        textColor=colors.HexColor("#0a2540"),
        spaceAfter=6,
        alignment=TA_CENTER,
    )
    h2_style = ParagraphStyle(
        "CustomH2",
        parent=styles["Heading2"],
        fontSize=15,
        textColor=colors.HexColor("#1a56db"),
        spaceBefore=14,
        spaceAfter=4,
    )
    h3_style = ParagraphStyle(
        "CustomH3",
        parent=styles["Heading3"],
        fontSize=12,
        textColor=colors.HexColor("#0a2540"),
        spaceBefore=10,
        spaceAfter=3,
    )
    body_style = ParagraphStyle(
        "CustomBody",
        parent=styles["Normal"],
        fontSize=10,
        leading=15,
        textColor=colors.HexColor("#222222"),
        spaceAfter=6,
    )
    bullet_style = ParagraphStyle(
        "CustomBullet",
        parent=styles["Normal"],
        fontSize=10,
        leading=14,
        leftIndent=14,
        textColor=colors.HexColor("#333333"),
        spaceAfter=3,
    )

    story = []

    for line in report.splitlines():
        stripped = line.strip()

        if not stripped:
            story.append(Spacer(1, 4))
            continue

        if stripped.startswith("# "):
            text = stripped[2:].strip()
            story.append(Paragraph(text, title_style))
            story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1a56db"), spaceAfter=8))

        elif stripped.startswith("## "):
            text = stripped[3:].strip()
            story.append(Paragraph(text, h2_style))

        elif stripped.startswith("### "):
            text = stripped[4:].strip()
            story.append(Paragraph(text, h3_style))

        elif stripped.startswith(("- ", "* ")):
            text = _clean_inline_markdown(stripped[2:].strip())
            story.append(Paragraph(f"&bull; &nbsp; {text}", bullet_style))

        else:
            text = _clean_inline_markdown(stripped)
            story.append(Paragraph(text, body_style))

    doc.build(story)
    return buffer.getvalue()


def _clean_inline_markdown(text: str) -> str:
    """Convert inline markdown to reportlab XML tags."""
    text = re.sub(r"\*\*\*(.*?)\*\*\*", r"<b><i>\1</i></b>", text)
    text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"\*(.*?)\*", r"<i>\1</i>", text)
    text = re.sub(r"`(.*?)`", r"<font name='Courier'>\1</font>", text)
    text = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", text)
    return text


def save_markdown_report(report: str, topic: str, output_dir: str = "outputs") -> str:
    """Save report as PDF and return path."""
    ensure_output_dir(output_dir)
    file_name = build_timestamped_filename(topic).replace(".md", ".pdf")
    output_path = Path(output_dir) / file_name
    pdf_bytes = markdown_to_pdf_bytes(report, topic)
    output_path.write_bytes(pdf_bytes)
    return str(output_path)

