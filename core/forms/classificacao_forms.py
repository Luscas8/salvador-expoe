from django import forms
from ..models import Bairro

class ClassificacaoBairrosForm(forms.Form):
    bairro = forms.ModelChoiceField(
        queryset=Bairro.objects.all(),
        required=False,
        empty_label="Todos os bairros",
        label="Bairro"
    )
    
    criterio = forms.ChoiceField(
        choices=[
            ('media', 'Nota Média'),
            ('avaliacoes', 'Número de Avaliações')
        ],
        required=False,
        label="Critério de Ordenação"
    )
    
    ordem = forms.ChoiceField(
        choices=[
            ('desc', 'Maior para Menor'),
            ('asc', 'Menor para Maior')
        ],
        required=False,
        label="Ordem"
    ) 