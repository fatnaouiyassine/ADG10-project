"""Diagnostic WhatsApp en simulation par defaut."""


def main():
    from whatsapp_sender import envoyer_whatsapp

    success = envoyer_whatsapp(
        numero="+212600000000",
        message="Message de test ADG-10.",
        dry_run=True,
    )
    print("Simulation reussie." if success else "Echec de la simulation.")


if __name__ == "__main__":
    main()
