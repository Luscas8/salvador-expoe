import os
import django
from django.core.management import call_command

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'salvador_expoe.settings')
django.setup()

def migrate_to_mysql():
    print("Iniciando migração para MySQL...")
    
    # 1. Criar dump dos dados do SQLite
    print("Criando backup dos dados atuais...")
    call_command('dumpdata', '--natural-foreign', '--natural-primary', 
                '--exclude=contenttypes', '--exclude=auth.permission',
                output='backup.json')
    
    # 2. Configurar para usar MySQL
    os.environ['USE_MYSQL'] = 'True'
    
    # 3. Criar as tabelas no MySQL
    print("Criando estrutura no MySQL...")
    call_command('migrate')
    
    # 4. Carregar os dados
    print("Carregando dados no MySQL...")
    call_command('loaddata', 'backup.json')
    
    print("Migração concluída com sucesso!")
    print("Para usar o MySQL, defina a variável de ambiente USE_MYSQL=True")
    print("Para voltar ao SQLite, remova a variável de ambiente USE_MYSQL")

if __name__ == '__main__':
    migrate_to_mysql() 