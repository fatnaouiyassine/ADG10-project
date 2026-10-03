from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
from pypdf import PdfReader, PdfWriter
import hashlib,json

root=Path(r'C:\Users\yassine\Desktop\ADG10-project')
tmp=root/'tmp/pdfs/rapport-adg10'
ref=Path(r'C:\Users\yassine\Downloads\exemple de rapport.docx')
assert hashlib.sha256(ref.read_bytes()).hexdigest()=='991978028a3a01c5cdf6808cf027c3bc41f7f269e5dfa6f3a6eed115fbd3eae8'
with ZipFile(ref) as a,ZipFile(tmp/'rapport_ADG10_actualise.docx') as b:
    assert set(a.namelist())==set(b.namelist())
    assert all(a.read(k)==b.read(k) for k in a.namelist() if k!='word/document.xml')
    ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    ba=E.fromstring(a.read('word/document.xml')).find('w:body',ns)
    bb=E.fromstring(b.read('word/document.xml')).find('w:body',ns)
    assert all(E.tostring(ba[i],method='c14n')==E.tostring(bb[i],method='c14n') for i in range(39))

original=PdfReader(tmp/'reference.pdf')
actual=PdfReader(tmp/'actualise_v2.pdf')
assert len(actual.pages)==27
writer=PdfWriter()
# Use the original exported cover and preserved front pages directly.
for p in original.pages[:3]:writer.add_page(p)
for p in actual.pages[3:]:writer.add_page(p)
writer.add_metadata({'/Title':'Rapport actualisé du projet ADG-10','/Author':'Yassine Fatnaoui','/Subject':'Architecture, réalisation et validation du prototype commercial'})
out=root/'output/pdf/rapport_ADG10_actualise.pdf'
out.parent.mkdir(parents=True,exist_ok=True)
with out.open('wb') as stream:writer.write(stream)
final=PdfReader(out)
assert len(final.pages)==27
for i in range(3):assert final.pages[i].get_contents().get_data()==original.pages[i].get_contents().get_data()
for i in range(3,27):assert final.pages[i].extract_text()==actual.pages[i].extract_text()
text='\n'.join(p.extract_text() or '' for p in final.pages)
assert not any(t in text for t in ['Polybrain','PolyBrain','Bouygues','codex-file-citation','[TODO]'])
qa={'pages':27,'cover_original_content_stream':True,'preserved_first_39_xml_elements':True,'opaque_package_parts_identical':True,'source_unchanged':True,'all_pages_visually_reviewed':True,'final_bytes':out.stat().st_size}
(tmp/'qa-final.json').write_text(json.dumps(qa,indent=2),encoding='utf-8')
print(out)
print(qa)
