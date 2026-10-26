document.querySelectorAll('.prompt .copy').forEach(function(b){
  b.addEventListener('click',function(){
    var t=b.parentElement.querySelector('code').innerText;
    (navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(function(){
      b.textContent='Copied';setTimeout(function(){b.textContent='Copy'},1500)},function(){b.textContent='Select and copy'});
  });
});
