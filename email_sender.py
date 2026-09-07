import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
from dotenv import load_dotenv

load_dotenv()

GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")


def envoyer_email(destinataire: str, objet: str, contenu: str, piece_jointe=None) -> bool:
    """
    Envoie un email reel via Gmail SMTP.
    piece_jointe peut etre : None, un chemin (str), ou une liste de chemins.
    """
    try:
        msg = MIMEMultipart()
        msg["From"] = GMAIL_ADDRESS
        msg["To"] = destinataire
        msg["Subject"] = objet
        msg.attach(MIMEText(contenu, "plain"))

        fichiers = []
        if piece_jointe:
            fichiers = piece_jointe if isinstance(piece_jointe, list) else [piece_jointe]

        for chemin in fichiers:
            if chemin and os.path.exists(chemin):
                with open(chemin, "rb") as f:
                    piece = MIMEApplication(f.read(), _subtype="pdf")
                    piece.add_header(
                        "Content-Disposition", "attachment", filename=os.path.basename(chemin)
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