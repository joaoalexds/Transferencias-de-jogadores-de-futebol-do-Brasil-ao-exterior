# 🗺️ Visualização de Grafos no Gephi

Esta pasta contém os arquivos de grafos exportados (`.gexf`) gerados pelo nosso pipeline de processamento em Python. Estes arquivos já carregam todos os nós, arestas, pesos financeiros e métricas de centralidade pré-calculadas.

Para replicar as visualizações analíticas originais do projeto, siga as diretrizes de formatação abaixo no software **Gephi**:

### 1. Algoritmo de Disposição Espacial (Layout)
* Na aba lateral esquerda (Layout), selecione o algoritmo **ForceAtlas 2**. 
* Este algoritmo simula repulsão entre nós e atração pelas arestas, sendo excelente para desenredar a rede e colocar os maiores exportadores (hubs) em evidência.

### 2. Esquema de Cores (Nós)
Para manter a uniformidade visual da análise baseada nas divisões, aplique o seguinte padrão de cores. Vá em *Appearance* > *Nodes* > Aba *Color* > Selecione *Partition* e escolha o atributo **Categoria**:
* 🟢 **Verde:** Exterior
* 🔵 **Azul:** Série A
* 🟠 **Laranja:** Série B
* ⚪ **Cinza:** Séries Inferiores

### 3. Dimensionamento Topológico (Tamanho dos Nós)
Para destacar o impacto individual de cada clube no mercado, ajuste o tamanho dos nós. Vá em *Appearance* > *Nodes* > Aba *Size* > Selecione *Ranking* e alterne entre as métricas abaixo para mudar a perspectiva da análise:
* **Grau de Entrada (*In-Degree*):** Dimensiona os nós baseado em quem mais importa/compra jogadores.
* **Grau de Saída (*Out-Degree*):** Evidencia o poder de exportação e fornecimento da Série B e das Séries Inferiores.
* **Centralidade de Intermediação (*Betweenness Centrality*):** Destaca os verdadeiros vetores e pontes da rede (quem atua como o principal intermediário no fluxo de jogadores).
