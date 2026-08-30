from airtable_client import get_all_records, update_record
from scoring import calculer_score, get_routing
from proposal_generator import generer_proposition_pdf
from nurturing import jours_ecoules, message_du_jour
from email_sender import envoyer_email


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
        email = fields.get("email")

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

            if not email or email == "Non renseigné":
                print(f"   ⚠️  Pas d'email renseigné — impossible d'envoyer la proposition")
            else:
                succes = envoyer_email(
                    destinataire=email,
                    objet=f"Votre proposition de formation - {numero_prop}",
                    contenu=(
                        f"Bonjour {nom},\n\n"
                        f"Veuillez trouver ci-joint notre proposition commerciale "
                        f"pour la formation {formation_par_defaut.get('titre', '')}.\n\n"
                        f"N'hésitez pas à nous contacter pour toute question.\n\n"
                        f"Cordialement,\nADBCENTER LOGISPLAN"
                    ),
                    piece_jointe=fichier
                )
                if succes:
                    print(f"   ✅ Proposition envoyée par email à {email}")
                else:
                    print(f"   ❌ Échec de l'envoi de la proposition")
            continue

        # --- E5 : Nurturing sinon ---
        date_contact = fields.get("date_premier_contact")

        if not date_contact:
            print("⚠️  Pas de date de premier contact renseignée → nurturing ignoré")
            continue

        jours = jours_ecoules(date_contact)
        message = message_du_jour(jours)

        if not message:
            print(f"⏳ Nurturing (J+{jours}) → rien à envoyer aujourd'hui")
            continue

        print(f"📩 Nurturing (J+{jours})")
        print(f"   Canal : {message['canal']}")
        print(f"   Objet : {message['objet']}")

        if message["canal"] == "Email":
            if not email or email == "Non renseigné":
                print(f"   ⚠️  Pas d'email renseigné pour ce lead — envoi impossible")
            else:
                succes = envoyer_email(email, message["objet"], message["contenu"])
                if succes:
                    print(f"   ✅ Email envoyé à {email}")
                else:
                    print(f"   ❌ Échec de l'envoi")
        elif message["canal"] == "WhatsApp":
            print(f"   ⚠️  Canal WhatsApp non connecté — message affiché uniquement (voir CdC E7)")


if __name__ == "__main__":
    main()