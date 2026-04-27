from fastapi import FastAPI, HTTPException, Body, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
import logging
from typing import Optional, Dict, Any

# Configuração de logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Importações das suas queries originais
from app.database.querys import (
    payment_method_map,
    category_map,
    fg_monthly_summary,
    query_money_flow,
    fg_spent_by_category,
    with_no_filter,
    record_financial,
    update_financial,
    deleta_item_treeview,
    fg_outstanding_debts,
    fg_active_installments,
    fg_value_pending,
    fg_total_exp,
    database_connection
)

API_KEY_SECRET = "pedro_financas_2026_seguro_!@"

app = FastAPI(title="API Acompanhamento Financeiro")

@app.middleware("http")
async def verify_api_key(request: Request, call_next):
    # Pula a verificação para opções (CORS)
    if request.method == "OPTIONS":
        return await call_next(request)
    
    api_key = request.headers.get("X-API-Key")
    if api_key != API_KEY_SECRET:
        return JSONResponse(status_code=403, content={"detail": "Acesso negado: Chave de API invalida"})
    
    response = await call_next(request)
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- AUXILIARES ---
def get_db_data(query_func, params=None):
    try:
        if params is not None:
            return query_func(params)
        return query_func()
    except Exception as e:
        logger.error(f"Erro ao executar {query_func.__name__}: {e}")
        return None

# --- ROTAS DE CONFIGURAÇÃO ---
@app.get("/api/categorias")
def get_categories():
    return {"categorias": get_db_data(category_map) or {}}

@app.get("/api/formas-pagamento")
def get_payment_methods():
    return {"formas_pagamento": get_db_data(payment_method_map) or {}}

# --- ROTAS DE DASHBOARD / RELATÓRIO ---
def parse_currency(value):
    if value is None: return 0.0
    if isinstance(value, (int, float)): return float(value)
    # Remove R$, espaços e converte formato brasileiro para americano
    clean = str(value).replace('R$', '').replace(' ', '').replace('.', '').replace(',', '.')
    try:
        return float(clean)
    except:
        return 0.0

@app.get("/api/resumo-mensal/{ano}")
def get_monthly_summary_route(ano: int):
    resumo = get_db_data(fg_monthly_summary, (ano,))
    if not resumo: return {"resumo": []}
    
    return {"resumo": [{
        "mes": str(linha[0]).strip(), 
        "ano": linha[1], 
        "orcamento": parse_currency(linha[2]), 
        "gasto": parse_currency(linha[3]), 
        "saldo": parse_currency(linha[4]), 
        "percentual": linha[5], 
        "qtd": linha[6], 
        "maior_gasto": linha[7],
        "acumulado": parse_currency(linha[8]), 
        "variacao": linha[9], 
        "percentual_var": linha[10]
    } for linha in resumo]}

@app.get("/api/fluxo-caixa/{ano}/{mes}")
def get_money_flow_route(ano: int, mes: int):
    fluxo = get_db_data(query_money_flow, (mes, ano))
    if not fluxo or not fluxo[0] or fluxo[0][0] is None:
        return {"fluxo": {"vl_entradas": 0, "vl_saidas": 0, "custo_medio_mensal": 0, "saldo_atual": 0}}
    
    l = fluxo[0]
    return {"fluxo": {"vl_entradas": l[0], "vl_saidas": l[1], "custo_medio_mensal": l[2], "saldo_atual": l[3]}}

@app.get("/api/gastos-por-categoria/{ano}/{mes}")
def get_spent_by_category_route(ano: int, mes: int):
    return {"gastos": get_db_data(fg_spent_by_category, (mes, ano)) or {}}

@app.get("/api/debitos-pendentes")
def get_pending_debts():
    debitos = get_db_data(fg_outstanding_debts, (0, 1)) # Parâmetros baseados no file_generator.py
    if not debitos: return {"debitos": []}
    
    return {"debitos": [{
        "descricao": d[0], "mes_compra": d[1], "ano": d[2], "parcelas_pendentes": d[3],
        "valor_total": d[4], "valor_parcela": d[5], "valor_pendente": d[6],
        "mes_ultimo_debito": d[7], "ano_ultimo_debito": d[8]
    } for d in debitos]}

@app.get("/api/visao-geral-relatorio/{ano}/{mes}")
def get_report_overview(ano: int, mes: int):
    periodo = (mes, ano)
    vl_total = get_db_data(fg_total_exp, periodo) or 0
    vl_pendente = get_db_data(fg_value_pending, (1, 0)) or 0
    qtd_pendente = get_db_data(fg_active_installments, (1, 0)) or 0
    
    return {
        "total_gastos": vl_total,
        "valor_disponivel": 7500 - vl_total,
        "valor_total_pendente": vl_pendente,
        "qtd_debitos_pendentes": qtd_pendente
    }

# --- ROTAS DE REGISTROS (CRUD) ---
@app.get("/api/transacoes")
def get_transactions():
    query = with_no_filter()
    conn, cursor = database_connection()
    try:
        with conn:
            cursor.execute(query)
            rows = cursor.fetchall()
            return {"transacoes": [{
                "id": r[8], "dt_compra": r[0], "dt_pagamento": r[1], "total": r[2],
                "valor_parcela": r[3], "valor_pendente": r[4], "categoria": r[5],
                "descricao": r[6], "local": r[7], "forma_pagamento": r[9],
                "parcelamento": r[10], "n_parcelas": r[11]
            } for r in rows]}
    except Exception as e:
        logger.error(f"Erro ao buscar transações: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@app.post("/api/transacoes")
def create_transaction(data: Dict[Any, Any] = Body(...)):
    try:
        data["dt_registro"] = datetime.now()
        record_financial(data)
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Erro ao criar transação: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/transacoes/{id_registro}")
def update_transaction(id_registro: int, data: Dict[Any, Any] = Body(...)):
    try:
        update_financial(data, id_registro)
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Erro ao atualizar transação: {e}")
        raise HTTPException(status_code=500, detail=str(e))

from app.gui.services.file_generator import GenerateFile

@app.post("/api/exportar-relatorio")
def export_report_route(data: Dict[str, int] = Body(...)):
    try:
        mes = data.get("mes")
        ano = data.get("ano")
        if not mes or not ano:
            raise HTTPException(status_code=400, detail="Mês e ano são obrigatórios")
        
        generator = GenerateFile(mes_visualizacao=mes, ano_vizualizacao=ano)
        return {"status": "success", "path": str(generator.caminho_gerado)}
    except Exception as e:
        logger.error(f"Erro ao exportar relatório: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/transacoes/{id_registro}")
def delete_transaction(id_registro: int):
    try:
        deleta_item_treeview((id_registro,))
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Erro ao deletar transação: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)