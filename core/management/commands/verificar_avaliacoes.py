from django.core.management.base import BaseCommand
from django.db.models import Avg, Count
from core.models import Bairro, Avaliacao

class Command(BaseCommand):
    help = 'Verifica e corrige as avaliações no banco de dados'

    def handle(self, *args, **options):
        self.stdout.write('Verificando avaliações...')
        
        # 1. Verificar total de avaliações
        total_avaliacoes = Avaliacao.objects.count()
        self.stdout.write(f'Total de avaliações: {total_avaliacoes}')
        
        # 2. Verificar bairros com avaliações
        bairros_com_avaliacoes = Bairro.objects.annotate(
            total_avaliacoes=Count('avaliacoes')
        ).filter(total_avaliacoes__gt=0)
        
        self.stdout.write(f'Bairros com avaliações: {bairros_com_avaliacoes.count()}')
        
        # 3. Verificar bairros com coordenadas
        bairros_com_coordenadas = Bairro.objects.filter(
            latitude__isnull=False,
            longitude__isnull=False
        )
        self.stdout.write(f'Bairros com coordenadas: {bairros_com_coordenadas.count()}')
        
        # 4. Verificar bairros que aparecem no mapa
        bairros_no_mapa = Bairro.objects.annotate(
            media=Avg('avaliacoes__nota'),
            total_avaliacoes=Count('avaliacoes')
        ).filter(
            total_avaliacoes__gt=0,
            latitude__isnull=False,
            longitude__isnull=False
        )
        
        self.stdout.write('\nDetalhes dos bairros que aparecem no mapa:')
        for bairro in bairros_no_mapa:
            self.stdout.write(f'\nBairro: {bairro.nome}')
            self.stdout.write(f'Latitude: {bairro.latitude}')
            self.stdout.write(f'Longitude: {bairro.longitude}')
            self.stdout.write(f'Média: {bairro.media:.2f}')
            self.stdout.write(f'Total de avaliações: {bairro.total_avaliacoes}')
            
            # Verificar avaliações individuais
            avaliacoes = Avaliacao.objects.filter(bairro=bairro)
            self.stdout.write('Avaliações:')
            for av in avaliacoes:
                self.stdout.write(f'- {av.usuario.username}: {av.nota}/10 - {av.comentario}') 