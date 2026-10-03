import sharp from 'sharp';
import fs from 'node:fs/promises';
const prefix=process.argv[2]||'source';const dir='tmp/slides/adg10';
const files=(await fs.readdir(dir)).filter(x=>new RegExp('^'+prefix+'-\\d+\\.png$').test(x)).sort((a,b)=>parseInt(a.split('-')[1])-parseInt(b.split('-')[1]));
for(let i=0;i<files.length;i+=6){const parts=[];for(let j=0;j<Math.min(6,files.length-i);j++)parts.push({input:await sharp(dir+'/'+files[i+j]).resize(640,360,{fit:'contain'}).png().toBuffer(),left:(j%2)*650,top:Math.floor(j/2)*370});await sharp({create:{width:1290,height:Math.ceil(Math.min(6,files.length-i)/2)*370,channels:3,background:'#dddddd'}}).composite(parts).png().toFile(`${dir}/${prefix}-sheet-${Math.floor(i/6)+1}.png`);}
