import os
from dotenv import load_dotenv
from pyairtable import Api

# Charge les variables du fichier .env
load_dotenv()

token = os.getenv("AIRTABLE_TOKEN")
base_id = os.getenv("AIRTABLE_BASE_ID")

print("Token trouvé :", token[:10] + "..." if token else "AUCUN TOKEN TROUVÉ")
print("Base ID trouvé :", base_id if base_id else "AUCUN BASE ID TROUVÉ")

# Connexion à Airtable
api = Api(token)
table = api.table(base_id, "Formations")

# Lire toutes les formations
formations = table.all()

print(f"\n{len(formations)} formations trouvées :\n")
for f in formations:
    print(f["fields"].get("titre", "Sans titre"))