from django.db import models
from django.db.models import Sum
from QuickShipApp.domains.user.models import Province, City, UserProfile
from QuickShipApp.domains.prices.models.models import PriceBase
from django.conf import settings
from decimal import Decimal
import logging
logger = logging.getLogger(__name__)

"""
Este módulo se encargará de administrar los modelos.

 relacionadas con la vista previa de los pedidos

"""
######PENDING SHIPMENT MODEL
"""
Este modelo es el cuerpo de la vista previa del pedido.

aqui se muestran los datos del remitente y destinatario,

sumado al detalle de los productos que se enviaran y el total a pagar.

"""
class PendingShipment(models.Model):
    user_fk = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name='shipment' )
    def get_total_price(self, calculatorsub = None, calculatortotal_class = None):
        if calculatorsub is None or calculatortotal_class is None:
            try:
                from .logic import  CalculateTotalPrice, CalculateSubTotal
                calculatortotal_class = CalculateTotalPrice
                calculatorsub = CalculateSubTotal
            except(AttributeError, ImportError) as e:
                logger.error(f'Error crítico: no se pudo encontrar una clase {e}')
                return Decimal('0.00')
        details = self.details.all()
        if details:
            list_price = [calculatorsub(detail.weight, detail.height, detail.length, detail.width, detail.quantity).calculate() for detail in details]
            total_price = Decimal(str(CalculateTotalPrice(list_price).calculate()))
            return round(total_price, 2)
        return 0
      

        
#######DATA SHIPMENT MODEL
"""
Este modelo se encarga de registrar los datos.

del remitente y el destinatario.

"""
class Data(models.Model):
    shipment_fk = models.OneToOneField(PendingShipment, on_delete=models.CASCADE, related_name='data')
    origin_province = models.ForeignKey(Province, on_delete=models.RESTRICT, null = True, blank=True, verbose_name='Provincia de origen', related_name='origin_province')
    origin_city = models.ForeignKey(City, on_delete=models.RESTRICT, null=True, blank=True, verbose_name='Ciudad de origen', related_name='origin_city')
    origin_zipcode = models.CharField(max_length=10, null=True, blank=True,  verbose_name='Código postal de origen')
    origin_address = models.CharField(max_length=255, null=True, blank=True, verbose_name='Origen de paquete')
    receiver = models.CharField(max_length=255, null=True, blank=True, verbose_name='Nombre del destinatario')
    TYPE_DOC = [('DNI','DNI'),('CUIT','CUIT/CUIL'), ('LIB','LIBRETA  UNICA') ]
    receiver_type_document = models.CharField(max_length=20, default='DNI', choices=TYPE_DOC)
    TAX_CONDITIONS = [('CF', 'Consumidor Final'), ('MO', 'Monotributista'), ('RI', 'Responsable Inscripto'), ('EX', 'Exento'),]
    receiver_tax_condition = models.CharField(max_length=20,  default='CF', choices=TAX_CONDITIONS, verbose_name='Condición fiscal')
    receiver_business_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='Razón social')
    receiver_document = models.CharField(max_length=20, null = True, blank=True, verbose_name='Documento del destinatario')
    receiver_number_phone = models.CharField(max_length=20, null=True, blank=True, verbose_name='Número de celular')
    receiver_email = models.EmailField(max_length=255, null=True, blank=True, verbose_name='Correo electrónico')
    destination_province = models.ForeignKey(Province, on_delete=models.RESTRICT, verbose_name='Provincia', null = True, blank = True)
    destination_city = models.ForeignKey(City, on_delete=models.RESTRICT, verbose_name='Ciudad', null = True, blank = True)
    destination_zipcode = models.CharField(max_length=10, null=True, blank=True, verbose_name='Código postal')
    destination_address = models.CharField(max_length=255, null=True, blank=True, verbose_name='Domicilio')
    destination_extrainfo = models.CharField(max_length=255, null=True, blank=True, verbose_name='Información extra')
    TYPE_SHIPMEN = [('SUCURSAL', 'SUCURSAL'), ('DOMICILIO','DOMICILIO'),('EXPRESS','EXPRESS')]
    type_shipment = models.CharField(max_length=60, choices=TYPE_SHIPMEN, default='SUCURSAL')
"""
"""
######DETAILS MODEL
"""
Este modelo se encarga de registrar 

los detalles de los productos que se enviaran.

"""
class Details(models.Model):
    shipment_fk = models.ForeignKey(PendingShipment, on_delete=models.CASCADE, related_name='details')
    description = models.CharField(max_length=255, verbose_name='Descripción')
    weight = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Peso')
    height = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Alto')
    width = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Ancho')
    length = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Largo')
    quantity = models.IntegerField(default = 1 , verbose_name='Cantidad')
    def get_weight_price(self, calculator_class = None):
        if calculator_class is None:
            try:
                from .logic import CalculateWeightPrice
                calculator_class = CalculateWeightPrice
            except(ImportError, AttributeError) as e:
                logger.error(f'Error crítico al importar CalculateWeightPrice: {e}')
                return Decimal('0.00')
            return calculator_class(self.weight, self.height, self.length, self.width).calculate()
                
    def get_subtotal(self, calculator_class = None):
        if  calculator_class is None:
            try:
                from .logic import CalculateSubTotal
                calculator_class = CalculateSubTotal
            except (ImportError, AttributeError) as e:
                logger.error(f'Error crítico al importar CalculateSubTotal: {e}')
                return Decimal('0.00')
        return calculator_class(self.weight, self.height, self.length, self.width, self.quantity).calculate()



    