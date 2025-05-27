from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from core.models import PerfilUsuario


class CadastroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    data_nascimento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text='Informe sua data de nascimento'
    )
    aceita_localizacao = forms.BooleanField(
        required=False,
        label='Permitir uso da minha localização',
        help_text='Marque esta opção para permitir que o site utilize sua localização'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
            
            # Usar get_or_create para evitar duplicação
            perfil, created = PerfilUsuario.objects.get_or_create(
                usuario=user,
                defaults={
                    'data_nascimento': self.cleaned_data['data_nascimento'],
                    'aceita_localizacao': self.cleaned_data['aceita_localizacao']
                }
            )
            
            # Se o perfil já existia, atualizar os dados
            if not created:
                perfil.data_nascimento = self.cleaned_data['data_nascimento']
                perfil.aceita_localizacao = self.cleaned_data['aceita_localizacao']
            perfil.save()

        return user
