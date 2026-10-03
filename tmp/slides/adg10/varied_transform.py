import zipfile, sys, posixpath, hashlib
from lxml import etree as E
R='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
ns={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':R}
slides=[3,5,9,16,22,24]
with zipfile.ZipFile(sys.argv[1]) as src, zipfile.ZipFile(sys.argv[2]) as art:
    data={n:src.read(n) for n in src.namelist()}
    hashes=[]
    for i,n in enumerate(slides,1):
        bg=E.fromstring(art.read(f'ppt/slides/slide{i}.xml')).find('.//p:pic',ns)
        rels=E.fromstring(art.read(f'ppt/slides/_rels/slide{i}.xml.rels'))
        rid=bg.find('.//a:blip',ns).get('{'+R+'}embed')
        target=next(r.get('Target') for r in rels if r.get('Id')==rid)
        part=posixpath.normpath(posixpath.join('ppt/slides',target)).lstrip('/')
        new=f'ppt/media/subject-slide-{n}.png'
        data[new]=art.read(part)
        hashes.append(hashlib.sha256(data[new]).hexdigest())
        rn=f'ppt/slides/_rels/slide{n}.xml.rels'
        rels=E.fromstring(data[rn])
        next(r for r in rels if r.get('Id')=='rIdWorkflowBg').set('Target',f'../media/subject-slide-{n}.png')
        data[rn]=E.tostring(rels,xml_declaration=True,encoding='UTF-8',standalone=True)
        note=f'ppt/notesSlides/notesSlide{n}.xml'
        if note in data:
            root=E.fromstring(data[note])
            body=root.find('.//p:sp[p:nvSpPr/p:nvPr/p:ph[@type="body"]]/p:txBody',ns) if False else None
            for sp in root.findall('.//p:sp',ns):
                ph=sp.find('p:nvSpPr/p:nvPr/p:ph',ns)
                if ph is not None and ph.get('type')=='body':body=sp.find('p:txBody',ns)
            if body is not None:
                para=E.SubElement(body,'{'+ns['a']+'}p')
                run=E.SubElement(para,'{'+ns['a']+'}r')
                E.SubElement(run,'{'+ns['a']+'}t').text='Icône : Lucide, https://lucide.dev/ ; licence ISC. Illustration thématique.'
                data[note]=E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
    assert len(set(hashes))==6
    for n in range(1,25):
        part=f'ppt/slides/slide{n}.xml'
        assert src.read(part)==data[part]
    with zipfile.ZipFile(sys.argv[3],'w',zipfile.ZIP_DEFLATED) as dst:
        for n,b in data.items():dst.writestr(n,b)
    print('24 slide XMLs unchanged. Six unique illustrations embedded. Notes, charts, tables and effects retained.')
