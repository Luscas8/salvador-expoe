from django.core.management.base import BaseCommand
from core.models import Bairro, Avaliacao
from django.db.models import Avg, Count

def verificar_dados():
    print("Verificando dados para o mapa de calor...")
    
    # Verificar bairros com coordenadas
    bairros_com_coordenadas = Bairro.objects.filter(
        latitude__isnull=False,
        longitude__isnull=False
    )
    print(f"\nTotal de bairros com coordenadas: {bairros_com_coordenadas.count()}")
    
    # Verificar bairros com avaliações
    bairros_com_avaliacoes = Bairro.objects.annotate(
        media_nota=Avg('avaliacoes__nota'),
        total_avaliacoes=Count('avaliacoes')
    ).filter(
        media_nota__isnull=False
    )
    print(f"Total de bairros com avaliações: {bairros_com_avaliacoes.count()}")
    
    # Verificar bairros que aparecerão no mapa
    bairros_no_mapa = Bairro.objects.annotate(
        media_nota=Avg('avaliacoes__nota'),
        total_avaliacoes=Count('avaliacoes')
    ).filter(
        media_nota__isnull=False,
        latitude__isnull=False,
        longitude__isnull=False
    )
    print(f"Total de bairros que aparecerão no mapa: {bairros_no_mapa.count()}")
    
    # Mostrar detalhes dos bairros que aparecerão no mapa
    print("\nDetalhes dos bairros que aparecerão no mapa:")
    for bairro in bairros_no_mapa:
        print(f"\nBairro: {bairro.nome}")
        print(f"Latitude: {bairro.latitude}")
        print(f"Longitude: {bairro.longitude}")
        print(f"Média de notas: {bairro.media_nota:.2f}")
        print(f"Total de avaliações: {bairro.total_avaliacoes}")

if __name__ == "__main__":
    import os
    import django
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'salvador_expoe.settings')
    django.setup()
    
    verificar_dados() 