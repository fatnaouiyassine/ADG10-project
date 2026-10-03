"""Envoi d'emails transactionnels via Gmail SMTP."""

from email.message import EmailMessage
from email.utils import formataddr, make_msgid
import mimetypes
import os
import smtplib

from config import require_configuration, settings


def envoyer_email(
    destinataire: str,
    objet: str,
    contenu: str,
    piece_jointe=None,
    contenu_html: str | None = None,
    dry_run: bool | None = None,
) -> bool:
    """Envoie un email ou le simule, avec validation stricte des pieces jointes."""
    effective_dry_run = settings.dry_run if dry_run is None else dry_run
    if not destinataire or "@" not in destinataire:
        print("Erreur lors de l'envoi de l'email : adresse destinataire invalide")
        return False

    files = piece_jointe if isinstance(piece_jointe, list) else [piece_jointe]
    files = [str(path) for path in files if path]
    missing_files = [path for path in files if not os.path.exists(path)]
    if missing_files:
        print(
            "Erreur lors de l'envoi de l'email : piece(s) jointe(s) introuvable(s) : "
            + ", ".join(missing_files)
        )
        return False

    if effective_dry_run:
        print(f"[SIMULATION] Email prepare pour {destinataire} : {objet}")
        return True

    try:
        require_configuration("gmail_address", "gmail_app_password")
        message = EmailMessage()
        message["From"] = formataddr((settings.company_name, settings.gmail_address))
        message["To"] = destinataire
        message["Subject"] = objet
        message["Message-ID"] = make_msgid(
            domain=settings.gmail_address.split("@")[-1]
        )
        if settings.sender_email:
            message["Reply-To"] = settings.sender_email
        message.set_content(contenu)
        if contenu_html:
            message.add_alternative(contenu_html, subtype="html")

        for path in files:
            mime_type, _ = mimetypes.guess_type(path)
            main_type, sub_type = (mime_type or "application/octet-stream").split("/", 1)
            with open(path, "rb") as attachment:
                message.add_attachment(
                    attachment.read(),
                    maintype=main_type,
                    subtype=sub_type,
                    filename=os.path.basename(path),
                )

        with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as server:
            server.starttls()
            server.login(settings.gmail_address, settings.gmail_app_password)
            server.send_message(message)
        return True
    except Exception as exc:
        print(f"Erreur lors de l'envoi de l'email : {exc}")
        return False
