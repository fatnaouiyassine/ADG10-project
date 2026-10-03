import fs from 'node:fs/promises';
const p=JSON.parse(await fs.readFile('tmp/slides/adg10/source.json','utf8'));
console.log(JSON.stringify(p.slides[0].elements.find(e=>e.name==='object 7'),null,2));
console.log(JSON.stringify(p.slides[9],null,2).slice(0,12000));
