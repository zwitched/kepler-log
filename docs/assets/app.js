(function(){
  // ticking clock in Central time
  var c=document.querySelector('[data-clock]');
  function tick(){if(!c)return;try{c.textContent=new Date().toLocaleTimeString('en-US',{timeZone:'America/Chicago',hour12:false})+' CT';}catch(e){}}
  tick();setInterval(tick,1000);
  // count-up stats
  document.querySelectorAll('[data-count]').forEach(function(el){var n=+el.dataset.count,t0=null;if(!n)return;el.textContent='0';
    function step(t){if(!t0)t0=t;var p=Math.min(1,(t-t0)/1200);el.textContent=Math.round(n*(1-Math.pow(1-p,3)));if(p<1)requestAnimationFrame(step);}requestAnimationFrame(step);});
  // relative times
  function ago(d){var s=(Date.now()-d)/1000;if(s<90)return'just now';var m=s/60;if(m<60)return Math.round(m)+' min ago';var h=m/60;if(h<36)return Math.round(h)+' h ago';return Math.round(h/24)+' days ago';}
  document.querySelectorAll('time.ago').forEach(function(t){var d=new Date(t.getAttribute('datetime'));t.title=t.textContent;t.textContent=ago(d);});
  // open a signal from #hash
  function openHash(){var id=decodeURIComponent(location.hash.slice(1));if(!id)return;var el=document.getElementById(id);if(el&&el.tagName==='DETAILS')el.open=true;
    if(el&&el.classList.contains('anchor')){var n=el.nextElementSibling;if(n&&n.tagName==='DETAILS')n.open=true;}}
  openHash();window.addEventListener('hashchange',openHash);
  // discoveries filters
  var list=document.querySelector('[data-list]');if(!list)return;
  var key='all',flag='',q='';var cards=[].slice.call(list.querySelectorAll('details.sig'));var empty=document.querySelector('[data-empty]');
  function apply(){var shown=0;cards.forEach(function(c){var ok=(key==='all'||c.dataset.key===key)&&(!flag||c.dataset.flags.indexOf(flag)>=0)&&(!q||c.dataset.search.toLowerCase().indexOf(q)>=0);c.hidden=!ok;if(ok)shown++;});empty.hidden=shown>0;}
  document.querySelectorAll('[data-filters] button').forEach(function(b){b.onclick=function(){document.querySelectorAll('[data-filters] button').forEach(function(x){x.classList.remove('on')});b.classList.add('on');key=b.dataset.k;apply();};});
  document.querySelectorAll('[data-flagfilters] button').forEach(function(b){b.onclick=function(){var on=b.classList.contains('on');document.querySelectorAll('[data-flagfilters] button').forEach(function(x){x.classList.remove('on')});if(!on){b.classList.add('on');flag=b.dataset.f;}else flag='';apply();};});
  var s=document.querySelector('[data-search]');if(s)s.oninput=function(){q=s.value.trim().toLowerCase();apply();};
})();
