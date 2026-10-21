// Verify author-approved visual assets; generate only silent local media and runtime files.
import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const at=(p)=>path.join(root,p);
const save=(p,bytes)=>{fs.mkdirSync(path.dirname(at(p)),{recursive:true});fs.writeFileSync(at(p),bytes);};
const manifest=JSON.parse(fs.readFileSync(at('config/assets.json'),'utf8'));
for(const item of manifest){
 if(!fs.existsSync(at(item.path)))throw new Error(`Bundled visual asset missing: ${item.path}. Restore the file from Git.`);
 const data=fs.readFileSync(at(item.path));
 if(createHash('sha256').update(data).digest('hex')!==item.sha256)throw new Error(`Visual asset differs from manifest: ${item.path}. Preserve intentional edits and update config/assets.json.`);
}
// Source offsets extend past 228s; a complete silent media timeline avoids seeking errors.
if(!fs.existsSync(at('assets/audio/demo-silence.wav'))){
 const rate=8000;const bytes=240*rate*2;const wav=Buffer.alloc(44+bytes);
 wav.write('RIFF');wav.writeUInt32LE(36+bytes,4);wav.write('WAVEfmt ',8);wav.writeUInt32LE(16,16);wav.writeUInt16LE(1,20);wav.writeUInt16LE(1,22);wav.writeUInt32LE(rate,24);wav.writeUInt32LE(rate*2,28);wav.writeUInt16LE(2,32);wav.writeUInt16LE(16,34);wav.write('data',36);wav.writeUInt32LE(bytes,40);save('assets/audio/demo-silence.wav',wav);
}
save('assets/vendor/gsap.min.js',fs.readFileSync(at('node_modules/gsap/dist/gsap.min.js')));
console.log(`Verified ${manifest.length} bundled visuals. Silent audio and GSAP 3.14.2 are ready locally; no original music downloaded.`);
