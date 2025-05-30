from django import template
from django.db.models import Avg, Count
from core.models import Bairro

register = template.Library()

@register.inclusion_tag('core/includes/ranking_bairros.html')
def ranking_bairros(limit=10):
    """
    Tag para exibir o ranking dos bairros.
    
    Args:
        limit: Número de bairros a serem exibidos (padrão: 10)
    """
    ranking_bairros = Bairro.objects.annotate(
        media_nota=Avg('avaliacoes__nota'),
        total_avaliacoes=Count('avaliacoes')
    ).filter(
        media_nota__isnull=False
    ).order_by('-media_nota')[:limit]
    
    return {
        'ranking_bairros': ranking_bairros
    }

@register.filter
def multiply(value, arg):
    """Multiplica o valor pelo argumento"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def sum(queryset, field):
    """Soma os valores de um campo específico do queryset"""
    try:
        return sum(getattr(obj, field) for obj in queryset)
    except (AttributeError, TypeError):
        return 0

@register.filter
def stars(value):
    """Gera estrelas de avaliação baseado no valor"""
    try:
        value = float(value)
        full_stars = int(value)
        half_star = value - full_stars >= 0.5
        
        stars_html = ''
        for _ in range(full_stars):
            stars_html += '<i class="fas fa-star"></i>'
        if half_star:
            stars_html += '<i class="fas fa-star-half-alt"></i>'
        for _ in range(5 - full_stars - (1 if half_star else 0)):
            stars_html += '<i class="far fa-star"></i>'
            
        return stars_html
    except (ValueError, TypeError):
        return ''

@register.filter
def progress_bar_color(media):
    """Retorna a classe CSS para a cor da barra de progresso baseado na média"""
    try:
        media = float(media)
        if media >= 7:
            return 'bg-success' # Verde
        elif media >= 4:
            return 'bg-warning' # Amarelo
        else:
            return 'bg-danger'  # Vermelho
    except (ValueError, TypeError):
        return '' 