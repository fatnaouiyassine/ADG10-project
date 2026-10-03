"""Composants visuels partages par les documents PDF ADG-10."""

from functools import lru_cache
from pathlib import Path
import re
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from config import BASE_DIR, settings


NAVY = colors.HexColor("#102A43")
BLUE = colors.HexColor("#1F5A94")
TEAL = colors.HexColor("#13A89E")
INK = colors.HexColor("#243B53")
MUTED = colors.HexColor("#627D98")
LIGHT = colors.HexColor("#F2F6FA")
BORDER = colors.HexColor("#D9E2EC")
WHITE = colors.white


@lru_cache(maxsize=1)
def register_fonts() -> None:
    font_dir = BASE_DIR / "fonts"
    pdfmetrics.registerFont(TTFont("ADG-Regular", str(font_dir / "DejaVuSans.ttf")))
    pdfmetrics.registerFont(TTFont("ADG-Bold", str(font_dir / "DejaVuSans-Bold.ttf")))
    pdfmetrics.registerFont(
        TTFont("ADG-Italic", str(font_dir / "DejaVuSans-Oblique.ttf"))
    )


@lru_cache(maxsize=1)
def document_styles() -> dict[str, ParagraphStyle]:
    register_fonts()
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "ADGTitle",
            parent=base["Title"],
            fontName="ADG-Bold",
            fontSize=23,
            leading=28,
            textColor=NAVY,
            alignment=TA_LEFT,
            spaceAfter=5 * mm,
        ),
        "subtitle": ParagraphStyle(
            "ADGSubtitle",
            parent=base["Normal"],
            fontName="ADG-Regular",
            fontSize=10,
            leading=15,
            textColor=MUTED,
            spaceAfter=5 * mm,
        ),
        "section": ParagraphStyle(
            "ADGSection",
            parent=base["Heading2"],
            fontName="ADG-Bold",
            fontSize=11,
            leading=15,
            textColor=BLUE,
            spaceBefore=4 * mm,
            spaceAfter=2.5 * mm,
        ),
        "body": ParagraphStyle(
            "ADGBody",
            parent=base["BodyText"],
            fontName="ADG-Regular",
            fontSize=9.2,
            leading=14,
            textColor=INK,
            spaceAfter=2.5 * mm,
        ),
        "small": ParagraphStyle(
            "ADGSmall",
            parent=base["BodyText"],
            fontName="ADG-Regular",
            fontSize=7.5,
            leading=10,
            textColor=MUTED,
        ),
        "small_light": ParagraphStyle(
            "ADGSmallLight",
            parent=base["BodyText"],
            fontName="ADG-Regular",
            fontSize=7.5,
            leading=10,
            textColor=colors.HexColor("#D9E7F5"),
        ),
        "label": ParagraphStyle(
            "ADGLabel",
            parent=base["BodyText"],
            fontName="ADG-Bold",
            fontSize=7.5,
            leading=10,
            textColor=MUTED,
            spaceAfter=1 * mm,
        ),
        "label_light": ParagraphStyle(
            "ADGLabelLight",
            parent=base["BodyText"],
            fontName="ADG-Bold",
            fontSize=7.5,
            leading=10,
            textColor=colors.HexColor("#D9E7F5"),
            spaceAfter=1 * mm,
        ),
        "value": ParagraphStyle(
            "ADGValue",
            parent=base["BodyText"],
            fontName="ADG-Regular",
            fontSize=9,
            leading=13,
            textColor=INK,
        ),
        "value_right": ParagraphStyle(
            "ADGValueRight",
            parent=base["BodyText"],
            fontName="ADG-Regular",
            fontSize=9,
            leading=13,
            textColor=INK,
            alignment=TA_RIGHT,
        ),
        "amount": ParagraphStyle(
            "ADGAmount",
            parent=base["Heading1"],
            fontName="ADG-Bold",
            fontSize=16,
            leading=20,
            textColor=WHITE,
            alignment=TA_RIGHT,
        ),
        "center": ParagraphStyle(
            "ADGCenter",
            parent=base["BodyText"],
            fontName="ADG-Regular",
            fontSize=8.5,
            leading=12,
            textColor=INK,
            alignment=TA_CENTER,
        ),
    }


def text(value, default: str = "Non renseigné") -> str:
    if value is None or str(value).strip() == "":
        return default
    return str(value).strip()


def paragraph(value, style: str = "body") -> Paragraph:
    safe_value = escape(text(value)).replace("\n", "<br/>")
    return Paragraph(safe_value, document_styles()[style])


def section_title(number: str, title: str) -> Paragraph:
    return Paragraph(
        f"{escape(number)}&nbsp;&nbsp;{escape(title)}",
        document_styles()["section"],
    )


