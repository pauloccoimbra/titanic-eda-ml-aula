#!/usr/bin/env python3
"""Gera docs/index.html (página de aula) a partir do notebook executado.

Uso:  python scripts/gerar_site.py
Requer: pip install markdown
O texto, o código e os resultados da página vêm do próprio notebook,
então página e notebook nunca ficam dessincronizados.
"""
import base64, html, json, re, sys
from pathlib import Path
import markdown

RAIZ = Path(__file__).resolve().parent.parent
NB = RAIZ / "notebook" / "Titanic_Analise_Completa.ipynb"
DOCS = RAIZ / "docs"
IMG = DOCS / "img"
REPO = "titanic-eda-ml-aula"
USUARIO = "pauloccoimbra"          # será trocado por scripts/definir_usuario.py
GOAT = f"https://{REPO}.goatcounter.com/count"

nb = json.loads(NB.read_text(encoding="utf-8"))
IMG.mkdir(parents=True, exist_ok=True)
for f in IMG.glob("fig-*.png"):
    f.unlink()

MD = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists"])
ANSI = re.compile(r"\x1b\[[0-9;]*m")

def render_md(src):
    MD.reset()
    return MD.convert(src)

def slug(t):
    t = re.sub(r"<[^>]+>", "", t)
    t = re.sub(r"[^\w\s-]", "", t.lower(), flags=re.UNICODE).strip()
    return re.sub(r"[\s_]+", "-", t)[:60]

def add_ids(h):
    """Coloca id em h2/h3 e coleta o índice (apenas h2)."""
    toc = []
    def rep(m):
        nivel, txt = m.group(1), m.group(2)
        i = slug(txt)
        if nivel == "2":
            toc.append((i, re.sub(r"<[^>]+>", "", txt)))
        return f'<h{nivel} id="{i}">{txt}</h{nivel}>'
    return re.sub(r"<h([23])>(.*?)</h\1>", rep, h), toc

def sanitiza_html_tabela(h):
    h = re.sub(r"<div[^>]*>\s*<style.*?</style>", lambda m: re.search(r"<style.*?</style>", m.group(0), re.S).group(0), h, flags=re.S)
    return h

partes, toc_geral = [], []
fig_n = 0
cod_n = 0
ultimo_titulo = ""

for c in nb["cells"]:
    src = "".join(c["source"])
    if c["cell_type"] == "markdown":
        h = render_md(src)
        h, toc = add_ids(h)
        toc_geral += toc
        m = re.findall(r"<h[23][^>]*>(.*?)</h[23]>", h)
        if m:
            ultimo_titulo = re.sub(r"<[^>]+>", "", m[-1])
        # Leitura/interpretação recebe destaque visual
        cls = "texto"
        if src.lstrip().startswith("**Leitura") or src.lstrip().startswith("**Leitura honesta"):
            cls = "texto leitura"
        elif "Como citar este material" in src:
            cls = "texto citar"
        partes.append(f'<section class="{cls}">{h}</section>')
        continue
    cod_n += 1
    bloco = [f'<div class="celula" id="cel-{cod_n}">',
             f'<div class="cel-topo"><span class="cel-rotulo">Célula de código {cod_n}</span>'
             f'<button class="btn-copiar" type="button" data-alvo="cod-{cod_n}">Copiar código</button></div>',
             f'<pre class="codigo"><code class="language-python" id="cod-{cod_n}">{html.escape(src)}</code></pre>']
    saidas = []
    for o in c.get("outputs", []):
        t = o["output_type"]
        if t == "stream":
            txt = ANSI.sub("", "".join(o["text"]))
            if "Warning" in txt and "site-packages" in txt:
                continue
            saidas.append(f'<pre class="saida-txt">{html.escape(txt)}</pre>')
        elif t in ("display_data", "execute_result"):
            d = o["data"]
            if "image/png" in d:
                fig_n += 1
                nome = f"fig-{fig_n:02d}.png"
                (IMG / nome).write_bytes(base64.b64decode(d["image/png"]))
                saidas.append(f'<figure><img loading="lazy" src="img/{nome}" alt="Gráfico {fig_n}: {html.escape(ultimo_titulo)}">'
                              f'<figcaption>Figura {fig_n}. {html.escape(ultimo_titulo)}</figcaption></figure>')
            elif "text/html" in d:
                h = "".join(d["text/html"])
                saidas.append(f'<div class="tabela">{h}</div>')
            elif "text/plain" in d:
                txt = ANSI.sub("", "".join(d["text/plain"]))
                if "Styler object" in txt or txt.startswith("<"):
                    continue
                saidas.append(f'<pre class="saida-txt">{html.escape(txt)}</pre>')
        elif t == "error":
            saidas.append('<pre class="saida-txt erro">erro na execução</pre>')
    if saidas:
        bloco.append('<div class="saida"><div class="saida-rotulo">Resultado</div>' + "".join(saidas) + "</div>")
    bloco.append("</div>")
    partes.append("".join(bloco))

