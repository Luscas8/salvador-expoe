import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'salvador_expoe.settings')

import django
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

# Remover todos os usuários existentes
User.objects.all().delete()

# Criar novo usuário diretamente no banco
User.objects.create(
    username='admin',
    password=make_password('admin123'),
    is_superuser=True,
    is_staff=True,
    is_active=True
)

print("Novo usuário admin criado!")
print("Username: admin")
print("Senha: admin123")
