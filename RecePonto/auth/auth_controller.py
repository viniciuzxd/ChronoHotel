from database.conexao import conectar

def verificar_login(username, senha):
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT nivel_acesso FROM usuarios_sistema 
        WHERE username = ? AND senha = ?
    ''', (username, senha))
    
    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        return resultado[0] 
    else:
        return None 