from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('cadastro/', views.CadastroView.as_view(), name='cadastro'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('avaliar/', views.avaliar_bairro, name='avaliar_bairro'),
    path('minhas-avaliacoes/', views.minhas_avaliacoes, name='minhas_avaliacoes'),
    path('classificacao-bairros/', views.classificacao_bairros, name='classificacao_bairros'),
    path('mapa-calor/', views.mapa_calor, name='mapa_calor'),
    path('mapa-calor-dados/', views.mapa_calor_dados, name='mapa_calor_dados'),
    path('dados-radar/', views.dados_radar, name='dados_radar'),
    path('ranking-bairros-html/', views.ranking_bairros_html, name='ranking_bairros_html'),
]
