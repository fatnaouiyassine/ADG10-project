"""Acces minimal et paresseux a Airtable."""

from functools import lru_cache

from pyairtable import Api

from config import require_configuration, settings


@lru_cache(maxsize=1)
def get_api() -> Api:
    require_configuration("airtable_token", "airtable_base_id")
    return Api(settings.airtable_token)


def get_table(table_name: str):
    """Retourne une reference a une table Airtable."""
    if not table_name or not table_name.strip():
        raise ValueError("Le nom de la table Airtable est obligatoire.")
    return get_api().table(settings.airtable_base_id, table_name.strip())


def get_all_records(table_name: str):
    """Recupere tous les enregistrements d'une table."""
    return get_table(table_name).all()


def update_record(table_name: str, record_id: str, fields: dict):
    """Met a jour un enregistrement Airtable."""
    if not record_id:
        raise ValueError("L'identifiant Airtable est obligatoire.")
    if not fields:
        return None
    return get_table(table_name).update(record_id, fields)
