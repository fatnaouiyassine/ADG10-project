import fs from 'node:fs/promises';
import sharp from 'sharp';
import {FileBlob,PresentationFile} from '@oai/artifact-tool';
const dir='tmp/slides/adg10';
const p=await PresentationFile.importPptx(await FileBlob.load('output/presentations/Presentation_ADG10_Yassine_Fatnaoui.pptx'));
let seconds=0;
for(let i=0;i<p.slides.items.length;i++){
 const s=p.slides.items[i];const b=await p.export({slide:s,format:'png',scale:.75});
 const file=`${dir}/verified-${i+1}.png`;await fs.writeFile(file,new Uint8Array(await b.arrayBuffer()));
 const a=await sharp(`${dir}/final-${i+1}.png`).raw().toBuffer(),c=await sharp(file).raw().toBuffer();
 let delta=0;for(let j=0;j<a.length;j++)delta+=Math.abs(a[j]-c[j]);
 console.log(i+1,'mean pixel change',delta/a.length);
}
const inspect=await p.inspect({kind:'notes,slide',maxChars:150000});
await fs.writeFile(dir+'/verified-notes.ndjson',inspect.ndjson);
console.log('22 final slides rendered.');
