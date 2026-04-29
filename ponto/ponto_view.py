import tkinter as tk
from tkinter import ttk, messagebox
from database.conexao import conectar
from datetime import datetime

# --- IDENTIDADE VISUAL CRYSTAL HOTEL ---
COR_VERMELHO = "#B22222"
COR_AMARELO = "#FFD700"
COR_BRANCO = "#FFFFFF"
COR_FUNDO = "#FDF5E6"
COR_TEXTO = "#1A1A1A"

class TelaRegistroPonto:
    # Recebemos o comando_voltar aqui!
    def __init__(self, root, comando_voltar=None):
        self.root = root
        self.comando_voltar = comando_voltar # Salva a função de voltar
        
        self.root.title("Crystal Hotel - Registro de Ponto")
        self.root.configure(bg=COR_FUNDO)
        
        self.funcionarios_dict = {}
        
        self.criar_widgets()
        self.atualizar_relogio()
        self.carregar_funcionarios()
        self.carregar_historico()

    def criar_widgets(self):
        header = tk.Frame(self.root, bg=COR_VERMELHO, pady=15)
        header.pack(fill="x")

        tk.Frame(header, bg=COR_AMARELO, height=3).pack(fill="x", side="bottom")

        # --- BOTÃO DE VOLTAR NO CANTO SUPERIOR ESQUERDO ---
        if self.comando_voltar:
            btn_voltar = tk.Button(header, text="⏪ VOLTAR", bg=COR_VERMELHO, fg=COR_AMARELO, 
                                   font=("Helvetica", 11, "bold"), relief="flat", cursor="hand2", 
                                   activebackground=COR_VERMELHO, activeforeground=COR_BRANCO,
                                   command=self.comando_voltar)
            # O .place(x, y) fixa o botão exatamente no canto, sem bagunçar os textos centralizados
            btn_voltar.place(x=15, y=10) 

        tk.Label(header, text="CRYSTAL HOTEL", font=("Helvetica", 24, "bold"), bg=COR_VERMELHO, fg=COR_BRANCO).pack()
        tk.Label(header, text="REGISTRO DE PONTO OFICIAL", font=("Helvetica", 9, "bold"), bg=COR_VERMELHO, fg=COR_AMARELO).pack()
        
        frame_relogio = tk.Frame(self.root, bg=COR_FUNDO, pady=20)
        frame_relogio.pack(fill="x")

        self.lbl_relogio = tk.Label(frame_relogio, text="00:00:00", font=("Helvetica", 42, "bold"), bg=COR_FUNDO, fg=COR_VERMELHO)
        self.lbl_relogio.pack()
        
        self.lbl_data = tk.Label(frame_relogio, text="--/--/----", font=("Helvetica", 14, "bold"), bg=COR_FUNDO, fg=COR_VERMELHO)
        self.lbl_data.pack()

        frame_central = tk.Frame(self.root, bg=COR_FUNDO, pady=10)
        frame_central.pack(fill="x", padx=50)

        tk.Label(frame_central, text="Selecione o Funcionário:", font=("Helvetica", 11, "bold"), bg=COR_FUNDO, fg=COR_VERMELHO).pack(pady=5)
        
        self.cb_func = ttk.Combobox(frame_central, state="readonly", width=60, font=("Helvetica", 12))
        self.cb_func.pack(pady=5)

        btn_frame = tk.Frame(frame_central, bg=COR_FUNDO)
        btn_frame.pack(pady=20)

        self.btn_entrada = tk.Button(btn_frame, text="CONFIRMAR\nENTRADA", bg=COR_VERMELHO, fg=COR_BRANCO, font=("Helvetica", 11, "bold"), width=20, height=3, relief="flat", cursor="hand2", command=lambda: self.processar_registro("entrada"))
        self.btn_entrada.grid(row=0, column=0, padx=15)

        self.btn_saida = tk.Button(btn_frame, text="CONFIRMAR\nSAÍDA", bg=COR_AMARELO, fg=COR_VERMELHO, font=("Helvetica", 11, "bold"), width=20, height=3, relief="flat", cursor="hand2", command=lambda: self.processar_registro("saida"))
        self.btn_saida.grid(row=0, column=1, padx=15)

        frame_historico = tk.Frame(self.root, bg=COR_FUNDO)
        frame_historico.pack(fill="both", expand=True, padx=40, pady=(0, 20))

        tk.Label(frame_historico, text="HISTÓRICO RECENTE", font=("Helvetica", 11, "bold"), bg=COR_FUNDO, fg=COR_VERMELHO).pack(anchor="w", pady=(0, 10))

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background=COR_BRANCO, fieldbackground=COR_BRANCO, rowheight=30, font=("Helvetica", 10))
        style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"), background=COR_VERMELHO, foreground=COR_BRANCO)

        self.tabela = ttk.Treeview(frame_historico, columns=("data", "nome", "entrada", "saida", "valor"), show="headings")
        self.tabela.heading("data", text="Data")
        self.tabela.heading("nome", text="Funcionário (Cargo)")
        self.tabela.heading("entrada", text="Entrada")
        self.tabela.heading("saida", text="Saída")
        self.tabela.heading("valor", text="Ganhos (R$)")
        
        self.tabela.column("data", width=100, anchor="center")
        self.tabela.column("nome", width=250)
        self.tabela.column("entrada", width=100, anchor="center")
        self.tabela.column("saida", width=100, anchor="center")
        self.tabela.column("valor", width=100, anchor="center")
        
        self.tabela.pack(fill="both", expand=True)

    def atualizar_relogio(self):
        try:
            if not hasattr(self, 'lbl_relogio') or not self.lbl_relogio.winfo_exists():
                return
            
            agora = datetime.now()
            self.lbl_relogio.config(text=agora.strftime("%H:%M:%S"))
            self.lbl_data.config(text=agora.strftime("%d/%m/%Y"))
            self.root.after(1000, self.atualizar_relogio)
        except Exception as e:
            pass # Ignora erros de destruição de janela

    def carregar_funcionarios(self):
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome, cargo FROM funcionarios")
            rows = cursor.fetchall()
            
            ordem_cargos = {"Gerente": 1, "Recepcionista Comum": 2, "Camareira": 3, "Cozinha": 4, "Folguista": 5}
            rows_sorted = sorted(rows, key=lambda x: (ordem_cargos.get(x[2] or "", 99), x[1] or ""))
            
            self.funcionarios_dict = {f"{nome} ({cargo})": id_f for id_f, nome, cargo in rows_sorted}
            self.cb_func['values'] = list(self.funcionarios_dict.keys())
            conn.close()
        except Exception as e:
            messagebox.showerror("Aviso", f"Não foi possível carregar a lista de funcionários.\nDetalhe: {e}")

    def carregar_historico(self):
        try:
            from financeiro.calculos import calcular_horas_decimais, VALORES_POR_CARGO
            
            for i in self.tabela.get_children(): self.tabela.delete(i)
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT r.data, f.nome, f.cargo, r.hora_entrada, r.hora_saida 
                FROM registros_ponto r
                JOIN funcionarios f ON r.id_funcionario = f.id
                ORDER BY r.data DESC, r.id DESC LIMIT 50
            ''')
            
            for data, nome, cargo, entrada, saida in cursor.fetchall():
                valor_dia = "---"
                if entrada and saida:
                    horas = calcular_horas_decimais(entrada, saida)
                    cargo_nome = cargo if cargo else ""
                    valor_hora = VALORES_POR_CARGO.get(cargo_nome, 0.0)
                    valor_dia = f"R$ {horas * valor_hora:.2f}"
                
                try: data_br = datetime.strptime(data, "%Y-%m-%d").strftime("%d/%m/%Y")
                except ValueError: data_br = data
                    
                self.tabela.insert("", "end", values=(data_br, f"{nome} ({cargo})", entrada, saida or "Aberto", valor_dia))
            conn.close()
        except Exception as e:
            pass

    def processar_registro(self, tipo):
        id_display = self.cb_func.get()
        if not id_display:
            messagebox.showwarning("Atenção", "Por favor, selecione um funcionário na lista!")
            return

        id_func = self.funcionarios_dict[id_display]
        agora = datetime.now()
        data_iso = agora.strftime("%Y-%m-%d")
        hora_iso = agora.strftime("%H:%M")

        conn = conectar()
        cursor = conn.cursor()

        try:
            if tipo == "entrada":
                cursor.execute("SELECT id FROM registros_ponto WHERE id_funcionario = ? AND data = ? AND hora_saida IS NULL", (id_func, data_iso))
                if cursor.fetchone():
                    messagebox.showerror("Erro", f"{id_display} já possui uma entrada em aberto hoje!")
                else:
                    cursor.execute("INSERT INTO registros_ponto (id_funcionario, data, hora_entrada) VALUES (?, ?, ?)", (id_func, data_iso, hora_iso))
                    messagebox.showinfo("Sucesso", f"Entrada de {id_display} registrada às {hora_iso}")
            elif tipo == "saida":
                cursor.execute("SELECT id FROM registros_ponto WHERE id_funcionario = ? AND hora_saida IS NULL ORDER BY id DESC LIMIT 1", (id_func,))
                registro = cursor.fetchone()
                
                if registro:
                    cursor.execute("UPDATE registros_ponto SET hora_saida = ? WHERE id = ?", (hora_iso, registro[0]))
                    messagebox.showinfo("Sucesso", f"Saída de {id_display} registrada às {hora_iso}")
                else:
                    messagebox.showerror("Erro", f"Não foi encontrada uma entrada aberta para {id_display}")

            conn.commit()
            self.carregar_historico()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao registrar ponto: {e}")
        finally:
            conn.close()