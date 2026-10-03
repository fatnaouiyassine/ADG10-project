"""Generation d'une proposition commerciale professionnelle."""

from datetime import date, timedelta
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, Table, TableStyle

from config import settings
from pdf_theme import (
    BORDER,
    LIGHT,
    NAVY,
    TEAL,
    WHITE,
    build_pdf,
    bullet_paragraphs,
    details_table,
    document_styles,
    info_block,
    output_path,
    paragraph,
    section_title,
    text,
    vertical_space,
)


def nettoyer_texte(texte) -> str:
    return text(texte)


def generer_proposition_pdf(
    lead: dict,
    formation: dict,
    numero_prop: str,
    output_dir: Path | None = None,
) -> str:
    today = date.today()
    validity_date = today + timedelta(days=30)
    path = output_path("proposition", numero_prop, output_dir)

    story = [
        Paragraph("Proposition commerciale", document_styles()["title"]),
        Paragraph(
            "Une solution de formation construite autour de vos enjeux, de vos équipes "
            "et de vos objectifs opérationnels.",
            document_styles()["subtitle"],
        ),
    ]

    meta = Table(
        [
            [
                info_block("Référence", numero_prop, 50 * mm),
                info_block("Date", today.strftime("%d/%m/%Y"), 50 * mm),
                info_block("Validité", validity_date.strftime("%d/%m/%Y"), 50 * mm),
            ]
        ],
        colWidths=[52 * mm, 52 * mm, 52 * mm],
        hAlign="LEFT",
    )
    meta.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 2 * mm),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    story.extend([meta, vertical_space(5)])

    story.extend(
        [
            section_title("01", "Votre organisation"),
            details_table(
                [
                    ("Contact", lead.get("nom_prenom")),
                    ("Entreprise", lead.get("entreprise") or lead.get("raison_sociale")),
                    ("Email", lead.get("email")),
                    ("Téléphone", lead.get("telephone")),
                ]
            ),
            section_title("02", "La solution proposée"),
            Paragraph(text(formation.get("titre")), document_styles()["section"]),
            paragraph(
                formation.get("pitch_100_mots")
                or (
                    "Cette intervention sera cadrée avec votre équipe afin de relier les "
                    "apports aux situations professionnelles rencontrées par les participants."
                )
            ),
            details_table(
                [
                    ("Durée", formation.get("duree")),
                    ("Public concerné", formation.get("public")),
                    (
                        "Format",
                        formation.get("modalite")
                        or formation.get("format")
                        or "Présentiel, distanciel ou format hybride selon validation",
                    ),
                    (
                        "Lieu",
                        formation.get("lieu")
                        or "À confirmer selon le format retenu",
                    ),
                ]
            ),
            section_title("03", "Bénéfices attendus"),
        ]
    )
    story.extend(bullet_paragraphs(formation.get("benefices")))

    story.extend(
        [
            section_title("04", "Approche pédagogique"),
            paragraph(
                formation.get("methodes_pedagogiques")
                or (
                    "Alternance d'apports structurés, d'exercices, de mises en situation "
                    "et de temps de synthèse. Le cadrage initial permet d'adapter les exemples "
                    "et les cas pratiques au contexte des participants."
                )
            ),
            section_title("05", "Investissement"),
        ]
    )

    price = text(formation.get("prix_inter"))
    investment = Table(
        [
            [
                Paragraph("INVESTISSEMENT HT", document_styles()["label_light"]),
                Paragraph(f"{price} MAD", document_styles()["amount"]),
            ],
            [
                Paragraph(
                    "Le périmètre final, le nombre de participants et les éventuels frais "
                    "logistiques sont confirmés avant contractualisation.",
                    document_styles()["small_light"],
                ),
                "",
            ],
        ],
        colWidths=[92 * mm, 64 * mm],
    )
    investment.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), NAVY),
                ("TEXTCOLOR", (0, 0), (-1, -1), WHITE),
                ("SPAN", (0, 1), (1, 1)),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5 * mm),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5 * mm),
                ("TOPPADDING", (0, 0), (-1, 0), 4 * mm),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 2 * mm),
                ("TOPPADDING", (0, 1), (-1, 1), 1 * mm),
                ("BOTTOMPADDING", (0, 1), (-1, 1), 4 * mm),
            ]
        )
    )
    story.extend(
        [
            investment,
            section_title("06", "Prochaines étapes"),
            paragraph(
                "1. Validation du périmètre et des objectifs.\n"
                "2. Confirmation du calendrier et des participants.\n"
                "3. Signature de la convention puis préparation de la session."
            ),
            vertical_space(4),
        ]
    )

    contact_box = Table(
        [
            [
                Paragraph("VOTRE INTERLOCUTEUR", document_styles()["label"]),
                Paragraph(settings.signatory_name, document_styles()["value"]),
            ],
            [
                Paragraph("CONTACT", document_styles()["label"]),
                Paragraph(
                    settings.sender_email or settings.company_phone or "Coordonnées à confirmer",
                    document_styles()["value"],
                ),
            ],
        ],
        colWidths=[45 * mm, 111 * mm],
    )
    contact_box.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
                ("BOX", (0, 0), (-1, -1), 0.7, BORDER),
                ("LINEBELOW", (0, 0), (-1, 0), 0.4, BORDER),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4 * mm),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4 * mm),
                ("TOPPADDING", (0, 0), (-1, -1), 3 * mm),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3 * mm),
            ]
        )
    )
    story.extend(
        [
            contact_box,
            section_title("07", "Conditions et accord"),
            paragraph(
                f"{settings.payment_terms} {settings.cancellation_terms}",
                "small",
            ),
        ]
    )

    approval = Table(
        [
            [
                Paragraph("BON POUR ACCORD", document_styles()["label"]),
                Paragraph("SIGNATURE DU CLIENT", document_styles()["label"]),
            ],
            [
                paragraph(
                    f"Organisation : {text(lead.get('entreprise') or lead.get('raison_sociale'))}\n"
                    f"Nom : {text(lead.get('nom_prenom'))}\n"
                    "Date :"
                ),
                paragraph("Signature et cachet précédés de la mention « Bon pour accord » :"),
            ],
        ],
        colWidths=[78 * mm, 78 * mm],
        rowHeights=[10 * mm, 31 * mm],
    )
    approval.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 0.7, BORDER),
                ("LINEBEFORE", (1, 0), (1, -1), 0.7, BORDER),
                ("BACKGROUND", (0, 0), (-1, 0), LIGHT),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4 * mm),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4 * mm),
                ("TOPPADDING", (0, 0), (-1, -1), 3 * mm),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3 * mm),
            ]
        )
    )
    story.append(approval)

    return build_pdf(
        path,
        story,
        document_name="Proposition commerciale",
        title=f"Proposition {numero_prop}",
    )
