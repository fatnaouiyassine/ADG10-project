import os
from dotenv import load_dotenv

load_dotenv()

AIRTABLE_TOKEN = os.getenv("AIRTABLE_TOKEN")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")

if not AIRTABLE_TOKEN or not AIRTABLE_BASE_ID:
    raise ValueError("AIRTABLE_TOKEN ou AIRTABLE_BASE_ID manquant dans le fichier .env")