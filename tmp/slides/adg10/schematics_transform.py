import zipfile,sys,posixpath,hashlib
from lxml import etree as E
R='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
ns={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':R}
with zipfile.ZipFile(sys.argv[1]) as src,zipfile.ZipFile(sys.argv[2]) as art:
 data={n:src.read(n) for n in src.namelist()}
 hashes=[]
 for i,n in enumerate([3,5,9,16,22,24],1):
  bg=E.fromstring(art.read(f'ppt/slides/slide{i}.xml')).find('.//p:pic',ns)
  rels=E.fromstring(art.read(f'ppt/slides/_rels/slide{i}.xml.rels'))
  rid=bg.find('.//a:blip',ns).get('{'+R+'}embed')
  target=next(r.get('Target') for r in rels if r.get('Id')==rid)
  part=posixpath.normpath(posixpath.join('ppt/slides',target)).lstrip('/')
  new=f'ppt/media/schematic-slide-{n}.png'
  data[new]=art.read(part)
  hashes.append(hashlib.sha256(data[new]).hexdigest())
  rn=f'ppt/slides/_rels/slide{n}.xml.rels'
  rels=E.fromstring(data[rn])
  next(r for r in rels if r.get('Id')=='rIdWorkflowBg').set('Target',f'../media/schematic-slide-{n}.png')
  data[rn]=E.tostring(rels,xml_declaration=True,encoding='UTF-8',standalone=True)
 assert len(set(hashes))==6
 for n in range(1,25):
  part=f'ppt/slides/slide{n}.xml'
  assert src.read(part)==data[part]
 with zipfile.ZipFile(sys.argv[3],'w',zipfile.ZIP_DEFLATED) as dst:
  for n,b in data.items():dst.writestr(n,b)
 print('Six distinct schematic backgrounds; all 24 slide XMLs, notes, tables, charts and effects unchanged.')
