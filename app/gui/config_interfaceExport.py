import tkinter as tk
from tkinter import ttk, Toplevel, messagebox
from app.gui.services.file_generator import GenerateFile


class InterfaceExport:
    def __init__(self, root):
        self.root = root
        self.frame = Toplevel(self.root)
        self.frame.title("Exportador - Demonstrativo Financeiro.")
        self.frame.columnconfigure(1, weight=1)
        self.config_interface()

    def config_interface(self):
        self.label_handler()
        self.entry_handler()
        self.button_handler()

    def label_handler(self):
        l_font = ("Helvetica", 13, "bold")

        l_month_to_export = tk.Label(
            self.frame,
            text="Mês de Exportação:",
            font=l_font
        )
        l_year_to_export = tk.Label(
            self.frame,
            text="Ano de Exportação:",
            font=l_font
        )

        l_month_to_export.grid(
            row=0, column=0, padx=5, pady=5, sticky="W"
        )
        l_year_to_export.grid(
            row=1, column=0, padx=5, pady=5, sticky="W"
        )

    def entry_handler(self):
        e_font = ("Helvetica", 13)

        self.cb_month_to_export = ttk.Combobox(
            self.frame,
            values=[
                'Janeiro', 'Fevereiro', 'Março', 'Abril',
                'Maio', 'Junho', 'Julho', 'Agosto',
                'Setembro', 'Outubro', 'Novembro', 'Dezembro'
            ],
            font=e_font,
            state="readonly"
        )

        self.e_year_to_export = tk.Entry(
            self.frame,
            font=e_font,
            bg="#ffffff",
            fg="#333333",
            bd=2,
            relief="groove"
        )

        self.cb_month_to_export.grid(
            row=0, column=1, padx=5, pady=5, sticky="WE"
        )
        self.e_year_to_export.grid(
            row=1, column=1, padx=5, pady=5, sticky="WE"
        )

    def button_handler(self):
        button = tk.Button(
            self.frame,
            text="Exportar Relatório",
            command=self.export_handler,
            font=("Arial", 15, "bold"),
            bg="#4CAF50",
            fg="#ffffff",
            relief="raised",
            bd=1
        )

        button.grid(
            row=3, column=0, columnspan=2,
            sticky="WE", pady=15, padx=5
        )

    def export_handler(self):
        month_map = {
            "Janeiro": 1, "Fevereiro": 2, "Março": 3, "Abril": 4,
            "Maio": 5, "Junho": 6, "Julho": 7, "Agosto": 8,
            "Setembro": 9, "Outubro": 10, "Novembro": 11, "Dezembro": 12
        }

        month_text = self.cb_month_to_export.get()
        year_text = self.e_year_to_export.get().strip()

        if not month_text or not year_text:
            messagebox.showwarning(
                "Campos obrigatórios",
                "Informe o mês e o ano para exportação."
            )
            return

        try:
            v_month = month_map[month_text]
            v_year = int(year_text)
        except ValueError:
            messagebox.showerror(
                "Valor inválido",
                "O ano deve ser um número inteiro."
            )
            return

        try:
            GenerateFile(
                mes_visualizacao=v_month,
                ano_vizualizacao=v_year
            )

            messagebox.showinfo(
                "Exportação concluída",
                "Relatório exportado com sucesso!"
            )

        except Exception as e:
            messagebox.showerror(
                "Erro na exportação",
                f"Ocorreu um erro ao exportar o relatório:\n\n{e}"
            )

