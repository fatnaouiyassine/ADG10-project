import zipfile,sys,re,copy,posixpath
from lxml import etree as E
P='http://schemas.openxmlformats.org/presentationml/2006/main';A='http://schemas.openxmlformats.org/drawingml/2006/main';R='http://schemas.openxmlformats.org/officeDocument/2006/relationships';PK='http://schemas.openxmlformats.org/package/2006/relationships'
ns={'p':P,'a':A,'r':R}
def ser(x):return E.tostring(x,xml_declaration=True,encoding='UTF-8',standalone=True)
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
with zipfile.ZipFile(sys.argv[1]) as src,zipfile.ZipFile(sys.argv[2]) as art:
 data={n:src.read(n) for n in src.namelist()}
 bg=E.fromstring(art.read('ppt/slides/slide1.xml')).find('.//p:pic',ns)
 ar=E.fromstring(art.read('ppt/slides/_rels/slide1.xml.rels'));rid=bg.find('.//a:blip',ns).get('{'+R+'}embed')
 target=next(r.get('Target') for r in ar if r.get('Id')==rid)
 part=posixpath.normpath(posixpath.join('ppt/slides',target)).lstrip('/')
 data['ppt/media/workflow-background.png']=art.read(part)
 for n in range(1,25):
  name=f'ppt/slides/slide{n}.xml';root=E.fromstring(data[name]);tree=root.find('p:cSld/p:spTree',ns)
  if n in (1,3,5,9,16,22,24):
   pic=next(p for p in tree.findall('p:pic',ns) if p.find('p:nvPicPr/p:cNvPr',ns).get('id')=='2000')
   pic.find('.//a:blip',ns).set('{'+R+'}embed','rIdWorkflowBg')
   pic.find('p:nvPicPr/p:cNvPr',ns).set('descr','Illustration conceptuelle du suivi des prospects, des échanges et des documents commerciaux')
   rn=f'ppt/slides/_rels/slide{n}.xml.rels';rels=E.fromstring(data[rn]);E.SubElement(rels,'{'+PK+'}Relationship',Id='rIdWorkflowBg',Type=R+'/image',Target='../media/workflow-background.png');data[rn]=ser(rels)
  shapes=tree.findall('p:sp',ns);byid={s.find('p:nvSpPr/p:cNvPr',ns).get('id'):s for s in shapes}
  for s in shapes:
   txt=''.join(s.xpath('.//a:t/text()',namespaces=ns))
   if re.fullmatch(r'\d{2} / 24',txt):typography(s,22,'414548','ctr')
  if n==1:
   for p in tree.findall('p:pic',ns):
    xf=p.find('p:spPr/a:xfrm',ns)
    if p.find('p:nvPicPr/p:cNvPr',ns).get('id')!='2000':xf.find('a:off',ns).set('y',str(145*9525))
   for s in shapes:
    txt=''.join(s.xpath('.//a:t/text()',namespaces=ns))
    if txt.startswith('SOUTENANCE'):position(s,105,275,1100,65)
    elif txt=='ADG-10':position(s,100,360,1020,165)
    elif txt.startswith('Automatisation'):position(s,105,535,1080,165)
    elif txt.startswith('Présenté'):position(s,105,760,1090,100)
    elif txt.startswith('Encadré'):position(s,105,860,1090,125)
    elif txt.startswith('Année'):position(s,105,1018,900,34);typography(s,22)
  if n in (4,6):
   for i in range(3):
    position(byid[str(4+2*i)],150,345+i*190,100,100);typography(byid[str(4+2*i)],34)
    position(byid[str(5+2*i)],310,315+i*190,1370,160);typography(byid[str(5+2*i)],38,'414548')
  if n==2:
   for i in range(5):
    position(byid[str(5+2*i)],215+i*342,410,120,120);typography(byid[str(5+2*i)],40)
    s=byid[str(6+2*i)];position(s,125+i*342,565,306,240);s.find('p:txBody/a:bodyPr',ns).set('anchor','t')
  if n==7:
   for i in range(4):
    position(byid[str(4+2*i)],240+i*425,370,140,140);typography(byid[str(4+2*i)],40)
    s=byid[str(5+2*i)];position(s,115+i*425,560,390,240);s.find('p:txBody/a:bodyPr',ns).set('anchor','t')
  if n in (11,12,14,15):
   for s in shapes:
    f=s.find('p:spPr/a:solidFill/a:srgbClr',ns)
    if f is not None and f.get('val') in ('5D818B','A65A43','414548'):
     f.set('val','E1E5DD');typography(s,None,'414548')
     for c in s.findall('p:spPr/a:ln/a:solidFill/a:srgbClr',ns):c.set('val','5D818B')
  data[name]=ser(root)
  assert E.fromstring(src.read(name)).xpath('//a:t/text()',namespaces=ns)==root.xpath('//a:t/text()',namespaces=ns)
 with zipfile.ZipFile(sys.argv[3],'w',zipfile.ZIP_DEFLATED) as dst:
  for name,b in data.items():dst.writestr(name,b)
 print('All 24 slide texts preserved; triangle backgrounds replaced; layouts aligned.')
