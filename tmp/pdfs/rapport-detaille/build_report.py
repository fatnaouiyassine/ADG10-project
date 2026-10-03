from pathlib import Path
import re, json, math
from xml.sax.saxutils import escape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image, KeepTogether, Flowable
from pypdf import PdfReader, PdfWriter

BASE=Path(__file__).parent
ROOT=BASE.parents[2]
OUT=ROOT/'output/pdf/Rapport_Stage_ADG10_Yassine_Fatnaoui_Mis_A_Jour.pdf'
SOURCE=Path(r'C:\Users\yassine\Desktop\Rapport_Stage_ADG10_Yassine_Fatnaoui.pdf')
W,H=595.32,841.92
WIDTH=467.26
for name,file in [('TimesNew','times.ttf'),('TimesNewB','timesbd.ttf'),('TimesNewI','timesi.ttf'),('Calibri','calibri.ttf'),('CalibriB','calibrib.ttf')]:
    pdfmetrics.registerFont(TTFont(name, 'C:/Windows/Fonts/'+file))
pdfmetrics.registerFontFamily('TimesNew',normal='TimesNew',bold='TimesNewB',italic='TimesNewI',boldItalic='TimesNewB')
ST={
 'body':ParagraphStyle('body',fontName='TimesNew',fontSize=11.5,leading=16,alignment=TA_JUSTIFY,firstLineIndent=16,spaceAfter=8),
 'h1':ParagraphStyle('h1',fontName='CalibriB',fontSize=20,leading=25,spaceBefore=8,spaceAfter=21,keepWithNext=True),
 'h2':ParagraphStyle('h2',fontName='CalibriB',fontSize=16,leading=20,spaceBefore=15,spaceAfter=10,keepWithNext=True),
 'h3':ParagraphStyle('h3',fontName='CalibriB',fontSize=13.6,leading=17,spaceBefore=12,spaceAfter=8,keepWithNext=True),
 'h4':ParagraphStyle('h4',fontName='CalibriB',fontSize=12,leading=15,spaceBefore=10,spaceAfter=7,keepWithNext=True),
 'cell':ParagraphStyle('cell',fontName='TimesNew',fontSize=9.4,leading=12),
 'caption':ParagraphStyle('caption',fontName='TimesNewI',fontSize=10,leading=13,alignment=TA_CENTER,spaceBefore=6,spaceAfter=11),
 'code':ParagraphStyle('code',fontName='Calibri',fontSize=10,leading=14,leftIndent=12,spaceAfter=4),
 'toc':ParagraphStyle('toc',fontName='TimesNew',fontSize=10.5,leading=14,spaceAfter=4),
}
def clean(s):
    return s.replace('\u2011','-').replace('\u2013','-').replace('\u2014','-').replace('`','')
def p(s, style='body'):
    return Paragraph(escape(clean(s)),ST[style])
def roman(n):
    out=''
    for v,c in [(50,'L'),(40,'XL'),(10,'X'),(9,'IX'),(5,'V'),(4,'IV'),(1,'I')]:
        while n>=v: out+=c; n-=v
    return out
class Doc(SimpleDocTemplate):
    def __init__(self,path,front=False):
        super().__init__(str(path),pagesize=(W,H),leftMargin=68.06,rightMargin=60,topMargin=57,bottomMargin=55,title='Rapport de stage ADG-10 - Yassine Fatnaoui',author='Yassine Fatnaoui')
        self.entries=[]; self.front=front
    def afterFlowable(self,f):
        if hasattr(f,'entry'): self.entries.append((*f.entry,self.page))
def footer(c,d):
    c.saveState(); c.setFont('TimesNew',10); c.setFillColor(colors.black)
    c.drawCentredString(W/2,30,roman(d.page+2) if d.front else str(d.page)); c.restoreState()
def heading(s,level=1):
    f=p(s,'h'+str(level)); f.entry=('heading',level,clean(s)); return f
def caption(s,kind):
    f=p(s,'caption'); f.entry=(kind,0,clean(s)); return f
