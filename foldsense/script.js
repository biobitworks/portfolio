(function(){
  const nodes=[[34,38],[76,28],[116,54],[154,36],[192,69],[225,112],[194,146],[148,125],[107,160],[75,205],[117,239],[171,222],[214,255],[249,215]];
  const helix=document.querySelector('.helix');
  if(helix){
    nodes.forEach((p,i)=>{const n=document.createElement('span');n.className='node';n.style.left=p[0]+'px';n.style.top=p[1]+'px';n.style.opacity=(.58+(i%4)*.1).toFixed(2);helix.appendChild(n);if(i){const a=nodes[i-1],dx=p[0]-a[0],dy=p[1]-a[1],len=Math.hypot(dx,dy),b=document.createElement('span');b.className='bond';b.style.left=(a[0]+8)+'px';b.style.top=(a[1]+8)+'px';b.style.width=len+'px';b.style.transform=`rotate(${Math.atan2(dy,dx)}rad)`;helix.appendChild(b)}})
  }
  const slides=[...document.querySelectorAll('.slide')],dots=[...document.querySelectorAll('.sdot')]; let idx=0;
  function show(i){if(!slides.length)return;idx=(i+slides.length)%slides.length;slides.forEach((s,j)=>s.classList.toggle('active',j===idx));dots.forEach((d,j)=>d.classList.toggle('active',j===idx));const c=document.querySelector('[data-slide-count]');if(c)c.textContent=`${idx+1} / ${slides.length}`}
  document.querySelector('[data-prev]')?.addEventListener('click',()=>show(idx-1));
  document.querySelector('[data-next]')?.addEventListener('click',()=>show(idx+1));
  dots.forEach((d,i)=>d.addEventListener('click',()=>show(i)));show(0);
})();
