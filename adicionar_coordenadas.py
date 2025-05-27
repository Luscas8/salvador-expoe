import os
import django
import sys
import requests
from time import sleep

# Configurar o Django
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'salvador_expoe.settings')
django.setup()

from core.models import Bairro

def geocodificar_bairro(nome_bairro):
    # Adiciona "Salvador, BA" ao nome do bairro para melhorar a precisão
    query = f"{nome_bairro}, Salvador, BA"
    url = f"https://nominatim.openstreetmap.org/search?q={query}&format=json&limit=1"
    
    # Adiciona headers para identificar a aplicação
    headers = {
        'User-Agent': 'SalvadorExpoe/1.0'
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data:
                # Pega a primeira ocorrência que é geralmente a mais relevante
                return float(data[0]['lat']), float(data[0]['lon'])
        return None
    except Exception as e:
        print(f"Erro ao geocodificar {nome_bairro}: {str(e)}")
        return None

def adicionar_coordenadas_manuais(nome_bairro, latitude, longitude):
    try:
        bairro = Bairro.objects.get(nome=nome_bairro)
        bairro.latitude = float(latitude)
        bairro.longitude = float(longitude)
        bairro.save()
        print(f"Coordenadas adicionadas manualmente para {nome_bairro}: ({latitude}, {longitude})")
        return True
    except Bairro.DoesNotExist:
        print(f"Bairro {nome_bairro} não encontrado!")
        return False
    except Exception as e:
        print(f"Erro ao adicionar coordenadas para {nome_bairro}: {str(e)}")
        return False

def atualizar_coordenadas_todos_bairros():
    bairros = Bairro.objects.all()
    total = len(bairros)
    atualizados = 0
    
    print(f"Iniciando atualização de coordenadas para {total} bairros...")
    
    for bairro in bairros:
        print(f"\nProcessando {bairro.nome} ({atualizados + 1}/{total})...")
        
        # Busca coordenadas mais precisas
        coordenadas = geocodificar_bairro(bairro.nome)
        
        if coordenadas:
            latitude, longitude = coordenadas
            bairro.latitude = latitude
            bairro.longitude = longitude
            bairro.save()
            print(f"✓ Coordenadas atualizadas: ({latitude}, {longitude})")
            atualizados += 1
        else:
            print(f"✗ Não foi possível obter coordenadas precisas")
        
        # Respeita o limite de 1 requisição por segundo
        sleep(1)
    
    print(f"\nProcesso finalizado! {atualizados} bairros atualizados.")

def adicionar_coordenadas():
    """
    Função para adicionar coordenadas aos bairros que precisam
    """
    # Coordenadas do São Rafael
    bairro = Bairro.objects.get(nome='São Rafael')
    bairro.latitude = -12.9160999  # Latitude aproximada
    bairro.longitude = -38.4968986  # Longitude aproximada
    bairro.save()
    
    print(f"Coordenadas adicionadas para o bairro {bairro.nome}")

if __name__ == '__main__':
    atualizar_coordenadas_todos_bairros()
    adicionar_coordenadas() 