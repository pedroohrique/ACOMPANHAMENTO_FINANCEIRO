from app.database.connection import database_connection
from app.utils.logger import log_builder

log = log_builder("querys.py")

def payment_method_map() -> dict:
    connection, cursor = database_connection()
    try:        
        with connection:
            query = "SELECT DESCRICAO, ID_FORMA FROM TB_FORMA_PAGAMENTO"
            cursor.execute(query)
            retorno_query = cursor.fetchall()
            formas = {linha[0]:linha[1] for linha in retorno_query}    
        return formas
    except Exception as e:
        log.error(f"Falha ao executar a query: {e}")
    finally:
        cursor.close()
        
        
def category_map() -> dict:
    connection, cursor = database_connection()
    try:        
        with connection:
            query = "SELECT DESCRICAO, ID_CATEGORIA FROM TB_CATEGORIA"
            cursor.execute(query)
            retorno_query = cursor.fetchall()
            categorias = {linha[0]:linha[1] for linha in retorno_query}
        return categorias
    except Exception as e:
        log.error(f"Erro ao executar a query: {e}")
    finally:
        cursor.close()


def update_financial(array, id_registro):
    connection, cursor = database_connection()
    query = """UPDATE TB_REG_FINANC 
                SET 
                    DATA_GASTO= ?,
                    VALOR = ?,
                    DESCRICAO = ?,
                    LOCAL_GASTO = ?,
                    IDCATEGORIA = ?,
                    IDFORMA_PAGAMENTO = ?,
                    PARCELAMENTO = ?,
                    N_PARCELAS = ?
                WHERE ID_REGISTRO = ?"""
    try:
    
        with connection:
            cursor.execute(query,
                        array["dt_gasto"],
                        array["valor"],
                        array["desc"],
                        array["desc_local"],
                        array["desc_categoria"],
                        array["forma_pagamento"],
                        array["flag_parcelamento"],
                        array["qt_parcelas"],
                        id_registro)
    except Exception as e:
        log.error(f"Falha ao atualizar o registro selecionado: {e}")
    finally:
        cursor.close()
        
def record_financial(array):
    connection, cursor = database_connection()
    query = """INSERT INTO TB_REG_FINANC (
                DATA_REGISTRO, 
                DATA_GASTO, 
                VALOR,
                DESCRICAO, 
                LOCAL_GASTO, 
                PARCELAMENTO, 
                N_PARCELAS, 
                IDCATEGORIA, 
                IDFORMA_PAGAMENTO) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
                
    try:
        with connection:
            cursor.execute(query,
                        array["dt_registro"],
                        array["dt_gasto"],
                        array["valor"],
                        array["desc"],
                        array["desc_local"],
                        array["flag_parcelamento"],
                        array["qt_parcelas"],
                        array["desc_categoria"],
                        array["forma_pagamento"])
    except Exception as e:
        log.error(f"Falha ao inserir o registro no banco de dados: {e}")
    finally:
        cursor.close()

def deleta_item_treeview(id):
    connection, cursor = database_connection()
    query = "DELETE FROM TB_REG_FINANC WHERE ID_REGISTRO = ?"
    try:
        with connection:
            cursor.execute(query, id)
    
    except Exception as e:
        log.error(f"Falha ao excluir o registro: {id}, erro: {e}")
    finally:
        cursor.close()

def with_filter():    
    query = """SELECT
                CONVERT(VARCHAR, AF.DT_COMPRA, 103) AS "DT Compra",
                CONVERT(VARCHAR, AF.DT_PAGAMENTO, 103) AS "DT Pagamento",
                AF.VALOR_TOTAL AS "Total",
                AF.VALOR_PARCELA AS "Valor Parcela",
                AF.VALOR_PENDENTE AS "Valor Pendente",
                C.DESCRICAO AS "Categoria",
                RF.DESCRICAO AS "Descrição",
                RF.LOCAL_GASTO AS "Local",
                RF.ID_REGISTRO AS "IDREGISTRO",
                FP.DESCRICAO,
                RF.PARCELAMENTO,
				RF.N_PARCELAS
            FROM 
                TB_ACOMPANHAMENTO_FINANC AF
                JOIN TB_CATEGORIA C ON AF.IDCATEGORIA = C.ID_CATEGORIA
                JOIN TB_REG_FINANC RF ON AF.IDREGISTRO = RF.ID_REGISTRO
                JOIN TB_FORMA_PAGAMENTO FP ON RF.IDFORMA_PAGAMENTO = FP.ID_FORMA"""
            
    return query    
        
def with_no_filter():
    query = """SELECT
                    CONVERT(VARCHAR, AF.DT_COMPRA, 103) AS "DT Compra",
                    CONVERT(VARCHAR, AF.DT_PAGAMENTO, 103) AS "DT Pagamento",
                    AF.VALOR_TOTAL "Total",
                    AF.VALOR_PARCELA "Valor Parcela",
                    AF.VALOR_PENDENTE "Valor Pendente",
                    C.DESCRICAO "Categoria",
                    RF.DESCRICAO "Descrição",
                    RF.LOCAL_GASTO "Local",
                    RF.ID_REGISTRO "IDREGISTRO",
                    FP.DESCRICAO,
                    RF.PARCELAMENTO,
				    RF.N_PARCELAS
                FROM 
                    TB_ACOMPANHAMENTO_FINANC AF
                    JOIN TB_CATEGORIA C ON AF.IDCATEGORIA = C.ID_CATEGORIA
                    JOIN TB_REG_FINANC RF ON AF.IDREGISTRO = RF.ID_REGISTRO
                    JOIN TB_FORMA_PAGAMENTO FP ON RF.IDFORMA_PAGAMENTO = FP.ID_FORMA
                WHERE
                    MONTH(AF.DT_PAGAMENTO) >= ?
                ORDER BY
                    AF.DT_COMPRA DESC"""
        
    return query