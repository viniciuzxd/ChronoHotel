import shutil
import os
from datetime import datetime

def realizar_backup():
    """Cria uma cópia de segurança do banco de dados na pasta /backups"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_origem = os.path.join(base_dir, "dados_hotel.db")
    pasta_backup = os.path.join(base_dir, "backups")
    
    if not os.path.exists(pasta_backup):
        os.makedirs(pasta_backup)
    
    if os.path.exists(data_origem):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        nome_backup = f"backup_hotel_{timestamp}.db"
        caminho_destino = os.path.join(pasta_backup, nome_backup)
        
        shutil.copy2(data_origem, caminho_destino)
        print(f"✅ Backup realizado com sucesso: {nome_backup}")
        return True
    return False