import sys,zipfile,re
from lxml import etree as E
P='http://schemas.openxmlformats.org/presentationml/2006/main'
A='http://schemas.openxmlformats.org/drawingml/2006/main'
ns={'p':P,'a':A}
slate=len(sys.argv)>3 and sys.argv[3]=='slate'
def el(tag,**attrs):return E.Element('{'+P+'}'+tag,**{k:str(v) for k,v in attrs.items()})
def add(parent,tag,**attrs):x=el(tag,**attrs);parent.append(x);return x
with zipfile.ZipFile(sys.argv[1]) as src,zipfile.ZipFile(sys.argv[2],'w',zipfile.ZIP_DEFLATED) as dst:
 for item in src.infolist():
  data=src.read(item.filename)
  if re.fullmatch(r'ppt/slides/slide\d+\.xml',item.filename):
   root=E.fromstring(data)
   for old in root.findall('p:transition',ns)+root.findall('p:timing',ns):root.remove(old)
   trans=el('transition',spd='med',advClick='1');add(trans,'push',dir='l') if slate else add(trans,'fade')
   timing=el('timing');lst=add(timing,'tnLst');par=add(lst,'par');rtn=add(par,'cTn',id='1',dur='indefinite',restart='never',nodeType='tmRoot');children=add(rtn,'childTnLst')
   seq=add(children,'seq',concurrent='1',nextAc='seek');main=add(seq,'cTn',id='2',dur='indefinite',nodeType='mainSeq');mainlst=add(main,'childTnLst')
   # Automatic entrance fades on editable text. Keep diagrams/connectors visible as a unit.
   targets=[]
   for sp in root.findall('.//p:spTree/p:sp',ns):
    txt=''.join(sp.xpath('.//a:t/text()',namespaces=ns));off=sp.find('p:spPr/a:xfrm/a:off',ns)
    if off is None or not txt.strip():continue
    y=int(off.get('y','0'))/9525
    if 120<=y<940:targets.append(sp.find('p:nvSpPr/p:cNvPr',ns).get('id'))
   slide=int(re.search(r'slide(\d+)',item.filename)[1])
   if slide in (11,12,14,15):targets=targets[:1]
   idx=3
   for j,target in enumerate(targets):
    outer=add(mainlst,'par');ct=add(outer,'cTn',id=idx,fill='hold');idx+=1
    cond=add(ct,'stCondLst');add(cond,'cond',delay=100+min(j,7)*90)
    inner=add(add(ct,'childTnLst'),'par');effect=add(inner,'cTn',id=idx,presetID='22' if slate else '10',presetClass='entr',presetSubtype='1' if slate else '0',fill='hold',nodeType='withEffect');idx+=1
    add(add(effect,'stCondLst'),'cond',delay='0');behaviors=add(effect,'childTnLst')
    vis=add(behaviors,'set');bh=add(vis,'cBhvr');add(bh,'cTn',id=idx,dur='1',fill='hold');idx+=1
    add(add(bh,'tgtEl'),'spTgt',spid=target);add(add(bh,'attrNameLst'),'attrName').text='style.visibility';add(add(vis,'to'),'strVal',val='visible')
    fade=add(behaviors,'animEffect',transition='in',filter='wipe(right)' if slate else 'fade');bh=add(fade,'cBhvr');add(bh,'cTn',id=idx,dur='550' if slate else '450',fill='hold');idx+=1;add(add(bh,'tgtEl'),'spTgt',spid=target)
   add(add(seq,'prevCondLst'),'cond',evt='onPrev',delay='0').append(el('tgtEl'));seq[-1][0][0].append(el('sldTgt'))
   add(add(seq,'nextCondLst'),'cond',evt='onNext',delay='0').append(el('tgtEl'));seq[-1][0][0].append(el('sldTgt'))
   pos=len(root)
   ext=root.find('p:extLst',ns)
   if ext is not None:pos=list(root).index(ext)
   root.insert(pos,trans);root.insert(pos+1,timing)
   data=E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
  dst.writestr(item,data)
