document.querySelectorAll('.prompt .copy').forEach(function(b){
  b.addEventListener('click',function(){
    var t=b.parentElement.querySelector('code').innerText;
    (navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(function(){
      b.textContent='Copied';setTimeout(function(){b.textContent='Copy'},1500)},function(){b.textContent='Select and copy'});
  });
});
(function(){
  var f=document.querySelector('.tier-float'),blocks=document.querySelectorAll('.tiers');
  if(!f||!blocks.length||!('IntersectionObserver' in window))return;
  f.hidden=false;var seen=0;
  var io=new IntersectionObserver(function(es){es.forEach(function(e){seen+=e.isIntersecting?1:-1;if(seen<0)seen=0});upd()});
  blocks.forEach(function(b){io.observe(b)});
  function upd(){f.classList.toggle('on',window.scrollY>window.innerHeight*0.9&&seen===0)}
  window.addEventListener('scroll',upd,{passive:true});
  f.addEventListener('click',function(ev){var t=document.getElementById('guides');if(t){ev.preventDefault();t.scrollIntoView({behavior:'smooth'});history.replaceState(null,'','#guides')}});
})();
