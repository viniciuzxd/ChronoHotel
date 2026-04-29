import sqlite3
import os
import random
from datetime import datetime, timedelta

def conectar():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "dados_hotel.db")
    return sqlite3.connect(db_path)

def popular_dados():
    conn = conectar()
    cursor = conn.cursor()
    
    # Garantir que a coluna valor_hora existe (caso o banco seja antigo)
    try:
        cursor.execute("ALTER TABLE funcionarios ADD COLUMN valor_hora REAL DEFAULT 7.50")
    except sqlite3.OperationalError:
        pass # Coluna já existe

    # 2. Adicionar Funcionários
    funcionarios = [
        ("Maria Oliveira", "Camareira", "11122233344", 7.50),
        ("Joana Santos", "Camareira", "22233344455", 7.50),
        ("Carlos Ferreira", "Cozinha", "33344455566", 7.50),
        ("Ana Beatriz", "Cozinha", "44455566677", 7.50),
        ("Roberto Silva", "Folguista", "55566677788", 7.50)
    ]
    
    for nome, cargo, cpf, v_hora in funcionarios:
        try:
            cursor.execute("INSERT INTO funcionarios (nome, cargo, cpf, valor_hora) VALUES (?, ?, ?, ?)",
                           (nome, cargo, cpf, v_hora))
        except sqlite3.IntegrityError:
            # Já existe, atualizar valor_hora
            cursor.execute("UPDATE funcionarios SET valor_hora = ? WHERE cpf = ?", (v_hora, cpf))
            
    # Pegar os IDs dos novos funcionários
    cursor.execute("SELECT id, nome, cargo FROM funcionarios WHERE cargo IN ('Camareira', 'Cozinha', 'Folguista')")
    funcs_db = cursor.fetchall()
    
    # 3. Gerar Pontos para o último mês
    hoje = datetime.now()
    data_inicio = hoje - timedelta(days=30)
    
    for i in range(31):
        data_atual = data_inicio + timedelta(days=i)
        if data_atual > hoje: break
        
        data_iso = data_atual.strftime("%Y-%m-%d")
        dia_semana = data_atual.weekday() # 6 é domingo
        
        for f_id, nome, cargo in funcs_db:
            if cargo == "Folguista":
                # Roberto (Folguista) trabalhou o último domingo 24h
                # Vamos verificar se data_atual é o domingo mais recente
                is_last_sunday = (dia_semana == 6 and (hoje - data_atual).days < 7)
                if is_last_sunday:
                    # Domingo 24h: Entrada 08:00 Saída 08:00 (o calculos.py trata t2 < t1 como dia seguinte)
                    cursor.execute("INSERT INTO registros_ponto (id_funcionario, data, hora_entrada, hora_saida) VALUES (?, ?, ?, ?)",
                                   (f_id, data_iso, "08:00", "08:00"))
                continue
            
            # Outros (70% de chance de trabalhar)
            if random.random() < 0.7:
                horas = random.randint(4, 8)
                minutos = random.choice([0, 15, 30, 45])
                hora_entrada = random.randint(7, 10)
                h_e_str = f"{hora_entrada:02d}:00"
                h_s = hora_entrada + horas
                h_s_str = f"{h_s:02d}:{minutos:02d}"
                
                cursor.execute("INSERT INTO registros_ponto (id_funcionario, data, hora_entrada, hora_saida) VALUES (?, ?, ?, ?)",
                               (f_id, data_iso, h_e_str, h_s_str))

    conn.commit()
    conn.close()
    print("Dados populados com sucesso!")

if __name__ == "__main__":
    popular_dados()
