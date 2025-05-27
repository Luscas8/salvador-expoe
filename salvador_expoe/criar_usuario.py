import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'salvador_expoe.settings')
django.setup()

from django.contrib.auth.models import User

try:
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@exemplo.com', 'senha123')
        print('Superusuário criado com sucesso!')
    else:
        print('Usuário admin já existe!')
except Exception as e:
    print(f'Erro ao criar superusuário: {e}')
