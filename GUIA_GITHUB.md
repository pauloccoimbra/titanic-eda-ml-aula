# Guia: publicar este material no GitHub

## 0. Dados do repositório

| Campo | Valor sugerido |
|---|---|
| **Nome** | `titanic-eda-ml-aula` (o mesmo código do GoatCounter) |
| **Descrição** (até 350 caracteres) | `Aula prática em português com os dados do Titanic (Kaggle): análise exploratória, inferência estatística e machine learning em Python. Página de aula com código para copiar, notebook reproduzível e artigo didático.` |
| **Site (Website)** | `https://pauloccoimbra.github.io/titanic-eda-ml-aula/` |
| **Visibilidade** | Public |
| **Tópicos (tags)** | `titanic` `kaggle` `exploratory-data-analysis` `machine-learning` `data-science` `scikit-learn` `logistic-regression` `statistics` `jupyter-notebook` `python` `teaching` `education` `pt-br` `github-pages` `econometrics` |
| **Licença** | já incluída (`LICENSE`, MIT; textos em `LICENSE-CONTEUDO.md`, CC BY 4.0) |

> No GitHub, os tópicos têm letras minúsculas e hífens, no máximo 20 por repositório.

## 1. Usuário do GitHub

Todos os links já usam o usuário **`pauloccoimbra`**. Se for publicar em outra conta ou organização, troque em todos os arquivos com:

```bash
python scripts/definir_usuario.py novo-usuario
```

## 2. Crie o repositório vazio

**Pelo site:** github.com → **New repository** → nome `titanic-eda-ml-aula`, descrição acima, *Public*. **Não** marque "Add a README", ".gitignore" nem licença (já existem aqui).

**Ou pela linha de comando** (com o [GitHub CLI](https://cli.github.com)):
```bash
gh repo create titanic-eda-ml-aula --public \
  --description "Aula prática em português com os dados do Titanic (Kaggle): análise exploratória, inferência estatística e machine learning em Python. Página de aula com código para copiar, notebook reproduzível e artigo didático." \
  --homepage "https://pauloccoimbra.github.io/titanic-eda-ml-aula/"
```

## 3. Envie os arquivos

Dentro da pasta `titanic-eda-ml-aula` (a que contém o `README.md`):

```bash
git init -b main
git add .
git commit -m "Material didático: Titanic, da análise exploratória à predição"
git remote add origin https://github.com/pauloccoimbra/titanic-eda-ml-aula.git
git push -u origin main
```
Se criou pelo `gh`, o remoto já pode existir (`git remote -v` mostra). *Alternativa sem terminal:* no repositório vazio, **uploading an existing file** e arraste o conteúdo da pasta (mantenha as subpastas; o upload pelo navegador aceita até 100 arquivos por vez).

## 4. Tags (tópicos) e descrição, se não usou o `gh`

Na página do repositório, ao lado de **About** clique na engrenagem ⚙️, cole a descrição e o site, adicione os tópicos da tabela acima e salve.

## 5. Ative o GitHub Pages (a página da aula)

**Settings → Pages → Build and deployment → Source: *Deploy from a branch* → Branch: `main`, pasta `/docs` → Save.**
Em 1 a 2 minutos a página estará em `https://pauloccoimbra.github.io/titanic-eda-ml-aula/`.

## 6. Crie o painel do GoatCounter (mesmo nome do repositório)

1. Acesse https://www.goatcounter.com/signup e cadastre o site com o **código `titanic-eda-ml-aula`** (o painel ficará em `https://titanic-eda-ml-aula.goatcounter.com`).
2. A página já contém a linha de rastreamento no final do `index.html`:
   ```html
   <script data-goatcounter="https://titanic-eda-ml-aula.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
   ```
3. Depois de publicada, visite a página e confirme a primeira visita no painel. Se o código escolhido no cadastro for outro, altere a constante `REPO`/`GOAT` em `scripts/gerar_site.py` e rode `python scripts/gerar_site.py`.
4. Em *Settings* do GoatCounter, em **Allow adding visitors from these domains**, inclua `pauloccoimbra.github.io`.

## 7. Versão citável com DOI (opcional, recomendado)

1. Em zenodo.org, entre com o GitHub e ative o repositório em *GitHub → Flip the switch*.
2. No GitHub, **Releases → Draft a new release**, tag `v1.0.0`, título "Versão 1.0.0", **Publish release**.
3. O Zenodo gera o **DOI**; adicione-o ao `README.md` (emblema) e ao `CITATION.cff` (`doi:`), e faça novo *commit*.

## 8. Checklist final

- [ ] os links do `README.md` e do `CITATION.cff` apontam para o seu usuário
- [ ] A página abre pelo link do GitHub Pages e os gráficos aparecem
- [ ] O botão "Abrir no Colab" do README abre o notebook
- [ ] O botão **Cite this repository** aparece (vem do `CITATION.cff`)
- [ ] A primeira visita aparece no GoatCounter
- [ ] Tópicos, descrição e site preenchidos em **About**

Para onde submeter o artigo: veja `artigo/ONDE_PUBLICAR.md`.
