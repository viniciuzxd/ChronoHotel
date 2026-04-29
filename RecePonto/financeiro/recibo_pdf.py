from fpdf import FPDF
import os

class ReciboCompacto(FPDF):
    def __init__(self):
        super().__init__(orientation='P', unit='mm', format='A4')
        self.set_auto_page_break(auto=False)
        self.add_page()
        
    def gerar_layout_recibo(self, dados, posicao_y):
        # Aumentamos um pouquinho o espaçamento entre os recibos (96mm cada bloco)
        offset_y = posicao_y * 96 + 4 
        
        # --- BORDA DO RECIBO ---
        self.set_draw_color(178, 34, 34)   # Vermelho Cristal
        self.set_line_width(0.4)
        self.rect(10, offset_y, 190, 92)   # Altura do recibo definida para 92mm
        
        # --- CARREGAMENTO DA LOGO ---
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # Prioriza .jpg para evitar o bug do fundo cinza transparente do fpdf
        caminho_logo = None
        for ext in [".jpg", ".jpeg", ".png"]:
            teste = os.path.join(base_dir, f"logo{ext}")
            if os.path.exists(teste):
                caminho_logo = teste
                break

        if caminho_logo:
            # Largura reduzida para 25 para garantir que fique restrita ao cabeçalho superior
            self.image(caminho_logo, x=15, y=offset_y + 4, w=25)
        else:
            self.set_xy(15, offset_y + 8)
            self.set_font('helvetica', 'B', 14)
            self.set_text_color(178, 34, 34)
            self.cell(40, 10, 'CRISTAL HOTEL', border=0)

        # --- TÍTULO DO DOCUMENTO (Alinhado à direita no topo) ---
        self.set_xy(90, offset_y + 6)
        self.set_font('helvetica', 'B', 16)
        self.set_text_color(178, 34, 34)
        self.cell(105, 8, 'RECIBO DE PAGAMENTO', border=0, ln=0, align='R')
        
        self.set_xy(90, offset_y + 13)
        self.set_font('helvetica', 'I', 9)
        self.set_text_color(100, 100, 100)
        self.cell(105, 5, 'João Alfredo - PE | Gestão Profissional', border=0, ln=0, align='R')

        # --- LINHA DIVISÓRIA AMARELA ---
        self.set_draw_color(255, 215, 0) # Amarelo Dourado
        self.set_line_width(0.8)
        self.line(15, offset_y + 21, 195, offset_y + 21)

        # --- DADOS DO FUNCIONÁRIO (Completamente separados da logo) ---
        self.set_text_color(0, 0, 0)
        self.set_font('helvetica', 'B', 11)
        self.set_xy(15, offset_y + 24)
        self.cell(0, 6, f"NOME: {dados['nome'].upper()}")
        
        self.set_font('helvetica', '', 10)
        self.set_xy(15, offset_y + 30)
        self.cell(85, 6, f"CARGO: {dados['cargo']}")
        self.set_xy(100, offset_y + 30)
        self.cell(95, 6, f"PERÍODO: {dados['inicio']} a {dados['fim']}")
        
        self.set_xy(15, offset_y + 36)
        self.cell(0, 6, f"CPF: {dados['cpf']}")

        # --- TABELA DE LANÇAMENTOS ---
        self.set_fill_color(178, 34, 34)
        self.set_text_color(255, 255, 255)
        self.set_font('helvetica', 'B', 9)
        self.set_xy(15, offset_y + 45)
        self.cell(110, 7, ' DESCRIÇÃO', border=0, fill=True)
        self.cell(35, 7, 'HORAS', border=0, fill=True, align='C')
        self.cell(35, 7, 'TOTAL ', border=0, fill=True, align='R')

        self.set_text_color(0, 0, 0)
        self.set_font('helvetica', '', 10)
        self.set_draw_color(178, 34, 34)
        self.set_line_width(0.2)
        
        self.set_xy(15, offset_y + 52)
        self.cell(110, 9, ' Horas Trabalhadas (Quinzena)', border='B')
        self.cell(35, 9, str(dados['horas']), border='B', align='C')
        self.cell(35, 9, f"R$ {dados['salario']}", border='B', align='R')

        # --- VALOR LÍQUIDO ---
        self.set_xy(15, offset_y + 64)
        self.set_font('helvetica', 'B', 11)
        self.cell(145, 9, 'VALOR LÍQUIDO A RECEBER: ', align='R')
        
        self.set_fill_color(255, 215, 0)
        self.set_text_color(178, 34, 34)
        self.set_font('helvetica', 'B', 12)
        self.cell(35, 9, f"R$ {dados['salario']}", border=1, fill=True, align='C')

        # --- ASSINATURA (Com mais espaço) ---
        self.set_draw_color(0, 0, 0)
        self.set_text_color(0, 0, 0)
        self.set_line_width(0.3)
        self.line(90, offset_y + 85, 195, offset_y + 85) # Linha da assinatura movida para a direita
        
        self.set_xy(90, offset_y + 86)
        self.set_font('helvetica', '', 9)
        self.cell(105, 5, 'Assinatura do Colaborador', align='C')

        # --- LINHA DE CORTE ---
        if posicao_y < 2:
            self.set_draw_color(180, 180, 180)
            self.set_dash_pattern(dash=2, gap=2)
            self.line(5, offset_y + 96, 205, offset_y + 96)
            self.set_dash_pattern()

    # >>> A FUNÇÃO QUE FALTAVA FOI DEVOLVIDA AQUI <<<
    def salvar(self, nome_arquivo):
        self.output(nome_arquivo)


