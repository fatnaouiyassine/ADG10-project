"""Sequence de suivi d'une proposition commerciale."""

from datetime import date, datetime

from commercial_templates import nom_contact, signature, titre_formation


SEQUENCE_CLOSING = {
    5: {
        "canal": "WhatsApp",
        "objet": "Suivi de votre proposition",
        "contenu": (
            "Bonjour {nom}, avez-vous pu consulter notre proposition pour « {formation} » ? "
            "Je reste disponible pour clarifier un point ou ajuster le format à vos priorités."
        ),
    },
    8: {
        "canal": "Email",
        "objet": "Vos questions sur notre proposition",
        "contenu": (
            "Bonjour {nom},\n\nJe reviens vers vous concernant notre proposition pour "
            "« {formation} ». Trois points peuvent naturellement mériter un ajustement :\n\n"
            "- Le budget : nous pouvons revoir le périmètre, le nombre de participants ou le format.\n"
            "- L'organisation : le calendrier et les modalités peuvent être adaptés à vos contraintes.\n"
            "- Le contenu : les cas pratiques peuvent être alignés sur vos situations professionnelles.\n\n"
            "Dites-moi simplement le point à approfondir et je vous proposerai une réponse concrète.\n\n"
            "{signature}"
        ),
    },
    12: {
        "canal": "Appel",
        "objet": "Appel de décision",
        "contenu": (
            "Appeler {nom} pour confirmer la décision, identifier le point restant et "
            "convenir d'une prochaine action datée pour « {formation} »."
        ),
    },
}


def jours_depuis_proposition(date_envoi_str: str) -> int | None:
    if not date_envoi_str:
        return None
    proposal_date = datetime.strptime(date_envoi_str, "%Y-%m-%d").date()
    return (date.today() - proposal_date).days


def message_closing_du_jour(
    jours: int,
    lead: dict | None = None,
    formation: dict | None = None,
) -> dict | None:
    raw_message = SEQUENCE_CLOSING.get(jours)
    if not raw_message:
        return None
    message = raw_message.copy()
    message["contenu"] = message["contenu"].format(
        nom=nom_contact(lead),
        formation=titre_formation(formation),
        signature=signature(),
    )
    return message
