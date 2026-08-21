from airtable_client import get_all_records, update_record
from generation_contenu import generer_contenu_formation


def main():
    formations = get_all_records("Formations")
    print(f"{len(formations)} formations trouvées.\n")

    for record in formations:
        fields = record["fields"]
        record_id = record["id"]

        contenu = generer_contenu_formation(
            titre=fields.get("titre", ""),
            duree=fields.get("duree", ""),
            prix_inter=fields.get("prix_inter", ""),
            public=fields.get("public", "")
        )

        update_record("Formations", record_id, contenu)
        print(f"✅ {fields.get('titre')} → contenu généré et sauvegardé")


if __name__ == "__main__":
    main()
    