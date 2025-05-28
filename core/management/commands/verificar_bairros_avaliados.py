from django.core.management.base import BaseCommand
from django.db.models import Avg, Count
from core.models import Bairro, Avaliacao

class Command(BaseCommand):
    help = 'Verifica bairros com avaliações e coordenadas'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Verificando bairros com avaliações e coordenadas...\n'))

        # Bairros com avaliações e coordenadas
        bairros_avaliados = Bairro.objects.annotate(
            media_nota=Avg('avaliacoes__nota'),
            total_avaliacoes=Count('avaliacoes')
        ).filter(
            media_nota__isnull=False,
            latitude__isnull=False,
            longitude__isnull=False
        ).order_by('-media_nota')

        self.stdout.write(f'Total de bairros com avaliações e coordenadas: {bairros_avaliados.count()}\n')

        # Detalhes dos bairros
        for bairro in bairros_avaliados:
            self.stdout.write(f'Bairro: {bairro.nome}')
            self.stdout.write(f'Latitude: {bairro.latitude}')
            self.stdout.write(f'Longitude: {bairro.longitude}')
            self.stdout.write(f'Média: {bairro.media_nota:.2f}')
            self.stdout.write(f'Total de avaliações: {bairro.total_avaliacoes}')
            
            # Listar avaliações
            avaliacoes = Avaliacao.objects.filter(bairro=bairro).select_related('usuario')
            self.stdout.write('Avaliações:')
            for avaliacao in avaliacoes:
                self.stdout.write(f'- {avaliacao.usuario.username}: {avaliacao.nota}/10 - {avaliacao.comentario or ""}')
            
            self.stdout.write('-' * 50 + '\n')

        # Bairros sem coordenadas
        bairros_sem_coordenadas = Bairro.objects.filter(
            latitude__isnull=True,
            longitude__isnull=True
        )
        
        if bairros_sem_coordenadas.exists():
            self.stdout.write(self.style.WARNING('\nBairros sem coordenadas:'))
            for bairro in bairros_sem_coordenadas:
                self.stdout.write(f'- {bairro.nome}')
            self.stdout.write('-' * 50 + '\n')

        # Bairros sem avaliações
        bairros_sem_avaliacoes = Bairro.objects.annotate(
            total_avaliacoes=Count('avaliacoes')
        ).filter(
            total_avaliacoes=0
        )
        
        if bairros_sem_avaliacoes.exists():
            self.stdout.write(self.style.WARNING('\nBairros sem avaliações:'))
            for bairro in bairros_sem_avaliacoes:
                self.stdout.write(f'- {bairro.nome}')
            self.stdout.write('-' * 50 + '\n') 