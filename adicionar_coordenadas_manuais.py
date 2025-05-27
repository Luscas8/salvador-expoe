import os
import django
import sys

# Configurar o Django
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'salvador_expoe.settings')
django.setup()

from adicionar_coordenadas import adicionar_coordenadas_manuais
from core.models import Bairro

def adicionar_coordenadas_manuais(nome_bairro, latitude, longitude):
    try:
        bairro = Bairro.objects.get(nome=nome_bairro)
        bairro.latitude = latitude
        bairro.longitude = longitude
        bairro.save()
        print(f"Coordenadas atualizadas para {nome_bairro}")
    except Bairro.DoesNotExist:
        print(f"Bairro {nome_bairro} não encontrado")

def main():
    # Lista de bairros com suas coordenadas
    coordenadas_bairros = [
        ("Acupe de Brotas", -12.9940335, -38.4941904),
        ("Alphaville I", -12.9405266, -38.4024687),
        ("Alto da Terezinha", -12.884567, -38.4777643),
        ("Alto das Pombas", -12.9730401, -38.502304),
        ("Alto do Cabrito", -12.909068, -38.4760034),
        ("Alto do Coqueirinho", -12.9388242, -38.3709312),
        ("Alto do Peru", -12.9378848, -38.4889345),
        ("Amaralina", -13.0124288, -38.4705355),
        ("Areia Branca", -12.8471507, -38.354401),
        ("Arenoso", -12.9480133, -38.4442423),
        ("Armação", -12.9869889, -38.4389824),
        ("Arraial do Retiro", -12.9439099, -38.4679066),
        ("Bairro da Paz", -12.9289596, -38.3779672),
        ("Baixa de Quintas", -12.9629702, -38.4925029),
        ("Baixa dos Sapateiros", -12.9688909, -38.5040726),
        ("Barbalho", -12.9660252, -38.5014166),
        ("Barra", -13.0084596, -38.5240096),
        ("Barragem de Ipitanga", -12.8611919, -38.388965),
        ("Barreiras", -12.9416765, -38.4588747),
        ("Barris", -12.9856151, -38.5152099),
        ("Barroquinha", -12.977043, -38.5132396),
        ("Boa Viagem", -12.9313803, -38.5092989),
        ("Boa Vista de São Caetano", -12.9254461, -38.4784214),
        ("Boa Vista do Lobato", -12.9091444, -38.4723263),
        ("Boca da Mata", -12.9008226, -38.3875672),
        ("Boca da Mata de Valéria", -12.8601853, -38.4353754),
        ("Boca do Rio", -12.9777378, -38.4291193),
        ("Bonfim", -12.9251875, -38.5073284),
        ("Brotas", -12.9857613, -38.4998158),
        ("CEASA", -12.8380547, -38.3692175),
        ("Cabula", -12.9580582, -38.4698385),
        ("Cabula VI", -12.954279, -38.4407152),
        ("Caixa D'Água", -12.9587814, -38.492795),
        ("Cajazeiras", -12.8993599, -38.4079273),
        ("Calabetão", -12.929889, -38.4680526),
        ("Calçada", -12.9448596, -38.5001028),
        ("Caminho das Árvores", -12.9778544, -38.4605517),
        ("Caminho de Areia", -12.9240591, -38.5072167),
        ("Campinas de Brotas", -12.9823353, -38.4771324),
        ("Campinas de Pirajá", -12.9251232, -38.4700758),
        ("Campo Grande", -12.9884598, -38.5144913),
        ("Canabrava", -12.924559, -38.4202172),
        ("Candeal", -12.9921219, -38.4825103),
        ("Canela", -12.9920827, -38.5224338),
        ("Capelinha", -12.9285806, -38.4843352),
        ("Cassange", -12.9024806, -38.3726132),
        ("Castelo Branco", -12.9022887, -38.4286459),
        ("Centro", -12.97604, -38.5132332),
        ("Centro Administrativo da Bahia", -12.947908, -38.4282302),
        ("Chame-Chame", -13.0030112, -38.5211205),
        ("Sussuarana", -12.9345, -38.439),
        ("Vale das Pedrinhas - Nordeste", -13.0094, -38.4781),
        ("Cajazeiras VIII", -12.9042, -38.4148),
        ("Canabrava", -12.55, -38.5167),
        ("Fazenda Grande III", -12.9034, -38.3956),
        ("Granjas Rurais Presidente Vargas", -12.9243, -38.4675),
    ]

    print("Iniciando adição de coordenadas...")
    for nome, lat, lon in coordenadas_bairros:
        adicionar_coordenadas_manuais(nome, lat, lon)
    print("Processo finalizado!")

if __name__ == '__main__':
    main() 