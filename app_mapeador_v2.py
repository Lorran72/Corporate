import os
import glob
import grafo_dependencias
from PIL import Image
import streamlit as st
import graphviz
import datetime
from consultas_manager import carregar_consultas, salvar_consultas
from utils import extrair_info_m, classificar_consulta
from identificar_relacoes import identificar_relacoes_consultas
from grafo_dependencias import gerar_grafo

def get_latest_grafo(path='Grafo', prefix='grafo_dependencias_'):
    arquivos = glob.glob(os.path.join(path, f"{prefix}*.png"))
    if not arquivos:
        return None
    return max(arquivos, key=os.path.getctime)

def show_form_adicionar(consultas):
    with st.form("formulario_consulta"):
        nome = st.text_input("Nome da Consulta")
        codigo_m = st.text_area("Cole aqui o código M da consulta", height=300)
        submitted = st.form_submit_button("Adicionar Consulta")
        if submitted and nome and codigo_m:
            info = extrair_info_m(codigo_m)
            tipo = classificar_consulta(nome)
            consultas[nome] = {
                "tipo": tipo,
                "tabelas": info["tabelas"],
                "colunas": info["colunas"],
                "codigo_m": codigo_m
            }
            salvar_consultas(consultas)
            st.success(f"Consulta '{nome}' adicionada com sucesso!")

def show_form_editar(consultas):
    consulta_editar = consultas[st.session_state["editar"]]
    with st.form("form_editar"):
        novo_nome = st.text_input("Nome da Consulta", value=st.session_state["editar"])
        novo_codigo_m = st.text_area("Cole aqui o código M da consulta", value=consulta_editar["codigo_m"], height=300)
        submitted_editar = st.form_submit_button("Salvar Alterações")
        cancelar_editar = st.form_submit_button("Cancelar")
        if submitted_editar and novo_nome and novo_codigo_m:
            info = extrair_info_m(novo_codigo_m)
            tipo = classificar_consulta(novo_nome)
            consultas.pop(st.session_state["editar"])
            consultas[novo_nome] = {
                "tipo": tipo,
                "tabelas": info["tabelas"],
                "colunas": info["colunas"],
                "codigo_m": novo_codigo_m
            }
            salvar_consultas(consultas)
            st.success(f"Consulta '{novo_nome}' editada com sucesso!")
            st.session_state["editar"] = None
        elif cancelar_editar:
            st.session_state["editar"] = None

def show_consultas(consultas):
    st.header("📋 Consultas Cadastradas")
    for nome, dados in consultas.items():
        with st.expander(f"{nome} ({dados['tipo']})"):
            st.markdown(f"**Tabelas Referenciadas:** {', '.join(dados['tabelas']) or 'Nenhuma'}")
            st.markdown(f"**Colunas Utilizadas:** {', '.join(dados['colunas']) or 'Nenhuma'}")
            st.code(dados["codigo_m"], language="m")
            col1, col2 = st.columns(2)
            if col1.button("Editar", key=f"editar_{nome}"):
                st.session_state["editar"] = nome
            if col2.button("Excluir", key=f"excluir_{nome}"):
                st.session_state["excluir"] = nome



def mostrar_grafo_dependencias(caminho_imagem):
    if os.path.exists(caminho_imagem):
        st.image(Image.open(caminho_imagem), caption="Grafo de Dependências entre Consultas", use_column_width=True)
    else:
        st.warning("Grafo ainda não foi gerado.")



def main():
    st.title("🔍 Mapeador de Consultas Power Query")

    if "editar" not in st.session_state:
        st.session_state["editar"] = None
    if "excluir" not in st.session_state:
        st.session_state["excluir"] = None
    if "mostrar_grafo" not in st.session_state:
        st.session_state["mostrar_grafo"] = False
    if "caminho_grafo" not in st.session_state:
        st.session_state["caminho_grafo"] = ""

    consultas = carregar_consultas()

    # Exclui consulta se solicitado
    if st.session_state["excluir"]:
        consultas.pop(st.session_state["excluir"], None)
        salvar_consultas(consultas)
        st.success(f"Consulta '{st.session_state['excluir']}' excluída com sucesso!")
        st.session_state["excluir"] = None

    # Edita consulta se solicitadoo
    if st.session_state["editar"]:
        show_form_editar(consultas)
    else:
        show_form_adicionar(consultas)

    show_consultas(consultas)

    json_path = os.path.join(os.path.dirname(__file__), "Base de dados", "consultas_m.json")
    relacoes = identificar_relacoes_consultas(json_path)
    st.header("🔗 Relações entre Consultas")
    for consulta, info in relacoes.items():
        tipos = ', '.join(info['tipo_relacao'])
        relacionadas = ', '.join(info['relacionadas'])
        st.markdown(f"**{consulta}**: {tipos} com **{relacionadas}**")
    
    # Botão para gerar grafo (apenas UM bloco, dinâmico)
    if st.button("Gerar Grafo de Dependências"):
        grafo_dependencias.gerar_grafo(consultas, relacoes)
        st.success("Grafo gerado com sucesso!")
        caminho_imagem = get_latest_grafo()
        if caminho_imagem and os.path.exists(caminho_imagem):
            st.image(caminho_imagem, caption="Grafo de Dependências", use_container_width=True)
        else:
            st.warning("Não foi possível encontrar a imagem do grafo.")

    if st.session_state.get("mostrar_grafo", False):
        mostrar_grafo_dependencias(st.session_state["caminho_grafo"])
        if st.button("Fechar Grafo"):
            st.session_state["mostrar_grafo"] = False



if __name__ == "__main__":
    main()
