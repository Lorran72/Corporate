import json  # Módulo para manipulação de arquivos JSON
import re  # Módulo para trabalhar com expressões regulares
import os  # Módulo para operações de sistema de arquivos

def identificar_relacoes_consultas(json_path):
    """
    Identifica as relações entre consultas com base no código M.
    
    Parâmetros:
    - json_path: Caminho para o arquivo JSON contendo as consultas.

    Retorna:
    - Um dicionário com as relações entre consultas, incluindo os tipos de relação.
    """
    # Abre o arquivo JSON e carrega as consultas
    with open(json_path, "r", encoding="utf-8") as f:
        consultas = json.load(f)

    relacoes = {}  # Dicionário para armazenar as relações entre consultas

    # Itera sobre cada consulta no arquivo JSON
    for nome, dados in consultas.items():
        codigo_m = dados.get("codigo_m", "")  # Obtém o código M da consulta
        relacionadas = set()  # Conjunto para armazenar consultas relacionadas
        tipos = []  # Lista para armazenar os tipos de relação

        # Identifica empilhamento (Table.Combine)
        combine_match = re.search(r'Table\.Combine\(\{([^\}]*)\}\)', codigo_m)
        if combine_match:
            # Extrai as consultas combinadas
            consultas_combinadas = [c.strip() for c in combine_match.group(1).split(",")]
            relacionadas.update(consultas_combinadas)  # Adiciona ao conjunto de relacionadas
            tipos.append("empilhamento")  # Adiciona o tipo de relação

        # Identifica mesclagem (Table.Join ou Table.NestedJoin)
        join_match = re.findall(r'Table\.(?:Join|NestedJoin)\s*\(\s*([^\s,]+)', codigo_m)
        if join_match:
            relacionadas.update(join_match)  # Adiciona ao conjunto de relacionadas
            tipos.append("mesclagem")  # Adiciona o tipo de relação

        # Se houver consultas relacionadas, adiciona ao dicionário de relações
        if relacionadas:
            relacoes[nome] = {
                "relacionadas": [],  # Lista de consultas relacionadas
                "tipo_relacao": []  # Lista de tipos de relação
            }
            # Adiciona as relações de empilhamento
            if combine_match:
                for c in consultas_combinadas:
                    relacoes[nome]["relacionadas"].append(c)
                    relacoes[nome]["tipo_relacao"].append("empilhamento")
            # Adiciona as relações de mesclagem
            if join_match:
                for j in join_match:
                    relacoes[nome]["relacionadas"].append(j)
                    relacoes[nome]["tipo_relacao"].append("mesclagem")

    return relacoes  # Retorna o dicionário de relações

def processar_relacoes_consultas():
    """
    Processa as relações entre consultas carregando o arquivo JSON e identificando as dependências.
    
    Retorna:
    - Um dicionário com as relações entre consultas.
    """
    # Define o caminho do arquivo JSON de consultas
    json_path = os.path.join(os.path.dirname(__file__), "Base de dados", "consultas_m.json")
    
    # Identifica as relações entre consultas
    relacoes = identificar_relacoes_consultas(json_path)
    
    return relacoes


# def identificar_relacoes_consultas(json_path):
#     with open(json_path, "r", encoding="utf-8") as f:
#         consultas = json.load(f)

#     relacoes = {}

#     for nome, dados in consultas.items():
#         codigo_m = dados.get("codigo_m", "")
#         relacionadas = set()
#         tipos = []

#         # Empilhamento: Table.Combine
#         combine_match = re.search(r'Table\.Combine\(\{([^\}]*)\}\)', codigo_m)
#         if combine_match:
#             consultas_combinadas = [c.strip() for c in combine_match.group(1).split(",")]
#             relacionadas.update(consultas_combinadas)
#             tipos.append("empilhamento")

#         # Mesclagem: Table.Join ou Table.NestedJoin
#         join_match = re.findall(r'Table\.(?:Join|NestedJoin)\s*\(\s*([^\s,]+)', codigo_m)
#         if join_match:
#             relacionadas.update(join_match)
#             tipos.append("mesclagem")

#         if relacionadas:
#             relacoes[nome] = {
#                 "relacionadas": list(relacionadas),
#                 "tipo_relacao": tipos
#             }

#     return relacoes

# # Exemplo de uso:
# if __name__ == "__main__":
#     json_path = os.path.join(os.path.dirname(__file__), "Base de dados", "consultas_m.json")
#     relacoes = identificar_relacoes_consultas(json_path)
#     for consulta, info in relacoes.items():
#         print(f"{consulta}: {info['tipo_relacao']} -> {', '.join(info['relacionadas'])}")