corpo_nb = "\n".join(partes)

# --------------------------------------------------------------------------- blocos de contexto
CONTEXTO = r'''
<section class="texto" id="contexto-bloco">
<h2 id="contexto">Antes de começar: o Titanic, o Kaggle e a ciência de dados</h2>

<h3 id="kaggle">O desafio do Kaggle</h3>
<p>O <a href="https://www.kaggle.com/competitions/titanic" rel="noopener">Titanic: Machine Learning from Disaster</a> é a competição de entrada do <a href="https://www.kaggle.com" rel="noopener">Kaggle</a>, a plataforma de desafios de ciência de dados. É o "<em>hello world</em>" do aprendizado de máquina supervisionado: quase todo estudante passa por ele.</p>
<ul>
<li><strong>Dados:</strong> <code>train.csv</code> (891 passageiros, com a coluna <code>Survived</code>) e <code>test.csv</code> (418 passageiros, <em>sem</em> o desfecho).</li>
<li><strong>Tarefa:</strong> aprender com o treino e prever <code>Survived</code> (0/1) para cada passageiro do teste, enviando um arquivo CSV com as colunas <code>PassengerId</code> e <code>Survived</code>.</li>
<li><strong>Métrica:</strong> acurácia sobre o teste oculto, exibida no <em>leaderboard</em> público.</li>
</ul>
<div class="aviso"><strong>Dois cuidados.</strong> (1) Como <code>test.csv</code> não traz o desfecho, aqui separamos 20% do <code>train.csv</code> como conjunto de teste próprio, o que permite calcular métricas, intervalos e testes. (2) Pontuações perfeitas no <em>leaderboard</em> costumam vir de consultar os desfechos reais, publicados na internet, e não de modelagem: não têm valor pedagógico (nem científico). O objetivo aqui é <strong>entender</strong>, não "subir no ranking". Confira as regras e a situação atual na <a href="https://www.kaggle.com/competitions/titanic" rel="noopener">página da competição</a>.</div>

<h3 id="porque-titanic">Por que o Titanic é um excelente laboratório de análise de dados e ML</h3>
<p>Poucos conjuntos de dados reúnem, em tão pouco espaço, tantos dos problemas reais que um analista enfrenta. Cada característica da base abre um tópico teórico, e é assim que organizamos a aula:</p>
<div class="tabela"><table class="conexoes">
<thead><tr><th>O que a base tem</th><th>Conceito de análise de dados / ML</th><th>Onde aparece</th></tr></thead>
<tbody>
<tr><td>Desfecho binário (<code>Survived</code>)</td><td>Classificação; regressão logística; acurácia, AUC, calibração</td><td>Partes 4, 7 e 9</td></tr>
<tr><td>Variáveis numéricas e categóricas misturadas</td><td>Pré-processamento, <em>one-hot encoding</em>, padronização</td><td>Parte 9</td></tr>
<tr><td>Dados ausentes: <code>Age</code> (20%), <code>Cabin</code> (77%)</td><td>Mecanismos de ausência (MCAR/MAR/MNAR), imputação, indicadores de ausência</td><td>Partes 2 e 6</td></tr>
<tr><td><code>Fare</code> muito assimétrica</td><td>Transformação logarítmica, medidas robustas, testes não paramétricos</td><td>Partes 3 e 7.3</td></tr>
<tr><td>Texto em <code>Name</code> e <code>Ticket</code></td><td>Engenharia de atributos (título, tamanho do grupo)</td><td>Parte 5</td></tr>
<tr><td>Porto de embarque correlacionado com classe</td><td>Confusão (<em>confounding</em>), paradoxo de Simpson, associação ≠ causa</td><td>Partes 4.6 e 7.5</td></tr>
<tr><td>Efeito do sexo depende da classe</td><td>Interação; modelos aditivos × não aditivos; razão de verossimilhança</td><td>Parte 7.6</td></tr>
<tr><td>Apenas 891 linhas</td><td>Incerteza amostral, intervalos de confiança, validação cruzada repetida</td><td>Partes 4 e 9</td></tr>
<tr><td>Muitas colunas derivadas e redundantes</td><td>Multicolinearidade (VIF), informação mútua, importância por permutação</td><td>Partes 8 e 10</td></tr>
<tr><td>Vários modelos "empatam"</td><td>Linhas de base, viés-variância, tamanho do teste, McNemar</td><td>Parte 9</td></tr>
<tr><td>Risco de "colar" informação do teste no treino</td><td>Vazamento de dados (<em>data leakage</em>) e <code>Pipeline</code></td><td>Parte 9</td></tr>
</tbody></table></div>

<h3 id="objetivos">Objetivos de aprendizagem</h3>
<p>Ao final, o aluno deverá ser capaz de:</p>
<ol>
<li>conduzir uma análise exploratória organizada (univariada, bivariada e multivariada) <strong>com medidas de incerteza</strong>;</li>
<li>diagnosticar e tratar dados ausentes, explicando por que a ausência pode ser informativa;</li>
<li>distinguir associação bruta, associação ajustada, confusão e interação, e escolher o teste estatístico adequado a cada situação;</li>
<li>construir um <strong>pipeline</strong> de ML sem vazamento, comparar modelos por validação cruzada e avaliar o resultado final no teste;</li>
<li>interpretar métricas (acurácia, precisão, recall, F1, AUC, Brier) <strong>contra linhas de base</strong>;</li>
<li>comunicar resultados e limitações com honestidade.</li>
</ol>

<h3 id="como-usar">Como usar esta página</h3>
<ul>
<li><strong>Na aula:</strong> role a página na ordem; use o índice à esquerda. O botão <em>Modo apresentação</em> aumenta a fonte e esconde o índice.</li>
<li><strong>Depois da aula:</strong> cada caixa de código tem um botão <em>Copiar código</em>. Para reproduzir o notebook, crie um notebook vazio e cole as células <strong>na ordem</strong> (cada célula depende das anteriores). O botão <em>Copiar todo o código</em> no topo reúne tudo de uma vez, com marcadores <code>#%%</code> entre as células.</li>
<li><strong>Resultados:</strong> as saídas (tabelas e gráficos) mostradas abaixo de cada código são as obtidas com a semente aleatória <code>SEED = 42</code>, e devem se repetir no seu computador (pequenas diferenças podem ocorrer entre versões das bibliotecas).</li>
</ul>
<h4>Instalação rápida</h4>
<pre class="codigo"><code class="language-bash" id="cod-inst">pip install pandas numpy matplotlib seaborn scipy statsmodels scikit-learn jupyter</code></pre>
<p class="peq">No Google Colab, tudo isso já vem instalado.</p>
</section>
'''

