from django.db import models
from django.utils import timezone
"""

Este modulo contiene los models encargados de administrar los precios del sistema

"""


####PRICE BASE MODEL
"""
Model encargado de administrar los precios

"""
class PriceBase(models.Model):
    shipment_price = models.DecimalField(max_digits=12, decimal_places=2, default = 8000, verbose_name='Precio de envio')
    weight_price = models.DecimalField(max_digits=12, decimal_places=2, default = 450 ,verbose_name = 'Precio por kilo')
    volumetric_divider = models.IntegerField(default = 4000, verbose_name = 'Divisor volumetrico')
    update_data = models.DateTimeField (default= timezone.now)
    
    