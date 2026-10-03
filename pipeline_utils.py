"""Fonctions pures partagees par les orchestrateurs du pipeline."""

from datetime import date
import hashlib
import re
from typing import Iterable


def choisir_formation(lead_fields: dict, formations: list[dict]) -> dict:
    """Associe un lead a sa formation, avec repli sur la premiere formation."""
    if not formations:
        raise ValueError("Aucune formation disponible.")

    requested = (
        lead_fields.get("formation")
        or lead_fields.get("formation_souhaitee")
        or lead_fields.get("formation_id")
    )
    requested_values = requested if isinstance(requested, list) else [requested]
    normalized = {str(value).strip().lower() for value in requested_values if value}

    for record in formations:
        fields = record.get("fields", {})
        candidates = {
            str(record.get("id", "")).strip().lower(),
            str(fields.get("titre", "")).strip().lower(),
        }
        if normalized & candidates:
            return fields

    return formations[0].get("fields", {})


def numero_proposition(record_id: str, year: int | None = None) -> str:
    """Produit une reference stable quand aucun compteur CRM n'est disponible."""
    effective_year = year or date.today().year
    digest = hashlib.sha1(record_id.encode("utf-8")).hexdigest()[:6].upper()
    return f"PROP-{effective_year}-{digest}"


def prochain_numero(
    prefixe: str,
    records: Iterable[dict],
    field_name: str = "numero_facture",
    reserved: set[str] | None = None,
) -> str:
    """Retourne le numero suivant a partir du maximum, en evitant les reservations."""
    used = set(reserved or set())
    for record in records:
        value = str(record.get("fields", {}).get(field_name, "")).strip()
        if value.startswith(prefixe):
            used.add(value)

    suffixes = []
    pattern = re.compile(rf"^{re.escape(prefixe)}(\d+)$")
    for value in used:
        match = pattern.match(value)
        if match:
            suffixes.append(int(match.group(1)))

    candidate = max(suffixes, default=0) + 1
    while f"{prefixe}{candidate:03d}" in used:
        candidate += 1
    return f"{prefixe}{candidate:03d}"


def numero_contrat_depuis_facture(numero_facture: str) -> str:
    if numero_facture.startswith("FAC-"):
        return f"CONV-{numero_facture[4:]}"
    return numero_facture.replace("FAC", "CONV", 1)
