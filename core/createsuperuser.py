from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.management import setup_environ
from salvador_expoe import settings

setup_environ(settings)

from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.management import setup_environ
from salvador_expoe import settings

setup_environ(settings)

try:
    superuser = User.objects.create_superuser(
        username='admin',
        email='admin@exemplo.com',
        password='Admin123456'
    )
    print("Superusuário criado com sucesso!")
except IntegrityError:
    print("Usuário já existe!")
except Exception as e:
    print(f"Erro ao criar superusuário: {e}")