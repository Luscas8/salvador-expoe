import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'salvador_expoe.settings')
django.setup()

from django.contrib.auth.models import User

try:
    # Primeiro, vamos remover o usuário admin se ele existir
    User.objects.filter(username='admin').delete()
    
    # Agora vamos criar um novo
    User.objects.create_superuser(
        username='admin',
        email='admin@admin.com',
        password='admin123'
    )
    print('Novo superusuário criado com sucesso!')
    print('Username: admin')
    print('Senha: admin123')
except Exception as e:
    print(f'Erro: {e}')
