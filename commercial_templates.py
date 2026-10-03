"""Modèles de messages commerciaux cohérents avec l'identité ADG-10."""

from config import settings


def _value(data: dict | None, key: str, default: str) -> str:
    value = (data or {}).get(key)
    return str(value).strip() if value not in (None, "") else default


def nom_contact(lead: dict | None) -> str:
    return _value(lead, "nom_prenom", "Madame, Monsieur")


def titre_formation(formation: dict | None) -> str:
    return _value(formation, "titre", "la formation envisagée")


def signature() -> str:
    lines = ["Cordialement,", settings.signatory_name, settings.company_name]
    if settings.sender_email:
        lines.append(settings.sender_email)
    if settings.company_phone:
        lines.append(settings.company_phone)
    return "\n".join(lines)


def email_proposition(
    lead: dict,
    formation: dict,
    numero_proposition: str,
) -> tuple[str, str]:
    subject = f"Votre proposition de formation | {numero_proposition}"
    body = (
        f"Bonjour {nom_contact(lead)},\n\n"
        f"Merci pour l'intérêt porté à notre accompagnement. Vous trouverez en pièce "
        f"jointe notre proposition pour « {titre_formation(formation)} ».\n\n"
        "Elle reprend le format recommandé, les objectifs, les modalités d'intervention "
        "et l'investissement correspondant. Nous restons disponibles pour l'ajuster à "
        "vos priorités, au niveau des participants et à votre calendrier.\n\n"
        "Je vous propose un court échange afin de valider ensemble les prochaines étapes.\n\n"
        f"{signature()}"
    )
    return subject, body


def email_documents_signature(
    lead: dict,
    formation: dict,
    numero_facture: str,
) -> tuple[str, str]:
    subject = f"Convention et facture | {numero_facture}"
    body = (
        f"Bonjour {nom_contact(lead)},\n\n"
        "Nous vous remercions pour votre confiance et vous confirmons la prise en charge "
        f"de votre demande concernant « {titre_formation(formation)} ».\n\n"
        "Vous trouverez en pièces jointes la convention de formation et la facture "
        "correspondante. Merci de vérifier les informations administratives et de nous "
        "retourner la convention signée selon les modalités convenues.\n\n"
        "Notre équipe reste disponible pour préparer la session et répondre à toute "
        "question logistique ou pédagogique.\n\n"
        f"{signature()}"
    )
    return subject, body
