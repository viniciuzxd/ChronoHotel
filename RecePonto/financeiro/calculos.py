import sqlite3
from datetime import datetime, timedelta
import calendar
from database.conexao import conectar

# 1. Tabela Base de Valores
VALORES_POR_CARGO = {
    "Cozinha": 7.50,
    "Cozinheiro": 7.50,
    "Cozinheira": 7.50,
    "Camareira": 7.50,
    "Recepcionista": 7.50,
    "Recepcionista Comum": 7.50,
    "Manutenção": 7.50,
    "Gerente": 7.50,
    "Folguista": 7.50,
    "Garçom": 7.50,
    "Serviços Gerais": 7.50
}

def calcular_horas_decimais(hora_entrada, hora_saida, cargo=""):
    """Calcula a diferença de horas. Agora recebe o cargo para regras especiais."""
    if not hora_entrada or not hora_saida or hora_saida in ["Em aberto", "Aberto"]:
        return 0.0
    
    formato = "%H:%M"
    try:
        t1 = datetime.strptime(hora_entrada, formato)
        t2 = datetime.strptime(hora_saida, formato)
        
        # Se a saída for menor que a entrada (ex: 22:00 às 06:00), virou a madrugada (adiciona 1 dia)
        if t2 < t1:
            t2 += timedelta(days=1)
            
        delta = t2 - t1
        horas = delta.total_seconds() / 3600.0
        
        # --- REGRA DO FOLGUISTA 24 HORAS ---
        # Se ele entra as 08:00 e sai as 08:00, as horas dariam Zero. 
        # Se der menos de 12 horas trabalhadas para um Folguista, significa que o relógio deu a volta (24h).
        cargo_limpo = cargo.strip().title() if cargo else ""
        if cargo_limpo == "Folguista" and horas <= 12.0:
            horas += 24.0
            
        return horas
    except:
        return 0.0

def converter_decimais_para_horas(horas_decimais):
    horas = int(horas_decimais)
    minutos = int(round((horas_decimais - horas) * 60))
    if minutos >= 60:
        horas += 1
        minutos -= 60
    return f"{horas}h{minutos:02d}m"

def gerar_relatorio_pagamento(id_funcionario, data_inicio, data_fim):
    """Gera o consolidado do mês/quinzena e adiciona os extras."""
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("SELECT cargo, valor_hora FROM funcionarios WHERE id = ?", (id_funcionario,))
    res = cursor.fetchone()
    
    if not res:
        conn.close()
        return None
        
    cargo_db, valor_hora_func = res
    cargo_norm = cargo_db.strip().title() if cargo_db else ""
    
    cursor.execute('''
        SELECT hora_entrada, hora_saida FROM registros_ponto 
        WHERE id_funcionario = ? 
        AND data BETWEEN ? AND ?
        AND hora_saida IS NOT NULL AND hora_saida NOT IN ('Em aberto', 'Aberto')
    ''', (id_funcionario, data_inicio, data_fim))
    
    registros = cursor.fetchall()
    conn.close()
    
    total_horas_decimais = 0.0
    salario_total = 0.0
    
    for entrada, saida in registros:
        # Repassa o cargo para a fórmula entender se é o Folguista
        h_dec = calcular_horas_decimais(entrada, saida, cargo_norm)
        total_horas_decimais += h_dec
        
        # --- REGRA DE ALMOÇO DO FOLGUISTA (+ R$ 15,00) ---
        # Se o turno foi igual ou maior que 23 horas (permitindo margem de tolerância)
        extra_almoco = 0.0
        if cargo_norm == "Folguista" and h_dec >= 23.0:
            extra_almoco = 15.0
            
        salario_total += (h_dec * valor_hora_func) + extra_almoco
        
    return {
        "cargo": cargo_db,
        "horas_formatadas": converter_decimais_para_horas(total_horas_decimais),
        "salario": round(salario_total, 2)
    }

def obter_datas_periodo(mes, ano, tipo="1"):
    if tipo == "1":
        inicio = f"{ano}-{mes:02d}-01"
        fim = f"{ano}-{mes:02d}-15"
    elif tipo == "2":
        ultimo_dia = calendar.monthrange(ano, mes)[1]
        inicio = f"{ano}-{mes:02d}-16"
        fim = f"{ano}-{mes:02d}-{ultimo_dia}"
    else:
        ultimo_dia = calendar.monthrange(ano, mes)[1]
        inicio = f"{ano}-{mes:02d}-01"
        fim = f"{ano}-{mes:02d}-{ultimo_dia}"
    return inicio, fim