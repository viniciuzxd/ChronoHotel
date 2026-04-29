import tkinter as tk
from tkinter import ttk, messagebox
from database.backup import realizar_backup

# --- IDENTIDADE VISUAL CRISTAL HOTEL ---
COR_VERMELHO = "#B22222"  
COR_AMARELO = "#FFD700"   
COR_BRANCO = "#FFFFFF"    
COR_FUNDO = "#FDF5E6"     
COR_TEXTO = "#1A1A1A"     

class DashboardGerente:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        
        self.root.title("Cristal Hotel - Gestão Administrativa")
        self.root.geometry("1100x750")
        self.root.configure(bg=COR_FUNDO)
        
        self.main_frame = tk.Frame(self.root, bg=COR_FUNDO)
        self.main_frame.pack(fill="both", expand=True)
        
        self.criar_layout()
        self.verificar_lembrete_fechamento()

    def reconstruir_dashboard(self):
        """Limpa a janela atual e reconstrói o Dashboard do zero"""
        for widget in self.root.winfo_children():
            widget.destroy()
        self.__init__(self.root, self.username)

    def verificar_lembrete_fechamento(self):
        from datetime import datetime
        import calendar
        hoje = datetime.now()
        ultimo_dia = calendar.monthrange(hoje.year, hoje.month)[1]
        faltam = ultimo_dia - hoje.day
        
        if faltam in [0, 1, 2]:
            dias_texto = {0: "HOJE é o último dia", 1: "Falta 1 dia", 2: "Faltam 2 dias"}
            msg = f"⚠️ LEMBRETE DE FECHAMENTO ⚠️\n\n{dias_texto[faltam]} para o fim do mês!\n\nPor favor, gere o Relatório Mensal e realize o Fechamento do Mês."
            messagebox.showwarning("Aviso de Fechamento", msg)

    def criar_layout(self):
        header = tk.Frame(self.main_frame, bg=COR_VERMELHO, height=150)
        header.pack(fill="x")
        tk.Frame(header, bg=COR_AMARELO, height=5).pack(fill="x", side="bottom")

        tk.Label(header, text="CRISTAL HOTEL", font=("Helvetica", 32, "bold"), bg=COR_VERMELHO, fg=COR_BRANCO).pack(pady=(25, 0))
        tk.Label(header, text="SISTEMA DE GESTÃO DE PONTO E FINANCEIRO", font=("Helvetica", 10, "bold"), bg=COR_VERMELHO, fg=COR_AMARELO).pack(pady=(0, 20))

        btn_container = tk.Frame(self.main_frame, bg=COR_FUNDO)
        btn_container.pack(expand=True, pady=40)

        botoes = [
            ("👥 GESTÃO DE\nFUNCIONÁRIOS", self.abrir_funcionarios),
            ("🕒 REGISTRO\nDE PONTO", self.abrir_ponto),
            ("💰 RELATÓRIOS\nFINANCEIROS", self.abrir_financeiro),
            ("🔐 CONTROLE DE\nRECEPCIONISTAS", self.abrir_usuarios),
            ("📁 FECHAR MÊS /\nRELATÓRIO GERAL", self.fechar_mes_procedimento),
            ("🤝 AJUDANTES\nDIARISTAS", self.abrir_ajudantes)
        ]

        r, c = 0, 0
        for texto, comando in botoes:
            f = tk.Frame(btn_container, bg=COR_VERMELHO, padx=1, pady=1)
            f.grid(row=r, column=c, padx=20, pady=20)
            btn = tk.Button(f, text=texto, width=20, height=5, font=("Helvetica", 11, "bold"),
                            bg=COR_BRANCO, fg=COR_VERMELHO, relief="flat", borderwidth=0, 
                            cursor="hand2", command=comando, activebackground=COR_AMARELO)
            btn.pack()
            c += 1
            if c > 2: r += 1; c = 0

        footer = tk.Frame(self.main_frame, bg=COR_FUNDO, pady=10)
        footer.pack(fill="x", side="bottom")

        tk.Button(footer, text="SAIR DO SISTEMA", bg=COR_VERMELHO, fg=COR_BRANCO, font=("Helvetica", 9, "bold"),
                  relief="flat", cursor="hand2", padx=15, pady=5, command=self.finalizar_sessao).pack(side="right", padx=20)

    def fechar_mes_procedimento(self):
        for widget in self.root.winfo_children(): widget.destroy()

        header = tk.Frame(self.root, bg=COR_VERMELHO, pady=15)
        header.pack(fill="x")
        tk.Frame(header, bg=COR_AMARELO, height=5).pack(fill="x", side="bottom")

        tk.Button(header, text="⏪ VOLTAR", bg=COR_VERMELHO, fg=COR_AMARELO, font=("Helvetica", 11, "bold"), 
                  relief="flat", cursor="hand2", activebackground=COR_VERMELHO, activeforeground=COR_BRANCO,
                  command=self.reconstruir_dashboard).place(x=15, y=10)

        tk.Label(header, text="CRISTAL HOTEL", font=("Helvetica", 24, "bold"), bg=COR_VERMELHO, fg=COR_BRANCO).pack()
        tk.Label(header, text="FECHAMENTO MENSAL", font=("Helvetica", 10, "bold"), bg=COR_VERMELHO, fg=COR_AMARELO).pack()

        frame_conteudo = tk.Frame(self.root, bg=COR_FUNDO)
        frame_conteudo.pack(expand=True)

        tk.Label(frame_conteudo, text="PROCEDIMENTO DE FECHAMENTO", font=("Helvetica", 14, "bold"), bg=COR_FUNDO, fg=COR_VERMELHO).pack(pady=20)
        
        frame_inputs = tk.Frame(frame_conteudo, bg=COR_FUNDO)
        frame_inputs.pack(pady=10)

        from datetime import datetime
        mes_atual = datetime.now().month
        ano_atual = datetime.now().year

        tk.Label(frame_inputs, text="Mês:", bg=COR_FUNDO, font=("Helvetica", 11, "bold")).grid(row=0, column=0, padx=5)
        cb_mes = ttk.Combobox(frame_inputs, values=[str(i).zfill(2) for i in range(1, 13)], width=5, font=("Helvetica", 11))
        cb_mes.set(str(mes_atual).zfill(2))
        cb_mes.grid(row=0, column=1, padx=5)

        tk.Label(frame_inputs, text="Ano:", bg=COR_FUNDO, font=("Helvetica", 11, "bold")).grid(row=0, column=2, padx=5)
        ent_ano = tk.Entry(frame_inputs, width=8, font=("Helvetica", 11))
        ent_ano.insert(0, str(ano_atual))
        ent_ano.grid(row=0, column=3, padx=5)

        def executar():
            try:
                mes = int(cb_mes.get())
                ano = int(ent_ano.get())
                from financeiro.calculos import obter_datas_periodo, calcular_horas_decimais, converter_decimais_para_horas, VALORES_POR_CARGO
                from financeiro.recibo_pdf import RelatorioMensalGeral
                from database.conexao import conectar
                import os

                data_i, data_f = obter_datas_periodo(mes, ano, "T")
                conn = conectar()
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT r.data, f.nome, r.hora_entrada, r.hora_saida, f.cargo
                    FROM registros_ponto r
                    JOIN funcionarios f ON r.id_funcionario = f.id
                    WHERE r.data BETWEEN ? AND ?
                    ORDER BY r.data ASC, f.nome ASC
                """, (data_i, data_f))
                
                registros_db = cursor.fetchall()
                if not registros_db:
                    conn.close()
                    messagebox.showwarning("Aviso", "Não há registros de ponto para este mês.")
                    return

                dados_tabela = []
                for data, nome, ent, sai, cargo in registros_db:
                    horas_fmt = "---"
                    valor_dia = 0.0
                    if ent and sai:
                        h_dec = calcular_horas_decimais(ent, sai)
                        horas_fmt = converter_decimais_para_horas(h_dec)
                        cargo_norm = cargo.strip().title()
                        v_hora = VALORES_POR_CARGO.get(cargo_norm, 7.50)
                        valor_dia = h_dec * v_hora
                    
                    dados_tabela.append({
                        'data': datetime.strptime(data, "%Y-%m-%d").strftime("%d/%m/%Y"),
                        'nome': nome,
                        'entrada': ent,
                        'saida': sai if sai else "Aberto",
                        'horas': horas_fmt,
                        'valor': f"{valor_dia:.2f}"
                    })

                relatorio = RelatorioMensalGeral(mes, ano)
                relatorio.gerar_tabela(dados_tabela)
                
                base_dir = os.path.dirname(os.path.abspath(__file__))
                pasta_relatorios = os.path.join(base_dir, "relatorios_mensais")
                if not os.path.exists(pasta_relatorios): os.makedirs(pasta_relatorios)
                
                nome_arquivo = os.path.join(pasta_relatorios, f"Relatorio_Mensal_Detalhado_{mes}_{ano}.pdf")
                relatorio.salvar(nome_arquivo)

                confirmar = messagebox.askyesno("Confirmar Limpeza", 
                    f"Relatório gerado com sucesso!\n\nArquivo: {os.path.basename(nome_arquivo)}\n\nDeseja LIMPAR os registros de ponto do mês {mes}/{ano} do sistema agora?")
                
                if confirmar:
                    cursor.execute("DELETE FROM registros_ponto WHERE data BETWEEN ? AND ?", (data_i, data_f))
                    conn.commit()
                    messagebox.showinfo("Sucesso", "Registros do mês limpos com sucesso.")

                conn.close()
                os.startfile(os.path.abspath(nome_arquivo))
                self.reconstruir_dashboard() 

            except Exception as e:
                messagebox.showerror("Erro", f"Falha no procedimento: {e}")

        tk.Button(frame_conteudo, text="GERAR RELATÓRIO E FECHAR MÊS", bg=COR_VERMELHO, fg=COR_BRANCO, font=("Helvetica", 11, "bold"), command=executar, height=2, width=35).pack(pady=40)

    def abrir_funcionarios(self):
        for widget in self.root.winfo_children(): widget.destroy()
        from funcionarios.func_view import TelaCadastroFuncionarios
        TelaCadastroFuncionarios(self.root, comando_voltar=self.reconstruir_dashboard)

    def abrir_ponto(self):
        for widget in self.root.winfo_children(): widget.destroy()
        from ponto.ponto_view import TelaRegistroPonto
        TelaRegistroPonto(self.root, comando_voltar=self.reconstruir_dashboard)

    def abrir_financeiro(self):
        for widget in self.root.winfo_children(): widget.destroy()
        from financeiro.relatorio_view import TelaFinanceiroRelatorio
        TelaFinanceiroRelatorio(self.root, nivel_acesso="Gerente", comando_voltar=self.reconstruir_dashboard)

    def abrir_usuarios(self):
        for widget in self.root.winfo_children(): widget.destroy()
        from auth.usuarios_view import TelaGerenciarRecepcionistas
        TelaGerenciarRecepcionistas(self.root, comando_voltar=self.reconstruir_dashboard)

    def abrir_ajudantes(self):
        for widget in self.root.winfo_children(): widget.destroy()
        from financeiro.ajudante_view import TelaAjudante
        TelaAjudante(self.root, comando_voltar=self.reconstruir_dashboard)

    def finalizar_sessao(self):
        realizar_backup()
        self.root.destroy()


# --- DASHBOARD DO RECEPCIONISTA COMUM ---
class DashboardComum:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.root.title(f"Cristal Hotel - Operação Diária")
        
        self.root.geometry("1100x750")
        self.root.configure(bg=COR_FUNDO)

        self.main_frame = tk.Frame(self.root, bg=COR_FUNDO)
        self.main_frame.pack(fill="both", expand=True)

        self.funcionarios_dict = {}
        self.carregar_funcionarios_memoria()

        self.criar_layout()
        self.atualizar_relogio()
        self.carregar_dados_dia()
        self.verificar_lembrete_fechamento()

    def verificar_lembrete_fechamento(self):
        from datetime import datetime
        import calendar
        hoje = datetime.now()
        ultimo_dia = calendar.monthrange(hoje.year, hoje.month)[1]
        faltam = ultimo_dia - hoje.day
        if faltam in [0, 1, 2]:
            dias_texto = {0: "HOJE é o último dia", 1: "Falta 1 dia", 2: "Faltam 2 dias"}
            msg = f"⚠️ LEMBRETE DE FECHAMENTO ⚠️\n\n{dias_texto[faltam]} para o fim do mês!\n\nPor favor, informe ao Gerente para realizar o Fechamento."
            messagebox.showwarning("Aviso", msg)

    def carregar_funcionarios_memoria(self):
        try:
            from database.conexao import conectar
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome, cargo FROM funcionarios")
            ordem_cargos = {"Gerente": 1, "Recepcionista Comum": 2, "Camareira": 3, "Cozinha": 4, "Folguista": 5}
            rows = cursor.fetchall()
            rows_sorted = sorted(rows, key=lambda x: (ordem_cargos.get(x[2] or "", 99), x[1] or ""))
            self.funcionarios_dict = {f"{nome} ({cargo})": id_f for id_f, nome, cargo in rows_sorted}
            conn.close()
        except Exception as e:
            print(f"Erro ao carregar dict de funcionários: {e}")

    def criar_layout(self):
        header = tk.Frame(self.main_frame, bg=COR_VERMELHO, height=120)
        header.pack(fill="x")
        tk.Frame(header, bg=COR_AMARELO, height=5).pack(fill="x", side="bottom")

        tk.Label(header, text="CRISTAL HOTEL", font=("Helvetica", 28, "bold"), bg=COR_VERMELHO, fg=COR_BRANCO).pack(pady=(15, 0))
        tk.Label(header, text="PAINEL DE OPERAÇÃO - RECEPÇÃO", font=("Helvetica", 10, "bold"), bg=COR_VERMELHO, fg=COR_AMARELO).pack(pady=(0, 15))

        sidebar = tk.Frame(self.main_frame, bg=COR_BRANCO, width=280)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="AÇÕES RÁPIDAS", font=("Helvetica", 11, "bold"), bg=COR_BRANCO, fg=COR_VERMELHO, pady=20).pack()

        tk.Button(sidebar, text="🕒 REGISTRAR ENTRADA", bg=COR_VERMELHO, fg=COR_BRANCO, font=("Helvetica", 10, "bold"), height=2, relief="flat", cursor="hand2", command=self.popup_entrada).pack(fill="x", padx=20, pady=10)
        tk.Button(sidebar, text="✅ FINALIZAR EXPEDIENTE\n(Marcar Saída)", bg=COR_AMARELO, fg=COR_VERMELHO, font=("Helvetica", 10, "bold"), height=2, relief="flat", cursor="hand2", command=self.marcar_saida_selecionado).pack(fill="x", padx=20, pady=10)
        tk.Button(sidebar, text="🔄 ATUALIZAR LISTA", bg=COR_FUNDO, fg=COR_VERMELHO, font=("Helvetica", 10, "bold"), height=2, relief="flat", cursor="hand2", command=self.carregar_dados_dia).pack(fill="x", padx=20, pady=20)
        tk.Button(sidebar, text="SAIR DO SISTEMA", bg="#CC0000", fg=COR_BRANCO, font=("Helvetica", 9, "bold"), relief="flat", cursor="hand2", command=self.finalizar_sessao).pack(side="bottom", fill="x", padx=20, pady=20)

        content_frame = tk.Frame(self.main_frame, bg=COR_FUNDO, padx=30, pady=10)
        content_frame.pack(side="right", fill="both", expand=True)

        frame_relogio = tk.Frame(content_frame, bg=COR_FUNDO)
        frame_relogio.pack(pady=(0, 20))
        self.lbl_relogio = tk.Label(frame_relogio, text="00:00:00", font=("Helvetica", 36, "bold"), bg=COR_FUNDO, fg=COR_VERMELHO)
        self.lbl_relogio.pack()
        self.lbl_data = tk.Label(frame_relogio, text="--/--/----", font=("Helvetica", 12, "bold"), bg=COR_FUNDO, fg=COR_VERMELHO)
        self.lbl_data.pack()

        tk.Label(content_frame, text="REGISTROS DE HOJE", font=("Helvetica", 14, "bold"), bg=COR_FUNDO, fg=COR_VERMELHO).pack(anchor="w", pady=(0, 5))
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background=COR_BRANCO, fieldbackground=COR_BRANCO, rowheight=35, font=("Helvetica", 10))
        style.configure("Treeview.Heading", font=("Helvetica", 11, "bold"), background=COR_VERMELHO, foreground=COR_BRANCO)

        self.tabela = ttk.Treeview(content_frame, columns=("id_reg", "nome", "entrada", "saida", "horas", "valor"), displaycolumns=("nome", "entrada", "saida", "horas", "valor"), show="headings")
        self.tabela.heading("nome", text="Funcionário")
        self.tabela.heading("entrada", text="Entrada")
        self.tabela.heading("saida", text="Saída")
        self.tabela.heading("horas", text="Horas")
        self.tabela.heading("valor", text="Valor (R$)")
        
        self.tabela.column("nome", width=250)
        self.tabela.column("entrada", width=100, anchor="center")
        self.tabela.column("saida", width=100, anchor="center")
        self.tabela.column("horas", width=100, anchor="center")
        self.tabela.column("valor", width=120, anchor="center")
        self.tabela.pack(fill="both", expand=True)

    def atualizar_relogio(self):
        try:
            from datetime import datetime 
            if not hasattr(self, 'lbl_relogio') or not self.lbl_relogio.winfo_exists(): return
            agora = datetime.now()
            self.lbl_relogio.config(text=agora.strftime("%H:%M:%S"))
            self.lbl_data.config(text=agora.strftime("%d/%m/%Y"))
            self.root.after(1000, self.atualizar_relogio)
        except Exception as e:
            pass

    def carregar_dados_dia(self):
        try:
            from financeiro.calculos import calcular_horas_decimais, converter_decimais_para_horas, VALORES_POR_CARGO
            from database.conexao import conectar
            from datetime import datetime

            for i in self.tabela.get_children(): self.tabela.delete(i)
            hoje = datetime.now().strftime("%Y-%m-%d")
            
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT r.id, f.nome, r.hora_entrada, r.hora_saida, f.cargo
                FROM registros_ponto r
                JOIN funcionarios f ON r.id_funcionario = f.id
                WHERE r.data = ?
                ORDER BY r.id DESC
            """, (hoje,))
            
            registros = cursor.fetchall()
            conn.close()

            for id_reg, nome, entrada, saida, cargo in registros:
                if entrada and saida:
                    horas_dec = calcular_horas_decimais(entrada, saida)
                    horas_fmt = converter_decimais_para_horas(horas_dec)
                    cargo_norm = cargo.strip().title() if cargo else ""
                    valor_hora = VALORES_POR_CARGO.get(cargo_norm, 0.0)
                    valor_dia = horas_dec * valor_hora
                    self.tabela.insert("", "end", values=(id_reg, nome, entrada, saida, horas_fmt, f"{valor_dia:.2f}"))
                else:
                    self.tabela.insert("", "end", values=(id_reg, nome, entrada, "Em aberto", "---", "---"))
        except Exception as e:
            pass

    def popup_entrada(self):
        if not self.funcionarios_dict:
            messagebox.showwarning("Aviso", "Nenhum funcionário cadastrado.")
            return

        popup = tk.Toplevel(self.root)
        popup.title("Registrar Chegada")
        popup.geometry("400x200")
        popup.configure(bg=COR_FUNDO)
        popup.grab_set() 
        
        tk.Label(popup, text="Quem está chegando agora?", font=("Helvetica", 12, "bold"), bg=COR_FUNDO, fg=COR_VERMELHO).pack(pady=20)
        cb = ttk.Combobox(popup, values=list(self.funcionarios_dict.keys()), state="readonly", width=40, font=("Helvetica", 11))
        cb.pack(pady=10)
        
        def confirmar():
            selecao = cb.get()
            if not selecao: return
            id_func = self.funcionarios_dict[selecao]
            
            from database.conexao import conectar
            from datetime import datetime
            agora = datetime.now()
            data_iso = agora.strftime("%Y-%m-%d")
            hora_iso = agora.strftime("%H:%M")
            
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM registros_ponto WHERE id_funcionario = ? AND data = ? AND hora_saida IS NULL", (id_func, data_iso))
            if cursor.fetchone():
                messagebox.showerror("Aviso", "Este funcionário já está com o ponto aberto hoje!", parent=popup)
            else:
                cursor.execute("INSERT INTO registros_ponto (id_funcionario, data, hora_entrada) VALUES (?, ?, ?)", (id_func, data_iso, hora_iso))
                conn.commit()
                popup.destroy()
                self.carregar_dados_dia() 
            conn.close()

        tk.Button(popup, text="SALVAR ENTRADA", bg=COR_VERMELHO, fg=COR_BRANCO, font=("Helvetica", 10, "bold"), relief="flat", cursor="hand2", command=confirmar).pack(pady=15)

    def marcar_saida_selecionado(self):
        selecionado = self.tabela.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um funcionário 'Em aberto' na tabela primeiro!")
            return
            
        valores = self.tabela.item(selecionado[0], "values")
        id_registro = valores[0]
        nome = valores[1]
        status_saida = valores[3]
        
        if status_saida != "Em aberto":
            messagebox.showinfo("Aviso", f"O expediente de {nome} já foi finalizado (Saída: {status_saida}).")
            return
            
        if messagebox.askyesno("Confirmar Saída", f"Deseja finalizar o expediente de {nome} agora?"):
            from database.conexao import conectar
            from datetime import datetime
            hora_iso = datetime.now().strftime("%H:%M")
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("UPDATE registros_ponto SET hora_saida = ? WHERE id = ?", (hora_iso, id_registro))
            conn.commit()
            conn.close()
            self.carregar_dados_dia() 

    def finalizar_sessao(self):
        self.root.destroy()