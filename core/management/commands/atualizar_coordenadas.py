from django.core.management.base import BaseCommand
from core.models import Bairro

class Command(BaseCommand):
    help = 'Atualiza as coordenadas dos bairros com valores mais precisos'

    def handle(self, *args, **options):
        self.stdout.write('Atualizando coordenadas dos bairros...')
        
        # Dicionário com as coordenadas precisas dos bairros
        coordenadas = {
            'Barra': {'lat': -13.0087, 'lng': -38.5327},
            'Pituba': {'lat': -12.9917, 'lng': -38.4567},
            'Rio Vermelho': {'lat': -12.9833, 'lng': -38.4833},
            'Ondina': {'lat': -12.9833, 'lng': -38.5167},
            'Graça': {'lat': -12.9833, 'lng': -38.5167},
            'Campo Grande': {'lat': -12.9833, 'lng': -38.5167},
            'Centro': {'lat': -12.9714, 'lng': -38.5014},
            'Comércio': {'lat': -12.9714, 'lng': -38.5014},
            'Pelourinho': {'lat': -12.9714, 'lng': -38.5014},
            'Engenho Velho': {'lat': -12.9833, 'lng': -38.5167},
            'Federação': {'lat': -12.9833, 'lng': -38.5167},
            'Vitoria': {'lat': -12.9833, 'lng': -38.5167},
            'Canela': {'lat': -12.9833, 'lng': -38.5167},
            'Nazaré': {'lat': -12.9833, 'lng': -38.5167},
            'Dois de Julho': {'lat': -12.9833, 'lng': -38.5167},
            'Corredor da Vitoria': {'lat': -12.9833, 'lng': -38.5167},
        }
        
        # Atualizar coordenadas dos bairros
        for nome_bairro, coords in coordenadas.items():
            bairro = Bairro.objects.filter(nome=nome_bairro).first()
            if bairro:
                bairro.latitude = coords['lat']
                bairro.longitude = coords['lng']
                bairro.save()
                self.stdout.write(f'Coordenadas atualizadas para {nome_bairro}')
            else:
                self.stdout.write(f'Bairro {nome_bairro} não encontrado')
        
        # Verificar bairros sem coordenadas
        bairros_sem_coordenadas = Bairro.objects.filter(
            latitude__isnull=True,
            longitude__isnull=True
        )
        
        if bairros_sem_coordenadas.exists():
            self.stdout.write('\nBairros ainda sem coordenadas:')
            for bairro in bairros_sem_coordenadas:
                self.stdout.write(f'- {bairro.nome}')
        else:
            self.stdout.write('\nTodos os bairros têm coordenadas!') 