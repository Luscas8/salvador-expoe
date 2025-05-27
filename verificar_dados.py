import os
import django
import sys

# Configurar o Django
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'salvador_expoe.settings')
django.setup()

from core.models import Bairro, Avaliacao
from django.db.models import Avg, Count

def verificar_dados():
    """
    Função para verificar os dados no banco de dados
    """
    print("Verificando dados no banco de dados...")
    
    # Verificar total de bairros
    total_bairros = Bairro.objects.count()
    print(f"\nTotal de bairros: {total_bairros}")
    
    # Verificar bairros com coordenadas
    bairros_com_coordenadas = Bairro.objects.filter(
        latitude__isnull=False,
        longitude__isnull=False
    ).count()
    print(f"Bairros com coordenadas: {bairros_com_coordenadas}")
    
    # Verificar bairros com avaliações
    bairros_com_avaliacoes = Bairro.objects.annotate(
        total_avaliacoes=Count('avaliacoes')
    ).filter(total_avaliacoes__gt=0)
    print(f"Bairros com avaliações: {bairros_com_avaliacoes.count()}")
    
    # Verificar bairros com avaliações mas sem coordenadas
    bairros_sem_coordenadas = bairros_com_avaliacoes.filter(
        latitude__isnull=True,
        longitude__isnull=True
    )
    
    print("\nBairros com avaliações mas sem coordenadas:")
    for bairro in bairros_sem_coordenadas:
        print(f"- {bairro.nome}: Total de avaliações = {bairro.total_avaliacoes}")
    
    # Verificar bairros com coordenadas e avaliações
    bairros_completo = Bairro.objects.annotate(
        nota_media=Avg('avaliacoes__nota'),
        total_avaliacoes=Count('avaliacoes')
    ).filter(
        nota_media__isnull=False,
        latitude__isnull=False,
        longitude__isnull=False
    ).order_by('-nota_media')
    
    print(f"\nBairros com coordenadas e avaliações: {bairros_completo.count()}")
    
    # Mostrar detalhes dos bairros com coordenadas e avaliações
    print("\nDetalhes dos bairros com coordenadas e avaliações:")
    for bairro in bairros_completo:
        print(f"- {bairro.nome}: Nota média = {bairro.nota_media:.1f}, Total de avaliações = {bairro.total_avaliacoes}, Coordenadas = ({bairro.latitude}, {bairro.longitude})")

if __name__ == "__main__":
    verificar_dados() 