"""Render the actual dashboard with an isolated illustrative data source."""
from pathlib import Path
import sys, runpy
from dataclasses import replace
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT))
import config, airtable_client, state_store
config.settings=replace(config.settings, state_dir=Path(__file__).parent/'demo-state', output_dir=Path(__file__).parent/'assets', dry_run=True)
formations=[{'id':'recDemoFormation','fields':{'titre':'Intelligence artificielle appliquée aux métiers','duree':'2 jours','prix_inter':'5 000','public':'Cadres et équipes','pitch_100_mots':'Programme de démonstration pour le rapport.','benefices':'Structurer un usage métier\nÉvaluer les résultats\nPréparer un plan d’action'}}]
names=['Contact Alpha','Contact Bêta','Contact Gamma','Contact Delta','Contact Epsilon','Contact Zêta']
scores=[9.0,8.5,6.0,3.5,8.0,9.5]
leads=[]
for i,(name,score) in enumerate(zip(names,scores)):
    f={'nom_prenom':name,'entreprise':'Entreprise démo '+str(i+1),'email':'contact'+str(i+1)+'@example.com','score':score,'urgence':'< 1 mois' if score>=8 else '3-6 mois','decideur':'DRH' if score>=8 else 'Prescripteur'}
    if i==1:f['date_envoi_proposition']='2026-09-12'
    if i==4:f['client_signe']=True
    if i==5:f.update(client_signe=True,numero_facture='FAC-2026-DEMO')
    leads.append({'id':'recDemo'+str(i),'fields':f})
airtable_client.get_all_records=lambda table: leads if table=='Leads' else formations
airtable_client.update_record=lambda *a,**k: (_ for _ in ()).throw(RuntimeError('Lecture illustrative uniquement'))
runpy.run_path(str(ROOT/'app.py'),run_name='rapport_demo')
