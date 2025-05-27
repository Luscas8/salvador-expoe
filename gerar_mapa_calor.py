import os
import django
import sys
import folium
from folium.plugins import HeatMap
from django.db.models import Avg

# Configurar o Django
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)
os.environ['DJANGO_SETTINGS_MODULE'] = 'salvador_expoe.settings'
django.setup()

from core.models import Bairro, Avaliacao

def gerar_mapa_calor():
    # Criar o mapa centrado em Salvador
    mapa = folium.Map(location=[-12.9714, -38.5014], zoom_start=12)

    # Obter dados dos bairros e suas avaliações médias
    bairros = Bairro.objects.annotate(
        media_avaliacoes=Avg('avaliacoes__nota')
    ).filter(
        media_avaliacoes__isnull=False,  # Apenas bairros com avaliações
        latitude__isnull=False,
        longitude__isnull=False
    )
    
    dados_heatmap = []

    for bairro in bairros:
        # Adicionar ponto ao heatmap com peso baseado na média
        dados_heatmap.append([
            bairro.latitude,
            bairro.longitude,
            bairro.media_avaliacoes
        ])

    # Definir a escala de cores personalizada com base nas notas de 1 a 10
    gradient = {
        0.0: 'red',     # 1-2
        0.2: 'red',     # 1-2
        0.3: 'orange',  # 3-4
        0.4: 'orange',  # 3-4
        0.5: 'yellow',  # 5-6
        0.6: 'yellow',  # 5-6
        0.7: 'blue',    # 7-8
        0.8: 'blue',    # 7-8
        0.9: 'green',   # 9
        1.0: 'green'    # 10
    }

    # Adicionar o heatmap ao mapa com configurações otimizadas
    HeatMap(
        dados_heatmap,
        gradient=gradient,
        min_opacity=0.6,      # Aumentado para melhor visibilidade
        max_opacity=0.9,      # Aumentado para melhor visibilidade
        radius=75,            # TESTE: valor intermediário
        blur=50               # TESTE: muito mais suave
    ).add_to(mapa)

    # Adicionar marcadores para cada bairro
    for bairro in bairros:
        # Criar marcador com popup
        # Definir cor baseada na nota
        if bairro.media_avaliacoes <= 4:
            cor = 'red'
        elif bairro.media_avaliacoes <= 6:
            cor = 'orange'
        elif bairro.media_avaliacoes <= 8:
            cor = 'blue'
        else:
            cor = 'green'

        folium.CircleMarker(
            location=[bairro.latitude, bairro.longitude],
            radius=8,  # Tamanho fixo para melhor visualização
            color=cor,
            fill=True,
            fill_color=cor,
            fill_opacity=0.7,
            popup=f'<div style="font-family: Arial; font-size: 12px;">'
                  f'<b>{bairro.nome}</b><br>'
                  f'Nota média: {bairro.media_avaliacoes:.1f}</div>'
        ).add_to(mapa)

    # Adicionar legenda mais visível
    legend_html = '''
    <div style="position: fixed; 
                bottom: 50px; right: 50px; width: 180px; height: 150px; 
                border:2px solid grey; z-index:9999; font-size:14px;
                background-color:white;
                padding: 10px;
                border-radius: 5px;
                box-shadow: 0 0 10px rgba(0,0,0,0.2);">
        <div style="font-weight: bold; margin-bottom: 10px; text-align: center;">
            Legenda de Notas
        </div>
        <div style="display: flex; align-items: center; margin-bottom: 8px;">
            <div style="width: 20px; height: 20px; background-color: red; margin-right: 10px; border-radius: 3px;"></div>
            <span>1-4: Vermelho</span>
        </div>
        <div style="display: flex; align-items: center; margin-bottom: 8px;">
            <div style="width: 20px; height: 20px; background-color: orange; margin-right: 10px; border-radius: 3px;"></div>
            <span>5-6: Laranja</span>
        </div>
        <div style="display: flex; align-items: center; margin-bottom: 8px;">
            <div style="width: 20px; height: 20px; background-color: blue; margin-right: 10px; border-radius: 3px;"></div>
            <span>7-8: Azul</span>
        </div>
        <div style="display: flex; align-items: center;">
            <div style="width: 20px; height: 20px; background-color: green; margin-right: 10px; border-radius: 3px;"></div>
            <span>9-10: Verde</span>
        </div>
    </div>
    '''
    mapa.get_root().html.add_child(folium.Element(legend_html))

    # Salvar o mapa
    mapa.save('mapa_calor_salvador.html')
    print("Mapa de calor gerado com sucesso! Verifique o arquivo 'mapa_calor_salvador.html'")

if __name__ == '__main__':
    gerar_mapa_calor() 