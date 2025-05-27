from django.core.management.base import BaseCommand
from core.models import Bairro

class Command(BaseCommand):
    help = 'Lista bairros com coordenadas fora da área de Salvador'

    def handle(self, *args, **options):
        suspeitos = []
        for b in Bairro.objects.all():
            try:
                lat = float(b.latitude)
                lng = float(b.longitude)
                if not (-13.1 < lat < -12.8 and -38.7 < lng < -38.3):
                    suspeitos.append((b.nome, lat, lng))
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Bairro '{b.nome}' com coordenada inválida: {b.latitude}, {b.longitude} ({e})"))
        if suspeitos:
            self.stdout.write(self.style.ERROR('Bairros com coordenadas suspeitas:'))
            for nome, lat, lng in suspeitos:
                self.stdout.write(f"{nome}: lat={lat}, lng={lng}")
        else:
            self.stdout.write(self.style.SUCCESS('Nenhum bairro suspeito encontrado!')) 