# titanic-eda-ml-aula

**Titanic: da análise exploratória à predição de sobrevivência.** Material didático em português com os dados do desafio [Titanic do Kaggle](https://www.kaggle.com/competitions/titanic): página de aula, notebook Python e artigo.

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/pauloccoimbra/titanic-eda-ml-aula/blob/main/notebook/Titanic_Analise_Completa.ipynb)
[![Licença do código: MIT](https://img.shields.io/badge/c%C3%B3digo-MIT-blue.svg)](LICENSE)
[![Licença dos textos: CC BY 4.0](https://img.shields.io/badge/textos-CC%20BY%204.0-lightgrey.svg)](LICENSE-CONTEUDO.md)

- 🌐 **Página de aula:** https://pauloccoimbra.github.io/titanic-eda-ml-aula/
- 📓 **Notebook:** [`notebook/Titanic_Analise_Completa.ipynb`](notebook/Titanic_Analise_Completa.ipynb)
- 📄 **Artigo didático:** [`artigo/artigo.pdf`](artigo/artigo.pdf) (fonte em [`artigo/artigo.md`](artigo/artigo.md); versão Word em [`artigo/artigo.docx`](artigo/artigo.docx))

## O que é

Um percurso completo, do dado bruto ao modelo, usando um conjunto pequeno o bastante para ser entendido linha a linha e rico o bastante para exigir quase todas as decisões de um projeto real de análise de dados:

1. **Análise exploratória** com intervalos de confiança (univariada, bivariada e multivariada);
2. **Dados ausentes** (por que `Age` e `Cabin` não faltam ao acaso);
3. **Engenharia de atributos** (título, tamanho de família e de grupo de bilhete, convés);
4. **Inferência estatística** (qui-quadrado e V de Cramér, razão de chances, Mann-Whitney, regressão logística, razão de verossimilhança, interações, confusão);
5. **Machine learning** com `Pipeline` sem vazamento, validação cruzada repetida, ajuste de hiperparâmetros, ROC, calibração, importância por permutação e análise de erros;
6. **Resenha** dos resultados, com as limitações.

### Resultado principal (em uma frase)
Sexo e classe (e a interação entre os dois) explicam a maior parte do que é previsível; porto e tarifa perdem relevância depois do ajuste; e, em um teste de 179 passageiros, os modelos de ML não se distinguem de modo confiável de uma regra de uma linha ("mulher sobrevive, homem morre"). Detalhes e números na página e no artigo.

## Como usar

### Na aula
Abra a página de aula (GitHub Pages). Ela traz o texto, o código (com botão **Copiar**) e os resultados comentados. O botão *Copiar todo o código* reúne o código de todas as células.

### Para reproduzir o notebook
**Opção A, Colab:** clique no botão "Abrir no Colab" acima. Nada a instalar.

**Opção B, local:**
```bash
git clone https://github.com/pauloccoimbra/titanic-eda-ml-aula.git
cd titanic-eda-ml-aula
python -m venv .venv && source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter notebook notebook/Titanic_Analise_Completa.ipynb
```
O notebook baixa o `train.csv` de fontes públicas. Sem internet, coloque o `train.csv` do Kaggle na pasta onde o notebook roda (o código procura `titanic.csv` e `train.csv` localmente primeiro).

**Opção C, a partir da página:** crie um notebook vazio e cole as células de código na ordem.

### Regenerar a página a partir do notebook
```bash
python scripts/gerar_site.py     # lê o notebook executado e escreve docs/index.html
```

## Estrutura

```
titanic-eda-ml-aula/
├── README.md
├── LICENSE                 # MIT (código)
├── LICENSE-CONTEUDO.md     # CC BY 4.0 (textos e figuras)
├── CITATION.cff            # o GitHub mostra "Cite this repository"
├── requirements.txt
├── notebook/
│   └── Titanic_Analise_Completa.ipynb
├── docs/                   # página de aula (GitHub Pages)
│   ├── index.html
│   └── img/
├── artigo/
│   ├── artigo.md / .pdf / .docx
│   ├── referencias.bib
│   ├── figuras/
│   └── ONDE_PUBLICAR.md
└── scripts/
    ├── gerar_site.py  (+ site.css, site.js)
    └── definir_usuario.py
```

## Como citar

Cite o tipo de material que você usou. Em todos os casos, use o ano e o endereço do repositório; se houver DOI (Zenodo), prefira-o.

**Repositório (ABNT):**
> COIMBRA, Paulo C. **Titanic: da análise exploratória à predição de sobrevivência**: material didático (página de aula, notebook e artigo). Juiz de Fora: UFJF, 2026. Disponível em: https://github.com/pauloccoimbra/titanic-eda-ml-aula. Acesso em: dia mês ano.

**Repositório (APA 7):**
> Coimbra, P. C. (2026). *Titanic: da análise exploratória à predição de sobrevivência: material didático* [Material didático, notebook Python e artigo]. GitHub. https://github.com/pauloccoimbra/titanic-eda-ml-aula

**Página de aula:**
> COIMBRA, Paulo C. **Titanic: da análise exploratória à predição de sobrevivência** [página de aula]. Juiz de Fora: UFJF, 2026. Disponível em: https://pauloccoimbra.github.io/titanic-eda-ml-aula/. Acesso em: dia mês ano.

**Notebook:**
> COIMBRA, Paulo C. **Titanic_Analise_Completa.ipynb** [notebook Jupyter]. Juiz de Fora: UFJF, 2026. Disponível em: https://github.com/pauloccoimbra/titanic-eda-ml-aula/blob/main/notebook/Titanic_Analise_Completa.ipynb.

**Artigo:**
> COIMBRA, Paulo C. **Do Titanic ao aprendizado de máquina: um roteiro didático de análise de dados, inferência e predição**. Juiz de Fora: UFJF, 2026. Disponível em: https://github.com/pauloccoimbra/titanic-eda-ml-aula/tree/main/artigo.

**BibTeX:**
```bibtex
@misc{coimbra2026titanic,
  author = {Coimbra, Paulo C.},
  title  = {Titanic: da an{\'a}lise explorat{\'o}ria {\`a} predi{\c c}{\~a}o de sobreviv{\^e}ncia: material did{\'a}tico},
  year   = {2026},
  howpublished = {\url{https://github.com/pauloccoimbra/titanic-eda-ml-aula}},
  note   = {Licen{\c c}as: MIT (c{\'o}digo) e CC BY 4.0 (textos)}
}

@misc{coimbra2026artigo,
  author = {Coimbra, Paulo C.},
  title  = {Do Titanic ao aprendizado de m{\'a}quina: um roteiro did{\'a}tico de an{\'a}lise de dados, infer{\^e}ncia e predi{\c c}{\~a}o},
  year   = {2026},
  howpublished = {\url{https://github.com/pauloccoimbra/titanic-eda-ml-aula/tree/main/artigo}}
}
```
O arquivo [`CITATION.cff`](CITATION.cff) permite usar o botão **Cite this repository** do GitHub.

## Licenças

- **Código:** [MIT](LICENSE).
- **Textos, figuras e artigo:** [CC BY 4.0](LICENSE-CONTEUDO.md).
- **Dados:** `train.csv` da competição do Kaggle; não é redistribuído aqui. Consulte as [regras da competição](https://www.kaggle.com/competitions/titanic).

## Estatísticas de acesso

A página de aula usa o [GoatCounter](https://www.goatcounter.com), um contador de visitas sem *cookies*, com o código de site **`titanic-eda-ml-aula`** (painel em `https://titanic-eda-ml-aula.goatcounter.com`). Se você reutilizar a página, troque o código no final de `docs/index.html` (e em `scripts/gerar_site.py`).

## Nota sobre o uso de IA

O material foi elaborado com assistência de IA (Claude, da Anthropic) e revisado pelo autor. Os números do texto saem do notebook, executado com `SEED = 42`.

## Autor

Paulo C. Coimbra, Departamento de Economia e Finanças, Universidade Federal de Juiz de Fora (UFJF).
