from pathlib import Path
from PIL import Image, ImageOps, ImageDraw
import pdfplumber
from pypdf import PdfReader
base=Path(__file__).parent
files=sorted(base.glob('page-*.png'))
for start in range(0,len(files),6):
    sheet=Image.new('RGB',(1410,2060),'#dddddd');d=ImageDraw.Draw(sheet)
    for j,path in enumerate(files[start:start+6]):
        im=Image.open(path);im.thumbnail((690,650));x=(j%2)*705+(705-im.width)//2;y=(j//2)*686+22;sheet.paste(im,(x,y));d.text((x,y-17),path.stem,fill='black')
    sheet.save(base/f'contact-{start//6+1:02}.png')
pdf=base.parents[2]/'output/pdf/Rapport_Stage_ADG10_Yassine_Fatnaoui_Mis_A_Jour.pdf'
with pdfplumber.open(pdf) as doc:
    for i,page in enumerate(doc.pages):
        words=page.extract_words();text=page.extract_text() or ''
        bad=[w['text'] for w in words if i>=3 and (w['x0']<60 or w['x1']>540 or w['top']<45 or w['bottom']>819)]
        print(i+1, len(text), 'BOUNDARY',bad[:10])
source=PdfReader(r'C:\Users\yassine\Desktop\Rapport_Stage_ADG10_Yassine_Fatnaoui.pdf');dest=PdfReader(pdf)
assert all(source.pages[i].get_contents().get_data()==dest.pages[i].get_contents().get_data() for i in range(3))
print('FIRST THREE PAGES: EXACT CONTENT STREAM MATCH')
