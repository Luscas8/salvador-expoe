from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth.models import User
from core.models import Bairro, Avaliacao

class Command(BaseCommand):
    help = 'Adiciona novas avaliações para os bairros'

    def handle(self, *args, **options):
        self.stdout.write('Adicionando novas avaliações...')
        
        # Lista de usuários de teste
        usuarios = [
            {'username': 'usuario1', 'email': 'usuario1@teste.com', 'password': 'teste123'},
            {'username': 'usuario2', 'email': 'usuario2@teste.com', 'password': 'teste123'},
            {'username': 'usuario3', 'email': 'usuario3@teste.com', 'password': 'teste123'},
        ]
        
        # Criar ou obter usuários
        users = []
        for user_data in usuarios:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                email=user_data['email']
            )
            if created:
                user.set_password(user_data['password'])
                user.save()
            users.append(user)
        
        # Lista de bairros populares para avaliação
        bairros_populares = [
            'Barra', 'Pituba', 'Rio Vermelho', 'Ondina', 'Graça',
            'Campo Grande', 'Centro', 'Comércio', 'Pelourinho'
        ]
        
        # Avaliações variadas
        avaliacoes = [
            {'nota': 9, 'comentario': 'Ótimo lugar para morar!'},
            {'nota': 8, 'comentario': 'Boa localização e infraestrutura'},
            {'nota': 7, 'comentario': 'Bairro tranquilo e agradável'},
            {'nota': 10, 'comentario': 'Melhor bairro de Salvador!'},
            {'nota': 6, 'comentario': 'Regular, precisa melhorar'},
        ]
        
        # Adicionar avaliações
        with transaction.atomic():
            for user in users:
                for bairro_nome in bairros_populares:
                    bairro = Bairro.objects.filter(nome=bairro_nome).first()
                    if bairro:
                        # Verificar se já existe avaliação deste usuário para este bairro
                        if not Avaliacao.objects.filter(usuario=user, bairro=bairro).exists():
                            avaliacao = avaliacoes[len(users) % len(avaliacoes)]
                            Avaliacao.objects.create(
                                usuario=user,
                                bairro=bairro,
                                nota=avaliacao['nota'],
                                comentario=avaliacao['comentario']
                            )
                            self.stdout.write(f"Adicionada avaliação para {bairro.nome} por {user.username}")
        
        self.stdout.write(self.style.SUCCESS('\nNovas avaliações adicionadas com sucesso!'))
        self.stdout.write(f"Total de avaliações no banco: {Avaliacao.objects.count()}") 