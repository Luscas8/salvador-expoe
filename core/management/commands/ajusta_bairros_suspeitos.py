from django.core.management.base import BaseCommand
from core.models import Bairro

class Command(BaseCommand):
    help = 'Ajusta ou remove bairros com coordenadas suspeitas ou inválidas (interativo)'

    def handle(self, *args, **options):
        suspeitos = []
        for b in Bairro.objects.all():
            try:
                lat = float(b.latitude)
                lng = float(b.longitude)
                if not (-13.1 < lat < -12.8 and -38.7 < lng < -38.3):
                    suspeitos.append(b)
            except Exception:
                suspeitos.append(b)
        if not suspeitos:
            self.stdout.write(self.style.SUCCESS('Nenhum bairro suspeito encontrado!'))
            return
        for b in suspeitos:
            self.stdout.write(self.style.WARNING(f"Bairro: {b.nome} | lat: {b.latitude} | lng: {b.longitude}"))
            acao = input("[C]orrigir / [E]xcluir / [P]ular? ").strip().lower()
            if acao == 'c':
                nova_lat = input("Nova latitude: ").strip()
                nova_lng = input("Nova longitude: ").strip()
                try:
                    b.latitude = float(nova_lat)
                    b.longitude = float(nova_lng)
                    b.save()
                    self.stdout.write(self.style.SUCCESS(f"Bairro '{b.nome}' atualizado!"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Erro ao atualizar: {e}"))
            elif acao == 'e':
                b.delete()
                self.stdout.write(self.style.SUCCESS(f"Bairro '{b.nome}' excluído!"))
            else:
                self.stdout.write("Pulando...") 