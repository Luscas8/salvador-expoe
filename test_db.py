import os
import django
from django.db import connection
from django.core.management import call_command

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'salvador_expoe.settings')
django.setup()

def test_database():
    print("Iniciando testes do banco de dados...")
    
    try:
        # 1. Testar conexão
        print("\n1. Testando conexão com o banco de dados...")
        connection.ensure_connection()
        print("✅ Conexão com o banco de dados estabelecida com sucesso!")
        
        # 2. Verificar migrações
        print("\n2. Verificando migrações...")
        call_command('showmigrations')
        print("✅ Migrações verificadas com sucesso!")
        
        # 3. Verificar tabelas
        print("\n3. Verificando tabelas...")
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            print("Tabelas encontradas:")
            for table in tables:
                print(f"- {table[0]}")
        
        print("\n✅ Testes concluídos com sucesso!")
        print("O banco de dados está funcionando corretamente!")
        
    except Exception as e:
        print(f"\n❌ Erro encontrado: {str(e)}")
        print("O banco de dados não está funcionando corretamente.")

if __name__ == '__main__':
    test_database() 