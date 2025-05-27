import os
import django
import sys
import time
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

# Configurar o Django
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'salvador_expoe.settings')
django.setup()

from core.models import Bairro

def geocodificar_bairro(nome_bairro):
    """
    Função para obter as coordenadas de um bairro usando OpenStreetMap
    """
    try:
        geolocator = Nominatim(user_agent="salvador_expoe")
        # Formatar a consulta para melhor precisão
        query = f"{nome_bairro}, Salvador, Bahia, Brasil"
        location = geolocator.geocode(query, timeout=10)
        
        if location:
            return location.latitude, location.longitude
        return None
    except GeocoderTimedOut:
        print(f"Tempo esgotado ao buscar {nome_bairro}")
        return None
    except Exception as e:
        print(f"Erro ao buscar {nome_bairro}: {str(e)}")
        return None

def atualizar_coordenadas():
    """
    Função principal para atualizar as coordenadas de todos os bairros
    """
    print("Iniciando atualização de coordenadas...")
    bairros = Bairro.objects.all()
    total_bairros = bairros.count()
    atualizados = 0
    
    for i, bairro in enumerate(bairros, 1):
        print(f"\nProcessando {bairro.nome} ({i}/{total_bairros})...")
        
        # Tentar obter as coordenadas
        coordenadas = geocodificar_bairro(bairro.nome)
        
        if coordenadas:
            latitude, longitude = coordenadas
            bairro.latitude = latitude
            bairro.longitude = longitude
            bairro.save()
            print(f"✓ Coordenadas atualizadas: ({latitude}, {longitude})")
            atualizados += 1
        else:
            print(f"✗ Não foi possível obter coordenadas para {bairro.nome}")
        
        # Aguardar 1 segundo entre as requisições para respeitar os limites da API
        time.sleep(1)
    
    print(f"\nProcesso finalizado!")
    print(f"Total de bairros: {total_bairros}")
    print(f"Bairros atualizados: {atualizados}")
    print(f"Bairros não encontrados: {total_bairros - atualizados}")

if __name__ == "__main__":
    atualizar_coordenadas() 