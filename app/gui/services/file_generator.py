from app.database.querys import fg_total_exp, fg_spent_by_category, fg_outstanding_debts, fg_active_installments, fg_value_pending, fg_monthly_summary
from datetime import datetime
from calendar import monthrange
import textwrap
from tabulate import tabulate
from app.utils.logger import log_builder
import json
import os

class GenerateFile:
    def __init__(self, mes_visualizacao, ano_vizualizacao):
        self.mes_visualizacao = mes_visualizacao
        self.ano_visualizacao = ano_vizualizacao
        self.periodo = (self.mes_visualizacao, self.ano_visualizacao)
        self.logging = log_builder("file_generator.py")
        self.export(self.formatacao_relatorio())
        
    
    def dados_relatorio(self, periodo):
        vl_total = fg_total_exp(params=periodo)
        
        vl_categoria = fg_spent_by_category(params=periodo)
        debitos_pendentes = fg_outstanding_debts(params=(0, 1))
        qtd_debitos_pendentes = fg_active_installments(params=(1, 0))
        vl_pendente = fg_value_pending(params=(1, 0))
        resumo_mensal = fg_monthly_summary(params=(self.ano_visualizacao))
        vl_disponivel = (7500 - vl_total)
        vls_categoria = fg_spent_by_category(params=periodo)

        dados = {
            "vl_total": vl_total,
            "vl_categoria": vl_categoria,
            "debitos_pendentes": debitos_pendentes,
            "qtd_debitos_pendentes": qtd_debitos_pendentes,
            "vl_pendente": vl_pendente,
            "resumo_mensal": resumo_mensal,
            "vl_disponivel": vl_disponivel,
            "vls_cat": [vls_categoria]
        }
        return dados
        
    def calcula_dias_restantes(self):
            dt_atual = datetime.today()
            ultimo_dia_mes = monthrange(dt_atual.year, dt_atual.month)[1]
            fim_mes = datetime(dt_atual.year, dt_atual.month, ultimo_dia_mes)
            dias_restantes = ((fim_mes - dt_atual).days + 1)
            return dias_restantes

    def carrega_textos(self):
            caminho_arquivo = r"C:\Users\Pedro Henrique\Documents\Projetos\ACOMPANHAMENTO_FINANCEIRO\app\utils\fg_labels.json"
            try:
                with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except FileNotFoundError:
                pass
                #raise Exception(logging.error(f"Falha ao carregar as informações! Arquivo não encontrado ou corrompido em: {caminho_arquivo}"))
    
    def formatacao_relatorio(self):
            
            def alinhamento_texto(texto, caracter):
                    texto_formatado = texto.center(190, caracter)
                    return texto_formatado
            
            relatorio = []
            dias_restantes = self.calcula_dias_restantes()
            valores = self.dados_relatorio(periodo=self.periodo)
            vl_total = valores["vl_total"]
            vl_disponivel = valores["vl_disponivel"]
            vl_recomendado = (vl_disponivel / dias_restantes)
            vl_por_categoria = valores["vls_cat"]
            vl_transporte = vl_por_categoria[0]["TRANSPORTE"]
            vl_alimentacao = vl_por_categoria[0]["ALIMENTAÇÃO"]
            vl_moradia = vl_por_categoria[0]["MORADIA"]
            vl_saude = vl_por_categoria[0]["SAÚDE"]
            vl_lazer = vl_por_categoria[0]["LAZER E ENTRETENIMENTO"]
            vl_pg_fatura = vl_por_categoria[0]["PAGAMENTO FATURA"]
            vl_gastos_ocasionais = vl_por_categoria[0]["GASTOS OCASIONAIS"]
            vl_outros = vl_por_categoria[0]["OUTROS"]
            vl_educacao = vl_por_categoria[0]["EDUCAÇÃO"]
            vl_investimentos = vl_por_categoria[0]["INVESIMENTOS E APLICAÇÕES"]
            vl_compras = vl_por_categoria[0]["COMPRAS"]
            qtd_debitos_pendentes = valores["qtd_debitos_pendentes"]
            vl_pendente = valores["vl_pendente"]
            tb_debitos_pendentes = valores["debitos_pendentes"]
            tb_resumo_mensal = valores["resumo_mensal"]
            
            textos = self.carrega_textos()
            titulo_timestamp = f"{textos['labels']['01']} - {datetime.today()}"
            rotulo = alinhamento_texto(texto=(titulo_timestamp), caracter=" ")
            relatorio.append(rotulo)
            relatorio.append(" ")
            relatorio.append("=" * 190)
            relatorio.append(textwrap.fill(textos['labels']['06'], width=180))
            rotulo = alinhamento_texto(texto=(textos['labels']['02']), caracter="-")
            relatorio.append(rotulo)
            relatorio.append(" ")
            relatorio.append(f"{textos['labels']['07']}{dias_restantes}")
            relatorio.append(f"{textos['labels']['08']}{textos['labels']['09']}")
            relatorio.append(f"{textos['labels']['10']}{vl_total} R$")
            relatorio.append(f"{textos['labels']['11']}{vl_disponivel} R$")
            relatorio.append(f"{textos['labels']['12']}{vl_recomendado:.2f} R$")
            relatorio.append(" ")
            rotulo = alinhamento_texto(texto=(textos['labels']['03']), caracter="-")
            relatorio.append(rotulo)
            relatorio.append(" ")
            relatorio.append(f"{textos['labels']['13']}{vl_transporte} R$")
            relatorio.append(f"{textos['labels']['14']}{vl_alimentacao} R$")
            relatorio.append(f"{textos['labels']['15']}{vl_moradia} R$")
            relatorio.append(f"{textos['labels']['16']}{vl_saude} R$")
            relatorio.append(f"{textos['labels']['17']}{vl_lazer} R$")
            relatorio.append(f"{textos['labels']['18']}{vl_pg_fatura} R$")
            relatorio.append(f"{textos['labels']['19']}{vl_gastos_ocasionais} R$")
            relatorio.append(f"{textos['labels']['20']}{vl_outros} R$")
            relatorio.append(f"{textos['labels']['21']}{vl_educacao} R$")
            relatorio.append(f"{textos['labels']['22']}{vl_investimentos} R$")
            relatorio.append(f"{textos['labels']['23']}{vl_compras} R$")
            relatorio.append(" ")
            rotulo = alinhamento_texto(texto=(textos['labels']['04']), caracter="-")
            relatorio.append(rotulo)
            relatorio.append(" ")
            relatorio.append(f"{textos['labels']['24']}{qtd_debitos_pendentes}")
            relatorio.append(f"{textos['labels']['25']}{vl_pendente} R$")
            relatorio.append(" ")
            cabecalho = ["DESCRIÇÃO", "MÊS DT COMPRA", "ANO DT COMPPRA", "PARCELAS PENDENTES", "VALOR TOTAL", "VALOR PARCELA", "VALOR PENDENTE", "MÊS ÚLTIMO DÉBITO", "ANO ÚLTIMO DÉBITO"]
            tabela = tabulate(tb_debitos_pendentes, headers=cabecalho, tablefmt="grid")
            relatorio.append(tabela)
            relatorio.append(" ")
            rotulo = alinhamento_texto(texto=(textos['labels']['05']), caracter="-")
            relatorio.append(rotulo)
            relatorio.append(" ")
            cabecalho = ["MÊS", "ANO", "ORÇAMENTO MENSAL", "VALOR GASTO", "DISPONÍVEL", "% ORÇAMENTO UTILIZADO", "QTD TRANSAÇÕES", "MAIOR GASTO", "ACUMULADO - ANO ATUAL", "VARIAÇÃO GASTO", "% VARIAÇÃO GASTO"]
            tabela = tabulate(tb_resumo_mensal, headers=cabecalho, tablefmt="grid")
            relatorio.append(tabela)
            
            return relatorio
        
    def export(self, array):
            destino = r"C:\Users\Pedro Henrique\Documents\Projetos\ACOMPANHAMENTO_FINANCEIRO\app\Relatórios"
            timestamp = str(datetime.today())
            timestamp = timestamp.replace(":", ".")
            nome_arquivo = f"DEMONSTRATIVO FINANCEIRO{timestamp}.txt"
            os.makedirs(destino, exist_ok=True)
            caminho = os.path.join(destino, nome_arquivo)
            with open(caminho, "w", encoding="utf-8") as f:
                    f.write("\n".join(array))
            