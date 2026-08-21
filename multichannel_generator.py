def generer_post_linkedin(titre, pitch_100_mots, prix_inter):
    return (
        f"🎓 {titre}\n\n"
        f"{pitch_100_mots}\n\n"
        f"💰 Investissement : {prix_inter} MAD HT\n"
        f"📍 Formation disponible à Agadir et en distanciel\n\n"
        f"#Formation #ADBCENTER #Agadir"
    )


def generer_post_whatsapp(titre, pitch_30_mots):
    return (
        f"Bonjour 👋\n\n"
        f"Nouvelle formation disponible : *{titre}*\n"
        f"{pitch_30_mots}\n\n"
        f"Intéressé(e) ? Répondez à ce message pour plus d'infos."
    )


def generer_contenu_multicanal(formation: dict) -> dict:
    titre = formation.get("titre", "")
    pitch_30 = formation.get("pitch_30_mots", "")
    pitch_100 = formation.get("pitch_100_mots", "")
    prix = formation.get("prix_inter", "")

    return {
        "post_linkedin": generer_post_linkedin(titre, pitch_100, prix),
        "message_whatsapp": generer_post_whatsapp(titre, pitch_30),
    }