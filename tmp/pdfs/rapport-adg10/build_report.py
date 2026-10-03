from pathlib import Path
from zipfile import ZipFile
from copy import deepcopy
import hashlib, json
from lxml import etree as E

ROOT = Path(r'C:\Users\yassine\Desktop\ADG10-project')
TMP = ROOT / 'tmp/pdfs/rapport-adg10'
REF = Path(r'C:\Users\yassine\Downloads\exemple de rapport.docx')
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': W}
def q(s): return '{%s}%s' % (W,s)
z = ZipFile(REF)
r = E.fromstring(z.read('word/document.xml'))
b = r.find('w:body', NS)
original = list(b)
source_table = deepcopy(b.find('w:tbl',NS))
ps = b.findall('w:p', NS)
inventory = {i.filename: {'size': i.file_size, 'sha256': hashlib.sha256(z.read(i)).hexdigest(), 'mode': 'editable' if i.filename == 'word/document.xml' else 'preserve-only'} for i in z.infolist()}
(TMP/'package-baseline.json').write_text(json.dumps(inventory, indent=2), encoding='utf-8')
sections = [deepcopy(e) for e in r.xpath('.//w:sectPr', namespaces=NS)]
roles = {'title':108, 'chapter':123, 'h':129, 'sub':131, 'p':133, 'front':42, 'toc':61}
evidence = {role: E.tostring(ps[idx], encoding='unicode') for role,idx in roles.items()}
(TMP/'role-evidence.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2),encoding='utf-8')

pages = []
def page(title, *items, chapter=False): pages.append((title,items,chapter))
def H(t): return ('h',t)
def S(t): return ('sub',t)
def P(t): return ('p',t)
def T(caption, rows): return ('table',(caption,rows))

page('Résumé',
 P("ADG-10 est un prototype d’agent commercial développé en Python pour ADBCENTER LOGISPLAN et Adaoui Business Centre. Il accompagne le traitement commercial des formations, depuis la préparation des contenus marketing jusqu’à la génération des propositions, des conventions et des factures. Le projet relie les données Airtable aux règles de qualification, aux modèles de communication et aux outils d’envoi."),
 P("La version examinée le 16 septembre 2026 comprend désormais une interface Streamlit, une configuration centralisée, des textes commerciaux personnalisés et une identité visuelle commune aux documents PDF. ReportLab remplace la génération précédente fondée sur fpdf2. Un journal local mémorise les actions envoyées afin de réduire les doublons et de faciliter la réconciliation avec le CRM après certaines erreurs."),
 P("Le périmètre implémenté couvre E1, E2 et E4 à E8. E2 prépare des variantes de contenu sans les publier ; E3, consacré à la publication sur les réseaux sociaux, reste absent. Le mode simulation est activé par défaut. Il autorise la lecture du CRM et la préparation locale des documents, mais empêche les envois et les modifications Airtable."),
 P("Les onze tests unitaires des règles métier ont réussi. Ces résultats ne constituent pas une validation des services externes ni une garantie de fonctionnement sans supervision. La mise en production nécessite encore la validation des données, des prix, de la fiscalité, des mentions contractuelles et des scénarios réels d’envoi."),
 P("Mots clés : intelligence artificielle, automatisation commerciale, Python, Airtable, Streamlit, qualification de prospects, ReportLab, CRM."))
page('Abstract',
 P("ADG-10 is a Python-based sales automation prototype developed for ADBCENTER LOGISPLAN and Adaoui Business Centre. It supports the commercial lifecycle of training services by combining Airtable records, lead qualification rules, personalized communication templates and PDF document generation."),
 P("The version reviewed on 16 September 2026 includes a Streamlit dashboard, centralized configuration, revised sales messages and a shared visual theme for proposals, training agreements and invoices. PDF generation now relies on ReportLab. A local dispatch ledger records sent actions to reduce repeated messages and support CRM reconciliation after selected failures."),
 P("The implemented scope includes E1, E2 and E4 through E8. E2 generates channel-specific content but does not publish it. E3, the social publishing stage, is not implemented. Simulation is enabled by default: CRM data may be read and local documents may be prepared, but messages are not sent and Airtable records are not updated."),
 P("Eleven business-rule unit tests passed. These checks do not demonstrate live integration success or unattended production readiness. Before customer use, the project requires controlled end-to-end tests, strict data validation, verified financial rules and review of legal company details and contractual wording."),
 P("Keywords: artificial intelligence, sales automation, Python, Airtable, Streamlit, lead scoring, ReportLab, CRM."))
page('Glossaire', T('Glossaire des termes utilisés',[
 ['Terme','Définition'],['ADG-10','Nom du prototype d’automatisation commerciale.'],['CRM','Outil de gestion de la relation client ; Airtable remplit ce rôle dans le prototype.'],['API','Interface permettant à un programme de communiquer avec un service externe.'],['LLM','Modèle de langage utilisé pour produire du contenu à partir d’un prompt.'],['Lead','Prospect représenté par une fiche commerciale.'],['Scoring','Calcul d’une note de qualification à partir de critères métier.'],['Nurturing','Séquence de contacts destinée à accompagner un prospect.'],['SMTP','Protocole employé pour transmettre les emails.'],['JSON','Format structuré des contenus générés et du journal local.'],['Dry-run','Mode simulation sans envoi de messages ni écriture CRM.'],['Réconciliation','Mise à jour du CRM à partir d’une action déjà enregistrée comme envoyée.'],['PDF','Format de livraison des documents commerciaux.'],['MAD','Dirham marocain.']]))
page('Sommaire',
 ('toc','Introduction générale\t1'),('toc','Chapitre 1  Contexte général du projet\t2'),
 ('toc','1.1  Organisme d’accueil et problématique\t3'),('toc','1.2  Démarche et évolution du projet\t4'),
 ('toc','Chapitre 2  Analyse et conception\t5'),('toc','2.1  Pipeline commercial\t6'),
 ('toc','2.2  Besoins et modèle de données\t7'),('toc','2.3  Scoring et séquences de relance\t8'),
 ('toc','Chapitre 3  Étude technique\t9'),('toc','3.1  Architecture et responsabilités\t10'),
 ('toc','3.2  Technologies et configuration\t11'),('toc','3.3  Sécurité et maîtrise des envois\t12'),
 ('toc','Chapitre 4  Réalisation et résultats\t13'),('toc','4.1  Tableau de bord\t14'),
 ('toc','4.2  Communications et documents commerciaux\t15'),('toc','4.3  Vérifications techniques\t16'),
 ('toc','4.4  Limites et plan de validation\t17'),('toc','Conclusion générale et perspectives\t18'),('toc','Références techniques\t19'))
page('Liste des tableaux',
 P('Tableau 1  Couverture du pipeline commercial ........................................ 6'),
 P('Tableau 2  Principales données métier ................................................... 7'),
 P('Tableau 3  Critères de qualification ........................................................ 8'),
 P('Tableau 4  Répartition des responsabilités techniques ........................... 10'),
 P('Tableau 5  Vérifications et portée des résultats ...................................... 16'),
 P('Tableau 6  Priorités avant la mise en production .................................... 17'),
 S('Repères de lecture'),
 P("Les numéros renvoient à la pagination du corps du rapport. Les pages préliminaires conservent la numérotation romaine du modèle. Les tableaux décrivent le périmètre actuel du prototype et ne présentent pas de résultats commerciaux mesurés."))
page('Introduction Générale',
 P("Le projet ADG-10 répond au besoin de structurer le suivi commercial des formations d’ADBCENTER LOGISPLAN. Les contenus de présentation, les critères de qualification, les relances et les documents de vente doivent rester cohérents tout au long du parcours d’un prospect. Leur préparation manuelle multiplie les tâches répétitives et rend le suivi des actions plus difficile."),
 P("Le prototype vise à automatiser une partie de ce travail, tout en conservant l’intervention humaine pour les décisions commerciales et les échanges qui l’exigent. L’intelligence artificielle intervient dans la rédaction des contenus ; les règles de qualification et de déclenchement reposent sur du code déterministe. Cette distinction permet d’expliquer le routage d’un lead sans dépendre d’une appréciation variable du modèle de langage."),
 P("La version actualisée apporte un tableau de bord utilisable depuis un navigateur, une meilleure présentation des propositions et des conventions, ainsi que des mécanismes de simulation et de journalisation. L’objectif de 100 clients signés par an, indiqué dans le cadrage du projet, demeure une cible commerciale. Aucun résultat présenté dans ce rapport ne démontre que cet objectif a été atteint."),
 P("Le rapport présente d’abord le contexte et la démarche de réalisation. Il décrit ensuite le pipeline, les données et les règles de qualification, puis l’architecture et les choix techniques. Le dernier chapitre expose les changements réalisés, les vérifications disponibles et les conditions à réunir avant une utilisation auprès de clients réels."),
 P("L’état technique décrit correspond à la version du projet examinée le 16 septembre 2026. Les tests métier sont séparés des essais d’intégration : un test local réussi ne prouve ni la réception d’un email, ni la délivrance d’un message WhatsApp, ni la conformité d’une facture."))
page('Chapitre 1  Contexte général du projet',
 S('Introduction'), P("Ce chapitre présente l’organisme d’accueil, la problématique commerciale et les objectifs du prototype. Il retrace également l’évolution de la première version vers une application pilotable depuis un tableau de bord, avec des documents commerciaux harmonisés et des protections supplémentaires contre les actions involontaires."),chapter=True)
page('1.1  Organisme d’accueil et problématique',
 S('Cadre du projet'),
 P("ADBCENTER LOGISPLAN et Adaoui Business Centre constituent le cadre métier présenté pour le projet. Le catalogue de formations et les fiches de prospects sont centralisés dans Airtable. ADG-10 exploite ces informations pour préparer les communications commerciales, prioriser les contacts et produire les documents associés à une vente."),
 S('Problématique'),
 P("Un prospect peut entrer par plusieurs canaux, présenter un budget incomplet ou ne pas être encore décisionnaire. Le suivi doit donc distinguer les contacts prioritaires de ceux qui nécessitent une qualification ou un accompagnement progressif. Une proposition doit ensuite être reliée à la formation choisie, puis suivie sans renvoyer plusieurs fois les mêmes documents."),
 P("La difficulté ne consiste pas uniquement à produire un texte ou un PDF. Elle porte aussi sur la fiabilité du déclenchement, la cohérence des données et la conservation de l’historique d’action. Un envoi réussi suivi d’un échec de mise à jour Airtable peut, par exemple, provoquer un doublon lors d’une nouvelle exécution si le système ne mémorise pas l’envoi."),
 S('Objectifs du prototype'),
 P("Le prototype fournit une base opérationnelle pour préparer du contenu, calculer les scores, organiser les relances, générer les propositions et préparer la contractualisation. Il doit aussi rendre ces actions compréhensibles pour l’utilisateur. Le dashboard et le mode simulation permettent de consulter les données et d’examiner les actions prévues avant toute exécution réelle."),
 P("Les gains de temps et l’amélioration du taux de conversion restent à mesurer sur un pilote. Ils ne sont pas déduits de la seule présence des fonctions dans le code."))
page('1.2  Démarche et évolution du projet',
 S('Approche progressive'),
 P("La réalisation s’appuie sur une séparation progressive des responsabilités. Les règles métier indépendantes des services externes ont été regroupées dans des modules testables. Les paramètres et les accès aux intégrations ont été centralisés. Les scripts restent les points d’entrée pour chaque étape du cycle commercial."),
 P("La première version reposait essentiellement sur des scripts et des documents PDF simples. La version actuelle ajoute une interface Streamlit, des modèles de communication partagés, un thème ReportLab et un journal anti-doublon. Cette évolution améliore la lisibilité du projet sans transformer le prototype en plateforme distribuée."),
 S('Contraintes techniques'),
 P("Airtable reste une dépendance externe pour la lecture et la mise à jour des fiches. La génération de contenu nécessite l’accès à Groq en mode réel. L’email repose sur SMTP, tandis que WhatsApp est piloté par WhatsApp Web. Ces choix réduisent la complexité initiale, mais imposent de vérifier les accès, les quotas, les erreurs réseau et les conditions d’utilisation applicables."),
 P("Le projet ne garantit pas un coût nul : les bibliothèques utilisées et les services connectés ont des conditions différentes. Les coûts et les limites des comptes devront être examinés lors du choix du mode de déploiement."),
 S('Organisation des changements'),
 P("Les modifications portent sur l’interface, les communications, la génération documentaire et la sécurité d’exécution. Le README décrit l’installation, les champs Airtable et les commandes disponibles. Les changements du code et les retraits de fichiers du suivi Git sont encore présents dans l’espace de travail ; leur présence ne signifie pas qu’une version de livraison a été commitée ou déployée."))
page('Chapitre 2  Analyse et conception',
 S('Introduction'), P("Ce chapitre présente la couverture réelle des huit étapes du cycle commercial. Il définit les besoins, les principaux enregistrements Airtable et les règles de scoring. Les séquences de relance sont décrites comme des actions déclenchées par l’exécution des scripts, et non comme un service permanent déjà déployé."),chapter=True)
page('2.1  Pipeline commercial',
 P("Le pipeline distingue la préparation marketing, le traitement des prospects et la phase documentaire. Les étapes ne disposent pas toutes du même niveau de réalisation."),
 T('Tableau 1  Couverture du pipeline commercial',[
 ['Étape','Fonction','État actuel'],['E1','Génération des pitchs, bénéfices et FAQ','Implémentée avec Groq ; simulation sans appel au modèle.'],['E2','Déclinaison des contenus par canal','Textes LinkedIn et WhatsApp préparés ; aucune publication.'],['E3','Publication sur les réseaux sociaux','Non implémentée.'],['E4','Qualification et routage','Score pondéré et orientation commerciale.'],['E5','Nurturing et qualification','Séquences email et WhatsApp selon les jours prévus.'],['E6','Proposition commerciale','Génération PDF et préparation ou envoi par email.'],['E7','Relances après proposition','WhatsApp, email et rappel d’intervention humaine.'],['E8','Convention et facture','Documents et email transactionnel pour les leads signés.']]),
 S('Orchestration'),
 P("run_pipeline.py coordonne E4 à E7. Les étapes E1 et E8 disposent de leurs propres commandes. Une erreur concernant un lead est traitée sans interrompre systématiquement les autres leads. La publication sociale et l’acquisition automatique de prospects ne sont pas assurées par ce pipeline."),
 P("Les mentions de délai, comme l’appel sous quatre heures, expriment une consigne de routage. Elles ne constituent pas la preuve qu’un appel est automatiquement réalisé ou qu’un engagement de délai est respecté."))
page('2.2  Besoins et modèle de données',
 S('Besoins fonctionnels'),
 P("L’utilisateur doit pouvoir consulter le catalogue et les prospects, comprendre la priorité d’un contact, préparer les documents et identifier les actions exécutées. Les scripts doivent conserver les contenus existants lorsqu’une génération échoue et empêcher l’attribution d’une facture si l’envoi documentaire échoue."),
 T('Tableau 2  Principales données métier',[
 ['Enregistrement','Champs principaux'],['Formation','titre, duree, public, prix_inter ; pitch_30_mots, pitch_100_mots, benefices, faq.'],['Formation  options','prix_ht, taux_tva, modalite, lieu, date_session, objectifs, methodes_pedagogiques.'],['Lead  identité','nom_prenom, entreprise, email, telephone, adresse.'],['Lead  qualification','budget_declare, urgence, decideur, taille_entreprise, canal_entree, score.'],['Lead  suivi','date_premier_contact, date_envoi_proposition, client_signe, numero_facture, formation.'],['Journal local','Identité du lead, séquence, jour, date d’ancrage, canal et métadonnées d’envoi.']]),
 S('Qualité des données'),
 P("Le lien entre un lead et une formation peut utiliser un identifiant Airtable ou un titre reconnu. En l’absence de lien explicite, le code conserve un comportement de compatibilité en choisissant la première formation. Ce choix doit être remplacé par une validation bloquante avant production, afin d’éviter une proposition portant sur la mauvaise formation."),
 P("La tolérance à certaines variations de texte facilite l’utilisation du prototype, mais ne remplace pas un schéma obligatoire. Les dates, contacts, tarifs et informations administratives doivent être contrôlés avant toute émission documentaire."))
page('2.3  Scoring et séquences de relance',
 P("Le score final est arrondi à une décimale et calculé sur dix : S = 0,30 × budget + 0,25 × urgence + 0,20 × décideur + 0,15 × taille + 0,10 × canal. Chaque critère reçoit une valeur de 0, 5 ou 10 selon les règles définies dans scoring.py."),
 T('Tableau 3  Critères de qualification',[
 ['Critère','Poids','Exemples de règles'],['Budget','30 %','Au moins 5 000 : 10 ; montant positif inférieur : 5 ; sinon : 0.'],['Urgence','25 %','Moins d’un mois : 10 ; 3-6 mois : 5 ; autres valeurs : 0.'],['Décideur','20 %','PDG ou DRH : 10 ; prescripteur : 5.'],['Taille','15 %','PME 10-250 : 10 ; TPE 1-9 : 5.'],['Canal','10 %','Recommandation : 10 ; email direct : 5.']]),
 S('Routage'),
 P("Un score supérieur ou égal à 8 déclenche une orientation prioritaire. Entre 5 inclus et 8 exclu, le prospect suit une qualification courte. En dessous de 5, il entre dans une séquence de nurturing. La normalisation traite les accents, la casse et les espaces ; une valeur inconnue peut toutefois recevoir zéro et dégrader le score."),
 S('Calendriers'),
 P("La qualification prévoit des contacts à J0, J3 et J7. Le nurturing prévoit J0, J3, J7, J14 et J21. Après la proposition, les relances sont prévues à J5 sur WhatsApp, J8 par email et J12 sous forme d’action humaine. Les jours sont calculés depuis la date d’ancrage concernée. Une exécution régulière reste nécessaire ; le prototype ne comporte pas de planificateur permanent déployé."))
page('Chapitre 3  Étude technique',
 S('Introduction'), P("L’architecture repose sur des modules Python spécialisés, des scripts d’orchestration et une interface Streamlit. Ce chapitre décrit les responsabilités, les bibliothèques et la configuration, puis les mécanismes qui limitent les envois involontaires et les répétitions. Il précise également les limites d’un stockage local face aux exécutions concurrentes."),chapter=True)
page('3.1  Architecture et responsabilités',
 P("ADG-10 est une application Python modulaire organisée à plat. Le tableau de bord lance les scripts dans des processus distincts. Les règles métier sont partagées entre ces points d’entrée, tandis que les adaptateurs assurent les communications avec les services externes. Il ne s’agit pas d’une architecture Angular/Spring ni d’un ensemble de microservices."),
 T('Tableau 4  Répartition des responsabilités techniques',[
 ['Couche','Modules et rôle'],['Présentation','app.py : interface Streamlit, indicateurs, filtres et commandes.'],['Orchestration','run_pipeline.py et run_e*.py : exécution des étapes commerciales.'],['Règles métier','scoring.py, nurturing.py, closing.py : score, messages et calendrier.'],['Documents et textes','commercial_templates.py, pdf_theme.py, proposal_generator.py, contract_generator.py.'],['Données et références','pipeline_utils.py : sélection de formation, prix et numérotation.'],['Intégrations','airtable_client.py, generation_contenu.py, email_sender.py, whatsapp_sender.py.'],['Configuration et état','config.py et state_store.py : paramètres, simulation et journal des envois.']]),
 S('Circulation des informations'),
 P("La lecture Airtable fournit le catalogue et les leads. Les règles sélectionnent le traitement applicable. Un document peut être produit localement, puis transmis en mode réel. Le journal enregistre l’action envoyée avant la mise à jour de suivi dans Airtable. Une nouvelle exécution peut ainsi retrouver certaines actions déjà réalisées et réconcilier le CRM plutôt que renvoyer le message."),
 P("Cette séparation améliore la testabilité. Elle laisse toutefois les transactions réparties entre un service distant, un fichier local et un canal d’envoi, sans transaction globale garantissant une exécution unique."))
page('3.2  Technologies et configuration',
 S('Socle technique'),
 P("Python porte l’ensemble du traitement métier. Streamlit fournit le dashboard et pandas prépare les données affichées. pyairtable assure l’accès au CRM ; Groq est utilisé pour générer les contenus ; EmailMessage et SMTP structurent les emails ; pywhatkit pilote WhatsApp Web. ReportLab produit les documents PDF avec des polices DejaVu intégrées au projet."),
 S('Configuration centralisée'),
 P("config.py regroupe les paramètres dans une structure Settings et lit le fichier .env depuis un chemin explicite. .env.example décrit les paramètres à renseigner sans contenir les secrets opérationnels. Les intégrations sont validées au moment où elles sont utilisées, ce qui évite de bloquer une commande indépendante pour un service inutile à son exécution."),
 P("Les informations d’identité de l’entreprise, de contact, de paiement et de signature sont paramétrables. Plusieurs champs administratifs et bancaires sont encore vides ou fondés sur des valeurs par défaut. Ils doivent être confirmés par l’entreprise avant diffusion des conventions et factures."),
 S('Contenu généré par IA'),
 P("Le prompt de génération demande les pitchs de 30 et 100 mots, les bénéfices et la FAQ dans un JSON structuré. Les quatre champs doivent être présents et non vides. Une erreur de génération provoque un échec contrôlé ; les contenus Airtable antérieurs ne sont pas remplacés par une réponse invalide."),
 P("En simulation, E1 annonce les générations prévues sans appeler Groq. En mode réel, la validation de structure doit être complétée par une relecture du fond : un JSON valide ne prouve pas l’exactitude commerciale des textes. Les dépendances de requirements.txt ne sont pas verrouillées par version, ce qui reste un risque de reproductibilité."))
page('3.3  Sécurité et maîtrise des envois',
 S('Simulation par défaut'),
 P("ADG10_DRY_RUN est actif par défaut. Les commandes acceptent --dry-run pour simuler et --live pour une exécution réelle volontaire. Dans le dashboard, la production exige un choix explicite et une confirmation. La simulation n’est pas un fonctionnement totalement hors ligne : elle peut lire Airtable et produire des fichiers PDF locaux."),
 S('Journal anti-doublon'),
 P("DispatchLedger mémorise les actions dans .runtime/dispatch_log.json. Les clés combinent le lead, la séquence, le jour, la date d’ancrage et le canal. Une écriture temporaire suivie d’un remplacement atomique réduit le risque d’un fichier partiellement écrit. Une corruption détectée empêche de poursuivre comme si aucun historique n’existait."),
 P("Pour la proposition et la contractualisation, l’historique peut être utilisé afin de remettre à jour Airtable après un envoi déjà enregistré. La numérotation des factures tient compte du maximum existant et des réservations de l’exécution. Les références des propositions sont fondées sur l’identifiant du lead ; elles ne dépendent plus de sa position dans une liste."),
 S('Limites de garantie'),
 P("Le journal local ne possède pas de verrou de concurrence. Deux processus ou deux machines peuvent décider d’envoyer la même action. Une interruption entre l’envoi externe et l’enregistrement local reste également une fenêtre de répétition. Le dispositif réduit certains doublons, sans garantir une délivrance exactement une fois."),
 S('Secrets et suivi Git'),
 P(".env, les journaux, les caches et les documents générés sont exclus du suivi. Les retraits du suivi Git sont préparés, mais pas encore commités. Les secrets ayant figuré dans d’anciens commits doivent être renouvelés ; l’exclusion actuelle ne les supprime pas de l’historique."))
page('Chapitre 4  Réalisation et résultats',
 S('Introduction'), P("Ce chapitre présente les améliorations visibles et les résultats des vérifications locales. Le dashboard, les emails et les documents commerciaux sont décrits à partir de leur réalisation actuelle. Les points restant à valider sont regroupés dans un plan de préparation à la production."),chapter=True)
page('4.1  Tableau de bord',
 S('Interface de pilotage'),
 P("app.py fournit une interface Streamlit avec une palette bleu marine et turquoise. Les indicateurs synthétisent les données commerciales. Les onglets donnent accès à la vue d’ensemble, aux leads, aux formations et à l’activité. Les filtres et les vues de priorité permettent de retrouver les prospects et de comprendre leur qualification."),
 P("L’interface présente également des graphiques et un journal d’exécution. Les données sont mises en cache pendant quinze secondes afin de limiter les lectures répétées. Cette mise en cache implique qu’une modification distante peut ne pas apparaître immédiatement sans actualisation."),
 S('Actions disponibles'),
 P("Quatre actions principales sont exposées : génération de contenu E1, calcul des scores E4, pipeline E4 à E7 et contractualisation E8. Les scripts sont lancés depuis le dossier du projet avec un chemin explicite. Le dashboard récupère la sortie standard, les erreurs et le code de retour. Le délai maximal d’une commande est de quinze minutes."),
 S('Accès au dashboard'),
 P("Depuis le dossier du projet, la commande .\\.venv\\Scripts\\python.exe -m streamlit run app.py démarre l’interface. Elle est ensuite consultable à l’adresse locale http://localhost:8501 tant que le serveur est actif. Le fichier .env doit contenir les paramètres nécessaires à la lecture Airtable."),
 P("Le dashboard constitue une interface de pilotage locale. Il ne dispose pas, dans cette version, d’un système applicatif de comptes et de rôles. Il ne doit donc pas être exposé publiquement sans protection adaptée. La représentation de certains statuts Airtable doit aussi être normalisée pour éviter d’interpréter une chaîne de caractères comme une valeur booléenne fiable."))
page('4.2  Communications et documents commerciaux',
 S('Emails et pitchs'),
 P("Les textes partagés sont regroupés dans commercial_templates.py. Ils personnalisent l’échange à partir du prospect, de l’entreprise et de la formation. Les messages de nurturing et de closing ont été réécrits pour préciser le contexte, proposer une prochaine action et éviter les promesses de retour sur investissement, de certification ou de remise non établies."),
 P("Le module d’email utilise EmailMessage, un nom d’expéditeur, une adresse de réponse et des pièces jointes vérifiées avant l’envoi. La connexion SMTP utilise STARTTLS. WhatsApp reste une automatisation de navigateur : le retour d’exécution ne constitue pas un accusé de réception du destinataire."),
 S('Proposition commerciale'),
 P("Le PDF de proposition présente la solution, les bénéfices attendus, les modalités, l’investissement et les prochaines étapes. Il comporte les coordonnées de contact, les conditions et un espace d’accord. La référence est stable pour un lead au sein d’une année. Le nom du fichier est sécurisé et le chemin de sortie est centralisé dans output/pdf."),
 S('Convention et facture'),
 P("La convention organise les parties, le périmètre, les objectifs, les engagements, les conditions financières, l’annulation, la confidentialité et les signatures. La facture reprend les parties, les dates, la désignation, les totaux et le paiement. Les trois documents partagent un thème ReportLab, des en-têtes, des pieds de page et une pagination cohérente."),
 P("E8 prépare la convention et la facture pour un lead signé. En mode réel, la facturation de suivi n’est enregistrée dans Airtable qu’après le succès de l’envoi. La qualité graphique des documents ne vaut pas validation juridique ou comptable ; les tarifs et les mentions doivent être approuvés avant leur émission."))
page('4.3  Vérifications techniques',
 P("Les vérifications locales portent sur les règles métier et la cohérence de l’environnement. Les tests unitaires ont été relancés le 16 septembre 2026 sans effectuer d’envois réels."),
 T('Tableau 5  Vérifications et portée des résultats',[
 ['Contrôle','Résultat','Portée'],['Tests unitaires','11 tests réussis','Scoring, sélection, prix, numérotation, messages et journal.'],['Syntaxe du projet','28 fichiers Python analysés','Absence d’erreur de syntaxe dans les fichiers propres au projet.'],['Dépendances','pip check sans conflit détecté','Cohérence des dépendances installées ; pas un audit de sécurité.'],['Documents commerciaux','Exemples PDF générés et examinés','Présentation vérifiée ; règles financières à valider.'],['Intégrations réelles','Non validées de bout en bout dans cet audit','Airtable, Groq, SMTP et WhatsApp exigent des essais contrôlés.']]),
 S('Scénarios couverts'),
 P("Les tests vérifient notamment la normalisation du score maximal et le routage intermédiaire, la sélection d’une formation par identifiant, les formats de prix usuels, les références stables des propositions, la réservation des numéros de facture et la réutilisation du suffixe pour la convention. Ils contrôlent également l’enregistrement d’une action, sa recherche pour réconciliation et le comportement face à un journal corrompu."),
 S('Interprétation'),
 P("Les résultats apportent une assurance sur des fonctions isolées. Ils ne couvrent pas toutes les erreurs réseau, les interruptions de processus ou les exécutions simultanées. Les scripts de test manuels sont désormais protégés pour éviter des actions au simple import, mais ils ne remplacent pas un protocole de recette avec des destinataires de test."))
page('4.4  Limites et plan de validation',
 T('Tableau 6  Priorités avant la mise en production',[
 ['Priorité','Action','Critère attendu'],['1','Valider l’identité de l’entreprise, les contrats et la fiscalité','Documents approuvés par les responsables compétents.'],['1','Rendre les données commerciales obligatoires','Blocage d’un dossier incomplet ou ambigu.'],['1','Renouveler les secrets historiques','Accès renouvelés et stratégie de traitement de l’historique définie.'],['2','Centraliser l’état et les réservations','Prévention des collisions entre processus et machines.'],['2','Réaliser une recette d’intégration','Envois de test vérifiés et erreurs CRM réconciliées.'],['3','Définir le déploiement et la publication E3','Hébergement protégé, cadence d’exécution et périmètre approuvés.']]),
 S('Règles financières à corriger'),
 P("Le parseur de prix retient le premier montant trouvé, y compris dans une fourchette. Une valeur invalide peut devenir zéro. La quantité de facture est fixée à un ; les calculs utilisent des nombres flottants. Le traitement actuel peut substituer 20 % à une TVA renseignée à zéro, et l’échéance reste calculée à trente jours. Ces comportements doivent être remplacés ou validés explicitement avant utilisation comptable."),
 S('Recette contrôlée'),
 P("Le pilote doit couvrir un lead complet, un lead incomplet, un client signé, un envoi refusé, un échec Airtable après envoi et une relance répétée. Il faut aussi vérifier l’exclusion des clients signés des relances commerciales et définir la politique applicable aux jours de contact manqués. La réception doit être contrôlée sur des boîtes et comptes de test, sans engager de vrais clients."))
page('Conclusion Générale et Perspectives',
 P("La version actualisée d’ADG-10 forme un prototype commercial plus cohérent et plus facile à piloter. Le tableau de bord centralise la consultation et l’exécution des étapes. Les modèles de communication donnent une structure commune aux échanges, tandis que les documents ReportLab présentent les propositions, conventions et factures dans une identité visuelle harmonisée."),
 P("La centralisation de la configuration, la simulation par défaut et le journal des envois améliorent la maîtrise des actions. La sélection des formations et la numérotation sont moins dépendantes de l’ordre des données. Les onze tests unitaires réussis constituent une base de non-régression pour les principales règles métier."),
 P("Le projet reste toutefois un prototype supervisé. E3 n’est pas réalisé, les intégrations n’ont pas été validées de bout en bout dans l’audit, et le stockage local ne garantit pas l’unicité des actions concurrentes. Les règles financières et les informations administratives nécessitent une validation préalable à l’émission de documents réels."),
 P("La prochaine étape recommandée est un pilote contrôlé. Il doit commencer par des données obligatoires et des documents approuvés, puis vérifier les envois et les scénarios d’échec sur des comptes de test. L’état des actions devra ensuite être centralisé si plusieurs utilisateurs ou processus exécutent le système."),
 P("Après cette validation, l’entreprise pourra décider du déploiement, de la fréquence d’exécution et de l’extension vers la publication sociale. Les gains de productivité et la conversion commerciale devront être mesurés pendant le pilote afin de comparer les résultats à l’objectif métier initial."))
page('Références techniques',
 P("Les références ci-dessous correspondent aux fichiers du projet décrivant l’état technique examiné. Elles permettent de retrouver les fonctions, les paramètres et les tests évoqués dans le rapport."),
 S('Présentation et points d’entrée'),
 P('README.md ; requirements.txt ; app.py ; run_pipeline.py ; run_e1_content.py ; run_e2_multichannel.py ; run_e4_scoring.py ; run_e8_contract.py.'),
 S('Règles métier et suivi'),
 P('scoring.py ; nurturing.py ; closing.py ; pipeline_utils.py ; state_store.py ; tests/test_business_rules.py.'),
 S('Intégrations et paramètres'),
 P('config.py ; .env.example ; airtable_client.py ; generation_contenu.py ; email_sender.py ; whatsapp_sender.py.'),
 S('Communications et documents'),
 P('commercial_templates.py ; pdf_theme.py ; proposal_generator.py ; contract_generator.py.'),
 S('Éléments de vérification'),
 P("Suite unittest de onze tests métier ; analyse syntaxique des vingt-huit fichiers Python du projet ; contrôle de cohérence des dépendances installées ; exemples locaux des propositions, conventions et factures. Aucun secret de configuration ni donnée personnelle réelle n’est reproduit dans ce rapport."))

def para(role,text):
    src=ps[roles[role]]
    p=E.Element(q('p'))
    pr=deepcopy(src.find('w:pPr',NS))
    if pr is not None:
        for el in list(pr):
            if el.tag in [q('numPr'),q('sectPr')]: pr.remove(el)
        p.append(pr)
    rr=E.SubElement(p,q('r'))
    rp=src.find('w:r/w:rPr',NS)
    if rp is not None: rr.append(deepcopy(rp))
    parts=text.split('\t')
    for i,t in enumerate(parts):
        if i: E.SubElement(rr,q('tab'))
        tt=E.SubElement(rr,q('t')); tt.set('{http://www.w3.org/XML/1998/namespace}space','preserve'); tt.text=t
    return p

def table(caption,rows):
    # Reuse the reference glossary's native table style, borders and cell rhythm.
    src=source_table
    tbl=deepcopy(src)
    for row in tbl.findall('w:tr',NS): tbl.remove(row)
    grid=tbl.find('w:tblGrid',NS)
    for x in list(grid):grid.remove(x)
    widths=([1800,3500,4600] if len(rows[0])==3 else [2400,7000])
    # Table retains the reference's 6.28-inch text span.
    widths=[int(x*9040/sum(widths)) for x in widths]
    for v in widths:E.SubElement(grid,q('gridCol')).set(q('w'),str(v))
    pr=tbl.find('w:tblPr',NS)
    tw=pr.find('w:tblW',NS)
    if tw is not None:tw.set(q('w'),'9040');tw.set(q('type'),'dxa')
    template=src.find('w:tr',NS)
    for ix,values in enumerate(rows):
        row=E.Element(q('tr'))
        if ix==0:
            trp=E.SubElement(row,q('trPr'));E.SubElement(trp,q('tblHeader'))
        for j,value in enumerate(values):
            cell=deepcopy(template.findall('w:tc',NS)[min(j,1)])
            for old in cell.findall('w:p',NS):cell.remove(old)
            cp=cell.find('w:tcPr',NS)
            cw=cp.find('w:tcW',NS)
            if cw is not None:cw.set(q('w'),str(widths[j]));cw.set(q('type'),'dxa')
            pp=deepcopy(template.findall('w:tc',NS)[min(j,1)].find('w:p',NS))
            ppr=deepcopy(pp.find('w:pPr',NS))
            pp.clear()
            if ppr is not None:pp.append(ppr)
            rr=E.SubElement(pp,q('r'))
            rp=E.SubElement(rr,q('rPr'))
            # Match the source table's Times New Roman typography.
            E.SubElement(rp,q('rFonts')).set(q('ascii'),'Times New Roman')
            rp.find(q('rFonts')).set(q('hAnsi'),'Times New Roman')
            E.SubElement(rp,q('sz')).set(q('val'),'22')
            if ix==0:E.SubElement(rp,q('b'))
            E.SubElement(rr,q('t')).text=value
            cell.append(pp);row.append(cell)
        tbl.append(row)
    return [para('sub',caption),tbl]

# The cover, dedication and acknowledgements are copied without a text or structure edit.
for e in list(b)[39:]:b.remove(e)
for idx,(title,items,chapter) in enumerate(pages):
    title_role='chapter' if chapter else ('h' if title[:1].isdigit() else 'title')
    b.append(para(title_role,title))
    if chapter:
        # The source chapter component uses vertical whitespace, retained here.
        first=b[-1];pr=first.find('w:pPr',NS)
        sp=pr.find('w:spacing',NS)
        if sp is None:sp=E.SubElement(pr,q('spacing'))
        sp.set(q('before'),'2800')
    for role,value in items:
        if role=='table':
            for e in table(*value):b.append(e)
        else:b.append(para('front' if idx<2 and role=='p' else role,value))
    # Reuse front-matter/body section components and exact original geometry.
    sect=deepcopy(sections[3 if idx<5 else 10])
    pn=sect.find('w:pgNumType',NS)
    if pn is not None:
        if idx==5:pn.set(q('start'),'1')
        else:pn.attrib.pop(q('start'),None)
    ty=sect.find('w:type',NS)
    if ty is not None:ty.set(q('val'),'nextPage')
    if idx==len(pages)-1:b.append(sect)
    else:
        p=E.SubElement(b,q('p'));pr=E.SubElement(p,q('pPr'));pr.append(sect)

out=TMP/'rapport_ADG10_actualise.docx'
with ZipFile(out,'w') as dest:
    for i in z.infolist():dest.writestr(deepcopy(i),E.tostring(r,xml_declaration=True,encoding='UTF-8',standalone=True) if i.filename=='word/document.xml' else z.read(i))
with ZipFile(out) as final:
    assert all(final.read(k)==z.read(k) for k in inventory if k!='word/document.xml')
print('Created',out,'planned pages',len(pages)+3)
print('Reference SHA256',hashlib.sha256(REF.read_bytes()).hexdigest())
