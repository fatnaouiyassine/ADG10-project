from pathlib import Path
from dataclasses import replace
import sys, subprocess
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
import config
A = Path(__file__).parent / 'assets'
config.settings = replace(config.settings, airtable_token='', airtable_base_id='', groq_api_key='', gmail_address='contact@example.com', gmail_app_password='', dry_run=True, company_name='ADBCENTER LOGISPLAN - DEMONSTRATION', company_legal_name='ADBCENTER LOGISPLAN - DEMONSTRATION', company_email='contact@example.com', company_address='Adresse fictive - Agadir', company_phone='', company_website='', company_rc='', company_ice='', company_if='', company_tp='', company_cnss='', company_bank='', company_rib='', signatory_name='Equipe pedagogique')
from proposal_generator import generer_proposition_pdf
from contract_generator import generer_contrat_pdf, generer_facture_pdf
lead = dict(nom_prenom='Contact Alpha', entreprise='Entreprise de demonstration', email='contact1@example.com', adresse='Adresse fictive - Agadir')
formation = dict(titre='Intelligence artificielle appliquee aux metiers', duree='2 jours', prix_ht=5000, prix_inter=5000, taux_tva=20, public='Cadres et equipes operationnelles', modalite='Presentiel', lieu='Agadir - lieu a confirmer', objectifs='Comprendre les usages de l’IA ; identifier un cas d’usage ; construire un plan d’action.', benefices='Gagner du temps sur les taches repetitives ; structurer les pratiques ; evaluer les limites.', pitch_100_mots='Une formation pratique pour identifier les usages pertinents de l’intelligence artificielle, experimenter des outils sur des cas professionnels et construire un plan d’action adapte aux contraintes de votre organisation. Le programme et les modalites seront confirmes ensemble avant validation.')
poppler = r'C:\Users\yassine\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdftoppm.exe'
for name, fun, ref in [('proposition', generer_proposition_pdf, 'PROP-2026-DEMO'), ('convention', generer_contrat_pdf, 'CONV-2026-DEMO'), ('facture', generer_facture_pdf, 'FAC-2026-DEMO')]:
    path = fun(lead, formation, ref, output_dir=A)
    subprocess.run([poppler, '-f', '1', '-l', '1', '-scale-to', '1800', '-png', path, str(A / name)], check=True)
    print(name, path)