def table(rows):
    n=len(rows[0]); weights=[1]*n
    if n==2: weights=[.32,.68]
    if n==3: weights=[.23,.40,.37]
    if n==4: weights=[.15,.29,.28,.28]
    if max(len(x[0]) for x in rows)<8: weights=[.10]+[(.9/(n-1))]*(n-1)
    weights=[x/sum(weights) for x in weights]
    data=[[p(x,'cell') for x in row] for row in rows]
    for i,x in enumerate(rows[0]): data[0][i]=Paragraph('<b>'+escape(clean(x))+'</b>',ST['cell'])
    t=Table(data,colWidths=[WIDTH*x for x in weights],repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e9ecea')),('GRID',(0,0),(-1,-1),.4,colors.HexColor('#a0a0a0')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
    return t

class Diagram(Flowable):
    def __init__(self,key):
        Flowable.__init__(self); self.key=key; self.width=WIDTH; self.height={'pipeline':235,'planning':235,'usecases':315,'sequence':330,'timeline':200,'classes':310,'architecture':310}[key]
    def draw(self):
        c=self.canv
        def txt(s,x,y,w=100,size=10,center=True):
            st=ParagraphStyle('d',fontName='Calibri',fontSize=size,leading=size+2,alignment=TA_CENTER if center else 0)
            q=Paragraph(escape(s).replace('\n','<br/>'),st); _,h=q.wrap(w,100);q.drawOn(c,x,y-h)
        def box(s,x,y,w=105,h=55,fill='#f2f5f3'):
            c.setStrokeColor(colors.HexColor('#42644f'));c.setFillColor(colors.HexColor(fill));c.roundRect(x,y,w,h,4,fill=1,stroke=1);txt(s,x+5,y+h-9,w-10)
        def arrow(x,y,u,v,label=''):
            c.setStrokeColor(colors.HexColor('#49534d'));c.setFillColor(colors.HexColor('#49534d'));c.setLineWidth(.8);c.line(x,y,u,v)
            a=math.atan2(v-y,u-x);p0=c.beginPath();p0.moveTo(u,v);p0.lineTo(u-6*math.cos(a-.4),v-6*math.sin(a-.4));p0.lineTo(u-6*math.cos(a+.4),v-6*math.sin(a+.4));p0.close();c.drawPath(p0,fill=1)
            if label: txt(label,min(x,u),max(y,v)+17,abs(u-x) or 100,8)
        k=self.key
        if k=='pipeline':
            labels=['E1\nContenus IA','E2\nTextes multicanaux','E3\nPublication absente','E4\nScoring / routage','E8\nConvention / facture','E7\nSuivi du closing','E6\nProposition PDF','E5\nNurturing']
            for i,s in enumerate(labels): box(s,(i%4)*119,150 if i<4 else 52,108,57,'#eeeeee' if i==2 else '#f2f5f3')
            for i in range(3): arrow(i*119+108,178,(i+1)*119,178);arrow((i+1)*119,80,i*119+108,80)
            arrow(411,150,411,109)
            txt('Les relances nécessitent l’exécution des scripts.\nLa signature et les décisions commerciales restent humaines.',0,32,WIDTH,10)
        elif k=='planning':
            labels=['Analyse et cadrage','CRM et configuration','IA et qualification','Relances et documents','Interface et sécurité','Tests et rapport']; bars=[(0,2),(1,3),(2,4),(3,6),(5,7),(6,8)]
            for j in range(8):txt('S'+str(j+1),174+j*35,225,33,9)
            for i,(label,(a,b)) in enumerate(zip(labels,bars)):
                y=178-i*26;txt(label,0,y+18,166,10,False)
                for j in range(8):c.setStrokeColor(colors.lightgrey);c.rect(174+j*35,y,35,22)
                c.setFillColor(colors.HexColor('#739783'));c.rect(176+a*35,y+4,(b-a)*35-4,14,stroke=0,fill=1)
            txt('Plan reconstitué à titre indicatif : il ne constitue pas un relevé daté du stage.',0,28,WIDTH,9)
        elif k=='usecases':
            c.setStrokeColor(colors.grey);c.rect(105,20,255,282);txt('Système ADG-10',105,294,255,12)
            box('Commercial',0,207,90,42);box('Administrateur',0,87,90,42)
            box('Airtable\nDonnées CRM',374,229,90,48);box('Groq\nGénération IA',374,151,90,48);box('SMTP / navigateur\nCommunication',374,61,90,52)
            for s,y in [('Consulter et filtrer les leads',243),('Exécuter en simulation / réel',191),('Générer contenus et documents',139),('Déclencher les relances',87),('Configurer et contrôler les journaux',35)]:
                c.setFillColor(colors.HexColor('#f2f5f3'));c.ellipse(120,y,345,y+38,fill=1);txt(s,128,y+30,210,10)
            for y in [262,210,158,106]:arrow(90,228,120,y)
            arrow(90,108,120,54);arrow(345,262,374,252);arrow(345,158,374,174);arrow(345,106,374,87)
        elif k=='sequence':
            xs=[44,139,234,329,424]
            for x,s in zip(xs,['Script E6','Airtable','Journal local','PDF','SMTP']):
                box(s,x-42,282,84,34);c.setStrokeColor(colors.lightgrey);c.setDash(2,3);c.line(x,20,x,282);c.setDash()
            actions=[(0,1,'1. Lire les prospects',255),(0,2,'2. Rechercher un envoi antérieur',218),(0,3,'3. Générer la proposition',181),(0,4,'4. Envoyer avec pièce jointe',144),(0,2,'5. Mémoriser le succès',107),(0,1,'6. Mettre à jour date et statut',70)]
            for a,b,s,y in actions:arrow(xs[a],y,xs[b],y,s)
            txt('Si l’envoi est déjà journalisé : réconcilier le CRM sans renvoyer le message.',0,27,WIDTH,9)
        elif k=='timeline':
            for i,(s,t) in enumerate([('J0','Proposition envoyée'),('J+5','WhatsApp'),('J+8','E-mail'),('J+12','Appel humain')]):
                x=i*119;box(s+'\n'+t,x,90,108,63)
                if i<3:arrow(x+108,122,x+119,122)
            txt('Ancrage : date de proposition, avec repli selon les données disponibles.\nÉchéances exactes : un jour manqué n’est pas automatiquement rattrapé.\nL’appel est signalé, mais non réalisé par le logiciel.',15,66,437,10)
        elif k=='classes':
            box('Formation\nid · titre · durée\nprix · pitch · objectifs',0,220,185,72)
            box('Lead\nid · coordonnées · score\nstatut · formation · dates',275,220,185,72)
            arrow(185,257,275,257,'1         0..*')
            box('Proposition\nréférence · date\nPDF local',0,105,140,72)
            box('Convention / Facture\nnuméro · montants\nPDF local',164,105,146,72)
            box('ActionEnvoi\nclé · canal · date UTC\njournal JSON',334,105,130,72)
            arrow(335,220,70,177);arrow(368,220,237,177);arrow(400,220,399,177)
            txt('Modèle conceptuel, et non classes Python persistées.\nAirtable conserve les données métier ; les fichiers PDF et le journal sont locaux.\nLes relations documentaires ne forment pas une base relationnelle transactionnelle.',0,68,WIDTH,10)
        elif k=='architecture':
            for s,y in [('Interface Streamlit : vues, filtres, commandes',257),('Scripts E1 à E8 et orchestrateur du pipeline',199),('Règles métier : scoring, séquences, modèles de messages',141)]:
                box(s,38,y,392,40)
            arrow(234,257,234,239);arrow(234,199,234,181)
            for s,x in [('Airtable / Groq\nAPI externes',0),('SMTP / WhatsApp\nAdaptateurs d’envoi',160),('ReportLab / JSON\nPDF et état local',320)]:
                box(s,x,58,147,58);arrow(234,141,x+73,116)
            txt('Configuration centralisée · simulation par défaut · logs · contrôles locaux',0,30,WIDTH,10)

def parse():
    lines=(BASE/'rapport.md').read_text(encoding='utf-8').splitlines(); story=[];i=0
    while i<len(lines):
        s=lines[i].strip();i+=1
        if not s:continue
        if s.startswith('#'):
            m=re.match(r'(#+) (.*)',s);level=len(m[1])
            if level==1 and story:story.append(PageBreak())
            story.append(heading(m[2],level));continue
        if s.startswith('@table '):
            rows=[]
            while i<len(lines) and not lines[i].strip():i+=1
            while i<len(lines) and lines[i].strip().startswith('|'):
                rows.append([x.strip() for x in lines[i].strip().strip('|').split('|')]);i+=1
            cap=caption(s[7:],'table');cap.keepWithNext=True;story.extend([cap,table(rows),Spacer(1,10)]);continue
        if s.startswith('@diagram '):
            key,cap=s[9:].split('|');group=[Diagram(key),caption(cap,'figure')]
            if story and hasattr(story[-1],'entry') and story[-1].entry[0]=='heading':group.insert(0,story.pop())
            story.append(KeepTogether(group));continue
        if s.startswith('@image '):
            file,cap,height=s[7:].split('|');im=Image(str(BASE/'assets'/file));scale=min(WIDTH/im.imageWidth,float(height)/im.imageHeight);im.drawWidth=im.imageWidth*scale;im.drawHeight=im.imageHeight*scale
            story.append(KeepTogether([im,caption(cap,'figure')]));continue
        if s.startswith('@example '):story.append(heading(s[9:],4));continue
        if s=='@endexample':continue
        if s=='@code':
            while i<len(lines) and lines[i]!='@endcode':story.append(p(lines[i],'code'));i+=1
            i+=1;story.append(Spacer(1,8));continue
        block=[s]
        while i<len(lines) and lines[i].strip() and not lines[i].startswith(('#','@')):block.append(lines[i].strip());i+=1
        if re.match(r'^\[\d+\]',s):
            st=ParagraphStyle('reference',parent=ST['body'],alignment=0,firstLineIndent=0,fontSize=10.5,leading=14)
            story.append(Paragraph(escape(clean(' '.join(block))),st))
        else:story.append(p(' '.join(block)))
    return story

def list_table(entries):
    rows=[]
    for kind,level,title,page in entries:
        if level==4:continue
        indent=0 if level<2 else 10*(level-1)
        st=ParagraphStyle('tocrow',parent=ST['toc'],leftIndent=indent,fontName='TimesNewB' if level==1 else 'TimesNew')
        rows.append([Paragraph(escape(title),st),p(str(page),'toc')])
    t=Table(rows,colWidths=[WIDTH-30,30],hAlign='LEFT');t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('ALIGN',(1,0),(1,-1),'RIGHT'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),4)]));return t

