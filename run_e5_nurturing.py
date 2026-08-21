from airtable_client import get_all_records
from nurturing import jours_ecoules, message_du_jour


def main():
    leads = get_all_records("Leads")

    print(f"{len(leads)} leads à vérifier pour le nurturing.\n")

    for record in leads:
        fields = record["fields"]
        nom = fields.get("nom_prenom", "Inconnu")
        date_contact = fields.get("date_premier_contact")

        if not date_contact:
            print(f"⚠️  {nom} → pas de date de premier contact renseignée, ignoré")
            continue

        jours = jours_ecoules(date_contact)
        message = message_du_jour(jours)

        if message:
            print(f"📩 {nom} (J+{jours}) → ENVOYER MAINTENANT")
            print(f"   Canal : {message['canal']}")
            print(f"   Objet : {message['objet']}")
            print(f"   Contenu : {message['contenu']}\n")
        else:
            print(f"⏳ {nom} (J+{jours}) → rien à envoyer aujourd'hui\n")


if __name__ == "__main__":
    main()