import tkinter as tk
from database.conexao import criar_tabelas
from auth.login_view import TelaLogin

def iniciar_sistema():
    # 1. Tenta inicializar o Banco de Dados e as Tabelas
    try:
        criar_tabelas()
    except Exception as e:
        # Se o banco falhar, o sistema nem abre para evitar erros maiores
        print(f"Erro ao inicializar o banco de dados: {e}")
        return

    # 2. Configura a janela principal (root) do Tkinter
    root = tk.Tk()
    root.title("Crystal Hotel - Sistema de Ponto")
    root.geometry("450x550")
    root.configure(bg="#002147") # Azul Marinho Crystal
    
    from auth.login_view import TelaLogin
    TelaLogin(root)

    # 4. Mantém o programa rodando
    root.mainloop()

if __name__ == "__main__":
    iniciar_sistema()