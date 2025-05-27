from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from django.contrib import messages
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
import folium
from folium.plugins import HeatMap
import json
from django.views.decorators.http import require_GET

from .models import Bairro, Avaliacao
from .forms.auth_forms import CadastroForm
from .forms.bairro_forms import AvaliacaoForm


class CustomLoginView(LoginView):
    template_name = 'core/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('home')
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().get(*args, **kwargs)


@method_decorator(csrf_protect, name='dispatch')
class CadastroView(CreateView):
    template_name = 'core/cadastro.html'
    form_class = CadastroForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(
            self.request, 'Cadastro realizado com sucesso! Faça login para continuar.')
        return super().form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().get(*args, **kwargs)


class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Dados para o heatmap - apenas bairros com avaliações
        bairros = Bairro.objects.annotate(
            media_nota=Avg('avaliacoes__nota'),
            total_avaliacoes=Count('avaliacoes')
        ).filter(
            media_nota__isnull=False,
            latitude__isnull=False,
            longitude__isnull=False
        )
        
        dados_heatmap = []
        for bairro in bairros:
            print(f"{bairro.nome}: lat={bairro.latitude}, lng={bairro.longitude}")
            # Nova lógica de normalização
            if bairro.media_nota <= 3:
                nota_normalizada = 0.0  # Vermelho para notas muito baixas (1-3)
            elif bairro.media_nota <= 5:
                nota_normalizada = 0.3  # Laranja para notas baixas (4-5)
            elif bairro.media_nota <= 7:
                nota_normalizada = 0.5  # Amarelo para notas médias (6-7)
            elif bairro.media_nota <= 9:
                nota_normalizada = 0.7  # Verde para notas boas (8-9)
            else:
                nota_normalizada = 1.0  # Azul para notas excelentes (10)
                
            dados_heatmap.append([
                float(bairro.latitude),
                float(bairro.longitude),
                nota_normalizada
            ])
        
        context['dados_heatmap'] = dados_heatmap
        context['form'] = AvaliacaoForm()
        context['avaliacoes_recentes'] = Avaliacao.objects.select_related('usuario', 'bairro').order_by('-data_criacao')[:10]
        
        return context


@login_required
def avaliar_bairro(request):
    if request.method == 'POST':
        form = AvaliacaoForm(request.POST)
        if form.is_valid():
            # Obter ou criar o bairro pelo nome
            nome_bairro = form.cleaned_data['bairro']
            bairro, _ = Bairro.objects.get_or_create(nome=nome_bairro)

            # Verificar se já existe avaliação para este bairro por este usuário
            avaliacao_existente = Avaliacao.objects.filter(
                usuario=request.user,
                bairro=bairro
            ).first()

            if avaliacao_existente:
                # Atualizar avaliação existente
                avaliacao_existente.nota = int(form.cleaned_data['nota'])
                avaliacao_existente.comentario = form.cleaned_data['comentario']
                avaliacao_existente.save()
                mensagem = 'Sua avaliação foi atualizada com sucesso!'
            else:
                # Criar nova avaliação
                avaliacao = form.save(commit=False)
                avaliacao.usuario = request.user
                avaliacao.bairro = bairro
                avaliacao.nota = int(form.cleaned_data['nota'])
                avaliacao.save()
                mensagem = 'Sua avaliação foi registrada com sucesso!'

            # Atualizar dados do mapa
            bairros = Bairro.objects.annotate(
                media_nota=Avg('avaliacoes__nota')
            ).filter(
                media_nota__isnull=False,
                latitude__isnull=False,
                longitude__isnull=False
            )
            
            dados_heatmap = []
            for bairro in bairros:
                print(f"{bairro.nome}: lat={bairro.latitude}, lng={bairro.longitude}")
                # Nova lógica de normalização
                if bairro.media_nota <= 3:
                    nota_normalizada = 0.0  # Vermelho para notas muito baixas (1-3)
                elif bairro.media_nota <= 5:
                    nota_normalizada = 0.3  # Laranja para notas baixas (4-5)
                elif bairro.media_nota <= 7:
                    nota_normalizada = 0.5  # Amarelo para notas médias (6-7)
                elif bairro.media_nota <= 9:
                    nota_normalizada = 0.7  # Verde para notas boas (8-9)
                else:
                    nota_normalizada = 1.0  # Azul para notas excelentes (10)
                    
                dados_heatmap.append([
                    float(bairro.latitude),
                    float(bairro.longitude),
                    nota_normalizada
                ])

            # Se for uma requisição AJAX, retornar JSON
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                avaliacoes_recentes = Avaliacao.objects.select_related('usuario', 'bairro').order_by('-data_criacao')[:10]
                avaliacoes_html = render_to_string('core/includes/avaliacoes_recentes.html', {
                    'avaliacoes_recentes': avaliacoes_recentes
                }, request=request)
                
                return JsonResponse({
                    'success': True,
                    'message': mensagem,
                    'dados_heatmap': dados_heatmap,
                    'avaliacoes_html': avaliacoes_html
                })

            messages.success(request, mensagem)
            return render(request, 'core/home.html', {
                'form': AvaliacaoForm(),
                'dados_heatmap': dados_heatmap,
                'avaliacoes_recentes': Avaliacao.objects.select_related('usuario', 'bairro').order_by('-data_criacao')[:10]
            })
    else:
        form = AvaliacaoForm()
        avaliacoes_recentes = Avaliacao.objects.select_related('usuario', 'bairro').order_by('-data_criacao')[:10]
        return render(request, 'core/home.html', {
            'form': form,
            'avaliacoes_recentes': avaliacoes_recentes
        })


