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
import os
from pathlib import Path # Certifique-se que Path está importado

from .models import Bairro, Avaliacao
from .forms.auth_forms import CadastroForm
from .forms.bairro_forms import AvaliacaoForm
from .forms import ClassificacaoBairrosForm, FiltroBairroForm


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
    except (ValueError, TypeError):
        return False


def classificacao_bairros(request):
    # Obter todos os bairros com suas médias e contagem de avaliações
    # Filtrar apenas bairros que foram avaliados (têm pelo menos uma avaliação)
    bairros_avaliados = Bairro.objects.annotate(
        media=Avg('avaliacoes__nota'),
        total_avaliacoes=Count('avaliacoes')
    ).filter(
        total_avaliacoes__gt=0
    ).order_by('-media')

    # Calcular total de bairros AVALIADOS
    total_bairros_avaliados_count = bairros_avaliados.count()

    # Calcular média geral dos bairros avaliados
    media_geral = bairros_avaliados.aggregate(media=Avg('avaliacoes__nota'))['media'] or 0

    # Calcular total de avaliações nos bairros avaliados
    total_avaliacoes = bairros_avaliados.aggregate(total=Count('avaliacoes'))['total'] or 0

    # Calcular faixas de avaliação APENAS para bairros avaliados
    faixas = {
        'Excelente__9_10_': bairros_avaliados.filter(media__gte=9).count(),
        'Muito_Bom__7_8_': bairros_avaliados.filter(media__gte=7, media__lt=9).count(),
        'Bom__5_6_': bairros_avaliados.filter(media__gte=5, media__lt=7).count(),
        'Regular__3_4_': bairros_avaliados.filter(media__gte=3, media__lt=5).count(),
        'Ruim__1_2_': bairros_avaliados.filter(media__lt=3).count()
    }

    # Formulário de filtros
    form = FiltroBairroForm(request.GET)
    # Aplicar filtros no queryset de bairros avaliados
    bairros_filtrados = bairros_avaliados # Começa com os avaliados

    if form.is_valid():
        bairro_nome = form.cleaned_data.get('bairro')
        criterio = form.cleaned_data.get('criterio')
        ordem = form.cleaned_data.get('ordem')

        if bairro_nome:
            bairros_filtrados = bairros_filtrados.filter(nome__icontains=bairro_nome)

        if criterio:
            if criterio == 'media':
                bairros_filtrados = bairros_filtrados.order_by('-media' if ordem == 'desc' else 'media')
            elif criterio == 'avaliacoes':
                bairros_filtrados = bairros_filtrados.order_by('-total_avaliacoes' if ordem == 'desc' else 'total_avaliacoes')

    # Recalcular total de bairros AVALIADOS e filtrados para a exibição
    bairros_para_exibicao = bairros_filtrados
    total_bairros_exibicao = bairros_para_exibicao.count()

    # Calcular estatísticas adicionais com base nos bairros FILTRADOS
    # total_avaliacoes já foi calculado acima para todos os bairros avaliados
    # media_avaliacoes_por_bairro pode ser calculado sobre bairros_avaliados
    media_avaliacoes_por_bairro = total_avaliacoes / total_bairros_avaliados_count if total_bairros_avaliados_count > 0 else 0
    
    # Encontrar bairros com mais avaliações (do queryset avaliado)
    bairros_mais_avaliados = bairros_avaliados.order_by('-total_avaliacoes')[:5]
    
    # Encontrar bairros com melhor média (do queryset avaliado)
    bairros_melhor_media = bairros_avaliados.order_by('-media')[:5]
    
    # Calcular tendências (comparando com a média geral dos bairros avaliados)
    for bairro in bairros_para_exibicao:
        if bairro.media:
            bairro.tendencia = 'up' if bairro.media > media_geral else 'down' if bairro.media < media_geral else 'stable'

    # Preparar dados para os gráficos em formato JSON (usando bairros_avaliados para os totais de faixas e bairros_para_exibicao para o top 10)
    # Os dados das faixas devem refletir a distribuição GERAL dos bairros avaliados, não apenas os filtrados
    faixas_data = list(faixas.values())
    # O top 10 deve ser dos bairros filtrados e ordenados
    top_bairros_data = [
        {'nome': b.nome, 'media': float(b.media) if b.media is not None else 0}
        for b in bairros_para_exibicao[:10]
    ]

    context = {
        'bairros': bairros_para_exibicao, # Passa os bairros filtrados para a tabela
        'media_geral': media_geral,
        'total_bairros': total_bairros_avaliados_count, # Total de bairros AVALIADOS
        'total_bairros_exibicao': total_bairros_exibicao, # Total de bairros na tabela após filtros
        'faixas': faixas, # Faixas dos bairros AVALIADOS
        'form': form,
        'total_avaliacoes': total_avaliacoes, # Total de avaliações GERAL
        'media_avaliacoes_por_bairro': media_avaliacoes_por_bairro,
        'bairros_mais_avaliados': bairros_mais_avaliados,
        'bairros_melhor_media': bairros_melhor_media,
        'faixas_data_json': json.dumps(faixas_data),
        'top_bairros_data_json': json.dumps(top_bairros_data),
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
