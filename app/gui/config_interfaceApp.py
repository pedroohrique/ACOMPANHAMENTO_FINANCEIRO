from datetime import datetime
from tkinter import ttk, Menu, Toplevel
import tkinter as tk
from app.gui.services.treeview_handler import handler
from app.utils.logger import log_builder
from app.gui.services.row_action_manager import treeview_click_handler
from app.gui.config_interfaceCadastro import Formulario

log = log_builder("config_interface.py")

class AppInterface:
    def __init__(self, root):
        self.root = root
        self.root.title(f"Acompanhamento Financeiro - {datetime.today().year}")
        self.config_setup()
        
    
    def config_setup(self):
        
        def setup_menu(root):
            menu = Menu(self.root)
            self.root.configure(menu=menu)
            menu.add_command(label="Registrar Gasto", command=lambda: Formulario(modo="cadastrar", root=self.root))
            menu.add_command(label="Atualizar", command = lambda: handler(root))
            
        def setup_filtro(Event=None):           
            #Configuração do frame de fitros da interface
            frame_filtro = tk.Frame(self.root, bd=2, relief="solid")
            frame_filtro.pack(fill="both", expand=True, padx=5, pady=(5))
            
            #Configuração dos Labels
            label_valor = tk.Label(frame_filtro, text="Valor Gasto:", font=("Arial", 13, "bold"))
            label_dt_gasto = tk.Label(frame_filtro, text="Data Gasto:", font=("Arial", 13, "bold"))
            label_dt_vencimento = tk.Label(frame_filtro, text="Data Vencimento:", font=("Arial", 13, "bold"))

            #Configuração dos Entrys
            self.entry_valor = tk.Entry(frame_filtro, font=("Arial", 12), bg="#FFFFFF", fg="#333333", bd=2, relief="solid")
            self.entry_dt_gasto = tk.Entry(frame_filtro, font=("Arial", 12), bg="#FFFFFF", fg="#333333", bd=2, relief="solid")
            self.entry_dt_vencimento = tk.Entry(frame_filtro, font=("Arial", 12), bg="#FFFFFF", fg="#333333", bd=2, relief="solid")
            
            #Posicionamento dos Widges
            #Labels
            label_valor.grid(row=0, column=0, padx=34, pady=6, sticky="w")
            label_dt_gasto.grid(row=0, column=2, padx=34, pady=6, sticky="w")
            label_dt_vencimento.grid(row=0, column=4, padx=34, pady=6, sticky="w")
            
            #Entrys
            self.entry_valor.grid(row=0, column=1, pady=6, sticky="w")
            self.entry_dt_gasto.grid(row=0, column=3, pady=6, sticky="w")
            self.entry_dt_vencimento.grid(row=0, column=5, pady=6, sticky="w")
            
        
        def setup_treeview():             
            setup_filtro()        
            
            frame_treeview = tk.Frame(self.root, bd=2, relief="solid")
            frame_treeview.pack(fill="both", expand=True, padx=5, pady=(5))
            style = ttk.Style()
            style.theme_use("alt")
            style.configure("Treeview.Heading", font=("Arial", 14, "bold"), bg="white")
            style.configure("Treeview", font=("Arial", 12), bg="white", rowheight=26, width=2500)
            
            columns = ["DT_COMPRA", "DT_PAGAMENTO", "VALOR_TOTAL", "VALOR_PARCELA", "VALOR_PENDENTE", "CATEGORIA", "DESCRICAO", "LOCAL_GASTO"]
            headings = ["Data", "Pagamento", "Total", "Parcela", "Pendente", "Categoria", "Descrição", "Local"]
            widths = [100, 130, 100, 100, 110, 170, 210, 210]
            
            treeview = ttk.Treeview(frame_treeview, style="Treeview", columns=columns, show="headings", height=20)
            treeview.pack(padx=5, pady=5, fill="both", expand=True)
            treeview.tag_configure("oddrow", background="#E9967A")
            treeview.tag_configure("evenrow", background="#ADD8E6")
             
            for col, heading, width in zip(columns, headings, widths):
                treeview.heading(col, text=heading, anchor="center")
                treeview.column(col, width=width, anchor="center") 
            
            try:
                handler(treeview=treeview)
                self.entry_valor.bind("<KeyRelease>", lambda e: handler(treeview, self.entry_valor, self.entry_dt_gasto, self.entry_dt_vencimento))
                self.entry_dt_gasto.bind("<KeyRelease>", lambda e: handler(treeview, self.entry_valor, self.entry_dt_gasto, self.entry_dt_vencimento))
                self.entry_dt_vencimento.bind("<KeyRelease>", lambda e: handler(treeview, self.entry_valor, self.entry_dt_gasto, self.entry_dt_vencimento))
            except Exception as e:
                log.error(f"Falha ao atualizar a Treeview: {e}")

            treeview.bind("<Double-1>", lambda e: treeview_click_handler(treeview=treeview, tkinter=tk, tkinter_funcition=Toplevel))
            
            setup_menu(root=treeview)
            
        setup_treeview()
        