import pandas as pd
import scipy.stats as stats

def testar_hipoteses_e_balanco(df_inter, df_transf):
    """Compila estatísticas financeiras e aplica testes de hipótese para a tese do projeto."""
    print("\n=================== TESTE DE HIPÓTESES E BALANÇO FINANCEIRO ===================")
    print("1. O FLUXO DA CADEIA DE SUPRIMENTOS (TODAS AS TRANSFERÊNCIAS INTER-SÉRIES):\n")
    
    categorias_ordem = ['Séries Inferiores', 'Série B', 'Série A', 'Exterior']
    dict_metricas = {}
    
    for orig in categorias_ordem:
        for dest in categorias_ordem:
            if orig != dest:
                fluxo = df_inter[(df_inter['Categoria_Origem'] == orig) & (df_inter['Categoria_Destino'] == dest)]
                vol = len(fluxo)
                val = fluxo['Valor_Euros'].sum()
                media = val / vol if vol > 0 else 0.0
                
                dict_metricas[(orig, dest)] = {'vol': vol, 'val': val, 'media': media, 'df': fluxo}
                if vol > 0:
                    print(f"-> {orig:<17} p/ {dest:<17}: {vol:>4} atletas | Total: € {val:>14,.2f} | Média/Atleta: € {media:>11,.2f}")
    
    print("\n-------------------------------------------------------------------------------")
    print("2. COMPROVAÇÃO DE VALORIZAÇÃO NA PONTE (SÉRIE A):\n")
    
    media_BA = dict_metricas[('Série B', 'Série A')]['media']
    media_AExt = dict_metricas[('Série A', 'Exterior')]['media']
    fluxo_BA = dict_metricas[('Série B', 'Série A')]['df']
    fluxo_AExt = dict_metricas[('Série A', 'Exterior')]['df']
    
    if media_AExt > media_BA and media_BA > 0:
        print(f"[CONFIRMADO] A Série A exporta para o Exterior com valor médio {(media_AExt/media_BA):.1f} vezes superior ao custo de aquisição da Série B.")
        
    amostra_AExt = fluxo_AExt[fluxo_AExt['Valor_Euros'] > 0]['Valor_Euros']
    amostra_BA = fluxo_BA[fluxo_BA['Valor_Euros'] > 0]['Valor_Euros']
    
    if len(amostra_AExt) > 1 and len(amostra_BA) > 1:
        _, p_val = stats.ttest_ind(amostra_AExt, amostra_BA, equal_var=False)
        print(f"[ESTATÍSTICA T-Test de Welch] P-valor (Série B->A vs Série A->Ext): {p_val:.4e} (p < 0.05 comprova a valorização)\n")
        
    print("-------------------------------------------------------------------------------")
    print("3. BALANÇO DE DIVISAS E INJEÇÃO DE CAPITAL EXTERNO:\n")
    
    for div in ['Série A', 'Série B', 'Séries Inferiores']:
        ent = df_transf[df_transf['Categoria_Destino'] == div]['Valor_Euros'].sum()
        sai = df_transf[df_transf['Categoria_Origem'] == div]['Valor_Euros'].sum()
        print(f"{div:<17} - Compras: € {ent:>14,.2f} | Vendas: € {sai:>14,.2f} | Saldo: € {(sai - ent):>14,.2f}")
        
    din_ext = df_transf[df_transf['Categoria_Destino'] == 'Exterior']['Valor_Euros'].sum()
    print(f"\nCONCLUSÃO ECONÔMICA: O Exterior injetou € {din_ext:,.2f} no ecossistema, financiando a liquidez e a ponte da Série A.")
    print("===============================================================================")


def gerar_ranking_exportacoes(df_transf):
    """Calcula e exibe o ranking dos maiores exportadores diretos para o mercado internacional."""
    print("\n--- MAIORES EXPORTADORES NACIONAIS PARA O EXTERIOR (TOP 20) ---")
    df_apenas_exterior = df_transf[
        (df_transf['Categoria_Destino'] == 'Exterior') &
        (df_transf['Categoria_Origem'] != 'Exterior')
    ]
    
    df_ranking_exterior = df_apenas_exterior.groupby(['Origem', 'Categoria_Origem']).agg(
        Quantidade_Exportada=('Jogador', 'count')
    ).reset_index()
    
    df_ranking_exterior.rename(columns={
        'Origem': 'Nome do Time',
        'Categoria_Origem': 'Série do Time',
        'Quantidade_Exportada': 'Quantidade Exportada'
    }, inplace=True)
    
    df_ranking_exterior = df_ranking_exterior.sort_values(by='Quantidade Exportada', ascending=False).reset_index(drop=True)
    
    # Como não temos o "display()" do Jupyter Notebook no terminal, usamos to_string()
    print(df_ranking_exterior.head(20).to_string())