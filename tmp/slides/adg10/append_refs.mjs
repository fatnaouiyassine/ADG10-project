import fs from 'node:fs/promises';
import {execFileSync} from 'node:child_process';
import {pathToFileURL} from 'node:url';
import {Presentation,PresentationFile,FileBlob} from '@oai/artifact-tool';
const ROOT=process.cwd(),TMP=ROOT+'/tmp/slides/adg10-refs',SOURCE='C:/Users/yassine/Downloads/Presentation_ADG10.pptx';
const SKILL='C:/Users/yassine/.codex/plugins/cache/openai-primary-runtime/presentations/26.915.20218/skills/presentations';
const PY='C:/Users/yassine/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe';
process.env.RUNTIME_NODE_MODULES='C:/Users/yassine/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
await fs.mkdir(TMP,{recursive:true});
if(process.argv[2]==='inspect'){
 const p=await PresentationFile.importPptx(await FileBlob.load(SOURCE));
 await fs.writeFile(TMP+'/source-inspect.ndjson',(await p.inspect({kind:'slide,layout',maxChars:40000})).ndjson);
 for(const n of [4,22]){const b=await p.export({slide:p.slides.items[n-1],format:'png',scale:.75});await fs.writeFile(TMP+`/source-${n}.png`,new Uint8Array(await b.arrayBuffer()));}
}else{
 const p=Presentation.create({slideSize:{width:1920,height:1080}});
 function tx(s,t,x,y,w,h,size,bold=false,color='#F1EBDD'){let a=s.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});a.text=t;a.text.style={typeface:'Calibri',fontSize:size,bold,color,verticalAlignment:'middle',autoFit:'none',insets:{left:0,right:0,top:0,bottom:0}};}
 const refs=[['Python','https://docs.python.org/3/'],['Airtable Web API','https://airtable.com/developers/web/api/introduction'],['Groq','https://console.groq.com/docs/overview'],['Streamlit','https://docs.streamlit.io/'],['ReportLab','https://docs.reportlab.com/']];
 for(let i=0;i<2;i++){let s=p.slides.add();s.background.fill='#293B4B';tx(s,'ADG-10  /  AUTOMATISATION DU CYCLE COMMERCIAL',100,42,1570,45,24,true,'#D2AB7D');tx(s,`${23+i} / 24`,1660,1007,145,40,26,true);}
 let s=p.slides.items[0];tx(s,'Références',100,132,1660,110,62,true,'#FFFFFF');
 refs.forEach(([name,url],i)=>{tx(s,name,145,310+i*103,440,66,36,true,'#D2AB7D');tx(s,url,585,310+i*103,1170,66,32);});
 tx(s,'Documentation interne : rapport de stage et code source du projet ADG-10.',145,865,1620,65,32);
 s.speakerNotes.textFrame.setText('Références techniques du projet.\n'+refs.map(x=>x.join(' : ')).join('\n')+'\nDocumentation interne : rapport de stage et code source ADG-10.');
 s=p.slides.items[1];tx(s,'Merci pour\nvotre attention',100,360,1120,245,96,true,'#FFFFFF');tx(s,'Questions et échanges',105,665,1000,85,44,false,'#D2AB7D');
 s.speakerNotes.textFrame.setText('Je vous remercie pour votre attention. Je suis à votre disposition pour répondre à vos questions.');
 await(await PresentationFile.exportPptx(p)).save(TMP+'/new-slides.pptx');
 execFileSync(PY,[ROOT+'/tmp/slides/adg10/merge_refs.py',SOURCE,TMP+'/new-slides.pptx',TMP+'/candidate.pptx']);
 const {finalizePresentation}=await import(pathToFileURL(SKILL+'/container_tools/artifact_tool_utils.mjs'));
 const finalPath=ROOT+'/output/presentations/Presentation_ADG10_References_Merci.pptx';
 await finalizePresentation({workspaceDir:ROOT,candidatePath:TMP+'/candidate.pptx',finalPath,pythonExecutable:PY,integrityValidatorPath:SKILL+'/container_tools/inspect_presentation_package_integrity.py',layoutValidatorPath:SKILL+'/container_tools/inspect_presentation_layout_geometry.py',layoutArgs:['--expected-slide-size-emu','18288000,10287000','--validate-bullet-geometry',...[8,10,17,21].flatMap(n=>['--require-native-table-slide',String(n)])],explicitTotalSlideCount:24,requiredNativeTableOwnerSlides:[8,10,17,21],requiredNativeChartOwnerSlides:[13],fontPolicy:{basis:'design',families:['Calibri']},verifyArtifactToolImport:true,receiptPath:TMP+'/validation.json'});
 const final=await PresentationFile.importPptx(await FileBlob.load(finalPath));
 for(let n=1;n<=24;n++){let b=await final.export({slide:final.slides.items[n-1],format:'png',scale:.75});await fs.writeFile(TMP+`/final-${n}.png`,new Uint8Array(await b.arrayBuffer()));console.log('Rendered',n);}
}
