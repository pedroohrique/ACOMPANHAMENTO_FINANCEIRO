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


def fg_total_exp(params):
    query = """SELECT 
                SUM(THF.VL_PARCELA)
            FROM
                TB_HISTORICO_FINANC THF
                JOIN TB_REG_FINANC TRF ON TRF.ID_REGISTRO = THF.IDREGISTRO
            WHERE
                TRF.IDCATEGORIA NOT IN (800, 900)
                AND THF.MES_DEBITO_PARCELA = ?
                AND THF.ANO_DEBITO_PARCELA = ?
            GROUP BY
                THF.MES_DEBITO_PARCELA,
                THF.ANO_DEBITO_PARCELA;"""
    
    connection,cursor = database_connection()
    
    try:
        with connection:
            cursor.execute(query, params)
            resultado_query =  cursor.fetchone()
            return resultado_query[0]
    
    except Exception as e:
        log.error(f"Falha ao executar a query, erro: {e}")
    finally:
        cursor.close()
        
def fg_spent_by_category(params):
    query = """SELECT
                    T1.DESCRICAO,
                    COALESCE(SUM(T3.VL_PARCELA), 0) AS TOTAL
                FROM TB_CATEGORIA T1
                LEFT JOIN TB_REG_FINANC T2 
                    ON T2.IDCATEGORIA = T1.ID_CATEGORIA
                LEFT JOIN TB_HISTORICO_FINANC T3 
                    ON T3.IDREGISTRO = T2.ID_REGISTRO
                    AND T3.MES_DEBITO_PARCELA = ?
                    AND T3.ANO_DEBITO_PARCELA = ?
                GROUP BY
                    T1.DESCRICAO;"""
    
    connection, cursor = database_connection()
    
    try:
        with connection:
            cursor.execute(query, params)
            resultado_query = cursor.fetchall()
            dados = {}
            for item in resultado_query:
                dados[item[0]] = item[1]
                
            return dados
    except Exception as e:
        log.error(f"Falha ao executar a query, erro: {e}")
    finally:
        cursor.close()
        

def fg_outstanding_debts(params):
    query = """SELECT
                DISTINCT
                T2.DESCRICAO,
                T3.NM_MES AS "MÊS COMPRA",
                T3.ANO,
                T4.QT_PARCELAS_PENDENTES,
                FORMAT(T4.VALOR_TOTAL, 'C', 'pt-BR') AS "VALOR TOTAL",
                FORMAT(T4.VALOR_PARCELA, 'C', 'pt-BR') AS "VALOR PARCELA",
                FORMAT(T4.VALOR_PENDENTE, 'C', 'pt-BR') AS "VALOR PENDENTE",
                DATENAME(MONTH, DATEADD(MONTH, T4.QT_PARCELAS - 1, T4.DT_COMPRA)) AS "MÊS ÚLTIMO DÉBITO",
                YEAR(DATEADD(MONTH, T4.QT_PARCELAS - 1, T4.DT_COMPRA)) AS "ANO ÚTLIMO DÉBITO"
            FROM
                TB_HISTORICO_FINANC T1
                JOIN TB_REG_FINANC T2 ON T2.ID_REGISTRO = T1.IDREGISTRO
                JOIN DIM_TEMPO T3 ON T3.ID_DATA = T2.IDDATA
                JOIN TB_ACOMPANHAMENTO_FINANC T4 ON T4.IDREGISTRO = T1.IDREGISTRO
            WHERE 
                T4.QT_PARCELAS_PENDENTES > ?
                AND T4.QT_PARCELAS > ?;"""
                
    connection, cursor = database_connection()
    
    try:
        with connection:
            cursor.execute(query, params)
            resultado_query = cursor.fetchall()
            return resultado_query
    except Exception as e:
        log.error(f"Falha ao executar a query, erro: {e}")
    finally:
        cursor.close()
        

def fg_active_installments(params):
    query = """SELECT COUNT(*) FROM TB_ACOMPANHAMENTO_FINANC WHERE QT_PARCELAS > ? AND QT_PARCELAS_PENDENTES > ?"""
    
    connection, cursor = database_connection()
    try:
        with connection:
            cursor.execute(query, params)
            resultado_query = cursor.fetchone()
            return resultado_query[0]
    except Exception as e:
        log.error(f"Falha ao executar a query, erro: {e}")
    finally:
        cursor.close()
        
