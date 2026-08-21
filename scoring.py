SCORING_WEIGHTS = {
    "budget": 0.30,
    "urgence": 0.25,
    "decideur": 0.20,
    "taille": 0.15,
    "canal": 0.10,
}


def score_budget(budget: float) -> float:
    if budget >= 5000:
        return 10
    elif budget > 0:
        return 5
    return 0


def score_urgence(urgence: str) -> float:
    return {"< 1 mois": 10, "3-6 mois": 5}.get(urgence, 0)


def score_decideur(decideur: str) -> float:
    return {"PDG/DRH": 10, "prescripteur": 5}.get(decideur, 0)


def score_taille(taille: str) -> float:
    return {"PME 10-250+": 10, "TPE 1-9": 5}.get(taille, 0)


def score_canal(canal: str) -> float:
    return {"recommandation": 10, "email direct": 5}.get(canal, 0)


def calculer_score(budget: float, urgence: str, decideur: str, taille: str, canal: str) -> float:
    """Calcule le score global d'un lead (0-10), selon la grille du CdC section 3.1"""
    total = (
        score_budget(budget) * SCORING_WEIGHTS["budget"] +
        score_urgence(urgence) * SCORING_WEIGHTS["urgence"] +
        score_decideur(decideur) * SCORING_WEIGHTS["decideur"] +
        score_taille(taille) * SCORING_WEIGHTS["taille"] +
        score_canal(canal) * SCORING_WEIGHTS["canal"]
    )
    return round(total, 1)
def get_routing(score: float) -> str:
    """Détermine le traitement à appliquer selon le score (section 3.1)"""
    if score >= 8:
        return "Appel <4h + devis 24h"
    elif score >= 5:
        return "Séquence email 8 jours"
    else:
        return "Nurturing 21 jours"

def get_routing(score: float) -> str:
    """Détermine le traitement à appliquer selon le score (section 3.1)"""
    if score >= 8:
        return "Appel <4h + devis 24h"
    elif score >= 5:
        return "Séquence email 8 jours"
    else:
        return "Nurturing 21 jours"