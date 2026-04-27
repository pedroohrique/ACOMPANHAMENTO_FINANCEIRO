import json
import pyodbc
from app.utils.logger import log_builder

log = log_builder("database.py")

# def load_config():
#     path = r"app\database\connection_config.json"
#     try:
#         with open(path, 'r') as f:
#             return json.load(f)
        
#     except FileNotFoundError:
#         raise Exception(log.error(f"Arquivo de configuração não encontrado em: {path}"))
    
    

def database_connection():
    path = r"app\database\connection_config.json"
    try:
        with open(path, 'r') as f:
            database_config = json.load(f)
    except FileNotFoundError:
        log.error(f"Arquivo de configuração não encontrado em: {path}")
        return None

    server = database_config["database"]["server"]
    database = database_config["database"]["name"]
    username = database_config["database"]["user"]
    password = database_config["database"]["password"]

    # Verificação rápida
    if not all([server, database, username, password]):
        log.error("Uma ou mais variáveis de ambiente do banco não foram carregadas.")
        return None

    try:
        # Usando Autenticação do Windows e confiando no certificado conforme print enviado
        connection = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            f'SERVER={server};DATABASE={database};'
            'Trusted_Connection=yes;'
            'TrustServerCertificate=yes;'
        )
        cursor = connection.cursor()
        return connection, cursor

    except pyodbc.Error as e:        
        log.error(f"Falha ao conectar ao banco de dados local: {e}")
        return None

