from datetime import datetime
from app.database.querys import record_financial, payment_method_map, category_map, update_financial
from app.gui.services.validate_form import validar_formulaio
from app.utils.logger import log_builder
from tkinter import messagebox


log = log_builder("action_handler.py")

def gerenciar_dados_formulario(widget, acao=""):
    
    categorias = category_map()
    formas = payment_method_map()
    
    try:
        valores_obtidos = {
            "dt_registro": datetime.today(),
            "dt_gasto": widget[0].get(),
            "valor": float(widget[1].get().split()[0]),
            "desc": widget[2].get(),
            "desc_categoria": categorias.get(widget[3].get().upper()),
            "desc_local": widget[4].get(),
            "forma_pagamento": formas.get(widget[5].get().upper()),
            "flag_parcelamento": widget[6].get()[0:-2],
            "qt_parcelas": int(widget[7].get()),
            "id_registro": widget[8]
            }
        
        validar_formulaio(array=valores_obtidos)
        record_financial(array=valores_obtidos) if acao == "cadastrar" else update_financial(array=valores_obtidos, id_registro=valores_obtidos["id_registro"])
        
    except ValueError as e:
        messagebox.showerror("Erro", f"Verifique os valores informados: {e}")
        log.error(f"Falha ao gerenciar os dados do formulário: {e}")
        raise  
    except Exception as e:
        messagebox.showerror("Erro", f"Erro inesperado, verifique o log da aplicação: {e}")
        log.error(f"Erro inesperado: {e}")
        raise
