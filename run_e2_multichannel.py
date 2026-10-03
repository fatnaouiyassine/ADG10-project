from airtable_client import get_all_records
from multichannel_generator import generer_contenu_multicanal

def main():
    formations = get_all_records("Formations")

    for record in formations:
        fields = record["fields"]
        record_id = record["id"]

        contenu = generer_contenu_multicanal(fields)

        print(f"\n--- {fields.get('titre')} ---")
        print(contenu["post_linkedin"])
        print("\n---")
        print(contenu["message_whatsapp"])

if __name__ == "__main__":
    main()
