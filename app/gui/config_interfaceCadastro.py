import tkinter as tk
from tkinter import ttk, Toplevel
from app.gui.services.action_handler import gerenciar_dados_formulario
from app.database.querys import category_map, payment_method_map

class Formulario:
    def __init__(self, root, array=None, modo=""):
        self.frame = Toplevel(root)
        self.dados = array
        self.modo = modo
        self.dados_formulario = {}
        self.setup_formulario()
        titulo_formulario = "Registro de Gastos" if self.modo == "cadastrar" else "Atualização de Registros"
        self.frame.title(titulo_formulario)
        self.frame.mainloop()
        
    def setup_formulario(self):
        
        def label_handler():
            #CRIAÇÃO DOS LABELS
            font_label = ("Helvetica", 13, "bold")
            label_data_gasto = tk.Label(self.frame, text="Data do Gasto: ", font=font_label)
            label_valor_total = tk.Label(self.frame, text="Valor Gasto: ", font=font_label)
            label_descricao = tk.Label(self.frame, text="Descrição: ", font=font_label)
            label_descricao_local = tk.Label(self.frame, text="Descrição Local:", font=font_label)
            label_forma_pagamento = tk.Label(self.frame, text="Forma Pagamento", font=font_label)
            label_descricao_categoria = tk.Label(self.frame, text="Categoria: ", font=font_label)
            label_qt_parcelas = tk.Label(self.frame, text="Quantidade Parcelas: ", font=font_label)
            label_flag_parcelamento = tk.Label(self.frame, text="Parcelamento: ", font=font_label)
            
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
            entry_data_gasto = tk.Entry(self.frame, font=font_entry, bg="#ffffff", fg="#333333", bd=2, relief="groove")
            entry_valor_gasto = tk.Entry(self.frame, font=font_entry, bg="#ffffff", fg="#333333", bd=2, relief="groove")
            entry_descricao = tk.Entry(self.frame, font=font_entry, bg="#ffffff", fg="#333333", bd=2, relief="groove")
            entry_descricao_local = tk.Entry(self.frame, font=font_entry, bg="#ffffff", fg="#333333", bd=2, relief="groove")
            combobox_forma_pagamento = ttk.Combobox(self.frame, values=[forma.capitalize() for forma in payment_method_map()], font=font_entry)
            combobox_descricao_categoria = ttk.Combobox(self.frame, values=[categoria.capitalize() for categoria in category_map()], font=font_entry)
            combobox_flag_parcelamento = ttk.Combobox(self.frame, values=['Sim', 'Não'], font=font_entry)
            entry_qt_parcelas = tk.Entry(self.frame, font=font_entry, bg="#ffffff", fg="#333333", bd=2, relief="groove")
            
            #POSICIONAMENTO DOS ENTRYS
            entry_data_gasto.grid(row=0, column=1, pady=3, padx=3, sticky="WE")
            entry_valor_gasto.grid(row=4, column=1, pady=3, padx=3, sticky="WE")
            entry_descricao.grid(row=6, column=1, pady=3, padx=3, sticky="WE")
            combobox_descricao_categoria.grid(row=8, column=1, pady=3, padx=2, sticky="WE")
            entry_descricao_local.grid(row=10, column=1, pady=3, padx=3, sticky="WE")
            combobox_forma_pagamento.grid(row=12, column=1, pady=3, padx=3, sticky="WE")
            combobox_flag_parcelamento.grid(row=14, column=1, pady=3, padx=3, sticky="WE")
            entry_qt_parcelas.grid(row=16, column=1, pady=3, padx=3, sticky="WE")
            
            id_registro = None
            
            if self.modo == "atualizar":
                entry_data_gasto.insert(0, self.dados[0])
                entry_valor_gasto.insert(0, self.dados[2])
                entry_descricao.insert(0, self.dados[6])
                combobox_descricao_categoria.insert(0, self.dados[5])
                entry_descricao_local.insert(0, self.dados[7])
                combobox_forma_pagamento.insert(0, self.dados[9])
                combobox_flag_parcelamento.insert(0, self.dados[10])
                entry_qt_parcelas.insert(0, self.dados[11])
                id_registro = self.dados[8]
            
            self.widgets = [entry_data_gasto, 
                          entry_valor_gasto, 
                          entry_descricao, 
                          combobox_descricao_categoria, 
                          entry_descricao_local,
                          combobox_forma_pagamento,
                          combobox_flag_parcelamento,
                          entry_qt_parcelas,
                          id_registro]  
              
        def button_handler():
            texto_botao = "Registrar" if self.modo == "cadastrar" else "Atualizar"
            botao_alterar = tk.Button(self.frame, 
                                      text=texto_botao, 
                                      command= lambda: [gerenciar_dados_formulario(self.widgets, acao=self.modo), self.frame.destroy()], 
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
        
        
        

