import os
import streamlit as st
from consultas_manager import carregar_consultas, salvar_consultas
from identificar_relacoes import processar_relacoes_consultas
from grafo_dependencias import gerar_grafo, get_latest_grafo, mostrar_grafo_dependencias
from modules.session_manager import inicializar_estado_sessao
from modules.interface import show_form_adicionar, show_form_editar, show_consultas

def main():
    """
    Função principal do aplicativo Streamlit. Gerencia o fluxo da interface e as ações do usuário.
    """
    st.title("🔍 Mapeador de Consultas Power Query")  # Título do app

    # Inicializa variáveis de estado da sessão
    inicializar_estado_sessao(["editar", "excluir", "mostrar_grafo", "caminho_grafo"])

    consultas = carregar_consultas()  # Carrega todas as consultas do arquivo JSON

    # Exclui consulta se solicitado
    if st.session_state["excluir"]:
        consultas.pop(st.session_state["excluir"], None)  # Remove consulta
        salvar_consultas(consultas)  # Salva alterações
        st.success(f"Consulta '{st.session_state['excluir']}' excluída com sucesso!")
        st.session_state["excluir"] = None

    # Edita consulta se solicitado
    if st.session_state["editar"]:
        show_form_editar(consultas)
    else:
        show_form_adicionar(consultas)

    show_consultas(consultas)  # Exibe todas as consultas cadastradas

    # Identifica relações entre consultas
    relacoes = processar_relacoes_consultas()
    st.header("🔗 Relações entre Consultas")
    for consulta, info in relacoes.items():
        tipos = ', '.join(info['tipo_relacao'])
        relacionadas = ', '.join(info['relacionadas'])
        st.markdown(f"**{consulta}**: {tipos} com **{relacionadas}**")
    
    # Botão para gerar grafo de dependências
    if st.button("Gerar Grafo de Dependências"):
        gerar_grafo(consultas, relacoes)  # Chama a função diretamente
        st.success("Grafo gerado com sucesso!")
        caminho_imagem = get_latest_grafo()  # Busca a imagem mais recente do grafo
        if caminho_imagem and os.path.exists(caminho_imagem):
            st.image(caminho_imagem, caption="Grafo de Dependências", use_container_width=True)
        else:
            st.warning("Não foi possível encontrar a imagem do grafo.")

    # Exibe grafo se solicitado
    if st.session_state.get("mostrar_grafo", False):
        mostrar_grafo_dependencias(st.session_state["caminho_grafo"])
        if st.button("Fechar Grafo"):
            st.session_state["mostrar_grafo"] = False


# Executa o app se chamado diretamente
if __name__ == "__main__":
    main()
