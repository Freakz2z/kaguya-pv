{
 const ctx=document.getElementById('__ID__').getContext('2d'),tracks=__TRACKS__,clock={t:0};
 const sample=(a,t)=>{t=Math.max(0,Math.min(216,t));const i=Math.floor(t),j=Math.min(216,i+1),p=t-i;return a[i].map((v,k)=>v+(a[j][k]-v)*p);};
 function paint(t){
  ctx.clearRect(0,0,1920,1080);ctx.lineCap='round';
  const f=t*30;
  tracks.forEach((track,n)=>{
   const head=sample(track.samples,f),residual=Math.max(0,1-(f-(195+n*6))/14);
   if(!residual)return;
   const pos=age=>{const a=sample(track.samples,f-age),wave=Math.sin(age*.24+f*.10+n*2)*Math.min(age,12)*.75;return [a[0]+a[4]-head[4],a[1]+wave];};
   for(let i=47;i>=0;i--){
    const age=i*.7;if(f-age<0)continue;
    const a=pos(age),b=pos(age+.7),fade=Math.pow(1-i/48,1.7)*residual;
    ctx.strokeStyle=track.color;ctx.globalAlpha=.10*fade;ctx.lineWidth=11*head[2];
    ctx.beginPath();ctx.moveTo(...a);ctx.lineTo(...b);ctx.stroke();
    ctx.globalAlpha=.4*fade;ctx.lineWidth=Math.max(.5,2.2*(1-i/48)*head[2]);
    ctx.beginPath();ctx.moveTo(...a);ctx.lineTo(...b);ctx.stroke();
    ctx.strokeStyle='#fff5d8';ctx.globalAlpha=.65*fade;ctx.lineWidth=.8;ctx.stroke();
    if(i%5===n%3){
     const drift=Math.sin(i*2.4+n)*18*(i/48),x=b[0],y=b[1]+drift;
     ctx.fillStyle=track.color;ctx.globalAlpha=.8*fade;
     const r=1.2+Math.pow(Math.sin(f*.15-i),8)*2.2;
     ctx.beginPath();ctx.moveTo(x-r,y);ctx.quadraticCurveTo(x,y,x,y-r*1.6);ctx.quadraticCurveTo(x,y,x+r,y);ctx.quadraticCurveTo(x,y,x,y+r*1.6);ctx.quadraticCurveTo(x,y,x-r,y);ctx.fill();
    }
   }
  });ctx.globalAlpha=1;
 }
 tl.fromTo(clock,{t:0},{t:7.2,duration:7.2,ease:'none',onUpdate:()=>paint(clock.t),immediateRender:true},0);paint(0);
}
