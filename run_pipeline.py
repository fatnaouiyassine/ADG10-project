from datetime import date
from airtable_client import get_all_records, update_record
from scoring import calculer_score, get_routing
from proposal_generator import generer_proposition_pdf
from nurturing import jours_ecoules, message_du_jour
from closing import jours_depuis_proposition, message_closing_du_jour
from email_sender import envoyer_email
from whatsapp_sender import envoyer_whatsapp


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
        telephone = fields.get("telephone")

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

        date_envoi_prop = fields.get("date_envoi_proposition")

        # --- E7 : Relance/closing si une proposition a déjà été envoyée ---
        if date_envoi_prop:
            jours_c = jours_depuis_proposition(date_envoi_prop)
            message_c = message_closing_du_jour(jours_c)

            if message_c:
                print(f"🔔 Closing (J+{jours_c} depuis l'envoi de la proposition)")
                print(f"   Canal : {message_c['canal']}")
                print(f"   Objet : {message_c['objet']}")

                if message_c["canal"] == "Email" and email and email != "Non renseigné":
                    succes = envoyer_email(email, message_c["objet"], message_c["contenu"])
                    print(f"   {'✅ Email envoyé' if succes else '❌ Échec envoi'} à {email}")
                elif message_c["canal"] == "WhatsApp":
                    if not telephone:
                        print(f"   ⚠️  Pas de numero de telephone renseigne")
                    else:
                        succes = envoyer_whatsapp(telephone, message_c["contenu"])
                        print(f"   {'✅ WhatsApp envoye' if succes else '❌ Echec envoi'} a {telephone}")
                else:
                    print(f"   ⚠️  Canal '{message_c['canal']}' non automatisable (appel humain requis)")
            else:
                print(f"⏳ Aucune relance de closing prévue aujourd'hui (J+{jours_c})")
            continue

        # --- E6 : Proposition automatique si score élevé (première fois) ---
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
                        f"Cordialement,\nADBCENTER LOGISPLAN"
                    ),
                    piece_jointe=fichier
                )
                if succes:
                    print(f"   ✅ Proposition envoyée par email à {email}")
                    update_record("Leads", record_id, {
                        "date_envoi_proposition": date.today().strftime("%Y-%m-%d")
                    })
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
                print(f"   ⚠️  Pas d'email renseigné")
            else:
                succes = envoyer_email(email, message["objet"], message["contenu"])
                print(f"   {'✅ Email envoyé' if succes else '❌ Échec envoi'} à {email}")
        elif message["canal"] == "WhatsApp":
            if not telephone:
                print(f"   ⚠️  Pas de numero de telephone renseigne")
            else:
                succes = envoyer_whatsapp(telephone, message["contenu"])
                print(f"   {'✅ WhatsApp envoye' if succes else '❌ Echec envoi'} a {telephone}")


if __name__ == "__main__":
    main()