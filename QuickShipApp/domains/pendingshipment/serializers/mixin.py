from rest_framework import serializers
from QuickShipApp.domains.pendingshipment.models import PendingShipment, Details, Data
from QuickShipApp.domains.user.models.models import Province, City, UserProfile
from QuickShipApp.domains.pendingshipment.serializers.mixins_logic import validate_tax_conditions, validate_document_format

"""
<--- Este modulo se encarga de las validaciones correspondiente al modulo pendingshipmentserializer.py ---> 

"""

#####DATA SHIPMENT SERIALIZER

class UpdatePendingShipmentDataMixin:
    """
    Validaciones complejas de geografía y fiscalidad para borradores.
    """
    def validate(self, attrs):
        """
        Valida que los datos de origen y destino sean coherentes y que la información fiscal
        del destinatario sea correcta.
        """
        origin_province = attrs.get('origin_province')
        origin_city = attrs.get('origin_city')
        origin_address = attrs.get('origin_address')
        destination_province = attrs.get('destination_province')
        destination_city = attrs.get('destination_city')
        destination_address = attrs.get('destination_address')
        receiver_type_document = attrs.get('receiver_type_document')
        receiver_document = attrs.get('receiver_document')
        receiver_tax_condition = attrs.get('receiver_tax_condition')
        receiver_business_name = attrs.get('receiver_business_name')
        user = self.context.get('request').user
        errors = {}
        validate_document = validate_document_format(receiver_document, receiver_type_document)
        validate_tax_condition = validate_tax_conditions(receiver_type_document, receiver_tax_condition, receiver_business_name)
        if validate_document:
            errors |= validate_document
        if validate_tax_condition:
            errors |= validate_tax_condition
        if origin_city not in origin_province.cities.all():
            errors['origin_city'] = f'{origin_city} no se encuentra en {origin_province}'
        if destination_city not in destination_province.cities.all():
            errors['destination_city'] = f'{destination_city} no se encuentra en {destination_province}'
        if destination_city == origin_city and destination_address == origin_address:
            errors['destination_address'] = 'No puedes hacer un envio al mismo domicilio de origen'
        if errors:
            raise serializers.ValidationError(errors)
        attrs['origin_zipcode'] = origin_city.zipcode
        attrs['destination_zipcode'] = destination_city.zipcode
        attrs['shipment_fk'] = PendingShipment.objects.get(user_fk = user)
        return attrs

####DETAILS SHIPMENT MIXIN
class RegisterPendingShipmentDetailMixin:
    """
    Lógica de creación o actualización de ítems en el borrador.
    """

    def create(self, validated_data):
        """
        Crea o actualiza un ítem en el borrador de envío, usando la descripción como identificador.
        """
        object_detail = validated_data['description']
        user = self.context.get('request').user
        validated_data['shipment_fk'] = PendingShipment.objects.get(user_fk = user)
        instance_detail, created =Details.objects.update_or_create(
            description = object_detail, defaults={
                'shipment_fk' : validated_data['shipment_fk'],
                'weight' : validated_data['weight'],
                'height' : validated_data['height'],
                'width' : validated_data['width'],
                'length' : validated_data['length'],
                'quantity' : validated_data['quantity']
            }
        )
        return instance_detail
        
    