"""Envoi WhatsApp Web avec mode simulation securise."""

from config import settings


def envoyer_whatsapp(
    numero: str,
    message: str,
    dry_run: bool | None = None,
) -> bool:
    effective_dry_run = settings.dry_run if dry_run is None else dry_run
    if not numero or not numero.startswith("+"):
        print("Erreur lors de l'envoi WhatsApp : numero international invalide")
        return False
    if effective_dry_run:
        print(f"[SIMULATION] WhatsApp prepare pour {numero}")
        return True

    try:
        import pywhatkit as kit

        kit.sendwhatmsg_instantly(
            phone_no=numero,
            message=message,
            wait_time=15,
            tab_close=True,
            close_time=3,
        )
        return True
    except Exception as exc:
        print(f"Erreur lors de l'envoi WhatsApp : {exc}")
        return False
