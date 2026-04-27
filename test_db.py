import pyodbc
try:
    server = "localhost"
    database = "FINANCEIRO"
    username = "Admin"
    password = "66tUa3ue!"
    conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    print(f"Tentando conectar: {conn_str}")
    conn = pyodbc.connect(conn_str, timeout=5)
    print("Conexão bem sucedida!")
    conn.close()
except Exception as e:
    print(f"Erro de conexão: {e}")
