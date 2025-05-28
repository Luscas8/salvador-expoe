import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'salvador_expoe.settings')
django.setup()

from django.contrib.auth.models import User

# Verifica se o usuário já existe
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='lucasbrendoalves@gmail.com',
        password='admin123'  # Você pode mudar esta senha depois
    )
    print("Superusuário criado com sucesso!")
else:
    print("O superusuário já existe!") 