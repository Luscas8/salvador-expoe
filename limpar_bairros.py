import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'salvador_expoe.settings')
django.setup()

from core.models import Bairro

# Lista de bairros reais de Salvador (exemplo, pode ser expandida)
bairros_reais = [
    'Barra', 'Pituba', 'Rio Vermelho', 'Ondina', 'Graça',
    'Campo Grande', 'Centro', 'Comércio', 'Pelourinho', 'Liberdade',
    'Brotas', 'Nazaré', 'Federação', 'Vitoria', 'Canela', 'Garcia',
    'Barris', 'Tororo', 'Barbalho', 'Santo Antônio', 'São Caetano',
    'Boa Viagem', 'Ribeira', 'Bonfim', 'Massaranduba', 'Calçada'
    # Adicione outros bairros reais conforme necessário
]

# Remove bairros que não estão na lista
Bairro.objects.exclude(nome__in=bairros_reais).delete()
print("Bairros irreais/duplicados removidos!") 