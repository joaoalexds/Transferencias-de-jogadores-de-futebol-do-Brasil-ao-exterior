import numpy as np
import networkx as nx
import powerlaw
from itertools import combinations
from src.config import DATA_PROCESSED_DIR

def analisar_grafo1_completo(df, dict_categorias):
    """Constrói o Grafo 1 (Geral Oficial), calcula métricas topológicas e exporta."""
    print("\n[Grafo 1] Construindo a topologia global e calculando métricas...")
    
    df_arestas = df.groupby(["Origem", "Destino"]).agg(
        Volume=("Jogador", "count"),
        Valor_Total=("Valor_Euros", "sum")
    ).reset_index()

    G1 = nx.DiGraph()
    for _, row in df_arestas.iterrows():
        G1.add_edge(
            row["Origem"], row["Destino"], 
            weight=row["Volume"], volume=row["Volume"], 
            valor_financeiro=row["Valor_Total"]
        )

    nx.set_node_attributes(G1, dict_categorias, "Categoria")
    nx.set_node_attributes(G1, dict(G1.in_degree(weight="volume")), "InDegree_Volume")
    nx.set_node_attributes(G1, dict(G1.out_degree(weight="volume")), "OutDegree_Volume")

    # Calculando Betweenness Centrality
    epsilon = np.finfo(float).eps
    distancia = {(u, v): 1 / (dados["volume"] + epsilon) for u, v, dados in G1.edges(data=True)}
    nx.set_edge_attributes(G1, distancia, "distancia")
    nx.set_node_attributes(G1, nx.betweenness_centrality(G1, weight="distancia"), "Betweenness")

    # Avaliando distribuição dos graus (Power Law)
    graus = np.array([grau for _, grau in G1.degree() if grau > 0])
    fit = powerlaw.Fit(graus, discrete=True, verbose=False)
    
    print(f"-> Expoente α (gamma): {fit.alpha:.4f} | xmin: {fit.xmin:.0f}")
    
    arquivo_gexf = DATA_PROCESSED_DIR / "grafo1_geral_oficial.gexf"
    nx.write_gexf(G1, arquivo_gexf)
    print(f"-> Grafo 1 salvo em: {arquivo_gexf}")
    
    return G1

def gerar_grafo2_inter_series(df, dict_categorias):
    """Constrói o Grafo 2 focado apenas no fluxo entre divisões diferentes."""
    print("\n[Grafo 2] Construindo fluxo Inter-Séries...")
    df_inter = df[df['Categoria_Origem'] != df['Categoria_Destino']].copy()
    df_jogadores = df_inter.groupby(['Origem', 'Destino']).agg(Volume=('Jogador', 'count')).reset_index()

    G2 = nx.DiGraph()
    for _, row in df_jogadores.iterrows():
        G2.add_edge(row['Origem'], row['Destino'], weight=row['Volume'])

    nx.set_node_attributes(G2, dict_categorias, 'Categoria')
    arquivo_gexf = DATA_PROCESSED_DIR / "grafo2_fluxo_jogadores.gexf"
    nx.write_gexf(G2, arquivo_gexf)
    print(f"-> Grafo 2 salvo em: {arquivo_gexf} (Nós: {G2.number_of_nodes()}, Arestas: {G2.number_of_edges()})")
    
    return G2, df_inter

def gerar_grafo3_macro(df_inter):
    """Constrói o Grafo 3 (Macroscópico) com os 4 nós categorias principais."""
    print("\n[Grafo 3] Construindo a rede macroscópica (4 Nós)...")
    df_macro = df_inter.groupby(['Categoria_Origem', 'Categoria_Destino']).agg(
        Volume=('Jogador', 'count'),
        Valor_Total=('Valor_Euros', 'sum')
    ).reset_index()

    G3 = nx.DiGraph()
    for _, row in df_macro.iterrows():
        G3.add_node(row['Categoria_Origem'], label=row['Categoria_Origem'])
        G3.add_node(row['Categoria_Destino'], label=row['Categoria_Destino'])
        G3.add_edge(row['Categoria_Origem'], row['Categoria_Destino'], 
                    weight=row['Volume'], valor_financeiro=row['Valor_Total'])

    arquivo_gexf = DATA_PROCESSED_DIR / "grafo3_macro.gexf"
    nx.write_gexf(G3, arquivo_gexf)
    print(f"-> Grafo 3 salvo em: {arquivo_gexf}")
    
    return G3

