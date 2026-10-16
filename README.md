# ⚽ Análise de Redes Complexas: Mercado de Transferências do Futebol Brasileiro

> **Autores:** [João Alexandre V. Bernardo](https://www.linkedin.com/in/joaoalexandrevb/), [Arthur Moya Valério](https://www.linkedin.com/in/arthur-moya-val%C3%A9rio/), [Felipe de Godoi Moreira](https://www.linkedin.com/in/felipe-godoi-moreira/) e [Nicolas Nunes Ferraz](https://www.linkedin.com/in/nicolas-nf/)  
> **Área:** Análise de dados | Análise de Redes Complexas (Graph Theory) | Ciência de Dados | Estatística  

 Este repositório contém um pipeline completo de Extração, Transformação e Carga (ETL), modelagem topológica e análise estatística da rede de transferências de jogadores de futebol masculino. O projeto foi desenvolvido para mapear o fluxo de capital e de atletas entre os clubes da Série A, Série B, Séries Inferiores e o mercado internacional (Exterior).

---
## 📊 Principais Conclusões e Hipóteses Validadas

Através da modelagem dos clubes como nós e das transferências como arestas, o projeto comprovou hipóteses importantes sobre a dinâmica do mercado da bola:

* **Topologia da Rede (Scale-Free e Small-World):** O ecossistema de transferências apresentou uma forte dissortatividade (-0,7224), com índice Sigma de 6,6045 e expoente $\gamma$ de 1,7963 no ajuste da Lei de Potência (método de *Clauset et al.*). Isso caracteriza o mercado como uma rede de *Mundo Pequeno* e *Sem Escala*, onde o capital escoa com alta velocidade logística através de grandes clubes (hubs) que buscam jogadores na periferia da rede para se alimentarem de ativos.
* **O Papel de Fornecimento da Base:** Ao contrário do senso comum, as Séries Inferiores fornecem um volume de jogadores cerca de 27 vezes maior para a Série A do que a própria Série B. No entanto, a Série B atua como um excelente ecossistema de valorização de ativos.
* **A Série A como "Ponte Lucrativa":** Utilizando o Teste-T de Welch para variâncias desiguais, comprovou-se estatisticamente ($p < 0.05$) que a Série A opera como a principal via comercial. Os clubes da primeira divisão compram atletas no mercado interno e os exportam com expressivas margens de valorização, sendo o sistema financiado pela injeção de capital estrangeiro.

---

## 🛠️ Tecnologias e Bibliotecas Utilizadas

* **Linguagem:** Python 3
* **Manipulação de Dados:** `pandas`, `numpy`
* **Web Scraping:** `beautifulsoup4` (BS4)
* **Teoria dos Grafos:** `networkx`, `powerlaw`
* **Estatística:** `scipy`
* **Visualização:** `matplotlib`, `seaborn`, `pyvis`, *Gephi* (Algoritmo ForceAtlas 2)

---

## 🏗️ Arquitetura do Código Fonte (`/src`)

Para garantir a manutenção e boas práticas de Engenharia de Software, a lógica originalmente desenvolvida em Jupyter Notebook foi fatorada e modularizada seguindo o princípio da responsabilidade única:

* **`config.py`**: Define globalmente os caminhos das pastas de input/output e regras estáticas (ex: nós artificiais de "fim de carreira").
* **`data_extraction.py`**: Motor de ETL. Lê o HTML, executa o scraping via BeautifulSoup, converte valores monetários e realiza a limpeza de nós indesejados.
* **`network_builder.py`**: O coração topológico. Cria grafos direcionados, calcula centralidades (*Betweenness*, *In-Degree*, *Out-Degree*), valida a propriedade Scale-Free/Small-World e gera as exportações `.gexf` e grafos bipartidos.
* **`statistics.py`**: Agrega os testes estatísticos (Test-T de Welch) e os cálculos de fluxo e balanço macroeconômico inter-divisões.
* **`main.py`**: Módulo orquestrador que importa os componentes acima e os executa de forma síncrona.

---

## 🚀 Como Executar o Pipeline

### 1. Preparação do Ambiente
Clone o repositório e instale as bibliotecas necessárias:
```bash
git clone https://github.com/joaoalexds/Transferencias-de-jogadores-de-futebol-do-Brasil-ao-exterior.git
cd Transferencias-de-jogadores-de-futebol-do-Brasil-ao-exterior
pip install -r requirements.txt
```

### 2. Base de Dados Bruta
Certifique-se de que os arquivos HTML extraídos do site *Transfermarkt* encontram-se na pasta `data/raw/` (ex: `serie_a_temp26.html`, `serie_a_temp25.html`, `serie_a_temp24.html`, `serie_b_temp26.html`, `serie_b_temp25.html`, `serie_b_temp24.html`). Devido ao volume e às boas práticas, estes arquivos originais não são enviados para o controle de versão do Git.

### 3. Processamento
Para iniciar o pipeline de extração, modelagem topológica dos grafos e validação estatística, certifique-se de estar na raiz do projeto e execute o módulo principal:

```bash
python -m src.main
```

---

## 🤖 Nota de Transparência (Uso de IA)

Este repositório documenta um trabalho acadêmico desenvolvido na universidade. A Inteligência Artificial foi utilizada para auxiliar na escrita, refatoração e estruturação do código-fonte. Contudo, toda a lógica principal, a fundamentação matemática e as análises prévias e posteriores dos dados foram realizadas integralmente por mim e pela minha equipe de projeto.
