from rest_framework import serializers
from QuickShipApp.domains.shipping.models import DataShipping, DetailShipping, ShippingStatus
from QuickShipApp.domains.user.models import Province, City
from QuickShipApp.domains.prices.models import PriceBase
from decimal import Decimal
"""
Lógica de negocio para la conversión de borrador a envío real.
"""
####VALIDATE LOGIC USER FUNCTION
def validate_logic_user(user_profile, pendingshipment):
    """
    Verifica que el usuario tenga su perfil completo antes de confirmar el envío.
    """
    errors = []

    if not user_profile.user.first_name:
        errors.append('Por favor, rellene el campo nombre en su perfil')
    if not user_profile.user.last_name:
        errors.append('Por favor, rellene el campo apellido en su perfil')

    list_data_user = ['document', 'phone_number']
    for item in list_data_user:
        if not getattr(user_profile, item, None):
            errors.append(f'Por favor, rellene el campo {item} en su perfil')
    
    if not hasattr(pendingshipment, 'data') or pendingshipment.data is None:
        errors.append('Por favor cargue los datos del destinatario')
    if not pendingshipment.details.all().exists():
        errors.append('Por favor cargue los productos que desea enviar')
    if errors:
        raise serializers.ValidationError(errors)
####REGISTER DATA FUNCTION
def add_data_shipment(shipping, user, profile, pendingshipment):
    data_receiver = pendingshipment.data
    """
    Guarda todos los datos del remitente y destinatario vinculados a este envío.
    """
    DataShipping.objects.create(
        #SENDER
        shipping_fk = shipping,
        sender_name = f'{user.first_name} {user.last_name}',
        sender_type_document = profile.type_document,
        sender_document = profile.document,
        sender_tax_condition = profile.tax_condition,
        sender_business_name = profile.business_name,
        sender_email = user.email,
        sender_number_phone = profile.phone_number,
        #ORIGIN
        origin_province = profile.province_fk.name_province,
        origin_city = profile.city_fk.name_city,
        origin_zipcode = profile.city_fk.zipcode, 
        origin_address = data_receiver.origin_address,
        #RECEIVER
        receiver_name = data_receiver.receiver,
        receiver_type_document = data_receiver.receiver_type_document,
        receiver_document = data_receiver.receiver_document,
        receiver_tax_condition = data_receiver.receiver_tax_condition,
        receiver_business_name = data_receiver.receiver_business_name,
        receiver_email = data_receiver.receiver_email,
        receiver_number_phone = data_receiver.receiver_number_phone,
        #DESTINATION
        destination_province = data_receiver.destination_province.name_province,
        destination_city = data_receiver.destination_city.name_city,
        destination_zipcode = data_receiver.destination_zipcode,
        destination_address = data_receiver.destination_address,
        destination_extra_info = data_receiver.destination_extrainfo
    )
####CLEAN DATA SHIPMENT
def clean_data_pendingshipment(pendingshipment):
    """
    Limpia los datos del borrador para que el usuario pueda cargar un envío nuevo.
    """
    shipment = pendingshipment.data
    shipment.origin_province = Province.objects.get(id = 1)
    shipment.origin_city = City.objects.get(id = 1)
    shipment.origin_zipcode = City.objects.get(id = 1).zipcode
    shipment.origin_address = ''
    shipment.receiver = ''
    shipment.receiver_type_document = 'DNI'
    shipment.receiver_tax_condition  = 'CF'
    shipment.receiver_business_name = ''
    shipment.receiver_document = ''
    shipment.receiver_number_phone = '' 
    shipment.receiver_email = ''
    shipment.destination_province = Province.objects.get(id=1) 
    shipment.destination_city =City.objects.get(id = 1)
    shipment.destination_zipcode =City.objects.get(id = 1).zipcode 
    shipment.destination_address = ''
    shipment.destination_extrainfo = ''
    shipment.type_shipment = 'DOMICILIO'
    shipment.save()
####REGISTER DETAILS FUNCTION
def add_detail_shipment(shipping, pendingshipment):
    details = pendingshipment.details.all()
    """
    Pasa los productos del borrador al envío definitivo y calcula los subtotales.
    """
    list_details = []
    for detail in details:
        detail_item = DetailShipping(
            shipping_fk = shipping,
            description = detail.description,
            weight = detail.weight,
            height = detail.height,
            width = detail.width,
            length = detail.length,
            quantity= detail.quantity,
            weight_price = detail.get_weight_price(),
            subtotal = detail.get_subtotal()
        )
        list_details.append(detail_item)
    DetailShipping.objects.bulk_create(list_details,ignore_conflicts=True)
####REGISTER STATUS FUNCTION
def add_status_shipment(shipping):
    """
    Crea el estado inicial del envío como 'Pendiente'.
    """
    ShippingStatus.objects.create(shipping_fk = shipping)
####SHIPING PRICE
def add_shipping_price():
    """
    Busca el precio de envío base más reciente en la configuración.
    """
    shipping_base_price= PriceBase.objects.all().latest('id')
    shipping_price = shipping_base_price.shipment_price
    return shipping_price
### TOTAL PRICE FUNCTION
def total_price(shipping_instance):
    """
    Suma los subtotales de todos los productos para obtener el precio final del envío.
    """
    totalprice =Decimal(0)
    map_details = shipping_instance.details_shipping.all()
    for detail in map_details:
        totalprice += Decimal(detail.subtotal)
    return totalprice