def fg_value_pending(params):
    query = """SELECT SUM(VALOR_PENDENTE) FROM TB_ACOMPANHAMENTO_FINANC WHERE QT_PARCELAS > ? AND QT_PARCELAS_PENDENTES > ?"""
    connection, cursor = database_connection()
    try:
        with connection:
            cursor.execute(query, params)
            resultado_query = cursor.fetchone()
            return resultado_query[0]
    except Exception as e:
        log.error(f"Falha ao executar a query, erro: {e}")
    finally:
        cursor.close()


def fg_monthly_summary(params):
    query = """WITH CTE AS (
            SELECT
                THF.MES_DEBITO_PARCELA,
                THF.ANO_DEBITO_PARCELA,
                SUM(THF.VL_PARCELA) AS TOTAL_MENSAL,
                COUNT(*) AS QTD_TRANSACOES,
                MAX(THF.VL_PARCELA) AS MAIOR_GASTO
            FROM TB_HISTORICO_FINANC THF
            JOIN TB_REG_FINANC TRF 
                ON TRF.ID_REGISTRO = THF.IDREGISTRO
            WHERE
                TRF.IDCATEGORIA NOT IN (800, 900)
                AND ANO_DEBITO_PARCELA = ?
            GROUP BY
                THF.MES_DEBITO_PARCELA,
                THF.ANO_DEBITO_PARCELA
        )
        SELECT
            CASE CTE.MES_DEBITO_PARCELA
                WHEN 1 THEN 'JAN'
                WHEN 2 THEN 'FEV'
                WHEN 3 THEN 'MAR'
                WHEN 4 THEN 'ABR'
                WHEN 5 THEN 'MAI'
                WHEN 6 THEN 'JUN'
                WHEN 7 THEN 'JUL'
                WHEN 8 THEN 'AGO'
                WHEN 9 THEN 'SET'
                WHEN 10 THEN 'OUT'
                WHEN 11 THEN 'NOV'
                WHEN 12 THEN 'DEZ'
            END AS MES,
            CTE.ANO_DEBITO_PARCELA AS ANO,
            FORMAT(7500.00, 'C', 'pt-BR') AS [ORÇAMENTO MENSAL],
            FORMAT(CTE.TOTAL_MENSAL, 'C', 'pt-BR') AS [VALOR GASTO],
            FORMAT(7500.00 - CTE.TOTAL_MENSAL, 'C', 'pt-BR') AS [SALDO MENSAL],
            FORMAT((CTE.TOTAL_MENSAL / 7500.00) * 100, 'N2', 'pt-BR') + '%' AS [% ORÇAMENTO UTILIZADO],
            CTE.QTD_TRANSACOES AS [QTD TRANSAÇÕES],
            FORMAT(CTE.MAIOR_GASTO, 'C', 'pt-BR') AS [MAIOR GASTO],
            FORMAT(SUM(CTE.TOTAL_MENSAL) OVER (PARTITION BY CTE.ANO_DEBITO_PARCELA ORDER BY CTE.MES_DEBITO_PARCELA ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW), 'C', 'pt-BR') AS [ACUMULADO - ÚLTIMOS 12 MESES],
            FORMAT(CTE.TOTAL_MENSAL - LAG(CTE.TOTAL_MENSAL) OVER (PARTITION BY CTE.ANO_DEBITO_PARCELA ORDER BY CTE.MES_DEBITO_PARCELA), 'C', 'pt-BR') AS [VARIAÇÃO GASTO],
            FORMAT(
                CASE 
                    WHEN LAG(CTE.TOTAL_MENSAL) OVER (PARTITION BY CTE.ANO_DEBITO_PARCELA ORDER BY CTE.MES_DEBITO_PARCELA) = 0 THEN NULL
                    ELSE ((CTE.TOTAL_MENSAL - LAG(CTE.TOTAL_MENSAL) OVER (PARTITION BY CTE.ANO_DEBITO_PARCELA ORDER BY CTE.MES_DEBITO_PARCELA)) / LAG(CTE.TOTAL_MENSAL) OVER (PARTITION BY CTE.ANO_DEBITO_PARCELA ORDER BY CTE.MES_DEBITO_PARCELA) * 100)
                END, 'N2', 'pt-BR'
            ) + '%' AS [% VARIAÇÃO GASTO]
        FROM CTE
        ORDER BY CTE.ANO_DEBITO_PARCELA, CTE.MES_DEBITO_PARCELA;
        """

    connection, cursor = database_connection()
    try:
        with connection:
            cursor.execute(query, params)
            resultado_query = cursor.fetchall()
            return resultado_query
    except Exception as e:
        log.error(f"Falha ao executar a query, erro: {e}")
    finally:
        cursor.close()



