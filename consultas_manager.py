import os  # Módulo para operações de sistema de arquivos
import json  # Módulo para manipulação de arquivos JSON

# Define o diretório base onde os dados serão armazenados
BASE_DIR = os.path.join(os.path.dirname(__file__), "Base de dados")
os.makedirs(BASE_DIR, exist_ok=True)  # Cria o diretório "Base de dados" se ele não existir

# Define o caminho completo do arquivo JSON onde as consultas serão salvas
DATA_FILE = os.path.join(BASE_DIR, "consultas_m.json")

def carregar_consultas():
    """
    Carrega as consultas salvas no arquivo JSON.
    - Verifica se o arquivo existe.
    - Se existir, lê e retorna os dados como um dicionário.
    - Se não existir, retorna um dicionário vazio.
    """
    if os.path.exists(DATA_FILE):  # Verifica se o arquivo JSON existe
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)  # Carrega os dados do arquivo JSON
    return {}  # Retorna um dicionário vazio se o arquivo não existir

def salvar_consultas(dados):
    """
    Salva as consultas no arquivo JSON.
    - Garante que o diretório base exista.
    - Escreve os dados fornecidos no arquivo JSON, formatados com indentação.
    """
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)  # Garante que o diretório exista
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)  # Salva os dados no arquivo JSON