from database.conexao import conectar

def verificar_login(username, senha):
    """
    Verifica as credenciais no banco de dados.
    Retorna o nível de acesso ('Gerente' ou 'Comum') se der certo, ou None se falhar.
    """
    conn = conectar()
    cursor = conn.cursor()
    
    # Busca o usuário e a senha exatos no banco
    cursor.execute('''
        SELECT nivel_acesso FROM usuarios_sistema 
        WHERE username = ? AND senha = ?
    ''', (username, senha))
    
    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        return resultado[0] # Retorna a string ('Gerente' ou 'Comum')
    else:
        return None # Credenciais incorretas