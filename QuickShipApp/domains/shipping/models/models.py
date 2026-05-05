from django.db import models
from django.conf import settings
from django.utils import timezone
"""
<--- En este módulo se administrarán los modelos
de pedidos registrados --->

"""

###SHIPPING MODEL
class Shipping(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, related_name='shipping' )
    shipping_number = models.CharField(max_length=20, null=True, blank=True, verbose_name='Número de factura')
    tracking_code = models.CharField(max_length=30, null=True, blank=True, verbose_name='Código de seguimiento')
    shipping_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='Precio de envío')
    total_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='Precio total')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Envío {self.shipping_number or self.id} para {self.user.username}"

    class Meta:
        verbose_name = "Envío"
        verbose_name_plural = "Envíos"
        ordering = ['-created_at']

###DETAIL SHIPPING
"""
Este modelo se encarga de registrar los datos.
del remitente y el destinatario para un envío ya registrado.
"""
class DataShipping(models.Model):
    shipping_fk = models.OneToOneField(Shipping, on_delete=models.CASCADE, related_name='data_shipping')
    #SENDER INFROMATION
    sender_name = models.CharField(max_length=255, verbose_name='Nombre del remitente')
    SENDER_TYPE_DOCUMENTS = [('DNI','Documentos de identidad'), ('CUIT', 'CUIT/CUIL'), ('LIB', 'LIBRETA UNICA')]
    sender_type_document = models.CharField(max_length=10, choices=SENDER_TYPE_DOCUMENTS, default='DNI', verbose_name='Tipo de documento del remitente')
    sender_document = models.CharField(max_length=20, null=True, blank=True, verbose_name='Documento del remitente') 
    SENDER_TAX_CONDITIONS = [('CF', 'Consumidor Final'), ('MO', 'Monotributista'), ('RI', 'Responsable Inscripto'), ('EX', 'Exento'),]
    sender_tax_condition = models.CharField(max_length=20, choices=SENDER_TAX_CONDITIONS, default='CF', verbose_name='Condición fiscal del remitente')
    sender_business_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='Razón social del remitente')
    sender_email = models.EmailField(max_length=255, verbose_name='Correo electrónico del remitente')
    sender_number_phone = models.CharField(max_length=20, null=True, blank=True, verbose_name='Número de teléfono del remitente')
    # ORIGIN INFORMATION
    origin_province = models.CharField(max_length=80, verbose_name='Provincia de origen')
    origin_city = models.CharField(max_length=100, verbose_name='Ciudad de origen')
    origin_zipcode = models.CharField(max_length=10, verbose_name='Código postal de origen')
    origin_address = models.CharField(max_length=255, verbose_name='Dirección de origen')
    # RECEIVER INFORMATION 
    receiver_name = models.CharField(max_length=255, verbose_name='Nombre del destinatario')
    RECEIVER_TYPE_DOCUMENTS = [('DNI','DNI'),('CUIT','CUIT/CUIL'), ('LIB','LIBRETA UNICA')]
    receiver_type_document = models.CharField(max_length=20, choices=RECEIVER_TYPE_DOCUMENTS, default='DNI', verbose_name='Tipo de documento del destinatario')
    receiver_document = models.CharField(max_length=20, null=True, blank=True, verbose_name='Documento del destinatario') 
    RECEIVER_TAX_CONDITIONS = [('CF', 'Consumidor Final'), ('MO', 'Monotributista'), ('RI', 'Responsable Inscripto'), ('EX', 'Exento'),]
    receiver_tax_condition = models.CharField(max_length=20, choices=RECEIVER_TAX_CONDITIONS, default='CF', verbose_name='Condición fiscal del destinatario')
    receiver_business_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='Razón social del destinatario')
    receiver_email = models.EmailField(max_length=255, null=True, blank=True, verbose_name='Correo electrónico del destinatario') 
    receiver_number_phone = models.CharField(max_length=20, null=True, blank=True, verbose_name='Número de teléfono del destinatario') 
    # DESTINATION INFORMATION
    destination_province = models.CharField(max_length=80, verbose_name='Provincia de destino')
    destination_city = models.CharField(max_length=100, verbose_name='Ciudad de destino')
    destination_zipcode = models.CharField(max_length=10, verbose_name='Código postal de destino')
    destination_address = models.CharField(max_length=255, verbose_name='Dirección de destino')
    destination_extra_info = models.CharField(max_length=255, null=True, blank=True, verbose_name='Información extra de destino')

    def __str__(self):
        return f"Datos de Envío {self.shipping_fk.shipping_number or self.shipping_fk.id}"

    class Meta:
        verbose_name = "Datos de Envío"
        verbose_name_plural = "Datos de Envíos"


###DETAIL SHIPPING MODEL
"""
Este modelo se encarga de registrar
los detalles de los productos que se enviaron.
"""
class DetailShipping(models.Model):
    shipping_fk = models.ForeignKey(Shipping, on_delete=models.CASCADE, related_name='details_shipping')
    description = models.CharField(max_length=255, verbose_name='Descripción del producto')
    weight = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Peso (kg)')
    height = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Alto (cm)')
    width = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Ancho (cm)')
    length = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Largo (cm)')
    quantity = models.IntegerField(default=1, verbose_name='Cantidad')
    weight_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Precio por peso/volumen')
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Subtotal')

    def __str__(self):
        return f"Detalle para Envío {self.shipping_fk.shipping_number or self.shipping_fk.id}: {self.description}"

    class Meta:
        verbose_name = "Detalle de Envío"
        verbose_name_plural = "Detalles de Envíos"


###SHIPPING STATUS MODEL
"""
Este modelo registra el estado actual y el historial de un envío.
"""
class ShippingStatus(models.Model):
    shipping_fk = models.OneToOneField(Shipping, on_delete=models.CASCADE, related_name='status')
    STATUS_CHOICES = [
        ('PENDING', 'Pendiente'),
        ('PROCESSING', 'En Proceso'),
        ('IN_TRANSIT', 'En Tránsito'),
        ('DELIVERED', 'Entregado'),
        ('CANCELLED', 'Cancelado'),
        ('RETURNED', 'Devuelto'),
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='PENDING', verbose_name='Estado del envío')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última actualización de estado')

    def __str__(self):
        return f"Estado de Envío {self.shipping_fk.shipping_number or self.shipping_fk.id}: {self.get_status_display()}"

    class Meta:
        verbose_name = "Estado de Envío"
        verbose_name_plural = "Estados de Envíos"
        ordering = ['-updated_at']