import zipfile,sys,re,copy,posixpath
from lxml import etree as E
P='http://schemas.openxmlformats.org/presentationml/2006/main';A='http://schemas.openxmlformats.org/drawingml/2006/main';R='http://schemas.openxmlformats.org/officeDocument/2006/relationships';PK='http://schemas.openxmlformats.org/package/2006/relationships'
ns={'p':P,'a':A,'r':R}
def ser(x):return E.tostring(x,xml_declaration=True,encoding='UTF-8',standalone=True)
def textcolor(c):return any(E.QName(a).localname in ('rPr','defRPr','endParaRPr') for a in c.iterancestors())
def position(s,x,y,w,h):
 xf=s.find('p:spPr/a:xfrm',ns)
 for tag,vals in [('off',{'x':x,'y':y}),('ext',{'cx':w,'cy':h})]:
  for k,v in vals.items():xf.find('a:'+tag,ns).set(k,str(round(v*9525)))
def typography(s,size=None,color=None,align=None):
 for r in s.xpath('.//a:rPr|.//a:defRPr|.//a:endParaRPr',namespaces=ns):
  if size:r.set('sz',str(round(size*75)))
  if color:
   for e in r.findall('a:solidFill',ns):r.remove(e)
   f=E.Element('{'+A+'}solidFill');E.SubElement(f,'{'+A+'}srgbClr',val=color);r.insert(1 if len(r) and E.QName(r[0]).localname=='ln' else 0,f)
 if align:
  for p in s.findall('.//a:p',ns):
   pp=p.find('a:pPr',ns)
   if pp is None:pp=E.Element('{'+A+'}pPr');p.insert(0,pp)
   pp.set('algn',align)
def circle(s,x,y,d,color):
 position(s,x,y,d,d);sp=s.find('p:spPr',ns)
 for e in list(sp):
  if E.QName(e).localname in ('prstGeom','custGeom','solidFill','noFill','ln'):sp.remove(e)
 g=E.SubElement(sp,'{'+A+'}prstGeom',prst='ellipse');E.SubElement(g,'{'+A+'}avLst')
 E.SubElement(E.SubElement(sp,'{'+A+'}solidFill'),'{'+A+'}srgbClr',val=color)
 E.SubElement(E.SubElement(sp,'{'+A+'}ln',w='19050'),'{'+A+'}solidFill').append(E.Element('{'+A+'}srgbClr',val=color))
 bp=s.find('p:txBody/a:bodyPr',ns);bp.set('anchor','ctr');bp.set('lIns','0');bp.set('rIns','0');bp.set('tIns','0');bp.set('bIns','0')
 typography(s,48,'F3F0E2','ctr')
