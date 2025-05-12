from app.gui.services.get_value_filter import get_value
from app.database.querys import with_filter, with_no_filter
from app.database.connection import database_connection
from app.utils.logger import log_builder
from datetime import datetime

log = log_builder("treeview_handler.py")

def handler(treeview, widget_1="", widget_2="", widget_3="", Event=None):
    connection, cursor = database_connection()
    dados = get_value(widget_1, widget_2, widget_3)
    
    def display_lines(values):
        try:
            for indice, item in enumerate(values):
                    tag = "evenrow" if indice % 2 == 0 else "oddrow"
                    treeview.insert("", "end", values=(item[0], 
                                                    item[1], str(item[2]) + " " + "R$", 
                                                    str(item[3]) + " " + "R$", str(item[4]) + " " + "R$", 
                                                    item[5].capitalize(), item[6], item[7], item[8], item[9], 
                                                    item[10], item[11]), tags=(tag,))
        except Exception as e:
            log.error(f"Falha ao inserir os dados na Treeview: {e}")
            
    for item in treeview.get_children():
        treeview.delete(item)
    
    if dados:
        query = with_filter()
        conditions = []
        params = []
            
        if dados.get("ValorCompra"):
            conditions.append(" AF.VALOR_TOTAL = ?")
            params.append(dados.get("ValorCompra"))
        if dados.get("DTCompra"):
            conditions.append(" AF.DT_COMPRA = ?")
            params.append(dados.get("DTCompra"))
        if dados.get("DTVencimento"):
            conditions.append(" AF.DT_PAGAMENTO = ?")
            params.append(dados.get("DTVencimento"))
        if conditions:
            query += " WHERE" + " AND".join(conditions)
                
        query += " ORDER BY AF.DT_COMPRA DESC"    
        with connection:     
            cursor.execute(query, params)  
            resultado = cursor.fetchall()   
    else:              
        query = with_no_filter()
        with connection:            
            cursor.execute(query, datetime.today().month)
            resultado = cursor.fetchall()  
            
    cursor.close()      
    return display_lines(values=resultado)  
    
        
       
    
    
    