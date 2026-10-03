"""Generation de conventions de formation et de factures."""

from datetime import date, timedelta
from pathlib import Path
import re

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
    legal_identifiers,
    output_path,
    paragraph,
    section_title,
    text,
    vertical_space,
)


def nettoyer_texte(texte) -> str:
    return text(texte)


def calculer_prix_ht(prix) -> float:
    """Extrait un prix HT, y compris depuis une valeur formatee ou une fourchette."""
    if isinstance(prix, bool) or prix in (None, ""):
        return 0.0
    if isinstance(prix, (int, float)):
        return float(prix)

    raw = str(prix).replace("\u00a0", "").replace(" ", "")
    match = re.search(r"\d[\d.,]*", raw)
    if not match:
        return 0.0
    number = match.group(0)
    if "," in number and "." in number:
        if number.rfind(",") > number.rfind("."):
            number = number.replace(".", "").replace(",", ".")
        else:
            number = number.replace(",", "")
    elif "," in number:
        decimals = len(number.rsplit(",", 1)[-1])
        number = number.replace(",", ".") if decimals == 2 else number.replace(",", "")
    elif number.count(".") > 1:
        number = number.replace(".", "")
    try:
        return float(number)
    except ValueError:
        return 0.0


def _prix_formation(formation: dict) -> float:
    return calculer_prix_ht(
        formation.get("prix_ht")
        or formation.get("prix_facture")
        or formation.get("prix_inter")
    )


def _money(amount: float) -> str:
    formatted = f"{amount:,.2f}".replace(",", " ").replace(".", ",")
    return f"{formatted} MAD"


def _client_name(lead: dict) -> str:
    return text(
        lead.get("entreprise")
        or lead.get("raison_sociale")
        or lead.get("nom_prenom")
    )


def _party_card(title: str, lines: list[str]) -> Table:
    data = [[Paragraph(title.upper(), document_styles()["label"])]]
    data.extend([[paragraph(line, "value")] for line in lines if line])
    card = Table(data, colWidths=[76 * mm])
    card.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
                ("BOX", (0, 0), (-1, -1), 0.6, BORDER),
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E6EEF6")),
                ("LEFTPADDING", (0, 0), (-1, -1), 4 * mm),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4 * mm),
                ("TOPPADDING", (0, 0), (-1, -1), 2.5 * mm),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5 * mm),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    return card


