from django.core.management.base import BaseCommand
from core.models import Bairro

class Command(BaseCommand):
    help = 'Lista todos os bairros existentes no banco de dados'

    def handle(self, *args, **options):
        bairros = Bairro.objects.all().order_by('nome')
        
        self.stdout.write('\nBairros existentes no banco de dados:')
        self.stdout.write('-' * 50)
        
        for bairro in bairros:
            self.stdout.write(f'Nome: {bairro.nome}')
            self.stdout.write(f'Latitude: {bairro.latitude}')
            self.stdout.write(f'Longitude: {bairro.longitude}')
            self.stdout.write('-' * 50)
        
        self.stdout.write(f'\nTotal de bairros: {bairros.count()}') 