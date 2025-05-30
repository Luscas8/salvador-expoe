from django import forms
from ..models import Bairro

class ClassificacaoBairrosForm(forms.Form):
    bairro = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar bairro...'
        })
    )
    criterio = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'Ordenar por...'),
            ('media', 'Média'),
            ('avaliacoes', 'Número de Avaliações')
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    ordem = forms.ChoiceField(
        required=False,
        choices=[
            ('desc', 'Maior para Menor'),
            ('asc', 'Menor para Maior')
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

class FiltroBairroForm(forms.Form):
    bairro = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar bairro...'
        })
    )
    criterio = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'Ordenar por...'),
            ('media', 'Média'),
            ('avaliacoes', 'Número de Avaliações')
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    ordem = forms.ChoiceField(
        required=False,
        choices=[
            ('desc', 'Maior para Menor'),
            ('asc', 'Menor para Maior')
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    ) 