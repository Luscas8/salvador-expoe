import os
import django

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'salvador_expoe.settings')
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

def padronizar_senhas():
    # Criar um superusuário se não existir
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@exemplo.com',
            password='senha123'
        )
        print("Novo superusuário 'admin' criado!")
    
    # Atualizar senha de todos os usuários
    usuarios = User.objects.all()
    for usuario in usuarios:
        usuario.set_password('senha123')
        usuario.save()
        print(f"Senha do usuário '{usuario.username}' atualizada")

    print("\nTodas as senhas foram padronizadas!")
    print("Use estas credenciais para login:")
    print("Username: admin")
    print("Senha: senha123")

if __name__ == '__main__':
    print("Iniciando padronização de senhas...")
    padronizar_senhas()