def main():
    body=Doc(BASE/'body.pdf');body.build(parse(),onFirstPage=footer,onLaterPages=footer)
    es=body.entries;front=[]
    def section(title,paragraphs):
        if front:front.append(PageBreak())
        front.append(heading(title))
        for s in paragraphs:front.append(p(s))
    section('Résumé',[
        'Ce rapport présente la conception et la réalisation d’ADG-10, un prototype d’automatisation du parcours commercial des formations pour ADBCENTER LOGISPLAN et son environnement Adaoui Business Centre. Le projet répond au besoin de mieux organiser les prospects, d’harmoniser les communications et de réduire les opérations répétitives entre la qualification d’un contact et la préparation des documents commerciaux.',
        'La solution repose sur Python, Airtable et un tableau de bord Streamlit. Groq intervient dans la génération de contenus ; des règles explicites réalisent le scoring et le routage des prospects. Les scripts préparent les messages, les relances et les propositions. ReportLab produit désormais les propositions, conventions de formation et factures, tandis qu’un journal local limite certains renvois lors des reprises d’exécution.',
        'Le rapport reprend l’ensemble du cheminement : présentation de l’organisme, problématique, conduite du projet, besoins, conception UML, choix techniques, architecture, mise en œuvre, tests et résultats illustrés. Il actualise en particulier le rôle du dashboard, la professionnalisation des communications et l’implémentation de l’étape de contractualisation et facturation.',
        'Les vérifications locales comprennent onze tests métier réussis, l’analyse syntaxique de vingt-huit fichiers Python et le contrôle des dépendances installées. Elles ne constituent pas une recette de production des services externes. Les limites de publication sociale, de planification des relances, de concurrence, de sécurité et de facturation sont distinguées des fonctionnalités opérationnelles dans le code.',
        'Mots-clés : automatisation commerciale, CRM, Python, Airtable, Streamlit, intelligence artificielle, scoring, documents PDF.'
    ])
    section('Abstract',[
        'This report describes the design and implementation of ADG-10, a prototype supporting the sales workflow for training services at ADBCENTER LOGISPLAN and its Adaoui Business Centre environment. The project aims to organise prospects, standardise communications and reduce repetitive tasks from lead qualification to commercial document preparation.',
        'The application combines Python scripts, an Airtable CRM and a Streamlit dashboard. Groq supports content generation, while explicit business rules determine lead scores and routing. The workflow prepares follow-up messages and proposals. ReportLab now generates proposals, training agreements and invoices. A local delivery ledger supports selected retry and CRM reconciliation scenarios.',
        'The report covers the host organisation, project planning, requirements, UML models, technical choices, architecture, implementation, tests and illustrated results. Particular attention is paid to the updated dashboard, professional communication templates and the implemented agreement and invoicing stage.',
        'Local verification includes eleven successful business tests, syntax checks on twenty-eight Python files and installed dependency consistency checks. These results do not demonstrate live delivery or production readiness of external services. Remaining limitations in social publishing, scheduling, concurrency, security and invoice validation are explicitly documented.',
        'Keywords: sales automation, CRM, Python, Airtable, Streamlit, artificial intelligence, lead scoring, PDF documents.'
    ])
    section('Liste des abréviations',[])
    front.append(table([['Abréviation','Signification'],['ABC','Adaoui Business Centre'],['ADG-10','Nom du projet d’automatisation commerciale étudié'],['API','Application Programming Interface'],['CRM','Customer Relationship Management'],['HT / TTC / TVA','Hors taxes / Toutes taxes comprises / Taxe sur la valeur ajoutée'],['IA','Intelligence artificielle'],['JSON','JavaScript Object Notation'],['KPI','Key Performance Indicator'],['LLM','Large Language Model'],['PDF','Portable Document Format'],['PME / TPE','Petite et moyenne entreprise / Très petite entreprise'],['SMTP','Simple Mail Transfer Protocol'],['UML','Unified Modeling Language'],['UTC','Coordinated Universal Time']]))
    section('Sommaire',[]);front.append(list_table([x for x in es if x[0]=='heading' and x[1]==1]))
    section('Liste des figures',[]);front.append(list_table([x for x in es if x[0]=='figure']))
    section('Liste des tableaux',[]);front.append(list_table([x for x in es if x[0]=='table']))
    section('Table des matières',[]);front.append(list_table([x for x in es if x[0]=='heading']))
    fd=Doc(BASE/'front.pdf',front=True);fd.build(front,onFirstPage=footer,onLaterPages=footer)
    source=PdfReader(SOURCE);fr=PdfReader(BASE/'front.pdf');br=PdfReader(BASE/'body.pdf');writer=PdfWriter()
    for page in list(source.pages[:3])+list(fr.pages)+list(br.pages):writer.add_page(page)
    offset=3+len(fr.pages)
    parent=None
    for kind,level,title,page in es:
        if kind=='heading' and level<=2:
            item=writer.add_outline_item(title,offset+page-1,parent=parent if level==2 else None)
            if level==1:parent=item
    writer.add_metadata({'/Title':'Rapport de stage ADG-10 - Version actualisée','/Author':'Yassine Fatnaoui','/Subject':'Analyse, conception, réalisation et validation du projet ADG-10'})
    OUT.parent.mkdir(parents=True,exist_ok=True)
    with OUT.open('wb') as f:writer.write(f)
    (BASE/'layout.json').write_text(json.dumps({'pages':len(writer.pages),'front':offset,'entries':es},ensure_ascii=False,indent=2),encoding='utf-8')
    print(OUT);print('Total pages:',len(writer.pages),'Preliminaries:',offset,'Body:',len(br.pages))
if __name__=='__main__':main()