@login_required
def minhas_avaliacoes(request):
    avaliacoes = Avaliacao.objects.filter(
        usuario=request.user).order_by('-data_criacao')
    return render(request, 'core/minhas_avaliacoes.html', {'avaliacoes': avaliacoes})


def is_float(value):
    try:
        float(value)
        return True
    except (TypeError, ValueError):
        return False


def classificacao_bairros(request):
    # Obter dados dos bairros e suas avaliações médias
    bairros = Bairro.objects.annotate(
        media=Avg('avaliacoes__nota'),
        total_avaliacoes=Count('avaliacoes')
    ).filter(
        media__isnull=False,
        latitude__isnull=False,
        longitude__isnull=False
    ).order_by('-media')

    # Filtrar bairros com latitude/longitude realmente válidas
    bairros = [
        b for b in bairros
        if b.latitude not in [None, '', 'None'] and b.longitude not in [None, '', 'None']
        and is_float(b.latitude) and is_float(b.longitude)
    ]

    # Calcular média geral
    media_geral = Avaliacao.objects.aggregate(Avg('nota'))['nota__avg'] or 0

    # Criar o mapa
    mapa = folium.Map(location=[-12.9714, -38.5014], zoom_start=12)
    
    # Preparar dados para o heatmap
    dados_heatmap = []
    for bairro in bairros:
        if bairro.latitude and bairro.longitude and bairro.media:
            # Nova lógica de normalização
            if bairro.media <= 3:
                nota_normalizada = 0.0  # Vermelho para notas muito baixas (1-3)
            elif bairro.media <= 5:
                nota_normalizada = 0.3  # Laranja para notas baixas (4-5)
            elif bairro.media <= 7:
                nota_normalizada = 0.5  # Amarelo para notas médias (6-7)
            elif bairro.media <= 9:
                nota_normalizada = 0.7  # Verde para notas boas (8-9)
            else:
                nota_normalizada = 1.0  # Azul para notas excelentes (10)
                
            dados_heatmap.append([
                float(bairro.latitude),
                float(bairro.longitude),
                nota_normalizada
            ])

    # Adicionar heatmap ao mapa
    HeatMap(dados_heatmap,
        gradient={
            0.0: '#ff0000',  # Vermelho para notas muito baixas (1-3)
            0.3: '#ff7f00',  # Laranja para notas baixas (4-5)
            0.5: '#ffff00',  # Amarelo para notas médias (6-7)
            0.7: '#00ff00',  # Verde para notas boas (8-9)
            1.0: '#0000ff'   # Azul para notas excelentes (10)
        },
        min_opacity=0.4,
        max_opacity=0.7,
        radius=15,
        blur=10
    ).add_to(mapa)

    # Adicionar marcadores
    for bairro in bairros:
        if bairro.latitude and bairro.longitude and bairro.media:
            # Definir cor baseada na nota
            if bairro.media <= 4:
                cor = 'red'
            elif bairro.media <= 6:
                cor = 'orange'
            elif bairro.media <= 8:
                cor = 'blue'
            else:
                cor = 'green'

            # Criar marcador
            folium.CircleMarker(
                location=[bairro.latitude, bairro.longitude],
                radius=5 + (bairro.media * 0.5),
                color=cor,
                fill=True,
                fill_color=cor,
                fill_opacity=0.7,
                popup=f'<div style="font-family: Arial; font-size: 12px;">'
                      f'<b>{bairro.nome}</b><br>'
                      f'Nota média: {bairro.media:.1f}<br>'
                      f'Total de avaliações: {bairro.total_avaliacoes}'
                      f'</div>'
            ).add_to(mapa)

    # Converter o mapa para HTML
    # mapa_html = mapa._repr_html_()  // Não precisa mais do HTML do folium

    context = {
        'dados_heatmap': json.dumps(dados_heatmap),
        'bairros_classificados': bairros,
        'total_bairros': len(bairros),
        'media_geral': media_geral
    }

    return render(request, 'core/classificacao_bairros.html', context)


