// Audit only the distributable Git file set, and validate generated runtime dependencies.
import fs from 'node:fs';
import path from 'node:path';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const files=execFileSync('git',['ls-files','-z'],{cwd:root,encoding:'utf8'}).split('\0').filter(Boolean);
const problems=[];
const forbidden=/^(?:node_modules|\.hyperframes|\.thumbnails|\.private-preview|references|renders|qa|assets\/(?:art|audio|vendor))\//;
for(const file of files){
 if(forbidden.test(file)||/\.(?:mp4|mp3|wav|webm|ttc|ttf|zip)$/i.test(file)||/(?:^|\/)\.env(?:\.|$)/.test(file))problems.push(`Excluded material tracked: ${file}`);
 const b=fs.readFileSync(path.join(root,file));
 if(b.length>5*1024*1024)problems.push(`Unexpected large file: ${file}`);
 if(!/\.(?:woff2|png|jpg|jpeg)$/i.test(file)){
  const t=b.toString('utf8');
  if(/\/(?:Users|var\/folders)\//.test(t))problems.push(`Machine-specific path: ${file}`);
  if(/(?:gh[pousr]_[A-Za-z0-9]{30,}|sk-[A-Za-z0-9_-]{30,}|-----BEGIN (?:RSA |OPENSSH )?PRIVATE KEY-----)/.test(t))problems.push(`Possible credential: ${file}`);
 }
}
const html=files.filter(f=>f==='index.html'||/^compositions\/.*\.html$/.test(f));
for(const file of html){
 const t=fs.readFileSync(path.join(root,file),'utf8');
 for(const ref of t.matchAll(/(?:assets\/[\w./-]+|data-composition-src="([^"]+)")/g)){
  const p=ref[1]||ref[0];if(!fs.existsSync(path.join(root,p)))problems.push(`Missing dependency in ${file}: ${p}`);
 }
}
const remote=execFileSync('git',['remote'],{cwd:root,encoding:'utf8'}).trim();
console.log(JSON.stringify({ok:problems.length===0,trackedFiles:files.length,runtimePages:html.length,remoteConfigured:Boolean(remote),problems},null,2));
process.exitCode=problems.length?1:0;
