from pyairtable import Api
from config import AIRTABLE_TOKEN, AIRTABLE_BASE_ID

_api = Api(AIRTABLE_TOKEN)


def get_table(table_name: str):
    """Retourne une référence à une table Airtable."""
    return _api.table(AIRTABLE_BASE_ID, table_name)


def get_all_records(table_name: str):
    """Récupère tous les enregistrements d'une table."""
    table = get_table(table_name)
    return table.all()


def update_record(table_name: str, record_id: str, fields: dict):
    """Met à jour un enregistrement."""
    table = get_table(table_name)
    return table.update(record_id, fields)