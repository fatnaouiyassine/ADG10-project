"""Diagnostic email en simulation par defaut."""


def main():
    from email_sender import envoyer_email

    success = envoyer_email(
        destinataire="test@example.com",
        objet="Test ADG-10",
        contenu="Message de test ADG-10.",
        dry_run=True,
    )
    print("Simulation reussie." if success else "Echec de la simulation.")


if __name__ == "__main__":
    main()
