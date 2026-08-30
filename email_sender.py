import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")


def envoyer_email(destinataire: str, objet: str, contenu: str) -> bool:
    """
    Envoie un email réel via Gmail SMTP (gratuit).
    Retourne True si l'envoi a réussi, False sinon.
    """
    try:
        msg = MIMEMultipart()
        msg["From"] = GMAIL_ADDRESS
        msg["To"] = destinataire
        msg["Subject"] = objet
        msg.attach(MIMEText(contenu, "plain"))

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
            server.send_message(msg)

        return True
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email : {e}")
        return False