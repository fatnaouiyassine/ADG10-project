import fs from 'node:fs/promises';
import {execFileSync} from 'node:child_process';
import {pathToFileURL} from 'node:url';
import {Presentation,PresentationFile,FileBlob} from '@oai/artifact-tool';
const ROOT=process.cwd(),TMP=ROOT+'/tmp/slides/adg10-organized';
const SKILL='C:/Users/yassine/.codex/plugins/cache/openai-primary-runtime/presentations/26.915.20218/skills/presentations';
const PY='C:/Users/yassine/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe';
process.env.RUNTIME_NODE_MODULES='C:/Users/yassine/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
await fs.mkdir(TMP,{recursive:true});
const p=Presentation.create({slideSize:{width:1920,height:1080}});
for(const [theme,file] of [['hero','exec-f1b06a61-68d9-4e50-827b-e6d116fe2b13.png']]) {
 await fs.copyFile('C:/Users/yassine/.codex/generated_images/01a09bb9-0fc9-7712-8eda-3d341c3041c4/'+file,TMP+'/'+theme+'.png');
 const s=p.slides.add();
 s.images.add({blob:new Uint8Array(await fs.readFile(TMP+'/'+theme+'.png')),contentType:'image/png',alt:'Fond ivoire à motifs géométriques bleu grisé, terracotta et anthracite, illustration générée',fit:'cover',position:{left:0,top:0,width:1920,height:1080}});
}
await(await PresentationFile.exportPptx(p)).save(TMP+'/backgrounds.pptx');
execFileSync(PY,[ROOT+'/tmp/slides/adg10/organized_transform.py',ROOT+'/output/presentations/Presentation_ADG10_Infographie_Ivoire.pptx',TMP+'/backgrounds.pptx',TMP+'/candidate.pptx'],{stdio:'inherit'});
const {finalizePresentation}=await import(pathToFileURL(SKILL+'/container_tools/artifact_tool_utils.mjs'));
const finalPath=ROOT+'/output/presentations/Presentation_ADG10_Design_Organise.pptx';
await finalizePresentation({workspaceDir:ROOT,candidatePath:TMP+'/candidate.pptx',finalPath,pythonExecutable:PY,integrityValidatorPath:SKILL+'/container_tools/inspect_presentation_package_integrity.py',layoutValidatorPath:SKILL+'/container_tools/inspect_presentation_layout_geometry.py',layoutArgs:['--expected-slide-size-emu','18288000,10287000','--validate-bullet-geometry',...[8,10,17,21].flatMap(n=>['--require-native-table-slide',String(n)])],explicitTotalSlideCount:24,requiredNativeTableOwnerSlides:[8,10,17,21],requiredNativeChartOwnerSlides:[13],fontPolicy:{basis:'design',families:['Calibri']},verifyArtifactToolImport:true,receiptPath:TMP+'/validation.json'});
const final=await PresentationFile.importPptx(await FileBlob.load(finalPath));
for(let n=1;n<=24;n++){const b=await final.export({slide:final.slides.items[n-1],format:'png',scale:.75});await fs.writeFile(TMP+`/final-${n}.png`,new Uint8Array(await b.arrayBuffer()));console.log('Rendered',n);}


