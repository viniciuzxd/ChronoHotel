import sqlite3
import random
from datetime import datetime, timedelta

def popular_financeiro():
    import os
    db_path = 'dados_hotel.db'
    if not os.path.exists(db_path):
        print(f"Erro: Banco de dados não encontrado em {db_path}")
        return
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Pega todos os funcionários
    cursor.execute("SELECT id, nome, cargo FROM funcionarios")
    funcionarios = cursor.fetchall()

    # Datas para a primeira e segunda quinzena de Abril 2024
    dias_abril = list(range(1, 28)) # Até dia 27 para testes

    print("Populando registros de ponto fictícios...")
    
    for f_id, nome, cargo in funcionarios:
        for dia in dias_abril:
            # Pula alguns dias aleatoriamente (folgas)
            if random.random() > 0.8:
                continue
                
            data = f"2024-04-{str(dia).zfill(2)}"
            
            # Horários aleatórios
            # Entrada entre 07:00 e 09:00
            h_ent = random.randint(7, 9)
            m_ent = random.randint(0, 59)
            entrada = f"{str(h_ent).zfill(2)}:{str(m_ent).zfill(2)}"
            
            # Saída entre 16:00 e 18:00
            h_sai = random.randint(16, 18)
            m_sai = random.randint(0, 59)
            saida = f"{str(h_sai).zfill(2)}:{str(m_sai).zfill(2)}"
            
            cursor.execute("""
                INSERT INTO registros_ponto (id_funcionario, data, hora_entrada, hora_saida)
                VALUES (?, ?, ?, ?)
            """, (f_id, data, entrada, saida))

    conn.commit()
    conn.close()
    print("Sucesso! Banco de dados populado para testes financeiros.")

if __name__ == "__main__":
    popular_financeiro()
