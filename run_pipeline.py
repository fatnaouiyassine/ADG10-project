from airtable_client import get_all_records, update_record
from scoring import calculer_score, get_routing
from proposal_generator import generer_proposition_pdf
from nurturing import jours_ecoules, message_du_jour


def main():
    leads = get_all_records("Leads")
    formations = get_all_records("Formations")

    if not formations:
        print("Aucune formation trouvée.")
        return

    formation_par_defaut = formations[0]["fields"]

    for i, record in enumerate(leads):
        fields = record["fields"]
        record_id = record["id"]
        nom = fields.get("nom_prenom", "Inconnu")

        print(f"\n{'='*50}")
        print(f"👤 {nom}")
        print(f"{'='*50}")

        # --- E4 : Scoring ---
        score = calculer_score(
            budget=fields.get("budget_declare", 0),
            urgence=fields.get("urgence", ""),
            decideur=fields.get("decideur", ""),
            taille=fields.get("taille_entreprise", ""),
            canal=fields.get("canal_entree", "")
        )
        routing = get_routing(score)
        update_record("Leads", record_id, {"score": score})
        print(f"📊 Score : {score}/10 → {routing}")

        # --- E6 : Proposition automatique si score élevé ---
        if score >= 8:
            numero_prop = f"PROP-2026-{i+1:03d}"
            fichier = generer_proposition_pdf(fields, formation_par_defaut, numero_prop)
            print(f"✅ Score élevé → proposition générée : {fichier}")
        else:
            # --- E5 : Nurturing si score pas assez élevé pour un devis direct ---
            date_contact = fields.get("date_premier_contact")

            if not date_contact:
                print("⚠️  Pas de date de premier contact renseignée → nurturing ignoré")
                continue

            jours = jours_ecoules(date_contact)
            message = message_du_jour(jours)

            if message:
                print(f"📩 Nurturing (J+{jours}) → ENVOYER MAINTENANT")
                print(f"   Canal : {message['canal']}")
                print(f"   Objet : {message['objet']}")
                print(f"   Contenu : {message['contenu']}")
            else:
                print(f"⏳ Nurturing (J+{jours}) → rien à envoyer aujourd'hui")


if __name__ == "__main__":
    main()