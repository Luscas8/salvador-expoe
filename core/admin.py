from django.contrib import admin
from .models import Bairro, Avaliacao, PerfilUsuario


@admin.register(Bairro)
class BairroAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)


@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'bairro', 'nota', 'data_criacao')
    list_filter = ('bairro', 'nota')
    search_fields = ('usuario__username', 'bairro__nome', 'comentario')
    date_hierarchy = 'data_criacao'


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'data_nascimento', 'aceita_localizacao', 'data_atualizacao')
    search_fields = ('usuario__username', 'bio')
    list_filter = ('data_nascimento', 'aceita_localizacao', 'data_atualizacao')
    readonly_fields = ('data_atualizacao',)
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('usuario', 'data_nascimento', 'foto', 'bio')
        }),
        ('Preferências', {
            'fields': ('aceita_localizacao',)
        }),
        ('Localização', {
            'fields': ('latitude', 'longitude')
        }),
        ('Metadados', {
            'fields': ('data_atualizacao',)
        })
    )
