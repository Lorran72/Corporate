import streamlit as st
from utils import extrair_info_m, classificar_consulta
from consultas_manager import salvar_consultas

def show_form_adicionar(consultas):
    """
    Exibe o formulário para adicionar uma nova consulta ao sistema.
    """
    with st.form("formulario_consulta"):
        nome = st.text_input("Nome da Consulta")
        codigo_m = st.text_area("Cole aqui o código M da consulta", height=300)
        submitted = st.form_submit_button("Adicionar Consulta")
        if submitted and nome and codigo_m:
            info = extrair_info_m(codigo_m)  # Extrai tabelas e colunas do código M
            tipo = classificar_consulta(nome)  # Classifica o tipo da consulta
            consultas[nome] = {
                "tipo": tipo,
                "tabelas": info["tabelas"],
                "colunas": info["colunas"],
                "codigo_m": codigo_m
            }
            salvar_consultas(consultas)  # Salva no arquivo JSON
            st.success(f"Consulta '{nome}' adicionada com sucesso!")

def show_form_editar(consultas):
    """
    Exibe o formulário para editar uma consulta existente.
    """
    consulta_editar = consultas[st.session_state["editar"]]
    with st.form("form_editar"):
        novo_nome = st.text_input("Nome da Consulta", value=st.session_state["editar"])
        novo_codigo_m = st.text_area("Cole aqui o código M da consulta", value=consulta_editar["codigo_m"], height=300)
        submitted_editar = st.form_submit_button("Salvar Alterações")
        cancelar_editar = st.form_submit_button("Cancelar")
        if submitted_editar and novo_nome and novo_codigo_m:
            info = extrair_info_m(novo_codigo_m)  # Extrai tabelas e colunas do novo código M
            tipo = classificar_consulta(novo_nome)  # Atualiza tipo da consulta
            consultas.pop(st.session_state["editar"])  # Remove consulta antiga
            consultas[novo_nome] = {
                "tipo": tipo,
                "tabelas": info.get("tabelas", []),  # Use get() para evitar KeyError
                "colunas": info.get("colunas", []),
                "codigo_m": novo_codigo_m
            }
            salvar_consultas(consultas)  # Salva alterações
            st.success(f"Consulta '{novo_nome}' editada com sucesso!")
            st.session_state["editar"] = None  # Sai do modo edição
        elif cancelar_editar:
            st.session_state["editar"] = None  # Cancela edição

def show_consultas(consultas):
    """
    Exibe todas as consultas cadastradas, mostrando detalhes e botões de ação.
    """
    st.header("📋 Consultas Cadastradas")
    for nome, dados in consultas.items():
        with st.expander(f"{nome} ({dados['tipo']})"):
            # Mostra tabelas e colunas utilizadas na consulta
            st.markdown(f"**Tabelas Referenciadas:** {', '.join(dados['tabelas']) or 'Nenhuma'}")
            st.markdown(f"**Colunas Utilizadas:** {', '.join(dados['colunas']) or 'Nenhuma'}")
            st.code(dados["codigo_m"], language="m")  # Exibe o código M
            col1, col2 = st.columns(2)
            # Botão para editar consulta
            if col1.button("Editar", key=f"editar_{nome}"):
                st.session_state["editar"] = nome
            # Botão para excluir consulta
            if col2.button("Excluir", key=f"excluir_{nome}"):
                st.session_state["excluir"] = nome