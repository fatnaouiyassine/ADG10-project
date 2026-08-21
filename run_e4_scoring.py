from airtable_client import get_all_records, update_record
from scoring import calculer_score, get_routing


def main():
    leads = get_all_records("Leads")
    print(f"{len(leads)} leads trouvés.\n")

    for record in leads:
        fields = record["fields"]
        record_id = record["id"]

        score = calculer_score(
            budget=fields.get("budget_declare", 0),
            urgence=fields.get("urgence", ""),
            decideur=fields.get("decideur", ""),
            taille=fields.get("taille_entreprise", ""),
            canal=fields.get("canal_entree", "")
        )
        routing = get_routing(score)

        update_record("Leads", record_id, {"score": score})
        print(f"✅ {fields.get('nom_prenom')} → score {score}/10 → {routing}")


if __name__ == "__main__":
    main()