@login_required
def mapa_calor(request):
    try:
        # Obter todos os bairros com avaliações
        bairros = Bairro.objects.annotate(
            media=Avg('avaliacoes__nota'),
            total_avaliacoes=Count('avaliacoes')
        ).filter(
            total_avaliacoes__gt=0,
            latitude__isnull=False,  # Garantir que latitude não seja nula
            longitude__isnull=False  # Garantir que longitude não seja nula
        )

        print(f"Total de bairros encontrados: {bairros.count()}")

        # Preparar dados para o mapa de calor
        dados_heatmap = []
        for bairro in bairros:
            if bairro.media is not None and bairro.latitude is not None and bairro.longitude is not None:
                try:
                    # Normalizar a média para um valor entre 0 e 1
                    if bairro.media <= 3:
                        intensidade = 0.0  # Vermelho para notas muito baixas (1-3)
                    elif bairro.media <= 5:
                        intensidade = 0.3  # Laranja para notas baixas (4-5)
                    elif bairro.media <= 7:
                        intensidade = 0.5  # Amarelo para notas médias (6-7)
                    elif bairro.media <= 9:
                        intensidade = 0.7  # Verde para notas boas (8-9)
                    else:
                        intensidade = 1.0  # Azul para notas excelentes (10)
                    
                    lat = float(bairro.latitude)
                    lng = float(bairro.longitude)
                    
                    print(f"Bairro {bairro.nome}: lat={lat}, lng={lng}, média={bairro.media}, intensidade={intensidade}")
                    dados_heatmap.append([lat, lng, intensidade])
                except (ValueError, TypeError) as e:
                    print(f"Erro ao processar bairro {bairro.nome}: {str(e)}")
                    continue

        # Calcular estatísticas
        total_bairros = bairros.count()
        total_avaliacoes = sum(b.total_avaliacoes for b in bairros)
        media_geral = bairros.aggregate(Avg('media'))['media__avg'] or 0

        # Obter top 5 bairros
        top_bairros = bairros.order_by('-media')[:5]
        melhor_bairro = top_bairros.first() if top_bairros else None

        # Garantir que os dados estejam no formato correto para JSON
        dados_heatmap_json = json.dumps(dados_heatmap)
        print(f"Dados do heatmap: {dados_heatmap_json}")

        context = {
            'dados_heatmap': dados_heatmap_json,
            'centro_mapa': [-12.9704, -38.5124],  # Coordenadas de Salvador
            'total_bairros': total_bairros,
            'total_avaliacoes': total_avaliacoes,
            'media_geral': float(media_geral) if media_geral else 0,
            'top_bairros': top_bairros,
            'melhor_bairro': melhor_bairro,
        }

        return render(request, 'core/mapa_calor.html', context)
    except Exception as e:
        print(f"Erro na view mapa_calor: {str(e)}")
        context = {
            'dados_heatmap': '[]',
            'centro_mapa': [-12.9704, -38.5124],
            'error': str(e)
        }
        return render(request, 'core/mapa_calor.html', context)

