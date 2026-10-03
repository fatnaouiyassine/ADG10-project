"""Generation de contenus marketing structures avec Groq."""

import json

from config import require_configuration, settings


class ContentGenerationError(RuntimeError):
    """Erreur de generation qui ne doit pas ecraser un contenu Airtable valide."""


EXPECTED_FIELDS = {"pitch_30_mots", "pitch_100_mots", "benefices", "faq"}


def _client_groq():
    from groq import Groq

    require_configuration("groq_api_key")
    return Groq(api_key=settings.groq_api_key)


def _validate_content(content: dict) -> dict:
    if not isinstance(content, dict):
        raise ContentGenerationError("La reponse IA n'est pas un objet JSON.")
    missing = EXPECTED_FIELDS - set(content)
    if missing:
        raise ContentGenerationError(
            "Champs manquants dans la reponse IA : " + ", ".join(sorted(missing))
        )
    cleaned = {field: str(content[field]).strip() for field in EXPECTED_FIELDS}
    if any(not value for value in cleaned.values()):
        raise ContentGenerationError("La reponse IA contient au moins un champ vide.")
    return cleaned


def generer_contenu_formation(titre, duree, prix_inter, public):
    """Genere un contenu B2B fiable, sans ecraser Airtable en cas d'erreur."""
    prompt = f"""Tu es un rédacteur B2B spécialisé dans la formation professionnelle au Maroc.

Voici une formation :
- Titre : {titre}
- Durée : {duree}
- Prix : {prix_inter} MAD HT
- Public cible : {public}

Rédige un contenu en français, crédible, clair et orienté vers la valeur métier.
Le ton doit être professionnel, humain et précis, sans superlatifs artificiels.
N'invente aucune certification, statistique, garantie, remise ou référence client.
Utilise des verbes d'action et des bénéfices observables.

Réponds UNIQUEMENT avec un objet JSON valide, sans texte avant ou après, avec exactement ces clés :
- "pitch_30_mots" : 25 à 35 mots, promesse concrète et public clairement identifié
- "pitch_100_mots" : 80 à 110 mots, problème, approche, résultats attendus et appel à l'action discret
- "benefices" : exactement 3 bénéfices, une ligne par bénéfice
- "faq" : exactement 3 questions-réponses utiles, séparées par des sauts de ligne
"""

    try:
        response = _client_groq().chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.45,
            max_tokens=2000,
            reasoning_effort="low",
        )
        text = response.choices[0].message.content.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
            text = text.strip()
        return _validate_content(json.loads(text))
    except Exception as exc:
        if isinstance(exc, ContentGenerationError):
            raise
        raise ContentGenerationError(f"Generation Groq impossible : {exc}") from exc
