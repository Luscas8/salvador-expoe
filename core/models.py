from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Bairro(models.Model):
    nome = models.CharField(max_length=100)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Bairro'
        verbose_name_plural = 'Bairros'
        ordering = ['nome']


class Avaliacao(models.Model):
    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='avaliacoes')
    bairro = models.ForeignKey(
        Bairro, on_delete=models.CASCADE, related_name='avaliacoes')
    nota = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)])
    comentario = models.TextField(blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Avaliação de {self.usuario.username} para {self.bairro.nome}: {self.nota}"

    class Meta:
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'
        ordering = ['-data_criacao']
        # Garantir que um usuário só possa avaliar um bairro uma vez
        unique_together = ('usuario', 'bairro')


class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='perfil'
    )
    data_nascimento = models.DateField(null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    foto = models.ImageField(upload_to='perfis/', null=True, blank=True)
    aceita_localizacao = models.BooleanField(default=False)
    # Coordenadas padrão de Salvador
    latitude = models.FloatField(
        default=-12.9714,
        validators=[
            MinValueValidator(-90),
            MaxValueValidator(90)
        ]
    )
    longitude = models.FloatField(
        default=-38.5014,
        validators=[
            MinValueValidator(-180),
            MaxValueValidator(180)
        ]
    )
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Perfil de {self.usuario.username}"

    class Meta:
        verbose_name = 'Perfil de Usuário'
        verbose_name_plural = 'Perfis de Usuários'

@receiver(post_save, sender=User)
def criar_ou_atualizar_perfil_usuario(sender, instance, created, **kwargs):
    """
    Signal para criar ou atualizar o perfil do usuário automaticamente
    """
    if created:
        PerfilUsuario.objects.create(usuario=instance)
    else:
        # Se o perfil não existir, cria um novo
        PerfilUsuario.objects.get_or_create(usuario=instance)

@receiver(post_save, sender=User)
def salvar_perfil_usuario(sender, instance, **kwargs):
    instance.perfil.save()
