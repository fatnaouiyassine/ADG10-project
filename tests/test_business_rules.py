from pathlib import Path
import tempfile
import unittest

from closing import message_closing_du_jour
from commercial_templates import email_proposition
from contract_generator import calculer_prix_ht
from nurturing import message_du_jour
from pipeline_utils import (
    choisir_formation,
    numero_contrat_depuis_facture,
    numero_proposition,
    prochain_numero,
)
from scoring import calculer_score, get_routing
from state_store import DispatchLedger, dispatch_key


class ScoringTests(unittest.TestCase):
    def test_maximum_score_accepts_normalized_values(self):
        score = calculer_score("5 000", "< 1 mois", "PDG/DRH", "PME 10-250+", "Recommandation")
        self.assertEqual(score, 10.0)
        self.assertIn("Prioritaire", get_routing(score))

    def test_medium_score_uses_short_qualification(self):
        score = calculer_score(3000, "3-6 mois", "prescripteur", "TPE 1-9", "email direct")
        self.assertGreaterEqual(score, 5)
        self.assertIn("Qualification", get_routing(score))


class NumberingTests(unittest.TestCase):
    def test_invoice_number_uses_maximum_and_reservations(self):
        records = [
            {"fields": {"numero_facture": "FAC-2026-001"}},
            {"fields": {"numero_facture": "FAC-2026-003"}},
        ]
        self.assertEqual(
            prochain_numero("FAC-2026-", records, reserved={"FAC-2026-004"}),
            "FAC-2026-005",
        )

    def test_contract_reuses_invoice_suffix(self):
        self.assertEqual(
            numero_contrat_depuis_facture("FAC-2026-014"),
            "CONV-2026-014",
        )

    def test_proposal_reference_is_stable(self):
        self.assertEqual(
            numero_proposition("recABC", year=2026),
            numero_proposition("recABC", year=2026),
        )


class DataAndContentTests(unittest.TestCase):
    def test_formation_is_selected_by_linked_record_id(self):
        formations = [
            {"id": "recF1", "fields": {"titre": "Formation A"}},
            {"id": "recF2", "fields": {"titre": "Formation B"}},
        ]
        self.assertEqual(
            choisir_formation({"formation": ["recF2"]}, formations)["titre"],
            "Formation B",
        )

    def test_price_parser_handles_common_formats(self):
        self.assertEqual(calculer_prix_ht("2 500,00 MAD"), 2500.0)
        self.assertEqual(calculer_prix_ht("2500-3500"), 2500.0)

    def test_messages_are_personalized_without_unverified_claims(self):
        lead = {"nom_prenom": "Nadia"}
        formation = {"titre": "Management d'equipe"}
        nurturing = message_du_jour(0, lead, formation)
        closing = message_closing_du_jour(8, lead, formation)
        subject, proposal = email_proposition(lead, formation, "PROP-2026-ABC")
        self.assertIn("Nadia", nurturing["contenu"])
        self.assertIn("Management d'equipe", closing["contenu"])
        self.assertIn("PROP-2026-ABC", subject)
        self.assertNotIn("15-25", closing["contenu"] + proposal)


class LedgerTests(unittest.TestCase):
    def test_dispatch_is_marked_once(self):
        with tempfile.TemporaryDirectory() as directory:
            ledger = DispatchLedger(Path(directory) / "ledger.json")
            key = dispatch_key("rec1", "closing", 5, "2026-09-01", "WhatsApp")
            self.assertFalse(ledger.has(key))
            ledger.mark(key, {"lead": "Test"})
            self.assertTrue(ledger.has(key))
            self.assertEqual(len(ledger.recent()), 1)

    def test_dispatch_can_be_found_for_crm_reconciliation(self):
        with tempfile.TemporaryDirectory() as directory:
            ledger = DispatchLedger(Path(directory) / "ledger.json")
            ledger.mark(
                "invoice-event",
                {
                    "record_id": "rec1",
                    "sequence": "facturation",
                    "invoice_number": "FAC-2026-009",
                },
            )
            event = ledger.find(sequence="facturation", record_id="rec1")
            self.assertEqual(event["invoice_number"], "FAC-2026-009")

    def test_corrupted_ledger_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "ledger.json"
            path.write_text("{invalid", encoding="utf-8")
            with self.assertRaises(RuntimeError):
                DispatchLedger(path).recent()


if __name__ == "__main__":
    unittest.main()
