import tkinter as tk
from tkinter import ttk, messagebox
from database.conexao import conectar
from datetime import datetime
import os

# --- IDENTIDADE VISUAL CRISTAL HOTEL ---
COR_VERMELHO = "#B22222"
COR_AMARELO = "#FFD700"
COR_BRANCO = "#FFFFFF"
COR_FUNDO = "#FDF5E6"

class TelaAjudante:
    def __init__(self, root, comando_voltar=None):
        self.root = root
        self.comando_voltar = comando_voltar
        self.root.title("Cristal Hotel - Ajudantes Diaristas")
        self.root.configure(bg=COR_FUNDO)
        
        self.criar_widgets()
        self.carregar_dados()

    def criar_widgets(self):
        # HEADER
        header = tk.Frame(self.root, bg=COR_VERMELHO, pady=15)
        header.pack(fill="x")
        tk.Frame(header, bg=COR_AMARELO, height=3).pack(fill="x", side="bottom")

        if self.comando_voltar:
            tk.Button(header, text="⏪ VOLTAR", bg=COR_VERMELHO, fg=COR_AMARELO, 
                      font=("Helvetica", 11, "bold"), relief="flat", cursor="hand2", 
                      activebackground=COR_VERMELHO, activeforeground=COR_BRANCO, 
                      command=self.comando_voltar).place(x=15, y=10)

        tk.Label(header, text="CRISTAL HOTEL", font=("Helvetica", 20, "bold"), bg=COR_VERMELHO, fg=COR_BRANCO).pack()
        tk.Label(header, text="CONTROLE DE AJUDANTES / DIARISTAS", font=("Helvetica", 9, "bold"), bg=COR_VERMELHO, fg=COR_AMARELO).pack()

        # --- CADASTRO RÁPIDO (1 CLIQUE) ---
        frame_cad = tk.Frame(self.root, bg=COR_BRANCO, pady=15, padx=20)
        frame_cad.pack(fill="x", padx=30, pady=15)
        
        tk.Label(frame_cad, text="NOVA DIÁRIA RÁPIDA (Auto: Hoje, 08h às 16h)", font=("Helvetica", 11, "bold"), bg=COR_BRANCO, fg=COR_VERMELHO).pack(anchor="w", pady=(0, 10))
        
        form_linha = tk.Frame(frame_cad, bg=COR_BRANCO)
        form_linha.pack(fill="x")

        tk.Label(form_linha, text="Nome do Ajudante:", bg=COR_BRANCO, font=("Helvetica", 10, "bold")).pack(side="left", padx=(0, 5))
        self.ent_nome = tk.Entry(form_linha, width=30, font=("Helvetica", 11))
        self.ent_nome.pack(side="left", padx=(0, 20))

        tk.Label(form_linha, text="Valor da Diária (R$):", bg=COR_BRANCO, font=("Helvetica", 10, "bold")).pack(side="left", padx=(0, 5))
        self.ent_valor = tk.Entry(form_linha, width=12, font=("Helvetica", 11))
        self.ent_valor.insert(0, "60.00") # Preço padrão sugerido (você pode apagar na hora de usar)
        self.ent_valor.pack(side="left", padx=(0, 20))

        tk.Button(form_linha, text="➕ REGISTRAR DIÁRIA", bg=COR_VERMELHO, fg=COR_BRANCO, font=("Helvetica", 10, "bold"), 
                  cursor="hand2", relief="flat", command=self.salvar_diaria).pack(side="left", padx=10, ipady=3, ipadx=10)

        # --- FILTROS E GERAÇÃO DE RECIBO QUINZENAL ---
        frame_filtro = tk.Frame(self.root, bg=COR_FUNDO)
        frame_filtro.pack(fill="x", padx=30, pady=5)

        tk.Label(frame_filtro, text="Mês:", bg=COR_FUNDO, font=("Helvetica", 10, "bold")).pack(side="left")
        self.cb_mes = ttk.Combobox(frame_filtro, values=[str(i).zfill(2) for i in range(1, 13)], width=4)
        self.cb_mes.set(datetime.now().strftime("%m"))
        self.cb_mes.pack(side="left", padx=5)

        tk.Label(frame_filtro, text="Ano:", bg=COR_FUNDO, font=("Helvetica", 10, "bold")).pack(side="left")
        self.ent_ano = tk.Entry(frame_filtro, width=6)
        self.ent_ano.insert(0, str(datetime.now().year))
        self.ent_ano.pack(side="left", padx=5)

        self.var_quinzena = tk.StringVar(value="T")
        tk.Radiobutton(frame_filtro, text="1ª Quinz.", variable=self.var_quinzena, value="1", bg=COR_FUNDO).pack(side="left", padx=5)
        tk.Radiobutton(frame_filtro, text="2ª Quinz.", variable=self.var_quinzena, value="2", bg=COR_FUNDO).pack(side="left", padx=5)
        tk.Radiobutton(frame_filtro, text="Mês Todo", variable=self.var_quinzena, value="T", bg=COR_FUNDO).pack(side="left", padx=5)

        tk.Button(frame_filtro, text="🔍 FILTRAR TABELA", bg=COR_AMARELO, fg=COR_VERMELHO, font=("Helvetica", 9, "bold"), cursor="hand2", relief="flat", command=self.carregar_dados).pack(side="left", padx=15)
        
        # O Botão de gerar a folha diretamente pela tela
        tk.Button(frame_filtro, text="📄 GERAR RECIBO QUINZENAL (PDF)", bg="#107C10", fg=COR_BRANCO, font=("Helvetica", 10, "bold"), cursor="hand2", relief="flat", command=self.gerar_recibo).pack(side="right")

        # --- TABELA E TOTAIS ---
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"), background=COR_VERMELHO, foreground=COR_BRANCO)
        
        self.tabela = ttk.Treeview(self.root, columns=("id", "nome", "data", "entrada", "saida", "valor"), show="headings", height=12)
        self.tabela.heading("id", text="ID")
        self.tabela.heading("nome", text="Nome do Ajudante")
        self.tabela.heading("data", text="Data")
        self.tabela.heading("entrada", text="Entrada")
        self.tabela.heading("saida", text="Saída")
        self.tabela.heading("valor", text="Valor Diária")
        
        self.tabela.column("id", width=50, anchor="center")
        self.tabela.column("data", width=100, anchor="center")
        self.tabela.column("entrada", width=80, anchor="center")
        self.tabela.column("saida", width=80, anchor="center")
        self.tabela.column("valor", width=100, anchor="center")
        
        self.tabela.pack(fill="both", expand=True, padx=30, pady=10)

        frame_soma = tk.Frame(self.root, bg=COR_FUNDO)
        frame_soma.pack(fill="x", padx=30, pady=(0, 20))
        
        tk.Button(frame_soma, text="🗑️ EXCLUIR SELECIONADO", bg="#8B0000", fg=COR_BRANCO, font=("Helvetica", 9, "bold"), cursor="hand2", relief="flat", command=self.excluir_ajudante).pack(side="left")
        
        self.lbl_soma = tk.Label(frame_soma, text="TOTAL NO PERÍODO: R$ 0.00", font=("Helvetica", 14, "bold"), bg=COR_FUNDO, fg=COR_VERMELHO)
        self.lbl_soma.pack(side="right")

    def salvar_diaria(self):
        nome = self.ent_nome.get().strip()
        valor_str = self.ent_valor.get().strip()

        if not nome or not valor_str:
            messagebox.showwarning("Aviso", "Preencha o Nome e o Valor da diária!")
            return

        try:
            v_float = float(valor_str.replace(",", "."))
        except ValueError:
            messagebox.showerror("Erro", "O valor deve ser um número válido (ex: 60.00)!")
            return

        # Puxa o dia atual e define a jornada como 8h (08:00 as 16:00) automaticamente
        agora = datetime.now()
        data_str = agora.strftime("%d/%m/%Y")
        entrada = "08:00"
        saida = "16:00"

        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO ajudantes (nome, data, entrada, saida, valor_diaria) VALUES (?, ?, ?, ?, ?)",
                           (nome, data_str, entrada, saida, v_float))
            conn.commit()
            conn.close()
            
            # Nota: O nome não apaga do campo para facilitar se for cadastrar ele no dia seguinte!
            messagebox.showinfo("Sucesso", f"Diária de {nome} registrada com sucesso hoje ({data_str})!")
            self.carregar_dados()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {e}")

    def carregar_dados(self):
        for i in self.tabela.get_children(): self.tabela.delete(i)
        
        try:
            mes = int(self.cb_mes.get())
            ano = int(self.ent_ano.get())
            periodo = self.var_quinzena.get()
            
            from financeiro.calculos import obter_datas_periodo
            str_i, str_f = obter_datas_periodo(mes, ano, periodo)
            dt_inicio = datetime.strptime(str_i, "%Y-%m-%d")
            dt_fim = datetime.strptime(str_f, "%Y-%m-%d")
            
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ajudantes ORDER BY id DESC")
            registros = cursor.fetchall()
            conn.close()

            total = 0.0
            for row in registros:
                r_data = row[2]
                try:
                    # Sistema tenta entender datas gravadas em formatos antigos e novos
                    if "-" in r_data:
                        dt_reg = datetime.strptime(r_data, "%Y-%m-%d")
                    else:
                        dt_reg = datetime.strptime(r_data, "%d/%m/%Y")
                except Exception:
                    continue 
                
                # Se estiver dentro do filtro (Mês e Quinzena selecionados), ele joga na tela
                if dt_inicio <= dt_reg <= dt_fim:
                    data_exibicao = dt_reg.strftime("%d/%m/%Y")
                    self.tabela.insert("", "end", values=(row[0], row[1], data_exibicao, row[3], row[4], f"R$ {row[5]:.2f}"))
                    total += float(row[5])
            
            self.lbl_soma.config(text=f"TOTAL NO PERÍODO: R$ {total:.2f}")

        except Exception as e:
            print(f"Erro no filtro: {e}")

    def excluir_ajudante(self):
        sel = self.tabela.selection()
        if not sel: return
        
        if messagebox.askyesno("Confirmar", "Deseja excluir este registro de diária?"):
            item_id = self.tabela.item(sel[0], "values")[0]
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM ajudantes WHERE id = ?", (item_id,))
            conn.commit()
            conn.close()
            self.carregar_dados()

    def gerar_recibo(self):
        itens = self.tabela.get_children()
        if not itens:
            messagebox.showwarning("Aviso", "A tabela está vazia. Filtre um período que possua diárias!")
            return
        
        # Agrupa os ajudantes que estão na tela para somar seus ganhos
        agrupado = {}
        for item in itens:
            v = self.tabela.item(item, "values")
            nome = v[1]
            valor = float(v[5].replace("R$ ", ""))
            if nome not in agrupado:
                agrupado[nome] = {"dias": 0, "total": 0.0}
            agrupado[nome]["dias"] += 1
            agrupado[nome]["total"] += valor

        try:
            mes = int(self.cb_mes.get())
            ano = int(self.ent_ano.get())
            periodo = self.var_quinzena.get()
            
            from financeiro.calculos import obter_datas_periodo
            data_i, data_f = obter_datas_periodo(mes, ano, periodo)
            data_i_br = datetime.strptime(data_i, "%Y-%m-%d").strftime("%d/%m/%Y")
            data_f_br = datetime.strptime(data_f, "%Y-%m-%d").strftime("%d/%m/%Y")

            # Aproveita o layout profissional do PDF já criado!
            from financeiro.recibo_pdf import ReciboCompacto
            gerador = ReciboCompacto()
            contador = 0

            for nome, info in agrupado.items():
                dados_pdf = {
                    "nome": nome,
                    "cargo": "Ajudante Diarista",
                    "inicio": data_i_br,
                    "fim": data_f_br,
                    "horas": f"{info['dias']} Diárias (8h/dia)",
                    "salario": f"{info['total']:.2f}",
                    "cpf": "Não Informado"
                }

                if contador > 0 and contador % 3 == 0:
                    gerador.add_page()
                
                gerador.gerar_layout_recibo(dados_pdf, contador % 3)
                contador += 1

            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            pasta_recibos = os.path.join(base_dir, "recibos_gerados")
            if not os.path.exists(pasta_recibos): os.makedirs(pasta_recibos)
            
            nome_arquivo = os.path.join(pasta_recibos, f"Recibo_Ajudantes_{mes}_{ano}_{periodo}.pdf")
            gerador.salvar(nome_arquivo)

            # Abre o PDF gerado automaticamente
            import subprocess, sys
            abspath = os.path.abspath(nome_arquivo)
            if os.name == 'nt':
                os.startfile(abspath)
            else:
                cmd = ['open', abspath] if sys.platform == 'darwin' else ['xdg-open', abspath]
                subprocess.run(cmd)

            messagebox.showinfo("Sucesso", f"Folha de Pagamento dos Ajudantes gerada!\n\nSalvo em: {nome_arquivo}")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao gerar recibo: {e}")