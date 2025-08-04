import graphviz  # Biblioteca para criação e visualização de grafos
import os  # Módulo para operações de sistema de arquivos
import glob  # Busca de arquivos por padrão
from datetime import datetime  # Módulo para manipulação de datas e horários
from PIL import Image  # Manipulação de imagens
import streamlit as st  # Framework para apps web interativos

def gerar_grafo(consultas, relacoes):
    """
    Gera um grafo de dependências entre consultas e salva como imagem PNG.
    
    Parâmetros:
    - consultas: Dicionário contendo as consultas e seus detalhes (tipo, tabelas, etc.).
    - relacoes: Dicionário contendo as relações entre consultas (relacionadas e tipo de relação).
    
    Retorna:
    - O caminho do arquivo PNG gerado.
    """
    # Cria um objeto Graphviz para o grafo
    dot = graphviz.Digraph(format='png')
    dot.attr(size='20,14')  # Define o tamanho do grafo em polegadas
    dot.attr(dpi='300')  # Define a resolução da imagem gerada

    # Define as cores para os diferentes tipos de consultas
    tipo_cores = {
        "stg": "lightblue",  # Cor para consultas do tipo "stg"
        "fato": "lightgreen",  # Cor para consultas do tipo "fato"
        "dimensão": "orange",  # Cor para consultas do tipo "dimensão"
        "outro": "white"  # Cor padrão para outros tipos
    }

    # Adiciona os nós (consultas) ao grafo
    for nome, dados in consultas.items():
        cor = tipo_cores.get(dados.get("tipo", "outro"), "white")  # Obtém a cor com base no tipo
        dot.node(nome, style="filled", fillcolor=cor)  # Cria o nó com estilo preenchido

    # Adiciona as arestas (relações) ao grafo
    for origem, info in relacoes.items():
        for destino, tipo in zip(info["relacionadas"], info["tipo_relacao"]):
            estilo = "solid" if tipo == "empilhamento" else "dashed"  # Define o estilo da linha
            cor = "blue" if tipo == "empilhamento" else "red"  # Define a cor da linha
            dot.edge(origem, destino, color=cor, style=estilo)  # Cria a aresta entre os nós

    # Define o diretório onde o grafo será salvo
    pasta = os.path.abspath("Grafo")
    os.makedirs(pasta, exist_ok=True)  # Cria o diretório "Grafo" se ele não existir

    # Define o nome do arquivo com base na data e hora atual
    caminho_arquivo = os.path.join(pasta, f"grafo_dependencias_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    
    # Renderiza o grafo e salva como PNG
    dot.render(caminho_arquivo, format='png', cleanup=True)
    caminho_arquivo_png = caminho_arquivo + ".png"

    # Retorna o caminho do arquivo gerado
    return caminho_arquivo_png

def get_latest_grafo(path='Grafo', prefix='grafo_dependencias_'):
    """
    Busca o arquivo de imagem do grafo de dependências mais recente na pasta especificada.
    """
    arquivos = glob.glob(os.path.join(path, f"{prefix}*.png"))
    if not arquivos:
        return None
    return max(arquivos, key=os.path.getctime)

def mostrar_grafo_dependencias(caminho_imagem):
    """
    Exibe a imagem do grafo de dependências, se existir.
    """
    if os.path.exists(caminho_imagem):
        st.image(Image.open(caminho_imagem), caption="Grafo de Dependências entre Consultas", use_column_width=True)
    else:
        st.warning("Grafo ainda não foi gerado.")
