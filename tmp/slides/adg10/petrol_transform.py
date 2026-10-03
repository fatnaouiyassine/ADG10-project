import zipfile,sys,re,copy,posixpath
from lxml import etree as E
P='http://schemas.openxmlformats.org/presentationml/2006/main';A='http://schemas.openxmlformats.org/drawingml/2006/main';R='http://schemas.openxmlformats.org/officeDocument/2006/relationships';PK='http://schemas.openxmlformats.org/package/2006/relationships'
ns={'p':P,'a':A,'r':R}
def ser(x):return E.tostring(x,xml_declaration=True,encoding='UTF-8',standalone=True)
def textcolor(c):return any(E.QName(a).localname in ('rPr','defRPr','endParaRPr') for a in c.iterancestors())
with zipfile.ZipFile(sys.argv[1]) as src,zipfile.ZipFile(sys.argv[2]) as art:
 data={n:src.read(n) for n in src.namelist()};bgs={}
 for i,theme in enumerate(('dark','light'),1):
  bg=E.fromstring(art.read(f'ppt/slides/slide{i}.xml')).find('.//p:pic',ns)
  ar=E.fromstring(art.read(f'ppt/slides/_rels/slide{i}.xml.rels'))
  rid=bg.find('.//a:blip',ns).get('{'+R+'}embed')
  target=next(r.get('Target') for r in ar if r.get('Id')==rid)
  part=posixpath.normpath(posixpath.join('ppt/slides',target)).lstrip('/')
  data[f'ppt/media/petrol-{theme}.png']=art.read(part);bgs[theme]=bg
 darks=(1,2,3,5,9,16,22,24)
 for name in list(data):
  if not (re.fullmatch(r'ppt/slides/slide\d+\.xml',name) or ('/charts/' in name and name.endswith('.xml'))):continue
  root=E.fromstring(data[name]);n=int(re.search(r'slide(\d+)\.xml',name)[1]) if '/charts/' not in name else 0
  dark=n in darks
  palette={'293B4B':'063E53' if dark else 'E6EFF2','344B5E':'D2E4EA','3C5364':'E3EDF1','1F303E':'07556D','D2AB7D':'21B5CF' if dark else '007B97','F1EBDD':'FFFFFF' if dark else '123A4B','FFFFFF':'FFFFFF' if dark else '123A4B','BDCBCD':'C5E2E9' if dark else '406570','B6D4DF':'C5E2E9' if dark else '406570','A9C1CC':'5C8E9E','A9BDC6':'5C8E9E','617888':'94B8C4','63E1E8':'007B97'}
  for c in root.findall('.//a:srgbClr',ns):
   old=c.get('val','').upper()
   if old in palette:c.set('val',palette[old])
  for c in root.findall('.//a:schemeClr',ns):
   if c.get('val') in ('bg1','lt1') and textcolor(c):c.tag='{'+A+'}srgbClr';c.set('val','FFFFFF' if dark else '123A4B')
  # Keep white labels on native dark table headers.
  for tbl in root.findall('.//a:tbl',ns):
   tr=tbl.find('a:tr',ns)
   for c in tr.findall('.//a:srgbClr',ns):
    if textcolor(c):c.set('val','FFFFFF')
  if n:
   tree=root.find('p:cSld/p:spTree',ns)
   for pic in list(tree.findall('p:pic',ns)):
    ext=pic.find('p:spPr/a:xfrm/a:ext',ns)
    if ext is not None and int(ext.get('cx'))>=18000000 and int(ext.get('cy'))>=10000000:tree.remove(pic)
   theme='dark' if dark else 'light'
   pic=copy.deepcopy(bgs[theme]);pic.find('p:nvPicPr/p:cNvPr',ns).set('id','2000');pic.find('.//a:blip',ns).set('{'+R+'}embed','rIdPetrolBg');tree.insert(2,pic)
   relname=f'ppt/slides/_rels/slide{n}.xml.rels';rels=E.fromstring(data[relname]);E.SubElement(rels,'{'+PK+'}Relationship',Id='rIdPetrolBg',Type=R+'/image',Target=f'../media/petrol-{theme}.png')
   if n==1:
    # An image-backed light strip keeps the original institutional logos legible.
    band=copy.deepcopy(bgs['light']);band.find('p:nvPicPr/p:cNvPr',ns).set('id','2001');band.find('.//a:blip',ns).set('{'+R+'}embed','rIdLogoBand')
    xf=band.find('p:spPr/a:xfrm',ns);xf.find('a:off',ns).set('x',str(90*9525));xf.find('a:off',ns).set('y',str(95*9525));xf.find('a:ext',ns).set('cx',str(1020*9525));xf.find('a:ext',ns).set('cy',str(125*9525));tree.insert(3,band)
    E.SubElement(rels,'{'+PK+'}Relationship',Id='rIdLogoBand',Type=R+'/image',Target='../media/petrol-light.png')
   data[relname]=ser(rels)
  data[name]=ser(root)
 for n in range(1,25):
  name=f'ppt/slides/slide{n}.xml'
  assert E.fromstring(src.read(name)).xpath('//a:t/text()',namespaces=ns)==E.fromstring(data[name]).xpath('//a:t/text()',namespaces=ns)
 for name in data:
  if name.startswith('ppt/notesSlides/') or name.startswith('ppt/embeddings/'):assert data[name]==src.read(name)
 with zipfile.ZipFile(sys.argv[3],'w',zipfile.ZIP_DEFLATED) as dst:
  for name,b in data.items():dst.writestr(name,b)
 print('24 slides restyled; all slide text, speaker notes, workbooks preserved.')
