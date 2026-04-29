import tkinter as tk
from tkinter import messagebox, ttk
from database.conexao import conectar

# --- IDENTIDADE VISUAL CRYSTAL HOTEL ---
COR_VERMELHO = "#B22222"
COR_AMARELO = "#FFD700"
COR_BRANCO = "#FFFFFF"
COR_FUNDO = "#FDF5E6"
COR_TEXTO = "#1A1A1A"

class TelaGerenciarRecepcionistas:
    def __init__(self, root, comando_voltar=None):
        self.root = root
        self.comando_voltar = comando_voltar
        self.root.title("Cristal Hotel - Controle de Acessos")
        self.root.configure(bg=COR_FUNDO)
        
        # Header
        header = tk.Frame(self.root, bg=COR_VERMELHO, pady=15)
        header.pack(fill="x")
        tk.Frame(header, bg=COR_AMARELO, height=3).pack(fill="x", side="bottom")

        if self.comando_voltar:
            btn_voltar = tk.Button(header, text="⏪ VOLTAR", bg=COR_VERMELHO, fg=COR_AMARELO, 
                                   font=("Helvetica", 11, "bold"), relief="flat", cursor="hand2", 
                                   activebackground=COR_VERMELHO, activeforeground=COR_BRANCO,
                                   command=self.comando_voltar)
            btn_voltar.place(x=15, y=10)

        tk.Label(header, text="CRISTAL HOTEL", font=("Helvetica", 20, "bold"), bg=COR_VERMELHO, fg=COR_BRANCO).pack()
        tk.Label(header, text="GERENCIAMENTO DE ACESSOS", font=("Helvetica", 9, "bold"), bg=COR_VERMELHO, fg=COR_AMARELO).pack()

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background=COR_FUNDO, borderwidth=0)
        style.configure("TNotebook.Tab", font=("Helvetica", 10, "bold"), padding=[20, 10], background=COR_BRANCO, foreground=COR_VERMELHO)
        style.map("TNotebook.Tab", background=[("selected", COR_VERMELHO)], foreground=[("selected", COR_BRANCO)])

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=30, pady=30)
        
        self.frame_cadastro = tk.Frame(self.notebook, bg=COR_BRANCO)
        self.frame_lista = tk.Frame(self.notebook, bg=COR_BRANCO)
        
        self.notebook.add(self.frame_cadastro, text=" NOVO ACESSO ")
        self.notebook.add(self.frame_lista, text=" LISTA DE USUÁRIOS ")
        
        self.criar_widgets_cadastro()
        self.criar_widgets_lista()
        self.carregar_usuarios()

    def criar_widgets_cadastro(self):
        container = tk.Frame(self.frame_cadastro, bg=COR_BRANCO, pady=30)
        container.pack()

        tk.Label(container, text="Usuário (Login):", bg=COR_BRANCO, fg=COR_VERMELHO, font=("Helvetica", 10, "bold")).pack(pady=(10, 0))
        self.ent_user = tk.Entry(container, font=("Helvetica", 11), width=35, bg=COR_FUNDO, relief="flat")
        self.ent_user.pack(pady=8, ipady=5)

        tk.Label(container, text="Senha:", bg=COR_BRANCO, fg=COR_VERMELHO, font=("Helvetica", 10, "bold")).pack(pady=(10, 0))
        self.ent_pass = tk.Entry(container, font=("Helvetica", 11), width=35, show="*", bg=COR_FUNDO, relief="flat")
        self.ent_pass.pack(pady=8, ipady=5)

        tk.Label(container, text="Nível de Acesso:", bg=COR_BRANCO, fg=COR_VERMELHO, font=("Helvetica", 10, "bold")).pack(pady=(10, 0))
        self.cb_nivel = ttk.Combobox(container, values=["Comum", "Gerente"], font=("Helvetica", 11), width=33)
        self.cb_nivel.set("Comum")
        self.cb_nivel.pack(pady=8)

        # Botão Salvar
        tk.Button(container, text="CADASTRAR ACESSO", bg=COR_VERMELHO, fg=COR_BRANCO, 
                  font=("Helvetica", 10, "bold"), width=30, height=2, relief="flat", cursor="hand2",
                  command=self.salvar_usuario).pack(pady=30)

    def criar_widgets_lista(self):
        # Estilo da Tabela
        style = ttk.Style()
        style.configure("Treeview", background=COR_BRANCO, fieldbackground=COR_BRANCO, 
                        rowheight=35, font=("Helvetica", 10))
        style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"), 
                        background=COR_VERMELHO, foreground=COR_BRANCO)
        
        self.tabela = ttk.Treeview(self.frame_lista, columns=("id", "user", "nivel"), show="headings")
        self.tabela.heading("id", text="ID")
        self.tabela.heading("user", text="Usuário")
        self.tabela.heading("nivel", text="Nível de Acesso")
        
        self.tabela.column("id", width=60, anchor="center")
        self.tabela.column("user", width=250)
        self.tabela.column("nivel", width=180, anchor="center")
        
        self.tabela.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Botão Remover
        tk.Button(self.frame_lista, text="🗑️ REMOVER ACESSO SELECIONADO", bg="#CC0000", fg=COR_BRANCO, 
                  font=("Helvetica", 9, "bold"), width=35, height=2, relief="flat", cursor="hand2",
                  command=self.excluir).pack(pady=(0, 20))

    def carregar_usuarios(self):
        for i in self.tabela.get_children(): self.tabela.delete(i)
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, nivel_acesso FROM usuarios_sistema")
        for row in cursor.fetchall():
            self.tabela.insert("", "end", values=row)
        conn.close()

    def salvar_usuario(self):
        user = self.ent_user.get()
        senha = self.ent_pass.get()
        nivel = self.cb_nivel.get()

        if not user or not senha:
            messagebox.showwarning("Erro", "Preencha todos os campos!")
            return

        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO usuarios_sistema (username, senha, nivel_acesso) VALUES (?, ?, ?)",
                           (user, senha, nivel))
            conn.commit()
            messagebox.showinfo("Sucesso", f"Usuário {user} criado como {nivel}!")
            self.ent_user.delete(0, tk.END)
            self.ent_pass.delete(0, tk.END)
            self.carregar_usuarios()
        except:
            messagebox.showerror("Erro", "Usuário já existe!")
        finally:
            conn.close()

    def excluir(self):
        selecionado = self.tabela.selection()
        if not selecionado: return
        
        u_id = self.tabela.item(selecionado[0], "values")[0]
        user = self.tabela.item(selecionado[0], "values")[1]
        
        if user == "admin":
            messagebox.showerror("Erro", "O administrador principal não pode ser removido!")
            return

        if messagebox.askyesno("Confirmar", f"Remover acesso de {user}?"):
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM usuarios_sistema WHERE id = ?", (u_id,))
            conn.commit()
            conn.close()
            self.carregar_usuarios()