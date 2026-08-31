from datetime import datetime, date


SEQUENCE_CLOSING = {
    5: {
        "canal": "WhatsApp",
        "objet": "Rappel doux",
        "contenu": "Avez-vous eu l'occasion de consulter notre proposition ?"
    },
    8: {
        "canal": "Email",
        "objet": "Vos questions sur notre proposition",
        "contenu": (
            "Bonjour,\n\n"
            "Nous espérons que notre proposition a retenu votre attention. "
            "Voici les réponses aux questions les plus fréquentes :\n\n"
            "- \"C'est trop cher\" → Notre formation génère en moyenne un gain de "
            "productivité équipe de 15-25%. C'est un investissement, pas une dépense. "
            "Éligible OFPPT.\n\n"
            "- \"On peut le faire en interne\" → Une formation externe certifiée apporte "
            "l'objectivité que le management interne ne peut pas toujours avoir.\n\n"
            "- \"On n'est pas prêts\" → C'est le bon moment pour former vos équipes avant "
            "un nouveau projet ou une réorganisation.\n\n"
            "N'hésitez pas à nous contacter pour en discuter.\n\n"
            "Cordialement,\nADBCENTER LOGISPLAN"
        )
    },
    12: {
        "canal": "Appel",
        "objet": "Appel de closing (humain)",
        "contenu": "Script de closing à suivre par Azouguigh (voir section 3.3 du CdC)"
    },
}


def jours_depuis_proposition(date_envoi_str: str) -> int:
    """Calcule le nombre de jours écoulés depuis l'envoi de la proposition."""
    if not date_envoi_str:
        return None
    date_envoi = datetime.strptime(date_envoi_str, "%Y-%m-%d").date()
    aujourd_hui = date.today()
    return (aujourd_hui - date_envoi).days


def message_closing_du_jour(jours: int) -> dict:
    """Retourne le message de relance/closing prévu pour ce jour, s'il y en a un."""
    return SEQUENCE_CLOSING.get(jours)