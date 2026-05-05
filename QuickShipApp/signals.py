from django.db.models.signals import post_save
from django.dispatch import receiver
from QuickShipApp.domains.shipping.models import Shipping
import random, string

"""
<--- En este módulo vamos a generar el Número de envío y código de seguimiento --->

"""

@receiver(post_save, sender = Shipping)
def new_number_shipping(sender, instance, created,  **kwargs):
    if created:
        characters = string.ascii_uppercase + string.digits
        while True:
            new_tracking_code = ''.join(random.choices(characters, k=10))
            if Shipping.objects.filter(tracking_code__iexact = new_tracking_code).exists():
                continue
            break        
        # Actualizamos los atributos de la instancia directamente
        instance.shipping_number = f'ENV-{instance.id:08d}'
        instance.tracking_code = new_tracking_code
        # Usamos update para guardar solo estos campos sin disparar señales recursivas
        Shipping.objects.filter(pk=instance.pk).update(
            shipping_number=instance.shipping_number, 
            tracking_code=instance.tracking_code
        )
        
