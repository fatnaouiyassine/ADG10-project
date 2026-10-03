"""Declinaisons editoriales multicanales."""


def generer_post_linkedin(titre, pitch_100_mots, prix_inter):
    return (
        f"Développer des compétences directement mobilisables : {titre}\n\n"
        f"{pitch_100_mots}\n\n"
        f"Format et investissement indicatif : {prix_inter} MAD HT.\n"
        "La session peut être adaptée au contexte et aux objectifs de votre équipe.\n\n"
        "Échangeons pour identifier le format le plus pertinent.\n\n"
        "#FormationProfessionnelle #DéveloppementDesCompétences #Agadir"
    )


def generer_post_whatsapp(titre, pitch_30_mots):
    return (
        "Bonjour,\n\n"
        f"Nous ouvrons de nouvelles sessions pour *{titre}*.\n\n"
        f"{pitch_30_mots}\n\n"
        "Souhaitez-vous recevoir le programme ou échanger sur vos besoins ?"
    )


def generer_contenu_multicanal(formation: dict) -> dict:
    return {
        "post_linkedin": generer_post_linkedin(
            formation.get("titre", ""),
            formation.get("pitch_100_mots", ""),
            formation.get("prix_inter", ""),
        ),
        "message_whatsapp": generer_post_whatsapp(
            formation.get("titre", ""),
            formation.get("pitch_30_mots", ""),
        ),
    }
