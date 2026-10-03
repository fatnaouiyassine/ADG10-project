import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import {pathToFileURL} from 'node:url';
import {Presentation,PresentationFile,FileBlob} from '@oai/artifact-tool';

const ROOT=process.cwd(), TMP=path.join(ROOT,'tmp/slides/adg10');
const SKILL='C:/Users/yassine/.codex/plugins/cache/openai-primary-runtime/presentations/26.909.11809/skills/presentations';
const PY='C:/Users/yassine/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe';
process.env.RUNTIME_NODE_MODULES='C:/Users/yassine/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const {finalizePresentation,applyPresentationChartFont}=await import(pathToFileURL(SKILL+'/container_tools/artifact_tool_utils.mjs'));
const sourceDir='C:/Users/yassine/Downloads/Re__Séances_d’encadrement';
const sourcePath=sourceDir+'/'+(await fs.readdir(sourceDir)).find(x=>x.normalize('NFC')==='Présentation_Stage_PFA.pptx');
const proto=(await PresentationFile.importPptx(await FileBlob.load(sourcePath))).toProto();
// Retain source backgrounds, theme, masters and branded ornaments. Replace only project content.
const keep=[['object 2','object 3','object 4','object 5','object 6','object 7','object 8','object 9','object 10','object 11','object 12'],['object 3','object 4','object 7','object 8','object 9','object 11','object 12','object 13','object 14'],['object 3','object 4','object 5'],['object 2','object 3','object 6','object 7'],['object 3','object 4','object 5'],['object 3','object 6','object 7'],['object 4','object 12','object 13'],['object 4'],['object 3','object 4','object 5'],['object 2'],[],['object 2'],[],['object 2'],[],['object 3','object 4','object 5'],['object 2'],['object 2'],['object 3','object 4','object 5'],['object 3','object 4'],['object 3','object 4'],['object 3','object 4','object 5']];
for(let i=0;i<proto.slides.length;i++){
 proto.slides[i].elements=proto.slides[i].elements.filter(e=>keep[i].includes(e.name));
 // Diagram-only source slides inherited the logo from content previously rasterized.
 if([10,12,14].includes(i)){
  const logo=structuredClone(proto.slides[9].elements.find(e=>e.name==='object 2'));logo.id='source-logo';proto.slides[i].elements.push(logo);
 }
}
const p=Presentation.load(proto), F='Times New Roman', GREEN='#0E933F', NAVY='#041C40';
const slide=n=>p.slides.items[n-1];
function text(n,s,x,y,w,h,size=42,bold=false,color=NAVY,align='left'){
 const a=slide(n).shapes.add({geometry:'textbox',name:s.slice(0,55),position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
 a.text=s;a.text.style={typeface:F,fontSize:size,bold,color,alignment:align,verticalAlignment:'middle',autoFit:'none',wrap:'square',insets:{left:0,right:0,top:0,bottom:0}};return a;
}
function title(n,s){return text(n,s,165,207,1380,105,52,true,NAVY,'center');}
function foot(n,s){text(n,s,165,944,1370,57,28,false,'#45544B','center');}
function page(n){text(n,String(n),850,1012,150,45,30,true,GREEN,'center');}
function para(n,items,{x=195,y=365,w=1290,size=42,gap=138}={}){items.forEach((v,i)=>text(n,v,x,y+i*gap,w,gap-15,size));}
function divider(n,titleText,sub){text(n,titleText,205,430,1290,120,56,true,NAVY,'center');text(n,sub,255,580,1190,130,38,false,NAVY,'center');page(n);}
function box(n,s,x,y,w,h,size=35,geom='rect'){
 const a=slide(n).shapes.add({geometry:geom,name:s.slice(0,55),position:{left:x,top:y,width:w,height:h},fill:'#FFFFFF',line:{fill:GREEN,width:2}});a.text=s;a.text.style={typeface:F,fontSize:size,color:NAVY,alignment:'center',verticalAlignment:'middle',autoFit:'none',insets:{left:12,right:12,top:9,bottom:9}};return a;
}
function link(n,a,b,from='right',to='left'){return slide(n).shapes.connect(a,b,{kind:'straight',fromSide:from,toSide:to,line:{fill:GREEN,width:3},tail:{type:'triangle',width:'sm',length:'sm'}});}
function table(n,rows,x,y,w,h,widths,size=34){
 const t=slide(n).tables.add({rows:rows.length,columns:rows[0].length,left:x,top:y,width:w,height:h,values:rows,columnWidths:widths});
 t.borders.assign({fill:'#B8CABE',width:1,style:'solid'});
 for(let r=0;r<rows.length;r++)for(let c=0;c<rows[0].length;c++){
  const a=t.getCell(r,c);a.fill=r===0?GREEN:r%2?'#F0F4F1':'#FFFFFF';a.text.style={typeface:F,fontSize:size,color:r===0?'#FFFFFF':NAVY,bold:r===0,verticalAlignment:'middle',insets:{left:15,right:15,top:8,bottom:8}};
 }
 return t;
}
async function pic(n,file,x,y,w,h,alt){slide(n).images.add({blob:new Uint8Array(await fs.readFile(path.join(ROOT,'tmp/pdfs/rapport-detaille/assets',file))),contentType:'image/png',alt,fit:'contain',position:{left:x,top:y,width:w,height:h}});}
function note(n,seconds,s,sources){slide(n).speakerNotes.textFrame.setText(`Durée indicative : ${seconds} secondes.\n\n${s}\n\nSources : ${sources}\nRéférence documentaire : Rapport de stage ADG-10, version du 17 septembre 2026.`);}

// 1. Cover: direct edits to the original title and attribution objects.
const cover=slide(1);
function editCover(name,value,rect,size,bold=false){const a=cover.shapes.items.find(x=>x.name===name);a.text=value;a.position=rect;a.text.style={typeface:F,fontSize:size,bold,color:NAVY,alignment:'center',verticalAlignment:'middle',insets:{left:24,right:24,top:12,bottom:12},autoFit:'none'};}
editCover('object 7','ADG-10\nAutomatisation du cycle commercial des formations',{left:108,top:394.84,width:1670,height:280.6},66);
editCover('object 9','Présenté par : Yassine FATNAOUI',{left:110,top:814,width:730,height:85},38);
editCover('object 12','Encadré par : Azouguigh El Houssaine',{left:1080,top:814,width:750,height:85},38);
editCover('object 10','2025-2026',{left:785,top:1000,width:290,height:60},36,true);
editCover('object 11','Soutenance du projet de fin d’année',{left:190,top:245,width:1510,height:100},60,true);
note(1,25,'Bonjour, je suis Yassine Fatnaoui. Je vous présente ADG-10, un projet consacré à l’automatisation du parcours commercial des formations. L’objectif est d’aider une équipe à qualifier ses prospects, préparer ses offres et suivre ses dossiers, tout en conservant la validation humaine.','Rapport, couverture et introduction générale.');

// 2. Preserve the photograph and five green markers from the source plan.
text(2,'Plan',310,218,750,105,70);
['Introduction','Contexte général du projet','Étude conceptuelle de la solution','Réalisation et mise en œuvre','Conclusion et perspectives'].forEach((s,i)=>text(2,s,383,[359,466,559,670,763][i],815,78,40));
note(2,20,'La présentation suit cinq parties. Après le contexte et les besoins, je présenterai le fonctionnement du système, puis ses choix techniques et une démonstration. Je terminerai par les résultats et les limites à traiter.','Structure du modèle de présentation fourni.');
divider(3,'INTRODUCTION','Comment assurer un suivi cohérent\ndu premier contact aux documents commerciaux ?');
note(3,15,'La question de départ est simple : comment assurer la continuité du suivi lorsqu’un dossier traverse plusieurs étapes et plusieurs outils ?','Rapport, introduction et problématique.');
title(4,'Organisme d’accueil et besoin métier');
slide(4).shapes.items.find(x=>x.name==='object 3').position={left:155,top:330,width:1387,height:615};
para(4,['ADBCENTER LOGISPLAN, dans l’environnement\nAdaoui Business Centre à Agadir.','Activité : formation et accompagnement professionnel\npour les salariés, les cadres et les entreprises.','Besoin : retrouver les informations du prospect et\npréparer la prochaine action sans refaire tout le dossier.'],{y:335,size:43,gap:183});page(4);
note(4,45,'Le contexte métier est celui de la commercialisation de formations. Un catalogue rassemble les titres, les publics, les durées et les tarifs. L’équipe doit ensuite faire correspondre une offre à un besoin réel. Le dossier commercial évolue au fil des échanges, et la perte d’une information peut affecter les relances ou les documents. Le projet porte sur cette continuité. La description de l’organisme reprend le cadrage fourni, sans inventer de données sur ses effectifs ou ses résultats.','Rapport, sections 1.1 et 1.2.');
divider(5,'CONTEXTE GÉNÉRAL DU PROJET','Des tâches répétitives à structurer\net des décisions commerciales à conserver');
note(5,10,'Le projet doit automatiser les opérations répétitives tout en laissant les décisions et la négociation au commercial.','Rapport, section 1.2.');
title(6,'Problématique');
para(6,['Des informations réparties entre le CRM,\nles messages et les fichiers.','Des relances difficiles à suivre et un risque\nde renvoyer une action déjà effectuée.','Comment fiabiliser le parcours sans perdre\nla personnalisation de la relation commerciale ?'],{y:385,size:45,gap:164});page(6);
note(6,45,'Le problème ne se résume pas à envoyer plus de messages. Il faut savoir quel prospect contacter, quelle formation proposer et quelle action a déjà été réalisée. Une interruption entre l’envoi d’un message et la mise à jour du CRM peut provoquer un doublon. La solution doit donc coordonner le contenu et les états du dossier. Le prototype apporte une première réponse, avec des limites que je préciserai.','Rapport, sections 1.2.3 et 3.2.2.');
title(7,'Objectifs et périmètre');
para(7,['Centraliser les formations et les prospects dans Airtable.','Prioriser les leads avec un score explicable.','Préparer des messages et des documents cohérents.','Piloter les traitements depuis un tableau de bord.'],{y:369,size:42,gap:120});foot(7,'La validation commerciale, la signature et le paiement restent hors automatisation complète.');page(7);
note(7,40,'Les objectifs sont opérationnels. Airtable sert de référentiel, les règles de scoring déterminent une priorité, et les modèles partagés harmonisent les communications. Le dashboard permet de consulter les données et de lancer les scripts. Le périmètre ne comprend pas une signature électronique ni un suivi automatique des paiements. Le nom d’agent commercial désigne ici un prototype supervisé, pas un système autonome de bout en bout.','README.md, app.py, run_pipeline.py et run_e8_contract.py.');
title(8,'Conduite du projet');
table(8,[['Phase','Travaux','Livrable'],['Cadrage','Parcours commercial et besoins','Périmètre E1 à E8'],['Conception','Données, règles et interactions','Modèles et scénarios'],['Réalisation','Scripts, documents et interface','Prototype intégré'],['Validation','Tests locaux et démonstration','Résultats et limites']],165,345,1390,470,[285,575,530],36);
foot(8,'Démarche itérative, avec validation des données et des fonctions à chaque phase.');page(8);
note(8,35,'J’ai organisé la présentation du travail par phases. Le cadrage précède la conception des données et des règles, puis les modules sont intégrés progressivement. Les vérifications servent à identifier les limites et à ajuster la solution. La démarche s’inspire d’un fonctionnement itératif. Je ne présente pas un historique de réunions ou un calendrier précis qui ne serait pas documenté.','Rapport, section 1.3.');
divider(9,'ÉTUDE CONCEPTUELLE DE LA SOLUTION','Le parcours commercial, les acteurs\net la circulation des données');
note(9,10,'La conception traduit les besoins métier en étapes, en données et en interactions entre les composants.','Rapport, chapitre 2.');
title(10,'Le parcours ADG-10');
table(10,[['Étape','Fonction','État dans le prototype'],['E1 / E2','Contenu IA et textes LinkedIn / WhatsApp','Génération disponible'],['E3','Publication sociale','À développer'],['E4 / E5','Scoring et entretien du contact','Règles et séquences disponibles'],['E6 / E7','Proposition et relances de closing','PDF, e-mail et jalons disponibles'],['E8','Convention et facture','Génération et envoi disponibles']],165,340,1390,525,[240,635,515],34);
foot(10,'Les scripts doivent s’exécuter aux échéances prévues. Les réponses du prospect nécessitent un suivi humain.');page(10);
note(10,55,'Le pipeline se décompose en huit étapes. E1 génère les contenus à partir du catalogue. E2 les décline pour certains canaux, mais E3 ne publie pas automatiquement. E4 qualifie les prospects, puis E5 entretient le contact. E6 prépare la proposition et E7 organise le suivi. Enfin, E8 produit la convention et la facture pour les dossiers marqués signés. Le pipeline principal relie surtout E4 à E7. E1 et E8 disposent de commandes séparées.','run_e1_content.py, run_e2_multichannel.py, run_pipeline.py, run_e8_contract.py.');
title(11,'Cas d’utilisation');
const actor=box(11,'Commercial',155,495,275,130,42);
const uses=[box(11,'Consulter et filtrer les prospects',570,335,780,110,38,'ellipse'),box(11,'Choisir et lancer un traitement',570,495,780,110,38,'ellipse'),box(11,'Vérifier les documents et le résultat',570,655,780,110,38,'ellipse')];
uses.forEach(a=>link(11,actor,a));
text(11,'Administrateur : configuration et contrôle des accès',230,840,1290,65,36,false,NAVY,'center');foot(11,'Rôles métier représentés. Le prototype ne dispose pas encore de comptes applicatifs distincts.');page(11);
note(11,40,'Le principal utilisateur est le commercial. Il consulte les prospects, choisit le mode d’exécution, lance une commande et contrôle son résultat. La configuration relève d’un rôle d’administration. Ces rôles décrivent les responsabilités du processus, mais ils ne correspondent pas encore à une gestion d’utilisateurs dans le dashboard. Les services techniques comme Airtable et Groq agissent en support.','app.py, config.py. Rapport, sections 2.1.3 et 2.2.');
title(12,'Modèle de données');
const formation=box(12,'Formation\nTitre, durée, public\nTarif et contenus',175,360,535,230,42);
const lead=box(12,'Lead\nContact, entreprise, score\nStatut et dates de suivi',945,360,615,230,42);
link(12,formation,lead);text(12,'1 formation\nplusieurs leads',718,347,220,110,31,false,NAVY,'center');
const docs=box(12,'Documents PDF\nProposition, convention, facture',175,710,610,160,38);
const log=box(12,'Journal local JSON\nAction, canal et date d’envoi',945,710,615,160,38);
link(12,lead,log,'bottom','top');link(12,formation,docs,'bottom','top');
foot(12,'Modèle conceptuel. Airtable conserve les fiches métier, le poste conserve les PDF et le journal.');page(12);
note(12,45,'Le modèle repose sur les formations et les leads. Un lead doit être rattaché à la bonne formation pour obtenir une offre cohérente. Les documents restent des fichiers locaux et le journal mémorise les actions envoyées. Le schéma est conceptuel : le code manipule des dictionnaires Airtable, sans ORM ni classes persistées correspondantes. Aujourd’hui, le repli sur la première formation en cas de lien invalide constitue une limite importante à supprimer avant exploitation.','airtable_client.py, pipeline_utils.py, state_store.py.');
title(13,'Scoring et routage des prospects');
text(13,'Pondération des critères (%)',200,310,720,55,30,false,NAVY,'center');
const chart=slide(13).charts.add('bar',{position:{left:145,top:350,width:810,height:495},categories:['Budget','Urgence','Décideur','Taille','Canal'],series:[{name:'Poids dans le score (%)',values:[30,25,20,15,10],fill:GREEN}],barOptions:{direction:'bar',grouping:'clustered',gapWidth:65},hasLegend:false,xAxis:{min:0,max:35,numberFormatCode:'0" %"',textStyle:{typeface:F,fontSize:26},majorGridlines:{fill:'#DDDDDD',width:1}},yAxis:{textStyle:{typeface:F,fontSize:32}},dataLabels:{showValue:true,position:'outEnd',textStyle:{typeface:F,fontSize:30}},chartFill:'#FFFFFF'});
applyPresentationChartFont(chart,{fontFamily:F});
text(13,'Score ≥ 8 : priorité commerciale\n\n5 ≤ score < 8 : qualification\n\nScore < 5 : nurturing',1030,365,600,330,40);
text(13,'Exemple fictif : 9,5 / 10\nBudget 6 000 MAD, besoin urgent, DRH, PME, e-mail direct.',1030,720,590,160,35);
foot(13,'Le score exprime une priorité de traitement. Il ne mesure pas une probabilité de vente.');page(13);
note(13,65,'Le scoring reste déterministe et explicable. Il combine cinq sous-notes sur dix avec les pondérations affichées. Le budget et l’urgence pèsent le plus. Les valeurs sont normalisées, puis le résultat est arrondi à une décimale. Dans l’exemple fictif, les contributions donnent 3 plus 2,5 plus 2 plus 1,5 plus 0,5, soit 9,5. Le lead passe en priorité. Un score intermédiaire entre dans une qualification courte, et les scores plus faibles dans une séquence de nurturing. Ces seuils sont des règles du prototype, pas des résultats statistiques de conversion.','scoring.py, tests/test_business_rules.py.');
title(14,'Séquence d’envoi d’une proposition');
const labels=['Script E6','Airtable','Journal local','PDF / SMTP']; const xs=[270,665,1060,1455];
const heads=labels.map((s,i)=>box(14,s,xs[i]-145,340,290,78,37));
// Native sequence diagram: lifelines and horizontally labelled message connectors.
const points=xs.map((x,i)=>{const bottom=box(14,'',x-1,910,2,2,1);slide(14).shapes.connect(heads[i],bottom,{kind:'straight',fromSide:'bottom',toSide:'top',line:{fill:'#A3B4A8',width:2,style:'dashed'}});return bottom;});
const actions=[[0,1,'1. Lire les données'],[0,2,'2. Vérifier un éventuel envoi antérieur'],[0,3,'3. Générer et envoyer la proposition'],[0,2,'4. Enregistrer le succès d’envoi'],[0,1,'5. Mettre à jour le CRM']];
actions.forEach(([a,b,s],i)=>{const y=478+i*88;const aa=box(14,'',xs[a]-1,y,2,2,1),bb=box(14,'',xs[b]-1,y,2,2,1);link(14,aa,bb);text(14,s,xs[a]+16,y-42,xs[b]-xs[a]-26,40,29);});
foot(14,'Après un échec CRM : le journal permet de réconcilier certains dossiers sans renvoyer le message.');page(14);
note(14,60,'Le scénario montre l’ordre des opérations. Le programme lit les données, vérifie le journal, prépare le PDF puis appelle la messagerie. Il enregistre le succès avant de mettre à jour le CRM. Si l’écriture CRM échoue, la reprise peut retrouver l’action et réconcilier le dossier. Cette protection réduit certains doublons. Elle ne garantit pas une exécution exactement une fois : une interruption entre l’envoi et l’écriture du journal reste possible, et le fichier JSON ne verrouille pas les exécutions simultanées.','run_pipeline.py, run_e6_proposal.py, state_store.py.');
title(15,'Architecture technique');
const ui=box(15,'Interface Streamlit\nConsultation et lancement des commandes',435,333,875,112,42);
const core=box(15,'Scripts Python et règles métier\nScoring, séquences et génération documentaire',435,517,875,125,42);link(15,ui,core,'bottom','top');
const services=[box(15,'Airtable et Groq\nCRM et contenus IA',145,765,450,125,36),box(15,'SMTP et WhatsApp\nCommunication',655,765,450,125,36),box(15,'ReportLab et JSON\nPDF et état local',1165,765,450,125,36)];services.forEach(a=>link(15,core,a,'bottom','top'));
foot(15,'Configuration centralisée et simulation par défaut. Architecture modulaire sur un poste local.');page(15);
note(15,55,'L’interface lit les données et déclenche les commandes dans des processus distincts. Le cœur métier applique les règles de score et construit les séquences. Les adaptateurs relient le programme aux services externes, tandis que ReportLab produit les PDF. La configuration est centralisée. Cette séparation facilite les tests locaux et la lecture du code. Le choix reste adapté à un prototype supervisé sur un poste. Une utilisation multi-utilisateur demande un service d’exécution, une base transactionnelle et une protection des accès.','app.py, config.py, run_pipeline.py, email_sender.py, whatsapp_sender.py, pdf_theme.py.');
divider(16,'RÉALISATION ET MISE EN ŒUVRE','Les fonctions développées\net leurs résultats visibles');
note(16,10,'Je passe maintenant aux choix de réalisation et aux résultats concrets du projet.','Rapport, chapitre 4.');
title(17,'Choix techniques');
table(17,[['Technologie','Rôle dans ADG-10','Justification'],['Python','Scripts et règles métier','Modules lisibles et testables'],['Airtable','Catalogue et prospects','Données accessibles à l’équipe'],['Groq','Génération des contenus','Réponse JSON contrôlée'],['Streamlit','Interface de pilotage','Dashboard directement en Python'],['ReportLab','Offres, conventions et factures','Thème documentaire partagé']],165,340,1390,540,[280,555,555],35);foot(17,'SMTP gère l’e-mail. WhatsApp repose sur l’automatisation du navigateur avec PyWhatKit.');page(17);
note(17,45,'Les technologies répondent à des responsabilités précises. Python porte les fonctions métier, Airtable le référentiel, et Groq la génération. Les quatre champs de contenu attendus sont contrôlés, même si la validation doit encore devenir plus stricte. Streamlit permet de regrouper les commandes sans développer un frontend séparé. ReportLab remplace l’ancienne génération documentaire. WhatsApp dépend d’une session navigateur disponible et ne fournit pas une preuve de réception.','requirements.txt, generation_contenu.py, app.py, pdf_theme.py et adaptateurs d’envoi.');
title(18,'Démonstration du tableau de bord');
await pic(18,'dashboard.png',150,328,1040,585,'Dashboard ADG-10 avec données fictives');
text(18,'1. Consulter les indicateurs\n\n2. Rechercher un prospect\n\n3. Choisir la simulation\n\n4. Lancer et vérifier',1235,354,435,492,38);
foot(18,'Capture de l’application réelle avec six prospects fictifs. Aucun envoi réel dans cette démonstration.');page(18);
note(18,80,'La démonstration suit un parcours court. Je présente les indicateurs : nombre de leads, score moyen, priorités et clients signés. Je montre ensuite la vue Leads, la recherche et le filtrage, puis je reviens aux commandes. Le mode simulation est sélectionné par défaut. Le passage en mode réel nécessite une confirmation. Les quatre onglets donnent accès à la vue d’ensemble, aux leads, aux formations et à l’activité. Dans la capture, les six contacts sont fictifs, le score moyen est 7,4 et quatre scores atteignent huit. Les mentions de configuration attestent la présence de paramètres, pas la réussite d’un appel externe. Si la démonstration en direct est indisponible, cette capture permet de présenter les mêmes étapes sans exposer de données réelles.','app.py. Capture locale dashboard.png, données de démonstration.');
// Reuse a content layout for the document slide, retaining the template's frame and logo.
title(19,'Documents et communications');
await pic(19,'proposition-1.png',150,322,450,600,'Proposition commerciale de démonstration');
await pic(19,'convention-1.png',675,322,450,600,'Convention de démonstration');
await pic(19,'facture-1.png',1200,322,450,600,'Facture de démonstration');
text(19,'Proposition',165,893,430,60,36,true,NAVY,'center');text(19,'Convention',685,893,430,60,36,true,NAVY,'center');text(19,'Facture',1210,893,430,60,36,true,NAVY,'center');
foot(19,'Exemples fictifs. L’équipe doit valider les données commerciales, contractuelles et fiscales avant émission.');page(19);
note(19,65,'La version actuelle produit trois documents avec un thème commun. La proposition reprend la formation, ses bénéfices, sa validité et les informations du prospect. La convention structure les engagements, les conditions et les signatures. La facture utilise une référence annuelle et affiche les montants. Les messages associent un objet clair, une personnalisation et une prochaine action. E8 traite les leads marqués signés et peut envoyer la convention et la facture ensemble. Cela ne remplace ni la signature électronique ni le rapprochement du paiement. Les règles de TVA, les prix textuels et les champs incomplets doivent encore être fiabilisés.','proposal_generator.py, contract_generator.py, commercial_templates.py, run_e8_contract.py. Exemples locaux sans valeur commerciale.');
title(20,'Résultats et validation');
text(20,'11 tests métier réussis',195,360,1300,100,64,true,GREEN,'center');
para(20,['Scoring, routage et sélection de la formation.','Prix, références et numérotation des documents.','Journal d’envoi, reprise CRM et erreurs contrôlées.'],{y:510,size:41,gap:105});
text(20,'28 fichiers Python analysés. Aucun conflit de dépendances détecté.',195,845,1320,70,34,false,NAVY,'center');foot(20,'Vérifications locales du 17 septembre 2026. Les services externes restent à valider en conditions réelles.');page(20);
note(20,55,'Les résultats vérifiés sont onze tests métier réussis, une analyse syntaxique de vingt-huit fichiers propres au projet et un contrôle de cohérence des dépendances. Les tests portent sur des règles ciblées, notamment les scores, les références et le journal. Ils ne constituent pas une recette complète des intégrations. Je ne présente pas de taux de conversion ou de gain de temps mesuré : ces indicateurs nécessitent une collecte en exploitation et une comparaison avec une situation de référence.','tests/test_business_rules.py. Vérifications locales réalisées pour le rapport le 17 septembre 2026.');
title(21,'Limites et perspectives');
table(21,[['Priorité','Amélioration attendue'],['Fiabilité métier','Formation obligatoire, prix structurés, règles de TVA validées'],['Exploitation','Planification, rattrapage des échéances, suivi des réponses'],['Sécurité','Accès authentifié, gestion des secrets et des habilitations'],['Montée en charge','Journal central, verrouillage et tests de concurrence'],['Périmètre','Publication sociale E3 et suivi après-vente']],165,350,1390,520,[330,1060],35);foot(21,'Priorité : fiabiliser les parcours existants avant d’ajouter de nouveaux canaux.');page(21);
note(21,60,'La première priorité est la cohérence des dossiers : une formation clairement identifiée et des montants non ambigus. Ensuite, un planificateur doit gérer les échéances manquées et l’arrêt des relances après réponse. La sécurité concerne l’accès au dashboard, les secrets et la protection des données. Pour plusieurs utilisateurs, le journal doit devenir central et transactionnel. Enfin, la publication sociale et le suivi après-vente étendent le périmètre. L’ordre proposé consolide les parcours existants avant d’ajouter des canaux.','Rapport, sections 3.2.4 et 4.3.2. État du code analysé.');
divider(22,'CONCLUSION','Un prototype qui relie la qualification du prospect\naux communications et aux documents commerciaux');
text(22,'Merci pour votre attention',280,786,1120,85,48,true,NAVY,'center');text(22,'Questions et échanges',280,881,1120,65,35,false,NAVY,'center');
note(22,40,'Pour conclure, ADG-10 réunit les principales fonctions du parcours commercial dans un prototype supervisé. Le travail combine analyse métier, intégration de services, génération documentaire et conception d’une interface. La suite consiste à renforcer la fiabilité et à conduire une recette sur un périmètre réel contrôlé. Ce projet m’a permis d’articuler les choix techniques avec les exigences du suivi commercial. Je vous remercie pour votre attention et je suis prêt à répondre à vos questions.','Rapport, conclusion générale et perspectives.');

await fs.mkdir(path.join(ROOT,'output/presentations'),{recursive:true});
const candidate=TMP+'/candidate.pptx';await (await PresentationFile.exportPptx(p)).save(candidate);
await fs.writeFile(TMP+'/built.json',JSON.stringify(p.toProto()));
for(let i=0;i<p.slides.items.length;i++){
 const img=await p.export({slide:p.slides.items[i],format:'png',scale:.75});
 await fs.writeFile(`${TMP}/final-${i+1}.png`,new Uint8Array(await img.arrayBuffer()));
}
const finalPath=path.join(ROOT,'output/presentations/Presentation_ADG10_Yassine_Fatnaoui.pptx');
const result=await finalizePresentation({workspaceDir:ROOT,candidatePath:candidate,finalPath,pythonExecutable:PY,integrityValidatorPath:SKILL+'/container_tools/inspect_presentation_package_integrity.py',layoutValidatorPath:SKILL+'/container_tools/inspect_presentation_layout_geometry.py',layoutArgs:['--expected-slide-size-emu','18288000,10287000','--validate-bullet-geometry','--validate-heading-fit',...[8,10,17,21].flatMap(n=>['--require-native-table-slide',String(n)])],requiredNativeTableOwnerSlides:[8,10,17,21],requiredNativeChartOwnerSlides:[13],materializeLiteralChartWorkbooks:true,fontPolicy:{basis:'reference',families:[F],referencePath:sourcePath,referenceSha256:crypto.createHash('sha256').update(await fs.readFile(sourcePath)).digest('hex')},verifyArtifactToolImport:true,receiptPath:TMP+'/validation.json'});
console.log(JSON.stringify(result));
