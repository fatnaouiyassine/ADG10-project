from airtable_client import get_all_records
from proposal_generator import generer_proposition_pdf


def main():
    leads = get_all_records("Leads")
    formations = get_all_records("Formations")

    if not leads or not formations:
        print("Pas assez de données pour tester.")
        return

    lead = leads[0]["fields"]
    formation = formations[0]["fields"]

    numero_prop = "PROP-2026-001"
    fichier = generer_proposition_pdf(lead, formation, numero_prop)

    print(f"✅ Proposition générée : {fichier}")


if __name__ == "__main__":
    main()