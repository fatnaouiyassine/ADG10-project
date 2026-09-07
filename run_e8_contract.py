from datetime import date
from airtable_client import get_all_records, update_record
from contract_generator import generer_contrat_pdf, generer_facture_pdf
from email_sender import envoyer_email


def prochain_numero(prefixe: str, leads: list) -> str:
    """Calcule le prochain numero sequentiel (ex: FAC-2026-004) en comptant les factures existantes."""
    compteur = 0
    for lead in leads:
        num = lead["fields"].get("numero_facture", "")
        if num and num.startswith(prefixe):
            compteur += 1
    return f"{prefixe}{compteur + 1:03d}"


def main():
    leads = get_all_records("Leads")
    formations = get_all_records("Formations")

    if not formations:
        print("Aucune formation trouvée.")
        return

    formation_par_defaut = formations[0]["fields"]

    for record in leads:
        fields = record["fields"]
        record_id = record["id"]
        nom = fields.get("nom_prenom", "Inconnu")

        client_signe = fields.get("client_signe", False)
        numero_facture_existant = fields.get("numero_facture")

        if not client_signe:
            continue

        if numero_facture_existant:
            print(f"⏭️  {nom} → déjà facturé ({numero_facture_existant}), ignoré")
            continue

        print(f"\n👤 {nom} → client signé, génération du contrat et de la facture")

        numero_contrat = prochain_numero("CONV-2026-", leads)
        numero_facture = prochain_numero("FAC-2026-", leads)

        fichier_contrat = generer_contrat_pdf(fields, formation_par_defaut, numero_contrat)
        fichier_facture = generer_facture_pdf(fields, formation_par_defaut, numero_facture)

        print(f"   ✅ Contrat généré : {fichier_contrat}")
        print(f"   ✅ Facture générée : {fichier_facture}")

        email = fields.get("email")
        if email and email != "Non renseigné":
            succes = envoyer_email(
                destinataire=email,
                objet=f"Bienvenue chez ADBCENTER - Contrat et facture {numero_facture}",
                contenu=(
                    f"Bonjour {nom},\n\n"
                    f"Nous vous confirmons votre inscription. Veuillez trouver ci-joint "
                    f"votre convention de formation ainsi que votre facture.\n\n"
                    f"Bienvenue chez ADBCENTER LOGISPLAN !\n\n"
                    f"Cordialement,\nAzouguigh El Houssaine"
                ),
                piece_jointe=[fichier_contrat, fichier_facture]
            )
            print(f"   {'✅ Email envoyé' if succes else '❌ Échec envoi'} à {email}")

        update_record("Leads", record_id, {
            "numero_facture": numero_facture,
        })


if __name__ == "__main__":
    main()