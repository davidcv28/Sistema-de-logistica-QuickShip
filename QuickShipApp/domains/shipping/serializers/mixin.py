from rest_framework import serializers
from django.db import transaction
from QuickShipApp.domains.pendingshipment.serializers import ListPendingShipment
from QuickShipApp.domains.shipping.models import Shipping, DataShipping, DetailShipping
from .mixins_logic import (validate_logic_user, add_data_shipment, add_detail_shipment,
                           add_status_shipment, total_price, add_shipping_price, clean_data_pendingshipment)
from decimal import Decimal
"""
<--- Este módulo se encarga de administrar la lógica para el serializer de shipping --->

"""

####MIXIN SHIPPING REGISTER METHOD
class MixinShippingRegisterMethod:
    def create(self, validated_data):
        user = self.context['request'].user
        profile = user.profile
        pendingshipment = user.shipment
        validate_logic_user(profile, pendingshipment)
        with transaction.atomic():
            shipping_instance = super().create(validated_data)
            add_data_shipment(shipping_instance, user, profile, pendingshipment)
            add_detail_shipment(shipping_instance, pendingshipment)
            add_status_shipment(shipping_instance)
            shipping_instance.shipping_price = round(Decimal(add_shipping_price()), 2)
            shipping_instance.total_price = round(Decimal(total_price(shipping_instance)), 2)
            clean_data_pendingshipment(pendingshipment)
            pendingshipment.details.all().delete()
            shipping_instance.save()
            shipping_instance.refresh_from_db()
            return shipping_instance
          
            