def generer_contrat_pdf(
    lead: dict,
    formation: dict,
    numero_contrat: str,
    output_dir: Path | None = None,
) -> str:
    today = date.today()
    path = output_path("contrat", numero_contrat, output_dir)
    price_ht = _prix_formation(formation)
    tax_rate = float(formation.get("taux_tva", 20) or 20)
    tax = price_ht * tax_rate / 100
    total = price_ht + tax

    provider_lines = [
        settings.company_legal_name,
        settings.company_address,
        legal_identifiers(),
        settings.sender_email,
        settings.company_phone,
    ]
    client_identifiers = legal_identifiers(
        {
            "ice": lead.get("ice"),
            "if": lead.get("if"),
            "rc": lead.get("rc"),
            "tp": lead.get("tp"),
            "cnss": lead.get("cnss"),
        }
    )
    client_lines = [
        _client_name(lead),
        text(lead.get("nom_prenom"), ""),
        text(lead.get("adresse"), ""),
        client_identifiers,
        text(lead.get("email"), ""),
        text(lead.get("telephone"), ""),
    ]

    story = [
        Paragraph("Convention de formation", document_styles()["title"]),
        Paragraph(
            "Cadre contractuel de l'intervention et engagements des parties.",
            document_styles()["subtitle"],
        ),
        details_table(
            [
                ("Référence", numero_contrat),
                ("Date d'émission", today.strftime("%d/%m/%Y")),
                (
                    "Session",
                    formation.get("date_session")
                    or formation.get("dates")
                    or "À planifier d'un commun accord",
                ),
            ]
        ),
        section_title("01", "Parties à la convention"),
    ]

    parties = Table(
        [[_party_card("Le prestataire", provider_lines), _party_card("Le client", client_lines)]],
        colWidths=[80 * mm, 80 * mm],
    )
    parties.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (0, -1), 4 * mm),
                ("RIGHTPADDING", (1, 0), (1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    story.extend(
        [
            parties,
            section_title("02", "Objet et périmètre"),
            paragraph(
                f"La présente convention encadre la réalisation de la formation "
                f"« {text(formation.get('titre'))} » par {settings.company_legal_name} "
                f"au bénéfice du Client."
            ),
            details_table(
                [
                    ("Intitulé", formation.get("titre")),
                    ("Durée", formation.get("duree")),
                    ("Public concerné", formation.get("public")),
                    (
                        "Modalité",
                        formation.get("modalite")
                        or formation.get("format")
                        or "À confirmer avant la session",
                    ),
                    (
                        "Lieu",
                        formation.get("lieu")
                        or "À confirmer avant la session",
                    ),
                    (
                        "Participants",
                        formation.get("nombre_participants")
                        or lead.get("nombre_participants")
                        or "À confirmer",
                    ),
                ]
            ),
            section_title("03", "Objectifs et approche"),
            paragraph(
                formation.get("objectifs")
                or formation.get("pitch_100_mots")
                or (
                    "Les objectifs opérationnels sont précisés lors du cadrage. "
                    "L'intervention alterne apports, exercices et mises en situation."
                )
            ),
        ]
    )
    story.extend(bullet_paragraphs(formation.get("benefices")))
    story.extend(
        [
            section_title("04", "Engagements du prestataire"),
            paragraph(
                "Le Prestataire s'engage à mobiliser les moyens pédagogiques convenus, "
                "à assurer l'intervention avec diligence et à informer le Client de tout "
                "événement susceptible d'affecter le déroulement de la session."
            ),
            section_title("05", "Engagements du client"),
            paragraph(
                "Le Client communique les informations nécessaires au cadrage, confirme "
                "la liste des participants, met à disposition les moyens convenus et veille "
                "au respect des modalités administratives et financières."
            ),
            section_title("06", "Conditions financières"),
        ]
    )

    finance = Table(
        [
            ["Montant HT", _money(price_ht)],
            [f"TVA ({tax_rate:g} %)", _money(tax)],
            ["TOTAL TTC", _money(total)],
        ],
        colWidths=[100 * mm, 60 * mm],
    )
    finance.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, -2), "ADG-Regular"),
                ("FONTNAME", (0, -1), (-1, -1), "ADG-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("TEXTCOLOR", (0, 0), (-1, -1), NAVY),
                ("ALIGN", (1, 0), (1, -1), "RIGHT"),
                ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#DFF5F2")),
                ("BOX", (0, 0), (-1, -1), 0.7, BORDER),
                ("LINEBELOW", (0, 0), (-1, -2), 0.4, BORDER),
                ("LEFTPADDING", (0, 0), (-1, -1), 4 * mm),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4 * mm),
                ("TOPPADDING", (0, 0), (-1, -1), 3 * mm),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3 * mm),
            ]
        )
    )
    story.extend(
        [
            finance,
            vertical_space(2),
            paragraph(settings.payment_terms, "small"),
            section_title("07", "Report, annulation et confidentialité"),
            paragraph(settings.cancellation_terms),
            paragraph(
                "Chaque partie s'engage à traiter comme confidentielles les informations "
                "non publiques obtenues dans le cadre de la préparation et de l'exécution "
                "de la formation."
            ),
            section_title("08", "Prise d'effet et règlement des différends"),
            paragraph(
                "La convention prend effet à sa signature par les deux parties. Toute "
                "difficulté d'interprétation ou d'exécution fait d'abord l'objet d'une "
                "recherche de solution amiable. À défaut, les parties se rapprochent de "
                "leurs conseils pour déterminer la suite appropriée."
            ),
            vertical_space(1),
        ]
    )

    signatures = Table(
        [
            [
                Paragraph("POUR LE PRESTATAIRE", document_styles()["label"]),
                Paragraph("POUR LE CLIENT", document_styles()["label"]),
            ],
            [
                paragraph(
                    f"{settings.signatory_name}\n{settings.signatory_title}\n\n"
                    "Date, signature et cachet :"
                ),
                paragraph(
                    f"{_client_name(lead)}\n\nDate, signature et cachet :"
                ),
            ],
        ],
        colWidths=[80 * mm, 80 * mm],
        rowHeights=[8 * mm, 26 * mm],
    )
    signatures.setStyle(
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
    story.append(signatures)

    return build_pdf(
        path,
        story,
        document_name="Convention de formation",
        title=f"Convention {numero_contrat}",
    )


def generer_facture_pdf(
    lead: dict,
    formation: dict,
    numero_facture: str,
    output_dir: Path | None = None,
) -> str:
    today = date.today()
    due_date = today + timedelta(days=30)
    path = output_path("facture", numero_facture, output_dir)
    price_ht = _prix_formation(formation)
    tax_rate = float(formation.get("taux_tva", 20) or 20)
    tax = price_ht * tax_rate / 100
    total = price_ht + tax

    story = [
        Paragraph("Facture", document_styles()["title"]),
        Paragraph(
            f"Référence {numero_facture}",
            document_styles()["subtitle"],
        ),
    ]

    identity = Table(
        [
            [
                _party_card(
                    "Émetteur",
                    [
                        settings.company_legal_name,
                        settings.company_address,
                        legal_identifiers(),
                        settings.sender_email,
                        settings.company_phone,
                    ],
                ),
                _party_card(
                    "Facturé à",
                    [
                        _client_name(lead),
                        text(lead.get("nom_prenom"), ""),
                        text(lead.get("adresse"), ""),
                        legal_identifiers(
                            {
                                "ice": lead.get("ice"),
                                "if": lead.get("if"),
                                "rc": lead.get("rc"),
                                "tp": lead.get("tp"),
                                "cnss": lead.get("cnss"),
                            }
                        ),
                        text(lead.get("email"), ""),
                    ],
                ),
            ]
        ],
        colWidths=[80 * mm, 80 * mm],
    )
    identity.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (0, -1), 4 * mm),
                ("RIGHTPADDING", (1, 0), (1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    story.extend(
        [
            identity,
            vertical_space(5),
            details_table(
                [
                    ("Date de facture", today.strftime("%d/%m/%Y")),
                    ("Date d'échéance", due_date.strftime("%d/%m/%Y")),
                    ("Référence client", lead.get("reference_client")),
                ]
            ),
            vertical_space(5),
        ]
    )

    line_items = Table(
        [
            ["DESCRIPTION", "QTÉ", "PRIX HT", "TOTAL HT"],
            [
                Paragraph(
                    text(formation.get("titre")),
                    document_styles()["value"],
                ),
                "1",
                _money(price_ht),
                _money(price_ht),
            ],
        ],
        colWidths=[82 * mm, 18 * mm, 30 * mm, 30 * mm],
    )
    line_items.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
                ("FONTNAME", (0, 0), (-1, 0), "ADG-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "ADG-Regular"),
                ("FONTSIZE", (0, 0), (-1, -1), 8.5),
                ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BOX", (0, 0), (-1, -1), 0.7, BORDER),
                ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
                ("LEFTPADDING", (0, 0), (-1, -1), 3 * mm),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3 * mm),
                ("TOPPADDING", (0, 0), (-1, -1), 3 * mm),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3 * mm),
            ]
        )
    )
    story.extend([line_items, vertical_space(4)])

    totals = Table(
        [
            ["Sous-total HT", _money(price_ht)],
            [f"TVA ({tax_rate:g} %)", _money(tax)],
            ["TOTAL A PAYER", _money(total)],
        ],
        colWidths=[45 * mm, 43 * mm],
        hAlign="RIGHT",
    )
    totals.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, -2), "ADG-Regular"),
                ("FONTNAME", (0, -1), (-1, -1), "ADG-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("ALIGN", (1, 0), (1, -1), "RIGHT"),
                ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#DFF5F2")),
                ("TEXTCOLOR", (0, -1), (-1, -1), NAVY),
                ("LINEBELOW", (0, 0), (-1, -2), 0.4, BORDER),
                ("BOX", (0, 0), (-1, -1), 0.7, BORDER),
                ("LEFTPADDING", (0, 0), (-1, -1), 3 * mm),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3 * mm),
                ("TOPPADDING", (0, 0), (-1, -1), 3 * mm),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3 * mm),
            ]
        )
    )
    story.extend(
        [
            totals,
            section_title("01", "Modalités de paiement"),
            paragraph(settings.payment_terms),
        ]
    )
    if settings.company_bank or settings.company_rib:
        story.append(
            details_table(
                [
                    ("Banque", settings.company_bank),
                    ("RIB", settings.company_rib),
                ]
            )
        )
    story.extend(
        [
            vertical_space(3),
            paragraph(
                "Merci d'indiquer la référence de la facture lors du règlement. "
                "Pour toute question administrative, contactez-nous aux coordonnées "
                "figurant en bas de page.",
                "small",
            ),
        ]
    )

    return build_pdf(
        path,
        story,
        document_name="Facture",
        title=f"Facture {numero_facture}",
    )
