import sqlite3
import os

def conectar():
    # Define o caminho do banco de dados relativo ao diretório pai (RecePonto)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "dados_hotel.db")
    return sqlite3.connect(db_path)

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()
    
    # Tabela de Usuários do Sistema (Recepcionistas)
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios_sistema (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        senha TEXT,
        nivel_acesso TEXT
    )''')

    # Tabela de Funcionários do Hotel
    cursor.execute('''CREATE TABLE IF NOT EXISTS funcionarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        cargo TEXT,
        cpf TEXT UNIQUE,
        valor_hora REAL DEFAULT 7.50
    )''')

    # Tabela de Ajudantes (Página Ajudante)
    cursor.execute('''CREATE TABLE IF NOT EXISTS ajudantes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        data TEXT,
        entrada TEXT,
        saida TEXT,
        valor_diaria REAL
    )''')

    # Tabela de Ponto
    cursor.execute('''CREATE TABLE IF NOT EXISTS registros_ponto (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_funcionario INTEGER,
        data TEXT,
        hora_entrada TEXT,
        hora_saida TEXT,
        FOREIGN KEY(id_funcionario) REFERENCES funcionarios(id)
    )''')

    # Criar Admin Supremo padrão se não existir
    cursor.execute("SELECT * FROM usuarios_sistema WHERE username = 'admin'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO usuarios_sistema (username, senha, nivel_acesso) VALUES (?, ?, ?)",
                       ('admin', '1234', 'Gerente'))
    
    conn.commit()
    conn.close()
    print("Banco de dados pronto e tabelas verificadas.")