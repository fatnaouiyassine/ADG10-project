import pywhatkit as kit
import time


def envoyer_whatsapp(numero: str, message: str) -> bool:
    """
    Envoie un message WhatsApp reel via WhatsApp Web (pywhatkit).
    Le numero doit etre au format international, ex: +212612345678
    Retourne True si l'envoi a probablement reussi, False sinon.
    """
    try:
        kit.sendwhatmsg_instantly(
            phone_no=numero,
            message=message,
            wait_time=15,
            tab_close=True,
            close_time=3
        )
        return True
    except Exception as e:
        print(f"Erreur lors de l'envoi WhatsApp : {e}")
        return False