EXERCICIOS = r'''
<section class="texto" id="exercicios-bloco">
<h2 id="exercicios">Exercícios propostos</h2>
<ol>
<li><strong>Imputação.</strong> Compare três estratégias para <code>Age</code> (mediana geral, mediana por sexo × classe, mediana por título × classe) usando validação cruzada. A escolha muda o AUC? Quanto?</li>
<li><strong>Regularização.</strong> Troque a regressão logística por uma versão com penalização L1 (<code>penalty="l1", solver="liblinear"</code>) e veja quais coeficientes vão a zero. Isso concorda com a importância por permutação?</li>
<li><strong>Interação no ML.</strong> Adicione manualmente a interação <code>Sexo × Classe</code> à regressão logística e compare com a floresta aleatória. O que a floresta "descobre" sozinha?</li>
<li><strong>Vazamento de propósito.</strong> Calcule a mediana de idade por título usando <em>todo</em> o conjunto (antes do <code>train_test_split</code>) e compare as métricas. O vazamento é grande? Por que, neste caso, ele é pequeno, e quando seria grave?</li>
<li><strong>Ranking do Kaggle.</strong> Treine o melhor modelo em todo o <code>train.csv</code>, aplique ao <code>test.csv</code> e envie o CSV. Compare a pontuação do <em>leaderboard</em> com a validação cruzada. Por que diferem?</li>
<li><strong>Causalidade.</strong> Escreva, em 10 linhas, por que "a tarifa não importa depois de controlar a classe" <em>não</em> prova que o dinheiro era irrelevante para sobreviver.</li>
</ol>
</section>
'''