class RelatorioMensalGeral(FPDF):
    def __init__(self, mes, ano):
        super().__init__(orientation='P', unit='mm', format='A4')
        self.mes = mes
        self.ano = ano
        self.set_auto_page_break(auto=True, margin=15)
        self.add_page()
        self.header_relatorio()

    def header_relatorio(self):
        self.set_fill_color(178, 34, 34)
        self.rect(0, 0, 210, 40, 'F')
        self.set_fill_color(255, 215, 0)
        self.rect(0, 40, 210, 2, 'F')

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        caminho_logo = None
        for ext in [".jpg", ".jpeg", ".png"]:
            teste = os.path.join(base_dir, f"logo{ext}")
            if os.path.exists(teste):
                caminho_logo = teste
                break
        
        if caminho_logo:
            self.image(caminho_logo, x=10, y=5, w=25)
            self.set_xy(40, 12)
        else:
            self.set_xy(10, 12)

        self.set_font('helvetica', 'B', 26)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, 'CRISTAL HOTEL', ln=1)
        
        self.set_x(40 if caminho_logo else 10)
        self.set_font('helvetica', 'B', 12)
        self.set_text_color(255, 215, 0)
        self.cell(0, 10, f'RELATÓRIO MENSAL DE PONTO - {self.mes:02d}/{self.ano}', ln=1)
        self.ln(15)

    def gerar_tabela(self, registros):
        self.set_fill_color(178, 34, 34)
        self.set_text_color(255, 255, 255)
        self.set_font('helvetica', 'B', 10)
        
        col_widths = [25, 65, 25, 25, 20, 30]
        headers = ['Data', 'Funcionário', 'Entrada', 'Saída', 'Horas', 'Valor (R$)']
        
        for i in range(len(headers)):
            self.cell(col_widths[i], 10, headers[i], border=1, align='C', fill=True)
        self.ln()
        
        self.set_text_color(0, 0, 0)
        self.set_font('helvetica', '', 9)
        fill = False
        
        for r in registros:
            self.set_fill_color(245, 245, 245) if fill else self.set_fill_color(255, 255, 255)
            self.cell(col_widths[0], 8, r['data'], 1, 0, 'C', fill=True)
            self.cell(col_widths[1], 8, r['nome'], 1, 0, 'L', fill=True)
            self.cell(col_widths[2], 8, r['entrada'], 1, 0, 'C', fill=True)
            self.cell(col_widths[3], 8, r['saida'], 1, 0, 'C', fill=True)
            self.cell(col_widths[4], 8, r['horas'], 1, 0, 'C', fill=True)
            self.cell(col_widths[5], 8, f"{r['valor']}", 1, 1, 'R', fill=True)
            fill = not fill

    def salvar(self, nome_arquivo):
        self.output(nome_arquivo)