with zipfile.ZipFile(sys.argv[1]) as src,zipfile.ZipFile(sys.argv[2]) as art:
 data={n:src.read(n) for n in src.namelist()};bgs={}
 for i,theme in enumerate(('hero','content'),1):
  bg=E.fromstring(art.read(f'ppt/slides/slide{i}.xml')).find('.//p:pic',ns)
  ar=E.fromstring(art.read(f'ppt/slides/_rels/slide{i}.xml.rels'));rid=bg.find('.//a:blip',ns).get('{'+R+'}embed')
  target=next(r.get('Target') for r in ar if r.get('Id')==rid)
  part=posixpath.normpath(posixpath.join('ppt/slides',target)).lstrip('/')
  data[f'ppt/media/research-{theme}.png']=art.read(part);bgs[theme]=bg
 colors=['5D818B','A65A43','414548','A47A3E','5D818B']
 for name in list(data):
  if not (re.fullmatch(r'ppt/slides/slide\d+\.xml',name) or ('/charts/' in name and name.endswith('.xml'))):continue
  root=E.fromstring(data[name]);n=int(re.search(r'slide(\d+)\.xml',name)[1]) if '/charts/' not in name else 0
  palette={'293B4B':'F3F0E2','344B5E':'E1E5DD','3C5364':'ECEBDD','1F303E':'5D818B','D2AB7D':'A65A43','F1EBDD':'414548','FFFFFF':'414548','BDCBCD':'686B67','B6D4DF':'686B67','A9C1CC':'5D818B','A9BDC6':'5D818B','617888':'ACAFA6','63E1E8':'A65A43'}
  for c in root.findall('.//a:srgbClr',ns):
   old=c.get('val','').upper()
   if old in palette:c.set('val',palette[old])
  for c in root.findall('.//a:schemeClr',ns):
   if c.get('val') in ('bg1','lt1') and textcolor(c):c.tag='{'+A+'}srgbClr';c.set('val','414548')
  for tbl in root.findall('.//a:tbl',ns):
   for c in tbl.find('a:tr',ns).findall('.//a:srgbClr',ns):
    if textcolor(c):c.set('val','F3F0E2')
  if n:
   tree=root.find('p:cSld/p:spTree',ns)
   for pic in list(tree.findall('p:pic',ns)):
    ext=pic.find('p:spPr/a:xfrm/a:ext',ns)
    if ext is not None and int(ext.get('cx'))>=18000000 and int(ext.get('cy'))>=10000000:tree.remove(pic)
   theme='hero' if n in (1,3,5,9,16,22,24) else 'content'
   pic=copy.deepcopy(bgs[theme]);pic.find('p:nvPicPr/p:cNvPr',ns).set('id','2000');pic.find('.//a:blip',ns).set('{'+R+'}embed','rIdResearchBg');tree.insert(2,pic)
   relname=f'ppt/slides/_rels/slide{n}.xml.rels';rels=E.fromstring(data[relname]);E.SubElement(rels,'{'+PK+'}Relationship',Id='rIdResearchBg',Type=R+'/image',Target=f'../media/research-{theme}.png');data[relname]=ser(rels)
   shapes=tree.findall('p:sp',ns)
   for s in shapes:
    if re.fullmatch(r'\d{2} / 24',''.join(s.xpath('.//a:t/text()',namespaces=ns))):position(s,1510,1018,140,34);typography(s,22,'414548')
   byid={s.find('p:nvSpPr/p:cNvPr',ns).get('id'):s for s in shapes}
   # Transform existing numbered content into editable infographic structures.
   if n==2:
    for i in range(5):
     x=125+i*342;circle(byid[str(5+2*i)],x+78,420,150,colors[i])
     position(byid[str(6+2*i)],x,605,306,240);typography(byid[str(6+2*i)],36,None,'ctr')
   if n in (4,6):
    pts=[(260,335),(125,600),(395,600)]
    for i,(x,y) in enumerate(pts):
     circle(byid[str(4+i*2)],x,y,210,colors[i])
     position(byid[str(5+i*2)],770,330+i*190,990,165);typography(byid[str(5+i*2)],36,colors[i])
   if n==7:
    for i in range(4):
     x=115+i*425;circle(byid[str(4+2*i)],x+115,370,160,colors[i])
     position(byid[str(5+2*i)],x,575,390,240);typography(byid[str(5+2*i)],36,None,'ctr')
   if n==20:
    for i in range(3):
     circle(byid[str(5+2*i)],150,515+i*107,75,colors[i]);typography(byid[str(5+2*i)],30,'F3F0E2','ctr')
     position(byid[str(6+2*i)],255,510+i*107,1290,90)
   # Diagram nodes alternate the muted reference colors without changing relationships.
   if n in (11,12,14,15):
    count=0
    for s in shapes:
     fill=s.find('p:spPr/a:solidFill/a:srgbClr',ns)
     if fill is not None and fill.get('val')=='E1E5DD':
      fill.set('val',colors[count%3]);typography(s,None,'F3F0E2');count+=1
  data[name]=ser(root)
 for n in range(1,25):
  name=f'ppt/slides/slide{n}.xml'
  assert E.fromstring(src.read(name)).xpath('//a:t/text()',namespaces=ns)==E.fromstring(data[name]).xpath('//a:t/text()',namespaces=ns)
 for name in data:
  if name.startswith('ppt/notesSlides/') or name.startswith('ppt/embeddings/'):assert data[name]==src.read(name)
 with zipfile.ZipFile(sys.argv[3],'w',zipfile.ZIP_DEFLATED) as dst:
  for name,b in data.items():dst.writestr(name,b)
 print('24 slides restyled; exact texts, notes, data and animations preserved.')
