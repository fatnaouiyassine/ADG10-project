"""Generation et envoi fiables des conventions et factures."""

import argparse
from datetime import date

from airtable_client import get_all_records, update_record
from commercial_templates import email_documents_signature
from config import settings
from contract_generator import generer_contrat_pdf, generer_facture_pdf
from email_sender import envoyer_email
from pipeline_utils import (
    choisir_formation,
    numero_contrat_depuis_facture,
    prochain_numero,
)
from state_store import DispatchLedger, dispatch_key


def _is_signed(value) -> bool:
    if isinstance(value, bool):
        return value
    return str(value or "").strip().lower() in {"1", "true", "oui", "yes", "signe"}


def main(dry_run: bool | None = None) -> int:
    effective_dry_run = settings.dry_run if dry_run is None else dry_run
    print(
        "ADG-10 - Contrats et factures - Mode "
        + ("SIMULATION" if effective_dry_run else "PRODUCTION")
    )

    try:
        leads = get_all_records("Leads")
        formations = get_all_records("Formations")
    except Exception as exc:
        print(f"[ERREUR] Chargement Airtable impossible : {exc}")
        return 1

    if not formations:
        print("[ERREUR] Aucune formation trouvee.")
        return 1

    prefix = f"FAC-{date.today().year}-"
    ledger = DispatchLedger()
    try:
        reserved: set[str] = {
            event["invoice_number"]
            for event in ledger.recent(10000)
            if event.get("sequence") == "facturation" and event.get("invoice_number")
        }
    except Exception as exc:
        print(f"[ERREUR] Journal anti-doublon indisponible : {exc}")
        return 1
    generated = 0
    errors = 0

    for record in leads:
        fields = record.get("fields", {})
        record_id = record.get("id", "")
        name = fields.get("nom_prenom", "Contact sans nom")
        existing_invoice = fields.get("numero_facture")

        if not _is_signed(fields.get("client_signe")):
            continue
        if existing_invoice:
            print(f"{name} : deja facture ({existing_invoice}), ignore.")
            continue

        try:
            prior_dispatch = ledger.find(
                sequence="facturation",
                record_id=record_id,
            )
            if prior_dispatch:
                prior_invoice = prior_dispatch["invoice_number"]
                if not effective_dry_run:
                    update_record(
                        "Leads",
                        record_id,
                        {"numero_facture": prior_invoice},
                    )
                    print(
                        f"{name} : facture {prior_invoice} deja envoyee, "
                        "etat Airtable reconcilie sans nouvel envoi."
                    )
                else:
                    print(
                        f"{name} : facture {prior_invoice} deja envoyee, "
                        "aucun doublon ne serait cree."
                    )
                continue
        except Exception as exc:
            errors += 1
            print(f"[ERREUR] Reconciliation impossible pour {name} : {exc}")
            continue

        invoice_number = prochain_numero(
            prefix,
            leads,
            field_name="numero_facture",
            reserved=reserved,
        )
        reserved.add(invoice_number)
        contract_number = numero_contrat_depuis_facture(invoice_number)

        try:
            event = dispatch_key(
                record_id,
                "facturation",
                0,
                invoice_number,
                "Email",
            )
            if ledger.has(event):
                if not effective_dry_run:
                    update_record(
                        "Leads",
                        record_id,
                        {"numero_facture": invoice_number},
                    )
                    print(
                        f"{name} : facture deja envoyee, etat Airtable reconcilie sans nouvel envoi."
                    )
                else:
                    print(f"{name} : facture deja envoyee, aucun doublon ne serait cree.")
                continue

            formation = choisir_formation(fields, formations)
            contract_path = generer_contrat_pdf(fields, formation, contract_number)
            invoice_path = generer_facture_pdf(fields, formation, invoice_number)
            print(f"\n{name}")
            print(f"  Convention : {contract_path}")
            print(f"  Facture : {invoice_path}")

            email = fields.get("email")
            if not email or "@" not in email:
                print("  [ERREUR] Documents non envoyes : adresse email invalide.")
                errors += 1
                continue

            subject, body = email_documents_signature(fields, formation, invoice_number)
            success = envoyer_email(
                destinataire=email,
                objet=subject,
                contenu=body,
                piece_jointe=[contract_path, invoice_path],
                dry_run=effective_dry_run,
            )
            if not success:
                print("  [ERREUR] Echec de l'envoi. Le lead n'est pas marque comme facture.")
                errors += 1
                continue

            generated += 1
            if effective_dry_run:
                print("  Documents prepares en simulation. Airtable n'a pas ete modifie.")
            else:
                ledger.mark(
                    event,
                    {
                        "lead": name,
                        "sequence": "facturation",
                        "channel": "Email",
                        "record_id": record_id,
                        "invoice_number": invoice_number,
                    },
                )
                update_record(
                    "Leads",
                    record_id,
                    {"numero_facture": invoice_number},
                )
                print("  Documents envoyes et numero de facture enregistre.")
        except Exception as exc:
            errors += 1
            print(f"  [ERREUR] Traitement impossible pour {name} : {exc}")

    print(f"\nBilan - dossiers prepares : {generated} | erreurs : {errors}")
    return 1 if errors else 0


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Contrats et factures ADG-10")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--live", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    arguments = _parse_args()
    requested_mode = False if arguments.live else True if arguments.dry_run else None
    raise SystemExit(main(dry_run=requested_mode))
