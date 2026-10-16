// Independent demo implementation by Freakz2z; MIT. Pure time sampling, no external template.
const demoFireCanvas=document.getElementById('append-fireworks-canvas');
const demoFireCtx=demoFireCanvas.getContext('2d');
const demoFireClock={t:0};
function demoFireDraw(t){
 const c=demoFireCtx,w=demoFireCanvas.width,h=demoFireCanvas.height;
 c.clearRect(0,0,w,h);c.fillStyle='#15172d';c.fillRect(0,0,w,h);
 const launches=[{x:.22,y:.25,t:.18,hue:330},{x:.72,y:.22,t:.47,hue:42},{x:.48,y:.15,t:.78,hue:190},{x:.86,y:.36,t:.98,hue:275},{x:.13,y:.4,t:1.18,hue:35}];
 for(const rocket of launches){
  const age=t-rocket.t;if(age<0)continue;
  const rise=.72,bx=rocket.x*w,by=rocket.y*h;
  if(age<rise){
   const p=age/rise,y=h+(by-h)*(1-Math.pow(1-p,2));
   for(let i=0;i<14;i++){c.fillStyle=`rgba(255,222,171,${(1-i/14)*.8})`;c.beginPath();c.arc(bx,y+i*8,Math.max(.7,3-i*.16),0,Math.PI*2);c.fill();}
  }else{
   const u=age-rise;if(u>2.1)continue;
   for(let i=0;i<72;i++){
    const a=i*Math.PI*2/72,speed=(130+(i%5)*12),x=bx+Math.cos(a)*speed*u,y=by+Math.sin(a)*speed*u+64*u*u;
    const fade=Math.pow(Math.max(0,1-u/2.1),1.4);
    c.strokeStyle=`hsla(${rocket.hue+i%9},85%,76%,${fade})`;c.lineWidth=2.2;c.beginPath();c.moveTo(x-Math.cos(a)*14,y-Math.sin(a)*14-6*u);c.lineTo(x,y);c.stroke();
   }
  }
 }
 if(t>3.2){const a=Math.min(1,(t-3.2)/.18);c.save();c.globalAlpha=a;c.fillStyle='#fff1da';c.textAlign='center';c.textBaseline='middle';c.font='310px serif';c.fillText('ねえ',w/2,h*.58);c.restore();}
}
tl.fromTo(demoFireClock,{t:0},{t:5.2333333333,duration:5.2333333333,ease:'none',onUpdate:()=>demoFireDraw(demoFireClock.t),immediateRender:true},0);
demoFireDraw(0);
