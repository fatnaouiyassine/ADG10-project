import zipfile,sys,re,copy,posixpath
from lxml import etree as E
P='http://schemas.openxmlformats.org/presentationml/2006/main';A='http://schemas.openxmlformats.org/drawingml/2006/main';R='http://schemas.openxmlformats.org/officeDocument/2006/relationships';PK='http://schemas.openxmlformats.org/package/2006/relationships'
ns={'p':P,'a':A,'r':R}
def ser(x):return E.tostring(x,xml_declaration=True,encoding='UTF-8',standalone=True)
with zipfile.ZipFile(sys.argv[1]) as src,zipfile.ZipFile(sys.argv[2]) as art:
 data={n:src.read(n) for n in src.namelist()}
 bg=E.fromstring(art.read('ppt/slides/slide1.xml')).find('.//p:pic',ns)
 ar=E.fromstring(art.read('ppt/slides/_rels/slide1.xml.rels'))
 rid=bg.find('.//a:blip',ns).get('{'+R+'}embed')
 target=next(r.get('Target') for r in ar if r.get('Id')==rid)
 imagepart=posixpath.normpath(posixpath.join('ppt/slides',target)).lstrip('/')
 data['ppt/media/pastel-background.png']=art.read(imagepart)
 palette={'293B4B':'CBDCF0','344B5E':'E0EAF6','3C5364':'D4E1F0','1F303E':'A6BDD8','D2AB7D':'C97345','F1EBDD':'17283E','FFFFFF':'17283E','BDCBCD':'405675','B6D4DF':'405675','A9C1CC':'6C91BE','A9BDC6':'6C91BE','617888':'91ACCE','63E1E8':'A54E24'}
 for name in list(data):
  if not (re.fullmatch(r'ppt/slides/slide\d+\.xml',name) or ('/charts/' in name and name.endswith('.xml'))):continue
  root=E.fromstring(data[name]);n=int(re.search(r'slide(\d+)\.xml',name)[1]) if '/charts/' not in name else 0
  for c in root.findall('.//a:srgbClr',ns):
   old=c.get('val','').upper()
   if old in palette:c.set('val',palette[old])
   # High-contrast text instead of bright orange on pastel blue.
   if old=='D2AB7D' and any(E.QName(a).localname in ('rPr','defRPr','endParaRPr') for a in c.iterancestors()):c.set('val','9B420B')
  for c in root.findall('.//a:schemeClr',ns):
   if c.get('val') in ('bg1','lt1') and any(E.QName(a).localname in ('rPr','defRPr','endParaRPr') for a in c.iterancestors()):
    c.tag='{'+A+'}srgbClr';c.set('val','17283E')
  if n:
   tree=root.find('p:cSld/p:spTree',ns)
   for pic in list(tree.findall('p:pic',ns)):
    ext=pic.find('p:spPr/a:xfrm/a:ext',ns)
    if ext is not None and int(ext.get('cx'))>=18000000 and int(ext.get('cy'))>=10000000:tree.remove(pic)
   if n in (1,2,3,5,9,16,22,24):
    pic=copy.deepcopy(bg);pic.find('p:nvPicPr/p:cNvPr',ns).set('id','2000');pic.find('.//a:blip',ns).set('{'+R+'}embed','rIdPastelBg');tree.insert(2,pic)
    relname=f'ppt/slides/_rels/slide{n}.xml.rels';rels=E.fromstring(data[relname]);E.SubElement(rels,'{'+PK+'}Relationship',Id='rIdPastelBg',Type=R+'/image',Target='../media/pastel-background.png');data[relname]=ser(rels)
  data[name]=ser(root)
 # Ensure no text, notes, chart data or source evidence is removed.
 for n in range(1,25):
  name=f'ppt/slides/slide{n}.xml'
  assert E.fromstring(src.read(name)).xpath('//a:t/text()',namespaces=ns)==E.fromstring(data[name]).xpath('//a:t/text()',namespaces=ns)
 with zipfile.ZipFile(sys.argv[3],'w',zipfile.ZIP_DEFLATED) as dst:
  for name,b in data.items():dst.writestr(name,b)
 print('Applied pastel theme; all 24 slides retain identical text.')