SOBRE = r'''
<section class="texto citar" id="citar-bloco">
<h2 id="citar">Como citar e licença</h2>
<p><strong>Página de aula:</strong></p>
<blockquote>COIMBRA, Paulo C. <strong>Titanic: da análise exploratória à predição de sobrevivência</strong> [página de aula]. Juiz de Fora: UFJF, 2026. Disponível em: https://@@USUARIO@@.github.io/@@REPO@@/. Acesso em: (data).</blockquote>
<p><strong>Notebook:</strong></p>
<blockquote>COIMBRA, Paulo C. <strong>Titanic_Analise_Completa.ipynb</strong> [notebook Jupyter]. Juiz de Fora: UFJF, 2026. Disponível em: https://github.com/@@USUARIO@@/@@REPO@@/blob/main/notebook/Titanic_Analise_Completa.ipynb.</blockquote>
<p><strong>Artigo:</strong></p>
<blockquote>COIMBRA, Paulo C. <strong>Do Titanic ao aprendizado de máquina: um roteiro didático de análise de dados, inferência e predição</strong>. Juiz de Fora: UFJF, 2026. Disponível em: https://github.com/@@USUARIO@@/@@REPO@@/tree/main/artigo.</blockquote>
<p><strong>BibTeX (repositório):</strong></p>
<pre class="codigo"><code class="language-latex" id="cod-bib">@misc{coimbra2026titanic,
  author = {Coimbra, Paulo C.},
  title  = {Titanic: da an{\'a}lise explorat{\'o}ria {\`a} predi{\c c}{\~a}o de sobreviv{\^e}ncia: material did{\'a}tico},
  year   = {2026},
  howpublished = {\url{https://github.com/@@USUARIO@@/@@REPO@@}},
  note   = {Licen{\c c}as: MIT (c{\'o}digo) e CC BY 4.0 (textos)}
}</code></pre>
<p><strong>Licenças.</strong> Código: <a href="https://opensource.org/licenses/MIT">MIT</a>. Textos, figuras e comentários: <a href="https://creativecommons.org/licenses/by/4.0/deed.pt-br">CC BY 4.0</a> (reuse e adapte, citando a fonte). Os dados são o <code>train.csv</code> da competição do Kaggle, de uso educacional; consulte as regras da competição.</p>
<p class="peq">Material elaborado com assistência de IA (Claude, da Anthropic) e revisado pelo autor.</p>
</section>
'''
SOBRE = SOBRE.replace('@@USUARIO@@', USUARIO).replace('@@REPO@@', REPO)


toc_html = "".join(f'<a href="#{i}">{html.escape(t)}</a>' for i, t in
                   [("contexto", "Contexto: Kaggle e ML")] + toc_geral +
                   [("exercicios", "Exercícios propostos"), ("citar", "Como citar e licença")])
# corpo: o 1º bloco do notebook (título/apresentação) vem antes do contexto
primeiro, resto = partes[0], partes[1:]
# o segundo bloco é a seção "Como citar" do início do notebook: tiramos (há uma versão completa no fim)
resto = [p for p in resto if 'class="texto citar"' not in p]
corpo_final = primeiro + CONTEXTO + "\n".join(resto) + EXERCICIOS + SOBRE

CSS = (Path(__file__).parent / "site.css").read_text(encoding="utf-8")
JS = (Path(__file__).parent / "site.js").read_text(encoding="utf-8")

pagina = f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Titanic: da análise exploratória à predição, aula</title>
<meta name="description" content="Aula prática e didática com o conjunto de dados do Titanic (Kaggle): análise exploratória, inferência estatística e machine learning em Python, com código para copiar e resultados comentados.">
<meta name="author" content="Paulo C. Coimbra">
<meta property="og:title" content="Titanic: da análise exploratória à predição">
<meta property="og:description" content="Aula prática com código copiável, resultados comentados e conexão com a teoria de análise de dados e ML.">
<meta property="og:type" content="article">
<style>{CSS}</style>
</head>
<body>
<div id="progresso" aria-hidden="true"></div>
<header class="topo">
  <button id="btn-menu" class="btn-ico" aria-label="Abrir índice">☰</button>
  <a class="marca" href="#">Titanic · EDA &amp; ML</a>
  <div class="acoes">
    <button id="btn-copiar-tudo" class="btn" type="button">Copiar todo o código</button>
    <button id="btn-apres" class="btn" type="button" aria-pressed="false">Modo apresentação</button>
    <button id="btn-tema" class="btn-ico" type="button" aria-label="Alternar tema">Tema</button>
  </div>
</header>
<div class="layout">
  <nav id="indice" aria-label="Índice">{toc_html}</nav>
  <main id="conteudo">
{corpo_final}
  <footer class="rodape">
    <p>© 2026 Paulo C. Coimbra · UFJF · Código MIT · Textos CC BY 4.0 ·
    <a href="https://github.com/{USUARIO}/{REPO}">Repositório no GitHub</a></p>
  </footer>
  </main>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js" crossorigin="anonymous"></script>
<script>{JS}</script>
<script data-goatcounter="{GOAT}" async src="//gc.zgo.at/count.js"></script>
</body>
</html>
'''
(DOCS / "index.html").write_text(pagina, encoding="utf-8")
(DOCS / ".nojekyll").write_text("", encoding="utf-8")
print(f"OK: docs/index.html, {fig_n} figuras, {cod_n} células de código, {len(pagina)/1e6:.2f} MB")
