from django.db import models
from django.conf import settings


""" Creamos las tablas correspondientes
a los datos del usuario"""

####PROVINCE MODEL
"""
    <----Modelo para representar una provincia en Argentina.---->
"""
class Province(models.Model):

    name_province = models.CharField( max_length=80, null=True, blank=True, verbose_name='Nombre de provincia', unique=True)
    def __str__(self):
        return f'{self.name_province}'
    class Meta:
        verbose_name = "Provincia"
        verbose_name_plural = "Provincias"
        ordering = ['name_province']
####CITY MODEL
"""
<----Modelo para representar una ciudad en Argentina.---->
"""
class City(models.Model):
    province_fk = models.ForeignKey(Province, on_delete=models.RESTRICT, null=True, blank=True, related_name='cities')
    name_city = models.CharField(max_length=100, null=True, blank=True, verbose_name='Nombre de ciudad', unique=True)
    zipcode = models.CharField( max_length=10, null=True, blank=True, unique=True)
    def __str__(self):
        return f'{self.name_city}'
    class Meta:
        verbose_name = 'Ciudad'
        verbose_name_plural = 'Ciudades'
        ordering = ['name_city']
    
####USER PROFILE MODEL
"""
    <----Modelo que extiende el modelo User de Django con información adicional
    específica del perfil de usuario, como datos de contacto, dirección y
    condiciones fiscales.---->
"""
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile') 
    #DOCUMENTS
    TYPE_DOCUMENTS = [('DNI','Documentos de identidad'), ('CUIT', 'CUIT/CUIL'), ('LIB', 'LIBRETA UNICA')]
    type_document = models.CharField(max_length=10, choices=TYPE_DOCUMENTS, default='DNI', verbose_name='Tipo de documento')
    document = models.CharField(max_length=20,  null = True, blank = True, verbose_name = 'Documento')
    #TAX INFORMATION
    TAX_CONDITIONS = [('CF', 'Consumidor Final'), ('MO', 'Monotributista'), ('RI', 'Responsable Inscripto'), ('EX', 'Exento'),]
    tax_condition = models.CharField(max_length = 20 , null=True, blank=True,choices=TAX_CONDITIONS, default = 'CF', verbose_name='Condición IVA')
    business_name = models.CharField(max_length=255, null = True, blank=True, verbose_name='Razón social')
    #CONTACT & ADDRESS
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name='Contacto')
    province_fk = models.ForeignKey(Province, on_delete=models.RESTRICT, null = True, blank=True, verbose_name='Provincia')
    city_fk = models.ForeignKey(City, on_delete=models.RESTRICT, null=True, blank=True, verbose_name='Ciudad/departamento')
    zipcode = models.CharField(max_length=150, null=True, blank=True, verbose_name='Código postal')
    street_name = models.CharField(max_length=255, null=True, blank=True,verbose_name='Calle/Barrio')
    street_number = models.CharField(max_length=100, null=True, blank=True, verbose_name='Altura/Número')
    #EXTRA INFO
    apartament = models.CharField(max_length=255, null=True, blank=True, verbose_name='Departamento(opcional)')
    extra_info = models.CharField(max_length=255, null=True, blank=True, verbose_name='Información extra (opcional)')
    is_verified = models.BooleanField(default=False, verbose_name='Usuario verificado')
    class Meta:
        verbose_name = 'Perfil de usuario'
        verbose_name_plural = 'Perfiles de usuarios'
        