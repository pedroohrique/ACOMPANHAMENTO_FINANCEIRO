import locale
from logging import log
from app.database.querys import (
    fg_total_exp,
    fg_spent_by_category,
    fg_outstanding_debts,
    fg_active_installments,
    fg_value_pending,
    fg_monthly_summary,
    query_money_flow
)
from datetime import datetime
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, NextPageTemplate, BaseDocTemplate, Frame, PageTemplate  # >>> ADICIONADO
)
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.colors import black, whitesmoke
from reportlab.lib.units import cm
from calendar import monthrange
from app.utils.logger import log_builder
from dotenv import load_dotenv
from copy import copy
import os


class GenerateFile:
    def __init__(self, mes_visualizacao, ano_vizualizacao):
        self.mes_visualizacao = mes_visualizacao
        self.ano_visualizacao = ano_vizualizacao
        load_dotenv(r"C:\Users\Pedro Henrique\Documents\DEV\Projetos\ACOMPANHAMENTO_FINANCEIRO\app\utils\.env")
        self.periodo = (self.mes_visualizacao, self.ano_visualizacao)
        self.logging = log_builder("file_generator.py")
        locale.setlocale(locale.LC_TIME, "Portuguese_Brazil.1252")
        self.export_pdf()

    def moeda(self, valor):
        try:
            if valor is None or valor == "":
                valor = 0
            valor = float(valor)
            return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        except Exception:
            return "R$ 0,00"

    def percentual(self, valor):
        try:
            if valor is None or valor == "":
                valor = 0
            return f"{float(valor):.2f}%"
        except Exception:
            return "0,00%"

    def dados_relatorio(self, periodo):
        vl_total = fg_total_exp(params=periodo)
        vl_categoria = fg_spent_by_category(params=periodo)
        debitos_pendentes = fg_outstanding_debts(params=(0, 1))
        qtd_debitos_pendentes = fg_active_installments(params=(1, 0))
        vl_pendente = fg_value_pending(params=(1, 0))
        resumo_mensal = fg_monthly_summary(params=(self.ano_visualizacao))
        vl_disponivel = (7500 - (vl_total or 0))
        vls_categoria = fg_spent_by_category(params=periodo)
        vls_fluxo_caixa = query_money_flow(params=periodo)

        dados = {
            "vl_total": vl_total,
            "vl_categoria": vl_categoria,
            "debitos_pendentes": debitos_pendentes,
            "qtd_debitos_pendentes": qtd_debitos_pendentes,
            "vl_pendente": vl_pendente,
            "resumo_mensal": resumo_mensal,
            "vl_disponivel": vl_disponivel,
            "vls_cat": [vls_categoria],
            "vls_fluxo_caixa": vls_fluxo_caixa
        }
        return dados

    def calcula_dias_restantes(self):
        dt_atual = datetime.today()
        ultimo_dia_mes = monthrange(dt_atual.year, dt_atual.month)[1]
        fim_mes = datetime(dt_atual.year, dt_atual.month, ultimo_dia_mes)
        dias_restantes = ((fim_mes - dt_atual).days + 1)
        return dias_restantes

    # =========================
    def export_pdf(self):
        destino_relatorio = os.getenv("DESTINO_RELATORIO")
        if not destino_relatorio:
            self.logging.error("Caminho para salvar o relatório não está definido.")
            return

        try:
            titulo = f"DEMONSTRATIVO_FINANCEIRO_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            caminho_arquivo = os.path.join(destino_relatorio, titulo)

            # >>> ALTERADO
            doc = BaseDocTemplate(
                caminho_arquivo,
                rightMargin=2*cm, leftMargin=2*cm,
                topMargin=2*cm, bottomMargin=2*cm
            )

            # >>> ADICIONADO
            frame_retrato = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="retrato")
            frame_landscape = Frame(doc.leftMargin, doc.bottomMargin, doc.height, doc.width, id="landscape")

            template_retrato = PageTemplate(id="retrato", frames=[frame_retrato], pagesize=A4)
            template_landscape = PageTemplate(id="landscape", frames=[frame_landscape], pagesize=landscape(A4))

            doc.addPageTemplates([template_retrato, template_landscape])

            styles = getSampleStyleSheet()
            titulo = styles["Title"]
            normal = styles["BodyText"]
            titulo.alignment = TA_CENTER
            info_style = copy(normal)
            info_style.alignment = TA_RIGHT
            subtitulos = copy(styles["Heading2"])
            subtitulos.leftIndent = -50

            elementos = []
            dados_relatorio = self.dados_relatorio(periodo=self.periodo)
            dias_restantes = self.calcula_dias_restantes()

            vl_total_num = dados_relatorio["vl_total"] or 0
            vl_disp_num = dados_relatorio["vl_disponivel"] or 0

            vl_total = self.moeda(vl_total_num)
            vl_disponivel = self.moeda(vl_disp_num)
            vl_p_categoria = dados_relatorio["vls_cat"][0]
            vl_rec = vl_disp_num / dias_restantes if dias_restantes else 0
            vl_rec = self.moeda(vl_rec)

            # ---------------------------- CABEÇALHO ---------------------------- #
            elementos.append(Paragraph(f"Demonstrativo Financeiro Pessoal - {self.ano_visualizacao}", titulo))
            elementos.append(Spacer(1, 12))
            elementos.append(Paragraph(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}", info_style))
            elementos.append(Spacer(1, 30))

            # ---------------------------- VISÃO GERAL ---------------------------- #
            elementos.append(Paragraph(datetime.now().strftime("Visão Geral - %B/%Y"), subtitulos))
            elementos.append(Spacer(1, 12))

            tabela_visao_geral_data = [
                ["Total de Gastos no Mês:", vl_total],
                ["Valor Disponível para o Mês:", vl_disponivel],
                [f"Valor Diário Recomendado (Restantes {dias_restantes} dias):", vl_rec]
            ]

            t1 = Table(tabela_visao_geral_data, colWidths=[14*cm, 6*cm])
            elementos.append(t1)

            t1.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), whitesmoke),
                ("GRID", (0, 0), (-1, -1), 0.5, black),
                ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 12),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
            ]))
            elementos.append(Spacer(1, 25))

            # ---------------------------- GASTOS POR CATEGORIA ---------------------------- #
            elementos.append(Paragraph(datetime.now().strftime("Gastos por Categoria - %B/%Y"), subtitulos))
            elementos.append(Spacer(1, 12))
            tab_categoria = [["Categoria", "Valor Gasto R$", "Percentual do Total (%)"]]

            for categoria, valor in vl_p_categoria.items():
                nome_cat = categoria.capitalize()
                vl_gasto = self.moeda(valor)
                perc_total = self.percentual((valor / vl_total_num * 100) if vl_total_num else 0)
                tab_categoria.append([nome_cat, vl_gasto, perc_total])

            t2 = Table(tab_categoria, colWidths=[8*cm, 6*cm, 6*cm])
            t2.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), whitesmoke),
                ("GRID", (0, 0), (-1, -1), 0.5, black),
                ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 12),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
            ]))

            elementos.append(t2)
            elementos.append(Spacer(1, 5))

            # ---------------------------- DÉBITOS PENDENTES ---------------------------- #
            elementos.append(Paragraph("Débitos Pendentes", subtitulos))
            elementos.append(Spacer(1, 12))

            debitos_pendentes = dados_relatorio["debitos_pendentes"]
            qtd_debitos_pendentes = dados_relatorio["qtd_debitos_pendentes"]
            vl_pendente = self.moeda(dados_relatorio["vl_pendente"])

            tab_debitos = [
                ["Quantidade de Débitos Pendentes:", str(qtd_debitos_pendentes)],
                ["Valor Total Pendente:", vl_pendente]
            ]

            t3 = Table(tab_debitos, colWidths=[14*cm, 6*cm])
            t3.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), whitesmoke),
                ("GRID", (0, 0), (-1, -1), 0.5, black),
                ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 12),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
            ]))

            elementos.append(t3)
            elementos.append(Spacer(1, 12))

            tab_detalhes_debitos = [[
                "Descrição", "Débitos", "Total R$", "Pendente R$", "Último Débito"
            ]]

            for debito in debitos_pendentes:
                descricao = debito[0]
                debitos_qtd = debito[3]
                valor_total = debito[4]
                valor_pendente = debito[6]
                mes_ultimo_debito = debito[7]
                ano_ultimo_debito = debito[8]
                ano_mes_ultimo_debito = f"{mes_ultimo_debito}/{ano_ultimo_debito}"

                tab_detalhes_debitos.append([
                    descricao, str(debitos_qtd), valor_total,
                    valor_pendente, ano_mes_ultimo_debito,
                ])

            t4 = Table(tab_detalhes_debitos, colWidths=[9*cm, 2*cm, 3*cm, 3*cm, 3*cm])
            t4.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), whitesmoke),
                ("GRID", (0, 0), (-1, -1), 0.5, black),
                ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
            ]))

            elementos.append(t4)
            elementos.append(Spacer(1, 25))

            # ---------------------------- FLUXO ---------------------------- #
            dados_fluxo = dados_relatorio["vls_fluxo_caixa"]

            elementos.append(Paragraph(datetime.now().strftime("Fluxo de Caixa - %B/%Y"), subtitulos))
            elementos.append(Spacer(1, 12))

            tabela_fluxo = [["Entradas R$", "Saídas R$", "Custo Médio R$", "Saldo R$"]]

            for fluxo in dados_fluxo:
                entradas = self.moeda(fluxo[0])
                saidas = self.moeda(fluxo[1])
                custo = self.moeda(fluxo[2])
                saldo = self.moeda(fluxo[3])
                tabela_fluxo.append([entradas, saidas, custo, saldo])

            t_fluxo = Table(tabela_fluxo, colWidths=[5*cm, 5*cm, 5*cm, 5*cm])
            t_fluxo.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), whitesmoke),
                ("GRID", (0, 0), (-1, -1), 0.5, black),
                ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 12),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
            ]))

            elementos.append(t_fluxo)
            elementos.append(Spacer(1, 25))

            # ==================== RESUMO MENSAL (3ª PÁGINA) ==================== #
            resumo_mensal = dados_relatorio["resumo_mensal"]
            
            tabela_resumo = [[
                "Mês", "Ano", "Orçamento", "Gasto", "Saldo",
                "% Utilizado", "Transações", "Maior Gasto",
                "Acumulado", "Variação", "% Variação"
            ]]
            
            for item in resumo_mensal:
                mes = item[0]
                ano = item[1]
                orcamento = item[2]
                gasto = item[3]
                saldo = item[4]
                perc_utilizado = item[5]
                qtd = item[6]
                maior_gasto = item[7]
                acumulado = item[8] 
                variacao = item[9]
                perc_variacao = item[10]
                tabela_resumo.append([
                    str(mes), str(ano), orcamento, gasto, saldo, perc_utilizado, qtd,
                    maior_gasto, acumulado, variacao, perc_variacao
                ])

            elementos.append(NextPageTemplate("landscape"))
            elementos.append(PageBreak())
            elementos.append(Paragraph(datetime.now().strftime("Resumo Anual Consolidado - %Y"), subtitulos))
            elementos.append(Spacer(1, 12))

            

            

            t_resumo = Table(tabela_resumo, repeatRows=1, colWidths=[1.7*cm,1.7*cm,2.9*cm,2.9*cm,2.9*cm,2.9*cm,2.9*cm,2.9*cm,2.9*cm,2.9*cm,2.9*cm])
            t_resumo.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), whitesmoke),
                ("GRID", (0, 0), (-1, -1), 0.4, black),

                ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 12),
                ("FONTSIZE", (0, 1), (-1, -1), 10),

                ("ALIGN", (1, 1), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("GRID", (0, 0), (-1, -1), 0.8, black),
                # 👉 ESPAÇAMENTO
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 13),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
            ]))

            elementos.append(t_resumo)

            # ---------------------------- FINAL ---------------------------- #
            doc.build(elementos)
            return caminho_arquivo

        except Exception as e:
            self.logging.error(f"Falha ao exportar o documento PDF: {e}")
