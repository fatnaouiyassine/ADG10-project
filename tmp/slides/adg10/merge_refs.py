import sys,zipfile,re,copy,posixpath
from lxml import etree as E
P='http://schemas.openxmlformats.org/presentationml/2006/main'
A='http://schemas.openxmlformats.org/drawingml/2006/main'
R='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
PK='http://schemas.openxmlformats.org/package/2006/relationships'
CT='http://schemas.openxmlformats.org/package/2006/content-types'
ns={'p':P,'a':A,'r':R}
def xml(b):return E.fromstring(b)
def serial(e):return E.tostring(e,xml_declaration=True,encoding='UTF-8',standalone=True)
with zipfile.ZipFile(sys.argv[1]) as src,zipfile.ZipFile(sys.argv[2]) as new:
 data={n:src.read(n) for n in src.namelist()}
 pres=xml(data['ppt/presentation.xml']);ids=pres.find('p:sldIdLst',ns)
 assert len(ids)==22
 rels=xml(data['ppt/_rels/presentation.xml.rels']);ct=xml(data['[Content_Types].xml'])
 nextid=max(int(x.get('id')) for x in ids)+1
 nextrid=max(int(x.get('Id')[3:]) for x in rels if x.get('Id').startswith('rId'))+1
 # Preserve all existing slide markup, including user edits and animation, apart from the total page count.
 for n in range(1,23):
  name=f'ppt/slides/slide{n}.xml';root=xml(data[name])
  for t in root.findall('.//a:t',ns):
   if re.fullmatch(r'\d{2} / 22',t.text or ''):t.text=t.text[:-2]+'24'
  data[name]=serial(root)
 for k,n in [(1,23),(2,24)]:
  root=xml(new.read(f'ppt/slides/slide{k}.xml'))
  sr=xml(data['ppt/slides/_rels/slide22.xml.rels'])
  outrels=E.Element('{'+PK+'}Relationships',nsmap={None:PK})
  for rel in sr:
   if rel.get('Type').endswith('/slideLayout'):outrels.append(copy.deepcopy(rel))
  if n==24:
   pic=copy.deepcopy(xml(data['ppt/slides/slide22.xml']).find('.//p:pic',ns))
   pic.find('p:nvPicPr/p:cNvPr',ns).set('id','1000')
   rid=pic.find('.//a:blip',ns).get('{'+R+'}embed')
   root.find('p:cSld/p:spTree',ns).insert(2,pic)
   outrels.append(copy.deepcopy(next(x for x in sr if x.get('Id')==rid)))
  E.SubElement(outrels,'{'+PK+'}Relationship',Id='rIdNotesAdded',Type=R+'/notesSlide',Target=f'../notesSlides/notesSlide{n}.xml')
  tr=E.SubElement(root,'{'+P+'}transition',spd='med',advClick='1');E.SubElement(tr,'{'+P+'}push',dir='l')
  data[f'ppt/slides/slide{n}.xml']=serial(root)
  data[f'ppt/slides/_rels/slide{n}.xml.rels']=serial(outrels)
  notes=xml(new.read(f'ppt/notesSlides/notesSlide{k}.xml'))
  data[f'ppt/notesSlides/notesSlide{n}.xml']=serial(notes)
  nr=xml(data['ppt/notesSlides/_rels/notesSlide22.xml.rels'])
  for r in nr:
   if r.get('Type').endswith('/slide'):r.set('Target',f'../slides/slide{n}.xml')
  data[f'ppt/notesSlides/_rels/notesSlide{n}.xml.rels']=serial(nr)
  rid=f'rId{nextrid}';nextrid+=1
  E.SubElement(rels,'{'+PK+'}Relationship',Id=rid,Type=R+'/slide',Target=f'slides/slide{n}.xml')
  E.SubElement(ids,'{'+P+'}sldId',id=str(nextid),attrib={'{'+R+'}id':rid});nextid+=1
  for part,typ in [(f'/ppt/slides/slide{n}.xml','slide'),(f'/ppt/notesSlides/notesSlide{n}.xml','notesSlide')]:
   E.SubElement(ct,'{'+CT+'}Override',PartName=part,ContentType=f'application/vnd.openxmlformats-officedocument.presentationml.{typ}+xml')
 data['ppt/presentation.xml']=serial(pres);data['ppt/_rels/presentation.xml.rels']=serial(rels);data['[Content_Types].xml']=serial(ct)
 if 'docProps/app.xml' in data:
  app=xml(data['docProps/app.xml'])
  for x in app:
   if E.QName(x).localname=='Slides':x.text='24'
  data['docProps/app.xml']=serial(app)
 with zipfile.ZipFile(sys.argv[3],'w',zipfile.ZIP_DEFLATED) as dst:
  for name,b in data.items():dst.writestr(name,b)
 print('Appended two slides; retained source slide content and native objects.')
