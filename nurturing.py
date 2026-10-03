"""Sequences de maturation et de qualification des leads."""

from datetime import date, datetime

from commercial_templates import nom_contact, signature, titre_formation


SEQUENCE_NURTURING = {
    0: {
        "canal": "Email",
        "objet": "Votre projet de formation - prochaines étapes",
        "contenu": (
            "Bonjour {nom},\n\nMerci pour votre prise de contact concernant « {formation} ». "
            "Afin de vous orienter vers le format le plus pertinent, nous pouvons préciser "
            "ensemble vos objectifs, le profil des participants et le calendrier souhaité.\n\n"
            "Je reste disponible pour un premier échange.\n\n{signature}"
        ),
    },
    3: {
        "canal": "WhatsApp",
        "objet": "Votre besoin de formation",
        "contenu": (
            "Bonjour {nom}, je reviens vers vous au sujet de « {formation} ». "
            "Je peux vous transmettre le programme détaillé et vous aider à choisir le format "
            "adapté à votre équipe. Souhaitez-vous en discuter ?"
        ),
    },
    7: {
        "canal": "Email",
        "objet": "Un format adapté à vos objectifs",
        "contenu": (
            "Bonjour {nom},\n\nUne formation est plus efficace lorsqu'elle part des situations "
            "réelles rencontrées par les participants. Pour « {formation} », nous pouvons "
            "adapter les cas pratiques, le rythme et les modalités au contexte de votre "
            "organisation.\n\nSi votre projet est toujours d'actualité, je vous propose un court "
            "échange de cadrage.\n\n{signature}"
        ),
    },
    14: {
        "canal": "WhatsApp",
        "objet": "Planification de votre session",
        "contenu": (
            "Bonjour {nom}, avez-vous avancé sur votre projet « {formation} » ? "
            "Nous pouvons vérifier les prochaines disponibilités et préparer une proposition "
            "ajustée à votre calendrier."
        ),
    },
    21: {
        "canal": "Email",
        "objet": "Restons disponibles pour votre projet de formation",
        "contenu": (
            "Bonjour {nom},\n\nJe me permets un dernier message au sujet de « {formation} ». "
            "Si le calendrier ou les priorités ont évolué, nous pourrons reprendre l'échange "
            "au moment qui vous conviendra.\n\nVous pouvez simplement répondre à cet email "
            "pour recevoir le programme ou demander un rendez-vous.\n\n{signature}"
        ),
    },
}

SEQUENCE_QUALIFICATION = {day: SEQUENCE_NURTURING[day] for day in (0, 3, 7)}


def jours_ecoules(date_premier_contact_str: str) -> int | None:
    if not date_premier_contact_str:
        return None
    contact_date = datetime.strptime(date_premier_contact_str, "%Y-%m-%d").date()
    return (date.today() - contact_date).days


def message_du_jour(
    jours: int,
    lead: dict | None = None,
    formation: dict | None = None,
    sequence: str = "nurturing",
) -> dict | None:
    messages = SEQUENCE_QUALIFICATION if sequence == "qualification" else SEQUENCE_NURTURING
    if jours not in messages:
        return None
    message = messages[jours].copy()
    message["contenu"] = message["contenu"].format(
        nom=nom_contact(lead),
        formation=titre_formation(formation),
        signature=signature(),
    )
    return message
