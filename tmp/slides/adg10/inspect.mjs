import fs from 'node:fs/promises';
import {FileBlob, PresentationFile} from '@oai/artifact-tool';
const dir='C:/Users/yassine/Downloads/Re__Séances_d’encadrement';
const name=(await fs.readdir(dir)).find(x=>x.normalize('NFC')==='Présentation_Stage_PFA.pptx');
const p=await PresentationFile.importPptx(await FileBlob.load(dir+'/'+name));
await fs.writeFile('tmp/slides/adg10/source.json',JSON.stringify(p.toProto()));
const snap=await p.inspect({kind:'slide,textbox,shape,image,layout',maxChars:100000});
await fs.writeFile('tmp/slides/adg10/inspect.ndjson',snap.ndjson);
console.log(snap.ndjson);
console.log('MASTERS',p.masters.items.map(x=>({id:x.id,name:x.name})));
for(let i=0;i<p.slides.items.length;i++){
 const slide=p.slides.items[i];
 const img=await p.export({slide,format:'png',scale:1});
 await fs.writeFile(`tmp/slides/adg10/source-${i+1}.png`,new Uint8Array(await img.arrayBuffer()));
}
