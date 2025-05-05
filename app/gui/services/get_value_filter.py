from app.utils.logger import log_builder

log = log_builder("get_value_filter.py")

def get_value(valor_entry, dtcompra_entry, dtvencimento_entry): 
    
    if not valor_entry or not dtcompra_entry or not dtvencimento_entry:
        return
    
    try:
        filtros_aplicados = {}
        
        if valor := valor_entry.get().strip():
            filtros_aplicados["ValorCompra"] = float(valor)
        if dt_compra := dtcompra_entry.get().strip():
            filtros_aplicados["DTCompra"] = str(dt_compra)
        if dt_vencimento := dtvencimento_entry.get().strip():
            filtros_aplicados["DTVencimento"] = str(dt_vencimento)     
        
        return filtros_aplicados if filtros_aplicados else None        
            
    except Exception as e:
        log.error(f"Falha ao obter os valores dos filtros: {e}")