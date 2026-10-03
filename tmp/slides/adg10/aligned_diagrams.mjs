export function alignedDiagrams(n,{slide,text,title,foot,box,link,NAVY,GREEN,F,nodeFill='#EAF5F7'}){
 const node=(s,x,y,w,h,sz=32,geom='rect')=>{const a=box(n,s,x,y,w,h,sz,geom);a.fill=nodeFill;return a;};
 if(n===11){
  title(n,'Cas d’utilisation');
  const boundary=slide(n).shapes.add({geometry:'rect',name:'Système ADG-10',position:{left:510,top:322,width:870,height:588},fill:'none',line:{fill:'#A9C1CC',width:2}});
  text(n,'Système ADG-10',560,328,770,48, thirty(),true,NAVY,'center');
  const commercial=node('Commercial',115,440,300, ninety(),36),admin=node('Administrateur',115,742,300,90,34);
  const labels=['Consulter et filtrer les leads','Exécuter en simulation / réel','Générer contenus et documents','Déclencher les relances','Configurer et contrôler les journaux'];
  const uses=labels.map((s,i)=>node(s,565,385+i*102,760,80,32,'ellipse'));
  for(let i=0;i<4;i++)link(n,commercial,uses[i]);link(n,admin,uses[4]);
  const at=node('Airtable\nDonnées CRM',1480,400,320,95,32),gr=node('Groq\nGénération IA',1480,594,320,95,32),sm=node('SMTP / navigateur\nCommunication',1480,790,320,95,32);
  link(n,uses[0],at);link(n,uses[2],gr);link(n,uses[3],sm);
  foot(n,'Rôles métier du rapport. Le prototype ne dispose pas encore de comptes applicatifs distincts.');
 }
 if(n===12){
  title(n,'Modèle conceptuel des données');
  const f=node('Formation\nid, titre, durée\nprix, pitch, objectifs',145,350,610,200,40);
  const lead=node('Lead\nid, coordonnées, score\nstatut, formation, dates',1135,350,610,200,40);
  link(n,f,lead);text(n,'1                         0..*',785,400,320,50,31,false,NAVY,'center');
  const pr=node('Proposition\nréférence, date\nPDF local',145,705,480,170,36);
  const co=node('Convention / Facture\nnuméro, montants\nPDF local',705,705,500,170,36);
  const ac=node('ActionEnvoi\nclé, canal, date UTC\njournal JSON',1285,705,460,170,36);
  [pr,co,ac].forEach(a=>link(n,lead,a,'bottom','top'));
  foot(n,'Modèle conceptuel, non classes Python persistées. Données métier dans Airtable, PDF et journal locaux.');
 }
 if(n===14){
  title(n,'Séquence d’envoi d’une proposition');
  const xs=[240,595,950,1305,1660],labs=['Script E6','Airtable','Journal local','PDF','SMTP'];
  const heads=labs.map((s,i)=>node(s,xs[i]-140,325,280,75,35));
  const anchor=(x,y)=>slide(n).shapes.add({geometry:'rect',name:'Point de séquence',position:{left:x,top:y,width:1,height:1},fill:'none',line:{fill:'none',width:0}});
  for(let i=0;i<5;i++)slide(n).shapes.connect(heads[i],anchor(xs[i],914),{kind:'straight',fromSide:'bottom',toSide:'top',line:{fill:'#A9BDC6',width:2,style:'dashed'}});
  const actions=[[1,'1. Lire les prospects'],[2,'2. Rechercher un envoi antérieur'],[3,'3. Générer la proposition'],[4,'4. Envoyer avec pièce jointe'],[2,'5. Mémoriser le succès'],[1,'6. Mettre à jour date et statut']];
  actions.forEach(([to,s],i)=>{const y=455+i* eighty();link(n,anchor(xs[0],y),anchor(xs[to],y));text(n,s,xs[0]+15,y-48,Math.max(xs[to]-xs[0]-25,530),44,29);});
  foot(n,'Si l’envoi est déjà journalisé : réconcilier le CRM sans renvoyer le message.');
 }
 if(n===15){
  title(n,'Architecture technique');
  const ui=node('Interface Streamlit : vues, filtres, commandes',355,325,1160,100,39);
  const scripts=node('Scripts E1 à E8 et orchestrateur du pipeline',355,485,1160,100,39);
  const rules=node('Règles métier : scoring, séquences, modèles de messages',355,645,1160,100,37);
  link(n,ui,scripts,'bottom','top');link(n,scripts,rules,'bottom','top');
  const targets=[node('Airtable / Groq\nAPI externes',130,820,480,105,33),node('SMTP / WhatsApp\nAdaptateurs d’envoi',700,820,480,105,33),node('ReportLab / JSON\nPDF et état local',1270,820,480,105,33)];
  targets.forEach(a=>link(n,rules,a,'bottom','top'));
  foot(n,'Configuration centralisée, simulation par défaut, logs et contrôles locaux.');
 }
 function thirty(){return 30;}function ninety(){return 90;}function eighty(){return 80;}
}
