"""Calcul controle du score des leads."""

import argparse

from airtable_client import get_all_records, update_record
from config import settings
from scoring import calculer_score, get_routing


def main(dry_run: bool | None = None) -> int:
    effective_dry_run = settings.dry_run if dry_run is None else dry_run
    try:
        leads = get_all_records("Leads")
    except Exception as exc:
        print(f"[ERREUR] Chargement Airtable impossible : {exc}")
        return 1

    errors = 0
    print(f"{len(leads)} lead(s) - Mode {'SIMULATION' if effective_dry_run else 'PRODUCTION'}")
    for record in leads:
        fields = record.get("fields", {})
        try:
            score = calculer_score(
                budget=fields.get("budget_declare", 0),
                urgence=fields.get("urgence", ""),
                decideur=fields.get("decideur", ""),
                taille=fields.get("taille_entreprise", ""),
                canal=fields.get("canal_entree", ""),
            )
            if not effective_dry_run:
                update_record("Leads", record["id"], {"score": score})
            print(
                f"{fields.get('nom_prenom', 'Contact sans nom')} : "
                f"{score}/10 - {get_routing(score)}"
            )
        except Exception as exc:
            errors += 1
            print(f"[ERREUR] Lead {record.get('id', '')} : {exc}")
    return 1 if errors else 0


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scoring ADG-10")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--live", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    arguments = _parse_args()
    requested_mode = False if arguments.live else True if arguments.dry_run else None
    raise SystemExit(main(dry_run=requested_mode))
