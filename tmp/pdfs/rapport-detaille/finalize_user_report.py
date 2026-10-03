from pathlib import Path
import io,json,re
from pypdf import PdfReader,PdfWriter
from reportlab.pdfgen import canvas
import build_report_revise as b

BASE=Path(__file__).parent
SOURCE=Path('C:/Users/yassine/Downloads/Rapport_Stage_ADG10_Yassine_Fatnaoui_Revise (3).pdf')
OUT=b.ROOT/'output/pdf/Rapport_Stage_ADG10_Table_Matieres_Corrigee.pdf'
r=PdfReader(SOURCE)
entries=json.loads((BASE/'layout-revise.json').read_text(encoding='utf8'))['entries']
pre=[('Page de garde (non numérotée)','-'),('Dédicace','I'),('Remerciements','II'),('Résumé','III'),('Abstract','IV'),('Liste des abréviations','V'),('Liste des figures','VI'),('Liste des tableaux','VII'),('Table des matières','VIII')]
b.ST['h1'].fontName='TimesNewB'
# Build a complete contents list without regenerating the user's report body.
tocrows=[('heading',1,t,n) for t,n in pre]+[e for e in entries if e[0]=='heading']
doc=b.Doc(BASE/'toc-final.pdf',front=True)
def tocfooter(c,d):
    c.setFont('TimesNew',10);c.drawCentredString(b.W/2,30,b.roman(d.page+7))
doc.build([b.heading('Table des matières'),b.list_table(tocrows)],onFirstPage=tocfooter,onLaterPages=tocfooter)
toc=PdfReader(BASE/'toc-final.pdf')
w=PdfWriter()
def remove_text(page,predicate):
    stream=page.get_contents();out=[];x=y=0
    for args,op in stream.operations:
        if op==b'Tm':x,y=float(args[4]),float(args[5])
        if op in (b'Tj',b'TJ') and predicate(x,y):continue
        out.append((args,op))
    stream.operations=out;page.replace_contents(stream)
def overlay(page,draw):
    mem=io.BytesIO();c=canvas.Canvas(mem,pagesize=(float(page.mediabox.width),float(page.mediabox.height)))
    draw(c);c.save();page.merge_page(PdfReader(mem).pages[0])
w.add_page(r.pages[0]);cover=w.pages[0]
remove_text(cover,lambda x,y:40<y<115)
def names(c):
    c.setFont('TimesNew',12)
    for text,y in [('AZOUGUIGH El Houssaine',109.94),('BAILOUL Charaf Eddine',89.304)]:
        c.drawString(63.624,y,'•');c.drawString(81.624,y,text)
overlay(cover,names)
for i in range(1,6):w.add_page(r.pages[i])
# Omit the source Sommaire (page 7). Renumber the two following preliminary pages.
for i,num in [(7,'VI'),(8,'VII')]:
    w.add_page(r.pages[i]);page=w.pages[-1]
    remove_text(page,lambda x,y:y<45)
    def draw(c,n=num):c.setFont('TimesNew',10);c.drawCentredString(b.W/2,30,n)
    overlay(page,draw)
for page in toc.pages:w.add_page(page)
body_start=len(w.pages)
for page in r.pages[12:]:w.add_page(page)
for title,number in pre[1:-1]:
    index={'I':1,'II':2,'III':3,'IV':4,'V':5,'VI':6,'VII':7}[number]
    w.add_outline_item(title,index)
w.add_outline_item('Table des matières',8)
parent=None
for kind,level,title,page in entries:
    if kind=='heading' and level<=2:
        item=w.add_outline_item(title,body_start+page-1,parent=parent if level==2 else None)
        if level==1:parent=item
w.add_metadata({'/Title':'Rapport de stage ADG-10 - Table des matières corrigée','/Author':'Yassine Fatnaoui'})
with OUT.open('wb') as f:w.write(f)
check=PdfReader(OUT)
assert len(check.pages)==8+len(toc.pages)+46
assert all(check.pages[body_start+i].extract_text()==r.pages[12+i].extract_text() for i in range(46))
assert all(check.pages[i].extract_text()==r.pages[i].extract_text() for i in range(1,6))
print(json.dumps({'output':str(OUT),'pages':len(check.pages),'toc_pages':len(toc.pages),'body_start_pdf_page':body_start+1,'body_and_preliminaries_preserved':True},ensure_ascii=False))