def mapa_calor_dados(request):
    print("Iniciando mapa_calor_dados")
    try:
        # Obter todos os bairros com avaliações
        bairros = Bairro.objects.annotate(
            media=Avg('avaliacoes__nota'),
            total_avaliacoes=Count('avaliacoes')
        ).filter(
            total_avaliacoes__gt=0
        )
        
        print(f"Total de bairros encontrados: {bairros.count()}")

        # Preparar dados para o mapa de calor
        dados_heatmap = []
        for bairro in bairros:
            if bairro.media is not None:
                # Normalizar a média para um valor entre 0 e 1
                if bairro.media <= 3:
                    intensidade = 0.0  # Vermelho para notas muito baixas (1-3)
                elif bairro.media <= 5:
                    intensidade = 0.3  # Laranja para notas baixas (4-5)
                elif bairro.media <= 7:
                    intensidade = 0.5  # Amarelo para notas médias (6-7)
                elif bairro.media <= 9:
                    intensidade = 0.7  # Verde para notas boas (8-9)
                else:
                    intensidade = 1.0  # Azul para notas excelentes (10)
                
                dados_heatmap.append([float(bairro.latitude), float(bairro.longitude), intensidade])
                print(f"Bairro {bairro.nome}: lat={bairro.latitude}, lng={bairro.longitude}, média={bairro.media}, intensidade={intensidade}")

        # Calcular estatísticas
        total_bairros = bairros.count()
        total_avaliacoes = sum(b.total_avaliacoes for b in bairros)
        media_geral = bairros.aggregate(Avg('media'))['media__avg'] or 0

        # Obter top 5 bairros com suas médias
        top_bairros = [
            {'nome': b.nome, 'media': b.media}
            for b in bairros.order_by('-media')[:5]
        ]

        # Encontrar a melhor nota
        melhor_nota = max((b.media for b in bairros if b.media is not None), default=0)

        # Adicionar marcadores para cada bairro
        marcadores = []
        for bairro in bairros:
            if bairro.media is not None:
                # Definir cor baseada na nota
                if bairro.media <= 3:
                    cor = '#ff0000'  # Vermelho
                elif bairro.media <= 5:
                    cor = '#ff7f00'  # Laranja
                elif bairro.media <= 7:
                    cor = '#ffff00'  # Amarelo
                elif bairro.media <= 9:
                    cor = '#00ff00'  # Verde
                else:
                    cor = '#0000ff'  # Azul

                marcadores.append({
                    'lat': float(bairro.latitude),
                    'lng': float(bairro.longitude),
                    'nome': bairro.nome,
                    'media': float(bairro.media),
                    'cor': cor
                })

        response_data = {
            'data': dados_heatmap,
            'marcadores': marcadores,
            'stats': {
                'total_bairros': total_bairros,
                'total_avaliacoes': total_avaliacoes,
                'media_geral': float(media_geral),
                'top_bairros': top_bairros,
                'melhor_nota': float(melhor_nota)
            }
        }
        
        print("Dados preparados com sucesso:", response_data)
        return JsonResponse(response_data)
    except Exception as e:
        print(f"Erro ao gerar dados do mapa: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

@require_GET
def dados_radar(request):
    bairros = Bairro.objects.annotate(
        media=Avg('avaliacoes__nota'),
        total_avaliacoes=Count('avaliacoes')
    ).filter(
        media__isnull=False
    ).order_by('-media')

    data = [
        {
            'nome': b.nome,
            'media': float(b.media or 0),
            'total': b.total_avaliacoes or 0
        }
        for b in bairros
    ]
    return JsonResponse({'bairros': data})

@require_GET
def ranking_bairros_html(request):
    bairros = Bairro.objects.annotate(
        media_nota=Avg('avaliacoes__nota'),
        total_avaliacoes=Count('avaliacoes')
    ).filter(
        media_nota__isnull=False,
        latitude__isnull=False,
        longitude__isnull=False
    ).order_by('-media_nota')
    html = render_to_string('core/includes/ranking_bairros.html', {'ranking_bairros': bairros})
    return JsonResponse({'html': html})
