from airtable_client import get_all_records
from pipeline_utils import choisir_formation, numero_proposition
from proposal_generator import generer_proposition_pdf


def main():
    leads = get_all_records("Leads")
    formations = get_all_records("Formations")

    if not leads or not formations:
        print("Pas assez de données pour tester.")
        return

    record = leads[0]
    lead = record["fields"]
    formation = choisir_formation(lead, formations)

    numero_prop = numero_proposition(record["id"])
    fichier = generer_proposition_pdf(lead, formation, numero_prop)

    print(f"✅ Proposition générée : {fichier}")


if __name__ == "__main__":
    main()
