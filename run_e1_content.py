"""Generation controlee des contenus de formation."""

import argparse

from airtable_client import get_all_records, update_record
from config import settings
from generation_contenu import ContentGenerationError, generer_contenu_formation


def main(dry_run: bool | None = None) -> int:
    effective_dry_run = settings.dry_run if dry_run is None else dry_run
    try:
        formations = get_all_records("Formations")
    except Exception as exc:
        print(f"[ERREUR] Chargement Airtable impossible : {exc}")
        return 1

    print(f"{len(formations)} formation(s) - Mode {'SIMULATION' if effective_dry_run else 'PRODUCTION'}")
    errors = 0
    for record in formations:
        fields = record.get("fields", {})
        title = fields.get("titre", "Formation sans titre")
        if effective_dry_run:
            print(f"[SIMULATION] Contenu a regenerer : {title}")
            continue
        try:
            content = generer_contenu_formation(
                titre=title,
                duree=fields.get("duree", ""),
                prix_inter=fields.get("prix_inter", ""),
                public=fields.get("public", ""),
            )
            update_record("Formations", record["id"], content)
            print(f"[OK] {title} : contenu genere et sauvegarde.")
        except ContentGenerationError as exc:
            errors += 1
            print(f"[ERREUR] {title} : {exc}. Le contenu Airtable existant est conserve.")
    return 1 if errors else 0


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generation de contenu ADG-10")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--live", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    arguments = _parse_args()
    requested_mode = False if arguments.live else True if arguments.dry_run else None
    raise SystemExit(main(dry_run=requested_mode))
