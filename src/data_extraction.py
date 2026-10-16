import re
import pandas as pd
from bs4 import BeautifulSoup
from src.config import DATA_RAW_DIR, NOS_ARTIFICIAIS

def converter_valor(valor_str):
    """Converte strings monetárias formatadas (ex: '2.5 mi.', '500 mil') para numéricos em Euros."""
    valor_str = valor_str.lower().strip()
    numeros = re.findall(r'\d+[,.]?\d*', valor_str)
    if not numeros:
        return 0.0
    valor_base = float(numeros[0].replace(',', '.'))
    if 'mi.' in valor_str:
        return valor_base * 1000000
    elif 'mil' in valor_str:
        return valor_base * 1000
    return valor_base

def extrair_e_categorizar():
    """Processa os arquivos HTML locais e estrutura o DataFrame geral de transferências."""
    # Busca os arquivos HTML na pasta configurada em config.py
    arquivos = list(DATA_RAW_DIR.glob('serie_[ab]_temp*.html'))
    divisoes_por_ano = {}

    # Mapeamento dinâmico dos times por temporada
    for arquivo in arquivos:
        ano_match = re.search(r'temp(\d{2})', arquivo.name)
        if not ano_match: continue
        ano = 2000 + int(ano_match.group(1))
        divisao = "Série A" if "serie_a" in arquivo.name else "Série B"

        if ano not in divisoes_por_ano:
            divisoes_por_ano[ano] = {'Série A': set(), 'Série B': set()}

        with open(arquivo, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            for h2 in soup.find_all('h2', class_='content-box-headline--logo'):
                divisoes_por_ano[ano][divisao].add(h2.get_text(strip=True))

    dados = []
    transferencias_unicas = set()

    # Extração das transferências
    for arquivo in arquivos:
        ano_match = re.search(r'temp(\d{2})', arquivo.name)
        if not ano_match: continue
        ano = 2000 + int(ano_match.group(1))
        divisao_referencia = "Série A" if "serie_a" in arquivo.name else "Série B"

        with open(arquivo, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            for box in soup.find_all('div', class_='box'):
                h2 = box.find('h2', class_='content-box-headline--logo')
                if not h2: continue
                clube_referencia = h2.get_text(strip=True)

                for tabela in box.find_all('div', class_='responsive-table'):
                    headers = tabela.find_all('th')
                    if not headers: continue
                    tipo_transacao = headers[0].get_text(strip=True)

                    if not tabela.find('tbody'): continue
                    for linha in tabela.find('tbody').find_all('tr'):
                        colunas = linha.find_all('td')
                        if len(colunas) < 9: continue

                        tag_a = colunas[0].find('a')
                        if not tag_a: continue
                        jogador = tag_a.get_text(strip=True)

                        clube_envolvido = colunas[7].get_text(strip=True)
                        valor_numerico = converter_valor(colunas[8].get_text(strip=True))

                        tag_img_pais = colunas[7].find('img', class_='flaggenrahmen')
                        pais = tag_img_pais['title'] if tag_img_pais else 'Brasil'

                        # Categorização
                        if pais != 'Brasil' and clube_envolvido.lower() not in NOS_ARTIFICIAIS:
                            cat_envolvido = 'Exterior'
                        else:
                            if clube_envolvido in divisoes_por_ano.get(ano, {}).get('Série A', set()):
                                cat_envolvido = 'Série A'
                            elif clube_envolvido in divisoes_por_ano.get(ano, {}).get('Série B', set()):
                                cat_envolvido = 'Série B'
                            else:
                                cat_envolvido = 'Séries Inferiores'

                        if tipo_transacao == 'Entradas':
                            origem, destino = clube_envolvido, clube_referencia
                            cat_origem, cat_destino = cat_envolvido, divisao_referencia
                        else:
                            origem, destino = clube_referencia, clube_envolvido
                            cat_origem, cat_destino = divisao_referencia, cat_envolvido

                        chave = (ano, jogador, origem, destino)
                        if chave not in transferencias_unicas:
                            transferencias_unicas.add(chave)
                            dados.append({
                                'Ano': ano, 'Jogador': jogador,
                                'Origem': origem, 'Destino': destino,
                                'Categoria_Origem': cat_origem, 'Categoria_Destino': cat_destino,
                                'Valor_Euros': valor_numerico
                            })

    df = pd.DataFrame(dados)

    clube_cats = {}
    for _, row in df.iterrows():
        for col_clube, col_cat in [('Origem', 'Categoria_Origem'), ('Destino', 'Categoria_Destino')]:
            if row[col_clube] not in clube_cats:
                clube_cats[row[col_clube]] = row[col_cat]
            elif row[col_cat] in ['Série A', 'Série B'] and clube_cats[row[col_clube]] == 'Séries Inferiores':
                clube_cats[row[col_clube]] = row[col_cat]

    return df, clube_cats

def executar_etl():
    """Função orquestradora: extrai, categoriza e limpa os dados globais."""
    print("[1/3] Extraindo dados e mapeando categorias...")
    df_transf_bruto, dict_categorias = extrair_e_categorizar()
    
    print(f"-> Transferências brutas identificadas: {len(df_transf_bruto)}")
    
    print("[2/3] Aplicando limpeza global do ecossistema...")
    df_transf_limpo = df_transf_bruto[
        (~df_transf_bruto['Origem'].str.lower().isin(NOS_ARTIFICIAIS)) &
        (~df_transf_bruto['Destino'].str.lower().isin(NOS_ARTIFICIAIS))
    ].copy()
    
    print(f"-> Transferências válidas retidas: {len(df_transf_limpo)}")
    
    return df_transf_limpo, dict_categorias