def gerar_grafos_exportacao(df):
    """Constrói os Grafos de recortes de exportação para o Exterior (Grafo 4)."""
    print("\n[Grafo 4] Gerando grafos de exportação direcional para o Exterior...")
    df_base_exterior = df[
        (df['Categoria_Destino'] == 'Exterior') & 
        (df['Categoria_Origem'] != 'Exterior')
    ].copy()

    recortes = {
        "grafo_todas_nacionais_para_exterior_COM_BETWEENNESS.gexf": df_base_exterior,
        "grafo_apenas_serie_B_para_exterior.gexf": df_base_exterior[df_base_exterior['Categoria_Origem'] == 'Série B'],
        "grafo_apenas_serie_A_para_exterior.gexf": df_base_exterior[df_base_exterior['Categoria_Origem'] == 'Série A']
    }

    grafos_gerados = {}
    for nome_arquivo, df_filtrado in recortes.items():
        if df_filtrado.empty: continue

        df_arestas = df_filtrado.groupby(['Origem', 'Destino', 'Categoria_Origem', 'Categoria_Destino']).agg(
            Volume=('Jogador', 'count'), Valor_Total=('Valor_Euros', 'sum')
        ).reset_index()

        G = nx.DiGraph()
        for _, row in df_arestas.iterrows():
            G.add_edge(row['Origem'], row['Destino'], weight=row['Volume'], volume=row['Volume'],
                        valor_financeiro=row['Valor_Total'], categoria_origem=row['Categoria_Origem'], 
                        categoria_destino=row['Categoria_Destino'])

        if "BETWEENNESS" in nome_arquivo:
            distancias = {(u, v): 1.0 / (d['volume'] + 1e-5) for u, v, d in G.edges(data=True)}
            nx.set_edge_attributes(G, distancias, 'distancia')
            nx.set_node_attributes(G, nx.betweenness_centrality(G.to_undirected(), weight='distancia'), 'Betweenness')

        caminho_arquivo = DATA_PROCESSED_DIR / nome_arquivo
        nx.write_gexf(G, caminho_arquivo)
        grafos_gerados[nome_arquivo] = G
        print(f"-> Exportado: {nome_arquivo} ({G.number_of_nodes()} nós, {G.number_of_edges()} arestas)")
        
    return grafos_gerados

def gerar_projecao_nacional(df, categoria_foco):
    """Constrói os Grafos Bipartidos projetados pelo compartilhamento de agentes no mercado externo (Grafo 5)."""
    print(f"\n[Grafo 5] Projetando grafo bipartido para {categoria_foco}...")
    mask = (((df['Categoria_Origem'] == categoria_foco) & (df['Categoria_Destino'] == 'Exterior')) |
            ((df['Categoria_Origem'] == 'Exterior') & (df['Categoria_Destino'] == categoria_foco)))
    
    df_filtrado = df[mask]
    relacoes_ext = {}
    
    for _, row in df_filtrado.iterrows():
        clube_ext = row['Origem'] if row['Categoria_Origem'] == 'Exterior' else row['Destino']
        clube_br = row['Destino'] if row['Categoria_Origem'] == 'Exterior' else row['Origem']
        relacoes_ext.setdefault(clube_ext, set()).add(clube_br)

    G_proj = nx.Graph()
    for clube_ext, clubes_br in relacoes_ext.items():
        if len(clubes_br) > 1:
            for u, v in combinations(clubes_br, 2):
                if G_proj.has_edge(u, v):
                    G_proj[u][v]['weight'] += 1
                    G_proj[u][v]['clubes_gringos_em_comum'] += f", {clube_ext}"
                else:
                    G_proj.add_edge(u, v, weight=1, clubes_gringos_em_comum=clube_ext)

    nx.set_node_attributes(G_proj, categoria_foco, 'Categoria')
    
    nome_arquivo = f"projecao_bipartida_{categoria_foco.replace(' ', '_')}.gexf"
    caminho_arquivo = DATA_PROCESSED_DIR / nome_arquivo
    nx.write_gexf(G_proj, caminho_arquivo)
    
    # CORREÇÃO: Utilizar G_proj em vez de G
    print(f"-> Exportado: {nome_arquivo} ({G_proj.number_of_nodes()} nós, {G_proj.number_of_edges()} arestas)")
    
    return G_proj

def executar_modelagem(df_transf, dict_categorias):
    """Função orquestradora: gera todas as redes complexas e exporta os arquivos GEXF."""
    G1 = analisar_grafo1_completo(df_transf, dict_categorias)
    G2, df_inter = gerar_grafo2_inter_series(df_transf, dict_categorias)
    G3 = gerar_grafo3_macro(df_inter)
    grafos_ext = gerar_grafos_exportacao(df_transf)
    grafo_projecao_A = gerar_projecao_nacional(df_transf, 'Série A')
    grafo_projecao_B = gerar_projecao_nacional(df_transf, 'Série B')
    
    return G1, df_inter