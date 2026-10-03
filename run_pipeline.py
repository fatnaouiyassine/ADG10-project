"""Orchestrateur principal du cycle commercial ADG-10."""

import argparse
from datetime import date

from airtable_client import get_all_records, update_record
from closing import jours_depuis_proposition, message_closing_du_jour
from commercial_templates import email_proposition
from config import settings
from email_sender import envoyer_email
from nurturing import jours_ecoules, message_du_jour
from pipeline_utils import choisir_formation, numero_proposition
from proposal_generator import generer_proposition_pdf
from scoring import calculer_score, get_routing
from state_store import DispatchLedger, dispatch_key
from whatsapp_sender import envoyer_whatsapp


def _valid_email(value: str | None) -> bool:
    return bool(value and "@" in value and value != "Non renseigné")


def _send_message(message: dict, email: str | None, phone: str | None, dry_run: bool) -> bool:
    if message["canal"] == "Email":
        if not _valid_email(email):
            print("   [ATTENTION] Adresse email absente ou invalide.")
            return False
        return envoyer_email(
            email,
            message["objet"],
            message["contenu"],
            dry_run=dry_run,
        )
    if message["canal"] == "WhatsApp":
        if not phone:
            print("   [ATTENTION] Numero de telephone absent.")
            return False
        return envoyer_whatsapp(phone, message["contenu"], dry_run=dry_run)
    print(f"   [ACTION HUMAINE] {message['contenu']}")
    return False


def main(dry_run: bool | None = None) -> int:
    effective_dry_run = settings.dry_run if dry_run is None else dry_run
    mode = "SIMULATION" if effective_dry_run else "PRODUCTION"
    print(f"ADG-10 - Pipeline commercial - Mode {mode}")

    try:
        leads = get_all_records("Leads")
        formations = get_all_records("Formations")
    except Exception as exc:
        print(f"[ERREUR] Chargement Airtable impossible : {exc}")
        return 1

    if not formations:
        print("[ERREUR] Aucune formation trouvee.")
        return 1

    ledger = DispatchLedger()
    actions = 0
    skipped = 0
    errors = 0

    for record in leads:
        fields = record.get("fields", {})
        record_id = record.get("id", "")
        name = fields.get("nom_prenom", "Contact sans nom")
        email = fields.get("email")
        phone = fields.get("telephone")
        print(f"\n--- {name} ---")

        try:
            formation = choisir_formation(fields, formations)
            score = calculer_score(
                budget=fields.get("budget_declare", 0),
                urgence=fields.get("urgence", ""),
                decideur=fields.get("decideur", ""),
                taille=fields.get("taille_entreprise", ""),
                canal=fields.get("canal_entree", ""),
            )
            print(f"Score : {score}/10 - {get_routing(score)}")
            if not effective_dry_run:
                update_record("Leads", record_id, {"score": score})

            proposal_date = fields.get("date_envoi_proposition")
            if proposal_date:
                days = jours_depuis_proposition(proposal_date)
                message = message_closing_du_jour(days, fields, formation)
                if not message:
                    print(f"Closing J+{days} : aucune action prevue aujourd'hui.")
                    skipped += 1
                    continue
                if message["canal"] == "Appel":
                    print(f"Closing J+{days} - {message['objet']}")
                    print(f"   [ACTION HUMAINE] {message['contenu']}")
                    skipped += 1
                    continue

                event = dispatch_key(
                    record_id,
                    "closing",
                    days,
                    proposal_date,
                    message["canal"],
                )
                if ledger.has(event):
                    print("Closing : action deja envoyee, aucun doublon cree.")
                    skipped += 1
                    continue

                print(f"Closing J+{days} - {message['canal']} - {message['objet']}")
                success = _send_message(message, email, phone, effective_dry_run)
                if success:
                    actions += 1
                    if not effective_dry_run:
                        ledger.mark(
                            event,
                            {"lead": name, "sequence": "closing", "channel": message["canal"]},
                        )
                else:
                    errors += 1
                continue

            if score >= 8:
                reference = numero_proposition(record_id)
                event = dispatch_key(
                    record_id,
                    "proposition",
                    0,
                    reference,
                    "Email",
                )
                prior_dispatch = ledger.get(event)
                if prior_dispatch:
                    if not effective_dry_run:
                        update_record(
                            "Leads",
                            record_id,
                            {
                                "date_envoi_proposition": prior_dispatch.get(
                                    "sent_date", date.today().isoformat()
                                )
                            },
                        )
                        print(
                            "Proposition deja envoyee : etat Airtable reconcilie sans nouvel envoi."
                        )
                    else:
                        print("Proposition deja envoyee : aucun doublon ne serait cree.")
                    skipped += 1
                    continue

                pdf_path = generer_proposition_pdf(fields, formation, reference)
                print(f"Proposition generee : {pdf_path}")
                if not _valid_email(email):
                    print("[ATTENTION] Proposition non envoyee : adresse email invalide.")
                    errors += 1
                    continue

                subject, body = email_proposition(fields, formation, reference)
                success = envoyer_email(
                    email,
                    subject,
                    body,
                    piece_jointe=pdf_path,
                    dry_run=effective_dry_run,
                )
                if success:
                    actions += 1
                    if not effective_dry_run:
                        sent_date = date.today().isoformat()
                        ledger.mark(
                            event,
                            {
                                "lead": name,
                                "sequence": "proposition",
                                "channel": "Email",
                                "sent_date": sent_date,
                            },
                        )
                        update_record(
                            "Leads",
                            record_id,
                            {"date_envoi_proposition": sent_date},
                        )
                    print("Proposition preparee." if effective_dry_run else "Proposition envoyee.")
                else:
                    errors += 1
                continue

            contact_date = fields.get("date_premier_contact")
            if not contact_date:
                print("Nurturing ignore : date du premier contact absente.")
                skipped += 1
                continue

            days = jours_ecoules(contact_date)
            sequence = "qualification" if score >= 5 else "nurturing"
            message = message_du_jour(days, fields, formation, sequence=sequence)
            if not message:
                print(f"{sequence.capitalize()} J+{days} : aucune action prevue aujourd'hui.")
                skipped += 1
                continue

            event = dispatch_key(
                record_id,
                sequence,
                days,
                contact_date,
                message["canal"],
            )
            if ledger.has(event):
                print(f"{sequence.capitalize()} : action deja envoyee.")
                skipped += 1
                continue

            print(f"{sequence.capitalize()} J+{days} - {message['canal']} - {message['objet']}")
            success = _send_message(message, email, phone, effective_dry_run)
            if success:
                actions += 1
                if not effective_dry_run:
                    ledger.mark(
                        event,
                        {"lead": name, "sequence": sequence, "channel": message["canal"]},
                    )
            else:
                errors += 1
        except Exception as exc:
            errors += 1
            print(f"[ERREUR] Traitement interrompu pour ce lead : {exc}")

    print(
        f"\nBilan - actions : {actions} | sans action/doublons : {skipped} | erreurs : {errors}"
    )
    return 1 if errors else 0


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Pipeline commercial ADG-10")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="Simule sans envoyer ni modifier Airtable")
    mode.add_argument("--live", action="store_true", help="Autorise les envois et mises a jour reels")
    return parser.parse_args()


if __name__ == "__main__":
    arguments = _parse_args()
    requested_mode = False if arguments.live else True if arguments.dry_run else None
    raise SystemExit(main(dry_run=requested_mode))
