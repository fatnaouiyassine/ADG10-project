import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generer_contenu_formation(titre, duree, prix_inter, public):
    """
    Genere le contenu marketing d'une formation via un vrai appel a l'IA (Groq).
    """
    prompt = f"""Tu es un expert en marketing pour un centre de formation professionnelle au Maroc.

Voici une formation :
- Titre : {titre}
- Duree : {duree}
- Prix : {prix_inter} MAD HT
- Public cible : {public}

Genere le contenu suivant, en francais, dans un style professionnel et convaincant.
Reponds UNIQUEMENT avec un objet JSON valide, sans texte avant ou apres, avec exactement ces cles :
- "pitch_30_mots" : un pitch tres court et accrocheur (environ 30 mots)
- "pitch_100_mots" : un pitch plus detaille (environ 100 mots)
- "benefices" : 3 benefices cles, sous forme de texte avec des sauts de ligne (\\n) entre chaque
- "faq" : 2 questions frequentes avec leurs reponses courtes, sous forme de texte avec des sauts de ligne (\\n) entre chaque
"""

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2000,
            reasoning_effort="low",
        )

        texte = response.choices[0].message.content.strip()

        if texte.startswith("```"):
            texte = texte.split("```")[1]
            if texte.startswith("json"):
                texte = texte[4:]
            texte = texte.strip()

        contenu = json.loads(texte)
        return contenu

    except Exception as e:
        print(f"⚠️  Erreur lors de la generation avec Groq : {e}")
        return {
            "pitch_30_mots": f"Decouvrez {titre} en {duree}.",
            "pitch_100_mots": f"Formation {titre} pour {public}.",
            "benefices": "Erreur de generation - a completer manuellement",
            "faq": "Erreur de generation - a completer manuellement"
        }