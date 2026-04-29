import sqlite3
import os
import random
from datetime import datetime, timedelta

def repopulate():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "dados_hotel.db")
    
    if not os.path.exists(db_path):
        print("Erro: Banco de dados não encontrado.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 1. Limpa registros antigos
    print("Limpando registros de ponto...")
    cursor.execute("DELETE FROM registros_ponto")
    
    # 2. Busca funcionários
    cursor.execute("SELECT id, nome FROM funcionarios")
    funcionarios = cursor.fetchall()
    
    if not funcionarios:
        print("Erro: Nenhum funcionário encontrado para popular.")
        conn.close()
        return

    # 3. Popula com dados de Abril de 2026 (Período atual no sistema)
    # E alguns de Março para teste
    meses = [(4, 2026), (3, 2026)]
    
    registros_count = 0
    for mes, ano in meses:
        # Dias 1 a 30 (simplificado)
        for dia in range(1, 29): # Até dia 28 para evitar erros de calendário
            data_str = f"{ano}-{mes:02d}-{dia:02d}"
            
            for f_id, nome in funcionarios:
                # Nem todo mundo trabalha todo dia
                if random.random() > 0.2: 
                    # Gera carga horária entre 4 e 8 horas
                    horas_trab = random.uniform(4, 8)
                    
                    # Hora de entrada aleatória entre 07:00 e 10:00
                    h_ent = random.randint(7, 10)
                    m_ent = random.randint(0, 59)
                    entrada_str = f"{h_ent:02d}:{m_ent:02d}"
                    
                    # Calcula saída
                    entrada_dt = datetime.strptime(entrada_str, "%H:%M")
                    saida_dt = entrada_dt + timedelta(hours=horas_trab)
                    saida_str = saida_dt.strftime("%H:%M")
                    
                    cursor.execute("""
                        INSERT INTO registros_ponto (id_funcionario, data, hora_entrada, hora_saida)
                        VALUES (?, ?, ?, ?)
                    """, (f_id, data_str, entrada_str, saida_str))
                    registros_count += 1

    conn.commit()
    conn.close()
    print(f"Sucesso! {registros_count} registros inseridos com carga horária de 4h a 8h.")

if __name__ == "__main__":
    repopulate()
