import tkinter as tk
from tkinter import Tk, ttk
from app.gui.services.action_handler import gerenciar_dados_formulario

class Formulario:
    def __init__(self, array=None, modo=""):
        self.root = Tk()
        self.dados = array
        self.modo = modo
        self.dados_formulario = {}
        self.setup_formulario()
        titulo_formulario = "Registro de Gastos" if self.modo == "cadastrar" else "Atualização de Registros"
        self.root.title(titulo_formulario)
        self.root.mainloop()
        
    def setup_formulario(self):
        
        def label_handler():
            #CRIAÇÃO DOS LABELS
            font_label = ("Helvetica", 13, "bold")
            label_data_gasto = tk.Label(self.root, text="Data do Gasto: ", font=font_label)
            label_valor_total = tk.Label(self.root, text="Valor Gasto: ", font=font_label)
            label_descricao = tk.Label(self.root, text="Descrição: ", font=font_label)
            label_descricao_local = tk.Label(self.root, text="Descrição Local:", font=font_label)
            label_forma_pagamento = tk.Label(self.root, text="Forma Pagamento", font=font_label)
            label_descricao_categoria = tk.Label(self.root, text="Categoria: ", font=font_label)
            label_qt_parcelas = tk.Label(self.root, text="Quantidade Parcelas: ", font=font_label)
            label_flag_parcelamento = tk.Label(self.root, text="Parcelamento: ", font=font_label)
            
            #POSICIONAMENTO DOS LABELS
            label_data_gasto.grid(row=0, column=0, columnspan=1, pady=3, padx=1, sticky="W")
            label_valor_total.grid(row=4, column=0, columnspan=1, pady=3, padx=1, sticky="W")
            label_descricao.grid(row=6, column=0, columnspan=1, pady=3, padx=1, sticky="W")
            label_descricao_categoria.grid(row=8, column=0, columnspan=1, pady=3, padx=1, sticky="W")
            label_descricao_local.grid(row=10, column=0, columnspan=1, pady=3, padx=1, sticky="W")           
            label_forma_pagamento.grid(row=12, column=0, columnspan=1, pady=3, padx=1, sticky="W")
            label_flag_parcelamento.grid(row=14, column=0, columnspan=1, pady=3, padx=1, sticky="W")
            label_qt_parcelas.grid(row=16, column=0, columnspan=1, pady=3, padx=1, sticky="W")
            
        def entry_handler():
            font_entry = ("Helvetica", 13)
            entry_data_gasto = tk.Entry(self.root, font=font_entry, bg="#ffffff", fg="#333333", bd=2, relief="groove")
            entry_valor_gasto = tk.Entry(self.root, font=font_entry, bg="#ffffff", fg="#333333", bd=2, relief="groove")
            entry_descricao = tk.Entry(self.root, font=font_entry, bg="#ffffff", fg="#333333", bd=2, relief="groove")
            entry_descricao_local = tk.Entry(self.root, font=font_entry, bg="#ffffff", fg="#333333", bd=2, relief="groove")
            combobox_forma_pagamento = ttk.Combobox(self.root, values="ADD VALORES AQUI", font=font_entry)
            combobox_descricao_categoria = ttk.Combobox(self.root, values="ADD_VALORES_AQUI", font=font_entry)
            combobox_flag_parcelamento = ttk.Combobox(self.root, values=['Sim', 'Não'], font=font_entry)
            entry_qt_parcelas = tk.Entry(self.root, font=font_entry, bg="#ffffff", fg="#333333", bd=2, relief="groove")
            
            #POSICIONAMENTO DOS ENTRYS
            entry_data_gasto.grid(row=0, column=1, pady=3, padx=3, sticky="WE")
            entry_valor_gasto.grid(row=4, column=1, pady=3, padx=3, sticky="WE")
            entry_descricao.grid(row=6, column=1, pady=3, padx=3, sticky="WE")
            combobox_descricao_categoria.grid(row=8, column=1, pady=3, padx=2, sticky="WE")
            entry_descricao_local.grid(row=10, column=1, pady=3, padx=3, sticky="WE")
            combobox_forma_pagamento.grid(row=12, column=1, pady=3, padx=3, sticky="WE")
            combobox_flag_parcelamento.grid(row=14, column=1, pady=3, padx=3, sticky="WE")
            entry_qt_parcelas.grid(row=16, column=1, pady=3, padx=3, sticky="WE")
        
            if self.modo == "atualizar":
                entry_data_gasto.insert(0, self.dados[0])
                entry_valor_gasto.insert(0, self.dados[2])
                entry_descricao.insert(0, self.dados[6])
                combobox_descricao_categoria.insert(0, self.dados[5])
                entry_descricao_local.insert(0, self.dados[7])
                combobox_forma_pagamento.insert(0, self.dados[9])
                combobox_flag_parcelamento.insert(0, self.dados[10])
                entry_qt_parcelas.insert(0, self.dados[11])
            
            self.widgets = [entry_data_gasto, 
                          entry_valor_gasto, 
                          entry_descricao, 
                          combobox_descricao_categoria, 
                          entry_descricao_local,
                          combobox_forma_pagamento,
                          combobox_flag_parcelamento,
                          entry_qt_parcelas]  
              
        def button_handler():
            texto_botao = "Registrar" if self.modo == "cadastrar" else "Atualizar"
            botao_alterar = tk.Button(self.root, 
                                      text=texto_botao, 
                                      command= lambda: gerenciar_dados_formulario(self.widgets, acao=self.modo, id=self.dados[8]), 
                                      borderwidth=5, 
                                      font=("Arial", 15, "bold"), 
                                      bg="#4CAF50", 
                                      fg="#ffffff", 
                                      relief="raised", 
                                      bd=1)
            botao_alterar.grid(row=20, column=0, columnspan=3, sticky="WE",  pady=(10), padx=3)
               
        label_handler()
        entry_handler()
        button_handler()
        
        
        

