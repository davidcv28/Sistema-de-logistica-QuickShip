from django.core.management import BaseCommand
from django.contrib.auth.models import User
from QuickShipApp.domains.user.models import UserProfile
from django.db import transaction
class Command(BaseCommand):
    def handle(self, *args, **options):
        with transaction.atomic():
            password_admin = 'Atre21lj@'
            admin,created = User.objects.get_or_create(
                username = 'admin', defaults={
                    'first_name':'Administrador',
                    'last_name':'QuickShip',
                    'email': 'admin@gmail.com',
                    'is_staff': True,
                    'is_superuser':True
                }
            )
            if created:
                self.stdout.write(self.style.WARNING('CARGANDO CUENTA ADMINISTRADOR'))
                admin.set_password(password_admin)
                admin.save()
                self.stdout.write(self.style.SUCCESS('CUENTA ADMIN CARGADA'))
            
            