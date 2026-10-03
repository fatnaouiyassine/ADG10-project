# ADG-10 - Automatisation commerciale

ADG-10 centralise le cycle commercial d'ADBCENTER LOGISPLAN : contenu de
formation, qualification des leads, nurturing, propositions, relances,
conventions et factures.

## Fonctionnalites

| Etape | Fonction | Etat |
|---|---|---|
| E1 | Generation de pitchs, benefices et FAQ avec Groq | Operationnel |
| E2 | Declinaisons LinkedIn et WhatsApp | Operationnel |
| E3 | Publication sur les reseaux sociaux | Non implemente |
| E4 | Scoring et routage des leads | Operationnel |
| E5 | Nurturing et qualification personnalises | Operationnel |
| E6 | Proposition commerciale PDF et email | Operationnel |
| E7 | Relances email, WhatsApp et action humaine | Operationnel |
| E8 | Convention, facture et email transactionnel | Operationnel |

## Architecture

~~~text
app.py                         Interface Streamlit
run_pipeline.py                Orchestration E4 a E7
run_e1_content.py              Generation de contenu
run_e8_contract.py             Contractualisation et facturation

scoring.py                     Regles de qualification
nurturing.py / closing.py      Sequences commerciales
commercial_templates.py        Emails et textes partages
pipeline_utils.py              Association et numerotation
state_store.py                 Journal anti-doublon

airtable_client.py             Acces CRM
email_sender.py                Gmail SMTP
whatsapp_sender.py             WhatsApp Web
generation_contenu.py          Groq

pdf_theme.py                   Identite visuelle des PDF
proposal_generator.py          Proposition commerciale
contract_generator.py          Convention et facture
~~~

## Installation

1. Creer un environnement Python.
2. Installer les dependances :

   ~~~powershell
   pip install -r requirements.txt
   ~~~

3. Copier **.env.example** vers **.env** et renseigner les integrations ainsi
   que l'identite legale de l'entreprise.
4. Lancer l'interface :

   ~~~powershell
   streamlit run app.py
   ~~~

Le projet est en mode simulation par defaut. Dans ce mode, Airtable est lu mais
aucun message n'est envoye et aucune donnee CRM n'est modifiee. Le mode
Production doit etre choisi et confirme explicitement dans l'interface.

## Commandes

~~~powershell
python run_e1_content.py --dry-run
python run_e4_scoring.py --dry-run
python run_pipeline.py --dry-run
python run_e8_contract.py --dry-run
~~~

Pour une execution reelle et volontaire, remplacer **--dry-run** par **--live**.

## Modele Airtable

### Table Formations

Champs principaux :

- titre, duree, prix_inter, public
- pitch_30_mots, pitch_100_mots, benefices, faq
- champs optionnels : prix_ht, taux_tva, modalite, lieu, date_session,
  objectifs, methodes_pedagogiques

### Table Leads

Champs principaux :

- nom_prenom, entreprise, email, telephone, adresse
- budget_declare, urgence, decideur, taille_entreprise, canal_entree
- score, date_premier_contact, date_envoi_proposition
- client_signe, numero_facture
- liaison formation recommandee : formation contenant l'identifiant du record
  Airtable ou le titre exact
- champs administratifs optionnels : ice, if, rc, tp, cnss

Sans liaison explicite, le systeme utilise la premiere formation comme
comportement de compatibilite.

## Securite et fiabilite

- .env, les caches, journaux locaux et PDF generes sont ignores par Git.
- Les integrations sont initialisees uniquement lorsqu'elles sont utilisees.
- Le journal .runtime/dispatch_log.json evite les doubles envois locaux.
- Les factures ne sont marquees dans Airtable qu'apres un envoi reussi.
- Chaque lead est traite independamment afin qu'une erreur n'arrete pas toute
  la campagne.

Important : si un fichier .env a deja ete versionne, l'ajout au .gitignore ne
le supprime pas de l'historique. Il faut retirer ce fichier du suivi Git, purger
l'historique si le depot a ete partage et renouveler les identifiants.

## Tests

La suite metier ne contacte aucun service externe :

~~~powershell
python -m unittest discover -s tests -v
~~~

Les documents commerciaux et contractuels doivent etre adaptes aux informations
legales reelles de l'entreprise et valides par un professionnel competent avant
utilisation definitive.
