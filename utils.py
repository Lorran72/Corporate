import re  # Módulo para trabalhar com expressões regulares

def extrair_info_m(codigo_m):
    """
    Extrai informações do código M fornecido.
    
    Parâmetros:
    - codigo_m: String contendo o código M.

    Retorna:
    - Um dicionário com:
        - tabela_final: Nome da tabela final (se especificado no comentário).
        - colunas: Lista de colunas selecionadas no código.
        - colunas_renomeadas: Lista de colunas renomeadas (pares de nomes original e novo).
    """
    # Extrai o nome da tabela final a partir de um comentário no final do código
    tabela_final = None
    tabela_match = re.search(r'//\s*([a-zA-Z0-9_]+)\s*"?\s*$', codigo_m)
    if tabela_match:
        tabela_final = tabela_match.group(1)  # Captura o nome da tabela final

    # Extrai as colunas referenciadas no Table.SelectColumns
    colunas = []
    select_match = re.search(r'Table\.SelectColumns\([^\{]*\{([^\}]*)\}', codigo_m)
    if select_match:
        # Remove espaços e aspas das colunas extraídas
        colunas = [col.strip().replace('"', '') for col in select_match.group(1).split(',')]

    # Extrai colunas renomeadas no Table.RenameColumns
    rename_matches = re.findall(r'\{\s*"([^"]+)"\s*,\s*"([^"]+)"\s*\}', codigo_m)
    colunas_renomeadas = [(orig, novo) for orig, novo in rename_matches]  # Lista de pares (original, novo)

    # Retorna as informações extraídas
    return {
        "tabela_final": tabela_final,
        "colunas": colunas,
        "colunas_renomeadas": colunas_renomeadas
    }

def classificar_consulta(nome):
    """
    Classifica o tipo de consulta com base no nome fornecido.
    
    Parâmetros:
    - nome: Nome da consulta.

    Retorna:
    - Uma string indicando o tipo da consulta:
        - "stg" para consultas que começam com "stg".
        - "fato" para consultas relacionadas a fatos.
        - "dimensão" para consultas relacionadas a dimensões.
        - "outro" para consultas que não se enquadram nos critérios acima.
    """
    nome = nome.lower()  # Converte o nome para minúsculas para facilitar a comparação
    if nome.startswith("stg"):
        return "stg"  # Classifica como "stg"
    elif nome.startswith("fato") or "fato" in nome or nome.startswith("f_"):
        return "fato"  # Classifica como "fato"
    elif nome.startswith("dim"):
        return "dimensão"  # Classifica como "dimensão"
    return "outro"  # Classifica como "outro" se não atender aos critérios anteriores