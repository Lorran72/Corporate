import graphviz

def gerar_grafo_dependencias(consultas, relacoes):
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

    return dot
