import os
import django
from django.db import transaction

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'salvador_expoe.settings')
django.setup()

from core.models import Bairro, Avaliacao
from django.contrib.auth.models import User

def criar_usuario_teste():
    # Criar usuário de teste
    user, created = User.objects.get_or_create(
        username='teste',
        email='teste@teste.com'
    )
    if created:
        user.set_password('teste123')
        user.save()
    return user

def popular_bairros():
    # Lista de bairros de Salvador com coordenadas
    bairros = [
        {'nome': 'Barra', 'latitude': -13.0087, 'longitude': -38.5327},
        {'nome': 'Pituba', 'latitude': -12.9917, 'longitude': -38.4567},
        {'nome': 'Rio Vermelho', 'latitude': -12.9917, 'longitude': -38.4867},
        {'nome': 'Ondina', 'latitude': -13.0017, 'longitude': -38.5067},
        {'nome': 'Graça', 'latitude': -12.9917, 'longitude': -38.5167},
    ]
    
    for bairro_data in bairros:
        Bairro.objects.get_or_create(
            nome=bairro_data['nome'],
            defaults={
                'latitude': bairro_data['latitude'],
                'longitude': bairro_data['longitude']
            }
        )

def criar_avaliacoes(user):
    # Criar algumas avaliações para cada bairro
    bairros = Bairro.objects.all()
    notas = [8, 9, 7, 6, 10]  # Diferentes notas para teste
    
    for i, bairro in enumerate(bairros):
        Avaliacao.objects.get_or_create(
            usuario=user,
            bairro=bairro,
            defaults={
                'nota': notas[i % len(notas)],
                'comentario': f'Avaliação de teste para {bairro.nome}'
            }
        )

def main():
    print("Iniciando população do banco de dados...")
    
    with transaction.atomic():
        # Criar usuário de teste
        user = criar_usuario_teste()
        print("Usuário de teste criado/atualizado")
        
        # Popular bairros
        popular_bairros()
        print("Bairros populados")
        
        # Criar avaliações
        criar_avaliacoes(user)
        print("Avaliações criadas")
    
    print("\nBanco de dados populado com sucesso!")
    print("Você pode fazer login com:")
    print("Usuário: teste")
    print("Senha: teste123")

if __name__ == "__main__":
    main() 