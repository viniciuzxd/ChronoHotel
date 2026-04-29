import tkinter as tk
from tkinter import ttk, messagebox
from financeiro.calculos import gerar_relatorio_pagamento, obter_datas_periodo
from financeiro.recibo_pdf import ReciboCompacto
from database.conexao import conectar
import os
from datetime import datetime

# --- IDENTIDADE VISUAL CRISTAL HOTEL ---
COR_VERMELHO = "#B22222"
COR_AMARELO = "#FFD700"
COR_BRANCO = "#FFFFFF"
COR_FUNDO = "#FDF5E6"
COR_TEXTO = "#1A1A1A"

class TelaFinanceiroRelatorio:
    def __init__(self, root, nivel_acesso="Gerente", comando_voltar=None):
        self.root = root
        self.comando_voltar = comando_voltar # Salva a função de voltar
        
        self.root.title("Cristal Hotel - Financeiro")
        self.root.configure(bg=COR_FUNDO)
        self.nivel_acesso = nivel_acesso
        
        self.criar_widgets()

    def criar_widgets(self):
        # Header Moderno
        header = tk.Frame(self.root, bg=COR_VERMELHO, pady=15)
        header.pack(fill="x")
        
        # Faixa amarela
        tk.Frame(header, bg=COR_AMARELO, height=5).pack(fill="x", side="bottom")

        # --- BOTÃO DE VOLTAR NO CANTO SUPERIOR ESQUERDO ---
        if self.comando_voltar:
            btn_voltar = tk.Button(header, text="⏪ VOLTAR", bg=COR_VERMELHO, fg=COR_AMARELO, 
                                   font=("Helvetica", 11, "bold"), relief="flat", cursor="hand2", 
                                   activebackground=COR_VERMELHO, activeforeground=COR_BRANCO,
                                   command=self.comando_voltar)
            btn_voltar.place(x=15, y=10)

        tk.Label(header, text="CRISTAL HOTEL", font=("Helvetica", 22, "bold"), bg=COR_VERMELHO, fg=COR_BRANCO).pack()
        tk.Label(header, text="GESTÃO FINANCEIRA E EMISSÃO DE RECIBOS", font=("Helvetica", 9, "bold"), bg=COR_VERMELHO, fg=COR_AMARELO).pack()

        # Filtros
        frame_filtros = tk.Frame(self.root, bg=COR_FUNDO, pady=20)
        frame_filtros.pack(fill="x", padx=30)

        tk.Label(frame_filtros, text="Mês:", bg=COR_FUNDO, fg=COR_VERMELHO, font=("Helvetica", 10, "bold")).pack(side="left", padx=5)
        self.cb_mes = ttk.Combobox(frame_filtros, values=[str(i).zfill(2) for i in range(1, 13)], width=5)
        self.cb_mes.set(datetime.now().strftime("%m"))
        self.cb_mes.pack(side="left", padx=5)
        self.cb_mes.bind("<<ComboboxSelected>>", lambda e: self.carregar_dados())

        tk.Label(frame_filtros, text="Ano:", bg=COR_FUNDO, fg=COR_VERMELHO, font=("Helvetica", 10, "bold")).pack(side="left", padx=5)
        self.ent_ano = tk.Entry(frame_filtros, width=6, font=("Helvetica", 10))
        self.ent_ano.insert(0, str(datetime.now().year))
        self.ent_ano.pack(side="left", padx=5)
        self.ent_ano.bind("<Return>", lambda e: self.carregar_dados())

        # Seleção de Período
        quinzena_atual = "1" if datetime.now().day <= 15 else "2"
        self.var_quinzena = tk.StringVar(value=quinzena_atual)

        tk.Radiobutton(frame_filtros, text="1ª Quinzena", variable=self.var_quinzena, value="1", 
                       bg=COR_FUNDO, fg=COR_VERMELHO, activebackground=COR_FUNDO,
                       font=("Helvetica", 9, "bold"), command=self.carregar_dados).pack(side="left", padx=10)
        tk.Radiobutton(frame_filtros, text="2ª Quinzena", variable=self.var_quinzena, value="2",
                       bg=COR_FUNDO, fg=COR_VERMELHO, activebackground=COR_FUNDO,
                       font=("Helvetica", 9, "bold"), command=self.carregar_dados).pack(side="left", padx=10)
        tk.Radiobutton(frame_filtros, text="Mês Todo", variable=self.var_quinzena, value="T",
                       bg=COR_FUNDO, fg=COR_VERMELHO, activebackground=COR_FUNDO,
                       font=("Helvetica", 9, "bold"), command=self.carregar_dados).pack(side="left", padx=10)

        # Botão Atualizar
        self.btn_recarregar = tk.Button(frame_filtros, text="🔄 ATUALIZAR TABELA", bg=COR_VERMELHO, fg=COR_BRANCO, 
                                      font=("Helvetica", 9, "bold"), relief="flat", cursor="hand2", padx=10,
                                      command=self.carregar_dados)
        self.btn_recarregar.pack(side="right", padx=10)

        # Tabela Profissional
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background=COR_BRANCO, fieldbackground=COR_BRANCO, rowheight=30, font=("Helvetica", 10))
        style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"), background=COR_VERMELHO, foreground=COR_BRANCO)
        
        self.tabela = ttk.Treeview(self.root, columns=("id", "nome", "cargo", "horas", "valor"), show="headings")
        self.tabela.heading("id", text="ID")
        self.tabela.heading("nome", text="Nome")
        self.tabela.heading("cargo", text="Cargo")
        self.tabela.heading("horas", text="Horas Totais")
        self.tabela.heading("valor", text="Total a Receber")
        
        self.tabela.column("id", width=50, anchor="center")
        self.tabela.column("nome", width=250)
        self.tabela.column("cargo", width=180)
        self.tabela.column("horas", width=130, anchor="center")
        self.tabela.column("valor", width=130, anchor="center")
        
        self.tabela.pack(fill="both", expand=True, padx=30, pady=10)

        # Ações do Gerente
        if self.nivel_acesso == "Gerente":
            btn_frame_acoes = tk.Frame(self.root, bg=COR_FUNDO, pady=20)
            btn_frame_acoes.pack(fill="x", padx=30)

            self.btn_imprimir_um = tk.Button(btn_frame_acoes, text="🖨️ EMITIR RECIBO SELECIONADO", 
                                          state="disabled", bg=COR_BRANCO, fg=COR_VERMELHO, 
                                          font=("Helvetica", 10, "bold"), height=2, relief="flat",
                                          highlightthickness=1, highlightbackground=COR_VERMELHO,
                                          command=self.imprimir_selecionado)
            self.btn_imprimir_um.pack(side="left", padx=5)

            self.btn_imprimir_todos = tk.Button(btn_frame_acoes, text="📄 GERAR TODOS (Lote 3x folha)", 
                                          bg=COR_VERMELHO, fg=COR_BRANCO, 
                                          font=("Helvetica", 10, "bold"), height=2, relief="flat",
                                          command=self.imprimir_todos)
            self.btn_imprimir_todos.pack(side="left", padx=5)
            
            self.tabela.bind("<<TreeviewSelect>>", lambda e: self.btn_imprimir_um.config(state="normal"))

        # Carrega dados iniciais
        self.root.after(100, self.carregar_dados)

    def carregar_dados(self):
        # Limpa tabela
        for i in self.tabela.get_children(): self.tabela.delete(i)
        
        try:
            mes_str = self.cb_mes.get()
            ano_str = self.ent_ano.get()
            
            if not mes_str or not ano_str:
                return

            mes = int(mes_str)
            ano = int(ano_str)
            tipo_periodo = self.var_quinzena.get()
            
            data_i, data_f = obter_datas_periodo(mes, ano, tipo_periodo)
            
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome, cargo, cpf FROM funcionarios")
            funcionarios = cursor.fetchall()
            conn.close()

            found_any = False
            for f_id, nome, cargo, cpf in funcionarios:
                res = gerar_relatorio_pagamento(f_id, data_i, data_f)
                if res:
                    # Garante que o CPF seja string para as tags
                    cpf_str = str(cpf) if cpf else "---"
                    self.tabela.insert("", "end", values=(f_id, nome, cargo, res['horas_formatadas'], f"R$ {res['salario']:.2f}"), 
                                   tags=(cpf_str,))
                    found_any = True
            
            if not found_any and hasattr(self, 'btn_imprimir_um'):
                self.btn_imprimir_um.config(state="disabled")

        except ValueError:
            messagebox.showerror("Erro", "Mês ou Ano inválidos!")
        except Exception as e:
            messagebox.showerror("Erro ao carregar", f"Ocorreu um erro: {e}")

    def imprimir_selecionado(self):
        selecao = self.tabela.selection()
        if not selecao:
            messagebox.showwarning("Atenção", "Selecione um funcionário na tabela!")
            return
            
        item = selecao[0]
        valores = self.tabela.item(item, "values")
        
        if valores[3] == "0h00m":
            messagebox.showwarning("Atenção", f"O funcionário {valores[1]} não possui horas trabalhadas no período selecionado!")
            return

        tags = self.tabela.item(item, "tags")
        cpf = tags[0] if tags else "---"
        
        mes = int(self.cb_mes.get())
        ano = int(self.ent_ano.get())
        tipo_periodo = self.var_quinzena.get()
        
        data_i, data_f = obter_datas_periodo(mes, ano, tipo_periodo)
        
        data_i_br = datetime.strptime(data_i, "%Y-%m-%d").strftime("%d/%m/%Y")
        data_f_br = datetime.strptime(data_f, "%Y-%m-%d").strftime("%d/%m/%Y")

        dados_pdf = {
            "nome": valores[1],
            "cargo": valores[2],
            "inicio": data_i_br,
            "fim": data_f_br,
            "horas": valores[3],
            "salario": valores[4].replace("R$ ", ""),
            "cpf": cpf
        }

        try:
            gerador = ReciboCompacto()
            gerador.gerar_layout_recibo(dados_pdf, 0) 
            
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            pasta_recibos = os.path.join(base_dir, "recibos_gerados")
            if not os.path.exists(pasta_recibos):
                os.makedirs(pasta_recibos)
            
            nome_limpo = "".join([c for c in valores[1] if c.isalnum() or c == " "]).replace(" ", "_")
            nome_arquivo = os.path.join(pasta_recibos, f"Recibo_{nome_limpo}_{mes}_{ano}_{tipo_periodo}.pdf")
            
            gerador.salvar(nome_arquivo)
            
            if not os.path.exists(nome_arquivo):
                raise FileNotFoundError(f"O arquivo {nome_arquivo} não foi criado.")

            abspath = os.path.abspath(nome_arquivo)
            if os.name == 'nt':
                try:
                    os.startfile(abspath)
                except Exception:
                    import subprocess
                    subprocess.Popen([abspath], shell=True)
            else:
                import subprocess
                import sys
                cmd = ['open', abspath] if sys.platform == 'darwin' else ['xdg-open', abspath]
                subprocess.run(cmd)
                
            messagebox.showinfo("Sucesso", f"Recibo gerado com sucesso!\nSalvo em: {nome_arquivo}")
        except Exception as e:
            messagebox.showerror("Erro na Geração", f"Não foi possível gerar ou abrir o PDF.\n\nDetalhes: {str(e)}")

    def imprimir_todos(self):
        itens = self.tabela.get_children()
        if not itens:
            messagebox.showwarning("Atenção", "Não há dados na tabela para gerar recibos!")
            return

        try:
            mes = int(self.cb_mes.get())
            ano = int(self.ent_ano.get())
            tipo_periodo = self.var_quinzena.get()
            data_i, data_f = obter_datas_periodo(mes, ano, tipo_periodo)
            data_i_br = datetime.strptime(data_i, "%Y-%m-%d").strftime("%d/%m/%Y")
            data_f_br = datetime.strptime(data_f, "%Y-%m-%d").strftime("%d/%m/%Y")

            gerador = ReciboCompacto()
            contador = 0
            
            for item in itens:
                valores = self.tabela.item(item, "values")
                tags = self.tabela.item(item, "tags")
                cpf = tags[0] if tags else "---"
                
                if valores[3] == "0h00m":
                    continue

                dados_pdf = {
                    "nome": valores[1],
                    "cargo": valores[2],
                    "inicio": data_i_br,
                    "fim": data_f_br,
                    "horas": valores[3],
                    "salario": valores[4].replace("R$ ", ""),
                    "cpf": cpf
                }

                if contador > 0 and contador % 3 == 0:
                    gerador.add_page()
                
                posicao_na_pagina = contador % 3
                gerador.gerar_layout_recibo(dados_pdf, posicao_na_pagina)
                contador += 1

            if contador == 0:
                messagebox.showwarning("Atenção", "Nenhum funcionário com horas trabalhadas no período!")
                return

            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            pasta_recibos = os.path.join(base_dir, "recibos_gerados")
            if not os.path.exists(pasta_recibos):
                os.makedirs(pasta_recibos)
                
            nome_arquivo = os.path.join(pasta_recibos, f"Recibos_Lote_{mes}_{ano}_{tipo_periodo}.pdf")
            gerador.salvar(nome_arquivo)
            
            if not os.path.exists(nome_arquivo):
                raise FileNotFoundError(f"O arquivo {nome_arquivo} não foi criado.")

            abspath = os.path.abspath(nome_arquivo)
            if os.name == 'nt':
                try:
                    os.startfile(abspath)
                except Exception:
                    import subprocess
                    subprocess.Popen([abspath], shell=True)
            else:
                import subprocess
                import sys
                cmd = ['open', abspath] if sys.platform == 'darwin' else ['xdg-open', abspath]
                subprocess.run(cmd)
                
            messagebox.showinfo("Sucesso", f"Lote de {contador} recibos gerado!\nSalvo em: {nome_arquivo}")
        except Exception as e:
            messagebox.showerror("Erro na Geração", f"Erro ao gerar lote de PDFs.\n\nDetalhes: {str(e)}")