import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {execFileSync} from 'node:child_process';
import {alignedDiagrams} from './aligned_diagrams.mjs';
import {Presentation,PresentationFile,FileBlob} from '@oai/artifact-tool';
const ROOT=process.cwd(),TMP=path.join(ROOT,'tmp/slides/adg10-enhanced');
const SKILL='C:/Users/yassine/.codex/plugins/cache/openai-primary-runtime/presentations/26.915.20218/skills/presentations';
const PY='C:/Users/yassine/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe';
process.env.RUNTIME_NODE_MODULES='C:/Users/yassine/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const {finalizePresentation,applyPresentationChartFont}=await import(pathToFileURL(SKILL+'/container_tools/artifact_tool_utils.mjs'));
const p=Presentation.create({slideSize:{width:1920,height:1080}}),F='Calibri',GREEN='#008C9B',NAVY='#102B40';
const dark=new Set([1,2,3,5,9,16,22]);
const bg=new Uint8Array(await fs.readFile(ROOT+'/tmp/slides/adg10-redesign/assets/automation.png'));
const slide=n=>p.slides.items[n-1];
function text(n,s,x,y,w,h,size=42,bold=false,color=NAVY,align='left'){
 const a=slide(n).shapes.add({geometry:'textbox',name:s.slice(0,55),position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
 a.text=s;a.text.style={typeface:F,fontSize:size,bold,color:dark.has(n)&&color===NAVY?'#FFFFFF':color,alignment:align,verticalAlignment:'middle',autoFit:'none',wrap:'square',insets:{left:0,right:0,top:0,bottom:0}};return a;
}
for(let n=1;n<=22;n++){
 const s=p.slides.add();s.background.fill=dark.has(n)?'#081827':'#F7FAFC';
 s.images.add({blob:bg,contentType:'image/png',alt:'Fond illustratif du réseau d’automatisation',fit:'cover',position:dark.has(n)?{left:0,top:0,width:1920,height:1080}:{left:0,top:0,width:1920,height:280}});
 text(n,'ADG-10  /  AUTOMATISATION DU CYCLE COMMERCIAL',100,42,1570,45,24,true,'#63E1E8');
 text(n,String(n).padStart(2,'0')+' / 22',1660,1007,145,40,26,true,dark.has(n)?'#FFFFFF':NAVY,'right');
}
function title(n,s){return text(n,s,100,132,1660,110,62,true,'#FFFFFF');}
function foot(n,s){text(n,s,165,940,1510, sixty(),27,false,'#506778');}function sixty(){return 60;}
function page(n){}
function para(n,items,{x=195,y=365,w=1290,size=42,gap=138}={}){items.forEach((v,i)=>{text(n,String(i+1).padStart(2,'0'),x-70,y+i*gap,60,gap-15,28,true,GREEN);text(n,v,x,y+i*gap,w,gap-15,size);});}
function divider(n,t,sub){const names={3:'Introduction',5:'Contexte général\ndu projet',9:'Étude conceptuelle\nde la solution',16:'Réalisation et\nmise en œuvre',22:'Conclusion'};text(n,n===22?'05':String([3,5,9,16].indexOf(n)+1).padStart(2,'0'),90,150,700,195,158,true,'#63E1E8');text(n,names[n]||t,100,370,1030,210,78,true);text(n,sub,105,615,950,150,39);}
function box(n,s,x,y,w,h,size=35,geom='rect'){
 const a=slide(n).shapes.add({geometry:geom,name:s.slice(0,55),position:{left:x,top:y,width:w,height:h},fill:'#EAF5F7',line:{fill:GREEN,width:2}});a.text=s;a.text.style={typeface:F,fontSize:size,color:NAVY,alignment:'center',verticalAlignment:'middle',autoFit:'none',insets:{left:12,right:12,top:9,bottom:9}};return a;
}
function link(n,a,b,from='right',to='left'){return slide(n).shapes.connect(a,b,{kind:'straight',fromSide:from,toSide:to,line:{fill:GREEN,width:3},tail:{type:'triangle',width:'sm',length:'sm'}});}
function table(n,rows,x,y,w,h,widths,size=34){
 const t=slide(n).tables.add({rows:rows.length,columns:rows[0].length,left:x,top:y,width:w+130,height:h,values:rows,columnWidths:widths.map(v=>v*(w+130)/w)});
 t.borders.assign({fill:'#D2E3E9',width:1,style:'solid'});
 for(let r=0;r<rows.length;r++)for(let c=0;c<rows[0].length;c++){const a=t.getCell(r,c);a.fill=r===0?NAVY:r%2?'#EAF3F6':'#FFFFFF';a.text.style={typeface:F,fontSize:size,color:r===0?'#FFFFFF':NAVY,bold:r===0,verticalAlignment:'middle',insets:{left:20,right:20,top:12,bottom:12}};}return t;
}
async function pic(n,file,x,y,w,h,alt){slide(n).images.add({blob:new Uint8Array(await fs.readFile(path.join(ROOT,'tmp/pdfs/rapport-detaille/assets',file))),contentType:'image/png',alt,fit:'contain',position:{left:x,top:y,width:w,height:h}});}
function note(n,seconds,s,sources){slide(n).speakerNotes.textFrame.setText(`Durée indicative : ${seconds} secondes.\n\n${s}\n\nSources : ${sources}\nRéférence documentaire : Rapport de stage ADG-10, version du 17 septembre 2026.`);}
text(1,'SOUTENANCE DU PROJET DE FIN D’ANNÉE',105,220,1100,65, thirty(),true,'#B6D4DF');function thirty(){return 30;}
text(1,'ADG-10',95,335,1000,165,136,true);
text(1,'Automatisation du cycle\ncommercial des formations',105,520,1000,165,60,true);
text(1,'Présenté par Yassine FATNAOUI',105,780,1090,50,33);
text(1,'Encadrants\nAZOUGUIGH El Houssaine\nBAILOUL Charaf Eddine',105,845,1090,125,29);
text(1,'Année universitaire 2025-2026',105,1007,700,40,26,false,'#B6D4DF');
let source=await fs.readFile(ROOT+'/tmp/slides/adg10/build.mjs','utf8');
let content=source.slice(source.indexOf('note(1,25'),source.indexOf("await fs.mkdir(path.join(ROOT,'output/presentations')"));
content=content.replace("text(2,'Plan',310,218,750,105,70);","text(2,'Plan de la présentation',100,200,1100,105,70,true);");
content=content.replace(".forEach((s,i)=>text(2,s,383,[359,466,559,670,763][i],815,78,40));",".forEach((s,i)=>{text(2,String(i+1).padStart(2,'0'),105,355+i*110,90,78,36,true,'#63E1E8');text(2,s,220,355+i*110,900,78,42);});");
content=content.replace("slide(4).shapes.items.find(x=>x.name==='object 3').position={left:155,top:330,width:1387,height:615};",'');
content=content.replace("text(22,'Merci pour votre attention',280,786,1120,85,48,true,NAVY,'center');text(22,'Questions et échanges',280,881,1120,65,35,false,NAVY,'center');","text(22,'Merci pour votre attention',105,805,1000,85,44,true,'#63E1E8');text(22,'Questions et échanges',105,900,900,60,32);");
for(const n of [11,12,14,15]){
 const start=content.indexOf(`title(${n},`),end=content.indexOf(`note(${n},`,start);
 content=content.slice(0,start)+`alignedDiagrams(${n},{slide,text,title,foot,box,link,NAVY,GREEN,F});\n`+content.slice(end);
}
await eval('(async()=>{'+content+'})()');
const raw=TMP+'/raw.pptx';await(await PresentationFile.exportPptx(p)).save(raw);
const candidate=TMP+'/candidate.pptx';
execFileSync(PY,[ROOT+'/tmp/slides/adg10/add_effects.py',raw,candidate]);
const finalPath=ROOT+'/output/presentations/Presentation_ADG10_Harmonisee_Animee.pptx';
const result=await finalizePresentation({workspaceDir:ROOT,candidatePath:candidate,finalPath,pythonExecutable:PY,integrityValidatorPath:SKILL+'/container_tools/inspect_presentation_package_integrity.py',layoutValidatorPath:SKILL+'/container_tools/inspect_presentation_layout_geometry.py',layoutArgs:['--expected-slide-size-emu','18288000,10287000','--validate-bullet-geometry','--validate-heading-fit',...[8,10,17,21].flatMap(n=>['--require-native-table-slide',String(n)])],explicitTotalSlideCount:22,requiredNativeTableOwnerSlides:[8,10,17,21],requiredNativeChartOwnerSlides:[13],materializeLiteralChartWorkbooks:true,fontPolicy:{basis:'design',families:[F]},verifyArtifactToolImport:true,receiptPath:TMP+'/validation.json'});
console.log(JSON.stringify(result));
const final=await PresentationFile.importPptx(await FileBlob.load(finalPath));
for(let i=0;i<22;i++){const img=await final.export({slide:final.slides.items[i],format:'png',scale:.75});await fs.writeFile(`${TMP}/final-${i+1}.png`,new Uint8Array(await img.arrayBuffer()));console.log('Rendered',i+1);}
await fs.writeFile(TMP+'/inspection.ndjson',(await final.inspect({kind:'slide,textbox,notes',maxChars:250000})).ndjson);
