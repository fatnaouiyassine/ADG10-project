import fs from 'node:fs/promises';
import {execFileSync} from 'node:child_process';
import {pathToFileURL} from 'node:url';
import {Presentation,PresentationFile,FileBlob} from '@oai/artifact-tool';
import sharp from 'sharp';
const ROOT=process.cwd(),TMP=ROOT+'/tmp/slides/adg10-varied';
const SKILL='C:/Users/yassine/.codex/plugins/cache/openai-primary-runtime/presentations/26.915.20218/skills/presentations';
const PY='C:/Users/yassine/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe';
process.env.RUNTIME_NODE_MODULES='C:/Users/yassine/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
await fs.mkdir(TMP,{recursive:true});
const assets=[{slide:3,name:'handshake'},{slide:5,name:'calendar-clock'},{slide:9,name:'network'},{slide:16,name:'laptop'},{slide:22,name:'puzzle'},{slide:24,name:'messages-square'}];
const p=Presentation.create({slideSize:{width:1920,height:1080}});
const backgrounds=Presentation.create({slideSize:{width:1920,height:1080}});
for(const a of assets){
 const s=p.slides.add();
 s.images.add({blob:new Uint8Array(await fs.readFile(ROOT+'/tmp/slides/adg10-research/content.png')),contentType:'image/png',alt:'Fond ivoire original',fit:'cover',position:{left:0,top:0,width:1920,height:1080}});
 const source=await fs.readFile(TMP+`/icons/${a.name}.svg`,'utf8');
 const styled=source.replace('stroke="currentColor"','stroke="#5D818B"').replace('stroke-width="2"','stroke-width="1.15"');
 const png=await sharp(Buffer.from(styled),{density:2400}).resize(600,600).png().toBuffer();
 s.images.add({blob:new Uint8Array(png),contentType:'image/png',alt:a.name,fit:'contain',position:{left:1300,top:330,width:390,height:390}});
 const rendered=await p.export({slide:s,format:'png',scale:1});
 const bytes=new Uint8Array(await rendered.arrayBuffer());
 await fs.writeFile(TMP+`/subject-${a.slide}.png`,bytes);
 const b=backgrounds.slides.add();
 b.images.add({blob:bytes,contentType:'image/png',alt:a.name,fit:'cover',position:{left:0,top:0,width:1920,height:1080}});
}
await(await PresentationFile.exportPptx(backgrounds)).save(TMP+'/backgrounds.pptx');
execFileSync(PY,[ROOT+'/tmp/slides/adg10/varied_transform.py',ROOT+'/output/presentations/Presentation_ADG10_Design_Organise.pptx',TMP+'/backgrounds.pptx',TMP+'/candidate.pptx'],{stdio:'inherit'});
const {finalizePresentation}=await import(pathToFileURL(SKILL+'/container_tools/artifact_tool_utils.mjs'));
const finalPath=ROOT+'/output/presentations/Presentation_ADG10_Visuels_Par_Theme.pptx';
await finalizePresentation({workspaceDir:ROOT,candidatePath:TMP+'/candidate.pptx',finalPath,pythonExecutable:PY,integrityValidatorPath:SKILL+'/container_tools/inspect_presentation_package_integrity.py',layoutValidatorPath:SKILL+'/container_tools/inspect_presentation_layout_geometry.py',layoutArgs:['--expected-slide-size-emu','18288000,10287000','--validate-bullet-geometry',...[8,10,17,21].flatMap(n=>['--require-native-table-slide',String(n)])],explicitTotalSlideCount:24,requiredNativeTableOwnerSlides:[8,10,17,21],requiredNativeChartOwnerSlides:[13],fontPolicy:{basis:'design',families:['Calibri']},verifyArtifactToolImport:true,receiptPath:TMP+'/validation.json'});
const final=await PresentationFile.importPptx(await FileBlob.load(finalPath));
for(let n=1;n<=24;n++){const b=await final.export({slide:final.slides.items[n-1],format:'png',scale:.75});await fs.writeFile(TMP+`/final-${n}.png`,new Uint8Array(await b.arrayBuffer()));console.log('Rendered',n);}
