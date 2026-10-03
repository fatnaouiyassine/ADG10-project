from airtable_client import get_all_records
from nurturing import jours_ecoules, message_du_jour
from pipeline_utils import choisir_formation


def main():
    leads = get_all_records("Leads")
    formations = get_all_records("Formations")

    print(f"{len(leads)} leads à vérifier pour le nurturing.\n")

    for record in leads:
        fields = record["fields"]
        nom = fields.get("nom_prenom", "Inconnu")
        date_contact = fields.get("date_premier_contact")

        if not date_contact:
            print(f"⚠️  {nom} → pas de date de premier contact renseignée, ignoré")
            continue

        jours = jours_ecoules(date_contact)
        formation = choisir_formation(fields, formations)
        try:
            score = float(fields.get("score", 0) or 0)
        except (TypeError, ValueError):
            score = 0
        sequence = "qualification" if score >= 5 else "nurturing"
        message = message_du_jour(
            jours,
            lead=fields,
            formation=formation,
            sequence=sequence,
        )

        if message:
            print(f"📩 {nom} (J+{jours}) → ENVOYER MAINTENANT")
            print(f"   Canal : {message['canal']}")
            print(f"   Objet : {message['objet']}")
            print(f"   Contenu : {message['contenu']}\n")
        else:
            print(f"⏳ {nom} (J+{jours}) → rien à envoyer aujourd'hui\n")


if __name__ == "__main__":
    main()
