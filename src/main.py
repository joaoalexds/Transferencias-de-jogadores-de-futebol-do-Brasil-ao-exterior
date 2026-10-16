import sys
from src.data_extraction import executar_etl
from src.network_builder import executar_modelagem
from src.statistics import testar_hipoteses_e_balanco, gerar_ranking_exportacoes

def main():
    print("="*80)
    print("INICIANDO PIPELINE DE ANÁLISE DE REDES COMPLEXAS: MERCADO DE TRANSFERÊNCIAS")
    print("="*80)

    try:
        # Passo 1: Extração e Tratamento dos Dados
        df_transf, dict_categorias = executar_etl()
        
        # Passo 2: Construção da Topologia e Exportação dos Grafos (.gexf)
        G1, df_inter = executar_modelagem(df_transf, dict_categorias)
        
        # Passo 3: Análises Estatísticas e Financeiras
        testar_hipoteses_e_balanco(df_inter, df_transf)
        gerar_ranking_exportacoes(df_transf)

        print("\n" + "="*80)
        print("PIPELINE CONCLUÍDA COM SUCESSO!")
        print("Os ficheiros .gexf foram guardados na pasta 'data/processed/'.")
        print("="*80)

    except Exception as e:
        print(f"\n[ERRO CRÍTICO] A execução falhou: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()