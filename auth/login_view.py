import tkinter as tk
from tkinter import messagebox
from auth.auth_controller import verificar_login
from dashboard import DashboardGerente, DashboardComum

# --- IDENTIDADE VISUAL CRISTAL HOTEL ---
COR_VERMELHO = "#B22222"
COR_AMARELO = "#FFD700"
COR_BRANCO = "#FFFFFF"
COR_FUNDO = "#FDF5E6"
COR_TEXTO = "#1A1A1A"

class TelaLogin:
    def __init__(self, root):
        self.root = root
        self.root.title("Cristal Hotel - Acesso")
        
        # Define tamanho e centraliza
        largura, altura = 450, 550
        largura_tela = self.root.winfo_screenwidth()
        altura_tela = self.root.winfo_screenheight()
        pos_x = (largura_tela // 2) - (largura // 2)
        pos_y = (altura_tela // 2) - (altura // 2)
        
        self.root.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")
        self.root.configure(bg=COR_FUNDO)
        self.root.resizable(False, False)
        
        self.criar_widgets()

    def criar_widgets(self):
        header = tk.Frame(self.root, bg=COR_VERMELHO, height=180)
        header.pack(fill="x")
        
        tk.Frame(header, bg=COR_AMARELO, height=5).pack(fill="x", side="bottom")
        
        tk.Label(header, text="CRISTAL HOTEL", font=("Helvetica", 28, "bold"), 
                 bg=COR_VERMELHO, fg=COR_BRANCO).pack(pady=(50, 5))
        tk.Label(header, text="GESTÃO DE PONTO PROFISSIONAL", font=("Helvetica", 9, "bold"), 
                 bg=COR_VERMELHO, fg=COR_AMARELO).pack()

        login_frame = tk.Frame(self.root, bg=COR_FUNDO, pady=40)
        login_frame.pack(fill="both", expand=True, padx=50)

        tk.Label(login_frame, text="USUÁRIO", font=("Helvetica", 9, "bold"), 
                 bg=COR_FUNDO, fg=COR_VERMELHO).pack(anchor="w")
        self.ent_user = tk.Entry(login_frame, font=("Helvetica", 12), relief="flat", highlightthickness=1)
        self.ent_user.config(highlightbackground=COR_AMARELO, highlightcolor=COR_VERMELHO)
        self.ent_user.pack(fill="x", pady=(5, 20), ipady=8)

        tk.Label(login_frame, text="SENHA", font=("Helvetica", 9, "bold"), 
                 bg=COR_FUNDO, fg=COR_VERMELHO).pack(anchor="w")
        self.ent_pass = tk.Entry(login_frame, font=("Helvetica", 12), show="*", relief="flat", highlightthickness=1)
        self.ent_pass.config(highlightbackground=COR_AMARELO, highlightcolor=COR_VERMELHO)
        self.ent_pass.pack(fill="x", pady=(5, 30), ipady=8)

        # Botão de Entrar Estilizado
        btn_login = tk.Button(login_frame, text="ACESSAR SISTEMA", bg=COR_VERMELHO, fg=COR_BRANCO, 
                              font=("Helvetica", 11, "bold"), relief="flat", height=2,
                              cursor="hand2", command=self.fazer_login)
        btn_login.pack(fill="x")

        tk.Label(self.root, text="© 2026 Crystal Hotel - Soluções em Gestão", 
                 font=("Helvetica", 7), bg=COR_FUNDO, fg="#888").pack(side="bottom", pady=15)

    def fazer_login(self):
        usuario = self.ent_user.get()
        senha = self.ent_pass.get()
        
        if not usuario or not senha:
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return

        nivel = verificar_login(usuario, senha)

        if nivel:
            self.abrir_dashboard(nivel)
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos!")

    def abrir_dashboard(self, nivel_acesso):
        usuario_logado = self.ent_user.get()
        
        for widget in self.root.winfo_children():
            widget.destroy()
        
        try:
            print(f"DEBUG: Transicionando para Dashboard ({nivel_acesso})")
            if nivel_acesso == "Gerente":
                self.root.app = DashboardGerente(self.root, usuario_logado)
            else:
                self.root.app = DashboardComum(self.root, usuario_logado)
        except Exception as e:
            print(f"ERRO CRÍTICO NA TRANSIÇÃO: {e}")
            messagebox.showerror("Erro de Sistema", f"Não foi possível carregar o painel: {e}")