from django.core.management import BaseCommand
from QuickShipApp.domains.prices.models.models import PriceBase


class Command(BaseCommand):
    """
    Comando para cargar un precio base de envío por defecto si no existe.
    """
    def handle(self, *args, **options):
        """
        Crea un registro de precio base inicial si no hay ninguno en la base de datos.
        """
        prices = PriceBase.objects.all()
        if not prices:
            self.stdout.write(self.style.WARNING('CARGANDO PRECIOS BASES'))
            PriceBase.objects.create()
            self.stdout.write(self.style.SUCCESS('PRECIOS CARGADOS'))