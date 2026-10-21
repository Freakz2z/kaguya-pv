// Audit only the distributable Git file set, and validate generated runtime dependencies.
import fs from 'node:fs';
import path from 'node:path';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const files=execFileSync('git',['ls-files','-z'],{cwd:root,encoding:'utf8'}).split('\0').filter(Boolean);
const problems=[];
const forbidden=/^(?:node_modules|\.venv[^/]*|__pycache__|\.hyperframes|\.thumbnails|\.private-preview|references|renders|qa|assets\/(?:audio|vendor))\//;
const excludedMedia=/\.(?:mp4|m4v|mov|mkv|avi|webm|mp3|wav|m4a|aac|ogg|opus|flac|aiff?|wma|alac|ttc|ttf|zip|7z|tar|gz)$/i;
const visuals=new Map(JSON.parse(fs.readFileSync(path.join(root,'config/assets.json'),'utf8')).map(row=>[row.path,row]));
for(const file of files){
 if(forbidden.test(file)||excludedMedia.test(file)||/(?:^|\/)\.env(?:\.|$)/.test(file))problems.push(`Excluded material tracked: ${file}`);
 const b=fs.readFileSync(path.join(root,file));
 if(/^(?:ID3|OggS|fLaC|RIFF|FORM)/.test(b.subarray(0,4).toString('ascii'))||b.subarray(4,8).toString('ascii')==='ftyp'||(b[0]===0xff&&(b[1]&0xe0)===0xe0))problems.push(`Possible audio/video payload: ${file}`);
 if(/^assets\/(?:art|covers)\//.test(file)){
  const row=visuals.get(file);
  if(!row)problems.push(`Visual not approved in manifest: ${file}`);
  else if(createHash('sha256').update(b).digest('hex')!==row.sha256)problems.push(`Visual SHA-256 mismatch: ${file}`);
  const magic=Buffer.from([137,80,78,71,13,10,26,10]);
  if(!b.subarray(0,8).equals(magic))problems.push(`Visual is not a PNG: ${file}`);
  else {
   if(row&&(b.readUInt32BE(16)!==row.width||b.readUInt32BE(20)!==row.height))problems.push(`Visual size mismatch: ${file}`);
   let offset=8,ended=false;
   while(offset+12<=b.length){const size=b.readUInt32BE(offset),type=b.subarray(offset+4,offset+8).toString('ascii');offset+=size+12;if(type==='IEND'){ended=offset===b.length;break;}}
   if(!ended)problems.push(`Malformed PNG or trailing payload: ${file}`);
  }
 }
 if(b.length>5*1024*1024)problems.push(`Unexpected large file: ${file}`);
 if(!/\.(?:woff2|png|jpg|jpeg)$/i.test(file)){
  const t=b.toString('utf8');
  if(/\/(?:Users|var\/folders)\//.test(t))problems.push(`Machine-specific path: ${file}`);
  if(/(?:gh[pousr]_[A-Za-z0-9]{30,}|sk-[A-Za-z0-9_-]{30,}|-----BEGIN (?:RSA |OPENSSH )?PRIVATE KEY-----)/.test(t))problems.push(`Possible credential: ${file}`);
 }
}
for(const name of visuals.keys())if(!files.includes(name))problems.push(`Manifest image is not tracked: ${name}`);
const html=files.filter(f=>f==='index.html'||/^compositions\/.*\.html$/.test(f));
for(const file of html){
 const t=fs.readFileSync(path.join(root,file),'utf8');
 for(const ref of t.matchAll(/(?:assets\/[\w./-]+|data-composition-src="([^"]+)")/g)){
  const p=ref[1]||ref[0];if(!fs.existsSync(path.join(root,p)))problems.push(`Missing dependency in ${file}: ${p}`);
 }
}
const remote=execFileSync('git',['remote'],{cwd:root,encoding:'utf8'}).trim();
console.log(JSON.stringify({ok:problems.length===0,trackedFiles:files.length,bundledVisuals:visuals.size,trackedAudioVideoFiles:files.filter(f=>excludedMedia.test(f)).length,runtimePages:html.length,remoteConfigured:Boolean(remote),problems},null,2));
process.exitCode=problems.length?1:0;
