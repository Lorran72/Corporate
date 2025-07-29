import re

def extrair_info_m(codigo_m):
    # Extrai nome da tabela do comentário final
    tabela_final = None
    tabela_match = re.search(r'//\s*([a-zA-Z0-9_]+)\s*"?\s*$', codigo_m)
    if tabela_match:
        tabela_final = tabela_match.group(1).strip()

    # Extrai colunas do Table.SelectColumns
    colunas = []
    select_match = re.search(r'Table\.SelectColumns\([^\{]*\{([^\}]*)\}', codigo_m)
    if select_match:
        colunas_raw = select_match.group(1)
        colunas += [col.strip().strip('"') for col in colunas_raw.split(",")]

    # Extrai colunas renomeadas (Table.RenameColumns)
    rename_matches = re.findall(r'\{\s*"([^"]+)"\s*,\s*"([^"]+)"\s*\}', codigo_m)
    for original, novo in rename_matches:
        colunas.append(novo)

    # Remove duplicadas e vazias
    colunas = [c for c in set(colunas) if c]

    # Retorna tabela do comentário final, se existir
    tabelas = [tabela_final] if tabela_final else []

    return {
        "tabelas": tabelas,
        "colunas": colunas
    }

def classificar_consulta(nome):
    nome = nome.lower()
    if nome.startswith("stg"):
        return "stg"
    elif nome.startswith("fato") or "fato" in nome or nome.startswith("f_"):

        return "fato"
    elif nome.startswith("dim"):
        return "dimensão"
    return "outro"