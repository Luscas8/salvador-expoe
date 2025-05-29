import os
import shutil
from datetime import datetime
import logging

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/backup.log'),
        logging.StreamHandler()
    ]
)

def create_backup():
    try:
        # Criar diretório de backup se não existir
        backup_dir = 'backups'
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        # Nome do arquivo de backup com timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = f'{backup_dir}/db_backup_{timestamp}.sqlite3'

        # Copiar o arquivo do banco de dados
        shutil.copy2('db.sqlite3', backup_file)
        
        # Manter apenas os últimos 5 backups
        backups = sorted([f for f in os.listdir(backup_dir) if f.startswith('db_backup_')])
        if len(backups) > 5:
            for old_backup in backups[:-5]:
                os.remove(os.path.join(backup_dir, old_backup))

        logging.info(f'Backup criado com sucesso: {backup_file}')
        return True

    except Exception as e:
        logging.error(f'Erro ao criar backup: {str(e)}')
        return False

if __name__ == '__main__':
    create_backup() 