def info_block(label: str, value, width: float) -> Table:
    table = Table(
        [
            [Paragraph(escape(label.upper()), document_styles()["label"])],
            [paragraph(value, "value")],
        ],
        colWidths=[width],
    )
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
                ("BOX", (0, 0), (-1, -1), 0.6, BORDER),
                ("LEFTPADDING", (0, 0), (-1, -1), 4 * mm),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4 * mm),
                ("TOPPADDING", (0, 0), (-1, -1), 2.5 * mm),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5 * mm),
            ]
        )
    )
    return table


def details_table(rows: list[tuple[str, object]], widths=None) -> Table:
    data = [
        [
            Paragraph(escape(str(label)), document_styles()["label"]),
            paragraph(value, "value"),
        ]
        for label, value in rows
        if value not in (None, "")
    ]
    table = Table(data, colWidths=widths or [45 * mm, 115 * mm], hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LINEBELOW", (0, 0), (-1, -2), 0.4, BORDER),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3 * mm),
                ("TOPPADDING", (0, 0), (-1, -1), 2.2 * mm),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2 * mm),
            ]
        )
    )
    return table


def bullet_paragraphs(value) -> list:
    lines = [line.strip(" -•\t") for line in text(value, "").splitlines() if line.strip()]
    flowables = []
    for line in lines:
        row = Table(
            [
                [
                    Paragraph("●", document_styles()["body"]),
                    paragraph(line, "body"),
                ]
            ],
            colWidths=[5 * mm, 155 * mm],
        )
        row.setStyle(
            TableStyle(
                [
                    ("TEXTCOLOR", (0, 0), (0, 0), TEAL),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 0),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 1 * mm),
                    ("TOPPADDING", (0, 0), (-1, -1), 0),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 1 * mm),
                ]
            )
        )
        flowables.append(row)
    return flowables or [paragraph("Contenu adapte aux objectifs valides lors du cadrage.")]


def legal_identifiers(data: dict | None = None) -> str:
    source = data if data is not None else {
        "ice": settings.company_ice,
        "if": settings.company_if,
        "rc": settings.company_rc,
        "tp": settings.company_tp,
        "cnss": settings.company_cnss,
    }
    identifiers = [
        ("ICE", source.get("ice")),
        ("IF", source.get("if")),
        ("RC", source.get("rc")),
        ("TP", source.get("tp")),
        ("CNSS", source.get("cnss")),
    ]
    return " | ".join(f"{label} : {value}" for label, value in identifiers if value)


def safe_filename(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", value).strip("._") or "document"


def output_path(prefix: str, reference: str, output_dir: Path | None = None) -> Path:
    target_dir = output_dir or settings.output_dir
    target_dir.mkdir(parents=True, exist_ok=True)
    return target_dir / f"{prefix}_{safe_filename(reference)}.pdf"


def _header_footer(canvas, doc, document_name: str) -> None:
    register_fonts()
    width, height = A4
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.roundRect(18 * mm, height - 25 * mm, 18 * mm, 12 * mm, 2 * mm, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("ADG-Bold", 10)
    canvas.drawCentredString(27 * mm, height - 20.7 * mm, "ADG")
    canvas.setFillColor(NAVY)
    canvas.setFont("ADG-Bold", 10)
    canvas.drawString(41 * mm, height - 18.5 * mm, settings.company_name)
    canvas.setFillColor(MUTED)
    canvas.setFont("ADG-Regular", 7)
    canvas.drawString(41 * mm, height - 22.5 * mm, document_name)
    canvas.setStrokeColor(BORDER)
    canvas.line(18 * mm, height - 29 * mm, width - 18 * mm, height - 29 * mm)

    canvas.line(18 * mm, 16 * mm, width - 18 * mm, 16 * mm)
    canvas.setFillColor(MUTED)
    canvas.setFont("ADG-Regular", 6.5)
    footer = " | ".join(
        item
        for item in [
            settings.company_address,
            settings.sender_email,
            settings.company_phone,
        ]
        if item
    )
    canvas.drawString(18 * mm, 10 * mm, footer[:115])
    canvas.drawRightString(width - 18 * mm, 10 * mm, f"Page {doc.page}")
    canvas.restoreState()


def build_pdf(path: Path, story: list, document_name: str, title: str) -> str:
    document = SimpleDocTemplate(
        str(path),
        pagesize=A4,
        rightMargin=22 * mm,
        leftMargin=22 * mm,
        topMargin=35 * mm,
        bottomMargin=23 * mm,
        title=title,
        author=settings.company_name,
        subject=document_name,
    )
    page_callback = lambda canvas, doc: _header_footer(canvas, doc, document_name)
    document.build(story, onFirstPage=page_callback, onLaterPages=page_callback)
    return str(path)


def vertical_space(height_mm: float = 3) -> Spacer:
    return Spacer(1, height_mm * mm)
