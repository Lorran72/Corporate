import streamlit as st

def inicializar_estado_sessao(chaves):
    """
    Inicializa as variáveis de estado da sessão no Streamlit.
    
    Parâmetros:
    - chaves: Lista de chaves a serem inicializadas no estado da sessão.
    """
    for chave in chaves:
        if chave not in st.session_state:
            st.session_state[chave] = None