from whatsapp_sender import envoyer_whatsapp

resultat = envoyer_whatsapp(
    numero="+212682778238",  # mets ton propre numero pour tester
    message="Ceci est un test depuis mon prototype ADG-10."
)

print("Succes" if resultat else "Echec")