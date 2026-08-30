from email_sender import envoyer_email

resultat = envoyer_email(
    destinataire="yassinefa0102@gmail.com",  # mets ton vrai email ici pour recevoir le test
    objet="Test ADG-10",
    contenu="Ceci est un email de test envoyé depuis mon prototype Python."
)

if resultat:
    print("✅ Email envoyé avec succès !")
else:
    print("❌ Échec de l'envoi.")