"""Regles de scoring des leads, independantes des integrations."""

import unicodedata


SCORING_WEIGHTS = {
    "budget": 0.30,
    "urgence": 0.25,
    "decideur": 0.20,
    "taille": 0.15,
    "canal": 0.10,
}


def _normalize(value) -> str:
    text = unicodedata.normalize("NFKD", str(value or ""))
    return " ".join(text.encode("ascii", "ignore").decode().casefold().split())


def _number(value) -> float:
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)
    try:
        return float(str(value or "0").replace(" ", "").replace(",", "."))
    except ValueError:
        return 0.0


def score_budget(budget: float) -> float:
    amount = _number(budget)
    if amount >= 5000:
        return 10
    if amount > 0:
        return 5
    return 0


def score_urgence(urgence: str) -> float:
    return {
        "< 1 mois": 10,
        "moins de 1 mois": 10,
        "3-6 mois": 5,
    }.get(_normalize(urgence), 0)


def score_decideur(decideur: str) -> float:
    return {
        "pdg/drh": 10,
        "pdg": 10,
        "drh": 10,
        "prescripteur": 5,
    }.get(_normalize(decideur), 0)


def score_taille(taille: str) -> float:
    return {
        "pme 10-250+": 10,
        "pme 10-250": 10,
        "tpe 1-9": 5,
    }.get(_normalize(taille), 0)


def score_canal(canal: str) -> float:
    return {
        "recommandation": 10,
        "email direct": 5,
    }.get(_normalize(canal), 0)


def calculer_score(
    budget: float,
    urgence: str,
    decideur: str,
    taille: str,
    canal: str,
) -> float:
    total = (
        score_budget(budget) * SCORING_WEIGHTS["budget"]
        + score_urgence(urgence) * SCORING_WEIGHTS["urgence"]
        + score_decideur(decideur) * SCORING_WEIGHTS["decideur"]
        + score_taille(taille) * SCORING_WEIGHTS["taille"]
        + score_canal(canal) * SCORING_WEIGHTS["canal"]
    )
    return round(total, 1)


def get_routing(score: float) -> str:
    if score >= 8:
        return "Prioritaire : appel sous 4 h et proposition sous 24 h"
    if score >= 5:
        return "Qualification : sequence courte de 8 jours"
    return "Nurturing : sequence progressive de 21 jours"
