(function(){
  var R = document.documentElement;
  function guarda(k,v){try{localStorage.setItem(k,v)}catch(e){}}
  function le(k){try{return localStorage.getItem(k)}catch(e){return null}}
  // tema
  var t = le('tema'); if(t) R.setAttribute('data-tema', t);
  document.getElementById('btn-tema').onclick = function(){
    var atual = R.getAttribute('data-tema');
    var escuroSistema = window.matchMedia && matchMedia('(prefers-color-scheme: dark)').matches;
    var novo = (atual ? atual === 'escuro' : escuroSistema) ? 'claro' : 'escuro';
    R.setAttribute('data-tema', novo); guarda('tema', novo);
  };
  // realce de sintaxe (se a biblioteca carregou)
  if (window.hljs) { document.querySelectorAll('pre.codigo code').forEach(function(b){ try{ hljs.highlightElement(b); }catch(e){} }); }
  // copiar
  function copiar(texto, btn, rotulo){
    function ok(){ if(!btn) return; var o = btn.textContent; btn.textContent = rotulo || 'Copiado ✓'; btn.classList.add('ok'); setTimeout(function(){ btn.textContent = o; btn.classList.remove('ok'); }, 1600); }
    if (navigator.clipboard && window.isSecureContext) { navigator.clipboard.writeText(texto).then(ok, fallback); } else { fallback(); }
    function fallback(){ var ta = document.createElement('textarea'); ta.value = texto; ta.style.position='fixed'; ta.style.opacity='0'; document.body.appendChild(ta); ta.select(); try{ document.execCommand('copy'); ok(); }catch(e){} document.body.removeChild(ta); }
  }
  document.querySelectorAll('.btn-copiar').forEach(function(b){
    b.onclick = function(){ copiar(document.getElementById(b.dataset.alvo).textContent, b); };
  });
  document.getElementById('btn-copiar-tudo').onclick = function(){
    var blocos = [].slice.call(document.querySelectorAll('.celula pre.codigo code'));
    var txt = blocos.map(function(c,i){ return '#%% Célula ' + (i+1) + '\n' + c.textContent.replace(/\s+$/,''); }).join('\n\n');
    copiar(txt, this, 'Copiado ✓ (' + blocos.length + ' células)');
  };
  // modo apresentação
  var ap = document.getElementById('btn-apres');
  ap.onclick = function(){ var on = document.body.classList.toggle('apres'); ap.setAttribute('aria-pressed', on); };
  // menu móvel
  var ind = document.getElementById('indice');
  document.getElementById('btn-menu').onclick = function(){ ind.classList.toggle('aberto'); };
  ind.addEventListener('click', function(e){ if(e.target.tagName==='A') ind.classList.remove('aberto'); });
  // barra de progresso
  var barra = document.getElementById('progresso');
  function prog(){ var h = document.documentElement; var p = h.scrollTop / Math.max(1, h.scrollHeight - h.clientHeight); barra.style.width = (p*100) + '%'; }
  addEventListener('scroll', prog, {passive:true}); prog();
  // índice: seção ativa
  var links = {}; ind.querySelectorAll('a').forEach(function(a){ links[a.getAttribute('href').slice(1)] = a; });
  var heads = [].slice.call(document.querySelectorAll('#conteudo h2[id]'));
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function(es){
      es.forEach(function(e){ if(e.isIntersecting){ ind.querySelectorAll('a.ativo').forEach(function(x){x.classList.remove('ativo')}); var a = links[e.target.id]; if(a){ a.classList.add('ativo'); a.scrollIntoView({block:'nearest'}); } } });
    }, {rootMargin:'-80px 0px -70% 0px'});
    heads.forEach(function(h){ io.observe(h); });
  }
})();
