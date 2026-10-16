// Original utility: generate neutral demo assets; never copy private artwork.
import fs from 'node:fs';
import path from 'node:path';
import zlib from 'node:zlib';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const at=(p)=>path.join(root,p);
const save=(p,bytes)=>{fs.mkdirSync(path.dirname(at(p)),{recursive:true});fs.writeFileSync(at(p),bytes);};
function crc32(b){let c=0xffffffff;for(const n of b){c^=n;for(let k=0;k<8;k++)c=(c>>>1)^((c&1)?0xedb88320:0);}return (c^0xffffffff)>>>0;}
function chunk(type,data){const t=Buffer.from(type);const out=Buffer.alloc(data.length+12);out.writeUInt32BE(data.length);t.copy(out,4);data.copy(out,8);out.writeUInt32BE(crc32(Buffer.concat([t,data])),out.length-4);return out;}
function png(w,h){
 const header=Buffer.alloc(13);header.writeUInt32BE(w);header.writeUInt32BE(h,4);header[8]=8;header[9]=6;
 const raw=Buffer.alloc((w*4+1)*h);
 for(let y=0;y<h;y++)for(let x=0;x<w;x++){
  const i=y*(w*4+1)+1+x*4;const border=x<6||x>=w-6||y<6||y>=h-6;
  const tone=border?[50,36,56]:((Math.floor(x/96)+Math.floor(y/96))%2?[203,184,212]:[235,223,235]);
  raw[i]=tone[0];raw[i+1]=tone[1];raw[i+2]=tone[2];raw[i+3]=border?200:92;
 }
 return Buffer.concat([Buffer.from([137,80,78,71,13,10,26,10]),chunk('IHDR',header),chunk('IDAT',zlib.deflateSync(raw,{level:9})),chunk('IEND',Buffer.alloc(0))]);
}
const manifest=JSON.parse(fs.readFileSync(at('config/assets.json'),'utf8'));
let created=0;
for(const item of manifest){if(!fs.existsSync(at(item.path))){save(item.path,png(item.width,item.height));created++;}}
// Source offsets extend past 228s; a complete silent media timeline avoids seeking errors.
if(!fs.existsSync(at('assets/audio/demo-silence.wav'))){
 const rate=8000;const bytes=240*rate*2;const wav=Buffer.alloc(44+bytes);
 wav.write('RIFF');wav.writeUInt32LE(36+bytes,4);wav.write('WAVEfmt ',8);wav.writeUInt32LE(16,16);wav.writeUInt16LE(1,20);wav.writeUInt16LE(1,22);wav.writeUInt32LE(rate,24);wav.writeUInt32LE(rate*2,28);wav.writeUInt16LE(2,32);wav.writeUInt16LE(16,34);wav.write('data',36);wav.writeUInt32LE(bytes,40);save('assets/audio/demo-silence.wav',wav);
}
save('assets/vendor/gsap.min.js',fs.readFileSync(at('node_modules/gsap/dist/gsap.min.js')));
console.log(`Demo assets ready: ${created} placeholders generated; existing files preserved. GSAP 3.14.2 copied locally.`);
