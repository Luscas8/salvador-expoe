from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import PerfilUsuario

class Command(BaseCommand):
    help = 'Cria perfis de usuário para usuários existentes que não possuem um'

    def handle(self, *args, **kwargs):
        users_without_profile = User.objects.filter(perfil__isnull=True)
        profiles_created = 0

        for user in users_without_profile:
            PerfilUsuario.objects.get_or_create(usuario=user)
            profiles_created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Foram criados {profiles_created} perfis de usuário com sucesso!'
            )
        ) 