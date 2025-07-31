import json
import re
import os

def identificar_relacoes_consultas(json_path):
    import json, re
    with open(json_path, "r", encoding="utf-8") as f:
        consultas = json.load(f)
    relacoes = {}
    for nome, dados in consultas.items():
        codigo_m = dados.get("codigo_m", "")
        relacionadas = set()
        tipos = []

        combine_match = re.search(r'Table\\.Combine\\(\\{([^}]+)\\}\\)', codigo_m)
        if combine_match:
            consultas_combinadas = [c.strip() for c in combine_match.group(1).split(",")]
            relacionadas.update(consultas_combinadas)
            tipos.append("empilhamento")

        join_match = re.findall(r'Table\\.(?:Join|NestedJoin)\\s*\\(\\s*([^\\s,]+)', codigo_m)
        if join_match:
            relacionadas.update(join_match)
            tipos.append("mesclagem")

        if relacionadas:
            relacoes[nome] = {
                "relacionadas": list(relacionadas),
                "tipo_relacao": tipos
            }
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