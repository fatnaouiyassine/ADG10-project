from datetime import datetime, date
import calendar


SEQUENCE_NURTURING = {
    0: {
        "canal": "Email",
        "objet": "Bienvenue chez ABC",
        "contenu": "Confirmation + brochure PDF programme + présentation formateur"
    },
    3: {
        "canal": "WhatsApp",
        "objet": "Un résultat similaire au vôtre...",
        "contenu": "Cas concret anonymisé + résultat chiffré (preuve sociale)"
    },
    7: {
        "canal": "Email",
        "objet": "30 min peuvent changer la donne",
        "contenu": "Invitation consultation gratuite (lien Calendly) + FAQ 3 questions"
    },
    14: {
        "canal": "WhatsApp",
        "objet": "Offre valable jusqu'au [date]",
        "contenu": "Témoignage client + remise 10% si signature ce mois"
    },
    21: {
        "canal": "Email",
        "objet": "Dernier message de notre part",
        "contenu": "Récap valeur + invitation à rester en contact + lien ressource gratuite"
    },
}


def jours_ecoules(date_premier_contact_str: str) -> int:
    """Calcule le nombre de jours écoulés depuis le premier contact."""
    if not date_premier_contact_str:
        return None
    date_contact = datetime.strptime(date_premier_contact_str, "%Y-%m-%d").date()
    aujourd_hui = date.today()
    return (aujourd_hui - date_contact).days


def date_fin_de_mois() -> str:
    """Retourne la date du dernier jour du mois en cours, au format JJ/MM/AAAA."""
    aujourd_hui = date.today()
    dernier_jour = calendar.monthrange(aujourd_hui.year, aujourd_hui.month)[1]
    date_limite = date(aujourd_hui.year, aujourd_hui.month, dernier_jour)
    return date_limite.strftime("%d/%m/%Y")


def message_du_jour(jours: int) -> dict:
    """
    Retourne le message de la séquence de nurturing correspondant
    au nombre de jours écoulés, s'il y en a un prévu aujourd'hui.
    """
    if jours not in SEQUENCE_NURTURING:
        return None

    message = SEQUENCE_NURTURING[jours].copy()

    # Remplace le placeholder [date] par une vraie date limite
    if "[date]" in message["objet"]:
        message["objet"] = message["objet"].replace("[date]", date_fin_de_mois())

    return message