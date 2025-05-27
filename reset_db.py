import os
import django
import sys

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'salvador_expoe.settings')
django.setup()

from django.contrib.auth.models import User

# Remover todos os usuários
User.objects.all().delete()

# Criar novo superusuário
User.objects.create_superuser(
    username='admin',
    email='admin@admin.com',
    password='admin123',
    is_staff=True,
    is_active=True
)

print("Superusuário criado com sucesso!")
print("Username: admin")
print("Senha: admin123")
