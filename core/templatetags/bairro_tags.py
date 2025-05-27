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