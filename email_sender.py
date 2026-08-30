import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
from dotenv import load_dotenv

load_dotenv()

GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")


def envoyer_email(destinataire: str, objet: str, contenu: str, piece_jointe: str = None) -> bool:
    """
    Envoie un email réel via Gmail SMTP (gratuit).
    Si piece_jointe est fourni (chemin vers un fichier), il est attaché à l'email.
    Retourne True si l'envoi a réussi, False sinon.
    """
    try:
        msg = MIMEMultipart()
        msg["From"] = GMAIL_ADDRESS
        msg["To"] = destinataire
        msg["Subject"] = objet
        msg.attach(MIMEText(contenu, "plain"))

        if piece_jointe and os.path.exists(piece_jointe):
            with open(piece_jointe, "rb") as f:
                piece = MIMEApplication(f.read(), _subtype="pdf")
                piece.add_header(
                    "Content-Disposition", "attachment", filename=os.path.basename(piece_jointe)
                )
                msg.attach(piece)

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
            server.send_message(msg)

        return True
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email : {e}")
        return False