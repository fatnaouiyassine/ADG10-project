from airtable_client import get_all_records, update_record
from scoring import calculer_score, get_routing
from proposal_generator import generer_proposition_pdf

from airtable_client import get_all_records, update_record
from scoring import calculer_score, get_routing
from proposal_generator import generer_proposition_pdf


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

    
        score = calculer_score(
            budget=fields.get("budget_declare", 0),
            urgence=fields.get("urgence", ""),
            decideur=fields.get("decideur", ""),
            taille=fields.get("taille_entreprise", ""),
            canal=fields.get("canal_entree", "")
        )
        routing = get_routing(score)

        update_record("Leads", record_id, {"score": score})
        print(f"\n👤 {fields.get('nom_prenom')} → score {score}/10 → {routing}")

        if score >= 8:
            numero_prop = f"PROP-2026-{i+1:03d}"
            fichier = generer_proposition_pdf(fields, formation_par_defaut, numero_prop)
            print(f"   ✅ Score élevé → proposition générée automatiquement : {fichier}")
        else:
            print(f"   ⏳ Score en dessous de 8 → pas de proposition automatique pour l'instant")


if __name__ == "__main__":
    main()