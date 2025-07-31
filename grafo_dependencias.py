import graphviz
import os
from datetime import datetime

def gerar_grafo(consultas, relacoes):
    dot = graphviz.Digraph(format='png')
    tipo_cores = {
        "stg": "lightblue",
        "fato": "lightgreen",
        "dimensão": "orange",
        "outro": "white"
    }

    for nome, dados in consultas.items():
        cor = tipo_cores.get(dados.get("tipo", "outro"), "white")
        dot.node(nome, style="filled", fillcolor=cor)

    for origem, info in relacoes.items():
        for destino, tipo in zip(info["relacionadas"], info["tipo_relacao"]):
            estilo = "solid" if tipo == "empilhamento" else "dashed"
            cor = "blue" if tipo == "empilhamento" else "red"
            dot.edge(destino, origem, color=cor, style=estilo)

    # Salva o arquivo na pasta Grafo com nome grafo_dependencias_YYYYMMDD_HHMMSS.png
    pasta = "Grafo"
    os.makedirs(pasta, exist_ok=True)
    caminho_arquivo = os.path.join(pasta, f"grafo_dependencias_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
    dot.render(caminho_arquivo, cleanup=True)

    # Retorna o caminho do arquivo gerado
    return caminho_arquivo
