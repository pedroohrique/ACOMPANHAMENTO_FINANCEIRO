from app.utils.logger import log_builder
from app.database.querys import deleta_item_treeview
from app.gui.services.treeview_handler import handler
from app.gui.config_interfaceCadastro import Formulario

log = log_builder("row_action_manager.py")

def treeview_click_handler(treeview, tkinter, tkinter_funcition):
    try:
        linha_selecionada = treeview.selection()[0]        
        if linha_selecionada:
            registros = treeview.item(linha_selecionada)['values']
            eixo_x, eixo_y, largura, altura = treeview.bbox(linha_selecionada)
            x_root = treeview.winfo_rootx() + eixo_x
            y_root = treeview.winfo_rooty() + eixo_y + altura
            container_botoes = tkinter_funcition(treeview)
            container_botoes.geometry(f"100x60+{x_root}+{y_root}")
            container_botoes.overrideredirect(True)
            tkinter.Button(container_botoes, text="Alterar", font=("Helvetica", 10, "bold"), fg="#32CD32", command=lambda:[container_botoes.destroy(), Formulario(registros, modo="atualizar")]).pack(fill=tkinter.BOTH, expand=True)
            tkinter.Button(container_botoes, text="Excluir", font=("Helvetica", 10, "bold"), fg="#FF0000", command=lambda:[container_botoes.destroy(), deleta_item_treeview(registros[8]), handler(treeview)]).pack(fill=tkinter.BOTH, expand=True)

            def close_window(event):
                container_botoes.destroy()
        
        treeview.bind("<Button-1>", close_window)

    except IndexError:
        log.error(f"Nenhum registro foi selecionado: {e}")
    except Exception as e:
        log.error(f"Erro ao manipular o registro da treeview: {e}")