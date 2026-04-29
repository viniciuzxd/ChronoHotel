import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from database.conexao import conectar

# --- IDENTIDADE VISUAL CRYSTAL HOTEL ---
COR_VERMELHO = "#B22222"
COR_AMARELO = "#FFD700"
COR_BRANCO = "#FFFFFF"
COR_FUNDO = "#FDF5E6"
COR_TEXTO = "#1A1A1A"

class TelaCadastroFuncionarios:
    def __init__(self, root, comando_voltar=None):
        self.root = root
        self.comando_voltar = comando_voltar
        self.root.title("Cristal Hotel - Gestão de Equipe")
        self.root.configure(bg=COR_FUNDO)
        
        # Header Moderno
        header = tk.Frame(self.root, bg=COR_VERMELHO, pady=15)
        header.pack(fill="x")
        
        tk.Frame(header, bg=COR_AMARELO, height=5).pack(fill="x", side="bottom")

        if self.comando_voltar:
            btn_voltar = tk.Button(header, text="⏪ VOLTAR", bg=COR_VERMELHO, fg=COR_AMARELO, 
                                   font=("Helvetica", 11, "bold"), relief="flat", cursor="hand2", 
                                   activebackground=COR_VERMELHO, activeforeground=COR_BRANCO,
                                   command=self.comando_voltar)
            btn_voltar.place(x=15, y=10)

        tk.Label(header, text="CRISTAL HOTEL", font=("Helvetica", 22, "bold"), bg=COR_VERMELHO, fg=COR_BRANCO).pack()
        tk.Label(header, text="GERENCIAMENTO DE COLABORADORES", font=("Helvetica", 9, "bold"), bg=COR_VERMELHO, fg=COR_AMARELO).pack()

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background=COR_FUNDO)
        style.configure("TNotebook.Tab", font=("Helvetica", 10, "bold"), padding=[20, 10], background=COR_BRANCO, foreground=COR_VERMELHO)
        style.map("TNotebook.Tab", background=[("selected", COR_VERMELHO)], foreground=[("selected", COR_BRANCO)])

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=30, pady=20)
        
        self.frame_cadastro = tk.Frame(self.notebook, bg=COR_BRANCO)
        self.frame_lista = tk.Frame(self.notebook, bg=COR_BRANCO)
        
        self.notebook.add(self.frame_cadastro, text=" ➕ NOVO CADASTRO ")
        self.notebook.add(self.frame_lista, text=" 📋 LISTA DE EQUIPE ")
        
        self.criar_interface_cadastro()
        self.criar_interface_lista()
        self.carregar_funcionarios()

    def criar_interface_cadastro(self):
        container = tk.Frame(self.frame_cadastro, bg=COR_BRANCO, pady=30)
        container.pack()

        # Inputs com estilo
        def criar_campo(label_text):
            tk.Label(container, text=label_text, bg=COR_BRANCO, fg=COR_VERMELHO, font=("Helvetica", 10, "bold")).pack(pady=(15, 0), anchor="w")
            ent = tk.Entry(container, font=("Helvetica", 12), width=45, relief="flat", highlightthickness=1)
            ent.config(highlightbackground=COR_AMARELO, highlightcolor=COR_VERMELHO)
            ent.pack(pady=5, ipady=5)
            return ent

        self.ent_nome = criar_campo("Nome Completo:")
        self.ent_cpf = criar_campo("CPF (Apenas números):")

        tk.Label(container, text="Cargo/Função:", bg=COR_BRANCO, fg=COR_VERMELHO, font=("Helvetica", 10, "bold")).pack(pady=(15, 0), anchor="w")
        self.cb_cargo = ttk.Combobox(container, values=["Gerente", "Recepcionista Comum", "Camareira", "Cozinha", "Folguista", "Manutenção", "Garçom", "Serviços Gerais"], font=("Helvetica", 11), width=43)
        self.cb_cargo.pack(pady=5, ipady=3)

        tk.Label(container, text="Valor da Hora (R$):", bg=COR_BRANCO, fg=COR_VERMELHO, font=("Helvetica", 10, "bold")).pack(pady=(15, 0), anchor="w")
        self.ent_valor_hora = tk.Entry(container, font=("Helvetica", 12), width=45, relief="flat", highlightthickness=1)
        self.ent_valor_hora.config(highlightbackground=COR_AMARELO, highlightcolor=COR_VERMELHO)
        self.ent_valor_hora.insert(0, "7.50")
        self.ent_valor_hora.pack(pady=5, ipady=5)

        # Botão Salvar
        tk.Button(container, text="SALVAR COLABORADOR", bg=COR_VERMELHO, fg=COR_BRANCO, 
                  font=("Helvetica", 11, "bold"), width=35, height=2, relief="flat", cursor="hand2",
                  command=self.salvar).pack(pady=40)

    def criar_interface_lista(self):
        # Tabela Profissional
        style = ttk.Style()
        style.configure("Treeview", background=COR_BRANCO, fieldbackground=COR_BRANCO, rowheight=30, font=("Helvetica", 10))
        style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"), background=COR_VERMELHO, foreground=COR_BRANCO)

        self.tabela = ttk.Treeview(self.frame_lista, columns=("id", "nome", "cpf", "cargo", "valor_hora"), show="headings")
        self.tabela.heading("id", text="ID")
        self.tabela.heading("nome", text="Nome Completo")
        self.tabela.heading("cpf", text="CPF")
        self.tabela.heading("cargo", text="Cargo/Função")
        self.tabela.heading("valor_hora", text="Valor Hora (R$)")
        
        self.tabela.column("id", width=60, anchor="center")
        self.tabela.column("nome", width=250)
        self.tabela.column("cpf", width=120, anchor="center")
        self.tabela.column("cargo", width=150, anchor="center")
        self.tabela.column("valor_hora", width=100, anchor="center")
        
        self.tabela.pack(fill="both", expand=True, padx=20, pady=20)
        
        btn_frame = tk.Frame(self.frame_lista, bg=COR_BRANCO)
        btn_frame.pack(pady=(0, 20))
        
        # Botão Excluir
        tk.Button(btn_frame, text="🗑️ EXCLUIR SELECIONADO", bg="#CC0000", fg=COR_BRANCO, 
                  font=("Helvetica", 9, "bold"), width=25, height=2, relief="flat", cursor="hand2",
                  command=self.excluir).pack(side="left", padx=10)
        
        # Botão Atualizar
        tk.Button(btn_frame, text="🔄 ATUALIZAR LISTA", bg=COR_VERMELHO, fg=COR_BRANCO, 
                  font=("Helvetica", 9, "bold"), width=25, height=2, relief="flat", cursor="hand2",
                  command=self.carregar_funcionarios).pack(side="left", padx=10)


    def carregar_funcionarios(self):
        for i in self.tabela.get_children(): self.tabela.delete(i)
        conn = conectar()
        cursor = conn.cursor()
        
        # Ordem hierárquica solicitada
        ordem_cargos = {
            "Gerente": 1,
            "Recepcionista Comum": 2,
            "Camareira": 3,
            "Cozinha": 4,
            "Folguista": 5
        }
        
        cursor.execute("SELECT id, nome, cpf, cargo, valor_hora FROM funcionarios")
        rows = cursor.fetchall()
        
        # Ordenar: primeiro pelo cargo (hierarquia), depois por nome
        rows_sorted = sorted(rows, key=lambda x: (ordem_cargos.get(x[3], 99), x[1]))
        
        for row in rows_sorted:
            self.tabela.insert("", "end", values=row)
        conn.close()

    def salvar(self):
        nome = self.ent_nome.get()
        cpf = self.ent_cpf.get()
        cargo = self.cb_cargo.get()
        valor_hora = self.ent_valor_hora.get()

        if not nome or not cpf or not cargo or not valor_hora:
            messagebox.showwarning("Atenção", "Por favor, preencha todos os campos!")
            return

        try:
            v_hora = float(valor_hora.replace(",", "."))
        except ValueError:
            messagebox.showerror("Erro", "Valor da hora deve ser um número!")
            return

        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO funcionarios (nome, cpf, cargo, valor_hora) VALUES (?, ?, ?, ?)",
                           (nome, cpf, cargo, v_hora))
            conn.commit()
            messagebox.showinfo("Sucesso", f"Funcionário {nome} cadastrado com sucesso!")
            self.ent_nome.delete(0, tk.END)
            self.ent_cpf.delete(0, tk.END)
            self.cb_cargo.set("")
            self.ent_valor_hora.delete(0, tk.END)
            self.ent_valor_hora.insert(0, "7.50")
            self.carregar_funcionarios()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar funcionário: {e}")
        finally:
            conn.close()

    def excluir(self):
        selecionado = self.tabela.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um funcionário para excluir!")
            return
        
        f_id = self.tabela.item(selecionado[0], "values")[0]
        nome = self.tabela.item(selecionado[0], "values")[1]
        
        if messagebox.askyesno("Confirmar", f"Deseja realmente excluir {nome}?\nOs IDs serão reorganizados."):
            conn = conectar()
            cursor = conn.cursor()
            try:
                # 1. Deletar o funcionário
                cursor.execute("DELETE FROM funcionarios WHERE id = ?", (f_id,))
                
                # 2. Reorganizar IDs
                # Criar tabela temporária
                cursor.execute("CREATE TABLE funcionarios_backup AS SELECT nome, cargo, cpf, valor_hora FROM funcionarios ORDER BY id")
                cursor.execute("DROP TABLE funcionarios")
                cursor.execute('''CREATE TABLE funcionarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT,
                    cargo TEXT,
                    cpf TEXT UNIQUE,
                    valor_hora REAL DEFAULT 7.50
                )''')
                cursor.execute("INSERT INTO funcionarios (nome, cargo, cpf, valor_hora) SELECT nome, cargo, cpf, valor_hora FROM funcionarios_backup")
                cursor.execute("DROP TABLE funcionarios_backup")
                
                conn.commit()
                messagebox.showinfo("Sucesso", "Funcionário removido e IDs reorganizados!")
                self.carregar_funcionarios()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir/reorganizar: {e}")
            finally:
                conn.close()