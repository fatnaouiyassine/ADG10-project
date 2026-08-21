def generer_contenu_formation(titre, duree, prix_inter, public):
    """
    Version simulée (mock) — à remplacer plus tard par un vrai appel à Claude API.
    """
    return {
        "pitch_30_mots": f"Découvrez {titre} en {duree}. Une formation conçue pour {public}.",
        "pitch_100_mots": (
            f"Notre formation {titre} s'adresse à {public}. "
            f"Sur {duree}, vous acquerrez des compétences concrètes et applicables immédiatement. "
            f"Investissement : {prix_inter}."
        ),
        "benefices": "1. Compétences pratiques\n2. Formateur certifié\n3. Résultats mesurables",
        "faq": "Q: Combien de participants ? R: 12 max.\nQ: Attestation fournie ? R: Oui."
    }